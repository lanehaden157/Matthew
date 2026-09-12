# Session summary — 2026-09-12 — translation-choices audit + rulings applied

## What was done

**Audit.** Scripted a dump of the actual English inside every `data-root`
span in the verse text (`p.v` + the `.prayer` block) of units 1–11, plus
greps for style-convention terms (heaven, faith, disciple, Lord, Christ,
Baptist, behold, amen, synagogue, leper, soul…). Rewrote
`translation-choices.md` so each row described what the units actually say,
not what the glossary data implied. Surfaced ~12 real inconsistencies and
asked Lane to rule on each.

**Rulings applied.** Lane answered all 12 in one message. Reworded across
units 1–11 to match:
- metanoia → **turn** (3:2/3:8/3:11 already were; fixed 4:17, 11:20, 11:21)
- mercy (eleos) → **loyal-love**, but may drift by context (5:7 fixed)
- wage, not reward (5:12, 5:46 fixed)
- gentle, not meek (5:5 fixed)
- "Father in the skies," not "heavenly Father" (5:48, 6:14, 6:26, 6:32)
- Immerser, not Baptizer (11:11–12)
- dikaios family may drift by context — kept as-is (righteous/just/
  right-doing/upright/in the right)
- stupid, not foolish (7:26 — kept as-is, already matched)
- fulfill formula → **filled full**, unhyphenated (1:22, 2:15, 2:17, 2:23,
  4:14, 8:17)
- synagōgē — both "synagogues" and "gathering-places" stand
- lepros rendered literally (10:8 "skin-diseased" → "cleanse the leprous")
- look, not behold (units 1–2, six places)
- amen, not truly (11:11)
- y'all's for plural possessive (11:17 "your chests" → "y'all's chests")
- life/being, not soul (11:29 "your souls" → "y'all's beings")
- "pulled apart with care," extended to 10:19 (was "anxious")
- good-news keeps its hyphen everywhere (one Greek word)
- **acts of power**, not miracles — promoted to a new global thread
  (dynamis), tagged at 7:22 and 11:20–23

**Tagging fixes** (structural, not wording): untagged 6:12 "debts"/"debtors"
(wrongly colored as `release`, a different Greek root); consolidated 1:17's
four "generations" onto one root (was double-tagged); tagged the `learn`
verb at 9:13 and 11:29 (only the noun was tagged before); tagged `deeds` in
11:2/11:19's actual verse text (was tagged only in the structure diagram);
fixed the unit-11 ring diagram's "the Christ" → "the Anointed"; corrected
three stale `threads.json` glosses.

**Thread promotions.** Three roots that recurred in a second unit as a side
effect of the wording fixes were promoted from local to global colour:
immerse (unit-03 → 11), anxious (unit-06 → 10), clean (unit-08 → 10). New
colours were picked with a script using `verify_occurrences.py`'s own CIE76
Lab-distance formula against every colour active in the affected units —
two rounds of manual guesses collided before switching to that.

**Build.** `pipeline/build.py` ran clean after each change.
`retrofit-tags.json` needed its recorded literal text updated on 6 entries
so the retrofit replay stayed idempotent against the new wording. Final
state: 11 units, 575 in-verse occurrences, 0 colour collisions, 0 coverage
gaps across 41 audited threads.

## Takeaways
- The glossary had been written from `threads.json`/`units.json` glosses,
  not the actual unit text — worth re-auditing periodically rather than
  trusting it silently.
- The `learn` thread's coverage gap (verb untagged, only the noun caught)
  is a pattern worth watching for other threads that mix noun and verb forms
  of the same root.

## Open questions
None outstanding — all 12 calls from the audit were resolved this session.
The three newly-promoted threads plus `acts-of-power` (and 7 pre-existing
threads) still have no Greek stems in `pipeline/thread-stems.json`, so
`audit_thread_coverage.py` flags them as advisory-only "undefined." Not
blocking; fold in during a future stems pass, same as past sessions.
