# Session summary — 2026-09-10

## Done

### Desktop width
- `css/styles.css`: `--maxw` 790px → 900px → 1150px → **100%** over the
  conversation. Content now fills the monitor minus the shared 26px side padding
  (topbar, `.wrap`, `.unit-pager` all use it, so alignment holds).
- Mobile unaffected — the 720px breakpoint layout and narrower viewports already
  filled the column.
- Open question: at 100% the verse prose runs long on wide monitors. Lane to
  eyeball; easy revert to a fixed cap (1000–1150px) if it reads badly.

### New tracked thread: `sin`
- `data/threads.json`: added `sin` (root `sin`, translit `hamartia · hamartanō`,
  colour `#8a4a5a` — a muted wine, min ΔE ~18 from every other resolved colour in
  units 1/3/9). opens 1:21; payoffs 9:2-6 and 26:28; `status: open`, `tagged: true`.
- `pipeline/retrofit-tags.json`: +5 `add` entries tagging `sins` at U1 v21,
  U3 v6, U9 v2 / v5 / v6 — every hamartia occurrence in Matthew's running text in
  the built units. (Non-Matthew text — Luke 11:4 compare box, NASB rows, endnotes,
  the 6:12 "debts" — deliberately left untagged.)
- Ran `apply_retrofit` → `refresh_meta` (U1 opens + U9 payoffs picked up
  automatically) → `scan_occurrences` → `verify_occurrences` (green: counts match,
  every root resolves, no colour collisions) → `threads_digest` (now 30 threads).
- Did **not** run the full `build.py` — its first step re-extracts from
  source-artifacts and would reintroduce the removed `.star` device in U2/3/7.

## Takeaways
- Adding a thread = threads.json entry + retrofit-tags.json entries + rerun the
  4 downstream steps (not `build.py`). The fragment's static legend `<li>` list is
  irrelevant — `threads.js` `rebuildLegend` regenerates it from
  occurrences + threads/units json at load.
- `data/*.json` are UTF-8; Windows Python's default `open()` picks cp1252 and
  chokes — always `io.open(..., encoding="utf-8")`.

## Open questions
- Desktop line length at `--maxw: 100%` (above).
- `sin` in units 11-28: will be tagged as those units are ported — the research
  project reads `threads-digest.md`, which now carries `sin`.
