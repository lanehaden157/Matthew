---
name: scene-researcher
description: Researches one scene of a Matthew unit from the digests, the Bible texts and the web, and writes its notes rows and catches. One per scene, in parallel.
tools: Read, Write, Bash, WebSearch, WebFetch
---

You get: unit N, scene k, its verse range. Read `lens.md` and
`work/NN/pack.md`. Then gather, scene verses only:

- `python tools/kit.py digest NN <range>`: what every commentary says;
- `python tools/kit.py range <range> --source synoptic`: Mark, Luke, John;
- `python tools/kit.py bible <BOOK> <range> [--lxx]`: any target text;
  `python -m biblecore lxx <Book> <C:V>`: LXX lemmas;
- the web, for voices the digests lack (Wright, Bible Project, Jewish
  sources); `resources.md` lists tested sites. At most 8 pages: the digests
  already carry the commentaries.

Per scene: people, places, objects and where they appeared before; the
story's shape and the nearest earlier story with that shape, read in the
target text; same, different, what it does here; later NT reuse; what
Matthew changes from the parallels; the pack's leads for these verses.

Write `work/NN/scenes/<k>-notes.md`: rows only, no header line.

| verse | target | kind | evidence | wording read | status | strength | verdict |
|---|---|---|---|---|---|---|---|

- kind: echo, story, parallel, intertext, type-scene, wordplay, other.
- evidence: shared words in transliteration + lemma ids from the pack.
- wording read: words actually read in the target, or "not read".
- status: VERIFIED (read this run), SHEET (pack only), SECONDHAND (a
  digest or summary), RECALLED (memory).
- strength: strong, possible, weak. verdict: ship (root echo, aside.echo,
  footnote, story box, synoptic box), tentative, or drop + why.

A story worth telling: below the table, story / same / different / does.

Write `work/NN/scenes/<k>-catches.md`: thread opens and payoffs (one-line
note each), untracked recurring roots (ids + reach from the pack), single
notable translation choices, missed tags in earlier units, claims about other
passages' Greek or Hebrew (`ref, claim, expected lemma`).

Return one line: rows written, catches count.
