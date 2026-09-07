#!/usr/bin/env python3
"""Apply the named-destination and no-ferry route review for seven Peninsula records."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEW = HERE / "peninsula-location-reviews.json"

def duration(minutes):
    hours, mins = divmod(minutes, 60)
    return f"~{hours} hr {mins} min from Seattle" if mins else f"~{hours} hr from Seattle"

def band(minutes):
    return "4+ hrs" if minutes >= 240 else "3-4hrs" if minutes >= 180 else "2-3hrs"

def route_url(lat, lon):
    return f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat},{lon}&travelmode=driving"

def main():
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    checked = review["checked_on"]
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields, rows = list(reader.fieldnames or []), list(reader)
    by_slug = {row["Slug"]: row for row in rows}
    for item in review["reviews"]:
        row = by_slug[item["slug"]]
        lat, lon = item["latitude"], item["longitude"]
        display = item["display_minutes"]
        row.update({
            "Data last updated": checked, "Address": item["address"],
            "Latitude": str(lat), "Longitude": str(lon),
            "Google Maps Link": f"https://www.google.com/maps?q={lat},{lon}",
            "Coordinates source": "Google Maps exact named destination matched to the published street address",
            "Coordinates checked": checked, "Coordinate precision": "named campground point",
            "Time from Seattle": duration(display), "Drive Time Minutes": str(display),
            "Drive Time Band": band(display), "Drive distance miles": str(item["distance_miles"]),
            "Drive route minutes": str(item["observed_route_minutes"]), "Drive time origin": "Seattle, Washington",
            "Drive time source": route_url(lat, lon), "Drive time checked": checked,
            "Drive time note": "Fastest no-ferry option at review time; ferry routes may be shorter but add fare and wait-time uncertainty.",
        })
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    print(f"Applied {len(review['reviews'])} Peninsula location and route reviews.")

if __name__ == "__main__":
    main()
