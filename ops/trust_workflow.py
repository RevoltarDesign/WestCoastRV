#!/usr/bin/env python3
"""Validate field evidence and campground coverage decisions.

This is deliberately read-only. Research proposes facts; a reviewed source row
remains the only input that can change published campground pages.
"""
import argparse
from datetime import date
import json
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / "verification-evidence.json"
COVERAGE = HERE / "coverage-inventory.json"
DATASET = HERE / "data" / "campgrounds.csv"
CRITICAL = {"operating_status", "rv_access", "reservation_method", "max_rv_length", "hookups"}
ACCEPTED = {"supported", "corrected_locally"}
DECISIONS = {"included_existing", "included_new", "excluded", "deferred", "research"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def valid_source(source):
    parsed = urlparse(source.get("url", ""))
    return parsed.scheme == "https" and bool(parsed.netloc) and all(
        source.get(key) for key in ("publisher", "source_family", "evidence")
    )


def audit(as_of):
    evidence = load(EVIDENCE)
    coverage = load(COVERAGE)
    errors, warnings = [], []
    seen = set()
    supported = {}
    for rule in evidence.get("dataset_rules", []):
        key = rule.get("id", "unnamed-rule")
        if not all(rule.get(field) for field in ("scope", "field", "checked_on", "value")):
            errors.append(f"incomplete dataset rule: {key}")
        try:
            checked = date.fromisoformat(rule["checked_on"])
            if checked > as_of:
                errors.append(f"future dataset rule date: {key}")
        except (KeyError, ValueError):
            errors.append(f"invalid dataset rule date: {key}")
        if not valid_source(rule.get("source", {})):
            errors.append(f"malformed dataset rule source: {key}")
    for item in evidence.get("observations", []):
        key = (item.get("slug"), item.get("field"))
        if key in seen:
            errors.append(f"duplicate evidence: {key[0]} / {key[1]}")
        seen.add(key)
        if item.get("status") not in ACCEPTED | {"conflict", "stale", "unknown", "unresearched"}:
            errors.append(f"invalid evidence status: {key}")
        try:
            checked = date.fromisoformat(item["checked_on"])
            if checked > as_of:
                errors.append(f"future evidence date: {key}")
        except (KeyError, ValueError):
            errors.append(f"invalid evidence date: {key}")
        sources = item.get("sources", [])
        if item.get("status") in ACCEPTED and not sources:
            errors.append(f"accepted fact has no source: {key}")
        if any(not valid_source(source) for source in sources):
            errors.append(f"malformed source: {key}")
        if item.get("status") in ACCEPTED:
            supported.setdefault(item.get("slug"), set()).add(item.get("field"))

    candidate_keys = set()
    for section in coverage.get("sections", []):
        undecided = 0
        if not section.get("inventory_sources") and section.get("status") == "complete":
            errors.append(f"complete section has no inventory source: {section.get('id')}")
        for candidate in section.get("candidates", []):
            key = (section.get("id"), candidate.get("name"))
            if key in candidate_keys:
                errors.append(f"duplicate coverage candidate: {key}")
            candidate_keys.add(key)
            if candidate.get("decision") not in DECISIONS:
                errors.append(f"invalid coverage decision: {key}")
            if candidate.get("decision") == "research":
                undecided += 1
            if candidate.get("decision", "").startswith("included") and not candidate.get("slug"):
                errors.append(f"included candidate missing slug: {key}")
            if not candidate.get("reason"):
                errors.append(f"coverage decision missing reason: {key}")
        if section.get("status") == "complete" and undecided:
            errors.append(f"complete section has {undecided} research decisions: {section.get('id')}")

    import csv
    with DATASET.open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))
    rule_support = {}
    for row in rows:
        fields = set()
        for rule in evidence.get("dataset_rules", []):
            scope = rule.get("scope", "")
            if scope.startswith("Park Type = ") and row.get("Park Type") == scope.removeprefix("Park Type = "):
                fields.add(rule.get("field"))
        rule_support[row["Slug"]] = fields

    coverage_summary = {"campgrounds": len(rows), "fully_supported": 0, "partially_supported": 0,
                        "unresearched": 0, "supported_by_field": {field: 0 for field in sorted(CRITICAL)}}
    for row in rows:
        slug = row["Slug"]
        fields = supported.get(slug, set()) | rule_support.get(slug, set())
        for field in fields & CRITICAL:
            coverage_summary["supported_by_field"][field] += 1
        missing = sorted(CRITICAL - fields)
        if missing:
            warnings.append(f"{slug}: critical evidence remaining: {', '.join(missing)}")
        if not missing:
            coverage_summary["fully_supported"] += 1
        elif fields:
            coverage_summary["partially_supported"] += 1
        else:
            coverage_summary["unresearched"] += 1
    return {"errors": errors, "warnings": warnings,
            "supported": {k: sorted(v) for k, v in supported.items()},
            "coverage_summary": coverage_summary}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("check", "summary"), nargs="?", default="check")
    parser.add_argument("--as-of", default=date.today().isoformat())
    args = parser.parse_args()
    result = audit(date.fromisoformat(args.as_of))
    if args.command == "summary":
        print(json.dumps(result, indent=2))
    else:
        for message in result["errors"]:
            print("ERROR", message)
        for message in result["warnings"]:
            print("WARN ", message)
        print(f"Trust workflow: {len(result['errors'])} errors, {len(result['warnings'])} warnings")
    raise SystemExit(bool(result["errors"]))


if __name__ == "__main__":
    main()
