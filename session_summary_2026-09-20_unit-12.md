# Session summary — 2026-09-20 — Unit 12 port

## Done
- Ported Unit 12 (Matt 12:1–50, "Master of the Sabbath, the Chosen Servant").
- Lane promoted 9 threads: judge, fruit, treasure (these three had been local roots
  in an earlier unit, with a different colour there), plus sign, defame, house,
  permitted, counsel, rest. Retro-tagged every earlier occurrence (units 2–11).
- Rulings: "defame" (not "blaspheme") everywhere; epitimaō "charge sharply" at
  8:26 as well as 12:16.
- translation-choices.md, CLAUDE.md status, style-reference map updated; build green.

## Takeaways
- palette.py's `all_colors()` keys a local root by name book-wide (first unit wins),
  so a local root with a different colour in two units shows as a false dE00 0.00
  "co-occurring" pair. Promoting such roots (the standing precedent) makes it go
  away; if a root is ever deliberately left local in two units, palette.py needs
  to become per-unit for locals.
- `apply_retrofit` `add` only tags the first free match in a verse; a second
  identical word needs a `text` op. Text ops run before adds, so a text op whose
  `from` contains a span that an add creates only lands on the second build.
- assign_color.py takes ~80s per root at 106 roots.

## Open
- ekteinō (`stretch-out`, local in 12) also occurs at 8:3, where it's untagged.
  If it's promoted, tag 8:3 as well.
- hunger (peinaō) left local; if promoted, it needs a tighter stem than `πειν`
  (that one also catches eipein, tapein-, blepein).
- epitimaō beyond unit 12 (8:26 done): 16:22, 17:18, 19:13, 20:31 will need
  the "charge sharply" call as they arrive.
- Visual check of unit 12 and the retro-tagged units in the live site (Lane).
