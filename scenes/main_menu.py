"""
Main menu scene.

Owns the menu background/logo/buttons AND the three popups that open from it
(leaderboard, info, settings) — those popups never appear anywhere else, so
keeping them here (instead of in main.py) keeps the scene self-contained.
"""

import sys
import time

import pygame

import config
import utils
from popups import leaderboards, info, settings

WIDTH = 0
HEIGHT = 0
_go_to_scene = None   # callback from main.py: go_to_scene(scene_name)

bg_image = None
logo_image = None
logo_rect = None

main_menu_buttons = []   # [{"img", "rect", "cb", "pressed_at"}, ...]
TAP_PAD = 0              # invisible extra tap area around each button

# Popup state — only relevant while this scene is active
active_popup = None   # None, "leaderboard", "info", or "settings"


def init(width, height, go_to_scene_callback):
    """Called once by main.py after the window is created."""
    global WIDTH, HEIGHT, _go_to_scene, bg_image, logo_image, logo_rect
    global main_menu_buttons, TAP_PAD

    WIDTH, HEIGHT = width, height
    _go_to_scene = go_to_scene_callback

    bg_image = utils.load_bg("background/menubg2.png", (WIDTH, HEIGHT))

    # ── Logo ──────────────────────────────────────────────────────────────
    logo_w = int(WIDTH * 0.55)
    logo_h = int(HEIGHT * 0.55)
    logo_image = utils.load_img("logos/hhlogo.png", (logo_w, logo_h))
    logo_rect = logo_image.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.30)))

    # ════════════════════════════════════════════════════════════════════
    #  BUTTON SIZES & POSITIONS ← adjust these to reposition/resize
    # ════════════════════════════════════════════════════════════════════

    # Play button (center)
    play_w  = int(WIDTH * 0.35)
    play_cx = WIDTH // 2
    play_cy = int(HEIGHT * 0.77)
    play_img  = utils.load_img("buttons/btn_play.png", utils.btn_size(play_w))
    play_rect = play_img.get_rect(center=(play_cx, play_cy))

    # Left-side icon buttons (leaderboard, info, settings)
    icon_w   = int(WIDTH * 0.12)
    icon_x   = int(WIDTH * 0.054)
    icon_top = int(HEIGHT * 0.64)
    icon_gap = int(HEIGHT * 0.020)

    _iw, _ih = utils.btn_size(icon_w)
    leaderboard_img = utils.load_img("buttons/btn_leaderboard.png", (_iw, _ih))
    info_img        = utils.load_img("buttons/btn_info.png",        (_iw, _ih))
    settings_img    = utils.load_img("buttons/btn_settings.png",    (_iw, _ih))

    leaderboard_rect = leaderboard_img.get_rect(center=(icon_x, icon_top))
    info_rect        = info_img.get_rect(center=(icon_x, icon_top + _ih + icon_gap))
    settings_rect    = settings_img.get_rect(center=(icon_x, icon_top + (_ih + icon_gap) * 2))

    # Close (X) button — top-right
    close_w  = int(WIDTH * 0.12)
    close_rx = int(WIDTH * 0.992)
    close_ty = int(HEIGHT * 0.02)
    close_img  = utils.load_img("buttons/btn_close.png", utils.btn_size(close_w))
    close_rect = close_img.get_rect(topright=(close_rx, close_ty))

    # ════════════════════════════════════════════════════════════════════

    main_menu_buttons = [
        {"img": play_img,        "rect": play_rect,        "cb": _on_play,        "pressed_at": 0},
        {"img": leaderboard_img, "rect": leaderboard_rect, "cb": _on_leaderboard, "pressed_at": 0},
        {"img": info_img,        "rect": info_rect,        "cb": _on_info,        "pressed_at": 0},
        {"img": settings_img,    "rect": settings_rect,    "cb": _on_settings,    "pressed_at": 0},
        {"img": close_img,       "rect": close_rect,       "cb": _on_close,       "pressed_at": 0},
    ]

    TAP_PAD = int(min(WIDTH, HEIGHT) * 0.03)

    # Popups live inside main_menu since they only ever appear here
    leaderboards.init(WIDTH, HEIGHT, _close_popup)
    info.init(WIDTH, HEIGHT, _close_popup)
    settings.init(WIDTH, HEIGHT, _close_popup)


# ── Popup open/close ─────────────────────────────────────────────────────────
def _open_popup(name):
    global active_popup
    active_popup = name


def _close_popup():
    global active_popup
    active_popup = None


# ── Button callbacks ──────────────────────────────────────────────────────────
def _on_play():        _go_to_scene("level_select")
def _on_leaderboard():  _open_popup("leaderboard")
def _on_info():          _open_popup("info")
def _on_settings():     _open_popup("settings")
def _on_close():        pygame.quit(); sys.exit()


# ── Tap handling ───────────────────────────────────────────────────────────────
def _hit_rect(btn):
    """Expanded hit-rect with tap padding on all sides."""
    r = btn["rect"]
    return pygame.Rect(r.x - TAP_PAD, r.y - TAP_PAD, r.width + TAP_PAD * 2, r.height + TAP_PAD * 2)


def _handle_button_tap(px, py):
    """Fire the first button hit; stop so only one action fires per tap."""
    for btn in main_menu_buttons:
        if _hit_rect(btn).collidepoint(px, py):
            btn["pressed_at"] = time.time()
            btn["cb"]()
            break


def handle_tap(px, py):
    if active_popup == "leaderboard":
        leaderboards.handle_tap(px, py)
    elif active_popup == "info":
        info.handle_tap(px, py)
    elif active_popup == "settings":
        settings.handle_tap(px, py)
    else:
        _handle_button_tap(px, py)


# ── Drawing ────────────────────────────────────────────────────────────────────
def _draw_button(surf, btn):
    img  = btn["img"]
    rect = btn["rect"]
    if time.time() - btn["pressed_at"] < config.PRESS_DURATION:
        new_w = int(rect.width  * config.PRESS_SCALE)
        new_h = int(rect.height * config.PRESS_SCALE)
        scaled = pygame.transform.smoothscale(img, (new_w, new_h))
        surf.blit(scaled, scaled.get_rect(center=rect.center))
    else:
        surf.blit(img, rect)


def draw(surf):
    surf.blit(bg_image, (0, 0))
    surf.blit(logo_image, logo_rect)
    for btn in main_menu_buttons:
        _draw_button(surf, btn)

    if active_popup == "leaderboard":
        leaderboards.draw(surf)
    elif active_popup == "info":
        info.draw(surf)
    elif active_popup == "settings":
        settings.draw(surf)
