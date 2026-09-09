# ============================================================
#  Scan Popup
#  Shown when the student needs to scan a physical card.
#  Includes a "Simulate Scan" button for testing without hardware.
# ============================================================

import pygame
import time

_W = _H = 0
_panel = None
_close_rect = None
_sim_btn = None

_card_name = ""
_question  = ""
_on_complete = None


def init(width: int, height: int):
    global _W, _H, _panel, _close_rect, _sim_btn

    _W, _H = width, height

    pw = int(_W * 0.55)
    ph = int(_H * 0.55)
    _panel = pygame.Rect(0, 0, pw, ph)
    _panel.center = (_W // 2, _H // 2)

    btn_w = int(pw * 0.50)
    btn_h = int(_H * 0.07)
    _sim_btn = pygame.Rect(0, 0, btn_w, btn_h)
    _sim_btn.centerx = _panel.centerx
    _sim_btn.bottom  = _panel.bottom - 20

    size = int(min(_W, _H) * 0.045)
    _close_rect = pygame.Rect(_panel.right - size - 10, _panel.top + 10, size, size)


def open(card_name: str, question: str, on_complete=None):
    global _card_name, _question, _on_complete
    _card_name   = card_name
    _question    = question
    _on_complete = on_complete


def handle_tap(px: int, py: int) -> bool:
    """Returns True if the popup consumed the tap."""
    if _sim_btn and _sim_btn.collidepoint(px, py):
        if _on_complete:
            _on_complete()
        return True
    if _close_rect and _close_rect.collidepoint(px, py):
        if _on_complete:
            _on_complete()
        return True
    if _panel and not _panel.collidepoint(px, py):
        return True  # blocked tap from going through
    return True


def draw(surf: pygame.Surface):
    if _panel is None:
        return

    # Dark overlay behind the panel
    overlay = pygame.Surface((_W, _H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surf.blit(overlay, (0, 0))

    # Panel background
    pygame.draw.rect(surf, (30, 30, 45), _panel, border_radius=14)
    pygame.draw.rect(surf, (255, 220, 80), _panel, width=3, border_radius=14)

    font_title = pygame.font.SysFont(None, int(_H * 0.045))
    font_body  = pygame.font.SysFont(None, int(_H * 0.033))

    # Card name (yellow)
    card_surf = font_title.render(f"Scan: {_card_name}", True, (255, 220, 80))
    surf.blit(card_surf, card_surf.get_rect(midtop=(_panel.centerx, _panel.top + 20)))

    # Question text (word-wrapped)
    _draw_wrapped(surf, font_body, _question, (220, 220, 220),
                  _panel.x + 20, _panel.top + int(_panel.height * 0.25),
                  _panel.width - 40)

    # Simulate Scan button (green)
    pygame.draw.rect(surf, (50, 180, 80), _sim_btn, border_radius=10)
    pygame.draw.rect(surf, (255, 255, 255), _sim_btn, width=2, border_radius=10)
    btn_lbl = font_body.render("Simulate Scan", True, (255, 255, 255))
    surf.blit(btn_lbl, btn_lbl.get_rect(center=_sim_btn.center))

    # Close button
    pygame.draw.rect(surf, (180, 50, 50), _close_rect, border_radius=6)
    x_lbl = font_body.render("X", True, (255, 255, 255))
    surf.blit(x_lbl, x_lbl.get_rect(center=_close_rect.center))


def _draw_wrapped(surf, font, text, color, x, y, max_width):
    """Draw text wrapping at max_width pixels."""
    words = text.split()
    line  = ""
    line_h = font.get_linesize()
    for word in words:
        test = (line + " " + word).strip()
        if font.size(test)[0] <= max_width:
            line = test
        else:
            surf.blit(font.render(line, True, color), (x, y))
            y   += line_h
            line = word
    if line:
        surf.blit(font.render(line, True, color), (x, y))
