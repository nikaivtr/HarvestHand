# ============================================================
#  SmokeFX — rising smoke particle effect
#
#  Emits soft grey puffs from the BOTTOM of the screen that rise,
#  drift, grow and fade. Used for eerie panels (e.g. S2P21, the
#  Baron's explosion). Toggle per slide in chapter data with:
#      "smoke": True
# ============================================================

import random

import pygame


# ── Tuning knobs ─────────────────────────────────────────────
EMISSION_RATE   = 26.0    # new puffs per second while active
BURST_COUNT     = 55      # puffs for a one-shot burst()
PUFF_LIFE       = (1.6, 2.6)   # seconds: (min, max)
PUFF_RISE       = (140, 260)   # design px/s upward speed: (min, max)
PUFF_DRIFT      = (-60, 60)    # design px/s horizontal drift range
PUFF_START_R    = (0.03, 0.055)  # start radius as fraction of screen width
PUFF_GROW       = (0.10, 0.22)   # radius growth, screen-width fraction/s
PUFF_ALPHA      = (60, 120)      # starting opacity range (0-255)


class _Puff:
    """One smoke particle."""

    __slots__ = ("x", "y", "vx", "vy", "r", "grow", "life", "age", "alpha")

    def __init__(self, screen_w, screen_h, x=None, y=None):
        sx = screen_w / 1920.0    # design px -> screen px (x/speeds)
        sr = min(screen_w / 1920.0, screen_h / 1080.0)  # sizes

        self.x = random.uniform(0, screen_w) if x is None else x
        # Spawn just below the bottom edge so puffs float INTO view.
        self.y = (screen_h + screen_h * 0.06) if y is None else y

        self.vx = random.uniform(*PUFF_DRIFT) * sx
        self.vy = -random.uniform(*PUFF_RISE) * sx
        self.r = random.uniform(*PUFF_START_R) * screen_w
        self.grow = random.uniform(*PUFF_GROW) * screen_w
        self.life = random.uniform(*PUFF_LIFE)
        self.age = 0.0
        self.alpha = random.randint(*PUFF_ALPHA)

    def update(self, dt, wobble):
        self.age += dt
        # Gentle sine wobble so the column breathes instead of
        # rising in a rigid line.
        self.x += (self.vx + wobble) * dt
        self.y += self.vy * dt
        self.r += self.grow * dt

    @property
    def dead(self) -> bool:
        return self.age >= self.life


class SmokeFX:
    """Manages the smoke puffs for one screen size."""

    def __init__(self, screen_w: int, screen_h: int):
        self._w = screen_w
        self._h = screen_h
        self._puffs: list[_Puff] = []
        self._emit_accum = 0.0
        self._wobble_t = random.uniform(0, 10)
        self._sprite_cache: dict[int, pygame.Surface] = {}

    # ── Control ──────────────────────────────────────────────
    def start(self, burst: bool = False):
        """Begin emitting. burst=True also fires one dense burst."""
        if burst:
            for _ in range(BURST_COUNT):
                self._puffs.append(_Puff(self._w, self._h))

    def stop(self):
        """Stop emitting; existing puffs finish fading naturally."""

    def clear(self):
        self._puffs.clear()

    @property
    def alive(self) -> bool:
        return bool(self._puffs)

    # ── Soft puff sprite (cached per radius bucket) ──────────
    def _sprite(self, radius: int) -> pygame.Surface:
        # Bucket to 8px steps so the cache stays tiny.
        key = max(4, int(radius) // 8 * 8)
        surf = self._sprite_cache.get(key)
        if surf is None:
            size = key * 2
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            cx = cy = key
            # Radial gradient: draw circles from the rim inwards with
            # alpha increasing toward the center. Each smaller circle
            # overwrites the center pixels, so the final result is a
            # dense core fading to transparent at the rim.
            for i in range(key, 0, -2):
                a = int(255 * (1 - i / key) ** 1.4)
                pygame.draw.circle(
                    surf, (200, 200, 200, a), (cx, cy), i
                )
            self._sprite_cache[key] = surf
        return surf

    # ── Frame update / draw ──────────────────────────────────
    def update(self, dt: float, emitting: bool):
        self._wobble_t += dt
        # Gentle alternating drift so the column breathes instead of
        # rising in a rigid line.
        wobble = 26 * (self._w / 1920.0) * (
            1 if int(self._wobble_t * 1.3) % 2 == 0 else -1
        )

        if emitting:
            self._emit_accum += EMISSION_RATE * dt
            while self._emit_accum >= 1.0:
                self._emit_accum -= 1.0
                self._puffs.append(_Puff(self._w, self._h))

        for p in self._puffs:
            p.update(dt, wobble)

        self._puffs = [
            p for p in self._puffs
            if not p.dead and p.y + p.r > -self._h * 0.2
        ]

    def draw(self, surf: pygame.Surface):
        for p in self._puffs:
            if p.dead:
                continue
            fade = max(0.0, 1.0 - (p.age / p.life))
            img = self._sprite(int(p.r))
            img = img.copy()
            img.set_alpha(int(p.alpha * fade))
            surf.blit(
                img,
                (int(p.x - p.r), int(p.y - p.r))
            )
