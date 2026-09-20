> **ARCHIVED — historical, superseded by the Joshua repo.**
> Written 2026-09-12 as the plan for forking Matthew into a Hebrew book, before
> Joshua existed. Joshua was then built and diverged from this plan in ways that
> matter: root identity moved from substring stems to lexicon-id sets (`roots.json`
> + `data-w`), `candidates[].stems` is gone, the `greek-title` masthead and the
> `<p id="n1">` endnote shape were both replaced. **Read this as a record of what
> was intended, never as instructions.** The live documents are in the Joshua repo
> (`../Joshua/`), and the current cross-project plan is `platform-design-review.md`.

# Bootstrap — empty repo to first unit live

**Ordered by irreversibility, not by convenience.** Steps near the top are cheap
to do now and expensive to change after units ship; steps near the bottom can be
redone any afternoon. This is deliberately not the order you would naturally work
in — resist reordering it.

The test for "irreversible" is: *if we change this at unit 12, how many already-
shipped units need re-editing?* Anything that touches the prose of every unit is
irreversible. Anything that touches only a script is not.

Two items are marked **⚠ MUST FIX BEFORE FIRST USE**. Both are bugs this project
has already paid to find once, in Greek, and will pay for again in Hebrew unless
fixed up front.

---

## Tier 0 — decisions that rewrite every unit if changed later

Nothing in Tier 1+ starts until these are written down in `translation-choices.md`
and `CLAUDE.md`.

### 0.1 The transliteration scheme

Write `pipeline/hebrew.py` **first**, per `HEBREW-TRANSLITERATION.md`, with its
`__main__` worked examples and a test file asserting them.

Every legend headword, every endnote lemma, every transliterated word in every
verse gloss comes out of this function. Changing `ḥ` to `kh`, or adding vowel
macrons, at unit 12 means re-editing twelve units of hand-authored prose. There
is no script that can do it for you, because the transliterations live inside
sentences.

Decide and record: the consonant table; begadkefat (recommended: **not modeled**);
vowel quantity (recommended: **collapsed**); dagesh forte doubling (recommended:
**yes**, and flagged as the most likely reversal); the sheva rule; the
qamats-qatan override list; and the divine name.

**Do not copy `pipeline/greek.py` into the repo, even as a fallback.** Its
detection gate returns Hebrew unchanged with no exception and no log line —
verified: `greek.transliterate("מֶלֶךְ")` returns `"מֶלֶךְ"`. A silent
pass-through is worse than an ImportError.

### 0.2 Stems or lemmas — the root-matching strategy

`HEBREW-TRANSLITERATION.md` §3.2. This determines the shape of one data file, the
matching half of `audit_thread_coverage.py`, and the `candidates` field in the
research project's contract — which means it determines what every artifact
writes.

The case for lemmas: Hebrew substring stems cannot match forms where the radical
is physically absent. נתן ("give") yields יִתֵּן and תֵּן — **no nun**. לקח yields
יִקַּח. Hollow roots (קום → קָם) and III-he roots (עשה → יַעַשׂ) lose radicals the
same way. A stem list misses these silently, which is exactly the failure the
coverage audit exists to prevent.

If the source text carries OSHB lemma tags, use them. Keep stems only as a
supplement for fixed phrases and deliberately multi-lemma threads.

### 0.3 The wording glossary, started empty

Create `translation-choices.md` with its Log section before unit 1 is drafted.
Seed the entries the book cannot avoid: the divine name, *ḥerem*, *ḥesed*,
*naḥalah*, *goel*, *nefesh*, and the `y'all` convention.

> Matthew started this at unit 10 and paid with a dedicated wording-audit session
> plus a retroactive pass over everything already shipped (`b0f73cc`, `aed087e`,
> `0138548`). The file costs nothing empty.

### 0.4 The colour policy, restated for Hebrew

One Hebrew lexical root per `data-root`; the root and its same-root forms only;
no themes, no formulae, no bundles; fixed repeated phrases are the one exception
and live in `threads.json`.

Write it into `CLAUDE.md` now. Matthew built a richer two-tier taxonomy and
reverted it the same day (`8d096c9` → `98b721a`); Hebrew's version of that
temptation is root vs. binyan vs. semantic field, and it will arrive around unit
3.

### 0.5 The Literary Unit Map

The unit count and the passage boundaries. Every `data-unit` number, every
filename, and every cross-unit thread reference depends on it. Renumbering after
units ship means editing `threads.json` opens/payoffs, every `retro` entry, and
every fragment's meta block.

Get Lane's confirmation on the map, including any place the literary units
disagree with the chapter grid, before unit 1.

---

## Tier 1 — the two must-fix bugs

Both are one-line changes. Both are silent when wrong. Do them before the first
thread is defined, not after the first miss is noticed.

### ⚠ 1.1 The Hebrew final-letter-form fold

`audit_thread_coverage.py`'s `strip_accents` folds Greek final sigma `ς → σ`
(commit `6453a4b`). It has no equivalent for Hebrew's five final forms.
Demonstrated against the live function:

```
stem מלכ  vs  מֶלֶךְ   (melek, "king")   -> NO MATCH
stem מלכ  vs  מְלָכִים (melakim, plural)  -> match
```

**This is worse than the Greek case.** In Greek, final sigma broke the inflected
forms while the citation form matched. In Hebrew the polarity is reversed —
lemmas are cited in the absolute singular, which is exactly where a final-form
letter sits. A `melek` thread in Joshua would report every plural and silently
miss every singular, in a book with a thirty-one-king list in one chapter.

Fix:

```python
_FINALS = str.maketrans("ךםןףץ", "כמנפצ")

def strip_accents(s):
    d = unicodedata.normalize("NFD", s)
    return ("".join(c for c in d if not unicodedata.combining(c))
            .lower().translate(_FINALS))
```

Verified good news: niqqud and cantillation need **no** new code —
`unicodedata.combining()` already returns non-zero across the pointing range
(sheva 10, qamats 18, dagesh 21, cantillation 220).

Test it the moment it is written, against a pointed form of the first root you
intend to track. If you adopt lemma matching (0.2) this still matters — anything
that compares surface forms needs it.

### ⚠ 1.2 Hardcoded book prefix and source filename

`audit_thread_coverage.py` hardcodes both:

```python
GREEK = os.path.join(ROOT, "MatthewSBLGNT.txt")          # line 45
m = re.match(r"Matt (\d+):(\d+)\t(.*)", line.rstrip("\n"))  # line 75
```

Both fail loudly (file-not-found, or "parsed to zero verses — wrong format?"), so
this is low-risk *today*. It matters because **Judges forks from Joshua**, and a
hardcoded literal is how the second fork becomes a copy-paste divergence instead
of a config change.

`data/units.json` already carries a `book` field the Python side never reads.
Read it, and add two siblings:

```json
{ "book": "Joshua", "source_text": "JoshuaWLC.txt", "verse_prefix": "Josh" }
```

Rename the module-level `GREEK` constant while you are in there — a variable
named `GREEK` holding a Hebrew path is how the next reader gets confused.

---

## Tier 2 — checks that must exist before content accumulates

Each of these is cheap now and retroactive-audit-shaped later. Matthew found all
four by inspection after the fact.

**2.1 Write `verify_occurrences.py` before the first generator runs.** Matthew's
silent-colour bug shipped across seven files because the verifier came second.
Include from day one: counts match, every `data-root` resolves to a colour, no
two roots in one unit collide perceptually, `tagged` flags are honest.

**2.2 Add the endnote-integrity assertion.** Per fragment, `{id="n…"}` must equal
`{href="#n…"}`. Matthew's style reference states this rule; nothing anywhere
checks it.

**2.3 Add the script-leakage grep.** No Hebrew codepoints (U+0590–05FF,
U+FB1D–FB4F) anywhere in a built fragment, **attribute values included**. Matthew
ships native Greek in a `logeion.uchicago.edu/προσκυνέω` href today.

**2.4 Add the unknown-key check to `unit_meta.validate()`.** Matthew's research
project authored `descriptor` and `discourse` in every v2 artifact for eleven
units; both were documented, both accepted, both silently discarded, neither
consumed by anything.

---

## Tier 3 — mechanical setup

Now the copying. All of this is trivially reversible.

**3.1 Fork the repo.** Copy Matthew, then delete per `ARCHITECTURE.md` §1.4:
`greek.py`, the four one-shot tools, `legend-overrides.json`, both fix-list JSONs
(recreate as `{}`), `data/occurrences.json`, `units/*`, `source-artifacts/*`,
`MatthewSBLGNT.txt`, and the Matthew content out of `threads.json` /
`units.json`.

**3.2 Strip the forked `extract_units.py`** down to the functions
`port_artifact.py` imports. Delete `normalize_verses`, `normalize_blocks`, and
`fix_greek_title` — they reconcile Matthew's pre-convention Unit-1 markup with a
convention that came later, and Joshua's unit 1 is authored under the convention.
Dead code here will be mistaken for a contract.

**3.3 Repoint the transliteration dispatch.** `extract_units._translit_token` →
`hebrew.transliterate`; delete `_rom_hebrew`, whose consonant-only,
vowel-dropping table is a loanword stopgap that would silently become the primary
path. Repoint `audit_thread_coverage.py`'s import too.

**3.4 Swap the porter's structure checks.** Delete the `aside.synoptic` block;
add the legend-required check (`ARCHITECTURE.md` §3).

**3.5 Rename strings.** `app/main.js` titles, `localStorage` prefix
`matthew:` → `joshua:`, `index.html`.

**3.6 Place the source text.** Pointed Hebrew Joshua, one verse per line,
`Josh C:V<TAB>text`, tracked in the repo root. Record its checksum in
`CLAUDE.md`. Decide ketiv/qere handling now — which form the audit matches, and
whether the artifact ever shows both.

**3.7 Seed the data files.** `data/units.json` with the book metadata, the
movements, and one row per unit from the map (all `built: false`).
`data/threads.json` as `{"threads": []}` — it starts empty and grows by hand.

**3.8 Seed the session-context files.** `session_index.md`,
`improvements_log.md`, `PLAN.md` with the phase list.

**3.9 Verify the empty pipeline runs.** `python pipeline/build.py` on zero units
should complete cleanly. If it doesn't, fix it now rather than debugging it
alongside real content.

---

## Tier 4 — the research-project contract

**4.1 Write `joshua_study_style_reference.md`.** Sections mirroring Matthew's:
colour policy (§1), fragment shape and meta schema (§2), component snippets (§3),
the pre-save checklist (§4), the Literary Unit Map (§7). Write it fresh — the
Matthew version is worth reading as a model and worth zero as starting text.

**4.2 Paste `PROJECT-INSTRUCTIONS.md` into the Claude.ai project**, TODOs
resolved. Keep this repo's copy as the single authored version and always paste
*from* it.

**4.3 Place the source text in the research project too**, byte-identical to the
repo's. Confirm the checksum matches.

**4.4 Generate and paste `threads-digest.md`.** It will be empty. Paste it
anyway, so the loop is exercised once before it matters.

---

## Tier 5 — first unit

**5.1 Draft unit 1 through all three passes.** Expect to discover contract
problems; that is what unit 1 is for.

**5.2 Dry-run the porter** — `python pipeline/port_artifact.py 1 --dry`. Read
every line of the thread delta, including the structure warnings.

**5.3 Fix problems in the artifact, in the research project, and re-download.**
Never hand-patch `source-artifacts/` — it is the untouched record of what the
research project produced, and divergence costs you the ability to re-port.

**5.4 Real port, then `python pipeline/build.py`.**

**5.5 Browser check** at desktop *and* ~375px. Confirm the legend renders with a
colour key — this is the check Matthew's Unit 11 would have failed.

**5.6 Feed unit 1 back into the contract.** Every ambiguity that came up in 5.1–5.3
gets resolved in `joshua_study_style_reference.md` or
`PROJECT-INSTRUCTIONS.md` **now**, before unit 2, and re-pasted. Unit 1 is the
most expensive unit to leave un-normalized: Matthew's `units/unit-01.html` is the
single most-churned fragment in the repo, with twenty commits, because it predates
every convention that came after it.

**5.7 Commit, and write the session summary.**

---

## After unit 1

The loop is `PIPELINE.md`. The rules are `CLAUDE.md`. The thing most likely to go
wrong is not technical — it is skipping step B3–B5 of the pipeline (read the
thread delta, apply it by hand, update the glossary in the same turn) on a unit
that looks fine.
