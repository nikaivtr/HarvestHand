"""
Shared building blocks for popup panels (leaderboard, info, settings).

Every popup module follows the same init()/handle_tap()/draw() contract as a
scene, but is only ever shown on top of the main menu. These helpers keep the
"rounded panel + title + X button" look consistent without copy-pasting it
into every popup file.
"""

import pygame


def make_panel_rect(width, height, w_pct=0.5, h_pct=0.6):
    panel_w = int(width * w_pct)
    panel_h = int(height * h_pct)
    rect = pygame.Rect(0, 0, panel_w, panel_h)
    rect.center = (width // 2, height // 2)
    return rect


def make_close_rect(panel_rect, width, height, size_pct=0.05, margin=10):
    size = int(min(width, height) * size_pct)
    return pygame.Rect(panel_rect.right - size - margin, panel_rect.top + margin, size, size)


def draw_overlay(surf, width, height):
    """Dim whatever scene is behind the popup."""
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surf.blit(overlay, (0, 0))


def draw_panel_frame(surf, panel_rect, title, title_font_size=56):
    pygame.draw.rect(surf, (40, 40, 50), panel_rect, border_radius=12)
    pygame.draw.rect(surf, (255, 255, 255), panel_rect, width=3, border_radius=12)

    title_font = pygame.font.SysFont(None, title_font_size)
    title_surf = title_font.render(title, True, (255, 255, 255))
    surf.blit(title_surf, title_surf.get_rect(midtop=(panel_rect.centerx, panel_rect.top + 20)))


def draw_close_button(surf, close_rect):
    pygame.draw.rect(surf, (200, 60, 60), close_rect, border_radius=6)
    font = pygame.font.SysFont(None, 32)
    label = font.render("X", True, (255, 255, 255))
    surf.blit(label, label.get_rect(center=close_rect.center))


def tap_closes_popup(px, py, panel_rect, close_rect, close_callback):
    """Standard popup tap behavior: close on the X, or on tapping outside the panel."""
    if close_rect.collidepoint(px, py):
        close_callback()
        return True
    if not panel_rect.collidepoint(px, py):
        close_callback()
        return True
    return False
