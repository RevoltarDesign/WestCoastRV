#!/usr/bin/env python3
"""Check every unique booking and evidence URL without changing site data."""
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
EVIDENCE = HERE / "verification-evidence.json"


def collect_urls():
    items = {}
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        for row in csv.DictReader(source):
            url = row.get("Reservation website", "").strip()
            if url:
                items.setdefault(url, {"kind": "reservation", "records": []})["records"].append(row["Slug"])
    ledger = json.loads(EVIDENCE.read_text())
    sources = [source for observation in ledger.get("observations", []) for source in observation.get("sources", [])]
    sources += [rule.get("source", {}) for rule in ledger.get("dataset_rules", [])]
    for source in sources:
        url = source.get("url", "").strip()
        if url:
            items.setdefault(url, {"kind": "evidence", "records": []})
    return items


def check(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 WARVCampgroundLinkCheck/1.0", "Range": "bytes=0-1024"})
    try:
        with urlopen(request, timeout=20) as response:
            return {"status": response.status, "final_url": response.geturl(), "ok": response.status < 400}
    except HTTPError as error:
        return {"status": error.code, "final_url": error.geturl(), "ok": error.code in {401, 403, 405, 429}}
    except (URLError, TimeoutError) as error:
        return {"status": None, "final_url": url, "ok": False, "error": str(error)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    items = collect_urls()
    results = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        pending = {pool.submit(check, url): url for url in items}
        for future in as_completed(pending):
            url = pending[future]
            results[url] = {**items[url], **future.result()}
    failures = {url: result for url, result in results.items() if not result["ok"]}
    if args.json:
        print(json.dumps({"checked": len(results), "failures": failures, "results": results}, indent=2))
    else:
        print(f"External links: {len(results)} checked, {len(failures)} need review")
        for url, result in sorted(failures.items()):
            print(f"FAIL {result.get('status') or result.get('error')} {url}")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
