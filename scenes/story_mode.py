# ============================================================
#  Story Mode Scene
#  Ties together: StoryEngine, CharacterLayer, scan popup, image popup.
#  You should NOT need to edit this file when adding chapter content.
# ============================================================

import pygame
import config
import game_state
import data.chapters as chapters_data
from story.engine     import StoryEngine
from story.characters import CharacterLayer
from popups           import scan_popup, image_popup

WIDTH = HEIGHT = 0
_go_to_scene   = None

_engine = None
_chars  = None
_last_ticks = 0

# _dbox is recomputed every frame from character bounds + text length.
_dbox: pygame.Rect = pygame.Rect(0, 0, 1, 1)

# ── Typewriter animation ──────────────────────────────────────
TYPING_SPEED   = 38
_typing_chars  = 0.0
_typing_done   = True
_typing_text   = ""
_prev_line_key = None

# ── Black fade transition ─────────────────────────────────────
_FADE_SPEED    = 320        # alpha units per second (0-255)
_HOLD_DURATION = 0.55       # seconds to hold on black before advancing
_fade_phase    = None       # None | "out" | "hold" | "in"
_fade_alpha    = 0
_fade_timer    = 0.0

# ── Chapter-complete overlay ──────────────────────────────────
_chapter_done  = False
_end_buttons   = {}     # {"repeat": Rect, "menu": Rect, "next": Rect}
_last_bg_surf  = None   # cached last background for the overlay backdrop

# ── Asset caches ──────────────────────────────────────────────
_bg_cache         : dict = {}
_logo_cache       : dict = {}
_choice_img_cache : dict = {}
_font_body               = None
_font_hint               = None

# ── Dialogue box style ────────────────────────────────────────
_DBOX_FILL   = (252, 242, 215)
_DBOX_BORDER = (165, 120, 60)
_DBOX_TEXT   = (45,  22,  8)
_HINT_COLOR  = (140, 100, 45)
_BORDER_W    = 3

# ── Choice question box — dark wood, directs question at student ──
_QBOX_FILL   = (72,  38,  10)
_QBOX_BORDER = (165, 100, 35)
_QBOX_TEXT   = (248, 228, 190)

# ── Day counter style ─────────────────────────────────────────
_DAY_FILL   = (240, 220, 185)
_DAY_BORDER = (155, 115, 60)
_DAY_TEXT   = (75,  42,  10)
_DAY_TOTAL  = 30    # overwritten per chapter by _load_chapter()

# ── Water meter (bottom of the planter) ─────────────────────────
_water_level        = 1.0    # 0.0 (bone dry) - 1.0 (freshly watered)
_crop_name          = ""     # current chapter's crop, for tailoring the meter
_pending_water_scan = False  # True while a scan popup for the Water Card is open

_WATER_DECAY_PER_TRANSITION = 0.28   # how much a day-skip dries out the soil
_WATER_BAR_W_FRAC           = 0.34
_WATER_BAR_H_FRAC           = 0.026
_WATER_BOTTOM_MARGIN_FRAC   = 0.035
_WATER_LOW_THRESHOLD        = 0.28
_WATER_DEFAULT_COLOR        = (70, 140, 200)

# Accent colour per crop so the meter reads as "that plant's" water, not a generic bar.
_CROP_WATER_COLORS = {
    "Pechay":   (100, 170, 90),
    "Monggo":   (150, 130, 60),
    "Okra":     (90,  150, 70),
    "Squash":   (230, 150, 40),
    "Tomato":   (200, 70,  55),
    "Eggplant": (120, 70,  140),
    "Kamote":   (170, 90,  140),
    "Rice":     (210, 190, 120),
    "Corn":     (235, 195, 60),
    "Cassava":  (150, 110, 70),
}

# ── Layout constants ──────────────────────────────────────────
_CHAR_GAP_FRAC    = 0.0001   # gap between character right/left edge and box
_EDGE_MARGIN_FRAC = 0.038   # margin from the opposite screen edge (~2 visual inches)


# ─────────────────────────────────────────────────────────────
#  Setup
# ─────────────────────────────────────────────────────────────

def init(width, height, go_to_scene_callback):
    global WIDTH, HEIGHT, _go_to_scene, _last_ticks
    global _font_body, _font_hint

    WIDTH, HEIGHT = width, height
    _go_to_scene  = go_to_scene_callback

    _font_body, _font_hint = _make_fonts(height)

    scan_popup.init(WIDTH, HEIGHT)
    image_popup.init(WIDTH, HEIGHT)
    _last_ticks = pygame.time.get_ticks()


def _make_fonts(h):
    try:
        body = pygame.font.Font("fonts/RumRaisin-Regular.ttf", int(h * 0.065))
        hint = pygame.font.Font("fonts/RumRaisin-Regular.ttf", int(h * 0.036))
        return body, hint
    except Exception:
        body = pygame.font.SysFont("Georgia", int(h * 0.065), bold=True)
        hint = pygame.font.SysFont("Georgia", int(h * 0.036))
        return body, hint


def _make_font(size_frac):
    try:
        return pygame.font.Font("fonts/RumRaisin-Regular.ttf", int(HEIGHT * size_frac))
    except Exception:
        return pygame.font.SysFont("Georgia", int(HEIGHT * size_frac), bold=True)


# ─────────────────────────────────────────────────────────────
#  Chapter loading
# ─────────────────────────────────────────────────────────────

def _load_chapter():
    global _engine, _chars, _DAY_TOTAL, _chapter_done, _last_bg_surf
    global _water_level, _crop_name, _pending_water_scan
    chapter     = chapters_data.load(game_state.selected_chapter)
    _DAY_TOTAL  = chapter.get("total_days", 30)
    _chars      = CharacterLayer(WIDTH, HEIGHT)
    _engine     = StoryEngine(chapter, on_chapter_end=_on_chapter_end)
    _chapter_done = False
    _last_bg_surf = None
    _water_level  = 1.0
    _crop_name    = chapter.get("crop", "")
    _pending_water_scan = False
    _reset_typing()
    _sync_chars()


def _sync_chars():
    if _engine is None or _chars is None:
        return
    s = _engine.slide
    if "day" in s:
        game_state.day = s["day"]
    _chars.set_slide(s.get("chars", {}), _engine.active_char)


def _on_chapter_end():
    global _engine, _chars, _chapter_done
    _chapter_done = True
    _chars = None
    _compute_end_buttons()


def _compute_end_buttons():
    global _end_buttons
    btn_w   = int(WIDTH  * 0.26)
    btn_h   = int(HEIGHT * 0.11)
    gap     = int(WIDTH  * 0.04)
    total_w = btn_w * 3 + gap * 2
    x0      = (WIDTH - total_w) // 2
    y       = int(HEIGHT * 0.60)
    _end_buttons = {
        "repeat": pygame.Rect(x0,                  y, btn_w, btn_h),
        "menu":   pygame.Rect(x0 + btn_w + gap,    y, btn_w, btn_h),
        "next":   pygame.Rect(x0 + (btn_w+gap)*2,  y, btn_w, btn_h),
    }


def _reset_typing():
    global _typing_chars, _typing_done, _typing_text, _prev_line_key
    global _fade_phase, _fade_alpha, _fade_timer
    _typing_chars  = 0.0
    _typing_done   = True
    _typing_text   = ""
    _prev_line_key = None
    _fade_phase    = None
    _fade_alpha    = 0
    _fade_timer    = 0.0


# ─────────────────────────────────────────────────────────────
#  Asset helpers
# ─────────────────────────────────────────────────────────────

def _get_bg(path: str) -> pygame.Surface:
    if path not in _bg_cache:
        raw = pygame.image.load(config.IMG_DIR + path).convert()
        _bg_cache[path] = pygame.transform.smoothscale(raw, (WIDTH, HEIGHT))
    return _bg_cache[path]


def _get_logo(path: str, target_w: int) -> pygame.Surface:
    key = (path, target_w)
    if key not in _logo_cache:
        raw   = pygame.image.load(config.IMG_DIR + path).convert_alpha()
        ratio = target_w / raw.get_width()
        _logo_cache[key] = pygame.transform.smoothscale(
            raw, (target_w, int(raw.get_height() * ratio))
        )
    return _logo_cache[key]


def _get_choice_img(path: str, max_w: int, max_h: int) -> pygame.Surface:
    key = (path, max_w, max_h)
    if key not in _choice_img_cache:
        raw     = pygame.image.load(config.IMG_DIR + path).convert_alpha()
        ratio   = min(max_w / raw.get_width(), max_h / raw.get_height())
        new_w   = max(1, int(raw.get_width()  * ratio))
        new_h   = max(1, int(raw.get_height() * ratio))
        _choice_img_cache[key] = pygame.transform.smoothscale(raw, (new_w, new_h))
    return _choice_img_cache[key]


# ─────────────────────────────────────────────────────────────
#  Dynamic dialogue box — sized to text, anchored to head
# ─────────────────────────────────────────────────────────────

def _wrapped_line_count(text: str, max_px: int) -> int:
    """Count how many visual lines the text wraps into."""
    words = text.split()
    line  = ""
    count = 0
    for word in words:
        test = (line + " " + word).strip()
        if _font_body.size(test)[0] <= max_px:
            line = test
        else:
            if line:
                count += 1
            line = word
    if line:
        count += 1
    return max(count, 1)


def _compute_dbox(full_text: str) -> pygame.Rect:
    """
    Compute the dialogue box rect:
      - Top    : aligned with the character's head (top of sprite).
      - Left   : just past the character's right edge (for left chars),
                 or from the left margin (for right chars).
      - Right  : screen edge minus ~2-inch visual margin.
      - Height : sized exactly to fit the full text + hint row.
    """
    s         = _engine.slide
    active_id = _engine.active_char
    chars_d   = s.get("chars", {})
    side      = chars_d.get(active_id) if active_id else None
    bounds    = _chars.get_char_bounds(active_id) if (_chars and active_id) else None

    edge_margin = int(WIDTH * _EDGE_MARGIN_FRAC)
    char_gap    = int(WIDTH * _CHAR_GAP_FRAC)
    pad         = int(WIDTH * 0.020)

    # Keep the dialogue box top at least 12% from top so it never touches the day counter.
    _DAY_CLEAR = int(HEIGHT * 0.12)

    if bounds and side:
        cx, cy, cw, _ = bounds
        head_y = max(cy, _DAY_CLEAR)
        if side == "left":
            box_left  = cx + cw + char_gap
            box_right = WIDTH - edge_margin
        else:
            box_left  = edge_margin
            box_right = cx - char_gap
    else:
        head_y    = _DAY_CLEAR
        box_left  = edge_margin
        box_right = WIDTH - edge_margin

    box_w = max(box_right - box_left, int(WIDTH * 0.20))

    # Height: one pad above text + text rows + small gap + hint row + one pad below
    n_lines  = _wrapped_line_count(full_text, box_w - pad * 2)
    text_h   = n_lines * _font_body.get_linesize()
    hint_h   = _font_hint.get_linesize()
    box_h    = pad + text_h + int(pad * 0.5) + hint_h + pad

    # Never overflow below the screen
    box_h = min(box_h, HEIGHT - head_y - int(HEIGHT * 0.02))

    return pygame.Rect(box_left, head_y, box_w, box_h)


# ─────────────────────────────────────────────────────────────
#  Input
# ─────────────────────────────────────────────────────────────

def handle_tap(px, py):
    global _typing_chars, _typing_done, _pending_water_scan

    # Chapter-complete overlay intercepts all taps
    if _chapter_done:
        _handle_end_tap(px, py)
        return

    if _engine is None:
        return
    if _fade_phase is not None:
        return  # block input during fade transition

    if _engine.popup_open == "scan":
        scan_popup.handle_tap(px, py)
        return
    if _engine.popup_open == "image":
        image_popup.handle_tap(px, py)
        return

    s = _engine.slide

    # Complete typing on first tap for dialogue/feedback
    if s["type"] in ("dialogue", "end", "feedback"):
        if not _typing_done:
            _typing_chars = float(len(_typing_text))
            _typing_done  = True
            return

    # Image choice buttons
    if s["type"] == "choice":
        for i, btn in enumerate(_choice_image_buttons()):
            if btn.collidepoint(px, py):
                if _engine.choose(i):
                    _sync_chars()
                return
        return

    prev_slide = _engine.slide_idx
    _engine.tap()
    if _engine.slide_idx != prev_slide:
        _sync_chars()

    if _engine.popup_open == "scan":
        card_name = s.get("card", "")
        _pending_water_scan = "water" in card_name.lower()
        scan_popup.open(
            card_name   = card_name,
            question    = s.get("question", ""),
            on_complete = _on_scan_done,
        )


def _on_scan_done():
    global _water_level
    if _engine is None:
        return
    if _pending_water_scan:
        _water_level = 1.0
    _engine.on_scan_complete()
    _sync_chars()


def _handle_end_tap(px, py):
    """Handle taps on the chapter-complete overlay buttons."""
    global _chapter_done, _engine

    idx = chapters_data.CHAPTER_IDS.index(game_state.selected_chapter)
    has_next = idx + 1 < len(chapters_data.CHAPTER_IDS)

    for key, rect in _end_buttons.items():
        if rect.collidepoint(px, py):
            _chapter_done = False
            game_state.day = 0
            if key == "repeat":
                _engine = None
                _load_chapter()
            elif key == "menu":
                game_state.selected_chapter = None
                _go_to_scene("main_menu")
            elif key == "next":
                if has_next:
                    game_state.selected_chapter = chapters_data.CHAPTER_IDS[idx + 1]
                    _engine = None
                    _load_chapter()
                else:
                    game_state.selected_chapter = None
                    _go_to_scene("main_menu")
            return


# ─────────────────────────────────────────────────────────────
#  Drawing
# ─────────────────────────────────────────────────────────────

def draw(surf):
    global _last_ticks, _typing_chars, _typing_done, _typing_text, _prev_line_key
    global _dbox, _fade_phase, _fade_alpha, _fade_timer, _last_bg_surf

    # Chapter-complete overlay
    if _chapter_done:
        _draw_chapter_complete(surf)
        return

    if _engine is None:
        if game_state.selected_chapter:
            _load_chapter()
        else:
            surf.fill(config.STORY_BG_COLOR)
            return

    now = pygame.time.get_ticks()
    dt  = (now - _last_ticks) / 1000.0
    _last_ticks = now

    s     = _engine.slide
    stype = s["type"]

    # ── Background ────────────────────────────────────────────
    bg_path = s.get("bg")
    if bg_path:
        bg = _get_bg(bg_path)
        surf.blit(bg, (0, 0))
        _last_bg_surf = bg
    else:
        surf.fill(config.STORY_BG_COLOR)

    # Dark overlay or coloured tint (for feedback slides)
    tint = s.get("tint")
    if tint:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(tint)
        surf.blit(overlay, (0, 0))
    elif s.get("dark"):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        surf.blit(overlay, (0, 0))

    _chars.update(dt)

    # ── Title slide ───────────────────────────────────────────
    if stype == "title":
        logo_path = s.get("logo")
        if logo_path:
            logo = _get_logo(logo_path, int(WIDTH * 0.50))
            surf.blit(logo, logo.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        return

    # ── Transition slide — kick off the black fade ────────────
    if stype == "transition" and _fade_phase is None:
        _fade_phase = "out"
        _fade_alpha = 0
        _fade_timer = 0.0

    if _fade_phase in ("out", "hold"):
        _apply_fade(surf, dt)
        return

    _chars.draw(surf)

    # ── Typewriter animation (dialogue, feedback) ─────────────
    line = _engine.current_line
    if stype == "choice" and _engine.is_retry and s.get("retry_question"):
        full_text = s["retry_question"]
    else:
        full_text = line[1] if line else s.get("dialogue", s.get("question", ""))
    line_key  = (_engine.slide_idx, _engine.line_idx)

    if stype in ("dialogue", "end", "feedback"):
        if line_key != _prev_line_key:
            _prev_line_key = line_key
            _typing_text   = full_text
            _typing_chars  = 0.0
            _typing_done   = (len(full_text) == 0)

        if not _typing_done:
            _typing_chars = min(_typing_chars + TYPING_SPEED * dt, len(_typing_text))
            if _typing_chars >= len(_typing_text):
                _typing_done = True

    # ── Compute dialogue box ──────────────────────────────────
    _dbox = _compute_dbox(full_text)

    # ── Day counter pill ──────────────────────────────────────
    _draw_day_counter(surf)

    # ── Dialogue box ──────────────────────────────────────────
    _draw_dbox(surf)

    # ── Choice image buttons (only on choice slide) ───────────
    if stype == "choice":
        _draw_choice_image_buttons(surf)

    # ── Water meter (bottom of the planter) ────────────────────
    _draw_water_bar(surf)

    # ── Fade-in overlay (drawn on top of fully-rendered next slide) ──
    if _fade_phase == "in":
        _apply_fade(surf, dt)

    # ── Popups ────────────────────────────────────────────────
    if _engine and _engine.popup_open == "scan":
        scan_popup.draw(surf)
    elif _engine and _engine.popup_open == "image":
        image_popup.draw(surf)


def _apply_fade(surf, dt):
    """Drive the black-fade state machine and blit the overlay."""
    global _fade_phase, _fade_alpha, _fade_timer

    if _fade_phase == "out":
        _fade_alpha = min(255, _fade_alpha + int(_FADE_SPEED * dt))
        if _fade_alpha >= 255:
            _fade_alpha = 255
            _fade_phase = "hold"
            _fade_timer = 0.0

    elif _fade_phase == "hold":
        _fade_timer += dt
        if _fade_timer >= _HOLD_DURATION:
            _engine.tap()   # advance from transition slide to next slide
            _sync_chars()
            _decay_water()  # days passed without a fresh watering
            _fade_phase = "in"
            _fade_alpha = 255

    elif _fade_phase == "in":
        _fade_alpha = max(0, _fade_alpha - int(_FADE_SPEED * dt))
        if _fade_alpha <= 0:
            _fade_phase = None
            return

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(_fade_alpha)
    surf.blit(overlay, (0, 0))


def _decay_water():
    """A day-skip passed without a fresh watering — the soil dries out a bit."""
    global _water_level
    _water_level = max(0.0, _water_level - _WATER_DECAY_PER_TRANSITION)


def _draw_water_bar(surf):
    """Water-level meter anchored to the bottom of the planter bed."""
    s = _engine.slide
    if _engine.popup_open or "planter" not in s.get("bg", ""):
        return

    color = _CROP_WATER_COLORS.get(_crop_name, _WATER_DEFAULT_COLOR)
    low   = _water_level < _WATER_LOW_THRESHOLD

    bar_w = int(WIDTH  * _WATER_BAR_W_FRAC)
    bar_h = int(HEIGHT * _WATER_BAR_H_FRAC)
    bar_x = (WIDTH - bar_w) // 2
    bar_y = HEIGHT - int(HEIGHT * _WATER_BOTTOM_MARGIN_FRAC) - bar_h
    track = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
    r     = bar_h // 2

    # Label
    label_text = f"{_crop_name} Water" if _crop_name else "Water"
    lbl        = _font_hint.render(label_text, True, (250, 245, 230))
    lbl_rect   = lbl.get_rect(midbottom=(WIDTH // 2, bar_y - 4))
    shadow     = _font_hint.render(label_text, True, (30, 20, 10))
    surf.blit(shadow, lbl_rect.move(1, 1))
    surf.blit(lbl, lbl_rect)

    # Track (empty background)
    pygame.draw.rect(surf, (45, 32, 20), track, border_radius=r)

    # Fill (how much water is left)
    if _water_level > 0:
        fill_w = min(bar_w, max(bar_h, int(bar_w * _water_level)))
        fill_color = (215, 70, 55) if low else color
        pygame.draw.rect(surf, fill_color, pygame.Rect(bar_x, bar_y, fill_w, bar_h), border_radius=r)

    # Border — flags red when the crop badly needs watering
    border_color = (235, 90, 70) if low else (245, 235, 210)
    pygame.draw.rect(surf, border_color, track, width=2, border_radius=r)

    # Droplet icon to the left of the bar, tinted to match the crop
    drop_r  = int(bar_h * 0.9)
    drop_cx = bar_x - drop_r - int(WIDTH * 0.012)
    drop_cy = bar_y + bar_h // 2
    drop_color = (215, 70, 55) if low else color
    pygame.draw.circle(surf, drop_color, (drop_cx, drop_cy + drop_r // 3), drop_r)
    pygame.draw.polygon(surf, drop_color, [
        (drop_cx,                     drop_cy - int(drop_r * 1.3)),
        (drop_cx - int(drop_r * 0.85), drop_cy),
        (drop_cx + int(drop_r * 0.85), drop_cy),
    ])
    pygame.draw.circle(surf, (255, 255, 255), (drop_cx, drop_cy + drop_r // 3), drop_r, width=1)


def _draw_day_counter(surf):
    """Pill badge fixed at the top-left corner of the screen."""
    day_text = f"day {game_state.day} / {_DAY_TOTAL}"
    label    = _font_hint.render(day_text, True, _DAY_TEXT)

    pad_x  = int(WIDTH  * 0.016)
    pad_y  = int(HEIGHT * 0.009)
    pill_w = label.get_width()  + pad_x * 2
    pill_h = label.get_height() + pad_y * 2
    pill_r = pill_h // 2

    pill = pygame.Rect(
        int(WIDTH  * 0.018),
        int(HEIGHT * 0.020),
        pill_w,
        pill_h,
    )

    pygame.draw.rect(surf, _DAY_FILL,   pill, border_radius=pill_r)
    pygame.draw.rect(surf, _DAY_BORDER, pill, width=2, border_radius=pill_r)
    surf.blit(label, label.get_rect(center=pill.center))


def _draw_dbox(surf):
    s     = _engine.slide
    stype = s["type"]
    pad   = int(WIDTH * 0.020)

    r = min(18, _dbox.width // 6, _dbox.height // 4)

    fill   = _QBOX_FILL   if stype == "choice" else _DBOX_FILL
    border = _QBOX_BORDER if stype == "choice" else _DBOX_BORDER
    pygame.draw.rect(surf, fill,   _dbox, border_radius=r)
    pygame.draw.rect(surf, border, _dbox, width=_BORDER_W, border_radius=r)

    if stype in ("dialogue", "end", "feedback"):
        visible = _typing_text[:int(_typing_chars)]
        _draw_wrapped(surf, _font_body, visible, _DBOX_TEXT,
                      _dbox.x + pad,
                      _dbox.y + pad,
                      _dbox.width - pad * 2)

        if _typing_done:
            hint = _font_hint.render("tap screen to continue...", True, _HINT_COLOR)
            hint.set_alpha(140)
            surf.blit(hint, hint.get_rect(
                bottomright=(
                    _dbox.right  - pad - _BORDER_W,
                    _dbox.bottom - pad - _BORDER_W,
                )
            ))

    elif stype == "choice":
        q = s.get("retry_question", s["question"]) if _engine.is_retry else s["question"]
        _draw_wrapped(surf, _font_body, q, _QBOX_TEXT,
                      _dbox.x + pad, _dbox.y + pad, _dbox.width - pad * 2)

    elif stype == "scan":
        _draw_wrapped(surf, _font_body, s.get("dialogue", ""), _DBOX_TEXT,
                      _dbox.x + pad, _dbox.y + pad, _dbox.width - pad * 2)
        hint = _font_hint.render("Tap to scan card  >>", True, _HINT_COLOR)
        surf.blit(hint, hint.get_rect(
            bottomright=(_dbox.right - pad, _dbox.bottom - int(pad * 0.4))
        ))


def _choice_image_buttons():
    """Return [left_rect, right_rect] for the two image choice buttons."""
    btn_w   = int(WIDTH  * 0.26)
    btn_h   = int(HEIGHT * 0.40)
    gap     = int(WIDTH  * 0.06)
    total_w = btn_w * 2 + gap
    left_x  = (WIDTH - total_w) // 2
    right_x = left_x + btn_w + gap
    y       = _dbox.bottom + int(HEIGHT * 0.04)
    return [
        pygame.Rect(left_x,  y, btn_w, btn_h),
        pygame.Rect(right_x, y, btn_w, btn_h),
    ]


def _draw_choice_image_buttons(surf):
    s       = _engine.slide
    choices = s.get("choices", [])
    buttons = _choice_image_buttons()
    pad     = int(WIDTH * 0.014)
    r       = 14
    label_font = _font_hint

    for btn, choice in zip(buttons, choices):
        pygame.draw.rect(surf, _DBOX_FILL,   btn, border_radius=r)
        pygame.draw.rect(surf, _DBOX_BORDER, btn, width=_BORDER_W, border_radius=r)

        label_text = choice.get("label", "")

        img_path = choice.get("img")
        if img_path:
            # Reserve space at bottom for text label if present
            label_h = (label_font.get_linesize() + 6) if label_text else 0
            inset   = max(4, int(WIDTH * 0.004))
            img     = _get_choice_img(
                img_path,
                btn.width  - inset * 2,
                btn.height - inset * 2 - label_h,
            )
            img_rect = img.get_rect(
                centerx = btn.centerx,
                centery = btn.top + inset + (btn.height - inset * 2 - label_h) // 2,
            )
            surf.blit(img, img_rect)

        # Text label below the image
        if label_text:
            lbl = label_font.render(label_text, True, _DBOX_TEXT)
            surf.blit(lbl, lbl.get_rect(
                centerx = btn.centerx,
                bottom  = btn.bottom - pad,
            ))


# ─────────────────────────────────────────────────────────────
#  Chapter-complete overlay
# ─────────────────────────────────────────────────────────────

_END_DARK  = (18, 36, 14)
_END_GOLD  = (255, 210, 50)
_END_GREEN = (60,  160, 70)
_END_BLUE  = (40,  90,  170)
_END_AMBER = (180, 100, 20)
_END_GRAY  = (60,  60,  60)


def _draw_chapter_complete(surf):
    # Backdrop — last in-game background dimmed, or solid colour
    if _last_bg_surf:
        surf.blit(_last_bg_surf, (0, 0))
    else:
        surf.fill(_END_DARK)

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 185))
    surf.blit(overlay, (0, 0))

    # ── Title ─────────────────────────────────────────────────
    font_big = _make_font(0.10)
    title    = font_big.render("Kabanata Tapos Na!", True, _END_GOLD)
    surf.blit(title, title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.24))))

    # ── Memory unlocked badge ─────────────────────────────────
    ch       = chapters_data.load(game_state.selected_chapter)
    mem_name = ch.get("memory", "")
    font_med = _make_font(0.052)
    if mem_name:
        badge_text = f"⭐ {mem_name} — Unlocked!"
        badge      = font_med.render(badge_text, True, (200, 240, 180))
        surf.blit(badge, badge.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.40))))

    # ── Buttons ───────────────────────────────────────────────
    idx      = chapters_data.CHAPTER_IDS.index(game_state.selected_chapter)
    has_next = idx + 1 < len(chapters_data.CHAPTER_IDS)

    btn_defs = {
        "repeat": ("Ulitin",    _END_GREEN),
        "menu":   ("Main Menu", _END_BLUE),
        "next":   ("Susunod",   _END_AMBER if has_next else _END_GRAY),
    }

    font_btn = _make_font(0.058)
    pad = int(WIDTH * 0.018)

    for key, rect in _end_buttons.items():
        label_str, color = btn_defs[key]
        pygame.draw.rect(surf, color, rect, border_radius=16)
        pygame.draw.rect(surf, (255, 255, 255), rect, width=2, border_radius=16)
        lbl = font_btn.render(label_str, True, (255, 255, 255))
        surf.blit(lbl, lbl.get_rect(center=rect.center))

    # "Next chapter" name hint
    if has_next:
        next_ch  = chapters_data.load(chapters_data.CHAPTER_IDS[idx + 1])
        hint_str = f"Susunod: {next_ch.get('crop', '')}"
        hint_lbl = _font_hint.render(hint_str, True, (200, 200, 200))
        next_rect = _end_buttons["next"]
        surf.blit(hint_lbl, hint_lbl.get_rect(
            midtop=(next_rect.centerx, next_rect.bottom + 8)
        ))


# ─────────────────────────────────────────────────────────────
#  Text helpers
# ─────────────────────────────────────────────────────────────

def _draw_wrapped(surf, font, text, color, x, y, max_width):
    words  = text.split()
    line   = ""
    line_h = font.get_linesize()
    for word in words:
        test = (line + " " + word).strip()
        if font.size(test)[0] <= max_width:
            line = test
        else:
            surf.blit(font.render(line, True, color), (x, y))
            y   += line_h
            line = word
    if line:
        surf.blit(font.render(line, True, color), (x, y))
