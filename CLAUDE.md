# Matthew Study — Project Guide

A 28-unit literary-canonical study of Matthew, implemented as a static site.
The `/units` fragments are hand-authored prose (reviewed like prose); `/app` and
`/data` are the engine that renders them.

**Roadmap and rationale live in `PLAN.md`.** Read it plus `session_index.md` at
the start of each session. This file is the standing architecture; PLAN.md is the
phase plan and the record of decisions.

## Status (2026-09-19)

- Live at https://lanehaden157.github.io/Matthew/ . Units 1–11 built. **Phases 1–9
  done.** Next content unit: **Unit 12 (Matt 12:1–50)**.
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
- `translation-choices.md` (hand-maintained) is the wording glossary the research
  project reads. **Keep it current as part of the normal workflow, not as a
  separate ask**: any session that changes a rendering (a word choice for a
  Greek lexeme, or a general style convention like `y'all`/`sky-skies`) updates
  the relevant row/bullet and the Log section in the same turn, before moving
  on — the same way `build.py` gets run without being asked. See
  "For the Claude.ai research project" below for the paste-ready instructions.

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
translation-choices.md  hand-maintained glossary of deliberate English
               renderings — the wording counterpart to threads.json. The
               Claude.ai research project reads it too. Kept current as part
               of the normal workflow (see Working notes), not regenerated.
/pipeline/     greek.py          deterministic Greek→Latin transliterator.
               unit_meta.py      the unit-meta block: parse / validate / generate.
               port_artifact.py  drop ONE new artifact in → fragment + data merge
                                 + thread-delta report. `--backfill` did units 1–8.
               extract_units.py  Phase-1 batch normalizer. Done its job; now just
                                 a library port_artifact.py imports. NOT a build
                                 step — re-running it drops post-extract edits.
               apply_retrofit.py replay retrofit-tags.json (+ generated
                                 retro-tags.json) onto units/*.html (idempotent;
                                 the edit record + safety net).
               retro-tags.json   generated — fixes for EARLIER units that a
                                 later unit's `threads.retro` meta block flagged;
                                 port_artifact.py merges them here (dry-checked
                                 first). Hand-authored edits go in retrofit-tags.
               refresh_meta.py   resync built fragments' meta blocks with the data.
                                 NOTE: units.json wins here. Fragments are the
                                 source of truth for prose and tagging, but the
                                 meta `roots[]` translit/gloss is regenerated
                                 FROM data/units.json — edit a legend entry
                                 there, not in the fragment, or the next build
                                 reverts you.
               threads_digest.py threads.json → threads-digest.md.
               palette.py        the colour policy in one place: both distance
                                 metrics, the thresholds, the chrome accents
                                 read out of styles.css, the co-occurrence
                                 graph, and the candidate search. Read its
                                 docstring before touching any colour rule.
               assign_color.py   pick a colour for a new root instead of
                                 guessing one: `assign_color.py <root>` for a
                                 thread, `--unit N` for a local root (a much
                                 weaker constraint), `--audit` for how much
                                 room is left.
               check_project_sync.py  TRACKED_FILES (the files that have to
                                 round-trip into the Claude.ai project) + the
                                 upload-only fallback: hash-diff what needs
                                 re-pasting.
               sync_to_github.py refresh project-side/synced/ from TRACKED_FILES.
                                 build.py runs it `--copy-only`, so the mirror
                                 never commits or pushes by itself.
               thread-stems.json + audit_thread_coverage.py  Greek-root coverage
                                 audit: scans MatthewSBLGNT.txt, flags tracked
                                 roots present in a built unit but untagged.
               build.py          replay retrofit → refresh_meta → scan → verify →
                                 digest → project-side mirror → coverage audit.
                                 Fragments are the source of truth; it never
                                 rebuilds them.
               scan_*.py         regenerate /data from the fragments.
               verify_*.py       independently re-derive the same result (no
                                 importing the generator) — run both before trusting.
               out/              generated seed + reports (git-ignored).
/project-side/ README.md   index of the files that have to round-trip into the
                           Claude.ai research project, and which is canonical.
               synced/     generated flat mirror of those files, pushed to
                           GitHub so the project's connector pulls them itself.
                           Never hand-edit. No scheduled task on purpose.
               sync-state.json  hashes for the upload-only fallback path.
/docs/audit/   port-analysis.md  the 2026-09-12 audit behind the Joshua fork.
               archive/    superseded planning docs, banner-marked. History,
                           never instructions.
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

**Colour separation is a per-unit rule, not a book-wide one.** Two roots must
look different when they appear on the same page; two roots that never share a
unit may sit close. That is what scales — 95 roots carry a colour, only 37% of
pairs ever share a unit, and the densest page holds 27. Twenty-seven
distinguishable colours is comfortable; ninety-five is not. Three things are
still hard failures book-wide: two threads sharing a hex (the legend and the
concordance identify a thread by its colour), any root within dE00 6 of a chrome
accent, and a root that resolves to nothing. **Chrome is deliberately
low-chroma** — saturated colour means "this word is that word again", so the
furniture doesn't get to borrow it. Don't pick a new colour by eye; run
`python pipeline/assign_color.py <root>`.

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

`MatthewSBLGNT.txt` (SBLGNT Greek of Matthew, whole book, `Matt C:V\t<text>`
lines) is in the repo root — `pipeline/audit_thread_coverage.py` reads it.
Everything else (NASB, Constable, Bible Project notes, Mark/Luke/John
comparisons) is research that lives in the Claude.ai project, not on disk. The
`/units` fragments are the *output* of that research. Nothing outside the
Matthew project folder is needed.

## Session Context System (Lane's global convention)

- `session_index.md` — running index, 3 lines max per session. Read FIRST.
- `improvements_log.md` — append-only log of concrete changes. Check before
  duplicating past work.
- `session_summary_[timestamp].md` — full summary at the END of each session; new
  file each time, never overwrite.

## For the Claude.ai research project (paste into its project instructions)

Copy everything between the lines below into the research project's own
instructions field, verbatim:

---START PASTE---
The authoritative copies of four files live in the site repo
`github.com/lanehaden157/Matthew` under `project-side/synced/`, which this
project's GitHub connector syncs. Read them from there rather than from an
uploaded copy or from memory:

- `matthew_study_style_reference.md` — the artifact contract (fragment shape,
  unit-meta schema, components, transliteration, the 28-unit map)
- `threads-digest.md` — which roots are tracked threads and the `data-root`
  id each uses
- `translation-choices.md` — the agreed English rendering per Greek lexeme
- `MatthewSBLGNT.txt` — the Greek text, byte-identical to the repo's copy

To find one: browse `project-side/synced/` in the repo through the connector,
or search the repo for the filename. `project-side/README.md` is the index —
it names the canonical repo path behind each mirrored file. Everything under
`synced/` is generated, never hand-edited, so it is the repo's current state
rather than a snapshot. If a synced file and an uploaded copy disagree, the
synced one wins, and say so in the reply instead of quietly picking one.

Before rendering a Greek word in a new unit's translation, check
`translation-choices.md` for a prior decision and match it. If a different
rendering genuinely fits better in a specific verse, use it — but flag it
explicitly in the artifact (a note, or in the thread-delta) rather than
silently drifting, so Lane can decide whether it's a one-off exception or a
correction that should propagate everywhere.
---END PASTE---

## Working notes

- Ask Lane for clarification on design/scope before going deep — cheaper than
  guessing.
- Guidance here is strong suggestion, not hard rule; rebuild what doesn't work.
- This shell (Git Bash on Windows) mangles inline Unicode in `bash -c` — put
  regex/Unicode work in `.py` files.
