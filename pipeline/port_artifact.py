"""Drop one research artifact into the site.

    python pipeline/port_artifact.py 9           # port source-artifacts/matthew_09_translation.html
    python pipeline/port_artifact.py 9 --dry     # show what would change, write nothing
    python pipeline/port_artifact.py --backfill  # units 1-8: inject a meta block, nothing else

Pipeline for a new unit N:
  1. read  source-artifacts/matthew_0N_translation.html
  2. if it is a full standalone doc, reduce it to the <article> fragment
     (reuses extract_units.py: script strip, root-span rewrite, endnote prefix)
  3. read the unit-meta block, validate it against data/threads.json
  4. merge the unit into data/units.json  (built:true; assign a local hue to
     every declared root that is NOT a tracked thread, avoiding collisions)
  5. write the threads.json DELTA to pipeline/out/thread-delta-0N.md for Lane —
     opens/payoffs that need a `tagged`/`status` flip, and every candidate.
     threads.json is never written here; it is policy Lane owns.
  6. re-inject a normalised meta block, write units/unit-0N.html
  7. apply_retrofit (if retrofit-tags.json has entries for the unit),
     then scan_occurrences + verify_occurrences

Nothing is committed. Review the fragment in the browser, apply the thread
delta by hand if you accept it, then commit.
"""

import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import extract_units as ex          # noqa: E402
import unit_meta as um              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source-artifacts")
UNITS = os.path.join(ROOT, "units")
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "pipeline", "out")

# non-binding well of legible, parchment-friendly hues (style reference §1)
WELL = [
    "#a8324a", "#1c7d70", "#c0641a", "#4a4f93", "#2f6db3", "#8a3c70", "#8a6a2a",
    "#6b2fb3", "#3f7d3a", "#455a6b", "#9c4f1c", "#9c2f8f", "#1f8f5f", "#0e8aa0",
    "#8a7a4a", "#7a2230", "#c0285f", "#b07a1e", "#3a4f8a", "#5e1822", "#147a63",
]


# --------------------------------------------------------------- colour distance

def _lab(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883
    def f(t): return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def _de(a, b):
    return sum((x - y) ** 2 for x, y in zip(_lab(a), _lab(b))) ** 0.5


def assign_hues(local_roots, taken):
    """local_roots: [names]; taken: [hex already used in this unit]. Return {name:hex}."""
    out, used = {}, list(taken)
    for name in local_roots:
        pick = None
        for cand in WELL:
            if all(_de(cand, u) >= 12 for u in used):
                pick = cand
                break
        if pick is None:                       # well exhausted vs. this unit
            pick = WELL[len(used) % len(WELL)]
        out[name] = pick
        used.append(pick)
    return out


# --------------------------------------------------------------- fragment build

def to_fragment(html, n, meta_roots):
    """A standalone artifact -> the <article> fragment. Idempotent: a string that
    is already a fragment passes through the same defensive cleaners."""
    u = f"{n:02d}"
    already = '<article class="unit"' in html
    palette = ex.local_palette(html)                 # {} for new-contract artifacts
    body = html if already else ex.get_body(html)

    body = ex.normalize_verses(body, u)
    body = ex.normalize_blocks(body, u)
    body = ex.fix_greek_title(body, u)
    body = ex.strip_gk_spans(body, u)
    body = ex.clean_redundancy(body)
    body = ex.strip_leftover_script(body, u)
    body = ex.clean_redundancy(body)
    body = ex.rewrite_roots(body, palette or {r: "" for r in meta_roots}, u)
    body = ex.prefix_endnotes(body, u)

    if already:
        body = um.strip(body)
        m = re.search(r'<article class="unit"[^>]*>\n?', body)
        inner = body[m.end():]
        inner = re.sub(r'\s*</article>\s*$', "", inner)
        return f'<article class="unit" data-unit="{n}">\n{inner.strip()}\n</article>\n'
    return f'<article class="unit" data-unit="{n}">\n{body.strip()}\n</article>\n'


# --------------------------------------------------------------- units.json merge

def merge_units_json(meta, dry):
    uj = um._load("units.json")
    n = meta["unit"]
    row = um._unit_row(uj, n)
    if row is None:
        row = {"n": n, "slug": meta.get("slug", f"unit-{n:02d}"),
               "passage": meta["passage"], "title": meta["title"],
               "movement": meta.get("movement"), "built": False}
        uj["units"].append(row)
        uj["units"].sort(key=lambda u: u["n"])

    threads = {t["root"]: t for t in um._load("threads.json")["threads"]}
    existing = row.get("roots") or {}
    local = [r["root"] for r in meta["roots"] if r["root"] not in threads]
    # seed "taken" with existing local hues AND the global colour of every
    # tracked thread this unit uses — a new local hue must clear both
    taken = [e["color"] for e in existing.values()
             if isinstance(e, dict) and e.get("color")]
    taken += [threads[r["root"]]["color"] for r in meta["roots"]
              if r["root"] in threads]
    hues = assign_hues([r for r in local if r not in existing], taken)

    roots = {}
    for r in meta["roots"]:
        name = r["root"]
        if name in threads:
            continue                                   # colour comes from threads.json
        prev = existing.get(name) if isinstance(existing.get(name), dict) else {}
        entry = {
            "color": prev.get("color") or hues.get(name) or WELL[0],
            "translit": r["translit"],
            "gloss": r["gloss"],
            "kind": r.get("kind", "root"),
        }
        if r.get("members"):
            entry["members"] = r["members"]
        roots[name] = entry

    row.update({"slug": meta.get("slug", row["slug"]), "passage": meta["passage"],
                "title": meta["title"], "built": True, "roots": roots})
    if meta.get("movement"):
        row["movement"] = meta["movement"]

    if not dry:
        json.dump(uj, open(os.path.join(DATA, "units.json"), "w", encoding="utf-8"),
                  indent=2, ensure_ascii=False)
        open(os.path.join(DATA, "units.json"), "a").write("\n")
    return roots


# --------------------------------------------------------------- thread delta

def thread_delta(meta):
    threads = {t["id"]: t for t in um._load("threads.json")["threads"]}
    n = meta["unit"]
    lines = [f"# Thread delta — Unit {n}", "",
             "Apply by hand to `data/threads.json` if you accept it. "
             "The porter does not touch threads.json.", ""]

    th = meta.get("threads", {})
    touched = []
    for kind in ("opens", "payoffs"):
        for e in th.get(kind, []) or []:
            t = threads.get(e["id"])
            if not t:
                continue
            touched.append(e["id"])
            flags = []
            if not t.get("tagged"):
                flags.append("set `tagged: true`")
            if kind == "payoffs" and t.get("status") == "open":
                flags.append("consider `status: \"closed\"` if this is the final payoff")
            note = f" — {'; '.join(flags)}" if flags else " — already consistent"
            lines.append(f"- **{kind[:-1]}** `{e['id']}` at {e.get('ref', '?')}{note}")
            if kind == "payoffs" and not any(
                    p.get("unit") == n for p in t.get("payoffs", [])):
                lines.append(f"    - add `{{ \"unit\": {n}, \"ref\": \"{e.get('ref','')}\" }}` "
                             f"to `{e['id']}`.payoffs")

    cands = th.get("candidates", []) or []
    if cands:
        lines += ["", "## New-thread candidates (Lane decides)", ""]
        for c in cands:
            lines.append(f"- `{c.get('root', '?')}` — {c.get('why', '').strip()}")
            lines.append(f"    - if promoted: add a threads.json entry with "
                         f"`\"root\": \"{c.get('root','?')}\"`, then re-tag this "
                         f"fragment's spans and re-run the pipeline")
    if not touched and not cands:
        lines.append("_no tracked threads opened or paid off in this unit, no candidates._")

    path = os.path.join(OUT, f"thread-delta-{n:02d}.md")
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return path


# --------------------------------------------------------------- retrofit + scan

def run_retrofit_and_scan():
    import subprocess
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for step in ("apply_retrofit.py", "scan_occurrences.py", "verify_occurrences.py"):
        print(f"\n=== {step} ===")
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), step)],
                           env=env)
        if r.returncode != 0 and step != "apply_retrofit.py":
            print(f"FAILED at {step}")
            return False
    return True


# --------------------------------------------------------------- commands

def port_one(n, dry):
    os.makedirs(OUT, exist_ok=True)
    matches = glob.glob(os.path.join(SRC, f"matthew_{n:02d}_*.html"))
    if not matches:
        sys.exit(f"no source artifact: source-artifacts/matthew_{n:02d}_*.html")
    raw = open(matches[0], encoding="utf-8").read()

    meta = um.parse(raw)
    if meta is None:
        sys.exit("artifact has no <script id=\"unit-meta\"> block — see "
                 "matthew_study_style_reference.md §2")
    meta.setdefault("unit", n)
    meta.setdefault("slug", f"unit-{n:02d}")
    errs = um.validate(meta, um._load("threads.json"))
    if errs:
        print("METADATA INVALID:")
        for e in errs:
            print("  -", e)
        sys.exit(1)

    meta_roots = [r["root"] for r in meta["roots"]]
    fragment = to_fragment(raw, n, meta_roots)

    roots = merge_units_json(meta, dry)
    if not meta.get("movement"):
        r = um._unit_row(um._load("units.json"), n)
        if r and r.get("movement"):
            meta["movement"] = r["movement"]
    fragment = um.inject(fragment, um.generate(n) if not dry else meta)

    delta = thread_delta(meta)
    dest = os.path.join(UNITS, f"unit-{n:02d}.html")
    if dry:
        print(f"[dry] would write {dest}")
        print(f"[dry] local hues: { {k: v['color'] for k, v in roots.items()} }")
        print(f"[dry] thread delta -> {delta}")
        return
    open(dest, "w", encoding="utf-8").write(fragment)
    print(f"wrote {dest}")
    print(f"local hues: { {k: v['color'] for k, v in roots.items()} }")
    print(f"\n>>> REVIEW THE THREAD DELTA: {delta}")
    run_retrofit_and_scan()
    print("\nported. view in the browser, apply the thread delta if you accept it, then commit.")


def backfill(dry):
    """Units 1-8 already match the fragment shape — just add/refresh meta."""
    report = ["# Re-normalize report — units 1-8", "",
              "Each existing fragment is already a pure `<article>` fragment. The "
              "only change is prepending a generated `<script id=\"unit-meta\">` "
              "block (derived from units.json / threads.json). Prose, tags, ids: "
              "untouched.", ""]
    for path in sorted(glob.glob(os.path.join(UNITS, "unit-0[1-8].html"))):
        n = int(re.search(r"unit-(\d+)", path).group(1))
        html = open(path, encoding="utf-8").read()
        had = um.parse(html)
        meta = um.generate(n)
        new = um.inject(html, meta)
        changed = new != html
        report.append(f"## Unit {n}")
        report.append(f"- meta block: {'refreshed' if had else 'added'}"
                      f"{' (no change)' if not changed else ''}")
        report.append(f"- roots declared: {', '.join(r['root'] for r in meta['roots'])}")
        t = meta["threads"]
        report.append(f"- threads opens: {[e['id'] for e in t['opens']] or '—'}  "
                      f"payoffs: {[e['id'] for e in t['payoffs']] or '—'}")
        body_delta = um.strip(new) != html and um.strip(new).strip() != html.strip()
        report.append(f"- body bytes outside the meta block changed: "
                      f"**{'YES — inspect' if body_delta else 'no'}**")
        report.append("")
        if not dry:
            open(path, "w", encoding="utf-8").write(new)

    rp = os.path.join(OUT, "renormalize-report.md")
    os.makedirs(OUT, exist_ok=True)
    open(rp, "w", encoding="utf-8").write("\n".join(report) + "\n")
    print(f"{'[dry] ' if dry else ''}wrote {rp}")
    if not dry:
        run_retrofit_and_scan()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("unit", nargs="?", type=int)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--backfill", action="store_true")
    a = ap.parse_args()
    if a.backfill:
        backfill(a.dry)
    elif a.unit:
        port_one(a.unit, a.dry)
    else:
        ap.error("give a unit number or --backfill")


if __name__ == "__main__":
    main()
