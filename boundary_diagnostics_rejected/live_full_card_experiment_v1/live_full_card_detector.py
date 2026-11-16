"""Isolated full-card detector, benchmark, and live tracker.

This experiment does not import or modify the production detector. A
candidate is only reported as verified when its four sides have independent
edge and contrast support and its geometry is consistent with the physical
card. Internal rectangles remain candidates, but are never silently reported
as verified without passing those checks.
"""

import argparse
import csv
import json
import math
import time
from pathlib import Path

import cv2
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ANNOTATIONS = (
    ROOT
    / "boundary_diagnostics_rejected"
    / "visual_localization_experiment_v1"
    / "manual_review"
    / "manual_boundary_annotations.json"
)
OUTPUT = HERE / "validation_results"
OVERLAYS = OUTPUT / "comparison_overlays"
CSV_PATH = OUTPUT / "full_card_validation.csv"
SUMMARY_PATH = OUTPUT / "full_card_summary.json"
REPORT_PATH = HERE / "FULL_CARD_EXPERIMENT_REPORT.md"

CARD_ASPECT = 120.0 / 168.0
MIN_AREA_RATIO = 0.035
MIN_EDGE_CONTINUITY = 0.12
MIN_EDGE_CONTRAST = 8.0
MIN_OUTER_CONTRAST = 5.0
MIN_OPPOSITE_SIDE_RATIO = 0.55
MIN_CORNER_ANGLE = 45.0
MAX_CORNER_ANGLE = 135.0
LOCK_FRAMES = 5
MIN_CANDIDATE_AREA_RATIO = 0.02


def order_quad(points):
    """Return a cyclic order based on angle around the centroid.

    Unlike sum/difference ordering, this remains cyclic for rotated
    quadrilaterals. The starting corner is intentionally not semantic;
    benchmark matching handles cyclic and reversed permutations.
    """
    points = np.asarray(points, dtype=np.float32).reshape(4, 2)
    center = points.mean(axis=0)
    angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])
    ordered = points[np.argsort(angles)]
    if cv2.contourArea(ordered, oriented=True) < 0:
        ordered = ordered[::-1]
    return ordered


def polygon_area(points):
    return abs(float(cv2.contourArea(order_quad(points))))


def corner_angles(points):
    points = order_quad(points)
    result = []
    for index in range(4):
        before = points[(index - 1) % 4] - points[index]
        after = points[(index + 1) % 4] - points[index]
        denominator = max(float(np.linalg.norm(before) * np.linalg.norm(after)), 1.0)
        cosine = float(np.dot(before, after)) / denominator
        result.append(math.degrees(math.acos(np.clip(cosine, -1.0, 1.0))))
    return result


def _sample_side(gray, start, end, center, edges):
    height, width = gray.shape[:2]
    length = max(int(np.linalg.norm(end - start)), 2)
    values = []
    continuity = 0
    tangent = (end - start) / max(float(np.linalg.norm(end - start)), 1.0)
    normal = np.array([-tangent[1], tangent[0]], dtype=np.float32)
    midpoint = (start + end) / 2.0
    if np.dot(normal, center - midpoint) < 0:
        normal = -normal
    for point in np.linspace(start, end, length):
        x, y = np.rint(point).astype(int)
        x0, x1 = max(0, x - 3), min(width, x + 4)
        y0, y1 = max(0, y - 3), min(height, y + 4)
        continuity += int(edges[y0:y1, x0:x1].any())
        inside = np.rint(point + normal * 6).astype(int)
        outside = np.rint(point - normal * 6).astype(int)
        inside_far = np.rint(point + normal * 12).astype(int)
        outside_far = np.rint(point - normal * 12).astype(int)
        inside = np.clip(inside, [0, 0], [width - 1, height - 1])
        outside = np.clip(outside, [0, 0], [width - 1, height - 1])
        inside_far = np.clip(inside_far, [0, 0], [width - 1, height - 1])
        outside_far = np.clip(outside_far, [0, 0], [width - 1, height - 1])
        values.append(
            (
                abs(float(gray[inside[1], inside[0]]) - float(gray[outside[1], outside[0]])),
                abs(
                    float(gray[inside_far[1], inside_far[0]])
                    - float(gray[outside_far[1], outside_far[0]])
                ),
            )
        )
    return continuity / float(length), values


def candidate_metrics(gray, points, edges=None):
    points = order_quad(points)
    height, width = gray.shape[:2]
    sides = [
        float(np.linalg.norm(points[(index + 1) % 4] - points[index]))
        for index in range(4)
    ]
    horizontal = (sides[0] + sides[2]) / 2.0
    vertical = (sides[1] + sides[3]) / 2.0
    aspect = min(horizontal, vertical) / max(horizontal, vertical, 1.0)
    opposite = min(
        sides[0] / max(sides[2], 1.0),
        sides[2] / max(sides[0], 1.0),
        sides[1] / max(sides[3], 1.0),
        sides[3] / max(sides[1], 1.0),
    )
    angles = corner_angles(points)
    if edges is None:
        edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
    continuity = []
    near_contrast = []
    far_contrast = []
    for start, end in zip(points, np.roll(points, -1, axis=0)):
        support, values = _sample_side(gray, start, end, points.mean(axis=0), edges)
        continuity.append(support)
        near_contrast.extend(value[0] for value in values)
        far_contrast.extend(value[1] for value in values)
    clipped = bool(
        np.any(points[:, 0] <= 2)
        or np.any(points[:, 1] <= 2)
        or np.any(points[:, 0] >= width - 3)
        or np.any(points[:, 1] >= height - 3)
    )
    area_ratio = polygon_area(points) / float(width * height)
    aspect_score = max(0.0, 1.0 - abs(aspect - CARD_ASPECT) / CARD_ASPECT)
    angle_score = max(
        0.0,
        1.0 - max(abs(min(angles) - 90), abs(max(angles) - 90)) / 90,
    )
    edge_score = min(1.0, 0.7 * min(continuity) + 0.3 * np.mean(continuity))
    contrast_score = min(1.0, np.mean(near_contrast) / 45.0)
    outer_score = min(1.0, np.mean(far_contrast) / 35.0)
    area_score = min(1.0, math.sqrt(max(area_ratio, 0.0) / 0.15))
    geometry_score = (
        0.35 * aspect_score
        + 0.25 * opposite
        + 0.25 * angle_score
        + 0.15 * (1.0 - clipped)
    )
    score = (
        0.30 * geometry_score
        + 0.25 * edge_score
        + 0.20 * contrast_score
        + 0.15 * outer_score
        + 0.10 * area_score
    )
    valid = (
        area_ratio >= MIN_AREA_RATIO
        and aspect_score >= 0.65
        and opposite >= MIN_OPPOSITE_SIDE_RATIO
        and min(angles) >= MIN_CORNER_ANGLE
        and max(angles) <= MAX_CORNER_ANGLE
        and min(continuity) >= MIN_EDGE_CONTINUITY
        and min(near_contrast) >= MIN_EDGE_CONTRAST
        and min(far_contrast) >= MIN_OUTER_CONTRAST
        and not clipped
    )
    return {
        "area_ratio": float(area_ratio),
        "aspect_ratio": float(aspect),
        "aspect_score": float(aspect_score),
        "opposite_side_ratio": float(opposite),
        "corner_angle_min": float(min(angles)),
        "corner_angle_max": float(max(angles)),
        "edge_continuity_min": float(min(continuity)),
        "edge_continuity_mean": float(np.mean(continuity)),
        "edge_contrast_min": float(min(near_contrast)),
        "edge_contrast_mean": float(np.mean(near_contrast)),
        "outer_contrast_min": float(min(far_contrast)),
        "outer_contrast_mean": float(np.mean(far_contrast)),
        "geometry_score": float(geometry_score),
        "score": float(score),
        "clipped": clipped,
        "valid": bool(valid),
    }


def _masks(gray, fast=False):
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    masks = []
    for low, high in ((30, 100), (50, 150), (80, 200)):
        masks.append(cv2.Canny(blurred, low, high))
    if fast:
        return [
            cv2.morphologyEx(
                mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=2
            )
            for mask in masks
        ]
    masks.append(
        cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            5,
        )
    )
    for threshold in (100, 140, 180):
        _, binary = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
        masks.append(binary)
    masks.append(
        cv2.morphologyEx(blurred, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8))
    )
    return [
        cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=2)
        for mask in masks
    ]


def _same_candidate(first, second):
    first = order_quad(first)
    second = order_quad(second)
    scale = max(
        np.linalg.norm(first[1] - first[0]),
        np.linalg.norm(first[3] - first[0]),
        1.0,
    )
    return float(np.mean(np.linalg.norm(first - second, axis=1))) / scale < 0.06


def find_candidates(image, fast=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_area = gray.shape[0] * gray.shape[1]
    max_dimension = 480.0 if fast else 900.0
    scale = min(1.0, max_dimension / max(gray.shape))
    source = (
        cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        if scale < 1.0
        else gray
    )
    source_edges = cv2.Canny(cv2.GaussianBlur(source, (5, 5), 0), 50, 150)
    candidates = []
    for mask_index, mask in enumerate(_masks(source, fast=fast)):
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour) / max(scale * scale, 1e-9)
            if (
                area < MIN_CANDIDATE_AREA_RATIO * image_area
                or area > 0.92 * image_area
            ):
                continue
            perimeter = cv2.arcLength(contour, True)
            for epsilon in (0.01, 0.02, 0.04):
                approx = cv2.approxPolyDP(contour, epsilon * perimeter, True)
                if len(approx) != 4 or not cv2.isContourConvex(approx):
                    continue
                source_points = order_quad(approx.reshape(4, 2).astype(np.float32))
                points = source_points / max(scale, 1e-9)
                candidates.append({
                    "points": points,
                    "metrics": candidate_metrics(source, source_points, source_edges),
                    "mask_index": mask_index,
                })
    unique = []
    for candidate in sorted(
        candidates, key=lambda item: item["metrics"]["score"], reverse=True
    ):
        if not any(_same_candidate(candidate["points"], item["points"]) for item in unique):
            unique.append(candidate)
    for candidate in unique:
        candidate["nested_penalty"] = 0.0
        candidate_area = polygon_area(candidate["points"])
        for outer in unique:
            outer_area = polygon_area(outer["points"])
            if outer_area <= candidate_area * 1.25:
                continue
            inside = all(
                cv2.pointPolygonTest(
                    order_quad(outer["points"]).astype(np.float32),
                    tuple(point),
                    False,
                ) >= 0
                for point in candidate["points"]
            )
            if inside:
                candidate["nested_penalty"] = max(candidate["nested_penalty"], 0.18)
        candidate["selection_score"] = candidate["metrics"]["score"] - candidate["nested_penalty"]
    return sorted(unique, key=lambda item: item["selection_score"], reverse=True)[:12]


def detect(image, reference_points=None, fast=False):
    candidates = find_candidates(image, fast=fast)
    verified = [candidate for candidate in candidates if candidate["metrics"]["valid"]]
    if not verified:
        return {
            "status": "uncertain",
            "reason": "no candidate has complete four-edge support",
            "candidates": candidates,
            "selected": None,
        }
    if reference_points is not None:
        height, width = image.shape[:2]
        diagonal = math.hypot(width, height)
        verified.sort(
            key=lambda candidate: (
                candidate["selection_score"]
                + 0.12
                * max(
                    0.0,
                    1.0
                    - float(
                        np.mean(
                            np.linalg.norm(
                                order_quad(candidate["points"])
                                - order_quad(reference_points),
                                axis=1,
                            )
                        )
                        / max(diagonal * 0.15, 1.0)
                    ),
                )
            ),
            reverse=True,
        )
    return {
        "status": "detected",
        "reason": "selected verified full-card candidate",
        "candidates": candidates,
        "selected": verified[0],
    }


def permutations(points):
    points = list(points)
    for reverse in (False, True):
        ordered = points[::-1] if reverse else points
        for shift in range(4):
            yield np.asarray(ordered[shift:] + ordered[:shift], dtype=np.float64)


def compare(reference, candidate, width, height):
    diagonal = math.hypot(width, height)
    best = None
    for ordered in permutations(candidate):
        errors = np.linalg.norm(ordered - reference, axis=1)
        result = {
            "mean_error_px": float(errors.mean()),
            "max_error_px": float(errors.max()),
            "normalized_mean_error": float(errors.mean() / diagonal),
            "normalized_max_error": float(errors.max() / diagonal),
            "ordered": ordered,
        }
        if best is None or result["mean_error_px"] < best["mean_error_px"]:
            best = result
    ref_area = abs(cv2.contourArea(reference.astype(np.float32)))
    pred = best["ordered"].astype(np.float32)
    pred_area = abs(cv2.contourArea(pred))
    intersection, _ = cv2.intersectConvexConvex(reference.astype(np.float32), pred)
    union = ref_area + pred_area - float(intersection)
    best["iou"] = float(intersection / union) if union > 0 else 0.0
    best.pop("ordered")
    return best


def draw_overlay(image, reference, result, filename):
    overlay = image.copy()
    if reference is not None:
        cv2.polylines(overlay, [order_quad(reference).astype(np.int32)], True, (0, 220, 0), 5)
    selected = result.get("selected")
    displayed = selected
    if displayed is None and result.get("candidates"):
        displayed = result["candidates"][0]
    if displayed is not None:
        color = (0, 0, 255) if selected is not None else (0, 165, 255)
        cv2.polylines(overlay, [displayed["points"].astype(np.int32)], True, color, 3)
        for point in displayed["points"].astype(np.int32):
            cv2.circle(overlay, tuple(point), 7, color, -1)
    text = f"{filename} | {result['status']} | candidates={len(result['candidates'])}"
    cv2.putText(overlay, text, (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    return overlay


class FullCardTracker:
    """Detector-assisted tracker with explicit loss and recovery states."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.points = None
        self.pending = None
        self.pending_count = 0
        self.previous_gray = None
        self.state = "LOST"
        self.had_lock = False

    def update(self, image):
        tracking = self.state == "TRACKING"
        result = detect(
            image,
            self.points if tracking else None,
            fast=tracking,
        )
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        selected = result["selected"]
        if self.state == "TRACKING" and self.points is not None:
            tracked = self._forward_backward(gray)
            prediction_matches = (
                selected is not None
                and tracked is not None
                and self._close(tracked, selected["points"], gray.shape)
            )
            detector_matches = (
                selected is not None
                and self._close(self.points, selected["points"], gray.shape)
            )
            if prediction_matches:
                self.points = 0.65 * tracked + 0.35 * selected["points"]
            elif tracked is None and detector_matches:
                self.points = selected["points"].copy()
            else:
                self.points = None
                self.pending = None
                self.pending_count = 0
                self.state = "REACQUIRING" if selected is not None else "LOST"
                if selected is not None:
                    self._update_pending(selected)
        else:
            self._update_pending(selected)
            if self.pending is None:
                self.points = None
                self.state = "LOST"
            elif self.pending_count >= LOCK_FRAMES:
                self.points = self.pending.copy()
                self.pending = None
                self.pending_count = 0
                self.had_lock = True
                self.state = "TRACKING"
            else:
                self.state = "REACQUIRING" if self.had_lock else "ACQUIRING"

        if self.state == "TRACKING" and self.points is not None:
            result["tracked_points"] = self.points.copy()
        else:
            self.points = None if self.state != "TRACKING" else self.points
            result.pop("tracked_points", None)
        result["status"] = self.state
        result["selected"] = selected
        self.previous_gray = gray
        return result

    def _update_pending(self, selected):
        if selected is None:
            self.pending = None
            self.pending_count = 0
            return
        points = selected["points"]
        if self.pending is not None and _same_candidate(self.pending, points):
            self.pending = points.copy()
            self.pending_count += 1
        else:
            self.pending = points.copy()
            self.pending_count = 1

    def _forward_backward(self, gray):
        if self.previous_gray is None or self.points is None:
            return None
        old = self.points.reshape(-1, 1, 2).astype(np.float32)
        forward, status, error = cv2.calcOpticalFlowPyrLK(
            self.previous_gray, gray, old, None, winSize=(21, 21), maxLevel=3
        )
        if forward is None or status is None or error is None or int(status.sum()) != 4:
            return None
        backward, back_status, _ = cv2.calcOpticalFlowPyrLK(
            gray, self.previous_gray, forward, None, winSize=(21, 21), maxLevel=3
        )
        if backward is None or back_status is None or int(back_status.sum()) != 4:
            return None
        if float(np.mean(np.linalg.norm(old - backward, axis=2))) > 2.5:
            return None
        if float(error.max()) > 35.0:
            return None
        points = order_quad(forward.reshape(4, 2))
        metrics = candidate_metrics(gray, points)
        return points if metrics["valid"] else None

    @staticmethod
    def _close(first, second, shape):
        diagonal = math.hypot(shape[1], shape[0])
        return float(np.mean(np.linalg.norm(order_quad(first) - order_quad(second), axis=1))) <= 0.03 * diagonal


def load_annotations():
    with ANNOTATIONS.open(encoding="utf-8") as handle:
        return [
            record
            for record in json.load(handle)
            if record.get("annotation_status") == "valid_complete_card"
        ]


def run_benchmark():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    OVERLAYS.mkdir(parents=True, exist_ok=True)
    rows = []
    timings = []
    for record in load_annotations():
        image = cv2.imread(record["source_path"])
        if image is None:
            raise RuntimeError(f"could not decode {record['source_path']}")
        start = time.perf_counter()
        result = detect(image)
        elapsed = (time.perf_counter() - start) * 1000.0
        timings.append(elapsed)
        selected = result["selected"]
        metrics = compare(
            np.asarray(record["corners"], dtype=np.float32),
            selected["points"],
            image.shape[1],
            image.shape[0],
        ) if selected is not None else {}
        correct = bool(
            selected is not None
            and metrics["normalized_mean_error"] <= 0.02
            and metrics["normalized_max_error"] <= 0.04
        )
        rows.append({
            "filename": record["filename"],
            "class": record["class"],
            "status": result["status"],
            "candidate_count": len(result["candidates"]),
            "verified": bool(selected is not None),
            "correct_full_card": correct,
            "mean_error_percent": metrics.get("normalized_mean_error", 0.0) * 100.0,
            "max_error_percent": metrics.get("normalized_max_error", 0.0) * 100.0,
            "iou": metrics.get("iou", 0.0),
            "elapsed_ms": elapsed,
            "reason": result["reason"],
        })
        overlay = draw_overlay(
            image,
            np.asarray(record["corners"], dtype=np.float32),
            result,
            record["filename"],
        )
        cv2.imwrite(str(OVERLAYS / record["filename"]), overlay)

    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    correct = sum(row["correct_full_card"] for row in rows)
    verified = sum(row["verified"] for row in rows)
    errors = sorted(row["mean_error_percent"] for row in rows if row["verified"])
    summary = {
        "eligible_images": len(rows),
        "verified_detections": verified,
        "correct_full_card_detections": correct,
        "incorrect_or_internal_detections": verified - correct,
        "missed_or_uncertain": len(rows) - verified,
        "internal_region_false_locks": verified - correct,
        "mean_corner_error_percent_verified": float(np.mean(errors)) if errors else None,
        "p95_corner_error_percent_verified": float(np.percentile(errors, 95)) if errors else None,
        "mean_processing_ms": float(np.mean(timings)),
        "p95_processing_ms": float(np.percentile(timings, 95)),
        "static_acceptance": {
            "correct_at_least_26": correct >= 26,
            "false_locks_zero": verified - correct == 0,
            "missed_at_most_3": len(rows) - verified <= 3,
            "mean_error_at_most_2_percent": bool(errors and np.mean(errors) <= 2.0),
            "p95_error_at_most_4_percent": bool(errors and np.percentile(errors, 95) <= 4.0),
        },
        "live_physical_testing": "not run by automated benchmark",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(summary, rows)
    return summary


def write_report(summary, rows):
    acceptance = summary["static_acceptance"]
    lines = [
        "# Experimental Full-Card Detector and Tracker",
        "",
        "This experiment is isolated from production recognition and preprocessing.",
        "A verified candidate requires four-edge continuity, near-card geometry, "
        "inside/outside contrast, and non-clipped coordinates.",
        "",
        "## Static benchmark",
        "",
        f"- Eligible manual complete cards: **{summary['eligible_images']}**",
        f"- Verified detections: **{summary['verified_detections']}**",
        f"- Correct full-card detections: **{summary['correct_full_card_detections']}**",
        f"- Incorrect/internal detections: **{summary['incorrect_or_internal_detections']}**",
        f"- Missed/uncertain: **{summary['missed_or_uncertain']}**",
        f"- Mean verified corner error: **{summary['mean_corner_error_percent_verified']}%**",
        f"- 95th-percentile verified corner error: **{summary['p95_corner_error_percent_verified']}%**",
        f"- Mean detection time: **{summary['mean_processing_ms']:.2f} ms**",
        f"- 95th-percentile detection time: **{summary['p95_processing_ms']:.2f} ms**",
        "",
        "## Mandatory static acceptance",
        "",
        "| Criterion | Required | Result |",
        "|---|---:|---:|",
        f"| Correct full-card detections | >= 26/29 | {'PASS' if acceptance['correct_at_least_26'] else 'FAIL'} |",
        f"| Internal-region false locks | 0 | {'PASS' if acceptance['false_locks_zero'] else 'FAIL'} |",
        f"| Missed detections | <= 3/29 | {'PASS' if acceptance['missed_at_most_3'] else 'FAIL'} |",
        f"| Mean corner error | <= 2% | {'PASS' if acceptance['mean_error_at_most_2_percent'] else 'FAIL'} |",
        f"| 95th-percentile error | <= 4% | {'PASS' if acceptance['p95_error_at_most_4_percent'] else 'FAIL'} |",
        "",
        "## Per-image results",
        "",
        "| Image | Status | Candidates | Verified | Correct | Mean error % | IoU | Time ms |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['filename']} | {row['status']} | {row['candidate_count']} | "
            f"{row['verified']} | {row['correct_full_card']} | "
            f"{row['mean_error_percent']:.2f} | {row['iou']:.3f} | {row['elapsed_ms']:.2f} |"
        )
    lines.extend([
        "",
        "## Live validation status",
        "",
        "Physical camera acquisition, 300-frame jitter, slow-motion tracking, "
        "obstruction, and 5-minute memory tests were not run by this automated "
        "benchmark. They remain required before any integration decision.",
        "",
        "See `validation_results/full_card_validation.csv`, "
        "`validation_results/full_card_summary.json`, and "
        "`validation_results/comparison_overlays/`.",
    ])
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_live(device):
    camera = cv2.VideoCapture(device)
    if not camera.isOpened():
        raise RuntimeError(f"could not open camera {device}")
    tracker = FullCardTracker()
    previous = time.perf_counter()
    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                raise RuntimeError("camera returned no frame")
            result = tracker.update(frame)
            display = frame.copy()
            points = result.get("tracked_points")
            if (
                points is None
                and result["status"] in {"ACQUIRING", "REACQUIRING"}
                and result.get("selected") is not None
            ):
                points = result["selected"]["points"]
            if points is not None:
                color = {
                    "TRACKING": (0, 220, 0),
                    "ACQUIRING": (255, 180, 0),
                    "REACQUIRING": (0, 165, 255),
                }.get(result["status"], (0, 0, 255))
                cv2.polylines(display, [order_quad(points).astype(np.int32)], True, color, 3)
            now = time.perf_counter()
            fps = 1.0 / max(now - previous, 1e-6)
            previous = now
            cv2.putText(
                display,
                f"{result['status']} | {fps:.1f} FPS | candidates={len(result['candidates'])}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )
            cv2.imshow("Experimental Full-Card Boundary", display)
            if cv2.waitKey(1) & 0xFF in (27, ord("q")):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--device", type=int, default=0)
    args = parser.parse_args()
    if args.live:
        run_live(args.device)
    else:
        summary = run_benchmark()
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
