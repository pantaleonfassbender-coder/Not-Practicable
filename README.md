# Not Practicable

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23226295.svg)](https://doi.org/10.5281/zenodo.23226295)

The canal across Florida, 1826–1990: a documentary apparatus in English, built from public-domain sources read against the page images. From the Army survey of 1829, which found a ship channel through the peninsula “not practicable”, to the ship canal begun near Ocala in 1935 with men from the relief rolls, the barge canal authorized for the war in 1942, the Rodman dam and the halt of 1971, and the act of 1990 that ended the project and left a greenway.

It asks who paid, who worked, who was asked, and what was lost: the counties that taxed themselves for thirty-five years after a bond vote open only to property owners who had paid the poll tax; the several thousand men from the relief rolls at Camp Roosevelt, one of whom, John Matthews, is named in the record only in the report of his death; the owners whose land was condemned and never returned; the Ocklawaha valley under the Rodman pool.

Live: https://not-practicable.netlify.app/

**Stage 1 is closed (October 2026).** It carries eight modules with 132 passages:

- **1 The ridge, 1826–1909** — the Senate committee and Florida's delegate Joseph M. White (1826); Bernard and Poussin's “not practicable” (1829); Pickell's water for the summit (1832); a railroad instead (1855); Gillmore's fifty million dollars (1880); the canal company that went “up in a soap bubble” (1883–84); five routes (1909).
- **2 The water-lane, 1832–1914** — Sidney Lanier on the Ocklawaha (1875): the raftsman, the pole-men Dick and Henry, the vanilla-gatherers, Payne's Landing as he told it; Colonel Hart's canal charter; the London prospectus of 1877; the engineers' Oklawaha report of 1914 (logs, railroad rates, a private cut-off).
- **3 Work for the relief rolls, 1933–1937** — the Ship Canal Authority and the memorial of 1933; the refused loan and Roosevelt's relief allotment (1935); the bond election open only to freeholders; the appraiser's “$8 to $10 an acre”; the right-of-way map of June 1936.
- **4 Camp Roosevelt, 1935–1936** — job hunters in Ocala, the first ground, the button at Hyde Park; the State Board of Health on the camps and its count by colour; ten miles of cut; the Chief of Engineers' “that Negro” at the Ocala rock; the mule auction; the death of John Matthews; 5,000 men out of work after the stop.
- **5 The water under Florida, 1934–1939** — the ground-water dispute; south Florida against the canal; the Senate votes of 1936 (34 to 39) and 1939 (36 to 45); the mock funeral at Silver Springs; the Board of Engineers against its Chief, who recommended the canal “as a combination of unemployment relief and of navigation improvement”.
- **6 A canal for the war, 1941–1945** — German submarines and oil; the House debate of 1 June 1942 (“boondoggling bill”, 85 to 121); the act of 23 July 1942; the engineers' report kept secret until 1945; no money.
- **7 Rodman, 1909–1974** — the revival; Johnson's ground-breaking at Palatka (1964); the western end at Inglis and Lake Rousseau (the dam of 1909, the reach finished in 1969, the Geological Survey's measurements); the Rodman pool and its 13,000 acres; the suit of 1969 and Nixon's halt of 19 January 1971.
- **8 Undoing the canal, 1971–1990** — thirty-five years of county canal tax; the Corps restudy of 1976 and Carter's “ill-advised project”; the Palatka hearing of 1985 (Governor Graham, Marjorie Carr, 204 to 201); the owners who could not get their land back; Public Law 101-640, the greenway and $32 million for the six counties.

With 80 public-domain plates (maps, congressional and court pages, newspaper cuttings, photographs of the works of 1935–36, the Rodman quadrangle of 1949 and 1993), 10 graphics, 17 comparisons setting the sources side by side, and a timeline of 42 stations linked into the texts.

What is **not carried**, and why, is listed on the Texts page (`data/modules.json`, key `missing`, 25 entries): among them segregation at the camps and wages (not documented in the sources read), the families on the route, the Ocala newspapers of 1935–36, the engineers' reports of 1935 and 1942, the opponents' report of 1970, and Marjorie Carr's oral history of 1989 (not in the public domain).

**Companion game:** [*Relief and Navigation*](https://leofassb.itch.io/relief-and-navigation), in two roles (the canal authority, 1933–1990; the river's defenders, 1962–1990), sold on itch.io. This apparatus stays free.

## Files

- `data/modules.json`: the modules carried, and what is not carried and why.
- `data/<module>.json`: the texts (`ridge`, `river`, `relief`, `camp`, `aquifer`, `war`, `rodman`, `undoing`).
- `data/timeline.json`, `data/compare.json`, `data/plates.json`.
- `tools/build-frame.py` (once, before the first module), `tools/build-<module>.py`, `tools/viz-<module>.py`, `tools/make-plates.py`. The plate script reads page images and PDFs from the project's source folder (`../quellen`, not in this repository), where the check logs (`PRUEFUNG.md`) record for each passage the page image it was read against.

Static site without a build step: `index.html`, `app.js` (hash routes; engine adapted from *The Shipping Point*), `style.css`, `legal.html`, `_headers`. Local: `python -m http.server` in the repository, then `http://localhost:8000/`.

## Citation

Fassbender, Pantaleon. *Not Practicable: The Canal across Florida, 1826–1990. A Documentary Apparatus.* 2026. https://doi.org/10.5281/zenodo.23226295 (all versions; version 1.0.0: https://doi.org/10.5281/zenodo.23226296). Please also cite the printed source of any passage you quote. Metadata: `CITATION.cff`, `.zenodo.json`.

## Licences

Code MIT; editorial texts CC BY 4.0; editions CC0 1.0; plates public domain. See [LICENSES.md](LICENSES.md).
