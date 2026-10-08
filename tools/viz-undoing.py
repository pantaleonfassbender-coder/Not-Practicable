"""Draws assets/viz/undoing-costs.svg for module 8: the estimated cost of a canal across Florida, 1880–1985, as the passages
of this apparatus give it (millions of dollars, not adjusted for inflation). Each bar links to its passage.
Run from the site root: python tools/viz-undoing.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
ROWS = [("1880", "Gillmore: ship canal", 50, "#/text/ridge/company/3", "var(--survey)"),
        ("1883", "Canal company: tidewater canal", 46, "#/text/ridge/company/5", "var(--land)"),
        ("1933", "Canal authority: estimate, upper", 160, "#/text/relief/authority/4", "var(--land)"),
        ("1937", "Board of Engineers: sea-level canal", 263.838, "#/text/aquifer/board/1", "var(--survey)"),
        ("1937", "Chief of Engineers: sea-level canal", 197.921, "#/text/aquifer/board/4", "var(--survey)"),
        ("1941", "Andrews and Pepper: sea-level canal", 160, "#/text/war/defence/1", "var(--capitol)"),
        ("1942", "Act: authorized for the barge canal and works", 93, "#/text/war/act/1", "var(--capitol)"),
        ("1964", "Board of Conservation: barge canal, federal", 157.9, "#/text/rodman/ground/3", "var(--water)"),
        ("1971", "Nixon: barge canal, total", 180, "#/text/rodman/halt/2", "var(--river)"),
        ("1985", "Carr: to complete, 1985 prices", 605, "#/text/undoing/palatka/4", "var(--river)")]


def build():
    W, H = 900, 520
    title = "What would it cost? Estimates, 1880–1985"
    desc = "; ".join(f"{y} {l}: ${v:,.1f} million" for y, l, v, _, _ in ROWS) + ". Not adjusted for inflation."
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="uc-t uc-d" font-family="var(--serif)">',
         f'<title id="uc-t">{escape(title)}</title><desc id="uc-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<text x="16" y="48" font-size="13" fill="var(--ink2)">Millions of dollars, in the money of each year, not adjusted for inflation. Each label links to its passage.</text>']
    sc = 420 / 620
    y = 70
    for yr, l, v, h, c in ROWS:
        o.append(f'<a href="{h}"><text x="16" y="{y + 17}" font-size="12.5" fill="var(--ink)" text-decoration="underline">{yr} · {escape(l)}</text></a>')
        o.append(f'<rect x="380" y="{y + 3}" width="{v * sc:.0f}" height="20" fill="{c}"/><text x="{386 + v * sc:.0f}" y="{y + 18}" font-size="12" fill="var(--ink)">{v:,.1f}</text>')
        y += 40
    o.append(f'<text x="16" y="{H - 12}" font-size="12" fill="var(--ink2)">Ship canals and barge canals, federal and total costs are mixed here as the sources give them; the comparison shows how the figure moved, not one canal’s price.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "undoing-costs.svg").write_text(build(), encoding="utf-8")
print("ok")
