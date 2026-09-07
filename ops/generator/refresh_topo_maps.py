#!/usr/bin/env python3
"""Refresh USGS topographic images for rows with reviewed coordinate provenance."""
import argparse
import csv
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parents[1]
PROJECT = SITE.parent
SOURCE = PROJECT / "Scripts" / "generate_topo.py"
CSV_PATH = HERE.parent / "data" / "campgrounds.csv"
OUT = SITE / "assets" / "images" / "topo"


def renderer_module():
    spec = importlib.util.spec_from_file_location("topo_renderer", SOURCE)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug")
    args = parser.parse_args()
    renderer = renderer_module()
    rows = list(csv.DictReader(CSV_PATH.open(newline="", encoding="utf-8-sig")))
    targets = [r for r in rows if r.get("Latitude") and r.get("Longitude") and r.get("Coordinates source")]
    if args.slug:
        targets = [r for r in targets if r["Slug"] == args.slug]
    if args.slug and not targets:
        raise SystemExit(f"No sourced coordinate record found for {args.slug}")
    failures = []
    for row in targets:
        lat, lon = float(row["Latitude"]), float(row["Longitude"])
        bbox = renderer.build_bbox(lat, lon, renderer.ZOOM_SPANS[renderer.DEFAULT_ZOOM])
        try:
            renderer.download(renderer.build_url(*bbox), OUT / f"{row['Slug']}.jpg")
        except Exception as exc:
            failures.append(f"{row['Slug']}: {exc}")
    print(f"Refreshed {len(targets) - len(failures)} of {len(targets)} sourced topographic maps.")
    for failure in failures:
        print(f"ERROR {failure}")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
