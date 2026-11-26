"""Persistence and validation for manually captured outer-card references."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from .engines import perspective_crop, validate_quad_geometry
from .paths import DATASETS


CONDITIONS = (
    ("flat_on_table", "Flat on Table"),
    ("tilted_right", "Tilted Right"),
    ("tilted_left", "Tilted Left"),
    ("held_by_hand", "Held by Hand"),
)
CONDITION_LABELS = dict(CONDITIONS)
REFERENCE_ROOT = DATASETS / "boundary_references"


def validate_annotation(
    points: Any, image_shape: tuple[int, ...],
) -> tuple[bool, list[str]]:
    """Validate manual points without changing their order or values."""
    try:
        corners = np.float32(points).reshape(4, 2)
    except (TypeError, ValueError):
        return False, ["Exactly four corners are required."]
    valid, reasons = validate_quad_geometry(
        corners, image_shape,
        min_area_ratio=0.005, max_area_ratio=0.98,
        min_aspect_ratio=0.35, max_aspect_ratio=0.95,
        max_perspective_distortion=0.80,
    )
    warnings = []
    if valid:
        # The collection accepts unusual but valid perspective; this is only advisory.
        area = abs(float(cv2.contourArea(corners)))
        if area / max(image_shape[0] * image_shape[1], 1) < 0.02:
            warnings.append("The polygon covers a small part of the frame.")
    return valid, reasons + warnings


def list_references() -> list[dict[str, Any]]:
    records = []
    for condition, _ in CONDITIONS:
        folder = REFERENCE_ROOT / condition
        for metadata_path in sorted(folder.glob("*.json"), reverse=True):
            try:
                record = json.loads(metadata_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            record["_metadata_path"] = str(metadata_path)
            records.append(record)
    return sorted(records, key=lambda item: item.get("timestamp", ""), reverse=True)


def save_reference(
    image: np.ndarray,
    points: list[list[float]],
    condition: str,
    session_id: str,
    visibility: str,
    notes: str = "",
    verified: bool = True,
    sample_id: str | None = None,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Save an original frame and JSON metadata, preserving the original image."""
    if condition not in CONDITION_LABELS:
        raise ValueError(f"Unknown capture condition: {condition}")
    valid, reasons = validate_annotation(points, image.shape)
    if not valid:
        raise ValueError("; ".join(reasons))
    sample_id = sample_id or f"boundary-{uuid.uuid4().hex}"
    folder = REFERENCE_ROOT / condition
    folder.mkdir(parents=True, exist_ok=True)
    if existing:
        image_path = Path(existing["image_path"])
        metadata_path = Path(existing["_metadata_path"])
        crop_path = Path(existing.get("rectified_crop_path", ""))
    else:
        stem = sample_id
        image_path = folder / f"{stem}.png"
        metadata_path = folder / f"{stem}.json"
        crop_path = folder / f"{stem}_rectified.png"
        if image_path.exists() or metadata_path.exists():
            raise FileExistsError(f"Reference sample already exists: {sample_id}")
        if not cv2.imwrite(str(image_path), image):
            raise OSError(f"Could not save original image: {image_path}")
    if existing and not image_path.exists():
        raise OSError(f"Original reference image is missing: {image_path}")
    crop = perspective_crop(image, points, size=(350, 490))
    if not cv2.imwrite(str(crop_path), crop):
        raise OSError(f"Could not save derived crop: {crop_path}")
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    record = {
        "sample_id": sample_id,
        "image_path": str(image_path),
        "rectified_crop_path": str(crop_path),
        "corners": [[float(x), float(y)] for x, y in points],
        "capture_condition": condition,
        "capture_condition_label": CONDITION_LABELS[condition],
        "image_width": int(image.shape[1]),
        "image_height": int(image.shape[0]),
        "timestamp": timestamp,
        "session_id": session_id,
        "annotation_status": "manually_annotated",
        "visibility_status": visibility,
        "notes": notes.strip(),
        "manually_verified": bool(verified),
        "validation_warnings": reasons,
        "ground_truth_source": "human_outer_boundary_annotation",
    }
    temporary = metadata_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(record, indent=2), encoding="utf-8")
    temporary.replace(metadata_path)
    record["_metadata_path"] = str(metadata_path)
    return record

