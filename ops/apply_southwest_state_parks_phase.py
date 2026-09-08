#!/usr/bin/env python3
"""Apply sourced fact, location, and route corrections for 12 southwest Washington state parks."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "southwest-state-parks-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-07"

SLUGS = (
    "penrose-point-state-park", "illahee-state-park", "saltwater-state-park",
    "dash-point-state-park", "schafer-state-park", "rainbow-falls-state-park",
    "lewis-and-clark-state-park", "seaquest-state-park", "battle-ground-lake-state-park",
    "beacon-rock-state-park", "millersylvania-state-park", "ike-kinswa-state-park",
)
STATE_PARK_URL = {slug: f"https://parks.wa.gov/find-parks/state-parks/{slug}" for slug in SLUGS}
STATE_PARK_URL["lewis-and-clark-state-park"] = "https://parks.wa.gov/find-parks/state-parks/lewis-clark-state-park"

CONTENT = {
    "penrose-point-state-park": {
        "Short Description": "Key Peninsula marine park with 82 standard campsites, a 35-foot equipment limit, forest trails, and Puget Sound shoreline; no hookups.",
        "Long description": "Penrose Point State Park occupies a forested point between Mayo Cove and Carr Inlet on the Key Peninsula. The campground has 82 standard campsites without hookups, plus separate hiker/biker and Cascadia Marine Trail sites. Washington State Parks lists a 35-foot equipment limit, showers, drinking water, and a trailer dump. Showers operate May 15 through October 1. Shellfish harvesting is closed for 2026, and the park's marine pumpout is no longer in service; check current advisories before planning water activities.",
        "Number of RV campsites": "82", "Max RV length": "35", "Hookups": "0", "RV Access": "yes",
        "Reservation window": "Reservable for May 15–September 15 arrivals; unreserved sites are first-come. Check the current winter schedule outside the main season",
        "Access note": "Roads within the campground are narrow and winding. Most vehicle sites provide about 35 feet of parking space; confirm the selected site's equipment limit.",
        "Nearby nature & parks": "Penrose Point lies between Mayo Cove and Carr Inlet on southern Puget Sound. Forest trails reach beaches and tidal shoreline used for paddling, wildlife viewing, and beach exploration. Shellfish harvesting is closed for 2026; consult the park alert and Washington health advisories before harvesting.",
    },
    "illahee-state-park": {
        "Short Description": "Year-round Bremerton marine park with 23 standard campsites and one full-hookup site, showers, a trailer dump, and Port Orchard Bay access.",
        "Long description": "Illahee State Park is a wooded marine park on Port Orchard Bay near Bremerton. Its campground has 23 standard campsites and one full-hookup site, with limited availability for equipment up to 40 feet. Washington State Parks lists showers, drinking water, a trailer dump, a boat launch, and year-round campsite reservations. The Beach Trail is closed until further notice; other park areas remain subject to current alerts.",
        "Number of RV campsites": "24", "Max RV length": "40", "Hookups": "3", "RV Access": "yes",
        "Reservation window": "Campsites reservable year-round; unreserved sites may be available first-come",
        "Access note": "Seattle drive time uses the no-ferry route through Tacoma for a stable towing estimate. The Beach Trail is closed until further notice.",
        "Nearby nature & parks": "Illahee State Park protects wooded shoreline on Port Orchard Bay. Visitors use the beach and pier for fishing, paddling, wildlife viewing, and scuba access; check current park alerts because the Beach Trail is closed until further notice.",
    },
    "saltwater-state-park": {
        "Short Description": "Puget Sound day-use park near Des Moines with beach, trails, and an underwater artificial reef; the campground is currently closed with reopening still to be determined.",
        "Long description": "Saltwater State Park provides beach, trail, picnic, and diving access on Puget Sound between Seattle and Tacoma. Its campground is currently closed because of projects addressing flooding and erosion. Washington State Parks is reevaluating the future camping configuration and has not announced a reopening date. Older campground counts and RV limits are therefore omitted until the operator publishes a current plan. The park remains useful for day visits, including shore access and the underwater artificial reef, subject to posted closures and conditions.",
        "Number of RV campsites": "", "Max RV length": "", "Hookups": "0", "RV Access": "unknown",
        "Reservation window": "Closed while flood and erosion projects and the future camping configuration are under review; reopening TBD",
        "Access note": "Do not plan an overnight stay: Washington State Parks currently lists the campground as closed and has not published a reopening date.",
        "Amenities: Showers": "false", "Dump station on site": "false",
        "Amenities summary": "Day-use facilities may remain available, but campground amenities are unavailable while the campground is closed. Check the current park page before visiting.",
        "Site Recommendations": "Overnight camping is not currently available. Use the official park page for project updates and visit only for currently open day-use activities.",
        "Things to do for families": "Puget Sound beach exploration\nScuba diving at the underwater artificial reef\nPark trails\nSaltwater fishing\nPicnicking with bay views",
        "Nearby nature & parks": "Saltwater State Park preserves a pocket of Puget Sound shoreline and a small creek corridor in an urban area. Day-use visitors can explore the beach, walk park trails, and access the underwater artificial reef when conditions and posted rules allow.",
    },
    "dash-point-state-park": {
        "Short Description": "Year-round Puget Sound campground with 111 standard and 27 utility sites, showers, a trailer dump, forest trails, and a 32-foot equipment limit.",
        "Long description": "Dash Point State Park combines a broad Puget Sound beach with forest trails between Federal Way and Tacoma. The official campground brochure identifies 111 standard campsites and 27 utility sites. Washington State Parks currently lists standard and utility camping, showers, drinking water, a trailer dump, and limited availability for equipment up to 32 feet. Campsites can be reserved year-round. The reviewed map pin points to the campground rather than the park's general day-use location.",
        "Number of RV campsites": "138", "Max RV length": "32", "Hookups": "2", "RV Access": "yes",
        "Reservation window": "Campsites reservable year-round; unreserved sites may be available first-come",
        "Access note": "Internal roads and individual pads vary; confirm the selected site's dimensions. Directions end at the named campground point.",
        "Amenities: Showers": "true", "Dump station on site": "true",
        "Nearby nature & parks": "Dash Point State Park includes Puget Sound beach and a wooded trail system between Federal Way and Tacoma. Low tides expose a broad intertidal area; visitors should consult tide tables and current park notices before beach activities.",
    },
    "schafer-state-park": {
        "Short Description": "Seasonal Satsop River campground with 68 numbered vehicle sites, including 34 partial-hookup sites, plus showers, a trailer dump, and a 40-foot limit.",
        "Long description": "Schafer State Park sits along the East Fork Satsop River west of Elma. The official campground map shows 68 numbered vehicle campsites, with 34 partial-hookup sites, plus separate walk-in and primitive camping. Washington State Parks lists showers, drinking water, a trailer dump, and an equipment limit of 40 feet. Camping is generally reservable during the main May 15 through September 15 season; check the current winter schedule and river conditions before traveling.",
        "Number of RV campsites": "68", "Max RV length": "40", "Hookups": "2", "RV Access": "yes",
        "Reservation window": "Generally reservable for May 15–September 15 arrivals; check the current winter schedule outside the main season",
        "Access note": "The 68-site total counts numbered vehicle sites; four walk-in sites and one primitive site are separate. Confirm the individual pad length when booking.",
        "Nearby nature & parks": "Schafer State Park protects forest and riverbank along the East Fork Satsop River. Fishing, paddling, and swimming conditions change with season and flow; verify current regulations and water conditions before entering the river.",
    },
    "rainbow-falls-state-park": {
        "Short Description": "Chehalis River campground with 40 standard and eight partial-hookup vehicle sites, showers, a trailer dump, and access to the Willapa Hills Trail.",
        "Long description": "Rainbow Falls State Park is a wooded campground on the Chehalis River west of Chehalis. The current park page lists 40 standard campsites and eight partial-hookup sites, plus separate hiker/biker and equestrian sites. Equipment up to 60 feet has limited availability. Showers and drinking water are listed, and the official campground map identifies a trailer dump. The park also connects with the Willapa Hills Trail. A kitchen shelter is closed through December 2026; the campground itself remains subject to the normal reservation and winter schedules.",
        "Number of RV campsites": "48", "Max RV length": "60", "Hookups": "2", "RV Access": "yes",
        "Reservation window": "Generally reservable for May 15–September 15 arrivals; check the current winter schedule outside the main season",
        "Access note": "The 48-site total counts vehicle campsites; hiker/biker and equestrian sites are separate. A kitchen shelter, not the campground, is closed through December 2026.",
        "Nearby nature & parks": "Rainbow Falls State Park includes riverbank forest on the Chehalis River and access to the Willapa Hills Trail. River levels and swimming conditions vary; check current park alerts and fishing regulations before a visit.",
    },
    "lewis-and-clark-state-park": {
        "Short Description": "Seasonal old-growth forest campground near Winlock with 24 standard and eight full-hookup vehicle sites, showers, and trails; main campground closed in winter.",
        "Long description": "Lewis and Clark State Park protects lowland forest along the I-5 corridor near Winlock. The current official brochure identifies 24 standard campsites and eight full-hookup back-in sites, for 32 vehicle campsites, plus separate hiker/biker and equestrian sites. Showers and drinking water are available. The official material does not publish a dependable park-wide RV length or list an RV trailer dump, so those details are omitted. The main campground closes for winter; the posted 2026–27 closure runs October 1 through May 1.",
        "Number of RV campsites": "32", "Max RV length": "", "Hookups": "3", "RV Access": "yes",
        "Reservation window": "Main campground closed October 1, 2026–May 1, 2027; reserve during the operating season and verify current dates",
        "Access note": "The park does not publish one current park-wide RV length. Confirm the selected campsite's dimensions; hiker/biker and equestrian sites are not included in the 32-site vehicle total.",
        "Dump station on site": "false",
        "Nearby nature & parks": "Lewis and Clark State Park protects a mature lowland forest with trails through Douglas fir, western red cedar, and wetland areas. The campground is seasonal, so consult the current winter schedule before traveling.",
    },
    "seaquest-state-park": {
        "Short Description": "Year-round Mount St. Helens base camp with 52 standard, 18 partial-hookup, and 15 full-hookup vehicle sites, showers, and a trailer dump.",
        "Long description": "Seaquest State Park provides a wooded, year-round base near Silver Lake and the Mount St. Helens Visitor Center. A pedestrian tunnel connects the park side of Spirit Lake Highway with the visitor-center area. The campground has 52 standard campsites, 18 partial-hookup sites, and 15 full-hookup sites, for 85 vehicle campsites. Washington State Parks lists showers, drinking water, a trailer dump, and limited availability for equipment up to 50 feet. Campsites can be reserved year-round.",
        "Number of RV campsites": "85", "Max RV length": "50", "Hookups": "3", "RV Access": "yes",
        "Reservation window": "Campsites reservable year-round; unreserved sites may be available first-come",
        "Access note": "The campground offers three utility levels. Confirm the selected site's hookup type and dimensions when booking.",
        "Amenities: Showers": "true", "Dump station on site": "true",
        "Nearby nature & parks": "Seaquest State Park sits beside Silver Lake near the Mount St. Helens Visitor Center. The park is a practical starting point for learning about the 1980 eruption and for exploring currently open destinations along Spirit Lake Highway; check road and monument conditions before longer day trips.",
    },
    "battle-ground-lake-state-park": {
        "Short Description": "Year-round forest and lake campground near Vancouver with 25 standard and six partial-hookup vehicle sites, showers, a trailer dump, and a 35-foot limit.",
        "Long description": "Battle Ground Lake State Park surrounds a small lake north of Vancouver. The official campground brochure identifies 25 standard vehicle campsites and six utility sites, for 31 vehicle campsites, plus separate primitive hike-in sites. Washington State Parks currently lists standard, partial-hookup, and primitive camping, showers, drinking water, a trailer dump, and limited availability for equipment up to 35 feet. Campsites can be reserved year-round.",
        "Number of RV campsites": "31", "Max RV length": "35", "Hookups": "2", "RV Access": "yes",
        "Reservation window": "Campsites reservable year-round; unreserved sites may be available first-come",
        "Access note": "Primitive hike-in sites are not included in the 31-site vehicle total. A temporary closure affected NE Grace Avenue when the route was reviewed; follow current navigation near the park.",
        "Nearby nature & parks": "Battle Ground Lake State Park centers on a small lake surrounded by forest and trails. Visitors use the lake for swimming, paddling, and seasonal fishing; consult current fishing rules, water conditions, and park alerts.",
    },
    "beacon-rock-state-park": {
        "Short Description": "Columbia River Gorge park with 32 vehicle campsites across Upper and Woodard Creek campgrounds; Woodard Creek has five full-hookup sites and a 40-foot limit.",
        "Long description": "Beacon Rock State Park spans several areas on the Washington side of the Columbia River Gorge. The Upper Campground has 25 standard vehicle sites and one separate hiker/biker site. Woodard Creek Campground has two standard sites and five full-hookup sites, bringing the vehicle total to 32. Woodard Creek accommodates equipment up to 40 feet with a 12-foot-9-inch height limit. Showers are listed, but the park does not list an RV trailer dump. The reviewed directions end at Woodard Creek, the RV hookup campground; trailheads and the Upper Campground use different entrances.",
        "Number of RV campsites": "32", "Max RV length": "40", "Hookups": "3", "RV Access": "yes",
        "Reservation window": "Campgrounds are reservable during their operating season; Upper Campground closes in winter. Verify current dates before travel",
        "Access note": "Directions end at Woodard Creek Campground. Its 40-foot equipment limit and 12-foot-9-inch height restriction do not describe every park entrance or campsite.",
        "Dump station on site": "false", "Amenities: Showers": "true",
        "Nearby nature & parks": "Beacon Rock State Park includes Beacon Rock, Hamilton Mountain, Columbia River shoreline, and multiple trailheads in the Columbia River Gorge. Trail, climbing, fire, and seasonal campground closures change independently, so check the current park alerts for the specific area you plan to use.",
    },
    "millersylvania-state-park": {
        "Short Description": "Year-round Deep Lake campground south of Olympia with 93 standard and 45 utility sites, showers, a trailer dump, forest trails, and a 60-foot limit.",
        "Long description": "Millersylvania State Park surrounds Deep Lake in forest south of Olympia. The official campground brochure and current campground map identify 93 standard campsites and 45 utility sites, for 138 vehicle campsites. Washington State Parks lists showers, drinking water, a trailer dump, and an equipment limit of 60 feet. Campsites can be reserved year-round. A trail near campsite 31 is closed indefinitely; use the current park map and alerts when choosing routes through the campground.",
        "Number of RV campsites": "138", "Max RV length": "60", "Hookups": "2", "RV Access": "yes",
        "Reservation window": "Campsites reservable year-round; unreserved sites may be available first-come",
        "Access note": "The 138-site total includes 93 standard and 45 utility campsites. A trail near campsite 31 is closed indefinitely.",
        "Nearby nature & parks": "Millersylvania State Park includes forest trails, wetlands, and Deep Lake. Visitors use the lake for swimming, paddling, and fishing; check current park alerts and seasonal water conditions before a visit.",
    },
    "ike-kinswa-state-park": {
        "Short Description": "Mayfield Lake campground with 101 numbered vehicle sites across full-hookup, partial-hookup, and non-hookup loops, plus showers, a trailer dump, and a 60-foot limit.",
        "Long description": "Ike Kinswa State Park sits on Mayfield Lake near Silver Creek. The current campground map numbers 101 vehicle campsites: Loop A has full-hookup sites, Loop B has water-and-electric sites, and Loop D has non-hookup sites. Nine cabins are separate from that total. Washington State Parks lists showers, drinking water, a year-round trailer dump, and limited availability for equipment up to 60 feet. Loop B remains open year-round; Loop A and Loop D have seasonal closures, and Loop A hookups do not operate in winter.",
        "Number of RV campsites": "101", "Max RV length": "60", "Hookups": "3", "RV Access": "yes",
        "Reservation window": "Loop B reservable year-round; Loop A closed September 30–May 16 and Loop D closed September 30–April 30. Loop A hookups do not operate in winter",
        "Access note": "The campground is on Mayfield Lake. The 101-site total counts numbered vehicle campsites in Loops A, B, and D; nine cabins are separate.",
        "Things to do for families": "Mayfield Lake fishing\nBoating and paddling\nSwimming\nForest walks\nWildlife viewing\nPlayground",
        "Nearby nature & parks": "Ike Kinswa State Park occupies forested shoreline on Mayfield Lake, a reservoir on the Cowlitz River. Boating, swimming, and fishing conditions vary with water level and season; consult current park alerts and fishing regulations before a visit.",
    },
}

MAX_VALUES = {
    "penrose-point-state-park": 35, "illahee-state-park": 40, "saltwater-state-park": None,
    "dash-point-state-park": 32, "schafer-state-park": 40, "rainbow-falls-state-park": 60,
    "lewis-and-clark-state-park": None, "seaquest-state-park": 50,
    "battle-ground-lake-state-park": 35, "beacon-rock-state-park": 40,
    "millersylvania-state-park": 60, "ike-kinswa-state-park": 60,
}

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
            "Data last updated": CHECKED, "Address": item["address"], "Latitude": str(lat), "Longitude": str(lon),
            "Google Maps Link": f"https://www.google.com/maps?q={lat},{lon}", "Coordinates source": item["coordinate_source"],
            "Coordinates checked": CHECKED, "Coordinate precision": item["precision"], "Time from Seattle": duration(display),
            "Drive Time Minutes": str(display), "Drive Time Band": band(display), "Drive distance miles": str(item["distance_miles"]),
            "Drive route minutes": str(item["observed_route_minutes"]), "Drive time origin": "Seattle, Washington",
            "Drive time source": route_url(lat, lon), "Drive time checked": CHECKED, "Drive time note": item["route_note"],
            "Access source": STATE_PARK_URL[slug], "Access checked": CHECKED,
        })
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    slugs = set(CONTENT); critical = {"operating_status", "rv_access", "reservation_method", "max_rv_length", "hookups"}
    evidence["observations"] = [o for o in evidence["observations"] if not (o.get("slug") in slugs and o.get("field") in critical)]
    for slug in sorted(slugs):
        row = by_slug[slug]
        is_closed = slug == "saltwater-state-park"
        values = {
            "operating_status": "campground currently closed; reopening TBD" if is_closed else "currently listed by Washington State Parks with dated closures preserved",
            "rv_access": None if is_closed else True,
            "reservation_method": row["Reservation window"],
            "max_rv_length": MAX_VALUES[slug],
            "hookups": int(row["Hookups"]),
        }
        summaries = {
            "operating_status": "The current operator page lists the active campground status and dated seasonal or project closures; those limits are preserved in the canonical record.",
            "rv_access": "The current operator page or official campground map identifies vehicle, RV, utility, or full-hookup campsites; Saltwater remains unclassified while its closed campground is reevaluated.",
            "reservation_method": "The current operator reservation page, park page, and winter schedule identify reservation availability and seasonal exceptions.",
            "max_rv_length": "The operator publishes this limit, or the record explicitly leaves a park-wide limit unconfirmed when current official material does not support one.",
            "hookups": "The current operator page or official campground map identifies the published utility level; closed Saltwater retains only the supported absence of hookups.",
        }
        source = {"url": STATE_PARK_URL[slug], "publisher": "Washington State Parks", "source_family": "washington-state-parks"}
        for field, value in values.items():
            evidence["observations"].append({
                "slug": slug, "field": field, "status": "corrected_locally", "checked_on": CHECKED,
                "summary": summaries[field], "proposed_value": value,
                "sources": [{**source, "evidence": summaries[field]}],
            })
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("Applied 12 southwest Washington State Parks reviews and 33 grouped campground fact corrections.")

if __name__ == "__main__":
    main()
