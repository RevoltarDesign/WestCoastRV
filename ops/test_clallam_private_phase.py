import csv, json, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent; SITE=HERE.parent
NEW={'quileute-oceanside-resort-rv-camping','hobuck-beach-resort-rv-camping','cape-resort-rv-park','masons-resort-sekiu','anglers-hideaway-rv-park','three-rivers-resort-rv-camping'}

class ClallamPrivatePhaseTests(unittest.TestCase):
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
 def test_existing_claims_are_conservative(self):
  self.assertEqual('',self.rows['elwha-dam-rv-park']['Number of RV campsites'])
  self.assertEqual('48.0978590',self.rows['elwha-dam-rv-park']['Latitude'])
  self.assertEqual('',self.rows['forks-101-rv-park']['Max RV length'])
  self.assertNotIn('May through October',self.rows['forks-101-rv-park']['Long description'])
  self.assertEqual('',self.rows['crescent-beach-rv-park']['Number of RV campsites'])
  self.assertEqual('',self.rows['gilgal-oasis-rv-park']['Max RV length'])
  self.assertNotIn('all within a mile',self.rows['gilgal-oasis-rv-park']['Long description'])
  self.assertEqual('',self.rows['cape-resort-rv-park']['Max RV length'])
 def test_tribal_type_is_supported_across_discovery_surfaces(self):
  directory=(SITE/'campgrounds.html').read_text(); map_page=(SITE/'map.html').read_text()
  self.assertIn('data-type="tribal"',directory)
  self.assertIn("'Tribal Campground':",map_page)
  for slug in {'quileute-oceanside-resort-rv-camping','hobuck-beach-resort-rv-camping','cape-resort-rv-park'}:
   self.assertEqual('Tribal Campground',self.rows[slug]['Park Type'])
 def test_coverage_records_include_defer_and_exclude_decisions(self):
  coverage=json.loads((HERE/'coverage-inventory.json').read_text())
  section=next(s for s in coverage['sections'] if s['id']=='clallam-private-tribal')
  self.assertEqual('complete',section['status'])
  decisions=[c['decision'] for c in section['candidates']]
  self.assertEqual(6,decisions.count('included_new'))
  self.assertIn('deferred',decisions); self.assertIn('excluded',decisions)
 def test_guide_has_all_clallam_records(self):
  guide=(SITE/'field-notes/clallam-county-rv-camping.html').read_text()
  self.assertEqual(23,guide.count('<article class="camp">'))
  for slug in NEW: self.assertIn(f'/campground/{slug}',guide)

if __name__=='__main__': unittest.main()
