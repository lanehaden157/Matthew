# Session summary — 2026-10-25: earlier-story boxes and the pass reorder

**Done** (from `intertext-build-prompt.md`)
- bible-core 0.17.0 (`79db418`, tag `v0.17.0`): `components/story` (`aside.story`: `par-title`/`par-ref` header, `par-story`, `par-match`, `par-diff`, `par-does`, `par-later`; validator for anchor, kind, strength, `data-scene` on type-scenes, required parts, translit only, no `data-root`). spotlight.js toggle `labels` puts a word on a chip (pill style in core.css). canon.py harvests story boxes (source "story"; kinds gain story, character, reuse). leads.py: Greek noun sweep. `canon/workflow.md`: briefing, research (notes file, one line in chat), verse-by-verse (tells the stories, ends with the artifact list), artifact; standing moves now in pass 3. Synoptic snippet: no cap.
- Vendored into Numbers, Joshua, Matthew (builds and tests green). Matthew enables `story`; style reference, instruction field, theme.css updated.

**Lane's calls**
- Story accent: slate blue (`--accent-olive`; Matthew's "olive" token is blue, its synoptic is plum and its echo ochre).
- Noun-sweep filter: stoplist of stock nouns (God, lord, Jesus, word, human, man, day, hour, time, part, name, faith, truth, disciple, crowd, thing, way); nouns on the rare list are not repeated. 50 rows for unit 15.

**Takeaways**
- The core suite takes ~4–5 min and its sibling-write guard trips if a book is edited mid-run; keep books quiet during `release.py`. Proposed a separate session to speed the suite up.
- Kept the prompt's `par-*` class names. "story" kept as the component name.

**Open**
- Not pushed: bible-core (+ tag), Numbers, Joshua, Matthew. Then `biblecore sync` in each book (chat-side files changed).
- Lane re-pastes `CHAT_SIDE_INSTRUCTIONS.md`, then `sync-check --mark-pasted`.
- Pilot: Lane runs unit 15 through the new loop; then `port 15 --force`, diff, ask before committing. Unit 14 waits.
- Delete `previews/` and both handoff files once the pilot lands (ask first).
- Endnote-marker §3 vs §4 point still unruled.
