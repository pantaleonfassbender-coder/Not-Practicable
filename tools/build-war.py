"""Builds data/war.json (module 6: A canal for the war, 1941–1945) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/war/PRUEFUNG.md):
  Sanford Herald, 16 January 1942, p. 2 (UFDC AA00087662/07123, plate only); Sanford Herald, 6 February 1941, 16 April 1942, 23 February 1943, 2 April 1943, all p. 2
    (UFDC AA00087662/06835, /07196, /07414, /07442);
  Congressional Record, House, 1 June 1942, pp. 4773–4774 (Internet Archive PL77711, leaves n22–n23,
    pages bound into the USDA legislative history of Public Law 77-711);
  Act of 23 July 1942, chapter 520, 56 Stat. 703 (govinfo STATUTE-56-Pg703);
  House Report 2, 79th Congress, 1st Session, 8 January 1945 (govinfo SERIALSET-10931_00_00-003-0002-0000).
Rights: federal printings in the public domain; for the Sanford Herald of 1941–43 no renewal of copyright found.
Run from the site root: python tools/build-war.py
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


CR = "Congressional Record, House, 1 June 1942"
SH = "Sanford Herald"

DEFENCE = [
    u(1, SH + ", 6 February 1941, p. 2",
      "Florida Senators Term Ship Canal Vital To Defense. Washington, Feb. 6—(Special)—Describing the Florida ship canal as a “vital element in our defense,” Senators Andrews and Pepper will urge Congress to enact legislation providing for its immediate construction and prompt completion. “In the event of United States' involvement in a war in this hemisphere,” they said, “the navy would have a difficult and hazardous task in protecting shipping in the Florida straits between the Caribbean Sea and the Gulf of Mexico.” The new canal bill will call for a sea-level canal, 33 feet deep, 400 feet wide in the Ocala cut, and 600 feet wide in the approaches and in the St. Johns, Oklawaha and Withlacoochee Rivers. The estimated cost is $160,000,000. … While they were satisfied that no basis existed for fears that water supply of South Florida would be endangered, the senators said, their bill would contain a provision “for the building of any control works which our Army engineers may deem advisable …”",
      "“A vital element in our defense”",
      "Before the United States entered the war, the ship canal comes back with a new reason. The plan is still the sea-level canal of 1937, with a clause for works to calm the fears about ground water (module 5)."),
]

DEBATE = [
    u(1, CR + ", p. 4773: a Representative from Florida (his name stands on p. 4772, not in the scan)",
      "In my first campaign for election to Congress more than 18 years ago, I promised the people of Florida to work for a canal across north Florida connecting up this intracoastal system; … Today, I am about to realize, I hope, the success of this 18 years of constant effort for an improvement which will be of tremendous peacetime economic value, and which at the moment is an absolute war essential. … I am thinking today of the almost daily occurring submarine tragedies on our Atlantic—particularly the lower Atlantic and Gulf areas. The blood of many hundreds of Americans has been spilled in this area by ruthless and savage attacks by enemy submarines. Millions of dollars' worth of cargoes—primarily oil—have been destroyed. Thousands of you who are inclined not to support this bill will bear in mind that these lives of our American people and these war-essential cargoes destroyed are worth far more in the protection of our great Nation than are financial investments.",
      "“Submarine tragedies”",
      "The speaker says “enemy submarines”; they were German. The Sanford Herald had reported on 16 January 1942: “An American tanker has been sunk by a German submarine just 60 miles outside New York harbor” (plate). Modern accounts call the German submarine campaign off the American coast, begun in January 1942, Operation Drumbeat (Paukenschlag). The speaker names no figures for the ships and lives lost. The bill, H.R. 6999, joined a barge canal across Florida to an oil pipeline and a deeper Gulf Intracoastal Waterway. The speaker also complains that the Republican members of the committee yielded time only to opponents."),
    u(2, CR + ", p. 4773: Representative Carter of California",
      "Mr. Carter. Mr. Speaker, I call the attention of the House to the fact that this bill was never submitted to the Bureau of the Budget, that it does not have the approval of the War Production Board, that it is brought in here with undue haste under a motion to suspend the rules … Mr. Speaker, this bill has been referred to as a boondoggling bill in an editorial in the Miami Herald in the State of Florida. I do not want this Congress to make itself ridiculous by passing a measure that has been said by somebody to be the beginning of the old Florida ship canal. We must conserve our financial resources to carry on the war and cut out all nonessential expenditures.",
      "“A boondoggling bill”",
      "Florida's own south again, through a Miami newspaper, as in 1936."),
    u(3, CR + ", pp. 4773–4774: Representative Mansfield of Texas",
      "Mr. Speaker, the question of the ship canal across Florida has been raised. I hold in my hand a minority report, which I made against that proposition, signed by myself and nine other members of the committee … They all signed it, in opposition to a ship canal across Florida, more than a year ago, long before this question here before us was ever raised. There is no ground or reason or argument for a ship canal there. … The bill here as proposed does not go to the ocean at either end. It only connects up the two shallow barge canal channels, 12 feet deep. … Several gentlemen from Florida, all of them, in fact, are in favor of a ship canal, if you will put it to their door. They have annoyed the life out of me for 6 years to get it to run here or there, but when you propose to put it across where the engineers say is the most practical place to put it, they object.",
      "“There is no ground or reason”",
      "The ship canal becomes a barge canal: twelve feet deep instead of thirty, to carry oil and other cargo inland, out of the submarines' reach, from Texas to the East."),
    u(4, CR + ", p. 4774",
      "Mr. Rankin of Mississippi. It was testified before the committee that it would supply 1,600,000 barrels of oil a day on the Atlantic coast. This short canal across Florida, when completed, in connection with the barge canal, would supply the entire amount, and it is the only proposition that has been proposed that will supply it. Mr. Mansfield. The gentleman is correct. Mr. Michener. … Now, who has asked for this legislation as presented? Mr. Mansfield. Millions of people all over the United States, both in the East and the West. Down in my State we have so much oil and gasoline that we cannot dispose of it. Up in the East they are rationed and still suffering for the need of it. Mr. Michener. Yes; I know, but I am asking who appeared before the committee? In other words, is the War Department asking for this as a national defense measure? Is the Navy asking for it? Is the administration asking for it, or is the War Production Board asking for it? …",
      "“Who has asked for this legislation?”",
      "Oil was the new argument: gasoline was rationed in the East. Michener's question, who in the war effort had asked for the canal, gets no answer before the time runs out."),
    u(5, CR + ", p. 4774",
      "The Speaker. The gentleman's time has expired. All time has expired. The question is, Will the rules be suspended and the bill passed? The question was taken; and on a division (demanded by Mr. Dingell) there were ayes 85 and noes 121. … So, two-thirds not having voted in favor thereof, the motion to suspend the rules and pass the bill was rejected.",
      "85 to 121",
      "The first attempt fails. Seven weeks later the bill became law (next section); the votes by which it then passed have not yet been read in the Record."),
]

ACT = [
    u(1, "Act of 23 July 1942, ch. 520, 56 Stat. 703 (Public Law 675, 77th Congress, H.R. 6999)",
      "An Act To promote the national defense and to promptly facilitate and protect the transport of materials and supplies needful to the Military Establishment by authorizing the construction and operation of a pipe line and a navigable barge channel across Florida, and by deepening and enlarging the Intracoastal Waterway from its present eastern terminus to the vicinity of the Mexican border. Be it enacted … That, in order to promote the national defense and to promptly facilitate and protect the transport of materials and supplies needful to the Military Establishment, there is hereby authorized to be constructed under the direction of the Secretary of War and the supervision of the Chief of Engineers a high-level lock barge canal from the Saint Johns River across Florida to the Gulf of Mexico in accordance with the plans set forth in the letter of the Chief of Engineers dated June 15, 1942; … And provided further, That … there is authorized to be constructed one or more pipe lines, together with all necessary terminal facilities, for the transport of petroleum and its products, from the vicinity of Port Saint Joe and other points on the Gulf Coast of Florida to the Saint Johns River … Sec. 2. There is hereby authorized to be appropriated the sum of $93,000,000 to carry out the provisions of this Act. Approved, July 23, 1942.",
      "A high-level lock barge canal",
      "The law that authorized the canal until 1990. A “high-level lock” canal: no deep cut into the limestone, and so no quarrel over the ground water. Authorized is not appropriated: the act allows Congress to spend $93,000,000; it does not spend it."),
    u(2, "House Report 2, 79th Congress, 1st Session, 8 January 1945",
      "On July 31, 1942, the Secretary of War transmitted a report from the Chief of Engineers, United States Army, dated June 12, 1942, together with accompanying papers and an illustration submitting a review of reports on the Atlantic-Gulf ship canal, Fla., … Accompanying this letter of transmittal, was a memorandum to the Speaker of the House of Representatives requesting that, as the accompanying report contains information affecting the national defense of the United States, it be read only in executive session and that it not be printed during the emergency. This request was complied with and the report was referred to the Committee on Rivers and Harbors without printing. On November 10, 1944, the Secretary of War transmitted another letter to the Speaker of the House, … advising that the confidential classification which accompanied the first letter of the Secretary of War has been removed … The purpose of this resolution is to comply with the suggestion of the Secretary of War and print the entire correspondence as a House document, which the Public Printer estimates will cost approximately $101.08.",
      "A secret report",
      "The engineers' review of June 1942 was kept from print until 1945, after the law it supported had been passed. The report itself (House Document 109, 79th Congress) has not yet been found; see Texts, “Examined and not included”."),
]

MONEY = [
    u(1, SH + ", 16 April 1942, p. 2",
      "According to President Roosevelt, the cross state canal is out for the duration. But that project has been out so many times before, we must expect to see it rise again.",
      "“Out for the duration”",
      "A note in the Sanford paper's editorial column, three months before the act. What exactly the President said, and where, the note does not tell."),
    u(2, SH + ", 23 February 1943, p. 2: editorial",
      "Sanford's opposition to the cross state canal from Yankeetown to Palatka has been based solely on the assumption that it would be a sea level canal cut through the Ocala limestone through which the artesian wells of this section are fed, thus lowering the water table to such an extent, or contaminating it with salt water, that our farmers and citrus growers would be at the mercy of a somewhat uncertain rainfall. But if the cross state canal is to be a lock canal including five locks, thus limiting the depth which it will have to be sunk into the limestone and carefully sealing the porous rock so that salt cannot seap into the subterranean veins which carry our underground water to us and if other adequate safety precautions are taken so that all danger to our farms and groves are removed, we can see no reason whatever why the people of this section would oppose its construction … Certainly the people of this section are not disposed to fight the cross state canal simply because it means something to Ocala or some other part of the state …",
      "Sanford changes its mind",
      "The barge canal with locks took away the argument of 1935–37. The editorial is set in a page about Senator Pepper's plan for a network of Florida waterways that would also serve Sanford."),
    u(3, SH + ", 2 April 1943, p. 2",
      "The House Appropriations Committee cut the cross state canal and the $44,000,000 for its construction from a War Department bill, declaring that it would be so long before the canal could possibly be built that it would be of no help whatever in solving the oil problem for the eastern seaboard. We may expect, however, that the canal, as it has had a habit of doing for the past ten years, will bob up again when the bill makes its appearance on the floor of the House.",
      "“Of no help whatever”",
      "The war argument turned against the canal: too slow to help in this war. No money for construction followed during the war; the next works began in 1964 (module 7)."),
]

SRC = ("Sanford Herald, 6 February 1941, 16 April 1942, 23 February and 2 April 1943 (Florida Digital Newspaper Library, University of Florida); "
       "Congressional Record, House, 1 June 1942 (Internet Archive); Act of 23 July 1942, 56 Stat. 703, and House Report 2, 79th Congress (1945) "
       "(govinfo.gov). The federal printings are in the public domain; for the newspaper no renewal of copyright has been found.")

T = {
    "id": "war", "titel": "A canal for the war", "jahr": "1941–1945",
    "autor": "Florida's senators, the House of Representatives, the Army's engineers and a Sanford newspaper",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. The pages of the Congressional Record of 1 June 1942 survive here only because they were bound, by chance, into another bill's legislative history; the speaker of the first passage is named on the preceding page, which is not in the scan. The final votes on the bill in July 1942 and the engineers' report of June 1942 have not yet been read.",
    "sections": [
        {"id": "defence", "titel": "Vital to defence (1941)",
         "blurb": "In February 1941 Florida's senators brought the ship canal back as “a vital element in our defense”: the Navy would find it hard to protect shipping in the Florida Straits in a war.",
         "plates": ["sh1941_defense"], "viz": "war-reasons", "units": DEFENCE},
        {"id": "debate", "titel": "Submarines and oil (June 1942)",
         "blurb": "With German submarines sinking tankers off the coast and gasoline rationed in the East, a barge canal and an oil pipeline across Florida came before the House. A Florida member spoke of the “blood of many hundreds of Americans”; a Californian quoted a Miami paper's “boondoggling bill”. The first vote failed, 85 to 121.",
         "plates": ["sh1942_tanker", "cr1942_submarines", "cr1942_vote"], "units": DEBATE},
        {"id": "act", "titel": "Authorized, not built (July 1942)",
         "blurb": "On 23 July 1942 Congress authorized “a high-level lock barge canal” across Florida and $93,000,000. The engineers' report behind it was kept secret until 1945.",
         "plates": ["stat1942_act", "hrept1945_secret"], "units": ACT},
        {"id": "money", "titel": "No money (1942–1943)",
         "blurb": "No construction money followed. Sanford, which had fought the sea-level canal over its wells, said it would not oppose a canal with locks; in 1943 the House Appropriations Committee struck $44,000,000 for the canal as too slow to help the war.",
         "plates": ["sh1942_duration", "sh1943_sanford", "sh1943_cut"], "units": MONEY},
    ],
}
for s in T["sections"]:
    s["zk"] = "A canal for the war, " + re.sub(r" \(.*", "", s["titel"])
(D / "war.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
NP = "Florida Digital Newspaper Library, University of Florida; no copyright renewal found."
NEW = [
    {"id": "sh1941_defense", "side": "capitol", "titel": "“Vital to defense”, February 1941",
     "caption": "Senators Andrews and Pepper ask for a sea-level ship canal for $160,000,000.",
     "source": SH + ", 6 February 1941, p. 2; " + NP},
    {"id": "sh1942_tanker", "side": "capitol", "titel": "“Sunk by a German submarine”, January 1942",
     "caption": "“An American tanker has been sunk by a German submarine just 60 miles outside New York harbor.”",
     "source": SH + ", 16 January 1942, p. 2; " + NP},
    {"id": "cr1942_submarines", "side": "capitol", "titel": "“Submarine tragedies”, 1 June 1942",
     "caption": "A Florida member of the House for the barge canal: “The blood of many hundreds of Americans has been spilled in this area by ruthless and savage attacks by enemy submarines.”",
     "source": CR + ", p. 4773, middle column; Internet Archive; public domain."},
    {"id": "cr1942_vote", "side": "capitol", "titel": "85 to 121, 1 June 1942",
     "caption": "Mansfield, Rankin and Michener on oil and the canal; then the division: ayes 85, noes 121.",
     "source": CR + ", p. 4774, middle column; Internet Archive; public domain."},
    {"id": "stat1942_act", "side": "capitol", "titel": "The act of 23 July 1942",
     "caption": "“A high-level lock barge canal from the Saint Johns River across Florida to the Gulf of Mexico”, a pipeline, the Intracoastal Waterway, and $93,000,000.",
     "source": "56 Stat. 703 (1942), chapter 520; U.S. Statutes at Large, govinfo.gov; public domain."},
    {"id": "hrept1945_secret", "side": "capitol", "titel": "Not to be printed during the emergency",
     "caption": "House Report 2 of January 1945 on the Chief of Engineers' report of June 1942, withheld from print as “information affecting the national defense”.",
     "source": "House Report 2, 79th Congress, 1st Session (1945); U.S. Congressional Serial Set, govinfo.gov; public domain."},
    {"id": "sh1942_duration", "side": "capitol", "titel": "“Out for the duration”, April 1942",
     "caption": "“According to President Roosevelt, the cross state canal is out for the duration.”",
     "source": SH + ", 16 April 1942, p. 2; " + NP},
    {"id": "sh1943_sanford", "side": "water", "titel": "Sanford and a canal with locks, 1943",
     "caption": "The Sanford Herald: the town's opposition rested “solely” on the fear of a sea-level cut through the Ocala limestone.",
     "source": SH + ", 23 February 1943, p. 2, detail; " + NP},
    {"id": "sh1943_cut", "side": "capitol", "titel": "$44,000,000 struck, April 1943",
     "caption": "The House Appropriations Committee cuts the canal from a War Department bill: “of no help whatever in solving the oil problem”.",
     "source": SH + ", 2 April 1943, p. 2; " + NP},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "war"), None) or next(x for x in M["shipped"] if x["id"] == "war")
M["planned"] = [x for x in M["planned"] if x["id"] != "war"]
m.update({"datei": "war", "zk": "Defence · Submarines · Act · Money",
          "kurz": "6 · A canal for the war",
          "warum": "In 1941 the ship canal was “vital to defense”; in 1942, with German submarines sinking tankers and gasoline rationed, it became a barge canal for oil. A first vote failed, 85 to 121; on 23 July 1942 Congress authorized a lock barge canal and $93,000,000, on a report kept secret until 1945. No construction money followed.",
          "quelle": "Sanford Herald 1941–1943; Congressional Record, 1 June 1942; Act of 23 July 1942 (56 Stat. 703); House Report 2, 79th Congress (1945)."})
order = ["ridge", "river", "relief", "camp", "aquifer", "war", "rodman", "undoing"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "war"] + [m], key=lambda x: order.index(x["id"]))
ADD = [{"id": "july1942", "side": "capitol", "kurz": "The votes of July 1942",
        "warum": "How H.R. 6999 passed House and Senate in July 1942, after failing on 1 June, has not yet been read in the Congressional Record (about p. 6231).",
        "quelle": "Congressional Record, July 1942."},
       {"id": "pipeline", "side": "capitol", "kurz": "The pipeline across Florida",
        "warum": "Whether the oil pipeline authorized with the canal in 1942 was built, and where, is not documented in the sources read.",
        "quelle": "Petroleum Administration for War; Corps of Engineers annual reports 1942–45."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "warreason", "titel": "War as a reason, 1826 and 1942",
     "frage": "How did war argue for a canal across Florida?",
     "note": "Florida's delegate in 1826 wanted “one connected chain of internal communication” in case of war; a Florida member of the House in 1942 spoke of tankers sunk by submarines. A century apart, the same argument: shipping kept inside the land is safe from an enemy at sea.",
     "voices": [{"text": "ridge", "sec": "senate", "n": [5], "wer": "Joseph M. White, 1826"},
                {"text": "war", "sec": "debate", "n": [1], "wer": "A Representative from Florida, 1942"}]},
    {"id": "sanford", "titel": "Sanford, 1937 and 1943",
     "frage": "Was central Florida against any canal, or against a certain canal?",
     "note": "In 1937 Sanford's mayor telegraphed that the city was “absolutely opposed” to the sea-level canal for fear for its ground water. In 1943 the town's paper wrote that a lock canal sealed against the limestone would give no reason for opposition.",
     "voices": [{"text": "aquifer", "sec": "board", "n": [5], "wer": "Mayors of Sanford and Winter Park, 1937"},
                {"text": "war", "sec": "money", "n": [2], "wer": "Sanford Herald, 1943"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/war/"
for s in TL["stations"]:
    if s["titel"] == "A barge canal for the war":
        s.update({"cite": K + "act/1", "citeLabel": "A canal for the war, 1942 [1]", "plate": "stat1942_act",
                  "text": "Congress authorizes “a high-level lock barge canal from the Saint Johns River across Florida to the Gulf of Mexico”, a pipeline, and $93,000,000. No construction money follows during the war."})
NEWST = [
    {"d": "1 June 1942", "side": "capitol", "titel": "Submarines, oil, and 85 to 121",
     "text": "The House debates a barge canal and pipeline across Florida as a war measure against the submarines; under suspension of the rules the bill fails, 85 to 121.",
     "cite": K + "debate/5", "citeLabel": "A canal for the war, 1942 [5]", "plate": "cr1942_vote",
     "quelle": "Congressional Record, House, 1 June 1942, pp. 4773–4774."},
    {"d": "2 April 1943", "side": "capitol", "titel": "$44,000,000 struck",
     "text": "The House Appropriations Committee cuts the canal from a War Department bill as too slow to help with the oil problem of the East.",
     "cite": K + "money/3", "citeLabel": "A canal for the war, 1943 [3]", "plate": "sh1943_cut",
     "quelle": "Sanford Herald, 2 April 1943, p. 2."},
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
