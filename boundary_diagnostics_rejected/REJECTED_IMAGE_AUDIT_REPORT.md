# Rejected Image Diagnostic Audit

## Dataset summary

The latest two-class training run saw 64 preprocessing rejections:

| Class | Total files | Usable | Rejected |
|---|---:|---:|---:|
| Pechay | 122 | 90 | 32 |
| Monggo | 132 | 100 | 32 |
| **Total** | **254** | **190** | **64** |

All 64 rejected files were reproduced by the current
`preprocess.prepare_detailed()` path. Every file decoded successfully as a
JPEG; there were no corrupted or unsupported files.

## Exact preprocessing conditions

The detector downsizes only for detection to a maximum dimension of 960,
converts RGB to blurred grayscale, and searches contours from:

1. Canny edges with morphological closing.
2. Binary light masks at thresholds 140 and 180 with morphological closing.

Candidates must be convex quadrilaterals and pass all of these checks:

- Area ratio at least 0.07.
- Aspect score at least 0.65 against the 5:7 card aspect.
- Opposite-side ratio at least 0.45.
- Corner angles between 45 and 135 degrees.
- Minimum edge support at least 0.02, except for candidates larger than 30%
  of the frame.

The observed failure messages were:

- `candidate too small`: 48 images.
- `no quadrilateral candidates`: 13 images.
- `card border edge support too weak`: 1 image.
- `candidate failed validation`: 2 images.

The message counts overlap in the sense that the latter two are candidate
validation outcomes; the per-image CSV is authoritative.

## Rejection categories

| Rejection category | Pechay | Monggo | Total | Typical recoverability |
|---|---:|---:|---:|---|
| Boundary Detection Failure | 25 | 29 | 54 | Recoverable |
| Poor Lighting / Shadows | 7 | 0 | 7 | Conditional |
| Perspective Distortion | 0 | 3 | 3 | Conditional |
| Blurred / Out of Focus | 0 | 0 | 0 | — |
| Partial / Obstructed Card | 0 | 0 | 0 | — |
| Low Resolution | 0 | 0 | 0 | — |
| Corrupted / Unsupported | 0 | 0 | 0 | — |
| Other / Uncertain | 0 | 0 | 0 | — |

The dominant issue is therefore the detector's inability to find or accept
the card quadrilateral, not file quality. Many cards are visible and appear
complete, but occupy a small fraction of the frame or have weak/fragmented
edges. Their full image dimensions are high; they are not intrinsically
low-resolution files.

## Recoverability

- **Recoverable:** 54 images. The card is
  visibly present and the current contour/candidate logic is the limiting
  factor. Candidate generation, multi-scale detection, or a separately
  validated detector could recover some of these.
- **Conditionally recoverable:** 10
  images. Better lighting or less severe camera geometry may help, but any
  recovered crop must still pass independent visual boundary review.
- **Unrecoverable:** 0 established by this audit.
- **Needs manual review:** 0.

No automatic correction was applied and no original image was modified.

## Recommendations

1. Improve candidate generation and ranking rather than lowering the
   `MIN_CARD_AREA_RATIO` or confidence thresholds blindly.
2. Add an independent content/boundary validation stage so a larger
   quadrilateral cannot silently select background.
3. Use multi-scale or card-size-aware detection for the small-card images.
4. Capture future samples with the card occupying more of the frame and with
   diffuse lighting.
5. Keep the 64 rejected images available for future detector experiments;
   do not add them to a production model until their crops are verified.

Improving localization could plausibly recover a meaningful subset because
most rejected photos contain a visible card. However, the prior v12 audit
showed that accepting geometrically plausible background regions is worse than
rejecting an uncertain crop, so recovery must be conservative.

## Contact sheets

- [All rejected images](rejected_images_contact_sheet.jpg)
- [Pechay rejected images](pechay_plant_rejected_contact_sheet.jpg)
- [Monggo rejected images](monggo_plant_rejected_contact_sheet.jpg)
- [Boundary failures](category_boundary_contact_sheet.jpg)
- [Lighting cases](category_lighting_contact_sheet.jpg)
- [Perspective cases](category_perspective_contact_sheet.jpg)
- [Per-image measurements and classifications](rejected_images_audit.csv)

## Individual classifications

| Filename | Class | Primary category | Recoverability | Preprocessing reason |
|---|---|---|---|---|
| 15b3c45c-229f-4bc2-8b11-a741f583d591.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 1ea480c8-e7c9-4298-8545-424246d671c2.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 2b5dd6d2-bb4e-4c9c-a0e5-996f783db777.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 2bacde34-d63f-4885-afa2-c63a54219b31.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 4407a29c-5afb-4a31-af48-5a2f23237a71.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 5339ff0a-02d3-4b5a-adb2-3b3eb45244f0.jpg | pechay_plant | Poor Lighting / Shadows | conditional | no quadrilateral candidates |
| 5b127e8d-7055-492f-8202-3c2a043df58d.jpg | pechay_plant | Poor Lighting / Shadows | conditional | no quadrilateral candidates |
| 5db9eba2-e62f-4e28-8b6e-a716d09e2149.jpg | pechay_plant | Poor Lighting / Shadows | conditional | no quadrilateral candidates |
| 668da6b6-cb26-495e-83ee-62a3b7b0fbc9.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 78330d81-82fc-437c-9eb5-3fec7da718b2.jpg | pechay_plant | Poor Lighting / Shadows | conditional | no quadrilateral candidates |
| 8291ce14-2bad-4ba3-9e2f-46e957709221.jpg | pechay_plant | Poor Lighting / Shadows | conditional | no quadrilateral candidates |
| 82964558-1618-4853-829e-f1f97fcbbd7e.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 93d262c8-f97f-4e23-ab3a-4e7002d75214.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 9695bc39-6647-4437-93d5-2bcc31b5b5b3.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 9d2195a4-fc90-4f13-9e8b-3de6d7e4f8d3.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| ba5f5898-1431-47c4-9fa4-4ecec1aa78de.jpg | pechay_plant | Poor Lighting / Shadows | conditional | no quadrilateral candidates |
| c4870fcb-1799-4d5c-b203-1d5b29e76dc0.jpg | pechay_plant | Poor Lighting / Shadows | conditional | no quadrilateral candidates |
| ced8a0e8-2fcc-4c5f-a979-0a98b0854b1e.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| cf18fef3-92cf-4437-b327-aaeb0915b4e8.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| cfe8a3cf-6665-4e61-a904-36dc93010a6e.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| d76a6f8c-f69f-4695-b876-7a1d51e427ab.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| db66a971-017b-414a-90d0-fc582e1d3be2.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| dcbb71ba-b01f-40d1-ab7a-e3b50e24a4d6.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| f32364fe-aff9-421e-9569-e97e42a976aa.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| f7acde1c-d3e9-4179-a169-00765e68e5c4.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_135321.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_135330.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_135346.jpg | pechay_plant | Boundary Detection Failure | recoverable | no quadrilateral candidates |
| IMG_20261110_135400.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_135414.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_135435.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_135729.jpg | pechay_plant | Boundary Detection Failure | recoverable | candidate too small |
| 06f34cc6-cfcf-4805-a210-9679a4cb591c - Copy.jpg | monggo_plant | Boundary Detection Failure | recoverable | no quadrilateral candidates |
| 06f34cc6-cfcf-4805-a210-9679a4cb591c.jpg | monggo_plant | Boundary Detection Failure | recoverable | no quadrilateral candidates |
| 0a01f9f6-fb25-4cb2-b253-89ad882e4ea4.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 299f151c-890e-4e80-b5ef-276cc8c1f737.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 325fe2ba-fe12-480b-9c91-4c037b5633ef.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 4e5e32c9-3d5b-498f-a498-0bcd5780a17d.jpg | monggo_plant | Boundary Detection Failure | recoverable | card border edge support too weak |
| 4ef036f9-3397-4241-b010-638cfaa9104d.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 4fa5ceb0-9108-4084-a1e4-0136026cce13 - Copy.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 4fa5ceb0-9108-4084-a1e4-0136026cce13.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 59db5bd6-f83e-4ed0-921f-e815160f210d.jpg | monggo_plant | Boundary Detection Failure | recoverable | no quadrilateral candidates |
| 5ac988f1-a307-4906-b2f9-d9e54f1aa139.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 65f44f31-81b6-44be-8bde-c65af98d4e63.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 6ba8cceb-393b-4b90-a19e-cf09c8dc5d80.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 85bceec5-2c5e-48ef-a279-8f85e12d0064.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 91258ac8-8731-4955-9712-9608ea857726.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| 9d342fee-0b8c-4af7-8c2c-2a4e795431b1.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| a294b9af-0fd9-4d40-b804-e781fa0eec07.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| a53bc616-2de1-4f66-a2e1-4fb06e43f639.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| ab95f40d-bddd-4e22-a49a-069b303a2fd3.jpg | monggo_plant | Boundary Detection Failure | recoverable | no quadrilateral candidates |
| b8d7215a-a96a-423f-92ac-c55aada888d0.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| c2e3bfdf-dc97-42ab-a366-5aa63562f3e2.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| ea1dcf87-454d-4074-aeaf-6aa4dcb720ad.jpg | monggo_plant | Boundary Detection Failure | recoverable | no quadrilateral candidates |
| IMG_20261110_141840.jpg | monggo_plant | Perspective Distortion | conditional | candidate too small |
| IMG_20261110_141906.jpg | monggo_plant | Perspective Distortion | conditional | candidate failed validation |
| IMG_20261110_141914.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_141941.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_141953.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_141958.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_142003.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_142009.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |
| IMG_20261110_142045.jpg | monggo_plant | Perspective Distortion | conditional | candidate failed validation |
| IMG_20261110_142050.jpg | monggo_plant | Boundary Detection Failure | recoverable | candidate too small |

## Limitations

The visual categories were assigned from the generated contact sheets and
current detector measurements. A rejection reason such as `candidate too
small` does not prove that the card is unusable; it identifies the current
algorithm's selected candidate. Blur and obstruction were not assigned unless
they were visually evident. No independent corner ground truth was available,
and no alternative preprocessing algorithm was used in this audit.
