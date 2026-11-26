"""Launch the separate HarvestHand live card-learning tester."""

import os
import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
os.environ["SDL_VIDEODRIVER"] = "windows"
os.environ["HARVESTHAND_CARD_MODEL"] = str(
    ROOT / "card_model_card_plants_mean_centered_v13_experimental.json"
)
sys.path.insert(0, str(ROOT))
runpy.run_path(
    str(ROOT / "tools" / "mini_live_card_tester.py"),
    run_name="__main__",
)
