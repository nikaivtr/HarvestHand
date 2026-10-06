# ============================================================
#  Card Model
#
#  "Training" here is deliberately simple and inspectable:
#
#    1. every sample photo -> a feature vector (features.py)
#    2. each card -> the average of its vectors (its centroid)
#    3. a live frame is compared to every centroid
#
#  There is no gradient descent, no pickle and no numpy, so the
#  trained model is a small JSON file you can open, read and
#  hand-edit. For four to seven visually distinct cards this
#  beats a neural network: it trains in under a second, runs in
#  microseconds on a Raspberry Pi, and never surprises you.
#
#  To teach it a card, drop photos in data/card_samples/<slug>/
#  and run:  python tools/train_cards.py
# ============================================================

import json
import os

import cardscan.features as features
import cardscan.registry as registry


MODEL_PATH  = "card_model.json"          # inside cardscan/
SAMPLES_DIR = "data/card_samples"

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

# Below this, a match is not trusted. Calibrated by
# tools/train_cards.py --report against your own samples.
DEFAULT_THRESHOLD = 0.86

# How much better the winner must be than the runner-up. A close
# second place means the card is genuinely ambiguous (two similar
# cards, or a bad angle) and we would rather keep scanning.
DEFAULT_MARGIN = 0.04

# Warn below this many samples per card when training.
MIN_SAMPLES = 5


def _model_file():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH)


def _samples_root(root=None):
    return root or os.path.join("data", "card_samples")


def sample_dirs(root=None):
    """card slug -> directory, for every catalog card that has a folder."""
    base = _samples_root(root)
    found = {}
    for card in registry.all_cards():
        path = os.path.join(base, card.slug)
        if os.path.isdir(path):
            found[card.slug] = path
    return found


def find_samples(slug, root=None):
    """Sorted list of sample image paths for one card."""
    path = os.path.join(_samples_root(root), slug)
    if not os.path.isdir(path):
        return []
    return [
        os.path.join(path, name)
        for name in sorted(os.listdir(path))
        if name.lower().endswith(IMAGE_EXTS)
    ]


# ── Distance ────────────────────────────────────────────────

def similarity(a, b):
    """Cosine similarity of two feature vectors, 0.0 - 1.0.

    Cosine is used rather than raw distance because the vectors
    are non-negative and only their shape matters, not magnitude.
    """
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
    """Component-wise mean, then re-normalised so magnitude is 1."""
    n = len(vectors[0])
    out = [0.0] * n
    for v in vectors:
        for i in range(n):
            out[i] += v[i]
    for i in range(n):
        out[i] /= len(vectors)
    mag = sum(x * x for x in out) ** 0.5
    return [x / mag for x in out] if mag > 0.0 else out



# ── Training ────────────────────────────────────────────────

def build_model(root=None, verbose=True):
    """Scan the sample folders and return a model dict."""
    cards = {}
    problems = []

    for slug, path in sorted(sample_dirs(root).items()):
        files = find_samples(slug, root)
        if not files:
            problems.append(f"{slug}: folder exists but holds no images")
            continue

        vectors = []
        skipped = 0
        for f in files:
            vec = features.extract(features.load_image(f))
            if vec is None:
                skipped += 1
                continue
            vectors.append(vec)

        if not vectors:
            problems.append(f"{slug}: none of {len(files)} images could be read")
            continue

        cards[slug] = _mean(vectors)
        if verbose:
            note = f"  {slug:<10} {len(vectors):>3} samples"
            if skipped:
                note += f"  ({skipped} unreadable)"
            if len(vectors) < MIN_SAMPLES:
                note += f"  <- thin, want {MIN_SAMPLES}+"
            print(note)

    if not cards:
        problems.append(
            "no usable samples found - put photos in "
            f"{os.path.join(_samples_root(root), '<card-slug>')}"
        )

    return {
        "version": 1,
        "grid": features.GRID,
        "crop": features.CROP,
        "threshold": DEFAULT_THRESHOLD,
        "margin": DEFAULT_MARGIN,
        "cards": cards,
    }


def save_model(model, path=None):
    path = path or _model_file()
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(model, fh, indent=1)
    return path


def load_model(path=None):
    """Load a trained model. Returns None if it is missing or unusable."""
    try:
        with open(path or _model_file(), "r", encoding="utf-8") as fh:
            model = json.load(fh)
    except (FileNotFoundError, OSError, ValueError):
        return None
    if not isinstance(model, dict) or not model.get("cards"):
        return None
    return model


def is_trained(path=None):
    return load_model(path) is not None


# ── Matching ────────────────────────────────────────────────

def match(model, vector):
    """Rank every known card against a frame's feature vector.

    Returns (best_slug, best_score, runner_up_slug, runner_up_score),
    or (None, 0.0, None, 0.0) if the model is empty.
    """
    if not model or not vector or not model.get("cards"):
        return None, 0.0, None, 0.0

    scored = []
    for slug, centroid in model["cards"].items():
        if len(centroid) != len(vector):
            continue                       # stale model vs different grid
        scored.append((similarity(vector, centroid), slug))
    if not scored:
        return None, 0.0, None, 0.0

    scored.sort(reverse=True)
    top_s, top_c = scored[0]
    run_s, run_c = scored[1] if len(scored) > 1 else (0.0, None)
    return top_c, top_s, run_c, run_s


def classify(model, vector, threshold=None, margin=None):
    """Decide whether a frame is a confident, unambiguous card.

    Returns (slug, score, confident). `confident` is False if the
    best score is below the threshold or too close to the runner-up.
    The scanner treats a non-confident result as "keep scanning"
    rather than as a wrong card, so a hand hovering at the edge of
    frame never counts as a mistake.
    """
    slug, score, _runner, runner = match(model, vector)
    if slug is None:
        return None, 0.0, False

    thr = model.get("threshold", DEFAULT_THRESHOLD) if threshold is None else threshold
    mrg = model.get("margin", DEFAULT_MARGIN) if margin is None else margin
    return slug, score, score >= thr and (score - runner) >= mrg
