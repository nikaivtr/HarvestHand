# Manual review

Review the combined overlays and fill `manual_boundary_annotations.json` only
with independently verified card corners. The annotation tool supports:

- Left click: add corners clockwise.
- `U`: undo the last point; `C`: clear points.
- `1` complete card; `2` partially obstructed; `3` boundary unclear;
  `4` blurred/damaged; `5` no usable card.
- `Space`: preview the perspective crop.
- `R`: show the experimental candidate overlay as a reference only.
- `T`: enter reviewer notes in the terminal.
- `S`: save; `N`/`P`: next/previous; `Q`/`Esc`: quit.

Empty fields mean no manual review has been supplied. The experiment does not
claim visual verification until these records are explicitly saved by a
reviewer.
