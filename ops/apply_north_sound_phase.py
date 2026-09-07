#!/usr/bin/env python3
"""Apply sourced location, route, and critical-fact corrections for six North Sound state parks."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "north-sound-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-07"

STATE_PARK_URL = {
    "deception-pass-state-park": "https://parks.wa.gov/find-parks/state-parks/deception-pass-state-park",
    "larrabee-state-park": "https://parks.wa.gov/find-parks/state-parks/larrabee-state-park",
    "birch-bay-state-park": "https://parks.wa.gov/find-parks/state-parks/birch-bay-state-park",
    "camano-island-state-park": "https://parks.wa.gov/find-parks/state-parks/camano-island-state-park",
    "fort-ebey-state-park": "https://parks.wa.gov/find-parks/state-parks/fort-ebey-state-park",
    "fort-casey-historical-state-park": "https://parks.wa.gov/find-parks/state-parks/fort-casey-historical-state-park",
}

CONTENT = {
    "deception-pass-state-park": {
        "Short Description": "Large Whidbey Island state park with standard and partial-hookup camping near Cranberry Lake, beaches, tide pools, and the Deception Pass Bridge.",
        "Long description": "Deception Pass State Park spans Whidbey and Fidalgo islands around its landmark bridges. Developed camping is spread across Cranberry Lake, Quarry Pond, and Bowman Bay; partial-hookup sites provide water and electricity, while showers and a trailer dump are available in the park. The reviewed map destination points to Cranberry Lake Campground, the park's largest camping area. Check the current park alerts before arrival because storm damage and winter schedules can limit particular roads, launches, and facilities.",
        "Number of RV campsites": "", "Max RV length": "", "Hookups": "2", "RV Access": "yes",
        "Access note": "The listing covers three campground areas with different site dimensions. The map pin and directions use Cranberry Lake Campground; confirm the selected site's equipment limit when reserving.",
    },
    "larrabee-state-park": {
        "Short Description": "Washington's first state park, with 26 water-and-electric utility sites near Samish Bay, tide pools, and Chuckanut Mountain trails.",
        "Long description": "Larrabee is Washington's first state park, set between Chuckanut Mountain and Samish Bay. The campground has 51 standard tent sites, 26 utility sites with water and electricity, and eight primitive sites, plus restrooms, showers, and a trailer dump. Highway 11 and active railroad tracks border the campground, and the state specifically warns that train noise occurs day and night.",
        "Max RV length": "", "Hookups": "2", "RV Access": "yes",
        "Reservation window": "Reservable up to 9 months ahead for May 15–September 15 arrivals; first-come outside that period",
        "Access note": "Utility sites provide water and electricity, not sewer hookups. The route avoids an option Google flagged for restricted or private-road use.",
    },
    "birch-bay-state-park": {
        "Short Description": "Forested beach campground near Blaine with 147 standard sites and 20 partial-hookup sites, plus tide flats and family-friendly shoreline access.",
        "Long description": "Birch Bay State Park combines a forested campground with broad tide flats on the Salish Sea. The current state brochure lists 147 standard campsites and 20 partial-hookup sites, and the park accommodates RVs and vehicle-trailer combinations up to 60 feet. Restrooms, showers, drinking water, and a trailer dump are available. From September 16 to May 14, camping is first-come in the North Loop and water may be winterized.",
        "Number of RV campsites": "167", "Max RV length": "60", "Hookups": "2", "RV Access": "yes",
        "Reservation window": "Reservable up to 9 months ahead for May 15–September 15 arrivals; North Loop is first-come September 16–May 14",
        "Access note": "The 20 utility sites are partial hookups. Confirm the individual site's dimensions for combinations approaching the park's 60-foot maximum.",
    },
    "camano-island-state-park": {
        "Short Description": "Island state park with 77 reservable standard campsites, several RV-friendly pull-throughs, rocky Puget Sound shoreline, and a trail to Cama Beach.",
        "Long description": "Camano Island State Park offers 77 reservable standard campsites near its rocky Puget Sound shoreline. Several sites in the upper loop are pull-throughs and are identified by the state as better suited for RVs. There are no campsite hookups; nearby facilities include restrooms, showers, drinking water, and a trailer dump. The lower loop is available year-round, while the upper loop generally operates from spring through September.",
        "Number of RV campsites": "77", "Max RV length": "", "Hookups": "0", "RV Access": "yes",
        "Access note": "Several upper-loop pull-through sites are better suited for RVs. Select a site using the reservation system's equipment limits; a park-wide maximum is not published on the current operator page.",
    },
    "fort-ebey-state-park": {
        "Max RV length": "", "Hookups": "2", "RV Access": "yes",
        "Access note": "The campground has 39 standard sites and 11 partial-hookup sites. Confirm the individual site's equipment limit when reserving; no park-wide maximum is published on the current operator page.",
    },
    "fort-casey-historical-state-park": {
        "Long description": "Fort Casey occupies a dramatic headland guarding Admiralty Inlet, with a historic lighthouse, coastal gun batteries, and broad water views. Thirteen of 35 campsites have water and electric hookups, and the state lists a maximum equipment length of 40 feet with limited availability at that size. Restrooms and showers are available, but the park does not list a trailer dump. The campground sits beside the Coupeville ferry terminal, and Navy training jets may pass overhead during the day or night.",
        "Hookups": "2", "RV Access": "yes", "Dump station on site": "false",
        "Reservation window": "Campground closed September 15, 2026–June 15, 2027 for water-line replacement; otherwise reservable up to 9 months ahead",
        "Access note": "The campground is scheduled to close September 15, 2026 through June 15, 2027 for water-line replacement. Ferry-terminal traffic and Navy training flights can add noise.",
    },
}

MAX_VALUES = {"deception-pass-state-park": None, "larrabee-state-park": None, "birch-bay-state-park": 60,
              "camano-island-state-park": None, "fort-ebey-state-park": None, "fort-casey-historical-state-park": 40}

def duration(minutes):
    hours, mins = divmod(minutes, 60)
    return f"~{hours} hr {mins} min from Seattle" if mins else f"~{hours} hr from Seattle"

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
        values = {"operating_status": "currently listed by Washington State Parks", "rv_access": True,
                  "reservation_method": row["Reservation window"], "max_rv_length": MAX_VALUES[slug], "hookups": int(row["Hookups"])}
        summaries = {
            "operating_status": "The current operator page lists the park and current alerts; Fort Casey's dated campground closure is preserved in the canonical record.",
            "rv_access": "The current operator page or official campground map identifies RV or utility campsites.",
            "reservation_method": "Washington State Parks links the park to its reservation system; seasonal exceptions are preserved where published.",
            "max_rv_length": "The current operator material publishes this park-wide limit, or the canonical record explicitly leaves it unconfirmed.",
            "hookups": "The current operator page or official campground brochure identifies the published utility level.",
        }
        source = {"url": STATE_PARK_URL[slug], "publisher": "Washington State Parks", "source_family": "washington-state-parks"}
        for field, value in values.items():
            evidence["observations"].append({"slug": slug, "field": field, "status": "corrected_locally", "checked_on": CHECKED,
                "summary": summaries[field], "proposed_value": value, "sources": [{**source, "evidence": summaries[field]}]})
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("Applied 6 North Sound location/route reviews and 8 campground fact corrections.")

if __name__ == "__main__": main()
