# Running Harvest Hand on Raspberry Pi

Harvest Hand is a Python/Pygame game, so it runs on Raspberry Pi OS as source
code rather than as a Windows `.exe`. Keep the complete project folder together:
the game needs the `img`, `data`, `scenes`, `story`, `popups`, and `minigames`
folders as well as `main.py`.

## Install

1. Copy or clone the complete Harvest Hand project onto a Raspberry Pi running
   Raspberry Pi OS with its desktop environment.
2. Open a terminal in the project folder and run:

   ```bash
   bash install_raspberry_pi.sh
   ```

   The installer uses `apt` to install Python 3, Pygame, and OpenCV (used for
   live card scanning), then verifies the Python imports. It works when run as
   root or through `sudo`.

## Start the game

From the project folder, run:

```bash
./run_raspberry_pi.sh
```

If the executable permission was not preserved while copying the files, use:

```bash
bash run_raspberry_pi.sh
```

The game opens fullscreen. Press **Esc** to exit. A desktop session is required
because the game creates a Pygame display window.
