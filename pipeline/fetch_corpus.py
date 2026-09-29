"""Download the two corpora canon_leads.py reads: MorphGNT's lemmatized SBLGNT
(the New Testament, Matthew included) and the CenterBLC Text-Fabric build of
Rahlfs' 1935 LXX (Old Testament in Greek, Matthew's own background text).

Both are pinned to a commit so a re-run is reproducible; neither is committed
to this repo (pipeline/corpus/ is git-ignored) -- re-run this after a fresh
clone, same idea as Joshua's `npm ci` for morphhb.

    python pipeline/fetch_corpus.py            # fetch anything missing
    python pipeline/fetch_corpus.py --force    # re-fetch everything

Sources and licences:
  * github.com/morphgnt/sblgnt @ aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d --
    the SBLGNT text is under the SBLGNT EULA (sblgnt.com/license), same as
    MatthewSBLGNT.txt already in this repo; the lemmatization is CC-BY-SA 3.0.
    27 book files, ~11 MB.
  * github.com/CenterBLC/LXX @ 4829f3746c84d75576702498e75a68856358f289 --
    MIT. Only the four Text-Fabric feature files canon_leads.py actually reads
    (book/chapter/verse + the Unicode lemma) -- not the whole tf/1935/ folder,
    and not the text-fabric package: these are plain one-value-per-line (or
    "start-end<TAB>value" range) files, simple enough to parse by hand
    (see greek_corpus.py), no new dependency. ~15.5 MB.
"""
import argparse
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "corpus")

MORPHGNT_SHA = "aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d"
MORPHGNT_BASE = f"https://raw.githubusercontent.com/morphgnt/sblgnt/{MORPHGNT_SHA}"
MORPHGNT_FILES = [
    "61-Mt-morphgnt.txt", "62-Mk-morphgnt.txt", "63-Lk-morphgnt.txt",
    "64-Jn-morphgnt.txt", "65-Ac-morphgnt.txt", "66-Ro-morphgnt.txt",
    "67-1Co-morphgnt.txt", "68-2Co-morphgnt.txt", "69-Ga-morphgnt.txt",
    "70-Eph-morphgnt.txt", "71-Php-morphgnt.txt", "72-Col-morphgnt.txt",
    "73-1Th-morphgnt.txt", "74-2Th-morphgnt.txt", "75-1Ti-morphgnt.txt",
    "76-2Ti-morphgnt.txt", "77-Tit-morphgnt.txt", "78-Phm-morphgnt.txt",
    "79-Heb-morphgnt.txt", "80-Jas-morphgnt.txt", "81-1Pe-morphgnt.txt",
    "82-2Pe-morphgnt.txt", "83-1Jn-morphgnt.txt", "84-2Jn-morphgnt.txt",
    "85-3Jn-morphgnt.txt", "86-Jud-morphgnt.txt", "87-Re-morphgnt.txt",
]

LXX_SHA = "4829f3746c84d75576702498e75a68856358f289"
LXX_BASE = f"https://raw.githubusercontent.com/CenterBLC/LXX/{LXX_SHA}/tf/1935"
LXX_FILES = ["book.tf", "chapter.tf", "verse.tf", "lex_utf8.tf"]


def fetch(url, dest, force):
    if os.path.exists(dest) and not force:
        return False
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "matthew-study-pipeline"})
    with urllib.request.urlopen(req) as r, open(dest, "wb") as f:
        f.write(r.read())
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download even if present")
    a = ap.parse_args()

    got, skipped = 0, 0
    for name in MORPHGNT_FILES:
        dest = os.path.join(CORPUS, "morphgnt", name)
        if fetch(f"{MORPHGNT_BASE}/{name}", dest, a.force):
            got += 1
            print("fetched", dest)
        else:
            skipped += 1
    for name in LXX_FILES:
        dest = os.path.join(CORPUS, "lxx", name)
        if fetch(f"{LXX_BASE}/{name}", dest, a.force):
            got += 1
            print("fetched", dest)
        else:
            skipped += 1
    print(f"\n{got} fetched, {skipped} already present.")
    if got == 0 and skipped == 0:
        sys.exit("nothing fetched -- check the file lists above")


if __name__ == "__main__":
    main()
