> **ARCHIVED — historical, superseded by the Joshua repo.**
> Written 2026-09-12 as the plan for forking Matthew into a Hebrew book, before
> Joshua existed. Joshua was then built and diverged from this plan in ways that
> matter: root identity moved from substring stems to lexicon-id sets (`roots.json`
> + `data-w`), `candidates[].stems` is gone, the `greek-title` masthead and the
> `<p id="n1">` endnote shape were both replaced. **Read this as a record of what
> was intended, never as instructions.** The live documents are in the Joshua repo
> (`../Joshua/`), and the current cross-project plan is `platform-design-review.md`.

# Joshua Study — Project Guide

> **This file is the draft `CLAUDE.md` for the Joshua repo.** It lives here in
> the Matthew repo until the fork happens; at that point it moves to the new
> repo's root and this copy becomes historical. Placeholders marked `TODO` are
> decisions that must be made at bootstrap, not carried over.

A literary-canonical study of Joshua, implemented as a static site. Forked from
the Matthew study (`lanehaden157/Matthew`), which shipped 11 of 28 units before
this fork. The `/units` fragments are hand-authored prose (reviewed like prose);
`/app` and `/data` are the engine that renders them.

**Roadmap and rationale live in `PLAN.md`.** Read it plus `session_index.md` at
the start of each session. This file is the standing architecture; PLAN.md is the
phase plan and the record of decisions.

Everything below marked **(learned)** exists because something broke in Matthew.
The commit is cited. Do not relax one of these without reading the commit first.

## Status (TODO: date)

- TODO: live URL. Units 0 built.
- Colour policy: one Hebrew lexical root per `data-root` (root + same-root forms
  only) — no themes, formulae, or bundles. Exception: fixed phrases the book
  repeats verbatim live in `threads.json`.
- Research continues in the Claude.ai project; the artifact it produces is a
  **drop-in fragment**. Port it with `python pipeline/port_artifact.py NN`,
  review `pipeline/out/thread-delta-NN.md`, eyeball in the browser, commit.
- `threads-digest.md` (generated) is the thread list the research project reads;
  refresh it there when `data/threads.json` changes.
- `translation-choices.md` (hand-maintained) is the wording glossary the research
  project reads. **Started at unit 1, not later.** Any session that changes a
  rendering — a word choice for a Hebrew lexeme, or a general convention —
  updates the relevant row and the Log section in the same turn, before moving
  on, the same way `build.py` gets run without being asked. **(learned:** Matthew
  started this file at unit 10 and paid for it with a full wording-audit session
  and a retroactive pass — commits `b0f73cc`, `aed087e`, `0138548`.**)**

## Layout

See `docs/next-project/ARCHITECTURE.md` in the Matthew repo for the fork
boundary — which files were copied verbatim, which were modified, and which were
deliberately left behind.

```
/units/        HTML fragments, one per literary unit (unit-01.html …). One
               <article class="unit" data-unit="N"> opened by a
               <script type="application/json" id="unit-meta"> block. No <head>,
               no <style>. Prose reviewed like prose.
/data/         threads.json      hand-authored ONLY — the tracked cross-unit
                                 threads. Policy; nothing derives it, no script
                                 writes it.
               units.json        seed + generated — per-unit title, passage,
                                 local root palette, book metadata.
               occurrences.json  generated only. Never hand-edit.
threads-digest.md       generated from threads.json. Never hand-edit.
translation-choices.md  hand-maintained glossary of deliberate English
                        renderings. Kept current as part of the normal workflow.
/pipeline/     hebrew.py         deterministic Hebrew→Latin transliterator.
                                 See docs HEBREW-TRANSLITERATION.md.
               unit_meta.py      the unit-meta block: parse / validate / generate.
               port_artifact.py  drop ONE new artifact in → fragment + data merge
                                 + thread-delta report.
               apply_retrofit.py replay retrofit-tags.json (+ generated
                                 retro-tags.json) onto units/*.html (idempotent).
               retrofit-tags.json  hand-authored fragment edits.
               retro-tags.json     generated — fixes for EARLIER units flagged by
                                 a later unit's `threads.retro` meta block.
               refresh_meta.py   resync built fragments' meta blocks with the data.
               threads_digest.py threads.json → threads-digest.md.
               thread-stems.json (or thread-lemmas.json — TODO, see below) +
               audit_thread_coverage.py   root-coverage audit against the Hebrew
                                 source text.
               build.py          replay retrofit → refresh_meta → scan → verify →
                                 digest → coverage audit. Fragments are the
                                 source of truth; it never rebuilds them.
               scan_*.py         regenerate /data from the fragments.
               verify_*.py       independently re-derive the same result.
               out/              generated reports (git-ignored).
/app/          main.js     tab router.
               threads.js  colour resolution + thread popover/concordance.
               store.js    localStorage — reading progress, personal notes.
/css/styles.css  the one shared stylesheet.
/source-artifacts/  untouched copies of the incoming research artifacts.
index.html     entry point / tab shell.
```

---

## Locked design decisions

### Two-tier colour, resolved at runtime **(learned)**

Every coloured word is `<span class="r" data-root="X">…</span>` (an occurrence)
or `<span class="rl" data-root="X">…</span>` (root-linked, not counted). At load,
`threads.js` colours it: if `X` is in `threads.json` → that thread's fixed global
colour, identical in every unit. Otherwise → this unit's local palette in
`units.json`. Promoting a root to global = one line in `threads.json`. Recolouring
a thread book-wide = one hex edit. **A `data-root` that resolves to no colour is
a hard verify failure.**

> **Why.** Matthew's original design baked colour into per-unit CSS. Unit 2 used
> root classes with no colour defined (rendered gray, no error). Unit 7 defined a
> palette matching Units 2–3's roots while its text used a completely different
> root set, so *every coloured word in Unit 7 rendered uncoloured* — silently,
> across seven files, until someone went looking (`PLAN.md:30-37`). This one
> finding produced the runtime resolver, the hard-fail rule, and the entire
> generate+verify discipline below.

### Generate + verify **(learned)**

Every script that writes into `/data` ships a sibling `verify_*.py` that
re-derives the same fact **by a different method** and refuses to proceed on
mismatch. `verify_occurrences.py` deliberately does not import
`scan_occurrences.py` — it recounts with a line-oriented tokeniser "so a bug in
one approach doesn't hide in both." Run both.

> **Why.** Same bug as above. It cost a few dozen lines per pair to prevent and
> shipped silently across seven files without it. **Write the verifier before or
> alongside the first generator, not after** — in Matthew it was written after,
> which is why the bug existed to be found.

### The fragments are the source of truth; the generator never re-runs **(learned)**

`units/*.html` is authoritative. No script regenerates a fragment from
`source-artifacts/`. Adding a new unit is `port_artifact.py NN`, never a batch
re-extract.

> **Why.** Commit `9713a27`. Matthew's Phase-1 batch normalizer
> (`extract_units.py`) was wired in as `build.py`'s first step. By then every unit
> had accumulated direct hand edits — pericope headings, compare boxes, cut
> chiasms — that existed only in the committed fragment. Re-running the generator
> blew all of it away with no warning; **eight units diverged** before it was
> caught. The generator was retired to a library-only role and `build.py`'s
> docstring now says so loudly. Design this in from the start.

### `threads.json` is policy a human owns; no script writes it **(learned/kept)**

The porter can *propose* — `threads.candidates`, `threads.retro`, the
thread-delta report — and can never write `data/threads.json`. Every promotion of
a root to a cross-unit thread, every colour, every editorial note passes through
a human decision applied by hand.

> **Why.** Not a bug — a boundary. Which recurring word matters enough to track
> book-wide is the one genuinely subjective judgement in the system, and it is
> the thing most tempting to automate. Matthew enforced this in every code path
> and in printed output; it is the sharpest boundary in the design. Joshua has
> the identical category of call (which Hebrew roots deserve thread status) and
> needs the identical firewall.

### Ground truth is the source text **(learned)**

`audit_thread_coverage.py` scans the actual Hebrew and treats it as authoritative
over whatever the artifact happened to tag — never the English rendering, never
the fragment's own claims.

> **Why.** This is what caught Matthew's `sin` thread missing *hamartōlos* /
> "sinner" at 9:10–13 (commit `d95b5c4`), among many others. An audit that
> trusted the English, or trusted that the research project tagged what it meant
> to, misses all of them. This is the project's actual quality floor.

### Derive verse alignment from the source, never guess **(learned)**

The canonical `(chapter, verse)` sequence for a unit comes from the source text
file. Anything that won't line up is **reported, never inferred**.

> **Why.** Commit `d6185f8`. The audit originally guessed chapter rollover from a
> "verse number dropped → bump the chapter" heuristic and got it wrong on a
> set-piece verse skip. Joshua and Judges have their own versification
> irregularities across traditions; the discipline transfers even though the code
> needs rewriting.

### Idempotent, self-checking mutation ops **(kept)**

Every `apply_retrofit.py` op reports `ok` / no-ops if already applied, which is
why `build.py` can re-run the whole chain from a clean checkout at any time
(verified in `9713a27`: "running it twice from clean touches nothing"). Hard
requirement for any new mutation op.

### Hand-authored and generated fix-lists stay in separate files **(kept)**

`retrofit-tags.json` (hand) and `retro-tags.json` (generated) both feed
`apply_retrofit.py`, specifically so an automated merge never has to touch,
reformat, or risk corrupting the hand-authored one.

### Content vs. engine stay separate

`/app` never hardcodes unit content; `/units` never carries styling or app logic.
Adding a unit touches no app code; redesigning the UI touches no fragment.

### No build step

Plain ES modules, one file per concern. What's committed is what runs. Relative
paths only (`new URL('../data/x.json', import.meta.url)`) — GitHub Pages serves
from a subpath and root-absolute paths 404 in production.

### Persistence

`localStorage` only (reading progress, notes), versioned for future migration. No
backend, no accounts.

### Transliteration only

No native Hebrew script in the rendered page — **including attribute values**.

> **Why the attribute clause.** Matthew ships native Greek today in a
> `logeion.uchicago.edu/προσκυνέω` href inside `units/unit-08.html`, because the
> strip only ever covered element content. `verify_occurrences.py` here greps
> built fragments for Hebrew codepoints anywhere in the file.
>
> **The one exception:** `threads.candidates[].stems` in a meta block are
> *supposed* to be unpointed Hebrew — the porter consumes and drops them, so they
> never reach the page.

### Desktop and mobile are both first-class

Every phase ships responsive. Hover affordances degrade to tap; everything works
and reads at ~375px. No horizontal page scroll; wide diagrams and tables scroll
in their own container.

---

## Rules that exist because of a near-miss

These are new in Joshua. Each closes a hole the Matthew audit found open.

**A field the pipeline drops must produce an error.** `validate()` carries an
unknown-key check. Matthew's research project authored `descriptor` and
`discourse` in every v2 artifact for eleven units; both were documented in the
style reference, accepted by the validator, silently discarded by
`merge_units_json`, and consumed by nothing. Never ship an accepted-and-ignored
field.

**Every documented fragment-contract rule has a check, or it isn't a rule.**
Matthew's "every endnote `href` must resolve to an `id` in the same fragment" had
no check anywhere. If a rule is worth writing in the style reference, it is worth
five lines in `verify_occurrences.py`. If it isn't worth five lines, delete the
rule.

**A required component missing is as bad as a wrong one present.** Matthew's
Unit 11 shipped with no `<section class="block legend">`, so the live site renders
it with no colour key while every other unit has one. `app/threads.js` *fills* a
legend and returns early if there is none — it never creates one. Nothing
reported it. The porter now checks for the legend, and `build.py` runs a
component-whitelist check (classes used in fragments that `css/styles.css` never
mentions, and required classes absent).

**Run `--forms` on every stem before committing it.** Not just suspicious ones.
Hebrew prefix stacking means every root over-matches more than its Greek
counterpart, so `exclude` is load-bearing from day one.

**Be tough on structures.** Chiasms and rings must be real and verifiable.

> **Why.** Commit `e9105a5` cut eight previously-published chiastic structures
> across seven Matthew units as over-reaching — a scholarly-judgement failure
> that repeated until it became a standing instruction. Narrative books invite a
> *different* version of this: Judges' cycle refrain is real and textually
> marked, but secondary chiasms imposed on narrative episodes are exactly what
> Matthew's experience warns against. Carry the caution; expect the specific
> failure to look different.

**Resist the richer taxonomy.** Everything tracked is a plain root: one
`data-root` slug, one colour, the word-family spelled out in the `translit`
string.

> **Why.** Commit `8d096c9` built a two-tier root/motif taxonomy — `kind`,
> `members` arrays, a third legend section, different underline styles, changes
> across `threads.json`, `units.json`, every fragment, `threads.js`, and the style
> reference. Commit `98b721a` reverted all of it the same day as complexity the
> data didn't need. `unit_meta.py` still actively rejects the old shape. Hebrew
> will have its own version of this temptation — root vs. binyan vs. semantic
> field. Read the revert before reaching for it.

**Any splice/insert tool must track open/close depth.**

> **Why.** Commit `67b2712`. Matthew's synoptic-box splice inserted asides inside
> an unclosed `.gloss` span or `.compare` div in eight places across six units, so
> the renderer collapsed them into generic note markers. Silent degradation, no
> error.

**Verify this file against reality periodically.**

> **Why.** Commit `daf5710`. Matthew's `CLAUDE.md` pointed at an external path
> that no longer held anything the project needed. Standing-instruction files are
> not self-verifying; this one drifted once and was caught by inspection, not by
> any check.

---

## Source text

TODO at bootstrap. Requirements:

- A pointed Hebrew text of Joshua, one verse per line, tab-separated
  `Josh C:V<TAB>text`, in the repo root and tracked.
- `data/units.json` carries `book`, `source_text`, and `verse_prefix`; the audit
  reads all three rather than hardcoding them.
- **Decide ketiv/qere handling before the first unit** — which form the audit
  matches against, and whether the artifact ever shows both.
- **Decide stems vs. lemmas before the first thread** — see
  `HEBREW-TRANSLITERATION.md` §3.2. Hebrew's I-nun assimilation, hollow roots,
  and III-he roots make substring stems miss forms in which the radical is
  physically absent (נתן → יִתֵּן has no nun). If the source carries OSHB lemma
  tags, match on lemma and keep stems only as a supplement.

Everything else (English versions, commentaries, comparison texts) is research
that lives in the Claude.ai project, not on disk.

---

## Session Context System (Lane's global convention)

- `session_index.md` — running index, 3 lines max per session. Read FIRST.
- `improvements_log.md` — append-only log of concrete changes. Check before
  duplicating past work.
- `session_summary_[timestamp].md` — full summary at the END of each session; new
  file each time, never overwrite.

Seed all three on day one. Matthew's exist and demonstrably work; a repo that
skips them re-derives the same conventions by accident.

---

## For the Claude.ai research project

The project's instructions live in `docs/next-project/PROJECT-INSTRUCTIONS.md`
(in the Matthew repo) until the fork; after that, in this repo's
`instructions.md`. Copy them into the research project's instructions field
verbatim and re-sync whenever the contract changes.

Two sync points are manual and unenforced, exactly as in Matthew — the source
text ↔ research-project copy, and pasting `threads-digest.md` /
`translation-choices.md` into the project. Nothing detects drift if a paste is
skipped. This is intentional low-ceremony process, not a gap; just know it is
on you.

---

## Working notes

- Ask Lane for clarification on design/scope before going deep — cheaper than
  guessing.
- Guidance here is strong suggestion, not hard rule; rebuild what doesn't work.
  **Except** the **(learned)** items above — those cost something to find.
- Put regex/Unicode work in `.py` files rather than inline `bash -c`.
