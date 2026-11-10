# Card Preprocessing
#
# Turns a raw camera frame (or sample photo) into a normalized
# portrait card image that the feature extractor can compare.
#
# Pipeline:
#   surface -> (optional) card-boundary detection
#            -> perspective warp to fronto-parallel card
#            -> letterbox onto a fixed 5:7 portrait canvas
#            -> pygame Surface (CANVAS_W x CANVAS_H)
#
# Design goals (HarvestHand, Raspberry Pi friendly):
#   * Detect the physical card boundary where possible (OpenCV
#     contours + 4-point perspective warp) so the whole card --
#     border, ID, illustration, name -- is preserved.
#   * Never stretch a portrait card into a square; letterbox to a
#     fixed 5:7 canvas instead.
#   * Handle detection failures gracefully with a centered-crop
#     fallback so the pipeline never crashes.
#   * Keep training and live recognition on the identical path.
#   * Work without numpy where OpenCV/numpy are unavailable: fall
#     back to a pure-Pygame centered crop + letterbox.
#

import pygame

# Bump whenever preprocessing changes so a model trained with an
# older crop is never silently used for live recognition.
PREPROCESS_VERSION = 3

# Normalized canvas: 5:7 portrait (poker-card proportions), never
# stretched. All cards share one template, so a fixed canvas keeps
# every card framed identically.
CANVAS_W = 120
CANVAS_H = 168
CARD_ASPECT = CANVAS_W / CANVAS_H

# Maximum dimension used for OpenCV card-boundary detection.
DETECT_MAX_DIMENSION = 960

# OpenCV/numpy availability (probed lazily).
_HAS_CV2 = None
_HAS_NP = None
_LAST_DETECTION_ERROR = None


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


# Pygame <-> OpenCV conversion (numpy path)

def _surface_to_array(surface):
    _, has_np = _probe()
    if not has_np:
        return None
    import numpy as np
    raw = pygame.image.tobytes(surface, 'RGB')
    w, h = surface.get_size()
    arr = np.frombuffer(raw, dtype=np.uint8).reshape(h, w, 3)
    return arr


def _array_to_surface(arr):
    h, w = arr.shape[:2]
    surf = pygame.Surface((w, h))
    pygame.surfarray.blit_array(surf, arr.transpose(1, 0, 2))
    return surf


def _array_to_gray(arr):
    import cv2
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray


# Card-boundary detection

def _largest_quad_contour(gray):
    import cv2
    import numpy as np

    best = None
    best_score = 0.0
    img_area = gray.shape[0] * gray.shape[1]
    center_x = gray.shape[1] / 2.0
    center_y = gray.shape[0] / 2.0
    center_norm = (center_x * center_x + center_y * center_y) ** 0.5
    edges = cv2.Canny(gray, 50, 150)
    edge_mask = cv2.morphologyEx(
        edges, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=2
    )
    masks = [(edge_mask, 0.04)]
    for threshold in (140, 180):
        _, light_mask = cv2.threshold(
            gray, threshold, 255, cv2.THRESH_BINARY
        )
        light_mask = cv2.morphologyEx(
            light_mask,
            cv2.MORPH_CLOSE,
            np.ones((7, 7), np.uint8),
            iterations=2,
        )
        masks.append((light_mask, 0.06))

    for mask, epsilon in masks:
        contours, _ = cv2.findContours(
            mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 0.003 * img_area or area > 0.85 * img_area:
                continue
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon * peri, True)
            if len(approx) != 4 or not cv2.isContourConvex(approx):
                continue

            (cx, cy), (rect_w, rect_h), _ = cv2.minAreaRect(approx)
            if rect_w <= 0 or rect_h <= 0:
                continue
            aspect = min(rect_w, rect_h) / max(rect_w, rect_h)
            if not 0.48 <= aspect <= 0.92:
                continue

            aspect_score = 1.0 - abs(aspect - CARD_ASPECT) / CARD_ASPECT
            center_distance = (
                (cx - center_x) ** 2 + (cy - center_y) ** 2
            ) ** 0.5
            center_score = max(0.2, 1.0 - center_distance / center_norm)
            score = area * aspect_score * center_score
            if score > best_score:
                best = approx.reshape(4, 2).astype(np.float32)
                best_score = score

    return best


def _order_points(pts):
    import numpy as np
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def _warp_to_card(surface, pts):
    import cv2
    import numpy as np

    rect = _order_points(pts)

    dst = np.array([
        [0, 0],
        [CANVAS_W - 1, 0],
        [CANVAS_W - 1, CANVAS_H - 1],
        [0, CANVAS_H - 1],
    ], dtype=np.float32)
    M = cv2.getPerspectiveTransform(rect, dst)
    arr = _surface_to_array(surface)
    warped = cv2.warpPerspective(arr, M, (CANVAS_W, CANVAS_H))
    return _array_to_surface(warped)


def _fit_into_canvas(src):
    sw, sh = src.get_size()
    if sw < 1 or sh < 1:
        return None
    scale = min(CANVAS_W / sw, CANVAS_H / sh)
    nw = max(1, int(sw * scale))
    nh = max(1, int(sh * scale))
    small = pygame.transform.smoothscale(src, (nw, nh))
    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    canvas.fill((0, 0, 0))
    ox = (CANVAS_W - nw) // 2
    oy = (CANVAS_H - nh) // 2
    canvas.blit(small, (ox, oy))
    return canvas


def _fallback_prepare(surface):
    w, h = surface.get_size()
    if w / h > CARD_ASPECT:
        crop_h = h
        crop_w = max(2, int(crop_h * CARD_ASPECT))
    else:
        crop_w = w
        crop_h = max(2, int(crop_w / CARD_ASPECT))
    crop_w = min(w, crop_w)
    crop_h = min(h, crop_h)
    ox = (w - crop_w) // 2
    oy = (h - crop_h) // 2
    crop = surface.subsurface(pygame.Rect(ox, oy, crop_w, crop_h))
    return _fit_into_canvas(crop)


# Public API

def prepare(surface):
    global _LAST_DETECTION_ERROR
    if surface is None or surface.get_width() < 2 or surface.get_height() < 2:
        return None

    has_cv2, _ = _probe()
    if has_cv2:
        import cv2

        width, height = surface.get_size()
        scale = min(1.0, DETECT_MAX_DIMENSION / max(width, height))
        detection_surface = surface
        if scale < 1.0:
            detection_surface = pygame.transform.smoothscale(
                surface,
                (max(2, int(width * scale)), max(2, int(height * scale))),
            )
        arr = _surface_to_array(detection_surface)
        if arr is not None:
            try:
                gray = _array_to_gray(arr)
                pts = _largest_quad_contour(gray)
                if pts is not None:
                    pts /= scale
                    canvas = _warp_to_card(surface, pts)
                    if canvas is not None:
                        _LAST_DETECTION_ERROR = None
                        return canvas
                _LAST_DETECTION_ERROR = None
            except cv2.error as exc:
                message = str(exc)
                if message != _LAST_DETECTION_ERROR:
                    print(f"[cardscan] card-boundary detection failed: {message}")
                    _LAST_DETECTION_ERROR = message

    return _fallback_prepare(surface)


def load_image(path):
    try:
        return pygame.image.load(path)
    except (pygame.error, FileNotFoundError, OSError):
        return None
