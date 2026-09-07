import csv, json, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

class NorthSoundPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}
        cls.reviews = json.loads((HERE / "north-sound-location-reviews.json").read_text(encoding="utf-8"))["reviews"]

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
        self.assertEqual("2", self.rows["larrabee-state-park"]["Hookups"])
        self.assertNotIn("full hookups", self.rows["larrabee-state-park"]["Long description"].lower())
        self.assertEqual("167", self.rows["birch-bay-state-park"]["Number of RV campsites"])
        self.assertEqual("77", self.rows["camano-island-state-park"]["Number of RV campsites"])
        self.assertEqual("false", self.rows["fort-casey-historical-state-park"]["Dump station on site"])
        self.assertIn("September 15, 2026", self.rows["fort-casey-historical-state-park"]["Reservation window"])

if __name__ == "__main__": unittest.main()
