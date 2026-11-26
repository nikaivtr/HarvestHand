"""Transparent closed-set recognition tests for Recognition Lab materials."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import os
import sys
from pathlib import Path

from recognition_lab.engines import (
    compare_images,
    detect_boundary_candidates,
    perspective_crop,
    read_image,
)
from recognition_lab.paths import REPORTS


RECOGNITION_REPORT = REPORTS / "recognition_test_pechay_monggo.json"
KNOWN_LABELS = {
    "ba76a831528f_1.png": "Pechay",
    "aa88005d9933_2.png": "Monggo",
}
TARGET_LABELS = {"Pechay", "Monggo"}
PLANT_LABELS = {
    "pechay_plant": "Pechay",
    "monggo_plant": "Monggo",
    "okra_plant": "Okra",
    "squash_plant": "Kalabasa",
    "tomato_plant": "Kamatis",
    "eggplant_plant": "Talong",
    "sweet_potato_plant": "Kamote",
    "rice_plant": "Palay",
}
TARGET_LABELS = set(PLANT_LABELS.values())


def _orb_template_matches(query: np.ndarray) -> list[dict[str, Any]]:
    """Match a normalized candidate against known card-design PNG files."""
    if query is None or query.ndim != 3:
        return []

    query_gray = cv2.cvtColor(query, cv2.COLOR_BGR2GRAY)
    query_gray = cv2.resize(query_gray, (640, 900), interpolation=cv2.INTER_AREA)
    orb = cv2.ORB_create(nfeatures=2000)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    query_kp, query_descriptors = orb.detectAndCompute(query_gray, None)
    if query_descriptors is None or not query_kp:
        return []

    repository_root = Path(__file__).resolve().parents[1]
    templates = (
        ("pechay_plant", "Pechay.png"),
        ("monggo_plant", "Monggo.png"),
        ("okra_plant", "Okra.png"),
        ("squash_plant", "Kalabasa.png"),
        ("tomato_plant", "Kamatis.png"),
        ("eggplant_plant", "Talong.png"),
        ("sweet_potato_plant", "Kamote.png"),
        ("rice_plant", "Palay.png"),
    )
    matches = []
    for slug, filename in templates:
        path = repository_root / "data" / "card_samples" / slug / filename
        if not path.is_file():
            continue
        template = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if template is None:
            continue
        template = cv2.resize(template, (640, 900), interpolation=cv2.INTER_AREA)
        _, template_descriptors = orb.detectAndCompute(template, None)
        if template_descriptors is None:
            continue
        pairs = matcher.knnMatch(query_descriptors, template_descriptors, k=2)
        good = [
            pair[0]
            for pair in pairs
            if len(pair) == 2
            and pair[0].distance < 0.75 * pair[1].distance
        ]
        normalized = len(good) / max(1, len(query_kp))
        matches.append({
            "slug": slug,
            "label": PLANT_LABELS[slug],
            "good_matches": len(good),
            "score": normalized,
        })
    return sorted(matches, key=lambda item: item["score"], reverse=True)


def _claude_experimental_model_path() -> Path:
    repository_root = Path(__file__).resolve().parents[1]
    return repository_root / "card_model_card_plants_no_corn_cassava_experimental.json"


def _load_claude_cardscan():
    model_path = _claude_experimental_model_path()
    if not model_path.is_file():
        return None

    claude_root = os.environ.get(
        "HARVESTHAND_CLAUDESCAN_ROOT",
        r"D:\CardScan-Claude",
    )
    claude_path = Path(claude_root)
    if not claude_path.is_dir():
        return None

    for name in list(sys.modules):
        if name == "cardscan" or name.startswith("cardscan."):
            del sys.modules[name]
    sys.path.insert(0, str(claude_path))

    try:
        import cardscan.features as features
        import cardscan.model as card_model
    except (ImportError, ModuleNotFoundError):
        return None

    loaded = card_model.load_model(str(model_path))
    if loaded is None:
        return None
    return features, card_model, loaded


def _recognize_claude_frame(frame: np.ndarray) -> dict[str, Any] | None:
    """Use the Claude v13 mean-centered model for live plant recognition."""
    claude = _load_claude_cardscan()
    if claude is None:
        return None

    import pygame

    features, card_model, model_data = claude
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    surface = pygame.image.frombuffer(
        rgb.tobytes(), (frame.shape[1], frame.shape[0]), "RGB",
    )
    import cardscan.preprocess as preprocess

    candidates = preprocess.prepare_candidates(
        surface, max_candidates=3, fallback="guide",
    )
    best = None
    for canvas, details in candidates:
        views = [canvas]
        if features and hasattr(pygame.transform, "rotate"):
            views.append(pygame.transform.rotate(canvas, 180))
        for view in views:
            vector = features.extract_card(view)
            if vector is None:
                continue
            match = card_model.match_detailed(model_data, vector)
            if match is None:
                continue
            confident = (
                match["best_score"] >= model_data["threshold"]
                and match["gap"] >= model_data["margin"]
            )
            rank = (confident, match["best_score"], match["gap"])
            if best is None or rank > best[0]:
                best = (
                    rank,
                    match,
                    details,
                )

    if best is None:
        return None

    rank, match, details = best
    confident, score, margin = rank
    prediction_slug = match["best_slug"]
    runner_slug = match["runner_slug"]
    runner_up = PLANT_LABELS.get(runner_slug, runner_slug)
    points = details.get("points")
    top_prediction = PLANT_LABELS.get(prediction_slug, prediction_slug)
    prediction = top_prediction if confident else None
    return {
        "prediction": prediction,
        "reference_id": prediction_slug if confident else None,
        "score": score,
        "runner_up": runner_up,
        "margin": margin,
        "candidate_count": len(candidates),
        "input_mode": details.get("source", "detected"),
        "engine": "CardScan-Claude v13 mean-centered model",
        "points": points,
        "initial_prediction": top_prediction,
        "initial_score": score,
        "cross_examined": False,
        "target_scores": [
            {
                "label": PLANT_LABELS.get(slug, slug),
                "slug": slug,
                "combined": item_score,
            }
            for item_score, slug in match["ranking"]
        ],
        "ranked": match["ranking"],
        "confident": confident,
        "message": (
            "Claude v13 model: confident prediction."
            if confident
            else "Claude v13 model: prediction is below confidence thresholds."
        ),
    }


def _recognize_harvesthand_frame(frame: np.ndarray) -> dict[str, Any] | None:
    """Use the original HarvestHand v12 mean-similarity model."""
    model_path = (
        Path(__file__).resolve().parents[1]
        / "card_model_card_plants_mean_centered_v13_experimental.json"
    )
    if not model_path.is_file():
        return None

    for name in list(sys.modules):
        if name == "cardscan" or name.startswith("cardscan."):
            del sys.modules[name]
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

    try:
        import cardscan.features as features
        import cardscan.model as card_model
        import cardscan.preprocess as preprocess
        import pygame
    except (ImportError, ModuleNotFoundError):
        return None

    model_data = card_model.load_model(str(model_path))
    if model_data is None:
        return None

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    surface = pygame.image.frombuffer(
        rgb.tobytes(), (frame.shape[1], frame.shape[0]), "RGB",
    )

    candidates = preprocess.prepare_candidates(
        surface,
        max_candidates=3,
        fallback=None,
    )
    match = None
    selected_details = None
    template_match = None
    for canvas, details in candidates:
        views = [canvas]
        views.append(pygame.transform.rotate(canvas, 180))
        for view in views:
            vector = features.extract_card(view)
            if vector is None:
                continue
            candidate = card_model.match_detailed(model_data, vector)
            if candidate is None:
                continue

            raw_rgb = pygame.image.tobytes(view, "RGB")
            raw_bgr = cv2.cvtColor(
                np.frombuffer(raw_rgb, dtype=np.uint8).reshape(
                    view.get_height(), view.get_width(), 3
                ),
                cv2.COLOR_RGB2BGR,
            )
            current_templates = _orb_template_matches(raw_bgr)
            if current_templates:
                top_template = current_templates[0]
                runner_template = (
                    current_templates[1]
                    if len(current_templates) > 1
                    else {"score": 0.0}
                )
                template_separation = (
                    top_template["score"] - runner_template["score"]
                )
                if (
                    top_template["score"] >= 0.20
                    and template_separation >= 0.08
                ):
                    top_template_copy = dict(top_template)
                    top_template_copy["separation"] = template_separation
                else:
                    top_template_copy = None
            else:
                top_template_copy = None

            candidate_confident = (
                candidate["best_score"] >= model_data["threshold"]
                and candidate["gap"] >= model_data["margin"]
            )
            if top_template_copy is not None:
                candidate_confident = True
            rank = (
                candidate_confident,
                candidate["best_score"],
                candidate["gap"],
            )
            if match is None or rank > match[0]:
                match = (rank, candidate)
                selected_details = details
                template_match = top_template_copy
        if match is not None and match[0][0]:
            break

    if match is None:
        return None

    rank, candidate = match
    details = selected_details or {}
    source = details.get("source", "detected")
    points = details.get("points")
    confident, score, margin = rank
    top_slug = candidate["best_slug"]
    top_prediction = PLANT_LABELS.get(top_slug, top_slug)
    if template_match is not None:
        top_slug = template_match["slug"]
        top_prediction = template_match["label"]
        confident = True
    runner_slug = candidate["runner_slug"]
    prediction = top_prediction if confident else None
    return {
        "prediction": prediction,
        "reference_id": top_slug if confident else None,
        "score": score,
        "runner_up": PLANT_LABELS.get(runner_slug, runner_slug),
        "margin": margin,
        "candidate_count": len(candidates),
        "input_mode": source,
        "engine": "HarvestHand CardScan v13 model",
        "points": points,
        "initial_prediction": top_prediction,
        "initial_score": score,
        "cross_examined": False,
        "target_scores": [
            {
                "label": PLANT_LABELS.get(slug, slug),
                "slug": slug,
                "combined": item_score,
            }
            for item_score, slug in candidate["ranking"]
        ],
        "ranked": candidate["ranking"],
        "confident": confident,
        "message": (
            "HarvestHand CardScan v13 model: confident prediction."
            if confident
            else "HarvestHand CardScan v13 model: prediction is below confidence thresholds."
        ),
    }


def _label(row: Any) -> str:
    path = Path(str(row["path"]))
    return str(row["card_name"] or KNOWN_LABELS.get(path.name, path.stem))


def _variants(image: np.ndarray) -> list[tuple[str, np.ndarray]]:
    height, width = image.shape[:2]
    source = np.float32([
        [0, 0], [width - 1, 0],
        [width - 1, height - 1], [0, height - 1],
    ])
    destination = np.float32([
        [8, 5], [width - 12, 0],
        [width - 1, height - 8], [3, height - 1],
    ])
    perspective = cv2.warpPerspective(
        image, cv2.getPerspectiveTransform(source, destination), (width, height),
    )
    brighter = cv2.convertScaleAbs(image, alpha=1.05, beta=8)
    return [
        ("mild_perspective", perspective),
        ("mild_brightness", brighter),
    ]


def run_recognition_test(rows: list[Any]) -> dict[str, Any]:
    """Run a reproducible closed-set test without training or changing data."""
    references = []
    loaded: list[tuple[dict[str, Any], np.ndarray]] = []
    for row in rows:
        path = Path(str(row["path"]))
        try:
            image = read_image(path)
        except ValueError as error:
            references.append({
                "label": _label(row), "path": str(path), "error": str(error),
            })
            continue
        item = {
            "id": int(row["id"]),
            "label": _label(row),
            "path": str(path),
            "width": int(image.shape[1]),
            "height": int(image.shape[0]),
        }
        references.append(item)
        loaded.append((item, image))

    tests = []
    for target, image in loaded:
        for variant_name, query in _variants(image):
            scores = []
            for reference, reference_image in loaded:
                scores.append({
                    "reference_id": reference["id"],
                    "label": reference["label"],
                    **compare_images(query, reference_image),
                })
            ranked = sorted(scores, key=lambda item: item["combined"], reverse=True)
            prediction = ranked[0] if ranked else None
            tests.append({
                "target_id": target["id"],
                "target_label": target["label"],
                "variant": variant_name,
                "predicted_id": prediction["reference_id"] if prediction else None,
                "predicted_label": prediction["label"] if prediction else None,
                "correct": bool(prediction and prediction["reference_id"] == target["id"]),
                "top_score": prediction["combined"] if prediction else None,
                "runner_up_score": ranked[1]["combined"] if len(ranked) > 1 else None,
                "margin": (
                    prediction["combined"] - ranked[1]["combined"]
                    if len(ranked) > 1 else None
                ),
                "ranked_scores": ranked,
            })

    def summary_for(label: str) -> dict[str, Any]:
        selected = [item for item in tests if item["target_label"] == label]
        correct = sum(item["correct"] for item in selected)
        return {
            "tests": len(selected),
            "correct_top1": correct,
            "top1_accuracy": correct / len(selected) if selected else None,
            "average_top_score": (
                sum(item["top_score"] for item in selected if item["top_score"] is not None)
                / len(selected)
                if selected else None
            ),
        }

    labels = sorted({item["label"] for item, _ in loaded})
    correct = sum(item["correct"] for item in tests)
    report = {
        "test": "Pechay and Monggo Recognition Lab closed-set test",
        "references": references,
        "reference_count": len(loaded),
        "target_cards": {
            "Pechay": summary_for("Pechay"),
            "Monggo": summary_for("Monggo"),
        },
        "overall": {
            "labels": labels,
            "tests": len(tests),
            "correct_top1": correct,
            "top1_accuracy": correct / len(tests) if tests else None,
        },
        "tests": tests,
        "interpretation": {
            "data_improvement_proven": False,
            "reason": (
                "No independent unseen camera query set or prior Pechay/Monggo "
                "recognition result is available for a before/after comparison."
            ),
            "test_type": (
                "Closed-set reference matching with mild deterministic perspective "
                "and brightness transformations."
            ),
            "not_proven": [
                "Unseen physical-camera recognition",
                "Recognition under lighting/background changes",
                "Open-set rejection of unrelated cards or objects",
                "Generalization beyond the stored references",
            ],
        },
    }
    return report


def export_recognition_report(report: dict[str, Any]) -> Path:
    RECOGNITION_REPORT.write_text(
        json.dumps(report, indent=2), encoding="utf-8",
    )
    return RECOGNITION_REPORT


def recognize_camera_frame(frame: np.ndarray, rows: list[Any]) -> dict[str, Any]:
    """Recognize one camera frame using the existing geometric crop and matcher."""
    engine = os.environ.get("HARVESTHAND_LAB_ENGINE", "own").strip().lower()
    if engine == "claude":
        claude_result = _recognize_claude_frame(frame)
        if claude_result is not None:
            return claude_result
    else:
        own_result = _recognize_harvesthand_frame(frame)
        if own_result is not None:
            return own_result

    references = []
    for row in rows:
        try:
            references.append({
                "id": int(row["id"]),
                "label": _label(row),
                "image": read_image(Path(str(row["path"]))),
            })
        except (KeyError, OSError, ValueError):
            continue

    candidates = detect_boundary_candidates(frame, max_candidates=12)
    queries: list[tuple[str, np.ndarray, list[list[float]] | None]] = []
    for candidate in candidates:
        points = candidate["points"]
        queries.append((
            "boundary_candidate",
            perspective_crop(frame, points.tolist(), size=(640, 900)),
            points.tolist(),
        ))

    if not queries:
        height, width = frame.shape[:2]
        crop_height = int(height * 0.85)
        crop_width = min(int(crop_height * 0.71), int(width * 0.85))
        left = max(0, (width - crop_width) // 2)
        top = max(0, (height - crop_height) // 2)
        queries.append((
            "center_fallback",
            frame[top:top + crop_height, left:left + crop_width],
            None,
        ))

    ranked_queries = []
    for input_mode, query, points in queries:
        ranked = sorted(
            (
                {
                    "reference_id": reference["id"],
                    "label": reference["label"],
                    **compare_images(query, reference["image"]),
                }
                for reference in references
            ),
            key=lambda item: item["combined"],
            reverse=True,
        )
        if ranked:
            ranked_queries.append({
                "input_mode": input_mode,
                "points": points,
                "ranked": ranked,
            })

    if not ranked_queries:
        return {
            "prediction": None,
            "candidate_count": len(candidates),
            "input_mode": "unavailable",
            "engine": "Recognition Lab compare_images",
            "message": "No readable references are available.",
        }

    best_query = max(ranked_queries, key=lambda item: item["ranked"][0]["combined"])
    all_ranked = best_query["ranked"]
    best = all_ranked[0]
    target_ranked = [item for item in all_ranked if item["label"] in TARGET_LABELS]
    target_best = target_ranked[0] if target_ranked else None
    cross_examined = best["label"] not in TARGET_LABELS
    selected = target_best if cross_examined else best
    runner_up = (
        target_ranked[1] if cross_examined and len(target_ranked) > 1
        else all_ranked[1] if len(all_ranked) > 1 else None
    )
    return {
        "prediction": selected["label"] if selected else None,
        "reference_id": selected["reference_id"] if selected else None,
        "score": selected["combined"] if selected else None,
        "runner_up": runner_up["label"] if runner_up else None,
        "margin": selected["combined"] - runner_up["combined"] if runner_up else None,
        "candidate_count": len(candidates),
        "input_mode": best_query["input_mode"],
        "engine": "Recognition Lab compare_images",
        "points": best_query["points"],
        "initial_prediction": best["label"],
        "initial_score": best["combined"],
        "cross_examined": cross_examined,
        "target_scores": target_ranked,
        "ranked": all_ranked,
        "message": (
            (
                "Another reference ranked first; cross-examined against Pechay "
                "and Monggo."
            )
            if cross_examined
            else (
                "Boundary candidate used."
                if best_query["input_mode"] == "boundary_candidate"
                else "No boundary candidate; center crop fallback used."
            )
        ),
    }
