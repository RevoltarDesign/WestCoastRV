#!/usr/bin/env python3
"""Report provenance coverage for coordinates and Seattle drive estimates."""
import csv
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATASET = HERE / "data" / "campgrounds.csv"


def main():
    rows = list(csv.DictReader(DATASET.open(newline="", encoding="utf-8-sig")))
    coord_fields = ("Latitude", "Longitude", "Coordinates source", "Coordinates checked")
    route_fields = ("Drive distance miles", "Drive route minutes", "Drive time origin", "Drive time source", "Drive time checked")
    sourced_coords = [r for r in rows if all(r.get(k) for k in coord_fields)]
    sourced_routes = [r for r in rows if all(r.get(k) for k in route_fields)]
    errors = []
    for row in sourced_routes:
        if row["Drive time origin"] != "Seattle, Washington":
            errors.append(f"{row['Slug']}: inconsistent route origin")
        if int(row["Drive Time Minutes"]) < int(row["Drive route minutes"]):
            errors.append(f"{row['Slug']}: public estimate is lower than observed route")
        if not row["Drive time source"].startswith("https://www.google.com/maps/dir/"):
            errors.append(f"{row['Slug']}: unsupported route source")
        try:
            date.fromisoformat(row["Drive time checked"])
        except ValueError:
            errors.append(f"{row['Slug']}: invalid route review date")
    report = {"campgrounds": len(rows), "coordinates_with_provenance": len(sourced_coords),
              "routes_with_provenance": len(sourced_routes), "coordinates_remaining": len(rows) - len(sourced_coords),
              "routes_remaining": len(rows) - len(sourced_routes), "errors": errors}
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
