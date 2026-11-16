# Visual Localization Experiment v1

This isolated experiment evaluates visual-only localization on the 54 boundary-category failures. Production files and thresholds were not modified.

## Important limitation

No independent corner annotations were supplied. Experimental quadrilaterals are therefore candidates, not verified card boundaries. `strong` and `possible` describe the ranking heuristics only. Visual correctness is `N/A` until the manual review CSV is completed.

## Method comparison

| Method | Candidate images | Strong | Possible | Extractor-compatible | Mean time (ms) |
|---|---:|---:|---:|---:|---:|
| existing | 0 | 0 | 0 | 0 | 19.45 |
| multi_scale | 54 | 49 | 3 | 0 | 2843.2 |
| contrast_enhanced | 54 | 42 | 11 | 0 | 4358.97 |
| combined | 54 | 50 | 3 | 0 | 16842.54 |

Visually verified correct boundaries: **N/A**. Background false positives: **N/A** until manual review is supplied.

## Combined method interpretation

The combined method searches multiple scales, contrast variants, edge maps, and contour approximations, then ranks candidates using geometry, edge continuity, border contrast, and a capped area term. It does not use class identity to accept a boundary.

The existing extractor test is separate from geometric correctness. A passing 2,304-value vector means only that the unchanged production preprocessing path accepted the experimental crop.

## Outputs

- `visual_localization_results.csv`: one row per image and method.
- `method_comparison.csv`: aggregate method comparison.
- `detection_overlays/`: top combined candidates, color-coded by heuristic category.
- `corrected_candidate_crops/`: crops from the combined top candidate.
- `contact_sheets/`: crop and method-comparison sheets.
- `manual_review/`: annotation template and instructions.

## Recommendation

Do not promote this detector or lower production thresholds from candidate counts alone. The next development stage should manually annotate the 54 images, calculate true/false boundary rates, and then tune the ranking weights against those annotations. If multi-scale candidates are visually correct, implement only the smallest validated candidate-generation change and re-test false accepts.
