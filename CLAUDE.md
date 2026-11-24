# Matthew (v2)

28-unit study of Matthew, live at https://lanehaden157.github.io/Matthew/ .
Everything runs in Claude Code; Lane's only part is answering calls.

- Build units: `/finish` (many, one session each) or `/unit N` (one).
- What to look for: `lens.md`. Who reads what: `.claude/agents/`; the unit
  skill only coordinates, so no context fills up.
- Fragment rules: `fragment-contract.md`, then `matthew_study_style_reference.md`
  (wins); markup `components-reference.md`; renderings `translation-choices.md`.
- Sources: `sources/` (gitignored), read through `python tools/kit.py`.
  After adding a source: `python tools/split_sources.py`.

## Commands (book root)

    python tools/unit_status.py [N]      # where units stand (all checkouts)
    python -m biblecore unit-pack N --out work/NN/pack.md
    python -m biblecore port N [--dry] [--promote]
    python -m biblecore lxx Isa 22:22 [--expect petra '!kleis'] | --checks N
    python -m biblecore audit | test [--quick] | build | data-w N

## Strong suggestions

- Units 1-13 are boxed (`"contract": "legacy"`): tags only, through
  `retrofit` and `data-w`, never a re-port. Diff a boxed unit before
  committing; a change beyond tags is a stop.
- Thread promotions: Claude decides, biased book-wide; close call → Lane.
  Colours from `python -m biblecore colour`. Every occurrence in built units
  needs `data-w`. Into built units: `docs/retrofit.md`.
- Questions for Lane → AskUserQuestion popups, recommended first and marked,
  four per call.
- Lane doesn't run commands or do visual checks in the in-app browser.

## Things to avoid

- Native Greek from `Matthew-words.tsv` / `MatthewSBLGNT.txt` in chat or files
  meant for reading.
- Editing `biblecore/` or generated files (`index.html`, `app/*.js`,
  `css/core.css`, `data/components.json`, `components-reference.md`,
  `fragment-contract.md`, `canon-conventions.md`). Look = `css/theme.css`.
- Inline Unicode in `bash -c` on Windows: put it in a `.py` file.
- `git add -A`: other sessions may share the repo; stage explicit paths.

## Session files

`session_index.md`: read first; standing state + last three sessions.
`history/`: past logs, read only if needed.
