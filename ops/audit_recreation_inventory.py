#!/usr/bin/env python3
"""Audit public RV campsite inventory and published lengths from Recreation.gov."""
import argparse
import csv
import json
import re
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATASET = HERE / "data" / "campgrounds.csv"

def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "WA-RV-Camping-inventory-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", action="append", default=[])
    args = parser.parse_args()
    with DATASET.open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))
    selected = set(args.slug)
    records = []
    for row in rows:
        match = re.search(r"recreation\.gov/camping/campgrounds/(\d+)", row["Reservation website"])
        if not match or (selected and row["Slug"] not in selected):
            continue
        facility_id = match.group(1)
        root = f"https://www.recreation.gov/api/camps/campgrounds/{facility_id}"
        facility = fetch(root)["campground"]
        campsites = fetch(root + "/campsites")["campsites"]
        active = [site for site in campsites if not site.get("is_deactivated", False)]
        public = [site for site in active if "MANAGEMENT" not in (site.get("campsite_type") or "")]
        rv_sites, lengths = [], []
        for site in public:
            equipment = [item for item in (site.get("permitted_equipment") or [])
                         if not item.get("is_deactivated") and item.get("equipment_name") in {"RV", "Trailer"}]
            if equipment:
                rv_sites.append(site["campsite_name"])
                lengths.extend(item.get("max_length") for item in equipment if (item.get("max_length") or 0) > 0)
        records.append({
            "slug": row["Slug"], "facility_id": facility_id, "facility_name": facility["facility_name"],
            "checked_on": date.today().isoformat(), "source": root + "/campsites",
            "active_inventory_records": len(active), "public_inventory_records": len(public),
            "public_rv_capable_records": len(set(rv_sites)), "public_non_rv_records": len(public) - len(set(rv_sites)),
            "largest_published_public_rv_length": max(lengths) if lengths else None,
            "rv_records_without_published_length": sum(1 for site in public if any(
                item.get("equipment_name") in {"RV", "Trailer"} and not item.get("max_length")
                for item in (site.get("permitted_equipment") or []))),
            "canonical_rv_sites": int(row["Number of RV campsites"]) if row["Number of RV campsites"] else None,
            "canonical_max_rv_length": int(row["Max RV length"]) if row["Max RV length"] else None,
        })
    report = {"checked_on": date.today().isoformat(), "records_checked": len(records), "records": records}
    (HERE / "recreation-inventory-audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
