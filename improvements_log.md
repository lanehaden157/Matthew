# Improvements Log

## 2026-09-07
- Added CLAUDE.md, session_index.md, improvements_log.md.
- Reworked CLAUDE.md into the Matthew Study project guide (static site, /units +
  /data + /app + pipeline, two-tier colour policy).
- Wrote PLAN.md — 9-phase build plan; ideas.md folded into scope.
- Phase 1 complete:
  - pipeline/greek.py — deterministic Greek→Latin transliterator (matches the
    ē/ō/ch/ph/ps/rh scheme already in the artifacts).
  - pipeline/extract_units.py — converts source-artifacts/matthew_NN_translation.html
    → units/unit-NN.html: strips head/style/fonts, removes all Greek+Hebrew script
    (314 synth translits, 4 manual), rewrites root spans to data-root, adds rl for
    unit-local colour spans, prefixes endnote ids u0N-nK, rebuilds .greek-title.
  - source-artifacts/ holds untouched copies of all 8 originals.
  - pipeline/out/units.seed.json — per-unit local palettes + roots (for Phase 4).
  - pipeline/out/extract-report.md — every transliteration decision.
- Known colour gaps for Phase 4: U2 call/king aliases, U3 wild→wilderness,
  U7 needs a fresh palette (its style block was a stale copy).

## 2026-09-07 (cont.) — Phase 2: the shell
- data/units.json — 28-unit manifest (movement, passage, title, built flag) +
  local root→hex palettes for the 8 built units. Includes the Phase-4 colour
  fixes: U2 call/king aliases, U3 wild+wilderness, U7 fresh 9-hue palette.
- css/styles.css — one reconciled stylesheet: app chrome (topbar, collapsible
  28-unit picker, prev/next pager, footnote flash keyframes) + the superset of
  all 8 artifacts' component CSS, with chrome colours moved to stable --accent-*
  tokens (no longer borrowing a unit's root palette). Responsive ≤720px.
- index.html — shell: sticky topbar, collapsible Contents nav, #content pane.
- app/main.js — ES-module router: hash routes (#/unit-03, #/unit-03/u03-n5),
  loads fragment, injects per-unit [data-root] colour rules from units.json,
  builds nav + pager, footnote jump-with-flash and click-again-to-return.
- .claude/launch.json (python http.server :4180), .gitignore.
- Verified in-browser: all 8 units render, palettes inject (U7 included — 0
  uncoloured roots anywhere), footnote jump/flash/back-link works, no horizontal
  overflow at 375px.
- extract_units.py fixes found via browser QA: preserve trailing text when
  unwrapping Latin-in-gk spans; keep the closing paren on `(<gk>G</gk>, translit)`.

## 2026-09-07 (cont.) — Phase 3: git + GitHub Pages
- git init -b main; .gitattributes (eol=lf); .gitignore excludes root
  matthew_0*_translation.html dupes (canonical in source-artifacts/).
- First commit ff46900 (36 files), pushed to github.com/lanehaden157/Matthew (public).
- Pages enabled: source main / root. Live at https://lanehaden157.github.io/Matthew/
- Verified live on the /Matthew/ subpath: units load, palettes inject, footnote
  jump works, data/units.json fetches, zero console errors — relative paths hold.

## 2026-09-07 (cont.) — Phase 4: colour engine + threads
- data/threads.json — 16 tracked cross-unit threads (13 from memory + torment /
  urge / sea). id, colour, translit, gloss, opens, payoffs, status. Global tier:
  a root here is that colour in every unit; recolour = one hex edit.
- data/units.json roots → {color, translit, gloss} per root (was hex). Backfilled
  from the fragments' hand legends by extract_legends.py (+ legend-overrides.json).
- pipeline: scan_occurrences.py → data/occurrences.json; verify_occurrences.py
  (independent re-count + colour-resolution + perceptual-collision check);
  apply_retrofit.py (retrofit-tags.json); build.py runs the whole chain.
- Retrofit applied to fragments: nations 4:15, apo-tote 4:17, law-prophets
  5:17 & 7:12, little-faith 6:30, light 5:14 & 6:23, wise-foolish 7:24/26;
  retag 8:26 faith→little-faith; unwrapped a mis-tagged "deportation" (U1).
- app/threads.js — colour resolution + data-driven legend rebuild (thread pills,
  occurrence counts). main.js fetches are cache-busted (?v=ts); index.html
  script/css tagged ?v=4.
- Colour collisions fixed: U6 seen→#1596b8, little-faith global→#8f6f9a.
- Verified on the live Pages deploy (fresh origin): all retrofit tags render,
  global thread colours consistent across units, zero console errors.
- Note: local python http.server + the in-app browser cache fragments very
  stickily; trust verify_occurrences.py + a fresh-origin check, not ctrl+shift+r.

## 2026-09-07 (cont.) — Spotlight + footnote polish
- app/spotlight.js — per-verse .gloss / .compare asides gathered into one
  collapsible <aside class="spotlight"> (quiet ✦ toggle on the verse, unit-level
  show-all/hide-all, collapsed by default, auto-expands for print). Runs on each
  loaded unit; fragments untouched.
- styles.css — unified spotlight panel (soft tint, gold left-accent, one style
  for gloss + compare, dashed compare border dropped); .spot-toggle / .spot-all;
  print block hides toggles + topbar.
- Footnote "↩ back" link now removes itself after one use (was lingering dead).
- Verified on live deploy: 23 panels in U7, 0 loose asides, collapse/expand +
  show-all all work.

## 2026-09-07 (cont.) — wording: heavens -> skies
- pipeline/wording_skies.py — one-shot revision of source-artifacts: the study's
  own 'heaven(s)' -> 'sky/skies' (units 1-5 had old wording; 6-8 already matched).
  Verbatim NASB/Hart rows in compare boxes protected (still "kingdom of heaven").
  31 substitutions. Re-ran build.py. Style reference §4 updated for units 9-28.

## 2026-09-07 (cont.) — Phase 5: root interactions
- threads.js wireRoots() — hover any coloured root (desktop) -> tip with
  translit + gloss; click any root -> popover: swatch, translit, gloss,
  "N× in this unit · vv…", and for tracked threads the trajectory
  (opens … → payoff Unit N links, built = live / unbuilt = greyed),
  "also in Unit X", and the thread note. Dismiss on outside-click/Esc/scroll.
- CSS: .root-tip, .root-pop, [data-root] hover underline + .root-active.
- Skipped the "threads active here" footer (redundant with the legend).

## 2026-09-07 (cont.) — thread polish
- scan_occurrences: `count` is now verse-text only (was counting legend/gloss
  too); `total` kept for verify's token cross-check. Popover + legend N× fixed.
- threads.js injectPalette: tracked-thread roots get a dotted underline in
  their own colour ("thread" under the word) + colour glow on hover/active.
- rebuildLegend: split into two groups — "✦ Cross-unit threads" / "In this unit".
- Confirmed: occurrences.json regenerates every build.py; threads.json
  trajectory is hand-maintained per unit as loops close.

## 2026-09-07 (cont.) — Phase 6a: concordance search
- scan_occurrences: each root now carries `hits: [{v, pre, hit, post}]` context
  snippets (verse text only, sup/verse-number stripped). VBLOCK tightened to the
  verse element itself (was over-capturing trailing glosses).
- app/search.js — #/search route: type a translit root (diacritic-folded, so
  "aphiemi" finds "aphiēmi") or English gloss -> results grouped by root then
  unit, each hit a snippet linking to #/unit-NN/vNN (jumps + flashes the verse).
- topbar "Search" link; main.js verse-anchor (#/unit-06/v14) support.
- Note: U6 v14 tags "false steps" (paraptoma, the object) as data-root=release —
  author's choice; shows up bolded in search. Left as-is.

## 2026-09-07 (cont.) — discourse structure surfaced
- units.json: added `discourses` (Sermon 5-7, Mission 10, Parables 13,
  Community 18, Woes+Olivet 23-25).
- Contents nav: discourse units wrapped in a gold left-bar sub-block with a
  "◆ Discourse N · Label" heading, nested inside their movement.
- Each unit page: a placement line under the masthead —
  "Movement II · … — ◆ Discourse I: Sermon on the Mount (2 of 3)".

## 2026-09-07 (cont.) — book structure map (replaces nested discourse blocks)
- Contents panel now opens with a map of the whole book: 28 unit ticks in three
  movement groups (roman-numeral hairline headers), the 5 discourses drawn as
  gold brackets spanning the units they cover, and a two-row key naming the
  movements and discourses. Ticks: built = solid + clickable, unbuilt = dashed
  and faded, in-discourse = gold-tinted, current = gold fill.
- The unit grid below is left uninterrupted (no more brackets over a wrapping
  grid, which was the confusing part).
- Names live only in the key, so nothing in the map can truncate.
- Mobile: the strip scrolls inside its own container with a soft right edge; the
  page itself never scrolls sideways.

## 2026-09-07 (cont.) — contents map: centered + discourse highlight
- book-map strip, movement labels, and the movements/discourses key all centered.
- discourse units now clearly marked in BOTH places: map ticks get a gold tint +
  gold-ish border; picker chips get a gold left-bar, warm tint, and a "◆ N" mark.

## 2026-09-07 (cont.) — U1 structure normalized + book-map sizing
- extract_units.normalize_verses(): Unit 1 (built pre-conventions) had
  <div class="v"> with .gloss/.compare nested INSIDE and compare using
  div.row/.lab. Now reshaped to <p class="v">…</p> + sibling blocks with
  span.row/.src, matching units 2-8 — so spotlight collapse + occurrence
  scan work on it. 20 verses normalized, 3 compare boxes.
- book-map: .bm-row fills 100% width on desktop (movements flex by unit
  count) so it's genuinely centred/full; scrolls sideways only below tablet.

## 2026-09-07 (cont.) — legend box consistency
- extract_units.normalize_blocks(): Unit 1's colour-key was <section class="legend">
  (no panel box) while every other unit is "block legend". Normalized.
- rebuildLegend: the "In this unit" / "✦ Cross-unit threads" sub-headings now
  only appear when BOTH groups are present; a unit with no tracked threads
  (U1, U2) just lists its roots under the h2, no orphan sub-header.

## 2026-09-07 (cont.) — two formatting bugs
- extract_units: bare Greek in a tag (Logeion href, title=...) was being wrapped
  in <span class="translit">, which broke the <a> markup — U1/2/3/4/6/8 endnote
  links. strip_leftover_script now splits on tags and only transliterates
  visible text; script inside a tag is left as-is (Greek URLs resolve fine).
- ring-diagram labels longer than 2 chars (e.g. "HINGE" in U4) overflowed the
  narrow label column. normalize_blocks marks them .lab-word; CSS renders those
  small-caps at 11px so they fit.

## 2026-09-07 (cont.) — Unit 1 verse normalization rewritten
- normalize_verses was a flat regex that couldn't handle U1's 2-level div
  nesting (verse > compare > row). It truncated verse 23's compare box,
  leaving an unclosed <span>/<div> that swallowed everything after it —
  raw markup showing in the verses, endnotes trapped in a white box.
- Rewrote with a depth-counting div matcher (_match_close). All 8 units now
  tag-balanced; U1 verses + compare boxes well-formed; endnotes a clean
  top-ruled section like every other unit.

## 2026-09-07 (cont.) — root/motif taxonomy
- Every tracked item is now kind:"root" (one Greek lexeme/family/phrase — colour
  = the same word recurs) or kind:"motif" (kindred but distinct words — colour =
  thematic grouping, called out).
- threads.json: +emmanuel (meta/Emmanouēl, 1:23<->28:20), +son-of-man (opens
  8:20); build-rock & wise-foolish -> motif; fish label -> halieus.
- units.json relabelled to single lexemes; SPLIT name->call+name,
  david(+king via U2), test->test+slanderer, dark->dark+shadow,
  way->way+gate; UNTAGGED strays (Jesus off save, angel off dream, Anointed
  off david, 'false steps' off release, blepō off eye); wage/seen/said -> motif.
- fragment retags via retrofit-tags.json (new ops: retag_word, untag_word, text).
- 'demonized' -> 'demon-possessed'; 8:10 pistis -> 'trust'.
- legend: three sections (✦ threads / ◈ motifs / roots). In text: threads get a
  dotted underline, motifs a dashed one, plain roots colour only. Popover says
  "root — the same word, recurring" vs "motif — kindred words: …".
- extract_legends.py retired from build.py (units.json is hand-maintained now).
- Unit 1 pre-conventions structure fully normalized (verses, compare boxes,
  legend box, endnotes).

## 2026-09-07 — Phase 9: author ergonomics / drop-in artifact contract
- Artifact contract v2. The Claude.ai project now emits a pure site fragment:
  one `<article class="unit" data-unit="N">`, no `<head>`/`<style>`/fonts/`--c-*`,
  opened by `<script type="application/json" id="unit-meta">` (unit, passage,
  title, roots [translit+gloss, NO colour], threads {opens,payoffs,candidates}).
- pipeline/unit_meta.py — single shared definition of the meta block: parse(),
  strip(), inject(), validate(meta, threads_json), generate(n) from the data files.
- pipeline/port_artifact.py — `NN` ports one artifact: standalone→fragment if
  needed (reuses extract_units cleaners), validates meta vs threads.json, merges
  the unit into units.json (assigns a local hue per non-thread root, dE≥12
  collision check against the §1 well), writes pipeline/out/thread-delta-NN.md
  for Lane, runs retrofit+scan+verify. Never writes threads.json. `--dry` +
  `--backfill` modes.
- pipeline/refresh_meta.py — regenerate built fragments' meta blocks from the data
  (idempotent). pipeline/threads_digest.py — threads.json → threads-digest.md.
  Both added to build.py (order: extract → retrofit → refresh_meta → scan →
  verify → digest).
- Units 1–8 backfilled: meta block prepended, **zero** change to prose/tags/ids
  (git diff = pure insertions; pipeline/out/renormalize-report.md). build.py
  re-run green: 332 occurrences, all roots resolve, no collisions.
- Docs: matthew_study_style_reference.md rewritten to v2 (§1–4, §6a point at
  threads-digest.md); new instructions.md (v2 research-project instructions,
  `old instructions.md` kept); PLAN.md Phase 9 marked done; CLAUDE.md status +
  layout updated.
- Known carry-over (not touched): units.json glosses use `(γεν-)` morphology
  shorthand with Greek chars — pre-existing taxonomy choice, already renders in
  the site legend; revisit if strict translit-only matters there.
- extract_units.py now skips any source-artifact already in v2 fragment shape
  (`<article class="unit">`) — those go through port_artifact.py only.

## 2026-09-07 — Unit 9 ported (first v2 artifact)
- `matthew_09_translation.html` arrived already in v2 shape; `port_artifact.py 9`
  ran clean after a porter fix (local-hue assignment now also clears the global
  colours of threads the unit uses — first run collided release/mercy,
  son-of-man/save).
- Promoted all 4 candidates to `data/threads.json`: **son-of-david** (#8a3c70,
  opens 9:27), **mercy** (#2f6db3, opens 9:13, Hosea 6:6), **save** (#c0641a =
  its old local hue, opens 1:21 — now global across units 1/3/9), **fringe**
  (#455a6b, opens 9:20). Added unit-9 payoff refs to authority / son-of-man /
  follow / throw.
- build.py green: 9 units, 362 in-verse occurrences, every root resolves, no
  collisions. Unit 1 meta block gained the `save` open. Units 2–8 unchanged.

## 2026-09-07 — drop the motif tier (everything is a root)
- Reverses the root/motif taxonomy (8d096c9). A bundled word-family
  (`wage` = misthos/apechō/apodidōmi, `seen`, `emmanuel`, `build-rock`,
  `wise-foolish`, `new-old`) is now just a plain root — one slug, one colour,
  the family listed in its `translit` string. No re-tagging, no colour changes.
- `kind` + `members` stripped from data/threads.json, data/units.json, the
  fragments' meta blocks, and source-artifacts/matthew_09.
- app/threads.js: no more dashed-underline motif rendering or "◈ Grouped motifs"
  legend section or "kindred words" popover copy — two tiers again (thread /
  root). css: dropped `.legend-members`, `.lg-motif`, `.rp-members`, `.rp-k`.
- pipeline/unit_meta.py now *rejects* `kind`/`members` in a meta block;
  port_artifact.py + threads_digest.py drop them. pipeline/apply_taxonomy.py
  deleted (one-shot, baked into units.json, referenced the removed taxonomy).
- matthew_study_style_reference.md §1/§2/§3 updated: "Word-families" replaces
  "Motifs". build.py green.

## 2026-09-07 — one lexical root per colour (retroactive)
- Rule (style ref §1): a tracked root = one Greek stem + its same-stem forms
  (`baptizō · baptisma`), never a theme/formula/bundle of distinct words. The
  one exception: fixed titles/markers Matthew repeats verbatim (son-of-man,
  son-of-david, law-prophets, apo-tote) — kept as threads.
- Split: `wise-foolish` thread → `wise` (phronimos) + `foolish` (mōros);
  `build-rock` → `build` (oikodomeō) + `rock` (petra). New hues foolish #5e1822,
  rock #6b7280.
- Trimmed to the head word: `wage` → misthos only (untag apechō "in full",
  apodidōmi "pay back"); `seen` → theaomai only (untag phainō/aphanizō/blepō).
- Dropped: `said` / `isay` / `yall` (U5 — rhetorical formulae, not roots),
  `new-old` (U9 — one-passage wordplay; endnote already carries neos vs kainos).
- Normalized `/` → `·` on same-stem translits (faith, mercy); `emmanuel`
  translit → `meta`; `kingdom` → `basileia`.
- Fragment edits via retrofit-tags.json (untag_word/retag_word/add) so they
  survive re-ports; U9 edits in its source artifact. build.py green — 9 units,
  every root resolves, no collisions. Threads: 22 → 24.

## 2026-09-08 — one section-heading form + consistent "show all notes"
- Section titles: `<h3 class="pericope">Title <span>· C:V–V</span></h3>` (Unit 8's
  form) is now the only section-divider markup.
  - `app/main.js` `normalizeSectionHeadings()` rewrites legacy `h2.secthead` /
    `h3.panel` / `h3.movement` / `.sectionhead` to `h3.pericope` on load and
    wraps a trailing ` · range` in a `<span>` — covers past fragments and any
    future drift.
  - Also fixed at source: `source-artifacts/matthew_06/07/10_translation.html`
    and the regenerated `units/unit-06/07/10.html` (Unit 10 was `h2.secthead`
    with *no* matching CSS — rendered unstyled). Unit 6's two "Movement N · …"
    headers became pericopes keyed on their descriptive subtitle.
  - `matthew_study_style_reference.md` §3 + §4: `h3.pericope` spec + checklist.
  - Units 1 (`div.sectionhead` ×2) and 3 (`div.panelhead` ×2) already had
    dividers in other markup — converted at source + rebuilt.
  - Units 2, 4, 5, 9 had none — **23 pericope headings authored** (Lane approved
    the proposal, only edit: Unit 4 "Isaiah's light"). Inserted into the source
    artifacts (2/4/5) + `units/unit-09.html` (v2, not regenerated) + unit-09
    source. build.py green — every unit now carries `h3.pericope` dividers.
- "Show all notes" control (`app/spotlight.js` `addAllControl`): anchor was
  `.verses || firstVerse.parentElement`; in the v2 fragments (9, 10) there is no
  `.verses` wrapper so it fell to `article.before(bar)` — the bar rendered above
  the masthead. Now: find the article-level node containing the first verse, and
  if a section heading sits just above it, place the bar above that — so it
  always lands just under the structural blocks, as in Unit 6.
- Asset version 27 → 28.

## 2026-09-08 — structural blocks always render first
- `app/main.js` `hoistStructureBlocks()` — on unit load, every
  `section.block` (except the colour key) is moved to the top of the article,
  just under the legend, in authored order. Rings/chiasms, comparison tables
  (`table.exod`), and itineraries (`.itin`) now come before the translation in
  every unit; the research fragments can keep dropping them wherever they fall
  in the prose. Runs right after `renderPlacement`, before palette/legend/
  spotlight wiring. Fragments untouched — pure app-side transform, like
  spotlight.js. Visible change in units 4, 6, 10 (had blocks mid/after verses).
- Asset version bumped 26 → 27 (index.html, main.js, search.js imports).

## 2026-09-08 — Unit 10 ported (Matt 9:35–11:1, Mission discourse)
- `port_artifact.py 10` on `source-artifacts/matthew_10_translation.html` (v2
  fragment shape). Validated clean; merged into units.json (built:true), local
  hues: worthy #a8324a, receive #2f6db3, harvest #9c2f8f, send-out #1f8f5f.
- threads.json (Lane's call from the thread delta):
  - Promoted 4 candidates — **hand-over** (paradidōmi, #8a3c70, opens 10:4 →
    10:17/19/21, 17:22, 20:18-19, 26, 27), **cross** (stauros, #455a6b, opens
    10:38 → 16:24, 27:32-42), **lose** (apollymi, #8a6a2a, opens 10:6 → 10:28/39/
    42, 15:24, 18:11-14), **fear** (phobeō, #1c7d70, opens 10:26 → 14:26-27,
    17:6-7, 25:25, 27:54, 28:4-10). Each kept its porter-assigned unit-10 local
    hue as its thread colour. No retag needed — spans already in the fragment.
  - Kept `worthy` (axios) local — dense in U10 but only 22:8 later.
  - Added unit-10 payoff refs to throw / authority / son-of-man / save / wise /
    nations / follow (status unchanged — none close at U10).
- Re-ran port + build.py: green. 10 units, 374 in-verse occurrences, every root
  resolves, no perceptual collisions. threads-digest.md → 29 threads. Units 1-8
  fragments untouched (refresh_meta produced identical output).

## 2026-09-07 — doc reconciliation (no contradictions)
- Deleted `old memory.md` + `old instructions.md` — fully superseded. Their live
  content (Greek-handling rules, research bash patterns, Constable-dialogue
  principle, "y'all only for genuine plural", surgical-edit preference) folded
  into `instructions.md`.
- `instructions.md` rewritten as the single current chat-side + artifact spec:
  translit-only + gloss-always + never-assume-known + explain-grammar-plainly;
  three-pass per-unit workflow; one-lexical-root colour rule; threads-digest.md
  is the thread source of truth (not memory).
- `matthew_study_style_reference.md`: dropped the v1/v2 changelog framing (units
  1–8 already conform), fixed "colours decided fresh per unit" → site's job,
  marked Unit 9 built.
- Stripped Greek-script morphology from units.json glosses (`(γεν-)` → `(gen-)`
  etc.) — was rendering in the site legend against the translit-only rule. Zero
  Greek/Hebrew chars now in data, fragments, or digest.
- PLAN.md "What exists today" retitled as a non-maintained kickoff snapshot;
  softened the stale "~16 threads" mention. CLAUDE.md status → units 1–9 built,
  next Unit 10; added the one-root colour policy line.
- Synoptic-parallel component added: `.synpar` div (sibling after `<p class="v">`,
  same rule as `.gloss`/`.compare`) auto-wraps via spotlight.js into a collapsible
  ✦-chip aside — third kind alongside note/spotlight, crimson accent to
  distinguish from the gold "Rendering" boxes. CSS + spotlight.js updated;
  matthew_study_style_reference.md documents the markup + checklist rule
  (translit only, no data-root inside it — corrupts occurrence counts). Asset
  version 29 → 30. Not yet applied to units 1–10 — pending the Claude.ai
  research project's synoptic-parallels.md handoff file.
- Correction to the above: Lane had already produced `synoptic_parallels_units_01_10.md`
  (28 boxes) using self-contained `<aside class="synoptic" data-anchor="C:V">` blocks with
  their own `<h4>` header — not the `.synpar` div format first sketched. Reworked
  spotlight.js to match: it now hides pre-authored `aside.synoptic` siblings in place and
  adds a toggle chip per box, rather than wrapping a bare div. matthew_study_style_reference.md
  updated to document the real shape. New `pipeline/splice_synoptic.py` spliced 27/28 boxes
  automatically (anchor -> chapter:verse resolved via running pericope-heading state); the
  28th (unit 6, 6:13 — the Lord's Prayer poem block has no numbered `<p class="v">`) inserted
  by hand after the block's trailing `.compare` siblings. Verified: 0 `data-root`/`.r`/`.rl`
  inside any spliced box. Asset version 30 -> 31.
- Toggle-chip styling: spot-toggle (gold, ✦) and syn-toggle (crimson, ✧) now
  keep their outline colour at rest, not just on hover — outline stays visible
  always, fills solid on open/click. Synoptic symbol changed from ✦ to ✧ (open
  star) so it reads as a variant of the rendering-box chip, not identical to
  it. Asset version 31 -> 32.
- Cut 8 over-reaching structural diagrams per Lane's call — they didn't hold up:
  Unit 2 Magi ring + Exile/Return triptych, Unit 3 "Mackie's symmetry" 3-panel
  frame, Unit 5 Beatitudes chiasm, Unit 6 devotion-panel ring, Unit 8's own-shape
  ring, Unit 9 paralytic ring-inside-ring, Unit 10 discourse-shape ring + ladder-
  of-receiving ring. Left the comparison tables (Inverted Exodus, Ezekiel 34,
  Israel/Adam/Jesus) and the smaller triads/itineraries in place — only cut
  where Lane named it. scan_occurrences + verify_occurrences green after
  (374 occurrences, every root still resolves elsewhere in its unit).
- Persistent prev/next unit buttons: small subtle circular fabs fixed to the
  bottom corners of the viewport (`.unit-fab`), always reachable regardless of
  scroll position — not just the pager at the bottom of a long unit. Low
  opacity at rest, full on hover/focus; hidden while the contents overlay is
  open; excluded from print. Wired into buildPager() alongside the existing
  bottom pager. Asset version 32 -> 33.

## 2026-09-09 — book-map centering fix
- `.book-map` and `.unit-nav .movement-label` each carried `margin: … 0 …`,
  which (equal specificity, later in the source) overrode the
  `.unit-nav > * { margin-inline: auto }` centering rule — so the contents-map
  strip sat flush-left instead of centred on the 790px column. Changed both to
  `margin: … auto …`.

## 2026-09-09 (cont.) — cross-unit thread retroactive coverage
- New policy: a tracked root is coloured at EVERY morphological occurrence in
  U1–10 — `.r` from its opening unit on, `.rl` before. `opens` stays the
  editorial trajectory anchor, not the first sighting. threads.json `_note`
  updated; full audit at pipeline/out/thread-retrofit-audit.md.
- Scanned SBLGNT (new file `Matthew greek text.txt`) lemma-by-lemma vs the
  fragments. 35 spans added via retrofit-tags.json `add`:
  light 5:16/6:22/10:27 · nations 5:47/6:7/6:32 · SEA 8:24/26/27/32 (flagship
  miss — storm narrative was untagged) · release 3:15/4:20/4:22/5:24/5:40/7:4 ·
  faith 9:22/28/29 · fear 1:20/2:22/9:8 · lose 2:13/5:29/5:30/7:13/8:25/9:17 ·
  save 8:25 · mercy 5:7×2/6:2/6:3/6:4 · foolish 5:13/5:22 · urge 2:18/5:4.
- apply_retrofit.py `add` now takes optional "cls":"rl"; skips inline "_c" notes.
- Colour collisions from the new co-occurrences (12) fixed:
  release thread #147a63 → #0e6a3f (was dE 6.6 from fear teal, now co-occur U9);
  8 local hexes in units.json nudged (u1 name, u2 call/king, u5
  evil/gehenna/kingdom, u6 father, u8 raise). verify_occurrences green.
- On review: authority 7:29 tagged by nesting data-root around the .star span
  (keeps gold-italic + adds thread underline); release 4:11 tagged via `text`
  op ('leaves', no .n marker). throw pre-opening left untagged (Lane); nations
  ethnikos rl kept (Lane). New collision fixed: u7 `way` #6b2fb3 → #6a4a3a
  (vs authority thread purple). Total 37 spans, 9 local hexes, verify green.

## 2026-09-09 (cont.) — remove .star "motif" gold-italic device
- Lane: never sanctioned it. Stripped all `<span class="star">` wrappers from
  units 2 (star/rising wordplay), 3 (stones/fire/fruit/way/wrath — 14 of them),
  7 (anomia/exousia cap). Dropped `.unit .star` from css/styles.css. Trimmed the
  explanatory sentences (u3 legend cap, u3 n3 hodos note, u7 cap reworded — and
  exousia is now a tracked thread anyway).
- authority 7:29 is now a plain thread span (no nested .star).
- Still present in source-artifacts/ — noted in retrofit-tags.json _note.

## 2026-09-09 (cont.) — rl -> r on the retro-tags
- Lane's call: the 27 pre-opening/incidental thread spans added above used
  class="rl" for the "not counted" property, but scan_occurrences counts any
  data-root inside a <p class="v"> regardless of class — so `.rl` there was a
  misleading label. Downgraded all 27 to class="r". No doc changes needed:
  the `.rl` "not counted" wording in CLAUDE.md / style-ref stays correct for
  its actual use (legend rows, diagram labels, glosses — all outside verse
  blocks). threads.json _note + retrofit _c + audit report reworded to drop
  the .r/.rl split; policy is now simply "tag every occurrence as .r, even
  before the thread's opens".

## 2026-09-09
- css/styles.css: --maxw 790px -> 900px. Reduces desktop side margins;
  no effect on mobile (breakpoint 720px, narrower viewports already fill the
  column; 26px page padding unchanged).
