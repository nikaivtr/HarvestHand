# ============================================================
#  Level Select Scene
#
#  Layout: three difficulty boxes (Beginner / Intermediate / Expert).
#  Tapping a difficulty expands it — chapter cards slide out to the right.
#  Tapping it again collapses them.
#  Drag left/right to scroll when expanded content is wider than the screen.
# ============================================================

import pygame
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
_DIFF_COLORS = {                       # difficulty box colour
    "beginner":     (45,  150,  75),
    "intermediate": (190, 125,  30),
    "advanced":     (165,  50,  50),
}
_CHAP_COLORS = {                       # chapter card colour (darker shade)
    "beginner":     (28,  105,  52),
    "intermediate": (145,  95,  20),
    "advanced":     (120,  30,  30),
}

# ── Groups (built in init) ────────────────────────────────────
# Each group = { id, label, color, chap_color, chapters[], expanded, anim }
_groups: list = []

# ── Layout constants (set in init) ────────────────────────────
_BOX_H  = 0   # height of every box
_DIFF_W = 0   # width of a difficulty box
_CHAP_W = 0   # full width of a chapter card
_GAP    = 0   # gap between boxes
_ROW_Y  = 0   # top edge of the row
_X0     = 0   # left start x (centers the 3 boxes when all collapsed)

# ── Scroll state ──────────────────────────────────────────────
_scroll_x       = 0.0
_drag_start_x   = 0
_drag_start_scr = 0.0
_is_dragging    = False
DRAG_THRESHOLD  = 8    # px before a tap becomes a drag

# ── Animation ─────────────────────────────────────────────────
ANIM_SPEED  = 6.0  # 0→1 per second
_last_ticks = 0


# ═══════════════════════════════════════════════════════════════
#  Init
# ═══════════════════════════════════════════════════════════════

def init(width, height, go_to_scene_callback):
    global WIDTH, HEIGHT, _go_to_scene, bg_image, back_rect
    global _BOX_H, _DIFF_W, _CHAP_W, _GAP, _ROW_Y, _X0
    global _groups, _scroll_x, _last_ticks

    WIDTH, HEIGHT = width, height
    _go_to_scene  = go_to_scene_callback

    bg_image = utils.load_bg("background/menubg2.png", (WIDTH, HEIGHT))

    back_size = int(min(WIDTH, HEIGHT) * 0.08)
    back_rect = pygame.Rect(int(WIDTH * 0.03), int(HEIGHT * 0.03), back_size, back_size)

    _BOX_H  = int(HEIGHT * 0.52)
    _DIFF_W = int(WIDTH  * 0.20)
    _CHAP_W = int(WIDTH  * 0.14)
    _GAP    = int(WIDTH  * 0.025)
    _ROW_Y  = HEIGHT // 2 - _BOX_H // 2

    # Center the 3 difficulty boxes when all are collapsed
    collapsed_total = 3 * _DIFF_W + 4 * _GAP
    _X0 = max(_GAP, (WIDTH - collapsed_total) // 2)

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

    _scroll_x   = 0.0
    _last_ticks = pygame.time.get_ticks()


# ═══════════════════════════════════════════════════════════════
#  Layout helpers
# ═══════════════════════════════════════════════════════════════

def _compute_layout():
    """
    Returns a list of items describing every visible box this frame.
    Each item: { kind:"diff"|"chap", gi, ci, rect, [ch] }
    Positions account for scroll_x and current anim values.
    """
    items = []
    x = _X0 - int(_scroll_x)

    for gi, g in enumerate(_groups):
        # Difficulty box
        items.append({
            "kind": "diff",
            "gi": gi, "ci": -1,
            "rect": pygame.Rect(x, _ROW_Y, _DIFF_W, _BOX_H),
        })
        x += _DIFF_W + _GAP

        # Chapter cards (width grows 0 → _CHAP_W as anim goes 0 → 1)
        if g["anim"] > 0:
            card_w = max(1, int(_CHAP_W * g["anim"]))
            for ci, ch in enumerate(g["chapters"]):
                items.append({
                    "kind": "chap",
                    "gi": gi, "ci": ci,
                    "rect": pygame.Rect(x, _ROW_Y, card_w, _BOX_H),
                    "ch": ch,
                })
                x += card_w + _GAP

    return items


def _content_right_edge():
    """Right edge of all content at full expansion."""
    x = _X0
    for g in _groups:
        x += _DIFF_W + _GAP
        if g["anim"] > 0:
            x += len(g["chapters"]) * (int(_CHAP_W * g["anim"]) + _GAP)
    return x


def _max_scroll():
    return max(0.0, _content_right_edge() - WIDTH + _GAP)


# ═══════════════════════════════════════════════════════════════
#  Input  (tap = finger/mouse down, drag = motion, release = up)
# ═══════════════════════════════════════════════════════════════

def handle_tap(px, _py):
    """Records the start of a potential drag. Clicks fire on release."""
    global _drag_start_x, _drag_start_scr, _is_dragging
    _drag_start_x   = px
    _drag_start_scr = _scroll_x
    _is_dragging    = False


def handle_drag(px, _py2):
    global _scroll_x, _is_dragging
    dx = _drag_start_x - px
    if abs(dx) > DRAG_THRESHOLD:
        _is_dragging = True
    if _is_dragging:
        _scroll_x = max(0.0, min(_max_scroll(), _drag_start_scr + dx))


def handle_release(px, _py):
    if _is_dragging:
        return  # was a scroll, not a tap

    # Back button
    if back_rect and back_rect.collidepoint(px, _py):
        _go_to_scene("main_menu")
        return

    # Check which box was tapped
    for item in _compute_layout():
        if item["rect"].collidepoint(px, _py):
            if item["kind"] == "diff":
                g = _groups[item["gi"]]
                g["expanded"] = not g["expanded"]
            elif item["kind"] == "chap":
                ch = item["ch"]
                game_state.selected_chapter = ch["_module_id"]
                _go_to_scene("story_mode")
            return


# ═══════════════════════════════════════════════════════════════
#  Draw
# ═══════════════════════════════════════════════════════════════

def draw(surf):
    global _last_ticks

    now = pygame.time.get_ticks()
    dt  = (now - _last_ticks) / 1000.0
    _last_ticks = now

    # ── Animate expand / collapse ────────────────────────────────
    for g in _groups:
        if g["expanded"]:
            g["anim"] = min(1.0, g["anim"] + ANIM_SPEED * dt)
        else:
            g["anim"] = max(0.0, g["anim"] - ANIM_SPEED * dt)

    # ── Background ───────────────────────────────────────────────
    surf.blit(bg_image, (0, 0))

    # ── Title ────────────────────────────────────────────────────
    font_title = pygame.font.SysFont(None, int(HEIGHT * 0.055))
    title = font_title.render("Piliin ang Kabanata", True, (255, 255, 255))
    surf.blit(title, title.get_rect(midtop=(WIDTH // 2, int(HEIGHT * 0.05))))

    # ── Boxes ────────────────────────────────────────────────────
    layout = _compute_layout()
    font_diff = pygame.font.SysFont(None, int(HEIGHT * 0.048))
    font_sub  = pygame.font.SysFont(None, int(HEIGHT * 0.028))
    font_chap = pygame.font.SysFont(None, int(HEIGHT * 0.030))
    font_crop = pygame.font.SysFont(None, int(HEIGHT * 0.038))

    for item in layout:
        g    = _groups[item["gi"]]
        rect = item["rect"]

        if item["kind"] == "diff":
            # Difficulty box
            border_col = (255, 230, 80) if g["expanded"] or g["anim"] > 0 else (200, 200, 200)
            pygame.draw.rect(surf, g["color"], rect, border_radius=14)
            pygame.draw.rect(surf, border_col, rect, width=3, border_radius=14)

            # Difficulty name
            lbl = font_diff.render(g["label"], True, (255, 255, 255))
            surf.blit(lbl, lbl.get_rect(center=(rect.centerx, rect.centery - int(HEIGHT * 0.04))))

            # Chapter count
            n = len(g["chapters"])
            sub = font_sub.render(f"{n} chapter{'s' if n != 1 else ''}", True, (220, 220, 180))
            surf.blit(sub, sub.get_rect(center=(rect.centerx, rect.centery + int(HEIGHT * 0.01))))

            # Expand arrow
            arrow = "v" if (g["expanded"] or g["anim"] > 0.5) else ">"
            arr_surf = font_sub.render(arrow, True, (255, 255, 255))
            surf.blit(arr_surf, arr_surf.get_rect(midbottom=(rect.centerx, rect.bottom - 14)))

        elif item["kind"] == "chap":
            # Chapter card — only draw content when wide enough
            pygame.draw.rect(surf, g["chap_color"], rect, border_radius=10)
            pygame.draw.rect(surf, (200, 200, 200), rect, width=2, border_radius=10)

            if g["anim"] > 0.55 and rect.width > 60:
                ch = item["ch"]

                # Find global chapter number
                ch_num = chapters_data.CHAPTER_IDS.index(ch["_module_id"]) + 1

                # Clip text to the card boundaries
                surf.set_clip(rect)

                num_lbl = font_chap.render(f"Ch {ch_num}", True, (255, 220, 80))
                surf.blit(num_lbl, num_lbl.get_rect(midtop=(rect.centerx, rect.top + 14)))

                crop_lbl = font_crop.render(ch["crop"], True, (255, 255, 255))
                surf.blit(crop_lbl, crop_lbl.get_rect(center=(rect.centerx, rect.centery)))

                tap_lbl = font_sub.render("Tap to play", True, (180, 220, 180))
                surf.blit(tap_lbl, tap_lbl.get_rect(midbottom=(rect.centerx, rect.bottom - 14)))

                surf.set_clip(None)

    # ── Scrollbar ────────────────────────────────────────────────
    max_s = _max_scroll()
    if max_s > 0:
        _draw_scrollbar(surf, max_s)

    # ── Back button ──────────────────────────────────────────────
    pygame.draw.rect(surf, (50, 50, 65), back_rect, border_radius=8)
    pygame.draw.rect(surf, (255, 255, 255), back_rect, width=2, border_radius=8)
    bfont = pygame.font.SysFont(None, int(HEIGHT * 0.042))
    blbl  = bfont.render("<", True, (255, 255, 255))
    surf.blit(blbl, blbl.get_rect(center=back_rect.center))


def _draw_scrollbar(surf, max_s):
    bar_h = 6
    bar_y = _ROW_Y + _BOX_H + 18
    bar_x = _GAP
    bar_w = WIDTH - 2 * _GAP

    # Track
    pygame.draw.rect(surf, (60, 60, 80), pygame.Rect(bar_x, bar_y, bar_w, bar_h), border_radius=3)

    # Thumb
    visible_ratio = min(1.0, WIDTH / (_content_right_edge() + 1))
    thumb_w = max(40, int(bar_w * visible_ratio))
    scroll_ratio = _scroll_x / max_s if max_s > 0 else 0
    thumb_x = bar_x + int(scroll_ratio * (bar_w - thumb_w))
    pygame.draw.rect(surf, (160, 160, 210), pygame.Rect(thumb_x, bar_y, thumb_w, bar_h), border_radius=3)
