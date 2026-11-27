"""Calibrate leave-one-out thresholds for targeted v13 verification."""

import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

MODEL_PATH = os.path.join(
    ROOT, "CardScanner-v13", "cardscan", "card_model.json"
)
THRESHOLD_PATH = os.path.join(ROOT, "cardscan", "target_verification.json")
REPORT_PATH = os.path.join(
    ROOT, "recognition_lab", "reports", "targeted_verification_v13.json"
)
TOP_K = 3
MAX_FALSE_ACCEPT_RATE = 0.01


def normalize(rows):
    rows = np.asarray(rows, dtype=np.float64)
    norms = np.maximum(np.linalg.norm(rows, axis=1, keepdims=True), 1e-12)
    return rows / norms


def top_k_expected_score(expected_samples, query):
    similarities = expected_samples @ query
    return float(np.sort(similarities)[::-1][:TOP_K].mean())


def leave_one_out_positive(samples):
    scores = []
    for index, query in enumerate(samples):
        others = np.delete(samples, index, axis=0)
        scores.append(top_k_expected_score(others, query))
    return np.asarray(scores, dtype=np.float64)


def choose_threshold(positive, negative, false_accept_limit):
    candidates = np.unique(np.concatenate((positive, negative)))
    best = None
    neg_sorted = np.sort(negative)
    pos_sorted = np.sort(positive)
    for threshold in candidates:
        tpr = float(np.searchsorted(pos_sorted, threshold, side="left"))
        tpr = 1.0 - tpr / len(pos_sorted)
        far = 1.0 - np.searchsorted(neg_sorted, threshold, side="left") / len(neg_sorted)
        if far <= false_accept_limit:
            rank = (tpr, -float(threshold))
            if best is None or rank > best[0]:
                best = (rank, float(threshold), tpr, far)
    if best is None:
        threshold = float(np.quantile(negative, 1.0 - false_accept_limit))
        tpr = float((positive >= threshold).mean())
        far = float((negative >= threshold).mean())
    else:
        _, threshold, tpr, far = best
    return threshold, tpr, far


def main():
    with open(MODEL_PATH, "r", encoding="utf-8") as fh:
        model = json.load(fh)
    cards = model["cards"]
    matrices = {
        slug: normalize(entry["samples"])
        for slug, entry in cards.items()
        if entry.get("samples")
    }

    classes = {}
    for expected, expected_samples in matrices.items():
        positive = leave_one_out_positive(expected_samples)
        negative_by_class = {}
        negative = []
        for slug, samples in matrices.items():
            if slug == expected:
                continue
            scores = np.asarray([
                top_k_expected_score(expected_samples, query)
                for query in samples
            ])
            negative_by_class[slug] = {
                "total_test_samples": int(len(scores)),
                "false_acceptances": int((scores >= 0.0).sum()),
            }
            negative.extend(scores.tolist())
        negative = np.asarray(negative, dtype=np.float64)
        threshold, tpr, far = choose_threshold(
            positive, negative, MAX_FALSE_ACCEPT_RATE
        )
        accepted = int((positive >= threshold).sum())
        rejected = int(len(positive) - accepted)
        negative_breakdown = {}
        for slug, scores in [
            (slug, np.asarray([
                top_k_expected_score(expected_samples, query)
                for query in samples
            ]))
            for slug, samples in matrices.items()
            if slug != expected
        ]:
            false_count = int((scores >= threshold).sum())
            negative_breakdown[slug] = {
                "total_test_samples": int(len(scores)),
                "false_acceptances": false_count,
                "false_acceptance_rate": float(false_count / len(scores)),
            }
        classes[expected] = {
            "total_test_samples": int(len(positive)),
            "correctly_accepted_expected_samples": accepted,
            "rejected_expected_samples": rejected,
            "false_acceptances": int((negative >= threshold).sum()),
            "false_acceptance_rate": far,
            "true_acceptance_rate": tpr,
            "threshold": threshold,
            "negative_total": int(len(negative)),
            "negative_breakdown": negative_breakdown,
        }

    all_vectors = []
    all_labels = []
    for slug, matrix in matrices.items():
        all_vectors.extend(matrix.tolist())
        all_labels.extend([slug] * len(matrix))
    all_vectors = np.asarray(all_vectors, dtype=np.float64)
    all_labels = np.asarray(all_labels)
    similarity_matrix = all_vectors @ all_vectors.T
    np.fill_diagonal(similarity_matrix, -1.0)
    multiclass_correct = 0
    multiclass_accepted = 0
    multiclass_wrong_accepted = 0
    slugs = list(matrices)
    for index, true_slug in enumerate(all_labels):
        scores = []
        for slug in slugs:
            mask = all_labels == slug
            class_scores = np.sort(similarity_matrix[index, mask])[::-1][:TOP_K]
            scores.append(float(class_scores.mean()))
        order = np.argsort(np.asarray(scores))[::-1]
        best = order[0]
        runner = order[1]
        predicted_slug = slugs[best]
        multiclass_correct += int(predicted_slug == true_slug)
        confident = (
            scores[best] >= float(model.get("threshold", 0.50))
            and scores[best] - scores[runner]
            >= float(model.get("margin", 0.20))
        )
        if confident:
            multiclass_accepted += 1
            if predicted_slug != true_slug:
                multiclass_wrong_accepted += 1
    targeted_positive = sum(row["total_test_samples"] for row in classes.values())
    targeted_accepted = sum(
        row["correctly_accepted_expected_samples"] for row in classes.values()
    )
    targeted_false = sum(row["false_acceptances"] for row in classes.values())
    targeted_negative = sum(row["negative_total"] for row in classes.values())
    output = {
        "method": "leave-one-out targeted v13 mean-centered top-k similarity",
        "model": os.path.relpath(MODEL_PATH, ROOT).replace(os.sep, "/"),
        "top_k": TOP_K,
        "maximum_false_acceptance_rate": MAX_FALSE_ACCEPT_RATE,
        "classes": classes,
        "comparison": {
            "targeted": {
                "total_test_samples": targeted_positive,
                "true_acceptances": targeted_accepted,
                "true_acceptance_rate": targeted_accepted / targeted_positive,
                "false_acceptances": targeted_false,
                "negative_test_samples": targeted_negative,
                "false_acceptance_rate": targeted_false / targeted_negative,
            },
            "existing_multiclass": {
                "total_test_samples": int(len(all_labels)),
                "top1_accuracy": multiclass_correct / len(all_labels),
                "accepted": multiclass_accepted,
                "acceptance_rate": multiclass_accepted / len(all_labels),
                "wrong_acceptances": multiclass_wrong_accepted,
                "wrong_acceptance_rate": (
                    multiclass_wrong_accepted / multiclass_accepted
                    if multiclass_accepted else 0.0
                ),
            },
        },
    }

    os.makedirs(os.path.dirname(THRESHOLD_PATH), exist_ok=True)
    with open(THRESHOLD_PATH, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2)

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2)

    print("Targeted verification v13 leave-one-out report")
    for slug, row in classes.items():
        print(
            f"{slug}: n={row['total_test_samples']} accepted="
            f"{row['correctly_accepted_expected_samples']} rejected="
            f"{row['rejected_expected_samples']} FA="
            f"{row['false_acceptances']}/{row['negative_total']} "
            f"({row['false_acceptance_rate']:.2%}) TAR="
            f"{row['true_acceptance_rate']:.2%} threshold="
            f"{row['threshold']:.6f}"
        )


if __name__ == "__main__":
    main()
