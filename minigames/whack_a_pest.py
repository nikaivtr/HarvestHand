"""Five-level, touch-friendly Whack-a-Pest garden defense game."""

from collections import deque
import math
import random
import time

import pygame

import config


WIDTH = HEIGHT = 0
_go_to_scene = None
_success_callback = None
_success_action_label = "MAIN MENU"
_background = None
_sprites = {}
_fonts = {}
_state = "ready"
_level = 1
_score = 0
_plants = set()
_pests = []
_next_pest_id = 0
_eliminations = 0
_level5_eliminations = 0
_invalid_actions = 0
_plants_lost = 0
_level_started = 0.0
_next_spawn = 0.0
_next_kill_window = 0.0
_kills_in_window = 0
_swarm_triggered = False
_swarm_pending = 0
_splats = []
_tile_rects = []
_buttons = {}
_message = ""
_message_until = 0.0

COLS = 5
ROWS = 3
LEVEL_DURATION = 10
TARGET_SCORE = 20_000
LEVEL_SPLAT_REWARDS = (75, 150, 225, 275, 700)
INVALID_PENALTY = 25
PLANT_LOSS_PENALTY = 50
LEVELS = (
    {"name": "Garden Patrol", "move": 3.0, "spawn": (1.8, 0.9), "batch": (1, 1), "limit": 5, "types": ("beetle",)},
    {"name": "Growing Threat", "move": 2.6, "spawn": (1.5, 0.8), "batch": (1, 2), "limit": 6, "types": ("beetle", "worm")},
    {"name": "Pest Invasion", "move": 2.2, "spawn": (1.2, 0.7), "batch": (1, 2), "limit": 7, "types": ("beetle", "worm", "spider", "fly")},
    {"name": "Last Harvest", "move": 1.8, "spawn": (1.0, 0.6), "batch": (1, 3), "limit": 8, "types": ("beetle", "worm", "spider", "rat", "fly")},
)
MADNESS_START_SPAWN = 0.65
MADNESS_MIN_SPAWN = 0.15
MADNESS_SPAWN_RAMP_PER_SECOND = 0.01
MADNESS_START_LIMIT = 12
MADNESS_LIMIT_STEP_SECONDS = 25
MADNESS_MAX_EXTRA_PESTS = 8
MADNESS_BATCH_START = (2, 3)
MADNESS_BATCH_GROWTH_SECONDS = 15
MADNESS_BATCH_MAX = 7
MADNESS_MOVE_INTERVAL = 0.75
MADNESS_MIN_MOVE_INTERVAL = 0.6
MADNESS_MOVE_RAMP_PER_SECOND = 0.003
MADNESS_SWARM_SIZE = 6
SPLAT_DURATION = 0.55
PLANT_TILES = {(2, 0), (2, 2), (2, 4), (1, 1), (1, 3)}
_PEST_DATA = {
    "beetle": {"rect": pygame.Rect(26, 744, 207, 199), "multiplier": 1.0, "splat": "bug_splat"},
    "worm": {"rect": pygame.Rect(1043, 510, 176, 156), "multiplier": 0.85, "splat": "mud_splat"},
    "spider": {"rect": pygame.Rect(22, 513, 224, 211), "multiplier": 1.15, "splat": "goo_splat"},
    "rat": {"rect": pygame.Rect(522, 515, 203, 202), "multiplier": 1.25, "splat": "mud_splat"},
    "fly": {"rect": pygame.Rect(492, 746, 274, 239), "multiplier": 0.7, "splat": "goo_splat"},
}
_PLANT_DATA = (
    pygame.Rect(15, 45, 251, 231),
    pygame.Rect(292, 48, 171, 204),
    pygame.Rect(295, 281, 183, 207),
    pygame.Rect(941, 281, 300, 208),
    pygame.Rect(790, 43, 139, 211),
)
_SPLAT_DATA = {
    "bug_splat": pygame.Rect(15, 985, 275, 222),
    "mud_splat": pygame.Rect(324, 990, 293, 207),
    "goo_splat": pygame.Rect(642, 1003, 274, 185),
}
_PALETTE = {
    "cream": (255, 247, 223),
    "green": (48, 117, 62),
    "red": (165, 58, 43),
    "panel": (35, 51, 34, 220),
}


def init(width, height, go_to_scene_callback):
    global WIDTH, HEIGHT, _go_to_scene, _background, _sprites, _fonts

    WIDTH, HEIGHT = width, height
    _go_to_scene = go_to_scene_callback
    background = pygame.image.load(
        f"{config.IMG_DIR}minigames/whackapestgamebg.jpg"
    ).convert()
    _background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))
    spritesheet = pygame.image.load(
        f"{config.IMG_DIR}minigames/Vegetable and Creature Sprite Sheet.png"
    ).convert()
    _sprites = {
        name: _extract_sprite(spritesheet, data["rect"])
        for name, data in _PEST_DATA.items()
    }
    _plants = [
        _extract_sprite(spritesheet, rect) for rect in _PLANT_DATA
    ]
    _sprites["plants"] = _plants
    _sprites["splats"] = {
        name: _extract_sprite(spritesheet, rect)
        for name, rect in _SPLAT_DATA.items()
    }
    _fonts = {
        "title": _make_font(0.052),
        "large": _make_font(0.039),
        "body": _make_font(0.027),
        "small": _make_font(0.021),
    }
    _layout()


def set_return_callback(callback, success_action_label="MAIN MENU"):
    """Set where a winning player goes and the matching result-button label."""
    global _go_to_scene, _success_callback, _success_action_label
    _go_to_scene = callback
    _success_callback = callback
    _success_action_label = success_action_label


def _make_font(fraction):
    size = max(14, int(HEIGHT * fraction))
    try:
        return pygame.font.Font("fonts/RumRaisin-Regular.ttf", size)
    except pygame.error:
        return pygame.font.SysFont("Georgia", size, bold=True)


def _extract_sprite(sheet, source_rect):
    source = sheet.subsurface(source_rect)
    sprite = pygame.Surface(source_rect.size, pygame.SRCALPHA)
    exterior = bytearray(source_rect.w * source_rect.h)
    queue = deque()

    def is_matte(x, y):
        color = source.get_at((x, y))
        return (
            min(color.r, color.g, color.b) > 205
            and max(color.r, color.g, color.b) - min(color.r, color.g, color.b) < 38
        )

    for x in range(source_rect.w):
        if is_matte(x, 0):
            queue.append((x, 0))
        if is_matte(x, source_rect.h - 1):
            queue.append((x, source_rect.h - 1))
    for y in range(source_rect.h):
        if is_matte(0, y):
            queue.append((0, y))
        if is_matte(source_rect.w - 1, y):
            queue.append((source_rect.w - 1, y))

    while queue:
        x, y = queue.popleft()
        index = y * source_rect.w + x
        if exterior[index] or not is_matte(x, y):
            continue
        exterior[index] = 1
        if x > 0:
            queue.append((x - 1, y))
        if x + 1 < source_rect.w:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y + 1 < source_rect.h:
            queue.append((x, y + 1))

    for y in range(source_rect.h):
        for x in range(source_rect.w):
            color = source.get_at((x, y))
            alpha = 0 if exterior[y * source_rect.w + x] else 255
            sprite.set_at((x, y), (color.r, color.g, color.b, alpha))
    bounds = sprite.get_bounding_rect(min_alpha=1)
    return sprite.subsurface(bounds).copy() if bounds.width and bounds.height else sprite


def _scale_sprite(sprite, size):
    scale = min(size[0] / sprite.get_width(), size[1] / sprite.get_height())
    fitted_size = (
        max(1, round(sprite.get_width() * scale)),
        max(1, round(sprite.get_height() * scale)),
    )
    return pygame.transform.smoothscale(sprite, fitted_size)


def _layout():
    global _tile_rects, _buttons
    left, top = round(WIDTH * 0.094), round(HEIGHT * 0.12)
    board_width, board_height = round(WIDTH * 0.815), round(HEIGHT * 0.65)
    tile_width, tile_height = board_width / COLS, board_height / ROWS
    _tile_rects = [
        pygame.Rect(
            round(left + col * tile_width),
            round(top + row * tile_height),
            round(tile_width),
            round(tile_height),
        )
        for row in range(ROWS)
        for col in range(COLS)
    ]
    button_w = max(112, round(WIDTH * 0.13))
    button_h = max(44, round(HEIGHT * 0.07))
    _buttons = {
        "menu": pygame.Rect(round(WIDTH * 0.025), round(HEIGHT * 0.025), button_w, button_h),
        "restart": pygame.Rect(WIDTH - round(WIDTH * 0.025) - button_w, round(HEIGHT * 0.025), button_w, button_h),
        "next": pygame.Rect(WIDTH // 2 - button_w - 12, round(HEIGHT * 0.67), button_w, button_h),
        "retry": pygame.Rect(WIDTH // 2 - button_w - 12, round(HEIGHT * 0.67), button_w, button_h),
        "result_menu": pygame.Rect(WIDTH // 2 + 12, round(HEIGHT * 0.67), button_w, button_h),
    }


def start():
    global _state, _level, _score, _eliminations, _invalid_actions, _plants_lost
    global _level5_eliminations
    global _plants, _pests, _splats, _next_pest_id, _message, _message_until
    _level = 1
    _score = _eliminations = _invalid_actions = _plants_lost = 0
    _level5_eliminations = 0
    _plants = set(PLANT_TILES)
    _pests = []
    _splats = []
    _next_pest_id = 0
    _message = ""
    _message_until = 0.0
    _start_level()


def _start_level():
    global _state, _level_started, _next_spawn, _next_kill_window
    global _kills_in_window, _swarm_triggered, _swarm_pending, _pests
    global _level5_eliminations
    now = time.monotonic()
    _state = "playing"
    _level_started = now
    if _level == 5:
        _level5_eliminations = 0
    _next_spawn = now + _spawn_interval(now)
    _next_kill_window = now + 1.0
    _kills_in_window = 0
    _swarm_triggered = False
    _swarm_pending = 0
    _pests = []
    _spawn_pest(now)


def _spawn_interval(now):
    if _level < 5:
        start, end = LEVELS[_level - 1]["spawn"]
        progress = min(1.0, max(0.0, (now - _level_started) / LEVEL_DURATION))
        return start + (end - start) * progress
    elapsed = max(0.0, now - _level_started)
    return max(
        MADNESS_MIN_SPAWN,
        MADNESS_START_SPAWN - elapsed * MADNESS_SPAWN_RAMP_PER_SECOND,
    )


def _spawn_batch_size(now):
    progress = min(1.0, max(0.0, (now - _level_started) / LEVEL_DURATION))
    if _level < 5:
        low, high = LEVELS[_level - 1]["batch"]
        highest = low + round((high - low) * progress)
        return random.randint(low, max(low, highest))
    elapsed = max(0.0, now - _level_started)
    batch_growth = int(elapsed // MADNESS_BATCH_GROWTH_SECONDS)
    low = min(MADNESS_BATCH_MAX, MADNESS_BATCH_START[0] + batch_growth)
    high = min(MADNESS_BATCH_MAX, MADNESS_BATCH_START[1] + batch_growth)
    return random.randint(low, high)


def _active_limit(now):
    if _level < 5:
        return LEVELS[_level - 1]["limit"]
    extra = min(
        MADNESS_MAX_EXTRA_PESTS,
        int(max(0.0, now - _level_started) // MADNESS_LIMIT_STEP_SECONDS),
    )
    return MADNESS_START_LIMIT + extra


def _check_victory():
    global _state
    if _level != 5 or not _plants or _level5_eliminations == 0:
        return
    if _score >= TARGET_SCORE:
        _state = "victory"


def _spawn_pest(now):
    global _next_pest_id
    occupied = {pest["pos"] for pest in _pests}
    candidates = [
        (row, col)
        for row in range(ROWS)
        for col in range(COLS)
        if (row, col) not in occupied and (row, col) not in _plants
        and _path_to_plant((row, col), occupied) is not None
    ]
    if not candidates:
        return False
    position = random.choice(candidates)
    pest_type = random.choice(
        LEVELS[_level - 1]["types"] if _level < 5 else tuple(_PEST_DATA)
    )
    if _level < 5:
        base_interval = LEVELS[_level - 1]["move"]
    else:
        elapsed = max(0.0, now - _level_started)
        base_interval = max(
            MADNESS_MIN_MOVE_INTERVAL,
            MADNESS_MOVE_INTERVAL - elapsed * MADNESS_MOVE_RAMP_PER_SECOND,
        )
    interval = base_interval * _PEST_DATA[pest_type]["multiplier"]
    _pests.append({
        "id": _next_pest_id,
        "pos": position,
        "type": pest_type,
        "interval": interval,
        "next_move": now + interval,
        "alive": True,
    })
    _next_pest_id += 1
    return True


def _path_to_plant(start, occupied):
    queue = deque([(start, [])])
    visited = {start}
    while queue:
        position, path = queue.popleft()
        if position in _plants:
            return path
        row, col = position
        for neighbor in ((row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)):
            nr, nc = neighbor
            if not (0 <= nr < ROWS and 0 <= nc < COLS) or neighbor in visited:
                continue
            if neighbor in occupied:
                continue
            visited.add(neighbor)
            queue.append((neighbor, path + [neighbor]))
    return None


def _move_pests(now):
    global _pests, _score, _plants_lost, _state, _message, _message_until
    occupied = {pest["pos"] for pest in _pests if pest["alive"]}
    due = sorted(
        (pest for pest in _pests if pest["alive"] and pest["next_move"] <= now),
        key=lambda pest: (pest["next_move"], pest["id"]),
    )
    for pest in due:
        occupied.discard(pest["pos"])
        path = _path_to_plant(pest["pos"], occupied)
        if path:
            pest["pos"] = path[0]
            if pest["pos"] in _plants:
                _plants.remove(pest["pos"])
                _plants_lost += 1
                _score = max(0, _score - PLANT_LOSS_PENALTY)
                pest["alive"] = False
                _message = "A crop was eaten!"
                _message_until = now + 1.2
            else:
                occupied.add(pest["pos"])
        pest["next_move"] += pest["interval"]
    _pests = [pest for pest in _pests if pest["alive"]]
    if not _plants:
        _state = "defeat"


def _update(now):
    global _state, _level, _next_spawn, _next_kill_window
    global _pests, _splats, _kills_in_window, _swarm_triggered, _swarm_pending
    global _message, _message_until
    if _state != "playing":
        return

    if _level < 5 and now - _level_started >= LEVEL_DURATION:
        _pests = []
        _state = "transition"
        return

    _move_pests(now)
    if _state != "playing":
        return

    while _swarm_pending and len(_pests) < _active_limit(now):
        if not _spawn_pest(now):
            break
        _swarm_pending -= 1

    while now >= _next_kill_window:
        _kills_in_window = 0
        _swarm_triggered = False
        _next_kill_window += 1.0

    while now >= _next_spawn:
        for _ in range(_spawn_batch_size(_next_spawn)):
            if len(_pests) >= _active_limit(_next_spawn):
                break
            _spawn_pest(_next_spawn)
        _next_spawn += _spawn_interval(_next_spawn)
    _splats = [splat for splat in _splats if now - splat["born"] < SPLAT_DURATION]

    _check_victory()


def handle_tap(px, py):
    global _state, _level, _score, _eliminations, _invalid_actions
    global _level5_eliminations
    global _pests, _kills_in_window, _swarm_triggered, _swarm_pending
    global _splats, _message, _message_until
    now = time.monotonic()
    _update(now)
    if _state in ("victory", "defeat"):
        if _buttons["retry"].collidepoint(px, py):
            start()
        elif _buttons["result_menu"].collidepoint(px, py):
            if _state == "victory" and _success_callback is not None:
                _success_callback("main_menu")
            else:
                _go_to_scene("main_menu")
        return
    if _state == "transition":
        if _buttons["next"].collidepoint(px, py):
            _level += 1
            _start_level()
        elif _buttons["menu"].collidepoint(px, py) or _buttons["result_menu"].collidepoint(px, py):
            _go_to_scene("main_menu")
        return
    if _buttons["menu"].collidepoint(px, py):
        _go_to_scene("main_menu")
        return
    if _buttons["restart"].collidepoint(px, py):
        start()
        return
    if _state != "playing":
        return

    selected_tile = None
    for tile_index, rect in enumerate(_tile_rects):
        if rect.collidepoint(px, py):
            selected_tile = divmod(tile_index, COLS)
            break
    if selected_tile is None:
        _invalid_actions += 1
        _score = max(0, _score - INVALID_PENALTY)
        _message = f"-{INVALID_PENALTY}: tap a pest"
        _message_until = now + 0.8
        return
    pest = next((item for item in reversed(_pests) if item["pos"] == selected_tile and item["alive"]), None)
    if pest is None:
        _invalid_actions += 1
        _score = max(0, _score - INVALID_PENALTY)
        _message = f"-{INVALID_PENALTY}: empty tile"
        _message_until = now + 0.8
        return

    pest["alive"] = False
    _pests = [item for item in _pests if item["alive"]]
    _eliminations += 1
    if _level == 5:
        _level5_eliminations += 1
    pest_data = _PEST_DATA[pest["type"]]
    points = LEVEL_SPLAT_REWARDS[_level - 1]
    _score = min(TARGET_SCORE, _score + points)
    _add_splat(selected_tile, pest_data["splat"], now)
    if _level == 5:
        _kills_in_window += 1
        if _kills_in_window >= 5 and not _swarm_triggered:
            _swarm_triggered = True
            _swarm_pending += MADNESS_SWARM_SIZE + min(
                6, int(max(0.0, now - _level_started) // 30)
            )
            while _swarm_pending and len(_pests) < _active_limit(now):
                if not _spawn_pest(now):
                    break
                _swarm_pending -= 1
            _message = "SWARM ALERT!"
            _message_until = now + 1.2
        else:
            _message = f"+{points}"
            _message_until = now + 0.65
    else:
        _message = f"+{points}"
        _message_until = now + 0.65
    _check_victory()


def handle_release(_px, _py):
    pass


def _add_splat(position, sprite_name, now):
    colors = {
        "bug_splat": (119, 216, 39),
        "mud_splat": (141, 91, 47),
        "goo_splat": (108, 210, 53),
    }
    particles = []
    for _ in range(9):
        particles.append((
            random.uniform(0.0, math.tau),
            random.uniform(28.0, 100.0),
            random.randint(3, 7),
        ))
    _splats.append({
        "pos": position,
        "sprite": sprite_name,
        "born": now,
        "angle": random.uniform(-18.0, 18.0),
        "particles": particles,
        "color": colors[sprite_name],
    })


def _tile_center(position):
    return _tile_rects[position[0] * COLS + position[1]].center


def _draw_text(surface, text, font, color, center, shadow=True):
    image = font.render(text, True, color)
    if shadow:
        shadow_image = font.render(text, True, (25, 29, 21))
        surface.blit(shadow_image, shadow_image.get_rect(center=(center[0] + 2, center[1] + 2)))
    surface.blit(image, image.get_rect(center=center))


def _draw_button(surface, key, label, color):
    rect = _buttons[key]
    pygame.draw.rect(surface, (27, 36, 25), rect.move(0, 4), border_radius=14)
    pygame.draw.rect(surface, color, rect, border_radius=14)
    pygame.draw.rect(surface, (255, 230, 171), rect, 2, border_radius=14)
    _draw_text(surface, label, _fonts["small"], _PALETTE["cream"], rect.center)


def _draw_hud(surface, now):
    panel = pygame.Rect(round(WIDTH * 0.19), round(HEIGHT * 0.015), round(WIDTH * 0.62), round(HEIGHT * 0.115))
    pygame.draw.rect(surface, _PALETTE["panel"], panel, border_radius=18)
    pygame.draw.rect(surface, (233, 200, 139), panel, 2, border_radius=18)
    title = f"LEVEL {_level}  -  {LEVELS[_level - 1]['name']}" if _level < 5 else "LEVEL 5  -  MADNESS MODE"
    _draw_text(surface, title, _fonts["large"], _PALETTE["cream"], (panel.centerx, panel.top + panel.h // 3))
    details = f"SCORE  {_score:,} / {TARGET_SCORE}       CROPS  {len(_plants)}"
    if _level < 5:
        remaining = max(0, LEVEL_DURATION - (now - _level_started))
        details += f"       TIME  {int(remaining):02d}s"
    else:
        details += f"       PESTS  {len(_pests)}"
    _draw_text(surface, details, _fonts["body"], (255, 229, 167), (panel.centerx, panel.top + panel.h * 0.73))
    if _level < 5:
        bar = pygame.Rect(panel.left + 18, panel.bottom - 7, panel.width - 36, 5)
        pygame.draw.rect(surface, (71, 74, 52), bar, border_radius=3)
        ratio = max(0.0, min(1.0, 1.0 - (now - _level_started) / LEVEL_DURATION))
        fill = bar.copy()
        fill.width = round(bar.width * ratio)
        pygame.draw.rect(surface, (237, 185, 72), fill, border_radius=3)
    _draw_button(surface, "menu", "MENU", _PALETTE["green"])
    _draw_button(surface, "restart", "RESTART", _PALETTE["red"])


def _draw_board(surface, now):
    for row in range(ROWS):
        for col in range(COLS):
            position = (row, col)
            rect = _tile_rects[row * COLS + col]
            if position in _plants:
                index = PLANT_TILES_ORDER.index(position)
                sprite = _sprites["plants"][index % len(_sprites["plants"])]
                image = _scale_sprite(sprite, (int(rect.w * 0.58), int(rect.h * 0.64)))
                surface.blit(image, image.get_rect(center=(rect.centerx, rect.centery + int(rect.h * 0.05))))
            pest = next((item for item in _pests if item["pos"] == position and item["alive"]), None)
            if pest is not None:
                sprite = _sprites[pest["type"]]
                size = (int(rect.w * 0.60), int(rect.h * 0.66))
                image = _scale_sprite(sprite, size)
                surface.blit(image, image.get_rect(center=(rect.centerx, rect.centery)))
                if pest["next_move"] - now < 0.45:
                    pygame.draw.circle(surface, (245, 83, 45), (rect.right - 18, rect.top + 18), 8)
    for splat in _splats:
        elapsed = now - splat["born"]
        progress = min(1.0, max(0.0, elapsed / SPLAT_DURATION))
        tile = _tile_rects[splat["pos"][0] * COLS + splat["pos"][1]]
        max_size = (int(tile.w * 0.76), int(tile.h * 0.76))
        size = (
            max(1, round(max_size[0] * (0.5 + 0.5 * progress))),
            max(1, round(max_size[1] * (0.5 + 0.5 * progress))),
        )
        image = _scale_sprite(_sprites["splats"][splat["sprite"]], size)
        image = pygame.transform.rotate(image, splat["angle"])
        image.set_alpha(round(255 * (1.0 - progress)))
        surface.blit(image, image.get_rect(center=tile.center))
        for angle, speed, radius in splat["particles"]:
            distance = speed * elapsed
            center = (
                round(tile.centerx + math.cos(angle) * distance),
                round(tile.centery + math.sin(angle) * distance),
            )
            particle_radius = max(1, round(radius * (1.0 - progress)))
            pygame.draw.circle(surface, splat["color"], center, particle_radius)
    if _message and now < _message_until:
        _draw_text(surface, _message, _fonts["body"], (255, 236, 184), (WIDTH // 2, int(HEIGHT * 0.91)))
    instruction = (
        "TAP PESTS  |  5 QUICK KILLS TRIGGER A SWARM"
        if _level == 5 else         f"TAP PESTS TO PROTECT THE CROPS  |  EMPTY TAPS COST {INVALID_PENALTY}"
    )
    _draw_text(
        surface,
        instruction,
        _fonts["small"],
        _PALETTE["cream"],
        (WIDTH // 2, int(HEIGHT * 0.965)),
    )


def _draw_result(surface, title, subtitle, action_label, action_key="retry"):
    veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    veil.fill((20, 28, 20, 175))
    surface.blit(veil, (0, 0))
    panel = pygame.Rect(int(WIDTH * 0.18), int(HEIGHT * 0.27), int(WIDTH * 0.64), int(HEIGHT * 0.48))
    pygame.draw.rect(surface, (57, 65, 40), panel, border_radius=28)
    pygame.draw.rect(surface, (241, 204, 127), panel, 3, border_radius=28)
    _draw_text(surface, title, _fonts["title"], _PALETTE["cream"], (panel.centerx, panel.top + panel.h * 0.23))
    _draw_text(surface, subtitle, _fonts["body"], (255, 226, 161), (panel.centerx, panel.top + panel.h * 0.43))
    stats = f"Eliminated {_eliminations}   |   Misses {_invalid_actions}   |   Crops lost {_plants_lost}"
    _draw_text(surface, stats, _fonts["small"], _PALETTE["cream"], (panel.centerx, panel.top + panel.h * 0.59))
    _draw_button(surface, action_key, action_label, _PALETTE["green"])
    result_menu_label = (
        _success_action_label if _state == "victory" else "MAIN MENU"
    )
    _draw_button(surface, "result_menu", result_menu_label, _PALETTE["red"])


PLANT_TILES_ORDER = tuple(sorted(PLANT_TILES))


def draw(surface):
    now = time.monotonic()
    _update(now)
    surface.blit(_background, (0, 0))
    _draw_hud(surface, now)
    _draw_board(surface, now)
    if _state == "transition":
        _draw_result(
            surface,
            f"Level {_level} complete!",
            f"Score {_score:,}   |   {len(_plants)} crops remain",
            "CONTINUE",
            action_key="next",
        )
    elif _state == "victory":
        _draw_result(
            surface,
            "Harvest protected!",
            f"Final score: {_score:,}",
            "PLAY AGAIN",
        )
    elif _state == "defeat":
        _draw_result(surface, "The pests got the garden!", f"Final score: {_score:,}", "TRY AGAIN")
