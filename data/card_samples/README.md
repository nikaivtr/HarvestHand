# Card samples

Put photos of your **physical cards** in here, one folder per card.

The folder name must match the card's *slug* from
`cardscan/registry.py`:

| Slug        | Card            | Used by chapters? |
|-------------|-----------------|-------------------|
| `water`     | AC-01 Water     | yes               |
| `fertilizer`| AC-02 Fertilizer| yes               |
| `weed`      | AC-03 Weed Removal | yes            |
| `pesticide` | AC-04 Pesticide | yes               |
| `harvest`   | AC-05 Harvest   | yes               |
| `heal`      | AC-06 Heal      | not yet           |
| `shield`    | AC-07 Shield    | not yet           |

```
data/card_samples/
    water/       01.jpg  02.jpg  ...
    fertilizer/  01.jpg  ...
    heal/
    shield/
```

Then train:

```
python tools/train_cards.py --report
```

You do not have to shoot these by hand. On the Raspberry Pi:

```
python tools/capture_samples.py --card water
```

which grabs photos from the live camera straight into these folders.

## How many photos, and how to shoot them

**At least 5 per card, ideally 15-30.** The recogniser averages
everything it is given, so more varied photos make it steadier.

Vary these on purpose, because they are exactly what changes in a
real classroom:

- **Distance** — close to the lens, and arm's length away.
- **Angle** — flat on, tilted left, tilted right. Hand-held cards
  are never perfectly square, and the recogniser crops a centred
  region, so a card that drifts off-centre must still match.
- **Lighting** — bright room, dim room, and some sideways light.
  This one matters most; the feature extractor divides out
  brightness, which is why it survives, but only if it has seen
  the range.
- **Background** — on the table, over the player's hand, over a
  mat. Anything consistently filling the frame changes the match.
- **Which card is up** — also photograph the cards *near* the
  target one, since neighbouring cards are what cause
  misreads.

## Gotchas

- **Film the card filling most of the frame.** `features.CROP`
  takes the middle 86% of the picture, so a small card far from
  the lens is mostly background and will not match well.
- **Use the same lighting you will scan in.** If the game runs in
  a bright classroom, do not train in the dark.
- **Keep the filenames short** and avoid spaces. Not required, but
  easier when you are eyeballing the folders.
- **Retrain after changing cards** or printing a new batch. The
  model is a snapshot, not something that learns at runtime.
