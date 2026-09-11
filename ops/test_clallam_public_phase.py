import csv, json, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent; SITE=HERE.parent
NEW={'bear-creek-campground','lyre-river-campground','sadie-creek-campground','log-cabin-resort-rv-campground'}

class ClallamPublicPhaseTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with (HERE/'data/campgrounds.csv').open(newline='',encoding='utf-8-sig') as f: cls.rows={r['Slug']:r for r in csv.DictReader(f)}
 def test_new_records_are_publishable_and_sourced(self):
  for slug in NEW:
   r=self.rows[slug]
   self.assertEqual('false',r['Draft']); self.assertEqual('yes',r['RV Access'])
   self.assertTrue(r['Coordinates source']); self.assertTrue(r['Access source'])
   self.assertGreaterEqual(int(r['Drive Time Minutes']),int(r['Drive route minutes']))
   self.assertTrue((SITE/f'assets/images/topo/{slug}.jpg').is_file())
   self.assertTrue((SITE/f'assets/images/svg/{slug}.svg').is_file())
   self.assertIn('Clallam County RV camping guide',(SITE/f'campground/{slug}.html').read_text())
 def test_existing_corrections_remain(self):
  self.assertEqual('69',self.rows['fairholme-campground']['Number of RV campsites'])
  self.assertEqual('60',self.rows['sequim-bay-state-park']['Number of RV campsites'])
  self.assertEqual('true',self.rows['dungeness-recreation-area']['Dump station on site'])
  self.assertEqual('Flush toilets',self.rows['salt-creek-recreation-area']['Amenities: Toilets'])
  self.assertEqual('47.8963623',self.rows['bogachiel-state-park']['Latitude'])
 def test_coverage_and_guide(self):
  coverage=json.loads((HERE/'coverage-inventory.json').read_text())
  sections={s['id']:s for s in coverage['sections']}
  for key in ('clallam-dnr','clallam-federal','clallam-county','clallam-state-parks'): self.assertEqual('complete',sections[key]['status'])
  self.assertEqual('in_progress',sections['clallam-private-tribal']['status'])
  guide=(SITE/'field-notes/clallam-county-rv-camping.html').read_text()
  self.assertEqual(17,guide.count('<article class="camp">'))
  self.assertIn('clallam-county-rv-camping',(SITE/'sitemap.xml').read_text())
 def test_measurement_events(self):
  nav=(SITE/'assets/nav.js').read_text(); map_page=(SITE/'map.html').read_text()
  for event in ('campground_open','campground_outbound','directions_click'): self.assertIn(event,nav)
  for event in ('campground_open','directions_click','map_filter'): self.assertIn(event,map_page)

if __name__=='__main__': unittest.main()
