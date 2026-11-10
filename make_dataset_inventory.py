"""Part 1 — Dataset inventory script.

Scans the existing training images in data/card_samples/ and produces
a CSV inventory with: filename, class label, image dimensions, file
modification timestamp, capture session identifier (if known), and
dataset membership (existing or new).

Read-only: does not modify any images or production files.
"""
import csv
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r"D:\HarvestHand")
from PIL import Image

ROOT = r"D:\HarvestHand\data\card_samples"
OUT_CSV = r"D:\HarvestHand\dataset_inventory.csv"

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def capture_session_from_name(name):
    """Extract a session identifier from the filename if possible.

    Existing files follow IMG_YYYYMMDD_HHMMSS.jpg, where the date
    portion (YYYYMMDD) is the best available session proxy.
    Returns None if no date pattern is found.
    """
    stem = Path(name).stem
    parts = stem.split("_")
    if len(parts) >= 2 and parts[0] == "IMG" and len(parts[1]) == 8:
        try:
            datetime.strptime(parts[1], "%Y%m%d")
            return parts[1]
        except ValueError:
            return None
    return None


def main():
    rows = []
    seen_hashes = {}

    for class_dir in sorted(os.listdir(ROOT)):
        class_path = os.path.join(ROOT, class_dir)
        if not os.path.isdir(class_path):
            continue

        # Class label comes from the folder name (sample_folder in registry).
        class_label = class_dir

        for name in sorted(os.listdir(class_path)):
            if not name.lower().endswith(IMAGE_EXTS):
                continue
            path = os.path.join(class_path, name)

            try:
                im = Image.open(path)
                width, height = im.size
                mode = im.mode
            except Exception as exc:
                print(f"  WARNING: cannot read {path}: {exc}")
                width = height = None
                mode = None

            try:
                mtime = os.path.getmtime(path)
                mtime_iso = datetime.fromtimestamp(mtime).isoformat()
            except OSError:
                mtime_iso = None

            digest = file_hash(path)
            session = capture_session_from_name(name)
            if session is None:
                session = "unknown"

            # Duplicate detection: flag if hash seen before.
            dup_of = None
            if digest in seen_hashes:
                dup_of = seen_hashes[digest]
            else:
                seen_hashes[digest] = path

            rows.append({
                "filename": name,
                "class_label": class_label,
                "path": path,
                "width": width,
                "height": height,
                "mode": mode,
                "file_hash": digest,
                "mtime": mtime_iso,
                "capture_session": session,
                "duplicate_of": dup_of if dup_of else "",
                "dataset_membership": "existing",
            })

    # Write inventory.
    fieldnames = [
        "filename", "class_label", "path", "width", "height", "mode",
        "file_hash", "mtime", "capture_session", "duplicate_of",
        "dataset_membership",
    ]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    # Summary.
    total = len(rows)
    by_class = {}
    by_session = {}
    for r in rows:
        by_class[r["class_label"]] = by_class.get(r["class_label"], 0) + 1
        by_session[r["capture_session"]] = by_session.get(r["capture_session"], 0) + 1
    dups = sum(1 for r in rows if r["duplicate_of"])

    print(f"Dataset inventory written to {OUT_CSV}")
    print(f"Total images: {total}")
    print(f"By class: {by_class}")
    print(f"By capture session: {by_session}")
    print(f"Exact duplicates (by hash): {dups}")


if __name__ == "__main__":
    main()
