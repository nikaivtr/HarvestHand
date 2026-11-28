# ============================================================
#  Card Scanner
#
#  The game-facing half of card recognition. It owns the rule the
#  classroom mechanic needs:
#
#      the game asks for a card  ->  the player holds up a card
#      ->  right card advances the panel
#      ->  wrong card is rejected, and the player tries again
#      ->  no confident read simply keeps waiting
#
#  Two ideas do the heavy lifting:
#
#  1. CONFIRM FRAMES. A single frame is never trusted. The same
#     card has to be read confidently several frames in a row
#     before anything is reported, so a card sliding into frame
#     cannot fire a false match.
#
#  2. WRONG CARDS STICK. A rejected card is remembered for a short
#     cooldown, so simply holding up the Fertilizer card does not
#     machine-gun "wrong" at the player. They have to actually
#     take it away and change cards.
#
#  Nothing here touches the game loop or any scene yet. It is a
#  standalone, fully testable unit.
# ============================================================

import pygame

import cardscan.camera as camera
import cardscan.features as features
import cardscan.marker as marker
import cardscan.model as model
import cardscan.preprocess as preprocess
import cardscan.registry as registry
import cardscan.targeted_verification as targeted_verification


# ── Tuning ──────────────────────────────────────────────────

# Frames the same card must read confidently before it counts.
CONFIRM_FRAMES = 4

# Seconds a rejected card stays suppressed after being reported.
WRONG_COOLDOWN = 1.6

# Seconds to wait after a match before accepting another one, so a
# panel transition is not double-fired.
MATCH_COOLDOWN = 0.8

# Max seconds between frames that still counts as "the card is
# being held there". Beyond this the streak resets, because the
# player has moved something.
MAX_GAP = 0.5


def _usable_marker_boundary(details):
    if details.get("blurry"):
        return False
    if details.get("area_ratio", 0.0) < preprocess.MIN_LIVE_CARD_AREA_RATIO:
        return False
    if details.get("quality", 0.0) < 0.42:
        return False
    if details.get("edge_support", 0.0) < 0.05:
        return False
    aspect = details.get("aspect", 0.0)
    return 0.50 <= aspect <= 0.92


class ScanResult:
    """One outcome from the scanner."""

    __slots__ = ("status", "card", "expected", "score")

    MATCH  = "match"
    WRONG  = "wrong"
    TIMEOUT = "timeout"
    ACCEPTED = "CARD_ACCEPTED"
    REJECTED = "CARD_REJECTED"
    UNCERTAIN = "SCAN_UNCERTAIN"

    def __init__(self, status, card, expected, score=0.0):
        self.status   = status      # one of MATCH / WRONG / TIMEOUT
        self.card     = card        # slug actually read, or None
        self.expected = expected    # slug the game asked for
        self.score    = score       # similarity 0.0 - 1.0

    @property
    def ok(self):
        """True when the right card was held up."""
        return self.status == self.MATCH

    def __repr__(self):
        return (f"<ScanResult {self.status} read={self.card!r} "
                f"want={self.expected!r} {self.score:.2f}>")


class CardScanner:
    """Holds the recognition state for one scan request.

    Typical use:

        scan = CardScanner()
        scan.start("AC-01 Water Card")

        # once per frame:
        result = scan.update(dt)
        if result and result.ok:
            advance_panel()

    start()  takes the same card string the chapter data uses, so
    it can be handed straight from a slide's "card" field.
    """

    def __init__(self, cam=None, model_data=None,
                 confirm_frames=CONFIRM_FRAMES,
                 wrong_cooldown=WRONG_COOLDOWN):
        self.cam             = cam
        self.model           = model_data if model_data is not None else model.load_model()
        self.confirm_frames  = max(1, int(confirm_frames))
        self.wrong_cooldown  = wrong_cooldown

        self.expected   = None        # slug the game asked for
        self.card       = None        # Card object
        self.active     = False
        self.t          = 0.0

        self.last_slug  = None        # current candidate streak
        self.streak     = 0
        self.last_t     = 0.0
        self.suppress   = {}          # slug -> time it was rejected
        self.match_at   = -99.0

        # Read-only view of the current frame, for a preview later.
        self.frame      = None
        self.last_score = 0.0
        self.saw_frame  = False   # did the last read actually deliver one?
        self.use_guide  = True    # fall back to the guide-box crop
        self.try_flipped = True   # also try the card rotated 180 degrees
        self.last_source = None   # "detected" | "guide" | None
        self.last_read  = None    # dict describing the latest frame's read
        self.marker_mode = preprocess.MARKER_MODE
        self.targeted = False
        self.threshold = None
        self.previous_points = None
        self.state = "WAITING_FOR_CARD"

    # ── Setup ────────────────────────────────────────────────

    def open_camera(self, **kwargs):
        self.cam = camera.open_camera(**kwargs)
        return self.cam

    @property
    def trained(self):
        return bool(
            self.model
            and self.model.get("cards")
            and self.model.get("feature_version") == features.PREPROCESS_VERSION
        )

    @property
    def can_recognize(self):
        return self.trained and len(self.model.get("cards", {})) >= 2

    def start(self, card_text=None, expected_card=None):
        """Begin waiting for a card.

        `card_text` is the chapter's display string, e.g.
        "AC-01 Water Card". Returns the resolved Card, or None if
        the string is not in the registry.
        """
        card = registry.resolve(card_text) if card_text else None
        if card is None and expected_card:
            card = registry.get(expected_card) or registry.resolve(expected_card)
        self.card     = card
        self.expected = card.slug if card else None
        if expected_card:
            self.expected = str(expected_card).strip().lower()
            if self.card is not None:
                self.expected = self.card.slug
        self.targeted = bool(expected_card)
        self.threshold = None
        self.previous_points = None
        self.state = "WAITING_FOR_CARD"
        self.frame = None
        self.saw_frame = False
        self.last_read = None
        self.last_source = None
        self.last_score = 0.0
        self.active   = True
        self.t        = 0.0
        self.last_slug = None
        self.streak   = 0
        self.last_t   = 0.0
        self.suppress = {}
        self.match_at = -99.0
        return card

    def stop(self):
        self.active = False
        self.expected = None
        self.card = None
        self.streak = 0
        self.last_slug = None
        self.targeted = False
        self.previous_points = None
        self.state = "WAITING_FOR_CARD"
        self.frame = None
        self.saw_frame = False
        self.last_read = None
        self.last_source = None
        self.last_score = 0.0

    def cancel(self):
        """Same as stop(), but also drops the camera."""
        self.stop()
        if self.cam:
            self.cam.release()
            self.cam = None

    # ── Per-frame ────────────────────────────────────────────

    def read_once(self):
        """Grab a single frame and classify it.

        Returns (slug, score, confident) with slug None when there
        is no camera, no model, or no readable frame. Camera frames
        are still captured without a trained model so preview clients
        can display live video.
        """
        if self.cam is None:
            self.saw_frame = False
            return None, 0.0, False

        self.last_read = None            # per-frame diagnostics (see below)
        self.frame = self.cam.read()
        self.saw_frame = self.frame is not None
        if self.frame is None:
            return None, 0.0, False

        if self.targeted:
            is_action_card = (
                self.expected == "analyze"
                or (
                    self.card is not None
                    and self.card.card_id.startswith("AC-")
                )
            )
            cands = preprocess.prepare_candidates(
                self.frame,
                max_candidates=3,
                fallback=None,
                previous=self.previous_points,
                fast_marker=not is_action_card,
            )
            top_details = cands[0][1] if cands else None
            marker_details = None
            if top_details and top_details.get("source") == "marker":
                marker_details = top_details
            elif top_details and top_details.get("marker_identity_only"):
                marker_details = next(
                    (details for _, details in cands
                     if details.get("marker_identity_only")
                     and _usable_marker_boundary(details)),
                    None,
                )
                if marker_details is None:
                    self.state = "SCAN_UNCERTAIN"
                    self.last_read = {
                        "slug": top_details.get("marker_slug"),
                        "score": 0.0,
                        "confident": False,
                        "reason": "action-card marker found but card boundary is unreliable",
                        "source": "marker",
                        "marker_id": top_details.get("marker_id"),
                        "targeted": True,
                    }
                    return None, 0.0, False
            marker_slug = marker_details.get("marker_slug") if marker_details else None
            if marker_slug is not None:
                top_details = marker_details
                points = top_details.get("points")
                if points is not None:
                    self.previous_points = points
                if top_details.get("blurry"):
                    self.state = "SCAN_UNCERTAIN"
                    self.last_read = {
                        "slug": marker_slug,
                        "score": 0.0,
                        "confident": False,
                        "reason": "marker frame is blurry",
                        "source": "marker",
                        "strategy": "aruco",
                        "quality": top_details.get("quality"),
                        "sharpness": top_details.get("sharpness"),
                        "blurry": True,
                        "marker_id": top_details.get("marker_id"),
                        "targeted": True,
                    }
                    return marker_slug, 0.0, False

                marker_matches = (
                    targeted_verification.model_slug(marker_slug)
                    == targeted_verification.model_slug(self.expected)
                )
                if marker_matches:
                    self.last_source = "marker"
                    self.last_score = 1.0
                    self.threshold = 1.0
                    self.state = "VERIFYING_EXPECTED_CARD"
                    self.last_read = {
                        "slug": marker_slug,
                        "score": 1.0,
                        "confident": True,
                        "reason": "ArUco marker matches expected card",
                        "source": "marker",
                        "strategy": "aruco",
                        "quality": top_details.get("quality"),
                        "sharpness": top_details.get("sharpness"),
                        "blurry": top_details.get("blurry"),
                        "marker_id": top_details.get("marker_id"),
                        "targeted": True,
                    }
                    return marker_slug, 1.0, True

                self.last_source = "marker"
                self.last_score = 1.0
                self.threshold = 1.0
                self.state = "CARD_DETECTED"
                self.last_read = {
                    "slug": marker_slug,
                    "score": 1.0,
                    "confident": False,
                    "reason": "ArUco marker does not match expected card",
                    "source": "marker",
                    "strategy": "aruco",
                    "quality": top_details.get("quality"),
                    "sharpness": top_details.get("sharpness"),
                    "blurry": top_details.get("blurry"),
                    "marker_id": top_details.get("marker_id"),
                    "targeted": True,
                }
                return marker_slug, 1.0, False

            if is_action_card:
                self.last_source = None
                self.last_score = 0.0
                self.state = "SCAN_UNCERTAIN"
                reason = (
                    "action card ArUco marker not detected"
                    if cands
                    else "action card boundary not found"
                )
                self.last_read = {
                    "slug": None,
                    "score": 0.0,
                    "confident": False,
                    "reason": reason,
                    "source": "image",
                    "targeted": True,
                }
                return None, 0.0, False

            if not self.can_recognize:
                self.state = "SCAN_UNCERTAIN"
                self.last_read = {
                    "slug": None,
                    "score": 0.0,
                    "confident": False,
                    "reason": (
                        "compatible card model unavailable; "
                        "targeted image matching cannot run"
                    ),
                    "targeted": True,
                }
                return None, 0.0, False

            best = None
            for canvas, details in cands:
                source = details.get("source")
                if source == "marker":
                    marker_slug = details.get("marker_slug")
                    if marker_slug is not None:
                        from cardscan.targeted_verification import model_slug
                        if model_slug(marker_slug) != model_slug(self.expected):
                            continue
                elif source != "detected":
                    continue
                if source != "marker":
                    if details.get("blurry"):
                        continue
                    if details.get("area_ratio", 0.0) < preprocess.MIN_LIVE_CARD_AREA_RATIO:
                        continue
                    if details.get("quality", 0.0) < 0.42:
                        continue
                    if details.get("edge_support", 0.0) < 0.05:
                        continue
                    aspect = details.get("aspect", 0.0)
                    if aspect < 0.50 or aspect > 0.92:
                        continue
                points = details.get("points")
                if points is not None and self.previous_points is not None:
                    import numpy as np
                    first = np.asarray(points, dtype=np.float32)
                    second = np.asarray(self.previous_points, dtype=np.float32)
                    if first.shape == second.shape:
                        diagonal = max(
                            float(np.linalg.norm(
                                np.asarray([
                                    [0.0, 0.0],
                                    [self.frame.get_width(),
                                     self.frame.get_height()],
                                ], dtype=np.float32)[1]
                            )),
                            1.0,
                        )
                        jump = float(np.mean(np.linalg.norm(first - second, axis=1)))
                        if jump / diagonal > 0.12:
                            continue
                views = [canvas]
                if self.try_flipped and source != "marker":
                    views.append(pygame.transform.rotate(canvas, 180))
                for view in views:
                    vec = features.extract_card(view)
                    info = targeted_verification.verify(
                        self.model, vec, self.expected
                    )
                    score = info["score"]
                    confident = info["accepted"]
                    read = (confident, score, details, info)
                    if (not confident
                            and (best is None or score > best[1])):
                        best = read
                    if confident:
                        best = read
                        break
                if best is not None and best[0]:
                    break
            if best is None:
                self.last_source = None
                self.previous_points = None
                self.state = "SCAN_UNCERTAIN"
                return None, 0.0, False

            confident, score, det, info = best
            self.last_source = det.get("source")
            self.last_score = score
            self.threshold = info["threshold"]
            self.previous_points = det.get("points")
            if confident:
                self.state = "VERIFYING_EXPECTED_CARD"
            else:
                self.state = "CARD_DETECTED" if det.get("points") else "SCAN_UNCERTAIN"
            self.last_read = {
                "slug": self.expected,
                "score": score,
                "confident": confident,
                "runner": None,
                "runner_score": 0.0,
                "gap": 0.0,
                "reason": info["reason"],
                "source": det.get("source"),
                "strategy": det.get("strategy"),
                "quality": det.get("quality"),
                "sharpness": det.get("sharpness"),
                "blurry": det.get("blurry"),
                "threshold": info["threshold"],
                "targeted": True,
            }
            return self.expected, score, confident

        if not self.can_recognize:
            return None, 0.0, False

        # Boundary detection returns a few ranked candidates. Take the
        # first one the card model is CONFIDENT about; otherwise keep the
        # best-scoring read. A geometrically plausible but wrong boundary
        # (inner frame, neighbouring card) scores poorly and is skipped.
        cands = preprocess.prepare_candidates(
            self.frame, max_candidates=3,
            fallback="guide" if self.use_guide else None,
            fast_marker=True)
        best = None
        for canvas, details in cands:
            # Boundary geometry cannot tell a card from the same card
            # upside down, so a read that is not confident upright is
            # retried rotated 180 degrees.
            views = [canvas]
            if self.try_flipped and not details.get("oriented_by_marker"):
                views.append(pygame.transform.rotate(canvas, 180))
            for view in views:
                vec = features.extract_card(view)
                info = model.classify_detailed(self.model, vec)
                slug, score = info["slug"], info["score"]
                confident = info["confident"]
                if slug is None:
                    continue
                read = (confident, score, slug, details.get("source"),
                        info, details)
                if best is None or read[:2] > best[:2]:
                    best = read
                if confident:
                    break
            if best is not None and best[0]:
                break
        top_details = cands[0][1] if cands else None
        marker_slug = (
            top_details.get("marker_slug")
            if top_details and (
                top_details.get("source") == "marker"
                or (
                    top_details.get("marker_identity_only")
                    and top_details.get("source") == "detected"
                )
            )
            else None
        )
        if marker_slug is not None:
            c_conf, c_score, c_slug = False, 0.0, None
            c_info = None
            if best is not None:
                c_conf, c_score, c_slug, _, c_info, _ = best
            if self.marker_mode == "strict":
                confident = bool(c_conf and c_slug == marker_slug)
                reason = "marker + classifier agree" if confident else "classifier not confident"
                score = c_score
            elif c_conf and c_slug != marker_slug:
                confident = False
                reason = "marker says %s, classifier says %s" % (marker_slug, c_slug)
                score = c_score
            else:
                confident = True
                reason = "marker"
                score = 1.0
            self.last_source = "marker"
            self.last_score = score
            self.last_read = {
                "slug": marker_slug,
                "score": score,
                "confident": confident,
                "runner": c_info["runner_slug"] if c_info else None,
                "runner_score": c_info["runner_score"] if c_info else 0.0,
                "gap": c_info["gap"] if c_info else 0.0,
                "reason": reason,
                "source": "marker",
                "strategy": "aruco",
                "quality": top_details.get("quality"),
                "sharpness": top_details.get("sharpness"),
                "blurry": top_details.get("blurry"),
                "marker_id": top_details.get("marker_id"),
                "classifier_slug": c_slug,
                "classifier_confident": c_conf,
            }
            return marker_slug, score, confident
        if best is None:
            self.last_source = None
            return None, 0.0, False

        confident, score, slug, self.last_source, info, det = best
        self.last_score = score
        # Everything tools/live_test.py needs to explain this frame.
        self.last_read = {
            "slug": slug, "score": score, "confident": confident,
            "runner": info["runner_slug"], "runner_score": info["runner_score"],
            "gap": info["gap"], "reason": info["reason"],
            "source": det.get("source"), "strategy": det.get("strategy"),
            "quality": det.get("quality"), "sharpness": det.get("sharpness"),
            "blurry": det.get("blurry"),
        }
        return slug, score, confident

    def update(self, dt):
        """Advance the scanner by one frame.

        Returns a ScanResult when something happened (a match, a
        rejected card), otherwise None.
        """
        if not self.active:
            return None

        self.t += dt
        slug, score, confident = self.read_once()

        if slug is None:
            self.streak = 0
            self.last_slug = None
            return None

        if self.targeted and not confident:
            if (
                slug is not None
                and slug != self.expected
                and self.last_read
                and self.last_read.get("source") == "marker"
            ):
                until = self.suppress.get(slug, 0.0)
                if self.t < until:
                    return None
                self.suppress[slug] = self.t + self.wrong_cooldown
                return ScanResult(
                    ScanResult.WRONG,
                    slug,
                    self.expected,
                    score,
                )
            until = self.suppress.get("target_card", 0.0)
            self.state = "CARD_REJECTED"
            self.streak = 0
            self.last_slug = None
            if self.t < until:
                return None
            self.suppress["target_card"] = self.t + self.wrong_cooldown
            return ScanResult(
                ScanResult.REJECTED,
                None,
                self.expected,
                score,
            )

        # A long gap means something moved; the streak is stale.
        if self.last_slug is not None and (self.t - self.last_t) > MAX_GAP:
            self.streak = 0
        self.last_t = self.t

        if not confident:
            # Ambiguous or low-confidence: keep waiting quietly
            # rather than telling the player they got it wrong.
            self.streak = 0
            self.last_slug = None
            return None

        if slug != self.last_slug:
            self.last_slug = slug
            self.streak = 1
        else:
            self.streak += 1

        # A guide-box crop is less trustworthy than a detected boundary,
        # so it must hold for a couple more frames.
        need = self.confirm_frames + (2 if self.last_source == "guide" else 0)
        if self.streak < need:
            return None

        # Confirmed: same card, confidently, several frames running.
        self.streak = 0
        self.last_slug = None

        if slug == self.expected:
            # One card in view should mean one match. Without this the
            # same card would re-match every few frames for as long as
            # it stayed in shot, and the caller could advance twice.
            if (self.t - self.match_at) < MATCH_COOLDOWN:
                return None
            self.match_at = self.t
            self.state = "CARD_ACCEPTED"
            return ScanResult(ScanResult.MATCH, slug, self.expected, score)

        until = self.suppress.get(slug, 0.0)
        if self.t < until:
            return None                    # already told them; be quiet

        self.suppress[slug] = self.t + self.wrong_cooldown
        return ScanResult(ScanResult.WRONG, slug, self.expected, score)

    # ── Introspection ────────────────────────────────────────

    def progress(self):
        """0.0 - 1.0 toward a confirmed read, for a loading hint."""
        if not self.active or self.confirm_frames <= 0:
            return 0.0
        return min(1.0, self.streak / float(self.confirm_frames))

    def status(self):
        """One-line summary for logs and the debug overlay."""
        if not self.active:
            return "idle"
        if not self.trained and not self.targeted:
            return "no current model (run tools/train_cards.py)"
        if not self.can_recognize and not self.targeted:
            return "only one card class trained; train another card to enable recognition"
        if not self.can_recognize and self.targeted:
            if self.last_read and self.last_read.get("reason"):
                return self.last_read["reason"]
            return "model unavailable; targeted matching requires a recognizable card marker"
        if self.cam is None or not self.cam.is_open:
            return "camera not open"
        if not self.saw_frame:
            return f"{self.cam.backend} camera returning no frame"
        resolution = f"{self.frame.get_width()}x{self.frame.get_height()}"
        if self.last_slug is None:
            if (
                self.last_read
                and self.last_read.get("reason")
                == "action card ArUco marker not detected"
            ):
                return "Hold the action card so its ArUco marker is visible"
            detection = preprocess.last_detection()
            if detection.get("status") == "failed":
                return (
                    f"{resolution} | card boundary not found: "
                    f"{detection.get('reason', 'retry capture')}"
                )
            if detection.get("blurry"):
                return (f"{resolution} | image looks blurry "
                        f"(sharpness {detection.get('sharpness')}): "
                        "hold the card 20-30 cm away / lock focus")
            return f"{resolution} | waiting for {self.expected}"
        return (f"{resolution} | reading {self.last_slug} "
                f"{self.progress() * 100:.0f}% ({self.last_score:.2f})")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.cancel()
        return False
