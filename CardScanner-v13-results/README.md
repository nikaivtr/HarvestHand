# CardScanner v13 Results

This folder records measured training, stored-card replay, and live-camera
probe results for the integrated CardScan-Claude v13 pipeline.

## Final model

- Model: `CardScanner-v13/card_model_card_plants_mean_centered_v13_experimental.json`
- Classes: 8
- Readable samples: 1,907
- Feature/preprocessing version: 13
- Score threshold: 0.50
- Margin threshold: 0.20

## Leave-one-out stored-photo results

| Card | Readable | Top-1 | Confident |
|---|---:|---:|---:|
| Pechay | 269 | 89.2% | 58.0% |
| Monggo | 433 | 89.8% | 54.5% |
| Okra | 301 | 86.4% | 66.1% |
| Kalabasa | 301 | 92.4% | 67.8% |
| Kamatis | 151 | 82.1% | 46.4% |
| Talong | 151 | 91.4% | 82.1% |
| Kamote | 150 | 82.0% | 38.7% |
| Palay | 151 | 82.8% | 37.1% |

Overall leave-one-out:

- Top-1: 87.9%
- Confident: 57.8%
- Wrong confident matches: 0 / 1,907

This is stored-photo evaluation. It does not prove physical-camera recognition.

## Stored-card replay

The design PNG replay produced:

| Card | Result | Score | Margin |
|---|---|---:|---:|
| Pechay | Pechay | 0.951 | 0.457 |
| Monggo | Monggo | 0.886 | 0.390 |
| Okra | Okra | 0.974 | 0.442 |
| Kalabasa | Kalabasa | 0.987 | 0.440 |
| Kamatis | Kamatis | 0.973 | 0.325 |
| Talong | Talong | 0.829 | 0.414 |
| Kamote | Kamote | 0.762 | 0.211 |
| Palay | Palay | 0.983 | 0.402 |

## Live-camera probes

The live probe frames contain no-card scenes or physically held but partially
occluded Pechay captures. They did not produce a confident match.

Examples:

- Live no-card frame scores: 0.790, 0.729, 0.456, 0.699, 0.845, 0.713
- Physical Pechay frames were repeatedly selected as other cards or rejected
- The latest Pechay probes used scores below 0.83 and margins below 0.20
- The model did not produce a confident Pechay match in the available physical
  camera frames

## Folder contents

- `training/`: model and leave-one-out summaries
- `stored_replay/`: eight design-card PNG references
- `live_frames/`: no-card, physical-Pechay, ORB, and variant frames
- `reports/`: historical Recognition Lab and boundary investigation reports
