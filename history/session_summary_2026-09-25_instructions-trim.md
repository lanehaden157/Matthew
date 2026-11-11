# Session summary — 2026-09-25: instruction files trimmed

**Done**
- Confirmed the intertext pass was already adopted (2026-09-22). The unit-13 canon-leads
  sheet exists and is synced, and regenerating it produced identical output.
- `instructions.md` (pasted into the Claude.ai project) and `CLAUDE.md` trimmed to light
  files of pointers. Anything that existed only in them was moved first: the named-commentator
  rule and `.gloss` marker placement went to style ref §4, the 1–12 backlogs to PLAN.md,
  and the units.json-wins gotcha to the `refresh_meta.py` docstring.
- `apply_retrofit.apply_text` idempotency bug fixed. Insert-style ops (`from` ⊂ `to`)
  duplicated on every build. The only live casualty was the 12:26 gloss, which was
  reverted before commit.

**Takeaway:** Lane wants instruction files light, pointing to where the real info lives
and not doing heavy technical lifting.

**Open**
- Lane should re-paste `instructions.md` into the research project's instructions field.
- PLAN.md's "Open question for Lane" (Phase 1 Greek strip) looks long settled. It's
  worth pruning some time.
