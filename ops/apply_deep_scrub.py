#!/usr/bin/env python3
"""Apply source-backed corrections from the 2026-09-06 full-content scrub."""
import csv
from pathlib import Path


MASTER = Path(__file__).resolve().parent / "data" / "campgrounds.csv"


def main():
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    by_slug = {row["Slug"]: row for row in rows}

    # Remove an obsolete State Park identity and unsupported ecology claims.
    row = by_slug["osoyoos-lake-veterans-memorial-state-park"]
    row.update({
        "Data last updated": "2026-09-06",
        "Things to do for families summary": "Swimming, boating, fishing, and lakeside camping near the Canadian border.",
        "Nearby nature & parks": "Osoyoos Lake Veteran's Memorial Park is a City of Oroville park in the Okanogan River Valley, just south of the U.S.–Canada border. The city lists a swimming area, boat launch, picnic areas, and standard, utility, primitive, and accessible campsites around the south end of Osoyoos Lake.",
    })

    # Replace a Grays Harbor/Ocean Shores paragraph copied onto this Long Beach page.
    row = by_slug["andersens-oceanside-rv-park"]
    row.update({
        "Data last updated": "2026-09-06",
        "Short Description": "Oceanfront private RV park on the Long Beach Peninsula with 60 full-hookup sites, 50/30/20-amp service, and direct beach access.",
        "Long description": "Andersen's Oceanside RV Park has 60 full-hookup RV sites on a seven-acre property on the Long Beach Peninsula. The operator lists 50/30/20-amp power, water, sewer, and a picnic table at every RV site, plus a sandy path to the beach. Downtown Long Beach is 3.5 miles away, Ocean Park is 6 miles away, and Cape Disappointment and Ilwaco are about 9 miles away. Reservations are required and same-day arrivals must book before noon.",
        "Nearby nature & parks": "The park sits on the Pacific side of the Long Beach Peninsula with direct access to the peninsula's broad sandy shoreline. The operator places downtown Long Beach 3.5 miles away, Ocean Park 6 miles away, and Ilwaco and Cape Disappointment about 9 miles away, making the campground a practical base for beach walks and peninsula day trips.",
        "Site Recommendations": "The operator groups its 60 sites into premium, forest, and prime areas. Ask about the premium end sites for the widest pads and closest beach access; the forest sites are seasonal and may have limited satellite reception. Reservations are required, and same-day arrivals must book before noon.",
        "Access source": "https://andersensrv.com/",
        "Access checked": "2026-09-06",
        "RV Access": "yes",
    })

    # Current NPS campground status and inventory.
    row = by_slug["hoh-campground"]
    row.update({
        "Data last updated": "2026-09-06",
        "Number of RV campsites": "78",
        "Max RV length": "",
        "Access note": "NPS lists 78 total sites; RV pads are generally 21 feet, with a few up to 35 feet.",
        "Access source": "https://www.nps.gov/olym/planyourvisit/camping.htm",
        "Access checked": "2026-09-06",
        "RV Access": "yes",
    })

    row = by_slug["ohanapecosh-campground"]
    row.update({
        "Data last updated": "2026-09-06",
        "Short Description": "Closed for the entire 2026 season during campground rehabilitation; NPS expects the improved Mount Rainier campground to reopen for summer 2027.",
        "Long description": "Ohanapecosh Campground and the surrounding developed area are closed to all visitor access for the entire 2026 season while the National Park Service rehabilitates 185 campsites and nine restroom buildings. Work is scheduled through November 2026, and NPS expects camping to reopen for summer 2027. Reservations for the 2027 season are expected to return to Recreation.gov in December 2026. Check the current NPS construction page before planning a stay.",
        "Number of RV campsites": "185",
        "Max RV length": "",
        "Reservation window": "Closed for 2026; 2027 reservations expected to open in December 2026",
        "Nearby nature & parks": "Ohanapecosh lies in an old-growth river valley on Mount Rainier's southeast side. The entire developed area is closed during 2026 construction, including the campground, visitor center, picnic area, river access, and campground trailheads. NPS lists alternate 2026 access points for the Silver Falls Trail from State Route 123 and Stevens Canyon Road.",
        "Access note": "No camping or visitor access in 2026; NPS expects the rehabilitated campground to reopen for summer 2027.",
        "Access source": "https://www.nps.gov/mora/planyourvisit/park-construction-faqs.htm",
        "Access checked": "2026-09-06",
        "RV Access": "yes",
    })

    # Current Recreation.gov facility details.
    corrections = {
        "horseshoe-cove-campground": {
            "Number of RV campsites": "39",
            "Max RV length": "40",
            "Short Description": "Baker Lake campground with 39 sites, including three group sites, plus a sandy swim beach, boat ramp, and forested shoreline setting.",
            "Long description": "Horseshoe Cove Campground has 39 campsites, including three large group sites, beneath forest canopy along Baker Lake. Recreation.gov lists a boat ramp, a large sandy swimming beach, a trail, and firewood at the campground. Several sites sit at or near the lake; confirm the fit of an individual parking spur for your RV during booking.",
            "Access source": "https://www.recreation.gov/camping/campgrounds/232059",
        },
        "johnny-creek-campground": {
            "Number of RV campsites": "65",
            "Max RV length": "65",
            "Short Description": "Two-loop Icicle Creek campground with 65 sites for tents, trailers, and RVs up to 65 feet, about 12 miles from Leavenworth.",
            "Long description": "Johnny Creek has 65 first-come, first-served campsites split between upper and lower loops near the confluence of Johnny Creek and Icicle Creek. Recreation.gov says the sites accept tents, trailers, and RVs up to 65 feet, with a table, fire ring, and grate at each site. Drinking water and vault toilets are available, and Leavenworth is about 12 miles away.",
            "Access source": "https://www.recreation.gov/camping/campgrounds/10250569",
        },
        "salmon-la-sac-campground": {
            "Number of RV campsites": "67",
            "Max RV length": "127",
            "Short Description": "Okanogan-Wenatchee National Forest campground between the Cle Elum and Cooper Rivers with 67 sites; one published pull-through accepts equipment up to 127 feet.",
            "Long description": "Salmon La Sac Campground has 67 sites for tents and RVs between the Cle Elum and Cooper Rivers; Recreation.gov currently lists 40 as reservable. The campground provides drinking water, trash collection, vault toilets, picnic tables, and campfire rings. Site 20 is a 127-foot pull-through, but many sites are much shorter, so match the booking to your full equipment length.",
            "Reservation window": "Check Recreation.gov for currently available dates",
            "Access source": "https://www.recreation.gov/camping/campgrounds/232094",
        },
    }
    for slug, values in corrections.items():
        values.update({"Data last updated": "2026-09-06", "Access checked": "2026-09-06", "RV Access": "yes"})
        by_slug[slug].update(values)

    # Big Creek is first-come and the old link led to an Indiana campground.
    row = by_slug["big-creek-campground"]
    row.update({
        "Data last updated": "2026-09-06",
        "Reservation website": "https://www.fs.usda.gov/recarea/olympic/recreation/camping-cabins/recarea/?actid=29&recid=79317",
        "Reservation window": "First-come, first-served",
        "Max RV length": "35",
        "Short Description": "First-come Olympic National Forest campground near Hoodsport with 64 units, a one-mile creek loop trail, and access toward Lake Cushman and Staircase.",
        "Long description": "Big Creek Campground has 64 first-come camp units in second-growth forest near Hoodsport. The Forest Service says the campground accepts tents, trailers, and RVs but its current web listing does not publish one campground-wide maximum length. Potable water and accessible vault toilets are available, and the one-mile Big Creek Campground Loop begins on site. Confirm your rig's fit and check the Forest Service page for current status before driving up Forest Road 24.",
        "Access note": "The current operator page confirms RV access but does not publish one campground-wide maximum length.",
        "Access source": "https://www.fs.usda.gov/recarea/olympic/recreation/camping-cabins/recarea/?actid=29&recid=79317",
        "Access checked": "2026-09-06",
        "RV Access": "yes",
    })

    # The old URL was for the reservable group kitchen, not the campground.
    row = by_slug["swan-lake-campground"]
    row.update({
        "Data last updated": "2026-09-06",
        "Reservation website": "https://www.recreation.gov/camping/campgrounds/10378408",
        "Reservation window": "First-come, first-served; check Recreation.gov for current payment details",
        "Access source": "https://www.recreation.gov/camping/campgrounds/10378408",
        "Access checked": "2026-09-06",
        "RV Access": "yes",
    })

    # Replace an outdated trail name, incorrect trail length, and unsupported river designation.
    row = by_slug["lake-easton-state-park"]
    row.update({
        "Data last updated": "2026-09-06",
        "Long description": "Lake Easton State Park is a 697-acre campground between Seattle and Ellensburg with 24,000 feet of freshwater access on Lake Easton and the Yakima River. The park has full-hookup and non-hookup camping, showers, a dump station, and selected sites that fit RVs up to 60 feet. The adjacent Palouse to Cascades State Park Trail supports hiking, bicycling, and horseback riding. I-90 traffic is audible from the campground, so light sleepers may want earplugs.",
        "Nearby nature & parks": "Lake Easton State Park sits in a forested Cascade foothills valley along Lake Easton and the Yakima River. The Palouse to Cascades State Park Trail runs beside the park, and the lake supports fishing, paddling, swimming, and motorized boating with a 10-horsepower limit. In winter, the area shifts to skiing, snowshoeing, dog sledding, and snowmobile access when snow conditions allow.",
        "Things to do for families": "Lake Easton beach swimming and fishing\nKayaking and paddleboarding on the lake\nHiking and biking the Palouse to Cascades State Park Trail\nWinter skiing and snowshoeing when conditions allow\nPlayground and picnic area\nScenic Cascade foothills driving",
        "Site Recommendations": "Selected campsites accommodate RVs up to 60 feet; confirm the individual pad before booking. Most RV spaces are near Lake Easton, while many standard sites sit nearer the Yakima River. Expect highway noise because the campground is close to I-90. Check the operator's winter schedule for seasonal loop closures and winter parking-area camping rules.",
        "Access source": "https://parks.wa.gov/find-parks/state-parks/lake-easton-state-park",
        "Access checked": "2026-09-06",
        "RV Access": "yes",
    })

    # Remove a dataset-wide universal claim that was never supported per campsite.
    for row in rows:
        text = row.get("Amenities summary", "")
        text = text.replace("Every site includes a fire pit.", "Fire pits are listed as available; check current fire restrictions with the operator.")
        text = text.replace("Every site has a fire pit.", "Fire pits are listed as available; check current fire restrictions with the operator.")
        text = text.replace("fire pits at every site", "fire pits listed as available")
        text = text.replace("fire pits and picnic tables at every site", "fire pits and picnic tables listed as available")
        row["Amenities summary"] = text

    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("Applied deep-scrub corrections and removed unsupported universal fire-pit wording.")


if __name__ == "__main__":
    main()
