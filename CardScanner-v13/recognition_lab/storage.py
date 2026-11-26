"""Small, durable SQLite store for lab metadata and verification records."""

from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import DATABASE, MATERIALS, ensure_layout


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    def __init__(self, path: Path = DATABASE) -> None:
        ensure_layout()
        self.path = path
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(
            """
            PRAGMA foreign_keys=ON;
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY,
                path TEXT NOT NULL UNIQUE,
                phase TEXT NOT NULL,
                kind TEXT NOT NULL,
                card_name TEXT,
                sha256 TEXT NOT NULL,
                imported_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY,
                phase TEXT NOT NULL,
                image_path TEXT,
                card_name TEXT,
                prediction TEXT,
                verification TEXT NOT NULL,
                details_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phase TEXT NOT NULL,
                version TEXT NOT NULL,
                config_json TEXT NOT NULL,
                dataset_version TEXT,
                metrics_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(name, version)
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS candidate_annotations (
                id INTEGER PRIMARY KEY,
                session_id TEXT NOT NULL,
                candidate_id INTEGER NOT NULL,
                frame_path TEXT NOT NULL,
                crop_path TEXT,
                corners_json TEXT NOT NULL,
                metrics_json TEXT NOT NULL,
                detection_method TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                tracking_status TEXT NOT NULL,
                judgment TEXT,
                UNIQUE(session_id, candidate_id)
            );
            """
        )
        columns = {
            row["name"] for row in self.connection.execute(
                "PRAGMA table_info(candidate_annotations)"
            )
        }
        if "crop_path" not in columns:
            self.connection.execute(
                "ALTER TABLE candidate_annotations ADD COLUMN crop_path TEXT"
            )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def import_file(self, source: Path, phase: str, kind: str, card_name: str = "") -> Path:
        source = source.resolve()
        if source.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError(f"Unsupported image format: {source.suffix}")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        existing = self.connection.execute(
            "SELECT path FROM materials WHERE sha256 = ?", (digest,)
        ).fetchone()
        if existing:
            return Path(existing["path"])
        target_dir = MATERIALS / "uploads" / phase
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{digest[:12]}_{source.name}"
        shutil.copy2(source, target)
        self.connection.execute(
            "INSERT INTO materials(path, phase, kind, card_name, sha256, imported_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (str(target), phase, kind, card_name.strip() or None, digest, utc_now()),
        )
        self.connection.commit()
        return target

    def materials(self, phase: str | None = None) -> list[sqlite3.Row]:
        if phase:
            return list(self.connection.execute(
                "SELECT * FROM materials WHERE phase = ? ORDER BY imported_at DESC", (phase,)
            ))
        return list(self.connection.execute("SELECT * FROM materials ORDER BY imported_at DESC"))

    def add_observation(
        self, phase: str, image_path: str | None, card_name: str | None,
        prediction: str | None, verification: str, details: dict[str, Any],
    ) -> int:
        cursor = self.connection.execute(
            "INSERT INTO observations(phase,image_path,card_name,prediction,verification,"
            "details_json,created_at) VALUES (?,?,?,?,?,?,?)",
            (phase, image_path, card_name, prediction, verification,
             json.dumps(details, sort_keys=True), utc_now()),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def observations(self, phase: str | None = None) -> list[sqlite3.Row]:
        if phase:
            return list(self.connection.execute(
                "SELECT * FROM observations WHERE phase = ? ORDER BY created_at DESC", (phase,)
            ))
        return list(self.connection.execute(
            "SELECT * FROM observations ORDER BY created_at DESC"
        ))

    def add_experiment(
        self, name: str, phase: str, version: str, config: dict[str, Any],
        dataset_version: str = "", metrics: dict[str, Any] | None = None,
    ) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO experiments(name,phase,version,config_json,"
            "dataset_version,metrics_json,created_at) VALUES (?,?,?,?,?,?,?)",
            (name, phase, version, json.dumps(config, sort_keys=True),
             dataset_version, json.dumps(metrics or {}, sort_keys=True), utc_now()),
        )
        self.connection.commit()

    def experiments(self) -> list[sqlite3.Row]:
        return list(self.connection.execute("SELECT * FROM experiments ORDER BY created_at DESC"))

    def counts(self) -> dict[str, int]:
        return {
            "materials": self.connection.execute("SELECT COUNT(*) FROM materials").fetchone()[0],
            "observations": self.connection.execute("SELECT COUNT(*) FROM observations").fetchone()[0],
            "experiments": self.connection.execute("SELECT COUNT(*) FROM experiments").fetchone()[0],
        }

    def set_setting(self, key: str, value: str) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO settings(key,value) VALUES (?,?)", (key, value)
        )
        self.connection.commit()

    def get_setting(self, key: str, default: str = "") -> str:
        row = self.connection.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return str(row["value"]) if row else default

    def save_candidate_annotation(
        self, session_id: str, candidate_id: int, frame_path: str,
        corners: list[list[float]], metrics: dict[str, Any],
        detection_method: str, tracking_status: str, judgment: str,
        crop_path: str | None = None,
    ) -> int:
        cursor = self.connection.execute(
            "INSERT INTO candidate_annotations("
            "session_id,candidate_id,frame_path,corners_json,metrics_json,"
            "detection_method,timestamp,tracking_status,judgment,crop_path) "
            "VALUES (?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(session_id,candidate_id) DO UPDATE SET "
            "frame_path=excluded.frame_path,corners_json=excluded.corners_json,"
            "metrics_json=excluded.metrics_json,detection_method=excluded.detection_method,"
            "timestamp=excluded.timestamp,tracking_status=excluded.tracking_status,"
            "judgment=excluded.judgment,crop_path=excluded.crop_path",
            (
                session_id, int(candidate_id), frame_path, json.dumps(corners),
                json.dumps(metrics, sort_keys=True), detection_method, utc_now(),
                tracking_status, judgment, crop_path,
            ),
        )
        self.connection.commit()
        return int(cursor.lastrowid or self.connection.execute(
            "SELECT id FROM candidate_annotations WHERE session_id=? AND candidate_id=?",
            (session_id, candidate_id),
        ).fetchone()["id"])

    def reset_candidate_annotation(self, session_id: str, candidate_id: int) -> None:
        self.connection.execute(
            "UPDATE candidate_annotations SET judgment=NULL WHERE session_id=? AND candidate_id=?",
            (session_id, candidate_id),
        )
        self.connection.commit()

    def candidate_annotations(self, session_id: str | None = None) -> list[sqlite3.Row]:
        if session_id:
            return list(self.connection.execute(
                "SELECT * FROM candidate_annotations WHERE session_id=? ORDER BY timestamp DESC",
                (session_id,),
            ))
        return list(self.connection.execute(
            "SELECT * FROM candidate_annotations ORDER BY timestamp DESC"
        ))

    def candidate_judgment(self, session_id: str, candidate_id: int) -> str | None:
        row = self.connection.execute(
            "SELECT judgment FROM candidate_annotations WHERE session_id=? AND candidate_id=?",
            (session_id, candidate_id),
        ).fetchone()
        return str(row["judgment"]) if row and row["judgment"] else None
