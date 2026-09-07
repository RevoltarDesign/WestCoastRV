#!/usr/bin/env python3
"""Generate every campground locator SVG from the canonical coordinate record."""
import argparse
import csv
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parents[1]
PROJECT = SITE.parent
SOURCE = PROJECT / "Scripts" / "generate_campground_svgs.py"
CSV_PATH = HERE.parent / "data" / "campgrounds.csv"
OUT = SITE / "assets" / "images" / "svg"


def load_renderer():
    spec = importlib.util.spec_from_file_location("legacy_state_map_renderer", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug")
    args = parser.parse_args()
    renderer = load_renderer()
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source); fields, rows = list(reader.fieldnames or []), list(reader)
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for row in rows:
        if args.slug and row["Slug"] != args.slug:
            continue
        lat = row.get("Latitude") or renderer.extract_lat_lng(row.get("Google Maps Link", ""))[0]
        lon = row.get("Longitude") or renderer.extract_lat_lng(row.get("Google Maps Link", ""))[1]
        if lat in (None, "") or lon in (None, ""):
            raise SystemExit(f"Missing coordinates: {row['Slug']}")
        (OUT / f"{row['Slug']}.svg").write_text(renderer.make_svg(float(lat), float(lon)), encoding="utf-8")
        row["State Map"] = f"/assets/images/svg/{row['Slug']}.svg"
        count += 1
    with CSV_PATH.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    print(f"Generated {count} local campground locator maps from canonical coordinates.")


if __name__ == "__main__":
    main()
