import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent


class JeffersonFederalPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data/campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}

    def test_falls_view_is_published_with_reviewed_trip_data(self):
        row = self.rows["falls-view-campground"]
        self.assertEqual("false", row["Draft"])
        self.assertEqual("yes", row["RV Access"])
        self.assertEqual("35", row["Max RV length"])
        self.assertEqual("0", row["Hookups"])
        self.assertEqual("47.7905528", row["Latitude"])
        self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))

    def test_seal_rock_factual_corrections(self):
        row = self.rows["seal-rock-campground"]
        self.assertEqual("21", row["Max RV length"])
        self.assertEqual("47.7103836", row["Latitude"])
        self.assertIn("closed", row["Reservation window"].lower())
        self.assertNotEqual("40", row["Max RV length"])
        page = (SITE / "campground/seal-rock-campground.html").read_text().lower()
        self.assertIn("labels the facility closed", page)
        self.assertNotIn("currently campground closed", page)
        self.assertIn("21 ft", page)
        self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))

    def test_federal_inventory_has_complete_decisions(self):
        coverage = json.loads((HERE / "coverage-inventory.json").read_text())
        section = next(s for s in coverage["sections"] if s["id"] == "jefferson-federal")
        self.assertEqual("complete", section["status"])
        self.assertEqual(11, len(section["candidates"]))
        self.assertTrue(all(c["decision"] in {"included_existing", "included_new", "excluded", "deferred"} for c in section["candidates"]))

    def test_generated_assets_and_regional_guide(self):
        guide = (SITE / "field-notes/jefferson-county-rv-camping.html").read_text()
        self.assertEqual(17, guide.count('<article class="camp">'))
        for slug in {"falls-view-campground", "hoh-campground", "kalaloch-campground", "south-beach-campground"}:
            self.assertIn(f"/campground/{slug}", guide)
        self.assertTrue((SITE / "assets/images/topo/falls-view-campground.jpg").is_file())
        self.assertTrue((SITE / "assets/images/svg/falls-view-campground.svg").is_file())
        page = (SITE / "campground/falls-view-campground.html").read_text()
        self.assertIn("Jefferson County RV camping guide", page)


if __name__ == "__main__":
    unittest.main()
