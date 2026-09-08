import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

class CentralEasternStateParksPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}
        cls.reviews = json.loads((HERE / "central-eastern-state-parks-location-reviews.json").read_text(encoding="utf-8"))["reviews"]

    def test_all_twelve_locations_and_routes_match(self):
        self.assertEqual(12, len(self.reviews))
        for item in self.reviews:
            with self.subTest(slug=item["slug"]):
                row = self.rows[item["slug"]]
                self.assertAlmostEqual(item["latitude"], float(row["Latitude"]), places=6)
                self.assertAlmostEqual(item["longitude"], float(row["Longitude"]), places=6)
                self.assertEqual(item["address"], row["Address"])
                self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))
                self.assertEqual("Seattle, Washington", row["Drive time origin"])

    def test_high_impact_inventory_corrections(self):
        expected = {"potholes-state-park":"121", "columbia-hills-historical-state-park":"12",
                    "maryhill-state-park":"71", "brooks-memorial-state-park":"35",
                    "lincoln-rock-state-park":"94", "alta-lake-state-park":"125",
                    "lake-wenatchee-state-park":"197"}
        for slug, count in expected.items():
            self.assertEqual(count, self.rows[slug]["Number of RV campsites"])
        self.assertEqual("2", self.rows["alta-lake-state-park"]["Hookups"])
        self.assertEqual("40", self.rows["lake-wenatchee-state-park"]["Max RV length"])

    def test_navigation_and_unsupported_claim_corrections(self):
        self.assertIn("Wanapum Recreation Area", self.rows["ginkgo-petrified-forest-state-park"]["Access note"])
        self.assertEqual("false", self.rows["ginkgo-petrified-forest-state-park"]["Dump station on site"])
        self.assertEqual("true", self.rows["columbia-hills-historical-state-park"]["Dump station on site"])
        self.assertNotIn("complimentary", self.rows["maryhill-state-park"]["Long description"].lower())
        self.assertNotIn("most popular", self.rows["pearrygin-lake-state-park"]["Long description"].lower())
        self.assertIn("SR-20 closes seasonally", self.rows["pearrygin-lake-state-park"]["Access note"])

    def test_generated_pages_preserve_key_limits(self):
        alta = (HERE.parent / "campground" / "alta-lake-state-park.html").read_text(encoding="utf-8")
        wenatchee = (HERE.parent / "campground" / "lake-wenatchee-state-park.html").read_text(encoding="utf-8")
        self.assertIn('<div class="stat-val">125</div>', alta)
        self.assertIn("partial rather than full", alta)
        self.assertIn('<div class="stat-val">197</div>', wenatchee)
        self.assertIn("under 20 feet", wenatchee)

if __name__ == "__main__":
    unittest.main()
