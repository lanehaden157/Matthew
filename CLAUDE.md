# Matthew Study — Project Guide

A 28-unit literary-canonical study of Matthew, implemented as a static site.
The `/units` fragments are hand-authored prose (reviewed like prose); `/app` and
`/data` are the engine that renders them.

**Roadmap and rationale live in `PLAN.md`.** Read it plus `session_index.md` at
the start of each session. This file is the standing architecture; PLAN.md is the
phase plan and the record of decisions.

## Status (2026-09-08)

- Live at https://lanehaden157.github.io/Matthew/ . Units 1–10 built. **Phases 1–9
  done.** Next content unit: **Unit 11 (Matt 11:2–30)**.
- Colour policy: one Greek lexical root per `data-root` (stem + same-stem forms
  only) — no themes/formulae/bundles. Exception: fixed titles Matthew repeats
  verbatim (son-of-man, son-of-david, law-prophets, apo-tote) live in threads.json.
- Research continues in the Claude.ai project. As of Phase 9 the artifact it
  produces is a **drop-in fragment** (`matthew_study_style_reference.md` v2):
  one `<article>`, no `<head>`/`<style>`, a `<script id="unit-meta">` JSON block,
  `data-root` spans only. Port it with `python pipeline/port_artifact.py NN`,
  review `pipeline/out/thread-delta-NN.md`, eyeball in the browser, commit.
- `threads-digest.md` (generated) is the thread list the research project reads;
  refresh it there when `data/threads.json` changes.

## Layout

```
/units/        HTML fragments, one per literary unit (unit-01.html …). One
               <article class="unit" data-unit="N"> opened by a
               <script type="application/json" id="unit-meta"> block. No <head>,
               no <style>. Prose reviewed like prose.
/data/         threads.json    hand-authored — the tracked cross-unit threads
                               (id, root, color, translit, gloss, opens/payoffs,
                               open/closed). Policy; nothing derives it.
               units.json      seed + generated — per-unit title, passage, local
                               root palette + translit/gloss, discourse flags.
               occurrences.json  generated only — which data-root fires in which
                               unit, count, verse anchors. Never hand-edit.
threads-digest.md  generated from threads.json — the thread list the Claude.ai
               research project reads. Never hand-edit.
/pipeline/     greek.py          deterministic Greek→Latin transliterator.
               unit_meta.py      the unit-meta block: parse / validate / generate.
               port_artifact.py  drop ONE new artifact in → fragment + data merge
                                 + thread-delta report. `--backfill` did units 1–8.
               extract_units.py  Phase-1 batch normalizer. Done its job; now just
                                 a library port_artifact.py imports. NOT a build
                                 step — re-running it drops post-extract edits.
               apply_retrofit.py replay retrofit-tags.json onto units/*.html
                                 (idempotent; the edit record + safety net).
               refresh_meta.py   resync built fragments' meta blocks with the data.
               threads_digest.py threads.json → threads-digest.md.
               thread-stems.json + audit_thread_coverage.py  Greek-root coverage
                                 audit: scans MatthewSBLGNT.txt, flags tracked
                                 roots present in a built unit but untagged.
               build.py          replay retrofit → refresh_meta → scan → verify →
                                 digest → coverage audit. Fragments are the
                                 source of truth; it never rebuilds them.
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

**Transliteration only** — no native Greek or Hebrew script in the final rendered unit.html page. Use Latin morphology shorthand (`gen-`, `pist-`).

**Desktop and mobile are both first-class.** Every phase ships responsive. Hover
affordances degrade to tap; everything else works and reads at ~375px. No
horizontal page scroll; wide diagrams/tables scroll in their own container.

**Rings/chiasms** render as static HTML for now; interactivity is shelved, not cut.

## Source texts

NASB, Constable, Bible Project notes, Mark/Luke/John comparisons
live outside this repo (Claude.ai project) The `/units` fragments are
the *output* of that research, not the research itself. 

Greek (SBLGNT) lives in the repo for easy access

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
