"""Apply pipeline/retrofit-tags.json to units/*.html.

Idempotent — every op no-ops if already applied, so build.py re-runs it each
time. The committed fragments already have all of this; the file is the record
of what was done, and the safety net if port_artifact.py re-derives a fragment
(it imports extract_units cleaners, which don't know about these edits).

  strip_span   whole unit: unwrap every <span class="CLS">…</span>, keeping the
               inner text (for design devices cut from the fragments but still
               present in source-artifacts/ — e.g. the .star motif in 2/3/7)
  add          wrap the first untagged occurrence of `text` in verse `verse`
               (optional "cls": "rl" for a root-linked, uncounted span, default
                "r"; optional "nth": 2 to pick the 2nd .v block with that number
                in a cross-chapter unit, e.g. 4:6 vs 3:6 in unit-03)
  retag        change data-root on the span wrapping `text` in `verse`
  unwrap       strip the data-root span around every `text` (whole unit)
  retag_word   whole unit: any `<span … data-root="from" …>TEXT</span> whose
               TEXT matches the `match` regex -> data-root="to"
  untag_word   whole unit: unwrap data-root="root" spans whose TEXT matches
               `match` (or, with `nomatch`, whose TEXT does NOT match)
  text         plain find/replace in the unit's visible text (wording fixes)
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = os.path.join(ROOT, "units")
SPEC = os.path.join(ROOT, "pipeline", "retrofit-tags.json")
# generated: retro fixes for earlier units, merged in by port_artifact.py.
# kept separate so retrofit-tags.json stays hand-authored and hand-formatted.
RETRO_SPEC = os.path.join(ROOT, "pipeline", "retro-tags.json")

SPAN = r'<span class="r[l]?"[^>]*\bdata-root="%s"[^>]*>([^<]*)</span>'


def vblock(html, verse, nth=1):
    """(start, end) of the nth .v block whose number is `verse`. `nth` (default
    1) disambiguates cross-chapter units where a bare verse number repeats
    (unit-03 has 3:6 and 4:6, both `<span class="n">6</span>`)."""
    pat = re.compile(r'<(?:div|p) class="v">(?:(?!</(?:div|p)>).)*?<span class="n">'
                     + re.escape(str(verse)) + r'</span>.*?</(?:div|p)>', re.S)
    hits = list(pat.finditer(html))
    if len(hits) < nth:
        return None
    m = hits[nth - 1]
    return (m.start(), m.end())


def apply_add(html, it):
    nth = it.get("nth", 1)
    span = vblock(html, it["verse"], nth)
    if not span:
        return html, f"SKIP {it['unit']} v{it['verse']}: no .v block"
    a, b = span
    seg = html[a:b]
    cls = it.get("cls", "r")
    tag = f'<span class="{cls}" data-root="{it["root"]}">{it["text"]}</span>'
    already = re.search(r'<span class="r[l]?" data-root="%s">%s</span>'
                        % (re.escape(it["root"]), re.escape(it["text"])), seg)
    if already:
        return html, f"ok   {it['unit']} v{it['verse']} {it['root']}: already tagged"
    pat = re.compile(r'(?<![\w-])' + re.escape(it["text"]) + r'(?![\w-])')
    hit = _first_outside_tags(seg, pat)
    if hit is None:
        return html, f"MISS {it['unit']} v{it['verse']}: '{it['text']}' not free in verse"
    i, j = hit
    seg = seg[:i] + tag + seg[j:]
    return html[:a] + seg + html[b:], f"ADD  {it['unit']} v{it['verse']} {it['root']}: '{it['text']}'"


def apply_retag(html, it):
    span = vblock(html, it["verse"], it.get("nth", 1))
    if not span:
        return html, f"SKIP {it['unit']} v{it['verse']}: no .v block"
    a, b = span
    seg = html[a:b]
    old = f'data-root="{it["from"]}">{it["text"]}'
    new = f'data-root="{it["to"]}">{it["text"]}'
    if new in seg:
        return html, f"ok   {it['unit']} v{it['verse']}: already retagged"
    if old not in seg:
        return html, f"MISS {it['unit']} v{it['verse']}: '{old}' not present"
    return html[:a] + seg.replace(old, new, 1) + html[b:], \
        f"RTAG {it['unit']} v{it['verse']}: {it['from']}->{it['to']} '{it['text']}'"


def apply_unwrap(html, it):
    pat = re.compile(
        r'<span class="r[l]?"[^>]*\bdata-root="' + re.escape(it["root"]) + r'"[^>]*>'
        + re.escape(it["text"]) + r'</span>')
    new, n = pat.subn(it["text"], html)
    return new, (f"UNWR {it['unit']}: {n}x '{it['text']}' (was {it['root']})"
                 if n else f"ok   {it['unit']} unwrap '{it['text']}': nothing")


def apply_retag_word(html, it):
    m_re = re.compile(it["match"], re.I)
    n = [0]

    def repl(mm):
        if m_re.search(mm.group(1)):
            n[0] += 1
            return mm.group(0).replace(f'data-root="{it["from"]}"',
                                       f'data-root="{it["to"]}"', 1)
        return mm.group(0)

    new = re.sub(SPAN % re.escape(it["from"]), repl, html)
    return new, (f"RTAGW {it['unit']}: {n[0]}x {it['from']}->{it['to']} /{it['match']}/"
                 if n[0] else f"ok    {it['unit']} retag_word {it['from']}: no hit")


def apply_untag_word(html, it):
    pos = it.get("match")
    neg = it.get("nomatch")
    pr = re.compile(pos, re.I) if pos else None
    nr = re.compile(neg, re.I) if neg else None
    n = [0]

    def repl(mm):
        txt = mm.group(1)
        drop = (pr and pr.search(txt)) or (nr and not nr.search(txt))
        if drop:
            n[0] += 1
            return txt
        return mm.group(0)

    new = re.sub(SPAN % re.escape(it["root"]), repl, html)
    return new, (f"UNTGW {it['unit']}: {n[0]}x untag {it['root']}"
                 if n[0] else f"ok    {it['unit']} untag_word {it['root']}: no hit")


def apply_text(html, it):
    if it["to"] in html and it["from"] not in html:
        return html, f"ok   {it['unit']} text '{it['from']}': already applied"
    new, n = re.subn(re.escape(it["from"]), it["to"].replace("\\", "\\\\"), html)
    return new, (f"TEXT {it['unit']}: {n}x '{it['from']}' -> '{it['to']}'"
                 if n else f"MISS {it['unit']} text: '{it['from']}' not found")


def apply_strip_span(html, it):
    """Unwrap every <span class="CLS">…</span> in the unit, keeping inner text.
    For decorative wrappers removed from the design but still in source-artifacts
    (e.g. the cut `.star` motif in units 2/3/7) — so re-running extract_units
    doesn't silently resurrect them."""
    cls = re.escape(it["class"])
    pat = re.compile(r'<span class="' + cls + r'">(.*?)</span>', re.S)
    new, n = pat.subn(r"\1", html)
    return new, (f"STRIP {it['unit']}: {n}x span.{it['class']}"
                 if n else f"ok   {it['unit']} strip span.{it['class']}: none")


def _first_outside_tags(seg, pat):
    depth = 0
    for k, ch in enumerate(seg):
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth = max(0, depth - 1)
        elif depth == 0 and pat.match(seg, k):
            m = pat.match(seg, k)
            return m.start(), m.end()
    return None


FNS = {"add": apply_add, "retag": apply_retag, "unwrap": apply_unwrap,
       "retag_word": apply_retag_word, "untag_word": apply_untag_word,
       "text": apply_text, "strip_span": apply_strip_span}
ORDER = ["strip_span", "text", "untag_word", "retag_word", "unwrap", "retag", "add"]


def load_specs():
    spec = json.load(open(SPEC, encoding="utf-8"))
    if os.path.exists(RETRO_SPEC):
        retro = json.load(open(RETRO_SPEC, encoding="utf-8"))
        for op, items in retro.items():
            if isinstance(items, list):
                spec.setdefault(op, []).extend(items)
    return spec


def main():
    spec = load_specs()
    by_unit = {}
    for op in ORDER:
        for it in spec.get(op, []):
            if "unit" not in it:  # skip inline "_c" comment entries
                continue
            by_unit.setdefault(it["unit"], []).append((op, it))

    logs = []
    for unit, items in sorted(by_unit.items()):
        path = os.path.join(UNITS, unit + ".html")
        html = open(path, encoding="utf-8").read()
        for op, it in items:
            html, msg = FNS[op](html, it)
            logs.append(msg)
        open(path, "w", encoding="utf-8").write(html)

    for m in logs:
        print(m)
    if any(m.startswith(("MISS", "SKIP")) for m in logs):
        sys.exit(1)


if __name__ == "__main__":
    main()
