# Card Model
#
# Training is deliberate and inspectable:
#
#   1. every sample photo -> a feature vector (features.py)
#   2. each card -> its sample vectors plus a centroid
#   3. a live frame is compared to every class using nearest-sample
#      scoring (top-k average similarity to that class\'s samples)
#
# There is no gradient descent, no pickle and no numpy, so the trained
# model is a small JSON file you can open, read and hand-edit. It
# trains in under a second and runs in microseconds on a Raspberry Pi.
#
# To teach it a card, drop photos in data/card_samples/<slug>/
# and run:  python tools/train_cards.py
#
# Model versions: bump feature_version in features.py / preprocess.py
# whenever preprocessing changes; load_model() rejects stale models.
#

import json
import os

import cardscan.features as features
import cardscan.registry as registry


MODEL_PATH  = "card_model.json"          # inside cardscan/
SAMPLES_DIR = "data/card_samples"

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

DEFAULT_THRESHOLD = 0.80
DEFAULT_MARGIN = 0.07
MIN_SAMPLES = 5
TOP_K = 3
MODEL_VERSION = 2


def _model_file():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH)


def _samples_root(root=None):
    return root or os.path.join("data", "card_samples")


def sample_dirs(root=None):
    base = _samples_root(root)
    found = {}
    for card in registry.all_cards():
        path = os.path.join(base, card.sample_folder)
        if os.path.isdir(path):
            found[card.slug] = path
    return found


def find_samples(slug, root=None):
    card = registry.get(slug)
    if card is None:
        return []
    path = os.path.join(_samples_root(root), card.sample_folder)
    if not os.path.isdir(path):
        return []
    return [os.path.join(path, name) for name in sorted(os.listdir(path)) if name.lower().endswith(IMAGE_EXTS)]


def similarity(a, b):
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = na = nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na  += x * x
        nb  += y * y
    if na <= 0.0 or nb <= 0.0:
        return 0.0
    v = dot / ((na ** 0.5) * (nb ** 0.5))
    return 0.0 if v < 0.0 else (v if v <= 1.0 else 1.0)


def _mean(vectors):
    n = len(vectors[0])
    out = [0.0] * n
    for v in vectors:
        for i in range(n):
            out[i] += v[i]
    for i in range(n):
        out[i] /= len(vectors)
    mag = sum(x * x for x in out) ** 0.5
    if mag > 0.0:
        out = [x / mag for x in out]
    return out


def _class_score(samples, vector, top_k=TOP_K):
    if not samples:
        return 0.0
    sims = [similarity(vector, s) for s in samples]
    sims.sort(reverse=True)
    k = min(top_k, len(sims))
    return sum(sims[:k]) / k


# - Training -------------------------------------------------

def build_model(root=None, verbose=False):
    cards = {}
    problems = []
    found = sample_dirs(root)
    for slug in sorted(found):
        files = find_samples(slug, root)
        vectors = []
        skipped = 0
        for f in files:
            vec = features.extract(features.load_image(f))
            if vec is None:
                skipped += 1
                continue
            vectors.append(vec)
        if not vectors:
            problems.append(
                "%s: none of %d images could be read" % (slug, len(files)))
            continue
        cards[slug] = {
            "centroid": _mean(vectors),
            "samples": vectors,
            "n": len(vectors),
        }
        if verbose:
            note = "  %-20s %3d samples" % (slug, len(vectors))
            if skipped:
                note += "  (%d unreadable)" % skipped
            print(note)

    return {
        "version": MODEL_VERSION,
        "feature_version": features.PREPROCESS_VERSION,
        "grid": features.GRID,
        "threshold": DEFAULT_THRESHOLD,
        "margin": DEFAULT_MARGIN,
        "cards": cards,
        "problems": problems,
    }

def save_model(model, path=None):
    path = path or _model_file()
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(model, fh, indent=1)
    return path


def load_model(path=None):
    try:
        with open(path or _model_file(), "r", encoding="utf-8") as fh:
            model = json.load(fh)
    except (FileNotFoundError, OSError, ValueError):
        return None
    if (not isinstance(model, dict)
            or not model.get("cards")
            or model.get("feature_version") != features.PREPROCESS_VERSION
            or model.get("grid") != features.GRID):
        return None
    return model


def is_trained(path=None):
    return load_model(path) is not None


def _score_all(model, vector):
    scored = []
    for slug, entry in model.get("cards", {}).items():
        samples = entry.get("samples") or [entry.get("centroid")]
        if not samples:
            continue
        if len(samples[0]) != len(vector):
            continue
        scored.append((_class_score(samples, vector), slug))
    scored.sort(reverse=True)
    return scored


def match(model, vector):
    scored = _score_all(model, vector)
    if not scored:
        return None, 0.0, None, 0.0
    top_s, top_c = scored[0]
    run_s, run_c = scored[1] if len(scored) > 1 else (0.0, None)
    return top_c, top_s, run_c, run_s


def match_detailed(model, vector):
    scored = _score_all(model, vector)
    if not scored:
        return None
    top_s, top_c = scored[0]
    run_s, run_c = scored[1] if len(scored) > 1 else (0.0, None)
    return {
        "best_slug": top_c,
        "best_score": top_s,
        "runner_slug": run_c,
        "runner_score": run_s,
        "gap": top_s - run_s,
        "ranking": scored,
    }


def classify(model, vector, threshold=None, margin=None):
    slug, score, _, runner = match(model, vector)
    if slug is None:
        return None, 0.0, False
    if len(model.get("cards", {})) < 2:
        return slug, score, False
    thr = model.get("threshold", DEFAULT_THRESHOLD) if threshold is None else threshold
    mrg = model.get("margin", DEFAULT_MARGIN) if margin is None else margin
    confident = score >= thr and (score - runner) >= mrg
    return slug, score, confident


def classify_detailed(model, vector, threshold=None, margin=None):
    d = match_detailed(model, vector)
    if d is None:
        return {"slug": None, "score": 0.0, "confident": False,
                "reason": "no model", "best_slug": None,
                "best_score": 0.0, "runner_slug": None,
                "runner_score": 0.0, "gap": 0.0}
    thr = model.get("threshold", DEFAULT_THRESHOLD) if threshold is None else threshold
    mrg = model.get("margin", DEFAULT_MARGIN) if margin is None else margin
    confident = d["best_score"] >= thr and d["gap"] >= mrg
    if len(model.get("cards", {})) < 2:
        confident = False
    if not confident:
        if d["best_score"] < thr:
            reason = "below threshold"
        elif d["gap"] < mrg:
            reason = "ambiguous (runner-up too close)"
        else:
            reason = "not confident"
    else:
        reason = "match"
    return {
        "slug": d["best_slug"],
        "score": d["best_score"],
        "confident": confident,
        "reason": reason,
        "best_slug": d["best_slug"],
        "best_score": d["best_score"],
        "runner_slug": d["runner_slug"],
        "runner_score": d["runner_score"],
        "gap": d["gap"],
    }
