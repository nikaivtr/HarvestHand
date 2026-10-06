# ============================================================
#  Card Registry
#
#  The catalog of physical cards the scanner can recognise.
#
#  Chapter slides name a card as a display string, e.g.
#      "card": "AC-01 Water Card"
#  resolve() turns that into a slug ("water") which the
#  recognition model is trained against.
#
#  To add a new card:
#    1. add an entry to CARDS below
#    2. put sample photos in data/card_samples/<slug>/
#    3. run:  python tools/train_cards.py
#
#  Nothing here imports pygame or cv2, so this file is safe to
#  read from the training tools on a machine with no camera.
# ============================================================


class Card:
    """One physical card: its identity plus the names we accept for it."""

    __slots__ = ("slug", "card_id", "name", "aliases", "enabled")

    def __init__(self, slug, card_id, name, aliases=(), enabled=True):
        self.slug    = slug
        self.card_id = card_id          # e.g. "AC-01"
        self.name    = name             # e.g. "Water Card"
        self.aliases = tuple(aliases)   # extra strings that should match
        self.enabled = enabled

    @property
    def display(self):
        """The canonical string, matching the chapter data format."""
        return f"{self.card_id} {self.name}"

    def __repr__(self):
        return f"<Card {self.slug} ({self.display})>"


# ── The catalog ─────────────────────────────────────────────
# slug is the folder name under data/card_samples/ and the key
# the model is trained on. card_id / name mirror the chapter data.
CARDS = [
    Card("water",     "AC-01", "Water Card",
         aliases=("water card", "ac-01", "ac01")),
    Card("fertilizer", "AC-02", "Fertilizer Card",
         aliases=("fertilizer card", "ac-02", "ac02")),

    # ── Requested, not yet present in the chapter data ──────
    # These two are registered and trainable, but no slide
    # asks for them yet.
    Card("heal",      "AC-06", "Heal Card",
         aliases=("heal card", "healing card", "ac-06", "ac06")),
    Card("shield",    "AC-07", "Shield Card",
         aliases=("shield card", "ac-07", "ac07")),

    # ── Already used by the chapters ───────────────────────
    Card("weed",      "AC-03", "Weed Removal Card",
         aliases=("weed removal card", "weed card", "ac-03", "ac03")),
    Card("pesticide", "AC-04", "Pesticide Card",
         aliases=("pesticide card", "ac-04", "ac04")),
    Card("harvest",   "AC-05", "Harvest Card",
         aliases=("harvest card", "ac-05", "ac05")),
]

_BY_SLUG  = {c.slug: c for c in CARDS}
_BY_ORDER = list(CARDS)


def all_cards(enabled_only=False):
    """Every card, in catalog order."""
    if enabled_only:
        return [c for c in CARDS if c.enabled]
    return list(_BY_ORDER)


def get(slug):
    """Look a card up by slug, or None."""
    if not slug:
        return None
    return _BY_SLUG.get(str(slug).strip().lower())


def slugs(enabled_only=False):
    return [c.slug for c in all_cards(enabled_only)]


def _normalise(text):
    """Lower-case and collapse punctuation to single spaces."""
    out = []
    for ch in str(text).lower():
        out.append(" " if not ch.isalnum() else ch)
    return " ".join("".join(out).split())


def resolve(text):
    """Map a chapter's card string to a Card.

    Accepts the full display string ("AC-01 Water Card"), a bare
    slug ("water"), an alias, or a loose phrase containing one
    ("Scan the Water Card to ..."). Returns None if unknown.

    The longest match wins, so "weed removal card" is not
    swallowed by a shorter alias.
    """
    if not text:
        return None
    haystack = _normalise(text)
    if not haystack:
        return None

    best = None
    best_len = 0
    for card in _BY_ORDER:
        needles = (card.slug, card.name, card.card_id) + card.aliases
        for needle in needles:
            n = _normalise(needle)
            if not n:
                continue
            # Word-boundary match so "heal" does not fire inside
            # "health" or "wheat".
            if f" {n} " in f" {haystack} " and len(n) > best_len:
                best, best_len = card, len(n)
    return best
