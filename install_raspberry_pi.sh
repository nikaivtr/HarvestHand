#!/usr/bin/env bash
set -euo pipefail

if ! command -v apt-get >/dev/null 2>&1; then
    echo "This installer expects Raspberry Pi OS or another Debian-based system." >&2
    echo "Install Python 3, Pygame, and OpenCV with your distribution's package manager." >&2
    exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -f "$SCRIPT_DIR/main.py" ] || [ ! -d "$SCRIPT_DIR/img" ]; then
    echo "Run this installer from a complete Harvest Hand project folder." >&2
    exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
    APT_GET=(apt-get)
elif command -v sudo >/dev/null 2>&1; then
    APT_GET=(sudo apt-get)
else
    echo "Run this installer as root or install sudo to install system packages." >&2
    exit 1
fi

"${APT_GET[@]}" update
"${APT_GET[@]}" install -y python3 python3-pygame python3-opencv

if ! python3 -c "import pygame; import cv2" >/dev/null 2>&1; then
    echo "Dependency verification failed. Check the package installation output above." >&2
    exit 1
fi

chmod +x "$SCRIPT_DIR/run_raspberry_pi.sh"

echo
echo "Harvest Hand and its Python dependencies are installed. From this folder, start it with:"
echo "  ./run_raspberry_pi.sh"
echo "If you copied the files without preserving permissions, use:"
echo "  bash run_raspberry_pi.sh"
