import time
import unittest

import pygame

from scenes import story_mode


class StorySaveControlTests(unittest.TestCase):
    def test_draws_save_status_with_valid_font_size(self):
        pygame.font.init()
        previous = (
            story_mode.WIDTH,
            story_mode.HEIGHT,
            story_mode._chapter_done,
            story_mode._save_status,
            story_mode._save_status_until,
        )
        try:
            story_mode.WIDTH = 1280
            story_mode.HEIGHT = 720
            story_mode._chapter_done = False
            story_mode._save_status = "Progress saved."
            story_mode._save_status_until = time.monotonic() + 1

            story_mode._draw_chapter_exit(
                pygame.Surface((1280, 720)),
                include_save=True,
            )
        finally:
            (
                story_mode.WIDTH,
                story_mode.HEIGHT,
                story_mode._chapter_done,
                story_mode._save_status,
                story_mode._save_status_until,
            ) = previous


if __name__ == "__main__":
    unittest.main()
