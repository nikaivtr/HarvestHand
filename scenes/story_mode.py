# ============================================================
#  Story Mode Scene
#  Ties together: StoryEngine, CharacterLayer, scan popup, image popup.
#  You should NOT need to edit this file when adding chapter content.
# ============================================================

import random

import pygame
import config
import game_state
import player_data
import data.chapters as chapters_data
from cardscan import registry as card_registry
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
_memory_game_played = False
_ingredient_puzzle_played = False
_whack_a_pest_played = False
_tomato_seed_extraction_played = False
_end_buttons   = {}     # {"repeat": Rect, "menu": Rect, "next": Rect}
_last_bg_surf  = None   # cached last background for the overlay backdrop

# ── Asset caches ──────────────────────────────────────────────
_bg_cache         : dict = {}
_logo_cache       : dict = {}
_overlay_cache    : dict = {}
_overlay_aspect   : dict = {}
_overlay_inset    : dict = {}
_choice_img_cache : dict = {}
_gauge_icon_cache : dict = {}
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
_pending_water_scan = False
_gauge_remaining = {}
_gauge_totals = {}
_gauge_visible = {}
_GAUGE_ORDER = ("water", "fertilizer", "pests", "weeds")
_GAUGE_LABELS = {
    "water": "Water",
    "fertilizer": "Fertilizer",
    "pests": "Pest control",
    "weeds": "Weed removal",
}
_GAUGE_COLORS = {
    "water": (70, 140, 200),
    "fertilizer": (90, 160, 70),
    "pests": (200, 80, 65),
    "weeds": (140, 180, 65),
}
_GAUGE_ICON_PATHS = {
    "water": "ui/gauges/water.png",
    "fertilizer": "ui/gauges/fertilizer.png",
    "pests": "ui/gauges/pests.png",
    "weeds": "ui/gauges/weeds.png",
}
_ACTION_GAUGE_BY_SLUG = {
    "water": "water",
    "fertilizer": "fertilizer",
    "organic_fertilizer": "fertilizer",
    "chemical_fertilizer": "fertilizer",
    "weed": "weeds",
    "pesticide": "pests",
    "natural_pesticide": "pests",
    "chemical_pesticide": "pests",
}
_RANDOM_ACTION_CARDS = {
    "water": ("water", "background/Action_Challenge-Water.png"),
    "fertilizer": ("organic_fertilizer", "organicfertilizercard.png"),
    "pests": ("natural_pesticide", "naturalpesticidecard.png"),
    "weeds": ("weed", "weedremovalcard.png"),
}
_RANDOM_CHALLENGE_MIN_DAYS = 7
_RANDOM_CHALLENGE_MAX_DAYS = 14
_RANDOM_CHALLENGE_START_FRACTION = 0.25
_RANDOM_CHALLENGE_END_FRACTION = 0.75
_RANDOM_CHALLENGE_FIRST_WINDOW_FRACTION = 0.4
_ANALYSIS_CHALLENGE_PROBABILITY = 0.5

_WATER_DRYING_DAYS            = 7
_WATER_DECAY_PER_DAY          = 0.28 / _WATER_DRYING_DAYS
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

# ── Action challenge (temporary stand-in for the real card scan) ──
# Slide type "action_challenge": the instruction art is drawn over the
# slide background, and the player taps one of two squares. This is a
# placeholder so the scenes can be finished first; the camera-based
# cardscan package replaces it later.
_ACTION_BLUE  = ( 62, 132, 226)
_ACTION_RED   = (198,  74,  66)
_ACTION_OK    = ( 86, 176,  96)
_ACTION_EDGE  = (253, 241, 208)
_ACTION_WRONG_FACE = "I-click naman ang BLUE na square."
_ACTION_OK_FACE     = "Tama! Tama ang card na i-scan."
_ACTION_HINT_IDLE   = (253, 241, 208)

_ACTION_SOLVE_DELAY = 0.9   # seconds the success banner stays up
_ACTION_WRONG_TIME  = 0.45  # seconds the red square flashes
_ACTION_SOLVED_T    = 0.0
_ACTION_WRONG_T     = 0.0
_CHALLENGE_DURATION = 30.0
_challenge_timer_slide = None
_challenge_time_left = 0.0
_challenge_timeout_feedback = 0.0

# Layout, as fractions of the screen, so it scales to any resolution.
_ACTION_OVERLAY_W_FRAC = 0.60
_ACTION_OVERLAY_TOP_FRAC = 0.05
_ACTION_SQUARE_FRAC     = 0.17   # side length, of screen height
_ACTION_SQUARE_GAP_FRAC = 0.06   # gap between the two, of screen width
_ACTION_SQUARE_TOP_PAD  = 0.06   # gap under the instruction art
_ACTION_HINT_GAP_FRAC   = 0.045
_font_action = None

# ── Narration overlay ──────────────────────────────────────────
# Slide type "narration_overlay": a carved wooden board is laid over
# the slide background and a passage of narration is written on it.
# Used for the story beats where nobody is speaking (a time skip,
# a montage), so it needs neither a speaker nor a dialogue box.
_NARR_TEXT   = (253, 241, 208)   # cream paint on the board
_NARR_SHADOW = ( 44,  24,   8)   # dark offset shadow, as in level_select
_NARR_HINT   = (222, 200, 156)

# The board is a fixed 1.78:1 asset. Its height drives the size so
# the art keeps its own proportions, and the other dimension is
# re-clamped afterwards so the board can never run off the screen.
# The board sits dead centre, so the passage and the board read as
# one centred block.
_NARR_BOARD_H_FRAC     = 0.66
_NARR_BOARD_MAX_W_FRAC = 0.86
_NARR_BOARD_MAX_H_FRAC = 0.86

# The carved frame eats into each edge, so the text only ever goes
# inside the recessed panel. Fractions measured off woodbg.png,
# the same board the level-select signposts use.
_NARR_PANEL = (0.090, 0.150, 0.910, 0.850)

# Narration is read, not spoken aloud, so it gets noticeably bigger
# type than the dialogue box. The fitter starts at _NARR_FONT_MAX
# and only shrinks when a passage is long enough to need it.
_NARR_FONT_MAX_FRAC = 0.055
_NARR_FONT_MIN_FRAC = 0.030

# Free strip kept at the bottom of the panel for the hint line.
_NARR_HINT_RESERVE_FRAC = 0.02

# ── Choice wooden board ("dbox") ─────────────────────────────────
# A choice may carry a wooden board of its own and print its label
# inside the recessed panel. Only needed when the answer is a full
# sentence: the card art plus the single label line underneath it has
# room for a word or two, not a paragraph. Choices without a "dbox"
# keep the original panel-and-caption treatment untouched.
_CHOICE_DBOX_FONT_MAX_FRAC = 0.032
_CHOICE_DBOX_FONT_MIN_FRAC = 0.016


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

def _action_kind(slide):
    """Return the card identity for an action challenge, if it is known."""
    card = card_registry.resolve(slide.get("card", ""))
    if card is not None:
        return card.slug

    overlay = slide.get("overlay", "").replace("\\", "/").rsplit("/", 1)[-1].lower()
    if "analyze" in overlay or "analys" in overlay:
        return "analyze"
    if "water" in overlay:
        return "water"
    if "fertilizer" in overlay:
        return "fertilizer"
    if "weed" in overlay:
        return "weed"
    if "pesticide" in overlay or "pest" in overlay:
        return "pesticide"
    return None


def _random_action_pair(day, index, gauge, include_analysis=False, background=None):
    slug, overlay = _RANDOM_ACTION_CARDS[gauge]
    card = card_registry.get(slug)
    if card is None:
        raise ValueError(f"Random challenge card is not registered: {slug}")
    event_id = f"random_care_{day}_{index}"
    slides = []
    if include_analysis:
        research_messages = {
            "water": (
                "Napansin kong natutuyo ang lupa. Suriin muna natin ang mga palatandaan "
                "at i-scan ang Analyze Card para malaman kung anong pangangalaga ang kailangan."
            ),
            "fertilizer": (
                "Maputla ang mga dahon at tila kulang sa sustansya ang lupa. Suriin natin "
                "ang pananim gamit ang Analyze Card bago pumili ng pataba."
            ),
            "pests": (
                "May mga kagat at kakaibang marka sa mga dahon. Suriin muna natin ang "
                "mga palatandaan gamit ang Analyze Card bago kumilos."
            ),
            "weeds": (
                "May tumutubong damo sa paligid ng pananim. Suriin natin ang epekto nito "
                "gamit ang Analyze Card bago kumilos."
            ),
        }
        slides.extend((
            {
                "id": f"{event_id}_research",
                "type": "dialogue",
                "day": day,
                "bg": background or "background/scenebg_default.png",
                "chars": {"lola": {"side": "left", "expression": "worried", "flip": False}},
                "lines": [("lola", research_messages[gauge])],
                "random_research": True,
            },
            {
                "id": f"{event_id}_analyze",
                "type": "action_challenge",
                "day": day,
                "overlay": "analyzecard.png",
                "card": "Analyze Card",
                "question": "Analyze the crop to find the care action it needs.",
                "random_challenge": True,
            },
        ))
    slides.append({
        "id": f"{event_id}_action",
        "type": "action_challenge",
        "day": day,
        "overlay": overlay,
        "card": card.display,
        "question": f"Use the {card.name} to care for the crop.",
        "random_challenge": True,
    })
    return slides


def _place_chapter_characters(chapter):
    """Apply Chapter 8's Lucas placement rule to a per-playthrough copy."""
    slides = list(chapter.get("slides", ()))
    if chapter.get("id") != "ch08":
        return slides

    placed = []
    for index, original in enumerate(slides):
        chars = original.get("chars", {})
        lucas = chars.get("lucas")
        if not isinstance(lucas, dict):
            placed.append(original)
            continue

        nearby_characters = set(chars)
        if index:
            previous = slides[index - 1]
            nearby_characters.update(previous.get("chars", {}))
            nearby_characters.update(
                speaker for speaker, _ in previous.get("lines", ())
            )
        current_text = " ".join(text for _, text in original.get("lines", ())).lower()
        faces_opponent = any(
            any(name in actor.lower() for actor in nearby_characters)
            or name in current_text
            for name in ("chef", "baron", "kapitan")
        )

        slide = dict(original)
        slide_chars = dict(chars)
        lucas = dict(lucas)
        lucas["side"] = "left" if faces_opponent else "right"
        lucas["flip"] = faces_opponent
        slide_chars["lucas"] = lucas
        slide["chars"] = slide_chars
        placed.append(slide)
    return placed


def _prepare_chapter(chapter):
    """Build per-playthrough care challenges without mutating chapter modules."""
    prepared = dict(chapter)
    slides = _place_chapter_characters(chapter)
    crop = card_registry.crop_card(chapter.get("crop", ""))
    if crop is None:
        raise ValueError(f"No crop card is registered for chapter crop {chapter.get('crop')!r}")

    crop_needs = {
        "water": max(0, int(crop.details.get("water", 0))),
        "fertilizer": max(0, int(crop.details.get("fertilizer", 0))),
        "weeds": max(0, int(crop.details.get("weeds", 0))),
        "pests": max(0, int(crop.details.get("pests", 0))),
    }
    fixed_challenges = {gauge: 0 for gauge in _GAUGE_ORDER}
    for slide in slides:
        if slide.get("type") == "action_challenge":
            gauge = _ACTION_GAUGE_BY_SLUG.get(_action_kind(slide))
            if gauge is not None:
                fixed_challenges[gauge] += 1

    day_values = [slide["day"] for slide in slides if isinstance(slide.get("day"), int)]
    last_day = max(day_values, default=int(crop.details.get("days", 0)))
    total_days = max(
        int(chapter.get("total_days") or crop.details.get("days") or last_day),
        last_day,
    )
    candidates = [gauge for gauge in _GAUGE_ORDER if crop_needs[gauge] > 0]
    scheduled = []
    middle_start = max(
        _RANDOM_CHALLENGE_MIN_DAYS,
        int(total_days * _RANDOM_CHALLENGE_START_FRACTION + 0.999),
    )
    middle_end = min(
        last_day,
        int(total_days * _RANDOM_CHALLENGE_END_FRACTION),
    )
    if candidates and middle_start <= middle_end:
        first_event_latest = min(
            middle_end,
            max(
                middle_start,
                int(total_days * _RANDOM_CHALLENGE_FIRST_WINDOW_FRACTION + 0.999),
            ),
        )
        due_day = random.randint(middle_start, first_event_latest)
        while due_day <= middle_end:
            gauge = random.choices(
                candidates,
                weights=[3 if candidate == "water" else 1 for candidate in candidates],
                k=1,
            )[0]
            scheduled.append((due_day, gauge))
            due_day += random.randint(_RANDOM_CHALLENGE_MIN_DAYS, _RANDOM_CHALLENGE_MAX_DAYS)
    analyze_index = None
    if scheduled and random.random() < _ANALYSIS_CHALLENGE_PROBABILITY:
        analyze_index = random.randrange(len(scheduled))

    scheduled_index = 0
    prepared_slides = []
    current_day = 0
    random_counts = {gauge: 0 for gauge in _GAUGE_ORDER}
    for slide in slides:
        slide_day = slide.get("day", current_day)
        while scheduled_index < len(scheduled) and scheduled[scheduled_index][0] <= slide_day:
            due_day, gauge = scheduled[scheduled_index]
            prepared_slides.extend(_random_action_pair(
                due_day,
                scheduled_index + 1,
                gauge,
                include_analysis=(scheduled_index == analyze_index),
                background=slide.get("bg"),
            ))
            random_counts[gauge] += 1
            scheduled_index += 1
        prepared_slides.append(slide)
        if isinstance(slide.get("day"), int):
            current_day = slide["day"]

    totals = {
        gauge: (
            0 if gauge == "water"
            else max(crop_needs[gauge], fixed_challenges[gauge]) + random_counts[gauge]
        )
        for gauge in _GAUGE_ORDER
    }
    prepared["slides"] = prepared_slides
    return prepared, totals


def _load_chapter():
    global _engine, _chars, _DAY_TOTAL, _chapter_done, _last_bg_surf
    global _water_level, _crop_name, _pending_water_scan, _challenge_timer_slide
    global _gauge_remaining, _gauge_totals, _gauge_visible
    global _memory_game_played, _ingredient_puzzle_played, _whack_a_pest_played
    global _tomato_seed_extraction_played
    chapter, _gauge_totals = _prepare_chapter(
        chapters_data.load(game_state.selected_chapter)
    )
    _gauge_remaining = dict(_gauge_totals)
    _gauge_visible = {gauge: False for gauge in _GAUGE_ORDER}
    _DAY_TOTAL  = chapter.get("total_days", 30)
    game_state.day = 0
    _chars      = CharacterLayer(WIDTH, HEIGHT)
    _engine     = StoryEngine(chapter, on_chapter_end=_on_chapter_end)
    player_data.begin_chapter(game_state.selected_chapter)
    _chapter_done = False
    _memory_game_played = False
    _ingredient_puzzle_played = False
    _whack_a_pest_played = False
    _tomato_seed_extraction_played = False
    _last_bg_surf = None
    _water_level  = 1.0
    _crop_name    = chapter.get("crop", "")
    _pending_water_scan = False
    _challenge_timer_slide = None
    _reset_typing()
    _sync_chars()


def _sync_chars():
    if _engine is None or _chars is None:
        return
    s = _engine.slide
    if "day" in s:
        elapsed_days = max(0, s["day"] - game_state.day)
        if elapsed_days:
            _decay_water(elapsed_days)
        game_state.day = s["day"]
    _chars.set_slide(
        s.get("chars", {}),
        _engine.active_char,
        dim_others=bool(s.get("dim_inactive", False)),
    )
    _start_shake_if_flagged()

    # Fresh panel, fresh challenge state: a solved or flashing square from
    # a previous panel must never carry over.
    if s.get("type") != "action_challenge":
        _reset_action()
    _reset_challenge_timer()

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
    result = player_data.complete_chapter()
    if result is not None:
        game_state.score[result["chapter"]] = result["score"]
    _chapter_done = True
    _chars = None
    _compute_end_buttons()


def _launch_memory_game():
    global _chars, _memory_game_played
    from scenes import memory_game

    _memory_game_played = True
    _chars = None
    memory_game.set_success_action(
        _continue_story_after_memory_game,
        "CONTINUE STORY",
    )
    memory_game.start()
    _go_to_scene("memory_game")


def _continue_story_after_memory_game():
    resume_after_memory_game()
    _go_to_scene("story_mode")


def _launch_ingredient_puzzle():
    global _chars, _ingredient_puzzle_played
    from minigames.ingredient_puzzle import scene as ingredient_puzzle

    _ingredient_puzzle_played = True
    _chars = None
    ingredient_puzzle.set_success_action(
        _continue_story_after_ingredient_puzzle,
        "CONTINUE STORY",
    )
    ingredient_puzzle.start()
    _go_to_scene("ingredient_puzzle")


def _continue_story_after_ingredient_puzzle():
    resume_after_ingredient_puzzle()
    _go_to_scene("story_mode")


def _launch_whack_a_pest():
    global _chars, _whack_a_pest_played
    from minigames import whack_a_pest

    _whack_a_pest_played = True
    _chars = None
    whack_a_pest.set_return_callback(
        _return_from_whack_a_pest,
        "CONTINUE STORY",
    )
    whack_a_pest.start()
    _go_to_scene("whack_a_pest")


def _return_from_whack_a_pest(_scene_name):
    resume_after_whack_a_pest()
    _go_to_scene("story_mode")


def resume_after_whack_a_pest():
    global _chars, _chapter_done, _last_ticks
    if _engine is None:
        return
    _chars = CharacterLayer(WIDTH, HEIGHT)
    _chapter_done = False
    _last_ticks = pygame.time.get_ticks()


def _launch_tomato_seed_extraction():
    global _chars, _tomato_seed_extraction_played
    from minigames import tomato_seed_extraction

    _tomato_seed_extraction_played = True
    _chars = None
    tomato_seed_extraction.set_success_action(
        _return_from_tomato_seed_extraction,
        "CONTINUE STORY",
    )
    tomato_seed_extraction.set_return_callback(
        _return_from_tomato_seed_extraction,
        "CONTINUE STORY",
    )
    tomato_seed_extraction.start()
    _go_to_scene("tomato_seed_extraction")


def _return_from_tomato_seed_extraction(_scene_name):
    resume_after_tomato_seed_extraction()
    _go_to_scene("story_mode")


def resume_after_tomato_seed_extraction():
    global _chars, _chapter_done, _last_ticks
    if _engine is None:
        return
    _chars = CharacterLayer(WIDTH, HEIGHT)
    _chapter_done = False
    _last_ticks = pygame.time.get_ticks()
    _reset_typing()
    _sync_chars()


def resume_after_ingredient_puzzle():
    global _chars, _chapter_done, _last_ticks
    if _engine is None:
        return
    _chars = CharacterLayer(WIDTH, HEIGHT)
    _chapter_done = False
    _last_ticks = pygame.time.get_ticks()
    _reset_typing()
    _sync_chars()


def resume_after_memory_game():
    global _chars, _chapter_done, _last_ticks
    if _engine is None:
        return
    _chars = CharacterLayer(WIDTH, HEIGHT)
    _chapter_done = False
    _last_ticks = pygame.time.get_ticks()
    _reset_typing()
    _sync_chars()


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


def _get_overlay(path: str, target_w: int):
    """An instruction image drawn on top of a slide's background.

    Returns (surface, target_height). The width is honoured exactly and
    the height follows the art's own aspect ratio, so the picture is
    never stretched.
    """
    key = (path, target_w)
    if key not in _overlay_cache:
        raw   = pygame.image.load(config.IMG_DIR + path).convert_alpha()
        ratio = target_w / raw.get_width()
        h     = max(1, int(raw.get_height() * ratio))
        _overlay_cache[key] = pygame.transform.smoothscale(raw, (target_w, h))
    surf = _overlay_cache[key]
    return surf, surf.get_height()


def _get_overlay_aspect(path: str) -> float:
    """Native width/height of an overlay image, for sizing it by height.

    _get_overlay() sizes by width, so a board laid out from its height
    first needs the raw ratio to work out what that width would be.
    """
    if path not in _overlay_aspect:
        raw = pygame.image.load(config.IMG_DIR + path)
        _overlay_aspect[path] = raw.get_width() / max(1, raw.get_height())
    return _overlay_aspect[path]


def _alpha_bbox(surf: pygame.Surface):
    """Bounding rect of the non-transparent pixels of `surf`.

    Returns None when the surface is fully transparent. Uses the mask
    module's C implementation rather than looping over pixels in
    Python, since this runs on a 1366x768 board asset.
    """
    rects = pygame.mask.from_surface(surf, 8).get_bounding_rects()
    if not rects:
        return None
    out = pygame.Rect(rects[0])
    for r in rects[1:]:
        out = out.union(r)
    return out


def _get_overlay_inset(path: str):
    """Transparent border of an overlay, as (left, top, right, bottom)
    fractions of the image.

    The board art is not edge-to-edge: woodbg.png has a wider margin
    under the plank than above it, so centring the image rectangle
    leaves the wood the player actually sees a few pixels high. The
    border is measured once per path and returned as fractions so the
    caller can keep the visible plank centred at any size.
    """
    if path not in _overlay_inset:
        raw = pygame.image.load(config.IMG_DIR + path).convert_alpha()
        iw, ih = max(1, raw.get_width()), max(1, raw.get_height())
        rect = _alpha_bbox(raw)
        if rect is None or rect.width == 0 or rect.height == 0:
            _overlay_inset[path] = (0.0, 0.0, 0.0, 0.0)
        else:
            _overlay_inset[path] = (
                rect.left          / iw,
                rect.top           / ih,
                (iw - rect.right)  / iw,
                (ih - rect.bottom) / ih,
            )
    return _overlay_inset[path]


def _get_choice_img(path: str, max_w: int, max_h: int) -> pygame.Surface:
    key = (path, max_w, max_h)
    if key not in _choice_img_cache:
        raw     = pygame.image.load(config.IMG_DIR + path).convert_alpha()
        bounds  = _alpha_bbox(raw)
        if bounds is not None and bounds != raw.get_rect():
            raw = raw.subsurface(bounds).copy()
        elif bounds == raw.get_rect():
            corners = (
                raw.get_at((0, 0)),
                raw.get_at((raw.get_width() - 1, 0)),
                raw.get_at((0, raw.get_height() - 1)),
                raw.get_at((raw.get_width() - 1, raw.get_height() - 1)),
            )
            if all(
                pixel.a == 255 and pixel.r >= 245 and pixel.g >= 245 and pixel.b >= 245
                for pixel in corners
            ):
                # Remove only the white background connected to the canvas edge.
                white = pygame.mask.from_threshold(
                    raw, (255, 255, 255, 255), (12, 12, 12, 255)
                )
                background = pygame.Mask(raw.get_size())
                for point in (
                    (0, 0),
                    (raw.get_width() - 1, 0),
                    (0, raw.get_height() - 1),
                    (raw.get_width() - 1, raw.get_height() - 1),
                ):
                    if white.get_at(point):
                        background.draw(white.connected_component(point), (0, 0))

                foreground = pygame.mask.from_surface(raw, 8)
                foreground.erase(background, (0, 0))
                alpha = foreground.to_surface(
                    setcolor=(255, 255, 255, 255),
                    unsetcolor=(255, 255, 255, 0),
                )
                raw.blit(alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                bounds = _alpha_bbox(raw)
                if bounds is not None and bounds != raw.get_rect():
                    raw = raw.subsurface(bounds).copy()
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
    return max(len(_wrap_lines(text, max_px, font)), 1)


def _wrap_lines(text: str, max_px: int, font=None) -> list[str]:
    """Split text into the visual lines it occupies at this width.

    Single source of truth for the wrap: the line count used when
    fitting a font, the narration board and _draw_wrapped() all agree
    on where the breaks fall.
    """
    if font is None:
        font = _font_body

    max_px = max(1, int(max_px))

    lines = []
    line  = ""

    for word in text.split():
        test = (line + " " + word).strip()

        if font.size(test)[0] <= max_px:
            line = test
        else:
            if line:
                lines.append(line)
            # A single word wider than the box keeps its own line
            # rather than being broken mid-word.
            line = word

    if line:
        lines.append(line)

    return lines


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

    A slide can override the automatic choice with
    "dbox_side": "left" or "right" (see below).

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
    # Explicit side override from the slide data.
    #
    # Some backgrounds have their character painted into the art
    # (e.g. S2P51's Lucas watering the bed) instead of placed as
    # a sprite, so there is no "chars" entry for the rules above
    # to measure and the box lands centred — on top of the
    # artwork. "dbox_side" lets those slides state where the text
    # should go. The width chosen above is kept; only the position
    # is re-anchored, so the font sizing does not change.
    # ---------------------------------------------------------
    forced_side = _engine.slide.get("dbox_side")
    if forced_side in ("left", "right"):
        width = box_right - box_left
        if forced_side == "left":
            box_left = edge_margin
            box_right = box_left + width
        else:
            box_right = WIDTH - edge_margin
            box_left = box_right - width

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
#  Action challenge  (temporary stand-in for the real card scan)
# ─────────────────────────────────────────────────────────────

def _action_fonts():
    """Lazily built fonts for the challenge, so none are made per frame."""
    global _font_action
    if _font_action is None:
        _font_action = (_make_font(0.024), _make_font(0.038))
    return _font_action


def _reset_action():
    global _ACTION_SOLVED_T, _ACTION_WRONG_T
    _ACTION_SOLVED_T = 0.0
    _ACTION_WRONG_T  = 0.0


def _reset_challenge_timer():
    global _challenge_timer_slide, _challenge_time_left, _challenge_timeout_feedback
    if _engine is None or not _engine.slide.get("timer"):
        _challenge_timer_slide = None
        _challenge_time_left = 0.0
        _challenge_timeout_feedback = 0.0
        return
    if _challenge_timer_slide != _engine.slide_idx:
        _challenge_timer_slide = _engine.slide_idx
        _challenge_time_left = _CHALLENGE_DURATION
        _challenge_timeout_feedback = 0.0


def _update_challenge_timer(dt):
    global _challenge_time_left, _challenge_timeout_feedback
    if _engine is None or not _engine.slide.get("timer"):
        return
    if _challenge_timeout_feedback > 0.0:
        _challenge_timeout_feedback = max(0.0, _challenge_timeout_feedback - dt)
        if _challenge_timeout_feedback == 0.0:
            _challenge_time_left = _CHALLENGE_DURATION
        return
    _challenge_time_left = max(0.0, _challenge_time_left - dt)
    if _challenge_time_left == 0.0:
        player_data.record_mistake()
        _challenge_timeout_feedback = 1.5
        _reset_action()


def _draw_challenge_timer(surf):
    if _engine is None or not _engine.slide.get("timer"):
        return
    if _challenge_timeout_feedback > 0.0:
        text = "Time's up! Try again"
        color = (220, 90, 75)
    else:
        text = f"Time: {max(0, int(_challenge_time_left + 0.999))}s"
        color = _DAY_TEXT
    label = _font_hint.render(text, True, color)
    pad_x = int(WIDTH * 0.016)
    pad_y = int(HEIGHT * 0.009)
    exit_rect = _chapter_exit_button_rect()
    rect = pygame.Rect(
        exit_rect.left - label.get_width() - pad_x * 2 - int(WIDTH * 0.018),
        int(HEIGHT * 0.020),
        label.get_width() + pad_x * 2,
        label.get_height() + pad_y * 2,
    )
    pygame.draw.rect(surf, _DAY_FILL, rect, border_radius=rect.height // 2)
    pygame.draw.rect(surf, _DAY_BORDER, rect, width=2, border_radius=rect.height // 2)
    surf.blit(label, label.get_rect(center=rect.center))


def _action_layout():
    """Rects for the instruction art, the two squares and the hint line.

    Recomputed from the screen size every call, so it follows the
    resolution exactly like the rest of the scene.
    """
    lay = {"overlay": None, "blue": None, "red": None, "hint_y": HEIGHT}
    if _engine is None:
        return lay
    path = _engine.slide.get("overlay")
    if not path:
        return lay

    img, h = _get_overlay(path, int(WIDTH * _ACTION_OVERLAY_W_FRAC))
    r = pygame.Rect(0, 0, img.get_width(), h)
    r.midtop = (WIDTH // 2, int(HEIGHT * _ACTION_OVERLAY_TOP_FRAC))
    lay["overlay"] = (img, r)

    side = int(HEIGHT * _ACTION_SQUARE_FRAC)
    top  = r.bottom + int(HEIGHT * _ACTION_SQUARE_TOP_PAD)
    # Never let the squares run off the bottom, whatever the aspect ratio.
    floor = int(HEIGHT * 0.88)
    if top + side > floor:
        side = max(24, floor - top)
    gap  = int(WIDTH * _ACTION_SQUARE_GAP_FRAC)
    mid  = WIDTH // 2
    lay["blue"] = pygame.Rect(mid - gap // 2 - side, top, side, side)
    lay["red"]  = pygame.Rect(mid + gap // 2,      top, side, side)
    lay["hint_y"] = top + side + int(HEIGHT * _ACTION_HINT_GAP_FRAC)
    return lay


def _handle_action_tap(px, py):
    """Blue square -> solved. Red square -> flash and let them try again.

    Tapping anywhere else does nothing: the player has to pick a square,
    so the panel cannot be skipped past.
    """
    global _ACTION_SOLVED_T, _ACTION_WRONG_T, _water_level

    if _ACTION_SOLVED_T > 0:
        return                       # already solved, waiting to advance

    lay = _action_layout()
    blue, red = lay["blue"], lay["red"]
    if blue is not None and blue.collidepoint(px, py):
        player_data.record_challenge_success(
            _challenge_time_left if _engine.slide.get("timer") else 0
        )
        action = _action_kind(_engine.slide)
        gauge = _ACTION_GAUGE_BY_SLUG.get(action)
        if gauge is not None:
            _gauge_visible[gauge] = True
            if gauge != "water":
                _gauge_remaining[gauge] = max(0, _gauge_remaining[gauge] - 1)
        if gauge == "water":
            _water_level = 1.0
        _ACTION_SOLVED_T = _ACTION_SOLVE_DELAY
        return
    if red is not None and red.collidepoint(px, py):
        player_data.record_mistake()
        _ACTION_WRONG_T = _ACTION_WRONG_TIME
        return


def _draw_action_square(surf, rect, color, wobble_t=0.0, solved=False):
    """One pickable square, with a cream frame like the rest of the UI."""
    r = rect
    if wobble_t > 0.0:
        # Quick shake, so a wrong pick registers even without reading text.
        amp = int(6 * (wobble_t / _ACTION_WRONG_TIME))
        r = r.move(int(amp * 2.0 * ((wobble_t * 18) % 2 - 1)), 0)

    pygame.draw.rect(surf, color, r, border_radius=int(r.width * 0.12))
    edge = _ACTION_OK if solved else _ACTION_EDGE
    pygame.draw.rect(surf, edge, r, width=4, border_radius=int(r.width * 0.12))
    # Inner highlight so the flat colour reads as a solid tile.
    inset = r.inflate(-int(r.width * 0.22), -int(r.height * 0.22))
    pygame.draw.rect(surf, edge, inset, width=2, border_radius=int(inset.width * 0.14))


def _draw_action(surf, dt):
    """Instruction art over the slide background, plus the two squares.

    Advances the story on its own once the solved banner has had its
    moment, so the player sees the confirmation before moving on.
    """
    global _ACTION_SOLVED_T, _ACTION_WRONG_T

    if _ACTION_SOLVED_T > 0.0:
        _ACTION_SOLVED_T = max(0.0, _ACTION_SOLVED_T - dt)
        if _ACTION_SOLVED_T <= 0.0 and _engine is not None and not _chapter_done:
            _engine.tap()
            if not _chapter_done:
                _sync_chars()
                if _engine.slide.get("type") == "whack_a_pest" and not _whack_a_pest_played:
                    _launch_whack_a_pest()
            return
    if _ACTION_WRONG_T > 0.0:
        _ACTION_WRONG_T = max(0.0, _ACTION_WRONG_T - dt)

    lay = _action_layout()
    if lay["overlay"] is None:
        return
    img, r = lay["overlay"]
    surf.blit(img, r.topleft)

    solved = _ACTION_SOLVED_T > 0.0
    _draw_action_square(surf, lay["blue"], _ACTION_BLUE, solved=solved)
    _draw_action_square(surf, lay["red"],  _ACTION_RED,
                        wobble_t=_ACTION_WRONG_T if not solved else 0.0,
                        solved=solved)

    hint_f, banner_f = _action_fonts()
    if solved:
        text, color, font = _ACTION_OK_FACE, _ACTION_OK, banner_f
    elif _ACTION_WRONG_T > 0.0:
        text, color, font = _ACTION_WRONG_FACE, _ACTION_RED, banner_f
    else:
        text, color, font = _ACTION_WRONG_FACE, _ACTION_HINT_IDLE, hint_f

    # The hint sits over the planter, which is dark and busy, so the text
    # gets a dark shadow behind it and stays legible on any background.
    label = font.render(text, True, color)
    shad  = font.render(text, True, (20, 10, 4))
    y     = int(min(lay["hint_y"], HEIGHT - label.get_height() - 4))
    surf.blit(shad,  shad.get_rect(midtop=(WIDTH // 2 + 2, y + 2)))
    surf.blit(label, label.get_rect(midtop=(WIDTH // 2, y)))


# ─────────────────────────────────────────────────────────────
#  Narration overlay
# ─────────────────────────────────────────────────────────────

def _narration_layout():
    """Board rect and the recessed panel inside it that holds the text.

    Recomputed from the screen size every call, so the board and its
    text scale together on any resolution.
    """
    lay = {"board": None, "text": None}
    if _engine is None:
        return lay

    path = _engine.slide.get("overlay")
    if not path:
        return lay

    aspect = _get_overlay_aspect(path)

    # Height drives the size so the board keeps its own proportions.
    h = int(HEIGHT * _NARR_BOARD_H_FRAC)
    w = int(h * aspect)

    # Clamp both dimensions to the screen, re-deriving the other from
    # the image's own proportions each time, so neither a narrow nor a
    # very tall window can push the board off screen.
    max_w = int(WIDTH  * _NARR_BOARD_MAX_W_FRAC)
    max_h = int(HEIGHT * _NARR_BOARD_MAX_H_FRAC)

    if w > max_w:
        w = max_w
        h = int(w / aspect)
    if h > max_h:
        h = max_h
        w = int(h * aspect)

    img, img_h = _get_overlay(path, w)
    board = pygame.Rect(0, 0, w, img_h)

    # Dead centre of the screen: the board is the focal point of the
    # slide, not a strip hung under the top edge.
    #
    # Centring the image rectangle is not quite enough — the board art
    # has a transparent margin, and woodbg.png's margin is not even
    # (wider under the plank than above it). Centre the *visible* wood
    # instead, so the plank the player sees sits on the true middle of
    # the screen at every resolution and the passage travels with it.
    pad_l, pad_t, pad_r, pad_b = _get_overlay_inset(path)
    vis = pygame.Rect(
        int(round(pad_l * w)),
        int(round(pad_t * img_h)),
        int(round((1.0 - pad_r - pad_l) * w)),
        int(round((1.0 - pad_b - pad_t) * img_h)),
    )
    board.topleft = (WIDTH // 2 - vis.centerx, HEIGHT // 2 - vis.centery)

    lay["board"] = (img, board)

    # The carved frame eats into each edge, so the text only ever
    # goes inside the recessed panel. The fractions are measured off
    # the visible plank rather than the image rectangle, so the text
    # keeps its place on the wood and travels with it as one block.
    l, t, r, b = _NARR_PANEL
    lay["text"] = pygame.Rect(
        board.left + vis.left   + int(l * vis.width),
        board.top  + vis.top    + int(t * vis.height),
        int((r - l) * vis.width),
        int((b - t) * vis.height),
    )

    return lay


def _fit_narration_font(text: str, max_w: int, max_h: int):
    """Largest font that lets the whole passage fit the board's panel.

    Returns (font, lines, text_height). Starts deliberately large —
    narration is read by kids, not scanned — and only shrinks when
    the passage is long enough to demand it.
    """
    max_w = max(1, int(max_w))
    max_h = max(1, int(max_h))

    floor_px = max(14, int(HEIGHT * _NARR_FONT_MIN_FRAC))
    size     = max(floor_px, int(HEIGHT * _NARR_FONT_MAX_FRAC))

    while True:
        font  = _make_font_px(size)
        lines = _wrap_lines(text, max_w, font)
        height = len(lines) * font.get_linesize()

        if height <= max_h or size <= floor_px:
            return font, lines, height

        size -= 1


def _draw_narration(surf):
    """Wooden board over the slide background, carrying a narration.

    The passage is shown in full rather than typed out letter by
    letter: it is a block of prose to read, and having to wait for a
    typewriter to catch up would work against that.
    """
    lay = _narration_layout()
    if lay["board"] is None:
        return

    img, board = lay["board"]
    surf.blit(img, board.topleft)

    text = _engine.slide.get("narration", "")
    if not text:
        return

    inner = lay["text"]

    # Leave the hint line its own strip at the bottom of the panel.
    hint_f    = _dialogue_hint_font()
    reserve   = hint_f.get_linesize() + int(HEIGHT * _NARR_HINT_RESERVE_FRAC)
    font, lines, text_h = _fit_narration_font(
        text,
        inner.width,
        inner.height - reserve,
    )

    line_h = font.get_linesize()

    # The board is textured, so a dark offset shadow under the cream
    # letters keeps every line readable at a glance.
    off = max(1, font.get_height() // 22)

    # The passage and its hint are centred together as a single block,
    # so the whole thing sits on the board's centre line instead of
    # the text alone with the hint dangling underneath it.
    gap     = off * 2
    hint_h  = hint_f.get_linesize()
    block_h = text_h + gap + hint_h
    y       = inner.centery - block_h // 2

    for line in lines:
        shad  = font.render(line, True, _NARR_SHADOW)
        body  = font.render(line, True, _NARR_TEXT)
        rect  = body.get_rect(midtop=(inner.centerx, y))
        surf.blit(shad, rect.move(off, off))
        surf.blit(body, rect)
        y += line_h

    hint = hint_f.render("tap screen to continue...", True, _NARR_HINT)
    hint.set_alpha(150)
    surf.blit(hint, hint.get_rect(midtop=(inner.centerx, y + gap)))


# ─────────────────────────────────────────────────────────────
#  Input
# ─────────────────────────────────────────────────────────────

def handle_tap(px, py):
    global _typing_chars, _typing_done, _pending_water_scan

    if handle_chapter_exit_tap(px, py):
        exit_chapter()
        return

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
    if s.get("timer") and _challenge_timeout_feedback > 0.0:
        return
    if s["type"] == "memory_game" and not _memory_game_played:
        _launch_memory_game()
        return

    if s["type"] == "ingredient_puzzle" and not _ingredient_puzzle_played:
        _launch_ingredient_puzzle()
        return

    if s["type"] == "whack_a_pest" and not _whack_a_pest_played:
        _launch_whack_a_pest()
        return

    if s["type"] == "tomato_seed_extraction" and not _tomato_seed_extraction_played:
        _launch_tomato_seed_extraction()
        return

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
                if i != s.get("correct"):
                    player_data.record_mistake()
                else:
                    player_data.record_challenge_success(
                        _challenge_time_left if s.get("timer") else 0
                    )
                if _engine.choose(i):
                    _sync_chars()
                return
        return

    # Action challenge: the player has to pick a square, so this must be
    # handled before the generic tap below would advance the slide.
    if s["type"] == "action_challenge":
        _handle_action_tap(px, py)
        return

    prev_slide = _engine.slide_idx
    _engine.tap()

    # The tap may have ended the chapter (on_chapter_end fired during
    # engine.tap) — don't touch the engine afterwards.
    if _chapter_done or _engine is None:
        return

    if _engine.slide_idx != prev_slide:
        _sync_chars()
        if _engine.slide.get("type") == "memory_game" and not _memory_game_played:
            _launch_memory_game()
            return

        if _engine.slide.get("type") == "ingredient_puzzle" and not _ingredient_puzzle_played:
            _launch_ingredient_puzzle()
            return

        if _engine.slide.get("type") == "whack_a_pest" and not _whack_a_pest_played:
            _launch_whack_a_pest()
            return

        if _engine.slide.get("type") == "tomato_seed_extraction" and not _tomato_seed_extraction_played:
            _launch_tomato_seed_extraction()
            return

    # The chapter may have ended without slide_idx changing (e.g. all
    # trailing slides were skipped feedback) — don't touch the engine
    # once on_chapter_end() has fired.
    if _engine is None:
        return

    if _engine.popup_open == "scan":
        card_name = _engine.slide.get("card", "")
        _pending_water_scan = "water" in card_name.lower()
        scan_popup.open(
            card_name=card_name,
            question=_engine.slide.get("question", ""),
            on_complete=_on_scan_done,
            on_cancel=_on_scan_cancel,
        )


def _on_scan_done():
    global _water_level
    if _engine is None:
        return
    if _pending_water_scan:
        _water_level = 1.0
    _engine.on_scan_complete()
    _sync_chars()


def _on_scan_cancel():
    if _engine is not None:
        _engine.close_popup()


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


def exit_chapter():
    """Leave the current chapter and return to the chapter selector."""
    global _engine, _chars, _chapter_done, _fade_phase, _fade_alpha
    global _fade_timer, _pending_water_scan, _smoke

    if game_state.selected_chapter is None:
        return
    if _smoke is not None:
        _smoke.stop()
    scan_popup.close()
    _engine = None
    _chars = None
    _chapter_done = False
    _fade_phase = None
    _fade_alpha = 0
    _fade_timer = 0.0
    _pending_water_scan = False
    player_data.abort_chapter()
    game_state.day = 0
    game_state.selected_chapter = None
    _go_to_scene("level_select")


# ─────────────────────────────────────────────────────────────
#  Drawing
# ─────────────────────────────────────────────────────────────

def draw(surf):
    _draw_chapter_frame(surf)
    draw_chapter_exit(surf)


def handle_chapter_exit_tap(px, py):
    if game_state.selected_chapter is None:
        return False
    return _chapter_exit_button_rect().collidepoint(px, py)


def draw_chapter_exit(surf):
    if game_state.selected_chapter is not None:
        _draw_chapter_exit(surf)


def _draw_chapter_frame(surf):
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

    if stype == "memory_game":
        _draw_memory_game_return(target)
        _blit_shaken(surf)
        _finish_fade_in(surf, dt)
        return

    if stype == "ingredient_puzzle":
        _draw_ingredient_puzzle_return(target)
        _blit_shaken(surf)
        _finish_fade_in(surf, dt)
        return

    if stype == "whack_a_pest":
        _draw_whack_a_pest_return(target)
        _blit_shaken(surf)
        _finish_fade_in(surf, dt)
        return

    if stype == "tomato_seed_extraction":
        _draw_tomato_seed_extraction_return(target)
        _blit_shaken(surf)
        _finish_fade_in(surf, dt)
        return

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

    _update_challenge_timer(dt)

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

    # ── Action challenge: instruction art + two squares ─────────
    # Sits after the "scene" branch because it is the same shape of
    # screen: a background, no dialogue box, no typewriter.
    if stype == "action_challenge":
        if _chars is not None:
            _chars.draw(target)
        _draw_action(target, dt)
        _draw_day_counter(target)
        _draw_water_bar(target)
        _draw_challenge_timer(target)
        _blit_shaken(surf)
        _finish_fade_in(surf, dt)
        return

    # ── Narration overlay: board + prose, no dialogue box ────
    # Same shape of screen as "scene": a background, characters,
    # no typewriter. The board is drawn in front of the cast so
    # the passage is never read across their artwork.
    if stype == "narration_overlay":
        if _chars is not None:
            _chars.draw(target)
        _draw_narration(target)
        _draw_day_counter(target)
        _draw_water_bar(target)
        _blit_shaken(surf)
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
    _draw_challenge_timer(target)

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


def _chapter_exit_button_rect():
    button_w = max(92, min(160, int(WIDTH * 0.13)))
    button_h = max(44, min(64, int(HEIGHT * 0.075)))
    margin = max(10, int(min(WIDTH, HEIGHT) * 0.025))
    return pygame.Rect(WIDTH - button_w - margin, margin, button_w, button_h)


def _draw_chapter_exit(surf):
    rect = _chapter_exit_button_rect()
    pygame.draw.rect(surf, (132, 48, 40), rect, border_radius=rect.height // 3)
    pygame.draw.rect(surf, (245, 220, 195), rect, width=2, border_radius=rect.height // 3)

    font = _make_font(max(0.028, 16 / HEIGHT))
    label = font.render("Exit chapter", True, (255, 245, 230))
    max_width = rect.width - 16
    if label.get_width() > max_width:
        label = pygame.transform.smoothscale(
            label,
            (max_width, max(1, int(label.get_height() * max_width / label.get_width()))),
        )
    surf.blit(label, label.get_rect(center=rect.center))


def _draw_memory_game_return(surf):
    panel = pygame.Rect(
        int(WIDTH * 0.16),
        int(HEIGHT * 0.30),
        int(WIDTH * 0.68),
        int(HEIGHT * 0.38),
    )
    pygame.draw.rect(surf, _DBOX_FILL, panel, border_radius=24)
    pygame.draw.rect(surf, _DBOX_BORDER, panel, width=4, border_radius=24)

    title = _make_font(0.075).render("Memory Challenge Complete!", True, _DBOX_TEXT)
    title_width = int(panel.width * 0.9)
    if title.get_width() > title_width:
        title = pygame.transform.smoothscale(
            title,
            (title_width, int(title.get_height() * title_width / title.get_width())),
        )
    surf.blit(title, title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.42))))
    hint = _font_body.render("Tap to continue Chapter 2.", True, _HINT_COLOR)
    if hint.get_width() > title_width:
        hint = pygame.transform.smoothscale(
            hint,
            (title_width, int(hint.get_height() * title_width / hint.get_width())),
        )
    surf.blit(hint, hint.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.55))))


def _draw_ingredient_puzzle_return(surf):
    panel = pygame.Rect(
        int(WIDTH * 0.16),
        int(HEIGHT * 0.30),
        int(WIDTH * 0.68),
        int(HEIGHT * 0.38),
    )
    pygame.draw.rect(surf, _DBOX_FILL, panel, border_radius=24)
    pygame.draw.rect(surf, _DBOX_BORDER, panel, width=4, border_radius=24)

    title = _make_font(0.075).render("Ingredient Challenge Complete!", True, _DBOX_TEXT)
    title_width = int(panel.width * 0.9)
    if title.get_width() > title_width:
        title = pygame.transform.smoothscale(
            title,
            (title_width, int(title.get_height() * title_width / title.get_width())),
        )
    surf.blit(title, title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.42))))
    hint = _font_body.render("Tap to continue Chapter 3.", True, _HINT_COLOR)
    if hint.get_width() > title_width:
        hint = pygame.transform.smoothscale(
            hint,
            (title_width, int(hint.get_height() * title_width / hint.get_width())),
        )
    surf.blit(hint, hint.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.55))))


def _draw_whack_a_pest_return(surf):
    panel = pygame.Rect(
        int(WIDTH * 0.16),
        int(HEIGHT * 0.30),
        int(WIDTH * 0.68),
        int(HEIGHT * 0.38),
    )
    pygame.draw.rect(surf, _DBOX_FILL, panel, border_radius=24)
    pygame.draw.rect(surf, _DBOX_BORDER, panel, width=4, border_radius=24)

    title = _make_font(0.075).render("Whack-a-Pest Complete!", True, _DBOX_TEXT)
    title_width = int(panel.width * 0.9)
    if title.get_width() > title_width:
        title = pygame.transform.smoothscale(
            title,
            (title_width, int(title.get_height() * title_width / title.get_width())),
        )
    surf.blit(title, title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.42))))
    hint = _font_body.render("Tap to continue Chapter 4.", True, _HINT_COLOR)
    if hint.get_width() > title_width:
        hint = pygame.transform.smoothscale(
            hint,
            (title_width, int(hint.get_height() * title_width / hint.get_width())),
        )
    surf.blit(hint, hint.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.55))))


def _draw_tomato_seed_extraction_return(surf):
    panel = pygame.Rect(
        int(WIDTH * 0.16),
        int(HEIGHT * 0.30),
        int(WIDTH * 0.68),
        int(HEIGHT * 0.38),
    )
    pygame.draw.rect(surf, _DBOX_FILL, panel, border_radius=24)
    pygame.draw.rect(surf, _DBOX_BORDER, panel, width=4, border_radius=24)

    title = _make_font(0.075).render("Tomato Seed Extraction Complete!", True, _DBOX_TEXT)
    title_width = int(panel.width * 0.9)
    if title.get_width() > title_width:
        title = pygame.transform.smoothscale(
            title,
            (title_width, int(title.get_height() * title_width / title.get_width())),
        )
    surf.blit(title, title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.42))))
    hint = _font_body.render("Tap to continue Chapter 5.", True, _HINT_COLOR)
    if hint.get_width() > title_width:
        hint = pygame.transform.smoothscale(
            hint,
            (title_width, int(hint.get_height() * title_width / hint.get_width())),
        )
    surf.blit(hint, hint.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.55))))


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


def _decay_water(days_passed):
    """Reduce the meter in proportion to elapsed in-game days."""
    global _water_level
    _water_level = max(0.0, _water_level - _WATER_DECAY_PER_DAY * days_passed)


def _draw_water_bar(surf):
    """Draw only the care meters whose matching action has been encountered."""
    if _engine is None or _engine.popup_open:
        return

    visible = [gauge for gauge in _GAUGE_ORDER if _gauge_visible.get(gauge, False)]
    if not visible:
        return

    margin = max(8, int(WIDTH * 0.025))
    panel_h = max(68, int(HEIGHT * 0.09))
    panel_y = HEIGHT - panel_h - max(4, int(HEIGHT * 0.012))
    panel = pygame.Surface((WIDTH - margin * 2, panel_h), pygame.SRCALPHA)
    pygame.draw.rect(
        panel,
        (28, 22, 16, 205),
        panel.get_rect(),
        border_radius=max(8, panel_h // 5),
    )
    surf.blit(panel, (margin, panel_y))

    item_w = panel.get_width() // len(visible)
    icon_size = min(max(30, int(HEIGHT * 0.052)), panel_h - 12)
    label_font = _font_hint
    for index, gauge in enumerate(visible):
        x = margin + index * item_w
        icon = _get_gauge_icon(gauge, icon_size)
        icon_y = panel_y + (panel_h - icon_size) // 2
        surf.blit(icon, (x + 8, icon_y))

        if gauge == "water":
            water_label = f"Water {int(_water_level * 100)}%"
            label = f"{_crop_name} {water_label}" if _crop_name else water_label
        else:
            remaining = _gauge_remaining[gauge]
            total = _gauge_totals[gauge]
            label = f"{_GAUGE_LABELS[gauge]} {remaining}/{total}"
        text = label_font.render(label, True, (250, 245, 230))
        max_text_w = max(20, item_w - icon_size - 24)
        if text.get_width() > max_text_w:
            text = pygame.transform.smoothscale(
                text,
                (max_text_w, max(1, int(text.get_height() * max_text_w / text.get_width()))),
            )
        text_x = x + icon_size + 16
        surf.blit(text, (text_x, panel_y + 8))

        bar_x = text_x
        bar_y = panel_y + panel_h - 20
        bar_w = max(16, margin + (index + 1) * item_w - 8 - bar_x)
        track = pygame.Rect(bar_x, bar_y, bar_w, 9)
        pygame.draw.rect(surf, (54, 43, 31), track, border_radius=5)
        if gauge == "water":
            fraction = _water_level
            fill_color = (215, 70, 55) if _water_level < _WATER_LOW_THRESHOLD else _CROP_WATER_COLORS.get(
                _crop_name, _WATER_DEFAULT_COLOR
            )
        else:
            fraction = remaining / total if total else 0
            fill_color = _GAUGE_COLORS[gauge]
        fill_w = int(track.width * max(0.0, min(1.0, fraction)))
        if fill_w:
            pygame.draw.rect(
                surf,
                fill_color,
                pygame.Rect(track.x, track.y, fill_w, track.height),
                border_radius=5,
            )
        pygame.draw.rect(surf, (235, 225, 205), track, width=1, border_radius=5)


def _get_gauge_icon(gauge, size):
    key = (gauge, size)
    if key not in _gauge_icon_cache:
        path = config.IMG_DIR + _GAUGE_ICON_PATHS[gauge]
        image = pygame.image.load(path).convert_alpha()
        _gauge_icon_cache[key] = pygame.transform.scale(image, (size, size))
    return _gauge_icon_cache[key]


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


def _choice_image_slots():
    """Return the layout slots used to position the two image choices."""
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


def _choice_image_geometry(btn, choice):
    label_text = choice.get("label", "")
    label_h = (_font_hint.get_linesize() + 6) if label_text and _font_hint else 0
    inset = max(4, int(WIDTH * 0.004))
    img = _get_choice_img(
        choice["img"],
        btn.width - inset * 2,
        btn.height - inset * 2 - label_h,
    )
    img_rect = img.get_rect(
        centerx=btn.centerx,
        centery=btn.top + inset + (btn.height - inset * 2 - label_h) // 2,
    )
    return img, img_rect


def _choice_image_buttons():
    """Return click targets matching the visible choice artwork."""
    choices = _engine.slide.get("choices", [])
    slots = _choice_image_slots()
    buttons = []

    for slot, choice in zip(slots, choices):
        if choice.get("dbox"):
            aspect = _get_overlay_aspect(choice["dbox"])
            width = slot.width
            height = int(width / aspect)
            if height > slot.height:
                height = slot.height
                width = int(height * aspect)
            button = pygame.Rect(0, 0, width, height)
            button.center = slot.center
        elif choice.get("frame", True):
            button = slot
        elif choice.get("img"):
            _, button = _choice_image_geometry(slot, choice)
            label = choice.get("label", "")
            if label and _font_hint:
                label_rect = _font_hint.render(
                    label, True, _DBOX_TEXT
                ).get_rect(
                    centerx=slot.centerx,
                    bottom=slot.bottom - int(WIDTH * 0.014),
                )
                button = button.union(label_rect)
        else:
            button = slot
        buttons.append(button)

    return buttons


def _fit_dbox_font(text: str, max_w: int, max_h: int):
    """Largest font that lets a choice's label fit its wooden board."""
    max_w = max(1, int(max_w))
    max_h = max(1, int(max_h))

    floor_px = max(12, int(HEIGHT * _CHOICE_DBOX_FONT_MIN_FRAC))
    size     = max(floor_px, int(HEIGHT * _CHOICE_DBOX_FONT_MAX_FRAC))

    while True:
        font   = _make_font_px(size)
        lines  = _wrap_lines(text, max_w, font)
        height = len(lines) * font.get_linesize()

        if height <= max_h or size <= floor_px:
            return font, lines, height

        size -= 1


def _draw_dbox_choice(surf, btn, choice):
    """Draw one answer on its own wooden board, text inside the panel.

    Same board art and same recessed-panel fractions the narration
    slides use, so a choice board reads as part of the same world.
    Returns True when the board handled the whole choice.
    """
    path = choice.get("dbox")
    if not path:
        return False

    aspect = _get_overlay_aspect(path)

    # Fill the button rect with the board, keeping the art's own
    # proportions so the plank is never stretched.
    w = btn.width
    h = int(w / aspect)
    if h > btn.height:
        h = btn.height
        w = int(h * aspect)

    img, img_h = _get_overlay(path, w)
    board = pygame.Rect(0, 0, w, img_h)
    board.center = btn.center
    surf.blit(img, board.topleft)

    label = choice.get("label", "")
    if not label:
        return True

    # The carved frame eats into each edge, so the text only ever
    # goes inside the recessed panel.
    l, t, r, b = _NARR_PANEL
    panel = pygame.Rect(
        board.left + int(l * w),
        board.top  + int(t * img_h),
        int((r - l) * w),
        int((b - t) * img_h),
    )

    font, lines, _ = _fit_dbox_font(label, panel.width, panel.height)
    line_h = font.get_linesize()

    # The plank is textured, so a dark offset shadow under the cream
    # letters keeps every line readable at a glance.
    off = max(1, font.get_height() // 22)
    y   = panel.centery - (len(lines) * line_h) // 2

    for line in lines:
        shad = font.render(line, True, _NARR_SHADOW)
        body = font.render(line, True, _NARR_TEXT)
        rect = body.get_rect(centerx=panel.centerx, top=y)
        surf.blit(shad, rect.move(off, off))
        surf.blit(body, rect)
        y += line_h

    return True


def _draw_choice_image_buttons(surf):
    s       = _engine.slide
    choices = s.get("choices", [])
    buttons = _choice_image_slots()
    pad     = int(WIDTH * 0.014)
    r       = 14
    label_font = _font_hint

    for btn, choice in zip(buttons, choices):
        # A choice with its own "dbox" board carries the text inside
        # the wood, so it needs neither the panel nor the caption.
        if _draw_dbox_choice(surf, btn, choice):
            continue

        # Opt-out frame: slides whose art is a finished button with its own
        # frame and baked-in text (e.g. S2P55, S2P41) set "frame": False so
        # only the image is shown, with no panel behind it.
        framed = choice.get("frame", True)
        if framed:
            pygame.draw.rect(surf, _DBOX_FILL,   btn, border_radius=r)
            pygame.draw.rect(surf, _DBOX_BORDER, btn, width=_BORDER_W, border_radius=r)

        label_text = choice.get("label", "")

        img_path = choice.get("img")
        if img_path:
            img, img_rect = _choice_image_geometry(btn, choice)
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
