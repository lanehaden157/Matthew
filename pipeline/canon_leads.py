"""Canon leads: where a unit's rare Greek words and shared two-word phrases
occur elsewhere in Matthew's own canon -- the LXX (Old Testament in Greek)
and the rest of the New Testament -- as a short reading list for the
research project's intertext pass (pass 3, Lane 2026-09-22).

    python pipeline/canon_leads.py 13            # -> canon-leads/canon-leads-unit-13.md
    python pipeline/canon_leads.py 13 --rare 30  # looser rare-word cutoff
    python pipeline/canon_leads.py --all         # every unit in data/units.json
    python pipeline/canon_leads.py               # built units from 13 on, + the next unbuilt one
                                                  # (build.py runs this; units 1-12 shipped
                                                  # before the intertext pass existed and are
                                                  # a backlog, not regenerated automatically)

LEADS, NOT CONCLUSIONS -- ported from Joshua's `canon_leads.py` (Lane,
2026-09-21). Claude Code finds where words recur; the Claude.ai project
decides which recurrences mean anything. Two kinds of hit only, because
listing every word is useless:

  * rare words -- a lemma in the passage that occurs in at most --rare verses
    across the LXX + the rest of the NT combined (default 20), and somewhere
    outside Matthew
  * shared phrases -- two adjacent lemmas from one verse of the passage that
    stand adjacent in an LXX verse too, where neither word is ultra-common
    and the pair itself is not a stock formula

What it cannot see, by design: common words (the tracked threads, traced by
hand anyway), links by theme or type-scene, and Synoptic parallels (Mark/Luke
already have their own comparison path, §"Synoptic parallel" in the style
reference) -- those are excluded from the "later NT" hits so they don't
swamp the list with material the artifact already handles elsewhere. Those
links, and anything a word search can't see, are the project side's job.

Source: MorphGNT's lemmatized SBLGNT (the NT) and CenterBLC's Text-Fabric
Rahlfs-1935 LXX -- both pinned in pipeline/fetch_corpus.py, read by
pipeline/greek_corpus.py. Matching is by TRANSLITERATED lemma
(pipeline/greek.py), not a shared numeric id -- the two corpora don't share
one. Everything printed is transliterated; no native Greek reaches the output.
"""
import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import greek_corpus as gc  # noqa: E402
from audit_thread_coverage import parse_range  # noqa: E402

UNITS_JSON = os.path.join(ROOT, "data", "units.json")
OUT_DIR = os.path.join(ROOT, "canon-leads")

# Matthew's own file: the passage's own occurrences, and never a "later" hit
# for itself. Mark/Luke/John are excluded from "later" hits too -- Synoptic
# echoes have their own component (aside.synoptic) and would otherwise
# swamp this list with material the artifact already surfaces elsewhere.
SELF_BOOK = "Mt"
SYNOPTIC_EXCLUDE = {"Mk", "Lk"}

RARE_DEFAULT = 20
PHRASE_WORD_MAX = 300   # a phrase word occurring in more verses than this is too common to signal
PHRASE_TOTAL_MAX = 15   # a pair in more LXX verses than this is a stock formula

FIRST_INTERTEXT_UNIT = 13  # units before this shipped without the intertext pass (backlog)


def _unit_row(rows, n):
    for u in rows:
        if u["n"] == n:
            return u
    return None


def load_corpus():
    nt = gc.load_nt()
    lxx = gc.load_lxx()
    lxx_order = lxx.pop(gc.LXX_BOOKS_KEY)
    return nt, lxx, lxx_order


def verse_freq(nt, lxx):
    """Verses touched, not raw occurrences -- a lemma used twice in one verse
    still counts once, matching Joshua's cutoff semantics."""
    freq = collections.Counter()
    for verses in nt.values():
        by_verse = collections.defaultdict(set)
        for ch, v, key, _ in verses:
            by_verse[(ch, v)].add(key)
        for keys in by_verse.values():
            freq.update(keys)
    for verses in lxx.values():
        by_verse = collections.defaultdict(set)
        for ch, v, key in verses:
            by_verse[(ch, v)].add(key)
        for keys in by_verse.values():
            freq.update(keys)
    return freq


def fmt_nt(book, ch, v):
    return f"{book} {ch}:{v}"


def fmt_lxx(book, ch, v):
    return f"{book} {ch}:{v}"


def passage_words(nt, passage):
    """Matthew's own words in the unit's passage, verse by verse, as
    (ref_str, [(key, surface), ...]) -- adjacency preserved for phrase leads."""
    lo, hi = parse_range(passage)
    by_verse = collections.OrderedDict()
    for ch, v, key, surface in nt[SELF_BOOK]:
        if lo <= (ch, v) <= hi:
            by_verse.setdefault((ch, v), []).append((key, surface))
    return [(f"{ch}:{v}", words) for (ch, v), words in by_verse.items()]


def rare_leads(nt, lxx, freq, unit_words, rare=RARE_DEFAULT):
    """Rare lemmas in the passage, with every occurrence outside Matthew
    (Mark/Luke excluded -- Synoptic material has its own component)."""
    seen = collections.OrderedDict()
    for ref, words in unit_words:
        for key, surface in words:
            if freq[key] <= rare:
                seen.setdefault(key, {"surface": surface, "refs": []})
                if ref not in seen[key]["refs"]:
                    seen[key]["refs"].append(ref)

    leads = []
    for key, info in seen.items():
        lxx_hits = []
        for book in lxx:
            for ch, v, k in lxx[book]:
                if k == key:
                    lxx_hits.append((book, ch, v))
        nt_hits = []
        for book, verses in nt.items():
            if book == SELF_BOOK or book in SYNOPTIC_EXCLUDE:
                continue
            for ch, v, k, surface in verses:
                if k == key:
                    nt_hits.append((book, ch, v, surface))
        if lxx_hits or nt_hits:
            leads.append({"key": key, "surface": info["surface"], "mt": info["refs"],
                          "freq": freq[key], "lxx": lxx_hits, "nt": nt_hits})
    # LXX hits first (the older, background link), then rarest overall
    leads.sort(key=lambda L: (not L["lxx"], L["freq"]))
    return leads


def phrase_leads(lxx, freq, unit_words):
    """Adjacent lemma pairs in the passage that also stand adjacent in an LXX
    verse. Both words under PHRASE_WORD_MAX total occurrences; the pair in at
    most PHRASE_TOTAL_MAX LXX verses. Overlapping pairs in one verse merge
    into a single phrase lead, with every LXX verse behind any of its pairs."""
    lxx_pairs = collections.defaultdict(list)
    for book, verses in lxx.items():
        by_verse = collections.OrderedDict()
        for ch, v, key in verses:
            by_verse.setdefault((ch, v), []).append(key)
        for (ch, v), keys in by_verse.items():
            for a, b in zip(keys, keys[1:]):
                lxx_pairs[(a, b)].append((book, ch, v))

    def qualifies(a, b):
        pkey = (a[0], b[0])
        return (a[0] != b[0] and pkey in lxx_pairs
                and freq[a[0]] <= PHRASE_WORD_MAX and freq[b[0]] <= PHRASE_WORD_MAX
                and len(set(lxx_pairs[pkey])) <= PHRASE_TOTAL_MAX)

    leads = collections.OrderedDict()
    for ref, words in unit_words:
        idx = [i for i in range(len(words) - 1) if qualifies(words[i], words[i + 1])]
        runs = []
        for i in idx:
            if runs and runs[-1][-1] == i - 1:
                runs[-1].append(i)
            else:
                runs.append([i])
        for run in runs:
            span = words[run[0]:run[-1] + 2]
            pkey = tuple(w[0] for w in span)
            hits = collections.OrderedDict()
            for i in run:
                for h in lxx_pairs[(words[i][0], words[i + 1][0])]:
                    hits.setdefault(h, True)
            lead = leads.setdefault(pkey, {"words": span, "mt": [], "hits": list(hits)})
            if ref not in lead["mt"]:
                lead["mt"].append(ref)
    for lead in leads.values():
        lead["hits"].sort(key=lambda h: (h[0], h[1], h[2]))
    return list(leads.values())


def render(n, passage, rare_list, phrase_list, rare):
    L = [f"# Canon leads — Unit {n} ({passage})", "",
         "Generated by `pipeline/canon_leads.py` from the LXX (Old Testament in "
         "Greek) and the rest of the New Testament. **Leads, not conclusions.** "
         "This lists where the unit's rare words and two-word phrases occur "
         "elsewhere. Deciding which ones matter is the intertext pass's job. "
         "Every lead gets a verdict in the ledger, a rejection included.", "",
         f"It cannot see: common words (rare cutoff: {rare} verses across the LXX "
         "+ NT), links by theme or type-scene, or Mark/Luke (Synoptic parallels "
         "have their own comparison path). Search for those separately. Lemmas "
         "are transliterated only, with no gloss -- look them up by hand.", ""]

    L += [f"## Shared phrases with the LXX ({len(phrase_list)})", ""]
    if not phrase_list:
        L += ["_None under the cutoffs._", ""]
    for p in phrase_list:
        ws = p["words"]
        mt = ", ".join(p["mt"])
        L.append(f"- **{' '.join(w[1] for w in ws)}** ({' + '.join(w[0] for w in ws)}) — "
                 f"Matt {mt}")
        for book, ch, v in p["hits"]:
            L.append(f"  - {fmt_lxx(book, ch, v)}")
    L.append("")

    L += [f"## Rare words ({len(rare_list)})", ""]
    if not rare_list:
        L += ["_None under the cutoff._", ""]
    for r in rare_list:
        mt = ", ".join(r["mt"])
        L.append(f"- **{r['surface']}** ({r['key']}) — Matt {mt}; "
                 f"{r['freq']} verses across the LXX + NT")
        if r["lxx"]:
            L.append("  - LXX: " + "; ".join(fmt_lxx(*h) for h in r["lxx"][:8])
                     + (" …" if len(r["lxx"]) > 8 else ""))
        if r["nt"]:
            L.append("  - Later (NT): " + "; ".join(
                f"{fmt_nt(b, c, v)} ({s})" for b, c, v, s in r["nt"][:8])
                + (" …" if len(r["nt"]) > 8 else ""))
    L.append("")
    return "\n".join(L)


def build(n, rare=RARE_DEFAULT, nt=None, lxx=None, freq=None, out_dir=OUT_DIR):
    units = json.load(open(UNITS_JSON, encoding="utf-8"))["units"]
    row = _unit_row(units, n)
    if row is None:
        sys.exit(f"unit {n} is not in data/units.json")
    if nt is None or lxx is None:
        nt, lxx, _ = load_corpus()
    freq = freq or verse_freq(nt, lxx)
    uw = passage_words(nt, row["passage"])
    md = render(n, row["passage"], rare_leads(nt, lxx, freq, uw, rare),
                phrase_leads(lxx, freq, uw), rare)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"canon-leads-unit-{n:02d}.md")
    open(path, "w", encoding="utf-8").write(md)
    return path


def current_units(units):
    """Every built unit from FIRST_INTERTEXT_UNIT on, plus the first unbuilt
    one -- the unit the project side is about to research, so its leads are
    waiting before pass 1. Units 1-12 shipped before the intertext pass
    existed; they're a tracked backlog (run a unit number explicitly to
    generate one), not regenerated by build.py."""
    out = [u["n"] for u in units if u.get("built") and u["n"] >= FIRST_INTERTEXT_UNIT]
    nxt = next((u["n"] for u in sorted(units, key=lambda u: u["n"]) if not u.get("built")), None)
    if nxt is not None:
        out.append(nxt)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("unit", nargs="?", type=int)
    ap.add_argument("--all", action="store_true", help="every unit in data/units.json")
    ap.add_argument("--rare", type=int, default=RARE_DEFAULT,
                    help=f"rare-word cutoff, in verses across the LXX + NT (default {RARE_DEFAULT})")
    a = ap.parse_args()
    nt, lxx, _ = load_corpus()
    freq = verse_freq(nt, lxx)
    rows = json.load(open(UNITS_JSON, encoding="utf-8"))["units"]
    if a.unit:
        units = [a.unit]
    elif a.all:
        units = [u["n"] for u in rows]
    else:
        units = current_units(rows)
    for n in units:
        print("wrote", build(n, a.rare, nt, lxx, freq))


if __name__ == "__main__":
    main()
