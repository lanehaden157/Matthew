# Matthew Study — Artifact Style & Template Reference

A stable reference for the per-unit HTML translation artifacts and the chat commentary.
Consult it before building each unit's artifact.

> This is a *reference* file — headers, tables, code blocks are fine here.
> The no-headers/no-bullets rule applies only to the pre-read briefing and the
> verse-by-verse commentary, which stay in flowing prose.

**How the artifact works, in one paragraph.** The artifact is a **site fragment**, not a
standalone page — one `<article class="unit" data-unit="N">` with **no `<head>`, `<style>`,
font links, or hand-picked colours**. It drops into the static site
(`github.com/lanehaden157/Matthew`) when Lane runs `python -m biblecore port NN`. It opens with a
machine-readable **`unit-meta` block** (§2) that drives the site's data files. Every
coloured word is `<span class="r" data-root="X">…</span>` (counted) or `class="rl"`
(root-linked, not counted) — no class names like `beget`, no inline `style`. The site
resolves colour **two-tier**: a root that is a tracked cross-unit thread
(`threads-digest.md`) gets that thread's fixed colour in every unit; any other root gets a
hue the build assigns. **The artifact never picks a hex.** The
colour legend **is required** — include an empty `<ul></ul>`; the site fills in the
`<li>`s and swatches from data, it does not build the section itself (§3;
C6/B8, platform-design-review.md — unit 11 shipped with no legend precisely
because this line said optional). Output is still
`/mnt/user-data/outputs/matthew_NN_translation.html`; its content is just the `<article>`.

---

## 1. Colour for recurring roots — declare, don't paint

**A tracked root is exactly one Greek lexical root** — one stem, with all its inflected
forms and same-stem derivatives (verb + noun + adjective off that stem: `baptizō` /
`baptisma`, `krinō` / `krima`, `pistis` / `pisteuō`). It is **not** a theme, a formula, or
a bundle of different words that happen to rhyme semantically. `misthos` is a root;
"the reward economy" (misthos + apechō + apodidōmi) is not. `phōs` is a root;
"wise vs. foolish" (phronimos + mōros) is two roots, not one. If you catch yourself
grouping distinct lexemes under one colour because they share a *point*, stop — track the
one that carries the most weight and recurs, or track each separately. Fixed titles and
structural formulae Matthew repeats verbatim (*ho huios tou anthrōpou*, *apo tote*, *ho
nomos kai hoi prophētai*) are the one allowed exception, and they live in `threads.json`,
not in a unit's local roots.

Within a unit, pick the roots worth tracing (a Greek root that recurs and is doing
theological or structural work). For each one, decide the **transliteration** (list the
same-stem forms with `·`, e.g. `gennaō · genesis`) and a **plain-English gloss**. That's
it — **do not choose a colour, do not write a `<style>` block, do not invent `--c-*` vars.**

- List every tracked root in the `unit-meta` block's `roots` array (§2).
- Tag each occurrence in the prose as `<span class="r" data-root="X">word</span>`, where
  `X` is a short `[a-z0-9-]` slug (e.g. `follow`, `little-faith`, `law-prophets`).
- Use `class="rl"` instead of `class="r"` for a *root-linked* mention that shouldn't be
  counted as an occurrence (legend rows, diagram labels, a gloss restating the term).
- **Same Greek root → same `data-root` slug → same English root word**, across every verse
  in the unit, even when it reads repetitively. The repetition is the point.
- If a root is a **tracked cross-unit thread**, use *its* slug from `threads-digest.md`
  (the `data-root` column) so the site gives it the thread's global colour. Otherwise use
  any sensible slug; the build assigns a local hue.
- `roots[]` is for **local** roots. Don't re-declare a tracked thread there;
  `data/threads.json` is its single source of truth (older units did, and it
  does no harm, but new artifacts needn't).
- A `data-root` that resolves to no colour anywhere is a hard verify failure — so every
  slug you tag **must** appear either in `threads-digest.md` or in the `roots` array.

### Same-stem forms

There is no "motif" tier — everything tracked is one lexical root. A root's `translit`
lists its same-stem forms joined by `·` (`baptizō · baptisma`, `pistis · pisteuō`,
`eleos · eleeō`); tag every form with the one slug. Different words are different roots
(or not tracked) — see §1.

### 1a. `echo` — the canon behind and after a word (research pass, pass 2)

**`echo`** — optional field on any `roots[]` entry: one line saying where the word has
already appeared in the LXX (Matthew's own Old Testament, in Greek), or where it
reappears distinctively later in the canon, shown in the root's popover with a "cf."
prefix (Lane, 2026-09-22, adopting Joshua's convention — see its style reference §1 for
the worked examples: *sole of the foot*, Gen 8:9; *scarlet*, Gen 38). Lead with the
reference, then say in one short clause what it adds. A word with a canon history
should at least get a local root with an `echo`, even when it is tagged nowhere else in
the unit. Read for these the way you read for notable translation choices. Tracked
threads can carry an `echo` in `threads.json` too.

This is different from the **OT citation pointer** (§ below): a pointer marks Matthew
*quoting* or directly citing an OT text at that verse (formula quotations, "it stands
written"). `echo` is for the quieter case — a word or image with a canon history that
the verse doesn't cite outright: an allusion, a type-scene, a later reuse (including
elsewhere in the NT). A verse can carry both. Echoes should come from the kept rows of
the research pass's notes file (`core-workflow.md`, pass 2), not from memory at
drafting time — `canon-leads/canon-leads-unit-NN.md` (`python -m biblecore leads`) is the
mechanical half of that pass: where the unit's rare Greek words and shared two-word
phrases occur in the LXX and the rest of the NT, plus a noun sweep of the unit's
people, places and objects. It's a word search, not a judgment.

#### What belongs where

Each link lives in exactly one place. Pick by what the link *is*:

| The link is… | It goes in | Shown |
|---|---|---|
| A word's history across books (a tracked root) | root `echo` (above) | the root's popover |
| One verse or phrase elsewhere that sounds through this verse; one sentence says it | `aside.echo` (§3) | the verse note, behind `*` |
| A *different* earlier event with the same shape, worth telling: its background, what's the same, what's different, what Matthew does with it | `aside.story` (§3) | its own ◈ chip |
| The *same* event told by Mark, Luke or John, where Matthew's change is telling | `aside.synoptic` (§3) | its own ✧ chip |
| A formula quotation | OT citation pointer (§3) | inline |
| A contested reading, or a debate that needs room | footnote | the endnotes |

How to choose:
- The same event in another gospel → a synoptic, never a story box.
- An earlier event → a story box if it needs telling (a reader would need the
  background to see the point), an echo if one sentence carries it.
- When a story box covers a link, its word-level evidence goes inside the box.
  Don't also ship an echo for the same link.
- An interpretive argument about a link → a footnote; the story box states only
  what the parallel is.

**Ruling (Lane, 2026-10-25).** Story boxes, the pass reorder and the synoptic norm.
Lane's favourite intertext work was the Unit 14 scene walk: earlier stories told with
their background (Herod's feast beside Pharaoh's birthday feast, Elisha's loaves,
Exodus 14 at the sea), not word matches. The old loop couldn't produce that: the
intertext pass started from the rare-word sheet, its output was a ledger of one-line
links, and it ran after the verse-by-verse, so what it found never reached Lane, who
learns by listening to passes 1 and 3. Synoptic boxes were capped at 0–3 a unit, and
every unit hit the cap. So: a new `aside.story` component, research before the
verse-by-verse (`core-workflow.md`), and no synoptic cap. **Open point, carried
forward:** the endnote-marker rule (§4 says a marker sits at the end of the verse
`<p>`, never inside a `.gloss`) and what §3's examples and Unit 14 actually do
don't quite agree; Lane hasn't ruled.

---

## 2. Fragment shape

The whole artifact is one `<article>`, and nothing else — no `<!doctype>`, `<html>`,
`<head>`, `<body>`, `<style>`, or `<link>`.

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
    { "root": "faith",   "translit": "pistis · pisteuō",  "gloss": "trust, entrust oneself" },
    { "root": "forgive", "translit": "aphiēmi",           "gloss": "let go, release, forgive" }
  ],
  "threads": {
    "opens":   [],
    "payoffs": [
      { "id": "release", "ref": "9:2",
        "note": "'your sins are released' — the forgiveness the name promised (1:21), now enacted" },
      { "id": "little-faith", "ref": "9:22" }
    ],
    "candidates": [
      { "root": "compassion", "why": "splanchnizomai — fires 9:36, again 14:14, 15:32; worth promoting",
        "ids": ["splanchnizomai"], "refs": ["9:36", "14:14", "15:32"] }
    ],
    "retro": [
      { "unit": "unit-06", "verse": 12, "text": "debts", "root": "release",
        "why": "opheilēmata 6:12 — aphiēmi 'release' fires in the same verse, untagged" }
    ]
  }
}
</script>

<header class="mast">
  <div class="kicker">The Gospel According to Matthew · Study Translation</div>
  <h1>UNIT TITLE</h1>
  <div class="greek-title"><span class="translit">translit anchor phrase</span>
    — <span class="tsub">plain-English gloss of it</span></div>
  <div class="unit">Unit 9 · Matthew 9:1–34 · short descriptor</div>
</header>

<!-- structural sections, then the verses, then the notes (all below) -->
</article>
```

### The `unit-meta` block

| key | required | meaning |
|---|---|---|
| `unit` | ✓ | unit number (int) |
| `passage` | ✓ | e.g. `"Matthew 9:1–34"` |
| `title` | ✓ | working title from the Unit Map (`matthew-literary-unit-map.md`), refined if needed |
| `roots` | ✓ | every tracked root: `{root, translit, gloss, echo?}`. **No colour.** One Greek lexical root each — same-stem forms joined by `·` in `translit`; never a bundle of different words (§1). `echo` (§1a) is optional. |
| `threads` | ✓ | `{opens, payoffs, candidates, retro, promote?}` — the first four present, each a list, empty is fine; `promote` optional; see below |
| `slug` | — | `"unit-09"`; derived if omitted |
| `movement` | — | 1 / 2 / 3; looked up from the Unit Map if omitted |
| `descriptor` | — | the masthead tail line |
| `discourse` | — | `true` for the five discourse units |
| `questions` | — | calls only Lane can make, with a genuinely open alternative (below) |
| `checks` | — | claims about other passages' text for the code side to verify (below) |
| `intertext` | — | cross-book links worth recording (below) |
| `typescenes` | — | type-scene instances in this unit (below) |

`threads.opens` / `threads.payoffs` — the tracked threads (by their `id` from
`threads-digest.md`) that **begin** or **land** in this unit, each `{id, ref, note?}`.
Optional `note` is the one-line popover prose for that beat — the porter puts it straight
into the ready `threads.json` entry, so write it here rather than only in the commentary.
The porter turns these into a delta file for Lane to fold into `threads.json`.

`threads.candidates` — roots recurring across units that could be *promoted* to tracked
threads: `{root, why, ids?, refs?}`. `why` is a one-line reason. `ids` are the lemma ids
you saw, copied as the word table spells them (`splanchnizomai`, never Greek script);
a fixed phrase takes `seq` instead, the content words' lemma ids in order. `refs` are a
few representative verses as bare `C:V`. Claude decides whether a candidate is promoted,
biased toward book-wide, and asks Lane only when genuinely unsure; nothing is tagged
until it is promoted.

`threads.retro` — a fix-list for **earlier** units: things the close reading of *this*
unit made you notice about a prior one. Entries are `retrofit-tags.json` shape —
`{unit: "unit-06", verse, text, root, why}` (add the missing tag), or with
`op: "retag"` / `from` / `to` to move a mis-tagged span. `root`/`to` must be a tracked
thread or a declared root of that unit; `w` (the word id) is optional, since the
porter fills it. The porter dry-checks each against the target
fragment and merges the ones that apply. Use this instead of a prose "we should revisit
Unit 6" note.

`threads.promote` (optional) — a new thread ready for `threads.json`, taken from the
handoff: `{entry, reach, retrofit}`. `entry` is `{id, root, ids, gloss, opens: {unit, ref,
note?}, payoffs: [{unit, ref, note?}], translit?, note?}` (`ids` the lemma ids; no colour,
`python -m biblecore colour` assigns it), `reach` a sentence ("16 occurrences, retrofit in
units 1, 2, 5"), `retrofit` the unit numbers that need tags added. Use it for a thread Lane
has ruled on with the reach in view; `candidates` stays for a proposal that still needs an
id set. The porter turns it into a ready delta.

### `questions[]`, `checks[]`, `intertext[]`, `typescenes[]` (optional)

- `questions[]` — `{topic, note, options?}`. A call only Lane can make, with a
  genuinely open alternative the unit's argument depends on. Read
  `translation-choices.md` and the earlier units' meta first: a wording already ruled
  is used, with a note in the artifact's prose, not a question. The build chat asks every
  open call by popup before drafting (handoff calls, provisional renderings, conflicts
  with synced rulings); only what Lane left open goes here. Render
  your best provisional choice so the draft keeps moving, and flag it. Claude Code asks
  Lane each one by popup when the unit is ported.
- `checks[]` — `{ref, claim, expect}`. A claim about another passage's text that the
  code side can verify against the corpus (`ref` like `"Isa 22:22"`, `claim` what the
  artifact says, `expect` the lemma(s) it should find, a string or a list). Never a
  question: the porter prints checks in their own section and Lane doesn't answer them.
- `intertext[]` — `{ref, to, kind, note?}`: `ref` a bare `"C:V"` in Matthew, `to` a
  reference like `"Isa 6:10"`, `kind` one of `quotation`, `allusion`, `echo`,
  `type-scene`, `story`, `character`, `reuse`. An `aside.echo`, a root's `echo` and
  an `aside.story` box are already harvested, so list here only what those don't say.
- `typescenes[]` — `{id, ref, note?, label?}`: `id` from the type-scene index
  (`commissioning`, `water-crossing`, `mountain-theophany`, `annunciation`, ...). A
  new `id` is fine; give it a `label`.

### Endnotes

Use plain `id="nK"` / `href="#nK"` in the artifact. The porter prefixes them per unit
(`u09-nK`) so they don't collide in the site's shared notes pane. Every `href` must resolve
to an `id` in the same fragment.

---

## 3. Component snippets

All blocks live directly inside `<article>`. No colour vars — the classes below are styled
by the site's stylesheets (`css/core.css`, `components.css`, and the book's `theme.css`).

### Colour legend (REQUIRED — include the empty `<ul></ul>`; the site fills it in,
it does not create the section)

```html
<section class="block legend" aria-label="color key">
  <h2>Recurring roots — colour key</h2>
  <ul>
    <li><span class="r" data-root="follow">akoloutheō</span> — "follow, come along behind"</li>
    <li><span class="r" data-root="forgive">aphiēmi</span> — "let go, release, forgive"</li>
    <!-- one <li> per tracked root; the site adds the swatch + occurrence count -->
  </ul>
</section>
```

You may ship this as a stub (`<section class="block legend"><ul></ul></section>`) — the
site fills it from `units.json` / `threads.json` / `occurrences.json`. Do **not** hand-write
swatch dots or `style="background:…"`.

### Concentric / ring / triptych map (use `center` on the pivot row)

```html
<section class="block">
  <h2>TITLE — a concentric ring · C:V–V</h2>
  <p class="cap">one-line description of what the structure shows</p>
  <div class="ring">
    <div class="ringrow"><div class="lab">A<small>v–v</small></div><div class="txt">… <span class="ref">— gloss</span></div></div>
    <div class="ringrow center"><div class="lab">B<small>v–v</small></div><div class="txt">centre / pivot</div></div>
    <div class="ringrow"><div class="lab">A′<small>v–v</small></div><div class="txt">… <span class="ref">— gloss</span></div></div>
  </div>
</section>
```

Keep ring labels to a letter or two (`A`, `B′`, `C`). A long word in `.lab` gets squeezed;
if you must, the porter tags it `lab-word` so CSS can shrink it.

**`data-verses`** — a ring, table or other block that presents verses *in place of*
verse-by-verse text (a prayer set as a block, a table that condenses a repeated
formula) carries `data-verses="C:V–V"` (or `C:V–C:V`) naming exactly the verses it
replaces. Tracked words in those verses are then reported as covered by the block,
not as untagged gaps. The build fails if a declared verse is also written out as a
`<p class="v">`, or if the range falls outside the unit's passage. Say in the
pericope's gloss that the verses are condensed. Units 1–13 predate this check.

### Correspondence table (typology, Synoptic divergence, OT↔NT pairing)

```html
<section class="block">
  <h2>TITLE</h2>
  <p class="cap">caption</p>
  <table class="exod">
    <tr><th>Left column</th><th>Right column</th></tr>
    <tr><td class="eg">source side</td><td class="mt">Matthew side</td></tr>
  </table>
</section>
```

### Itinerary / sequence chips

```html
<div class="itin">
  <span class="stop">Place <sup>14:1–12</sup></span><span class="arr">→</span>
  <span class="stop">Place <sup>14:13–21</sup></span>
</div>
```

A stop's `<sup>` is its **verse**, `C:V` or a range `C:V–V`, never a theme word
(unit 14's first draft had "tripped up", "fear", "fed" there, and the port
failed it).

### Section heading (one per pericope / passage-group)

```html
<h3 class="pericope">The centurion's boy <span>· 8:5–13</span></h3>
```

One form only, site-wide: `<h3 class="pericope">`, an editorial title, then the
verse range in a `<span>` (rendered small + italic). Use it to divide the
translation into its natural passage units. Do **not** use `h2`, `secthead`,
`panel`, or `movement` — the site rewrites those to `pericope` but new artifacts
should emit the right thing. Every unit gets these; keep titles short and
descriptive (a phrase, not a sentence).

Always include the `· C:V–V` range — the coverage audit reads chapter context
from it. When a unit **crosses a chapter boundary** (e.g. 3:1–4:11), the pericope
that spans the break must show the full `C:V–C:V` range so the new chapter's
start is explicit (`· 3:13–4:11`).

### A verse + inline gloss

```html
<p class="v"><span class="n">12</span>English of the verse, with a
<span class="r" data-root="follow">tracked root</span> and an endnote<sup class="en"><a href="#n3">3</a></sup>.</p>
<span class="gloss">Short contextual gloss in italics, sits directly beneath the verse.</span>
```

`<p class="v">` with the `.gloss` / `.compare` as **following siblings**, never nested.

### OT citation pointer

When a `<p class="v">` verse quotes or directly cites an OT text (a formula
quotation, an "it stands written" / "it was said" citation, or a near-verbatim
reuse on a character's lips), close the verse with a linked short-ref pointer —
book abbreviation + `C:V` in parentheses, linked to Bible Hub, **after** the
quotation and **before** any endnote `<sup>`:

```html
<p class="v"><span class="n">3</span>…make straight his paths."
<a href="https://biblehub.com/isaiah/40-3.htm">(Isa 40:3)</a></p>
```

Short SBL-style abbreviations (`Isa`, `Deut`, `Ps`, `Mic`, `Hos`, `Jer`, `Exod`).
Range refs link to the first verse, label the range: `(Isa 9:1–2)`. If the quote
sits mid-verse, the pointer goes right after it, not at the verse end. Do **not**
wrap the quoted words themselves in the link, and do not pointer-tag loose
allusions the verse only echoes — those get an `aside.echo` or a root `echo`
(§1a) instead, below. The
Sermon's "y'all heard that it was said" antitheses (5:21–48) are left unpointered
by decision: Matthew doesn't frame them as citations and several are conflations.

### Cross-canon echo (`aside.echo` — a verse-level `echo`, intertext pass)

```html
<p class="v"><span class="n">15</span>…and their eyes they have closed.</p>
<aside class="echo" data-anchor="13:15">Isaiah's own words, quoted here almost verbatim — the
prophet's warning to a hardened people becomes the reason Jesus gives for speaking in parables.</aside>
```

`<aside class="echo" data-anchor="C:V">` as a **following sibling** of the verse it
comments on — same placement rule as `.gloss`/`.compare`, and it shares `.gloss`'s note
(`*`) toggle rather than getting its own chip (Lane, 2026-09-22: reads as one more thing
worth a second look, not a separate research thread the way a Synoptic parallel is). The
CSS prepends "cf." — don't write it into the echo's own text, or it renders "cf. cf.
Isa 6:10…". `data-anchor` must match the `C:V` of the verse it's actually a sibling of.
Translit only, no `data-root`/`class="r"`/`class="rl"` inside it. Use this for a
verse-level connection (an allusion, a type-scene, a later reuse); use a root's `echo`
(§1a) for a word-level one. Not for formula quotations — those get the OT citation
pointer below. Not for an earlier story that needs telling — that's an `aside.story`
(below; §1a "What belongs where").

### Earlier story (`aside.story` — a different, earlier event with the same shape)

```html
<p class="v"><span class="n">6</span>But when Herod's birthday came…</p>
<aside class="story" data-anchor="14:6" data-kind="type-scene" data-scene="royal-birthday-feast" data-strength="strong">
  <h4><span class="par-title">Pharaoh's birthday feast</span> <span class="par-ref">Gen 40:20–22</span></h4>
  <p class="par-story">Two to four plain sentences telling the earlier story, with the background a reader needs.</p>
  <ul class="par-match"><li>a king's birthday feast</li><li>a head lifted off</li></ul>
  <p class="par-diff">What's different. Required: no box ships without one.</p>
  <p class="par-does">What it does in Matthew: irony, reversal, identification, fulfilment, warning.</p>
  <p class="par-later">Later reuse, only if there is one.</p>
</aside>
```

`<aside class="story" data-anchor="C:V">` as a **following sibling** of the verse the
story bears on, or of the last verse of the scene it covers (`data-span="14:3–12"`
optional), after any `.gloss`/`.compare`/`aside.echo` on that verse. The site hides each
one behind its own ◈ chip, labelled "Type scene" for `data-kind="type-scene"` and "Earlier
story" otherwise; the chip carries no title. The site also supplies the part labels
(Same, Different, In Matthew, Later), so don't write them.

- `data-kind`: `type-scene`, `story`, `allusion`, `character` or `reuse`. A
  `type-scene` box names its type-scene in `data-scene` (`[a-z0-9-]`). Check
  `canon-decisions.md` first; a new id goes to Lane before it ships.
- `data-strength`: `strong` or `possible`. A weak link never ships as a story box; it
  stays in the notes or becomes a footnote.
- Required: the `<h4>` with `par-title` and `par-ref`, then `par-story`, `par-diff` and
  `par-does`. `par-match` and `par-later` are optional.
- Read the target text before writing the box. Quote Matthew in the verse text's own
  wording.
- Transliteration only, and no `data-root`/`class="r"`/`class="rl"` inside (same reason
  as the synoptic box). No named commentators.
- No floor and no cap: as many as the unit's scenes earn. Each box is harvested into the
  canon (an intertext row per reference, a type-scene row for `data-scene`), so don't
  repeat it in `intertext[]` or `typescenes[]`.

### Compare box (contested verses only)

```html
<div class="compare">
  <div class="row"><span class="src">Greek (translit.)</span><span class="txt translit">…transliterated phrase…</span></div>
  <div class="row"><span class="src">NASB</span><span class="txt">rendering for comparison</span></div>
  <div class="row"><span class="src">Hart</span><span class="txt">or Lattimore where illuminating</span></div>
  <div class="row"><span class="src">Text-form</span><span class="txt">MT vs LXX note when relevant</span></div>
</div>
```

### Synoptic parallel (every telling divergence)

```html
<aside class="synoptic" data-anchor="9:2">
  <h4>Mark 2:5 · Luke 5:20 <span>— short label for what the difference is</span></h4>
  <div class="row"><span class="src">Mark 2:5</span><span class="txt">wooden English, with <span class="translit">greek term</span> where it matters</span></div>
  <div class="row"><span class="src">Luke 5:20</span><span class="txt">…</span></div>
  <p class="take">Two or three sentences: what Matthew did with the parallel and why it matters for his argument — not a summary of the parallel.</p>
</aside>
```

`<aside class="synoptic" data-anchor="C:V">` as a **following sibling** of the anchor
verse's `<p class="v">` — after any `.gloss`/`.compare` already attached to that verse, same
placement rule as those. It is emitted whole, with its own `<h4>` header naming the
parallel(s) — the app doesn't rewrite the header, it only hides the aside by default and
adds its ✧-chip toggle (its own accent, distinct from the gold "Rendering" chip; a separate
toggle per parallel, not merged the way multiple `.compare` boxes are). `data-anchor` is
informational (matches the verse it sits after) — the app locates it by DOM position, not
by the attribute. Never nest it inside the verse. Never put `data-root`/`class="r"`/
`class="rl"` inside it — the occurrence scanner counts every `data-root` in the file and a
coloured word here corrupts cross-unit thread counts. Greek inside a row is
`<span class="translit">…</span>`, plain, uncoloured. **How many:** no cap (Lane,
2026-10-25; it was 0–3, and every unit hit it). Every scene Mark, Luke or John tell gets
checked, and every one where Matthew's change is telling (an addition, an omission, a
reordering, a rewording that shifts the point) gets a box: expect roughly three to six a
unit. The same event in another gospel is a synoptic, never an `aside.story`.

### Endnotes

```html
<div class="notes">
  <h2>Notes</h2>
  <ol>
    <li id="n1"><strong>Lemma (v. N).</strong> Discussion. Link out with <a href="URL">↗</a>.</li>
  </ol>
</div>
```

### Footer (optional)

```html
<footer>Translation rendered from the SBLGNT Greek of Matthew C:V–V · Unit N of the Matthew study · wooden to the Greek by design</footer>
```

---

## 4. Conventions checklist (run before shipping each artifact)

**Fragment structure**
- [ ] The file is one `<article class="unit" data-unit="N">…</article>` and nothing else — no `<head>`, `<style>`, `<link>`, `<!doctype>`.
- [ ] `<script type="application/json" id="unit-meta">` is the first child of `<article>` and is valid JSON with `unit`, `passage`, `title`, `roots`, and `threads` (the four lists `opens`, `payoffs`, `candidates`, `retro`; `promote` optional).
- [ ] No `roots` entry carries a colour. No `--c-*` vars anywhere. No inline `style="color:…"` / `style="background:…"`.
- [ ] Every coloured word is `<span class="r" data-root="X">` or `class="rl"`; every `X` appears in `threads-digest.md` **or** in the `roots` array.
- [ ] Endnote `id`/`href` use bare `nK`; every `href="#nK"` resolves in-fragment.
- [ ] `<p class="v">` verses with `.gloss`/`.compare`/`aside.synoptic`/`aside.echo`/`aside.story` as siblings, not nested. Endnote markers sit at the end of the verse `<p>`, never inside a `.gloss`.
- [ ] No `aside.synoptic`, `aside.echo` or `aside.story` block contains `data-root`, `class="r"`, or `class="rl"` — translit only.
- [ ] Every `aside.echo` and `aside.story` has a `data-anchor="C:V"` matching the verse it follows.
- [ ] Every `aside.story` states a difference (`par-diff`), tells the story (`par-story`) and says what it does in Matthew (`par-does`); its `data-strength` is `strong` or `possible`, never weak; a `type-scene` box has its `data-scene`.
- [ ] Each link lives in one place (§1a "What belongs where"): no `aside.echo` for a link a story box already covers, no story box for the same event in another gospel.
- [ ] The translation is divided into passage groups by `<h3 class="pericope">Title <span>· C:V–V</span></h3>` — no other heading form.
- [ ] Structural blocks (`.ring`, `table.exod`, `.itin`) come first, before the verses. The site also hoists them, but author them up top.
- [ ] A block that stands in place of verses carries `data-verses`; every `.itin` stop's `<sup>` is `C:V` or `C:V–V`.

**Translation & wording**
- [ ] Plural "you" → **"y'all"** everywhere in the translation.
- [ ] `ouranos` → **"sky / skies"**, always, in the study's own wording (verse text, glosses, diagrams). Verbatim NASB / Hart / Lattimore quotations keep their own wording.
- [ ] Same Greek root → same English root across verses, even when repetitive.
- [ ] Every `roots` entry is **one** Greek lexical root (same-stem forms only) — no themes, no formulae, no bundles of different words (§1).
- [ ] On first use of a tracked term *in this unit*, give transliteration + gloss; reintroduce the gloss even if a prior unit already had it — nothing carries over.
- [ ] Verses read on their own; glosses, notes, compare boxes are additive, never load-bearing.
- [ ] Compare box only at genuinely contested verses; include NASB, bring in Hart / Lattimore where their rendering is provocative.
- [ ] Hyperlinks for significant LXX/OT citations and key terms (biblehub, Logeion, NETS, earlyjewishwritings).
- [ ] Every `<p class="v">` that quotes/cites an OT text ends with a linked `(Book C:V)` Bible Hub pointer (§ OT citation pointer) — after the quote, before any `<sup>`; quoted words not themselves wrapped in the link.
- [ ] Every word with a Torah/LXX or later-canon history gets an `echo` (§1a) — a local `roots[]` entry if nowhere else, or an `aside.echo` for a verse-level connection. Checked against `canon-leads/canon-leads-unit-NN.md` and the research pass's notes file (`core-workflow.md` pass 2), not from memory.
- [ ] Chiasms / concentric structures mapped in a `.ring` block, not just described. These should be real and verifiable only, not loose made up connections forcing a pattern.
- [ ] Repeated-word counts noted only where the frequency is theologically significant (3, 7, 10, 12, 40, 70…).
- [ ] Transliteration only — zero native Greek or Hebrew script anywhere, attribute values and `threads.candidates` included.
- [ ] No named commentators in the artifact's prose (notes, glosses, compare boxes), from unit 13 on. Dissolve the attribution into the point: "a dispensational reading argues…", not "Constable argues…"; state a shared conclusion plainly rather than "(so France, Wright)". The research passes still name traditions; only the artifact drops the names. Units 1–12 are a separate tracked retrofit (`PLAN.md`).

**Threads**
- [ ] Checked `threads-digest.md`: **every** morphological occurrence of a tracked thread's Greek root in this passage is tagged with its thread `id` — even where the English renders it with a different word (*hamartōlos* → "sinner" still tags `sin`; *periballō* → "clothe" still tags `throw`). The tag follows the Greek lexeme, not the gloss. Threads that open or land here are also listed under `threads.opens` / `threads.payoffs`. The porter's coverage audit will list any you missed.
- [ ] Any root recurring across units that isn't yet a thread → `threads.candidates` with a reason (+ `ids` or `seq`, `refs`). Not tagged until it is promoted.
- [ ] A new thread Lane has ruled on, with its reach → `threads.promote` (`entry`, `reach`, `retrofit`), copied from the handoff.
- [ ] Calls were asked in chat before drafting (handoff's Calls for Lane, provisional renderings, departures from synced rulings); `questions[]` holds only what Lane left open.
- [ ] Any call only Lane can make → `questions[]` with your best provisional choice rendered, not a question in chat after the calls have been asked. Only genuinely open calls, never a wording `translation-choices.md` or an earlier unit already rules.
- [ ] Claims about other passages' text the code side can verify → `checks[]` (`ref`, `claim`, `expect`), never `questions[]`.
- [ ] Anything you noticed about an **earlier** unit (a missed tag, a mis-tag) → `threads.retro`, not a prose aside.

**Ship**
- [ ] Saved to `/mnt/user-data/outputs/matthew_NN_translation.html` (zero-padded), then `present_files`.
- [ ] (Site side, Lane / Claude Code) `python -m biblecore port NN`, review the thread delta and promotions, `data-w`, `build`, `test`, eyeball in the browser, commit.

### Chat-side conventions
The research passes (briefing, research notes, verse-by-verse) and the handoff are governed by the project instructions (`CHAT_SIDE_INSTRUCTIONS.md`), `core-workflow.md` and `canon-handoff-template.md`, not by this file. The artifact itself is built in a fresh build chat that opens with the pasted handoff; it builds from that, this file and the synced files without redoing the research.

---

## 5. Most-used reference URLs

| Use | URL pattern |
|---|---|
| OT verse (MT + English, parallels) | `https://biblehub.com/BOOK/C-V.htm` |
| Greek interlinear, Matthew | `https://biblehub.com/interlinear/matthew/C.htm` |
| Greek lexicon (fast) | `https://logeion.uchicago.edu/WORD` |
| LXX in English (NETS, per-book PDF) | `https://ccat.sas.upenn.edu/nets/edition/` |
| Young's Literal, Matthew | `https://ebible.org/engylt/MATCC.htm` (zero-padded) |
| Chrysostom homilies on Matthew | `https://www.newadvent.org/fathers/2001.htm` (homily N = `2001NN.htm`) |
| Second Temple texts index | `https://www.earlyjewishwritings.com/` |
| Psalms of Solomon 17 (Davidic messiah) | `https://www.earlyjewishwritings.com/psalmsofsolomon.html` |
| 1 Enoch (Son of Man) | `https://www.earlyjewishwritings.com/1enoch.html` |
| Targum traditions | `http://targuman.org/targum/` |
| Synoptic parallels | `https://www.gospelparallels.com/` |
| Bible Project Matthew overview | `https://bibleproject.com/explore/video/matthew/` |

The full annotated list (Dead Sea Scrolls, Didache, NETS, Allison's *New Moses*, and the rest) is `matthew_reference_links.md`.

The commentary set, and how to weigh it, is in `resources.md`; the lens is in
`CHAT_SIDE_INSTRUCTIONS.md`; the annotated shelf is `matthew_reference_links.md`.

---

## 6. Finding the next unit

This file is **not** a running log. To find which unit is next, check `PLAN.md` and
`session_index.md` in the site repo (or ask Lane), then take the following row from the
Literary Unit Map (`matthew-literary-unit-map.md`). The map is the plan of record: passages and seams are settled;
titles are working titles. Which roots a unit traces is decided per unit (§1); colour is
the site's job, and `data/units.json` records what each built unit tracks.

---

## 6a. Cross-unit threads — see `threads-digest.md`

The canonical list of tracked threads (id, root slug, translit, gloss, origin → payoff,
open/closed, per-thread note) is **`threads-digest.md`** in the site repo, generated from
`data/threads.json`, and synced to the research project automatically (`project-side/synced/`).

When you build a unit: tag **every occurrence** of a tracked thread's Greek root with its
`id` (follow the lexeme, not the English gloss); list threads that open or land under
`threads.opens` / `threads.payoffs` with a one-line `note`; and close the loop in the
commentary when a payoff lands. Propose new threads via `threads.candidates` (+ `ids` or
`seq`) — Claude decides promotion, biased book-wide, and asks Lane when unsure; once a
thread is promoted, `data-w` and `retrofit` tag it in every built unit. Flag anything you
notice about an earlier unit in `threads.retro`. The coverage audit (`python -m biblecore
audit`) cross-checks every thread's lemma ids against the built fragments and reports misses.

---

---

## 7. Literary Unit Map

The 28-unit map lives in `matthew-literary-unit-map.md` (synced to the project): the
structural skeleton, every unit's passage and title, the divergences from the chapter
grid, and the five discourses with their extra-scope flags. Confirm scope against it
before each walkthrough.
