# Recognition Lab Detection Regression Audit

**Audit timestamp:** 2026-11-17T16:59:27+08:00  
**Scope:** `recognition_lab/` only  
**Mode:** Investigation-only; no detector, threshold, model, annotation, or production-file changes were made.

## Executive conclusion

The evidence does not show that the current contour engine suddenly lost all of its previous behavior. The current engine and the preserved `reports/phase1_baseline_snapshot/engines.py` produce the same candidate result on the current 14-image boundary-reference collection: 1/14 images produces a candidate, with IoU 0.777 on that case, and the other 13 produce no candidate. The preserved eight-image pipeline report independently shows the same upstream failure pattern: seven images have no pre-filter quadrilateral with IoU at least 0.50 and the one accepted quadrilateral is an internal region.

The observed regression is therefore mainly a live-pipeline and acceptance problem layered on top of a pre-existing candidate-generation limitation:

1. **The detector is a geometry-based candidate generator, not a card classifier.** Bright regions, table surfaces, and arbitrary rectangles that satisfy the geometric filters are valid candidates.
2. **There is no final live rejection gate.** Phase 1 queues every generated candidate for review. The stored database now contains 261 manually judged `INCORRECT` candidates.
3. **The stored card data was historically not active in the live path.** Before the latest change, `outer_profile` was passed only when the benchmark setting was present. The current fallback profile ranks candidates, but does not reject false candidates or create missing outer boundaries.
4. **The 640-pixel live downscale changed candidate geometry.** It was introduced in commit `2bc80de` and reverted in `9b5bbd3` after the reported degradation. It is not present in the current code.
5. **Full-resolution live detection is slow.** On the current machine, current-engine timings ranged from approximately 333–1,096 ms for 1920x1080 references. The asynchronous worker keeps the UI responsive, but it does not increase detector throughput.
6. **The current physical-card collection is not a successful detector benchmark.** It contains 14 references from multiple sessions and resolutions; only one currently produces a candidate. This is a generation failure, not a ranking failure.

## Current inventory and evidence

### Boundary references

- 14 manually annotated references.
- Conditions: Flat on Table 2, Tilted Right 4, Tilted Left 4, Held by Hand 4.
- 8 images are 640x480; 6 images are 1920x1080.
- The prior eight-image audit is preserved and is not overwritten.
- Current replay against the current engine: 1/14 produced a candidate; 13/14 produced none.
- The one matching result is the existing flat 640x480 reference with IoU 0.777.
- The 1920x1080 reference replay produced 0/6 candidates.

The current replay was also run against the preserved baseline engine snapshot. Candidate counts and IoU outcomes matched the current engine on all 14 images. The current engine was slower because it computes additional diagnostic edge-support features.

### Stored candidate judgments

The current SQLite store contains:

- 48 `CORRECT`
- 261 `INCORRECT`
- 1 `UNSURE`
- 310 total annotations

These are human judgments of queued candidates, not automatically generated ground truth. The historical phase-1 audit report with 276 records and 227 incorrect records is an older snapshot; the current store has since grown and must not be mixed with that older count.

Among the 261 current incorrect records:

- 217 came from `canny_50_150`.
- 44 came from `canny_25_100`.
- Area ratio ranged from 0.010016 to 0.833625.
- Aspect ratio ranged from 0.4501 to 0.8984.
- Edge support ranged from 0.08 to 0.9299.
- Confidence ranged from 0.4774 to 0.8550.

These ranges overlap the configured card-like geometry ranges. That is direct evidence that geometric validity does not distinguish a physical card from a background rectangle.

## Pipeline findings

The current pipeline is:

1. BGR to grayscale.
2. Gaussian blur `(5,5)`.
3. Three masks: Canny `(50,150)`, Canny `(25,100)`, and adaptive threshold `(31,5)`.
4. Morphological close with a `5x5` kernel for two iterations.
5. `findContours(RETR_LIST, CHAIN_APPROX_SIMPLE)`.
6. `approxPolyDP` with epsilon `0.025 * perimeter`.
7. Four vertices, convexity, area ratio, aspect ratio, edge support, and geometry validation.
8. Duplicate suppression.
9. Nested-region annotation.
10. Ranking by outer-reference score and confidence when ranking is enabled.

The relevant implementation is [`engines.py`](../engines.py), especially `detect_boundary_candidates`, `candidate_metrics`, and `validate_quad_geometry`.

### Candidate generation versus acceptance

The preserved pipeline diagnostic traced 979 contours across the original eight references. It recorded:

- 633 non-four-vertex rejections.
- 33 non-convex rejections.
- 310 filter/geometry rejections.
- 1 accepted quadrilateral before final ranking.

The most frequent recorded rejection reasons were:

- Area outside limits: 620.
- Implausible card aspect: 374.
- Collapsed edge: 236.
- Insufficient edge support: 187.

This identifies candidate generation and contour approximation as the main physical-card bottleneck. Ranking cannot recover a card quadrilateral that was never generated.

At the same time, arbitrary rectangles that survive those filters are queued. In [`lab_main.py`](../lab_main.py), `_collect_review_candidate` persists generated candidates; it does not require a card-profile score or a physical-card acceptance decision. The `CORRECT` button guard is a review UX rule, not a live detector rejection gate.

## False-positive investigation

The available stored false positives are manually judged incorrect candidates with preserved frame paths and metrics. Their metrics demonstrate that they were accepted because they passed geometry and edge-support filters, not because the system identified card appearance.

The likely sources are:

- Bright lighting or table regions producing Canny contours.
- Background or object rectangles with card-like aspect ratios.
- Internal or unrelated panels that satisfy the area and edge-support thresholds.
- Candidate generation from multiple masks, especially `canny_50_150`.

The current implementation does not contain a semantic material classifier, color/lighting rejection, or validated card-image matching gate. The profile in `analysis.py` is a feature-distance ranking score only. It is not a trained model and is not used to reject candidates.

## False-negative investigation

The evidence classifies the physical-card failures as primarily **candidate-generation failures**:

- Seven of the original eight reference images had no sufficiently matching pre-filter quadrilateral.
- The one accepted candidate was an internal region, not the physical outer boundary.
- Current replay of the expanded 14-reference set gives 13/14 with no candidate.
- There is no evidence that the actual card candidate was generated and then lost only during ranking for this collection.

Tracking is a separate live concern. The asynchronous Phase 1 path calls the tracker with `detected=False` while the worker is still processing. This preserves existing tracks temporarily as `tracked`; it can make an old candidate remain visible for the grace period, but it does not explain the generation failure on still images.

## Feedback and experimental-data audit

No model-training code or learned model was found in the Recognition Lab. The stored profile uses feature summaries from manually judged rows:

- Positive distribution: 48 `CORRECT`.
- Negative distribution: 261 `INCORRECT`.

The data is not automatically relabeled. However, it is not an independent classifier-training set:

- Incorrect candidates were generated by the same geometry pipeline being evaluated.
- The positive set is small and comes from reviewed candidate crops, not a broad independent card corpus.
- The current reference collection has limited independent-session evidence.
- The live profile uses feature statistics, not image appearance.
- Stored duplicates and near-duplicates exist in historical candidate captures.

This is calibration evidence with selection bias, not proof that the detector can recognize cards.

## Regression timeline

| Time | Evidence | Interpretation |
|---|---|---|
| 11:07 | Initial detector commit `b615ad9` | Original contour-based candidate generation. |
| 12:17 | `8af22da` | Added explicit quadrilateral geometry validation, edge-support filtering, and distance-based duplicate suppression. This increased rejection strictness and changed the candidate pipeline substantially. |
| 12:54 | `19d8279` | Tightened defaults from approximately aspect `0.30–0.98` and edge support `0.05` to aspect `0.45–0.90` and edge support `0.08`; added outer-profile ranking and nested-region flags. This is a plausible false-negative risk, but not proven as the cause of the current live false positives. |
| 12:59 | `341ebb1` | Added optional ranking control and made live profile use conditional on a persisted benchmark. When that setting was absent, live candidates had no stored-profile score. |
| 13:32 | `00674fa` | Added audit/benchmark analysis and session comparison. |
| 14:44 | `dfd09c9` | Added corner/parallel edge-support metrics and an experimental outer score. The experimental score defaults off in the live detector. The added metrics increased processing cost. |
| 15:25 | `1747f2b` | Evaluation/UI changes; no new engine change shown. |
| 16:39 | `a021c0d` | Moved detection to an asynchronous worker and changed tracking behavior while a detection is pending. This improves UI responsiveness but does not improve detection quality. |
| 16:44 | `2bc80de` | Added a live 640-pixel processing downscale. This changed contour geometry and was later identified by observation as worsening card-corner detection. |
| 16:51 | `9b5bbd3` | Reverted the downscale and enabled a live profile fallback from stored labels. The profile affects ranking only; it is not a final acceptance gate. |

## Last known reliable state

The last evidence-backed baseline is preserved in [`reports/phase1_baseline_snapshot/`](.). The associated phase-1 audit recorded 48 manually correct references with:

- 89.58% IoU-at-least-0.50 generation recall.
- 89.58% IoU-at-least-0.75 generation recall.
- 5 generation failures.
- 5 internal-region failures.
- Mean processing time approximately 464.6 ms.

This was reliable only for that existing 640x480 reviewed-candidate corpus. It did not establish reliable physical-card recognition on the later boundary-reference collection.

## Root-cause hypotheses ranked by evidence

1. **No semantic final acceptance gate — high confidence.** The system queues every geometrically valid quadrilateral; the 261 current incorrect judgments prove this path.
2. **Upstream outer-boundary generation failure — high confidence.** Existing pipeline diagnostics show the physical boundary is absent before ranking on most references.
3. **Camera-resolution/content mismatch — high confidence for the live regression.** The expanded 1920x1080 reference set produces no candidates, while the one successful replay is an older 640x480 image.
4. **Live downscale altered candidate geometry — high confidence as a transient regression.** It was introduced and then reverted; no claim is made that it explains all historical failures.
5. **Stored profile was unavailable or ranking-only — high confidence.** Historical live calls passed `outer_profile=None` when no benchmark setting existed; the current fallback ranks but cannot reject or generate candidates.
6. **Asynchronous tracking hides freshness — medium confidence.** It may leave stale candidates visible while a slow detection is pending, but it does not create the initial false quadrilaterals.
7. **Additional diagnostic metrics increased latency — high confidence for performance, not accuracy.** Current replay timings are higher than the snapshot, but the candidate geometry matched on the 14-image comparison.

## Recommended recovery strategy

No recovery was implemented during this audit. Before approving changes:

1. Freeze the preserved baseline and current reports.
2. Add a replay harness that compares baseline and candidate changes on the same positive and negative frames.
3. Separate candidate generation, ranking, and final acceptance metrics.
4. Restore a measured full-resolution baseline for a fixed camera format, then test processing resolution as an isolated experiment.
5. Use stored labels only through a validated, held-out ranking/acceptance experiment; do not treat them as a card classifier.
6. Require a human-reviewed acceptance gate before any live candidate is called a card.
7. Investigate outer-boundary generation separately using the existing pipeline diagnostics before changing thresholds.

Approval is required before implementing any recovery or detector change.
