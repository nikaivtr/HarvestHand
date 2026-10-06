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

import cardscan.features as features
import cardscan.model as model
import cardscan.registry as registry


def _banner(text):
    print()
    print(text)
    print("-" * len(text))


def report(built, root):
    """Leave-one-out style check: how well does it know its own cards?"""
    _banner("Recognition report")
    print(f"  threshold {built['threshold']}   margin {built['margin']}\n")

    ok = bad = 0
    for slug in sorted(built["cards"]):
        files = model.find_samples(slug, root)
        if not files:
            continue
        hits = 0
        scores = []
        for f in files:
            vec = features.extract(features.load_image(f))
            if vec is None:
                continue
            guess, score, confident = model.classify(built, vec)
            scores.append(score)
            if guess == slug and confident:
                hits += 1
        n = len(scores) or 1
        mean = sum(scores) / n
        rate = hits / len(files)
        ok  += hits
        bad += len(files) - hits
        flag = "ok " if rate >= 0.8 else "WEAK"
        print(f"  {slug:<10} {hits:>3}/{len(files):<3} correct "
              f"({rate * 100:>5.1f}%)  mean {mean:.3f}  {flag}")

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
                s = model.similarity(built["cards"][a], built["cards"][b])
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
        print("  slugs from the catalog:")
        print("   ", ", ".join(registry.slugs()))
        return 1

    known = {c.slug for c in registry.all_cards()}
    for slug in sorted(os.listdir(root)):
        if os.path.isdir(os.path.join(root, slug)) and slug not in known:
            print(f"  ! '{slug}' is not in the catalog - ignored "
                  "(add it to cardscan/registry.py)")

    _banner("Training")
    built = model.build_model(root)

    if not built["cards"]:
        print("\n  nothing to train on.")
        for slug, path in sorted(found.items()):
            n = len(model.find_samples(slug, root))
            print(f"    {slug}: {n} images")
        return 1

    out = args.out
    if not out:
        out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "cardscan", "card_model.json")
    saved = model.save_model(built, out)
    size = os.path.getsize(saved)
    print(f"\n  saved {len(built['cards'])} cards -> {saved} ({size / 1024:.1f} KB)")

    if args.report:
        report(built, root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
