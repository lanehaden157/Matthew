# docs/audit/archive

Superseded planning documents, kept because they record *why* things were
decided, not *what is true now*. Nothing in here is an instruction.

## `joshua-fork-plan/` (2026-09-12)

Six documents planning the fork of Matthew's pipeline into a Hebrew book.
Joshua was built from this plan and then diverged from it — substring stems
gave way to lexicon-id sets, `candidates[].stems` was dropped, the masthead
and endnote shapes changed. The plan is still the clearest statement of the
reasoning behind the fork, which is why it is kept rather than deleted.

Two things in here have not been superseded and are wanted by the shared core
when it is extracted (see `platform-design-review.md` D8):

- `BOOTSTRAP.md`'s irreversibility tiers — which decisions are cheap to change
  later and which rewrite every shipped unit.
- `ARCHITECTURE.md`'s opening argument for fork-before-generalize, which the
  review restates as H1.

Live documents live in the Joshua repo (`../Joshua/`). The current
cross-project plan is `platform-design-review.md` in the repo root.
