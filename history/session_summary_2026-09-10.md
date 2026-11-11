# Session summary — 2026-09-10

## Headline: 5-phase thread-add restructure — complete

Adding a tracked thread was error-prone because the hard part (finding every
occurrence) was manual and the file-editing looked bigger than it was. All five
phases shipped and pushed:

1. **`audit_thread_coverage.py --forms`** + `pipeline/research-prompts.md` (the
   stems prompt for the Claude.ai project).
2. **Exact chapter/verse alignment** — the audit derives the canonical (ch,v)
   sequence straight from `MatthewSBLGNT.txt`, no more heading heuristics;
   `--unit` scope + `coverage_for_unit()` for the porter. Handles the Lord's
   Prayer hole (`.prayer` not `.v`), unit-10's `11:1`, final-sigma folding,
   `^`-anchored stems.
3. **New meta fields** `note` / `candidates.stems` + a richer thread-delta
   report (coverage gaps as retrofit lines, candidate stem previews, ready
   `threads.json` entries). `port_artifact --src PATH` to dry-run on a practice
   fragment.
4. **`threads.retro[]`** — fix-list for earlier units, dry-checked and merged
   into generated `pipeline/retro-tags.json` (kept separate so retrofit-tags.json
   stays hand-formatted). Porter **structure checks**: pericope headings + ·C:V
   range, no old heading classes, `aside.synoptic` data-anchor + translit-only.
5. **Style reference** updated (§2 new fields, §3 chapter-crossing pericopes,
   §4/§6a "tag every occurrence, follow the lexeme not the gloss").

### build.py made safe (Lane's call, mid-session)
Dropped `extract_units.py` from `STEPS` — it was the Phase-1 batch normalizer,
now a `port_artifact` library only. Running it wiped post-extract direct edits.
build.py is now replay-retrofit → refresh_meta → scan → verify → digest → audit
(advisory). Verified idempotent.

### All 24 audited threads clean — 0 coverage gaps
16 remaining stems folded in (research project), with `release` retidied and
`faith`/`little-faith` split. Pre-opening coverage pass: **throw** (+11 tags,
units 3-6, broad range; +6 retagged from unit-07's misapplied local `do`;
recoloured #a85520→#c2410c), **torment** (+1), **hand-over** (+2, recoloured
#8a3c70→#0e8aa0 off the shared purple). occurrences 423 → 437.

## Older items this session

## Done

### Desktop width
- `css/styles.css`: `--maxw` 790px → **100%** (four steps over the conversation).
  Content fills the monitor minus the shared 26px side padding. Mobile untouched.
- Open: verse prose runs long on wide monitors — Lane to eyeball; easy revert to
  a fixed cap (1000–1150px).

### New tracked thread: `sin` (hamartia / hamartōlos)
- `data/threads.json`: `sin`, translit `hamartia · hamartanō`, colour `#8a4a5a`,
  opens 1:21, payoffs 9:2-6+10-13 and 26:28.
- Tagged **8** occurrences in built units: 1:21, 3:6, 9:2/5/6 (first pass), then
  9:10/11/13 (ἁμαρτωλός "sinner" — same root, different English, **missed by the
  first English-grep pass, caught by the new audit tool**). 9:13 is the Hosea 6:6
  verse where `mercy` lands.
- `verify_occurrences` green; `audit_thread_coverage` reports `sin` clean.

### Thread-add tooling (the actual ask: efficiency + reliability)
- **`pipeline/audit_thread_coverage.py`** (new). Scans `MatthewSBLGNT.txt` for
  every morphological occurrence of a thread's Greek root; flags any inside a
  BUILT unit's passage with no `data-root` span. Also flags the reverse
  (tagged-but-no-root). `--stub <id>` emits ready `retrofit-tags.json` lines.
  Accent-insensitive **substring** match (augment/reduplication break prefixes:
  ἠκολούθησαν vs ἀκολουθεῖ). Transliterates via `pipeline/greek.py`.
- **`pipeline/thread-stems.json`** (new). Greek `stems` + `exclude` per thread.
  `phrase: true` for fixed-title threads (skipped). Seeded & verified: `sin`,
  `fear`, `sea`, `follow`, `fish`, `authority`, `hand-over`, `cross`. 16 threads
  still undefined — the audit lists them; fill in one at a time (each stem needs
  a look at what it drags in, e.g. `mercy` ελε- catches Ἐλεάζαρ / τέλειος).
- **`strip_span` op** added to `apply_retrofit.py`; the cut `.star` device
  (units 2/3/7) is now encoded in `retrofit-tags.json` instead of a prose note.
- New add-a-thread workflow written into `CLAUDE.md`: 2 hand-authored files
  (threads.json + thread-stems.json), then the audit finds the occurrences.

### Findings the tool surfaced (not acted on)
- **`hand-over` has 2 pre-opening gaps**: 4:12 (παρεδόθη, "John was handed over")
  and 5:25 (παραδῷ, "lest the adversary hand you over"). Both real paradidōmi in
  built units, never retro-tagged. **Deferred** — tagging 4:12 collides in
  unit-04 with `apo-tote` (both `#8a3c70`; verify fails). Fix = give `hand-over`
  its own colour (it shares `#8a3c70` with apo-tote / emmanuel / son-of-david),
  then add the 2 tags. Small separate task.

## Takeaways / decisions
- **`build.py` made safe** (Lane's call, done this session). Dropped
  `extract_units.py` from `STEPS` — it was the Phase-1 batch normalizer, already
  finished its job, and now exists only as a library `port_artifact.py` imports.
  Running it as a build step regenerated fragments from `source-artifacts/` and
  dropped every post-extract direct edit (confirmed by test: 8 units diverged).
  `build.py` now = replay `retrofit-tags.json` (idempotent) → `refresh_meta` →
  `scan` → `verify` → `digest` → coverage audit (advisory). Fragments are the
  source of truth. Verified idempotent (re-run touches nothing).
- `MatthewSBLGNT.txt` is **tracked** in the repo root (Lane put it there and
  wants it in the repo). He also loosened the transliteration rule to only cover
  the rendered `unit.html` page, so Greek in `pipeline/` and `data/` is fine.
  Audit degrades with a clear message if the file is absent. CLAUDE.md "Source
  texts" rewritten to point only at the in-repo file — the old external
  `Personal/Biblical Texts/Gospels/` path was a mistake and is gone; nothing
  outside the Matthew folder is needed.
- CLAUDE.md doc for the new tools: Lane trimmed my additions to the pipeline
  section — left to him to place (PLAN.md or a lean CLAUDE.md line). The
  add-a-thread workflow is written up in this summary and improvements_log.
- Adding stems is genuine lexical work — verify each against the whole book
  before trusting. Single stems are unreliable (σῴζω has zero σωζ- forms in
  Matthew; needs σωσ/σωθ/σεσω + exclude for δοξάσωσιν).

## Open questions
- Desktop line length at `--maxw: 100%`.
- `hand-over` colour + its 2 gaps.
- The 16 undefined thread stems — incremental backlog, audit tracks it.
- (resolved) build.py safety — done, see above.
