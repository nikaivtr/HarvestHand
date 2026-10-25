"""
Timer — countdown clock for the ingredient puzzle levels.

Uses a monotonic time source so the countdown is frame-rate independent.
Supports pause / resume.
"""

import time


class Timer:
    def __init__(self, total_seconds):
        self.total_seconds = total_seconds
        self._start_time = None
        self._paused_time = 0.0
        self._is_paused = False
        self._is_running = False
        self._pause_start = None

    def start(self):
        self._start_time = time.monotonic()
        self._paused_time = 0.0
        self._is_paused = False
        self._is_running = True

    def pause(self):
        if self._is_running and not self._is_paused:
            self._is_paused = True
            self._pause_start = time.monotonic()

    def resume(self):
        if self._is_paused:
            self._paused_time += time.monotonic() - self._pause_start
            self._is_paused = False
            self._pause_start = None

    def stop(self):
        self._is_running = False
        self._is_paused = False

    def remaining(self):
        if not self._is_running:
            return self.total_seconds
        now = time.monotonic()
        elapsed = now - self._start_time - self._paused_time
        if self._is_paused:
            elapsed = self._pause_start - self._start_time - self._paused_time
        left = self.total_seconds - elapsed
        return max(0.0, left)

    def is_expired(self):
        return self.remaining() <= 0.0

    def formatted(self):
        total = int(self.remaining())
        minutes = total // 60
        seconds = total % 60
        return f"{minutes:02d}:{seconds:02d}"
