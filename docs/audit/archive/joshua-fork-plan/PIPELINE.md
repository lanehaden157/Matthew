> **ARCHIVED — historical, superseded by the Joshua repo.**
> Written 2026-09-12 as the plan for forking Matthew into a Hebrew book, before
> Joshua existed. Joshua was then built and diverged from this plan in ways that
> matter: root identity moved from substring stems to lexicon-id sets (`roots.json`
> + `data-w`), `candidates[].stems` is gone, the `greek-title` masthead and the
> `<p id="n1">` endnote shape were both replaced. **Read this as a record of what
> was intended, never as instructions.** The live documents are in the Joshua repo
> (`../Joshua/`), and the current cross-project plan is `platform-design-review.md`.

# Pipeline — one unit, end to end

Both halves: what happens in the Claude.ai research project and what happens in
the repo. Every step is marked:

- **[auto]** — a script does it; you type one command or nothing
- **[manual]** — a human does it; nothing detects it if skipped
- **[manual ⚠]** — a human does it, **and Matthew shipped a bug because it was
  skipped or done inconsistently**. These are the ones to watch.

---

## The loop, at a glance

```
Claude.ai research project                          the repo
──────────────────────────                          ────────
reads threads-digest.md          ◄──────────────────  pipeline/threads_digest.py  [auto]
reads translation-choices.md     ◄──────────────────  (hand-maintained)        [manual ⚠]
reads instructions.md            ◄──────────────────  (hand-maintained)           [manual]
reads <book>_style_reference.md  ◄──────────────────  (hand-maintained)           [manual]
reads the source text            ◄──────────────────  (same file, copied)      [manual ⚠]
   │
   │ pass 1 pre-read briefing      (chat)
   │ pass 2 verse-by-verse         (chat)
   │ pass 3 HTML artifact          (file)
   ▼
source-artifacts/<book>_NN_translation.html          [manual: download + place]
   │
   │  python pipeline/port_artifact.py NN --dry      [auto]
   │  …review, fix the artifact, repeat…             [manual]
   │  python pipeline/port_artifact.py NN            [auto]
   ▼
units/unit-NN.html + data/units.json + pipeline/retro-tags.json
   │                        ↳ apply_retrofit → scan → verify   [auto, chained]
   ▼
pipeline/out/thread-delta-NN.md
   │
   │  Lane reads it                                  [manual ⚠]
   ▼
data/threads.json edits · translation-choices.md edits        [manual ⚠]
   │
   │  python pipeline/build.py                       [auto]
   │  browser check                                  [manual]
   │  git commit                                     [manual]
   ▼
threads-digest.md regenerated → paste back into the research project  [manual ⚠]
```

---

## A. Research-project side

### A1. Confirm scope **[manual]**

State the unit and passage from the Literary Unit Map, flag any divergence from
the chapter grid, and surface open scoping questions before starting. If the
request conflicts with the session record (a unit already shipped), raise it as a
question rather than silently rebuilding.

### A2. Pass 1 — pre-read briefing **[manual]**

Chat, flowing prose. Literary and structural placement, ANE background, genre,
intertextual setup, the vocabulary to watch, the interpretive tensions. Orient,
don't resolve. Pause and present.

### A3. Pass 2 — verse-by-verse **[manual]**

Chat, same prose style. Transliterated Hebrew quoted alongside the English.
Throughout this pass:

- Check every surfacing root against **`threads-digest.md`**. When a tracked
  thread opens or pays off, name it and draft the one-line popover sentence that
  will become the meta block's `note` field.
- A root recurring across units but not yet tracked → flag as a **candidate**.
  Lane decides. Do not start treating it as a thread.
- A missed or wrong tag noticed in an *earlier* unit → it becomes a
  `threads.retro` entry in pass 3, not a prose "we should revisit unit 4" aside.
- Before choosing an English word for a Hebrew lexeme, check
  **`translation-choices.md`**. Match the prior decision, or deviate *and flag
  the deviation explicitly* so Lane can decide whether it is a one-off or a
  correction that should propagate.

Pause and present.

### A4. Pass 3 — the artifact **[manual]**

Only after Lane confirms. Produces one `<article>` fragment, no `<head>`, no
`<style>`. Contract and worked example: `PROJECT-INSTRUCTIONS.md`.

Run the style-reference checklist before saving. Save zero-padded as
`<book>_NN_translation.html` and present the file.

### A5. Download and place **[manual]**

Put the file at `source-artifacts/<book>_NN_translation.html` in the repo. The
porter globs `<book>_NN_*.html`, so the tail of the name is flexible; the
zero-padded number is not.

---

## B. Repo side

### B1. Dry run **[auto]**

```
python pipeline/port_artifact.py NN --dry
```

Writes nothing. Validates the meta block, builds the fragment in memory, and
writes the full thread-delta report so you can see everything the real run would
do. **Always do this first.** A `--src PATH` variant dry-runs against a file
outside `source-artifacts/`.

Two things fail here rather than later:

- **Metadata invalid** → prints every problem and exits 1. Nothing is written.
- **Structure warnings** → appear in the thread delta as
  "Fragment structure — fix in the artifact." These do *not* block the port, so
  read them.

If the artifact needs fixing, fix it in the research project and re-download —
**do not hand-patch `source-artifacts/`.** That directory is the untouched record
of what the research project produced; divergence between it and the fragment is
how you lose the ability to re-port.

### B2. Real port **[auto]**

```
python pipeline/port_artifact.py NN
```

In order:

1. Reduces the artifact to a validated `<article>` fragment.
2. Merges the unit's row into `data/units.json`, assigning a local hue to every
   declared root that is *not* a tracked thread — collision-checked in perceptual
   colour space against both the unit's existing local hues and the global colour
   of every thread the unit uses.
3. Merges `threads.retro` (fixes for *earlier* units) into
   `pipeline/retro-tags.json`, dry-checking each entry against its target
   fragment first. Entries that wouldn't apply cleanly are **reported, not
   written**.
4. Re-injects a normalized meta block and writes `units/unit-NN.html`.
5. Chains `apply_retrofit.py → scan_occurrences.py → verify_occurrences.py`.
6. Writes `pipeline/out/thread-delta-NN.md` against the fragment as it now
   stands on disk.

**`data/threads.json` is never written by this command.** By design — see
`CLAUDE.md`.

### B3. Read the thread delta **[manual ⚠]**

`pipeline/out/thread-delta-NN.md` is the one output meant for a human, and the
step most likely to get skipped when a port "looks fine." It contains:

- **opens/payoffs** needing a `tagged` / `status` flip, each with a ready-to-paste
  `threads.json` entry including the popover `note`.
- **New-thread candidates**, each with a stem/lemma preview and match counts
  across the whole book.
- **Retro fixes** merged into earlier units.
- **Fragment-structure warnings.**
- **Coverage**: every occurrence of a tracked root the source text has in this
  passage that the fragment left untagged, formatted as ready `retrofit-tags.json`
  lines — plus the reverse (tagged where the root isn't there).

> Coverage is where the real defects surface. Matthew's `sin` thread was missing
> *hamartōlos* at 9:10–13 and nobody noticed until this report existed
> (commit `d95b5c4`).

### B4. Apply the delta by hand **[manual ⚠]**

Edit `data/threads.json` for the entries you accept. Add `retrofit-tags.json`
lines for the coverage gaps you accept. Both are judgement calls; the porter
deliberately can't make them.

### B5. Update `translation-choices.md` **[manual ⚠]**

**In the same turn, before moving on.** Any rendering decided or changed in this
unit gets its row updated and a Log entry, the same way `build.py` gets run
without being asked.

> Matthew let this slide until unit 10 and paid with a dedicated wording-audit
> session plus a retroactive pass across everything already shipped
> (`b0f73cc`, `aed087e`, `0138548`). This step is cheap only if it is never
> deferred.

### B6. Rebuild **[auto]**

```
python pipeline/build.py
```

1. `apply_retrofit.py` — replay both fix-lists onto the fragments (idempotent)
2. `refresh_meta.py` — regenerate every built fragment's meta block from the data
3. `scan_occurrences.py` → `data/occurrences.json`
4. `verify_occurrences.py` — independent re-derivation, colour resolution, colour
   collision, endnote integrity, script leakage. **Exits non-zero on failure.**
5. `threads_digest.py` → `threads-digest.md`
6. *(advisory)* `audit_thread_coverage.py --check` — never fails the build

`build.py` never regenerates a fragment from `source-artifacts/`. See
`CLAUDE.md` — this rule cost eight diverged units to learn.

### B7. Browser check **[manual]**

Load the unit. Confirm: colours resolve, the legend renders with a colour key
(a missing legend is silent — see below), thread popovers open, endnote links
jump, no horizontal scroll at ~375px.

### B8. Commit **[manual]**

### B9. Re-paste the digest **[manual ⚠]**

If `threads.json` changed, `build.py` regenerated `threads-digest.md`. **Paste it
into the Claude.ai project.** Nothing detects the drift if you don't, and the
next artifact will tag against a stale thread list.

Same for `translation-choices.md` if B5 changed it.

---

## C. The manual steps that bit Matthew

Five sync points have no enforcement. Ranked by what went wrong:

**1. `translation-choices.md` upkeep (B5).** Deferred to unit 10; cost a full
audit session and a retroactive pass. *Mitigation in Joshua:* the file exists from
unit 1 and CLAUDE.md makes updating it a same-turn workflow step, not a separate
ask.

**2. Reading the thread delta (B3–B4).** The report is generated whether or not
anyone reads it. There is no "delta acknowledged" state. *Mitigation:* nothing
technical — this is the human-judgement step the whole design is built around.
Just don't skip it.

**3. Digest re-paste (B9).** *Mitigation:* make it the last line of every session
summary, and treat a `threads.json` diff without a digest re-paste as an
incomplete session.

**4. Source-text sync.** The research project's copy and the repo's copy must be
byte-identical or the coverage audit's verse alignment silently disagrees with the
artifact's. *Mitigation:* record a checksum in `CLAUDE.md` when the file is
placed, and re-check it if alignment warnings ever appear.

**5. Instructions/style-reference sync.** The contract lives in three places
(repo `instructions.md`, the style reference, the Claude.ai project's own
instructions field). Matthew's drifted — commit `daf5710` fixed a `CLAUDE.md`
section pointing at a path that no longer held anything. *Mitigation:* keep the
paste-block in `CLAUDE.md` as the single authored copy and paste *from* it, never
edit the project's field directly.

---

## D. Steps that are automated in Joshua but were manual in Matthew

These are the concrete process improvements the audit paid for. Each was a
human-noticed problem in Matthew and is a check here.

| Was | Now |
|---|---|
| Missing legend caught by eye, or not at all — Unit 11 shipped without one and the live site renders it with no colour key | `port_artifact.py` structure check |
| Endnote `href`/`id` pairing stated in the style reference, checked nowhere | `verify_occurrences.py` assertion |
| Native script in attribute values — Matthew still ships Greek in a `logeion.uchicago.edu/προσκυνέω` href | `verify_occurrences.py` grep over whole fragments |
| Unknown meta keys accepted and silently dropped — `descriptor` and `discourse` authored for eleven units, consumed by nothing | `unit_meta.validate()` unknown-key error |
| New CSS classes invented in artifacts, discovered when they rendered unstyled | `build.py` component-whitelist advisory step |
| Book prefix and source filename hardcoded in the audit | read from `data/units.json` |

Still manual, deliberately: everything in §C. Those are judgement, not mechanism.
