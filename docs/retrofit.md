# Retrofit recipe

Promoting a thread makes every occurrence in every built unit need `data-w`, boxed units
included. Usually `python -m biblecore data-w N` fills them in place; what it can't decide,
and the port's coverage gaps, go in `retrofit/retrofit-tags.json`.

Per promoted root, per unit, for the verses `data-w` reports as undecided:

1. Compare the root's occurrences in `Matthew-words.tsv` for the verse with the fragment's
   `<span class="r" data-root="ROOT">` spans, in order.
2. Where the counts differ, look closer: one span over two source words (one `retag`, or
   split by hand); one source word as two English spans (keep the span a reader recognises
   as the word and `unwrap` the other, or give both the same `w` with `retag`'s `occ`); or a
   truly untagged occurrence (`add`).
3. Same root and same text twice in a verse: `retag`'s `occ` (1-based); for `add`, the `w`
   makes each entry idempotent on its own word id.
4. One entry per occurrence: `{"unit", "verse", "from", "to", "text", "w"}`. In a unit that
   crosses a chapter, `verse` is `"C:V"`.
5. Re-run `python -m biblecore build` (it replays the retrofit file and audits); every
   promoted root should report clean. In a boxed unit, diff it afterwards: only tag spans and
   `data-w` may differ.
