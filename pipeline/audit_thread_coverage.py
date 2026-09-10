"""Audit tracked-thread tag coverage against the Greek.

For every thread in data/threads.json that has a stem entry in
pipeline/thread-stems.json, scan MatthewSBLGNT.txt for every morphological
occurrence of the root, and report the ones that fall inside a BUILT unit's
passage but carry no <span data-root> in the fragment. Also flags the reverse:
a verse tagged with the root where the Greek has no such root (likely wrong
verse / over-tag).

    python pipeline/audit_thread_coverage.py             # every defined thread
    python pipeline/audit_thread_coverage.py sin follow  # just these
    python pipeline/audit_thread_coverage.py --stub sin  # print retrofit-tags
                                                         # lines for the gaps
    python pipeline/audit_thread_coverage.py --forms mercy light
                        # every word form those stems match, counts + chapters +
                        # what `exclude` drops — sanity-check a stem set

Informational: exits 0 even with gaps (units 11-28 don't exist yet, so most
threads legitimately show gaps past unit 10).

Greek source: MatthewSBLGNT.txt at the repo root (tracked — see CLAUDE.md
'Source texts'). Tab-separated 'Matt C:V<TAB>text' lines. If it's missing the
script says so and exits 2.
"""

import glob
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from greek import transliterate as _translit
except Exception:  # pragma: no cover
    def _translit(s):
        return s

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = os.path.join(ROOT, "units")
DATA = os.path.join(ROOT, "data")
GREEK = os.path.join(ROOT, "MatthewSBLGNT.txt")

VBLOCK = re.compile(r'<(?:div|p)\s+class="v"[^>]*>(.*?)</(?:div|p)>', re.S)
NUM = re.compile(r'<span class="n">(\d+)</span>')
ROOTSPAN = re.compile(r'data-root="([a-z0-9-]+)"')
HEAD = re.compile(r'<h[1-4][^>]*>(.*?)</h[1-4]>', re.S)
HEAD_CV = re.compile(r'·\s*(\d+):\d+')
TAGS = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")
GREEKWORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def strip_accents(s):
    d = unicodedata.normalize("NFD", s)
    return "".join(c for c in d if not unicodedata.combining(c)).lower()


def detag(s):
    return WS.sub(" ", TAGS.sub("", s)).strip()


# ----------------------------------------------------------------- Greek side

def load_greek():
    if not os.path.exists(GREEK):
        sys.exit(f"[audit] {GREEK} not found — put the SBLGNT Matthew text there "
                 f"(tab-separated 'Matt C:V<TAB>text' lines). See CLAUDE.md.")
    verses = []
    for line in open(GREEK, encoding="utf-8"):
        m = re.match(r"Matt (\d+):(\d+)\t(.*)", line.rstrip("\n"))
        if m:
            verses.append((int(m.group(1)), int(m.group(2)), m.group(3)))
    if not verses:
        sys.exit(f"[audit] {GREEK} parsed to zero verses — wrong format?")
    return verses


def greek_hits(verses, spec):
    """{ (ch,v): [surface words] } for one thread's stem spec."""
    stems = [strip_accents(s) for s in spec["stems"]]
    exclude = {strip_accents(x) for x in spec.get("exclude", [])}
    out = {}
    for ch, v, txt in verses:
        hits = []
        for w in GREEKWORD.findall(txt):
            sw = strip_accents(w)
            if sw in exclude:
                continue
            if any(st in sw for st in stems):
                hits.append(w)
        if hits:
            out[(ch, v)] = hits
    return out


# ----------------------------------------------------------------- fragment side

def parse_range(passage):
    m = re.search(r"(\d+):(\d+)\s*[-–]\s*(?:(\d+):)?(\d+)", passage)
    if not m:
        m2 = re.search(r"(\d+):(\d+)", passage)
        c, v = int(m2.group(1)), int(m2.group(2))
        return (c, v), (c, v)
    c1, v1 = int(m.group(1)), int(m.group(2))
    c2 = int(m.group(3)) if m.group(3) else c1
    v2 = int(m.group(4))
    return (c1, v1), (c2, v2)


def tagged_map(html, start_ch, end_ch):
    """{ (ch,v): set(roots) } from the fragment's .v blocks, in document order.

    Chapter is tracked from section headings that carry '· C:V', with a
    fallback bump when a verse number drops sharply and no heading intervened.
    """
    tagged = {}
    ch = start_ch
    prev_v = 0
    # walk .v blocks and headings together, in order
    marks = []
    for m in VBLOCK.finditer(html):
        marks.append((m.start(), "v", m.group(1)))
    for m in HEAD.finditer(html):
        cv = HEAD_CV.search(detag(m.group(1)))
        if cv:
            marks.append((m.start(), "ch", int(cv.group(1))))
    marks.sort()

    for _, kind, payload in marks:
        if kind == "ch":
            if start_ch <= payload <= end_ch:
                ch = payload
                prev_v = 0
            continue
        seg = payload
        nums = NUM.findall(seg)
        if not nums:
            continue
        v = int(nums[0])
        if v < prev_v - 2 and ch < end_ch:
            ch += 1
        prev_v = v
        roots = tagged.setdefault((ch, v), set())
        roots.update(ROOTSPAN.findall(seg))
    return tagged


def verse_text(html, v):
    """Best-effort detagged English of a verse, for the report."""
    for m in VBLOCK.finditer(html):
        seg = m.group(1)
        nums = NUM.findall(seg)
        if nums and int(nums[0]) == v:
            t = detag(re.sub(r"<sup\b.*?</sup>", "", seg, flags=re.S))
            return re.sub(r"^\d+\s*", "", t)
    return ""


# ----------------------------------------------------------------- audit

def built_units(units_json):
    for u in units_json["units"]:
        if u.get("built"):
            path = os.path.join(UNITS, u["slug"] + ".html")
            if os.path.exists(path):
                yield u, open(path, encoding="utf-8").read()


def in_range(cv, lo, hi):
    return lo <= cv <= hi


def forms_report(only=None):
    """For each thread with a stem spec, list every distinct word form its
    stems match across the whole book — counts, chapters, and which forms the
    `exclude` list rules out. Use this to sanity-check a stem set (esp. one the
    research project just handed back) before trusting the coverage audit."""
    verses = load_greek()
    threads = {t["id"]: t for t in json.load(
        open(os.path.join(DATA, "threads.json"), encoding="utf-8"))["threads"]}
    stems = json.load(open(os.path.join(os.path.dirname(__file__),
                      "thread-stems.json"), encoding="utf-8"))["stems"]

    want = set(only) if only else None
    targets = [tid for tid in threads
               if tid in stems and stems[tid].get("stems")
               and (want is None or tid in want)]
    if want:
        for tid in want:
            if tid not in targets:
                print(f"  (no stem spec for '{tid}' in thread-stems.json)")

    for tid in targets:
        spec = stems[tid]
        raw_stems = [strip_accents(s) for s in spec["stems"]]
        exclude = {strip_accents(x) for x in spec.get("exclude", [])}
        kept, dropped = {}, {}
        for ch, v, txt in verses:
            for w in GREEKWORD.findall(txt):
                sw = strip_accents(w)
                if not any(st in sw for st in raw_stems):
                    continue
                bucket = dropped if sw in exclude else kept
                e = bucket.setdefault(sw, {"surface": w, "n": 0, "ch": set()})
                e["n"] += 1
                e["ch"].add(ch)
        print(f"\n=== {tid}  stems: {', '.join(spec['stems'])}"
              f"{'  exclude: ' + str(len(exclude)) if exclude else ''} ===")
        for sw, e in sorted(kept.items(), key=lambda kv: -kv[1]["n"]):
            chs = ",".join(str(c) for c in sorted(e["ch"]))
            print(f"    {e['surface']:16} {_translit(e['surface']):18} "
                  f"{e['n']:2}x  ch {chs}")
        if dropped:
            print("    — excluded —")
            for sw, e in sorted(dropped.items(), key=lambda kv: -kv[1]["n"]):
                chs = ",".join(str(c) for c in sorted(e["ch"]))
                print(f"    {e['surface']:16} {_translit(e['surface']):18} "
                      f"{e['n']:2}x  ch {chs}")
    return 0


def audit(only=None, stub_for=None):
    verses = load_greek()
    threads = {t["id"]: t for t in json.load(
        open(os.path.join(DATA, "threads.json"), encoding="utf-8"))["threads"]}
    stems = json.load(open(os.path.join(os.path.dirname(__file__),
                      "thread-stems.json"), encoding="utf-8"))["stems"]
    units_json = json.load(open(os.path.join(DATA, "units.json"), encoding="utf-8"))
    units = list(built_units(units_json))

    defined, phrase, undefined = [], [], []
    for tid in threads:
        if tid in stems and stems[tid].get("phrase"):
            phrase.append(tid)
        elif tid in stems and stems[tid].get("stems"):
            defined.append(tid)
        else:
            undefined.append(tid)

    targets = defined if not only else [t for t in defined if t in only]
    total_gaps = 0
    stub_lines = []

    for tid in targets:
        root = threads[tid]["root"]
        hits = greek_hits(verses, stems[tid])
        gaps, overs = [], []
        for u, html in units:
            lo, hi = parse_range(u["passage"])
            tmap = tagged_map(html, lo[0], hi[0])
            u_hits = {cv: w for cv, w in hits.items() if in_range(cv, lo, hi)}
            for cv, words in sorted(u_hits.items()):
                if root not in tmap.get(cv, set()):
                    gaps.append((u["slug"], cv, words,
                                 verse_text(html, cv[1])))
            for cv, roots in sorted(tmap.items()):
                if root in roots and cv not in u_hits:
                    overs.append((u["slug"], cv))

        if not gaps and not overs:
            print(f"  ✓ {tid:14} clean across {len(units)} built units "
                  f"({len(hits)} occ. book-wide)")
            continue
        print(f"  ✗ {tid:14} {len(gaps)} gap(s), {len(overs)} tagged-but-no-root")
        for slug, (c, v), words, txt in gaps:
            total_gaps += 1
            wl = " ".join(words)
            tl = " ".join(_translit(w) for w in words)
            print(f"      GAP  {slug}  {c}:{v}  ‹{wl}› ({tl})")
            if txt:
                print(f"           “{txt[:96]}”")
            stub_lines.append((tid,
                f'    {{ "unit": "{slug}", "verse": {v}, "text": "???", '
                f'"root": "{root}", "why": "{tl} {c}:{v}" }},'))
        for slug, (c, v) in overs:
            print(f"      OVER {slug}  {c}:{v}  tagged {root}, Greek has no "
                  f"{tid} root here — wrong verse?")

    if phrase:
        print(f"\n  phrase threads (coverage by hand, not audited): "
              f"{', '.join(sorted(phrase))}")
    if undefined:
        print(f"\n  NO STEMS DEFINED — add to pipeline/thread-stems.json:")
        for tid in sorted(undefined):
            print(f"      {tid:14} root=‹{threads[tid]['root']}›  "
                  f"translit: {threads[tid].get('translit', '')}")

    if stub_for is not None:
        want = set(stub_for)
        lines = [ln for tid, ln in stub_lines if not want or tid in want]
        print(f"\n--- retrofit-tags.json stubs "
              f"({'all audited' if not want else ', '.join(sorted(want))}) — "
              f"fill in \"text\", paste into retrofit-tags.json 'add' ---")
        for ln in lines:
            print(ln)
        if not lines:
            print("    (no gaps)")

    print(f"\n{total_gaps} built-unit gap(s) across "
          f"{len(targets)} audited thread(s).")
    return total_gaps


def main():
    args = sys.argv[1:]
    stub = None
    if "--stub" in args:
        i = args.index("--stub")
        stub = args[i + 1:] if len(args) > i + 1 else []
        args = args[:i]
    check = "--check" in args
    forms = "--forms" in args
    args = [a for a in args if not a.startswith("--")]
    only = args or None

    if forms:
        print("thread stem forms — every word each stem set matches\n")
        sys.exit(forms_report(only=only))

    print("thread coverage audit — Greek vs. built fragments\n")
    gaps = audit(only=only, stub_for=stub)
    if check and gaps:
        print("\n[audit] built-unit gaps exist — see above "
              "(warning only, not a build failure)")
    sys.exit(0)


if __name__ == "__main__":
    main()
