# Session summary — 2026-10-07 — interlinear rework

## Done
- Showed Lane four mockups (A per-verse fold-out, B stacked true interlinear, C tap-a-word popover, D cross-highlight). Picked: A + D, with the verse number as the toggle, a Plain / Notes / Greek pill, Greek + translit, all books via core, "every note open" as a settings switch, Greek mode = Notes + all verses open. Also asked: prettier settings controls.
- bible-core 0.16.0 (e82f2df, tag v0.16.0):
  - `emit` writes `data/script/<ch>.json` (words in the original script, parallel to `words/`); Hebrew drops OSHB slashes and the cantillation. ARCHITECTURE's "no native script" rule now names this as the one exception. `verify-words` checks the alignment (a book with no script folder gets a note to rebuild).
  - reader.js: `toggleVerse`, `wireVerseNumbers` (click/Enter on `.v > .n`, cross-highlight via `data-w`), `prepVerseNumbers`; rows fold with a height animation (off under reduced motion). Hebrew rows run right to left.
  - main.js: segmented pill (`#mode-pill`) + appearance pill; open-notes switch; old "open" mode migrates.
  - core.css: tray-style rows (no per-word boxes), Gentium Book Plus / Noto Serif Hebrew for the script line (loaded on use), switches.
- Vendored into Numbers, Joshua, Matthew (built and tested in each). Nothing pushed.

## Takeaways
- English words map to Greek only where they're tagged with `data-w` (thread words, about 1–2 per verse), so the cross-highlight is sparse. A full English↔Greek alignment would be a research-side job.

## Open
- Lane to look over the live site after pushing (desktop and phone; Hebrew rows in Numbers/Joshua).
- Matthew: `python -m biblecore sync` after the push (chat-side files changed).
