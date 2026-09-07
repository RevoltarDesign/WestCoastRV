#!/usr/bin/env python3
"""Apply the reviewed coordinate queue and its current Seattle route checks."""
import csv
import json
import math
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
RESOLUTIONS = HERE / "coordinate-resolutions.json"
CHECKED = "2026-09-06"

ROUTES = {
    "mora-campground": (251, 224, 255, "Fastest no-ferry route; ferry routes may be shorter but add fare and wait-time uncertainty."),
    "cougar-rock-campground": (128, 94.4, 135, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
    "verlot-campground": (67, 54.4, 75, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
    "bedal-campground": (111, 91.3, 120, "Uses the Darrington/WA-530 approach recommended by the Forest Service; public estimate rounded up."),
    "shannon-creek-campground": (128, 112, 135, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
    "douglas-fir-campground": (131, 116, 135, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
    "silver-fir-campground": (146, 127, 150, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
    "coho-campground": (146, 130, 150, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
    "johnny-creek-campground": (151, 128, 165, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
    "nason-creek-campground": (120, 106, 120, "Current fastest driving estimate via US 2; conditions and pass delays vary."),
    "swan-lake-campground": (316, 299, 330, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
    "noisy-creek-campground": (357, 374, 360, "Current fastest driving estimate; road closures and conditions can materially change this trip."),
    "iron-creek-campground": (145, 116, 150, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
    "peterson-prairie-campground": (251, 170, 255, "Current route uses national-forest roads; check seasonal road conditions before towing."),
    "beckler-river-campground": (82, 68.6, 90, "Current fastest driving estimate; public estimate rounded up to the next 15 minutes."),
}


def label(minutes):
    hours, mins = divmod(minutes, 60)
    return f"~{hours} hr" + (f" {mins} min" if mins else "") + " from Seattle"


def band(minutes):
    if minutes < 60: return "Under 1hr"
    if minutes < 120: return "1-2hrs"
    if minutes < 180: return "2-3hrs"
    if minutes < 240: return "3-4hrs"
    return "4+ hrs"


def main():
    review = json.loads(RESOLUTIONS.read_text(encoding="utf-8"))
    resolved = {item["slug"]: item for item in review["resolutions"]}
    if set(resolved) != set(ROUTES):
        raise SystemExit("Resolution and route queues do not match")
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields, rows = list(reader.fieldnames or []), list(reader)
    by_slug = {row["Slug"]: row for row in rows}
    missing = sorted(set(resolved) - set(by_slug))
    if missing:
        raise SystemExit(f"Unknown campground slugs: {missing}")
    coordinate_changes = route_changes = 0
    for slug, item in resolved.items():
        lat, lon = item["latitude"], item["longitude"]
        if not (45.5 <= lat <= 49.1 and -125 <= lon <= -116.8):
            raise SystemExit(f"Coordinate outside Washington: {slug}")
        observed, miles, public, note = ROUTES[slug]
        if public < observed or public % 15:
            raise SystemExit(f"Unsafe public route estimate: {slug}")
        row = by_slug[slug]
        old_link = row.get("Google Maps Link", "")
        new_link = f"https://www.google.com/maps?q={lat:.7f},{lon:.7f}"
        if old_link != new_link:
            coordinate_changes += 1
        if row.get("Drive Time Minutes") != str(public):
            route_changes += 1
        destination = f"{lat:.7f},{lon:.7f}"
        route_url = "https://www.google.com/maps/dir/?api=1&origin=" + quote("Seattle, Washington") + "&destination=" + destination + "&travelmode=driving"
        row.update({
            "Latitude": f"{lat:.7f}", "Longitude": f"{lon:.7f}",
            "Google Maps Link": new_link,
            "Coordinates source": "Google Maps named campground destination; corroborated by Recreation.gov facility record and agency directions",
            "Coordinates checked": CHECKED,
            "Coordinate precision": "reviewed campground navigation point",
            "Time from Seattle": label(public), "Drive Time Minutes": str(public), "Drive Time Band": band(public),
            "Drive distance miles": f"{miles:g}", "Drive route minutes": str(observed),
            "Drive time origin": "Seattle, Washington", "Drive time source": route_url,
            "Drive time checked": CHECKED, "Drive time note": note,
        })
        if slug == "mora-campground":
            row["Coordinates source"] = "Google Maps named campground destination and agency directions; Recreation.gov API coordinate is invalid (0,0)"
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    print(f"Resolved {len(resolved)} manual coordinate reviews ({coordinate_changes} pins changed).")
    print(f"Reviewed 15 Seattle routes ({route_changes} public estimates changed).")


if __name__ == "__main__":
    main()
