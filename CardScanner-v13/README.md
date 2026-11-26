# CardScanner v13

Self-contained Card Scanner bundle with training, live camera recognition,
boundary diagnostics, and a pre-trained mean-centered experimental model.

## Run

Train or retrain:

```powershell
& .\.venv\Scripts\python.exe tools/train_cards.py --report --out card_model_card_plants_mean_centered_v13_experimental.json
```

Check stored photos:

```powershell
& .\.venv\Scripts\python.exe tools/check_cards.py --samples data/card_samples --out debug/cards
```

Run Recognition Lab:

```powershell
& .\.venv\Scripts\python.exe -m recognition_lab.lab_main
```

Run the scanner demo:

```powershell
& .\.venv\Scripts\python.exe live_test.py
```

## Included

- `cardscan/`: v13 detector, preprocessing, features, model, camera, tracker, scanner
- `tools/`: training and sample diagnostics
- `data/card_samples/`: card photo datasets
- `recognition_lab/`: live recognition and diagnostics interface
- `card_model_card_plants_mean_centered_v13_experimental.json`: trained experimental model
- `live_test.py`: live recognition diagnostic with scores
