import sys

import pygame

from scenes import main_menu, level_select, story_mode

pygame.init()

# ── Window ────────────────────────────────────────────────────────────────────
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption("Harvest Hand")
clock = pygame.time.Clock()

# ── Enable touch events ───────────────────────────────────────────────────────
pygame.event.set_allowed([
    pygame.QUIT,
    pygame.KEYDOWN,
    pygame.MOUSEBUTTONDOWN,
    pygame.MOUSEBUTTONUP,
    pygame.MOUSEMOTION,
    pygame.FINGERDOWN,
    pygame.FINGERUP,
    pygame.FINGERMOTION,
])

# ── Scene manager ─────────────────────────────────────────────────────────────
# Every scene module exposes the same contract: init(), handle_tap(), draw().
SCENES = {
    "main_menu": main_menu,
    "level_select": level_select,
    "story_mode": story_mode,
}
current_scene = "main_menu"


def go_to_scene(scene_name):
    global current_scene
    current_scene = scene_name


for scene in SCENES.values():
    scene.init(WIDTH, HEIGHT, go_to_scene)

# ── Single-touch lock ─────────────────────────────────────────────────────────
active_finger = None


def _call(method, *args):
    """Call an optional method on the current scene if it exists."""
    scene = SCENES[current_scene]
    fn = getattr(scene, method, None)
    if fn:
        fn(*args)


# ── Main loop ─────────────────────────────────────────────────────────────────
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()

        if event.type == pygame.FINGERDOWN:
            if active_finger is None:
                active_finger = event.finger_id
                _call("handle_tap", int(event.x * WIDTH), int(event.y * HEIGHT))

        if event.type == pygame.FINGERMOTION:
            if event.finger_id == active_finger:
                _call("handle_drag", int(event.x * WIDTH), int(event.y * HEIGHT))

        if event.type == pygame.FINGERUP:
            if event.finger_id == active_finger:
                _call("handle_release", int(event.x * WIDTH), int(event.y * HEIGHT))
                active_finger = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if active_finger is None:
                _call("handle_tap", *event.pos)

        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if active_finger is None:
                _call("handle_drag", *event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if active_finger is None:
                _call("handle_release", *event.pos)

    SCENES[current_scene].draw(screen)
    pygame.display.flip()
    clock.tick(60)
