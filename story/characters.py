# ============================================================
#  CharacterLayer  (resolution-scaled version)
#
#  What changed vs. the old version:
#    1. Sizes are no longer fixed pixels. Everything is authored
#       in "design pixels" (your Figma frame) and multiplied by a
#       scale factor so it looks the same on 1280x720, 1920x1080,
#       2560x1440, etc.
#    2. The old "crop transparent padding + shrink to fit 80% x 90%
#       of 409x727" step is GONE. That step was what made wide poses
#       (like Lucas with his arm out) shrink.
#       Now the full PNG canvas is scaled by ONE number
#       (CHARACTER_SCALE), exactly like placing the PNG in Figma.
#    3. Drop-shadow silhouette is cached instead of rebuilt every frame.
#    4. The dialogue-box layout uses its own slot width
#       (CHARACTER_SLOT_DESIGN_W), so characters can be big and
#       overlap the box like in your Figma mockup.
# ============================================================

import pygame
import utils


# ============================================================
# DESIGN SPACE  (set these to your FIGMA FRAME size)
# ============================================================
DESIGN_W = 1920
DESIGN_H = 1080


# ============================================================
# CHARACTER SIZE  <-- THE MAIN KNOB
# ============================================================
# 1.0 = the PNG canvas (409 x 727) at 1:1 in design pixels.
# 1.5 = 50% bigger  (613 x 1090 in a 1920x1080 design)
#
# To match Figma exactly:
#     CHARACTER_SCALE = (character layer WIDTH in Figma) / 409
#     (assuming DESIGN_W/DESIGN_H equal your Figma frame size)
CHARACTER_SCALE = 1.5

# Push characters down (design px). Positive = hangs off the
# bottom of the screen (Figma-style crop). 0 = feet on the edge.
CHARACTER_BOTTOM_OFFSET = 0


# ============================================================
# LAYOUT SLOT USED BY THE DIALOGUE BOX
# ============================================================
# Horizontal space (design px) the dialogue box reserves per
# character. Smaller than the character's drawn width on purpose,
# so the artwork overlaps the box a little (like in Figma).
CHARACTER_SLOT_DESIGN_W = 409


def get_slot_width(screen_w: int) -> int:
    """Slot width in real screen pixels (used by story_scene)."""
    return int(CHARACTER_SLOT_DESIGN_W * screen_w / DESIGN_W)


# ============================================================
# CHARACTER ZONES (design px)
# ============================================================
LEFT_ZONE_LEFT = 40
LEFT_ZONE_RIGHT = 900

RIGHT_ZONE_LEFT = 1050
RIGHT_ZONE_RIGHT = 1918

# Extra outward nudge (design px) applied AFTER the zone/position
# math: left-side characters are pushed further LEFT and right-side
# characters further RIGHT, so they hug the screen edges and overlap
# the dialogue box less.
LEFT_EDGE_PUSH = 140
RIGHT_EDGE_PUSH = 140


# ============================================================
# MOVEMENT / DIMMING / SHADOW
# ============================================================
SLIDE_SPEED = 1600          # design px per second

DIM_INACTIVE = False
DIM_ALPHA = 90

SHADOW_ALPHA = 64
SHADOW_COLOR = (0, 0, 0)

RIGHT_SHADOW_X = 10
RIGHT_SHADOW_Y = 0
LEFT_SHADOW_X = -10
LEFT_SHADOW_Y = 10


# ============================================================
# CHARACTER ASSETS
# ============================================================
CHAR_ASSETS = {

    "lucas": {
        "default": "characters/Lucas/Lucas-default.png",
        "talking": "characters/Lucas/Lucas-talking.png",
        "thumbs": "characters/Lucas/Lucas-thumbs.png",
        "wrong": "characters/Lucas/Lucas-wrong.png",
        "concerned": "characters/Lucas/Lucas-concerned.png",
        "afraid": "characters/Lucas/Lucas-afraid.png",
        "confused": "characters/Lucas/Lucas-confused.png",
        "defense": "characters/Lucas/Lucas-defense.png",
        "determined": "characters/Lucas/Lucas-determined.png",
        "waters": "characters/Lucas/Lucas-waters.png",
    },

    "lola": {
        "worried": "characters/Lola Marie/lola_worried.png",
        "thumbs": "characters/Lola Marie/Lola-thumbs.png",
        "tired": "characters/Lola Marie/lola_tired.png",
        "sad": "characters/Lola Marie/Lola-sad.png",
        "default": "characters/Lola Marie/Lola-default.png",
        "shocked": "characters/Lola Marie/lola_shocked.png",
        "angry": "characters/Lola Marie/Lola-angry.png",
        "celebrates": "characters/Lola Marie/lola_celebrates.png",
    },

    "baron": {
        "default": "characters/Blight Baron/Baron-default.png",
        "angry": "characters/Blight Baron/Baron-angry.png",
        "smile": "characters/Blight Baron/Baron-sinister.png",
        "renewed": "characters/Blight Baron/Baron-renewed.png",
        "nervous": "characters/Blight Baron/Baron-nervous.png",
        "laugh": "characters/Blight Baron/Baron-laugh.png",
        "defeated": "characters/Blight Baron/Baron-defeated.png",
        "explosion": "characters/Blight Baron/explosion.png",
    },

    # Old single-image format
    "chef": "characters/Chef/Chef_Default.png",
    "chef_thumbs": "characters/Chef/Chef_Default.png",
    "chef_wrong": "characters/Chef/Chef_Default.png",
    "kapitan": "characters/Kapitan/kapitan_wrong.png",
    "kapitan_wrong": "characters/Kapitan/kapitan_wrong.png",
}


# ============================================================
# CHARACTER COLOUR FILTERS
# ============================================================
# Optional per-character "look" applied to every loaded expression.
# Each entry keys on the character id and supports:
#
#   "except"     expressions left completely untouched
#   "grayscale"  True → desaturate the sprite (Saturation -100)
#   "brightness" 0..1 multiplier on RGB (crushes Exposure /
#                Contrast / Highlights / Shadows toward dark)
#
# Baron's "dark and eerie" look emulates these editor settings:
#     Exposure -100, Contrast -100, Saturation -100,
#     Temperature 0, Tint 0, Highlights -100, Shadows -100
# on EVERY expression except "renewed" (his purified form).
CHAR_FILTERS = {
    "baron": {
        "except": {"renewed"},
        "grayscale": True,
        "brightness": 0.30,   # 0 = pure black, 1 = untouched
    },
}


def _apply_char_filter(
    char_id: str,
    expression: str,
    img: pygame.Surface,
) -> pygame.Surface:
    """Apply a character's colour filter to a loaded sprite, unless
    the expression is exempt (e.g. baron's "renewed"). Runs once per
    (character, expression) — CharacterLayer._load() caches the
    result, so the per-pixel work is never repeated per frame."""
    filt = CHAR_FILTERS.get(char_id)
    if not filt or expression in filt.get("except", ()):
        return img

    out = img

    if filt.get("grayscale"):
        out = pygame.transform.grayscale(out)

    brightness = filt.get("brightness", 1.0)
    if 0 <= brightness < 1.0:
        if out is img:
            out = out.copy()   # never mutate the cached original
        v = max(0, min(255, int(255 * brightness)))
        # BLEND_RGB_MULT touches RGB only, so the sprite's alpha
        # channel (its silhouette) is preserved.
        out.fill((v, v, v), special_flags=pygame.BLEND_RGB_MULT)

    return out


# ============================================================
# CHARACTER OBJECT
# ============================================================

class _Char:
    """One character on screen."""

    def __init__(
        self,
        image: pygame.Surface,
        side: str,
        screen_w: int,
        screen_h: int,
        flip_x: bool = False,
        position: float = 0.5,
    ):
        self._screen_w = screen_w
        self._screen_h = screen_h

        # design px -> screen px
        self._sx = screen_w / DESIGN_W                       # for x positions
        self._ui = min(screen_w / DESIGN_W,                  # for sizes
                       screen_h / DESIGN_H)

        self.side = side
        self.flip_x = flip_x
        self.position = max(0.0, min(1.0, float(position)))

        # Forced dim, set from the chapter data ("dim_inactive" on a
        # character spec). Used e.g. for fourth-wall-break panels where
        # a non-speaking character should sink into the background.
        self.dimmed = False

        self.set_image(image, flip_x)
        self._calculate_zone()
        self._calculate_position()

        self.x = float(self.x_off)          # start off-screen
        self._target = float(self.x_on)

    # --------------------------------------------------------
    def _calculate_zone(self):
        if self.side == "left":
            zl, zr = LEFT_ZONE_LEFT, LEFT_ZONE_RIGHT
        else:
            zl, zr = RIGHT_ZONE_LEFT, RIGHT_ZONE_RIGHT

        self.zone_left = max(0, min(self._screen_w, int(zl * self._sx)))
        self.zone_right = max(self.zone_left,
                              min(self._screen_w, int(zr * self._sx)))

    # --------------------------------------------------------
    def _calculate_position(self):
        """
        position 0.0 = character's left edge at zone's left edge
        position 1.0 = character's right edge at zone's right edge
        If the character is wider than the zone, available_width is
        negative, so it overhangs evenly instead of getting stuck.
        """
        zone_width = self.zone_right - self.zone_left
        available = zone_width - self.w          # may be negative

        if self.side == "center":
            # Centered on the screen, ignoring zones/push/position.
            self.x_on = (self._screen_w - self.w) // 2
        else:
            self.x_on = self.zone_left + int(available * self.position)

            # Nudge characters outward so they hug the screen edges and
            # overlap the dialogue box less. Left-side characters shift
            # further LEFT, right-side characters further RIGHT.
            if self.side == "left":
                self.x_on -= int(LEFT_EDGE_PUSH * self._sx)
                # Never push more than half the character off-screen.
                self.x_on = max(self.x_on, -(self.w // 2))
            else:
                self.x_on += int(RIGHT_EDGE_PUSH * self._sx)
                self.x_on = min(self.x_on, self._screen_w - (self.w // 2))

        if self.side == "left" or self.side == "center":
            self.x_off = -(self.w + 10)
        else:
            self.x_off = self._screen_w + 10

    # --------------------------------------------------------
    def set_image(self, image: pygame.Surface, flip_x: bool = False):
        """
        Scale the FULL PNG canvas by one uniform factor.
        No cropping, no fit-to-frame, so every expression keeps
        exactly the same size and alignment (same as Figma).
        """
        self.flip_x = flip_x

        scale = CHARACTER_SCALE * self._ui
        w = max(1, int(image.get_width() * scale))
        h = max(1, int(image.get_height() * scale))

        img = pygame.transform.smoothscale(image, (w, h))
        if flip_x:
            img = pygame.transform.flip(img, True, False)

        self.image = img
        self.w = w
        self.h = h

        # Bottom-aligned (optionally hanging off the bottom edge)
        self.y = (self._screen_h - h
                  + int(CHARACTER_BOTTOM_OFFSET * self._ui))

        # Cache the shadow silhouette once per image
        mask = pygame.mask.from_surface(img, threshold=1)
        self._shadow = mask.to_surface(
            setcolor=(SHADOW_COLOR[0], SHADOW_COLOR[1],
                      SHADOW_COLOR[2], SHADOW_ALPHA),
            unsetcolor=(0, 0, 0, 0),
        )

    # --------------------------------------------------------
    def slide_in(self):
        self._target = float(self.x_on)

    def slide_out(self):
        self._target = float(self.x_off)

    def is_offscreen(self) -> bool:
        return self.x == self.x_off and self._target == self.x_off

    def update(self, dt: float):
        diff = self._target - self.x
        step = SLIDE_SPEED * self._sx * dt

        if abs(diff) <= step:
            self.x = self._target
        elif diff > 0:
            self.x += step
        else:
            self.x -= step

    # --------------------------------------------------------
    def draw(self, surf: pygame.Surface, is_active: bool, dim_others: bool = False):
        if self.side == "right":
            sx, sy = RIGHT_SHADOW_X, RIGHT_SHADOW_Y
        elif self.side == "center":
            sx, sy = 0, 0
        else:
            sx, sy = LEFT_SHADOW_X, LEFT_SHADOW_Y

        sx = int(sx * self._ui)
        sy = int(sy * self._ui)

        surf.blit(self._shadow, (int(self.x) + sx, self.y + sy))

        # self.dimmed   → forced dim from the chapter data, regardless
        #                 of who is speaking (e.g. S2P7 fourth-wall break).
        # dim_others / DIM_INACTIVE → dim every character that is NOT
        #                 the active speaker.
        dim_this = self.dimmed or (
            (DIM_INACTIVE or dim_others) and not is_active
        )

        if dim_this:
            img = self.image.copy()
            img.set_alpha(DIM_ALPHA)
        else:
            img = self.image

        surf.blit(img, (int(self.x), self.y))


# ============================================================
# CHARACTER LAYER
# ============================================================

class CharacterLayer:
    """Manages all characters visible on the current slide."""

    def __init__(self, screen_w: int, screen_h: int):
        self._w = screen_w
        self._h = screen_h
        self._cache: dict[tuple[str, str], pygame.Surface] = {}
        self._chars: dict[str, _Char] = {}
        self._active: str | None = None
        self._dim_others = False

    # --------------------------------------------------------
    def _load(self, char_id: str, expression: str = "default") -> pygame.Surface:
        assets = CHAR_ASSETS.get(char_id)

        if assets is None:
            raise ValueError(
                f"Unknown character: '{char_id}'. "
                "Add it to CHAR_ASSETS in story/characters.py"
            )

        # "lucas_talking" -> "talking"
        if isinstance(assets, dict):
            prefix = char_id + "_"
            if expression.startswith(prefix):
                expression = expression[len(prefix):]

        key = (char_id, expression)

        if key not in self._cache:
            if isinstance(assets, dict):
                path = assets.get(expression)
                if path is None:
                    # A panel asked for art that doesn't exist yet
                    # (e.g. baron's "explosion"). Keep the story
                    # running on the character's default sprite.
                    print(
                        f"[characters] unknown expression "
                        f"'{expression}' for '{char_id}' — using default"
                    )
                    path = assets.get("default") or next(iter(assets.values()))
            else:
                path = assets

            self._cache[key] = _apply_char_filter(
                char_id, expression, utils.load_img(path)
            )

        return self._cache[key]

    # --------------------------------------------------------
    def set_slide(
        self,
        chars: dict,
        active_char: str | None,
        dim_others: bool = False,
    ):
        self._active = active_char
        self._dim_others = dim_others

        for cid, char in list(self._chars.items()):
            if cid not in chars:
                char.slide_out()

        for cid, spec in chars.items():
            if isinstance(spec, str):
                side, expression, flip_x, position = spec, "default", False, 0.5
            else:
                side = spec.get("side", "left")
                expression = spec.get("expression", "default")
                flip_x = spec.get("flip", False)
                position = spec.get("position", 0.5)

            img = self._load(cid, expression)

            dim_flag = (
                spec.get("dim_inactive", False)
                if isinstance(spec, dict)
                else False
            )

            if cid not in self._chars:
                self._chars[cid] = _Char(
                    img, side, self._w, self._h, flip_x, position
                )
            else:
                char = self._chars[cid]
                char.side = side
                char.position = max(0.0, min(1.0, float(position)))
                char._calculate_zone()
                char.set_image(img, flip_x)
                char._calculate_position()
                char.slide_in()

            self._chars[cid].dimmed = bool(dim_flag)

    # --------------------------------------------------------
    def get_char_bounds(self, char_id: str):
        ch = self._chars.get(char_id)
        if ch is None:
            return None
        return (ch.x_on, ch.y, ch.w, ch.h)

    # --------------------------------------------------------
    def update(self, dt: float):
        gone = [cid for cid, c in self._chars.items() if c.is_offscreen()]
        for cid in gone:
            del self._chars[cid]

        for char in self._chars.values():
            char.update(dt)

    # --------------------------------------------------------
    def draw(self, surf: pygame.Surface):
        for cid, char in self._chars.items():
            is_active = True if self._active is None else (cid == self._active)
            char.draw(surf, is_active=is_active, dim_others=self._dim_others)