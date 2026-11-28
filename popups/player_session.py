"""Player profile selection and new-game setup."""

import pygame

import player_data
from popups import base


WIDTH = HEIGHT = 0
_panel = None
_close_rect = None
_close_popup = None
_on_continue = None
_on_new_game = None
_stage = "choice"
_profile = None
_name = ""
_error = ""
_choice_buttons = {}
_name_buttons = {}
_name_rect = None
_keyboard_buttons = []
_space_rect = None

_CREAM = (255, 246, 220)
_GREEN = (79, 119, 62)
_RED = (132, 68, 51)


def init(width, height, close_popup_callback, continue_callback, new_game_callback):
    global WIDTH, HEIGHT, _panel, _close_rect, _close_popup
    global _on_continue, _on_new_game, _choice_buttons, _name_buttons
    global _name_rect, _keyboard_buttons, _space_rect

    WIDTH, HEIGHT = width, height
    _close_popup = close_popup_callback
    _on_continue = continue_callback
    _on_new_game = new_game_callback
    _panel = base.make_panel_rect(WIDTH, HEIGHT, w_pct=0.76, h_pct=0.82)
    _close_rect = base.make_close_rect(_panel, WIDTH, HEIGHT)

    button_h = max(42, int(_panel.height * 0.105))
    button_gap = max(10, int(_panel.width * 0.025))
    choice_w = int((_panel.width * 0.88 - button_gap * 2) / 3)
    choice_y = _panel.bottom - button_h - int(_panel.height * 0.075)
    choice_x = _panel.centerx - (choice_w * 3 + button_gap * 2) // 2
    _choice_buttons = {
        "continue": pygame.Rect(choice_x, choice_y, choice_w, button_h),
        "new_game": pygame.Rect(
            choice_x + choice_w + button_gap, choice_y, choice_w, button_h
        ),
        "cancel": pygame.Rect(
            choice_x + (choice_w + button_gap) * 2, choice_y, choice_w, button_h
        ),
    }

    _name_rect = pygame.Rect(
        _panel.left + int(_panel.width * 0.12),
        _panel.top + int(_panel.height * 0.29),
        int(_panel.width * 0.76),
        max(38, int(_panel.height * 0.09)),
    )
    name_button_y = choice_y
    _name_buttons = {
        "save": pygame.Rect(
            _panel.centerx - choice_w - button_gap // 2,
            name_button_y,
            choice_w,
            button_h,
        ),
        "cancel": pygame.Rect(
            _panel.centerx + button_gap // 2,
            name_button_y,
            choice_w,
            button_h,
        ),
    }

    key_gap = 6
    key_width = max(16, (_panel.width - 2 * 24 - 9 * key_gap) // 10)
    keyboard_y = _name_rect.bottom + max(14, int(_panel.height * 0.035))
    available_key_height = (
        name_button_y - keyboard_y - 4 * key_gap
    ) // 4
    key_height = min(
        max(28, int(_panel.height * 0.075)),
        max(1, available_key_height),
    )
    _keyboard_buttons = []
    for row_index, keys in enumerate(("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM")):
        row_width = len(keys) * key_width + (len(keys) - 1) * key_gap
        x = _panel.centerx - row_width // 2
        y = keyboard_y + row_index * (key_height + key_gap)
        for column, key in enumerate(keys):
            rect = pygame.Rect(
                x + column * (key_width + key_gap), y, key_width, key_height
            )
            _keyboard_buttons.append((key, rect))
    _keyboard_buttons.append((
        "BACK",
        pygame.Rect(
            _panel.centerx + 4 * (key_width + key_gap),
            keyboard_y + 2 * (key_height + key_gap),
            key_width,
            key_height,
        ),
    ))
    space_width = min(int(_panel.width * 0.48), key_width * 5 + key_gap * 4)
    _space_rect = pygame.Rect(
        _panel.centerx - space_width // 2,
        keyboard_y + 3 * (key_height + key_gap),
        space_width,
        key_height,
    )


def open():
    global _stage, _profile, _name, _error
    _profile = player_data.last_profile()
    _stage = "choice" if _profile else "name"
    _name = ""
    _error = ""
    _sync_text_input()


def _sync_text_input():
    if _stage == "name":
        pygame.key.start_text_input()
    else:
        pygame.key.stop_text_input()


def _close():
    pygame.key.stop_text_input()
    _close_popup()


def _start_new_game():
    global _error
    if not player_data.create_profile(_name):
        _error = player_data.last_error()
        return
    pygame.key.stop_text_input()
    _on_new_game()


def _button_action(key):
    global _stage, _name, _error
    if _stage == "choice":
        if key == "continue":
            if not player_data.select_profile(_profile["id"]):
                _error = player_data.last_error()
                return
            _sync_text_input()
            _on_continue(player_data.current_profile())
        elif key == "new_game":
            _name = ""
            _error = ""
            _stage = "name"
            _sync_text_input()
        elif key == "cancel":
            _close()
    elif key == "save":
        _start_new_game()
    elif key == "cancel":
        if _profile:
            _stage = "choice"
            _error = ""
            _sync_text_input()
        else:
            _close()


def handle_tap(px, py):
    global _name
    if _close_rect.collidepoint(px, py):
        _close()
        return
    if not _panel.collidepoint(px, py):
        _close()
        return

    if _stage == "choice":
        for key, rect in _choice_buttons.items():
            if rect.collidepoint(px, py):
                _button_action(key)
                return
        return

    for key, rect in _name_buttons.items():
        if rect.collidepoint(px, py):
            _button_action(key)
            return
    for key, rect in _keyboard_buttons:
        if rect.collidepoint(px, py):
            if key == "BACK":
                _name = _name[:-1]
            elif len(_name) < 16:
                _name += key
            return
    if _space_rect.collidepoint(px, py) and len(_name) < 16:
        _name += " "


def handle_event(event):
    global _name
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        _button_action("cancel")
        return
    if _stage != "name":
        return
    if event.type == pygame.TEXTINPUT:
        _name = (_name + event.text)[:16]
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            _name = _name[:-1]
        elif event.key == pygame.K_RETURN:
            _button_action("save")


def _font(size, bold=False):
    return pygame.font.SysFont(None, max(16, size), bold=bold)


def _draw_button(surface, rect, label, color):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, (226, 205, 157), rect, width=2, border_radius=10)
    text = _font(int(HEIGHT * 0.032), bold=True).render(label, True, _CREAM)
    if text.get_width() > rect.width - 12:
        new_width = rect.width - 12
        text = pygame.transform.smoothscale(
            text,
            (new_width, max(1, round(text.get_height() * new_width / text.get_width()))),
        )
    surface.blit(text, text.get_rect(center=rect.center))


def _fit_text(text, size, max_width, bold=False):
    rendered = _font(size, bold).render(text, True, _CREAM)
    if rendered.get_width() > max_width:
        new_width = max_width
        rendered = pygame.transform.smoothscale(
            rendered,
            (new_width, max(1, round(rendered.get_height() * new_width / rendered.get_width()))),
        )
    return rendered


def draw(surface):
    base.draw_overlay(surface, WIDTH, HEIGHT)
    base.draw_panel_frame(
        surface,
        _panel,
        "Story Mode",
        title_font_size=max(30, int(HEIGHT * 0.05)),
    )
    base.draw_close_button(surface, _close_rect)

    if _stage == "choice":
        title = _fit_text(
            f"Continue as {_profile['name']}?",
            int(HEIGHT * 0.052),
            int(_panel.width * 0.82),
            True,
        )
        surface.blit(title, title.get_rect(
            center=(_panel.centerx, _panel.top + int(_panel.height * 0.25))
        ))
        details = (
            f"Saved total: {player_data.profile_total_score(_profile):,} points"
            f"   |   Chapters completed: "
            f"{len(_profile.get('completed_chapters', []))}"
        )
        detail_text = _fit_text(
            details, int(HEIGHT * 0.032), int(_panel.width * 0.86)
        )
        surface.blit(detail_text, detail_text.get_rect(
            center=(_panel.centerx, _panel.top + int(_panel.height * 0.38))
        ))
        _draw_button(surface, _choice_buttons["continue"], "Continue", _GREEN)
        _draw_button(surface, _choice_buttons["new_game"], "New Game", _GREEN)
        _draw_button(surface, _choice_buttons["cancel"], "Cancel", _RED)
    else:
        prompt = _fit_text(
            "Enter a unique player name",
            int(HEIGHT * 0.04),
            int(_panel.width * 0.82),
        )
        surface.blit(prompt, prompt.get_rect(
            center=(_panel.centerx, _panel.top + int(_panel.height * 0.20))
        ))
        pygame.draw.rect(surface, (255, 255, 245), _name_rect, border_radius=8)
        pygame.draw.rect(surface, (226, 205, 157), _name_rect, width=2, border_radius=8)
        value = _name or "Tap keys or type a name"
        color = (40, 40, 40) if _name else (120, 120, 120)
        name_text = _font(int(HEIGHT * 0.04)).render(value, True, color)
        if name_text.get_width() > _name_rect.width - 20:
            new_width = _name_rect.width - 20
            name_text = pygame.transform.smoothscale(
                name_text,
                (new_width, max(1, round(name_text.get_height() * new_width / name_text.get_width()))),
            )
        surface.blit(name_text, name_text.get_rect(
            midleft=(_name_rect.left + 12, _name_rect.centery)
        ))
        for key, rect in _keyboard_buttons:
            _draw_button(surface, rect, key, _GREEN)
        _draw_button(surface, _space_rect, "SPACE", _GREEN)
        _draw_button(surface, _name_buttons["save"], "Start Game", _GREEN)
        _draw_button(surface, _name_buttons["cancel"], "Back", _RED)

    if _error:
        error = _fit_text(
            _error, int(HEIGHT * 0.026), int(_panel.width * 0.86)
        )
        surface.blit(error, error.get_rect(
            center=(_panel.centerx, _panel.bottom - int(_panel.height * 0.035))
        ))
