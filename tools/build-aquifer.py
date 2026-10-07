"""Builds data/aquifer.json (module 5: The water under Florida, 1934–1939) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/aquifer/PRUEFUNG.md):
  Congressional Record, Senate, 17 March 1936, pp. 3839, 3842, 3845–3846 (Internet Archive gpo-crecb-1936-pt-4-v-80-5,
    leaves n16, n19, n22, n23);
  Bradford County Telegraph (Starke), 7 August 1936, p. 1 (UFDC UF00027795/02553);
  House Document 194, 75th Congress, 1st Session (1937), pp. 4–6, 17, map and profile
    (govinfo SERIALSET-10127_00_00-002-0194-0000, PDF pp. 14–16, 27, 39, 601);
  Hearings on H.R. 6150, House Committee on Rivers and Harbors (1937), p. 125 (UFDC UF00018663/00001, image 00129);
  Congressional Record, Senate, 17 May 1939, pp. 5648–5649 (Internet Archive dli.ernet.78569, leaves n1014–n1015).
All U.S. government printings in the public domain; the newspaper of 1936 with no renewal of copyright found. Texts of
others read into the Record (newspaper editorials, telegrams) are quoted as the Record prints them.
Run from the site root: python tools/build-aquifer.py
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


CR36 = "Congressional Record, Senate, 17 March 1936"
HD194 = "House Document 194, 75th Congress, 1st Session (1937)"

WARNING = [
    u(1, CR36 + ", p. 3842: statement of H. H. Buckman, engineer of the canal authority, printed at Senator Fletcher's request",
      "In its report of June 28, 1934, the board of review found—I quote: “Any possible damage to agriculture beyond the limits of the right-of-way to be secured for the canal would be negligible, due to the fact that the water table is now from 30 to 70 feet below the ground along the route of the canal and for miles on either side of it. The damage to water supply would be small and would consist only in lowering levels in nearby wells. The possibility of salting the water supply at high level would be eliminated.”",
      "“Negligible”",
      "The President's special board of review of 1934, as quoted by the canal's own engineer. The Army's special board of 1933 had wanted a lock canal as a precaution; the board of review accepted a sea-level cut."),
    u(2, CR36 + ", p. 3842: Buckman, continued",
      "Under date of June 25, 1935, the State geologist, in a letter to Mr. Coachman, restates his attitude in the following words. I quote: “It was not my purpose to condemn a sea-level canal, provided the construction plans are adequate to maintain the adjacent ground-water level at approximately 40 feet above sea.”",
      "The State geologist",
      "Florida's own geologist, quoted by the canal's advocate: not against the canal, but only if the ground water were held at about 40 feet above the sea, which a sea-level cut could not do without works to hold it."),
    u(3, CR36 + ", p. 3842: Buckman, continued",
      "Under date of August 26, 1935, the personal assistant to the Secretary of the Interior, Mr. Harry Slattery, in a letter to Hon. J. Hardin Peterson, stated that in the opinion of the Geological Survey: “There appears to be no reasonable doubt that serious adverse effects would be produced upon the important underground water supplies of the Ocala limestone in a wide zone extending outward from the canal line by the construction of a sea-level canal along 13-B. “The particular dangers herein discussed apply to a sea-level canal only and not to a lock canal so constructed as to avoid deep cuts in the Ocala limestone and thus to leave undisturbed the present water level in this important water-bearing formation.”",
      "“No reasonable doubt”",
      "Four days before the President's allotment, the federal Geological Survey's warning, sent to a Florida congressman: a sea-level cut through the Ocala limestone would harm the ground water in a wide zone. Buckman prints it to argue that the Survey had made no special study of its own."),
    u(4, CR36 + ", p. 3839: the Chief of Engineers to Senator Fletcher, 28 January 1936",
      "The preliminary data gathered by the Department indicated that there was some possibility of adverse effects on the underground water supply. The more detailed information which is now available clearly indicates that the adverse effects are largely local and not of a serious nature. When the project was placed under way as a part of the relief program, I had the district engineer at Ocala, Fla., assemble a board of selected experts to consider the data gathered by the two boards, the State geological department and the Geological Survey, and to undertake additional and exhaustive field investigations. These experts have recently submitted their interim report, which definitely concludes that the effects of the sea-level canal on the underground water supply will not be serious but local in nature and capable of control with reasonable expenditures for remedial works. The authentic information available permits the conclusion that the sea-level canal will not contaminate the underground water supply of adjacent areas.",
      "“Will not contaminate”",
      "The Army's answer, written after the work had begun: its own board of experts, assembled at Ocala, found the effects local. Their report of December 1935 (Senate Document 147) has not yet been found; see Texts, “Examined and not included”."),
]

SENATE = [
    u(1, CR36 + ", p. 3845: editorial of the Miami Daily News, 11 March 1935, read at Senator Vandenberg's request",
      "There are reports, and more reports, on this huge enterprise, no two of which agree, and there remain many serious questions to be answered. The findings of Dr. Henry S. Sharp, geologist of Columbia University, appearing in the News' columns today, renew the challenge to Congress to answer these questions before authorizing construction or appropriating another dollar for the canal. Dr. Sharp asserts that it will jeopardize Florida's water supply over a wide area, “a matter of considerable economic importance.” … But $150,000,000 would be a relatively small amount compared to the damage if Florida's water resources were ruined, with all the agriculture dependent upon them. That is a disaster neither Florida nor the Nation can risk. So long as this threat remains the canal must not be built.",
      "“The canal must not be built”",
      "A Miami newspaper, as printed in the Record a year after it appeared. South Florida, which drew its water from the ground and grew citrus and vegetables, saw the canal as a threat; it was also not on the canal's route."),
    u(2, CR36 + ", p. 3845: telegram of W. Keith Phillips, president of the Miami Chamber of Commerce, read by Senator Vandenberg",
      "The people most affected by this canal are thousands of small farmers, truck gardeners, and citrus growers scattered over the southern two-thirds of this State, who are unorganized and unable to make a proper defense of their rights. We beg of you to stand by us in this hour of need, and, if possible, defeat this dangerous project. There is no demand for this canal from the shipping interests; and personal contact with numerous shipping men convinces me that the canal will not be used, and that negotiating it during the winter will be very difficult on account of fogs and in the fall of the year on account of high cross winds.",
      "“Small farmers … unable to make a proper defense”",
      "The opponents, too, spoke for others: a chamber of commerce for the small farmers of the south."),
    u(3, CR36 + ", pp. 3845–3846: telegram of E. C. Rolph, president of the First National Bank of Miami, and Senator Vandenberg's conclusion",
      "I think I speak the prevailing sentiment of this entire south Florida area when I say that, in our judgment, the cross-State canal, if completed, will be a calamity. … but it should be suggested to the Senate that there are more people living and more active business south of the proposed canal than north of it, and that the southern portion is almost unanimously opposed to it. If this project were left for decision to the people of Florida, I think it would be overwhelmingly defeated. Mr. President, everything that has been said respecting the merits of the matter suffices, so far as I am concerned, to leave the decision to the conscience of the Senate. I simply remind the Senate, in conclusion, that it is now being asked to approve an enormous appropriation which has been rejected by P. W. A., which has been recommended against by the Department of the Interior, which has been recommended against in the reports of the Department of Commerce, which has been rejected by the House Appropriations Committee, which has been rejected by the House itself, which has had an adverse report by the Senate Appropriations Committee; and now the final decision impends.",
      "“Rejected by P. W. A.”",
      "Vandenberg, senator from Michigan, led the opposition. A Miami banker claims to speak for “the people of Florida”; the six counties on the route had voted 26 to 1 for the land, in an election only of property owners (module 3)."),
    u(4, CR36 + ", p. 3846: Senator Fletcher of Florida",
      "Every waterway association in the country—the Mississippi Valley Association, the Atlantic Deeper Waterways Association, the National Rivers and Harbors Congress—all favor this project and have passed resolutions to that effect. I shall not go into details about that; but, with reference to the water supply, I simply wish to call the attention of the Senate to Senate Document 147, which deals with the subject. It is a report made recently by a board of experts, dated December 18, 1935. Clarence E. Boesch, Sidney Paige, Frank C. Carey, E. B. Burwell, and Malcolm Pirnie were the members of a board of experts on water questions, geology, and so forth, set up by Colonel Somervell, of the Board of Rivers and Harbors Engineers, and instructed to make special examination into this question of the water supply and the effect of the construction of the canal upon it. That report is a Senate document, and I ask Senators to read it. It is mentioned by General Markham in his testimony, in which he said, regarding it: The Board unanimously regards the effects of the sea-level canal as being, using a term, relatively inconsequential. … Senator Vandenberg. You think that the rather generally expressed fears in general and southern Florida are without foundation? General Markham. I think they are wholly without foundation.",
      "“Wholly without foundation”",
      "Duncan U. Fletcher, Florida's senior senator and the canal's oldest advocate in Congress."),
    u(5, CR36 + ", p. 3846",
      "The result was announced—yeas 34, nays 39, as follows: Yeas—34: Bachman, Bailey, Barkley, Benson, Bilbo, Black, Byrnes, Caraway, Connally, Fletcher, George, Glass, Harrison, Hatch, Hayden, Holt, Johnson, Logan, McGill, McKellar, Murray, Neely, Norris, Overton, Pittman, Radcliffe, Reynolds, Robinson, Schwellenbach, Sheppard, Smith, Thomas, Utah, Wagner, Wheeler. … So Mr. Fletcher's amendment was rejected.",
      "34 to 39",
      "The amendment would have given the canal more money in the War Department appropriation bill. The list of the 39 nays and of those absent follows in the Record; it is not printed here. Florida's junior senator, Park Trammell, was absent."),
]

FUNERAL = [
    u(1, "Bradford County Telegraph (Starke), 7 August 1936, p. 1",
      "A mock burial for the cross-state canal put on by the Gainesville Kiwanis Club at Silver Springs recently, shows that folks in that section can see the humorous side of the situation in spite of being bitterly disappointed over the “death” of the project. Congressman R. A. Green, impersonated by a member of the club, took an important part in the proceedings. The “last respects” to the canal, in part, follow: “It is our last sad duty to pay final respects to the only child of one of our sister cities (Ocala). This infant was sired by Washington and damned by South Florida. There was in this child bad blood from the start. It is said that the infant was prematurely born due to fright of a terrible hurricane. Some thought that he would not live, but others thought that he would pull through and not amount to much. “It was the favorite child in Washington, except for TVA. Little Nira was knocked in the head; and little AAA was killed by nine old men. “But there came a time when there was no money, and there could be no more operations to save the baby. It had become emaciated by malnutrition. Perhaps, …”",
      "“Sired by Washington and damned by South Florida”",
      "A joke by the businessmen of Gainesville, north of the route, at Silver Springs, near the cut. The jokes are about New Deal programmes and the Supreme Court. The canal's death is mourned as a loss to the towns, not to the men who had dug it (module 4)."),
]

BOARD = [
    u(1, HD194 + ", p. 6: Board of Engineers for Rivers and Harbors, syllabus, 24 February 1937",
      "The Board of Engineers for Rivers and Harbors finds that a ship canal across the Florida Peninsula of adequate dimensions to pass the large anticipated traffic with reasonable convenience and safety should have a depth of 35 feet, increased to 36 feet in the rock sections, and 37 feet in the Atlantic and Gulf entrances, and a minimum width of 400 feet in the land cuts and of 600 feet in open waters. The estimated expenditure at present costs of labor and materials for the construction of a sea-level canal of these dimensions is $263,838,000, exclusive of rights-of-way to be furnished by local interests, at an estimated cost of $3,000,000. The Board of Engineers for Rivers and Harbors reports that the reasonably assured present and prospective benefits from a canal across Florida do not establish the economic justification for the large expenditures necessary for its construction.",
      "“Do not establish the economic justification”",
      "The Army's own review board, after the work had stopped: not justified."),
    u(2, HD194 + ", p. 17: the Board's findings on ground water",
      "The Board of Engineers for Rivers and Harbors, after due consideration of the facts presented, finds that the construction of a sea-level canal would certainly draw down the ground water in the Ocala limestone adjacent to the canal line. The distance to which the draw-down would extend is dependent upon the unknown courses and capacities of such underground channels through the limestone as might be opened by the canal excavation. The borings made along the canal route show sufficient cavities in the limestone to indicate that many underground channels will in fact be cut, but do not afford any indications of the extent and ramification of these channels under the adjacent lands. With the release of the present pressure of the ground water, a local rise in the underlying salt water is to be expected, with the consequent formation of a ridge or dome of salt water rising to perhaps sea level along the canal line. … By no remote possibility could these effects extend to distant portions of the Florida Peninsula, nor affect the great areas of marsh and swamp which occupy a considerable portion of the State. … This Board is of the opinion that many claims for damage of varying justification must be anticipated if a sea-level canal is constructed.",
      "“A dome of salt water”",
      "Neither side's picture: the Board finds the damage certain near the canal and unknowable in extent, but rules out the ruin of south Florida. The “subterranean stream” Lieutenant Pickell struck on the ridge (module 1) is here a network of cavities in the limestone."),
    u(3, HD194 + ", p. 4: the Chief of Engineers, General E. M. Markham, 1 April 1937",
      "10. I do not share the apprehension expressed in the report of the Board of Engineers, as to the possible adverse effect on ground water supplies, being of the opinion that a sea-level canal will not to any consequential, or vitiative, degree influence the ground water levels of the State, or result in serious intrusion of salt water.",
      "“I do not share the apprehension”",
      "The Chief of Engineers overrules his own board."),
    u(4, HD194 + ", pp. 4–5",
      "14. … They show that, at current prices for materials and labor, with a construction period of 6 years, the canal can be built at a cost to the United States of $197,921,000 and of $3,000,000 to local interests with annual maintenance and operation at $1,090,000. They also show that the annual fixed charges and maintenance and operation expenses against the United States will amount to $8,641,000 and $264,000 to local interests, while the benefits to shipping now in being will be $8,741,000. These figures indicate definitely that the canal would not be, in any sense, a bad investment at the present time. 15. … It appears likely that for a period of years it may be advisable to finance public works with the dual purpose of constructing useful facilities and of employing those who otherwise would require relief. … If the amount to be expended for labor in whole, or in substantial part, is deducted from the capital investment, the canal will show a handsome profit in benefits to shipping. 16. In view of the foregoing considerations, a canal of the basic dimensions stated, viz. 400 by 33 feet, is worthy of favorable consideration as a combination of unemployment relief and of navigation improvement.",
      "“Unemployment relief and navigation improvement”",
      "The sentence that gives the companion game its title. Markham's own figures leave $100,000 a year between charges and benefits; to make the canal pay handsomely, he proposes to count the wages as relief rather than as cost. He lowers the Board's estimate by cutting the depth and the rock costs, and by dropping amortization."),
    u(5, "Hearings on H.R. 6150, House Committee on Rivers and Harbors (April 1937), p. 125: telegrams read by the chairman",
      "One is from Sanford, Fla., from Edward Higgins, mayor: The city commission of Sanford went on record in December of last year by resolution condemning the proposed sea-level ship canal. We are still absolutely opposed to the construction of this canal as it is very probable it would affect the underground waters of Florida which would cause inestimable damage to the principal industry of the State. Here is another one from Winter Park, Fla.: Citizens of Winter Park very much opposed to cross-State sea-level canal on account of possibility of endangering our water supply which comes from deep wells. A recent poll taken by chamber of commerce showed 99 percent against canal. J. K. Moody, Mayor.",
      "Sanford and Winter Park",
      "Towns of central Florida, off the route but on the same ground water. The Winter Park “poll” was taken by its chamber of commerce; how and of whom, the telegram does not say."),
]

LAST = [
    u(1, "Congressional Record, Senate, 17 May 1939, p. 5648",
      "Mr. Chavez. Mr. President, I offer an amendment which I send to the desk. … The Chief Clerk. It is proposed to add, after line 8 on page 2 of the bill, a new section, to read as follows: The canal shall be known and designated as the “Duncan Fletcher Florida Ship Canal.” The amendment was agreed to.",
      "The Duncan Fletcher Florida Ship Canal",
      "The Senate first named the canal after Senator Fletcher."),
    u(2, "Congressional Record, Senate, 17 May 1939, p. 5649",
      "The result was announced—yeas 36, nays 45, as follows: … So the bill S. 1100 was not passed.",
      "36 to 45",
      "Then it refused to build it. Among the yeas were Florida's two senators, Andrews and Pepper; among the nays Vandenberg. The full lists are in the Record."),
]

SRC = ("Congressional Record, Senate, 17 March 1936 and 17 May 1939 (Internet Archive); House Document 194, 75th Congress, 1st Session, "
       "Atlantic-Gulf Ship Canal, Fla. (1937; U.S. Congressional Serial Set, govinfo.gov); Hearings on H.R. 6150, House Committee on Rivers and "
       "Harbors (1937; University of Florida Digital Collections); Bradford County Telegraph, 7 August 1936 (Florida Digital Newspaper Library). "
       "The federal printings are in the public domain; for the newspaper no renewal of copyright has been found.")

T = {
    "id": "aquifer", "titel": "The water under Florida", "jahr": "1934–1939",
    "autor": "Senators, engineers, geologists, mayors, bankers and a Kiwanis club",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission; roll calls are shortened. Much of this module is quotation within quotation: letters and editorials read into the Congressional Record by one side to answer the other. Each passage names who is speaking and through whom. The question itself, whether a sea-level cut through the Ocala limestone would harm the ground water of central and south Florida, was never tested: the canal was stopped before it was cut deep enough.",
    "sections": [
        {"id": "warning", "titel": "No reasonable doubt, or negligible (1934–1936)",
         "blurb": "Would a sea-level cut through the limestone drain the wells of central Florida, or let the sea into them? The President's board of review thought the damage negligible; the federal Geological Survey saw “no reasonable doubt” of serious harm; the Chief of Engineers' own experts found it local. All of it was argued after the digging had begun.",
         "plates": ["hd1937_profile", "cr1936_buckman"], "units": WARNING},
        {"id": "senate", "titel": "South against north (March 1936)",
         "blurb": "In the Senate, Vandenberg of Michigan read the voices of south Florida against the canal: a Miami newspaper, a chamber of commerce, a bank. On 17 March 1936 the Senate refused more money, 34 to 39. In June the House and Senate refused again, and the work stopped.",
         "plates": ["cr1936_miami", "cr1936_vote"], "viz": "aquifer-votes", "units": SENATE},
        {"id": "funeral", "titel": "A funeral at Silver Springs (August 1936)",
         "blurb": "The canal's friends in north Florida buried it in jest: “sired by Washington and damned by South Florida”.",
         "plates": ["bct1936_funeral"], "units": FUNERAL},
        {"id": "board", "titel": "The board and its chief (1937)",
         "blurb": "In 1937 the Army's Board of Engineers found the canal not justified and the damage to ground water certain near the cut, unknowable in extent. The Chief of Engineers overruled it and recommended the canal “as a combination of unemployment relief and of navigation improvement”. Sanford and Winter Park telegraphed their opposition.",
         "plates": ["hd1937_route", "h1937_telegrams"], "units": BOARD},
        {"id": "last", "titel": "Named and refused (1939)",
         "blurb": "On 17 May 1939 the Senate voted to name the ship canal for Senator Fletcher, and then refused to build it, 36 to 45.",
         "plates": ["cr1939_vote"], "units": LAST},
    ],
}
for s in T["sections"]:
    s["zk"] = "The water under Florida, " + re.sub(r" \(.*", "", s["titel"])
(D / "aquifer.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
CRP = "Congressional Record; Internet Archive; public domain."
SER = "U.S. Congressional Serial Set, scan of govinfo.gov; public domain."
NEW = [
    {"id": "hd1937_profile", "side": "water", "titel": "Profile along route 13-B, 1937",
     "caption": "The Army engineers' profile of the western half of the route, from the Gulf past Dunnellon, Santos and Silver Springs Run: ground surface, hydraulic gradient, and the top of the Ocala limestone the cut would open (hatched).",
     "source": HD194 + ", annex 5, plate 17, detail. " + SER},
    {"id": "cr1936_buckman", "side": "water", "titel": "The ground-water record, as the canal's engineer told it",
     "caption": "Buckman's statement in the Congressional Record: the board of review's “negligible”, the State geologist's 40 feet, and the Geological Survey's “no reasonable doubt”.",
     "source": CR36 + ", p. 3842, right column. " + CRP},
    {"id": "cr1936_miami", "side": "water", "titel": "Miami against the canal, 1936",
     "caption": "The Miami Daily News and the president of the Miami Chamber of Commerce, read into the Record by Senator Vandenberg.",
     "source": CR36 + ", p. 3845, right column. " + CRP},
    {"id": "cr1936_vote", "side": "capitol", "titel": "34 to 39, 17 March 1936",
     "caption": "Vandenberg's list of rejections, Fletcher's appeal to Senate Document 147, and the roll call.",
     "source": CR36 + ", p. 3846, left column. " + CRP},
    {"id": "bct1936_funeral", "side": "water", "titel": "A mock burial at Silver Springs, 1936",
     "caption": "“This infant was sired by Washington and damned by South Florida.”",
     "source": "Bradford County Telegraph (Starke), 7 August 1936, p. 1; Florida Digital Newspaper Library, University of Florida; no copyright renewal found."},
    {"id": "hd1937_route", "side": "survey", "titel": "Sea-level route 13-B, 1937",
     "caption": "The Board of Engineers' map of the ship canal from the St. Johns at Jacksonville by Palatka, the Ocklawaha, Silver Springs, Ocala and Dunnellon to the Gulf at Inglis, with its profile and a map of the Gulf and Atlantic coasts.",
     "source": HD194 + ", map dated 24 February 1937. " + SER},
    {"id": "h1937_telegrams", "side": "water", "titel": "Telegrams from Sanford and Winter Park, 1937",
     "caption": "“Very probable it would affect the underground waters of Florida”; “99 percent against canal”.",
     "source": "Hearings on H.R. 6150, House Committee on Rivers and Harbors (1937), p. 125; University of Florida Digital Collections; public domain."},
    {"id": "cr1939_vote", "side": "capitol", "titel": "36 to 45, 17 May 1939",
     "caption": "“So the bill S. 1100 was not passed.”",
     "source": "Congressional Record, Senate, 17 May 1939, p. 5649, detail; Internet Archive; public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "aquifer"), None) or next(x for x in M["shipped"] if x["id"] == "aquifer")
M["planned"] = [x for x in M["planned"] if x["id"] != "aquifer"]
m.update({"datei": "aquifer", "zk": "Warning · Senate · Funeral · Board · 1939",
          "kurz": "5 · The water under Florida",
          "warum": "The Geological Survey saw “no reasonable doubt” of harm to the ground water; the Army's experts saw it local. South Florida spoke through Miami's newspaper, chamber and bank; the Senate refused money in 1936 (34 to 39) and the canal in 1939 (36 to 45). The Army's own board found the canal unjustified; its chief recommended it as relief.",
          "quelle": "Congressional Record 1936 and 1939; House Document 194, 75th Congress (1937); House hearings 1937; Bradford County Telegraph 1936."})
order = ["ridge", "river", "relief", "camp", "aquifer", "war", "rodman", "undoing"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "aquifer"] + [m], key=lambda x: order.index(x["id"]))
for x in M["missing"]:
    if x["id"] == "sdoc147":
        x["warum"] = "The report of the board of experts on ground water (18 December 1935; Boesch, Paige, Carey, Burwell, Pirnie), printed as Senate Document 147, 74th Congress, is cited by Senator Fletcher and the Chief of Engineers but not yet found in a reachable scan. Its findings appear here only in their words."
ADD = [{"id": "june1936", "side": "capitol", "kurz": "The votes of June 1936",
        "warum": "The final refusals of money in the House and Senate in June 1936, which stopped the work, are known here only from a newspaper report (module 4); the Congressional Record of those days has not yet been read.",
        "quelle": "Congressional Record, June 1936."},
       {"id": "sharp1935", "side": "water", "kurz": "Henry S. Sharp's findings (1935)",
        "warum": "The Columbia geologist's articles in the Miami Daily News are known only from the editorial read into the Record; the newspaper of 1935 is not in the collections reached and its rights are unchecked.",
        "quelle": "Miami Daily News, March 1935."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "groundwater", "titel": "The water under the cut",
     "frage": "Would a sea-level canal harm Florida's ground water?",
     "note": "The Geological Survey in 1935: “no reasonable doubt” of serious harm in a wide zone. The Chief of Engineers in 1936: “will not contaminate”. His own board in 1937: certain draw-down near the canal, a dome of salt water, extent unknown, no harm to distant parts. The Chief in 1937: “I do not share the apprehension.”",
     "voices": [{"text": "aquifer", "sec": "warning", "n": [3], "wer": "Geological Survey, 1935"},
                {"text": "aquifer", "sec": "board", "n": [2], "wer": "Board of Engineers, 1937"},
                {"text": "aquifer", "sec": "board", "n": [3], "wer": "Chief of Engineers, 1937"}]},
    {"id": "voice", "titel": "Who speaks for Florida?",
     "frage": "Whose Florida wanted the canal, and whose did not?",
     "note": "A Miami banker spoke for “the people of Florida” and a chamber of commerce for south Florida's “small farmers”; the six counties on the route had voted for the land, but only their property owners could vote. Neither side counted those who had no voice in either.",
     "voices": [{"text": "aquifer", "sec": "senate", "n": [2, 3], "wer": "Miami, read by Senator Vandenberg, 1936"},
                {"text": "relief", "sec": "bonds", "n": [2], "wer": "Representative W. J. Sears, 1936"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/aquifer/"
for s in TL["stations"]:
    if s["titel"] == "34 to 39":
        s.update({"cite": K + "senate/5", "citeLabel": "The water under Florida, 1936 [5]", "plate": "cr1936_vote"})
    if s["titel"] == "A funeral at Silver Springs":
        s.update({"cite": K + "funeral/1", "citeLabel": "The water under Florida, 1936 [1]", "plate": "bct1936_funeral"})
    if s["titel"] == "36 to 45":
        s.update({"cite": K + "last/2", "citeLabel": "The water under Florida, 1939 [2]", "plate": "cr1939_vote"})
NEWST = [
    {"d": "26 August 1935", "side": "water", "titel": "“No reasonable doubt”",
     "text": "The Geological Survey warns, through the Interior Department, that a sea-level canal would seriously harm the ground water of the Ocala limestone in a wide zone.",
     "cite": K + "warning/3", "citeLabel": "The water under Florida, 1935 [3]", "plate": "cr1936_buckman",
     "quelle": "Congressional Record, Senate, 17 March 1936, p. 3842."},
    {"d": "24 February 1937", "side": "survey", "titel": "Not justified",
     "text": "The Army's Board of Engineers for Rivers and Harbors finds a ship canal across Florida not economically justified, at $263,838,000; the Chief of Engineers overrules it in April and recommends it as relief and navigation.",
     "cite": K + "board/1", "citeLabel": "The water under Florida, 1937 [1]", "plate": "hd1937_route",
     "quelle": "House Document 194, 75th Congress, 1st Session, pp. 4–6."},
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
