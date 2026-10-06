# ============================================================
#  capture_samples.py
#
#  Grabs training photos from the live camera straight into
#  data/card_samples/<card>/. This is the "teach the system the
#  cards" tool for the Raspberry Pi.
#
#  Usage:
#      python tools/capture_samples.py --card water
#      python tools/capture_samples.py --card water --count 20
#      python tools/capture_samples.py --card water --device 1
#
#  Press SPACE to shoot, Q or ESC to stop. Shoot the same card
#  from a few angles and distances - that variety is what makes
#  recognition steady later.
# ============================================================

import argparse
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

import cardscan.camera as camera
import cardscan.registry as registry


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, "data", "card_samples")

HELP = [
    "SPACE  shoot a photo",
    "Q/ESC  quit",
]


def draw_hud(surf, card, shots, count):
    w, h = surf.get_size()
    fonts = [
        pygame.font.SysFont(None, int(h * 0.030)),
        pygame.font.SysFont(None, int(h * 0.042)),
        pygame.font.SysFont(None, int(h * 0.024)),
    ]
    small, big, tiny = fonts

    band = pygame.Surface((w, int(h * 0.13)), pygame.SRCALPHA)
    band.fill((0, 0, 0, 150))
    surf.blit(band, (0, 0))

    l1 = big.render(f"Capturing: {card.display}", True, (255, 220, 90))
    surf.blit(l1, l1.get_rect(midtop=(w // 2, int(h * 0.022))))

    l2 = small.render(f"{shots}/{count} photos saved", True, (230, 230, 230))
    surf.blit(l2, l2.get_rect(midtop=(w // 2, int(h * 0.072))))

    l3 = tiny.render("  |  ".join(HELP), True, (170, 170, 170))
    surf.blit(l3, l3.get_rect(midtop=(w // 2, int(h * 0.104))))

    # A box showing what the recogniser actually looks at, so the
    # player can see the card is where it needs to be.
    side = int(min(w, h) * 0.86)
    box = pygame.Rect(0, 0, side, side)
    box.center = (w // 2, h // 2)
    pygame.draw.rect(surf, (120, 220, 120), box, width=3, border_radius=8)


def main():
    ap = argparse.ArgumentParser(description="Capture card sample photos")
    ap.add_argument("--card", required=True,
                    help="card slug, e.g. water")
    ap.add_argument("--count", type=int, default=10,
                    help="photos to take (default 10)")
    ap.add_argument("--device", type=int, default=0, help="camera index")
    ap.add_argument("--out", default=None, help="output folder override")
    args = ap.parse_args()

    card = registry.get(args.card)
    if card is None:
        print(f"unknown card '{args.card}'")
        print("known slugs:", ", ".join(registry.slugs()))
        return 1

    out_dir = args.out or os.path.join(SAMPLES, card.slug)
    os.makedirs(out_dir, exist_ok=True)

    pygame.init()
    screen = pygame.display.set_mode((960, 720))
    pygame.display.set_caption(f"Harvest Hand - capture {card.slug}")

    try:
        cam = camera.open_camera("opencv", device=args.device)
    except camera.CameraError as exc:
        print(f"camera problem: {exc}")
        print("on a Pi also check:  sudo raspi-config  -> Interface -> Camera")
        return 1

    clock = pygame.time.Clock()
    shots = 0
    print(f"saving to {out_dir}")
    print("  " + " | ".join(HELP))

    while shots < args.count:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                cam.release()
                return 0
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_q, pygame.K_ESCAPE):
                cam.release()
                print(f"done: {shots} photos")
                return 0
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                frame = cam.read()
                if frame is None:
                    print("  (no frame, skipped)")
                    continue
                stamp = datetime.now().strftime("%H%M%S_%f")[:-3]
                path = os.path.join(out_dir, f"{card.slug}_{stamp}.jpg")
                pygame.image.save(frame, path)
                shots += 1
                print(f"  {shots}/{args.count}  {os.path.basename(path)}")

        frame = cam.read()
        if frame is None:
            screen.fill((25, 25, 32))
            msg = pygame.font.SysFont(None, 34).render(
                "waiting for camera...", True, (200, 200, 200))
            screen.blit(msg, msg.get_rect(center=(480, 360)))
        else:
            screen.blit(pygame.transform.smoothscale(frame, screen.get_size()), (0, 0))
            draw_hud(screen, card, shots, args.count)

        pygame.display.flip()
        clock.tick(30)

    cam.release()
    print(f"done: {shots} photos -> {out_dir}")
    print("now run:  python tools/train_cards.py --report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
