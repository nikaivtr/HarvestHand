"""Launch the standalone HarvestHand Recognition Lab."""

from __future__ import annotations

import sys
import json
import time
import uuid
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pygame

from recognition_lab.analysis import (
    audit_annotations,
    benchmark_annotations,
    build_outer_profile,
    compare_experimental_models,
    evaluate_candidate_generation,
    evaluate_centroid_ranker,
    feature_summary,
)
from recognition_lab.engines import (
    CandidateTracker,
    compare_images,
    detect_boundary_candidates,
    ocr_text,
    perspective_crop,
    read_image,
)
from recognition_lab.paths import EXPORTS, REPORTS, ensure_layout
from recognition_lab.reports import (
    export_candidate_annotations,
    export_phase1_audit,
    export_phase1_audit_visuals,
    export_report,
)
from recognition_lab.storage import IMAGE_SUFFIXES, Store


WIDTH, HEIGHT = 1280, 760
BG = (20, 25, 32)
PANEL = (31, 39, 49)
PANEL2 = (39, 49, 61)
TEXT = (235, 240, 244)
MUTED = (156, 169, 181)
ACCENT = (86, 190, 160)
WARNING = (237, 177, 82)
CANDIDATE_COLORS = [
    (75, 205, 160), (95, 160, 240), (235, 155, 75),
    (205, 120, 225), (235, 95, 120), (155, 210, 95),
    (90, 205, 220), (235, 215, 90),
]


class RecognitionLab:
    def __init__(self) -> None:
        ensure_layout()
        self.store = Store()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("HarvestHand Recognition Lab")
        self.font = pygame.font.Font(None, 25)
        self.small = pygame.font.Font(None, 20)
        self.title = pygame.font.Font(None, 38)
        self.page = "Dashboard"
        self.message = "Ready. Import original references or camera observations to begin."
        self.camera = None
        self.camera_device = 0
        self.camera_backend = "unopened"
        self.camera_read_failures = 0
        self.last_frame = None
        self.running_camera = False
        self.session_id = uuid.uuid4().hex[:12]
        self.boundary_tracker = CandidateTracker(
            max_candidates=12, match_threshold=0.35,
            grace_seconds=0.75, smoothing=0.35,
        )
        self.boundary_candidates = []
        self.boundary_detection_frequency = 1
        self.boundary_frame_number = 0
        self.boundary_frames = 0
        self.boundary_detected_total = 0
        self.boundary_last_detection_ms = 0.0
        self.boundary_last_update = time.monotonic()
        self.review_mode = "review"
        self.review_queue = []
        self.review_index = 0
        self.review_clear_pending = False
        self.diagnostic_selected_id = None
        self.boundary_benchmark = self._load_boundary_benchmark()
        self.phase1_audit = self._load_phase1_audit()
        self.phase1_inspection_index = 0
        self.boundary_settings = {
            "max_candidates": 12,
            "min_area_ratio": 0.01,
            "max_area_ratio": 0.92,
            "min_aspect_ratio": 0.45,
            "max_aspect_ratio": 0.90,
            "max_perspective_distortion": 0.45,
            "min_edge_support": 0.08,
            "match_threshold": 0.35,
            "grace_seconds": 0.75,
            "smoothing": 0.35,
        }
        self.phase_pages = {"Phase 1: Boundary Recognition": "phase1",
                            "Phase 2: Illustration Identification": "phase2",
                            "Phase 3: Text Recognition / OCR": "phase3"}
        self.buttons = []
        self._load_previous_review_records()

    def _load_boundary_benchmark(self) -> dict | None:
        raw = self.store.get_setting("boundary_benchmark", "")
        expected_count = self.store.get_setting("boundary_benchmark_annotation_count", "")
        if not raw or expected_count != str(len(self.store.candidate_annotations())):
            return None
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            return None
        return value if isinstance(value, dict) else None

    def _invalidate_boundary_benchmark(self) -> None:
        self.boundary_benchmark = None
        self.store.set_setting("boundary_benchmark", "")
        self.store.set_setting("boundary_benchmark_annotation_count", "")

    def _load_phase1_audit(self) -> dict | None:
        path = REPORTS / "phase1_ground_truth_audit.json"
        if not path.exists():
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        if value.get("audit", {}).get("total") != len(self.store.candidate_annotations()):
            return None
        cases = value.get("generation", {}).get("cases", [])
        if cases and "ground_truth_points" not in cases[0]:
            return None
        return value

    def _load_previous_review_records(self) -> None:
        """Make persisted annotations revisitable without mixing session IDs."""
        for row in self.store.candidate_annotations()[:24]:
            frame_path = Path(row["frame_path"])
            if not frame_path.exists():
                continue
            try:
                frame = read_image(frame_path)
                points = json.loads(row["corners_json"])
                metrics = json.loads(row["metrics_json"])
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            self.review_queue.append({
                "candidate_id": int(row["candidate_id"]),
                "session_id": row["session_id"],
                "points": __import__("numpy").float32(points),
                "metrics": metrics,
                "status": row["tracking_status"],
                "judgment": row["judgment"],
                "frame": frame,
                "frame_path": row["frame_path"],
                "crop_path": row["crop_path"],
                "persisted": True,
            })

    def text(self, value: str, position: tuple[int, int], color=TEXT, font=None) -> None:
        self.screen.blit((font or self.font).render(value, True, color), position)

    def fitted_text(
        self, value: str, position: tuple[int, int], max_width: int,
        color=TEXT, font=None,
    ) -> None:
        selected_font = font or self.font
        suffix = "..."
        rendered = selected_font.render(value, True, color)
        if rendered.get_width() <= max_width:
            self.screen.blit(rendered, position)
            return
        shortened = value
        while shortened and selected_font.size(shortened + suffix)[0] > max_width:
            shortened = shortened[:-1]
        self.screen.blit(selected_font.render(shortened + suffix, True, color), position)

    def button(self, label: str, rect: pygame.Rect, action: str, selected=False) -> None:
        pygame.draw.rect(self.screen, ACCENT if selected else PANEL2, rect, border_radius=6)
        font = self.small if rect.height < 30 else self.font
        text_height = font.get_height()
        self.fitted_text(
            label,
            (rect.x + 7, rect.y + max(1, (rect.height - text_height) // 2)),
            rect.width - 14,
            BG if selected else TEXT, font,
        )
        self.buttons.append((rect, action))

    def draw(self) -> None:
        self.screen.fill(BG)
        self.buttons = []
        pygame.draw.rect(self.screen, PANEL, (0, 0, 245, HEIGHT))
        self.text("RECOGNITION LAB", (24, 25), ACCENT, self.small)
        nav = [
            ("Dashboard", "Dashboard"),
            ("Phase 1: Boundary", "Phase 1: Boundary Recognition"),
            ("Phase 1: Evaluation", "Phase 1 Evaluation"),
            ("Phase 2: Illustration", "Phase 2: Illustration Identification"),
            ("Phase 3: Text / OCR", "Phase 3: Text Recognition / OCR"),
            ("Boundary Analysis", "Boundary Analysis"),
            ("Materials & Database", "Materials & Database"),
            ("Dataset Manager", "Dataset Manager"),
            ("Experiments & Models", "Experiments & Models"),
            ("Reports & Evaluation", "Reports & Evaluation"),
            ("Settings", "Settings"),
        ]
        y = 72
        for label, action in nav:
            self.button(label, pygame.Rect(15, y, 215, 37), action, self.page == action)
            y += 43
        self.text("Experimental only", (24, HEIGHT - 48), WARNING, self.small)
        self.text(self.message[:125], (270, HEIGHT - 36), MUTED, self.small)
        self.text(self.page, (270, 28), TEXT, self.title)
        if self.page == "Dashboard":
            self.dashboard()
        elif self.page in self.phase_pages:
            self.phase(self.phase_pages[self.page])
        elif self.page == "Phase 1 Evaluation":
            self.phase1_evaluation()
        elif self.page == "Boundary Analysis":
            self.boundary_analysis()
        elif self.page == "Materials & Database":
            self.materials()
        elif self.page == "Reports & Evaluation":
            self.reports()
        elif self.page == "Experiments & Models":
            self.experiments()
        elif self.page == "Dataset Manager":
            self.dataset()
        else:
            self.settings()

    def dashboard(self) -> None:
        counts = self.store.counts()
        cards = [("Materials", counts["materials"]), ("Verified observations", counts["observations"]),
                 ("Experiments", counts["experiments"])]
        for index, (label, value) in enumerate(cards):
            x = 270 + index * 205
            pygame.draw.rect(self.screen, PANEL, (x, 92, 185, 100), border_radius=8)
            self.text(label, (x + 15, 110), MUTED, self.small)
            self.text(str(value), (x + 15, 145), ACCENT, self.title)
        pygame.draw.rect(self.screen, PANEL, (270, 225, 710, 300), border_radius=8)
        self.text("Start here", (295, 250), TEXT, self.title)
        self.text("1. Import original card artwork in Materials & Database.", (295, 305), TEXT)
        self.text("2. Run a phase with an image or camera.", (295, 340), TEXT)
        self.text("3. Verify every prediction before saving it.", (295, 375), TEXT)
        self.text("No experimental result is sent to the game automatically.", (295, 430), WARNING)

    def phase(self, phase: str) -> None:
        if phase == "phase1":
            self.phase1()
            return
        pygame.draw.rect(self.screen, PANEL, (270, 90, 710, 470), border_radius=8)
        self.text("Live camera is optional; imported images work offline.", (295, 115), MUTED)
        self.button("Open camera", pygame.Rect(295, 155, 150, 40), "camera")
        self.button("Stop camera", pygame.Rect(455, 155, 150, 40), "stop_camera")
        self.button("Import image", pygame.Rect(615, 155, 150, 40), "import")
        self.button("Save correct", pygame.Rect(775, 155, 150, 40), "save_correct")
        self.button("Save incorrect", pygame.Rect(295, 205, 150, 40), "save_incorrect")
        self.button("Save uncertain", pygame.Rect(455, 205, 150, 40), "save_uncertain")
        if self.last_frame is not None:
            preview = self.last_frame.copy()
            if phase == "phase1":
                result = detect_boundary(preview)
                if result["found"]:
                    import cv2
                    points = __import__("numpy").int32(result["points"])
                    cv2.polylines(preview, [points], True, (70, 220, 130), 4)
                    self.text(f"Boundary score: {result['score']:.2f}", (295, 270), ACCENT)
                else:
                    self.text("Boundary: LOST / no verified quadrilateral", (295, 270), WARNING)
            elif phase == "phase3":
                result = ocr_text(preview)
                self.text(result["message"], (295, 270), WARNING, self.small)
            else:
                references = self.store.materials("phase2")
                if references:
                    try:
                        score = compare_images(preview, read_image(references[0]["path"]))
                        self.text(
                            f"Top reference: {Path(references[0]['path']).name}  "
                            f"combined score {score['combined']:.2f}",
                            (295, 270), ACCENT, self.small,
                        )
                    except ValueError as error:
                        self.text(f"Reference comparison failed: {error}", (295, 270), WARNING, self.small)
                else:
                    self.text("Import one or more phase2 references to compare illustrations.", (295, 270), TEXT)
            preview = pygame.surfarray.make_surface(preview[:, :, ::-1].swapaxes(0, 1))
            preview = pygame.transform.smoothscale(preview, (360, 250))
            self.screen.blit(preview, (295, 310))
        else:
            self.text("No frame available. Import an image or open a camera.", (295, 300), MUTED)
        self.text(f"Phase data: recognition_lab/materials/{phase}", (295, 535), MUTED, self.small)

    def _fit_preview(self, image, size: tuple[int, int]):
        surface = pygame.surfarray.make_surface(image[:, :, ::-1].swapaxes(0, 1))
        scale = min(size[0] / surface.get_width(), size[1] / surface.get_height())
        fitted = pygame.transform.smoothscale(
            surface,
            (max(1, int(surface.get_width() * scale)), max(1, int(surface.get_height() * scale))),
        )
        canvas = pygame.Surface(size)
        canvas.fill((10, 14, 19))
        canvas.blit(fitted, ((size[0] - fitted.get_width()) // 2, (size[1] - fitted.get_height()) // 2))
        return canvas

    def _draw_candidate_overlay(self, image, candidate: dict) -> None:
        import cv2
        import numpy as np

        points = np.rint(candidate["points"]).astype(np.int32)
        color_rgb = CANDIDATE_COLORS[(candidate["id"] - 1) % len(CANDIDATE_COLORS)]
        color = color_rgb[::-1]
        status = candidate["status"]
        if status == "temporarily_lost":
            for start, end in zip(points, np.roll(points, -1, axis=0)):
                for fraction in np.linspace(0, 1, 12)[::2]:
                    begin = start * (1 - fraction)
                    finish = start * (1 - min(fraction + 0.1, 1)) + end * min(fraction + 0.1, 1)
                    cv2.line(image, tuple(np.rint(begin).astype(int)), tuple(np.rint(finish).astype(int)), color, 2)
        else:
            thickness = 3 if status == "live" else 2
            cv2.polylines(image, [points], True, color, thickness)
        for index, point in enumerate(points):
            x, y = int(point[0]), int(point[1])
            cv2.circle(image, (x, y), 7, color, -1)
            cv2.putText(image, str(index + 1), (x + 7, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
        label = f"#{candidate['id']} {status}"
        cv2.putText(image, label, tuple(points[0] + np.array([4, -10])), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    def phase1(self) -> None:
        pygame.draw.rect(self.screen, PANEL, (270, 90, 970, 610), border_radius=8)
        self.text(
            "Phase 1 boundary review"
            if self.review_mode == "review"
            else "Phase 1 diagnostic view",
            (295, 112), TEXT, self.title,
        )
        self.text(
            f"Session {self.session_id} | active {len(self.boundary_candidates)} | "
            f"queue {len(self.review_queue)}",
            (295, 138), ACCENT, self.small,
        )
        self.button("REVIEW MODE", pygame.Rect(295, 155, 140, 36), "mode:review",
                    self.review_mode == "review")
        self.button("DIAGNOSTIC MODE", pygame.Rect(445, 155, 175, 36), "mode:diagnostic",
                    self.review_mode == "diagnostic")
        self.button("Open camera", pygame.Rect(295, 195, 140, 36), "camera")
        self.button("Stop camera", pygame.Rect(445, 195, 140, 36), "stop_camera")
        self.button("Import image", pygame.Rect(595, 195, 140, 36), "import")
        self.button("Export annotations", pygame.Rect(745, 195, 160, 36), "export_candidates")
        self.button("Clear queue", pygame.Rect(915, 195, 140, 36), "clear_queue")
        self.button("Reset tracker", pygame.Rect(1065, 195, 140, 36), "reset_boundary")
        if self.review_mode == "review":
            self.review_phase()
        else:
            self.diagnostic_phase()

    def review_phase(self) -> None:
        preview_rect = pygame.Rect(295, 250, 560, 370)
        item = self.review_queue[self.review_index] if self.review_queue else None
        if item is not None:
            overlay = item["frame"].copy()
            self._draw_candidate_overlay(overlay, {
                "id": item["candidate_id"], "points": item["points"], "status": "selected",
            })
            self.screen.blit(self._fit_preview(overlay, preview_rect.size), preview_rect.topleft)
            crop = perspective_crop(item["frame"], item["points"].tolist(), size=(300, 420))
            self.screen.blit(self._fit_preview(crop, (190, 265)), (875, 250))
            metrics = item["metrics"]
            self.text(
                f"Candidate {self.review_index + 1} of {len(self.review_queue)} | "
                f"{item['judgment'] or 'UNREVIEWED'}",
                (295, 625), ACCENT, self.small,
            )
            self.fitted_text(
                f"area {metrics.get('area_ratio', 0):.3f} aspect {metrics.get('aspect_ratio', 0):.2f} "
                f"edge {metrics.get('edge_support', 0):.2f} "
                f"ref {metrics.get('outer_reference_score', 0):.2f}",
                (875, 530), 340, TEXT, self.small,
            )
            self.fitted_text(
                f"method {metrics.get('detection_method', 'unknown')} | status {item['status']}",
                (875, 552), 340, MUTED, self.small,
            )
            if metrics.get("likely_internal_region"):
                self.fitted_text(
                    "LIKELY INTERNAL REGION - diagnostic only; CORRECT disabled",
                    (875, 574), 340, WARNING, self.small,
                )
        else:
            pygame.draw.rect(self.screen, (10, 14, 19), preview_rect, border_radius=5)
            self.text("Waiting for a geometrically valid candidate.", (380, 420), MUTED)
            self.text("Candidates are collected in the background.", (380, 455), MUTED, self.small)
        reviewed = sum(item.get("judgment") is not None for item in self.review_queue)
        self.text(
            f"reviewed {reviewed} | pending {len(self.review_queue) - reviewed} | "
            f"remaining {max(0, len(self.review_queue) - self.review_index - 1)}",
            (295, 675), MUTED, self.small,
        )
        self.button("PREVIOUS", pygame.Rect(875, 585, 100, 30), "review:previous")
        can_next = item is not None and item.get("judgment") is not None
        next_rect = pygame.Rect(985, 585, 130, 30)
        if can_next:
            self.button("NEXT CANDIDATE", next_rect, "review:next", True)
        else:
            pygame.draw.rect(self.screen, (55, 62, 70), next_rect, border_radius=6)
            self.fitted_text("DECIDE FIRST", (next_rect.x + 7, next_rect.y + 8),
                             next_rect.width - 14, MUTED, self.small)
        outer_score = item["metrics"].get("outer_reference_score")
        can_mark_correct = (
            item is not None
            and not item["metrics"].get("likely_internal_region")
            and (outer_score is None or outer_score >= 0.35)
        )
        if can_mark_correct:
            self.button("CORRECT", pygame.Rect(875, 625, 100, 30), "review:correct")
        else:
            pygame.draw.rect(self.screen, (55, 62, 70), pygame.Rect(875, 625, 100, 30), border_radius=6)
            self.fitted_text("CORRECT", (882, 633), 86, MUTED, self.small)
        self.button("INCORRECT", pygame.Rect(985, 625, 100, 30), "review:incorrect")
        self.button("UNSURE", pygame.Rect(1095, 625, 90, 30), "review:unsure")

    def diagnostic_phase(self) -> None:
        preview_rect = pygame.Rect(295, 250, 610, 390)
        if self.last_frame is not None:
            overlay = self.last_frame.copy()
            for candidate in self.boundary_candidates:
                self._draw_candidate_overlay(overlay, candidate)
            self.screen.blit(self._fit_preview(overlay, preview_rect.size), preview_rect.topleft)
        else:
            pygame.draw.rect(self.screen, (10, 14, 19), preview_rect, border_radius=5)
            self.text("Open the camera or import an image.", (445, 420), MUTED)
        self.text("CANDIDATES", (930, 250), TEXT, self.small)
        self.text("solid=live  thin=tracked  dotted=temporarily lost", (930, 272), MUTED, self.small)
        y = 295
        for candidate in self.boundary_candidates[:6]:
            row = pygame.Rect(920, y, 300, 58)
            pygame.draw.rect(self.screen, PANEL2, row, border_radius=5)
            color = CANDIDATE_COLORS[(candidate["id"] - 1) % len(CANDIDATE_COLORS)]
            pygame.draw.rect(self.screen, color, (row.x, row.y, 5, row.height), border_radius=3)
            metrics = candidate["metrics"]
            judgment = candidate.get("judgment") or "unreviewed"
            self.fitted_text(
                f"#{candidate['id']} {candidate['status']} | {judgment}",
                (row.x + 12, row.y + 6), 280, color, self.small,
            )
            self.fitted_text(
                f"area {metrics['area_ratio']:.3f}  aspect {metrics['aspect_ratio']:.2f}  "
                f"conf {metrics['confidence']:.2f}"
                + (" | INTERNAL" if metrics.get("likely_internal_region") else ""),
                (row.x + 12, row.y + 27), 280, TEXT, self.small,
            )
            self.button("Inspect", pygame.Rect(row.x + 220, row.y + 17, 70, 24),
                        f"diagnostic:{candidate['id']}")
            y += 62
        selected = next(
            (candidate for candidate in self.boundary_candidates
             if candidate["id"] == self.diagnostic_selected_id), None
        )
        if selected is not None and self.last_frame is not None:
            crop = perspective_crop(self.last_frame, selected["points"].tolist(), size=(220, 310))
            self.screen.blit(self._fit_preview(crop, (150, 190)), (1060, 575))
        self.text(
            f"frames {self.boundary_frames} | candidates/frame {self.boundary_detected_total}/"
            f"{max(self.boundary_frames, 1)} | detection frequency {self.boundary_detection_frequency}",
            (295, 655), MUTED, self.small,
        )

    def update_boundary(self, dt: float) -> None:
        if self.last_frame is None:
            self.boundary_candidates = []
            return
        self.boundary_frame_number += 1
        detect_now = self.boundary_frame_number % self.boundary_detection_frequency == 0
        detections = []
        started = time.perf_counter()
        if detect_now:
            detection_settings = {
                key: self.boundary_settings[key]
                for key in (
                    "max_candidates", "min_area_ratio", "max_area_ratio",
                    "min_aspect_ratio", "max_aspect_ratio",
                    "max_perspective_distortion", "min_edge_support",
                )
            }
            profile = (
                build_outer_profile(self.store.candidate_annotations())
                if self.boundary_benchmark is not None
                else None
            )
            detections = detect_boundary_candidates(
                self.last_frame, outer_profile=profile, **detection_settings
            )
            self.boundary_last_detection_ms = (time.perf_counter() - started) * 1000.0
            self.boundary_frames += 1
            self.boundary_detected_total += len(detections)
        self.boundary_candidates = self.boundary_tracker.update(detections, dt, detected=detect_now)
        for candidate in self.boundary_candidates:
            candidate["judgment"] = self.store.candidate_judgment(
                self.session_id, candidate["id"]
            ) or candidate.get("judgment")
            self._collect_review_candidate(candidate)

    def _collect_review_candidate(self, candidate: dict) -> None:
        import numpy as np
        from recognition_lab.engines import CandidateTracker

        if any(
            item["session_id"] == self.session_id
            and item["candidate_id"] == candidate["id"]
            for item in self.review_queue
        ):
            return
        if any(
            item["session_id"] == self.session_id
            and CandidateTracker._distance(item["points"], candidate["points"]) < 0.12
            for item in self.review_queue
        ):
            return
        item = {
            "candidate_id": candidate["id"],
            "session_id": self.session_id,
            "points": np.float32(candidate["points"]).copy(),
            "metrics": dict(candidate["metrics"]),
            "status": candidate["status"],
            "judgment": self.store.candidate_judgment(self.session_id, candidate["id"]),
            "frame": self.last_frame.copy(),
            "frame_path": None,
            "crop_path": None,
            "persisted": False,
        }
        self._save_queue_capture(item)
        self.review_queue.append(item)

    def _save_queue_capture(self, item: dict) -> None:
        import cv2

        output = EXPORTS / "phase1_candidates" / item["session_id"]
        output.mkdir(parents=True, exist_ok=True)
        stem = f"candidate_{item['candidate_id']}_{int(time.time() * 1000)}"
        frame_path = output / f"{stem}.png"
        crop_path = output / f"{stem}_crop.png"
        if cv2.imwrite(str(frame_path), item["frame"]):
            crop = perspective_crop(item["frame"], item["points"].tolist())
            if cv2.imwrite(str(crop_path), crop):
                item["frame_path"] = str(frame_path)
                item["crop_path"] = str(crop_path)

    def _review_item(self) -> dict | None:
        if not self.review_queue:
            return None
        self.review_index = max(0, min(self.review_index, len(self.review_queue) - 1))
        return self.review_queue[self.review_index]

    def _save_review_judgment(self, judgment: str) -> None:
        item = self._review_item()
        if item is None:
            self.message = "There is no candidate selected for review."
            return
        if item["frame_path"] is None:
            self._save_queue_capture(item)
        elif item.get("crop_path") is None:
            import cv2
            crop_path = Path(item["frame_path"]).with_name(
                Path(item["frame_path"]).stem + "_crop.png"
            )
            if cv2.imwrite(str(crop_path), perspective_crop(item["frame"], item["points"].tolist())):
                item["crop_path"] = str(crop_path)
        if item["frame_path"] is None:
            self.message = "Could not preserve the original candidate frame."
            return
        self.store.save_candidate_annotation(
            item["session_id"], item["candidate_id"], item["frame_path"],
            item["points"].tolist(), item["metrics"],
            item["metrics"].get("detection_method", "unknown"), item["status"],
            judgment, item.get("crop_path"),
        )
        item["judgment"] = judgment
        self._invalidate_boundary_benchmark()
        self.message = f"Candidate {self.review_index + 1} marked {judgment}."

    def save_candidate_judgment(self, candidate_id: int, judgment: str) -> None:
        candidate = next(
            (item for item in self.boundary_candidates if item["id"] == candidate_id), None
        )
        if candidate is None:
            self.message = f"Candidate #{candidate_id} is no longer active; no decision saved."
            return
        if judgment == "reset":
            self.store.reset_candidate_annotation(self.session_id, candidate_id)
            candidate["judgment"] = None
            self.message = f"Reset candidate #{candidate_id}."
            return
        if self.last_frame is None:
            self.message = "No original frame is available for this candidate."
            return
        import cv2
        output = EXPORTS / "phase1_candidates" / self.session_id
        output.mkdir(parents=True, exist_ok=True)
        frame_path = output / f"candidate_{candidate_id}_{int(time.time() * 1000)}.png"
        if not cv2.imwrite(str(frame_path), self.last_frame):
            self.message = f"Could not save frame for candidate #{candidate_id}."
            return
        self.store.save_candidate_annotation(
            self.session_id, candidate_id, str(frame_path),
            candidate["points"].tolist(), candidate["metrics"],
            candidate["metrics"]["detection_method"], candidate["status"], judgment,
        )
        candidate["judgment"] = judgment
        self._invalidate_boundary_benchmark()
        self.message = f"Saved candidate #{candidate_id} as {judgment}."

    def boundary_analysis(self) -> None:
        rows = self.store.candidate_annotations()
        summary = feature_summary(rows)
        pygame.draw.rect(self.screen, PANEL, (270, 90, 970, 610), border_radius=8)
        self.text("Candidate Analysis", (295, 112), TEXT, self.title)
        self.text(
            "Only CORRECT and INCORRECT samples are eligible for supervised analysis; "
            "UNSURE remains retained but excluded.",
            (295, 158), MUTED, self.small,
        )
        self.button("Benchmark outer boundary", pygame.Rect(930, 112, 270, 32), "benchmark:boundary")
        self.button("Run dataset audit", pygame.Rect(700, 112, 210, 32), "audit:phase1")
        counts = {value: sum(row["judgment"] == value for row in rows) for value in ("correct", "incorrect", "unsure")}
        cards = [("Correct", counts["correct"], ACCENT), ("Incorrect", counts["incorrect"], WARNING),
                 ("Unsure", counts["unsure"], MUTED), ("Total", len(rows), TEXT)]
        for index, (label, value, color) in enumerate(cards):
            x = 295 + index * 160
            pygame.draw.rect(self.screen, PANEL2, (x, 195, 140, 90), border_radius=6)
            self.text(label, (x + 12, 210), MUTED, self.small)
            self.text(str(value), (x + 12, 238), color, self.title)
        if not rows:
            self.text("No manually verified candidates yet.", (295, 335), WARNING)
            self.text("Open Phase 1 and judge candidates with OK, NO, or ?.", (295, 370), TEXT)
            return
        if self.boundary_benchmark is None:
            self.fitted_text(
                "Run Benchmark outer boundary before any supervised ranking experiment.",
                (295, 315), 880, WARNING, self.small,
            )
        else:
            evaluation = evaluate_centroid_ranker(rows)
            self.fitted_text(evaluation["message"], (295, 315), 880, WARNING, self.small)
            if evaluation.get("ready"):
                self.text(
                    f"Held-out baseline ({evaluation['method']}): "
                    f"{evaluation['held_out_accuracy']:.2f} on {evaluation['held_out_samples']} samples",
                    (295, 340), ACCENT, self.small,
                )
        profile = build_outer_profile(rows)
        self.text(
            f"Reference supervision loaded: {profile['correct_count']} CORRECT outer references; "
            f"{profile['incorrect_count']} INCORRECT negatives",
            (295, 360), ACCENT, self.small,
        )
        if self.boundary_benchmark:
            benchmark = self.boundary_benchmark
            recall = "-" if benchmark["recall"] is None else f"{benchmark['recall']:.2%}"
            mean_iou = "-" if benchmark["mean_iou"] is None else f"{benchmark['mean_iou']:.3f}"
            corner_error = "-" if benchmark["mean_corner_error"] is None else f"{benchmark['mean_corner_error']:.3f}"
            self.fitted_text(
                f"Stage A generation: recall {recall} | IoU {mean_iou} | "
                f"corner error {corner_error} | no outer boundary {benchmark['missed']}"
                if benchmark["held_out_recall"] is not None
                else f"Stage A generation: recall {recall} | IoU {mean_iou} | "
                     f"corner error {corner_error} | no outer boundary {benchmark['missed']}",
                (295, 382), 880, TEXT, self.small,
            )
            self.fitted_text(
                f"Stage B ranking: top-1 {benchmark['ranking_top1_accuracy']:.2%} | "
                f"mean matching rank {benchmark['ranking_mean_match_rank']:.2f}"
                if benchmark["ranking_top1_accuracy"] is not None
                else "Stage B ranking: -",
                (295, 400), 880, WARNING, self.small,
            )
            self.fitted_text(
                f"Session-held-out: recall {benchmark['held_out_recall']:.2%} | "
                f"top-1 ranking {benchmark['held_out_ranking_top1_accuracy']:.2%}"
                if benchmark["held_out_recall"] is not None
                else "Session-held-out evaluation unavailable (one session only).",
                (295, 418), 880, TEXT, self.small,
            )
            self.fitted_text(
                f"Negative reproduction {benchmark['incorrect_reproduction_rate']:.2%} | "
                f"false-acceptance estimate {benchmark['internal_region_false_acceptance_rate']:.2%}"
                if benchmark["internal_region_false_acceptance_rate"] is not None
                else "Negative reproduction / false-acceptance estimate: -",
                (295, 436), 880, WARNING, self.small,
            )
        if self.phase1_audit:
            audit = self.phase1_audit["audit"]
            generation = self.phase1_audit["generation"]
            models = self.phase1_audit["models"]
            self.fitted_text(
                f"Audit: decoded {audit['decoded_images']}/{audit['total']} | "
                f"questionable {len(audit['questionable'])} | "
                f"near-duplicate samples {audit['near_duplicate_sample_count']}",
                (295, 454), 880, TEXT, self.small,
            )
            self.fitted_text(
                f"Generation: IoU .50 {generation['iou_0_5_recall']:.2%} | "
                f"IoU .75 {generation['iou_0_75_recall']:.2%} | "
                f"gen failures {generation['generation_failures']} | "
                f"rank failures {generation['ranking_failures']} | "
                f"localization {generation['localization_failures']} | "
                f"internal {generation['internal_region_failures']}",
                (295, 472), 880, ACCENT, self.small,
            )
            self.fitted_text(
                f"Models: geometry held-out accuracy "
                f"{models['geometry_baseline']['accuracy']:.2%}"
                if models["geometry_baseline"]["accuracy"] is not None
                else "Models: grouped holdout unavailable; Logistic Regression and Random Forest not installed.",
                (295, 490), 880, WARNING, self.small,
            )
        self.text("Feature means: correct vs incorrect", (295, 510), TEXT)
        y = 538
        for feature, values in list(summary["features"].items())[:6]:
            correct = "-" if values["correct_mean"] is None else f"{values['correct_mean']:.3f}"
            incorrect = "-" if values["incorrect_mean"] is None else f"{values['incorrect_mean']:.3f}"
            self.fitted_text(
                f"{feature}: {correct} vs {incorrect}", (295, y), 500, TEXT, self.small
            )
            y += 24
        self.text("Recent annotations", (760, 510), TEXT)
        for index, row in enumerate(rows[:6]):
            self.fitted_text(
                f"session {row['session_id']}  candidate #{row['candidate_id']}  "
                f"{row['judgment'] or 'unreviewed'}  {row['detection_method']}",
                (760, 538 + index * 26), 450, TEXT, self.small,
            )

    def phase1_evaluation(self) -> None:
        import cv2
        pygame.draw.rect(self.screen, PANEL, (270, 90, 970, 610), border_radius=8)
        self.text("Phase 1 Evaluation", (295, 112), TEXT, self.title)
        self.button("Run dataset audit", pygame.Rect(985, 112, 220, 32), "audit:phase1")
        report = self.phase1_audit
        if not report:
            self.text("Run the audit to inspect generation and ranking evidence.", (295, 180), WARNING)
            self.text("No labels, images, or detector settings are changed.", (295, 215), MUTED, self.small)
            return
        audit = report["audit"]
        generation = report["generation"]
        self.fitted_text(
            f"{audit['total']} samples | decoded {audit['decoded_images']} | "
            f"CORRECT {audit['correct']} | INCORRECT {audit['incorrect']} | UNSURE {audit['unsure']}",
            (295, 155), 880, TEXT, self.small,
        )
        self.fitted_text(
            f"IoU .50 {generation['iou_0_5_recall']:.2%} | "
            f"IoU .75 {generation['iou_0_75_recall']:.2%} | "
            f"corner error {generation['mean_corner_error']:.4f} | "
            f"internal frequency {generation['internal_candidate_frequency']:.2%}",
            (295, 178), 880, ACCENT, self.small,
        )
        cases = [
            case for case in generation["cases"]
            if case["failure"] or case["internal_candidates"]
        ] or generation["cases"]
        self.phase1_inspection_index = max(
            0, min(self.phase1_inspection_index, len(cases) - 1)
        )
        case = cases[self.phase1_inspection_index]
        self.button("PREVIOUS", pygame.Rect(295, 205, 100, 30), "evaluation:previous")
        self.button("NEXT", pygame.Rect(405, 205, 100, 30), "evaluation:next")
        self.text(
            f"Case {self.phase1_inspection_index + 1} of {len(cases)} | "
            f"record #{case['id']} | {case['failure'] or 'internal candidate present'}",
            (530, 213), WARNING, self.small,
        )
        image = cv2.imread(case["frame_path"])
        if image is not None:
            overlay = image.copy()
            self._draw_evaluation_polygon(overlay, case["ground_truth_points"], (70, 220, 90))
            if case["best_candidate_points"]:
                self._draw_evaluation_polygon(overlay, case["best_candidate_points"], (60, 80, 235))
            if case["top_candidate_points"]:
                self._draw_evaluation_polygon(overlay, case["top_candidate_points"], (235, 160, 50))
            for internal in case["internal_candidates"]:
                self._draw_evaluation_polygon(overlay, internal["points"], (205, 80, 220))
            self.screen.blit(self._fit_preview(image, (400, 300)), (295, 255))
            self.screen.blit(self._fit_preview(overlay, (400, 300)), (715, 255))
        self.text("ORIGINAL", (295, 560), MUTED, self.small)
        self.text("OVERLAY: green ground truth / blue best / orange top / purple internal", (715, 560), MUTED, self.small)
        self.fitted_text(
            f"IoU {case['best_iou']:.3f} | corner error {case['best_corner_error']:.4f} | "
            f"top-rank IoU {case['top_rank_iou']:.3f} | candidates {case['candidate_count']}",
            (295, 585), 880, TEXT, self.small,
        )
        self.fitted_text(
            f"Exact duplicate groups: {audit.get('exact_duplicate_groups', [])} | "
            f"Questionable IDs: {[item['id'] for item in audit['questionable']]}",
            (295, 615), 880, WARNING, self.small,
        )
        self.fitted_text(
            f"Session groups: {len(generation['session_breakdown'])} | "
            f"generation failures {generation['generation_failures']} | "
            f"ranking failures {generation['ranking_failures']} | "
            f"localization failures {generation['localization_failures']} | "
            f"internal failures {generation['internal_region_failures']}",
            (295, 645), 880, ACCENT, self.small,
        )
        session_text = " | ".join(
            f"{session[:6]}:{values['total']}/{values['generation_failures']}gf"
            for session, values in generation["session_breakdown"].items()
        )
        self.fitted_text(
            f"Per-session total/generation-failures: {session_text}",
            (715, 585), 490, MUTED, self.small,
        )
        self.fitted_text(
            f"Top metrics: confidence {case['top_candidate_metrics'].get('confidence', 0):.3f} | "
            f"edge support {case['top_candidate_metrics'].get('edge_support', 0):.3f}",
            (715, 615), 490, TEXT, self.small,
        )

    def _draw_evaluation_polygon(self, image, points, color) -> None:
        import cv2
        import numpy as np
        cv2.polylines(image, [np.int32(points)], True, color, 3)
    def materials(self) -> None:
        pygame.draw.rect(self.screen, PANEL, (270, 90, 710, 470), border_radius=8)
        self.text("Import without modifying production assets", (295, 115), TEXT)
        self.button("Import file...", pygame.Rect(295, 155, 150, 40), "import")
        self.button("Import folder...", pygame.Rect(455, 155, 160, 40), "import_folder")
        rows = self.store.materials()
        self.text(f"{len(rows)} imported material(s)", (295, 225), ACCENT)
        for index, row in enumerate(rows[:10]):
            self.text(f"{row['phase']} | {row['kind']} | {Path(row['path']).name}",
                      (295, 260 + index * 25), TEXT, self.small)

    def dataset(self) -> None:
        rows = self.store.observations()
        pygame.draw.rect(self.screen, PANEL, (270, 90, 710, 470), border_radius=8)
        self.text("Human verification dataset", (295, 115), TEXT)
        self.text("Only records marked correct are suitable as verified samples.", (295, 155), MUTED)
        for index, row in enumerate(rows[:14]):
            self.text(f"{row['phase']} | {row['verification']} | {row['prediction'] or '-'}",
                      (295, 200 + index * 25), TEXT, self.small)

    def experiments(self) -> None:
        rows = self.store.experiments()
        pygame.draw.rect(self.screen, PANEL, (270, 90, 710, 470), border_radius=8)
        self.text("Versioned experimental configurations", (295, 115), TEXT)
        self.text("Experiments are metadata only until a real dataset is evaluated.", (295, 155), WARNING)
        for index, row in enumerate(rows[:14]):
            self.text(f"{row['phase']} | {row['name']} v{row['version']}",
                      (295, 200 + index * 25), TEXT, self.small)

    def reports(self) -> None:
        pygame.draw.rect(self.screen, PANEL, (270, 90, 710, 470), border_radius=8)
        self.text("Reports", (295, 115), TEXT)
        self.text("Export human-verified CSV and JSON reports.", (295, 155), MUTED)
        y = 205
        for phase in ("phase1", "phase2", "phase3"):
            self.button(f"Export {phase}", pygame.Rect(295, y, 180, 40), f"report:{phase}")
            y += 58

    def settings(self) -> None:
        pygame.draw.rect(self.screen, PANEL, (270, 90, 970, 610), border_radius=8)
        self.text("Settings", (295, 115), TEXT)
        self.text("Camera device", (295, 175), MUTED)
        self.text(str(self.camera_device), (450, 175), TEXT)
        self.text(f"Database: {self.store.path}", (295, 225), MUTED, self.small)
        self.text("Phase 1 detection controls", (295, 275), TEXT)
        controls = [
            ("Max candidates", "max_candidates", str(self.boundary_settings["max_candidates"])),
            ("Match threshold", "match_threshold", f"{self.boundary_settings['match_threshold']:.2f}"),
            ("Grace seconds", "grace_seconds", f"{self.boundary_settings['grace_seconds']:.2f}"),
            ("Smoothing", "smoothing", f"{self.boundary_settings['smoothing']:.2f}"),
            ("Detection frequency", "detection_frequency", str(self.boundary_detection_frequency)),
            ("Min aspect ratio", "min_aspect_ratio", f"{self.boundary_settings['min_aspect_ratio']:.2f}"),
            ("Max perspective", "max_perspective_distortion", f"{self.boundary_settings['max_perspective_distortion']:.2f}"),
        ]
        y = 315
        for label, key, value in controls:
            self.text(f"{label}: {value}", (295, y + 8), TEXT, self.small)
            self.button("-", pygame.Rect(550, y, 35, 30), f"setting:{key}:-")
            self.button("+", pygame.Rect(590, y, 35, 30), f"setting:{key}:+")
            y += 38
        self.text("Apply changed tracker settings with Reset tracker.", (295, 595), MUTED, self.small)

    def import_path(self, path: Path, phase: str = "phase2") -> None:
        try:
            target = self.store.import_file(path, phase, "reference")
            self.last_frame = read_image(target)
            self.message = f"Imported {target.name}"
        except (OSError, ValueError) as error:
            self.message = f"Import failed: {error}"

    def choose_file(self) -> None:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title="Import Recognition Lab image",
            filetypes=[("Images", " ".join(f"*{suffix}" for suffix in sorted(IMAGE_SUFFIXES)))],
        )
        root.destroy()
        if path:
            phase = self.phase_pages.get(self.page, "phase2")
            self.import_path(Path(path), phase)

    def choose_folder(self) -> None:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory(title="Import Recognition Lab image folder")
        root.destroy()
        if not folder:
            return
        phase = self.phase_pages.get(self.page, "phase2")
        imported = 0
        for path in sorted(Path(folder).iterdir()):
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
                try:
                    self.import_path(path, phase)
                    imported += 1
                except OSError:
                    continue
        self.message = f"Imported {imported} image(s) from {Path(folder).name}."

    def handle(self, action: str) -> None:
        if action in {"Dashboard", *self.phase_pages, "Materials & Database",
                      "Phase 1 Evaluation",
                      "Boundary Analysis", "Dataset Manager", "Experiments & Models",
                      "Reports & Evaluation", "Settings"}:
            self.page = action
            return
        if action == "camera":
            import cv2
            self.camera = None
            for backend_name, backend in (
                ("DirectShow", cv2.CAP_DSHOW),
                ("default", cv2.CAP_ANY),
            ):
                capture = cv2.VideoCapture(self.camera_device, backend)
                if capture.isOpened():
                    self.camera = capture
                    self.camera_backend = backend_name
                    break
                capture.release()
            if self.camera is None:
                self.camera = None
                self.camera_backend = "unavailable"
                self.message = "Camera unavailable. Use Import image for offline testing."
            else:
                self.running_camera = True
                self.camera_read_failures = 0
                self.message = f"Camera started ({self.camera_backend})."
            return
        if action == "stop_camera":
            self.running_camera = False
            if self.camera is not None:
                self.camera.release()
                self.camera = None
            self.camera_backend = "unopened"
            self.camera_read_failures = 0
            self.message = "Camera stopped."
            return
        if action == "import":
            self.choose_file()
            return
        if action == "import_folder":
            self.choose_folder()
            return
        if action.startswith("report:"):
            phase = action.split(":", 1)[1]
            json_path, csv_path = export_report(self.store.observations(phase), phase)
            self.message = f"Exported {json_path.name} and {csv_path.name}"
            return
        if action == "export_candidates":
            json_path, csv_path = export_candidate_annotations(
                self.store.candidate_annotations()
            )
            self.message = f"Exported {json_path.name} and {csv_path.name}"
            return
        if action == "benchmark:boundary":
            rows = self.store.candidate_annotations()
            profile = build_outer_profile(rows)
            settings = {
                key: self.boundary_settings[key]
                for key in (
                    "max_candidates", "min_area_ratio", "max_area_ratio",
                    "min_aspect_ratio", "max_aspect_ratio",
                    "max_perspective_distortion", "min_edge_support",
                )
            }
            self.boundary_benchmark = benchmark_annotations(
                rows,
                lambda image, **kwargs: detect_boundary_candidates(
                    image,
                    outer_profile=profile if kwargs.get("rank_candidates", True) else None,
                    max_candidates=kwargs.pop("max_candidates", settings["max_candidates"]),
                    **{key: value for key, value in settings.items() if key != "max_candidates"},
                    **kwargs
                ),
            )
            self.store.set_setting("boundary_benchmark", json.dumps(self.boundary_benchmark))
            self.store.set_setting(
                "boundary_benchmark_annotation_count",
                str(len(rows)),
            )
            self.message = (
                f"Benchmarked {self.boundary_benchmark['references']} saved CORRECT references."
            )
            return
        if action == "audit:phase1":
            rows = self.store.candidate_annotations()
            settings = {
                key: self.boundary_settings[key]
                for key in (
                    "max_candidates", "min_area_ratio", "max_area_ratio",
                    "min_aspect_ratio", "max_aspect_ratio",
                    "max_perspective_distortion", "min_edge_support",
                )
            }
            detect_fn = lambda image, **kwargs: detect_boundary_candidates(
                image,
                outer_profile=None,
                max_candidates=kwargs.pop("max_candidates", 1000),
                **{key: value for key, value in settings.items() if key != "max_candidates"},
                **kwargs
            )
            self.phase1_audit = {
                "audit": audit_annotations(rows),
                "generation": evaluate_candidate_generation(rows, detect_fn),
                "models": compare_experimental_models(rows),
            }
            export_phase1_audit_visuals(self.phase1_audit)
            path = export_phase1_audit(self.phase1_audit)
            self.message = f"Phase 1 audit complete: {path.name}"
            return
        if action.startswith("evaluation:"):
            if self.phase1_audit is None:
                self.message = "Run the dataset audit before inspecting evaluation cases."
                return
            cases = [
                case for case in self.phase1_audit["generation"]["cases"]
                if case["failure"] or case["internal_candidates"]
            ] or self.phase1_audit["generation"]["cases"]
            if action.endswith("previous"):
                self.phase1_inspection_index = max(0, self.phase1_inspection_index - 1)
            else:
                self.phase1_inspection_index = min(
                    len(cases) - 1, self.phase1_inspection_index + 1
                )
            return
        if action == "reset_boundary":
            self.boundary_tracker = CandidateTracker(
                max_candidates=self.boundary_settings["max_candidates"],
                match_threshold=self.boundary_settings["match_threshold"],
                grace_seconds=self.boundary_settings["grace_seconds"],
                smoothing=self.boundary_settings["smoothing"],
            )
            self.boundary_candidates = []
            self.session_id = uuid.uuid4().hex[:12]
            self.boundary_benchmark = None
            self.message = f"Started new Phase 1 session {self.session_id}."
            return
        if action.startswith("mode:"):
            self.review_mode = action.split(":", 1)[1]
            self.message = f"Switched to {self.review_mode} mode; session and queue preserved."
            return
        if action == "clear_queue":
            if not self.review_clear_pending:
                self.review_clear_pending = True
                self.message = "Press Clear queue again to confirm; saved annotations are preserved."
                return
            self.review_queue.clear()
            self.review_index = 0
            self.review_clear_pending = False
            self.message = "Review queue cleared. Saved annotations remain available in Analysis."
            return
        if action.startswith("review:"):
            command = action.split(":", 1)[1]
            item = self._review_item()
            if command in {"correct", "incorrect", "unsure"}:
                score = item["metrics"].get("outer_reference_score") if item else None
                if command == "correct" and item is not None and item["metrics"].get("likely_internal_region"):
                    self.message = "Likely internal regions cannot be marked CORRECT."
                elif command == "correct" and score is not None and score < 0.35:
                    self.message = "Candidate has insufficient outer-card reference support."
                else:
                    self._save_review_judgment(command)
            elif command == "previous":
                self.review_index = max(0, self.review_index - 1)
            elif command == "next":
                if item is None or item.get("judgment") is None:
                    self.message = "Submit CORRECT, INCORRECT, or UNSURE before continuing."
                elif self.review_index + 1 < len(self.review_queue):
                    self.review_index += 1
                else:
                    self.message = "All currently queued candidates have been reviewed."
            return
        if action.startswith("diagnostic:"):
            self.diagnostic_selected_id = int(action.split(":", 1)[1])
            return
        if action.startswith("setting:"):
            _, key, direction = action.split(":", 2)
            delta = 1 if direction == "+" else -1
            if key == "max_candidates":
                self.boundary_settings[key] = max(1, min(24, self.boundary_settings[key] + delta))
            elif key == "match_threshold":
                self.boundary_settings[key] = round(max(0.05, min(1.0, self.boundary_settings[key] + delta * 0.05)), 2)
            elif key == "grace_seconds":
                self.boundary_settings[key] = round(max(0.05, min(5.0, self.boundary_settings[key] + delta * 0.25)), 2)
            elif key == "smoothing":
                self.boundary_settings[key] = round(max(0.0, min(0.9, self.boundary_settings[key] + delta * 0.05)), 2)
            elif key == "detection_frequency":
                self.boundary_detection_frequency = max(1, min(10, self.boundary_detection_frequency + delta))
            elif key == "min_aspect_ratio":
                self.boundary_settings[key] = round(max(0.30, min(0.80, self.boundary_settings[key] + delta * 0.05)), 2)
            elif key == "max_perspective_distortion":
                self.boundary_settings[key] = round(max(0.10, min(0.80, self.boundary_settings[key] + delta * 0.05)), 2)
            self.message = f"Changed {key}; reset the Phase 1 session to apply tracker settings."
            return
        if action.startswith("candidate:"):
            _, raw_id, judgment = action.split(":", 2)
            self.save_candidate_judgment(int(raw_id), judgment)
            return
        if action.startswith("save_"):
            verification = action.removeprefix("save_")
            phase = self.phase_pages.get(self.page)
            if phase and self.last_frame is not None:
                output = EXPORTS / "observations"
                output.mkdir(parents=True, exist_ok=True)
                path = output / f"{phase}_{pygame.time.get_ticks()}.png"
                pygame.image.save(pygame.surfarray.make_surface(
                    self.last_frame[:, :, ::-1].swapaxes(0, 1)), path)
                self.store.add_observation(phase, str(path), None, None, verification, {})
                self.message = f"Saved {verification} observation."

    def run(self) -> None:
        clock = pygame.time.Clock()
        active = True
        while active:
            dt = clock.tick(30) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    for rect, action in self.buttons:
                        if rect.collidepoint(event.pos):
                            self.handle(action)
            if self.running_camera and self.camera is not None:
                ok, frame = self.camera.read()
                if ok and frame is not None and frame.size:
                    self.last_frame = frame
                    self.camera_read_failures = 0
                else:
                    self.camera_read_failures += 1
                    if self.camera_read_failures >= 5:
                        self.camera.release()
                        self.camera = None
                        self.running_camera = False
                        self.camera_backend = "unavailable"
                        self.message = (
                            "Camera stopped: no frames received. Check camera permissions "
                            "or use Import image."
                        )
            if self.page in self.phase_pages and self.phase_pages[self.page] == "phase1":
                self.update_boundary(dt)
            self.draw()
            pygame.display.flip()
        self.handle("stop_camera")
        self.store.close()
        pygame.quit()


def main() -> None:
    pygame.init()
    RecognitionLab().run()


if __name__ == "__main__":
    main()
