# Matthew Study — Artifact Style & Template Reference

A stable reference for the HTML translation artifacts and the chat commentary, so the
formatting, component structure, and conventions stay consistent across every unit. Consult it
before building each unit's artifact. **This file is not updated per-unit** — it is a fixed
template, not a running log. Colors are assigned fresh within each unit (see §1); which unit is
next is recovered from past chats, not tracked here.

> Note: this is a *reference* file, so it uses headers, tables, and code blocks freely.
> The no-headers/no-bullets rule applies only to the pre-read briefing and verse-by-verse
> commentary, which stay in flowing prose.

---

## 1. Color for Recurring Greek Roots — per-unit only

**Color consistency is per-unit, not cross-book.** Within a single unit's artifact, a given
tracked root gets one color and holds it throughout that artifact, and the legend explains each.
Colors do **not** carry across units — each unit reassigns hues freely to whatever serves that
unit's roots best. Pick distinct, legible hues for the roots that unit actually tracks, and watch
only for *within-unit* collisions (two roots near-identical in one artifact). There is no
cross-unit registry to maintain and nothing to update here after a unit ships.

(Earlier units, 1–2, tracked colors across the whole book; that requirement has been dropped.
The palette below is retained only as a convenient set of legible, parchment-friendly hues to
draw from — not as a binding root→color map. Reuse, reassign, or ignore it as the unit needs.)

### Reference palette (non-binding — a well of legible hues)

| Hex | Family | (Earlier use, FYI only) |
|---|---|---|
| `#a8324a` | crimson | gennaō — beget |
| `#1c7d70` | teal | kaleō — call / onoma — name |
| `#c0641a` | orange | sōzō — save / Iēsous — Jesus |
| `#4a4f93` | indigo | pneuma — Spirit |
| `#2f6db3` | blue | onar — dream / angelos — angel |
| `#8a3c70` | plum | meta — with / Emmanouēl — Emmanuel |
| `#8a6a2a` | gold | Dauid — David / basileus — king |
| `#6b2fb3` | violet | proskyneō — worship |
| `#3f7d3a` | green | paidion — child |
| `#455a6b` | slate | plēroō — fulfill |
| `#9c4f1c` | burnt brown | anachōreō — withdraw |
| `#9c2f8f` | magenta | basileia — kingdom |
| `#1f8f5f` | emerald | metanoeō — repent |
| `#0e8aa0` | cyan | baptizō — immerse |
| `#8a7a4a` | khaki | erēmos — wilderness |
| `#7a2230` | oxblood | peirazō — test |
| `#c0285f` | cerise | huios — Son |
| `#b07a1e` | amber-bronze | dikaiosynē — righteousness |

Within-unit collision sense: the purples (`#4a4f93` / `#6b2fb3` / `#8a3c70`) read fine apart but
should not crowd one artifact untweaked; likewise orange `#c0641a` vs burnt brown `#9c4f1c`, and
crimson `#a8324a` vs cerise `#c0285f`. If two needed roots land too close in one unit, push one
toward blue and one toward magenta (or just pick a different hue from the well).

---

## 2. The Reusable Stylesheet

Paste this whole `<style>` block verbatim into each unit's artifact, then set the root-color
classes to whatever that unit tracks (assign hues fresh per §1 — the vars below are a starting
palette, not fixed assignments). Fonts: **Cormorant Garamond** (display) + **EB Garamond** (body)
on a warm parchment ground.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#f5efe2;
    --panel:#fbf7ee;
    --panel-2:#f1e8d5;
    --ink:#2a2520;
    --ink-soft:#5c5347;
    --rule:#d8cdb6;
    --rule-soft:#e7dec9;
    /* === Greek-root colors — a starting palette; assign per-unit (§1) === */
    --c-beget:#a8324a;   /* genesis / gennaō */
    --c-name:#1c7d70;    /* kaleō / onoma   */
    --c-save:#c0641a;    /* sōzō / Iēsous  */
    --c-spirit:#4a4f93;  /* pneuma hagion    */
    --c-dream:#2f6db3;   /* onar / angelos kyriou */
    --c-with:#8a3c70;    /* meta / Emmanouēl */
    --c-david:#8a6a2a;   /* Dauid / basileus */
    --c-worship:#6b2fb3; /* proskyneō       */
    --c-child:#3f7d3a;   /* paidion         */
    --c-fulfill:#455a6b; /* plēroō          */
    --c-withdraw:#9c4f1c;/* anachōreō        */
  }
  *{box-sizing:border-box;}
  body{
    margin:0;
    background:
      radial-gradient(circle at 18% -5%, #faf5ea 0%, transparent 55%),
      radial-gradient(circle at 105% 102%, #ece2cc 0%, transparent 50%),
      var(--bg);
    color:var(--ink);
    font-family:"EB Garamond", Georgia, serif;
    font-size:19px;
    line-height:1.65;
    -webkit-font-smoothing:antialiased;
  }
  .wrap{max-width:790px;margin:0 auto;padding:56px 26px 120px;}

  a{color:inherit;text-decoration:none;border-bottom:1px dotted currentColor;}
  a:hover{border-bottom-style:solid;}

  /* ---- masthead ---- */
  header.mast{text-align:center;border-bottom:2px solid var(--ink);padding-bottom:26px;margin-bottom:8px;}
  .mast .kicker{letter-spacing:.32em;text-transform:uppercase;font-size:12.5px;color:var(--ink-soft);}
  .mast h1{font-family:"Cormorant Garamond",serif;font-weight:600;font-size:43px;line-height:1.05;margin:.18em 0 .12em;letter-spacing:.01em;}
  .mast .greek-title{font-size:21px;color:var(--c-david);font-style:italic;margin-bottom:.2em;}
  .mast .unit{font-family:"Cormorant Garamond",serif;font-size:19px;color:var(--ink-soft);font-style:italic;}

  /* ---- shared section frame (ALWAYS page-break-protected) ---- */
  section.block{background:var(--panel);border:1px solid var(--rule);border-radius:7px;padding:20px 24px;margin:30px 0;page-break-inside:avoid;break-inside:avoid;}
  section.block h2{font-family:"Cormorant Garamond",serif;font-size:16px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft);font-weight:600;margin:0 0 4px;}
  section.block .cap{font-style:italic;color:var(--ink-soft);font-size:15px;margin:0 0 16px;}

  /* ---- legend ---- */
  .legend ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:6px 26px;}
  .legend li{font-size:15.5px;line-height:1.4;}
  .swatch{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:8px;vertical-align:baseline;}
  .legend .r{font-style:italic;} /* the transliterated root itself carries its color + bold from .r + root-class */
  .legend .tag{font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);margin-left:6px;}
  @media(max-width:560px){.legend ul{grid-template-columns:1fr;}}

  /* ---- root spans: add a class per tracked root, pointing at its var ---- */
  .r{font-weight:600;}
  .beget{color:var(--c-beget);}
  .call{color:var(--c-name);}
  .save{color:var(--c-save);}
  .spirit{color:var(--c-spirit);}
  .dream{color:var(--c-dream);}
  .with{color:var(--c-with);}
  .king{color:var(--c-david);}
  .worship{color:var(--c-worship);}
  .child{color:var(--c-child);}
  .fulfill{color:var(--c-fulfill);}
  .withdraw{color:var(--c-withdraw);}
  .star{color:#9a7a12;font-style:italic;} /* "noted but not tracked" accent */

  /* ---- ring / triptych / concentric structure maps ---- */
  .ring{display:grid;grid-template-columns:1fr;gap:10px;}
  .ringrow{display:grid;grid-template-columns:42px 1fr;gap:14px;align-items:start;padding:9px 12px;border-radius:6px;background:var(--panel-2);}
  .ringrow.center{background:#efe4cb;border:1px solid var(--rule);}
  .ringrow .lab{font-family:"Cormorant Garamond",serif;font-weight:600;font-size:21px;color:var(--c-david);text-align:center;}
  .ringrow .lab small{display:block;font-size:11px;color:var(--ink-soft);letter-spacing:.06em;font-weight:400;}
  .ringrow .txt{font-size:15.5px;line-height:1.45;}
  .ringrow .ref{color:var(--ink-soft);font-style:italic;}

  /* ---- correspondence / comparison table ---- */
  table.exod{width:100%;border-collapse:collapse;font-size:15.5px;}
  table.exod th,table.exod td{padding:8px 10px;border:1px solid var(--rule);text-align:left;}
  table.exod th{background:var(--panel-2);font-family:"Cormorant Garamond",serif;letter-spacing:.08em;text-transform:uppercase;font-size:12.5px;color:var(--ink-soft);font-weight:600;}
  table.exod td.mt{color:var(--c-withdraw);font-weight:600;}
  table.exod td.eg{color:var(--ink-soft);}

  /* ---- itinerary / sequence chips ---- */
  .itin{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:6px 4px;}
  .itin .stop{font-family:"Cormorant Garamond",serif;font-size:17px;font-weight:600;padding:4px 11px;border-radius:20px;background:var(--panel-2);border:1px solid var(--rule);}
  .itin .arr{color:var(--ink-soft);font-size:15px;}
  .itin .stop sup{font-size:10px;color:var(--c-fulfill);font-weight:700;}

  /* ---- verses ---- */
  .verses{margin-top:40px;}
  .v{margin:0 0 14px;padding-left:42px;text-indent:-42px;line-height:1.7;}
  .v .n{display:inline-block;width:30px;text-indent:0;font-family:"Cormorant Garamond",serif;font-size:15px;color:var(--c-beget);font-weight:600;vertical-align:top;}
  .gloss{display:block;text-indent:0;margin:3px 0 14px 0;padding:6px 14px;border-left:2px solid var(--rule);color:var(--ink-soft);font-style:italic;font-size:15px;line-height:1.5;}
  sup.en{font-size:.62em;font-style:normal;color:var(--c-beget);font-weight:700;vertical-align:super;line-height:0;}
  sup.en a{border:none;}

  /* ---- compare box (transliterated Greek / NASB / Hart / Lattimore / text-form at contested verses) ---- */
  /* each row is its own grid line — label column + text column — so rows always stack and never run together */
  .compare{display:block;text-indent:0;margin:6px 0 14px 0;border:1px dashed var(--rule);border-radius:6px;background:var(--panel);padding:12px 16px;font-size:15px;page-break-inside:avoid;break-inside:avoid;}
  .compare .row{display:grid;grid-template-columns:112px 1fr;gap:4px 14px;align-items:baseline;margin:0;padding:5px 0;border-top:1px solid var(--rule);}
  .compare .row:first-child{border-top:none;padding-top:0;}
  .compare .src{font-variant:small-caps;letter-spacing:.05em;color:var(--ink-soft);font-style:normal;font-size:13.5px;}
  .compare .txt{line-height:1.5;}
  @media(max-width:520px){.compare .row{grid-template-columns:1fr;gap:1px;}}

  .translit{font-style:italic;}
  .tr{font-style:italic;color:var(--ink-soft);font-size:.92em;}

  /* ---- endnotes ---- */
  .notes{margin-top:48px;border-top:2px solid var(--ink);padding-top:18px;}
  .notes h2{font-family:"Cormorant Garamond",serif;font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft);font-weight:600;margin:0 0 16px;}
  .notes ol{margin:0;padding-left:26px;}
  .notes li{margin:0 0 15px;font-size:16px;line-height:1.55;}

  footer{margin-top:50px;text-align:center;font-size:13px;color:var(--ink-soft);font-style:italic;}
</style>
```

---

## 3. Component Snippets

Copy, fill in, done. All structural/visual blocks live inside `<div class="wrap">`.

### Masthead
```html
<header class="mast">
  <div class="kicker">The Gospel According to Matthew · Study Translation</div>
  <h1>UNIT TITLE</h1>
  <div class="greek-title">Transliterated title — <span style="font-style:normal;font-size:.8em;color:var(--ink-soft)">"plain-English gloss"</span></div>
  <div class="unit">Unit N · Matthew C:V–V · short descriptor</div>
</header>
```

### Color legend (every tracked root in this unit gets a row)
```html
<section class="block legend" aria-label="color key">
  <h2>Recurring Greek roots — color key</h2>
  <p class="cap">The roots tracked in this unit (transliterated only) and the color each holds throughout the artifact.</p>
  <ul>
    <li><span class="swatch" style="background:var(--c-beget)"></span><span class="r beget">gennaō</span> — "beget"</li>
    <!-- one <li> per tracked root in THIS unit. The word itself is colored via .r + its root class (same
         class used in the verse text), so the key doesn't rely on the swatch dot alone. -->
  </ul>
</section>
```

### Concentric / ring / triptych map (use `center` on the pivot row)
```html
<section class="block">
  <h2>TITLE — a concentric ring · C:V–V</h2>
  <p class="cap">one-line description of what the structure shows</p>
  <div class="ring">
    <div class="ringrow"><div class="lab">A<small>v–v</small></div><div class="txt">… <span class="ref">— gloss</span></div></div>
    <div class="ringrow center"><div class="lab">B<small>v–v</small></div><div class="txt">center / pivot</div></div>
    <div class="ringrow"><div class="lab">A′<small>v–v</small></div><div class="txt">… <span class="ref">— gloss</span></div></div>
  </div>
</section>
```

### Correspondence table (typology, Synoptic divergence, OT↔NT pairing)
```html
<section class="block">
  <h2>TITLE</h2>
  <p class="cap">caption</p>
  <table class="exod">
    <tr><th>Left column</th><th>Right column</th></tr>
    <tr><td class="eg">source side</td><td class="mt">Matthew side (colored)</td></tr>
  </table>
</section>
```

### Itinerary / sequence chips (good for geography or citation chains)
```html
<div class="itin">
  <span class="stop">Place <sup>Prophet</sup></span><span class="arr">→</span>
  <span class="stop">Place <sup>Prophet</sup></span>
</div>
```

### A verse + inline gloss
```html
<p class="v"><span class="n">12</span>English of the verse, with a <span class="worship r">tracked root</span> colored and an endnote<sup class="en"><a href="#n3">3</a></sup>.</p>
<span class="gloss">Short contextual gloss in italics, sits directly beneath the verse.</span>
```

### Compare box (contested verses only)
```html
<div class="compare">
  <div class="row"><span class="src">Greek (translit.)</span><span class="txt translit">…transliterated phrase…</span></div>
  <div class="row"><span class="src">NASB</span><span class="txt">rendering for comparison</span></div>
  <div class="row"><span class="src">Hart</span><span class="txt">or Lattimore where illuminating</span></div>
  <div class="row"><span class="src">Text-form</span><span class="txt">MT vs LXX note when relevant</span></div>
</div>
<!-- each .row is a label-column + text-column grid line (see §2 CSS) — rows always stack cleanly,
     the label never collides with the text, and there's no native Greek script, only transliteration -->
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

### Footer
```html
<footer>Translation rendered from the SBLGNT Greek of Matthew C:V–V · Unit N of the Matthew study · wooden to the Greek by design</footer>
```

---

## 4. Conventions Checklist (run before shipping each artifact)

- [ ] **Every structural block** (`section.block`, `.compare`) has `page-break-inside:avoid` + `break-inside:avoid`. No chart, table, ring, or compare box may split across a page.
- [ ] **Plural "you" → "y'all"** everywhere in the translation (e.g. 2:8 "when y'all find him").
- [ ] **Transliteration only — no native Greek script anywhere** (masthead, legend, verse text, compare boxes, endnotes). On first use of a tracked term *in this unit*, give the transliteration plus a plain-English gloss: `sarx` ("flesh"). After that first gloss, the bare transliteration (`.translit` class; colored via `.r` + root class where tracked) can recur through that unit's artifact — but never assume a gloss carries over from a *prior* unit; reintroduce it there too.
- [ ] **Same Greek root → same English root** across verses, even when it reads repetitively. That repetition is the point.
- [ ] **Same Greek root → same color** *within this unit's artifact*, and every tracked root has a legend row. Colors are assigned fresh per unit (§1); no cross-unit registry to match.
- [ ] **Verses readable alone.** Glosses, notes, compare boxes are additive, never load-bearing.
- [ ] **Compare box only at genuinely contested verses** where the translation choice does real work. Include NASB; bring in Hart or Lattimore where their rendering is provocative or illuminating.
- [ ] **Hyperlinks** for significant LXX/OT citations and key terms — biblehub for OT verses, Logeion for lexis, NETS for LXX text-form, Qumran/earlyjewishwritings for Second Temple.
- [ ] **Chiasms/concentric structures mapped visually** in a `.ring` block, not just described.
- [ ] **Repeated-word counts** noted only when the frequency is theologically significant (3, 7, 10, 12, 40, 70…).
- [ ] Artifact saved to `/mnt/user-data/outputs/matthew_NN_translation.html` (zero-padded unit number), then `present_files`. (No log to update afterward — this file stays fixed.)

### Chat-side conventions (commentary, not artifact)
- Pre-read briefing and verse-by-verse: **flowing prose only** — no bullets, no headers, no bold, no markdown.
- Confirm scope before each walkthrough; flag where chapter divisions and literary seams diverge; flag the five discourses (5–7, 10, 13, 18, 23–25) as multi-chapter units when they arrive.
- Hold Constable in active dialogue with France, Wright, Bible Project teacher notes, Jewish/Second Temple/rabbinic voices, and Chrysostom — don't let the dispensationalist frame stand unchallenged.
- Flag rabbit holes (deep intertextual territory, major debates, extended structural work) and ask whether to go deeper or keep moving.

---

## 5. Most-Used Reference URLs (distilled from matthew_reference_links.md)

Quick-grab subset for artifact hyperlinks and routine lookups. Full annotated list lives in
`matthew_reference_links.md`.

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
(historical), Bauckham, Amy-Jill Levine (Jewish readings). Bible Project teacher notes
(`rise-of-the-messiah-teacher-notes.pdf`, `messianic-torah-teacher-notes.pdf`) for the
literary-canonical frame; Constable (`matthew.pdf`) for traditional/dispensationalist, to be
balanced.

---

## 6. Finding the next unit

This file is **not** a running log and is not edited per-unit. To find which unit is next when
Lane hasn't said, search past chats (`conversation_search` / `recent_chats`) for the most recent
unit shipped, then take the following row from the Literary Unit Map (§7). The map below is the
fixed plan of record: passages and seams are settled; the titles are working titles and may be
refined when a unit is actually built. Roots and colors are decided fresh per unit (§1) and are
not recorded here. Do not track which units have shipped in this file — that list goes stale
immediately; recover it from past chats every time.

---

## 6a. Live cross-unit threads

Threads opened in one unit's commentary that are meant to pay off in a *later* unit (e.g. a
keyword planted early that resurfaces, an inclusio spanning several units, a hinge matched by a
later hinge). These are **tracked in project memory**, not listed here — keeping them in one place
avoids a list in this file drifting out of sync with what's actually been opened. When a thread's
payoff unit arrives, close the loop in that unit's commentary and update the memory; add new
threads to memory as they open.

---

## 7. Literary Unit Map (full gospel)

The plan of record for how Matthew is divided for this study. Twenty-eight units, each *roughly*
chapter-length, but cut along Matthew's own literary seams rather than the medieval chapter
divisions. Where a unit's boundary diverges from a chapter boundary, the divergence is flagged
and the reason given. Confirm scope against this map before each walkthrough.

### 7.1 The structural skeleton Matthew built in

Four converging structural signals define the seams. They do not compete so much as layer, and
the unit divisions below try to honor all four at once.

**(a) The two *apo tote* ("from that time") hinges (Kingsbury).** Twice Matthew writes *Apo tote
ērxato ho Iēsous* ("From that time Jesus began to…"), at **4:17** and **16:21**, and each time the verb that
follows turns the whole story:
- 4:17 — *began to proclaim*: "Repent, for the kingdom of the heavens has drawn near."
- 16:21 — *began to show*: that he must go to Jerusalem, suffer, be killed, and be raised.

This carves the gospel into three movements: **the person of the Messiah (1:1–4:16)**, **the
proclamation in Galilee (4:17–16:20)**, and **the road to the cross (16:21–28:20)**. France's
"drama in three acts" (Galilee → journey → Jerusalem) maps onto the same skeleton.

**(b) The five discourse formulas (Bacon).** Five times Matthew closes a teaching block with
*kai egeneto hote etelesen ho Iēsous* ("And it came about when Jesus finished…"), at **7:28,
11:1, 13:53, 19:1, 26:1**, marking the five great discourses: the Sermon on the Mount (5–7),
the Mission charge (10), the Kingdom parables (13), the Community discourse (18), and the
Woes + Olivet discourse (23–25). Bacon read these as a "new Pentateuch," Jesus as the new Moses
delivering a new Torah from a mountain — the Bible Project's "Messianic Torah" frame.

**(c) Mackie / Bible Project macro-design** (from `rise-of-the-messiah-teacher-notes.pdf`)
fuses (a) and (b): an **Introduction (1:1–4:17)** and matching **Conclusion (26:1–28:20)**, each
saturated with formula quotations (7+3 / 7), framing a **three-part body (4:17–25:46)** —
Kingdom *established* (4:17–11:1), Kingdom *resisted* (11:2–16:20), Kingdom *confronts Jerusalem*
(16:21–25:46) — with a discourse seated in each part. This is the lens of record for the study.

**(d) Davies & Allison's triads + the great inclusio.** Allison finds Matthew composing in
threes at every scale (three sets of fourteen in the genealogy, three temptations, triads of
miracles in 8–9, three parables of judgment in 21–22, etc.); read units with an eye for the
pattern of three. And the whole book is bracketed by an **Emmanuel inclusio** — *meth' hēmōn ho
theos* "God with us" (1:23) answered by *egō meth' hymōn eimi* "I am with y'all" (28:20) — the `with`
root (*meta* / *Emmanouēl*, "with-us") is load-bearing across the entire gospel — worth coloring
in any unit where it surfaces, though the specific hue is chosen per unit.

### 7.2 The twenty-eight units

Format: **Unit — passage — title.** Rationale notes the seam honored and any divergence from
the chapter grid. "Watch across the seam" flags inclusios/triads that span a unit boundary and
should be read together even though the units are studied apart.

**MOVEMENT ONE — The Person of the Messiah (1:1–4:16/17).** *The origin, identity, and
authentication of Jesus before he speaks a public word.*

- **Unit 1 — 1:1–25 — The Book of the Genesis.** ✅ Genealogy + birth. Whole of ch. 1.
- **Unit 2 — 2:1–23 — Out of Egypt I Called My Son.** ✅ Magi, flight, Nazareth. Whole of ch. 2.
  *(Units 1–2 together = the infancy narrative 1:1–2:23; split at the chapter for length.)*
- **Unit 3 — 3:1–4:11 — Wilderness, Water, Wilderness.** John the Baptist, the baptism, the
  temptation. **Diverges from the chapter grid:** runs past 3:17 to 4:11 because John → baptism →
  testing is one continuous wilderness/Jordan movement bound by Spirit, sonship, and the
  Deut/Israel-in-the-desert backdrop; the seam falls at 4:11 (end of the testing), not at the
  3/4 chapter line. Constable likewise ends his "preparation" block at 4:11.
- **Unit 4 — 4:12–25 — The Light Has Dawned.** ✅ Withdrawal to Capernaum + Isaiah 9 light
  quotation, call of the four, the programmatic ministry summary (4:23). **Short (14 vv) and it
  straddles the 4:17 hinge** — i.e. this unit sits exactly on the seam between the
  Introduction and the body, which is itself worth dwelling on. *(Scoping resolved: built as a
  stand-alone overture. The old "fold into Unit 3" option is moot — Unit 3 already runs through
  4:11; verse boundaries are settled at 4:12–25.)*

**MOVEMENT TWO — The Kingdom Proclaimed in Galilee (4:17–16:20).**

*Part A — Kingdom established in word and deed (4:17–11:1).*

- **Unit 5 — 5:1–48 — The Greater Righteousness.** Beatitudes, salt & light, and the six
  contrasts ("you heard it said… but I say"). Whole of ch. 5.
- **Unit 6 — 6:1–34 — Before Your Father Who Sees.** The three acts of piety (alms/prayer/
  fasting) with the Lord's Prayer at the concentric center, then treasure, the eye, mammon, and
  anxiety. Whole of ch. 6.
- **Unit 7 — 7:1–29 — The Two Ways.** Judging, the holy and the pearls, ask/seek/knock, the
  Golden Rule, and the eschatological pairs (two gates, two trees, two builders) + the crowd's
  astonishment and discourse formula (7:28). Whole of ch. 7.
  - ⚑ **Discourse 1 = the Sermon on the Mount (5:1–7:29) is one three-chapter unit** split here
    into three roughly-chapter units. **Watch across the seam:** the *Law and the Prophets*
    inclusio frames the whole body of the Sermon — opened at **5:17** ("I did not come to abolish
    the Law or the Prophets") and closed at **7:12** ("this is the Law and the Prophets"). The
    6:1–18 piety triad is a self-contained concentric panel, and the movement 6:19–7:12 arguably
    runs *across* the 6/7 chapter line. *Open scoping question:* default split is 5 / 6 / 7
    (chapter-length, defensible); the more literary alternative is 5:1–48 / 6:1–7:12 / 7:13–29.
    Confirm with Lane when we reach the Sermon.
- **Unit 8 — 8:1–34 — The Deeds of the Messiah (I).** Leper, centurion, Peter's mother-in-law +
  healing summary, would-be followers, the stilling of the storm, the Gadarene demoniacs. Whole
  of ch. 8.
- **Unit 9 — 9:1–34 — The Deeds of the Messiah (II).** Paralytic, call of Matthew, the question
  about fasting, Jairus's daughter + the hemorrhaging woman, two blind men, the mute demoniac.
  Whole of ch. 9 *minus* the harvest summary. **Watch across the seam:** chs. 8–9 form one
  ten-miracle deed-block (Davies & Allison: three triads with discipleship/controversy
  interludes) answering the words of chs. 5–7 — read 8–9 as a single "deeds" arc.
- **Unit 10 — 9:35–11:1 — The Sending (Discourse 2).** The harvest/compassion summary
  (9:35–38) as the narrative on-ramp, then the Mission charge, closed by the formula at 11:1.
  **Diverges from the chapter grid:** starts at 9:35 (the harvest belongs with the sending, not
  with the ch. 9 miracles) and runs to 11:1.

*Part B — Kingdom meets growing hostility (11:2–16:20).*

- **Unit 11 — 11:2–30 — Are You the Coming One?** John's question from prison, Jesus on John,
  the woes on the unrepentant towns, and the great invitation ("Come to me… I am gentle and lowly").
  Runs 11:2–30 (11:1 belongs to the prior unit's formula).
- **Unit 12 — 12:1–50 — Lord of the Sabbath, Servant of the Lord.** The two Sabbath conflicts,
  the Isaiah 42 Servant quotation, the Beelzebul controversy, the sign of Jonah, the return of
  the unclean spirit, the true family. Whole of ch. 12 — the hostility crests here.
- **Unit 13 — 13:1–53 — The Parables of the Kingdom (Discourse 3).** Sower through the
  householder's treasure; the structural pivot from public crowds to private disciples; closed by
  the formula at 13:53. Whole of the discourse (essentially ch. 13).
- **Unit 14 — 13:54–14:36 — Rejection, a Beheading, Bread, and the Sea.** Rejection at Nazareth,
  Herod and the death of John, the feeding of the 5,000, the walking on the water, Gennesaret.
  **Diverges from the chapter grid:** starts at 13:54 (right after the parables formula) and runs
  through ch. 14; the seam is the formula at 13:53, not the 13/14 line.
- **Unit 15 — 15:1–39 — Clean and Unclean; Bread for the Dogs.** The tradition/defilement
  controversy, the Canaanite woman, the feeding of the 4,000. Whole of ch. 15, unified by
  clean/unclean and bread, and by the Israel→nations movement.
- **Unit 16 — 16:1–20 — On This Rock.** The demand for a sign, the leaven of the Pharisees and
  Sadducees, Peter's confession at Caesarea Philippi. Ends at **16:20** — the climax of Movement
  Two, immediately before the 16:21 hinge.

**MOVEMENT THREE — The Road to the Cross (16:21–28:20).**

*Part A — The journey: suffering foretold, Jerusalem approached (16:21–20:34).*

- **Unit 17 — 16:21–17:27 — The Road to the Cross Begins; Transfigured.** First passion
  prediction (at the 16:21 hinge), "take up your cross," the Transfiguration, the boy healed at
  the mountain's foot, the second passion prediction, the temple tax. **Diverges from the chapter
  grid:** opens at the 16:21 hinge and runs through ch. 17.
- **Unit 18 — 18:1–35 — Life in the Community (Discourse 4).** Greatness as a child, the little
  ones, the lost sheep, reproof in the *ekklēsia* ("assembly/church"), unlimited forgiveness, the unforgiving servant;
  closed by the formula at 19:1. Whole of ch. 18.
- **Unit 19 — 19:1–30 — Leaving Galilee: Marriage, Children, Riches.** The departure from
  Galilee (19:1–2 doubles as the discourse formula), divorce and celibacy, the children, the rich
  young man, "the first/last." Whole of ch. 19.
- **Unit 20 — 20:1–34 — The Last Shall Be First.** The laborers in the vineyard, the third
  passion prediction, the sons of Zebedee, the two blind men at Jericho. Whole of ch. 20.
  **Watch across the seam:** the vineyard parable (20:1–16) is bracketed with 19:30 by the
  "first/last" inclusio (**19:30** "many first will be last" / **20:16** "the last first, the
  first last") — read 19:16–20:16 as one money-and-reversal arc.

*Part B — Jerusalem: confrontation in the temple (21:1–25:46).*

- **Unit 21 — 21:1–46 — The King Enters; the Temple Judged.** Triumphal entry, the temple
  action, the cursed fig tree, the challenge to Jesus' authority, the parable of the two sons,
  the parable of the tenants. Whole of ch. 21.
- **Unit 22 — 22:1–46 — The Banquet and the Four Questions.** The wedding banquet, then the four
  controversy dialogues (tax, resurrection, greatest commandment, David's son). Whole of ch. 22.
  **Watch across the seam:** the three judgment parables run **21:28–22:14** (two sons → tenants
  → banquet), closing on "many called, few chosen" — read the triad together across the 21/22 line.
- **Unit 23 — 23:1–39 — Seven Woes and a Lament.** The indictment of the scribes and Pharisees
  (seven woes) and the lament over Jerusalem. Whole of ch. 23.
- **Unit 24 — 24:1–51 — The Olivet Discourse (I): Temple and Son of Man.** The temple's fall
  foretold, the birth-pangs, the abomination, the coming of the Son of Man, the fig tree, "this
  generation," and the first watchfulness parables. Whole of ch. 24.
- **Unit 25 — 25:1–46 — The Olivet Discourse (II): Three Parables of the End (Discourse 5).**
  Ten virgins, the talents, the sheep and the goats; closed by the formula at 26:1. Whole of ch. 25.
  - ⚑ **Discourse 5 spans 23:1–25:46 in the Mackie/Bible Project scheme** (woes + Olivet as one
    block), split here into Units 23–25. Note the live debate over whether ch. 23 belongs *with*
    the Olivet Discourse or stands as a separate woe-oracle, with 24–25 as the discourse proper —
    flag this when we arrive. Like the Sermon, this is a multi-chapter discourse needing extra
    scoping care.

*Part C — Conclusion: Death, Resurrection, Commission (26:1–28:20).*

- **Unit 26 — 26:1–75 — The Night of Betrayal.** Plot, the anointing at Bethany, Judas's
  bargain, the Last Supper, Gethsemane, the arrest, the Sanhedrin trial, Peter's denial. Whole of
  ch. 26. **Long (75 vv)** — coherent as "the night," but a candidate to split (e.g. 26:1–46 /
  26:47–75) if it runs heavy; confirm with Lane.
- **Unit 27 — 27:1–66 — The Crucifixion.** Handover to Pilate, the death of Judas, Barabbas, the
  mockery, the crucifixion, the death with its signs (darkness, torn veil, earthquake, raised
  saints), the burial, the guard at the tomb. Whole of ch. 27.
- **Unit 28 — 28:1–20 — The Mountain of Commission.** The empty tomb and the women, the guards'
  cover-up, the Great Commission on the mountain. Whole of ch. 28. **Watch across the whole book:**
  closes the **Emmanuel inclusio** (28:20 "I am with y'all always" ↔ 1:23 "God with us") and the
  mountain frame (testing-mountain 4 / teaching-mountain 5 / commission-mountain 28).

### 7.3 Divergences from the chapter grid, at a glance

Units that do **not** equal a single chapter, and why:

| Unit | Passage | Why it's cut here, not at the chapter line |
|---|---|---|
| 3 | 3:1–4:11 | John + baptism + testing = one wilderness movement; seam is 4:11 |
| 4 | 4:12–25 | overture to the public ministry; straddles the 4:17 hinge (short) |
| 9 | 9:1–34 | the 9:35–38 harvest summary is pulled forward into the Mission unit |
| 10 | 9:35–11:1 | Mission Discourse + its harvest on-ramp + closing formula |
| 11 | 11:2–30 | starts after the 11:1 formula |
| 14 | 13:54–14:36 | starts after the 13:53 parables formula; runs across 13/14 |
| 16 | 16:1–20 | ends at 16:20, just before the 16:21 hinge |
| 17 | 16:21–17:27 | opens at the 16:21 hinge; runs across 16/17 |

Inclusios/triads to read *across* unit seams: **5:17↔7:12** (Law & Prophets, Units 5–7),
**19:30↔20:16** (first/last, Units 19–20), **21:28–22:14** (three judgment parables, Units 21–22),
**1:23↔28:20** (Emmanuel, Units 1 & 28).

### 7.4 The five discourses (extra-scope flags)

When these arrive, flag the multi-chapter scope and confirm the split before building:
- **Discourse 1 — Sermon on the Mount (5–7)** → Units 5, 6, 7. Heavy rabbit-hole risk.
- **Discourse 2 — Mission (10)** → Unit 10 (with 9:35–38 on-ramp).
- **Discourse 3 — Kingdom Parables (13)** → Unit 13.
- **Discourse 4 — Community (18)** → Unit 18.
- **Discourse 5 — Woes + Olivet (23–25)** → Units 23, 24, 25. Heavy rabbit-hole risk.
