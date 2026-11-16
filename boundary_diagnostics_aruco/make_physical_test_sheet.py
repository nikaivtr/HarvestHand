"""Generate the isolated, print-ready ArUco physical test sheet."""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DPI = 300
PAGE_MM = (215.9, 279.4)  # US Letter
CARD_MM = (63.0, 88.2)  # exact 5:7 portrait ratio
MARKER_MM = 10.0
QUIET_ZONE_MM = 2.0
MARKER_TILE_MM = MARKER_MM + 2 * QUIET_ZONE_MM
MARKER_INSET_MM = 4.0
DICT_NAME = "DICT_4X4_50"
MARKER_IDS = (0, 1, 2, 3)


def px(mm):
    return int(round(mm * DPI / 25.4))


def dictionary():
    return cv2.aruco.getPredefinedDictionary(
        getattr(cv2.aruco, DICT_NAME)
    )


def marker_tile(marker_id):
    size = px(MARKER_MM)
    marker = np.zeros((size, size), dtype=np.uint8)
    marker = cv2.aruco.generateImageMarker(
        dictionary(), marker_id, size, marker, 1
    )
    tile = Image.new("RGB", (px(MARKER_TILE_MM), px(MARKER_TILE_MM)), "white")
    tile.paste(Image.fromarray(marker).convert("RGB"),
               (px(QUIET_ZONE_MM), px(QUIET_ZONE_MM)))
    return tile


def card_marker_positions():
    inset = MARKER_INSET_MM + QUIET_ZONE_MM
    right = CARD_MM[0] - inset - MARKER_MM
    bottom = CARD_MM[1] - inset - MARKER_MM
    return {
        0: (inset, inset),
        1: (right, inset),
        2: (inset, bottom),
        3: (right, bottom),
    }


def font(size, bold=False):
    candidates = (
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    )
    for candidate in candidates:
        if bold == ("bd" in candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def draw_card(page, origin):
    x0, y0 = origin
    card = Image.new("RGB", (px(CARD_MM[0]), px(CARD_MM[1])), "#f4f3e8")
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle(
        (0, 0, card.width - 1, card.height - 1),
        radius=px(1.5), outline="#245d3a", width=px(1.2)
    )
    safe = (
        px(12), px(18),
        card.width - px(12), card.height - px(18),
    )
    draw.rectangle(safe, outline="#aab9ad", width=px(0.5))
    draw.text((px(16), px(35)), "ILLUSTRATION-SAFE AREA",
              fill="#718276", font=font(px(3.0), bold=True))
    draw.text((px(21), px(44)), "Keep artwork and labels here",
              fill="#718276", font=font(px(2.4)))
    draw.text((px(20), px(72)), "ARUCO PHYSICAL TEST",
              fill="#193f29", font=font(px(3.2), bold=True))
    draw.text((px(21), px(76)), "HH-ARUCO-TEST-01",
              fill="#193f29", font=font(px(2.5)))
    for marker_id, position in card_marker_positions().items():
        tile = marker_tile(marker_id)
        card.paste(tile, (px(position[0] - QUIET_ZONE_MM),
                          px(position[1] - QUIET_ZONE_MM)))
        draw.text((px(position[0] + MARKER_MM + 1), px(position[1] + 2)),
                  f"ID {marker_id}", fill="#193f29", font=font(px(2.1)))
    page.paste(card, (x0, y0))


def make_page():
    page = Image.new("RGB", (px(PAGE_MM[0]), px(PAGE_MM[1])), "white")
    draw = ImageDraw.Draw(page)
    draw.text((px(15), px(12)), "HarvestHand ArUco Physical Test Card",
              fill="#193f29", font=font(px(5.5), bold=True))
    draw.text((px(15), px(19)),
              "Print at 100% / actual size. Do not fit to page.",
              fill="#9b2f2f", font=font(px(3.2), bold=True))
    card_x = (page.width - px(CARD_MM[0])) // 2
    draw_card(page, (card_x, px(31)))
    y = px(31 + CARD_MM[1] + 10)
    draw.text((px(15), y), "Dimensions", fill="#193f29",
              font=font(px(3.4), bold=True))
    lines = [
        f"Card: {CARD_MM[0]:.1f} x {CARD_MM[1]:.1f} mm (5:7)",
        f"Black marker: {MARKER_MM:.1f} mm square",
        f"Quiet zone: {QUIET_ZONE_MM:.1f} mm on each side",
        f"Black-marker inset from card edges: "
        f"{MARKER_INSET_MM + QUIET_ZONE_MM:.1f} mm",
        f"Dictionary: {DICT_NAME}; IDs: 0, 1, 2, 3",
    ]
    for index, line in enumerate(lines):
        draw.text((px(15), y + px(5 + index * 4.5)), line,
                  fill="#333333", font=font(px(2.8)))
    ref_y = page.height - px(26)
    ref_x = px(15)
    draw.line((ref_x, ref_y, ref_x + px(50), ref_y),
              fill="#193f29", width=px(0.5))
    draw.line((ref_x, ref_y - px(1), ref_x, ref_y + px(1)),
              fill="#193f29", width=px(0.5))
    draw.line((ref_x + px(50), ref_y - px(1),
               ref_x + px(50), ref_y + px(1)),
              fill="#193f29", width=px(0.5))
    draw.text((ref_x, ref_y + px(2)), "50 mm reference line",
              fill="#193f29", font=font(px(2.8)))
    draw.text((px(15), page.height - px(10)),
              "Verify the reference line with a ruler after printing.",
              fill="#9b2f2f", font=font(px(2.5), bold=True))
    return page


def make_marker_reference():
    page = Image.new("RGB", (px(PAGE_MM[0]), px(PAGE_MM[1])), "white")
    draw = ImageDraw.Draw(page)
    draw.text((px(15), px(12)), "ArUco Marker Reference",
              fill="#193f29", font=font(px(5.5), bold=True))
    draw.text((px(15), px(20)),
              f"{DICT_NAME}; print at 100%; each black marker is {MARKER_MM:.1f} mm",
              fill="#333333", font=font(px(3.0)))
    positions = ((25, 38), (125, 38), (25, 88), (125, 88))
    for marker_id, (x, y) in zip(MARKER_IDS, positions):
        tile = marker_tile(marker_id)
        page.paste(tile, (px(x), px(y)))
        draw.text((px(x), px(y + MARKER_TILE_MM + 3)),
                  f"ID {marker_id}", fill="#193f29", font=font(px(3.2)))
    draw.text((px(15), px(145)),
              "Do not redraw or resize individual markers.",
              fill="#9b2f2f", font=font(px(3.2), bold=True))
    return page


def main():
    page = make_page()
    reference = make_marker_reference()
    output = ROOT / "aruco_physical_test_sheet.pdf"
    page.save(output, "PDF", resolution=DPI, save_all=True,
              append_images=[reference])
    print(output)


if __name__ == "__main__":
    main()
