# Matthew Study — Resources

Read this before pass 1 of every unit. **This list is a starting point, not a limit.** The project holds very little on purpose; search the web freely and draw on whatever serves the passage: France, Wright, Davies & Allison, Keener, Turner, Nolland, Hagner, Luz, Jewish and patristic sources, journal articles, anything. Name commentators and tell Lane which you leaned on. Read the passage before attributing a view to someone; anything not read in this chat is marked "recalled, unverified". Paraphrase, and keep any direct quote short.

This file lives in the repo and syncs to the project, like everything in the synced folder. Edit it in the repo, never on the project side. If a synced file and an uploaded copy disagree, the synced one wins; say so rather than quietly picking one.

## In the project

- **`MatthewSBLGNT.txt`** (synced). The Greek, one verse per line: `Matt C:V<TAB>text`. Extract a passage: `sed -n '/^Matt 7:1	/,/^Matt 8:1	/p' MatthewSBLGNT.txt | sed '$d'`.
- **`MatthewWEB.txt`** (synced). The World English Bible (public domain), same line format as the Greek: `Matt C:V<TAB>text`. It's an English comparison text, not the study's own translation. It keeps the WEB's verse numbering, so it has three verses the SBLGNT omits (17:21, 18:11, 23:14, marked `[not in the SBLGNT]`). Converted 2026-10-02 from ebible.org's `eng-web_usfm.zip` (Strong's tags and footnotes stripped).
- **`translation-choices.md`** (synced). The agreed English renderings. Check before rendering a Greek word and match it; if a different rendering genuinely fits a verse better, use it but flag it in the artifact so Lane can call it a one-off or a correction.
- **`matthew_reference_links.md`** (synced). The annotated list of outside sources, by kind: Second Temple texts, the LXX in English, patristic readings.
- **`canon-leads-unit-NN.md`** (synced). Pass 3's starting list for that unit. If the current unit's sheet isn't there, ask for it.
- **`threads-digest.md`** (synced). The tracked threads: check roots against it as they surface.
- **Constable, Notes on Matthew** (2026 edition; uploaded as `/mnt/project/matthew.pdf`). The dispensational baseline. Plain text despite the `.pdf` extension, with CRLF line endings: read it with `grep -a` / `sed`, never a PDF tool. Find a section by its outline heading, which appears twice (once in the outline near line 600, once in the body), and take the second hit: `grep -a -n 'withdrawal to Tyre and Sidon' matthew.pdf`, then `sed -n 'START,ENDp' matthew.pdf | tr -d ''`. Running page headers ("Dr. Constable's Notes on Matthew 2026 Edition" plus a page number) interrupt the text; strip them with `grep -a -v "Constable's Notes on Matthew"`. Read him here, don't recall him. `constable-index.md` (synced) lists every outline section with its body line range (for example 15:1-20 → 13311-13524): go straight to those lines with `sed -n`. StudyLight's copy is the 2012 edition and is usually bot-blocked; use it only as a fallback.
- **Bible Project teacher notes** (`rise-of-the-messiah` and `messianic-torah` `teacher-notes.pdf`, uploaded; plain text despite the extension, so use `grep -a`, `sed` and `awk`). They cover Matthew 1-8 only. From chapter 9 on, draw the literary-canonical side from the Bible Project podcast series and the web, and say which you leaned on.

## On the web (URL patterns checked 2026-10-03 from Claude Code, not from the chat project)

Tool rule: the fetch tool only opens a URL that appeared in a search result, an earlier fetched page, or Lane's message. A URL built from the patterns below is refused, so search for the exact page first and fetch the link the search returns; fetching a site's table-of-contents page first also unlocks its chapter links. The patterns say where a page lives (to recognise the right search result, or a link on a contents page), not what to type. `curl` does not work: the sandbox allowlist excludes these sites. StudyLight bot-blocks intermittently (the book index fetched on 2026-10-03, the chapter page did not); retry once in the `www.studylight.org` form before giving up. When a page can't be reached, say so and mark the source "recalled, unverified" rather than working from search excerpts as if they were the page.

**Other StudyLight commentaries: the same page pattern with a different code.** `https://www.studylight.org/commentaries/eng/<code>/matthew-N.html`
- Barclay, Daily Study Bible (1956-59), code `dsb`: pastoral, strong on Palestinian background. Still under copyright, so paraphrase only.
- Ellicott, Commentary for English Readers (1878), code `ebc`: Anglican, verse by verse.

Same bot-block risk as above; BibleHub carries Ellicott (`biblehub.com/commentaries/ellicott/matthew/N.htm`) as an alternative (the page loads from Claude Code, checked on chapters 13 and 15; search for it, then fetch the result).

**Catena Aurea (Aquinas, 1842 Parker translation): the Fathers chained by verse; CCEL, one page per chapter.** Table of contents: `https://www.ccel.org/ccel/aquinas/catena1.toc.html`. Chapter N = `https://www.ccel.org/ccel/aquinas/catena1.ii.<N in lowercase Roman numerals>.html` (ch. 13 = `catena1.ii.xiii.html`): clean text in verse blocks, each excerpt labeled by the Father quoted. Avoid `isidore.co/aquinas/english/CAMatthew.htm` (one page, later chapters cut off, garbled characters). The Catena's Chrysostom homily numbers do not match New Advent's; don't use them to look up homilies.

**Chrysostom, Homilies on Matthew: New Advent, one homily per page.** Homily N = `https://www.newadvent.org/fathers/2001NN.htm`, N as two digits (Homily 44 = `200144.htm`); each page opens with its passage. To find which homilies cover a passage, use the CCEL table of contents `https://www.ccel.org/ccel/schaff/npnf110.toc.html`: passages are listed in order, and Homily 1 has none, so the first passage line is Homily 2. Matthew 13: Homilies 44 (starts 12:46), 45 (13:10), 46 (13:24), 47 (13:34), 48 (13:53). Don't use the full PDF; it's too large to fetch usefully.

**J. C. Ryle, Expository Thoughts on Matthew (1856): evangelical, devotional; CCEL, one page per section.** Table of contents: `https://ccel.org/ccel/ryle/matthew/matthew.toc.html`. Section URL = `matthew.<chapter + 1 in Roman numerals>.<section>.html` (13:1-23 = `matthew.xiv.i.html`), but check the contents first: chapter 14 sits under `xiv` too (14:22-36 = `xiv.v`), 14:1-21 is at the end of the 13:51-58 page (`xiv.iv`), and 22:34-46 is at the end of `xxii.iii`; neither has its own contents line.

**Edersheim, Life and Times of Jesus the Messiah (1883): Jewish background; CCEL.** Ordered by event, not by Matthew chapter. Table of contents: `https://ccel.org/ccel/edersheim/lifetimes/lifetimes.toc.html`. Find the event there, or in Index II of Gospel passages, `lifetimes.xiii.html` (the Matthew 13 parables = `lifetimes.viii.xxiii.html`).

**BibleProject: literary design and the metanarrative.** The Matthew guide, `https://bibleproject.com/guides/book-of-matthew/` (also in the instruction field, so it can be fetched directly), links to the related articles and podcast episodes. The guide page loads from Claude Code; the links on it are untested.

France, Wright, Davies & Allison and the rest have no tested page set: search for them each time (publisher previews, Google Books, journal articles, reviews), and say when you could only reach a summary.

## The synced folder

`synced-index.md` in the synced folder lists every file the repo mirrors there and what each one is for. It's generated on every sync, so it's always complete.
