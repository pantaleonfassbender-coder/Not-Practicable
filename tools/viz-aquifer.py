"""Draws assets/viz/aquifer-votes.svg for module 5 (The water under Florida): the two Senate votes on the ship canal
(17 March 1936, 34 to 39; 17 May 1939, 36 to 45) and the two estimates of 1937 (Board of Engineers $263,838,000;
Chief of Engineers $197,921,000; annual charges $8,641,000 against benefits $8,741,000).
Run from the site root: python tools/viz-aquifer.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/aquifer/"


def build():
    W, H = 900, 360
    title = "Two votes and two estimates, 1936–1939"
    desc = ("Senate, 17 March 1936: 34 for the canal money, 39 against. Senate, 17 May 1939: 36 for the canal bill, 45 against. "
            "1937: the Board of Engineers put a sea-level ship canal at $263,838,000 and found it not justified; the Chief of Engineers put it at "
            "$197,921,000, with annual charges of $8,641,000 against benefits to shipping of $8,741,000.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="av-t av-d" font-family="var(--serif)">',
         f'<title id="av-t">{escape(title)}</title><desc id="av-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<text x="16" y="48" font-size="13" fill="var(--ink2)">Each label links to its passage.</text>']
    sc = 380 / 50
    y = 80
    for lab, yes, no, h in [("Senate, 17 March 1936", 34, 39, "senate/5"), ("Senate, 17 May 1939", 36, 45, "last/2")]:
        o.append(f'<a href="{T}{h}"><text x="16" y="{y + 18}" font-size="13" fill="var(--ink)" text-decoration="underline">{lab}</text></a>')
        o.append(f'<rect x="200" y="{y}" width="{yes * sc:.0f}" height="12" fill="var(--land)"/><text x="{206 + yes * sc:.0f}" y="{y + 11}" font-size="12" fill="var(--ink)">{yes} for</text>')
        o.append(f'<rect x="200" y="{y + 15}" width="{no * sc:.0f}" height="12" fill="var(--work)"/><text x="{206 + no * sc:.0f}" y="{y + 26}" font-size="12" fill="var(--ink)">{no} against</text>')
        y += 50
    y += 20
    o.append(f'<text x="16" y="{y}" font-size="14" font-weight="bold" fill="var(--ink)">The Army against itself, 1937 (millions of dollars)</text>')
    y += 16
    sc2 = 560 / 270
    for lab, v, col, h in [("Board of Engineers: cost", 263.838, "var(--work)", "board/1"), ("Chief of Engineers: cost", 197.921, "var(--survey)", "board/4")]:
        o.append(f'<a href="{T}{h}"><text x="16" y="{y + 16}" font-size="12.5" fill="var(--ink)" text-decoration="underline">{lab}</text></a>')
        o.append(f'<rect x="200" y="{y + 2}" width="{v * sc2:.0f}" height="18" fill="{col}"/><text x="{206 + v * sc2:.0f}" y="{y + 16}" font-size="12" fill="var(--ink)">{v:,.1f}</text>')
        y += 28
    o.append(f'<a href="{T}board/4"><text x="16" y="{y + 18}" font-size="12.5" fill="var(--ink)" text-decoration="underline">Chief, a year: charges 8.641 · benefits 8.741</text></a>')
    o.append(f'<text x="360" y="{y + 18}" font-size="12" fill="var(--ink2)">a margin of $100,000 a year, before the wages are counted as relief</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "aquifer-votes.svg").write_text(build(), encoding="utf-8")
print("ok")
