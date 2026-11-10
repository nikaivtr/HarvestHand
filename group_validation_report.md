# HarvestHand — Group-Based Validation Report

## Overview

Two experiments compare feature methods on the HarvestHand card scanner:

**Experiment A** — Existing 41-image dataset (20 pechay, 21 monggo),
Leave-One-Out Cross-Validation (LOOCV). All images from a single
capture session (20261109). This is the historical baseline.

**Experiment B** — Expanded dataset, group-based session cross-validation.
Images from the same capture session never appear in both training
and validation. Provides independent-session generalization estimate.

Fixed configuration: GRID=24, confidence=0.8,
top-k=3, cosine similarity, nearest-sample classifier.

## Session Information

- **pechay_plant**: 20 images, 1 sessions
- **monggo_plant**: 21 images, 1 sessions

## Experiment A — Existing 41-Image Dataset (LOOCV Baseline)

| Method | Raw acc. | Pechay acc. | Monggo acc. | Mean gap | Median gap |
|--------|----------|-------------|-------------|----------|------------|
| full_card | 0.683 | 0.650 | 0.714 | 0.004029 | 0.002979 |
| illustration_only | 0.732 | 0.700 | 0.762 | 0.003773 | 0.002566 |
| combined | 0.732 | 0.750 | 0.714 | 0.003975 | 0.002703 |

### Confusion matrices (Experiment A)

#### full_card
| Actual \ Predicted | pechay_plant | monggo_plant |
|---------------------|--------------|--------------|
| pechay_plant | 13 | 7 |
| monggo_plant | 6 | 15 |

#### illustration_only
| Actual \ Predicted | pechay_plant | monggo_plant |
|---------------------|--------------|--------------|
| pechay_plant | 14 | 6 |
| monggo_plant | 5 | 16 |

#### combined
| Actual \ Predicted | pechay_plant | monggo_plant |
|---------------------|--------------|--------------|
| pechay_plant | 15 | 5 |
| monggo_plant | 6 | 15 |

### Threshold simulations (Experiment A, confidence=0.80)

| Method | Margin | Coverage | Accepted | Correct acc. | False-accept (all) | Correct rejected |
|--------|--------|----------|----------|--------------|--------------------|------------------|
| full_card | 0.001 | 0.829 | 34 | 0.765 | 0.1951 | 2 |
| full_card | 0.003 | 0.488 | 20 | 0.750 | 0.1220 | 13 |
| full_card | 0.005 | 0.341 | 14 | 0.786 | 0.0732 | 17 |
| full_card | 0.0075 | 0.195 | 8 | 0.875 | 0.0244 | 21 |
| full_card | 0.01 | 0.049 | 2 | 0.500 | 0.0244 | 27 |
| full_card | 0.015 | 0.000 | 0 | 0.000 | 0.0000 | 28 |
| full_card | 0.02 | 0.000 | 0 | 0.000 | 0.0000 | 28 |
| full_card | 0.03 | 0.000 | 0 | 0.000 | 0.0000 | 28 |
| full_card | 0.05 | 0.000 | 0 | 0.000 | 0.0000 | 28 |
| full_card | 0.07 | 0.000 | 0 | 0.000 | 0.0000 | 28 |
| illustration_only | 0.001 | 0.854 | 35 | 0.714 | 0.2439 | 5 |
| illustration_only | 0.003 | 0.439 | 18 | 0.833 | 0.0732 | 15 |
| illustration_only | 0.005 | 0.244 | 10 | 0.700 | 0.0732 | 23 |
| illustration_only | 0.0075 | 0.195 | 8 | 0.875 | 0.0244 | 23 |
| illustration_only | 0.01 | 0.049 | 2 | 0.500 | 0.0244 | 29 |
| illustration_only | 0.015 | 0.000 | 0 | 0.000 | 0.0000 | 30 |
| illustration_only | 0.02 | 0.000 | 0 | 0.000 | 0.0000 | 30 |
| illustration_only | 0.03 | 0.000 | 0 | 0.000 | 0.0000 | 30 |
| illustration_only | 0.05 | 0.000 | 0 | 0.000 | 0.0000 | 30 |
| illustration_only | 0.07 | 0.000 | 0 | 0.000 | 0.0000 | 30 |
| combined | 0.001 | 0.854 | 35 | 0.743 | 0.2195 | 4 |
| combined | 0.003 | 0.415 | 17 | 0.824 | 0.0732 | 16 |
| combined | 0.005 | 0.341 | 14 | 0.786 | 0.0732 | 19 |
| combined | 0.0075 | 0.195 | 8 | 0.875 | 0.0244 | 23 |
| combined | 0.01 | 0.049 | 2 | 0.500 | 0.0244 | 29 |
| combined | 0.015 | 0.000 | 0 | 0.000 | 0.0000 | 30 |
| combined | 0.02 | 0.000 | 0 | 0.000 | 0.0000 | 30 |
| combined | 0.03 | 0.000 | 0 | 0.000 | 0.0000 | 30 |
| combined | 0.05 | 0.000 | 0 | 0.000 | 0.0000 | 30 |
| combined | 0.07 | 0.000 | 0 | 0.000 | 0.0000 | 30 |

## Experiment B — Expanded Dataset (Group-Based Session CV)

**Not available** — insufficient independent capture sessions for group-based validation.
All existing pechay/monggo images come from a single session (20261109).
Group-based validation requires at least 2 sessions per class (one for
training, one for validation). Please add images from additional sessions.

## Comparison: Experiment A vs Experiment B

| Method | Exp A raw acc. | Exp B raw acc. | Change |
|--------|---------------|---------------|--------|
| full_card | 0.683 | N/A | N/A |
| illustration_only | 0.732 | N/A | N/A |
| combined | 0.732 | N/A | N/A |

## Notes

- Raw results: `group_validation_results.csv`
- Threshold results analyze the same predictions, not independent validation.
- No production files, card_model.json, thresholds, or training images were modified.
- Experiment B requires multiple independent capture sessions per class.

