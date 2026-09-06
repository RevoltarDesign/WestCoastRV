#!/usr/bin/env python3
"""Resolve the campground/RV-park identity conflict in the Sol Duc record."""
import csv
from pathlib import Path


MASTER = Path(__file__).resolve().parent / "data" / "campgrounds.csv"


def main():
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    row = next(item for item in rows if item["Slug"] == "sol-duc-campground")
    row.update({
        "Name": "Sol Duc Campground",
        "Data last updated": "2026-09-06",
        "Short Description": "Olympic National Park resort campground with 82 standard sites plus a separate 17-site RV area offering water and electric hookups for rigs up to 36 feet.",
        "Long description": "Sol Duc Hot Springs RV Park and Campground share an old-growth setting along the Sol Duc River but offer different site types. The campground has 82 standard campsites, flush restrooms, and running water; many sites fit smaller RVs, with a few campground sites listed up to 35 feet. The separate 17-site RV area is a gravel, back-in lot with water and electric hookups and spaces from 20 to 36 feet. Both areas use the same Recreation.gov listing and provide direct access to the Sol Duc valley, hot spring pools, and the trail to Sol Duc Falls.",
        "Number of RV campsites": "17",
        "Max RV length": "36",
        "Maneuverability": "2",
        "Site surface type": "Mixed",
        "Hookups": "2",
        "Reservation window": "Reservable up to 6 months in advance",
        "Amenities summary": "The campground has flush restrooms and running water. The separate 17-site RV area has water and electric hookups; showers and hot spring pools require resort access.",
        "Site Recommendations": "Choose one of the 17 dedicated RV spaces when water and electric hookups are essential; Recreation.gov identifies 20-, 26-, and 36-foot RV site groups, all back-in. The separate 82-site campground is more wooded and private, but most RV-compatible pads are shorter and have no hookups. Confirm the equipment limit on the exact site before booking.",
        "RV Access": "yes",
        "Access note": "The dedicated RV area fits vehicles from 20 to 36 feet; campground sites usually fit 21 feet, with a few up to 35 feet.",
        "Access source": "https://www.nps.gov/olym/planyourvisit/camping.htm",
        "Access checked": "2026-09-06",
    })
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("Resolved the Sol Duc campground and RV-area record.")


if __name__ == "__main__":
    main()
