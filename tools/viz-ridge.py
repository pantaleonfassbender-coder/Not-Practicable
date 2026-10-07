"""Draws two graphics for module 1 (The ridge):
  assets/viz/ridge-heights.svg  the height of the ridge as the surveys found it, 1829–1883
      (House Document 8, 23-2, p. 65; House Document 185, 22-1, pp. 2, 6, 44; Ocala Banner, 1 September 1883);
  assets/viz/ridge-costs.svg    what a ship canal would have had to carry to pay, by Gillmore's figures of 1880
      (Senate Executive Document 154, 46-2, p. 14).
Run from the site root: python tools/viz-ridge.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/ridge/"


def head(W, H, ident, title, desc, sub):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="{ident}-t {ident}-d" font-family="var(--serif)">',
            f'<title id="{ident}-t">{escape(title)}</title><desc id="{ident}-d">{escape(desc)}</desc>',
            f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
            f'<text x="16" y="48" font-size="13" fill="var(--ink2)">{escape(sub)}</text>']


def heights():
    W, H = 900, 330
    rows = [
        ("Ridge of the peninsula, mean (1829)", 150, "board/3", "var(--survey)"),
        ("Watershed on Stone's line (1883)", 143, "company/5", "var(--land)"),
        ("Ridge crossed on Pickell's line (1832)", 116.849, "water/4", "var(--water)"),
        ("Bottom of the summit cut planned (1829)", 116.4, "water/1", "var(--water)"),
        ("Divide near the Ocklawaha (1829)", 87, "board/2", "var(--river)"),
    ]
    title = "How high is the ridge?"
    desc = ("Heights above the sea in feet, as the surveys found them: the mean height of the ridge of the peninsula 150 feet (Bernard and Poussin, 1829); "
            "the watershed on the canal company's line 143 feet (Stone, 1883); the ridge where Pickell's line crossed it 116.849 feet, and the bottom of the planned summit cut 116.4 feet (1829/1832); "
            "the divide near the Ocklawaha 87 feet, set aside in 1829 for want of water.")
    o = head(W, H, "rh", title, desc, "Feet above the sea, as each survey reported it. Each label links to its passage.")
    sc = 520 / 160
    y = 72
    for label, v, href, col in rows:
        o.append(f'<a href="{T}{href}"><text x="16" y="{y + 19}" font-size="13" fill="var(--ink)" text-decoration="underline">{escape(label)}</text></a>')
        o.append(f'<rect x="300" y="{y}" width="{v * sc:.0f}" height="28" fill="{col}"/>')
        o.append(f'<text x="{306 + v * sc:.0f}" y="{y + 19}" font-size="13" fill="var(--ink)">{v:g} ft</text>')
        y += 44
    o.append(f'<text x="16" y="{H - 14}" font-size="12" fill="var(--ink2)">The lowest crossing was the Ocklawaha divide; the engineers of 1829 dismissed it because no streams on the ridge could feed a canal there.</text>')
    o.append("</svg>")
    return "\n".join(o)


def costs():
    W, H = 900, 300
    rows = [
        ("Needed to pay running costs", 1.758, "var(--ink2)"),
        ("Passed the Florida Straits in a year", 2.6, "var(--river)"),
        ("Needed to pay costs and 5 % on $50,000,000", 10.7143, "var(--work)"),
    ]
    title = "Would a ship canal pay? Gillmore's figures, 1880"
    desc = ("Millions of tons a year at a toll of 28 cents a ton: about 1,758,000 tons to pay the canal's running costs; about 2,600,000 tons passed through the Florida Straits in the last fiscal year; "
            "about 10,714,300 tons to pay running costs and 5 per cent on a construction cost of about $50,000,000.")
    o = head(W, H, "rc", title, desc, "Millions of tons a year, at a toll of 28 cents a ton. The labels link to the passage.")
    sc = 520 / 11
    y = 80
    for label, v, col in rows:
        o.append(f'<a href="{T}company/3"><text x="16" y="{y + 19}" font-size="13" fill="var(--ink)" text-decoration="underline">{escape(label)}</text></a>')
        o.append(f'<rect x="330" y="{y}" width="{v * sc:.0f}" height="28" fill="{col}"/>')
        o.append(f'<text x="{336 + v * sc:.0f}" y="{y + 19}" font-size="13" fill="var(--ink)">{v:,.3g} million t</text>')
        y += 48
    o.append(f'<text x="16" y="{H - 34}" font-size="12" fill="var(--ink2)">Gillmore: “it is impossible to answer satisfactorily the question of the capacity of the enterprise to yield a moderate interest”.</text>')
    o.append(f'<text x="16" y="{H - 16}" font-size="12" fill="var(--ink2)">He thought a national canal need not pay; later reports measured every plan by its benefits and costs.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "ridge-heights.svg").write_text(heights(), encoding="utf-8")
(OUT / "ridge-costs.svg").write_text(costs(), encoding="utf-8")
print("ok")
