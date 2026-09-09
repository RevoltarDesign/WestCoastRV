#!/usr/bin/env python3
"""Publish the reviewed Jefferson County county/city/port campground layer."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "jefferson-public-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
COVERAGE = HERE / "coverage-inventory.json"
CHECKED = "2026-09-09"

COUNTY = "https://jeffersoncountywa.myrec.com/info/facilities/default.aspx"
QUILCENE = "https://jeffersoncountywa.myrec.com/info/facilities/details.aspx?FacilityID=9916"
LELAND = "https://jeffersoncountywa.myrec.com/info/facilities/details.aspx?FacilityID=9914"
OAK_BAY = "https://jeffersoncountywa.myrec.com/info/facilities/details.aspx?FacilityID=9911"
COUNTY_BROCHURE = "https://jeffersoncountywa.myrec.com/forms/7455_no_year_parks_brochure_2025__fees_chart_update.pdf"
POINT_HUDSON = "https://portofpt.com/point-hudson-marina-rv-park/"
POINT_BOOKING = "https://www.camplife.com/1403/reservation/step1"
FAIR = "https://jeffcofairgrounds.org/campround/"
FAIR_BOOKING = "https://parkwith.us/camps/the-campground-at-jefferson-county-fairgrounds"

COMMON_COUNTY = {
    "Park Type": "County Campground", "Archived": "false", "Draft": "false",
    "RV Access": "yes", "Reservation window": "First-come, first-served; no reservations or site holding",
    "Hookups": "0", "Dump station on site": "false", "Generator policy": "1",
    "Cell coverage": "0", "Maneuverability": "2", "Site surface type": "Mixed",
    "Amenities: Showers": "false", "Amenities: Fire pits": "true",
}

ROWS = {
    "quilcene-campground": {
        **COMMON_COUNTY,
        "Name": "Quilcene Campground", "Nearest town": "Quilcene, WA",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/quilcene-campground.jpg",
        "Short Description": "Nine-site wooded county campground in central Quilcene with a 30-foot vehicle limit, fresh water, playground, courts, and first-come camping.",
        "Long description": "Quilcene Campground is a small wooded county campground beside the community center and US 101. Jefferson County publishes nine first-come campsites, each with a picnic table and fire ring, for vehicles up to 30 feet. Fresh water, toilets, trash service, a playground, basketball and tennis or pickleball courts are available. The campground operates April 1 through October 31; the park remains open for day use outside the camping season.",
        "Reservation website": QUILCENE, "Number of RV campsites": "9", "Max RV length": "30",
        "Amenities: Toilets": "Toilets", "Amenities: Drinking water": "true",
        "Amenities summary": "Fresh water, toilets, trash service, picnic tables, fire rings, playground, and courts; no campsite hookups or showers.",
        "Things to do for families": "Use the playground and courts\nWalk into Quilcene\nFish the Big Quilcene River under current rules\nVisit Quilcene Bay\nHike Mount Walker\nExplore Olympic Peninsula trails",
        "Things to do for families summary": "A simple in-town base with a playground, courts, Hood Canal access, and Olympic Peninsula day trips.",
        "Nearby nature & parks": "Quilcene sits where river valleys meet Hood Canal and the eastern Olympic Mountains. Mount Walker, Quilcene Bay, Lake Leland, and forest trailheads are practical day trips from this small central base.",
        "Site Recommendations": "All nine sites are first-come, with no site holding. Site sizes vary and the county limits vehicles to 30 feet, so arrive with a backup plan during busy weekends. The 2026 fee is $25 and ParkMobile is the required payment method.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "true", "Beach & Tide Pools": "false", "Boating": "false", "Playground": "true",
        "Access note": "Directly off US 101 beside the Quilcene Community Center; county materials publish a 30-foot vehicle maximum.", "Access source": QUILCENE, "Access checked": CHECKED,
        "Nearby campgrounds": "lake-leland-park-campground;seal-rock-campground;dosewallips-state-park;upper-oak-bay-campground",
    },
    "lake-leland-park-campground": {
        **COMMON_COUNTY,
        "Name": "Lake Leland Park Campground", "Nearest town": "Quilcene, WA",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/lake-leland-park-campground.jpg",
        "Short Description": "Twenty-two-site county campground at Lake Leland with a 30-foot limit, boat ramp, fishing pier, toilets, and no potable water or hookups.",
        "Long description": "Lake Leland Park Campground has 22 first-come campsites near a fishing lake six miles north of Quilcene. Sites include picnic tables and fire rings and accept vehicles up to 30 feet. The campground has toilets, trash service, a fishing pier, and a boat ramp, but the county explicitly says there is no potable water, so arrive with a full supply. Camping runs April 1 through October 31, while the waterfront day-use area remains active year-round.",
        "Reservation website": LELAND, "Number of RV campsites": "22", "Max RV length": "30",
        "Amenities: Toilets": "Toilets", "Amenities: Drinking water": "false",
        "Amenities summary": "Toilets, trash service, picnic tables, fire rings, fishing pier, and boat ramp; no potable water, showers, campsite hookups, or dump station.",
        "Things to do for families": "Fish from the pier\nLaunch a boat at the county ramp\nPaddle Lake Leland\nSwim when current water-quality guidance permits\nVisit Quilcene\nExplore Mount Walker",
        "Things to do for families summary": "Lake access for fishing, paddling, boating, and seasonal swimming, with dry first-come camping nearby.",
        "Nearby nature & parks": "Lake Leland is a small lowland lake between Discovery Bay and Quilcene. Check Jefferson County Public Health lake advisories before swimming or paddling because seasonal algae conditions can affect recreation.",
        "Site Recommendations": "All 22 campsites are first-come and the county publishes a 30-foot vehicle maximum. Bring all drinking water. The 2026 fee is $30 and ParkMobile is the required payment method.",
        "Hiking": "false", "Fishing": "true", "Swimming": "true", "Kayaking/Paddling": "true", "Beach & Tide Pools": "false", "Boating": "true", "Playground": "false",
        "Access note": "About 300 yards west of US 101 on Leland Valley Road; no potable water is available and vehicles are limited to 30 feet.", "Access source": LELAND, "Access checked": CHECKED,
        "Nearby campgrounds": "quilcene-campground;upper-oak-bay-campground;lower-oak-bay-campground;fort-worden-historical-state-park",
    },
    "upper-oak-bay-campground": {
        **COMMON_COUNTY,
        "Name": "Upper Oak Bay Campground", "Nearest town": "Port Hadlock, WA", "Hookups": "1",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/upper-oak-bay-campground.jpg",
        "Short Description": "Wooded county campground above Oak Bay with electric hookups at every public site, a 30-foot limit, beach access, water, and a playground.",
        "Long description": "Upper Oak Bay Campground occupies the wooded upland above Oak Bay, a short drive east of Port Hadlock. Jefferson County's live facility page lists 24 campsites with electrical hookups, picnic tables, and fire rings, plus fresh water, toilets, trash service, beach access, and a playground. The county limits vehicles to 30 feet. Camping is first-come from April 1 through October 31, with no reservations or site holding.",
        "Reservation website": OAK_BAY, "Number of RV campsites": "24", "Max RV length": "30",
        "Amenities: Toilets": "Toilets", "Amenities: Drinking water": "true",
        "Amenities summary": "Electrical service at all public sites, fresh water, toilets, trash service, picnic tables, fire rings, beach access, and playground; no showers or dump station.",
        "Things to do for families": "Walk to Oak Bay beach access\nUse the playground\nWatch birds and marine traffic\nFish under current regulations\nPaddle protected water when conditions allow\nVisit Port Townsend",
        "Things to do for families summary": "Electric camping in the woods with beach access, a playground, and easy Port Townsend day trips.",
        "Nearby nature & parks": "Upper Oak Bay looks toward Indian Island and the protected waters between Port Hadlock and Port Ludlow. Lower Oak Bay is nearby at shoreline level, while Fort Flagler and Port Townsend make easy day trips.",
        "Site Recommendations": "The live county page lists 24 electric campsites, while a 2025 brochure says 23 and the 2024 map labels 20 electric campsites plus other numbered positions. Treat 24 as the current operator total but check the posted map on arrival. All sites have a 30-foot vehicle maximum and are first-come. The 2026 fee is $35 and ParkMobile is required.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "true", "Beach & Tide Pools": "true", "Boating": "false", "Playground": "true",
        "Access note": "Follow Cleveland Street to Upper Oak Bay Park Road. The county publishes a 30-foot vehicle maximum.", "Access source": OAK_BAY, "Access checked": CHECKED,
        "Nearby campgrounds": "lower-oak-bay-campground;fort-flagler-historical-state-park;lake-leland-park-campground;point-hudson-marina-rv-park",
    },
    "lower-oak-bay-campground": {
        **COMMON_COUNTY,
        "Name": "Lower Oak Bay Campground", "Nearest town": "Port Hadlock, WA",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/lower-oak-bay-campground.jpg",
        "Short Description": "Small first-come county campground on an Oak Bay sand spit with beach access, fresh water, toilets, and a 30-foot vehicle maximum.",
        "Long description": "Lower Oak Bay Campground places dry campsites on a narrow shoreline setting beside a lagoon and Oak Bay. The current county facility page lists 12 campsites with picnic tables and fire rings, plus fresh water, toilets, trash service, beach access, and a nearby boat ramp. Vehicles are limited to 30 feet. Camping is first-come from April 1 through October 31, with no reservations or site holding.",
        "Reservation website": OAK_BAY, "Number of RV campsites": "12", "Max RV length": "30",
        "Amenities: Toilets": "Toilets", "Amenities: Drinking water": "true",
        "Amenities summary": "Fresh water, toilets, trash service, picnic tables, fire rings, beach access, and nearby boat ramp; no hookups, showers, or dump station.",
        "Things to do for families": "Explore the shoreline\nWatch shorebirds and marine traffic\nFish under current regulations\nLaunch a small boat nearby\nPaddle when tides and weather allow\nVisit Port Townsend",
        "Things to do for families summary": "Simple shoreline camping for beach access, birding, fishing, paddling, and nearby Port Townsend trips.",
        "Nearby nature & parks": "The lower campground sits on a sand spit at Oak Bay, close to tidal water and a lagoon. Its exposed shoreline setting is quite different from the wooded electric sites at Upper Oak Bay just uphill.",
        "Site Recommendations": "The live county page lists 12 campsites; a newer brochure lists eight, so check the posted campground diagram and current open-site markers on arrival. Sites are first-come with a 30-foot vehicle maximum. The 2026 fee is $30 and ParkMobile is required.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "true", "Beach & Tide Pools": "true", "Boating": "true", "Playground": "false",
        "Access note": "Follow Portage Way to the shoreline campground. The county publishes a 30-foot vehicle maximum.", "Access source": OAK_BAY, "Access checked": CHECKED,
        "Nearby campgrounds": "upper-oak-bay-campground;fort-flagler-historical-state-park;lake-leland-park-campground;point-hudson-marina-rv-park",
    },
    "point-hudson-marina-rv-park": {
        "Name": "Point Hudson Marina & RV Park", "Park Type": "City Campground", "Nearest town": "Port Townsend, WA",
        "Archived": "false", "Draft": "false", "RV Access": "yes", "Hookups": "3", "Generator policy": "1", "Cell coverage": "0", "Maneuverability": "1", "Site surface type": "Mixed",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/point-hudson-marina-rv-park.jpg",
        "Short Description": "Port-operated waterfront RV park in walkable Port Townsend with 46 full-hookup sites, two dry sites, showers, laundry, and online reservations.",
        "Long description": "Point Hudson Marina & RV Park sits on the Port Townsend waterfront beside the marina and a short walk from downtown. The Port of Port Townsend publishes 46 full-hookup sites and two sites without hookups. Guests have access-controlled restrooms, showers, and coin laundry; campfires and beach fires are prohibited. Online reservations are available through CampLife, and individual site dimensions should be confirmed during booking because the Port does not publish one park-wide RV maximum.",
        "Reservation window": "Reserve online through CampLife; 2026 general reservations opened January 21", "Reservation website": POINT_BOOKING,
        "Number of RV campsites": "48", "Max RV length": "", "Dump station on site": "false",
        "Amenities: Toilets": "Flush toilets", "Amenities: Showers": "true", "Amenities: Drinking water": "true", "Amenities: Fire pits": "false",
        "Amenities summary": "Most sites have full hookups; access-controlled restrooms, showers, coin laundry, and marina access are on site. Campfires and beach fires are prohibited.",
        "Things to do for families": "Walk Port Townsend's waterfront\nVisit Point Wilson Lighthouse\nExplore Fort Worden\nWatch ships enter Admiralty Inlet\nVisit downtown shops and restaurants\nPaddle or sail with a local outfitter",
        "Things to do for families summary": "A walkable waterfront base for Port Townsend, Fort Worden, maritime activities, and Admiralty Inlet views.",
        "Nearby nature & parks": "Point Hudson is at the northeast edge of downtown Port Townsend where Port Townsend Bay meets Admiralty Inlet. The shoreline walk continues toward Chetzemoka Park, Fort Worden, and Point Wilson.",
        "Site Recommendations": "The Port publishes 46 full-hookup sites and two dry sites but no single RV length limit. Use the live booking inventory to confirm pad length for your exact rig. This is a compact marina setting; check the site map before choosing a waterfront or interior position.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "true", "Beach & Tide Pools": "true", "Boating": "true", "Playground": "false",
        "Access note": "Use the named Point Hudson RV park entrance and current Port address; compact marina roads and site dimensions vary.", "Access source": POINT_HUDSON, "Access checked": CHECKED,
        "Nearby campgrounds": "fort-worden-historical-state-park;jefferson-county-fairgrounds-campground;fort-flagler-historical-state-park;upper-oak-bay-campground",
    },
    "jefferson-county-fairgrounds-campground": {
        "Name": "Jefferson County Fairgrounds Campground", "Park Type": "County Campground", "Nearest town": "Port Townsend, WA",
        "Archived": "false", "Draft": "false", "RV Access": "yes", "Hookups": "3", "Generator policy": "0", "Cell coverage": "1", "Maneuverability": "2", "Site surface type": "Mixed",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/jefferson-county-fairgrounds-campground.jpg",
        "Short Description": "Year-round Port Townsend campground with more than 50 full-, partial-, electric-, and dry-site choices, online reservations, showers, Wi-Fi, and a dump station.",
        "Long description": "The campground at Jefferson County Fairgrounds is a public, reservation-only base near Fort Worden and North Beach. Its nonprofit operator publishes more than 50 sites across full-hookup, power-and-water, electric-only, and dry options. Full-hookup sites accept rigs up to 50 feet; dry vehicle sites are limited to 20 feet. Restrooms, showers, community Wi-Fi, and a dump station are available. Some sites close in wet winter months and the entire public campground closes around the county fair, so check live inventory for the exact dates and site type.",
        "Reservation window": "Reservation required before arrival; book current inventory online", "Reservation website": FAIR_BOOKING,
        "Number of RV campsites": "", "Max RV length": "50", "Dump station on site": "true",
        "Amenities: Toilets": "Flush toilets", "Amenities: Showers": "true", "Amenities: Drinking water": "true", "Amenities: Fire pits": "false",
        "Amenities summary": "Full, partial, electric-only, and dry sites; restrooms, showers, community Wi-Fi, and dump station. Campfires and generators are prohibited.",
        "Things to do for families": "Walk or bike to Fort Worden\nVisit North Beach\nExplore Port Townsend\nUse nearby forested trails\nAttend fairgrounds events when open\nVisit Point Wilson Lighthouse",
        "Things to do for families summary": "An affordable Port Townsend base near Fort Worden, North Beach, trails, and community events.",
        "Nearby nature & parks": "The fairgrounds sit between Port Townsend neighborhoods, North Beach, and Fort Worden. This is a practical service-focused base rather than a wilderness campground, with shoreline and forest walks close by.",
        "Site Recommendations": "Reserve before arrival; an empty site may already be assigned. Full-hookup sites fit rigs up to 50 feet, while no-hookup vehicle sites cap equipment at 20 feet. Winter and event closures reduce inventory, and generators and campfires are prohibited.",
        "Hiking": "true", "Fishing": "false", "Swimming": "false", "Kayaking/Paddling": "false", "Beach & Tide Pools": "true", "Boating": "false", "Playground": "false",
        "Access note": "Use the separately named campground point at 4450 Jackman Street, not the center of the fairgrounds parcel.", "Access source": FAIR, "Access checked": CHECKED,
        "Nearby campgrounds": "fort-worden-historical-state-park;point-hudson-marina-rv-park;fort-flagler-historical-state-park;upper-oak-bay-campground",
    },
}

FACTS = {
    "quilcene-campground": {"url": QUILCENE, "publisher": "Jefferson County Parks & Recreation", "status": "Open seasonally April 1–October 31", "reservation": "First-come, no reservations", "max": 30, "hookups": 0},
    "lake-leland-park-campground": {"url": LELAND, "publisher": "Jefferson County Parks & Recreation", "status": "Open seasonally April 1–October 31", "reservation": "First-come, no reservations", "max": 30, "hookups": 0},
    "upper-oak-bay-campground": {"url": OAK_BAY, "publisher": "Jefferson County Parks & Recreation", "status": "Open seasonally April 1–October 31", "reservation": "First-come, no reservations", "max": 30, "hookups": 1},
    "lower-oak-bay-campground": {"url": OAK_BAY, "publisher": "Jefferson County Parks & Recreation", "status": "Open seasonally April 1–October 31", "reservation": "First-come, no reservations", "max": 30, "hookups": 0},
    "point-hudson-marina-rv-park": {"url": POINT_HUDSON, "publisher": "Port of Port Townsend", "status": "Open for transient RV reservations", "reservation": "Online reservation through CampLife", "max": None, "hookups": 3},
    "jefferson-county-fairgrounds-campground": {"url": FAIR, "publisher": "Jefferson County Fairgrounds Association", "status": "Year-round with seasonal and event closures", "reservation": "Online reservation required before occupying a site", "max": 50, "hookups": 3},
}

def duration(minutes):
    hours, mins = divmod(minutes, 60)
    return f"~{hours} hr {mins} min from Seattle" if mins else f"~{hours} hr from Seattle"

def main():
    reviews = json.loads(REVIEWS.read_text())["reviews"]
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source); fields, rows = list(reader.fieldnames or []), list(reader)
    by_slug = {row["Slug"]: row for row in rows}
    for review in reviews:
        slug = review["slug"]
        row = by_slug.get(slug, {field: "" for field in fields})
        row.update(ROWS[slug]); row["Slug"] = slug
        lat, lon, display = review["latitude"], review["longitude"], review["display_minutes"]
        row.update({
            "Data last updated": CHECKED, "Address": review["address"],
            "Latitude": f"{lat:.7f}", "Longitude": f"{lon:.7f}",
            "Google Maps Link": f"https://www.google.com/maps?q={lat:.7f},{lon:.7f}",
            "Coordinates source": review["coordinate_source"], "Coordinates checked": CHECKED,
            "Coordinate precision": review["precision"], "Drive distance miles": str(review["distance_miles"]),
            "Drive route minutes": str(review["observed_route_minutes"]), "Drive Time Minutes": str(display),
            "Time from Seattle": duration(display), "Drive Time Band": "2-3hrs",
            "Drive time origin": "Seattle, Washington",
            "Drive time source": f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat:.7f},{lon:.7f}&travelmode=driving",
            "Drive time checked": CHECKED, "Drive time note": review["route_note"],
        })
        if slug not in by_slug:
            rows.append(row); by_slug[slug] = row
    for slug, nearby in {
        "fort-worden-historical-state-park": "point-hudson-marina-rv-park;jefferson-county-fairgrounds-campground;fort-flagler-historical-state-park;fort-casey-historical-state-park",
        "fort-flagler-historical-state-park": "upper-oak-bay-campground;lower-oak-bay-campground;fort-worden-historical-state-park;point-hudson-marina-rv-park",
        "dosewallips-state-park": "seal-rock-campground;quilcene-campground;lake-leland-park-campground;potlatch-state-park",
        "seal-rock-campground": "dosewallips-state-park;quilcene-campground;lake-leland-park-campground;potlatch-state-park",
    }.items():
        by_slug[slug]["Nearby campgrounds"] = nearby
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

    coverage = json.loads(COVERAGE.read_text())
    section = next(s for s in coverage["sections"] if s["id"] == "jefferson-county-city-port")
    section["status"] = "complete"
    section["inventory_sources"] = [COUNTY, POINT_HUDSON, FAIR]
    decisions = {
        "Quilcene Campground": ("quilcene-campground", "Nine-site seasonal county campground accepts vehicles up to 30 feet."),
        "Lake Leland Park Campground": ("lake-leland-park-campground", "Twenty-two-site seasonal county campground accepts vehicles up to 30 feet."),
        "Upper Oak Bay Campground": ("upper-oak-bay-campground", "Seasonal county campground provides electrical service and accepts vehicles up to 30 feet."),
        "Lower Oak Bay Campground": ("lower-oak-bay-campground", "Seasonal shoreline county campground accepts vehicles up to 30 feet."),
        "Point Hudson Marina & RV Park": ("point-hudson-marina-rv-park", "Port-operated transient RV park publishes 48 sites and online reservations."),
        "Jefferson County Fairgrounds Campground": ("jefferson-county-fairgrounds-campground", "County-owned, nonprofit-operated campground is open to public reservations with full, partial, and dry options."),
    }
    for candidate in section["candidates"]:
        candidate["slug"], candidate["reason"] = decisions[candidate["name"]]
        candidate["decision"] = "included_new"
    COVERAGE.write_text(json.dumps(coverage, indent=2) + "\n")

    evidence = json.loads(EVIDENCE.read_text())
    slugs = set(ROWS)
    evidence["observations"] = [o for o in evidence["observations"] if o.get("slug") not in slugs]
    for slug, fact in FACTS.items():
        source = {"url": fact["url"], "publisher": fact["publisher"], "source_family": "jefferson-public-operator", "evidence": "Current operator page explicitly supports this published field."}
        values = {
            "operating_status": fact["status"], "rv_access": True,
            "reservation_method": fact["reservation"], "max_rv_length": fact["max"], "hookups": fact["hookups"],
        }
        for field, value in values.items():
            status = "unknown" if field == "max_rv_length" and value is None else "supported"
            summary = "The operator does not publish one park-wide maximum; verify the selected site." if status == "unknown" else f"Current operator information supports {field.replace('_', ' ')}: {value}."
            evidence_text = {
                "operating_status": f"The current operator page describes active overnight use and its applicable season or closure limits: {fact['status']}.",
                "rv_access": "The operator explicitly describes RV, trailer, vehicle-length, or hookup inventory for overnight use.",
                "reservation_method": f"The operator states the current way to obtain a site: {fact['reservation']}.",
                "max_rv_length": ("The operator publishes this maximum for the applicable RV sites."
                                  if value is not None else "The current operator page publishes no single park-wide RV maximum."),
                "hookups": "The operator explicitly lists the available campsite utility level; the dataset stores the highest available level.",
            }[field]
            field_source = dict(source, evidence=evidence_text)
            evidence["observations"].append({"slug": slug, "field": field, "status": status, "checked_on": CHECKED, "summary": summary, "proposed_value": value, "sources": [field_source]})
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n")
    print(f"Published 6 Jefferson County public campgrounds; dataset now contains {len(rows)} records.")

if __name__ == "__main__":
    main()
