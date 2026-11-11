# Session summary: 2026-09-30, interlinear mode

Built from `docs/interlinear-prompt.md`: a Greek word-by-word reading mode, copied
from bible-core's Greek path and adapted. Matthew stays standalone. Pilot for a
future core version (Luke, Revelation).

## Lane's calls (popups)
- Credit footer site-wide.
- Notes and ✦ asides stay in interlinear mode (as Joshua).
- 6:10–13 (no numbered verses inside the prayer block): labelled boxes after the prayer.
- Parsing line hidden on phones, as core.
- Search: when the query is exactly a lemma id, that word's block goes first, above the tracked roots.

## Done
- Pipeline: `morphgnt.py`, `greek_morph.py`, `greek_lexicon.py` (from core @25efd85), `build_words.py` (from `emit.py`), new `verify_words.py`; both in `build.py`. `fetch_corpus.py` fetches `lexemes.yaml` at core's pin (sha1 matches core's copy).
- Data: `data/words/1..28.json`, `data/lemmas.json`. 18,329 words, 1,680 lemmas, all glossed. Byte-identical to core's pre-revert output.
- App: `app/interlinear.js`; `main.js` (fourth mode, mount on load and on switch, `C:V` anchors, `#/search/<query>`, `SOURCES` footer); `search.js` (Greek words block); `css/styles.css`; `index.html` (footer, v=40).
- Docs: `docs/interlinear-pilot.md`, CLAUDE.md, PLAN.md.

## Checked
- `build.py` ok. `verify_words.py` catches a dropped word, a raw parsing code and a wrong lemma id (injected, then restored).
- In the preview, by DOM and computed style: every verse of all 13 units gets a box; unit 10 rolls 9:35 → 11:1; switching modes mounts and unmounts; 375px has no horizontal overflow from the interlinear, search or footer; dark and light tokens resolve; centered layout; print rules present.
- Not checked: how it looks (Lane's browser check), paper print, and the scroll-to-verse jump (the hidden preview pane pauses animation frames; the lookup itself was tested).

## Takeaways
- Matthew's `greek.py` and core's `lang/greek.py` agree on every word of Matthew.
- The build now needs `pipeline/corpus/`; a fresh clone runs `fetch_corpus.py` first.

## Open
- Lane: visual check, desktop and phone, light and dark, then OK to commit.
- Gloss colour is about 3.9:1 on the box background in the light theme (same as core/Joshua).
- Unit 8's thread table overflows 375px by 4px in every mode; predates this session.
- Still backlog: print page, verse jump, resume.
