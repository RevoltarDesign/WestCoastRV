#!/usr/bin/env python3
"""Apply reviewed official Recreation.gov coordinates from the latest audit snapshot."""
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
AUDIT = HERE / "recreation-gov-audit.json"
FIELDS = ["Latitude", "Longitude", "Coordinates source", "Coordinates checked", "Coordinate precision"]


def main():
    report = json.loads(AUDIT.read_text(encoding="utf-8"))
    if report.get("identity_errors"):
        raise SystemExit("Refusing coordinate update while facility identity errors remain")
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    for field in FIELDS:
        if field not in fields:
            fields.append(field)
    by_slug = {row["Slug"]: row for row in rows}
    changed = 0
    skipped = []
    for item in report["results"]:
        latitude, longitude = item.get("official_latitude"), item.get("official_longitude")
        drift = item.get("coordinate_drift_miles")
        valid_wa = latitude is not None and longitude is not None and 45.5 <= latitude <= 49.1 and -125 <= longitude <= -116.8
        if not item.get("ok") or not valid_wa or drift is None or drift > 2:
            skipped.append({"slug": item["slug"], "reason": "manual coordinate review required", "drift_miles": drift})
            continue
        row = by_slug[item["slug"]]
        new = {
            "Latitude": f"{latitude:.6f}",
            "Longitude": f"{longitude:.6f}",
            "Coordinates source": item["source"],
            "Coordinates checked": report["checked_on"],
            "Coordinate precision": "official facility point; confirm entrance routing",
            "Google Maps Link": f"https://www.google.com/maps?q={latitude:.6f},{longitude:.6f}",
        }
        if any(row.get(key, "") != value for key, value in new.items()):
            changed += 1
        row.update(new)
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Applied official facility coordinates to {changed} Recreation.gov-backed records.")
    print(f"Skipped {len(skipped)} records for manual review.")
    for item in skipped:
        print(f"  {item['slug']}: {item['reason']} (drift={item['drift_miles']})")


if __name__ == "__main__":
    main()
