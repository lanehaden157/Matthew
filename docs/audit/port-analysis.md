# Port Analysis: Reusing the Matthew Pipeline for a Hebrew Book

Read-only audit. No code was changed to produce this. All claims are cited to
file paths and line ranges as of commit `0138548` (2026-09-12, `main`,
working tree clean). Line numbers will drift as the repo changes — re-check
before trusting a specific number.

---

## 1. Classification: every pipeline script, data file, and convention

Legend: **LN** = language-neutral (mechanism has no Greek/Hebrew assumption
baked in) · **GK** = Greek-specific (assumes Greek script, phonology, or
morphology) · **MT** = Matthew-specific (assumes this book's content,
structure, or one-time history, independent of language).

A file can carry more than one classification when its *mechanism* and its
*data* differ — noted inline.

### 1.1 `pipeline/greek.py` — **GK**, entirely

The whole module is a deterministic Greek→Latin transliterator with no
generality attempted or claimed (its own docstring, [greek.py:1-4](pipeline/greek.py#L1-L4)).

| Assumption | Lines | Hebrew equivalent behavior |
|---|---|---|
| `_BASE` maps 24 Greek letters 1:1 to Latin | [greek.py:8-13](pipeline/greek.py#L8-L13) | Hebrew has 22 consonants, no vowel letters in the same sense (vowels are points or matres lectionis) — a structurally different table, not a data swap |
| `_DIPH` — Greek diphthongs (ου, αι, γγ→ng, etc.) | [greek.py:14-18](pipeline/greek.py#L14-L18) | No analog; Hebrew's parallel problem is matres lectionis (ו/י standing in for vowels) and begadkefat spirantization — unmodeled |
| Rough breathing → prepend `h` | [greek.py:37,52-53,76-85](pipeline/greek.py#L37) | No Hebrew analog (Hebrew has no breathing marks; it has dagesh, which changes plosive/fricative, unrelated) |
| Detection gate: only fires on Greek Unicode ranges `Ͱ-Ͽ`, `ἀ-῿` | [greek.py:34](pipeline/greek.py#L34) | **Silent pass-through.** Hebrew text (U+0590–05FF, U+FB1D–FB4F) does not match either range, so `transliterate()` returns it completely unchanged — no exception, no log line from this module. Anyone who assumes `greek.transliterate()` is "the transliterator" for a Hebrew project would ship untransliterated Hebrew script silently. |

**Verdict:** not portable as-is. A Hebrew project needs a **new sibling
module** (`hebrew.py`) playing the same architectural role — a single
deterministic scheme, logged, reviewed by a human — not a parameterization
of this file. The *pattern* (one small pure function, unit-testable via its
own `__main__` block, [greek.py:88-91](pipeline/greek.py#L88-L91)) is worth
copying exactly.

### 1.2 `pipeline/extract_units.py` — mixed, mostly **MT** (one-time), partly **GK**, mechanism **LN**

This file is explicitly retired from the live pipeline (`build.py`'s own
docstring, [build.py:14-16](pipeline/build.py#L14-L16): "extract_units.py did
that once (Phase 1) and now lives only as a library port_artifact.py
imports"). It is still load-bearing, though — `port_artifact.py` imports 8 of
its functions ([port_artifact.py:43,102-113](pipeline/port_artifact.py#L102-L113)).

| Piece | Lines | Class | Note |
|---|---|---|---|
| `GREEK`/`HEBREW`/`SCRIPT` Unicode-range regexes | [extract_units.py:30-34](pipeline/extract_units.py#L30-L34) | GK+data for HB | Already carries a Hebrew range — but only to *strip* stray Hebrew loanwords embedded in Matthew's Greek text (place names, "Gehenna," "shamayim"), not to process a Hebrew-primary source |
| `_translit_token` dispatcher | [extract_units.py:220-231](pipeline/extract_units.py#L220-L231) | LN mechanism | Correctly routes Hebrew → `_rom_hebrew`, Greek → `greek.transliterate`. The *routing* is reusable |
| `_HEB` / `_rom_hebrew` — naive consonant-only romanizer | [extract_units.py:234-245](pipeline/extract_units.py#L234-L245) | **GK-analog gap** | Maps 22 consonants; explicitly **drops** niqqud/cantillation points (the `"֑" <= c <= "ׇ"` range is discarded, not rendered as vowels — [extract_units.py:245](pipeline/extract_units.py#L245)). Every hit is tagged `(REVIEW)` in the log ([extract_units.py:227](pipeline/extract_units.py#L227)) precisely because it's a stopgap for a handful of loanwords, not a real scheme. For a Hebrew-primary book this crude table would become the **primary** transliteration path with **zero vowel information** unless someone builds a real Hebrew equivalent of `greek.py`. This is a *silent* degradation risk: it produces plausible-looking output (a consonantal skeleton) with no error, so a reviewer has to know to distrust it rather than being told to. |
| `MANUAL` hand-correction dict (4 entries) | [extract_units.py:212-217](pipeline/extract_units.py#L212-L217) | MT data | Matthew-specific vocabulary; the *mechanism* (an override table consulted before the deterministic pass) is a good pattern to keep |
| `normalize_verses` / `normalize_blocks` — Unit-1-only reshaping | [extract_units.py:43-105](pipeline/extract_units.py#L43-L105) | MT, one-time debt | Fixes pre-convention markup drift specific to this project's own history (see §3). Harmless no-op for a fresh book — nothing to migrate, but also nothing worth porting. |
| `fix_greek_title` — parses `<div class="greek-title">` | [extract_units.py:156-179](pipeline/extract_units.py#L156-L179) | LN mechanism, GK naming | Text-processing logic (split on em dash, extract translit/gloss) has no language dependency; the *class name* `greek-title` is a naming leftover that a Hebrew project would either rename or knowingly reuse |
| `GKSPAN` / `strip_gk_spans` | [extract_units.py:182-207](pipeline/extract_units.py#L182-L207) | LN mechanism (checks `SCRIPT`, both ranges), GK naming | Actually script-agnostic in behavior already — the class is called `gk` but the regex and dispatch handle Hebrew too via `_translit_token` |
| `rewrite_roots`, `prefix_endnotes`, `clean_redundancy` | [extract_units.py:248-333](pipeline/extract_units.py#L248-L333) | **LN** | Pure span/id rewriting, no language assumption at all |
| `ROOT_ALIASES = {"wild": "wilderness"}` | [extract_units.py:300](pipeline/extract_units.py#L300) | MT data | One Matthew-specific rename, structurally reusable pattern |

### 1.3 `pipeline/apply_retrofit.py` — **LN**, entirely

Every operation (`add`, `retag`, `unwrap`, `retag_word`, `untag_word`,
`text`, `strip_span`) works on generic `<span data-root="X">` markup and
plain regex text substitution — [apply_retrofit.py:1-22](pipeline/apply_retrofit.py#L1-L22)
for the op catalogue, [apply_retrofit.py:39-152](pipeline/apply_retrofit.py#L39-L152)
for implementations. Nothing here reads or assumes anything about Greek,
Hebrew, or Matthew. `retrofit-tags.json`'s *content* is Matthew-specific data;
the *engine* is a fully portable "patch a static HTML fragment idempotently"
tool.

### 1.4 `pipeline/audit_thread_coverage.py` — mixed: engine **LN**, one hardcoded assumption is **MT** (fails loud), one gap is a **GK-analog silent risk**

This is the most consequential file to get right for a Hebrew port, because
it is the project's central integrity check (see §4).

| Piece | Lines | Class | Fails how for Hebrew |
|---|---|---|---|
| Source-file line format `Matt (\d+):(\d+)\t(.*)` | [audit_thread_coverage.py:75](pipeline/audit_thread_coverage.py#L75) | **MT**, hardcoded literal `"Matt"` | **Loud.** A Joshua/Judges text file using `Josh 1:1\t…` or `Judg 1:1\t…` lines won't match at all; `verses` comes back empty and the script exits with `"[audit] {GREEK} parsed to zero verses — wrong format?"` ([audit_thread_coverage.py:79](pipeline/audit_thread_coverage.py#L79)). Easy, well-guarded fix — parameterize the book prefix. |
| Hardcoded source filename `MatthewSBLGNT.txt` | [audit_thread_coverage.py:45](pipeline/audit_thread_coverage.py#L45) | MT | Loud (file-not-found exit, [audit_thread_coverage.py:70-72](pipeline/audit_thread_coverage.py#L70-L72)) — trivial rename |
| `strip_accents` — folds Greek final sigma ς→σ | [audit_thread_coverage.py:55-60](pipeline/audit_thread_coverage.py#L55-L60) | **GK, and this is the sharpest transferable lesson in the whole audit** | This exists because of a real, already-fixed bug (commit `6453a4b`, see §3): a stem written `φωσ` didn't match `φῶς` because word-final ς is a distinct codepoint from medial σ. **Hebrew has the identical class of problem**: five letters have distinct final forms — ך/כ, ם/מ, ן/נ, ף/פ, ץ/צ. `strip_accents` has no fold for these. A Hebrew stem-matching audit built by copying this function verbatim would **silently under-match** on every root that happens to end a word in its lexical form — the exact bug Matthew already paid to fix, recurring for free. This is worth fixing *before* first use, not after discovery. |
| `GREEKWORD = re.compile(r"[^\W\d_]+", re.UNICODE)` word tokenizer | [audit_thread_coverage.py:52](pipeline/audit_thread_coverage.py#L52) | **LN** | Matches any Unicode word character, including Hebrew — no change needed |
| Stem-substring matching (`_compile_stems`, `^`-anchored word-start) | [audit_thread_coverage.py:83-94](pipeline/audit_thread_coverage.py#L83-L94) | **LN mechanism** | The technique (accent-stripped substring or prefix match against a hand-authored stem list) is language-agnostic. Hebrew's own prefix-stacking (ו/ה/ל/ב/כ/מ conjunctions and prepositions glued to the head of a word) is a mirror-image problem to Greek's augment/reduplication defeating prefix matching (documented at [thread-stems.json:2](pipeline/thread-stems.json#L2)) — the *same* accommodation (don't anchor on `^` for roots that take prefixes) transfers directly, it just needs to be *known* going in rather than discovered. |
| `expected_seq` / chapter rollover derived from the source text, never guessed | [audit_thread_coverage.py:138-167](pipeline/audit_thread_coverage.py#L138-L167) | **LN principle** | Explicitly documented as deliberate ([audit_thread_coverage.py:161-167](pipeline/audit_thread_coverage.py#L161-L167): "No heuristics for the chapter... anything that won't line up is reported, never guessed"). This resulted from a real bug (commit `d6185f8`, §3) and is a principle, not code, that must be re-applied — Joshua and Judges both have their own verse-numbering irregularities across traditions/manuscripts, so the same "derive from source, never guess" discipline is exactly as necessary there. |

### 1.5 `pipeline/thread-stems.json` — **MT/GK data**, schema **LN**

Pure Matthew-content data (Greek stems per tracked thread). The *shape*
(`stems: [...]`, `exclude: [...]`, `phrase: true`, leading-`^` anchor
convention, documented in its own `_note` field, [thread-stems.json:2](pipeline/thread-stems.json#L2))
is directly reusable for Hebrew stems; none of it transfers as data.

### 1.6 `pipeline/port_artifact.py` — **LN**, one **MT genre assumption**

| Piece | Lines | Class |
|---|---|---|
| `WELL` hue palette, `_lab`/`_de` perceptual-distance math, `assign_hues` | [port_artifact.py:52-92](pipeline/port_artifact.py#L52-L92) | **LN** — pure color science, no language or book dependency |
| `to_fragment`, `merge_units_json`, `thread_delta`, `merge_retro` | [port_artifact.py:97-407](pipeline/port_artifact.py#L97-L407) | **LN** — all operate on the generic unit-meta schema |
| `_append_structure`'s synoptic-aside checks | [port_artifact.py:247-287](pipeline/port_artifact.py#L266-L287) | **MT, genre-specific, not language-specific** | The `<aside class="synoptic">` convention encodes Gospel-parallel comparison (Matthew/Mark/Luke), a structure that doesn't exist for Joshua/Judges in the same sense (no "synoptic" parallel book in the same genre; at most a Judges↔Samuel/Kings echo, which is a different kind of cross-reference). This check would simply never fire for a Hebrew narrative book — graceful no-op, not a break — but it signals that the "compare boxes" concept (§4, Phase 7 in `PLAN.md`) may need a different shape for narrative rather than sermon/discourse material. |
| `_append_coverage`, pericope-heading check | [port_artifact.py:252-264,321-355](pipeline/port_artifact.py#L252-L264) | **LN** — heading-shape and thread-coverage checks are book-agnostic |

### 1.7 `pipeline/unit_meta.py` — **LN**, entirely

Parses/validates/generates a JSON schema (`unit`, `slug`, `passage`, `title`,
`movement`, `roots[]`, `threads{opens,payoffs,candidates,retro}` —
[unit_meta.py:9-42](pipeline/unit_meta.py#L9-L42)) with no language or book
assumption anywhere in `validate()` or `generate()`
([unit_meta.py:103-247](pipeline/unit_meta.py#L103-L247)). This is the single
most directly portable file in the pipeline — it could be pointed at a
Hebrew project's `data/units.json` / `data/threads.json` unchanged.

### 1.8 `pipeline/threads_digest.py`, `pipeline/scan_occurrences.py`, `pipeline/verify_occurrences.py`, `pipeline/refresh_meta.py`, `pipeline/build.py` — **LN**, entirely

All five operate purely on the generic fragment markup
(`<span data-root>`, `<p class="v">`) and the generic `threads.json` /
`units.json` schema. `verify_occurrences.py`'s perceptual-color-collision
check ([verify_occurrences.py:42-58](pipeline/verify_occurrences.py#L42-L58))
is pure color math. None reference Greek, Hebrew, or Matthew by name except
in comments/docstrings. `build.py`'s orchestration order
([build.py:29-31](pipeline/build.py#L29-L31)) is a book-agnostic recipe.

### 1.9 One-shot / retired tools — **MT**, explicitly not part of the ongoing pipeline

- `pipeline/extract_legends.py` — one-shot backfill, superseded ("units.json
  is hand-maintained now," [build.py:20-21](pipeline/build.py#L20-L21)).
- `pipeline/wording_skies.py` — one-shot content rewrite (`ouranos`→"sky"),
  own docstring says "Run once" ([wording_skies.py:6](pipeline/wording_skies.py#L6)).
- `pipeline/splice_synoptic.py` — one-shot retrofit, own docstring: "not part
  of the ongoing pipeline" ([splice_synoptic.py:6](pipeline/splice_synoptic.py#L6)).
- `pipeline/legend-overrides.json` — one Matthew-specific override entry
  ([legend-overrides.json:1-5](pipeline/legend-overrides.json#L1-L5)), tied to
  the retired `extract_legends.py`.

None of these four should be copied into a Hebrew project at all — they're
historical debt-paydown tools, not reusable machinery. `git log` confirms
each ran once and was never touched again after its introducing commit
(consistent with the churn table in §3).

### 1.10 Data files

| File | Schema | Content |
|---|---|---|
| `data/threads.json` | **LN** — `id/root/translit/gloss/color/status/tagged/opens/payoffs/note` ([data/threads.json](data/threads.json), sampled at thread `light`) | **MT** — 58 threads, entirely Matthew-content policy |
| `data/units.json` | **LN** for the per-unit row (`n/slug/passage/title/movement/built/roots`); **MT-genre** for the top-level `movements`/`discourses` arrays | `unit_count: 28`, `book: "Matthew"`, 3 movements, 5 discourses — all Matthew-specific literary-critical content. The *concept* of "discourse" (Bible Project's 5-discourse framework for Matthew) is Matthew-specific; Joshua/Judges would either leave `discourses: []` empty (the UI degrades gracefully — `app/main.js`'s `discourseOf()` at [main.js:110-112](app/main.js#L110-L112) just returns `null` for every unit) or invent an analogous grouping (Judges' judge-cycles, say) under the same field name |
| `data/occurrences.json` | **LN**, pure generated fact | N/A (never hand-edit, [scan_occurrences.py:10](pipeline/scan_occurrences.py#L10)) |

Confirmed no hardcoded `28` or `"Matthew"` literal anywhere in the Python
pipeline (only in comments/docstrings and generated data,
`grep -rn "\b28\b" pipeline/` returns only comment text and unrelated verse
numbers in `retrofit-tags.json`). `data/units.json`'s `unit_count: 28` is
read dynamically by `app/main.js` (`markCurrent`, [main.js:377](app/main.js#L377));
nothing assumes 28 anywhere in code. This validates `PLAN.md`'s own stated
goal, "**Book-agnostic where cheap:** a Jonah project is planned on this
structure; scripts avoid hardcoding 'Matthew' / 28 where it costs nothing"
([PLAN.md:102-103](PLAN.md#L102-L103)) — the goal was met for the orchestration
layer.

### 1.11 The app layer (`app/*.js`, `css/styles.css`)

- `app/main.js`, `app/threads.js` (read in full): **LN**, essentially
  wholesale portable. The only hardcoded literals are cosmetic strings
  (`"Matthew Study"` in `<title>`, [main.js:1,252,294](app/main.js#L294);
  `localStorage` key prefixes `matthew:`/`matthew.search.q`,
  [main.js:25](app/main.js#L25), [search.js:6](app/search.js#L6)) — a
  find-and-replace, not a redesign. `roman()`'s hardcoded `["", "I", "II",
  "III", "IV", "V"]` array ([main.js:483](app/main.js#L483)) caps at 5 with a
  graceful `|| String(n)` fallback beyond that — a scale limit, not a
  Hebrew-specific one.
- `css/styles.css`: **LN** mechanism, Latin-only fonts (`EB Garamond`,
  `Cormorant Garamond`, [css/styles.css:24-25](css/styles.css#L24-L25)), and
  **zero RTL/bidi support anywhere** (`grep -rn "rtl\|direction\|unicode-bidi"`
  across the repo finds no `dir=`, no `unicode-bidi`, and the only
  `flex-direction` hits are unrelated layout code). This is **not a gap**
  given the project's own already-locked policy: "**Transliteration only** —
  no native Greek or Hebrew script in the final rendered unit.html page"
  ([CLAUDE.md:113](CLAUDE.md#L113)), reaffirmed in the research-project
  instructions ([instructions.md:96-97](instructions.md#L96-L97)) and the
  style-reference checklist ([matthew_study_style_reference.md:347](matthew_study_style_reference.md#L347)).
  The Hebrew project inherits an already-Hebrew-inclusive form of this rule —
  `instructions.md` line 4-5 already says "Lane has only a little Greek
  **and Hebrew**... never print native script anywhere." If that policy is
  ever relaxed for the Hebrew project specifically, the missing RTL CSS and
  font coverage becomes a real, silent (mojibake/backwards-word-order, no
  error) problem — flag it as a known gap contingent on that policy choice,
  not an active bug today.

---

## 2. The research-project ↔ repo interface, as one contract

### 2.1 Repo → research project (what the Claude.ai project reads)

| Artifact | Generated by | Trigger | Consumed how |
|---|---|---|---|
| `threads-digest.md` | `pipeline/threads_digest.py` from `data/threads.json` | Run as part of `build.py` ([build.py:29](pipeline/build.py#L29)) whenever `threads.json` changes | Hand-authored instruction: "**the source of truth**" for which roots are tracked ([threads_digest.py:33-39](pipeline/threads_digest.py#L33-L39)); the research project checks new tags against this table before writing an artifact ([instructions.md:60](instructions.md#L60)) |
| `translation-choices.md` | Hand-maintained (not generated) | Updated "in the same turn" as any wording change, per standing workflow rule ([CLAUDE.md:28-33](CLAUDE.md#L28-L33), commit `aed087e`) | Research project checks it before rendering a Greek word, matches prior decisions or flags a deliberate deviation ([translation-choices.md:12-19](translation-choices.md#L12-L19); the CLAUDE.md paste-block, [CLAUDE.md:139-146](CLAUDE.md#L139-L146)) |
| `matthew_study_style_reference.md` | Hand-maintained | Ad hoc, rewritten to "v2" for Phase 9 (commit `504de35`/`497059b`) | The artifact spec itself — fragment shape, unit-meta schema, conventions checklist, literary unit map |
| `instructions.md` | Hand-maintained | Ad hoc | The research project's own operating instructions (persona, sourcing, three-pass workflow, artifact contract) |
| `MatthewSBLGNT.txt` (repo root) | Copied from the research project's own `Matt.txt` | **Manual, unautomated** — instructions.md states the two files must be kept in sync by hand ([instructions.md:21-24](instructions.md#L21-L24): "identical text lives in the site repo as `MatthewSBLGNT.txt`... keep the two in sync") | Ground truth for `pipeline/audit_thread_coverage.py` |

### 2.2 Research project → repo (what gets ported in)

**File.** `source-artifacts/matthew_NN_translation.html` — either a full
standalone doc (pre-Phase-9 shape) or, since Unit 9, a pure fragment
(v2 contract).

**Required shape**, enforced by `pipeline/unit_meta.py.validate()`
([unit_meta.py:103-194](pipeline/unit_meta.py#L103-L194)):

- One `<article class="unit" data-unit="N">`, nothing else at the top level.
- Opened by `<script type="application/json" id="unit-meta">` carrying:
  - `unit` (int, required), `slug`, `passage` (required), `title` (required),
    `movement` (optional int), `descriptor` (optional).
  - `roots: [{root, translit, gloss}]` (required) — **no `color` field**
    (rejected if present, [unit_meta.py:119-121](pipeline/unit_meta.py#L119-L121))
    and **no `kind`/`members`** (rejected — a taxonomy that was tried and
    reverted, see §3) — [unit_meta.py:124-126](pipeline/unit_meta.py#L124-L126).
    `root` must match `[a-z0-9-]+` ([unit_meta.py:122-123](pipeline/unit_meta.py#L122-L123)).
  - `threads: {opens, payoffs, candidates, retro}` (required):
    - `opens`/`payoffs`: `{id, ref, note?}` — `id` must already exist in
      `data/threads.json` or validation fails
      ([unit_meta.py:151-159](pipeline/unit_meta.py#L151-L159)).
    - `candidates`: `{root, why, stems?, exclude?}` — proposals only, **never
      auto-promoted** ([unit_meta.py:139-149](pipeline/unit_meta.py#L139-L149)).
    - `retro`: `{unit, verse, text, root, why, nth?, op?}` — fixes for
      *earlier* units; rejected if it targets the unit's own slug
      ([unit_meta.py:170-179](pipeline/unit_meta.py#L170-L179)); the target
      root/thread must resolve to a real color or validation fails
      ([unit_meta.py:184-193](pipeline/unit_meta.py#L184-L193)).

**Markup conventions** the porter/extractor parses out of the body (not
schema-validated, but load-bearing):

- `<span class="r" data-root="X">…</span>` (counted) / `class="rl"`
  (not counted in the legend, still counted by `scan_occurrences.py` inside
  a `.v` block per commit `394db71` — a documented gotcha, §3).
- `<p class="v"><span class="n">V</span>…</p>` with `.gloss`/`.compare` as
  **following siblings**, never nested (style-reference rule; violation
  detected by `port_artifact.py`'s structure check,
  [port_artifact.py:276-287](pipeline/port_artifact.py#L276-L287)).
- `<h3 class="pericope">Title <span>· C:V</span></h3>` section headings
  ([port_artifact.py:252-264](pipeline/port_artifact.py#L252-L264)).
- `<aside class="synoptic" data-anchor="C:V">` for cross-Gospel comparison
  (Matthew-genre-specific, §1.6).
- Endnotes as bare `nK` ids — the pipeline prefixes them per unit
  (`prefix_endnotes`, [extract_units.py:328-332](pipeline/extract_units.py#L328-L332)).

**Command.** `python pipeline/port_artifact.py NN` (or `--dry`, or `--src X`
to dry-run a practice file, [port_artifact.py:1-33](pipeline/port_artifact.py#L1-L33)).

**What it writes (real run, not `--dry`):**
1. `units/unit-NN.html` — the reduced/validated fragment.
2. `data/units.json` — merges the unit's row, assigns local hues to any
   root not already a tracked thread, collision-checked against both local
   and thread colors ([port_artifact.py:126-169](pipeline/port_artifact.py#L126-L169)).
3. `pipeline/retro-tags.json` — dry-checks each `threads.retro` entry against
   its target fragment, merges only the ones that apply
   ([port_artifact.py:371-407](pipeline/port_artifact.py#L371-L407)).
4. Re-runs `apply_retrofit.py → scan_occurrences.py → verify_occurrences.py`
   ([port_artifact.py:415-425](pipeline/port_artifact.py#L415-L425)).
5. `pipeline/out/thread-delta-NN.md` — **the one output meant for a human**,
   never auto-applied: ready-to-paste `threads.json` payoff entries,
   new-thread stem previews with book-wide match counts, fragment-structure
   warnings, and any tracked-thread Greek occurrence the artifact left
   untagged ([port_artifact.py:174-355](pipeline/port_artifact.py#L174-L355)).

**What it explicitly never writes:** `data/threads.json`. Every code path
says so in a comment or printed message — `port_artifact.py:26` ("threads.json
is never written here; it is policy Lane owns"),
`thread_delta`'s header line ([port_artifact.py:180](pipeline/port_artifact.py#L180):
"Apply by hand to `data/threads.json` if you accept it. The porter does not
touch threads.json."). This is the single sharpest, most consistently
enforced boundary in the whole system — an editorial-authority firewall, not
a technical one.

### 2.3 The full round trip

```
Claude.ai research project                          this repo
──────────────────────────                          ─────────
reads threads-digest.md ◄─────────────────────────── pipeline/threads_digest.py
reads translation-choices.md ◄──────────────────────  (hand-maintained)
reads instructions.md ◄─────────────────────────────  (hand-maintained, paste-synced from CLAUDE.md)
reads matthew_study_style_reference.md ◄────────────  (hand-maintained)
   │
   │ writes matthew_NN_translation.html
   ▼
source-artifacts/matthew_NN_translation.html
   │  python pipeline/port_artifact.py NN
   ▼
units/unit-NN.html  +  data/units.json  +  pipeline/retro-tags.json
   │
   ▼
pipeline/out/thread-delta-NN.md ──── Lane reviews ──► hand-edits data/threads.json
                                                       hand-edits translation-choices.md
                                                       (loop closes back to §2.1)
```

Two steps in this loop are **manual and unenforced**: the `Matt.txt` ↔
`MatthewSBLGNT.txt` sync (§2.1), and the `threads-digest.md` /
`translation-choices.md` paste-into-the-Claude.ai-project step (Lane
performs this by hand; nothing detects drift if it's skipped). For a Hebrew
project, both sync points need the same manual discipline — there is no
technical reason they couldn't be automated (a scheduled export, a shared
drive), but nothing in the current architecture does so, and CLAUDE.md's own
"Working notes" section treats this as intentional low-ceremony process
rather than a gap to close.

---

## 3. Git archaeology: what broke, and which conventions exist because of it

72 commits total, 2026-09-07 to 2026-09-12. Churn leaders (excluding logs/
session files, which are process overhead, not code):
`app/main.js` (27), `css/styles.css` (23), `units/unit-01.html` (20),
`data/occurrences.json` (20), `data/threads.json` (17), `app/search.js` (17).
Unit 1 is the single most-touched fragment because it predates every later
convention (§3.1) — a useful signal that early, un-convention'd content is
disproportionately expensive to reconcile later, directly relevant to how a
Hebrew project should treat its own "unit 1."

### 3.1 Silent color-resolution failure → the entire two-tier engine + hard-verify rule

The project's own kickoff inspection (`PLAN.md:30-37`) found: Unit 2 used
root classes with no color defined (renders gray, no error); Unit 7 defined
a palette matching Units 2-3's roots but its actual text used a *completely
different* root set, so **every colored word in Unit 7 silently rendered
uncolored**. This one finding is the direct cause of:

- The two-tier runtime color resolution system (global thread vs. per-unit
  palette) instead of baked-in CSS (`PLAN.md:55-71`).
- The rule "a `data-root` that resolves to no colour is a hard verify
  failure" (`PLAN.md:70-71`), implemented in
  [verify_occurrences.py:74-84](pipeline/verify_occurrences.py#L74-L84).
- The "generate + verify" discipline itself — "every generator ships a
  sibling `verify_*.py` that re-derives the result independently"
  (`PLAN.md:84-89`, `CLAUDE.md`'s "Locked design decisions").

**Lesson for the Hebrew project:** build the verify step *before* or
*alongside* the first generator, not after — this bug shipped silently
across 7 files before anyone looked for it.

### 3.2 `extract_units.py` re-run in `build.py` silently dropped hand edits (commit `9713a27`, 2026-09-10)

> "Running it as build.py's first step regenerated the fragments from
> source and silently dropped all of that (tested: 8 units diverged)."
> — [commit 9713a27](pipeline/build.py)

`extract_units.py` was the Phase-1 batch normalizer. By the time this bug
was found, every unit had accumulated direct hand edits (pericope headings,
synoptic boxes, chiasm cuts) that existed *only* in the committed fragment,
nowhere in `source-artifacts/`. Re-running the "generate `units/*.html` from
`source-artifacts/*.html`" step blew all of it away with no warning. This is
now a load-bearing, explicitly documented rule:

> "units/\*.html are the source of truth here — this script never
> regenerates them from source-artifacts/... Adding a NEW unit is
> `port_artifact.py NN`, not this." — [build.py:13-18](pipeline/build.py#L13-L18)

**Lesson:** once a fragment accepts hand edits after generation, the
generator that produced it must never run again on that fragment. This is a
structural risk for a Hebrew project too, if the same "extract once, then
hand-edit forever" workflow is reused — the fix (retire the generator to a
library-only role, document it loudly in the orchestrator) transfers
directly and should be designed in from the start rather than discovered.

### 3.3 Greek final-sigma fold (commit `6453a4b`, 2026-09-10)

Already covered in depth at §1.4. Concrete, mechanical bug: `ς` (final
sigma) and `σ` (medial) are different codepoints; a stem written with the
medial form didn't match words ending in the stem. Fixed by folding `ς→σ`
in `strip_accents` ([audit_thread_coverage.py:55-60](pipeline/audit_thread_coverage.py#L55-L60)).
**This is the single most directly transferable lesson in the whole
codebase** — Hebrew has five letters with distinct final forms
(ך/כ ם/מ ן/נ ף/פ ץ/צ) and the exact same class of bug will recur unless the
fold is added up front.

### 3.4 Chiasm over-fitting (commit `e9105a5`, 2026-09-09)

Not a code bug — a scholarly-judgment failure mode. Eight previously-authored
chiastic/ring structures across seven units (Magi ring, Exile & Return
triptych, "Mackie's symmetry," Beatitudes ring, devotion-panel ring, a unit's
own-shape ring, paralytic ring-inside-ring, discourse-shape + ladder rings)
were cut as "over-reaching" — Lane's judgment call, recorded in the commit
message. This produced a standing instruction that exists purely because of
this repeated failure:

> "chiasms (real and verifiable, be tough on how you weight these, they're
> easy to make up. Avoid seeing patterns where there are none)"
> — [instructions.md:13](instructions.md#L13)

**Lesson for a Hebrew project:** narrative books (Joshua, Judges) invite a
*different* over-fitting risk than Matthew's discourses — type-scenes and
cyclical-structure pattern-matching (the judge-cycle refrain in Judges is
real and textually marked, but secondary "chiasms" imposed on narrative
episodes are exactly the kind of thing Matthew's experience warns against).
Carry the caution, expect the specific failure mode to look different.

### 3.5 Root/motif taxonomy: built and reverted the same day (commits `8d096c9` → `98b721a`, both 2026-09-07)

A two-tier taxonomy (`kind: root` for a single lexeme vs. `kind: motif` for
a bundle of kindred-but-distinct words, with different underline styles, a
third legend section, and `members` arrays) was designed, fully implemented
across `threads.json`, `units.json`, every fragment meta block, `threads.js`,
and the style reference — then reverted in its entirety hours later. The
revert commit's reasoning: a bundled word-family is "just a root: one
data-root slug, one colour, the family spelled out in its translit string"
([commit 98b721a](data/threads.json)) — added complexity the data didn't
need. `unit_meta.py` still actively rejects the old shape today
([unit_meta.py:124-126](pipeline/unit_meta.py#L124-L126): "'kind'/'members'
are gone — every tracked item is a plain root now").

**Lesson:** this project has already run the experiment of "richer taxonomy
tier" and rejected it in favor of a flatter model with information pushed
into a string field (`translit: "gennaō · genesis"` for a compound root,
per `data/units.json`'s `beget` entry). A Hebrew project — which will have
its *own* temptation toward a richer taxonomy (root vs. binyan vs. semantic
field) — should read this revert before reaching for the same complexity.

### 3.6 Synoptic-aside nesting bug, 8 instances (commit `67b2712`, 2026-09-10)

The 2026-09-09 synoptic-parallel splice (`splice_synoptic.py`) inserted
`<aside class="synoptic">` boxes that ended up nested inside an unclosed
`.gloss` span or a `.compare` div in 8 places across 6 units, so
`spotlight.js` collapsed them into a generic note marker instead of their
own distinct chip. This produced both a one-time fix and a permanent
structural check:

> "the aside must be a sibling of the verse, never spliced inside an
> unclosed `<span class="gloss">` — otherwise spotlight.js rolls it into a
> plain note (\*) instead of giving it its own ✧ chip."
> — [port_artifact.py:276-282](pipeline/port_artifact.py#L276-L282)

**Lesson:** any splice/insert tool that doesn't track open/close depth in
the surrounding markup will produce this exact silent-degradation class of
bug. Directly relevant if a Hebrew project reuses a similar
insert-a-cross-reference-box script.

### 3.7 Chapter/verse alignment guessed, then made authoritative (commit `d6185f8`, 2026-09-10)

Covered at §1.4. The audit originally inferred chapter numbers from a
"verse number dropped → bump the chapter" heuristic; replaced with deriving
the canonical `(chapter, verse)` sequence directly from the source Greek
text file, "anything that won't line up is reported, never guessed"
([audit_thread_coverage.py:161-167](pipeline/audit_thread_coverage.py#L161-L167)).
This is a principle, not code, and needs conscious re-application — Joshua
and Judges both have manuscript/versification irregularities (e.g., some
traditions number Judges differently around chapter boundaries) that make
"derive from the source text, never guess" exactly as necessary there as it
was for Matthew's Lord's-Prayer set-piece verse-skip case.

### 3.8 CLAUDE.md itself had to be corrected against stale info (commit `daf5710`, 2026-09-10)

Not a code bug — a documentation-drift bug. `CLAUDE.md`'s "Source texts"
section pointed at an external OneDrive path that no longer held anything
the project needed; fixed to state plainly that `MatthewSBLGNT.txt` in the
repo root is sufficient and "nothing outside the Matthew folder is needed."
**Lesson:** the standing-instructions file is not self-verifying; it drifted
from reality once and was caught by inspection, not by any check. Worth a
periodic manual sanity pass on the Hebrew project's own CLAUDE.md once it
exists.

### 3.9 `.rl` mislabeling (commit `394db71`, 2026-09-09)

A cosmetic-seeming class distinction (`class="r"` = counted, `class="rl"` =
not counted) turned out to be misleading: `scan_occurrences.py` counts
*every* `data-root` inside a `<p class="v">` block regardless of class, so
using `rl` inside verse text didn't actually suppress the count — it just
mislabeled intent. Fixed by downgrading 27 spans from `rl`→`r` and clarifying
that `.rl` only means "not counted" outside verse blocks (legend rows,
glosses, labels). A small thing, but it shows the counting mechanism's
actual behavior needs to be read from `scan_occurrences.py`
([scan_occurrences.py:47-49](pipeline/scan_occurrences.py#L47-L49): both
`ROOTSPAN.findall(seg)` calls count `data-root` regardless of `r`/`rl`),
not inferred from the class names' apparent meaning.

---

## 4. What to keep unchanged — the design defended

**The generate/verify pairing.** Every script that writes into `/data` has a
sibling that independently re-derives the same fact by a different method
and refuses to proceed on mismatch (`scan_occurrences.py` /
`verify_occurrences.py`, which deliberately does *not* import the scanner
and recounts with "a line-oriented tokeniser so a bug in one approach
doesn't hide in both," [verify_occurrences.py:2-3](pipeline/verify_occurrences.py#L2-L3)).
This is cheap (a few dozen lines per pair) and has already caught the exact
class of silent failure (§3.1) that motivated it in the first place. Keep
this exactly as-is for a Hebrew project; it costs nothing per unit and its
value compounds with every unit added.

**Two-tier, runtime-resolved color.** Baking color into per-unit CSS was
the original design and it failed silently and repeatedly (§3.1). Resolving
`data-root` → color at load time from two JSON files, with a hard-fail if
nothing resolves, converts a class of bug that used to be invisible (wrong
color, or no color, with no signal) into a build-time hard stop. This is
architecturally the single best decision in the project and should not be
touched.

**`threads.json` as owned policy, `occurrences.json` as pure fact, and the
firewall between them.** The porter can propose (`candidates`, `retro`,
the thread-delta report) but can never write `data/threads.json`
(§2.2) — every promotion of a root to a cross-unit thread, every color, every
editorial note, passes through a human decision, recorded as a diff Lane
applies by hand. This protects the one thing in the system that is
genuinely subjective (which recurring word matters enough to track,
book-wide) from being silently automated. A Hebrew project will have the
exact same category of subjective call (which Hebrew roots deserve
thread status) and should keep the same firewall.

**Deriving ground truth from the actual source text, not from the English
translation or the fragment's own claims.** `audit_thread_coverage.py`
scans the real Hebrew/Greek text and treats it as authoritative over
whatever the artifact happened to tag — this is what caught the `sin`
thread missing `hamartōlos`/"sinner" at 9:10-13 (commit `d95b5c4`), among
many other gaps. An audit that trusted the English rendering, or trusted
that the research project tagged everything it meant to, would have missed
these. This principle is the project's actual quality floor and should be
non-negotiable in the Hebrew port, even though the specific regex/format
needs updating (§1.4).

**No build step, relative paths, plain ES modules.** Chosen for a specific,
still-true constraint (GitHub Pages serves from a subpath,
`new URL('../data/x.json', import.meta.url)` style resolution,
`CLAUDE.md`'s "Locked design decisions"). What's committed is what runs —
there's no compiled-output-vs-source drift possible, no build cache to
distrust. For a project this size (28 units, a handful of JS modules), this
is a correct proportionality call, not a missing feature.

**Idempotent, self-checking mutation ops.** Every `apply_retrofit.py`
operation reports `ok`/ no-op if already applied
([apply_retrofit.py:63-64,82-83,95-96,etc.](pipeline/apply_retrofit.py#L63-L64)),
which is why `build.py` can safely re-run the entire chain from a clean
checkout at any time (verified explicitly in commit `9713a27`: "Verified
idempotent — running it twice from clean touches nothing"). This operational
property is worth the small amount of extra code in each `apply_*` function
and should be a hard requirement for any new Hebrew-specific mutation op.

**The retrofit-tags.json / retro-tags.json split.** Hand-authored fixes and
porter-generated fixes-for-earlier-units live in separate files that both
feed `apply_retrofit.py`
([apply_retrofit.py:174-181](pipeline/apply_retrofit.py#L174-L181)),
specifically so an automated merge never has to touch, reformat, or risk
corrupting the hand-authored one. Small mechanism, real protection against
tooling clobbering judgment calls; keep it.

**The porter's dry-run and `--src` modes.** `port_artifact.py --dry` and
`--src PATH` let a new unit (or, for a Hebrew project, a first practice
artifact) be validated and previewed — including a full thread-delta and
coverage report — with the write path fully disabled
([port_artifact.py:430-478](pipeline/port_artifact.py#L430-L478)). This is
exactly the right amount of safety for a human-in-the-loop pipeline that
otherwise touches committed data files, and costs nothing to keep.

---

## 5. Net assessment for the port

Roughly by line count, the pipeline is **~85% directly reusable** (`unit_meta.py`,
`apply_retrofit.py`, `port_artifact.py`'s mechanism, `scan_occurrences.py`,
`verify_occurrences.py`, `refresh_meta.py`, `build.py`, `threads_digest.py`,
and the entire `/app` layer), **~10% needs a new sibling module** (a
`hebrew.py` transliterator with real vowel-pointing handling, replacing
`greek.py`'s role — the one piece of genuinely new engineering work), and
**~5% needs small, well-guarded parameter changes** (the hardcoded `"Matt"`
prefix and filename in `audit_thread_coverage.py`, which already fail loud
rather than silent). The four one-shot historical tools (§1.9) and the two
Matthew-content data files (`threads.json`, `units.json`'s content) don't
transfer and aren't meant to. The single sharpest latent risk worth fixing
*before* first use rather than after discovery is the Hebrew final-letter-form
fold in stem matching (§1.4, §3.3) — a bug this project already paid to find
and fix once for Greek.
