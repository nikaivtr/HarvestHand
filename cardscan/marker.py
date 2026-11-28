# ArUco Marker Support
#
# Every physical card carries a small ArUco marker (DICT_4X4_50, top
# right of the art panel). The marker gives three things the colour
# recogniser cannot:
#
#   1. IDENTITY    - a decoded number, not a similarity score.
#   2. ORIENTATION - which way is up, even for a card held sideways or
#                    upside down.
#   3. A STABLE FRAME - the marker is printed at a fixed spot on the
#                    art, so it locates the printed card exactly no
#                    matter how the card was cut or how much white
#                    margin it has. (The detected card OUTLINE varies by
#                    ~8 % with the cut; the marker does not.)
#
# Card IDs: crop cards use their number (CC-03 -> marker 3). Other
# cards are listed in cardscan/marker_ids.json ({"11": "water", ...});
# `python tools/marker_enroll.py` writes that file from your sample
# photos so nothing has to be typed by hand.
#
# Detection notes (measured on the project's real card photos):
#   * the markers are small and have no white quiet zone, so a plain
#     detector fails with even slight blur. A wide adaptive-threshold
#     window plus multi-scale sharpened detection improves recovery;
#     severe or motion blur can still defeat it.
#   * capture at 1280x720 if you can; print the markers larger and with
#     a white margin of at least one cell for much better reliability.
#
# Requires OpenCV with the aruco module (opencv-python >= 4.7, or the
# contrib build on older versions) and NumPy.

import json
import os

DICTIONARY = "DICT_4X4_50"

# Crop box in MARKER units: the marker is the unit square (0,0)-(1,1),
# x to the right along its top edge, y downwards. These bounds frame
# the whole printed card with a small margin; measured so that all
# eight sample cards land in the same place.
CROP_BOX = (-3.45, 1.25, -0.70, 6.40)       # x0, x1, y0, y1

# Action-card markers identify and orient the card, but their varying
# printed size makes CROP_BOX unreliable for framing those cards.
CROP_IDS = frozenset(range(1, 11))

MIN_SIDE_PIXELS = 12.0   # ignore markers smaller than this (in the frame)

IDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "marker_ids.json")

_DETECTOR = None
_DETECTOR_ERROR = None
_ID_MAP = None


class Marker:
    """One decoded marker. `corners` are 4x2 float32 in the ORIGINAL frame,
    in the marker's own printed order (TL, TR, BR, BL), so they carry the
    card's orientation."""

    __slots__ = ("id", "corners", "side")

    def __init__(self, marker_id, corners):
        import numpy as np
        self.id = int(marker_id)
        self.corners = np.asarray(corners, dtype=np.float32).reshape(4, 2)
        c = self.corners
        self.side = float(sum(np.linalg.norm(c[(i + 1) % 4] - c[i])
                              for i in range(4)) / 4.0)

    def __repr__(self):
        return "<Marker id=%d side=%.0fpx>" % (self.id, self.side)


# ── Availability / detector ─────────────────────────────────

def available():
    """True when OpenCV's aruco module can be used."""
    return _get_detector() is not None


def unavailable_reason():
    return _DETECTOR_ERROR


def _get_detector():
    global _DETECTOR, _DETECTOR_ERROR
    if _DETECTOR is not None or _DETECTOR_ERROR is not None:
        return _DETECTOR
    try:
        import cv2
        import numpy  # noqa: F401
        aruco = cv2.aruco
    except (ImportError, AttributeError) as exc:
        _DETECTOR_ERROR = ("OpenCV aruco module not available (%s). Install "
                           "opencv-python >= 4.7 or opencv-contrib-python." % exc)
        return None
    try:
        dict_id = getattr(aruco, DICTIONARY)
        if hasattr(aruco, "ArucoDetector"):                 # OpenCV >= 4.7
            params = aruco.DetectorParameters()
            _tune(params)
            det = aruco.ArucoDetector(aruco.getPredefinedDictionary(dict_id), params)
            _DETECTOR = lambda gray: det.detectMarkers(gray)[:2]
        else:                                               # legacy API
            dictionary = aruco.Dictionary_get(dict_id)
            params = aruco.DetectorParameters_create()
            _tune(params)
            _DETECTOR = lambda gray: aruco.detectMarkers(
                gray, dictionary, parameters=params)[:2]
    except Exception as exc:                                # noqa: BLE001
        _DETECTOR_ERROR = "could not create the ArUco detector: %s" % exc
        return None
    return _DETECTOR


def _tune(params):
    # A wide adaptive-threshold window finds the marker border even when
    # it touches dark artwork (there is no printed quiet zone).
    params.adaptiveThreshWinSizeMin = 3
    params.adaptiveThreshWinSizeMax = 103
    params.adaptiveThreshWinSizeStep = 8
    params.adaptiveThreshConstant = 5


# ── Detection ───────────────────────────────────────────────

# Markers without a quiet zone can be detected at one image scale and
# missed at another, so examine several sizes and sharpened variants.
SCALES = (1280, 960, 640, 1920, 800, 480, 1600)
FAST_SCALES_PER_CALL = 3
_CALL = 0


def _gray_variants(gray):
    import cv2
    yield gray
    yield cv2.addWeighted(gray, 1.8, cv2.GaussianBlur(gray, (0, 0), 3), -0.8, 0)


def detect(rgb, fast=False):
    """Return plausible markers, detected across multiple image scales."""
    global _CALL
    import cv2
    import numpy as np

    detector = _get_detector()
    if detector is None:
        return []
    h, w = rgb.shape[:2]
    long_side = max(h, w)
    gray0 = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    scales = [target for target in SCALES if target <= long_side * 2.0]
    if not scales:
        scales = [long_side]
    if fast and len(scales) > FAST_SCALES_PER_CALL:
        start = (_CALL * FAST_SCALES_PER_CALL) % len(scales)
        scales = [
            scales[(start + index) % len(scales)]
            for index in range(FAST_SCALES_PER_CALL)
        ]
        _CALL += 1

    known = id_map()
    hits = {}
    for target in scales:
        scale = target / float(long_side)
        gray = gray0 if scale == 1.0 else cv2.resize(
            gray0,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC,
        )
        for variant in _gray_variants(gray):
            try:
                corners, ids = detector(variant)
            except cv2.error:
                continue
            if ids is None:
                continue
            for quad, marker_id in zip(corners, ids.ravel()):
                item = Marker(marker_id, np.asarray(quad).reshape(4, 2) / scale)
                if _plausible(item):
                    hits.setdefault(item.id, []).append((target, item))
        if any(marker_id in known and len(found) >= 2
               for marker_id, found in hits.items()):
            break

    found = []
    for marker_id, observations in hits.items():
        if marker_id not in known and len(observations) < 2:
            continue
        item = max(observations, key=lambda observation: observation[0])[1]
        found.append((len(observations), item))
    found.sort(key=lambda result: (-result[0], -result[1].side))
    return [item for _, item in found]


def _plausible(m):
    import numpy as np
    c = m.corners
    sides = [float(np.linalg.norm(c[(i + 1) % 4] - c[i])) for i in range(4)]
    if min(sides) < MIN_SIDE_PIXELS:
        return False
    if max(sides) / max(min(sides), 1e-6) > 1.8:      # must be near-square
        return False
    return True


def best_known(markers):
    """The largest marker whose id belongs to a known card, else None."""
    ids = id_map()
    for m in markers:
        if m.id in ids:
            return m
    return None


def has_crop(marker_id):
    """Whether CROP_BOX reliably frames the card for this marker."""
    return int(marker_id) in CROP_IDS


# ── Marker id <-> card ──────────────────────────────────────

def id_map(reload=False):
    """{marker id: card slug}. Crop cards CC-nn use nn; marker_ids.json adds
    or overrides entries."""
    global _ID_MAP
    if _ID_MAP is not None and not reload:
        return _ID_MAP
    mapping = {}
    try:
        import cardscan.registry as registry
        for card in registry.all_cards():
            cid = card.card_id or ""
            if cid.upper().startswith("CC-") and cid[3:].isdigit():
                mapping[int(cid[3:])] = card.slug
    except Exception:                                       # noqa: BLE001
        pass
    if os.path.isfile(IDS_FILE):
        try:
            with open(IDS_FILE, "r", encoding="utf-8") as fh:
                for key, slug in json.load(fh).items():
                    mapping[int(key)] = str(slug)
        except (OSError, ValueError):
            print("[cardscan] could not read %s" % IDS_FILE)
    _ID_MAP = mapping
    return mapping


def slug_for_id(marker_id):
    return id_map().get(int(marker_id))


def save_id_map(mapping):
    """Write marker_ids.json ({id: slug}); returns the path."""
    global _ID_MAP
    with open(IDS_FILE, "w", encoding="utf-8") as fh:
        json.dump({str(k): v for k, v in sorted(mapping.items())}, fh, indent=2)
    _ID_MAP = None
    return IDS_FILE


# ── Marker-anchored crop ────────────────────────────────────

def _homography(marker, width, height, box):
    import cv2
    import numpy as np
    x0, x1, y0, y1 = box
    dst = np.float32([[(u - x0) / (x1 - x0) * width, (v - y0) / (y1 - y0) * height]
                      for u, v in ((0, 0), (1, 0), (1, 1), (0, 1))])
    return cv2.getPerspectiveTransform(marker.corners, dst)


def card_array(rgb, marker, width, height, supersample=2, box=CROP_BOX):
    """The printed card, upright, framed by the marker (RGB array)."""
    import cv2
    sw, sh = width * supersample, height * supersample
    m = _homography(marker, sw, sh, box)
    big = cv2.warpPerspective(rgb, m, (sw, sh), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_REPLICATE)
    if supersample > 1:
        return cv2.resize(big, (width, height), interpolation=cv2.INTER_AREA)
    return big


def card_quad(marker, box=CROP_BOX):
    """The crop box as a quad in frame coordinates (for overlays)."""
    import cv2
    import numpy as np
    m = _homography(marker, 1.0, 1.0, box)
    inv = np.linalg.inv(m)
    corners = np.float32([[0, 0], [1, 0], [1, 1], [0, 1]]).reshape(-1, 1, 2)
    return cv2.perspectiveTransform(corners, inv).reshape(4, 2)
