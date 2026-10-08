"""Builds data/rodman.json (module 7: Rodman, 1909–1974) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/rodman/PRUEFUNG.md):
  Florida Geological Survey, Twelfth Biennial Report (1955–56), p. 45 (UFDC UF00000223/00010);
  Sanford Herald, 14 August 1962, p. 1 (UFDC AA00087662/00859);
  Public Papers of the Presidents: Lyndon B. Johnson, 1963–64, Book I, no. 198, pp. 315–316 (govinfo PPP-1963-book2);
  Florida Board of Conservation, Biennial Report 1963–1964, p. 71 (UFDC UF00075929/00014);
  The Tampa Morning Tribune, 3 June 1909 (UFDC AA00020296/01174); The Metropolis (Jacksonville), 5 April 1912
    (UFDC UF00048819/01717);
  U.S. Geological Survey, G. L. Faulkner, Ground-water conditions in the lower Withlacoochee River – Cross-Florida
    Barge Canal complex, WRI 4-72 (January 1973), data sheet and pp. 1–2; Faulkner, Geohydrology of the Cross-Florida
    Barge Canal area, WRI 1-73 (1973), p. 87;
  Federal Water Pollution Control Administration, Pre-impoundment studies of the waters of the Cross-Florida Barge
    Canal (December 1967), pp. 3A, 5A (Internet Archive micro_IA41159433_0119, leaves n7, n9);
  Boynton v. Canal Authority, 311 So.2d 412 (Fla. 1st DCA 1975), p. 414; Canal Authority of Florida v. Callaway,
    489 F.2d 567 (5th Cir. 1974), pp. 570–571 (Caselaw Access Project page images);
  House Report 91-1701 (9 December 1970) (govinfo SERIALSET-12884_08_00-035-1701-0000);
  USGS topographic maps, Rodman quadrangle, editions of 1949 and 1993.
Rights: federal and Florida state works and court decisions are in the public domain; the newspapers of 1909 and 1912
were published before 1931; for the Sanford Herald of 1962 no renewal of copyright has been found.
Run from the site root: python tools/build-rodman.py
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


CA5 = "Canal Authority of Florida v. Callaway, 489 F.2d 567 (5th Cir., 15 February 1974)"

REVIVAL = [
    u(1, "Florida Geological Survey, Twelfth Biennial Report (1955–1956), p. 45",
      "The tonnages of water-borne commerce anticipated to be transported by the Cross-Florida and Sanford-Titusville canals were estimated based on data obtained from the Army Engineers, port authorities, barge operators, barge terminal operators, towing companies, and some industries that manufacture or mine products that could be transported by barge. … The survey of traffic indicates sufficient tonnage would be shipped to justify the construction of the Cross-Florida Barge Canal and that the Sanford-Titusville Canal will be extensively used as a commercial waterway, and for pleasure craft as soon as it can be opened for navigation. … At least 19 new industrial schedules involving 12 different products have indicated a desire to locate along the Cross-Florida Barge Canal, if built.",
      "Nineteen industries",
      "The barge canal's new reason after the war: growth and industry. The traffic study was made by consultants “under direct supervision of the Florida Ship Canal Authority” (same page): the canal's sponsor counted its own traffic. Sanford, the old opponent, now had a canal of its own in view."),
    u(2, "Sanford Herald, 14 August 1962, p. 1 (United Press International)",
      "Washington (UPI)—The House appropriations committee today virtually crushed the long-cherished dream of a barge canal across the heart of Florida. The committee refused to approve any money for the Cross-Florida Barge Canal and said it will not consider the project again until Congress once more authorizes …",
      "“Virtually crushed”",
      "Twenty years after the act of 1942, still no construction money. It came in the next budget years; the money and the votes of 1962–1963 have not yet been read in the Congressional Record."),
]

GROUND = [
    u(1, "Public Papers of the Presidents: Lyndon B. Johnson, 1963–64, Book I, no. 198: Remarks at the Ground-Breaking Ceremony for the Florida Cross-State Barge Canal, 27 February 1964, p. 315",
      "God was good to this country. He endowed it with resources unsurpassed in their variety and their abundance. But in His wisdom the Creator left something for men to do for themselves. He gave us great rivers, but He left them to run wild in the flood, and sometimes to go dry in the drought—and sometimes to rain when we have a celebration. But He left it to us to control these carriers of commerce. … Today we accept another challenge. We make use of another resource. We will construct a canal across northern Florida to shorten navigation distances between our Atlantic and our Gulf coasts. When this canal is completed, it will spark new and permanent economic growth. It will accelerate business and industry to locate here on its banks. It will open up new recreation areas. The challenge of a modern society is to make the resources of nature useful and beneficial to the community. … This new ribbon of water will enable barges to move across the Florida peninsula a few years from now, bearing commerce between the two seacoasts.",
      "“A ribbon of water”",
      "The President at Palatka. Rivers “run wild”; the canal makes “the resources of nature useful”. Seven years later another President would call the same river “a natural treasure”."),
    u(2, "Public Papers, Johnson 1963–64, no. 198, pp. 315–316",
      "I am relieved that I am finally going to press the button and push the switch that starts this great canal, because I remember every time I went to the House, Billy Matthews would catch me by the lapels of my coat, and George Smathers couldn't leave a leadership meeting without talking to me about it. I thought Spessard Holland was going to have a heart attack the last time he talked to me because he told me if this money was not in for the Florida Cross-State Canal, there was going to be trouble when my budget got to the Congress. … Governor Bryant, as I throw this switch detonating an explosive charge to break ground for this canal, let me commend the Army Corps of Engineers who will build this canal so wisely and so many times before.",
      "The switch",
      "As in 1935, the work began with a charge set off by the President, this time on the spot. The money, by his own account, came from the pressure of Florida's delegation."),
    u(3, "Florida Board of Conservation, Biennial Report 1963–1964, p. 71",
      "When President Johnson pushed the button to touch off the blast that moved the first dirt at ground-breaking ceremonies near Palatka on February 27, 1964, a dream of far-seeing Floridians dating back to the administration of Territorial Governor Andrew Jackson was culminated. Ground was broken December 17, 1964 for the St. Johns Lock, the first of five giant navigational locks along the 107-mile barge canal, and earlier the U. S. Army Corps of Engineers had awarded a $1.81 million contract for dredging a five mile segment of the canal at the western terminus, the mouth of the Withlacoochee River. The shallow-draft waterway avoids a deep cut into the Florida aquifer and will have no adverse effect on the fresh water resources of the state. … Construction costs of $157.9 million, will be borne entirely by the federal government. Lands for right-of-way and spoil areas must be acquired by state and local interests. These costs are estimated at $12.4 million.",
      "“No adverse effect”",
      "The State's assurance on the old fear of 1935–37 (module 5): a shallow canal with locks will not harm the ground water. Land, as before, was to come from state and local interests."),
]

INGLIS = [
    u(1, "The Tampa Morning Tribune, 3 June 1909: from Dunnellon",
      "Rapid progress on the dam across the Withlacoochee river, ten miles below here, by the Camp Power company, is being made, and it is expected to be completed by the first of September. The dam will be one of the largest in the state of this kind, costing about $200,000. The power will be used for the purpose of operating phosphate plants and for lighting towns and other power purposes.",
      "A dam on the Withlacoochee",
      "The dam near Inglis, built for the phosphate mines of the Dunnellon district, made the lake of the lower Withlacoochee that the barge canal planned to use as its western pool ([3])."),
    u(2, "The Metropolis (Jacksonville), 5 April 1912, from the report of E. H. Sellards, State Geologist",
      "A notable feature in the development of the hard rock industry was the construction of a dam across the Withlacoochee river, as a result of which it has been possible to supply electric power to a number of the phosphate plants in Citrus and Marion counties. With the aid of electric power and light some of the mines have been able to work day and night shifts, thereby materially increasing the output.",
      "Day and night shifts",
      "Power for the hard-rock phosphate mines; the work in those mines, much of it done by leased convicts in the 1890s, is documented in the companion apparatus on Williston, The Shipping Point."),
    u(3, "U.S. Geological Survey, G. L. Faulkner, Geohydrology of the Cross-Florida Barge Canal Area, WRI 1-73 (1973), p. 87",
      "Inglis Pool.—The Inglis Pool will consist essentially of what presently is called the Withlacoochee backwater or Lake Rousseau, the impoundment on the Withlacoochee River maintained by the old Inglis Dam …",
      "Lake Rousseau",
      "The lake made by the dam of 1909 was to become a pool of the barge canal, the step above Inglis Lock."),
    u(4, "U.S. Geological Survey, G. L. Faulkner, Ground-water conditions in the lower Withlacoochee River – Cross-Florida Barge Canal complex, WRI 4-72 (January 1973), data sheet",
      "Construction of the westernmost 7-mile reach of the Cross Florida Barge Canal, which intersects the lower Withlacoochee River 9 miles above its mouth, began in 1965 and completed in 1969. The river channel and the canal penetrate the cavernous limestone of the Floridan Aquifer below the water table.",
      "Built: the western end",
      "At Inglis the canal was built: a lock, a bypass channel from the old river and a cut to the Gulf."),
    u(5, "USGS WRI 4-72 (1973), pp. 1–2",
      "Ground-water levels in a 15-square-mile area centered at the Barge Canal near the U.S. Highway 19 bridge are 0.5 foot to nearly 15 feet lower than they would be had the canal not been built. … During the same 1-year period, an average of 237 cfs of surface water was discharged through Inglis Dam and diverted down the canal to the gulf. Had the canal not been built, this water would have flowed to the gulf via the river and would have amounted to about 16 percent of the fresh-water discharge of the river for the 1-year period. … When fresh-water flow from Inglis Dam to the Barge Canal is very low, the water level in the canal is at or very near sea level, and salt water from the gulf moves inland by way of the canal to Inglis Lock and part way up the 1.5 mile reach of the river between the canal and the dam.",
      "Lower water, and salt",
      "What the finished western end did, measured: ground water lowered near the cut, river water diverted down the canal, and salt water moving inland to the lock. The old fear of 1935, on a small scale and in a place where no one had feared it."),
    u(6, "Federal Water Pollution Control Administration, Pre-impoundment studies (December 1967), p. 5A",
      "Monitors for chlorides and/or conductivity should be installed on the impoundment ends of the St. Johns and Inglis locks in order to assess the significance of salinity intrusion from the operation of these locks.",
      "Salt at the locks",
      "Foreseen in 1967, measured in 1971 ([5])."),
]

RODMAN = [
    u(1, "Federal Water Pollution Control Administration, Pre-impoundment studies (December 1967), p. 3A",
      "Physical, chemical and bacteriological water quality studies of the proposed Cross Florida Barge Canal area were conducted in March and April of 1967 to determine conditions before significant construction activity on the major impoundments in the canal took place. In general, water quality in the proposed impounded areas was excellent and should be acceptable if maintained at these levels for the proposed contact and non-contact recreational uses. However, there are problems which are presently localized but which, if not carefully controlled, may impair the desired uses. … It is imperative that the Corps of Engineers strictly control the release of water from Moss Bluff Dam so that there is no possibility of drowning Silver Springs with Oklawaha River water during the flood season.",
      "“Excellent”",
      "The river measured before the dam: excellent water. A reader of the copy wrote in the margin that the report “discusses the problems which may affect water quality”."),
    u(2, "Boynton v. Canal Authority, 311 So.2d 412 (Fla. 1st DCA, 24 April 1975), p. 414",
      "Appellants, who will hereinafter be referred to as the landowners, initially held fee simple title to approximately 632 acres of land, extending northerly from the thread of the Ocklawaha River. In 1965 appellee sought to acquire the fee simple title to 540 acres of that property, located adjacent to and upstream of the Rodman Dam, for the purpose of flooding 520 acres as part of the Rodman Pool (now known as Lake Ocklawaha), the other 20 acres constituting a 300 foot “collar” of land between the pool and the landowners remaining 92 acres of upland. In that proceeding the trial court declined to allow the Canal Authority to condemn the fee title to the 540 acres, whereupon an Order of Taking was entered on January 3, 1966 vesting in the Canal Authority, instead of the fee simple title, a “perpetual right and easement.” In 1968 another suit was filed to acquire the fee simple title to the same 540 acres of land … A trial was held in September of 1970 … A second trial was held in March of 1973, culminating in a hung jury and a resulting mistrial. In September of 1973 a third trial was held …",
      "“To enter upon, and permanently or intermittently overflow, flood and submerge”",
      "One property under the Rodman pool, in court for ten years. The easement taken in 1966 gave the Canal Authority the right “to enter upon, and permanently or intermittently overflow, flood and submerge the lands”. The decision names the landowners only as “Boynton, et al.”; how many families lost land to the pool is not counted in the sources read."),
    u(3, CA5 + ", p. 570",
      "The Ocklawaha River has its source in several large lakes of the central peninsula of Florida. It flows northward for sixty miles and enters the St. Johns River eight miles below Lake George. Its waters run clear, although stained by acids from the bark and leaves of the dense tree swamp through which it meanders. Its tree swamp ecology is rich, supporting a much more abundant and varied wildlife population than the adjacent pine islands. … As part of the Cross Florida Barge Canal project, Rodman Dam was built on the Ocklawaha River. After the dam's completion in 1968, the waters it impounded created a lake approximately sixteen miles long, flooding some 13,000 acres of partially cleared land in the Ocklawaha Valley. A number of the trees in this area had previously been cleared by being crushed into the swamp floor. However, approximately 1135 acres of large hardwood trees, many of which had lined the course of the Ocklawaha River prior to the inundation, were left standing to be flooded by the lake, primarily so as to serve as a fish habitat. The flooding is progressively killing off the remaining trees.",
      "Thirteen thousand acres",
      "Lanier's water-lane (module 2), ninety years on: a lake sixteen miles long over a crushed and drowned forest."),
    u(4, "House Report 91-1701, 9 December 1970",
      "The purpose of the bill is to rename the Rodman Pool of the Cross-Florida Barge Canal, Lake Ocklawaha. … The total distance of the waterway will be 185 miles and will include five single-lift navigation locks, each 84 feet wide by 600 feet long, and three dams and reservoirs to provide water supply for lock operation. The Rodman Pool, which the bill would rename Lake Ocklawaha, is formed by the Rodman Dam on the Ocklawaha River, and stretches from the Rodman Dam to the Eureka lock and dam. The suggested name change would both preserve the name of the river and restore it to its original spelling as indicated on the Corps of Engineers maps compiled in 1839 and 1842.",
      "Lake Ocklawaha",
      "The reservoir that drowned the river was to bear its name, “to preserve the name of the river”. Six weeks later the work was stopped."),
]

HALT = [
    u(1, CA5 + ", p. 570",
      "In September, 1969, the Environmental Defense Fund, joined by the Florida Defenders of the Environment and several individuals, filed suit in the United States District Court for the District of Columbia to halt construction of the Cross Florida Barge Canal project. After a hearing, the district court denied the defendants' motion to dismiss and orally granted the plaintiffs' motion for a preliminary injunction to stop certain aspects of the construction. Before these orders were entered the President of the United States, pursuant to the advice of the Council on Environmental Quality, ordered the suspension of further construction of the canal.",
      "The suit of 1969",
      "The opponents' own report of 1970 is not printed here (see Texts, “Examined and not included”); their case appears in the federal record: in this court's summary and in the hearings of the 1980s (module 8)."),
    u(2, CA5 + ", pp. 570–571, footnote 2: “The full text of the President's statement of January 19, 1971”",
      "I am today ordering a halt to further construction of the Cross Florida Barge Canal to prevent potentially serious environmental damages. The purpose of the Canal was to reduce transportation costs for barge shipping. It was conceived and designed at a time when the focus of Federal concern in such matters was still almost completely on maximizing economic return. In calculating that return, the destruction of natural, ecological values was not counted as a cost, nor was a credit allowed for actions preserving the environment. A natural treasure is involved in the case of the Barge Canal—the Oklawaha River—a uniquely beautiful, semi-tropical stream, one of a very few of its kind in the United States, which would be destroyed by construction of the Canal. The Council on Environmental Quality has recommended to me that the project be halted, and I have accepted its advice. The Council has pointed out to me that the project could endanger the unique wildlife of the area and destroy this region of unusual and natural beauty. The total cost of the project if it were completed would be about $180 million. About $50 million has already been committed to construction. I am asking the Secretary of the Army to work with the Council on Environmental Quality in developing recommendations for the future of the area. The step I have taken today will prevent a past mistake from causing permanent damage. But more important, we must assure that in the future we take not only full but also timely account of the environmental impact of such projects—so that instead of merely halting the damage, we prevent it.",
      "“A past mistake”",
      "The statement is also printed in the Public Papers of the Presidents, Richard Nixon, 1971, no. 20, pp. 43–44. The President names the cost the old accounts had left out: what was destroyed."),
    u(3, CA5 + ", p. 571",
      "The Canal Authority of the State of Florida, the local sponsor of the project, then moved to intervene in the District of Columbia action alleging that as a result of the President's order the federal defendants were no longer able to defend the canal project. Prior to the granting of the motion, the Canal Authority filed a second action in the Middle District of Florida against substantially the same defendants, alleging wrongful termination of the project. … Prior to the consolidation the United States Forest Service recommended that Lake Ocklawaha be drained, so as to preserve as many trees as possible. … On June 1, 1972 … a task force … composed of more than fifty experts in the fields of ecology, forestry, plant physiology and pathology, aquatic weeds, recreation, fisheries, biology, photogrammetry, hydrology, biochemistry, engineering, agronomy, and mathematics … recommended that Lake Ocklawaha be lowered immediately to an elevation of thirteen feet m. s. l. to preserve the large number of living trees threatened with imminent death so as to maintain all future options for ecologically sound use of the area.",
      "Drain the lake, or keep it",
      "The fight moved from the canal to the lake: the canal's sponsors sued to keep it full, the foresters wanted it drained. The question of the dam outlasted the canal; it is outlook, not subject, of this apparatus."),
]

SRC = ("Florida Geological Survey 1956 and Florida Board of Conservation 1964 reports (University of Florida Digital Collections); Public Papers of the "
       "Presidents, Johnson 1963–64 (govinfo.gov); Tampa Morning Tribune 1909, The Metropolis 1912, Sanford Herald 1962 (Florida Digital Newspaper "
       "Library); U.S. Geological Survey reports WRI 4-72 and WRI 1-73 (1973); Federal Water Pollution Control Administration, Pre-impoundment studies "
       "(1967; Internet Archive); Boynton v. Canal Authority (1975) and Canal Authority v. Callaway (1974) (Caselaw Access Project); House Report 91-1701 "
       "(1970). Public domain; for the newspaper of 1962 no renewal of copyright has been found.")

T = {
    "id": "rodman", "titel": "Rodman", "jahr": "1909–1974",
    "autor": "Florida's agencies, President Johnson, the Geological Survey, federal and state courts",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. Newspapers from 1964 on are not printed here. The opponents of the 1960s, the Florida Defenders of the Environment and their allies, are heard through the courts' summaries and, in module 8, through their testimony to Congress; their own publications of the time are named, not printed.",
    "sections": [
        {"id": "revival", "titel": "Nineteen industries (1956–1962)",
         "blurb": "After the war the canal was argued for as growth: a traffic survey for the canal authority counted nineteen industries waiting for it. Congress still gave no money; in 1962 a House committee “virtually crushed the long-cherished dream”.",
         "plates": ["fgs1956_industries", "sh1962_crushed"], "units": REVIVAL},
        {"id": "ground", "titel": "A ribbon of water (1964)",
         "blurb": "On 27 February 1964 President Johnson set off the first charge at Palatka: a canal to make “the resources of nature useful”. The State promised that the shallow canal with locks would do no harm to its ground water.",
         "plates": ["ppp1964_palatka", "bc1964_activities"], "units": GROUND},
        {"id": "inglis", "titel": "The western end: Inglis and Lake Rousseau (1909–1973)",
         "blurb": "At Inglis the canal met an older work: the dam of 1909 that made the Withlacoochee backwater, Lake Rousseau, to power the phosphate mines. The canal's western reach, with Inglis Lock and a bypass channel, was finished in 1969; geologists measured what it did.",
         "plates": ["tt1909_dam", "met1912_power", "usgs1973_inglis"], "units": INGLIS},
        {"id": "rodman", "titel": "The Rodman pool (1965–1970)",
         "blurb": "In the east the Rodman dam, finished in 1968, flooded some 13,000 acres of the Ocklawaha valley. Owners of the land fought the Canal Authority in court for years; Congress was asked to name the reservoir Lake Ocklawaha.",
         "plates": ["topo1949_rodman", "topo1993_rodman", "fwpca1967_excellent", "boynton1975_easement"], "viz": "rodman-acres", "units": RODMAN},
        {"id": "halt", "titel": "The halt (1969–1972)",
         "blurb": "In 1969 the Environmental Defense Fund and the Florida Defenders of the Environment sued to stop the canal. On 19 January 1971, on the advice of his Council on Environmental Quality, President Nixon ordered the work halted, “to prevent potentially serious environmental damages”. The Canal Authority sued for its canal; the fight turned to the dam and the drowning trees.",
         "plates": ["ca5_1974_ocklawaha", "ca5_1974_nixon", "hrept1970_lake"], "units": HALT},
    ],
}
for s in T["sections"]:
    s["zk"] = "Rodman, " + re.sub(r" \(.*", "", re.sub(r":.*", "", s["titel"]))
(D / "rodman.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
UFDC = "University of Florida Digital Collections; public domain."
NP = "Florida Digital Newspaper Library, University of Florida; public domain."
CAP = "Caselaw Access Project, Harvard Law School Library, page image; public domain."
NEW = [
    {"id": "fgs1956_industries", "side": "land", "titel": "Nineteen industries, 1956",
     "caption": "The Florida Geological Survey reports the canal authority's traffic study: sufficient tonnage, and “at least 19 new industrial schedules”.",
     "source": "Florida Geological Survey, Twelfth Biennial Report (1955–56), p. 45; " + UFDC},
    {"id": "sh1962_crushed", "side": "capitol", "titel": "“Virtually crushed”, August 1962",
     "caption": "The House Appropriations Committee refuses money for the barge canal.",
     "source": "Sanford Herald, 14 August 1962, p. 1, detail; Florida Digital Newspaper Library, University of Florida; no copyright renewal found."},
    {"id": "ppp1964_palatka", "side": "capitol", "titel": "Ground-breaking at Palatka, 27 February 1964",
     "caption": "President Johnson's remarks: “This new ribbon of water will enable barges to move across the Florida peninsula a few years from now.”",
     "source": "Public Papers of the Presidents, Lyndon B. Johnson, 1963–64, Book I, p. 315; govinfo.gov; public domain."},
    {"id": "bc1964_activities", "side": "water", "titel": "“No adverse effect”, 1964",
     "caption": "The Florida Board of Conservation on the ground-breaking, the first lock, and the canal's harmlessness to the State's fresh water.",
     "source": "Florida Board of Conservation, Biennial Report 1963–1964, p. 71; " + UFDC},
    {"id": "tt1909_dam", "side": "river", "titel": "A dam on the Withlacoochee, 1909",
     "caption": "From Dunnellon: “Rapid progress on the dam across the Withlacoochee river, ten miles below here … The power will be used for the purpose of operating phosphate plants.”",
     "source": "The Tampa Morning Tribune, 3 June 1909; " + NP},
    {"id": "met1912_power", "side": "river", "titel": "Power for the mines, 1912",
     "caption": "The State Geologist: the Withlacoochee dam powers phosphate plants in Citrus and Marion counties, “day and night shifts”.",
     "source": "The Metropolis (Jacksonville), 5 April 1912, detail; " + NP},
    {"id": "usgs1973_inglis", "side": "water", "titel": "The western end measured, 1973",
     "caption": "The Geological Survey's conclusions on the canal below Inglis Lock: ground water lowered by up to 15 feet near the U.S. 19 bridge, salt water moving inland to the lock.",
     "source": "U.S. Geological Survey, WRI 4-72 (January 1973), p. 1; public domain."},
    {"id": "topo1949_rodman", "side": "river", "titel": "The Ocklawaha valley at Rodman, 1949",
     "caption": "The Rodman quadrangle before the dam: the Ocklawaha winding through its swamp forest.",
     "source": "Rodman quadrangle, 1:24,000, edition of 1949; USGS Historical Topographic Map Collection; public domain."},
    {"id": "topo1993_rodman", "side": "river", "titel": "The same valley, 1993",
     "caption": "The Rodman quadrangle after the dam: the pool over the valley.",
     "source": "U.S. Geological Survey, Rodman quadrangle, 1:24,000, 1993; USGS Historical Topographic Map Collection; public domain."},
    {"id": "fwpca1967_excellent", "side": "river", "titel": "“Excellent”, 1967",
     "caption": "The federal water-quality study before the impoundments, with a reader's note in the margin.",
     "source": "Federal Water Pollution Control Administration, Pre-impoundment studies of the waters of the Cross-Florida Barge Canal (1967), p. 3A; Internet Archive; public domain."},
    {"id": "boynton1975_easement", "side": "land", "titel": "Flood and submerge, 1966–1975",
     "caption": "Boynton v. Canal Authority: 540 acres taken for the Rodman pool, the easement “to … flood and submerge the lands”, and three trials.",
     "source": "Boynton v. Canal Authority, 311 So.2d 412 (Fla. 1st DCA 1975), p. 414; " + CAP},
    {"id": "ca5_1974_ocklawaha", "side": "river", "titel": "Thirteen thousand acres, 1974",
     "caption": "The Court of Appeals on the Ocklawaha, the Rodman dam, the drowning hardwoods, and the suit of 1969.",
     "source": "Canal Authority of Florida v. Callaway, 489 F.2d 567 (5th Cir. 1974), p. 570; " + CAP},
    {"id": "ca5_1974_nixon", "side": "capitol", "titel": "The halt, 19 January 1971",
     "caption": "The President's statement in full, printed by the Court of Appeals in a footnote.",
     "source": "Canal Authority of Florida v. Callaway, 489 F.2d 567 (5th Cir. 1974), p. 571; " + CAP},
    {"id": "hrept1970_lake", "side": "capitol", "titel": "Lake Ocklawaha, 1970",
     "caption": "House Report 91-1701: to rename the Rodman Pool “Lake Ocklawaha”.",
     "source": "House Report 91-1701 (9 December 1970), p. 1; U.S. Congressional Serial Set, govinfo.gov; public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "rodman"), None) or next(x for x in M["shipped"] if x["id"] == "rodman")
M["planned"] = [x for x in M["planned"] if x["id"] != "rodman"]
m.update({"datei": "rodman", "zk": "Revival · Palatka · Inglis · Rodman · Halt",
          "kurz": "7 · Rodman",
          "warum": "Johnson's “ribbon of water” in 1964; the western end at Inglis and Lake Rousseau, finished in 1969 and measured by geologists; the Rodman dam of 1968 flooding some 13,000 acres of the Ocklawaha valley and a family's land; the suit of 1969 and Nixon's halt of 19 January 1971, “to prevent potentially serious environmental damages”.",
          "quelle": "Florida Geological Survey 1956; Public Papers 1964; Board of Conservation 1964; newspapers 1909, 1912, 1962; USGS 1973; FWPCA 1967; court decisions 1974 and 1975; House Report 91-1701."})
order = ["ridge", "river", "relief", "camp", "aquifer", "war", "rodman", "undoing"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "rodman"] + [m], key=lambda x: order.index(x["id"]))
M["missing"] = [x for x in M["missing"] if x["id"] != "inglis"]
ADD = [{"id": "money1963", "side": "capitol", "kurz": "The money of 1963–1964",
        "warum": "How the barge canal finally received construction money in 1963–64, after twenty years, has not yet been read in the Congressional Record or the appropriation acts.",
        "quelle": "Congressional Record 1963; Public Works Appropriation Act 1964."},
       {"id": "ceq1971", "side": "river", "kurz": "The Council on Environmental Quality's advice (1971)",
        "warum": "The recommendation of January 1971 on which the President halted the canal is known here only from his statement and the court's summary.",
        "quelle": "Council on Environmental Quality, January 1971; annual report 1971."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "nature", "titel": "Rivers that run wild, a natural treasure",
     "frage": "What was the river for?",
     "note": "In 1964 the rivers “run wild” and the canal makes the resources of nature “useful and beneficial”. In 1971 the same river is “a natural treasure … which would be destroyed”, and the old accounts are faulted for not counting its destruction as a cost.",
     "voices": [{"text": "rodman", "sec": "ground", "n": [1], "wer": "Lyndon B. Johnson, 1964"},
                {"text": "rodman", "sec": "halt", "n": [2], "wer": "Richard Nixon, 1971"}]},
    {"id": "lanerodman", "titel": "The water-lane and the pool",
     "frage": "What became of Lanier's river?",
     "note": "In 1875 a lane of “pure delight betwixt hedgerows of oaks and cypresses”; in 1974 a lake sixteen miles long over a forest crushed into the swamp floor, its last hardwoods dying.",
     "voices": [{"text": "river", "sec": "lanier", "n": [3], "wer": "Sidney Lanier, 1875"},
                {"text": "rodman", "sec": "rodman", "n": [3], "wer": "U.S. Court of Appeals, 1974"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/rodman/"
for s in TL["stations"]:
    if s["titel"] == "Ground broken at Palatka":
        s.update({"cite": K + "ground/1", "citeLabel": "Rodman, 1964 [1]", "plate": "ppp1964_palatka"})
    if s["titel"] == "The halt":
        s.update({"cite": K + "halt/2", "citeLabel": "Rodman, 1971 [2]", "plate": "ca5_1974_nixon"})
NEWST = [
    {"d": "3 June 1909", "side": "river", "titel": "A dam on the Withlacoochee",
     "text": "A power company builds a dam below Dunnellon to supply the phosphate mines; its lake, later called Lake Rousseau, was planned as the western pool of the barge canal.",
     "cite": K + "inglis/1", "citeLabel": "Rodman, 1909 [1]", "plate": "tt1909_dam",
     "quelle": "The Tampa Morning Tribune, 3 June 1909."},
    {"d": "1968", "side": "river", "titel": "The Rodman dam",
     "text": "The dam on the Ocklawaha is finished; its pool, sixteen miles long, floods some 13,000 acres of the valley.",
     "cite": K + "rodman/3", "citeLabel": "Rodman, 1968 [3]", "plate": "topo1993_rodman",
     "quelle": "Canal Authority of Florida v. Callaway, 489 F.2d 567 (1974), p. 570."},
    {"d": "1969", "side": "survey", "titel": "The western end finished",
     "text": "The westernmost seven miles of the canal, with Inglis Lock, are completed from the Withlacoochee to the Gulf.",
     "cite": K + "inglis/4", "citeLabel": "Rodman, 1969 [4]", "plate": "usgs1973_inglis",
     "quelle": "U.S. Geological Survey, WRI 4-72 (1973)."},
    {"d": "September 1969", "side": "river", "titel": "The suit",
     "text": "The Environmental Defense Fund and the Florida Defenders of the Environment sue in Washington to halt the canal.",
     "cite": K + "halt/1", "citeLabel": "Rodman, 1969 [1]",
     "quelle": "Canal Authority of Florida v. Callaway, 489 F.2d 567 (1974), p. 570."},
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
