#!/usr/bin/env python3
"""Publish the reviewed Jefferson County private-campground layer."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "jefferson-private-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
COVERAGE = HERE / "coverage-inventory.json"
CHECKED = "2026-09-09"

REGIONAL = "https://cdn2.creativecirclemedia.com/ptleader/files/20250527-183002-db0-PT%20Leader%20Getaway%202025.pdf"
COVE = "https://coverv.com/accomodations/"
COVE_BOOKING = "https://www.campspot.com/book/cove-rv"
HARD_RAIN = "https://hohrainforest.wixsite.com/hardrain"
HARD_RAIN_COMMUNITY = "https://maps.campendium.com/us/forks-wa/food-drink/hard-rain-cafe-rv-park-forks"
PORT_LUDLOW = "https://portludlowrvpark.com/"
PORT_LUDLOW_COMMUNITY = "https://maps.campendium.com/us/port-ludlow-wa/camping-rv/port-ludlow-rv-park"
GOOD_SAM = "https://www.goodsam.com/campgrounds-rv-parks/washington/port-ludlow/port-ludlow-rv-park/cgid-201201387"
SMITTYS = "https://maps.campendium.com/us/wa/camping-rv/smittys-island-retreat-rv-park"
HOH_TRIBE = "https://hohtribe-nsn.org/"

BASE = {
    "Park Type": "Private Campground", "Archived": "false", "Draft": "false",
    "RV Access": "yes", "Amenities: Drinking water": "true",
}

ROWS = {
    "cove-rv-park-country-store": {
        **BASE, "Name": "Cove RV Park & Country Store", "Nearest town": "Brinnon, WA",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/cove-rv-park-country-store.jpg",
        "Short Description": "Small Hood Canal RV park near Brinnon with full hookups, sites for rigs up to 40 feet, hot showers, laundry, Wi-Fi, a country store, and online reservations.",
        "Long description": "Cove RV Park & Country Store is a small private campground on US 101 between Quilcene and Brinnon. The operator lists full-hookup standard sites with water, sewer, 30- or 50-amp power, and cable for RVs up to 40 feet. A smaller camper-van site has water and 30-amp power without sewer. Guests can use Wi-Fi, hot showers, laundry, a covered pavilion, games, loaner bicycles, a short creek trail, and the on-site store. Reservations are available through Campspot.",
        "Reservation window": "Reserve available dates online through Campspot", "Reservation website": COVE_BOOKING,
        "Number of RV campsites": "25", "Max RV length": "40", "Maneuverability": "2", "Site surface type": "Gravel",
        "Hookups": "3", "Dump station on site": "", "Generator policy": "", "Cell coverage": "1",
        "Amenities: Toilets": "Flush toilets", "Amenities: Showers": "true", "Amenities: Fire pits": "true",
        "Amenities summary": "Full hookups at standard RV sites, Wi-Fi, hot showers, laundry, picnic tables, campfire rings, pavilion, games, loaner bicycles, and an on-site country store.",
        "Things to do for families": "Walk the private Marple Creek trail\nBorrow a bicycle at the campground\nPlay basketball or lawn games\nExplore Hood Canal beaches\nVisit Rocky Brook Falls\nHike in Olympic National Forest",
        "Things to do for families summary": "A service-rich Hood Canal base with simple on-site recreation, a store, nearby beaches, waterfalls, and forest trails.",
        "Nearby nature & parks": "The park sits along the Hood Canal side of US 101 near Seal Rock and Dosewallips State Park. Brinnon-area beaches, the Duckabush and Dosewallips river valleys, and Olympic National Forest trailheads are close day trips.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "true", "Beach & Tide Pools": "true", "Boating": "true", "Playground": "false",
        "Site Recommendations": "Standard RV sites accept vehicles up to 40 feet and include full hookups. The smallest camper-van site has water and 30-amp power but no sewer, so confirm the site type during booking. The operator publishes 25 sites in the current regional inventory.",
        "Access note": "The named campground entrance is directly off US 101 at the operator's published address. Standard sites accept RVs up to 40 feet.", "Access source": COVE, "Access checked": CHECKED,
        "Nearby campgrounds": "seal-rock-campground;dosewallips-state-park;quilcene-campground;lake-leland-park-campground",
    },
    "hard-rain-cafe-campground": {
        **BASE, "Name": "Hard Rain Cafe & Campground", "Nearest town": "Forks, WA",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/hard-rain-cafe-campground.jpg",
        "Short Description": "Seasonal 13-site private campground on Upper Hoh Road with water-and-electric RV sites, hot showers, a cafe and store, and quick access to the Hoh Rain Forest.",
        "Long description": "Hard Rain Cafe & Campground is a compact seasonal base on Upper Hoh Road between US 101 and Olympic National Park's Hoh Rain Forest entrance. The operator publishes a March 15 through November 15 camping season and asks guests to reserve online with a nonrefundable first-night deposit. The current regional guide and community inventory list 13 sites; community reports identify 30-amp power and water at RV sites, hot showers, restrooms, picnic tables, and fire rings. Because the operator does not publish a park-wide vehicle maximum, the page uses the conservative 36-foot longest vehicle reported by campers and tells larger-rig travelers to confirm directly.",
        "Reservation window": "Camping March 15–November 15; reserve online with first-night deposit", "Reservation website": HARD_RAIN,
        "Number of RV campsites": "13", "Max RV length": "36", "Maneuverability": "2", "Site surface type": "Dirt",
        "Hookups": "2", "Dump station on site": "", "Generator policy": "", "Cell coverage": "2",
        "Amenities: Toilets": "Flush toilets", "Amenities: Showers": "true", "Amenities: Fire pits": "true",
        "Amenities summary": "Water and 30-amp electric service reported at RV sites, restrooms, hot showers, picnic tables, fire rings, cafe, store, and seasonal visitor services.",
        "Things to do for families": "Visit the Hoh Rain Forest early or after 6 p.m.\nWalk the nearby Land of Legends trails\nExplore Hall of Mosses\nStop at Ruby Beach\nWatch for elk and river wildlife\nEat at the seasonal cafe",
        "Things to do for families summary": "One of the closest private RV bases to the Hoh Rain Forest, with food, showers, forest trails, and Pacific coast day trips.",
        "Nearby nature & parks": "The campground lies between mile five and six of Upper Hoh Road, west of the national-park entrance. The Hoh River valley, Land of Legends trails, Olympic National Park, and Ruby Beach shape most trips from this remote base.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "true", "Beach & Tide Pools": "true", "Boating": "false", "Playground": "false",
        "Site Recommendations": "The operator does not publish a park-wide maximum length. A current community listing reports a 36-foot longest vehicle, so rigs near or above that length should call before reserving. Peak-season visitors should reach the Hoh entrance before 9 a.m. or consider an evening visit, following the operator's own guidance.",
        "Access note": "Use the named Hard Rain property at the operator's published Upper Hoh Road address. The campground shares the property with the cafe and store.", "Access source": HARD_RAIN, "Access checked": CHECKED,
        "Nearby campgrounds": "hoh-campground;kalaloch-campground;bogachiel-state-park;forks-101-rv-park",
    },
    "port-ludlow-rv-park": {
        **BASE, "Name": "Port Ludlow RV Park", "Nearest town": "Port Ludlow, WA",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/port-ludlow-rv-park.jpg",
        "Short Description": "Wooded year-round private park in Port Ludlow with 37 sites, full hookups, pull-through options, showers, Wi-Fi, and sites reported for RVs up to 40 feet.",
        "Long description": "Port Ludlow RV Park is a wooded private campground near the marina, Ludlow Falls, and the Hood Canal Bridge. The current Jefferson County visitor guide lists 37 sites, while the park and current campground directories describe full hookups, pull-through choices, restrooms, showers, Wi-Fi, picnic tables, and fire rings. The operator says sites accommodate rigs up to 40 feet. Reservations are handled directly by the park rather than through an online inventory, so call before arrival and confirm the fit of the assigned site.",
        "Reservation window": "Call the park directly for current availability", "Reservation website": PORT_LUDLOW,
        "Number of RV campsites": "37", "Max RV length": "40", "Maneuverability": "2", "Site surface type": "Gravel",
        "Hookups": "3", "Dump station on site": "true", "Generator policy": "", "Cell coverage": "2",
        "Amenities: Toilets": "Flush toilets", "Amenities: Showers": "true", "Amenities: Fire pits": "true",
        "Amenities summary": "Full hookups, pull-through choices, restrooms, hot showers, Wi-Fi, picnic tables, fire rings, and dump access; call for the current site assignment and services.",
        "Things to do for families": "Walk the Ludlow Falls trail\nVisit Port Ludlow Marina\nPaddle protected Port Ludlow Bay\nExplore Fort Flagler\nVisit Port Townsend\nWalk shoreline trails",
        "Things to do for families summary": "A quiet wooded base for Port Ludlow Bay, Ludlow Falls, Marrowstone Island, and Port Townsend day trips.",
        "Nearby nature & parks": "Port Ludlow Bay and the short Ludlow Falls trail are close to the campground. Fort Flagler, Oak Bay, Port Townsend, and Hood Canal shoreline access make practical half-day trips.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "true", "Beach & Tide Pools": "true", "Boating": "true", "Playground": "false",
        "Site Recommendations": "The operator states a 40-foot maximum and advertises pull-through sites, but wooded interior roads and pads vary. Call with total rig length and tow vehicle details. The current regional guide lists 37 sites; other directories range from 39 total to 37 spaces, so this page uses the local guide's count.",
        "Access note": "Use the exact named campground point on Breaker Lane rather than the center of Port Ludlow. Wooded internal roads and site dimensions vary.", "Access source": PORT_LUDLOW, "Access checked": CHECKED,
        "Nearby campgrounds": "upper-oak-bay-campground;lower-oak-bay-campground;fort-flagler-historical-state-park;point-hudson-marina-rv-park",
    },
}

FACTS = {
    "cove-rv-park-country-store": {
        "values": {"operating_status": "Current transient reservations available", "rv_access": True, "reservation_method": "Online through Campspot", "max_rv_length": 40, "hookups": 3},
        "sources": [(COVE, "Cove RV Park & Country Store", "Operator lists current RV site types, utilities, amenities, and its 40-foot limit."), (COVE_BOOKING, "Campspot", "Live booking page confirms transient RV inventory and the park identity."), (REGIONAL, "Olympic Peninsula Tourism Commission / Port Townsend Leader", "Current regional guide corroborates the campground, address, 25-site count, and hookups.")],
    },
    "hard-rain-cafe-campground": {
        "values": {"operating_status": "Seasonal March 15–November 15", "rv_access": True, "reservation_method": "Reserve online with first-night deposit", "max_rv_length": 36, "hookups": 2},
        "sources": [(HARD_RAIN, "Hard Rain Cafe & Campground", "Operator states the current season, reservation method, address, and active campground operation."), (REGIONAL, "Olympic Peninsula Tourism Commission / Port Townsend Leader", "Current regional guide corroborates 13 sites and RV hookups."), (HARD_RAIN_COMMUNITY, "Campendium", "Camper reports support water and 30-amp service and the conservative 36-foot vehicle figure.")],
    },
    "port-ludlow-rv-park": {
        "values": {"operating_status": "Open year-round", "rv_access": True, "reservation_method": "Call park directly for availability", "max_rv_length": 40, "hookups": 3},
        "sources": [(PORT_LUDLOW, "Port Ludlow RV Park", "Current park site states year-round operation, full hookups, amenities, address, and a 40-foot maximum."), (REGIONAL, "Olympic Peninsula Tourism Commission / Port Townsend Leader", "Current regional guide corroborates active private operation, 37 sites, address, and hookups."), (PORT_LUDLOW_COMMUNITY, "Campendium", "Current visitor reports and campground details corroborate transient stays, full hookups, and the 40-foot limit."), (GOOD_SAM, "Good Sam", "Current directory independently corroborates year-round public operation and contact details.")],
    },
}


def duration(minutes):
    hours, mins = divmod(minutes, 60)
    return f"~{hours} hr {mins} min from Seattle" if mins else f"~{hours} hr from Seattle"


def main():
    reviews = json.loads(REVIEWS.read_text())["reviews"]
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields, rows = list(reader.fieldnames or []), list(reader)
    by_slug = {row["Slug"]: row for row in rows}
    review_by_slug = {r["slug"]: r for r in reviews}
    for slug, values in ROWS.items():
        review = review_by_slug[slug]
        row = by_slug.get(slug, {field: "" for field in fields})
        row.update(values)
        lat, lon, display = review["latitude"], review["longitude"], review["display_minutes"]
        row.update({
            "Slug": slug, "Data last updated": CHECKED, "Address": review["address"],
            "Latitude": f"{lat:.7f}", "Longitude": f"{lon:.7f}",
            "Google Maps Link": f"https://www.google.com/maps?q={lat:.7f},{lon:.7f}",
            "Coordinates source": review["coordinate_source"], "Coordinates checked": CHECKED,
            "Coordinate precision": review["precision"], "Drive distance miles": str(review["distance_miles"]),
            "Drive route minutes": str(review["observed_route_minutes"]), "Drive Time Minutes": str(display),
            "Time from Seattle": duration(display),
            "Drive Time Band": "1-2hrs" if display < 120 else "2-3hrs" if display < 180 else "4plus",
            "Drive time origin": "Seattle, Washington",
            "Drive time source": f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat:.7f},{lon:.7f}&travelmode=driving",
            "Drive time checked": CHECKED, "Drive time note": review["route_note"],
        })
        if slug not in by_slug:
            rows.append(row)
            by_slug[slug] = row

    for slug, nearby in {
        "seal-rock-campground": "cove-rv-park-country-store;dosewallips-state-park;quilcene-campground;lake-leland-park-campground",
        "dosewallips-state-park": "cove-rv-park-country-store;seal-rock-campground;quilcene-campground;lake-leland-park-campground",
        "hoh-campground": "hard-rain-cafe-campground;kalaloch-campground;bogachiel-state-park;forks-101-rv-park",
        "fort-flagler-historical-state-park": "port-ludlow-rv-park;upper-oak-bay-campground;lower-oak-bay-campground;fort-worden-historical-state-park",
    }.items():
        by_slug[slug]["Nearby campgrounds"] = nearby

    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    coverage = json.loads(COVERAGE.read_text())
    coverage["updated_on"] = CHECKED
    section = next(s for s in coverage["sections"] if s["id"] == "jefferson-private-tribal")
    section.update({
        "status": "complete",
        "inventory_sources": [REGIONAL, COVE, HARD_RAIN, PORT_LUDLOW, HOH_TRIBE],
        "candidates": [
            {"name": "Cove RV Park & Country Store", "slug": "cove-rv-park-country-store", "decision": "included_new", "reason": "Current operator and booking pages support transient full-hookup RV stays."},
            {"name": "Hard Rain Cafe & Campground", "slug": "hard-rain-cafe-campground", "decision": "included_new", "reason": "Current operator page supports seasonal reservations and the regional inventory confirms RV sites."},
            {"name": "Port Ludlow RV Park", "slug": "port-ludlow-rv-park", "decision": "included_new", "reason": "Current local guide, operator page, map listing, and recent visitor reports support transient RV stays."},
            {"name": "Halfway RV Park", "decision": "excluded", "reason": "Present in older guides but absent from the current 2025 regional campground inventory and no current operator source was found."},
            {"name": "Smitty's Island Retreat RV Park", "decision": "excluded", "reason": "Recent visitor reporting describes a 30-day minimum and no overnight or short-stay option; it is outside the transient trip-planning scope."},
            {"name": "Hoh Tribe visitor RV campground", "decision": "excluded", "reason": "No public visitor RV campground or reservation channel appears in the Tribe's current official visitor-facing materials."},
        ],
    })
    COVERAGE.write_text(json.dumps(coverage, indent=2) + "\n")

    evidence = json.loads(EVIDENCE.read_text())
    slugs = set(ROWS)
    evidence["observations"] = [o for o in evidence["observations"] if o.get("slug") not in slugs]
    for slug, bundle in FACTS.items():
        for field, value in bundle["values"].items():
            sources = [{"url": url, "publisher": publisher, "source_family": "jefferson-private-review", "evidence": note} for url, publisher, note in bundle["sources"]]
            evidence["observations"].append({
                "slug": slug, "field": field, "status": "supported", "checked_on": CHECKED,
                "summary": f"Cross-source review supports {field.replace('_', ' ')}: {value}.",
                "proposed_value": value, "sources": sources,
            })
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n")
    print(f"Published 3 Jefferson County private campgrounds; dataset now contains {len(rows)} records.")


if __name__ == "__main__":
    main()
