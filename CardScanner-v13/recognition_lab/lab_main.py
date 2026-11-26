"""Launch the standalone HarvestHand Recognition Lab."""

from __future__ import annotations

import sys
import json
import time
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pygame

from recognition_lab.analysis import (
    audit_annotations,
    benchmark_annotations,
    build_outer_profile,
    compare_detector_variants,
    compare_experimental_models,
    evaluate_candidate_generation,
    evaluate_centroid_ranker,
    feature_summary,
)
from recognition_lab.camera_capture import CameraCapture, CameraConfig, RESOLUTIONS
from recognition_lab.boundary_reference_pipeline_diagnostics import (
    DIAGNOSTIC_REPORT,
    export_pipeline_diagnostics,
    run_pipeline_diagnostics,
)
from recognition_lab.boundary_reference_analysis import (
    REFERENCE_REPORT,
    evaluate_boundary_references,
    export_boundary_reference_report,
)
from recognition_lab.boundary_references import (
    CONDITIONS,
    CONDITION_LABELS,
    list_references,
    save_reference,
    validate_annotation,
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
from recognition_lab.recognition_testing import (
    RECOGNITION_REPORT,
    export_recognition_report,
    recognize_camera_frame,
    run_recognition_test,
)
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
        self.camera_device = 0
        self.camera_config = CameraConfig()
        self.camera_capture = CameraCapture(self.camera_config)
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
        self.live_outer_profile = self._build_live_outer_profile()
        self.phase1_audit = self._load_phase1_audit()
        self.phase1_inspection_index = 0
        self.reference_condition = CONDITIONS[0][0]
        self.reference_view = "capture"
        self.reference_frame = None
        self.reference_points = []
        self.reference_drag_index = None
        self.reference_visibility = "fully_visible"
        self.reference_notes = ""
        self.reference_selected_id = None
        self.reference_save_pending = False
        self.reference_records = list_references()
        self.reference_preview_rect = pygame.Rect(295, 230, 650, 430)
        self.boundary_reference_audit = self._load_boundary_reference_audit()
        self.pipeline_diagnostics = self._load_pipeline_diagnostics()
        self.recognition_test = self._load_recognition_test()
        self.background_executor = ThreadPoolExecutor(max_workers=1)
        self.background_future: Future | None = None
        self.background_job = ""
        self.background_job_kind = ""
        self.boundary_detection_executor = ThreadPoolExecutor(max_workers=1)
        self.boundary_detection_future: Future | None = None
        self.recognition_future: Future | None = None
        self.recognition_result: dict | None = None
        self.recognition_frame = None
        self.recognition_feedback = ""
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

    def _load_recognition_test(self) -> dict | None:
        if not RECOGNITION_REPORT.exists():
            return None
        try:
            value = json.loads(RECOGNITION_REPORT.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def _load_pipeline_diagnostics(self) -> dict | None:
        if not DIAGNOSTIC_REPORT.exists():
            return None
        try:
            value = json.loads(DIAGNOSTIC_REPORT.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def _invalidate_boundary_benchmark(self) -> None:
        self.boundary_benchmark = None
        self.store.set_setting("boundary_benchmark", "")
        self.store.set_setting("boundary_benchmark_annotation_count", "")
        self.live_outer_profile = self._build_live_outer_profile()

    def _build_live_outer_profile(self) -> dict | None:
        rows = self.store.candidate_annotations()
        correct_count = sum(row["judgment"] == "correct" for row in rows)
        if correct_count < 3:
            return None
        return build_outer_profile(rows)

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
        if "comparison" not in value:
            return None
        return value

    def _load_boundary_reference_audit(self) -> dict | None:
        if not REFERENCE_REPORT.exists():
            return None
        try:
            value = json.loads(REFERENCE_REPORT.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

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
            ("Boundary References", "Boundary Reference Capture"),
            ("Camera Diagnostics", "Camera Diagnostics"),
            ("Recognition Testing", "Recognition Testing"),
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
        if self.background_future is not None and not self.background_future.done():
            self.text(f"Running {self.background_job} in background...", (760, HEIGHT - 36), ACCENT, self.small)
        self.text(self.page, (270, 28), TEXT, self.title)
        if self.page == "Dashboard":
            self.dashboard()
        elif self.page in self.phase_pages:
            self.phase(self.phase_pages[self.page])
        elif self.page == "Phase 1 Evaluation":
            self.phase1_evaluation()
        elif self.page == "Boundary Reference Capture":
            self.boundary_references()
        elif self.page == "Camera Diagnostics":
            self.camera_diagnostics()
        elif self.page == "Recognition Testing":
            self.recognition_testing()
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
        import cv2

        height, width = image.shape[:2]
        scale = min(size[0] / width, size[1] / height)
        fitted_size = (
            max(1, int(width * scale)),
            max(1, int(height * scale)),
        )
        fitted_image = cv2.resize(image, fitted_size, interpolation=cv2.INTER_AREA)
        fitted = pygame.surfarray.make_surface(
            fitted_image[:, :, ::-1].swapaxes(0, 1)
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
        self.fitted_text(
            f"frames {self.boundary_frames} | candidates/frame {self.boundary_detected_total}/"
            f"{max(self.boundary_frames, 1)} | detection frequency {self.boundary_detection_frequency} | "
            f"last detection {self.boundary_last_detection_ms:.0f} ms | "
            f"card profile {'active' if self.live_outer_profile else 'inactive'}",
            (295, 655), 610, MUTED, self.small,
        )

    @staticmethod
    def _run_boundary_detection(
        frame, profile: dict | None, detection_settings: dict,
    ) -> tuple[list[dict], float]:
        started = time.perf_counter()
        detections = detect_boundary_candidates(
            frame, outer_profile=profile, **detection_settings
        )
        return detections, (time.perf_counter() - started) * 1000.0

    def update_boundary(self, dt: float, collect_review: bool = True) -> None:
        if self.last_frame is None:
            self.boundary_candidates = []
            return
        self.boundary_frame_number += 1
        detect_now = self.boundary_frame_number % self.boundary_detection_frequency == 0
        detections = []
        detection_completed = False
        if self.boundary_detection_future is not None and self.boundary_detection_future.done():
            future = self.boundary_detection_future
            self.boundary_detection_future = None
            try:
                detections, elapsed_ms = future.result()
            except Exception as error:
                self.message = f"Boundary detection failed: {error}"
            else:
                self.boundary_last_detection_ms = elapsed_ms
                self.boundary_frames += 1
                self.boundary_detected_total += len(detections)
                detection_completed = True
        if detect_now and self.boundary_detection_future is None:
            detection_settings = {
                key: self.boundary_settings[key]
                for key in (
                    "max_candidates", "min_area_ratio", "max_area_ratio",
                    "min_aspect_ratio", "max_aspect_ratio",
                    "max_perspective_distortion", "min_edge_support",
                )
            }
            profile = self.live_outer_profile
            self.boundary_detection_future = self.boundary_detection_executor.submit(
                self._run_boundary_detection,
                self.last_frame,
                profile,
                detection_settings,
            )
        self.boundary_candidates = self.boundary_tracker.update(
            detections, dt, detected=detection_completed
        )
        for candidate in self.boundary_candidates:
            candidate["judgment"] = self.store.candidate_judgment(
                self.session_id, candidate["id"]
            ) or candidate.get("judgment")
            if collect_review:
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
        comparison = report["comparison"]
        baseline = comparison["baseline"]
        experimental = comparison["experimental"]
        self.fitted_text(
            f"Positive IoU .50 baseline/experimental: "
            f"{baseline['positive']['iou_0_5_recall']:.2%} / "
            f"{experimental['positive']['iou_0_5_recall']:.2%} | "
            f"IoU .75: {baseline['positive']['iou_0_75_recall']:.2%} / "
            f"{experimental['positive']['iou_0_75_recall']:.2%}",
            (295, 235), 880, ACCENT, self.small,
        )
        self.fitted_text(
            f"Incorrect false acceptance: "
            f"{baseline['incorrect']['false_acceptance_rate']:.2%} / "
            f"{experimental['incorrect']['false_acceptance_rate']:.2%} | "
            f"rejected: {experimental['incorrect']['rejected']}/"
            f"{experimental['incorrect']['total']}",
            (295, 255), 880, ACCENT, self.small,
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
            self.screen.blit(self._fit_preview(image, (400, 280)), (295, 275))
            self.screen.blit(self._fit_preview(overlay, (400, 280)), (715, 275))
        self.text("ORIGINAL", (295, 560), MUTED, self.small)
        self.text("OVERLAY: green ground truth / blue best / orange top / purple internal", (715, 560), MUTED, self.small)
        self.fitted_text(
            f"IoU {case['best_iou']:.3f} | corner error {case['best_corner_error']:.4f} | "
            f"top-rank IoU {case['top_rank_iou']:.3f} | candidates {case['candidate_count']} | "
            f"{case.get('processing_time_ms', 0):.1f} ms",
            (295, 585), 400, TEXT, self.small,
        )
        self.fitted_text(
            f"Top metrics: confidence {case['top_candidate_metrics'].get('confidence', 0):.3f} | "
            f"edge support {case['top_candidate_metrics'].get('edge_support', 0):.3f}",
            (715, 585), 490, TEXT, self.small,
        )
        self.fitted_text(
            f"Duplicate groups: {len(audit.get('exact_duplicate_groups', []))} | "
            f"questionable samples: {len(audit['questionable'])}",
            (295, 615), 400, WARNING, self.small,
        )
        self.fitted_text(
            f"Sessions: {len(generation['session_breakdown'])} | "
            f"generation failures: {generation['generation_failures']}",
            (715, 615), 490, MUTED, self.small,
        )
        self.fitted_text(
            f"Ranking failures: {generation['ranking_failures']} | "
            f"localization: {generation['localization_failures']} | "
            f"internal: {generation['internal_region_failures']}",
            (295, 645), 400, ACCENT, self.small,
        )
        self.fitted_text(
            f"Incorrect accepted: {experimental['incorrect']['accepted']}/"
            f"{experimental['incorrect']['total']} | internal accepted: "
            f"{experimental['incorrect']['internal_region_accepted']}",
            (715, 645), 490, WARNING, self.small,
        )
        changes = comparison.get("incorrect_changes", {})
        self.fitted_text(
            f"New rejections: {len(changes.get('new_correct_rejections', []))} | "
            f"new false accepts: {len(changes.get('new_false_acceptances', []))}",
            (295, 675), 400, WARNING, self.small,
        )
        self.fitted_text(
            f"Mean time baseline/experimental: "
            f"{baseline['positive'].get('mean_processing_time_ms', 0):.1f}/"
            f"{experimental['positive'].get('mean_processing_time_ms', 0):.1f} ms",
            (715, 675), 490, WARNING, self.small,
        )

    def _reference_display_geometry(self, image) -> tuple[pygame.Rect, float, tuple[int, int]]:
        surface_width, surface_height = image.shape[1], image.shape[0]
        scale = min(
            self.reference_preview_rect.width / surface_width,
            self.reference_preview_rect.height / surface_height,
        )
        display_size = (
            max(1, int(surface_width * scale)),
            max(1, int(surface_height * scale)),
        )
        origin = (
            self.reference_preview_rect.x
            + (self.reference_preview_rect.width - display_size[0]) // 2,
            self.reference_preview_rect.y
            + (self.reference_preview_rect.height - display_size[1]) // 2,
        )
        return pygame.Rect(*origin, *display_size), scale, origin

    def _reference_image_point(self, position: tuple[int, int]) -> tuple[float, float] | None:
        if self.reference_frame is None:
            return None
        display, scale, origin = self._reference_display_geometry(self.reference_frame)
        if not display.collidepoint(position):
            return None
        x = (position[0] - origin[0]) / scale
        y = (position[1] - origin[1]) / scale
        return (
            max(0.0, min(float(self.reference_frame.shape[1] - 1), x)),
            max(0.0, min(float(self.reference_frame.shape[0] - 1), y)),
        )

    def _reference_point_screen(self, point: list[float]) -> tuple[int, int]:
        _, scale, origin = self._reference_display_geometry(self.reference_frame)
        return (
            int(origin[0] + point[0] * scale),
            int(origin[1] + point[1] * scale),
        )

    def _draw_reference_overlay(self) -> None:
        import cv2
        import numpy as np

        image = self.reference_frame.copy()
        if len(self.reference_points) >= 2:
            cv2.polylines(
                image, [np.int32(self.reference_points)], len(self.reference_points) == 4,
                (70, 220, 130), 3,
            )
        display, _, _ = self._reference_display_geometry(image)
        self.screen.blit(self._fit_preview(image, self.reference_preview_rect.size),
                         self.reference_preview_rect.topleft)
        for index, point in enumerate(self.reference_points):
            x, y = self._reference_point_screen(point)
            pygame.draw.circle(self.screen, ACCENT, (x, y), 9)
            pygame.draw.circle(self.screen, BG, (x, y), 4)
            self.text(str(index + 1), (x + 11, y - 10), TEXT, self.small)
        if len(self.reference_points) == 4:
            self.text("TL  1   TR  2   BR  3   BL  4", (295, 670), ACCENT, self.small)

    def boundary_references(self) -> None:
        pygame.draw.rect(self.screen, PANEL, (270, 90, 970, 610), border_radius=8)
        self.text("Boundary Reference Capture", (295, 112), TEXT, self.title)
        self.fitted_text(
            "Human-annotated physical outer-card references. Detector candidates are not used.",
            (295, 153), 900, MUTED, self.small,
        )
        self.button("CAPTURE", pygame.Rect(295, 180, 110, 32), "reference:capture",
                    self.reference_view == "capture")
        self.button("COLLECTION", pygame.Rect(415, 180, 125, 32), "reference:collection",
                    self.reference_view == "collection")
        self.button("AUDIT DETECTOR", pygame.Rect(555, 180, 145, 32), "reference:audit")
        self.button("PIPELINE DIAGNOSTICS", pygame.Rect(710, 180, 190, 32),
                    "reference:pipeline")
        if self.reference_view == "annotate":
            self._draw_reference_annotation()
        elif self.reference_view == "collection":
            self._draw_reference_collection()
        else:
            self._draw_reference_capture()
    def _draw_reference_capture(self) -> None:
        self.text(f"Condition: {CONDITION_LABELS[self.reference_condition]}",
                  (295, 235), ACCENT, self.font)
        for index, (condition, label) in enumerate(CONDITIONS):
            self.button(label, pygame.Rect(295 + (index % 2) * 190, 275 + (index // 2) * 44,
                                           175, 34), f"reference:condition:{condition}",
                        condition == self.reference_condition)
        self.button("Open camera", pygame.Rect(700, 275, 145, 34), "camera")
        self.button("Import image", pygame.Rect(855, 275, 145, 34), "reference:import")
        self.button("Capture current frame", pygame.Rect(700, 320, 300, 38), "reference:capture_frame")
        if self.last_frame is not None:
            self.screen.blit(self._fit_preview(self.last_frame, (650, 310)), (295, 385))
            self.text(
                "Camera frames update live; capture freezes the current frame for annotation.",
                (295, 670), MUTED, self.small,
            )
        else:
            self.text("Open the camera or import an image to begin.", (295, 430), WARNING)

    def _draw_reference_annotation(self) -> None:
        self.text(
            f"{CONDITION_LABELS[self.reference_condition]} | click corners in order: "
            "Top-left, Top-right, Bottom-right, Bottom-left",
            (295, 205), ACCENT, self.small,
        )
        if self.reference_frame is not None:
            self._draw_reference_overlay()
        self.button("Reset points", pygame.Rect(975, 230, 120, 34), "reference:reset")
        self.button("Retake", pygame.Rect(1105, 230, 100, 34), "reference:retake")
        self.button("Cancel", pygame.Rect(975, 275, 120, 34), "reference:cancel")
        self.button(
            "Confirm save" if self.reference_save_pending else "Save reference",
            pygame.Rect(1105, 275, 100, 34), "reference:save",
        )
        self.text("Visibility", (975, 340), MUTED, self.small)
        self.button("Fully visible", pygame.Rect(975, 365, 110, 30), "reference:visibility:fully_visible",
                    self.reference_visibility == "fully_visible")
        self.button("Partially obstructed", pygame.Rect(1090, 365, 125, 30), "reference:visibility:partially_obstructed",
                    self.reference_visibility == "partially_obstructed")
        self.fitted_text(
            f"Points: {len(self.reference_points)}/4 | Notes are stored in JSON metadata.",
            (975, 420), 245, TEXT, self.small,
        )
        self.fitted_text(
            f"Notes: {self.reference_notes or '(none)'}",
            (975, 440), 245, MUTED, self.small,
        )
        self.fitted_text(
            "Press S to save, R to reset, or Escape to cancel.",
            (975, 455), 245, MUTED, self.small,
        )
        if len(self.reference_points) == 4 and self.reference_frame is not None:
            valid, reasons = validate_annotation(self.reference_points, self.reference_frame.shape)
            self.fitted_text(
                (
                    "Valid quadrilateral."
                    if valid and not reasons
                    else ("Valid with warning: " + "; ".join(reasons)
                          if valid else "Invalid: " + "; ".join(reasons))
                ),
                (975, 500), 245, ACCENT if valid else WARNING, self.small,
            )

    def _draw_reference_collection(self) -> None:
        self.reference_records = list_references()
        total = len(self.reference_records)
        verified = sum(item.get("manually_verified", False) for item in self.reference_records)
        partial = sum(item.get("visibility_status") == "partially_obstructed" for item in self.reference_records)
        self.fitted_text(
            f"Total {total} | verified {verified} | needs review {total - verified} | "
            f"fully visible {total - partial} | partially obstructed {partial}",
            (295, 210), 900, ACCENT, self.small,
        )
        counts = {
            condition: sum(item.get("capture_condition") == condition for item in self.reference_records)
            for condition, _ in CONDITIONS
        }
        self.fitted_text(
            " | ".join(f"{CONDITION_LABELS[key]}: {counts[key]}" for key, _ in CONDITIONS),
            (295, 235), 900, TEXT, self.small,
        )
        for index, record in enumerate(self.reference_records[:12]):
            x = 295 + (index % 4) * 160
            y = 275 + (index // 4) * 130
            image = read_image(record["image_path"]) if Path(record["image_path"]).exists() else None
            if image is not None:
                self.screen.blit(self._fit_preview(image, (145, 95)), (x, y))
            self.button(
                f"{record['sample_id'][-8:]}",
                pygame.Rect(x, y + 98, 145, 25),
                f"reference:select:{record['sample_id']}",
            )
        if not self.reference_records:
            self.text("No references saved yet. Capture a real card to begin.", (295, 300), WARNING)
        if self.boundary_reference_audit:
            positive = self.boundary_reference_audit["positive"]
            negative = self.boundary_reference_audit["negative"]
            self.fitted_text(
                f"Audit: IoU .50 {positive['iou_0_50_recall']:.1%} | "
                f"IoU .75 {positive['iou_0_75_recall']:.1%} | "
                f"valid annotations {self.boundary_reference_audit['annotation_validation']['valid_annotations']}",
                (295, 660), 900, ACCENT, self.small,
            )
            self.fitted_text(
                f"Negative set: {negative['total']} incorrect | "
                f"queued acceptance {negative['false_acceptance_rate']:.1%} | "
                "baseline detector; no final acceptance gate",
                (295, 682), 900, WARNING, self.small,
            )
        else:
            self.text("Select a thumbnail to inspect or correct its annotation.",
                      (295, 660), MUTED, self.small)

    def _select_reference(self, sample_id: str) -> None:
        record = next((item for item in list_references() if item["sample_id"] == sample_id), None)
        if record is None:
            self.message = "Reference sample could not be found."
            return
        try:
            self.reference_frame = read_image(record["image_path"])
        except ValueError as error:
            self.message = str(error)
            return
        self.reference_selected_id = sample_id
        self.reference_condition = record["capture_condition"]
        self.reference_visibility = record.get("visibility_status", "fully_visible")
        self.reference_notes = record.get("notes", "")
        self.reference_points = [list(point) for point in record["corners"]]
        self.reference_view = "annotate"
        self.message = f"Inspecting reference {sample_id}."

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

    def camera_diagnostics(self) -> None:
        pygame.draw.rect(self.screen, PANEL, (270, 90, 970, 610), border_radius=8)
        self.text("Camera Diagnostics", (295, 112), TEXT, self.title)
        self.fitted_text(
            "Latest-frame capture; stale frames are discarded instead of queued.",
            (295, 153), 900, MUTED, self.small,
        )
        self.button("Open / Restart", pygame.Rect(295, 185, 145, 34), "camera")
        self.button("Stop", pygame.Rect(450, 185, 90, 34), "stop_camera")
        self.text("Backend", (295, 245), MUTED, self.small)
        for index, (key, label) in enumerate(
            (("auto", "Auto (MSMF first)"), ("msmf", "Media Foundation"), ("dshow", "DirectShow"))
        ):
            self.button(label, pygame.Rect(295 + index * 190, 270, 175, 32),
                        f"camera:backend:{key}", self.camera_config.backend == key)
        self.text("Resolution", (295, 330), MUTED, self.small)
        for index, resolution in enumerate(RESOLUTIONS):
            label = f"{resolution[0]}x{resolution[1]}"
            self.button(label, pygame.Rect(295 + index * 145, 355, 130, 32),
                        f"camera:resolution:{resolution[0]}:{resolution[1]}",
                        (self.camera_config.width, self.camera_config.height) == resolution)
        self.text("Target FPS", (295, 415), MUTED, self.small)
        for index, fps in enumerate((30, 15)):
            self.button(str(fps), pygame.Rect(295 + index * 90, 440, 75, 32),
                        f"camera:fps:{fps}", self.camera_config.target_fps == fps)
        preview_rect = pygame.Rect(295, 500, 520, 170)
        self.text("Camera preview", preview_rect.topleft, MUTED, self.small)
        preview_area = pygame.Rect(
            preview_rect.x, preview_rect.y + 22,
            preview_rect.width, preview_rect.height - 22,
        )
        pygame.draw.rect(self.screen, (10, 14, 19), preview_area)
        if self.last_frame is not None:
            overlay = self.last_frame.copy()
            for candidate in self.boundary_candidates:
                self._draw_candidate_overlay(overlay, candidate)
            self.screen.blit(
                self._fit_preview(overlay, preview_area.size),
                preview_area.topleft,
            )
            if self.boundary_candidates:
                self.text(
                    f"{len(self.boundary_candidates)} candidate border(s)",
                    (preview_area.x + 12, preview_area.y + 10), ACCENT, self.small,
                )
            else:
                self.text(
                    "No quadrilateral candidate detected yet.",
                    (preview_area.x + 12, preview_area.y + 10), WARNING, self.small,
                )
        else:
            self.text(
                "No frame available. Open the camera to start preview.",
                (preview_area.x + 18, preview_area.y + 64), MUTED, self.small,
            )
        status = self.camera_capture.snapshot()
        actual = (
            f"{status.actual_resolution[0]}x{status.actual_resolution[1]}"
            if status.actual_resolution else "unavailable"
        )
        metrics_x = 875
        metrics_width = 335
        self.text("Measured capture", (metrics_x, 245), TEXT)
        lines = [
            f"Device: {status.device_name}",
            f"Status: {'RUNNING' if status.running else 'STOPPED'}",
            f"Backend: {status.selected_backend} (requested {status.requested_backend})",
            f"Resolution: {actual} (requested {status.requested_resolution[0]}x{status.requested_resolution[1]})",
            f"FPS: measured {status.measured_fps:.2f} | reported {status.reported_fps or 0:.2f} | target {status.requested_fps}",
            f"FOURCC: {status.fourcc or 'unknown'} (requested {status.requested_fourcc})",
            f"Frames: {status.frames_captured} | failed reads: {status.failed_frames}",
            f"Average read: {status.average_read_ms:.2f} ms",
            f"Brightness: {status.brightness:.1f} | contrast: {status.contrast:.1f}",
            f"Indicative sharpness: {status.sharpness:.1f}",
        ]
        for index, line in enumerate(lines):
            self.fitted_text(line, (metrics_x, 280 + index * 26),
                             metrics_width, TEXT, self.small)
        measured = status.measured_fps
        performance = "Excellent" if measured >= 25 else "Acceptable" if measured >= 15 else "Slow"
        color = ACCENT if measured >= 25 else WARNING
        self.text(f"Performance: {performance}", (metrics_x, 555), color)
        if status.initialization_errors:
            self.text("Initialization errors:", (metrics_x, 600), WARNING, self.small)
            for index, error in enumerate(status.initialization_errors[-3:]):
                self.fitted_text(error, (metrics_x, 623 + index * 20),
                                 metrics_width, WARNING, self.small)
        elif status.last_error:
            self.fitted_text(status.last_error, (metrics_x, 600),
                             metrics_width, WARNING, self.small)
        self.text(
            "Measured FPS is based on successful frames, not CAP_PROP_FPS.",
            (295, 680), MUTED, self.small,
        )

    def recognition_testing(self) -> None:
        pygame.draw.rect(self.screen, PANEL, (270, 90, 970, 610), border_radius=8)
        self.text("Recognition Testing", (295, 112), TEXT, self.title)
        self.fitted_text(
            "Show a card to the camera, recognize one frame, then verify the result.",
            (295, 153), 900, MUTED, self.small,
        )
        self.button("Start live test", pygame.Rect(295, 185, 135, 34), "recognition:start")
        self.button("Stop camera", pygame.Rect(440, 185, 110, 34), "stop_camera")
        self.button("Recognize frame", pygame.Rect(560, 185, 155, 34), "recognition:capture")
        self.button("Run offline test", pygame.Rect(725, 185, 140, 34), "recognition:run")
        preview_rect = pygame.Rect(295, 245, 600, 390)
        pygame.draw.rect(self.screen, (10, 14, 19), preview_rect)
        status = self.camera_capture.snapshot()
        camera_status = (
            f"Camera: {status.selected_backend} "
            f"{status.actual_resolution[0]}x{status.actual_resolution[1]}"
            if status.actual_resolution
            else (
                f"Camera: {status.selected_backend}"
                if status.running
                else "Camera: not started"
            )
        )
        self.fitted_text(camera_status, (295, 225), 590, ACCENT, self.small)
        if self.last_frame is not None:
            overlay = self.last_frame.copy()
            result = self.recognition_result
            if result and result.get("points"):
                import cv2
                import numpy as np
                points = np.rint(result["points"]).astype(np.int32)
                cv2.polylines(overlay, [points], True, (70, 220, 130), 4)
            self.screen.blit(self._fit_preview(overlay, preview_rect.size), preview_rect.topleft)
        else:
            self.text("Open the camera to show a live preview.", (330, 420), MUTED, self.small)
        result = self.recognition_result
        if result:
            prediction = result.get("prediction") or "NO CARD MATCH"
            score = result.get("score")
            score_text = f"{score:.2f}" if isinstance(score, (float, int)) else "n/a"
            margin = result.get("margin")
            margin_text = f"{margin:.2f}" if isinstance(margin, (float, int)) else "n/a"
            initial = result.get("initial_prediction")
            candidate_text = (
                f"Top candidate: {initial}" if initial else "Top candidate: none"
            )
            self.fitted_text(
                f"Prediction: {prediction} | score {score_text} | {result.get('message', '')}",
                (295, 650), 930,
                ACCENT if prediction in {
                    "Pechay", "Monggo", "Okra", "Kalabasa",
                    "Kamatis", "Talong", "Kamote", "Palay",
                } else WARNING,
                self.small,
            )
            self.fitted_text(
                f"{candidate_text} | margin {margin_text}",
                (295, 675), 930, MUTED, self.small,
            )
            self.fitted_text(
                f"Engine: {result.get('engine', 'Recognition Lab matcher')}",
                (920, 370), 300, MUTED, self.small,
            )
            self.button("CORRECT", pygame.Rect(920, 265, 120, 38), "recognition:correct")
            self.button("INCORRECT", pygame.Rect(1050, 265, 135, 38), "recognition:incorrect")
            if self.recognition_feedback:
                self.fitted_text(self.recognition_feedback, (920, 320), 300, MUTED, self.small)
        elif self.recognition_future is not None and not self.recognition_future.done():
            self.text("Recognizing captured frame...", (920, 270), ACCENT, self.small)
        else:
            self.fitted_text(
                "Recognition compares against stored Phase 2 references. "
                "Verify every result.",
                (920, 270), 300, MUTED, self.small,
            )
        observations = self.store.observations("phase2")
        self.fitted_text(
            f"Verified camera observations: {len(observations)}",
            (920, 405), 300, TEXT, self.small,
        )
        self.fitted_text(
            "The offline test remains available for transformed-reference smoke testing.",
            (920, 445), 300, WARNING, self.small,
        )

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

    def choose_reference_file(self) -> None:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title="Import boundary reference image",
            filetypes=[("Images", " ".join(f"*{suffix}" for suffix in sorted(IMAGE_SUFFIXES)))],
        )
        root.destroy()
        if not path:
            return
        try:
            self.reference_frame = read_image(Path(path))
            self.reference_points = []
            self.reference_selected_id = None
            self.reference_view = "annotate"
            self.message = f"Loaded {Path(path).name}; annotate the original frame."
        except ValueError as error:
            self.message = f"Reference import failed: {error}"

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

    def _background_job_running(self) -> bool:
        return self.background_future is not None and not self.background_future.done()

    def _start_background_job(self, label: str, work, kind: str) -> None:
        self.background_job = label
        self.background_job_kind = kind
        self.background_future = self.background_executor.submit(work)
        self.message = f"{label.capitalize()} started; the interface remains available."

    def _run_phase1_audit(self, rows, baseline_fn, experimental_fn) -> dict:
        report = {
            "audit": audit_annotations(rows),
            "generation": evaluate_candidate_generation(rows, baseline_fn),
            "comparison": compare_detector_variants(rows, baseline_fn, experimental_fn),
            "models": compare_experimental_models(rows),
        }
        export_phase1_audit_visuals(report)
        export_phase1_audit(report)
        return report

    def _poll_background_job(self) -> None:
        future = self.background_future
        if future is None or not future.done():
            return
        self.background_future = None
        try:
            result = future.result()
        except Exception as error:
            self.message = f"{self.background_job} failed: {error}"
            self.background_job = ""
            self.background_job_kind = ""
            return
        kind = self.background_job_kind
        if kind == "audit":
            self.phase1_audit = result
            self.message = "Phase 1 audit complete: phase1_ground_truth_audit.json"
        elif kind == "reference_audit":
            self.boundary_reference_audit = result
            path = export_boundary_reference_report(result)
            self.message = f"Boundary reference audit complete: {path.name}"
        elif kind == "reference_pipeline":
            self.pipeline_diagnostics = result
            path = export_pipeline_diagnostics(result)
            self.message = f"Pipeline diagnostics complete: {path.name}"
        elif kind == "benchmark":
            self.boundary_benchmark = result
            self.store.set_setting("boundary_benchmark", json.dumps(result))
            self.store.set_setting(
                "boundary_benchmark_annotation_count",
                str(len(self.store.candidate_annotations())),
            )
            self.message = f"Benchmarked {result['references']} saved CORRECT references."
        elif kind == "recognition_test":
            self.recognition_test = result
            path = export_recognition_report(result)
            self.message = f"Recognition test complete: {path.name}"
        self.background_job = ""
        self.background_job_kind = ""

    def _poll_recognition_job(self) -> None:
        future = self.recognition_future
        if future is None or not future.done():
            return
        self.recognition_future = None
        try:
            self.recognition_result = future.result()
            self.recognition_feedback = ""
        except Exception as error:
            self.recognition_result = None
            self.message = f"Recognition failed: {error}"

    def _save_recognition_feedback(self, verification: str) -> None:
        if self.recognition_result is None or self.recognition_frame is None:
            self.message = "Recognize a camera frame before verifying it."
            return
        import cv2

        output_dir = EXPORTS / "recognition_tests"
        output_dir.mkdir(parents=True, exist_ok=True)
        frame_path = output_dir / f"camera_{int(time.time() * 1000)}.png"
        if not cv2.imwrite(str(frame_path), self.recognition_frame):
            self.message = "Could not save the camera observation."
            return
        prediction = self.recognition_result.get("prediction")
        self.store.add_observation(
            "phase2",
            str(frame_path),
            prediction,
            prediction,
            verification,
            self.recognition_result,
        )
        self.recognition_feedback = f"Saved as {verification.lower()}."
        self.message = f"Camera observation saved: {verification.lower()}."

    def handle(self, action: str) -> None:
        if action in {"Dashboard", *self.phase_pages, "Materials & Database",
                      "Phase 1 Evaluation",
                      "Boundary Reference Capture",
                      "Camera Diagnostics",
                      "Recognition Testing",
                      "Boundary Analysis", "Dataset Manager", "Experiments & Models",
                      "Reports & Evaluation", "Settings"}:
            self.page = action
            if action == "Recognition Testing" and not self.running_camera:
                if self.camera_capture.start():
                    self.running_camera = True
                    status = self.camera_capture.snapshot()
                    resolution = (
                        f"{status.actual_resolution[0]}x{status.actual_resolution[1]}"
                        if status.actual_resolution else "awaiting frame"
                    )
                    self.message = (
                        f"Recognition camera started: "
                        f"{status.selected_backend}, {resolution}"
                    )
                else:
                    self.running_camera = False
                    self.message = (
                        "Recognition camera unavailable. "
                        + self.camera_capture.snapshot().last_error
                    )
            return
        if action == "camera":
            if self.camera_capture.start():
                self.running_camera = True
                status = self.camera_capture.snapshot()
                self.message = (
                    f"Camera started: {status.selected_backend}, "
                    f"{status.actual_resolution[0]}x{status.actual_resolution[1]} requested"
                    if status.actual_resolution else
                    f"Camera started: {status.selected_backend}; awaiting first frame."
                )
            else:
                self.running_camera = False
                self.message = (
                    "Camera unavailable. Use Import image for offline testing. "
                    + self.camera_capture.snapshot().last_error
                )
            return
        if action == "recognition:start":
            self.handle("camera")
            return
        if action == "recognition:run":
            if self._background_job_running():
                self.message = f"{self.background_job} is still running."
                return
            self._start_background_job(
                "Pechay/Monggo recognition test",
                lambda: run_recognition_test(self.store.materials("phase2")),
                "recognition_test",
            )
            return
        if action == "recognition:capture":
            if self.recognition_future is not None and not self.recognition_future.done():
                self.message = "Recognition is already running."
                return
            if self.last_frame is None:
                self.message = "Open the camera and wait for a frame first."
                return
            rows = [dict(row) for row in self.store.materials("phase2")]
            if not rows:
                self.message = "No Phase 2 references are available."
                return
            self.recognition_frame = self.last_frame.copy()
            self.recognition_result = None
            self.recognition_feedback = ""
            self.recognition_future = self.background_executor.submit(
                recognize_camera_frame, self.recognition_frame.copy(), rows,
            )
            self.message = "Captured frame; recognizing against Phase 2 references."
            return
        if action == "recognition:correct":
            self._save_recognition_feedback("CORRECT")
            return
        if action == "recognition:incorrect":
            self._save_recognition_feedback("INCORRECT")
            return
        if action == "reference:collection":
            self.reference_view = "collection"
            self.reference_records = list_references()
            return
        if action == "reference:audit":
            if self._background_job_running():
                self.message = f"{self.background_job} is still running."
                return
            rows = self.store.candidate_annotations()
            settings = {
                key: self.boundary_settings[key]
                for key in (
                    "max_candidates", "min_area_ratio", "max_area_ratio",
                    "min_aspect_ratio", "max_aspect_ratio",
                    "max_perspective_distortion", "min_edge_support",
                )
            }
            detector = lambda image, **kwargs: detect_boundary_candidates(
                image,
                max_candidates=kwargs.pop("max_candidates", 1000),
                **{key: value for key, value in settings.items() if key != "max_candidates"},
                **kwargs,
            )
            self._start_background_job(
                "boundary reference audit",
                lambda: evaluate_boundary_references(rows, detector),
                "reference_audit",
            )
            return
        if action == "reference:pipeline":
            if self._background_job_running():
                self.message = f"{self.background_job} is still running."
                return
            rows = self.store.candidate_annotations()
            settings = {
                key: self.boundary_settings[key]
                for key in (
                    "min_area_ratio", "max_area_ratio", "min_aspect_ratio",
                    "max_aspect_ratio", "max_perspective_distortion",
                    "min_edge_support",
                )
            }
            self._start_background_job(
                "boundary pipeline diagnostics",
                lambda: run_pipeline_diagnostics(rows, settings=settings),
                "reference_pipeline",
            )
            return
        if action == "reference:capture":
            self.reference_view = "capture"
            return
        if action == "reference:import":
            self.choose_reference_file()
            return
        if action == "reference:capture_frame":
            if self.last_frame is None:
                self.message = "No current frame. Open the camera or import an image first."
                return
            self.reference_frame = self.last_frame.copy()
            self.reference_points = []
            self.reference_selected_id = None
            self.reference_view = "annotate"
            self.message = "Frame frozen. Mark the four physical outer-card corners."
            return
        if action == "reference:reset":
            self.reference_points = []
            self.reference_drag_index = None
            self.reference_save_pending = False
            self.message = "Reference points reset."
            return
        if action == "reference:retake":
            self.reference_selected_id = None
            self.reference_points = []
            self.reference_save_pending = False
            self.reference_view = "capture"
            self.message = "Ready to capture another frame."
            return
        if action == "reference:cancel":
            self.reference_selected_id = None
            self.reference_points = []
            self.reference_frame = None
            self.reference_view = "capture"
            self.reference_save_pending = False
            self.message = "Annotation cancelled; no reference was saved."
            return
        if action == "reference:save":
            if not self.reference_save_pending:
                if self.reference_frame is None or len(self.reference_points) != 4:
                    self.message = "Select all four corners before requesting save confirmation."
                    return
                valid, reasons = validate_annotation(
                    self.reference_points, self.reference_frame.shape
                )
                if not valid:
                    self.message = "Cannot save invalid polygon: " + "; ".join(reasons)
                    return
                self.reference_save_pending = True
                self.message = "Review the polygon and press Confirm save to preserve it."
            else:
                self._save_boundary_reference()
            return
        if action.startswith("reference:condition:"):
            self.reference_condition = action.rsplit(":", 1)[1]
            self.reference_save_pending = False
            return
        if action.startswith("reference:visibility:"):
            self.reference_visibility = action.rsplit(":", 1)[1]
            self.reference_save_pending = False
            return
        if action.startswith("reference:select:"):
            self._select_reference(action.rsplit(":", 1)[1])
            return
        if action == "stop_camera":
            self.running_camera = False
            self.camera_capture.stop()
            self.message = "Camera stopped."
            return
        if action.startswith("camera:backend:"):
            self.camera_config.backend = action.rsplit(":", 1)[1]
            self.message = "Camera backend changed; restart camera to apply."
            return
        if action.startswith("camera:resolution:"):
            _, _, width, height = action.split(":")
            self.camera_config.width = int(width)
            self.camera_config.height = int(height)
            self.message = "Camera resolution changed; restart camera to apply."
            return
        if action.startswith("camera:fps:"):
            self.camera_config.target_fps = int(action.rsplit(":", 1)[1])
            self.message = "Camera target FPS changed; restart camera to apply."
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
            if self._background_job_running():
                self.message = f"{self.background_job} is still running."
                return
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
            detector = lambda image, **kwargs: detect_boundary_candidates(
                image,
                outer_profile=profile if kwargs.get("rank_candidates", True) else None,
                max_candidates=kwargs.pop("max_candidates", settings["max_candidates"]),
                **{key: value for key, value in settings.items() if key != "max_candidates"},
                **kwargs
            )
            self._start_background_job(
                "boundary benchmark",
                lambda: benchmark_annotations(rows, detector),
                "benchmark",
            )
            return
        if action == "audit:phase1":
            if self._background_job_running():
                self.message = f"{self.background_job} is still running."
                return
            rows = self.store.candidate_annotations()
            settings = {
                key: self.boundary_settings[key]
                for key in (
                    "max_candidates", "min_area_ratio", "max_area_ratio",
                    "min_aspect_ratio", "max_aspect_ratio",
                    "max_perspective_distortion", "min_edge_support",
                )
            }
            def make_detector(experimental: bool):
                return lambda image, **kwargs: detect_boundary_candidates(
                    image,
                    outer_profile=None,
                    experimental_outer=experimental,
                    max_candidates=kwargs.pop("max_candidates", 1000),
                    **{key: value for key, value in settings.items() if key != "max_candidates"},
                    **kwargs
                )
            baseline_fn = make_detector(False)
            experimental_fn = make_detector(True)
            self._start_background_job(
                "Phase 1 dataset audit",
                lambda: self._run_phase1_audit(rows, baseline_fn, experimental_fn),
                "audit",
            )
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

    def _save_boundary_reference(self) -> None:
        if self.reference_frame is None:
            self.message = "Capture or import an image before saving."
            return
        if len(self.reference_points) != 4:
            self.message = "Select all four corners before saving."
            return
        valid, reasons = validate_annotation(self.reference_points, self.reference_frame.shape)
        if not valid:
            self.message = "Cannot save invalid polygon: " + "; ".join(reasons)
            return
        try:
            existing = None
            if self.reference_selected_id:
                existing = next(
                    (item for item in list_references()
                     if item["sample_id"] == self.reference_selected_id),
                    None,
                )
            record = save_reference(
                self.reference_frame, self.reference_points, self.reference_condition,
                self.session_id, self.reference_visibility, self.reference_notes,
                verified=True, sample_id=self.reference_selected_id, existing=existing,
            )
        except (OSError, ValueError) as error:
            self.message = f"Reference not saved: {error}"
            return
        self.reference_records = list_references()
        self.reference_selected_id = record["sample_id"]
        self.reference_save_pending = False
        self.reference_view = "collection"
        self.message = f"Saved verified boundary reference {record['sample_id']}."

    def _handle_reference_mouse_down(self, position: tuple[int, int]) -> None:
        if self.reference_view != "annotate" or self.reference_frame is None:
            return
        point = self._reference_image_point(position)
        if point is None:
            return
        distances = [
            (index, (point[0] - existing[0]) ** 2 + (point[1] - existing[1]) ** 2)
            for index, existing in enumerate(self.reference_points)
        ]
        if distances and min(distances, key=lambda item: item[1])[1] <= 24 ** 2:
            self.reference_drag_index = min(distances, key=lambda item: item[1])[0]
        elif len(self.reference_points) < 4:
            self.reference_points.append([point[0], point[1]])
            self.reference_save_pending = False
        else:
            self.message = "Four corners are set; drag a marker or reset the points."

    def _handle_reference_mouse_motion(self, position: tuple[int, int]) -> None:
        if self.reference_drag_index is None:
            return
        point = self._reference_image_point(position)
        if point is not None:
            self.reference_points[self.reference_drag_index] = [point[0], point[1]]
            self.reference_save_pending = False

    def _handle_reference_mouse_up(self) -> None:
        self.reference_drag_index = None

    def run(self) -> None:
        clock = pygame.time.Clock()
        active = True
        while active:
            dt = clock.tick(30) / 1000.0
            self._poll_background_job()
            self._poll_recognition_job()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_reference_mouse_down(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self._handle_reference_mouse_motion(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self._handle_reference_mouse_up()
                    for rect, action in self.buttons:
                        if rect.collidepoint(event.pos):
                            self.handle(action)
                elif event.type == pygame.KEYDOWN and self.reference_view == "annotate":
                    if event.key == pygame.K_ESCAPE:
                        self.handle("reference:cancel")
                    elif event.key == pygame.K_r:
                        self.handle("reference:reset")
                    elif event.key == pygame.K_s:
                        self.handle("reference:save")
                    elif event.key == pygame.K_BACKSPACE:
                        self.reference_notes = self.reference_notes[:-1]
                    elif event.unicode and len(self.reference_notes) < 160:
                        self.reference_notes += event.unicode
            if self.running_camera:
                frame = self.camera_capture.latest_frame()
                if frame is not None:
                    self.last_frame = frame
                status = self.camera_capture.snapshot()
                if not status.running and status.last_error and self.running_camera:
                    self.running_camera = False
                    self.message = f"Camera stopped: {status.last_error}"
            phase1_page = (
                self.page in self.phase_pages
                and self.phase_pages[self.page] == "phase1"
            )
            diagnostics_page = self.page == "Camera Diagnostics" and self.running_camera
            if phase1_page or diagnostics_page:
                self.update_boundary(dt, collect_review=phase1_page)
            self.draw()
            pygame.display.flip()
        self.handle("stop_camera")
        self.boundary_detection_executor.shutdown(wait=True)
        self.background_executor.shutdown(wait=True)
        self.store.close()
        pygame.quit()


def main() -> None:
    pygame.init()
    RecognitionLab().run()


if __name__ == "__main__":
    main()
