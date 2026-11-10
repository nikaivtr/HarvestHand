# Card Features
#
# Turns a captured frame (or sample photo) into a compact numeric
# fingerprint that the model can compare.
#
# Pipeline:
#   surface -> preprocess.prepare (detect card, perspective-correct,
#            letterbox to a fixed 5:7 portrait canvas)
#           -> downscale to GRID x GRID
#           -> per-cell mean colour + edge energy
#           -> gentle centre / illustration-band weighting
#           -> concatenate colour + edge (fixed-length vector)
#
# Pure Python (no numpy) so it trains and runs headless on a Pi.
# The old 12x12 grid could not separate cards that share one
# template; the higher grid plus card isolation resolves the
# illustration, name and ID differences.
#

import pygame

import cardscan.preprocess as preprocess

# Analysis resolution. 24x24 gives enough spatial detail to tell
# same-template cards apart without being so fine that a 2px hand
# tremor changes the result. Each cell is 5x7 px on the 120x168
# normalized card.
GRID = 24

# Must match preprocess.PREPROCESS_VERSION so stale models are
# rejected.
PREPROCESS_VERSION = preprocess.PREPROCESS_VERSION

# Edge weighting. Edges survive bad lighting, but pure edge matching
# would confuse two cards with the same outline, so they are mixed
# with colour rather than used alone.
EDGE_WEIGHT = 0.85

# Centre weighting. The card is centred in the normalized canvas, so
# cells near the middle (illustration) are more informative than the
# corners (border / background padding). 0.0 disables.
CENTER_FALLOFF = 0.5

# Horizontal band that usually holds the crop illustration gets a
# small extra boost; name (top) and ID (bottom) bands keep their
# colour so the card ID is a supporting signal.
ILLUSTRATION_BAND = (0.30, 0.75)
ILLUSTRATION_BOOST = 0.25

_LR, _LG, _LB = 0.299, 0.587, 0.114


def prepare(surface):
    """Normalize a frame/sample to the standard card canvas.

    Delegates to cardscan.preprocess.prepare so training and live
    recognition use identical preprocessing. Returns a (CANVAS_W x
    CANVAS_H) pygame Surface, or None.
    """
    return preprocess.prepare(surface)


def load_image(path):
    """Load a sample photo off disk, or None if it cannot be read."""
    return preprocess.load_image(path)


def _cell_mean(buf, w, x, y):
    """Mean RGB of one grid cell. Cell (0,0) is the top-left."""
    i = (y * w + x) * 3
    return buf[i], buf[i + 1], buf[i + 2]


def _build_weight_map(w, h):
    """Per-cell weight: centre-weighted with an illustration-band boost."""
    cx = (w - 1) / 2.0
    cy = (h - 1) / 2.0
    norm = max(cx, cy) or 1.0
    top, bottom = ILLUSTRATION_BAND
    wt = [[0.0] * w for _ in range(h)]
    for y in range(h):
        dy = (y - cy) / norm
        band = 1.0 if top <= (y / max(h - 1, 1)) <= bottom else 0.0
        for x in range(w):
            dx = (x - cx) / norm
            d2 = dx * dx + dy * dy
            k = 1.0 - CENTER_FALLOFF * (d2 if d2 < 1.0 else 1.0)
            if k < 0.3:
                k = 0.3
            k += ILLUSTRATION_BOOST * band
            wt[y][x] = k
    return wt


def extract(surface):
    """Compute the feature vector for one frame or sample image.

    Returns a list of floats, or None if the image cannot be read.
    Length is stable: GRID*GRID*4 values (mean R, G, B and edge
    energy per cell).
    """
    card = preprocess.prepare(surface)
    if card is None:
        return None
    small = pygame.transform.smoothscale(card, (GRID, GRID))
    w, h = small.get_size()
    buf = pygame.image.tobytes(small, 'RGB')

    colour = [0.0] * (w * h * 3)
    lumas = [0.0] * (w * h)
    for y in range(h):
        for x in range(w):
            r, g, b = _cell_mean(buf, w, x, y)
            i = y * w + x
            c = i * 3
            lum = _LR * r + _LG * g + _LB * b
            # Keep absolute colour (helps separate illustrations);
            # only guard near-black cells against noise.
            if lum > 18.0:
                colour[c] = r / 255.0
                colour[c + 1] = g / 255.0
                colour[c + 2] = b / 255.0
            lumas[i] = lum / 255.0

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

    weight = _build_weight_map(w, h)
    out = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            k = weight[y][x]
            c = i * 3
            out.append(colour[c] * k)
            out.append(colour[c + 1] * k)
            out.append(colour[c + 2] * k)
            out.append(edge[i] * k)
    return out


def describe(vec):
    if not vec:
        return 'empty'
    ncell = len(vec) // 4
    edge_sum = sum(vec[i] for i in range(3, len(vec), 4))
    return '%d dims, %d cells, mean edge %.2f' % (len(vec), ncell, edge_sum / ncell)
