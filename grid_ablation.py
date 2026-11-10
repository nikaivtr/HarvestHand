"""Part 2 — Feature-resolution ablation experiment.

Compares GRID = 12, 24, 32 using LOOCV on the same 41 original samples
(20 pechay_plant, 21 monggo_plant). Read-only: does not modify production
files, card_model.json, thresholds, or training images.

For each grid and each feature method (full_card, illustration_only,
combined) runs leave-one-out cross-validation with the nearest-sample
classifier (top-k=3, cosine similarity) at confidence 0.80 and multiple
margin thresholds.
"""
import csv
import os
import sys
import statistics

sys.path.insert(0, r"D:\HarvestHand")
import pygame
import cardscan.preprocess as preprocess
import cardscan.model as model_module
import cardscan.features as features

pygame.init()

PECHAY_DIR = r"D:\HarvestHand\data\card_samples\pechay_plant"
MONGO_DIR  = r"D:\HarvestHand\data\card_samples\monggo_plant"
OUT_CSV = r"D:\HarvestHand\grid_ablation_results.csv"
OUT_MD = r"D:\HarvestHand\grid_ablation_report.md"

GRIDS = (12, 24, 32)
METHODS = ("full_card", "illustration_only", "combined")
CLASSES = ("pechay_plant", "monggo_plant")
CONF_THRESH = 0.80
MARGINS = (0.001, 0.003, 0.005, 0.0075, 0.010)
TOP_K = 3
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

ILLUSTRATION_TOP = 0.25
ILLUSTRATION_BOTTOM = 0.75


# ------------------------------------------------------------ features
def extract_direct(surface, grid):
    if surface is None:
        return None
    small = pygame.transform.smoothscale(surface, (grid, grid))
    w, h = small.get_size()
    raw = pygame.image.tobytes(small, "RGB")
    lumas = [0.0] * (w * h)
    colours = [0.0] * (w * h * 3)
    lr, lg, lb = 0.299, 0.587, 0.114
    for y in range(h):
        for x in range(w):
            i = y * w + x
            j = i * 3
            lum = lr * raw[j] + lg * raw[j + 1] + lb * raw[j + 2]
            if lum > 18.0:
                colours[j] = raw[j] / 255.0
                colours[j + 1] = raw[j + 1] / 255.0
                colours[j + 2] = raw[j + 2] / 255.0
            lumas[i] = lum / 255.0
    edges = [0.0] * (w * h)
    for y in range(h):
        for x in range(w):
            i = y * w + x
            gx = 0.0; gy = 0.0
            if 0 < x < w - 1:
                gx = lumas[i + 1] - lumas[i - 1]
            if 0 < y < h - 1:
                gy = lumas[i + w] - lumas[i - w]
            mag = (gx * gx + gy * gy) ** 0.5
            edges[i] = min(mag, 1.0) * features.EDGE_WEIGHT
    # Build weight map inline (mirrors features._build_weight_map).
    cx = (w - 1) / 2.0; cy = (h - 1) / 2.0
    norm = max(cx, cy) or 1.0
    top, bottom = ILLUSTRATION_TOP, ILLUSTRATION_BOTTOM
    CENTER_FALLOFF = 0.5
    ILLUSTRATION_BOOST = 0.25
    wt = [[0.0] * w for _ in range(h)]
    for y in range(h):
        dy = (y - cy) / norm
        band = 1.0 if top <= (y / max(h - 1, 1)) <= bottom else 0.0
        for x in range(w):
            dx = (x - cx) / norm
            d2 = dx * dx + dy * dy
            k = 1.0 - CENTER_FALLOFF * (d2 if d2 < 1.0 else 1.0)
            if k < 0.3:
                k = 0.3
            k += ILLUSTRATION_BOOST * band
            wt[y][x] = k
    out = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            k = wt[y][x]
            c = i * 3
            out.append(colours[c] * k)
            out.append(colours[c + 1] * k)
            out.append(colours[c + 2] * k)
            out.append(edges[i] * k)
    return out


def extract_illustration(prepared_surface, grid):
    if prepared_surface is None:
        return None
    w, h = prepared_surface.get_size()
    top = int(h * ILLUSTRATION_TOP)
    bottom = int(h * ILLUSTRATION_BOTTOM)
    ch = bottom - top
    if ch <= 0:
        return None
    rect = pygame.Rect(0, top, w, ch)
    illustration = prepared_surface.subsurface(rect).copy()
    return extract_direct(illustration, grid)


def extract_all(path, grid):
    raw = preprocess.load_image(path)
    if raw is None:
        return None
    prepared = preprocess.prepare(raw)
    if prepared is None:
        return None
    full = extract_direct(prepared, grid)
    illus = extract_illustration(prepared, grid)
    if full is None or illus is None:
        return None
    return {"full_card": full, "illustration_only": illus, "combined": full + illus}


# ------------------------------------------------------------ data loading
def discover_samples():
    samples = []
    for slug, folder in (("pechay_plant", PECHAY_DIR), ("monggo_plant", MONGO_DIR)):
        for name in sorted(os.listdir(folder)):
            if not name.lower().endswith(IMAGE_EXTS):
                continue
            path = os.path.join(folder, name)
            samples.append({"slug": slug, "name": name, "path": path})
    return samples


# ------------------------------------------------------------ LOOCV
def build_fold_model(training_samples, method_key, grid):
    vectors_by_class = {slug: [] for slug in CLASSES}
    for s in training_samples:
        vec = s["features"][grid][method_key]
        vectors_by_class[s["slug"]].append(vec)
    cards = {}
    for slug in CLASSES:
        vecs = vectors_by_class[slug]
        cards[slug] = {
            "centroid": model_module._mean(vecs),
            "samples": vecs,
            "n": len(vecs),
        }
    return {"cards": cards}


def classify_fold(fold_model, vector):
    scored = []
    for slug, entry in fold_model["cards"].items():
        samples = entry.get("samples") or [entry.get("centroid")]
        if not samples:
            continue
        scored.append((model_module._class_score(samples, vector, TOP_K), slug))
    scored.sort(reverse=True)
    if not scored:
        return None, 0.0, None, 0.0
    top_s, top_c = scored[0]
    run_s, run_c = scored[1] if len(scored) > 1 else (0.0, None)
    return top_c, top_s, run_c, run_s


def run_ablation():
    samples = discover_samples()
    print(f"Total samples: {len(samples)}")
    assert len(samples) == 41, f"Expected 41 samples, got {len(samples)}"
    pechay = [s for s in samples if s["slug"] == "pechay_plant"]
    monggo = [s for s in samples if s["slug"] == "monggo_plant"]
    assert len(pechay) == 20 and len(monggo) == 21

    # Extract features for every sample at every grid.
    for s in samples:
        s["features"] = {}
        for grid in GRIDS:
            vecs = extract_all(s["path"], grid)
            if vecs is None:
                print(f"  WARNING: feature extraction failed for {s['path']}")
            s["features"][grid] = vecs

    valid = [s for s in samples if all(s["features"].get(g) for g in GRIDS)]
    print(f"Valid samples: {len(valid)}/{len(samples)}")
    assert len(valid) == 41

    all_rows = []  # raw per-fold results

    for grid in GRIDS:
        print(f"\n=== GRID {grid} ===")
        for test_index, test_sample in enumerate(valid):
            training = [s for i, s in enumerate(valid) if i != test_index]
            # Verify test sample excluded.
            assert test_sample not in training, "Test sample leaked into training!"
            for method_key in METHODS:
                fold_model = build_fold_model(training, method_key, grid)
                top_c, top_s, run_c, run_s = classify_fold(fold_model, test_sample["features"][grid][method_key])
                gap = top_s - run_s
                correct = top_c == test_sample["slug"]
                all_rows.append({
                    "grid": grid,
                    "method": method_key,
                    "fold": test_index + 1,
                    "filename": test_sample["name"],
                    "actual": test_sample["slug"],
                    "predicted": top_c if top_c else "",
                    "score": top_s,
                    "runner_score": run_s if run_s is not None else 0.0,
                    "gap": gap,
                    "correct": correct,
                })
    return all_rows


def write_csv(rows):
    fieldnames = ["grid", "method", "fold", "filename", "actual", "predicted",
                  "score", "runner_score", "gap", "correct"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Raw results saved to {OUT_CSV} ({len(rows)} rows)")


def summarize(rows):
    """Compute per-grid, per-method summary metrics."""
    summary = {}
    for grid in GRIDS:
        summary[grid] = {}
        for method in METHODS:
            mrows = [r for r in rows if r["grid"] == grid and r["method"] == method]
            total = len(mrows)
            correct = [r for r in mrows if r["correct"]]
            incorrect = [r for r in mrows if not r["correct"]]
            raw_acc = len(correct) / total if total else 0.0
            gaps = [r["gap"] for r in mrows]
            mean_gap = statistics.mean(gaps) if gaps else 0.0
            median_gap = statistics.median(gaps) if gaps else 0.0
            min_gap = min(gaps) if gaps else 0.0
            max_gap = max(gaps) if gaps else 0.0
            cgaps = [r["gap"] for r in correct]
            igaps = [r["gap"] for r in incorrect]
            # Per-class accuracy.
            per_class = {}
            for slug in CLASSES:
                cr = [r for r in mrows if r["actual"] == slug]
                cc = [r for r in cr if r["correct"]]
                per_class[slug] = {"total": len(cr), "correct": len(cc),
                                   "acc": len(cc) / len(cr) if cr else 0.0}
            # Threshold simulations.
            thresholds = {}
            for margin in MARGINS:
                accepted = [r for r in mrows if r["score"] >= CONF_THRESH and r["gap"] >= margin]
                acc_count = len(accepted)
                acc_correct = [r for r in accepted if r["correct"]]
                acc_incorr = [r for r in accepted if not r["correct"]]
                coverage = acc_count / total if total else 0.0
                acc_acc = len(acc_correct) / acc_count if acc_count else 0.0
                false_acc_all = len(acc_incorr) / total if total else 0.0
                correct_rejected = len(correct) - len(acc_correct)
                thresholds[margin] = {
                    "coverage": coverage, "accepted": acc_count,
                    "correct_accepted": len(acc_correct),
                    "incorrect_accepted": len(acc_incorr),
                    "accepted_accuracy": acc_acc,
                    "false_accept_rate_all": false_acc_all,
                    "correct_rejected": correct_rejected,
                }
            summary[grid][method] = {
                "total": total, "correct": len(correct), "incorrect": len(incorrect),
                "raw_accuracy": raw_acc,
                "mean_gap": mean_gap, "median_gap": median_gap,
                "min_gap": min_gap, "max_gap": max_gap,
                "correct_gaps": cgaps,
                "incorrect_gaps": igaps,
                "per_class": per_class,
                "thresholds": thresholds,
            }
    return summary


def write_report(summary):
    lines = []
    lines.append("# HarvestHand — Feature-Resolution Ablation Report")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("Leave-one-out cross-validation on 41 original samples "
                 "(20 pechay_plant, 21 monggo_plant) comparing feature grid "
                 "resolutions 12, 24, and 32. Classifier: nearest-sample with "
                 "top-k=3 cosine similarity. Preprocessing identical across grids "
                 "(card normalization to 120x168 5:7 canvas via cardscan.preprocess). "
                 "Confidence threshold fixed at 0.80. Margin thresholds simulated: "
                 "0.001, 0.003, 0.005, 0.0075, 0.010.")
    lines.append("")
    lines.append("## Per-Grid, Per-Method Summary")
    lines.append("")

    for grid in GRIDS:
        lines.append(f"### GRID {grid}")
        lines.append("")
        lines.append("| Method | Raw acc. | Per-class acc. (pechay/monggo) | Mean gap | Median gap | Min gap | Max gap |")
        lines.append("|--------|----------|--------------------------------|----------|------------|---------|---------|")
        for method in METHODS:
            s = summary[grid][method]
            pc = s["per_class"]
            pc_text = f"{pc['pechay_plant']['acc']:.3f} / {pc['monggo_plant']['acc']:.3f}"
            lines.append(
                f"| {method} | {s['raw_accuracy']:.3f} | {pc_text} | "
                f"{s['mean_gap']:.6f} | {s['median_gap']:.6f} | "
                f"{s['min_gap']:.6f} | {s['max_gap']:.6f} |"
            )
        lines.append("")

        lines.append("#### Gap distributions (correct vs incorrect)")
        lines.append("")
        lines.append("| Method | Correct n | Correct mean | Correct median | Incorrect n | Incorrect mean | Incorrect median |")
        lines.append("|--------|-----------|--------------|----------------|-------------|----------------|------------------|")
        for method in METHODS:
            s = summary[grid][method]
            cg = s["correct_gaps"]; ig = s["incorrect_gaps"]
            lines.append(
                f"| {method} | {len(cg)} | {statistics.mean(cg):.6f} | {statistics.median(cg):.6f} | "
                f"{len(ig)} | {statistics.mean(ig):.6f} | {statistics.median(ig):.6f} |"
            )
        lines.append("")
        lines.append("#### Threshold simulations (confidence = 0.80)")
        lines.append("")
        lines.append("| Method | Margin | Coverage | Accepted | Correct acc. | Incorrect acc. | False-accept (all) | Correct rejected |")
        lines.append("|--------|--------|----------|----------|--------------|----------------|--------------------|------------------|")
        for method in METHODS:
            for margin in MARGINS:
                t = summary[grid][method]["thresholds"][margin]
                lines.append(
                    f"| {method} | {margin} | {t['coverage']:.3f} | {t['accepted']} | "
                    f"{t['accepted_accuracy']:.3f} | "
                    f"{t['incorrect_accepted'] / t['accepted'] if t['accepted'] else 0:.3f} | "
                    f"{t['false_accept_rate_all']:.4f} | {t['correct_rejected']} |"
                )
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- Raw results: `grid_ablation_results.csv` (one row per fold, grid, method).")
    lines.append("- Threshold results are analysis of the same LOOCV predictions, not independent validation.")
    lines.append("- No production files, card_model.json, thresholds, or training images were modified.")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Report saved to {OUT_MD}")


def main():
    rows = run_ablation()
    write_csv(rows)
    summary = summarize(rows)
    write_report(summary)
    print("\nAblation complete.")


if __name__ == "__main__":
    main()
