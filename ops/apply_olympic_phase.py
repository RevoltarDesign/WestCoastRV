#!/usr/bin/env python3
"""Apply the first section-level verification pass: Olympic National Park."""
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
EVIDENCE = HERE / "verification-evidence.json"
NPS = "https://www.nps.gov/olym/planyourvisit/camping.htm"
CHECKED = "2026-09-06"


OLYMPIC = {
    "fairholme-campground": {
        "Number of RV campsites": "88", "Max RV length": "35", "RV Access": "yes",
        "Reservation window": "Seasonal reservations required May 15–September 29, 2026; sites open up to 6 months, 2 weeks, or 4 days ahead",
        "Access note": "Most sites fit 21-foot equipment; some fit equipment up to 35 feet.",
        "route": ("~3 hr 15 min from Seattle", "195", "165", "182", "Fastest no-ferry option; ferry routes may be shorter but add fare and wait-time uncertainty."),
    },
    "heart-o-the-hills-campground": {
        "Number of RV campsites": "97", "Max RV length": "35", "RV Access": "yes",
        "Reservation window": "First-come, first-served", "Reservation website": NPS,
        "Address": "2823 S Oak St, Port Angeles, WA 98362",
        "Access note": "Most sites fit 21-foot equipment; a few fit equipment up to 35 feet. Walk-in access may apply during heavy snow.",
        "coords": (48.0363165, -123.4297563, "Google Maps named campground pin, corroborated by the official NPS listing"),
        "route": ("~2 hr 45 min from Seattle", "165", "143", "157", "Fastest no-ferry option; ferry routes may be shorter but add fare and wait-time uncertainty."),
    },
    "hoh-campground": {
        "Number of RV campsites": "78", "Max RV length": "35", "RV Access": "yes",
        "Reservation window": "Seasonal reservations required June 12–September 6, 2026; first-come outside that period",
        "Access note": "Most sites fit 21-foot equipment; a few fit equipment up to 35 feet. No dump station.",
        "route": ("~4 hr 15 min from Seattle", "255", "216", "245", "Fastest normal route at review time; traffic and park-road conditions vary."),
    },
    "kalaloch-campground": {
        "Number of RV campsites": "170", "Max RV length": "35", "RV Access": "yes",
        "Reservation window": "Seasonal reservations required May 15–September 20, 2026; first-come outside that period",
        "Access note": "Most sites fit 21-foot equipment; a few fit equipment up to 35 feet.",
        "route": ("~3 hr 15 min from Seattle", "195", "177", "186", "Fastest normal route at review time; traffic and park-road conditions vary."),
    },
    "mora-campground": {
        "Number of RV campsites": "94", "Max RV length": "35", "RV Access": "yes",
        "Reservation window": "Seasonal reservations required May 15–September 20, 2026; first-come outside that period",
        "Access note": "Most sites fit 21-foot equipment; a few fit equipment up to 35 feet. The Recreation.gov coordinate is invalid, so the named campground pin was retained.",
        "coords": (47.9158, -124.5973, "Google Maps named campground pin; Recreation.gov API returned invalid 0,0 coordinates"),
        "route": ("~4 hr 15 min from Seattle", "255", "223", "247", "Fastest no-ferry option; ferry routes may be shorter but add fare and wait-time uncertainty."),
    },
    "ozette-campground": {
        "Number of RV campsites": "15", "Max RV length": "21", "RV Access": "yes",
        "Reservation window": "First-come, first-served", "Reservation website": NPS,
        "Address": "21083 Hoko-Ozette Rd, Clallam Bay, WA 98326",
        "Access note": "Sites fit equipment up to 21 feet. Some sites may flood in winter; facilities become primitive in winter.",
        "coords": (48.1527628, -124.6665665, "Google Maps named campground pin, corroborated by the official NPS listing"),
        "route": ("~4 hr 15 min from Seattle", "255", "160", "248", "Fastest no-ferry option; ferry routes may be shorter but add fare and wait-time uncertainty."),
    },
    "sol-duc-campground": {
        "Number of RV campsites": "17", "Max RV length": "36", "RV Access": "yes",
        "Reservation window": "Reservable up to 6 months in advance",
        "Access note": "The 17-site RV Park has water and electric hookups and accepts vehicles from 26 to 36 feet; the separate 82-site campground is mostly shorter and has no site hookups.",
        "route": ("~3 hr 30 min from Seattle", "210", "178", "203", "Fastest no-ferry option; ferry routes may be shorter but add fare and wait-time uncertainty."),
    },
    "south-beach-campground": {
        "Number of RV campsites": "55", "Max RV length": "35", "RV Access": "yes",
        "Reservation window": "First-come, first-served", "Reservation website": NPS,
        "Access note": "Most sites fit 21-foot equipment; a few fit equipment up to 35 feet. No potable water.",
        "coords": (47.567457, -124.3615252, "Google Maps named campground pin, corroborated by the official NPS listing"),
        "route": ("~3 hr 15 min from Seattle", "195", "174", "185", "Fastest normal route at review time; traffic and park-road conditions vary."),
    },
    "staircase-campground": {
        "Number of RV campsites": "49", "Max RV length": "35", "RV Access": "yes",
        "Reservation window": "Seasonal reservations required July 8–September 29, 2026; first-come outside that period",
        "Access note": "Most sites fit 21-foot equipment; a few fit equipment up to 35 feet. Access includes a winding gravel road beyond Lake Cushman.",
        "route": ("~2 hr 15 min from Seattle", "135", "112", "128", "Fastest normal route at review time; the final road is winding and partly gravel."),
    },
    "graves-creek-campground": {
        "Number of RV campsites": "0", "Max RV length": "", "RV Access": "no",
        "Reservation window": "First-come, first-served", "Reservation website": NPS,
        "Access note": "RVs and trailers are not allowed because of road conditions.",
        "coords": (47.5739181, -123.5794138, "Google Maps named campground pin, corroborated by the official NPS listing"),
        "route": ("~3 hr 45 min from Seattle", "225", "169", "212", "Passenger-vehicle route only; NPS prohibits RVs and trailers on the access road."),
    },
}

OSOYOOS = {
    "Address": "417 Ironwood St, Oroville, WA 98844",
    "Reservation website": "https://book.letsbonfire.com/osoyooslakeveteransmemorialpark",
    "Reservation window": "2026 reservations opened January 1, 2026; check current availability",
    "Things to do for families": "Swimming from the sandy beach\nBoating and watersports\nFishing\nBird watching\nPickleball and horseshoes\nNearby hiking and biking trails",
    "Site Recommendations": "The city lists 41 standard sites, 39 power-and-water utility sites, 12 walk-in primitive sites, and two accessible sites. Match the reservation category to your rig and utility needs, and confirm the individual site dimensions before booking. The park also has a trailer dump, restroom and shower complex, boat launch, and swimming area.",
    "coords": (48.9286, -119.4378, "Google Maps park point, checked against the City of Oroville park listing"),
    "route": ("~4 hr 45 min from Seattle", "285", "274", "277", "Fastest normal route at review time; seasonal pass and traffic conditions vary."),
}


def route_url(lat, lon):
    return f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat},{lon}&travelmode=driving"


def apply_route(row, route):
    public, rounded, miles, observed, note = route
    row.update({
        "Time from Seattle": public, "Drive Time Minutes": rounded,
        "Drive Time Band": "4+ hrs" if int(rounded) >= 240 else "3-4hrs" if int(rounded) >= 180 else "2-3hrs",
        "Drive distance miles": miles, "Drive route minutes": observed,
        "Drive time origin": "Seattle, Washington", "Drive time source": route_url(row["Latitude"], row["Longitude"]),
        "Drive time checked": CHECKED, "Drive time note": note,
    })


def main():
    with MASTER.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields, rows = list(reader.fieldnames or []), list(reader)
    extra = ["Latitude", "Longitude", "Coordinates source", "Coordinates checked", "Coordinate precision",
             "Drive distance miles", "Drive route minutes", "Drive time origin", "Drive time source",
             "Drive time checked", "Drive time note"]
    for field in extra:
        if field not in fields:
            fields.append(field)
    by_slug = {row["Slug"]: row for row in rows}

    for slug, changes in OLYMPIC.items():
        row = by_slug[slug]
        row.update({k: v for k, v in changes.items() if k not in {"coords", "route"}})
        row.update({"Data last updated": CHECKED, "Access source": NPS, "Access checked": CHECKED})
        if "coords" in changes:
            lat, lon, source = changes["coords"]
            row.update({"Latitude": str(lat), "Longitude": str(lon), "Google Maps Link": f"https://www.google.com/maps?q={lat},{lon}",
                        "Coordinates source": source, "Coordinates checked": CHECKED, "Coordinate precision": "named campground point"})
        apply_route(row, changes["route"])

    osoyoos = by_slug["osoyoos-lake-veterans-memorial-state-park"]
    osoyoos.update({k: v for k, v in OSOYOOS.items() if k not in {"coords", "route"}})
    lat, lon, source = OSOYOOS["coords"]
    osoyoos.update({"Latitude": str(lat), "Longitude": str(lon), "Google Maps Link": f"https://www.google.com/maps?q={lat},{lon}",
                    "Coordinates source": source, "Coordinates checked": CHECKED, "Coordinate precision": "park entrance/address point",
                    "Data last updated": CHECKED})
    apply_route(osoyoos, OSOYOOS["route"])

    with MASTER.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    olympic_slugs = set(OLYMPIC)
    critical = {"operating_status", "rv_access", "reservation_method", "max_rv_length", "hookups"}
    evidence["observations"] = [o for o in evidence["observations"] if not (o.get("slug") in olympic_slugs and o.get("field") in critical)]
    source = {"url": NPS, "publisher": "National Park Service", "source_family": "nps-olympic-camping"}
    for slug, changes in OLYMPIC.items():
        row = by_slug[slug]
        values = {
            "operating_status": "open/currently listed by NPS",
            "rv_access": row["RV Access"] == "yes",
            "reservation_method": row["Reservation window"],
            "max_rv_length": int(row["Max RV length"]) if row["Max RV length"] else None,
            "hookups": int(row["Hookups"]),
        }
        for field, value in values.items():
            status = "corrected_locally" if slug in {"fairholme-campground", "heart-o-the-hills-campground", "hoh-campground", "staircase-campground"} and field in {"reservation_method", "max_rv_length"} else "supported"
            evidence_text = {
                "operating_status": "The current campground section publishes its operating status and seasonal limitations.",
                "rv_access": "The current campground section states whether RVs and trailers are allowed and gives equipment guidance.",
                "reservation_method": "The current campground section states the 2026 reservation or first-come rules.",
                "max_rv_length": "The current campground section publishes the equipment length range, or explicitly prohibits RVs and trailers.",
                "hookups": "The NPS facility lists identify the dedicated Sol Duc RV hookup area; the other reviewed park campgrounds list basic facilities without site hookups.",
            }[field]
            evidence["observations"].append({"slug": slug, "field": field, "status": status,
                "checked_on": CHECKED, "summary": evidence_text, "proposed_value": value,
                "sources": [{**source, "evidence": evidence_text}]})
    osoyoos_slug = "osoyoos-lake-veterans-memorial-state-park"
    evidence["observations"] = [o for o in evidence["observations"] if not (o.get("slug") == osoyoos_slug and o.get("field") in critical)]
    city_source = {"url": "https://oroville-wa.com/departments/parks-department/", "publisher": "City of Oroville",
                   "source_family": "city-of-oroville-parks"}
    osoyoos_values = {"operating_status": "active 2026 reservation listing", "rv_access": True,
                      "reservation_method": OSOYOOS["Reservation window"], "max_rv_length": None, "hookups": 2}
    osoyoos_evidence = {
        "operating_status": "The city publishes current park contacts and links to the active 2026 reservation system.",
        "rv_access": "The city lists standard and utility campsites plus a trailer dump.",
        "reservation_method": "The city links directly to the 2026 Bonfire reservation page.",
        "max_rv_length": "The current city page does not publish a campground-wide maximum RV length, so the site leaves it unconfirmed.",
        "hookups": "The city lists 39 utility sites with power and water plus one accessible power-and-water site.",
    }
    for field, value in osoyoos_values.items():
        evidence["observations"].append({"slug": osoyoos_slug, "field": field, "status": "supported",
            "checked_on": CHECKED, "summary": osoyoos_evidence[field], "proposed_value": value,
            "sources": [{**city_source, "evidence": osoyoos_evidence[field]}]})
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("Applied 10-campground Olympic NPS verification and 11 reviewed Seattle route records.")


if __name__ == "__main__":
    main()
