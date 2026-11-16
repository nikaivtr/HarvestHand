import os
import sys
import time

sys.path.insert(0, 'D:/HarvestHand')
import cardscan.features as features
import cardscan.model as model

# Load 5 pechay images only
base_path = 'D:/HarvestHand/data/card_samples/pechay_plant'
all_files = sorted(os.listdir(base_path))
img_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))]
img_files = img_files[:5]

print(f'Loading {len(img_files)} pechay images...')
surfaces = []
for f in img_files:
    s = features.load_image(os.path.join(base_path, f))
    if s is not None:
        surfaces.append(s)

print(f'Loaded {len(surfaces)} surfaces')

# Pre-extract features
all_vectors = [features.extract(s) for s in surfaces]

print('Running LOOCV on 5 images...')
t0 = time.time()

results = []
for i in range(len(surfaces)):
    left_vec = all_vectors[i]
    other_indices = [j for j in range(len(surfaces)) if j != i]
    
    class_to_vecs = {}
    for j in other_indices:
        cls = 'pechay_plant'
        if cls not in class_to_vecs:
            class_to_vecs[cls] = []
        class_to_vecs[cls].append(all_vectors[j])
    
    tmp_model = {
        "feature_version": features.PREPROCESS_VERSION,
        "grid": features.GRID,
        "cards": {},
        "threshold": model.DEFAULT_THRESHOLD,
        "margin": model.DEFAULT_MARGIN,
        "model_version": model.MODEL_VERSION,
    }
    for cls, vecs in class_to_vecs.items():
        valid = [v for v in vecs if v is not None]
        if valid:
            tmp_model["cards"][cls] = {"samples": valid, "centroid": None}
    
    detail = model.classify_detailed(tmp_model, left_vec)
    results.append({
        "image": img_files[i],
        "predicted": detail["slug"],
        "score": detail["best_score"],
        "gap": detail["gap"],
        "accepted": detail["confident"],
    })
    print(f'  {img_files[i]}: {detail["slug"]} | {detail["best_score"]:.4f} | gap={detail["gap"]:.4f} | acc={detail["confident"]}')

t1 = time.time()
print(f'Completed {len(results)} iterations in {t1 - t0:.2f} seconds')
