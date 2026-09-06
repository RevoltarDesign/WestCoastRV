#!/usr/bin/env python3
"""Apply the reviewed Jefferson County state-park pilot to the master dataset."""
import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"


NEW_CAMPGROUNDS = [
    {
        "Name": "Dosewallips State Park",
        "Slug": "dosewallips-state-park",
        "Data last updated": "2026-09-06",
        "Nearby campgrounds": "seal-rock-campground;potlatch-state-park;fort-worden-historical-state-park;fort-flagler-historical-state-park",
        "Archived": "false",
        "Draft": "false",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/dosewallips-state-park.jpg",
        "Short Description": "Hood Canal state park with standard, water-and-electric, and full-hookup camping for RVs up to 40 feet, plus river and shoreline access.",
        "Park Type": "State Park",
        "Reservation window": "Reservable up to 9 months in advance",
        "Reservation website": "https://parks.wa.gov/find-parks/state-parks/dosewallips-state-park",
        "Long description": "Dosewallips State Park spans both sides of Highway 101 where the Dosewallips River reaches Hood Canal. The developed campground mixes standard sites with water-and-electric and full-hookup options, and the park accommodates RVs and vehicle-trailer combinations up to 40 feet. Campers have access to flush restrooms, showers, drinking water, a dump station, forest trails, river access, and a Hood Canal shoreline. Camping is offered year-round, though water service is limited to a smaller winter loop from mid-November through March.",
        "Time from Seattle": "~2 hr 25 min from Seattle",
        "Drive Time Band": "2-3hrs",
        "Drive Time Minutes": "145",
        "Address": "306996 Highway 101, Brinnon, WA 98320",
        "Number of RV campsites": "",
        "Max RV length": "40",
        "Maneuverability": "2",
        "Site surface type": "Mixed",
        "Hookups": "3",
        "Dump station on site": "true",
        "Generator policy": "1",
        "Cell coverage": "2",
        "Things to do for families": "Walk the forest and river trails\nExplore the Hood Canal shoreline\nFish the Dosewallips River and Hood Canal\nSwim or paddle when conditions allow\nWatch for elk, eagles, and marine wildlife",
        "Things to do for families summary": "A flexible Hood Canal base for river walks, shoreline exploring, fishing, and paddling.",
        "Nearby nature & parks": "The park connects a lowland forest and the Dosewallips River with Hood Canal shoreline, making it easy to experience several Olympic Peninsula habitats in one stop. Olympic National Park trailheads lie farther up the Dosewallips valley, while nearby Seal Rock adds another public shoreline and a short interpretive trail.",
        "Hiking": "true",
        "Fishing": "true",
        "Swimming": "true",
        "Kayaking/Paddling": "true",
        "Beach & Tide Pools": "true",
        "Boating": "false",
        "Playground": "false",
        "Amenities: Toilets": "Flush toilets",
        "Amenities: Showers": "true",
        "Amenities: Drinking water": "true",
        "Amenities: Fire pits": "true",
        "Amenities summary": "Flush restrooms, showers, drinking water, and a dump station serve the developed campground. Water service is reduced in winter.",
        "Nearest town": "Brinnon, WA",
        "Site Recommendations": "Use the current campground map to match your rig and hookup needs: sites 2–5 and 11–40 are marked full hookup; sites 53–58, 71–73, and 77–92 are marked water and electric. From November 15 through March 31, the park says water is available only at sites 21–29. Individual pad length varies, so confirm your exact equipment length while booking.",
        "Google Maps Link": "https://www.google.com/maps?q=47.69636536,-122.9194565",
        "State Map": "",
        "RV Access": "yes",
        "Access note": "Official park guidance allows RVs and vehicle-trailer combinations up to 40 feet; individual site limits vary.",
        "Access source": "https://parks.wa.gov/find-parks/state-parks/dosewallips-state-park",
        "Access checked": "2026-09-06",
    },
    {
        "Name": "Fort Flagler Historical State Park",
        "Slug": "fort-flagler-historical-state-park",
        "Data last updated": "2026-09-06",
        "Nearby campgrounds": "fort-worden-historical-state-park;fort-casey-historical-state-park;sequim-bay-state-park;dosewallips-state-park",
        "Archived": "false",
        "Draft": "false",
        "Topographic background image": "https://westcoastrvcamping.com/assets/images/topo/fort-flagler-historical-state-park.jpg",
        "Short Description": "Spacious RV camping on Marrowstone Island with standard, partial, and full-hookup sites, beaches, historic batteries, and rigs up to 50 feet.",
        "Park Type": "State Park",
        "Reservation window": "Reservable up to 9 months in advance",
        "Reservation website": "https://parks.wa.gov/find-parks/state-parks/fort-flagler-historical-state-park",
        "Long description": "Fort Flagler Historical State Park occupies the north end of Marrowstone Island, with broad views across Admiralty Inlet and Port Townsend Bay. Its two developed campgrounds offer different experiences: the Lower Campground has standard, partial-hookup, and full-hookup sites near the water, while the Upper Campground has more private standard sites in the forest. Official park materials list 59 standard and 55 full-hookup sites and accommodate RVs up to 50 feet. Campers can walk historic coastal-defense batteries, hike shoreline trails, paddle from the beach, and use flush restrooms, showers, drinking water, and a dump station.",
        "Time from Seattle": "~2 hr 15 min from Seattle",
        "Drive Time Band": "2-3hrs",
        "Drive Time Minutes": "135",
        "Address": "10541 Flagler Road, Nordland, WA 98358",
        "Number of RV campsites": "114",
        "Max RV length": "50",
        "Maneuverability": "1",
        "Site surface type": "Mixed",
        "Hookups": "3",
        "Dump station on site": "true",
        "Generator policy": "1",
        "Cell coverage": "2",
        "Things to do for families": "Explore historic gun batteries and military buildings\nWalk beaches and shoreline trails\nKayak or paddleboard on protected water\nFish and watch boats in Admiralty Inlet\nVisit the park museum and interpretive displays",
        "Things to do for families summary": "Historic fort exploration, beach walks, paddling, and roomy campground loops on Marrowstone Island.",
        "Nearby nature & parks": "Fort Flagler sits where Port Townsend Bay meets Admiralty Inlet, with shoreline on three sides and long views toward Whidbey Island and the Olympic Mountains. The park's trails link beaches, bluff overlooks, forest, and the remains of the Harbor Defenses of Puget Sound. Fort Worden and Fort Casey form the other two points of the historic Triangle of Fire and make natural follow-on stops.",
        "Hiking": "true",
        "Fishing": "true",
        "Swimming": "true",
        "Kayaking/Paddling": "true",
        "Beach & Tide Pools": "true",
        "Boating": "true",
        "Playground": "true",
        "Amenities: Toilets": "Flush toilets",
        "Amenities: Showers": "true",
        "Amenities: Drinking water": "true",
        "Amenities: Fire pits": "true",
        "Amenities summary": "Flush restrooms, showers, drinking water, and a dump station serve the developed campgrounds.",
        "Nearest town": "Port Townsend, WA",
        "Site Recommendations": "Choose the Lower Campground for water views and standard, partial-hookup, or full-hookup choices; choose the Upper Campground for a quieter forest setting with standard sites. The lower campground is reservable year-round beginning in 2026, while upper-loop availability changes seasonally. Confirm the length limit for the exact site even though the park accommodates RVs up to 50 feet.",
        "Google Maps Link": "https://www.google.com/maps?q=48.085842,-122.701643",
        "State Map": "",
        "RV Access": "yes",
        "Access note": "Official park materials list RV accommodation up to 50 feet; individual site limits vary.",
        "Access source": "https://parks.wa.gov/find-parks/state-parks/fort-flagler-historical-state-park",
        "Access checked": "2026-09-06",
    },
]


NEARBY_UPDATES = {
    "fort-worden-historical-state-park": "fort-flagler-historical-state-park;fort-casey-historical-state-park;fort-ebey-state-park;sequim-bay-state-park",
    "seal-rock-campground": "dosewallips-state-park;potlatch-state-park;illahee-state-park;big-creek-campground",
    "potlatch-state-park": "dosewallips-state-park;big-creek-campground;staircase-campground;twanoh-state-park",
}


def main():
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    by_slug = {row["Slug"]: row for row in rows}
    for slug, nearby in NEARBY_UPDATES.items():
        by_slug[slug]["Nearby campgrounds"] = nearby

    for facts in NEW_CAMPGROUNDS:
        slug = facts["Slug"]
        row = {field: "" for field in fields}
        row.update(facts)
        if slug in by_slug:
            by_slug[slug].update(facts)
        else:
            rows.append(row)
            by_slug[slug] = row

    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Master dataset now contains {len(rows)} campgrounds.")


if __name__ == "__main__":
    main()
