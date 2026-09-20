"""Independently re-derive occurrence counts and check colour resolution.
Does NOT import scan_occurrences — re-counts with a line-oriented tokeniser so a
bug in one approach doesn't hide in both. (It does import pipeline/palette.py,
which is policy and metrics, not a generator.)

Checks:
  1. per-unit, per-root counts match data/occurrences.json
  2. every data-root in every fragment resolves to a colour
     (threads.json global OR units.json local)
  3. HARD, per-unit: no two roots ON THE SAME PAGE render too close, by BOTH
     CIE76 and CIEDE2000. This is the reader-facing rule and the one that
     scales — see pipeline/palette.py for why it is per-unit and not book-wide.
  4. threads.json roots marked tagged:true actually appear in some fragment;
     tagged:false roots do NOT appear yet
  5. HARD, book-wide: no two threads share a hex. The global tier promises
     "that thread's fixed colour in every unit", and the legend, concordance
     and any future canon view identify a thread BY its colour — so two threads
     on one hex is a broken promise even when check 3 stays quiet.
  6. HARD, book-wide: no root sits within dE00 6 of a chrome accent or an ink
     value from css/styles.css. Chrome renders inline beside coloured words;
     sixteen roots used to sit on chrome, eleven byte-identical.
  7. ADVISORY: close pairs that never co-occur, and per-unit headroom. Never
     fails — two roots that share no page are not a reader problem, they are
     something to know before a future unit puts them together.
Exit non-zero on any failure.
"""

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import palette as P  # noqa: E402

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


def check_thread_hexes(threads):
    """5. Two threads may not share a hex, co-occurring or not."""
    by_hex = {}
    for t in threads:
        by_hex.setdefault(t["color"].lower(), []).append(t["id"])
    for hexv, ids in sorted(by_hex.items()):
        if len(ids) > 1:
            fail.append(f"threads {', '.join(sorted(ids))} all share {hexv} — "
                        f"the global tier promises one fixed colour per thread")


def check_chrome():
    """6. No root may sit on the furniture."""
    reserved = P.reserved()
    for root, m in sorted(P.all_colors().items()):
        for name, hexv in reserved.items():
            d = P.de2000(m["color"], hexv)
            if d < P.CHROME_DE00:
                fail.append(
                    f"root '{root}' {m['color']} ({m['tier']}) sits dE00 {d:.2f} "
                    f"from --{name} {hexv} — a coloured word and a piece of "
                    f"chrome reading as the same colour. Move one, or run "
                    f"`python pipeline/assign_color.py {root} --recolour`")


def report_headroom(occ):
    """7. Advisory. What is close but harmless, and how much room is left."""
    colors = P.all_colors()
    co = P.cooccurring_pairs(occ)

    near_safe = []
    keys = sorted(colors)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = keys[i], keys[j]
            if (a, b) in co:
                continue
            d = P.de2000(colors[a]["color"], colors[b]["color"])
            if d < P.ADVISORY_DE00:
                near_safe.append((d, a, b))
    near_safe.sort()

    tight = []
    for slug in sorted(occ):
        rs = [r for r in occ[slug] if r in colors]
        worst = None
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                d = P.de2000(colors[rs[i]]["color"], colors[rs[j]]["color"])
                if worst is None or d < worst[0]:
                    worst = (d, rs[i], rs[j])
        if worst:
            tight.append((worst[0], slug, len(rs), worst[1], worst[2]))

    print(f"palette: {len(colors)} roots carry a colour; "
          f"{len(co)} pairs share a unit")
    if tight:
        d, slug, n, a, b = min(tight)
        print(f"  tightest page: {slug} ({n} roots) — {a} / {b} at dE00 {d:.2f} "
              f"(JND is ~2.3)")
    if near_safe:
        print(f"  {len(near_safe)} close pair(s) that never co-occur "
              f"(harmless today, worth knowing):")
        for d, a, b in near_safe[:5]:
            print(f"    dE00 {d:5.2f}  {a} / {b}")
    print("  `python pipeline/assign_color.py --audit` for the full picture; "
          "`assign_color.py <root>` to pick one.")


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

        # colour resolution + per-unit collision (check 3)
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
                (ra, ca), (rb, cb) = items[i], items[j]
                d76, d00 = P.de76(ca, cb), P.de2000(ca, cb)
                if d76 < P.CO_OCCUR_DE76 or d00 < P.CO_OCCUR_DE00:
                    fail.append(f"{slug}: '{ra}' {ca} and '{rb}' {cb} too close "
                                f"on one page (dE76={d76:.1f}, dE00={d00:.2f})")

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

    check_thread_hexes(load("threads.json")["threads"])
    check_chrome()
    report_headroom(occ)

    if fail:
        print("FAIL")
        for f in fail:
            print(" -", f)
        sys.exit(1)
    print("occurrences verified — counts match, every root resolves, "
          "no collisions, chrome clear")


if __name__ == "__main__":
    main()
