"""Build listen/ pages (plain HTML, for Safari Read Aloud) from readings/NN-*.md.

    python tools/make_listen.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "listen"
CSS = ("body{font:19px/1.65 Georgia,serif;max-width:40rem;margin:0 auto;padding:1rem 16px 4rem;"
       "background:#fff;color:#1a1a1a}h1{font-size:1.5rem}h2{font-size:1.2rem;margin-top:2rem}"
       "a{color:inherit}@media(prefers-color-scheme:dark){body{background:#111;color:#e8e8e8}}")


def paras(path):
    return [p.strip() for p in path.read_text("utf-8").split("\n\n") if p.strip()]


def is_heading(p):
    return "\n" not in p and len(p) < 90 and not p.endswith((".", "?", "!", '"', "”"))


def page(title, body):
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title><style>{CSS}</style></head><body>\n{body}\n</body></html>\n')


def section(name, ps):
    out = [f"<h2>{html.escape(name)}</h2>"]
    for p in ps:
        tag = "h3" if is_heading(p) else "p"
        out.append(f"<{tag}>{html.escape(p)}</{tag}>")
    return "\n".join(out)


def main():
    OUT.mkdir(exist_ok=True)
    units = sorted({int(m.group(1)) for f in (ROOT / "readings").glob("*-briefing.md")
                    if (m := re.match(r"(\d+)-", f.name))})
    links = []
    for n in units:
        nn = f"{n:02d}"
        b, v = ROOT / "readings" / f"{nn}-briefing.md", ROOT / "readings" / f"{nn}-verse-by-verse.md"
        if not v.exists():
            continue
        body = (f'<p><a href="index.html">All units</a></p><h1>Matthew, unit {n}</h1>\n'
                + section("Briefing", paras(b)) + "\n" + section("Verse by verse", paras(v)))
        (OUT / f"unit-{nn}.html").write_text(page(f"Matthew unit {n}: listen", body), "utf-8")
        links.append(f'<li><a href="unit-{nn}.html">Unit {n}</a></li>')
    idx = '<h1>Matthew: listen</h1>\n<ul>\n' + "\n".join(links) + "\n</ul>"
    (OUT / "index.html").write_text(page("Matthew: listen", idx), "utf-8")
    print(f"listen/: {len(links)} unit page(s)")


if __name__ == "__main__":
    main()
