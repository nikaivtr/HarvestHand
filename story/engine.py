# ============================================================
#  StoryEngine
#  Tracks which slide the student is on and what happens next.
#  You should NOT need to edit this file when adding chapters.
# ============================================================

import random


class StoryEngine:
    def __init__(self, chapter: dict, on_chapter_end=None):
        self.chapter = chapter
        self.slides = chapter["slides"]
        self.on_chapter_end = on_chapter_end  # called when the last slide is done

        self.slide_idx = 0   # which slide we're on
        self.line_idx = 0    # which line of dialogue we're on (for dialogue/end/feedback slides)
        self.answer_result = None  # None = not answered yet | True = correct | False = wrong
        self.popup_open = None     # None | "scan" | "image"
        self._last_answer = None   # persists through feedback slides so they can branch
        self._skip_slides: set = set()  # indices to skip (losing members of a random_pick group)
        self._retry_slide: int | None = None  # slide index to loop back to on wrong answer
        self.is_retry: bool = False  # True when re-showing a choice after a wrong attempt

    # ── Quick accessors ──────────────────────────────────────

    @property
    def slide(self) -> dict:
        return self.slides[self.slide_idx]

    @property
    def active_char(self) -> str | None:
        """Returns the name of the character who is currently speaking."""
        s = self.slide
        if s["type"] in ("dialogue", "end", "feedback"):
            lines = s.get("lines", [])
            if 0 <= self.line_idx < len(lines):
                return lines[self.line_idx][0]
        if s["type"] == "choice":
            chars = s.get("chars", {})
            if chars:
                return next(iter(chars))
        return s.get("active")

    @property
    def current_line(self) -> tuple | None:
        """Returns (character_name, text) for the current dialogue line."""
        s = self.slide
        if s["type"] in ("dialogue", "end", "feedback"):
            lines = s.get("lines", [])
            if 0 <= self.line_idx < len(lines):
                return lines[self.line_idx]
        return None

    # ── Student actions ──────────────────────────────────────

    def tap(self) -> bool:
        """
        Called when the student taps the screen (not a choice button).
        - On dialogue/end/feedback slides: advance to the next line, or next slide.
        - On scan slides: open the scan popup.
        Returns True if something changed.
        """
        s = self.slide

        if self.popup_open:
            return False  # let the popup handle taps itself

        if s["type"] in ("dialogue", "end", "feedback"):
            lines = s.get("lines", [])
            if self.line_idx < len(lines) - 1:
                self.line_idx += 1
                return True
            else:
                return self._advance()

        if s["type"] in ("title", "transition"):
            return self._advance()

        if s["type"] == "scan":
            self.popup_open = "scan"
            return True

        if s["type"] == "choice":
            # Tapping outside a button does nothing — player must pick a choice
            return False

        return False

    def choose(self, idx: int) -> bool:
        """
        Called when the student picks an answer on a choice slide.
        Records the answer and immediately advances to the matching feedback slide.
        On a wrong answer, remembers this slide index so wrong feedback can loop back.
        """
        s = self.slide
        if s["type"] != "choice":
            return False
        self._last_answer = (idx == s["correct"])
        self._skip_slides = set()
        if not self._last_answer:
            # Remember where to return after wrong feedback
            self._retry_slide = self.slide_idx
        else:
            # Correct answer: clear retry state
            self._retry_slide = None
            self.is_retry = False
        return self._advance()

    def dismiss_answer(self) -> bool:
        """Legacy method kept for compatibility. With feedback slides this is unused."""
        self.answer_result = None
        return self._advance()

    def on_scan_complete(self) -> bool:
        """Called by the scan popup when the card is scanned (or simulated)."""
        self.popup_open = None
        return self._advance()

    def close_popup(self):
        """Called when any popup is closed."""
        self.popup_open = None

    # ── Internal ─────────────────────────────────────────────

    def _advance(self) -> bool:
        """Move to the next slide, skipping non-matching and unchosen random feedback slides.
        If the current slide is a wrong-answer feedback marked retry_to_choice, loop back
        to the choice slide instead of moving forward."""

        # Wrong feedback that wants a retry: jump back to the choice slide
        current = self.slides[self.slide_idx]
        if current.get("retry_to_choice") and self._retry_slide is not None:
            self.slide_idx = self._retry_slide
            self.line_idx  = 0
            self.answer_result = None
            self.is_retry  = True
            self._skip_slides = set()
            return True

        if self.slide_idx < len(self.slides) - 1:
            self.slide_idx += 1
            self.line_idx = 0
            self.answer_result = None

            # Skip feedback slides that don't match last answer, or were not randomly chosen
            while self.slide_idx < len(self.slides):
                s = self.slides[self.slide_idx]
                if s["type"] == "feedback" and "if_correct" in s and s["if_correct"] != self._last_answer:
                    self.slide_idx += 1
                    continue
                if self.slide_idx in self._skip_slides:
                    self.slide_idx += 1
                    continue
                break

            # If we landed on the start of a random_pick group, choose one and skip the rest
            if self.slide_idx < len(self.slides):
                s = self.slides[self.slide_idx]
                if s.get("type") == "feedback" and s.get("random_pick"):
                    group = []
                    i = self.slide_idx
                    while i < len(self.slides):
                        si = self.slides[i]
                        if (si.get("type") == "feedback" and
                                si.get("random_pick") and
                                si.get("if_correct") == s.get("if_correct")):
                            group.append(i)
                            i += 1
                        else:
                            break
                    chosen = random.choice(group)
                    for idx in group:
                        if idx != chosen:
                            self._skip_slides.add(idx)
                    self.slide_idx = chosen

            if self.slide_idx < len(self.slides):
                return True

        if self.on_chapter_end:
            self.on_chapter_end()
        return False
