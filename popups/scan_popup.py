"""Live camera card scan popup used by story action challenges."""

import pygame

import player_data
from cardscan import CameraError, CardScanner


_W = _H = 0
_panel = None
_preview_rect = None
_close_rect = None
_retry_rect = None
_scanner = None
_card_name = ""
_question = ""
_on_complete = None
_on_cancel = None
_error = ""
_status = ""
_retry_enabled = False
_last_ticks = 0
_pending_match_at = 0

_CREAM = (255, 246, 220)
_GREEN = (79, 119, 62)
_BORDER = (226, 205, 157)


def init(width: int, height: int):
    global _W, _H, _panel, _preview_rect, _close_rect
    global _retry_rect, _scanner, _pending_match_at
    if _scanner is not None:
        _scanner.cancel()
    _W, _H = width, height
    panel_width = int(_W * 0.88)
    panel_height = int(_H * 0.88)
    _panel = pygame.Rect(0, 0, panel_width, panel_height)
    _panel.center = (_W // 2, _H // 2)

    preview_width = int(_panel.width * 0.60)
    preview_height = int(_panel.height * 0.60)
    _preview_rect = pygame.Rect(0, 0, preview_width, preview_height)
    _preview_rect.center = (
        _panel.centerx,
        _panel.top + int(_panel.height * 0.54),
    )
    close_size = max(34, int(min(_W, _H) * 0.065))
    _close_rect = pygame.Rect(
        _panel.right - close_size - 12,
        _panel.top + 12,
        close_size,
        close_size,
    )
    _retry_rect = pygame.Rect(
        0,
        0,
        min(int(_panel.width * 0.38), max(150, int(_W * 0.24))),
        max(42, int(_H * 0.065)),
    )
    _retry_rect.center = (
        _panel.centerx,
        _panel.bottom - int(_panel.height * 0.10),
    )
    _scanner = CardScanner(confirm_frames=12)
    _pending_match_at = 0


def open(card_name: str, question: str, on_complete=None, on_cancel=None):
    global _card_name, _question, _on_complete, _on_cancel
    global _error, _status, _retry_enabled, _last_ticks, _pending_match_at
    if _scanner is not None:
        _scanner.cancel()
    _card_name = card_name
    _question = question
    _on_complete = on_complete
    _on_cancel = on_cancel
    _error = ""
    _retry_enabled = False
    _status = "Opening camera..."
    _last_ticks = pygame.time.get_ticks()
    _pending_match_at = 0
    _start_scan()


def _start_scan():
    global _error, _status, _retry_enabled
    if _scanner is None:
        return
    _retry_enabled = False
    card = _scanner.start(_card_name)
    if card is None:
        _error = f"Unrecognized card in story: {_card_name}"
        _status = "This card is not in the scanner catalog."
        return
    if not _scanner.trained:
        _error = "No current trained card model. Run tools/train_cards.py."
        _status = "Train the card samples before scanning."
        return
    if not _scanner.can_recognize:
        _error = "The model has only one trained card class."
        _status = "Train samples for at least one more card to enable scanning."
        return
    settings = player_data.get_settings()
    try:
        _scanner.open_camera(
            kind="opencv",
            device=settings["camera_device"],
        )
    except CameraError as exc:
        _error = str(exc)
        _status = "Camera unavailable. Check focus and connection, then retry."
        _retry_enabled = True
        return
    _error = ""
    _status = f"Show the {card.name} to the camera."


def close():
    if _scanner is not None:
        _scanner.cancel()


def _cancel():
    global _on_cancel
    close()
    callback = _on_cancel
    _on_cancel = None
    if callback is not None:
        callback()


def handle_tap(px: int, py: int) -> bool:
    if _close_rect and _close_rect.collidepoint(px, py):
        _cancel()
    elif (
        _retry_enabled
        and _retry_rect
        and _retry_rect.collidepoint(px, py)
        and _error
    ):
        _start_scan()
    return True


def _font(size, bold=False):
    return pygame.font.SysFont(None, max(16, size), bold=bold)


def _fit(text, size, max_width, color, bold=False):
    rendered = _font(size, bold).render(text, True, color)
    if rendered.get_width() <= max_width:
        return rendered
    new_height = max(1, round(rendered.get_height() * max_width / rendered.get_width()))
    return pygame.transform.smoothscale(rendered, (max_width, new_height))


def _draw_wrapped(surface, text, rect, size, color):
    font = _font(size)
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and font.size(candidate)[0] > rect.width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    y = rect.top
    for line in lines:
        rendered = _fit(line, size, rect.width, color)
        surface.blit(rendered, rendered.get_rect(midtop=(rect.centerx, y)))
        y += font.get_linesize()


def _draw_button(surface, rect, label):
    pygame.draw.rect(surface, _GREEN, rect, border_radius=10)
    pygame.draw.rect(surface, _BORDER, rect, width=2, border_radius=10)
    text = _fit(label, int(_H * 0.032), rect.width - 16, _CREAM, bold=True)
    surface.blit(text, text.get_rect(center=rect.center))


def _update_scanner():
    global _last_ticks, _status, _error, _retry_enabled, _pending_match_at
    if _scanner is None or not _scanner.cam or _error:
        return
    now = pygame.time.get_ticks()
    if _pending_match_at:
        if now >= _pending_match_at:
            callback = _on_complete
            close()
            if callback is not None:
                callback()
        return
    dt = max(0.001, min(0.1, (now - _last_ticks) / 1000.0))
    _last_ticks = now
    try:
        result = _scanner.update(dt)
    except CameraError as exc:
        _error = str(exc)
        _status = "Camera read failed. Check focus and connection, then retry."
        close()
        _retry_enabled = True
        return
    if result is None:
        return
    if result.status == result.MATCH:
        _status = f"Matched {result.card.replace('_', ' ').title()} ({result.score:.0%})."
        _pending_match_at = now + 1500
    elif result.status == result.WRONG:
        _status = (
            f"Detected {result.card.replace('_', ' ').title()}; "
            "show the requested card."
        )


def draw(surface: pygame.Surface):
    if _panel is None:
        return
    _update_scanner()

    overlay = pygame.Surface((_W, _H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    surface.blit(overlay, (0, 0))
    pygame.draw.rect(surface, (30, 30, 45), _panel, border_radius=14)
    pygame.draw.rect(surface, _BORDER, _panel, width=3, border_radius=14)

    title = _fit(
        f"Scan: {_card_name}",
        int(_H * 0.052),
        int(_panel.width * 0.78),
        _CREAM,
        bold=True,
    )
    surface.blit(title, title.get_rect(midtop=(
        _panel.centerx, _panel.top + int(_panel.height * 0.035)
    )))
    _draw_wrapped(
        surface,
        _question,
        pygame.Rect(
            _panel.left + int(_panel.width * 0.08),
            _panel.top + int(_panel.height * 0.13),
            int(_panel.width * 0.84),
            int(_panel.height * 0.10),
        ),
        int(_H * 0.032),
        (225, 225, 215),
    )

    pygame.draw.rect(surface, (8, 12, 12), _preview_rect, border_radius=10)
    pygame.draw.rect(surface, (116, 131, 105), _preview_rect, width=2, border_radius=10)
    frame = _scanner.frame if _scanner is not None else None
    if frame is not None:
        scale = min(
            (_preview_rect.width - 8) / frame.get_width(),
            (_preview_rect.height - 8) / frame.get_height(),
        )
        size = (
            max(1, int(frame.get_width() * scale)),
            max(1, int(frame.get_height() * scale)),
        )
        image = pygame.transform.smoothscale(frame, size)
        image_rect = image.get_rect(center=_preview_rect.center)
        surface.blit(image, image_rect)
        guide_side = int(min(size) * 0.86)
        guide = pygame.Rect(0, 0, guide_side, guide_side)
        guide.center = image_rect.center
        pygame.draw.rect(surface, (125, 225, 130), guide, width=2, border_radius=6)
    else:
        message = _error or "Starting camera preview..."
        rendered = _fit(message, int(_H * 0.027), _preview_rect.width - 24, (245, 190, 145))
        surface.blit(rendered, rendered.get_rect(center=_preview_rect.center))

    status = _fit(_status, int(_H * 0.028), int(_panel.width * 0.82), _CREAM)
    status_y = _preview_rect.bottom + int(_panel.height * 0.03)
    surface.blit(status, status.get_rect(midtop=(_panel.centerx, status_y)))
    if _retry_enabled:
        _draw_button(surface, _retry_rect, "Retry camera")

    pygame.draw.rect(surface, (150, 55, 48), _close_rect, border_radius=8)
    pygame.draw.rect(surface, _BORDER, _close_rect, width=2, border_radius=8)
    close_label = _font(int(_H * 0.04), bold=True).render("X", True, _CREAM)
    surface.blit(close_label, close_label.get_rect(center=_close_rect.center))
