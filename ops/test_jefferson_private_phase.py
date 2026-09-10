import csv
import json
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
SLUGS = {"cove-rv-park-country-store", "hard-rain-cafe-campground", "port-ludlow-rv-park"}


class JeffersonPrivatePhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data/campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}

    def test_three_current_transient_parks_are_published(self):
        self.assertTrue(SLUGS <= self.rows.keys())
        for slug in SLUGS:
            self.assertEqual("false", self.rows[slug]["Draft"])
            self.assertEqual("yes", self.rows[slug]["RV Access"])
            self.assertTrue(self.rows[slug]["Latitude"])
            self.assertTrue(self.rows[slug]["Drive route minutes"])

    def test_high_value_facts(self):
        self.assertEqual("40", self.rows["cove-rv-park-country-store"]["Max RV length"])
        self.assertEqual("3", self.rows["cove-rv-park-country-store"]["Hookups"])
        self.assertEqual("13", self.rows["hard-rain-cafe-campground"]["Number of RV campsites"])
        self.assertEqual("2", self.rows["hard-rain-cafe-campground"]["Hookups"])
        self.assertEqual("37", self.rows["port-ludlow-rv-park"]["Number of RV campsites"])

    def test_coverage_decisions_are_complete(self):
        coverage = json.loads((HERE / "coverage-inventory.json").read_text())
        section = next(s for s in coverage["sections"] if s["id"] == "jefferson-private-tribal")
        self.assertEqual("complete", section["status"])
        self.assertEqual(6, len(section["candidates"]))
        self.assertTrue(all(c["decision"] in {"included_new", "excluded"} for c in section["candidates"]))

    def test_assets_pages_and_guide(self):
        guide = (SITE / "field-notes/jefferson-county-rv-camping.html").read_text()
        self.assertEqual(17, guide.count('<article class="camp">'))
        for slug in SLUGS:
            self.assertTrue((SITE / "assets/images/topo" / f"{slug}.jpg").is_file())
            self.assertTrue((SITE / "assets/images/svg" / f"{slug}.svg").is_file())
            self.assertIn(f"/campground/{slug}", guide)
            page = (SITE / "campground" / f"{slug}.html").read_text()
            self.assertIn("Jefferson County RV camping guide", page)
            self.assertIn(f"/assets/images/topo/{slug}.jpg", page)

    def test_unconfirmed_dump_station_is_not_presented_as_no(self):
        for slug in {"cove-rv-park-country-store", "hard-rain-cafe-campground"}:
            self.assertEqual("", self.rows[slug]["Dump station on site"])
            page = (SITE / "campground" / f"{slug}.html").read_text()
            self.assertIn("Not confirmed", page)
            schemas = [json.loads(value) for value in re.findall(
                r'<script type="application/ld\+json">\s*(.*?)\s*</script>', page, re.DOTALL
            )]
            schema = next(value for value in schemas if "amenityFeature" in value)
            names = {feature["name"] for feature in schema["amenityFeature"]}
            self.assertNotIn("Dump Station", names)


if __name__ == "__main__":
    unittest.main()
