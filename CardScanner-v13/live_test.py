"""Live v13 card-recognition diagnostic."""

import os

import cv2

import cardscan.model as card_model
import cardscan.preprocess as preprocess
import cardscan.features as features


LABELS = {
    "pechay_plant": "Pechay",
    "monggo_plant": "Monggo",
    "okra_plant": "Okra",
    "squash_plant": "Kalabasa",
    "tomato_plant": "Kamatis",
    "eggplant_plant": "Talong",
    "sweet_potato_plant": "Kamote",
    "rice_plant": "Palay",
}


def open_camera():
    for name, api in (
        ("Media Foundation", cv2.CAP_MSMF),
        ("DirectShow", cv2.CAP_DSHOW),
    ):
        camera = cv2.VideoCapture(0, api)
        if not camera.isOpened():
            camera.release()
            continue
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        for _ in range(8):
            ok, frame = camera.read()
            if ok and frame is not None:
                print("Camera:", name, frame.shape[1], "x", frame.shape[0])
                return camera
        camera.release()
    return None


def main():
    model_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "card_model_card_plants_mean_centered_v13_experimental.json",
    )
    trained = card_model.load_model(model_path)
    if trained is None:
        raise RuntimeError("No valid v13 model found.")

    camera = open_camera()
    if camera is None:
        raise RuntimeError("Camera unavailable.")

    print("Press Q to stop.")
    while True:
        ok, frame = camera.read()
        if not ok or frame is None:
            continue
        cv2.imshow("CardScanner v13", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key != ord("r"):
            continue

        import pygame

        pygame.init()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surface = pygame.image.frombuffer(
            rgb.tobytes(), (frame.shape[1], frame.shape[0]), "RGB",
        )
        candidates = preprocess.prepare_candidates(
            surface, max_candidates=3, fallback=None,
        )
        best = None
        for canvas, details in candidates:
            for view in (canvas, pygame.transform.rotate(canvas, 180)):
                vector = features.extract_card(view)
                if vector is None:
                    continue
                match = card_model.match_detailed(trained, vector)
                if match is None:
                    continue
                confident = (
                    match["best_score"] >= trained["threshold"]
                    and match["gap"] >= trained["margin"]
                )
                rank = (confident, match["best_score"], match["gap"])
                if best is None or rank > best[0]:
                    best = (rank, match, details)
        if best is None:
            print("NO CARD MATCH")
        else:
            rank, match, details = best
            slug = match["best_slug"]
            print(
                LABELS.get(slug, slug),
                "score=", round(match["best_score"], 3),
                "gap=", round(match["gap"], 3),
                "CONFIDENT" if rank[0] else "NOT CONFIDENT",
                "source=", details.get("source"),
            )
        pygame.quit()

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
