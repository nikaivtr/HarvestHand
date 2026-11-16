# Physical ArUco Test Instructions

## Print and prepare

1. Open `aruco_physical_test_sheet.pdf`.
2. Print the first page at **100% / actual size**.
3. Disable “Fit to page”, “Scale to fit”, and automatic printer scaling.
4. After printing, measure the 50 mm reference line. Reprint if it is not
   50 mm.
5. Confirm the card outline measures 63.0 mm by 88.2 mm.
6. Cut out the card along the outline, or mount the sheet flat for initial
   tests. Do not cover any marker or its white quiet zone.
7. Check that the four black marker squares are 10.0 mm and that IDs read
   0, 1, 2, and 3. The second PDF page is a marker reference.

## Photographing

Use a normal smartphone or webcam. The Python project does not need to be
connected to the camera; save ordinary JPG or PNG photographs first.

Create folders under `physical_photos` named for the condition, for example:

```text
physical_photos/
  straight_on/
  slight_rotation/
  strong_perspective/
  near_camera/
  far_camera/
  bright_lighting/
  dim_lighting/
  uneven_lighting/
  glare/
  shadow/
  partial_marker/
```

Save each image in the matching folder with a descriptive filename such as
`straight_on_001.jpg`. The folder name becomes the reported test condition.
Images placed directly in `physical_photos` are reported as `unlabeled`, or
can use `--condition`.

Capture at least:

- Straight-on, centered, evenly lit.
- Slight clockwise and counter-clockwise rotation.
- Strong perspective from above and from the side.
- Near and far distances while keeping the card visible.
- Bright, dim, and uneven lighting.
- Glare from a lamp or window and a distinct cast shadow.
- Partial obstruction of one marker, then two markers.
- Busy backgrounds and a hand holding the card.

Keep the whole card in frame when testing perspective. Do not edit, crop, or
retouch the photographs. Preserve the original files.

## Run the isolated test

From the repository root:

```powershell
& .venv\Scripts\python.exe boundary_diagnostics_aruco\physical_aruco_test.py `
  --input-dir boundary_diagnostics_aruco\physical_photos
```

To label photographs all at once:

```powershell
& .venv\Scripts\python.exe boundary_diagnostics_aruco\physical_aruco_test.py `
  --input-dir boundary_diagnostics_aruco\physical_photos `
  --condition straight_on
```

The script writes `physical_test_results.csv`,
`physical_test_contact_sheet.jpg`, `PHYSICAL_TEST_REPORT.md`, and per-image
visualizations/crops under `physical_results/`.

## Optional independent ground truth

For geometric accuracy, create `ground_truth.json` beside the input
photographs. It must contain image-space outer card corners in this order:
top-left, top-right, bottom-right, bottom-left:

```json
{
  "straight_on_001.jpg": [[120, 80], [820, 90], [810, 1100], [130, 1090]]
}
```

These coordinates must be measured independently from the photograph, not
copied from the detector output. Without this file, the report explicitly
leaves corner accuracy unmeasured.

## Manual checklist

- [ ] Printed card is 63.0 x 88.2 mm.
- [ ] Each black marker is 10.0 mm.
- [ ] All four marker IDs are correct.
- [ ] Quiet zones are white and unobstructed.
- [ ] No marker is clipped by the page or card edge.
- [ ] The 50 mm reference line measures 50 mm.
- [ ] No unwanted print scaling was applied.
