# Session summary — 2026-09-19 — G5: Matthew hygiene

Implements group **G5** of `platform-design-review.md`: B2, B5, B6, B7, B4, plus
the live bug behind B8. B1 and B3 were deliberately left out — both belong to the
core extraction (G6/G7) and doing them now means doing them twice.

## What was done

Ordered as worked: the live defect first, then correctness, then hygiene, then
the new sync folder.

1. **Unit 11's missing legend.** Units 1–10 each carry a
   `section.block.legend`; unit 11 had none, so the page rendered coloured words
   with no key. Added it in the same position the other ten use.
2. **B2 — the palette.** Five threads recoloured, plus two new book-wide checks
   in `verify_occurrences.py`. Details in `improvements_log.md`.
3. **B6 — stale text.** CLAUDE.md status, style reference §7.2, `units.json`
   `_note`, `egerō`→`egeirō`.
4. **B5 — unit 2's legend data.** Three wrong rows fixed; the 44 shadowed local
   roots kept, per Lane.
5. **B7 — the fork drafts.** Archived under `docs/audit/archive/joshua-fork-plan/`
   with a banner on each.
6. **B4 — `project-side/`.** Joshua's pattern, Matthew's file list, two
   deliberate divergences (below).

## Takeaways

- **The per-unit collision check could not have caught B2.** It only compares
  roots that appear in the *same* unit, and none of the colliding sets co-occur
  yet. The promise the global tier makes ("this thread's fixed colour in every
  unit") is book-wide, so the check has to be book-wide too. Generalises: a
  check scoped more narrowly than the invariant it defends will pass forever
  and still be wrong.
- **Raw Lab distance overstates how different two blues look.** `shake` and
  `cross` sat 1.68 apart in CIEDE2000 — below the just-noticeable difference,
  i.e. literally the same colour to a reader — while passing a CIE76 threshold
  of 11. Both metrics are now in the file, each with its own threshold, and the
  new picks satisfy both.
- **58 threads is close to the ceiling.** After this pass the closest surviving
  pair is dE00 3.34 (`test`/`learn`), and finding five replacement colours that
  cleared both metrics needed a search, not an eye. This is review item H11
  arriving on the colour axis before the reading axis. The fix when it arrives
  is display-side (a per-unit "quiet" set, or the isolate-thread toggle in
  `ideas.md`), not more palette.
- **`refresh_meta.py` regenerates fragment meta from `units.json`.** Editing
  unit 2's meta block directly looked right and was silently reverted by the
  next build. "Fragments are the source of truth" holds for prose and tagging,
  not for legend metadata. Now stated in CLAUDE.md.
- **Chrome accents duplicate thread colours.** `--accent-gold`, `--accent-slate`
  and `--accent-warm` are byte-identical to `lose`, `cross` and `save`. Reported
  as advisory, not fixed — see open questions.

## Open questions

- **The chrome-accent overlap.** Verse numbers, endnote markers and ring labels
  use hexes that three threads also own, and verse numbers sit inline next to
  coloured words. Fixing it means either moving three threads or giving the
  chrome its own reserved hues; the second is better but is a design change, not
  hygiene, so it was left for a decision.
- **`test` / `learn` at dE00 3.34.** Above the JND, below comfortable. Worth a
  nudge next time either is touched; not worth a recolour on its own.
- **Should `instructions.md` be synced?** Currently out of TRACKED_FILES,
  matching the Joshua call. If the research project's instructions field is meant
  to point at the repo copy rather than restate it (review D6/H12), it should go in.
- **B8's other half** — making the legend a validated requirement — is still
  open, and belongs with B1's validator work in the core extraction.

## Divergences from Joshua, on purpose

- **No scheduled task.** Joshua syncs every 15 minutes from Task Scheduler;
  review A10/H9 flags the commit noise. `build.py` already runs after every
  change that matters.
- **`--copy-only` in the build.** The build refreshes the mirror in the working
  tree but never commits or pushes it, so the mirror lands in the same commit as
  the change that caused it, and no script pushes on its own.

## State

`pipeline/build.py` green: 11 units, every root resolves, no collisions, 0
coverage gaps across 41 audited threads. Unchanged from before this session:
11 threads still have no Greek stems (advisory), and the 6 phrase threads remain
hand-audited — both retire with B3.

**Not verified in a browser.** The colour changes and the unit-11 legend need an
eyeball on the live page.

---

# Part 2 — chrome desaturation and a palette that scales

Asked for after part 1: fix the chrome overlap, and make the palette survive a
growing thread count.

## Correction to part 1

Part 1 said "58 threads is near the ceiling", from ranking thread colours
book-wide. That was the wrong measurement. 95 roots carry a colour, but only
37% of pairs ever appear in the same unit and the densest page holds 27. The
constraint that matters is per-unit, and after this pass every built unit's
tightest pair is dE00 >= 6.05 against a just-noticeable difference of ~2.3.
There is room to keep adding threads; what there is not room for is picking
their colours by eye.

## What changed

- **Chrome is now low-chroma.** Sixteen roots sat on a chrome accent, eleven
  byte-identical — `beget`, `deeds` and `judge` were all exactly the verse-number
  crimson. The stylesheet already claimed chrome was "independent of any unit's
  root palette"; now it is. Saturated colour belongs to the thread system alone.
- **`pipeline/palette.py`** holds the whole colour policy: both metrics, the
  thresholds, the chrome accents parsed from the stylesheet, the co-occurrence
  graph, the candidate search.
- **`pipeline/assign_color.py`** picks colours. A local root only has to clear
  its own unit, which is a far weaker constraint than a thread's, so it gets
  better colours — the tool knows the difference.
- **The verifier enforces the right rule**: per-unit separation on both metrics
  (hard), no thread sharing a hex and no root on chrome (hard, book-wide),
  everything else advisory with per-unit headroom reported.
- Five roots moved to clear the new bar.

## Takeaway

The rule that failed here was not "too close" but "scoped wrong". A book-wide
uniqueness rule is unsatisfiable at 95 roots and would have forced the
thresholds down until they meant nothing; a per-unit rule is both satisfiable
and the one a reader actually experiences. Scope the check to the invariant,
then the threshold can stay honest.

## Still open

- The five new chrome neutrals are unreviewed on a real page. They change the
  look of every unit — verse numbers, headings, ring labels, the Greek title.
- `test`/`learn` at dE00 3.34 never co-occur, so the check is quiet. If a future
  unit puts them together the build will fail and one of them moves.
