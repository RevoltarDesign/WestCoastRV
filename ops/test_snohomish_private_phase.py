import csv, json, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
SLUGS = {
    "angel-of-the-winds-rv-resort", "lake-pleasant-rv-park", "maple-grove-rv-resort",
    "cascade-views-rv-resort", "thousand-trails-thunderbird", "emerald-springs-rv-park",
    "lake-goodwin-resort", "lake-ki-rv-resort"
}

class SnohomishPrivatePhaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data/campgrounds.csv").open(newline="", encoding="utf-8-sig") as handle:
            cls.rows = {r["Slug"]: r for r in csv.DictReader(handle)}

    def test_all_eight_records_and_assets_exist(self):
        self.assertTrue(SLUGS <= self.rows.keys())
        for slug in SLUGS:
            self.assertTrue((SITE / "campground" / f"{slug}.html").exists())
            self.assertTrue((SITE / "assets/images/topo" / f"{slug}.jpg").exists())
            self.assertTrue((SITE / "assets/images/svg" / f"{slug}.svg").exists())

    def test_unknown_is_distinct_from_no_hookups(self):
        for slug in ("cascade-views-rv-resort", "thousand-trails-thunderbird"):
            self.assertEqual("", self.rows[slug]["Hookups"])
            page = (SITE / "campground" / f"{slug}.html").read_text()
            self.assertIn("Not confirmed", page)
            self.assertNotIn(f"{self.rows[slug]['Name']} is dry camping only", page)

    def test_location_and_route_provenance_is_complete(self):
        for slug in SLUGS:
            row = self.rows[slug]
            for field in ("Latitude", "Longitude", "Coordinates source", "Coordinates checked",
                          "Drive distance miles", "Drive route minutes", "Drive time source", "Drive time checked"):
                self.assertTrue(row[field], f"{slug}: {field}")
            self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))

    def test_coverage_and_critical_evidence_are_complete(self):
        coverage = json.loads((HERE / "coverage-inventory.json").read_text())
        section = next(s for s in coverage["sections"] if s["id"] == "snohomish-private-tribal")
        self.assertEqual("complete", section["status"])
        included = {c.get("slug") for c in section["candidates"] if c["decision"] == "included_new"}
        self.assertEqual(SLUGS, included)
        evidence = json.loads((HERE / "verification-evidence.json").read_text())["observations"]
        for slug in SLUGS:
            fields = {o["field"] for o in evidence if o.get("slug") == slug and o.get("source_family") == "snohomish-private-review"}
            self.assertTrue({"operating_status", "rv_access", "reservation_method", "hookups", "max_rv_length"} <= fields)

    def test_guide_contains_all_snohomish_records(self):
        guide = (SITE / "field-notes/snohomish-county-rv-camping.html").read_text()
        self.assertEqual(15, guide.count('<article class="camp">'))
        for slug in SLUGS:
            self.assertIn(f"/campground/{slug}", guide)

if __name__ == "__main__":
    unittest.main()
