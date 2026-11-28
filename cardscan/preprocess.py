# Card Preprocessing
#
# Turns a raw camera frame (or sample photo) into a normalized
# portrait card image that the feature extractor can compare.
#
# Pipeline:
#   surface -> cardscan.detect (multi-view card-boundary detection,
#                               ranked candidates)
#           -> perspective warp to a fronto-parallel card
#           -> fixed 5:7 portrait canvas (CANVAS_W x CANVAS_H)
#           -> pygame Surface
#
# v13 replaces the old "contour -> approxPolyDP -> exactly 4 points"
# detector. See cardscan/detect.py for how boundaries are found and
# scored. This module owns everything AFTER detection:
#
#   * supersampled warp (2x, then area-downscale) so thin card features
#     do not alias differently between a sample photo and a live frame
#   * a small inward trim so background never bleeds into the crop
#   * fallbacks, so a failed detection does not have to mean "no read":
#       fallback="training"  an already-cropped card image (e.g. your
#                            card design files) is used whole
#       fallback="guide"     live use: crop the on-screen guide box
#   * guide_rect(): the 5:7 box to draw on the preview so players can
#     fit the card into it
#
# Training and live recognition share this exact path. Requires
# OpenCV + NumPy.

import pygame

# Bump whenever preprocessing changes so a model trained with an
# older crop is never silently used for live recognition.
PREPROCESS_VERSION = 13

# Normalized canvas: 5:7 portrait (poker-card proportions).
CANVAS_W = 120
CANVAS_H = 168
CARD_ASPECT = CANVAS_W / CANVAS_H          # 0.714

WARP_SUPERSAMPLE = 2
QUAD_INSET = 0.012          # trim this fraction off each side of the quad

# Detection runs on a downscaled copy. 480 is as accurate as 640 on the
# benchmark and cheaper; lower it further on a slow Raspberry Pi.
DETECT_MAX_DIMENSION = 480

GUIDE_HEIGHT_RATIO = 0.82   # guide box height / frame height
WHOLE_IMAGE_ASPECT_TOLERANCE = 0.10
BLUR_THRESHOLD = 30.0       # variance-of-Laplacian on a <=640px frame
MIN_LIVE_CARD_AREA_RATIO = 0.10       # variance-of-Laplacian on a <=640px frame
MARKER_MODE = "assist"

# OpenCV/numpy availability (probed lazily).
_HAS_CV2 = None
_HAS_NP = None
_LAST_DETECTION_ERROR = None
_LAST_DETECTION = {
    "status": "not_run",
    "reason": "preprocessing has not run",
}


def _probe():
    global _HAS_CV2, _HAS_NP
    if _HAS_CV2 is None:
        _HAS_NP = _try_import('numpy')
        _HAS_CV2 = _try_import('cv2') and _HAS_NP
    return _HAS_CV2, _HAS_NP


def _try_import(name):
    try:
        __import__(name)
        return True
    except ImportError:
        return False


# ── Pygame <-> OpenCV ───────────────────────────────────────

def _surface_to_array(surface):
    _, has_np = _probe()
    if not has_np:
        return None
    import numpy as np
    raw = pygame.image.tobytes(surface, 'RGB')
    w, h = surface.get_size()
    return np.frombuffer(raw, dtype=np.uint8).reshape(h, w, 3)


def _array_to_surface(arr):
    import numpy as np
    arr = np.ascontiguousarray(arr)
    h, w = arr.shape[:2]
    return pygame.image.frombuffer(arr.tobytes(), (w, h), 'RGB').copy()


def guide_rect(width, height):
    """The 5:7 guide box to draw on the live preview.

    A card fitted inside this box always yields a usable crop, even when
    boundary detection cannot find its edges.
    """
    gh = int(height * GUIDE_HEIGHT_RATIO)
    gw = int(gh * CARD_ASPECT)
    if gw > width * 0.95:
        gw = int(width * 0.95)
        gh = int(gw / CARD_ASPECT)
    return pygame.Rect((width - gw) // 2, (height - gh) // 2, gw, gh)


# ── Detection ───────────────────────────────────────────────

def _sharpness(rgb):
    import cv2
    h, w = rgb.shape[:2]
    scale = min(1.0, 640.0 / max(h, w))
    small = (cv2.resize(rgb, None, fx=scale, fy=scale,
                        interpolation=cv2.INTER_AREA) if scale < 1.0 else rgb)
    gray = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def _details(det, sharp, rank):
    return {
        "status": "detected",
        "reason": "validated card boundary",
        "source": "detected",
        "strategy": det.source,
        "quality": float(det.score),
        "area_ratio": float(det.area_ratio),
        "aspect": float(det.aspect),
        "edge_support": float(det.support),
        "contrast": float(det.contrast),
        "points": [[float(p[0]), float(p[1])] for p in det.corners],
        "candidate_rank": rank,
        "sharpness": round(sharp, 1),
        "blurry": bool(sharp < BLUR_THRESHOLD),
    }


def find_candidates(rgb, max_candidates=3, previous=None):
    """Ranked boundary candidates for an RGB array: [(points, details)].

    `previous` (last frame's quad, optional) nudges the ranking toward
    temporal consistency when tracking live video.
    """
    import numpy as np
    import cardscan.detect as detect

    sharp = _sharpness(rgb)
    found = detect.find_cards(
        rgb, max_dim=DETECT_MAX_DIMENSION,
        max_candidates=max(max_candidates, 6)
        if previous is not None else max_candidates)
    if previous is not None and found:
        prev = np.asarray(previous, np.float32).reshape(4, 2)
        diag = float(np.hypot(rgb.shape[1], rgb.shape[0]))
        for d in found:
            dist = float(np.mean(np.linalg.norm(d.corners - prev, axis=1)))
            d.rank += 0.12 * max(0.0, 1.0 - dist / (0.25 * diag))
        found.sort(key=lambda d: -d.rank)
        found = found[:max_candidates]
    return [(d.corners.astype(np.float32), _details(d, sharp, i))
            for i, d in enumerate(found)]


def detect_quad(rgb, previous=None):
    """Best card boundary: (points 4x2 float32 or None, details)."""
    cands = find_candidates(rgb, 1, previous)
    if cands:
        return cands[0]
    reason = "no card-shaped outline found"
    sharp = _sharpness(rgb)
    if sharp < BLUR_THRESHOLD:
        reason += ("; image is blurry - lock focus or hold the card "
                   "20-30 cm from the lens")
    return None, {"status": "failed", "reason": reason,
                  "sharpness": round(sharp, 1),
                  "blurry": bool(sharp < BLUR_THRESHOLD)}


# Back-compat helpers (older tools/tests call these).
def _find_card_quad(gray):
    import cv2
    return detect_quad(cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB))


def _largest_quad_contour(gray):
    pts, _ = _find_card_quad(gray)
    return pts


def _order_points(pts):
    """TL, TR, BR, BL for a quad (angle sort; safe up to 45 deg tilt)."""
    import numpy as np
    pts = np.asarray(pts, dtype=np.float32).reshape(4, 2)
    c = pts.mean(axis=0)
    ang = np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0])
    pts = pts[np.argsort(ang)]
    return np.roll(pts, -int(np.argmin(pts.sum(axis=1))), axis=0)


# ── Warp ────────────────────────────────────────────────────

def _warp_array(arr, pts):
    """Warp the card quad (TL,TR,BR,BL of a portrait card) to the canvas."""
    import cv2
    import numpy as np

    q = np.asarray(pts, dtype=np.float32).reshape(4, 2)
    c = q.mean(axis=0)
    q = (c + (q - c) * (1.0 - 2.0 * QUAD_INSET)).astype(np.float32)

    sw, sh = CANVAS_W * WARP_SUPERSAMPLE, CANVAS_H * WARP_SUPERSAMPLE
    dst = np.array([[0, 0], [sw - 1, 0], [sw - 1, sh - 1], [0, sh - 1]],
                   dtype=np.float32)
    m = cv2.getPerspectiveTransform(q, dst)
    big = cv2.warpPerspective(arr, m, (sw, sh), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_REPLICATE)
    if WARP_SUPERSAMPLE > 1:
        return cv2.resize(big, (CANVAS_W, CANVAS_H),
                          interpolation=cv2.INTER_AREA)
    return big


def _warp_to_card(surface, pts):
    return _array_to_surface(_warp_array(_surface_to_array(surface), pts))


def _fit_into_canvas(src):
    sw, sh = src.get_size()
    if sw < 1 or sh < 1:
        return None
    scale = min(CANVAS_W / sw, CANVAS_H / sh)
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    small = pygame.transform.smoothscale(src, (nw, nh))
    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    canvas.fill((0, 0, 0))
    canvas.blit(small, ((CANVAS_W - nw) // 2, (CANVAS_H - nh) // 2))
    return canvas


def _fallback_prepare(surface):
    """Centered 5:7 crop (kept for older callers)."""
    w, h = surface.get_size()
    if w / h > CARD_ASPECT:
        crop_h = h
        crop_w = max(2, int(crop_h * CARD_ASPECT))
    else:
        crop_w = w
        crop_h = max(2, int(crop_w / CARD_ASPECT))
    crop_w, crop_h = min(w, crop_w), min(h, crop_h)
    crop = surface.subsurface(pygame.Rect((w - crop_w) // 2,
                                          (h - crop_h) // 2, crop_w, crop_h))
    return _fit_into_canvas(crop)


def center_prepare(surface, height_ratio=GUIDE_HEIGHT_RATIO):
    """Compatibility center crop using the Claude guide rectangle."""
    if surface is None:
        return None
    rect = guide_rect(surface.get_width(), surface.get_height())
    rgb = _surface_to_array(surface)
    if rgb is None:
        return None
    crop = rgb[rect.top:rect.bottom, rect.left:rect.right]
    import cv2
    canvas = cv2.resize(
        crop,
        (CANVAS_W, CANVAS_H),
        interpolation=cv2.INTER_AREA,
    )
    return _array_to_surface(canvas)


# ── Fallbacks ───────────────────────────────────────────────

def _is_card_shaped(w, h):
    ratio = min(w, h) / float(max(w, h))
    return abs(ratio - CARD_ASPECT) <= WHOLE_IMAGE_ASPECT_TOLERANCE * CARD_ASPECT


def _apply_fallback(surface, arr, fallback, details):
    """(canvas, details) for a failed detection, or (None, details)."""
    import cv2
    w, h = surface.get_size()
    if fallback == "training" and _is_card_shaped(w, h):
        img = arr if h >= w else cv2.rotate(arr, cv2.ROTATE_90_CLOCKWISE)
        canvas = cv2.resize(img, (CANVAS_W, CANVAS_H),
                            interpolation=cv2.INTER_AREA)
        return _array_to_surface(canvas), {
            **details, "status": "fallback", "source": "whole_image",
            "reason": "no boundary found; image is already card-shaped"}
    if fallback == "guide":
        r = guide_rect(w, h)
        crop = arr[r.top:r.bottom, r.left:r.right]
        if crop.size == 0:
            return None, details
        canvas = cv2.resize(crop, (CANVAS_W, CANVAS_H),
                            interpolation=cv2.INTER_AREA)
        return _array_to_surface(canvas), {
            **details, "status": "fallback", "source": "guide",
            "reason": "no boundary found; using the guide box"}
    return None, details


# ── Public API ──────────────────────────────────────────────

def _record(details):
    global _LAST_DETECTION
    _LAST_DETECTION = details
    return details


def _find_marker(arr, fast=False):
    import cardscan.marker as marker
    if not marker.available():
        return None
    return marker.best_known(marker.detect(arr, fast=fast))


def _marker_fields(m, arr):
    import cardscan.marker as marker
    sharp = _sharpness(arr)
    return {
        "marker_id": m.id,
        "marker_slug": marker.slug_for_id(m.id),
        "marker_side": round(m.side, 1),
        "sharpness": round(sharp, 1),
        "blurry": bool(sharp < BLUR_THRESHOLD),
    }


def _marker_crop(arr, m):
    import cardscan.marker as marker
    canvas = _array_to_surface(
        marker.card_array(arr, m, CANVAS_W, CANVAS_H, WARP_SUPERSAMPLE))
    return canvas, {
        "status": "detected",
        "reason": "ArUco marker %d" % m.id,
        "source": "marker",
        "strategy": "aruco",
        "quality": 1.0,
        "points": [[float(p[0]), float(p[1])]
                   for p in marker.card_quad(m)],
        **_marker_fields(m, arr),
    }


def _upright_turns(center_xy, size):
    x, y = center_xy[0] / size[0], center_xy[1] / size[1]
    return 180 if x < 0.5 and y > 0.5 else 0


def _identity_candidates(surface, arr, m, candidates, fallback):
    """Use action-card markers for identity/orientation, not card framing."""
    import cv2
    import numpy as np
    import cardscan.marker as marker

    fields = _marker_fields(m, arr)
    center = np.asarray(m.corners, dtype=np.float32).mean(axis=0)
    output = []
    for points, details in candidates:
        canvas = _array_to_surface(_warp_array(arr, points))
        quad = np.asarray(points, dtype=np.float32).reshape(4, 2)
        destination = np.float32([
            [0, 0], [CANVAS_W, 0], [CANVAS_W, CANVAS_H], [0, CANVAS_H]
        ])
        homography = cv2.getPerspectiveTransform(quad, destination)
        cx, cy = cv2.perspectiveTransform(
            center.reshape(1, 1, 2), homography
        ).reshape(2)
        turn = _upright_turns((cx, cy), (CANVAS_W, CANVAS_H))
        if turn:
            canvas = pygame.transform.rotate(canvas, turn)
        output.append((canvas, {
            **details,
            **fields,
            "marker_identity_only": True,
            "oriented_by_marker": True,
        }))

    if not output and fallback:
        canvas, details = _apply_fallback(surface, arr, fallback, {})
        if canvas is not None:
            output.append((canvas, {**details, **fields,
                                   "marker_identity_only": True}))
    return output


def prepare_candidates(surface, max_candidates=3, fallback=None,
                       previous=None, use_marker=None, fast_marker=False):
    """Return [(canvas, details), ...] best boundary first.

    The scanner uses the alternates to let the recognition model veto a
    boundary that is geometrically plausible but wrong (inner frame,
    neighbouring card). Never empty when `fallback` can supply a crop.
    """
    global _LAST_DETECTION_ERROR
    if surface is None or surface.get_width() < 2 or surface.get_height() < 2:
        _record({"status": "failed", "reason": "invalid input surface"})
        return []
    has_cv2, _ = _probe()
    if not has_cv2:
        _record({"status": "failed",
                 "reason": "OpenCV and NumPy are required for card detection"})
        return []
    import cv2
    arr = _surface_to_array(surface)
    if use_marker is None:
        use_marker = MARKER_MODE != "off"
    try:
        identity = None
        if use_marker:
            import cardscan.marker as marker
            m = _find_marker(arr, fast_marker)
            if m is not None:
                if marker.has_crop(m.id):
                    hit = _marker_crop(arr, m)
                    _LAST_DETECTION_ERROR = None
                    _record(hit[1])
                    return [hit]
                identity = m
        cands = find_candidates(arr, max_candidates, previous)
        if identity is not None:
            out = _identity_candidates(surface, arr, identity, cands, fallback)
            if out:
                _LAST_DETECTION_ERROR = None
                _record(out[0][1])
                return out
        if not cands:
            _, details = detect_quad(arr)
            canvas, details = _apply_fallback(surface, arr, fallback, details)
            _record(details)
            return [(canvas, details)] if canvas is not None else []
        out = [(_array_to_surface(_warp_array(arr, pts)), det)
               for pts, det in cands]
        _LAST_DETECTION_ERROR = None
        _record(out[0][1])
        return out
    except cv2.error as exc:
        message = str(exc)
        if message != _LAST_DETECTION_ERROR:
            print(f"[cardscan] card-boundary detection failed: {message}")
            _LAST_DETECTION_ERROR = message
        _record({"status": "failed", "reason": message})
        return []


def prepare_detailed(surface, fallback=None, previous=None):
    """Best (canvas, details); canvas is None when nothing usable."""
    cands = prepare_candidates(surface, 1, fallback, previous)
    if cands:
        return cands[0]
    return None, dict(_LAST_DETECTION)


def prepare(surface, fallback=None):
    """Return a normalized card, or None when no usable crop exists."""
    canvas, _ = prepare_detailed(surface, fallback=fallback)
    return canvas


def last_detection():
    """Details for the most recent preprocessing attempt."""
    return dict(_LAST_DETECTION)


def load_image(path):
    try:
        return pygame.image.load(path)
    except (pygame.error, FileNotFoundError, OSError):
        return None
