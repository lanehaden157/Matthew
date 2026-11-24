"""OCR a scanned PDF into one text file per page (resumable).

    python tools/ocr_pdf.py sources/raw/davies-allison-vol3.pdf sources/ocr/davies-allison-vol3

Needs Tesseract (C:/Program Files/Tesseract-OCR) and pymupdf. Pages already
done are skipped, so a killed run picks up where it stopped.
"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import pymupdf

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_page(args):
    pdf, out, i = args
    txt = os.path.join(out, f"page-{i + 1:04d}.txt")
    if os.path.exists(txt):
        return i
    png = os.path.join(out, f"_p{i + 1:04d}.png")
    doc = pymupdf.open(pdf)
    doc[i].get_pixmap(dpi=300).save(png)
    doc.close()
    subprocess.run([TESS, png, txt[:-4], "-l", "eng", "--psm", "1"],
                   check=True, capture_output=True)
    os.remove(png)
    return i


def main(pdf, out):
    os.makedirs(out, exist_ok=True)
    n = pymupdf.open(pdf).page_count
    done = 0
    with ThreadPoolExecutor(max_workers=max(2, (os.cpu_count() or 4) - 2)) as ex:
        for _ in ex.map(ocr_page, [(pdf, out, i) for i in range(n)]):
            done += 1
            if done % 50 == 0:
                print(f"{done}/{n}", flush=True)
    print(f"done {n} pages", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
