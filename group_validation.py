"""
HarvestHand — Group-Based Dataset Expansion & Independent Validation

This script runs two experiments:

  Experiment A: Existing 41-image dataset (LOOCV baseline)
  Experiment B: Expanded dataset (group-based session cross-validation)

Read-only: does not modify production files, card_model.json, thresholds,
or training images.

Outputs:
  - group_validation_results.csv   (raw per-fold results)
  - group_validation_report.md     (readable report)
  - expanded_validation_errors.png (contact sheet of incorrect predictions)
"""
import csv
import hashlib
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, r"D:\HarvestHand")

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
from PIL import Image

import cardscan.preprocess as preprocess
import cardscan.model as model_module
import cardscan.features as features

pygame.init()
pygame.font.init()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
EXISTING_PECHAY = r"D:\HarvestHand\data\card_samples\pechay_plant"
EXISTING_MONGO  = r"D:\HarvestHand\data\card_samples\monggo_plant"
EXPANDED_ROOT   = r"D:\HarvestHand\cardscan\dataset"

RESULTS_CSV = r"D:\HarvestHand\group_validation_results.csv"
REPORT_MD   = r"D:\HarvestHand\group_validation_report.md"
ERRORS_PNG  = r"D:\HarvestHand\expanded_validation_errors.png"

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
GRID = 24
CONF_THRESH = 0.80
TOP_K = 3
METHODS = ("full_card", "illustration_only", "combined")
CLASSES = ("pechay_plant", "monggo_plant")
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

MARGINS = (0.001, 0.003, 0.005, 0.0075, 0.010,
           0.015, 0.020, 0.030, 0.050, 0.070)

ILLUSTRATION_TOP = 0.25
ILLUSTRATION_BOTTOM = 0.75


# ---------------------------------------------------------------------------
# Feature extraction (mirrors run_crossval.py / features.py, parameterized)
# ---------------------------------------------------------------------------
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
    # weight map (mirrors features._build_weight_map)
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


# ---------------------------------------------------------------------------
# Dataset discovery
# ---------------------------------------------------------------------------
def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def session_from_path(path, root_label):
    """Determine capture session from path.

    Existing data: IMG_YYYYMMDD_HHMMSS.jpg -> date is session.
    Expanded data: cardscan/dataset/<class>/session_XX/ -> session_XX is session.
    """
    p = Path(path)
    # Check if under expanded dataset root
    try:
        rel = p.relative_to(EXPANDED_ROOT)
        # rel.parts[0] = class, parts[1] = session
        if len(rel.parts) >= 2:
            return rel.parts[1]
    except ValueError:
        pass
    # Existing data: extract date from filename
    stem = p.stem
    parts = stem.split("_")
    if len(parts) >= 2 and parts[0] == "IMG" and len(parts[1]) == 8:
        return parts[1]
    return "unknown"


def discover_all_samples():
    """Discover all samples from existing + expanded locations.

    Returns list of dicts with: path, class_label, session, source (existing/new)
    """
    samples = []
    seen_hashes = {}

    for class_label, folder in (("pechay_plant", EXISTING_PECHAY),
                                 ("monggo_plant", EXISTING_MONGO)):
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            if not name.lower().endswith(IMAGE_EXTS):
                continue
            path = os.path.join(folder, name)
            digest = file_hash(path)
            session = session_from_path(path, "existing")
            samples.append({
                "path": path, "class_label": class_label,
                "session": session, "source": "existing",
                "filename": name, "hash": digest,
            })
            seen_hashes[digest] = path

    # Expanded dataset (new images)
    if os.path.isdir(EXPANDED_ROOT):
        for class_label in CLASSES:
            class_dir = os.path.join(EXPANDED_ROOT, class_label)
            if not os.path.isdir(class_dir):
                continue
            for session_dir in sorted(os.listdir(class_dir)):
                session_path = os.path.join(class_dir, session_dir)
                if not os.path.isdir(session_path):
                    continue
                for name in sorted(os.listdir(session_path)):
                    if not name.lower().endswith(IMAGE_EXTS):
                        continue
                    path = os.path.join(session_path, name)
                    digest = file_hash(path)
                    # Duplicate check against existing
                    if digest in seen_hashes:
                        print(f"  DUPLICATE (exact): {path} matches {seen_hashes[digest]}")
                        continue
                    seen_hashes[digest] = path
                    samples.append({
                        "path": path, "class_label": class_label,
                        "session": session_dir, "source": "new",
                        "filename": name, "hash": digest,
                    })

    return samples


# ---------------------------------------------------------------------------
# Group-based cross-validation
# ---------------------------------------------------------------------------
def build_fold_model(training_samples, method_key, grid):
    vectors_by_class = {slug: [] for slug in CLASSES}
    for s in training_samples:
        vec = s["features"][grid][method_key]
        vectors_by_class[s["class_label"]].append(vec)
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


def run_leave_one_session_out(samples, grid):
    """Group-based CV: leave one session out per fold.

    Returns list of result dicts.
    """
    # Group samples by session
    sessions = defaultdict(list)
    for s in samples:
        sessions[s["session"]].append(s)

    session_names = sorted(sessions.keys())
    results = []

    for held_out_session in session_names:
        train_samples = []
        test_samples = []
        for sess_name, sess_samples in sessions.items():
            if sess_name == held_out_session:
                test_samples.extend(sess_samples)
            else:
                train_samples.extend(sess_samples)

        # Verify no session leakage
        train_sessions = {s["session"] for s in train_samples}
        test_sessions = {s["session"] for s in test_samples}
        assert not (train_sessions & test_sessions), "Session leakage detected!"

        for method_key in METHODS:
            fold_model = build_fold_model(train_samples, method_key, grid)
            for test_sample in test_samples:
                top_c, top_s, run_c, run_s = classify_fold(
                    fold_model, test_sample["features"][grid][method_key])
                gap = top_s - run_s
                correct = top_c == test_sample["class_label"]
                results.append({
                    "experiment": "B",
                    "grid": grid,
                    "method": method_key,
                    "held_out_session": held_out_session,
                    "filename": test_sample["filename"],
                    "class_label": test_sample["class_label"],
                    "session": test_sample["session"],
                    "source": test_sample["source"],
                    "predicted": top_c if top_c else "",
                    "score": top_s,
                    "runner_score": run_s if run_s is not None else 0.0,
                    "gap": gap,
                    "correct": correct,
                    "accepted": top_s >= CONF_THRESH and gap >= CONF_THRESH,  # placeholder
                })
    return results, session_names


def run_loocv_baseline(samples, grid):
    """Experiment A: Leave-one-out CV on existing 41 images."""
    results = []
    for test_index, test_sample in enumerate(samples):
        train_samples = [s for i, s in enumerate(samples) if i != test_index]
        for method_key in METHODS:
            fold_model = build_fold_model(train_samples, method_key, grid)
            top_c, top_s, run_c, run_s = classify_fold(
                fold_model, test_sample["features"][grid][method_key])
            gap = top_s - run_s
            correct = top_c == test_sample["class_label"]
            results.append({
                "experiment": "A",
                "grid": grid,
                "method": method_key,
                "held_out_session": "loocv",
                "filename": test_sample["filename"],
                "class_label": test_sample["class_label"],
                "session": test_sample["session"],
                "source": "existing",
                "predicted": top_c if top_c else "",
                "score": top_s,
                "runner_score": run_s if run_s is not None else 0.0,
                "gap": gap,
                "correct": correct,
                "accepted": False,  # placeholder
            })
    return results


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def safe_div(n, d):
    return n / d if d else 0.0


def compute_metrics(results, margins):
    """Compute per-method metrics from result rows."""
    by_method = defaultdict(list)
    for r in results:
        by_method[r["method"]].append(r)

    metrics = {}
    for method, rows in by_method.items():
        total = len(rows)
        correct = [r for r in rows if r["correct"]]
        incorrect = [r for r in rows if not r["correct"]]
        raw_acc = safe_div(len(correct), total)

        gaps = [r["gap"] for r in rows]
        cgaps = [r["gap"] for r in correct]
        igaps = [r["gap"] for r in incorrect]

        # Confusion matrix
        cm = defaultdict(int)
        for r in rows:
            cm[(r["class_label"], r["predicted"])] += 1

        # Per-class
        per_class = {}
        for slug in CLASSES:
            cr = [r for r in rows if r["class_label"] == slug]
            cc = [r for r in cr if r["correct"]]
            tp = len(cc)
            fp = sum(1 for r in rows if r["predicted"] == slug and r["class_label"] != slug)
            fn = sum(1 for r in rows if r["class_label"] == slug and r["predicted"] != slug)
            precision = safe_div(tp, tp + fp)
            recall = safe_div(tp, tp + fn)
            f1 = safe_div(2 * precision * recall, precision + recall) if (precision + recall) > 0 else 0.0
            per_class[slug] = {
                "total": len(cr), "correct": tp,
                "accuracy": safe_div(tp, len(cr)),
                "precision": precision, "recall": recall, "f1": f1,
                "false_positives": fp, "false_negatives": fn,
            }

        # Threshold simulations
        threshold_results = {}
        for margin in margins:
            accepted = [r for r in rows
                        if r["score"] >= CONF_THRESH and r["gap"] >= margin]
            acc_count = len(accepted)
            acc_correct = [r for r in accepted if r["correct"]]
            acc_incorr = [r for r in accepted if not r["correct"]]
            coverage = safe_div(acc_count, total)
            acc_acc = safe_div(len(acc_correct), acc_count)
            false_acc_all = safe_div(len(acc_incorr), total)
            correct_rejected = len(correct) - len(acc_correct)
            # Per-class accepted accuracy
            per_class_acc = {}
            for slug in CLASSES:
                cls_acc = [r for r in accepted if r["class_label"] == slug]
                cls_corr = [r for r in cls_acc if r["correct"]]
                per_class_acc[slug] = {
                    "coverage": safe_div(len(cls_acc), len([r for r in rows if r["class_label"] == slug])),
                    "accepted_accuracy": safe_div(len(cls_corr), len(cls_acc)),
                }
            threshold_results[margin] = {
                "coverage": coverage, "accepted": acc_count,
                "correct_accepted": len(acc_correct),
                "incorrect_accepted": len(acc_incorr),
                "accepted_accuracy": acc_acc,
                "false_accept_rate_all": false_acc_all,
                "correct_rejected": correct_rejected,
                "per_class": per_class_acc,
            }

        metrics[method] = {
            "total": total,
            "correct": len(correct),
            "incorrect": len(incorrect),
            "raw_accuracy": raw_acc,
            "mean_gap": sum(gaps) / len(gaps) if gaps else 0.0,
            "median_gap": sorted(gaps)[len(gaps) // 2] if gaps else 0.0,
            "min_gap": min(gaps) if gaps else 0.0,
            "max_gap": max(gaps) if gaps else 0.0,
            "correct_gaps": cgaps,
            "incorrect_gaps": igaps,
            "confusion_matrix": dict(cm),
            "per_class": per_class,
            "thresholds": threshold_results,
        }
    return metrics


# ---------------------------------------------------------------------------
# CSV output
# ---------------------------------------------------------------------------
def write_results_csv(all_rows, path):
    fieldnames = ["experiment", "grid", "method", "held_out_session",
                  "filename", "class_label", "session", "source",
                  "predicted", "score", "runner_score", "gap", "correct", "accepted"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in all_rows:
            w.writerow(r)
    print(f"Raw results saved to {path} ({len(all_rows)} rows)")


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def write_report(metrics_a, metrics_b, sessions_info, path):
    lines = []
    lines.append("# HarvestHand — Group-Based Validation Report")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("Two experiments compare feature methods on the HarvestHand card scanner:")
    lines.append("")
    lines.append("**Experiment A** — Existing 41-image dataset (20 pechay, 21 monggo),")
    lines.append("Leave-One-Out Cross-Validation (LOOCV). All images from a single")
    lines.append("capture session (20261109). This is the historical baseline.")
    lines.append("")
    lines.append("**Experiment B** — Expanded dataset, group-based session cross-validation.")
    lines.append("Images from the same capture session never appear in both training")
    lines.append("and validation. Provides independent-session generalization estimate.")
    lines.append("")
    lines.append(f"Fixed configuration: GRID={GRID}, confidence={CONF_THRESH},")
    lines.append(f"top-k={TOP_K}, cosine similarity, nearest-sample classifier.")
    lines.append("")
    lines.append("## Session Information")
    lines.append("")
    for label, info in sessions_info.items():
        lines.append(f"- **{label}**: {info['images']} images, {info['sessions']} sessions")
    lines.append("")
    lines.append("## Experiment A — Existing 41-Image Dataset (LOOCV Baseline)")
    lines.append("")
    lines.append("| Method | Raw acc. | Pechay acc. | Monggo acc. | Mean gap | Median gap |")
    lines.append("|--------|----------|-------------|-------------|----------|------------|")
    for method in METHODS:
        m = metrics_a[method]
        pc = m["per_class"]
        lines.append(
            f"| {method} | {m['raw_accuracy']:.3f} | "
            f"{pc['pechay_plant']['accuracy']:.3f} | {pc['monggo_plant']['accuracy']:.3f} | "
            f"{m['mean_gap']:.6f} | {m['median_gap']:.6f} |"
        )
    lines.append("")
    lines.append("### Confusion matrices (Experiment A)")
    lines.append("")
    for method in METHODS:
        cm = metrics_a[method]["confusion_matrix"]
        lines.append(f"#### {method}")
        lines.append("| Actual \\ Predicted | pechay_plant | monggo_plant |")
        lines.append("|---------------------|--------------|--------------|")
        lines.append(
            f"| pechay_plant | {cm.get(('pechay_plant','pechay_plant'),0)} | {cm.get(('pechay_plant','monggo_plant'),0)} |")
        lines.append(
            f"| monggo_plant | {cm.get(('monggo_plant','pechay_plant'),0)} | {cm.get(('monggo_plant','monggo_plant'),0)} |")
        lines.append("")
    lines.append("### Threshold simulations (Experiment A, confidence=0.80)")
    lines.append("")
    lines.append("| Method | Margin | Coverage | Accepted | Correct acc. | False-accept (all) | Correct rejected |")
    lines.append("|--------|--------|----------|----------|--------------|--------------------|------------------|")
    for method in METHODS:
        for margin in MARGINS:
            t = metrics_a[method]["thresholds"][margin]
            lines.append(
                f"| {method} | {margin} | {t['coverage']:.3f} | {t['accepted']} | "
                f"{t['accepted_accuracy']:.3f} | {t['false_accept_rate_all']:.4f} | {t['correct_rejected']} |"
            )
    lines.append("")

    lines.append("## Experiment B — Expanded Dataset (Group-Based Session CV)")
    lines.append("")
    if metrics_b:
        lines.append("| Method | Raw acc. | Pechay acc. | Monggo acc. | Mean gap | Median gap |")
        lines.append("|--------|----------|-------------|-------------|----------|------------|")
        for method in METHODS:
            m = metrics_b[method]
            pc = m["per_class"]
            lines.append(
                f"| {method} | {m['raw_accuracy']:.3f} | "
                f"{pc['pechay_plant']['accuracy']:.3f} | {pc['monggo_plant']['accuracy']:.3f} | "
                f"{m['mean_gap']:.6f} | {m['median_gap']:.6f} |"
            )
        lines.append("")
        lines.append("### Confusion matrices (Experiment B)")
        lines.append("")
        for method in METHODS:
            cm = metrics_b[method]["confusion_matrix"]
            lines.append(f"#### {method}")
            lines.append("| Actual \\ Predicted | pechay_plant | monggo_plant |")
            lines.append("|---------------------|--------------|--------------|")
            lines.append(
                f"| pechay_plant | {cm.get(('pechay_plant','pechay_plant'),0)} | {cm.get(('pechay_plant','monggo_plant'),0)} |")
            lines.append(
                f"| monggo_plant | {cm.get(('monggo_plant','pechay_plant'),0)} | {cm.get(('monggo_plant','monggo_plant'),0)} |")
            lines.append("")
        lines.append("### Threshold simulations (Experiment B, confidence=0.80)")
        lines.append("")
        lines.append("| Method | Margin | Coverage | Accepted | Correct acc. | False-accept (all) | Correct rejected |")
        lines.append("|--------|--------|----------|----------|--------------|--------------------|------------------|")
        for method in METHODS:
            for margin in MARGINS:
                t = metrics_b[method]["thresholds"][margin]
                lines.append(
                    f"| {method} | {margin} | {t['coverage']:.3f} | {t['accepted']} | "
                    f"{t['accepted_accuracy']:.3f} | {t['false_accept_rate_all']:.4f} | {t['correct_rejected']} |"
                )
        lines.append("")
    else:
        lines.append("**Not available** — insufficient independent capture sessions for group-based validation.")
        lines.append("All existing pechay/monggo images come from a single session (20261109).")
        lines.append("Group-based validation requires at least 2 sessions per class (one for")
        lines.append("training, one for validation). Please add images from additional sessions.")
        lines.append("")

    lines.append("## Comparison: Experiment A vs Experiment B")
    lines.append("")
    lines.append("| Method | Exp A raw acc. | Exp B raw acc. | Change |")
    lines.append("|--------|---------------|---------------|--------|")
    for method in METHODS:
        a = metrics_a[method]["raw_accuracy"]
        b_val = metrics_b[method]["raw_accuracy"] if metrics_b else None
        if b_val is not None:
            change = f"{b_val - a:+.3f}"
            b_str = f"{b_val:.3f}"
        else:
            change = "N/A"
            b_str = "N/A"
        lines.append(f"| {method} | {a:.3f} | {b_str} | {change} |")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Raw results: `group_validation_results.csv`")
    lines.append("- Threshold results analyze the same predictions, not independent validation.")
    lines.append("- No production files, card_model.json, thresholds, or training images were modified.")
    lines.append("- Experiment B requires multiple independent capture sessions per class.")
    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Report saved to {path}")


# ---------------------------------------------------------------------------
# Error contact sheet
# ---------------------------------------------------------------------------
def make_error_contact_sheet(error_rows, path):
    """Create a contact sheet of incorrect predictions."""
    if not error_rows:
        print("No errors to display in contact sheet.")
        return

    COLS = 4
    CELL_W = 320
    CELL_H = 460
    IMG_W = 260
    IMG_H = 364
    PAD = 14

    rows_needed = (len(error_rows) + COLS - 1) // COLS
    width = COLS * CELL_W + (COLS + 1) * PAD
    height = rows_needed * CELL_H + (rows_needed + 1) * PAD + 60

    sheet = pygame.Surface((width, height))
    sheet.fill((240, 240, 240))

    title = pygame.font.SysFont(None, 24).render(
        "Hard-Negative Analysis — Incorrect Validation Predictions", True, (30, 30, 30))
    sheet.blit(title, (PAD, PAD // 2))

    font = pygame.font.SysFont(None, 18)
    font_small = pygame.font.SysFont(None, 16)

    for idx, r in enumerate(error_rows):
        r_idx = idx // COLS
        c_idx = idx % COLS
        x = PAD + c_idx * (CELL_W + PAD)
        y = PAD + 50 + r_idx * (CELL_H + PAD)

        cell = pygame.Surface((CELL_W, CELL_H))
        cell.fill((255, 255, 255))
        pygame.draw.rect(cell, (180, 180, 180), cell.get_rect(), 2)

        # Load and display image
        img_surf = None
        try:
            raw = preprocess.load_image(r.get("path", ""))
            if raw is not None:
                prepared = preprocess.prepare(raw)
                if prepared is not None:
                    pw, ph = prepared.get_size()
                    scale = min(IMG_W / pw, IMG_H / ph)
                    nw = max(1, int(pw * scale))
                    nh = max(1, int(ph * scale))
                    img_surf = pygame.transform.smoothscale(prepared, (nw, nh))
        except Exception:
            pass

        if img_surf:
            ix = (CELL_W - nw) // 2
            iy = 30
            cell.blit(img_surf, (ix, iy))
            img_rect = pygame.Rect(ix, iy, nw, nh)
            pygame.draw.rect(cell, (180, 180, 180), img_rect, 1)

        # Labels
        name = r["filename"]
        if len(name) > 28:
            name = name[:25] + "..."
        name_surf = font_small.render(name, True, (30, 30, 30))
        cell.blit(name_surf, (CELL_W // 2 - name_surf.get_width() // 2, iy + nh + 8 if img_surf else 40))

        line1 = f"Actual: {r['class_label']}  Pred: {r['predicted']}"
        l1 = font.render(line1, True, (30, 30, 30))
        ly = iy + nh + 30 if img_surf else 66
        cell.blit(l1, (CELL_W // 2 - l1.get_width() // 2, ly))

        line2 = f"Score: {r['score']:.4f}  Gap: {r['gap']:.6f}"
        l2 = font.render(line2, True, (190, 60, 60))
        cell.blit(l2, (CELL_W // 2 - l2.get_width() // 2, ly + 24))

        line3 = f"Session: {r['session']}  Method: {r['method']}"
        l3 = font_small.render(line3, True, (100, 100, 100))
        cell.blit(l3, (CELL_W // 2 - l3.get_width() // 2, ly + 48))

        sheet.blit(cell, (x, y))

    pygame.image.save(sheet, path)
    print(f"Error contact sheet saved to {path} ({width}x{height})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # Discover all samples
    print("Discovering samples...")
    samples = discover_all_samples()
    print(f"Total samples discovered: {len(samples)}")

    by_class = defaultdict(list)
    by_session = defaultdict(list)
    for s in samples:
        by_class[s["class_label"]].append(s)
        by_session[s["session"]].append(s)

    print(f"By class: {{k: len(v) for k, v in by_class.items()}}")
    print(f"By session: {{k: len(v) for k, v in by_session.items()}}")

    # Session info
    sessions_info = {}
    for slug in CLASSES:
        cls_samples = [s for s in samples if s["class_label"] == slug]
        sessions = set(s["session"] for s in cls_samples)
        sessions_info[slug] = {
            "images": len(cls_samples),
            "sessions": len(sessions),
            "session_list": sorted(sessions),
        }

    # Extract features for all samples
    print(f"\nExtracting features (GRID={GRID})...")
    for s in samples:
        vecs = extract_all(s["path"], GRID)
        if vecs is None:
            print(f"  WARNING: feature extraction failed for {s['path']}")
        s["features"] = {GRID: vecs}

    valid = [s for s in samples if s.get("features")]
    print(f"Valid samples: {len(valid)}/{len(samples)}")

    # Experiment A: LOOCV on existing 41 images
    existing = [s for s in valid if s["source"] == "existing"]
    print(f"\n=== Experiment A: LOOCV on {len(existing)} existing images ===")
    results_a = run_loocv_baseline(existing, GRID)
    metrics_a = compute_metrics(results_a, MARGINS)

    # Experiment B: Group-based CV on all samples
    print(f"\n=== Experiment B: Group-based CV on {len(valid)} images ===")
    # Check if we have enough sessions for group-based validation
    min_sessions_per_class = 2
    enough_sessions = all(
        sessions_info[slug]["sessions"] >= min_sessions_per_class
        for slug in CLASSES
    )

    if enough_sessions and len(valid) > len(existing):
        results_b, session_names = run_leave_one_session_out(valid, GRID)
        metrics_b = compute_metrics(results_b, MARGINS)
    else:
        print("  Insufficient independent sessions for group-based validation.")
        print("  All existing pechay/monggo images are from a single session (20261109).")
        print("  Group-based validation requires at least 2 sessions per class.")
        results_b = []
        metrics_b = None

    # Write CSV
    all_rows = results_a + results_b
    write_results_csv(all_rows, RESULTS_CSV)

    # Write report
    write_report(metrics_a, metrics_b, sessions_info, REPORT_MD)

    # Error contact sheet (from Experiment B if available, else A)
    error_source = results_b if results_b else results_a
    error_rows = [r for r in error_source if not r["correct"]]
    # Attach paths for contact sheet
    path_by_filename = {s["filename"]: s["path"] for s in valid}
    for r in error_rows:
        r["path"] = path_by_filename.get(r["filename"], "")
    make_error_contact_sheet(error_rows, ERRORS_PNG)

    # Summary
    print("\n=== SUMMARY ===")
    for method in METHODS:
        ma = metrics_a[method]
        print(f"\n[Experiment A] {method}:")
        print(f"  Raw accuracy: {ma['raw_accuracy']:.3f}")
        print(f"  Pechay: {ma['per_class']['pechay_plant']['accuracy']:.3f} "
              f"({ma['per_class']['pechay_plant']['correct']}/{ma['per_class']['pechay_plant']['total']})")
        print(f"  Monggo: {ma['per_class']['monggo_plant']['accuracy']:.3f} "
              f"({ma['per_class']['monggo_plant']['correct']}/{ma['per_class']['monggo_plant']['total']})")
        if metrics_b:
            mb = metrics_b[method]
            print(f"\n[Experiment B] {method}:")
            print(f"  Raw accuracy: {mb['raw_accuracy']:.3f}")
            print(f"  Pechay: {mb['per_class']['pechay_plant']['accuracy']:.3f} "
                  f"({mb['per_class']['pechay_plant']['correct']}/{mb['per_class']['pechay_plant']['total']})")
            print(f"  Monggo: {mb['per_class']['monggo_plant']['accuracy']:.3f} "
                  f"({mb['per_class']['monggo_plant']['correct']}/{mb['per_class']['monggo_plant']['total']})")

    print("\nDone.")


if __name__ == "__main__":
    main()
