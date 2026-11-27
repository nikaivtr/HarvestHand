import unittest
from unittest.mock import patch

import pygame

from cardscan import features, preprocess
from cardscan.scanner import CardScanner, ScanResult
from cardscan.targeted_verification import identify_best


def _model():
    return {
        "feature_version": features.PREPROCESS_VERSION,
        "mean": [0.0, 0.0],
        "cards": {
            "natural_pesticide": {"samples": [[1.0, 0.0]]},
            "water": {"samples": [[0.0, 1.0]]},
        },
    }


class _Camera:
    def read(self):
        return pygame.Surface((640, 480))


class ActionChallengeScanningTests(unittest.TestCase):
    def test_best_class_identity_is_not_forced_to_expected_card(self):
        model = _model()
        thresholds = {
            "classes": {
                "natural_pesticide": {"threshold": 0.8},
                "water": {"threshold": 0.8},
            }
        }

        result = identify_best(model, [0.98, 0.02], thresholds)

        self.assertEqual(result["slug"], "natural_pesticide")
        self.assertTrue(result["accepted"])

        result = identify_best(model, [0.02, 0.98], thresholds)

        self.assertEqual(result["slug"], "water")
        self.assertTrue(result["accepted"])

        result = identify_best(model, [0.7, 0.7], thresholds)

        self.assertFalse(result["accepted"])

    def test_action_scan_uses_multiclass_fallback_without_marker(self):
        model = _model()
        scanner = CardScanner(model_data=model, confirm_frames=1)
        scanner.start(
            "AC-04A Natural Pesticide Card",
            expected_card="natural_pesticide",
        )
        scanner.cam = _Camera()
        canvas = pygame.Surface((160, 240))
        details = {
            "source": "detected",
            "blurry": False,
            "area_ratio": 0.5,
            "quality": 0.8,
            "edge_support": 0.1,
            "aspect": 0.66,
            "points": None,
        }

        with (
            patch.object(
                preprocess,
                "prepare_candidates",
                return_value=[(canvas, details)],
            ),
            patch.object(features, "extract_card", return_value=[0.98, 0.02]),
        ):
            slug, _, confident = scanner.read_once()

        self.assertEqual(slug, "natural_pesticide")
        self.assertTrue(confident)
        self.assertEqual(scanner.last_read["strategy"], "multiclass")

    def test_action_scan_reports_wrong_card_from_visual_fallback(self):
        model = _model()
        scanner = CardScanner(model_data=model, confirm_frames=1)
        scanner.start(
            "AC-04A Natural Pesticide Card",
            expected_card="natural_pesticide",
        )
        scanner.cam = _Camera()
        canvas = pygame.Surface((160, 240))
        details = {
            "source": "detected",
            "blurry": False,
            "area_ratio": 0.5,
            "quality": 0.8,
            "edge_support": 0.1,
            "aspect": 0.66,
            "points": None,
        }

        with (
            patch.object(
                preprocess,
                "prepare_candidates",
                return_value=[(canvas, details)],
            ),
            patch.object(features, "extract_card", return_value=[0.02, 0.98]),
        ):
            result = scanner.update(1.0)

        self.assertEqual(result.status, ScanResult.WRONG)
        self.assertEqual(result.card, "water")


if __name__ == "__main__":
    unittest.main()
