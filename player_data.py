"""Locally persisted settings, player profiles, story saves, and score records."""

from datetime import datetime, timezone
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import time
from uuid import uuid4


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
_active_profile_id = None
_last_error = ""
_pending_score_records = []
_score_prompts_deferred = False


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
    if not isinstance(_data.get("profiles"), dict):
        _data["profiles"] = {}
    legacy_completed = list(_data["completed_chapters"])
    legacy_completed.extend(
        record.get("chapter")
        for record in _data["chapter_records"]
        if isinstance(record, dict)
        and record.get("completed")
        and record.get("chapter")
    )
    legacy_completed = list(dict.fromkeys(legacy_completed))
    if not _data["profiles"] and legacy_completed:
        _data["profiles"]["legacy"] = {
            "name": "Player",
            "completed_chapters": legacy_completed,
            "total_score": 0,
            "checkpoint": None,
        }
        _data["last_profile_id"] = "legacy"
    if _data.get("last_profile_id") not in _data["profiles"]:
        _data["last_profile_id"] = None
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


def last_profile():
    data = _load()
    profile_id = data.get("last_profile_id")
    profile = data["profiles"].get(profile_id)
    if not isinstance(profile, dict):
        return None
    return {**deepcopy(profile), "id": profile_id}


def current_profile():
    data = _load()
    profile_id = _active_profile_id or data.get("last_profile_id")
    profile = data["profiles"].get(profile_id)
    if not isinstance(profile, dict):
        return None
    return {**deepcopy(profile), "id": profile_id}


def active_profile_id():
    return _active_profile_id


def select_profile(profile_id):
    global _active_profile_id
    data = _load()
    if profile_id not in data["profiles"]:
        _report_error("The selected player profile no longer exists.")
        return False
    previous_id = _active_profile_id
    previous_last_id = data.get("last_profile_id")
    _active_profile_id = profile_id
    data["last_profile_id"] = profile_id
    if not _save():
        _active_profile_id = previous_id
        data["last_profile_id"] = previous_last_id
        return False
    return True


def create_profile(player_name):
    global _active_profile_id
    name = str(player_name).strip()[:16]
    if not name:
        _report_error("Enter a name before starting a new game.")
        return False

    data = _load()
    if any(
        str(profile.get("name", "")).casefold() == name.casefold()
        for profile in data["profiles"].values()
        if isinstance(profile, dict)
    ):
        _report_error("A player with that name already has a save.")
        return False

    profile_id = uuid4().hex
    data["profiles"][profile_id] = {
        "name": name,
        "completed_chapters": [],
        "total_score": 0,
        "checkpoint": None,
    }
    previous_last_id = data.get("last_profile_id")
    previous_active_id = _active_profile_id
    data["last_profile_id"] = profile_id
    _active_profile_id = profile_id
    if not _save():
        del data["profiles"][profile_id]
        data["last_profile_id"] = previous_last_id
        _active_profile_id = previous_active_id
        return False
    return True


def profile_total_score(profile=None):
    profile = profile or current_profile()
    if not isinstance(profile, dict):
        return 0
    total = max(0, int(profile.get("total_score", 0)))
    checkpoint = profile.get("checkpoint")
    if isinstance(checkpoint, dict):
        run = checkpoint.get("run", {})
        if isinstance(run, dict):
            minigame_points = sum(
                max(0, int(score))
                for score in run.get("minigame_scores", {}).values()
            )
            total += max(
                0,
                (1000 if checkpoint.get("completed") else 0)
                + max(0, int(run.get("time_bonus", 0)))
                + minigame_points - max(0, int(run.get("mistakes", 0))) * 50,
            )
    return total


def player_rankings():
    profiles = [
        {
            "player_name": str(profile.get("name", "Player")),
            "score": profile_total_score(profile),
            "completed_chapters": len(profile.get("completed_chapters", [])),
        }
        for profile in _load()["profiles"].values()
        if isinstance(profile, dict)
    ]
    return sorted(
        profiles,
        key=lambda profile: (-profile["score"], profile["player_name"].casefold()),
    )


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
    global _current_run, _score_prompts_deferred
    _score_prompts_deferred = True
    _current_run = {
        "chapter": chapter_id,
        "started": time.monotonic(),
        "mistakes": 0,
        "time_bonus": 0,
        "challenges_solved": 0,
        "minigame_scores": {},
    }


def chapter_save(chapter_id=None):
    profile = current_profile()
    checkpoint = profile.get("checkpoint") if profile else None
    if not isinstance(checkpoint, dict):
        return None
    if chapter_id is not None and checkpoint.get("chapter") != chapter_id:
        return None
    return deepcopy(checkpoint)


def resume_chapter(chapter_id, checkpoint):
    global _current_run, _score_prompts_deferred
    if not isinstance(checkpoint, dict) or checkpoint.get("chapter") != chapter_id:
        return False
    run = checkpoint.get("run")
    if not isinstance(run, dict) or not isinstance(run.get("minigame_scores", {}), dict):
        return False
    try:
        elapsed = max(0, int(run.get("elapsed_seconds", 0)))
        mistakes = max(0, int(run.get("mistakes", 0)))
        time_bonus = max(0, int(run.get("time_bonus", 0)))
        challenges_solved = max(0, int(run.get("challenges_solved", 0)))
        minigame_scores = {
            str(name): max(0, int(score))
            for name, score in run.get("minigame_scores", {}).items()
        }
    except (TypeError, ValueError):
        return False
    _current_run = {
        "chapter": chapter_id,
        "started": time.monotonic() - elapsed,
        "mistakes": mistakes,
        "time_bonus": time_bonus,
        "challenges_solved": challenges_solved,
        "minigame_scores": minigame_scores,
    }
    _score_prompts_deferred = True
    return True


def save_chapter_progress(checkpoint):
    profile = current_profile()
    if profile is None:
        _report_error("Select a player before saving story progress.")
        return False
    if not isinstance(checkpoint, dict) or not checkpoint.get("chapter"):
        _report_error("The story checkpoint is invalid.")
        return False

    data = _load()
    profile_id = _active_profile_id or data.get("last_profile_id")
    stored_profile = data["profiles"][profile_id]
    old_checkpoint = deepcopy(stored_profile.get("checkpoint"))
    elapsed = (
        max(0, int(time.monotonic() - _current_run["started"]))
        if _current_run is not None
        else 0
    )
    run = {
        "mistakes": _current_run["mistakes"],
        "time_bonus": _current_run["time_bonus"],
        "challenges_solved": _current_run["challenges_solved"],
        "minigame_scores": dict(_current_run["minigame_scores"]),
        "elapsed_seconds": elapsed,
    } if _current_run is not None else {}
    stored_profile["checkpoint"] = deepcopy(checkpoint)
    stored_profile["checkpoint"]["run"] = run
    if not _save():
        stored_profile["checkpoint"] = old_checkpoint
        return False
    return True


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
        key = str(name)
        _current_run["minigame_scores"][key] = (
            _current_run["minigame_scores"].get(key, 0)
            + max(0, score - result["time_bonus"])
        )
        _current_run["time_bonus"] += result["time_bonus"]
    else:
        profile = current_profile()
        if profile is not None:
            data = _load()
            profile_id = _active_profile_id or data.get("last_profile_id")
            stored_profile = data["profiles"][profile_id]
            old_total = stored_profile.get("total_score", 0)
            stored_profile["total_score"] = max(0, int(old_total)) + score
            if not _save():
                stored_profile["total_score"] = old_total
                return False
        else:
            _pending_score_records.append({"kind": "minigame", "record": result})
    return True


def pending_score_record():
    if _score_prompts_deferred:
        return None
    return _pending_score_records[0] if _pending_score_records else None


def release_pending_score_prompts():
    global _score_prompts_deferred
    _score_prompts_deferred = False


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
    profile = current_profile()
    if profile is not None:
        profile_id = _active_profile_id or data.get("last_profile_id")
        stored_profile = data["profiles"][profile_id]
        completed = stored_profile.setdefault("completed_chapters", [])
        if result["chapter"] not in completed:
            completed.append(result["chapter"])
        stored_profile["total_score"] = (
            max(0, int(stored_profile.get("total_score", 0))) + total_score
        )
        stored_profile["checkpoint"] = None
        result["player_name"] = stored_profile.get("name", "Player")
    else:
        completed = data["completed_chapters"]
        if result["chapter"] not in completed:
            completed.append(result["chapter"])
    _current_run = None
    if profile is None:
        _save()
        _pending_score_records.append({"kind": "chapter", "record": result})
    else:
        _save()
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
    profile = current_profile()
    if profile is not None:
        return set(profile.get("completed_chapters", []))
    completed = {
        record.get("chapter")
        for record in _load()["chapter_records"]
        if isinstance(record, dict) and record.get("completed")
    }
    completed.update(_load()["completed_chapters"])
    return completed


def chapter_unlocked(chapter_id, chapter_ids):
    try:
        chapter_index = chapter_ids.index(chapter_id)
    except ValueError:
        return False
    completed = chapter_progress()
    return all(previous_id in completed for previous_id in chapter_ids[:chapter_index])
