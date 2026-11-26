# Boundary Reference Pipeline Diagnostic Summary

This is a read-only trace of the existing Recognition Lab detector. No detector settings, annotations, or production code were changed.

- Positive references traced: 8
- Representative incorrect samples traced: 12
- Contours extracted from positive references: 979
- Four-corner candidates accepted before final ranking: 1
- Four-corner candidates rejected by filters/geometry: 310

## Evidence

The best pre-filter quadrilateral IoU for each reference is recorded in `boundary_reference_pipeline_diagnostics.json`. Seven references had best pre-filter IoU below 0.50, indicating that no sufficiently matching four-corner contour was produced before final candidate selection. One reference produced an accepted quadrilateral, but it was an internal region rather than the manually annotated outer card.

Most common recorded rejection reasons on quadrilateral approximations:
- area outside limits: 620
- implausible card aspect: 374
- collapsed edge: 236
- insufficient edge support: 187
- invalid corner angle: 2
- excessive perspective: 1
- uneven perspective: 1

## Bottleneck

The dominant measured bottleneck is upstream of ranking: the current masks and contour approximation do not produce a matching complete outer-card quadrilateral for seven of eight references. The one generated candidate is internal, so ranking is not the primary failure for this collection.

The intermediate images and per-contour records are preserved under `boundary_reference_pipeline_diagnostics/` for visual inspection.
