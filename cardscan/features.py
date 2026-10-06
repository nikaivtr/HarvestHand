# ============================================================
#  Card Features
#
#  Turns a captured frame (or a sample photo) into a compact
#  numeric fingerprint that the model can compare.
#
#  Deliberately dependency-free: this project has no numpy and
#  pygame.surfarray needs it, so everything here works on a
#  raw RGB byte buffer produced by pygame.image.tobytes().
#
#  The fingerprint is a coarse colour grid plus edge energy, and
#  it is built to survive the things that actually go wrong at
#  scan time: different lighting, the card being a bit further
#  from the lens, and small hand-held tilt. Those change
#  brightness and overall scale far more than they change which
#  card it is.
#
#  Pipeline:
#      surface -> centre crop -> flatten to GRID x GRID
#              -> per-cell mean colour
#              -> normalise for brightness
#              -> concatenate colour + edge rows
# ============================================================

import pygame


# ── Tuning ──────────────────────────────────────────────────
# The analysis resolution. 12x12 gives enough spatial detail to
# tell the card art apart without being so fine that a 2px hand
# tremor changes the result.
GRID = 12

# Fraction of the frame the card is expected to fill. A card
# held close to the lens covers a lot of the view, so we crop
# the middle rather than the whole frame.
CROP = 0.86

# Edge weighting. Edges are what survive bad lighting best, but
# pure edge matching would confuse two cards with the same
# outline, so they are mixed with colour rather than used alone.
EDGE_WEIGHT = 0.85

# Centre weighting. The card is meant to be held in the middle of
# the frame, so cells away from the centre are pulled down. Without
# this, a card that does not quite fill the frame is mostly
# background, and every card starts to look like every other one.
# 0.0 ignores the weighting, 1.0 makes it very strong.
CENTER_FALLOFF = 0.6

# Luminance weights (Rec. 601) used for the edge pass.
_LR, _LG, _LB = 0.299, 0.587, 0.114


def prepare(surface):
    """Crop the centre of a frame and flatten it to a GRID x GRID RGB buffer.

    Returns (width, height, bytes) or None if the surface is unusable.
    """
    if surface is None or surface.get_width() < 2 or surface.get_height() < 2:
        return None

    w, h = surface.get_size()
    cw = max(2, int(w * CROP))
    ch = max(2, int(h * CROP))
    ox = (w - cw) // 2
    oy = (h - ch) // 2

    crop = surface.subsurface(pygame.Rect(ox, oy, cw, ch))
    small = pygame.transform.smoothscale(crop, (GRID, GRID))
    # No .convert() here on purpose: converting needs a display, and this
    # runs headless during training. tobytes() reads a plain surface fine.
    return GRID, GRID, pygame.image.tobytes(small, "RGB")


def _cell_mean(buf, w, x, y):
    """Mean RGB of one grid cell. Cell (0,0) is the top-left."""
    i = (y * w + x) * 3
    return buf[i], buf[i + 1], buf[i + 2]


def extract(surface):
    """Compute the feature vector for one frame or sample image.

    Returns a list of floats, or None if the image cannot be read.
    Length is stable: GRID*GRID colour values followed by
    GRID*GRID edge values.
    """
    prep = prepare(surface)
    if prep is None:
        return None
    w, h, buf = prep

    # ── Pass 1: per-cell mean colour, normalised for brightness ──
    # Dividing out each cell's own luminance means a dim room or a
    # bright lamp compresses the whole vector toward 1.0 instead of
    # shifting it, so matching stays stable across lighting.
    # `colour` is a flat RGB run (3 floats per cell), `lumas` is one
    # float per cell.
    colour = [0.0] * (w * h * 3)
    lumas  = [0.0] * (w * h)
    for y in range(h):
        for x in range(w):
            r, g, b = _cell_mean(buf, w, x, y)
            i  = y * w + x
            c  = i * 3
            lum = _LR * r + _LG * g + _LB * b
            # A near-black cell has no usable hue, so it is left
            # neutral instead of being divided up into noise.
            if lum > 18.0:
                colour[c]     = r / lum
                colour[c + 1] = g / lum
                colour[c + 2] = b / lum
            lumas[i] = lum / 255.0

    # ── Pass 2: gradient energy along rows and columns ──
    # A card is mostly flat colour with a bold icon in the middle;
    # the icon's edges are the part that identifies it. Sampling
    # only left/right and up/down neighbours (not diagonals) keeps
    # this cheap while still capturing the outline.
    edge = [0.0] * (w * h)
    for y in range(h):
        for x in range(w):
            i = y * w + x
            gx = 0.0
            gy = 0.0
            if x > 0 and x < w - 1:
                gx = lumas[i + 1] - lumas[i - 1]
            if y > 0 and y < h - 1:
                gy = lumas[i + w] - lumas[i - w]
            mag = (gx * gx + gy * gy) ** 0.5
            if mag > 1.0:
                mag = 1.0
            edge[i] = mag * EDGE_WEIGHT

    # ── Pass 3: pull weight toward the middle of the frame ──
    _apply_centre_weight(w, h, colour, edge)

    return colour + edge


def _apply_centre_weight(w, h, colour, edge):
    """Scale every cell down by how far it sits from the centre.

    The card is held in the middle of the view, so the corners are
    expected to be whatever was behind it. Down-weighting them stops
    a half-empty background from drowning out the card's own colour,
    which is what made an unfilled frame match the wrong card.
    """
    if CENTER_FALLOFF <= 0.0:
        return
    cx = (w - 1) / 2.0
    cy = (h - 1) / 2.0
    # Longest half-axis, so the corners reach exactly 1.0.
    norm = max(cx, cy) or 1.0
    for y in range(h):
        dy = (y - cy) / norm
        for x in range(w):
            dx = (x - cx) / norm
            d2 = dx * dx + dy * dy
            if d2 <= 0.0:
                continue
            k = 1.0 - CENTER_FALLOFF * (d2 if d2 < 1.0 else 1.0)
            c = (y * w + x) * 3
            colour[c]     *= k
            colour[c + 1] *= k
            colour[c + 2] *= k
            edge[y * w + x] *= k


def load_image(path):
    """Load a sample photo off disk, or None if it cannot be read.

    The image is returned unconverted: convert()/convert_alpha() both
    require an initialised display, and training has to work headless.
    """
    try:
        return pygame.image.load(path)
    except (pygame.error, FileNotFoundError, OSError):
        return None


def describe(vec):
    """Short human-readable summary, handy when tuning a card by hand."""
    if not vec:
        return "empty"
    half = len(vec) // 2
    bright = sum(vec[half:]) / half * 255.0
    return f"{len(vec)} dims, {len(vec) // 6} cells, mean edge {bright:.0f}/255"
