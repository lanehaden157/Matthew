# `pipeline/hebrew.py` — design

A sibling to `pipeline/greek.py`, not a generalization of it. Same architectural
role: one small pure module, deterministic, no dependencies, a `__main__` block
of worked examples, and every word it touches logged for human review. Different
internals throughout, because the two problems are not the same problem.

Read `docs/audit/port-analysis.md` §1.1 and §7 first — this document assumes them.

---

## 0. What the transliteration is *for*

Three consumers, and the scheme has to serve all three:

1. **Legend headwords and endnote lemmas** — the reader sees `ḥesed` next to a
   coloured word and learns what the colour means.
2. **Root recognition across forms** — the whole point of the colour system is
   that the reader notices the same root recurring. If *melek*, *malkī*, and
   *hammelek* don't visibly share letters, the transliteration has failed at its
   main job even if it is phonetically perfect.
3. **Reading aloud** — Lane should be able to say the word.

It is explicitly *not* for: reconstructing the pointing, distinguishing vowel
length, or supporting philological argument. Those wants pull toward a heavier
scheme; resist them. `matthew_study_style_reference.md`'s own framing —
"transliterate every word, gloss its meaning, never print native script" — is
about carrying the language to a reader who doesn't read it.

---

## 1. The scheme

### 1.1 Governing rule

**A diacritic only where the plain Latin letter is already claimed by a different
Hebrew letter.** This is what keeps the diacritic load honest: every mark in the
output is load-bearing, and a reader can be told the rule in one sentence.

Under that rule, four consonants get marks (`ḥ ṭ ś` and the `ʾ`/`ʿ` pair) and no
vowel does.

### 1.2 Consonants

| Hebrew | Output | Note |
|---|---|---|
| א | `ʾ` | U+02BE modifier letter right half ring |
| ב | `b` | no spirantization — see §1.4 |
| ג | `g` | |
| ד | `d` | |
| ה | `h` | silent word-final ה still written `h` (`naḥalah`) — see §1.6 |
| ו | `w` | consonantal; as a vowel letter see §1.5 |
| ז | `z` | |
| ח | `ḥ` | `h` is taken by ה |
| ט | `ṭ` | `t` is taken by ת |
| י | `y` | consonantal; as a vowel letter see §1.5 |
| כ ך | `k` | |
| ל | `l` | |
| מ ם | `m` | |
| נ ן | `n` | |
| ס | `s` | |
| ע | `ʿ` | U+02BF modifier letter left half ring |
| פ ף | `p` | |
| צ ץ | `ts` | `ts` is unclaimed, so no diacritic is needed |
| ק | `q` | `q` is unclaimed |
| ר | `r` | |
| שׁ | `sh` | |
| שׂ | `ś` | `s` is taken by ס |
| ש (unpointed) | `sh` | with a warning — the sin/shin dot is missing from the source |
| ת | `t` | |

**Final forms transliterate identically to their base forms.** ך=k, ם=m, ן=n,
ף=p, ץ=ts. This is not the same thing as the stem-matching fold in §3 — that is
a separate fix in a separate file, and conflating them is how the bug survives.

**Precedent, not invention.** Matthew's own `MANUAL` override table already
renders the handful of Hebrew loanwords in the Greek text this way — `ḥoba`,
`ḥanef`, `shamayim` ([extract_units.py:212-217](pipeline/extract_units.py#L212-L217)).
The scheme above generalizes the choices Lane already made by hand, rather than
imposing a new one. Note that the *deterministic* stopgap beside it
(`_rom_hebrew`) does something different and worse — `ch` for ח, and a single `'`
collapsing א and ע into one another — which is exactly why it must not become the
primary path.

### 1.3 Why `w` for ו and `q` for ק

`w` is the biblical value and keeps ו distinct from ב if spirantization is ever
modeled. `q` for ק rather than `k` because the letter is genuinely distinct
(`qol` vs `kol` are different words) and `q` costs nothing — nothing else wants
it.

### 1.4 Begadkefat spirantization: **not modeled**

ב ג ד כ פ ת each have a plosive and a fricative realization depending on dagesh
lene. A full scheme renders `b/v g/gh d/dh k/kh p/f t/th`.

**Decision: always render the plosive.** `melek` not `melekh`, `bayit` not
`vayit`, `torah` not `thorah`.

Justification, in priority order:

1. **It would defeat purpose (2).** The same root shows `k` in *malkī* and `kh`
   in *melek*; `p` in *mishpaṭ* and `f` in *sofer*. The colour system's entire
   claim is that the reader sees recurrence. A scheme that spells one root two
   ways every other verse actively works against the product.
2. **It makes correctness depend on dagesh detection.** Dagesh lene and dagesh
   forte are the same codepoint (U+05BC); telling them apart requires knowing
   whether the preceding syllable is open or closed. That is real logic with real
   edge cases, in service of a distinction the reader was never going to use.
3. **SBL's general-purpose style does the same thing**, for the same audience
   reason.

Cost, stated plainly: the transliteration will not tell a reader why Hebrew
speakers say *khesed* rather than *ḥesed* — but nothing about `ḥ` was going to
tell them that anyway.

### 1.5 Vowels: quality only, no length

| Point | Output |
|---|---|
| patah ַ , qamats ָ | `a` |
| segol ֶ , tsere ֵ | `e` |
| hiriq ִ | `i` |
| holem ֹ , holem-waw וֹ | `o` |
| qubbuts ֻ , shuruq וּ | `u` |
| hatef-patah ֲ | `a` |
| hatef-segol ֱ | `e` |
| hatef-qamats ֳ | `o` |
| vocal sheva ְ | `e` |
| silent sheva ְ | *(nothing)* |
| hiriq + י (ִי) | `i` |
| tsere/segol + י | `e` |
| qamats + ה (word-final) | `ah` |

**Decision: no macrons, no breves, no superscripts.** Quantity is collapsed:
qamats and patah both give `a`, tsere and segol both give `e`.

Justification: the diacritic budget is already spent on `ḥ ṭ ś ʾ ʿ`, which
disambiguate *consonants a reader would otherwise confuse*. Vowel length
disambiguates nothing a reader of this study will act on, and `mišpāṭ` asks more
of Lane than `mishpaṭ` delivers to him. The audit's §3.5 lesson applies directly:
this project already built a richer taxonomy tier once and reverted it as
complexity the data didn't need.

**Qamats-qatan** (a qamats pronounced `o`, as in *kol* כָּל) is the one real cost
of collapsing quantity — it is written identically to ordinary qamats and only
context distinguishes them. Handle it the way `greek.py` handles its own
irregulars: a small `MANUAL` override dict consulted before the deterministic
pass, seeded with the handful of high-frequency words (`kol`, `ḥokmah`,
`qodesh`), extended when the log flags one.

### 1.6 Sheva: the one place with real logic

Sheva is vocal (`e`) or silent (nothing), and the rule is not lookup-table
shaped. Implement the standard rule:

Vocal if — word-initial; the second of two adjacent shevas; under a letter
carrying dagesh forte; or immediately after a long vowel. Silent otherwise.

This rule has genuine exceptions and any implementation of it will be wrong
occasionally. That is acceptable **only if every sheva decision is logged**, the
same way `greek.py`'s docstring promises "every span it touches is logged for
review." Log line per word: the surface form, the output, and which sheva rule
fired. Review the log for the first three units, then spot-check.

### 1.7 Dagesh forte → doubled consonant

`הַמֶּלֶךְ` → `hammelek`, not `hamelek`. It costs one character and it shows the
reader the assimilated article, which the commentary will want to point at.

**Flag this as the decision most likely to be reversed after unit 1.** If
`hammelek` reads worse than `hamelek` in practice, it is a one-line change plus a
`translation-choices.md` log entry. Decide it once, in unit 1, and record the
decision — do not let it drift.

### 1.8 Maqqef, capitals, and the divine name

- **Maqqef** (־) → `-`. It is textual punctuation; keep it.
- **Capitals**: capitalize proper nouns only, matching `greek.py`'s
  "preserve leading capital" behaviour. The Hebrew source has no case, so this
  requires a name list — start with the one the Joshua text needs and grow it.
- **יהוה is not a transliteration problem, it is a policy problem.** The pointing
  in the Masoretic text is the *qere perpetuum* — the vowels of *adonai* or
  *elohim* set on the consonants YHWH. Transliterating the points mechanically
  produces `yehowah`, a form nobody in the Bible ever said. **The module must
  special-case יהוה to output the bare consonants `YHWH`**, and the English
  rendering (*Yahweh* / *the LORD* / *the Name*) is a `translation-choices.md`
  decision Lane makes at unit 1. Matthew already set a precedent here
  (commit `5739624`, the Lord→Master/Yahweh pass) — carry it forward
  deliberately rather than rediscovering it.

  Same treatment for the other qere-perpetuum forms the text carries.

---

## 2. Module shape

Mirror `greek.py` exactly, because the shape is the part that transfers:

```python
"""Deterministic Hebrew -> Latin transliteration. …scheme summary…
Good enough for legend headwords and endnote lemmas; every word it touches is
logged for review."""

_CONS   = { … }          # §1.2
_VOWEL  = { … }          # §1.5
_MANUAL = { … }          # qamats-qatan words, יהוה, irregular names

def transliterate(text: str) -> str:
    """Transliterate a Hebrew word/phrase. Non-Hebrew characters pass through."""

if __name__ == "__main__":
    for t in [ …worked examples… ]:
        print(f"{t}  ->  {transliterate(t)}")
```

Two departures from `greek.py`, both deliberate:

**(a) Fail loud on the wrong script.** `greek.py`'s detection gate silently
returns non-Greek input unchanged — verified: `greek.transliterate("מֶלֶךְ")`
returns `"מֶלֶךְ"`. That behaviour is fine when Greek is the only script in play
and catastrophic when it isn't. `hebrew.transliterate` should pass through
plain-Latin text (it is called on mixed strings) but **raise** on Greek
codepoints, so a copy-pasted Matthew fixture fails immediately instead of
shipping untransliterated.

**(b) The log is not optional.** `greek.py` says every span is logged; make
`hebrew.py` actually return or emit the decision record, because §1.6's sheva
rule and §1.5's qamats-qatan gap both depend on a human reading it.

### Worked examples for the `__main__` block

Seed it with words that exercise each hard case, and with what the study will
actually trace in Joshua:

```
מֶלֶךְ            -> melek          (final kaf; segol/segol)
הַמֶּלֶךְ          -> hammelek       (article + dagesh forte, §1.7)
חֶסֶד             -> ḥesed          (ḥet, §1.2)
חֵרֶם             -> ḥerem          (the Joshua thread)
נַחֲלָה           -> naḥalah        (hatef-patah; final ה, §1.5)
מִשְׁפָּט           -> mishpaṭ        (shin dot; ṭet; no spirantization, §1.4)
יְהוֹשֻׁעַ          -> Yehoshuaʿ      (initial vocal sheva; ayin)
בְּנֵי יִשְׂרָאֵל     -> bene yisraʾel  (vocal sheva; sin; aleph)
כָּל               -> kol            (qamats-qatan, MANUAL, §1.5)
יהוה              -> YHWH           (qere perpetuum, §1.8)
```

Each of these has a documented reason to be in the list. A test file that
asserts them is worth more than any other test in the pipeline, because
everything downstream displays what this function returns.

---

## 3. The two fixes in `audit_thread_coverage.py`

These are not part of `hebrew.py` but they are the other half of the same
problem, and the audit flags both as must-fix-before-first-use.

### 3.1 Final-form fold — the Greek bug, worse

`strip_accents` folds Greek final sigma `ς → σ` (commit `6453a4b`). Hebrew has
five letters with distinct final forms and no fold exists. Demonstrated against
the live function:

```
stem מלכ  vs  מֶלֶךְ   (melek, "king")   -> NO MATCH
stem מלכ  vs  מְלָכִים (melakim, plural)  -> match
```

**This is worse than the Greek case, not merely analogous.** In Greek, final
sigma broke the inflected forms while the citation form matched. In Hebrew the
polarity is reversed: Hebrew lemmas are cited in the absolute singular, which is
exactly where a final-form letter sits. A `melek` thread in Joshua — a book with
thirty-one kings in one chapter list — would report every plural and silently
miss every singular.

Fix, one line in `strip_accents`:

```python
_FINALS = str.maketrans("ךםןףץ", "כמנפצ")
... .lower().translate(_FINALS)
```

**Good news, verified:** niqqud and cantillation need no new code.
`unicodedata.combining()` already returns non-zero across the pointing range
(sheva 10, qamats 18, dagesh 21, cantillation 220), so the existing
combining-mark strip handles pointed text correctly as written.

### 3.2 Substring stems are structurally weaker in Hebrew — consider lemmas instead

`thread-stems.json`'s `_note` explains why Greek stems are substring matches:
augment and reduplication defeat prefix matching. Hebrew has that problem *and*
three more that substring matching cannot solve at all:

- **Prefix stacking.** ו ה ל ב כ מ ש glue to the head of a word, and the article
  triggers gemination, so `הַמֶּלֶךְ` is not `ה` + the citation form. Substring
  matching absorbs this — but it means `^`-anchored stems are useless in Hebrew,
  and every stem over-matches far more than its Greek counterpart, making
  `exclude` load-bearing from day one rather than an occasional tuning knob.
- **I-nun assimilation.** נתן ("give") yields יִתֵּן (*yitten*) and תֵּן (*ten*) —
  **the nun is not in the word.** No substring of נתן matches either form.
  Same for לקח → יִקַּח.
- **Hollow and III-he roots.** קום → קָם (*qam*); עשה → עָשׂוּ, יַעַשׂ. The middle or
  final radical disappears.

A stem list will therefore miss a large, *silent*, and root-dependent fraction of
occurrences — precisely the failure mode the coverage audit exists to prevent.

**Recommendation: match on lemma, not on substring.** The Open Scriptures Hebrew
Bible (OSHB / WLC) ships per-word lemma and morphology tags. If the source text
carries them, `thread-stems.json` becomes a `thread-lemmas.json` mapping each
thread to one or more lemma ids, and the audit becomes *more* accurate than
Matthew's, not less — no stems, no `exclude`, no homograph tuning.

Keep the stem mechanism as a supplement for the cases lemma data can't express
(the Hebrew equivalent of `phrase: true` fixed titles, and any thread that
deliberately spans two lemmas).

**This is a decision for Lane, not a default.** It changes the shape of one data
file and the matching half of one script, in exchange for removing the largest
silent-failure surface in the port. Decide it at bootstrap, before the first
thread is defined — see `BOOTSTRAP.md` step 4. What must *not* happen is
inheriting `thread-stems.json` unexamined because it worked for Greek.
