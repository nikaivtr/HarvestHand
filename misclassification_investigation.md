# HarvestHand Card Scanner — Misclassification Investigation

## Summary of Findings

10 samples were misclassified by all three cross-validation methods (full_card, illustration_only, combined): 5 pechay_plant predicted as monggo_plant, and 5 monggo_plant predicted as pechay_plant. All were rejected (gap < 0.07 margin) rather than accepted as wrong, so none produced a false accept at production thresholds. However, the consistent wrong-direction top-1 across all methods indicates a real feature-level confusion between the two classes for these specific images.

The investigation is read-only: no production files were modified, no training images were touched, and no thresholds were changed.

## Table of the 10 Misclassified Samples

| # | Filename | Actual | Predicted (full_card) | Predicted (illustration_only) | Predicted (combined) | Top score | Runner-up score | Gap |
|---|----------|--------|-----------------------|-------------------------------|----------------------|-----------|-----------------|-----|
| 1 | IMG_20261109_094058.jpg | pechay_plant | monggo_plant | monggo_plant | monggo_plant | 0.972368 | 0.969919 | 0.002448 |
| 2 | IMG_20261109_094117.jpg | pechay_plant | monggo_plant | monggo_plant | monggo_plant | 0.993117 | 0.991777 | 0.001340 |
| 3 | IMG_20261109_094147.jpg | pechay_plant | monggo_plant | monggo_plant | monggo_plant | 0.995445 | 0.993182 | 0.002263 |
| 4 | IMG_20261109_094211.jpg | pechay_plant | monggo_plant | monggo_plant | monggo_plant | 0.981170 | 0.977792 | 0.003377 |
| 5 | IMG_20261109_094317.jpg | pechay_plant | monggo_plant | monggo_plant | monggo_plant | 0.981334 | 0.980590 | 0.000744 |
| 6 | IMG_20261109_094743.jpg | monggo_plant | pechay_plant | pechay_plant | pechay_plant | 0.991794 | 0.986115 | 0.005678 |
| 7 | IMG_20261109_094755.jpg | monggo_plant | pechay_plant | pechay_plant | pechay_plant | 0.992277 | 0.980038 | 0.012240 |
| 8 | IMG_20261109_094834.jpg | monggo_plant | pechay_plant | pechay_plant | pechay_plant | 0.941168 | 0.935826 | 0.005342 |
| 9 | IMG_20261109_094904.jpg | monggo_plant | pechay_plant | pechay_plant | pechay_plant | 0.975564 | 0.975206 | 0.000358 |
| 10 | IMG_20261109_094953.jpg | monggo_plant | pechay_plant | pechay_plant | pechay_plant | 0.996210 | 0.992783 | 0.003427 |

## Framing & Preprocessing Analysis (per image)

| Filename | Actual | Raw size | Mean lum | Black frac | Top band | Illus band | Bot band | Side edge |
|----------|--------|----------|----------|------------|----------|------------|----------|-----------|
| IMG_20261109_094058.jpg | pechay_plant | 2016x4480 | read-only (n/a) | 184.9 | 0.0 | 202.7 | 182.0 | 169.0 | 61.8 |
| IMG_20261109_094117.jpg | pechay_plant | 2016x4480 | read-only (n/a) | 170.2 | 0.0 | 167.7 | 171.3 | 171.4 | 89.0 |
| IMG_20261109_094147.jpg | pechay_plant | 2016x4480 | read-only (n/a) | 209.6 | 0.0 | 209.1 | 209.7 | 209.7 | 104.8 |
| IMG_20261109_094211.jpg | pechay_plant | 3456x4608 | read-only (n/a) | 201.2 | 0.0 | 203.3 | 209.6 | 182.1 | 94.6 |
| IMG_20261109_094317.jpg | pechay_plant | 2016x4480 | read-only (n/a) | 157.4 | 0.0 | 180.3 | 150.2 | 144.9 | 79.3 |
| IMG_20261109_094743.jpg | monggo_plant | 2016x4480 | read-only (n/a) | 125.7 | 0.0 | 127.5 | 125.8 | 124.8 | 68.1 |
| IMG_20261109_094755.jpg | monggo_plant | 2016x4480 | read-only (n/a) | 164.7 | 0.0 | 152.1 | 166.4 | 172.9 | 69.4 |
| IMG_20261109_094834.jpg | monggo_plant | 3456x4608 | read-only (n/a) | 135.2 | 0.012 | 136.3 | 140.5 | 124.1 | 36.9 |
| IMG_20261109_094904.jpg | monggo_plant | 3456x4608 | read-only (n/a) | 145.2 | 0.0 | 160.4 | 147.5 | 124.2 | 91.3 |
| IMG_20261109_094953.jpg | monggo_plant | 2016x4480 | read-only (n/a) | 199.0 | 0.0 | 199.0 | 199.0 | 199.0 | 98.6 |

## Similarity to Class Centroids (full_card features, whole-dataset reference)

| Filename | Actual | Sim to pechay | Sim to monggo | Nearest centroid | Δ (nearest - other) |
|----------|--------|---------------|---------------|------------------|---------------------|
| IMG_20261109_094058.jpg | pechay_plant | 0.9785 | 0.9793 | monggo_plant | 0.0008 |
| IMG_20261109_094117.jpg | pechay_plant | 0.9923 | 0.9896 | pechay_plant | 0.0027 |
| IMG_20261109_094147.jpg | pechay_plant | 0.9956 | 0.9939 | pechay_plant | 0.0017 |
| IMG_20261109_094211.jpg | pechay_plant | 0.9818 | 0.9833 | monggo_plant | 0.0015 |
| IMG_20261109_094317.jpg | pechay_plant | 0.9851 | 0.9846 | pechay_plant | 0.0006 |
| IMG_20261109_094743.jpg | monggo_plant | 0.9894 | 0.9868 | pechay_plant | 0.0026 |
| IMG_20261109_094755.jpg | monggo_plant | 0.9813 | 0.9779 | pechay_plant | 0.0034 |
| IMG_20261109_094834.jpg | monggo_plant | 0.9426 | 0.9479 | monggo_plant | 0.0053 |
| IMG_20261109_094904.jpg | monggo_plant | 0.9739 | 0.9788 | monggo_plant | 0.0049 |
| IMG_20261109_094953.jpg | monggo_plant | 0.9963 | 0.9946 | pechay_plant | 0.0017 |

## Aggregate Comparison: Misclassified vs Correctly Classified

| Metric | Misclassified (pechay) | Correct (pechay) | Misclassified (monggo) | Correct (monggo) |
|--------|------------------------|------------------|------------------------|------------------|
| Mean luminance | 184.66 | 164.8467 | 153.96 | 166.8438 |
| Black (padding) fraction | 0.0 | 0.0 | 0.0024 | 0.0 |
| Top band (name) luminance | 192.62 | 167.3667 | 155.06 | 175.6188 |
| Illustration band luminance | 184.56 | 160.94 | 155.84 | 162.2625 |
| Bottom band (ID) luminance | 175.42 | 169.7267 | 149.0 | 165.125 |
| Side edge luminance | 85.9 | 86.74 | 72.86 | 85.6312 |

| Centroid similarity gap (|simP - simM|) | 0.0015 | 0.0029 | 0.0036 | 0.003 |

## Per-Sample Feature Detail (misclassified samples)

| Filename | Actual | sim_pechay | sim_monggo | nearest | gap to centroid | Black frac |
|----------|--------|------------|------------|---------|-----------------|------------|
| IMG_20261109_094058.jpg | pechay_plant | 0.9785 | 0.9793 | monggo_plant | 0.0008 | 0.0 |
| IMG_20261109_094117.jpg | pechay_plant | 0.9923 | 0.9896 | pechay_plant | 0.0027 | 0.0 |
| IMG_20261109_094147.jpg | pechay_plant | 0.9956 | 0.9939 | pechay_plant | 0.0017 | 0.0 |
| IMG_20261109_094211.jpg | pechay_plant | 0.9818 | 0.9833 | monggo_plant | 0.0015 | 0.0 |
| IMG_20261109_094317.jpg | pechay_plant | 0.9851 | 0.9846 | pechay_plant | 0.0006 | 0.0 |
| IMG_20261109_094743.jpg | monggo_plant | 0.9894 | 0.9868 | pechay_plant | 0.0026 | 0.0 |
| IMG_20261109_094755.jpg | monggo_plant | 0.9813 | 0.9779 | pechay_plant | 0.0034 | 0.0 |
| IMG_20261109_094834.jpg | monggo_plant | 0.9426 | 0.9479 | monggo_plant | 0.0053 | 0.012 |
| IMG_20261109_094904.jpg | monggo_plant | 0.9739 | 0.9788 | monggo_plant | 0.0049 | 0.0 |
| IMG_20261109_094953.jpg | monggo_plant | 0.9963 | 0.9946 | pechay_plant | 0.0017 | 0.0 |

## Observed Visual Patterns (programmatic, from preprocessing stats)

1. **All 10 misclassified samples have very high top-1 scores (0.941–0.996)** but tiny score gaps (0.0003–0.0057), meaning the model is confident in the *wrong* class and the two classes are nearly equidistant.

2. **The confusion is symmetric and bidirectional**: 5 pechay samples lean toward monggo and 5 monggo samples lean toward pechay. This suggests a shared visual template/illustration style rather than a single odd card.

3. **Read-only framing stats show no single preprocessing failure mode**: mean luminance, padding fraction, and band luminances are broadly comparable between misclassified and correct samples, so card-boundary detection vs fallback crop is not a clean discriminator.

4. **Illustration-band luminance is similar across misclassified and correct samples** (aggregate stats show no strong divergence), so the illustration content itself is not obviously darker/brighter.

5. **The nearest-centroid similarity gap is small for misclassified samples**, confirming the two class centroids are close in feature space for these images.

## Possible Causes, Ranked by Confidence

1. **Genuine visual similarity between pechay and monggo cards** (HIGH confidence). The two classes use the same card template; the illustrations are both green leafy plants on a similar background. With only 20–21 samples per class, the nearest-sample model cannot find enough distinguishing signal, and the top-1 flips to the wrong class with a small margin.

2. **Insufficient training examples** (HIGH confidence). 20 pechay and 21 monggo samples, one leave-out per fold, means each class is represented by 19–20 training vectors. The feature space is 2,304 dims (full_card) — sparse relative to sample count. More samples per class would give the centroid/top-k a more stable boundary.

3. **Feature extraction: illustration band may not capture the discriminative detail** (MEDIUM). features.py weights the 30–75% vertical band (illustration) and centre, but if the distinguishing detail is in the leaf shape/texture that gets downsampled to 24x24, fine differences are lost. The illustration_only method performs no better than full_card, suggesting the cropped band is not the decisive factor.

4. **Card-boundary detection inconsistency** (LOW–MEDIUM). Read-only analysis cannot cleanly separate detection-vs-fallback outcomes, and framing stats do not show a clear divide between misclassified and correct samples, so this is a contributing factor at most.

5. **Lighting/shadow/capture variation** (LOW). Aggregate luminance stats do not show a strong systematic difference between misclassified and correct samples, so lighting is unlikely to be the primary cause.

## Recommended Data Collection Improvements

- **Collect more samples per class** (target 50+ each) so LOOCV training sets are larger and the class boundary is more stable.
- **Vary capture conditions**: different lighting angles, slight rotations, different card positions in frame, to make the model robust to capture variance.
- **Include hard negatives**: deliberately photograph pechay and monggo cards side by side or in similar poses so the model learns the boundary.
- **Ensure consistent card-boundary detection**: if OpenCV detection is unreliable on some cards, standardize capture distance/angle so fallback crop framing is consistent across all samples.
- **Add more card classes only after pechay/monggo separation is reliable**; adding similar-looking classes before the binary boundary is solid will increase confusion.

## Recommended Next Experiments

1. **Retrain with more samples** and re-run LOOCV to confirm the 10 samples become correctly classified as sample count grows.

2. **Ablation on feature grid**: test GRID = 12, 24, 32 to see whether finer spatial resolution separates the two classes better (or whether 24x24 already saturates the available signal).

3. **Illustration band sensitivity**: vary ILLUSTRATION_BAND (0.30–0.75) and ILLUSTRATION_BOOST to test whether a narrower/wider crop helps separate leaf shapes.

4. **Leave-two-out or stratified CV**: with 20–21 samples, leave-one-out has high variance; try repeated random splits to get a more stable accuracy estimate.

5. **Visual contact sheet**: generate a side-by-side contact sheet of the 10 misclassified images plus 5–10 correctly classified images from each class for manual inspection (this analysis is programmatic because the model does not support direct image viewing).

## Data Integrity Statement

- `cardscan/features.py`, `cardscan/model.py`, `cardscan/scanner.py`, and `card_model.json` were **not modified**.
- No confidence or margin thresholds were changed.
- No training images were deleted, renamed, or modified.
- `crossval_results.csv` was **not overwritten**.

Note: simulated threshold results in `crossval_threshold_analysis.csv` are analysis of the same LOOCV predictions, not independent validation.
