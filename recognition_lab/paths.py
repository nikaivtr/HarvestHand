"""Paths owned by the Recognition Lab."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "recognition_lab.sqlite3"
MATERIALS = ROOT / "materials"
REFERENCES = ROOT / "references"
DATASETS = ROOT / "datasets"
MODELS = ROOT / "models"
REPORTS = ROOT / "reports"
EXPORTS = ROOT / "exports"
CONFIG = ROOT / "config"


def ensure_layout() -> None:
    for path in (MATERIALS, REFERENCES, DATASETS, MODELS, REPORTS, EXPORTS, CONFIG):
        for phase in ("phase1", "phase2", "phase3"):
            (path / phase).mkdir(parents=True, exist_ok=True)
    (MATERIALS / "uploads").mkdir(parents=True, exist_ok=True)
    (MATERIALS / "observations").mkdir(parents=True, exist_ok=True)
    for condition in ("flat_on_table", "tilted_right", "tilted_left", "held_by_hand"):
        (DATASETS / "boundary_references" / condition).mkdir(parents=True, exist_ok=True)
