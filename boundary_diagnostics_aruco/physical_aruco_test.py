"""Process user-supplied physical ArUco prototype photographs.

This script is isolated from cardscan production code. It accepts photographs
from a directory, validates the four configured marker IDs, estimates the
outer card by a calibrated marker-layout homography, and fails closed.
"""

import argparse
import csv
import json
import math
import time
from pathlib import Path

import cv2
import numpy as np


# ── Physical layout configuration ───────────────────────────
# These values must match the print-ready prototype.
DICT_NAME = "DICT_4X4_50"
EXPECTED_IDS = (0, 1, 2, 3)
CARD_WIDTH_MM = 63.0
CARD_HEIGHT_MM = 88.2
MARKER_SIZE_MM = 10.0
QUIET_ZONE_MM = 2.0
MARKER_INSET_MM = 4.0
OUTPUT_SIZE = (120, 168)
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "physical_results"


def get_dictionary():
    return cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, DICT_NAME))


def get_detector():
    return cv2.aruco.ArucoDetector(
        get_dictionary(), cv2.aruco.DetectorParameters()
    )


def marker_positions_mm():
    inset = MARKER_INSET_MM + QUIET_ZONE_MM
    right = CARD_WIDTH_MM - inset - MARKER_SIZE_MM
    bottom = CARD_HEIGHT_MM - inset - MARKER_SIZE_MM
    return {
        0: (inset, inset),
        1: (right, inset),
        2: (inset, bottom),
        3: (right, bottom),
    }


def order_corners(points):
    points = np.asarray(points, dtype=np.float32)
    total = points.sum(axis=1)
    difference = np.diff(points, axis=1).ravel()
    return np.array([
        points[np.argmin(total)],
        points[np.argmin(difference)],
        points[np.argmax(total)],
        points[np.argmax(difference)],
    ], dtype=np.float32)


def layout_homography(corners_by_id):
    source = []
    target = []
    for marker_id in EXPECTED_IDS:
        x, y = marker_positions_mm()[marker_id]
        source.extend([
            (x, y),
            (x + MARKER_SIZE_MM, y),
            (x + MARKER_SIZE_MM, y + MARKER_SIZE_MM),
            (x, y + MARKER_SIZE_MM),
        ])
        target.extend(corners_by_id[marker_id])
    return cv2.findHomography(
        np.float32(source), np.float32(target), method=0
    )[0]


def estimate_outer_corners(corners_by_id):
    homography = layout_homography(corners_by_id)
    if homography is None:
        raise ValueError("could not calculate marker-layout homography")
    card_mm = np.float32([
        [0, 0],
        [CARD_WIDTH_MM, 0],
        [CARD_WIDTH_MM, CARD_HEIGHT_MM],
        [0, CARD_HEIGHT_MM],
    ])
    return cv2.perspectiveTransform(
        card_mm.reshape(1, -1, 2), homography
    ).reshape(-1, 2)


def validate_boundary(corners, image_shape):
    height, width = image_shape[:2]
    ordered = order_corners(corners)
    if not cv2.isContourConvex(ordered.reshape(-1, 1, 2)):
        return False, "estimated boundary is not convex"
    area = abs(cv2.contourArea(ordered))
    if area < 0.01 * width * height:
        return False, "estimated boundary is too small"
    if not np.all(np.isfinite(ordered)):
        return False, "estimated boundary contains invalid coordinates"
    inside = (
        (ordered[:, 0] >= -0.05 * width)
        & (ordered[:, 0] <= 1.05 * width)
        & (ordered[:, 1] >= -0.05 * height)
        & (ordered[:, 1] <= 1.05 * height)
    )
    if not np.all(inside):
        return False, "estimated boundary is outside the image"
    top = np.linalg.norm(ordered[1] - ordered[0])
    bottom = np.linalg.norm(ordered[2] - ordered[3])
    left = np.linalg.norm(ordered[3] - ordered[0])
    right = np.linalg.norm(ordered[2] - ordered[1])
    if min(top, bottom, left, right) < 10:
        return False, "estimated boundary has a degenerate side"
    return True, ""


def load_ground_truth(input_dir):
    path = input_dir / "ground_truth.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return {
        name: np.float32(points)
        for name, points in data.items()
    }


def error_metrics(estimated, ground_truth):
    if ground_truth is None:
        return {"mean_corner_error_px": "", "max_corner_error_px": "",
                "normalized_mean_error": "", "per_corner_error_px": ""}
    expected = order_corners(ground_truth)
    actual = order_corners(estimated)
    errors = np.linalg.norm(actual - expected, axis=1)
    scale = math.sqrt(CARD_WIDTH_MM ** 2 + CARD_HEIGHT_MM ** 2)
    return {
        "mean_corner_error_px": f"{float(errors.mean()):.4f}",
        "max_corner_error_px": f"{float(errors.max()):.4f}",
        "normalized_mean_error": f"{float(errors.mean() / scale):.6f}",
        "per_corner_error_px": ",".join(f"{float(x):.4f}" for x in errors),
    }


def condition_for(path, input_dir, override):
    if override:
        return override
    relative = path.parent.relative_to(input_dir)
    return relative.parts[0] if relative.parts else "unlabeled"


def process_image(path, input_dir, output_dir, override, ground_truth):
    started = time.perf_counter()
    image = cv2.imread(str(path))
    result = {
        "filename": path.name,
        "relative_path": str(path.relative_to(input_dir)),
        "condition": condition_for(path, input_dir, override),
        "detected_ids": "",
        "expected_markers_detected": 0,
        "all_four_expected_markers": False,
        "boundary_success": False,
        "perspective_success": False,
        "processing_ms": "",
        "failure_reason": "",
        "mean_corner_error_px": "",
        "max_corner_error_px": "",
        "normalized_mean_error": "",
        "per_corner_error_px": "",
        "visualization_path": "",
        "corrected_crop_path": "",
    }
    if image is None:
        result["failure_reason"] = "image could not be read"
        result["processing_ms"] = f"{(time.perf_counter() - started) * 1000:.2f}"
        return result

    corners, ids, _ = get_detector().detectMarkers(image)
    detected_ids = [] if ids is None else [int(value) for value in ids.ravel()]
    result["detected_ids"] = ",".join(str(value) for value in sorted(detected_ids))
    result["expected_markers_detected"] = sum(
        marker_id in detected_ids for marker_id in EXPECTED_IDS
    )
    if set(detected_ids) != set(EXPECTED_IDS):
        result["failure_reason"] = (
            "expected exactly IDs 0,1,2,3; "
            f"detected {result['detected_ids'] or 'none'}"
        )
        visualization = image.copy()
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(visualization, corners, ids)
        visual_path = output_dir / "visualizations" / f"{path.stem}.jpg"
        cv2.imwrite(str(visual_path), visualization)
        result["visualization_path"] = str(visual_path)
        result["processing_ms"] = f"{(time.perf_counter() - started) * 1000:.2f}"
        return result

    result["all_four_expected_markers"] = True
    corners_by_id = {
        int(marker_id): marker_corners.reshape(4, 2)
        for marker_id, marker_corners in zip(ids.ravel(), corners)
    }
    try:
        outer = estimate_outer_corners(corners_by_id)
        valid, reason = validate_boundary(outer, image.shape)
        if not valid:
            result["failure_reason"] = reason
        else:
            result["boundary_success"] = True
            crop = cv2.warpPerspective(
                image,
                cv2.getPerspectiveTransform(
                    order_corners(outer),
                    np.float32([[0, 0], [OUTPUT_SIZE[0] - 1, 0],
                                [OUTPUT_SIZE[0] - 1, OUTPUT_SIZE[1] - 1],
                                [0, OUTPUT_SIZE[1] - 1]]),
                ),
                OUTPUT_SIZE,
            )
            crop_path = output_dir / "corrected_cards" / f"{path.stem}.png"
            cv2.imwrite(str(crop_path), crop)
            result["corrected_crop_path"] = str(crop_path)
            result["perspective_success"] = True
            result.update(error_metrics(outer, ground_truth.get(path.name)))
    except (TypeError, ValueError, cv2.error) as error:
        result["failure_reason"] = str(error)

    visualization = image.copy()
    cv2.aruco.drawDetectedMarkers(visualization, corners, ids)
    if result["boundary_success"]:
        cv2.polylines(visualization, [np.int32(order_corners(outer))], True,
                      (0, 220, 0), 5)
    visual_path = output_dir / "visualizations" / f"{path.stem}.jpg"
    cv2.imwrite(str(visual_path), visualization)
    result["visualization_path"] = str(visual_path)
    result["processing_ms"] = f"{(time.perf_counter() - started) * 1000:.2f}"
    return result


def write_contact_sheet(rows, output):
    images = []
    for row in rows:
        image = cv2.imread(row["visualization_path"])
        if image is None:
            continue
        image = cv2.resize(image, (320, 240))
        color = (0, 170, 0) if row["perspective_success"] else (0, 0, 220)
        label = f"{row['filename']} | {row['condition']}"
        cv2.putText(image, label[:48], (5, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.45, color, 1, cv2.LINE_AA)
        cv2.putText(image, row["failure_reason"][:48], (5, 235),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, color, 1, cv2.LINE_AA)
        images.append(image)
    if not images:
        canvas = np.full((240, 320, 3), 255, np.uint8)
        cv2.putText(canvas, "No photographs supplied", (25, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 180), 2)
    else:
        columns = 3
        rows_count = math.ceil(len(images) / columns)
        canvas = np.full((rows_count * 240, columns * 320, 3), 255, np.uint8)
        for index, image in enumerate(images):
            y = (index // columns) * 240
            x = (index % columns) * 320
            canvas[y:y + 240, x:x + 320] = image
    cv2.imwrite(str(output), canvas)


def write_report(rows, output, input_dir):
    total = len(rows)
    four = sum(row["all_four_expected_markers"] for row in rows)
    boundaries = sum(row["boundary_success"] for row in rows)
    warps = sum(row["perspective_success"] for row in rows)
    measured = [float(row["mean_corner_error_px"]) for row in rows
                if row["mean_corner_error_px"]]
    if total:
        summary = (
            f"Photographs processed: {total}\n\n"
            f"- All four expected markers: {four}/{total} "
            f"({four / total * 100:.1f}%)\n"
            f"- Boundary estimated: {boundaries}/{total} "
            f"({boundaries / total * 100:.1f}%)\n"
            f"- Perspective correction: {warps}/{total} "
            f"({warps / total * 100:.1f}%)\n"
        )
    else:
        summary = "No photographs supplied; real-world testing is pending.\n"
    if measured:
        summary += (
            f"- Mean measured corner error: {np.mean(measured):.3f} px\n"
            f"- Ground-truth rows: {len(measured)}\n"
        )
    else:
        summary += "- Independent ground-truth corner measurements: none\n"
    output.write_text(
        f"""# Physical ArUco Test Report

## Configuration

- Dictionary: `{DICT_NAME}`
- Expected IDs: `{EXPECTED_IDS}`
- Card layout: {CARD_WIDTH_MM:.1f} x {CARD_HEIGHT_MM:.1f} mm
- Marker: {MARKER_SIZE_MM:.1f} mm, with {QUIET_ZONE_MM:.1f} mm quiet zone
- Marker inset: {MARKER_INSET_MM + QUIET_ZONE_MM:.1f} mm to black square
- Output crop: {OUTPUT_SIZE[0]} x {OUTPUT_SIZE[1]} pixels
- Input directory: `{input_dir}`

## Results

{summary}
Four detected markers are not by themselves proof of correct localization.
The script also checks exact IDs, estimates the boundary from the calibrated
physical layout, validates the quadrilateral, and records corrected crops.

## Accuracy

Corner error is reported only when independent coordinates are supplied in
`ground_truth.json`. Detector-generated coordinates must not be used as
ground truth. If no such file is present, geometric accuracy remains
unmeasured.

## Review

Inspect the per-image visualizations, corrected cards, and
`physical_test_results.csv`. Review glare, blur, shadows, marker wear,
partial occlusion, false detections, and whether the four markers really
belong to the same physical card.
""",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path,
                        default=ROOT / "physical_photos")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--condition", default="")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "visualizations").mkdir(exist_ok=True)
    (args.output_dir / "corrected_cards").mkdir(exist_ok=True)
    input_dir = args.input_dir
    input_dir.mkdir(parents=True, exist_ok=True)
    ground_truth = load_ground_truth(input_dir)
    paths = sorted(
        path for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    rows = [
        process_image(path, input_dir, args.output_dir, args.condition,
                      ground_truth)
        for path in paths
    ]
    fields = list(rows[0]) if rows else [
        "filename", "relative_path", "condition", "detected_ids",
        "expected_markers_detected", "all_four_expected_markers",
        "boundary_success", "perspective_success", "processing_ms",
        "failure_reason", "mean_corner_error_px", "max_corner_error_px",
        "normalized_mean_error", "per_corner_error_px",
        "visualization_path", "corrected_crop_path",
    ]
    csv_path = args.output_dir / "physical_test_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    write_contact_sheet(rows, args.output_dir / "physical_test_contact_sheet.jpg")
    write_report(rows, args.output_dir / "PHYSICAL_TEST_REPORT.md",
                 input_dir)
    print(f"Processed {len(rows)} photographs")
    print(f"Results: {csv_path}")


if __name__ == "__main__":
    main()
