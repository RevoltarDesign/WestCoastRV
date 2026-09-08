#!/usr/bin/env python3
"""Apply sourced fact, location, and route corrections for eight eastern Washington state parks."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "eastern-state-parks-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-07"

SLUGS = (
    "curlew-lake-state-park", "steamboat-rock-state-park", "sun-lakes-dry-falls-state-park",
    "lake-chelan-state-park", "twenty-five-mile-creek-state-park", "riverside-state-park",
    "yakima-sportsman-state-park", "bridgeport-state-park",
)
STATE_URL = {slug: f"https://parks.wa.gov/find-parks/state-parks/{slug}" for slug in SLUGS}

CONTENT = {
    "curlew-lake-state-park": {
        "Hiking":"true", "Fishing":"true", "Swimming":"true", "Kayaking/Paddling":"true", "Beach & Tide Pools":"false", "Boating":"true", "Playground":"false",
        "Short Description":"Northeastern Washington lake park with 53 vehicle-access campsites, including full and partial hookups, plus showers, a trailer dump, and a 45-foot limit.",
        "Long description":"Curlew Lake State Park is a seasonal campground near Republic. The official map shows 53 vehicle-access campsites: sites 1–27 and 57–82. Walk-in sites 28–56 are separate. Vehicle sites include standard, partial-hookup, and full-hookup options, with six pull-through sites. Washington State Parks lists showers, drinking water, a trailer dump, and a 45-foot maximum site length.",
        "Number of RV campsites":"53", "Max RV length":"45", "Hookups":"3", "RV Access":"yes", "Dump station on site":"true",
        "Reservation window":"Most campsites are reservable during the operating season, with some first-come availability. Most loops close in late October and reopen in April or May as weather allows",
        "Access note":"Most of the campground closes for winter. The winter schedule separately lists sites 17–19 as first-come December 1–March 15 without utility service; verify weather-dependent access before travel.",
        "Things to do for families summary":"Seasonal lake camping with fishing, paddling, swimming, short trails, and both partial and full hookups.",
        "Nearby nature & parks":"Curlew Lake State Park sits beside Curlew Lake in the forested hills of Ferry County. The park offers lake access, two miles of hiking and biking trails, and a nearby roadside heritage site; seasonal access changes with winter weather.",
        "Site Recommendations":"The 53-site vehicle total excludes walk-in sites 28–56. Utility type varies by site, and sites 73–80 have seasonal mooring-dock access; confirm the exact pad and opening date.",
    },
    "steamboat-rock-state-park": {
        "Hiking":"true", "Fishing":"true", "Swimming":"true", "Kayaking/Paddling":"true", "Beach & Tide Pools":"true", "Boating":"true", "Playground":"true",
        "Short Description":"Large Banks Lake park with 280 developed and primitive vehicle campsites, including 166 full-hookup and 18 partial-hookup sites, plus showers and a trailer dump.",
        "Long description":"Steamboat Rock State Park is a large year-round recreation park at the north end of Banks Lake. The official brochure lists 26 standard, 166 full-hookup, 18 partial-hookup, and 70 primitive campsites at Jones Bay and Osborn Bay, for 280 vehicle campsites, plus five separate equestrian sites. Washington State Parks lists showers, a trailer dump, and limited availability for equipment up to 50 feet. Primitive areas have fewer services and require separate suitability checks.",
        "Number of RV campsites":"280", "Max RV length":"50", "Hookups":"3", "RV Access":"yes", "Dump station on site":"true",
        "Reservation window":"Developed camping is reservable April 1–October 31. Sage, Dune, and Cove loops close November 1–March 31; Bay Loop remains first-come during that period",
        "Access note":"The 280-site total includes 210 developed standard or utility sites and 70 primitive sites at Jones Bay and Osborn Bay. Confirm road and pad suitability for primitive camping.",
        "Things to do for families summary":"Banks Lake camping with boating, swimming, hiking, paddling, a play area, and utility options ranging from dry camping to full hookups.",
        "Things to do for families":"Steamboat Rock and Northrup Canyon trails\nBanks Lake swimming and beach recreation\nBoating and paddling\nFishing under current regulations\nPlay area and sports courts\nGrand Coulee Dam area day trips",
        "Nearby nature & parks":"The park surrounds the basalt Steamboat Rock formation at the north end of Banks Lake. Trails reach the rock plateau and Northrup Canyon, while Grand Coulee Dam is a separate nearby destination with its own seasonal programs.",
        "Site Recommendations":"Choose among developed full-hookup, partial-hookup, standard, and primitive areas. Sage, Dune, Cove, and Bay have different winter schedules; Jones Bay and Osborn Bay are primitive and less suitable for some rigs.",
    },
    "sun-lakes-dry-falls-state-park": {
        "Hiking":"true", "Fishing":"true", "Swimming":"true", "Kayaking/Paddling":"true", "Beach & Tide Pools":"true", "Boating":"true", "Playground":"true",
        "Short Description":"High-desert lakes park with 96 standard and 41 full-hookup campsites, showers, a trailer dump, a 65-foot limit, and access to Dry Falls geology.",
        "Long description":"Sun Lakes–Dry Falls State Park has 96 standard campsites and 41 full-hookup sites, for 137 vehicle campsites. Washington State Parks lists showers, drinking water, a trailer dump, and limited availability for equipment up to 65 feet. Strong winds are common. Dry Falls Visitor Center is undergoing renovation through 2026; the park remains open, while the visitor-center restroom, parking lot, and outdoor overlook may close when construction begins.",
        "Number of RV campsites":"137", "Max RV length":"65", "Hookups":"3", "RV Access":"yes", "Dump station on site":"true",
        "Reservation window":"Reservable during the main season; camping is first-come September 16–April 14. Sites 1–31 may close October 31–March 16 depending on weather",
        "Access note":"Water may be shut off after October 1 at sites 1–31 and more broadly in mid-October. Deep Lake and Dry Falls access gates have weather-dependent winter closures.",
        "Things to do for families summary":"High-desert camping with lake recreation, trails, golf, and Ice Age Floods geology, subject to current visitor-center construction access.",
        "Things to do for families":"Dry Falls geology and park viewpoints\nLake swimming and boating\nFishing under current regulations\nHiking through the coulee landscape\nKayaking and paddleboarding\nPark golf course and playground",
        "Nearby nature & parks":"Sun Lakes–Dry Falls State Park spans lakes and basalt coulees shaped by Ice Age floods. Dry Falls remains visible from other park locations when visitor-center construction limits access to its primary parking and overlook area.",
        "Site Recommendations":"The 137-site total is 96 standard plus 41 full-hookup campsites. Expect wind and limited shade; verify winter water, gate, and visitor-center access before travel.",
    },
    "lake-chelan-state-park": {
        "Hiking":"true", "Fishing":"true", "Swimming":"true", "Kayaking/Paddling":"true", "Beach & Tide Pools":"true", "Boating":"true", "Playground":"true",
        "Short Description":"South-shore Lake Chelan campground with 144 numbered sites, including partial and full hookups, plus showers, a trailer dump, and a 45-foot utility-site limit.",
        "Long description":"Lake Chelan State Park occupies the forested south shore of Lake Chelan. The official campground map numbers 144 sites. Older official brochure material categorizes 103 standard spaces and 35 utility spaces, including 17 full-hookup and 18 partial-hookup sites; those category totals do not fully reconcile with the current 144-site map, so the listing preserves that distinction. Washington State Parks lists showers, a trailer dump, and utility sites accommodating equipment up to 45 feet.",
        "Number of RV campsites":"144", "Max RV length":"45", "Hookups":"3", "RV Access":"yes", "Dump station on site":"true",
        "Reservation window":"Beach Loop is reservable April 15–September 30, West Loop April 15–September 14, Trailer Loop sites 8–17 year-round, and Trailer Loop sites 1–7 and 18–35 April 15–September 30",
        "Access note":"Google reported a restricted-use or private-road warning near the destination when reviewed. Follow current signs on South Lakeshore Road and do not use an unmarked shortcut.",
        "Things to do for families":"Lake swimming and beach access\nBoating and paddling\nFishing under current regulations\nLittle Bear Trail\nPlayground and volleyball\nChelan-area day trips",
        "Things to do for families summary":"Lake Chelan camping with standard, partial-hookup, and full-hookup sites, a swimming beach, boating, trails, and family recreation.",
        "Nearby nature & parks":"Lake Chelan State Park provides direct access to the south shore of Lake Chelan. Chelan and other lake destinations are separate drives; marina, launch, and winter water availability should be checked before travel.",
        "Site Recommendations":"Use the 144-site map for site numbers and confirm the selected site's utility type. Only selected utility sites support equipment up to 45 feet, and loop reservation seasons differ.",
    },
    "twenty-five-mile-creek-state-park": {
        "Hiking":"true", "Fishing":"true", "Swimming":"true", "Kayaking/Paddling":"true", "Beach & Tide Pools":"true", "Boating":"true", "Playground":"false",
        "Short Description":"Seasonal upper Lake Chelan campground with 36 numbered sites, including seven full-hookup and four partial-hookup sites, plus showers and a 30-foot utility limit.",
        "Long description":"Twenty-Five Mile Creek State Park is a seasonal campground and marina on Lake Chelan. The current official map numbers 36 campsites: seven full-hookup sites, four partial-hookup sites, and 25 standard sites. Utility sites have a published 30-foot maximum. Washington State Parks lists showers, seasonal groceries and boat fuel, and a trailer dump on the current map. The boat launch has a later, lake-level-dependent spring opening than the campground.",
        "Number of RV campsites":"36", "Max RV length":"30", "Hookups":"3", "RV Access":"yes", "Dump station on site":"true",
        "Reservation window":"Reservable during the main season; first-come September 16–October 31 and April 1–30. Campground closes November 1–April 1, with opening dates weather dependent",
        "Access note":"The watercraft launch is scheduled to reopen June 1 only when Lake Chelan is above 1,092 feet. South Lakeshore Road is winding; allow additional time and confirm lake level and park status.",
        "Things to do for families summary":"Seasonal Lake Chelan camping with a marina, paddling, fishing, swimming, nearby trails, and limited full and partial hookups.",
        "Things to do for families":"Lake Chelan swimming\nBoating and paddling\nFishing under current regulations\nSeasonal marina services\nCreekside exploration\nNearby trail access when conditions allow",
        "Nearby nature & parks":"The park lies at the road-accessible upper end of Lake Chelan's south shore. Nearby mountain trails and lake access are affected by wildfire, weather, road conditions, and seasonal water levels.",
        "Site Recommendations":"The 36-site total includes seven full-hookup, four partial-hookup, and 25 standard sites. Utility sites are limited to 30 feet; verify the selected pad and launch status.",
    },
    "riverside-state-park": {
        "Hiking":"true", "Fishing":"true", "Swimming":"false", "Kayaking/Paddling":"true", "Beach & Tide Pools":"false", "Boating":"false", "Playground":"false",
        "Short Description":"Riverside's main Bowl and Pitcher campground has 31 vehicle sites—16 standard, 13 partial-hookup, and two full-hookup—with showers and a 45-foot limit.",
        "Long description":"This listing covers Bowl and Pitcher, Riverside State Park's main campground on the Spokane River. The current official brochure lists 16 standard, 13 partial-hookup, and two full-hookup campsites, for 31 vehicle sites. Washington State Parks lists two restrooms with showers, a trailer dump, and a 45-foot maximum site length. Riverside also has separate camping at Lake Spokane and the Equestrian Area; those facilities have different locations and seasons.",
        "Number of RV campsites":"31", "Max RV length":"45", "Hookups":"3", "RV Access":"yes", "Dump station on site":"true",
        "Reservation window":"Bowl and Pitcher sites 15–33 are reservable year-round; sites 1–14 open April 1–October 15. Water and the dump station close October 15–mid-April",
        "Access note":"Directions end at Bowl and Pitcher campground, not the Riverside park office, Nine Mile Recreation Area, Lake Spokane campground, or the equestrian campground.",
        "Things to do for families":"Bowl and Pitcher suspension bridge\nSpokane River trails\nHiking and mountain biking\nPicnicking\nPaddling in designated river sections\nSpokane-area day trips",
        "Things to do for families summary":"Spokane River camping with standard and utility sites, a suspension bridge, and direct access to Riverside's trail network.",
        "Nearby nature & parks":"Bowl and Pitcher sits among ponderosa pines and basalt formations on the Spokane River. Other Riverside State Park areas are separate destinations; Little Spokane River Natural Area prohibits pets, bicycles, swimming, and motorized boats.",
        "Site Recommendations":"Choose from 16 standard, 13 partial-hookup, and two full-hookup sites. Sites 15–33 carry winter availability, but campground water and the dump station close seasonally.",
    },
    "yakima-sportsman-state-park": {
        "Hiking":"true", "Fishing":"true", "Swimming":"false", "Kayaking/Paddling":"false", "Beach & Tide Pools":"false", "Boating":"false", "Playground":"true",
        "Short Description":"Seasonal Yakima campground with 37 standard and 37 full-hookup sites, showers, a trailer dump, and selected sites for RVs up to 60 feet.",
        "Long description":"Yakima Sportsman State Park is a 266-acre campground and wetland park near central Yakima. The official brochure lists 37 standard and 37 full-hookup campsites, for 74 vehicle sites, with selected sites accommodating RVs up to 60 feet. Washington State Parks lists showers, drinking water, a trailer dump, a playground, and more than 130 bird species. A long-term ecosystem-restoration project along Levy Trail is scheduled through late 2027 and can create equipment noise near campsites 17–36.",
        "Number of RV campsites":"74", "Max RV length":"60", "Hookups":"3", "RV Access":"yes", "Dump station on site":"true",
        "Reservation window":"Reservable during the operating season; the park is scheduled to close October 1, 2026 and reopen April 16, 2027",
        "Access note":"Use the current University Parkway entrance. Expect construction traffic and noise near Levy Trail and campsites 17–36 during the ecosystem-restoration project scheduled through late 2027.",
        "Things to do for families":"Wetland bird watching\nJuan A. Alvarez Living Classroom trail and pier\nPlayground and lawn games\nSeasonal fishing under current regulations\nPicnic shelters\nYakima-area day trips",
        "Things to do for families summary":"Full-hookup camping near Yakima with wetland birding, accessible trails, a playground, and seasonal fishing.",
        "Nearby nature & parks":"The park protects irrigated lawns, ponds, wetlands, and Yakima River habitat within the city. The Levy Trail restoration project affects part of this landscape through late 2027.",
        "Site Recommendations":"The 74-site total includes 37 standard and 37 full-hookup sites. Full-hookup sites 1–16 are pull-throughs and sites 17–36 are back-ins; construction noise currently affects the latter area.",
    },
    "bridgeport-state-park": {
        "Hiking":"true", "Fishing":"true", "Swimming":"true", "Kayaking/Paddling":"true", "Beach & Tide Pools":"true", "Boating":"true", "Playground":"true",
        "Short Description":"Year-round Rufus Woods Lake park with 14 standard and 20 partial-hookup sites, showers, a trailer dump, and a 45-foot limit.",
        "Long description":"Bridgeport State Park sits on Rufus Woods Lake behind Chief Joseph Dam. The official brochure lists 14 standard campsites and 20 partial-hookup sites, for 34 vehicle campsites, all accommodating equipment up to 45 feet. Washington State Parks lists showers, drinking water, a trailer dump, a swimming area, a playground, and a paved connection toward the dam. Golf is not listed as a current park amenity and has been removed from this listing.",
        "Number of RV campsites":"34", "Max RV length":"45", "Hookups":"2", "RV Access":"yes", "Dump station on site":"true",
        "Reservation window":"Reservable May 15–September 15; first-come September 16–April 30. Dry camping may move to the watercraft-launch area when snow removal is unavailable",
        "Access note":"Winter water may be turned off; the winter supply is near the trailer dump. Follow Half Sun Way to the official park entrance.",
        "Things to do for families":"Rufus Woods Lake swimming\nBoating and paddling\nFishing under current regulations\nPaved bike ride toward Chief Joseph Dam\nPlayground\nSummer interpretive programs when offered",
        "Things to do for families summary":"Year-round lake camping with partial hookups, swimming, paddling, a playground, and nearby Chief Joseph Dam interpretation.",
        "Nearby nature & parks":"Bridgeport State Park occupies shaded shoreline on Rufus Woods Lake immediately behind Chief Joseph Dam. Dam programs and facilities are managed separately and should be checked for current hours.",
        "Site Recommendations":"The campground has 34 vehicle sites: 14 standard and 20 partial-hookup. Winter operation is first-come and may shift to dry camping near the launch when snow removal is limited.",
    },
}

MAX_VALUES = {slug: int(data["Max RV length"]) for slug, data in CONTENT.items()}

def duration(minutes):
    hours, mins = divmod(minutes, 60)
    return f"~{hours} hr {mins} min from Seattle" if hours and mins else f"~{hours} hr from Seattle" if hours else f"~{mins} min from Seattle"

def band(minutes):
    return "4+ hrs" if minutes >= 240 else "3-4hrs" if minutes >= 180 else "2-3hrs" if minutes >= 120 else "1-2hrs" if minutes >= 60 else "under-1hr"

def route_url(lat, lon):
    return f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat},{lon}&travelmode=driving"

def main():
    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))["reviews"]
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source); fields, rows = list(reader.fieldnames or []), list(reader)
    by_slug = {row["Slug"]: row for row in rows}
    for item in reviews:
        slug = item["slug"]; row = by_slug[slug]; lat, lon = item["latitude"], item["longitude"]; display = item["display_minutes"]
        row.update(CONTENT[slug])
        row.update({
            "Data last updated":CHECKED, "Address":item["address"], "Latitude":str(lat), "Longitude":str(lon),
            "Google Maps Link":f"https://www.google.com/maps?q={lat},{lon}", "Coordinates source":item["coordinate_source"],
            "Coordinates checked":CHECKED, "Coordinate precision":item["precision"], "Time from Seattle":duration(display),
            "Drive Time Minutes":str(display), "Drive Time Band":band(display), "Drive distance miles":str(item["distance_miles"]),
            "Drive route minutes":str(item["observed_route_minutes"]), "Drive time origin":"Seattle, Washington",
            "Drive time source":route_url(lat, lon), "Drive time checked":CHECKED, "Drive time note":item["route_note"],
            "Access source":STATE_URL[slug], "Access checked":CHECKED,
        })
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    slugs = set(CONTENT); critical = {"operating_status", "rv_access", "reservation_method", "max_rv_length", "hookups"}
    evidence["observations"] = [o for o in evidence["observations"] if not (o.get("slug") in slugs and o.get("field") in critical)]
    summaries = {
        "operating_status":"The current operator page and winter schedule identify dated seasonal, construction, utility, or weather-dependent restrictions preserved in the canonical record.",
        "rv_access":"The current operator page or official campground map identifies vehicle, RV, utility, or full-hookup campsites.",
        "reservation_method":"The current operator reservation information and winter schedule identify reservable periods, first-come periods, and seasonal exceptions.",
        "max_rv_length":"The operator publishes the maximum or limited-availability equipment length preserved in the record.",
        "hookups":"The current operator page or official campground map identifies the highest published utility level and the text preserves site-type distinctions.",
    }
    for slug in sorted(slugs):
        row = by_slug[slug]
        values = {"operating_status":"current dated closures and alerts preserved", "rv_access":True,
                  "reservation_method":row["Reservation window"], "max_rv_length":MAX_VALUES[slug], "hookups":int(row["Hookups"])}
        source = {"url":STATE_URL[slug], "publisher":"Washington State Parks", "source_family":"washington-state-parks"}
        for field, value in values.items():
            evidence["observations"].append({"slug":slug, "field":field, "status":"corrected_locally", "checked_on":CHECKED,
                "summary":summaries[field], "proposed_value":value,
                "sources":[{**source, "evidence":summaries[field]}]})
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("Applied eight eastern Washington State Parks reviews and 48 grouped campground fact corrections.")

if __name__ == "__main__":
    main()
