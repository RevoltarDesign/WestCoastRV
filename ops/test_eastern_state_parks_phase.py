import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

class EasternStateParksPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}
        cls.reviews = json.loads((HERE / "eastern-state-parks-location-reviews.json").read_text(encoding="utf-8"))["reviews"]

    def test_all_eight_locations_and_routes_match(self):
        self.assertEqual(8, len(self.reviews))
        for item in self.reviews:
            with self.subTest(slug=item["slug"]):
                row = self.rows[item["slug"]]
                self.assertAlmostEqual(item["latitude"], float(row["Latitude"]), places=6)
                self.assertAlmostEqual(item["longitude"], float(row["Longitude"]), places=6)
                self.assertEqual(item["address"], row["Address"])
                self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))

    def test_inventory_and_utility_corrections(self):
        expected = {"curlew-lake-state-park":"53", "steamboat-rock-state-park":"280",
                    "sun-lakes-dry-falls-state-park":"137", "lake-chelan-state-park":"144",
                    "twenty-five-mile-creek-state-park":"36", "riverside-state-park":"31",
                    "yakima-sportsman-state-park":"74", "bridgeport-state-park":"34"}
        for slug, count in expected.items():
            self.assertEqual(count, self.rows[slug]["Number of RV campsites"])
        self.assertEqual("3", self.rows["curlew-lake-state-park"]["Hookups"])
        self.assertEqual("3", self.rows["twenty-five-mile-creek-state-park"]["Hookups"])
        self.assertEqual("3", self.rows["riverside-state-park"]["Hookups"])

    def test_location_and_claim_corrections(self):
        riverside = self.rows["riverside-state-park"]
        self.assertIn("Bowl and Pitcher", riverside["Short Description"])
        self.assertEqual("named campground point", riverside["Coordinate precision"])
        self.assertEqual("4427 N Aubrey L White Parkway, Spokane, WA 99205", riverside["Address"])
        self.assertNotIn("golf", self.rows["bridgeport-state-park"]["Short Description"].lower())
        self.assertIn("scheduled through late 2027", self.rows["yakima-sportsman-state-park"]["Access note"])
        self.assertGreaterEqual(int(self.rows["curlew-lake-state-park"]["Drive Time Minutes"]), 318)

    def test_generated_pages_render_batch_facts(self):
        steamboat = (HERE.parent / "campground" / "steamboat-rock-state-park.html").read_text(encoding="utf-8")
        riverside = (HERE.parent / "campground" / "riverside-state-park.html").read_text(encoding="utf-8")
        self.assertIn('<div class="stat-val">280</div>', steamboat)
        self.assertIn("70 primitive campsites", steamboat)
        self.assertIn('<div class="stat-val">31</div>', riverside)
        self.assertIn("Bowl and Pitcher campground", riverside)

if __name__ == "__main__":
    unittest.main()
