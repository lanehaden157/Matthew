# Build prompt: earlier-story boxes, reordered passes, more synoptics

Paste into a fresh Claude Code session opened in the Matthew repo. Decided with
Lane on 2026-10-25; supersedes `intertext-redesign-handoff.md` (the chat side's
first draft, written against the old pipeline). Read this whole prompt before
touching anything. Ask Lane by AskUserQuestion popup when something here
doesn't fit what you find in the code.

## Why

Lane's favourite intertext work was the Unit 14 scene walk: earlier stories
told with their background (Herod's feast beside Pharaoh's birthday feast,
Elisha's loaves, Exodus 14 at the sea), not word matches. The current loop
can't produce that: pass 3 starts from a rare-word sheet, its output is a
ledger of one-line links, and it runs after the verse-by-verse, so what it
finds never reaches Lane, who learns by listening to passes 1 and 2. Synoptic
comparisons are also capped at 0–3 per unit, and every unit hits the cap.

## What belongs where (settle this first; the rest follows)

Each link lives in exactly one place. Pick by what the link *is*:

| The link is… | It goes in | Shown |
|---|---|---|
| A word's history across books (a tracked root) | root `echo` popover | on the root word |
| One verse or phrase elsewhere that sounds through this verse; one sentence says it | `aside.echo` (unchanged) | verse note, behind `*` |
| A *different* earlier event with the same shape, worth telling: background, same, different, what Matthew does with it | **new `aside.story`** | its own ◈ chip |
| The *same* event told by Mark, Luke or John, where Matthew's change is telling | `aside.synoptic` | its own ✧ chip |
| A formula quotation | OT citation pointer (unchanged) | inline |
| A contested reading or a debate that needs room | footnote | endnotes |

How to choose:
- Same event in another gospel → synoptic, never a story box.
- Earlier event → story box if it needs telling (a reader would need the
  background to see the point), echo if one sentence carries it.
- When a story box covers a link, its word-level evidence goes inside the box.
  Don't also ship an echo for the same link.
- Interpretive argument about a link → footnote, and the story box states only
  what the parallel is.

## 1. The new component: `aside.story` (bible-core)

Build it in `../bible-core/biblecore/components/story/` on the pattern of
`echo` and `synoptic` (component.json, snippet.md, style.css, `__init__.py`
validator). "story" is a working name; rename it if core's naming suggests
better, but tell Lane.

- **A verse sibling**, anchored with `data-anchor="C:V"` like echo and
  synoptic, after the verse the story bears on (or after the last verse of the
  scene it covers). Optional `data-span="C:V–C:V"`.
- **Hidden by default behind its own chip**, one chip per box (`toggle` with
  `each`, as synoptic does; see `biblecore/web/app/spotlight.js`). Glyph ◈, its
  own accent. Olive is the suggestion: it's distinct from echo's Jordan blue,
  synoptic's crimson and the Rendering gold. Check `data/palette.json` and the
  theme accents, and show Lane if it's close to anything.
- **The chip label follows the kind**: `data-kind="type-scene"` → "Type
  scene"; anything else (`story`, `allusion`, `character`, `reuse`) → "Earlier
  story". The chip shows the glyph and that label only, no story title (Lane's
  call). Per-element labels may need a small extension to spotlight.js's
  `toggle` handling; make it generic, so it reads a label map from
  component.json.
- **Inside the box**, a header with the reference(s) and a short title, then
  the body:
  - `par-story`: the earlier story in two to four plain sentences.
  - `par-match`: what's the same (a short list).
  - `par-diff`: what's different. **Required**; nothing ships without a stated
    difference.
  - `par-does`: what it does in Matthew (irony, reversal, identification,
    fulfilment, warning).
  - `par-later`: later reuse, optional.

  Class names may change to fit core conventions. `previews/parallel-preview.html`
  is a mock-up of the box's insides; the always-visible hook and "more ▾" there
  are superseded by the chip.
- **The validator checks**: anchor shape, required parts present (ref, story,
  diff, does), `data-kind` and `data-strength` in their sets (`strong` |
  `possible`; weak never ships), transliteration only (no Greek or Hebrew
  script), and no `data-root`, `class="r"` or `class="rl"` inside (same reason
  as echo/synoptic: the occurrence scanner counts every `data-root`).
- **The canon harvest**: a story box becomes an `intertext[]` row, the way
  echoes are harvested today (check `biblecore/canon.py` for the row shape and
  allowed kinds, and extend them rather than inventing a meta key). A
  `type-scene` box also yields a `typescenes[]` row. Adding a *new* type-scene
  id to core's shared list needs Lane's OK by popup each time.
- Light/dark safe via theme variables, readable at phone width, all bodies
  expanded in print.
- No floor and no per-unit cap. No `sweep[]` meta key.

## 2. Synoptics (bible-core snippet + Matthew style reference)

- Drop the "0–3 per unit" cap (style reference §3, synoptic section, and core's
  `components/synoptic/snippet.md` if it carries one).
- New norm: every scene where Mark, Luke or John tell the same event gets
  checked, and every one where Matthew's change is telling (an addition, an
  omission, a reordering, a rewording that shifts the point) gets a box.
  Expect roughly three to six per unit. It still sits behind its ✧ chip.

## 3. Pass structure (bible-core `canon/workflow.md`, the default for every book)

Passes 1 and 3 are for Lane: he listens to them read aloud. Passes 2 and 4 are
working passes, split out so the chat side isn't doing too much in one turn and
losing context.

1. **Briefing (for listening).** As now: flowing prose, no headers or bullets.
   Its intertextual setup also names the earlier stories the unit seems to lean
   on, scene by scene, without telling them yet.
2. **Research (a working pass, not presented).** Per scene:
   - the people, places and objects, and where they appeared before;
   - the story shape;
   - the nearest earlier story with that shape, read in the target text;
   - what's the same and what's different;
   - what it does in Matthew;
   - later reuse.

   Then the word leads (`canon-leads-unit-NN.md`): leads inside a found story
   attach to it as evidence; the rest are judged on their own (echo, root echo,
   footnote, drop). Then each scene against its Mark/Luke/John parallels. Prune
   as you go. The output is a **notes file** (chat-side output; it doubles as
   the full ledger, rejected rows included) that passes 3 and 4 read. In chat
   it's one line: research done, ready for the verse-by-verse. Lane doesn't
   read the notes file.
3. **Verse-by-verse (for listening).** As now, but built on pass 2: when a
   verse reaches an earlier story, tell it there, with its background, the
   match, the difference and what Matthew does. Meaningful synoptic
   differences are spoken in place too. Spoken style throughout: no verse
   numbers, references or Greek in the telling. It ends with a short spoken
   list of what will go into the artifact (story boxes, synoptic boxes,
   notable echoes). That list is Lane's veto point, and usually a quick yes.
4. **Artifact (a working pass).** Built from the notes file and pass 3.

Also:
- Renumber "Seven standing moves during pass 2" to the verse-by-verse (now
  pass 3), and make the type-scene move point at `aside.story`.
- Drop "every lead on the sheet gets a row" and "considers fifteen to thirty
  links and keeps six to twelve".
- Grep core and the book for other pass-number references (instruction
  template, conventions, style reference, `CHAT_SIDE_INSTRUCTIONS.md`) and
  renumber them.

## 4. Leads (bible-core `biblecore/leads.py`)

The rare-word/phrase sheet stays; it's an input to pass 2. Add a second
section or sheet: a **noun sweep** of every proper noun and every narrative
noun in the unit, with no rarity cutoff, each with its first LXX occurrence
and its occurrences in the other gospels. It's not a judgment, just
candidates the rarity cutoff hides. Group it by scene if the unit map gives
scene boundaries, by verse otherwise. Keep it short enough to read; the
narrative-noun filter is a judgment call, so propose it to Lane.

## 5. Matthew

- Vendor the new core (`python ../bible-core/tools/core_sync.py .`), enable
  `story` in `book.json` `components`, then build and test. `migrate` skips the
  boxed units 1–13; leave them alone.
- `matthew_study_style_reference.md`:
  - §1a gets the "what belongs where" table above;
  - §3 gets the `aside.story` markup and rules, and the synoptic cap change;
  - §4's checklist gets the story-box checks (stated difference, anchor,
    translit only, nothing weak);
  - add a dated ruling (2026-10-25, Lane) with the reason;
  - carry forward the unresolved §3 vs §4 point on endnote markers inside a
    gloss.
- `CHAT_SIDE_INSTRUCTIONS.md`: the new pass order, the story-box verdict, the
  synoptic norm, pass 3's closing list. Lane pastes it into the project field
  afterwards; run `sync-check --mark-pasted` once he says it's done.
- Theme: if the ◈ chip needs a Matthew touch, put it in `css/theme.css`, not
  core.

## 6. Pilot: rebuild Unit 15

Code can't write the unit's content: the story boxes come from the chat side
running the new loop on Unit 15. So the order is: ship the core and Matthew
changes, sync, have Lane paste the field, Lane runs Unit 15 in the research
project, then `port 15 --force`. Diff against the shipped unit and ask Lane
before committing the replacement. Unit 14 waits until Lane has seen the
pilot.

## Working rules

- `../bible-core` may have another session working in it: check `git status`
  there and here first, use a worktree if either is dirty, and stage explicit
  paths.
- A core release: bump the version, sync to Matthew (and say whether Numbers
  and Joshua need re-vendoring), and `python -m biblecore test` green in each
  book touched.
- Lane never runs commands; ask him only for pastes, saves and decisions.
  Decisions go by popup, recommended option first.
- Commit, push and `sync` after Lane's OK. After pushing, say "pushed" and
  move on.
- Delete `previews/` and both handoff files once the build lands (ask first).
- Keep the session files (`session_index.md`, `improvements_log.md`,
  `session_summary_[timestamp].md`).
