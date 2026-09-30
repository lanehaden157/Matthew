# Session prompt: Matthew interlinear (pilot for core's Greek books)

Paste everything below the line into a new Claude Code session opened in
`Bible/Matthew`. It runs locally: it needs `pipeline/corpus/` (from
`fetch_corpus.py`) and read access to the sibling `../bible-core`.

---

Add an **interlinear reading mode** to Matthew: Greek word by word under each
verse. Matthew stays standalone (its own `app/` and `pipeline/`, reverted off
bible-core on 2026-09-29), so build it here. **It's also a pilot.** Lane expects
a later bible-core version for future Greek books (Luke, Revelation), so write
it to move into core with little change.

## Read first

- `session_index.md`, `CLAUDE.md` and `PLAN.md` "Reader features from the core
  shell". The 2026-09-30 session added the other reading modes, which this one
  extends: `MODES`, `applyMode`, `wireModes` in `app/main.js`, `body.mode-*` CSS
  in `css/styles.css`.
- **Core's existing Greek path: copy it, then adapt it.** Core already emitted
  a Greek interlinear for Matthew while Matthew was on core (0.7.0 Greek
  adapter, 0.9.2 glosses). Copy the relevant functions into Matthew's
  `pipeline/` and `app/`, then adapt them. Don't rewrite from scratch, and don't
  import or vendor the `biblecore` package (that dependency is what Matthew
  reverted). The adapting that's known to be needed:
  - `emit.py` reads core's `book`/`meta`/`roots` objects. Swap those for
    Matthew's `data/units.json` and the MorphGNT reader.
  - Transliterate with Matthew's `pipeline/greek.py`, not core's
    `lang/greek.py`. They're separate implementations, so output can differ
    from the pre-revert files; check any differences.
  - Cell links go to `#/search/<lemma>`, not core's `#/lemma/`.
  - Drop the Hebrew-only bits, such as the Aramaic `a` flag.

  The files to copy from:
  - `../bible-core/biblecore/emit.py`: the `data/words/<ch>.json` and
    `lemmas.json` shapes
  - `../bible-core/biblecore/corpus/morphgnt.py`
  - `../bible-core/biblecore/lang/greek_morph.py`: parsing codes to readable
    text
  - `../bible-core/biblecore/lang/greek_lexicon.py`: the dependency-free YAML
    reader
  - `../bible-core/corpus/README.md`: the lexicon's pinned commit and licence
  - `../bible-core/biblecore/web/app/reader.js`: `indexVerses`,
    `mountInterlinear`, `unmountInterlinear`
  - `../bible-core/biblecore/web/core.css`: the `.il` / `.il-w` rules
  - `../bible-core/biblecore/web/app/main.js`: the `SOURCES` footer
- **The output core produced for Matthew:** `git show
  pre-revert-2026-09-29:data/words/5.json` (and `lemmas.json`). It's a
  reference to diff against, not something to restore.

## Lane's decisions (2026-09-30)

1. **Data:** Matthew's own generator plus an independent verify script, both
   run by `build.py`.
2. **Cells like Joshua's:**
   - the transliterated word
   - a lexicon gloss from the MorphGNT morphological lexicon
   - the parsing in small text
3. **Plain cells:** no thread colour and no root popovers in the interlinear.
4. **Tapping a cell opens search for that lemma.**
5. **Search gains a "Greek words" block** for every lemma, tracked or not:
   - lemma, gloss and count
   - every Matthew reference, linked where the unit is built and dimmed where
     it isn't

   Tracked roots keep their existing coloured block above it. Joshua/Numbers'
   `sr-lemma` blocks are the model.

## Build

1. **Corpus.** Extend `pipeline/fetch_corpus.py` to fetch the lexicon's
   `lexemes.yaml`. Pin it to the same commit core uses, and put it in the
   git-ignored `pipeline/corpus/`. Update the docstring's sources and licences.
2. **Generator** (e.g. `pipeline/build_words.py`). It writes `data/words/<ch>.json`
   for all 28 chapters, not only built units, since it's cheap and search needs
   every reference. It also writes a `data/lemmas.json` with gloss, count and
   refs.
   - Use core's shapes unless there's a reason not to, and note any deviation.
   - Transliterate with `pipeline/greek.py`, so the interlinear matches the
     study's conventions in legends and `translation-choices.md`. Check a few
     against unit legends.
3. **Verify** (e.g. `pipeline/verify_words.py`). It must be independent of the
   generator and re-read MorphGNT itself. Check:
   - word counts per verse
   - every verse of every chapter present
   - every lemma has a gloss, or is on a named exception list
   - the schema

   Wire both into `build.py`. Add the new files to CLAUDE.md's "never
   hand-edited" list.
4. **Front end.**
   - Put the interlinear in its own module, `app/interlinear.js`, with a small
     interface (mount/unmount given a root and a unit).
   - Chapter:verse comes from the unit's passage plus verse-number rollover,
     like core's `indexVerses`. Units span chapters (unit 10 is 9:35–11:1), and
     fragments carry bare verse numbers. Don't edit fragments.
   - Add `["interlinear", "Interlinear (word by word)"]` to `MODES`.
   - Switching modes mounts or unmounts it, and so does loading a unit while
     the mode is on.
   - Fetch chapter files lazily and cache them.
   - Cells link to `#/search/<lemma>`.
5. **Search.**
   - Support `#/search/<query>`: it pre-fills and runs the query. The plain
     `#/search` link keeps working.
   - Add the Greek words block from `lemmas.json`, matching on transliterated
     lemma or gloss, accent-insensitive like the existing root search.
6. **Credit footer.** MorphGNT/SBLGNT and the lexicon need attribution (CC BY-SA
   3.0 plus the SBLGNT licence). Copy core's Greek `SOURCES` wording into a
   footer on Matthew's pages. Ask Lane whether it shows site-wide or only in
   interlinear mode.
7. **CSS.** Adapt core's `.il` rules into `css/styles.css` using Matthew's
   variables. Check:
   - dark mode (`data-theme` dark and auto)
   - `body.text-center`
   - print
   - 375px with no horizontal page scroll: cells wrap, and long glosses are
     capped

   Decide with Lane what happens to notes and ✦ asides in interlinear mode
   (Joshua keeps them).

## Pilot notes (deliverable)

Write `docs/interlinear-pilot.md`, short, for the future core port. Cover:

- what's book-agnostic and could move to core as-is
- what's Matthew-specific
- what had to change from core's code, and why; which changes core should
  take back
- data sizes and load behaviour
- anything that surprised you

Keep the generator and `app/interlinear.js` free of Matthew-only assumptions
where it's cheap: pass the book id, chapter count and paths as parameters.

## Working rules

- Ask Lane before going deep on anything this prompt leaves open. Use the
  AskUserQuestion popup.
- `python pipeline/build.py` must pass. A Windows build rewrites line endings
  (CRLF) on files it doesn't change; `git checkout` those back.
- Keep the asset `?v=` numbers in step: bump `index.html`'s css/main.js
  versions and main.js's import versions for every changed file.
- Lane does the visual check in the browser (the in-app browser caches badly).
- Log in `improvements_log.md`, `session_index.md` and a new
  `session_summary_[date].md`. Update PLAN.md's "Reader features" entry and
  `project-side/` if a synced file changes. Commit after Lane's OK.
