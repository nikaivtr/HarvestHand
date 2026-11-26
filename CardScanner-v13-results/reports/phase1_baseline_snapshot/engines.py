"""Independent, dependency-light recognition engines used by the lab."""

from __future__ import annotations

import math
import time
from pathlib import Path
from typing import Any

import cv2
import numpy as np


def read_image(path: str | Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not read image: {path}")
    return image


def _order_points(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=np.float32).reshape(4, 2)
    center = points.mean(axis=0)
    ordered = points[np.argsort(np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0]))]
    if cv2.contourArea(ordered, oriented=True) < 0:
        ordered = ordered[::-1]
    return ordered


def _segments_intersect(first_start, first_end, second_start, second_end) -> bool:
    def orientation(a, b, c) -> float:
        return float((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))

    def on_segment(a, b, c) -> bool:
        return (
            min(a[0], b[0]) <= c[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
        )

    first = orientation(first_start, first_end, second_start)
    second = orientation(first_start, first_end, second_end)
    third = orientation(second_start, second_end, first_start)
    fourth = orientation(second_start, second_end, first_end)
    if first == 0 and on_segment(first_start, first_end, second_start):
        return True
    if second == 0 and on_segment(first_start, first_end, second_end):
        return True
    if third == 0 and on_segment(second_start, second_end, first_start):
        return True
    if fourth == 0 and on_segment(second_start, second_end, first_end):
        return True
    return (first > 0) != (second > 0) and (third > 0) != (fourth > 0)


def validate_quad_geometry(
    points: np.ndarray, image_shape: tuple[int, ...],
    min_area_ratio: float = 0.01, max_area_ratio: float = 0.92,
    min_aspect_ratio: float = 0.45, max_aspect_ratio: float = 0.90,
    max_perspective_distortion: float = 0.45,
) -> tuple[bool, list[str]]:
    """Reject malformed or implausible card-like quads before queueing."""
    reasons: list[str] = []
    try:
        points = np.asarray(points, dtype=np.float32).reshape(4, 2)
    except (TypeError, ValueError):
        return False, ["exactly four corners required"]
    if not np.isfinite(points).all():
        reasons.append("non-finite corner")
    if len({(round(float(x), 2), round(float(y), 2)) for x, y in points}) != 4:
        reasons.append("duplicate corners")
    if _segments_intersect(points[0], points[1], points[2], points[3]) or _segments_intersect(
        points[1], points[2], points[3], points[0]
    ):
        reasons.append("self-intersecting input order")
    ordered = _order_points(points)
    if not cv2.isContourConvex(ordered.reshape(-1, 1, 2)):
        reasons.append("non-convex")
    if _segments_intersect(ordered[0], ordered[1], ordered[2], ordered[3]) or _segments_intersect(
        ordered[1], ordered[2], ordered[3], ordered[0]
    ):
        reasons.append("self-intersecting")
    height, width = image_shape[:2]
    area = abs(float(cv2.contourArea(ordered)))
    area_ratio = area / max(width * height, 1)
    if not min_area_ratio <= area_ratio <= max_area_ratio:
        reasons.append("area outside limits")
    sides = np.array([
        np.linalg.norm(ordered[(index + 1) % 4] - ordered[index])
        for index in range(4)
    ])
    if float(sides.min()) < max(8.0, min(width, height) * 0.02):
        reasons.append("collapsed edge")
    long_side = max(float(sides[0] + sides[2]), float(sides[1] + sides[3]), 1.0)
    short_side = min(float(sides[0] + sides[2]), float(sides[1] + sides[3]))
    aspect = short_side / long_side
    if not min_aspect_ratio <= aspect <= max_aspect_ratio:
        reasons.append("implausible card aspect")
    opposite_ratio = min(
        sides[0] / max(sides[2], 1.0), sides[2] / max(sides[0], 1.0),
        sides[1] / max(sides[3], 1.0), sides[3] / max(sides[1], 1.0),
    )
    if opposite_ratio < 0.55:
        reasons.append("excessive perspective")
    perspective = (abs(sides[0] - sides[2]) + abs(sides[1] - sides[3])) / long_side
    if perspective > max_perspective_distortion:
        reasons.append("uneven perspective")
    angles = []
    for index in range(4):
        before = ordered[(index - 1) % 4] - ordered[index]
        after = ordered[(index + 1) % 4] - ordered[index]
        denominator = max(float(np.linalg.norm(before) * np.linalg.norm(after)), 1.0)
        angles.append(float(np.degrees(np.arccos(np.clip(np.dot(before, after) / denominator, -1, 1)))))
    if min(angles) < 25 or max(angles) > 155:
        reasons.append("invalid corner angle")
    return not reasons, reasons


def _edge_support(edges: np.ndarray, points: np.ndarray) -> float:
    values = []
    for start, end in zip(points, np.roll(points, -1, axis=0)):
        length = max(int(np.linalg.norm(end - start)), 2)
        hits = 0
        for point in np.linspace(start, end, min(length, 180)):
            x, y = np.rint(point).astype(int)
            x0, x1 = max(0, x - 2), min(edges.shape[1], x + 3)
            y0, y1 = max(0, y - 2), min(edges.shape[0], y + 3)
            hits += int(edges[y0:y1, x0:x1].any())
        values.append(hits / min(length, 180))
    return float(min(values)) if values else 0.0


def candidate_metrics(
    image: np.ndarray, points: np.ndarray, edges: np.ndarray | None = None,
    method: str = "canny",
) -> dict[str, Any]:
    """Return measurable features without declaring a candidate correct."""
    height, width = image.shape[:2]
    points = _order_points(points)
    contour = points.reshape(-1, 1, 2)
    area = abs(float(cv2.contourArea(contour)))
    sides = np.array([
        np.linalg.norm(points[(index + 1) % 4] - points[index])
        for index in range(4)
    ])
    long_side = max(float(sides[0] + sides[2]), float(sides[1] + sides[3]), 1.0)
    short_side = min(float(sides[0] + sides[2]), float(sides[1] + sides[3]))
    aspect = short_side / long_side
    min_rect = cv2.minAreaRect(contour.astype(np.float32))
    rect_width, rect_height = min_rect[1]
    rect_area = max(float(rect_width * rect_height), 1.0)
    angles = []
    for index in range(4):
        before = points[(index - 1) % 4] - points[index]
        after = points[(index + 1) % 4] - points[index]
        denominator = max(float(np.linalg.norm(before) * np.linalg.norm(after)), 1.0)
        angles.append(float(np.degrees(np.arccos(np.clip(np.dot(before, after) / denominator, -1, 1)))))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x, y, box_width, box_height = cv2.boundingRect(contour)
    inner = gray[max(y, 0):min(y + box_height, height), max(x, 0):min(x + box_width, width)]
    sharpness = float(cv2.Laplacian(inner, cv2.CV_64F).var()) if inner.size else 0.0
    if edges is None:
        edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
    support = _edge_support(edges, points)
    margin = min(float(x), float(y), float(width - (x + box_width)), float(height - (y + box_height)))
    rotation = float(min_rect[2])
    geometry = max(0.0, 1.0 - abs(aspect - 0.714) / 0.714)
    rectangularity = min(area / rect_area, 1.0)
    confidence = 0.35 * geometry + 0.25 * rectangularity + 0.25 * support + 0.15 * min(area / (width * height) / 0.2, 1.0)
    return {
        "area": round(area, 2),
        "area_ratio": round(area / max(width * height, 1), 6),
        "width": round(float(box_width), 2),
        "height": round(float(box_height), 2),
        "aspect_ratio": round(float(aspect), 4),
        "corner_angles": [round(value, 2) for value in angles],
        "convexity": bool(cv2.isContourConvex(contour)),
        "rectangularity": round(rectangularity, 4),
        "edge_support": round(support, 4),
        "border_strength": round(support, 4),
        "perspective_distortion": round(float(abs(sides[0] - sides[2]) + abs(sides[1] - sides[3])) / long_side, 4),
        "rotation": round(rotation, 3),
        "sharpness": round(sharpness, 2),
        "frame_margin": round(margin, 2),
        "geometry_score": round(geometry, 4),
        "confidence": round(float(confidence), 4),
        "detection_method": method,
    }


def _candidate_iou(first: np.ndarray, second: np.ndarray) -> float:
    first_box = cv2.boundingRect(first.astype(np.float32))
    second_box = cv2.boundingRect(second.astype(np.float32))
    ax0, ay0, aw, ah = first_box
    bx0, by0, bw, bh = second_box
    ix0, iy0 = max(ax0, bx0), max(ay0, by0)
    ix1, iy1 = min(ax0 + aw, bx0 + bw), min(ay0 + ah, by0 + bh)
    intersection = max(0, ix1 - ix0) * max(0, iy1 - iy0)
    union = aw * ah + bw * bh - intersection
    return intersection / union if union else 0.0


def detect_boundary_candidates(
    image: np.ndarray,
    max_candidates: int = 12,
    min_area_ratio: float = 0.01,
    max_area_ratio: float = 0.92,
    min_aspect_ratio: float = 0.45,
    max_aspect_ratio: float = 0.90,
    max_perspective_distortion: float = 0.45,
    min_edge_support: float = 0.08,
    outer_profile: dict[str, Any] | None = None,
    rank_candidates: bool = True,
) -> list[dict[str, Any]]:
    """Generate multiple plausible quads from several independent masks."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    masks = [
        ("canny_50_150", cv2.Canny(blurred, 50, 150)),
        ("canny_25_100", cv2.Canny(blurred, 25, 100)),
        ("adaptive", cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 5,
        )),
    ]
    height, width = gray.shape
    candidates: list[dict[str, Any]] = []
    for method, raw_mask in masks:
        mask = cv2.morphologyEx(raw_mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            if perimeter <= 0:
                continue
            approx = cv2.approxPolyDP(contour, 0.025 * perimeter, True)
            if len(approx) != 4 or not cv2.isContourConvex(approx):
                continue
            points = _order_points(approx.reshape(4, 2))
            metrics = candidate_metrics(image, points, cv2.Canny(blurred, 50, 150), method)
            if not min_area_ratio <= metrics["area_ratio"] <= max_area_ratio:
                continue
            if not min_aspect_ratio <= metrics["aspect_ratio"] <= max_aspect_ratio:
                continue
            if metrics["edge_support"] < min_edge_support:
                continue
            valid, reasons = validate_quad_geometry(
                points, image.shape, min_area_ratio, max_area_ratio,
                min_aspect_ratio, max_aspect_ratio, max_perspective_distortion,
            )
            if not valid:
                continue
            if any(
                _candidate_iou(points, prior["points"]) > 0.92
                or CandidateTracker._distance(points, prior["points"]) < 0.08
                for prior in candidates
            ):
                continue
            if outer_profile:
                from recognition_lab.analysis import score_outer_candidate
                metrics["outer_reference_score"] = score_outer_candidate(metrics, outer_profile)
            metrics["geometry_rejection_reasons"] = reasons
            candidates.append({"points": points, "metrics": metrics})
    _mark_nested_regions(candidates)
    if rank_candidates:
        candidates.sort(
            key=lambda item: (
                item["metrics"].get("outer_reference_score", 0.0),
                item["metrics"]["confidence"],
            ),
            reverse=True,
        )
    return candidates[:max(1, int(max_candidates))]


def _mark_nested_regions(candidates: list[dict[str, Any]]) -> None:
    """Flag plausible internal card sections without hiding them diagnostically."""
    for child in candidates:
        child["metrics"]["likely_internal_region"] = False
        child["metrics"]["internal_parent_indices"] = []
        child_area = child["metrics"]["area"]
        for parent_index, parent in enumerate(candidates):
            if parent is child or parent["metrics"]["area"] <= child_area * 1.25:
                continue
            parent_contour = np.float32(parent["points"]).reshape(-1, 1, 2)
            contained = all(
                cv2.pointPolygonTest(parent_contour, (float(point[0]), float(point[1])), False) >= -2
                for point in child["points"]
            )
            if contained and child_area / parent["metrics"]["area"] <= 0.78:
                child["metrics"]["likely_internal_region"] = True
                child["metrics"]["internal_parent_indices"].append(parent_index)


def detect_boundary(image: np.ndarray) -> dict[str, Any]:
    """Backward-compatible single-result wrapper for non-Phase-1 callers."""
    candidates = detect_boundary_candidates(image, max_candidates=1)
    if not candidates:
        return {"found": False, "points": None, "score": 0.0}
    item = candidates[0]
    return {"found": True, "points": item["points"].tolist(), "score": item["metrics"]["confidence"]}


class CandidateTracker:
    """Associate quads over time while retaining short-lived missing tracks."""

    def __init__(
        self, max_candidates: int = 12, match_threshold: float = 0.35,
        grace_seconds: float = 0.75, smoothing: float = 0.35,
    ) -> None:
        self.max_candidates = max(1, int(max_candidates))
        self.match_threshold = max(0.05, float(match_threshold))
        self.grace_seconds = max(0.05, float(grace_seconds))
        self.smoothing = min(max(float(smoothing), 0.0), 1.0)
        self.next_id = 1
        self.tracks: dict[int, dict[str, Any]] = {}
        self.total_frames = 0

    @staticmethod
    def _distance(first: np.ndarray, second: np.ndarray) -> float:
        diagonal = max(float(np.linalg.norm(first.max(axis=0) - first.min(axis=0))), 1.0)
        corner_distance = float(np.mean(np.linalg.norm(first - second, axis=1))) / diagonal
        iou_distance = 1.0 - _candidate_iou(first, second)
        centers = float(np.linalg.norm(first.mean(axis=0) - second.mean(axis=0))) / diagonal
        return 0.55 * corner_distance + 0.25 * iou_distance + 0.20 * centers

    def update(self, detections: list[dict[str, Any]], dt: float, detected: bool = True) -> list[dict[str, Any]]:
        self.total_frames += 1
        dt = max(0.0, min(float(dt), 1.0))
        unmatched_tracks = set(self.tracks)
        unmatched_detections = set(range(len(detections)))
        pairs = []
        for track_id, track in self.tracks.items():
            for index, detection in enumerate(detections):
                distance = self._distance(track["points"], detection["points"])
                if distance <= self.match_threshold:
                    pairs.append((distance, track_id, index))
        for _, track_id, index in sorted(pairs):
            if track_id not in unmatched_tracks or index not in unmatched_detections:
                continue
            track = self.tracks[track_id]
            detection = detections[index]
            movement = float(np.mean(np.linalg.norm(track["points"] - detection["points"], axis=1)))
            track["movement_sum"] += movement
            track["movement_count"] += 1
            track["points"] = (
                track["points"] * self.smoothing
                + detection["points"] * (1.0 - self.smoothing)
            )
            track["metrics"] = detection["metrics"]
            track["status"] = "live" if detected else "tracked"
            track["missing_seconds"] = 0.0
            track["seen_frames"] += 1
            track["duration_seconds"] += dt
            unmatched_tracks.remove(track_id)
            unmatched_detections.remove(index)
        for track_id in list(unmatched_tracks):
            track = self.tracks[track_id]
            if not detected:
                track["status"] = "tracked"
            else:
                track["missing_seconds"] += dt
                track["status"] = "temporarily_lost"
            track["duration_seconds"] += dt
            if track["missing_seconds"] > self.grace_seconds:
                del self.tracks[track_id]
        for index in sorted(unmatched_detections):
            if len(self.tracks) >= self.max_candidates:
                break
            detection = detections[index]
            track_id = self.next_id
            self.next_id += 1
            self.tracks[track_id] = {
                "id": track_id,
                "points": detection["points"].copy(),
                "metrics": detection["metrics"],
                "status": "live",
                "missing_seconds": 0.0,
                "seen_frames": 1,
                "duration_seconds": 0.0,
                "judgment": None,
                "movement_sum": 0.0,
                "movement_count": 0,
            }
        return self.active()

    def active(self) -> list[dict[str, Any]]:
        result = []
        for track in sorted(self.tracks.values(), key=lambda item: item["id"]):
            copy = dict(track)
            copy["points"] = track["points"].copy()
            copy["metrics"] = dict(track["metrics"])
            average_movement = track["movement_sum"] / max(track["movement_count"], 1)
            copy["metrics"]["tracking_duration"] = round(track["duration_seconds"], 3)
            copy["metrics"]["seen_frames"] = track["seen_frames"]
            copy["metrics"]["position_stability"] = round(1.0 / (1.0 + average_movement), 6)
            result.append(copy)
        return result


def compare_images(observation: np.ndarray, reference: np.ndarray) -> dict[str, float]:
    target_size = (256, 360)
    a = cv2.resize(observation, target_size, interpolation=cv2.INTER_AREA)
    b = cv2.resize(reference, target_size, interpolation=cv2.INTER_AREA)
    gray_a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    mse = float(np.mean((gray_a.astype(np.float32) - gray_b.astype(np.float32)) ** 2))
    ssim = max(0.0, 1.0 - mse / (255.0 * 255.0))
    orb = cv2.ORB_create(nfeatures=500)
    key_a, desc_a = orb.detectAndCompute(gray_a, None)
    key_b, desc_b = orb.detectAndCompute(gray_b, None)
    matches = 0
    if desc_a is not None and desc_b is not None and len(desc_a) and len(desc_b):
        raw = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(desc_a, desc_b, k=2)
        matches = sum(1 for pair in raw if len(pair) == 2 and pair[0].distance < 0.75 * pair[1].distance)
    orb_score = min(matches / 30.0, 1.0)
    return {"ssim": round(ssim, 4), "orb_matches": float(matches), "orb_score": round(orb_score, 4),
            "combined": round(0.45 * ssim + 0.55 * orb_score, 4)}


def ocr_text(image: np.ndarray) -> dict[str, Any]:
    """Best-effort OCR hook using OpenCV preprocessing; no hidden ground truth."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return {"text": "", "preprocessed": binary, "backend": "opencv-preprocessing",
            "message": "Install and configure Tesseract, EasyOCR, or PaddleOCR to enable text output."}


def perspective_crop(image: np.ndarray, points: list[list[float]], size=(640, 900)) -> np.ndarray:
    source = _order_points(np.float32(points))
    target = np.float32([[0, 0], [size[0] - 1, 0], [size[0] - 1, size[1] - 1], [0, size[1] - 1]])
    return cv2.warpPerspective(image, cv2.getPerspectiveTransform(source, target), size)
