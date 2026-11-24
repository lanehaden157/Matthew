---
name: unit
description: Build one Matthew unit end to end (research, briefing, verse by verse, fact-check, Lane's calls, fragment, port, ship). Use when told "do unit N", "/unit N", or started by the finish conductor. Resumes from wherever the unit stands.
---

# One unit, end to end

You only coordinate. Agents do the reading and writing; each one gets a small,
named set of files, so none runs out of room. Things to avoid here: reading
sources, parts, digests, notes, prose or the fragment yourself; pasting file
contents into an agent prompt (give paths). Each agent returns one line; keep
command output short (`| tail -40`).

`python tools/unit_status.py N` says where the unit stands; resume at the
first step whose output is missing. NN = zero-padded N.

## 1. Prepare

- `python -m biblecore unit-pack N --out work/NN/pack.md`
- `python tools/kit.py scenes N` → write `work/NN/scenes.md`, one line per
  scene: `k | C:V-C:V | title`. Aim for scenes of 5-20 verses; merge tiny
  ones. A scope doubt → note it for the handoff, don't stop.
- `python tools/kit.py parts N`

## 2. Digest (parallel)

One `source-reader` per file in `work/NN/parts/`, given that path and N.

## 3. Research (parallel)

One `scene-researcher` per scene: N, k, range. Then
`python tools/kit.py merge N notes` and `merge N catches`.

## 4. Write (parallel)

One `writer` with job "briefing", and one `writer` per scene with job
"verse k". Then `merge N verse`.

## 5. Fact-check (parallel)

One `fact-checker` per scene (its notes + verse files) and one for the
briefing. Then `merge N factcheck`. Fact-check cost: note the agent's token
use in `work/NN/cost.md` so Lane can judge whether to keep this step.

## 6. Handoff

One `handoff-writer`. Then `python tools/kit.py calls N`.

## 7. Calls (Lane)

Lane absent: `PushNotification` "Unit N: K calls ready" and end the turn.
Lane here (or via Remote Control): each call through AskUserQuestion, four per
popup, recommended first and marked; tentative boxes as yes/no. Append the
answers under `## Answers` in `work/NN/handoff.md`, one line per call.

## 8. Build (in unit order)

- Unit N-1 must be shipped (`unit_status`). If not, say so and end the turn;
  the conductor resumes you.
- `git fetch -q && git rebase origin/main`; regenerate the pack (threads may
  have changed since research).
- One `head-builder`, and one `scene-builder` per scene (parallel). Then
  `python tools/kit.py assemble N`.
- `python -m biblecore port N --dry | tail -60`. Errors → a `scene-builder`
  fix job for the scene that holds the verse (head errors → `head-builder`);
  repeat. `python -m biblecore lxx --checks N | tail -20`: a failed check →
  fix the claim, not the check.
- `python -m biblecore port N --promote | tail -60`; apply the delta's ready
  payoffs (`apply-delta N`); `audit | tail -20`; `test | tail -15`.
- Copy `work/NN/briefing.md` and `work/NN/verse-by-verse.md` to
  `readings/NN-briefing.md` and `readings/NN-verse-by-verse.md`.

## 9. Ship

Stage explicit paths: `work/NN/` (not `parts/`), `readings/`,
`source-artifacts/`, `units/`, `data/`, `canon-leads/`, `threads-digest.md`,
and whatever else `git status` shows the build regenerated. Commit naming the
unit and its promotions; `git push origin HEAD:main`. One line in
`session_index.md`. Say "unit N pushed".
