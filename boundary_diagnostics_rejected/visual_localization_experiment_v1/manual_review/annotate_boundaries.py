"""Interactive manual card-boundary annotation tool.

Controls:
  Left click: add a corner in clockwise order.
  U: undo the last point.  C: clear all points.
  1: complete card visible.  2: partially obstructed.
  3: boundary unclear.  4: blurred/damaged.  5: no usable card.
  Space: preview the perspective crop from the four selected points.
  R: toggle the experimental candidate overlay reference. T: edit notes.
  S: save the current record.  N/P: next/previous image.  Q/Esc: quit.

Candidate overlays are references only and are never copied into annotations.
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np


MANUAL_DIR = Path(__file__).resolve().parent
EXPERIMENT = MANUAL_DIR.parent
RESULTS_CSV = EXPERIMENT / "visual_localization_results.csv"
ANNOTATIONS_JSON = MANUAL_DIR / "manual_boundary_annotations.json"
WINDOW = "HarvestHand manual boundary annotation"
PREVIEW_WINDOW = "Perspective preview (reference only)"
REFERENCE_WINDOW = "Candidate overlay reference only"
MAX_DISPLAY = (1400, 900)
CARD_SIZE = (120, 168)

STATUS_KEYS = {
    ord("1"): "valid_complete_card",
    ord("2"): "partially_obstructed",
    ord("3"): "boundary_unclear",
    ord("4"): "blurred_or_damaged",
    ord("5"): "no_usable_card",
}


def load_images():
    with RESULTS_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    unique = {}
    for row in rows:
        if row.get("method") == "combined":
            unique[row["filename"]] = row
    result = list(unique.values())
    result.sort(key=lambda row: (row["class"], row["filename"]))
    if len(result) != 54:
        raise RuntimeError(f"expected 54 combined rows, found {len(result)}")
    return result


def blank_record(row):
    image = cv2.imread(row["source_path"], cv2.IMREAD_COLOR)
    if image is None:
        raise RuntimeError(f"could not read {row['source_path']}")
    height, width = image.shape[:2]
    return {
        "filename": row["filename"],
        "class": row["class"],
        "source_path": row["source_path"],
        "image_width": width,
        "image_height": height,
        "corners": None,
        "annotation_status": None,
        "all_corners_visible": None,
        "reviewer_notes": "",
        "annotated_at": None,
    }


def load_annotations(rows):
    records = {}
    if ANNOTATIONS_JSON.exists():
        with ANNOTATIONS_JSON.open(encoding="utf-8") as handle:
            loaded = json.load(handle)
        records = {record["filename"]: record for record in loaded}
    for row in rows:
        if row["filename"] not in records:
            record = blank_record(row)
            records[record["filename"]] = record
    return [records[row["filename"]] for row in rows]


def save_annotations(records):
    write_annotations(ANNOTATIONS_JSON, records)


def write_annotations(path, records):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(records, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def fit_image(image):
    height, width = image.shape[:2]
    scale = min(MAX_DISPLAY[0] / width, MAX_DISPLAY[1] / height, 1.0)
    if scale == 1.0:
        return image.copy(), scale
    return cv2.resize(
        image, (max(2, int(width * scale)), max(2, int(height * scale))),
        interpolation=cv2.INTER_AREA,
    ), scale


def source_point(display_point, scale):
    return [round(display_point[0] / scale, 2),
            round(display_point[1] / scale, 2)]


def display_point(source, scale):
    return (int(round(source[0] * scale)), int(round(source[1] * scale)))


def close_reference_window():
    try:
        cv2.destroyWindow(REFERENCE_WINDOW)
    except cv2.error:
        pass


def close_preview_window():
    try:
        cv2.destroyWindow(PREVIEW_WINDOW)
    except cv2.error:
        pass


def annotation_window_open():
    try:
        return cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) >= 1
    except cv2.error:
        return False


def draw_overlay(image, points, status, index, total, show_reference):
    output = image.copy()
    if points:
        display = np.asarray(points, dtype=np.int32)
        if len(display) >= 2:
            cv2.polylines(output, [display], False, (0, 255, 255), 2)
        for number, point in enumerate(display):
            cv2.circle(output, tuple(point), 7, (0, 255, 0), -1)
            cv2.putText(
                output, str(number + 1), (int(point[0]) + 8, int(point[1]) - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
            )
    lines = [
        f"Image {index + 1}/{total}",
        "Click corners clockwise | U undo | C clear | Space preview",
        "1 complete 2 obstructed 3 unclear 4 blurred 5 unusable",
        f"Status: {status or 'UNSET'} | R reference | S save | N/P next",
    ]
    for number, line in enumerate(lines):
        cv2.putText(
            output, line, (12, 28 + number * 28),
            cv2.FONT_HERSHEY_SIMPLEX, 0.68, (0, 0, 0), 4,
        )
        cv2.putText(
            output, line, (12, 28 + number * 28),
            cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255, 255, 255), 1,
        )
    if show_reference:
        cv2.putText(
            output, "REFERENCE OVERLAY ENABLED - not ground truth",
            (12, output.shape[0] - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
            (0, 140, 255), 2,
        )
    return output


def preview(points, source):
    crop = perspective_crop(points, source)
    if crop is None:
        print("Preview requires four distinct clockwise corners.")
        return
    enlarged = cv2.resize(crop, (CARD_SIZE[0] * 4, CARD_SIZE[1] * 4),
                           interpolation=cv2.INTER_NEAREST)
    cv2.imshow(PREVIEW_WINDOW, enlarged)


def perspective_crop(points, source):
    if not points_are_clockwise(points):
        return None
    corners = np.asarray(points, dtype=np.float32)
    destination = np.asarray([
        [0, 0], [CARD_SIZE[0] - 1, 0],
        [CARD_SIZE[0] - 1, CARD_SIZE[1] - 1], [0, CARD_SIZE[1] - 1],
    ], dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(corners, destination)
    return cv2.warpPerspective(source, matrix, CARD_SIZE)


def points_are_clockwise(points):
    if len(points) != 4:
        return False
    values = []
    for index in range(4):
        first = np.asarray(points[index], dtype=np.float32)
        second = np.asarray(points[(index + 1) % 4], dtype=np.float32)
        third = np.asarray(points[(index + 2) % 4], dtype=np.float32)
        first_vector = second - first
        second_vector = third - second
        values.append(
            float(first_vector[0] * second_vector[1]
                  - first_vector[1] * second_vector[0])
        )
    return all(value > 1.0 for value in values)


def annotate(rows, records, start_index):
    state = {
        "index": start_index,
        "points": records[start_index].get("corners") or [],
        "status": records[start_index].get("annotation_status"),
        "show_reference": False,
    }

    def mouse_callback(event, x, y, flags, userdata):
        if event == cv2.EVENT_LBUTTONDOWN and len(state["points"]) < 4:
            state["points"].append(source_point((x, y), userdata["scale"]))

    try:
        cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(WINDOW, mouse_callback, {"scale": 1.0})
    except cv2.error as exc:
        raise RuntimeError(f"could not open annotation window: {exc}") from exc
    while True:
        if not annotation_window_open():
            print("Annotation window was closed; saved work is preserved.")
            break
        index = state["index"]
        row = rows[index]
        source = cv2.imread(row["source_path"], cv2.IMREAD_COLOR)
        if source is None:
            raise RuntimeError(f"could not read {row['source_path']}")
        display, scale = fit_image(source)
        display_points = [display_point(point, scale)
                          for point in state["points"]]
        if state["show_reference"]:
            reference = cv2.imread(row.get("overlay", ""), cv2.IMREAD_COLOR)
            if reference is not None:
                reference, _ = fit_image(reference)
                cv2.imshow(REFERENCE_WINDOW, reference)
            else:
                close_reference_window()
        else:
            close_reference_window()
        canvas = draw_overlay(
            display, display_points, state["status"], index, len(rows),
            state["show_reference"],
        )
        try:
            cv2.setMouseCallback(WINDOW, mouse_callback, {"scale": scale})
            cv2.imshow(WINDOW, canvas)
        except cv2.error:
            print("Annotation window became unavailable; saved work is preserved.")
            break
        key = cv2.waitKey(30) & 0xFF
        if key == 27 or key in (ord("q"), ord("Q")):
            break
        if key == ord("u") or key == ord("U"):
            if state["points"]:
                state["points"].pop()
        elif key == ord("c") or key == ord("C"):
            state["points"] = []
        elif key == ord("r") or key == ord("R"):
            state["show_reference"] = not state["show_reference"]
        elif key == ord("t") or key == ord("T"):
            record = records[index]
            notes = input(
                f"Reviewer notes for {record['filename']} "
                "(leave blank to clear): "
            )
            record["reviewer_notes"] = notes
        elif key == ord(" "):
            preview(state["points"], source)
        elif key in STATUS_KEYS:
            state["status"] = STATUS_KEYS[key]
        elif key in (ord("s"), ord("S")):
            if state["status"] is None:
                print("Choose a status before saving.")
                continue
            if (
                state["status"] == "valid_complete_card"
                and not points_are_clockwise(state["points"])
            ):
                print("A complete card requires four clockwise, distinct corners.")
                continue
            record = records[index]
            record["corners"] = state["points"][:] if state["points"] else None
            record["annotation_status"] = state["status"]
            record["all_corners_visible"] = (
                state["status"] == "valid_complete_card"
                and len(state["points"]) == 4
            )
            record["annotated_at"] = datetime.now(timezone.utc).isoformat()
            save_annotations(records)
            print(f"Saved {record['filename']}")
        elif key in (ord("n"), ord("N"), ord("p"), ord("P")):
            direction = 1 if key in (ord("n"), ord("N")) else -1
            state["index"] = (index + direction) % len(rows)
            next_record = records[state["index"]]
            state["points"] = next_record.get("corners") or []
            state["status"] = next_record.get("annotation_status")
            close_preview_window()
            close_reference_window()
    cv2.destroyAllWindows()


def self_test(rows, records):
    if len(rows) != 54 or len(records) != 54:
        raise RuntimeError("annotation set must contain exactly 54 records")
    for row in rows:
        if not Path(row["source_path"]).is_file():
            raise RuntimeError(f"missing source image: {row['source_path']}")
        if not Path(row.get("overlay", "")).is_file():
            raise RuntimeError(f"missing candidate overlay: {row.get('overlay')}")
        source = cv2.imread(row["source_path"], cv2.IMREAD_COLOR)
        overlay = cv2.imread(row["overlay"], cv2.IMREAD_COLOR)
        if source is None or overlay is None:
            raise RuntimeError(f"could not decode visual reference for {row['filename']}")
    sample = rows[0]
    source = cv2.imread(sample["source_path"], cv2.IMREAD_COLOR)
    height, width = source.shape[:2]
    points = [[1, 1], [width - 2, 1], [width - 2, height - 2], [1, height - 2]]
    crop = perspective_crop(points, source)
    if crop is None or crop.shape[:2] != (CARD_SIZE[1], CARD_SIZE[0]):
        raise RuntimeError("perspective preview validation failed")
    temporary = MANUAL_DIR / "manual_boundary_annotations.self_test.json"
    try:
        round_trip_records = json.loads(json.dumps(records))
        round_trip_records[0]["corners"] = points
        round_trip_records[0]["annotation_status"] = "valid_complete_card"
        round_trip_records[0]["all_corners_visible"] = True
        round_trip_records[0]["reviewer_notes"] = "self-test note"
        write_annotations(temporary, round_trip_records)
        with temporary.open(encoding="utf-8") as handle:
            reopened = json.load(handle)
        if len(reopened) != len(records):
            raise RuntimeError("annotation save/reopen validation failed")
        restored = reopened[0]
        if (
            restored["corners"] != points
            or restored["annotation_status"] != "valid_complete_card"
            or restored["reviewer_notes"] != "self-test note"
        ):
            raise RuntimeError("saved corners or notes were not preserved")
    finally:
        if temporary.exists():
            temporary.unlink()
    print("self_test_ok")
    print(f"records={len(records)}")
    print("source_images=54")
    print("candidate_overlays=54")
    print("perspective_preview=120x168")
    print("annotation_round_trip=ok (corners, status, notes)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0,
                        help="zero-based image index to open")
    parser.add_argument("--initialize", action="store_true",
                        help="create blank records without opening the GUI")
    parser.add_argument("--self-test", action="store_true",
                        help="validate paths, preview geometry, and JSON round-trip")
    args = parser.parse_args()
    rows = load_images()
    records = load_annotations(rows)
    if not 0 <= args.start < len(rows):
        raise ValueError(f"--start must be between 0 and {len(rows) - 1}")
    if args.initialize:
        save_annotations(records)
        print(f"Initialized {len(records)} blank records at {ANNOTATIONS_JSON}")
        return
    if args.self_test:
        self_test(rows, records)
        return
    if os.environ.get("DISPLAY") == "" and sys.platform != "win32":
        raise RuntimeError("OpenCV GUI requires a desktop display.")
    annotate(rows, records, args.start)


if __name__ == "__main__":
    main()
