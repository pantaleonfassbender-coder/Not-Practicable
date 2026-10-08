"""Draws assets/viz/rodman-acres.svg for module 7 (Rodman): areas affected by the barge canal works as the sources give them
(Callaway 1974; Boynton 1975; USGS WRI 4-72, 1973: 15 square miles = 9,600 acres).
Run from the site root: python tools/viz-rodman.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
ROWS = [("Rodman pool, flooded (1968)", 13000, "var(--river)", "#/text/rodman/rodman/3"),
        ("Ground water lowered, Inglis reach (1971)", 9600, "var(--water)", "#/text/rodman/inglis/5"),
        ("Hardwoods left standing to drown", 1135, "var(--land)", "#/text/rodman/rodman/3"),
        ("One property's land taken for the pool (Boynton)", 540, "var(--work)", "#/text/rodman/rodman/2")]


def build():
    W, H = 900, 290
    title = "What the water took, in acres"
    desc = "; ".join(f"{l}: about {v:,} acres" for l, v, _, _ in ROWS) + ". The Inglis figure is 15 square miles, converted."
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ra-t ra-d" font-family="var(--serif)">',
         f'<title id="ra-t">{escape(title)}</title><desc id="ra-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<text x="16" y="48" font-size="13" fill="var(--ink2)">Areas named in the sources of this module. Each label links to its passage.</text>']
    sc = 470 / 13000
    y = 74
    for l, v, c, h in ROWS:
        o.append(f'<a href="{h}"><text x="16" y="{y + 18}" font-size="13" fill="var(--ink)" text-decoration="underline">{escape(l)}</text></a>')
        o.append(f'<rect x="340" y="{y}" width="{max(3, v * sc):.0f}" height="26" fill="{c}"/><text x="{346 + v * sc:.0f}" y="{y + 18}" font-size="12.5" fill="var(--ink)">{v:,}</text>')
        y += 42
    o.append(f'<text x="16" y="{H - 30}" font-size="12" fill="var(--ink2)">Ground water lowered 0.5 to nearly 15 feet in a 15-square-mile area around the canal below Inglis Lock (USGS, 1973).</text>')
    o.append(f'<text x="16" y="{H - 12}" font-size="12" fill="var(--ink2)">How many families lived or farmed on these acres is not counted in the sources read.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "rodman-acres.svg").write_text(build(), encoding="utf-8")
print("ok")
