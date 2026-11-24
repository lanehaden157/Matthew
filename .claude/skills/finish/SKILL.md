---
name: finish
description: Conductor for building many Matthew units. Starts one session per unit, keeps about three researching at once, and lets builds land in unit order. Use when Lane says "finish Matthew", "do units 20-24", or asks where the units stand.
---

# Conductor

1. `python tools/unit_status.py` (all units, main checkout and worktrees).
2. For each unit in range not started, in order: `start_session`
   (`initiation: "user_asked"`, `use_worktree: true`, `context: "fresh"`,
   title `Matthew unit N`, prompt `/unit N`). At most three units in steps 1-4
   at once; start the next when one reaches calls.
3. When a unit session reports back, check its files, then:
   - reached calls → tell Lane in one line which units have calls waiting,
     with links, earliest unit first (earlier answers can change later units);
   - shipped → `SendMessage` the next unit's session to resume its build if
     it was waiting on order.
4. Never answer Lane's calls, never merge a unit's branch by hand: each unit
   session ships itself.
