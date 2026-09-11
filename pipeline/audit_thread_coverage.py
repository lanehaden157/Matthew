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
    python pipeline/audit_thread_coverage.py --unit unit-11
                        # just one unit (port_artifact.py uses coverage_for_unit)

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
TAGS = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")
GREEKWORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def strip_accents(s):
    d = unicodedata.normalize("NFD", s)
    # drop combining marks, lowercase, and fold final sigma ς -> σ so a stem
    # written with medial σ matches a word that ends in the stem (φωσ ~ φῶς)
    return ("".join(c for c in d if not unicodedata.combining(c))
            .lower().replace("ς", "σ"))


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


def _compile_stems(stem_list):
    """A stem is a substring match, or — with a leading '^' — a word-start
    match (`^αφι` = word begins αφι). Returns a predicate on an accent-stripped
    word."""
    subs = [strip_accents(s[1:]) if s.startswith("^") else strip_accents(s)
            for s in stem_list]
    anchored = [s.startswith("^") for s in stem_list]
    pairs = list(zip(subs, anchored))

    def match(sw):
        return any(sw.startswith(s) if a else s in sw for s, a in pairs)
    return match


def greek_hits(verses, spec):
    """{ (ch,v): [surface words] } for one thread's stem spec."""
    match = _compile_stems(spec["stems"])
    exclude = {strip_accents(x) for x in spec.get("exclude", [])}
    out = {}
    for ch, v, txt in verses:
        hits = [w for w in GREEKWORD.findall(txt)
                if strip_accents(w) not in exclude and match(strip_accents(w))]
        if hits:
            out[(ch, v)] = hits
    return out


# ----------------------------------------------------------------- fragment side

NUM_CV = re.compile(r'<span class="n">\s*(?:(\d+):)?(\d+)\s*</span>')


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


def greek_index(verses):
    """maxv[ch] = last verse number of that chapter; present = set of (ch,v)
    that actually exist in the SBLGNT (so the three textual omissions —
    17:21, 18:11, 23:14 — are simply absent)."""
    maxv, present = {}, set()
    for ch, v, _ in verses:
        maxv[ch] = max(maxv.get(ch, 0), v)
        present.add((ch, v))
    return maxv, present


def expected_seq(lo, hi, maxv, present):
    """The canonical (ch,v) list for a unit's passage, straight from the Greek —
    the authority on how many verses each chapter has and where it rolls over."""
    (c1, v1), (c2, v2) = lo, hi
    seq, ch, v = [], c1, v1
    while (ch, v) <= (c2, v2):
        if (ch, v) in present:
            seq.append((ch, v))
        if ch < c2 and v >= maxv.get(ch, v):
            ch, v = ch + 1, 1
        else:
            v += 1
    return seq


def tagged_map(html, lo, hi, maxv, present, slug="?"):
    """{ (ch,v): set(data-root) } from the fragment, plus a list of warnings.

    Verse blocks (.v) are one-per-verse in canonical order; the chapter for a
    bare-integer number comes from position in the expected sequence (from the
    Greek), an explicit 'C:V' number is trusted as-is. Where the .v sequence
    skips verses — an embedded set-piece like the Lord's Prayer (6:9b-13) is a
    .prayer block, not .v — every data-root in the HTML between the bracketing
    verses is attributed to each skipped verse, AND to the verse immediately
    before the skip run: a Greek verse that opens a set-piece (6:9's "Our
    Father...") routinely has its own translation continue past its .v block's
    close into the set-piece's own markup, so the verse right before the gap
    gets the same gap content credited, not just the skipped ones. No
    heuristics for the chapter: anything that won't line up is reported,
    never guessed."""
    seq = expected_seq(lo, hi, maxv, present)
    blocks = [(m.start(), m.end(), m.group(1)) for m in VBLOCK.finditer(html)]
    numbered = [(s, e, seg, NUM_CV.search(seg)) for s, e, seg in blocks]
    numbered = [(s, e, seg, m) for s, e, seg, m in numbered if m]

    tagged, warn, si = {}, [], 0
    holefilled = set()   # verses whose tags were read from surrounding HTML,
                         # not their own .v block — imprecise, so exempt from
                         # the "tagged but no Greek root" (over-tag) check
    placed = []  # (cv, block_end) for hole-filling
    for bi, (s, e, seg, m) in enumerate(numbered):
        if m.group(1):
            cv = (int(m.group(1)), int(m.group(2)))
            while si < len(seq) and seq[si] < cv:
                si += 1
        else:
            v = int(m.group(2))
            # find this verse in what's left of the expected sequence
            ahead = next((k for k in range(si, len(seq)) if seq[k][1] == v), None)
            if ahead is None:
                warn.append(f"{slug}: verse block #{bi} (v{v}) has no match in "
                            f"the expected sequence from {seq[si] if si < len(seq) else 'end'}"
                            f" — numbering drift")
                continue
            cv = seq[ahead]
            si = ahead
        tagged.setdefault(cv, set()).update(ROOTSPAN.findall(seg))
        if placed:
            prev_cv, prev_end = placed[-1]
            skipped = [q for q in seq if prev_cv < q < cv]
            if skipped:
                roots = set(ROOTSPAN.findall(html[prev_end:s]))
                tagged.setdefault(prev_cv, set()).update(roots)
                holefilled.add(prev_cv)
                for q in skipped:
                    tagged.setdefault(q, set()).update(roots)
                    holefilled.add(q)
        si += 1
        placed.append((cv, e))
    return tagged, warn, holefilled


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
        match = _compile_stems(spec["stems"])
        exclude = {strip_accents(x) for x in spec.get("exclude", [])}
        kept, dropped = {}, {}
        for ch, v, txt in verses:
            for w in GREEKWORD.findall(txt):
                sw = strip_accents(w)
                if not match(sw):
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


def _load_all():
    verses = load_greek()
    maxv, present = greek_index(verses)
    threads = {t["id"]: t for t in json.load(
        open(os.path.join(DATA, "threads.json"), encoding="utf-8"))["threads"]}
    stems = json.load(open(os.path.join(os.path.dirname(__file__),
                      "thread-stems.json"), encoding="utf-8"))["stems"]
    units_json = json.load(open(os.path.join(DATA, "units.json"), encoding="utf-8"))
    return verses, maxv, present, threads, stems, units_json


def _classify(threads, stems):
    defined, phrase, undefined = [], [], []
    for tid in threads:
        if tid in stems and stems[tid].get("phrase"):
            phrase.append(tid)
        elif tid in stems and stems[tid].get("stems"):
            defined.append(tid)
        else:
            undefined.append(tid)
    return defined, phrase, undefined


def coverage_for_fragment(slug, html, passage, threads=None, stems=None):
    """Structured gap report for one fragment string across every defined
    thread — no units.json lookup, so it works during a port before the row
    exists. Returns {"gaps": [...], "overs": [...], "warnings": [...]};
    each gap is {thread, root, ch, v, words, translit, text}."""
    verses, maxv, present, th, st, _ = _load_all()
    threads = threads or th
    stems = stems or st
    lo, hi = parse_range(passage)
    tmap, warn, holefilled = tagged_map(html, lo, hi, maxv, present, slug)
    defined, _, _ = _classify(threads, stems)

    gaps, overs = [], []
    for tid in defined:
        root = threads[tid]["root"]
        hits = {cv: w for cv, w in greek_hits(verses, stems[tid]).items()
                if in_range(cv, lo, hi)}
        for cv, words in sorted(hits.items()):
            if root not in tmap.get(cv, set()):
                gaps.append({"thread": tid, "root": root, "ch": cv[0], "v": cv[1],
                             "words": words,
                             "translit": " ".join(_translit(w) for w in words),
                             "text": verse_text(html, cv[1])})
        for cv, roots in sorted(tmap.items()):
            if root in roots and cv not in hits and cv not in holefilled:
                overs.append({"thread": tid, "root": root,
                              "ch": cv[0], "v": cv[1]})
    return {"gaps": gaps, "overs": overs, "warnings": warn}


def coverage_for_unit(slug, threads=None, stems=None):
    """coverage_for_fragment for a BUILT unit, reading its passage from
    units.json and its html from units/<slug>.html."""
    uj = json.load(open(os.path.join(DATA, "units.json"), encoding="utf-8"))
    row = next((u for u in uj["units"] if u["slug"] == slug), None)
    if row is None:
        return {"gaps": [], "overs": [], "warnings": [f"{slug}: not in units.json"]}
    html = open(os.path.join(UNITS, slug + ".html"), encoding="utf-8").read()
    return coverage_for_fragment(slug, html, row["passage"], threads, stems)


def stem_preview(stems_list, exclude_list=None):
    """What a candidate stem set would match across the whole book — for the
    thread-delta report. Returns a list of {surface, translit, n, chapters},
    most frequent first, plus a `dropped` list for the exclude entries."""
    verses = load_greek()
    match = _compile_stems(stems_list)
    exclude = {strip_accents(x) for x in (exclude_list or [])}
    kept, dropped = {}, {}
    for ch, v, txt in verses:
        for w in GREEKWORD.findall(txt):
            sw = strip_accents(w)
            if not match(sw):
                continue
            b = dropped if sw in exclude else kept
            e = b.setdefault(sw, {"surface": w, "translit": _translit(w),
                                  "n": 0, "chapters": set()})
            e["n"] += 1
            e["chapters"].add(ch)
    fmt = lambda d: sorted(({**e, "chapters": sorted(e["chapters"])}
                            for e in d.values()), key=lambda e: -e["n"])
    return {"kept": fmt(kept), "dropped": fmt(dropped)}


def audit(only=None, stub_for=None, unit_slugs=None):
    verses, maxv, present, threads, stems, units_json = _load_all()
    units = [(u, h) for u, h in built_units(units_json)
             if not unit_slugs or u["slug"] in unit_slugs]

    defined, phrase, undefined = _classify(threads, stems)

    targets = defined if not only else [t for t in defined if t in only]
    total_gaps = 0
    stub_lines = []
    all_warn = []

    tmaps, holefilled, seqs = {}, {}, {}
    for u, html in units:
        lo, hi = parse_range(u["passage"])
        tmaps[u["slug"]], w, holefilled[u["slug"]] = tagged_map(
            html, lo, hi, maxv, present, u["slug"])
        seqs[u["slug"]] = expected_seq(lo, hi, maxv, present)
        all_warn += w

    for tid in targets:
        root = threads[tid]["root"]
        hits = greek_hits(verses, stems[tid])
        gaps, overs = [], []
        for u, html in units:
            lo, hi = parse_range(u["passage"])
            tmap = tmaps[u["slug"]]
            u_hits = {cv: w for cv, w in hits.items() if in_range(cv, lo, hi)}
            for cv, words in sorted(u_hits.items()):
                if root not in tmap.get(cv, set()):
                    gaps.append((u["slug"], cv, words,
                                 verse_text(html, cv[1])))
            for cv, roots in sorted(tmap.items()):
                if (root in roots and cv not in u_hits
                        and cv not in holefilled[u["slug"]]):
                    overs.append((u["slug"], cv))

        if not gaps and not overs:
            scope = (f"{len(units)} built unit" + ("s" if len(units) != 1 else "")
                     if not unit_slugs else ", ".join(unit_slugs))
            print(f"  ✓ {tid:14} clean across {scope} "
                  f"({len(hits)} occ. book-wide)")
            continue
        print(f"  ✗ {tid:14} {len(gaps)} gap(s), {len(overs)} tagged-but-no-root")
        for slug, (c, v), words, txt in gaps:
            total_gaps += 1
            wl = " ".join(words)
            tl = " ".join(_translit(w) for w in words)
            nth = 1 + sum(1 for q in seqs.get(slug, []) if q < (c, v) and q[1] == v)
            nth_f = f' "nth": {nth},' if nth > 1 else ""
            amb = "  ⚠ repeats across chapters — nth set" if nth > 1 else ""
            print(f"      GAP  {slug}  {c}:{v}  ‹{wl}› ({tl}){amb}")
            if txt:
                print(f"           “{txt[:96]}”")
            stub_lines.append((tid,
                f'    {{ "unit": "{slug}", "verse": {v},{nth_f} "text": "???", '
                f'"root": "{root}", "why": "{tl} {c}:{v}" }},'))
        for slug, (c, v) in overs:
            print(f"      OVER {slug}  {c}:{v}  tagged {root}, Greek has no "
                  f"{tid} root here — wrong verse?")

    if phrase and not unit_slugs:
        print(f"\n  phrase threads (coverage by hand, not audited): "
              f"{', '.join(sorted(phrase))}")
    if undefined and not unit_slugs:
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

    if all_warn:
        print(f"\n  ⚠ chapter/verse alignment — audit could not line these up "
              f"cleanly against the Greek:")
        for w in all_warn:
            print(f"      {w}")

    scope = "built-unit" if not unit_slugs else "/".join(unit_slugs)
    print(f"\n{total_gaps} {scope} gap(s) across "
          f"{len(targets)} audited thread(s).")
    return total_gaps


def main():
    args = sys.argv[1:]
    stub = None
    if "--stub" in args:
        i = args.index("--stub")
        stub = args[i + 1:] if len(args) > i + 1 else []
        args = args[:i]
    unit_slugs = None
    if "--unit" in args:
        i = args.index("--unit")
        unit_slugs = [a for a in args[i + 1:] if not a.startswith("--")]
        args = args[:i]
    check = "--check" in args
    forms = "--forms" in args
    args = [a for a in args if not a.startswith("--")]
    only = args or None

    if forms:
        print("thread stem forms — every word each stem set matches\n")
        sys.exit(forms_report(only=only))

    scope = f" — {', '.join(unit_slugs)}" if unit_slugs else " vs. built fragments"
    print(f"thread coverage audit — Greek{scope}\n")
    gaps = audit(only=only, stub_for=stub, unit_slugs=unit_slugs)
    if check and gaps:
        print("\n[audit] built-unit gaps exist — see above "
              "(warning only, not a build failure)")
    sys.exit(0)


if __name__ == "__main__":
    main()
