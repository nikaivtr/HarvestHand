#!/usr/bin/env python3
"""
HarvestHand Fixed-Threshold LOOCV Diagnostic
============================================

Compares three feature methods:
  A. Full-card features (2,304 dims)
  B. Illustration-only features (2,304 dims)
  C. Combined full-card + illustration features (4,608 dims)

Uses fixed production thresholds (0.80, 0.07).
Does NOT modify card_model.json or the production scanner.
"""

import csv
from pathlib import Path

import pygame
import cardscan.preprocess as preprocess
import cardscan.features as features
import cardscan.model as model_module
import cardscan.registry as registry


# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------
CLASSES = ("pechay_plant", "monggo_plant")
EXPECTED_COUNTS = {
    "pechay_plant": 21,
    "monggo_plant": 21,
}
THRESHOLD = 0.80
MARGIN = 0.07
GRID = features.GRID
IMAGE_EXTS = tuple(model_module.IMAGE_EXTS)
OUTPUT_CSV = "crossval_results.csv"
ILLUSTRATION_TOP = 0.25
ILLUSTRATION_BOTTOM = 0.75


# ------------------------------------------------------------
# DATASET DISCOVERY
# ------------------------------------------------------------
def get_sample_folder(card):
    folder = Path(card.sample_folder)
    if folder.is_absolute():
        return folder
    if str(folder).replace("\\", "/").startswith("data/card_samples/"):
        return folder
    return Path(model_module.SAMPLES_DIR) / folder


def discover_samples():
    samples = []
    for slug in CLASSES:
        card = registry.get(slug)
        if card is None:
            raise RuntimeError(f"Card not found in registry: {slug}")
        folder = get_sample_folder(card)
        if not folder.is_dir():
            raise RuntimeError(f"Sample folder does not exist for {slug}: {folder}")
        paths = sorted(
            path for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTS
        )
        print(f"{slug}: {len(paths)} files found in {folder}")
        for path in paths:
            samples.append({
                "slug": slug,
                "name": card.name,
                "path": path.resolve(),
            })
    return samples


# ------------------------------------------------------------
# FEATURE EXTRACTION
# ------------------------------------------------------------

def extract_direct(surface):
    """
    Extract features from an already-prepared surface.
    Mirrors features.extract() but does NOT call preprocess.prepare() again.
    """
    if surface is None:
        return None
    small = pygame.transform.smoothscale(surface, (GRID, GRID))
    width, height = small.get_size()

    raw = pygame.image.tobytes(small, "RGB")
    lumas = [0.0] * (width * height)
    colours = [0.0] * (width * height * 3)

    lr, lg, lb = 0.299, 0.587, 0.114
    for y in range(height):
        for x in range(width):
            i = y * width + x
            j = i * 3
            red = raw[j]
            green = raw[j + 1]
            blue = raw[j + 2]
            lum = lr * red + lg * green + lb * blue
            if lum > 18.0:
                colours[j] = red / 255.0
                colours[j + 1] = green / 255.0
                colours[j + 2] = blue / 255.0
            lumas[i] = lum / 255.0

    edges = [0.0] * (width * height)
    for y in range(height):
        for x in range(width):
            i = y * width + x
            gx = 0.0
            gy = 0.0
            if 0 < x < width - 1:
                gx = lumas[i + 1] - lumas[i - 1]
            if 0 < y < height - 1:
                gy = lumas[i + width] - lumas[i - width]
            magnitude = (gx * gx + gy * gy) ** 0.5
            magnitude = min(magnitude, 1.0)
            edges[i] = magnitude * features.EDGE_WEIGHT

    weights = features._build_weight_map(width, height)
    output = []
    for y in range(height):
        for x in range(width):
            i = y * width + x
            j = i * 3
            weight = weights[y][x]
            output.extend((
                colours[j] * weight,
                colours[j + 1] * weight,
                colours[j + 2] * weight,
                edges[i] * weight,
            ))
    return output


def extract_illustration(prepared_surface):
    if prepared_surface is None:
        return None
    width, height = prepared_surface.get_size()
    top = int(height * ILLUSTRATION_TOP)
    bottom = int(height * ILLUSTRATION_BOTTOM)
    crop_height = bottom - top
    if crop_height <= 0:
        return None
    rect = pygame.Rect(0, top, width, crop_height)
    illustration = prepared_surface.subsurface(rect).copy()
    return extract_direct(illustration)


def verify_extractor(path):
    raw = preprocess.load_image(str(path))
    if raw is None:
        raise RuntimeError(f"Could not load verification image: {path}")
    prepared = preprocess.prepare(raw)
    if prepared is None:
        raise RuntimeError(f"Could not prepare verification image: {path}")
    production_vector = features.extract(raw)
    diagnostic_vector = extract_direct(prepared)
    if len(production_vector) != len(diagnostic_vector):
        raise RuntimeError(
            f"Vector length mismatch: "
            f"{len(production_vector)} vs {len(diagnostic_vector)}"
        )
    max_difference = max(
        abs(a - b) for a, b in zip(production_vector, diagnostic_vector)
    )
    print(f"  {path}: max difference = {max_difference:.10f}")
    if max_difference > 1e-7:
        raise RuntimeError(
            "Diagnostic extractor differs from production extractor. "
            "Do not trust the LOOCV results until this is fixed."
        )


def extract_all_features(path):
    try:
        raw_surface = preprocess.load_image(str(path))
        if raw_surface is None:
            return None

        prepared = preprocess.prepare(raw_surface)
        if prepared is None:
            return None

        full_vector = extract_direct(prepared)
        illustration_vector = extract_illustration(prepared)

        if full_vector is None or illustration_vector is None:
            return None

        return {
            "full_card": full_vector,
            "illustration_only": illustration_vector,
            "combined": full_vector + illustration_vector,
        }
    except Exception as exc:
        print(f"  Feature extraction failed: {path} ({exc})")
        return None


# ------------------------------------------------------------
# MODEL BUILDING
# ------------------------------------------------------------

def build_fold_model(training_samples, method_key):
    vectors_by_class = {slug: [] for slug in CLASSES}
    for sample in training_samples:
        vector = sample["features"][method_key]
        vectors_by_class[sample["slug"]].append(vector)

    cards = {}
    for slug in CLASSES:
        vectors = vectors_by_class[slug]
        if not vectors:
            raise RuntimeError(f"No training vectors for {slug} in this fold.")
        cards[slug] = {
            "centroid": model_module._mean(vectors),
            "samples": vectors,
            "n": len(vectors),
        }

    return {
        "version": model_module.MODEL_VERSION,
        "feature_version": features.PREPROCESS_VERSION,
        "grid": GRID,
        "threshold": THRESHOLD,
        "margin": MARGIN,
        "cards": cards,
    }


# ------------------------------------------------------------
# CLASSIFICATION AND RESULT RECORDING
# ------------------------------------------------------------

def classify_one(fold_model, vector, actual_slug, method_key, sample_path):
    detail = model_module.classify_detailed(
        fold_model,
        vector,
        threshold=THRESHOLD,
        margin=MARGIN,
    )

    return {
        "fold": sample_path.name,
        "path": str(sample_path),
        "method": method_key,
        "actual": actual_slug,
        "predicted": detail.get("best_slug"),
        "score": detail.get("best_score"),
        "runner_slug": detail.get("runner_slug"),
        "runner_score": detail.get("runner_score"),
        "gap": detail.get("gap"),
        "accepted": bool(detail.get("confident")),
        "reason": detail.get("reason"),
    }


def run_loocv(samples):
    results = []
    methods = ("full_card", "illustration_only", "combined")
    total = len(samples)

    for test_index, test_sample in enumerate(samples):
        print(f"\nFold {test_index + 1}/{total}: {test_sample['slug']}")

        training_samples = [
            sample for index, sample in enumerate(samples)
            if index != test_index
        ]

        for slug in CLASSES:
            count = sum(1 for sample in training_samples if sample["slug"] == slug)
            if count < 1:
                raise RuntimeError(
                    f"No training samples remain for {slug}."
                )

        for method_key in methods:
            fold_model = build_fold_model(training_samples, method_key)
            test_vector = test_sample["features"][method_key]

            result = classify_one(
                fold_model,
                test_vector,
                test_sample["slug"],
                method_key,
                test_sample["path"],
            )

            results.append(result)

            score = result["score"]
            score_text = f"{score:.4f}" if score is not None else "N/A"
            status = "ACCEPT" if result["accepted"] else "REJECT"
            print(
                f"  {method_key:18s} {status:6s} "
                f"predicted={str(result['predicted']):14s} score={score_text}"
            )

    return results


# ------------------------------------------------------------
# METRICS
# ------------------------------------------------------------

def safe_rate(numerator, denominator):
    return numerator / denominator if denominator else 0.0


def analyze_method(results, method_key):
    rows = [row for row in results if row["method"] == method_key]
    total = len(rows)
    accepted = [row for row in rows if row["accepted"]]
    rejected = [row for row in rows if not row["accepted"]]

    correct_raw = [row for row in rows if row["predicted"] == row["actual"]]
    correct_accepted = [
        row for row in rows
        if row["accepted"] and row["predicted"] == row["actual"]
    ]
    wrong_accepted = [
        row for row in rows
        if row["accepted"] and row["predicted"] != row["actual"]
    ]
    wrong_rejected = [
        row for row in rows
        if not row["accepted"] and row["predicted"] != row["actual"]
    ]
    correct_rejected = [
        row for row in rows
        if not row["accepted"] and row["predicted"] == row["actual"]
    ]

    gaps = [row["gap"] for row in rows if isinstance(row["gap"], (int, float))]

    summary = {
        "total": total,
        "accepted": len(accepted),
        "rejected": len(rejected),
        "correct_raw": len(correct_raw),
        "correct_accepted": len(correct_accepted),
        "wrong_accepted": len(wrong_accepted),
        "wrong_rejected": len(wrong_rejected),
        "correct_rejected": len(correct_rejected),
        "raw_accuracy": safe_rate(len(correct_raw), total),
        "coverage": safe_rate(len(accepted), total),
        "accepted_correct_rate": safe_rate(len(correct_accepted), len(accepted)),
        "false_accept_rate": safe_rate(len(wrong_accepted), total),
        "rejection_rate": safe_rate(len(rejected), total),
        "mean_gap": sum(gaps) / len(gaps) if gaps else None,
        "min_gap": min(gaps) if gaps else None,
        "max_gap": max(gaps) if gaps else None,
        "per_class": {},
    }

    for slug in CLASSES:
        class_rows = [row for row in rows if row["actual"] == slug]
        class_accepted = [row for row in class_rows if row["accepted"]]
        class_correct_raw = [r for r in class_rows if r["predicted"] == slug]
        class_correct_accepted = [
            r for r in class_accepted if r["predicted"] == slug
        ]

        summary["per_class"][slug] = {
            "total": len(class_rows),
            "accepted": len(class_accepted),
            "correct_raw": len(class_correct_raw),
            "correct_accepted": len(class_correct_accepted),
            "raw_accuracy": safe_rate(len(class_correct_raw), len(class_rows)),
            "coverage": safe_rate(len(class_accepted), len(class_rows)),
            "accepted_accuracy": safe_rate(
                len(class_correct_accepted), len(class_accepted)
            ),
        }

    return summary


def print_report(results):
    print("\n" + "=" * 65)
    print("LOOCV RESULTS")
    print("=" * 65)

    for method_key in ("full_card", "illustration_only", "combined"):
        summary = analyze_method(results, method_key)

        print(f"\n--- {method_key.upper()} ---")
        print(f"Evaluated samples:       {summary['total']}")
        print(f"Raw top-1 accuracy:      {summary['raw_accuracy'] * 100:.1f}% ({summary['correct_raw']}/{summary['total']})")
        print(f"Coverage:                {summary['coverage'] * 100:.1f}%")
        print(f"Correct among accepted:  {summary['accepted_correct_rate'] * 100:.1f}%")
        print(f"False accepts:           {summary['wrong_accepted']}")
        print(f"False-accept rate:       {summary['false_accept_rate'] * 100:.1f}%")
        print(f"Rejected:                {summary['rejected']}")
        print(f"Correct but rejected:    {summary['correct_rejected']}")

        for slug, values in summary["per_class"].items():
            print(f"  {slug}: {values['correct_raw']}/{values['total']} raw correct ({values['raw_accuracy'] * 100:.1f}%)")

        if summary["mean_gap"] is not None:
            print(f"Mean score gap:           {summary['mean_gap']:.6f}")
            print(f"Minimum score gap:        {summary['min_gap']:.6f}")
            print(f"Maximum score gap:        {summary['max_gap']:.6f}")

        wrong = [row for row in results if row["method"] == method_key and row["predicted"] != row["actual"]]
        if wrong:
            print("Misclassified samples:")
            for row in wrong[:10]:
                print(f"  {row['actual']} -> {row['predicted']} | accepted={row['accepted']} | {row['fold']}")


def export_csv(results, output_path):
    if not results:
        print("No results to export.")
        return

    fieldnames = [
        "fold", "path", "method", "actual", "predicted",
        "score", "runner_slug", "runner_score", "gap", "accepted", "reason",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nCSV saved to: {Path(output_path).resolve()}")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    try:
        pygame.init()

        print("=" * 65)
        print("HarvestHand LOOCV Diagnostic")
        print("=" * 65)

        samples = discover_samples()

        print("\nDataset verification:")
        for slug in CLASSES:
            actual = sum(1 for sample in samples if sample["slug"] == slug)
            expected = EXPECTED_COUNTS[slug]
            print(f"  {slug}: {actual} (expected {expected})")

            if actual != expected:
                raise RuntimeError(
                    f"Expected {expected} samples for {slug}, but found {actual}."
                )

        print(f"\nTotal images: {len(samples)}")

        print(f"Verifying extractor equivalence on all {len(samples)} samples...")
        for sample in samples:
            verify_extractor(sample["path"])
        print("  Extractor verification PASSED")

        valid_samples = []
        skipped = []

        for index, sample in enumerate(samples, start=1):
            print(f"  [{index}/{len(samples)}] {sample['slug']} / {sample['path'].name}")
            vectors = extract_all_features(sample["path"])
            if vectors is None:
                skipped.append(sample["path"])
                continue
            sample["features"] = vectors
            valid_samples.append(sample)

        if skipped:
            print("\nSkipped unreadable or invalid images:")
            for path in skipped:
                print(f"  {path}")

        if len(valid_samples) < 4:
            raise RuntimeError(f"Not enough valid samples for LOOCV: {len(valid_samples)}")

        for slug in CLASSES:
            count = sum(1 for sample in valid_samples if sample["slug"] == slug)
            if count < 2:
                raise RuntimeError(
                    f"Not enough valid samples for {slug}: {count}. Each class needs at least 2 valid images."
                )

        print(f"\nValid images: {len(valid_samples)}/{len(samples)}")

        print("\nStarting LOOCV...")
        results = run_loocv(valid_samples)

        print_report(results)
        export_csv(results, OUTPUT_CSV)

        print("\n" + "=" * 65)
        print("DIAGNOSTIC COMPLETE")
        print("Production card_model.json was not modified.")
        print("No production thresholds were changed.")
        print("=" * 65)

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
