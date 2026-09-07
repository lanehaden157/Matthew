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
