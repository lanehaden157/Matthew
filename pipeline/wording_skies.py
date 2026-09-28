"""One-shot translation revision: 'heaven(s)' -> 'sky/skies' across the study's
own wording, in source-artifacts/ (units 1-5 use the old wording; 6-8 already
say sky/skies). Verbatim quotations from copyrighted translations are protected.

Run once, then re-run pipeline/build.py. Prints a before/after list for review.
"""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source-artifacts")

# .compare rows whose <span class="src"> names one of these keep verbatim wording
PROTECT_SRC = {"NASB", "Hart", "Lattimore", "RSV", "ESV", "NRSV", "KJV", "NIV"}

SUBS = [
    (r"\bheavens\b", "skies"), (r"\bHeavens\b", "Skies"),
    (r"\bheaven\b", "sky"), (r"\bHeaven\b", "Sky"),
]

MASK = "@@MASKROW{}@@"


def mask_protected(html):
    store = []

    def stash(m):
        row = m.group(0)
        sm = re.search(r'<span class="src">([^<]*)</span>', row)
        if sm and sm.group(1).strip().strip('"') in PROTECT_SRC:
            store.append(row)
            return MASK.format(len(store) - 1)
        return row

    html = re.sub(r'<span class="row">.*?</span>\s*(?=<span class="row"|</span>\s*</span>)',
                  stash, html, flags=re.S)
    return html, store


def main():
    for path in sorted(glob.glob(os.path.join(SRC, "matthew_0[1-8]_translation.html"))):
        html = open(path, encoding="utf-8").read()
        masked, store = mask_protected(html)
        log = []
        for pat, repl in SUBS:
            def rec(m):
                a = m.start()
                ctx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", masked[max(0, a - 45):a + 25]))
                log.append(f"    {m.group(0)!r} -> {repl!r}   …{ctx}…")
                return repl
            masked = re.sub(pat, rec, masked)
        for i, row in enumerate(store):
            masked = masked.replace(MASK.format(i), row)
        if log:
            print(os.path.basename(path))
            print("\n".join(log))
            open(path, "w", encoding="utf-8").write(masked)
    print("\nrewrote source-artifacts. now run: python pipeline/build.py")


if __name__ == "__main__":
    main()
