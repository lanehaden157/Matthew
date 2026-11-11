# Matthew

@biblecore/BOOK_CLAUDE.md

Above = shared guide (commands, files, chat side, threads). Below = what
Matthew does differently; it wins. 28-unit study, live at
https://lanehaden157.github.io/Matthew/ .

## Boxed units 1-13

Shipped before Matthew moved onto core; stamped `"contract": "legacy"`
(ARCHITECTURE §5). No versioned fragment check, `migrate` leaves them alone,
prose and structure stay as built. A new thread still gets tagged into them
through `retrofit` and `data-w`, never by re-porting. Diff a boxed unit before
committing: a change beyond tags is a stop. Units 14 on go through core's
loop. Pre-core state: tag `pre-revert-2026-09-29`.

## Matthew-only

    python -m biblecore lxx Isa 22:22 [--expect petra '!kleis']  # an LXX verse's lemmas; '!x' = must be absent
    python -m biblecore lxx --checks 17  # run a unit's checks[]
    python tools/constable_index.py      # constable-index.md (see the script's docstring)

- Fresh clone: `python -m biblecore fetch` once, then `corpus`.
- Synced extras (`book.json` `sync.extra`): `MatthewSBLGNT.txt` (the project's
  copy must match byte for byte), `MatthewWEB.txt`, `constable-index.md`.
  `Matthew-words.tsv` and `MatthewSBLGNT.txt` hold native Greek: never copy it
  into chat, handoffs or fragments.
- `port` prints a unit's `checks[]` (run them against the corpus; not for
  Lane) and `threads.promote[]` (written into the thread delta). Neither is
  stored after the port. Check the delta's rows citing the unit's verses
  against the unit map.
- Promoting into built units: `docs/retrofit.md`.
- Git Bash on Windows mangles inline Unicode in `bash -c`: put regex and
  Unicode work in `.py` files.

## Corpus

SBLGNT via MorphGNT plus the LXX, pinned in `book.json` and
`biblecore/fetch.py`. `python -m biblecore corpus` gives 1,068 verses, 18,329
words, 1,680 lemmas; drift → check against a printed SBLGNT.
`Matthew-words.tsv` and `Matthew-reading.txt` are generated.
