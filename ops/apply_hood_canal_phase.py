#!/usr/bin/env python3
"""Apply sourced location, route, and critical-fact corrections for six Hood Canal-area state parks."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "hood-canal-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-07"

STATE_PARK_URL = {
    slug: f"https://parks.wa.gov/find-parks/state-parks/{slug}"
    for slug in (
        "sequim-bay-state-park", "fort-worden-historical-state-park", "potlatch-state-park",
        "twanoh-state-park", "belfair-state-park", "jarrell-cove-state-park",
    )
}

CONTENT = {
    "sequim-bay-state-park": {
        "Short Description": "Olympic Peninsula park with standard and full-utility camping, a 40-foot equipment limit, and direct access to Sequim Bay and the Olympic Discovery Trail.",
        "Long description": "Sequim Bay State Park sits in the Olympic rain shadow beside a sheltered saltwater bay. The campground offers standard and full-utility sites, showers, drinking water, and a trailer dump, and the park accommodates RVs and vehicle-trailer combinations up to 40 feet. Reservations are available for May 15 through September 15 arrivals, with first-come camping outside that period. The Lower Loop is currently closed for restroom construction, with reopening still to be determined by the park.",
        "Number of RV campsites": "", "Max RV length": "40", "Hookups": "3", "RV Access": "yes",
        "Reservation window": "Reservable for May 15–September 15 arrivals; first-come September 16–May 14. Lower Loop currently closed for restroom construction; reopening TBD",
        "Access note": "The current park page does not publish a dependable full-utility site count, so the listing avoids an exact count. Lower Loop closure was posted August 30, 2026; confirm the current alert before arrival.",
    },
    "fort-worden-historical-state-park": {
        "Short Description": "Historic Port Townsend fort with 50 full-hookup beach sites and 30 water-and-electric forest sites, plus beaches, trails, museums, and lighthouse access.",
        "Long description": "Fort Worden has two developed campgrounds: 50 full-hookup sites at the Beach Campground and 30 water-and-electric sites in the Upper Forest Campground. Both have nearby restrooms and showers, and the park has a trailer dump. The current park page lists a maximum equipment length of 75 feet with limited availability. The reviewed directions point to the Beach Campground; the Upper Forest Campground has a separate internal entrance. Beach sites 18–50 are scheduled to close March 1 through June 30, 2027 for utility upgrades and new-site work.",
        "Number of RV campsites": "80", "Max RV length": "75", "Hookups": "3", "RV Access": "yes",
        "Reservation window": "Reservations required; 2026 camping offered April 1–October 31. Beach sites 18–50 closed March 1–June 30, 2027 for upgrades",
        "Access note": "Map pin and directions use the named Beach Campground. Upper Forest Campground has water and electric hookups; Beach Campground has water, electric, and sewer.",
    },
    "potlatch-state-park": {
        "Short Description": "Hood Canal park with 38 standard and 35 partial-hookup campsites, shoreline recreation, showers, and a seasonal trailer dump.",
        "Long description": "Potlatch State Park has 38 standard campsites, 35 partial-hookup sites, and two hiker/biker sites along Hood Canal. The state lists showers, drinking water, and a trailer dump; the dump and campground water close during the off-season. Sites 1–27 remain reservable year-round, while sites 36–93 close November 15 through March 31. An older official campground brochure lists equipment up to 60 feet, so travelers near that limit should confirm their individual site before booking.",
        "Number of RV campsites": "73", "Max RV length": "60", "Hookups": "2", "RV Access": "yes",
        "Reservation window": "Sites 1–27 reservable year-round; sites 36–93 closed November 15–March 31",
        "Access note": "The park publishes standard and partial-hookup inventory. Confirm the selected site's dimensions; the 60-foot maximum comes from the official campground brochure.",
    },
    "twanoh-state-park": {
        "Short Description": "Hood Canal park with 25 standard and 22 full-hookup campsites for equipment up to 35 feet; campground open first-come during the 2026 day-use restoration.",
        "Long description": "Twanoh State Park has 25 standard campsites and 22 full-hookup sites, with limited availability for equipment up to 35 feet. Two campground restrooms and a shower are nearby. The day-use area, main parking lots, beach, pier, dock, kitchen shelters, and day-use restrooms are closed through September 30, 2026 for shoreline and creek restoration, but the campground remains open first-come, first-served during the work. Campers should expect construction noise, potentially at night. The park lists a marine pumpout rather than a trailer dump.",
        "Number of RV campsites": "47", "Max RV length": "35", "Hookups": "3", "RV Access": "yes", "Dump station on site": "false",
        "Reservation window": "Campground open first-come during day-use construction through September 30, 2026; reservations resume if work ends early",
        "Access note": "The 2026 construction closure applies to day-use facilities, not the campground. The map pin and directions use the named campground point.",
    },
    "belfair-state-park": {
        "Short Description": "Year-round Hood Canal campground with standard and full-hookup sites, tidal wetlands, a swimming beach, showers, and a trailer dump.",
        "Long description": "Belfair State Park offers primitive, standard, and full-hookup camping beside Hood Canal, with showers, drinking water, and a trailer dump. Campsites are reservable year-round, while Tree Loop is available May 15 through September 15 and cannot accommodate trailers or motorhomes longer than 18 feet. Other loops have different site dimensions, so this listing does not publish one park-wide maximum or campground total. Check current health advisories before harvesting shellfish; Hood Canal was under a paralytic shellfish poisoning closure when this record was reviewed.",
        "Number of RV campsites": "", "Max RV length": "", "Hookups": "3", "RV Access": "yes",
        "Reservation window": "Primitive, standard, and full-hookup sites reservable year-round; Tree Loop open May 15–September 15",
        "Access note": "Equipment limits vary by loop and site. Tree Loop is limited to 18 feet; select the specific campsite using the reservation system's equipment limit.",
    },
    "jarrell-cove-state-park": {
        "Short Description": "Harstine Island park with 10 standard and 2 partial-hookup vehicle campsites, showers, forest trails, and protected saltwater moorage.",
        "Long description": "Jarrell Cove State Park is reached by road across the Harstine Island bridge or by boat. The current park page lists 10 standard vehicle campsites, two partial-hookup sites, and one Cascadia Marine Trail site reserved for travelers arriving by wind- or human-powered watercraft. Standard sites 5, 6, and 7 and the marine site are first-come; the other campsites are generally reservable year-round. Restrooms and showers are available. The pumpout serves boats at the cove; the park does not list a trailer dump for RVs.",
        "Number of RV campsites": "12", "Max RV length": "", "Hookups": "2", "RV Access": "yes", "Dump station on site": "false",
        "Reservation window": "Sites 5–7 and marine site MT22 first-come; all other campsites reservable, most year-round",
        "Access note": "The park page does not publish a park-wide RV length. Confirm the individual site's dimensions; the listed pumpout is a marine facility, not an RV trailer dump.",
    },
}

MAX_VALUES = {
    "sequim-bay-state-park": 40, "fort-worden-historical-state-park": 75,
    "potlatch-state-park": 60, "twanoh-state-park": 35,
    "belfair-state-park": None, "jarrell-cove-state-park": None,
}

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
            "operating_status": "The current operator page lists the park and its active dated closures; those limits are preserved in the canonical record.",
            "rv_access": "The current operator page or campground map identifies vehicle, RV, utility, or full-hookup campsites.",
            "reservation_method": "The current operator page identifies reservation availability and first-come or seasonal exceptions.",
            "max_rv_length": "The operator publishes this limit, or the record explicitly leaves a single park-wide limit unconfirmed when dimensions vary by site.",
            "hookups": "The current operator page or official campground map identifies the published utility level.",
        }
        source = {"url": STATE_PARK_URL[slug], "publisher": "Washington State Parks", "source_family": "washington-state-parks"}
        for field, value in values.items():
            evidence["observations"].append({"slug": slug, "field": field, "status": "corrected_locally", "checked_on": CHECKED,
                "summary": summaries[field], "proposed_value": value, "sources": [{**source, "evidence": summaries[field]}]})
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("Applied 6 Hood Canal location/route reviews and 12 grouped campground fact corrections.")

if __name__ == "__main__": main()
