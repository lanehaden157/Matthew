"""Where each unit stands, read from the files (no state is stored).

    python tools/unit_status.py          # every unit
    python tools/unit_status.py 20       # one unit

Looks in this checkout and every .claude/worktrees/* checkout, and reports the
furthest stage found for each unit, with where it was found.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT
# inside a worktree, the main checkout is three levels up
if ROOT.parent.name == "worktrees" and ROOT.parent.parent.name == ".claude":
    MAIN = ROOT.parent.parent.parent

STAGES = ["not started", "researched", "briefed", "verse by verse", "fact-checked",
          "awaiting calls", "calls answered", "built", "shipped"]
# files per stage: notes.md, briefing.md, verse-by-verse.md, factcheck.md, calls.md


def shipped(n):
    """unit-NN.html on origin/main."""
    r = subprocess.run(["git", "-C", str(MAIN), "cat-file", "-e", f"origin/main:units/unit-{n:02d}.html"],
                       capture_output=True)
    return r.returncode == 0


def stage(root, n):
    w = root / "work" / f"{n:02d}"
    h = w / "calls.md"
    if (root / "units" / f"unit-{n:02d}.html").exists():
        return 7
    if h.exists():
        text = h.read_text("utf-8")
        answers = re.search(r"^## Answers\s*\n(.+)", text, re.M | re.S)
        return 6 if answers and answers.group(1).strip() else 5
    for i, f in ((4, "factcheck.md"), (3, "verse-by-verse.md"), (2, "briefing.md"), (1, "notes.md")):
        if (w / f).exists():
            return i
    return 0


def calls(root, n):
    h = root / "work" / f"{n:02d}" / "calls.md"
    m = h.exists() and re.search(r"^## Calls for Lane \((\d+)\)", h.read_text("utf-8"), re.M)
    return m.group(1) if m else ""


def main(only):
    planned = range(1, 29)
    roots = [MAIN] + sorted((MAIN / ".claude" / "worktrees").glob("*/"))
    for n in planned:
        if only and n not in only:
            continue
        if shipped(n):
            print(f"{n:2d}  shipped")
            continue
        best, where = 0, ""
        for r in roots:
            s = stage(r, n)
            if s > best:
                best, where = s, ("main" if r == MAIN else r.name)
        root = MAIN if where == "main" else MAIN / ".claude" / "worktrees" / where
        extra = f"  ({calls(root, n)} calls)" if best == 5 else ""
        print(f"{n:2d}  {STAGES[best]}" + (f"  [{where}]" if where else "") + extra)


if __name__ == "__main__":
    main({int(a) for a in sys.argv[1:]})
