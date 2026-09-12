import csv, json, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent; SITE=HERE.parent
ALL={'flowing-lake-county-park','kayak-point-regional-park','wenberg-county-park','river-meadows-county-park','squire-creek-park-campground','whitehorse-campground','evergreen-state-fairgrounds-rv-2'}
NEW={'river-meadows-county-park','squire-creek-park-campground','whitehorse-campground','evergreen-state-fairgrounds-rv-2'}

class SnohomishCountyPhaseTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with (HERE/'data/campgrounds.csv').open(newline='',encoding='utf-8-sig') as f: cls.rows={r['Slug']:r for r in csv.DictReader(f)}
 def test_records_are_publishable_sourced_and_generated(self):
  for slug in ALL:
   r=self.rows[slug]
   self.assertEqual('false',r['Draft']); self.assertEqual('yes',r['RV Access'])
   self.assertTrue(r['Coordinates source']); self.assertTrue(r['Access source'])
   self.assertGreaterEqual(int(r['Drive Time Minutes']),int(r['Drive route minutes']))
   self.assertTrue((SITE/f'assets/images/topo/{slug}.jpg').is_file())
   self.assertTrue((SITE/f'assets/images/svg/{slug}.svg').is_file())
   self.assertIn('Snohomish County RV camping guide',(SITE/f'campground/{slug}.html').read_text())
 def test_conservative_corrections_remain(self):
  self.assertEqual('39',self.rows['flowing-lake-county-park']['Number of RV campsites'])
  self.assertEqual('',self.rows['flowing-lake-county-park']['Max RV length'])
  self.assertEqual('false',self.rows['kayak-point-regional-park']['Dump station on site'])
  self.assertIn('300-foot',self.rows['kayak-point-regional-park']['Long description'])
  self.assertIn('east shore',self.rows['wenberg-county-park']['Long description'])
  self.assertEqual('',self.rows['wenberg-county-park']['Max RV length'])
 def test_inventory_guide_and_public_surfaces(self):
  coverage=json.loads((HERE/'coverage-inventory.json').read_text()); section=next(s for s in coverage['sections'] if s['id']=='snohomish-county')
  self.assertEqual('complete',section['status']); self.assertEqual(2,sum(c['decision']=='excluded' for c in section['candidates']))
  guide=(SITE/'field-notes/snohomish-county-rv-camping.html').read_text(); self.assertEqual(7,guide.count('<article class="camp">'))
  for slug in NEW:
   for path in ('campgrounds.html','map.html','sitemap.xml'): self.assertIn(slug,(SITE/path).read_text())

if __name__=='__main__': unittest.main()
