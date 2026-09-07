# Session Summary — 2026-09-07 (Phase 2: the shell)

## What was done

Built the static-site shell that renders the Phase 1 fragments.

- **`data/units.json`** — 28-unit manifest (number, slug, passage, working title,
  movement, `built` flag). The 8 built units carry a local `roots` map
  (root → hex). Folded in the Phase 4 colour fixes early so everything renders:
  U2 `call`→name / `king`→david aliases, U3 `wild` + `wilderness`, and a fresh
  9-hue palette for U7 (whose original `<style>` was a stale copy).

- **`css/styles.css`** — one reconciled stylesheet. App chrome (sticky topbar,
  collapsible 28-unit Contents picker grouped by movement, prev/next pager,
  footnote-flash `@keyframes`) + the *superset* of all 8 artifacts' component CSS
  (genealogy frame, ring maps, correspondence tables, itinerary chips, prayer
  block, compare box, endnotes…). Chrome colours that used to borrow a unit's
  root vars (`--c-beget` for verse numbers etc.) now use stable `--accent-*`
  tokens. Responsive breakpoint at 720px.

- **`index.html`** — shell: topbar with a Contents toggle showing "Unit N of 28",
  hidden-by-default unit nav, `#content` pane, pager.

- **`app/main.js`** — ES-module hash router:
  - `#/unit-03` loads `units/unit-03.html`; `#/unit-03/u03-n5` also scrolls to and
    flashes that endnote.
  - Injects `.unit[data-unit="N"] [data-root="x"]{color:…}` from `units.json` on
    each load — no build step, no per-unit `<style>`.
  - Footnote interaction: click a ref → smooth-scroll + 1.15s flash + a "↩ back"
    link appended to the note; click the same ref again (note in view) or the
    back-link → return to the verse and flash it.
  - Builds the movement-grouped nav and the prev/next pager from the manifest.

- **`.claude/launch.json`** (python http.server :4180), **`.gitignore`**.

## Verified in-browser (in-app browser, localhost:4180)

- All 8 units render with the parchment theme intact.
- Per-unit palettes inject correctly — **0 uncoloured `data-root` spans** in any
  unit, U7 included.
- Footnote jump → flash → back-link → return-and-flash all work.
- No horizontal overflow at 375px; legend collapses to one column, tables/frames
  reflow.
- Pager and collapsible nav behave (Esc closes, picking a built unit closes it).

## Bugs fixed mid-phase (in `pipeline/extract_units.py`, re-run clean)

- Unwrapping a Latin-mislabelled `<span class="gk">` was dropping the trailing
  captured context ("David is named before Abraham…" → "Davidm…").
- `(<gk>βίβλος γενέσεως</gk>, biblos geneseōs)` was losing its closing paren.

Both were caught by reading the rendered page, not the fragment.

## Next — Phase 3: Git + GitHub Pages

Lane drives; I walk through `git init`, `.gitignore` is ready, first commit,
create the GitHub repo, push, enable Pages from the subpath, verify the deployed
site (so relative-path bugs surface now, not at Unit 20).

Then Phase 4: `data/threads.json` (the 16 tracked threads), the scan/verify
pipeline, data-driven legends, and the tag-retrofit review.
