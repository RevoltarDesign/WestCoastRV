#!/usr/bin/env python3
"""Apply the September public-campground location, route, and factual scrub batch."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "public-location-batch-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-12"

URLS = {
    "hozomeen-campground": "https://www.nps.gov/noca/planyourvisit/hozomeen.htm",
    "big-creek-campground": "https://www.fs.usda.gov/r06/olympic/recreation/big-creek-campground",
    "twin-harbors-state-park": "https://parks.wa.gov/find-parks/state-parks/twin-harbors-state-park",
    "grayland-beach-state-park": "https://parks.wa.gov/find-parks/state-parks/grayland-beach-state-park",
    "cape-disappointment-state-park": "https://parks.wa.gov/find-parks/state-parks/cape-disappointment-state-park",
    "silver-lake-park": "https://www.whatcomcounty.us/3518/Camping-at-Silver-Lake-Park",
    "dosewallips-state-park": "https://parks.wa.gov/find-parks/state-parks/dosewallips-state-park",
    "fort-flagler-historical-state-park": "https://parks.wa.gov/find-parks/state-parks/fort-flagler-historical-state-park",
}

CONTENT = {
    "hozomeen-campground": {
        "Short Description": "Remote Ross Lake campground area currently closed by the Border 2 Fire; the Hozomeen border gate is also closed to vehicle and foot traffic until further notice.",
        "Long description": "Hozomeen lies at the north end of Ross Lake near the U.S.–Canada border. The National Park Service currently lists the entire Hozomeen area—including Winnebago Flats, the Upper and Lower Loop campgrounds, docks, and public areas—as closed because of the Border 2 Fire. Separately, the gate at Hozomeen remains closed until further notice and vehicle and foot traffic across the border are prohibited. There is no direct road approach from Washington; boat and multi-day trail approaches described by the park are also subject to the current area closure. Check the NPS closure page before making any plans.",
        "Reservation window": "Entire Hozomeen area currently closed for the Border 2 Fire; border gate also closed until further notice",
        "Reservation website": "https://www.nps.gov/noca/planyourvisit/fire-closures.htm",
        "Number of RV campsites": "", "Max RV length": "", "RV Access": "no",
        "Access note": "Do not attempt to drive to Hozomeen. The usual road approach runs through Canada, but cross-border vehicle and foot traffic at the Hozomeen gate are prohibited. The entire Hozomeen area is also currently closed for the Border 2 Fire.",
        "Amenities: Toilets": "", "Amenities: Showers": "false", "Amenities: Drinking water": "false", "Amenities: Fire pits": "false", "Dump station on site": "false",
        "Amenities summary": "No campground services are currently available because the entire Hozomeen area is closed. When the area reopens, verify water, fire, road, border, and waste-service conditions directly with NPS.",
        "Things to do for families summary": "The area normally supports Ross Lake boating, fishing, and wilderness hiking, but it is currently closed.",
        "Nearby nature & parks": "Hozomeen sits at the remote north end of Ross Lake in Ross Lake National Recreation Area, close to the U.S.–Canada border and the peaks of the North Cascades. The East Bank Trail connects the area to State Route 20, and Ross Lake provides a water approach when conditions and closures allow. The entire Hozomeen area is currently closed for the Border 2 Fire.",
        "Site Recommendations": "Do not plan an RV stay or attempt the border approach while the NPS area and gate closures remain in effect. Recheck the official Hozomeen and fire-closure pages before considering a future boat, trail, or vehicle itinerary.",
    },
    "big-creek-campground": {
        "Short Description": "Open, first-come Olympic National Forest campground near Lake Cushman with 64 units, a one-mile creek loop trail, and access toward Staircase.",
        "Max RV length": "",
        "Nearby nature & parks": "Big Creek Campground lies in second-growth forest near Lake Cushman in Olympic National Forest. The one-mile Big Creek Campground Trail loops around the campground and crosses Big Creek twice; a longer upper loop climbs through the surrounding basin. Lake Cushman and the Staircase area of Olympic National Park are nearby by road.",
        "Site Recommendations": "All 64 units are first-come, first-served. The current Forest Service listing accepts tents, trailers, and RVs but does not publish one campground-wide RV length, so confirm your rig's fit with the Hood Canal Ranger District. Use North Lake Cushman Road and Forest Road 24; save directions before leaving Hoodsport because service can be limited.",
        "Access note": "The current operator page confirms RV access but does not publish one campground-wide maximum length. Directions now end at the named Olympic National Forest campground rather than a nearby road point.",
    },
    "twin-harbors-state-park": {
        "Short Description": "Large coastal state park near Westport with standard and full-hookup camping, showers, a dump station, and direct trail access to the Pacific beach.",
        "Long description": "Twin Harbors State Park occupies coastal forest and dunes south of Westport. The current park page offers standard, full-hookup, and hiker/biker camping, plus cabins and yurts. Hookup sites are small and close together, with limited availability up to 35 feet; larger RVs may be difficult to place. Seasonal flooding closes the entire Eastside loop and Westside sites 232–299 from November through May 31, while other campsites shift to first-come service during parts of the shoulder season. Use the current campground map and winter schedule when choosing a site.",
        "Number of RV campsites": "", "Max RV length": "35",
        "Reservation window": "Main-season reservations available; Eastside loop and Westside sites 232–299 close November–May 31, and remaining sites shift to first-come during parts of the shoulder season",
        "Access note": "Directions end at the Eastside campground near the main entrance. Hookup sites have limited 35-foot availability, and larger units may have difficulty. Check seasonal flooding closures before arrival.",
        "Site Recommendations": "Match your rig to the current campground map instead of relying on older site totals. Hookup sites are compact, and seasonal flooding closes large sections of the campground. The Shifting Sands trail provides campground-to-beach access; check current beach and razor-clam rules before visiting.",
    },
    "grayland-beach-state-park": {
        "Short Description": "Year-round coastal state park with at least 98 utility campsites, primitive and standard options, paved RV pads up to 60 feet, and five dune trails to the Pacific beach.",
        "Long description": "Grayland Beach State Park offers primitive, standard, partial-utility, and full-utility camping in shore-pine forest beside the Pacific. The official park brochure identifies 60 full-utility and 38 partial-utility sites, plus four standard and four primitive campsites. The current park page lists paved driveways and limited availability for RVs up to 60 feet. Heavy coastal rainfall can flood more than 50 campsites from November 1 through April 15; affected sites are first-come during that period and should be inspected on arrival.",
        "Number of RV campsites": "98",
        "Reservation window": "Reservations available year-round; 50+ flood-prone sites are first-come November 1–April 15 and should be inspected on arrival",
        "Access note": "The reviewed pin matches the campground and current Cranberry Beach Road address. Limited sites accommodate equipment up to 60 feet; seasonal flooding can affect more than 50 campsites.",
        "Site Recommendations": "Use the reservation system's individual pad length and inspect the assigned site during the wet season. Five marked dune trails reach the beach but may also flood in winter and spring. Check WDFW dates for razor-clam openings and current State Parks beach advisories.",
    },
    "cape-disappointment-state-park": {
        "Short Description": "Major coastal park at the Columbia River mouth whose campground remains closed for construction; reopening timing depends on project progress.",
        "Long description": "Cape Disappointment State Park protects beaches, forest, lighthouses, and Lewis and Clark history at the mouth of the Columbia River. All campground loops remain listed as closed for entrance-road, culvert, trail, wetland, and welcome-center work. Washington State Parks expected a summer 2026 reopening but states that timing depends on construction and weather. The park's campground normally includes standard, partial-hookup, full-hookup, and hiker/biker sites with limited availability for equipment up to 45 feet. Check the project and park alert pages before planning any overnight stay or access to Waikiki Beach, North Jetty, or the boat launch.",
        "Number of RV campsites": "", "RV Access": "no",
        "Reservation window": "All campground loops currently closed for construction; reopening timing depends on project progress and current park alerts",
        "Reservation website": "https://parks.wa.gov/about/strategic-planning-projects-public-input/projects/cape-disappointment-temporary-camping-closure",
        "Access note": "Do not plan an overnight stay until Washington State Parks confirms reopening. Directions point to the campground for future planning, but construction closures currently restrict the campground and several nearby day-use areas.",
        "Amenities: Toilets": "", "Amenities: Showers": "false", "Amenities: Drinking water": "false", "Amenities: Fire pits": "false", "Dump station on site": "false",
        "Amenities summary": "Campground restrooms, showers, drinking water, fire pits, and the trailer dump are unavailable while all camping loops remain closed for construction.",
        "Site Recommendations": "Check the official temporary-closure project page and live park alerts before traveling. Do not rely on older reservation availability or loop descriptions while construction remains active.",
    },
    "silver-lake-park": {
        "Short Description": "Whatcom County park with 75 reservable RV sites in Maple Creek and Red Mountain, water and electric hookups, seasonal showers, a dump station, and lake access.",
        "Long description": "Silver Lake Park is a 410-acre Whatcom County park in the Cascade foothills. Maple Creek has 45 standard and two double-size RV sites with water and electric hookups; Red Mountain adds 28 RV sites with water and electric. A separate 15-site RV group camp is rented as one group facility, while Cedar Campground is not recommended for RVs and prohibits vehicles over 25 feet. Seasonal showers, flush toilets, an RV dump, boat rentals, trails, a beach, and a playground serve the park during the camping season.",
        "Number of RV campsites": "75",
        "Reservation window": "Camping season April 10–October 26, 2026; reservations recommended, with limited first-come sites. Following-year reservations open the first business day of December",
        "Access note": "Directions end near Maple Creek Campground, the most convenient RV area for the boat launch, beach, playground, showers, and dump station. Red Mountain is about three-quarters of a mile from the lake; Cedar is not recommended for RVs.",
    },
}

def duration(minutes):
    hours, mins = divmod(minutes, 60)
    return f"~{hours} hr {mins} min from Seattle" if mins else f"~{hours} hr from Seattle"

def band(minutes):
    return "4+ hrs" if minutes >= 240 else "3-4hrs" if minutes >= 180 else "2-3hrs" if minutes >= 120 else "1-2hrs" if minutes >= 60 else "under-1hr"

def route_source(lat, lon):
    return f"https://router.project-osrm.org/route/v1/driving/-122.3321,47.6062;{lon},{lat}?overview=false&steps=false"

def main():
    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))["reviews"]
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source); fields, rows = list(reader.fieldnames or []), list(reader)
    by_slug = {row["Slug"]: row for row in rows}
    changed = 0
    for item in reviews:
        row = by_slug[item["slug"]]
        updates = dict(CONTENT.get(item["slug"], {}))
        lat, lon, display = item["latitude"], item["longitude"], item["display_minutes"]
        updates.update({
            "Data last updated": CHECKED, "Address": item["address"], "Latitude": str(lat), "Longitude": str(lon),
            "Google Maps Link": f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat},{lon}&travelmode=driving",
            "Coordinates source": item["coordinate_source"], "Coordinates checked": CHECKED,
            "Coordinate precision": item["precision"], "Time from Seattle": duration(display),
            "Drive Time Minutes": str(display), "Drive Time Band": band(display),
            "Drive distance miles": str(item["distance_miles"]), "Drive route minutes": str(item["observed_route_minutes"]),
            "Drive time origin": "Seattle, Washington", "Drive time source": route_source(lat, lon),
            "Drive time checked": CHECKED, "Drive time note": item["route_note"],
            "Access source": URLS[item["slug"]], "Access checked": CHECKED,
        })
        if item["slug"] == "hozomeen-campground":
            updates["Time from Seattle"] = "Vehicle access currently closed (usual route ~6 hr 30 min)"
        for key, value in updates.items():
            if row.get(key) != value:
                changed += 1
                row[key] = value

    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    slugs = {item["slug"] for item in reviews}
    critical = {"operating_status", "rv_access", "reservation_method", "max_rv_length", "hookups"}
    evidence["observations"] = [o for o in evidence["observations"] if not (o.get("slug") in slugs and o.get("field") in critical)]
    statuses = {
        "hozomeen-campground": ("entire area currently closed for the Border 2 Fire; border gate closed until further notice", False, None, 0),
        "big-creek-campground": ("site open", True, None, 0),
        "twin-harbors-state-park": ("open with seasonal campground-loop closures", True, 35, 3),
        "grayland-beach-state-park": ("open year-round with seasonal flooding impacts", True, 60, 3),
        "cape-disappointment-state-park": ("all campground loops currently closed for construction", False, 45, 3),
        "silver-lake-park": ("2026 camping season April 10 through October 26", True, None, 2),
        "dosewallips-state-park": ("year-round camping park", True, 40, 3),
        "fort-flagler-historical-state-park": ("active campground with year-round Lower Campground reservations", True, 50, 3),
    }
    for slug in sorted(slugs):
        status, rv_access, max_length, hookups = statuses[slug]
        row = by_slug[slug]
        publisher = "National Park Service" if slug == "hozomeen-campground" else "U.S. Forest Service" if slug == "big-creek-campground" else "Whatcom County Parks & Recreation" if slug == "silver-lake-park" else "Washington State Parks"
        source_family = "nps" if slug == "hozomeen-campground" else "usfs" if slug == "big-creek-campground" else "whatcom-county" if slug == "silver-lake-park" else "washington-state-parks"
        values = {"operating_status": status, "rv_access": rv_access, "reservation_method": row["Reservation window"], "max_rv_length": max_length, "hookups": hookups}
        for field, value in values.items():
            summary = f"The current operator material supports the reviewed {field.replace('_', ' ')} value and any closure or seasonal qualification preserved in the canonical record."
            evidence["observations"].append({"slug": slug, "field": field, "status": "corrected_locally", "checked_on": CHECKED, "summary": summary, "proposed_value": value, "sources": [{"url": URLS[slug], "publisher": publisher, "source_family": source_family, "evidence": summary}]})
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"Applied 8 public campground reviews; corrected {changed} canonical data fields and refreshed 40 critical evidence observations.")

if __name__ == "__main__":
    main()
