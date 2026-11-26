"""Targeted single-class verification for chapter card unlocking."""

import json
import os

import cardscan.registry as registry


DEFAULT_FAR_LIMIT = 0.01
TOP_K = 3


def _normalize_slug(expected_card):
    if not expected_card:
        return None
    text = str(expected_card).strip().lower()
    card = registry.get(text)
    if card is not None:
        return card.slug
    card = registry.resolve(expected_card)
    if card is not None:
        return card.slug
    for slug in (
        "pechay_plant", "monggo_plant", "okra_plant", "squash_plant",
        "tomato_plant", "eggplant_plant", "sweet_potato_plant",
        "rice_plant", "corn_plant", "cassava_plant",
    ):
        if text in (slug, slug.replace("_plant", ""), text):
            return slug
    return text


def model_slug(expected_card):
    slug = _normalize_slug(expected_card)
    aliases = {
        "pechay": "pechay_plant",
        "monggo": "monggo_plant",
        "okra": "okra_plant",
        "squash": "squash_plant",
        "tomato": "tomato_plant",
        "eggplant": "eggplant_plant",
        "sweet_potato": "sweet_potato_plant",
        "rice": "rice_plant",
        "corn": "corn_plant",
        "cassava": "cassava_plant",
    }
    return aliases.get(slug, slug)


def _config_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "target_verification.json")


def load_thresholds(path=None):
    try:
        with open(path or _config_path(), "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (FileNotFoundError, OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def get_threshold(expected_card, model=None, thresholds=None):
    slug = model_slug(expected_card)
    data = thresholds if thresholds is not None else load_thresholds()
    entry = data.get("classes", {}).get(slug)
    if isinstance(entry, dict):
        return float(entry.get("threshold", 1.0))
    if model is not None:
        card = model.get("cards", {}).get(slug)
        if card:
            return float(card.get("verification_threshold", 1.0))
    return 1.0


def verify(model, vector, expected_card, threshold=None, top_k=TOP_K):
    """Verify a mean-centered live vector against only the expected class."""
    import cardscan.model as model_module

    slug = model_slug(expected_card)
    entry = (model or {}).get("cards", {}).get(slug)
    if entry is None:
        return {
            "slug": slug,
            "score": 0.0,
            "threshold": 1.0,
            "accepted": False,
            "reason": "expected class missing from model",
        }
    centered = model_module._center(model, vector)
    samples = entry.get("samples") or [entry.get("centroid")]
    if not samples or len(samples[0]) != len(centered):
        return {
            "slug": slug,
            "score": 0.0,
            "threshold": 1.0,
            "accepted": False,
            "reason": "feature vector incompatible",
        }
    score = model_module._class_score(samples, centered, top_k=top_k)
    required = get_threshold(slug, model) if threshold is None else float(threshold)
    accepted = score >= required
    return {
        "slug": slug,
        "score": score,
        "threshold": required,
        "accepted": accepted,
        "reason": "target match" if accepted else "below targeted threshold",
    }
