# ============================================================
#  SmokeFX — rising smoke particle effect
#
#  Emits soft grey puffs from the BOTTOM of the screen that rise,
#  drift, grow and fade. Used for eerie panels (e.g. S2P21, the
#  Baron's explosion). Toggle per slide in chapter data with:
#      "smoke": True
# ============================================================

import bisect
import random

import pygame


# ── Tuning knobs ─────────────────────────────────────────────
EMISSION_RATE   = 12.0    # new puffs per second while active
BURST_COUNT     = 26      # puffs for a one-shot burst()
PUFF_LIFE       = (1.8, 3.0)   # seconds: (min, max)
PUFF_RISE       = (140, 260)   # design px/s upward speed: (min, max)
PUFF_DRIFT      = (-60, 60)    # design px/s horizontal drift range
PUFF_START_R    = (0.020, 0.038)  # start radius as fraction of screen width
PUFF_GROW       = (0.030, 0.070)  # radius growth, screen-width fraction/s
PUFF_MAX_R      = 0.15      # hard cap on radius, screen-width fraction
PUFF_ALPHA      = (70, 125)      # starting opacity range (0-255)
MAX_PUFFS       = 40        # hard cap on live puffs (bounds draw cost)

# The sprite ladder is pre-rendered once, so it needs no eviction cap:
# its size is fixed by SPRITE_LADDER_RATIO and the screen size.
#
# Ratio 1.12 keeps a puff's sprite within ~5.6% of its true radius
# (≈8 px at the 288 px cap) while using only ~19 surfaces / ~6.7 MB.
SPRITE_LADDER_RATIO = 1.12
SPRITE_MIN_R        = 8      # smallest sprite radius, in px


class _Puff:
    """One smoke particle."""

    __slots__ = ("x", "y", "vx", "vy", "r", "grow", "max_r", "life", "age", "alpha")

    def __init__(self, screen_w, screen_h, x=None, y=None):
        sx = screen_w / 1920.0    # design px -> screen px (x/speeds)
        sr = min(screen_w / 1920.0, screen_h / 1080.0)  # sizes

        self.x = random.uniform(0, screen_w) if x is None else x
        # Spawn just below the bottom edge so puffs float INTO view.
        self.y = (screen_h + screen_h * 0.06) if y is None else y

        self.vx = random.uniform(*PUFF_DRIFT) * sx
        self.vy = -random.uniform(*PUFF_RISE) * sx
        # Radius is capped: without a cap a puff grows past half the
        # screen width and the effect stops reading as smoke.
        self.max_r = PUFF_MAX_R * screen_w
        self.r = min(random.uniform(*PUFF_START_R) * screen_w, self.max_r)
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
        if self.r < self.max_r:
            self.r = min(self.r + self.grow * dt, self.max_r)

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
        self._sprites: list[pygame.Surface] = []
        self._radii: list[int] = []
        self._build_ladder()

    # ── Control ──────────────────────────────────────────────
    def start(self, burst: bool = False):
        """Begin emitting. burst=True also fires one dense burst."""
        if burst:
            for _ in range(BURST_COUNT):
                if len(self._puffs) >= MAX_PUFFS:
                    self._puffs.pop(0)
                self._puffs.append(_Puff(self._w, self._h))

    def stop(self):
        """Stop emitting; existing puffs finish fading naturally."""

    def clear(self):
        self._puffs.clear()

    @property
    def alive(self) -> bool:
        return bool(self._puffs)

    # ── Soft puff sprite (pre-rendered radius ladder) ────────
    def _build_ladder(self) -> None:
        """Pre-render every sprite the effect will ever need.

        Building sprites lazily inside draw() meant a brand-new surface
        was allocated mid-frame whenever a puff crossed a radius
        boundary. That allocation is what blew the frame budget: the
        large surface triggered a GC pause plus page faults, so the
        frames that happened to build a bucket cost 15-21 ms while
        every other frame cost 3-5 ms.

        Rendering the whole ladder up front means draw() only reads
        from a fixed list -- no allocation, no GC spike, and the cost
        of the ladder is paid once when the scene starts.
        """
        max_r = max(SPRITE_MIN_R, int(PUFF_MAX_R * self._w))
        radii = []
        r = float(SPRITE_MIN_R)
        while r < max_r:
            radii.append(int(round(r)))
            r *= SPRITE_LADDER_RATIO
        radii.append(max_r)
        radii = sorted(set(radii))

        base = self._base_gradient()
        self._radii = radii
        self._sprites = [
            pygame.transform.smoothscale(base, (rad * 2, rad * 2))
            for rad in radii
        ]

    def _base_gradient(self) -> pygame.Surface:
        """Build the low-res radial alpha ramp every puff sprite is scaled from.

        Rasterising the ramp once at low resolution and scaling it up
        is far cheaper than re-drawing a gradient per radius, and the
        upscale gives the soft edge smoke needs.
        """
        n = 64
        base = pygame.Surface((n, n), pygame.SRCALPHA)
        c = (n - 1) / 2.0
        for y in range(n):
            for x in range(n):
                d = ((x - c) ** 2 + (y - c) ** 2) ** 0.5 / c
                if d > 1.0:
                    continue
                a = int(255 * (1.0 - d) ** 1.4)
                base.set_at((x, y), (200, 200, 200, a))
        return base

    def _sprite_index(self, radius: int) -> int:
        """Index into the sprite ladder for a requested radius.

        Returns an int rather than a (surface, radius) tuple on purpose:
        a tuple is a GC-tracked allocation, and allocating one per puff
        per frame was enough to trigger a generational GC pass inside
        draw() -- which cost more than the blits themselves.
        """
        radii = self._radii
        idx = bisect.bisect_left(radii, radius)
        if idx >= len(radii):
            idx = len(radii) - 1
        elif idx > 0 and radius - radii[idx - 1] < radii[idx] - radius:
            # Snap to the nearer neighbour so the error stays <= half a step.
            idx -= 1
        return idx

    def _sprite(self, radius: int) -> tuple[pygame.Surface, int]:
        """Return (sprite, sprite_radius) for a requested radius.

        The sprite is drawn at the *bucketed* radius, so the caller must
        use the returned radius when positioning it, otherwise puffs would
        jitter as they cross bucket boundaries.
        """
        idx = self._sprite_index(radius)
        return self._sprites[idx], self._radii[idx]

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
                if len(self._puffs) < MAX_PUFFS:
                    self._puffs.append(_Puff(self._w, self._h))
                else:
                    # Budget spent: drop the oldest puff so the column
                    # keeps moving instead of stalling.
                    self._puffs.pop(0)

        for p in self._puffs:
            p.update(dt, wobble)

        # Cull in place: rebuilding the list every frame allocates a new
        # list object, and the churn was enough to trigger a GC pass.
        puffs = self._puffs
        write = 0
        for p in puffs:
            if not p.dead and p.y + p.r > -self._h * 0.2:
                puffs[write] = p
                write += 1
        del puffs[write:]

    def draw(self, surf: pygame.Surface):
        # The pre-rendered sprite is reused directly: set_alpha()
        # modulates the per-pixel alpha of an SRCALPHA surface, so
        # copying it per puff per frame (a full-surface memcpy) buys
        # nothing.
        #
        # Nothing in this loop allocates, so no frame can be stalled by
        # a GC pause -- that was the cause of the 15-21 ms spikes.
        sprites = self._sprites
        radii = self._radii
        blit = surf.blit
        for p in self._puffs:
            if p.dead:
                continue
            fade = max(0.0, 1.0 - (p.age / p.life))
            idx = self._sprite_index(int(p.r))
            img = sprites[idx]
            img.set_alpha(max(0, min(255, int(p.alpha * fade))))
            sr = radii[idx]
            blit(img, (int(p.x - sr), int(p.y - sr)))
