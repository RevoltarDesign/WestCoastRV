#!/usr/bin/env python3
"""Apply the final private/fairgrounds coordinate, route, and factual scrub batch."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "private-coordinate-final-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
CHECKED = "2026-09-12"

SOURCES = {
    "pine-village-koa-holiday": ("https://koa.com/campgrounds/leavenworth/general-information/", "Kampgrounds of America", "koa"),
    "thousand-trails-leavenworth": ("https://www.rvonthego.com/washington/leavenworth-rv-campground/directions", "RVontheGo / Thousand Trails", "thousand-trails"),
    "tall-chief-rv-park-campground": ("https://thousandtrails.com/washington/tall-chief-rv-camping-resort/", "Thousand Trails", "thousand-trails"),
    "packwood-rv-park-campground": ("https://packwoodrvpark.com/contact", "Packwood RV Park & Campground", "operator"),
    "american-heritage-campground": ("https://www.americanheritagecampground.com/ah_frontpage.htm", "American Heritage Campground", "operator"),
    "andersens-oceanside-rv-park": ("https://andersensrv.com/", "Andersen's Oceanside RV Park", "operator"),
    "beachside-rv-park": ("https://birchbaywa.org/birch-bay-rv-parks/", "Birch Bay Chamber of Commerce", "local-destination-organization"),
    "sunnyside-rv-park": ("https://www.goodsam.com/campgrounds-rv-parks/washington/sunnyside/sunnyside-rv-park/cgid-201820823", "Good Sam Campgrounds", "current-campground-directory"),
    "north-whidbey-rv-park": ("https://northwhidbeyrvpark.com/", "North Whidbey RV Park", "operator"),
    "whidbey-island-fairgrounds-campground": ("https://portofsouthwhidbey.com/facilities/fairgrounds-campground-south-whidbey/", "Port of South Whidbey", "port-of-south-whidbey"),
}

CONTENT = {
    "pine-village-koa-holiday": {
        "Short Description": "Year-round KOA near the Wenatchee River with full-hookup RV sites, a pool, playground, dog park, and a new Zelt Strasse entrance north of US-2.",
        "Reservation window": "Reservations available online or by phone; summer and festival dates can fill well ahead",
        "Long description": "Leavenworth/Pine Village KOA Holiday is a year-round campground near the Wenatchee River on the north side of Leavenworth. The current operator pages list full-hookup and water-and-electric RV choices, tent sites, cabins, a seasonal pool and hot tub, a playground, KampK9 dog park, laundry, propane, and a camp store. The former Riverbend Drive approach has changed: turn from US-2 onto River Bend Drive, continue as it becomes Ward Strasse, then take Zelt Strasse to the signed campground entrance.",
        "Number of RV campsites": "", "Max RV length": "", "Playground": "true",
        "Things to do for families": "Seasonal swimming pool and hot tub\nPlayground and KampK9 dog park\nLeavenworth shops, restaurants, and festivals\nWenatchee River recreation\nIcicle Creek and Okanogan-Wenatchee National Forest day trips",
        "Things to do for families summary": "A year-round, family-focused KOA near Leavenworth with a seasonal pool, playground, dog park, river recreation, and Cascade trail access.",
        "Nearby nature & parks": "The campground is near the Wenatchee River on Leavenworth's north side. Icicle Creek and the Okanogan-Wenatchee National Forest provide trail and picnic options by road, while Tumwater Canyon begins west of town on US-2. Check trailhead permits, seasonal road conditions, and river conditions before a day trip.",
        "Amenities summary": "The operator lists full-hookup and water-and-electric RV options, restrooms, showers, laundry, Wi-Fi, propane, a store, a seasonal pool and hot tub, playground, and KampK9 dog park. Site dimensions vary; enter your equipment length in the reservation system.",
        "Nearest town": "Leavenworth (about 1 mi)", "Nearest gas station": "1", "Nearest major grocery store": "1", "Nearest Starbucks": "1",
        "Site Recommendations": "Use the current Zelt Strasse entrance and follow campground signs to the A-frame office. Enter the complete RV and tow-vehicle length when booking because the operator does not publish one campground-wide maximum. Winter camping is available, but the operator advises carrying winter equipment and preparing for snow, ice, and very cold temperatures.",
        "Access note": "Use the new Zelt Strasse entrance. The operator asks guests to enter their equipment length when booking and does not publish one campground-wide RV maximum.",
    },
    "thousand-trails-leavenworth": {
        "Short Description": "Year-round forested resort on 300 acres near the Chiwawa River and Fish Lake, with 279 total sites and public booking available without a membership.",
        "Reservation window": "Public reservations available; membership is optional. Check current dates, site types, and stay limits in the booking system",
        "Long description": "Thousand Trails Leavenworth is a 300-acre forested resort north of Leavenworth near the Chiwawa River. The current operator directory lists 279 total sites and year-round operation. The property borders the Chiwawa River; Fish Lake is about four miles away, the Wenatchee River about five miles away, and Icicle River about twenty miles away. The current booking page says no membership is needed for ordinary reservations, while membership options remain available.",
        "Number of RV campsites": "", "Max RV length": "",
        "Things to do for families": "Seasonal pools and organized activities\nMini golf, sports courts, and playground\nFishing and paddling at Fish Lake\nChiwawa River and Lake Wenatchee area recreation\nLeavenworth day trips",
        "Things to do for families summary": "A large year-round forest resort near the Chiwawa River and Fish Lake, with public booking, seasonal recreation facilities, and Leavenworth within driving distance.",
        "Nearby nature & parks": "The resort is in the Lake Wenatchee and Chiwawa River area north of Leavenworth. The operator places Fish Lake about four miles away, the Wenatchee River about five miles away, and Icicle River about twenty miles away. Lake Wenatchee State Park and Okanogan-Wenatchee National Forest trailheads are reached by road.",
        "Nearest town": "Leavenworth (about 17 mi)", "Nearest gas station": "16", "Nearest major grocery store": "16", "Nearest Starbucks": "17",
        "Site Recommendations": "Book the site type that matches your equipment and hookup needs; the forest layout varies and the operator does not publish one campground-wide RV maximum. Public reservations do not require a Thousand Trails membership. This is a driving-distance base for Leavenworth rather than a walk-to-downtown campground.",
        "Access note": "Operator GPS points to the Chiwawa Loop Road resort. Public reservations are available without membership; verify the selected site's equipment and hookup limits while booking.",
    },
    "tall-chief-rv-park-campground": {
        "Short Description": "Year-round wooded Fall City resort with 180 sites, water and electric service, no sewer sites, and public reservations without a membership.",
        "Reservation window": "Public reservations available without membership; RV sites are back-in and chosen first-come after arrival",
        "Long description": "Tall Chief RV Resort is a 180-site, year-round wooded resort near Fall City, about 24 road miles from central Seattle. The current operator page says no membership is needed for ordinary stays. RV sites are back-in and are not assigned before arrival. The park has water and electric service but no sewer sites; paid honey-wagon service is offered on a schedule. Seasonal recreation includes a pool area, mini golf, sports courts, and a kids play area, although the operator currently lists the pool, hot tub, sauna, and adjacent restroom as temporarily unavailable during improvements.",
        "Max RV length": "", "Hookups": "2", "Playground": "true",
        "Things to do for families": "Snoqualmie Falls day trip\nPickleball, basketball, volleyball, and cornhole\nSeasonal mini golf and kids play area\nSnoqualmie Valley and foothill trail day trips",
        "Things to do for families summary": "A close-to-Seattle wooded resort with sports, seasonal recreation, and easy driving access to Snoqualmie Falls and the Cascade foothills.",
        "Nearby nature & parks": "Tall Chief sits in the forested foothills west of Fall City. Snoqualmie Falls, the Snoqualmie Valley Trail, Tiger Mountain State Forest, and other Cascade foothill destinations are reachable by road. The operator does not describe the campground as a Snoqualmie River-front property.",
        "Nearest town": "Fall City (about 6 mi)", "Nearest gas station": "6", "Nearest major grocery store": "10", "Nearest Starbucks": "8",
        "Amenities summary": "The operator lists water and electric RV service, restrooms, showers, laundry, a lodge, sports courts, seasonal recreation, and a dump station. There are no sewer sites; scheduled paid honey-wagon service is available. The pool, hot tub, sauna, and adjacent restroom are currently listed as temporarily unavailable during improvements.",
        "Site Recommendations": "All RV sites are back-in and selected first-come after arrival, so arrive within check-in hours. Bring a portable waste tote or plan around the dump station or paid honey-wagon service because there are no sewer sites. Confirm the current status of seasonal facilities before booking.",
        "Access note": "Use the operator-published SE 8th Street address and GPS. Sites are back-in only and the operator does not publish one resort-wide RV maximum.",
    },
    "packwood-rv-park-campground": {
        "Short Description": "Year-round in-town Packwood RV park with 77 sites, full hookups, and pull-through options near US-12 recreation corridors.",
        "Reservation window": "Reservations available through the operator's CampLife booking link",
        "Reservation website": "https://packwoodrvpark.com/contact",
        "Long description": "Packwood RV Park & Campground is a year-round private park in Packwood with 77 RV sites. Current operator and White Pass Scenic Byway information lists full utility hookups, big-rig access, and pull-through options, with some pull-throughs published at up to 40 feet. Its in-town US-12 location provides road access toward Mount Rainier National Park, White Pass, Gifford Pinchot National Forest, and the Cowlitz River valley.",
        "Number of RV campsites": "77", "Max RV length": "40",
        "Things to do for families": "Mount Rainier National Park day trips\nWhite Pass skiing and summer recreation\nGifford Pinchot National Forest trails\nCowlitz River valley recreation\nWalk to Packwood shops and food",
        "Things to do for families summary": "An in-town, full-hookup base for Mount Rainier, White Pass, Gifford Pinchot National Forest, and the upper Cowlitz River valley.",
        "Nearby nature & parks": "Packwood lies in the upper Cowlitz River valley between Mount Rainier National Park, Goat Rocks Wilderness, and the William O. Douglas Wilderness. Access and trail conditions change seasonally; check current National Park Service and Forest Service notices before choosing a day trip.",
        "Site Recommendations": "Use the operator's CampLife link to match your full equipment length to a specific site. The current regional listing publishes 77 sites and pull-through options up to 40 feet; larger rigs should confirm fit directly. Check current Mount Rainier entrances and trail closures rather than relying on older Grove of the Patriarchs guidance.",
        "Access note": "The reviewed point uses the current 12985 US-12 address. Pull-through options are published up to 40 feet; confirm total equipment fit while booking.",
    },
    "american-heritage-campground": {
        "Short Description": "Year-round wooded campground south of Olympia with full-hookup and water-electric RV sites, a seasonal heated pool, playground, dog park, and showers.",
        "Reservation window": "Reserve by phone or in person up to one year ahead; the operator does not offer online booking",
        "Reservation website": "https://www.americanheritagecampground.com/ah_rates.htm",
        "Long description": "American Heritage Campground is a wooded, year-round campground south of Olympia. The operator lists back-in RV sites with either full hookups or 30-amp water and electric service. Facilities include restrooms, showers, laundry, a seasonal heated outdoor pool, playground, dog park, store, and propane. Reservations are taken by phone or in person and may be made up to one year in advance.",
        "Number of RV campsites": "", "Max RV length": "", "Dump station on site": "",
        "Things to do for families": "Seasonal heated outdoor pool\nPlayground and dog park\nHorseshoes and open play space\nOlympia and Tumwater day trips\nMillersylvania State Park and Capitol Forest",
        "Things to do for families summary": "A wooded Olympia-area campground with a seasonal heated pool, playground, dog park, and access to South Sound parks and city attractions.",
        "Nearby nature & parks": "Millersylvania State Park and Capitol State Forest are convenient driving destinations south and west of Olympia. The Billy Frank Jr. Nisqually National Wildlife Refuge is farther northeast by road. Check each land manager's current hours, passes, and trail conditions.",
        "Amenities summary": "The operator lists full-hookup and water-electric RV sites, restrooms, showers, laundry, a seasonal heated pool, playground, dog park, store, and propane. All RV sites are back-in. Mini golf is not listed in the current operator amenities.",
        "Site Recommendations": "Call to reserve and give the operator the full RV and tow-vehicle dimensions because all RV sites are back-in and no campground-wide maximum is published. Ask whether a full-hookup or water-electric site best matches the stay.",
        "Access note": "The named campground point corrects a former pin several miles north. All RV sites are back-in; confirm equipment fit by phone.",
    },
    "andersens-oceanside-rv-park": {
        "Reservation window": "Reservations required; same-day reservations must be made before noon and stays are limited to 21 nights",
        "Max RV length": "", "Dump station on site": "",
        "Long description": "Andersen's Oceanside RV Park offers 60 full-hookup RV sites on seven acres along the Long Beach Peninsula. The operator lists 50/30/20-amp power, water, sewer, picnic tables, and a sandy path to the ocean beach. All sites are described as 100 feet long, but the operator does not publish one maximum RV length. Reservations are required and same-day arrivals must book before noon. Accepted equipment is limited to self-contained motorhomes, fifth wheels, and travel trailers longer than 18 feet; tents, Class B vans, truck campers, pop-ups, and conversions are not accepted.",
        "Amenities summary": "The operator lists full-hookup sites, restrooms, showers, laundry, Wi-Fi, a playground, dog walk, and direct beach path. Because sites already have sewer hookups, a separate public dump-station claim is not published here.",
        "Playground": "true",
        "Site Recommendations": "Choose among premium, prime, and seasonal forest sites in the operator's booking system. Every listed site is 100 feet long, but confirm the fit and maneuvering room for the complete rig. Review the equipment restrictions before booking; the park does not accept tents, Class B vans, truck campers, pop-ups, or conversions.",
        "Access note": "The operator reservation system supplies the corrected point at the 138th Street property. The park accepts specified self-contained RV types over 18 feet; confirm fit because no single RV maximum is published.",
    },
    "beachside-rv-park": {
        "Dump station on site": "", "Amenities: Fire pits": "",
        "Amenities summary": "Current destination and campground listings support 72 full-hookup sites, restrooms, showers, laundry, and Wi-Fi. A separate dump station and individual fire pits were not confirmed during this review.",
        "Site Recommendations": "The park is across Birch Bay Drive from the shoreline. Confirm availability, total equipment fit, and current amenities by phone because the operator website is not reliably accessible and no current operator-published maximum length was available.",
        "Access note": "The corrected named campground point is on Birch Bay Drive. Confirm equipment fit by phone because a current operator-published maximum length was not available.",
    },
    "sunnyside-rv-park": {
        "Short Description": "Year-round, 35-site full-hookup RV park on Scoon Road in the lower Yakima Valley, with pull-through sites, a seasonal pool, showers, laundry, and Wi-Fi.",
        "Reservation window": "Reservations accepted; contact the park or use its current booking channel for availability", "Dump station on site": "",
        "Long description": "Sunnyside RV Park is a year-round, 35-site private park on Scoon Road in the lower Yakima Valley. Current campground listings support full hookups, 30/50-amp service, pull-through options, Wi-Fi, restrooms, showers, laundry, and a seasonal pool. Listings publish a maximum of 65 feet, but travelers should enter or confirm the complete equipment length when reserving.",
        "Things to do for families": "Seasonal pool\nLower Yakima Valley wineries and farm stands\nYakima River recreation\nSunnyside parks and seasonal community events",
        "Things to do for families summary": "A practical full-hookup Yakima Valley base with pull-through sites, a seasonal pool, and road access to wineries, farm stands, and river recreation.",
        "Nearby nature & parks": "Sunnyside sits in the lower Yakima Valley amid vineyards, orchards, hop fields, and irrigated farmland. Yakima River access and wildlife areas vary by location and season; confirm public access and current rules before visiting.",
        "Site Recommendations": "Pull-through and full-hookup options make this a useful overnight or wine-country base. Current listings publish a 65-foot maximum, but confirm the complete motorhome or trailer-and-tow-vehicle length before arrival.",
        "Access note": "Use 609 Scoon Road; the former Yakima Valley Highway pin was several miles east of the campground. Current directories publish a 65-foot maximum.",
    },
    "north-whidbey-rv-park": {
        "Reservation window": "Reservations available through the operator; check live availability and site-specific fit",
        "Max RV length": "",
        "Long description": "North Whidbey RV Park is a year-round private park on Cornet Bay Road beside Deception Pass State Park. The operator lists 100 paved, full-hookup sites with 30/50-amp power, water, sewer, picnic tables, and fire pits. Facilities include free hot showers, laundry, a clubhouse, playground, fenced dog park, and propane. The stable Seattle driving route uses I-5, WA-20, and Deception Pass rather than a ferry.",
        "Things to do for families summary": "One hundred paved, full-hookup sites beside Deception Pass State Park, with trails, beaches, Cornet Bay recreation, and Anacortes within driving distance.",
        "Nearby nature & parks": "Deception Pass State Park is directly nearby, with forest trails, saltwater shorelines, beaches, and Cornet Bay facilities. Anacortes, Fort Casey Historical State Park, and central Whidbey destinations are accessible by road; drive times depend on island traffic.",
        "Nearest Costco": "35", "Nearest Starbucks": "8",
        "Site Recommendations": "Use the operator's live booking information to match a site to the complete rig length; the current public pages do not publish one park-wide 60-foot maximum. The all-road approach over Deception Pass avoids ferry schedules. Expect possible aircraft noise from nearby NAS Whidbey Island.",
        "Access note": "The reviewed point matches the Cornet Bay Road property. Use the all-road Deception Pass route and confirm site-specific equipment fit with the operator.",
    },
    "whidbey-island-fairgrounds-campground": {
        "Short Description": "Year-round Port of South Whidbey campground in Langley with 20 RV sites offering power and/or water, showers, a dump station, and reservable or same-day empty sites.",
        "Reservation window": "Reserve online or claim an empty site on arrival; open year-round with limited water service November through March",
        "Long description": "The Port of South Whidbey operates this year-round campground at the Whidbey Island Fairgrounds in Langley. The current operator page lists 20 RV sites with power and/or water, bathrooms with private showers, and a public dump station. Travelers may reserve online or claim an empty site on arrival; cash is not accepted. Water availability is limited from November through March. Long vehicles should enter from Fairgrounds Road at Langley Road/Camano Avenue and turn immediately into the campground entrance.",
        "Max RV length": "",
        "Things to do for families": "Walk or drive into Langley\nSaratoga Passage viewpoints and paddling\nDouble Bluff Beach\nFort Casey Historical State Park\nSouth Whidbey parks and trails",
        "Things to do for families summary": "A small year-round Langley base with hookups, showers, a dump station, and access to South Whidbey beaches, parks, and town attractions.",
        "Nearby nature & parks": "Langley overlooks Saratoga Passage. Double Bluff Beach, Fort Casey Historical State Park, and other South and Central Whidbey parks are reachable by road. Verify current access before relying on older descriptions of South Whidbey State Park facilities.",
        "Amenities summary": "The operator lists 20 RV sites with power and/or water, bathrooms with private showers, and a public dump station. Water is limited November through March. Cash is not accepted; reserve online or follow the posted instructions for an empty site.",
        "Site Recommendations": "Use the Fairgrounds Road entrance recommended for long vehicles. The operator does not publish one campground-wide RV maximum, so match the reservation to the complete equipment length. From Seattle, allow time beyond the nominal route for Mukilteo-Clinton ferry boarding and queues, and check live ferry conditions before departure.",
        "Access note": "Long vehicles should turn from Langley Road/Camano Avenue onto Fairgrounds Road and immediately right into the campground. The public drive estimate includes a ferry margin; ferry queues can still make the trip longer.",
    },
}

MAX_VALUES = {
    "pine-village-koa-holiday": None, "thousand-trails-leavenworth": None,
    "tall-chief-rv-park-campground": None, "packwood-rv-park-campground": 40,
    "american-heritage-campground": None, "andersens-oceanside-rv-park": None,
    "beachside-rv-park": None, "sunnyside-rv-park": 65,
    "north-whidbey-rv-park": None, "whidbey-island-fairgrounds-campground": None,
}

def duration(minutes):
    hours, mins = divmod(minutes, 60)
    if hours and mins:
        return f"~{hours} hr {mins} min from Seattle"
    if hours:
        return f"~{hours} hr from Seattle"
    return f"~{mins} min from Seattle"

def band(minutes):
    return "4+ hrs" if minutes >= 240 else "3-4hrs" if minutes >= 180 else "2-3hrs" if minutes >= 120 else "1-2hrs" if minutes >= 60 else "under-1hr"

def route_source(lat, lon):
    return f"https://router.project-osrm.org/route/v1/driving/-122.3321,47.6062;{lon},{lat}?overview=false&steps=false"

def main():
    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))["reviews"]
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source); fields, rows = list(reader.fieldnames or []), list(reader)
    by_slug = {row["Slug"]: row for row in rows}
    changed = 0
    for item in reviews:
        row = by_slug[item["slug"]]
        lat, lon, display = item["latitude"], item["longitude"], item["display_minutes"]
        updates = dict(CONTENT[item["slug"]])
        updates.update({
            "Data last updated": CHECKED, "Address": item["address"], "Latitude": str(lat), "Longitude": str(lon),
            "Google Maps Link": f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat},{lon}&travelmode=driving",
            "Coordinates source": item["coordinate_source"], "Coordinates checked": CHECKED, "Coordinate precision": item["precision"],
            "Drive distance miles": str(item["distance_miles"]), "Drive route minutes": str(item["observed_route_minutes"]),
            "Drive time origin": "Seattle, Washington", "Drive time source": route_source(lat, lon), "Drive time checked": CHECKED,
            "Drive time note": item["route_note"], "Drive Time Minutes": str(display), "Drive Time Band": band(display),
            "Time from Seattle": duration(display), "RV Access": "yes", "Access source": SOURCES[item["slug"]][0], "Access checked": CHECKED,
        })
        if item["slug"] == "whidbey-island-fairgrounds-campground":
            updates["Time from Seattle"] += " (via Mukilteo-Clinton ferry; allow for queues)"
        for key, value in updates.items():
            if row.get(key, "") != str(value):
                row[key] = str(value); changed += 1
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    slugs = {item["slug"] for item in reviews}
    critical = {"operating_status", "rv_access", "reservation_method", "max_rv_length", "hookups"}
    evidence["observations"] = [o for o in evidence["observations"] if not (o.get("slug") in slugs and o.get("field") in critical)]
    for slug in sorted(slugs):
        row = by_slug[slug]
        url, publisher, family = SOURCES[slug]
        values = {
            "operating_status": "active campground with current visitor information",
            "rv_access": True,
            "reservation_method": row["Reservation window"],
            "max_rv_length": MAX_VALUES[slug],
            "hookups": int(row["Hookups"]),
        }
        for field, value in values.items():
            if field == "max_rv_length" and value is None:
                summary = "Current source material does not publish one campground-wide RV maximum; the page directs travelers to confirm site-specific fit."
            else:
                summary = f"Current source material supports the reviewed {field.replace('_', ' ')} value and qualifications preserved in the canonical record."
            evidence["observations"].append({
                "slug": slug, "field": field, "status": "corrected_locally", "checked_on": CHECKED,
                "summary": summary, "proposed_value": value,
                "sources": [{"url": url, "publisher": publisher, "source_family": family, "evidence": summary}],
            })
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"Applied 10 final coordinate reviews; corrected {changed} canonical data fields and refreshed 50 critical evidence observations.")

if __name__ == "__main__":
    main()
