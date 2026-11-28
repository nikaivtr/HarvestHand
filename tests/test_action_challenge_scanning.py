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

    def test_action_scan_waits_for_marker_without_image_fallback(self):
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
            ) as prepare_candidates,
            patch.object(features, "extract_card") as extract,
        ):
            result = scanner.update(1.0)

        self.assertIsNone(result)
        self.assertEqual(
            scanner.last_read["reason"],
            "action card ArUco marker not detected",
        )
        self.assertFalse(prepare_candidates.call_args.kwargs["fast_marker"])
        extract.assert_not_called()

    def test_action_scan_rejects_marker_for_wrong_expected_card(self):
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
            "marker_identity_only": True,
            "marker_slug": "water",
            "marker_id": 11,
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
            patch.object(features, "extract_card") as extract,
        ):
            result = scanner.update(1.0)

        self.assertEqual(result.status, ScanResult.WRONG)
        self.assertEqual(result.card, "water")
        self.assertEqual(scanner.last_read["marker_id"], 11)
        extract.assert_not_called()

    def test_action_marker_accepts_expected_card_without_model_class(self):
        model = {
            "feature_version": features.PREPROCESS_VERSION,
            "mean": [0.0, 0.0],
            "cards": {
                "water": {"samples": [[0.0, 1.0]]},
                "weed": {"samples": [[1.0, 0.0]]},
            },
        }
        scanner = CardScanner(model_data=model, confirm_frames=1)
        scanner.start(
            "AC-04A Natural Pesticide Card",
            expected_card="natural_pesticide",
        )
        scanner.cam = _Camera()
        details = {
            "source": "detected",
            "marker_identity_only": True,
            "marker_slug": "natural_pesticide",
            "marker_id": 15,
            "blurry": False,
            "area_ratio": 0.5,
            "quality": 0.8,
            "edge_support": 0.1,
            "aspect": 0.66,
        }

        with (
            patch.object(
                preprocess,
                "prepare_candidates",
                return_value=[(pygame.Surface((160, 240)), details)],
            ) as prepare_candidates,
            patch.object(features, "extract_card") as extract,
        ):
            result = scanner.update(0.1)

        self.assertEqual(result.status, ScanResult.MATCH)
        self.assertEqual(result.card, "natural_pesticide")
        self.assertFalse(prepare_candidates.call_args.kwargs["fast_marker"])
        extract.assert_not_called()


if __name__ == "__main__":
    unittest.main()
