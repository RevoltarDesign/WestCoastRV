#!/usr/bin/env python3
"""Apply source-backed dataset-wide normalization rules."""
import csv
from pathlib import Path


MASTER = Path(__file__).resolve().parent / "data" / "campgrounds.csv"


def main():
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    changed = 0
    for row in rows:
        if row.get("Park Type") != "State Park":
            continue
        if row.get("Reservation window") == "Reserving 6 months in advance":
            row["Reservation window"] = "Reservable up to 9 months in advance"
            changed += 1

    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Updated the reservation window for {changed} Washington State Parks records.")


if __name__ == "__main__":
    main()
