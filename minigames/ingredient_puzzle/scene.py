"""
Ingredient Jigsaw Challenge — main scene module.

Follows the Harvest Hand scene contract:
  init(width, height, go_to_scene_callback)
  start()
  handle_tap(x, y)
  handle_drag(x, y)
  handle_release(x, y)
  draw(screen)

The mini-game is launched by story_mode when a slide of type
"ingredient_puzzle" is reached. It can also be reached from a menu.
"""

import math
import random
import time

import pygame

from . import assets_config as AC
from .puzzle_engine import generate_puzzle
from .puzzle_piece import PuzzlePiece
from .timer import Timer
from .level_manager import LevelManager
from .results_screen import ResultsScreen

# ── Globals ──────────────────────────────────────────────────────────────
WIDTH = HEIGHT = 0
_go_to_scene = None
_on_complete = None
_success_callback = None
_success_action_label = "Continue Story"

_background = None
_font_title = None
_font_body = None
_font_label = None
_font_timer = None

_level_mgr = None
_timer = None
_results = None
_sidebar_rect = None
_reference_rect = None
_workspace_rect = None
_target_rect = None
_silhouette_surface = None
_current_ingredient = None
_current_pieces = []
_reference_images = {}
_dragging_piece = None
_selected_piece = None
_advance_at = None
_game_score = 0
_message = ""
_message_until = 0.0


def start():
    """Called by story_mode or main menu to begin the mini-game at level 1."""
    global _timer, _game_score
    global _current_ingredient, _current_pieces, _dragging_piece, _selected_piece
    global _message, _message_until, _advance_at

    _level_mgr.start_level(1)
    _game_score = 0
    _timer = Timer(sum(cfg["timer_seconds"] for cfg in AC.LEVELS.values()))
    _timer.start()
    _results.hide()
    _dragging_piece = None
    _selected_piece = None
    _advance_at = None
    _message = ""
    _message_until = 0.0
    _begin_ingredient(0)


def set_success_action(callback, label):
    """Configure the victory action for story or mini-game-menu launches."""
    global _success_callback, _success_action_label
    _success_callback = callback
    _success_action_label = label
    if _results is not None:
        _results.continue_label = label


def _begin_ingredient(ingredient_index):
    """Start solving a single ingredient within the current level."""
    global _current_ingredient, _current_pieces, _dragging_piece
    global _selected_piece, _advance_at, _game_score
    global _silhouette_surface

    cfg = _level_mgr.get_config()
    ing_keys = cfg["ingredients"]
    if ingredient_index >= len(ing_keys):
        if _level_mgr.is_final_level():
            _finish_level()
        else:
            completed_level = _level_mgr.current_level
            _game_score += _level_mgr.complete_level()
            _level_mgr.start_level(completed_level + 1)
            _show_message(f"Level {completed_level} complete!")
            _begin_ingredient(0)
        return

    _current_ingredient = ing_keys[ingredient_index]
    _dragging_piece = None
    _selected_piece = None
    _advance_at = None

    piece_count = cfg["pieces_per_ingredient"]
    target_source_rect = pygame.Rect(0, 0, _target_rect.w, _target_rect.h)
    raw_pieces = generate_puzzle(
        _current_ingredient, piece_count, target_source_rect
    )
    _silhouette_surface = raw_pieces[0]["silhouette_surface"]

    pieces = []
    for i, raw in enumerate(raw_pieces):
        surf = raw["surface"]
        mask = pygame.mask.from_surface(surf, threshold=10)

        correct_pos = (
            _target_rect.x + raw["correct_pos"][0],
            _target_rect.y + raw["correct_pos"][1],
        )

        piece = PuzzlePiece(
            piece_id=f"{_current_ingredient}_{i}",
            surface=surf,
            mask=mask,
            guide_surface=raw["guide_surface"],
            correct_pos=correct_pos,
            correct_angle=0.0,
            index_in_ingredient=i,
            total_pieces=piece_count,
        )
        pieces.append(piece)

    _scatter_pieces(pieces, cfg["rotation"])
    _current_pieces = pieces

_results = None

_current_ingredient = None
_current_pieces = []
_dragging_piece = None

_workspace_rect = None
_target_rect = None
_sidebar_rect = None
_reference_rect = None

_message = ""
_message_until = 0.0

_advance_at = None


def init(width, height, go_to_scene_callback):
    global WIDTH, HEIGHT, _go_to_scene
    global _background, _font_title, _font_body, _font_label, _font_timer
    global _level_mgr, _timer, _results

    WIDTH, HEIGHT = width, height
    _go_to_scene = go_to_scene_callback

    background = pygame.image.load(AC.BACKGROUND).convert()
    _background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

    _font_title = _make_font(AC.UI["title_font_frac"])
    _font_body = _make_font(0.030)
    _font_label = _make_font(AC.UI["label_font_frac"])
    _font_timer = _make_font(AC.UI["timer_font_frac"])

    _level_mgr = LevelManager()
    _timer = Timer(90)
    _results = ResultsScreen(WIDTH, HEIGHT)
    _results.continue_label = _success_action_label
    _layout()


def _make_font(size_fraction):
    size = max(14, min(int(HEIGHT * size_fraction), int(WIDTH * size_fraction * 1.5)))
    try:
        return pygame.font.Font(AC.FONT_PATH, size)
    except pygame.error:
        return pygame.font.SysFont(AC.FONT_FALLBACK, size, bold=True)


def _finish_level(time_up=False):
    """Current level finished — show results."""
    time_left = _timer.remaining()
    time_bonus = int(time_left * AC.POINTS_TIME_BONUS_PER_SECOND) if not time_up else 0
    if time_up:
        total = _game_score + _level_mgr.level_score
    else:
        total = _game_score + _level_mgr.complete_level(time_bonus)
    _timer.stop()

    if time_up:
        _results.show("timeup", _level_mgr.current_level, total, 0)
    elif _level_mgr.is_final_level():
        _results.show("victory", _level_mgr.current_level, total, time_bonus)
    else:
        _results.show("complete", _level_mgr.current_level, total, time_bonus)



def _next_ingredient():
    """Advance to the next ingredient in the current level."""
    cfg = _level_mgr.get_config()
    ing_keys = cfg["ingredients"]
    try:
        current_index = ing_keys.index(_current_ingredient)
    except ValueError:
        current_index = -1
    _begin_ingredient(current_index + 1)


def _show_message(text, duration=1.5):
    global _message, _message_until
    _message = text
    _message_until = time.monotonic() + duration


def _layout():
    global _sidebar_rect, _reference_rect, _workspace_rect, _target_rect

    header_h = max(54, int(HEIGHT * 0.085))
    footer_h = max(68, int(HEIGHT * 0.105))
    content_top = header_h + max(10, int(HEIGHT * 0.018))
    content_bottom = HEIGHT - footer_h - max(8, int(HEIGHT * 0.015))
    content_h = max(1, content_bottom - content_top)
    margin_x = max(14, int(WIDTH * 0.025))
    sidebar_w = int(WIDTH * AC.UI["sidebar_w"])
    gap = max(12, int(WIDTH * 0.018))

    _sidebar_rect = pygame.Rect(
        margin_x, content_top, sidebar_w, content_h
    )
    board_x = _sidebar_rect.right + gap
    _workspace_rect = pygame.Rect(
        board_x, content_top, max(1, WIDTH - margin_x - board_x), content_h
    )

    panel_padding = max(12, int(WIDTH * 0.012))
    reference_h = int(content_h * 0.38)
    _reference_rect = pygame.Rect(
        _sidebar_rect.x + panel_padding,
        _sidebar_rect.y + max(48, int(HEIGHT * 0.075)),
        _sidebar_rect.w - panel_padding * 2,
        reference_h,
    )

    target_size = min(
        int(_workspace_rect.w * 0.33),
        int(_workspace_rect.h * 0.56),
    )
    target_center_y = _workspace_rect.centery + max(8, int(HEIGHT * 0.012))
    _target_rect = pygame.Rect(0, 0, target_size, target_size)
    _target_rect.center = (_workspace_rect.centerx, target_center_y)


def _scatter_pieces(pieces, rotation_enabled):
    left_tray = pygame.Rect(
        _workspace_rect.left + 12,
        _workspace_rect.top + 48,
        max(1, _target_rect.left - _workspace_rect.left - 24),
        max(1, _workspace_rect.bottom - _workspace_rect.top - 60),
    )
    right_tray = pygame.Rect(
        _target_rect.right + 12,
        _workspace_rect.top + 48,
        max(1, _workspace_rect.right - _target_rect.right - 24),
        max(1, _workspace_rect.bottom - _workspace_rect.top - 60),
    )
    split = (len(pieces) + 1) // 2

    for index, piece in enumerate(pieces):
        tray = left_tray if index < split else right_tray
        tray_index = index if index < split else index - split
        tray_count = split if index < split else len(pieces) - split
        columns = 1 if tray_count <= 2 else 2
        rows = math.ceil(tray_count / columns)
        row, column = divmod(tray_index, columns)

        angle = random.choice((0, 180)) if rotation_enabled else 0
        piece.set_angle(angle)
        slot_w = tray.w / columns
        slot_h = tray.h / rows
        center_x = tray.left + (column + 0.5) * slot_w
        center_y = tray.top + (row + 0.5) * slot_h
        piece_w, piece_h = piece.rect().size
        center_x = max(
            tray.left + min(piece_w / 2, tray.w / 2),
            min(center_x, tray.right - min(piece_w / 2, tray.w / 2)),
        )
        center_y = max(
            tray.top + min(piece_h / 2, tray.h / 2),
            min(center_y, tray.bottom - min(piece_h / 2, tray.h / 2)),
        )
        piece.pos = [center_x, center_y]
        piece._rotated_rect.center = piece.pos


def draw_header(surf):
    header = pygame.Rect(0, 0, WIDTH, max(54, int(HEIGHT * 0.085)))
    pygame.draw.rect(surf, AC.PALETTE["deep_green"], header)
    pygame.draw.line(
        surf, AC.PALETTE["gold"], (0, header.bottom - 2), (WIDTH, header.bottom - 2), 3
    )

    level = _font_body.render(f"LEVEL {_level_mgr.current_level}", True, AC.PALETTE["cream"])
    surf.blit(level, level.get_rect(left=int(WIDTH * 0.025), centery=header.centery))

    title = _font_title.render("INGREDIENT JIGSAW", True, AC.PALETTE["cream"])
    surf.blit(title, title.get_rect(center=(WIDTH // 2, header.centery)))

    timer = _font_timer.render(
        f"TIME  {_timer.formatted()}", True, AC.PALETTE["gold"]
    )
    surf.blit(timer, timer.get_rect(right=int(WIDTH * 0.975), centery=header.centery))


def draw_sidebar(surf):
    panel = _sidebar_rect
    pygame.draw.rect(surf, (250, 248, 238), panel, border_radius=20)
    pygame.draw.rect(surf, (211, 201, 174), panel, width=2, border_radius=20)

    heading = _font_body.render("REFERENCE", True, AC.PALETTE["deep_green"])
    surf.blit(heading, heading.get_rect(centerx=panel.centerx, top=panel.y + 12))

    pygame.draw.rect(surf, (239, 236, 221), _reference_rect, border_radius=14)
    pygame.draw.rect(
        surf, (211, 201, 174), _reference_rect, width=2, border_radius=14
    )
    source = _load_reference_image()
    if source:
        artwork = source.get_bounding_rect(min_alpha=8)
        if artwork:
            source = source.subsurface(artwork).copy()
        image = pygame.transform.smoothscale(
            source,
            _fit_size(source.get_size(), (_reference_rect.w - 20, _reference_rect.h - 20)),
        )
        surf.blit(image, image.get_rect(center=_reference_rect.center))

    ingredient_index = next(
        i for i, (key, _, _) in enumerate(AC.INGREDIENT_GRID_ORDER)
        if key == _current_ingredient
    )
    name_lines = _wrap_text(
        AC.ingredient_label(ingredient_index), _font_label, panel.w - 20
    )
    name_top = _reference_rect.bottom + 12
    for index, line in enumerate(name_lines):
        label = _font_label.render(line, True, AC.PALETTE["ink"])
        surf.blit(
            label,
            label.get_rect(
                centerx=panel.centerx,
                top=name_top + index * (_font_label.get_linesize() + 1),
            ),
        )

    completed = _completed_ingredient_count()
    total = sum(len(config["ingredients"]) for config in AC.LEVELS.values())
    progress_y = name_top + len(name_lines) * (_font_label.get_linesize() + 1) + 8
    progress_lines = _wrap_text(
        f"INGREDIENTS {completed} OF {total} COMPLETE",
        _font_label,
        panel.w - 20,
    )
    for index, line in enumerate(progress_lines):
        progress = _font_label.render(line, True, AC.PALETTE["deep_green"])
        surf.blit(
            progress,
            progress.get_rect(
                centerx=panel.centerx,
                top=progress_y + index * (_font_label.get_linesize() + 1),
            ),
        )

    bar_top = progress_y + len(progress_lines) * (_font_label.get_linesize() + 1) + 8
    bar_rect = pygame.Rect(panel.x + 18, bar_top, panel.w - 36, 12)
    pygame.draw.rect(surf, (224, 219, 202), bar_rect, border_radius=6)
    fill_w = round(bar_rect.w * completed / max(1, total))
    if fill_w:
        pygame.draw.rect(
            surf, AC.PALETTE["green"],
            pygame.Rect(bar_rect.x, bar_rect.y, max(12, fill_w), bar_rect.h),
            border_radius=6,
        )

    instruction_top = bar_rect.bottom + 24
    instruction_lines = ["Drag pieces into the", "matching center outline."]
    if _level_mgr.get_config()["rotation"]:
        instruction_lines.extend(("Select a piece, then", "tap Rotate."))
    for index, line in enumerate(instruction_lines):
        text = _font_label.render(line, True, (91, 91, 77))
        surf.blit(
            text,
            text.get_rect(
                centerx=panel.centerx,
                top=instruction_top + index * (_font_label.get_linesize() + 4),
            ),
        )


def _fit_size(size, bounds):
    scale = min(bounds[0] / size[0], bounds[1] / size[1])
    return max(1, int(size[0] * scale)), max(1, int(size[1] * scale))


def _completed_ingredient_count():
    completed_in_earlier_levels = sum(
        len(config["ingredients"])
        for level, config in AC.LEVELS.items()
        if level < _level_mgr.current_level
    )
    completed_in_current_level = min(
        _level_mgr.ingredients_completed,
        len(_level_mgr.get_config()["ingredients"]),
    )
    return completed_in_earlier_levels + completed_in_current_level


def _wrap_text(text, font, max_width):
    lines = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if line and font.size(candidate)[0] > max_width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def _load_reference_image():
    if _current_ingredient in _reference_images:
        return _reference_images[_current_ingredient]

    index = None
    for i, (key, _, _) in enumerate(AC.INGREDIENT_GRID_ORDER):
        if key == _current_ingredient:
            index = i
            break
    if index is None:
        return None
    sheet = pygame.image.load(AC.SPRITE_SHEET).convert_alpha()
    crop_rect = pygame.Rect(
        *AC.crop_rect_for(index, sheet.get_width(), sheet.get_height())
    )
    from .puzzle_engine import _remove_magenta_matte

    source = _remove_magenta_matte(sheet.subsurface(crop_rect).copy())
    _reference_images[_current_ingredient] = source
    return source


def draw_workspace(surf):
    pygame.draw.rect(surf, (248, 246, 235), _workspace_rect, border_radius=22)
    pygame.draw.rect(
        surf, (211, 201, 174), _workspace_rect, width=2, border_radius=22
    )

    label = _font_label.render(
        "PIECES", True, (105, 103, 84)
    )
    surf.blit(
        label,
        label.get_rect(
            centerx=(_workspace_rect.left + _target_rect.left) // 2,
            top=_workspace_rect.top + 14,
        ),
    )
    label = _font_label.render("ASSEMBLE HERE", True, AC.PALETTE["deep_green"])
    surf.blit(
        label,
        label.get_rect(centerx=_target_rect.centerx, top=_workspace_rect.top + 14),
    )
    label = _font_label.render("PIECES", True, (105, 103, 84))
    surf.blit(
        label,
        label.get_rect(
            centerx=(_target_rect.right + _workspace_rect.right) // 2,
            top=_workspace_rect.top + 14,
        ),
    )

    surf.blit(_silhouette_surface, _target_rect)

    tray_top = _workspace_rect.top + 42
    tray_height = _workspace_rect.bottom - tray_top - 12
    left_tray = pygame.Rect(
        _workspace_rect.left + 10,
        tray_top,
        max(1, _target_rect.left - _workspace_rect.left - 20),
        tray_height,
    )
    right_tray = pygame.Rect(
        _target_rect.right + 10,
        tray_top,
        max(1, _workspace_rect.right - _target_rect.right - 20),
        tray_height,
    )
    for tray in (left_tray, right_tray):
        pygame.draw.rect(surf, (241, 238, 224), tray, border_radius=16)

    for piece in _current_pieces:
        if not piece.placed:
            piece.draw_target_guide(surf)

    for piece in _current_pieces:
        if not piece.placed:
            piece.draw(surf)

    for piece in _current_pieces:
        if piece.placed:
            piece.draw(surf)

    if _dragging_piece:
        _dragging_piece.draw(surf)


def draw_buttons(surf):
    buttons = [
        ("restart", "Restart", AC.PALETTE["red"]),
        ("pause", "Resume" if _timer._is_paused else "Pause", AC.PALETTE["gold"]),
    ]
    if "rotate" in _button_rects():
        buttons.append(("rotate", "Rotate", AC.PALETTE["deep_green"]))
    buttons.extend((
        ("skip", "Skip", AC.PALETTE["deep_green"]),
        ("exit", "Exit", AC.PALETTE["ink"]),
    ))

    rects = _button_rects()
    footer_h = max(68, int(HEIGHT * 0.105))
    footer = pygame.Rect(0, HEIGHT - footer_h, WIDTH, footer_h)
    pygame.draw.rect(surf, (250, 248, 238), footer)
    pygame.draw.line(
        surf, (211, 201, 174), (0, footer.top), (WIDTH, footer.top), 2
    )
    for key, label, color in buttons:
        rect = rects[key]
        shadow = rect.move(0, 4)
        pygame.draw.rect(surf, (38, 32, 23), shadow, border_radius=14)
        pygame.draw.rect(surf, color, rect, border_radius=14)
        pygame.draw.rect(surf, (255, 244, 207), rect, width=2, border_radius=14)
        txt = _font_label.render(label, True, (255, 255, 255))
        surf.blit(txt, txt.get_rect(center=rect.center))
    return rects


def draw_message(surf):
    now = time.monotonic()
    if _message and now < _message_until:
        ms = _font_body.render(_message, True, AC.PALETTE["ink"])
        panel = pygame.Rect(0, 0, ms.get_width() + 28, ms.get_height() + 16)
        panel.center = (_workspace_rect.centerx, _workspace_rect.bottom - 24)
        pygame.draw.rect(surf, (255, 253, 245), panel, border_radius=12)
        pygame.draw.rect(surf, (211, 201, 174), panel, width=1, border_radius=12)
        surf.blit(ms, ms.get_rect(center=panel.center))


def draw(surf):
    surf.blit(_background, (0, 0))

    if _results.active:
        _results.draw(surf)
        return

    if _advance_at is not None and time.monotonic() >= _advance_at:
        _next_ingredient()

    if _timer._is_running and _timer.is_expired():
        _finish_level(time_up=True)

    if _results.active:
        _results.draw(surf)
        return

    draw_header(surf)

    draw_sidebar(surf)
    draw_workspace(surf)
    draw_message(surf)
    draw_buttons(surf)
    if _timer._is_paused:
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((23, 41, 20, 110))
        surf.blit(shade, (0, 0))
        paused = _font_title.render("PAUSED", True, AC.PALETTE["cream"])
        surf.blit(paused, paused.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

def _button_rects():
    labels = ["restart", "pause", "skip", "exit"]
    if _level_mgr.get_config()["rotation"]:
        labels.insert(2, "rotate")

    group_w = int(WIDTH * (0.84 if len(labels) == 5 else 0.64))
    gap = max(8, int(WIDTH * 0.014))
    button_w = (group_w - gap * (len(labels) - 1)) // len(labels)
    button_h = min(58, max(42, int(HEIGHT * 0.065)))
    footer_h = max(68, int(HEIGHT * 0.105))
    start_x = (WIDTH - group_w) // 2
    top = HEIGHT - footer_h + (footer_h - button_h) // 2
    return {
        key: pygame.Rect(start_x + index * (button_w + gap), top, button_w, button_h)
        for index, key in enumerate(labels)
    }


def handle_tap(x, y):
    global _timer, _advance_at

    if _results.active:
        key = _results.handle_tap((x, y))
        if key == "next":
            _results.hide()
            next_level = _level_mgr.current_level + 1
            if next_level in _level_mgr.levels:
                _level_mgr.start_level(next_level)
                _begin_ingredient(0)
        elif key == "retry":
            _restart_level()
        elif key == "continue_story":
            _results.hide()
            if _success_callback is not None:
                _success_callback()
            else:
                from scenes import story_mode
                story_mode.resume_after_ingredient_puzzle()
                _go_to_scene("story_mode")
        elif key == "menu":
            _results.hide()
            _go_to_scene("main_menu")

        return

    global _selected_piece

    buttons = _button_rects()
    if buttons["restart"].collidepoint(x, y):
        _restart_level()
        return
    if buttons["pause"].collidepoint(x, y):
        if _timer._is_paused:
            _timer.resume()
        else:
            _timer.pause()
        return
    if buttons["skip"].collidepoint(x, y):
        if _timer._is_paused or _advance_at is not None:
            return
        _level_mgr.ingredient_completed()
        _advance_at = time.monotonic() + 0.35
        _show_message("Ingredient skipped.")
        return
    if buttons["exit"].collidepoint(x, y):
        _timer.stop()
        _go_to_scene("main_menu")
        return
    if "rotate" in buttons and buttons["rotate"].collidepoint(x, y):
        if _timer._is_paused:
            return
        if _selected_piece and not _selected_piece.placed:
            _selected_piece.rotate(90)
            _show_message("Rotated! Match the outline.")
        else:
            _show_message("Select a piece to rotate.")
        return

    if _timer._is_paused:
        return

    _selected_piece = None
    for piece in reversed(_current_pieces):
        if piece.placed:
            continue
        if piece.contains_point((x, y)):
            for current_piece in _current_pieces:
                current_piece.hovered = False
            piece.hovered = True
            _selected_piece = piece
            piece.start_drag((x, y))
            global _dragging_piece
            _dragging_piece = piece
            break


def handle_drag(x, y):
    if _dragging_piece and not _dragging_piece.placed and not _timer._is_paused:
        _dragging_piece.update_drag((x, y))


def handle_release(x, y):
    global _dragging_piece, _advance_at

    if _dragging_piece:
        piece = _dragging_piece
        piece.end_drag()
        if _timer._is_paused:
            _dragging_piece = None
            return

        cfg = _level_mgr.get_config()
        pos_tol = max(
            12, int(min(_workspace_rect.size) * AC.POS_TOLERANCE_FRAC)
        )
        angle_tol = AC.ANGLE_TOLERANCE_DEG if cfg["rotation"] else 5.0

        if piece.is_correctly_placed(pos_tol, angle_tol):
            piece.snap_to_correct()
            _show_message("Piece placed!")

            if all(p.placed for p in _current_pieces):
                _level_mgr.ingredient_completed(AC.POINTS_PER_INGREDIENT)
                _advance_at = time.monotonic() + 1.0
                _show_message("Ingredient complete!")

        else:
            _show_message(
                "Match the outline."
                if not cfg["rotation"] or piece.angle_diff() <= angle_tol
                else "Rotate the piece to match."
            )

        _dragging_piece = None



def handle_rotate(x, y):
    """Right-click a loose piece to rotate it in rotation-enabled levels."""
    global _selected_piece

    if _timer._is_paused or not _level_mgr.get_config()["rotation"]:
        return
    for piece in reversed(_current_pieces):
        if not piece.placed and piece.contains_point((x, y)):
            if _selected_piece:
                _selected_piece.hovered = False
            _selected_piece = piece
            piece.hovered = True
            piece.rotate(90)
            _show_message("Rotated! Match the outline.")
            return


def _restart_level():
    start()
