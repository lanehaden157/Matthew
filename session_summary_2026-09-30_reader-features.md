# Session summary: 2026-09-30, reader features from the core shell

Lane asked for the "All books" link and the settings Joshua and Numbers have.

## Found
- Matthew already had dark mode (Settings → Appearance, shared `bible:theme` key) and center-align.
- Missing vs the core shell: All books link, reading modes, interlinear, print, verse jump + resume, source footer.

## Lane's calls (popup)
- Add to Matthew's own code (stays standalone): **All books link** and **reading modes** now.
- Interlinear later, as its own session. Print and verse jump + resume were not picked; logged in PLAN.md.

## Done
- `app/main.js`: `addHubLink`, `MODES`/`readMode`/`applyMode`/`wireModes` (`matthew:mode`), `wireAppearance` (moved from an inline script in `index.html`); "every note open" applied on each unit load.
- `app/spotlight.js`: exported `openAll`.
- `index.html`: Settings panel grouped Reading mode / Appearance / Layout; v=39.
- `css/styles.css`: settings headings, `body.mode-plain` hides, `.topbar-actions` wraps under 720px.
- PLAN.md: "Reader features from the core shell" backlog entry. `build.py` ok (its CRLF-only rewrites of units/data restored).

## Open
- Lane: browser check (desktop + 375px): All books link, three modes, dark mode still switching, top bar wrap.
- Uncommitted until Lane OKs.
