"""Independently check data/words/<ch>.json and data/lemmas.json against the
MorphGNT source. Does NOT import build_words.py, morphgnt.py or greek.py: it
re-reads the source file with its own whitespace split and never
transliterates, so a bug in the generator can't hide in both.

Checks (any failure exits non-zero):
  1. every chapter file is present, its "c" matches its name, and it has
     exactly the source's verses for that chapter -- no more, no fewer
  2. per verse: the same number of words as the source, word ids are
     bbccvv + position in order, and every row has exactly {w, t, l, m}
  3. transliterations use only Latin letters (with ē/ō, and a final ’ on
     elided forms like kat’), never Greek script;
     every parsing was decoded to words (no raw "V-:..." code left over)
  4. lemma ids follow the source's lemmas one-to-one: every occurrence of a
     Greek lemma carries the same id, and two Greek lemmas never share one
  5. lemmas.json: exactly {t, g, n, refs} per entry; n is the book count;
     refs are that lemma's verses in text order without repeats; t is the id
     minus its digit; every lemma has a gloss unless it's in GLOSS_EXCEPTIONS
     (empty as of 2026-09-30: all 1,680 matched the lexicon)

    python pipeline/verify_words.py
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

GLOSS_EXCEPTIONS = set()  # lemma ids allowed an empty gloss, with a reason each
TRANSLIT_RE = re.compile(r"^[A-Za-zēōĒŌ]+’?$")  # ’ marks elision (kat’, di’)
WORD_KEYS = {"w", "t", "l", "m"}
LEMMA_KEYS = {"t", "g", "n", "refs"}


def read_source(path):
    """-> [(ch, v, bbccvv, greek_lemma)] in text order, by plain split."""
    out = []
    for line in open(path, encoding="utf-8"):
        cols = line.split()
        if len(cols) != 7:
            continue
        ref = cols[0]
        out.append((int(ref[2:4]), int(ref[4:6]), ref, cols[6]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=os.path.join(HERE, "corpus", "morphgnt", "61-Mt-morphgnt.txt"))
    ap.add_argument("--data", default=os.path.join(ROOT, "data"))
    a = ap.parse_args()
    if not os.path.exists(a.source):
        sys.exit(f"MorphGNT not found at {a.source} -- run `python pipeline/fetch_corpus.py`")

    errs = []
    src = read_source(a.source)
    by_verse = defaultdict(list)
    for ch, v, ref, lemma in src:
        by_verse[(ch, v)].append((ref, lemma))
    chapters = sorted({ch for ch, _ in by_verse})

    lemma_to_id, id_to_lemma = {}, {}
    counts, refs = defaultdict(int), defaultdict(list)
    for ch in chapters:
        path = os.path.join(a.data, "words", f"{ch}.json")
        if not os.path.exists(path):
            errs.append(f"missing {path}")
            continue
        d = json.load(open(path, encoding="utf-8"))
        if d.get("c") != ch:
            errs.append(f"words/{ch}.json: c is {d.get('c')!r}")
        want = sorted(v for c, v in by_verse if c == ch)
        got = d.get("verses", {})
        if sorted(int(v) for v in got) != want:
            errs.append(f"words/{ch}.json: verses {sorted(int(v) for v in got)} != source {want}")
        for v in want:
            rows, source = got.get(str(v), []), by_verse[(ch, v)]
            if len(rows) != len(source):
                errs.append(f"{ch}:{v}: {len(rows)} words, source has {len(source)}")
                continue
            for i, (row, (bcv, glemma)) in enumerate(zip(rows, source), 1):
                where = f"{ch}:{v} word {i}"
                if set(row) != WORD_KEYS:
                    errs.append(f"{where}: keys {sorted(row)}")
                    continue
                if row["w"] != f"{bcv}{i:02d}":
                    errs.append(f"{where}: id {row['w']} != {bcv}{i:02d}")
                if not TRANSLIT_RE.match(row["t"]):
                    errs.append(f"{where}: transliteration {row['t']!r}")
                if not row["m"] or ":" in row["m"]:
                    errs.append(f"{where}: parsing not decoded: {row['m']!r}")
                lid = row["l"]
                if lemma_to_id.setdefault(glemma, lid) != lid:
                    errs.append(f"{where}: lemma id {lid} != {lemma_to_id[glemma]} elsewhere")
                if id_to_lemma.setdefault(lid, glemma) != glemma:
                    errs.append(f"{where}: id {lid} used for two Greek lemmas")
                counts[lid] += 1
                ref = f"{ch}:{v}"
                if not refs[lid] or refs[lid][-1] != ref:
                    refs[lid].append(ref)
    extra = [f for f in os.listdir(os.path.join(a.data, "words"))
             if f.endswith(".json") and int(f[:-5]) not in chapters]
    if extra:
        errs.append(f"stray chapter files: {extra}")

    lp = os.path.join(a.data, "lemmas.json")
    lem = json.load(open(lp, encoding="utf-8")).get("lemmas", {})
    if set(lem) != set(counts):
        errs.append(f"lemmas.json ids differ from the words: only in lemmas "
                    f"{sorted(set(lem) - set(counts))[:10]}, only in words "
                    f"{sorted(set(counts) - set(lem))[:10]}")
    for lid, e in lem.items():
        if set(e) != LEMMA_KEYS:
            errs.append(f"lemma {lid}: keys {sorted(e)}")
            continue
        if e["n"] != counts.get(lid):
            errs.append(f"lemma {lid}: n={e['n']}, the words count {counts.get(lid)}")
        if e["refs"] != refs.get(lid):
            errs.append(f"lemma {lid}: refs differ from the words")
        if e["t"] != lid.rstrip("0123456789"):
            errs.append(f"lemma {lid}: t={e['t']!r}")
        if not e["g"] and lid not in GLOSS_EXCEPTIONS:
            errs.append(f"lemma {lid}: no gloss (add to GLOSS_EXCEPTIONS with a reason if expected)")

    n_words = sum(counts.values())
    if errs:
        for e in errs[:50]:
            print("FAIL", e)
        print(f"verify_words: {len(errs)} failure(s)")
        sys.exit(1)
    print(f"verify_words: ok -- {len(chapters)} chapters, {len(by_verse)} verses, "
          f"{n_words} words, {len(lem)} lemmas, all glossed")


if __name__ == "__main__":
    main()
