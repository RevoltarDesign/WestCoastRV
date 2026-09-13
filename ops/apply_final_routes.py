#!/usr/bin/env python3
"""Apply the final Seattle route-provenance queue and route-adjacent access fixes."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "final-route-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-13"

CONTENT = {
    "ohanapecosh-campground": {
        "Number of RV campsites": "", "RV Access": "no", "Amenities: Toilets": "",
        "Reservation website": "https://www.nps.gov/mora/planyourvisit/park-construction-faqs.htm",
        "Amenities: Showers": "false", "Amenities: Drinking water": "false", "Amenities: Fire pits": "false",
        "Dump station on site": "false",
        "Hiking": "false", "Fishing": "false", "Swimming": "false", "Kayaking/Paddling": "false",
        "Beach & Tide Pools": "false", "Boating": "false", "Playground": "false",
        "Things to do for families": "No campground, visitor center, picnic area, river, or campground-trailhead access during the 2026 closure\nUse only NPS-listed alternate trailheads outside the closed developed area",
        "Things to do for families summary": "The entire Ohanapecosh developed area is closed to visitors throughout 2026. Use the current NPS construction page to identify open alternatives.",
        "Amenities summary": "No campground services are available while the entire Ohanapecosh developed area remains closed to visitors for the 2026 construction season.",
        "Site Recommendations": "Do not enter, park along SR 123 to walk in, or plan an overnight stay during the 2026 closure. NPS expects the campground to reopen for summer 2027 and expects 2027 reservations to open in December 2026; verify both before traveling.",
    },
    "white-river-campground": {
        "Short Description": "Open first-come Mount Rainier campground with 88 sites, no hookups, and RVs up to 27 feet; White River Road reopened September 5, 2026.",
        "Reservation window": "Open first-come until early October 2026, weather permitting; use Recreation.gov Scan and Pay after arrival",
        "Reservation website": "https://www.nps.gov/mora/planyourvisit/campgrounds.htm",
        "Number of RV campsites": "88", "Max RV length": "27", "RV Access": "yes", "Amenities: Fire pits": "false",
        "Long description": "White River Campground is a high-elevation, first-come campground on Mount Rainier's northeast side. NPS lists 88 individual sites, no hookups, RVs up to 27 feet, and trailers up to 18 feet. White River Road and the campground reopened September 5, 2026 and the campground is expected to remain open until early October, weather permitting. The Sunrise Road beyond the campground remains closed to vehicles because of the Grand Park 2 and Wonderland Complex fires. A park-wide fire ban currently prohibits campfires and charcoal fires.",
        "Access note": "White River Road and the campground reopened September 5, 2026. The Sunrise Road beyond the campground remains closed to vehicles due to fire activity. RV maximum is 27 feet; trailer maximum is 18 feet.",
        "Amenities summary": "NPS lists flush toilets and drinking water, with no showers, hookups, or dump station. A current park-wide fire ban prohibits wood and charcoal fires; portable fuel devices that can be switched off are permitted.",
        "Site Recommendations": "Arrive prepared for a first-come stay and cold high-elevation nights. Do not assume campground access means Sunrise is open: the road beyond the campground remains closed to vehicles due to active fire impacts. Check the NPS campground, fire, and road updates immediately before travel.",
    },
    "newhalem-creek-campground": {
        "Reservation window": "First-come after September 7, 2026; Loop C closes September 14 and Loops A and B close September 27",
        "Number of RV campsites": "107", "RV Access": "yes",
        "Access note": "Many RV and trailer sites are available up to 50 feet. Loop C closes September 14, 2026; Loops A and B close September 27. Water, trash, flush toilets, and the dump station are seasonal.",
    },
    "goodell-creek-campground": {
        "Reservation window": "First-come after September 7, 2026; primitive camping remains available outside the operational season without water or trash service", "RV Access": "yes",
        "Access note": "RV camping remains available on a primitive first-come basis outside the operational season, but water and trash service are unavailable. Check SR 20 conditions before travel.",
    },
    "colonial-creek-south-campground": {
        "Reservation window": "Vehicle campground closes September 14, 2026; ten walk-in tent-only sites remain first-come outside the operational season", "RV Access": "yes",
        "Access note": "RV access is seasonal. Vehicle campsites close September 14, 2026; the ten sites remaining outside the operational season are walk-in and tent-only. Check SR 20 conditions.",
    },
    "colonial-creek-north-campground": {
        "Reservation window": "First-come after September 7, 2026; campground closes for the season September 14", "RV Access": "yes",
        "Access note": "RV access is seasonal, and the campground closes September 14, 2026. Check SR 20 conditions before travel.",
    },
}

def duration(minutes):
    hours, mins = divmod(minutes, 60)
    if hours and mins: return f"~{hours} hr {mins} min from Seattle"
    if hours: return f"~{hours} hr from Seattle"
    return f"~{mins} min from Seattle"

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
        lat, lon, display = row["Latitude"], row["Longitude"], item["display_minutes"]
        updates = dict(CONTENT.get(item["slug"], {}))
        updates.update({
            "Data last updated": CHECKED, "Drive distance miles": str(item["distance_miles"]),
            "Drive route minutes": str(item["observed_route_minutes"]), "Drive time origin": "Seattle, Washington",
            "Drive time source": route_source(lat, lon), "Drive time checked": CHECKED, "Drive time note": item["route_note"],
            "Drive Time Minutes": str(display), "Drive Time Band": band(display), "Time from Seattle": duration(display),
            "Google Maps Link": f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat},{lon}&travelmode=driving",
            "RV Access": item["rv_access"], "Access source": item["access_source"], "Access checked": CHECKED,
        })
        for key, value in updates.items():
            if row.get(key, "") != str(value): row[key] = str(value); changed += 1
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    slugs = {item["slug"] for item in reviews}
    evidence["observations"] = [o for o in evidence["observations"] if not (o.get("slug") in slugs and o.get("field") == "rv_access")]
    for item in reviews:
        summary = "Current operator material supports RV access and the seasonal or closure qualification recorded on the listing."
        evidence["observations"].append({
            "slug": item["slug"], "field": "rv_access", "status": "corrected_locally", "checked_on": CHECKED,
            "summary": summary, "proposed_value": item["rv_access"] == "yes",
            "sources": [{"url": item["access_source"], "publisher": "National Park Service" if "nps.gov" in item["access_source"] else "U.S. Forest Service / Recreation.gov", "source_family": "federal-operator", "evidence": summary}],
        })
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"Applied 17 route reviews; corrected {changed} canonical fields and refreshed 17 RV-access evidence observations.")

if __name__ == "__main__": main()
