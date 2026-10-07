"""Builds data/camp.json (module 4: Camp Roosevelt, 1935–1936) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/camp/PRUEFUNG.md):
  Federal Writers' Project, American Guide, Marion County (typescript, Jacksonville 1936), folios 81 and 91
    (UFDC AA00106063/00001, images 00093, 00103);
  Citrus County Chronicle (Inverness), 12 September 1935, p. 4, and 19 September 1935, p. 1
    (UFDC UF00028315/06862, /06863);
  Madison Enterprise-Recorder, 20 September 1935, p. 10 (UFDC UF00028405/02018);
  Florida State Board of Health, Thirty-sixth Annual Report (1935), pp. 36, 55 (Internet Archive annualreportstat1935flor);
  Documentary History of the Florida Canal (Senate Document 275, 74th Congress, 1936), pp. ii–iv, vi, 389
    (UFDC UF00055183/00001);
  Hearings on H.R. 6150, House Committee on Rivers and Harbors (1937), pp. 17, 466–467 (UFDC UF00018663/00001);
  Sanford Herald, 3 March, 3 April, 19 June and 8 July 1936 (UFDC AA00087662/05133, /05160, /05225, /05240).
Rights: federal works (FWP typescript, congressional printings) and Florida state reports are in the public domain;
for the Florida newspapers of 1935–36 no renewal of copyright has been found (not checked in the renewal records).
Run from the site root: python tools/build-camp.py
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


DH = "Documentary History of the Florida Canal (Senate Document 275, 74th Congress, 1936)"
HR = "House hearings on H.R. 6150, April 1937"
SBH = "Florida State Board of Health, Thirty-sixth Annual Report, for the year 1935"

START = [
    u(1, "Citrus County Chronicle (Inverness), 12 September 1935, p. 4",
      "Just Like Boom Days. The biggest development to hit this section of Florida since boom days is the cross-state canal project, work on which has actually begun following the allocation of $5,000,000 last week by President Roosevelt to start preliminary construction. Ocala, operations headquarters for the gigantic undertaking, is already assuming a boom-time aspect and is buzzing with activity as hundreds of job hunters swarm over the town and as the big headquarter's camp is being constructed just out of the city. … Col. Brehon B. Somervell, army engineer who has charge of building “the world's greatest canal,” has announced that employment on the project would be done under the WPA with eligible men to be certified by the National Re-employment service offices. Labor will be chosen as near as possible from the section near by the canal, those who can subsist themselves and live at home being given preference.",
      "“Hundreds of job hunters”",
      "The “boom days” are those of the Florida land boom of the 1920s, which ended in collapse. Preference was to go to men who lived near the canal and could keep themselves at home; the camp was for the others."),
    u(2, "Madison Enterprise-Recorder, 20 September 1935, p. 10",
      "… a crew of 100 men labored with axe and shovel September 14 breaking the first ground in construction of the Florida canal. … Col. Somervell, who 17 years ago was building railroads near the front in France, chopped down the first tree on the right-of-way. Slightly more than 1750 men labored at Camp Roosevelt, central construction camp a mile and a half south of Ocala. Col. Somervell said Monday a crew of 200 additional men would be placed at work digging and six crews of 120 men each would start clearing right-of-way. The canal chief said by Christmas all the $500,000 set aside for housing would be spent, and that more would be asked.",
      "Axe and shovel",
      "The beginning of the work has three dates in the sources: 3 September (the order, module 3), 14 September (the first ground broken, here) and 19 September (the ceremony, [3]). The 1,750 men at Camp Roosevelt were building the camp itself."),
    u(3, "Federal Writers' Project, Marion County (typescript, 1936), “Ocala”, folio 81",
      "Formal opening of the excavation of the Florida Gulf-Atlantic Ship Canal, at a point near Ocala, occurred September 19, 1935, when at one o'clock p. m., President Roosevelt, at his Hyde Park home, pushed the button that set off a heavy charge of dynamite. By October 1st, 3000 men were employed. The work is directed by Lt. Col. Brehon Somervall, Chief Engineer of Canals.",
      "A button at Hyde Park",
      "Written by the Federal Writers' Project, itself a relief programme, for the American Guide. The typescript spells the engineer's name “Somervall”."),
    u(4, "Citrus County Chronicle (Inverness), 19 September 1935, p. 1",
      "All Workers Are Hired on Recommendations of Re-employment Office. Citrus county's unemployed are already being benefitted by construction of the Atlantic-Gulf ship canal across Florida, on which actual digging got under way Sunday a few miles out of Ocala. H. T. Ashley, manager of the National Re-employment service's office here, said yesterday that already more than 20 carpenters and brick masons from this county have been given employment on the project, which is being pushed vigorously by United States army engineers. Although this number is only a small percentage of Citrus county's unemployed, every jobless man in this and surrounding counties is expected to land a position with the canal project when construction work reaches its peak. Already more than 1000 men are at work in the Ocala area and a total of 7000 will be on the job in less than four months, high ranking army officials have announced.",
      "“Every jobless man”",
      "The promise of the canal in one county newspaper: work for every jobless man of the surrounding counties. Women are not mentioned."),
]

CAMP = [
    u(1, SBH + ", p. 36: “Camp Roosevelt and Canal Zone Sanitation”",
      "Sanitation in connection with Camp Roosevelt and other construction camps installed in the cross-state Canal zone area has been a matter of utmost importance to the Bureau. Before adequate plans had been made for necessary sanitary facilities in these camps, the workers began to arrive and measures to handle the situation required prompt action on the part of the State Board of Health. As a result it was necessary for our District Sanitary Officer stationed in Ocala to spend practically all of his time during September and early October working with the camp officials to devise ways and means to handle a situation made serious by a dual problem—absence of proper sanitary facilities and inadequate protection of food and the sanitary preparation of same.",
      "“Before adequate plans had been made”",
      "The men came faster than the latrines. What the “serious” situation meant for those living in the camps, illness or not, the report does not say."),
    u(2, SBH + ", p. 36",
      "The matter of safe water supply, was one that gave much real concern. As is the case with new well installations, where materials used are not properly sterilized previous to use; examinations on samples collected indicated poor sanitary quality. This prevented approval of the several deep wells immediately following completion and in some instances it was several weeks before results were obtained that would permit the Bureau to pass favorably upon these supplies. Upon recommendation of the Bureau, officials at the camp arranged to have the main supply subjected to chlorination and by the close of the year all supplies were giving constant, satisfactory results.",
      "Water of poor quality",
      "For several weeks the camp's new wells had not passed the state's tests."),
    u(3, SBH + ", p. 55: table of the public health nursing service, “Corrections”",
      "[Corrections:] White, Colored. … Canal Workers Examination 56, 3.",
      "White 56, Colored 3",
      "The last line of a table of the state's public health nurses: 59 examinations of canal workers in 1935, counted by colour. It shows that the state's health service kept its records by race; it does not show how the camps or the crews were divided, nor how many of the canal's workers were Black. What “examination” covered here is not explained."),
]

WORK = [
    u(1, DH + ", p. vi: bulletin of the Ship Canal Authority, 1 June 1936",
      "Present status (June 1, 1936): Length of central cut excavated (approximate) … miles 10. Yardage removed (approximate) … cubic yards 17,000,000. Bridges: Piers of first bridge substantially complete. Other structures: Headquarters and other camps complete. Other work: Clearing on central cut section complete. Expended to date (approximate) … $5,000,000. Men now employed (approximate) … 6,000.",
      "Ten miles in nine months",
      "The canal authority's own figures, published to win more money. The same page gives the total excavation planned as 571,000,000 cubic yards: what had been moved was about three per cent."),
    u(2, DH + ", p. 389: Representative W. J. Sears before a House Appropriations subcommittee, 17 April 1936",
      "There are now 6,000 people employed on the canal, 90 percent of whom were taken from the relief rolls. They allowed contractors 10 percent not on relief rolls, because the contractors had to take with them certain men who had been with them for years. The men are doing real work, and you are getting dollar for dollar for the work. If $12,000,000 is appropriated, the result will be that 10,000 more people in Florida will come off the relief rolls and begin digging the canal.",
      "“Taken from the relief rolls”",
      "Nine in ten from relief, one in ten the contractors' own men. Wages and hours are not given in any source read so far."),
    u(3, "Federal Writers' Project, Marion County (typescript, 1936), folio 91",
      "The estimated cost of the canal is $143,000,000, exclusive of the land, which is being furnished by local interests. It is now expected that the canal will be completed within six years, providing funds are available at the rate sufficient to permit work in the most economical manner. Approximately 6,000 men began work on the project, the largest single labor project in the United States. It is estimated that 20,000 will be employed at the peak of operation.",
      "“The largest single labor project”",
      "A claim made in the spring of 1936; no source checks it against other relief works of the time."),
    u(4, HR + ", p. 17: General E. M. Markham, Chief of Engineers",
      "Mr. Culkin. General, suppose it is treated as a work-relief project, what would be the added cost of it? General Markham. I doubt if anything would be added, providing the work were not complicated by what would ordinarily be the relief regulations. For example, I think that, if they went forward with the common labor obtained from relief rolls, the cost would be all right. Complications come with the regulations or the class and character of operators. They would have to get into this vast affair from relief, under regulations which would increase the cost in amounts which we could not estimate at this time.",
      "“Common labor obtained from relief rolls”",
      "In 1937, after the stop, the Chief of Engineers wanted the work as contract work: relief labour for the shovels, but without relief regulations."),
    u(5, HR + ", pp. 466–467: Markham on the “Ocala rock”",
      "I asked that a quarry with a 70-foot face be prepared in this Ocala for demolition in my presence so that I personally could come to a perfectly understand of just what our task was in excavating this unprecedented amount of material. That was done. … When I got down where the boulders were, if I saw a sharp projection from a boulder I could reach over and break it off with my hand, and that is this so-called rock. I observed a large boulder the size of this chair [indicating] and turning to the owner I said, “Will you have that Negro take that sledge and work on that boulder?” The sledge was about a 5-pound one and the Negro swung it about five times and split the entire boulder into pieces.",
      "“That Negro”",
      "The only Black worker who appears at the canal's rock in these sources: unnamed, set to work by the general's word to the quarry's owner, used to prove that the limestone was soft. Who he was and what he was paid is not recorded."),
]

STOP = [
    u(1, "Sanford Herald, 3 March 1936, p. 5: advertisement",
      "Public Auction Sale. 201 Young Mules & Harness Used By United States Government. 10:00 A. M., Wednesday, March 4, 1936. Camp No. 1, 9 Miles South of Ocala, Fla. We will sell at auction 201 mules and harness used by United States Government on Atlantic-Gulf Ship Canal project, starting at 10:00 A. M., Wednesday, March 4, 1936, at the mule barns, Camp No. 1, on Orange Road (Paved), 9 miles south of Ocala, Florida. … Fies & Sons, Birmingham, Ala.",
      "201 mules",
      "The canal was cleared and dug partly with mules. The advertisement does not say why the mules were sold in March, three months before the money ran out; it names a second camp nine miles south of Ocala."),
    u(2, "Sanford Herald, 3 April 1936, p. 1 (Associated Press)",
      "One Killed, 20 Hurt in Crash of Truck on Canal at Ocala. Ocala, Apr. 3.—(AP)—John Matthews, negro, died at a hospital of a broken neck received Wednesday night when a truck carrying 22 Florida ship canal construction workers overturned three miles south of here. All occupants were injured. All available ambulances were pressed into service to carry the men to a hospital. The crew was en route to a canal construction camp when the truck driver apparently lost control. The vehicle plunged into a ditch.",
      "John Matthews",
      "The only death on the canal works of 1935–36 found so far, and the only canal worker of these months named in the sources read. The report names him and his race, not his age, home or family; the other 21 men are not named. No count of accidents on the works has been found."),
    u(3, "Sanford Herald, 19 June 1936, p. 1 (Associated Press)",
      "Canal Defeat Gives Gloomy Air To Ocala. Ocala, June 19.—(AP)—Gloom prevailed in Ocala yesterday over the defeat of the Florida ship canal project in the House and Senate. Nevertheless, hope was not entirely lacking. Many confidently expressed belief the canal will be built, and some saw a possibility of favorable action on the project before the present Congress adjourns. At Camp Roosevelt, headquarters of the United States Engineers District, and along the right of way of the canal work continued according to schedule. Maj. E. H. Levy, acting district engineer, said the present program calls for work that will not be completed before the end of July, unless instructions are received to bring all activity to an end in the meantime.",
      "Gloom in Ocala",
      "How Congress refused the money is the subject of module 5."),
    u(4, "Sanford Herald, 8 July 1936, p. 2",
      "Hendricks Advises Local Efforts On Indian River Canal. … the speaker emphasized the importance of renewing the fight for the St. Johns-Indian River canal at the present time. He said that since work has stopped on the cross state canal about 5,000 men are left unemployed and that it might be a good suggestion to urge the President to transfer those men to the new canal as a relief …",
      "Five thousand left",
      "The speaker is Joe Hendricks, a candidate for Congress. Ten months after the first tree was cut, the men of the canal were a reserve of relief labour to be moved to the next project."),
]

SRC = ("Federal Writers' Project, American Guide, Marion County (typescript, 1936); Documentary History of the Florida Canal "
       "(Senate Document 275, 74th Congress, 1936); Hearings on H.R. 6150, House Committee on Rivers and Harbors (1937): University of Florida "
       "Digital Collections. Florida State Board of Health, Thirty-sixth Annual Report (1935): Internet Archive. Citrus County Chronicle, "
       "Madison Enterprise-Recorder and Sanford Herald, 1935–36: Florida Digital Newspaper Library. Federal and state works are in the public "
       "domain; for the newspapers no renewal of copyright has been found.")

T = {
    "id": "camp", "titel": "Camp Roosevelt", "jahr": "1935–1936",
    "autor": "County newspapers, a state health report, the canal's advocates and the Associated Press",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission; tables are set as running text. The newspapers of Ocala for these months are not in the digital collections reached; the town's own record of the camp is missing. No worker of the canal speaks in these sources: they appear as numbers, as “job hunters”, as an unnamed man with a sledge and, once, by name, in the report of his death. Wages, hours, food and the division of the camps by race are not documented in what has been read.",
    "sections": [
        {"id": "start", "titel": "Hundreds of job hunters (September 1935)",
         "blurb": "Within days of the President's allotment Ocala filled with men looking for work. A hundred broke the first ground with axes and shovels on 14 September; on the 19th the President set off a charge of dynamite by pressing a button at Hyde Park; by the first of October 3,000 men were at work.",
         "plates": ["ccc1935_boom", "mer1935_axe"], "viz": "camp-men", "units": START},
        {"id": "camp", "titel": "Before the latrines (autumn 1935)",
         "blurb": "The state's health officers found the workers arriving before the camps had sanitation, food protection or safe water. Their own records counted the canal workers they examined by colour.",
         "plates": ["sbh1935_sanitation", "sbh1935_table"], "units": CAMP},
        {"id": "work", "titel": "Ten miles of cut (1935–1936)",
         "blurb": "By June 1936 about ten miles of the central cut south of Ocala had been dug by dragline, conveyor and industrial railway, by some 6,000 men, nine in ten of them from the relief rolls. The Chief of Engineers proved the softness of the rock with an unnamed Black worker and a sledge.",
         "plates": ["sd1936_railway", "sd1936_cut", "sd1936_slopes", "sd1936_bridge", "sd1936_belt"], "units": WORK},
        {"id": "stop", "titel": "Mules, a death, and the stop (1936)",
         "blurb": "In March 1936 the government sold 201 mules from a canal camp; in April a truck of canal workers overturned and John Matthews died. In June Congress refused more money, and by July some 5,000 men were out of work again.",
         "plates": ["sh1936_mules", "sh1936_matthews", "sh1936_gloomy", "sh1936_hendricks"], "units": STOP},
    ],
}
for s in T["sections"]:
    s["zk"] = "Camp Roosevelt, " + re.sub(r" \(.*", "", s["titel"])
(D / "camp.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
NP = "Florida Digital Newspaper Library, University of Florida; no copyright renewal found."
DHP = "Documentary History of the Florida Canal, Senate Document 275, 74th Congress (1936)"
UFDC = "University of Florida Digital Collections; public domain."
NEW = [
    {"id": "ccc1935_boom", "side": "work", "titel": "“Just like boom days”, September 1935",
     "caption": "Ocala “buzzing with activity as hundreds of job hunters swarm over the town”; employment under the WPA through the National Re-employment Service.",
     "source": "Citrus County Chronicle (Inverness), 12 September 1935, p. 4; " + NP},
    {"id": "mer1935_axe", "side": "work", "titel": "Axe and shovel, 14 September 1935",
     "caption": "A hundred men break the first ground; “slightly more than 1750 men” at Camp Roosevelt, a mile and a half south of Ocala.",
     "source": "Madison Enterprise-Recorder, 20 September 1935, p. 10; " + NP},
    {"id": "sbh1935_sanitation", "side": "work", "titel": "Camp Roosevelt and canal zone sanitation, 1935",
     "caption": "The State Board of Health: the workers arrived “before adequate plans had been made for necessary sanitary facilities”.",
     "source": "Florida State Board of Health, Thirty-sixth Annual Report (1935), p. 36; Internet Archive; public domain."},
    {"id": "sbh1935_table", "side": "work", "titel": "Counted by colour, 1935",
     "caption": "The foot of the public health nurses' table of corrections, white and colored: “Canal Workers Examination 56 3”.",
     "source": "Florida State Board of Health, Thirty-sixth Annual Report (1935), p. 55, detail; Internet Archive; public domain."},
    {"id": "sd1936_railway", "side": "work", "titel": "Industrial railway, loaded by dragline",
     "caption": "“Industrial railway used in canal excavation, loaded by dragline.” Photograph of the works south of Ocala, 1935–36; photographer not named.",
     "source": DHP + ", plate p. ii; " + UFDC},
    {"id": "sd1936_cut", "side": "work", "titel": "An earth cut, early stage",
     "caption": "“Typical earth cut in preliminary stage.”",
     "source": DHP + ", plate p. ii; " + UFDC},
    {"id": "sd1936_slopes", "side": "work", "titel": "Slopes, berm and spoil banks",
     "caption": "“View of excavating work, showing slopes, berm, and spoil banks.”",
     "source": DHP + ", plate p. iii; " + UFDC},
    {"id": "sd1936_bridge", "side": "work", "titel": "Dragline and bridge conveyor",
     "caption": "“Dragline loading bridge conveyor.”",
     "source": DHP + ", plate p. iii; " + UFDC},
    {"id": "sd1936_belt", "side": "work", "titel": "Belt conveyor on the canal",
     "caption": "“Belt conveyor in operation on the canal.” The men along the conveyor are the only workers visible in the published photographs.",
     "source": DHP + ", plate p. iv; " + UFDC},
    {"id": "sh1936_mules", "side": "work", "titel": "201 mules for sale, March 1936",
     "caption": "Auction of 201 mules and harness used on the canal, at the mule barns of Camp No. 1, nine miles south of Ocala.",
     "source": "Sanford Herald, 3 March 1936, p. 5, detail; " + NP},
    {"id": "sh1936_matthews", "side": "work", "titel": "John Matthews, April 1936",
     "caption": "“One Killed, 20 Hurt in Crash of Truck on Canal at Ocala”: the Associated Press report of the death of John Matthews.",
     "source": "Sanford Herald, 3 April 1936, p. 1; " + NP},
    {"id": "sh1936_gloomy", "side": "capitol", "titel": "Gloom in Ocala, June 1936",
     "caption": "“Canal Defeat Gives Gloomy Air To Ocala”: work at Camp Roosevelt to end in July unless stopped sooner.",
     "source": "Sanford Herald, 19 June 1936, p. 1, detail; " + NP},
    {"id": "sh1936_hendricks", "side": "work", "titel": "Five thousand left unemployed, July 1936",
     "caption": "“Since work has stopped on the cross state canal about 5,000 men are left unemployed.”",
     "source": "Sanford Herald, 8 July 1936, p. 2, detail; " + NP},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
if "Florida State Board of Health" not in P["credit"]:
    P["credit"] = P["credit"].replace(" All in the public domain or CC0.", " The report of the Florida State Board of Health from the Internet Archive; photographs of the works of 1935–36 from the Documentary History of the Florida Canal. All in the public domain or CC0, newspapers after 1930 with no renewal of copyright found.")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "camp"), None) or next(x for x in M["shipped"] if x["id"] == "camp")
M["planned"] = [x for x in M["planned"] if x["id"] != "camp"]
m.update({"datei": "camp", "zk": "Start · Camp · Work · Stop",
          "kurz": "4 · Camp Roosevelt",
          "warum": "Hundreds of job hunters in Ocala in September 1935; a camp without latrines; ten miles of cut dug by some 6,000 men, nine in ten from relief; the state counting canal workers by colour; a general proving the rock soft with an unnamed Black worker; John Matthews killed on the way to camp; 5,000 men out of work again by July 1936.",
          "quelle": "Federal Writers' Project, Marion County (1936); Florida State Board of Health 1935; Documentary History of the Florida Canal (1936); House hearings 1937; Citrus County Chronicle, Madison Enterprise-Recorder, Sanford Herald 1935–36."})
order = ["ridge", "river", "relief", "camp", "aquifer", "war", "rodman", "undoing"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "camp"] + [m], key=lambda x: order.index(x["id"]))
for x in M["missing"]:
    if x["id"] == "wages":
        x["warum"] = "No wage rates, hours or living conditions of 1935–36 have been found in the sources read; only that nine in ten men came from the relief rolls and that 73 per cent of the first allotment was meant for wages. The records of the WPA and the Corps of Engineers (National Archives, Record Groups 69 and 77) would be needed."
ADD = [{"id": "ocalapress", "side": "work", "kurz": "The Ocala newspapers of 1935–36",
        "warum": "The town of the camp is the gap in this module: the Ocala papers of these months are not in the digital collections reached, and Chronicling America is behind a bot check that is not bypassed here. Camp Roosevelt is therefore seen from Inverness, Madison and Sanford.",
        "quelle": "Ocala Evening Star, Ocala Banner, 1935–36."},
       {"id": "accidents", "side": "work", "kurz": "Accidents on the works",
        "warum": "The death of John Matthews is the only accident of 1935–36 found so far. No count of injuries or deaths on the canal works has been found.",
        "quelle": "Corps of Engineers and WPA records; Florida State Board of Health."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "promise", "titel": "Promised and counted",
     "frage": "How many men would the canal employ?",
     "note": "In September 1935 army officials promised 7,000 men within four months; in the spring of 1936 the Writers' Project expected 20,000 at the peak. In June 1936 the canal authority counted about 6,000, and in July a candidate for Congress spoke of about 5,000 left unemployed.",
     "voices": [{"text": "camp", "sec": "start", "n": [4], "wer": "Citrus County Chronicle, 1935"},
                {"text": "camp", "sec": "work", "n": [1, 3], "wer": "Canal authority and Writers' Project, 1936"},
                {"text": "camp", "sec": "stop", "n": [4], "wer": "Sanford Herald, July 1936"}]},
    {"id": "workers", "titel": "How the workers appear",
     "frage": "In what form do the men of the canal enter the record?",
     "note": "As a share of the relief rolls in a congressman's statement; as an unnamed “Negro” with a sledge in the Chief of Engineers' testimony; and once by name, in a news agency report of his death.",
     "voices": [{"text": "camp", "sec": "work", "n": [2], "wer": "Representative W. J. Sears, 1936"},
                {"text": "camp", "sec": "work", "n": [5], "wer": "General E. M. Markham, 1937"},
                {"text": "camp", "sec": "stop", "n": [2], "wer": "Associated Press, April 1936"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/camp/"
for s in TL["stations"]:
    if s["titel"] == "The first blast":
        s.update({"cite": K + "start/3", "citeLabel": "Camp Roosevelt, 1935 [3]", "plate": "mer1935_axe"})
    if s["titel"] == "Ten miles, six thousand men":
        s.update({"cite": K + "work/1", "citeLabel": "Camp Roosevelt, 1936 [1]", "plate": "sd1936_belt"})
NEWST = [
    {"d": "12 September 1935", "side": "work", "titel": "Hundreds of job hunters",
     "text": "Ocala takes on a “boom-time aspect” as job hunters swarm over the town; hiring is to go through the National Re-employment Service.",
     "cite": K + "start/1", "citeLabel": "Camp Roosevelt, 1935 [1]", "plate": "ccc1935_boom",
     "quelle": "Citrus County Chronicle, 12 September 1935, p. 4."},
    {"d": "3 April 1936", "side": "work", "titel": "John Matthews",
     "text": "A truck carrying 22 canal workers overturns three miles south of Ocala; John Matthews, a Black worker, dies of a broken neck, and all the others are injured.",
     "cite": K + "stop/2", "citeLabel": "Camp Roosevelt, 1936 [2]", "plate": "sh1936_matthews",
     "quelle": "Sanford Herald, 3 April 1936, p. 1 (Associated Press)."},
    {"d": "8 July 1936", "side": "work", "titel": "About 5,000 men left unemployed",
     "text": "With work stopped on the canal, a candidate for Congress proposes moving the men to another canal as relief.",
     "cite": K + "stop/4", "citeLabel": "Camp Roosevelt, 1936 [4]", "plate": "sh1936_hendricks",
     "quelle": "Sanford Herald, 8 July 1936, p. 2."},
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
