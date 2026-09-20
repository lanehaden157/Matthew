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
  5. book-wide: no two threads share a hex. The global tier promises "that
     thread's fixed colour in every unit", so two threads on one hex is a
     broken promise even when they never co-occur and check 3 stays quiet.
  6. book-wide, ADVISORY: the closest thread pairs by CIEDE2000, and any
     thread that sits on a chrome accent from css/styles.css. Never fails —
     at 58 threads a strict palette threshold is unreachable and a red build
     you've decided to live with is worse than no check. It prints the
     ceiling so you can see it coming.
Exit non-zero on any failure.
"""

import glob
import json
import math
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


def de2000(c1, c2):
    """CIEDE2000. Used only by the book-wide palette checks below; the per-unit
    check above keeps its plain CIE76 distance and its own threshold. Raw Lab
    distance badly overstates how different two blues look, which is how
    'shake' and 'cross' sat 1.7 apart for eleven units without anyone noticing.
    """
    L1, a1, b1 = hex_to_lab(c1)
    L2, a2, b2 = hex_to_lab(c2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))) if Cb else 0.5
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    else:
        dhp = h2p - h1p - 360 if h2p > h1p else h2p - h1p + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2
    else:
        hbp = (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30))
         + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6))
         - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) if Cbp else 0.0
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * (30 * math.exp(-(((hbp - 275) / 25) ** 2))))) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                     + Rt * (dCp / Sc) * (dHp / Sh))


def chrome_accents():
    """--accent-* / --ink / --ink-soft from the stylesheet, for the advisory."""
    css = os.path.join(ROOT, "css", "styles.css")
    if not os.path.exists(css):
        return {}
    text = open(css, encoding="utf-8").read()
    return dict(re.findall(r"--((?:accent-|ink)[\w-]*)\s*:\s*(#[0-9a-fA-F]{6})", text))


def check_palette(threads):
    """5 (hard) + 6 (advisory). Book-wide, independent of what's tagged."""
    by_hex = {}
    for t in threads:
        by_hex.setdefault(t["color"].lower(), []).append(t["id"])
    for hexv, ids in sorted(by_hex.items()):
        if len(ids) > 1:
            fail.append(f"threads {', '.join(sorted(ids))} all share {hexv} — "
                        f"the global tier promises one fixed colour per thread")

    pairs = []
    for i in range(len(threads)):
        for j in range(i + 1, len(threads)):
            pairs.append((de2000(threads[i]["color"], threads[j]["color"]),
                          threads[i]["id"], threads[j]["id"]))
    pairs.sort()
    print(f"palette: {len(threads)} threads, closest pairs by CIEDE2000 "
          f"(advisory; ~2.3 is the just-noticeable difference)")
    for d, a, b in pairs[:5]:
        print(f"  dE00 {d:5.2f}  {a} / {b}")

    for name, hexv in sorted(chrome_accents().items()):
        near = [(de2000(t["color"], hexv), t["id"]) for t in threads]
        d, tid = min(near)
        if d < 6:
            print(f"  advisory: thread '{tid}' sits dE00 {d:.2f} from "
                  f"--{name} ({hexv}) — a coloured word and a piece of chrome "
                  f"reading as the same colour")


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

    check_palette(load("threads.json")["threads"])

    if fail:
        print("FAIL")
        for f in fail:
            print(" -", f)
        sys.exit(1)
    print("occurrences verified — counts match, every root resolves, no collisions")


if __name__ == "__main__":
    main()
