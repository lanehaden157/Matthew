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

## 2026-09-10 — desktop width + `sin` thread
- css: `--maxw` 790px → 100% (kill desktop dead space; mobile untouched).
- New tracked thread `sin` (hamartia/hamartanō, #8a4a5a): opens 1:21, payoff
  9:2-6 + 26:28. Tagged 5 occ (U1 v21, U3 v6, U9 v2/5/6) via retrofit-tags.json.
  threads.json + refresh_meta + scan/verify + digest all green.

## 2026-09-10 (cont.) — thread-add tooling
- `audit_thread_coverage.py` + `thread-stems.json`: scans MatthewSBLGNT.txt
  (git-ignored, repo root) for every morphological occ. of a thread's Greek
  root, flags built-unit gaps. Caught 3 missed `sin` (9:10/11/13, ἁμαρτωλός
  "sinner") — now fixed. Seeded stems for 8 threads; 16 still undefined.
- `strip_span` op added to apply_retrofit (`.star` device now encoded).
- Known: `hand-over` has 2 pre-opening gaps (4:12, 5:25) — deferred, needs a
  distinct colour (currently shares #8a3c70 with apo-tote → same-unit collision).
- build.py made safe: dropped extract_units from its STEPS (it's now a
  port_artifact-only library), added the coverage audit as an advisory step.
  Fragments are the source of truth; build.py replays retrofit + regenerates
  data only. Verified idempotent.

## 2026-09-10 (cont. 2) — thread-add tooling phases 1-3 + stems
- Phase 1: `--forms` mode + research-prompts.md (stems prompt). Phase 2: exact
  chapter/verse alignment from the Greek + `--unit`/coverage_for_unit. Phase 3:
  new meta fields (opens/payoffs `note`, candidate `stems`) + richer
  thread-delta report (coverage gaps, stem previews) + `port_artifact --src`.
- All 16 remaining stems folded in (research project). Coverage now 0 gaps
  across 24 threads: tagged throw (pre-opening + unit-07 `do` misfix, recolour),
  torment, hand-over (recolour off shared purple). occurrences 423 -> 437.
- Phase 4 DONE: `threads.retro[]` fix-list for earlier units (dry-checked,
  merged into generated retro-tags.json, applied); porter structure checks
  (pericope headings + ·C:V range, no old heading classes, aside.synoptic
  data-anchor + translit-only). All 5 phases of the thread-add restructure
  complete. Remaining: Phase 5 = update the style reference (repo-root
  matthew_study_style_reference.md) to describe the new meta fields.

## 2026-09-10 (cont. 3) — OT citation pointer standardized
- Unit 3's trailing linked `(Book C:V)` Bible Hub pointer on OT-quoting `p.v`
  verses applied to U1/2/4/7/8/9/10 (10 verses; U2 quote-links unwrapped).
- Sermon antitheses left alone by decision; style reference + checklist updated
  so future artifacts emit the pointer.

## 2026-09-10 (cont. 4) — buried synoptic asides
- 8 synoptic asides (U1/4/5/8/9/10) were spliced inside an unclosed .gloss span
  or .compare box → rendered with a bare `*`/`✦` chip instead of `✧`. Pulled out
  to sibling position, split glosses rejoined. Porter now flags this. build green.

## 2026-09-10 (cont. 5) — Unit 11 ported
- `port_artifact.py 11` clean. Promoted 6 new global threads (skandalon,
  metanoia, generation, come-here, gentle, well-pleased) per the artifact's own
  "Lane's decision this session" retro notes; reopened law-prophets (11:13).
  Fixed 4 same-unit colour collisions the porter's hue-assigner missed. `seize`
  left as a local candidate (Lane to decide on promotion). build green — 11
  units, 464 occurrences, 36 threads. Verified in-browser. Next: Unit 12.
