# HarvestHand — Feature-Resolution Ablation Report

## Overview

Leave-one-out cross-validation on 41 original samples (20 pechay_plant, 21 monggo_plant) comparing feature grid resolutions 12, 24, and 32. Classifier: nearest-sample with top-k=3 cosine similarity. Preprocessing identical across grids (card normalization to 120x168 5:7 canvas via cardscan.preprocess). Confidence threshold fixed at 0.80. Margin thresholds simulated: 0.001, 0.003, 0.005, 0.0075, 0.010.

## Per-Grid, Per-Method Summary

### GRID 12

| Method | Raw acc. | Per-class acc. (pechay/monggo) | Mean gap | Median gap | Min gap | Max gap |
|--------|----------|--------------------------------|----------|------------|---------|---------|
| full_card | 0.683 | 0.650 / 0.714 | 0.003735 | 0.002740 | 0.000022 | 0.011928 |
| illustration_only | 0.683 | 0.700 / 0.667 | 0.003490 | 0.002036 | 0.000289 | 0.012984 |
| combined | 0.756 | 0.750 / 0.762 | 0.003657 | 0.002508 | 0.000019 | 0.012145 |

#### Gap distributions (correct vs incorrect)

| Method | Correct n | Correct mean | Correct median | Incorrect n | Incorrect mean | Incorrect median |
|--------|-----------|--------------|----------------|-------------|----------------|------------------|
| full_card | 28 | 0.004067 | 0.003395 | 13 | 0.003019 | 0.002249 |
| illustration_only | 28 | 0.003666 | 0.002660 | 13 | 0.003111 | 0.001872 |
| combined | 31 | 0.003570 | 0.002836 | 10 | 0.003926 | 0.002268 |

#### Threshold simulations (confidence = 0.80)

| Method | Margin | Coverage | Accepted | Correct acc. | Incorrect acc. | False-accept (all) | Correct rejected |
|--------|--------|----------|----------|--------------|----------------|--------------------|------------------|
| full_card | 0.001 | 0.878 | 36 | 0.722 | 0.278 | 0.2439 | 2 |
| full_card | 0.003 | 0.488 | 20 | 0.800 | 0.200 | 0.0976 | 12 |
| full_card | 0.005 | 0.268 | 11 | 0.727 | 0.273 | 0.0732 | 20 |
| full_card | 0.0075 | 0.171 | 7 | 0.857 | 0.143 | 0.0244 | 22 |
| full_card | 0.01 | 0.073 | 3 | 0.667 | 0.333 | 0.0244 | 26 |
| illustration_only | 0.001 | 0.829 | 34 | 0.735 | 0.265 | 0.2195 | 3 |
| illustration_only | 0.003 | 0.415 | 17 | 0.765 | 0.235 | 0.0976 | 15 |
| illustration_only | 0.005 | 0.268 | 11 | 0.727 | 0.273 | 0.0732 | 20 |
| illustration_only | 0.0075 | 0.171 | 7 | 0.857 | 0.143 | 0.0244 | 22 |
| illustration_only | 0.01 | 0.024 | 1 | 0.000 | 1.000 | 0.0244 | 28 |
| combined | 0.001 | 0.854 | 35 | 0.714 | 0.286 | 0.2439 | 6 |
| combined | 0.003 | 0.439 | 18 | 0.778 | 0.222 | 0.0976 | 17 |
| combined | 0.005 | 0.268 | 11 | 0.727 | 0.273 | 0.0732 | 23 |
| combined | 0.0075 | 0.195 | 8 | 0.875 | 0.125 | 0.0244 | 24 |
| combined | 0.01 | 0.049 | 2 | 0.500 | 0.500 | 0.0244 | 30 |

### GRID 24

| Method | Raw acc. | Per-class acc. (pechay/monggo) | Mean gap | Median gap | Min gap | Max gap |
|--------|----------|--------------------------------|----------|------------|---------|---------|
| full_card | 0.683 | 0.650 / 0.714 | 0.004029 | 0.002979 | 0.000114 | 0.012723 |
| illustration_only | 0.732 | 0.700 / 0.762 | 0.003773 | 0.002566 | 0.000233 | 0.013876 |
| combined | 0.732 | 0.750 / 0.714 | 0.003975 | 0.002703 | 0.000051 | 0.013016 |

#### Gap distributions (correct vs incorrect)

| Method | Correct n | Correct mean | Correct median | Incorrect n | Incorrect mean | Incorrect median |
|--------|-----------|--------------|----------------|-------------|----------------|------------------|
| full_card | 28 | 0.004517 | 0.003466 | 13 | 0.002977 | 0.002317 |
| illustration_only | 30 | 0.003816 | 0.002977 | 11 | 0.003654 | 0.002311 |
| combined | 30 | 0.004140 | 0.002828 | 11 | 0.003525 | 0.002153 |

#### Threshold simulations (confidence = 0.80)

| Method | Margin | Coverage | Accepted | Correct acc. | Incorrect acc. | False-accept (all) | Correct rejected |
|--------|--------|----------|----------|--------------|----------------|--------------------|------------------|
| full_card | 0.001 | 0.829 | 34 | 0.765 | 0.235 | 0.1951 | 2 |
| full_card | 0.003 | 0.488 | 20 | 0.750 | 0.250 | 0.1220 | 13 |
| full_card | 0.005 | 0.341 | 14 | 0.786 | 0.214 | 0.0732 | 17 |
| full_card | 0.0075 | 0.195 | 8 | 0.875 | 0.125 | 0.0244 | 21 |
| full_card | 0.01 | 0.049 | 2 | 0.500 | 0.500 | 0.0244 | 27 |
| illustration_only | 0.001 | 0.854 | 35 | 0.714 | 0.286 | 0.2439 | 5 |
| illustration_only | 0.003 | 0.439 | 18 | 0.833 | 0.167 | 0.0732 | 15 |
| illustration_only | 0.005 | 0.244 | 10 | 0.700 | 0.300 | 0.0732 | 23 |
| illustration_only | 0.0075 | 0.195 | 8 | 0.875 | 0.125 | 0.0244 | 23 |
| illustration_only | 0.01 | 0.049 | 2 | 0.500 | 0.500 | 0.0244 | 29 |
| combined | 0.001 | 0.854 | 35 | 0.743 | 0.257 | 0.2195 | 4 |
| combined | 0.003 | 0.415 | 17 | 0.824 | 0.176 | 0.0732 | 16 |
| combined | 0.005 | 0.341 | 14 | 0.786 | 0.214 | 0.0732 | 19 |
| combined | 0.0075 | 0.195 | 8 | 0.875 | 0.125 | 0.0244 | 23 |
| combined | 0.01 | 0.049 | 2 | 0.500 | 0.500 | 0.0244 | 29 |

### GRID 32

| Method | Raw acc. | Per-class acc. (pechay/monggo) | Mean gap | Median gap | Min gap | Max gap |
|--------|----------|--------------------------------|----------|------------|---------|---------|
| full_card | 0.683 | 0.650 / 0.714 | 0.004009 | 0.002822 | 0.000019 | 0.012625 |
| illustration_only | 0.732 | 0.700 / 0.762 | 0.003831 | 0.002574 | 0.000209 | 0.014346 |
| combined | 0.732 | 0.750 / 0.714 | 0.003977 | 0.002628 | 0.000257 | 0.013353 |

#### Gap distributions (correct vs incorrect)

| Method | Correct n | Correct mean | Correct median | Incorrect n | Incorrect mean | Incorrect median |
|--------|-----------|--------------|----------------|-------------|----------------|------------------|
| full_card | 28 | 0.004545 | 0.003462 | 13 | 0.002853 | 0.002184 |
| illustration_only | 30 | 0.003914 | 0.003095 | 11 | 0.003605 | 0.002211 |
| combined | 30 | 0.004190 | 0.002927 | 11 | 0.003394 | 0.002258 |

#### Threshold simulations (confidence = 0.80)

| Method | Margin | Coverage | Accepted | Correct acc. | Incorrect acc. | False-accept (all) | Correct rejected |
|--------|--------|----------|----------|--------------|----------------|--------------------|------------------|
| full_card | 0.001 | 0.780 | 32 | 0.750 | 0.250 | 0.1951 | 4 |
| full_card | 0.003 | 0.463 | 19 | 0.737 | 0.263 | 0.1220 | 14 |
| full_card | 0.005 | 0.317 | 13 | 0.846 | 0.154 | 0.0488 | 17 |
| full_card | 0.0075 | 0.195 | 8 | 0.875 | 0.125 | 0.0244 | 21 |
| full_card | 0.01 | 0.049 | 2 | 0.500 | 0.500 | 0.0244 | 27 |
| illustration_only | 0.001 | 0.854 | 35 | 0.743 | 0.257 | 0.2195 | 4 |
| illustration_only | 0.003 | 0.463 | 19 | 0.842 | 0.158 | 0.0732 | 14 |
| illustration_only | 0.005 | 0.244 | 10 | 0.800 | 0.200 | 0.0488 | 22 |
| illustration_only | 0.0075 | 0.171 | 7 | 0.857 | 0.143 | 0.0244 | 24 |
| illustration_only | 0.01 | 0.073 | 3 | 0.667 | 0.333 | 0.0244 | 28 |
| combined | 0.001 | 0.854 | 35 | 0.743 | 0.257 | 0.2195 | 4 |
| combined | 0.003 | 0.463 | 19 | 0.789 | 0.211 | 0.0976 | 15 |
| combined | 0.005 | 0.293 | 12 | 0.833 | 0.167 | 0.0488 | 20 |
| combined | 0.0075 | 0.195 | 8 | 0.875 | 0.125 | 0.0244 | 23 |
| combined | 0.01 | 0.049 | 2 | 0.500 | 0.500 | 0.0244 | 29 |

## Notes

- Raw results: `grid_ablation_results.csv` (one row per fold, grid, method).
- Threshold results are analysis of the same LOOCV predictions, not independent validation.
- No production files, card_model.json, thresholds, or training images were modified.
