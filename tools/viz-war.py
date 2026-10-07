"""Draws assets/viz/war-reasons.svg for module 6 (A canal for the war): the reasons given for a canal across Florida,
1826–1942, as they appear in the passages of modules 1, 3, 5 and 6. Each dot links to its passage.
Run from the site root: python tools/viz-war.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
ROWS = ["Shipping, wrecks, insurance", "War and defence", "Land and settlement", "Work for the unemployed", "Oil"]
# (year, row, label, href)
DOTS = [(1826, 0, "White 1826: the reefs", "#/text/ridge/senate/2"),
        (1826, 1, "White 1826: in time of war", "#/text/ridge/senate/5"),
        (1826, 2, "White 1826: emigration", "#/text/ridge/senate/3"),
        (1855, 0, "Smith 1855: insurance, time", "#/text/ridge/rails/3"),
        (1855, 1, "Smith 1855: hostilities", "#/text/ridge/rails/3"),
        (1880, 0, "Gillmore 1880: tonnage", "#/text/ridge/company/3"),
        (1883, 0, "Stone 1883: wrecks and salvage", "#/text/ridge/company/6"),
        (1933, 3, "Memorial 1933: human labor", "#/text/relief/authority/3"),
        (1933, 0, "Memorial 1933: the Straits", "#/text/relief/authority/3"),
        (1935, 3, "Roosevelt 1935: work relief", "#/text/relief/loan/2"),
        (1937, 3, "Markham 1937: relief and navigation", "#/text/aquifer/board/4"),
        (1941, 1, "Andrews and Pepper 1941", "#/text/war/defence/1"),
        (1942, 1, "House 1942: submarines", "#/text/war/debate/1"),
        (1942, 4, "House 1942: oil for the East", "#/text/war/debate/4")]


def build():
    W, H = 900, 360
    x0, x1 = 230, 870
    sx = lambda y: x0 + (x1 - x0) * (y - 1820) / (1945 - 1820)
    title = "Why a canal? The reasons given, 1826–1942"
    desc = "; ".join(f"{y}: {l}" for y, _, l, _ in DOTS) + "."
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="wr-t wr-d" font-family="var(--serif)">',
         f'<title id="wr-t">{escape(title)}</title><desc id="wr-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<text x="16" y="48" font-size="13" fill="var(--ink2)">Each dot is a passage in this apparatus that argues for the canal on that ground; hover for the source, click to read it.</text>']
    for i, r in enumerate(ROWS):
        y = 90 + i * 44
        o.append(f'<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" stroke="var(--line)"/><text x="16" y="{y + 5}" font-size="13" fill="var(--ink)">{escape(r)}</text>')
    for yr in (1825, 1850, 1875, 1900, 1925, 1945):
        o.append(f'<text x="{sx(yr):.0f}" y="{90 + 5 * 44}" font-size="11.5" text-anchor="middle" fill="var(--ink2)">{yr}</text>')
    cols = ["var(--river)", "var(--capitol)", "var(--land)", "var(--work)", "var(--survey)"]
    for yr, row, lab, href in DOTS:
        o.append(f'<a href="{href}"><circle cx="{sx(yr):.0f}" cy="{90 + row * 44}" r="7" fill="{cols[row]}"><title>{escape(lab)}</title></circle></a>')
    o.append(f'<text x="16" y="{H - 14}" font-size="12" fill="var(--ink2)">Ships and war run through the whole record; work came in 1933, oil in 1942. Growth, the reason of the 1960s, follows in module 7.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "war-reasons.svg").write_text(build(), encoding="utf-8")
print("ok")
