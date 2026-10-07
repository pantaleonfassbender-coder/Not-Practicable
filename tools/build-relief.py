"""Builds data/relief.json (module 3: Work for the relief rolls, 1933–1937) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/relief/PRUEFUNG.md):
  Documentary History of the Florida Canal, comp. H. H. Buckman for the Ship Canal Authority of the State of Florida,
    Senate Document 275, 74th Congress, 2nd Session (1936), pp. 81–83, 123, 155–156, 382–383
    (UFDC UF00055183/00001, images gray0934-2 … gray1085-2);
  Levy County Journal (Bronson), 8 June 1933, p. 1 (UFDC UF00028309/01173);
  Atlantic-Gulf Ship Canal, Fla.: Hearings before the House Committee on Rivers and Harbors on H.R. 6150,
    75th Congress, 1st Session (April 1937), pp. 2, 114–115 (UFDC UF00018663/00001, images 00006, 00118–00119).
Rights: the Senate document and the hearings are U.S. government printings without copyright notice (public domain);
the Levy County Journal of 1933 was published with no renewal found (renewal not checked in the Copyright Office records).
Run from the site root: python tools/build-relief.py
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

AUTHORITY = [
    u(1, DH + ", pp. 81–82: the act of 12 May 1933, as summarized by its title",
      "For the purpose of cooperating with the Federal Government in the construction of the canal, the Legislature of the State of Florida, by an act approved May 12, 1933, created the Ship Canal Authority of the State of Florida. The title of this bill is as follows: An Act Creating and incorporating the Ship Canal Authority of the State of Florida; … providing that none of the general revenues of the State shall be used for or pledged for such purpose; authorizing said corporation to borrow money and to issue revenue bonds securing the repayment thereof; authorizing said corporation to procure rights-of-way and other property by condemnation and otherwise, and giving said corporation the right to take and use certain State lands for such purposes; authorizing counties to condemn or otherwise procure and to donate to said corporation land, rights-of-way, and other property needed or useful in the construction and operation of said canal, and to levy taxes for such purposes; … authorizing said corporation to transfer its rights and property to the United States of America under certain conditions; and repealing conflicting laws.",
      "No money from the State",
      "The design of the next sixty years is in this title: the State itself pays nothing; the canal authority may take land by condemnation; the counties along the route may take land, give it away and tax their people for it. The act itself (Laws of Florida 1933) has not yet been read in the original; this is its title as printed in the canal authority's own compilation."),
    u(2, DH + ", p. 82",
      "Pursuant to the authority and direction of the above act, the Governor appointed the following to be directors of the Ship Canal Authority of the State of Florida: Gen. Charles P. Summerall (chairman), Eustis, Lake County, Fla. Hon. John W. Campbell, mayor, Palatka, Fla. Dr. Eugene G. Peek, Ocala, Fla. Mr. J. W. Turner, Cedar Keys, Fla. Mr. Walter F. Coachman, Jr., Jacksonville, Fla. The Ship Canal Authority of the State of Florida took over the application of the National Gulf-Atlantic Ship Canal Association to the Reconstruction Finance Corporation for a loan with which to construct a canal, and subsequently the association did not participate in any official capacity.",
      "The directors",
      "Five men from the towns on the route and from Jacksonville, under a retired general. The newspaper report of the first meeting ([4]) names partly different members; which list was in force when is not clear from these sources."),
    u(3, DH + ", pp. 82–83: Joint Memorial No. 11 of the Florida Legislature to the President, approved 27 May 1933",
      "Whereas the construction of a ship canal across the State of Florida will give employment to a vast amount of human labor, thus greatly relieving the distress due to the unemployment crisis; at the same time creating a valuable commercial and military asset which will, in the course of time, repay its own cost through the collection of reasonable tolls from ships using the canal; … Whereas such a canal will cut off approximately 500 miles of distance by the water route between New Orleans and the Gulf ports, on the one hand, and New York and Liverpool, on the other, will eliminate the danger to shipping incident to passage through the Florida Straits, will bring about tremendous savings by reason of the resultant reduction in time, insurance, and other transportation costs, and will constitute a valuable asset to our national defense; …",
      "“A vast amount of human labor”",
      "Four years into the Depression, the first reason given is work. The old reasons of 1826 and 1880, the Straits, insurance and war (module 1), follow."),
    u(4, "Levy County Journal (Bronson), 8 June 1933, p. 1",
      "Senator Turner on Ship Canal Authority. Tallahassee, June 5.—The Florida Ship Canal Authority at its organization meeting here today elected Gen. Charles P. Summerall of Eustis, chairman, and D. F. Goodell, West Palm Beach, temporary secretary. Commissions as members of the authority were given Summerall, Goodell, Walter F. Coachman, Jacksonville; Senator J. W. Turner, Cedar Keys, and Hal Dooley, Pensacola. Under the act of recent Legislature, the authority has power to obtain right-of-way and to finance, construct and operate, either independently or in connection with the Federal government, a cross-State canal. … Summerall added that engineers have estimated it will cost from $114,000,000 to $160,000,000 to construct the canal, depending on the route selected and specifications.",
      "The first meeting",
      "The county newspaper of Levy County, on the canal's western route."),
]

LOAN = [
    u(1, DH + ", p. 123 (see also p. 94): Philip B. Fleming, Acting Deputy Administrator, to the Administrator of Public Works, 21 December 1934",
      "Memorandum. For: The Administrator. Docket No. 139, Florida; Ship Canal; Loan. Recommendation: Disapproval. This application was received on August 14, 1933, and has been disapproved by an independent board of engineers appointed to study this project. It is the opinion of this board that the proposed project would not be self-liquidating. I concur in the conclusion of this board and recommend that this application be disapproved.",
      "“Would not be self-liquidating”",
      "As a loan to be repaid from tolls, the canal failed. The compiler of the canal authority's history, H. H. Buckman, comments on the same page that the memorandum was “erroneous” and reversed the findings of the agency's own examiners; the Administrator of Public Works, Harold L. Ickes, disapproved the application on 29 January 1935 (p. 94)."),
    u(2, DH + ", p. 155: Franklin D. Roosevelt to the Secretary of the Treasury, 30 August 1935",
      "My Dear Mr. Secretary: By virtue of the authority vested in me under the Emergency Relief Appropriation Act of 1935, approved April 8, 1935, it is requested that the following funds be transferred from the appropriation made in said act to the War Department, Corps of Engineers, for the purpose indicated below: Amount: $5,000,000. Purpose: To provide work relief and increase employment in accordance with the attached schedule of projects. … Clearing right-of-way, housing, and excavation in central area to give employment to those on relief rolls (during the first 12 months the money included in the estimates for wages amounts to 73 percent of the total allotment which is for a period of 12 months), work to be started immediately to absorb not only a large portion of the local relief load but also workers from transient camps and adjacent States. Clearing right-of-way $500,000. Housing, shops, storehouses, and minor structures 500,000. Excavation in central areas 3,500,000. Bridge foundations 500,000. Total 5,000,000.",
      "Five million dollars for relief",
      "What had failed as a loan was begun as relief: not by an act of Congress for a canal, but by the President's allotment from the relief appropriation, and with the Army's engineers as builders. Seventy-three per cent of the money was to be wages. The schedule is set here as running text."),
    u(3, DH + ", p. 156",
      "On September 3, 1935, the Chief of Engineers issued orders to the district engineer of the Ocala district, Lt. Col. B. B. Somervell, to begin construction of the canal pursuant to the authorization issued by the President under date of August 30, 1935. (See Doc. 87.) Actual work on the project was begun on the same day.",
      "Begun the same day",
      "Four days after the allotment; seven weeks before the counties voted to pay for the land ([1] in the next section). The start of the work is the subject of module 4."),
]

BONDS = [
    u(1, DH + ", p. 156",
      "On October 22, 1935, in conformity with the conditions imposed by Federal authority, the six counties (Duval, Clay, Putnam, Marion, Levy, and Citrus) comprising the Florida ship canal navigation district voted, by a majority of 27 to 1, a bond issue of $1,500,000 for the purchase of all necessary land for right-of-way for the canal, and for the dedication of such right-of-way to the Federal Government for the purpose of constructing, maintaining, and operating a ship canal.",
      "Twenty-seven to one",
      "The counties paid for the land and gave it to the United States, as the engineers had asked of the Ocklawaha towns in 1914 (module 2). The vote came after the work had begun."),
    u(2, DH + ", p. 382: Representative William J. Sears of Florida before the subcommittee of the House Committee on Appropriations, 17 April 1936",
      "The last Legislature of Florida provided for a bonding election, in what we call in Florida the cross-State canal district, composed of the counties of Clay, Duval, Putnam, Marion, Citrus, and Levy, six counties, the amount of the bond issue being $1,500,000. They did that because the administration told the delegation from Florida, at which meeting my colleague, Congressman Caldwell, was present, with myself and the other members of the delegation, that before the administration would go on with the canal the people had to show their good faith by giving the right-of-way. At that election only freeholders could vote. In other words, those qualified electors who had registered and paid their poll tax and who owned property could vote. It was out of the taxes that they paid that this million and a half dollars would be refunded. The vote was as follows: In Clay County the vote was 473 for and 47 against. In Duval County the vote was 10,039 for and 329 against. In Putnam County the vote was 1,720 for and 100 against. In Marion County the vote was 2,115 for and 46 against. In Citrus County the vote was 485 for and 37 against. In Levy County the vote was 603 for and 31 against. I am informed that 90 percent or more of the qualified freeholders participated in this election. Under our law in Florida a majority of the qualified freeholders must participate.",
      "“Only freeholders could vote”",
      "Who was asked: only registered voters who had paid the poll tax and owned property. That these conditions shut out many Black and poor white residents of the six counties is an inference from the conditions themselves; the passage does not say so, and no source read here counts who was left out. The six counties' figures add up to 15,435 for and 590 against, about 26 to 1."),
    u(3, DH + ", p. 383: Sears, continued",
      "The Chairman. The freeholders are landowners? Mr. Sears. Yes; freeholders are landowners, and not less than 50 percent of the freeholders must vote. … The afternoon before the election I happened to be in Jacksonville. … There must have been 15,000 people on Forsyth Street that night listening to the speakers. I told them that the Florida delegation had assured the President the people of the district would give the right-of-way as demanded by him; and if they did not do so, work on the canal would cease when the first allotment was exhausted. That if they placed a mortgage on their homes they need have no fear work on the canal would stop. … I said also to those people, “There are thousands of you listening to me who have been hungry and who are hungry tonight, but who have refrained from going on the relief rolls because you did not want to add to the expense of the Government in taking care of the needy. If the bond issue carries, and I know it will, the battle will be won and you can then secure work on the canal.”",
      "“Who are hungry tonight”",
      "A congressman's campaign speech, as he retold it: the bond vote as a vote for work. The hungry in the street could hear it; only the property owners among them could vote."),
    u(4, HR + ", p. 2: Representative Lex Green of Florida",
      "It was determined in 1935 that, if the State of Florida would deliver the right-of-way, the Government, through P. W. A. funds, under the order of the President, would begin the construction of the project. The counties affected, that is the counties adjacent to the canal and in the right-of-way of the canal on the route adopted by the engineers, determined to furnish the right-of-way. They held elections of the freeholders in the respective counties and voted bonds of $1,500,000 to be used for the purchase of the right-of-way. The bond issue was carried by amount 98 percent, or 95 percent to 98 percent of the freeholders voting for the bonds. The bonds were sold, the money obtained, the right-of-way purchased and delivered to the Federal Government.",
      "Delivered to the Federal Government",
      "A year and a half later, after the work had stopped (module 5). Green speaks of P.W.A. funds; the allotment of 1935 came from the relief appropriation ([2] in the previous section)."),
]

LAND = [
    u(1, HR + ", p. 114: James A. Taylor, Marion County, questioned by Representative Carter",
      "Mr. Carter. Do you know just where the canal zone runs through there? Mr. Taylor. Yes, sir. I might say that I was one of the appraisers of the land. Mr. Carter. And you condemned some of that property? Mr. Taylor. Yes, sir; and I am very familiar with it. Mr. Carter. You are within this bonded district, then? You are helping to pay for that land? Mr. Taylor. Yes, sir. … Mr. Taylor. Yes, sir; there are. But that is not a farming district. I have lived a great many years—in fact, all of my life—in this section, and I am more or less familiar with all of the farms in it. The farms in the right-of-way, as I remember, are approximately 700 acres that were under cultivation or had been under cultivation. Mr. Carter. That is for the entire length of the right-of-way or in that particular section? Mr. Taylor. In that entire length of the right-of-way. Mr. Carter. You mean from the Atlantic Ocean clear on across? Mr. Taylor. Oh, no; just in about 40 miles.",
      "“One of the appraisers of the land”",
      "The man who valued the land for the condemnations, himself a taxpayer of the district, testifying for the canal."),
    u(2, HR + ", p. 115",
      "Mr. Carter. What did you pay for that land—the farm land? Mr. Taylor. It averaged $8 to $10 an acre. Mr. Carter. For farm land? Mr. Taylor. Yes, sir. Mr. Carter. What did you pay for the other land that was not farm land? Mr. Taylor. Anywhere from $2 to $5 or $6 an acre, depending upon how much timber growth it had on it. … Mr. Taylor. We paid them for anything they had on the land, wells or anything else. But these people in this area here do not depend upon farming entirely. A great many of them are Negroes and they work on public works or in the citrus groves. Mr. Carter. In addition to having something in the way of a farm, too? Mr. Taylor. Most of them depend upon the citrus groves south of us for a living. Mr. Carter. Was $10 an acre the most that you allowed for that farm land? Mr. Taylor. In that particular section; yes. That was a very poor section.",
      "“A great many of them are Negroes”",
      "The only passage found so far on the people whose land was taken in 1935–36. They are described by the appraiser who set the price, not heard; their names, their number and whether they accepted or contested the price are not in the sources read. Owning land, they met one condition of the bond vote that paid for it; whether they had registered and paid the poll tax, the sources do not say ([2] in the previous section)."),
    u(3, "House Document 194, 75th Congress, 1st Session (1937), map: U.S. Engineer Office, Ocala, Status of Right of Way Acquisition, June 1936, sheet 1",
      "Status of right of way acquisition. In possession 21,633 acres 26.6%. Balance required 59,859 acres 73.4%. Total acres 81,492. Exercised options 12,003 ac. 14.8%. In condemnation 9,630 ac. 11.8%. In possession 21,633 ac. 26.6%. Condemnation requested 6,196 ac. 7.6%. Other 53,663 ac. 65.8%. Balance required 59,859 ac. 73.4%. U. S. Engineer Office, Ocala, Fla., June, 1936.",
      "81,492 acres",
      "The legend of the Army engineers' map of the western part of the route, from Ocala past Dunnellon to the Gulf near Yankeetown, eight months after the bond vote. A quarter of the land was in hand; more than half of that had been bought on options, the rest was being taken by condemnation, and 6,196 acres more were waiting for it. South of Camp Roosevelt the cut runs through the settlement of Santos. Behind the acres are owners whose names the map does not give."),
]

SRC = ("Documentary History of the Florida Canal, compiled by Henry Holland Buckman for the Ship Canal Authority of the State of Florida, "
       "Senate Document 275, 74th Congress, 2nd Session (Washington 1936); Atlantic-Gulf Ship Canal, Fla.: Hearings before the Committee on "
       "Rivers and Harbors, House of Representatives, on H.R. 6150 (Washington 1937): University of Florida Digital Collections; "
       "Levy County Journal, 8 June 1933: Florida Digital Newspaper Library. The congressional printings are in the public domain; "
       "for the newspaper of 1933 no renewal of copyright has been found.")

T = {
    "id": "relief", "titel": "Work for the relief rolls", "jahr": "1933–1937",
    "autor": "The canal authority's own record, a congressman, an appraiser and a county newspaper",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission; schedules and vote lists are set as running text. The figures of the bond vote are those of the printed page; the OCR text of the online edition misreads several of them. Most passages come from the Documentary History, a compilation made by the canal authority's own engineer to argue for the canal; it prints its opponents' documents too, but comments on them. Those who were not asked, because they had no property or had not paid the poll tax, and those whose land was taken, appear only in the words of others.",
    "sections": [
        {"id": "authority", "titel": "A canal authority (1933)",
         "blurb": "In May 1933 Florida's legislature created a Ship Canal Authority and asked the President for a canal that would “give employment to a vast amount of human labor”. The State was to pay nothing; the counties on the route could take land and tax for it.",
         "plates": ["sd1936_act", "lcj1933_authority"], "units": AUTHORITY},
        {"id": "loan", "titel": "Not a loan, but relief (1934–1935)",
         "blurb": "The canal authority asked the Public Works Administration for a loan to be repaid from tolls. It was refused: the canal “would not be self-liquidating”. In August 1935 the President gave five million dollars from the relief appropriation instead, three quarters of it for wages, and the Army began work four days later.",
         "plates": ["sd1936_allotment"], "units": LOAN},
        {"id": "bonds", "titel": "Only freeholders (October 1935)",
         "blurb": "The condition was the land. On 22 October 1935 the six counties of the canal district voted $1,500,000 in bonds to buy the right-of-way and give it to the United States. Only property owners who had registered and paid the poll tax could vote; a congressman promised the hungry in Jacksonville work if the bonds carried.",
         "plates": ["sd1936_votes"], "viz": "relief-votes", "units": BONDS},
        {"id": "land", "titel": "Eight to ten dollars an acre (1935–1937)",
         "blurb": "The land was bought on options or taken by condemnation. In June 1936 the Army's engineers mapped how far they had got; in 1937 one of the appraisers told Congress what had been paid, and who had lived there.",
         "plates": ["h1937_taylor", "hd1937_rightofway"], "viz": "relief-land", "units": LAND},
    ],
}
for s in T["sections"]:
    s["zk"] = "Work for the relief rolls, " + re.sub(r" \(.*", "", s["titel"])
(D / "relief.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
DHP = "Documentary History of the Florida Canal, Senate Document 275, 74th Congress (1936)"
UFDC = "University of Florida Digital Collections; public domain."
NEW = [
    {"id": "sd1936_act", "side": "land", "titel": "The canal authority, 1933",
     "caption": "The title of Florida's act of 12 May 1933 creating the Ship Canal Authority (none of the State's general revenues to be used; counties may condemn land and levy taxes), the directors, and the Legislature's memorial to the President.",
     "source": DHP + ", p. 82; " + UFDC},
    {"id": "lcj1933_authority", "side": "land", "titel": "The first meeting, June 1933",
     "caption": "“Senator Turner on Ship Canal Authority”: the authority's organization meeting at Tallahassee, and an estimate of $114,000,000 to $160,000,000.",
     "source": "Levy County Journal (Bronson), 8 June 1933, p. 1; Florida Digital Newspaper Library, University of Florida; no copyright renewal found."},
    {"id": "sd1936_allotment", "side": "capitol", "titel": "Five million dollars for relief, 30 August 1935",
     "caption": "The President's allotment from the Emergency Relief Appropriation Act of 1935: “To provide work relief and increase employment”, with the schedule of works.",
     "source": DHP + ", p. 155; " + UFDC},
    {"id": "sd1936_votes", "side": "land", "titel": "Only freeholders, 1935",
     "caption": "Representative Sears on the bond election of 22 October 1935: “At that election only freeholders could vote”, and the vote in each of the six counties.",
     "source": DHP + ", p. 382, detail; " + UFDC},
    {"id": "h1937_taylor", "side": "land", "titel": "“$8 to $10 an acre”, 1937",
     "caption": "The appraiser James A. Taylor before the House Committee on Rivers and Harbors: the price of the land, and “A great many of them are Negroes”.",
     "source": "Hearings on H.R. 6150, House Committee on Rivers and Harbors (1937), p. 115; " + UFDC},
    {"id": "hd1937_rightofway", "side": "land", "titel": "Status of right of way acquisition, June 1936",
     "caption": "The Army engineers' map of the western part of the route, from Ocala, Camp Roosevelt and Santos past Dunnellon to the Gulf near Inglis and Yankeetown, with the land under option, in condemnation and still required: 21,633 of 81,492 acres in possession.",
     "source": "House Document 194, 75th Congress, 1st Session (1937), map sheet 1 (U.S. Engineer Office, Ocala, June 1936); U.S. Congressional Serial Set, scan of govinfo.gov; public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["credit"] = P["credit"].replace("newspaper pages from the Florida Digital Newspaper Library, University of Florida;",
                                  "newspaper pages from the Florida Digital Newspaper Library and congressional printings from the University of Florida Digital Collections;")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "relief"), None) or next(x for x in M["shipped"] if x["id"] == "relief")
M["planned"] = [x for x in M["planned"] if x["id"] != "relief"]
m.update({"datei": "relief", "zk": "Authority · Relief · Bonds · Land",
          "kurz": "3 · Work for the relief rolls",
          "warum": "In 1933 Florida created a canal authority that the State would not pay for. Refused as a loan, the canal was begun in 1935 with relief money. The counties bought the land, in a bond election open only to property owners who had paid the poll tax; the appraiser said many of those on the land were Black.",
          "quelle": "Documentary History of the Florida Canal (Senate Document 275, 1936); House hearings on H.R. 6150 (1937); Levy County Journal 1933."})
order = ["ridge", "river", "relief", "camp", "aquifer", "war", "rodman", "undoing"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "relief"] + [m], key=lambda x: order.index(x["id"]))
for x in M["missing"]:
    if x["id"] == "families":
        x["warum"] = ("The sources give acreages and prices (of the right-of-way in 1936, of the Rodman pool, of lawsuits) and one appraiser's remark that many of those on the land in Marion County were Black, but not the number or names of the families who lost land or homes. County land and court records would be needed.")
ADD = [{"id": "laws1933", "side": "land", "kurz": "The acts of 1933 and 1935",
        "warum": "Florida's act creating the Ship Canal Authority (1933) and the act creating the navigation district and its bond election (1935) are known here only by their titles and from congressional testimony; the Laws of Florida have not yet been read in the original.",
        "quelle": "Laws of Florida 1933 and 1935."},
       {"id": "excluded", "side": "land", "kurz": "Who could not vote on the bonds",
        "warum": "How many adults in the six counties were kept from the bond election by the poll tax and the property requirement, and how many of them were Black, is not counted in any source read so far.",
        "quelle": "County voter registration and tax rolls, 1935; census of 1930 and 1940."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "condition", "titel": "The land as the condition",
     "frage": "Who was to give the land for a waterway?",
     "note": "In 1914 the engineers recommended locks on the Ocklawaha only if local interests gave the land free and held the United States harmless for flooding. In 1935 the administration would go on with the canal only if the six counties gave the right-of-way; they bonded their taxpayers for it.",
     "voices": [{"text": "river", "sec": "trade", "n": [6], "wer": "Chief of Engineers, 1914"},
                {"text": "relief", "sec": "bonds", "n": [2], "wer": "Representative W. J. Sears, 1936"}]},
    {"id": "asked", "titel": "Who was asked, who was described",
     "frage": "Whose voice decided on the land?",
     "note": "The bond election was open to freeholders who had paid their poll tax; their vote was counted county by county. The people on the land in Marion County appear in the record only through the appraiser who priced it.",
     "voices": [{"text": "relief", "sec": "bonds", "n": [2], "wer": "Representative W. J. Sears, 1936"},
                {"text": "relief", "sec": "land", "n": [2], "wer": "James A. Taylor, appraiser, 1937"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/relief/"
for s in TL["stations"]:
    if s["titel"] == "A memorial for work":
        s.update({"cite": K + "authority/3", "citeLabel": "Work for the relief rolls, 1933 [3]", "plate": "sd1936_act"})
NEWST = [
    {"d": "12 May 1933", "side": "land", "titel": "A canal authority the State will not pay for",
     "text": "Florida creates the Ship Canal Authority; none of the State's general revenues may be used, but counties may condemn land for the canal and levy taxes for it.",
     "cite": K + "authority/1", "citeLabel": "Work for the relief rolls, 1933 [1]", "plate": "sd1936_act",
     "quelle": "Documentary History of the Florida Canal (1936), pp. 81–82."},
    {"d": "21 December 1934", "side": "capitol", "titel": "“Not self-liquidating”",
     "text": "The Public Works Administration's deputy administrator recommends refusing the canal authority's loan; the Administrator disapproves it on 29 January 1935.",
     "cite": K + "loan/1", "citeLabel": "Work for the relief rolls, 1934 [1]",
     "quelle": "Documentary History of the Florida Canal (1936), p. 123."},
    {"d": "30 August 1935", "side": "capitol", "titel": "Five million dollars for relief",
     "text": "The President allots $5,000,000 from the Emergency Relief Appropriation Act to the Corps of Engineers for the canal, “to provide work relief and increase employment”; 73 per cent is for wages.",
     "cite": K + "loan/2", "citeLabel": "Work for the relief rolls, 1935 [2]", "plate": "sd1936_allotment",
     "quelle": "Documentary History of the Florida Canal (1936), p. 155."},
    {"d": "22 October 1935", "side": "land", "titel": "Only freeholders vote",
     "text": "The six counties of the canal district vote $1,500,000 in bonds for the right-of-way, 15,435 to 590. Only registered property owners who have paid the poll tax may vote.",
     "cite": K + "bonds/2", "citeLabel": "Work for the relief rolls, 1935 [2]", "plate": "sd1936_votes",
     "quelle": "Documentary History of the Florida Canal (1936), pp. 156, 382."},
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
