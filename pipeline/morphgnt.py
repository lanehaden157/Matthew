"""MorphGNT (SBLGNT) word reader for the interlinear (build_words.py).

Adapted from bible-core biblecore/corpus/morphgnt.py (@25efd85, 2026-09-30):
FILES, the line regex, lemma_ids() and lemma_forms() are core's; load_words()
is core's parse() without the word-table / reading-file round trip (Matthew
has no data-w layer, so it reads the source lines straight into dicts); and
lemma_key() is core's lang/greek.py lemma_key over Matthew's own
transliterator (pipeline/greek.py). Book-agnostic: pass the osis id and the
folder of *-morphgnt.txt files (fetch_corpus.py puts them in
pipeline/corpus/morphgnt/). canon_leads.py reads the same files through
greek_corpus.py; the two aren't merged, since that one keys lemmas without
the digit suffix below.

Source lines (https://github.com/morphgnt/sblgnt):
    010101 N- ----NSF- Βίβλος Βίβλος βίβλος βίβλος
    bbccvv pos parse    text   word   normalized lemma
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import greek  # noqa: E402

DEFAULT_DIR = os.path.join(HERE, "corpus", "morphgnt")

# OSIS id -> MorphGNT file stem, in canonical order
FILES = [
    ("Matt", "61-Mt"), ("Mark", "62-Mk"), ("Luke", "63-Lk"), ("John", "64-Jn"),
    ("Acts", "65-Ac"), ("Rom", "66-Ro"), ("1Cor", "67-1Co"), ("2Cor", "68-2Co"),
    ("Gal", "69-Ga"), ("Eph", "70-Eph"), ("Phil", "71-Php"), ("Col", "72-Col"),
    ("1Thess", "73-1Th"), ("2Thess", "74-2Th"), ("1Tim", "75-1Ti"), ("2Tim", "76-2Ti"),
    ("Titus", "77-Tit"), ("Phlm", "78-Phm"), ("Heb", "79-Heb"), ("Jas", "80-Jas"),
    ("1Pet", "81-1Pe"), ("2Pet", "82-2Pe"), ("1John", "83-1Jn"), ("2John", "84-2Jn"),
    ("3John", "85-3Jn"), ("Jude", "86-Jud"), ("Rev", "87-Re"),
]
LINE_RE = re.compile(r"^(\d{2})(\d{2})(\d{2})\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$")
_MOVABLE = re.compile(r"\(.*?\)")


def _file(corpus_dir, stem):
    return os.path.join(corpus_dir, f"{stem}-morphgnt.txt")


def _rows(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = LINE_RE.match(line)
            if m:
                yield m.groups()


def lemma_key(lemma):
    """A Greek lemma's id: its transliteration, lower case. MorphGNT spells a
    handful of lemmas with a parenthesized movable letter -- ἔξεστι(ν),
    οὕτω(ς), εἴκοσι(ν) -- stripped first so the id is the cited form."""
    return greek.transliterate(_MOVABLE.sub("", lemma)).lower()


def lemma_ids(corpus_dir=DEFAULT_DIR):
    """Greek lemma -> id, over every NT book on disk, so the same lemma gets
    the same id in every book. A transliteration two lemmas share gets a
    digit on the second and later (by first appearance)."""
    ids, taken = {}, {}
    for _osis, stem in FILES:
        p = _file(corpus_dir, stem)
        if not os.path.exists(p):
            continue
        for g in _rows(p):
            lemma = g[8]
            if lemma in ids:
                continue
            key = lemma_key(lemma)
            n = taken.get(key, 0) + 1
            taken[key] = n
            ids[lemma] = key if n == 1 else f"{key}{n}"
    return ids


def lemma_forms(corpus_dir=DEFAULT_DIR):
    """id key -> the Greek lemma text (with accents), the inverse of
    lemma_ids -- for looking a lemma's gloss up in the morphological lexicon
    (greek_lexicon.py)."""
    return {v: k for k, v in lemma_ids(corpus_dir).items()}


def book_stem(osis):
    for o, stem in FILES:
        if o == osis:
            return stem
    raise ValueError(f"{osis} isn't a MorphGNT book (NT osis ids: "
                     f"{', '.join(o for o, _ in FILES)})")


def load_words(osis, corpus_dir=DEFAULT_DIR):
    """-> [{word_id, ch, v, surface, lemma (id key), morph}] in text order.
    word_id is bbccvv + two-digit position in the verse ("01050101"), core's
    scheme; morph is "<pos>:<parse>" for greek_morph.describe()."""
    path = _file(corpus_dir, book_stem(osis))
    if not os.path.exists(path):
        sys.exit(f"MorphGNT not found at {path} -- run `python pipeline/fetch_corpus.py`")
    ids = lemma_ids(corpus_dir)
    out, cur, pos_in_verse = [], None, 0
    for bk, c, v, pos, parse_, _t, word, _norm, lemma in _rows(path):
        if (c, v) != cur:
            cur, pos_in_verse = (c, v), 0
        pos_in_verse += 1
        out.append({"word_id": f"{bk}{c}{v}{pos_in_verse:02d}", "ch": int(c), "v": int(v),
                    "surface": word, "lemma": ids[lemma], "morph": f"{pos}:{parse_}"})
    return out
