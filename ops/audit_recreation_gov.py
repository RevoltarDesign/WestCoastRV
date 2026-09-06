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
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATASET = HERE / "data" / "campgrounds.csv"
ALIASES = {
    "hoh-campground": "Hoh Rainforest Campground",
    "sol-duc-campground": "Sol Duc Hot Springs Resort Campground",
}


def normalized(value):
    return re.sub(r"[^a-z0-9]", "", value.lower().replace("campground", ""))


def main():
    with DATASET.open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))
    results, errors = [], []
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
        item = {"slug": row["Slug"], "facility_id": facility_id, "expected": expected,
                "actual": actual, "identity_score": round(score, 3), "ok": ok,
                "checked_on": date.today().isoformat(), "source": url}
        results.append(item)
        if not ok:
            errors.append(item)
    report = {"checked_on": date.today().isoformat(), "records_checked": len(results),
              "identity_errors": len(errors), "errors": errors, "results": results}
    output = HERE / "recreation-gov-audit.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("checked_on", "records_checked", "identity_errors", "errors")}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
