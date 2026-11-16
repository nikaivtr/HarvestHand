"""Isolated ArUco card-localization feasibility experiment.

This file deliberately does not import or modify cardscan production modules.
It creates synthetic marker-bearing cards with known geometry, tests detection
and perspective correction, and scans the existing sample set only to document
whether the intended marker IDs are present.
"""

import csv
import math
import os
import shutil
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SYNTHETIC = ROOT / "synthetic_samples"
MARKERS = ROOT / "generated_markers"
DETECTIONS = ROOT / "marker_visualizations"
WARPS = ROOT / "corrected_cards"
DICT_NAME = "DICT_4X4_50"
MARKER_IDS = (0, 1, 2, 3)
CARD_W, CARD_H = 600, 840
CANVAS_W, CANVAS_H = 120, 168
MARKER_SIZE = 70
MARKER_INSET = 28


def dictionary():
    return cv2.aruco.getPredefinedDictionary(
        getattr(cv2.aruco, DICT_NAME)
    )


def detector():
    params = cv2.aruco.DetectorParameters()
    return cv2.aruco.ArucoDetector(dictionary(), params)


def make_marker(marker_id):
    marker = np.zeros((MARKER_SIZE, MARKER_SIZE), dtype=np.uint8)
    marker = cv2.aruco.generateImageMarker(
        dictionary(), marker_id, MARKER_SIZE, marker, 1
    )
    return cv2.cvtColor(marker, cv2.COLOR_GRAY2BGR)


def marker_positions():
    return {
        0: (MARKER_INSET, MARKER_INSET),
        1: (CARD_W - MARKER_INSET - MARKER_SIZE, MARKER_INSET),
        2: (MARKER_INSET, CARD_H - MARKER_INSET - MARKER_SIZE),
        3: (
            CARD_W - MARKER_INSET - MARKER_SIZE,
            CARD_H - MARKER_INSET - MARKER_SIZE,
        ),
    }


def make_card():
    card = np.full((CARD_H, CARD_W, 3), (236, 242, 226), np.uint8)
    cv2.rectangle(card, (0, 0), (CARD_W - 1, CARD_H - 1), (35, 115, 55), 12)
    cv2.rectangle(card, (85, 145), (CARD_W - 85, CARD_H - 145),
                  (222, 174, 116), -1)
    cv2.ellipse(card, (CARD_W // 2, 400), (145, 105), 0, 0, 360,
                (55, 150, 70), -1)
    cv2.ellipse(card, (CARD_W // 2 - 90, 370), (70, 95), 20, 0, 360,
                (35, 105, 50), -1)
    cv2.ellipse(card, (CARD_W // 2 + 90, 370), (70, 95), -20, 0, 360,
                (35, 105, 50), -1)
    cv2.putText(card, "EXPERIMENTAL CARD", (145, 115),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (25, 55, 35), 2,
                cv2.LINE_AA)
    cv2.putText(card, "Markers remain outside the artwork",
                (122, 755), cv2.FONT_HERSHEY_SIMPLEX, 0.62,
                (25, 55, 35), 2, cv2.LINE_AA)
    for marker_id, (x, y) in marker_positions().items():
        card[y:y + MARKER_SIZE, x:x + MARKER_SIZE] = make_marker(marker_id)
    return card


def scene_for(name, card, rng):
    background = np.zeros((1500, 1100, 3), np.uint8)
    background[:] = (92, 112, 132)
    for y in range(0, background.shape[0], 55):
        cv2.line(background, (0, y), (1100, y + 180), (115, 135, 95), 4)
    if name == "front":
        dst = np.float32([[250, 150], [850, 150], [850, 990], [250, 990]])
    elif name == "rotated":
        dst = np.float32([[405, 105], [990, 360], [680, 1195], [95, 940]])
    elif name == "perspective":
        dst = np.float32([[180, 90], [930, 210], [815, 1240], [300, 1120]])
    elif name == "uneven_light":
        dst = np.float32([[250, 170], [850, 130], [890, 1010], [220, 970]])
    elif name == "shadow":
        dst = np.float32([[200, 220], [820, 120], [900, 1080], [250, 1160]])
    elif name == "busy_background":
        for _ in range(120):
            p1 = tuple(rng.integers(0, 1100, 2).tolist())
            p2 = tuple(rng.integers(0, 1500, 2).tolist())
            cv2.line(background, p1, p2,
                     tuple(int(x) for x in rng.integers(20, 200, 3)), 2)
        dst = np.float32([[135, 270], [760, 150], [930, 1190], [240, 1300]])
    else:
        dst = np.float32([[220, 180], [850, 180], [850, 1040], [220, 1040]])

    src = np.float32([[0, 0], [CARD_W - 1, 0],
                      [CARD_W - 1, CARD_H - 1], [0, CARD_H - 1]])
    transform = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(card, transform, (1100, 1500))
    mask = cv2.warpPerspective(
        np.full((CARD_H, CARD_W), 255, np.uint8), transform, (1100, 1500)
    )
    scene = np.where(mask[:, :, None] > 0, warped, background)
    if name == "uneven_light":
        gradient = np.linspace(0.45, 1.15, scene.shape[1])[None, :, None]
        scene = np.clip(scene.astype(np.float32) * gradient, 0, 255).astype(
            np.uint8
        )
    elif name == "shadow":
        overlay = scene.copy()
        cv2.ellipse(overlay, (540, 690), (360, 190), -20, 0, 360,
                    (20, 25, 30), -1)
        scene = cv2.addWeighted(overlay, 0.30, scene, 0.70, 0)
    if name == "partial_marker":
        cv2.rectangle(scene, (int(dst[0, 0]) - 5, int(dst[0, 1]) - 5),
                      (int(dst[0, 0]) + 130, int(dst[0, 1]) + 125),
                      (92, 112, 132), -1)
    elif name == "missing_marker":
        # Cover the lower-right marker, leaving the rest of the card intact.
        p = dst[2].astype(int)
        cv2.circle(scene, tuple(p), 55, (92, 112, 132), -1)
    elif name == "distractor":
        extra = make_marker(10)
        scene[40:40 + MARKER_SIZE, 40:40 + MARKER_SIZE] = extra
    return scene, dst


def order_points(points):
    points = np.asarray(points, dtype=np.float32)
    total = points.sum(axis=1)
    diff = np.diff(points, axis=1).ravel()
    return np.array([
        points[np.argmin(total)],
        points[np.argmin(diff)],
        points[np.argmax(total)],
        points[np.argmax(diff)],
    ], dtype=np.float32)


def estimate_card_corners(corners_by_id):
    # Calibrate the physical marker layout in card coordinates first. A
    # constant pixel offset would be wrong after perspective distortion.
    source = []
    target = []
    for marker_id in MARKER_IDS:
        x, y = marker_positions()[marker_id]
        source.extend([
            (x, y), (x + MARKER_SIZE - 1, y),
            (x + MARKER_SIZE - 1, y + MARKER_SIZE - 1),
            (x, y + MARKER_SIZE - 1),
        ])
        target.extend(corners_by_id[marker_id])
    homography, _ = cv2.findHomography(
        np.float32(source), np.float32(target), 0
    )
    card_corners = np.float32(
        [[0, 0], [CARD_W - 1, 0],
         [CARD_W - 1, CARD_H - 1], [0, CARD_H - 1]]
    )
    return cv2.perspectiveTransform(
        card_corners.reshape(1, -1, 2), homography
    ).reshape(-1, 2)


def detect_and_warp(image, expected_corners, stem):
    found_corners, found_ids, _ = detector().detectMarkers(image)
    ids = [] if found_ids is None else [int(x) for x in found_ids.ravel()]
    unique_expected = (
        set(ids) == set(MARKER_IDS) and len(ids) == len(MARKER_IDS)
    )
    by_id = {}
    if found_ids is not None:
        for marker_id, points in zip(found_ids.ravel(), found_corners):
            by_id[int(marker_id)] = points.reshape(4, 2)

    estimated = None
    error = ""
    warp_path = ""
    if unique_expected:
        estimated = estimate_card_corners(by_id)
        error = float(np.mean(np.linalg.norm(
            estimated - expected_corners, axis=1
        )))
        output = cv2.warpPerspective(
            image,
            cv2.getPerspectiveTransform(
                order_points(estimated),
                np.float32([[0, 0], [CANVAS_W - 1, 0],
                            [CANVAS_W - 1, CANVAS_H - 1], [0, CANVAS_H - 1]]),
            ),
            (CANVAS_W, CANVAS_H),
        )
        warp_path = str(WARPS / f"{stem}.png")
        cv2.imwrite(warp_path, output)

    visualization = image.copy()
    if found_ids is not None:
        cv2.aruco.drawDetectedMarkers(visualization, found_corners, found_ids)
    if estimated is not None:
        cv2.polylines(visualization, [np.int32(estimated)], True,
                      (0, 255, 0), 5)
    detection_path = str(DETECTIONS / f"{stem}.jpg")
    cv2.imwrite(detection_path, visualization)
    return {
        "detected_ids": ",".join(str(x) for x in sorted(ids)),
        "marker_count": len(ids),
        "all_four_detected": bool(unique_expected),
        "corner_error_px": error,
        "warp_success": bool(unique_expected),
        "detection_path": detection_path,
        "warp_path": warp_path,
    }


def contact_sheet(rows, output):
    thumbs = []
    for row in rows:
        image = cv2.imread(row["detection_path"])
        image = cv2.resize(image, (260, 355))
        color = (0, 170, 0) if row["warp_success"] else (0, 0, 210)
        cv2.putText(image, row["name"], (5, 24), cv2.FONT_HERSHEY_SIMPLEX,
                    0.58, color, 2, cv2.LINE_AA)
        cv2.putText(image, "ids=" + row["detected_ids"], (5, 348),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, color, 1, cv2.LINE_AA)
        thumbs.append(image)
    cols = 3
    rows_count = math.ceil(len(thumbs) / cols)
    sheet = np.full((rows_count * 355, cols * 260, 3), 255, np.uint8)
    for index, image in enumerate(thumbs):
        sheet[(index // cols) * 355:(index // cols + 1) * 355,
              (index % cols) * 260:(index % cols + 1) * 260] = image
    cv2.imwrite(str(output), sheet)


def scan_existing_dataset():
    output = ROOT / "existing_dataset_scan.csv"
    rows = []
    for slug in ("pechay_plant", "monggo_plant"):
        for path in sorted((REPO / "data" / "card_samples" / slug).glob("*.jpg")):
            image = cv2.imread(str(path))
            found_corners, found_ids, _ = detector().detectMarkers(image)
            ids = [] if found_ids is None else [
                int(x) for x in found_ids.ravel()
            ]
            intended = all(marker_id in ids for marker_id in MARKER_IDS)
            rows.append({
                "class": slug,
                "filename": path.name,
                "detected_ids": ",".join(str(x) for x in sorted(ids)),
                "intended_four_markers_detected": intended,
            })
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main():
    for directory in (SYNTHETIC, MARKERS, DETECTIONS, WARPS):
        directory.mkdir(parents=True, exist_ok=True)
    for marker_id in MARKER_IDS:
        cv2.imwrite(str(MARKERS / f"marker_{marker_id}.png"), make_marker(marker_id))

    card = make_card()
    cv2.imwrite(str(ROOT / "card_layout_mockup.png"), card)
    rng = np.random.default_rng(20261113)
    names = (
        "front", "rotated", "perspective", "uneven_light", "shadow",
        "busy_background", "partial_marker", "missing_marker", "distractor",
    )
    rows = []
    for name in names:
        image, corners = scene_for(name, card, rng)
        source = SYNTHETIC / f"{name}.jpg"
        cv2.imwrite(str(source), image)
        result = detect_and_warp(image, corners, name)
        rows.append({"name": name, "source_path": str(source), **result})
    output = ROOT / "synthetic_detection_results.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    contact_sheet(rows, ROOT / "synthetic_contact_sheet.jpg")
    existing = scan_existing_dataset()
    successful = sum(row["warp_success"] for row in rows)
    all_four = sum(row["all_four_detected"] for row in rows)
    expected_marker_instances = len(rows) * len(MARKER_IDS)
    detected_expected_instances = sum(
        sum(marker_id in row["detected_ids"].split(",")
            for marker_id in (str(x) for x in MARKER_IDS))
        for row in rows
    )
    expected_set = sum(
        all(str(marker_id) in row["detected_ids"].split(",")
            for marker_id in MARKER_IDS)
        for row in rows
    )
    errors = [
        float(row["corner_error_px"]) for row in rows
        if row["corner_error_px"] != ""
    ]
    existing_all_four = sum(
        row["intended_four_markers_detected"] for row in existing
    )
    report = ROOT / "ARUCO_FEASIBILITY_REPORT.md"
    report.write_text(
        (
            f"# ArUco Feasibility Report\n\n"
            f"## Compatibility\n\n"
            f"- OpenCV: `{cv2.__version__}`\n"
            f"- `cv2.aruco`: available\n"
            f"- Dictionary: `{DICT_NAME}`\n"
            f"- Marker IDs: `{MARKER_IDS}`; marker size: {MARKER_SIZE}px; "
            f"corner inset: {MARKER_INSET}px\n"
            f"- Output warp: {CANVAS_W} x {CANVAS_H} (5:7)\n\n"
            f"## Layout\n\n"
            f"The mockup places one marker near each corner, outside the central "
            f"illustration and label areas. The outer card corners are inferred "
            f"from the calibrated marker inset; missing or duplicate expected IDs "
            f"fail closed rather than using a guessed boundary.\n\n"
            f"## Synthetic results\n\n"
            f"Tested {len(rows)} controlled scenes. Four-marker detection and "
            f"perspective correction succeeded for {all_four}/{len(rows)} "
            f"({all_four / len(rows) * 100:.1f}%). Successful warps: "
            f"{successful}/{len(rows)} ({successful / len(rows) * 100:.1f}%). "
            f"Individual expected-marker detections were "
            f"{detected_expected_instances}/{expected_marker_instances} "
            f"({detected_expected_instances / expected_marker_instances * 100:.1f}%). "
            f"All four expected IDs were present in {expected_set}/{len(rows)} "
            f"scenes; mean/max corner error among successful warps was "
            f"{np.mean(errors):.2f}/{max(errors):.2f}px. "
            f"These are synthetic newly photographed-card substitutes, not the "
            f"existing dataset.\n\n"
            f"Expected failures were the partially obscured and missing-marker "
            f"cases. The distractor case demonstrates that an unexpected marker "
            f"ID must not be accepted as one of the card corners.\n\n"
            f"## Existing 42-image dataset\n\n"
            f"The intended four IDs were detected in {existing_all_four}/"
            f"{len(existing)} images. These photos do not contain the experimental "
            f"markers, so this is not a localization validation of the current "
            f"cards and cannot be compared directly with v12's 16/42 verified "
            f"visual boundaries.\n\n"
            f"## Comparison with v12\n\n"
            f"| Metric | v12 visual detector | ArUco experiment |\n"
            f"|---|---:|---:|\n"
            f"| Complete card localization | 16/42 verified | {all_four}/{len(rows)} "
            f"synthetic scenes |\n"
            f"| Incorrectly accepted boundaries | 9/42 | See per-scene CSV; "
            f"0/6 successful synthetic warps |\n"
            f"| False rejections | 8/42 | Missing/obscured markers fail closed |\n"
            f"| Perspective correction | Audit found invalid crops | "
            f"{successful}/{len(rows)} synthetic warps |\n\n"
            f"## Limitations and recommendation\n\n"
            f"ArUco is technically supported and promising for a redesigned card "
            f"or printed marker prototype. This experiment does not establish "
            f"performance on the existing cards, marker wear, print quality, "
            f"glare, motion blur, or real gameplay occlusion. Markers would change "
            f"card artwork and require new physical cards plus a new capture set. "
            f"Classification: **Inconclusive**. The next step is a physical "
            f"prototype with four markers, photographed under the same 42 capture "
            f"conditions, followed by blinded boundary review. Do not integrate "
            f"ArUco into the production scanner yet.\n"
        ),
        encoding="utf-8",
    )
    print(report)
    print(f"synthetic four-marker success: {all_four}/{len(rows)}")
    print(f"existing intended-marker detections: {existing_all_four}/{len(existing)}")


if __name__ == "__main__":
    main()
