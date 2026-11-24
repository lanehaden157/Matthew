# File formats for a unit

## notes.md

First line: `Unit NN, <passage>, notes`. Append each row the moment it's
judged, rejected rows too.

| verse | target | kind | evidence | wording read | status | strength | verdict |
|---|---|---|---|---|---|---|---|

- verse: C:V in this unit. target: Book C:V.
- kind: echo, story, parallel, intertext, type-scene, wordplay, other.
- evidence: shared words in transliteration + lemma ids from the pack.
- wording read: words actually read in the target, or "not read".
- status: VERIFIED (read in this unit's work), SHEET (pack or leads only),
  SECONDHAND (a source's summary), RECALLED (memory).
- strength: strong, possible, weak.
- verdict: ship (root echo, aside.echo, footnote, story box, synoptic box),
  tentative, or drop + why.

Story worth telling: after the table, story / same / different / what it does.
End with **Source status** (read, secondhand, unavailable, by verse) and
`Rows: N`.

## handoff.md

Every heading, in order; "none" under an empty one. Say what the fragment
must carry, not how research got there. Lint:
`python -m biblecore handoff-check work/NN/handoff.md work/NN/notes.md`.

- `## Scope`: unit, passage `C:V-C:V`, title, scope calls, `Notes: N rows`.
- `## Verse by verse`: per verse with something to carry: settled renderings
  (cite the ruling; an open one points to its call), roots to tag
  (`data-root` slugs; translit + gloss for a local one), gloss and footnote
  points (each footnote with a bold lead).
- `## Approved boxes`: per box `### Title`, then **Kind**, **Anchor** (C:V),
  **Ref**, **Story**, **Same**, **Different**, **Does**, **Strength**
  (strong ships; tentative goes to Lane as a call). Echo may omit
  Story/Same/Different. Count line: "N rows considered, N ship, N dropped"
  (tentative counts as ship until Lane says no).
- `## Decisions`: renderings and glossary choices you settled without Lane,
  one line each: lexeme or phrase, rendering, reason.
- `## Threads`: opens and payoffs (one-line popover note each); promotions
  decided (`id`, lemma ids from pack, `gloss`, opener note, reason); close
  calls → Calls; retro entries.
- `## Calls for Lane (N)`: each with the verse, 2-3 options, recommended first,
  one-line reason each. The only place a provisional rendering, scope doubt,
  close-call promotion or tentative box appears. A settled ruling that merely
  looks odd isn't a call.
- `## Checks for code`: `ref, claim, expected lemma(s)`; lemma in translit or
  a pack id; leading `!` = must be absent. Only claims actually read.
- `## Source status`: from notes.
- `## Answers`: added in step 5, one line per call.

## factcheck.md

One row per claim checked: `claim | where | source opened | result (ok, fixed,
unsettled) | note`. End with `Checked: N, fixed: N, unsettled: N`.
