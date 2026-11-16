# Deep Boundary-Failure Audit

This is an isolated analysis of the 54 images manually categorized as
boundary failures. Production preprocessing and feature extraction were
not changed.

## Important measurement limitation

The original detector does not retain failed corner coordinates. This
audit uses a more permissive contour search to obtain the best available
quadrilateral proxy. These are not independent ground-truth corners and
the corrected crops are not manual annotations. They estimate the upper
bound of what a corrected crop might achieve. The overlay contact sheet
must be reviewed before treating any candidate as a true card boundary.

## Aggregate results

- Boundary-category images: **54**
- Images with a proxy quadrilateral: **54/54** (100.0%)
- Proxy crops passing unchanged `features.extract()`: **12/54** (22.2%)
- Strong corner-identifiability proxy: **8/54** (14.8%)

## Proxy geometry measurements

- Mean proxy card area ratio: **0.442**
- Mean proxy card width ratio: **0.614**
- Mean proxy card height ratio: **0.556**
- Mean absolute proxy rotation: **5.7°**
- Mean proxy opposite-side ratio: **0.846**
- Mean proxy edge contrast: **22.9 grayscale levels**

The rotation, perspective, contrast, and corner values are available
per image in the CSV. Rotation is the top-edge angle after consistent
corner ordering; opposite-side ratio is a perspective/shape proxy.

## Extractor test

Each proxy quadrilateral was warped into a card-shaped crop with a 5%
border and passed to the unchanged `cardscan.features.extract()`.
A pass means the existing preprocessing detector found a boundary in
that corrected crop and returned the normal feature vector. It does not
prove that the proxy boundary was the true card boundary.

## Files

- [Per-image CSV](boundary_failures_deep_audit.csv)
- [Overlay contact sheet](boundary_failures_deep_contact_sheet.jpg)
- Corrected crop directory: `boundary_failure_corrected_crops/`
- Overlay directory: `boundary_failure_overlays/`

## Decision guidance

Use the overlay sheet to separate true-card proxies from background
rectangles. If a substantial number of true-card proxies pass the
extractor, the highest-value next experiment is conservative multi-scale
candidate generation plus independent content validation. Do not lower
the production area or recognition thresholds based on this proxy audit.
