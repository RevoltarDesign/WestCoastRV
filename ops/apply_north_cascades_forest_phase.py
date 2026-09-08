#!/usr/bin/env python3
"""Apply sourced inventory, access, location, and route corrections for eight National Forest campgrounds."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "north-cascades-forest-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-07"

IDS = {
    "tinkham-campground": "232113", "kachess-campground": "232064",
    "verlot-campground": "232120", "gold-basin-campground": "232051",
    "turlo-campground": "232118", "bedal-campground": "233864",
    "horseshoe-cove-campground": "232059", "shannon-creek-campground": "232096",
}
URLS = {slug: f"https://www.recreation.gov/camping/campgrounds/{facility_id}" for slug, facility_id in IDS.items()}

COMMON = {
    "Hookups": "0", "RV Access": "yes", "Dump station on site": "false",
    "Amenities: Showers": "false", "Generator policy": "1",
}

CONTENT = {
    "tinkham-campground": {
        "Short Description": "South Fork Snoqualmie River campground with 42 public RV-capable sites, three tent-only sites, vault toilets, hand-pump water, and no hookups.",
        "Long description": "Tinkham Campground sits beside the South Fork Snoqualmie River one mile from I-90 Exit 42. The current Recreation.gov inventory contains 42 public standard sites that permit RVs and three tent-only sites; management records are excluded. Public RV dimensions vary by site, with selected sites publishing lengths up to 46 feet. The campground has vault toilets and hand-pump drinking water but no electrical hookups or dump station. Recreation.gov warns that the water's mineral content affects its color and taste and recommends bringing drinking water.",
        "Number of RV campsites": "42", "Max RV length": "46",
        "Reservation window": "Reservable through Recreation.gov during the operating season, generally up to six months ahead; confirm current site availability and opening dates",
        "Access note": "Use I-90 Exit 42 and Tinkham Road. The final road is gravel and conditions vary with weather, heavy use, and maintenance. Recreation.gov reports that Apple Maps incorrectly labels the road closed.",
        "Things to do for families": "Tinkham Discovery Trail\nSouth Fork Snoqualmie River access\nFishing under current regulations\nNearby forest hiking\nPicnicking\nI-90 corridor day trips",
        "Things to do for families summary": "A close-to-Seattle river campground with a short discovery trail, fishing, hiking, and dry RV camping.",
        "Nearby nature & parks": "The campground lies in the forested South Fork Snoqualmie valley west of Snoqualmie Pass. Nearby trails and river access change with snow, flooding, and seasonal maintenance.",
        "Site Recommendations": "The 42-site RV count excludes three tent-only sites and management inventory. Published equipment limits vary by site from roughly 20 to 46 feet; select the exact site for your combined equipment length.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "false", "Beach & Tide Pools": "false", "Boating": "false", "Playground": "false",
    },
    "kachess-campground": {
        "Short Description": "Large Kachess Lake campground with 150 tent-and-RV sites, drinking water, boat launches, a swimming area, no hookups, and a current seasonal fire closure.",
        "Long description": "Kachess Campground sits on the northwest shore of Kachess Lake. Recreation.gov publishes 150 tent-and-RV sites including one group site; 106 single-family sites and the group site are reservable, with the remainder normally first-come. Drinking water, vault toilets, motorized and non-motorized launches, a swimming area, and picnic areas are available, but campsite hookups and a dump station are not. The current inventory publishes site-specific equipment lengths, with limited sites up to 110 feet.",
        "Number of RV campsites": "150", "Max RV length": "110",
        "Reservation window": "Normally a mix of Recreation.gov reservations and first-come sites during the operating season; the campground is currently closed for the 2026 season under the Three Queens Fire order",
        "Access note": "As checked September 7, 2026, Recreation.gov lists Kachess closed for the season under the Three Queens Fire closure, Forest Service Order 06-17-03-2026-32. The boat launch closed August 1, 2026 because of low lake levels.",
        "Things to do for families": "Kachess Lake swimming area\nMotorized and non-motorized boating\nPaddling\nFishing under current regulations\nKachess Lake Trail\nPicnicking and mountain biking",
        "Things to do for families summary": "Large lakeside campground with swimming, boating, paddling, fishing, and trail access when seasonal conditions permit.",
        "Nearby nature & parks": "Kachess Lake is a reservoir in the Okanogan-Wenatchee National Forest. Lake levels vary through summer, affecting launches and shoreline access; current forest orders take priority.",
        "Site Recommendations": "The operator publishes 150 sites, including one group site. Equipment limits are site-specific and only selected inventory supports very long combinations; confirm the selected pad rather than treating 110 feet as a campground-wide fit.",
        "Hiking": "true", "Fishing": "true", "Swimming": "true", "Kayaking/Paddling": "true", "Beach & Tide Pools": "true", "Boating": "true", "Playground": "false",
    },
    "verlot-campground": {
        "Short Description": "Mountain Loop campground with 19 public RV-capable sites, three tent-only sites, one camper-van/pop-up site, flush toilets, drinking water, and no hookups.",
        "Long description": "Verlot Campground is beside the South Fork Stillaguamish River on the Mountain Loop Highway. The current Recreation.gov inventory contains 19 public sites that permit RV or trailer equipment, three tent-only sites, and one site limited to camper vans, pickup campers, or pop-ups; three management records are excluded. Flush toilets and drinking water are available, which is unusual for this corridor, but there are no electrical hookups, showers, or dump station. The operator does not publish usable RV lengths for the public sites, so the listing does not claim a park-wide maximum.",
        "Number of RV campsites": "19", "Max RV length": "",
        "Reservation window": "Reservable through Recreation.gov during the operating season, generally up to six months ahead; confirm current site availability and opening dates",
        "Access note": "The campground is about 10.8 miles east of Granite Falls on the Mountain Loop Highway. Confirm road, fire, and seasonal conditions before travel.",
        "Things to do for families": "South Fork Stillaguamish River access\nFishing under current regulations\nMountain Loop scenic drive\nNearby forest hikes\nVerlot Public Service Center\nPicnicking",
        "Things to do for families summary": "Riverside dry camping with flush toilets, drinking water, fishing, nearby hiking, and Mountain Loop access.",
        "Nearby nature & parks": "Verlot lies in the South Fork Stillaguamish valley near the Forest Service's historic Verlot Public Service Center. Trail and highway access can change after storms, fires, and seasonal closures.",
        "Site Recommendations": "The 19-site RV count excludes three tent-only sites, one camper-van/pop-up site, and three management records. Recreation.gov permits RV equipment on the 19 sites but publishes zero-length placeholders, so verify the exact pad before bringing a larger rig.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "false", "Beach & Tide Pools": "false", "Boating": "false", "Playground": "false",
    },
    "gold-basin-campground": {
        "Short Description": "Mountain Loop campground with 37 public RV-capable sites, one tent-only site, vault toilets, no water or hookups, and an accessible mill-pond trail across the highway.",
        "Long description": "Gold Basin Campground sits near the South Fork Stillaguamish River. Current federal descriptions conflict, citing both 39 and 29 primitive campsites. The live Recreation.gov inventory resolves the RV question more precisely: 37 public standard sites permit RVs, one additional public site is tent-only, and three management records are excluded. Public site-specific limits reach 45 feet. The campground has vault toilets but no potable water, hookups, showers, or dump station.",
        "Number of RV campsites": "37", "Max RV length": "45",
        "Reservation window": "Reservable through Recreation.gov during the operating season, generally up to six months ahead; confirm current availability because older Forest Service material still shows a closure",
        "Access note": "Directions use the named Gold Basin Campground entrance on NF-4018. The Recreation.gov facility coordinate resolves across Mountain Loop Highway at Gold Basin Mill Pond, so it is not used for the map pin.",
        "Things to do for families": "Gold Basin Mill Pond accessible trail\nSouth Fork Stillaguamish River access\nFishing under current regulations\nNearby forest hikes\nOpen field recreation\nMountain Loop scenic drive",
        "Things to do for families summary": "Dry forest camping with river access, hiking, fishing, an open recreation field, and an accessible interpretive trail across the highway.",
        "Nearby nature & parks": "Gold Basin is in the South Fork Stillaguamish corridor. Gold Basin Mill Pond and its accessible interpretive trail are across the highway from the campground, not inside the camping loops.",
        "Site Recommendations": "The 37-site RV count comes from current public standard inventory and excludes one tent-only and three management records. Site-specific RV limits range from 22 to 45 feet; bring all drinking water.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "false", "Beach & Tide Pools": "false", "Boating": "false", "Playground": "false",
    },
    "turlo-campground": {
        "Short Description": "Small Mountain Loop campground with 18 standard tent-and-RV sites, drinking water, South Fork Stillaguamish access, and no hookups.",
        "Long description": "Turlo Campground has 18 standard sites beside the South Fork Stillaguamish River. Recreation.gov identifies all 18 as accommodating tent and RV camping and lists drinking water, picnic tables, and river access. There are no electrical hookups, showers, or dump station. Public inventory permits RVs but contains zero-length placeholders, so the listing does not claim a campground-wide maximum.",
        "Number of RV campsites": "18", "Max RV length": "",
        "Reservation window": "Reservable through Recreation.gov during the operating season, generally up to six months ahead; confirm current site availability and opening dates",
        "Access note": "The campground is just off Mountain Loop Highway east of Granite Falls. Confirm highway, fire, and seasonal conditions before travel.",
        "Things to do for families": "South Fork Stillaguamish River access\nFishing under current regulations\nNearby forest hikes\nMountain Loop scenic drive\nPicnicking\nForest and wildlife observation",
        "Things to do for families summary": "Small riverside campground with drinking water, fishing, forest recreation, and no campsite utilities.",
        "Nearby nature & parks": "Turlo lies in the forested South Fork Stillaguamish valley. Mountain Loop Highway and nearby trails are subject to seasonal, storm, and fire-related changes.",
        "Site Recommendations": "All 18 public inventory records permit RV equipment, but Recreation.gov does not publish usable RV length values. Confirm the selected pad and road conditions before bringing a larger trailer.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "false", "Beach & Tide Pools": "false", "Boating": "false", "Playground": "false",
    },
    "bedal-campground": {
        "Short Description": "Primitive Sauk River campground with 22 standard sites, vault toilets, a whitewater boat ramp, no water or hookups, and a gravel approach from Darrington.",
        "Long description": "Bedal Campground is a primitive campground beside the Sauk River. Recreation.gov publishes 22 standard sites with vault toilets, food-storage lockers, fire rings, and a boat ramp for whitewater paddlers. There is no potable water, electrical service, shower, or dump station. Current public inventory publishes site-specific RV lengths up to 58 feet, but many sites are much shorter and trailer fields are often unreported.",
        "Number of RV campsites": "22", "Max RV length": "58",
        "Reservation window": "Reservable through Recreation.gov during the operating season, generally up to six months ahead; confirm current site availability and opening dates",
        "Access note": "Approach from Darrington on WA-530 and Mountain Loop Highway. Recreation.gov says the final 7.5 miles are gravel and variable and recommends this direction because the Barlow Pass section may be gated.",
        "Things to do for families": "Sauk River access\nWhitewater paddling launch\nFishing under current regulations\nNorth Fork Sauk Falls area\nNearby forest hiking\nMountain Loop scenic drive",
        "Things to do for families summary": "Primitive Sauk River camping with whitewater access, fishing, nearby waterfalls, and no potable water.",
        "Nearby nature & parks": "Bedal sits on the eastern Mountain Loop Highway near Sauk River recreation and forest trails. The access road and nearby trails change with weather, washouts, snow, and fire conditions.",
        "Site Recommendations": "The operator publishes 22 standard sites. Site 1 lists the 58-foot maximum, while many inventory records are under 35 feet; confirm the selected site's RV and trailer fields and bring all drinking water.",
        "Hiking": "true", "Fishing": "true", "Swimming": "false", "Kayaking/Paddling": "true", "Beach & Tide Pools": "false", "Boating": "false", "Playground": "false",
    },
    "horseshoe-cove-campground": {
        "Short Description": "Baker Lake campground with 39 campsites including three group sites, a sandy swimming beach, boat ramp, forested shoreline, and no hookups.",
        "Long description": "Horseshoe Cove Campground is on the west shore of Baker Lake. Recreation.gov and Forest Service material publish 39 campsites including three group sites, with standard tent-and-trailer camping, a sandy swimming beach, a boat ramp, and trail access. Campsites have no utility hookups, showers, or dump station. Current public individual-site inventory does not publish usable RV lengths; the 40-foot values belong to group and management records, so no park-wide maximum is claimed.",
        "Number of RV campsites": "39", "Max RV length": "",
        "Reservation window": "Twenty-five campsites are normally reservable through Recreation.gov and remaining sites are first-come during the operating season; confirm current opening dates and availability",
        "Access note": "Follow SR-20 to Baker Lake Road, then NF-1118 past Bayview Campground. Confirm seasonal road, campground, lake, and fire conditions before travel.",
        "Things to do for families": "Baker Lake swimming beach\nBoating and paddling\nFishing under current regulations\nBaker Lake shoreline access\nNearby family-friendly trails\nPicnicking",
        "Things to do for families summary": "Baker Lake camping with a sandy swim beach, boat ramp, paddling, fishing, and nearby trails.",
        "Nearby nature & parks": "The campground sits on Baker Lake below Mount Baker and North Cascades trail systems. Lake levels, fire restrictions, and seasonal road operations affect access and recreation.",
        "Site Recommendations": "The 39-site published total includes three group sites. Public individual-site RV length values are not supplied, so verify the selected site rather than relying on the group-site 40-foot field.",
        "Hiking": "true", "Fishing": "true", "Swimming": "true", "Kayaking/Paddling": "true", "Beach & Tide Pools": "true", "Boating": "true", "Playground": "false",
    },
    "shannon-creek-campground": {
        "Short Description": "North Baker Lake campground with 14 public RV-capable sites, four tent-only booking units, drinking water, vault toilets, and no hookups.",
        "Long description": "Shannon Creek Campground sits near the north end of Baker Lake. The live Recreation.gov inventory contains 14 public standard sites that permit RVs and four tent-only booking units; two management records are excluded. Public RV-capable sites publish lengths up to 36 feet. The campground has drinking water, vault toilets, picnic tables, and fire rings but no electrical hookups, showers, or dump station. The current Forest Service recreation listing shows the campground seasonally closed, so visitors should use live availability before travel.",
        "Number of RV campsites": "14", "Max RV length": "36",
        "Reservation window": "Reservable through Recreation.gov during the operating season, generally up to six months ahead; currently shown seasonally closed by the Forest Service",
        "Access note": "The campground is approximately 23.3 miles up Baker Lake Road from SR-20. Confirm the seasonal opening, road, fire, and lake conditions before travel.",
        "Things to do for families": "Baker Lake paddling and boating\nSwimming\nFishing under current regulations\nBaker Lake Trail\nBaker River Trail\nOld-growth forest walks",
        "Things to do for families summary": "North Baker Lake camping with paddling, swimming, fishing, and access to family-friendly forest trails.",
        "Nearby nature & parks": "Shannon Creek is near Baker Lake, the Baker River Trail, and North Cascades National Park access. Seasonal closures, snow, fire restrictions, and lake conditions affect recreation.",
        "Site Recommendations": "The 14-site RV count excludes four tent-only booking units and two management records. Public RV-capable sites range from 22 to 36 feet in the current inventory.",
        "Hiking": "true", "Fishing": "true", "Swimming": "true", "Kayaking/Paddling": "true", "Beach & Tide Pools": "false", "Boating": "true", "Playground": "false",
    },
}

MAX_VALUES = {slug: (int(data["Max RV length"]) if data["Max RV length"] else None) for slug, data in CONTENT.items()}

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
        lat_text, lon_text = f"{lat:.7f}", f"{lon:.7f}"
        row.update(COMMON); row.update(CONTENT[slug])
        row.update({
            "Data last updated": CHECKED, "Address": item["address"], "Latitude": lat_text, "Longitude": lon_text,
            "Google Maps Link": f"https://www.google.com/maps?q={lat_text},{lon_text}", "Coordinates source": item["coordinate_source"],
            "Coordinates checked": CHECKED, "Coordinate precision": item["precision"], "Time from Seattle": duration(display),
            "Drive Time Minutes": str(display), "Drive Time Band": band(display), "Drive distance miles": str(item["distance_miles"]),
            "Drive route minutes": str(item["observed_route_minutes"]), "Drive time origin": "Seattle, Washington",
            "Drive time source": route_url(lat_text, lon_text), "Drive time checked": CHECKED, "Drive time note": item["route_note"],
            "Access source": URLS[slug], "Access checked": CHECKED,
        })
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    slugs = set(CONTENT); critical = {"operating_status", "rv_access", "reservation_method", "max_rv_length", "hookups"}
    evidence["observations"] = [o for o in evidence["observations"] if not (o.get("slug") in slugs and o.get("field") in critical)]
    summaries = {
        "operating_status": "The live Recreation.gov facility page and current notices identify seasonal availability, closures, and access alerts preserved in the canonical record.",
        "rv_access": "The live Recreation.gov campsite inventory identifies public sites that permit RV or trailer equipment; management records and tent-only sites are excluded from the RV count.",
        "reservation_method": "The operator page identifies Recreation.gov reservations and published first-come exceptions where available.",
        "max_rv_length": "The maximum is the largest positive RV or trailer length in current public campsite inventory; the canonical value is intentionally blank where only zero placeholders or non-public records provide lengths.",
        "hookups": "The current operator facility description states that electrical hookups are unavailable.",
    }
    for slug in sorted(slugs):
        row = by_slug[slug]; facility_id = IDS[slug]
        sources = {
            "operating_status": URLS[slug], "reservation_method": URLS[slug], "hookups": URLS[slug],
            "rv_access": f"https://www.recreation.gov/api/camps/campgrounds/{facility_id}/campsites",
            "max_rv_length": f"https://www.recreation.gov/api/camps/campgrounds/{facility_id}/campsites",
        }
        values = {"operating_status": row["Access note"], "rv_access": True,
                  "reservation_method": row["Reservation window"], "max_rv_length": MAX_VALUES[slug], "hookups": 0}
        for field, value in values.items():
            evidence["observations"].append({"slug": slug, "field": field, "status": "corrected_locally", "checked_on": CHECKED,
                "summary": summaries[field], "proposed_value": value,
                "sources": [{"url": sources[field], "publisher": "Recreation.gov / U.S. Forest Service", "source_family": "recreation-gov", "evidence": summaries[field]}]})
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("Applied eight National Forest reviews and 51 grouped campground fact corrections.")

if __name__ == "__main__":
    main()
