"""Low-latency, measurable webcam capture for the Recognition Lab."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any

import cv2
import numpy as np


BACKENDS = {
    "auto": (("Media Foundation", cv2.CAP_MSMF), ("DirectShow", cv2.CAP_DSHOW)),
    "msmf": (("Media Foundation", cv2.CAP_MSMF),),
    "dshow": (("DirectShow", cv2.CAP_DSHOW),),
}
RESOLUTIONS = ((1920, 1080), (1280, 720), (640, 480))


@dataclass
class CameraConfig:
    device: int = 0
    backend: str = "auto"
    width: int = 1920
    height: int = 1080
    target_fps: int = 30
    fourcc: str = "MJPG"


@dataclass
class CameraStatus:
    running: bool = False
    selected_backend: str = "unopened"
    requested_backend: str = "auto"
    requested_resolution: tuple[int, int] = (1920, 1080)
    actual_resolution: tuple[int, int] | None = None
    requested_fps: int = 30
    reported_fps: float | None = None
    measured_fps: float = 0.0
    fourcc: str = ""
    requested_fourcc: str = "MJPG"
    failed_frames: int = 0
    frames_captured: int = 0
    average_read_ms: float = 0.0
    brightness: float = 0.0
    contrast: float = 0.0
    sharpness: float = 0.0
    started_at: float | None = None
    initialization_errors: list[str] = field(default_factory=list)
    last_error: str = ""
    device_name: str = "USB 2.0 HD1080P PC Camera (configured)"


class CameraCapture:
    """Own exactly one VideoCapture and publish only its newest successful frame."""

    def __init__(self, config: CameraConfig | None = None) -> None:
        self.config = config or CameraConfig()
        self.status = CameraStatus(
            requested_backend=self.config.backend,
            requested_resolution=(self.config.width, self.config.height),
            requested_fps=self.config.target_fps,
            requested_fourcc=self.config.fourcc,
        )
        self._capture: cv2.VideoCapture | None = None
        self._latest_frame: np.ndarray | None = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._read_times: list[float] = []
        self._measure_started: float | None = None
        self._consecutive_failures = 0

    def start(self) -> bool:
        self.stop()
        self.status = CameraStatus(
            requested_backend=self.config.backend,
            requested_resolution=(self.config.width, self.config.height),
            requested_fps=self.config.target_fps,
            requested_fourcc=self.config.fourcc,
        )
        self._latest_frame = None
        self._read_times = []
        self._measure_started = None
        self._consecutive_failures = 0
        for backend_name, backend in BACKENDS.get(self.config.backend, BACKENDS["auto"]):
            capture = cv2.VideoCapture(self.config.device, backend)
            if not capture.isOpened():
                self.status.initialization_errors.append(
                    f"{backend_name}: could not open device {self.config.device}"
                )
                capture.release()
                continue
            capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.config.fourcc))
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
            capture.set(cv2.CAP_PROP_FPS, self.config.target_fps)
            warm_frame = None
            warm_error = None
            for _ in range(8):
                ok, frame = capture.read()
                if ok and frame is not None and frame.size:
                    warm_frame = frame
                    break
                warm_error = "could not deliver a readable frame"
            if warm_frame is None:
                self.status.initialization_errors.append(
                    f"{backend_name}: {warm_error or 'warm-up frame failed'}"
                )
                capture.release()
                continue
            self._capture = capture
            self.status.selected_backend = backend_name
            self.status.reported_fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
            self.status.actual_resolution = (
                int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0),
                int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0),
            )
            self.status.fourcc = self._decode_fourcc(capture.get(cv2.CAP_PROP_FOURCC))
            self._stop_event.clear()
            self.status.running = True
            self.status.started_at = time.perf_counter()
            self._thread = threading.Thread(
                target=self._capture_loop,
                name="recognition-lab-camera",
                daemon=True,
            )
            self._thread.start()
            return True
        self.status.selected_backend = "unavailable"
        self.status.last_error = "; ".join(self.status.initialization_errors)
        return False

    def stop(self) -> None:
        self._stop_event.set()
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=2.0)
        self._thread = None
        if self._capture is not None:
            self._capture.release()
            self._capture = None
        self.status.running = False

    def latest_frame(self) -> np.ndarray | None:
        with self._lock:
            return self._latest_frame

    def snapshot(self) -> CameraStatus:
        with self._lock:
            return CameraStatus(
                **{
                    key: (value.copy() if isinstance(value, list) else value)
                    for key, value in self.status.__dict__.items()
                }
            )

    def _capture_loop(self) -> None:
        while not self._stop_event.is_set() and self._capture is not None:
            started = time.perf_counter()
            ok, frame = self._capture.read()
            elapsed = time.perf_counter() - started
            self._read_times.append(elapsed)
            if len(self._read_times) > 120:
                self._read_times.pop(0)
            self.status.average_read_ms = (
                sum(self._read_times) / len(self._read_times) * 1000.0
                if self._read_times else 0.0
            )
            if not ok or frame is None or frame.size == 0:
                self.status.failed_frames += 1
                self._consecutive_failures += 1
                if self._consecutive_failures >= 5:
                    self.status.last_error = "Five consecutive frame reads failed."
                    break
                continue
            self._consecutive_failures = 0
            with self._lock:
                self._latest_frame = frame
                self.status.frames_captured += 1
                if self.status.frames_captured % 10 == 0:
                    sample = cv2.resize(frame, (320, 180), interpolation=cv2.INTER_AREA)
                    gray = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
                    self.status.brightness = float(gray.mean())
                    self.status.contrast = float(gray.std())
                    self.status.sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
                if self._measure_started is None:
                    self._measure_started = time.perf_counter()
                duration = time.perf_counter() - self._measure_started
                if duration > 0:
                    self.status.measured_fps = self.status.frames_captured / duration
                self.status.actual_resolution = (int(frame.shape[1]), int(frame.shape[0]))
        self.status.running = False
        if self._capture is not None:
            self._capture.release()

    @staticmethod
    def _decode_fourcc(value: float) -> str:
        raw = int(value)
        if raw <= 0:
            return ""
        decoded = "".join(chr((raw >> (8 * index)) & 0xFF) for index in range(4))
        return decoded if decoded.isprintable() else "unknown"

