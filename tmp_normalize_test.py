"""Test per-image color normalization before feature extraction."""
import os, sys, math
sys.path.insert(0, r'D:\HarvestHand')
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame
import cardscan.features as features
import cardscan.model as model
pygame.init()

PECHAY_DIR = r'D:\HarvestHand\data\card_samples\pechay_plant'
MONGGO_DIR = r'D:\HarvestHand\data\card_samples\monggo_plant'
EXTS = ('.jpg', '.jpeg', '.png')

def list_imgs(d):
    return sorted(
        os.path.join(d, f) for f in os.listdir(d)
        if f.lower().endswith(EXTS) and os.path.isfile(os.path.join(d, f))
    )

def zscore_color(vec):
    n = len(vec)
    out = [0.0] * n
    for c in range(3):
        vals = [vec[i] for i in range(c, n, 3)]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / len(vals)
        std = math.sqrt(var)
        if std < 1e-9:
            std = 1.0
        for i in range(c, n, 3):
            out[i] = (vec[i] - mean) / std
    return out

def color_ratio(vec):
    n = len(vec)
    out = [0.0] * n
    for i in range(0, n, 4):
        r = vec[i]; g = vec[i + 1]; b = vec[i + 2]
        s = r + g + b
        if s > 1e-9:
            out[i] = r / s; out[i + 1] = g / s; out[i + 2] = b / s
        else:
            out[i] = r; out[i + 1] = g; out[i + 2] = b
        out[i + 3] = vec[i + 3]
    return out

def whiten_global(vec):
    n = len(vec)
    out = [0.0] * n
    for c in range(3):
        vals = [vec[i] for i in range(c, n, 3)]
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / len(vals)
        std = math.sqrt(var)
        if std < 1e-9:
            std = 1.0
        for i in range(c, n, 3):
            out[i] = (vec[i] - mean) / std
    for i in range(3, n, 4):
        out[i] = vec[i]
    return out

def loocv(vectors, transform):
    """Proper LOOCV: hold out one image, train on the other 41."""
    correct = 0
    total = 0
    gaps = []
    for idx, (label, vec) in enumerate(vectors):
        train = [vectors[j] for j in range(len(vectors)) if j != idx]
        train = [(l, transform(v)) for l, v in train]
        by_class = {}
        for l, v in train:
            by_class.setdefault(l, []).append(v)
        scored = []
        for cls, samples in by_class.items():
            sims = [model.similarity(transform(vec), s) for s in samples]
            sims.sort(reverse=True)
            k = min(3, len(sims))
            scored.append((sum(sims[:k]) / k, cls))
        scored.sort(reverse=True)
        pred = scored[0][1] if scored else None
        if pred == label:
            correct += 1
        total += 1
        if len(scored) > 1:
            gaps.append((scored[0][0] - scored[1][0], label, pred))
    acc = correct / total * 100 if total else 0
    return acc, correct, total, gaps

def run(name, transform):
    vectors = []
    for d, label in [(PECHAY_DIR, 'pechay_plant'), (MONGGO_DIR, 'monggo_plant')]:
        for p in list_imgs(d):
            surf = features.load_image(p)
            vec = features.extract(surf)
            if vec is None:
                print(f"  SKIP {p}")
                continue
            vectors.append((label, vec))
    acc, correct, total, gaps = loocv(vectors, transform)
    gap_vals = [g[0] for g in gaps]
    mean_gap = sum(gap_vals) / len(gap_vals) if gap_vals else 0
    max_gap = max(gap_vals) if gap_vals else 0
    min_gap = min(gap_vals) if gap_vals else 0
    print(f"\n=== {name} ===")
    print(f"  accuracy: {acc:.1f}%  ({correct}/{total})")
    print(f"  gap: mean={mean_gap:.4f} min={min_gap:.4f} max={max_gap:.4f}")
    for cls in ['pechay_plant', 'monggo_plant']:
        cls_correct = sum(1 for g in gaps if g[1] == cls and g[2] == cls)
        cls_total = sum(1 for g in gaps if g[1] == cls)
        print(f"  {cls}: {cls_correct}/{cls_total}")
    return acc, gaps

run('baseline (no transform)', lambda v: v)
run('zscore per color channel', zscore_color)
run('color ratio (chromaticity)', color_ratio)
run('global whiten', whiten_global)
run('zscore then color ratio', lambda v: color_ratio(zscore_color(v)))