# Session summary 2026-10-30: instruction trim

**Done.** Ranked the Matthew instruction docs, took 12 decisions from Lane, then trimmed them.
Instruction field 916 → 552 words; style reference 37 → 16 KB, renumbered to core's section
layout with a validated worked example in §8; `CLAUDE.md` 11 → 5 KB; `translation-choices.md`
27 → 11 KB; `resources.md` absorbed `matthew_reference_links.md` (15 → 8 KB); unit map 10 → 8 KB.
`PLAN.md` and the finished one-offs are in `archive/docs-2026-10-30/`. The retrofit recipe is
in `docs/retrofit.md`.

In bible-core (uncommitted): `canon/workflow.md`, `handoff-template.md` and `conventions.md`
trimmed; `digest.py` drops columns that say the same thing on every row; `components` no
longer doubles headings; compare snippet uses the `div` form units use.

**Lane's decisions.** Claude decides promotion and asks when unsure. Component markup lives
only in `components-reference.md`. The checklist holds judgment items only. Echoes are judged,
not automatic. Terms are reintroduced at first use per unit. `PLAN.md` is archived. The field
is lens plus chat routing. Lane sees Claude slip most in the build chat and long sessions.

**Also fixed.** Added the 23 thread rows missing from `translation-choices.md`, using renderings
tallied from the units, and the unit 15-16 rulings that were never recorded (hampers, little
dogs, fitting, Hades, adulterous, bound/loosed). Removed the dead `emmanuel` tag instruction.

**Checks.** `biblecore test` 9/9, worked example valid. Core 379/380: the one failure is
`test_numbers_passes_biblecore_test`, because Numbers' committed digest predates `digest.py`.
A release rebuilds it.

**Open.**
- Commit, core release and `core_sync --all`, push, `sync` in each book, re-paste Matthew's
  field. Until then the vendored `core-workflow.md`, handoff template and
  `components-reference.md` in Matthew are still the old text.
- apistos: unit 17 ships "not-trusting", but the 2026-10-29 log names "trustless" as a ruling
  that isn't recorded anywhere else. Marked for Lane in `translation-choices.md`.
- Not yet tried on a real research or build chat.
