# Session Summary — 2026-09-07 (Phase 4: colour engine + threads)

## What was done

**`data/threads.json`** — 16 tracked cross-unit threads (the 13 from project
memory + torment / urge / sea). Each: `id`, `root`, `translit`, `gloss`,
`color`, `opens`, `payoffs[]`, `status`, `tagged`. Global tier — a root listed
here gets its thread colour in *every* unit it appears in; recolouring a thread
book-wide is one hex edit.

**`data/units.json`** — each built unit's `roots` map became
`name → {color, translit, gloss}` (was `name → hex`). translit/gloss backfilled
from the fragments' hand-written legends by `pipeline/extract_legends.py`
(+ `legend-overrides.json` for the few the heuristic couldn't place, + cross-unit
inheritance for carried-over roots).

**Pipeline:**
- `scan_occurrences.py` → `data/occurrences.json` (per-unit per-root counts + verse anchors)
- `verify_occurrences.py` — independent re-count (token walk, not the scanner's
  regex) + checks every `data-root` resolves to a colour + no two roots in a unit
  within ΔE 11 + tagged-flag consistency
- `apply_retrofit.py` (`retrofit-tags.json`) — adds/​retags/​unwraps root spans
- `build.py` — runs the whole chain

**Retrofit applied to the fragments** (the tracked threads the artifacts never
marked): `nations` 4:15, `apo-tote` 4:17, `law-prophets` 5:17 & 7:12,
`little-faith` 6:30, `light` 5:14 & 6:23, `wise-foolish` 7:24/26; retagged 8:26
"little-faiths" from `faith` → `little-faith`; unwrapped a mis-tagged
"deportation" (author slip — it was `beget`) in U1.

**`app/threads.js`** — colour resolution (global thread → local palette →
verify-fail) + rebuilds each unit's legend from data: tracked threads sorted
first with a "thread" pill, occurrence counts, gloss from `threads.json`. Legend
caption auto-generated. `main.js` / `threads.js` fetches are cache-busted
(`?v=<ts>`); `index.html` tags its script/css `?v=4`.

**Colour collisions fixed** (surfaced by verify after the retrofit): U6 `seen`
→ `#1596b8`; `little-faith` global → `#8f6f9a`.

## Verified on the live deploy

https://lanehaden157.github.io/Matthew/ (commit 3208f00) — every retrofit tag
renders in the verse text, `follow`/`release`/etc. are the same colour in every
unit they appear in, U6 legend shows its thread pills, zero console errors.

## Takeaway / gotcha

The local `python -m http.server` + the in-app browser cache fragments **very**
stickily — `ctrl+shift+r` and even `cache: no-store` didn't reliably dislodge
`unit-01.html` / `unit-06.html` this session. Trust `verify_occurrences.py`
(reads disk) and a fresh-origin fetch, not the dev tab. Production (Pages, fresh
origin, real cache headers) was correct first try.

## Next — Phase 5: thread & note interactions

- root hover → gloss-only tooltip (desktop; tap on mobile)
- root click → popover: translit + gloss + count-in-unit + (if tracked) the
  trajectory (`opens` / `payoffs` from `threads.json`) with jump links to built units
- "threads active here" footer per unit → (eventually) the dashboard
- footnote jump/return already shipped in Phase 2
