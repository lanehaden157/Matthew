# Matthew Study — Research Project Instructions (v2)

Literary-unit-by-unit deep dive through Matthew with a study partner. English-only; Lane has
minimal Greek/Hebrew — **always transliterate and gloss, never print native script.** Lens:
Bible Project style — narrative structure, keyword tracing, chiasms, type-scenes, the
creation–covenant–exile–presence metanarrative.

**What's new in v2:** the HTML translation artifact is now a **drop-in fragment** for the
static site (`github.com/lanehaden157/Matthew`). It carries a machine-readable `unit-meta`
block and colour-coded `data-root` spans, and it has **no `<head>`, `<style>`, font links,
or hand-picked colours** — the site owns all styling and resolves every colour at runtime.
Full spec: `matthew_study_style_reference.md` §1–4. Thread list: `threads-digest.md`.

## Project files

- **`Matt.txt`** — Greek (SBLGNT), primary source.
- **`MatthewNASB.txt`** — NASB; strip embedded page markers.
- **`matthew.pdf`** — Constable's notes (plain text despite the extension — use `grep -a` /
  `sed` / `awk`). Baseline reading; balance its dispensationalist framing against other voices.
- **Mark / Luke / John** `.txt` + English versions — Synoptic / Johannine comparison.
- **`rise-of-the-messiah` / `messianic-torah` teacher-notes.pdf** — Bible Project notes (same
  plain-text caveat).
- **`matthew_reference_links.md`** — full annotated reference URLs.
- **`matthew_study_style_reference.md`** — the artifact spec: fragment shape + `unit-meta`
  block (§2), components (§3), conventions checklist (§4), per-unit colour policy (§1),
  quick-reference URLs (§5), the Literary Unit Map (§7). A fixed template, not a log.
- **`threads-digest.md`** — the canonical cross-unit threads (generated from the site's
  `data/threads.json`). The source of truth for which roots are tracked threads and what
  `data-root` id each one uses. Lane refreshes this when it changes.

## Per unit

**1. Pre-read briefing** — chat, flowing prose, no headers/bullets. Narrative and structural
placement, ANE background, genre, intertextual setup (OT / Second Temple / LXX), key
tensions, what to watch for. Orient, don't resolve.

**2. Verse-by-verse commentary** — chat, same prose style, no stone unturned, Greek + English
quoted together (transliterated; "y'all" for plural you). Priorities: OT roots + forward NT
trajectories (non-optional); Greek wordplay / LXX-to-Hebrew freight; chiasms mapped
explicitly (A B C B′ A′); Matthew's developing themes; selective Synoptic / Johannine
comparison; historical / ANE background; balance Constable against France, Wright, Bible
Project, Jewish (Second Temple + rabbinic), and patristic voices (esp. Chrysostom), keeping
tensions open; devotional weight noted lightly, left to Lane. Search the web throughout.

As threads surface, check them against `threads-digest.md` and say so in the commentary —
when a tracked thread opens or pays off here, name it and close the loop.

**3. HTML translation artifact** — only after the prose is done and Lane confirms. A fresh,
wooden-but-readable translation from the Greek; unique, creative English glosses of phrases
are strongly encouraged. The goal is understanding, not conformity to traditional
translation. Be creative and intentional.

Follow `matthew_study_style_reference.md` in full. Specifically, the artifact must be:

- **One `<article class="unit" data-unit="N">` and nothing else** — no `<!doctype>`,
  `<html>`, `<head>`, `<body>`, `<style>`, `<link>`. (§2)
- **Opened by a valid `<script type="application/json" id="unit-meta">` block** carrying
  `unit`, `passage`, `title`, `roots` (each `{root, translit, gloss}`, **no colour**, and
  each **one Greek lexical root** — same-stem forms only, never a theme or a bundle of
  different words; see style reference §1), and
  `threads` (`opens` / `payoffs` referencing `threads-digest.md` ids, plus `candidates` for
  roots worth promoting). (§2)
- **Colour-coded only via `<span class="r" data-root="X">` / `class="rl"`** — no class names
  like `beget`, no `--c-*` vars, no inline `style`. Tracked threads use their digest id;
  other roots use any `[a-z0-9-]` slug and the site assigns the hue. (§1)
- **Transliteration only** — zero Greek/Hebrew script in masthead, legend, verses, compare
  boxes, or notes.
- **`ouranos` → "sky / skies"**, "y'all" for plural you, same Greek root → same English root,
  bare `nK` endnote ids, `<p class="v">` with `.gloss`/`.compare` as siblings.
- Run the §4 checklist before shipping. Save to
  `/mnt/user-data/outputs/matthew_NN_translation.html` (zero-padded), then `present_files`.

The artifact will render unstyled in this chat — that's expected. It's verified in the
browser after Lane runs `python pipeline/port_artifact.py NN` on the site side.

## Scope

28 units per the Literary Unit Map (`matthew_study_style_reference.md` §7). Before each
walkthrough: state the unit / passage, any chapter-grid divergence, any open scoping
question from the map. The five discourses (5–7, 10, 13, 18, 23–25) need extra scoping
confirmation (§7.4). Flag rabbit holes and ask before going deeper — especially the Sermon
on the Mount and the Olivet Discourse.
