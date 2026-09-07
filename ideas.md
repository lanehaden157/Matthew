# Matthew Study — Feature Ideas

Brainstorm from planning the web-app rebuild. Split into what to build first vs. what to
revisit once the core site and a handful of units are live.

---

## Now

- **Footnote jump + return.** Click an endnote ref in the verse text: smooth-scroll
  down to that note and flash-highlight it for ~1s. The note's back-link (or clicking
  the same ref number again) jumps back to the exact verse and briefly highlights it.
  Works without JS as a plain anchor; the highlight + return-to-origin is the JS layer.

- **Root click → thread popover.** Click a colored span: transliteration + gloss (always),
  occurrence count in this unit, and — if it's a tracked cross-unit thread — its trajectory
  ("also in Unit 6, Unit 8 → payoff Unit 14"), with jump links to built units.
- **Root hover → light tooltip.** *(desktop only — see Platform note)* Cheap, quick gloss-only preview on hover, distinct from
  (and lighter than) the click popover. Keeps reading flow unbroken.
- **Compare boxes collapsed by default.** Translation-sensitive verses get a small flag
  icon; click to expand the wooden / NASB / Hart / Lattimore comparison inline, collapse
  again when done. No more breaking the reading rhythm with a box that's always open.
- **Threads dashboard.** A standalone page (separate from the 28 unit tabs) — one entry per
  tracked cross-unit thread, each with a mini timeline across the 28 units showing where it
  appears, open/closed status, and jump links. Canonical home for the global-palette threads.
- **"Threads active here" footer.** On every unit page, a quick list of which tracked
  threads fire in *this* unit, linking out to the dashboard.
- **Global concordance search.** Search bar — type a transliterated root or English gloss,
  get every tagged occurrence across every *built* unit with context snippets. Grows more
  useful as more units ship, so worth having from early on.

---

## Later

- **Isolate-thread toggle.** Click a legend swatch (not just a word) to dim everything on
  the page except that root's occurrences — turns the color-key into an actual filter.
- **Clickable ring/chiasm diagrams.** SVG structure diagrams where clicking node "A" scrolls
  to that verse and highlights its pair "A'" elsewhere on the page.
- **Chiastic reading-order toggle.** A view switch that reflows a unit's translation into
  its ring structure instead of straight reading order.
- **Synoptic side-panel.** Click a verse, slide over the Mark/Luke/John (English) parallel
  inline, pulled from the mounted comparison texts.
- **Root-density sparkline.** Thin strip at the top of a unit showing where each tracked
  root fires across the verses; click a tick to jump there.
- **Book-level heatmap.** One horizontal bar across all 28 units, colored by thread density.
- **Bookend split-view pages.** Paired side-by-side view for inclusios (Unit 1 ↔ 28
  Emmanuel; Unit 5 ↔ 7 Law & Prophets) with tethered verses.
- **Word-level diff in compare view.** Diff the wooden rendering against NASB like a git
  diff, coloring words that got smoothed over or added.
- **Reading progress + local notes.** Mark units read, drop personal verse annotations,
  stored in localStorage.
- **Devotional layer.** Collapsed-by-default "sit with this" box at a unit's end.
- **Constable-vs.-the-room flag.** Inline icon wherever the dispensational reading is held
  in tension with France/Wright/Davies-Allison, expandable to the fuller comparison.

---

## Platform — desktop and mobile, both first-class

The site must look and work well on a phone as well as a desktop. Hover-only
affordances (light root tooltip) degrade to tap on mobile; everything else —
tab nav, thread popovers, compare-box expand, footnote jump, concordance search,
dashboard timelines — must be usable and legible at ~375px wide. Touch targets
sized for thumbs, no horizontal page scroll, diagrams/tables scroll inside their
own container.
