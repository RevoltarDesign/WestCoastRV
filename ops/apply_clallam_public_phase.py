#!/usr/bin/env python3
"""Publish the reviewed Clallam County public-campground phase."""
import csv, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
MASTER=HERE/'data/campgrounds.csv'; EVIDENCE=HERE/'verification-evidence.json'; COVERAGE=HERE/'coverage-inventory.json'
REVIEWS=HERE/'clallam-public-location-reviews.json'; CHECKED='2026-09-11'
DNR='https://dnr.wa.gov/forest-and-trust-lands/olympic-peninsula-forests'
DNR_STATUS='https://dnr.wa.gov/recreation/find-your-campsite'
NPS='https://www.nps.gov/olym/planyourvisit/camping.htm'
COUNTY='https://www.clallamcountywa.gov/Facilities'
STATE='https://parks.wa.gov/find-parks/state-parks'

NEW={
 'bear-creek-campground': dict(Name='Bear Creek Campground', Park='State Forest', sites='16', length='30', hookups='0', lat=48.0656333, lon=-124.2407638,
  short='Sixteen-site first-come DNR campground beside the Sol Duc River, with dry sites for trailers up to 30 feet and direct access from US 101.',
  long='Bear Creek is a 16-site Washington DNR campground beside the Sol Duc River west of Lake Crescent. DNR allows trailers up to 30 feet and provides two toilets, but no hookups, showers, potable water, or dump station. Sites are first-come and a Discover Pass is required for vehicle access. DNR lists a seasonal closure from September 15, 2026 through April 15, 2027, so confirm status before travel.',
  reservation='First-come, first-served; scheduled closure September 15, 2026–April 15, 2027', town='Forks, WA', surface='Dirt', toilets='Vaulted toilets', water='false', showers='false', dump='false', maneuver='2', cell='0',
  access='Directly off the south side of US 101 near milepost 206. Confirm the scheduled winter closure before travel.', nearby='lyre-river-campground;sadie-creek-campground;fairholme-campground;sol-duc-campground'),
 'lyre-river-campground': dict(Name='Lyre River Campground', Park='State Forest', sites='11', length='20', hookups='0', lat=48.1500240, lon=-123.8328907,
  short='Eleven-site first-come DNR campground beside the Lyre River with potable water and dry sites for trailers up to 20 feet.',
  long='Lyre River is an 11-site Washington DNR campground on the river north of Lake Crescent. DNR allows trailers up to 20 feet and provides potable water, two toilets, and a picnic shelter. There are no hookups, showers, or dump station. Sites are first-come and a Discover Pass is required. DNR lists a seasonal closure from September 15, 2026 through April 15, 2027.',
  reservation='First-come, first-served; scheduled closure September 15, 2026–April 15, 2027', town='Port Angeles, WA', surface='Dirt', toilets='Vaulted toilets', water='true', showers='false', dump='false', maneuver='2', cell='0',
  access='From SR 112 between mileposts 46 and 47, follow the paved access road about 0.4 mile and turn left into the campground.', nearby='sadie-creek-campground;bear-creek-campground;log-cabin-resort-rv-campground;fairholme-campground'),
 'sadie-creek-campground': dict(Name='Sadie Creek Campground', Park='State Forest', sites='6', length='30', hookups='0', lat=48.1340580, lon=-123.9062550,
  short='Six-site first-come DNR campground serving the Sadie Creek trail system, with primitive dry sites for trailers up to 30 feet.',
  long='Sadie Creek is a six-site Washington DNR campground at a 30-mile multi-use trail system west of Lake Crescent. DNR allows trailers up to 30 feet. Camping is first-come with a Discover Pass required; there are no hookups, showers, potable water, or dump station. The main gravel road is shared with active timber traffic, and trail closures can change with forest operations.',
  reservation='First-come, first-served', town='Port Angeles, WA', surface='Dirt', toilets='Vaulted toilets', water='false', showers='false', dump='false', maneuver='2', cell='0',
  access='From SR 112 between mileposts 42 and 43, go south on East Twin River Road about 0.1 mile. Expect active logging traffic on the gravel road.', nearby='lyre-river-campground;bear-creek-campground;log-cabin-resort-rv-campground;fairholme-campground'),
 'log-cabin-resort-rv-campground': dict(Name='Log Cabin Resort RV & Campground', Park='National Park', sites='31', length='35', hookups='3', lat=48.0938949, lon=-123.7886940,
  short='Concession-operated Lake Crescent campground with 31 RV sites, full hookups, showers, laundry, and space for rigs up to 35 feet.',
  long='Log Cabin Resort operates a seasonal campground on the north shore of Lake Crescent inside Olympic National Park. The current NPS inventory lists 38 total campsites; the concession record identifies 31 RV sites and seven tent sites. RV sites accept rigs up to 35 feet and offer full hookups. Flush toilets, showers, potable water, laundry, and a dump station are available. Call the operator to reserve and confirm the exact assigned pad.',
  reservation='Call 866-405-2950; open May–October 2026', town='Port Angeles, WA', surface='Gravel', toilets='Flush toilets', water='true', showers='true', dump='true', maneuver='1', cell='1',
  access='From US 101, take East Beach Road about three miles and turn left at the Log Cabin Resort sign.', nearby='fairholme-campground;lyre-river-campground;sadie-creek-campground;sol-duc-campground'),
}

def duration(m):
 h,mm=divmod(m,60); return f'~{h} hr {mm} min from Seattle' if mm else f'~{h} hr from Seattle'
def source(url,publisher,family,evidence): return {'url':url,'publisher':publisher,'source_family':family,'evidence':evidence}

def main():
 reviews={r['slug']:r for r in json.loads(REVIEWS.read_text())['reviews']}
 with MASTER.open(newline='',encoding='utf-8-sig') as f: reader=csv.DictReader(f); fields=list(reader.fieldnames or []); rows=list(reader)
 by={r['Slug']:r for r in rows}
 for slug,c in NEW.items():
  row=by.get(slug,{k:'' for k in fields}); rev=reviews[slug]; m=rev['display_minutes']
  row.update({'Name':c['Name'],'Slug':slug,'Data last updated':CHECKED,'Archived':'false','Draft':'false','Topographic background image':f'https://westcoastrvcamping.com/assets/images/topo/{slug}.jpg','Short Description':c['short'],'Park Type':c['Park'],'Reservation window':c['reservation'],'Reservation website':DNR if c['Park']=='State Forest' else NPS,'Long description':c['long'],'Time from Seattle':duration(m),'Drive Time Band':'3-4hrs','Drive Time Minutes':str(m),'Address':rev['address'],'Number of RV campsites':c['sites'],'Max RV length':c['length'],'Maneuverability':c['maneuver'],'Site surface type':c['surface'],'Hookups':c['hookups'],'Dump station on site':c['dump'],'Generator policy':'','Cell coverage':c['cell'],'Things to do for families':'Explore nearby trails\nWatch the river or lake from camp\nLook for birds and wildlife\nPlan a Lake Crescent day trip\nPractice leave-no-trace camping','Things to do for families summary':'A practical base for Lake Crescent, river scenery, nearby trails, and Olympic Peninsula day trips.','Nearby nature & parks':'These campgrounds sit around Lake Crescent and the north Olympic Peninsula, close to Olympic National Park forests, rivers, and the Strait of Juan de Fuca.','Hiking':'true','Fishing':'true','Swimming':'true' if slug=='log-cabin-resort-rv-campground' else 'false','Kayaking/Paddling':'true' if slug=='log-cabin-resort-rv-campground' else 'false','Beach & Tide Pools':'false','Boating':'true' if slug=='log-cabin-resort-rv-campground' else 'false','Playground':'false','Amenities: Toilets':c['toilets'],'Amenities: Showers':c['showers'],'Amenities: Drinking water':c['water'],'Amenities: Fire pits':'true','Amenities summary':'See the verified facility details above and confirm seasonal restrictions with the operator before travel.','Nearest town':c['town'],'Site Recommendations':'Confirm operating status and the exact site fit before towing. Primitive DNR sites require self-contained camping supplies.','Google Maps Link':f"https://www.google.com/maps?q={rev['latitude']:.7f},{rev['longitude']:.7f}",'State Map':f'/assets/images/svg/{slug}.svg','RV Access':'yes','Access note':c['access'],'Access source':DNR if c['Park']=='State Forest' else NPS,'Access checked':CHECKED,'Latitude':f"{rev['latitude']:.7f}",'Longitude':f"{rev['longitude']:.7f}",'Coordinates source':rev['coordinate_source'],'Coordinates checked':CHECKED,'Coordinate precision':rev['precision'],'Drive distance miles':str(rev['distance_miles']),'Drive route minutes':str(rev['observed_route_minutes']),'Drive time origin':'Seattle, Washington','Drive time source':f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={rev['latitude']:.7f},{rev['longitude']:.7f}&travelmode=driving",'Drive time checked':CHECKED,'Drive time note':rev['route_note'],'Nearby campgrounds':c['nearby']})
  if slug not in by: rows.append(row)
  by[slug]=row

 # Existing-record corrections found during the Clallam scrub.
 by['fairholme-campground'].update({'Data last updated':CHECKED,'Number of RV campsites':'69','Access note':'The current reservation inventory identifies drive-in standard sites 1–69; remaining numbered spaces are walk-in. Most drive-in sites fit 21-foot equipment and selected sites fit up to 35 feet.'})
 by['sequim-bay-state-park'].update({'Data last updated':CHECKED,'Number of RV campsites':'60','RV Access':'yes','Access note':'The official brochure lists 45 standard and 15 full-hookup campsites, with selected sites for rigs up to 40 feet. Lower Loop is closed for restroom construction; reopening is TBD.'})
 by['dungeness-recreation-area'].update({'Data last updated':CHECKED,'Dump station on site':'true','Amenities: Toilets':'Flush toilets','RV Access':'yes','Access note':'All 66 main-loop campsites accept tents or recreational vehicles; individual pad measurements vary. Sites 1–24 are first-come and sites 25–66 are reservable.','Access source':'https://clallamcountywa.gov/facilities/facility/details/Dungeness-Recreation-Area-2','Access checked':CHECKED})
 by['salt-creek-recreation-area'].update({'Data last updated':CHECKED,'Amenities: Toilets':'Flush toilets','RV Access':'yes','Access note':'Sites 1–39 have electricity and seasonal water; sites 40–92 have no hookups. Both reservable and first-come sites are available; check the individual pad before booking.','Access source':'https://www.clallamcountywa.gov/Facilities/Facility/Details/Salt-Creek-Recreation-Area-26','Access checked':CHECKED,'Nearby campgrounds':'crescent-beach-rv-park;heart-o-the-hills-campground;lyre-river-campground;dungeness-recreation-area'})
 rev=reviews['bogachiel-state-park']; by['bogachiel-state-park'].update({'Data last updated':CHECKED,'RV Access':'yes','Access note':'The park offers standard and partial-hookup sites for RVs and combinations up to 40 feet.','Access source':'https://parks.wa.gov/find-parks/state-parks/bogachiel-state-park','Access checked':CHECKED,'Latitude':f"{rev['latitude']:.7f}",'Longitude':f"{rev['longitude']:.7f}",'Google Maps Link':f"https://www.google.com/maps?q={rev['latitude']:.7f},{rev['longitude']:.7f}",'Coordinates source':rev['coordinate_source'],'Coordinates checked':CHECKED,'Coordinate precision':rev['precision'],'Nearby campgrounds':'forks-101-rv-park;hard-rain-cafe-campground;mora-campground;bear-creek-campground'})
 with MASTER.open('w',newline='',encoding='utf-8') as f: w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)

 coverage=json.loads(COVERAGE.read_text()); coverage['updated_on']=CHECKED
 sections=[
  {'id':'clallam-dnr','county':'Clallam','operator_layer':'Washington DNR','status':'complete','inventory_sources':[DNR_STATUS,DNR],'candidates':[{'name':NEW[s]['Name'],'slug':s,'decision':'included_new','reason':'Current DNR inventory and official regional page confirm drive-in RV access.'} for s in ('bear-creek-campground','lyre-river-campground','sadie-creek-campground')]},
  {'id':'clallam-federal','county':'Clallam','operator_layer':'federal','status':'complete','inventory_sources':[NPS],'candidates':[
   *[{'name':by[s]['Name'],'slug':s,'decision':'included_existing','reason':'Current NPS inventory confirms RV access and operating details.'} for s in ('fairholme-campground','heart-o-the-hills-campground','mora-campground','ozette-campground','sol-duc-campground')],
   {'name':NEW['log-cabin-resort-rv-campground']['Name'],'slug':'log-cabin-resort-rv-campground','decision':'included_new','reason':'Current NPS concession inventory confirms 31 RV sites and access up to 35 feet.'},
   {'name':'Deer Park Campground','decision':'excluded','reason':'NPS explicitly lists tents only and says the access road is unsuitable for RVs or trailers.'}]},
  {'id':'clallam-county','county':'Clallam','operator_layer':'county','status':'complete','inventory_sources':[COUNTY],'candidates':[{'name':'Dungeness Recreation Area','slug':'dungeness-recreation-area','decision':'included_existing','reason':'County inventory confirms 66 drive-in campsites for tents and RVs.'},{'name':'Salt Creek Recreation Area','slug':'salt-creek-recreation-area','decision':'included_existing','reason':'County inventory confirms 92 utility and nonutility RV campsites.'}]},
  {'id':'clallam-state-parks','county':'Clallam','operator_layer':'state_parks','status':'complete','inventory_sources':[STATE],'candidates':[{'name':'Bogachiel State Park','slug':'bogachiel-state-park','decision':'included_existing','reason':'Current park page confirms standard and partial-hookup RV camping.'},{'name':'Sequim Bay State Park','slug':'sequim-bay-state-park','decision':'included_existing','reason':'Current park page and brochure confirm standard and full-hookup camping.'}]},
  {'id':'clallam-private-tribal','county':'Clallam','operator_layer':'private_tribal','status':'in_progress','inventory_sources':['https://www.clallamcountywa.gov/Facilities'],'candidates':[]}
 ]
 # Python syntax cannot splat an empty list into a dict; populate the active private queue explicitly.
 sections[-1]['candidates']=[{'name':by[s]['Name'],'slug':s,'decision':'included_existing','reason':'Existing public record retained for the private/tribal verification queue.'} for s in ('elwha-dam-rv-park','forks-101-rv-park','crescent-beach-rv-park','gilgal-oasis-rv-park')]
 sections[-1]['candidates'] += [{'name':'Private and tribal operator inventory','decision':'research','reason':'Full operator-by-operator inventory is the next Clallam layer.'}]
 for section in sections:
  old=next((x for x in coverage['sections'] if x['id']==section['id']),None)
  if old: old.update(section)
  else: coverage['sections'].append(section)
 COVERAGE.write_text(json.dumps(coverage,indent=2)+'\n')

 evidence=json.loads(EVIDENCE.read_text()); affected=set(NEW)|{'fairholme-campground','sequim-bay-state-park','dungeness-recreation-area','salt-creek-recreation-area','bogachiel-state-park'}
 evidence['observations']=[o for o in evidence['observations'] if not (o.get('slug') in affected and o.get('source_family')=='clallam-public-review')]
 dnr_sources=[source(DNR_STATUS,'Washington Department of Natural Resources','clallam-public-review','Current inventory supports operating status and county.'),source(DNR,'Washington Department of Natural Resources','clallam-public-review','Official regional page supports directions, facilities, first-come use, and RV limits.')]
 nps_sources=[source(NPS,'National Park Service','clallam-public-review','Current campground inventory supports status, reservation method, site inventory, RV limits, and facilities.')]
 for slug,c in NEW.items():
  sources=dnr_sources if c['Park']=='State Forest' else nps_sources
  for field,value in {'operating_status':'current operator status','rv_access':True,'reservation_method':c['reservation'],'max_rv_length':int(c['length']),'hookups':int(c['hookups'])}.items(): evidence['observations'].append({'slug':slug,'field':field,'status':'supported','checked_on':CHECKED,'summary':f'Current official sources support {field.replace("_"," ")}.','proposed_value':value,'source_family':'clallam-public-review','sources':sources})
 corrections={
  'fairholme-campground':('rv_site_count',69,nps_sources),
  'sequim-bay-state-park':('rv_site_count',60,[source('https://parks.wa.gov/sites/default/files/2023-03/SequimBay_Brochure_03.22.2023.pdf','Washington State Parks','clallam-public-review','Official brochure lists 45 standard and 15 full-hookup campsites.')]),
  'dungeness-recreation-area':('facilities','flush toilets, showers, water and dump station',[source('https://clallamcountywa.gov/facilities/facility/details/Dungeness-Recreation-Area-2','Clallam County','clallam-public-review','Current county page confirms the campground inventory and facilities.')]),
  'salt-creek-recreation-area':('facilities','flush toilets, showers, seasonal water and dump station',[source('https://www.clallamcountywa.gov/Facilities/Facility/Details/Salt-Creek-Recreation-Area-26','Clallam County','clallam-public-review','Current county page confirms the campground inventory and facilities.')]),
  'bogachiel-state-park':('coordinates','47.8963623,-124.3605957',[source('https://parks.wa.gov/find-parks/state-parks/bogachiel-state-park','Washington State Parks','clallam-public-review','Current park page publishes the locate point.')])}
 for slug,(field,value,sources) in corrections.items(): evidence['observations'].append({'slug':slug,'field':field,'status':'corrected_locally','checked_on':CHECKED,'summary':f'Clallam public review corrected {field.replace("_"," ")}.','proposed_value':value,'source_family':'clallam-public-review','sources':sources})
 EVIDENCE.write_text(json.dumps(evidence,indent=2)+'\n')
 print(f'Completed Clallam public phase; dataset now contains {len(rows)} records and five grouped existing-record corrections.')

if __name__=='__main__': main()
