"""State-machine tests for detector-assisted movement and reacquisition."""

import json
import sys
from pathlib import Path

import cv2
import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import live_full_card_detector as detector  # noqa: E402


def candidate(points):
    return {"points": np.asarray(points, dtype=np.float32), "metrics": {"valid": True}}


def translated(points, dx, dy):
    return np.asarray(points, dtype=np.float32) + np.array([dx, dy], dtype=np.float32)


def run_case(name, positions, flow_positions):
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    frame_index = 0
    original_detect = detector.detect

    def fake_detect(_image, _reference_points=None, fast=False):
        points = positions[frame_index]
        selected = None if points is None else candidate(points)
        return {
            "status": "detected" if selected is not None else "lost",
            "reason": "synthetic motion test",
            "candidates": [] if selected is None else [selected],
            "selected": selected,
        }

    detector.detect = fake_detect
    tracker = detector.FullCardTracker()
    statuses = []
    errors = []
    stale_frames = 0
    try:
        for frame_index in range(len(positions)):
            result = tracker.update(image)
            statuses.append(result["status"])
            tracked = result.get("tracked_points")
            target = positions[frame_index]
            if tracked is not None and target is not None:
                errors.append(float(np.mean(np.linalg.norm(tracked - target, axis=1))))
            if tracked is not None and target is None:
                stale_frames += 1
            if flow_positions[frame_index] is None:
                tracker._forward_backward = lambda _gray: None
            else:
                flow = np.asarray(flow_positions[frame_index], dtype=np.float32)
                tracker._forward_backward = lambda _gray, flow=flow: flow.copy()
    finally:
        detector.detect = original_detect

    verified_indices = [
        index
        for index, status in enumerate(statuses)
        if status == "TRACKING"
    ]
    reacquisition_start = next(
        (
            index
            for index, status in enumerate(statuses)
            if status == "REACQUIRING"
            and any(previous < index for previous in verified_indices)
            and index > min(verified_indices, default=-1)
        ),
        None,
    )
    reacquisition_end = (
        next(
            (
                index
                for index in range(reacquisition_start, len(statuses))
                if statuses[index] == "TRACKING"
            ),
            None,
        )
        if reacquisition_start is not None
        else None
    )
    return {
        "case": name,
        "frames": len(positions),
        "statuses": statuses,
        "max_tracking_error_px": max(errors) if errors else None,
        "verified_at_end": statuses[-1] == "TRACKING",
        "stale_boundary_frames": stale_frames,
        "false_locks": sum(
            status == "TRACKING" and target is None
            for status, target in zip(statuses, positions)
        ),
        "acquisition_frames_after_disruption": (
            reacquisition_end - reacquisition_start + 1
            if reacquisition_start is not None and reacquisition_end is not None
            else None
        ),
    }


def main():
    base = np.array([[180, 120], [300, 100], [320, 300], [160, 320]], dtype=np.float32)
    cases = []

    stationary = [base.copy() for _ in range(8)]
    cases.append(run_case("stationary", stationary, stationary))

    slow_horizontal = [translated(base, index * 6, 0) for index in range(8)]
    cases.append(run_case("slow_horizontal", slow_horizontal, slow_horizontal))

    slow_vertical = [translated(base, 0, index * 5) for index in range(8)]
    cases.append(run_case("slow_vertical", slow_vertical, slow_vertical))

    sudden_horizontal = [base.copy() for _ in range(5)] + [
        translated(base, 180, 0) for _ in range(5)
    ]
    sudden_flow = [base.copy() for _ in range(5)] + [base.copy()] + [
        translated(base, 180, 0) for _ in range(4)
    ]
    cases.append(run_case("sudden_horizontal", sudden_horizontal, sudden_flow))

    sudden_vertical = [base.copy() for _ in range(5)] + [
        translated(base, 0, 120) for _ in range(5)
    ]
    sudden_vertical_flow = [base.copy() for _ in range(5)] + [base.copy()] + [
        translated(base, 0, 120) for _ in range(4)
    ]
    cases.append(run_case("sudden_vertical", sudden_vertical, sudden_vertical_flow))

    sudden_diagonal = [base.copy() for _ in range(5)] + [
        translated(base, 150, 100) for _ in range(5)
    ]
    sudden_diagonal_flow = [base.copy() for _ in range(5)] + [base.copy()] + [
        translated(base, 150, 100) for _ in range(4)
    ]
    cases.append(run_case("sudden_diagonal", sudden_diagonal, sudden_diagonal_flow))

    rotated = []
    for angle in np.linspace(0, 12, 8):
        radians = np.deg2rad(angle)
        rotation = np.array(
            [[np.cos(radians), -np.sin(radians)], [np.sin(radians), np.cos(radians)]],
            dtype=np.float32,
        )
        rotated.append((base - base.mean(axis=0)) @ rotation.T + base.mean(axis=0))
    cases.append(run_case("rotation_while_moving", rotated, rotated))

    leaving = [base.copy() for _ in range(5)] + [None, None] + [
        translated(base, 220, 80) for _ in range(5)
    ]
    returning_flow = [base.copy() for _ in range(5)] + [None, None] + [
        translated(base, 220, 80) for _ in range(5)
    ]
    cases.append(run_case("leave_and_return_elsewhere", leaving, returning_flow))

    for name, missing_count, offset in (
        ("partial_outside_frame", 2, (0, 0)),
        ("obstruction", 3, (0, 0)),
        ("face_or_unrelated_object", 4, (0, 0)),
        ("brief_disappearance", 1, (0, 0)),
        ("absent_for_several_seconds", 10, (0, 0)),
    ):
        returning = translated(base, *offset)
        positions = [base.copy() for _ in range(5)] + [None] * missing_count + [
            returning.copy() for _ in range(5)
        ]
        flow = [base.copy() for _ in range(5)] + [None] * missing_count + [
            returning.copy() for _ in range(5)
        ]
        cases.append(run_case(name, positions, flow))

    print(json.dumps(cases, indent=2))


if __name__ == "__main__":
    main()
