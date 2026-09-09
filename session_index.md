# Session Index

Read this first. 3 lines max per session.

## 2026-09-07 — kickoff + Phase 1
- Set project direction: static site rebuild of the 28-unit Matthew study;
  wrote CLAUDE.md guide + PLAN.md (9 phases). 8 source artifacts on hand (units 1–8).
- Phase 1 done: pipeline/ extracts source artifacts → units/unit-NN.html
  (script stripped, translit-only, data-root spans, prefixed endnote ids).
- Phase 2 done: index.html + app/main.js router + css/styles.css; all 8 units
  render in-browser, responsive, footnote jump works.
- Phase 3 done: live at https://lanehaden157.github.io/Matthew/
- Phase 4 done: data/threads.json (16 threads), two-tier colour engine
  (threads.js), occurrence pipeline + verify, data-driven legends, retrofit tags
  applied. Verified on live deploy.
- Phase 5 done: root hover tip + click popover (thread trajectory w/ jump
  links). Spotlight split (light * notes vs ✦ rendering boxes). heavens->skies.
- Phase 5 done (cont.): root hover/click popovers.

## 2026-09-07 — Phase 9 (author ergonomics)
- Artifact contract v2: pure `<article>` fragment + `<script id="unit-meta">` JSON
  block, `data-root` only, no `<style>`/colours. Rewrote matthew_study_style_reference.md
  + new instructions.md; threads-digest.md now generated.
- New pipeline: unit_meta.py, port_artifact.py (single-unit port + thread-delta),
  refresh_meta.py, threads_digest.py; folded into build.py.
- Units 1–8 re-normalized = meta block only, zero prose/tag change.
- Unit 9 ported (first v2 artifact) — clean after a porter hue-collision fix.
  Promoted son-of-david / mercy / save / fringe to threads.json. build green.
- Dropped the motif tier entirely (Lane's call) — every tracked item is a plain
  root now. Stripped kind/members from data + fragments + app/threads.js + css +
  style reference; deleted apply_taxonomy.py.
- Then hardened to "one Greek lexical root per colour" retroactively: split
  wise/foolish + build/rock, trimmed wage→misthos & seen→theaomai, dropped
  said/isay/yall/new-old. Fixed titles (son-of-man etc.) kept as the exception.
- Doc reconciliation: deleted old memory.md + old instructions.md (folded live
  bits into instructions.md), rewrote instructions.md as the single chat-side +
  artifact spec, de-Greeked units.json glosses, fixed PLAN/CLAUDE staleness.
  build green, 9 units. Next: Unit 10 (9:35–11:1, Mission discourse).

## 2026-09-08 — Unit 10 ported (Mission discourse)
- `port_artifact.py 10` clean; local hues worthy/receive/harvest/send-out.
- Promoted 4 candidates to threads.json: hand-over (paradidōmi, opens 10:4),
  cross (stauros, 10:38), lose (apollymi, 10:6), fear (phobeō, 10:26). Kept
  `worthy` local. Added unit-10 payoff refs to throw/authority/son-of-man/save/
  wise/nations/follow. build green — 10 units, 374 occurrences, 29 threads.
- main.js hoistStructureBlocks(): all section.block (rings/tables/itineraries)
  now render at the top of every unit, under the legend, before the translation.
- Section headings normalized to <h3 class="pericope"> (Unit 8's form) via
  main.js + fixed at source for units 6/7/10; style ref updated. Units 1-5, 9
  have no dividers — needs authored titles (asked Lane).
- spotlight.js "show all notes" bar now anchors consistently (was above the
  masthead in units 9/10). Asset version 26 → 28.

## 2026-09-09 — Synoptic parallel component
- Designed synoptic-comparison feature: chat-side research produces a markdown
  handoff file, backported into units 1-10, then built-in going forward.
- Wired `.synpar` into spotlight.js/css as a 3rd collapsible kind (crimson
  accent). Style reference + checklist updated. Waiting on handoff file.
- Corrected: reused Lane's already-produced synoptic_parallels_units_01_10.md
  (28 boxes, aside.synoptic + data-anchor format) instead of re-requesting.
  Wrote pipeline/splice_synoptic.py, spliced 27/28 automatically, 1 by hand
  (unit 6 Lord's Prayer poem block). spotlight.js/style-ref updated to match.

## 2026-09-09 (cont.) — book-map centering + cross-unit thread audit
- Fixed contents-map strip: `.book-map`/`.movement-label` had `margin: … 0 …`
  overriding the `.unit-nav > *` centering; → `margin: … auto …`.
- Retro-tagged tracked roots at every morphological occurrence in U1–10
  (35 spans, `retrofit-tags.json`): flagship = `sea` ×4 in U8 storm, missing.
  New policy in threads.json `_note`; audit in pipeline/out/thread-retrofit-audit.md.
- Colour ripple fixed: `release` thread #147a63→#0e6a3f, 8 local hexes nudged.
