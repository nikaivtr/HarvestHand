#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required. Install it with: sudo apt install python3" >&2
    exit 1
fi

if ! python3 -c "import pygame; import cv2" >/dev/null 2>&1; then
    echo "Game dependencies are missing. Run: bash install_raspberry_pi.sh" >&2
    exit 1
fi

exec python3 main.py
