#!/usr/bin/env python3
"""Offline regression checks for factual contamination and unsupported wording."""
import csv
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATASET = HERE / "data" / "campgrounds.csv"


def audit():
    with DATASET.open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))
    errors = []
    by_slug = {row["Slug"]: row for row in rows}

    forbidden = {
        "silver-lake-park": ("cowlitz", "mount st. helens", "heather meadows", "mt. baker"),
        "osoyoos-lake-veterans-memorial-state-park": ("osoyoos lake veterans memorial state park",),
        "andersens-oceanside-rv-park": ("ocean shores", "grays harbor"),
        "lake-easton-state-park": ("john wayne pioneer trail", "wild and scenic"),
    }
    for slug, phrases in forbidden.items():
        text = " ".join(by_slug[slug].values()).lower()
        for phrase in phrases:
            if phrase in text:
                errors.append(f"{slug}: cross-region or obsolete identity: {phrase}")

    for row in rows:
        summary = row.get("Amenities summary", "")
        if re.search(r"every site (?:includes|has) (?:a )?fire pit|fire pits? at every site", summary, re.I):
            errors.append(f"{row['Slug']}: unsupported universal fire-pit claim")
        if "closed for rehabilitation through early 2026" in row.get("Long description", "").lower():
            errors.append(f"{row['Slug']}: stale closure language")

    expected_links = {
        "big-creek-campground": "fs.usda.gov/recarea/olympic/",
        "swan-lake-campground": "/10378408",
    }
    for slug, fragment in expected_links.items():
        if fragment not in by_slug[slug]["Reservation website"]:
            errors.append(f"{slug}: reservation link no longer identifies the correct facility")
    return {"campgrounds_checked": len(rows), "errors": errors}


def main():
    result = audit()
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["errors"]))


if __name__ == "__main__":
    main()
