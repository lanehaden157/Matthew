# Matthew Study — Build Plan

Phased plan for turning the 8 standalone HTML study-translation artifacts into a
static site with a shared engine, a two-tier color system, and cross-unit thread
tracking. Draft for Lane's sign-off; CLAUDE.md gets rewritten to match once approved.

---

## What exists today

- **8 artifacts** — `matthew_01_translation.html` … `matthew_08_translation.html`.
  Each is a full standalone HTML doc: `<head>`, Google Fonts link, a ~6.5–7.4 KB
  inline `<style>` block, body inside `<div class="wrap">`.
- **`matthew_study_style_reference.md`** — CSS/component library (§2–3), conventions
  checklist (§4), Literary Unit Map for all 28 units (§7). Says "translit only, no
  Greek script" and "per-unit color, no cross-unit registry."
- **`old memory.md`** — project memory. Lists **13 live cross-unit threads** with
  origin/payoff verses + open/closed status, plus 3 candidates (now approved →
  **16 threads**). Says script-first policy and "memory is authoritative over the
  style reference." Units 1–8 complete; **Unit 9 (Matt 9:1–34) is next**.
- **`ideas.md`** — feature backlog, split Now / Later.

### Findings from inspecting the 8 files

1. **The per-unit CSS-color system is already failing silently.**
   - Unit 2 uses root classes `call`, `king` with no color defined → render gray.
   - Unit 3 uses `wild`, no `--c-wild` → gray.
   - **Unit 7 defines Units 2–3's palette but its text uses a completely
     different root set** (`ask build do enter eye fruit judge measure way`) →
     *every colored word in Unit 7 is uncolored.*
   - `--c-dream` = `#2f6db3` in units 1–3 but `#0e8aa0` in unit 7 (drift).
   - Unit 1 has no legend and no endnotes (predates those components).
2. **Every unit's shared CSS core has drifted** — no two `<style>` blocks match
   even after stripping color vars. Needs one canonical stylesheet + per-unit
   render check.
3. **Greek script split.** Units 1–7 are dense with native Greek (`<span
   class="gk">…</span>`, 31–76 uses each, ~370 total). **Unit 8 — the most recent
   rebuild — has zero.** Unit 8 is the model of where the project is heading.
   Decision taken: **translit only** (option a). Units 1–7 need a script-strip pass.
4. **Only 8 of 16 threads are tagged anywhere.** `nations`, `apo-tote`,
   `law-prophets`, `little-faith`, `wise-foolish` fire in units whose markup has
   no matching tag. `light` is tagged in Unit 4 but not at its 5:14 / 6:23
   payoffs. Retrofitting those tags is scholarly judgment → Phase 4 gets a
   Lane-approves-the-tag-list step.

---

## Design decisions (locked)

### Color: kill per-unit `<style>`, resolve at runtime

Every colored word gets identical markup, no classes, no vars in the fragment:

```html
<span class="r" data-root="beget">begot</span>
```

`threads.js` resolves the color at load:

1. `data-root` in **`data/threads.json`** (the ~16 tracked threads)? → global
   color, identical in every unit, forever. Recolor book-wide = one hex edit.
2. Otherwise → that unit's **local palette** in `data/units.json`.

Promoting a root to global = add one line to `threads.json`. Demoting = delete it.
A `data-root` that resolves to no color anywhere = hard verify failure (Unit 7's
bug becomes structurally impossible).

### Data files: split "policy" from "fact"

| File | Authored how | Holds |
|---|---|---|
| `data/threads.json` | **hand-authored** | which roots are tracked; per-thread color, translit, gloss, origin unit, payoff unit(s), open/closed |
| `data/units.json` | **hand seed + generated** | title, passage range, discourse flags (seed); local palette, verse count (may be generated) |
| `data/occurrences.json` | **generated only** | which `data-root` fires in which unit, count, verse anchors — scanned from `/units/*.html` |

"Never hand-edit `/data`" is relaxed: it applies to `occurrences.json` (pure
derived fact). `threads.json` is policy nothing can derive.

### Verify

Each generator ships a sibling `verify_*.py` that re-derives the result
independently from the fragments (no importing the generator). Checks that matter:
every `data-root` resolves to a color; no two roots in one unit within a
perceptual-distance threshold; occurrence counts match a second scan.

### Other

- **Greek script:** translit only. Phase 1 strips `class="gk"` native-script spans
  from units 1–7, keeping the adjacent `(translit)`. Where a `gk` span has only an
  English gloss and no translit (legend rows), supply the translit.
- **Endnote ids:** prefix per unit at build or in source (`u07-n1`) so they stop
  colliding in a shared pane.
- **Rings/chiasms:** `.ring` markup stays and renders as static HTML. No JS
  interactivity this round (shelved, not deleted).
- **Paths:** all relative (`new URL('../data/x.json', import.meta.url)`), never
  root-absolute — GitHub Pages serves from a subpath.
- **Book-agnostic where cheap:** a Jonah project is planned on this structure;
  scripts avoid hardcoding "Matthew" / 28 where it costs nothing.
- **Desktop + mobile, both first-class.** Every phase ships responsive. Hover
  affordances (root tooltip) degrade to tap on touch; all other interaction —
  tabs, popovers, compare expand, footnote jump, search, dashboard — usable and
  legible at ~375px. No horizontal page scroll; wide diagrams/tables scroll in
  their own container.

---

## Phases

### Phase 1 — Extract & normalize ✅ DONE

`pipeline/extract_units.py` (+ `pipeline/greek.py` deterministic transliterator)
converts the 8 artifacts → `units/unit-01.html` … `unit-08.html`:

- Stripped `<head>`, fonts link, `<style>`. Body content only, wrapped in
  `<article class="unit" data-unit="N">`.
- `class="r beget"` / `class="beget r"` → `class="r" data-root="beget"`;
  bare local-colour spans → `class="rl" data-root="beget"`.
- All native Greek **and Hebrew** script removed — 314 transliterations
  synthesised, 4 hand-corrected (`shamayim`, `ḥoba`, `ḥanef`, dropped `netzer`),
  redundant echoes cleaned. Zero script chars remain in any fragment.
- `.greek-title` mastheads rebuilt as `<span class="translit">` + optional
  `<span class="tsub">` gloss.
- Endnote ids/hrefs prefixed `u0N-nK`. All refs resolve (source U04 is missing
  its own `n7` — pre-existing, logged, not ours to fix here).
- `pipeline/out/units.seed.json` — per-unit local palette, roots used, unused
  palette entries, title, passage.
- `pipeline/out/extract-report.md` — every synth/manual/drop, for spot-check.

Originals untouched; copies in `source-artifacts/`. Prose never edited.
**Known colour gaps carried to Phase 4:** U2 (`call`→name, `king`→david),
U3 (`wild`→`wilderness` rename), U7 (needs a full fresh 9-hue palette — its
`<style>` was a stale copy of U2/3's).

### Phase 2 — The shell ✅ DONE

- `css/styles.css` — one reconciled stylesheet: app chrome + the superset of all
  8 artifacts' component CSS; chrome colours moved to stable `--accent-*` tokens.
  Responsive ≤720px. Google-fonts `<link>` in `index.html`.
- `data/units.json` — 28-unit manifest + local palettes for the 8 built (with the
  U2/U3/U7 colour fixes folded in).
- `index.html` — sticky topbar, collapsible 28-unit Contents nav, content pane.
- `app/main.js` — hash router (`#/unit-03`, `#/unit-03/u03-n5`), per-unit
  `[data-root]` colour injection from `units.json`, prev/next pager, footnote
  jump + flash + click-again-to-return.
- Verified in-browser: 8 units render, palettes inject (U7 fixed), footnote jump
  works, no horizontal overflow at 375px.

<details><summary>original Phase 2 plan</summary>

- `index.html` — tab shell.
- `app/main.js` — tab router, loads a fragment into the content pane, handles
  the prefixed endnote anchors.
- Renders all 8 units correctly. First thing Lane can click.

</details>

**Run locally:** `python -m http.server 4180` in the project root, then open
`http://localhost:4180`.

### Phase 3 — Git + GitHub Pages ✅ DONE

`git init -b main`, `.gitattributes` (`eol=lf`), `.gitignore`. First commit
`ff46900`, pushed to **github.com/lanehaden157/Matthew** (public). Pages enabled
(main / root) → **https://lanehaden157.github.io/Matthew/**. Verified live on the
`/Matthew/` subpath: fragments load, palettes inject, footnote jump works,
`data/units.json` fetches, zero console errors — relative paths hold.

### Phase 4 — Colour engine + threads ✅ DONE

- `data/threads.json` — 16 tracked threads (13 from memory + torment/urge/sea).
  Global tier: a root here holds its thread colour in every unit; recolour
  book-wide = one hex edit.
- `data/units.json` roots are now `{color, translit, gloss}`, backfilled from the
  fragments' hand legends (`pipeline/extract_legends.py` + `legend-overrides.json`).
- `pipeline/scan_occurrences.py` → `data/occurrences.json`;
  `pipeline/verify_occurrences.py` independently re-counts and checks every
  `data-root` resolves to a colour with no perceptual collisions.
- `pipeline/apply_retrofit.py` (`retrofit-tags.json`) added the tracked-thread
  spans the artifacts never marked: nations 4:15, apo-tote 4:17, law-prophets
  5:17 & 7:12, little-faith 6:30, light 5:14 & 6:23, wise-foolish 7:24/26; retag
  8:26 faith→little-faith; unwrapped a mis-tagged "deportation" in U1.
- `pipeline/build.py` runs the whole chain.
- `app/threads.js` resolves colours and rebuilds each unit's legend from data
  (thread pills, occurrence counts). Fetches are cache-busted.
- Verified on the live Pages deploy: retrofit tags render, global thread colours
  identical across units, zero console errors.

### Phase 5 — Thread & note interactions *(ideas.md "Now")*

- Root hover → light gloss-only tooltip (desktop; tap-equivalent on mobile).
- Root click → popover: translit + gloss + count-in-this-unit + (if tracked)
  trajectory with jump links to built units.
- "Threads active here" footer on every unit, linking to the dashboard.
- **Footnote jump + return:** click an endnote ref → smooth-scroll to the note
  and flash-highlight ~1s; clicking the ref again (or the note's back-link)
  returns to the exact verse and flashes it. Plain anchor without JS; highlight
  and return-to-origin are the JS layer.

### Phase 6 — Dashboard + concordance

- `dashboard.html` (or a tab) — one row per tracked thread, mini-timeline across
  the 28-unit map, open/closed, jump links. Canonical home of the global palette.
- Global concordance search — type a translit root or English gloss, get every
  tagged occurrence across every built unit with context snippets.

### Phase 7 — Compare boxes collapsed *(ideas.md "Now")*

Flag icon on translation-sensitive verses; click to expand the wooden / NASB /
Hart / Lattimore box inline, collapse when done. CSS/JS over existing `.compare`
markup — no fragment edits.

### Phase 8 — Persistence

`app/store.js` — versioned `localStorage`: mark units read, per-verse personal
notes. Schema version gate for future migration. No backend, no accounts.

### Phase 9 — Author ergonomics *(payoff for units 9–28)*

- `pipeline/port_artifact.py` — drop a fresh artifact in, one command produces the
  fragment (script strip, tag rewrite, id prefix, legend removal).
- Rewrite `matthew_study_style_reference.md` §1–4: future artifacts emit
  `data-root` directly, skip the `<style>` block, skip the hand legend, translit
  only. Point thread tracking at `threads.json` instead of memory.
- Unit 9 is the first test of the ported path.

---

## Shelved (saved, not cancelled)

Ring/chiasm JS interactivity · isolate-thread toggle · chiastic reading-order
toggle · synoptic side-panel · root-density sparkline · book-level heatmap ·
bookend split-view · word-level diff in compare · devotional layer ·
Constable-tension flag.

---

## Open question for Lane

**Phase 1 Greek-script strip — confirm the approach.** Units 1–7 have ~370 native
Greek spans. Options:

- **(a1) Strip to translit** — smallest, permanent, matches Unit 8. Recommended.
- **(a2) Keep script in source, hide by default with a toggle** — reversible, but
  adds a feature and a data attribute to carry; Greek stays available for later.

Everything else above is considered locked unless you flag it.
