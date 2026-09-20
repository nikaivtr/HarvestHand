# ============================================================
#  Story Mode Scene
#  Ties together: StoryEngine, CharacterLayer, scan popup, image popup.
#  You should NOT need to edit this file when adding chapter content.
# ============================================================

import random

import pygame
import config
import game_state
import data.chapters as chapters_data
from story.engine     import StoryEngine
from story.characters import CharacterLayer, get_slot_width
from story.effects    import SmokeFX
from popups           import scan_popup, image_popup


WIDTH = HEIGHT = 0
_go_to_scene   = None

_engine = None
_chars  = None
_smoke  = None
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

# ── Camera shake (slide flag: "shake": True) ─────────────────
SHAKE_DURATION  = 0.45     # seconds the shake lasts after landing
SHAKE_INTENSITY = 0.008    # max offset as a fraction of screen width
_shake_timer = 0.0
_shake_surf: pygame.Surface | None = None

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
_dialogue_font           = None

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
_EDGE_MARGIN_FRAC = 0.03

# Each character occupies one fixed invisible horizontal slot.
# The character itself is rendered at CHARACTER_W × 727 px by
# story/characters.py.
_CHARACTER_SLOT_GAP = 20

# Dialogue box placement. The box uses whatever horizontal space
# remains after left/right character slots are accounted for, then
# clamps to a maximum width so the box stays compact even when the
# characters leave a lot of room.
_DIALOGUE_TOP_FRAC = 0.12
_DIALOGUE_MAX_HEIGHT_FRAC = 0.22
_DIALOGUE_MAX_WIDTH_FRAC = 0.52

# Middle margin between the characters' artwork and the dialogue
# box: 5% of screen width when the box shares the screen with one
# character, 2% on each side when characters stand on both sides.
# Measured from the art's actual drawn edges so the box never sits
# on top of a character.
_DBOX_SIDE_MARGIN_FRAC = 0.05
_DBOX_MID_MARGIN_FRAC = 0.02

# Padding around the box's content, as a fraction of screen width.
# Shared by _compute_dbox() (sizing) and _draw_dbox() (drawing) so
# the two always agree.
_DBOX_PAD_FRAC = 0.014

# Base dialogue text size, as a fraction of the box's inner text
# width. Because the box's width is whatever space the character
# slots leave over, the text automatically gets smaller when 1-2
# characters are on screen and bigger when the box is wider.
_DIALOGUE_FONT_W_FRAC = 0.042

# Ceiling for the dialogue font, as a fraction of screen height
# (POINT size). Deliberately much smaller than the body font
# (0.065 in _make_fonts) so dialogue text stays compact.
_DIALOGUE_MAX_FONT_FRAC = 0.042

# Point-size fraction for the small corner hint line inside the
# dialogue box ("tap screen to continue..."). Smaller than the
# shared _font_hint so it adds less height to every box.
_DIALOGUE_HINT_PT_FRAC = 0.022

# The font will shrink only as much as needed. The floor is stored
# as a fraction of screen height so it stays readable on any
# resolution.
_DIALOGUE_MIN_FONT_FRAC = 0.024


# ─────────────────────────────────────────────────────────────
#  Setup
# ─────────────────────────────────────────────────────────────

def init(width, height, go_to_scene_callback):
    global WIDTH, HEIGHT, _go_to_scene, _last_ticks
    global _font_body, _font_hint, _smoke

    WIDTH, HEIGHT = width, height
    _go_to_scene  = go_to_scene_callback

    _font_body, _font_hint = _make_fonts(height)

    scan_popup.init(WIDTH, HEIGHT)
    image_popup.init(WIDTH, HEIGHT)
    _smoke = SmokeFX(width, height)
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
    _chars.set_slide(
        s.get("chars", {}),
        _engine.active_char,
        dim_others=bool(s.get("dim_inactive", False)),
    )
    _start_shake_if_flagged()

    # Smoke panels (e.g. S2P21) also fire a dense one-shot burst on
    # arrival; emission continues while the slide stays on screen.
    if _smoke is not None:
        if s.get("smoke"):
            _smoke.start(burst=True)
        else:
            _smoke.stop()


def _start_shake_if_flagged():
    """Called every time we land on a slide. If the slide carries the
    "shake" flag, kick off a camera shake — e.g. tapping from S2P20
    into S2P21 (the Baron's explosion) rattles the screen."""
    global _shake_timer
    if _engine is not None and _engine.slide.get("shake"):
        _shake_timer = SHAKE_DURATION


def _blit_shaken(surf: pygame.Surface):
    """Present the offscreen frame with a decaying random offset.
    The thin gaps this reveals at the screen edges read as impact."""
    if _shake_timer <= 0 or _shake_surf is None:
        return
    t = _shake_timer / SHAKE_DURATION
    mag = int(SHAKE_INTENSITY * WIDTH * t)
    dx = random.randint(-mag, mag)
    dy = random.randint(-mag, mag)
    surf.fill((0, 0, 0))
    surf.blit(_shake_surf, (dx, dy))


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

def _wrapped_line_count(text: str, max_px: int, font=None) -> int:
    """Count visual lines using the supplied font and width."""
    if font is None:
        font = _font_body

    words = text.split()
    if not words:
        return 1

    line = ""
    count = 0

    for word in words:
        test = (line + " " + word).strip()

        if font.size(test)[0] <= max_px:
            line = test
        else:
            if line:
                count += 1
                line = word
            else:
                # A single word is wider than the box. Count it as
                # one line; _draw_wrapped() will place it on a line.
                count += 1
                line = ""

    if line:
        count += 1

    return max(count, 1)


def _dialogue_min_font_px() -> int:
    """Smallest allowed dialogue font size, in screen pixels."""
    return max(16, int(HEIGHT * _DIALOGUE_MIN_FONT_FRAC))


# Pixel-sized dialogue fonts are created during _fit_dialogue_font(),
# which runs every frame — cache them so the shrink search only pays
# the cost once per size.
_font_px_cache: dict[int, pygame.font.Font] = {}


def _make_font_px(size_px: int):
    """Create (and cache) the story font at an exact pixel size."""
    size_px = max(1, int(size_px))

    cached = _font_px_cache.get(size_px)
    if cached is not None:
        return cached

    try:
        font = pygame.font.Font(
            "fonts/RumRaisin-Regular.ttf",
            size_px
        )
    except Exception:
        font = pygame.font.SysFont(
            "Georgia",
            size_px,
            bold=True
        )

    _font_px_cache[size_px] = font
    return font


def _dialogue_hint_font():
    """Small font for the dialogue box's corner hint line."""
    return _make_font_px(
        max(12, int(HEIGHT * _DIALOGUE_HINT_PT_FRAC))
    )


def _fit_dialogue_font(text: str, max_width: int, max_height: int, pad: int):
    """
    Find the largest font that lets the full dialogue fit in the
    available width/height.
    """
    max_width = max(1, int(max_width))
    max_height = max(1, int(max_height))

    # Start from a size that tracks the box's width (bigger box ->
    # bigger text), but never render taller than normal body text.
    base = int(max_width * _DIALOGUE_FONT_W_FRAC)
    size = min(
        int(HEIGHT * _DIALOGUE_MAX_FONT_FRAC),
        max(_dialogue_min_font_px(), base)
    )

    while size >= _dialogue_min_font_px():
        font = _make_font_px(size)

        line_count = _wrapped_line_count(
            text,
            max_width,
            font
        )

        text_height = (
            line_count
            * font.get_linesize()
        )

        hint_height = _dialogue_hint_font().get_linesize()

        required_height = (
            pad
            + text_height
            + int(pad * 0.3)
            + hint_height
            + pad
        )

        if required_height <= max_height:
            return font, required_height

        size -= 1

    font = _make_font_px(_dialogue_min_font_px())
    line_count = _wrapped_line_count(
        text,
        max_width,
        font
    )

    text_height = (
        line_count
        * font.get_linesize()
    )

    hint_height = _dialogue_hint_font().get_linesize()

    required_height = (
        pad
        + text_height
        + int(pad * 0.3)
        + hint_height
        + pad
    )

    return font, required_height


def _count_character_slots(chars_d: dict) -> tuple[int, int]:
    """Return (left_count, right_count) for the current slide."""
    left_count = 0
    right_count = 0

    for spec in chars_d.values():
        if isinstance(spec, str):
            side = spec
        elif isinstance(spec, dict):
            side = spec.get("side", "left")
        else:
            continue

        if side == "left":
            left_count += 1
        elif side == "right":
            right_count += 1

    return left_count, right_count


def _character_art_edges(chars_d: dict) -> tuple[int | None, int | None]:
    """
    Return (left_art_right, right_art_left): the right-most drawn
    edge of the left-side characters and the left-most drawn edge of
    the right-side characters on the current slide. The dialogue
    box's margins are measured from these so it never sits on top of
    the artwork. A value is None when that side has no character (or
    its bounds are unavailable). Only characters on the current slide
    count — ones still sliding out are ignored.
    """
    left_art_right = None
    right_art_left = None

    if _chars is None:
        return left_art_right, right_art_left

    for cid, spec in chars_d.items():
        if isinstance(spec, str):
            side = spec
        elif isinstance(spec, dict):
            side = spec.get("side", "left")
        else:
            continue

        bounds = _chars.get_char_bounds(cid)
        if bounds is None:
            continue

        x, _y, w, _h = bounds

        if side == "left":
            edge = x + w
            left_art_right = (
                edge if left_art_right is None
                else max(left_art_right, edge)
            )
        else:
            right_art_left = (
                x if right_art_left is None
                else min(right_art_left, x)
            )

    return left_art_right, right_art_left


def _compute_dbox(full_text: str) -> pygame.Rect:
    """
    Compute the dialogue box for the current slide.

    Horizontal placement is measured from the characters' actual
    drawn edges (so the box never sits on top of the artwork):

        1 left character:
            [ CHAR ](--5%--)[      DIALOGUE      ]|edge

        1 right character:
            edge|[      DIALOGUE      ](--5%--)[ CHAR ]

        2 characters (left + right):
            [ CHAR ](-2%-)[  DIALOGUE  ](-2%-)[ CHAR ]

        no characters:
            [        centred, width-capped box        ]

    Characters are drawn after the dialogue box.
    """
    global _dialogue_font

    chars_d = _engine.slide.get("chars", {})

    pad = int(WIDTH * _DBOX_PAD_FRAC)
    edge_margin = int(WIDTH * _EDGE_MARGIN_FRAC)

    box_top = int(
        HEIGHT * _DIALOGUE_TOP_FRAC
    )

    max_box_height = int(
        HEIGHT * _DIALOGUE_MAX_HEIGHT_FRAC
    )

    left_count, right_count = _count_character_slots(chars_d)

    # ---------------------------------------------------------
    # Calculate horizontal space occupied by character slots.
    # ---------------------------------------------------------
    slot_w = get_slot_width(WIDTH)

    # Gap between logical character slots.
    slot_gap = int(
        _CHARACTER_SLOT_GAP
        * WIDTH
        / 1920
    )

    left_slots_width = (
        left_count * slot_w
        + max(0, left_count - 1) * slot_gap
    )

    right_slots_width = (
        right_count * slot_w
        + max(0, right_count - 1) * slot_gap
    )

    # ---------------------------------------------------------
    # Horizontal placement of the dialogue area. Margins are
    # measured from the characters' actual drawn edges so the box
    # never sits on top of the artwork:
    #
    #   1 character         → box hugs the FAR side of the screen,
    #                         5% middle margin to the character.
    #   2 characters (L+R)  → box fills the middle, 2% margin to
    #                         the art on each side.
    #   no characters       → centred box with a capped width.
    # ---------------------------------------------------------
    left_art_right, right_art_left = _character_art_edges(chars_d)

    # Fall back to the slot boundaries when art bounds are missing.
    if left_count and left_art_right is None:
        left_art_right = edge_margin + left_slots_width
    if right_count and right_art_left is None:
        right_art_left = WIDTH - edge_margin - right_slots_width

    side_margin = int(WIDTH * _DBOX_SIDE_MARGIN_FRAC)
    mid_margin = int(WIDTH * _DBOX_MID_MARGIN_FRAC)

    if left_count and right_count:
        # Box fills the middle, with a small margin to each character.
        box_left = left_art_right + mid_margin
        box_right = right_art_left - mid_margin

    elif left_count:
        # Box hugs the far RIGHT edge, with a bigger margin so it
        # never sits on top of the left character.
        box_right = WIDTH - edge_margin
        box_left = left_art_right + side_margin

    elif right_count:
        # Mirror: box hugs the far LEFT edge.
        box_left = edge_margin
        box_right = right_art_left - side_margin

    else:
        # No characters → centred box with a capped width.
        box_left = edge_margin
        box_right = WIDTH - edge_margin

        max_box_width = int(WIDTH * _DIALOGUE_MAX_WIDTH_FRAC)
        if box_right - box_left > max_box_width:
            center = (box_left + box_right) // 2
            box_left = center - max_box_width // 2
            box_right = box_left + max_box_width

    # ---------------------------------------------------------
    # Safety: if many character slots consume the available
    # screen, keep a minimum usable dialogue width.
    # ---------------------------------------------------------
    minimum_width = int(
        WIDTH * 0.20
    )

    if box_right - box_left < minimum_width:
        center = (
            box_left
            + box_right
        ) // 2

        box_left = (
            center
            - minimum_width // 2
        )

        box_right = (
            box_left
            + minimum_width
        )

    # Clamp to the screen.
    box_left = max(
        edge_margin,
        int(box_left)
    )

    box_right = min(
        WIDTH - edge_margin,
        int(box_right)
    )

    box_width = max(
        1,
        box_right - box_left
    )

    # ---------------------------------------------------------
    # Automatically choose the largest font that fits.
    # ---------------------------------------------------------
    text_width = max(
        1,
        box_width - pad * 2
    )

    _dialogue_font, box_height = _fit_dialogue_font(
        full_text,
        text_width,
        max_box_height,
        pad
    )

    # Never allow the box to extend below the screen.
    box_height = min(
        box_height,
        HEIGHT
        - box_top
        - int(HEIGHT * 0.02)
    )

    return pygame.Rect(
        int(box_left),
        int(box_top),
        int(box_width),
        int(box_height)
    )


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

    # The tap may have ended the chapter (on_chapter_end fired during
    # engine.tap) — don't touch the engine afterwards.
    if _chapter_done:
        return

    if _engine.slide_idx != prev_slide:
        _sync_chars()

    # The chapter may have ended without slide_idx changing (e.g. all
    # trailing slides were skipped feedback) — don't touch the engine
    # once on_chapter_end() has fired.
    if _engine is None:
        return

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
    global _shake_timer, _shake_surf

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

    # ── Camera shake ─────────────────────────────────────────
    if _shake_timer > 0:
        _shake_timer = max(0.0, _shake_timer - dt)
    shaking = _shake_timer > 0
    if shaking:
        if _shake_surf is None or _shake_surf.get_size() != (WIDTH, HEIGHT):
            _shake_surf = pygame.Surface((WIDTH, HEIGHT))
        target = _shake_surf    # render offscreen, present with offset
    else:
        target = surf

    # ── Smoke particles ──────────────────────────────────────
    if _smoke is not None:
        _smoke.update(dt, emitting=bool(s.get("smoke")))

    # ── Background ────────────────────────────────────────────
    bg_path = s.get("bg")
    if bg_path:
        bg = _get_bg(bg_path)
        target.blit(bg, (0, 0))
        _last_bg_surf = bg
    else:
        target.fill(config.STORY_BG_COLOR)

    # Dark overlay or coloured tint (for feedback slides)
    tint = s.get("tint")
    if tint:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(tint)
        target.blit(overlay, (0, 0))
    elif s.get("dark"):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        target.blit(overlay, (0, 0))

    _chars.update(dt)

    # ── Title slide ───────────────────────────────────────────
    if stype == "title":
        logo_path = s.get("logo")
        if logo_path:
            logo = _get_logo(logo_path, int(WIDTH * 0.50))
            surf.blit(logo, logo.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        _finish_fade_in(surf, dt)
        return

    # ── Transition slide — kick off the black fade ────────────
    if stype == "transition" and _fade_phase is None:
        _fade_phase = "out"
        _fade_alpha = 0
        _fade_timer = 0.0

    if _fade_phase in ("out", "hold"):
        _apply_fade(surf, dt)
        return

    # ── Character-only scene ─────────────────────────────────
    if stype == "scene":
        if _chars is not None:
            _chars.draw(target)
        if _smoke is not None:
            _smoke.draw(target)
        _draw_day_counter(target)
        _draw_water_bar(target)
        _blit_shaken(surf)
        # The fade-in has to be driven on this path too: a "scene" slide
        # can sit directly after a "transition" slide (S2P26 does). Leaving
        # it out keeps _fade_phase stuck on "in" forever, and handle_tap()
        # blocks every tap while a fade is running — the panel just sits
        # there looking frozen and never reaches S2P27.
        _finish_fade_in(surf, dt)
        return
    
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
    _draw_day_counter(target)

    # ── Dialogue box ──────────────────────────────────────────
    _draw_dbox(target)

    # Characters are drawn AFTER the dialogue box so that
    # characters appear in front of it.
    _chars.draw(target)

    # Smoke floats in front of the characters but behind UI.
    if _smoke is not None:
        _smoke.draw(target)

    # ── Choice image buttons (only on choice slide) ───────────

    # ── Choice image buttons (only on choice slide) ───────────
    if stype == "choice":
        _draw_choice_image_buttons(target)

    # ── Water meter (bottom of the planter) ────────────────────
    _draw_water_bar(target)

    # ── Camera shake: present the frame with the offset ───────
    _blit_shaken(surf)

    # ── Fade-in overlay (drawn on top of fully-rendered next slide) ──
    if _fade_phase == "in":
        _apply_fade(surf, dt)

    # ── Popups ────────────────────────────────────────────────
    if _engine and _engine.popup_open == "scan":
        scan_popup.draw(surf)
    elif _engine and _engine.popup_open == "image":
        image_popup.draw(surf)


def _finish_fade_in(surf, dt):
    """Blit (and advance) the black fade-in overlay for render paths that
    return early (title / scene slides).

    _apply_fade() drives "out" and "hold" before those paths are even
    reached, but the "in" phase is blitted at the very end of the normal
    dialogue path. A slide rendered by an early-return path would never
    clear it, leaving _fade_phase on "in" — which permanently blocks
    input in handle_tap().
    """
    if _fade_phase == "in":
        _apply_fade(surf, dt)


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
    s = _engine.slide
    stype = s["type"]
    pad = int(WIDTH * _DBOX_PAD_FRAC)

    r = min(18, _dbox.width // 6, _dbox.height // 4)

    fill = _QBOX_FILL if stype == "choice" else _DBOX_FILL
    border = _QBOX_BORDER if stype == "choice" else _DBOX_BORDER

    pygame.draw.rect(
        surf,
        fill,
        _dbox,
        border_radius=r
    )

    pygame.draw.rect(
        surf,
        border,
        _dbox,
        width=_BORDER_W,
        border_radius=r
    )

    body_font = (
        _dialogue_font
        if _dialogue_font is not None
        else _font_body
    )

    if stype in ("dialogue", "end", "feedback"):
        visible = _typing_text[:int(_typing_chars)]

        _draw_wrapped(
            surf,
            body_font,
            visible,
            _DBOX_TEXT,
            _dbox.x + pad,
            _dbox.y + pad,
            _dbox.width - pad * 2
        )

        if _typing_done:
            hint = _dialogue_hint_font().render(
                "tap screen to continue...",
                True,
                _HINT_COLOR
            )

            hint.set_alpha(140)

            surf.blit(
                hint,
                hint.get_rect(
                    bottomright=(
                        _dbox.right - pad - _BORDER_W,
                        _dbox.bottom - pad - _BORDER_W
                    )
                )
            )

    elif stype == "choice":
        q = (
            s.get("retry_question", s["question"])
            if _engine.is_retry
            else s["question"]
        )

        _draw_wrapped(
            surf,
            body_font,
            q,
            _QBOX_TEXT,
            _dbox.x + pad,
            _dbox.y + pad,
            _dbox.width - pad * 2
        )

    elif stype == "scan":
        _draw_wrapped(
            surf,
            body_font,
            s.get("dialogue", ""),
            _DBOX_TEXT,
            _dbox.x + pad,
            _dbox.y + pad,
            _dbox.width - pad * 2
        )

        hint = _dialogue_hint_font().render(
            "Tap to scan card  >>",
            True,
            _HINT_COLOR
        )

        surf.blit(
            hint,
            hint.get_rect(
                bottomright=(
                    _dbox.right - pad,
                    _dbox.bottom - int(pad * 0.4)
                )
            )
        )


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

def _draw_wrapped(
    surf,
    font,
    text,
    color,
    x,
    y,
    max_width
):
    """Draw text wrapped to max_width."""
    if not text:
        return

    max_width = max(1, int(max_width))

    words = text.split()
    line = ""
    line_h = font.get_linesize()
    current_y = y

    for word in words:
        test = (
            line + " " + word
        ).strip()

        if font.size(test)[0] <= max_width:
            line = test
            continue

        if line:
            surf.blit(
                font.render(
                    line,
                    True,
                    color
                ),
                (
                    x,
                    current_y
                )
            )

            current_y += line_h

        # Start the next line with this word.
        line = word

    if line:
        surf.blit(
            font.render(
                line,
                True,
                color
            ),
            (
                x,
                current_y
            )
        )
