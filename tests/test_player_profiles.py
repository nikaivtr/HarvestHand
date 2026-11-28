import json
import tempfile
import unittest
from pathlib import Path

import player_data
from story.engine import StoryEngine


class PlayerProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self._data_path = player_data._DATA_PATH
        player_data._DATA_PATH = Path(self.temp_dir.name) / "player_data.json"
        self._reset_state()

    def tearDown(self):
        player_data._DATA_PATH = self._data_path
        self._reset_state()
        self.temp_dir.cleanup()

    @staticmethod
    def _reset_state():
        player_data._data = None
        player_data._current_run = None
        player_data._active_profile_id = None
        player_data._last_error = ""
        player_data._pending_score_records = []
        player_data._score_prompts_deferred = False

    def test_profile_checkpoint_resumes_and_counts_chapter_score_once(self):
        self.assertTrue(player_data.create_profile("Maya"))
        profile_id = player_data.active_profile_id()
        player_data.begin_chapter("ch01_pechay")
        player_data.record_minigame_result("ingredient_puzzle", 500)
        player_data.record_minigame_result("ingredient_puzzle", 250)
        checkpoint = {
            "chapter": "ch01_pechay",
            "engine": {"slide_idx": 4},
            "day": 3,
        }
        self.assertTrue(player_data.save_chapter_progress(checkpoint))
        self.assertEqual(player_data.profile_total_score(), 750)

        self._reset_state()
        self.assertTrue(player_data.select_profile(profile_id))
        saved = player_data.chapter_save("ch01_pechay")
        self.assertEqual(saved["engine"]["slide_idx"], 4)
        self.assertTrue(player_data.resume_chapter("ch01_pechay", saved))
        result = player_data.complete_chapter()

        self.assertEqual(result["minigame_points"], 750)
        self.assertEqual(result["score"], 1750)
        self.assertEqual(player_data.profile_total_score(), 1750)
        self.assertIsNone(player_data.chapter_save())
        self.assertEqual(player_data.chapter_rankings(), [])

    def test_chapter_unlocks_follow_completed_chapter_order(self):
        chapter_ids = ["ch01_pechay", "ch02_monggo", "ch03_okra"]
        self.assertTrue(player_data.create_profile("Kai"))
        self.assertTrue(player_data.chapter_unlocked(chapter_ids[0], chapter_ids))
        self.assertFalse(player_data.chapter_unlocked(chapter_ids[1], chapter_ids))

        player_data.begin_chapter(chapter_ids[0])
        player_data.complete_chapter()
        self.assertTrue(player_data.chapter_unlocked(chapter_ids[1], chapter_ids))
        self.assertFalse(player_data.chapter_unlocked(chapter_ids[2], chapter_ids))

        player_data.begin_chapter(chapter_ids[1])
        player_data.complete_chapter()
        self.assertTrue(player_data.chapter_unlocked(chapter_ids[2], chapter_ids))

    def test_standalone_minigame_score_updates_profile_total(self):
        self.assertTrue(player_data.create_profile("Sam"))
        self.assertTrue(player_data.record_minigame_result("whack_a_pest", 1200))
        self.assertEqual(player_data.profile_total_score(), 1200)
        self.assertEqual(player_data.minigame_rankings(), [])

    def test_existing_global_chapter_progress_migrates_to_legacy_profile(self):
        player_data._DATA_PATH.write_text(
            json.dumps({"completed_chapters": ["ch01_pechay", "ch02_monggo"]}),
            encoding="utf-8",
        )
        player_data._data = None

        profile = player_data.last_profile()

        self.assertEqual(profile["id"], "legacy")
        self.assertEqual(
            profile["completed_chapters"],
            ["ch01_pechay", "ch02_monggo"],
        )
        self.assertTrue(
            player_data.chapter_unlocked(
                "ch03_okra",
                ["ch01_pechay", "ch02_monggo", "ch03_okra"],
            )
        )

    def test_new_profile_does_not_overwrite_existing_name(self):
        self.assertTrue(player_data.create_profile("Robin"))
        first_profile_id = player_data.active_profile_id()

        self.assertFalse(player_data.create_profile("robin"))
        self.assertEqual(player_data.active_profile_id(), first_profile_id)
        self.assertEqual(len(player_data._load()["profiles"]), 1)

    def test_story_engine_restores_branch_and_dialogue_position(self):
        chapter = {
            "slides": [
                {"type": "dialogue", "lines": [("Farmer", "One"), ("Farmer", "Two")]},
                {"type": "choice", "correct": 0, "lines": []},
            ]
        }
        source = StoryEngine(chapter)
        source.slide_idx = 1
        source.line_idx = 0
        source._last_answer = True
        source._retry_slide = 0
        source._skip_slides = {0}
        source.is_retry = True

        restored = StoryEngine(chapter)

        self.assertTrue(restored.restore_state(source.snapshot_state()))
        self.assertEqual(restored.slide_idx, 1)
        self.assertTrue(restored._last_answer)
        self.assertEqual(restored._retry_slide, 0)
        self.assertEqual(restored._skip_slides, {0})
        self.assertTrue(restored.is_retry)

    def test_story_engine_rejects_out_of_range_checkpoint(self):
        engine = StoryEngine({"slides": [{"type": "dialogue", "lines": []}]})

        self.assertFalse(engine.restore_state({"slide_idx": 4}))


if __name__ == "__main__":
    unittest.main()
