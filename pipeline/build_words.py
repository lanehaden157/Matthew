"""The interlinear's data layer: every Greek word of the book, per chapter,
plus a lemma index for search. Run by build.py; checked by verify_words.py.

    python pipeline/build_words.py

Writes (generated -- never hand-edit):

  data/words/<ch>.json  {"c": 5, "verses": {"1": [{"w", "t", "l", "m"}]}}
                        every word of the chapter in text order: MorphGNT
                        word id (bbccvv + position), transliterated surface
                        form, lemma id, parsing in plain words.
  data/lemmas.json      {"lemmas": {"horaō": {"t", "g", "n", "refs"}}}:
                        lemma transliterated, the MorphGNT lexicon gloss (a
                        reader's identifier for the word, never the study's
                        rendering), count in the book, and every verse it
                        occurs in ("5:1"), deduplicated, in text order.

All chapters are written, not only built units: it's cheap, and search's
"every reference" needs the whole book. No native script is written
anywhere. Deterministic, so re-running changes nothing.

Adapted from bible-core biblecore/emit.py (@25efd85, 2026-09-30) -- see
docs/interlinear-pilot.md for what changed and why. The shapes are core's
Greek output unchanged. The book comes from data/units.json (the last unit's
passage gives the chapter count, which must match the corpus) instead of
core's book.json; words come from morphgnt.py; transliteration is
pipeline/greek.py, the study's own scheme, so interlinear words match the
legends and translation-choices.md. Core's Hebrew-only branches (Strong's,
the Aramaic "a" flag, Ketiv rows) and text.json are dropped.

Book-agnostic: --osis, --units and --data are parameters (defaults: Matthew
in this repo).
"""
import argparse
import json
import os
import re
import sys
from collections import OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import greek  # noqa: E402
import greek_lexicon  # noqa: E402
import morphgnt  # noqa: E402
from greek_morph import describe  # noqa: E402

LEXICON = os.path.join(HERE, "corpus", "lexicon", "lexemes.yaml")
PASSAGE_END_RE = re.compile(r"(\d+):\d+\s*[–-]\s*(?:(\d+):)?\d+\s*$")


def chapter_count(units_path):
    """The last chapter the unit map covers ("Matthew 28:1-20" -> 28)."""
    units = json.load(open(units_path, encoding="utf-8"))["units"]
    m = PASSAGE_END_RE.search(units[-1]["passage"])
    if not m:
        sys.exit(f"can't read a chapter range from {units[-1]['passage']!r}")
    return int(m.group(2) or m.group(1))


def words_by_chapter(osis):
    by_ch = defaultdict(lambda: defaultdict(list))
    lemma_refs = defaultdict(list)
    for w in morphgnt.load_words(osis):
        key = w["lemma"]
        row = OrderedDict(w=w["word_id"], t=greek.transliterate(w["surface"]),
                          l=key, m=describe(w["morph"]))
        by_ch[w["ch"]][str(w["v"])].append(row)
        ref = f"{w['ch']}:{w['v']}"
        if not lemma_refs[key] or lemma_refs[key][-1] != ref:
            lemma_refs[key].append(ref)
    return by_ch, lemma_refs


def lemmas(lemma_refs, counts):
    """The lemma id is already the transliterated lexical form (plus a digit
    when two NT lemmas share one); the gloss comes from the lexicon, keyed
    by the Greek lemma text, which lemma_forms() maps the id back to."""
    glosses = greek_lexicon.load_glosses(LEXICON)
    if not glosses:
        sys.exit(f"lexicon not found at {LEXICON} -- run `python pipeline/fetch_corpus.py`")
    forms = morphgnt.lemma_forms()
    out = OrderedDict()
    for key in sorted(lemma_refs):
        form = forms.get(key)
        out[key] = OrderedDict(t=key.rstrip("0123456789"),
                               g=glosses.get(form, "") if form else "",
                               n=counts[key], refs=lemma_refs[key])
    return out


def _write_json(path, obj):
    text = json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n"
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != text:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--osis", default="Matt")
    ap.add_argument("--units", default=os.path.join(ROOT, "data", "units.json"))
    ap.add_argument("--data", default=os.path.join(ROOT, "data"))
    a = ap.parse_args()

    by_ch, lemma_refs = words_by_chapter(a.osis)
    n_ch = chapter_count(a.units)
    if sorted(by_ch) != list(range(1, n_ch + 1)):
        sys.exit(f"units.json covers chapters 1-{n_ch}, the corpus has {sorted(by_ch)}")
    counts = defaultdict(int)
    for ch in by_ch.values():
        for ws in ch.values():
            for w in ws:
                counts[w["l"]] += 1
    wrote = 0
    for ch in sorted(by_ch):
        verses = OrderedDict((v, by_ch[ch][v]) for v in sorted(by_ch[ch], key=int))
        wrote += _write_json(os.path.join(a.data, "words", f"{ch}.json"), {"c": ch, "verses": verses})
    lem = lemmas(lemma_refs, counts)
    wrote += _write_json(os.path.join(a.data, "lemmas.json"), {"lemmas": lem})
    print(f"build_words: {len(by_ch)} chapter word files, {sum(counts.values())} words, "
          f"{len(lem)} lemmas ({wrote} file(s) changed)")


if __name__ == "__main__":
    main()
