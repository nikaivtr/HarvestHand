"""Compare experimental candidates with manually annotated card boundaries."""

import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pygame
from PIL import Image, ImageDraw, ImageFont

VALIDATION = Path(__file__).resolve().parent
MANUAL_DIR = VALIDATION.parent
EXPERIMENT = MANUAL_DIR.parent
ROOT = EXPERIMENT.parent.parent.parent
ANNOTATIONS = MANUAL_DIR / "manual_boundary_annotations.json"
RESULTS = EXPERIMENT / "visual_localization_results.csv"
REPORT_AUDIT = VALIDATION / "ANNOTATION_AUDIT_REPORT.md"
REPORT_VALIDATION = EXPERIMENT / "CANDIDATE_VS_MANUAL_REPORT.md"
RESULTS_CSV = VALIDATION / "candidate_vs_manual_validation.csv"
EXTRACTOR_CSV = VALIDATION / "manual_crop_extractor_results.csv"
SUMMARY_JSON = VALIDATION / "validation_summary.json"
OVERLAY_DIR = VALIDATION / "comparison_overlays"
SHEET_DIR = VALIDATION / "comparison_contact_sheets"

sys.path.insert(0, str(EXPERIMENT))
import visual_localization_experiment as experiment
import cardscan.features as features
import cardscan.preprocess as preprocess


METHODS = ("existing", "multi_scale", "contrast_enhanced", "combined")
STATUSES = {
    "valid_complete_card",
    "no_usable_card",
    "blurred_or_damaged",
}


def load_data():
    with ANNOTATIONS.open(encoding="utf-8") as handle:
        annotations = json.load(handle)
    with RESULTS.open(newline="", encoding="utf-8-sig") as handle:
        result_rows = list(csv.DictReader(handle))
    combined = {
        row["filename"]: row
        for row in result_rows
        if row.get("method") == "combined"
    }
    return annotations, combined


def cross(first, second):
    return float(first[0] * second[1] - first[1] * second[0])


def polygon_properties(points):
    points = np.asarray(points, dtype=np.float64)
    values = []
    for index in range(4):
        first = points[index]
        second = points[(index + 1) % 4]
        third = points[(index + 2) % 4]
        values.append(cross(second - first, third - second))
    area = abs(cv2.contourArea(points.astype(np.float32)))
    return values, area


def audit_annotations(annotations, combined):
    issues = []
    warnings = []
    filenames = [record.get("filename") for record in annotations]
    if len(annotations) != 54:
        issues.append(f"expected 54 records, found {len(annotations)}")
    if len(set(filenames)) != len(filenames):
        issues.append("duplicate annotation filenames found")
    if set(filenames) != set(combined):
        missing = sorted(set(combined) - set(filenames))
        extra = sorted(set(filenames) - set(combined))
        if missing:
            issues.append(f"missing combined-result filenames: {missing}")
        if extra:
            issues.append(f"annotation filenames not in combined results: {extra}")
    for record in annotations:
        filename = record.get("filename")
        status = record.get("annotation_status")
        if status not in STATUSES:
            issues.append(f"{filename}: unrecognized status {status!r}")
        corners = record.get("corners")
        if not isinstance(corners, list) or len(corners) != 4:
            issues.append(f"{filename}: corner set does not contain four points")
            continue
        try:
            points = np.asarray(corners, dtype=np.float64)
        except (TypeError, ValueError):
            issues.append(f"{filename}: corner coordinates are not numeric")
            continue
        if points.shape != (4, 2) or not np.isfinite(points).all():
            issues.append(f"{filename}: corners are not finite 2D coordinates")
            continue
        width = int(record.get("image_width", 0))
        height = int(record.get("image_height", 0))
        if (
            (points[:, 0] < 0).any() or (points[:, 0] >= width).any()
            or (points[:, 1] < 0).any() or (points[:, 1] >= height).any()
        ):
            issues.append(f"{filename}: corner lies outside image bounds")
        turns, area = polygon_properties(points)
        if not all(value > 1.0 for value in turns):
            issues.append(f"{filename}: corners are not clockwise convex points")
        pairwise = [
            np.linalg.norm(points[index] - points[(index + 1) % 4])
            for index in range(4)
        ]
        if min(pairwise) < 2.0:
            issues.append(f"{filename}: duplicate or collapsed corners")
        area_ratio = area / max(width * height, 1)
        if area_ratio < 0.001:
            issues.append(f"{filename}: quadrilateral is implausibly small")
        elif area_ratio < 0.005:
            warnings.append(
                f"{filename}: small annotated quadrilateral area ratio "
                f"{area_ratio:.5f}"
            )
        if status == "valid_complete_card" and record.get("all_corners_visible") is not True:
            warnings.append(f"{filename}: complete status but all_corners_visible is not true")
    return issues, warnings


def write_audit_report(annotations, combined, issues, warnings):
    counts = {}
    for record in annotations:
        status = record.get("annotation_status")
        counts[status] = counts.get(status, 0) + 1
    annotation_names = {record.get("filename") for record in annotations}
    matched_count = len(set(combined) & annotation_names)
    lines = [
        "# Annotation Audit Report",
        "",
        f"- Records: **{len(annotations)}**",
        f"- Matching combined-result filenames: **{matched_count}**",
        f"- `valid_complete_card`: **{counts.get('valid_complete_card', 0)}**",
        f"- `no_usable_card`: **{counts.get('no_usable_card', 0)}**",
        f"- `blurred_or_damaged`: **{counts.get('blurred_or_damaged', 0)}**",
        "",
        "## Issues",
        "",
    ]
    lines.extend(f"- {issue}" for issue in issues or ["None"])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in warnings or ["None"])
    lines.extend([
        "",
        "Only valid complete-card records are eligible for the primary "
        "geometric benchmark. Excluded statuses are retained for reporting "
        "but are not treated as card-boundary ground truth.",
    ])
    REPORT_AUDIT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def permutations(points):
    points = list(points)
    for reverse in (False, True):
        ordered = points[::-1] if reverse else points
        for shift in range(4):
            yield np.asarray(ordered[shift:] + ordered[:shift], dtype=np.float64)


def match_metrics(manual, candidate, width, height):
    diagonal = math.hypot(width, height)
    best = None
    for ordered in permutations(candidate):
        errors = np.linalg.norm(ordered - manual, axis=1)
        mean_error = float(errors.mean())
        if best is None or mean_error < best["mean_corner_error_px"]:
            best = {
                "mean_corner_error_px": mean_error,
                "max_corner_error_px": float(errors.max()),
                "normalized_mean_error": mean_error / diagonal,
                "normalized_max_error": float(errors.max()) / diagonal,
                "ordered_candidate": ordered,
            }
    manual_polygon = manual.astype(np.float32)
    candidate_polygon = best["ordered_candidate"].astype(np.float32)
    manual_area = abs(cv2.contourArea(manual_polygon))
    candidate_area = abs(cv2.contourArea(candidate_polygon))
    intersection, _ = cv2.intersectConvexConvex(
        manual_polygon, candidate_polygon
    )
    union = manual_area + candidate_area - float(intersection)
    best["iou"] = float(intersection / union) if union > 0 else 0.0
    best.pop("ordered_candidate")
    return best


def matched_order(manual, candidate):
    best = None
    for ordered in permutations(candidate):
        errors = np.linalg.norm(ordered - manual, axis=1)
        mean_error = float(errors.mean())
        if best is None or mean_error < best[0]:
            best = (mean_error, ordered)
    return best[1] if best is not None else None


def candidate_record(base, method, rank, candidate, metrics, selection):
    result = {
        "class": base["class"],
        "filename": base["filename"],
        "method": method,
        "candidate_selection": selection,
        "candidate_rank": rank,
        "candidate_exists": True,
    }
    result.update(metrics)
    if candidate is not None:
        result.update({
            "candidate_area_ratio": candidate["metrics"]["area_ratio"],
            "candidate_overall_score": candidate["metrics"]["overall_score"],
            "candidate_rank_category": candidate["metrics"]["rank_category"],
        })
    return result


def draw_comparison(source, manual, candidate, label, output):
    image = source.copy()
    manual_points = np.rint(manual).astype(np.int32)
    cv2.polylines(image, [manual_points], True, (0, 255, 0), 4)
    for index, point in enumerate(manual_points):
        cv2.circle(image, tuple(point), 8, (0, 255, 0), -1)
        cv2.putText(image, f"M{index + 1}", tuple(point + [8, -8]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    if candidate is not None:
        candidate_points = np.rint(candidate).astype(np.int32)
        cv2.polylines(image, [candidate_points], True, (0, 0, 255), 3)
        for index, point in enumerate(candidate_points):
            cv2.circle(image, tuple(point), 6, (0, 0, 255), -1)
            cv2.putText(image, f"C{index + 1}", tuple(point + [8, 18]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.line(
                image, tuple(manual_points[index]), tuple(point),
                (255, 0, 255), 2,
            )
    cv2.putText(image, label, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 255), 3)
    cv2.putText(image, label, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 0, 0), 1)
    cv2.imwrite(str(output), image)


def make_contact_sheets(overlays):
    grouped = {}
    for path in overlays:
        method = path.name.split("__", 1)[0]
        grouped.setdefault(method, []).append(path)
    for method, paths in grouped.items():
        columns = 3
        cell_width, cell_height = 460, 360
        sheet = Image.new(
            "RGB",
            (columns * cell_width,
             math.ceil(len(paths) / columns) * cell_height),
            "white",
        )
        draw = ImageDraw.Draw(sheet)
        for index, path in enumerate(paths):
            x = index % columns * cell_width
            y = index // columns * cell_height
            try:
                image = Image.open(path).convert("RGB")
                image.thumbnail((440, 325))
                sheet.paste(
                    image,
                    (x + (cell_width - image.width) // 2, y + 28),
                )
            except (OSError, ValueError):
                draw.text((x + 15, y + 140), "IMAGE UNAVAILABLE",
                          fill="red")
            draw.text((x + 8, y + 7), path.name[:58], fill="black")
        sheet.save(
            SHEET_DIR / f"{method}_manual_comparison_contact_sheet.jpg",
            quality=90,
        )


def run_validation(annotations, combined):
    eligible = [
        record for record in annotations
        if record["annotation_status"] == "valid_complete_card"
    ]
    output_rows = []
    extractor_rows = []
    overlays = []
    pygame.init()
    try:
        for record in eligible:
            source = preprocess.load_image(record["source_path"])
            if source is None:
                raise RuntimeError(f"could not load {record['filename']}")
            manual = np.asarray(record["corners"], dtype=np.float64)
            source_array = cv2.imread(record["source_path"], cv2.IMREAD_COLOR)
            height, width = source_array.shape[:2]
            manual_crop, manual_pass, manual_length, manual_ms = (
                experiment.run_extractor(source, manual)
            )
            manual_detection = preprocess.last_detection()
            manual_crop_path = VALIDATION / (
                f"manual_crop_{record['class']}__{record['filename']}"
            )
            pygame.image.save(manual_crop, str(manual_crop_path))
            extractor_rows.append({
                "class": record["class"],
                "filename": record["filename"],
                "source_type": "manual",
                "method": "manual",
                "preprocessing_succeeded": manual_detection.get("status") == "detected",
                "feature_extraction_succeeded": manual_pass,
                "feature_length": manual_length,
                "processing_ms": manual_ms,
                "failure_reason": manual_detection.get("reason", ""),
                "crop_path": str(manual_crop_path),
            })
            method_candidates = {}
            for method in METHODS:
                if method == "existing":
                    method_candidates[method] = []
                else:
                    method_candidates[method] = experiment.method_candidates(
                        source, method
                    )
            for method in METHODS:
                candidates = method_candidates[method]
                ranked = candidates[0] if candidates else None
                ranked_match = (
                    match_metrics(manual, ranked["points"], width, height)
                    if ranked is not None else None
                )
                oracle = None
                oracle_candidate = None
                for candidate in candidates:
                    current = match_metrics(
                        manual, candidate["points"], width, height
                    )
                    if oracle is None or current["mean_corner_error_px"] < oracle["mean_corner_error_px"]:
                        oracle = current
                        oracle_candidate = candidate
                if ranked is None:
                    row = {
                        "class": record["class"],
                        "filename": record["filename"],
                        "method": method,
                        "candidate_selection": "ranked_top",
                        "candidate_rank": "",
                        "candidate_exists": False,
                        "mean_corner_error_px": "",
                        "max_corner_error_px": "",
                        "normalized_mean_error": "",
                        "normalized_max_error": "",
                        "iou": "",
                        "candidate_area_ratio": "",
                        "candidate_overall_score": "",
                        "candidate_rank_category": "",
                    }
                    output_rows.append(row)
                else:
                    output_rows.append(candidate_record(
                        record, method, 1, ranked, ranked_match, "ranked_top"
                    ))
                if oracle_candidate is not None and oracle_candidate is not ranked:
                    output_rows.append(candidate_record(
                        record, method, "", oracle_candidate, oracle,
                        "oracle_best_candidate",
                    ))
                if ranked is not None:
                    crop, passed, length, elapsed = experiment.run_extractor(
                        source, ranked["points"]
                    )
                    detection = preprocess.last_detection()
                    crop_path = VALIDATION / (
                        f"{method}_crop_{record['class']}__{record['filename']}"
                    )
                    pygame.image.save(crop, str(crop_path))
                    extractor_rows.append({
                        "class": record["class"],
                        "filename": record["filename"],
                        "source_type": "experimental",
                        "method": method,
                        "preprocessing_succeeded": detection.get("status") == "detected",
                        "feature_extraction_succeeded": passed,
                        "feature_length": length,
                        "processing_ms": elapsed,
                        "failure_reason": detection.get("reason", ""),
                        "crop_path": str(crop_path),
                    })
                candidate_points = ranked["points"] if ranked is not None else None
                if candidate_points is not None:
                    candidate_points = matched_order(manual, candidate_points)
                overlay_path = OVERLAY_DIR / (
                    f"{method}__{record['class']}__{record['filename']}"
                )
                draw_comparison(
                    source_array, manual, candidate_points,
                    f"{method} | {record['filename']}", overlay_path
                )
                overlays.append(overlay_path)
    finally:
        pygame.quit()
    return output_rows, extractor_rows, overlays, len(eligible)


def write_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def aggregate(output_rows, eligible_count):
    summary = {}
    summary["ranked_rows"] = [
        row for row in output_rows
        if row["candidate_selection"] == "ranked_top"
    ]
    for method in METHODS:
        ranked = [
            row for row in output_rows
            if row["method"] == method
            and row["candidate_selection"] == "ranked_top"
        ]
        missing = sum(not row["candidate_exists"] for row in ranked)
        incorrect = 0
        for row in ranked:
            if not row["candidate_exists"]:
                continue
            if (
                float(row["normalized_max_error"]) > 0.10
                or float(row["iou"]) < 0.50
            ):
                incorrect += 1
        summary[method] = {
            "eligible_images": eligible_count,
            "candidate_missing": missing,
            "incorrect_or_background": incorrect,
            "geometrically_correct_at_10_percent": (
                eligible_count - missing - incorrect
            ),
            "candidate_detection_rate": (
                (eligible_count - missing) / max(eligible_count, 1)
            ),
            "correct_boundary_rate": (
                (eligible_count - missing - incorrect)
                / max(eligible_count, 1)
            ),
        }
        for threshold in (0.02, 0.05, 0.10):
            summary[method][f"all_corners_within_{int(threshold * 100)}_percent"] = sum(
                row["candidate_exists"]
                and float(row["normalized_max_error"]) <= threshold
                for row in ranked
            )
    return summary


def write_validation_report(
    annotations, summary, extractor_rows, issues, warnings
):
    lines = [
        "# Candidate vs Manual Boundary Validation",
        "",
        "This evaluation compares reconstructed experimental candidates with "
        "manually annotated boundaries. Production code, thresholds, models, "
        "and the original annotation JSON were not modified.",
        "",
        "## Annotation eligibility",
        "",
        "- Total annotations: **54**",
        "- Primary benchmark: **29 `valid_complete_card` records**",
        "- Excluded: **23 `no_usable_card`, 2 `blurred_or_damaged`**",
        "- Annotation audit issues: **" + str(len(issues)) + "**",
        "- Annotation audit warnings: **" + str(len(warnings)) + "**",
        "",
        "Only the 29 complete-card records are included in geometric accuracy.",
        "",
        "## Geometric results",
        "",
        "| Method | Missing | Incorrect/background | Correct <=10% diagonal | "
        "2% / 5% / 10% corner threshold counts |",
        "|---|---:|---:|---:|---:|",
    ]
    for method in METHODS:
        item = summary[method]
        lines.append(
            f"| {method} | {item['candidate_missing']} | "
            f"{item['incorrect_or_background']} | "
            f"{item['geometrically_correct_at_10_percent']} | "
            f"{item['all_corners_within_2_percent']} / "
            f"{item['all_corners_within_5_percent']} / "
            f"{item['all_corners_within_10_percent']} |"
        )
    lines.extend(["", "## Per-class geometric results", ""])
    lines.extend([
        "| Class | Method | Eligible | Missing | Incorrect/background | "
        "Correct <=10% |",
        "|---|---|---:|---:|---:|---:|",
    ])
    for class_name in ("pechay_plant", "monggo_plant"):
        for method in METHODS:
            rows = [
                row for row in summary["ranked_rows"]
                if row["class"] == class_name
                and row["method"] == method
            ]
            missing = sum(not row["candidate_exists"] for row in rows)
            incorrect = sum(
                row["candidate_exists"]
                and (
                    float(row["normalized_max_error"]) > 0.10
                    or float(row["iou"]) < 0.50
                )
                for row in rows
            )
            correct = len(rows) - missing - incorrect
            lines.append(
                f"| {class_name} | {method} | {len(rows)} | {missing} | "
                f"{incorrect} | {correct} |"
            )
    lines.extend(["", "## Extractor compatibility summary", ""])
    lines.extend([
        "| Source | Method | Total | Preprocessing success | "
        "Feature success |",
        "|---|---|---:|---:|---:|",
    ])
    for source_type, method in (
        ("manual", "manual"),
        ("experimental", "multi_scale"),
        ("experimental", "contrast_enhanced"),
        ("experimental", "combined"),
    ):
        rows = [
            row for row in extractor_rows
            if row["source_type"] == source_type and row["method"] == method
        ]
        lines.append(
            f"| {source_type} | {method} | {len(rows)} | "
            f"{sum(row['preprocessing_succeeded'] for row in rows)} | "
            f"{sum(row['feature_extraction_succeeded'] for row in rows)} |"
        )
    lines.extend([
        "",
        "Incorrect/background is defined for the ranked top candidate as "
        "maximum corner error above 10% of the image diagonal or polygon IoU "
        "below 0.50. This is a geometric evaluation rule, not a visual "
        "semantic classifier.",
        "",
        "## Extractor results",
        "",
        "Manual and experimental crops were passed through the unchanged "
        "`features.extract()` path. A 2,304-value vector indicates extractor "
        "compatibility only; it does not prove a correct boundary.",
        "",
        "See `manual_crop_extractor_results.csv` for per-image results.",
        "",
        "## Candidate reconstruction note",
        "",
        "The original `visual_localization_results.csv` stores candidate "
        "metrics and crop paths but not corner coordinates. Therefore, the "
        "isolated experiment's candidate-generation functions were rerun for "
        "the 29 eligible images to reconstruct coordinates. This was required "
        "for geometric comparison and did not modify prior outputs.",
        "",
        "## Recommendation",
        "",
        "Geometric accuracy alone is not sufficient for production integration. "
        "A method should only proceed to a controlled implementation "
        "experiment after review of the comparison overlays, false positives, "
        "crop completeness, and processing cost.",
    ])
    REPORT_VALIDATION.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    OVERLAY_DIR.mkdir(parents=True, exist_ok=True)
    SHEET_DIR.mkdir(parents=True, exist_ok=True)
    annotations, combined = load_data()
    issues, warnings = audit_annotations(annotations, combined)
    write_audit_report(annotations, combined, issues, warnings)
    print(f"annotation_records={len(annotations)}")
    print(f"annotation_issues={len(issues)}")
    print(f"annotation_warnings={len(warnings)}")
    if issues:
        print(f"audit_report={REPORT_AUDIT}")
        raise SystemExit(2)
    if args.audit_only:
        print("audit_ok")
        return
    rows, extractor_rows, overlays, eligible = run_validation(
        annotations, combined
    )
    write_csv(RESULTS_CSV, rows)
    write_csv(EXTRACTOR_CSV, extractor_rows)
    summary = aggregate(rows, eligible)
    make_contact_sheets(overlays)
    SUMMARY_JSON.write_text(json.dumps({
        "annotation_counts": {
            status: sum(
                record["annotation_status"] == status for record in annotations
            )
            for status in sorted(STATUSES)
        },
        "eligible_complete_cards": eligible,
        "methods": {
            method: values for method, values in summary.items()
            if method != "ranked_rows"
        },
        "visual_verification": "manual review overlays required",
    }, indent=2) + "\n", encoding="utf-8")
    write_validation_report(
        annotations, summary, extractor_rows, issues, warnings
    )
    print(f"eligible={eligible}")
    print(f"validation_rows={len(rows)}")
    print(f"extractor_rows={len(extractor_rows)}")
    print(f"report={REPORT_VALIDATION}")


if __name__ == "__main__":
    main()
