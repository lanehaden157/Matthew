# Session summary — 2026-09-22 (intertext pass)

## What was asked
Integrate Joshua's intertext pass and echo structures into Matthew, forward from
unit 13. Research the design (Joshua's `Claude_ai_chat_side_instructions.md`,
`joshua_study_style_reference.md`, `pipeline/canon_leads.py`, `bible-core`'s
`check_echo()`) and ask clarifying questions before building.

## Decisions (Lane, via AskUserQuestion)
- Echo scope: both pieces, as in Joshua — a root-level `echo` (word-level,
  popover) and `aside.echo` (verse-level). Existing OT citation pointers stay
  for actual quotations; echoes cover allusions/type-scenes/later reuse.
- Leads corpus: LXX + rest of NT (not LXX-only) — Greek-to-Greek lemma matching.
- Backfill: forward from unit 13 only. Units 1-12 are a tracked backlog.
- Echo chip: shares `.gloss`'s note (`*`) toggle, not its own chip (unlike
  Joshua, which gives `aside.echo` no separate chip either, actually — this
  matches Joshua's own choice, just confirmed rather than assumed).

## What was built
- **Corpora**: `pipeline/fetch_corpus.py` downloads MorphGNT's lemmatized
  SBLGNT (27 NT books) and 4 of CenterBLC's Text-Fabric Rahlfs-1935 LXX files,
  both pinned to a commit, into git-ignored `pipeline/corpus/`. Licences
  checked before downloading: MorphGNT's lemmatization is CC-BY-SA 3.0 (text
  itself under the SBLGNT EULA, same as the repo's existing
  `MatthewSBLGNT.txt`); CenterBLC's Text-Fabric build is MIT.
- **`pipeline/greek_corpus.py`**: hand-rolled Text-Fabric plain-text parser (no
  `text-fabric` dependency) + MorphGNT column parser. Both keyed by
  transliterated lemma (`pipeline/greek.py`) since the corpora share no
  numeric id.
- **`pipeline/canon_leads.py`**: ported from Joshua. Generates
  `canon-leads/canon-leads-unit-NN.md` — rare Greek words and shared two-word
  phrases vs. the LXX and rest of NT, Synoptic hits (Mark/Luke) excluded since
  that has its own comparison path. Found and fixed a frequency-counting bug
  during testing (deduped per book instead of per verse) that had flooded the
  first draft with ~1300 lines of noise; fixed output is 110 lines, matching
  Joshua's quality bar on a real test (unit 13).
- **`echo` field + `aside.echo` component**: wired through
  `pipeline/unit_meta.py` (schema, validation), `pipeline/port_artifact.py`
  (units.json merge, structural checks ported from `bible-core`'s
  `check_echo()`), `app/threads.js` (popover render), `app/spotlight.js`
  (bucketed with `.gloss`), `css/styles.css` (`--accent-slate` border,
  CSS-prepended "cf.").
- **`build.py`**: new advisory step (`canon_leads.py`, never fails the build).
  **`check_project_sync.py`**: globs `canon-leads/*.md` into `TRACKED_FILES`.
- **Docs**: `instructions.md` (3 passes → 4, new pass 3 ledger),
  `matthew_study_style_reference.md` (§1a, component snippet, checklist),
  `CLAUDE.md` (status, layout, paste-block), `project-side/README.md`.

## Verification
`python pipeline/build.py` green throughout (existing 12 units unaffected).
Generated `canon-leads/canon-leads-unit-13.md` as a live test — real, useful
hits (e.g. Matt 13:15's "closed eyes" phrase → Isa 6:10). Smoke-tested the new
`aside.echo` structural checks against synthetic fragments (good, bad anchor,
bad nesting, missing anchor, tagged span) — all fire correctly. JS syntax
checked (`node --check`). No unit ported yet, so nothing to eyeball in the
browser this session.

## Open questions
None outstanding. Not yet committed/pushed — Lane reviews first.
