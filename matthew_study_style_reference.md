# Matthew Study — Artifact Style & Template Reference

A stable reference for the per-unit HTML translation artifacts and the chat commentary.
Consult it before building each unit's artifact.

> This is a *reference* file — headers, tables, code blocks are fine here.
> The no-headers/no-bullets rule applies only to the pre-read briefing and the
> verse-by-verse commentary, which stay in flowing prose.

**How the artifact works, in one paragraph.** The artifact is a **site fragment**, not a
standalone page — one `<article class="unit" data-unit="N">` with **no `<head>`, `<style>`,
font links, or hand-picked colours**. It drops into the static site
(`github.com/lanehaden157/Matthew`) via `pipeline/port_artifact.py`. It opens with a
machine-readable **`unit-meta` block** (§2) that drives the site's data files. Every
coloured word is `<span class="r" data-root="X">…</span>` (counted) or `class="rl"`
(root-linked, not counted) — no class names like `beget`, no inline `style`. The site
resolves colour **two-tier**: a root that is a tracked cross-unit thread
(`threads-digest.md`) gets that thread's fixed colour in every unit; any other root gets a
hue the pipeline assigns into `data/units.json`. **The artifact never picks a hex.** The
colour legend may be a stub — the site rebuilds it from data (§3). Output is still
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
  any sensible slug; the pipeline assigns a local hue and you tweak the hex in
  `data/units.json` after porting if two land too close.
- A `data-root` that resolves to no colour anywhere is a hard verify failure — so every
  slug you tag **must** appear either in `threads-digest.md` or in the `roots` array.

### Same-stem forms

There is no "motif" tier — everything tracked is one lexical root. A root's `translit`
lists its same-stem forms joined by `·` (`baptizō · baptisma`, `pistis · pisteuō`,
`eleos · eleeō`); tag every form with the one slug. Different words are different roots
(or not tracked) — see §1.

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
    "payoffs": [ { "id": "release", "ref": "9:2" }, { "id": "little-faith", "ref": "9:22" } ],
    "candidates": [
      { "root": "compassion", "why": "splanchnizomai — fires 9:36, again 14:14, 15:32; worth promoting" }
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
| `title` | ✓ | working title from the Unit Map (§7), refined if needed |
| `roots` | ✓ | every tracked root: `{root, translit, gloss}`. **No colour.** One Greek lexical root each — same-stem forms joined by `·` in `translit`; never a bundle of different words (§1). |
| `threads` | ✓ | `{opens, payoffs, candidates}` — see below |
| `slug` | — | `"unit-09"`; derived if omitted |
| `movement` | — | 1 / 2 / 3; looked up from the Unit Map if omitted |
| `descriptor` | — | the masthead tail line |
| `discourse` | — | `true` for the five discourse units |

`threads.opens` / `threads.payoffs` — list the tracked threads (by their `id` from
`threads-digest.md`) that **begin** or **land** in this unit, each `{id, ref}`. The porter
turns these into a delta file for Lane to fold into `threads.json`.

`threads.candidates` — roots recurring across units that you think should be *promoted* to
tracked threads: `{root, why}`, one-line reason. Never assumed — surfaced for Lane.

### Endnotes

Use plain `id="nK"` / `href="#nK"` in the artifact. The porter prefixes them per unit
(`u09-nK`) so they don't collide in the site's shared notes pane. Every `href` must resolve
to an `id` in the same fragment.

---

## 3. Component snippets

All blocks live directly inside `<article>`. No colour vars — the classes below are styled
by the site's one stylesheet (`css/styles.css`).

### Colour legend (optional — the site rebuilds it from data)

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
  <span class="stop">Place <sup>Prophet</sup></span><span class="arr">→</span>
  <span class="stop">Place <sup>Prophet</sup></span>
</div>
```

### A verse + inline gloss

```html
<p class="v"><span class="n">12</span>English of the verse, with a
<span class="r" data-root="follow">tracked root</span> and an endnote<sup class="en"><a href="#n3">3</a></sup>.</p>
<span class="gloss">Short contextual gloss in italics, sits directly beneath the verse.</span>
```

`<p class="v">` with the `.gloss` / `.compare` as **following siblings**, never nested.

### Compare box (contested verses only)

```html
<div class="compare">
  <div class="row"><span class="src">Greek (translit.)</span><span class="txt translit">…transliterated phrase…</span></div>
  <div class="row"><span class="src">NASB</span><span class="txt">rendering for comparison</span></div>
  <div class="row"><span class="src">Hart</span><span class="txt">or Lattimore where illuminating</span></div>
  <div class="row"><span class="src">Text-form</span><span class="txt">MT vs LXX note when relevant</span></div>
</div>
```

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
- [ ] `<script type="application/json" id="unit-meta">` is the first child of `<article>` and is valid JSON with `unit`, `passage`, `title`, `roots`, `threads`.
- [ ] No `roots` entry carries a colour. No `--c-*` vars anywhere. No inline `style="color:…"` / `style="background:…"`.
- [ ] Every coloured word is `<span class="r" data-root="X">` or `class="rl"`; every `X` appears in `threads-digest.md` **or** in the `roots` array.
- [ ] Endnote `id`/`href` use bare `nK`; every `href="#nK"` resolves in-fragment.
- [ ] `<p class="v">` verses with `.gloss`/`.compare` as siblings, not nested.

**Translation & wording**
- [ ] Plural "you" → **"y'all"** everywhere in the translation.
- [ ] `ouranos` → **"sky / skies"**, never "heaven / heavens", in the study's own wording (verse text, glosses, diagrams). Verbatim NASB / Hart / Lattimore quotations keep their own wording.
- [ ] Same Greek root → same English root across verses, even when repetitive.
- [ ] Every `roots` entry is **one** Greek lexical root (same-stem forms only) — no themes, no formulae, no bundles of different words (§1).
- [ ] On first use of a tracked term *in this unit*, give transliteration + gloss; reintroduce the gloss even if a prior unit already had it — nothing carries over.
- [ ] Verses read on their own; glosses, notes, compare boxes are additive, never load-bearing.
- [ ] Compare box only at genuinely contested verses; include NASB, bring in Hart / Lattimore where their rendering is provocative.
- [ ] Hyperlinks for significant LXX/OT citations and key terms (biblehub, Logeion, NETS, earlyjewishwritings).
- [ ] Chiasms / concentric structures mapped in a `.ring` block, not just described.
- [ ] Repeated-word counts noted only where the frequency is theologically significant (3, 7, 10, 12, 40, 70…).
- [ ] Transliteration only — zero native Greek or Hebrew script anywhere.

**Threads**
- [ ] Checked `threads-digest.md`: every tracked thread that surfaces in this passage is tagged with its thread `id` and listed under `threads.opens` / `threads.payoffs`.
- [ ] Any root recurring across units that isn't yet a thread → added to `threads.candidates` with a reason (not tagged as a thread until Lane promotes it).

**Ship**
- [ ] Saved to `/mnt/user-data/outputs/matthew_NN_translation.html` (zero-padded), then `present_files`.
- [ ] (Site side, Lane / Claude Code) `python pipeline/port_artifact.py NN`, review the thread delta, eyeball in the browser, commit.

### Chat-side conventions (commentary, not artifact)
- Pre-read briefing and verse-by-verse: **flowing prose only** — no bullets, headers, bold, markdown.
- Confirm scope before each walkthrough; flag chapter-grid divergences and the five discourses (5–7, 10, 13, 18, 23–25) as multi-chapter units.
- Hold Constable in active dialogue with France, Wright, Bible Project notes, Jewish / Second Temple / rabbinic voices, and Chrysostom — don't let the dispensationalist frame stand unchallenged.
- Flag rabbit holes and ask whether to go deeper or keep moving.

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

### Scholars to weigh per crux
Davies & Allison (ICC, technical), France (NICNT, literary-canonical), Keener (background/
social-historical), Luz (reception history), Wright (Jewish context/new creation), Meier
(historical), Bauckham, Amy-Jill Levine (Jewish readings). Bible Project teacher notes for
the literary-canonical frame; Constable for traditional/dispensationalist, to be balanced.

---

## 6. Finding the next unit

This file is **not** a running log. To find which unit is next, check `PLAN.md` and
`session_index.md` in the site repo (or ask Lane), then take the following row from the
Literary Unit Map (§7). The map is the plan of record: passages and seams are settled;
titles are working titles. Which roots a unit traces is decided per unit (§1); colour is
the site's job, and `data/units.json` records what each built unit tracks.

---

## 6a. Cross-unit threads — see `threads-digest.md`

The canonical list of tracked threads (id, root slug, translit, gloss, origin → payoff,
open/closed, per-thread note) is **`threads-digest.md`** in the site repo, generated from
`data/threads.json`. Lane refreshes it in the research project whenever it changes.

When you build a unit: tag each tracked thread that surfaces with its `id`, list it under
`threads.opens` / `threads.payoffs` in the `unit-meta` block, and close the loop in the
commentary when a payoff lands. Propose new threads via `threads.candidates` — Lane
promotes them; only then are they tagged as threads.

---

## 7. Literary Unit Map (full gospel)

Twenty-eight units, each *roughly* chapter-length, cut along Matthew's own literary seams
rather than the medieval chapter divisions. Where a unit's boundary diverges from a chapter
boundary, the divergence is flagged. Confirm scope against this map before each walkthrough.

### 7.1 The structural skeleton Matthew built in

Four converging structural signals layer to define the seams:

**(a) The two *apo tote* ("from that time") hinges (Kingsbury)** — *Apo tote ērxato ho
Iēsous* at **4:17** ("began to proclaim") and **16:21** ("began to show" he must suffer) —
carving three movements: **the person of the Messiah (1:1–4:16)**, **the proclamation in
Galilee (4:17–16:20)**, **the road to the cross (16:21–28:20)**. France's "drama in three
acts" maps onto the same skeleton.

**(b) The five discourse formulas (Bacon)** — *kai egeneto hote etelesen ho Iēsous* at
**7:28, 11:1, 13:53, 19:1, 26:1** — the Sermon on the Mount (5–7), the Mission charge (10),
the Kingdom parables (13), the Community discourse (18), the Woes + Olivet discourse
(23–25). Bacon's "new Pentateuch," Jesus as the new Moses — the Bible Project's "Messianic
Torah" frame.

**(c) Mackie / Bible Project macro-design** fuses (a) and (b): an **Introduction
(1:1–4:17)** and matching **Conclusion (26:1–28:20)**, each saturated with formula
quotations, framing a **three-part body (4:17–25:46)** — Kingdom *established* (4:17–11:1),
Kingdom *resisted* (11:2–16:20), Kingdom *confronts Jerusalem* (16:21–25:46). The lens of
record for the study.

**(d) Davies & Allison's triads + the great inclusio** — Matthew composing in threes at
every scale; and the **Emmanuel inclusio**, *meth' hēmōn ho theos* "God with us" (1:23)
answered by *egō meth' hymōn eimi* "I am with y'all" (28:20). The `with` root is load-bearing
across the whole gospel — worth tagging (thread id `emmanuel`) in any unit where it surfaces.

### 7.2 The twenty-eight units

Format: **Unit — passage — title.** ✅ = built.

**MOVEMENT ONE — The Person of the Messiah (1:1–4:16/17).**

- **Unit 1 — 1:1–25 — The Book of the Genesis.** ✅ Genealogy + birth.
- **Unit 2 — 2:1–23 — Out of Egypt I Called My Son.** ✅ Magi, flight, Nazareth.
- **Unit 3 — 3:1–4:11 — Wilderness, Water, Wilderness.** ✅ John, baptism, temptation.
  **Diverges:** runs past 3:17 to 4:11 — John → baptism → testing is one wilderness movement;
  seam at 4:11, not the 3/4 line.
- **Unit 4 — 4:12–25 — The Light Has Dawned.** ✅ Withdrawal to Capernaum, Isaiah 9, call of
  the four, the 4:23 ministry summary. Short (14 vv), straddles the 4:17 hinge — built as a
  standalone overture.

**MOVEMENT TWO — The Kingdom Proclaimed in Galilee (4:17–16:20).**

*Part A — Kingdom established in word and deed (4:17–11:1).*

- **Unit 5 — 5:1–48 — The Greater Righteousness.** ✅ Beatitudes, salt & light, the six
  contrasts.
- **Unit 6 — 6:1–34 — Before Your Father Who Sees.** ✅ The three acts of piety with the
  Lord's Prayer at the concentric centre, then treasure, the eye, mammon, anxiety.
- **Unit 7 — 7:1–29 — The Two Ways.** ✅ Judging, the pearls, ask/seek/knock, the Golden
  Rule, the three eschatological pairs, the crowd's astonishment (7:28).
  - ⚑ **Discourse 1 = the Sermon on the Mount (5:1–7:29)**, split 5 / 6 / 7. **Watch across
    the seam:** the *Law and the Prophets* inclusio — opened **5:17**, closed **7:12**. Open
    scoping alternative: 5:1–48 / 6:1–7:12 / 7:13–29. Confirm at the Sermon.
- **Unit 8 — 8:1–34 — The Deeds of the Messiah (I).** ✅ Leper, centurion, Peter's
  mother-in-law + summary, would-be followers, the storm, the Gadarene demoniacs.
- **Unit 9 — 9:1–34 — The Deeds of the Messiah (II).** ✅ Paralytic, call of Matthew, the
  fasting question, Jairus's daughter + the haemorrhaging woman, two blind men, the mute
  demoniac. Ch. 9 *minus* the harvest summary. **Watch across the seam:** chs. 8–9 are one
  ten-miracle deed-block (three triads with interludes) answering chs. 5–7.
- **Unit 10 — 9:35–11:1 — The Sending (Discourse 2).** The harvest/compassion summary
  (9:35–38) as on-ramp, then the Mission charge, closed by the 11:1 formula. **Diverges:**
  starts at 9:35.

*Part B — Kingdom meets growing hostility (11:2–16:20).*

- **Unit 11 — 11:2–30 — Are You the Coming One?** John's question, Jesus on John, woes on the
  towns, the great invitation. 11:2–30 (11:1 belongs to the prior formula).
- **Unit 12 — 12:1–50 — Lord of the Sabbath, Servant of the Lord.** Two Sabbath conflicts,
  Isaiah 42, Beelzebul, the sign of Jonah, the return of the unclean spirit, the true family.
- **Unit 13 — 13:1–53 — The Parables of the Kingdom (Discourse 3).** Sower through the
  householder's treasure; the pivot from crowds to disciples; closed at 13:53.
- **Unit 14 — 13:54–14:36 — Rejection, a Beheading, Bread, and the Sea.** Nazareth, Herod
  and John's death, the 5,000, the walking on water, Gennesaret. **Diverges:** starts 13:54.
- **Unit 15 — 15:1–39 — Clean and Unclean; Bread for the Dogs.** The defilement controversy,
  the Canaanite woman, the 4,000. Unified by clean/unclean, bread, and Israel → nations.
- **Unit 16 — 16:1–20 — On This Rock.** The demand for a sign, the leaven, Peter's confession.
  Ends **16:20** — the climax of Movement Two, before the 16:21 hinge.

**MOVEMENT THREE — The Road to the Cross (16:21–28:20).**

*Part A — The journey (16:21–20:34).*

- **Unit 17 — 16:21–17:27 — The Road to the Cross Begins; Transfigured.** First passion
  prediction (at the hinge), "take up your cross," the Transfiguration, the boy healed, the
  second prediction, the temple tax. **Diverges:** opens at 16:21.
- **Unit 18 — 18:1–35 — Life in the Community (Discourse 4).** Greatness as a child, the
  little ones, the lost sheep, reproof in the *ekklēsia*, unlimited forgiveness, the
  unforgiving servant; closed at 19:1.
- **Unit 19 — 19:1–30 — Leaving Galilee: Marriage, Children, Riches.** The departure
  (19:1–2 doubles as the formula), divorce and celibacy, the children, the rich young man,
  "the first/last."
- **Unit 20 — 20:1–34 — The Last Shall Be First.** The labourers in the vineyard, the third
  passion prediction, the sons of Zebedee, the two blind men at Jericho. **Watch across the
  seam:** **19:30 ↔ 20:16** first/last inclusio — read 19:16–20:16 as one arc.

*Part B — Jerusalem (21:1–25:46).*

- **Unit 21 — 21:1–46 — The King Enters; the Temple Judged.** Triumphal entry, the temple
  action, the fig tree, the authority challenge, the two sons, the tenants.
- **Unit 22 — 22:1–46 — The Banquet and the Four Questions.** The wedding banquet, then the
  four controversy dialogues. **Watch across the seam:** the three judgment parables run
  **21:28–22:14**.
- **Unit 23 — 23:1–39 — Seven Woes and a Lament.** The indictment of the scribes and
  Pharisees, the lament over Jerusalem.
- **Unit 24 — 24:1–51 — The Olivet Discourse (I): Temple and Son of Man.** The temple's
  fall, the birth-pangs, the abomination, the coming of the Son of Man, the fig tree, "this
  generation," the first watchfulness parables.
- **Unit 25 — 25:1–46 — The Olivet Discourse (II): Three Parables of the End (Discourse 5).**
  Ten virgins, the talents, the sheep and the goats; closed at 26:1.
  - ⚑ **Discourse 5 spans 23:1–25:46** in the Mackie scheme, split 23–25. Live debate
    whether ch. 23 belongs with the Olivet Discourse — flag on arrival.

*Part C — Conclusion (26:1–28:20).*

- **Unit 26 — 26:1–75 — The Night of Betrayal.** Plot, the anointing, Judas's bargain, the
  Last Supper, Gethsemane, the arrest, the Sanhedrin trial, Peter's denial. **Long (75 vv)**
  — candidate to split (26:1–46 / 26:47–75); confirm with Lane.
- **Unit 27 — 27:1–66 — The Crucifixion.** Pilate, the death of Judas, Barabbas, the mockery,
  the crucifixion, the death with its signs, the burial, the guard.
- **Unit 28 — 28:1–20 — The Mountain of Commission.** The empty tomb and the women, the
  cover-up, the Great Commission. **Watch across the whole book:** closes the Emmanuel
  inclusio (28:20 ↔ 1:23) and the mountain frame (4 / 5 / 28).

### 7.3 Divergences from the chapter grid, at a glance

| Unit | Passage | Why it's cut here |
|---|---|---|
| 3 | 3:1–4:11 | John + baptism + testing = one wilderness movement; seam is 4:11 |
| 4 | 4:12–25 | overture to the public ministry; straddles the 4:17 hinge |
| 9 | 9:1–34 | the 9:35–38 harvest summary is pulled into the Mission unit |
| 10 | 9:35–11:1 | Mission Discourse + its harvest on-ramp + closing formula |
| 11 | 11:2–30 | starts after the 11:1 formula |
| 14 | 13:54–14:36 | starts after the 13:53 parables formula |
| 16 | 16:1–20 | ends at 16:20, just before the 16:21 hinge |
| 17 | 16:21–17:27 | opens at the 16:21 hinge |

Inclusios/triads to read *across* unit seams: **5:17↔7:12** (Law & Prophets, Units 5–7),
**19:30↔20:16** (first/last, Units 19–20), **21:28–22:14** (three judgment parables, Units
21–22), **1:23↔28:20** (Emmanuel, Units 1 & 28).

### 7.4 The five discourses (extra-scope flags)

- **Discourse 1 — Sermon on the Mount (5–7)** → Units 5, 6, 7. Heavy rabbit-hole risk.
- **Discourse 2 — Mission (10)** → Unit 10 (with 9:35–38 on-ramp).
- **Discourse 3 — Kingdom Parables (13)** → Unit 13.
- **Discourse 4 — Community (18)** → Unit 18.
- **Discourse 5 — Woes + Olivet (23–25)** → Units 23, 24, 25. Heavy rabbit-hole risk.
