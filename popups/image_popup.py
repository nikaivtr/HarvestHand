# ============================================================
#  Image Popup
#  Shown when students tap to reveal a picture during a slide.
#  Any tap dismisses it.
# ============================================================

import pygame
import utils

_W = _H = 0
_image  = None
_rect   = None
_on_dismiss = None


def init(width: int, height: int):
    global _W, _H
    _W, _H = width, height


def open(image_path: str, on_dismiss=None):
    """Load and display an image. Tap anywhere to close."""
    global _image, _rect, _on_dismiss
    _on_dismiss = on_dismiss

    raw = utils.load_img(image_path)

    # Scale to fit within 75% width / 68% height, keeping aspect ratio
    max_w = int(_W * 0.75)
    max_h = int(_H * 0.68)
    scale = min(max_w / raw.get_width(), max_h / raw.get_height())
    new_w = int(raw.get_width()  * scale)
    new_h = int(raw.get_height() * scale)
    _image = pygame.transform.smoothscale(raw, (new_w, new_h))

    _rect = _image.get_rect(center=(_W // 2, _H // 2))


def handle_tap(px: int, py: int) -> bool:
    """Any tap closes the image popup."""
    if _on_dismiss:
        _on_dismiss()
    return True


def draw(surf: pygame.Surface):
    if _image is None:
        return

    overlay = pygame.Surface((_W, _H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surf.blit(overlay, (0, 0))

    surf.blit(_image, _rect)

    font = pygame.font.SysFont(None, int(_H * 0.03))
    hint = font.render("Tap anywhere to close", True, (200, 200, 200))
    surf.blit(hint, hint.get_rect(midbottom=(_W // 2, _rect.bottom + 30)))
