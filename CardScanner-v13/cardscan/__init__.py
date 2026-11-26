# ============================================================
#  cardscan - physical card recognition
#
#  Prepared for the Raspberry Pi build. Nothing in the game calls
#  this yet; it is a self-contained, testable unit.
#
#  Typical use, once wiring it into gameplay:
#
#      from cardscan import CardScanner
#      scan = CardScanner()
#      scan.open_camera(device=0)
#      scan.start("AC-01 Water Card")
#      ...each frame:  result = scan.update(dt)
#
#  Teaching it the cards (on any machine, no camera needed):
#
#      python tools/train_cards.py
#
#  See data/card_samples/README.md for how to collect samples.
# ============================================================

from cardscan.registry import (
    Card,
    CARDS,
    all_cards,
    get,
    slugs,
    resolve,
)
from cardscan.features import extract, load_image
from cardscan.model import (
    build_model,
    save_model,
    load_model,
    is_trained,
    classify,
    match,
)
from cardscan.camera import (
    CameraError,
    open_camera,
    OpenCVCamera,
    FolderCamera,
    NullCamera,
)
from cardscan.scanner import CardScanner, ScanResult


__all__ = [
    "Card", "CARDS", "all_cards", "get", "slugs", "resolve",
    "extract", "load_image",
    "build_model", "save_model", "load_model", "is_trained",
    "classify", "match",
    "CameraError", "open_camera", "OpenCVCamera", "FolderCamera",
    "NullCamera",
    "CardScanner", "ScanResult",
]
