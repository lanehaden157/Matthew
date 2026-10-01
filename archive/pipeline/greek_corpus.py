"""Loaders for the two corpora canon_leads.py searches: MorphGNT's lemmatized
SBLGNT (all 27 NT books, Matthew included) and CenterBLC's Text-Fabric build
of Rahlfs' 1935 LXX. Both must be present via `python pipeline/fetch_corpus.py`
first (pipeline/corpus/ is git-ignored, not committed).

Everything downstream keys words by their TRANSLITERATED lemma
(`pipeline/greek.py`), never Strong's numbers or native script -- the two
corpora don't share a numbering scheme, but the same deterministic
transliterator run over each one's own lemma column gives a matching,
accent-insensitive key, exactly the way `data-root` slugs already collapse
inflected forms onto one stem.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import greek  # noqa: E402

CORPUS = os.path.join(HERE, "corpus")
MORPHGNT_DIR = os.path.join(CORPUS, "morphgnt")
LXX_DIR = os.path.join(CORPUS, "lxx")

# order of appearance in the MorphGNT repo == NT canonical order; "Mt" is
# Matthew, the book every lead is measured against, so it's never a "later"
# hit for itself.
NT_FILES = [
    ("Mt", "61-Mt-morphgnt.txt"), ("Mk", "62-Mk-morphgnt.txt"), ("Lk", "63-Lk-morphgnt.txt"),
    ("Jn", "64-Jn-morphgnt.txt"), ("Ac", "65-Ac-morphgnt.txt"), ("Ro", "66-Ro-morphgnt.txt"),
    ("1Co", "67-1Co-morphgnt.txt"), ("2Co", "68-2Co-morphgnt.txt"), ("Ga", "69-Ga-morphgnt.txt"),
    ("Eph", "70-Eph-morphgnt.txt"), ("Php", "71-Php-morphgnt.txt"), ("Col", "72-Col-morphgnt.txt"),
    ("1Th", "73-1Th-morphgnt.txt"), ("2Th", "74-2Th-morphgnt.txt"), ("1Ti", "75-1Ti-morphgnt.txt"),
    ("2Ti", "76-2Ti-morphgnt.txt"), ("Tit", "77-Tit-morphgnt.txt"), ("Phm", "78-Phm-morphgnt.txt"),
    ("Heb", "79-Heb-morphgnt.txt"), ("Jas", "80-Jas-morphgnt.txt"), ("1Pe", "81-1Pe-morphgnt.txt"),
    ("2Pe", "82-2Pe-morphgnt.txt"), ("1Jn", "83-1Jn-morphgnt.txt"), ("2Jn", "84-2Jn-morphgnt.txt"),
    ("3Jn", "85-3Jn-morphgnt.txt"), ("Jud", "86-Jud-morphgnt.txt"), ("Re", "87-Re-morphgnt.txt"),
]
NT_BOOKS = [b for b, _ in NT_FILES]

MORPHGNT_LINE_RE = re.compile(
    r"^(\d{2})(\d{2})(\d{2})\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)\s*$"
)


def _key(lemma_greek):
    return greek.transliterate(lemma_greek).lower()


def load_nt():
    """-> {book: [(chapter, verse, key, word)]} in file order (verse order),
    `key` the transliterated lemma, `word` the transliterated inflected
    surface form (for display)."""
    if not os.path.isdir(MORPHGNT_DIR):
        sys.exit(f"MorphGNT not found at {MORPHGNT_DIR} -- run "
                  "`python pipeline/fetch_corpus.py`")
    out = {}
    for book, fname in NT_FILES:
        path = os.path.join(MORPHGNT_DIR, fname)
        verses = []
        for line in open(path, encoding="utf-8"):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            m = MORPHGNT_LINE_RE.match(line)
            if not m:
                continue
            _, ch, v, lemma = m.groups()
            cols = line.split()
            surface = cols[4]  # "word" column: punctuation-stripped
            verses.append((int(ch), int(v), _key(lemma), greek.transliterate(surface)))
        out[book] = verses
    return out


# ---------------------------------------------------------------- LXX (Text-Fabric)

def _tf_values(path, limit):
    """Yield the first `limit` node values from a Text-Fabric plain-text
    feature file (word-slot nodes 1..limit, which is where the per-word
    book/chapter/verse/lemma features for this dataset live -- verified
    against pipeline/fetch_corpus.py's pinned commit; higher node types
    (book/chapter/verse nodes themselves) follow afterward and are not read).
    Each data line is either a bare value (implicit next node) or
    "start[-end]<TAB>value" (explicit node/range -- expanded here)."""
    lines = open(path, encoding="utf-8").read().split("\n")
    i = 0
    while lines[i] != "":
        i += 1
    i += 1  # skip the blank line ending the header
    node = 1
    while node <= limit and i < len(lines):
        line = lines[i]
        i += 1
        if "\t" in line:
            rng, value = line.split("\t", 1)
            if "-" in rng:
                start, end = (int(x) for x in rng.split("-"))
            else:
                start = end = int(rng)
            for _ in range(start, min(end, limit) + 1):
                yield value
            node = end + 1
        else:
            yield line
            node += 1


def load_lxx():
    """-> {book: [(chapter, verse, key)]} in text order. No display surface
    form is kept (only the lemma is available per-word in this dataset);
    leads print the transliterated lemma itself, which is enough to search
    biblehub/Logeion by hand."""
    for name in ("lex_utf8.tf", "book.tf", "chapter.tf", "verse.tf"):
        if not os.path.exists(os.path.join(LXX_DIR, name)):
            sys.exit(f"LXX Text-Fabric data not found ({name}) -- run "
                      "`python pipeline/fetch_corpus.py`")
    lex_path = os.path.join(LXX_DIR, "lex_utf8.tf")
    # word count = data lines after the header's trailing blank line
    with open(lex_path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    i = 0
    while lines[i] != "":
        i += 1
    n_words = len(lines) - (i + 1)
    if lines and lines[-1] == "":
        n_words -= 1

    lemmas = list(_tf_values(os.path.join(LXX_DIR, "lex_utf8.tf"), n_words))
    books = list(_tf_values(os.path.join(LXX_DIR, "book.tf"), n_words))
    chapters = list(_tf_values(os.path.join(LXX_DIR, "chapter.tf"), n_words))
    verses = list(_tf_values(os.path.join(LXX_DIR, "verse.tf"), n_words))

    out = {}
    order = []
    for book, ch, v, lemma in zip(books, chapters, verses, lemmas):
        if book not in out:
            out[book] = []
            order.append(book)
        if not lemma:
            continue
        out[book].append((int(ch), int(v), _key(lemma)))
    out["__order__"] = order
    return out


LXX_BOOKS_KEY = "__order__"
