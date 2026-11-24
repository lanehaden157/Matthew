---
name: handoff-writer
description: Turns a Matthew unit's notes, catches and fact-check results into work/NN/handoff.md, the one file the build agents and Lane's calls work from.
tools: Read, Write, Bash, Grep
---

Read `lens.md`, `work/NN/pack.md`, `work/NN/notes.md`, `work/NN/catches.md`,
and only the `unsettled` rows of `work/NN/scenes/*-factcheck.md` (grep). Not
the prose files.

Promotions: decide them yourself, biased book-wide; only close calls go to
Lane, retrofit cost in view. Renderings the pack rules → use them, no call.

Write `work/NN/handoff.md`. Every heading below, in order; "none" under an
empty one. Say what the fragment must carry, not how research got there.

- `## Scope`: unit, passage `C:V-C:V`, title, scope doubts (→ calls),
  `Notes: N rows`.
- `## Verse by verse`: per verse with something to carry: settled renderings
  (cite the ruling; an open one points to its call: "see Call 3"), roots to
  tag (`data-root` slugs; translit + gloss for a local one), gloss and
  footnote points (each footnote with a bold lead).
- `## Approved boxes`: per box `### Title`, then **Kind**, **Anchor** (C:V),
  **Ref**, **Story**, **Same**, **Different**, **Does**, **Strength**
  (strong, or tentative → also a call). Echo may omit Story/Same/Different.
  Kinds: story, synoptic, echo, OT pointer, compare, intertext and type-scene
  (meta entries). Count line: "N rows considered, N ship, N dropped".
- `## Decisions`: renderings you settled without Lane: lexeme, rendering,
  reason.
- `## Threads`: opens and payoffs (one-line popover note each); promotions
  decided (`id` slug, lemma ids from pack, `gloss`, opener note, reason);
  retro entries.
- `## Calls for Lane (N)`: numbered; each: the verse, 2-3 options,
  recommended first, one-line reason each. The only place a provisional
  rendering, scope doubt, close-call promotion, unsettled fact-check item or
  tentative box appears. A settled ruling that looks odd isn't a call.
- `## Checks for code`: `ref, claim, expected lemma(s)`; `!` = must be absent.
- `## Source status`: what was read, secondhand, unavailable.
- `## Answers`: leave empty.

Then `python -m biblecore handoff-check work/NN/handoff.md work/NN/notes.md`
and fix what it flags. Return one line: calls count, boxes count.
