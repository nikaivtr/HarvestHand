import pygame

from popups import base

WIDTH = 0
HEIGHT = 0
_close_popup = None

panel_rect = None
close_btn_rect = None

# TODO: replace with real how-to-play copy
INFO_LINES = [
    "Lay a Crop, Water, or Harvest card",
    "on the scanner to grow your farm",
    "and learn along the way!",
]


def init(width, height, close_popup_callback):
    """Called once by main_menu.py after the window is created."""
    global WIDTH, HEIGHT, _close_popup, panel_rect, close_btn_rect
    WIDTH, HEIGHT = width, height
    _close_popup = close_popup_callback

    panel_rect = base.make_panel_rect(WIDTH, HEIGHT, h_pct=0.45)
    close_btn_rect = base.make_close_rect(panel_rect, WIDTH, HEIGHT)


def handle_tap(px, py):
    base.tap_closes_popup(px, py, panel_rect, close_btn_rect, _close_popup)


def draw(surf):
    base.draw_overlay(surf, WIDTH, HEIGHT)
    base.draw_panel_frame(surf, panel_rect, "How to Play")

    body_font = pygame.font.SysFont(None, 32)
    line_y = panel_rect.top + 100
    line_gap = 38
    for line in INFO_LINES:
        text = body_font.render(line, True, (230, 230, 230))
        surf.blit(text, text.get_rect(midtop=(panel_rect.centerx, line_y)))
        line_y += line_gap

    base.draw_close_button(surf, close_btn_rect)
