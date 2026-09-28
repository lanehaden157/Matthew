# Matthew Study — Project Guide

A 28-unit literary-canonical study of Matthew as a static site, live at
https://lanehaden157.github.io/Matthew/ . The `/units` fragments are hand-authored
prose (reviewed like prose); `/app`, `/data` and `/pipeline` are the engine that
renders them. Research happens in a Claude.ai project; its output lands here.

## Start of a session

Read `session_index.md` (what recent sessions did, and the next unit) and `PLAN.md`
(phases, locked decisions, tracked backlogs). `improvements_log.md` before changing
something that might already have been done.

## Where things live

| For… | Read |
|---|---|
| What each pipeline script does | its module docstring. Start with `build.py` (the full rebuild, in order) and `port_artifact.py` (bringing in a new unit) |
| The artifact contract: fragment shape, unit-meta schema, components, checklist, 28-unit map | `matthew_study_style_reference.md` |
| The research workflow (four passes) — also the text Lane pastes into the Claude.ai project's instructions field | `instructions.md` |
| What round-trips to the research project, and how | `project-side/README.md` |
| Colour policy: metrics, thresholds, what's a hard failure | `pipeline/palette.py` docstring; pick colours with `assign_color.py`, not by eye |
| Tracked threads | `data/threads.json` (hand-authored policy) → `threads-digest.md` (generated) |
| English renderings per Greek lexeme | `translation-choices.md` |
| Design decisions and their rationale | `PLAN.md` "Design decisions"; `docs/audit/` for the 2026-09-12 audit (`archive/` is history, not instructions) |

## Everyday workflow

- **New unit:** `python pipeline/port_artifact.py NN`, review
  `pipeline/out/thread-delta-NN.md`, Lane eyeballs it in the browser, commit.
- **Anything else that touches fragments or `/data`:** run `python pipeline/build.py`
  without being asked. It refreshes the generated files and the `project-side/synced/`
  mirror; commit the mirror with the change that caused it.
- **Changing a rendering** (a word choice, or a convention like y'all or sky/skies):
  update `translation-choices.md`'s row and Log section in the same turn.
- **Editing a built unit's legend (translit/gloss):** edit `data/units.json`, not the
  fragment. The build regenerates it from there (see `refresh_meta.py`).
- **Fresh clone:** `python pipeline/fetch_corpus.py` once, for `canon_leads.py`.

## The site shell and bible-core (since 2026-09-26)

The site runs bible-core's template shell, the one Numbers and Joshua run:
`index.html`, `app/*.js`, and `css/core.css` + `components.css` +
`division.css` (all generated) + `css/theme.css` (Matthew's own rings,
triads, exodus tables, prayer block, Greek title). `css/styles.css` and the
forked `app/` are in git history.

- `book.json` + a vendored `biblecore/` drive the shell and its reader data:
  `python -m biblecore corpus` (MorphGNT word table), `emit` (interlinear,
  search text), `assets` (css, `data/components.json`), `manifest`. Run
  `emit` + `manifest` after porting a unit.
- Units are still ported and built with `pipeline/` (above). Moving the pipeline
  onto core is its own job (phase E).
- `python -m biblecore test` is safe to run here (since phase D, 2026-09-28): it
  puts back anything it touches. It passes 7 of 8. `idempotent` fails because
  core's refresh writes a different meta block (adds `contract`, `discourse`,
  blank `note`s) and digest paragraph than `pipeline/refresh_meta.py` and
  `threads_digest.py` do, and each build reverts the other's. That goes away
  when one generator matches the other.
- Still don't run `python -m biblecore build`, `port` or `migrate` here.
  `build` rewrites the meta blocks and digest into core's form, which the old
  build then reverts. `migrate` would stamp the units, and a stamp at or past
  0.3.0 switches on core's `itin` rule: a stop's `<sup>` must be a verse. Matthew
  uses those sups as labels ("Micah", "Sermon", "God acts"), which is 25 errors
  in units 2, 4, 6, 7, 9 and 12. Unstamped units count as 0.2.0, which passes.
- Discourses are the shell's "overlay" grouping (`book.json` `overlay`);
  `data/units.json` holds movements and discourses as `groupings`.
- `.compare` and `aside.synoptic` are core components with their own chips (✦, ✧).
- Take shell updates from `../bible-core/template/app/`; update core with
  `python ../bible-core/tools/core_sync.py .`.
- **Interlinear glosses (core 0.9.2, plan D1):** `pipeline/corpus/lexicon/lexemes.yaml`
  (MorphGNT's morphological lexicon; `python pipeline/fetch_corpus.py` fetches it,
  `book.json` `paths.greek_lexicon` points at it) -- `emit` reads it. 100% coverage
  on Matthew's own words.
- **Phrase threads (core 0.9.2, plan D2):** `data/roots.json` can give a thread with
  no single lemma (son-of-man, apo-tote, ...) a `"seq"` instead of `"ids"` -- see
  `bible-core/ARCHITECTURE.md`. Matthew doesn't have `data/roots.json` yet (still
  `pipeline/thread-stems.json`'s stem matching) -- that conversion is plan B, still open.
- **Canon leads (core 0.9.2, plan D4):** `python -m biblecore leads` now works here
  too (the LXX + rest-of-NT path, ported from `pipeline/canon_leads.py`, proven
  against it). `pipeline/canon_leads.py` is still the one `pipeline/build.py` calls;
  switching over is part of retiring `pipeline/` (plan E), not done yet.

## Guardrails worth keeping in mind

Rationale for each is in `PLAN.md`. These are strong defaults, not laws. Raise it with
Lane if one stops fitting.

- Content and engine stay separate: `/app` never hardcodes unit content, and fragments
  carry no styling or app logic.
- Colour is resolved at runtime from `data-root`. There's one Greek lexical root per
  root, with no themes or bundles. Fixed titles Matthew repeats verbatim are the
  exception, and they live in `threads.json`.
- Every `/data` generator has an independent `verify_*.py`. Run both.
- There's no JS build step. Use relative paths only, because Pages serves from a subpath.
- Persistence is `localStorage` only, with no backend.
- Transliteration only, never native Greek or Hebrew script in the rendered site.
- Desktop and mobile (~375px) are both first-class, with no horizontal page scroll.
- Generated files are never hand-edited: `occurrences.json`, `threads-digest.md`,
  `canon-leads/`, `project-side/synced/`.

## Working notes

- Ask Lane about design or scope before going deep. It's cheaper than guessing.
- Lane does the visual checks in the browser.
- Git Bash on Windows mangles inline Unicode in `bash -c`. Put regex and Unicode work
  in `.py` files.
- Session context files (`session_index.md`, `improvements_log.md`,
  `session_summary_[timestamp].md`) follow Lane's global convention.
