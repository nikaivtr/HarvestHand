import unittest
from types import SimpleNamespace
from unittest.mock import patch

import pygame

import game_state
from cardscan import registry as card_registry
from scenes import story_mode


class _CaptureFont:
    def __init__(self):
        self.labels = []

    def render(self, text, antialias, color):
        self.labels.append(text)
        return pygame.Surface((max(1, len(text) * 8), 18))


class ActionGaugeUsageTests(unittest.TestCase):
    def setUp(self):
        self._previous = {
            name: getattr(story_mode, name)
            for name in (
                "WIDTH",
                "HEIGHT",
                "_engine",
                "_gauge_remaining",
                "_gauge_totals",
                "_gauge_visible",
                "_gauge_used",
                "_font_hint",
                "_chapter_done",
            )
        }
        for name in (
            "_gauge_remaining",
            "_gauge_totals",
            "_gauge_visible",
            "_gauge_used",
        ):
            self._previous[name] = dict(self._previous[name])
        story_mode._gauge_remaining = {
            gauge: 2 for gauge in story_mode._GAUGE_ORDER
        }
        story_mode._gauge_totals = {
            gauge: 2 for gauge in story_mode._GAUGE_ORDER
        }
        story_mode._gauge_visible = {
            gauge: False for gauge in story_mode._GAUGE_ORDER
        }
        story_mode._gauge_used = {
            gauge: 0 for gauge in story_mode._GAUGE_ORDER
        }
        story_mode._chapter_done = False

    def tearDown(self):
        for name, value in self._previous.items():
            setattr(story_mode, name, value)

    def test_scanned_action_cards_increment_their_meter_usage(self):
        expected_gauges = {
            "water": "water",
            "organic_fertilizer": "fertilizer",
            "chemical_fertilizer": "fertilizer",
            "weed": "weeds",
            "natural_pesticide": "pests",
            "chemical_pesticide": "pests",
        }
        with patch("scenes.story_mode.player_data.record_challenge_success"):
            for card_slug, gauge in expected_gauges.items():
                with self.subTest(card=card_slug):
                    story_mode._gauge_used = {
                        key: 0 for key in story_mode._GAUGE_ORDER
                    }
                    story_mode._gauge_visible = {
                        key: False for key in story_mode._GAUGE_ORDER
                    }
                    story_mode._engine = SimpleNamespace(slide={
                        "type": "action_challenge",
                        "card": card_registry.get(card_slug).display,
                    })

                    story_mode._record_action_success()

                    self.assertEqual(story_mode._gauge_used[gauge], 1)
                    self.assertTrue(story_mode._gauge_visible[gauge])

    def test_water_meter_tracks_uses_instead_of_draining(self):
        pygame.init()
        story_mode.WIDTH = 1280
        story_mode.HEIGHT = 720
        story_mode._engine = SimpleNamespace(popup_open=None)
        story_mode._gauge_visible = {
            "water": True,
            "fertilizer": True,
            "pests": False,
            "weeds": False,
        }
        story_mode._gauge_used = {
            "water": 1,
            "fertilizer": 1,
            "pests": 0,
            "weeds": 0,
        }
        story_mode._gauge_totals["water"] = 2
        story_mode._gauge_totals["fertilizer"] = 2
        capture_font = _CaptureFont()
        story_mode._font_hint = capture_font

        with patch.object(
            story_mode,
            "_get_gauge_icon",
            return_value=pygame.Surface((36, 36)),
        ):
            story_mode._draw_water_bar(pygame.Surface((1280, 720)))

        self.assertIn("Watering can used 1/2", capture_font.labels)
        self.assertIn("Fertilizer used 1/2", capture_font.labels)
        self.assertEqual(story_mode._gauge_used["water"], 1)

    def test_water_requirement_comes_from_chapter_action_challenges(self):
        import data.chapters as chapters_data

        chapter = chapters_data.load("ch02_monggo")
        prepared, totals = story_mode._prepare_chapter(chapter)
        expected = sum(
            1
            for slide in prepared["slides"]
            if slide.get("type") == "action_challenge"
            and story_mode._ACTION_GAUGE_BY_SLUG.get(
                story_mode._action_kind(slide)
            ) == "water"
        )

        self.assertGreater(expected, 0)
        self.assertEqual(totals["water"], expected)

    def test_usage_counts_are_included_in_saved_chapter_checkpoint(self):
        story_mode._engine = SimpleNamespace(
            snapshot_state=lambda: {"slide_idx": 2}
        )
        story_mode._chapter_done = False
        story_mode._gauge_used = {
            "water": 1,
            "fertilizer": 2,
            "pests": 0,
            "weeds": 1,
        }
        captured = {}
        previous_chapter = game_state.selected_chapter
        game_state.selected_chapter = "ch01_pechay"
        try:
            with (
                patch(
                    "scenes.story_mode.player_data.current_profile",
                    return_value={"id": "test-player"},
                ),
                patch(
                    "scenes.story_mode.player_data.save_chapter_progress",
                    side_effect=lambda checkpoint: captured.update(checkpoint) or True,
                ),
            ):
                self.assertTrue(story_mode._save_current_progress())
        finally:
            game_state.selected_chapter = previous_chapter

        self.assertEqual(captured["gauge_used"], story_mode._gauge_used)


if __name__ == "__main__":
    unittest.main()
