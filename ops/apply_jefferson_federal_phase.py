#!/usr/bin/env python3
"""Publish the reviewed Jefferson County federal-facility layer."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "jefferson-federal-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
COVERAGE = HERE / "coverage-inventory.json"
CHECKED = "2026-09-09"

FOREST_INVENTORY = "https://www.fs.usda.gov/activity/olympic/recreation/camping-cabins/?actid=31&recid=47687"
COUNTY_INVENTORY = "https://www.co.jefferson.wa.us/DocumentCenter/View/18148/2022-Jeff-Co-PROS-Plan?bidId="
FALLS_VIEW = "https://www.recreation.gov/camping/campgrounds/10355712"
COLLINS = "https://www.recreation.gov/camping/campgrounds/10355676"
SEAL_RIG_DIRECTORY = "https://www.allstays.com/Campgrounds-details/32601.htm"
NPS_CAMPING = "https://www.nps.gov/olym/planyourvisit/camping.htm"
NPS_CONDITIONS = "https://www.nps.gov/olym/planyourvisit/conditions.htm"

FALLS_ROW = {
    "Name": "Falls View Campground", "Slug": "falls-view-campground",
    "Data last updated": CHECKED, "Archived": "false", "Draft": "false",
    "Park Type": "National Forest", "RV Access": "yes", "Nearest town": "Quilcene, WA",
    "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/falls-view-campground.jpg",
    "Short Description": "Small Olympic National Forest campground directly off US 101 near Quilcene, currently listing 11 sites, dry camping, and selected RV spaces up to 35 feet.",
    "Long description": "Falls View Campground sits directly off US 101 in conifer and rhododendron forest above the Big Quilcene River. The current Recreation.gov overview says the campground offers 11 sites and can accommodate small RVs, while its facility detail retains the larger historic loop layout and says selected spaces accept trailers or motorhomes up to 35 feet. The Forest Service currently labels the facility open. Camping is first-come and paid on arrival through Recreation.gov Scan & Pay; there are no hookups or potable water. Confirm the open loop and an individual site before bringing a longer rig.",
    "Reservation window": "First-come, first-served; claim and pay on arrival with Recreation.gov Scan & Pay",
    "Reservation website": FALLS_VIEW, "Number of RV campsites": "11", "Max RV length": "35",
    "Maneuverability": "2", "Site surface type": "Mixed", "Hookups": "0",
    "Dump station on site": "false", "Generator policy": "1", "Cell coverage": "1",
    "Amenities: Toilets": "Vaulted toilets", "Amenities: Showers": "false",
    "Amenities: Drinking water": "false", "Amenities: Fire pits": "true",
    "Amenities summary": "Dry camping with toilets, garbage service, tables, and fire rings. No hookups or potable water; download the Recreation.gov app before arriving.",
    "Things to do for families": "Walk the short Falls View loop\nSee the Big Quilcene River waterfall\nExplore nearby Mount Walker\nVisit Quilcene Bay\nHike Olympic National Forest trails\nFish under current regulations",
    "Things to do for families summary": "A simple highway-accessible forest base for a short waterfall walk, Mount Walker, Quilcene Bay, and nearby trailheads.",
    "Nearby nature & parks": "The campground occupies a forested bench above the Big Quilcene River. Its short loop reaches a waterfall viewpoint, while Mount Walker, Quilcene Bay, and eastern Olympic Mountain trailheads are nearby.",
    "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "false",
    "Beach & Tide Pools": "false", "Boating": "false", "Playground": "false",
    "Site Recommendations": "The current overview says 11 sites are offered, but the facility detail still describes the older two-loop layout. Treat 35 feet as a selected-site maximum rather than a campground-wide promise. Bring all drinking water and download Scan & Pay before leaving coverage.",
    "Access note": "The exact named campground entrance is directly off US 101 about 3.5 miles south of Quilcene. Confirm that the RV loop is open before towing to the campground.",
    "Access source": FALLS_VIEW, "Access checked": CHECKED,
    "Nearby campgrounds": "quilcene-campground;lake-leland-park-campground;seal-rock-campground;cove-rv-park-country-store",
}

SEAL_UPDATES = {
    "Data last updated": CHECKED, "Draft": "false", "RV Access": "yes",
    "Short Description": "Hood Canal National Forest campground with 41 tent/RV sites and a current 21-foot published RV limit; the Forest Service presently labels the facility closed.",
    "Long description": "Seal Rock is a saltwater Olympic National Forest campground on Hood Canal with 41 tent/RV sites, including three paved accessible units. The Forest Service's current recreation inventory labels the facility closed, so do not rely on it for an overnight stop until the operator posts a reopening. Current Forest Service trip material publishes a 21-foot RV and trailer maximum, correcting the older 40-foot figure previously shown here. When open, the campground provides drinking water, flush toilets, waterfront access, shellfish opportunities subject to WDFW rules, and two short interpretive trails.",
    "Reservation window": "Campground closed; check Forest Service status before travel",
    "Reservation website": FOREST_INVENTORY, "Max RV length": "21",
    "Address": "305365 US Highway 101, Brinnon, WA 98320",
    "Site Recommendations": "The Forest Service currently lists Seal Rock closed. When it reopens, use 21 feet as the published RV and trailer maximum and confirm the assigned site. Check WDFW shellfish status separately before harvesting.",
    "Access note": "Use the exact named campground entrance at 305365 US 101. The Forest Service currently lists the facility closed and publishes a 21-foot RV/trailer maximum.",
    "Access source": FOREST_INVENTORY, "Access checked": CHECKED,
    "Nearby campgrounds": "cove-rv-park-country-store;dosewallips-state-park;falls-view-campground;quilcene-campground",
}


def duration(minutes):
    hours, mins = divmod(minutes, 60)
    return f"~{hours} hr {mins} min from Seattle" if mins else f"~{hours} hr from Seattle"


def apply_location(row, review):
    lat, lon, display = review["latitude"], review["longitude"], review["display_minutes"]
    row.update({
        "Address": review["address"], "Latitude": f"{lat:.7f}", "Longitude": f"{lon:.7f}",
        "Google Maps Link": f"https://www.google.com/maps?q={lat:.7f},{lon:.7f}",
        "Coordinates source": review["coordinate_source"], "Coordinates checked": CHECKED,
        "Coordinate precision": review["precision"], "Drive distance miles": str(review["distance_miles"]),
        "Drive route minutes": str(review["observed_route_minutes"]), "Drive Time Minutes": str(display),
        "Time from Seattle": duration(display), "Drive Time Band": "1-2hrs" if display < 120 else "2-3hrs",
        "Drive time origin": "Seattle, Washington",
        "Drive time source": f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat:.7f},{lon:.7f}&travelmode=driving",
        "Drive time checked": CHECKED, "Drive time note": review["route_note"],
    })


def source(url, publisher, evidence):
    return {"url": url, "publisher": publisher, "source_family": "jefferson-federal-review", "evidence": evidence}


def main():
    reviews = {r["slug"]: r for r in json.loads(REVIEWS.read_text())["reviews"]}
    with MASTER.open(newline="", encoding="utf-8-sig") as source_file:
        reader = csv.DictReader(source_file); fields, rows = list(reader.fieldnames or []), list(reader)
    by_slug = {row["Slug"]: row for row in rows}

    falls = by_slug.get("falls-view-campground", {field: "" for field in fields})
    falls.update(FALLS_ROW); apply_location(falls, reviews["falls-view-campground"])
    if "falls-view-campground" not in by_slug:
        rows.append(falls); by_slug["falls-view-campground"] = falls
    seal = by_slug["seal-rock-campground"]
    seal.update(SEAL_UPDATES); apply_location(seal, reviews["seal-rock-campground"])

    for slug, nearby in {
        "quilcene-campground": "falls-view-campground;lake-leland-park-campground;seal-rock-campground;cove-rv-park-country-store",
        "cove-rv-park-country-store": "seal-rock-campground;dosewallips-state-park;falls-view-campground;quilcene-campground",
    }.items():
        by_slug[slug]["Nearby campgrounds"] = nearby

    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

    coverage = json.loads(COVERAGE.read_text()); coverage["updated_on"] = CHECKED
    section = next((s for s in coverage["sections"] if s["id"] == "jefferson-federal"), None)
    payload = {
        "id": "jefferson-federal", "county": "Jefferson", "operator_layer": "federal", "status": "complete",
        "inventory_sources": [COUNTY_INVENTORY, FOREST_INVENTORY, NPS_CAMPING, NPS_CONDITIONS],
        "candidates": [
            {"name": "Hoh Campground", "slug": "hoh-campground", "decision": "included_existing", "reason": "NPS publishes current RV access, seasonal reservations, and operating status."},
            {"name": "Kalaloch Campground", "slug": "kalaloch-campground", "decision": "included_existing", "reason": "NPS publishes current RV access, summer reservations, and year-round operation."},
            {"name": "South Beach Campground", "slug": "south-beach-campground", "decision": "included_existing", "reason": "NPS publishes seasonal first-come camping and selected RV sites up to 35 feet."},
            {"name": "Queets Campground", "decision": "excluded", "reason": "NPS explicitly says RVs and trailers are not recommended on the remote Upper Queets access road."},
            {"name": "Seal Rock Campground", "slug": "seal-rock-campground", "decision": "included_existing", "reason": "Developed RV campground retained with a prominent current closure notice and corrected 21-foot limit."},
            {"name": "Falls View Campground", "slug": "falls-view-campground", "decision": "included_new", "reason": "Current federal inventory labels it open and Recreation.gov confirms first-come dry sites with selected RV capacity to 35 feet."},
            {"name": "Collins Campground", "decision": "deferred", "reason": "Recreation.gov maintains active facility details, but the current Forest Service inventory labels the site closed; publish after status is reconciled."},
            {"name": "Elkhorn Campground", "decision": "excluded", "reason": "Road washouts eliminated motor-vehicle access; the Forest Service describes the remaining area as a walk-in dispersed camp."},
            {"name": "Rainbow Campground", "decision": "excluded", "reason": "The former campground is decommissioned and gated; only trail access remains."},
            {"name": "Interrorem Cabin", "decision": "excluded", "reason": "Bookable cabin lodging rather than a transient RV campground."},
            {"name": "Mount Walker Viewpoint", "decision": "excluded", "reason": "Day-use viewpoint without legal overnight campsites."},
        ],
    }
    if section: section.update(payload)
    else: coverage["sections"].insert(1, payload)
    COVERAGE.write_text(json.dumps(coverage, indent=2) + "\n")

    evidence = json.loads(EVIDENCE.read_text())
    reviewed = {"falls-view-campground", "seal-rock-campground"}
    evidence["observations"] = [o for o in evidence["observations"] if o.get("slug") not in reviewed]
    facts = {
        "falls-view-campground": {
            "values": {"operating_status": "Open in current Forest Service inventory", "rv_access": True, "reservation_method": "First-come with Scan & Pay", "max_rv_length": 35, "hookups": 0},
            "sources": [source(FOREST_INVENTORY, "US Forest Service", "Current Olympic National Forest inventory labels Falls View open."), source(FALLS_VIEW, "Recreation.gov / US Forest Service", "Current facility record supports first-come operation, dry camping, and selected RV sites up to 35 feet.")],
        },
        "seal-rock-campground": {
            "values": {"operating_status": "Currently listed closed", "rv_access": True, "reservation_method": "No current booking while closed", "max_rv_length": 21, "hookups": 0},
            "sources": [source(FOREST_INVENTORY, "US Forest Service", "Current inventory labels Seal Rock closed and identifies 41 tent/RV sites."), source(SEAL_RIG_DIRECTORY, "AllStays", "Current campground directory independently reports the 21-foot RV maximum from the Forest Service facility record.")],
        },
    }
    for slug, bundle in facts.items():
        for field, value in bundle["values"].items():
            evidence["observations"].append({
                "slug": slug, "field": field, "status": "supported", "checked_on": CHECKED,
                "summary": f"Cross-source federal review supports {field.replace('_', ' ')}: {value}.",
                "proposed_value": value, "sources": bundle["sources"],
            })
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n")
    print(f"Completed Jefferson federal review; dataset now contains {len(rows)} records.")


if __name__ == "__main__":
    main()
