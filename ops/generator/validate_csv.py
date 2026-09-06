#!/usr/bin/env python3
"""
validate_csv.py — Pre-import CSV validator
==========================================
Run this before every Webflow import to catch any value drift,
missing fields, or format inconsistencies.

USAGE:
  python3 validate_csv.py              # validate all 4 tier CSVs
  python3 validate_csv.py --master     # also validate master CSV
  python3 validate_csv.py --fix        # auto-fix slug mismatches (dry-run first)

EXIT CODE:
  0 = all checks passed
  1 = one or more errors found
"""

import csv
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[3] / "Scripts"

# ── Field constraints (must match Webflow exactly) ────────────────────────────

OPTION_FIELDS = {
    "Maneuverability":    {"1", "2", "3"},
    "Site surface type":  {"Paved", "Gravel", "Dirt", "Mixed"},
    "Hookups":            {"0", "1", "2", "3"},
    "Generator policy":   {"0", "1", "2"},
    "Cell coverage":      {"0", "1", "2"},
    "Amenities: Toilets": {"Vaulted toilets", "Flush toilets"},  # empty = None
}

SWITCH_FIELDS = [
    "Archived",
    "Draft",
    "Dump station on site",
    "Amenities: Showers",
    "Amenities: Drinking water",
    "Amenities: Fire pits",
    "Hiking",
    "Fishing",
    "Swimming",
    "Kayaking/Paddling",
    "Beach & Tide Pools",
    "Boating",
    "Playground",
]

NUMBER_FIELDS = [
    "Number of RV campsites",
    "Max RV length",
    "Nearest state park",
    "Nearest gas station",
    "Nearest major grocery store",
    "Nearest Costco",
    "Nearest Starbucks",
]

LINK_FIELDS = [
    "Reservation website",
    "Google Maps Link",
]

REQUIRED_FIELDS = [
    "Name",
    "Slug",
    "Short Description",
    "Long description",
    "Park Type",
    "Reservation window",
    "Time from Seattle",
    "Address",
    "Maneuverability",
    "Site surface type",
    "Hookups",
    "Cell coverage",
    "Amenities: Toilets",
    "Nearest town",
    "Site Recommendations",
    "Google Maps Link",
    "Data last updated",
]

SKIP_EMPTY_CHECK = {
    # Image fields and Webflow-managed fields are intentionally empty on first import
    "Topographic background image",
    "Hero image",
    "State Map",
    "Collection ID",
    "Locale ID",
    "Item ID",
    "Created On",
    "Updated On",
    "Published On",
    # Multi-reference populated in Pass 2
    "Nearby campgrounds",
}

TIER_FILES = [
    "Washington RV Camping - Campgrounds - Tier1 National Parks.csv",
    "Washington RV Camping - Campgrounds - Tier2 State Parks.csv",
    "Washington RV Camping - Campgrounds - Tier3 National Forests.csv",
    "Washington RV Camping - Campgrounds - Tier4 County and Private.csv",
]

MASTER_FILE = "Washington RV Camping - Campgrounds - ALL CAMPGROUNDS (Master).csv"
CANONICAL_SLUG_EXCEPTIONS = {
    "Osoyoos Lake Veteran's Memorial Park": "osoyoos-lake-veterans-memorial-state-park",
}


# ── Slug helper ───────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"['\u2018\u2019\u201b`]", "", s)
    s = re.sub(r"[^a-z0-9\s\-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


# ── Validators ────────────────────────────────────────────────────────────────

def validate_file(path: Path) -> list[str]:
    """Run all checks on a single CSV. Returns list of error strings."""
    errors = []

    if not path.exists():
        return [f"FILE NOT FOUND: {path.name}"]

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    tier = path.name.split(" - ", 2)[-1].replace(".csv", "")

    # 1. Required fields present in CSV
    for col in REQUIRED_FIELDS:
        if col not in fieldnames:
            errors.append(f"[{tier}] MISSING COLUMN: '{col}'")

    # 2. Option fields — valid values only
    for col, valid in OPTION_FIELDS.items():
        if col not in fieldnames:
            continue
        for row in rows:
            val = row.get(col, "").strip()
            if val and val not in valid:
                errors.append(
                    f"[{tier}] INVALID OPTION '{col}' = {val!r} "
                    f"(valid: {sorted(valid)}) — {row['Name']}"
                )

    # 3. Switch fields — must be 'true' or 'false'
    for col in SWITCH_FIELDS:
        if col not in fieldnames:
            continue
        for row in rows:
            val = row.get(col, "").strip().lower()
            if val and val not in {"true", "false"}:
                errors.append(
                    f"[{tier}] INVALID SWITCH '{col}' = {val!r} — {row['Name']}"
                )

    # 4. Number fields — must be integers
    for col in NUMBER_FIELDS:
        if col not in fieldnames:
            continue
        for row in rows:
            val = row.get(col, "").strip()
            if val and not re.match(r"^\d+$", val):
                errors.append(
                    f"[{tier}] NON-NUMERIC '{col}' = {val!r} — {row['Name']}"
                )

    # 5. Link fields — must be valid URLs (start with http/https, no double protocol)
    for col in LINK_FIELDS:
        if col not in fieldnames:
            continue
        for row in rows:
            val = row.get(col, "").strip()
            if not val:
                continue
            if not re.match(r"^https?://", val):
                errors.append(
                    f"[{tier}] INVALID URL '{col}' = {val!r} — {row['Name']}"
                )
            elif re.search(r"https?://.*https?://", val):
                errors.append(
                    f"[{tier}] DOUBLE PROTOCOL in '{col}' = {val!r} — {row['Name']}"
                )

    # 7. Required fields — must not be empty
    for col in REQUIRED_FIELDS:
        if col not in fieldnames:
            continue
        for row in rows:
            if not row.get(col, "").strip():
                errors.append(
                    f"[{tier}] EMPTY REQUIRED '{col}' — {row['Name']}"
                )

    # 8. Slug consistency — must match slugify(Name)
    if "Slug" in fieldnames:
        for row in rows:
            name = row.get("Name", "").strip()
            slug = row.get("Slug", "").strip()
            expected = CANONICAL_SLUG_EXCEPTIONS.get(name, slugify(name))
            if slug != expected:
                errors.append(
                    f"[{tier}] SLUG MISMATCH — {name!r}: "
                    f"CSV={slug!r} expected={expected!r}"
                )

    # 9. Nearby campgrounds — semicolon-separated slugs, no spaces
    if "Nearby campgrounds" in fieldnames:
        for row in rows:
            val = row.get("Nearby campgrounds", "").strip()
            if not val:
                continue
            parts = val.split(";")
            for part in parts:
                if " " in part:
                    errors.append(
                        f"[{tier}] SLUG WITH SPACE in 'Nearby campgrounds': "
                        f"{part!r} — {row['Name']}"
                    )

    # 10. Duplicate slugs
    if "Slug" in fieldnames:
        seen = {}
        for row in rows:
            slug = row.get("Slug", "").strip()
            if slug in seen:
                errors.append(
                    f"[{tier}] DUPLICATE SLUG {slug!r}: "
                    f"{seen[slug]!r} and {row['Name']!r}"
                )
            seen[slug] = row.get("Name", "")

    return errors


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    include_master = "--master" in sys.argv
    files = TIER_FILES + ([MASTER_FILE] if include_master else [])

    print("WA RV Campground CSV Validator")
    print("=" * 55)

    all_errors = []
    for filename in files:
        path = BASE / filename
        errors = validate_file(path)
        tier = filename.split(" - ", 2)[-1].replace(".csv", "")
        if errors:
            print(f"\n  ✗  {tier}")
            for e in errors:
                # Strip the [tier] prefix for cleaner display
                msg = re.sub(r"^\[.*?\] ", "", e)
                print(f"       {msg}")
        else:
            print(f"  ✓  {tier}")
        all_errors.extend(errors)

    print("\n" + "=" * 55)
    if all_errors:
        print(f"  {len(all_errors)} error(s) found — fix before importing to Webflow")
        sys.exit(1)
    else:
        print(f"  All checks passed — safe to import")
        sys.exit(0)


if __name__ == "__main__":
    main()
