"""Separate live card-learning window for the v13 scanner.

This tool does not replace the game scanner or modify the v13 model.
Verified observations are copied into a live-learning dataset and an
incremental experimental model is rebuilt from the existing v13 model.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import cv2
import numpy as np
import pygame

import cardscan.features as features
import cardscan.model as model_module
import cardscan.registry as registry
from recognition_lab.recognition_testing import _recognize_harvesthand_frame


PLANT_LABELS = [
    ("pechay_plant", "Pechay"),
    ("monggo_plant", "Monggo"),
    ("okra_plant", "Okra"),
    ("squash_plant", "Kalabasa"),
    ("tomato_plant", "Kamatis"),
    ("eggplant_plant", "Talong"),
    ("sweet_potato_plant", "Kamote"),
    ("rice_plant", "Palay"),
]
V13_MODEL = ROOT / "card_model_card_plants_mean_centered_v13_experimental.json"
EXPORT_DIR = ROOT / "recognition_lab" / "exports" / "live_training"
LIVE_MODEL = EXPORT_DIR / "card_model_card_plants_v13_live_experimental.json"
OBSERVATIONS = EXPORT_DIR / "observations.jsonl"


def open_camera(device=0, width=1280, height=720):
    for candidate in range(device, device + 4):
        for backend_name, backend in (
            ("Media Foundation", cv2.CAP_MSMF),
            ("DirectShow", cv2.CAP_DSHOW),
            ("Default", cv2.CAP_ANY),
        ):
            cap = cv2.VideoCapture(candidate, backend)
            if not cap.isOpened():
                cap.release()
                continue
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            cap.set(cv2.CAP_PROP_FPS, 30)
            cap.set(cv2.CAP_PROP_FOURCC,
                    cv2.VideoWriter_fourcc(*"MJPG"))
            ok, frame = cap.read()
            if ok and frame is not None:
                return cap, candidate, backend_name
            cap.release()
    return None, None, None


def crop_card(frame_bgr, points):
    if not points or len(points) != 4:
        return None
    try:
        source = np.asarray(points, dtype=np.float32).reshape(4, 2)
        destination = np.float32([
            [0, 0],
            [119, 0],
            [119, 167],
            [0, 167],
        ])
        matrix = cv2.getPerspectiveTransform(source, destination)
        return cv2.warpPerspective(
            frame_bgr, matrix, (120, 168),
            flags=cv2.INTER_LINEAR,
        )
    except cv2.error:
        return None


def bgr_to_surface(frame_bgr):
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    height, width = rgb.shape[:2]
    return pygame.image.frombuffer(
        rgb.tobytes(), (width, height), "RGB"
    )


def add_live_sample(actual_slug, crop_bgr):
    model_path = LIVE_MODEL if LIVE_MODEL.is_file() else V13_MODEL
    live_model = model_module.load_model(str(model_path))
    if live_model is None:
        return None

    pygame.init()
    vector = features.extract_card(bgr_to_surface(crop_bgr))
    if vector is None:
        return None
    centered = model_module._normalize([
        x - m
        for x, m in zip(vector, live_model["mean"])
    ])
    entry = live_model["cards"].get(actual_slug)
    if entry is None:
        live_model["cards"][actual_slug] = {
            "centroid": centered,
            "samples": [centered],
            "n": 1,
        }
    else:
        entry.setdefault("samples", [])
        entry["samples"].append(centered)
        entry["n"] = len(entry["samples"])
        entry["centroid"] = model_module._mean(entry["samples"])

    LIVE_MODEL.parent.mkdir(parents=True, exist_ok=True)
    model_module.save_model(live_model, str(LIVE_MODEL))
    os.environ["HARVESTHAND_CARD_MODEL"] = str(LIVE_MODEL)
    return LIVE_MODEL


def append_jsonl(path, row):
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def save_verified(frame_bgr, crop_bgr, result, actual_slug, verdict):
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    raw_path = EXPORT_DIR / f"{stamp}_raw.jpg"
    crop_path = EXPORT_DIR / f"{stamp}_crop.jpg"
    cv2.imwrite(str(raw_path), frame_bgr)
    if crop_bgr is not None:
        cv2.imwrite(str(crop_path), crop_bgr)

    row = {
        "timestamp": datetime.now().isoformat(),
        "verdict": verdict,
        "actual_slug": actual_slug,
        "predicted_slug": result.get("reference_id"),
        "prediction": result.get("prediction"),
        "score": result.get("score"),
        "margin": result.get("margin"),
        "input_mode": result.get("input_mode"),
        "marker_id": result.get("marker_id"),
        "engine": result.get("engine"),
        "raw_image": str(raw_path),
        "crop_image": str(crop_path) if crop_bgr is not None else None,
        "target_scores": result.get("target_scores", []),
    }
    append_jsonl(OBSERVATIONS, row)
    live_model = None
    if crop_bgr is not None:
        live_model = add_live_sample(actual_slug, crop_bgr)

    dataset_dir = ROOT / "data" / "live_card_observations" / actual_slug
    dataset_dir.mkdir(parents=True, exist_ok=True)
    dataset_image = dataset_dir / f"{stamp}.jpg"
    cv2.imwrite(
        str(dataset_image),
        crop_bgr if crop_bgr is not None else frame_bgr,
    )
    row["training_dataset_image"] = str(dataset_image)
    return row, live_model


class MiniLiveCardTester:
    def __init__(self, width=1280, height=720, device=0):
        pygame.init()
        pygame.display.set_caption("HarvestHand - Live Card Learning")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.small = pygame.font.SysFont(None, 22)
        self.cap = None
        self.device = device
        self.backend = None
        self.frame = None
        self.result = None
        self.last_recognize = 0.0
        self.actual_slug = None
        self.feedback = ""
        self.running = True

    def open(self):
        self.cap, device, self.backend = open_camera(
            self.device, 1280, 720
        )
        if self.cap is not None:
            self.device = device
        return self.cap is not None

    def predict(self):
        if self.frame is None:
            return
        self.result = _recognize_harvesthand_frame(
            self.frame,
            model_path=(
                LIVE_MODEL if LIVE_MODEL.is_file() else V13_MODEL
            ),
        )
        self.actual_slug = None

    def _text(self, text, rect, color=(235, 238, 228),
              font=None, center=False):
        font = font or self.font
        surface = font.render(text, True, color)
        if center:
            target = surface.get_rect(center=rect.center)
        else:
            target = rect
        self.screen.blit(surface, target)

    def draw(self):
        self.screen.fill((28, 36, 36))
        pygame.draw.rect(
            self.screen, (10, 12, 14),
            pygame.Rect(20, 20, 760, 520),
            border_radius=8,
        )
        if self.frame is not None:
            rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            rgb = cv2.resize(rgb, (760, 520))
            surface = pygame.image.frombuffer(
                rgb.tobytes(), (760, 520), "RGB"
            )
            self.screen.blit(surface, (20, 20))
            if self.result and self.result.get("points"):
                try:
                    points = np.asarray(
                        self.result["points"], dtype=np.float32
                    )
                    height, width = self.frame.shape[:2]
                    points[:, 0] *= 760.0 / width
                    points[:, 1] *= 520.0 / height
                    pygame.draw.lines(
                        self.screen, (90, 220, 130),
                        True,
                        [(int(x), int(y) + 20) for x, y in points],
                        3,
                    )
                except (ValueError, TypeError):
                    pass
        else:
            self._text(
                "Camera unavailable",
                pygame.Rect(220, 250, 360, 50),
                (245, 170, 120),
                center=True,
            )

        panel = pygame.Rect(800, 20, 460, 680)
        pygame.draw.rect(
            self.screen, (42, 52, 50), panel, border_radius=10
        )
        self._text("LIVE CARD TESTER", pygame.Rect(825, 38, 410, 40),
                   (210, 225, 190), pygame.font.SysFont(None, 34))

        status = (
            f"Camera: {self.backend} / device {self.device}"
            if self.cap is not None else "Camera: unavailable"
        )
        self._text(status, pygame.Rect(825, 82, 410, 24),
                   (170, 205, 180), self.small)

        if self.result:
            prediction = self.result.get("prediction") or "NO CONFIDENT MATCH"
            score = float(self.result.get("score", 0.0))
            margin = float(self.result.get("margin", 0.0))
            color = (
                (110, 220, 130)
                if self.result.get("confident") else (245, 180, 120)
            )
            self._text("Prediction", pygame.Rect(825, 125, 410, 24),
                       (190, 205, 195), self.small)
            self._text(prediction, pygame.Rect(825, 150, 410, 42),
                       color, pygame.font.SysFont(None, 42))
            self._text(
                f"score {score:.3f}  margin {margin:.3f}",
                pygame.Rect(825, 194, 410, 26),
                (210, 220, 210), self.small,
            )
            self._text(
                self.result.get("engine", ""),
                pygame.Rect(825, 220, 410, 24),
                (180, 190, 185), self.small,
            )
        else:
            self._text("Prediction: waiting", pygame.Rect(825, 125, 410, 40),
                       (245, 180, 120))

        self._text("If correct:", pygame.Rect(825, 260, 410, 24),
                   (210, 220, 210), self.small)
        correct_rect = pygame.Rect(825, 288, 410, 48)
        pygame.draw.rect(self.screen, (62, 120, 78), correct_rect,
                         border_radius=8)
        self._text("CORRECT", correct_rect, (245, 250, 238),
                   pygame.font.SysFont(None, 30), center=True)

        self._text("If wrong, choose actual card:",
                   pygame.Rect(825, 350, 410, 24),
                   (210, 220, 210), self.small)
        y = 378
        for index, (slug, label) in enumerate(PLANT_LABELS):
            x = 825 + (index % 2) * 205
            row_y = y + (index // 2) * 42
            rect = pygame.Rect(x, row_y, 195, 34)
            selected = slug == self.actual_slug
            pygame.draw.rect(
                self.screen,
                (92, 128, 96) if selected else (55, 68, 65),
                rect, border_radius=7,
            )
            self._text(label, rect, (245, 245, 235),
                       self.small, center=True)

        wrong_rect = pygame.Rect(825, 630, 410, 48)
        pygame.draw.rect(self.screen, (155, 75, 65), wrong_rect,
                         border_radius=8)
        self._text("INCORRECT - SAVE ACTUAL", wrong_rect,
                   (255, 245, 235),
                   pygame.font.SysFont(None, 27), center=True)
        self._text(self.feedback, pygame.Rect(825, 680, 410, 24),
                   (190, 205, 195), self.small)

    def handle_click(self, pos):
        correct_rect = pygame.Rect(825, 288, 410, 48)
        if correct_rect.collidepoint(pos):
            self.verify("CORRECT")
            return
        wrong_rect = pygame.Rect(825, 630, 410, 48)
        if wrong_rect.collidepoint(pos):
            self.verify("INCORRECT")
            return
        y = 378
        for index, (slug, _label) in enumerate(PLANT_LABELS):
            x = 825 + (index % 2) * 205
            row_y = y + (index // 2) * 42
            rect = pygame.Rect(x, row_y, 195, 34)
            if rect.collidepoint(pos):
                self.actual_slug = slug
                return

    def verify(self, verdict):
        if self.frame is None or self.result is None:
            self.feedback = "No frame/prediction to verify."
            return
        actual_slug = self.actual_slug
        if verdict == "CORRECT":
            actual_slug = self.result.get("reference_id") or actual_slug
        if actual_slug is None:
            self.feedback = "Choose the actual card."
            return
        crop = crop_card(
            self.frame,
            self.result.get("points"),
        )
        row, live_model = save_verified(
            self.frame, crop, self.result, actual_slug, verdict
        )
        self.feedback = (
            f"Saved {verdict.lower()} as {actual_slug}"
            + ("; live model updated" if live_model else "")
        )

    def run(self):
        while self.running:
            now = time.monotonic()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            if self.cap is not None:
                ok, frame = self.cap.read()
                if ok and frame is not None:
                    self.frame = frame
            if now - self.last_recognize >= 0.5:
                self.last_recognize = now
                self.predict()
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)
        if self.cap is not None:
            self.cap.release()
        pygame.quit()


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip())
    parser.add_argument("--device", type=int, default=0)
    args = parser.parse_args()
    tester = MiniLiveCardTester(device=args.device)
    if not tester.open():
        print("No readable camera found.")
    tester.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
