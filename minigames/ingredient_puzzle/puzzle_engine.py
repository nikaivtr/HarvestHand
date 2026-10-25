"""
PuzzleEngine — loads sprite-sheet ingredients and cuts them into jigsaw pieces.
"""

import math
import random
from itertools import product

import pygame

from . import assets_config as AC


_source_sheet = None


def _load_source_surface(ingredient_key):
    """Crop one ingredient from the sheet and remove its magenta backdrop."""
    global _source_sheet

    index = next(
        (i for i, (key, _, _) in enumerate(AC.INGREDIENT_GRID_ORDER)
         if key == ingredient_key),
        None,
    )
    if index is None:
        raise ValueError(f"Unknown puzzle ingredient: {ingredient_key}")

    if _source_sheet is None:
        _source_sheet = pygame.image.load(AC.SPRITE_SHEET).convert()

    crop_rect = pygame.Rect(
        *AC.crop_rect_for(index, _source_sheet.get_width(), _source_sheet.get_height())
    )
    source = _source_sheet.subsurface(crop_rect).copy()
    return _remove_magenta_matte(source)


def _remove_magenta_matte(source):
    """Turn the sprite sheet's magenta background transparent and defringe edges."""
    pixels = bytearray(pygame.image.tobytes(source, "RGBA"))
    background = (255, 18, 255)

    for i in range(0, len(pixels), 4):
        red, green, blue = pixels[i], pixels[i + 1], pixels[i + 2]
        coverage = max(255 - red, green, 255 - blue)
        alpha = max(0, min(255, round((coverage - 28) * 255 / 227)))

        if alpha < 12:
            pixels[i:i + 4] = b"\x00\x00\x00\x00"
            continue

        if alpha < 255:
            inverse_alpha = 255 / alpha
            pixels[i] = max(
                0, min(255, round((red - background[0] * (1 - alpha / 255))
                                  * inverse_alpha))
            )
            pixels[i + 1] = max(
                0, min(255, round((green - background[1] * (1 - alpha / 255))
                                  * inverse_alpha))
            )
            pixels[i + 2] = max(
                0, min(255, round((blue - background[2] * (1 - alpha / 255))
                                  * inverse_alpha))
            )
        pixels[i + 3] = alpha

    return pygame.image.frombytes(bytes(pixels), source.get_size(), "RGBA")


def _grid_shape(piece_count):
    if piece_count == 4:
        return 2, 2
    if piece_count == 6:
        return 3, 2
    if piece_count == 8:
        return 4, 2
    raise ValueError(f"Unsupported puzzle piece count: {piece_count}")


def _grid_edges(source, cols, rows):
    """Shift grid seams slightly when needed to keep artwork in every cell."""
    width, height = source.get_size()
    mask = pygame.mask.from_surface(source, threshold=10)
    integral = [[0] * (width + 1) for _ in range(height + 1)]
    for y in range(height):
        row_count = 0
        for x in range(width):
            row_count += mask.get_at((x, y))
            integral[y + 1][x + 1] = integral[y][x + 1] + row_count

    def candidates(count, extent):
        edges = []
        for index in range(count + 1):
            base = index * extent // count
            if index in (0, count):
                edges.append([base])
                continue
            reach = max(1, round(extent / count * 0.2))
            edges.append(sorted({
                max(1, min(extent - 1, base + round(reach * offset)))
                for offset in (-1, -0.5, 0, 0.5, 1)
            }))
        return edges

    x_options = candidates(cols, width)
    y_options = candidates(rows, height)
    best_edges = None
    best_score = (-1, float("-inf"))

    for inner_x in product(*x_options[1:-1]):
        x_edges = (0, *inner_x, width)
        if any(right <= left for left, right in zip(x_edges, x_edges[1:])):
            continue
        for inner_y in product(*y_options[1:-1]):
            y_edges = (0, *inner_y, height)
            if any(bottom <= top for top, bottom in zip(y_edges, y_edges[1:])):
                continue

            cell_counts = []
            for row in range(rows):
                for col in range(cols):
                    left, right = x_edges[col], x_edges[col + 1]
                    top, bottom = y_edges[row], y_edges[row + 1]
                    cell_counts.append(
                        integral[bottom][right] - integral[top][right]
                        - integral[bottom][left] + integral[top][left]
                    )

            minimum = min(cell_counts)
            deviation = sum(
                abs(edge - index * extent // count)
                for edges, count, extent in (
                    (x_edges, cols, width), (y_edges, rows, height)
                )
                for index, edge in enumerate(edges[1:-1], start=1)
            )
            score = (minimum, -deviation)
            if score > best_score:
                best_edges = (x_edges, y_edges)
                best_score = score

    return best_edges


def _seam_points(start, end, horizontal, sign, depth):
    """Create a repeatable tabbed edge shared by both neighboring pieces."""
    points = []
    tab_profile = (
        (0.00, 0.00), (0.28, 0.00), (0.35, 0.25),
        (0.41, 0.82), (0.47, 1.00), (0.53, 1.00),
        (0.59, 0.82), (0.65, 0.25), (0.72, 0.00), (1.00, 0.00),
    )
    for t, amount in tab_profile:
        along = round(start + (end - start) * t)
        offset = round(sign * depth * amount)
        point = (along, offset) if horizontal else (offset, along)
        points.append(point)
    return points


def _piece_polygon(row, col, rows, cols, x_edges, y_edges):
    x0, x1 = x_edges[col], x_edges[col + 1]
    y0, y1 = y_edges[row], y_edges[row + 1]
    horizontal_depth = max(5, (x1 - x0) * 0.15)
    vertical_depth = max(5, (y1 - y0) * 0.15)
    points = [(x0, y0)]

    if row == 0:
        points.append((x1, y0))
    else:
        sign = 1 if (row + col - 1) % 2 == 0 else -1
        points.extend(
            (x, y0 + offset)
            for x, offset in _seam_points(
                x0, x1, True, sign, horizontal_depth
            )
        )

    if col == cols - 1:
        points.append((x1, y1))
    else:
        sign = 1 if (row + col) % 2 == 0 else -1
        points.extend(
            (x1 + offset, y)
            for offset, y in _seam_points(y0, y1, False, sign, vertical_depth)
        )

    if row == rows - 1:
        points.append((x0, y1))
    else:
        sign = 1 if (row + col) % 2 == 0 else -1
        points.extend(
            (x, y1 + offset)
            for x, offset in reversed(
                _seam_points(x0, x1, True, sign, horizontal_depth)
            )
        )

    if col == 0:
        points.append((x0, y0))
    else:
        sign = 1 if (row + col - 1) % 2 == 0 else -1
        points.extend(
            (x0 + offset, y)
            for offset, y in reversed(
                _seam_points(y0, y1, False, sign, vertical_depth)
            )
        )

    return points


def _clip_surface_to_mask(surface, mask, bounds):
    mask_surface = mask.to_surface(
        setcolor=(255, 255, 255, 255),
        unsetcolor=(0, 0, 0, 0),
    )
    mask_surface = mask_surface.subsurface(bounds).copy()
    result = surface.copy()
    result.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return result


def _make_guide_surface(size, polygon, bounds):
    local_polygon = [(x - bounds.x, y - bounds.y) for x, y in polygon]
    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.polygon(surface, (255, 255, 255, 255), local_polygon)
    return surface


def generate_puzzle(ingredient_key, piece_count, target_rect):
    """Cut a complete ingredient image into complementary jigsaw fragments."""
    artwork = _load_source_surface(ingredient_key)
    artwork_bounds = artwork.get_bounding_rect(min_alpha=12)
    artwork = artwork.subsurface(artwork_bounds).copy()

    fit_scale = min(
        target_rect.w * 0.9 / artwork.get_width(),
        target_rect.h * 0.9 / artwork.get_height(),
    )
    artwork_size = (
        max(1, round(artwork.get_width() * fit_scale)),
        max(1, round(artwork.get_height() * fit_scale)),
    )
    artwork = pygame.transform.smoothscale(artwork, artwork_size)
    source = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    source.blit(artwork, artwork.get_rect(center=source.get_rect().center))
    silhouette_mask = pygame.mask.from_surface(source, threshold=10)
    silhouette_surface = silhouette_mask.to_surface(
        setcolor=AC.PALETTE["silhouette_fill"],
        unsetcolor=(0, 0, 0, 0),
    )
    silhouette_outline = silhouette_mask.outline()
    if len(silhouette_outline) > 2:
        pygame.draw.lines(
            silhouette_surface,
            AC.PALETTE["silhouette_border"],
            True,
            silhouette_outline,
            3,
        )
    cols, rows = _grid_shape(piece_count)
    x_edges, y_edges = _grid_edges(source, cols, rows)

    pieces = []
    claimed_pixels = pygame.Mask(target_rect.size)
    for row in range(rows):
        for col in range(cols):
            polygon = _piece_polygon(row, col, rows, cols, x_edges, y_edges)
            min_x = max(0, min(x for x, _ in polygon))
            max_x = min(target_rect.w - 1, max(x for x, _ in polygon))
            min_y = max(0, min(y for _, y in polygon))
            max_y = min(target_rect.h - 1, max(y for _, y in polygon))
            bounds = pygame.Rect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
            fragment = source.subsurface(bounds).copy()
            polygon_surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)
            pygame.draw.polygon(polygon_surface, (255, 255, 255, 255), polygon)
            piece_mask = pygame.mask.from_surface(polygon_surface)
            piece_mask.erase(claimed_pixels, (0, 0))
            claimed_pixels.draw(piece_mask, (0, 0))
            clipped = _clip_surface_to_mask(fragment, piece_mask, bounds)
            guide_surface = _make_guide_surface(bounds.size, polygon, bounds)

            pieces.append({
                "surface": clipped,
                "guide_surface": guide_surface,
                "silhouette_surface": silhouette_surface,
                "mask": pygame.mask.from_surface(clipped, threshold=10),
                "correct_pos": (
                    bounds.x + bounds.w / 2,
                    bounds.y + bounds.h / 2,
                ),
                "correct_angle": 0.0,
                "index": row * cols + col,
                "total": piece_count,
                "cell_rect": bounds,
            })

    return pieces


def scramble_pieces(pieces, workspace_rect, rotation=False):
    """Scatter pieces in bounded workspace slots and optionally rotate them."""
    piece_count = len(pieces)
    cols = math.ceil(math.sqrt(piece_count))
    rows = math.ceil(piece_count / cols)
    slot_w = workspace_rect.w / cols
    slot_h = workspace_rect.h / rows

    for index, piece in enumerate(pieces):
        row, col = divmod(index, cols)
        width = piece["width"]
        height = piece["height"]
        angle = random.choice((0, 90, 180, 270)) if rotation else 0
        if angle in (90, 270):
            width, height = height, width

        slot_left = workspace_rect.left + col * slot_w
        slot_top = workspace_rect.top + row * slot_h
        x_margin = max(0, (slot_w - width) / 2)
        y_margin = max(0, (slot_h - height) / 2)
        x = random.uniform(slot_left + x_margin, slot_left + slot_w - x_margin)
        y = random.uniform(slot_top + y_margin, slot_top + slot_h - y_margin)

        piece["current_pos"] = [x, y]
        piece["current_angle"] = angle
        piece["placed"] = False


def validate_placement(piece, pos_tolerance_px, angle_tolerance_deg):
    """Return whether a piece is close enough to its own target and orientation."""
    dx = piece["current_pos"][0] - piece["correct_pos"][0]
    dy = piece["current_pos"][1] - piece["correct_pos"][1]
    distance = math.hypot(dx, dy)
    angle_diff = abs(
        (piece["current_angle"] - piece["correct_angle"] + 180) % 360 - 180
    )
    return distance <= pos_tolerance_px and angle_diff <= angle_tolerance_deg
