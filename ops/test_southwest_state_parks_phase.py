import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

class SouthwestStateParksPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}
        cls.reviews = json.loads((HERE / "southwest-state-parks-location-reviews.json").read_text(encoding="utf-8"))["reviews"]

    def test_reviewed_locations_and_routes_match(self):
        self.assertEqual(12, len(self.reviews))
        for item in self.reviews:
            with self.subTest(slug=item["slug"]):
                row = self.rows[item["slug"]]
                self.assertAlmostEqual(item["latitude"], float(row["Latitude"]), places=6)
                self.assertAlmostEqual(item["longitude"], float(row["Longitude"]), places=6)
                self.assertEqual(item["address"], row["Address"])
                self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))
                self.assertEqual("Seattle, Washington", row["Drive time origin"])

    def test_high_impact_status_and_inventory_corrections(self):
        self.assertIn("currently closed", self.rows["saltwater-state-park"]["Short Description"])
        self.assertEqual("unknown", self.rows["saltwater-state-park"]["RV Access"])
        self.assertTrue(self.rows["saltwater-state-park"]["Reservation window"].startswith("Closed"))
        self.assertNotIn("Sites 1–25", self.rows["saltwater-state-park"]["Site Recommendations"])
        self.assertIn("campground amenities are unavailable", self.rows["saltwater-state-park"]["Amenities summary"])
        self.assertEqual("138", self.rows["dash-point-state-park"]["Number of RV campsites"])
        self.assertEqual("68", self.rows["schafer-state-park"]["Number of RV campsites"])
        self.assertEqual("32", self.rows["lewis-and-clark-state-park"]["Number of RV campsites"])
        self.assertEqual("31", self.rows["battle-ground-lake-state-park"]["Number of RV campsites"])
        self.assertEqual("32", self.rows["beacon-rock-state-park"]["Number of RV campsites"])
        self.assertEqual("138", self.rows["millersylvania-state-park"]["Number of RV campsites"])
        self.assertEqual("101", self.rows["ike-kinswa-state-park"]["Number of RV campsites"])
        self.assertIn("Mayfield Lake", self.rows["ike-kinswa-state-park"]["Long description"])
        self.assertNotIn("Riffe Lake", self.rows["ike-kinswa-state-park"]["Long description"])

    def test_facility_and_access_corrections(self):
        self.assertEqual("true", self.rows["dash-point-state-park"]["Amenities: Showers"])
        self.assertEqual("true", self.rows["seaquest-state-park"]["Amenities: Showers"])
        self.assertEqual("false", self.rows["lewis-and-clark-state-park"]["Dump station on site"])
        self.assertEqual("named campground point", self.rows["dash-point-state-park"]["Coordinate precision"])
        self.assertEqual("named campground point", self.rows["beacon-rock-state-park"]["Coordinate precision"])
        self.assertIn("no-ferry", self.rows["illahee-state-park"]["Drive time note"])

    def test_closed_page_and_stat_copy_render_cleanly(self):
        html = (HERE.parent / "campground" / "saltwater-state-park.html").read_text(encoding="utf-8")
        self.assertIn('<div class="stat-val">Closed</div>', html)
        self.assertIn('<div class="stat-note">Check limits by site</div>', html)
        self.assertIn("Closure details", html)

if __name__ == "__main__":
    unittest.main()
