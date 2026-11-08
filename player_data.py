"""Locally persisted game settings, chapter runs, and minigame records."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time


def _data_directory():
    if os.name == "nt":
        root = Path(os.environ.get(
            "LOCALAPPDATA",
            os.environ.get("APPDATA", Path.home() / "AppData" / "Local"),
        ))
        return root / "HarvestHand"
    root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return root / "harvesthand"


_DATA_PATH = _data_directory() / "player_data.json"
_DEFAULT_SETTINGS = {
    "sound_volume": 0.7,
    "music_volume": 0.25,
    "fullscreen": True,
    "camera_device": 0,
}
_data = None
_current_run = None
_last_error = ""
_pending_score_records = []


def _load():
    global _data
    if _data is not None:
        return _data

    try:
        contents = _DATA_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        contents = None
    except OSError as exc:
        _report_error(f"Could not read local game data: {exc}")
        contents = None

    if contents is None:
        _data = {}
    else:
        try:
            loaded = json.loads(contents)
            if not isinstance(loaded, dict):
                _report_error("Local game data has an invalid root; using fresh defaults.")
                loaded = {}
            _data = loaded
        except json.JSONDecodeError as exc:
            _report_error(f"Local game data is invalid JSON: {exc}")
            _data = {}

    settings = _data.setdefault("settings", {})
    if not isinstance(settings, dict):
        settings = _data["settings"] = {}
    for key, value in _DEFAULT_SETTINGS.items():
        settings.setdefault(key, value)
    if not isinstance(_data.get("chapter_records"), list):
        _data["chapter_records"] = []
    if not isinstance(_data.get("minigame_records"), list):
        _data["minigame_records"] = []
    if not isinstance(_data.get("completed_chapters"), list):
        _data["completed_chapters"] = []
    return _data


def _report_error(message):
    global _last_error
    _last_error = message
    print(f"[player-data] {message}", file=sys.stderr)


def last_error():
    return _last_error


def get_settings():
    return dict(_load()["settings"])


def update_settings(**changes):
    settings = _load()["settings"]
    for key, value in changes.items():
        if key in ("sound_volume", "music_volume"):
            settings[key] = max(0.0, min(1.0, float(value)))
        elif key == "fullscreen":
            settings[key] = bool(value)
        elif key == "camera_device":
            settings[key] = max(0, min(9, int(value)))
    return _save()


def _save():
    global _last_error
    data = _load()
    temp_path = _DATA_PATH.with_suffix(".tmp")
    try:
        _DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        temp_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_path.replace(_DATA_PATH)
    except OSError as exc:
        _report_error(f"Could not save local game data: {exc}")
        return False
    _last_error = ""
    return True


def begin_chapter(chapter_id):
    global _current_run
    _current_run = {
        "chapter": chapter_id,
        "started": time.monotonic(),
        "mistakes": 0,
        "time_bonus": 0,
        "challenges_solved": 0,
        "minigame_scores": {},
    }


def abort_chapter():
    global _current_run
    _current_run = None


def record_mistake():
    if _current_run is not None:
        _current_run["mistakes"] += 1


def record_challenge_success(time_left=0):
    if _current_run is None:
        return
    _current_run["challenges_solved"] += 1
    _current_run["time_bonus"] += max(0, int(float(time_left))) * 10


def record_minigame_result(name, score, mistakes=0, time_bonus=0):
    score = max(0, int(score))
    result = {
        "game": str(name),
        "score": score,
        "mistakes": max(0, int(mistakes)),
        "time_bonus": max(0, int(time_bonus)),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    if _current_run is not None:
        _current_run["minigame_scores"][str(name)] = max(0, score - result["time_bonus"])
        _current_run["time_bonus"] += result["time_bonus"]
    _pending_score_records.append({"kind": "minigame", "record": result})
    return True


def pending_score_record():
    return _pending_score_records[0] if _pending_score_records else None


def record_pending_score(player_name):
    if not _pending_score_records:
        return False
    player_name = str(player_name).strip()[:16]
    if not player_name:
        _report_error("Enter a nickname before recording the score.")
        return False

    pending = _pending_score_records[0]
    data = _load()
    records_key = (
        "chapter_records" if pending["kind"] == "chapter" else "minigame_records"
    )
    records = data[records_key]
    previous_records = list(records)
    record = dict(pending["record"])
    record["player_name"] = player_name
    records.append(record)
    del records[:-500]
    if not _save():
        records[:] = previous_records
        return False
    _pending_score_records.pop(0)
    return True


def decline_pending_score():
    if not _pending_score_records:
        return False
    _pending_score_records.pop(0)
    return True


def complete_chapter():
    global _current_run
    if _current_run is None:
        return None

    elapsed = max(0, int(time.monotonic() - _current_run["started"]))
    minigame_points = sum(_current_run["minigame_scores"].values())
    completion_points = 1000
    mistake_penalty = _current_run["mistakes"] * 50
    total_score = max(
        0,
        completion_points + _current_run["time_bonus"]
        + minigame_points - mistake_penalty,
    )
    result = {
        "chapter": _current_run["chapter"],
        "score": total_score,
        "completed": True,
        "completion_points": completion_points,
        "time_bonus": _current_run["time_bonus"],
        "mistakes": _current_run["mistakes"],
        "challenges_solved": _current_run["challenges_solved"],
        "minigame_scores": dict(_current_run["minigame_scores"]),
        "minigame_points": minigame_points,
        "elapsed_seconds": elapsed,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    data = _load()
    completed = data["completed_chapters"]
    if _current_run["chapter"] not in completed:
        completed.append(_current_run["chapter"])
    _current_run = None
    _save()
    _pending_score_records.append({"kind": "chapter", "record": result})
    return result


def chapter_rankings():
    records = [
        dict(record) for record in _load()["chapter_records"]
        if isinstance(record, dict) and record.get("completed")
    ]
    return sorted(
        records,
        key=lambda record: (
            -int(record.get("score", 0)),
            int(record.get("mistakes", 0)),
            int(record.get("elapsed_seconds", 0)),
        ),
    )


def minigame_rankings():
    best = {}
    for record in _load()["minigame_records"]:
        if not isinstance(record, dict):
            continue
        game = record.get("game")
        if not game:
            continue
        if game not in best or int(record.get("score", 0)) > int(best[game].get("score", 0)):
            best[game] = dict(record)
    return sorted(best.values(), key=lambda record: (-int(record["score"]), record["game"]))


def chapter_progress():
    completed = {
        record.get("chapter")
        for record in _load()["chapter_records"]
        if isinstance(record, dict) and record.get("completed")
    }
    completed.update(_load()["completed_chapters"])
    return completed
