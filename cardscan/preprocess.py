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
#   * Reject unreliable detections explicitly so a bad crop never
#     enters the recognition pipeline.
#   * Keep training and live recognition on the identical path.
#   * Work without numpy where OpenCV/numpy are unavailable: fall
#     back to a pure-Pygame centered crop + letterbox.
#

import pygame

# Bump whenever preprocessing changes so a model trained with an
# older crop is never silently used for live recognition.
PREPROCESS_VERSION = 12

# Normalized canvas: 5:7 portrait (poker-card proportions), never
# stretched. All cards share one template, so a fixed canvas keeps
# every card framed identically.
CANVAS_W = 120
CANVAS_H = 168
CARD_ASPECT = CANVAS_W / CANVAS_H

# Maximum dimension used for OpenCV card-boundary detection.
DETECT_MAX_DIMENSION = 960
MIN_CARD_AREA_RATIO = 0.07
MIN_EDGE_SUPPORT = 0.02
MIN_OPPOSITE_SIDE_RATIO = 0.45
MIN_CORNER_ANGLE = 45.0
MAX_CORNER_ANGLE = 135.0

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

def _quad_metrics(gray, points):
    import cv2
    import numpy as np

    height, width = gray.shape[:2]
    ordered = _order_points(points)
    area = abs(cv2.contourArea(ordered))
    area_ratio = area / float(width * height)
    top = np.linalg.norm(ordered[1] - ordered[0])
    right = np.linalg.norm(ordered[2] - ordered[1])
    bottom = np.linalg.norm(ordered[2] - ordered[3])
    left = np.linalg.norm(ordered[3] - ordered[0])
    horizontal = (top + bottom) / 2.0
    vertical = (left + right) / 2.0
    aspect = min(horizontal, vertical) / max(horizontal, vertical)
    opposite_ratio = min(
        top / max(bottom, 1.0), bottom / max(top, 1.0),
        left / max(right, 1.0), right / max(left, 1.0),
    )

    angles = []
    for i in range(4):
        before = ordered[(i - 1) % 4] - ordered[i]
        after = ordered[(i + 1) % 4] - ordered[i]
        cosine = np.dot(before, after) / (
            max(np.linalg.norm(before) * np.linalg.norm(after), 1.0)
        )
        angles.append(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))

    edges = cv2.Canny(gray, 50, 150)
    support = []
    for start, end in zip(ordered, np.roll(ordered, -1, axis=0)):
        length = max(int(np.linalg.norm(end - start)), 2)
        xs = np.rint(np.linspace(start[0], end[0], length)).astype(int)
        ys = np.rint(np.linspace(start[1], end[1], length)).astype(int)
        good = 0
        for x, y in zip(xs, ys):
            x0, x1 = max(0, x - 2), min(width, x + 3)
            y0, y1 = max(0, y - 2), min(height, y + 3)
            if edges[y0:y1, x0:x1].any():
                good += 1
        support.append(good / float(length))

    center = ordered.mean(axis=0)
    center_distance = np.linalg.norm(
        center - np.array([width / 2.0, height / 2.0])
    )
    center_score = max(
        0.0,
        1.0 - center_distance / np.linalg.norm(
            [width / 2.0, height / 2.0]
        ),
    )
    aspect_score = max(
        0.0, 1.0 - abs(aspect - CARD_ASPECT) / CARD_ASPECT
    )
    edge_support = min(support)
    valid = (
        area_ratio >= MIN_CARD_AREA_RATIO
        and aspect_score >= 0.65
        and opposite_ratio >= MIN_OPPOSITE_SIDE_RATIO
        and min(angles) >= MIN_CORNER_ANGLE
        and max(angles) <= MAX_CORNER_ANGLE
        and (
            edge_support >= MIN_EDGE_SUPPORT
            or area_ratio >= 0.30
        )
    )
    quality = (
        0.45 * min(area_ratio / 0.55, 1.0)
        + 0.20 * aspect_score
        + 0.15 * opposite_ratio
        + 0.10 * center_score
        + 0.10 * edge_support
    )
    return {
        "area_ratio": float(area_ratio),
        "aspect": float(aspect),
        "aspect_score": float(aspect_score),
        "opposite_side_ratio": float(opposite_ratio),
        "min_angle": float(min(angles)),
        "max_angle": float(max(angles)),
        "edge_support": float(edge_support),
        "center_score": float(center_score),
        "quality": float(quality),
        "valid": bool(valid),
    }


def _find_card_quad(gray):
    import cv2
    import numpy as np

    candidates = []
    img_area = gray.shape[0] * gray.shape[1]
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
            points = approx.reshape(4, 2).astype(np.float32)
            metrics = _quad_metrics(gray, points)
            candidates.append((metrics["quality"], points, metrics))

    if not candidates:
        return None, {
            "status": "failed",
            "reason": "no quadrilateral candidates",
        }

    candidates.sort(key=lambda item: item[0], reverse=True)
    for _, points, metrics in candidates:
        if metrics["valid"]:
            return points, {
                "status": "detected",
                "reason": "validated card boundary",
                **metrics,
            }

    metrics = candidates[0][2]
    reason = "candidate failed validation"
    if metrics["area_ratio"] < MIN_CARD_AREA_RATIO:
        reason = "candidate too small"
    elif metrics["edge_support"] < MIN_EDGE_SUPPORT:
        reason = "card border edge support too weak"
    elif metrics["opposite_side_ratio"] < MIN_OPPOSITE_SIDE_RATIO:
        reason = "perspective distortion too strong"
    return None, {
        "status": "failed",
        "reason": reason,
        "candidate_points": [
            [float(point[0]), float(point[1])] for point in points
        ],
        **metrics,
    }


def _largest_quad_contour(gray):
    """Compatibility helper returning only a validated card boundary."""
    points, _ = _find_card_quad(gray)
    return points


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

def prepare_detailed(surface):
    global _LAST_DETECTION, _LAST_DETECTION_ERROR
    if surface is None or surface.get_width() < 2 or surface.get_height() < 2:
        details = {"status": "failed", "reason": "invalid input surface"}
        _LAST_DETECTION = details
        return None, details

    has_cv2, _ = _probe()
    if not has_cv2:
        details = {
            "status": "failed",
            "reason": "OpenCV and NumPy are required for card detection",
        }
        _LAST_DETECTION = details
        return None, details

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
    if arr is None:
        details = {"status": "failed", "reason": "image conversion failed"}
        _LAST_DETECTION = details
        return None, details
    try:
        gray = _array_to_gray(arr)
        pts, details = _find_card_quad(gray)
        if pts is None:
            candidate_points = details.get("candidate_points")
            if candidate_points is not None:
                details = dict(details)
                details["candidate_points"] = [
                    [
                        float(point[0]) / scale,
                        float(point[1]) / scale,
                    ]
                    for point in candidate_points
                ]
            _LAST_DETECTION = details
            return None, details
        pts /= scale
        details = dict(details)
        details["points"] = [
            [float(point[0]), float(point[1])] for point in pts
        ]
        canvas = _warp_to_card(surface, pts)
        if canvas is None:
            details = {
                "status": "failed",
                "reason": "perspective transform failed",
            }
            _LAST_DETECTION = details
            return None, details
        _LAST_DETECTION_ERROR = None
        _LAST_DETECTION = details
        return canvas, details
    except cv2.error as exc:
        message = str(exc)
        if message != _LAST_DETECTION_ERROR:
            print(f"[cardscan] card-boundary detection failed: {message}")
            _LAST_DETECTION_ERROR = message
        details = {"status": "failed", "reason": message}
        _LAST_DETECTION = details
        return None, details


def prepare(surface):
    """Return a normalized card only after boundary validation succeeds."""
    canvas, _ = prepare_detailed(surface)
    return canvas


def last_detection():
    """Return quality details for the most recent preprocessing attempt."""
    return dict(_LAST_DETECTION)


def load_image(path):
    try:
        return pygame.image.load(path)
    except (pygame.error, FileNotFoundError, OSError):
        return None
