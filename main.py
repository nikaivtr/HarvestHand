import sys

import pygame

import audio_manager
import game_state
import player_data
from scenes import main_menu, level_select, story_mode, memory_game
from minigames.ingredient_puzzle import scene as ingredient_puzzle
from minigames import whack_a_pest
from minigames import tomato_seed_extraction
from popups import score_prompt

pygame.init()

# ── Window ────────────────────────────────────────────────────────────────────
_settings = player_data.get_settings()
if _settings["fullscreen"]:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
else:
    display_info = pygame.display.Info()
    window_size = (min(1280, display_info.current_w), min(720, display_info.current_h))
    screen = pygame.display.set_mode(window_size)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Harvest Hand")
clock = pygame.time.Clock()
audio_manager.start_music(_settings)

# ── Enable touch events ───────────────────────────────────────────────────────
pygame.event.set_allowed([
    pygame.QUIT,
    pygame.KEYDOWN,
    pygame.TEXTINPUT,
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
    "memory_game": memory_game,
    "ingredient_puzzle": ingredient_puzzle,
    "whack_a_pest": whack_a_pest,
    "tomato_seed_extraction": tomato_seed_extraction,
}
current_scene = "main_menu"


def go_to_scene(scene_name):
    global current_scene
    current_scene = scene_name


def _apply_display_mode(fullscreen):
    global screen, WIDTH, HEIGHT
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
    else:
        display_info = pygame.display.Info()
        window_size = (min(1280, display_info.current_w), min(720, display_info.current_h))
        screen = pygame.display.set_mode(window_size)
    WIDTH, HEIGHT = screen.get_size()
    for scene in SCENES.values():
        scene.init(WIDTH, HEIGHT, go_to_scene)
    score_prompt.init(WIDTH, HEIGHT)
    main_menu.set_display_change_callback(_apply_display_mode)


for scene in SCENES.values():
    scene.init(WIDTH, HEIGHT, go_to_scene)
score_prompt.init(WIDTH, HEIGHT)
main_menu.set_display_change_callback(_apply_display_mode)

# ── Single-touch lock ─────────────────────────────────────────────────────────
active_finger = None
skip_next_release = False


def _call(method, *args):
    """Call an optional method on the current scene if it exists."""
    scene = SCENES[current_scene]
    fn = getattr(scene, method, None)
    if fn:
        fn(*args)


def _try_chapter_exit_tap(px, py):
    global skip_next_release
    if story_mode.handle_chapter_exit_tap(px, py):
        story_mode.exit_chapter()
        skip_next_release = True
        return True
    return False


def _handle_tap(px, py):
    if score_prompt.active():
        score_prompt.handle_tap(px, py)
        return
    if _try_chapter_exit_tap(px, py):
        return
    _call("handle_tap", px, py)


def _handle_release(px, py):
    if not score_prompt.active():
        _call("handle_release", px, py)


def _handle_drag(px, py):
    if not score_prompt.active():
        _call("handle_drag", px, py)


# ── Main loop ─────────────────────────────────────────────────────────────────
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.TEXTINPUT and score_prompt.active():
            score_prompt.handle_event(event)
            continue

        if event.type == pygame.KEYDOWN and score_prompt.active():
            score_prompt.handle_event(event)
            continue

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            chapter_scene = current_scene not in ("main_menu", "level_select")
            if game_state.selected_chapter is not None and chapter_scene:
                story_mode.exit_chapter()
            else:
                pygame.quit(); sys.exit()

        if event.type == pygame.FINGERDOWN:
            if active_finger is None:
                active_finger = event.finger_id
                _handle_tap(int(event.x * WIDTH), int(event.y * HEIGHT))
            else:
                px, py = int(event.x * WIDTH), int(event.y * HEIGHT)
                if score_prompt.active():
                    score_prompt.handle_tap(px, py)
                elif not _try_chapter_exit_tap(px, py):
                    _call("handle_additional_tap", px, py)

        if event.type == pygame.FINGERMOTION:
            if event.finger_id == active_finger:
                _handle_drag(int(event.x * WIDTH), int(event.y * HEIGHT))

        if event.type == pygame.FINGERUP:
            if event.finger_id == active_finger:
                if not skip_next_release:
                    _handle_release(int(event.x * WIDTH), int(event.y * HEIGHT))
                skip_next_release = False
                active_finger = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if active_finger is None:
                _handle_tap(*event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if active_finger is None and not score_prompt.active():
                fn = getattr(SCENES[current_scene], "handle_rotate", None)
                if fn:
                    fn(*event.pos)

        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if active_finger is None:
                _handle_drag(*event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if active_finger is None:
                if not skip_next_release:
                    _handle_release(*event.pos)
                skip_next_release = False

        if event.type == pygame.USEREVENT:
            fn = getattr(SCENES[current_scene], "handle_userevent", None)
            if fn:
                fn(event)

    SCENES[current_scene].draw(screen)
    if current_scene != "story_mode":
        story_mode.draw_chapter_exit(screen)
    score_prompt.draw(screen)
    pygame.display.flip()
    clock.tick(60)
