"""Measure the 54 boundary-category failures without changing production code.

The production detector does not retain coordinates for failed detections.
This script therefore runs a deliberately permissive, isolated candidate
search. Its geometry and crop results are proxies for manual correction, not
ground-truth annotations. The unchanged cardscan.features.extract() function
is used for the extractor check.
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cardscan.features as features
import cardscan.preprocess as preprocess


ROOT = Path(__file__).resolve().parent
INPUT_CSV = ROOT / "rejected_images_audit.csv"
OUTPUT_CSV = ROOT / "boundary_failures_deep_audit.csv"
OVERLAY_DIR = ROOT / "boundary_failure_overlays"
CROP_DIR = ROOT / "boundary_failure_corrected_crops"
CONTACT_SHEET = ROOT / "boundary_failures_deep_contact_sheet.jpg"
REPORT = ROOT / "BOUNDARY_FAILURE_DEEP_AUDIT_REPORT.md"

DETECT_MAX = preprocess.DETECT_MAX_DIMENSION
CARD_ASPECT = preprocess.CARD_ASPECT
CANVAS = (preprocess.CANVAS_W, preprocess.CANVAS_H)


def font(size):
    for path in ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def order_points(points):
    rect = np.zeros((4, 2), dtype=np.float32)
    sums = points.sum(axis=1)
    rect[0] = points[np.argmin(sums)]
    rect[2] = points[np.argmax(sums)]
    diffs = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diffs)]
    rect[3] = points[np.argmax(diffs)]
    return rect


def edge_support(gray, points):
    edges = cv2.Canny(gray, 50, 150)
    height, width = gray.shape[:2]
    values = []
    for start, end in zip(points, np.roll(points, -1, axis=0)):
        length = max(int(np.linalg.norm(end - start)), 2)
        xs = np.rint(np.linspace(start[0], end[0], length)).astype(int)
        ys = np.rint(np.linspace(start[1], end[1], length)).astype(int)
        good = 0
        for x, y in zip(xs, ys):
            x0, x1 = max(0, x - 3), min(width, x + 4)
            y0, y1 = max(0, y - 3), min(height, y + 4)
            good += int(edges[y0:y1, x0:x1].any())
        values.append(good / float(length))
    return values


def geometry(gray, points):
    height, width = gray.shape[:2]
    rect = order_points(points)
    area = abs(cv2.contourArea(rect))
    sides = [
        np.linalg.norm(rect[1] - rect[0]),
        np.linalg.norm(rect[2] - rect[1]),
        np.linalg.norm(rect[2] - rect[3]),
        np.linalg.norm(rect[3] - rect[0]),
    ]
    horizontal = (sides[0] + sides[2]) / 2.0
    vertical = (sides[1] + sides[3]) / 2.0
    aspect = min(horizontal, vertical) / max(horizontal, vertical, 1.0)
    top_angle = math.degrees(math.atan2(
        rect[1][1] - rect[0][1], rect[1][0] - rect[0][0]
    ))
    bottom_angle = math.degrees(math.atan2(
        rect[2][1] - rect[3][1], rect[2][0] - rect[3][0]
    ))
    left_angle = math.degrees(math.atan2(
        rect[3][1] - rect[0][1], rect[3][0] - rect[0][0]
    ))
    right_angle = math.degrees(math.atan2(
        rect[2][1] - rect[1][1], rect[2][0] - rect[1][0]
    ))
    support = edge_support(gray, rect)
    return {
        "area_ratio": float(area / (width * height)),
        "width_ratio": float(horizontal / width),
        "height_ratio": float(vertical / height),
        "aspect_ratio": float(aspect),
        "rotation_deg": float(top_angle),
        "top_bottom_angle_delta_deg": float(abs(top_angle - bottom_angle)),
        "left_right_angle_delta_deg": float(abs(left_angle - right_angle)),
        "opposite_side_ratio": float(min(
            sides[0] / max(sides[2], 1.0), sides[2] / max(sides[0], 1.0),
            sides[1] / max(sides[3], 1.0), sides[3] / max(sides[1], 1.0),
        )),
        "corner_angle_min_deg": float(min_corner_angle(rect)),
        "corner_angle_max_deg": float(max_corner_angle(rect)),
        "edge_support_min": float(min(support)),
        "edge_support_mean": float(sum(support) / len(support)),
    }


def corner_angles(rect):
    values = []
    for index in range(4):
        before = rect[(index - 1) % 4] - rect[index]
        after = rect[(index + 1) % 4] - rect[index]
        cosine = np.dot(before, after) / max(
            np.linalg.norm(before) * np.linalg.norm(after), 1.0
        )
        values.append(math.degrees(math.acos(np.clip(cosine, -1.0, 1.0))))
    return values


def min_corner_angle(rect):
    return min(corner_angles(rect))


def max_corner_angle(rect):
    return max(corner_angles(rect))


def candidate_quads(gray):
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    masks = []
    edges = cv2.Canny(blurred, 30, 180)
    masks.append(cv2.morphologyEx(
        edges, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=2
    ))
    for threshold in (80, 110, 140, 170, 200):
        _, mask = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
        masks.append(cv2.morphologyEx(
            mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8), iterations=2
        ))
    image_area = gray.shape[0] * gray.shape[1]
    results = []
    for mask in masks:
        contours, _ = cv2.findContours(
            mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 0.001 * image_area or area > 0.92 * image_area:
                continue
            perimeter = cv2.arcLength(contour, True)
            for epsilon_ratio in (0.01, 0.02, 0.04, 0.07):
                approx = cv2.approxPolyDP(
                    contour, epsilon_ratio * perimeter, True
                )
                if len(approx) != 4 or not cv2.isContourConvex(approx):
                    continue
                points = order_points(
                    approx.reshape(4, 2).astype(np.float32)
                )
                metrics = geometry(gray, points)
                aspect_distance = abs(metrics["aspect_ratio"] - CARD_ASPECT)
                score = (
                    0.45 * min(metrics["area_ratio"] / 0.30, 1.0)
                    + 0.25 * max(0.0, 1.0 - aspect_distance / CARD_ASPECT)
                    + 0.15 * metrics["opposite_side_ratio"]
                    + 0.15 * metrics["edge_support_min"]
                )
                results.append((score, points, metrics))
    unique = {}
    for score, points, metrics in results:
        key = tuple(np.rint(points).astype(int).reshape(-1))
        if key not in unique or score > unique[key][0]:
            unique[key] = (score, points, metrics)
    return sorted(unique.values(), key=lambda item: item[0], reverse=True)


def local_contrast(gray, points):
    """Estimate card/background contrast from narrow bands around each edge."""
    rect = order_points(points)
    values = []
    height, width = gray.shape[:2]
    for index, (start, end) in enumerate(
        zip(rect, np.roll(rect, -1, axis=0))
    ):
        edge = end - start
        length = max(int(np.linalg.norm(edge)), 2)
        tangent = edge / max(np.linalg.norm(edge), 1.0)
        normal = np.array([-tangent[1], tangent[0]])
        center = (start + end) / 2.0
        toward_center = rect.mean(axis=0) - center
        if np.dot(normal, toward_center) < 0:
            normal = -normal
        samples = []
        for distance in (4, 10):
            inside = np.rint(center + normal * distance).astype(int)
            outside = np.rint(center - normal * distance).astype(int)
            inside = np.clip(inside, [0, 0], [width - 1, height - 1])
            outside = np.clip(outside, [0, 0], [width - 1, height - 1])
            samples.append(abs(
                float(gray[inside[1], inside[0]])
                - float(gray[outside[1], outside[0]])
            ))
        values.append(sum(samples) / len(samples))
    return values


def warp_with_padding(surface, points):
    """Make a perspective-correct crop with a small border for re-detection."""
    rect = order_points(points)
    width = max(
        np.linalg.norm(rect[1] - rect[0]),
        np.linalg.norm(rect[2] - rect[3]),
    )
    height = max(
        np.linalg.norm(rect[3] - rect[0]),
        np.linalg.norm(rect[2] - rect[1]),
    )
    pad_x = max(4.0, width * 0.05)
    pad_y = max(4.0, height * 0.05)
    src = np.array([
        rect[0] - [pad_x, pad_y],
        rect[1] + [pad_x, -pad_y],
        rect[2] + [pad_x, pad_y],
        rect[3] + [-pad_x, pad_y],
    ], dtype=np.float32)
    out_w = max(32, int(width + 2 * pad_x))
    out_h = max(32, int(height + 2 * pad_y))
    src_surface = preprocess._surface_to_array(surface)
    dst = np.array([
        [0, 0], [out_w - 1, 0],
        [out_w - 1, out_h - 1], [0, out_h - 1],
    ], dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(src, dst)
    array = cv2.warpPerspective(src_surface, matrix, (out_w, out_h))
    return preprocess._array_to_surface(array)


def process(row):
    path = Path(row["path"])
    source = preprocess.load_image(str(path))
    if source is None:
        return {**row, "proxy_status": "decode_failed"}
    width, height = source.get_size()
    scale = min(1.0, DETECT_MAX / max(width, height))
    detection_surface = source
    if scale < 1.0:
        detection_surface = pygame.transform.smoothscale(
            source, (max(2, int(width * scale)), max(2, int(height * scale)))
        )
    array = preprocess._surface_to_array(detection_surface)
    gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    candidates = candidate_quads(gray)
    if not candidates:
        return {
            **row, "proxy_status": "no_proxy_quad",
            "candidate_count": 0,
        }
    _, points, metrics = candidates[0]
    points = points / scale
    full_gray = cv2.cvtColor(
        preprocess._surface_to_array(source), cv2.COLOR_RGB2GRAY
    )
    metrics = geometry(full_gray, points)
    contrast = local_contrast(full_gray, points)
    metrics["edge_contrast_mean"] = float(sum(contrast) / len(contrast))
    metrics["edge_contrast_min"] = float(min(contrast))
    metrics["corner_identifiability"] = (
        "strong" if metrics["edge_support_min"] >= 0.15
        and metrics["edge_contrast_min"] >= 8.0
        else "weak"
    )
    overlay = cv2.cvtColor(full_gray, cv2.COLOR_GRAY2RGB)
    cv2.polylines(overlay, [np.rint(points).astype(np.int32)], True,
                  (255, 0, 0), max(2, width // 500))
    for index, point in enumerate(points):
        x, y = np.rint(point).astype(int)
        cv2.circle(overlay, (x, y), max(4, width // 150), (0, 255, 0), -1)
        cv2.putText(overlay, str(index + 1), (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    overlay_path = OVERLAY_DIR / path.name
    cv2.imwrite(str(overlay_path), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
    corrected = warp_with_padding(source, points)
    crop_path = CROP_DIR / path.name
    pygame.image.save(corrected, str(crop_path))
    started = time.perf_counter()
    vector = features.extract(corrected)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    proxy_metrics = {
        f"proxy_{key}": value for key, value in metrics.items()
    }
    return {
        **row,
        **proxy_metrics,
        "proxy_status": "proxy_quad",
        "candidate_count": len(candidates),
        "corrected_crop": str(crop_path),
        "overlay": str(overlay_path),
        "extractor_passed": bool(vector is not None),
        "feature_length": len(vector) if vector is not None else 0,
        "extractor_ms": elapsed_ms,
    }


def make_contact_sheet(rows):
    columns = 4
    cell_w, cell_h = 420, 350
    sheet = Image.new(
        "RGB", (columns * cell_w, math.ceil(len(rows) / columns) * cell_h),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    title = font(15)
    small = font(13)
    for index, row in enumerate(rows):
        x = (index % columns) * cell_w
        y = (index // columns) * cell_h
        try:
            image = Image.open(row["overlay"]).convert("RGB")
            image.thumbnail((400, 290))
            sheet.paste(image, (x + (cell_w - image.width) // 2, y + 22))
        except (KeyError, OSError, ValueError):
            draw.text((x + 15, y + 120), "NO PROXY QUAD", fill="red",
                      font=title)
        label = f"{row['class']} | {row['filename'][:32]}"
        draw.text((x + 8, y + 4), label, fill="black", font=title)
        draw.multiline_text(
            (x + 8, y + 310),
            f"size={row.get('proxy_area_ratio', '')}  "
            f"rot={row.get('proxy_rotation_deg', '')}\n"
            f"corner={row.get('proxy_corner_identifiability', '')}  "
            f"extract={row.get('extractor_passed', '')}",
            fill="darkred", font=small, spacing=2,
        )
    sheet.save(CONTACT_SHEET, quality=90)


def write_report(rows):
    proxy = [row for row in rows if row.get("proxy_status") == "proxy_quad"]
    passed = [row for row in proxy if row.get("extractor_passed")]
    strong = [row for row in proxy
              if row.get("proxy_corner_identifiability") == "strong"]
    def mean(key):
        values = [
            float(row[key]) for row in proxy
            if row.get(key) not in ("", None)
        ]
        return sum(values) / len(values) if values else 0.0
    lines = [
        "# Deep Boundary-Failure Audit",
        "",
        "This is an isolated analysis of the 54 images manually categorized as",
        "boundary failures. Production preprocessing and feature extraction were",
        "not changed.",
        "",
        "## Important measurement limitation",
        "",
        "The original detector does not retain failed corner coordinates. This",
        "audit uses a more permissive contour search to obtain the best available",
        "quadrilateral proxy. These are not independent ground-truth corners and",
        "the corrected crops are not manual annotations. They estimate the upper",
        "bound of what a corrected crop might achieve. The overlay contact sheet",
        "must be reviewed before treating any candidate as a true card boundary.",
        "",
        "## Aggregate results",
        "",
        f"- Boundary-category images: **{len(rows)}**",
        f"- Images with a proxy quadrilateral: **{len(proxy)}/{len(rows)}** "
        f"({100 * len(proxy) / max(len(rows), 1):.1f}%)",
        f"- Proxy crops passing unchanged `features.extract()`: "
        f"**{len(passed)}/{len(proxy)}** "
        f"({100 * len(passed) / max(len(proxy), 1):.1f}%)",
        f"- Strong corner-identifiability proxy: **{len(strong)}/{len(proxy)}** "
        f"({100 * len(strong) / max(len(proxy), 1):.1f}%)",
        "",
        "## Proxy geometry measurements",
        "",
        f"- Mean proxy card area ratio: **{mean('proxy_area_ratio'):.3f}**",
        f"- Mean proxy card width ratio: **{mean('proxy_width_ratio'):.3f}**",
        f"- Mean proxy card height ratio: **{mean('proxy_height_ratio'):.3f}**",
        f"- Mean absolute proxy rotation: "
        f"**{mean_abs(rows, 'proxy_rotation_deg'):.1f}°**",
        f"- Mean proxy opposite-side ratio: "
        f"**{mean('proxy_opposite_side_ratio'):.3f}**",
        f"- Mean proxy edge contrast: "
        f"**{mean('proxy_edge_contrast_mean'):.1f} grayscale levels**",
        "",
        "The rotation, perspective, contrast, and corner values are available",
        "per image in the CSV. Rotation is the top-edge angle after consistent",
        "corner ordering; opposite-side ratio is a perspective/shape proxy.",
        "",
        "## Extractor test",
        "",
        "Each proxy quadrilateral was warped into a card-shaped crop with a 5%",
        "border and passed to the unchanged `cardscan.features.extract()`.",
        "A pass means the existing preprocessing detector found a boundary in",
        "that corrected crop and returned the normal feature vector. It does not",
        "prove that the proxy boundary was the true card boundary.",
        "",
        "## Files",
        "",
        f"- [Per-image CSV]({OUTPUT_CSV.name})",
        f"- [Overlay contact sheet]({CONTACT_SHEET.name})",
        f"- Corrected crop directory: `{CROP_DIR.name}/`",
        f"- Overlay directory: `{OVERLAY_DIR.name}/`",
        "",
        "## Decision guidance",
        "",
        "Use the overlay sheet to separate true-card proxies from background",
        "rectangles. If a substantial number of true-card proxies pass the",
        "extractor, the highest-value next experiment is conservative multi-scale",
        "candidate generation plus independent content validation. Do not lower",
        "the production area or recognition thresholds based on this proxy audit.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def mean_abs(rows, key):
    values = [
        abs(float(row[key])) for row in rows
        if row.get(key) not in ("", None)
    ]
    return sum(values) / len(values) if values else 0.0


def main():
    OVERLAY_DIR.mkdir(exist_ok=True)
    CROP_DIR.mkdir(exist_ok=True)
    with INPUT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        source_rows = list(csv.DictReader(handle))
    rows = [
        row for row in source_rows
        if row.get("primary_category") == "Boundary Detection Failure"
    ]
    pygame.init()
    try:
        output = [process(row) for row in rows]
        fields = sorted({key for row in output for key in row})
        with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(output)
        make_contact_sheet(output)
        write_report(output)
        print(f"boundary_failures={len(output)}")
        print(f"proxy_quads={sum(r.get('proxy_status') == 'proxy_quad' for r in output)}")
        print(f"extractor_passes={sum(bool(r.get('extractor_passed')) for r in output)}")
        print(f"csv={OUTPUT_CSV}")
        print(f"report={REPORT}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
