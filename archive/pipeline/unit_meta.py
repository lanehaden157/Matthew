"""The per-fragment metadata block: parse, validate, generate.

Every fragment carries, right after <article class="unit" …>, a block:

    <script type="application/json" id="unit-meta">
    { …the JSON below… }
    </script>

Shape:
  unit       int      unit number
  slug       str      "unit-09"            (derived if absent)
  passage    str      "Matthew 9:1-34"
  title      str
  movement   int      1 | 2 | 3            (optional; looked up from units.json)
  descriptor str      masthead tail line   (optional)
  discourse  bool     (optional)
  roots      [ {root, translit, gloss, echo?} ]
             every coloured root the unit tracks — translit + gloss ONLY, NO
             colour. A root whose translit bundles a small word-family
             ("misthos / apechō / apodidōmi") is still one root, one slug.
             `echo`: optional, one line naming where the word already
             appeared in the LXX, or where it reappears distinctively later in
             the canon, shown in the root's popover with a "cf." prefix
             (intertext pass, pass 3, Lane 2026-09-22; canon-leads/ is the
             mechanical half of that pass).
  threads    { opens:[{id,ref,note?}], payoffs:[{id,ref,note?}],
               candidates:[{root,why,stems?,exclude?}],
               retro:[{unit,verse,text,root,why,nth?,op?}] }
             opens/payoffs reference threads.json ids; optional `note` is the
             one-line popover prose for that beat, echoed into the thread-delta
             report ready to paste. candidates PROPOSE new threads (never written
             automatically); optional `stems`/`exclude` are accent-stripped Greek
             for thread-stems.json if Lane promotes the candidate.
             retro is a fix-list for EARLIER units in retrofit-tags.json shape
             (op defaults to "add") — things the close reading of this unit
             noticed about a prior one. The porter merges these into
             retrofit-tags.json and applies them. `root` must be a tracked
             thread or a declared root of the target unit.
             All of opens/payoffs/candidates/retro are consumed by the porter
             and dropped — generate() rebuilds the block from the data files, so
             none of this reaches the rendered page.

The block is inert (type="application/json", not executed) and invisible; the
site injects fragments with innerHTML so it just sits in the DOM.

This module is the single definition shared by port_artifact.py and build.py.
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

BLOCK_RE = re.compile(
    r'[ \t]*<script type="application/json" id="unit-meta">\s*'
    r'(\{.*?\})\s*</script>\n?',
    re.S,
)
ARTICLE_RE = re.compile(r'(<article class="unit"[^>]*>\n?)')


# ---------------------------------------------------------------- load helpers

def _load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


def _unit_row(units_json, n):
    for u in units_json["units"]:
        if u["n"] == n:
            return u
    return None


# ---------------------------------------------------------------- parse

def parse(html):
    """Return the metadata dict from a fragment string, or None if absent."""
    m = BLOCK_RE.search(html)
    if not m:
        return None
    return json.loads(m.group(1))


def strip(html):
    """Remove an existing metadata block (used before re-injecting)."""
    return BLOCK_RE.sub("", html, count=1)


def inject(html, meta):
    """Insert / replace the metadata block immediately after the <article> tag."""
    html = strip(html)
    m = ARTICLE_RE.search(html)
    if not m:
        raise ValueError("fragment has no <article class=\"unit\"> open tag")
    body = json.dumps(meta, indent=2, ensure_ascii=False)
    block = f'<script type="application/json" id="unit-meta">\n{body}\n</script>\n'
    return html[:m.end()] + block + html[m.end():]


# ---------------------------------------------------------------- validate

REQUIRED = ("unit", "passage", "title", "roots", "threads")


def validate(meta, threads_json=None):
    """Return a list of human-readable problems ([] == clean)."""
    errs = []
    if not isinstance(meta, dict):
        return ["metadata is not a JSON object"]
    for k in REQUIRED:
        if k not in meta:
            errs.append(f"missing required key: {k}")
    if "unit" in meta and not isinstance(meta["unit"], int):
        errs.append("unit must be an integer")

    for i, r in enumerate(meta.get("roots", []) or []):
        where = f"roots[{i}]"
        for k in ("root", "translit", "gloss"):
            if not r.get(k):
                errs.append(f"{where}: missing {k}")
        if "color" in r or "colour" in r:
            errs.append(f"{where}: carries a colour — the site assigns colours, "
                        "declare translit + gloss only")
        if not re.fullmatch(r"[a-z0-9-]+", r.get("root", "x")):
            errs.append(f"{where}: root '{r.get('root')}' must be [a-z0-9-]")
        if "kind" in r or "members" in r:
            errs.append(f"{where}: 'kind'/'members' are gone — every tracked "
                        "item is a plain root now")
        if "echo" in r and not (isinstance(r["echo"], str) and r["echo"].strip()):
            errs.append(f"{where}: 'echo' must be a non-empty string")
        extra = set(r) - {"root", "translit", "gloss", "echo"}
        if extra:
            errs.append(f"{where}: unknown key(s) {sorted(extra)} — roots[] is "
                        "{root, translit, gloss, echo?}")

    # C5 (platform-design-review.md): all four threads sub-keys are required,
    # matching Joshua's stricter rule -- any subset silently accepted meant a
    # missing key and an empty key looked identical, which is one more shape
    # `generate()` had to guess right. Empty list is how "nothing here" is said.
    th = meta.get("threads", {}) or {}
    for key in ("opens", "payoffs", "candidates", "retro"):
        if key not in th:
            errs.append(f"threads.{key} is required (use [] if there's nothing "
                        "to report)")
        elif not isinstance(th[key], list):
            errs.append(f"threads.{key} must be a list")

    for key in ("opens", "payoffs"):
        for i, e in enumerate(th.get(key, []) or []):
            if "note" in e and not isinstance(e["note"], str):
                errs.append(f"threads.{key}[{i}]: 'note' must be a string "
                            "(the popover line for this opens/payoff)")

    for i, c in enumerate(th.get("candidates", []) or []):
        if not c.get("root"):
            errs.append(f"threads.candidates[{i}]: missing 'root'")
        elif not re.fullmatch(r"[a-z0-9-]+", c["root"]):
            errs.append(f"threads.candidates[{i}]: root '{c['root']}' must be "
                        "[a-z0-9-]")
        for k in ("stems", "exclude"):
            if k in c and not (isinstance(c[k], list)
                               and all(isinstance(x, str) for x in c[k])):
                errs.append(f"threads.candidates[{i}]: '{k}' must be a list of "
                            "strings (accent-stripped Greek, for thread-stems.json)")

    if threads_json is not None:
        ids = {t["id"] for t in threads_json["threads"]}
        roots = {t["root"] for t in threads_json["threads"]}
        for key in ("opens", "payoffs"):
            for e in th.get(key, []) or []:
                if e.get("id") not in ids:
                    errs.append(f"threads.{key}: '{e.get('id')}' is not a "
                                "thread id in data/threads.json "
                                "(use threads.candidates to propose a new one)")

        this_slug = meta.get("slug") or f"unit-{meta.get('unit', 0):02d}"
        try:
            units_json = _load("units.json")
        except Exception:
            units_json = {"units": []}
        unit_roots = {u["slug"]: set((u.get("roots") or {}).keys())
                      for u in units_json["units"]}
        VALID_OPS = {"add", "retag", "retag_word", "untag_word", "unwrap",
                     "strip_span", "text"}
        for i, e in enumerate(th.get("retro", []) or []):
            w = f"threads.retro[{i}]"
            slug = e.get("unit", "")
            op = e.get("op", "add")
            if not re.fullmatch(r"unit-\d{2}", slug):
                errs.append(f"{w}: 'unit' must be a slug like 'unit-06'")
            elif slug == this_slug:
                errs.append(f"{w}: retro is for EARLIER units, not this one "
                            f"({slug}) — tag this unit's own occurrences in the "
                            "fragment or in retrofit-tags.json directly")
            if not e.get("why"):
                errs.append(f"{w}: missing 'why'")
            if op not in VALID_OPS:
                errs.append(f"{w}: op '{op}' not one of {sorted(VALID_OPS)}")
            # the root(s) this entry resolves a span to must have a colour
            targets = ([e.get("to")] if op in ("retag", "retag_word", "text")
                       else [e.get("root")] if op in ("add", "unwrap", "untag_word")
                       else [])
            for r in filter(None, targets):
                known = slug in unit_roots and r in unit_roots[slug]
                if r not in roots and not known:
                    errs.append(f"{w}: '{r}' is neither a tracked thread nor a "
                                f"declared root of {slug} — a tag that resolves "
                                "to no colour is a hard verify failure")
    return errs


# ---------------------------------------------------------------- generate
# (derive a metadata block for an already-built unit from the data files —
#  used to backfill units 1-8 and to keep blocks fresh in build.py)

def _threads_touching(threads_json, n):
    """opens/payoffs entries for unit n, carrying `note` through when present.

    C4 (platform-design-review.md): `note` stays OPTIONAL here, unlike
    Joshua's required version -- Matthew has 12 units of history and only
    114 of 228 opens/payoffs entries carry one yet, so requiring it now would
    fail the build over content that hasn't been written, not a bug. But it
    must round-trip: this used to drop `note` unconditionally, so every
    refresh_meta.py regen silently erased it from the fragment's own
    unit-meta block even though threads.json still had it (the same class of
    bug as Joshua's A2).
    """
    opens, payoffs = [], []
    for t in threads_json["threads"]:
        o = t.get("opens", {})
        if o.get("unit") == n:
            entry = {"id": t["id"], "ref": o.get("ref", "")}
            if o.get("note"):
                entry["note"] = o["note"]
            opens.append(entry)
        for p in t.get("payoffs", []):
            if p.get("unit") == n:
                entry = {"id": t["id"], "ref": p.get("ref", "")}
                if p.get("note"):
                    entry["note"] = p["note"]
                payoffs.append(entry)
    return opens, payoffs


def generate(n, units_json=None, threads_json=None, occurrences_json=None):
    """Build the metadata dict for unit n from the committed data files."""
    units_json = units_json or _load("units.json")
    threads_json = threads_json or _load("threads.json")
    row = _unit_row(units_json, n)
    if row is None:
        raise KeyError(f"unit {n} not in units.json")

    thread_roots = {t["root"] for t in threads_json["threads"]}
    roots = []
    for name, e in (row.get("roots") or {}).items():
        if isinstance(e, str):
            e = {"translit": "", "gloss": ""}
        # a unit's `roots` map is a harmless superset; keep the ones that are
        # either a tracked thread or actually carry translit/gloss
        if name not in thread_roots and not (e.get("translit") or e.get("gloss")):
            continue
        entry = {"root": name,
                 "translit": e.get("translit", ""),
                 "gloss": e.get("gloss", "")}
        if e.get("echo"):
            entry["echo"] = e["echo"]
        roots.append(entry)
    roots.sort(key=lambda r: r["root"])

    opens, payoffs = _threads_touching(threads_json, n)
    meta = {
        "unit": n,
        "slug": row["slug"],
        "passage": row["passage"],
        "title": row["title"],
        "movement": row.get("movement"),
        "roots": roots,
        # candidates/retro are hand-authored during porting and never derived
        # from the committed data files; generate() only knows to say "none
        # yet", same as it always has -- C5 just means it must say so, not omit.
        "threads": {"opens": opens, "payoffs": payoffs, "candidates": [], "retro": []},
    }
    if meta["movement"] is None:
        del meta["movement"]
    return meta
