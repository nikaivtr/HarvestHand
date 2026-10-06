# ============================================================
#  Camera Sources
#
#  Everything the scanner needs from a lens, behind one tiny
#  interface, so the recognition code never knows or cares what
#  it is looking at:
#
#      src = open_camera()
#      frame = src.read()        # -> pygame.Surface, or None
#      src.release()
#
#  Three sources are provided:
#
#    OpenCVCamera   a real USB/CSI camera via OpenCV (Raspberry Pi)
#    FolderCamera   replays a folder of JPEGs, so the whole
#                   pipeline can be developed and tested on a
#                   laptop with no camera attached
#    NullCamera     always returns None (headless CI, tests)
#
#  OpenCV is imported lazily and only inside open(). A machine
#  without cv2 installed still runs the game and still trains a
#  model - it simply cannot read a live camera.
# ============================================================

import os

import pygame


class CameraError(Exception):
    """Raised when a camera source cannot be opened."""


class _Base:
    """Common surface, so all sources are interchangeable."""

    def read(self):
        raise NotImplementedError

    def release(self):
        pass

    @property
    def is_open(self):
        return False

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.release()
        return False


# ── OpenCV ──────────────────────────────────────────────────

class OpenCVCamera(_Base):
    """A live camera through OpenCV.

    The frame is handed to pygame without any numpy work on our
    side: cv2 gives a BGR buffer, we ask cv2 to convert it to RGB
    and hand over the raw bytes, and pygame wraps them in a
    Surface.
    """

    backend = "opencv"

    def __init__(self, device=0, width=640, height=480):
        self.device = device
        self.width  = width
        self.height = height
        self._cv2   = None
        self._cap   = None

    def open(self):
        try:
            import cv2
        except ImportError as exc:
            raise CameraError(
                "OpenCV is not installed. On the Raspberry Pi run:\n"
                "    pip install opencv-python-headless"
            ) from exc

        cap = cv2.VideoCapture(self.device)
        if not cap.isOpened():
            raise CameraError(
                f"could not open camera {self.device} - check the ribbon "
                "seating and that the camera is enabled (sudo raspi-config)"
            )
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self._cv2 = cv2
        self._cap = cap
        return self

    def read(self):
        """Grab one frame as a pygame.Surface, or None."""
        if self._cap is None:
            return None
        ok, frame = self._cap.read()
        if not ok or frame is None:
            return None

        rgb = self._cv2.cvtColor(frame, self._cv2.COLOR_BGR2RGB)
        h, w = rgb.shape[:2]
        return pygame.image.frombuffer(rgb.tobytes(), (w, h), "RGB")

    def release(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    @property
    def is_open(self):
        return self._cap is not None



# ── Folder replay ───────────────────────────────────────────

class FolderCamera(_Base):
    """Cycles through images in a folder, then holds on the last.

    This is the development path: record a few dozen photos of each
    card with the actual Pi camera, drop them in a folder, and the
    whole recognition pipeline can then be developed and tested on
    a laptop with no camera and no OpenCV at all.
    """

    backend = "folder"
    EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

    def __init__(self, path, loop=True):
        self.path = path
        self.loop = loop
        self._files = []
        self._i = 0
        self._last = None

    def open(self):
        if not os.path.isdir(self.path):
            raise CameraError(f"no such folder: {self.path}")
        self._files = [
            os.path.join(self.path, n)
            for n in sorted(os.listdir(self.path))
            if n.lower().endswith(self.EXTS)
        ]
        if not self._files:
            raise CameraError(f"no images in {self.path}")
        self._i = 0
        return self

    def read(self):
        if not self._files:
            return None
        if self._i >= len(self._files):
            if not self.loop:
                return self._last          # hold the final frame
            self._i = 0
        try:
            img = pygame.image.load(self._files[self._i])
        except (pygame.error, OSError):
            self._i += 1
            return self.read()
        self._last = img
        self._i += 1
        return img

    def release(self):
        self._files = []
        self._last = None

    @property
    def is_open(self):
        return bool(self._files)

    def __len__(self):
        return len(self._files)


# ── Null ────────────────────────────────────────────────────

class NullCamera(_Base):
    """A camera that is not there. Used by tests and on dev PCs."""

    backend = "null"

    def open(self):
        return self

    def read(self):
        return None

    @property
    def is_open(self):
        return True


# ── Factory ─────────────────────────────────────────────────

def open_camera(kind="auto", device=0, path=None, loop=True):
    """Build and open a camera source.

    kind: "opencv" | "folder" | "null" | "auto"

    Auto prefers a real OpenCV camera and falls back to a null
    source, so a missing camera never crashes the game.
    """
    if kind == "null":
        return NullCamera().open()
    if kind == "folder":
        if not path:
            raise CameraError("folder source needs a path")
        return FolderCamera(path, loop).open()
    if kind == "opencv":
        return OpenCVCamera(device).open()
    if kind != "auto":
        raise CameraError(f"unknown camera kind: {kind}")

    try:
        return OpenCVCamera(device).open()
    except CameraError as exc:
        print(f"[cardscan] no live camera "
              f"({str(exc.args[0]).splitlines()[0]}); continuing without one")
        return NullCamera().open()
