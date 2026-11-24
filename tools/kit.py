"""Verse-keyed reads of the sources, in pieces small enough to open.

    python tools/kit.py parts NN [--cap 80]       # the unit's commentaries as files <= cap KB
    python tools/kit.py range 20:1-16 [--source chrysostom,catena] [--cap 28] [--out FILE]
    python tools/kit.py bible MAR 10:17-31        # WEB text; --lxx for Brenton's LXX English
    python tools/kit.py greek 20:1-16             # SBLGNT per verse + lemma(morph) list
    python tools/kit.py calls NN                  # the Calls for Lane section of work/NN/calls.md

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
CAP_KB = 28          # range output (shell output stops near 30k characters)
PARTS_KB = 80        # comfortably opened with Read
COMMENTARIES = ["constable", "france", "davies-allison", "chrysostom", "catena", "ellicott"]
CORE = ["constable", "france", "davies-allison"]   # read whole; the rest by range


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
def cmd_parts(n, cap):
    r = unit_range(n)
    out = ROOT / "work" / f"{n:02d}" / "parts"
    out.mkdir(parents=True, exist_ok=True)
    lab = labels()
    for key in CORE:
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


def cmd_range(r, sources, cap, out=None):
    """Print (or with --out, write to a file for Read) the sections touching r."""
    text = "".join(f"## {key}: {x['title']} [{fmt((x['s'], x['e']))}]\n\n{x['text']}\n\n"
                   for key in sources for x in hits(key, r))
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(text, "utf-8")
        print(f"{out}  {len(text.encode()) // 1000} KB")
        return
    b = text.encode()
    print(b[:cap * 1000].decode("utf-8", errors="ignore"))
    if len(b) > cap * 1000:
        print(f"\n[cut at {cap} KB of {len(b) // 1000}: narrow the range, pass --source, or --out FILE and Read it]")


def cmd_bible(book, r, lxx):
    f = TEXT / ("brenton-lxx.txt" if lxx else "web-bible.txt")
    for line in f.read_text("utf-8").splitlines():
        m = re.match(r"(\w{3}) (\d+):(\d+) ", line)
        if m and m.group(1) == book.upper() and r[0] <= v(int(m.group(2)), int(m.group(3))) <= r[1]:
            print(line)


def cmd_calls(n):
    h = ROOT / "work" / f"{n:02d}" / "calls.md"
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


def main(a):
    if not a:
        sys.exit(__doc__)
    opt = {a[i]: a[i + 1] for i in range(len(a) - 1) if a[i].startswith("--") and a[i] != "--lxx"}
    pos = [x for i, x in enumerate(a) if not x.startswith("--") and not (i and a[i - 1] in opt)]
    cap = int(opt.get("--cap", PARTS_KB if a[0] == "parts" else CAP_KB))
    c = pos[0]
    if c == "parts":
        cmd_parts(int(pos[1]), cap)
    elif c == "range":
        src = opt["--source"].split(",") if "--source" in opt else COMMENTARIES + ["synoptic"]
        cmd_range(rng(pos[1]), src, cap, opt.get("--out"))
    elif c == "bible":
        cmd_bible(pos[1], rng(pos[2]), "--lxx" in a)
    elif c == "greek":
        cmd_greek(rng(pos[1]))
    elif c == "calls":
        cmd_calls(int(pos[1]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
