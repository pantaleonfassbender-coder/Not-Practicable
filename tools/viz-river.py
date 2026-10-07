"""Draws assets/viz/river-rates.svg for module 2 (The water-lane): freight rates per hundred pounds to Jacksonville
from Leesburg (rail only) and from Sanford (on the St. Johns), by class, and the rate on a box of oranges by the
old Ocklawaha steamers and by rail (House Document 514, 63rd Congress, 2nd Session, p. 8).
Run from the site root: python tools/viz-river.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/river/"


def build():
    W, H = 900, 400
    classes = [("First", 68, 37), ("Second", 62, 32), ("Third", 57, 29), ("Fourth", 45, 24), ("Fifth", 38, 19), ("Sixth", 33, 16)]
    title = "Twice the rate: freight to Jacksonville, 1911"
    desc = ("Cents per hundred pounds to Jacksonville, by class, from Leesburg (by rail only) and from Sanford (on the St. Johns River): "
            + "; ".join(f"{c} class {a} and {b}" for c, a, b in classes)
            + ". A box of oranges from Leesburg cost 10 cents by the old Ocklawaha steamers; from Emeralda by the railroad's boat and train it cost 26 cents.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="rr-t rr-d" font-family="var(--serif)">',
         f'<title id="rr-t">{escape(title)}</title><desc id="rr-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<a href="{T}trade/3"><text x="16" y="48" font-size="13" fill="var(--ink2)" text-decoration="underline">Cents per hundred pounds, by freight class, as reported by the Army\'s district engineer. Link to the passage.</text></a>']
    sc = 380 / 70
    y = 70
    for c, a, b in classes:
        o.append(f'<text x="16" y="{y + 22}" font-size="13" fill="var(--ink)">{c} class</text>')
        o.append(f'<rect x="120" y="{y}" width="{a * sc:.0f}" height="14" fill="var(--land)"/><text x="{126 + a * sc:.0f}" y="{y + 12}" font-size="12" fill="var(--ink)">{a}</text>')
        o.append(f'<rect x="120" y="{y + 16}" width="{b * sc:.0f}" height="14" fill="var(--river)"/><text x="{126 + b * sc:.0f}" y="{y + 28}" font-size="12" fill="var(--ink)">{b}</text>')
        y += 40
    o.append(f'<rect x="120" y="{y + 4}" width="12" height="12" fill="var(--land)"/><text x="138" y="{y + 15}" font-size="12" fill="var(--ink)">Leesburg, at the head of the Ocklawaha: rail only</text>'
             f'<rect x="480" y="{y + 4}" width="12" height="12" fill="var(--river)"/><text x="498" y="{y + 15}" font-size="12" fill="var(--ink)">Sanford, on the St. Johns: river steamers</text>')
    # oranges
    x0 = 640
    o.append(f'<text x="{x0}" y="86" font-size="13.5" font-weight="bold" fill="var(--ink)">A box of oranges</text>')
    for i, (lab, v, col) in enumerate([("by the old steamers", 10, "var(--river)"), ("by the railroad's boat and train", 26, "var(--land)")]):
        yy = 104 + i * 64
        o.append(f'<rect x="{x0}" y="{yy}" width="{v * 7}" height="24" fill="{col}"/><text x="{x0 + v * 7 + 6}" y="{yy + 17}" font-size="13" fill="var(--ink)">{v} ¢</text>')
        o.append(f'<text x="{x0}" y="{yy + 42}" font-size="12" fill="var(--ink2)">{escape(lab)}</text>')
    o.append(f'<text x="{x0}" y="250" font-size="12" fill="var(--ink2)">Leesburg or Emeralda to Jacksonville</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "river-rates.svg").write_text(build(), encoding="utf-8")
print("ok")
