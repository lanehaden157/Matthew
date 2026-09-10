# Prompts for the Claude.ai research project

Paste-ready asks for the project that reads the Greek closely. Each produces
structured data the code side ingests directly.

---

## 1. Greek stems for the 16 undefined tracked threads

**Attach to the project:** `pipeline/thread-stems.json` (current version — for the
format and the 8 worked examples) and `MatthewSBLGNT.txt` (unless the project
already has the SBLGNT Greek of Matthew — it must be the same text). Everything
else the prompt needs is inline below.

**Prompt:**

> I've attached `thread-stems.json` and the SBLGNT Greek of Matthew. I need
> `thread-stems.json` entries for the 16 tracked threads that don't have one yet.
> That file drives a script that scans the Greek text for every morphological
> occurrence of a thread's root and flags any that a built unit leaves untagged.
> The 8 entries already in the file (sin, fear, sea, follow, fish, authority,
> hand-over, cross) are the pattern to follow.
>
> **How the matcher works** (so your stems are right): a Greek word matches a
> thread if its **accent-stripped, lowercased** form **contains** any string in
> `stems`, and is not listed in `exclude`. Substring, not prefix — because the
> augment and reduplication break prefixes (ἠκολούθησεν and ἀκολουθεῖ are the
> same verb; a stem of `ακολουθ` misses the first, so the entry needs both
> `ακολουθ` and `ηκολουθ`). Give stems **without accents**, lowercase.
>
> For each thread below, give me:
> - `stems`: the minimal set of accent-stripped Greek fragments that catches
>   **every** inflected form of this lexeme in Matthew (all tenses/cases, with
>   and without augment) and nothing from an unrelated lexeme.
> - `exclude`: accent-stripped whole word-forms that a stem unavoidably catches
>   but that belong to a **different** word (homographs). Example already in the
>   file: `sin` excludes `καταμαρτυρουσιν` ("testify against" — the μαρτυρ root,
>   not ἁμαρτ).
> - A short prose note listing any **compound verbs** you're unsure about —
>   e.g. for ἀφίημι, whether συνίημι / ἀφίημι / etc. should count. I'll decide
>   those with Lane; default to **excluding** a compound unless it's clearly the
>   same thread.
>
> **Check yourself against what's already tagged.** For each thread I've listed
> the verses the built units (Matthew 1–10) currently tag. Your stems, run over
> chapters 1–10, should hit **at least** those verses (more is fine and
> expected — the whole point is finding misses). If your stems would *miss* a
> currently-tagged verse, the stem set is wrong.
>
> Threads (translit · gloss · currently-tagged):
>
> | id | translit | gloss | tagged now in units 1–10 |
> |----|----------|-------|--------------------------|
> | build | oikodomeō | build | U7 7:24, 7:26 |
> | faith | pistis · pisteuō | trust, faith | U8 8:10, 8:13; U9 9:2, 9:22, 9:28, 9:29 |
> | foolish | mōros | foolish / dull | U5 5:13, 5:22; U7 7:26 |
> | fringe | kraspedon | tassel / hem | U9 9:20 |
> | light | phōs | light | U4 4:16; U5 5:14, 5:16; U6 6:22, 6:23; U10 10:27 |
> | lose | apollymi | lose, destroy, be lost | U2 2:13; U5 5:29, 5:30; U7 7:13; U8 8:25; U9 9:17; U10 10:6, 10:28, 10:39, 10:42 |
> | mercy | eleos · eleeō | loyal-love, covenant-kindness | U5 5:7; U6 6:2, 6:3, 6:4; U9 9:13, 9:27 |
> | nations | ethnē | nations / Gentiles | U4 4:15; U5 5:47; U6 6:7, 6:32; U10 10:5, 10:18 |
> | release | aphiēmi | release / forgive / leave | U3 3:11, 3:15; U4 4:20, 4:22; U5 5:24, 5:40; U6 6:14, 6:15; U7 7:4; U8 8:15, 8:22; U9 9:2, 9:5, 9:6 |
> | rock | petra | rock (bedrock) | U7 7:24, 7:25 |
> | save | sōzō | save / heal / rescue | U1 1:21; U8 8:25; U9 9:21, 9:22; U10 10:22 |
> | shake | seismos | shaking / earthquake / storm | U8 8:24 |
> | throw | ballō | throw / cast out | U8 8:6, 8:12, 8:14, 8:16, 8:31; U9 9:2, 9:16, 9:17, 9:25, 9:33, 9:34; U10 10:1, 10:8, 10:34, 10:38 |
> | torment | basanizō | torment | U8 8:6, 8:29 |
> | urge | parakaleō | urge / entreat / call alongside | U2 2:18; U5 5:4; U8 8:5, 8:31, 8:34 |
> | wise | phronimos | shrewd / prudent | U7 7:24; U10 10:16 |
>
> Notes on the hard ones (your call, but flag your reasoning):
> - **release** (ἀφίημι) — the thread deliberately spans "release / forgive /
>   leave", so ἀφῆκεν "left [the nets]" (4:20) counts. But ἀφ- is a very common
>   prefix; you'll need `exclude` for ἀφ- words that aren't ἀφίημι.
> - **throw** (βάλλω) — the thread explicitly includes "cast out" (ἐκβάλλω), so
>   compounds of -βαλλω mostly count here. Confirm which.
> - **light** (φῶς / φωτ-) — must **not** catch φωνή "voice" or ἀδελφῷ "brother".
> - **mercy** (ἐλε-) — must **not** catch Ἐλεάζαρ, τέλειος, ἤθελεν, ἐλεύσεται.
> - **lose** (ἀπόλλυμι) — must **not** catch ἀπολύω "release/divorce" (5:31–32)
>   or Δεκάπολις.
> - **save** (σῴζω) — there are **no** σωζ- forms in Matthew; it's σωσ- / σωθ- /
>   σεσω- / (augmented) ἐσώθη.
>
> Output: a JSON object I can drop straight into `thread-stems.json`'s `stems`
> map (16 keys), plus the compound-verb notes as prose below it.

**After it answers:** paste into `pipeline/thread-stems.json`, then

```bash
python pipeline/audit_thread_coverage.py --forms <ids…>   # eyeball every matched form
python pipeline/audit_thread_coverage.py <ids…>           # coverage gaps in built units
```

Fix `exclude` for any junk `--forms` shows; re-run until each thread is `✓ clean`
or its gaps are real misses to retro-tag.
