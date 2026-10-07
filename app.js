/* Not Practicable. The canal across Florida, 1826–1990. A documentary apparatus in English,
   built on the engine of "The Shipping Point" (after "One Bridge, Two Newsreels"). Vanilla JS, hash routes. */
"use strict";

const view = document.getElementById("view");
const D = { mods: null, plates: null, timeline: null, compare: null, texts: {} };

const S = {
  title: "Not Practicable", loading: "Loading…", allTexts: "← All texts", allCmp: "← All comparisons",
  citeAs: "cited as", cite: "Cite as", srcNote: "Source and editorial note", source: "Source",
  planned: "planned", notTaken: "not included", shipped: "Printed here", plannedH: "Planned",
  missingH: "Examined and not included", textsTag: "Texts", textsH: "The corpus",
  textsLede: "Every module can be read in full, in the words of its public-domain sources, each passage read against the page image. What was examined and not included is listed below, with the reason.",
  cmpTag: "Compare", cmpH: "Voices side by side", tlTag: "Timeline", tlH: "From the survey of 1826 to the greenway",
  platesTag: "Plates", platesH: "Maps, photographs, views", fail: "The apparatus could not be loaded: "
};
const SIDES = {
  survey: "Surveys and plans", river: "The river", work: "Work and camps", water: "Water under the ground", capitol: "Washington", land: "Land and counties"
};

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const side = s => `<span class="side ${s}">${esc(SIDES[s] || s)}</span>`;
const plateOf = id => (D.plates.plates || []).find(p => p.id === id);
const getJSON = url => fetch(url).then(r => { if (!r.ok) throw new Error(url); return r.json(); });

async function boot() {
  [D.mods, D.plates, D.timeline, D.compare] = await Promise.all(
    ["data/modules.json", "data/plates.json", "data/timeline.json", "data/compare.json"].map(getJSON));
  document.getElementById("navCompare").hidden = !(D.compare.pairs || []).length;
  document.getElementById("navPlates").hidden = !(D.plates.plates || []).length;
  window.addEventListener("hashchange", route);
  route();
}

async function text(id) {
  if (!D.texts[id]) D.texts[id] = await getJSON(`data/${id}.json`);
  return D.texts[id];
}

function route() {
  const parts = (location.hash.replace(/^#\/?/, "") || "").split("/").filter(Boolean);
  const [page, ...args] = parts;
  document.querySelectorAll(".top nav a").forEach(a => {
    const t = a.getAttribute("href").replace(/^#\/?/, "");
    a.classList.toggle("on", (t || "") === (page === "text" ? "texts" : page || ""));
  });
  view.innerHTML = "";
  window.scrollTo(0, 0);
  const pages = { "": overview, texts, text: reader, compare, timeline, plates, sources };
  (pages[page || ""] || overview)(args);
}

/* ------------------------------------------------------------ overview */
const OVERVIEW = {
  tag: "Florida · Palatka · Ocala · Dunnellon · Inglis · 1826–1990",
  h: "Not Practicable",
  lede: "In 1829 two Army engineers reported that a ship channel through the peninsula of Florida “is not practicable”: the ridge between the oceans stood a hundred and fifty feet above the sea. For the next hundred and sixty years the canal was argued for again and again, each time for a new reason — for shipping, for the unemployed, for the war, for growth — and begun twice, near Ocala in 1935 and at Palatka in 1964. Twice it was stopped. In 1990 Congress provided for its end, and the land along the route became a greenway.",
  body: "This apparatus follows the canal through its own public-domain record: the surveys of the Army engineers, the debates and votes of Congress, the statements of presidents, the documents of the Ship Canal Authority in Ocala, the reports of Florida's agencies, the hearings at which supporters and opponents spoke, and the newspapers of the towns on the route. It asks who paid, who worked, who was asked, and what was lost under the water of the Rodman pool. Where the sources are silent, it says so.",
  q: [
    ["Why was a canal across Florida wanted?", "To spare shipping the passage round the Keys and the Florida Straits, the case from 1826 on; to put men from the relief rolls to work in 1935; to keep barges safe from submarines in 1942; and in 1964 to bring trade and growth to the counties on the route."],
    ["Why was it stopped?", "In 1936 the Senate refused further money, after warnings that a sea-level cut could harm the underground water of central Florida. In 1971 the President halted the barge canal “to prevent potentially serious environmental damages”, with about $50 million of $180 million committed."],
    ["Who paid, who worked, who was asked?", "The six counties of the canal district voted bonds and paid a canal tax for decades. Several thousand men, most of them from the relief rolls, dug the cut south of Ocala in 1935–36. Only property owners could vote on the bonds; the people living on the right of way appear in the record through the words of a land appraiser."],
    ["Can one retrace it?", "Relief and Navigation, a companion game in preparation, will let you take the place of the canal authority's secretary at Ocala between 1933 and 1990. Every card will point to its passage here."]
  ],
  none: "The modules are in preparation; the Texts page lists them with their sources.",
  have: "What the apparatus contains", qs: "The questions"
};

function overview() {
  const O = OVERVIEW;
  view.innerHTML = `
  <div class="hero one"><div>
    <span class="tag">${esc(O.tag)}</span>
    <h1>${esc(O.h)}</h1>
    <p class="lede">${esc(O.lede)}</p>
    <p class="readable">${esc(O.body)}</p>
  </div></div>
  <h2>${esc(O.have)}</h2>
  ${D.mods.shipped.length ? "" : `<p class="fine">${esc(O.none)}</p>`}
  <div class="grid g2">${D.mods.shipped.map(m => card(m)).join("")}${(D.mods.planned || []).map(m => card(m, true)).join("")}</div>
  <h2>${esc(O.qs)}</h2>
  <div class="grid g2">${O.q.map(([h, p]) => `<div class="panel"><h3>${esc(h)}</h3><p>${esc(p)}</p></div>`).join("")}</div>`;
}

function card(m, planned) {
  const inner = `<div>${side(m.side)} <span class="fine">${esc(planned ? S.planned : m.zk || "")}</span></div>
    <h3>${esc(m.kurz)}</h3><p class="fine">${esc(m.warum)}</p>`;
  return planned ? `<div class="card planned">${inner}</div>` : `<a class="card" href="#/text/${m.id}">${inner}</a>`;
}

/* ------------------------------------------------------------ texts */
function texts() {
  const other = (list, label) => list.map(m => `
      <div class="card planned"><div>${side(m.side)} <span class="fine">${esc(label)}</span></div>
      <h3>${esc(m.kurz)}</h3><p class="fine">${esc(m.warum)}</p><p class="fine"><b>${esc(S.source)}:</b> ${esc(m.quelle)}</p></div>`).join("");
  view.innerHTML = `
    <span class="tag">${esc(S.textsTag)}</span><h1>${esc(S.textsH)}</h1>
    <p class="lede">${esc(S.textsLede)}</p>
    ${D.mods.shipped.length ? `<h2>${esc(S.shipped)}</h2><div class="grid g2">${D.mods.shipped.map(m => card(m)).join("")}</div>` : ""}
    ${(D.mods.planned || []).length ? `<h2>${esc(S.plannedH)}</h2><div class="grid g2">${other(D.mods.planned, S.planned)}</div>` : ""}
    ${(D.mods.missing || []).length ? `<h2 id="missing">${esc(S.missingH)}</h2><div class="grid g2">${other(D.mods.missing, S.notTaken)}</div>` : ""}`;
}

async function reader([id, secId, unitN]) {
  const m = D.mods.shipped.find(x => x.id === id);
  if (!m) { location.hash = "#/texts"; return; }
  view.innerHTML = `<p class="fine">${esc(S.loading)}</p>`;
  const t = await text(m.datei);
  const sec = t.sections.find(s => s.id === secId) || t.sections[0];
  view.innerHTML = `
    <p class="fine"><a href="#/texts">${esc(S.allTexts)}</a></p>
    <span class="tag">${side(m.side)} ${esc(t.jahr)} · ${esc(S.citeAs)} ${esc(sec.zk)} [n]</span>
    <h1>${esc(t.titel)}</h1>
    <p class="fine">${esc(t.autor)}</p>
    <nav class="toc">${t.sections.map(s => `<a href="#/text/${id}/${s.id}" class="${s.id === sec.id ? "on" : ""}">${esc(s.titel)}</a>`).join("")}</nav>
    <div class="panel readable"><h3>${esc(sec.titel)}</h3><p>${esc(sec.blurb)}</p>${sec.note ? `<p class="fine">${esc(sec.note)}</p>` : ""}</div>
    ${(sec.plates || []).length ? `<div class="grid g4 secplates">${sec.plates.map(plateOf).filter(Boolean).map(plateFig).join("")}</div>` : ""}
    ${sec.viz ? `<div class="viz" id="viz"><p class="fine">${esc(S.loading)}</p></div>` : ""}
    <div id="units"></div>
    <div class="panel readable hinweis"><span class="tag">${esc(S.srcNote)}</span>
      <p><b>${esc(S.source)}.</b> ${esc(t.quelle)}</p><p>${esc(t.hinweis)}</p></div>`;
  bindPlates(view);
  if (sec.viz) fetch(`assets/viz/${sec.viz}.svg`).then(r => r.ok ? r.text() : "").then(svg => {
    const el = document.getElementById("viz");
    if (el) el.innerHTML = svg || "";
  });
  const box = view.querySelector("#units");
  for (const u of sec.units) {
    box.insertAdjacentHTML("beforeend", `
      <div class="unit ${String(u.n) === unitN ? "hl" : ""}" id="u${u.n}">
        <div class="num"><a href="#/text/${id}/${sec.id}/${u.n}" title="${esc(S.cite)} ${esc(sec.zk)} [${u.n}]">[${u.n}]</a>
          ${u.pg ? `<span class="pg">${esc(u.pg)}</span>` : ""}</div>
        <div>${u.titel ? `<h4>${esc(u.titel)}</h4>` : ""}<div class="cols one"><div class="text">${esc(u.orig)}</div></div></div>
        ${u.note ? `<div class="note">${esc(u.note)}</div>` : ""}
      </div>`);
  }
  if (unitN) { const el = document.getElementById("u" + unitN); if (el) el.scrollIntoView({ block: "center" }); }
}

/* ------------------------------------------------------------ compare */
async function compare([pid]) {
  const CMP = D.compare;
  const pair = (CMP.pairs || []).find(p => p.id === pid);
  if (!pair) {
    view.innerHTML = `
      <span class="tag">${esc(S.cmpTag)}</span><h1>${esc(S.cmpH)}</h1>
      <p class="lede">${esc(CMP.lede)}</p>
      <div class="grid g2">${(CMP.pairs || []).map(p => `<a class="card" href="#/compare/${p.id}">
        <h3>${esc(p.titel)}</h3><p class="fine">${esc(p.frage)}</p></a>`).join("")}</div>`;
    return;
  }
  view.innerHTML = `<p class="fine"><a href="#/compare">${esc(S.allCmp)}</a></p><p class="fine">${esc(S.loading)}</p>`;
  const docs = await Promise.all(pair.voices.map(v => {
    const m = D.mods.shipped.find(x => x.id === v.text);
    return text(m.datei).then(t => ({ v, m, t }));
  }));
  const col = ({ v, m, t }) => {
    const sec = t.sections.find(s => s.id === v.sec);
    const units = v.n.map(n => sec.units.find(u => u.n === n)).filter(Boolean);
    return `<div class="voice">
      <div class="vhead">${side(m.side)} <b>${esc(v.wer || t.autor)}</b><br><span class="fine">${esc(t.jahr)} · ${esc(sec.titel)}</span></div>
      ${units.map(u => `<div class="vunit"><div class="fine"><a href="#/text/${m.id}/${sec.id}/${u.n}">${esc(sec.zk)} [${u.n}]</a>${u.titel ? ` · ${esc(u.titel)}` : ""}</div>
        <div class="text">${esc(u.orig)}</div></div>`).join("")}
    </div>`;
  };
  view.innerHTML = `
    <p class="fine"><a href="#/compare">${esc(S.allCmp)}</a></p>
    <span class="tag">${esc(S.cmpTag)}</span><h1>${esc(pair.titel)}</h1>
    <p class="lede">${esc(pair.frage)}</p>
    <div class="panel readable"><p>${esc(pair.note)}</p></div>
    <div class="cmp n${docs.length}">${docs.map(col).join("")}</div>`;
}

/* ------------------------------------------------------------ timeline */
function timeline() {
  const TL = D.timeline;
  view.innerHTML = `
    <span class="tag">${esc(S.tlTag)}</span><h1>${esc(S.tlH)}</h1>
    <p class="lede">${esc(TL.lede)}</p>
    <div class="legend">${Object.keys(SIDES).map(side).join(" ")}</div>
    <div class="tl">${TL.stations.map(s => {
      const p = s.plate && plateOf(s.plate);
      return `<div class="st" style="--c:var(--${s.side})">
        <div><div class="d">${esc(s.d)} · ${side(s.side)}</div><h3>${esc(s.titel)}</h3><p>${esc(s.text)}</p>
        ${s.cite ? `<p class="fine"><a href="${s.cite}">✦ ${esc(s.citeLabel)}</a></p>` : ""}
        ${s.quelle ? `<p class="fine">${esc(s.quelle)}</p>` : ""}</div>
        ${p ? `<img src="assets/plates/${p.id}_t.jpg" alt="${esc(p.titel)}" title="${esc(p.titel)}">` : "<span></span>"}
      </div>`;
    }).join("")}</div>`;
}

/* ------------------------------------------------------------ plates */
function plates() {
  view.innerHTML = `
    <span class="tag">${esc(S.platesTag)}</span><h1>${esc(S.platesH)}</h1>
    <p class="lede">${esc(D.plates.lede)}</p>
    <div class="grid g4">${D.plates.plates.map(plateFig).join("")}</div>
    <p class="fine">${esc(D.plates.credit)}</p>`;
  bindPlates(view);
}
function plateFig(p) {
  return `<figure class="plate card"><a href="#" data-p="${p.id}"><img src="assets/plates/${p.id}_t.jpg" alt="${esc(p.titel)}"></a>
      <figcaption>${side(p.side)} <b>${esc(p.titel)}</b><br>${esc(p.caption)}<br><i>${esc(p.source)}</i></figcaption></figure>`;
}
function bindPlates(root) {
  root.querySelectorAll("[data-p]").forEach(a => a.onclick = e => {
    e.preventDefault();
    const p = plateOf(a.dataset.p);
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.innerHTML = `<figure><img src="assets/plates/${p.id}.jpg" alt="${esc(p.titel)}"><figcaption class="cap"><b>${esc(p.titel)}.</b> ${esc(p.caption)}</figcaption></figure>`;
    lb.onclick = () => lb.remove();
    document.body.append(lb);
  });
}

/* ------------------------------------------------------------ sources */
const METHOD = {
  tag: "Sources, method, limits", h: "How this apparatus is made",
  p: [
    ["Public domain only.", "Almost every text here is a work of the United States government: reports of the Army engineers and the Geological Survey, the Congressional Record and congressional documents and hearings, statutes, the public papers of the presidents, and decisions of federal courts. Florida's own agency publications are added where they carry no claim of copyright, newspapers only up to 1930 or where their rights are stated. The Ship Canal Authority's own compilation of 1936 was printed as a Senate document without a copyright notice. Each passage is read against the page image. Recent research is named and summarized as such, never printed."],
    ["Advocates and opponents.", "Many of the documents were written to win a vote. The apparatus says whose words a passage carries — the canal authority's, the engineers', a senator's, a witness's — and sets the figures of each side next to each other."],
    ["Whose voices.", "The men who dug at Camp Roosevelt, the families whose land lay in the way, and the Black residents of the route speak in these sources only through officials, reporters and an appraiser. Where a voice is missing, the apparatus says so and does not invent it."],
    ["Numbers.", "Costs, benefits, tonnages and acreages changed with every report and every rate of interest. They stand with their date and their author, never as a single truth."],
    ["Boundaries.", "The canal from the St. Johns to the Gulf and the country along its route, from the survey of 1826 to the act of 1990. The greenway since then, and the dispute over the dam at Rodman, are outlook, not subject."]
  ],
  printed: "Sources printed here", plates: "Plates"
};

function sources() {
  const M = METHOD;
  view.innerHTML = `
    <span class="tag">${esc(M.tag)}</span><h1>${esc(M.h)}</h1>
    <div class="readable">${M.p.map(([b, p]) => `<p><b>${esc(b)}</b> ${esc(p)}</p>`).join("")}</div>
    ${D.mods.shipped.length ? `<h2>${esc(M.printed)}</h2>
    <div class="grid g2">${D.mods.shipped.map(m => `<div class="panel"><b>${esc(m.kurz)}</b><p class="fine" id="src-${m.id}">…</p></div>`).join("")}</div>` : ""}
    ${(D.plates.plates || []).length ? `<h2>${esc(M.plates)}</h2><p class="fine readable">${esc(D.plates.credit)}</p>` : ""}`;
  D.mods.shipped.forEach(async m => {
    const t = await text(m.datei);
    const el = document.getElementById("src-" + m.id);
    if (el) el.textContent = t.quelle;
  });
}

boot().catch(e => { view.innerHTML = `<p>${esc(S.fail)}${esc(e.message)}</p>`; });
