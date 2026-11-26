"""Export verified observations without inventing performance results."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from .paths import REPORTS


def build_report(rows: list[Any], phase: str) -> dict[str, Any]:
    total = len(rows)
    verified = [row for row in rows if row["verification"] == "correct"]
    rejected = [row for row in rows if row["verification"] in {"incorrect", "uncertain"}]
    return {
        "phase": phase,
        "total_samples": total,
        "verified_correct": len(verified),
        "incorrect_or_uncertain": len(rejected),
        "accuracy": len(verified) / total if total else None,
        "note": "Accuracy is based only on human verification records.",
    }


def export_report(rows: list[Any], phase: str) -> tuple[Path, Path]:
    REPORTS.mkdir(parents=True, exist_ok=True)
    report = build_report(rows, phase)
    json_path = REPORTS / f"{phase}_report.json"
    csv_path = REPORTS / f"{phase}_observations.csv"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    fieldnames = ["id", "phase", "image_path", "card_name", "prediction", "verification", "created_at"]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})
    return json_path, csv_path


def export_candidate_annotations(rows: list[Any]) -> tuple[Path, Path]:
    """Export all Phase 1 candidate records, including unreviewed samples."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS / "phase1_candidate_annotations.json"
    csv_path = REPORTS / "phase1_candidate_metrics.csv"
    records = []
    for row in rows:
        record = dict(row)
        record["corners"] = json.loads(record.pop("corners_json"))
        record["metrics"] = json.loads(record.pop("metrics_json"))
        records.append(record)
    json_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    fieldnames = [
        "id", "session_id", "candidate_id", "frame_path", "crop_path", "detection_method",
        "timestamp", "tracking_status", "judgment",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow({field: row.get(field) for field in fieldnames})
    return json_path, csv_path


def export_phase1_audit(report: dict[str, Any]) -> Path:
    """Write a read-only Phase 1 dataset/generation audit result."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / "phase1_ground_truth_audit.json"
    path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    return path


def export_phase1_audit_visuals(report: dict[str, Any]) -> None:
    """Persist read-only overlays for failures and internal-region examples."""
    output = REPORTS / "phase1_audit_overlays"
    output.mkdir(parents=True, exist_ok=True)
    for case in report.get("generation", {}).get("cases", []):
        if not case.get("failure") and not case.get("internal_candidates"):
            continue
        image = cv2.imread(str(case["frame_path"]))
        if image is None:
            continue
        overlay = image.copy()
        polygons = (
            (case.get("ground_truth_points"), (70, 220, 90)),
            (case.get("best_candidate_points"), (60, 80, 235)),
            (case.get("top_candidate_points"), (235, 160, 50)),
        )
        for points, color in polygons:
            if points:
                cv2.polylines(overlay, [np.int32(points)], True, color, 3)
        for internal in case.get("internal_candidates", []):
            cv2.polylines(
                overlay, [np.int32(internal["points"])], True, (205, 80, 220), 3
            )
        path = output / f"record_{case['id']}_overlay.png"
        if cv2.imwrite(str(path), overlay):
            case["overlay_path"] = str(path)
