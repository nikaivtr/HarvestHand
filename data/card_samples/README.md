# Card training photos

Put photos of your physical cards in this folder, with one subfolder per
card. Folder names match the card names in `Harvest_Hand_Card_Details.xlsx`
(lowercase, with spaces changed to underscores). The scanner's internal
class names are separate, so you do not need to name folders after code slugs.

## Action cards

| Card ID | Card name | Sample folder |
|---|---|---|
| AC-01 | Watering Can | `watering_can/` |
| AC-02A | Organic Fertilizer | `organic_fertilizer/` |
| AC-02B | Chemical Fertilizer | `chemical_fertilizer/` |
| AC-03 | Weed Removal | `weed_removal/` |
| AC-04A | Natural Pesticide | `natural_pesticide/` |
| AC-04B | Chemical Pesticide | `chemical_pesticide/` |
| AC-05 | Harvest | `harvest/` |

## Crop cards

| Card ID | Card name | Sample folder |
|---|---|---|
| CC-01 | Pechay | `pechay_plant/` |
| CC-02 | Monggo | `monggo_plant/` |
| CC-03 | Okra | `okra_plant/` |
| CC-04 | Kalabasa (Squash) | `squash_plant/` |
| CC-05 | Kamatis (Tomato) | `tomato_plant/` |
| CC-06 | Talong (Eggplant) | `eggplant_plant/` |
| CC-07 | Kamote (Sweet Potato) | `sweet_potato_plant/` |
| CC-08 | Palay (Rice) | `rice_plant/` |
| CC-09 | Mais (Corn) | `corn_plant/` |
| CC-10 | Kamoteng Kahoy (Cassava) | `cassava_plant/` |

For example:

```text
data/card_samples/
    watering_can/01.jpg  02.jpg  ...
    organic_fertilizer/01.jpg  ...
    pechay_plant/01.jpg  ...
```

`analyze/` is an optional extra used by the game's research challenge; it is
not listed in the supplied card-details spreadsheet. There are no sample
folders for Shield, Heal, or generic AC-02/AC-04 cards because they are not in
that physical card list. AC-02 and AC-04 chapter prompts are treated as the
Organic Fertilizer and Natural Pesticide cards respectively.

To capture samples with a connected camera, run this from the project root,
replacing `watering_can` with another sample folder name from the tables:

```text
python tools/capture_samples.py --card watering_can
python tools/capture_samples.py --card organic_fertilizer
python tools/capture_samples.py --card pechay_plant
```

The capture tool saves them into the matching named folder. Press Space to
take each picture and Q or Escape to finish. You can also copy photos into
these folders manually.

Once you have added or changed photos, train and inspect the report:

```text
python tools/train_cards.py --report
```

At least 5 photos per card are recommended; 15-30 varied photos work better.
Vary distance, angle, lighting, background, and nearby cards. Keep the whole
card inside the green capture square and use the same lighting as the game.
Retrain after adding photos or changing the printed cards; the model is a
snapshot and does not learn during play.
