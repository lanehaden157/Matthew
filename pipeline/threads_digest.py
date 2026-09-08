"""data/threads.json  ->  threads-digest.md   (repo root)

A human-readable snapshot of the canonical cross-unit threads, for pasting into
the Claude.ai research project so the artifacts tag the right roots with the
right thread ids. Regenerate whenever threads.json changes (build.py does).

Never hand-edit threads-digest.md — it is derived.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "threads.json")
OUT = os.path.join(ROOT, "threads-digest.md")


def _ref(d):
    return f"{d.get('unit', '?')}" + (f" ({d['ref']})" if d.get("ref") else "")


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    threads = data["threads"]
    openc = sum(1 for t in threads if t.get("status") == "open")

    lines = [
        "# Cross-unit threads — canonical digest",
        "",
        f"Generated from `data/threads.json` (version {data.get('version', '?')}). "
        f"{len(threads)} threads, {openc} open.",
        "",
        "**This is the source of truth for thread tagging.** In a unit's artifact, "
        "a root that appears in the `id` column below is a *tracked thread*: tag it "
        "`<span class=\"r\" data-root=\"<id>\">…</span>` and list it under "
        "`threads.opens` / `threads.payoffs` in the unit-meta block. A root that is "
        "recurring but *not* here is unit-local — tag it with its own name and just "
        "list it in `roots`. To propose promoting a local root to a tracked thread, "
        "add it to `threads.candidates` with a one-line reason; Lane decides.",
        "",
        "| id | root (data-root) | translit | gloss | opens | payoffs | status |",
        "|---|---|---|---|---|---|---|",
    ]
    for t in sorted(threads, key=lambda x: (x.get("opens", {}).get("unit", 99), x["id"])):
        payoffs = " · ".join(_ref(p) for p in t.get("payoffs", [])) or "—"
        lines.append(
            f"| `{t['id']}` | `{t['root']}` | {t.get('translit', '')} | "
            f"{t.get('gloss', '')} | {_ref(t.get('opens', {}))} | {payoffs} | "
            f"{t.get('status', '')} |"
        )

    lines += ["", "## Notes per thread", ""]
    for t in sorted(threads, key=lambda x: x["id"]):
        lines.append(f"- **`{t['id']}`**: {t.get('note', '').strip()}")

    lines.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print(f"wrote {OUT} — {len(threads)} threads")


if __name__ == "__main__":
    main()
