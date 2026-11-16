# Physical ArUco Test Report

## Configuration

- Dictionary: `DICT_4X4_50`
- Expected IDs: `(0, 1, 2, 3)`
- Card layout: 63.0 x 88.2 mm
- Marker: 10.0 mm, with 2.0 mm quiet zone
- Marker inset: 6.0 mm to black square
- Output crop: 120 x 168 pixels
- Input directory: `D:\HarvestHand\boundary_diagnostics_aruco\physical_photos`

## Results

No photographs supplied; real-world testing is pending.
- Independent ground-truth corner measurements: none

Four detected markers are not by themselves proof of correct localization.
The script also checks exact IDs, estimates the boundary from the calibrated
physical layout, validates the quadrilateral, and records corrected crops.

## Accuracy

Corner error is reported only when independent coordinates are supplied in
`ground_truth.json`. Detector-generated coordinates must not be used as
ground truth. If no such file is present, geometric accuracy remains
unmeasured.

## Review

Inspect the per-image visualizations, corrected cards, and
`physical_test_results.csv`. Review glare, blur, shadows, marker wear,
partial occlusion, false detections, and whether the four markers really
belong to the same physical card.
