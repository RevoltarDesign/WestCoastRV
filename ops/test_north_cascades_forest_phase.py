import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

class NorthCascadesForestPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}
        cls.reviews = json.loads((HERE / "north-cascades-forest-location-reviews.json").read_text(encoding="utf-8"))["reviews"]

    def test_inventory_corrections(self):
        expected = {"tinkham-campground":"42", "kachess-campground":"150", "verlot-campground":"19",
                    "gold-basin-campground":"37", "turlo-campground":"18", "bedal-campground":"22",
                    "horseshoe-cove-campground":"39", "shannon-creek-campground":"14"}
        for slug, count in expected.items(): self.assertEqual(count, self.rows[slug]["Number of RV campsites"])
        self.assertEqual("", self.rows["verlot-campground"]["Max RV length"])
        self.assertEqual("", self.rows["turlo-campground"]["Max RV length"])
        self.assertEqual("", self.rows["horseshoe-cove-campground"]["Max RV length"])
        self.assertEqual("58", self.rows["bedal-campground"]["Max RV length"])

    def test_location_and_routes(self):
        self.assertEqual(8, len(self.reviews))
        for item in self.reviews:
            row = self.rows[item["slug"]]
            self.assertAlmostEqual(item["latitude"], float(row["Latitude"]), places=6)
            self.assertAlmostEqual(item["longitude"], float(row["Longitude"]), places=6)
            self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))
        self.assertIn("Darrington", self.rows["bedal-campground"]["Drive time note"])
        self.assertIn("mill pond", self.rows["gold-basin-campground"]["Access note"].lower())

    def test_current_access_and_claims(self):
        self.assertIn("Three Queens Fire", self.rows["kachess-campground"]["Access note"])
        self.assertIn("tent-only", self.rows["shannon-creek-campground"]["Short Description"])
        for slug in [item["slug"] for item in self.reviews]:
            self.assertEqual("0", self.rows[slug]["Hookups"])
            self.assertEqual("yes", self.rows[slug]["RV Access"])

    def test_generated_pages(self):
        tinkham = (HERE.parent / "campground" / "tinkham-campground.html").read_text(encoding="utf-8")
        kachess = (HERE.parent / "campground" / "kachess-campground.html").read_text(encoding="utf-8")
        self.assertIn('<div class="stat-val">42</div>', tinkham)
        self.assertIn("42 public standard sites", tinkham)
        self.assertIn("Three Queens Fire", kachess)

if __name__ == "__main__": unittest.main()
