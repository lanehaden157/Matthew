"""Apply pipeline/retrofit-tags.json to units/*.html.

Runs AFTER extract_units.py (which regenerates fragments from source and would
otherwise wipe these). Idempotent: skips a tag already present.

  add:   wrap the first untagged occurrence of `text` inside the .v block for
         `verse` with <span class="r" data-root="ROOT">text</span>
  retag: change data-root="from" -> "to" on the span wrapping `text` in that verse
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = os.path.join(ROOT, "units")
SPEC = os.path.join(ROOT, "pipeline", "retrofit-tags.json")


def vblock(html, verse):
    """(start, end) of the .v paragraph containing <span class="n">verse</span>."""
    m = re.search(r'<(?:div|p) class="v">(?:(?!</(?:div|p)>).)*?<span class="n">'
                  + str(verse) + r'</span>.*?</(?:div|p)>', html, re.S)
    return (m.start(), m.end()) if m else None


def apply_add(html, item):
    span = vblock(html, item["verse"])
    if not span:
        return html, f"SKIP {item['unit']} v{item['verse']}: no .v block"
    a, b = span
    seg = html[a:b]
    tag = f'<span class="r" data-root="{item["root"]}">{item["text"]}</span>'
    if tag in seg or f'data-root="{item["root"]}"' in seg:
        return html, f"ok   {item['unit']} v{item['verse']} {item['root']}: already tagged"
    # wrap first occurrence of text that is not inside an existing tag
    # (depth tracking handles tag-avoidance; boundary is alnum/hyphen only)
    pat = re.compile(r'(?<![\w-])' + re.escape(item["text"]) + r'(?![\w-])')
    depth_ok = _first_outside_tags(seg, pat)
    if depth_ok is None:
        return html, f"MISS {item['unit']} v{item['verse']}: '{item['text']}' not found free in verse"
    i, j = depth_ok
    seg = seg[:i] + tag + seg[j:]
    return html[:a] + seg + html[b:], f"ADD  {item['unit']} v{item['verse']} {item['root']}: wrapped '{item['text']}'"


def apply_retag(html, item):
    span = vblock(html, item["verse"])
    if not span:
        return html, f"SKIP {item['unit']} v{item['verse']}: no .v block"
    a, b = span
    seg = html[a:b]
    old = f'data-root="{item["from"]}">{item["text"]}'
    new = f'data-root="{item["to"]}">{item["text"]}'
    if new in seg:
        return html, f"ok   {item['unit']} v{item['verse']}: already retagged"
    if old not in seg:
        return html, f"MISS {item['unit']} v{item['verse']}: '{old}' not present"
    seg = seg.replace(old, new, 1)
    return html[:a] + seg + html[b:], f"RTAG {item['unit']} v{item['verse']}: {item['from']} -> {item['to']} on '{item['text']}'"


def _first_outside_tags(seg, pat):
    depth = 0
    for k, ch in enumerate(seg):
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth = max(0, depth - 1)
        elif depth == 0:
            m = pat.match(seg, k)
            if m:
                return m.start(), m.end()
    return None


def apply_unwrap(html, item):
    """Strip the <span class="r"[...]data-root="root"[...]>TEXT</span> wrapper
    around every occurrence of TEXT, leaving TEXT."""
    pat = re.compile(
        r'<span class="r"[^>]*\bdata-root="' + re.escape(item["root"]) + r'"[^>]*>'
        + re.escape(item["text"]) + r'</span>')
    new, n = pat.subn(item["text"], html)
    if not n:
        return html, f"ok   {item['unit']} unwrap '{item['text']}': nothing to do"
    return new, f"UNWR {item['unit']}: unwrapped {n}x '{item['text']}' (was {item['root']})"


def main():
    spec = json.load(open(SPEC, encoding="utf-8"))
    by_unit = {}
    for it in spec.get("unwrap", []):
        by_unit.setdefault(it["unit"], []).append(("unwrap", it))
    for it in spec.get("add", []):
        by_unit.setdefault(it["unit"], []).append(("add", it))
    for it in spec.get("retag", []):
        by_unit.setdefault(it["unit"], []).append(("retag", it))

    logs = []
    for unit, items in sorted(by_unit.items()):
        path = os.path.join(UNITS, unit + ".html")
        html = open(path, encoding="utf-8").read()
        fn = {"add": apply_add, "retag": apply_retag, "unwrap": apply_unwrap}
        for kind, it in items:
            html, msg = fn[kind](html, it)
            logs.append(msg)
        open(path, "w", encoding="utf-8").write(html)

    for m in logs:
        print(m)
    if any(m.startswith(("MISS", "SKIP")) for m in logs):
        sys.exit(1)


if __name__ == "__main__":
    main()
