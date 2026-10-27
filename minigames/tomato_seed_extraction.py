"""Tomato slicing and seed extraction mini-game."""
import os
import math
import random
import time

import pygame

WIDTH = HEIGHT = 0
_go_to_scene = None
_return_callback = None
_return_label = "MAIN MENU"
_success_callback = None
_success_label = "CONTINUE"
_background = None
_fonts = {}
_sprites = {}
_raw_sprites = {}

SPRITE_DIR = os.path.join("assets", "minigames", "tomato_seed_extraction", "sprites")
BG_PATH = os.path.join("assets", "minigames", "tomato_seed_extraction", "background.png")

SEED_COUNT = 10
SLICE_HOLD_TIME = 0.6

_PALETTE = {
    "ink": (40, 30, 20),
    "cream": (255, 247, 223),
    "green": (48, 117, 62),
    "red": (165, 58, 43),
    "gold": (248, 188, 64),
}

_state = "slicing"
_stage_timer = 0.0
_last_ticks = 0.0

_ptr = (0, 0)
_ptr_down = False

_tomato_rect = None
_tray_rect = None
_knife_dragging = False
_slice_start = None
_sliced = False
_slice_anim_t = 0.0

_seeds = []
_active_seed = None
_extracting = False
_drag_offset = (0, 0)
_drag_distance = 0.0
_remaining = SEED_COUNT
_total_seeds = SEED_COUNT

_buttons = {}


def _make_font(size_fraction):
    size = max(16, int(HEIGHT * size_fraction))
    try:
        return pygame.font.Font("fonts/RumRaisin-Regular.ttf", size)
    except pygame.error:
        return pygame.font.SysFont("Georgia", size, bold=True)


def _load_sprite(name):
    path = os.path.join(SPRITE_DIR, name)
    return pygame.image.load(path).convert_alpha()


def _sprite(name, size=None):
    if name not in _raw_sprites:
        _raw_sprites[name] = _load_sprite(name)
    img = _raw_sprites[name]
    if size:
        key = (name, size)
        if key not in _sprites:
            scale = min(size[0] / img.get_width(), size[1] / img.get_height())
            scaled_size = (
                max(1, round(img.get_width() * scale)),
                max(1, round(img.get_height() * scale)),
            )
            scaled = pygame.transform.smoothscale(img, scaled_size)
            fitted = pygame.Surface(size, pygame.SRCALPHA)
            fitted.blit(scaled, scaled.get_rect(center=fitted.get_rect().center))
            _sprites[key] = fitted
        return _sprites[key]
    return img


def init(width, height, go_to_scene_callback):
    global WIDTH, HEIGHT, _go_to_scene, _background, _fonts
    global _tomato_rect, _tray_rect, _last_ticks

    WIDTH, HEIGHT = width, height
    _go_to_scene = go_to_scene_callback

    try:
        bg = pygame.image.load(BG_PATH).convert()
        _background = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))
    except pygame.error:
        _background = None

    _fonts = {
        "title": _make_font(0.05),
        "body": _make_font(0.03),
        "small": _make_font(0.022),
    }

    ts = int(min(WIDTH, HEIGHT) * 0.38)
    _tomato_rect = pygame.Rect(0, 0, ts, ts)
    _tomato_rect.center = (WIDTH // 2, int(HEIGHT * 0.42))
    tray_width = int(WIDTH * 0.19)
    tray_height = int(HEIGHT * 0.11)
    _tray_rect = pygame.Rect(0, 0, tray_width, tray_height)
    _tray_rect.center = (int(WIDTH * 0.75), int(HEIGHT * 0.78))

    _last_ticks = time.monotonic()
    reset_game()


def reset_game():
    global _state, _stage_timer, _ptr, _ptr_down
    global _knife_dragging, _slice_start, _sliced, _slice_anim_t
    global _seeds, _active_seed, _extracting
    global _drag_offset, _drag_distance
    global _remaining, _total_seeds

    _state = "slicing"
    _stage_timer = 0.0
    scale = min(WIDTH, HEIGHT)
    _ptr = (
        min(WIDTH - 1, _tomato_rect.right + int(scale * 0.18)),
        min(HEIGHT - 1, _tomato_rect.centery + int(scale * 0.16)),
    )
    _ptr_down = False

    _knife_dragging = False
    _slice_start = None
    _sliced = False
    _slice_anim_t = 0.0

    _total_seeds = SEED_COUNT
    _remaining = SEED_COUNT
    _seeds = _make_seeds()
    _active_seed = None
    _extracting = False
    _drag_offset = (0, 0)
    _drag_distance = 0.0


def _make_seeds():
    seeds = []
    cx, cy = _tomato_rect.center
    r = _tomato_rect.width * 0.30
    for i in range(SEED_COUNT):
        ang = (i / SEED_COUNT) * math.pi * 2 + random.uniform(-0.2, 0.2)
        rr = r * random.uniform(0.35, 0.78)
        x = cx + math.cos(ang) * rr
        y = cy + math.sin(ang) * rr * 0.85
        seeds.append({
            "pos": (x, y),
            "origin": (x, y),
            "state": "in_tomato",
            "progress": 0.0,
        })
    return seeds


def set_return_callback(callback, label):
    global _return_callback, _return_label
    _return_callback = callback
    _return_label = label


def set_success_action(callback, label):
    global _success_callback, _success_label
    _success_callback = callback
    _success_label = label


def start():
    reset_game()


def _button_rects():
    global _buttons
    _buttons = {}
    if _state in ("success", "failure"):
        w = int(WIDTH * 0.26)
        h = int(HEIGHT * 0.07)
        gap = int(WIDTH * 0.03)
        cx = WIDTH // 2
        y = int(HEIGHT * 0.78)
        _buttons["primary"] = pygame.Rect(cx - w // 2, y, w, h)
    return _buttons

def handle_tap(x, y):
    global _ptr, _ptr_down, _knife_dragging, _slice_start, _state
    global _extracting, _active_seed, _drag_offset, _drag_distance

    if _state in ("success", "failure"):
        rects = _button_rects()
        if rects["primary"].collidepoint(x, y):
            if _state == "success":
                if _success_callback:
                    _success_callback(_success_label)
                else:
                    reset_game()
            else:
                reset_game()
            return
        return

    if _state == "slicing":
        _ptr = (x, y)
        if _tomato_rect.collidepoint(x, y):
            _ptr_down = True
            _knife_dragging = True
            _slice_start = (x, y)
        return

    if _state == "extraction":
        for s in _seeds:
            if s is _active_seed:
                continue
            if s["state"] != "in_tomato":
                continue
            sx, sy = s["origin"]
            hit_radius = max(22, int(min(WIDTH, HEIGHT) * 0.035))
            if math.hypot(x - sx, y - sy) < hit_radius:
                if _active_seed is not None:
                    _state = "failure"
                    _ptr_down = False
                    _extracting = False
                    return
                _ptr = (x, y)
                _active_seed = s
                _extracting = True
                _drag_offset = (sx - x, sy - y)
                _drag_distance = 0.0
                _ptr_down = True
                s["state"] = "grabbed"
                return


def handle_additional_tap(x, y):
    global _state, _ptr_down, _extracting

    if _state != "extraction" or _active_seed is None:
        return

    hit_radius = max(22, int(min(WIDTH, HEIGHT) * 0.035))
    for seed in _seeds:
        if seed is _active_seed or seed["state"] != "in_tomato":
            continue
        sx, sy = seed["origin"]
        if math.hypot(x - sx, y - sy) < hit_radius:
            _state = "failure"
            _ptr_down = False
            _extracting = False
            return


def handle_drag(x, y):
    global _ptr, _drag_distance
    if _state == "extraction" and _ptr_down and _active_seed is not None:
        dx = x - _ptr[0]
        dy = y - _ptr[1]
        distance = math.hypot(dx, dy)
        if distance > 0:
            _drag_distance += distance
            _active_seed["pos"] = (x + _drag_offset[0], y + _drag_offset[1])
    _ptr = (x, y)


def handle_release(x, y):
    global _ptr, _ptr_down, _knife_dragging, _slice_start
    global _active_seed, _extracting, _remaining, _state
    global _drag_distance

    if (
        _state == "extraction"
        and _ptr_down
        and _active_seed is not None
        and math.hypot(x - _ptr[0], y - _ptr[1]) > 0
    ):
        handle_drag(x, y)
    _ptr = (x, y)
    _ptr_down = False

    if _state == "slicing":
        _knife_dragging = False
        _slice_start = None
        return
    if _state == "extraction" and _active_seed is not None:
        if (
            _tray_rect.collidepoint(_active_seed["pos"])
            and _drag_distance >= 12
        ):
            slot = _total_seeds - _remaining
            column = slot % 5
            row = slot // 5
            _active_seed["pos"] = (
                _tray_rect.centerx + (column - 2) * int(min(WIDTH, HEIGHT) * 0.045),
                _tray_rect.centery + (row - 0.5) * int(min(WIDTH, HEIGHT) * 0.035),
            )
            _active_seed["state"] = "extracted"
            _remaining = max(0, _remaining - 1)
            if _remaining == 0:
                _state = "success"
        else:
            _active_seed["state"] = "in_tomato"
            _active_seed["pos"] = _active_seed["origin"]
        _active_seed = None
        _extracting = False
        _drag_distance = 0.0


def _update(dt):
    global _state, _slice_anim_t
    global _knife_dragging, _slice_start, _sliced
    dt = min(max(dt, 0.0), 0.1)

    if _state == "slicing":
        if _knife_dragging and _ptr_down and _slice_start is not None:
            sx, sy = _slice_start
            cx, cy = _ptr
            started_left = sx < _tomato_rect.centerx and _tomato_rect.left <= sx <= _tomato_rect.right
            ended_right = cx > _tomato_rect.centerx and _tomato_rect.left <= cx <= _tomato_rect.right
            started_right = sx > _tomato_rect.centerx and _tomato_rect.left <= sx <= _tomato_rect.right
            ended_left = cx < _tomato_rect.centerx and _tomato_rect.left <= cx <= _tomato_rect.right
            crosses_horiz = (started_left and ended_right) or (started_right and ended_left)
            vert_ok = (
                _tomato_rect.top <= sy <= _tomato_rect.bottom
                and _tomato_rect.top <= cy <= _tomato_rect.bottom
                and abs(cy - sy) < _tomato_rect.height * 0.45
            )
            if crosses_horiz and vert_ok:
                _state = "slicing_anim"
                _slice_anim_t = 0.0
                _knife_dragging = False
        return

    if _state == "slicing_anim":
        _slice_anim_t += dt
        if _slice_anim_t >= SLICE_HOLD_TIME:
            _state = "extraction"
        return

def draw(surface):
    global _last_ticks
    now = time.monotonic()
    dt = now - _last_ticks
    _last_ticks = now
    _update(dt)

    if _background is not None:
        surface.blit(_background, (0, 0))
    else:
        surface.fill((60, 90, 60))

    if _state in ("success", "failure"):
        _draw_result(surface)
        return

    _draw_tomato(surface)
    if _state == "extraction":
        _draw_tray(surface)
    if _state in ("extraction", "success", "failure"):
        _draw_seeds(surface)
    _draw_tool(surface)
    _draw_ui(surface)

def _draw_tomato(surface):
    if _state == "slicing_anim":
        name = "tomato_just_sliced.png"
    elif _state == "slicing" and _knife_dragging:
        name = "tomato_slicing.png"
    elif _state == "slicing":
        name = "tomato_cut_guide.png"
    else:
        name = "tomato_cut_open.png"
    img = _sprite(name, (_tomato_rect.width, _tomato_rect.height))
    surface.blit(img, _tomato_rect)


def _draw_seeds(surface):
    seed_size = max(26, int(min(WIDTH, HEIGHT) * 0.045))
    for s in _seeds:
        sx, sy = s["pos"]
        if s["state"] == "extracted":
            name = "seed_extracted.png"
        elif s is _active_seed and _extracting:
            name = "seed_grabbed.png"
        elif s["state"] == "grabbed":
            name = "seed_grabbed.png"
        else:
            name = "seed_normal.png"
        img = _sprite(name, (seed_size, seed_size))
        surface.blit(img, img.get_rect(center=(int(sx), int(sy))))


def _draw_tray(surface):
    pygame.draw.ellipse(surface, (98, 56, 35), _tray_rect)
    inner = _tray_rect.inflate(-8, -8)
    pygame.draw.ellipse(surface, (222, 164, 83), inner)
    opening = inner.inflate(-18, -22)
    pygame.draw.ellipse(surface, (135, 82, 45), opening)
    pygame.draw.arc(surface, (247, 210, 144), opening, 0, math.pi, 3)
    label = _fonts["small"].render("SEED TRAY", True, (255, 239, 195))
    surface.blit(label, label.get_rect(center=(opening.centerx, _tray_rect.top - 10)))


def _draw_tool(surface):
    scale = min(WIDTH, HEIGHT)
    if _state in ("slicing", "slicing_anim"):
        frames = ("knife_move_01.png", "knife_move_02.png", "knife_move_03.png")
        name = frames[int(time.monotonic() * 12) % len(frames)] if _knife_dragging else "knife_idle.png"
        img = _sprite(name, (int(scale * 0.18), int(scale * 0.24)))
        rect = img.get_rect()
        rect.topright = _ptr
        surface.blit(img, rect)
    else:
        if _active_seed is not None and _extracting:
            name = "tweezers_grabbing.png"
            x, y = _active_seed["pos"]
        else:
            name = "tweezers_idle.png"
            x, y = _ptr
        img = _sprite(name, (int(scale * 0.10), int(scale * 0.17)))
        rect = img.get_rect()
        rect.bottomleft = (int(x), int(y))
        surface.blit(img, rect)


def _draw_ui(surface):
    message = None
    if _state == "slicing":
        message = "Slice across the guide to reveal the seeds!"
    elif _state == "extraction":
        message = "Drag one seed at a time into the tray."

    if message:
        banner = pygame.Rect(
            int(WIDTH * 0.12),
            int(HEIGHT * 0.025),
            int(WIDTH * 0.76),
            max(38, int(HEIGHT * 0.075)),
        )
        panel = pygame.Surface(banner.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, (40, 30, 20, 185), panel.get_rect(), border_radius=12)
        surface.blit(panel, banner)
        txt = _fonts["body"].render(message, True, _PALETTE["cream"])
        surface.blit(txt, txt.get_rect(center=banner.center))

    if _state not in ("slicing", "extraction"):
        return

    counter_y = int(HEIGHT * 0.12)
    seed_icon_size = max(24, int(min(WIDTH, HEIGHT) * 0.04))
    counter = pygame.Rect(
        int(WIDTH * 0.04),
        counter_y - 4,
        int(WIDTH * 0.17),
        seed_icon_size + 8,
    )
    pygame.draw.rect(surface, (255, 247, 223), counter, border_radius=12)
    pygame.draw.rect(surface, (177, 128, 59), counter, width=2, border_radius=12)
    seed_icon = _sprite("seed_normal.png", (seed_icon_size, seed_icon_size))
    surface.blit(seed_icon, (counter.x + 6, counter.y + 4))
    ctext = _fonts["body"].render(f"{_remaining} / {_total_seeds}", True, _PALETTE["ink"])
    surface.blit(ctext, (counter.x + seed_icon_size + 12, counter.centery - ctext.get_height() // 2))

def _draw_result(surface):
    veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    veil.fill((20, 30, 20, 170))
    surface.blit(veil, (0, 0))

    panel = pygame.Rect(int(WIDTH * 0.18), int(HEIGHT * 0.20), int(WIDTH * 0.64), int(HEIGHT * 0.66))
    pygame.draw.rect(surface, (255, 247, 219), panel, border_radius=24)
    pygame.draw.rect(surface, (177, 128, 59), panel, width=4, border_radius=24)

    if _state == "success":
        title = "Seeds Extracted!"
        sub = "Great job preparing the tomato."
        icon_size = int(min(WIDTH, HEIGHT) * 0.16)
        img = _sprite("feedback_success.png", (icon_size, icon_size))
    else:
        title = "One Seed at a Time!"
        sub = "Drop the seed in the tray before picking another."
        icon_size = int(min(WIDTH, HEIGHT) * 0.16)
        img = _sprite("feedback_failure.png", (icon_size, icon_size))

    t = _fonts["title"].render(title, True, _PALETTE["ink"])
    surface.blit(t, t.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.29))))
    s = _fonts["body"].render(sub, True, _PALETTE["ink"])
    surface.blit(s, s.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.39))))
    surface.blit(img, img.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.55))))

    rects = _button_rects()
    pygame.draw.rect(surface, _PALETTE["green"], rects["primary"], border_radius=14)
    plabel = _success_label if _state == "success" else "Retry"
    pt = _fonts["body"].render(plabel, True, (255, 255, 255))
    surface.blit(pt, pt.get_rect(center=rects["primary"].center))
