content = '''#!/usr/bin/env python3
import csv
import os
import sys
from pathlib import Path
sys.path.insert(0, '.')
import pygame
import cardscan.preprocess as p
import cardscan.features as f
import cardscan.model as m
import cardscan.registry as r

PROD_THRESHOLD = 0.80
PROD_MARGIN = 0.07
GRID = 24
CLASSES = ("pechay_plant", "monggo_plant")
EXPECTED_COUNTS = {"pechay_plant": 21, "monggo_plant": 21}
OUTPUT_CSV = "crossval_results.csv"

all_samples = []
for slug in CLASSES:
    card = r.get(slug)
    if card is None:
        raise RuntimeError(f"Card not found: {slug}")
    folder = Path(card.sample_folder)
    paths = sorted([x for x in folder.iterdir() if x.is_file() and x.suffix.lower() in m.IMAGE_EXTS])
    print(f"{slug}: {len(paths)} files")
    for path in paths:
        all_samples.append((slug, card.name, path.resolve()))

print(f"Total samples: {len(all_samples)}")
assert sum(1 for s in all_samples if s[0]=="pechay_plant") == 21
assert sum(1 for s in all_samples if s[0]=="monggo_plant") == 21
print("Dataset verification PASSED")

results = []
for test_idx, (actual_slug, target_name, test_path) in enumerate(all_samples):
    im_test = p.load_image(test_path)
    c_test = p.prepare(im_test)
    v_test = f.extract(c_test)
    ch, cw = c_test.get_size()
    y_start = int(ch * 0.25); y_end = int(ch * 0.75)
    ill_card = c_test.subsurface(pygame.Rect(0, y_start, cw, y_end - y_start))
    ill_small = pygame.transform.smoothscale(ill_card, (GRID, GRID))
    v_ill = f.extract(ill_small)

    train_paths = [s for s in all_samples if s[2] != test_path]

    for method_key in ("full_card", "illustration_only", "combined"):
        if method_key == "full_card": v = v_test
        elif method_key == "illustration_only": v = v_ill
        else: v = v_test + v_ill

        vectors_by_class = {"pechay_plant": [], "monggo_plant": []}
        for slug, name, path in train_paths:
            im = p.load_image(path)
            c = p.prepare(im)
            if c is None: continue
            v_train = f.extract(c)
            if v_train is None: continue
            vectors_by_class[slug].append(v_train)

        cards = {}
        for slug in ("pechay_plant", "monggo_plant"):
            vecs = vectors_by_class[slug]
            cards[slug] = {"centroid": m._mean(vecs), "samples": vecs, "n": len(vecs)}

        model = {"version": m.MODEL_VERSION, "feature_version": f.PREPROCESS_VERSION,
                 "grid": GRID, "threshold": PROD_THRESHOLD, "margin": PROD_MARGIN,
                 "cards": cards}
        detail = m.classify_detailed(model, v, threshold=PROD_THRESHOLD, margin=PROD_MARGIN)

        results.append({
            "fold": test_idx + 1, "path": str(test_path), "method": method_key,
            "actual": actual_slug, "predicted": detail["best_slug"],
            "score": detail["best_score"], "runner_slug": detail["runner_slug"],
            "runner_score": detail["runner_score"], "gap": detail["gap"],
            "accepted": detail["confident"], "reason": detail["reason"],
        })

print("\n" + "="*65)
print("LOOCV RESULTS")
print("="*65)

for method_key in ("full_card", "illustration_only", "combined"):
    rs = [r for r in results if r["method"] == method_key]
    n = len(rs)
    correct = sum(1 for r in rs if r["predicted"] == r["actual"])
    accepted = [r for r in rs if r["accepted"]]
    fa = sum(1 for r in accepted if r["actual"] != r["predicted"])
    gaps = [r["gap"] for r in rs if r["gap"] is not None]
print("\n=== Threshold Simulation ===")
print(f"{'Margin':>8} {'Cov':>8} {'Acc':>8} {'FA':>6} {'FAR':>8} {'AccR':>8} {'PechCov':>8} {'MongCov':>8} {'PechAcc':>8} {'MongAcc':>8}")
for margin in (0.001, 0.002, 0.003, 0.004, 0.005, 0.0075, 0.010, 0.015, 0.020, 0.030, 0.050, 0.070):
    accepted = [r for r in results if r["accepted"] and float(r["gap"]) >= margin]
    n = len(results)
    cov = len(accepted) / n * 100 if n else 0
    ca = [r for r in accepted if r["actual"] == r["predicted"]]
    wa = [r for r in accepted if r["actual"] != r["predicted"]]
    ar = len(ca) / len(accepted) * 100 if accepted else 0
    far = len(wa) / n * 100 if n else 0
    pechay_all = [r for r in results if r["actual"] == "pechay_plant" and r["accepted"] and float(r["gap"]) >= margin]
    monggo_all = [r for r in results if r["actual"] == "monggo_plant" and r["accepted"] and float(r["gap"]) >= margin]
    pechay_c = [r for r in pechay_all if r["predicted"] == "pechay_plant"]
    monggo_c = [r for r in monggo_all if r["predicted"] == "monggo_plant"]
    pech_cov = len(pechay_all) / len([r for r in results if r["actual"] == "pechay_plant"]) * 100
    mong_cov = len(monggo_all) / len([r for r in results if r["actual"] == "monggo_plant"]) * 100
    pech_acc = len(pechay_c) / len(pechay_all) * 100 if pechay_all else 0
    mong_acc = len(monggo_c) / len(monggo_all) * 100 if monggo_all else 0
    print(f"{margin:>8.3f} {cov:>7.1f}% {ar:>7.1f}% {len(wa):>6} {far:>7.1f}% {ar:>7.1f}% {pech_cov:>7.1f}% {mong_cov:>7.1f}% {pech_acc:>7.1f}% {mong_acc:>7.1f}%")

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["fold","path","method","actual","predicted","score","runner_slug","runner_score","gap","accepted","reason"])
    writer.writeheader()
    writer.writerows(results)
print(f"\nCSV saved to crossval_results.csv")
print("\nDIAGNOSTIC COMPLETE - Production card_model.json was not modified.")
'''
pathlib.Path('run_crossval.py').write_text(content, encoding='utf-8')
print('run_crossval.py written successfully')
    print(f"\n--- {method_key.upper()} ---")
    print(f"  Samples: {n}")
    print(f"  Accuracy: {correct/n*100:.1f}% ({correct}/{n})")
    print(f"  Coverage: {len(accepted)/n*100:.1f}% ({len(accepted)}/{n})")
    print(f"  Correct among accepted: {sum(1 for r in accepted if r[\"actual\"]==r[\"predicted\"])/len(accepted)*100:.1f}% ({sum(1 for r in accepted if r[\"actual\"]==r[\"predicted\"])}/{len(accepted)})")
    print(f"  False accepts: {fa}")
    print(f"  False-accept rate: {fa/n*100:.1f}%")
    print(f"  Rejected: {len(rejected)} ({len(rejected)/n*100:.1f}%)")
    print(f"  Correct but rejected: {sum(1 for r in rejected if r[\"predicted\"]==r[\"actual\"])}")
    print(f"  Mean gap: {sum(gaps)/len(gaps):.6f}")
    print(f"  Min gap: {min(gaps):.6f}")
    print(f"  Max gap: {max(gaps):.6f}")
    for cls in ("pechay_plant", "monggo_plant"):
        cls_rows = [r for r in rs if r["actual"] == cls]
        cls_correct = sum(1 for r in cls_rows if r["predicted"] == cls)
        print(f"  {cls}: {cls_correct}/{len(cls_rows)} ({cls_correct/len(cls_rows)*100:.1f}%)")