"""
PuzzlePiece — a single fragment of an ingredient illustration.

Handles source artwork + polygon mask clipping, current/target position,
current/target orientation, drag state, placement state, and rendering.
"""

import math

import pygame

from . import assets_config as AC


def _make_font(size_fraction, height):
    size = max(14, int(height * size_fraction))
    try:
        return pygame.font.Font(AC.FONT_PATH, size)
    except pygame.error:
        return pygame.font.SysFont(AC.FONT_FALLBACK, size, bold=True)


class PuzzlePiece:
    """One puzzle piece with drag, rotate, snap, and placement logic."""

    def __init__(self, piece_id, surface, mask, guide_surface, correct_pos, correct_angle,
                 index_in_ingredient, total_pieces):
        self.piece_id = piece_id
        self.image = surface                      # clipped piece surface (alpha)
        self.mask = mask                          # pygame.Mask for collision
        self.guide_surface = guide_surface
        self._guide_fill = pygame.mask.from_surface(guide_surface).to_surface(
            setcolor=AC.PALETTE["guide_fill"],
            unsetcolor=(0, 0, 0, 0),
        )
        self._guide_outline = pygame.mask.from_surface(guide_surface).outline()
        self.correct_pos = correct_pos            # (x, y) where it belongs
        self.correct_angle = correct_angle        # degrees, target rotation
        self.index_in_ingredient = index_in_ingredient
        self.total_pieces = total_pieces

        self.pos = list(correct_pos)              # [x, y] current centre
        self.angle = 0.0                          # degrees current rotation
        self.placed = False                       # snapped into correct spot
        self.dragging = False                     # being dragged
        self.hovered = False                      # mouse over

        self._rotated_image = surface
        self._rotated_mask = mask
        self._shadow = mask.to_surface(
            setcolor=AC.PALETTE["piece_shadow"],
            unsetcolor=(0, 0, 0, 0),
        )
        self._outline = mask.outline(4)
        self._rotated_rect = surface.get_rect(center=correct_pos)
        self._cached_angle = None

    def rect(self):
        return self._rotated_rect

    def centre(self):
        return self.pos[0], self.pos[1]

    def distance_to_target(self):
        dx = self.pos[0] - self.correct_pos[0]
        dy = self.pos[1] - self.correct_pos[1]
        return math.hypot(dx, dy)

    def rotate(self, degrees):
        self.angle = (self.angle + degrees) % 360
        self._rebuild_rotation()


    def set_angle(self, degrees):
        self.angle = degrees % 360
        self._rebuild_rotation()

    def _rebuild_rotation(self):
        if self._cached_angle == self.angle:
            return
        self._cached_angle = self.angle
        if self.angle == 0:
            self._rotated_image = self.image
        else:
            self._rotated_image = pygame.transform.rotate(self.image, self.angle)
        self._rotated_mask = pygame.mask.from_surface(
            self._rotated_image, threshold=10
        )
        self._shadow = self._rotated_mask.to_surface(
            setcolor=AC.PALETTE["piece_shadow"],
            unsetcolor=(0, 0, 0, 0),
        )
        self._outline = self._rotated_mask.outline(4)
        self._rotated_rect = self._rotated_image.get_rect(center=self.pos)

    def start_drag(self, mouse_pos):
        self.dragging = True
        self.offset_x = self.pos[0] - mouse_pos[0]
        self.offset_y = self.pos[1] - mouse_pos[1]
        self._rebuild_rotation()

    def update_drag(self, mouse_pos):
        if not self.dragging:
            return
        self.pos[0] = mouse_pos[0] + self.offset_x
        self.pos[1] = mouse_pos[1] + self.offset_y
        self._rotated_rect.center = self.pos

    def end_drag(self):
        self.dragging = False

    def contains_point(self, point):
        if not self._rotated_rect.collidepoint(point):
            return False
        rx, ry = point
        lx = int(rx - self._rotated_rect.left)
        ly = int(ry - self._rotated_rect.top)
        if 0 <= lx < self._rotated_mask.get_size()[0] and 0 <= ly < self._rotated_mask.get_size()[1]:
            return self._rotated_mask.get_at((lx, ly))
        return False

    def snap_to_correct(self):
        self.pos = [float(self.correct_pos[0]), float(self.correct_pos[1])]
        self.angle = self.correct_angle
        self.placed = True
        self.dragging = False
        self._rebuild_rotation()

    def nudge_away(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy
        self._rotated_rect.center = self.pos

    def draw(self, surf):
        if not self.placed:
            surf.blit(self._shadow, self._rotated_rect.move(3, 4))

        surf.blit(self._rotated_image, self._rotated_rect)

        border_col = AC.PALETTE["green"] if self.placed else AC.PALETTE["piece_border"]
        if len(self._outline) > 2:
            points = [
                (self._rotated_rect.left + x, self._rotated_rect.top + y)
                for x, y in self._outline
            ]
            pygame.draw.lines(surf, border_col, True, points, 2)

        if self.hovered and not self.placed:
            glow = pygame.Surface(self._rotated_rect.size, pygame.SRCALPHA)
            glow.blit(self._rotated_image, (0, 0))
            glow.fill((255, 255, 255, 60), special_flags=pygame.BLEND_RGBA_ADD)
            surf.blit(glow, self._rotated_rect)

    def draw_target_guide(self, surf):
        guide_rect = self.guide_surface.get_rect(center=self.correct_pos)
        surf.blit(self._guide_fill, guide_rect)
        if len(self._guide_outline) > 2:
            pygame.draw.lines(
                surf,
                AC.PALETTE["guide_border"],
                True,
                [
                    (guide_rect.left + x, guide_rect.top + y)
                    for x, y in self._guide_outline
                ],
                2,
            )


    def angle_diff(self):
        diff = (self.angle - self.correct_angle + 180) % 360 - 180
        return abs(diff)

    def is_correctly_placed(self, pos_tolerance_px, angle_tolerance_deg):
        if self.placed:
            return True
        return (self.distance_to_target() <= pos_tolerance_px
                and self.angle_diff() <= angle_tolerance_deg)
