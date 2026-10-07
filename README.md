# Not Practicable

The canal across Florida, 1826–1990: a documentary apparatus in English, built from public-domain sources read against the page images. From the Army survey of 1829, which found a ship channel through the peninsula “not practicable”, to the ship canal begun near Ocala in 1935 with men from the relief rolls, the barge canal authorized for the war in 1942, the Rodman dam and the halt of 1971, and the act of 1990 that ended the project and left a greenway.

**Status:** printed: module 1 *The ridge* (1826–1909), module 2 *The water-lane* (1832–1914), module 3 *Work for the relief rolls* (1933–1937) and module 4 *Camp Roosevelt* (1935–1936), 73 passages, 38 plates, 6 graphics, 8 comparisons. Planned: 5 *The water under Florida* (1935–1939), 6 *A canal for the war* (1941–1945), 7 *Rodman* (1958–1971), 8 *Undoing the canal* (1971–1990). The source survey is in the project folder (`KONZEPT.md`, `quellen/`, not in this repository).

**Companion game (in preparation):** *Relief and Navigation*.

## Structure

Static site without a build step: `index.html`, `app.js` (hash routes; engine adapted from *The Shipping Point*), `style.css`, `legal.html`, `_headers`. Data in `data/` (`modules.json`, `timeline.json`, `compare.json`, `plates.json`, one file per module); the frame is written by `python tools/build-frame.py`, each module by `python tools/build-<module>.py`, its graphics by `python tools/viz-<module>.py`, the plates by `python tools/make-plates.py`.

Local: `python -m http.server` in the repository, then `http://localhost:8000/`.

## Licences

Code MIT; editorial texts CC BY 4.0; editions CC0 1.0. See [LICENSES.md](LICENSES.md).
