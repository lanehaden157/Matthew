"""Drop one research artifact into the site.

    python pipeline/port_artifact.py 9              # port source-artifacts/matthew_09_translation.html
    python pipeline/port_artifact.py 9 --dry        # show what would change, write nothing
    python pipeline/port_artifact.py 11 --src X.html  # build the thread-delta report from X, write nothing
    python pipeline/port_artifact.py --backfill     # units 1-8: inject a meta block, nothing else

Pipeline for a new unit N:
  1. read  source-artifacts/matthew_0N_translation.html
  2. if it is a full standalone doc, reduce it to the <article> fragment
     (reuses extract_units.py: script strip, root-span rewrite, endnote prefix)
  3. read the unit-meta block, validate it against data/threads.json
  4. merge the unit into data/units.json  (built:true; assign a local hue to
     every declared root that is NOT a tracked thread, avoiding collisions)
  5. merge threads.retro (fixes for EARLIER units) into retro-tags.json,
     dry-checking each against its target fragment first
  6. write the thread-delta report to pipeline/out/thread-delta-0N.md for Lane:
     - opens/payoffs that need a `tagged`/`status` flip, with a ready
       payoffs entry (incl. any `note` from the meta block)
     - new-thread candidates, each with a stem preview and a ready
       thread-stems.json entry
     - fragment-structure warnings (pericope headings, aside.synoptic)
     - the retro fixes that were merged
     - tracked-thread COVERAGE: every occurrence the Greek has in this
       passage that the fragment left untagged, as ready retrofit-tags lines
     threads.json is never written here; it is policy Lane owns.
  7. re-inject a normalised meta block, write units/unit-0N.html
  8. apply_retrofit (retrofit-tags.json + retro-tags.json), then
     scan_occurrences + verify_occurrences

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
        roots[name] = {
            "color": prev.get("color") or hues.get(name) or WELL[0],
            "translit": r["translit"],
            "gloss": r["gloss"],
        }

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

def thread_delta(meta, fragment_html=None, retrofit_applied=True):
    threads = {t["id"]: t for t in um._load("threads.json")["threads"]}
    n = meta["unit"]
    slug = meta.get("slug", f"unit-{n:02d}")
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
                entry = {"unit": n, "ref": e.get("ref", "")}
                if e.get("note"):
                    entry["note"] = e["note"]
                lines.append(f"    - add to `{e['id']}`.payoffs: "
                             f"`{json.dumps(entry, ensure_ascii=False)}`")
            elif kind == "opens" and e.get("note"):
                lines.append(f"    - popover note for the opens: “{e['note']}”")

    cands = th.get("candidates", []) or []
    if cands:
        lines += ["", "## New-thread candidates (Lane decides)", ""]
        for c in cands:
            root = c.get("root", "?")
            lines.append(f"- `{root}` — {c.get('why', '').strip()}")
            if c.get("stems"):
                _append_stem_preview(lines, root, c)
            else:
                lines.append(f"    - no stems proposed; if promoted, add a "
                             f"`thread-stems.json` entry and run "
                             f"`audit_thread_coverage.py --forms {root}`")

    retro = th.get("retro", []) or []
    if retro:
        lines += ["", "## Retro fixes for earlier units", "",
                  "The porter dry-checks each against its target fragment, then "
                  "merges the ones that apply into `pipeline/retro-tags.json` "
                  "(a real port only — not `--dry`/`--src`):", ""]
        for e in retro:
            op = e.get("op", "add")
            lines.append(f"- `{e.get('unit','?')}` {op} `{e.get('root', e.get('to','?'))}` "
                         f"— {e.get('why','').strip()}")
            body = {k: v for k, v in e.items() if k not in ("op", "why")}
            lines.append(f"    `{json.dumps(body, ensure_ascii=False)}`")

    if fragment_html is not None:
        _append_structure(lines, fragment_html)
        _append_coverage(lines, slug, fragment_html, meta.get("passage", ""),
                         retrofit_applied)

    if not touched and not cands and not retro:
        lines.append("_no tracked threads opened or paid off in this unit, "
                     "no candidates, no retro fixes._")

    path = os.path.join(OUT, f"thread-delta-{n:02d}.md")
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return path


def _append_structure(lines, html):
    """Fragment-shape checks the style reference asks for (matthew_study_style
    _reference.md §3-4). Warnings only — the port still writes the fragment."""
    issues = []

    pericopes = re.findall(r'<h3 class="pericope">(.*?)</h3>', html, re.S)
    if not pericopes:
        issues.append("no `<h3 class=\"pericope\">` headings — the translation "
                      "should be divided into passage groups (style ref §3)")
    for h in pericopes:
        if not re.search(r'(?:·|&middot;)\s*\d+:\d+', h):
            issues.append(f"pericope heading without a `· C:V` range: "
                          f"“{re.sub(r'<[^>]+>', '', h).strip()[:50]}”")

    for m in re.finditer(r'<h[1-4][^>]*class="(movement|panel|panelhead|sectionhead)"',
                         html):
        issues.append(f"heading uses the old `{m.group(1)}` class — new artifacts "
                      "use `<h3 class=\"pericope\">` only (style ref §3)")

    for m in re.finditer(r'<aside class="synoptic"([^>]*)>(.*?)</aside>', html, re.S):
        attrs, inner = m.group(1), m.group(2)
        if "data-anchor" not in attrs:
            issues.append("`<aside class=\"synoptic\">` missing `data-anchor=\"C:V\"`")
        if re.search(r'data-root=|class="rl?"', inner):
            issues.append("`<aside class=\"synoptic\">` contains a tagged span — "
                          "synoptic parallels are translit only, no `data-root` "
                          "(style ref §4)")
        # the aside must be a sibling of the verse, never spliced inside an
        # unclosed .gloss span or a .compare box — otherwise spotlight.js rolls
        # it into a plain note (`*`) instead of giving it its own `✧` chip.
        before = html[:m.start()]
        open_gloss = before.rfind('<span class="gloss">')
        if open_gloss != -1 and '</span>' not in before[open_gloss:]:
            issues.append("`<aside class=\"synoptic\">` is nested inside an "
                          "unclosed `<span class=\"gloss\">` — close the gloss "
                          "first so the aside is a sibling (style ref §3)")
        open_cmp = before.rfind('<div class="compare">')
        if open_cmp != -1 and '</div>' not in before[open_cmp:]:
            issues.append("`<aside class=\"synoptic\">` is nested inside a "
                          "`<div class=\"compare\">` — move it out below the "
                          "compare box (style ref §3)")

    if issues:
        lines += ["", "## Fragment structure — fix in the artifact", ""]
        lines += [f"- {i}" for i in issues]


def _append_stem_preview(lines, root, cand):
    try:
        import audit_thread_coverage as atc
        pv = atc.stem_preview(cand["stems"], cand.get("exclude"))
    except Exception as ex:                                   # pragma: no cover
        lines.append(f"    - (stem preview unavailable: {ex})")
        return
    entry = {"stems": cand["stems"]}
    if cand.get("exclude"):
        entry["exclude"] = cand["exclude"]
    lines.append(f"    - if promoted, `thread-stems.json` entry: "
                 f"`\"{root}\": {json.dumps(entry, ensure_ascii=False)}`")
    kept = pv["kept"]
    total = sum(e["n"] for e in kept)
    lines.append(f"    - those stems match **{total}** words book-wide "
                 f"({len(kept)} distinct forms):")
    for e in kept[:12]:
        lines.append(f"        {e['surface']} ({e['translit']}) ×{e['n']}  "
                     f"ch {','.join(map(str, e['chapters']))}")
    extra = len(kept) - 12
    if extra > 0:
        lines.append(f"        …and {extra} more form" + ("s" if extra != 1 else ""))
    if pv["dropped"]:
        drp = ", ".join(f"{e['surface']}×{e['n']}" for e in pv["dropped"])
        lines.append(f"    - `exclude` drops: {drp}")


def _append_coverage(lines, slug, html, passage, retrofit_applied=True):
    try:
        import audit_thread_coverage as atc
        cov = atc.coverage_for_fragment(slug, html, passage)
    except Exception as ex:                                   # pragma: no cover
        lines.append(f"\n## Tracked-thread coverage\n\n(unavailable: {ex})")
        return
    lines += ["", "## Tracked-thread coverage in this unit", ""]
    if not retrofit_applied:
        lines.append("_(checked on the raw fragment — retrofit-tags.json not yet "
                     "applied; entries already there will show as gaps)_")
        lines.append("")
    if cov["warnings"]:
        lines.append("**alignment warnings — check these first:**")
        lines += [f"- {w}" for w in cov["warnings"]] + [""]
    if not cov["gaps"] and not cov["overs"]:
        lines.append("Every tracked-thread occurrence in this passage is tagged. ✓")
        return
    if cov["gaps"]:
        lines.append(f"**{len(cov['gaps'])} occurrence(s) the Greek has but the "
                     f"fragment leaves untagged** — add to `retrofit-tags.json` "
                     f"`add` (fill in `text`):")
        lines.append("")
        for g in cov["gaps"]:
            txt = (g["text"][:90] + "…") if len(g["text"]) > 90 else g["text"]
            lines.append(f'    {{ "unit": "{slug}", "verse": {g["v"]}, '
                         f'"text": "???", "root": "{g["root"]}", '
                         f'"why": "{g["translit"]} {g["ch"]}:{g["v"]}" }},')
            if txt:
                lines.append(f"        # “{txt}”")
    if cov["overs"]:
        lines += ["", "**tagged but the Greek root isn't there — wrong verse?**"]
        for o in cov["overs"]:
            lines.append(f"- `{o['root']}` at {o['ch']}:{o['v']}")


# --------------------------------------------------------------- retrofit + scan

RETRO_FIELDS = {
    "add": ("unit", "verse", "text", "root", "why", "nth", "cls"),
    "retag": ("unit", "verse", "from", "to", "text", "why", "nth"),
    "retag_word": ("unit", "from", "to", "match", "why"),
    "untag_word": ("unit", "root", "match", "why"),
    "unwrap": ("unit", "text", "root", "why"),
    "strip_span": ("unit", "class", "why"),
    "text": ("unit", "from", "to", "why"),
}
RETRO_SPEC = os.path.join(ROOT, "pipeline", "retro-tags.json")


def merge_retro(meta, dry):
    """Merge meta.threads.retro (fixes for earlier units) into the generated
    pipeline/retro-tags.json, which apply_retrofit.py loads alongside the
    hand-authored retrofit-tags.json. Each entry is dry-checked against its
    target fragment first; ones that wouldn't apply cleanly are reported, not
    written. Returns (n_written, [skip messages])."""
    import apply_retrofit as ar
    retro = (meta.get("threads", {}) or {}).get("retro", []) or []
    if not retro:
        return 0, []
    rt = json.load(open(RETRO_SPEC, encoding="utf-8")) \
        if os.path.exists(RETRO_SPEC) else {}
    n = meta["unit"]
    stamp = f"from Unit {n} port ({_today()})"
    written, skips = 0, []
    for e in retro:
        op = e.get("op", "add")
        entry = {k: e[k] for k in RETRO_FIELDS.get(op, ()) if k in e}
        html = open(os.path.join(UNITS, e["unit"] + ".html"),
                    encoding="utf-8").read()
        _, msg = ar.FNS[op](html, entry)
        if msg.startswith(("MISS", "SKIP")):
            skips.append(f"{msg}  ({e.get('why','').strip()})")
            continue
        if msg.startswith("ok"):
            continue                              # already tagged — nothing to record
        arr = rt.setdefault(op, [])
        if any(x == entry for x in arr):
            continue
        entry["_from"] = stamp
        arr.append(entry)
        written += 1
    if (written or skips) and not dry:
        json.dump(rt, open(RETRO_SPEC, "w", encoding="utf-8"), indent=2,
                  ensure_ascii=False)
        open(RETRO_SPEC, "a", encoding="utf-8").write("\n")
    return written, skips


def _today():
    import datetime
    return datetime.date.today().isoformat()


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

def port_one(n, dry, src=None):
    os.makedirs(OUT, exist_ok=True)
    if src:
        if not os.path.exists(src):
            sys.exit(f"--src not found: {src}")
        raw = open(src, encoding="utf-8").read()
    else:
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

    no_write = dry or bool(src)
    roots = merge_units_json(meta, no_write)
    if not meta.get("movement"):
        r = um._unit_row(um._load("units.json"), n)
        if r and r.get("movement"):
            meta["movement"] = r["movement"]
    fragment = um.inject(fragment, um.generate(n) if not no_write else meta)

    dest = os.path.join(UNITS, f"unit-{n:02d}.html")
    if no_write:
        why = "dry run" if dry else "--src: writing nothing"
        delta = thread_delta(meta, fragment, retrofit_applied=False)
        print(f"[{why}] would write {dest}")
        print(f"[{why}] local hues: { {k: v['color'] for k, v in roots.items()} }")
        nretro = len((meta.get("threads", {}) or {}).get("retro", []) or [])
        if nretro:
            print(f"[{why}] {nretro} retro fix(es) for earlier units — would be "
                  f"merged into retrofit-tags.json (see the thread delta)")
        print(f"[{why}] thread delta -> {delta}  "
              f"(coverage checked before retrofit-tags.json is applied)")
        return
    open(dest, "w", encoding="utf-8").write(fragment)
    print(f"wrote {dest}")
    print(f"local hues: { {k: v['color'] for k, v in roots.items()} }")
    written, skips = merge_retro(meta, dry=False)
    if written:
        print(f"merged {written} retro fix(es) for earlier units -> "
              f"pipeline/retro-tags.json")
    for s in skips:
        print(f"  retro NOT merged — {s}")
    run_retrofit_and_scan()
    # coverage against the fragment as it now stands on disk (retrofit applied)
    final = open(dest, encoding="utf-8").read()
    delta = thread_delta(meta, final, retrofit_applied=True)
    print(f"\n>>> REVIEW THE THREAD DELTA: {delta}")
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
    ap.add_argument("--src", metavar="PATH",
                    help="port from this file instead of source-artifacts/; "
                         "writes nothing, just builds the thread-delta report "
                         "(for dry-running the porter on a practice fragment)")
    a = ap.parse_args()
    if a.backfill:
        backfill(a.dry)
    elif a.unit:
        port_one(a.unit, a.dry, a.src)
    else:
        ap.error("give a unit number or --backfill")


if __name__ == "__main__":
    main()
