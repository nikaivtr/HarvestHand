# Experimental Full-Card Detector and Tracker

This experiment is isolated from production recognition and preprocessing.
A verified candidate requires four-edge continuity, near-card geometry, inside/outside contrast, and non-clipped coordinates.

## Static benchmark

- Eligible manual complete cards: **29**
- Verified detections: **0**
- Correct full-card detections: **0**
- Incorrect/internal detections: **0**
- Missed/uncertain: **29**
- Mean verified corner error: **None%**
- 95th-percentile verified corner error: **None%**
- Mean detection time: **141.93 ms**
- 95th-percentile detection time: **367.49 ms**

## Mandatory static acceptance

| Criterion | Required | Result |
|---|---:|---:|
| Correct full-card detections | >= 26/29 | FAIL |
| Internal-region false locks | 0 | PASS |
| Missed detections | <= 3/29 | FAIL |
| Mean corner error | <= 2% | FAIL |
| 95th-percentile error | <= 4% | FAIL |

## Per-image results

| Image | Status | Candidates | Verified | Correct | Mean error % | IoU | Time ms |
|---|---|---:|---:|---:|---:|---:|---:|
| 0a01f9f6-fb25-4cb2-b253-89ad882e4ea4.jpg | uncertain | 5 | False | False | 0.00 | 0.000 | 262.69 |
| 4ef036f9-3397-4241-b010-638cfaa9104d.jpg | uncertain | 1 | False | False | 0.00 | 0.000 | 57.11 |
| 6ba8cceb-393b-4b90-a19e-cf09c8dc5d80.jpg | uncertain | 5 | False | False | 0.00 | 0.000 | 306.49 |
| 85bceec5-2c5e-48ef-a279-8f85e12d0064.jpg | uncertain | 2 | False | False | 0.00 | 0.000 | 107.52 |
| 91258ac8-8731-4955-9712-9608ea857726.jpg | uncertain | 2 | False | False | 0.00 | 0.000 | 126.01 |
| IMG_20261110_141914.jpg | uncertain | 2 | False | False | 0.00 | 0.000 | 77.27 |
| IMG_20261110_141941.jpg | uncertain | 3 | False | False | 0.00 | 0.000 | 71.84 |
| IMG_20261110_141953.jpg | uncertain | 0 | False | False | 0.00 | 0.000 | 13.36 |
| IMG_20261110_142003.jpg | uncertain | 1 | False | False | 0.00 | 0.000 | 28.25 |
| IMG_20261110_142009.jpg | uncertain | 1 | False | False | 0.00 | 0.000 | 26.05 |
| IMG_20261110_142050.jpg | uncertain | 4 | False | False | 0.00 | 0.000 | 164.58 |
| a294b9af-0fd9-4d40-b804-e781fa0eec07.jpg | uncertain | 7 | False | False | 0.00 | 0.000 | 533.50 |
| a53bc616-2de1-4f66-a2e1-4fb06e43f639.jpg | uncertain | 3 | False | False | 0.00 | 0.000 | 125.59 |
| b8d7215a-a96a-423f-92ac-c55aada888d0.jpg | uncertain | 4 | False | False | 0.00 | 0.000 | 162.85 |
| c2e3bfdf-dc97-42ab-a366-5aa63562f3e2.jpg | uncertain | 2 | False | False | 0.00 | 0.000 | 173.11 |
| 2b5dd6d2-bb4e-4c9c-a0e5-996f783db777.jpg | uncertain | 2 | False | False | 0.00 | 0.000 | 150.78 |
| 4407a29c-5afb-4a31-af48-5a2f23237a71.jpg | uncertain | 4 | False | False | 0.00 | 0.000 | 408.16 |
| 668da6b6-cb26-495e-83ee-62a3b7b0fbc9.jpg | uncertain | 5 | False | False | 0.00 | 0.000 | 218.28 |
| 82964558-1618-4853-829e-f1f97fcbbd7e.jpg | uncertain | 1 | False | False | 0.00 | 0.000 | 76.29 |
| 9695bc39-6647-4437-93d5-2bcc31b5b5b3.jpg | uncertain | 1 | False | False | 0.00 | 0.000 | 155.49 |
| IMG_20261110_135321.jpg | uncertain | 1 | False | False | 0.00 | 0.000 | 51.22 |
| IMG_20261110_135330.jpg | uncertain | 4 | False | False | 0.00 | 0.000 | 256.84 |
| IMG_20261110_135346.jpg | uncertain | 2 | False | False | 0.00 | 0.000 | 65.56 |
| IMG_20261110_135400.jpg | uncertain | 4 | False | False | 0.00 | 0.000 | 148.77 |
| IMG_20261110_135414.jpg | uncertain | 5 | False | False | 0.00 | 0.000 | 168.62 |
| IMG_20261110_135435.jpg | uncertain | 0 | False | False | 0.00 | 0.000 | 15.57 |
| IMG_20261110_135729.jpg | uncertain | 0 | False | False | 0.00 | 0.000 | 13.69 |
| f32364fe-aff9-421e-9569-e97e42a976aa.jpg | uncertain | 2 | False | False | 0.00 | 0.000 | 138.04 |
| f7acde1c-d3e9-4179-a169-00765e68e5c4.jpg | uncertain | 0 | False | False | 0.00 | 0.000 | 12.40 |

## Live validation status

Physical camera acquisition, 300-frame jitter, slow-motion tracking, obstruction, and 5-minute memory tests were not run by this automated benchmark. They remain required before any integration decision.

See `validation_results/full_card_validation.csv`, `validation_results/full_card_summary.json`, and `validation_results/comparison_overlays/`.
