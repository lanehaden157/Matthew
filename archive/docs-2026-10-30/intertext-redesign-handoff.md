# Handoff for Claude Code: make the Matthew intertext pass scene-based and put it in the artifact

From Lane, via the chat/project side. Date: 2026-10-20.
Pilot unit: Unit 14 (Matthew 13:54–14:36), already shipped as `matthew_14_translation.html`.

## 0. What Lane asked for, in his words

After the scene-by-scene intertext walkthrough of Unit 14 (Herod's birthday feast beside Pharaoh's birthday feast in Gen 40, and the rest of those OT and NT parallels with background on each original story), Lane said that is exactly the intertext pass he wants. He wants those parallels always in the verse-by-verse and integrated into the artifact often. He asked why the current pass 3 doesn't produce it, and for changes to instructions, structures and style sheets so future units do.

Read-first caveat: I (chat side) could read the project-synced `core-workflow.md`, `matthew_study_style_reference.md`, `components-reference.md`, `canon-decisions.md`, `synced-index.md` and the canon-leads sheets. I did NOT read `css/styles.css`, the chat-side `instructions.md`, `pipeline/canon_leads.py`, `pipeline/port_artifact.py`, `pipeline/build.py`, or how `intertext[]`/`typescenes[]` in the meta block are validated and rendered. Everything below that touches those is a proposal to verify against the real code.

## 1. Diagnosis: why the current pass 3 doesn't produce what Lane liked

1. **The pass starts from a word search and is organised around it.** Pass 3 begins at `canon-leads-unit-NN.md`, and the first strong suggestion is "every lead on the sheet gets a row." The sheet is rare-word and two-word-phrase matches only. It cannot see common words, themes, type-scenes, or Mark/Luke. The best Unit 14 links were exactly the things it cannot see: the Gen 40 birthday feast, Elisha's twenty loaves (2 Kgs 4), "stand firm and see the salvation" (Exod 14:13), Jezebel and Elijah, Jephthah, the burial of Ish-bosheth's head (2 Sam 4), Moses withdrawing in fear (Exod 2), Job 9:8, Ps 69. The workflow admits the blind spot ("the pass starts there but doesn't end there") but makes the non-mechanical sweep a loose suggestion ("central people, places and objects get a web search"), not a required step with its own output.
2. **The unit of analysis is the link, not the scene.** The ledger has one row per link: verse, target text, kind, evidence, strength, verdict. A row has no place for the original story, for what is the same and different, or for what the echo does in Matthew. Those are what make Lane's example land. "Herod's feast is Pharaoh's birthday feast" matters because of the Gen 40 story (a birthday feast, a head, a baker hanged, a cupbearer restored) and the contrast with the wilderness meal, not because two Greek words match.
3. **The verdict vocabulary has no slot for a scene-level parallel.** The only outputs are root `echo` (one line in a popover), `aside.echo`, OT citation pointer (quotations only), footnote, or drop. The style reference says an echo should "lead with the reference, then say in one short clause what it adds," and it sits behind the shared note (`*`) toggle with the gloss. The footnote is the only long-form place, and it lands at the end of the unit, detached from the verse. So a rich parallel either gets squeezed to a clause or ends up in an endnote nobody reads.
4. **The culling target rewards short lists.** "A typical unit considers fifteen to thirty links and keeps six to twelve." The Unit 14 keep rate was 16 of 42, and most of what was dropped were word-only leads. Fine as a hygiene rule, but nothing pushes the other direction (a required scene-level parallel per pericope).
5. **The artifact's design philosophy makes intertext optional by construction.** "Verses read on their own; glosses, notes, compare boxes are additive, never load-bearing," plus hiding echoes and synoptic parallels behind chips. That is right for glosses. It means the intertext, which is the project's stated primary lens ("intertextuality first"), is always the thing you have to click to see.
6. **Pass 3 is a separate turn and a table.** Intertext is deferred out of pass 2 into its own turn, and the deliverable is a table. A table is a research audit shape. Lane listens to these (he has the findings read aloud), and a table with verse numbers, references and Greek is unlistenable. The scene walk he liked is ordered by scene, gives background first, and is spoken prose.
7. **Registries are too thin to hold scene links.** `canon-decisions.md` lists six type-scenes (commissioning, scouts, water-crossing, census, mountain-theophany, annunciation). The birthday feast, wilderness feeding, prophet's death at a king's hands, sea-walking and the like have nowhere to be recorded, and `intertext[]`/`typescenes[]` seem to be harvested into `data/canon.json` (verify).

Net: the system is built to record verified word-level links compactly. Lane wants story-level parallels with background and function, shown in the reading. Those need a different unit of analysis, a different component, and a different default visibility.

## 2. Proposed changes

Where an edit goes matters: `core-workflow.md` is vendored from `bible-core/canon/workflow.md` ("Don't edit the book's copy"), and the project instruction field wins for Matthew. So put the Matthew override in the project instruction field now, and propose the general version upstream to `bible-core/canon/workflow.md` so other books can opt in.

### 2.1 Pass 3 redesign (project instruction field + upstream workflow)

Replace the ledger-first pass with two layers, in this order:

**3a. Scene sweep (required, per pericope, before opening the leads sheet).** For each pericope, answer in writing:
- Who are the people, places and objects here, and where have they appeared before (OT, LXX, Second Temple, elsewhere in the NT)?
- What type-scene or story pattern is this (feast, hand-off of a head, feeding in want, crossing water, withdrawal in fear, rejection of a prophet at home, and so on)?
- What is the nearest earlier story that has the same shape? Name it, tell it in two to four plain sentences, and say what is the same and what is different.
- Where does the line come back later (the NT, and where it matters, Second Temple or rabbinic or patristic reception)?
- What does the match do in Matthew's telling (irony, reversal, identification, fulfilment, warning)?
Search the web for each central person, place and object, as the workflow already half-says. Read the target text before logging a link. Mark each as strong, possible or weak.

**3b. Word leads (secondary).** Run `canon-leads-unit-NN.md` against what 3a already found: every lead still gets a row; leads that fall inside a 3a parallel are attached to it as evidence rather than judged alone.

**Deliverables from pass 3, two forms:**
- **Listenable scene walk (in chat).** Ordered by scene. Per scene: the Matthew line in plain words, then the earlier story (background first), then what matches, what differs, and what it does. No verse numbers, no references, no Greek, no tables; names spoken as a person would say them ("the book of Genesis" not "Gen 40:20"). This is what Lane has read aloud.
- **Ledger file (for Lane's marking and for the artifact).** One row per parallel, with these columns: unit-anchor verse, source ref, kind, source story (2 to 4 sentences), what matches, what differs, what it does in Matthew, evidence/where found, strength, verdict. Rejected rows stay. Delivered as a file, not pasted into chat.

Pause after pass 3 as now. Lane marks keeps.

### 2.2 New verdict and component: the scene parallel

Add a sixth verdict, `parallel` (alongside root `echo`, `aside.echo`, OT pointer, footnote, drop). Use it whenever a link has a source story worth telling. Keep `aside.echo` for one-clause connections and root `echo` for word histories.

Proposed markup (Code to adjust to the real component system):

```html
<aside class="parallel" data-anchor="14:6" data-kind="type-scene" data-strength="strong">
  <h4 class="par-head">
    <span class="par-label">Earlier story</span>
    <span class="par-ref">Gen 40:20–22</span>
    <span class="par-title">Pharaoh's birthday feast</span>
  </h4>
  <p class="par-hook">One-line hook that is always visible.</p>
  <div class="par-body">
    <p class="par-story">Two to four plain sentences retelling the source story.</p>
    <ul class="par-match"><li>…what matches…</li></ul>
    <p class="par-diff"><b>Different:</b> …</p>
    <p class="par-does"><b>In Matthew:</b> …</p>
    <p class="par-later">Later reuse, only if there is one.</p>
  </div>
</aside>
```

Rules to propose:
- Following sibling of the verse (or of the last verse of the scene it covers), same rule as `.gloss`/`.echo`; `data-anchor` must match the verse it follows, and the build checks it. Optional `data-span="14:3–12"` if a scene range is wanted.
- **Visible by default, hook plus header; body collapsible** (open/closed state remembered per viewer in a try/catch-wrapped localStorage, but the page must render fully with it empty). This reverses "hidden behind a chip" for parallels only. Everything else keeps its chip.
- Translit only, no Greek or Hebrew script, no `data-root`/`class="r"`/`class="rl"` inside it (same as `aside.echo`). No named commentators from unit 13 on (existing rule). No "cf." in the text; the CSS supplies the label.
- Fields required by the build: `data-anchor`, `data-kind` (type-scene | story | allusion | reuse | reception), `data-strength` (strong | possible), a `par-ref`, a `par-hook`, and a `par-diff` (no parallel ships without a stated difference; this guards against over-claiming). `weak` is never shipped as a parallel; it stays in the ledger or becomes a footnote.
- No numeric cap. Replace the "6 to 12 kept" norm with a floor and a quality bar: every pericope carries at least one `parallel`, or a recorded "swept, none found" line in `unit-meta` (see 2.3) so the omission is a decision and not an oversight.
- Keep the existing 0 to 3 limit for `aside.synoptic`; they are a different thing (the same story told by Mark, Luke or John).

### 2.3 `unit-meta` additions

Add to the unit-meta block:
- `parallels[]`: `{id, anchor, source_ref, kind, strength, title}` so the site and `data/canon.json` can index parallels the way `aside.echo` is harvested today. (Verify how `intertext[]`/`typescenes[]` are validated before inventing a new key; reuse them if they fit.)
- `sweep[]`: per pericope, `{pericope, status: "parallels" | "none-found", note}`. The audit uses this to enforce the floor.

### 2.4 Style reference edits (`matthew_study_style_reference.md`)

- **§1a:** add a paragraph on the three tiers: root `echo` (word), `aside.echo` (one-clause), `parallel` (scene-level story with background). Say how to choose. Change "lead with the reference, then one short clause" to apply to root `echo` and `aside.echo` only.
- **§3:** add "Scene parallel (`aside.parallel`)" with the markup and rules above, next to the existing `aside.echo` section.
- **"Verses read on their own… never load-bearing" (§4 checklist):** keep it for glosses, but add a carve-out: parallels are part of the reading; the verse text must still stand alone, but a pericope is not complete without its parallel.
- **§4 checklist, new items:**
  - Every pericope has at least one `aside.parallel`, or a `sweep[]` "none-found" entry with a note.
  - Every `parallel` has a source story, a stated difference, and a "what it does in Matthew" line.
  - Parallels are anchored to the right verse and use the verse text's own wording for anything quoted.
  - Strength is `strong` or `possible` only; nothing weak ships as a parallel.
- Flag the existing §3 vs §4 inconsistency on endnote-marker placement inside a gloss span (spotted in Unit 14); Lane hasn't ruled.
- Note in the style reference that this change was made at Lane's request on 2026-10-20 and why, per the file's own convention of dated rulings.

### 2.5 `css/styles.css`

Add `.parallel` styles (verify what variables exist and reuse them):
- Visually distinct from `.gloss`, `.echo`, `.synoptic` (suggest a left rule in a neutral accent, a small-caps "Earlier story" label, the `par-ref` in a monospace or small caps).
- Hook always shown; `.par-body` collapsible with a toggle (a `<details>`-style or JS toggle that degrades to open if JS is missing).
- Light and dark safe; no hard-coded colours.
- Mobile first: no horizontal scroll, readable at phone width, body text same size as `.gloss` or larger.
- Print: expand all bodies.
- Make sure the existing "shared note (`*`) toggle" logic does not swallow `.parallel` and that `aside.echo` keeps working.
- Scene-range anchors: if `data-span` is supported, draw a thin bracket or label so the reader sees which verses it covers.

### 2.6 Pipeline

- **`canon_leads.py`:** add a second output, a per-pericope "scene sweep sheet" generated from the word table: every proper noun, and every narrative noun (head, platter, feast, birthday, bread, loaves, fish, boat, sea, mountain, wilderness, grass, wind) regardless of the 20-verse rare cutoff, with its first LXX occurrence and its occurrences in the other gospels (Mark/Luke/John files exist on the project side). It isn't a judgment, but it hands pass 3a candidates the rare-word cutoff hides. Also add Mark, Luke and John to the cross-reference corpus, which the current sheet omits. Verify whether the Synoptic comparison path already covers part of this.
- **`port_artifact.py` / audit:** validate `aside.parallel` (anchor matches, required child classes present, no script, no `data-root` inside, strength in the allowed set); warn when a pericope has no parallel and no `sweep[]` none-found entry; harvest parallels into `data/canon.json`.
- **`build.py`:** render the `parallels[]` index if the site has a canon page; no change otherwise.
- **Registries:** extend `canon/typescenes.json` (and `canon-decisions.md` by Lane's say) with the scene types Unit 14 surfaced, e.g. royal-birthday-feast, prophet-killed-by-a-court, feeding-in-want, crossing-water-by-night/rescued-in-the-sea, withdrawal-in-fear. Ask Lane before adding to the shared canon file.

### 2.7 Project instruction field (Matthew), concrete edits

Add a "Pass 3 differs for Matthew" bullet: sweep by scene first, ledger columns, listenable chat walk, ledger as a file, new `parallel` verdict, floor of one per pericope. Update the existing line "Pass 3 verdicts are a root `echo`, an `aside.echo`, an OT citation pointer…, a footnote, or drop" to include `parallel`. Add: "Pass 2 notes any type-scene or story parallel as it goes, so pass 3 starts with candidates instead of a blank page" (that is the fourth and sixth standing moves, strengthened). Keep the existing transliteration-only, no-commentator-names-in-artifact and y'all/sky/Master/Immerser rules unchanged.

Per the instruction field's own rule, since this touches the style reference's artifact rules, flag the conflict to Lane for a ruling instead of picking one: the new always-visible component departs from the "additive, hidden" philosophy.

### 2.8 Pass 2 integration

Lane also asked for the parallels "in the verse by verse." Add to the pass-2 instructions that when a verse or scene has a clear earlier-story shape, pass 2 gives it a short flowing-prose mention (a sentence or two, no refs), and pass 3 develops it. This keeps the verse-by-verse and the intertext pass from splitting the same material.

## 3. Pilot: apply to Unit 14

The Unit 14 scene walk Lane liked is the template. Suggested pilot steps once the above is in:
1. Re-run 3a for the five pericopes (rejection at home 13:54–58; Herod and the beheading 14:1–12; the wilderness meal 14:13–21; the sea 14:22–33; Gennesaret 14:34–36).
2. Convert the strongest scene links into `parallel` components. From the chat walk, the candidates were: Herod's feast against Pharaoh's birthday feast (Gen 40); Herodias and Jezebel/Elijah; Herod's oath and Jephthah; John's disciples burying the body (2 Sam 4); Elisha's twenty loaves (2 Kgs 4:42–44); the wilderness meal and the manna; the sea scene with Exod 14 and Job 9:8, Ps 69, and Moses's withdrawal in Exod 2. (This list comes from the chat walk and my notes; Code should re-verify each wording against the LXX before shipping. The unverified wordings from the Unit 14 handoff still stand: Exod 2:15 verb, Ps 131:15 LXX *chortazō*, Gen 40:20 *genesia* wording, Isa 43/51 wording.)
3. Keep the existing 10 `aside.echo` and 15 endnotes where they still fit; move any that are really scene parallels into the new component.
4. Diff against the shipped unit and ask Lane before replacing it, since the working rule is to ask rather than silently rebuild a shipped unit.

## 4. Guardrails (do not lose these)

- Chiasms only when real and verifiable; parallels are the same. The required "different:" field and the strength gate are there to stop overreach.
- Every link needs the target text read, and the chat side marks anything not read this session as "recalled, unverified."
- Transliteration only, everywhere, including attributes.
- Weigh Matthew's own markers (discourse formulas, *apo tote*, formula quotations) next to the patterns found.
- Constable stays the baseline reading, in dialogue with France, Wright, Davies and Allison, the Bible Project, Jewish and patristic voices in the research passes; the artifact drops the names.
- Ask Lane before adding to shared canon files, and before changing a shipped unit.

## 5. Questions for Lane (not for Code to guess)

1. Should parallels be open by default, or hook-visible with the body collapsed?
2. Is one per pericope the right floor, or lighter for short pericopes?
3. Should the listenable walk be the standing chat deliverable for pass 3, with the ledger as a file?
4. Apply to Unit 14 now as the pilot, or start with Unit 15?
