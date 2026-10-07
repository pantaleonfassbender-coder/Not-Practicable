"""Draws assets/viz/relief-votes.svg for module 3 (Work for the relief rolls): the bond election of 22 October 1935
in the six counties of the canal district, votes for and against, as Representative Sears gave them on 17 April 1936
(Documentary History of the Florida Canal, Senate Document 275, 74th Congress, p. 382; figures from the page image).
Run from the site root: python tools/viz-relief.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/relief/"
VOTES = [("Duval", 10039, 329), ("Marion", 2115, 46), ("Putnam", 1720, 100), ("Levy", 603, 31), ("Citrus", 485, 37), ("Clay", 473, 47)]


def build():
    W, H = 900, 400
    tf = sum(v[1] for v in VOTES)
    ta = sum(v[2] for v in VOTES)
    title = "Who voted for the land, 22 October 1935"
    desc = ("Votes for and against $1,500,000 in bonds for the canal's right-of-way, by county: "
            + "; ".join(f"{c} {f:,} for, {a} against" for c, f, a in VOTES)
            + f". In all {tf:,} for and {ta} against. Only freeholders, that is registered property owners who had paid the poll tax, could vote.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="rv-t rv-d" font-family="var(--serif)">',
         f'<title id="rv-t">{escape(title)}</title><desc id="rv-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<a href="{T}bonds/2"><text x="16" y="48" font-size="13" fill="var(--ink2)" text-decoration="underline">Votes on the right-of-way bonds, by county, as given in Congress in April 1936. Link to the passage.</text></a>']
    sc = 560 / 10500
    y = 72
    for c, f, a in VOTES:
        o.append(f'<text x="16" y="{y + 19}" font-size="13.5" fill="var(--ink)">{c}</text>')
        o.append(f'<rect x="100" y="{y}" width="{max(1, f * sc):.1f}" height="26" fill="var(--land)"/>'
                 f'<rect x="{100 + f * sc:.1f}" y="{y}" width="{max(2, a * sc):.1f}" height="26" fill="var(--work)"/>')
        o.append(f'<text x="{108 + (f + a) * sc:.0f}" y="{y + 18}" font-size="12.5" fill="var(--ink)">{f:,} for · {a} against</text>')
        y += 38
    o.append(f'<text x="16" y="{y + 18}" font-size="13" fill="var(--ink)">All six counties: {tf:,} for, {ta} against (the compilation says “27 to 1”; the figures give about {tf / ta:.0f} to 1).</text>')
    o.append(f'<rect x="16" y="{y + 34}" width="12" height="12" fill="var(--land)"/><text x="34" y="{y + 45}" font-size="12" fill="var(--ink)">for</text>'
             f'<rect x="80" y="{y + 34}" width="12" height="12" fill="var(--work)"/><text x="98" y="{y + 45}" font-size="12" fill="var(--ink)">against</text>'
             f'<text x="170" y="{y + 45}" font-size="12" fill="var(--ink2)">Not shown, because not counted anywhere: those who could not vote for want of property or of a paid poll tax.</text>')
    o.append("</svg>")
    return "\n".join(o)


def land():
    W, H = 900, 250
    parts = [("Bought on options", 12003, "var(--land)"), ("In condemnation", 9630, "var(--work)"),
             ("Condemnation requested", 6196, "var(--survey)"), ("Other land still required", 53663, "var(--line)")]
    tot = sum(p[1] for p in parts)
    title = "The right-of-way, June 1936"
    desc = ("81,492 acres required for the western part of the route: " + "; ".join(f"{l} {v:,} acres" for l, v, _ in parts)
            + ". In possession: 21,633 acres, 26.6 per cent.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="rl-t rl-d" font-family="var(--serif)">',
         f'<title id="rl-t">{escape(title)}</title><desc id="rl-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<a href="{T}land/3"><text x="16" y="48" font-size="13" fill="var(--ink2)" text-decoration="underline">81,492 acres on the Army engineers’ map of the route west of Ocala, eight months after the bond vote. Link to the passage.</text></a>']
    x, sc = 16, 868 / tot
    for l, v, c in parts:
        o.append(f'<rect x="{x:.1f}" y="70" width="{v * sc:.1f}" height="44" fill="{c}" stroke="var(--panel)"/>')
        x += v * sc
    y, x = 140, 16
    for l, v, c in parts:
        o.append(f'<rect x="{x}" y="{y}" width="12" height="12" fill="{c}"/><text x="{x + 18}" y="{y + 11}" font-size="12.5" fill="var(--ink)">{escape(l)}: {v:,} acres ({v / tot * 100:.1f} %)</text>')
        y += 22
    o.append(f'<text x="470" y="151" font-size="12.5" fill="var(--ink2)">In possession (options and condemnation): 21,633 acres.</text>')
    o.append(f'<text x="470" y="173" font-size="12.5" fill="var(--ink2)">Owners and their names: not on the map.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "relief-land.svg").write_text(land(), encoding="utf-8")
(OUT / "relief-votes.svg").write_text(build(), encoding="utf-8")
print("ok")
