# Chat-side findings from the unit 16 port (2026-10-28)

Source: `source-artifacts/matthew_16_translation.html`. Port, build, audit (0 gaps) and
`python -m biblecore test` (9 ok) are green. These are notes for the research project's
instructions and the artifact the chat side hands over, ranked by how much code-side time they save.

## 1. Don't re-ask rulings that already exist (4 of 6 questions)

The porter surfaced 6 `questions[]`. Only two were real decisions (promote `anointed`/`blessed`;
the 16:19 perfect "will have been bound").

- **christos "Anointed One"**: `translation-choices.md` and 11:2 already rule this. The artifact
  flagged it "in case Lane wants 'the Christ'". Put such a note in the artifact's prose, not `questions[]`.
- **kophinos/spyris "baskets/hampers"**: settled at unit 15. Same for Hades / "adulterous" (matches 12:39).
- Rule for the chat side: read `translation-choices.md` + prior units' meta before raising a question;
  a question must have a genuinely open alternative the unit's argument depends on.
- Lane had to answer 5 popups; 3 could have been zero.

## 2. Code-side checks belong in their own field, not `questions[]`

The sixth "question" (Greek-text checks: Isa 22:22 key, Isa 38:10 / Wis 16:13, Deut 5:26 / Josh 3:10,
Isa 51:1–2, 2 Sam 22:2 / Deut 32, Ezek 16:32 / Hos 3:1) has no options and isn't for Lane. It rendered
as an unanswerable popup item. Suggest a separate `checks_for_code[]` (or a section in the notes file),
and ask the chat side to give each as `book chapter:verse, claim, expected lemma(s)` so it can be run as-is.

I ran them against the LXX corpus (Rahlfs 1935). Results the chat side can rely on:

| Claim | Result |
|---|---|
| Isa 22:22 has no word for "key" | confirmed (no *kleis*; "the glory of David") |
| "gates of Hades": Isa 38:10, Wis 16:13 | confirmed (*pylē* + *hadēs*) |
| "living God": Deut 5:26, Josh 3:10 | confirmed (*theos* + *zaō*) |
| Isa 51:1–2 petra and Abraham | confirmed (*petra* 51:1, Abraham 51:2) |
| 2 Sam 22:2 petra for the LORD | confirmed (*petra mou*) |
| Deut 32 has no petra for God | confirmed (only *petra* is 32:13, honey from the rock) |
| Ezek 16:32 / Hos 3:1 adulterous wife | **partly**: Hos 3:1 has *moichalis*; Ezek 16:32 has the verb *moichaomai* ("the wife who commits adultery"), not *moichalis*. Worth a precise wording in the artifact. |

Not checked (as the artifact itself says): Mark/Luke/John boxes follow lemmas + English summaries only.

## 3. Hand over thread promotions as ready JSON

The thread delta only covers existing threads. For promotions the code side had to look up every
occurrence's unit by hand and write `opens`/`payoffs`. If the artifact (or notes file) included, per
candidate: `id`, `root`, lemma id(s), gloss, `opens` {unit, ref}, `payoffs` [{unit, ref, note}], one-line
`note`, this becomes paste-in work. Use the unit map for unit numbers. Done here for `anointed` (christos,
16 uses) and `blessed` (makarios, 13 uses).

## 4. Promotion is the expensive step: flag it earlier

Promoting two roots needed 17 hand-written `add` retrofit entries (unit 1 ×4, 2, 5 ×9, 11 ×2, 13) because
those words had no span at all in the boxed units. Knowing a candidate's reach before the artifact is
final would let Lane rule before the port rather than during it. Suggest the research pass lists, for any
proposed new thread, the verses/units it reaches (the `Matthew-words.tsv` count is enough) and says "this
needs retrofit in N units". Then promotion can be decided with the cost in view.

## 5. Stale / duplicate refs the chat side noticed

- The artifact said the son-of-man thread files 16:13 under the old unit 17. Confirmed and fixed (the 16:13
  row had been under unit 17 from the earlier plan; now unit 16, with 16:27 left under 17). The
  chat side can't see `threads.json` per unit, so a one-line "check thread rows citing this unit's verses"
  in the instructions would catch these on the code side sooner.
- The `sign` thread's digest payoffs were empty; unit 16:1 is now its first payoff.

## 6. Cosmetic, for the code side (not the chat side)

- Unit 11 renders "the Anointed" (v2) next to "the Anointed One" (v3 and the unit 16 usage). Boxed unit,
  left as shipped; flagged for Lane if rendering is ever harmonised.
- New thread colour `blessed #a00020` sits 8.1 ΔE from `evil` and 8.3 from `seek` (limit 7, so passes,
  with a validate warning in unit 16). `anointed` is 8.3 from `son-of-man`. Fine; recolour if it looks muddy.

## 7. Candidate code-side streamlining (for the improvements list, not chat)

- `audit` could print retrofit-ready `add` JSON for untagged gaps (unit, verse, root, w, candidate text);
  today it prints the gap and I wrote the JSON by hand (script in session).
- `port` could apply accepted thread promotions from a `promotions.json` the chat side provides (items 3 and 4 above).
- `port --dry` prints questions with no `--answers` file; accepting answers from a file would save a re-read.
- An LXX lookup command (`python -m biblecore lxx Isa 22:22`) would make the checks in section 2 a one-liner;
  I used `load_greek_corpus()` in a scratch script.
- `data/*.json` writes show a CRLF→LF git warning on Windows (checkout line endings); cosmetic.
