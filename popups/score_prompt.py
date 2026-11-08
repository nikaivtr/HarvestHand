"""Touch-friendly prompts for optionally saving named scores."""

import pygame

import player_data


WIDTH = HEIGHT = 0
_panel = None
_name_rect = None
_choice_buttons = {}
_confirm_buttons = {}
_name_buttons = {}
_keyboard_buttons = []
_space_rect = None
_stage = "choice"
_name = ""
_error = ""
_current_record = None

_CREAM = (255, 246, 220)
_GREEN = (79, 119, 62)
_RED = (132, 68, 51)
_INK = (40, 40, 50)


def init(width, height):
    global WIDTH, HEIGHT, _panel, _name_rect, _choice_buttons
    global _confirm_buttons, _name_buttons, _keyboard_buttons, _space_rect
    WIDTH, HEIGHT = width, height
    panel_width = int(WIDTH * 0.88)
    panel_height = int(HEIGHT * 0.90)
    _panel = pygame.Rect(0, 0, panel_width, panel_height)
    _panel.center = (WIDTH // 2, HEIGHT // 2)

    button_width = int(_panel.width * 0.40)
    button_height = max(42, int(_panel.height * 0.12))
    button_gap = max(14, int(_panel.width * 0.04))
    choice_y = _panel.top + int(_panel.height * 0.66)
    _choice_buttons = {
        "record": pygame.Rect(
            _panel.centerx - button_gap // 2 - button_width,
            choice_y,
            button_width,
            button_height,
        ),
        "skip": pygame.Rect(
            _panel.centerx + button_gap // 2,
            choice_y,
            button_width,
            button_height,
        ),
    }
    _confirm_buttons = {
        "yes": _choice_buttons["record"].copy(),
        "no": _choice_buttons["skip"].copy(),
    }

    _name_rect = pygame.Rect(
        _panel.left + int(_panel.width * 0.12),
        _panel.top + int(_panel.height * 0.35),
        int(_panel.width * 0.76),
        max(38, int(_panel.height * 0.09)),
    )
    name_button_y = _panel.top + int(_panel.height * 0.82)
    _name_buttons = {
        "save": pygame.Rect(
            _panel.centerx - button_gap // 2 - button_width,
            name_button_y,
            button_width,
            button_height,
        ),
        "cancel": pygame.Rect(
            _panel.centerx + button_gap // 2,
            name_button_y,
            button_width,
            button_height,
        ),
    }

    key_width = max(26, (_panel.width - 2 * 24 - 9 * 6) // 10)
    key_height = max(28, int(_panel.height * 0.075))
    key_gap = 6
    rows = ("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM")
    keyboard_y = _panel.top + int(_panel.height * 0.47)
    _keyboard_buttons = []
    for row_index, keys in enumerate(rows):
        row_width = len(keys) * key_width + (len(keys) - 1) * key_gap
        x = _panel.centerx - row_width // 2
        y = keyboard_y + row_index * (key_height + key_gap)
        for column, key in enumerate(keys):
            rect = pygame.Rect(
                x + column * (key_width + key_gap), y, key_width, key_height
            )
            _keyboard_buttons.append((key, rect))
    backspace_rect = pygame.Rect(
        _panel.centerx + 4 * (key_width + key_gap),
        keyboard_y + 2 * (key_height + key_gap),
        key_width,
        key_height,
    )
    _keyboard_buttons.append(("⌫", backspace_rect))
    space_width = min(int(_panel.width * 0.48), key_width * 5 + key_gap * 4)
    _space_rect = pygame.Rect(0, 0, space_width, key_height)
    _space_rect.center = (
        _panel.centerx,
        keyboard_y + 3 * (key_height + key_gap),
    )


def active():
    _sync_pending_record()
    return _current_record is not None


def _sync_pending_record():
    global _current_record, _stage, _name, _error
    pending = player_data.pending_score_record()
    if pending is _current_record:
        return
    if _stage == "name":
        pygame.key.stop_text_input()
    _current_record = pending
    _stage = "choice"
    _name = ""
    _error = ""


def _score_description():
    record = _current_record["record"]
    if _current_record.get("kind") == "chapter":
        title = str(record.get("chapter", "Chapter")).replace("_", " ").title()
        return title, int(record.get("score", 0))
    title = str(record.get("game", "Mini-game")).replace("_", " ").title()
    return title, int(record.get("score", 0))


def _set_stage(stage):
    global _stage, _error
    if _stage == "name" and stage != "name":
        pygame.key.stop_text_input()
    _stage = stage
    _error = ""
    if stage == "name":
        pygame.key.start_text_input()


def _button_action(key):
    global _name, _error
    if _stage == "choice":
        if key == "record":
            _set_stage("name")
        elif key == "skip":
            _set_stage("confirm")
    elif _stage == "confirm":
        if key == "yes":
            player_data.decline_pending_score()
            _sync_pending_record()
        elif key == "no":
            _set_stage("choice")
    elif _stage == "name":
        if key == "save":
            if not _name.strip():
                _error = "Enter a nickname before saving."
            elif player_data.record_pending_score(_name):
                _sync_pending_record()
            else:
                _error = player_data.last_error() or "The score could not be saved."
        elif key == "cancel":
            _set_stage("choice")


def handle_tap(px, py):
    global _name
    if not active() or not _panel.collidepoint(px, py):
        return
    if _stage == "choice":
        for key, rect in _choice_buttons.items():
            if rect.collidepoint(px, py):
                _button_action(key)
                return
    elif _stage == "confirm":
        for key, rect in _confirm_buttons.items():
            if rect.collidepoint(px, py):
                _button_action(key)
                return
    elif _stage == "name":
        for key, rect in _name_buttons.items():
            if rect.collidepoint(px, py):
                _button_action(key)
                return
        for key, rect in _keyboard_buttons:
            if rect.collidepoint(px, py):
                if key == "⌫":
                    _name = _name[:-1]
                elif len(_name) < 16:
                    _name += key
                return
        if _space_rect.collidepoint(px, py) and len(_name) < 16:
            _name += " "


def handle_event(event):
    global _name
    if not active():
        return
    if event.type == pygame.TEXTINPUT and _stage == "name":
        _name = (_name + event.text)[:16]
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            if _stage == "name":
                _set_stage("choice")
            elif _stage == "confirm":
                _set_stage("choice")
        elif event.key == pygame.K_BACKSPACE and _stage == "name":
            _name = _name[:-1]
        elif event.key == pygame.K_RETURN:
            if _stage == "choice":
                _button_action("record")
            elif _stage == "confirm":
                _button_action("yes")
            elif _stage == "name":
                _button_action("save")


def _font(size, bold=False):
    return pygame.font.SysFont(None, max(16, size), bold=bold)


def _fit(text, size, max_width, bold=False):
    font = _font(size, bold)
    rendered = font.render(text, True, _CREAM)
    if rendered.get_width() > max_width:
        rendered = pygame.transform.smoothscale(
            rendered,
            (max_width, max(1, round(rendered.get_height() * max_width / rendered.get_width()))),
        )
    return rendered


def _draw_button(surface, rect, label, color):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, (226, 205, 157), rect, width=2, border_radius=10)
    text = _fit(label, int(HEIGHT * 0.035), rect.width - 14, bold=True)
    surface.blit(text, text.get_rect(center=rect.center))


def draw(surface):
    if not active():
        return
    veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    veil.fill((0, 0, 0, 185))
    surface.blit(veil, (0, 0))
    pygame.draw.rect(surface, _INK, _panel, border_radius=16)
    pygame.draw.rect(surface, (226, 205, 157), _panel, width=3, border_radius=16)

    title, score = _score_description()
    title_text = _fit("Save your score?", int(HEIGHT * 0.06), int(_panel.width * 0.85), True)
    surface.blit(title_text, title_text.get_rect(
        center=(_panel.centerx, _panel.top + int(_panel.height * 0.12))
    ))
    detail = _fit(
        f"{title}  |  {score:,} points",
        int(HEIGHT * 0.035),
        int(_panel.width * 0.86),
    )
    surface.blit(detail, detail.get_rect(
        center=(_panel.centerx, _panel.top + int(_panel.height * 0.25))
    ))

    if _stage == "choice":
        prompt = "Would you like to record this score?"
        y = _panel.top + int(_panel.height * 0.46)
        text = _fit(prompt, int(HEIGHT * 0.04), int(_panel.width * 0.84))
        surface.blit(text, text.get_rect(center=(_panel.centerx, y)))
        _draw_button(surface, _choice_buttons["record"], "Record score", _GREEN)
        _draw_button(surface, _choice_buttons["skip"], "Don't record", _RED)
    elif _stage == "confirm":
        prompt = "Are you sure you don't want to record your score?"
        text = _fit(prompt, int(HEIGHT * 0.04), int(_panel.width * 0.84))
        surface.blit(text, text.get_rect(center=(
            _panel.centerx, _panel.top + int(_panel.height * 0.48)
        )))
        _draw_button(surface, _confirm_buttons["yes"], "Yes, skip", _RED)
        _draw_button(surface, _confirm_buttons["no"], "No, go back", _GREEN)
    else:
        prompt = _fit("Enter a nickname (up to 16 characters)", int(HEIGHT * 0.035),
                      int(_panel.width * 0.84))
        surface.blit(prompt, prompt.get_rect(center=(
            _panel.centerx, _panel.top + int(_panel.height * 0.31)
        )))
        pygame.draw.rect(surface, (255, 255, 245), _name_rect, border_radius=8)
        pygame.draw.rect(surface, (226, 205, 157), _name_rect, width=2, border_radius=8)
        name_text = _font(int(HEIGHT * 0.045)).render(
            _name or "Tap keys or type a name",
            True,
            (40, 40, 40) if _name else (120, 120, 120),
        )
        if name_text.get_width() > _name_rect.width - 20:
            scaled_height = max(
                1,
                round(name_text.get_height() * (_name_rect.width - 20) / name_text.get_width()),
            )
            name_text = pygame.transform.smoothscale(
                name_text, (_name_rect.width - 20, scaled_height)
            )
        surface.blit(name_text, name_text.get_rect(midleft=(
            _name_rect.left + 12, _name_rect.centery
        )))
        for key, rect in _keyboard_buttons:
            _draw_button(surface, rect, key, _GREEN)
        _draw_button(surface, _space_rect, "SPACE", _GREEN)
        _draw_button(surface, _name_buttons["save"], "Save score", _GREEN)
        _draw_button(surface, _name_buttons["cancel"], "Back", _RED)

    if _error:
        error = _fit(_error, int(HEIGHT * 0.027), int(_panel.width * 0.84))
        surface.blit(error, error.get_rect(center=(
            _panel.centerx, _panel.bottom - int(_panel.height * 0.035)
        )))
