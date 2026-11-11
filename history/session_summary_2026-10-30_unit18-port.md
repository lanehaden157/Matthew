# Session summary — 2026-10-30, unit 18 port

**Done:** Ported unit 18. The dry run failed on metadata: the `kerdainō` root was non-ASCII, and `retro[]` (validated against tracked threads) conflicted with `promote[]` (rejects already-tracked threads). Promoted `debt`, `gain`, `mikros` by hand, moved their unit-18 payoffs into `payoffs[]`, and dropped `promote[]`. Applied the thread delta (28 payoffs). Dropped the duplicate `skandalon` retro at 17:27. Added retrofit adds for `mikros` (10:42, 11:11, 13:32) and `gain` (16:26). Build, audit (0 gaps), test (10 ok) green.

**Takeaways:** the chat side should either list new threads in `promote[]` with no `retro[]` pointing at them, or the porter should count `promote[]` ids as tracked in the retro check (core change, not made). Chat-side roots should be ASCII ([a-z0-9-]).

**Open:** nothing committed or synced. LXX checks: Esth 1:14 partial (lemmas horaō/prosōpon absent; the `!blepō` half holds); NT refs are not LXX-checkable (15 `?`). `long-tempered`/`mikros` are 8.0 ΔE apart in unit 18. `adelphos` candidate held by Lane.
