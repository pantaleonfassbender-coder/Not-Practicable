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
    # Modul 3: Work for the relief rolls
    "sd1936_act": ("ufdc", "UF00055183/00001/gray0935-1.jp2", (40, 30, 960, 700)),
    "lcj1933_authority": ("local", Q + "state/verify/lcj1933_col.png", None),
    "sd1936_allotment": ("ufdc", "UF00055183/00001/gray0971-2.jp2", (40, 30, 960, 800)),
    "sd1936_votes": ("ufdc", "UF00055183/00001/gray1085-1.jp2", (60, 655, 960, 945)),
    "h1937_taylor": ("ufdc", "UF00018663/00001/00119.jp2", (60, 60, 960, 560)),
    "hd1937_rightofway": ("local", Q + "relief/hd194_rightofway.png", (20, 230, 990, 960)),   # H. Doc. 75-194, PDF-S. 60
    # Modul 4: Camp Roosevelt
    "ccc1935_boom": ("local", Q + "state/verify/ccc1935.png", None),
    "mer1935_axe": ("local", Q + "state/verify/mer1935.png", (0, 0, 1000, 760)),
    "sbh1935_sanitation": ("ia", IAP.format("annualreportstat1935flor", 23), (172, 160, 525, 730)),
    "sbh1935_table": ("local", Q + "people/img/sbh1935_n32_R.jpg", (180, 680, 700, 905)),
    "sd1936_railway": ("local", Q + "camp/gray0891-1.jp2", (80, 150, 890, 465)),
    "sd1936_cut": ("local", Q + "camp/gray0891-1.jp2", (80, 580, 890, 845)),
    "sd1936_slopes": ("local", Q + "camp/gray0891-2.jp2", (115, 225, 930, 465)),
    "sd1936_bridge": ("local", Q + "camp/gray0891-2.jp2", (115, 555, 930, 845)),
    "sd1936_belt": ("local", Q + "camp/gray0893-1.jp2", (105, 390, 920, 660)),
    "sh1936_mules": ("local", Q + "camp/sh1936_mules.png", (0, 0, 1000, 560)),
    "sh1936_matthews": ("local", Q + "people/img/sh_19360403_matthews.png", (192, 0, 795, 1000)),
    "sh1936_gloomy": ("local", Q + "camp/sh1936_gloomy.png", (0, 220, 530, 860)),
    "sh1936_hendricks": ("local", Q + "state/verify/sh1936_hendricks.png", (80, 160, 1000, 880)),
    # Modul 5: The water under Florida
    "hd1937_profile": ("local", Q + "aquifer/hd194_profile.png", None),
    "cr1936_buckman": ("ia", IAP.format("gpo-crecb-1936-pt-4-v-80-5", 19), (500, 0, 1000, 1000)),
    "cr1936_miami": ("ia", IAP.format("gpo-crecb-1936-pt-4-v-80-5", 22), (500, 0, 1000, 1000)),
    "cr1936_vote": ("ia", IAP.format("gpo-crecb-1936-pt-4-v-80-5", 23), (0, 0, 500, 1000)),
    "bct1936_funeral": ("local", Q + "state/verify/bct1936.png", None),
    "hd1937_route": ("local", Q + "aquifer/hd194_route.png", (10, 20, 990, 985)),
    "h1937_telegrams": ("ufdc", "UF00018663/00001/00129.jp2", (60, 740, 960, 950)),
    "cr1939_vote": ("local", Q + "aquifer/dli.ernet.78569_n1015.jpg", (500, 0, 1000, 520)),
    # Modul 6: A canal for the war
    "sh1941_defense": ("local", Q + "war/np/sh1941.png", (0, 70, 1000, 1000)),
    "cr1942_submarines": ("local", Q + "war/PL77711_n22.jpg", (345, 40, 655, 1000)),
    "cr1942_vote": ("local", Q + "war/PL77711_n23.jpg", (345, 40, 655, 1000)),
    "stat1942_act": ("pdf", Q + "federal/govinfo/STATUTE-56-Pg703.pdf::1", (40, 60, 990, 640)),
    "hrept1945_secret": ("pdf", SER + "10931_00_00-003-0002-0000.pdf::1", None),
    "sh1942_tanker": ("local", Q + "war/np/sh1942g.png", (0, 380, 690, 640)),
    "sh1942_duration": ("local", Q + "war/np/sh1942b.png", None),
    "sh1943_sanford": ("local", Q + "war/np/sh1943a.png", (0, 0, 640, 1000)),
    "sh1943_cut": ("local", Q + "war/np/sh1943b.png", None),
    # Modul 7: Rodman
    "fgs1956_industries": ("local", Q + "state/verify/fgs12_p45.jpg", (60, 0, 1000, 1000)),
    "sh1962_crushed": ("local", Q + "rodman/np/sh1962.png", (0, 0, 1000, 380)),
    "ppp1964_palatka": ("local", Q + "rodman/lbj_p399.png", None),
    "bc1964_activities": ("ufdc", "UF00075929/00014/00073.jp2", None),
    "tt1909_dam": ("local", Q + "rodman/np/tt1909.png", (0, 150, 1000, 1000)),
    "met1912_power": ("local", Q + "rodman/np/met1912b.png", None),
    "usgs1973_inglis": ("local", Q + "rodman/wri72_p13.png", None),
    "topo1949_rodman": ("pdf", Q + "state/topo/FL_Rodman_348331_1949_24000_geo.pdf::1", None),
    "topo1993_rodman": ("pdf", Q + "state/topo/FL_Rodman_348330_1993_24000_geo.pdf::1", None),
    "fwpca1967_excellent": ("local", Q + "rodman/micro_IA41159433_0119_n7.jpg", (60, 40, 950, 960)),
    "boynton1975_easement": ("pdf", Q + "rodman/courts/so2d311_412.pdf::3", None),
    "ca5_1974_ocklawaha": ("pdf", Q + "rodman/courts/f2d489_567.pdf::4", None),
    "ca5_1974_nixon": ("pdf", Q + "rodman/courts/f2d489_567.pdf::5", None),
    "hrept1970_lake": ("pdf", SER + "12884_08_00-035-1701-0000.pdf::1", None),
    # Modul 8: Undoing the canal
    "h1985_tax": ("local", Q + "undoing/micro_IA41152634_0813_n96.jpg", (100, 40, 940, 960)),
    "restudy1976_p13": ("ufdc", "NF00000163/00001/00018.jp2", None),
    "carter1977": ("local", Q + "undoing/micro_IA41153362_0079_n13.jpg", (20, 440, 520, 800)),
    "h1985_graham": ("local", Q + "undoing/micro_IA41152634_0813_n31.jpg", (100, 40, 920, 960)),
    "h1985_carr": ("local", Q + "undoing/micro_IA41152634_0813_n146.jpg", (100, 40, 920, 960)),
    "h1985_carr_statement": ("local", Q + "undoing/micro_IA41152634_0813_n175.jpg", (100, 40, 920, 760)),
    "h1985_lee": ("local", Q + "undoing/micro_IA41152634_0813_n153.jpg", (100, 40, 920, 960)),
    "h1985_mainer": ("local", Q + "undoing/micro_IA41152634_0813_n233.jpg", (100, 40, 920, 960)),
    "h1985_mainer_owners": ("local", Q + "undoing/micro_IA41152634_0813_n234.jpg", (100, 40, 920, 960)),
    "pl1990_a": ("pdf", Q + "undoing/stat104.pdf::41", None),
    "pl1990_b": ("pdf", Q + "undoing/stat104.pdf::42", None),
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
