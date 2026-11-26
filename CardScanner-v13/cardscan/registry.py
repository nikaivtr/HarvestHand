# ============================================================
#  Card Registry
#
#  The catalog of physical cards the scanner can recognise.
#
#  Chapter slides name a card as a display string, e.g.
#      "card": "AC-01 Watering Can"
#  resolve() turns that into a slug ("water") which the
#  recognition model is trained against.
#
#  To add a new card:
#    1. add an entry to CARDS below
#    2. put sample photos in data/card_samples/<sample_folder>/
#    3. run:  python tools/train_cards.py
#
#  Nothing here imports pygame or cv2, so this file is safe to
#  read from the training tools on a machine with no camera.
# ============================================================


class Card:
    """One physical card: its identity plus the names we accept for it."""

    __slots__ = (
        "slug", "sample_folder", "card_id", "name", "aliases", "enabled", "details"
    )

    def __init__(
        self, slug, card_id, name, aliases=(), enabled=True, details=None,
        sample_folder=None,
    ):
        self.slug    = slug
        self.sample_folder = sample_folder or slug
        self.card_id = card_id          # e.g. "AC-01"
        self.name    = name             # e.g. "Water Card"
        self.aliases = tuple(aliases)   # extra strings that should match
        self.enabled = enabled
        self.details = dict(details or {})

    @property
    def display(self):
        """The canonical string, matching the chapter data format."""
        return f"{self.card_id} {self.name}".strip()

    def __repr__(self):
        return f"<Card {self.slug} ({self.display})>"


# ── The catalog ─────────────────────────────────────────────
# slug is the model key; sample_folder is the matching directory under
# data/card_samples/. card_id / name mirror the physical card details.
CARDS = [
    Card("water",     "AC-01", "Watering Can",
         aliases=("water card", "diligan", "ac-01", "ac01"),
         sample_folder="watering_can",
         details={
             "effect": "Water one plant or advance water-based goals.",
             "when_to_use": "When a crop needs water or water progress.",
         }),
    Card("organic_fertilizer", "AC-02A", "Organic Fertilizer Card",
         aliases=(
             "organic fertilizer", "organikong pataba", "fertilizer card",
             "ac-02", "ac02", "ac-02a", "ac02a",
         ),
         details={
             "effect": "Add 1 water or fertilizer progress; keep soil healthy.",
             "when_to_use": "When a crop needs water or fertilizer progress.",
         }),
    Card("chemical_fertilizer", "AC-02B", "Chemical Fertilizer Card",
         aliases=("chemical fertilizer", "kemikal na pataba", "ac-02b", "ac02b"),
         details={
             "effect": "Add 1 fertilizer progress, but harms soil organisms.",
             "when_to_use": "When fertilizer progress is needed; minimize use.",
         }),
    Card("weed", "AC-03", "Weed Removal Card",
         aliases=("weed removal", "weed card", "pagtanggal ng damo", "ac-03", "ac03"),
         sample_folder="weed_removal",
         details={
             "effect": "Remove all weeds and advance weed-based goals.",
             "when_to_use": "When weeds must be removed to advance a goal.",
         }),
    Card("natural_pesticide", "AC-04A", "Natural Pesticide Card",
         aliases=(
             "natural pesticide", "natural na pestisidyo", "pesticide card",
             "ac-04", "ac04", "ac-04a", "ac04a",
         ),
         details={
             "effect": "Remove all pests without harming beneficial organisms.",
             "when_to_use": "To remove pests while protecting beneficial organisms.",
         }),
    Card("chemical_pesticide", "AC-04B", "Chemical Pesticide Card",
         aliases=("chemical pesticide", "kemikal na pestisidyo", "ac-04b", "ac04b"),
         details={
             "effect": "Remove all pests, including beneficial organisms.",
             "when_to_use": "To remove all pests; this also harms beneficial organisms.",
         }),
    Card("harvest", "AC-05", "Harvest Card",
         aliases=("harvest", "umani", "ac-05", "ac05"),
         details={
             "effect": "Collect a fully grown crop and earn points.",
             "when_to_use": "Only when the crop's maturity indicator appears.",
         }),
    Card("analyze", "", "Analyze Card",
         aliases=("analyzing situation", "analyze card", "analyse card"),
         details={
             "effect": "Identify the crop problem and recommended action.",
             "when_to_use": "Before choosing an action card for an unknown problem.",
         }),

    # ── Crop cards (CC-01 through CC-10) ─────────────────────
    Card("pechay_plant", "CC-01", "Pechay Plant Card",
         aliases=("pechay", "pechay bok choy", "plant pechay"),
         details={
             "filipino": "Pechay", "english": "Pechay (Bok Choy)",
             "days": 30, "season": "Cool / Any", "growth": "Fast",
             "water": 2, "fertilizer": 0, "weeds": 0, "pests": 0,
             "tip": "Shallow planting. Tiny seeds, tiny holes.",
             "fact": "Grows fastest! Great for first-time farmers.",
             "dish": "Pechay Soup",
         }),
    Card("monggo_plant", "CC-02", "Monggo Plant Card",
         aliases=("monggo", "monggo beans", "plant monggo"),
         details={
             "filipino": "Monggo", "english": "Monggo Beans",
             "days": 65, "season": "Any", "growth": "Fast",
             "water": 2, "fertilizer": 0, "weeds": 0, "pests": 0,
             "tip": "Small seed, small hole. Don't crowd them.",
             "fact": "Enriches soil with nitrogen, a natural fertilizer!",
             "dish": "Monggo Guisado",
         }),
    Card("okra_plant", "CC-03", "Okra Plant Card",
         aliases=("okra", "plant okra"),
         details={
             "filipino": "Okra", "english": "Okra",
             "days": 55, "season": "Dry", "growth": "Fast",
             "water": 2, "fertilizer": 0, "weeds": 0, "pests": 0,
             "tip": "Roots grow deep, so water follows the roots.",
             "fact": "Flowers first, then pods grow from the flower.",
             "dish": "Sinigang",
         }),
    Card("squash_plant", "CC-04", "Squash Plant Card",
         aliases=("squash", "kalabasa", "plant squash"),
         details={
             "filipino": "Kalabasa", "english": "Squash",
             "days": 90, "season": "Any", "growth": "Medium",
             "water": 1, "fertilizer": 1, "weeds": 1, "pests": 1,
             "tip": "Loves compost. Feed the soil, not just the leaves.",
             "fact": "A vining crop that needs wide space to crawl and grow.",
             "dish": "Ginataang Kalabasa",
         }),
    Card("tomato_plant", "CC-05", "Tomato Plant Card",
         aliases=("tomato", "kamatis", "plant tomato"),
         details={
             "filipino": "Kamatis", "english": "Tomato",
             "days": 75, "season": "Dry", "growth": "Medium",
             "water": 1, "fertilizer": 1, "weeds": 1, "pests": 1,
             "tip": "Wet leaves = sick plant. Water the base only.",
             "fact": "Starts in a nursery tray, then moves to the soil.",
             "dish": "Sarciado",
         }),
    Card("eggplant_plant", "CC-06", "Eggplant Plant Card",
         aliases=("eggplant", "talong", "plant eggplant"),
         details={
             "filipino": "Talong", "english": "Eggplant",
             "days": 80, "season": "Dry", "growth": "Medium",
             "water": 1, "fertilizer": 1, "weeds": 1, "pests": 1,
             "tip": "Needs deep holes; it gets heavy!",
             "fact": "Keeps producing fruit. Harvest regularly to grow more!",
             "dish": "Kare-Kare",
         }),
    Card("sweet_potato_plant", "CC-07", "Sweet Potato Plant Card",
         aliases=("sweet potato", "kamote", "plant sweet potato"),
         details={
             "filipino": "Kamote", "english": "Sweet Potato",
             "days": 120, "season": "Dry", "growth": "Slow",
             "water": 1, "fertilizer": 1, "weeds": 1, "pests": 0,
             "tip": "Grows from a vine cutting, not a seed.",
             "fact": "Grows from vine cuttings called slips and is ready in about 4 months.",
             "dish": "Kamote Cue",
         }),
    Card("rice_plant", "CC-08", "Rice Plant Card",
         aliases=("rice", "palay", "plant rice"),
         details={
             "filipino": "Palay", "english": "Rice",
             "days": 113, "season": "Wet", "growth": "Slow",
             "water": 1, "fertilizer": 1, "weeds": 2, "pests": 1,
             "tip": "The only crop that wants wet feet.",
             "fact": "A staple food for over half the world's population.",
             "dish": "Sinangag",
         }),
    Card("corn_plant", "CC-09", "Corn Plant Card",
         aliases=("corn", "mais", "plant corn"),
         details={
             "filipino": "Mais", "english": "Corn",
             "days": 102, "season": "Wet", "growth": "Slow",
             "water": 2, "fertilizer": 1, "weeds": 1, "pests": 1,
             "tip": "Needs wind and straight rows to grow strong.",
             "fact": "Needs wind to pollinate. Tassels drop pollen onto the silks.",
             "dish": "Maja Blanca",
         }),
    Card("cassava_plant", "CC-10", "Cassava Plant Card",
         aliases=("cassava", "kamoteng kahoy", "plant cassava"),
         details={
             "filipino": "Kamoteng Kahoy", "english": "Cassava",
             "days": 201, "season": "Dry", "growth": "Slow",
             "water": 1, "fertilizer": 1, "weeds": 1, "pests": 1,
             "tip": "Never eat raw. Must be cooked first!",
             "fact": "Toxic when raw. Always peel, wash, and cook it!",
             "dish": "Cassava Cake",
         }),
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


def crop_card(crop_name):
    """Find a crop card by its chapter crop name or card-language name."""
    target = _normalise(crop_name)
    if not target:
        return None
    for card in _BY_ORDER:
        if not card.card_id.startswith("CC-"):
            continue
        names = (card.details.get("english", ""), card.details.get("filipino", ""))
        if any(_normalise(name) == target for name in names if name):
            return card
    return None


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
