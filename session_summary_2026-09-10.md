# Session summary — 2026-09-10

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
- **`build.py` is not safe to run casually.** Its step 1 (`extract_units.py`)
  regenerates fragments from `source-artifacts/` and drops every post-extract
  direct edit not in `retrofit-tags.json` — pericope headings, synoptic boxes,
  chiasm cuts, prev/next nav. Confirmed by test (8 units diverged). `strip_span`
  fixes only the `.star` case. For a data/thread change, run the 4 downstream
  steps directly (`apply_retrofit → refresh_meta → scan_occurrences →
  verify_occurrences → threads_digest`). Documented in CLAUDE.md. Making build.py
  truly safe is a real architectural question (encode every divergence, or treat
  units/ as source of truth) — for a future session.
- `MatthewSBLGNT.txt` is **tracked** in the repo root — Lane's call (he edited
  CLAUDE.md mid-session: "Greek (SBLGNT) lives in the repo for easy access", and
  loosened the transliteration rule to only cover the rendered `unit.html` page,
  so Greek in `pipeline/` and `data/` is now explicitly fine). Audit still
  degrades with a clear message if the file is absent.
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
- build.py safety — architectural.
