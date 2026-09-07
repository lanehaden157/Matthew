# Matthew Study — Project Guide

A 28-unit literary-canonical study of Matthew, implemented as a static site.
The `/units` fragments are hand-authored prose (reviewed like prose); `/app` and
`/data` are the engine that renders them.

**Roadmap and rationale live in `PLAN.md`.** Read it plus `session_index.md` at
the start of each session. This file is the standing architecture; PLAN.md is the
phase plan and the record of decisions.

## Status (2026-09-07)

- Source research artifacts: units 1–8 exist (`source-artifacts/matthew_0N_translation.html`).
  Research continues in the Claude.ai project; new units arrive as artifacts and
  get ported in via `pipeline/`.
- **Phase 1 done** — 8 artifacts normalized into `units/unit-0N.html`.
- **Phase 2 next** — `index.html` shell + `app/main.js` router + `css/styles.css`.

## Layout

```
/units/        hand-authored HTML fragments, one per literary unit (unit-01.html …).
               Body content only, wrapped in <article class="unit" data-unit="N">.
               No <head>, no <style>. Reviewed like prose.
/data/         threads.json    hand-authored — the ~16 tracked cross-unit threads
                               (id, color, translit, gloss, origin unit, payoff
                               unit(s), open/closed). Policy; nothing derives it.
               units.json      seed + generated — per-unit title, passage, local
                               palette, discourse flags.
               occurrences.json  generated only — which data-root fires in which
                               unit, count, verse anchors. Never hand-edit.
/pipeline/     greek.py          deterministic Greek→Latin transliterator.
               extract_units.py  Phase 1 one-shot: artifact → normalized fragment.
               scan_*.py         regenerate /data from the fragments.
               verify_*.py       independently re-derive the same result (no
                                 importing the generator) — run both before trusting.
               out/              generated seed + reports (git-ignored).
/app/          main.js     tab router — loads a unit fragment into the content pane.
               threads.js  colour resolution + thread popover/concordance.
               store.js    localStorage — reading progress, personal notes.
/css/styles.css  the one shared stylesheet: chrome + the global thread palette vars.
/source-artifacts/  untouched copies of the original standalone artifacts.
index.html     entry point / tab shell.
```

## Locked design decisions

**Two-tier colour, resolved at runtime.** Every coloured word is
`<span class="r" data-root="X">…</span>` (an occurrence) or
`<span class="rl" data-root="X">…</span>` (root-linked, not counted). At load,
`threads.js` colours it: if `X` is in `threads.json` → that thread's fixed global
colour, identical in every unit. Otherwise → this unit's local palette in
`units.json`. Promoting a root to global = one line in `threads.json`. Recolouring
a thread book-wide = one hex edit. A `data-root` that resolves to no colour is a
hard verify failure.

**Content vs. engine stay separate.** `/app` never hardcodes unit content;
`/units` never carries styling or app logic. Adding a unit touches no app code;
redesigning the UI touches no fragment.

**Generate + verify.** Every script that writes `/data` ships a sibling
`verify_*.py` that re-derives the result independently from the fragments. Run
both.

**No build step.** Plain ES modules, one file per concern. What's committed is
what runs. Relative paths only (`new URL('../data/x.json', import.meta.url)`) —
GitHub Pages serves from a subpath and root-absolute paths 404 in production.

**Persistence:** `localStorage` only (reading progress, notes), versioned for
future migration. No backend, no accounts.

**Transliteration only** — no native Greek or Hebrew script anywhere in the
rendered units. Script may appear in `threads.json` / dashboard metadata later if
wanted (data-driven, zero fragment edits).

**Desktop and mobile are both first-class.** Every phase ships responsive. Hover
affordances degrade to tap; everything else works and reads at ~375px. No
horizontal page scroll; wide diagrams/tables scroll in their own container.

**Rings/chiasms** render as static HTML for now; interactivity is shelved, not cut.

## Source texts

Greek (SBLGNT), NASB, Constable, Bible Project notes, Mark/Luke/John comparisons
live outside this repo (Claude.ai project, and
`OneDrive/Documents/Personal/Biblical Texts/Gospels/`). The `/units` fragments are
the *output* of that research, not the research itself.

## Session Context System (Lane's global convention)

- `session_index.md` — running index, 3 lines max per session. Read FIRST.
- `improvements_log.md` — append-only log of concrete changes. Check before
  duplicating past work.
- `session_summary_[timestamp].md` — full summary at the END of each session; new
  file each time, never overwrite.

## Working notes

- Ask Lane for clarification on design/scope before going deep — cheaper than
  guessing.
- Guidance here is strong suggestion, not hard rule; rebuild what doesn't work.
- This shell (Git Bash on Windows) mangles inline Unicode in `bash -c` — put
  regex/Unicode work in `.py` files.
