# Matthew Study — Style Reference

The artifact contract for pass 4: what a unit artifact must contain and must not.
`CHAT_SIDE_INSTRUCTIONS.md` and `core-workflow.md` govern how the passes work. Where a rule
gives a reason, the reason outranks the rule. `components-reference.md` holds the markup
for the optional components.

The artifact is a **site fragment**: one `<article class="unit" data-unit="N">`, opening
with a `unit-meta` block (§3) and ending with the notes. The **artifact never picks a
colour**: tracked threads get their fixed colour, any other root gets a hue from the build.
§8 shows the shape.

---

## 1. Colour policy

**A tracked root is one Greek lexical root**: one stem, with its inflected forms and
same-stem derivatives (`baptizō · baptisma`, `pistis · pisteuō`). It is not a theme, a
formula or a bundle of words sharing a point: `misthos` is a root, "the reward economy" is
not, and wise/foolish is two roots. Fixed titles and formulae Matthew repeats verbatim
(*ho huios tou anthrōpou*, *apo tote*) are the one exception, and they live in
`threads.json`.

- Pick the roots worth tracing: one that recurs and does theological or structural work,
  or a single striking translation choice. Each gets a `translit` (same-stem forms joined
  by `·`) and a plain-English `gloss`.
- Tag occurrences `<span class="r" data-root="X">word</span>`, where `X` is a short
  `[a-z0-9-]` slug. Use `class="rl"` for a mention that shouldn't count (legend rows,
  diagram labels, a gloss restating the term).
- **Same Greek root → same slug → same English root word**, even when it reads
  repetitively. The repetition is the point.
- **Tag every occurrence of a tracked thread's root**, even where the English uses another
  word (*hamartōlos* "sinner" tags `sin`; *periballō* "clothe" tags `throw`). The tag
  follows the lexeme, not the gloss. `threads-digest.md` lists the threads; the id is the slug.
- Every slug must be in `threads-digest.md` or this unit's `roots[]`, or the build fails.
  **`roots[]` is local roots only**: don't re-declare a tracked thread there.

**`echo`** (optional on any root): one line saying where the word has already appeared in
the LXX or reappears distinctively later, shown in the popover with a "cf.". Lead with the
reference, then say in a short clause what it adds. Echoes come from the kept rows of the
research notes, not from memory. Tracked threads can carry one in `threads.json`.

### What belongs where

Each link lives in exactly one place. Pick by what the link *is*:

| The link is… | It goes in | Shown |
|---|---|---|
| A word's history across books (a root) | root `echo` | the root's popover |
| One verse or phrase elsewhere that sounds through this verse; one sentence says it | `aside.echo` | the verse note, behind `*` |
| A *different* earlier event with the same shape, worth telling | `aside.story` | its own ◈ chip |
| The *same* event told by Mark, Luke or John, where Matthew's change is telling | `aside.synoptic` | its own ✧ chip |
| A quotation or direct citation | OT citation pointer (§4) | inline |
| A contested reading, or a debate that needs room | footnote | the endnotes |

An earlier event gets a story box if a reader needs the background to see the point, an
echo if one sentence carries it. A story box holds its own word-level evidence, so don't
also ship an echo for that link. An interpretive argument about a link is a footnote; the
box states only what the parallel is.

---

## 2. Word ids

Each thread is a hand-curated set of lemma ids in `data/roots.json`. Tag with `data-root`
only: **don't hand-chase word ids**, because the porter fills `data-w` and reports the few
it can't decide. Local roots don't need one.

---

## 3. The contract

The whole artifact is one `<article>`: no `<!doctype>`, `<html>`, `<head>`, `<body>`,
`<style>` or `<link>`, no inline `style`, no `--c-*` vars. `<script type="application/json"
id="unit-meta">` is its first child. Unknown top-level keys are an error.

| key | required | meaning |
|---|---|---|
| `unit` | ✓ | unit number (int) |
| `passage` | ✓ | `"Matthew 9:1–34"` |
| `title` | ✓ | working title from the unit map, refined if needed |
| `roots` | ✓ | local roots: `{root, translit, gloss, echo?}`, no colour |
| `threads` | ✓ | `{opens, payoffs, candidates, retro, promote?}`: the first four present, empty is fine |
| `slug` | — | derived if omitted |
| `movement` | — | looked up from the unit map if omitted |
| `descriptor` | — | the masthead tail line |
| `discourse` | — | `true` for the five discourse units |
| `questions`, `checks`, `intertext`, `typescenes` | — | below |

**`threads`**

- `opens` / `payoffs`: threads that begin or land here, `{id, ref, note?}`. `note` is the
  one-line popover prose; the porter copies it into the ready `threads.json` entry.
- `candidates`: roots recurring across units that could be promoted, `{root, why, ids?,
  refs?}`. `ids` are lemma ids as the word table spells them; a fixed phrase takes `seq`
  (the content words' ids in order); `refs` are bare `C:V`. Nothing is tagged until promoted.
- `promote`: a new thread ready for `threads.json`, from the handoff: `{entry, reach,
  retrofit}`. `entry` is `{id, root?, ids, gloss, opens: {unit, ref, note?}, payoffs:
  [{unit, ref, note?}], translit?, note?}` (`root` defaults to `id`; ASCII `[a-z0-9-]` only, e.g. `kerdaino`; a `retro[]` in the same unit may tag the promoted id, and `apply-delta` creates the `threads.json` and `roots.json` entries), `reach` a sentence ("16 occurrences, retrofit
  in units 1, 2, 5"), `retrofit` the unit numbers. **Claude decides promotion, biased toward
  book-wide**, and asks Lane only when genuinely unsure.
- `retro`: fixes for **earlier** units, instead of a prose note: `{unit, verse, text, root,
  why, nth?, op?, w?}`, with `unit` a slug like `"unit-06"` and `op` one of `add` (default),
  `retag`, `retag_word`, `untag_word`, `unwrap`, `strip_span`, `text`. The porter fills `w`.

**`questions[]`** — `{topic, note, options?}`. A call only Lane can make, with a genuinely
open alternative the unit's argument depends on, still open after the popups in pass 4.
A wording `translation-choices.md` or an earlier unit already rules is used, not asked.
Render your best provisional choice and flag it.

**`checks[]`** — `{ref, claim, expect}`. A claim about another passage's text that the
code side can verify (`ref` like `"Isa 22:22"`, `expect` the lemma(s), `"!lemma"` for
absent). These never go in `questions[]`.

**`intertext[]`** — `{ref, to, kind, note?}`: `ref` a bare `C:V`, `to` like `"Isa 6:10"`,
`kind` one of `quotation`, `allusion`, `echo`, `type-scene`, `story`, `character`, `reuse`.

**`typescenes[]`** — `{id, ref, note?, label?}`: `id` from the type-scene index; a new `id`
takes a `label`.

Root echoes, `aside.echo` and `aside.story` are harvested automatically, so list in these
two only what they don't say.

---

## 4. Components

All blocks sit directly inside `<article>`. Structural blocks (`.ring`, `table.exod`,
`.itin`) come first, before the verses. The optional components (echo, itin, compare,
synoptic, story) are in `components-reference.md`; Matthew's notes on them are below.

```html
<!-- legend: required, and the site fills it -->
<section class="block legend" aria-label="color key"><ul></ul></section>

<!-- ring or concentric map; `center` marks the pivot, labels stay a letter or two -->
<section class="block">
  <h2>TITLE — a concentric ring · C:V–V</h2>
  <p class="cap">one line on what the structure shows</p>
  <div class="ring">
    <div class="ringrow"><div class="lab">A<small>v–v</small></div><div class="txt">… <span class="ref">— gloss</span></div></div>
    <div class="ringrow center"><div class="lab">B<small>v–v</small></div><div class="txt">pivot</div></div>
  </div>
</section>

<!-- correspondence table: typology, OT↔NT pairing -->
<section class="block">
  <h2>TITLE</h2>
  <p class="cap">caption</p>
  <table class="exod">
    <tr><th>Left</th><th>Right</th></tr>
    <tr><td class="eg">source side</td><td class="mt">Matthew side</td></tr>
  </table>
</section>

<!-- pericope heading: every passage group, one form only -->
<h3 class="pericope">The centurion's boy <span>· 8:5–13</span></h3>

<!-- verse, then its gloss as a following sibling -->
<p class="v"><span class="n">12</span>English of the verse, with a
<span class="r" data-root="follow">tracked root</span>.<sup class="en"><a href="#n3">3</a></sup></p>
<span class="gloss">Short contextual gloss, sits beneath the verse.</span>

<!-- notes, then an optional footer -->
<div class="notes">
  <h2>Notes</h2>
  <ol><li id="n1"><strong>Lemma (v. N).</strong> Discussion.</li></ol>
</div>
<footer>Translation rendered from the SBLGNT Greek of Matthew C:V–V · Unit N of the Matthew study · wooden to the Greek by design</footer>
```

- **Verse siblings.** `.gloss`, `.compare`, `aside.echo`, `aside.story` and `aside.synoptic`
  follow the verse's `<p class="v">`, never nested. The endnote marker is the last thing in
  the verse `<p>`, never inside a `.gloss`, where the toggle would hide it.
- **Glosses** stay short: a phrase or one sentence, about 25 words at most. Longer material
  goes in a footnote with a bold lead.
- **Endnotes** use plain `id="nK"` / `href="#nK"`; the porter prefixes them per unit.
- **Pericope range.** Always include `· C:V–V`; the coverage audit reads chapter context
  from it. A pericope crossing a chapter shows the full `C:V–C:V`.
- **`data-verses`.** A block presenting verses *in place of* verse text carries
  `data-verses="C:V–V"` naming exactly the verses it replaces, and the pericope's gloss says
  they're condensed. The build fails if a declared verse is also written out.
- **Inside a story, synoptic or echo box:** no `data-root`, `class="r"` or `class="rl"`,
  because the scanner would corrupt thread counts. Greek is translit in
  `<span class="translit">`.
- **Hyperlinks.** Link significant LXX/OT citations and key terms: Bible Hub
  (`https://biblehub.com/BOOK/C-V.htm`), Logeion (`https://logeion.uchicago.edu/WORD`),
  NETS, Early Jewish Writings.

**OT citation pointer.** A verse that quotes or directly cites an OT text (a formula
quotation, "it stands written", a near-verbatim reuse on a character's lips) carries a
linked short ref, right after the quotation and before any endnote `<sup>`:

```html
<p class="v"><span class="n">3</span>…make straight his paths."
<a href="https://biblehub.com/isaiah/40-3.htm">(Isa 40:3)</a></p>
```

Use short SBL abbreviations; a range links to its first verse and labels the range. Don't
wrap the quoted words in the link. The Sermon's "y'all heard that it was said" antitheses
(5:21–48) stay unpointered: Matthew doesn't frame them as citations and several are
conflations.

**`aside.echo`** is for an allusion, a type-scene or a later reuse at verse level, not a
quotation. An example: at 11:29, "y'all will find rest for y'all's beings" sounds Jer 6:16.

**`aside.story`.** Read the target text before writing the box, and quote Matthew in the
verse text's own wording. Check `canon-decisions.md` before naming a `data-scene`; a new id
goes to Lane before it ships. No floor and no cap: as many as the unit's scenes earn.

**`aside.synoptic`.** The take says what Matthew did with the parallel and why it matters,
in two or three sentences, not a summary of it.

**Compare box.** Only at genuinely contested verses. Include NASB, and Hart or Lattimore
where their rendering is provocative.

**Voice.** No named commentators in artifact prose (Units 1–13 are boxed as shipped).
Dissolve the attribution into the point: "a dispensational reading argues…", not "Constable
argues…". The research passes still name people; only the artifact drops them.

---

## 5. Greek in English

**Transliteration only**, zero native Greek or Hebrew anywhere, attribute values included.
Scheme: η → `ē`, ω → `ō`; `th ph ch ps` for θ φ χ ψ; `y` for υ except in `ou au eu`;
γγ/γκ → `ng`/`nk`; rough breathing → initial `h`, initial ρ → `rh`; accents, smooth
breathing and iota subscript dropped. A Hebrew word uses `ḥ ṭ ś`, `ʾ`/`ʿ`, no vowel length.

**Wording.** A wooden-but-readable rendering from the SBLGNT, not a polish of an English
version. Check `translation-choices.md` before rendering a lexeme. A better verse-specific
rendering is fine, but it goes to Lane as a call.

---

## 6. Judgment

**Be tough on structures.** Map a chiasm in a `.ring` block only when it's real and
verifiable. Note repeated-word counts only where the number is theologically significant
(3, 7, 10, 12, 40, 70…). Verses read on their own: glosses, notes and boxes are additive,
never load-bearing.

---

## 7. Before saving

The port catches structural errors. These are the ones it can't:

- [ ] Plural "you" is **y'all**; `ouranos` is **sky / skies** in the study's own wording.
- [ ] Same Greek root → same English root, and wording matches `translation-choices.md`.
- [ ] Every tracked thread's root is tagged in this passage, wherever the English differs.
- [ ] Each term has transliteration and gloss at its first use in this unit.
- [ ] Every quotation has its OT citation pointer; no loose allusion does.
- [ ] Each link lives in one place. No echo for a link a story box covers, and no story box for the same event in another gospel.
- [ ] Every story box tells the story, states a difference and says what it does in Matthew. Nothing weak ships.
- [ ] Echoes and boxes come from the handoff, not from memory.
- [ ] Chiasms are real, and counts appear only where significant.
- [ ] No named commentators in the prose.
- [ ] Glosses are short; longer material is in footnotes.
- [ ] All calls were asked before drafting, and `questions[]` holds only what Lane left open.
- [ ] Text claims are in `checks[]`, ready promotions in `threads.promote`, earlier-unit fixes in `threads.retro`.
- [ ] Saved as `matthew_NN_translation.html`, zero-padded, in `/mnt/user-data/outputs/`, then `present_files`.

---

## 8. Worked example

```html
<article class="unit" data-unit="9">
<script type="application/json" id="unit-meta">
{
  "unit": 9,
  "passage": "Matthew 9:1–34",
  "title": "The Deeds of the Messiah (II)",
  "descriptor": "the second triad, and what following costs",
  "discourse": false,
  "roots": [
    { "root": "laugh-down", "translit": "katagelaō", "gloss": "laugh down, jeer at" }
  ],
  "threads": {
    "opens": [],
    "payoffs": [
      { "id": "release", "ref": "9:2", "note": "'your sins are released': the name's promise, now enacted" }
    ],
    "candidates": [],
    "retro": []
  }
}
</script>

<header class="mast">
  <div class="kicker">The Gospel According to Matthew · Study Translation</div>
  <h1>The Deeds of the Messiah (II)</h1>
  <div class="greek-title"><span class="translit">translit anchor phrase</span>
    — <span class="tsub">plain-English gloss of it</span></div>
  <div class="unit">Unit 9 · Matthew 9:1–34 · the second triad</div>
</header>

<section class="block legend" aria-label="color key"><ul></ul></section>

<h3 class="pericope">The paralysed man <span>· 9:1–8</span></h3>
<p class="v"><span class="n">2</span>…your sins are <span class="r" data-root="release">released</span>.<sup class="en"><a href="#n1">1</a></sup></p>
<span class="gloss">The verb that lets go nets and debts lets go sins.</span>

<div class="notes">
  <h2>Notes</h2>
  <ol><li id="n1"><strong>released (v. 2).</strong> The longer discussion.</li></ol>
</div>
</article>
```

---

## 9. The unit map

`matthew-literary-unit-map.md` is the plan of record: passages and seams are settled, and
titles are working titles.
