#!/usr/bin/env python3
"""Remove cross-region content and refresh Silver Lake Park from Whatcom County sources."""
import csv
from pathlib import Path


MASTER = Path(__file__).resolve().parent / "data" / "campgrounds.csv"


def main():
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    row = next(item for item in rows if item["Slug"] == "silver-lake-park")
    row.update({
        "Data last updated": "2026-09-06",
        "Reservation website": "https://www.whatcomcounty.us/3517/Silver-Lake-Park",
        "Reservation window": "Reservations for the next calendar year open the first business day of December",
        "Short Description": "Whatcom County lake campground near Maple Falls with two water-and-electric RV areas, seasonal showers, paddling, fishing, and forest trails.",
        "Long description": "Silver Lake Park is a 410-acre Whatcom County park in the Cascade foothills, about 40 minutes east of Bellingham. Maple Creek and Red Mountain are the park's two RV campgrounds, both with water and electric hookups; a separate Cedar campground is intended for tents, cars, and vans, and a reservable group camp also accepts RVs. The lake has a boat launch and seasonal canoe, kayak, rowboat, pedal boat, and paddleboard rentals. Campground connector, forest canopy, and equestrian trails add options away from the water.",
        "Number of RV campsites": "",
        "Max RV length": "",
        "Cell coverage": "0",
        "Things to do for families": "Fishing for rainbow and coastal cutthroat trout\nBoating with a 10-horsepower motor limit\nSeasonal canoe, kayak, and paddleboard rentals\nSwimming and lakeside picnics\nCampground Connector and Canopy Loop trails\nBlack Mountain equestrian trail\nPlayground",
        "Things to do for families summary": "Lake fishing, small-boat paddling, forest trails, and a playground in the Cascade foothills east of Bellingham.",
        "Nearby nature & parks": "Silver Lake Park covers 410 acres in Whatcom County's Cascade foothills near Maple Falls. Its 5.75-mile trail system connects the lake, three campground areas, quiet forest canopy, meadows, and the base of Red Mountain. Silver Lake is a local fishing and boating destination for rainbow and coastal cutthroat trout, with a 10-horsepower motor limit that keeps the water oriented toward smaller craft.",
        "Amenities summary": "Vault toilets are available in each campground. Maple Creek and Red Mountain add seasonal flush toilets and showers; drinking water and a seasonal dump station are available.",
        "Site Recommendations": "Choose Maple Creek for the easiest access to the boat launch, beach, picnic area, and playground. Red Mountain sits about three-quarters of a mile from the lake and suits campers who prefer woods, meadow edges, hiking, or equestrian access. Cedar Campground does not allow vehicles over 25 feet and is not recommended for RVs. Whatcom County reports no cell service or Wi-Fi, so save maps and reservation details before arrival.",
        "RV Access": "yes",
        "Access note": "Maple Creek and Red Mountain accept RVs; Cedar is not recommended for RVs and prohibits vehicles over 25 feet.",
        "Access source": "https://www.whatcomcounty.us/3518/Camping-at-Silver-Lake-Park/messages",
        "Access checked": "2026-09-06",
    })
    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("Corrected Silver Lake Park's region, facilities, and current operating details.")


if __name__ == "__main__":
    main()
