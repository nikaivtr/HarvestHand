"""
Asset configuration for the Ingredient Jigsaw Challenge mini-game.

Defines ingredient metadata, sprite-sheet crop rectangles, level configurations,
scoring, placement tolerances, layout fractions, colours, and font settings.
"""

SPRITE_SHEET = "minigames/ingredient_puzzle/PuzzleGame.jpg"
BACKGROUND = "minigames/ingredient_puzzle/KitchenBGGame.jpg"
SPRITE_SHEET_COLS = 3
SPRITE_SHEET_ROWS = 3

INGREDIENT_GRID_ORDER = [
    ("kamatis",     None,                       "Kamatis (Tomato)"),
    ("okra",        None,                       "Okra"),
    ("gabi",        None,                       "Gabi (Taro)"),
    ("sibuyas",     None,                       "Sibuyas (Onion)"),
    ("labanos",     None,                       "Labanos (Radish)"),
    ("baboy",       None,                       "Baboy (Pork)"),
    ("kangkong",    None,                       "Kangkong (Water Spinach)"),
    ("pechay",      None,                       "Pechay (Chinese Cabbage)"),
    ("siling",      None,                       "Siling Pansigang (Chili Pepper)"),
]

LEVELS = {
    1: {
        "name": "Level 1 — Beginner",
        "ingredients": ["kamatis", "okra", "gabi"],
        "pieces_per_ingredient": 4,
        "timer_seconds": 90,
        "rotation": False,
        "reference_prominence": 1.0,
    },
    2: {
        "name": "Level 2 — Intermediate",
        "ingredients": ["sibuyas", "labanos", "baboy"],
        "pieces_per_ingredient": 6,
        "timer_seconds": 120,
        "rotation": True,
        "reference_prominence": 0.7,
    },
    3: {
        "name": "Level 3 — Advanced",
        "ingredients": ["kangkong", "pechay", "siling"],
        "pieces_per_ingredient": 8,
        "timer_seconds": 150,
        "rotation": True,
        "reference_prominence": 0.5,
    },
}

POINTS_PER_INGREDIENT = 100
POINTS_LEVEL_BONUS = 250
POINTS_TIME_BONUS_PER_SECOND = 1

POS_TOLERANCE_FRAC = 0.08
ANGLE_TOLERANCE_DEG = 25

UI = {
    "sidebar_w": 0.215,
    "timer_font_frac": 0.045,
    "title_font_frac": 0.042,
    "label_font_frac": 0.024,
}

PALETTE = {
    "ink": (66, 43, 25),
    "cream": (255, 246, 220),
    "green": (65, 138, 66),
    "deep_green": (35, 94, 53),
    "gold": (248, 188, 64),
    "red": (193, 76, 55),
    "shadow": (43, 36, 23, 110),
    "panel_border": (177, 128, 59),
    "piece_border": (255, 255, 255),
    "piece_shadow": (43, 36, 23, 90),
    "guide_fill": (100, 145, 76, 90),
    "guide_border": (72, 110, 58),
    "silhouette_fill": (78, 120, 62, 35),
    "silhouette_border": (65, 105, 52, 155),
}

FONT_PATH = "fonts/RumRaisin-Regular.ttf"
FONT_FALLBACK = "Georgia"


def ingredient_key(index: int) -> str:
    return INGREDIENT_GRID_ORDER[index][0]


def ingredient_label(index: int) -> str:
    return INGREDIENT_GRID_ORDER[index][2]


def crop_rect_for(
    index: int, sheet_width: int, sheet_height: int
) -> tuple[int, int, int, int]:
    col = index % SPRITE_SHEET_COLS
    row = index // SPRITE_SHEET_COLS
    left = col * sheet_width // SPRITE_SHEET_COLS
    top = row * sheet_height // SPRITE_SHEET_ROWS
    right = (col + 1) * sheet_width // SPRITE_SHEET_COLS
    bottom = (row + 1) * sheet_height // SPRITE_SHEET_ROWS
    return (left, top, right - left, bottom - top)
