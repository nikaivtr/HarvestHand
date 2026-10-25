"""
ResultsScreen — level-completion, victory, and time-up overlays.
"""

import pygame

from . import assets_config as AC


class ResultsScreen:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.font_title = None
        self.font_body = None
        self.font_small = None
        self.active = False
        self.mode = None            # "complete", "victory", "timeup"
        self.score = 0
        self.level = 1
        self.time_bonus = 0
        self.buttons = {}
        self.continue_label = "Continue Story"
        self._make_fonts(height)

    def _make_fonts(self, height):
        try:
            self.font_title = pygame.font.Font(AC.FONT_PATH, max(24, int(height * 0.055)))
            self.font_body = pygame.font.Font(AC.FONT_PATH, max(20, int(height * 0.032)))
            self.font_small = pygame.font.Font(AC.FONT_PATH, max(16, int(height * 0.026)))
        except pygame.error:
            self.font_title = pygame.font.SysFont("Georgia", max(24, int(height * 0.055)), bold=True)
            self.font_body = pygame.font.SysFont("Georgia", max(20, int(height * 0.032)), bold=True)
            self.font_small = pygame.font.SysFont("Georgia", max(16, int(height * 0.026)), bold=True)

    def resize(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self._make_fonts(height)

    def show(self, mode, level, score, time_bonus=0):
        self.active = True
        self.mode = mode
        self.level = level
        self.score = score
        self.time_bonus = time_bonus
        self._build_buttons()

    def hide(self):
        self.active = False

    def _build_buttons(self):
        self.buttons = {}
        pw = int(self.WIDTH * 0.42)
        bh = int(self.HEIGHT * 0.075)
        gap = int(self.HEIGHT * 0.03)
        total_w = pw * 2 + gap
        start_x = (self.WIDTH - total_w) // 2
        start_y = int(self.HEIGHT * 0.62)

        if self.mode == "timeup":
            self.buttons["retry"] = pygame.Rect(start_x, start_y, pw, bh)
            self.buttons["menu"] = pygame.Rect(start_x + pw + gap, start_y, pw, bh)
        elif self.mode == "victory":
            self.buttons["continue_story"] = pygame.Rect(start_x, start_y, pw, bh)
            self.buttons["menu"] = pygame.Rect(start_x + pw + gap, start_y, pw, bh)

        else:  # complete
            self.buttons["next"] = pygame.Rect(start_x, start_y, pw, bh)
            self.buttons["menu"] = pygame.Rect(start_x + pw + gap, start_y, pw, bh)

    def draw(self, surf):
        if not self.active:
            return

        # Shade background
        shade = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        shade.fill((23, 41, 20, 185))
        surf.blit(shade, (0, 0))

        # Panel
        panel = pygame.Rect(
            int(self.WIDTH * 0.16),
            int(self.HEIGHT * 0.24),
            int(self.WIDTH * 0.68),
            int(self.HEIGHT * 0.42),
        )
        pygame.draw.rect(surf, AC.PALETTE["cream"], panel, border_radius=28)
        pygame.draw.rect(surf, AC.PALETTE["panel_border"], panel, width=5, border_radius=28)

        # Title
        if self.mode == "victory":
            title = "Level Complete! — All Ingredients Ready!"
        elif self.mode == "timeup":
            title = "Time's Up!"
        else:
            title = f"Level {self.level} Complete!"

        title_surf = self.font_title.render(title, True, AC.PALETTE["deep_green"])
        surf.blit(title_surf, title_surf.get_rect(center=(self.WIDTH // 2, int(self.HEIGHT * 0.36))))

        # Score
        score_text = f"Score: {self.score}"
        if self.time_bonus:
            score_text += f"  (+{self.time_bonus} time bonus)"
        score_surf = self.font_body.render(score_text, True, AC.PALETTE["ink"])
        surf.blit(score_surf, score_surf.get_rect(center=(self.WIDTH // 2, int(self.HEIGHT * 0.46))))

        # Detail
        if self.mode == "timeup":
            detail = "The clock ran out before all ingredients were assembled."
        elif self.mode == "victory":
            detail = "Congratulations! You reconstructed every ingredient."
        else:
            detail = f"Ingredients assembled. Get ready for the next challenge."
        detail_surf = self.font_body.render(detail, True, AC.PALETTE["ink"])
        surf.blit(detail_surf, detail_surf.get_rect(center=(self.WIDTH // 2, int(self.HEIGHT * 0.52))))

        # Buttons
        for key, rect in self.buttons.items():
            label = {
                "next": "Next Level",
                "retry": "Retry Level",
                "menu": "Main Menu",
                "continue_story": self.continue_label,
            }[key]

            color = AC.PALETTE["green"] if key in ("next", "retry", "continue_story") else AC.PALETTE["deep_green"]
            self._draw_button(surf, rect, label, color)

    def _draw_button(self, surf, rect, label, color):
        shadow = rect.move(0, 4)
        pygame.draw.rect(surf, (38, 32, 23), shadow, border_radius=16)
        pygame.draw.rect(surf, color, rect, border_radius=16)
        pygame.draw.rect(surf, (255, 244, 207), rect, width=2, border_radius=16)
        txt = self.font_body.render(label, True, (255, 255, 255))
        surf.blit(txt, txt.get_rect(center=rect.center))

    def handle_tap(self, pos):
        if not self.active:
            return None
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return key
        return None
