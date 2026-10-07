"""Builds data/ridge.json (module 1: The ridge, 1826–1909) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/ridge/PRUEFUNG.md):
  Senate Document 21, 19th Congress, 1st Session (1826), pp. 1, 9–10 (govinfo SERIALSET-00126_00_00-003-0021-0000);
  House Document 8, 23rd Congress, 2nd Session (1834), pp. 65–66, 72–73, 75 (SERIALSET-00271_00_00-010-0008-0000);
  House Document 185, 22nd Congress, 1st Session (1832), pp. 2–3, 6, 8, 44 (SERIALSET-00219_00_00-083-0185-0000);
  Senate Executive Document 76, 33rd Congress, 2nd Session (1855), pp. 2, 12 (SERIALSET-00756_00_00-014-0076-0000);
  Senate Executive Document 154, 46th Congress, 2nd Session (1880), pp. 2, 14–15 and map (SERIALSET-01885_00_00-056-0154-0000);
  Ocala Banner-Lacon, 26 May 1883 (UFDC AA00089092/00041); Ocala Banner, 1 September 1883 (UF00048734/01281);
  The Pensacolian, 23 August 1884 (UFDC AA00083042/00037);
  Ocala Evening Star, 21 May 1909 (UFDC UF00075908/03173).
All in the public domain (works of the United States government; newspapers published before 1931).
Run from the site root: python tools/build-ridge.py
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


SD21 = "Senate Document 21, 19th Congress, 1st Session"
HD8 = "House Document 8, 23rd Congress, 2nd Session"
HD185 = "House Document 185, 22nd Congress, 1st Session"

SENATE = [
    u(1, SD21 + ", 19 January 1826, p. 1",
      "Mr. Hendricks, from the Select Committee on Roads and Canals, to whom was referred “A Bill for the Survey of a route for a Canal between the Atlantic and the Gulf of Mexico,” Reported: That they have given the subject all the examination which the means afforded enabled them to bestow. No documents accompanying the bill, they have availed themselves of the information of several gentlemen acquainted with the character of the country through which the proposed canal is intended to pass, and from the best lights afforded, they have no hesitation in forming the opinion, that the great importance of a canal communication between the waters of the Atlantic coast and the Gulf of Mexico, justifies the expenditure proposed, to determine the fact whether such communication be practicable or not. Nor would the committee hesitate in recommending the measure, were the probability of a favorable result to the examination much more remote than it is. The Committee are of opinion, from all the information which they have been able to procure, that this work is not only practicable, but much more easily accomplished than former estimates and opinions have supposed.",
      "“Not only practicable”",
      "The first word of Congress on a canal across Florida. The committee had no survey before it, only the information of “several gentlemen” and the letter of Florida's delegate that follows. Congress passed the survey act on 3 March 1826 ([1] in the next section)."),
    u(2, SD21 + ", p. 9: Joseph M. White, Delegate from the Territory of Florida, 18 January 1826",
      "The navigation around the capes of Florida is the most dangerous on the American coast. The Tortugas banks, Florida reefs, and shoals of the Bahamas, combined with the depredations of pirates, occasion to our citizens an annual loss estimated at five hundred thousand dollars. It would be needless to say that this canal or cut would furnish a safe navigation, as well as a short one, and the annual loss we now sustain would be doubly, perhaps four-fold sufficient to complete it.",
      "The most dangerous coast",
      "The first of the canal's reasons, and the longest-lived: the passage round the Florida reefs. The figure of $500,000 a year is White's estimate; he does not say where it comes from."),
    u(3, SD21 + ", p. 9",
      "The great duty of a Government is to defend the territory committed to its charge, and its first policy, to invite emigration to its borders. The United States have in Florida about twenty millions of acres of lands. These have been partly surveyed, and one inconsiderable sale effected, and much of it is yet unknown and unexplored. By this canal, emigration would be invited to the interior, and extend its progress to the rich streams with which it would communicate. Farm houses and villages would spring up in what is now a wilderness, and the tide of population roll on to the shores of the ocean. Lands which are now a lake or morass, would bloom with rice or cotton.",
      "“What is now a wilderness”",
      "The second reason: land. The interior White calls “unknown and unexplored” and “a wilderness” was not empty; the letter says nothing of the Seminole and other people who lived there. Rice and cotton were, in the South of the 1820s, plantation crops worked by enslaved people; the letter does not say who would grow them."),
    u(4, SD21 + ", p. 10",
      "No naval force can approach their haunts, embosomed in creeks, forests, and morasses. No piratical force can approach our commerce, embosomed in a canal, through the heart of our country. The islands that afford them shelter, are approached no longer, and the vile trade is destroyed by robbing them of their victims. Such ports as Key West will no longer be a grave-yard for our brave seamen, and the occupation of their shores will cease with the cessation of their cause and necessity: our navy may then breathe a purer atmosphere, and boast a nobler service.",
      "Against the pirates"),
    u(5, SD21 + ", p. 10",
      "These, sir, are some few of its advantages in time of peace; but, should our happy country be again visited with the calamities of war, we should have, from Massachusetts to Mississippi, from Mississippi to St. Augustine, from one end to the other of our wide-spread empire, one connected chain of internal communication.",
      "In time of war",
      "The argument of war, made in 1826 against Britain and the pirates of the Caribbean, returned in 1855 ([3] in “A railroad instead”) and carried the act of 1942 (module 6)."),
    u(6, HD8 + ", p. 72–73: J. M. White to C. F. Mercer, chairman of the House Committee on Roads and Canals, December 1826",
      "The Territory of Florida, which is capable of producing nearly all the articles of Cuba, has scarcely attracted, in five years which it has been in the possession of the United States, any attention, in consequence of the desolation occasioned by the invasion of 1812, from which it is but just now recovering. … It is estimated that an orange grove of ten acres, which requires the attention of but two hands, will produce as much as a cotton or sugar plantation by the employment and labor of forty.",
      "Two hands or forty",
      "Eleven months later, before any survey had reported, White wrote again. The “hands” on a cotton or sugar plantation of the 1820s were, as a rule, enslaved people; White counts them only as a cost of labour. “The invasion of 1812” is White's phrase; he does not say who invaded, or whom the desolation struck."),
    u(7, HD8 + ", p. 75",
      "The improvement of the Territory is nothing more than an improvement of the property of the nation; and to neglect any means of promoting their prosperity, would be as unwise as for a parent to neglect the patrimony of his children during their minority. It has been a part of the policy of every liberal and enlightened Government to promote its provinces and colonies; and we may hope that works combining such singular and pre-eminent advantages will be executed by the United States.",
      "“Provinces and colonies”"),
]

BOARD = [
    u(1, HD185 + ", p. 8: message of President John Quincy Adams, 25 February 1829",
      "By the act of Congress of the third of March, 1826, for the survey of a route for a canal between the Atlantic and the Gulf of Mexico, the President of the United States was authorized to cause to be made an accurate and minute examination of the country south of the St. Mary's river, and including the same, with a view to ascertain the most eligible route for a canal admitting the transit of boats to connect the Atlantic with the Gulf of Mexico, and also with a view to ascertain the practicability of a ship channel; … In execution of this law, I transmit herewith a report from the Secretary of War, with a copy of that of the Board of Engineers upon this great and most desirable national work.",
      "“This great and most desirable national work”",
      "The act of 1826 asked two questions: the best route for a canal for boats, and whether a ship channel was practicable at all. The engineers answered them differently ([3], [4])."),
    u(2, HD185 + ", p. 44: report of the Board of Engineers for Internal Improvement, 1829",
      "The line, after leaving the head of Hillsborough bay, follows the military road as far as the old Indian town O-ke-hum-ky, hence, it takes an easterly course to Ocklawaha river. … The dividing point of the Florida ridge is near the 76th mile, about four miles west of the Ocklawaha swamp: its elevation above the gulf has proved to be but 87 feet. … The foregoing results show sufficiently that, though the top of the Florida ridge be very low in this direction, yet, the want of water precludes the practicability of connecting, by a canal, the Ocklawaha, with either the Amaxura or Hillsborough river. We shall, therefore, dismiss the subject, and pass to the investigation of the St. Mary's and St. John's routes of canal.",
      "The Ocklawaha, dismissed",
      "In 1829 the engineers looked at the Ocklawaha and set it aside for want of water at the summit. The barge canal begun in 1964 ran up the Ocklawaha valley (module 7). The “old Indian town” on the military road appears only as a landmark; who lived there, and what became of them, the report does not say."),
    u(3, HD8 + ", pp. 65–66: Bernard and Poussin, summary, Washington, 19 February 1829",
      "The coast on the Gulf of Mexico, between Tampa bay and Appalachie bay, cannot be approached by vessels drawing more than five feet; in this latter bay eight feet can be carried, at high tide, to St. Mark's. Besides, the ridge of the peninsula of Florida has a mean elevation of one hundred and fifty feet above the ocean, and its top does not offer, at any place, either natural reservoirs or heads of streams adequate to the supply of a canal having very large dimensions. Therefore, a ship channel, destined to connect, through the peninsula, the Atlantic with the Gulf of Mexico, is not practicable.",
      "“Not practicable”",
      "The sentence that gives this apparatus its name. Two reasons: no harbour on the Gulf side deep enough for ships, and no water on the ridge for a canal of ship size. The summary is signed by Brigadier General Simon Bernard, member of the Board of Internal Improvement, and Captain William Tell Poussin of the Topographical Engineers."),
    u(4, HD8 + ", p. 66",
      "The heads of Santa Fé river and of Black creek present to a canal for boats the best passage across the summit of the ridge. Natural reservoirs, in this vicinity, will supply the lockage at the dividing point, whilst it is anticipated that filtration from the ground will keep replenished the trunk of the summit level. In this direction, a canal from the fork of Black creek to the mouth of the Santa Fé would connect the St. John's with the Suwanee; therefore, the Atlantic with the Gulf. Such a canal would be about seventy-eight miles in length, and the ascent and descent together two hundred and fourteen feet.",
      "A canal for boats",
      "What the engineers thought possible: a canal for boats, not ships, from the St. Johns to the Suwannee, fed by ponds and by water seeping in from the ground. Whether the ground would give that water was the question sent back to Florida in 1830."),
]

WATER = [
    u(1, HD185 + ", p. 2: Lieutenant John Pickell to Lieutenant Colonel J. J. Abert, Washington, 6 March 1832",
      "The object contemplated by those instructions, having been principally to determine the quantity of water that could be obtained by infiltration, for the supply of the summit pass, my attention was directed, immediately after my arrival in Florida, to the accomplishment of this duty. … The quantity of water required for the supply of the prism of the canal and lockages at the summit, allowing for absorption and evaporation, is 66,087,450 cubic yards. By the report of the Board of Internal Improvements, dated February 19, 1829, the bottom of the canal upon the summit, as contemplated, is 116 4/10 feet above the level of the water in the Atlantic.",
      "Water for the summit",
      "Pickell sank four timbered shafts on the ridge between Black Creek and the Santa Fe and measured how fast water came in."),
    u(2, HD185 + ", p. 3",
      "At the depth of 20 feet 6 inches, a subterranean stream was encountered, and the further excavation of the shaft was necessarily abandoned.",
      "A stream under the ridge",
      "First shaft in the valley of Bull Creek. A hundred years later the water under the ridge became the strongest argument against the canal: the fear that a deep cut would drain or salt the underground water of central Florida (module 5)."),
    u(3, HD185 + ", p. 6",
      "Kingsley's pond, 15,483,052 cubic yards. Little Santa Fe pond, 7,734,236. Big Santa Fe pond, or Aquila lake, 37,932,350. Pond of the Woods, 4,682,030. Trout pond, 12,280,360. Summit pond, 1,932,620. Head of S. prong Black creek, 2,199,132. Making an aggregate of 111,970,888 cubic yards, or an excess of 45,883,438 cubic yards over the quantity required for the summit level of the canal and lockage.",
      "Enough water, for boats",
      "Pickell's answer: the ponds near the summit hold more than enough water for a canal for boats. The table is set here as running text; the print sets it in columns."),
    u(4, HD185 + ", p. 6",
      "The ridge dividing the waters running into the Gulf of Mexico, from those emptying into the Atlantic, is encountered between Kingsley's pond, and the head of the Horse Shoe. It is traversed at an elevation of 116.849 feet above the line of reference.",
      "The height of the ridge",
      "Measured, not averaged: where Pickell's line crossed it, the ridge stood about 117 feet above the reference level. A canal for boats was possible; none was built."),
]

RAILS = [
    u(1, "Senate Executive Document 76, 33rd Congress, 2nd Session (3 March 1855), p. 2: J. J. Abert to Lieutenant M. L. Smith, 22 November 1853",
      "I transmit you a copy of a letter from Mr. Call. Although a survey for a railroad cannot be directed under the appropriation which supplies the means of your present duties, yet, in making the survey for the canal route, your attention can at the same time be given to the properties for a railroad possessed by the canal survey, and this subject can be made to occupy a part of your ultimate report.",
      "A railroad on the canal's money",
      "A new canal survey had been funded by the act of 30 August 1852. The chief of the Topographical Engineers allows its officer to look at a railroad at the same time, although the money was not voted for one."),
    u(2, "Senate Executive Document 76, p. 2: M. L. Smith to J. J. Abert, Washington, 2 March 1855",
      "The object of the canal survey having been the connexion of the Atlantic and Gulf, for the benefit of commerce, more especially that portion of it which passes around the Florida keys, in speaking of a railroad connecting these waters it seems proper, since the object of the two works is the same, that the discussion of them should be somewhat similar in character; hence, the proper location of the road, estimates of its cost, and its connexion with the interests of the country, will be considered. Any view of the subject more general than this could amount to little more than saying what most are at present aware of, viz: that the country affords unusual facilities for such a work, since it is rather flat, has no mountains or ridges but what can be readily crossed at any given point or traversed their entire length without difficulty, no rivers not susceptible of being easily bridged, and timber of good quality is in abundance. I will add that the canal surveys gave accurate and minute data that could be readily applied to the subject specified in your instructions.",
      "“No mountains or ridges”",
      "The ridge that stopped the ship canal in 1829 is no obstacle to a railroad. Smith's line runs from Fernandina, at the mouth of the St. Marys, to Cedar Key on the Gulf: the route of the Florida Railroad that was then being built."),
    u(3, "Senate Executive Document 76, p. 12",
      "To force trade along any but natural channels is virtually to suppress it, and if in the case of hostilities, as supposed, the interior lines of railroad only existed, doubtless the great staple articles of Gulf trade which happen to be bulky, viz: cotton, sugar, and molasses, would be detained from market, or find their way there at expenses so greatly exaggerated as would be equivalent to a detention. In conclusion: the object of the preceding remarks has been to show the necessity as well as utility of a direct connexion between the Atlantic and Gulf across Florida, from— 1st. The heavy increased insurance the dangerous navigation through the straits of Florida imposes on the Gulf trade. 2d. The loss of time, consequently the loss of interest on capital employed in that trade. 3d. The increased mail facilities that would be opened. 4th. The security that would be given to our commerce, particularly that coming under the head of coasting trade, during a period of hostilities.",
      "Four reasons",
      "Insurance, time, mail and war: White's reasons of 1826, now argued for a railroad. The “great staple articles” Smith names, cotton, sugar and molasses, were in 1855 grown and made largely by enslaved people; the report speaks only of freight."),
]

COMPANY = [
    u(1, "Senate Executive Document 154, 46th Congress, 2nd Session (22 April 1880), p. 2: Lieutenant Colonel Q. A. Gillmore, New York, 6 April 1880",
      "Congress by act approved June 18, 1878, directed an examination to be made of the peninsula of Florida, with a view to the construction of a ship-canal from the Saint Mary's River to the Gulf of Mexico. The duty of making this examination was assigned to me by the Chief of Engineers, under date July 8, 1878, and an allotment of $7,500 was made for this object. It was understood that with this sum such an examination could be made as would determine the feasibility of the project of a peninsula ship-canal, and furnish data for an approximate estimate of its cost.",
      "Seven thousand five hundred dollars",
      "Fifty years after Bernard, Congress asks again about a ship canal, on a northern line from the St. Marys through the Okefenokee country to the Gulf."),
    u(2, "Senate Executive Document 154, p. 14",
      "From a national point of view a Florida Ship-Canal is an object of importance, as part of a comprehensive scheme for improving and cheapening our means of water transportation from the heart of our grain and cotton growing regions to foreign ports, and there would seem to be as little need of attempting to fix its rentable or money-earning value as in undertaking to apply the same rule to the works of river and harbor improvement prosecuted by the United States Government.",
      "No need to make it pay",
      "Gillmore argues that a national waterway need not earn its cost. Every later report on the canal, from 1937 to 1985, turned on the opposite question: whether its benefits outweighed its costs (modules 5, 7 and 8)."),
    u(3, "Senate Executive Document 154, pp. 14–15",
      "The Florida Ship-Canal is estimated to cost about $50,000,000, and, as already stated, the aggregate tonnage which passed through the Florida Straits during the last fiscal year amounted to about 2,600,000 tons. All of this could have saved 12 to 14 hours in time of transit if the Florida Canal had existed. To earn the current expenses for administration and maintenance, about 1,758,000 tons must go through the canal annually at 28 cents per ton toll. To earn the current expenses and 5 per cent. on the cost of construction, about 10,714,300 tons must pass through the canal at 28 cents per ton toll. … It is probable that some years after the completion of the canal, if constructed at an early day, enough tonnage would use that passage to pay current expenses, perhaps somewhat more. But it is impossible to answer satisfactorily the question of the capacity of the enterprise to yield a moderate interest on the capital invested.",
      "Fifty million dollars",
      "His own figures: to pay five per cent on its cost, the canal would need about four times the traffic that passed the Florida Straits in a year."),
    u(4, "Ocala Banner-Lacon, 26 May 1883, p. 2",
      "Twenty-six million dollars has been subscribed to the capital stock of the Florida Ship Canal, and work will commence at once.",
      "“Work will commence at once”",
      "A private company now. The notice gives no source for the figure, and no work began."),
    u(5, "Ocala Banner, 1 September 1883, p. 3: Charles P. Stone, chief engineer, to John C. Brown, president, New York, 15 August 1883",
      "The Florida Ship Canal. Its ultimate success is now a fixed fact. … Taking that route as a basis, I have computed that a tidewater ship canal of sufficient width and depth to allow the passage of two sea going steamers of the first class without inconvenience, can be constructed at a total cost of $46,000,000, as follows: Excavations, $36,000,000; harbors at termini, $4,500,000. The total length of the canal would be one hundred and thirty-seven and a half miles, and the highest elevation in crossing the watershed one hundred and forty-three feet, but this deep cut would be only for a short distance. A large amount of excavating can be made by steam dredges. As a whole, I am able to report that the engineering difficulties are decidedly less than I expected.",
      "“A fixed fact”",
      "A canal at sea level, cut through a watershed of 143 feet, for less than Gillmore's lock canal. The two items Stone lists add up to $40,500,000, not $46,000,000; the rest is not itemized in the summary as printed."),
    u(6, "Ocala Banner, 1 September 1883, p. 3",
      "The gain by avoiding the dangerous passage through the Florida Straits is very great. The official statistics of five recent years show that three hundred and twenty-six salvage cases were adjudicated in the United States District Court for the Southern District of Florida, to the value of more than $11,000,000, and careful estimates show the present loss from wreckage to be about $3,000,000 per year.",
      "Wrecks and salvage"),
    u(7, "The Pensacolian, 23 August 1884, p. 1",
      "We learn from the Florida Herald that the far-famed, Florida Ship Canal, has gone up in a soap bubble and bursted. The employes of the company are entering suit against the directors for unpaid salaries.",
      "“A soap bubble”",
      "A year after the “fixed fact”. The note names no one; who the company's employees were, and whether they were ever paid, has not been found."),
]

ROUTES = [
    u(1, "Ocala Evening Star, 21 May 1909, p. 1",
      "Florida Ship Canal. Work of Surveying the Routes Will Commence at Once. Savannah, Ga., May 21.—The board of officers of the corps of engineers appointed to recommend routes for a survey for a canal across the northern part of the state of Florida, from east to west, will recommend to the war department a survey of five routes, 1,000 miles in all at a cost of approximately $25,000. The canal routes to be surveyed will aggregate very much more than the Panama canal survey and will require several months to complete with five parties of surveyors at work. It is reported that if the plan of survey is approved the work will begin at once. The shortest line from coast to coast contemplated is 110 miles, with other surveys necessitated making each route survey approximately 200 miles. The officers who compose the board of engineers at work on this problem are Col. Dan C. Kingman, of Savannah; Capt. Earl I. Brown, Wilmington, N. C.; Capt. E. M. Adams, Charleston, S. C.; Capt. George S. Spalding, Jacksonville.",
      "Five routes",
      "Eighty years after Bernard, the Army's engineers set out once more. The surveys of the years before the First World War, and the newspaper campaigns for the canal in Ocala, belong to the prehistory of the 1930s; they are not yet printed here."),
]

SRC = ("Senate Document 21, 19th Congress, 1st Session (1826); House Document 8, 23rd Congress, 2nd Session (1834), "
       "reprinting the report of S. Bernard and W. T. Poussin of 19 February 1829 and J. M. White's letter of December 1826; "
       "House Document 185, 22nd Congress, 1st Session (1832), with J. Pickell's report and the Board of Engineers' report of 1829; "
       "Senate Executive Document 76, 33rd Congress, 2nd Session (1855); Senate Executive Document 154, 46th Congress, 2nd Session (1880): "
       "all U.S. Congressional Serial Set, scans of govinfo.gov. Ocala Banner-Lacon, 26 May 1883; Ocala Banner, 1 September 1883; The Pensacolian, 23 August 1884; "
       "Ocala Evening Star, 21 May 1909: Florida Digital Newspaper Library, University of Florida. All in the public domain.")

T = {
    "id": "ridge", "titel": "The ridge", "jahr": "1826–1909",
    "autor": "Florida's delegate in Congress, the Army's engineers, a canal company and the newspapers",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. Tables are set as running text. The sources of this module are almost all written for a canal: by Florida's delegate, by engineers asked whether it could be built, by a company selling its stock. The people who lived along the routes, Seminole, enslaved and free, do not speak in them; where a passage passes over them, the note says so.",
    "sections": [
        {"id": "senate", "titel": "A canal for the territory (1826)",
         "blurb": "Florida had been a territory of the United States for five years when its delegate asked Congress for a canal across the peninsula: against the reefs and the pirates, for settlers and their crops, and for war. A Senate committee thought it “not only practicable, but much more easily accomplished” than supposed.",
         "plates": ["sdoc1826_report"], "units": SENATE},
        {"id": "board", "titel": "Not practicable (1829)",
         "blurb": "The survey ordered in 1826 reported in February 1829. The engineers looked at the Ocklawaha and dismissed it for want of water; they found the ridge of the peninsula a hundred and fifty feet high on average, and a ship channel through it “not practicable”. A canal for boats was another matter.",
         "plates": ["board1829_summary", "board1829_ocklawaha"], "viz": "ridge-heights", "units": BOARD},
        {"id": "water", "titel": "Water for the summit (1832)",
         "blurb": "Sent back to measure the water that would seep into a summit cut, a lieutenant of the Topographical Engineers sank shafts on the ridge, struck an underground stream, and found the ponds near the summit full enough for a canal for boats.",
         "plates": ["pickell1832_ponds"], "units": WATER},
        {"id": "rails", "titel": "A railroad instead (1853–1855)",
         "blurb": "Twenty years later another canal survey became, on the side, a railroad survey. The ridge that stopped the ship channel was no obstacle to a railroad from Fernandina to Cedar Key, and the reasons for crossing Florida stayed the same: insurance, time, mail and war.",
         "plates": ["smith1855_railroad"], "units": RAILS},
        {"id": "company", "titel": "Fifty million dollars, and a soap bubble (1880–1884)",
         "blurb": "In 1880 the Army's engineers put a ship canal at fifty million dollars and declined to say whether it could ever pay. In 1883 a private company announced twenty-six million dollars subscribed and its success “a fixed fact”; a year later it had “gone up in a soap bubble”, and its employees were suing for their pay.",
         "plates": ["gillmore1880_map", "obl1883_subscribed", "ob1883_fixedfact", "pens1884_bubble"], "viz": "ridge-costs", "units": COMPANY},
        {"id": "routes", "titel": "Five routes (1909)",
         "blurb": "In 1909 a board of Army engineers proposed to survey five routes across northern Florida. The canal had become a question that came back every generation.",
         "plates": ["oes1909_routes"], "units": ROUTES},
    ],
}
for s in T["sections"]:
    s["zk"] = "The ridge, " + re.sub(r" \(.*", "", s["titel"])
(D / "ridge.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
SER = "U.S. Congressional Serial Set, scan of govinfo.gov; public domain."
UF = "Florida Digital Newspaper Library, University of Florida; public domain."
NEW = [
    {"id": "sdoc1826_report", "side": "capitol", "titel": "In the Senate, 19 January 1826",
     "caption": "The report of the Senate's Select Committee on Roads and Canals on the bill for a survey of a canal route between the Atlantic and the Gulf: the work “not only practicable, but much more easily accomplished than former estimates and opinions have supposed.”",
     "source": "Senate Document 21, 19th Congress, 1st Session, p. 1. " + SER},
    {"id": "board1829_summary", "side": "survey", "titel": "“Not practicable”, 1829",
     "caption": "The summary of Bernard and Poussin's report of 19 February 1829, from the foot of p. 65 to the head of p. 66, set together: the ridge of the peninsula 150 feet high on average, a ship channel “not practicable.”",
     "source": "House Document 8, 23rd Congress, 2nd Session, pp. 65–66. " + SER},
    {"id": "board1829_ocklawaha", "side": "river", "titel": "The Ocklawaha dismissed, 1829",
     "caption": "The engineers' line from Tampa Bay past the “old Indian town O-ke-hum-ky” to the Ocklawaha: the ridge only 87 feet high there, but “the want of water precludes the practicability” of a canal.",
     "source": "House Document 185, 22nd Congress, 1st Session, p. 44. " + SER},
    {"id": "pickell1832_ponds", "side": "water", "titel": "Ponds on the summit, 1832",
     "caption": "Lieutenant Pickell's count of the water in the ponds near the summit: an excess of 45,883,438 cubic yards over what a canal for boats would need.",
     "source": "House Document 185, 22nd Congress, 1st Session, p. 6. " + SER},
    {"id": "smith1855_railroad", "side": "survey", "titel": "A railroad survey, 1853–1855",
     "caption": "The instruction of November 1853 allowing the officer of the canal survey to examine a railroad as well, and the opening of his report on a line from Fernandina to Cedar Key.",
     "source": "Senate Executive Document 76, 33rd Congress, 2nd Session, p. 2. " + SER},
    {"id": "gillmore1880_map", "side": "survey", "titel": "A ship canal from the St. Marys, 1879",
     "caption": "Map of the country embraced in the preliminary survey for a ship canal from the St. Marys River to the Gulf of Mexico, made in 1879 under Brevet Major General Q. A. Gillmore, with the profile of the canal across the ridge below.",
     "source": "Senate Executive Document 154, 46th Congress, 2nd Session (1880), folding map. " + SER},
    {"id": "obl1883_subscribed", "side": "land", "titel": "Twenty-six million dollars, 1883",
     "caption": "“Twenty-six million dollars has been subscribed to the capital stock of the Florida Ship Canal, and work will commence at once.”",
     "source": "Ocala Banner-Lacon, 26 May 1883, p. 2. " + UF},
    {"id": "ob1883_fixedfact", "side": "land", "titel": "“A fixed fact”, 1883",
     "caption": "The directors of the Florida Ship Canal and Transit Company adopt their chief engineer's report: a tidewater ship canal for $46,000,000.",
     "source": "Ocala Banner, 1 September 1883, p. 3, detail. " + UF},
    {"id": "pens1884_bubble", "side": "work", "titel": "“A soap bubble”, 1884",
     "caption": "“… has gone up in a soap bubble and bursted. The employes of the company are entering suit against the directors for unpaid salaries.”",
     "source": "The Pensacolian, 23 August 1884, p. 1. " + UF},
    {"id": "oes1909_routes", "side": "survey", "titel": "Five routes, 1909",
     "caption": "A board of Army engineers at Savannah proposes to survey five routes across northern Florida, a thousand miles in all.",
     "source": "Ocala Evening Star, 21 May 1909, p. 1. " + UF},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["lede"] = "Public-domain maps, documents and photographs, each with its source."
P["credit"] = ("Pages and maps of congressional documents from the U.S. Congressional Serial Set, scans of govinfo.gov; "
               "newspaper pages from the Florida Digital Newspaper Library, University of Florida. All in the public domain.")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "ridge"), None) or next(x for x in M["shipped"] if x["id"] == "ridge")
M["planned"] = [x for x in M["planned"] if x["id"] != "ridge"]
m.update({"datei": "ridge", "zk": "Territory · Ridge · Water · Railroad · Company · Routes",
          "kurz": "1 · The ridge",
          "warum": "In 1826 Florida's delegate wanted a canal against the reefs, for settlers and for war, and a Senate committee thought it “not only practicable”. In 1829 the Army's engineers found the ridge 150 feet high and a ship channel “not practicable”. A railroad crossed instead; a canal company of 1883 went “up in a soap bubble”.",
          "quelle": "Senate and House documents of 1826, 1829, 1832, 1855 and 1880; Ocala Banner 1883; The Pensacolian 1884; Ocala Evening Star 1909."})
order = ["ridge", "river", "relief", "camp", "aquifer", "war", "rodman", "undoing"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "ridge"] + [m], key=lambda x: order.index(x["id"]))
ADD = [{"id": "seminole", "side": "land", "kurz": "The people of the interior",
        "warum": "The canal surveys of 1826–1832 pass over the Seminole and other people who lived in the interior of the peninsula; the report of 1829 names an “old Indian town” only as a landmark. Their history in the canal country is not covered by any source read so far; it is named here so that the apparatus does not begin as if the land had been empty.",
        "quelle": "To be found."},
       {"id": "company1883", "side": "land", "kurz": "The canal companies of 1872 and 1883",
        "warum": "The charters reported in the press for a Florida Ship Canal Company (1872) and for the Florida Ship Canal and Transit Company (1883), the company's own reports and the suits of its employees have not yet been read; only newspaper notices are printed here.",
        "quelle": "Laws of Florida 1872 and 1883; Tallahassee Sentinel 1872; Florida Times-Union 1883."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "practicable", "titel": "Practicable, or not",
     "frage": "Could a canal be cut across Florida?",
     "note": "In January 1826, before any survey, a Senate committee thought the work “not only practicable, but much more easily accomplished” than supposed. Three years later the engineers sent to survey it found a ship channel “not practicable”, and a canal for boats possible.",
     "voices": [{"text": "ridge", "sec": "senate", "n": [1], "wer": "Senate committee, 1826"},
                {"text": "ridge", "sec": "board", "n": [3], "wer": "Bernard and Poussin, 1829"}]},
    {"id": "pay", "titel": "Must it pay?",
     "frage": "Should a canal across Florida earn its cost?",
     "note": "Gillmore in 1880 saw “as little need” to fix a national canal's money-earning value as a harbour's, and then showed that it would need four times the traffic of the Florida Straits to pay five per cent. Stone in 1883 promised a cheaper canal and a quick return to a company's shareholders; a year later the company was gone.",
     "voices": [{"text": "ridge", "sec": "company", "n": [2, 3], "wer": "Q. A. Gillmore, 1880"},
                {"text": "ridge", "sec": "company", "n": [5, 7], "wer": "C. P. Stone, 1883; The Pensacolian, 1884"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/ridge/"
LINK = {  # stations of the frame that now point into the module
    "A Senate committee for a canal": (K + "senate/1", "The ridge, 1826 [1]", "sdoc1826_report"),
    "“Not practicable”": (K + "board/3", "The ridge, 1829 [3]", "board1829_summary"),
    "Fifty million dollars": (K + "company/3", "The ridge, 1880–1884 [3]", "gillmore1880_map"),
}
for s in TL["stations"]:
    if s["titel"] in LINK:
        s["cite"], s["citeLabel"], s["plate"] = LINK[s["titel"]]
NEWST = [
    {"d": "6 March 1832", "side": "water", "titel": "Water for a canal for boats",
     "text": "Lieutenant John Pickell reports that the ponds near the summit hold 45,883,438 cubic yards more water than a canal for boats would need. In one of his shafts he strikes an underground stream.",
     "cite": K + "water/3", "citeLabel": "The ridge, 1832 [3]", "plate": "pickell1832_ponds",
     "quelle": "House Document 185, 22nd Congress, 1st Session, pp. 3, 6."},
    {"d": "2 March 1855", "side": "survey", "titel": "A railroad instead",
     "text": "The officer of a new canal survey reports on a railroad from Fernandina to Cedar Key: the country has “no mountains or ridges” a railroad could not cross.",
     "cite": K + "rails/2", "citeLabel": "The ridge, 1855 [2]", "plate": "smith1855_railroad",
     "quelle": "Senate Executive Document 76, 33rd Congress, 2nd Session, p. 2."},
    {"d": "1 September 1883", "side": "land", "titel": "“A fixed fact”",
     "text": "The directors of the Florida Ship Canal and Transit Company adopt their engineer's estimate of $46,000,000 for a tidewater ship canal.",
     "cite": K + "company/5", "citeLabel": "The ridge, 1883 [5]", "plate": "ob1883_fixedfact",
     "quelle": "Ocala Banner, 1 September 1883, p. 3."},
    {"d": "23 August 1884", "side": "work", "titel": "“A soap bubble”",
     "text": "The company has “gone up in a soap bubble and bursted”; its employees sue the directors for unpaid salaries.",
     "cite": K + "company/7", "citeLabel": "The ridge, 1884 [7]", "plate": "pens1884_bubble",
     "quelle": "The Pensacolian, 23 August 1884, p. 1."},
    {"d": "21 May 1909", "side": "survey", "titel": "Five routes",
     "text": "A board of Army engineers proposes to survey five routes across northern Florida, a thousand miles in all.",
     "cite": K + "routes/1", "citeLabel": "The ridge, 1909 [1]", "plate": "oes1909_routes",
     "quelle": "Ocala Evening Star, 21 May 1909, p. 1."},
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
TL["lede"] = "Stations read against the page images of their sources only; each names its source and, where printed, links to its passage."
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
