"""Launch Harvest Hand with the current experimental card model."""

import os
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "card_model_card_plants_mean_centered_v13_experimental.json"

if not MODEL.exists():
    raise FileNotFoundError(f"Experimental card model not found: {MODEL}")

os.environ["HARVESTHAND_CARD_MODEL"] = str(MODEL)
runpy.run_path(str(ROOT / "main.py"), run_name="__main__")
