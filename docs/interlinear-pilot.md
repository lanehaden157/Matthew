# Interlinear pilot: notes for the core port

Matthew's interlinear (2026-09-30) was built by copying bible-core's Greek path
(@25efd85) and adapting it. This is what a future core version for Luke and
Revelation should know. Matthew stays standalone; nothing here imports
`biblecore`.

## Where each piece came from

| Matthew | Copied from core | Changed? |
|---|---|---|
| `pipeline/greek_morph.py` | `lang/greek_morph.py` | No. Docstring only. |
| `pipeline/greek_lexicon.py` | `lang/greek_lexicon.py` | No. Docstring only. |
| `pipeline/morphgnt.py` | `corpus/morphgnt.py` + `lang/greek.py` `lemma_key` | `FILES`, the line regex, `lemma_ids`, `lemma_forms` as core. `load_words(osis, corpus_dir)` replaces `parse`/`build`/`load_words`: it reads the source lines straight into dicts, with no `<Book>-words.tsv` step. |
| `pipeline/build_words.py` | `emit.py` | `words_by_chapter`, `lemmas`, `_write_json` kept. Hebrew branches, `main_lemma`, `text.json` dropped. |
| `pipeline/verify_words.py` | new | Core has no independent check of `words/` and `lemmas.json`. |
| `app/interlinear.js` | `web/app/reader.js` | `passageRange`, `unitForRef`, `indexVerses` as core. `findVerse`, `mountInterlinear`, `unmountInterlinear` changed (below). |
| `.il*`, `.sr-lemma`, `.site-foot` in `css/styles.css` | `web/core.css` | Same rules. Matthew's `--accent-gold` alias in place of `--accent-bronze`. |
| `SOURCES` in `app/main.js` | `web/app/main.js` | Greek wording unchanged. |
| Greek words block in `app/search.js` | `web/app/search.js` `lemmaResults` | Changed (below). |

## Data: identical to core's

`data/words/<ch>.json` and `data/lemmas.json` are **byte-identical** to what
core emitted for Matthew before the revert (`git show
pre-revert-2026-09-29:data/words/5.json`): all 28 chapter files and
`lemmas.json`, 18,329 words, 1,680 lemmas. So:

- Matthew's `pipeline/greek.py` and core's `lang/greek.py` transliterate every
  word and lemma of Matthew the same way. They are still separate
  implementations, so re-run the diff for a new book.
- The shapes are core's, with no deviation. The `w` word id is kept, though
  Matthew has no `data-w` layer and nothing reads it.
- Lemma ids are the transliterated lemma. Two in Matthew carry a digit because
  two NT lemmas share a transliteration: `ou2` (hou, "where") and `tis2`
  (indefinite tis).
- Every lemma matched a lexicon gloss. `verify_words.py` has an empty
  `GLOSS_EXCEPTIONS` list for the day one doesn't.

## What had to change, and whether core should take it back

1. **Book comes from parameters, not `book()`.** `build_words.py` takes
   `--osis`, `--units`, `--data`; `morphgnt.py` takes the osis id and corpus
   folder. The chapter count is read from the last unit's passage in
   `units.json` and must match the corpus. *Core: no change needed; it has
   `book.json`.*
2. **Link target.** Cells link to `#/search/<lemma id>` through a `lemmaHref`
   option (core hardcodes `#/lemma/`). *Core should take the option* so a book
   can choose.
3. **Hebrew bits dropped**: the Aramaic `a` flag and `.il-arc`, Strong's
   `senses()` splitting on `;`, Ketiv rows. *Core keeps them.* Note that
   `senses()` would also run on a Greek gloss; MorphGNT glosses use commas, so
   it's harmless today.
4. **Verses with no block of their own.** Matthew's 6:9–13 is one `.prayer`
   block after verse 9, so 6:10–13 have no `.v` to hang boxes on. Core's
   `mountInterlinear` silently skips them. Matthew's version finds the gap
   between two consecutive verse blocks (`between()`), and puts a labelled box
   (`.il.il-gap`, with an `.il-ref` "6:10") per skipped verse just before the
   next verse, above any heading. `findVerse` resolves `6:11` to that box, or
   to the closest verse before it when the interlinear is off. *Core should
   take this back*: any book with a condensed or block-formatted passage has
   the same hole. (Core's `data-verses` condensed verses may want a different
   rule: check there first.)
5. **Mount/unmount race.** Core's mount awaits the fetch and then inserts. If
   the reader switches mode or unit meanwhile, boxes land after an unmount or
   twice. Matthew keeps a generation counter on the root (`root._ilGen`);
   unmount bumps it and a stale mount returns. *Core should take this back.*
6. **Key line placement.** Core prepends `.il-key` to `.verses` or
   `article.unit`. Only Matthew's units 1–4 have a `.verses` wrapper, so in
   the rest it would sit above the masthead. Matthew puts it before the notes
   bar (`.spot-controls`) or the first verse. *Core: only if its fragments
   vary the same way.*
7. **Key line and tooltip wording.** "Strong's gloss" became "a lexicon
   gloss"; "in the book" became the book's name (a `book` option). *Core
   should take the wording fix for Greek books*: its key line says "Strong's"
   for MorphGNT glosses.
8. **Search.** `#/search/<query>` pre-fills and runs; typing keeps the hash in
   step with `history.replaceState`. When the query is exactly a lemma id (what
   the interlinear links with), that lemma's block goes first and open, above
   the tracked roots; the rest follow as "Other Greek words" (Lane,
   2026-09-30). Without this, tapping *ho* put 22 substring-matched root blocks
   above the word. A one-letter id (*ē*, *ō*) shows only its own block. Core's
   `=<key>` exact form was not carried over; the plain id does the job.
   *Core: worth taking the lemma-first ordering if it moves cell links to
   search.*
9. **Independent verify.** `verify_words.py` re-reads the MorphGNT file with a
   plain split and never transliterates. It checks verse sets, per-verse word
   counts, word ids, the row schema, Latin-only transliterations (a final ’
   is allowed for elision: *kat’*, *di’*), that every parsing decoded, that
   lemma ids map one-to-one to Greek lemmas, and `lemmas.json` counts, refs
   and glosses. *Core should take this back*, per book language.
10. **Lexicon fetch.** `fetch_corpus.py` pulls `lexemes.yaml` at core's pinned
    commit (`0dca2af`, sha1 `9db21bd7…`, verified equal to core's vendored
    copy). Matthew fetches; core vendors. Either works.

## Book-agnostic as written

`greek_morph.py`, `greek_lexicon.py`, `morphgnt.py`, `build_words.py` (given
`--osis`), `app/interlinear.js` (options: `data`, `lemmaHref`, `book`), and
the CSS. `verify_words.py` takes `--source` and `--data`.

## Matthew-specific

- `pipeline/greek.py` as the transliterator.
- `units.json` as the unit map (`passage` strings with en dashes).
- `main.js` wiring: `MODES`, `IL_OPTS = { book: "Matthew" }`, the `currentUnit`
  guard, `SOURCES`.
- "Greek words in Matthew" headings and the search hint in `search.js`.
- Lane's calls: notes and ✦ asides stay in interlinear mode (as Joshua); no
  thread colour or root popover in the boxes; the credit footer is site-wide;
  parsing hides at ≤720px (as core) and comes back in print.

## Sizes and load behaviour

- `data/words/`: 28 files, 1.35 MB raw, about 182 KB gzipped. A chapter
  averages 48 KB raw (6.5 KB gzipped); the largest, chapter 26, is 92 KB.
- `data/lemmas.json`: 223 KB raw, about 60 KB gzipped.
- The interlinear fetches `lemmas.json` plus only the chapters the open unit
  covers (one to three), on first use, and caches them for the page's life.
  Search fetches `lemmas.json` once. Neither is fetched in the other modes
  unless search is opened.
- These fetches don't use `main.js`'s cache-busting `?v=Date.now()`: the files
  only change when the corpus pin changes.
- `build_words.py` plus `verify_words.py` add about 3 s to the build.

## Surprises

- The data came out byte-identical to core's on the first run. The two
  transliterators agree across all of Matthew.
- Legend transliterations match lemma ids except where the legend joins
  several lemmas ("akouō · akoē") or cites a middle form: the legend's
  *haptomai* is MorphGNT's `haptō`. A search for "haptomai" finds the tracked
  root but not the Greek word.
- Gloss colour contrast is low: `--accent-bronze` on `--panel` is about 3.9:1
  in the light theme at 12.5px, under the 4.5:1 usually wanted for small text.
  Same in core and Joshua. Worth a look in `themes.json`.
- Unit 8's thread table (`table.exod`) overflows 375px by 4px in every mode.
  It predates this work and isn't wrapped in `.table-scroll`.
- The build now needs `pipeline/corpus/` (it was advisory-only before), so a
  fresh clone must run `fetch_corpus.py` before `build.py`.

## Not done here

- `data/text.json` and core's "In the translation" search block, print page,
  verse jump and resume: still PLAN.md backlog.
- Print was checked at the rule level (boxes avoid page breaks, parsing
  shown), not on paper.
