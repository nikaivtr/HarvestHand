"""Card scanner test panel."""
import os
import pygame
import numpy as np
import cv2
import config
from cardscan import (CardScanner, all_cards, open_camera, CameraError)

WIDTH = 0
HEIGHT = 0
_close_popup = None

_panel = None
_close_rect = None
_scanner = None
_cam_opened = False
_cards = []
_selected_idx = 0
_result_msg = "Select a card, then hold it up."
_card_rects = []
_preview_rect = None

_ACCENT = (190, 160, 110)
_OK = (90, 200, 110)
_BAD = (220, 90, 90)
_IDLE = (100, 110, 100)
_AMBER = (210, 130, 80)


def _make_font(size, bold=False):
    try:
        return pygame.font.Font(os.path.join("fonts", "RumRaisin-Regular.ttf"), size)
    except (pygame.error, OSError):
        return pygame.font.SysFont("Arial", size, bold=bold)


def init(width, height, close_popup_callback):
    global WIDTH, HEIGHT, _close_popup, _panel, _close_rect, _close_img, _scanner, _cards, _cam_opened, _selected_idx
    WIDTH, HEIGHT = width, height
    _close_popup = close_popup_callback
    panel_w = int(WIDTH * 0.9)
    panel_h = int(HEIGHT * 0.9)
    _panel = pygame.Rect(0, 0, panel_w, panel_h)
    _panel.center = (WIDTH // 2, HEIGHT // 2)
    _close_rect = pygame.Rect(_panel.right - 44, _panel.top + 10, 36, 36)
    import utils
    _close_img = utils.load_img("buttons/btn_close.png", utils.btn_size(int(WIDTH * 0.06)))
    _close_rect = _close_img.get_rect(topright=(_panel.right - 10, _panel.top + 10))
    _cards = all_cards()
    _selected_idx = 0
    _scanner = CardScanner()
    try:
        _scanner.open_camera(device=0)
        _cam_opened = True
        _scanner.start(_cards[0].display)
    except Exception:
        _cam_opened = False


def handle_tap(px, py):
    global _selected_idx
    if _close_rect and _close_rect.collidepoint(px, py):
        _close_popup()
        return
    if _panel and not _panel.collidepoint(px, py):
        _close_popup()
        return
    for i, r in enumerate(_card_rects):
        if r.collidepoint(px, py):
            _selected_idx = i
            if _scanner:
                _scanner.start(_cards[i].display)
            return


def _frame_to_surface(frame):
    if frame is None:
        return None
    if isinstance(frame, pygame.Surface):
        return pygame.transform.smoothscale(frame, (_preview_rect.width, _preview_rect.height))
    return None


def draw(surf):
    global _result_msg, _preview_rect, _card_rects
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surf.blit(overlay, (0, 0))
    pygame.draw.rect(surf, (26, 32, 40), _panel, border_radius=16)
    pygame.draw.rect(surf, (90, 110, 100), _panel, width=2, border_radius=16)

    title_font = _make_font(max(28, int(HEIGHT * 0.05)), bold=True)
    body_font = _make_font(max(16, int(HEIGHT * 0.024)))
    t = title_font.render("Card Scan Tester", True, (240, 235, 225))
    surf.blit(t, t.get_rect(midtop=(_panel.centerx, _panel.top + 16)))

    # camera preview (center-left)
    pw = int(_panel.width * 0.55)
    ph = int(_panel.height * 0.55)
    _preview_rect = pygame.Rect(0, 0, pw, ph)
    _preview_rect.center = (_panel.left + int(_panel.width * 0.32), _panel.centery + 20)
    pygame.draw.rect(surf, (0, 0, 0), _preview_rect, border_radius=10)
    pygame.draw.rect(surf, (90, 110, 100), _preview_rect, width=2, border_radius=10)

    if _scanner:
        res = _scanner.update(1.0 / 60.0)
        if res is not None:
            if res.status == res.MATCH:
                _result_msg = f"MATCH: {res.card}"
            elif res.status == res.WRONG:
                _result_msg = f"WRONG: read {res.card}, want {res.expected}"
            else:
                _result_msg = str(res)
        frame = _scanner.frame
        s = _frame_to_surface(frame)
        if s:
            surf.blit(s, _preview_rect.topleft)
        else:
            nf = body_font.render("No camera frame", True, (150, 160, 150))
            surf.blit(nf, nf.get_rect(center=_preview_rect.center))
        st = body_font.render(_scanner.status(), True, (150, 160, 150))
        surf.blit(st, st.get_rect(midtop=(_preview_rect.centerx, _preview_rect.bottom + 8)))

    # card list (right)
    _card_rects = []
    lx = _panel.right - int(_panel.width * 0.34)
    ly = _panel.top + int(_panel.height * 0.18)
    for i, c in enumerate(_cards):
        r = pygame.Rect(lx, ly + i * 44, int(_panel.width * 0.3), 36)
        _card_rects.append(r)
        color = (60, 90, 70) if i == _selected_idx else (40, 50, 60)
        pygame.draw.rect(surf, color, r, border_radius=8)
        pygame.draw.rect(surf, (90, 110, 100), r, width=1, border_radius=8)
        lbl = body_font.render(c.display, True, (240, 235, 225))
        surf.blit(lbl, lbl.get_rect(midleft=(r.left + 8, r.centery)))
        ly += 0  # handled by i

    # result message
    rm = body_font.render(_result_msg, True, (210, 130, 80))
    surf.blit(rm, rm.get_rect(midbottom=(_panel.centerx, _panel.bottom - 16)))

    # close button
    surf.blit(_close_img, _close_rect)
