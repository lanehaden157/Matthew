"""Deterministic Greek -> Latin transliteration, matching the scheme already in use
across the artifacts (ē ō ch ph th ps rh, ou/ai/ei/oi/au/eu, gg->ng, rough breathing h).
Good enough for legend headwords and endnote lemmas; every span it touches is logged
for review."""

import unicodedata

_BASE = {
    "α": "a", "β": "b", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "ē",
    "θ": "th", "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ξ": "x",
    "ο": "o", "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t", "υ": "y",
    "φ": "ph", "χ": "ch", "ψ": "ps", "ω": "ō",
}
_DIPH = {
    "ου": "ou", "αυ": "au", "ευ": "eu", "ηυ": "ēu",
    "αι": "ai", "ει": "ei", "οι": "oi", "υι": "ui",
    "γγ": "ng", "γκ": "nk", "γξ": "nx", "γχ": "nch",
}


def _stripaccents(s: str) -> str:
    out = []
    for ch in unicodedata.normalize("NFD", s):
        if unicodedata.category(ch) == "Mn":
            continue
        out.append(ch)
    return unicodedata.normalize("NFC", "".join(out))


def transliterate(text: str) -> str:
    """Transliterate a Greek word/phrase. Non-Greek characters pass through."""
    result = []
    for word in _split_keep(text):
        if not any("Ͱ" <= c <= "Ͽ" or "ἀ" <= c <= "῿" for c in word):
            result.append(word)
            continue
        rough = _has_rough_breathing(word)
        w = _stripaccents(word).lower()
        i, buf = 0, []
        while i < len(w):
            pair = w[i:i + 2]
            if pair in _DIPH:
                buf.append(_DIPH[pair])
                i += 2
                continue
            buf.append(_BASE.get(w[i], w[i]))
            i += 1
        out = "".join(buf)
        # initial rho -> rh
        if out.startswith("r"):
            out = "rh" + out[1:]
        if rough and out and out[0] in "aeiouēō y".replace(" ", ""):
            out = "h" + out
        # preserve leading capital
        if word[:1].isupper():
            out = out[:1].upper() + out[1:]
        result.append(out)
    return "".join(result)


def _split_keep(text: str):
    """Split into tokens, keeping separators (spaces, slashes, punctuation)."""
    tok, cur = [], []
    for ch in text:
        if ch.isalpha() or "̀" <= ch <= "ͯ":
            cur.append(ch)
        else:
            if cur:
                tok.append("".join(cur)); cur = []
            tok.append(ch)
    if cur:
        tok.append("".join(cur))
    return tok


def _has_rough_breathing(word: str) -> bool:
    for ch in unicodedata.normalize("NFD", word[:2]):
        if ch in ("̔",):  # combining reversed comma above = rough
            return True
    # precomposed forms with dasia
    for ch in word[:2]:
        name = unicodedata.name(ch, "")
        if "DASIA" in name or "ROUGH" in name:
            return True
    return False


if __name__ == "__main__":
    for t in ["βίβλος γενέσεως", "ἐγέννησεν", "ἅγιος", "πνεῦμα", "Ἐμμανουήλ",
              "δικαιοσύνη", "ῥαββί", "ἀναχωρέω", "προσκυνέω"]:
        print(f"{t}  ->  {transliterate(t)}")
