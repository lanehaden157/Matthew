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
- Units 1–8 re-normalized = meta block only, zero prose/tag change
  (pipeline/out/renormalize-report.md). Next: port Unit 9 when the artifact lands.
