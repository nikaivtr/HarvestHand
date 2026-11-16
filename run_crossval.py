#!/usr/bin/env python3
"""Leave-one-out validation for the Pechay and Monggo card samples."""

import argparse
import csv
import os
import statistics
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

import cardscan.features as features
import cardscan.model as model
import cardscan.preprocess as preprocess


PROD_THRESHOLD = model.DEFAULT_THRESHOLD
PROD_MARGIN = model.DEFAULT_MARGIN
CLASSES = ("pechay_plant", "monggo_plant")
METHODS = ("full_card", "illustration_only", "combined")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
OUTPUT_CSV = "crossval_results.csv"


def load_dataset(base):
    dataset = {}
    for slug in CLASSES:
        folder = os.path.join(base, slug)
        if not os.path.isdir(folder):
            continue
        dataset[slug] = [
            os.path.join(folder, name)
            for name in sorted(os.listdir(folder))
            if name.lower().endswith(IMAGE_EXTS)
        ]
    return dataset


def extract_direct(surface):
    """Extract features from an already prepared surface.

    This is the same computation as ``features.extract`` after its call to
    ``preprocess.prepare``. It exists so the illustration crop is not
    preprocessed a second time.
    """
    if surface is None:
        return None
    small = pygame.transform.smoothscale(surface, (features.GRID, features.GRID))
    width, height = small.get_size()
    raw = pygame.image.tobytes(small, "RGB")
    colour = [0.0] * (width * height * 3)
    lumas = [0.0] * (width * height)
    for y in range(height):
        for x in range(width):
            i = y * width + x
            c = i * 3
            red, green, blue = raw[c], raw[c + 1], raw[c + 2]
            lum = features._LR * red + features._LG * green + features._LB * blue
            if lum > 18.0:
                red_n, green_n, blue_n = red / 255.0, green / 255.0, blue / 255.0
                maximum = max(red_n, green_n, blue_n)
                minimum = min(red_n, green_n, blue_n)
                delta = maximum - minimum
                if maximum == minimum:
                    hue = 0.0
                elif maximum == red_n:
                    hue = (60.0 * ((green_n - blue_n) / delta) + 360.0) % 360.0
                elif maximum == green_n:
                    hue = (60.0 * ((blue_n - red_n) / delta) + 120.0) % 360.0
                else:
                    hue = (60.0 * ((red_n - green_n) / delta) + 240.0) % 360.0
                colour[c] = hue / 360.0
                colour[c + 1] = 0.0 if maximum == 0.0 else delta / maximum
                colour[c + 2] = maximum
            lumas[i] = lum / 255.0

    edge = [0.0] * (width * height)
    for y in range(height):
        for x in range(width):
            i = y * width + x
            gx = lumas[i + 1] - lumas[i - 1] if 0 < x < width - 1 else 0.0
            gy = lumas[i + width] - lumas[i - width] if 0 < y < height - 1 else 0.0
            edge[i] = min((gx * gx + gy * gy) ** 0.5, 1.0) * features.EDGE_WEIGHT

    weights = features._build_weight_map(width, height)
    vector = []
    for y in range(height):
        for x in range(width):
            i = y * width + x
            c = i * 3
            weight = weights[y][x]
            vector.extend((
                colour[c] * weight,
                colour[c + 1] * weight,
                colour[c + 2] * weight,
                edge[i] * weight,
            ))
    return vector


def extract_illustration(card_surface):
    if card_surface is None:
        return None
    width, height = card_surface.get_size()
    top, bottom = features.ILLUSTRATION_BAND
    y_start = int(height * top)
    y_end = int(height * bottom)
    if y_end <= y_start:
        return None
    crop = card_surface.subsurface(
        pygame.Rect(0, y_start, width, y_end - y_start)
    ).copy()
    return extract_direct(crop)


def verify_extractor(path):
    """Load and prepare one image, returning all three method vectors."""
    raw = preprocess.load_image(path)
    prepared = preprocess.prepare(raw)
    if prepared is None:
        return None
    full = extract_direct(prepared)
    illustration = extract_illustration(prepared)
    if full is None or illustration is None:
        return None
    verified = {
        "full_card": full,
        "illustration_only": illustration,
        "combined": full + illustration,
    }
    expected = features.GRID * features.GRID * 4
    if len(full) != expected or len(illustration) != expected:
        raise ValueError("unexpected feature vector length for %s" % path)
    return verified


def _fold_model(training, method):
    cards = {}
    for slug in CLASSES:
        vectors = [sample["vectors"][method] for sample in training
                   if sample["actual"] == slug]
        if vectors:
            cards[slug] = {
                "centroid": model._mean(vectors),
                "samples": vectors,
                "n": len(vectors),
            }
    return {"cards": cards}


def run_loocv(samples):
    results = []
    for test_index, test in enumerate(samples, 1):
        training = samples[:test_index - 1] + samples[test_index:]
        for method in METHODS:
            fold_model = _fold_model(training, method)
            detail = model.classify_detailed(
                fold_model,
                test["vectors"][method],
                threshold=PROD_THRESHOLD,
                margin=PROD_MARGIN,
            )
            results.append({
                "fold": test_index,
                "path": test["path"],
                "method": method,
                "actual": test["actual"],
                "predicted": detail["best_slug"] or "",
                "score": detail["best_score"],
                "runner_slug": detail["runner_slug"] or "",
                "runner_score": detail["runner_score"],
                "gap": detail["gap"],
                "accepted": detail["confident"],
                "reason": detail["reason"],
            })
    return results


def analyze_method(results, method):
    rows = [row for row in results if row["method"] == method]
    correct = [row for row in rows if row["predicted"] == row["actual"]]
    accepted = [row for row in rows if row["accepted"]]
    rejected = [row for row in rows if not row["accepted"]]
    false_accepts = [row for row in accepted if row["predicted"] != row["actual"]]
    gaps = [float(row["gap"]) for row in rows]
    return {
        "rows": rows,
        "raw_correct": len(correct),
        "raw_accuracy": len(correct) / len(rows) if rows else 0.0,
        "accepted": accepted,
        "rejected": rejected,
        "false_accepts": false_accepts,
        "mean_gap": sum(gaps) / len(gaps) if gaps else 0.0,
        "median_gap": statistics.median(gaps) if gaps else 0.0,
        "max_gap": max(gaps) if gaps else 0.0,
        "per_class": {
            slug: (
                sum(row["predicted"] == slug for row in rows
                    if row["actual"] == slug),
                sum(row["actual"] == slug for row in rows),
            )
            for slug in CLASSES
        },
    }


def print_report(results):
    print("\n" + "=" * 70)
    print("LOOCV RESULTS")
    print("=" * 70)
    for method in METHODS:
        report = analyze_method(results, method)
        rows = report["rows"]
        print("\n--- %s ---" % method.upper())
        print("  Samples: %d" % len(rows))
        print("  Raw top-1 accuracy: %.1f%% (%d/%d)" % (
            report["raw_accuracy"] * 100, report["raw_correct"], len(rows)))
        print("  Accepted: %d" % len(report["accepted"]))
        print("  Rejected: %d" % len(report["rejected"]))
        print("  False accepts: %d" % len(report["false_accepts"]))
        print("  Mean runner-up gap: %.6f" % report["mean_gap"])
        print("  Median runner-up gap: %.6f" % report["median_gap"])
        print("  Maximum runner-up gap: %.6f" % report["max_gap"])
        for slug in CLASSES:
            correct, total = report["per_class"][slug]
            print("  %s: %.1f%% (%d/%d)" % (
                slug, correct / total * 100 if total else 0.0, correct, total))
        mistakes = [
            os.path.basename(row["path"])
            for row in rows if row["predicted"] != row["actual"]
        ]
        print("  Misclassified: %s" % (", ".join(mistakes) or "none"))


def export_csv(results, path=OUTPUT_CSV):
    fields = [
        "fold", "path", "method", "actual", "predicted", "score",
        "runner_slug", "runner_score", "gap", "accepted", "reason",
    ]
    with open(path, "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
    print("\nCSV saved to %s (%d rows)" % (path, len(results)))


def run_loocv_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--illustration-boost", type=float,
                        default=features.ILLUSTRATION_BOOST)
    parser.add_argument("--band-top", type=float,
                        default=features.ILLUSTRATION_BAND[0])
    parser.add_argument("--band-bottom", type=float,
                        default=features.ILLUSTRATION_BAND[1])
    parser.add_argument("--center-falloff", type=float,
                        default=features.CENTER_FALLOFF)
    parser.add_argument("--output", default=OUTPUT_CSV)
    args = parser.parse_args()
    if not 0.0 <= args.band_top < args.band_bottom <= 1.0:
        raise SystemExit("illustration band must satisfy 0 <= top < bottom <= 1")
    features.ILLUSTRATION_BOOST = args.illustration_boost
    features.ILLUSTRATION_BAND = (args.band_top, args.band_bottom)
    features.CENTER_FALLOFF = args.center_falloff
    dataset = load_dataset(os.path.join(_HERE, "data", "card_samples"))
    samples = []
    for slug in CLASSES:
        paths = dataset.get(slug, [])
        if args.max_samples is not None:
            paths = paths[:args.max_samples]
        for path in paths:
            vectors = verify_extractor(path)
            if vectors is None:
                print("[run_crossval] FAILED to prepare: %s" % path)
                continue
            samples.append({"actual": slug, "path": path, "vectors": vectors})
    if not samples:
        raise SystemExit("No usable Pechay/Monggo images found")
    print("HarvestHand LOOCV Cross-Validation")
    print("Feature version: %s, Grid: %s" % (
        features.PREPROCESS_VERSION, features.GRID))
    print("Threshold: %.2f, Margin: %.2f" % (PROD_THRESHOLD, PROD_MARGIN))
    print("Boost: %.2f, Band: (%.2f, %.2f), Center falloff: %.2f" % (
        features.ILLUSTRATION_BOOST, features.ILLUSTRATION_BAND[0],
        features.ILLUSTRATION_BAND[1], features.CENTER_FALLOFF))
    print("Samples: %d (%s)" % (len(samples), ", ".join(
        "%s=%d" % (slug, sum(s["actual"] == slug for s in samples))
        for slug in CLASSES)))
    results = run_loocv(samples)
    print_report(results)
    export_csv(results, args.output)


if __name__ == "__main__":
    pygame.init()
    try:
        run_loocv_main()
    finally:
        pygame.quit()
