"""Generate data/occurrences.json from the unit fragments.

For every data-root span in units/unit-NN.html: the count per unit, and the verse
numbers it falls in (nearest preceding <span class="n">N</span> within the same
.v block; null when it's in a legend / ring / table / heading).

Never hand-edit data/occurrences.json — re-run this. A sibling verify_occurrences.py
re-derives the same numbers independently.
"""

import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = os.path.join(ROOT, "units")
OUT = os.path.join(ROOT, "data", "occurrences.json")

VBLOCK = re.compile(r'<(div|p)\s+class="v"[^>]*>(.*?)(?=<(?:div|p)\s+class="v"|<(?:section|div|footer|h3)\b|</article>)', re.S)
NUM = re.compile(r'<span class="n">(\d+)</span>')
ROOTSPAN = re.compile(r'data-root="([a-z0-9-]+)"')


def scan_unit(html):
    """count = occurrences in the verse translation only (what a reader sees in
    the text). total = every data-root in the fragment (legend, glosses,
    diagrams too) — kept for verify_occurrences' token cross-check."""
    roots = {}
    for m in VBLOCK.finditer(html):
        seg = m.group(2)
        nums = NUM.findall(seg)
        verse = int(nums[0]) if nums else None
        for r in ROOTSPAN.findall(seg):
            e = roots.setdefault(r, {"count": 0, "verses": [], "total": 0})
            e["count"] += 1
            if verse:
                e["verses"].append(verse)

    for r in ROOTSPAN.findall(html):
        roots.setdefault(r, {"count": 0, "verses": [], "total": 0})["total"] += 1

    for r, e in roots.items():
        e["verses"] = sorted(set(e["verses"]))
    return dict(sorted(roots.items()))


def main():
    data = {}
    for path in sorted(glob.glob(os.path.join(UNITS, "unit-*.html"))):
        slug = os.path.splitext(os.path.basename(path))[0]
        data[slug] = scan_unit(open(path, encoding="utf-8").read())
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    tot = sum(r["count"] for u in data.values() for r in u.values())
    print(f"wrote {OUT} — {len(data)} units, {tot} in-verse root occurrences")


if __name__ == "__main__":
    main()
