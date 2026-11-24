---
name: unit
description: Build one Matthew unit end to end in this session (research, briefing, verse by verse, fact-check, Lane's calls, fragment, port, ship). Use when told "do unit N", "/unit N", or started by the finish conductor. Resumes from wherever the unit stands.
---

# One unit, end to end

This session does the whole unit, so nothing is lost between hands. The one
other agent is the `fact-checker`, kept separate for fresh eyes. The heaviest
unit's sources are about 240k tokens; the context holds that with room to
spare. Strong suggestions: read Constable, France and D&A whole (they're the
dialogue); take Chrysostom, the Catena and Ellicott by scene; keep command
output short (`| tail -40`).

`python tools/unit_status.py N` says where the unit stands; resume at the
first step whose file is missing (after a restart, re-read what that step
needs). NN = zero-padded N. Files go in `work/NN/`.

## 1. Read

- `python -m biblecore unit-pack N --out work/NN/pack.md`; read it. Ids,
  rulings, threads, lemma table, leads: copy from it, never recall.
- `lens.md`; the unit's map entry (`matthew-literary-unit-map.md`).
- `python tools/kit.py greek <range>`, `python tools/kit.py parts N`, then
  Read every file in `work/NN/parts/`.
- Per scene: `python tools/kit.py range <scene> --source synoptic`, and
  `--source chrysostom,catena,ellicott --out work/NN/extra/<scene>.md`, Read.
- Targets: `python tools/kit.py bible <BOOK> <range> [--lxx]`,
  `python -m biblecore lxx <Book> <C:V>`. Web for voices the sources lack
  (Wright, Bible Project, Jewish sources); `resources.md` lists tested sites.
- Scope doubt → a call later, not a stop.

## 2. Notes → `notes.md`

Per scene: people, places, objects and where they appeared before; the
story's shape and the nearest earlier story with that shape, read in the
target; same, different, what it does here; later NT reuse; what Matthew
changes from the parallels; the pack's leads. One row per link, rejected ones
too:

| verse | target | kind | evidence | wording read | status | strength | verdict |
|---|---|---|---|---|---|---|---|

kind: echo, story, parallel, intertext, type-scene, wordplay, other.
evidence: shared words, transliterated, + pack lemma ids. status: VERIFIED
(read in this unit's work), SHEET (pack only), SECONDHAND, RECALLED.
strength: strong, possible, weak. verdict: ship (root echo, aside.echo,
footnote, story box, synoptic box), tentative, or drop + why. End with
**Source status** (read, secondhand, unavailable).

## 3. Prose → `briefing.md`, `verse-by-verse.md`

Read aloud by the web app: flowing prose, a short heading per scene is fine;
no bullets, bold, tables, verse numbers or references in the text; names as a
person says them ("the book of Genesis"). Quotation marks only for VERIFIED
wording.

- Briefing, 600-900 words: placement, background, genre, vocabulary to
  watch, tensions to hold, earlier stories the unit leans on (named, not
  told). Orient, don't resolve.
- Verse by verse: depth over speed. Earlier-Scripture roots and canonical
  trajectories first; then wordplay, real structures, background, commentary
  dialogue. Where a verse reaches an earlier story, tell it there:
  background, what matches, what differs, what Matthew does with it. A telling
  difference from a parallel is said in place. Leave tensions open;
  devotional weight lightly.

## 4. Fact-check

One `fact-checker` on `work/NN/`. Read its `factcheck.md` totals; its
unsettled items become calls. Note its token use in `work/NN/cost.md`.

## 5. Calls → `calls.md`

Decide everything you can: renderings the pack rules, strong boxes,
promotions (biased book-wide, retrofit cost in view). Write `calls.md`:

- `## Calls for Lane (N)`: numbered; each: the verse, 2-3 options,
  recommended first, one-line reason each. Only provisional renderings, scope
  doubts, close-call promotions, unsettled fact-check items, tentative boxes
  (yes/no). A settled ruling that looks odd isn't a call.
- `## Decided without Lane`: one line each (rendering, box, promotion, why),
  so Lane can audit.
- `## Answers`: empty until step 6.

## 6. Ask

Lane absent: `PushNotification` "Unit N: K calls ready", end the turn. Lane
here (or via Remote Control): AskUserQuestion, four per popup, recommended
first and marked. Answers → `## Answers`, one line per call.

## 7. Build (in unit order)

- Unit N-1 shipped (`unit_status`)? If not, say so and end the turn; the
  conductor resumes you.
- `git fetch -q && git rebase origin/main`; regenerate the pack and diff it
  against what you used (threads may have changed).
- Read `fragment-contract.md`, `matthew_study_style_reference.md` (wins),
  `components-reference.md`; grep `translation-choices.md` per lexeme. Write
  `source-artifacts/matthew_NN_translation.html` from your notes, prose and
  answers: claims about other passages' Greek or Hebrew → `checks[]`;
  promotions → `threads.promote[]`.
- `python -m biblecore port N --dry | tail -60` until clean;
  `python -m biblecore lxx --checks N | tail -20` (fix the claim, not the
  check); `port N --promote | tail -60`; `apply-delta N`; `audit | tail -20`;
  `test | tail -15`.
- Copy `briefing.md`, `verse-by-verse.md` to `readings/NN-briefing.md`,
  `readings/NN-verse-by-verse.md`.

## 8. Ship

Stage explicit paths: `work/NN/` (not `parts/`, `extra/`), `readings/`,
`source-artifacts/`, `units/`, `data/`, `canon-leads/`, `threads-digest.md`,
and what else `git status` shows the build regenerated. Commit naming the unit
and its promotions; `git push origin HEAD:main`. One line in
`session_index.md`. Say "unit N pushed".
