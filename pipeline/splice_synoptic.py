"""Splice the hand-authored synoptic-parallel boxes into units 1-10.

    python pipeline/splice_synoptic.py                 # apply
    python pipeline/splice_synoptic.py --dry            # report only, write nothing

Source: synoptic_parallels_units_01_10.md (chat-produced, one-time retrofit —
not part of the ongoing pipeline). Format per entry:

    ## Unit N — Matthew ...
    ### anchor C:V
    placement: after-verse
    parallels: ...
    why: ...
    ```html
    <aside class="synoptic" data-anchor="C:V">...</aside>
    ```

Each <aside> is inserted as a sibling immediately after its anchor verse's
<p class="v">...</p> — after any .gloss/.compare/.synoptic siblings already
attached to that verse, before the next stop element. Only `after-verse`
placement appears in the source file; that's the only case handled.

Verse -> chapter resolution: the fragments carry no per-verse chapter marker,
so this script tracks the running chapter by parsing each
<h3 class="pericope">... <span>· C:V-V</span></h3> heading's leading chapter
number as it walks the file in order.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_MD = ROOT / "synoptic_parallels_units_01_10.md"
UNITS_DIR = ROOT / "units"

UNIT_HEAD = re.compile(r"^## Unit (\d+) — ", re.M)
ANCHOR_BLOCK = re.compile(
    r"### anchor (\d+:\d+)\n"
    r"placement: (\S+)\n"
    r"parallels: [^\n]*\n"
    r"why: [^\n]*\n"
    r"\n```html\n([\s\S]*?)\n```"
)

PERICOPE_CHAPTER = re.compile(r'<h3 class="pericope">.*?·\s*(\d+):\d+', re.S)
VERSE_OPEN = re.compile(r'<p class="v"><span class="n">(\d+)</span>')
# after a verse paragraph, siblings that stay attached to it
TRAILING_SIB = re.compile(
    r'(?:\s*<span class="gloss">.*?</span>|\s*<div class="compare">.*?</div>|\s*<aside class="synoptic"[^>]*>.*?</aside>)',
    re.S,
)


def parse_source():
    text = SRC_MD.read_text(encoding="utf-8")
    units = {}
    heads = list(UNIT_HEAD.finditer(text))
    for i, m in enumerate(heads):
        n = int(m.group(1))
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        section = text[start:end]
        entries = []
        for am in ANCHOR_BLOCK.finditer(section):
            anchor, placement, html = am.group(1), am.group(2), am.group(3)
            entries.append((anchor, placement, html.strip()))
        units[n] = entries
    return units


def find_verse_end(html, chapter_verse):
    """Return the index right after the anchor verse's <p class="v"> (and any
    trailing gloss/compare/synoptic siblings), tracking chapter via pericope
    headings. Returns None if not found."""
    chapter = None
    pos = 0
    target_ch, target_v = (int(x) for x in chapter_verse.split(":"))
    events = sorted(
        [(m.start(), "h", m) for m in PERICOPE_CHAPTER.finditer(html)]
        + [(m.start(), "v", m) for m in VERSE_OPEN.finditer(html)],
        key=lambda t: t[0],
    )
    for start, kind, m in events:
        if kind == "h":
            chapter = int(m.group(1))
            continue
        verse_num = int(m.group(1))
        if chapter == target_ch and verse_num == target_v:
            end = m.end()
            # <p class="v">...</p> — find the closing tag for THIS paragraph
            close = html.index("</p>", end)
            end = close + len("</p>")
            tm = TRAILING_SIB.match(html, end)
            while tm:
                end = tm.end()
                tm = TRAILING_SIB.match(html, end)
            return end
    return None


def main():
    dry = "--dry" in sys.argv
    units = parse_source()
    total_inserted = 0
    for n in sorted(units):
        entries = units[n]
        path = UNITS_DIR / f"unit-{n:02d}.html"
        html = path.read_text(encoding="utf-8")
        inserted = 0
        skipped = []
        # insert in reverse anchor order isn't necessary since we look up
        # position fresh each time from the (mutating) html string
        for anchor, placement, box_html in entries:
            if placement != "after-verse":
                skipped.append((anchor, f"unhandled placement '{placement}'"))
                continue
            idx = find_verse_end(html, anchor)
            if idx is None:
                skipped.append((anchor, "anchor verse not found"))
                continue
            html = html[:idx] + "\n" + box_html + html[idx:]
            inserted += 1
        if skipped:
            for anchor, reason in skipped:
                print(f"  Unit {n:02d}  SKIP {anchor}: {reason}")
        if inserted:
            print(f"  Unit {n:02d}  inserted {inserted}/{len(entries)}")
            if not dry:
                path.write_text(html, encoding="utf-8")
        elif entries:
            print(f"  Unit {n:02d}  inserted 0/{len(entries)}")
        total_inserted += inserted
    print(f"\n{'[dry run] ' if dry else ''}{total_inserted} boxes spliced.")


if __name__ == "__main__":
    main()
