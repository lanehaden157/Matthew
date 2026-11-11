# Session summary: 2026-10-01, Matthew onto core (pass 1)

The full account is in the Bible folder: `../session_summary_2026-10-01_matthew-box-pass1.md`. For this repo:

- Commits `5666f47` (the move) and `c0a5e84` (core 0.15.1 vendor); not pushed. Push this repo first (the hub and core's CI read its main).
- Units 1-13 are boxed (`contract: legacy`): visible text identical to the old site, bodies equal the tag's apart from units 4 and 6 (an itinerary `</span>` each). Known pre-existing markup quirks left alone: stray `</span>` before the footnote sup at 3:6, 4:14, 6:2; unit 3's 4:10 compare row nests the next row.
- `biblecore test` 9/9, audit 0 gaps / 81 threads, 13 units browser-checked (text, interlinear, 375px, print).
- Don't run `python -m biblecore sync` until pass 2 re-pastes the field: the research project would get `core-workflow.md` while its field still describes the old pipeline.
- Open for pass 2: unit 14 (artifact at the tag), chat-side rebase on the template (M5), `resources.md` (skipped in sync), template base unset, `instructions.md` rename.
