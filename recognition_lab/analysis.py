"""Transparent feature analysis for manually verified Phase 1 candidates."""

from __future__ import annotations

import json
import hashlib
import time
from statistics import mean
from typing import Any

import cv2
import numpy as np


FEATURES = (
    "area_ratio", "aspect_ratio", "rectangularity", "edge_support",
    "perspective_distortion", "rotation", "sharpness", "frame_margin",
    "position_stability", "tracking_duration",
)


def build_outer_profile(rows: list[Any]) -> dict[str, Any]:
    """Build an explicit positive/negative feature profile from saved labels."""
    groups: dict[str, list[dict[str, float]]] = {"correct": [], "incorrect": []}
    for record in _records(rows):
        groups[record["judgment"]].append(record["features"])
    profile: dict[str, Any] = {"correct_count": len(groups["correct"]), "incorrect_count": len(groups["incorrect"]), "features": {}}
    for feature in FEATURES:
        values = {}
        for label in ("correct", "incorrect"):
            samples = [item[feature] for item in groups[label]]
            values[label] = {
                "mean": mean(samples) if samples else None,
                "std": max(float(np.std(samples)), 0.02) if samples else None,
            }
        profile["features"][feature] = values
    return profile


def score_outer_candidate(metrics: dict[str, Any], profile: dict[str, Any] | None) -> float:
    """Return a comparative supervision score; it never becomes ground truth."""
    if not profile or profile.get("correct_count", 0) == 0:
        return 0.0
    correct_distance = 0.0
    incorrect_distance = 0.0
    used = 0
    for feature in FEATURES:
        value = float(metrics.get(feature, 0.0) or 0.0)
        distributions = profile["features"].get(feature, {})
        positive = distributions.get("correct", {})
        negative = distributions.get("incorrect", {})
        if positive.get("mean") is None:
            continue
        correct_distance += abs(value - positive["mean"]) / positive["std"]
        if negative.get("mean") is not None:
            incorrect_distance += abs(value - negative["mean"]) / negative["std"]
        used += 1
    if not used:
        return 0.0
    separation = (incorrect_distance - correct_distance) / used
    return round(float(1.0 / (1.0 + np.exp(-separation))), 4)


def benchmark_annotations(
    rows: list[Any], detect_fn, limit: int | None = None,
) -> dict[str, Any]:
    """Measure generation first, then ranking, with a session-held-out split."""
    correct_rows = [row for row in rows if row["judgment"] == "correct"]
    incorrect_rows = [row for row in rows if row["judgment"] == "incorrect"]
    if limit is not None:
        correct_rows = correct_rows[:limit]

    def candidate_match(image: np.ndarray, target: np.ndarray, candidate: dict[str, Any]) -> tuple[float, float]:
        points = np.float32(candidate["points"])
        mask_target = np.zeros(image.shape[:2], dtype=np.uint8)
        mask_candidate = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask_target, [np.int32(target)], 1)
        cv2.fillPoly(mask_candidate, [np.int32(points)], 1)
        intersection = np.logical_and(mask_target, mask_candidate).sum()
        union = np.logical_or(mask_target, mask_candidate).sum()
        iou = float(intersection / union) if union else 0.0
        error = float(np.mean(np.linalg.norm(points - target, axis=1))) / max(
            np.hypot(image.shape[1], image.shape[0]), 1.0
        )
        return iou, error

    def evaluate_group(
        group: list[Any], profile: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        matches = []
        misses = 0
        top_matches = 0
        ranks = []
        accepted = 0
        for row in group:
            image = cv2.imread(str(row["frame_path"])) if row["frame_path"] else None
            if image is None:
                misses += 1
                continue
            target = np.float32(json.loads(row["corners_json"]))
            generated = detect_fn(image, rank_candidates=False, max_candidates=1000)
            ranked = detect_fn(image, rank_candidates=True, max_candidates=1000)
            scored = [candidate_match(image, target, candidate) for candidate in generated]
            best_iou, best_error = max(scored, default=(0.0, 0.0), key=lambda item: item[0])
            if best_iou >= 0.5:
                matches.append((best_iou, best_error))
            else:
                misses += 1
            ranked_scores = [candidate_match(image, target, candidate)[0] for candidate in ranked]
            ranked_match = max(ranked_scores, default=0.0)
            if ranked_scores and ranked_scores[0] >= 0.5:
                top_matches += 1
            if ranked_match >= 0.5:
                ranks.append(ranked_scores.index(ranked_match) + 1)
            if row["judgment"] == "incorrect" and ranked_scores:
                top = ranked[0]
                if (
                    ranked_scores[0] >= 0.5
                    and top["metrics"].get("outer_reference_score", 0.0) >= 0.35
                    and not top["metrics"].get("likely_internal_region", False)
                ):
                    accepted += 1
        total = len(group)
        return {
            "total": total,
            "matched": len(matches),
            "missed": misses,
            "recall": len(matches) / total if total else None,
            "mean_iou": mean([item[0] for item in matches]) if matches else None,
            "mean_corner_error": mean([item[1] for item in matches]) if matches else None,
            "top1_accuracy": top_matches / total if total else None,
            "mean_rank": mean(ranks) if ranks else None,
            "accepted": accepted,
        }

    profile = build_outer_profile(rows)
    generation = evaluate_group(correct_rows)
    ranking = evaluate_group(correct_rows, profile)
    negative = evaluate_group(incorrect_rows, profile)

    sessions = sorted({row["session_id"] for row in correct_rows})
    held_out_session = sessions[-1] if len(sessions) > 1 else None
    held_out_rows = [row for row in correct_rows if row["session_id"] == held_out_session]
    training_rows = [row for row in rows if row["session_id"] != held_out_session]
    held_out_profile = build_outer_profile(training_rows) if held_out_session else None
    held_out = evaluate_group(held_out_rows, held_out_profile) if held_out_rows else None
    return {
        "references": generation["total"],
        "matched": generation["matched"],
        "missed": generation["missed"],
        "recall": generation["recall"],
        "mean_iou": generation["mean_iou"],
        "mean_corner_error": generation["mean_corner_error"],
        "generation_recall": generation["recall"],
        "no_outer_boundary_generated": generation["missed"],
        "ranking_top1_accuracy": ranking["top1_accuracy"],
        "ranking_mean_match_rank": ranking["mean_rank"],
        "held_out_session": held_out_session,
        "held_out_references": held_out["total"] if held_out else 0,
        "held_out_recall": held_out["recall"] if held_out else None,
        "held_out_ranking_top1_accuracy": held_out["top1_accuracy"] if held_out else None,
        "held_out_missed": held_out["missed"] if held_out else 0,
        "incorrect_reproduced": negative["matched"],
        "incorrect_reproduction_rate": negative["recall"],
        "internal_region_false_acceptance_rate": (
            negative["accepted"] / negative["total"] if negative["total"] else None
        ),
        "incorrect_unmatched": negative["missed"],
    }


def _records(rows: list[Any]) -> list[dict[str, Any]]:
    records = []
    for row in rows:
        if row["judgment"] not in {"correct", "incorrect"}:
            continue
        metrics = json.loads(row["metrics_json"])
        records.append({
            "judgment": row["judgment"],
            "features": {
                name: float(metrics.get(name, 0.0) or 0.0) for name in FEATURES
            },
        })
    return records


def feature_summary(rows: list[Any]) -> dict[str, Any]:
    records = _records(rows)
    summary: dict[str, Any] = {
        "correct": sum(item["judgment"] == "correct" for item in records),
        "incorrect": sum(item["judgment"] == "incorrect" for item in records),
        "eligible": len(records),
        "features": {},
    }
    for feature in FEATURES:
        correct = [item["features"][feature] for item in records if item["judgment"] == "correct"]
        incorrect = [item["features"][feature] for item in records if item["judgment"] == "incorrect"]
        summary["features"][feature] = {
            "correct_mean": mean(correct) if correct else None,
            "incorrect_mean": mean(incorrect) if incorrect else None,
        }
    return summary


def evaluate_centroid_ranker(rows: list[Any], minimum_per_class: int = 3) -> dict[str, Any]:
    """Evaluate a small held-out nearest-centroid baseline without extra packages."""
    records = _records(rows)
    correct = [item for item in records if item["judgment"] == "correct"]
    incorrect = [item for item in records if item["judgment"] == "incorrect"]
    if len(correct) < minimum_per_class or len(incorrect) < minimum_per_class:
        return {
            "ready": False,
            "message": f"Need at least {minimum_per_class} correct and "
                       f"{minimum_per_class} incorrect samples; currently "
                       f"{len(correct)} correct and {len(incorrect)} incorrect.",
        }
    # Hold out the last sample from each class. This is deterministic and avoids
    # presenting training performance as generalization.
    training = correct[:-1] + incorrect[:-1]
    held_out = correct[-1:] + incorrect[-1:]
    centroids = {}
    for label in ("correct", "incorrect"):
        samples = [item["features"] for item in training if item["judgment"] == label]
        centroids[label] = {
            feature: mean(sample[feature] for sample in samples) for feature in FEATURES
        }
    predictions = []
    for item in held_out:
        distances = {
            label: sum((item["features"][feature] - centroid[feature]) ** 2 for feature in FEATURES)
            for label, centroid in centroids.items()
        }
        predicted = min(distances, key=distances.get)
        predictions.append(predicted == item["judgment"])
    return {
        "ready": True,
        "method": "nearest-centroid",
        "held_out_samples": len(held_out),
        "held_out_accuracy": sum(predictions) / len(predictions),
        "message": "Experimental only; original candidate visibility and settings are unchanged.",
    }


def _candidate_iou_and_error(
    image: np.ndarray, target: np.ndarray, candidate: dict[str, Any],
) -> tuple[float, float]:
    points = normalize_corners(candidate["points"])
    target = normalize_corners(target)
    target_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    candidate_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.fillPoly(target_mask, [np.int32(target)], 1)
    cv2.fillPoly(candidate_mask, [np.int32(points)], 1)
    intersection = np.logical_and(target_mask, candidate_mask).sum()
    union = np.logical_or(target_mask, candidate_mask).sum()
    iou = float(intersection / union) if union else 0.0
    error = float(np.mean(np.linalg.norm(points - target, axis=1))) / max(
        np.hypot(image.shape[1], image.shape[0]), 1.0
    )
    return iou, error


def _is_internal_candidate(target: np.ndarray, candidate: dict[str, Any]) -> bool:
    target = normalize_corners(target)
    points = normalize_corners(candidate["points"])
    target_area = abs(float(cv2.contourArea(target)))
    candidate_area = abs(float(cv2.contourArea(points)))
    if candidate_area >= target_area * 0.85:
        return False
    contour = target.reshape(-1, 1, 2)
    return all(
        cv2.pointPolygonTest(contour, (float(point[0]), float(point[1])), False) >= -2
        for point in points
    )


def normalize_corners(points: Any) -> np.ndarray:
    """Normalize four corners to a stable clockwise image-coordinate order."""
    corners = np.float32(points).reshape(4, 2)
    center = corners.mean(axis=0)
    ordered = corners[
        np.argsort(np.arctan2(corners[:, 1] - center[1], corners[:, 0] - center[0]))
    ]
    if cv2.contourArea(ordered, oriented=True) < 0:
        ordered = ordered[::-1]
    return ordered


def audit_annotations(rows: list[Any]) -> dict[str, Any]:
    """Audit stored files and coordinates without changing any annotation."""
    from recognition_lab.engines import validate_quad_geometry

    duplicates: dict[str, list[int]] = {}
    near_duplicates: dict[str, list[int]] = {}
    dimensions: dict[str, int] = {}
    coordinate_bounds_valid = 0
    results = []
    for row in rows:
        image = cv2.imread(str(row["frame_path"])) if row["frame_path"] else None
        issues: list[str] = []
        corners = None
        try:
            corners = np.float32(json.loads(row["corners_json"])).reshape(4, 2)
        except (TypeError, ValueError, json.JSONDecodeError):
            issues.append("invalid four-corner JSON")
        if image is None:
            issues.append("image missing or undecodable")
        if corners is not None and image is not None:
            if not np.isfinite(corners).all():
                issues.append("non-finite coordinates")
            height, width = image.shape[:2]
            dimensions[f"{width}x{height}"] = dimensions.get(f"{width}x{height}", 0) + 1
            bounds_ok = True
            if (corners[:, 0] < 0).any() or (corners[:, 0] >= width).any():
                issues.append("x coordinates outside original frame")
                bounds_ok = False
            if (corners[:, 1] < 0).any() or (corners[:, 1] >= height).any():
                issues.append("y coordinates outside original frame")
                bounds_ok = False
            if bounds_ok:
                coordinate_bounds_valid += 1
            valid, reasons = validate_quad_geometry(normalize_corners(corners), image.shape)
            if not valid:
                issues.extend(f"geometry: {reason}" for reason in reasons)
            digest = hashlib.sha1(image.tobytes()).hexdigest()
            duplicates.setdefault(digest, []).append(int(row["id"]))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            tiny_digest = hashlib.sha1(
                cv2.resize(gray, (8, 6), interpolation=cv2.INTER_AREA).tobytes()
            ).hexdigest()
            near_duplicates.setdefault(tiny_digest, []).append(int(row["id"]))
        results.append({
            "id": int(row["id"]),
            "judgment": row["judgment"],
            "session_id": row["session_id"],
            "frame_path": row["frame_path"],
            "issues": issues,
        })
    duplicate_groups = [ids for ids in duplicates.values() if len(ids) > 1]
    near_duplicate_groups = [ids for ids in near_duplicates.values() if len(ids) > 1]
    return {
        "total": len(rows),
        "correct": sum(row["judgment"] == "correct" for row in rows),
        "incorrect": sum(row["judgment"] == "incorrect" for row in rows),
        "unsure": sum(row["judgment"] == "unsure" for row in rows),
        "decoded_images": sum(not item["issues"] or "image missing or undecodable" not in item["issues"] for item in results),
        "frame_dimensions": dimensions,
        "coordinate_bounds_valid": coordinate_bounds_valid,
        "corner_order_normalized_for_metrics": True,
        "iou_method": "same-frame rasterized polygon intersection over union",
        "questionable": [item for item in results if item["issues"]],
        "duplicate_groups": duplicate_groups,
        "exact_duplicate_groups": duplicate_groups,
        "near_duplicate_groups": near_duplicate_groups,
        "duplicate_sample_count": sum(len(group) for group in duplicate_groups),
        "near_duplicate_sample_count": sum(len(group) for group in near_duplicate_groups),
        "semantic_outer_boundary_review": "Manual labels are preserved; pixel inspection is required to confirm complete physical-card semantics.",
    }


def evaluate_candidate_generation(
    rows: list[Any], detect_fn, profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate outer-boundary generation and ranking as separate outcomes."""
    correct_rows = [row for row in rows if row["judgment"] == "correct"]
    cases = []
    iou_values = []
    errors = []
    internal_hits = 0
    for row in correct_rows:
        started = time.perf_counter()
        image = cv2.imread(str(row["frame_path"])) if row["frame_path"] else None
        if image is None:
            cases.append({"id": int(row["id"]), "failure": "missing_image"})
            continue
        target = normalize_corners(json.loads(row["corners_json"]))
        generated = detect_fn(image, rank_candidates=False, max_candidates=1000)
        ranked = detect_fn(image, rank_candidates=True, max_candidates=1000)
        processing_time_ms = (time.perf_counter() - started) * 1000
        generated_scores = [_candidate_iou_and_error(image, target, item) for item in generated]
        ranked_scores = [_candidate_iou_and_error(image, target, item) for item in ranked]
        outer_generated = [
            (index, score) for index, score in enumerate(generated_scores)
            if not _is_internal_candidate(target, generated[index])
        ]
        best_outer_index, (best_iou, best_error) = max(
            outer_generated, key=lambda item: item[1][0], default=(-1, (0.0, 0.0))
        )
        best_any_index, (best_any_iou, _) = max(
            enumerate(generated_scores), key=lambda item: item[1][0], default=(-1, (0.0, 0.0))
        )
        top_iou = ranked_scores[0][0] if ranked_scores else 0.0
        if best_iou:
            iou_values.append(best_iou)
            errors.append(best_error)
        internal_hits += sum(
            bool(item["metrics"].get("likely_internal_region")) for item in generated
        )
        failure = None
        if best_iou < 0.5:
            failure = "candidate_generation_failure"
        elif top_iou < 0.5:
            failure = "candidate_ranking_failure"
        elif best_iou < 0.75:
            failure = "localization_failure"
        internal_failure = (
            best_any_iou >= 0.5
            and best_outer_index < 0
        )
        cases.append({
            "id": int(row["id"]),
            "session_id": row["session_id"],
            "frame_path": row["frame_path"],
            "candidate_count": len(generated),
            "processing_time_ms": round(processing_time_ms, 3),
            "best_iou": best_iou,
            "best_corner_error": best_error,
            "top_rank_iou": top_iou,
            "best_any_iou": best_any_iou,
            "best_candidate_internal": internal_failure,
            "ground_truth_points": target.tolist(),
            "best_candidate_points": normalize_corners(
                generated[best_outer_index]["points"]
            ).tolist() if best_outer_index >= 0 else None,
            "best_any_candidate_points": normalize_corners(
                generated[best_any_index]["points"]
            ).tolist() if best_any_index >= 0 else None,
            "top_candidate_points": normalize_corners(ranked[0]["points"]).tolist() if ranked else None,
            "top_candidate_metrics": ranked[0]["metrics"] if ranked else {},
            "internal_candidates": [
                {
                    "points": normalize_corners(item["points"]).tolist(),
                    "metrics": item["metrics"],
                }
                for item in generated
                if item["metrics"].get("likely_internal_region")
            ],
            "failure": failure,
        })
    total = len(correct_rows)
    return {
        "total_correct": total,
        "evaluated_once": len(cases) == total,
        "iou_0_5_recall": sum(item["best_iou"] >= 0.5 for item in cases) / total if total else None,
        "iou_0_75_recall": sum(item["best_iou"] >= 0.75 for item in cases) / total if total else None,
        "mean_corner_error": mean(errors) if errors else None,
        "mean_candidate_count": mean([item["candidate_count"] for item in cases]) if cases else None,
        "mean_processing_time_ms": mean(
            [item["processing_time_ms"] for item in cases]
        ) if cases else None,
        "internal_candidate_frequency": internal_hits / total if total else None,
        "generation_failures": sum(item["failure"] == "candidate_generation_failure" for item in cases),
        "ranking_failures": sum(item["failure"] == "candidate_ranking_failure" for item in cases),
        "localization_failures": sum(item["failure"] == "localization_failure" for item in cases),
        "internal_region_failures": sum(item["best_candidate_internal"] for item in cases),
        "session_breakdown": _session_breakdown(cases),
        "cases": cases,
    }


def _session_breakdown(cases: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    breakdown: dict[str, dict[str, Any]] = {}
    for case in cases:
        session = case["session_id"]
        item = breakdown.setdefault(session, {"total": 0, "generation_failures": 0, "ranking_failures": 0, "localization_failures": 0})
        item["total"] += 1
        failure = case["failure"]
        if failure:
            item[failure.replace("candidate_", "") + "s"] += 1
    return breakdown


def compare_experimental_models(rows: list[Any]) -> dict[str, Any]:
    """Compare the available geometry baseline and report unavailable models explicitly."""
    eligible = [row for row in rows if row["judgment"] in {"correct", "incorrect"}]
    sessions = sorted({row["session_id"] for row in eligible})
    held_out = sessions[-1] if len(sessions) > 1 else None
    train = [row for row in eligible if row["session_id"] != held_out]
    test = [row for row in eligible if row["session_id"] == held_out]
    profile = build_outer_profile(train)
    predictions = []
    for row in test:
        metrics = json.loads(row["metrics_json"])
        predicted = "correct" if score_outer_candidate(metrics, profile) >= 0.5 else "incorrect"
        predictions.append(predicted == row["judgment"])
    result: dict[str, Any] = {
        "split": "session-held-out",
        "held_out_session": held_out,
        "train_samples": len(train),
        "test_samples": len(test),
        "geometry_baseline": {
            "accuracy": sum(predictions) / len(predictions) if predictions else None,
            "evaluated": bool(predictions),
        },
        "logistic_regression": {"available": False, "reason": "scikit-learn is not installed; no model was trained."},
        "random_forest": {"available": False, "reason": "scikit-learn is not installed; no model was trained."},
    }
    return result


def compare_detector_variants(
    rows: list[Any], baseline_fn, experimental_fn,
) -> dict[str, Any]:
    """Compare baseline generation with the explainable perimeter experiment."""
    baseline_positive = evaluate_candidate_generation(rows, baseline_fn)
    experimental_positive = evaluate_candidate_generation(rows, experimental_fn)
    incorrect_rows = [row for row in rows if row["judgment"] == "incorrect"]

    def evaluate_incorrect(detector_fn, experimental: bool) -> dict[str, Any]:
        generated = 0
        accepted = 0
        internal_accepted = 0
        counts = []
        scores = []
        processing_times = []
        cases = []
        for row in incorrect_rows:
            started = time.perf_counter()
            image = cv2.imread(str(row["frame_path"])) if row["frame_path"] else None
            if image is None:
                counts.append(0)
                continue
            candidates = detector_fn(image, rank_candidates=True, max_candidates=1000)
            processing_time_ms = (time.perf_counter() - started) * 1000
            counts.append(len(candidates))
            generated += bool(candidates)
            if not candidates:
                processing_times.append(processing_time_ms)
                cases.append({
                    "id": int(row["id"]),
                    "candidate_count": 0,
                    "accepted": False,
                    "top_score": 0.0,
                    "likely_internal_region": False,
                    "processing_time_ms": round(processing_time_ms, 3),
                })
                continue
            top = candidates[0]
            score = (
                top["metrics"].get("experimental_outer_score", 0.0)
                if experimental
                else top["metrics"].get("confidence", 0.0)
            )
            scores.append(score)
            if experimental:
                is_accepted = (
                    score >= 0.35
                    and not top["metrics"].get("likely_internal_region", False)
                )
            else:
                is_accepted = True
            accepted += is_accepted
            internal_accepted += bool(
                is_accepted and top["metrics"].get("likely_internal_region", False)
            )
            processing_times.append(processing_time_ms)
            cases.append({
                "id": int(row["id"]),
                "candidate_count": len(candidates),
                "accepted": bool(is_accepted),
                "top_score": round(float(score), 4),
                "likely_internal_region": bool(
                    top["metrics"].get("likely_internal_region", False)
                ),
                "processing_time_ms": round(processing_time_ms, 3),
            })
        total = len(incorrect_rows)
        return {
            "total": total,
            "generated": generated,
            "accepted": accepted,
            "rejected": total - accepted,
            "false_acceptance_rate": accepted / total if total else None,
            "internal_region_accepted": internal_accepted,
            "mean_candidate_count": mean(counts) if counts else None,
            "mean_top_score": mean(scores) if scores else None,
            "mean_processing_time_ms": mean(processing_times) if processing_times else None,
            "cases": cases,
            "acceptance_rule": (
                "top candidate experimental_outer_score >= 0.35 and not likely_internal_region"
                if experimental else
                "current baseline has no explicit final acceptance gate; any top candidate is queued"
            ),
        }

    result = {
        "baseline": {
            "positive": baseline_positive,
            "incorrect": evaluate_incorrect(baseline_fn, False),
        },
        "experimental": {
            "positive": experimental_positive,
            "incorrect": evaluate_incorrect(experimental_fn, True),
        },
    }
    baseline_cases = {
        item["id"]: item for item in result["baseline"]["incorrect"]["cases"]
    }
    experimental_cases = {
        item["id"]: item for item in result["experimental"]["incorrect"]["cases"]
    }
    result["incorrect_changes"] = {
        "new_false_acceptances": [
            record_id for record_id, item in experimental_cases.items()
            if item["accepted"] and not baseline_cases[record_id]["accepted"]
        ],
        "new_correct_rejections": [
            record_id for record_id, item in experimental_cases.items()
            if not item["accepted"] and baseline_cases[record_id]["accepted"]
        ],
    }
    known_failure_ids = {207, 191, 178, 156}
    baseline_positive_cases = {
        item["id"]: item for item in baseline_positive["cases"]
    }
    experimental_positive_cases = {
        item["id"]: item for item in experimental_positive["cases"]
    }
    result["known_failure_outcomes"] = {
        str(record_id): {
            "baseline": {
                "best_iou": baseline_positive_cases[record_id]["best_iou"],
                "top_rank_iou": baseline_positive_cases[record_id]["top_rank_iou"],
                "failure": baseline_positive_cases[record_id]["failure"],
            },
            "experimental": {
                "best_iou": experimental_positive_cases[record_id]["best_iou"],
                "top_rank_iou": experimental_positive_cases[record_id]["top_rank_iou"],
                "failure": experimental_positive_cases[record_id]["failure"],
                "top_score": experimental_positive_cases[record_id][
                    "top_candidate_metrics"
                ].get("experimental_outer_score", 0.0),
            },
        }
        for record_id in sorted(known_failure_ids)
        if record_id in baseline_positive_cases and record_id in experimental_positive_cases
    }
    return result
