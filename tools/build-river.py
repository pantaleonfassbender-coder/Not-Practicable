"""Builds data/river.json (module 2: The water-lane, 1875–1914) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/river/PRUEFUNG.md):
  Sidney Lanier, Florida: Its Scenery, Climate, and History (Philadelphia 1875/76), pp. 18, 20, 29–30, 32, 101, 202
    (Internet Archive floridaitsscene00lanigoog, leaves n23, n25, n34–n35, n37, n106, n207);
  The Atlantic & Gulf Ship Canal across the Peninsula of Florida (London 1877), title page, pp. 30–31
    (IA cu31924022881555, leaves n6, n37–n38);
  House Document 514, 63rd Congress, 2nd Session (1914), Oklawaha River, Fla., pp. 2, 7–8, 10
    (IA oklawahariverfla00unit, leaves n1, n6–n7, n9).
Plates from Wikimedia Commons (Library of Congress, New York Public Library, Metropolitan Museum of Art,
State Archives of Florida), all public domain or CC0.
Run from the site root: python tools/build-river.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"


def u(n, pg, orig, titel=None, note=None):
    x = {"n": n, "pg": pg}
    if titel:
        x["titel"] = titel
    x["orig"] = orig
    if note:
        x["note"] = note
    return x


LAN = "Sidney Lanier, Florida (1875/76)"
HD514 = "House Document 514, 63rd Congress, 2nd Session (1914)"

LANIER = [
    u(1, LAN + ", p. 18",
      "For a perfect journey God gave us a perfect day. The little Ocklawaha steamboat Marion—a steamboat which is like nothing in the world so much as a Pensacola gopher with a preposterously exaggerated back—had started from Pilatka some hours before daylight, having taken on her passengers the night previous; and by seven o'clock of such a May morning as no words could describe unless words were themselves May mornings we had made the twenty-five miles up the St. Johns, to where the Ocklawaha flows into that stream nearly opposite Welaka, one hundred miles above Jacksonville. Just before entering the mouth of the river our little gopher-boat scrambled alongside a long raft of pine-logs which had been brought in separate sections down the Ocklawaha and took off the lumbermen, to carry them back for another descent while this raft was being towed by a tug to Jacksonville.",
      "The Marion",
      "Lanier, a poet from Georgia, wrote the book as a guide for visitors; the journey up the Ocklawaha is its second chapter. The first thing he meets on the river is work: a raft of pine logs and the men who rode it down."),
    u(2, LAN + ", p. 20",
      "“Waal, sir,” he says, with a dilute smile, as he wearily leans his arm against the low deck where I am sitting, “ef we did'n' have ther sentermentillest rain right thar last night, I'll be dad-busted!” He had been in it all night.",
      "A lumberman",
      "Before this, Lanier spends a page mocking the raftsman's looks, and then withdraws his remarks: “He has a right to look disheveled.” His is the only voice of a worker on the river in this module, and it comes to us in the spelling of the visitor who heard it."),
    u(3, LAN + ", p. 20",
      "Presently we rounded the raft, abandoned the broad and garish highway of the St. Johns, and turned off to the right into the narrow lane of the Ocklawaha, the sweetest water-lane in the world, a lane which runs for more than a hundred and fifty miles of pure delight betwixt hedgerows of oaks and cypresses and palms and bays and magnolias and mosses and manifold vine-growths, a lane clean to travel along for there is never a speck of dust in it save the blue dust and gold dust which the wind blows out of the flags and lilies, a lane which is as if a typical woods-stroll had taken shape and as if God had turned into water and trees the recollection of some meditative ramble through the lonely seclusions of His own soul. As we advanced up the stream our wee craft even seemed to emit her steam in more leisurely whiffs, as one puffs one's cigar in a contemplative walk through the forest. Dick, the pole-man—a man of marvelous fine functions when we shall presently come to the short, narrow curves—lay asleep on the guards, in great peril of rolling into the river over the three inches between his length and the edge; the people of the boat moved not, and spoke not; the white crane, the curlew, the limpkin, the heron, the water-turkey, were scarcely disturbed in their quiet avocations as we passed.",
      "“The sweetest water-lane in the world”",
      "The sentence that made the river famous, and the river the canal of the 1960s would partly drown (module 7). Its opponents quoted it; this apparatus takes its name for the module from it."),
    u(4, LAN + ", p. 29",
      "—And then, after this day of glory, came a night of glory. Down in these deep-shaded lanes it was dark indeed as the night drew on. The stream which had been all day a baldrick of beauty, sometimes blue and sometimes green, now became a black band of mystery. But presently a brilliant flame flares out overhead: they have lighted the pine-knots on top of the pilot-house. … Now there is a mighty crack and crash: limbs and leaves scrape and scrub along the deck; a little bell tinkles; we stop. In turning a short curve, or rather doubling, the boat has run her nose smack into the right bank, and a projecting stump has thrust itself sheer through the starboard side. Out, Dick! out, Henry! Dick and Henry shuffle forward to the bow, thrust forth their long white pole against a tree-trunk, strain and push and bend to the deck as if they were salaaming the god of night and adversity, our bow slowly rounds into the stream, the wheel turns, and we puff quietly along.",
      "Out, Dick! out, Henry!",
      "The work that kept the boat moving: the pine-knot fire on the pilot-house, and two pole-men who push the bow off the bank when the boat runs into it. Lanier names them only by their first names."),
    u(5, LAN + ", p. 30",
      "You should hear him! With the great aperture of his mouth, and the rounding vibratory-surfaces of his thick lips, he gets out a mellow breadth of tone that almost entitles him to rank as an orchestral instrument. … It is a genuine plagal cadence. Observe the syncopations marked in this air: they are characteristic of negro music.",
      "Dick's tune",
      "Dick was Black. Lanier, a musician, writes down the two tunes Dick whistles in the stern (the print gives them in notes) and admires his music in the racial language of 1875, describing his body as an instrument; Dick himself says nothing in the book. Whether he and Henry were paid hands, and what they earned, the book does not say."),
    u(6, LAN + ", p. 32",
      "You must know that in the low grounds of the Ocklawaha grows what is called the vanilla-plant—a plant with a leaf much like that of tobacco when dried. This leaf is now extensively used to adulterate cheap chewing-tobacco, and the natives along the Ocklawaha drive a considerable trade in gathering it. The process of this commerce is exceedingly simple: and the bills drawn against the consignments are primitive. The officer in charge of the Marion showed me several of the communications received at various landings during our journey, which accompanied small shipments of the spurious weed. They were generally about as follows: “Deer Sir “i send you one bag Verneller, pleeze fetch one par of shus numb 8 and ef enny over fetch twelve yards hoamspin. “Yrs trly “&c.”",
      "Vanilla-gatherers",
      "The boat as the river's shop: the people along the banks pay for shoes and homespun in leaves gathered in the swamp, and the steamer's officer settles the account. The note Lanier copies is the only writing of a river dweller in this module; he prints it for its spelling."),
]

PAYNE = [
    u(1, LAN + ", p. 202",
      "In the course of many “talks,” a proposition was made to the Indians by the United States Government, offering them strong inducements to remove to the West; and finally a treaty was made at Payne's Landing on the Ocklawaha River in 1832 by which many of the chiefs agreed that if the proposed Western country should be acceptable to a delegation which they should appoint to examine it, and if the Creeks would reunite with them, they would remove. … But meantime the party which had originally opposed removal had grown stronger. It included Osceola, who was exceedingly violent in his denunciation of the project; and the negroes (of whom it is said there were a thousand living with the Indians, some of them being very prominent persons in the councils of the savages) were also hostile to the movement.",
      "A treaty on the river",
      "Lanier's history chapter, written forty years after the events, from the side of the government and the army: “strong inducements” is his word for the pressure to leave, “savages” his word for the Seminole. What followed, the war that began in 1835, with its violence on all sides, and the removal of Seminole people to the West, Lanier tells in his next pages from the same side; it is not printed here. The treaty itself and the records of the war are named among the sources not yet read."),
]

ROUTES = [
    u(1, LAN + ", p. 101",
      "One of the largest saw-mills in Florida is situated at the mouth of the Withlacoochee, and is supplied with material from the timber floated down that stream. There is an inside passage from Cedar Keys to this point: and one of the most important projects, it would seem, that has been mooted in Florida, is one to connect the Withlacoochee River with the Ocklawaha by a canal, for which a charter has been already obtained by Colonel Hart, of Pilatka. An astonishingly small amount of labor would accomplish this end, and would thus render practicable a clear water-way across the entire peninsula of Florida from the Gulf to the Atlantic. Lake Panasofka, which has the Withlacoochee for its outlet into the Gulf, is but about thirteen miles from Lake Harris, whose outlet is the Ocklawaha, flowing into the St. Johns. Thus this new water-way would be: from the Gulf of Mexico, up the Withlacoochee, via Lakes Panasofka, Okohumpka, and Harris, into the Ocklawaha, thence into the St. Johns, to the Atlantic Ocean.",
      "Colonel Hart's charter",
      "The idea of 1829, dismissed for want of water (module 1), comes back from the river itself. Hart's Daily Line, under H. L. Hart, ran the Ocklawaha steamers from Palatka (plate); Lanier names a Colonel Hart of Palatka as holder of the charter. The route joins the same two rivers as the barge canal of 1942 and 1964, by a line farther south."),
    u(2, "The Atlantic & Gulf Ship Canal across the Peninsula of Florida (London 1877), title page",
      "Privately Printed. Only 20 Copies. The Atlantic & Gulf Ship Canal across the Peninsula of Florida, connecting the Atlantic Ocean with the Gulf of Mexico and Caribbean Sea. Also, the Great Tide-Water Canal Route, from the Port of Fernandina, through the Peninsula to the Port of Key West, and Cuba, their Commercial and Financial Character, and Properties. London. 1877.",
      "A prospectus for twenty readers"),
    u(3, "The Atlantic & Gulf Ship Canal (1877), p. 31",
      "The Ship Canal commences in the harbours of Fernandina and Nassau Inlet, in the Atlantic; thence by way of the inside tide waters and connecting Canal into the St. John's River; thence by way of the St. John's and Doctor's Lake; thence overland into the Suannee River (at tide water); thence by way of the Suannee River into the Gulf of Mexico. Length of this route 165 miles. … Under the Charter Act of 1874 the Company has the right to go up the St. John's, and thence cross by the Ocklawaha River, Lake Orange, and overland to the River and Bay of Wacassasse into the Gulf, or by way of Silver Springs and the Withlacoochee River into the Gulf. … Neither the land or water section presents a single engineering difficulty. There are no mountains, or hills, or swamps, hard rocks, or quicksands to encounter on the whole line; geography describes the surface of the State as being generally “low and level.”",
      "“Not a single engineering difficulty”",
      "Written in London to raise money for a company with a Florida charter of 1874. Its claim that the line has no hills answers, without naming it, the engineers of 1829, who had found the ridge 150 feet high."),
    u(4, "The Atlantic & Gulf Ship Canal (1877), p. 30",
      "Amount of net tons of merchandise now ready to pass through the Ship Canal. 1. Present Commerce of the Gulf, &c. … 10,000,000. 2. Exports from the Mississippi Valley and the Gulf States … 15,000,000. 3. Imports into the Mississippi Valley and the Gulf States (large) … 4. Freights viâ the Three Trans-Continental Railways and the Darien Ship Canal (large) … 5. Exports, Imports, and Internal Trade of the State of Florida 2,000,000. Total (now) … 27,000,000.",
      "Twenty-seven million tons",
      "The prospectus counts ten times the traffic the Army's engineers found passing the Florida Straits three years later (2,600,000 tons; module 1). The table is set here as running text."),
]

TRADE = [
    u(1, HD514 + ", p. 7: Major J. R. Slattery, Jacksonville, 29 December 1911, quoting the report of Mr. Sackett",
      "In 1860 a line of steamers was established between Jacksonville and Leesburg on Lake Griffin and into Lakes Eustis and Harris (then called Lake Astatula), and during high stages of the water these steamers are said to have gone to Okahumka. This line of steamers is said to have done a flourishing business and was the means of rapidly developing the agricultural resources of the region thus made accessible. In 1874 a competing line of steamers was put on the same run, and both are said to have done a good business until 1883, when an unusually low stage of the water occurred, which seriously interfered with the traffic. About this time a railroad was built from Astor, on the St. Johns River, to Fort Mason, on Lake Eustis, a distance of about 25 miles.",
      "Steamers, 1860–1883"),
    u(2, HD514 + ", pp. 7–8",
      "In the meanwhile logging operations began on the Oklawaha River which caused so many obstructions that navigation became very difficult. Lack of use aggravated the conditions, and floating islands so obstructed the river between Lake Griffin and a point about 5 miles below the lake that navigation even for small boats became very difficult. The railroads then obtained control of the traffic, which had previously been tributary to the lake region at the head of the river, and have retained it ever since, establishing freight rates that have seriously handicapped further development of this section as compared with other sections more favorably situated as to means of transportation.",
      "Logs, and the railroads",
      "The same logging that Lanier met at the river's mouth in 1875 choked its upper course; the railroads took the trade."),
    u(3, HD514 + ", p. 8",
      "First [class]: Leesburg 68 cents, Sanford 37 cents. Second: 62, 32. Third: 57, 29. Fourth: 45, 24. Fifth: 38, 19. Sixth: 33, 16. Thus it will be seen that the freight rates on all classes from Leesburg averages nearly twice the rate from Sanford. I am informed that during the time the Oklawaha steamers ran to Leesburg the rate on a box of oranges from Leesburg to Jacksonville was 10 cents. Shipments from the large orange groves at Emeralda, situated on the river and on Lake Griffin, where the river leaves the lake, are now required to be made across the lake on a boat owned by the railroad and delivered at the terminal owned by the railroad at Leesburg. The rate from Emeralda to Leesburg is 9 cents per box, and the rate from Leesburg to Jacksonville is 17 cents, a total of 26 cents, as against the rate of 10 cents formerly enjoyed.",
      "Ten cents or twenty-six",
      "Freight rates per hundred pounds to Jacksonville, from Leesburg (by rail only) and from Sanford (on the St. Johns, with river steamers); the table is set here as running text. The argument for a waterway is here what it was for the barge canal later: competition with the railroads."),
    u(4, HD514 + ", p. 7",
      "A board of Engineer officers was appointed April 5, 1911, to consider and make recommendations concerning the improvement and the preservation of the navigability of this stream. The board submitted its report under date of April 27, 1911. It recommended that a cut-off about 4 miles long made by private enterprise for the purpose of reclaiming land between Moss Bluff and a point about 10 miles above Silver Springs Run be legalized and that the available funds be expended in the construction of a lock and dam to insure that the water level above this cut-off might not be lowered.",
      "A private cut-off",
      "Before any federal canal, private owners had already cut the river to drain land; the engineers proposed to make the cut lawful and build a lock to hold the water above it."),
    u(5, HD514 + ", p. 10: Board of Engineers for Rivers and Harbors, 2 April 1912",
      "This river has been under improvement since 1891, when a project was adopted for clearing the river of obstructions so as to give a 4-foot channel depth at mean low water from the mouth to Leesburg, a distance of 94 miles. … There is a total commerce in this lake region reported to amount to about 100,000 tons, all handled by rail. Except perhaps for a small amount of local commerce, there is none by water in the upper section of the river, but on the lower river it is reported as amounting to nearly 100,000 tons, about 80,000 tons of which consists of logs.",
      "Eighty thousand tons of logs",
      "What the water-lane carried around 1910: mostly logs."),
    u(6, HD514 + ", p. 2: Acting Chief of Engineers, 7 January 1914",
      "The board expresses the opinion that the present and prospective commerce is sufficient to justify the United States in undertaking this improvement— Provided, That any land necessary for the construction of the waterway shall be given to the United States without charge; that interested property owners shall agree to protect the United States against claims for damages on account of any land that may be flooded; that local interests give satisfactory assurance that they will provide for the use of the public suitable wharf and terminal facilities in the vicinity of Leesburg; and that they will establish and operate a boat line over this waterway which will be competitive with the railroads and not subject to control or purchase by railroad and other corporate interests.",
      "On conditions",
      "The pattern of the later canal is already here: the federal government builds, but the land must come free from local interests, and the owners of flooded land must hold Washington harmless. In the 1930s the counties of the canal district bought the right of way (module 3)."),
]

SRC = ("Sidney Lanier, Florida: Its Scenery, Climate, and History (Philadelphia: J. B. Lippincott, 1875/76); "
       "The Atlantic & Gulf Ship Canal across the Peninsula of Florida (London 1877, privately printed); "
       "House Document 514, 63rd Congress, 2nd Session (1914), Oklawaha River, Fla.: all Internet Archive. All in the public domain.")

T = {
    "id": "river", "titel": "The water-lane", "jahr": "1832–1914",
    "autor": "A poet on a steamboat, a canal company's prospectus and the Army's engineers",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. Tables are set as running text; Lanier's two tunes, printed in notes, are left out. Lanier wrote for visitors, the prospectus for investors, the engineers for Congress. The people who worked and lived on the river, raftsmen, pole-men, gatherers, appear only through them, and the Seminole people of the valley only in Lanier's history written from the government's side.",
    "sections": [
        {"id": "lanier", "titel": "A water-lane (1875)",
         "blurb": "In May 1875 the poet Sidney Lanier went up the Ocklawaha on the little steamboat Marion and called it “the sweetest water-lane in the world”. He also wrote down who worked on it: the raftsmen bringing pine logs down, the pole-men Dick and Henry, the people along the banks who paid for shoes in swamp leaves.",
         "plates": ["barker1886_osceola", "lanier1875_lane", "champney1873_marion", "fenn1870_shingles"], "units": LANIER},
        {"id": "payne", "titel": "Payne's Landing (1832, told in 1875)",
         "blurb": "The river had a history before the steamboats. At Payne's Landing on the Ocklawaha, in 1832, the United States made the treaty by which Seminole leaders were to agree to leave Florida; war followed in 1835. Lanier tells it from the government's side.",
         "units": PAYNE},
        {"id": "routes", "titel": "A canal through the river (1874–1877)",
         "blurb": "The canal idea came back by way of the river. The owner of the Ocklawaha steamers held a charter for a canal to the Withlacoochee, and a company with a Florida charter of 1874 sought money in London for a ship canal by the Ocklawaha or the Suwannee, in a prospectus printed in twenty copies.",
         "plates": ["prospectus1877_title", "hart1890_card"], "units": ROUTES},
        {"id": "trade", "titel": "Logs, oranges and railroads (1911–1914)",
         "blurb": "By 1910 the river carried about 100,000 tons a year, four fifths of it logs; the steamers to the lakes had given way to railroads, which charged Leesburg twice the rates of towns on the St. Johns. The Army's engineers proposed locks and a six-foot channel, on condition that local interests give the land and run a boat line free of the railroads.",
         "plates": ["okl1914_rates", "detroit1902_ocklawaha", "okl1914_proviso"], "viz": "river-rates", "units": TRADE},
    ],
}
for s in T["sections"]:
    s["zk"] = "The water-lane, " + re.sub(r" \(.*", "", s["titel"])
(D / "river.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
IA = "Internet Archive; public domain."
NEW = [
    {"id": "barker1886_osceola", "side": "river", "titel": "The Osceola in the Great Cypress Pass, 1886",
     "caption": "The steamer Osceola in the Great Cypress Pass of the Ocklawaha. Photograph by George Barker of Niagara Falls.",
     "source": "Library of Congress, Prints and Photographs, cph.3b42152, via Wikimedia Commons; public domain."},
    {"id": "lanier1875_lane", "side": "river", "titel": "“The sweetest water-lane in the world”, 1875",
     "caption": "Page 20 of Lanier's Florida: the lumberman's complaint about the rain, the turn into the Ocklawaha, and Dick the pole-man asleep on the guards.",
     "source": "Sidney Lanier, Florida (1875/76), p. 20; " + IA},
    {"id": "champney1873_marion", "side": "river", "titel": "The Marion on the Ocklawaha, 1873",
     "caption": "The stern-wheeler Marion on the Ocklawaha, drawn by J. Wells Champney for Edward King's series on the South; Lanier travelled on a boat of that name in 1875.",
     "source": "Edward King, The Great South (1875), engraving after J. Wells Champney, via Wikimedia Commons; public domain."},
    {"id": "fenn1870_shingles", "side": "work", "titel": "A cypress-shingle yard on the Ocklawaha, 1870",
     "caption": "Harry Fenn's watercolour of a yard where shingles were split from cypress on the river: the timber work that the steamers carried and the logging that later choked the upper river.",
     "source": "Harry Fenn, The Cypress-Shingle Yard, Ocklawaha River, Florida, watercolour, 1870; The Metropolitan Museum of Art 201672, via Wikimedia Commons; CC0."},
    {"id": "prospectus1877_title", "side": "land", "titel": "A prospectus for twenty readers, 1877",
     "caption": "Title page of the privately printed prospectus of the Atlantic & Gulf Ship Canal across the Peninsula of Florida, London 1877: “Only 20 Copies.”",
     "source": "The Atlantic & Gulf Ship Canal across the Peninsula of Florida (London 1877), title page; Cornell University Library via " + IA},
    {"id": "hart1890_card", "side": "river", "titel": "Hart's Daily Line, 1890",
     "caption": "Schedule card of Hart's Daily Line, Ocklawaha Navigation Company, Palatka, 14 February 1890, signed by H. L. Hart, general manager: the steamers Okeehumpkee and Astatula between Palatka and Silver Springs. Lanier names a “Colonel Hart, of Pilatka” as the holder of a canal charter.",
     "source": "State Archives of Florida, Florida Memory, item 148613, via Wikimedia Commons; public domain."},
    {"id": "okl1914_rates", "side": "land", "titel": "Twice the rate, 1911",
     "caption": "Freight rates to Jacksonville from Leesburg, by rail only, and from Sanford, on the river: “nearly twice the rate”; a box of oranges 10 cents by the old steamers, 26 cents by rail.",
     "source": "House Document 514, 63rd Congress, 2nd Session (1914), p. 8; " + IA},
    {"id": "detroit1902_ocklawaha", "side": "river", "titel": "On the Ocklawaha, about 1902",
     "caption": "A river steamer on the Ocklawaha, Detroit Publishing Company photograph.",
     "source": "Library of Congress, Detroit Publishing Company collection, LCCN 2008679617, via Wikimedia Commons; public domain."},
    {"id": "okl1914_proviso", "side": "capitol", "titel": "On conditions, 1914",
     "caption": "The Army's engineers recommend locks and a six-foot channel to Lake Dora, provided that local interests give the land free, hold the United States harmless for flooded land, and run a boat line free of the railroads.",
     "source": "House Document 514, 63rd Congress, 2nd Session (1914), p. 2; " + IA},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["credit"] = ("Pages and maps of congressional documents from the U.S. Congressional Serial Set, scans of govinfo.gov, and from the Internet Archive; "
               "newspaper pages from the Florida Digital Newspaper Library, University of Florida; photographs and drawings of the Ocklawaha from the Library of Congress, "
               "the Metropolitan Museum of Art and the State Archives of Florida via Wikimedia Commons. All in the public domain or CC0.")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "river"), None) or next(x for x in M["shipped"] if x["id"] == "river")
M["planned"] = [x for x in M["planned"] if x["id"] != "river"]
m.update({"datei": "river", "zk": "Lanier · Payne's Landing · Routes · Trade",
          "kurz": "2 · The water-lane",
          "warum": "In 1875 a poet called the Ocklawaha “the sweetest water-lane in the world” and wrote down who worked on it: raftsmen, the pole-men Dick and Henry, gatherers paid in shoes. A London prospectus promised a canal through it with “not a single engineering difficulty”. By 1910 the river carried mostly logs, and the railroads had its trade.",
          "quelle": "Sidney Lanier, Florida (1875/76); The Atlantic & Gulf Ship Canal (London 1877); House Document 514, 63rd Congress (1914); photographs of 1886 and 1902."})
order = ["ridge", "river", "relief", "camp", "aquifer", "war", "rodman", "undoing"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "river"] + [m], key=lambda x: order.index(x["id"]))
ADD = [{"id": "crews", "side": "work", "kurz": "The crews of the river",
        "warum": "Raftsmen, pole-men, firemen and woodcutters appear only in a visitor's book and as tonnage in the engineers' reports. Their names beyond “Dick” and “Henry”, their pay, and whether the boats' Black hands were free labourers or, before 1865, enslaved, is not in the sources read.",
        "quelle": "Records of the steamboat lines (Hart Line); census returns of Putnam and Marion counties."},
       {"id": "removal", "side": "land", "kurz": "Payne's Landing and the war of 1835–1842",
        "warum": "The treaty of Payne's Landing (1832) and the records of the Second Seminole War are federal documents and in the public domain, but have not yet been read for this apparatus. Until they are, the river's Seminole history appears only in Lanier's account of 1875, told from the government's side.",
        "quelle": "Treaty with the Seminole at Payne's Landing, 1832 (Statutes at Large, vol. 7); American State Papers, Military Affairs and Indian Affairs."},
       {"id": "inglis", "side": "river", "kurz": "The dam at Inglis",
        "warum": "The power dam on the Withlacoochee near Inglis, which made Lake Rousseau and later lay on the canal's western route, has not yet been documented from a source of its time.",
        "quelle": "To be found."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "tons", "titel": "How much would pass?",
     "frage": "How much traffic was waiting for a canal across Florida?",
     "note": "A London prospectus of 1877 counted 27,000,000 tons “now ready to pass”. Three years later the Army's engineers found about 2,600,000 tons a year passing the Florida Straits, and needed four times that to make a canal pay.",
     "voices": [{"text": "river", "sec": "routes", "n": [4], "wer": "Canal prospectus, London 1877"},
                {"text": "ridge", "sec": "company", "n": [3], "wer": "Q. A. Gillmore, 1880"}]},
    {"id": "lane", "titel": "Water-lane and log road",
     "frage": "What was the Ocklawaha?",
     "note": "To the poet in 1875 the river was a lane of pure delight, with logs and raftsmen at its mouth. To the engineers in 1912 it was a channel that carried 80,000 tons of logs a year and nothing above the lakes.",
     "voices": [{"text": "river", "sec": "lanier", "n": [3], "wer": "Sidney Lanier, 1875"},
                {"text": "river", "sec": "trade", "n": [5], "wer": "Board of Engineers, 1912"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/river/"
for s in TL["stations"]:
    if s["titel"] == "“The sweetest water-lane in the world”":
        s.update({"cite": K + "lanier/3", "citeLabel": "The water-lane, 1875 [3]", "plate": "lanier1875_lane",
                  "text": "Sidney Lanier goes up the Ocklawaha on the steamboat Marion, past raftsmen bringing pine logs down; the pole-men Dick and Henry push the boat off the banks at night."})
NEWST = [
    {"d": "1877", "side": "land", "titel": "Twenty copies for London",
     "text": "A privately printed prospectus seeks money for a ship canal across Florida, by the Suwannee or the Ocklawaha, under a Florida charter of 1874: “not a single engineering difficulty”, 27,000,000 tons “now ready to pass”.",
     "cite": K + "routes/3", "citeLabel": "The water-lane, 1877 [3]", "plate": "prospectus1877_title",
     "quelle": "The Atlantic & Gulf Ship Canal across the Peninsula of Florida (London 1877), pp. 30–31."},
    {"d": "29 December 1911", "side": "land", "titel": "Twice the rate",
     "text": "The Army's district engineer reports that the railroads control the trade of the lakes at the head of the Ocklawaha and charge Leesburg nearly twice the rates of Sanford on the St. Johns.",
     "cite": K + "trade/3", "citeLabel": "The water-lane, 1911 [3]", "plate": "okl1914_rates",
     "quelle": "House Document 514, 63rd Congress, 2nd Session, pp. 7–8."},
    {"d": "7 January 1914", "side": "river", "titel": "Locks for the Ocklawaha, on conditions",
     "text": "The Chief of Engineers' office recommends a six-foot channel with locks to Lake Dora for $733,000, if local interests give the land and run a boat line independent of the railroads. The river carries about 100,000 tons a year, mostly logs.",
     "cite": K + "trade/6", "citeLabel": "The water-lane, 1914 [6]", "plate": "okl1914_proviso",
     "quelle": "House Document 514, 63rd Congress, 2nd Session, pp. 2, 10."},
]
titles = {s["titel"] for s in NEWST}
TL["stations"] = [s for s in TL["stations"] if s["titel"] not in titles] + NEWST
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def key(s):
    d = s["d"]
    y = re.search(r"\d{4}", d)
    mon = next((i + 1 for i, x in enumerate(MONTHS) if x in d), 0)
    day = re.match(r"(\d{1,2}) ", d)
    return (int(y.group()) if y else 9999, mon, int(day.group(1)) if day else 0)


TL["stations"].sort(key=key)
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
