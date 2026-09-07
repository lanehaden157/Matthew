# Session Summary — 2026-09-07 (kickoff + Phase 1)

## What was done

**Direction set.** Turned the loose CLAUDE.md into a project guide, then wrote
`PLAN.md` — a 9-phase plan to rebuild the 28-unit Matthew study as a static site
with a shared engine, runtime-resolved two-tier colour, and cross-unit thread
tracking. `ideas.md` folded into the phase scope.

**Contradictions surfaced and resolved with Lane:**
- Per-unit vs. global colour — the style reference reverses itself. Resolved:
  kill per-unit `<style>`; every colour word is `<span class="r" data-root="X">`,
  resolved at load (global `threads.json` → else local `units.json`).
- "Never hand-edit /data" fought itself. Split: `threads.json` hand-authored
  (policy), `occurrences.json` generated (fact), `units.json` seed + generated.
- Greek script: style ref says translit-only, memory says script-first, units 1–7
  are full of Greek, unit 8 (newest) has none. Lane chose **translit only**.
- 3 candidate threads (torment / urge / sea-mirror) → **approved**, so 16 tracked
  threads total.

**Phase 1 built and run:**
- `pipeline/greek.py` — deterministic Greek→Latin transliterator. Output matches
  the existing ē/ō/ch/ph/ps/rh/ou scheme exactly on every test word.
- `pipeline/extract_units.py` — `source-artifacts/matthew_NN_translation.html` →
  `units/unit-NN.html`. Strips head/style/fonts; removes all Greek + Hebrew script
  (314 synthesised transliterations, 4 hand-corrected, redundant echoes cleaned,
  zero script chars left); `class="r X"` → `data-root`; bare colour spans →
  `class="rl"`; endnote ids/hrefs → `u0N-nK`; `.greek-title` rebuilt.
- `source-artifacts/` — untouched copies of all 8 originals.
- `pipeline/out/units.seed.json`, `pipeline/out/extract-report.md`.
- All 8 fragments: tags balanced, endnote refs resolve, prose untouched.

## Takeaways

- Inline Unicode ranges in `bash -c` get mangled in this shell — always put
  regex/Unicode work in `.py` files and run the file.
- Unit 8 is the normalization target: it's the newest rebuild and already
  translit-only with `.translit` / `.tr` spans and plain-English endnote lemmas.
- The colour system was already failing silently before this work — Unit 7's
  `<style>` block is a stale copy of Units 2–3, so every coloured word in Unit 7
  currently renders grey.

## Open questions / next

- **Phase 2** is next: `index.html` tab shell + `app/main.js` router + one
  reconciled `css/styles.css` (base on Unit 8 + style ref §2, fold in the 8
  drifted cores). Must render all 8 units and be responsive (desktop + mobile).
- Phase 4 must resolve: U2 `call`/`king` aliases, U3 `wild`→`wilderness`, and a
  fresh 9-hue palette for U7.
- Lane will drive the git init + GitHub Pages setup at Phase 3.
- New ideas captured this session: footnote jump-and-highlight with return;
  desktop+mobile both first-class (added to `ideas.md` and `PLAN.md`).
