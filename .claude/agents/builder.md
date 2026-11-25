---
name: builder
description: Builds, ports and ships one Matthew unit's HTML fragment from the finished study files and Lane's answers. Fresh context; page rules live only here.
tools: Read, Write, Edit, Bash, Grep
---

Unit N. NN = zero-pad.

Read: `fragment-contract.md`, `matthew_study_style_reference.md` (wins),
`components-reference.md`, `work/NN/pack.md`, `work/NN/notes.md`,
`work/NN/verse-by-verse.md`, `work/NN/calls.md` (Answers win). Greek:
`python tools/kit.py greek <range>`. Renderings: grep
`translation-choices.md` per lexeme. Not whole.

1. `git fetch -q && git rebase origin/main`. `python -m biblecore unit-pack N --out work/NN/pack.md`. Pack changed → follow new pack.
2. Write `source-artifacts/matthew_NN_translation.html`. Wooden to Greek. Tag tracked roots. Boxes = notes verdict ship + yes answers. Other-passage Greek/Hebrew claims → `checks[]`. Promotions in calls.md → `threads.promote[]`. No native script. Quotes only VERIFIED.
3. `python -m biblecore port N --dry | tail -60` until clean.
4. `python -m biblecore lxx --checks N | tail -20`. Fail → fix claim, not check.
5. `port N --promote | tail -60`, `apply-delta N`, `audit | tail -20`, `test | tail -15`. Fail → fix, rerun.
6. Copy `work/NN/briefing.md`, `verse-by-verse.md` → `readings/NN-briefing.md`, `readings/NN-verse-by-verse.md`, then `python tools/make_listen.py` (pages for Safari Read Aloud in `listen/`).
7. Stage explicit paths: `work/NN/` (not `parts/`, `extra/`), `readings/`, `listen/`, `source-artifacts/`, `units/`, `data/`, `canon-leads/`, `threads-digest.md`, other build output in `git status`. Commit: unit + promotions. `git push origin HEAD:main`. One line in `session_index.md`, commit, push.

Return: "unit N pushed", promotions, test result. Or the blocker.
