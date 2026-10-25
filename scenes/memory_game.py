"""Five-level garden-themed memory matching game."""

from array import array
import math
import random

import pygame

import config
import game_state
import utils


WIDTH = HEIGHT = 0
_go_to_scene = None
_background = None
_font_title = None
_font_large = None
_font_body = None
_font_small = None
_font_card_label = None
_sound_match = None
_sound_mismatch = None
_sound_complete = None
_cards = []
_buttons = {}
_level_index = 0
_selected = []
_hearts = 5
_game_over = False
_game_over_pending = False
_previewing = False
_preview_flipping = False
_preview_until = 0
_preview_duration_ms = 0
_mismatch_until = 0
_mismatch_flipping = False
_message_until = 0
_message = ""
_level_complete = False
_finale = False
_last_ticks = 0
_card_images = []
_card_back_image = None
_success_callback = None
_success_action_label = "Continue Story"

_LEVEL_PAIRS = (3, 4, 6, 8, 10)
_PREVIEW_START_MS = 6000
_PREVIEW_STEP_MS = 500
_PREVIEW_MAX_MS = 8000
_STARTING_HEARTS = 5
_FLIP_DURATION = 0.18
_MISMATCH_DELAY = 0.9
_MESSAGE_DURATION = 1.1
_PALETTE = {
    "ink": (66, 43, 25),
    "cream": (255, 246, 220),
    "green": (65, 138, 66),
    "deep_green": (35, 94, 53),
    "gold": (248, 188, 64),
    "red": (193, 76, 55),
    "shadow": (43, 36, 23, 95),
}
_scaled_art_cache = {}
_scaled_back_cache = {}
_label_cache = {}
_shadow_cache = {}
_CARD_ART = (
    ("sprout.png", "Sprout", (79, 156, 77)),
    ("sunflower.png", "Sunflower", (244, 187, 57)),
    ("carrot.png", "Carrot", (232, 123, 47)),
    ("tomato.png", "Tomato", (205, 77, 61)),
    ("corn.png", "Corn", (244, 201, 66)),
    ("strawberry.png", "Strawberry", (194, 75, 102)),
    ("apple.png", "Apple", (204, 74, 57)),
    ("pumpkin.png", "Pumpkin", (224, 127, 45)),
    ("lettuce.png", "Lettuce", (99, 164, 84)),
    ("tree.png", "Tree", (69, 130, 63)),
    ("bee.png", "Bee", (240, 185, 49)),
    ("butterfly.png", "Butterfly", (156, 104, 184)),
    ("tractor.png", "Tractor", (194, 68, 52)),
    ("watering_can.png", "Watering Can", (78, 143, 188)),
    ("basket.png", "Basket", (161, 111, 57)),
    ("shovel.png", "Shovel", (112, 132, 145)),
)


def init(width, height, go_to_scene_callback):
    global WIDTH, HEIGHT, _go_to_scene
    global _font_title, _font_large, _font_body, _font_small
    global _sound_match, _sound_mismatch, _sound_complete

    WIDTH, HEIGHT = width, height
    _go_to_scene = go_to_scene_callback
    _font_title = _make_font(0.057)
    _font_large = _make_font(0.052)
    _font_body = _make_font(0.034)
    _font_small = _make_font(0.025)
    _sound_match = _make_chime((659, 784), 0.22)
    _sound_mismatch = _make_chime((330,), 0.16)
    _sound_complete = _make_chime((523, 659, 784), 0.62)


def set_success_action(callback, label):
    """Configure the finale button for story or mini-game-menu launches."""
    global _success_callback, _success_action_label
    _success_callback = callback
    _success_action_label = label


def _make_font(size_fraction):
    size = max(16, int(HEIGHT * size_fraction))
    try:
        return pygame.font.Font("fonts/RumRaisin-Regular.ttf", size)
    except pygame.error:
        return pygame.font.SysFont("Georgia", size, bold=True)


def _make_chime(notes, duration):
    mixer = pygame.mixer.get_init()
    if mixer is None or mixer[1] != -16:
        return None
    sample_rate, _, channels = mixer
    sample_count = int(sample_rate * duration)
    note_length = max(1, sample_count // len(notes))
    samples = array("h")
    for index in range(sample_count):
        note = notes[min(index // note_length, len(notes) - 1)]
        elapsed = index / sample_rate
        note_elapsed = (index % note_length) / sample_rate
        envelope = min(1.0, note_elapsed / 0.012, (note_length / sample_rate - note_elapsed) / 0.04)
        amplitude = int(32767 * 0.16 * max(0.0, envelope) * math.sin(2 * math.pi * note * elapsed))
        samples.extend([amplitude] * channels)
    return pygame.mixer.Sound(buffer=samples.tobytes())


def _play(sound):
    if sound is not None:
        sound.play()


def start():
    """Begin a fresh run when Chapter 2 reaches its final story panel."""
    global _background, _level_index, _finale, _card_images, _card_back_image
    if not _card_images:
        card_images = [
            utils.load_img(f"memory-cards/{filename}")
            for filename, _, _ in _CARD_ART
        ]
        card_back_image = utils.load_img("memory-cards/card-back.png")
        _card_images = card_images
        _card_back_image = card_back_image
    _background = utils.load_bg("background/Monggobg.jpg", (WIDTH, HEIGHT))
    _level_index = 0
    _finale = False
    _start_level()


def _start_level():
    global _cards, _selected, _mismatch_until, _message_until, _message
    global _level_complete, _last_ticks, _mismatch_flipping, _finale
    global _previewing, _preview_flipping, _preview_until, _preview_duration_ms
    global _hearts, _game_over, _game_over_pending

    pair_count = _LEVEL_PAIRS[_level_index]
    card_ids = list(range(pair_count))
    card_ids *= 2
    random.shuffle(card_ids)
    _cards = [
        {
            "kind": card_id,
            "face_up": True,
            "matched": False,
            "flip_from": False,
            "flip_started": None,
        }
        for card_id in card_ids
    ]
    _selected = []
    _hearts = _STARTING_HEARTS
    _game_over = False
    _game_over_pending = False
    _previewing = True
    _preview_flipping = False
    _preview_duration_ms = min(
        _PREVIEW_START_MS + _PREVIEW_STEP_MS * _level_index,
        _PREVIEW_MAX_MS,
    )
    _preview_until = pygame.time.get_ticks() + _preview_duration_ms
    _mismatch_until = 0
    _mismatch_flipping = False
    _message_until = 0
    _message = ""
    _level_complete = False
    _finale = False
    _last_ticks = pygame.time.get_ticks()
    _layout()


def _layout():
    global _font_card_label, _buttons

    margin = int(min(WIDTH, HEIGHT) * 0.035)
    button_h = max(42, int(HEIGHT * 0.06))
    button_w = max(110, int(WIDTH * 0.15))
    button_top = int(HEIGHT * 0.015)
    _buttons = {
        "menu": pygame.Rect(margin, button_top, button_w, button_h),
        "restart": pygame.Rect(WIDTH - margin - button_w, button_top, button_w, button_h),
    }

    card_count = len(_cards)
    side_margin = int(WIDTH * 0.055)
    top = int(HEIGHT * 0.285)
    bottom = int(HEIGHT * 0.91)
    gap = max(8, int(min(WIDTH, HEIGHT) * 0.018))
    available_w = WIDTH - side_margin * 2
    available_h = bottom - top
    columns = max(
        (count for count in range(1, card_count + 1) if card_count % count == 0),
        key=lambda count: _grid_card_width(
            available_w, available_h, gap, card_count, count
        ) ** 2,
    )
    rows = card_count // columns
    card_w = _grid_card_width(available_w, available_h, gap, card_count, columns)
    card_h = int(card_w / 1.08)
    _font_card_label = _make_font(max(0.018, min(0.03, card_h * 0.0009)))
    _scaled_art_cache.clear()
    _scaled_back_cache.clear()
    _label_cache.clear()
    card_w = min(card_w, int((available_h - gap * (rows - 1)) / rows * 1.08))
    card_h = int(card_w / 1.08)
    grid_w = columns * card_w + (columns - 1) * gap
    grid_h = rows * card_h + (rows - 1) * gap
    start_x = (WIDTH - grid_w) // 2
    start_y = top + max(0, (available_h - grid_h) // 2)

    for index, card in enumerate(_cards):
        row, column = divmod(index, columns)
        card["rect"] = pygame.Rect(
            start_x + column * (card_w + gap),
            start_y + row * (card_h + gap),
            card_w,
            card_h,
        )


def _grid_card_width(available_w, available_h, gap, card_count, columns):
    rows = card_count // columns
    width_limit = (available_w - gap * (columns - 1)) // columns
    height_limit = int((available_h - gap * (rows - 1)) / rows * 1.08)
    return max(1, min(width_limit, height_limit))


def _leave():
    game_state.day = 0
    game_state.selected_chapter = None
    _go_to_scene("level_select")


def _continue_story():
    from scenes import story_mode

    story_mode.resume_after_memory_game()
    _go_to_scene("story_mode")


def _finish_success():
    if _success_callback is not None:
        _success_callback()
    else:
        _continue_story()


def _button_rects():
    if _finale:
        button_w = int(WIDTH * 0.20)
        button_h = int(HEIGHT * 0.085)
        gap = int(WIDTH * 0.02)
        start_x = (WIDTH - (button_w * 3 + gap * 2)) // 2
        return {
            "continue_story": pygame.Rect(start_x, int(HEIGHT * 0.65), button_w, button_h),
            "replay": pygame.Rect(
                start_x + button_w + gap, int(HEIGHT * 0.65), button_w, button_h
            ),
            "level_select": pygame.Rect(
                start_x + (button_w + gap) * 2, int(HEIGHT * 0.65), button_w, button_h
            ),
        }
    if _game_over:
        button_w = int(WIDTH * 0.25)
        button_h = int(HEIGHT * 0.085)
        gap = int(WIDTH * 0.035)
        start_x = (WIDTH - (button_w * 2 + gap)) // 2
        return {
            "retry_level": pygame.Rect(start_x, int(HEIGHT * 0.65), button_w, button_h),
            "level_select": pygame.Rect(
                start_x + button_w + gap, int(HEIGHT * 0.65), button_w, button_h
            ),
        }
    button_w = int(WIDTH * 0.20)
    button_h = int(HEIGHT * 0.085)
    gap = int(WIDTH * 0.02)
    start_x = (WIDTH - (button_w * 3 + gap * 2)) // 2
    return {
        "next_level": pygame.Rect(start_x, int(HEIGHT * 0.65), button_w, button_h),
        "replay": pygame.Rect(
            start_x + button_w + gap, int(HEIGHT * 0.65), button_w, button_h
        ),
        "level_select": pygame.Rect(
            start_x + (button_w + gap) * 2, int(HEIGHT * 0.65), button_w, button_h
        ),
    }


def _complete_level():
    global _level_complete, _finale
    _level_complete = True
    _finale = _level_index == len(_LEVEL_PAIRS) - 1
    _play(_sound_complete)


def _flip(card, face_up):
    card["flip_from"] = card["face_up"]
    card["face_up"] = face_up
    card["flip_started"] = pygame.time.get_ticks()


def _select_card(index):
    global _selected, _mismatch_until, _mismatch_flipping, _message, _message_until
    global _hearts, _game_over_pending
    if _level_complete or _game_over or _previewing or _mismatch_until or len(_selected) >= 2:
        return
    card = _cards[index]
    if card["matched"] or card["face_up"]:
        return

    _flip(card, True)
    _selected.append(index)
    if len(_selected) == 2:
        first, second = (_cards[i] for i in _selected)
        if first["kind"] == second["kind"]:
            first["matched"] = second["matched"] = True
            _selected = []
            _play(_sound_match)
            _message = "Great job! You found a match!"
            _message_until = pygame.time.get_ticks() + int(_MESSAGE_DURATION * 1000)
            if all(item["matched"] for item in _cards):
                _complete_level()
        else:
            _hearts -= 1
            _play(_sound_mismatch)
            _message = "One heart used. Keep looking!" if _hearts else "Let's try this level again!"
            _message_until = pygame.time.get_ticks() + int(_MISMATCH_DELAY * 1000)
            _mismatch_until = _message_until
            _mismatch_flipping = False
            _game_over_pending = _hearts == 0


def handle_tap(px, py):
    global _level_index, _level_complete, _finale

    if not _cards:
        return
    if _game_over:
        for key, rect in _button_rects().items():
            if rect.collidepoint(px, py):
                if key == "retry_level":
                    _start_level()
                else:
                    _leave()
                return
        return
    if _level_complete:
        for key, rect in _button_rects().items():
            if rect.collidepoint(px, py):
                if key == "next_level":
                    _level_index += 1
                    _start_level()
                elif key == "continue_story":
                    _finish_success()
                elif key == "replay":
                    _start_level()
                else:
                    _leave()
                return
        return

    if _buttons["menu"].collidepoint(px, py):
        _leave()
        return
    if _buttons["restart"].collidepoint(px, py):
        _start_level()
        return
    if _previewing:
        return
    if _mismatch_until:
        return
    for index, card in enumerate(_cards):
        if card["rect"].collidepoint(px, py):
            _select_card(index)
            return


def handle_drag(_px, _py):
    pass


def handle_release(_px, _py):
    pass


def _update(now):
    global _selected, _mismatch_until, _mismatch_flipping
    global _previewing, _preview_flipping, _preview_until, _game_over
    global _game_over_pending
    if _previewing and now >= _preview_until:
        if _preview_flipping:
            _previewing = False
            _preview_flipping = False
        else:
            for card in _cards:
                _flip(card, False)
            _preview_flipping = True
            _preview_until = now + int(_FLIP_DURATION * 1000)

    if _mismatch_until and now >= _mismatch_until:
        if _mismatch_flipping:
            _mismatch_until = 0
            _mismatch_flipping = False
            if _game_over_pending:
                _game_over = True
                _game_over_pending = False
        else:
            for index in _selected:
                _flip(_cards[index], False)
            _selected = []
            _mismatch_flipping = True
            _mismatch_until = now + int(_FLIP_DURATION * 1000)

    for card in _cards:
        started = card["flip_started"]
        if started is not None and now - started >= int(_FLIP_DURATION * 1000):
            card["flip_started"] = None


def draw(surf):
    global _last_ticks
    if not _cards:
        surf.fill(config.STORY_BG_COLOR)
        return

    now = pygame.time.get_ticks()
    dt = max(0.0, min(0.05, (now - _last_ticks) / 1000.0))
    _last_ticks = now
    _update(now)

    if _background is not None:
        surf.blit(_background, (0, 0))
    else:
        surf.fill(config.STORY_BG_COLOR)
    _draw_header(surf)
    for card in _cards:
        _draw_card(surf, card, now)
    _draw_feedback(surf, now, dt)
    if _game_over:
        _draw_game_over(surf)
    elif _level_complete:
        _draw_completion(surf)


def _draw_header(surf):
    panel_rect = pygame.Rect(
        int(WIDTH * 0.12),
        int(HEIGHT * 0.065),
        int(WIDTH * 0.76),
        int(HEIGHT * 0.22),
    )
    panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(panel, (41, 67, 39, 185), panel.get_rect(), border_radius=22)
    pygame.draw.rect(
        panel,
        (241, 212, 145, 220),
        panel.get_rect(),
        width=2,
        border_radius=22,
    )
    surf.blit(panel, panel_rect)

    title = _fit(_font_title, "The Great Garden Memory Challenge!", int(WIDTH * 0.76))
    surf.blit(title, title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.105))))

    _draw_button(surf, _buttons["menu"], "Level Select", _PALETTE["deep_green"])
    _draw_button(surf, _buttons["restart"], "Restart", _PALETTE["red"])

    level_text = _font_large.render(
        f"Level {_level_index + 1} of {len(_LEVEL_PAIRS)}",
        True,
        _PALETTE["cream"],
    )
    surf.blit(level_text, level_text.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.165))))

    if _previewing:
        instruction_text = (
            "Get ready to find the pairs!"
            if _preview_flipping
            else "Memorize the cards!"
        )
    elif _level_index == 0:
        instruction_text = "Tap a card to peek, then find its matching garden friend!"
    else:
        instruction_text = "Find two matching garden cards. Take your time!"
    instruction = _fit(_font_body, instruction_text, int(WIDTH * 0.75), _PALETTE["cream"])
    surf.blit(instruction, instruction.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.215))))

    found = sum(card["matched"] for card in _cards) // 2
    pair_count = _LEVEL_PAIRS[_level_index]
    if _previewing and not _preview_flipping:
        seconds_left = max(1, math.ceil((_preview_until - pygame.time.get_ticks()) / 1000))
        counter = _font_body.render(f"Cards flip in {seconds_left}...", True, (255, 226, 144))
    else:
        counter = _font_body.render(
            f"{found} / {pair_count} pairs found",
            True,
            (255, 226, 144),
        )
    surf.blit(counter, counter.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.26))))
    _draw_hearts(surf)


def _draw_hearts(surf):
    label = _font_small.render("Lives", True, _PALETTE["cream"])
    heart_w = max(13, int(HEIGHT * 0.025))
    gap = max(4, int(heart_w * 0.22))
    label_rect = label.get_rect(midright=(int(WIDTH * 0.72), int(HEIGHT * 0.26)))
    surf.blit(label, label_rect)
    start_x = label_rect.right + max(8, int(WIDTH * 0.008))
    center_y = int(HEIGHT * 0.26)
    for index in range(_STARTING_HEARTS):
        center_x = start_x + index * (heart_w + gap) + heart_w // 2
        color = (226, 82, 71) if index < _hearts else (104, 91, 77)
        width = max(0, heart_w // 12) if index < _hearts else 2
        top = center_y - heart_w // 2
        pygame.draw.circle(
            surf,
            color,
            (center_x - heart_w // 4, top + heart_w // 3),
            heart_w // 4,
            width,
        )
        pygame.draw.circle(
            surf,
            color,
            (center_x + heart_w // 4, top + heart_w // 3),
            heart_w // 4,
            width,
        )
        pygame.draw.polygon(
            surf,
            color,
            (
                (center_x - heart_w // 2, top + heart_w // 3),
                (center_x + heart_w // 2, top + heart_w // 3),
                (center_x, center_y + heart_w // 2),
            ),
            width,
        )


def _draw_card(surf, card, now):
    rect = card["rect"]
    visual_face_up = card["face_up"]
    width_scale = 1.0
    started = card["flip_started"]
    if started is not None:
        progress = min(1.0, (now - started) / (_FLIP_DURATION * 1000))
        width_scale = max(0.08, abs(1.0 - 2.0 * progress))
        visual_face_up = card["face_up"] if progress >= 0.5 else card["flip_from"]
    draw_rect = pygame.Rect(0, 0, max(4, int(rect.width * width_scale)), rect.height)
    draw_rect.center = rect.center

    shadow_size = (draw_rect.width + 12, draw_rect.height + 12)
    shadow = _shadow_cache.get(shadow_size)
    if shadow is None:
        shadow = pygame.Surface(shadow_size, pygame.SRCALPHA)
        pygame.draw.rect(
            shadow,
            _PALETTE["shadow"],
            shadow.get_rect(),
            border_radius=max(8, draw_rect.width // 12),
        )
        _shadow_cache[shadow_size] = shadow
    surf.blit(shadow, shadow.get_rect(center=(draw_rect.centerx, draw_rect.centery + 5)))

    radius = max(8, min(draw_rect.width, draw_rect.height) // 12)
    if visual_face_up:
        border_color = _CARD_ART[card["kind"]][2]
        pygame.draw.rect(surf, border_color, draw_rect, border_radius=radius)
        inner = draw_rect.inflate(-6, -6)
        pygame.draw.rect(surf, (255, 249, 227), inner, border_radius=max(6, radius - 2))
        art_panel = pygame.Rect(
            inner.x + int(inner.width * 0.07),
            inner.y + int(inner.height * 0.07),
            int(inner.width * 0.86),
            int(inner.height * 0.67),
        )
        pygame.draw.rect(
            surf,
            (250, 241, 210),
            art_panel,
            border_radius=max(6, radius - 3),
        )
        pygame.draw.line(
            surf,
            tuple(max(0, channel - 28) for channel in border_color),
            (inner.x + int(inner.width * 0.18), inner.bottom - int(inner.height * 0.19)),
            (inner.right - int(inner.width * 0.18), inner.bottom - int(inner.height * 0.19)),
            max(1, draw_rect.width // 110),
        )
        _draw_art(surf, card["kind"], draw_rect)
    else:
        pygame.draw.rect(surf, (47, 113, 65), draw_rect, border_radius=radius)
        inset = draw_rect.inflate(-7, -7)
        pygame.draw.rect(surf, (77, 150, 81), inset, border_radius=max(6, radius - 2))
        pygame.draw.rect(
            surf,
            (240, 218, 157),
            inset,
            width=max(2, draw_rect.width // 70),
            border_radius=max(6, radius - 2),
        )
        _draw_card_back(surf, draw_rect)
    if card["matched"]:
        pygame.draw.rect(
            surf,
            (255, 220, 93),
            draw_rect.inflate(-4, -4),
            width=max(3, draw_rect.width // 35),
            border_radius=radius,
        )


def _draw_card_back(surf, rect):
    inset = rect.inflate(-7, -7)
    size = inset.size
    image = _scaled_back_cache.get(size)
    if image is None:
        image = pygame.transform.smoothscale(_card_back_image, size)
        _scaled_back_cache[size] = image
    surf.blit(image, image.get_rect(center=rect.center))


def _draw_art(surf, kind, rect):
    art_rect = pygame.Rect(
        rect.x + int(rect.width * 0.13),
        rect.y + int(rect.height * 0.08),
        int(rect.width * 0.74),
        int(rect.height * 0.70),
    )
    source = _card_images[kind]
    scale = min(art_rect.width / source.get_width(), art_rect.height / source.get_height())
    image_size = (
        max(1, int(source.get_width() * scale)),
        max(1, int(source.get_height() * scale)),
    )
    image = _scaled_art_cache.get((kind, image_size))
    if image is None:
        image = pygame.transform.smoothscale(source, image_size)
        _scaled_art_cache[(kind, image_size)] = image
    surf.blit(image, image.get_rect(center=art_rect.center))

    label = _label_cache.get(kind)
    if label is None:
        label = _fit(
            _font_card_label,
            _CARD_ART[kind][1],
            int(rect.width * 0.82),
            _PALETTE["ink"],
        )
        _label_cache[kind] = label
    surf.blit(label, label.get_rect(center=(rect.centerx, rect.bottom - int(rect.height * 0.11))))


class _IconPainter:
    def __init__(self, surf, scale):
        self.surf = surf
        self.scale = scale

    def _point(self, point):
        return tuple(int(value * self.scale) for value in point)

    def _rect(self, bounds):
        rect = pygame.Rect(bounds)
        return pygame.Rect(
            int(rect.x * self.scale),
            int(rect.y * self.scale),
            int(rect.width * self.scale),
            int(rect.height * self.scale),
        )

    def rect(self, color, bounds, width=0, border_radius=0):
        return pygame.draw.rect(
            self.surf,
            color,
            self._rect(bounds),
            width=int(width * self.scale),
            border_radius=int(border_radius * self.scale),
        )

    def line(self, color, start, end, width=1):
        return pygame.draw.line(
            self.surf,
            color,
            self._point(start),
            self._point(end),
            max(1, int(width * self.scale)),
        )

    def ellipse(self, color, bounds, width=0):
        return pygame.draw.ellipse(
            self.surf,
            color,
            self._rect(bounds),
            width=int(width * self.scale),
        )

    def circle(self, color, center, radius, width=0):
        return pygame.draw.circle(
            self.surf,
            color,
            self._point(center),
            int(radius * self.scale),
            width=int(width * self.scale),
        )

    def polygon(self, color, points, width=0):
        return pygame.draw.polygon(
            self.surf,
            color,
            [self._point(point) for point in points],
            width=int(width * self.scale),
        )

    def arc(self, color, bounds, start_angle, stop_angle, width=1):
        return pygame.draw.arc(
            self.surf,
            color,
            self._rect(bounds),
            start_angle,
            stop_angle,
            max(1, int(width * self.scale)),
        )


def _paint_icon(surf, kind):
    draw = _IconPainter(surf, 3)
    green = (70, 135, 62)
    dark_green = (45, 105, 50)
    if kind == 0:
        draw.rect((157, 100, 55), (36, 67, 48, 22), border_radius=5)
        draw.rect((189, 131, 74), (36, 67, 48, 22), width=1, border_radius=5)
        draw.line((225, 185, 115), (37, 69), (83, 69), 3)
        draw.line(dark_green, (60, 68), (60, 34), 5)
        draw.ellipse((88, 171, 83), (27, 34, 38, 21))
        draw.ellipse((116, 192, 91), (59, 26, 34, 21))
        draw.line((176, 215, 139), (32, 48), (57, 42), 2)
        draw.line((176, 215, 139), (63, 37), (85, 31), 2)
        draw.ellipse((233, 201, 125), (31, 89, 58, 7))
    elif kind == 1:
        draw.line(dark_green, (60, 90), (60, 42), 5)
        draw.ellipse(green, (34, 58, 31, 15))
        draw.ellipse(green, (59, 69, 30, 14))
        draw.line((150, 199, 111), (60, 85), (60, 62), 2)
        for angle in range(0, 360, 60):
            cx = int(60 + 19 * math.cos(math.radians(angle)))
            cy = int(34 + 19 * math.sin(math.radians(angle)))
            draw.circle((246, 190, 59), (cx, cy), 12)
            draw.circle((255, 220, 119), (cx - 3, cy - 4), 4)
        draw.circle((116, 73, 38), (60, 34), 11)
        draw.circle((229, 171, 72), (60, 34), 8)
        for x, y in ((57, 32), (63, 35), (59, 38)):
            draw.circle((123, 81, 42), (x, y), 1)
    elif kind == 2:
        draw.polygon((238, 132, 49), [(42, 28), (79, 28), (60, 87)])
        draw.line((255, 174, 79), (48, 40), (58, 72), 3)
        draw.line((238, 132, 49), (43, 31), (58, 87), 4)
        draw.line((238, 132, 49), (78, 31), (61, 87), 4)
        for x, y in ((48, 48), (52, 60), (71, 47), (67, 61)):
            draw.line((193, 94, 42), (x, y), (x + (3 if x < 60 else -3), y + 3), 2)
        draw.line(dark_green, (60, 32), (60, 18), 4)
        draw.ellipse(green, (36, 12, 26, 13))
        draw.ellipse((90, 168, 68), (59, 14, 26, 13))
        draw.line((137, 194, 105), (40, 17), (55, 22), 2)
        draw.line((137, 194, 105), (63, 19), (80, 15), 2)
    elif kind == 3:
        draw.circle((212, 66, 55), (60, 56), 30)
        draw.ellipse((231, 92, 73), (39, 31, 29, 17))
        draw.ellipse((167, 49, 45), (38, 27, 44, 55), width=1)
        draw.polygon(dark_green, [(60, 34), (54, 23), (60, 27), (67, 20), (65, 31), (76, 30), (66, 38)])
        draw.line((97, 67, 47), (60, 27), (61, 16), 4)
        draw.ellipse((255, 154, 115), (37, 39, 12, 21))
    elif kind == 4:
        draw.ellipse((245, 199, 64), (33, 21, 54, 68))
        for x in (43, 54, 66, 77):
            draw.line((219, 164, 48), (x, 25), (x, 84), 3)
        for y in (36, 48, 60, 72):
            for x in (47, 59, 71):
                draw.circle((255, 226, 125), (x, y), 2)
        draw.polygon(green, [(39, 30), (30, 17), (48, 24)])
        draw.polygon((86, 160, 68), [(78, 30), (91, 17), (72, 24)])
        draw.line((152, 200, 103), (34, 29), (45, 25), 2)
        draw.line((152, 200, 103), (76, 26), (87, 22), 2)
    elif kind == 5:
        draw.circle((206, 67, 94), (60, 57), 28)
        draw.circle((150, 44, 75), (60, 57), 28, width=1)
        draw.polygon(green, [(60, 37), (48, 25), (57, 30), (61, 16), (66, 30), (78, 23), (70, 39)])
        for x, y in ((48, 51), (62, 48), (73, 58), (53, 66), (66, 73)):
            draw.ellipse((255, 222, 150), (x, y, 4, 7), width=1)
    elif kind == 6:
        draw.circle((209, 68, 57), (51, 56), 23)
        draw.circle((209, 68, 57), (70, 56), 23)
        draw.polygon((209, 68, 57), [(30, 59), (90, 59), (61, 91)])
        draw.circle((160, 49, 44), (51, 56), 23, width=1)
        draw.circle((160, 49, 44), (70, 56), 23, width=1)
        draw.line((105, 72, 45), (60, 34), (64, 18), 5)
        draw.ellipse(green, (62, 17, 24, 12))
        draw.ellipse((255, 144, 104), (39, 42, 11, 17))
    elif kind == 7:
        draw.ellipse((235, 133, 49), (29, 35, 62, 50))
        for x in (45, 60, 75):
            draw.arc((191, 92, 37), (x - 12, 32, 24, 57), 0, 3.14, 3)
        draw.ellipse((181, 99, 43), (33, 39, 54, 42), width=1)
        draw.rect((93, 70, 45), (56, 25, 9, 14), border_radius=3)
        draw.ellipse((96, 157, 73), (61, 16, 24, 12))
        draw.line((255, 172, 89), (37, 55), (50, 49), 3)
    elif kind == 8:
        draw.ellipse((102, 169, 76), (22, 38, 40, 26))
        draw.ellipse((121, 184, 83), (57, 27, 42, 28))
        draw.ellipse((66, 137, 51), (22, 38, 40, 26), width=1)
        draw.ellipse((76, 150, 55), (57, 27, 42, 28), width=1)
        draw.line((62, 131, 67), (60, 45), (60, 88), 5)
        draw.line((62, 131, 67), (60, 62), (35, 51), 4)
        draw.line((62, 131, 67), (61, 70), (86, 53), 4)
        draw.line((62, 131, 67), (60, 77), (40, 83), 4)
        draw.line((180, 210, 124), (60, 55), (36, 47), 2)
        draw.line((180, 210, 124), (61, 67), (85, 48), 2)
    else:
        draw.polygon((83, 151, 192), [(38, 44), (70, 44), (66, 78), (43, 78)])
        draw.arc((51, 103, 143), (31, 34, 31, 41), 1.5, 4.8, 5)
        draw.polygon((83, 151, 192), [(68, 51), (95, 36), (99, 42), (72, 61)])
        draw.line((47, 112, 164), (88, 40), (101, 42), 5)
        draw.line((174, 215, 245), (41, 47), (65, 47), 3)
        draw.line((174, 215, 245), (43, 77), (65, 77), 3)
        draw.circle((211, 231, 240), (51, 55), 2)
        draw.circle((211, 231, 240), (58, 55), 2)
        draw.circle((211, 231, 240), (51, 63), 2)
        draw.circle((211, 231, 240), (58, 63), 2)
        for x in (95, 106, 112):
            draw.circle((89, 170, 218), (x, 54 + (x % 3) * 7), 3)


def _draw_feedback(surf, now, _dt):
    if _message and now < _message_until and not _level_complete:
        label = _font_body.render(_message, True, _PALETTE["cream"])
        panel = pygame.Rect(
            WIDTH // 2 - int(WIDTH * 0.25),
            int(HEIGHT * 0.925),
            int(WIDTH * 0.50),
            int(HEIGHT * 0.055),
        )
        pygame.draw.rect(surf, (45, 91, 47), panel, border_radius=18)
        surf.blit(label, label.get_rect(center=panel.center))


def _draw_game_over(surf):
    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((23, 41, 20, 185))
    surf.blit(shade, (0, 0))

    panel = pygame.Rect(
        int(WIDTH * 0.16),
        int(HEIGHT * 0.26),
        int(WIDTH * 0.68),
        int(HEIGHT * 0.48),
    )
    pygame.draw.rect(surf, (255, 247, 219), panel, border_radius=28)
    pygame.draw.rect(surf, (177, 128, 59), panel, width=5, border_radius=28)

    title = _fit(
        _font_large,
        "Out of hearts!",
        int(panel.width * 0.88),
        _PALETTE["red"],
    )
    surf.blit(title, title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.39))))
    detail = _fit(
        _font_body,
        "Try this level again. You can do it!",
        int(panel.width * 0.9),
        _PALETTE["ink"],
    )
    surf.blit(detail, detail.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.50))))

    for key, rect in _button_rects().items():
        label = "Try Again" if key == "retry_level" else "Level Select"
        color = _PALETTE["green"] if key == "retry_level" else _PALETTE["deep_green"]
        _draw_button(surf, rect, label, color)


def _draw_completion(surf):
    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((23, 41, 20, 178))
    surf.blit(shade, (0, 0))

    panel = pygame.Rect(
        int(WIDTH * 0.16),
        int(HEIGHT * 0.25),
        int(WIDTH * 0.68),
        int(HEIGHT * 0.53),
    )
    pygame.draw.rect(surf, (255, 247, 219), panel, border_radius=28)
    pygame.draw.rect(surf, (177, 128, 59), panel, width=5, border_radius=28)

    title_text = "Amazing! All the pairs are found!" if not _finale else "You're a Master Farmer!"
    title = _fit(_font_large, title_text, int(panel.width * 0.9), _PALETTE["deep_green"])
    surf.blit(title, title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.39))))
    detail = (
        f"Level {_level_index + 1} complete! You're ready for the next challenge."
        if not _finale
        else "You completed all five garden memory challenges!"
    )
    detail_label = _fit(_font_body, detail, int(panel.width * 0.88), _PALETTE["ink"])
    surf.blit(detail_label, detail_label.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.51))))

    labels = (
        {
            "continue_story": _success_action_label,
            "replay": "Replay Level",
            "level_select": "Level Select",
        }
        if _finale
        else {
            "next_level": "Next Level",
            "replay": "Replay Level",
            "level_select": "Level Select",
        }
    )
    for key, rect in _button_rects().items():
        color = _PALETTE["green"] if key in ("next_level", "continue_story") else _PALETTE["deep_green"]
        _draw_button(surf, rect, labels[key], color)


def _fit(font, text, max_width, color=(255, 255, 255)):
    image = font.render(text, True, color)
    if image.get_width() <= max_width:
        return image
    return pygame.transform.smoothscale(
        image,
        (max_width, max(1, int(image.get_height() * max_width / image.get_width()))),
    )


def _draw_button(surf, rect, label, color):
    pygame.draw.rect(surf, (38, 32, 23), rect.move(0, 4), border_radius=16)
    pygame.draw.rect(surf, color, rect, border_radius=16)
    pygame.draw.rect(surf, (255, 244, 207), rect, width=2, border_radius=16)
    text = _fit(_font_body, label, int(rect.width * 0.88))
    surf.blit(text, text.get_rect(center=rect.center))
