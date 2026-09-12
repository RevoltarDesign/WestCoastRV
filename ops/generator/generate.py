#!/usr/bin/env python3
"""
WA RV Camping — Campground Page Generator
==========================================
Reads:  Scripts/campground-template.html
        Data/Washington RV Camping - Campgrounds - ALL CAMPGROUNDS (Master).csv
Writes: site/campground/{slug}.html  (110 pages)

Usage:
  python3 Scripts/generate.py                     # all 110 pages
  python3 Scripts/generate.py --slug fairholme-campground   # single page
  python3 Scripts/generate.py --dry-run           # validate without writing
"""

import csv, re, html as htmllib, os, json, sys
from pathlib import Path
from urllib.parse import urlsplit

# ── Paths ──────────────────────────────────────────────────────────────────────
SITE_DIR      = Path(__file__).resolve().parents[2]
BASE_DIR      = SITE_DIR.parent
CSV_PATH      = SITE_DIR / "ops" / "data" / "campgrounds.csv"
TEMPLATE_PATH = Path(__file__).resolve().parent / "campground-template.html"
OUT_DIR       = SITE_DIR / "campground"

# ── Lookup tables ──────────────────────────────────────────────────────────────
HOOKUP_LABEL = {'0': 'None', '1': 'Electric', '2': 'Water + Electric', '3': 'Full Hookups'}
HOOKUP_NOTE  = {'0': 'dry camping',   '1': 'electric only',
                '2': 'water & electric', '3': 'full hookups'}

MANEUV_LABEL = {'1': 'Reported easy', '2': 'Reported moderate', '3': 'Reported challenging'}
MANEUV_NOTE  = {
    '1': 'Road and pad conditions vary by site',
    '2': 'Review the operator map for your loop',
    '3': 'Confirm the approach for your rig',
}

CELL_LABEL = {'0': 'Not confirmed', '1': 'Reported spotty', '2': 'Reported good'}
CELL_NOTE  = {'0': 'Check your carrier map', '1': 'Coverage varies by carrier', '2': 'Coverage varies by carrier'}

GEN_LABEL = {'0': 'Not allowed', '1': 'Restricted', '2': 'Allowed', '': 'Not confirmed'}
GEN_NOTE  = {'0': 'Operator prohibits generators', '1': 'Designated hours only',
             '2': 'No generator restrictions', '': 'Confirm with the operator'}

PARK_BADGE = {
    'National Forest': 'National Forest',
    'State Forest':       'State Forest',
    'National Park':      'National Park',
    'State Park':         'State Park',
    'County Campground':  'County Park',
    'City Campground':    'Municipal RV Park',
    'Private Campground': 'Private',
    'Tribal Campground':  'Tribal Campground',
}
PARK_FILTER = {
    'National Forest': 'forest',
    'State Forest':       'state-forest',
    'National Park':      'national',
    'State Park':         'state',
    'County Campground':  'county',
    'City Campground':    'city',
    'Private Campground': 'private',
    'Tribal Campground':  'tribal',
}
PASS_META = {
    'National Forest': 'Check the operator for camping and day-use fees',
    'State Forest':       'Discover Pass required for vehicle access; campsites are first-come with no separate camping fee',
    'National Park':      'Entrance passes generally do not cover camping fees',
    'State Park':         'Overnight guests do not need a Discover Pass at the park where they camp',
    'County Campground':  'Check park website for day-use fees',
    'City Campground':    'Check the operator for current rates and parking rules',
    'Private Campground': 'No pass required — rates vary by season',
    'Tribal Campground':  'Check the tribal operator for permits, current rates, and access rules',
}

ACTIVITY_DEFS = [
    ('Hiking',            '🥾', 'Hiking'),
    ('Fishing',           '🎣', 'Fishing'),
    ('Swimming',          '🏊', 'Swimming'),
    ('Kayaking/Paddling', '🚣', 'Kayaking'),
    ('Beach & Tide Pools','🏖️', 'Beach'),
    ('Boating',           '⛵', 'Boating'),
    ('Playground',        '🛝', 'Playground'),
]

NEARBY_ICONS = ['🌲', '🏕️', '⛰️', '🌊', '🌿', '🏞️']

SVG_CHECK = ('<svg class="tick" width="16" height="16" viewBox="0 0 16 16" fill="none" '
             'stroke="currentColor" stroke-width="2.2"><polyline points="2.5,8 6.5,12 13.5,4"/></svg>')
SVG_CROSS = ('<svg class="cross" width="16" height="16" viewBox="0 0 16 16" fill="none" '
             'stroke="currentColor" stroke-width="2"><line x1="4" y1="4" x2="12" y2="12"/>'
             '<line x1="12" y1="4" x2="4" y2="12"/></svg>')
SVG_ARROW = ('<svg class="nearby-camp-arrow" width="16" height="16" viewBox="0 0 16 16" '
             'fill="none" stroke="currentColor" stroke-width="2"><polyline points="6,3 11,8 6,13"/></svg>')

# ── Helpers ────────────────────────────────────────────────────────────────────
def h(s):
    return htmllib.escape(str(s)) if s else ''

def display_image(row):
    """One topographic asset per campground across cards, heroes and metadata."""
    relative = f"/assets/images/topo/{row['Slug']}.jpg"
    if not (BASE_DIR / 'site' / relative.lstrip('/')).is_file():
        raise ValueError(f"Missing topographic map: {relative}; run generate_topo.py first")
    return relative


def dots_html(on_count, total=3, color='green'):
    cls = {'green': 'on-green', 'warn': 'on-warn', 'danger': 'on-danger'}.get(color, 'on-green')
    parts = [f'<div class="dot {cls}"></div>' if i < on_count else '<div class="dot"></div>'
             for i in range(total)]
    return '\n          '.join(parts)

def maneuv_dots(level):
    if level == '1':   return dots_html(3, color='green')
    elif level == '2': return dots_html(2, color='warn')
    else:              return dots_html(1, color='danger')

def cell_dots(level):
    if level == '0': return dots_html(0)
    return dots_html(1, color='warn') if level == '1' else dots_html(2, color='green')

def gen_dots(level):
    return dots_html(int(level), color='warn') if level in {'0', '1', '2'} else dots_html(0)

def extract_lat_lng(maps_url, row=None):
    if row and row.get('Latitude') and row.get('Longitude'):
        return row['Latitude'].strip(), row['Longitude'].strip()
    m = re.search(r'(?:q=|query=)([-\d.]+),([-\d.]+)', maps_url or '')
    return (m.group(1), m.group(2)) if m else ('', '')

def directions_url(row):
    """Open turn-by-turn directions to the reviewed point from the visitor's location."""
    lat, lng = extract_lat_lng(row.get('Google Maps Link', ''), row)
    if lat and lng:
        return f'https://www.google.com/maps/dir/?api=1&destination={lat},{lng}&travelmode=driving'
    return row.get('Google Maps Link', '#')

def parse_address(addr):
    parts = [p.strip() for p in (addr or '').split(',')]
    if len(parts) >= 3:
        street = parts[0]
        city   = parts[1]
        sz     = parts[-1].strip().split()
        state  = sz[0] if sz else 'WA'
        postal = sz[1] if len(sz) > 1 else ''
        return street, city, state, postal
    return addr, '', 'WA', ''

def format_reservation_short(text):
    if not text: return 'FCFS'
    if re.search(r'^(campground\s+)?closed\b', text, re.I): return 'Closed'
    if re.search(r'opened January 1', text, re.I): return 'Jan. 1 release'
    m = re.search(r'(\d+)\s*month', text, re.I)
    if m: return f'{m.group(1)} mo.'
    if re.search(r'\breserv(?:e|able|ations?)\b', text, re.I): return 'Seasonal'
    if re.search(r'first.come', text, re.I): return 'FCFS'
    m = re.search(r'(\d+)\s*day', text, re.I)
    if m: return f'{m.group(1)} days'
    return text[:12]

def hookup_display(level):
    return HOOKUP_LABEL.get(level, 'Unknown'), HOOKUP_NOTE.get(level, ''), level != '0'

def true_val(s):
    return str(s).strip().lower() == 'true'

def optional_bool(s):
    value = str(s).strip().lower()
    if value == 'true': return True
    if value == 'false': return False
    return None

# ── HTML builders ──────────────────────────────────────────────────────────────
def build_activity_pills(row):
    lines = []
    for col, icon, label in ACTIVITY_DEFS:
        cls = 'act-on' if true_val(row.get(col, '')) else 'act-off'
        lines.append(f'      <span class="act-pill {cls}">{icon} {label}</span>')
    return '\n'.join(lines)

def build_activity_list(row):
    things = (row.get('Things to do for families') or '').strip()
    if not things:
        return '          <li>Ask the camp host for current activity recommendations</li>'
    items = [ln.strip() for ln in things.split('\n') if ln.strip()][:8]
    return '\n'.join(f'          <li>{h(item)}</li>' for item in items)

def build_amenities_grid(row):
    toilet_type = (row.get('Amenities: Toilets') or '').strip()
    has_toilet  = bool(toilet_type) and toilet_type.lower() != 'false'
    has_shower  = true_val(row.get('Amenities: Showers', ''))
    has_water   = true_val(row.get('Amenities: Drinking water', ''))
    has_fire    = true_val(row.get('Amenities: Fire pits', ''))

    def block(icon, name, has, label_on, label_off='Not available'):
        cls = 'on' if has else 'off'
        return (f'      <div class="amenity">\n'
                f'        <div class="amenity-icon {cls}">{icon}</div>\n'
                f'        <div>\n'
                f'          <div class="amenity-name">{name}</div>\n'
                f'          <div class="amenity-status {cls}">{label_on if has else label_off}</div>\n'
                f'        </div>\n'
                f'      </div>')

    return '\n'.join([
        block('🚻', 'Toilets',       has_toilet, toilet_type if has_toilet else 'Flush toilets'),
        block('🚿', 'Showers',       has_shower,  'Available'),
        block('💧', 'Drinking Water', has_water,   'Available'),
        block('🔥', 'Fire Pits',     has_fire,    'Listed as available'),
    ])

def build_specs_grid(row):
    maneuv = row.get('Maneuverability', '2')
    cell   = row.get('Cell coverage', '1')
    gen    = row.get('Generator policy', '1')
    surface = (row.get('Site surface type') or 'Mixed').strip()
    dump   = optional_bool(row.get('Dump station on site', ''))
    hookup_level = row.get('Hookups', '0')
    hookup_label, hookup_note_txt, has_hookup = hookup_display(hookup_level)

    if dump is True:
        dump_val = f'{SVG_CHECK}\n          On-site'
        dump_note = 'Confirm hours and access with the operator'
    elif dump is False:
        dump_val = f'{SVG_CROSS}\n          Not available'
        dump_note = 'Plan a separate dump stop'
    else:
        dump_val = 'Not confirmed'
        dump_note = 'Confirm with the operator'
    hook_val  = f'{SVG_CHECK}\n          {hookup_label}' if has_hookup else f'{SVG_CROSS}\n          {hookup_label}'
    hook_note = {'0': 'Bring full tanks',
                 '1': 'Electric service available',
                 '2': 'Water & electric at site',
                 '3': 'Full W+E+S hookups'}.get(hookup_level, '')

    return f'''      <div class="spec-cell">
        <div class="spec-label">Maneuverability</div>
        <div class="spec-val">{MANEUV_LABEL.get(maneuv, 'Moderate')}</div>
        <div class="dots">
          {maneuv_dots(maneuv)}
        </div>
        <div class="spec-note" style="margin-top:7px;">{MANEUV_NOTE.get(maneuv, '')}</div>
      </div>

      <div class="spec-cell">
        <div class="spec-label">Cell Coverage</div>
        <div class="spec-val">{CELL_LABEL.get(cell, 'Spotty')}</div>
        <div class="dots">
          {cell_dots(cell)}
        </div>
        <div class="spec-note" style="margin-top:7px;">{CELL_NOTE.get(cell, '')}</div>
      </div>

      <div class="spec-cell">
        <div class="spec-label">Generators</div>
        <div class="spec-val">{GEN_LABEL.get(gen, 'Restricted')}</div>
        <div class="dots">
          {gen_dots(gen)}
        </div>
        <div class="spec-note" style="margin-top:7px;">{GEN_NOTE.get(gen, '')}</div>
      </div>

      <div class="spec-cell">
        <div class="spec-label">Site Surface</div>
        <div class="spec-val">{h(surface)}</div>
        <div class="spec-note" style="margin-top:8px;">Check conditions at check-in</div>
      </div>

      <div class="spec-cell">
        <div class="spec-label">Dump Station</div>
        <div class="spec-val">
          {dump_val}
        </div>
        <div class="spec-note" style="margin-top:7px;">{dump_note}</div>
      </div>

      <div class="spec-cell">
        <div class="spec-label">Hookups</div>
        <div class="spec-val">
          {hook_val}
        </div>
        <div class="spec-note" style="margin-top:7px;">{hook_note}</div>
      </div>'''

def build_nearby_camps(row, slug_lookup):
    raw = (row.get('Nearby campgrounds') or '').strip()
    if not raw:
        return '<p style="color:var(--text-muted);font-size:14px;">Nearby campground data coming soon.</p>'
    slugs = [s.strip() for s in raw.split(';') if s.strip()][:4]
    links = []
    for i, slug in enumerate(slugs):
        nr = slug_lookup.get(slug)
        if not nr or nr.get('RV Access') == 'no': continue
        name      = nr.get('Name', slug)
        park_type = nr.get('Park Type', '')
        drive     = (nr.get('Time from Seattle') or '').replace(' from Seattle', '')
        icon      = NEARBY_ICONS[i % len(NEARBY_ICONS)]
        meta      = f'{park_type} · {drive}' if park_type else drive
        reason = nearby_reason(row, nr)
        links.append(
            f'          <a href="/campground/{slug}" class="nearby-camp-link">\n'
            f'            <div class="nearby-camp-icon">{icon}</div>\n'
            f'            <div class="nearby-camp-info">\n'
            f'              <div class="nearby-camp-name">{h(name)}</div>\n'
            f'              <div class="nearby-camp-meta">{h(meta)}</div>\n'
            f'              <div class="nearby-camp-reason">{h(reason)}</div>\n'
            f'            </div>\n'
            f'            {SVG_ARROW}\n'
            f'          </a>')
    return '\n'.join(links) if links else '<p style="color:var(--text-muted);font-size:14px;">More coming soon.</p>'


def nearby_reason(current, candidate):
    """Explain the practical difference behind each discovery link."""
    current_hookups = int(current.get('Hookups') or 0)
    candidate_hookups = int(candidate.get('Hookups') or 0)
    candidate_length = (candidate.get('Max RV length') or '').strip()
    candidate_town = (candidate.get('Nearest town') or '').strip()
    if candidate_hookups > current_hookups:
        return f'More services: {HOOKUP_LABEL.get(str(candidate_hookups), "hookups")}'
    if candidate_length:
        return f'Fits listed rigs up to {candidate_length} ft'
    if candidate.get('Park Type') == current.get('Park Type'):
        return f'Another {candidate.get("Park Type", "campground").lower()} option'
    if candidate_town:
        return f'Another option near {candidate_town}'
    return 'Compare this nearby camping option'


def build_regional_guide(row):
    snohomish = {
        'flowing-lake-county-park', 'kayak-point-regional-park',
        'wenberg-county-park', 'river-meadows-county-park',
        'squire-creek-park-campground', 'whitehorse-campground',
        'evergreen-state-fairgrounds-rv-2',
    }
    if row.get('Slug') in snohomish:
        return ('<a class="regional-guide-link" href="/field-notes/snohomish-county-rv-camping">'
                '<span>Snohomish County RV camping guide</span>'
                '<small>Compare 7 county-operated choices from Puget Sound to Darrington</small>'
                '</a>')
    clallam = {
        'fairholme-campground', 'heart-o-the-hills-campground', 'mora-campground',
        'ozette-campground', 'sol-duc-campground', 'log-cabin-resort-rv-campground',
        'bear-creek-campground', 'lyre-river-campground', 'sadie-creek-campground',
        'bogachiel-state-park', 'sequim-bay-state-park', 'dungeness-recreation-area',
        'salt-creek-recreation-area', 'elwha-dam-rv-park', 'forks-101-rv-park',
        'crescent-beach-rv-park', 'gilgal-oasis-rv-park',
        'quileute-oceanside-resort-rv-camping', 'hobuck-beach-resort-rv-camping',
        'cape-resort-rv-park', 'masons-resort-sekiu', 'anglers-hideaway-rv-park',
        'three-rivers-resort-rv-camping',
    }
    if row.get('Slug') in clallam:
        return ('<a class="regional-guide-link" href="/field-notes/clallam-county-rv-camping">'
                '<span>Clallam County RV camping guide</span>'
                '<small>Compare 23 campground records from Sequim to Neah Bay</small>'
                '</a>')
    jefferson = {
        'dosewallips-state-park', 'fort-flagler-historical-state-park',
        'fort-worden-historical-state-park', 'seal-rock-campground',
        'quilcene-campground', 'lake-leland-park-campground',
        'upper-oak-bay-campground', 'lower-oak-bay-campground',
        'point-hudson-marina-rv-park', 'jefferson-county-fairgrounds-campground',
        'cove-rv-park-country-store', 'hard-rain-cafe-campground',
        'port-ludlow-rv-park', 'falls-view-campground', 'hoh-campground',
        'kalaloch-campground', 'south-beach-campground',
        'coppermine-bottom-campground', 'cottonwood-campground',
        'hoh-oxbow-campground', 'minnie-peterson-campground',
        'south-fork-hoh-campground',
    }
    if row.get('Slug') not in jefferson:
        return ''
    return ('<a class="regional-guide-link" href="/field-notes/jefferson-county-rv-camping">'
            '<span>Jefferson County RV camping guide</span>'
            '<small>Compare 22 sourced records from primitive DNR camps to Port Townsend</small>'
            '</a>')

def build_long_desc_paras(row):
    desc = (row.get('Long description') or row.get('Short Description') or '').strip()
    paras = [p.strip() for p in desc.split('\n') if p.strip()] if desc else []
    if not paras:
        return f'          <p>{h(row.get("Short Description", ""))}</p>'
    return '\n'.join(f'          <p>{h(p)}</p>' for p in paras[:3])

def build_site_recs_paras(row):
    recs = (row.get('Site Recommendations') or '').strip()
    if not recs:
        return '      <p>Ask the camp host for current site recommendations at check-in.</p>'
    paras = [p.strip() for p in recs.split('\n') if p.strip()]
    return '\n'.join(f'      <p>{h(p)}</p>' for p in paras[:2])

def build_nearby_nature_paras(row):
    nature = (row.get('Nearby nature & parks') or '').strip()
    park_type = row.get('Park Type', 'Washington')
    if not nature:
        return f'          <p>Located within {h(park_type)} — explore the surrounding natural area for hiking, wildlife, and scenery unique to this region of Washington.</p>'
    paras = [p.strip() for p in nature.split('\n') if p.strip()]
    if len(paras) >= 2:
        return f'          <p>{h(paras[0])}</p>\n          <p>{h(paras[1])}</p>'
    return f'          <p>{h(paras[0])}</p>' if paras else f'          <p>{h(nature[:300])}</p>'

# ── JSON-LD builders ────────────────────────────────────────────────────────────
def build_faq_json(row):
    name          = row.get('Name', '')
    hookup_level  = row.get('Hookups', '0')
    hookup_label, _, _ = hookup_display(hookup_level)
    max_length    = row.get('Max RV length', '')
    drive_time    = row.get('Time from Seattle', '')
    drive_mins    = row.get('Drive Time Minutes', '')
    has_showers   = true_val(row.get('Amenities: Showers', ''))
    has_dump      = optional_bool(row.get('Dump station on site', ''))
    reserve_url   = row.get('Reservation website', '')
    reservation   = row.get('Reservation window', '')

    # Hookups answer
    if hookup_level == '0':
        dump_clause = ('A dump station is available on site.' if has_dump is True else
                       'There is no dump station.' if has_dump is False else
                       'The dump-station status is not confirmed; check with the operator.')
        hook_ans = f"No. {name} is dry camping only — no electric, water, or sewer hookups. {dump_clause}"
    elif hookup_level == '1':
        hook_ans = f"Yes. {name} offers electric-only hookups. Water and sewer are not available at the site."
    elif hookup_level == '2':
        hook_ans = f"Yes. {name} offers water and electric (W+E) hookups. Full sewer hookups are not available."
    else:
        hook_ans = f"Yes. {name} offers full hookups including water, electric, and sewer connections."

    miles_str = ''  # Drive Time Minutes is not a distance.
    drive_ans = f"{name} is approximately {drive_time.replace(' from Seattle','')}{miles_str} from Seattle."

    if re.search(r'^(campground\s+)?closed\b', reservation, re.I):
        res_ans = f"{name} is currently closed. Check the official closure details before travel."
    elif 'recreation.gov' in (reserve_url or '').lower():
        res_ans = f"{name} accepts reservations through Recreation.gov. {reservation}."
    elif reserve_url:
        res_ans = f"{name} accepts reservations online. {reservation}."
    elif 'first-come' in reservation.lower():
        res_ans = f'{name} is first-come, first-served. Check official access and camping rules before travel.'
    else:
        res_ans = f"{name} is first-come, first-served. No advance reservation is required."

    faqs = [
        (f"Does {name} have hookups?",
         hook_ans),
        (f"What is the maximum RV length at {name}?",
         f'RVs and trailers are not allowed at {name}.' if row.get('RV Access') == 'no' else f"Reported maximum RV length at {name} is {max_length} feet; confirm the individual site and vehicle rules." if max_length
         else f"Contact {name} for current RV length restrictions."),
        (f"How far is {name} from Seattle?",
         drive_ans),
        (f"Does {name} have showers?",
         f"{'Yes, showers are available on-site at' if has_showers else 'No, there are no showers at'} {name}."),
        (f"Does {name} have a dump station?",
         f"Yes, there is a dump station on site at {name}." if has_dump is True else
         f"No, there is no dump station at {name}." if has_dump is False else
         f"The dump-station status at {name} is not confirmed; check with the operator before relying on one."),
        (f"How do I reserve a site at {name}?",
         res_ans),
    ]
    entities = [{"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": entities}, indent=2)

def build_breadcrumb_json(row):
    name       = row.get('Name', '')
    park_type  = row.get('Park Type', '')
    pf         = PARK_FILTER.get(park_type, 'state')
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type":"ListItem","position":1,"name":"Home",        "item":"https://westcoastrvcamping.com/"},
            {"@type":"ListItem","position":2,"name":"Campgrounds", "item":"https://westcoastrvcamping.com/campgrounds"},
            {"@type":"ListItem","position":3,"name":park_type,     "item":f"https://westcoastrvcamping.com/campgrounds?type={pf}"},
            {"@type":"ListItem","position":4,"name":name},
        ]
    }, indent=2)

def build_campground_json(row):
    name        = row.get('Name', '')
    slug        = row.get('Slug', '')
    short_desc  = row.get('Short Description', '')
    hero_image  = 'https://westcoastrvcamping.com' + display_image(row)
    address     = row.get('Address', '')
    maps_url    = row.get('Google Maps Link', '')
    reserve_url = row.get('Reservation website', '')
    rv_sites    = row.get('Number of RV campsites', '')
    park_type   = row.get('Park Type', '')
    hookup_level = row.get('Hookups', '0')

    lat, lng = extract_lat_lng(maps_url, row)
    street, city, state, postal = parse_address(address)

    has_dump    = optional_bool(row.get('Dump station on site', ''))
    has_shower  = true_val(row.get('Amenities: Showers', ''))
    has_water   = true_val(row.get('Amenities: Drinking water', ''))
    has_fire    = true_val(row.get('Amenities: Fire pits', ''))
    has_hookup  = hookup_level != '0'
    toilet_type = (row.get('Amenities: Toilets') or '').strip()
    has_toilet  = bool(toilet_type) and toilet_type.lower() != 'false'

    tourist = ['RV Campers']
    if true_val(row.get('Hiking','')): tourist.append('Hikers')
    if true_val(row.get('Fishing','')): tourist.append('Anglers')
    if true_val(row.get('Kayaking/Paddling','')): tourist.append('Kayakers')
    if true_val(row.get('Playground','')) or true_val(row.get('Swimming','')): tourist.append('Families')

    amenities = [
        {"@type":"LocationFeatureSpecification","name":"Toilets",        "value": has_toilet},
        {"@type":"LocationFeatureSpecification","name":"Showers",        "value": has_shower},
        {"@type":"LocationFeatureSpecification","name":"Drinking Water", "value": has_water},
    ]
    if has_dump is not None:
        amenities.append(
            {"@type":"LocationFeatureSpecification","name":"Dump Station", "value": has_dump}
        )
    amenities.extend([
        {"@type":"LocationFeatureSpecification","name":"Electric Hookups","value": has_hookup},
        {"@type":"LocationFeatureSpecification","name":"Fire Pits",      "value": has_fire},
    ])

    schema = {
        "@context": "https://schema.org",
        "@type": ["CivicStructure", "TouristAttraction"],
        "name": name,
        "description": short_desc,
        "url": f"https://westcoastrvcamping.com/campground/{slug}",
        "image": hero_image,
        "amenityFeature": amenities,
        "touristType": tourist,
    }
    if rv_sites:
        try: schema["numberOfRooms"] = int(rv_sites)
        except: pass
    if lat and lng:
        schema["geo"]    = {"@type":"GeoCoordinates","latitude":float(lat),"longitude":float(lng)}
        schema["hasMap"] = maps_url
    if street:
        schema["address"] = {"@type":"PostalAddress","streetAddress":street,
                             "addressLocality":city,"addressRegion":state,
                             "postalCode":postal,"addressCountry":"US"}
    if reserve_url:
        schema["sameAs"] = reserve_url
    return json.dumps(schema, indent=2)

# ── Page assembler ──────────────────────────────────────────────────────────────
def generate_page(row, slug_lookup, template):
    slug = (row.get('Slug') or '').strip()
    if not slug: return None

    name         = (row.get('Name') or '').strip()
    hero_image   = display_image(row)
    topo_image   = hero_image
    state_map    = (row.get('State Map') or '').strip()
    park_type    = (row.get('Park Type') or 'State Park').strip()
    drive_time   = (row.get('Time from Seattle') or '').replace(' from Seattle', '')
    drive_mins   = (row.get('Drive Time Minutes') or '').strip()
    address      = (row.get('Address') or '').strip()
    rv_sites     = (row.get('Number of RV campsites') or '—').strip()
    max_length   = (row.get('Max RV length') or '').strip()
    hookup_level = (row.get('Hookups') or '0').strip()
    surface      = (row.get('Site surface type') or 'Mixed').strip()
    dump         = optional_bool(row.get('Dump station on site', ''))
    reservation  = (row.get('Reservation window') or '').strip()
    reserve_url  = (row.get('Reservation website') or '#').strip() or '#'
    nearest_town = (row.get('Nearest town') or '').strip()
    data_updated = (row.get('Data last updated') or 'Feb 2026').strip()

    hookup_label, hookup_note_txt, has_hookup = hookup_display(hookup_level)
    dump_display = 'On-site' if dump is True else 'Not available' if dump is False else 'Not confirmed'
    dump_note = ('Confirm access with the operator' if dump is True else
                 'Plan a separate dump stop' if dump is False else 'Confirm with the operator')
    reserve_short = format_reservation_short(reservation)
    reserve_note  = 'Check exact dates with the operator' if 'month' in reservation.lower() else 'Availability varies'

    addr_parts = [p.strip() for p in address.split(',')]
    city = addr_parts[1] if len(addr_parts) >= 2 else nearest_town

    miles = (row.get('Drive distance miles') or '').strip()
    miles_str = f' · {miles} mi' if miles else ''
    drive_full = f'{row.get("Time from Seattle","")}{miles_str}'
    pass_meta     = PASS_META.get(park_type, 'Check website for current fees')

    if re.search(r'^(campground\s+)?closed\b', reservation, re.I):
        res_meta = f'Closure details · {reservation}'
    elif 'recreation.gov' in (reserve_url or '').lower():
        res_meta = f'Recreation.gov · {reservation}'
    elif reserve_url and reserve_url != '#':
        res_meta = f'Online reservation · {reservation}'
    elif 'first-come' in reservation.lower():
        res_meta = f'No advance reservations · {reservation}'
    else:
        res_meta = reservation or 'First-come, first-served'

    nature_eyebrow = park_type
    nature_title   = {
        'National Park':     "One of Washington's crown jewels",
        'State Forest':      'Primitive camping on Washington trust lands',
        'State Park':        'Washington State Parks — built for exploration',
        'County Campground': 'Local parks, local character',
        'Private Campground':'Privately managed, full-service',
    }.get(park_type, 'Explore the surrounding area')

    page_title = (f"{name} — {park_type}, {city}, WA | WA RV Camping" if city
                  else f"{name} — {park_type} RV Campground | WA RV Camping")

    rv_str = rv_sites if rv_sites != '—' else ''
    len_str = f'{max_length}ft max, ' if max_length else ''
    hookup_phrase = 'no hookups' if hookup_level == '0' else hookup_label.lower()
    meta_desc = (f"{name}: {rv_str+' sites, ' if rv_str else ''}{len_str}"
                 f"{hookup_phrase}. {drive_time} from Seattle. "
                 f"{row.get('Short Description','')}")[:160]
    if row.get('RV Access') == 'no':
        meta_desc = row.get('Short Description', '')[:160]
    og_title = f"{name} — {park_type} | WA RV Camping"
    og_desc  = (f"{rv_str+'-site ' if rv_str else ''}{park_type} campground, "
                f"{len_str}{hookup_phrase}. {drive_time} from Seattle.")[:200]
    closed = bool(re.search(r'^(campground\s+)?closed\b', reservation, re.I))
    if closed:
        og_desc = row.get('Short Description', '')[:200]

    services_note = (f"Stock up in {nearest_town} before heading out — services get limited near the campground."
                     if nearest_town else "Stock up on supplies before leaving the nearest town.")

    def dist(field):
        v = (row.get(field) or '').strip()
        return f'{v} mi' if v and v != '0' else '—'

    fcfs = 'first-come' in reservation.lower()
    reserve_label = 'Closure details' if closed else 'Camping rules' if fcfs else 'Booking details'
    access_notice = ''
    if (row.get('RV Access') == 'no' or closed) and row.get('Access note'):
        access_notice = ('<aside style="padding:100px 24px 24px;background:#fff1d6;color:#352d1b;text-align:center" aria-label="Campground access restriction">'
                         + '<strong>' + h(row['Access note']) + '</strong> '
                         + '<a href="' + h(row.get('Access source', '')) + '">Official source</a>'
                         + ' · Checked ' + h(row.get('Access checked', '')) + '</aside>')
    tokens = {
        '{{reserve_label}}': reserve_label,
        '{{nav_mode}}': 'data-access-restricted' if row.get('RV Access') == 'no' or closed else 'data-nav-transparent',
        '{{access_notice}}': access_notice,
        '{{page_title}}':               page_title,
        '{{meta_desc}}':                meta_desc,
        '{{slug}}':                     slug,
        '{{hero_image}}':               hero_image,
        '{{social_image}}':             'https://westcoastrvcamping.com' + hero_image,
        '{{og_title}}':                 og_title,
        '{{og_desc}}':                  og_desc,
        '{{breadcrumb_json}}':          build_breadcrumb_json(row),
        '{{faq_json}}':                 build_faq_json(row),
        '{{campground_json}}':          build_campground_json(row),
        '{{reserve_url}}':              reserve_url,
        '{{park_badge}}':               PARK_BADGE.get(park_type, park_type),
        '{{drive_time}}':               drive_time,
        '{{name}}':                     h(name),
        '{{short_desc}}':               h(row.get('Short Description', '')),
        '{{rv_sites}}':                 rv_sites,
        '{{max_length_val}}':           'No RV access' if row.get('RV Access') == 'no' else f'{max_length} ft' if max_length else 'Not confirmed',
        '{{max_length_note}}':          'Confirm the selected site' if max_length else 'Check limits by site',
        '{{hookup_val}}':               hookup_label,
        '{{hookup_note}}':              hookup_note_txt,
        '{{surface}}':                  h(surface),
        '{{dump_val}}':                 dump_display,
        '{{dump_note}}':                dump_note,
        '{{reservation_val}}':          reserve_short,
        '{{reservation_note}}':         reserve_note,
        '{{long_desc_paras}}':          build_long_desc_paras(row),
        '{{address}}':                  h(address),
        '{{drive_time_miles}}':         h(drive_full),
        '{{reservation_meta}}':         h(res_meta),
        '{{pass_meta}}':                h(pass_meta),
        '{{state_map}}':                state_map,
        '{{google_maps}}':              directions_url(row),
        '{{map_region}}':               h(f'{city}, WA' if city else 'Washington State'),
        '{{specs_grid_html}}':          '<p>RVs and trailers are not allowed. See the official access guidance above.</p>' if row.get('RV Access') == 'no' else build_specs_grid(row),
        '{{activities_title}}':         h(f'Activities at {name}'),
        '{{activity_pills}}':           build_activity_pills(row),
        '{{activity_list_html}}':       build_activity_list(row),
        '{{nature_eyebrow}}':           h(nature_eyebrow),
        '{{nature_title}}':             h(nature_title),
        '{{nearby_nature_paras}}':      build_nearby_nature_paras(row),
        '{{amenities_grid_html}}':      build_amenities_grid(row),
        '{{amenities_note}}':           h(row.get('Amenities summary', '')),
        '{{tips_image_url}}':           topo_image,
        '{{site_recs_paras}}':          build_site_recs_paras(row),
        '{{nearest_town}}':             h(nearest_town),
        '{{gas_mi}}':                   dist('Nearest gas station'),
        '{{grocery_mi}}':               dist('Nearest major grocery store'),
        '{{costco_mi}}':                dist('Nearest Costco'),
        '{{starbucks_mi}}':             dist('Nearest Starbucks'),
        '{{state_park_mi}}':            dist('Nearest state park'),
        '{{services_note}}':            h(services_note),
        '{{nearby_camps_html}}':        build_nearby_camps(row, slug_lookup),
        '{{regional_guide_html}}':      build_regional_guide(row),
        '{{reserve_title}}':            h(f'Plan your visit to {name}'),
        '{{reserve_sub}}':              h(f'{reservation}. Confirm current rules, site dimensions, and conditions with the operator. Booking and availability are handled externally.'),
        '{{data_updated}}':             h(f'Record updated {data_updated} · Individual facts may need rechecking'),
    }

    page = template
    for token, value in tokens.items():
        page = page.replace(token, value)
    return page

# ── Main ────────────────────────────────────────────────────────────────────────
def main():
    filter_slug = None
    dry_run = False
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--slug' and i + 1 < len(args):
            filter_slug = args[i+1]; i += 2
        elif args[i] == '--dry-run':
            dry_run = True; i += 1
        else:
            i += 1

    if not TEMPLATE_PATH.exists():
        print(f"ERROR: Template not found: {TEMPLATE_PATH}")
        sys.exit(1)
    template = TEMPLATE_PATH.read_text(encoding='utf-8')

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    print(f"Loaded {len(rows)} campgrounds from CSV")

    slug_lookup = {r['Slug'].strip(): r for r in rows if r.get('Slug','').strip()}

    if not dry_run:
        OUT_DIR.mkdir(exist_ok=True)

    generated, errors = 0, []
    for row in rows:
        slug = (row.get('Slug') or '').strip()
        if not slug or (filter_slug and slug != filter_slug):
            continue
        try:
            page_html = generate_page(row, slug_lookup, template)
            if page_html is None:
                continue
            if dry_run:
                unfilled = re.findall(r'\{\{[^}]+\}\}', page_html)
                status = f"WARN unfilled: {unfilled[:5]}" if unfilled else "OK"
                print(f"  {slug}: {status}")
            else:
                (OUT_DIR / f'{slug}.html').write_text(page_html, encoding='utf-8')
                generated += 1
                if generated % 20 == 0:
                    print(f"  ... {generated} pages written")
        except Exception as e:
            errors.append((slug, str(e)))
            print(f"  ERROR {slug}: {e}")

    if not dry_run:
        print(f"\n✅ Generated {generated} pages → {OUT_DIR}/")
    if errors:
        print(f"\n⚠️  {len(errors)} errors:")
        for slug, err in errors:
            print(f"   {slug}: {err}")
        raise SystemExit(1)

if __name__ == '__main__':
    main()
