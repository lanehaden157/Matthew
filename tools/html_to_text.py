"""Strip downloaded commentary HTML to plain text (stdlib only; nothing executed).

    python -I tools/html_to_text.py sources/downloads/catena sources/text/catena
    python -I tools/html_to_text.py sources/downloads/ellicott sources/text/ellicott

chNN.html -> chNN.txt. Drops script, style, nav and header/footer chrome.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SKIP = {"script", "style", "nav", "header", "footer", "noscript", "form", "select", "button"}
BLOCK = {"p", "div", "br", "h1", "h2", "h3", "h4", "h5", "li", "tr", "table", "blockquote"}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def convert(src, dst):
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob("ch*.html")):
        p = Text()
        p.feed(f.read_text("utf-8", errors="replace"))
        t = re.sub(r"[ \t\r\f\v]+", " ", "".join(p.out))
        t = re.sub(r"\n\s*\n\s*(\n\s*)+", "\n\n", t).strip()
        (dst / (f.stem + ".txt")).write_text(t + "\n", "utf-8")


if __name__ == "__main__":
    convert(Path(sys.argv[1]), Path(sys.argv[2]))
