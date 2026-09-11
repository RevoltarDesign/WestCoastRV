#!/usr/bin/env python3
"""Publish the reviewed Jefferson County Washington DNR campground layer."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "data" / "campgrounds.csv"
REVIEWS = HERE / "jefferson-dnr-location-reviews.json"
EVIDENCE = HERE / "verification-evidence.json"
COVERAGE = HERE / "coverage-inventory.json"
CHECKED = "2026-09-10"
DNR = "https://dnr.wa.gov/forest-and-trust-lands/olympic-peninsula-forests"
DNR_STATUS = "https://dnr.wa.gov/recreation/find-your-campsite"
DNR_GUIDE = "https://dnr.wa.gov/sites/default/files/publications/amp_recreation_guide.pdf"

CAMPS = {
  "coppermine-bottom-campground": {
    "Name":"Coppermine Bottom Campground", "Maneuverability":"1",
    "Short Description":"Primitive first-come DNR campground beside the Clearwater River with dry sites for trailers up to 30 feet and a long gravel forest-road approach.",
    "Long description":"Coppermine Bottom is a primitive Washington DNR campground beside the Clearwater River southwest of Forks. DNR allows trailers up to 30 feet and currently lists the campground open. Sites are first-come, a Discover Pass is required for vehicle access, and there are no hookups or potable water. DNR does not publish a current site total, and community sources disagree, so this listing leaves the count unconfirmed. The final approach follows active forest roads; check DNR alerts and road conditions before towing.",
    "Access note":"From US 101 near milepost 147, follow Hoh-Clearwater Mainline about 12.6 miles, then C-1010 about 1.5 miles. Active forest operations may affect access.",
    "Site Recommendations":"Best for smaller, self-contained rigs comfortable with a long gravel approach. Bring water, pack out trash, and do not depend on cell service.",
    "Nearby campgrounds":"south-fork-hoh-campground;cottonwood-campground;kalaloch-campground;bogachiel-state-park",
  },
  "cottonwood-campground": {
    "Name":"Cottonwood Campground", "Maneuverability":"2",
    "Short Description":"Primitive DNR campground near the lower Hoh River with first-come dry sites for trailers up to 30 feet, reached from Oil City Road.",
    "Long description":"Cottonwood is a primitive Washington DNR campground in the lower Hoh River forest near Forks. DNR allows trailers up to 30 feet and currently lists the facility open. Camping is first-come with a Discover Pass required for vehicle access; there are no hookups, potable water, showers, or dump station. DNR does not publish a current site count and community reports vary, so confirm space and turning room on arrival.",
    "Access note":"From US 101 between mileposts 177 and 178, take Oil City Road about 2.3 miles and H-4060 about 0.9 mile to the campground.",
    "Site Recommendations":"Arrive with water and choose a site only after checking the full loop and exit path. Turning room varies among the wooded sites.",
    "Nearby campgrounds":"hoh-oxbow-campground;kalaloch-campground;south-beach-campground;bogachiel-state-park",
  },
  "hoh-oxbow-campground": {
    "Name":"Hoh Oxbow Campground", "Maneuverability":"2", "Number of RV campsites":"8",
    "Short Description":"Eight-site first-come DNR campground beside a Hoh River oxbow, with dry camping for trailers up to 30 feet and direct access near US 101.",
    "Long description":"Hoh Oxbow is an eight-site Washington DNR campground beside a quiet Hoh River oxbow east of US 101. DNR allows trailers up to 30 feet and provides a toilet, but no hookups, potable water, showers, or dump station. Camping is first-come and a Discover Pass is required for vehicle access. DNR has scheduled a full public-access closure from September 14 through October 13, 2026 for Hoh Bridge work; check the live status page before travel.",
    "Reservation window":"First-come, first-served; scheduled closure September 14–October 13, 2026",
    "Access note":"The campground is directly east of US 101 between mileposts 176 and 177. DNR has scheduled no public access September 14–October 13, 2026 for bridge work.",
    "Site Recommendations":"A simpler DNR choice for rigs that want to avoid the longest forest-road approaches. Confirm the scheduled 2026 bridge closure has ended before travel.",
    "Amenities: Toilets":"Toilets",
    "Nearby campgrounds":"cottonwood-campground;minnie-peterson-campground;hard-rain-cafe-campground;hoh-campground",
  },
  "minnie-peterson-campground": {
    "Name":"Minnie Peterson Campground", "Maneuverability":"1", "Number of RV campsites":"9",
    "Short Description":"Nine-site primitive DNR campground on Upper Hoh Road with first-come dry camping beside a forest creek for trailers up to 30 feet.",
    "Long description":"Minnie Peterson is a nine-site Washington DNR campground beside a forest creek on Upper Hoh Road. DNR allows trailers up to 30 feet and currently lists the campground open. Sites are first-come, a Discover Pass is required for vehicle access, and there are no hookups, potable water, showers, or dump station. The small wooded loop can feel tight, so inspect the site and exit path before committing a longer trailer.",
    "Access note":"Follow Upper Hoh Road to about one mile beyond Willoughby Creek. The exact DNR-linked campground point is on the north side of the road.",
    "Site Recommendations":"Best for compact rigs and travelers who bring water and can dry camp. Walk the loop first if your trailer approaches 30 feet.",
    "Nearby campgrounds":"hard-rain-cafe-campground;hoh-campground;hoh-oxbow-campground;south-fork-hoh-campground",
  },
  "south-fork-hoh-campground": {
    "Name":"South Fork Hoh Campground", "Maneuverability":"1",
    "Short Description":"Remote primitive DNR campground on the South Fork Hoh River with first-come dry sites for trailers up to 30 feet and a long forest-road approach.",
    "Long description":"South Fork Hoh is a remote primitive Washington DNR campground beside the South Fork Hoh River. DNR allows trailers up to 30 feet and currently lists the campground open. Camping is first-come, a Discover Pass is required for vehicle access, and the site has no hookups, potable water, showers, or dump station. Community sources report a small loop and unreliable cell service, while DNR warns that forest operations occur along the access roads. Treat this as a self-contained, road-condition-dependent trip.",
    "Access note":"From US 101 near milepost 176, follow Hoh Mainline about 6.6 miles, then H-1000 about 7.4 miles. Active forest operations may affect the long primitive approach.",
    "Site Recommendations":"Use a smaller rig, bring water and emergency supplies, and allow extra time for roughly 14 miles of forest-road access. Do not rely on cell coverage.",
    "Nearby campgrounds":"minnie-peterson-campground;hard-rain-cafe-campground;hoh-campground;coppermine-bottom-campground",
  },
}

def duration(minutes):
    h, m = divmod(minutes, 60)
    return f"~{h} hr {m} min from Seattle" if m else f"~{h} hr from Seattle"

def source(url, publisher, evidence):
    return {"url":url,"publisher":publisher,"source_family":"jefferson-dnr-review","evidence":evidence}

def main():
    reviews = {r["slug"]:r for r in json.loads(REVIEWS.read_text())["reviews"]}
    with MASTER.open(newline="", encoding="utf-8-sig") as f:
        reader=csv.DictReader(f); fields=list(reader.fieldnames or []); rows=list(reader)
    by_slug={r["Slug"]:r for r in rows}
    common={
      "Data last updated":CHECKED,"Archived":"false","Draft":"false","Park Type":"State Forest","RV Access":"yes",
      "Reservation window":"First-come, first-served; Discover Pass required for vehicle access","Reservation website":DNR,
      "Max RV length":"30","Site surface type":"Dirt","Hookups":"0","Dump station on site":"false","Generator policy":"",
      "Cell coverage":"0","Amenities: Toilets":"Vaulted toilets","Amenities: Showers":"false","Amenities: Drinking water":"false","Amenities: Fire pits":"true",
      "Amenities summary":"Primitive dry camping with a toilet and fire rings. No hookups, potable water, showers, or dump station; pack out trash and obey current fire restrictions.",
      "Nearest town":"Forks, WA","Access source":DNR,"Access checked":CHECKED,
      "Things to do for families":"Explore temperate rain forest\nWatch the river from camp\nLook for birds and wildlife\nVisit the Hoh Rain Forest\nPractice leave-no-trace camping",
      "Things to do for families summary":"A quiet, primitive forest base for river scenery, wildlife watching, and Hoh Rain Forest day trips.",
      "Nearby nature & parks":"These DNR sites sit in the wet forests and river valleys west of Olympic National Park, with the Hoh Rain Forest, Pacific beaches, and working state trust lands nearby.",
      "Hiking":"true","Fishing":"true","Swimming":"false","Kayaking/Paddling":"false","Beach & Tide Pools":"false","Boating":"false","Playground":"false",
    }
    for slug, specific in CAMPS.items():
        row=by_slug.get(slug,{k:"" for k in fields}); row.update(common); row.update(specific); row["Slug"]=slug
        rev=reviews[slug]; lat,lon=rev["latitude"],rev["longitude"]
        row.update({"Address":rev["address"],"Latitude":f"{lat:.7f}","Longitude":f"{lon:.7f}","Google Maps Link":f"https://www.google.com/maps?q={lat:.7f},{lon:.7f}","Coordinates source":rev["coordinate_source"],"Coordinates checked":CHECKED,"Coordinate precision":rev["precision"],"Drive distance miles":str(rev["distance_miles"]),"Drive route minutes":str(rev["observed_route_minutes"]),"Drive Time Minutes":str(rev["display_minutes"]),"Time from Seattle":duration(rev["display_minutes"]),"Drive Time Band":"3-4hrs" if rev["display_minutes"]<240 else "4plus","Drive time origin":"Seattle, Washington","Drive time source":f"https://www.google.com/maps/dir/?api=1&origin=Seattle%2C%20Washington&destination={lat:.7f},{lon:.7f}&travelmode=driving","Drive time checked":CHECKED,"Drive time note":rev["route_note"],"Topographic background image":f"https://westcoastrvcamping.com/assets/images/topo/{slug}.jpg"})
        if slug not in by_slug: rows.append(row)
        by_slug[slug]=row
    for slug,nearby in {"hoh-campground":"minnie-peterson-campground;hard-rain-cafe-campground;hoh-oxbow-campground;south-fork-hoh-campground","hard-rain-cafe-campground":"minnie-peterson-campground;hoh-campground;hoh-oxbow-campground;south-fork-hoh-campground","kalaloch-campground":"cottonwood-campground;south-beach-campground;coppermine-bottom-campground;bogachiel-state-park"}.items(): by_slug[slug]["Nearby campgrounds"]=nearby
    with MASTER.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n"); w.writeheader(); w.writerows(rows)

    coverage=json.loads(COVERAGE.read_text()); coverage["updated_on"]=CHECKED
    payload={"id":"jefferson-dnr","county":"Jefferson","operator_layer":"Washington DNR","status":"complete","inventory_sources":[DNR_STATUS,DNR,DNR_GUIDE],"candidates":[
      *[{"name":CAMPS[s]["Name"],"slug":s,"decision":"included_new","reason":"Current DNR inventory lists the campground open and the official recreation guide supports RV/trailer access up to 30 feet."} for s in CAMPS],
      {"name":"Upper Clearwater Campground","decision":"deferred","reason":"DNR lists the campground closed for all of 2026 and says RVs are allowed but not recommended; reconsider after a reopening and access review."},
      {"name":"Yahoo Lake Campground","decision":"excluded","reason":"DNR describes backcountry campsites reached by a one-mile hike, so it is outside the drive-in RV scope."}]}
    section=next((s for s in coverage["sections"] if s["id"]=="jefferson-dnr"),None)
    if section: section.update(payload)
    else: coverage["sections"].insert(2,payload)
    COVERAGE.write_text(json.dumps(coverage,indent=2)+"\n")

    evidence=json.loads(EVIDENCE.read_text()); slugs=set(CAMPS)
    evidence["observations"]=[o for o in evidence["observations"] if o.get("slug") not in slugs]
    sources=[source(DNR_STATUS,"Washington Department of Natural Resources","Current campsite inventory supports county and operating status."),source(DNR,"Washington Department of Natural Resources","Official regional page supports directions, facilities, first-come use, and current alerts."),source(DNR_GUIDE,"Washington Department of Natural Resources","Official recreation guide supports a 30-foot trailer maximum and primitive campground context.")]
    for slug in CAMPS:
      for field,value in {"operating_status":"Open in current DNR inventory","rv_access":True,"reservation_method":"First-come; Discover Pass required","max_rv_length":30,"hookups":0}.items():
        evidence["observations"].append({"slug":slug,"field":field,"status":"supported","checked_on":CHECKED,"summary":f"Current official DNR sources support {field.replace('_',' ')}: {value}.","proposed_value":value,"sources":sources})
    EVIDENCE.write_text(json.dumps(evidence,indent=2)+"\n")
    print(f"Completed Jefferson DNR review; dataset now contains {len(rows)} records.")

if __name__ == "__main__": main()
