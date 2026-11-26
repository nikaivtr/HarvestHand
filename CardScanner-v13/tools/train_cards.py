# ============================================================
#  train_cards.py
#
#  Builds cardscan/card_model.json from the sample photos in
#  data/card_samples/. Run this on the Raspberry Pi after you
#  photograph your physical cards - it is the "teach the system
#  the cards" step.
#
#  Usage:
#      python tools/train_cards.py              # train and save
#      python tools/train_cards.py --report     # train, then show
#                                             #   per-card accuracy
#      python tools/train_cards.py --samples DIR
#
#  Nothing here needs a camera or OpenCV.
# ============================================================

import argparse
import os
import sys

# Allow running as `python tools/train_cards.py` from the repo root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")   # no window needed
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

import cardscan.model as model
import cardscan.registry as registry


def _banner(text):
    print()
    print(text)
    print("-" * len(text))


def report(built):
    """Report leave-one-out sample recognition and class separation."""
    _banner("Recognition report")
    print(f"  threshold {built['threshold']}   margin {built['margin']}\n")

    ok = bad = 0
    for slug in sorted(built["cards"]):
        entry = built["cards"][slug]
        samples = entry["samples"]
        if not samples:
            continue
        top_hits = accepted_hits = 0
        scored = []
        for sample_index, vec in enumerate(samples):
            held_out = dict(built)
            held_out["cards"] = dict(built["cards"])
            held_out_entry = dict(entry)
            held_out_entry["samples"] = (
                samples[:sample_index] + samples[sample_index + 1:]
            )
            held_out["cards"][slug] = held_out_entry
            result = model.classify_detailed(held_out, vec)
            scored.append(result)
            if result["slug"] == slug:
                top_hits += 1
                if result["confident"]:
                    accepted_hits += 1
        n = len(scored)
        rate = accepted_hits / n if n else 0.0
        ok  += accepted_hits
        bad += n - accepted_hits
        flag = "ok " if rate >= 0.8 else "WEAK"
        mean_score = sum(row["best_score"] for row in scored) / n if n else 0.0
        mean_gap = sum(row["gap"] for row in scored) / n if n else 0.0
        print(f"  {slug:<20} ranked {top_hits:>3}/{n:<3}  "
              f"accepted {accepted_hits:>3}/{n:<3} "
              f"({rate * 100:>5.1f}%)  best {mean_score:.3f}  "
              f"gap {mean_gap:.3f}  {flag}")

    total = ok + bad
    if total:
        print(f"\n  overall {ok}/{total} ({ok / total * 100:.1f}%)")
    if ok < total:
        print("  -> add more samples, or photograph the cards more "
              "varied (tilt, distance, lighting)")

    # A quick check that cards stay distinguishable from each other.
    slugs = sorted(built["cards"])
    if len(slugs) > 1:
        _banner("Card separation (higher is better)")
        print("  lowest cross-score per card:")
        for a in slugs:
            worst, other = 1.0, None
            for b in slugs:
                if a == b:
                    continue
                s = model.similarity(
                    built["cards"][a]["centroid"],
                    built["cards"][b]["centroid"],
                )
                if s < worst:
                    worst, other = s, b
            flag = "ok " if worst < built["threshold"] else "CLOSE"
            print(f"    {a:<10} vs {other:<10} {worst:.3f}  {flag}")


def main():
    ap = argparse.ArgumentParser(description="Train the card model from sample photos")
    ap.add_argument("--samples", default=None,
                    help="root sample folder (default data/card_samples)")
    ap.add_argument("--report", action="store_true",
                    help="show per-card accuracy after training")
    ap.add_argument("--out", default=None, help="model output path")
    args = ap.parse_args()

    root = args.samples
    if root:
        root = os.path.abspath(root)
    else:
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        root = os.path.join(here, "data", "card_samples")

    pygame.init()

    _banner("Card samples")
    if not os.path.isdir(root):
        print(f"  sample folder not found: {root}")
        print(f"  create it, e.g. {os.path.join(root, 'water')}/")
        return 1

    found = model.sample_dirs(root)
    if not found:
        print("  no card folders yet. Create one per card, using the")
        print("  sample folder names from the catalog:")
        print("   ", ", ".join(
            card.sample_folder for card in registry.all_cards()
        ))
        return 1

    known = {c.sample_folder for c in registry.all_cards()}
    for folder in sorted(os.listdir(root)):
        if os.path.isdir(os.path.join(root, folder)) and folder not in known:
            print(f"  ! '{folder}' is not in the catalog - ignored "
                  "(add it to cardscan/registry.py)")

    _banner("Training")
    built = model.build_model(root, verbose=True)

    if not built["cards"]:
        print("\n  nothing to train on.")
        for slug in sorted(found):
            n = len(model.find_samples(slug, root))
            print(f"    {slug}: {n} images")
        return 1

    if len(built["cards"]) < 2:
        print(
            "\n  WARNING: only one card class was trained. The scanner cannot "
            "distinguish it from other objects and will not accept scans. "
            "Train at least one more visually distinct card class."
        )

    out = args.out
    if not out:
        out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "cardscan", "card_model.json")
    saved = model.save_model(built, out)
    size = os.path.getsize(saved)
    print(f"\n  saved {len(built['cards'])} cards -> {saved} ({size / 1024:.1f} KB)")

    if args.report:
        report(built)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
