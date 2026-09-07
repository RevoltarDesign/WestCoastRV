#!/usr/bin/env python3
"""Offline coordinate gate: bounds, field consistency, reviewed pins, and near duplicates."""
import csv, json, math, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
MAP_COORDS = re.compile(r"(?:q=|destination=)(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)")

def miles(a, b):
    lat1, lon1 = map(math.radians, a); lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2-lat1, lon2-lon1
    value = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 3958.8 * 2 * math.asin(math.sqrt(value))

def point(row):
    if row["Latitude"] and row["Longitude"]: return float(row["Latitude"]), float(row["Longitude"])
    match = MAP_COORDS.search(row["Google Maps Link"] or "")
    return (float(match.group(1)), float(match.group(2))) if match else None

def main():
    with MASTER.open(newline="", encoding="utf-8-sig") as source: rows = list(csv.DictReader(source))
    errors, warnings, points = [], [], {}
    for row in rows:
        p = point(row)
        if not p:
            errors.append(f"{row['Slug']}: missing usable coordinates"); continue
        points[row["Slug"]] = p
        if not (45.5 <= p[0] <= 49.1 and -125.0 <= p[1] <= -116.7): errors.append(f"{row['Slug']}: outside Washington bounds {p}")
        if row["Latitude"] and row["Longitude"]:
            match = MAP_COORDS.search(row["Google Maps Link"] or "")
            if match and miles(p, (float(match.group(1)), float(match.group(2)))) > .01: errors.append(f"{row['Slug']}: explicit fields disagree with Google Maps link")
        if not row["Coordinates source"]: warnings.append(f"{row['Slug']}: coordinate has not completed sourced review")
    reviews = []
    for name in ("coordinate-resolutions.json", "peninsula-location-reviews.json"):
        payload = json.loads((HERE / name).read_text(encoding="utf-8")); reviews.extend(payload.get("resolutions", payload.get("reviews", [])))
    for item in reviews:
        actual = points.get(item["slug"]); expected = item["latitude"], item["longitude"]
        if not actual or miles(expected, actual) > .01: errors.append(f"{item['slug']}: reviewed coordinate drifted from its evidence record")
    slugs = sorted(points)
    for index, left in enumerate(slugs):
        for right in slugs[index+1:]:
            distance = miles(points[left], points[right])
            if distance < .02: warnings.append(f"{left} and {right}: pins are only {distance:.3f} miles apart; confirm they are distinct")
    print(f"Coordinate gate: {len(rows)} records, {len(errors)} errors, {len(warnings)} warnings")
    for message in errors: print(f"ERROR {message}")
    for message in warnings[:20]: print(f"WARN  {message}")
    if len(warnings) > 20: print(f"WARN  ... {len(warnings)-20} more warnings")
    raise SystemExit(1 if errors else 0)

if __name__ == "__main__": main()
