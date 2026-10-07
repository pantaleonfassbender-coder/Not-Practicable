"""Draws assets/viz/camp-men.svg for module 4 (Camp Roosevelt): the men at work on the canal, September 1935 to July 1936,
as reported, set against the numbers promised (sources and passages as in data/camp.json).
Run from the site root: python tools/viz-camp.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/camp/"
# (months after 1 Sept 1935, men, label, link, kind)
REPORTED = [(0.45, 100, "14 Sept 1935: first ground, 100 men", "start/2"),
            (0.6, 1750, "by 20 Sept: 1,750 at Camp Roosevelt", "start/2"),
            (1.0, 3000, "1 Oct: 3,000 employed", "start/3"),
            (7.5, 6000, "Apr.–June 1936: about 6,000", "work/1"),
            (10.2, 5000, "8 July 1936: about 5,000 left unemployed", "stop/4")]
PROMISED = [(4.6, 7000, "promised Sept 1935: 7,000 within four months", "start/4"),
            (9, 20000, "expected 1936: 20,000 at the peak", "work/3")]


def build():
    W, H = 900, 470
    x0, x1, y0, y1 = 70, 860, 280, 70
    sx = lambda m: x0 + (x1 - x0) * m / 11
    sy = lambda v: y0 - (y0 - y1) * v / 21000
    title = "Men on the canal, as reported and as promised"
    desc = ("Reported: " + "; ".join(l for _, _, l, _ in REPORTED) + ". Promised: " + "; ".join(l for _, _, l, _ in PROMISED) + ".")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="cm-t cm-d" font-family="var(--serif)">',
         f'<title id="cm-t">{escape(title)}</title><desc id="cm-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">September 1935 to July 1936. Filled dots: numbers reported at the time; open dots: numbers promised. The list below links to the passages.</text>']
    for v in (0, 5000, 10000, 15000, 20000):
        o.append(f'<line x1="{x0}" x2="{x1}" y1="{sy(v):.0f}" y2="{sy(v):.0f}" stroke="var(--line)"/><text x="{x0 - 6}" y="{sy(v) + 4:.0f}" font-size="11" text-anchor="end" fill="var(--ink2)">{v:,}</text>')
    for i, mname in enumerate(["Sept 1935", "Nov", "Jan 1936", "Mar", "May", "July"]):
        o.append(f'<text x="{sx(i * 2):.0f}" y="{y0 + 18}" font-size="11" text-anchor="middle" fill="var(--ink2)">{mname}</text>')
    pts = " ".join(f"{sx(m):.0f},{sy(v):.0f}" for m, v, _, _ in REPORTED)
    o.append(f'<polyline points="{pts}" fill="none" stroke="var(--work)" stroke-width="2"/>')
    allp = [(m, v, l, h, True) for m, v, l, h in REPORTED] + [(m, v, l, h, False) for m, v, l, h in PROMISED]
    allp.sort(key=lambda t: t[0])
    for k, (m, v, l, h, rep) in enumerate(allp, 1):
        if rep:
            o.append(f'<circle cx="{sx(m):.0f}" cy="{sy(v):.0f}" r="5" fill="var(--work)"/>')
        else:
            o.append(f'<circle cx="{sx(m):.0f}" cy="{sy(v):.0f}" r="6" fill="var(--panel)" stroke="var(--survey)" stroke-width="2"/>')
        dy = -10 if k % 2 else 18
        o.append(f'<text x="{sx(m):.0f}" y="{sy(v) + dy:.0f}" font-size="11.5" font-weight="bold" text-anchor="middle" fill="var(--ink)">{k}</text>')
        col, row = (k - 1) // 4, (k - 1) % 4
        o.append(f'<a href="{T}{h}"><text x="{16 + col * 440}" y="{y0 + 50 + row * 22}" font-size="12.5" fill="var(--ink)" text-decoration="underline">{k}. {escape(l)}</text></a>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "camp-men.svg").write_text(build(), encoding="utf-8")
print("ok")
