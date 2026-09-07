"""Independently re-derive occurrence counts and check colour resolution.
Does NOT import scan_occurrences — re-counts with a line-oriented tokeniser so a
bug in one approach doesn't hide in both.

Checks:
  1. per-unit, per-root counts match data/occurrences.json
  2. every data-root in every fragment resolves to a colour
     (threads.json global OR units.json local)
  3. no two distinct roots in one unit render within a small perceptual distance
  4. threads.json roots marked tagged:true actually appear in some fragment;
     tagged:false roots do NOT appear yet
Exit non-zero on any failure.
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = os.path.join(ROOT, "units")
DATA = os.path.join(ROOT, "data")

fail = []


def load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


def recount(html):
    """Token-by-token count, independent of scan_occurrences' regex structure."""
    counts = {}
    for tok in html.replace(">", "> ").split():
        if tok.startswith('data-root="'):
            r = tok.split('"')[1]
            counts[r] = counts.get(r, 0) + 1
    return counts


def hex_to_lab(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    x, y, z = x / 0.95047, y, z / 1.08883
    def f(t): return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def de(c1, c2):
    a, b = hex_to_lab(c1), hex_to_lab(c2)
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def main():
    occ = load("occurrences.json")
    threads = {t["root"]: t for t in load("threads.json")["threads"]}
    units = {u["slug"]: u for u in load("units.json")["units"]}

    for path in sorted(glob.glob(os.path.join(UNITS, "unit-*.html"))):
        slug = os.path.splitext(os.path.basename(path))[0]
        html = open(path, encoding="utf-8").read()
        mine = recount(html)
        theirs = {r: v["total"] for r, v in occ.get(slug, {}).items()}
        if mine != theirs:
            fail.append(f"{slug}: count mismatch\n   verify={mine}\n   json  ={theirs}")

        # colour resolution + collision
        local = (units.get(slug, {}) or {}).get("roots", {})
        resolved = {}
        for r in mine:
            if r in threads:
                resolved[r] = threads[r]["color"]
            elif r in local:
                lc = local[r]
                resolved[r] = lc["color"] if isinstance(lc, dict) else lc
            else:
                fail.append(f"{slug}: data-root '{r}' resolves to NO colour")
        items = list(resolved.items())
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                d = de(items[i][1], items[j][1])
                if d < 11:
                    fail.append(f"{slug}: '{items[i][0]}' {items[i][1]} and "
                                f"'{items[j][0]}' {items[j][1]} too close (dE={d:.1f})")

    # thread tagged-flag sanity
    all_roots = set()
    for path in glob.glob(os.path.join(UNITS, "unit-*.html")):
        all_roots |= set(recount(open(path, encoding="utf-8").read()))
    for t in load("threads.json")["threads"]:
        present = t["root"] in all_roots
        if t.get("tagged") and not present:
            fail.append(f"thread '{t['id']}' tagged:true but root '{t['root']}' not in any fragment")
        if not t.get("tagged") and present:
            fail.append(f"thread '{t['id']}' tagged:false but root '{t['root']}' IS in a fragment — flip the flag")

    if fail:
        print("FAIL")
        for f in fail:
            print(" -", f)
        sys.exit(1)
    print("occurrences verified — counts match, every root resolves, no collisions")


if __name__ == "__main__":
    main()
