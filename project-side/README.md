# Project-side sync — index, not a copy of the canonical files

Every file in the table below has **one canonical copy**, at the repo path
linked. This file exists so you don't have to hunt for the canonical paths.

**`project-side/synced/` is the one deliberate exception.** It holds a flat,
auto-generated *copy* of every tracked file's current content (basenames only,
e.g. `data/threads.json` → `synced/threads.json`), pushed to
`github.com/lanehaden157/Matthew`. Point the Claude.ai research project's
GitHub connector at that folder and its "sync" feature pulls fresh content on
its own — no re-pasting, ever. Never hand-edit anything under `synced/`; it is
overwritten on the next sync.

**What keeps it current:** `pipeline/sync_to_github.py` copies every
`TRACKED_FILES` entry into `synced/`, and if anything actually changed, commits
and pushes. `pipeline/build.py` runs it as its last step, so the mirror
refreshes exactly when the data it mirrors does. Run it by hand any time with:

```bash
python pipeline/sync_to_github.py
```

**Deliberately no scheduled task.** Joshua runs its sync every 15 minutes from
Windows Task Scheduler; `platform-design-review.md` A10/H9 flags the resulting
commit noise as a problem worth not inheriting. `build.py` already runs after
every change that matters.

**Fallback for a project that can't use a GitHub connector** (one that only
takes uploaded files): `pipeline/check_project_sync.py` does the older
hash-diff-and-tell-you-what-changed job —

```bash
python pipeline/check_project_sync.py               # what needs re-pasting
python pipeline/check_project_sync.py --mark-synced  # after you've pasted everything
```

— tracked separately in `project-side/sync-state.json`.

## Files

| file | direction | what it is | update cadence |
|---|---|---|---|
| [`matthew_study_style_reference.md`](../matthew_study_style_reference.md) | repo → project | The artifact contract — fragment shape, unit-meta schema, component whitelist, transliteration scheme, the 28-unit map, checklist | Whenever it changes |
| [`translation-choices.md`](../translation-choices.md) | repo → project | Hand-maintained glossary of deliberate English renderings | Edit **in the same turn** as any wording decision — `CLAUDE.md` makes this a standing workflow step, not a separate ask |
| [`threads-digest.md`](../threads-digest.md) | repo → project | Generated snapshot of tracked cross-unit threads — the source of truth for what to tag | Regenerate (`python pipeline/threads_digest.py`, or just run `build.py`) any time `data/threads.json` changes; never hand-edit |
| [`MatthewSBLGNT.txt`](../MatthewSBLGNT.txt) | repo → project | SBLGNT Greek of Matthew, `Matt C:V\t<text>` lines. The project's copy has to be **byte-identical** to this one, which until now was kept true by discipline alone | Static unless the corpus pin changes — but syncing it is the point: the mirror makes identity mechanical |

**Not synced, on purpose:** `instructions.md` (the chat-side contract — still
authoritative at its repo path, but the project holds its own copy in its
instructions field) and `synoptic_parallels_units_01_10.md` (research input,
not a contract). Both match the call made on the Joshua side, 2026-09-16.
Adding either is one line in `pipeline/check_project_sync.py`.

## Also worth knowing about, not part of the sync loop

- [`CLAUDE.md`](../CLAUDE.md) — how *this repo* behaves (pipeline, layout,
  locked decisions). Repo-side only; the project doesn't need it.
- [`PLAN.md`](../PLAN.md) — phase list and open questions. Repo-side only.
- [`platform-design-review.md`](../platform-design-review.md) — the
  cross-project audit this folder came out of (item B4). Reference.
