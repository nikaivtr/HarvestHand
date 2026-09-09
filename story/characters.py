# ============================================================
#  CharacterLayer
#  Loads character images and slides them on/off screen.
#  You should NOT need to edit this file when adding chapters.
#
#  To add a new character:
#    1. Add their image to img/characters/YourChar/YourChar.png
#    2. Add an entry to CHAR_ASSETS below.
# ============================================================

import pygame
import utils

# Maps the character id used in slide data → image file path
CHAR_ASSETS = {
    "lucas":        "characters/Lucas/lucas_talking.png",
    "lucas_thumbs": "characters/Lucas/lucas_thumbs.png",
    "lucas_wrong":  "characters/Lucas/lucas_wrong.png",
    "lola":         "characters/Lola Marie/lola_worried.png",
    "lola_thumbs":  "characters/Lola Marie/lola_thumbs.png",
    "chef":         "characters/Chef/Chef_Default.png",
    "chef_thumbs":  "characters/Chef/Chef_Default.png",   # placeholder — replace with thumbs-up image
    "chef_wrong":   "characters/Chef/Chef_Default.png",   # placeholder — replace with worried image
    "kapitan":      "characters/Kapitan/kapitan_wrong.png",  # placeholder — replace with neutral image
    "kapitan_wrong": "characters/Kapitan/kapitan_wrong.png",
    "baron":        "characters/Blight Baron/baron_black.png",
}

SLIDE_SPEED = 1600   # pixels per second — how fast characters move on/off screen
DIM_ALPHA   = 90     # 0–255: how dark inactive characters appear (90 = fairly dim)


class _Char:
    """Represents one character on screen."""

    def __init__(self, image: pygame.Surface, side: str, screen_w: int, screen_h: int):
        # Scale image to 93% of screen height, preserving aspect ratio
        target_h = int(screen_h * 0.93)
        ratio    = target_h / image.get_height()
        target_w = int(image.get_width() * ratio)
        self.image = pygame.transform.smoothscale(image, (target_w, target_h))
        self.w = target_w
        self.h = target_h

        # On-screen and off-screen X positions
        if side == "left":
            self.x_on  = int(screen_w * 0.02)
            self.x_off = -(self.w + 10)
        else:  # right
            self.x_on  = int(screen_w * 0.52)
            self.x_off = screen_w + 10

        self.y = screen_h - target_h   # sits at the bottom of the screen
        self.x = float(self.x_off)     # start off-screen
        self._target = float(self.x_on)  # immediately slide in

    def slide_in(self):
        self._target = float(self.x_on)

    def slide_out(self):
        self._target = float(self.x_off)

    def is_offscreen(self) -> bool:
        return self.x == self.x_off and self._target == self.x_off

    def update(self, dt: float):
        """Move toward target at constant speed."""
        diff = self._target - self.x
        step = SLIDE_SPEED * dt
        if abs(diff) <= step:
            self.x = self._target
        else:
            self.x += step if diff > 0 else -step

    def draw(self, surf: pygame.Surface, is_active: bool):
        img = self.image.copy()
        img.set_alpha(255 if is_active else DIM_ALPHA)
        surf.blit(img, (int(self.x), self.y))


class CharacterLayer:
    """Manages all characters visible on screen for the current slide."""

    def __init__(self, screen_w: int, screen_h: int):
        self._w = screen_w
        self._h = screen_h
        self._cache: dict[str, pygame.Surface] = {}
        self._chars: dict[str, _Char] = {}
        self._active: str | None = None

    def _load(self, char_id: str) -> pygame.Surface:
        if char_id not in self._cache:
            path = CHAR_ASSETS.get(char_id)
            if path is None:
                raise ValueError(f"Unknown character: '{char_id}'. Add it to CHAR_ASSETS in story/characters.py")
            self._cache[char_id] = utils.load_img(path)
        return self._cache[char_id]

    def set_slide(self, chars: dict, active_char: str | None):
        """
        chars = {"lucas": "left", "baron": "right", ...}
        active_char = "lucas"
        """
        self._active = active_char

        for cid, char in self._chars.items():
            if cid not in chars:
                char.slide_out()

        for cid, side in chars.items():
            if cid not in self._chars:
                img = self._load(cid)
                self._chars[cid] = _Char(img, side, self._w, self._h)
            else:
                self._chars[cid].slide_in()

    def get_char_bounds(self, char_id: str):
        """Return (x_on, y, w, h) using the target on-screen position, or None."""
        ch = self._chars.get(char_id)
        if ch is None:
            return None
        return (ch.x_on, ch.y, ch.w, ch.h)

    def update(self, dt: float):
        """Update all character positions. Remove any that have fully left the screen."""
        fully_gone = [cid for cid, c in self._chars.items() if c.is_offscreen()]
        for cid in fully_gone:
            del self._chars[cid]

        for char in self._chars.values():
            char.update(dt)

    def draw(self, surf: pygame.Surface):
        for cid, char in self._chars.items():
            char.draw(surf, is_active=(cid == self._active))
