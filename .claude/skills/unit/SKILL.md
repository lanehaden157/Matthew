---
name: unit
description: Do one Matthew unit: study it here (research, notes, briefing, verse by verse), fact-check, Lane's calls, then hand the build to the builder agent. Use for "do unit N", "/unit N", or from the finish conductor. Resumes where the unit stands.
---

# Unit N

You study. `fact-checker` checks. `builder` builds. NN = zero-pad. Files in
`work/NN/`. Where it stands: `python tools/unit_status.py N`; resume at
first missing file.

## 1. Read

- `python -m biblecore unit-pack N --out work/NN/pack.md`. Read. Ids, rulings, threads, leads: copy, never recall.
- `lens.md`. Unit's map entry (`matthew-literary-unit-map.md`).
- `python tools/kit.py greek <range>`.
- `python tools/kit.py parts N`, Read all `work/NN/parts/` (Constable, France, D&A whole).
- Per scene: `kit.py range <scene> --source synoptic`; `kit.py range <scene> --source chrysostom,catena,ellicott --out work/NN/extra/<scene>.md`, Read.
- Targets: `kit.py bible <BOOK> <range> [--lxx]`, `python -m biblecore lxx <Book> <C:V>`.
- Web: voices sources lack (Wright, Bible Project, Jewish). Sites: `resources.md`.
- Output long → `| tail -40`. Scope doubt → call, not stop.

## 2. notes.md

Per scene: people, places, objects, earlier appearances; story shape + nearest earlier same-shape story (read target); same / different / does; later NT reuse; Matthew vs parallels; pack leads. One row per link, dropped too.

| verse | target | kind | evidence | wording read | status | strength | verdict |
|---|---|---|---|---|---|---|---|

- kind: echo, story, parallel, intertext, type-scene, wordplay, other.
- evidence: shared words translit + pack lemma ids.
- status: VERIFIED (read this unit), SHEET (pack), SECONDHAND, RECALLED.
- strength: strong, possible, weak.
- verdict: ship (root echo / aside.echo / footnote / story box / synoptic box), tentative, drop + why.

End: **Source status** (read / secondhand / unavailable).

## 3. briefing.md, verse-by-verse.md

Read aloud by app. Flowing prose. Scene headings ok. No bullets, bold, tables, verse numbers, refs. Names spoken ("the book of Genesis"). Quotes only VERIFIED.

- Briefing 600-900 words: placement, background, genre, words to watch, tensions, earlier stories leaned on (name, don't tell). Orient, don't resolve.
- Verse by verse: depth. Scripture roots + canon trajectories first; then wordplay, real structures, background, commentary dialogue. Verse reaches earlier story → tell it there: background, match, differ, what Matthew does. Telling parallel difference → say in place. Tensions open. Devotion light.

## 4. Fact-check

`fact-checker` agent, unit N. Unsettled → calls. Its token use → `work/NN/cost.md`.

## 5. calls.md

Decide all you can: pack-ruled renderings, strong boxes, promotions (book-wide bias, retrofit cost).

- `## Calls for Lane (N)`: numbered. Verse, 2-3 options, recommended first, one-line reason each. Only: provisional renderings, scope doubts, close-call promotions, unsettled fact-checks, tentative boxes (yes/no). Odd-looking ruling ≠ call.
- `## Decided without Lane`: one line each, why. Lane audits.
- `## Answers`: empty till 6.

## 6. Ask

Lane absent: `PushNotification` "Unit N: K calls ready". End turn. Lane here (or Remote Control): AskUserQuestion, four per popup, recommended first, marked. Answers → `## Answers`.

## 7. Build

Unit N-1 not shipped (`unit_status`) → say so, end turn; conductor resumes. Else `builder` agent, unit N. Relay its result.
