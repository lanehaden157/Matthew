"""Cut the commentaries in sources/ into one file per unit.

    python tools/split_sources.py            # all units, all sources found
    python tools/split_sources.py 20 21      # just these units

Reads sources/text/ (pdftotext / OCR output) and sources/raw/, writes
sources/units/NN/<source>.md, each opening with what it covers. Unit ranges
come from matthew-literary-unit-map.md. A section goes to every unit its verse
range touches, so a parent section's intro can land in two units.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
OUT = SRC / "units"
DASH = "[-–—]"


def v(c, n):
    return c * 1000 + n


def parse_range(s, chapter=None):
    """'21:18—22:46' | '19:1-12' | '23' | '24—25' | '1:1–25' -> (start, end)."""
    s = s.strip().rstrip(".")
    m = re.fullmatch(rf"(\d+)(?::(\d+))?(?:\s*{DASH}\s*(\d+)(?::(\d+))?)?", s)
    if not m:
        return None
    c1, v1, x, y = m.groups()
    c1 = int(c1)
    if v1 is None:                       # chapters only
        c2 = int(x) if x else c1
        return v(c1, 1), v(c2, 999)
    start = v(c1, int(v1))
    if x is None:
        return start, start
    if y is None:                        # 19:1-12
        return start, v(c1, int(x))
    return start, v(int(x), int(y))


def units():
    out = {}
    for m in re.finditer(r"\*\*Unit (\d+) — ([\d:–\-—]+) — ([^*]+?)\.?\*\*",
                         (ROOT / "matthew-literary-unit-map.md").read_text("utf-8")):
        out[int(m.group(1))] = (parse_range(m.group(2)), m.group(2), m.group(3))
    return out


def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]


def fmt(r):
    return f"{r[0] // 1000}:{r[0] % 1000}–{r[1] // 1000}:{r[1] % 1000 if r[1] % 1000 != 999 else 'end'}"


# ---- Constable ---------------------------------------------------------
CON_HEAD = re.compile(
    rf"^(?:[IVX]+\.|[A-Z]\.|\d+\.|[a-z]\.|\(\d+\)|\([a-z]\))?\s*(?P<title>[A-Z'\"].{{2,110}}?)\s+"
    rf"(?:CHS?\.\s*)?(?P<ref>\d+(?::\d+)?(?:\s*{DASH}\s*\d+(?::\d+)?)?)"
    rf"(?:\s*\(cf\..*\))?\s*$")
CON_NOISE = re.compile(r"^(Dr\. Constable's Notes on Matthew|2026 Edition|\d+|\f.*)$")


def constable():
    lines = (SRC / "text" / "constable.txt").read_text("utf-8").split("\n")
    body = next(i for i, l in enumerate(lines) if l.startswith("I. THE INTRODUCTION OF THE KING"))
    heads = []
    for i in range(body, len(lines)):
        m = CON_HEAD.match(lines[i].strip())
        if (m and len(lines[i]) < 160 and not re.match(r"^\d+:\d+", lines[i])
                and not re.search(r"\bvv?\.", lines[i])):  # chiasm rows: "D ... vv. 24-33"
            r = parse_range(m.group("ref"))
            if r:
                heads.append((i, r, lines[i].strip()))
    chunks = []
    for k, (i, r, title) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        text = [l.replace("\f", "") for l in lines[i:end]]
        text = [l for l in text if not CON_NOISE.match(l.strip())]
        chunks.append((r, title, "\n".join(text).strip()))
    return chunks


# ---- Chrysostom --------------------------------------------------------
def chrysostom():
    text = (SRC / "raw" / "chrysostom-homilies-matthew.txt").read_text("utf-8")
    hits = list(re.finditer(r"^HOMILY ([LXVI]+)\s*\nMATTHEW (\d+:\d+(?:[-–,]\s*\d+)*)", text, re.M))
    chunks = []
    for k, m in enumerate(hits):
        start = parse_range(re.split(r"[,]", m.group(2))[0])[0]
        nxt = parse_range(re.split(r"[,]", hits[k + 1].group(2))[0])[0] if k + 1 < len(hits) else v(28, 20)
        r = (start, max(start, nxt - 1))
        end = hits[k + 1].start() if k + 1 < len(hits) else len(text)
        chunks.append((r, f"Homily {m.group(1)} (from Matthew {m.group(2)})", text[m.start():end].strip()))
    return chunks


# ---- Davies & Allison vol. 3 (OCR pages) --------------------------------
def da_range(ref):
    """'19.1–12' | '20.20–8' (= 20:20-28) | 'Mt 19.1–23.39' -> range."""
    m = re.search(rf"(\d+)[.:](\d+)(?:\s*{DASH}\s*(\d+)(?:[.:](\d+))?)?", ref)
    if not m:
        return None
    c, a, x, y = m.groups()
    if x and y:
        return v(int(c), int(a)), v(int(x), int(y))
    if x and len(x) < len(a):                      # 20.20–8 -> 20:20-28
        x = a[: len(a) - len(x)] + x
    return v(int(c), int(a)), v(int(c), int(x or a))


def davies_allison():
    import pymupdf
    pdf = SRC / "raw" / "davies-allison-vol3.pdf"
    pages = SRC / "ocr" / "davies-allison-vol3"
    if not pdf.exists() or not pages.exists():
        return []
    d = pymupdf.open(pdf)
    covers = []
    for i in range(d.page_count):
        t = d[i].get_text().replace("\n", " ")
        if "Bloomsbury" in t:
            m = re.search(r'"(.+?)\.?"', t)
            covers.append((i + 1, m.group(1) if m else f"section at pdf p. {i + 1}"))
    chunks = []
    for k, (p1, title) in enumerate(covers):
        p2 = covers[k + 1][0] - 1 if k + 1 < len(covers) else d.page_count
        r = da_range(title) or (v(99, 0), v(99, 0))   # retrospect: no unit, see BOOK
        body = []
        for p in range(p1 + 1, p2 + 1):
            f = pages / f"page-{p:04d}.txt"
            if f.exists():
                body.append(f"[pdf p. {p}]\n" + f.read_text("utf-8", errors="replace").strip())
        missing = (p2 - p1) - len(body)
        note = f" ({missing} pages not yet OCR'd)" if missing else ""
        chunks.append((r, title + note, f"## {title}\n\n" + "\n\n".join(body)))
    return chunks


SOURCES = {
    "constable": ("Constable, Notes on Matthew (2026). Dispensational baseline.", constable),
    "chrysostom": ("Chrysostom, Homilies on Matthew (NPNF1 10, 1888). Patristic.", chrysostom),
    "davies-allison": ("Davies & Allison, ICC Matthew vol. 3 (1997), OCR; check odd words against context. "
                       "Private copy: paraphrase, never quote at length.", davies_allison),
}


def main(only):
    us = units()
    for key, (label, fn) in SOURCES.items():
        try:
            chunks = fn()
        except FileNotFoundError:
            print(f"{key}: source missing, skipped")
            continue
        if not chunks:
            print(f"{key}: nothing parsed, skipped")
            continue
        for n, (r, ref, title) in us.items():
            if only and n not in only:
                continue
            got = [c for c in chunks if overlaps(c[0], r)]
            if not got:
                continue
            d = OUT / f"{n:02d}"
            d.mkdir(parents=True, exist_ok=True)
            head = (f"# Unit {n} ({ref}, {title}): {key}\n\n{label}\n\n"
                    f"Sections ({len(got)}): " + "; ".join(f"{c[1]} [{fmt(c[0])}]" for c in got) + "\n\n---\n\n")
            (d / f"{key}.md").write_text(head + "\n\n---\n\n".join(c[2] for c in got) + "\n", "utf-8")
        book = [c for c in chunks if c[0][0] == v(99, 0)]
        if book:
            (OUT / f"book-{key}.md").write_text("\n\n".join(c[2] for c in book) + "\n", "utf-8")
        print(f"{key}: {len(chunks)} sections -> units")


if __name__ == "__main__":
    main({int(a) for a in sys.argv[1:]})
