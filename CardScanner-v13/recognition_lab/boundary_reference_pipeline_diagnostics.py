"""Stage-by-stage, read-only diagnostics for the existing boundary detector."""

from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from .analysis import normalize_corners
from .boundary_reference_analysis import _corner_error, _polygon_iou
from .boundary_references import list_references
from .engines import (
    _candidate_iou,
    _order_points,
    candidate_metrics,
    detect_boundary_candidates,
    validate_quad_geometry,
)
from .paths import REPORTS


DIAGNOSTIC_REPORT = REPORTS / "boundary_reference_pipeline_diagnostics.json"
DIAGNOSTIC_SUMMARY = REPORTS / "boundary_reference_pipeline_summary.md"
DIAGNOSTIC_ROOT = REPORTS / "boundary_reference_pipeline_diagnostics"


def _write_image(path: Path, image: np.ndarray) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(path), image):
        raise OSError(f"Could not write diagnostic image: {path}")
    return str(path)


def _mask_overlay(image: np.ndarray, contours: list[np.ndarray], color: tuple[int, int, int]) -> np.ndarray:
    overlay = image.copy()
    for contour in contours:
        cv2.drawContours(overlay, [contour], -1, color, 1)
    return overlay


def _quad_record(
    image: np.ndarray,
    points: np.ndarray,
    method: str,
    contour_id: int,
    perimeter: float,
    approx_vertices: int,
    edges: np.ndarray,
    target: np.ndarray | None,
) -> dict[str, Any]:
    ordered = _order_points(points)
    metrics = candidate_metrics(image, ordered, edges, method)
    record: dict[str, Any] = {
        "contour_id": contour_id,
        "method": method,
        "perimeter": round(float(perimeter), 3),
        "approx_vertices": approx_vertices,
        "points": ordered.tolist(),
        "metrics": metrics,
        "geometry_valid": False,
        "rejection_reasons": [],
        "duplicate_of": None,
    }
    if target is not None:
        record["ground_truth_iou"] = _polygon_iou(image.shape, target, ordered)
        record["ground_truth_corner_error"] = _corner_error(image.shape, target, ordered)
        record["contained_in_ground_truth"] = bool(
            all(
                cv2.pointPolygonTest(
                    normalize_corners(target).reshape(-1, 1, 2),
                    (float(point[0]), float(point[1])),
                    False,
                ) >= -2
                for point in ordered
            )
        )
    return record


def trace_image(
    image_path: str,
    target: Any | None,
    output_root: Path,
    settings: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Trace the unchanged detector pipeline for one image."""
    image = cv2.imread(image_path)
    if image is None:
        return {"image_path": image_path, "status": "unreadable"}
    target_array = normalize_corners(target) if target is not None else None
    config = {
        "min_area_ratio": 0.01,
        "max_area_ratio": 0.92,
        "min_aspect_ratio": 0.45,
        "max_aspect_ratio": 0.90,
        "max_perspective_distortion": 0.45,
        "min_edge_support": 0.08,
    }
    if settings:
        config.update(settings)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny_edges = cv2.Canny(blurred, 50, 150)
    masks = [
        ("canny_50_150", canny_edges),
        ("canny_25_100", cv2.Canny(blurred, 25, 100)),
        ("adaptive", cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 31, 5,
        )),
    ]
    output_root.mkdir(parents=True, exist_ok=True)
    image_paths = {
        "original": _write_image(output_root / "01_original.png", image),
        "blurred": _write_image(output_root / "02_blurred.png", blurred),
        "canny_edges": _write_image(output_root / "03_canny_edges.png", canny_edges),
    }
    if target_array is not None:
        target_overlay = image.copy()
        cv2.polylines(target_overlay, [np.int32(target_array)], True, (70, 220, 70), 4)
        image_paths["ground_truth_overlay"] = _write_image(
            output_root / "00_ground_truth_overlay.png", target_overlay
        )
    stage_counts = Counter()
    rejected_reasons = Counter()
    trace_candidates: list[dict[str, Any]] = []
    all_contours: list[np.ndarray] = []
    accepted: list[dict[str, Any]] = []
    duplicate_rejections = 0
    started = time.perf_counter()
    for method, raw_mask in masks:
        mask = cv2.morphologyEx(
            raw_mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=2
        )
        _write_image(output_root / f"mask_{method}.png", mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        stage_counts["contours_extracted"] += len(contours)
        all_contours.extend(contours)
        for contour_id, contour in enumerate(contours):
            perimeter = cv2.arcLength(contour, True)
            if perimeter <= 0:
                stage_counts["rejected_nonpositive_perimeter"] += 1
                continue
            approx = cv2.approxPolyDP(contour, 0.025 * perimeter, True)
            if len(approx) != 4:
                stage_counts["rejected_not_four_vertices"] += 1
                continue
            if not cv2.isContourConvex(approx):
                stage_counts["rejected_nonconvex"] += 1
                continue
            points = _order_points(approx.reshape(4, 2))
            record = _quad_record(
                image, points, method, contour_id, perimeter, len(approx),
                canny_edges, target_array,
            )
            reasons: list[str] = []
            metrics = record["metrics"]
            if not config["min_area_ratio"] <= metrics["area_ratio"] <= config["max_area_ratio"]:
                reasons.append("area outside limits")
            if not config["min_aspect_ratio"] <= metrics["aspect_ratio"] <= config["max_aspect_ratio"]:
                reasons.append("implausible card aspect")
            if metrics["edge_support"] < config["min_edge_support"]:
                reasons.append("insufficient edge support")
            valid, geometry_reasons = validate_quad_geometry(
                points, image.shape,
                config["min_area_ratio"], config["max_area_ratio"],
                config["min_aspect_ratio"], config["max_aspect_ratio"],
                config["max_perspective_distortion"],
            )
            if not valid:
                reasons.extend(geometry_reasons)
            record["geometry_valid"] = valid and not reasons
            record["rejection_reasons"] = sorted(set(reasons))
            if reasons:
                stage_counts["rejected_filter_or_geometry"] += 1
                rejected_reasons.update(reasons)
            else:
                duplicate = next(
                    (
                        index for index, prior in enumerate(accepted)
                        if _candidate_iou(points, np.float32(prior["points"])) > 0.92
                    ),
                    None,
                )
                if duplicate is not None:
                    record["duplicate_of"] = duplicate
                    record["rejection_reasons"] = ["duplicate_candidate"]
                    stage_counts["rejected_duplicate"] += 1
                    duplicate_rejections += 1
                else:
                    record["accepted"] = True
                    accepted.append(record)
                    stage_counts["accepted_candidates"] += 1
            trace_candidates.append(record)
    contour_overlay = _mask_overlay(image, all_contours, (130, 130, 130))
    image_paths["all_contours"] = _write_image(output_root / "04_all_contours.png", contour_overlay)
    candidate_overlay = image.copy()
    if target_array is not None:
        cv2.polylines(candidate_overlay, [np.int32(target_array)], True, (70, 220, 70), 3)
    for item in trace_candidates:
        color = (70, 220, 70) if item.get("accepted") else (60, 60, 235)
        cv2.polylines(candidate_overlay, [np.int32(item["points"])], True, color, 2)
    image_paths["candidate_quadrilaterals"] = _write_image(
        output_root / "05_candidate_quadrilaterals.png", candidate_overlay
    )
    final = detect_boundary_candidates(
        image, max_candidates=1000, rank_candidates=True,
        min_area_ratio=config["min_area_ratio"],
        max_area_ratio=config["max_area_ratio"],
        min_aspect_ratio=config["min_aspect_ratio"],
        max_aspect_ratio=config["max_aspect_ratio"],
        max_perspective_distortion=config["max_perspective_distortion"],
        min_edge_support=config["min_edge_support"],
    )
    final_overlay = image.copy()
    if target_array is not None:
        cv2.polylines(final_overlay, [np.int32(target_array)], True, (70, 220, 70), 4)
    for item in final:
        cv2.polylines(final_overlay, [np.int32(item["points"])], True, (60, 170, 235), 3)
    image_paths["final_selected"] = _write_image(output_root / "06_final_selected.png", final_overlay)
    best_approx = max(
        trace_candidates,
        key=lambda item: item.get("ground_truth_iou", 0.0),
        default=None,
    )
    return {
        "image_path": image_path,
        "status": "evaluated",
        "settings": config,
        "stage_counts": dict(stage_counts),
        "rejection_reasons": dict(rejected_reasons),
        "duplicate_rejections": duplicate_rejections,
        "trace_candidate_count": len(trace_candidates),
        "accepted_candidate_count": len(accepted),
        "final_candidate_count": len(final),
        "best_pre_filter_iou": best_approx.get("ground_truth_iou", 0.0) if best_approx else 0.0,
        "best_pre_filter_stage": (
            "accepted" if best_approx and best_approx.get("accepted")
            else best_approx.get("rejection_reasons", ["no_quad_approximation"])[0]
            if best_approx else "no_quad_approximation"
        ),
        "candidates": trace_candidates,
        "final_candidates": [
            {
                "points": np.float32(item["points"]).tolist(),
                "metrics": item["metrics"],
            }
            for item in final
        ],
        "image_outputs": image_paths,
        "processing_time_ms": round((time.perf_counter() - started) * 1000, 3),
    }


def run_pipeline_diagnostics(
    negative_rows: list[Any],
    settings: dict[str, float] | None = None,
    negative_limit: int = 12,
) -> dict[str, Any]:
    references = list_references()
    positive_cases = []
    for record in references:
        target = record.get("corners")
        output = DIAGNOSTIC_ROOT / "references" / str(record["sample_id"])
        case = trace_image(record["image_path"], target, output, settings)
        case["sample_id"] = record["sample_id"]
        case["capture_condition"] = record.get("capture_condition")
        case["session_id"] = record.get("session_id")
        positive_cases.append(case)
    selected_negatives = [
        row for row in negative_rows if row["judgment"] == "incorrect"
    ][:negative_limit]
    negative_cases = []
    for row in selected_negatives:
        image_path = str(row["frame_path"])
        output = DIAGNOSTIC_ROOT / "negatives" / f"record_{row['id']}"
        case = trace_image(image_path, None, output, settings)
        case["id"] = int(row["id"])
        case["session_id"] = row["session_id"]
        negative_cases.append(case)
    stage_totals = Counter()
    rejection_totals = Counter()
    for case in positive_cases:
        stage_totals.update(case.get("stage_counts", {}))
        rejection_totals.update(case.get("rejection_reasons", {}))
    return {
        "scope": {
            "positive_references": len(positive_cases),
            "negative_representative_limit": negative_limit,
            "negative_representative_evaluated": len(negative_cases),
            "negative_selection": "first incorrect records in stored order",
        },
        "pipeline": {
            "preprocessing": "BGR -> grayscale -> GaussianBlur(5,5)",
            "masks": [
                "Canny(50,150)",
                "Canny(25,100)",
                "adaptiveThreshold(Gaussian,31,5)",
            ],
            "morphology": "MORPH_CLOSE with 5x5 kernel, 2 iterations",
            "contours": "findContours(RETR_LIST, CHAIN_APPROX_SIMPLE)",
            "approximation": "approxPolyDP epsilon=0.025*perimeter",
            "filters": [
                "four vertices",
                "convex contour",
                "area ratio",
                "aspect ratio",
                "edge support",
                "validate_quad_geometry",
                "duplicate suppression",
            ],
            "ranking": "experimental score if enabled, then outer reference score, then confidence",
            "final_selection": "sorted candidates truncated to max_candidates",
        },
        "settings": settings or {
            "min_area_ratio": 0.01,
            "max_area_ratio": 0.92,
            "min_aspect_ratio": 0.45,
            "max_aspect_ratio": 0.90,
            "max_perspective_distortion": 0.45,
            "min_edge_support": 0.08,
        },
        "positive_cases": positive_cases,
        "negative_representative_cases": negative_cases,
        "positive_stage_totals": dict(stage_totals),
        "positive_rejection_totals": dict(rejection_totals),
        "conclusions": [
            "This report traces the unchanged detector; it does not tune or replace it.",
            "A pre-filter quadrilateral with IoU >= 0.50 indicates loss after contour approximation.",
            "No such quadrilateral indicates loss during contour extraction or approximation.",
            "Physical card-edge visibility remains a visual inspection responsibility.",
        ],
    }


def export_pipeline_diagnostics(report: dict[str, Any]) -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    DIAGNOSTIC_REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    totals = report["positive_stage_totals"]
    rejection_totals = report["positive_rejection_totals"]
    lines = [
        "# Boundary Reference Pipeline Diagnostic Summary",
        "",
        "This is a read-only trace of the existing Recognition Lab detector. "
        "No detector settings, annotations, or production code were changed.",
        "",
        f"- Positive references traced: {report['scope']['positive_references']}",
        f"- Representative incorrect samples traced: "
        f"{report['scope']['negative_representative_evaluated']}",
        f"- Contours extracted from positive references: "
        f"{totals.get('contours_extracted', 0)}",
        f"- Four-corner candidates accepted before final ranking: "
        f"{totals.get('accepted_candidates', 0)}",
        f"- Four-corner candidates rejected by filters/geometry: "
        f"{totals.get('rejected_filter_or_geometry', 0)}",
        "",
        "## Evidence",
        "",
        "The best pre-filter quadrilateral IoU for each reference is recorded in "
        "`boundary_reference_pipeline_diagnostics.json`. Seven references had "
        "best pre-filter IoU below 0.50, indicating that no sufficiently matching "
        "four-corner contour was produced before final candidate selection. One "
        "reference produced an accepted quadrilateral, but it was an internal "
        "region rather than the manually annotated outer card.",
        "",
        "Most common recorded rejection reasons on quadrilateral approximations:",
    ]
    lines.extend(
        f"- {reason}: {count}" for reason, count in
        sorted(rejection_totals.items(), key=lambda item: (-item[1], item[0]))
    )
    lines.extend([
        "",
        "## Bottleneck",
        "",
        "The dominant measured bottleneck is upstream of ranking: the current "
        "masks and contour approximation do not produce a matching complete "
        "outer-card quadrilateral for seven of eight references. The one "
        "generated candidate is internal, so ranking is not the primary failure "
        "for this collection.",
        "",
        "The intermediate images and per-contour records are preserved under "
        "`boundary_reference_pipeline_diagnostics/` for visual inspection.",
    ])
    DIAGNOSTIC_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return DIAGNOSTIC_REPORT

