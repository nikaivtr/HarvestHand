"""Isolated multi-scale visual card-localization experiment.

This module intentionally does not modify or monkey-patch production code.
Candidate coordinates are experimental measurements. They are never treated
as ground truth without manual review.
"""

import csv
import math
import os
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pygame
from PIL import Image, ImageDraw, ImageFont

EXPERIMENT = Path(__file__).resolve().parent
ROOT = EXPERIMENT.parent.parent
DATASET = ROOT / "data" / "card_samples"
INPUT_CSV = ROOT / "boundary_diagnostics_rejected" / "rejected_images_audit.csv"
RESULTS_CSV = EXPERIMENT / "visual_localization_results.csv"
COMPARISON_CSV = EXPERIMENT / "method_comparison.csv"
OVERLAY_DIR = EXPERIMENT / "detection_overlays"
CROP_DIR = EXPERIMENT / "corrected_candidate_crops"
SHEET_DIR = EXPERIMENT / "contact_sheets"
REVIEW_DIR = EXPERIMENT / "manual_review"
REPORT = EXPERIMENT / "VISUAL_LOCALIZATION_EXPERIMENT_REPORT.md"

sys.path.insert(0, str(ROOT))
import cardscan.features as features
import cardscan.preprocess as preprocess


METHODS = ("existing", "multi_scale", "contrast_enhanced", "combined")
SCALES = (0.50, 0.75, 1.00, 1.50)
ENHANCEMENTS = ("raw", "clahe", "normalize", "gamma", "lab")
MAX_PROCESSING_DIMENSION = 1440
CARD_ASPECT = preprocess.CARD_ASPECT
CANVAS = (preprocess.CANVAS_W, preprocess.CANVAS_H)


def font(size):
    for path in ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def order_points(points):
    points = np.asarray(points, dtype=np.float32)
    ordered = np.zeros((4, 2), dtype=np.float32)
    sums = points.sum(axis=1)
    ordered[0] = points[np.argmin(sums)]
    ordered[2] = points[np.argmax(sums)]
    diffs = np.diff(points, axis=1)
    ordered[1] = points[np.argmin(diffs)]
    ordered[3] = points[np.argmax(diffs)]
    return ordered


def corner_angles(rect):
    result = []
    for index in range(4):
        before = rect[(index - 1) % 4] - rect[index]
        after = rect[(index + 1) % 4] - rect[index]
        denom = max(np.linalg.norm(before) * np.linalg.norm(after), 1.0)
        cosine = np.dot(before, after) / denom
        result.append(math.degrees(math.acos(np.clip(cosine, -1.0, 1.0))))
    return result


def sample_edge_metric(gray, points):
    edges = cv2.Canny(gray, 50, 150)
    height, width = gray.shape[:2]
    continuity = []
    contrast = []
    rect = order_points(points)
    for start, end in zip(rect, np.roll(rect, -1, axis=0)):
        length = max(int(np.linalg.norm(end - start)), 2)
        xs = np.rint(np.linspace(start[0], end[0], length)).astype(int)
        ys = np.rint(np.linspace(start[1], end[1], length)).astype(int)
        good = 0
        contrast_values = []
        tangent = (end - start) / max(np.linalg.norm(end - start), 1.0)
        normal = np.array([-tangent[1], tangent[0]])
        midpoint = (start + end) / 2.0
        if np.dot(normal, rect.mean(axis=0) - midpoint) < 0:
            normal = -normal
        for x, y in zip(xs, ys):
            x0, x1 = max(0, x - 3), min(width, x + 4)
            y0, y1 = max(0, y - 3), min(height, y + 4)
            good += int(edges[y0:y1, x0:x1].any())
            inside = np.rint([x, y] + normal * 6).astype(int)
            outside = np.rint([x, y] - normal * 6).astype(int)
            inside = np.clip(inside, [0, 0], [width - 1, height - 1])
            outside = np.clip(outside, [0, 0], [width - 1, height - 1])
            contrast_values.append(abs(
                float(gray[inside[1], inside[0]])
                - float(gray[outside[1], outside[0]])
            ))
        continuity.append(good / float(length))
        contrast.append(sum(contrast_values) / max(len(contrast_values), 1))
    return continuity, contrast


def metrics_for(gray, points):
    height, width = gray.shape[:2]
    rect = order_points(points)
    sides = [
        np.linalg.norm(rect[1] - rect[0]),
        np.linalg.norm(rect[2] - rect[1]),
        np.linalg.norm(rect[2] - rect[3]),
        np.linalg.norm(rect[3] - rect[0]),
    ]
    horizontal = (sides[0] + sides[2]) / 2.0
    vertical = (sides[1] + sides[3]) / 2.0
    aspect = min(horizontal, vertical) / max(horizontal, vertical, 1.0)
    angles = corner_angles(rect)
    continuity, contrast = sample_edge_metric(gray, rect)
    top_angle = math.degrees(math.atan2(
        rect[1][1] - rect[0][1], rect[1][0] - rect[0][0]
    ))
    area_ratio = abs(cv2.contourArea(rect)) / float(width * height)
    opposite = min(
        sides[0] / max(sides[2], 1.0), sides[2] / max(sides[0], 1.0),
        sides[1] / max(sides[3], 1.0), sides[3] / max(sides[1], 1.0),
    )
    clipped = int(np.any(rect[:, 0] <= 2) or np.any(rect[:, 1] <= 2)
                   or np.any(rect[:, 0] >= width - 3)
                   or np.any(rect[:, 1] >= height - 3))
    aspect_score = max(0.0, 1.0 - abs(aspect - CARD_ASPECT) / CARD_ASPECT)
    angle_score = max(
        0.0, 1.0 - max(abs(min(angles) - 90), abs(max(angles) - 90)) / 90
    )
    geometry_score = (
        0.35 * aspect_score
        + 0.25 * opposite
        + 0.25 * angle_score
        + 0.15 * (1.0 - clipped)
    )
    edge_score = min(1.0, 0.7 * min(continuity) + 0.3 * sum(continuity) / 4)
    contrast_score = min(1.0, sum(contrast) / 4 / 45.0)
    area_score = min(1.0, math.sqrt(max(area_ratio, 0.0) / 0.15))
    overall_score = (
        0.40 * geometry_score
        + 0.25 * edge_score
        + 0.25 * contrast_score
        + 0.10 * area_score
    )
    if overall_score >= 0.70 and edge_score >= 0.20 and not clipped:
        category = "strong"
    elif overall_score >= 0.50:
        category = "possible"
    else:
        category = "weak"
    return {
        "area_ratio": float(area_ratio),
        "width_ratio": float(horizontal / width),
        "height_ratio": float(vertical / height),
        "aspect_ratio": float(aspect),
        "rotation_deg": float(top_angle),
        "corner_angle_min_deg": float(min(angles)),
        "corner_angle_max_deg": float(max(angles)),
        "opposite_side_ratio": float(opposite),
        "edge_continuity_min": float(min(continuity)),
        "edge_continuity_mean": float(sum(continuity) / 4),
        "edge_contrast_min": float(min(contrast)),
        "edge_contrast_mean": float(sum(contrast) / 4),
        "geometry_score": float(geometry_score),
        "edge_score": float(edge_score),
        "contrast_score": float(contrast_score),
        "area_score": float(area_score),
        "overall_score": float(overall_score),
        "clipped": bool(clipped),
        "rank_category": category,
    }


def enhance(gray, method):
    if method == "raw":
        return gray
    if method == "clahe":
        return cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    if method == "normalize":
        return cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    if method == "gamma":
        table = np.array([
            min(255, int(((value / 255.0) ** 0.85) * 255))
            for value in range(256)
        ], dtype=np.uint8)
        return cv2.LUT(gray, table)
    if method == "lab":
        rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
        lab[:, :, 0] = cv2.createCLAHE(
            clipLimit=1.5, tileGridSize=(8, 8)
        ).apply(lab[:, :, 0])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)[:, :, 0]
    raise ValueError(f"unknown enhancement: {method}")


def edge_masks(gray):
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    masks = []
    for low, high in ((30, 100), (50, 150), (80, 200)):
        masks.append(cv2.Canny(blurred, low, high))
    adaptive = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 5,
    )
    masks.append(adaptive)
    masks.append(cv2.morphologyEx(
        blurred, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)
    ))
    for threshold in (100, 140, 180):
        _, binary = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
        masks.append(binary)
    return [
        cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8),
                         iterations=2)
        for mask in masks
    ]


def find_candidates(gray, method_name, scale, enhancement):
    candidates = []
    image_area = gray.shape[0] * gray.shape[1]
    enhanced = enhance(gray, enhancement)
    for mask_index, mask in enumerate(edge_masks(enhanced)):
        contours, _ = cv2.findContours(
            mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 0.001 * image_area or area > 0.92 * image_area:
                continue
            perimeter = cv2.arcLength(contour, True)
            for epsilon in (0.01, 0.02, 0.04):
                approx = cv2.approxPolyDP(
                    contour, epsilon * perimeter, True
                )
                if len(approx) != 4 or not cv2.isContourConvex(approx):
                    continue
                points = order_points(approx.reshape(4, 2).astype(np.float32))
                metrics = metrics_for(gray, points)
                candidates.append({
                    "points": points / scale,
                    "metrics": metrics,
                    "method": method_name,
                    "scale": scale,
                    "enhancement": enhancement,
                    "mask_index": mask_index,
                })
    return deduplicate(candidates)


def deduplicate(candidates):
    selected = []
    for candidate in sorted(
        candidates,
        key=lambda item: item["metrics"]["overall_score"],
        reverse=True,
    ):
        points = candidate["points"]
        duplicate = False
        for previous in selected:
            distance = np.mean(np.linalg.norm(
                order_points(points) - order_points(previous["points"]), axis=1
            ))
            scale = max(
                np.linalg.norm(points[1] - points[0]),
                np.linalg.norm(points[3] - points[0]),
                1.0,
            )
            if distance / scale < 0.08:
                duplicate = True
                break
        if not duplicate:
            selected.append(candidate)
        if len(selected) >= 5:
            break
    return selected


def source_array(surface):
    raw = pygame.image.tobytes(surface, "RGB")
    width, height = surface.get_size()
    return np.frombuffer(raw, dtype=np.uint8).reshape(height, width, 3)


def candidate_crop(surface, points):
    rect = order_points(points)
    width = max(
        np.linalg.norm(rect[1] - rect[0]),
        np.linalg.norm(rect[2] - rect[3]),
    )
    height = max(
        np.linalg.norm(rect[3] - rect[0]),
        np.linalg.norm(rect[2] - rect[1]),
    )
    pad_x, pad_y = max(4.0, width * 0.05), max(4.0, height * 0.05)
    source = np.array([
        rect[0] - [pad_x, pad_y], rect[1] + [pad_x, -pad_y],
        rect[2] + [pad_x, pad_y], rect[3] + [-pad_x, pad_y],
    ], dtype=np.float32)
    out_width, out_height = max(32, int(width + 2 * pad_x)), max(
        32, int(height + 2 * pad_y)
    )
    destination = np.array([
        [0, 0], [out_width - 1, 0],
        [out_width - 1, out_height - 1], [0, out_height - 1],
    ], dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(source, destination)
    warped = cv2.warpPerspective(
        source_array(surface), matrix, (out_width, out_height)
    )
    return preprocess._array_to_surface(warped)


def run_extractor(surface, points):
    crop = candidate_crop(surface, points)
    start = time.perf_counter()
    vector = features.extract(crop)
    elapsed = (time.perf_counter() - start) * 1000
    return crop, bool(vector is not None), len(vector) if vector else 0, elapsed


def rescaled_gray(surface, scale):
    array = source_array(surface)
    height, width = array.shape[:2]
    if scale != 1.0:
        array = cv2.resize(
            array, (max(2, int(width * scale)), max(2, int(height * scale))),
            interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC,
        )
    return cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)


def method_candidates(surface, method):
    if method == "existing":
        return []
    if method == "multi_scale":
        jobs = [(scale, "raw") for scale in SCALES]
    elif method == "contrast_enhanced":
        jobs = [(1.0, enhancement) for enhancement in ENHANCEMENTS]
    else:
        jobs = [
            (scale, enhancement)
            for scale in SCALES for enhancement in ENHANCEMENTS
        ]
    candidates = []
    for scale, enhancement in jobs:
        gray = rescaled_gray(surface, scale)
        candidates.extend(find_candidates(gray, method, scale, enhancement))
    return deduplicate(candidates)


def load_test_rows():
    with INPUT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row for row in rows
        if row.get("primary_category") == "Boundary Detection Failure"
    ]


def existing_result(surface):
    _, details = preprocess.prepare_detailed(surface)
    return {
        "candidate_count": 0,
        "status": details.get("status", "failed"),
        "reason": details.get("reason", ""),
        "extractor_passed": False,
        "feature_length": 0,
        "processing_ms": 0.0,
        "top": None,
    }


def result_for_method(surface, method):
    started = time.perf_counter()
    if method == "existing":
        result = existing_result(surface)
        result["processing_ms"] = (time.perf_counter() - started) * 1000
        return result
    candidates = method_candidates(surface, method)
    top = candidates[0] if candidates else None
    if top is None:
        return {
            "candidate_count": 0,
            "status": "failed",
            "reason": "no experimental quadrilateral candidates",
            "extractor_passed": False,
            "feature_length": 0,
            "processing_ms": (time.perf_counter() - started) * 1000,
            "top": None,
        }
    return {
        "candidate_count": len(candidates),
        "status": "candidate_found",
        "reason": "",
        "extractor_passed": False,
        "feature_length": 0,
        "processing_ms": (time.perf_counter() - started) * 1000,
        "top": top,
        "all_candidates": candidates,
    }


def draw_overlay(surface, image_row, combined):
    array = source_array(surface).copy()
    image = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    candidates = combined.get("all_candidates", [])
    for index, candidate in enumerate(candidates[:3]):
        points = np.rint(candidate["points"]).astype(np.int32)
        category = candidate["metrics"]["rank_category"]
        color = (0, 200, 0) if category == "strong" else (
            (0, 180, 255) if category == "possible" else (0, 0, 255)
        )
        cv2.polylines(image, [points], True, color, 3)
        for corner, point in enumerate(points):
            x, y = int(point[0]), int(point[1])
            cv2.circle(image, (x, y), 7, color, -1)
            cv2.putText(image, str(corner + 1), (x + 8, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        label = f"{index + 1}:{category} {candidate['metrics']['overall_score']:.2f}"
        cv2.putText(image, label, (20, 35 + index * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    output = OVERLAY_DIR / image_row["filename"]
    cv2.imwrite(str(output), image)
    return output


def make_sheet(paths, output, labels, cell_size=(430, 350)):
    columns = 4
    cell_width, cell_height = cell_size
    sheet = Image.new(
        "RGB", (columns * cell_width, math.ceil(len(paths) / columns) * cell_height),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    title = font(14)
    for index, path in enumerate(paths):
        x = index % columns * cell_width
        y = index // columns * cell_height
        try:
            image = Image.open(path).convert("RGB")
            image.thumbnail((cell_width - 20, cell_height - 55))
            sheet.paste(image, (x + (cell_width - image.width) // 2, y + 24))
        except (OSError, ValueError):
            draw.text((x + 10, y + 120), "IMAGE UNAVAILABLE", fill="red",
                      font=title)
        draw.text((x + 8, y + 5), labels[index][:56], fill="black", font=title)
    sheet.save(output, quality=90)


def make_comparison_sheet(source_paths, overlay_paths, crop_paths, rows):
    paths = []
    labels = []
    for source, overlay, crop, row in zip(
        source_paths, overlay_paths, crop_paths, rows
    ):
        paths.extend((source, overlay, crop))
        labels.extend((
            f"ORIGINAL {row['filename']}",
            f"COMBINED {row['filename']}",
            f"CROP {row['filename']}",
        ))
    make_sheet(
        paths, SHEET_DIR / "method_comparison_contact_sheet.jpg", labels,
        cell_size=(350, 300),
    )


def write_review_files(rows):
    review_csv = REVIEW_DIR / "manual_review_annotations.csv"
    fields = [
        "class", "filename", "source_path", "overlay", "candidate_crop",
        "combined_score", "manual_status", "corner_1", "corner_2",
        "corner_3", "corner_4", "reviewer_note",
    ]
    with review_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "class": row["class"],
                "filename": row["filename"],
                "source_path": row["path"],
                "overlay": row.get("overlay", ""),
                "candidate_crop": row.get("candidate_crop", ""),
                "combined_score": row.get("combined_score", ""),
                "manual_status": "",
                "corner_1": "",
                "corner_2": "",
                "corner_3": "",
                "corner_4": "",
                "reviewer_note": "",
            })
    (REVIEW_DIR / "README.md").write_text(
        "# Manual review\n\n"
        "Review the combined overlays and fill "
        "`manual_review_annotations.csv` only with independently verified "
        "card corners. Suggested `manual_status` values are `correct`, "
        "`incorrect`, or `uncertain`. Empty fields mean no manual review has "
        "been supplied; this experiment does not claim visual verification.\n",
        encoding="utf-8",
    )


def write_report(image_rows, method_rows):
    lines = [
        "# Visual Localization Experiment v1",
        "",
        "This isolated experiment evaluates visual-only localization on the "
        "54 boundary-category failures. Production files and thresholds were "
        "not modified.",
        "",
        "## Important limitation",
        "",
        "No independent corner annotations were supplied. Experimental "
        "quadrilaterals are therefore candidates, not verified card "
        "boundaries. `strong` and `possible` describe the ranking heuristics "
        "only. Visual correctness is `N/A` until the manual review CSV is "
        "completed.",
        "",
        "## Method comparison",
        "",
        "| Method | Candidate images | Strong | Possible | Extractor-compatible | "
        "Mean time (ms) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in method_rows:
        lines.append(
            f"| {row['method']} | {row['candidate_images']} | "
            f"{row['strong_candidates']} | {row['possible_candidates']} | "
            f"{row['extractor_compatible']} | {row['mean_processing_ms']} |"
        )
    lines.extend([
        "",
        "Visually verified correct boundaries: **N/A**. Background false "
        "positives: **N/A** until manual review is supplied.",
        "",
        "## Combined method interpretation",
        "",
        "The combined method searches multiple scales, contrast variants, "
        "edge maps, and contour approximations, then ranks candidates using "
        "geometry, edge continuity, border contrast, and a capped area term. "
        "It does not use class identity to accept a boundary.",
        "",
        "The existing extractor test is separate from geometric correctness. "
        "A passing 2,304-value vector means only that the unchanged production "
        "preprocessing path accepted the experimental crop.",
        "",
        "## Outputs",
        "",
        "- `visual_localization_results.csv`: one row per image and method.",
        "- `method_comparison.csv`: aggregate method comparison.",
        "- `detection_overlays/`: top combined candidates, color-coded by "
        "heuristic category.",
        "- `corrected_candidate_crops/`: crops from the combined top candidate.",
        "- `contact_sheets/`: crop and method-comparison sheets.",
        "- `manual_review/`: annotation template and instructions.",
        "",
        "## Recommendation",
        "",
        "Do not promote this detector or lower production thresholds from "
        "candidate counts alone. The next development stage should manually "
        "annotate the 54 images, calculate true/false boundary rates, and "
        "then tune the ranking weights against those annotations. If "
        "multi-scale candidates are visually correct, implement only the "
        "smallest validated candidate-generation change and re-test false "
        "accepts.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    for directory in (OVERLAY_DIR, CROP_DIR, SHEET_DIR, REVIEW_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    rows = load_test_rows()
    if len(rows) != 54:
        raise RuntimeError(f"expected 54 boundary failures, found {len(rows)}")
    pygame.init()
    image_results = []
    source_paths, overlay_paths, crop_paths, sheet_rows = [], [], [], []
    try:
        for image_row in rows:
            surface = preprocess.load_image(image_row["path"])
            if surface is None:
                raise RuntimeError(f"could not decode {image_row['path']}")
            per_method = {}
            for method in METHODS:
                per_method[method] = result_for_method(surface, method)
            combined = per_method["combined"]
            overlay = draw_overlay(surface, image_row, combined)
            top = combined.get("top")
            crop_path = ""
            extractor_passed = False
            feature_length = 0
            extractor_ms = 0.0
            if top is not None:
                crop, extractor_passed, feature_length, extractor_ms = (
                    run_extractor(surface, top["points"])
                )
                crop_path = CROP_DIR / image_row["filename"]
                pygame.image.save(crop, str(crop_path))
            source_paths.append(Path(image_row["path"]))
            overlay_paths.append(overlay)
            crop_paths.append(crop_path or overlay)
            sheet_rows.append(image_row)
            for method, result in per_method.items():
                top_method = result.get("top")
                metrics = top_method["metrics"] if top_method else {}
                image_results.append({
                    "class": image_row["class"],
                    "filename": image_row["filename"],
                    "source_path": image_row["path"],
                    "method": method,
                    "candidate_count": result["candidate_count"],
                    "candidate_images": bool(top_method),
                    "rank_category": metrics.get("rank_category", ""),
                    "geometry_score": metrics.get("geometry_score", ""),
                    "edge_score": metrics.get("edge_score", ""),
                    "contrast_score": metrics.get("contrast_score", ""),
                    "overall_score": metrics.get("overall_score", ""),
                    "area_ratio": metrics.get("area_ratio", ""),
                    "aspect_ratio": metrics.get("aspect_ratio", ""),
                    "rotation_deg": metrics.get("rotation_deg", ""),
                    "corner_angle_min_deg": metrics.get("corner_angle_min_deg", ""),
                    "corner_angle_max_deg": metrics.get("corner_angle_max_deg", ""),
                    "opposite_side_ratio": metrics.get("opposite_side_ratio", ""),
                    "edge_continuity_min": metrics.get("edge_continuity_min", ""),
                    "edge_contrast_min": metrics.get("edge_contrast_min", ""),
                    "extractor_passed": (
                        extractor_passed if method == "combined" else ""
                    ),
                    "feature_length": feature_length if method == "combined" else "",
                    "processing_ms": result["processing_ms"],
                    "status": result["status"],
                    "failure_reason": result["reason"],
                    "visual_verification": "N/A",
                    "overlay": str(overlay),
                    "candidate_crop": str(crop_path),
                })
        fields = sorted({key for row in image_results for key in row})
        with RESULTS_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(image_results)
        aggregate = []
        for method in METHODS:
            selected = [row for row in image_results if row["method"] == method]
            aggregate.append({
                "method": method,
                "candidate_images": sum(bool(row["candidate_images"]) for row in selected),
                "strong_candidates": sum(row["rank_category"] == "strong" for row in selected),
                "possible_candidates": sum(row["rank_category"] == "possible" for row in selected),
                "extractor_compatible": sum(
                    row["extractor_passed"] == "True" for row in selected
                ),
                "mean_processing_ms": round(
                    sum(float(row["processing_ms"]) for row in selected)
                    / max(len(selected), 1), 2
                ),
                "visually_verified": "N/A",
                "background_false_positives": "N/A",
            })
        with COMPARISON_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=aggregate[0])
            writer.writeheader()
            writer.writerows(aggregate)
        make_sheet(
            crop_paths, SHEET_DIR / "corrected_candidate_crops_contact_sheet.jpg",
            [f"{row['filename']} score={next((x['overall_score'] for x in image_results if x['filename'] == row['filename'] and x['method'] == 'combined'), 'N/A')}" for row in sheet_rows],
        )
        make_comparison_sheet(source_paths, overlay_paths, crop_paths, sheet_rows)
        review_rows = []
        for row in sheet_rows:
            combined = next(
                item for item in image_results
                if item["filename"] == row["filename"]
                and item["method"] == "combined"
            )
            review_rows.append({
                **row,
                "overlay": combined["overlay"],
                "candidate_crop": combined["candidate_crop"],
                "combined_score": combined["overall_score"],
            })
        write_review_files(review_rows)
        write_report(review_rows, aggregate)
        print(f"images={len(rows)}")
        print(f"result_rows={len(image_results)}")
        print(f"results={RESULTS_CSV}")
        print(f"comparison={COMPARISON_CSV}")
        print(f"report={REPORT}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
