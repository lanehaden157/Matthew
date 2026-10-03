"""Section index for Constable's Notes on Matthew -> constable-index.md.

    python tools/constable_index.py            # build the index
    python tools/constable_index.py --check    # exit 1 if the index is stale
    python tools/constable_index.py SRC OUT    # other source or output paths

SRC defaults to constable/matthew.txt: the plain-text copy of the project's
`/mnt/project/matthew.pdf`, saved byte-for-byte from the project (a real PDF run
through pdftotext numbers its lines differently, so the ranges wouldn't match
what the research chat sees). Replace that file whenever the project's copy
changes and re-run; the index records the source's sha1 and `--check` compares.

Each outline heading (it appears twice in the file: once in the outline, once in
the body) maps to its body line range, from the body heading to the line before
the next heading at the same or a higher level. Lines are counted with `\\n`
only, as `grep -a -n` and `sed -n` count them.
"""
import hashlib
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "constable" / "matthew.txt"
OUT = ROOT / "constable-index.md"

ROMAN = re.compile(r"^[IVX]+$")
DASH = r"(?:--|-|–|—)"
VREF = rf"\d+(?::\d+)?(?:\s*{DASH}\s*\d+(?::\d+)?)?"
REF = rf"(?:chs?\.?\s*)?{VREF}(?:\s*(?:,|and)\s*{VREF})*"
OUTLINE = re.compile(
    rf"^\s*(?P<label>[IVX]+|[A-Z]|\d+|[a-z])\.\s+(?P<title>\S.*?)\s+(?P<ref>{REF})\s*$"
)
HEADER = re.compile(r"^<!-- source-sha1: (\w+) -->$", re.M)


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def read_lines(path):
    text = path.read_bytes().decode("utf-8", errors="replace")
    return text.replace("\r", "").split("\n")


def level_of(label, last2):
    if label.isdigit():
        return 3
    if label.islower():
        return 4
    if ROMAN.match(label) and not (last2 and len(label) == 1 and ord(label) == ord(last2) + 1):
        return 1
    return 2


def outline_entries(lines):
    def starts_outline(i):
        m = OUTLINE.match(lines[i])
        if not (m and m["label"] == "I"):
            return False
        return any((n := OUTLINE.match(l)) and n["label"] == "A" for l in lines[i + 1:i + 25])

    first = next((i for i in range(len(lines)) if starts_outline(i)), None)
    if first is None:
        sys.exit("no outline lines found (expected e.g. 'I. The introduction of the King 1:1--4:11')")
    m0 = OUTLINE.match(lines[first])
    key0 = norm(f"{m0['label']}. {m0['title']}")
    body0 = next((i for i in range(first + 1, len(lines)) if norm(lines[i]).startswith(key0)), None)
    if body0 is None:
        sys.exit(f"the first outline heading never appears a second time: {key0!r}")
    entries, last2 = [], None
    for i in range(first, body0):
        m = OUTLINE.match(lines[i])
        if not m:
            continue
        lvl = level_of(m["label"], last2)
        if lvl == 2:
            last2 = m["label"]
        entries.append({"label": m["label"], "title": m["title"], "ref": m["ref"], "level": lvl})
    return entries, body0


LEAD = re.compile(r"^\d+:\d+(?:\s*(?:--|-|–|,)\s*\d+(?::\d+)?)*\s+")


def find_bodies(lines, entries, cursor):
    """Each entry's body heading, searched forward in outline order. A body
    heading may follow a verse reference ("16:13  1. ...") or be reworded a
    little ("Instructions" for "Instruction"): exact first, then close."""
    def heads(i):
        one = LEAD.sub("", norm(lines[i]))
        if not one:  # a blank line is not a heading, even with one right after it
            return ("", "")
        two = LEAD.sub("", norm(lines[i] + " " + (lines[i + 1] if i + 1 < len(lines) else "")))
        return one, two

    missing = []
    for e in entries:
        key = norm(f"{e['label']}. {e['title']}")
        hit = next((i for i in range(cursor, len(lines)) if any(h.startswith(key) for h in heads(i))), None)
        if hit is None:
            lead = norm(f"{e['label']}. ")
            hit = next((i for i in range(cursor, len(lines))
                        if any(h.startswith(lead) and SequenceMatcher(None, h[:len(key)], key).ratio() >= 0.75
                               for h in heads(i))), None)
        if hit is None:  # reworded title, same label and the same verses
            ref = norm(e["ref"])
            hit = next((i for i in range(cursor, len(lines))
                        if any(h.startswith(lead) and ref in h for h in heads(i))), None)
        if hit is None:
            missing.append(e)
        else:
            e["start"] = hit + 1
            cursor = hit + 1
    return missing


def build(src, out):
    lines = read_lines(src)
    entries, body0 = outline_entries(lines)
    missing = find_bodies(lines, entries, body0)
    found = [e for e in entries if "start" in e]
    biblio = next((i + 1 for i in range(found[-1]["start"], len(lines))
                   if re.match(r"^\s*Bibliography\s*$", lines[i])), None)
    last_line = (biblio - 1) if biblio else len(lines)
    for n, e in enumerate(found):
        nxt = next((f for f in found[n + 1:] if f["level"] <= e["level"]), None)
        e["end"] = (nxt["start"] - 1) if nxt else last_line

    sha = hashlib.sha1(src.read_bytes()).hexdigest()
    rows = [
        "# Constable, Notes on Matthew: section index",
        "",
        f"<!-- source-sha1: {sha} -->",
        "Generated by `tools/constable_index.py` from the project's `matthew.pdf`; don't edit.",
        f"Source: {len(lines)} lines. Read a section with `sed -n 'START,ENDp' matthew.pdf | tr -d '\\r' "
        "| grep -a -v \"Constable's Notes on Matthew\"`; each range runs from the section's body heading to the "
        "line before the next heading at the same or a higher level (a parent's range includes its children). "
        "See `resources.md` for the reading rules.",
        "",
        "Section | verses | body lines",
        "---|---|---",
    ]
    for e in found:
        ref = re.sub(DASH, "–", e["ref"])
        ref = ref.replace("––", "–")
        pad = " " * (e["level"] - 1)
        rows.append(f"{pad}{e['label']}. {e['title']} | {ref} | {e['start']}–{e['end']}")
    if missing:
        rows += ["", "Not located in the body (check the heading's wording):"]
        rows += [f"- {e['label']}. {e['title']} {e['ref']}" for e in missing]
    out.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    print(f"{out.name}: {len(found)} sections, {len(missing)} not located, source sha1 {sha[:10]}")
    return len(missing)


def check(src, out):
    if not out.exists():
        print(f"{out.name} is missing: run tools/constable_index.py")
        return 1
    m = HEADER.search(out.read_text(encoding="utf-8"))
    sha = hashlib.sha1(src.read_bytes()).hexdigest()
    if not m or m.group(1) != sha:
        print(f"{out.name} is stale (the source changed): run tools/constable_index.py")
        return 1
    print(f"{out.name} is current")
    return 0


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    src = Path(args[0]) if args else SRC
    out = Path(args[1]) if len(args) > 1 else OUT
    if not src.exists():
        sys.exit(f"no source at {src}: save the project's plain-text matthew.pdf there")
    if "--check" in argv:
        return check(src, out)
    return 1 if build(src, out) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
