import csv, json, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

class HoodCanalPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}
        cls.reviews = json.loads((HERE / "hood-canal-location-reviews.json").read_text(encoding="utf-8"))["reviews"]

    def test_reviewed_locations_and_routes_match(self):
        self.assertEqual(6, len(self.reviews))
        for item in self.reviews:
            with self.subTest(slug=item["slug"]):
                row = self.rows[item["slug"]]
                self.assertAlmostEqual(item["latitude"], float(row["Latitude"]), places=6)
                self.assertAlmostEqual(item["longitude"], float(row["Longitude"]), places=6)
                self.assertEqual(item["address"], row["Address"])
                self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))
                self.assertEqual("Seattle, Washington", row["Drive time origin"])

    def test_corrected_public_facts(self):
        self.assertEqual("40", self.rows["sequim-bay-state-park"]["Max RV length"])
        self.assertIn("Lower Loop", self.rows["sequim-bay-state-park"]["Reservation window"])
        self.assertEqual("80", self.rows["fort-worden-historical-state-park"]["Number of RV campsites"])
        self.assertEqual("73", self.rows["potlatch-state-park"]["Number of RV campsites"])
        self.assertNotIn("campground is closed", self.rows["twanoh-state-park"]["Long description"].lower())
        self.assertEqual("false", self.rows["twanoh-state-park"]["Dump station on site"])
        self.assertEqual("3151 NE State Route 300, Belfair, WA 98528", self.rows["belfair-state-park"]["Address"])
        self.assertEqual("12", self.rows["jarrell-cove-state-park"]["Number of RV campsites"])
        self.assertEqual("false", self.rows["jarrell-cove-state-park"]["Dump station on site"])

if __name__ == "__main__": unittest.main()
