# Matthew Study — Resources

Read this before pass 1 of every unit. Cite only the commentators below by name. Where they can't reach something (a lead, a background question, a cross-reference), say so in the relevant pass and search the web there. Don't stretch one of them past its actual content.

This file lives in the repo and syncs to the project, like everything in the synced folder. Edit it in the repo, never on the project side. If a synced file and an uploaded copy disagree, the synced one wins; say so rather than quietly picking one.

## Texts

- **`MatthewSBLGNT.txt`** (synced). The Greek, one verse per line: `Matt C:V<TAB>text`. Extract a passage: `sed -n '/^Matt 7:1\t/,/^Matt 8:1\t/p' MatthewSBLGNT.txt | sed '$d'`.
- **`MatthewNASB.txt`** (uploaded to the project). The NASB, for the compare boxes. Strip the injected page markers: `sed -E 's/Gospel of Matthew NASB Page \| [0-9]+//g'`.
- **Mark, Luke and John `.txt`** plus English versions (uploaded). For Synoptic and Johannine comparison.
- **`translation-choices.md`** (synced). The agreed English renderings. Check before rendering a Greek word and match it; if a different rendering genuinely fits a verse better, use it but flag it in the artifact so Lane can call it a one-off or a correction.
- **`matthew_reference_links.md`** (synced). The annotated list of outside sources, by kind. Go here when a pass needs a Second Temple text, the LXX in English, or a patristic reading.
- **`canon-leads-unit-NN.md`** (synced). Pass 3's starting list for that unit. If the current unit's sheet isn't there, ask for it.
- **`threads-digest.md`** (synced). The tracked threads: check roots against it as they surface.

## Commentary

- **Constable, notes on Matthew** (`matthew.pdf`, uploaded). Plain text despite the extension; use `grep -a`, `sed` and `awk`, and navigate by a `grep -a -n` header scan, then `sed -n 'START,ENDp'`. The dispensationalist baseline reading.
- **Bible Project teacher notes** (`rise-of-the-messiah` and `messianic-torah` `teacher-notes.pdf`, uploaded; same plain-text caveat). They cover Matthew 1–8 only. From chapter 9 on, draw the literary-canonical side from the Bible Project podcast series, France and Wright (links in `matthew_reference_links.md`), and say which you leaned on.

## The synced folder

`synced-index.md` in the synced folder lists every file the repo mirrors there and what each one is for. It's generated on every sync, so it's always complete.
