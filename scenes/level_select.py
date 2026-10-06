# ============================================================
#  Level Select Scene
#
#  Layout: three rustic wooden signposts, one per difficulty.
#  Each signpost is a carved board (img/woodbg.png) that acts as
#  the plate for a difficulty name, with that group's chapter
#  cards hanging underneath it on a slim wooden post.
#
#  Tapping a signpost expands / collapses its chapters.
#  Tapping a chapter card starts that chapter.
#
#  You should NOT need to edit this file when adding chapters.
# ============================================================

import time

import pygame

import config
import utils
import game_state
import data.chapters as chapters_data


WIDTH = HEIGHT = 0
_go_to_scene = None

bg_image  = None
back_rect = None

# ── Difficulty definitions ────────────────────────────────────
_DIFF_ORDER  = ["beginner", "intermediate", "advanced"]
_DIFF_LABELS = {
    "beginner":     "Beginner",
    "intermediate": "Intermediate",
    "advanced":     "Expert",
}

# Paint on the ribbon across the top of each wooden sign.
_DIFF_COLORS = {
    "beginner":     (92,  158, 80),
    "intermediate": (206, 146, 48),
    "advanced":     (176, 66,  56),
}
# Slim stripe down the left edge of each chapter card.
_CHAP_COLORS = {
    "beginner":     (136, 196, 110),
    "intermediate": (232, 178, 78),
    "advanced":     (212, 112, 98),
}

# ── Text colours (cream paint on dark wood) ──────────────────
_CREAM     = (253, 241, 208)
_CREAM_DIM = (222, 200, 156)
_GOLD      = (255, 216, 126)
_SHADOW    = (44,  24,  8)

# ── Wood ──────────────────────────────────────────────────────
# The board's carved frame eats into each edge, so text only ever
# goes inside the recessed panel. Fractions of the board measured
# off woodbg.png: (left, top, right, bottom).
_PANEL = (0.090, 0.150, 0.910, 0.850)
# A slice of that panel with no frame in it, i.e. plain wood grain,
# so it can be stretched to any aspect for slim slats (title, post).
_PANEL_CROP = (150, 170, 1000, 430)

# ── Groups (built in init) ────────────────────────────────────
# Each group = { id, label, color, chap_color, chapters[], expanded, anim }
_groups: list = []

# ── Layout (set in init) ──────────────────────────────────────
_TITLE_TOP = 0
_TITLE_H   = 0
_COL_Y     = 0        # top edge of the wooden signs
_PLAQ_W    = 0
_PLAQ_H    = 0
_TILE_TOP  = 0
_TILE_W    = 0
_TILE_H    = 0
_TILE_GAP  = 0
_POST_W    = 0
_POST_H    = 0
_COL_X     = []       # left edge of each signpost

# ── Surfaces, all scaled once in init ─────────────────────────
_plaque_s = None
_tile_s   = None
_post_s   = None
_title_s  = None
_back_s   = None


# ═══════════════════════════════════════════════════════════════
#  Init
# ═══════════════════════════════════════════════════════════════

def init(width, height, go_to_scene_callback):
    global WIDTH, HEIGHT, _go_to_scene, bg_image, back_rect
    global _groups, _last_ticks, _press_at, _pressed, _font_cache
    global _TITLE_TOP, _TITLE_H, _COL_Y
    global _PLAQ_W, _PLAQ_H, _TILE_TOP, _TILE_W, _TILE_H, _TILE_GAP
    global _POST_W, _POST_H, _COL_X
    global _plaque_s, _tile_s, _post_s, _title_s, _back_s
    global _shadow_p, _shadow_t
    global _f_title, _f_name, _f_sub, _f_chap, _f_crop, _f_back

    WIDTH, HEIGHT = width, height
    _go_to_scene  = go_to_scene_callback

    bg_image = utils.load_bg("background/menubg2.png", (WIDTH, HEIGHT))
    wood     = utils.load_img("woodbg.png")
    panel    = wood.subsurface(pygame.Rect(*_PANEL_CROP))

    # ── Load chapters, group by difficulty ──────────────────────
    by_diff = {"beginner": [], "intermediate": [], "advanced": []}
    for ch_id in chapters_data.CHAPTER_IDS:
        ch = chapters_data.load(ch_id)
        ch["_module_id"] = ch_id                         # store full id for game_state
        lvl = ch.get("level", "beginner")
        if lvl not in by_diff:
            lvl = "beginner"
        by_diff[lvl].append(ch)

    _groups = []
    for diff in _DIFF_ORDER:
        _groups.append({
            "id":         diff,
            "label":      _DIFF_LABELS[diff],
            "color":      _DIFF_COLORS[diff],
            "chap_color": _CHAP_COLORS[diff],
            "chapters":   by_diff[diff],
            "expanded":   False,
            "anim":       0.0,
        })

    # ── Layout ─────────────────────────────────────────────────
    _TITLE_H   = int(HEIGHT * 0.085)
    _TITLE_TOP = int(HEIGHT * 0.035)
    _COL_Y     = int(HEIGHT * 0.165)

    # Signs are as tall as the screen allows, then shrunk as a group
    # if the three of them don't fit side by side.
    _PLAQ_H = int(HEIGHT * 0.21)
    _PLAQ_W = int(_PLAQ_H * 1.90)
    gap     = int(WIDTH * 0.032)
    fit     = (WIDTH * 0.92) / (3 * _PLAQ_W + 2 * gap)
    if fit < 1.0:
        _PLAQ_W = int(_PLAQ_W * fit)
        _PLAQ_H = int(_PLAQ_H * fit)
        gap     = int(gap * fit)

    # Cards hang below their sign, trimmed to whatever room the
    # tallest group actually needs.
    _TILE_TOP = _COL_Y + _PLAQ_H + int(HEIGHT * 0.018)
    _TILE_GAP = int(HEIGHT * 0.012)
    rows      = max(1, max(len(g["chapters"]) for g in _groups))
    room      = int(HEIGHT * 0.965) - _TILE_TOP
    _TILE_H   = int((room - _TILE_GAP * (rows - 1)) / rows)
    _TILE_W   = int(_TILE_H * 1.90)
    if _TILE_W > _PLAQ_W * 0.86:                 # never wider than its sign
        _TILE_W = int(_PLAQ_W * 0.86)
        _TILE_H = int(_TILE_W / 1.90)

    _POST_W = max(4, int(_TILE_W * 0.09))
    _POST_H = int(HEIGHT * 0.975) - (_COL_Y + _PLAQ_H)

    total = 3 * _PLAQ_W + 2 * gap
    x0    = max(0, (WIDTH - total) // 2)
    _COL_X = [x0 + i * (_PLAQ_W + gap) for i in range(3)]

    # ── Pre-scale every wooden surface (no per-frame scaling) ───
    _plaque_s = pygame.transform.smoothscale(wood, (_PLAQ_W, _PLAQ_H))
    _tile_s   = pygame.transform.smoothscale(wood, (_TILE_W, _TILE_H))
    _post_s   = pygame.transform.smoothscale(panel, (_POST_W, _POST_H))

    _title_w = int(HEIGHT * 0.145)
    _title_s = pygame.transform.smoothscale(panel, (_title_w, _TITLE_H))

    back_w  = int(min(WIDTH, HEIGHT) * 0.13)
    _back_s = pygame.transform.smoothscale(panel, (back_w, int(back_w / 1.9)))
    back_rect = _back_s.get_rect(topleft=(int(WIDTH * 0.028), _TITLE_TOP))

    _shadow_p = _make_shadow(_PLAQ_W, _PLAQ_H, int(_PLAQ_H * 0.09))
    _shadow_t = _make_shadow(_TILE_W, _TILE_H, int(_TILE_H * 0.14))

    # ── Fonts ──────────────────────────────────────────────────
    _font_cache = {}
    _f_title = _make_font(HEIGHT * 0.046)
    _f_name  = _make_font(HEIGHT * 0.044)
    _f_sub   = _make_font(HEIGHT * 0.023)
    _f_chap  = _make_font(HEIGHT * 0.022)
    _f_crop  = _make_font(HEIGHT * 0.032)
    _f_back  = _make_font(HEIGHT * 0.034)

    _press_at   = 0.0
    _pressed    = None
    _last_ticks = pygame.time.get_ticks()

_shadow_p = None
_shadow_t = None

# ── Fonts ─────────────────────────────────────────────────────
_f_title = None
_f_name  = None
_f_sub   = None
_f_chap  = None
_f_crop  = None
_f_back  = None
_font_cache: dict = {}

# ── Animation / press feedback ────────────────────────────────
ANIM_SPEED  = 6.0     # 0 to 1 per second
_press_at   = 0.0
_pressed    = None    # (kind, gi, ci) currently shrinking
_last_ticks = 0


# ═══════════════════════════════════════════════════════════════
#  Small helpers
# ═══════════════════════════════════════════════════════════════

def _make_font(size):
    try:
        return pygame.font.Font("fonts/RumRaisin-Regular.ttf", int(size))
    except Exception:
        return pygame.font.SysFont("Georgia", int(size), bold=True)


def _fit_font(text, max_w, font, floor=10):
    """Shrink `font` until the text fits max_w, then remember it.

    "Intermediate" is a much longer word than "Expert", so the sign
    names are scaled to their own plank rather than trusting one size.
    """
    key = (text, int(max_w), font.get_height())
    hit = _font_cache.get(key)
    if hit is not None:
        return hit

    size = font.get_height()
    while size > floor and font.size(text)[0] > max_w:
        size = int(size * 0.94)
        font = _make_font(size)

    _font_cache[key] = font
    return font


def _make_shadow(w, h, radius, alpha=115):
    sh = pygame.Surface((max(1, w), max(1, h)), pygame.SRCALPHA)
    pygame.draw.rect(sh, (22, 11, 4, alpha), sh.get_rect(), border_radius=radius)
    return sh


def _scaled_rect(img, rect, k):
    """Where img actually lands when drawn at `k` scale inside rect."""
    if k >= 0.999:
        return rect
    w = max(1, int(img.get_width()  * k))
    h = max(1, int(img.get_height() * k))
    return pygame.Rect(0, 0, w, h).move(
        rect.centerx - w // 2,
        rect.centery - h // 2,
    )


def _blit_scaled(surf, img, rect, k=1.0):
    if k >= 0.999:
        surf.blit(img, rect)
    else:
        out = pygame.transform.smoothscale(
            img, (max(1, int(img.get_width() * k)), max(1, int(img.get_height() * k)))
        )
        surf.blit(out, _scaled_rect(img, rect, k))


def _press_k(item, k=1.0):
    """Multiply a draw scale by the press-shrink while the finger is down."""
    if _pressed == (item["kind"], item["gi"], item["ci"]):
        if time.time() - _press_at < config.PRESS_DURATION:
            return k * config.PRESS_SCALE
    return k


def _paint_text(surf, text, font, color, pos, anchor="center"):
    """Cream paint with a dark offset shadow so it reads on the wood."""
    shadow = font.render(text, True, _SHADOW)
    body   = font.render(text, True, color)
    rect   = body.get_rect(**{anchor: pos})
    surf.blit(shadow, rect.move(2, 3))
    surf.blit(body,   rect)


def _panel_rect(rect):
    """The recessed area inside a carved board, in board-local fractions."""
    l, t, r, b = _PANEL
    return pygame.Rect(
        rect.left + int(l * rect.width),
        rect.top  + int(t * rect.height),
        int((r - l) * rect.width),
        int((b - t) * rect.height),
    )


# ═══════════════════════════════════════════════════════════════
#  Layout
# ═══════════════════════════════════════════════════════════════

def _compute_layout():
    """
    Every visible board this frame.
    Each item: { kind:"diff"|"chap", gi, ci, rect, [ch] }

    The three signs sit side by side; each group's chapter cards
    stack underneath its own sign, and only appear while it is open.
    """
    items = []
    for gi, g in enumerate(_groups):
        x = _COL_X[gi]
        items.append({
            "kind": "diff",
            "gi": gi, "ci": -1,
            "rect": pygame.Rect(x, _COL_Y, _PLAQ_W, _PLAQ_H),
        })

        if g["anim"] <= 0.001:
            continue

        cx = x + (_PLAQ_W - _TILE_W) // 2
        y  = _TILE_TOP
        for ci, ch in enumerate(g["chapters"]):
            items.append({
                "kind": "chap",
                "gi": gi, "ci": ci,
                "rect": pygame.Rect(cx, y, _TILE_W, _TILE_H),
                "ch": ch,
            })
            y += _TILE_H + _TILE_GAP
    return items



# ═══════════════════════════════════════════════════════════════
#  Input
# ═══════════════════════════════════════════════════════════════

def handle_tap(px, _py):
    """Remember the press so the board under the finger shrinks."""
    global _press_at, _pressed
    for item in _compute_layout():
        if item["rect"].collidepoint(px, _py):
            _pressed = (item["kind"], item["gi"], item["ci"])
            _press_at = time.time()
            return


def handle_drag(_px, _py):
    """Nothing to drag, but main.py still calls this."""
    pass


def handle_release(px, py):
    global _pressed
    _pressed = None

    if back_rect and back_rect.collidepoint(px, py):
        _go_to_scene("main_menu")
        return

    for item in _compute_layout():
        if not item["rect"].collidepoint(px, py):
            continue
        if item["kind"] == "diff":
            g = _groups[item["gi"]]
            g["expanded"] = not g["expanded"]
        elif item["kind"] == "chap":
            ch = item["ch"]
            game_state.selected_chapter = ch["_module_id"]
            _go_to_scene("story_mode")
        return




# ═══════════════════════════════════════════════════════════════
#  Drawing
# ═══════════════════════════════════════════════════════════════

def draw(surf):
    global _last_ticks

    now = pygame.time.get_ticks()
    dt  = (now - _last_ticks) / 1000.0
    _last_ticks = now

    # ── Animate expand / collapse ──────────────────────────────
    for g in _groups:
        if g["expanded"]:
            g["anim"] = min(1.0, g["anim"] + ANIM_SPEED * dt)
        else:
            g["anim"] = max(0.0, g["anim"] - ANIM_SPEED * dt)

    surf.blit(bg_image, (0, 0))

    _draw_title(surf)

    # Posts first, so the cards hang in front of them.
    for gi, g in enumerate(_groups):
        if g["anim"] > 0.001:
            _draw_post(surf, gi, g)

    for item in _compute_layout():
        if item["kind"] == "diff":
            _draw_sign(surf, item)
        else:
            _draw_card(surf, item)

    _draw_back(surf)


def _draw_title(surf):
    rect = _title_s.get_rect(midtop=(WIDTH // 2, _TITLE_TOP))
    _blit_scaled(surf, _title_s, rect)
    _paint_text(
        surf,
        "Piliin ang Kabanata",
        _fit_font("Piliin ang Kabanata", int(rect.width * 0.88), _f_title),
        _CREAM,
        rect.center,
    )


def _draw_post(surf, gi, g):
    """Slim wooden post the chapter cards hang from."""
    a = g["anim"]
    x = _COL_X[gi] + _PLAQ_W // 2
    rect = pygame.Rect(
        x - _POST_W // 2,
        _COL_Y + _PLAQ_H - int(_POST_H * 0.06),
        _POST_W,
        _POST_H,
    )
    k = 0.35 + 0.65 * a
    _blit_scaled(surf, _post_s, rect, k)


def _draw_sign(surf, item):
    """The difficulty name, painted on its own carved board."""
    g = _groups[item["gi"]]
    k = _press_k(item)
    rect = item["rect"]

    _blit_scaled(surf, _shadow_p, rect.move(0, int(HEIGHT * 0.008)), k)
    _blit_scaled(surf, _plaque_s, rect, k)

    panel = _panel_rect(_scaled_rect(_plaque_s, rect, k))

    # Ribbon of paint across the top of the recessed panel.
    rib_h = max(4, int(panel.height * 0.20))
    rib   = pygame.Rect(panel.left, panel.top, panel.width, rib_h)
    pygame.draw.rect(surf, g["color"], rib, border_radius=int(rib_h * 0.4))
    pygame.draw.rect(
        surf, _CREAM_DIM, rib, width=2, border_radius=int(rib_h * 0.4)
    )

    # Name, then the chapter count underneath it.
    mid = panel.centerx
    _paint_text(
        surf,
        g["label"],
        _fit_font(g["label"], int(panel.width * 0.84), _f_name),
        _CREAM,
        (mid, panel.top + rib_h + int(panel.height * 0.34)),
    )

    n = len(g["chapters"])
    _paint_text(
        surf,
        f"{n} chapter{'s' if n != 1 else ''}",
        _fit_font(f"{n} chapters", int(panel.width * 0.70), _f_sub),
        _CREAM_DIM,
        (mid, panel.top + rib_h + int(panel.height * 0.66)),
    )


def _draw_card(surf, item):
    """One chapter, hanging on the post under its difficulty sign."""
    g   = _groups[item["gi"]]
    ch  = item["ch"]
    a   = g["anim"]
    k   = _press_k(item, 0.80 + 0.20 * a)
    rect = item["rect"]

    _blit_scaled(surf, _shadow_t, rect.move(0, int(HEIGHT * 0.006)), k)
    _blit_scaled(surf, _tile_s, rect, k)

    r    = _scaled_rect(_tile_s, rect, k)
    panel = _panel_rect(r)

    # Difficulty-coloured stripe down the left edge of the panel.
    stripe_w = max(3, int(panel.width * 0.035))
    pygame.draw.rect(
        surf,
        g["chap_color"],
        pygame.Rect(panel.left, panel.top, stripe_w, panel.height),
        border_radius=stripe_w,
    )

    ch_num = chapters_data.CHAPTER_IDS.index(ch["_module_id"]) + 1
    _paint_text(
        surf,
        f"KABANATA {ch_num}",
        _fit_font(f"KABANATA {ch_num}", int(panel.width * 0.72), _f_chap),
        _GOLD,
        (panel.left + stripe_w + int(panel.width * 0.40), panel.centery - int(panel.height * 0.19)),
    )
    _paint_text(
        surf,
        ch["crop"],
        _fit_font(ch["crop"], int(panel.width * 0.72), _f_crop),
        _CREAM,
        (panel.left + stripe_w + int(panel.width * 0.40), panel.centery + int(panel.height * 0.21)),
    )


def _draw_back(surf):
    _blit_scaled(surf, _back_s, back_rect)
    _paint_text(surf, "<", _f_back, _CREAM, back_rect.center)
