# ============================================================
#  Card Scanner
#
#  The game-facing half of card recognition. It owns the rule the
#  classroom mechanic needs:
#
#      the game asks for a card  ->  the player holds up a card
#      ->  right card advances the panel
#      ->  wrong card is rejected, and the player tries again
#      ->  no confident read simply keeps waiting
#
#  Two ideas do the heavy lifting:
#
#  1. CONFIRM FRAMES. A single frame is never trusted. The same
#     card has to be read confidently several frames in a row
#     before anything is reported, so a card sliding into frame
#     cannot fire a false match.
#
#  2. WRONG CARDS STICK. A rejected card is remembered for a short
#     cooldown, so simply holding up the Fertilizer card does not
#     machine-gun "wrong" at the player. They have to actually
#     take it away and change cards.
#
#  Nothing here touches the game loop or any scene yet. It is a
#  standalone, fully testable unit.
# ============================================================

import cardscan.camera as camera
import cardscan.features as features
import cardscan.model as model
import cardscan.registry as registry


# ── Tuning ──────────────────────────────────────────────────

# Frames the same card must read confidently before it counts.
CONFIRM_FRAMES = 4

# Seconds a rejected card stays suppressed after being reported.
WRONG_COOLDOWN = 1.6

# Seconds to wait after a match before accepting another one, so a
# panel transition is not double-fired.
MATCH_COOLDOWN = 0.8

# Max seconds between frames that still counts as "the card is
# being held there". Beyond this the streak resets, because the
# player has moved something.
MAX_GAP = 0.5


class ScanResult:
    """One outcome from the scanner."""

    __slots__ = ("status", "card", "expected", "score")

    MATCH  = "match"
    WRONG  = "wrong"
    TIMEOUT = "timeout"

    def __init__(self, status, card, expected, score=0.0):
        self.status   = status      # one of MATCH / WRONG / TIMEOUT
        self.card     = card        # slug actually read, or None
        self.expected = expected    # slug the game asked for
        self.score    = score       # similarity 0.0 - 1.0

    @property
    def ok(self):
        """True when the right card was held up."""
        return self.status == self.MATCH

    def __repr__(self):
        return (f"<ScanResult {self.status} read={self.card!r} "
                f"want={self.expected!r} {self.score:.2f}>")


class CardScanner:
    """Holds the recognition state for one scan request.

    Typical use:

        scan = CardScanner()
        scan.start("AC-01 Water Card")

        # once per frame:
        result = scan.update(dt)
        if result and result.ok:
            advance_panel()

    start()  takes the same card string the chapter data uses, so
    it can be handed straight from a slide's "card" field.
    """

    def __init__(self, cam=None, model_data=None,
                 confirm_frames=CONFIRM_FRAMES,
                 wrong_cooldown=WRONG_COOLDOWN):
        self.cam             = cam
        self.model           = model_data if model_data is not None else model.load_model()
        self.confirm_frames  = max(1, int(confirm_frames))
        self.wrong_cooldown  = wrong_cooldown

        self.expected   = None        # slug the game asked for
        self.card       = None        # Card object
        self.active     = False
        self.t          = 0.0

        self.last_slug  = None        # current candidate streak
        self.streak     = 0
        self.last_t     = 0.0
        self.suppress   = {}          # slug -> time it was rejected
        self.match_at   = -99.0

        # Read-only view of the current frame, for a preview later.
        self.frame      = None
        self.last_score = 0.0
        self.saw_frame  = False   # did the last read actually deliver one?

    # ── Setup ────────────────────────────────────────────────

    def open_camera(self, **kwargs):
        self.cam = camera.open_camera(**kwargs)
        return self.cam

    @property
    def trained(self):
        return bool(self.model and self.model.get("cards"))

    def start(self, card_text):
        """Begin waiting for a card.

        `card_text` is the chapter's display string, e.g.
        "AC-01 Water Card". Returns the resolved Card, or None if
        the string is not in the registry.
        """
        card = registry.resolve(card_text)
        self.card     = card
        self.expected = card.slug if card else None
        self.active   = True
        self.t        = 0.0
        self.last_slug = None
        self.streak   = 0
        self.last_t   = 0.0
        self.suppress = {}
        self.match_at = -99.0
        return card

    def stop(self):
        self.active = False
        self.expected = None
        self.card = None
        self.streak = 0
        self.last_slug = None

    def cancel(self):
        """Same as stop(), but also drops the camera."""
        self.stop()
        if self.cam:
            self.cam.release()
            self.cam = None

    # ── Per-frame ────────────────────────────────────────────

    def read_once(self):
        """Grab a single frame and classify it.

        Returns (slug, score, confident) with slug None when there
        is no camera, no model, or no readable frame.
        """
        if self.cam is None or not self.trained:
            self.saw_frame = False
            return None, 0.0, False

        self.frame = self.cam.read()
        self.saw_frame = self.frame is not None
        if self.frame is None:
            return None, 0.0, False

        vec = features.extract(self.frame)
        if vec is None:
            return None, 0.0, False

        slug, score, confident = model.classify(self.model, vec)
        self.last_score = score
        return slug, score, confident

    def update(self, dt):
        """Advance the scanner by one frame.

        Returns a ScanResult when something happened (a match, a
        rejected card), otherwise None.
        """
        if not self.active:
            return None

        self.t += dt
        slug, score, confident = self.read_once()

        if slug is None:
            self.streak = 0
            self.last_slug = None
            return None

        # A long gap means something moved; the streak is stale.
        if self.last_slug is not None and (self.t - self.last_t) > MAX_GAP:
            self.streak = 0
        self.last_t = self.t

        if not confident:
            # Ambiguous or low-confidence: keep waiting quietly
            # rather than telling the player they got it wrong.
            self.streak = 0
            self.last_slug = None
            return None

        if slug != self.last_slug:
            self.last_slug = slug
            self.streak = 1
        else:
            self.streak += 1

        if self.streak < self.confirm_frames:
            return None

        # Confirmed: same card, confidently, several frames running.
        self.streak = 0
        self.last_slug = None

        if slug == self.expected:
            # One card in view should mean one match. Without this the
            # same card would re-match every few frames for as long as
            # it stayed in shot, and the caller could advance twice.
            if (self.t - self.match_at) < MATCH_COOLDOWN:
                return None
            self.match_at = self.t
            return ScanResult(ScanResult.MATCH, slug, self.expected, score)

        until = self.suppress.get(slug, 0.0)
        if self.t < until:
            return None                    # already told them; be quiet

        self.suppress[slug] = self.t + self.wrong_cooldown
        return ScanResult(ScanResult.WRONG, slug, self.expected, score)

    # ── Introspection ────────────────────────────────────────

    def progress(self):
        """0.0 - 1.0 toward a confirmed read, for a loading hint."""
        if not self.active or self.confirm_frames <= 0:
            return 0.0
        return min(1.0, self.streak / float(self.confirm_frames))

    def status(self):
        """One-line summary for logs and the debug overlay."""
        if not self.active:
            return "idle"
        if not self.trained:
            return "no model (run tools/train_cards.py)"
        if self.cam is None or not self.cam.is_open:
            return "camera not open"
        if not self.saw_frame:
            return f"{self.cam.backend} camera returning no frame"
        if self.last_slug is None:
            return f"waiting for {self.expected}"
        return (f"reading {self.last_slug} "
                f"{self.progress() * 100:.0f}% ({self.last_score:.2f})")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.cancel()
        return False

        self.score    = score       # similarity 0.0 - 1.0

    @property
    def ok(self):
        return self.status == self.MATCH

    def __repr__(self):
        return (f"<ScanResult {self.status} read={self.card!r} "
                f"want={self.expected!r} {self.score:.2f}>")
