"""Read-only audit and detector evaluation for captured boundary references."""

from __future__ import annotations

import hashlib
import json
import time
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any, Callable

import cv2
import numpy as np

from .analysis import audit_annotations, normalize_corners
from .boundary_references import CONDITIONS, list_references, validate_annotation
from .engines import detect_boundary_candidates
from .paths import REPORTS


REFERENCE_REPORT = REPORTS / "boundary_reference_detector_audit.json"
OVERLAY_ROOT = REPORTS / "boundary_reference_audit_overlays"


def _polygon_iou(image_shape: tuple[int, ...], first: Any, second: Any) -> float:
    first_mask = np.zeros(image_shape[:2], dtype=np.uint8)
    second_mask = np.zeros(image_shape[:2], dtype=np.uint8)
    cv2.fillPoly(first_mask, [np.int32(normalize_corners(first))], 1)
    cv2.fillPoly(second_mask, [np.int32(normalize_corners(second))], 1)
    intersection = np.logical_and(first_mask, second_mask).sum()
    union = np.logical_or(first_mask, second_mask).sum()
    return float(intersection / union) if union else 0.0


def _corner_error(image_shape: tuple[int, ...], first: Any, second: Any) -> float:
    image_diagonal = max(float(np.hypot(image_shape[1], image_shape[0])), 1.0)
    return float(np.mean(
        np.linalg.norm(
            normalize_corners(first) - normalize_corners(second), axis=1
        )
    ) / image_diagonal)


def _contained(inner: Any, outer: Any) -> bool:
    contour = normalize_corners(outer).reshape(-1, 1, 2)
    return all(
        cv2.pointPolygonTest(contour, (float(point[0]), float(point[1])), False) >= -2
        for point in normalize_corners(inner)
    )


def _digest(path: Path, reduced: bool = False) -> str | None:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None
    if reduced:
        image = cv2.resize(image, (8, 6), interpolation=cv2.INTER_AREA)
    return hashlib.sha1(image.tobytes()).hexdigest()


def _duplicate_groups(paths: list[Path], reduced: bool = False) -> list[list[str]]:
    grouped: dict[str, list[str]] = {}
    for path in paths:
        digest = _digest(path, reduced)
        if digest:
            grouped.setdefault(digest, []).append(str(path))
    return [group for group in grouped.values() if len(group) > 1]


def audit_reference_collection(records: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    records = list_references() if records is None else records
    results = []
    image_paths = []
    for record in records:
        issues: list[str] = []
        warnings: list[str] = []
        image_path = Path(str(record.get("image_path", "")))
        image = cv2.imread(str(image_path)) if image_path.exists() else None
        if image is None:
            issues.append("original image missing or unreadable")
        else:
            image_paths.append(image_path)
        try:
            corners = np.float32(record["corners"]).reshape(4, 2)
        except (KeyError, TypeError, ValueError):
            corners = None
            issues.append("exactly four corners are not present")
        if corners is not None and image is not None:
            if not np.isfinite(corners).all():
                issues.append("corner coordinates are non-finite")
            height, width = image.shape[:2]
            if (
                (corners[:, 0] < 0).any() or (corners[:, 0] >= width).any()
                or (corners[:, 1] < 0).any() or (corners[:, 1] >= height).any()
            ):
                issues.append("corner coordinates are outside original image bounds")
            valid, geometry_messages = validate_annotation(corners, image.shape)
            if not valid:
                issues.extend(geometry_messages)
            else:
                warnings.extend(geometry_messages)
            if record.get("image_width") != width or record.get("image_height") != height:
                issues.append("metadata dimensions do not match original image")
        if record.get("ground_truth_source") != "human_outer_boundary_annotation":
            warnings.append("ground-truth source metadata is missing or unexpected")
        if record.get("capture_condition") not in dict(CONDITIONS):
            issues.append("unknown capture condition")
        if record.get("manually_verified") is not True:
            warnings.append("annotation requires human verification")
        # Whether this is the physical perimeter cannot be proven from pixels alone.
        warnings.append("physical outer-boundary semantics require visual human review")
        results.append({
            "sample_id": record.get("sample_id"),
            "capture_condition": record.get("capture_condition"),
            "session_id": record.get("session_id"),
            "image_path": str(image_path),
            "visibility_status": record.get("visibility_status"),
            "manually_verified": record.get("manually_verified") is True,
            "valid": not issues,
            "issues": issues,
            "warnings": warnings,
        })
    exact = _duplicate_groups(image_paths)
    near = _duplicate_groups(image_paths, reduced=True)
    return {
        "total_samples": len(records),
        "conditions": {
            condition: {
                "label": label,
                "samples": sum(item.get("capture_condition") == condition for item in records),
            }
            for condition, label in CONDITIONS
        },
        "fully_visible": sum(item.get("visibility_status") == "fully_visible" for item in records),
        "partially_obstructed": sum(
            item.get("visibility_status") == "partially_obstructed" for item in records
        ),
        "manually_verified": sum(item.get("manually_verified") is True for item in records),
        "requires_review": sum(item.get("manually_verified") is not True for item in records),
        "unreadable_or_invalid": sum(not item["valid"] for item in results),
        "exact_duplicate_groups": exact,
        "near_duplicate_groups": near,
        "semantic_outer_boundary_review_required": len(records),
        "samples": results,
    }


def _evaluate_positive(
    records: list[dict[str, Any]],
    detector: Callable[..., list[dict[str, Any]]],
) -> dict[str, Any]:
    cases = []
    for record in records:
        image = cv2.imread(record["image_path"]) if Path(record["image_path"]).exists() else None
        if image is None:
            cases.append({
                "sample_id": record["sample_id"],
                "status": "excluded_unreadable",
                "capture_condition": record.get("capture_condition"),
            })
            continue
        target = normalize_corners(record["corners"])
        started = time.perf_counter()
        candidates = detector(image, rank_candidates=True, max_candidates=1000)
        elapsed = (time.perf_counter() - started) * 1000
        scored = [
            {
                "iou": _polygon_iou(image.shape, target, item["points"]),
                "corner_error": _corner_error(image.shape, target, item["points"]),
                "internal": _contained(item["points"], target)
                    and _polygon_iou(image.shape, target, item["points"]) < 0.85,
                "points": normalize_corners(item["points"]).tolist(),
                "metrics": item["metrics"],
            }
            for item in candidates
        ]
        outer = [item for item in scored if not item["internal"]]
        best = max(outer, key=lambda item: item["iou"], default=None)
        top = scored[0] if scored else None
        cases.append({
            "sample_id": record["sample_id"],
            "capture_condition": record.get("capture_condition"),
            "visibility_status": record.get("visibility_status"),
            "status": "evaluated",
            "candidate_count": len(scored),
            "processing_time_ms": round(elapsed, 3),
            "best_iou": best["iou"] if best else 0.0,
            "best_corner_error": best["corner_error"] if best else None,
            "top_iou": top["iou"] if top else 0.0,
            "top_is_internal": bool(top and top["internal"]),
            "internal_candidate_count": sum(item["internal"] for item in scored),
            "multiple_competing_candidates": len(scored) > 1,
            "ground_truth_points": target.tolist(),
            "best_candidate_points": best["points"] if best else None,
            "top_candidate_points": top["points"] if top else None,
            "top_candidate_metrics": top["metrics"] if top else {},
            "failure": (
                "candidate_generation_failure" if not best or best["iou"] < 0.50
                else "ranking_failure" if not top or top["iou"] < 0.50
                else "localization_failure" if best["iou"] < 0.75
                else None
            ),
        })
    return _summarize_positive(cases)


def _summarize_positive(cases: list[dict[str, Any]]) -> dict[str, Any]:
    evaluated = [case for case in cases if case["status"] == "evaluated"]
    def values(key: str) -> list[float]:
        return [float(case[key]) for case in evaluated if case.get(key) is not None]
    return {
        "total": len(cases),
        "evaluated": len(evaluated),
        "excluded": len(cases) - len(evaluated),
        "iou_0_50_recall": sum(case["best_iou"] >= 0.50 for case in evaluated) / len(evaluated)
            if evaluated else None,
        "iou_0_75_recall": sum(case["best_iou"] >= 0.75 for case in evaluated) / len(evaluated)
            if evaluated else None,
        "mean_iou": mean(values("best_iou")) if evaluated else None,
        "mean_corner_error": mean(values("best_corner_error")) if values("best_corner_error") else None,
        "missed_detections": sum(case["failure"] == "candidate_generation_failure" for case in evaluated),
        "internal_border_detections": sum(case["internal_candidate_count"] > 0 for case in evaluated),
        "ranking_failures": sum(case["failure"] == "ranking_failure" for case in evaluated),
        "localization_failures": sum(case["failure"] == "localization_failure" for case in evaluated),
        "multiple_competing_candidates": sum(case["multiple_competing_candidates"] for case in evaluated),
        "mean_candidate_count": mean(values("candidate_count")) if evaluated else None,
        "mean_processing_time_ms": mean(values("processing_time_ms")) if evaluated else None,
        "cases": cases,
    }


def _evaluate_negative(
    rows: list[Any],
    detector: Callable[..., list[dict[str, Any]]],
) -> dict[str, Any]:
    cases = []
    for row in rows:
        path = Path(str(row["frame_path"])) if row["frame_path"] else Path()
        image = cv2.imread(str(path)) if path.exists() else None
        if image is None:
            cases.append({"id": int(row["id"]), "status": "excluded_unreadable"})
            continue
        started = time.perf_counter()
        candidates = detector(image, rank_candidates=True, max_candidates=1000)
        elapsed = (time.perf_counter() - started) * 1000
        top = candidates[0] if candidates else None
        cases.append({
            "id": int(row["id"]),
            "status": "evaluated",
            "candidate_count": len(candidates),
            "generated": bool(candidates),
            # Baseline has no final acceptance gate; a top candidate is queued.
            "accepted": bool(top),
            "top_is_internal": bool(top and top["metrics"].get("likely_internal_region")),
            "top_metrics": top["metrics"] if top else {},
            "processing_time_ms": round(elapsed, 3),
        })
    evaluated = [case for case in cases if case["status"] == "evaluated"]
    accepted = sum(case["accepted"] for case in evaluated)
    methods = Counter(
        case["top_metrics"].get("detection_method", "unknown")
        for case in evaluated if case["accepted"]
    )
    categories = Counter(
        "internal-region" if case["top_is_internal"] else "other-rectangle"
        for case in evaluated if case["accepted"]
    )
    return {
        "total": len(cases),
        "evaluated": len(evaluated),
        "excluded": len(cases) - len(evaluated),
        "candidate_generated": sum(case["generated"] for case in evaluated),
        "accepted": accepted,
        "rejected": sum(not case["accepted"] for case in evaluated),
        "false_acceptance_rate": accepted / len(evaluated) if evaluated else None,
        "internal_top_candidates": sum(case["top_is_internal"] for case in evaluated),
        "accepted_candidate_methods": dict(methods),
        "accepted_candidate_categories": dict(categories),
        "mean_candidate_count": mean([case["candidate_count"] for case in evaluated])
            if evaluated else None,
        "mean_processing_time_ms": mean([case["processing_time_ms"] for case in evaluated])
            if evaluated else None,
        "cases": cases,
        "acceptance_definition": "baseline detector has no explicit final gate; any top candidate is queued",
        "negative_label_caveat": (
            "INCORRECT candidate annotations are retained as negatives for reporting, "
            "but their semantic suitability as arbitrary-rectangle negatives requires review."
        ),
    }


def _condition_breakdown(cases: list[dict[str, Any]]) -> dict[str, Any]:
    result = {}
    for condition, _ in CONDITIONS:
        subset = [case for case in cases if case.get("capture_condition") == condition]
        summary = _summarize_positive(subset)
        result[condition] = summary
    return result


def _write_overlay(case: dict[str, Any], output: Path, image_path: str) -> None:
    image = cv2.imread(image_path)
    if image is None:
        return
    if case.get("ground_truth_points"):
        cv2.polylines(image, [np.int32(case["ground_truth_points"])], True, (70, 220, 70), 3)
    if case.get("best_candidate_points"):
        cv2.polylines(image, [np.int32(case["best_candidate_points"])], True, (235, 80, 60), 3)
    if case.get("top_candidate_points"):
        cv2.polylines(image, [np.int32(case["top_candidate_points"])], True, (60, 170, 235), 2)
    label = (
        f"{case.get('sample_id', case.get('id'))} "
        f"IoU={case.get('best_iou', 0.0):.3f} {case.get('failure') or 'matched'}"
    )
    cv2.putText(image, label, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    cv2.imwrite(str(output), image)


def evaluate_boundary_references(
    negative_rows: list[Any],
    detector: Callable[..., list[dict[str, Any]]] = detect_boundary_candidates,
) -> dict[str, Any]:
    references = list_references()
    inventory = audit_reference_collection(references)
    positive = _evaluate_positive(references, detector)
    for case, record in zip(positive["cases"], references):
        if case["status"] == "evaluated":
            case["image_path"] = record["image_path"]
    incorrect_rows = [
        row for row in negative_rows if row["judgment"] == "incorrect"
    ]
    negative = _evaluate_negative(incorrect_rows, detector)
    negative_paths = [
        Path(str(row["frame_path"])) for row in incorrect_rows if row["frame_path"]
    ]
    session_counts = Counter(record.get("session_id") for record in references)
    overlays = OVERLAY_ROOT / "references"
    overlays.mkdir(parents=True, exist_ok=True)
    for case in positive["cases"]:
        if case["status"] == "evaluated":
            _write_overlay(
                case, overlays / f"{case['sample_id']}.png", case["image_path"]
            )
    return {
        "inventory": inventory,
        "annotation_validation": {
            "valid_annotations": inventory["total_samples"] - inventory["unreadable_or_invalid"],
            "suspicious_annotations": inventory["unreadable_or_invalid"],
            "note": "Physical outer-boundary semantics remain a human visual-review task.",
        },
        "positive": positive,
        "by_condition": _condition_breakdown(positive["cases"]),
        "by_visibility": {
            visibility: _summarize_positive([
                case for case in positive["cases"]
                if case.get("visibility_status") == visibility
            ])
            for visibility in ("fully_visible", "partially_obstructed")
        },
        "negative": negative,
        "negative_dataset_audit": audit_annotations(incorrect_rows),
        "negative_duplicate_analysis": {
            "exact_duplicate_groups": _duplicate_groups(negative_paths),
            "near_duplicate_groups": _duplicate_groups(negative_paths, reduced=True),
            "source_rows": len(incorrect_rows),
        },
        "session_analysis": {
            "session_count": len(session_counts),
            "samples_per_session": dict(session_counts),
            "held_out_evaluation_available": len(session_counts) >= 2,
            "note": (
                "All references share one capture session; no independent "
                "session-held-out generalization result is available."
                if len(session_counts) < 2 else
                "Sessions are available for grouped evaluation."
            ),
        },
        "limitations": [
            "Only captured references present at evaluation time are measured.",
            "Eight references across four conditions are too few for generalization claims.",
            "All captured references currently have fully_visible metadata.",
            "The baseline negative acceptance definition is queued-top-candidate behavior.",
            "No training or model fitting was performed.",
        ],
    }


def export_boundary_reference_report(report: dict[str, Any]) -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    REFERENCE_REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    return REFERENCE_REPORT

