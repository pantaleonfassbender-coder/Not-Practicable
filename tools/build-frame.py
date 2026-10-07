"""Builds the frame of the apparatus: data/modules.json (planned and missing), data/timeline.json,
and empty data/compare.json and data/plates.json. Module builds (tools/build-<id>.py) later move
modules from "planned" to "shipped" and add their stations, pairs and plates.

    python tools/build-frame.py      (once, before the first module)
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

PLANNED = [
    ("ridge", "survey", "1 · The ridge",
     "In 1826 a Senate committee thought a canal across Florida “not only practicable, but much more easily accomplished” than supposed; in 1829 the Army's engineers found the ridge of the peninsula a hundred and fifty feet high and a ship channel “not practicable”. In 1880 a new survey put a ship canal at about fifty million dollars.",
     "Senate Document 21, 19th Congress (1826); report of Bernard and Poussin, 1829, in House Document 8, 23rd Congress; Gillmore's report, Senate Executive Document 154, 46th Congress (1880); Florida newspapers on the canal companies of 1872 and 1883."),
    ("river", "river", "2 · The water-lane",
     "Before the canal, the Ocklawaha was a steamboat river: a poet's “sweetest water-lane in the world” in 1875, a tourist route of the Hart line, and a channel for logs. What the river carried and who worked on it, from the travel books, timetables and the engineers' reports.",
     "Sidney Lanier, Florida (1875/76); Hart line timetable 1890; photographs of 1886 and 1902; House Document 514, 63rd Congress (1914)."),
    ("relief", "land", "3 · Work for the relief rolls",
     "In 1933 the Florida legislature created a Ship Canal Authority and asked Washington for a canal that would “give employment to a vast amount of human labor”. The six counties of the canal district voted bonds to buy the right of way, in an election open only to property owners who had paid their poll tax.",
     "Documentary History of the Florida Canal (Ship Canal Authority, printed as Senate Document 275, 74th Congress, 1936); Congressional Record 1936; House hearings on H.R. 6150 (1937); Levy County Journal 1933."),
    ("camp", "work", "4 · Camp Roosevelt",
     "In September 1935 the President set off the first blast from afar, and within months several thousand men, most of them from the relief rolls, were digging south of Ocala. The camps filled before their sanitation was ready; a Black worker, John Matthews, died when a truck of canal workers overturned in 1936.",
     "Florida State Board of Health, report for 1935; Federal Writers' Project, Marion County (1936); Senate Document 275 (1936); Citrus County Chronicle, Madison Enterprise-Recorder, Sanford Herald 1935–36."),
    ("aquifer", "water", "5 · The water under Florida",
     "The Geological Survey saw “no reasonable doubt” of serious harm to the underground water of the Ocala limestone; Sanford and Winter Park telegraphed their fear. The Senate refused further money in 1936 (34 to 39) and the bill to finish the canal in 1939 (36 to 45). At Silver Springs the canal was buried in a mock funeral.",
     "Congressional Record, 17 March 1936 and 17 May 1939; House Document 194, 75th Congress (1937); House hearings 1937; Bradford County Telegraph, 7 August 1936."),
    ("war", "capitol", "6 · A canal for the war",
     "With submarines sinking ships off the Atlantic coast, Congress was asked again in 1942. A first vote failed; a Miami paper had called it a “boondoggling bill”. On 23 July 1942 a high-level lock barge canal was authorized, at ninety-three million dollars, and then not built.",
     "Congressional Record, 1 June 1942; Act of 23 July 1942 (56 Stat. 703); House Report 2, 79th Congress (1945)."),
    ("rodman", "river", "7 · Rodman",
     "In February 1964 President Johnson broke ground at Palatka. The dam at Rodman flooded thousands of acres of the Ocklawaha valley. Opponents carried the case to the courts and to Washington, and on 19 January 1971 President Nixon ordered the work halted.",
     "Public Papers of the Presidents 1964 and 1971; Florida Board of Conservation reports; congressional reports and hearings; federal court decisions 1971–1974."),
    ("undoing", "land", "8 · Undoing the canal",
     "The counties had paid a canal tax from 1936 to 1971. A President called the project “ill-advised” in 1977; in 1984 the House kept it alive by 204 to 201; landowners sued for the return of their land. The act of 1990 ended it and set aside a corridor of at least 300 yards.",
     "The President's Environmental Program 1977; House hearing at Palatka, 10 June 1985; Laws of Florida 1979; Public Law 101-640 (1990)."),
]

MISSING = [
    ("segregation", "work", "Segregation at the camps",
     "The sources found so far count canal workers as “White” and “Colored” in a health report, but do not say how camps and crews were divided. That needs the records of the WPA and the Corps of Engineers (National Archives, Record Groups 69 and 77) and the Ocala newspapers of 1935–36, which are not yet reachable here."),
    ("wages", "work", "Wages",
     "No hourly rates of 1935–36 found yet; only payroll totals in the press and the statement that ninety per cent of the men came from the relief rolls."),
    ("families", "land", "The families on the route",
     "The sources give acreages (of the right of way in 1936, of the Rodman pool, of lawsuits) but not the number or names of the families who lost homes. County land and court records would be needed."),
    ("archaeology", "river", "Sites under the Rodman pool",
     "The state's list of salvage excavations for 1964–66 names no site on the canal route. That is a silence of the source, not proof that nothing was there or that nothing was lost."),
    ("hdoc109", "capitol", "The engineers' report of 1942",
     "The Chief of Engineers' review of 12 June 1942 was withheld as a defence matter and printed in 1945 as House Document 109, 79th Congress. Not yet found in a reachable scan."),
    ("sdoc147", "water", "The groundwater board of 1935",
     "The report of the board of experts on groundwater (December 1935, Senate Document 147, 74th Congress) is cited in the debates but not yet found."),
    ("fde1970", "river", "The opponents' report of 1970",
     "The Florida Defenders of the Environment's report on the canal's environmental impact (1970) is not digitized here and its rights are unclear. It is named, not printed; the opponents speak in this apparatus through their testimony in federal hearings."),
    ("photos1964", "survey", "Photographs of 1964–71",
     "No public-domain photographs of the barge canal works, the locks or the Rodman dam have been found yet in reachable federal collections."),
    ("timmerman", "work", "A death reported in 1936",
     "A news agency report of March 1936, found only in Spanish translation, tells of an unemployed mason found nailed to a cross near the canal camp, linked by the police to labour troubles on the canal. What happened, who did it and how it ended is not documented in the sources found, and it is not told here beyond that."),
]

STATIONS = [
    ("19 January 1826", "survey", "A Senate committee for a canal",
     "Reporting on a bill to survey a canal route between the Atlantic and the Gulf, a Senate committee thinks the work “not only practicable, but much more easily accomplished than former estimates and opinions have supposed.”",
     "Senate Document 21, 19th Congress, 1st Session, p. 1."),
    ("19 February 1829", "survey", "“Not practicable”",
     "General Simon Bernard and Captain William Tell Poussin report that the ridge of the peninsula has a mean elevation of one hundred and fifty feet above the ocean; a ship channel through it “is not practicable.” They propose a boat canal instead.",
     "Report of the Board of Internal Improvement, reprinted in House Document 8, 23rd Congress, pp. 65–66."),
    ("1875", "river", "“The sweetest water-lane in the world”",
     "Sidney Lanier describes the Ocklawaha from the deck of a steamboat.",
     "Sidney Lanier, Florida: Its Scenery, Climate, and History (1875/76), p. 20."),
    ("22 April 1880", "survey", "Fifty million dollars",
     "A report by Lieutenant Colonel Quincy A. Gillmore puts a ship canal from the St. Marys River to the Gulf at about $50,000,000, against some 2,600,000 tons a year passing through the Florida Straits.",
     "Senate Executive Document 154, 46th Congress, p. 14."),
    ("27 May 1933", "land", "A memorial for work",
     "The Florida legislature asks Congress for the canal, which would “give employment to a vast amount of human labor”.",
     "Joint Memorial No. 11 (1933), in Documentary History of the Florida Canal (Senate Document 275, 74th Congress, 1936), p. 82."),
    ("19 September 1935", "work", "The first blast",
     "The President sets off the first blast on the canal near Ocala “at 1 o'clock on the afternoon of September 19, 1935”. Construction under the Chief of Engineers had begun on 3 September.",
     "Documentary History of the Florida Canal (1936), pp. 156–157; Congressional Record, 17 March 1936, p. 3839."),
    ("17 March 1936", "capitol", "34 to 39",
     "The Senate rejects Senator Fletcher's amendment for further canal money, after Senator Vandenberg sets out the objections of the Public Works Administration and the Interior Department and the Geological Survey's warning on the groundwater.",
     "Congressional Record, Senate, 17 March 1936, pp. 3842, 3846."),
    ("1 June 1936", "work", "Ten miles, six thousand men",
     "The canal authority counts about ten miles of the central cut, 17,000,000 cubic yards moved, about $5,000,000 spent and about 6,000 men employed.",
     "Documentary History of the Florida Canal (1936), p. vi."),
    ("7 August 1936", "water", "A funeral at Silver Springs",
     "With the money gone, the canal is buried in a mock funeral at Silver Springs: “sired by Washington and damned by South Florida”.",
     "Bradford County Telegraph, 7 August 1936."),
    ("17 May 1939", "capitol", "36 to 45",
     "The Senate defeats the bill to complete the ship canal, after first voting to name it for the late Senator Duncan Fletcher.",
     "Congressional Record, Senate, 17 May 1939, p. 5649."),
    ("23 July 1942", "capitol", "A barge canal for the war",
     "Congress authorizes “a high-level lock barge canal from the Saint Johns River across Florida to the Gulf of Mexico” and $93,000,000.",
     "Act of 23 July 1942, 56 Stat. 703."),
    ("27 February 1964", "capitol", "Ground broken at Palatka",
     "President Johnson: “This new ribbon of water will enable barges to move across the Florida peninsula a few years from now”.",
     "Public Papers of the Presidents, Lyndon B. Johnson, 1963–64, Book I, no. 198, p. 315."),
    ("19 January 1971", "river", "The halt",
     "President Nixon orders “a halt to further construction of the Cross Florida Barge Canal to prevent potentially serious environmental damages.” About $50 million of an estimated $180 million has been committed.",
     "Public Papers of the Presidents, Richard Nixon, 1971, no. 20, pp. 43–44."),
    ("23 May 1977", "capitol", "“Ill-advised”",
     "President Carter asks Congress to deauthorize the canal and “put an end to the long controversy over this ill-advised project.”",
     "The President's Environmental Program, 1977, p. M-10."),
    ("28 June 1984", "capitol", "204 to 201",
     "The House of Representatives votes, 204 to 201, not to deauthorize the canal, as a witness recalls at the hearing in Palatka a year later.",
     "House hearing, Cross-Florida Barge Canal, Palatka, 10 June 1985, p. 147."),
    ("28 November 1990", "land", "The end, and a greenway",
     "Congress provides that the canal be deauthorized once Florida's Governor and Cabinet so resolve, and that a greenway corridor “not be less than 300 yards wide”.",
     "Public Law 101-640, § 402, 104 Stat. 4644–4645."),
]


def dump(name, obj):
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    import sys
    cur = json.loads((DATA / "modules.json").read_text(encoding="utf-8")) if (DATA / "modules.json").exists() else {}
    if cur.get("shipped") and "--force" not in sys.argv:
        sys.exit("modules are already shipped; the frame would overwrite them (use --force only to start over)")
    dump("modules.json", {
        "shipped": [],
        "planned": [dict(id=i, side=s, kurz=k, warum=w, quelle=q) for i, s, k, w, q in PLANNED],
        "missing": [dict(id=i, side=s, kurz=k, warum=w, quelle="—") for i, s, k, w in MISSING]})
    dump("timeline.json", {
        "lede": "Stations read against the page images of their sources only; each names its source. Links into the modules follow as the modules are printed.",
        "stations": [dict(d=d, side=s, titel=t, text=x, quelle=q) for d, s, t, x, q in STATIONS]})
    dump("compare.json", {"lede": "Where the sources speak about the same thing, their voices stand side by side.", "pairs": []})
    dump("plates.json", {"lede": "Public-domain maps, photographs and views, each with its source. Plates follow with the modules.", "credit": "", "plates": []})
    print("frame written")
