# Matthew (v2)

28-unit study, live https://lanehaden157.github.io/Matthew/ . All in Claude Code. Lane only answers calls.

- Units: `/finish` (many) or `/unit N` (one). Study = unit session; check = `fact-checker`; build = `builder`.
- Lens: `lens.md`. Page rules (builder only): `fragment-contract.md`, `matthew_study_style_reference.md` (wins), `components-reference.md`, `translation-choices.md`.
- Sources: `sources/` (gitignored), via `python tools/kit.py`. New source → `python tools/split_sources.py`.

## Commands

    python tools/unit_status.py [N]
    python -m biblecore unit-pack N --out work/NN/pack.md
    python -m biblecore port N [--dry] [--promote]
    python -m biblecore lxx Isa 22:22 [--expect petra '!kleis'] | --checks N
    python -m biblecore audit | test [--quick] | build | data-w N

## Do

- Units 1-13 boxed (`"contract": "legacy"`): tags only via `retrofit` / `data-w`, never re-port. Diff before commit; change beyond tags = stop.
- Promotions: Claude decides, book-wide bias; close call → Lane. Colours: `python -m biblecore colour`. Every occurrence in built units needs `data-w`. Into built units: `docs/retrofit.md`.
- Lane questions → AskUserQuestion, recommended first, marked, four per popup.
- Lane runs no commands, does no in-app browser checks.

## Don't

- Native Greek from `Matthew-words.tsv` / `MatthewSBLGNT.txt` in chat or reader files.
- Edit `biblecore/` or generated files (`index.html`, `app/*.js`, `css/core.css`, `data/components.json`, `components-reference.md`, `fragment-contract.md`, `canon-conventions.md`). Look = `css/theme.css`.
- Inline Unicode in `bash -c` on Windows: use a `.py`.
- `git add -A`: stage explicit paths.

## Session files

`session_index.md` first. `history/` only if needed.
