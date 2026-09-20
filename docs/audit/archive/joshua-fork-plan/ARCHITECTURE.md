> **ARCHIVED — historical, superseded by the Joshua repo.**
> Written 2026-09-12 as the plan for forking Matthew into a Hebrew book, before
> Joshua existed. Joshua was then built and diverged from this plan in ways that
> matter: root identity moved from substring stems to lexicon-id sets (`roots.json`
> + `data-w`), `candidates[].stems` is gone, the `greek-title` masthead and the
> `<p id="n1">` endnote shape were both replaced. **Read this as a record of what
> was intended, never as instructions.** The live documents are in the Joshua repo
> (`../Joshua/`), and the current cross-project plan is `platform-design-review.md`.

# Architecture — the Joshua fork

Derived from `docs/audit/port-analysis.md`. That document is the evidence; this
one is the decision.

**The approach is fork-and-modify, not generalize.** Copy the Matthew repo to a
new repo, delete what doesn't apply, change what needs changing. Do *not* extract
a shared framework, a plugin system, or a `book_config.json` that both projects
read. Two books is not enough evidence to know what varies; the audit found that
the orchestration layer is already ~85% language-neutral by accident of good
design, and the 15% that isn't is concentrated in two files. A framework would
add a coupling that makes every Matthew change a Joshua risk, in exchange for
avoiding a one-time copy.

Judges, later, forks from Joshua the same way. If the *third* fork reveals the
same three parameters changing every time, that is when to consider extracting
them — with three data points instead of one.

---

## 1. The fork boundary

### 1.1 Copy verbatim — do not touch

These files have no Greek, Hebrew, or Matthew assumption anywhere in their
mechanism. Copy them and move on.

| File | Why it's safe |
|---|---|
| `pipeline/unit_meta.py` | Pure JSON schema parse/validate/generate. The most portable file in the repo. (One change in §3.) |
| `pipeline/apply_retrofit.py` | Generic `<span data-root>` patching. Every op is language-blind and idempotent. |
| `pipeline/scan_occurrences.py` | Counts `data-root` inside `.v` blocks. |
| `pipeline/verify_occurrences.py` | Independent re-derivation + perceptual colour-collision maths. (Two additions in §3.) |
| `pipeline/refresh_meta.py` | Re-injects meta blocks from the data files. |
| `pipeline/threads_digest.py` | `threads.json` → `threads-digest.md`. |
| `pipeline/build.py` | Orchestration order. Book-agnostic recipe. |
| `app/threads.js` | Two-tier colour resolution, popover, concordance. (One change in §3.) |
| `app/store.js`, `app/search.js` | localStorage + search. Key prefix rename only. |
| `css/styles.css` | Latin-only fonts are correct given the transliteration-only policy. |

### 1.2 Copy and rename strings only

| File | Change |
|---|---|
| `app/main.js` | `"Matthew Study"` title strings; `localStorage` prefix `matthew:` → `joshua:`. Nothing structural. `roman()`'s 5-entry array is a scale cap with a `\|\| String(n)` fallback, not a Matthew assumption. |
| `index.html` | Title, masthead. |

### 1.3 Copy and modify

| File | What changes | Detail |
|---|---|---|
| `pipeline/audit_thread_coverage.py` | Book prefix, source filename, final-form fold | §2 |
| `pipeline/port_artifact.py` | Drop the `aside.synoptic` check, add the legend and endnote checks | §3 |
| `pipeline/extract_units.py` | Strip to the functions `port_artifact.py` actually imports | §4 |
| `pipeline/thread-stems.json` | New file, Hebrew stems, same schema | data only |

### 1.4 Do not copy

| File | Why |
|---|---|
| `pipeline/greek.py` | Replaced by `hebrew.py` — see `HEBREW-TRANSLITERATION.md`. It is not a parameterization; it is a sibling. |
| `pipeline/extract_legends.py` | One-shot backfill, superseded. |
| `pipeline/wording_skies.py` | One-shot content rewrite. |
| `pipeline/splice_synoptic.py` | One-shot retrofit, and the genre doesn't transfer. |
| `pipeline/legend-overrides.json` | Tied to the retired `extract_legends.py`. |
| `pipeline/retrofit-tags.json`, `pipeline/retro-tags.json` | Matthew edit records. Start both empty (`{}`). |
| `data/threads.json`, `data/units.json` (content) | Matthew policy. Keep the *schema*, empty the content. |
| `data/occurrences.json` | Generated. Delete; `build.py` recreates it. |
| `units/*.html`, `source-artifacts/*` | Matthew prose. |
| `MatthewSBLGNT.txt` | Replaced by the Hebrew source text. |
| `matthew_study_style_reference.md`, `translation-choices.md`, `threads-digest.md` | Rewrite from scratch for Joshua. The Matthew versions are worth reading as models and worth zero as starting text. |

**Delete `normalize_verses`, `normalize_blocks`, and `fix_greek_title` from the
forked `extract_units.py`** — they exist to reconcile Matthew's pre-convention
Unit-1 markup (`div.v`, `div.gloss`, `div.greek-title`) with the convention that
came later. Joshua's unit 1 will be authored under the convention. Keeping them
is dead code that will be mistaken for a contract.

---

## 2. Parameterization targets

Exactly three things are worth parameterizing, and all three are already
half-parameterized.

**(a) The book prefix in the source-text parser.** Today:

```python
GREEK = os.path.join(ROOT, "MatthewSBLGNT.txt")
m = re.match(r"Matt (\d+):(\d+)\t(.*)", line.rstrip("\n"))
```

`data/units.json` already carries `"book": "Matthew"` and the Python side never
reads it. Read it. Add a sibling `source_text` and `verse_prefix` key:

```json
{ "book": "Joshua", "source_text": "JoshuaBHS.txt", "verse_prefix": "Josh" }
```

This is worth doing *now*, not at the Judges fork, because doing it once at
Joshua is a five-line change and doing it at Judges means editing a file that
has diverged.

**(b) `localStorage` namespace.** One constant, already isolated to two files.

**(c) Nothing else.** Resist the pull. The `unit_count`, the movements, the
discourses, the colour well, the unit-slug format — all already generic, all
already read from data.

---

## 3. Changes to otherwise-portable files

**`unit_meta.py` — add an unknown-key check.** The audit's §6.2 items 1 and 5:
`descriptor` and `discourse` were authored in every v2 artifact, accepted by the
validator, and silently discarded; `threads.opens` was documented and never used.
Add to `validate()`:

```python
KNOWN = {"unit", "slug", "passage", "title", "movement", "roots", "threads"}
for k in meta:
    if k not in KNOWN:
        errs.append(f"unknown key '{k}' — the pipeline will drop it silently")
```

Then decide `descriptor`/`discourse`/`opens` deliberately: either wire them
through to `units.json` and the rendered page, or drop them from the spec. Do not
ship them as accepted-and-ignored.

**`port_artifact.py` — replace the synoptic check with a legend check.** Delete
the `aside.synoptic` block ([port_artifact.py:266-287]) — the genre doesn't exist
for Joshua, and leaving a check tuned to markup nobody writes is how a
repurposed component inherits a nesting rule it doesn't match (audit §3.6).
Replace with the check that would have caught the live unit-11 bug:

```python
if not re.search(r'<section class="block legend"', html):
    issues.append("no `<section class=\"block legend\">` — the site fills a "
                  "legend but never creates one; without it the unit ships "
                  "with no colour key")
```

**`verify_occurrences.py` — two new assertions.**

1. *Endnote integrity* (audit §6.2 item 6): per fragment, `{id="n…"}` must equal
   `{href="#n…"}`. The only stated contract rule with no check.
2. *Script leakage* (audit §6.2 item 7): no Hebrew codepoints (U+0590–05FF,
   U+FB1D–FB4F) anywhere in a built fragment, **attribute values included** —
   Matthew ships native Greek in a `logeion.uchicago.edu/προσκυνέω` href today
   because the strip only covers element content.

**`app/threads.js` — leave `rebuildLegend` as-is.** It is correct to fail closed;
the fix belongs in the porter check above, so the problem is caught before the
fragment is committed rather than papered over at render time.

**`build.py` — add the component-whitelist check** as a sixth advisory step
(audit §7 item 4): classes used in `units/*.html` that `css/styles.css` never
mentions. Ten lines, and it catches both unknown components and — inverted —
missing required ones.

---

## 4. The one genuinely new module

`pipeline/hebrew.py`. A sibling to `greek.py`, not a generalization of it: same
architectural role (one small pure function, deterministic, `__main__` block with
worked examples, every span it touches logged for review), completely different
internals. Design is in `HEBREW-TRANSLITERATION.md`.

Two consumers, both already routed correctly:

- `extract_units._translit_token` already dispatches Hebrew → `_rom_hebrew`
  ([extract_units.py:220-231]). Repoint it at `hebrew.transliterate` and delete
  `_rom_hebrew`, whose 22-consonant, vowel-dropping table is a stopgap for
  loanwords that would become the *primary* path in a Hebrew-primary book.
- `audit_thread_coverage.py` imports `greek.transliterate` for display in reports
  ([audit_thread_coverage.py:36-40]). Repoint.

**Do not leave `greek.py` in the forked repo as a fallback.** Its detection gate
(`"Ͱ" <= c <= "Ͽ"`) means Hebrew passes through completely unchanged, with no
exception and no log line — verified: `greek.transliterate("מֶלֶךְ")` returns
`"מֶלֶךְ"`. A fallback that silently emits untransliterated Hebrew is worse than
an ImportError.

---

## 5. What the fork does *not* change

Stated explicitly so nobody relitigates it mid-project:

- **Two-tier runtime colour resolution**, with a hard verify failure for any
  `data-root` that resolves to nothing. The best decision in the project.
- **`threads.json` is never written by code.** The porter proposes; the human
  disposes. Hebrew will have the identical subjective call (which roots deserve
  thread status) and needs the identical firewall.
- **Generate + verify, with the verifier not importing the generator.**
- **Ground truth is the source text**, never the English rendering and never the
  artifact's own claims about what it tagged.
- **No build step, relative paths, plain ES modules.**
- **Fragments are the source of truth**; the generator that produced them never
  runs on them again (audit §3.2 — this cost eight diverged units to learn).
- **Transliteration only**, now explicitly covering attribute values, with
  `candidates.stems` as the one documented exception.
- **Desktop and mobile both first-class**; no horizontal page scroll.
