import pygame

from popups import base

WIDTH = 0
HEIGHT = 0
_close_popup = None   # callback: close_popup()

panel_rect = None
close_btn_rect = None

# Placeholder leaderboard data — replace with real scores later
PLACEHOLDER_SCORES = [
    ("Player 1", 9999),
    ("Player 2", 8421),
    ("Player 3", 7310),
    ("Player 4", 5200),
    ("Player 5", 3050),
]


def init(width, height, close_popup_callback):
    """Called once by main_menu.py after the window is created."""
    global WIDTH, HEIGHT, _close_popup, panel_rect, close_btn_rect
    WIDTH, HEIGHT = width, height
    _close_popup = close_popup_callback

    panel_rect = base.make_panel_rect(WIDTH, HEIGHT)
    close_btn_rect = base.make_close_rect(panel_rect, WIDTH, HEIGHT)


def handle_tap(px, py):
    base.tap_closes_popup(px, py, panel_rect, close_btn_rect, _close_popup)


def draw(surf):
    base.draw_overlay(surf, WIDTH, HEIGHT)
    base.draw_panel_frame(surf, panel_rect, "Leaderboard")

    # Placeholder score rows
    row_font = pygame.font.SysFont(None, 36)
    row_y = panel_rect.top + 90
    row_gap = int(panel_rect.height * 0.12)
    for i, (name, score) in enumerate(PLACEHOLDER_SCORES):
        row_text = f"{i + 1}. {name} — {score}"
        row = row_font.render(row_text, True, (230, 230, 230))
        surf.blit(row, row.get_rect(midtop=(panel_rect.centerx, row_y)))
        row_y += row_gap

    base.draw_close_button(surf, close_btn_rect)
