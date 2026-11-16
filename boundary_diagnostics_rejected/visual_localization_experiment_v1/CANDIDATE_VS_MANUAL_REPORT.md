# Candidate vs Manual Boundary Validation

This evaluation compares reconstructed experimental candidates with manually annotated boundaries. Production code, thresholds, models, and the original annotation JSON were not modified.

## Annotation eligibility

- Total annotations: **54**
- Primary benchmark: **29 `valid_complete_card` records**
- Excluded: **23 `no_usable_card`, 2 `blurred_or_damaged`**
- Annotation audit issues: **0**
- Annotation audit warnings: **0**

Only the 29 complete-card records are included in geometric accuracy.

## Geometric results

| Method | Missing | Incorrect/background | Correct <=10% diagonal | 2% / 5% / 10% corner threshold counts |
|---|---:|---:|---:|---:|
| existing | 29 | 0 | 0 | 0 / 0 / 0 |
| multi_scale | 0 | 26 | 3 | 3 / 3 / 4 |
| contrast_enhanced | 0 | 29 | 0 | 0 / 0 / 1 |
| combined | 0 | 25 | 4 | 3 / 4 / 4 |

## Per-class geometric results

| Class | Method | Eligible | Missing | Incorrect/background | Correct <=10% |
|---|---|---:|---:|---:|---:|
| pechay_plant | existing | 14 | 14 | 0 | 0 |
| pechay_plant | multi_scale | 14 | 0 | 13 | 1 |
| pechay_plant | contrast_enhanced | 14 | 0 | 14 | 0 |
| pechay_plant | combined | 14 | 0 | 13 | 1 |
| monggo_plant | existing | 15 | 15 | 0 | 0 |
| monggo_plant | multi_scale | 15 | 0 | 13 | 2 |
| monggo_plant | contrast_enhanced | 15 | 0 | 15 | 0 |
| monggo_plant | combined | 15 | 0 | 12 | 3 |

## Extractor compatibility summary

| Source | Method | Total | Preprocessing success | Feature success |
|---|---|---:|---:|---:|
| manual | manual | 29 | 18 | 18 |
| experimental | multi_scale | 29 | 13 | 13 |
| experimental | contrast_enhanced | 29 | 12 | 12 |
| experimental | combined | 29 | 14 | 14 |

Incorrect/background is defined for the ranked top candidate as maximum corner error above 10% of the image diagonal or polygon IoU below 0.50. This is a geometric evaluation rule, not a visual semantic classifier.

## Extractor results

Manual and experimental crops were passed through the unchanged `features.extract()` path. A 2,304-value vector indicates extractor compatibility only; it does not prove a correct boundary.

See `manual_crop_extractor_results.csv` for per-image results.

## Candidate reconstruction note

The original `visual_localization_results.csv` stores candidate metrics and crop paths but not corner coordinates. Therefore, the isolated experiment's candidate-generation functions were rerun for the 29 eligible images to reconstruct coordinates. This was required for geometric comparison and did not modify prior outputs.

## Recommendation

Geometric accuracy alone is not sufficient for production integration. A method should only proceed to a controlled implementation experiment after review of the comparison overlays, false positives, crop completeness, and processing cost.
