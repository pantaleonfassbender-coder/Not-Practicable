"""Builds data/undoing.json (module 8: Undoing the canal, 1971–1990) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/undoing/PRUEFUNG.md):
  Cross-Florida Barge Canal: Hearing before the Subcommittee on Water Resources, House Committee on Public Works and
    Transportation, Palatka, 10 June 1985 (GPO 1986), pp. 26, 91, 139–140, 146–147, 169, 192, 226–227
    (Internet Archive micro_IA41152634_0813, leaves n31, n96, n145–n146, n152–n153, n175, n199, n233–n234);
  U.S. Army Corps of Engineers, Jacksonville District, Cross Florida Barge Canal Restudy Report, Summary (August 1976), p. 13
    (UFDC NF00000163/00001, image 00018);
  The President's Environmental Program, 1977 (23 May 1977), p. M-10 (Internet Archive micro_IA41153362_0079, leaf n13);
  Public Law 101-640, § 402, 28 November 1990, 104 Stat. 4644–4645 (govinfo STATUTE-104-Pg4604).
All federal printings, and decisions and statements printed in them, in the public domain. Prepared statements of private
witnesses printed by the GPO in 1986 without notice are quoted briefly.
Run from the site root: python tools/build-undoing.py
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


H85 = "House hearing, Cross-Florida Barge Canal, Palatka, 10 June 1985"

TAX = [
    u(1, H85 + ", p. 91: statement on the Cross Florida Canal Navigation District",
      "The district began levying and collecting taxes in 1936 and continued to do so uninterrupted until January 1971, when the order was issued by President Nixon to halt work on the canal. At that time the total amount of taxes which had been collected by the district since 1936 was $9,340,720. (See Appendix B.) The majority of that money had been transferred to the Canal Authority which in turn used it to acquire the right-of-way for the canal. Of that total amount approximately $900,000 is currently on hand in the district's accounts. … at the time of the Presidential “stop order,” the Authority had acquired substantially all the land necessary for the project. The amount of land acquired and currently held by the Authority is approximately 50,000 acres. Of this amount approximately 40,000 acres are held in fee simple, the remainder being held in the form of permanent easements. In addition to the money received from the Navigation District, the Canal Authority also received from 1962 to 1970 appropriations totaling approximately $7.5 million from the Florida Legislature disbursed from general …",
      "Thirty-five years of canal tax",
      "The bonds of 1935, voted by property owners only (module 3), became a tax on the six counties for thirty-five years. The State, which in 1933 was to pay nothing, had paid $7.5 million in the 1960s. The statement is printed in the hearing record; its author is named on the preceding page, not read here."),
]

RESTUDY = [
    u(1, "U.S. Army Corps of Engineers, Jacksonville District, Cross Florida Barge Canal Restudy Report, Summary (August 1976), p. 13",
      "The Oklawaha River Basin ecosystem would be lost as an entity along with the river fishery and river reptiles and invertebrates under the authorized alternative. These would be replaced with a reservoir ecosystem. … A temporary flooded tree habitat would benefit red-headed woodpecker and wood duck before the trees fall. … A total of 25,800 acres of productive forest land would be permanently lost under the authorized alternative, along with 4,800 acres of unclassified forest, and 4,000 acres of non-forest land. Commercial timber which will be cut and no longer produced is presently valued at $8,650,000. Fifteen endangered or threatened species would lose habitat while two would be benefited.",
      "“Lost as an entity”",
      "The Army's own restudy after the halt. Here the river ecosystem is counted among the losses, as Nixon had asked in 1971 (module 7)."),
    u(2, "The President's Environmental Program, 1977: message of President Carter to the Congress, 23 May 1977, p. M-10",
      "I am also submitting legislation to the Congress to withdraw authority for future construction of the Cross-Florida Barge Canal, to extend the boundaries of the Ocala National Forest to protect the Oklawaha River, and to authorize study of the Oklawaha River for possible designation as a Wild and Scenic River. Enactment of this legislation will put an end to the long controversy over this ill-advised project. I am also directing the Secretary of Agriculture, the Secretary of the Army, and other appropriate federal agencies, in cooperation with the State of Florida, to recommend ways to dispose of canal lands and structures, as well as ways to restore the Oklawaha River portion of the project area.",
      "“This ill-advised project”",
      "Congress did not enact it. Thirteen more years passed before the canal was ended (last section)."),
]

PALATKA = [
    u(1, H85 + ", p. 26: prepared statement of Governor Bob Graham",
      "Florida is among America's fastest growing states. We have many needs—we need new schools, more teachers, roads, bridges, mass transit, water and sewer lines—but there is one thing we don't need, and that's the Cross-Florida Barge Canal. I don't mean to make you feel unwelcome by using excessively clear language—but we do not want this canal. Period. … President Nixon terminated all work on the project in 1971—or so we thought. In 1972 the Governor and Cabinet suspended support for the project, pending completion of economic and environmental impact studies. In 1976 a definitive review and analysis found no reason to continue the project, and abundant reasons to cancel it. On January 17, 1977, the Governor and Cabinet of Florida adopted a resolution condemning this project and requesting its deauthorization. … On May 16, 1985, the Florida Legislature passed a memorial to the United States Congress requesting deauthorization. … the margin by which that memorial passed the Florida House of Representatives was 105-5. In the Florida Senate, the vote was 33-3.",
      "“We do not want this canal. Period.”",
      "In 1933 the Florida Legislature had sent the President a memorial for the canal (module 3). In 1985 it sent Congress one against it."),
    u(2, H85 + ", p. 139: Representative Bill Chappell of Florida",
      "Now keep in mind, the corps had made those assessments, they had put them into their assessment that went through the Atlanta office, was accepted as proper there, and then a task force from Mr. Nixon's office was put together to prohibit that information coming on up, so they cut it out at the Washington level and it was not considered. … No. 1 is to identify the source of coal for the area and what impact that could have on the cost of electricity; savings and so forth, which it had been estimated that the savings alone in the transportation of coal over a period of 10 years would pay for the canal of and by itself.",
      "The canal's last defenders",
      "The canal still had advocates in Congress. Their claim: the benefits had been left out of the accounts. Every side, since 1880, had accused the other of leaving something out."),
    u(3, H85 + ", pp. 139–140: Marjorie Harris Carr, president of Florida Defenders of the Environment",
      "Mr. Roe. … We are going to start out first with Ms. Carr. You do not come to us as being someone we do not feel we know. [Laughter.] Ms. Carr. The notorious Ms. Carr. … I am Marjorie Harris Carr, president of Florida Defenders of the Environment, a statewide conservation group with headquarters in Gainesville, FL. Our organization was formed in 1969 in order to gather the facts relative to the environment and economic impact of construction of the Cross-Florida Barge Canal. And may I say that the group that formed FDE, as we are commonly called, the nucleus of that group had coalesced early in the sixties when we first heard about the barge canal. … And we were shocked in 1962, when we found that the route of the canal went right down the Oklawaha River, one of the beautiful rivers in Florida. So our little group in the early sixties tried to get the canal route changed away from the river. We were unsuccessful in that. We reached our Waterloo in that effort in 1966. … We were unable to stop the route of the canal in 1966. No one in government would listen to us at all, though I rather imagine now they wish they had. … When they moved ahead with the construction, our group did organize; we became incorporated; Florida Defenders of the Environment, in 1969. In the first year of our existence, a group of us—and all of our people were volunteers—prepared this 115 page report. “Environmental Impact of the Cross-Florida Barge Canal with Special Emphasis on the Oklawaha Regional Ecosystem” was printed early in 1970.",
      "“The notorious Ms. Carr”",
      "The opponents' own account, in their own words, fifteen years after the halt. The report of 1970 she holds up is named, not printed, in this apparatus."),
    u(4, H85 + ", p. 169: prepared statement of Marjorie H. Carr",
      "The Oklawaha and Withlacoochee Rivers have already been damaged by canal construction. If the project was completed, much of the remaining Oklawaha river valley forest would be destroyed, the river would be severely impacted, and the wildlife would suffer. Thousands of acres of scarce forest types would be lost, including the habitat of several species of Endangered and Threatened plants. … The Cross Florida Barge Canal project is a waste of taxpayers' money. The cost of completing the Cross Florida Barge Canal at 1985 price levels is $605 million. At current discount rates of 8 3/8% for public works projects the canal would cost far more than it would produce in benefits. The benefit/cost ratio at current discount rates would be about .50-1. … The six counties that contributed tax money to purchase the canal right-of-way cannot receive repayment until after deauthorization.",
      "Fifty cents on the dollar",
      "Carr argues with the canal's own measures: cost, benefit, the counties' tax."),
    u(5, H85 + ", p. 146: Dr. John H. Kaufmann, Florida Defenders of the Environment",
      "… that will not affect the basic conclusion that the economics of this project are so bad that at the current discount rate and with the appropriate corrections in the cost-benefit ratio, which I have detailed in my written testimony, the current benefit-cost ratio for this project in current valid economic terms would be far less than 50 cents on the dollar. … We ask you now to deauthorize the canal, not to delay further, not to wait for more studies to be done, because the State of Florida and the conservation organizations of this State have, in a sense, been held hostage over this issue; the State of Florida for 10 years, the conservation organizations for 20 years.",
      "“Held hostage”"),
    u(6, H85 + ", p. 147: Charles Lee, Florida Audubon Society",
      "Last year on June 28, the U.S. House of Representatives voted 204 to 201 not to deauthorize the Cross-Florida Barge Canal project. The Florida delegation to the U.S. House voted 13 to 6 in favor of deauthorization of the canal …",
      "204 to 201",
      "Three votes kept the canal alive in 1984; most of Florida's own members had voted to end it."),
]

LAND = [
    u(1, H85 + ", p. 192: formal statement of Florida's Attorney General, Jim Smith",
      "This statement is to address the possibility that the public would lose certain easement interests held for the Cross Florida Barge Canal upon deauthorization of the canal project. … Of the land held for Lake Oklawaha, a large amount (over 7300 acres) is held by perpetual easements, acquired in condemnation.",
      "Easements under the lake",
      "If the canal ended, would the land under Lake Oklawaha go back to its owners? The easements of the 1960s (module 7, Boynton) were the question."),
    u(2, H85 + ", pp. 226–227: Supreme Court of Florida, Mainer v. Canal Authority, 18 April 1985",
      "These nine consolidated cases were brought by the petitioners to reacquire lands originally taken by the Canal Authority for the construction of the Cross-Florida Barge Canal. … We disapprove the decision in Ocala Manufacturing and hold that, absent fraudulent intent or bad faith at the time of the taking, fee simple title taken by a governmental entity through condemnation, settlement, or donation cannot be collaterally attacked on the basis of a failure or discontinuation of the use originally intended for the land taken. … The lands in question were acquired in fee simple between 1966 and 1970. … The property of Joyce G. Mainer was acquired in fee simple through a contested condemnation proceeding by an order of taking entered June 6, 1968. … The property of Kenneth T. Hodges was acquired in fee simple through a deed recorded on August 3, 1967. The closing statement submitted in these proceedings reflects the following statement: “The receipt of $1,583.24 is acknowledged by the undersigned Sellers.”",
      "Nine owners who wanted their land back",
      "The canal was stopped; the land taken for it stayed taken. The court names the owners and how each lost the land; none of them speaks in the decision. The Florida legislature had already provided in 1979 for some lands around Lake Rousseau; that act has not yet been read at the page image."),
]

END = [
    u(1, "Public Law 101-640, § 402 (28 November 1990), 104 Stat. 4644",
      "Sec. 1114. Cross Florida Barge Canal. (a) Deauthorization.—The barge canal project located between the Gulf of Mexico and the Atlantic Ocean …, as described in the Act of July 23, 1942 (56 Stat. 703), shall be deauthorized by operation of law immediately upon the Governor and Cabinet of the State of Florida adopting a resolution specifically agreeing on behalf of the State of Florida … to all of the terms of the agreement prescribed in subsection (b). (b) Transfer of Project Lands.—… the Secretary is … directed to transfer to the State all lands and interests in lands acquired by the Secretary and facilities completed for the project …, without consideration, if the State agrees to each of the following: (1) The State shall agree to hold the United States harmless from all claims arising from or through the operations of the lands and facilities conveyed by the United States. (2) The State shall agree to preserve and maintain a greenway corridor which shall be open to the public for compatible recreation and conservation activities and which shall be continuous … Such greenway corridor shall not be less than 300 yards wide …",
      "Deauthorized, and a greenway",
      "Forty-eight years after the act of 1942, the canal ends by law, on condition: the land goes to the State, and the State keeps a corridor across Florida open to the public."),
    u(2, "Public Law 101-640, § 402, 104 Stat. 4645",
      "(5) The State shall agree to pay, from the assets of the State Canal Authority and the Cross Florida Canal Navigation District, including revenues from the sale of former project lands declared surplus by the State management plan, to the counties of Citrus, Clay, Duval, Levy, Marion, and Putnam a minimum aggregate sum of $32,000,000 in cash or, at the option of the counties, payment to be made by conveyance of surplus former project lands selected by the State at current appraised values. (6) The State shall agree to provide that, after repayment of all sums due to the counties …, the State may use any remaining funds generated from the sale of former project lands declared surplus by the State to acquire the fee title to lands along the project route as to which less than fee title was obtained, or to purchase privately owned lands, or easements over such privately owned lands …",
      "$32,000,000 for the six counties",
      "The six counties of 1935 are paid back. The law repays counties, not the people whose land was taken; their claims ended with Mainer ([2] in the previous section)."),
]

SRC = ("Hearing before the Subcommittee on Water Resources, House Committee on Public Works and Transportation, Palatka, 10 June 1985 (GPO 1986; Internet "
       "Archive); Corps of Engineers, Cross Florida Barge Canal Restudy Report, Summary (1976; University of Florida Digital Collections); The President's "
       "Environmental Program, 1977 (Internet Archive); Public Law 101-640 (1990; govinfo.gov). All in the public domain.")

T = {
    "id": "undoing", "titel": "Undoing the canal", "jahr": "1971–1990",
    "autor": "A Corps restudy, two Presidents, a governor, the canal's last defenders and its opponents, courts and Congress",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. Almost everything here comes from one hearing, held at Palatka in June 1985, where supporters and opponents of the canal testified on the same day. Newspapers of these years are not printed. The greenway and the dispute over the Rodman dam after 1990 are outlook, not subject.",
    "sections": [
        {"id": "tax", "titel": "Thirty-five years of canal tax (1936–1971)",
         "blurb": "What the canal cost the counties that had voted for it in 1935: $9.3 million in taxes until the halt, and some 50,000 acres of land held by the Canal Authority.",
         "plates": ["h1985_tax"], "viz": "undoing-costs", "units": TAX},
        {"id": "restudy", "titel": "Ill-advised (1976–1977)",
         "blurb": "The Army's restudy counted the Ocklawaha ecosystem and 25,800 acres of forest as costs; President Carter asked Congress to end “this ill-advised project”. Congress did not.",
         "plates": ["restudy1976_p13", "carter1977"], "units": RESTUDY},
        {"id": "palatka", "titel": "Palatka, 10 June 1985",
         "blurb": "At Palatka, where Johnson had broken ground, a House subcommittee heard the governor (“we do not want this canal. Period.”), the canal's last defenders, and Marjorie Carr and the Florida Defenders of the Environment, who told how they had organized against the canal. A year before, the House had kept it alive by 204 to 201.",
         "plates": ["h1985_graham", "h1985_carr", "h1985_carr_statement", "h1985_lee"], "units": PALATKA},
        {"id": "land", "titel": "The land stays taken (1985)",
         "blurb": "Owners whose land had been condemned for the canal sued to get it back. In April 1985 the Supreme Court of Florida held that land taken in good faith stays taken, even if the canal is never built.",
         "plates": ["h1985_mainer", "h1985_mainer_owners"], "units": LAND},
        {"id": "end", "titel": "The end, and a greenway (1990)",
         "blurb": "On 28 November 1990 Congress provided that the canal be deauthorized once Florida agreed to keep a greenway across the State and to repay the six counties $32 million.",
         "plates": ["pl1990_a", "pl1990_b"], "units": END},
    ],
}
for s in T["sections"]:
    s["zk"] = "Undoing the canal, " + re.sub(r" \(.*", "", s["titel"]).replace("Palatka, 10 June 1985", "Palatka")
(D / "undoing.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
HP = "House hearing, Cross-Florida Barge Canal, Palatka, 10 June 1985 (GPO 1986)"
IA = "Internet Archive; public domain."
NEW = [
    {"id": "h1985_tax", "side": "land", "titel": "$9,340,720 in canal taxes", "caption": "The navigation district's taxes 1936–1971, and the 50,000 acres held by the Canal Authority.", "source": HP + ", p. 91; " + IA},
    {"id": "restudy1976_p13", "side": "river", "titel": "“Lost as an entity”, 1976", "caption": "The Corps of Engineers' restudy: the Oklawaha River Basin ecosystem lost, 25,800 acres of productive forest.", "source": "Corps of Engineers, Cross Florida Barge Canal Restudy Report, Summary (1976), p. 13; University of Florida Digital Collections; public domain."},
    {"id": "carter1977", "side": "capitol", "titel": "“This ill-advised project”, 1977", "caption": "President Carter's environmental message of 23 May 1977.", "source": "The President's Environmental Program, 1977, p. M-10; " + IA},
    {"id": "h1985_graham", "side": "capitol", "titel": "“We do not want this canal. Period.”", "caption": "Governor Bob Graham's statement to the House subcommittee at Palatka.", "source": HP + ", p. 26; " + IA},
    {"id": "h1985_carr", "side": "river", "titel": "“The notorious Ms. Carr”, 1985", "caption": "Marjorie Harris Carr begins the testimony of the Florida Defenders of the Environment.", "source": HP + ", p. 140; " + IA},
    {"id": "h1985_carr_statement", "side": "river", "titel": "Fifty cents on the dollar", "caption": "Marjorie Carr's prepared statement: rivers damaged, forests lost, a benefit/cost ratio of about .50 to 1.", "source": HP + ", p. 169; " + IA},
    {"id": "h1985_lee", "side": "capitol", "titel": "204 to 201", "caption": "Charles Lee of the Florida Audubon Society on the House vote of 28 June 1984.", "source": HP + ", p. 147; " + IA},
    {"id": "h1985_mainer", "side": "land", "titel": "Mainer v. Canal Authority, 1985", "caption": "The Supreme Court of Florida on nine owners' suits to reacquire their land.", "source": HP + ", p. 226 (exhibit); " + IA},
    {"id": "h1985_mainer_owners", "side": "land", "titel": "How the land was taken", "caption": "The court lists each owner and how the Canal Authority acquired the land, 1966–1970.", "source": HP + ", p. 227 (exhibit); " + IA},
    {"id": "pl1990_a", "side": "land", "titel": "Deauthorized, 28 November 1990", "caption": "Public Law 101-640, section 402: deauthorization, transfer of the lands, a greenway at least 300 yards wide.", "source": "104 Stat. 4644; U.S. Statutes at Large, govinfo.gov; public domain."},
    {"id": "pl1990_b", "side": "land", "titel": "$32,000,000 for the counties", "caption": "The State to pay the six counties of the canal district.", "source": "104 Stat. 4645; U.S. Statutes at Large, govinfo.gov; public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "undoing"), None) or next(x for x in M["shipped"] if x["id"] == "undoing")
M["planned"] = [x for x in M["planned"] if x["id"] != "undoing"]
m.update({"datei": "undoing", "zk": "Tax · Restudy · Palatka · Land · End",
          "kurz": "8 · Undoing the canal",
          "warum": "$9.3 million in county taxes; an Army restudy counting a river ecosystem as lost; Carter's “ill-advised project”; at Palatka in 1985 a governor's “we do not want this canal. Period.” and Marjorie Carr's “the notorious Ms. Carr”; owners who could not get their land back; and in 1990 the end, a greenway and $32 million for the counties.",
          "quelle": "House hearing, Palatka, 1985; Corps restudy 1976; The President's Environmental Program 1977; Public Law 101-640 (1990)."})
order = ["ridge", "river", "relief", "camp", "aquifer", "war", "rodman", "undoing"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "undoing"] + [m], key=lambda x: order.index(x["id"]))
ADD = [{"id": "carr1989", "side": "river", "kurz": "Marjorie Carr's oral history (1989)",
        "warum": "The Samuel Proctor Oral History Program of the University of Florida holds an interview with Marjorie Carr of 24 April 1989 (transcript online in the University of Florida Digital Collections, UF00024777). It is published under a Creative Commons Attribution Non-Commercial licence, not in the public domain; no audio was found online. It is named here, not printed.",
        "quelle": "University of Florida Digital Collections UF00024777; Samuel Proctor Oral History Program."},
       {"id": "laws1979", "side": "land", "kurz": "Florida's act of 1979 on Lake Rousseau",
        "warum": "Chapter 79-167, Laws of Florida, on the state lands around Lake Rousseau and the canal right-of-way to the Withlacoochee, is available only as a text file, without page image; not yet printed.",
        "quelle": "Laws of Florida 1979, ch. 79-167 (UFDC UF00052140)."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "memorials", "titel": "Florida asks, 1933 and 1985",
     "frage": "What did Florida's legislature ask of Washington?",
     "note": "In 1933 a joint memorial asked the President for a canal that would employ “a vast amount of human labor”. In 1985 a memorial, passed 105 to 5 and 33 to 3, asked Congress to deauthorize it.",
     "voices": [{"text": "relief", "sec": "authority", "n": [3], "wer": "Florida Legislature, 1933"},
                {"text": "undoing", "sec": "palatka", "n": [1], "wer": "Governor Bob Graham, 1985"}]},
    {"id": "counties", "titel": "The counties pay, the counties are repaid",
     "frage": "Who carried the cost of the right-of-way, and who got it back?",
     "note": "Only property owners voted the bonds of 1935; the counties then taxed everyone for thirty-five years. In 1990 the law repaid the six counties $32 million. The owners whose land was condemned did not get it back.",
     "voices": [{"text": "relief", "sec": "bonds", "n": [2], "wer": "Representative W. J. Sears, 1936"},
                {"text": "undoing", "sec": "tax", "n": [1], "wer": "Hearing, 1985"},
                {"text": "undoing", "sec": "end", "n": [2], "wer": "Public Law 101-640, 1990"}]},
    {"id": "ratio", "titel": "Does it pay? 1880, 1937, 1985",
     "frage": "Was the canal worth its cost?",
     "note": "Gillmore in 1880 thought a national canal need not pay. Markham in 1937 found benefits $100,000 a year above charges, and more if wages counted as relief. In 1985 the opponents put the ratio at fifty cents on the dollar or less.",
     "voices": [{"text": "ridge", "sec": "company", "n": [2], "wer": "Q. A. Gillmore, 1880"},
                {"text": "aquifer", "sec": "board", "n": [4], "wer": "E. M. Markham, 1937"},
                {"text": "undoing", "sec": "palatka", "n": [5], "wer": "John H. Kaufmann, 1985"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/undoing/"
for s in TL["stations"]:
    if s["titel"] == "“Ill-advised”":
        s.update({"cite": K + "restudy/2", "citeLabel": "Undoing the canal, 1977 [2]", "plate": "carter1977"})
    if s["titel"] == "204 to 201":
        s.update({"cite": K + "palatka/6", "citeLabel": "Undoing the canal, 1985 [6]", "plate": "h1985_lee"})
    if s["titel"] == "The end, and a greenway":
        s.update({"cite": K + "end/1", "citeLabel": "Undoing the canal, 1990 [1]", "plate": "pl1990_a"})
NEWST = [
    {"d": "August 1976", "side": "river", "titel": "The restudy",
     "text": "The Corps of Engineers counts the loss of the Oklawaha River Basin ecosystem and 25,800 acres of productive forest under the authorized plan.",
     "cite": K + "restudy/1", "citeLabel": "Undoing the canal, 1976 [1]", "plate": "restudy1976_p13",
     "quelle": "Cross Florida Barge Canal Restudy Report, Summary (1976), p. 13."},
    {"d": "18 April 1985", "side": "land", "titel": "The land stays taken",
     "text": "The Supreme Court of Florida rejects nine owners' suits to reacquire land condemned for the canal.",
     "cite": K + "land/2", "citeLabel": "Undoing the canal, 1985 [2]", "plate": "h1985_mainer",
     "quelle": "Mainer v. Canal Authority (1985), printed in the House hearing of 1985, pp. 226–227."},
    {"d": "10 June 1985", "side": "river", "titel": "Hearing at Palatka",
     "text": "Governor Graham: “we do not want this canal. Period.” Marjorie Carr tells how the Florida Defenders of the Environment organized against it.",
     "cite": K + "palatka/3", "citeLabel": "Undoing the canal, 1985 [3]", "plate": "h1985_carr",
     "quelle": "House hearing, Cross-Florida Barge Canal, Palatka, 10 June 1985, pp. 26, 139–140."},
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
