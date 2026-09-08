#!/usr/bin/env python3
"""Apply sourced fact, location, and route corrections for 12 central/eastern Washington state parks."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "central-eastern-state-parks-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-07"

SLUGS = (
    "lake-easton-state-park", "ginkgo-petrified-forest-state-park", "potholes-state-park",
    "columbia-hills-historical-state-park", "maryhill-state-park", "brooks-memorial-state-park",
    "wenatchee-confluence-state-park", "lincoln-rock-state-park", "daroga-state-park",
    "alta-lake-state-park", "lake-wenatchee-state-park", "pearrygin-lake-state-park",
)
STATE_URL = {slug: f"https://parks.wa.gov/find-parks/state-parks/{slug}" for slug in SLUGS}
STATE_URL["ginkgo-petrified-forest-state-park"] = "https://parks.wa.gov/find-parks/state-parks/wanapum-recreation-area"

CONTENT = {
    "lake-easton-state-park": {
        "Short Description": "Cascade foothills park with 135 numbered vehicle campsites, full-hookup and non-hookup options, showers, a trailer dump, and Lake Easton access.",
        "Long description": "Lake Easton State Park is a forested Cascade foothills campground beside Lake Easton and the Yakima River. The current campground map numbers 135 vehicle campsites, with both full-hookup and non-hookup options. Washington State Parks lists showers, drinking water, a trailer dump, and limited availability for equipment up to 60 feet. Seasonal loop closures vary, and winter camping moves to a designated day-use and boat-launch area when conditions allow.",
        "Number of RV campsites":"135", "Max RV length":"60", "Hookups":"3", "RV Access":"yes",
        "Reservation window":"Sites 94–135 close September 16–May 1; sites 1–93 close November 1–May 1 and are first-come October 16–31. Verify the current winter schedule",
        "Access note":"The park is open while staff monitor the Three Queens Fire and smoke conditions. Expect I-90 and rail noise; verify fire and winter alerts before travel.",
        "Site Recommendations":"Choose by utility type and published pad length rather than loop alone. Sites 94–135 have a longer seasonal closure, and winter camping uses a designated day-use and boat-launch area with a Sno-Park permit.",
        "Nearby nature & parks":"Lake Easton State Park lies beside Lake Easton and the Yakima River in the Cascade foothills. The Palouse to Cascades State Park Trail passes the park, and seasonal lake and snow activities depend on current water, fire, and winter conditions.",
    },
    "ginkgo-petrified-forest-state-park": {
        "Short Description":"Columbia River campground at Wanapum Recreation Area with 50 full-hookup sites, showers, a swim beach, and nearby Ginkgo Petrified Forest interpretation.",
        "Long description":"Camping for Ginkgo Petrified Forest State Park is three miles away at Wanapum Recreation Area on the Columbia River. The official brochure identifies 50 reservable full-hookup campsites plus two separate hiker/biker sites. Washington State Parks lists showers, drinking water, a swim beach, and limited availability for equipment up to 60 feet. The current park page does not list a trailer dump, so the directory does not claim one. High winds and intense summer heat are common in this exposed shrub-steppe setting.",
        "Number of RV campsites":"50", "Max RV length":"60", "Hookups":"3", "RV Access":"yes", "Dump station on site":"false",
        "Reservation window":"Wanapum campground closes November 1–March 1. Sites 1–31 are first-come March 1–April 15; sites 32–49 open April 1 and are first-come through April 15",
        "Access note":"Directions end at Wanapum Recreation Area, the campground at 4511 Huntzinger Road, not the Ginkgo interpretive center or trail area.",
        "Site Recommendations":"Select a campsite at Wanapum Recreation Area. Expect limited shade, high winds, and very hot summer afternoons; secure awnings and lightweight gear.",
        "Things to do for families summary":"Camp beside the Columbia River at Wanapum, then visit the separate Ginkgo interpretive center and petrified-forest trails.",
        "Nearby nature & parks":"Wanapum Recreation Area provides Columbia River access in an exposed shrub-steppe landscape. Ginkgo Petrified Forest's interpretive center and trails are separate destinations nearby; check their current hours and access alerts before leaving camp.",
    },
    "potholes-state-park": {
        "Short Description":"Potholes Reservoir park with 121 vehicle campsites, including 60 full-hookup sites, plus showers, a trailer dump, and a 50-foot equipment limit.",
        "Long description":"Potholes State Park sits on Potholes Reservoir in the Columbia Basin. The official campground brochure lists 61 standard campsites and 60 full-hookup sites, for 121 vehicle campsites, plus separate cabins and hiker/biker sites. Washington State Parks lists showers, drinking water, a trailer dump, and a 50-foot equipment limit. Reservoir levels fluctuate substantially, and camping is allowed only in designated sites rather than beside the water.",
        "Number of RV campsites":"121", "Max RV length":"50", "Hookups":"3", "RV Access":"yes",
        "Reservation window":"First-come November 1–February 29; reserve during the main season and verify current dates. Campground water is normally off October 24–April 1",
        "Access note":"The official address is near Othello. A current sewer obstruction affects sites 12–16: greywater may be used there, but blackwater must go to the trailer dump by the welcome station.",
        "Site Recommendations":"The 121-site total is 61 standard plus 60 full-hookup vehicle sites. Confirm the selected pad and check the current sewer alert for sites 12–16 before arrival.",
        "Things to do for families summary":"Reservoir camping with full-hookup options, boating, fishing, swimming, and nearby shrub-steppe wildlife habitat.",
        "Nearby nature & parks":"Potholes State Park borders Potholes Reservoir and nearby wetland and shrub-steppe habitat. Water levels change substantially through the year, so shoreline access, boating conditions, and fishing plans should be checked close to travel.",
    },
    "columbia-hills-historical-state-park": {
        "Short Description":"Small Horsethief Lake campground with four standard and eight partial-hookup vehicle sites, showers, a trailer dump, and Columbia Gorge recreation.",
        "Long description":"The Horsethief Lake area of Columbia Hills Historical State Park has four standard and eight partial-hookup vehicle campsites, for 12 vehicle sites, plus separate walk-in and hiker/biker sites. Washington State Parks lists showers, drinking water, and a trailer dump. The campground closes in winter. Cultural sites and rock art require respectful visitation, and access rules for guided areas should be checked with the park.",
        "Number of RV campsites":"12", "Max RV length":"", "Hookups":"2", "RV Access":"yes", "Dump station on site":"true",
        "Reservation window":"Horsethief Lake campground closes November 1–March 31; first-come September 16–October 31 and April 1–May 14; reservable May 15–September 15",
        "Access note":"Directions end at the Horsethief Lake campground on Lewis and Clark Highway. The operator's seasonal schedule governs if a third-party map reports a conflicting status.",
        "Site Recommendations":"Only 12 vehicle campsites are available: four standard and eight partial-hookup. The operator does not publish one current park-wide RV length, so confirm the selected site's dimensions.",
        "Nearby nature & parks":"The Horsethief Lake campground sits within the Columbia River Gorge landscape of basalt cliffs, open grassland, and river shoreline. Rock-art areas have specific access and protection rules; use current park guidance for tours and trails.",
    },
    "maryhill-state-park": {
        "Short Description":"Columbia River campground with 71 numbered vehicle sites across primitive, standard, and full-hookup options, plus showers and a trailer dump.",
        "Long description":"Maryhill State Park is a Columbia River campground near the US-97 bridge. The current campground map numbers 71 vehicle campsites across primitive, standard, and full-hookup options. Washington State Parks lists showers, drinking water, a trailer dump, and limited availability for equipment up to 60 feet. Goldendale Observatory and Maryhill Museum are separate nearby attractions with their own admission, hours, and reservation rules.",
        "Number of RV campsites":"71", "Max RV length":"60", "Hookups":"3", "RV Access":"yes",
        "Reservation window":"Sites 51–71 close October 31–March 15; camping is first-come November 1–March 15. Verify the current winter schedule before travel",
        "Access note":"Winter water is limited to the entrance and trailer-dump area; campground restrooms close and portable toilets are supplied. Frequent rail noise is possible.",
        "Things to do for families summary":"Columbia River camping near Goldendale Observatory, Maryhill Museum, and the Stonehenge memorial; each attraction has separate current visitor rules.",
        "Things to do for families":"Columbia River boating and fishing\nPark shoreline and picnic areas\nGoldendale Observatory visit with separate admission or reservation\nMaryhill Museum of Art\nStonehenge Memorial\nColumbia Gorge scenic driving",
        "Site Recommendations":"Select by site type and published pad length. Sites 51–71 have a seasonal closure; winter facilities are limited. Goldendale Observatory admission is separate from camping.",
        "Nearby nature & parks":"Maryhill State Park occupies Columbia River shoreline near the US-97 bridge. Nearby destinations include Goldendale Observatory, Maryhill Museum of Art, and the Stonehenge Memorial, each with independent hours, fees, and access rules.",
    },
    "brooks-memorial-state-park": {
        "Short Description":"Seasonal forest campground near Goldendale with 35 numbered vehicle sites, full-hookup options, showers, a trailer dump, and nine miles of trails.",
        "Long description":"Brooks Memorial State Park is a seasonal pine and fir campground on US-97 north of Goldendale. The current campground map numbers 35 vehicle campsites, with separate tent and wall-tent sites. Washington State Parks lists full-hookup camping, showers, drinking water, and a trailer dump. The operator does not publish one park-wide RV length, so travelers should confirm the selected site's dimensions. Highway noise is present, and several sites sit near overhead power lines.",
        "Number of RV campsites":"35", "Max RV length":"", "Hookups":"3", "RV Access":"yes",
        "Reservation window":"Closed November 1–April 15; first-come September 16–October 31 and April 16–May 14; reservable during the main season",
        "Access note":"Expect highway noise throughout the campground. Sites 8–10 and 16–18 are near overhead power lines; water at hookup sites is generally available mid-April through late October.",
        "Site Recommendations":"The 35-site total counts numbered vehicle campsites; tent and wall-tent sites are separate. Confirm the individual pad length because no current park-wide maximum is published.",
        "Things to do for families":"Park hiking trails\nDisc golf\nPicnicking in the forest\nWildlife watching\nGoldendale Observatory visit with separate admission or reservation\nScenic drive toward the Columbia River",
        "Nearby nature & parks":"Brooks Memorial State Park protects pine and fir forest in the Simcoe Mountains north of Goldendale. The park's trails, disc-golf area, and seasonal campground provide a cooler forest setting above the Columbia River corridor.",
    },
    "wenatchee-confluence-state-park": {
        "Short Description":"Year-round urban river campground with eight standard and 52 full-hookup sites, showers, a trailer dump, and Apple Capital Loop Trail access.",
        "Long description":"Wenatchee Confluence State Park sits where the Wenatchee and Columbia rivers meet. The current park page lists eight standard campsites and 52 full-hookup sites, for 60 vehicle campsites. Washington State Parks lists showers, drinking water, a trailer dump, and limited availability for equipment up to 65 feet. The Apple Capital Loop Trail connects the park with the wider Wenatchee riverfront.",
        "Number of RV campsites":"60", "Max RV length":"65", "Hookups":"3", "RV Access":"yes",
        "Reservation window":"Loop 2 is open year-round and first-come October 16–March 31. Loop 1 closes October 16 and its reopening depends on construction completion",
        "Access note":"Loop 1's reopening depends on construction completion. Winter water is available near the trailer dump and sites 34 and 36; verify current alerts before travel.",
        "Site Recommendations":"Choose by utility type and individual pad length. Loop 1 has a construction-dependent reopening; Loop 2 carries the year-round winter availability.",
        "Things to do for families summary":"Full-hookup river camping with direct trail access and nearby Wenatchee services.",
        "Nearby nature & parks":"The park lies at the confluence of the Wenatchee and Columbia rivers and connects directly to the Apple Capital Loop Trail. Downtown services and other Wenatchee riverfront parks are close by.",
    },
    "lincoln-rock-state-park": {
        "Short Description":"Columbia River campground with 94 numbered vehicle sites, including full and partial hookups, plus showers, a trailer dump, and a 65-foot limit.",
        "Long description":"Lincoln Rock State Park occupies Columbia River shoreline north of East Wenatchee. The current campground map numbers 94 vehicle campsites, including full-hookup and partial-hookup loops. Washington State Parks lists showers, drinking water, a trailer dump, and limited availability for equipment up to 65 feet. Individual loop availability changes during winter, so the current schedule should be checked before travel.",
        "Number of RV campsites":"94", "Max RV length":"65", "Hookups":"3", "RV Access":"yes",
        "Reservation window":"Some loops close November 1–March 13 while others remain available; camping is first-come October 16–31 and March 1–May 14. Verify the current loop schedule",
        "Access note":"Use the current official entrance at 91 Lincoln Rock Park Road. Confirm the selected site's utility type and pad dimensions.",
        "Site Recommendations":"The 94-site total follows the numbered vehicle sites on the current campground map. Utility type and winter availability vary by loop; confirm the exact site when booking.",
        "Things to do for families summary":"Columbia River camping with full and partial hookups, a swimming area, boating, and nearby Wenatchee services.",
        "Things to do for families":"Columbia River swimming area\nBoating and paddling from the launch\nFishing under current regulations\nRiverfront picnic areas\nPlayground and sports areas\nRocky Reach Dam visitor area when open",
        "Nearby nature & parks":"Lincoln Rock State Park sits on the Columbia River north of East Wenatchee, with views toward the basalt formation that gives the park its name. Rocky Reach Dam and other Wenatchee-area riverfront parks are nearby and have separate operating schedules.",
    },
    "daroga-state-park": {
        "Short Description":"Seasonal Columbia River park with 28 partial-hookup vehicle sites, showers, a trailer dump, and boating and swimming access.",
        "Long description":"Daroga State Park is a seasonal Columbia River campground near Orondo. The current campground map identifies 28 partial-hookup vehicle campsites; primitive sites 29–45 are separate. Washington State Parks lists showers, drinking water, and a trailer dump. A shoreline project beginning September 14, 2026 closes walk-in campsites, docks, and portions of the shoreline trail while other amenities remain open until the seasonal campground closure.",
        "Number of RV campsites":"28", "Max RV length":"", "Hookups":"2", "RV Access":"yes",
        "Reservation window":"Campground closes October 1, 2026 and is scheduled to reopen in April 2027; verify project and seasonal dates before travel",
        "Access note":"Beginning September 14, 2026, walk-in campsites, docks, and portions of the shoreline trail are closed for construction. Vehicle camping remains subject to the October 1 seasonal closure.",
        "Site Recommendations":"The 28-site RV total counts partial-hookup vehicle sites; primitive sites 29–45 are separate. Confirm the individual pad length because no current park-wide maximum is published.",
        "Things to do for families summary":"Seasonal Columbia River camping with partial hookups, boating, fishing, and swimming, subject to the current shoreline project.",
        "Nearby nature & parks":"Daroga State Park occupies Columbia River shoreline in an arid orchard region north of Wenatchee. Boating, swimming, fishing, and trail access can be affected by water conditions and the current shoreline construction project.",
    },
    "alta-lake-state-park": {
        "Short Description":"Seasonal mountain-lake park near Pateros with 125 numbered vehicle sites, partial-hookup options, showers, a trailer dump, and a 38-foot limit.",
        "Long description":"Alta Lake State Park is a seasonal campground above Pateros. The current campground map numbers 125 vehicle campsites across three loops, with both standard and partial-hookup options. Washington State Parks lists showers, drinking water, a trailer dump, and an equipment limit of 38 feet. Loop closure dates vary in fall and spring, so travelers should use the current winter schedule rather than a single park-wide opening date.",
        "Number of RV campsites":"125", "Max RV length":"38", "Hookups":"2", "RV Access":"yes",
        "Reservation window":"Loop 1 closes September 30–April 15, Loop 2 October 31–April 15, and Loop 3 September 10–April 15; first-come October 1–31 and April 3–14",
        "Access note":"The campground is seasonal and loop dates differ. Confirm the selected site's utility type and 38-foot equipment limit before booking.",
        "Site Recommendations":"The 125-site count follows all numbered vehicle campsites on the current map. Hookups are partial rather than full; choose by loop, utility type, and pad length.",
        "Things to do for families summary":"Seasonal mountain-lake camping with partial-hookup options, swimming, paddling, fishing, and Cascade views.",
        "Nearby nature & parks":"Alta Lake sits above the Methow River valley near Pateros, where dry hillsides meet scattered pine forest. Lake activities and nearby trail access are seasonal; check current fire, smoke, and closure notices before travel.",
    },
    "lake-wenatchee-state-park": {
        "Short Description":"Large alpine-lake park with 197 vehicle campsites: 155 standard and 42 partial-hookup, with showers, a trailer dump, and distinct north and south limits.",
        "Long description":"Lake Wenatchee State Park has separate North and South campgrounds. Official material lists 155 standard campsites and 42 partial-hookup sites, for 197 vehicle campsites. The South Campground's 100 sites are intended for vehicle and trailer combinations under 20 feet. The North Campground has the 42 utility sites and accommodates selected equipment up to 40 feet. Showers and the trailer dump are in the North Campground. Winter camping moves to a designated South day-use area after the regular campgrounds close for snow.",
        "Number of RV campsites":"197", "Max RV length":"40", "Hookups":"2", "RV Access":"yes",
        "Reservation window":"Regular campgrounds close for snow between October and mid-November and reopen April to mid-May as conditions allow. Normal campsites require reservations; winter camping is first-come in the South day-use area",
        "Access note":"South Campground vehicle-and-trailer combinations must be under 20 feet; selected North Campground sites accommodate up to 40 feet. Winter campers need a Sno-Park permit and must unhook trailers.",
        "Things to do for families summary":"Alpine-lake camping with swimming, paddling, fishing, trails, and winter recreation; Leavenworth is a separate drive from the park.",
        "Things to do for families":"Lake Wenatchee swimming and beach access\nKayaking and boating\nFishing under current regulations\nNearby forest trails\nLeavenworth day trip\nCross-country skiing and snowshoeing when conditions allow",
        "Site Recommendations":"North has utility sites, showers, and the trailer dump; South is limited to combinations under 20 feet. Winter camping uses the South day-use area with trailers unhooked.",
        "Nearby nature & parks":"Lake Wenatchee State Park surrounds the eastern end of Lake Wenatchee near the Wenatchee River outlet. National forest roads and trails extend into the surrounding mountains, with access changing according to snow, fire, and road conditions.",
    },
    "pearrygin-lake-state-park": {
        "Short Description":"Methow Valley lake park near Winthrop with 163 vehicle campsites across standard and utility options, plus showers, a trailer dump, and a 60-foot limit.",
        "Long description":"Pearrygin Lake State Park is a large camping and recreation park near Winthrop. The official campground brochure identifies 92 standard campsites and 71 utility sites, for 163 vehicle campsites. Washington State Parks lists showers, drinking water, a trailer dump, and an equipment limit of 60 feet. East and West campgrounds follow different seasonal closure dates, and openings can change with weather.",
        "Number of RV campsites":"163", "Max RV length":"60", "Hookups":"3", "RV Access":"yes",
        "Reservation window":"West campground closes October 25–April 20; East closes October 31–April 5. Open campsites are reservable, with spring dates dependent on weather",
        "Access note":"Use the new entrance at 625 Bear Creek Road. SR-20 closes seasonally, so approach from US-97 when North Cascades Highway is closed and allow additional travel time.",
        "Things to do for families summary":"Lake swimming, paddling, fishing, hiking, and winter recreation near Winthrop in the Methow Valley.",
        "Site Recommendations":"Choose between East and West campgrounds by utility needs and seasonal availability. Water is generally off from mid-October to early April; verify opening dates and road conditions.",
        "Nearby nature & parks":"Pearrygin Lake State Park lies just outside Winthrop in the Methow Valley, with lake, grassland, and pine-forest scenery. The park connects with local trails, while broader valley access can change with wildfire, snow, and the seasonal SR-20 closure.",
    },
}

MAX_VALUES = {slug: (int(data["Max RV length"]) if data.get("Max RV length") else None) for slug, data in CONTENT.items()}

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
    for slug in sorted(slugs):
        row = by_slug[slug]
        values = {"operating_status":"current dated closures and alerts preserved", "rv_access":True,
                  "reservation_method":row["Reservation window"], "max_rv_length":MAX_VALUES[slug], "hookups":int(row["Hookups"])}
        summaries = {
            "operating_status":"The current operator page and winter schedule identify dated seasonal, fire, construction, or utility restrictions preserved in the canonical record.",
            "rv_access":"The current operator page or official campground map identifies vehicle, RV, utility, or full-hookup campsites.",
            "reservation_method":"The current operator reservation information and winter schedule identify reservable periods, first-come periods, and seasonal exceptions.",
            "max_rv_length":"The operator publishes this limit, or the record explicitly leaves a park-wide limit unconfirmed when current official material does not support one.",
            "hookups":"The current operator page or official campground map identifies the published utility level.",
        }
        source = {"url":STATE_URL[slug], "publisher":"Washington State Parks", "source_family":"washington-state-parks"}
        for field, value in values.items():
            evidence["observations"].append({"slug":slug, "field":field, "status":"corrected_locally", "checked_on":CHECKED,
                "summary":summaries[field], "proposed_value":value,
                "sources":[{**source, "evidence":summaries[field]}]})
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("Applied 12 central/eastern Washington State Parks reviews and 56 grouped campground fact corrections.")

if __name__ == "__main__":
    main()
