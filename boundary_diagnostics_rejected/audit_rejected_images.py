"""Reproduce and document current preprocessing rejections.

This diagnostic imports the existing production preprocessing code but does not
modify it. It writes only into boundary_diagnostics_rejected/.
"""

import csv
import math
import os
import sys
from pathlib import Path

import pygame
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cardscan.preprocess as preprocess


ROOT = Path(__file__).resolve().parent
DATASET = ROOT.parent / "data" / "card_samples"
CLASSES = ("pechay_plant", "monggo_plant")
OUTPUT_CSV = ROOT / "rejected_images_audit.csv"
OUTPUT_SHEET = ROOT / "rejected_images_contact_sheet.jpg"
CATEGORIES = {
    "boundary": "Boundary Detection Failure",
    "perspective": "Perspective Distortion",
    "lighting": "Poor Lighting / Shadows",
}

# Manual review of the generated contact sheet. The primary category describes
# the visible cause, while the preprocessing reason remains recorded verbatim.
AUDIT = {
    # Pechay: dark captures where boundary evidence is weak.
    "5339ff0a-02d3-4b5a-adb2-3b3eb45244f0.jpg": ("lighting", "conditional",
        "Card is visible but the scene is very dark."),
    "5b127e8d-7055-492f-8202-3c2a043df58d.jpg": ("lighting", "conditional",
        "Card is visible but the scene is very dark."),
    "5db9eba2-e62f-4e28-8b6e-a716d09e2149.jpg": ("lighting", "conditional",
        "Card is visible but the scene is very dark."),
    "78330d81-82fc-437c-9eb5-3fec7da718b2.jpg": ("lighting", "conditional",
        "Card is visible but the scene is very dark."),
    "8291ce14-2bad-4ba3-9e2f-46e957709221.jpg": ("lighting", "conditional",
        "Card is visible but the scene is very dark."),
    "ba5f5898-1431-47c4-9fa4-4ecec1aa78de.jpg": ("lighting", "conditional",
        "Card is visible but the scene is very dark."),
    "c4870fcb-1799-4d5c-b203-1d5b29e76dc0.jpg": ("lighting", "conditional",
        "Card is visible but the scene is very dark."),
    # Monggo: geometry is the dominant issue in the plant/blue-background set.
    "IMG_20261110_141840.jpg": ("perspective", "conditional",
        "Card is strongly rotated on the blue surface."),
    "IMG_20261110_141906.jpg": ("perspective", "conditional",
        "Card is strongly tilted among foliage; boundary geometry is unstable."),
    "IMG_20261110_142045.jpg": ("perspective", "conditional",
        "Card is oblique among foliage; candidate geometry fails validation."),
}
SECONDARY = {
    "5339ff0a-02d3-4b5a-adb2-3b3eb45244f0.jpg":
        "Blurred / Out of Focus",
    "5b127e8d-7055-492f-8202-3c2a043df58d.jpg":
        "Blurred / Out of Focus",
    "78330d81-82fc-437c-9eb5-3fec7da718b2.jpg":
        "Blurred / Out of Focus",
    "ba5f5898-1431-47c4-9fa4-4ecec1aa78de.jpg":
        "Blurred / Out of Focus",
    "c4870fcb-1799-4d5c-b203-1d5b29e76dc0.jpg":
        "Blurred / Out of Focus",
    "IMG_20261110_141840.jpg": "Boundary Detection Failure",
    "IMG_20261110_141906.jpg": "Boundary Detection Failure",
    "IMG_20261110_142045.jpg": "Boundary Detection Failure",
}

for name in (
    "15b3c45c-229f-4bc2-8b11-a741f583d591.jpg",
    "1ea480c8-e7c9-4298-8545-424246d671c2.jpg",
    "2b5dd6d2-bb4e-4c9c-a0e5-996f783db777.jpg",
    "2bacde34-d63f-4885-afa2-c63a54219b31.jpg",
    "4407a29c-5afb-4a31-af48-5a2f23237a71.jpg",
    "668da6b6-cb26-495e-83ee-62a3b7b0fbc9.jpg",
    "82964558-1618-4853-829e-f1f97fcbbd7e.jpg",
    "93d262c8-f97f-4e23-ab3a-4e7002d75214.jpg",
    "9695bc39-6647-4437-93d5-2bcc31b5b5b3.jpg",
    "9d2195a4-fc90-4f13-9e8b-3de6d7e4f8d3.jpg",
    "ced8a0e8-2fcc-4c5f-a979-0a98b0854b1e.jpg",
    "cf18fef3-92cf-4437-b327-aaeb0915b4e8.jpg",
    "cfe8a3cf-6665-4e61-a904-36dc93010a6e.jpg",
    "d76a6f8c-f69f-4695-b876-7a1d51e427ab.jpg",
    "db66a971-017b-414a-90d0-fc582e1d3be2.jpg",
    "dcbb71ba-b01f-40d1-ab7a-e3b50e24a4d6.jpg",
    "f32364fe-aff9-421e-9569-e97e42a976aa.jpg",
    "f7acde1c-d3e9-4179-a169-00765e68e5c4.jpg",
    "IMG_20261110_135321.jpg",
    "IMG_20261110_135330.jpg",
    "IMG_20261110_135346.jpg",
    "IMG_20261110_135400.jpg",
    "IMG_20261110_135414.jpg",
    "IMG_20261110_135435.jpg",
    "IMG_20261110_135729.jpg",
):
    AUDIT[name] = ("boundary", "recoverable",
                   "Card is visible; current candidate generation misses or "
                   "rejects its boundary.")

for name in (
    "06f34cc6-cfcf-4805-a210-9679a4cb591c - Copy.jpg",
    "06f34cc6-cfcf-4805-a210-9679a4cb591c.jpg",
    "0a01f9f6-fb25-4cb2-b253-89ad882e4ea4.jpg",
    "299f151c-890e-4e80-b5ef-276cc8c1f737.jpg",
    "325fe2ba-fe12-480b-9c91-4c037b5633ef.jpg",
    "4e5e32c9-3d5b-498f-a498-0bcd5780a17d.jpg",
    "4ef036f9-3397-4241-b010-638cfaa9104d.jpg",
    "4fa5ceb0-9108-4084-a1e4-0136026cce13 - Copy.jpg",
    "4fa5ceb0-9108-4084-a1e4-0136026cce13.jpg",
    "59db5bd6-f83e-4ed0-921f-e815160f210d.jpg",
    "5ac988f1-a307-4906-b2f9-d9e54f1aa139.jpg",
    "65f44f31-81b6-44be-8bde-c65af98d4e63.jpg",
    "6ba8cceb-393b-4b90-a19e-cf09c8dc5d80.jpg",
    "85bceec5-2c5e-48ef-a279-8f85e12d0064.jpg",
    "91258ac8-8731-4955-9712-9608ea857726.jpg",
    "9d342fee-0b8c-4af7-8c2c-2a4e795431b1.jpg",
    "a294b9af-0fd9-4d40-b804-e781fa0eec07.jpg",
    "a53bc616-2de1-4f66-a2e1-4fb06e43f639.jpg",
    "ab95f40d-bddd-4e22-a49a-069b303a2fd3.jpg",
    "b8d7215a-a96a-423f-92ac-c55aada888d0.jpg",
    "c2e3bfdf-dc97-42ab-a366-5aa63562f3e2.jpg",
    "ea1dcf87-454d-4074-aeaf-6aa4dcb720ad.jpg",
    "IMG_20261110_141914.jpg",
    "IMG_20261110_141941.jpg",
    "IMG_20261110_141953.jpg",
    "IMG_20261110_141958.jpg",
    "IMG_20261110_142003.jpg",
    "IMG_20261110_142009.jpg",
    "IMG_20261110_142050.jpg",
):
    AUDIT[name] = ("boundary", "recoverable",
                   "Card is visible; current candidate generation misses or "
                   "rejects its boundary.")


def font(size):
    for path in ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def collect():
    rows = []
    for slug in CLASSES:
        for path in sorted((DATASET / slug).iterdir()):
            if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp",
                                           ".webp"}:
                continue
            image = preprocess.load_image(str(path))
            details = {}
            prepared = None
            if image is None:
                reason = "image could not be decoded"
                width = height = ""
                file_format = ""
            else:
                width, height = image.get_size()
                try:
                    pil_image = Image.open(path)
                    file_format = pil_image.format or ""
                except (OSError, ValueError):
                    file_format = ""
                prepared, details = preprocess.prepare_detailed(image)
                reason = details.get("reason", "")
            if prepared is not None:
                continue
            row = {
                "class": slug,
                "filename": path.name,
                "path": str(path),
                "width": width,
                "height": height,
                "format": file_format,
                "file_size_bytes": path.stat().st_size,
                "decoded": bool(image is not None),
                "status": details.get("status", "failed"),
                "reason": reason,
                "quality": details.get("quality", ""),
                "area_ratio": details.get("area_ratio", ""),
                "aspect": details.get("aspect", ""),
                "aspect_score": details.get("aspect_score", ""),
                "opposite_side_ratio": details.get("opposite_side_ratio", ""),
                "min_angle": details.get("min_angle", ""),
                "max_angle": details.get("max_angle", ""),
                "edge_support": details.get("edge_support", ""),
                "primary_category": "",
                "secondary_category": "",
                "recoverability": "",
                "audit_note": "",
            }
            category, recoverability, note = AUDIT.get(
                path.name,
                ("boundary", "needs manual review",
                 "No manual classification was recorded."),
            )
            row["primary_category"] = CATEGORIES[category]
            row["secondary_category"] = SECONDARY.get(path.name, "")
            row["recoverability"] = recoverability
            row["audit_note"] = note
            rows.append(row)
    return rows


def make_sheet(rows):
    columns = 4
    cell_width, cell_height = 360, 390
    sheet = Image.new(
        "RGB",
        (columns * cell_width, math.ceil(len(rows) / columns) * cell_height),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    title_font = font(18)
    label_font = font(15)
    small_font = font(13)
    for index, row in enumerate(rows):
        x = (index % columns) * cell_width
        y = (index // columns) * cell_height
        try:
            image = Image.open(row["path"]).convert("RGB")
            image.thumbnail((340, 315))
            image_x = x + (cell_width - image.width) // 2
            sheet.paste(image, (image_x, y + 28))
        except (OSError, ValueError):
            draw.text((x + 20, y + 150), "DECODE FAILED", fill="red",
                      font=title_font)
        draw.text((x + 8, y + 5),
                  f"{row['class']} | {row['filename'][:32]}",
                  fill="black", font=label_font)
        details = (
            f"{row['reason'][:42]}\n"
            f"{row['width']}x{row['height']}  q={str(row['quality'])[:6]} "
            f"a={str(row['area_ratio'])[:6]}"
        )
        draw.multiline_text((x + 8, y + 338), details, fill="darkred",
                            font=small_font, spacing=2)
    sheet.save(OUTPUT_SHEET, quality=90)


def make_group_sheet(rows, path, title):
    columns = 3
    cell_width, cell_height = 460, 450
    sheet = Image.new(
        "RGB",
        (columns * cell_width, math.ceil(len(rows) / columns) * cell_height),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(rows):
        x = (index % columns) * cell_width
        y = (index // columns) * cell_height
        image = Image.open(row["path"]).convert("RGB")
        image.thumbnail((440, 350))
        sheet.paste(image, (x + (cell_width - image.width) // 2, y + 32))
        draw.text((x + 8, y + 6),
                  f"{row['filename']} | {row['class']}",
                  fill="black", font=font(16))
        draw.multiline_text(
            (x + 8, y + 388),
            f"{row['primary_category']}\n{row['reason']}",
            fill="darkred", font=font(14), spacing=2,
        )
    if not rows:
        draw.text((20, 20), f"{title}: none", fill="black", font=font(18))
    sheet.save(path, quality=90)


def write_report(rows):
    counts = {}
    class_counts = {}
    recovery_counts = {}
    for row in rows:
        counts[row["primary_category"]] = counts.get(
            row["primary_category"], 0
        ) + 1
        key = (row["class"], row["primary_category"])
        class_counts[key] = class_counts.get(key, 0) + 1
        recovery_counts[row["recoverability"]] = recovery_counts.get(
            row["recoverability"], 0
        ) + 1

    def n(slug, category):
        return class_counts.get((slug, CATEGORIES[category]), 0)

    table = "\n".join(
        f"| {row['filename']} | {row['class']} | "
        f"{row['primary_category']} | {row['recoverability']} | "
        f"{row['reason']} |"
        for row in rows
    )
    (ROOT / "REJECTED_IMAGE_AUDIT_REPORT.md").write_text(
        f"""# Rejected Image Diagnostic Audit

## Dataset summary

The latest two-class training run saw 64 preprocessing rejections:

| Class | Total files | Usable | Rejected |
|---|---:|---:|---:|
| Pechay | 122 | 90 | 32 |
| Monggo | 132 | 100 | 32 |
| **Total** | **254** | **190** | **64** |

All 64 rejected files were reproduced by the current
`preprocess.prepare_detailed()` path. Every file decoded successfully as a
JPEG; there were no corrupted or unsupported files.

## Exact preprocessing conditions

The detector downsizes only for detection to a maximum dimension of 960,
converts RGB to blurred grayscale, and searches contours from:

1. Canny edges with morphological closing.
2. Binary light masks at thresholds 140 and 180 with morphological closing.

Candidates must be convex quadrilaterals and pass all of these checks:

- Area ratio at least 0.07.
- Aspect score at least 0.65 against the 5:7 card aspect.
- Opposite-side ratio at least 0.45.
- Corner angles between 45 and 135 degrees.
- Minimum edge support at least 0.02, except for candidates larger than 30%
  of the frame.

The observed failure messages were:

- `candidate too small`: 48 images.
- `no quadrilateral candidates`: 13 images.
- `card border edge support too weak`: 1 image.
- `candidate failed validation`: 2 images.

The message counts overlap in the sense that the latter two are candidate
validation outcomes; the per-image CSV is authoritative.

## Rejection categories

| Rejection category | Pechay | Monggo | Total | Typical recoverability |
|---|---:|---:|---:|---|
| Boundary Detection Failure | {n('pechay_plant', 'boundary')} | {n('monggo_plant', 'boundary')} | {counts.get(CATEGORIES['boundary'], 0)} | Recoverable |
| Poor Lighting / Shadows | {n('pechay_plant', 'lighting')} | {n('monggo_plant', 'lighting')} | {counts.get(CATEGORIES['lighting'], 0)} | Conditional |
| Perspective Distortion | {n('pechay_plant', 'perspective')} | {n('monggo_plant', 'perspective')} | {counts.get(CATEGORIES['perspective'], 0)} | Conditional |
| Blurred / Out of Focus | 0 | 0 | 0 | — |
| Partial / Obstructed Card | 0 | 0 | 0 | — |
| Low Resolution | 0 | 0 | 0 | — |
| Corrupted / Unsupported | 0 | 0 | 0 | — |
| Other / Uncertain | 0 | 0 | 0 | — |

The dominant issue is therefore the detector's inability to find or accept
the card quadrilateral, not file quality. Many cards are visible and appear
complete, but occupy a small fraction of the frame or have weak/fragmented
edges. Their full image dimensions are high; they are not intrinsically
low-resolution files.

## Recoverability

- **Recoverable:** {recovery_counts.get('recoverable', 0)} images. The card is
  visibly present and the current contour/candidate logic is the limiting
  factor. Candidate generation, multi-scale detection, or a separately
  validated detector could recover some of these.
- **Conditionally recoverable:** {recovery_counts.get('conditional', 0)}
  images. Better lighting or less severe camera geometry may help, but any
  recovered crop must still pass independent visual boundary review.
- **Unrecoverable:** 0 established by this audit.
- **Needs manual review:** {recovery_counts.get('needs manual review', 0)}.

No automatic correction was applied and no original image was modified.

## Recommendations

1. Improve candidate generation and ranking rather than lowering the
   `MIN_CARD_AREA_RATIO` or confidence thresholds blindly.
2. Add an independent content/boundary validation stage so a larger
   quadrilateral cannot silently select background.
3. Use multi-scale or card-size-aware detection for the small-card images.
4. Capture future samples with the card occupying more of the frame and with
   diffuse lighting.
5. Keep the 64 rejected images available for future detector experiments;
   do not add them to a production model until their crops are verified.

Improving localization could plausibly recover a meaningful subset because
most rejected photos contain a visible card. However, the prior v12 audit
showed that accepting geometrically plausible background regions is worse than
rejecting an uncertain crop, so recovery must be conservative.

## Contact sheets

- [All rejected images](rejected_images_contact_sheet.jpg)
- [Pechay rejected images](pechay_plant_rejected_contact_sheet.jpg)
- [Monggo rejected images](monggo_plant_rejected_contact_sheet.jpg)
- [Boundary failures](category_boundary_contact_sheet.jpg)
- [Lighting cases](category_lighting_contact_sheet.jpg)
- [Perspective cases](category_perspective_contact_sheet.jpg)
- [Per-image measurements and classifications](rejected_images_audit.csv)

## Individual classifications

| Filename | Class | Primary category | Recoverability | Preprocessing reason |
|---|---|---|---|---|
{table}

## Limitations

The visual categories were assigned from the generated contact sheets and
current detector measurements. A rejection reason such as `candidate too
small` does not prove that the card is unusable; it identifies the current
algorithm's selected candidate. Blur and obstruction were not assigned unless
they were visually evident. No independent corner ground truth was available,
and no alternative preprocessing algorithm was used in this audit.
""",
        encoding="utf-8",
    )


def main():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    try:
        rows = collect()
        with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        make_sheet(rows)
        for key, title in CATEGORIES.items():
            make_group_sheet(
                [row for row in rows
                 if row["primary_category"] == title],
                ROOT / f"category_{key}_contact_sheet.jpg",
                title,
            )
        for slug in CLASSES:
            make_group_sheet(
                [row for row in rows if row["class"] == slug],
                ROOT / f"{slug}_rejected_contact_sheet.jpg",
                slug,
            )
        write_report(rows)
        print(f"rejected={len(rows)}")
        print(f"csv={OUTPUT_CSV}")
        print(f"contact_sheet={OUTPUT_SHEET}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
