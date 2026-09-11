import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
SLUGS = {"coppermine-bottom-campground","cottonwood-campground","hoh-oxbow-campground","minnie-peterson-campground","south-fork-hoh-campground"}

class JeffersonDnrPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data/campgrounds.csv").open(newline="",encoding="utf-8-sig") as f:
            cls.rows={r["Slug"]:r for r in csv.DictReader(f)}

    def test_five_dnr_campgrounds_are_published_with_reviewed_trip_data(self):
        for slug in SLUGS:
            row=self.rows[slug]
            self.assertEqual("false",row["Draft"])
            self.assertEqual("State Forest",row["Park Type"])
            self.assertEqual("yes",row["RV Access"])
            self.assertEqual("30",row["Max RV length"])
            self.assertEqual("0",row["Hookups"])
            self.assertEqual("named campground point",row["Coordinate precision"])
            self.assertGreaterEqual(int(row["Drive Time Minutes"]),int(row["Drive route minutes"]))

    def test_dnr_inventory_decisions_are_complete(self):
        coverage=json.loads((HERE/"coverage-inventory.json").read_text())
        section=next(s for s in coverage["sections"] if s["id"]=="jefferson-dnr")
        self.assertEqual("complete",section["status"])
        self.assertEqual(7,len(section["candidates"]))
        self.assertEqual("deferred",next(c for c in section["candidates"] if c["name"].startswith("Upper Clearwater"))["decision"])
        self.assertEqual("excluded",next(c for c in section["candidates"] if c["name"].startswith("Yahoo Lake"))["decision"])

    def test_assets_pages_filters_and_guide(self):
        self.assertEqual(22,(SITE/"field-notes/jefferson-county-rv-camping.html").read_text().count('<article class="camp">'))
        self.assertIn('data-type="state-forest"',(SITE/"campgrounds.html").read_text())
        self.assertIn('data-type="State Forest"',(SITE/"map.html").read_text())
        for slug in SLUGS:
            self.assertTrue((SITE/f"assets/images/topo/{slug}.jpg").is_file())
            self.assertTrue((SITE/f"assets/images/svg/{slug}.svg").is_file())
            page=(SITE/f"campground/{slug}.html").read_text()
            self.assertIn("Jefferson County RV camping guide",page)

if __name__ == "__main__": unittest.main()
