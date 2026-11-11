# Matthew Study — Style Reference

Matthew's differences from `fragment-contract.md` (shared, read first). This
file wins. For units 14 on; units 1–13 are boxed as shipped.

## Colour

- Tracked root = one Greek lexical root: one stem, its inflected forms and
  same-stem derivatives (`baptizō · baptisma`, `pistis · pisteuō`). `misthos`
  is a root, "the reward economy" is not; wise/foolish is two roots. Fixed
  titles and formulae Matthew repeats verbatim (*ho huios tou anthrōpou*,
  *apo tote*) are threads.
- `translit` here joins same-stem forms with `·`.
- **Same Greek root → same slug → same English root word**, even when it
  reads repetitively. The repetition is the point. (*hamartōlos* "sinner"
  tags `sin`; *periballō* "clothe" tags `throw`.)
- `class="rl"` for a mention that shouldn't count: legend rows, diagram
  labels, a gloss restating the term.
- Root `echo`: where the word already appeared in the LXX or returns later.

## Meta

- Extra top-level keys: `descriptor` (the masthead tail line), `discourse`
  (`true` for the five discourse units).
- `candidates[]`: a fixed phrase takes `seq` (the content words' ids in
  order).
- New `data-scene` or type-scene id goes to Lane before it ships.

## What belongs where

Each link lives in exactly one place:

| The link is… | It goes in |
|---|---|
| A word's history across books | root `echo` |
| One verse or phrase elsewhere sounding through this verse; one sentence says it | `aside.echo` |
| A *different* earlier event with the same shape, worth telling | `aside.story` |
| The *same* event told by Mark, Luke or John, where Matthew's change is telling | `aside.synoptic` |
| A quotation or direct citation | OT citation pointer, inline |
| A contested reading, a debate that needs room | footnote |

A story box holds its own word-level evidence: no echo for the same link. No
story box for the same event in another gospel. Every story box tells the
story, states a difference, says what it does in Matthew.

## Components

On: echo, itin, compare, synoptic, story (markup in
`components-reference.md`). All blocks sit directly inside `<article>`.
Structural blocks (`.ring`, `table.exod`, `.itin`) come first, before the
verses.

```html
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

<!-- after the notes, optional -->
<footer>Translation rendered from the SBLGNT Greek of Matthew C:V–V · Unit N of the Matthew study · wooden to the Greek by design</footer>
```

- Verse siblings: `.gloss`, `.compare`, `aside.echo`, `aside.story`,
  `aside.synoptic` follow the verse's `<p class="v">`, never nested.
- Endnotes use plain `id="nK"` / `href="#nK"`; porter prefixes them per unit.
- Pericope crossing a chapter shows the full `C:V–C:V`.
- Inside a story, synoptic or echo box: no `data-root`, `class="r"` or
  `class="rl"`. Greek is translit in `<span class="translit">`.
- Hyperlinks: link significant LXX/OT citations and key terms. Bible Hub
  (`https://biblehub.com/BOOK/C-V.htm`), Logeion
  (`https://logeion.uchicago.edu/WORD`), NETS, Early Jewish Writings.

**OT citation pointer.** A verse that quotes or directly cites an OT text
(formula quotation, "it stands written", near-verbatim reuse on a character's
lips) carries a linked short ref, right after the quotation, before any
endnote `<sup>`:

```html
<p class="v"><span class="n">3</span>…make straight his paths."
<a href="https://biblehub.com/isaiah/40-3.htm">(Isa 40:3)</a></p>
```

Short SBL abbreviations; a range links to its first verse and labels the
range. Don't wrap the quoted words in the link. The Sermon's "y'all heard that
it was said" antitheses (5:21–48) stay unpointered. No loose allusion gets a
pointer.

- **`aside.echo`**: allusion, type-scene or later reuse at verse level, not a
  quotation. At 11:29, "y'all will find rest for y'all's beings" sounds Jer
  6:16.
- **`aside.story`**: read the target text before writing the box; quote
  Matthew in the verse text's own wording. Roughly three to six a unit; no
  floor, no cap.
- **`aside.synoptic`**: the take says what Matthew did with the parallel and
  why it matters, two or three sentences, not a summary of it.
- **Compare box**: only at genuinely contested verses. Include NASB, and Hart
  or Lattimore where their rendering is provocative.
- **Voice**: dissolve attribution into the point: "a dispensational reading
  argues…", not "Constable argues…".

## Greek in English

**Transliteration** (the Greek letters here only explain the scheme): η →
`ē`, ω → `ō`; `th ph ch ps` for θ φ χ ψ; `y` for υ except in `ou au eu`;
γγ/γκ → `ng`/`nk`; rough breathing → initial `h`, initial ρ → `rh`; accents,
smooth breathing, iota subscript dropped. A Hebrew word uses `ḥ ṭ ś`,
`ʾ`/`ʿ`, no vowel length. Each term gets transliteration + gloss at its first
use in this unit.

**Wording.** Wooden-but-readable rendering from the SBLGNT, not a polish of an
English version. Plural "you" = **y'all**; `ouranos` = **sky / skies**. A
better verse-specific rendering than `translation-choices.md` goes to Lane as
a call.

## Judgment

- Map a chiasm in a `.ring` block only when it's real and verifiable.
- Repeated-word counts only where the number is theologically significant (3,
  7, 10, 12, 40, 70…).
- Verses read on their own: glosses, notes and boxes are additive, never
  load-bearing.
- Every quotation has its OT citation pointer.

## Worked example

Matthew's own; wins over the shared contract's.

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

## Unit map

`matthew-literary-unit-map.md` is the plan of record: passages and seams are
settled, titles are working titles.
