"""Lädt und skaliert die Tafeln nach assets/plates/<id>.jpg (1400 px) und <id>_t.jpg (Vorschau).

    python tools/make-plates.py              # alle Tafeln
    python tools/make-plates.py gillmore1880_map

Quellen: "ia" = Seitenbild des Internet Archive mit Ausschnitt in Promille (x0, y0, x1, y1);
"commons" = Datei auf Wikimedia Commons (2400 px; "commonsfull" in voller Größe); "ufdc" = Seitenbild (JPEG 2000) der University of Florida Digital Collections; "local" = Datei im Ordner ../quellen (etwa von Florida Memory,
dessen Seiten keine automatischen Abrufe zulassen und die deshalb von Hand geladen werden); "pdf" = Seite eines
lokalen PDF ("pfad::seite", 1-basiert, mit PyMuPDF bei 200 dpi gerendert), etwa Bände des Congressional Serial Set
von govinfo.gov oder Ausgaben-PDFs der University of Florida.
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "plates"
UA = {"User-Agent": "NotPracticableResearch/1.0 (pantaleonfassbender@gmail.com)"}
IAP = "https://archive.org/download/{}/page/n{}.jpg"

Q = "../quellen/"
SER = Q + "federal/serialset/SERIALSET-"

PLATES = {
    # filled module by module: id -> (kind, source, crop in per mille [, rotation])
    # Modul 1: The ridge
    "sdoc1826_report": ("pdf", SER + "00126_00_00-003-0021-0000.pdf::1", (40, 20, 960, 900)),
    "board1829_summary": ("local", Q + "ridge/board1829_summary.png", None),   # S. 65 unten + S. 66 oben, zusammengesetzt
    "board1829_ocklawaha": ("pdf", SER + "00219_00_00-083-0185-0000.pdf::44", (0, 40, 1000, 470)),
    "pickell1832_ponds": ("pdf", SER + "00219_00_00-083-0185-0000.pdf::6", (40, 20, 980, 330)),
    "smith1855_railroad": ("pdf", SER + "00756_00_00-014-0076-0000.pdf::2", (40, 290, 960, 640)),
    "gillmore1880_map": ("pdf", SER + "01885_00_00-056-0154-0000.pdf::39", None),
    "obl1883_subscribed": ("pdf", Q + "state/verify/AA00089092_00041.pdf::2", (50, 418, 205, 452)),
    "ob1883_fixedfact": ("pdf", Q + "ridge/np/UF00048734_01281.pdf::3", (40, 225, 175, 520)),
    "pens1884_bubble": ("pdf", Q + "ridge/np/AA00083042_00037.pdf::1", (293, 339, 413, 414)),
    "oes1909_routes": ("pdf", Q + "state/verify/UF00075908_03173.pdf::1", (176, 478, 322, 650)),
    # Modul 2: The water-lane
    "barker1886_osceola": ("commons", "File:George Barker, Steamer Osceola on the Ocklawaha cph.3b42152.jpg", None),
    "lanier1875_lane": ("ia", IAP.format("floridaitsscene00lanigoog", 25), (60, 40, 960, 960)),
    "champney1873_marion": ("commons", "File:Marion sternwheeler 1873 Ocklawaha River Florida.jpg", None),
    "fenn1870_shingles": ("commons", "File:The Cypress-Shingle Yard, Ocklawaha River, Florida MET 201672.jpg", None),
    "prospectus1877_title": ("ia", IAP.format("cu31924022881555", 6), (30, 20, 980, 980)),
    "hart1890_card": ("commonsfull", "File:Hart's Daily Line Schedule Card.jpg", None),
    "okl1914_rates": ("ia", IAP.format("oklawahariverfla00unit", 7), (40, 150, 990, 470)),
    "detroit1902_ocklawaha": ("commons", "File:On the Ocklawaha, Florida-LCCN2008679617.jpg", None),
    "okl1914_proviso": ("ia", IAP.format("oklawahariverfla00unit", 1), (40, 560, 990, 800)),
}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
        return r.read()


def commons(title, full=False):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 2400, "format": "json"})
    ii = next(iter(json.loads(fetch(u))["query"]["pages"].values()))["imageinfo"][0]
    return Image.open(io.BytesIO(fetch(ii["url"] if full else (ii.get("thumburl") or ii["url"]))))


def save(pid, im):
    im = im.convert("RGB")
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    DEST.mkdir(parents=True, exist_ok=True)
    im.save(DEST / f"{pid}.jpg", quality=86)
    t = im.copy()
    t.thumbnail((420, 420))
    t.save(DEST / f"{pid}_t.jpg", quality=82)
    print(pid, im.size)


def main(ids):
    for pid in ids or PLATES:
        kind, src, arg = PLATES[pid]
        if kind == "local":
            path = ROOT / src
            if not path.exists():
                print(pid, "fehlt noch:", path)
                continue
            im = Image.open(path)
        elif kind == "pdf":
            import pymupdf
            path, page = src.rsplit("::", 1)
            pix = pymupdf.open(ROOT / path)[int(page) - 1].get_pixmap(dpi=200)
            im = Image.open(io.BytesIO(pix.tobytes("png")))
        elif kind == "ufdc":
            b, v, f = src.split("/")
            im = Image.open(io.BytesIO(fetch("https://ufdcimages.uflib.ufl.edu/" + "/".join(b[i:i + 2] for i in range(0, 10, 2)) + f"/{v}/{f}")))
        elif kind in ("commons", "commonsfull"):
            im = commons(src, kind == "commonsfull")
        else:
            im = Image.open(io.BytesIO(fetch(src)))
        if arg:
            if len(arg) == 5:
                im = im.rotate(arg[4], expand=True)
            w, h = im.size
            x0, y0, x1, y1 = arg[:4]
            im = im.crop((w * x0 // 1000, h * y0 // 1000, w * x1 // 1000, h * y1 // 1000))
        save(pid, im)


if __name__ == "__main__":
    main(sys.argv[1:])
