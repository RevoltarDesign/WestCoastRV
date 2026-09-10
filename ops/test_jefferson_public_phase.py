import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
SLUGS = {
    "quilcene-campground", "lake-leland-park-campground",
    "upper-oak-bay-campground", "lower-oak-bay-campground",
    "point-hudson-marina-rv-park", "jefferson-county-fairgrounds-campground",
}

class JeffersonPublicPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data/campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}

    def test_all_six_candidates_are_published(self):
        self.assertTrue(SLUGS <= self.rows.keys())
        for slug in SLUGS:
            self.assertEqual("false", self.rows[slug]["Draft"])
            self.assertEqual("yes", self.rows[slug]["RV Access"])
            self.assertTrue(self.rows[slug]["Latitude"])
            self.assertTrue(self.rows[slug]["Drive route minutes"])

    def test_high_value_facts(self):
        self.assertEqual("30", self.rows["lake-leland-park-campground"]["Max RV length"])
        self.assertEqual("false", self.rows["lake-leland-park-campground"]["Amenities: Drinking water"])
        self.assertEqual("1", self.rows["upper-oak-bay-campground"]["Hookups"])
        self.assertEqual("48", self.rows["point-hudson-marina-rv-park"]["Number of RV campsites"])
        self.assertEqual("50", self.rows["jefferson-county-fairgrounds-campground"]["Max RV length"])
        self.assertEqual("0", self.rows["jefferson-county-fairgrounds-campground"]["Generator policy"])

    def test_coverage_section_is_complete(self):
        coverage = json.loads((HERE / "coverage-inventory.json").read_text())
        section = next(s for s in coverage["sections"] if s["id"] == "jefferson-county-city-port")
        self.assertEqual("complete", section["status"])
        self.assertEqual(6, len(section["candidates"]))
        self.assertTrue(all(c["decision"] == "included_new" and c.get("slug") for c in section["candidates"]))

    def test_topographic_and_locator_assets_exist(self):
        for slug in SLUGS:
            self.assertTrue((SITE / "assets/images/topo" / f"{slug}.jpg").is_file())
            self.assertTrue((SITE / "assets/images/svg" / f"{slug}.svg").is_file())

    def test_guide_and_generated_pages(self):
        guide = (SITE / "field-notes/jefferson-county-rv-camping.html").read_text()
        self.assertGreaterEqual(guide.count('<article class="camp">'), 10)
        for slug in SLUGS:
            self.assertIn(f'/campground/{slug}', guide)
            page = (SITE / "campground" / f"{slug}.html").read_text()
            self.assertIn("Jefferson County RV camping guide", page)
            self.assertIn(f'/assets/images/topo/{slug}.jpg', page)

if __name__ == "__main__":
    unittest.main()
