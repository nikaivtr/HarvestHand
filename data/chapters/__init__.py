# This file lets Python treat the chapters folder as a package.
# It also lists all 10 chapters and provides a load() function.

from importlib import import_module

# The order here matches the level select screen (index 0 = Level 1, etc.)
CHAPTER_IDS = [
    "ch01_pechay",
    "ch02_monggo",
    "ch03_okra",
    "ch04_squash",
    "ch05_tomato",
    "ch06_eggplant",
    "ch07_kamote",
    "ch08_rice",
    "ch09_corn",
    "ch10_cassava",
]


def load(chapter_id: str) -> dict:
    """Load a chapter's data by its ID string (e.g. 'ch01_pechay')."""
    mod = import_module(f"data.chapters.{chapter_id}")
    return mod.CHAPTER
