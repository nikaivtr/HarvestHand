"""Launch the updated root Recognition Lab instead of the stale v13 copy."""

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault(
    "HARVESTHAND_CARD_MODEL",
    str(ROOT / "card_model_card_plants_mean_centered_v13_experimental.json"),
)

from recognition_lab.lab_main import main


if __name__ == "__main__":
    main()
