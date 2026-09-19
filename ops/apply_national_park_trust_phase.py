#!/usr/bin/env python3
"""Apply the 2026-09-19 Mount Rainier and North Cascades trust review."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-19"

MORA_CAMPS = "https://www.nps.gov/mora/planyourvisit/campgrounds.htm"
MORA_FAQ = "https://www.nps.gov/mora/planyourvisit/park-construction-faqs.htm"
COUGAR = "https://www.recreation.gov/camping/campgrounds/232466"
NOCA_CAMPS = "https://www.nps.gov/noca/planyourvisit/camping.htm"
NOCA_NEWHALEM = "https://www.nps.gov/noca/planyourvisit/newhalem-creek-campground.htm"
NOCA_GOODELL = "https://www.nps.gov/noca/planyourvisit/goodell-creek-campground.htm"
NOCA_NORTH = "https://www.nps.gov/noca/planyourvisit/colonial-creek-north-campground.htm"
NOCA_SOUTH = "https://www.nps.gov/noca/planyourvisit/colonial-creek-south-campground.htm"

UPDATES = {
    "cougar-rock-campground": {
        "Data last updated": CHECKED,
        "Short Description": "Open Mount Rainier campground near Paradise with 173 individual sites, no hookups, RVs up to 35 feet, and a current campfire ban.",
        "Long description": "Cougar Rock is open on Mount Rainier's southwest side near Longmire and Paradise. Recreation.gov lists 173 individual campsites with drinking water, flush toilets, and picnic tables. Individual sites have no electric, water, or sewer hookups. Motorhomes over 35 feet and trailers over 27 feet may not enter because loop-road turns are tight. The RV dump and fill station is closed for the 2026 season, and a current campfire ban prohibits wood and charcoal fires; check current NPS conditions immediately before travel.",
        "Reservation window": "Open for the 2026 season; reserve on Recreation.gov, with limited first-come sites also available",
        "Number of RV campsites": "173", "Max RV length": "35", "Hookups": "0",
        "Dump station on site": "false", "Amenities: Fire pits": "false", "RV Access": "yes",
        "Amenities summary": "Flush toilets and drinking water are available. There are no hookups or showers, the RV dump and fill station is closed for 2026, and the current campfire ban prohibits wood and charcoal fires.",
        "Site Recommendations": "Select the exact driveway for your combined equipment length; motorhomes over 35 feet and trailers over 27 feet may not enter. Arrive without relying on a dump or water-fill station, and bring a fuel stove because wood and charcoal fires are currently prohibited. Reserve through Recreation.gov or use only an officially designated first-come site.",
        "Access note": "Open for the 2026 season. Motorhomes are limited to 35 feet and trailers to 27 feet because of tight loop-road turns. The dump and fill station is closed, and a campfire ban is in effect.",
        "Access source": MORA_CAMPS, "Access checked": CHECKED,
    },
    "ohanapecosh-campground": {
        "Data last updated": CHECKED, "Access checked": CHECKED,
    },
    "white-river-campground": {
        "Data last updated": CHECKED, "Access checked": CHECKED,
    },
    "newhalem-creek-campground": {
        "Data last updated": CHECKED,
        "Short Description": "Partially open North Cascades campground with Loops A and B first-come through September 27; many RV sites fit equipment up to 50 feet.",
        "Long description": "Newhalem Creek has 107 total campsites, including tent-only, walk-in, group, and drive-in inventory. NPS says many RV and trailer sites accept equipment up to 50 feet and that there are no hookups. Loop C closed September 14, 2026; Loops A and B remain first-come through September 27. Drinking water, trash service, flush toilets, and the dump station are seasonal. Check the current NPS camping page and SR 20 conditions before travel.",
        "Number of RV campsites": "", "Max RV length": "50", "Hookups": "0", "RV Access": "yes",
        "Reservation window": "Loops A and B are first-come through September 27, 2026; Loop C is closed for the season",
        "Amenities summary": "Loops A and B retain seasonal drinking water, trash, flush toilets, and dump-station service while open. There are no showers or hookups. Confirm service status before arrival.",
        "Site Recommendations": "Loop C is closed for the season. For travel through September 27, use only an available first-come site in Loops A or B and confirm the exact parking spur for your equipment; NPS lists a campground maximum of 50 feet but site sizes vary.",
        "Access note": "Loops A and B remain open first-come through September 27, 2026; Loop C is closed. Many RV and trailer sites fit equipment up to 50 feet. Water, trash, flush toilets, and the dump station are seasonal.",
        "Access source": NOCA_CAMPS, "Access checked": CHECKED,
    },
    "goodell-creek-campground": {
        "Data last updated": CHECKED,
        "Short Description": "Year-round Skagit River campground with 19 total sites; some sites fit small RVs and trailers up to 20 feet, with primitive off-season service.",
        "Long description": "Goodell Creek is a 19-site campground on the Skagit River. NPS says tents and small RVs are suitable, with a 20-foot maximum for RVs and trailers and no hookups or dump station. The campground remains open year-round; after seasonal service ends it is first-come, free, and primitive, with vault toilets but no potable water or trash service. Check SR 20 conditions before traveling.",
        "Number of RV campsites": "", "Max RV length": "20", "Hookups": "0", "RV Access": "yes",
        "Amenities: Drinking water": "false",
        "Amenities summary": "Vault toilets remain available year-round. Potable water and trash service are unavailable outside the seasonal operating period; there are no showers, hookups, or dump station.",
        "Site Recommendations": "Use only a site that fits your complete rig; NPS limits both RVs and trailers to 20 feet and says only some sites accommodate them. Bring drinking water, pack out trash, and expect first-come primitive service outside the summer reservation season.",
        "Access note": "Open year-round. Only some sites fit small RVs or trailers, with a current 20-foot maximum. Off-season camping is first-come and primitive, with vault toilets but no potable water or trash service.",
        "Access source": NOCA_GOODELL, "Access checked": CHECKED,
    },
    "colonial-creek-south-campground": {
        "Data last updated": CHECKED,
        "Short Description": "Vehicle campground closed for the 2026 season; ten walk-in, tent-only sites remain available first-come without normal seasonal services.",
        "Long description": "Colonial Creek South's vehicle campground closed for the season on September 14, 2026. Ten walk-in, tent-only sites numbered 64 through 73 remain available first-come outside the operational season, but they do not provide RV access. During its operating season the developed campground has no electric hookups, is not large-RV friendly, and lists a 36-foot RV and trailer maximum. Check the current NPS camping page and SR 20 conditions before planning a future stay.",
        "Reservation window": "Campground closed to vehicles for the 2026 season; ten walk-in tent-only sites remain first-come",
        "Reservation website": NOCA_CAMPS, "Number of RV campsites": "", "Max RV length": "36",
        "Hookups": "0", "Dump station on site": "false", "RV Access": "no",
        "Amenities: Toilets": "", "Amenities: Fire pits": "",
        "Amenities: Drinking water": "false",
        "Amenities summary": "The vehicle campground and its seasonal services are closed. Ten walk-in tent-only sites remain without normal water or trash service; no RV overnight access is available.",
        "Site Recommendations": "Do not plan an RV stay after the September 14 seasonal closure. The ten sites that remain are walk-in and tent-only. Recheck the NPS camping page for the 2027 vehicle-campground opening before routing a rig here.",
        "Access note": "Vehicle camping closed September 14, 2026. The ten sites remaining outside the operational season are walk-in and tent-only; do not route an RV to the campground for an overnight stay.",
        "Access source": NOCA_CAMPS, "Access checked": CHECKED,
    },
    "colonial-creek-north-campground": {
        "Data last updated": CHECKED,
        "Short Description": "Closed for the 2026 season; when operating, this no-hookup Diablo Lake campground accepts RVs and trailers up to 25 feet.",
        "Long description": "Colonial Creek North closed for the season on September 14, 2026. During its operating season it has no electric hookups, is not large-RV friendly, and lists a 25-foot maximum for both RVs and trailers. Reservations are used during peak season before the campground switches to first-come availability. Check the current NPS camping page and SR 20 conditions before planning a future stay.",
        "Reservation window": "Campground closed for the 2026 season; seasonal reservations return when the campground reopens",
        "Reservation website": NOCA_CAMPS, "Max RV length": "25", "Hookups": "0", "RV Access": "no",
        "Amenities: Toilets": "", "Amenities: Fire pits": "",
        "Amenities: Drinking water": "false",
        "Amenities summary": "The campground and its seasonal water, trash, and restroom services are closed. No RV overnight access is available until the next operating season.",
        "Site Recommendations": "Do not plan an overnight stay during the seasonal closure. When NPS reopens the campground, select the exact site for your equipment and keep both RVs and trailers at or below the published 25-foot maximum.",
        "Access note": "The campground closed for the season September 14, 2026. Do not route an RV here for an overnight stay until NPS posts the next seasonal opening.",
        "Access source": NOCA_CAMPS, "Access checked": CHECKED,
    },
}

FACTS = {
    "cougar-rock-campground": {
        "operating_status": ("open for the 2026 season", MORA_CAMPS, "NPS lists Cougar Rock as open."),
        "rv_access": (True, COUGAR, "Recreation.gov permits one RV and tow vehicle per individual site when both fit."),
        "reservation_method": ("Recreation.gov reservations plus limited first-come sites", MORA_CAMPS, "NPS lists Recreation.gov reservations and first-come availability."),
        "max_rv_length": (35, COUGAR, "Motorhomes over 35 feet and trailers over 27 feet may not enter."),
        "hookups": (0, COUGAR, "Individual sites have no electric, water, or sewer hookups."),
    },
    "ohanapecosh-campground": {
        "operating_status": ("closed for all of 2026", MORA_FAQ, "The developed area has no camping or visitor access during 2026 construction."),
        "rv_access": (False, MORA_FAQ, "No vehicle, camping, or day-use access is available in 2026."),
        "reservation_method": ("closed for 2026; 2027 reservations expected in December 2026", MORA_FAQ, "NPS expects 2027 reservations to reopen on Recreation.gov in December 2026."),
        "max_rv_length": ("32 feet when open; no access in 2026", MORA_CAMPS, "NPS lists a usual 32-foot RV maximum and confirms the 2026 closure."),
        "hookups": (0, MORA_CAMPS, "NPS states that its developed campgrounds have no utility hookups."),
    },
    "white-river-campground": {
        "operating_status": ("open until early October 2026, weather permitting", MORA_CAMPS, "NPS lists White River as open with an exact closing date still to be determined."),
        "rv_access": (True, MORA_CAMPS, "NPS lists RV access with a 27-foot maximum."),
        "reservation_method": ("first-come only; Scan and Pay after selecting a site", MORA_CAMPS, "NPS describes first-come-only payment through the Recreation.gov app or cashless kiosk."),
        "max_rv_length": (27, MORA_CAMPS, "NPS lists 27 feet for RVs and 18 feet for trailers."),
        "hookups": (0, MORA_CAMPS, "NPS states that its developed campgrounds have no utility hookups."),
    },
    "newhalem-creek-campground": {
        "operating_status": ("Loops A and B open through September 27; Loop C closed", NOCA_CAMPS, "The current seasonal notice gives the 2026 loop closure dates."),
        "rv_access": (True, NOCA_NEWHALEM, "NPS says many RV and trailer sites are available."),
        "reservation_method": ("first-come after September 7 until seasonal closure", NOCA_CAMPS, "NPS states reservations are not required after September 7, 2026."),
        "max_rv_length": (50, NOCA_NEWHALEM, "NPS lists a 50-foot maximum for RVs and trailers."),
        "hookups": (0, NOCA_NEWHALEM, "The NPS facility record lists zero electric hookups and explicitly says there are no hookups."),
    },
    "goodell-creek-campground": {
        "operating_status": ("open year-round with primitive off-season service", NOCA_GOODELL, "NPS lists year-round operation with vault toilets and no off-season water or trash service."),
        "rv_access": (True, NOCA_GOODELL, "NPS says small RVs and trailers fit in some sites."),
        "reservation_method": ("reservations in peak season; first-come outside it", NOCA_GOODELL, "NPS lists peak-season reservations and first-come winter camping."),
        "max_rv_length": (20, NOCA_GOODELL, "NPS lists a 20-foot maximum for both RVs and trailers."),
        "hookups": (0, NOCA_GOODELL, "The NPS facility record lists zero electric hookups and no dump station."),
    },
    "colonial-creek-south-campground": {
        "operating_status": ("vehicle campground closed; ten walk-in tent sites remain", NOCA_CAMPS, "NPS closed the vehicle campground September 14, 2026 and retains ten tent-only sites."),
        "rv_access": (False, NOCA_CAMPS, "Only walk-in tent-only sites remain outside the operating season."),
        "reservation_method": ("seasonal reservations; current remaining sites are first-come", NOCA_CAMPS, "NPS uses reservations in season and first-come access only for the remaining tent sites."),
        "max_rv_length": (36, NOCA_SOUTH, "NPS lists a 36-foot operating-season maximum for RVs and trailers."),
        "hookups": (0, NOCA_SOUTH, "The NPS facility record lists zero electric hookups."),
    },
    "colonial-creek-north-campground": {
        "operating_status": ("closed for the season September 14, 2026", NOCA_CAMPS, "The current NPS seasonal notice lists the closure date."),
        "rv_access": (False, NOCA_CAMPS, "The vehicle campground is closed for the season."),
        "reservation_method": ("seasonal Recreation.gov reservations", NOCA_NORTH, "NPS requires reservations during peak season before the annual closure."),
        "max_rv_length": (25, NOCA_NORTH, "NPS lists a 25-foot maximum for RVs and trailers."),
        "hookups": (0, NOCA_NORTH, "The NPS facility record lists zero electric hookups."),
    },
}


def main():
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields, rows = list(reader.fieldnames or []), list(reader)
    by_slug = {row["Slug"]: row for row in rows}
    changed = 0
    for slug, updates in UPDATES.items():
        for field, value in updates.items():
            if by_slug[slug].get(field, "") != str(value):
                by_slug[slug][field] = str(value)
                changed += 1
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)

    ledger = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    reviewed = set(FACTS)
    critical = {"operating_status", "rv_access", "reservation_method", "max_rv_length", "hookups"}
    ledger["observations"] = [o for o in ledger["observations"] if not (o.get("slug") in reviewed and o.get("field") in critical)]
    for slug, facts in FACTS.items():
        for field, (value, url, evidence) in facts.items():
            ledger["observations"].append({
                "slug": slug, "field": field, "status": "corrected_locally", "checked_on": CHECKED,
                "summary": evidence, "proposed_value": value,
                "sources": [{"url": url, "publisher": "National Park Service" if "nps.gov" in url else "Recreation.gov",
                             "source_family": "federal-operator", "evidence": evidence}],
            })
    EVIDENCE.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(f"Applied seven national-park trust reviews; changed {changed} canonical fields and refreshed 35 critical observations.")


if __name__ == "__main__":
    main()
