"""One-shot: pull translit + gloss for every tracked root out of each fragment's
existing hand-written legend, and rewrite data/units.json so each unit's `roots`
map is  name -> { color, translit, gloss }  instead of  name -> hex.

Matching strategy, in order:
  1. legend row carries data-root=  (Unit 8)          -> exact
  2. swatch var  --c-<name>  matches a units.json root -> exact
  3. gloss text startswith / contains the root name    -> heuristic (logged)
Anything unmatched is written with translit/gloss = null and listed loudly;
fix those by hand in pipeline/legend-overrides.json and re-run.
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS_DIR = os.path.join(ROOT, "units")
UNITS_JSON = os.path.join(ROOT, "data", "units.json")
OVERRIDES = os.path.join(ROOT, "pipeline", "legend-overrides.json")

report = []


def parse_legend(html):
    m = re.search(r'<section[^>]*class="[^"]*legend[^"]*"[^>]*>(.*?)</section>', html, re.S)
    if not m:
        return []
    rows = []
    for li in re.findall(r"<li>(.*?)</li>", m.group(1), re.S):
        data_root = re.search(r'data-root="([a-z0-9-]+)"', li)
        var = re.search(r"--c-([a-z0-9-]+)", li)
        translit = (re.search(r'<span class="translit">([^<]*)</span>', li)
                    or re.search(r'<span class="r" data-root="[a-z0-9-]+">([^<]*)</span>', li))
        # gloss = text after the first em dash, minus any <span class="tag"> / <span class="tr">
        after = li.split("—", 1)[1] if "—" in li else ""
        after = re.sub(r'<span class="tag">.*?</span>', "", after, flags=re.S)
        after = re.sub(r'<span class="tr">.*?</span>', "", after, flags=re.S)
        gloss = re.sub(r"<[^>]+>", "", after).strip().strip('"').strip()
        rows.append({
            "data_root": data_root.group(1) if data_root else None,
            "var": var.group(1) if var else None,
            "translit": translit.group(1).strip() if translit else None,
            "gloss": gloss or None,
        })
    return rows


def main():
    d = json.load(open(UNITS_JSON, encoding="utf-8"))
    overrides = json.load(open(OVERRIDES, encoding="utf-8")) if os.path.exists(OVERRIDES) else {}
    seen = {}  # root name -> first {translit, gloss} found in an earlier unit

    for u in d["units"]:
        if not u.get("built"):
            continue
        html = open(os.path.join(UNITS_DIR, f"{u['slug']}.html"), encoding="utf-8").read()
        rows = parse_legend(html)
        ov = overrides.get(u["slug"], {})
        new_roots = {}
        for name, cur in u["roots"].items():
            color = cur["color"] if isinstance(cur, dict) else cur
            meta = {"color": color,
                    "translit": cur.get("translit") if isinstance(cur, dict) else None,
                    "gloss": cur.get("gloss") if isinstance(cur, dict) else None}
            # 1/2: exact match by data-root or var
            row = next((r for r in rows if r["data_root"] == name or r["var"] == name), None)
            # 3: heuristic by gloss text
            if not row:
                row = next((r for r in rows if r["gloss"] and
                            (r["gloss"].lower().startswith(name) or
                             f" {name}" in r["gloss"].lower() or
                             r["gloss"].lower().split(" /")[0].strip() == name)), None)
                if row:
                    report.append(f"- {u['slug']} '{name}': heuristic gloss match -> {row['translit']!r} / {row['gloss']!r}")
            if row:
                meta["translit"] = row["translit"]
                meta["gloss"] = row["gloss"]
            # inherit from an earlier unit that glossed the same root
            if (not meta["translit"] or not meta["gloss"]) and name in seen:
                meta["translit"] = meta["translit"] or seen[name]["translit"]
                meta["gloss"] = meta["gloss"] or seen[name]["gloss"]
                report.append(f"- {u['slug']} '{name}': inherited from earlier unit")
            if name in ov:
                meta.update(ov[name])
            if not meta["translit"] or not meta["gloss"]:
                report.append(f"- {u['slug']} '{name}': UNRESOLVED (translit={meta['translit']!r} gloss={meta['gloss']!r}) — add to legend-overrides.json")
            elif name not in seen:
                seen[name] = {"translit": meta["translit"], "gloss": meta["gloss"]}
            new_roots[name] = meta
        u["roots"] = new_roots

    json.dump(d, open(UNITS_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    open(UNITS_JSON, "a", encoding="utf-8").write("\n")
    outp = os.path.join(ROOT, "pipeline", "out", "legend-report.md")
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    open(outp, "w", encoding="utf-8").write("# Legend extraction\n\n" + "\n".join(report) + "\n")
    print(f"rewrote units.json roots as objects. {len(report)} notes -> pipeline/out/legend-report.md")


if __name__ == "__main__":
    main()
