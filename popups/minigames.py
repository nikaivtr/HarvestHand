"""Floating carousel popup for launching mini-games."""

import os

import pygame

import config


WIDTH = HEIGHT = 0
_close_popup = None
_launch = None
_games = []
_font_title = None
_font_body = None
_font_label = None
_font_button = None
_background = None
_close_image = None

_viewport = None
_close_rect = None
_card_width = 0
_image_size = (0, 0)
_step = 0
_scroll = 0.0
_target_scroll = 0.0
_dragging = False
_drag_start_x = 0
_drag_start_scroll = 0.0
_moved = False

MIN_DRAG = 8
_INK = (39, 61, 43)
_MUTED = (69, 82, 67)
_ACCENT = (128, 91, 43)

_GAME_DATA = (
    {
        "id": "memory_game",
        "name": "Garden Memory",
        "desc": "Find matching cards and sharpen your memory.",
        "image": os.path.join(config.IMG_DIR, "minigames", "memorygame.jpg"),
        "color": (80, 139, 92),
    },
    {
        "id": "ingredient_puzzle",
        "name": "Ingredients Puzzle Game",
        "desc": "Piece together fresh ingredients for the kitchen.",
        "image": os.path.join(config.IMG_DIR, "minigames", "ingredientspuzzlegame.jpg"),
        "color": (193, 132, 78),
    },
    {
        "id": "whack_a_pest",
        "name": "Whack-a-Pest",
        "desc": "Protect the garden from hungry invading pests.",
        "image": os.path.join(config.IMG_DIR, "minigames", "whackapestgame.jpg"),
        "color": (91, 145, 75),
    },
    {
        "id": "tomato_seed_extraction",
        "name": "Tomato Seed Extraction",
        "desc": "Slice tomatoes and extract their seeds.",
        "image": os.path.join(config.IMG_DIR, "minigames", "tomatoseedextractiongame.jpg"),
        "color": (165, 58, 43),
    },
)


def init(width, height, close_popup_callback, launch_callback=None):
    global WIDTH, HEIGHT, _close_popup, _launch, _games
    global _font_title, _font_body, _font_label, _font_button
    global _viewport, _close_rect
    global _card_width, _image_size, _step, _scroll, _target_scroll
    global _background, _close_image

    WIDTH, HEIGHT = width, height
    _close_popup = close_popup_callback
    _launch = launch_callback
    background = pygame.image.load(
        os.path.join(config.IMG_DIR, "background", "menubg.png")
    ).convert()
    _background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

    _font_title = _make_font(max(30, int(HEIGHT * 0.064)), bold=True)
    _font_body = _make_font(max(17, int(HEIGHT * 0.027)))
    _font_label = _make_font(max(14, int(HEIGHT * 0.021)))
    _font_button = _make_font(max(16, int(HEIGHT * 0.025)), bold=True)

    margin_x = max(20, int(WIDTH * 0.045))
    top = int(HEIGHT * 0.20)
    bottom = int(HEIGHT * 0.84)
    _viewport = pygame.Rect(
        margin_x,
        top,
        max(1, WIDTH - margin_x * 2),
        max(1, bottom - top),
    )
    _card_width = int(WIDTH * 0.54)
    _step = int(WIDTH * 0.52)
    _image_size = (
        min(_card_width - 24, int(WIDTH * 0.39)),
        min(int(HEIGHT * 0.34), max(80, _viewport.height - 190)),
    )

    close_size = max(44, int(min(WIDTH, HEIGHT) * 0.075))
    close_source = pygame.image.load(
        os.path.join(config.IMG_DIR, "buttons", "btn_close.png")
    ).convert_alpha()
    close_height = max(1, round(close_size * close_source.get_height() / close_source.get_width()))
    _close_image = pygame.transform.smoothscale(
        close_source, (close_size, close_height)
    )
    _close_rect = pygame.Rect(
        WIDTH - margin_x - _close_image.get_width(),
        max(12, int(HEIGHT * 0.035)),
        *_close_image.get_size(),
    )
    _games = []
    for game in _GAME_DATA:
        try:
            image = pygame.image.load(game["image"]).convert()
        except (pygame.error, OSError):
            image = None
        _games.append({**game, "surface": image})

    _scroll = 0.0
    _target_scroll = 0.0


def _make_font(size, bold=False):
    try:
        font_path = os.path.join("fonts", "RumRaisin-Regular.ttf")
        return pygame.font.Font(font_path, size)
    except (pygame.error, OSError):
        return pygame.font.SysFont("Arial", size, bold=bold)


def _max_scroll():
    return max(0, (_step * (len(_games) - 1)))


def _clamp_scroll(value):
    return max(0.0, min(float(_max_scroll()), value))


def _active_index():
    if not _games or _step <= 0:
        return 0
    return max(0, min(len(_games) - 1, round(_target_scroll / _step)))


def _set_active(index):
    global _target_scroll
    index = max(0, min(len(_games) - 1, index))
    _target_scroll = float(index * _step)


def _card_rect(index, scroll=None):
    if scroll is None:
        scroll = _scroll
    center_x = _viewport.centerx + index * _step - scroll
    card_h = min(int(HEIGHT * 0.62), _viewport.height + 24)
    return pygame.Rect(
        round(center_x - _card_width / 2),
        round(_viewport.centery - card_h / 2),
        _card_width,
        card_h,
    )


def _card_focus(card_rect):
    distance = abs(card_rect.centerx - _viewport.centerx) / max(1, _step)
    return max(0.78, 1.0 - distance * 0.22)


def _cover_dimensions(game, focus):
    if game["surface"] is not None:
        source_w, source_h = game["surface"].get_size()
        fit_scale = min(
            _image_size[0] / source_w,
            _image_size[1] / source_h,
        )
        return (
            max(1, round(source_w * fit_scale * focus)),
            max(1, round(source_h * fit_scale * focus)),
        )
    side = max(1, round(min(_image_size) * focus))
    return side, side


def _play_rect(card_rect, game, focus):
    button_w = min(int(_card_width * 0.52), max(150, int(WIDTH * 0.22)))
    button_h = max(48, int(HEIGHT * 0.067))
    cover_h = _cover_dimensions(game, focus)[1]
    cover_center_y = _viewport.top + _image_size[1] // 2 + 6
    cover_bottom = cover_center_y + cover_h // 2
    title = _font_title.render(game["name"], True, _INK)
    description_lines = _wrap_text(game["desc"], _font_body, _card_width - 30)
    description_bottom = (
        cover_bottom + 18 + title.get_height() + 8
        + min(2, len(description_lines)) * (_font_body.get_linesize() + 3)
    )
    y = max(
        description_bottom + 8,
        min(card_rect.bottom - button_h - 4, _viewport.bottom - button_h - 2),
    )
    return pygame.Rect(card_rect.centerx - button_w // 2, y, button_w, button_h)


def handle_tap(px, py):
    global _dragging, _drag_start_x, _drag_start_scroll, _moved

    _dragging = True
    _drag_start_x = px
    _drag_start_scroll = _scroll
    _moved = False


def handle_drag(px, py):
    global _scroll, _moved

    if not _dragging:
        return
    if abs(px - _drag_start_x) > MIN_DRAG:
        _moved = True
    if _moved:
        _scroll = _clamp_scroll(_drag_start_scroll - (px - _drag_start_x))


def handle_release(px, py):
    global _dragging, _target_scroll

    if not _dragging:
        return
    was_moved = _moved
    _dragging = False

    if was_moved:
        if _step:
            _set_active(round(_scroll / _step))
        return

    if _close_rect.collidepoint(px, py):
        _close_popup()
        return

    for index, game in enumerate(_games):
        card_rect = _card_rect(index)
        focus = _card_focus(card_rect)
        if focus >= 0.97 and _play_rect(card_rect, game, focus).collidepoint(px, py):
            if _launch is not None:
                _launch(game["id"])
            return
        if _viewport.collidepoint(px, py) and card_rect.collidepoint(px, py):
            _set_active(index)
            return

    if not _viewport.collidepoint(px, py):
        _close_popup()


def _draw_cover(surf, game, rect, scale):
    base_size = _cover_dimensions(game, 1.0)
    size = (
        max(1, round(base_size[0] * scale)),
        max(1, round(base_size[1] * scale)),
    )
    cover_rect = pygame.Rect(0, 0, *size)
    cover_rect.center = rect.center

    shadow = pygame.Surface((size[0] + 24, size[1] + 24), pygame.SRCALPHA)
    pygame.draw.rect(
        shadow,
        (0, 0, 0, 95),
        shadow.get_rect(),
        border_radius=max(14, int(HEIGHT * 0.025)),
    )
    surf.blit(shadow, shadow.get_rect(center=cover_rect.center).move(0, 12))

    image_layer = pygame.Surface(size, pygame.SRCALPHA)
    radius = max(14, int(HEIGHT * 0.025))

    image = game["surface"]
    if image is not None:
        fitted = pygame.transform.smoothscale(image, size)
        image_layer.blit(fitted, (0, 0))
        clip = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(clip, (255, 255, 255, 255), clip.get_rect(), border_radius=radius)
        image_layer.blit(clip, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    else:
        pygame.draw.rect(
            image_layer, (*game["color"], 255), image_layer.get_rect(), border_radius=radius
        )
        initial = _make_font(max(48, int(size[0] * 0.32)), bold=True).render(
            game["name"][0], True, (255, 255, 255)
        )
        image_layer.blit(initial, initial.get_rect(center=image_layer.get_rect().center))

    pygame.draw.rect(
        image_layer, (255, 255, 255, 195), image_layer.get_rect(), width=2,
        border_radius=radius,
    )
    surf.blit(image_layer, cover_rect)
    return cover_rect


def _draw_card(surf, index):
    game = _games[index]
    card_rect = _card_rect(index)
    focus = _card_focus(card_rect)

    image_rect = pygame.Rect(
        0, 0,
        _image_size[0],
        _image_size[1],
    )
    image_rect.center = (card_rect.centerx, _viewport.top + image_rect.height // 2 + 6)
    cover_rect = _draw_cover(surf, game, image_rect, focus)

    if focus < 0.97:
        return None

    title = _font_title.render(game["name"], True, _INK)
    title.set_alpha(round(255 * focus))
    surf.blit(title, title.get_rect(centerx=card_rect.centerx, top=cover_rect.bottom + 18))

    description_lines = _wrap_text(
        game["desc"], _font_body, _card_width - 30
    )
    description_y = cover_rect.bottom + 18 + title.get_height() + 8
    for line_index, line in enumerate(description_lines[:2]):
        description = _font_body.render(line, True, _MUTED)
        description.set_alpha(round(255 * focus))
        surf.blit(
            description,
            description.get_rect(
                centerx=card_rect.centerx,
                top=description_y + line_index * (_font_body.get_linesize() + 3),
            ),
        )

    play_rect = _play_rect(card_rect, game, focus)
    button = pygame.Surface(play_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(
        button,
        (*game["color"], round(255 * focus)),
        button.get_rect(),
        border_radius=play_rect.height // 2,
    )
    surf.blit(button, play_rect)

    label = _font_button.render("PLAY", True, (255, 255, 255))
    surf.blit(label, label.get_rect(center=play_rect.center))

    return play_rect


def _wrap_text(text, font, max_width):
    lines = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and font.size(candidate)[0] > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw(surf):
    global _scroll

    if not _dragging:
        _scroll += (_target_scroll - _scroll) * 0.16
        if abs(_target_scroll - _scroll) < 0.5:
            _scroll = _target_scroll

    surf.blit(_background, (0, 0))

    eyebrow = _font_label.render("CHOOSE YOUR NEXT CHALLENGE", True, _ACCENT)
    surf.blit(eyebrow, eyebrow.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.075))))

    title = _font_title.render("Mini-games", True, _INK)
    surf.blit(title, title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.125))))

    hint = _font_label.render("SWIPE OR DRAG TO BROWSE", True, _MUTED)
    surf.blit(hint, hint.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.17))))

    old_clip = surf.get_clip()
    surf.set_clip(_viewport)
    for index in range(len(_games)):
        rect = _card_rect(index)
        if rect.right < _viewport.left or rect.left > _viewport.right:
            continue
        _draw_card(surf, index)
    surf.set_clip(old_clip)

    _draw_pagination(surf)
    _draw_close(surf)


def _draw_pagination(surf):
    label = _font_label.render(
        f"{_active_index() + 1:02d}  /  {len(_games):02d}",
        True,
        _MUTED,
    )
    surf.blit(
        label,
        label.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.91))),
    )
    dot_y = int(HEIGHT * 0.955)
    spacing = max(18, int(HEIGHT * 0.028))
    start_x = WIDTH // 2 - (len(_games) - 1) * spacing // 2
    for index in range(len(_games)):
        active = index == _active_index()
        pygame.draw.circle(
            surf,
            _ACCENT if active else (255, 255, 255, 100),
            (start_x + index * spacing, dot_y),
            5 if active else 4,
        )


def _draw_close(surf):
    surf.blit(_close_image, _close_rect)
