---
name: unit
description: Build one Matthew unit end to end (research, briefing, verse by verse, fact-check, Lane's calls, fragment, port, ship). Use when told "do unit N", "/unit N", or started by the finish conductor. Resumes from wherever the unit stands.
---

# One unit, end to end

Work in `work/NN/` (NN zero-padded). `python tools/unit_status.py N` says
where the unit stands; resume at the first step whose file is missing. Lane's
only part is step 5. Everything else runs without asking.

## 0. Start

- `python -m biblecore unit-pack N --out work/NN/pack.md`. Ids, rulings,
  threads, lemma table, leads: copy from it, never recall.
- Read `study-lens.md`, the pack, the unit's map entry, the `Sections` line of
  each `sources/units/NN/*.md`.
- Scope: follow the unit map. A split or a scope doubt → a call (step 5),
  not a stop.

## 1. Research → `notes.md`

Split the unit into scenes. One `scene-researcher` agent per scene, in
parallel; give each its verses, `work/NN/pack.md` and the paths of the source
files. Merge their rows into `notes.md` (format: `formats.md`). Then work the
pack's leads and parallel-account checks no scene covered.

## 2. Briefing → `briefing.md`; 3. Verse by verse → `verse-by-verse.md`

Built on the notes; don't re-research. A gap → name it in the text as not
researched. Prose rules: `study-lens.md`. While writing verse by verse, catch
thread opens/payoffs, promotion candidates, local roots, retro entries and
claims about other passages' Greek or Hebrew; they go in the handoff.

## 4. Fact-check → `factcheck.md`

One `fact-checker` agent over `notes.md`, `briefing.md`, `verse-by-verse.md`.
Apply its fixes. What it can't settle becomes a call. Then write `handoff.md`
(format and lint: `formats.md`). Promotions: decide them yourself, biased book-wide;
only close calls go to Lane, retrofit cost in view.

## 5. Calls (Lane)

If Lane isn't in the session: `PushNotification` "Unit N: K calls ready" and
end the turn. When Lane is here: every item under `## Calls for Lane` via
AskUserQuestion, four per popup, recommended first and marked. Tentative
boxes = one yes/no each. Write the answers under `## Answers` in `handoff.md`.

## 6. Build (in unit order)

- Unit N-1 must be shipped (`unit_status`). If not, say so and stop; the
  conductor resumes this session when it is.
- `git fetch && git rebase origin/main`, then regenerate the pack: threads may
  have changed. Re-check the handoff against it.
- Draft `source-artifacts/matthew_NN_translation.html` from the handoff +
  answers. Rules: `fragment-contract.md`, then `matthew_study_style_reference.md`
  (wins), markup in `components-reference.md`. Handoff "Checks for code" →
  `checks[]`; ready promotions → `threads.promote[]`.
- `python -m biblecore port N --dry`, fix until clean. `python -m biblecore
  lxx --checks N`: a failed check → fix the claim, not the check.
- `python -m biblecore port N --promote`; check the thread delta's rows for
  this unit's verses against the map; apply ready payoffs; `audit`; `test`.
- Copy `briefing.md` and `verse-by-verse.md` to `readings/NN-briefing.md`,
  `readings/NN-verse-by-verse.md`.

## 7. Ship

Commit `work/NN/`, `readings/`, `source-artifacts/`, `units/`, `data/`,
`canon-leads/`, `threads-digest.md` and anything the build regenerated, with
a message naming the unit and its promotions. `git push origin HEAD:main`.
Add one line to `session_index.md`. Say "unit N pushed".
