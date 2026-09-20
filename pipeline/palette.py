"""Colour identity for the two-tier palette: the metrics, the constraints, and
the search that picks a colour for a new root.

WHY THIS EXISTS. Colour is the study's primary way of saying "this word is that
word again". That only works while a reader can tell two colours apart. With 58
tracked threads plus local roots the hue circle is full, so "every root gets a
visibly different colour" is not a constraint that can be met book-wide, and
pretending otherwise produces either a permanently red build or a quietly
meaningless palette.

The constraint that CAN be met, and the one that actually matters to a reader,
is per-unit: two roots need to look different when they appear on the same page.
94 roots appear in built units; only 38% of pairs ever share a unit, and the
densest unit carries 27. Twenty-seven distinguishable colours is comfortable.
Ninety-four is not. So:

  HARD, book-wide     no two threads share a hex. Cheap, and the legend, the
                      concordance and any future canon view all identify a
                      thread BY its colour.
  HARD, book-wide     no root sits on a chrome accent (verse numbers, endnote
                      markers, ring labels). Chrome sits inline next to coloured
                      words; a word the same colour as the verse number in front
                      of it reads as chrome, not as a thread.
  HARD, per-unit      two roots in the SAME unit must be separated. This is the
                      reader-facing rule and the one that scales.
  ADVISORY            close pairs that never co-occur. Worth knowing before a
                      new unit puts them on one page; not worth failing over.

Two metrics, on purpose. CIE76 is plain Euclidean Lab distance and is what the
per-unit check has always used; CIEDE2000 corrects it for how badly it
overstates differences between dark blues. `shake` and `cross` sat dE00 1.68
apart -- below the just-noticeable difference -- while passing CIE76 at 10.6.
A candidate colour has to clear both.
"""
import colorsys
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Thresholds. CIE76 matches the per-unit check's historical value; the dE00
# floors come from what the existing palette can actually sustain -- the closest
# surviving pair after the 2026-09-19 recolour is 3.34.
CO_OCCUR_DE76 = 11.0    # hard: two roots on the same page
CO_OCCUR_DE00 = 6.0     # hard: same, perceptually corrected
CHROME_DE00 = 6.0       # hard: any root vs. a chrome accent
ADVISORY_DE00 = 3.0     # advisory: non-co-occurring pairs closer than this
CONTRAST_MIN = 4.5      # WCAG AA for body text on --bg


def hex_to_lab(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    x = (r * 0.4124564 + g * 0.3575761 + b * 0.1804375) / 0.95047
    y = (r * 0.2126729 + g * 0.7151522 + b * 0.0721750)
    z = (r * 0.0193339 + g * 0.1191920 + b * 0.9503041) / 1.08883
    def f(t): return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def de76(c1, c2):
    a, b = hex_to_lab(c1), hex_to_lab(c2)
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def de2000(c1, c2):
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


def contrast(c1, c2):
    def lum(h):
        h = h.lstrip("#")
        def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = (lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def css_vars():
    """--bg, --ink, --ink-soft and every --accent-* from the stylesheet."""
    path = os.path.join(ROOT, "css", "styles.css")
    if not os.path.exists(path):
        return {}
    text = open(path, encoding="utf-8").read()
    found = dict(re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{6})", text))
    return {k: v for k, v in found.items()
            if k.startswith("accent-") or k in ("bg", "ink", "ink-soft")}


def reserved():
    """Colours a root may not sit on: chrome accents and the two ink values.
    --bg is excluded -- it is the background, and contrast already covers it."""
    return {k: v for k, v in css_vars().items() if k != "bg"}


def background():
    return css_vars().get("bg", "#f5efe2")


def load(name):
    return json.load(open(os.path.join(ROOT, "data", name), encoding="utf-8"))


def all_colors():
    """root -> {color, tier, id, where}.

    A root tracked as a thread takes its global colour and ignores any local
    entry, exactly as threads.js resolves it at runtime.
    """
    out = {}
    for t in load("threads.json")["threads"]:
        out[t["root"]] = {"color": t["color"], "tier": "thread",
                          "id": t["id"], "where": ["threads.json"]}
    for u in load("units.json")["units"]:
        for root, v in (u.get("roots") or {}).items():
            if root in out:
                if out[root]["tier"] == "local":
                    out[root]["where"].append(u["slug"])
                continue
            out[root] = {"color": v["color"] if isinstance(v, dict) else v,
                         "tier": "local", "id": root, "where": [u["slug"]]}
    return out


def cooccurring_pairs(occ=None):
    """Unordered root pairs that appear in at least one built unit together.
    This is the graph the hard per-unit rule is really about."""
    occ = occ if occ is not None else load("occurrences.json")
    pairs = set()
    for _unit, roots in occ.items():
        rs = sorted(roots)
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                pairs.add((rs[i], rs[j]))
    return pairs


def propose(avoid, n=6, prefer_hue=None):
    """Rank candidate colours by how far the WORST conflict is.

    `avoid` is {label: hex} -- everything the new colour must stay away from.
    Returns [(hex, min_de00, min_de76, nearest_label)], best first. Candidates
    are drawn from the palette's own character (the lightness and saturation
    band the existing threads occupy) so a proposal looks like it belongs.
    """
    bg = background()
    scored = []
    hues = range(0, 360, 2) if prefer_hue is None else range(prefer_hue - 20, prefer_hue + 21)
    for h in hues:
        for lt in range(22, 51, 2):
            for st in range(28, 76, 4):
                r, g, b = colorsys.hls_to_rgb((h % 360) / 360, lt / 100, st / 100)
                hx = "#%02x%02x%02x" % tuple(round(c * 255) for c in (r, g, b))
                if contrast(hx, bg) < CONTRAST_MIN:
                    continue
                worst00, near = min(((de2000(hx, c), lbl) for lbl, c in avoid.items()),
                                    default=(999.0, None))
                if worst00 < CO_OCCUR_DE00:
                    continue
                worst76 = min((de76(hx, c) for c in avoid.values()), default=999.0)
                if worst76 < CO_OCCUR_DE76:
                    continue
                scored.append((round(worst00, 2), hx, round(worst76, 2), near))
    scored.sort(reverse=True)
    out = []
    for d00, hx, d76, near in scored:
        if all(de2000(hx, prev[0]) > 8 for prev in out):
            out.append((hx, d00, d76, near))
        if len(out) >= n:
            break
    return out
