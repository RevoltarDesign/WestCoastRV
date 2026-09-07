#!/usr/bin/env python3
"""Compare every Recreation.gov booking link with its live facility identity.

This networked audit is intentionally separate from the offline build. Run it during
scheduled content reviews and save the JSON output as review evidence.
"""
import csv
import difflib
import json
import re
import urllib.request
from datetime import date
from math import asin, cos, radians, sin, sqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATASET = HERE / "data" / "campgrounds.csv"
RESOLUTIONS = HERE / "coordinate-resolutions.json"
ALIASES = {
    "hoh-campground": "Hoh Rainforest Campground",
    "sol-duc-campground": "Sol Duc Hot Springs Resort Campground",
}


def normalized(value):
    return re.sub(r"[^a-z0-9]", "", value.lower().replace("campground", ""))


def legacy_coordinates(url):
    match = re.search(r"(?:q=|query=)(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", url or "")
    return (float(match.group(1)), float(match.group(2))) if match else (None, None)


def distance_miles(a, b):
    lat1, lon1, lat2, lon2 = map(radians, (*a, *b))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    value = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 3959 * 2 * asin(sqrt(value))


def main():
    with DATASET.open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))
    resolutions = {}
    if RESOLUTIONS.exists():
        resolutions = {item["slug"]: item for item in json.loads(RESOLUTIONS.read_text(encoding="utf-8"))["resolutions"]}
    results, errors, coordinate_warnings, applied_resolutions = [], [], [], []
    for row in rows:
        match = re.search(r"recreation\.gov/camping/campgrounds/(\d+)", row["Reservation website"])
        if not match:
            continue
        facility_id = match.group(1)
        url = f"https://www.recreation.gov/api/camps/campgrounds/{facility_id}"
        request = urllib.request.Request(url, headers={"User-Agent": "WA-RV-Camping-source-audit/1.0"})
        with urllib.request.urlopen(request, timeout=25) as response:
            facility = json.load(response)["campground"]
        expected = ALIASES.get(row["Slug"], row["Name"])
        actual = facility["facility_name"]
        score = difflib.SequenceMatcher(None, normalized(expected), normalized(actual)).ratio()
        suspicious_type = any(word in actual.lower() for word in ("kitchen", "picnic", "day use"))
        ok = score >= 0.65 and not suspicious_type
        official = (facility.get("facility_latitude"), facility.get("facility_longitude"))
        current = legacy_coordinates(row.get("Google Maps Link", ""))
        drift = distance_miles(current, official) if all(value is not None for value in (*current, *official)) else None
        resolution = resolutions.get(row["Slug"])
        resolution_applied = False
        if resolution and all(value is not None for value in current):
            chosen = (resolution["latitude"], resolution["longitude"])
            resolution_applied = distance_miles(current, chosen) <= 0.05
            if resolution_applied:
                applied_resolutions.append(row["Slug"])
        item = {"slug": row["Slug"], "facility_id": facility_id, "expected": expected,
                "actual": actual, "identity_score": round(score, 3), "ok": ok,
                "checked_on": date.today().isoformat(), "source": url,
                "official_latitude": official[0], "official_longitude": official[1],
                "previous_latitude": current[0], "previous_longitude": current[1],
                "coordinate_drift_miles": round(drift, 3) if drift is not None else None,
                "official_directions": facility.get("facility_directions", ""),
                "manual_resolution": resolution.get("decision") if resolution_applied else None}
        results.append(item)
        if not ok:
            errors.append(item)
        if (drift is None or drift > 2) and not resolution_applied:
            coordinate_warnings.append({k: item[k] for k in (
                "slug", "facility_id", "coordinate_drift_miles", "official_latitude", "official_longitude",
                "previous_latitude", "previous_longitude")})
    report = {"checked_on": date.today().isoformat(), "records_checked": len(results),
              "identity_errors": len(errors), "errors": errors,
              "coordinate_warnings": len(coordinate_warnings),
              "manual_coordinate_resolutions": len(applied_resolutions),
              "manual_coordinate_resolution_records": applied_resolutions,
              "coordinate_warning_records": coordinate_warnings, "results": results}
    output = HERE / "recreation-gov-audit.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("checked_on", "records_checked", "identity_errors", "errors", "coordinate_warnings", "coordinate_warning_records", "manual_coordinate_resolutions", "manual_coordinate_resolution_records")}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
