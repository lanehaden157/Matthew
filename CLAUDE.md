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
  (Phase E: `biblecore port` can't take this over yet — see "Phase E" below.)
- **Anything else that touches fragments or `/data`:** run `python pipeline/build.py`
  without being asked. It refreshes the generated files and the `project-side/synced/`
  mirror; commit the mirror with the change that caused it. Under the hood this now
  runs `pipeline/apply_retrofit.py` then `python -m biblecore refresh`, `scan`,
  `verify-occurrences`, `digest`, then `pipeline/sync_to_github.py --copy-only`,
  then the advisory `python -m biblecore audit` and `leads`.
- **Changing a rendering** (a word choice, or a convention like y'all or sky/skies):
  update `translation-choices.md`'s row and Log section in the same turn.
- **Editing a built unit's legend (translit/gloss):** edit `data/units.json`, not the
  fragment. The build regenerates it from there (`python -m biblecore refresh`).
- **Checking what needs re-pasting into the Claude.ai project:**
  `python -m biblecore sync-check` (book.json now declares the file list).
- **Fresh clone:** `python pipeline/fetch_corpus.py` once, for `leads`.

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
- **Phase E (moving `pipeline/` onto bible-core) is underway.** `refresh`, `scan`,
  `verify-occurrences`, `digest`, `audit` and `leads` are live in `build.py` —
  see the "Everyday workflow" table above. Still blocked, with the reason in the
  phase E PR: `port` (rejects unit-13's `descriptor` meta key — a legit,
  undeclared field), `retrofit` (core's `retrofit/retrofit-tags.json` is missing
  most of `pipeline/retrofit-tags.json`'s hand-authored entries — a data
  migration, not a code swap), and `build`/`migrate`/`test` as a whole (`test`
  fails on ~6 units for reasons unrelated to the pipeline: inline `--c-*` colour
  vars, inline `style=`, leftover native Greek script, mismatched
  `aside.synoptic` anchors — fragment-content cleanup, tracked separately, not
  part of retiring `pipeline/`). Don't run those four here until that's cleared.
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
- **Canon leads (core 0.9.2, plan D4):** `python -m biblecore leads` is what
  `pipeline/build.py`'s advisory step calls now; `pipeline/canon_leads.py` is
  retired (phase E).

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
