# ArUco Feasibility Report

## Compatibility

- OpenCV: `5.0.0`
- `cv2.aruco`: available
- Dictionary: `DICT_4X4_50`
- Marker IDs: `(0, 1, 2, 3)`; marker size: 70px; corner inset: 28px
- Output warp: 120 x 168 (5:7)

## Layout

The mockup places one marker near each corner, outside the central illustration and label areas. The outer card corners are inferred from the calibrated marker inset; missing or duplicate expected IDs fail closed rather than using a guessed boundary.

## Synthetic results

Tested 9 controlled scenes. Four-marker detection and perspective correction succeeded for 6/9 (66.7%). Successful warps: 6/9 (66.7%). Individual expected-marker detections were 34/36 (94.4%). All four expected IDs were present in 7/9 scenes; mean/max corner error among successful warps was 0.23/0.32px. These are synthetic newly photographed-card substitutes, not the existing dataset.

Expected failures were the partially obscured and missing-marker cases. The distractor case demonstrates that an unexpected marker ID must not be accepted as one of the card corners.

## Existing 42-image dataset

The intended four IDs were detected in 0/42 images. These photos do not contain the experimental markers, so this is not a localization validation of the current cards and cannot be compared directly with v12's 16/42 verified visual boundaries.

## Comparison with v12

| Metric | v12 visual detector | ArUco experiment |
|---|---:|---:|
| Complete card localization | 16/42 verified | 6/9 synthetic scenes |
| Incorrectly accepted boundaries | 9/42 | See per-scene CSV; 0/6 successful synthetic warps |
| False rejections | 8/42 | Missing/obscured markers fail closed |
| Perspective correction | Audit found invalid crops | 6/9 synthetic warps |

## Limitations and recommendation

ArUco is technically supported and promising for a redesigned card or printed marker prototype. This experiment does not establish performance on the existing cards, marker wear, print quality, glare, motion blur, or real gameplay occlusion. Markers would change card artwork and require new physical cards plus a new capture set. Classification: **Inconclusive**. The next step is a physical prototype with four markers, photographed under the same 42 capture conditions, followed by blinded boundary review. Do not integrate ArUco into the production scanner yet.
