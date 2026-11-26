# HarvestHand Recognition Lab

This is an isolated, experimental desktop application. It does not modify or
import results into the production game.

## Launch

From `D:\HarvestHand` with the existing virtual environment:

```powershell
.\.venv\Scripts\python.exe -m recognition_lab.lab_main
```

Original artwork and complete card photographs can be copied or imported from
the **Materials & Database** screen. Imported files are copied into
`recognition_lab\materials\uploads\`; source files are never changed.

## Workflow

1. Import reference images and observations.
2. Select a phase from the left navigation.
3. Use a camera if available, or use the offline image-import path.
4. Review the boundary/matching/OCR output.
5. Explicitly save **correct**, **incorrect**, or **uncertain** verification.
6. Export phase reports from **Reports & Evaluation**.

The local database is `recognition_lab\recognition_lab.sqlite3`. Reports are
written to `recognition_lab\reports\` as JSON and CSV. OCR intentionally reports
that a backend is unavailable until an OCR package is configured; it never
pretends that an empty result is a recognized card name.

## Phase 1 candidate verification

Phase 1 has two modes. **Review Mode** shows one frozen candidate at a time
from a background review queue. It requires a CORRECT, INCORRECT, or UNSURE
decision before NEXT CANDIDATE becomes active; PREVIOUS can revisit earlier
records. **Diagnostic Mode** shows multiple active candidates simultaneously
with IDs, statuses, metrics, and perspective-corrected inspection previews.
Solid lines are live detections, thin lines are tracked between detector runs,
and dotted lines are temporarily missing candidates within the configured
grace period. Switching modes does not reset the session or queue.

The detector rejects malformed, crossed, non-convex, collapsed, excessively
narrow, and poorly supported quadrilaterals before they enter the queue.
Each accepted candidate keeps its ID and frozen review geometry.

Saved CORRECT and INCORRECT annotations are loaded as an experimental outer-card
reference profile after the Stage A/B benchmark has been run. Candidate ranking
uses this profile as a comparative feature only; it does not replace manual
review. Nested candidates fully contained by a
larger plausible quadrilateral are retained in Diagnostic Mode but marked
`INTERNAL`; Review Mode does not allow them to be labeled CORRECT. This prevents
illustration and description panels from becoming positive outer-card examples
while keeping them available for investigation.

Use the review controls to save a manual judgment. The saved record includes
the original frame, four corners, perspective-corrected crop, detector
metrics, tracking status, session ID, and timestamp. **Clear queue** requires
confirmation and does not delete saved annotations. The **Boundary Analysis**
page compares correct and incorrect feature means and shows an experimental
nearest-centroid held-out baseline only after enough human-labeled samples
exist. **Benchmark outer boundary** compares generated polygons with saved
CORRECT corners using polygon IoU and normalized corner error. It reports Stage
A generation recall separately from Stage B top-ranked accuracy, no-boundary
cases, candidate rank, and an evaluation holdout by complete session. The
holdout is unavailable when only one session exists; it is never fabricated by
splitting near-identical rows. It also reports how often saved INCORRECT
polygons are reproduced and an outer-reference-support false-acceptance
estimate for those negative records. These measurements describe the current
experimental detector and are not claims of generalization without independent
camera conditions.
It never hides candidates or changes the detector automatically.

Candidate annotations can be exported from Phase 1 as
`phase1_candidate_annotations.json` and `phase1_candidate_metrics.csv`.

Use **Run dataset audit** on Boundary Analysis to evaluate the existing reviewed
dataset without changing it. The audit checks image decoding, four-corner
geometry, original-frame bounds, exact/near duplicates, outer-boundary
generation at IoU 0.50 and 0.75, internal-border failures, ranking versus
generation failures, and localization error. Candidate polygons contained
inside the annotated outer card are not counted as successful outer-boundary
matches. Results are written to
`recognition_lab\reports\phase1_ground_truth_audit.json`. Samples with
questionable geometry are flagged for review only. Logistic Regression and
Random Forest results are reported as unavailable when their dependency is not
installed; no experimental model is trained or deployed automatically.

## Boundary Reference Capture

Open **Boundary Reference Capture** from the navigation. Choose **Flat on
Table**, **Tilted Right**, **Tilted Left**, or **Held by Hand**, then open the
camera or import an image. Capture the current frame, click the physical outer
corners in TL/TR/BR/BL order, and drag markers to correct them before using
**Save reference** and **Confirm save**. Choose **Partially obstructed** for
handheld cards with a hidden edge; the status is stored as metadata.

Original frames and JSON annotations are stored in
`recognition_lab/datasets/boundary_references/<condition>/`. Rectified crops
are derived artifacts only. The collection is separate from Phase 1 candidate
annotations and never changes detector output or existing judgments.

The Phase 1 Evaluation page compares the preserved baseline against an
experimental explainable perimeter/nesting score. The baseline has no implicit
final card-acceptance gate, so its incorrect-sample rate is reported as queued
candidate behavior. The experimental comparison uses an explicit
diagnostic-only rule (`experimental_outer_score >= 0.35` and not a likely
internal region); it is not production behavior.
The comparison also records every incorrect-sample outcome, per-frame
candidate count, and detector processing time, plus separate outcomes for
records 207, 191, 178, and 156. A lower false-acceptance rate is not treated
as an improvement if positive outer-boundary recall regresses.

## Supported materials

JPG, JPEG, PNG, WEBP, BMP, TIFF, and similar OpenCV-readable images are
accepted. Use phase-specific folders and card names in the material metadata
when building a verified dataset. Camera availability and physical recognition
accuracy still require user testing with real cards and lighting conditions.
On Windows, the centralized camera service prefers Media Foundation and falls
back to DirectShow in Auto mode. The default request is 1920x1080 at 30 FPS
with MJPG. Capture runs on a dedicated latest-frame thread, so stale frames
are discarded rather than queued behind the GUI. The **Camera Diagnostics**
page reports the actual resolution, measured FPS, frame failures, read latency,
backend, initialization errors, and diagnostic-only brightness, contrast, and
Laplacian sharpness samples. If five consecutive frame reads fail, the lab
stops the camera and reports an actionable message instead of retaining a
stalled capture.

## Recognition Testing

The **Recognition Testing** page runs a read-only, closed-set matching test
against the stored Phase 2 materials. Pechay and Monggo are identified from
their verified image filenames when database card names are absent. The test
applies mild deterministic perspective and brightness changes, then uses the
existing `compare_images` matcher to rank all stored references. Results are
written to `reports/recognition_test_pechay_monggo.json`.

The same page also supports interactive camera verification: click
**Start live test**, wait for the preview, click **Recognize frame**, and mark the prediction **CORRECT** or
**INCORRECT**. Each verified frame is preserved under
`exports/recognition_tests/` and recorded in the lab observations database.
Recognition first tries the existing boundary detector and perspective crop;
when no candidate is available it reports that a center-crop fallback was
used.
Live results are restricted to Pechay and Monggo. If another stored reference
ranks first, the same crop is cross-examined against only those two target
references before a prediction is displayed.
The current production `cardscan/card_model.json` is not present, so the
interactive result explicitly identifies the Recognition Lab reference
matcher being used rather than pretending a trained production model ran.

This is a smoke/stress test, not proof of unseen-camera recognition. An
independent set of captured Pechay, Monggo, and unrelated-card images is
required before measuring whether added data improved generalization or
open-set rejection.
