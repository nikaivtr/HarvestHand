"""Part 1 — Visual contact sheet for misclassification inspection.

Loads original training images, identifies the 10 samples misclassified by
all three LOOCV methods (from crossval_results.csv), selects 5 correctly
classified Pechay and 5 correctly classified Monggo samples, and renders a
20-image contact sheet with labels. Read-only: does not modify any images
or production files.
"""
import csv
import os
import sys

sys.path.insert(0, r"D:\HarvestHand")
import pygame
import cardscan.preprocess as preprocess

pygame.font.init()

RESULTS_CSV = r"D:\HarvestHand\crossval_results.csv"
PECHAY_DIR = r"D:\HarvestHand\data\card_samples\pechay_plant"
MONGO_DIR  = r"D:\HarvestHand\data\card_samples\monggo_plant"
OUT_PNG = r"D:\HarvestHand\misclassification_contact_sheet.png"

COLS = 5
ROWS = 4
CELL_W = 360
CELL_H = 560
IMG_W = 300
IMG_H = 420            # 5:7 portrait, matches prepared canvas
PAD = 18
FONT = pygame.font.SysFont(None, 22)
FONT_SMALL = pygame.font.SysFont(None, 18)

COLOR_CORRECT = (60, 160, 60)
COLOR_WRONG = (190, 60, 60)
COLOR_TEXT = (30, 30, 30)
COLOR_BG = (240, 240, 240)
COLOR_CELL = (255, 255, 255)
COLOR_BORDER = (180, 180, 180)


def load_results():
    rows = []
    with open(RESULTS_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["score"] = float(r["score"])
            r["runner_score"] = float(r["runner_score"])
            r["gap"] = float(r["gap"])
            r["correct"] = r["actual"] == r["predicted"]
            rows.append(r)
    return rows


def cell_for_image(path, actual, predicted, correct):
    """Build one contact-sheet cell: prepared image + text labels."""
    raw = preprocess.load_image(path)
    if raw is None:
        return None
    prepared = preprocess.prepare(raw)
    if prepared is None:
        return None

    # Scale prepared image to fit IMG_W x IMG_H preserving aspect ratio.
    pw, ph = prepared.get_size()
    scale = min(IMG_W / pw, IMG_H / ph)
    nw = max(1, int(pw * scale))
    nh = max(1, int(ph * scale))
    img = pygame.transform.smoothscale(prepared, (nw, nh))

    cell = pygame.Surface((CELL_W, CELL_H))
    cell.fill(COLOR_CELL)
    pygame.draw.rect(cell, COLOR_BORDER, cell.get_rect(), 2)

    # Center the image in the top portion.
    ix = (CELL_W - nw) // 2
    iy = (CELL_H - IMG_H - PAD - 60) // 2
    cell.blit(img, (ix, iy))
    img_rect = pygame.Rect(ix, iy, nw, nh)
    pygame.draw.rect(cell, COLOR_BORDER, img_rect, 1)

    # Filename (truncate).
    name = os.path.basename(path)
    if len(name) > 34:
        name = name[:31] + "..."
    name_surf = FONT_SMALL.render(name, True, COLOR_TEXT)
    cell.blit(name_surf, (CELL_W // 2 - name_surf.get_width() // 2, iy + nh + 8))

    # Actual / predicted line.
    line1 = f"Actual: {actual}   Pred: {predicted}"
    l1 = FONT.render(line1, True, COLOR_TEXT)
    cell.blit(l1, (CELL_W // 2 - l1.get_width() // 2, iy + nh + 34))

    # Status line (colored).
    status = "CORRECT" if correct else "INCORRECT"
    scolor = COLOR_CORRECT if correct else COLOR_WRONG
    l2 = FONT.render(status, True, scolor)
    cell.blit(l2, (CELL_W // 2 - l2.get_width() // 2, iy + nh + 60))

    return cell


def main():
    results = load_results()

    # Group results by (filename, actual) across methods.
    by_sample = {}
    for r in results:
        key = (r["path"], r["actual"])
        by_sample.setdefault(key, []).append(r)

    # Identify misclassified by all three methods.
    misclassified = []
    correct_by_class = {"pechay_plant": [], "monggo_plant": []}
    for (path, actual), rows in by_sample.items():
        methods = {r["method"] for r in rows}
        if methods != {"full_card", "illustration_only", "combined"}:
            continue
        all_wrong = all(not r["correct"] for r in rows)
        any_correct = any(r["correct"] for r in rows)
        predicted = rows[0]["predicted"]  # all methods agree on these samples
        if all_wrong:
            misclassified.append({
                "path": path, "actual": actual, "predicted": predicted,
                "correct": False,
            })
        elif any_correct and len(correct_by_class[actual]) < 5:
            correct_by_class[actual].append({
                "path": path, "actual": actual, "predicted": predicted,
                "correct": True,
            })

    print(f"Misclassified by all 3 methods: {len(misclassified)}")
    print(f"Correct pechay selected: {len(correct_by_class['pechay_plant'])}")
    print(f"Correct monggo selected: {len(correct_by_class['monggo_plant'])}")

    # Build ordered list: misclassified first, then correct pechay, then correct monggo.
    selected = []
    selected.extend(misclassified)
    selected.extend(correct_by_class["pechay_plant"])
    selected.extend(correct_by_class["monggo_plant"])

    # Canvas.
    width = COLS * CELL_W + (COLS + 1) * PAD
    height = ROWS * CELL_H + (ROWS + 1) * PAD + 60  # extra for title
    sheet = pygame.Surface((width, height))
    sheet.fill(COLOR_BG)

    title = FONT.render("HarvestHand — Misclassification Contact Sheet", True, COLOR_TEXT)
    sheet.blit(title, (PAD, PAD // 2))
    subtitle = FONT_SMALL.render(
        "Red = misclassified by all 3 methods  |  Green = correctly classified  |  "
        "10 misclassified + 5 correct pechay + 5 correct monggo = 20 images",
        True, (100, 100, 100),
    )
    sheet.blit(subtitle, (PAD, PAD // 2 + 30))

    for idx, entry in enumerate(selected):
        r = idx // COLS
        c = idx % COLS
        if r >= ROWS:
            break
        x = PAD + c * (CELL_W + PAD)
        y = PAD + 70 + r * (CELL_H + PAD)
        cell = cell_for_image(
            entry["path"], entry["actual"], entry["predicted"], entry["correct"]
        )
        if cell is None:
            print(f"  SKIP (could not load): {entry['path']}")
            continue
        sheet.blit(cell, (x, y))

    pygame.image.save(sheet, OUT_PNG)
    print(f"Contact sheet saved to {OUT_PNG} ({width}x{height})")


if __name__ == "__main__":
    main()
