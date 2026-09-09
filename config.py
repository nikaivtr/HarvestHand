"""
Project-wide constants.

Anything that depends on the actual screen size (WIDTH/HEIGHT) stays inside
each scene's own init() — this file is only for values that never change.
"""

# ── Assets ──────────────────────────────────────────────────────────────────
IMG_DIR = "img/"   # all image paths passed to utils.load_img/load_bg are relative to this

# ── Button canvas ────────────────────────────────────────────────────────────
# All button PNGs share this canvas size, so scaling by width alone keeps
# every button's aspect ratio correct.
BTN_CANVAS_W = 2736
BTN_CANVAS_H = 1567
BTN_ASPECT   = BTN_CANVAS_W / BTN_CANVAS_H   # ≈ 1.746

# ── Press-shrink button feedback ────────────────────────────────────────────
PRESS_DURATION = 0.12
PRESS_SCALE    = 0.88

# ── Level select placeholders ───────────────────────────────────────────────
# TODO: remove once real level-card art replaces the colored rectangles
LEVEL_PLACEHOLDER_COLORS = [(120, 170, 90), (90, 140, 170), (170, 120, 90)]
LEVEL_PLACEHOLDER_BORDER = (255, 255, 255)

# ── Story mode ───────────────────────────────────────────────────────────────
# TODO: remove once a real background image is in place
STORY_BG_COLOR = (30, 30, 40)
