"""Diagnose card sample photos: boundary detection + recognition quality.

Run from the project root (the folder that contains `cardscan/` and
`data/`):

    python tools/check_cards.py                      # data/card_samples
    python tools/check_cards.py --samples some/dir   # another folder
    python tools/check_cards.py --out debug/cards    # where pictures go
    python tools/check_cards.py --no-eval            # skip the model check

For every sample photo it runs the SAME preprocessing as training and
live scanning, then writes:

  <out>/<card>/<photo>.jpg   photo with the detected boundary drawn on it
                             (green = detected, yellow = fallback crop,
                              red = rejected, with the reason)
  <out>/_crops_<card>.png    contact sheet of the normalized crops that
                             recognition actually sees - if a card looks
                             wrong here, it is wrong in the model
  <out>/_report.txt          one line per photo

and prints a per-card summary, then a leave-one-out recognition check.
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import cv2
import numpy as np
import pygame

import cardscan.model as model
import cardscan.preprocess as preprocess
import cardscan.registry as registry


def annotate(surface, details):
    rgb = preprocess._surface_to_array(surface)
    img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR).copy()
    status, source = details.get("status"), details.get("source")
    if status == "detected":
        colour, label = (0, 200, 0), "detected q=%.2f" % details.get("quality", 0)
        pts = details.get("points")
    elif status == "fallback":
        colour, label = (0, 200, 255), "FALLBACK (%s)" % source
        pts = None
    else:
        colour, label = (0, 0, 255), "REJECTED: " + str(details.get("reason", ""))[:70]
        pts = details.get("candidate_points")
    if pts is not None:
        cv2.polylines(img, [np.int32(np.rint(pts))], True, colour, max(2, img.shape[1] // 300))
    if details.get("blurry"):
        label += " | BLURRY %.0f" % details.get("sharpness", 0)
    cv2.rectangle(img, (0, 0), (img.shape[1], 26), (0, 0, 0), -1)
    cv2.putText(img, label, (6, 19), cv2.FONT_HERSHEY_SIMPLEX, 0.55, colour, 1, cv2.LINE_AA)
    return img


def contact_sheet(canvases, cols=10):
    if not canvases:
        return None
    h, w = preprocess.CANVAS_H, preprocess.CANVAS_W
    rows = (len(canvases) + cols - 1) // cols
    sheet = np.full((rows * h, cols * w, 3), 40, np.uint8)
    for i, c in enumerate(canvases):
        r, k = divmod(i, cols)
        sheet[r * h:(r + 1) * h, k * w:(k + 1) * w] = cv2.cvtColor(
            preprocess._surface_to_array(c), cv2.COLOR_RGB2BGR)
    return sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", default=os.path.join("data", "card_samples"))
    ap.add_argument("--out", default=os.path.join("debug", "cards"))
    ap.add_argument("--no-eval", action="store_true")
    args = ap.parse_args()

    dirs = model.sample_dirs(args.samples)
    if not dirs:
        print("No sample folders found under %s" % args.samples)
        print("Expected one folder per card, named like registry sample_folder:")
        for c in registry.all_cards():
            print("   %s/%s" % (args.samples, c.sample_folder))
        return 1
    os.makedirs(args.out, exist_ok=True)
    report = []
    print("%-22s %5s %9s %8s %8s %7s" % ("card", "photos", "detected", "fallback", "REJECTED", "blurry"))
    total_bad = 0
    for slug in sorted(dirs):
        files = model.find_samples(slug, args.samples)
        os.makedirs(os.path.join(args.out, slug), exist_ok=True)
        counts = dict(detected=0, fallback=0, failed=0, blurry=0)
        crops = []
        for f in files:
            surf = preprocess.load_image(f)
            if surf is None:
                counts["failed"] += 1
                report.append("%s\tUNREADABLE" % f)
                continue
            canvas, details = preprocess.prepare_detailed(surf, fallback="training")
            key = {"detected": "detected", "fallback": "fallback"}.get(details.get("status"), "failed")
            counts[key] += 1
            counts["blurry"] += int(bool(details.get("blurry")))
            if canvas is not None:
                crops.append(canvas)
            report.append("%s\t%s\t%s\tq=%s\tsharp=%s" % (
                f, details.get("status"), details.get("reason"),
                "%.2f" % details["quality"] if "quality" in details else "-",
                details.get("sharpness", "-")))
            cv2.imwrite(os.path.join(args.out, slug, os.path.splitext(os.path.basename(f))[0] + ".jpg"),
                        annotate(surf, details))
        sheet = contact_sheet(crops)
        if sheet is not None:
            cv2.imwrite(os.path.join(args.out, "_crops_%s.png" % slug), sheet)
        total_bad += counts["failed"]
        print("%-22s %5d %9d %8d %8d %7d" % (slug, len(files), counts["detected"],
                                              counts["fallback"], counts["failed"], counts["blurry"]))
    with open(os.path.join(args.out, "_report.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(report))
    print("\nPictures written to %s (open the _crops_*.png sheets first)." % args.out)

    missing = [c.slug for c in registry.all_cards() if c.slug not in dirs or not model.find_samples(c.slug, args.samples)]
    if missing:
        print("\nCards with NO sample photos (cannot be recognised): " + ", ".join(missing))

    if not args.no_eval:
        print("\nBuilding model for a recognition check ...")
        built = model.build_model(args.samples)
        for p in built.get("problems", []):
            if "of 0 images" not in p:
                print("  note:", p)
        if len(built["cards"]) >= 2:
            model.evaluate(built, verbose=True)
        else:
            print("  need photos for at least 2 cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
