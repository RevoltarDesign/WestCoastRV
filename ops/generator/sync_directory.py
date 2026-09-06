#!/usr/bin/env python3
"""Generate directory/map records and sitemap from the canonical CSV.

Run after generate.py. --check fails if outputs would change. Never deploys.
Legacy Draft flags are bookkeeping; this does not silently unpublish records.
"""
import argparse
import csv
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from generate import CSV_PATH, BASE_DIR, extract_lat_lng, display_image

TYPES = {'National Park': 'national', 'National Forest': 'forest', 'State Park': 'state',
         'County Campground': 'county', 'City Campground': 'city', 'Private Campground': 'private'}
HOOKUPS = {'0': ('none', 'No hookups'), '1': ('electric', 'Electric'),
           '2': ('water-electric', 'Water + Electric'), '3': ('full', 'Full hookups')}


def make_record(row):
    def number(key):
        value = row.get(key, '').strip()
        return int(value) if value else None
    mins = number('Drive Time Minutes')
    band = 'all' if mins is None else ('under-1' if mins < 60 else '1-2' if mins < 120
           else '2-3' if mins < 180 else '3-4' if mins < 240 else '4plus')
    key, label = HOOKUPS.get(row.get('Hookups'), ('unknown', 'Not confirmed'))
    lat, lon = extract_lat_lng(row.get('Google Maps Link'))
    if not lat or not lon:
        raise ValueError(f"Missing coordinates for {row['Slug']}")
    record = dict(name=row['Name'], slug=row['Slug'], desc=row['Short Description'],
                  type=row['Park Type'], typeKey=TYPES[row['Park Type']],
                  drive=row['Time from Seattle'], band=band, min=mins,
                  sites=number('Number of RV campsites'), len=number('Max RV length'),
                  hKey=key, hLabel=label, hookups=label, town=row['Nearest town'],
                  lat=float(lat), lon=float(lon), rvAccess=row.get('RV Access', 'unknown') or 'unknown',
                  updated=row['Data last updated'],
                  img=display_image(row))
    for key, field in {'hiking':'Hiking', 'fishing':'Fishing', 'swim':'Swimming',
                       'kayak':'Kayaking/Paddling', 'beach':'Beach & Tide Pools',
                       'showers':'Amenities: Showers', 'dump':'Dump station on site'}.items():
        record[key] = row.get(field, '').lower() == 'true'
    return record


def outputs():
    with CSV_PATH.open(encoding='utf-8-sig', newline='') as source:
        rows = list(csv.DictReader(source))
    records = [make_record(row) for row in rows]
    if len({r['slug'] for r in records}) != len(records):
        raise ValueError('Duplicate campground slugs')
    count = len(records)
    encoded = json.dumps(records, separators=(',', ':'), ensure_ascii=True).replace('<', '\\u003c')
    result = {}
    for name in ('campgrounds.html', 'map.html'):
        path = BASE_DIR / 'site' / name
        original = path.read_text()
        text, substitutions = re.subn(r'const CAMPS\s*=\s*\[.*?\];', lambda _: 'const CAMPS=' + encoded + ';', original, count=1, flags=re.S)
        if substitutions != 1:
            raise ValueError(f'Missing CAMPS marker in {name}')
        result[path] = text
    for name in ('index.html', 'campgrounds.html', 'map.html'):
        path = BASE_DIR / 'site' / name
        text = result.get(path, path.read_text())
        text = re.sub(r'\b\d+(?= (?:verified RV campgrounds|verified campgrounds|campgrounds|Campgrounds))', str(count), text)
        text = re.sub(r'(Browse all |browse all |View all |see all )\d+', lambda m: m[1] + str(count), text)
        text = re.sub(r'\b\d+ Washington RV Campgrounds', f'{count} Washington Campgrounds', text)
        text = re.sub(r'\b\d+ Washington Campgrounds', f'{count} Washington Campgrounds', text)
        text = re.sub(r'("numberOfItems":\s*)\d+', lambda m: m[1] + str(count), text)
        text = re.sub(r'(<strong>)\d+(</strong> camps)', lambda m: m[1] + str(count) + m[2], text)
        text = re.sub(r'(<div class="trust-num">)\d+(</div>)', lambda m: m[1] + str(count) + m[2], text, count=1)
        result[path] = text
    path = BASE_DIR / 'site/sitemap.xml'
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    tree = ET.fromstring(path.read_text())
    for entry in list(tree):
        loc = entry.find('{*}loc')
        if loc is not None and '/campground/' in (loc.text or ''):
            tree.remove(entry)
    if not any((entry.findtext('{' + ns + '}loc') or '').rstrip('/').endswith('/map') for entry in tree):
        entry = ET.SubElement(tree, '{' + ns + '}url')
        ET.SubElement(entry, '{' + ns + '}loc').text = 'https://westcoastrvcamping.com/map'
    for row in rows:
        entry = ET.SubElement(tree, '{' + ns + '}url')
        ET.SubElement(entry, '{' + ns + '}loc').text = 'https://westcoastrvcamping.com/campground/' + row['Slug']
    ET.indent(tree, space='  ')
    result[path] = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree, encoding='unicode') + '\n'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changes = {path: content for path, content in outputs().items() if path.read_text() != content}
    for path, content in changes.items():
        print(('STALE ' if args.check else 'Updated ') + str(path.relative_to(BASE_DIR)))
        if not args.check:
            path.write_text(content)
    if not changes:
        print('Directory, map, counts, and sitemap are synchronized.')
    return 1 if args.check and changes else 0


if __name__ == '__main__':
    raise SystemExit(main())
