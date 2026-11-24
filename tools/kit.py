"""Small, capped reads for unit agents, so no agent opens a big file whole.

    python tools/kit.py scenes NN                 # suggested scenes (from D&A / Constable headings)
    python tools/kit.py parts NN [--cap 80]       # cut the unit's sources into parts <= cap KB
    python tools/kit.py range 20:1-16 [--source constable,france] [--cap 45]
    python tools/kit.py bible MAR 10:17-31        # WEB text; --lxx for Brenton's LXX English
    python tools/kit.py digest NN 20:1-16         # digest entries touching these verses
    python tools/kit.py merge NN notes|verse|catches|factcheck
    python tools/kit.py calls NN                  # the handoff's Calls for Lane section
    python tools/kit.py greek 20:1-16             # SBLGNT per verse + lemma(morph) list
    python tools/kit.py assemble NN               # head + scene fragments -> source-artifacts/

Verse ranges: C:V, C:V-V, C:V-C:V. Book codes are the WEB's (GEN EXO ... ISA JER
EZE DAN ... MAT MAR LUK JOH ACT ROM ... REV; PSA, SOL = Song, EZE = Ezekiel).
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")   # Windows console default is cp1252
sys.path.insert(0, str(Path(__file__).resolve().parent))
from split_sources import DASH, overlaps, parse_range, units, v  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SEC = ROOT / "sources" / "sections"
TEXT = ROOT / "sources" / "text"
if not SEC.exists():   # inside a worktree without the copy: use the main checkout's
    for up in ROOT.parents:
        if (up / "sources" / "sections").exists():
            SEC, TEXT = up / "sources" / "sections", up / "sources" / "text"
            break
CAP_KB = 45          # range output
PARTS_KB = 80        # one source-reader agent per part
COMMENTARIES = ["constable", "france", "davies-allison", "chrysostom", "catena", "ellicott"]


def rng(s):
    s = s.replace(".", ":")
    m = re.fullmatch(rf"(\d+):(\d+)(?:\s*{DASH}\s*(?:(\d+):)?(\d+))?", s.strip())
    if not m:
        sys.exit(f"bad range: {s}")
    c1, v1, c2, v2 = m.groups()
    a = v(int(c1), int(v1))
    return a, (v(int(c2 or c1), int(v2)) if v2 else a)


def fmt(r):
    e = r[1] % 1000
    return f"{r[0] // 1000}:{r[0] % 1000}-{r[1] // 1000}:{'end' if e == 999 else e}"


def unit_range(n):
    return units()[n][0]


def records(key):
    f = SEC / f"{key}.jsonl"
    if not f.exists():
        return []
    return [json.loads(l) for l in f.read_text("utf-8").splitlines() if l.strip()]


def labels():
    f = SEC / "labels.json"
    return json.loads(f.read_text("utf-8")) if f.exists() else {}


def pieces(text, cap):
    """Split an oversize text at paragraph breaks into <= cap bytes."""
    if len(text.encode()) <= cap:
        return [text]
    out, cur = [], ""
    for para in re.split(r"\n\s*\n", text):
        if cur and len((cur + para).encode()) > cap:
            out.append(cur)
            cur = ""
        cur += para + "\n\n"
    return out + ([cur] if cur.strip() else [])


def hits(key, r):
    return [x for x in records(key) if overlaps((x["s"], x["e"]), r)]


# ---- commands -----------------------------------------------------------
def cmd_scenes(n):
    r = unit_range(n)
    for key in ("davies-allison", "constable"):
        seen = []
        for x in hits(key, r):
            title = re.sub(r", pdf p\. \d+$", "", x["title"])
            if x["s"] >= r[0] and x["e"] <= r[1] and x["e"] < v(99, 0) and (title, x["s"]) not in [s[:2] for s in seen]:
                seen.append((title, x["s"], x["e"]))
        if seen:
            print(f"# from {key}")
            for title, s, e in seen:
                print(f"{fmt((s, e))}  {title}")
            return
    print(f"no headings found; unit is {fmt(r)}")


def cmd_parts(n, cap):
    r = unit_range(n)
    out = ROOT / "work" / f"{n:02d}" / "parts"
    out.mkdir(parents=True, exist_ok=True)
    lab = labels()
    for key in COMMENTARIES:
        recs = hits(key, r)
        if not recs:
            continue
        parts, cur, cur_titles = [], "", []
        for x in recs:
            for p in pieces(x["text"], cap * 1000):
                if cur and len((cur + p).encode()) > cap * 1000:
                    parts.append((cur, cur_titles))
                    cur, cur_titles = "", []
                cur += p + "\n\n---\n\n"
                cur_titles.append(f"{x['title']} [{fmt((x['s'], x['e']))}]")
        if cur:
            parts.append((cur, cur_titles))
        for k, (text, titles) in enumerate(parts, 1):
            f = out / f"{key}-{k}.md"
            uniq = list(dict.fromkeys(re.sub(r", pdf p\. \d+", "", t) for t in titles))
            head = f"# {key} part {k}/{len(parts)}, unit {n}\n\n{lab.get(key, '')}\n\nHolds: {'; '.join(uniq)}\n\n---\n\n"
            f.write_text(head + text, "utf-8")
            print(f"{f.relative_to(ROOT).as_posix()}  {f.stat().st_size // 1000} KB")


def cmd_range(r, sources, cap):
    lab, total = labels(), 0
    for key in sources:
        for x in hits(key, r):
            t = f"## {key}: {x['title']} [{fmt((x['s'], x['e']))}]\n\n{x['text']}\n\n"
            if total + len(t.encode()) > cap * 1000:
                print(f"\n[cut at {cap} KB: narrow the range or pass --source]")
                return
            total += len(t.encode())
            print(t)


def cmd_bible(book, r, lxx):
    f = TEXT / ("brenton-lxx.txt" if lxx else "web-bible.txt")
    for line in f.read_text("utf-8").splitlines():
        m = re.match(r"(\w{3}) (\d+):(\d+) ", line)
        if m and m.group(1) == book.upper() and r[0] <= v(int(m.group(2)), int(m.group(3))) <= r[1]:
            print(line)


def cmd_digest(n, r):
    d = ROOT / "work" / f"{n:02d}" / "digests"
    for f in sorted(d.glob("*.md")):
        blocks = re.split(r"^(?=## )", f.read_text("utf-8"), flags=re.M)
        for b in blocks:
            m = re.match(rf"## (\d+:\d+(?:\s*{DASH}\s*(?:\d+:)?\d+)?)", b)
            if m and overlaps(rng(m.group(1)), r):
                print(f"[{f.stem}] {b.strip()}\n")


MERGE = {"notes": "notes.md", "verse": "verse-by-verse.md", "catches": "catches.md",
         "factcheck": "factcheck.md"}


def cmd_merge(n, kind):
    w = ROOT / "work" / f"{n:02d}"
    files = sorted((w / "scenes").glob(f"*-{kind}.md"), key=lambda p: int(p.name.split("-")[0]))
    body = "\n\n".join(f.read_text("utf-8").strip() for f in files)
    if kind == "notes":
        rows = len(re.findall(r"^\|\s*\d+:\d+", body, re.M))
        head = f"Unit {n}, {fmt(unit_range(n))}, notes\n\n"
        body = head + body + f"\n\nRows: Unit {n}: {rows} rows\n"
    (w / MERGE[kind]).write_text(body + "\n", "utf-8")
    print(f"{(w / MERGE[kind]).relative_to(ROOT).as_posix()}  {len(files)} scene files  {len(body.encode()) // 1000} KB")


def cmd_calls(n):
    h = ROOT / "work" / f"{n:02d}" / "handoff.md"
    m = re.search(r"^## Calls for Lane.*?(?=^## |\Z)", h.read_text("utf-8"), re.M | re.S)
    print(m.group(0).strip() if m else "no Calls for Lane section")


def cmd_greek(r):
    words = {}
    for line in (ROOT / "Matthew-words.tsv").read_text("utf-8").splitlines()[1:]:
        f = line.split("\t")
        m = re.match(r"Matt\.(\d+)\.(\d+)", f[1])
        if m and r[0] <= v(int(m.group(1)), int(m.group(2))) <= r[1]:
            words.setdefault(f[1], []).append(f"{f[3]}({f[4]})")
    for line in (ROOT / "Matthew-reading.txt").read_text("utf-8").splitlines():
        m = re.match(r"Matt (\d+):(\d+)\t", line)
        if m and r[0] <= v(int(m.group(1)), int(m.group(2))) <= r[1]:
            print(line)
            print("   " + " ".join(words.get(f"Matt.{m.group(1)}.{m.group(2)}", [])))


def cmd_assemble(n):
    w = ROOT / "work" / f"{n:02d}"
    r = unit_range(n)
    body, notes = [], []
    for f in sorted((w / "scenes").glob("*-fragment.html"), key=lambda p: int(p.name.split("-")[0])):
        part, _, ns = f.read_text("utf-8").partition("<!-- notes -->")
        body.append(part.strip())
        notes += re.findall(r"<li id=\"(s\d+-\d+)\">(.*?)</li>", ns, re.S)
    html = (w / "fragment-head.html").read_text("utf-8").strip() + "\n\n" + "\n\n".join(body)
    order = list(dict.fromkeys(re.findall(r'href="#(s\d+-\d+)"', html)))
    num = {old: i for i, old in enumerate(order, 1)}
    missing = [o for o in order if o not in dict(notes)] + [i for i, _ in notes if i not in num]
    for old, i in num.items():
        html = re.sub(rf'<a href="#{old}">[^<]*</a>', f'<a href="#n{i}">{i}</a>', html)
    text = dict(notes)
    ol = "\n".join(f'  <li id="n{num[i]}">{text[i]}</li>' for i in order if i in text)
    passage = units()[n][1]
    html += (f'\n\n<div class="notes">\n  <h2>Notes</h2>\n  <ol>\n{ol}\n  </ol>\n</div>\n\n'
             f"<footer>Translation rendered from the SBLGNT Greek of Matthew {passage} · Unit {n} of the "
             f"Matthew study · wooden to the Greek by design</footer>\n</article>\n")
    out = ROOT / "source-artifacts" / f"matthew_{n:02d}_translation.html"
    out.write_text(html, "utf-8")
    print(f"{out.relative_to(ROOT).as_posix()}  {len(body)} scenes  {len(num)} notes  {len(html.encode()) // 1000} KB")
    if missing:
        print("unmatched note ids: " + ", ".join(missing))


def main(a):
    if not a:
        sys.exit(__doc__)
    opt = {a[i]: a[i + 1] for i in range(len(a) - 1) if a[i].startswith("--") and a[i] != "--lxx"}
    pos = [x for i, x in enumerate(a) if not x.startswith("--") and not (i and a[i - 1] in opt)]
    cap = int(opt.get("--cap", PARTS_KB if a[0] == "parts" else CAP_KB))
    c = pos[0]
    if c == "scenes":
        cmd_scenes(int(pos[1]))
    elif c == "parts":
        cmd_parts(int(pos[1]), cap)
    elif c == "range":
        src = opt["--source"].split(",") if "--source" in opt else COMMENTARIES + ["synoptic"]
        cmd_range(rng(pos[1]), src, cap)
    elif c == "bible":
        cmd_bible(pos[1], rng(pos[2]), "--lxx" in a)
    elif c == "digest":
        cmd_digest(int(pos[1]), rng(pos[2]))
    elif c == "merge":
        cmd_merge(int(pos[1]), pos[2])
    elif c == "greek":
        cmd_greek(rng(pos[1]))
    elif c == "assemble":
        cmd_assemble(int(pos[1]))
    elif c == "calls":
        cmd_calls(int(pos[1]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
