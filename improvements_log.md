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
