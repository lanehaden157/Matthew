---
name: finish
description: Conductor for many Matthew units. One session per unit, about three studying at once, builds in unit order. Use for "finish Matthew", "do units 20-24", or "where do units stand".
---

1. `python tools/unit_status.py`.
2. Each unit in range not started, in order: `start_session` (`initiation: "user_asked"`, `use_worktree: true`, `context: "fresh"`, title `Matthew unit N`, prompt `/unit N`). Max three before calls; next starts when one reaches calls.
3. Unit session reports:
   - at calls → tell Lane which units wait, links, earliest first (early answers can change later units);
   - shipped → `SendMessage` next unit's session to resume build if it waited.
4. Never answer Lane's calls. Never merge unit branches by hand.
