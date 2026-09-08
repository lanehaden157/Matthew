"""Phase 1 - Extract & normalize.

source-artifacts/matthew_NN_translation.html  ->  units/unit-NN.html
  - body content only (no <head>, <style>, font links)
  - all native Greek/Hebrew script removed; transliteration kept or synthesised
  - tracked-root spans   -> class="r"  data-root="X"
  - unit-local colour spans (no .r) -> class="rl" data-root="X"
  - endnote ids/hrefs prefixed per unit (n3 -> u07-n3)
  - local palette + metadata -> pipeline/out/units.seed.json
  - every synthesised translit / Hebrew span / leftover script char
    -> pipeline/out/extract-report.md

Prose is never edited - only tags, ids, removed script.
"""

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from greek import transliterate  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source-artifacts")
OUT_UNITS = os.path.join(ROOT, "units")
OUT_PIPE = os.path.join(ROOT, "pipeline", "out")

GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")
HEBREW = re.compile(r"[֐-׿יִ-ﭏ]")
SCRIPT = re.compile(r"[Ͱ-Ͽἀ-῿֐-׿יִ-ﭏ]")
GREEK_RUN = re.compile(r"[Ͱ-Ͽἀ-῿][Ͱ-Ͽἀ-῿'’̀-ͯ\s]*[Ͱ-Ͽἀ-῿]|[Ͱ-Ͽἀ-῿]")
HEBREW_RUN = re.compile(r"[֐-׿יִ-ﭏ][֐-׿יִ-ﭏ\s]*[֐-׿יִ-ﭏ]|[֐-׿יִ-ﭏ]")

report = []


def log(m):
    report.append(m)


def normalize_blocks(body, u):
    """Unit 1's colour-key section is `class="legend"` where every other unit
    has `class="block legend"` — so it renders without the panel box. Also flag
    ring-diagram labels longer than a letter or two (e.g. "HINGE") so CSS can
    size them down to fit the narrow label column."""
    before = body
    body = body.replace('<section class="legend"', '<section class="block legend"')
    if body != before:
        log(f"- U{u}: normalised legend section to `block legend`")

    body, k = re.subn(
        r'<div class="lab">(?=[A-Za-z]{3})([^<]+)(<small>|</div>)',
        r'<div class="lab lab-word">\1\2', body)
    if k:
        log(f"- U{u}: marked {k} long ring label(s) lab-word")
    return body


_TAG = re.compile(r"<(/?)div\b[^>]*>", re.I)


def _match_close(s, open_end):
    """Given s and the index just past a `<div …>`, return the index of its
    matching `</div>` (start) by counting nested divs."""
    depth = 1
    for m in _TAG.finditer(s, open_end):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.start()
    return -1


def normalize_verses(body, u):
    """Unit 1 was built before the verse conventions settled: its verses are
    <div class="v"><span class="n">N</span><span class="txt">…</span> with the
    .gloss/.compare blocks nested INSIDE (and compare uses div.row/.lab). Every
    other unit has <p class="v">…</p> with those blocks as following siblings.
    Reshape U1 to match so the shared engine treats it like the rest."""
    out, i, k = [], 0, 0
    for m in re.finditer(r'<div class="v"><span class="n">(\d+)</span>'
                         r'<span class="txt">', body):
        out.append(body[i:m.start()])
        n = m.group(1)
        close = _match_close(body, m.end())          # matches <div class="v">
        if close < 0:
            out.append(body[m.start():m.end()]); i = m.end(); continue
        inner = body[m.end():close]                  # inside .v, after <span class="txt">
        cut = re.search(r'</span>\s*(?=<div class="(?:gloss|compare)">)', inner)
        if cut:
            txt = inner[:cut.start()]
            blocks = _blocks_to_spans(inner[cut.end():])
        else:
            txt = re.sub(r'</span>\s*$', '', inner)
            blocks = ""
        out.append(f'<p class="v"><span class="n">{n}</span>{txt.strip()}</p>')
        if blocks.strip():
            out.append("\n      " + blocks.strip())
        i = close + len("</div>")
        k += 1
    out.append(body[i:])
    if k:
        log(f"- U{u}: normalised {k} nested-gloss verses to sibling form")
    return "".join(out)


def _blocks_to_spans(s):
    """Turn U1's nested <div class="gloss/compare"> … <div class="row"><span
    class="lab"> into the shared <span class="…"> / <span class="row"> /
    <span class="src"> shape, closing tags correctly by depth."""
    for cls in ("gloss", "compare"):
        while True:
            o = re.search(r'<div class="' + cls + r'">', s)
            if not o:
                break
            end = _match_close(s, o.end())
            inner = s[o.end():end]
            if cls == "compare":
                inner = re.sub(r'<div class="row">', '<span class="row">', inner)
                inner = re.sub(r'<span class="lab">', '<span class="src">', inner)
                inner = _close_rows(inner)
            s = s[:o.start()] + f'<span class="{cls}">' + inner + "</span>" + s[end + len("</div>"):]
    return s


def _close_rows(s):
    out, i = [], 0
    for m in re.finditer(r'<span class="row">', s):
        out.append(s[i:m.end()])
        j = _first_div_close(s, m.end())
        out.append(s[m.end():j] + "</span>")
        i = j + len("</div>")
    out.append(s[i:])
    return "".join(out)


def _first_div_close(s, start):
    m = re.search(r"</div>", s[start:])
    return start + m.start() if m else len(s)


def get_body(html):
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    body = m.group(1)
    m = re.search(r'<div class="wrap">(.*)</div>\s*$', body.strip(), re.S)
    if m:
        body = m.group(1)
    return body.strip()


def local_palette(html):
    return dict(re.findall(r"--c-([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,8})", html))


def fix_greek_title(body, u):
    def repl(m):
        raw = re.sub(r"<span[^>]*>|</span>", "", m.group(1))
        left, dash, right = raw.partition("—")  # em dash
        if dash and SCRIPT.search(left):
            body_txt = right.strip()          # left is Greek script -> discard
        elif dash:
            body_txt = (left.strip() + ", " + right.strip()).strip(", ")
        else:
            body_txt = raw.strip()
        gm = re.match(r'([^,·"“]+?)\s*(?:[,·]\s+|\s*(?=["“]))(.*)$', body_txt)
        if gm and gm.group(1).strip():
            translit, gloss = gm.group(1).strip(), gm.group(2).strip(' ,·"“”')
        else:
            translit, gloss = body_txt.strip(' ,·"“”'), ""
        gloss = re.sub(r'",?\s+', " ", gloss).replace('"', "").strip(" ,")
        if SCRIPT.search(translit):
            translit = transliterate(translit)
        out = f'<span class="translit">{translit}</span>'
        if gloss:
            out += f' — <span class="tsub">{gloss}</span>'
        return f'<div class="greek-title">{out}</div>'

    return re.sub(r'<div class="greek-title">(.*?)</div>', repl, body, flags=re.S)


GKSPAN = r'<span class="gk">([^<]*)</span>'
_TRANSLITISH = r'[a-zà-ɏ][a-zà-ɏāēīōūȳăĕĀ-ſḀ-ỿ \-\'’.…]*'


def strip_gk_spans(body, u):
    # 1. .tr wrapper internals:  (<gk>G</gk>, translit)  ->  (translit)
    body = re.sub(GKSPAN + r'\s*,\s*(?=' + _TRANSLITISH + r'\)?)', "", body)

    # 2. <gk>G</gk> (translit)  ->  <span class="translit">translit</span>
    def paren(m):
        inner = m.group(2).strip()
        if SCRIPT.search(inner):
            inner = transliterate(inner)
        return f'<span class="translit">{inner}</span>'

    body = re.sub(GKSPAN + r'\s*\((' + _TRANSLITISH + r')\)', paren, body)

    # 3. any remaining bare <gk>G</gk>
    def bare(m):
        g = m.group(1).strip()
        if not SCRIPT.search(g):
            return g  # latin mislabelled as gk
        t = _translit_token(g, u)
        return "" if t is None else f'<span class="translit">{t}</span>'

    return re.sub(GKSPAN, bare, body)


# Hand corrections the deterministic romanizers can't get right (vowel-pointing,
# already-glossed-in-prose). Value None => drop the span entirely.
MANUAL = {
    "נצר": None,
    "שָׁמַיִם": "shamayim",
    "חוֹבָא": "ḥoba",
    "חָנֵף": "ḥanef",
}


def _translit_token(s, u):
    if s in MANUAL:
        v = MANUAL[s]
        log(f"- U{u}: manual `{s}` -> {v!r}")
        return v
    if HEBREW.search(s):
        rom = _rom_hebrew(s)
        log(f"- U{u}: HEBREW `{s}` -> `{rom}`  (REVIEW)")
        return rom
    t = transliterate(s)
    log(f"- U{u}: synth `{s}` -> `{t}`")
    return t


_HEB = {
    "א": "'", "ב": "b", "ג": "g", "ד": "d", "ה": "h",
    "ו": "w", "ז": "z", "ח": "ch", "ט": "t", "י": "y",
    "ך": "k", "כ": "k", "ל": "l", "ם": "m", "מ": "m",
    "ן": "n", "נ": "n", "ס": "s", "ע": "'", "ף": "p",
    "פ": "p", "ץ": "ts", "צ": "ts", "ק": "q", "ר": "r",
    "ש": "sh", "ת": "t",
}


def _rom_hebrew(s):
    return "".join(_HEB.get(c, "" if "֑" <= c <= "ׇ" else c) for c in s)


def clean_redundancy(body):
    # <span class="translit">X</span> (X)  or  , X   ->  drop the echo
    body = re.sub(
        r'(<span class="translit">([^<]+)</span>)\s*\(\s*\2\s*\)', r"\1", body)
    body = re.sub(
        r'(<span class="translit">([^<]+)</span>),\s*\2\b', r"\1", body)
    body = re.sub(
        r'(<span class="translit">([^<]+)</span>)\s*\(\s*<span class="tr">\2</span>\s*\)',
        r"\1", body)
    # collapse "(<span class=translit>X</span>)" left inside old .tr wrappers
    body = re.sub(r'<span class="tr">\(\s*(<span class="translit">[^<]+</span>)\s*\)</span>',
                  r"\1", body)
    # translit">X</span>[</span>...] (X[,;] ...)  -> drop the echoed X at paren head
    body = re.sub(
        r'(<span class="translit">([^<]+)</span>)((?:</span>)*\s*\()\s*\2\s*[,;]\s*',
        r"\1\3", body)
    # orphaned punctuation left by a dropped script span
    body = re.sub(r"\(\s*,\s*", "(", body)
    body = re.sub(r"\(\s*\)", "", body)
    body = re.sub(r"<em>\s*</em>", "", body)
    return body


def strip_leftover_script(body, u):
    """Transliterate bare script runs in VISIBLE TEXT only. Script inside a tag
    (e.g. Greek in a Logeion href) is left as-is — wrapping it in a <span> there
    would break the markup, and Greek URLs resolve fine."""
    def gk(m):
        t = _translit_token(m.group(0), u)
        return "" if t is None else f'<span class="translit">{t}</span>'

    def heb(seg, m):
        s = m.group(0)
        tail = seg[m.end():m.end() + 4]
        if tail.lstrip().startswith("("):
            log(f"- U{u}: dropped bare Hebrew `{s}` (translit follows in parens)")
            return ""
        t = _translit_token(s, u)
        return "" if t is None else f'<span class="translit">{t}</span>'

    out = []
    for part in re.split(r"(<[^>]+>)", body):
        if part.startswith("<"):
            out.append(part)
        else:
            part = GREEK_RUN.sub(gk, part)
            part = HEBREW_RUN.sub(lambda m: heb(part, m), part)
            out.append(part)
    return "".join(out)


# normalise a few inconsistent data-root spellings to one canonical name
ROOT_ALIASES = {"wild": "wilderness"}


def rewrite_roots(body, palette, u):
    names = set(palette)

    def two(m):
        a, b = m.group(1), m.group(2)
        root = b if a == "r" else a
        return f'class="r" data-root="{ROOT_ALIASES.get(root, root)}"'

    body = re.sub(r'class="(r) ([a-z0-9-]+)"', two, body)
    body = re.sub(r'class="([a-z0-9-]+) (r)"', two, body)

    # drop inline colour overrides that referenced per-unit CSS vars (now gone);
    # colours come from data/units.json + data/threads.json at render time
    body = re.sub(r'(<span class="r[l]?"[^>]*?)\s*style="color:var\(--c-[^"]*"', r"\1", body)

    def bare(m):
        cls = m.group(1)
        if cls in names:
            return f'<span class="rl" data-root="{ROOT_ALIASES.get(cls, cls)}">'
        return m.group(0)

    body = re.sub(r'<span class="([a-z0-9-]+)">', bare, body)
    return body


def prefix_endnotes(body, u):
    p = f"u{u}-"
    body = re.sub(r'id="(n\d+)"', lambda m: f'id="{p}{m.group(1)}"', body)
    body = re.sub(r'href="#(n\d+)"', lambda m: f'href="#{p}{m.group(1)}"', body)
    return body


def _title(html):
    m = re.search(r"<h1>([^<]*)</h1>", html)
    return m.group(1).strip() if m else ""


def _passage(html):
    m = re.search(r'class="unit">\s*Unit\s*\d+\s*[··]\s*([^··<]+)', html)
    return m.group(1).strip() if m else ""


def main():
    os.makedirs(OUT_UNITS, exist_ok=True)
    os.makedirs(OUT_PIPE, exist_ok=True)
    seed = {}

    for path in sorted(glob.glob(os.path.join(SRC, "matthew_*_translation.html"))):
        u = re.search(r"matthew_(\d+)_", path).group(1)
        html = open(path, encoding="utf-8").read()
        palette = local_palette(html)
        body = get_body(html)

        log(f"\n## Unit {u}")
        body = normalize_verses(body, u)
        body = normalize_blocks(body, u)
        body = fix_greek_title(body, u)
        body = strip_gk_spans(body, u)
        body = clean_redundancy(body)
        body = strip_leftover_script(body, u)
        body = clean_redundancy(body)
        body = rewrite_roots(body, palette, u)
        body = prefix_endnotes(body, u)

        visible = re.sub(r"<[^>]+>", "", body)   # script may remain inside hrefs
        script_left = bool(SCRIPT.search(visible))
        if script_left:
            log(f"- U{u}: !! SCRIPT STILL PRESENT in visible text")

        roots = sorted(set(re.findall(r'data-root="([a-z0-9-]+)"', body)))
        missing = [r for r in roots if r not in palette]
        if missing:
            log(f"- U{u}: data-root with no local colour: {missing}")

        seed[f"unit-{u}"] = {
            "title": _title(html),
            "passage": _passage(html),
            "local_palette": palette,
            "roots_used": roots,
            "palette_unused": sorted(set(palette) - set(roots)),
        }

        with open(os.path.join(OUT_UNITS, f"unit-{u}.html"), "w", encoding="utf-8") as f:
            f.write(f'<article class="unit" data-unit="{int(u)}">\n{body}\n</article>\n')
        print(f"unit-{u}.html  roots={len(roots)} palette={len(palette)}"
              + (f"  MISSING={missing}" if missing else "")
              + ("  SCRIPT-LEFT!" if script_left else ""))

    json.dump(seed, open(os.path.join(OUT_PIPE, "units.seed.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    with open(os.path.join(OUT_PIPE, "extract-report.md"), "w", encoding="utf-8") as f:
        f.write("# Phase 1 extraction report\n\nSpot-check every HEBREW and synth line.\n")
        f.write("\n".join(report))
    print("\nwrote units.seed.json + extract-report.md")


if __name__ == "__main__":
    main()
