#!/usr/bin/env python3
"""Apply operator-link fixes found by the 2026-09-06 full URL audit."""
import csv
from pathlib import Path


MASTER = Path(__file__).resolve().parent / "data" / "campgrounds.csv"


def main():
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    by_slug = {row["Slug"]: row for row in rows}
    by_slug["lewis-and-clark-state-park"]["Reservation website"] = "https://parks.wa.gov/find-parks/state-parks/lewis-clark-state-park"
    by_slug["thousand-trails-leavenworth"]["Reservation website"] = "https://thousandtrails.com/washington/leavenworth-rv-campground/"

    osoyoos = by_slug["osoyoos-lake-veterans-memorial-state-park"]
    osoyoos.update({
        "Name": "Osoyoos Lake Veteran's Memorial Park",
        "Data last updated": "2026-09-06",
        "Park Type": "City Campground",
        "Reservation website": "https://oroville-wa.com/departments/parks-department/",
        "Reservation window": "Contact the City of Oroville for current reservations",
        "Short Description": "City of Oroville campground on Osoyoos Lake with standard and water-and-electric sites, showers, a swim beach, boat launch, and trailer dump.",
        "Long description": "Osoyoos Lake Veteran's Memorial Park is a City of Oroville campground on the south shore of Osoyoos Lake near the Canadian border. It is a municipal park, not a Washington State Park, so a Discover Pass does not apply. The city lists standard campsites, water-and-electric utility sites, walk-in primitive sites, accessible sites, a restroom and shower complex, picnic areas, a swimming area, boat launch, and trailer dump.",
        "Number of RV campsites": "",
        "Max RV length": "",
        "Hookups": "2",
        "Access note": "The city lists standard and water-and-electric vehicle campsites but does not publish one park-wide RV length limit.",
        "Access source": "https://oroville-wa.com/departments/parks-department/",
        "Access checked": "2026-09-06",
        "RV Access": "yes",
    })

    beachside = by_slug["beachside-rv-park"]
    beachside.update({
        "Data last updated": "2026-09-06",
        "Reservation website": "https://birchbaywa.org/birch-bay-rv-parks/",
        "Reservation window": "Contact the campground for current availability",
        "Number of RV campsites": "72",
        "Max RV length": "",
        "Short Description": "Year-round private RV park across from Birch Bay with full hookups and walkable access to the bay, restaurants, and local activities.",
        "Long description": "Beachside RV Park is a year-round private campground across Birch Bay Drive from the protected waters of Birch Bay. The local destination organization lists 72 sites and describes the park as ten minutes from Canada and twenty minutes from Bellingham. Full-hookup RV sites, a walkable waterfront setting, and nearby restaurants make it a practical northern Washington stop; confirm current site dimensions and availability directly with the operator.",
        "Nearby nature & parks": "Birch Bay's broad, shallow saltwater shoreline warms at low tide and supports easy beach walks, paddling, bird watching, and seasonal shellfish exploration. Birch Bay State Park is a short drive south, adding more public shoreline, forest, and picnic space, while the Canadian border and Bellingham are straightforward day trips from camp.",
        "Site Recommendations": "The park sits across the road from Birch Bay and within walking distance of local restaurants and activities. Sites are close together in a traditional private RV-park layout, so ask the operator about the best fit for your slide-outs and total equipment length. Save the campground phone number before arrival because the operator website currently has a certificate problem.",
        "Access note": "The park accepts RVs, but a current operator-published maximum length was not available during review.",
        "Access source": "https://birchbaywa.org/birch-bay-rv-parks/",
        "Access checked": "2026-09-06",
        "RV Access": "yes",
    })

    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("Applied three repaired operator links and one safe directory fallback.")


if __name__ == "__main__":
    main()
