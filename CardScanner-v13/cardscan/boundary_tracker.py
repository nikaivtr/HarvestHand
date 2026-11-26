"""Live card-boundary acquisition and tracking for camera diagnostics."""

import pygame


class BoundaryTracker:
    """Acquire a card boundary, then follow it between detector updates."""

    ACQUIRE_SECONDS = 0.08
    MAX_INITIAL_JUMP = 0.25
    MIN_OPPOSITE_SIDE_RATIO = 0.55
    MIN_CORNER_ANGLE = 35.0
    MAX_CORNER_ANGLE = 145.0
    MIN_AREA_RATIO = 0.03
    MIN_EDGE_SUPPORT = 0.05

    def __init__(self):
        self.reset()

    def reset(self):
        self.points = None
        self.pending = None
        self.acquire_time = 0.0
        self.lost_time = 0.0
        self.locked = False
        self._previous_gray = None

    def update(self, surface, dt):
        """Return live boundary details for the current camera frame."""
        if surface is None:
            self.reset()
            return {"status": "lost", "reason": "no camera frame"}

        gray = self._gray(surface)
        dt = max(0.0, min(float(dt), 0.25))
        import cardscan.preprocess as preprocess
        candidate = self._find_candidate(
            preprocess._surface_to_array(surface), self.points)

        if self.points is None:
            self._acquire(candidate, dt)
        else:
            if candidate is not None and self._compatible(self.points, candidate):
                self.points = self._blend(self.points, candidate, 0.55)
                self.lost_time = 0.0
            elif candidate is not None:
                self.points = None
                self.locked = False
                self.pending = None
                self.acquire_time = 0.0
                self._acquire(candidate, dt)
            else:
                self.points = None
                self.locked = False
                self.pending = None
                self.acquire_time = 0.0

        self._previous_gray = gray
        if self.points is None:
            return {
                "status": "acquiring" if self.pending is not None else "lost",
                "reason": "calibrating initial boundary"
                if self.pending is not None
                else "awaiting a trackable card boundary",
                "points": self._as_lists(self.pending)
                if self.pending is not None
                else None,
            }

        status = "tracking" if self.locked else "acquiring"
        return {
            "status": status,
            "points": self._as_lists(self.points),
            "acquire_time": round(self.acquire_time, 3),
            "lost_time": round(self.lost_time, 3),
        }

    @classmethod
    def _find_candidate(cls, rgb, previous):
        """Best card quad in an RGB array, via the shared detector.

        Uses the same detection as recognition (cardscan.detect), so the
        diagnostic overlay shows exactly what the scanner sees. Last
        frame's quad is passed along to favour a stable choice.
        """
        import cardscan.preprocess as preprocess

        points, _ = preprocess.detect_quad(rgb, previous=previous)
        return points

    @staticmethod
    def _edge_support(edges, points):
        import cv2
        import numpy as np

        support = []
        for start, end in zip(points, np.roll(points, -1, axis=0)):
            count = 0
            length = max(int(np.linalg.norm(end - start)), 2)
            for point in np.linspace(start, end, min(length, 160)):
                x, y = np.rint(point).astype(int)
                x0, x1 = max(0, x - 2), min(edges.shape[1], x + 3)
                y0, y1 = max(0, y - 2), min(edges.shape[0], y + 3)
                count += int(edges[y0:y1, x0:x1].any())
            support.append(count / min(length, 160))
        return min(support)

    def _acquire(self, candidate, dt):
        if candidate is None:
            self.pending = None
            self.acquire_time = 0.0
            return
        candidate = self._order(self._as_array(candidate))
        if self.pending is None or not self._compatible(self.pending, candidate):
            self.pending = candidate
            self.acquire_time = 0.0
        else:
            self.pending = self._blend(self.pending, candidate, 0.35)
            self.acquire_time += dt
        if self.acquire_time >= self.ACQUIRE_SECONDS:
            self.points = self.pending.copy()
            self.locked = True
            self.lost_time = 0.0

    def _track(self, gray):
        if self._previous_gray is None or self.points is None:
            return None
        try:
            import cv2
            import numpy as np

            old = self._as_array(self.points).reshape(-1, 1, 2)
            new, status, error = cv2.calcOpticalFlowPyrLK(
                self._previous_gray,
                gray,
                old,
                None,
                winSize=(21, 21),
                maxLevel=3,
                criteria=(
                    cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                    20,
                    0.03,
                ),
            )
            if new is None or status is None or error is None:
                return None
            if int(status.sum()) != 4 or float(error.max()) > 40.0:
                return None
            points = new.reshape(4, 2).astype(np.float32)
            if not self._valid_quad(points, gray.shape[1], gray.shape[0]):
                return None
            return points
        except (ImportError, ValueError, TypeError):
            return None

    @staticmethod
    def _gray(surface):
        import cv2
        import numpy as np

        raw = pygame.image.tobytes(surface, "RGB")
        width, height = surface.get_size()
        array = np.frombuffer(raw, dtype=np.uint8).reshape(height, width, 3)
        return cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)

    @staticmethod
    def _as_array(points):
        import numpy as np
        return np.asarray(points, dtype=np.float32).reshape(4, 2)

    @classmethod
    def _as_lists(cls, points):
        return [
            [float(point[0]), float(point[1])]
            for point in cls._as_array(points)
        ]

    @classmethod
    def _blend(cls, first, second, amount):
        return cls._as_array(first) * (1.0 - amount) + cls._as_array(second) * amount

    @classmethod
    def _compatible(cls, first, second):
        import numpy as np
        first = cls._as_array(first)
        second = cls._as_array(second)
        diagonal = max(
            float(np.linalg.norm(first.max(axis=0) - first.min(axis=0))),
            1.0,
        )
        return float(np.mean(np.linalg.norm(first - second, axis=1))) / diagonal <= cls.MAX_INITIAL_JUMP

    @classmethod
    def _valid_quad(cls, points, width, height):
        import cv2
        import numpy as np

        ordered = cls._order(points)
        if not cv2.isContourConvex(ordered):
            return False
        area = abs(cv2.contourArea(ordered))
        if area < 0.02 * width * height or area > 0.95 * width * height:
            return False
        if np.any(ordered[:, 0] < -width * 0.05) or np.any(ordered[:, 0] > width * 1.05):
            return False
        if np.any(ordered[:, 1] < -height * 0.05) or np.any(ordered[:, 1] > height * 1.05):
            return False
        return cls._rectangle_like(ordered)

    @classmethod
    def _candidate_is_trackable(cls, points, details, surface):
        width, height = surface.get_size()
        if details.get("area_ratio", 0.0) < cls.MIN_AREA_RATIO:
            return False
        if details.get("edge_support", 0.0) < cls.MIN_EDGE_SUPPORT:
            return False
        return cls._valid_quad(points, width, height)

    @classmethod
    def _rectangle_like(cls, points):
        import numpy as np

        ordered = cls._order(points)
        sides = [
            float(np.linalg.norm(ordered[(i + 1) % 4] - ordered[i]))
            for i in range(4)
        ]
        opposite_ratio = min(
            sides[0] / max(sides[2], 1.0),
            sides[2] / max(sides[0], 1.0),
            sides[1] / max(sides[3], 1.0),
            sides[3] / max(sides[1], 1.0),
        )
        angles = []
        for i in range(4):
            before = ordered[(i - 1) % 4] - ordered[i]
            after = ordered[(i + 1) % 4] - ordered[i]
            denominator = max(
                float(np.linalg.norm(before) * np.linalg.norm(after)),
                1.0,
            )
            cosine = float(np.dot(before, after)) / denominator
            angles.append(float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))))
        return (
            opposite_ratio >= cls.MIN_OPPOSITE_SIDE_RATIO
            and min(angles) >= cls.MIN_CORNER_ANGLE
            and max(angles) <= cls.MAX_CORNER_ANGLE
        )

    @staticmethod
    def _order(points):
        import numpy as np
        import cv2

        points = np.asarray(points, dtype=np.float32)
        center = points.mean(axis=0)
        angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])
        ordered = points[np.argsort(angles)]
        if cv2.contourArea(ordered, oriented=True) < 0:
            ordered = ordered[::-1]
        return ordered
