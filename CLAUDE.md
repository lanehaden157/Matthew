# Matthew Study

How this repo behaves. The artifact contract lives in
`matthew_study_style_reference.md` and is authoritative over this file. A 28-unit
literary-canonical study of Matthew, live at https://lanehaden157.github.io/Matthew/ .
Research happens in a Claude.ai project, in two chats per unit (`core-workflow.md`); the
artifact lands here.

Built on **bible-core** (vendored in `biblecore/`, version in `biblecore/CORE_VERSION`); the
shared shape is in `bible-core/ARCHITECTURE.md`. Optional components come from core's
registry via `book.json` `components`. The book's own look is `css/theme.css`.

**State:** `python -m biblecore book` prints where the book stands, read from its data, so
it isn't written here.

## Boxed units 1-13

Units 1-13 shipped before Matthew moved onto core and are stamped `"contract": "legacy"`
(ARCHITECTURE §5). They're held to no versioned fragment check, `migrate` leaves them alone,
and their prose and structure stay as built. A new thread still gets tagged into them, through
`retrofit` and `data-w`, never by re-porting. Diff a boxed unit before committing: a change
beyond tags is a stop. Units from 14 on go through core's loop. The pre-core state is at tag
`pre-revert-2026-09-29`.

## Commands (run from this folder)

    python -m biblecore book             # where the book stands
    python -m biblecore port 15 [--dry]  # port source-artifacts/matthew_15_translation.html (--force re-ports)
    python -m biblecore port 15 --answers a.json  # {question topic: answer}: a dry run's answers carry over
    python -m biblecore build            # everything downstream of units/*.html
    python -m biblecore audit            # thread coverage (--ids ROOT previews an id set); gaps end with ready `add` JSON
    python -m biblecore lxx Isa 22:22 [--expect petra '!kleis']  # an LXX verse's lemmas; '!x' = must be absent
    python -m biblecore lxx --checks 17  # run a unit's checks[]
    python -m biblecore test [--quick]   # check the book: pin, units, contracts, build idempotence
    python -m biblecore sync             # mirror chat-side files, commit and push (after Lane's OK)
    python tools/constable_index.py      # constable-index.md (see the script's docstring)

`python -m biblecore` lists the rest, including `colour` and `data-w` for promoting a thread,
`retrofit`, `leads`, `sync-check --mark-pasted` after pasting the instruction field. **Fresh
clone:** `python -m biblecore fetch` once, then `corpus`.

`book.json` holds everything book-specific (closed keys). Change behaviour for this book with
a book-local module that wraps a core function, not by editing `biblecore/`;
`python ../bible-core/tools/core_diff.py` reports edits there. Update the vendored copy with
`python ../bible-core/tools/core_sync.py .`.

**Concurrent sessions.** Another session may be editing `../bible-core` or this repo. Check
`git status` first, work in a worktree if it's dirty, stage explicit paths, and check
`book.json`'s `core` version after vendoring (`../bible-core/CLAUDE.md`).

## Where things live

| For… | Read |
|---|---|
| The artifact contract | `matthew_study_style_reference.md` |
| The instruction field Lane pastes into the project | `CHAT_SIDE_INSTRUCTIONS.md` |
| What round-trips to the project, and how | `project-side/README.md` |
| Tracked threads | `data/threads.json` and `data/roots.json` → `threads-digest.md` (generated) |
| English renderings | `translation-choices.md` |
| Promoting a thread into built units | `docs/retrofit.md` |
| History | `archive/` and `docs/audit/`: not instructions |

## Threads

`data/threads.json` and `data/roots.json` are policy: the porter proposes, and Claude Code
applies what's decided. Claude decides promotion, biased toward book-wide, and asks Lane by
popup when unsure. Thread colours come from `python -m biblecore colour`; hand-pick one only if
Lane asks, because eyeballed colours collided before.

`port` also prints a unit's `checks[]` (run them against the corpus; they aren't for Lane) and
`threads.promote[]` (ready entries, written into the thread delta). Neither is stored after the
port. Check the delta's rows citing the unit's verses against the unit map.

## Asking Lane

Questions for Lane (open `questions[]`, wording calls, thread decisions) go through the
**AskUserQuestion popup**, best provisional choice first and marked "(Recommended)", batched
four per call, every time.

## Site and corpus

The build writes the app shell and generated css from bible-core, each marked "generated, don't
edit". A shell change goes into bible-core's `biblecore/web/`.

Corpus: SBLGNT via MorphGNT plus the LXX, pinned in `book.json` and `biblecore/fetch.py`.
`python -m biblecore corpus` gives 1,068 verses, 18,329 words, 1,680 lemmas; check against a
printed SBLGNT if these drift. `Matthew-words.tsv` and `Matthew-reading.txt` are generated.

## Working notes

- Ask Lane about design or scope before going deep. It's cheaper than guessing.
- Git Bash on Windows mangles inline Unicode in `bash -c`. Put regex and Unicode work in `.py`
  files.
- Session context files follow Lane's global convention.
