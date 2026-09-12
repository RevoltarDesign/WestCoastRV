# Washington campground coverage plan

The tracked master dataset is `ops/data/campgrounds.csv`, and the reproducible page generator is in `ops/generator/`. Run `python3 ops/generator/generate.py`, then `python3 ops/generator/sync_directory.py`. Before publishing, run `python3 ops/trust_workflow.py check`, `python3 ops/generator/validate_csv.py --master`, and `python3 ops/check_external_links.py`.

## Scope

The inventory covers developed Washington campgrounds that accept an RV, trailer, camper van, or truck camper and provide a legal overnight campsite. Tent-only, hike-in, dispersed, group-only, and permanently closed facilities are recorded as exclusions so they are not repeatedly rediscovered.

## Repeatable county pass

1. Start with official operator inventories: Washington State Parks, NPS, USFS, county and city parks, port districts, PUDs, and tribal or private operators.
2. Record every candidate before researching individual facts. Give each one a stable name, operator, county, source URL, and decision state.
3. Resolve facility identity and RV eligibility first. A parent park and a bookable campground are separate records when their rules or reservations differ.
4. Research accepted candidates in this order: operating status, RV access, reservation method, maximum length, hookups, then supporting amenities and trip context.
5. Store field-level evidence with retrieval date and source family. Official operator evidence can support an operational fact by itself when it is explicit and current; independent visitor sources are used for experiential claims such as cell service or maneuverability.
6. Publish only after deterministic checks confirm data, detail page, directory, map, sitemap, imagery, and evidence all agree.
7. Mark a coverage section complete only when every candidate from the section's official inventories has an include, exclude, or defer decision and exclusions have a reason.

## Rollout

Work county by county, finishing one operator layer at a time: state parks, federal facilities, county/city/port facilities, then private and tribal operators. Tier 1 counties remain the first priority. Within a county, favor facilities that add a new trip choice: different hookup level, trailer fit, landscape, season, or reservation style.

## Pilot: Jefferson County

- **State parks: complete for this pass.** Fort Worden was already present. Dosewallips and Fort Flagler were accepted and added on 2026-09-06. Non-camping state park units are exclusions when inventoried.
- **Federal: complete for this pass.** Hoh, Kalaloch, South Beach, and Seal Rock were already present; Falls View was added on 2026-09-09. Seal Rock's published rig limit was corrected to 21 feet and its exact entrance and current closure were recorded. Collins remains deferred because two federal surfaces conflict on current operating status. Queets, Elkhorn, Rainbow, Interrorem Cabin, and Mount Walker were documented as exclusions.
- **Washington DNR: complete for this pass.** Coppermine Bottom, Cottonwood, Hoh Oxbow, Minnie Peterson, and South Fork Hoh were verified and published on 2026-09-10 with exact DNR-linked map points, conservative no-ferry routes, and primitive-access notes. Upper Clearwater remains deferred while closed for 2026; hike-in Yahoo Lake is excluded from RV coverage.
- **County/city/port: complete for this pass.** Quilcene, Lake Leland, Upper Oak Bay, Lower Oak Bay, Point Hudson, and Jefferson County Fairgrounds were verified and published on 2026-09-09. Current operator pages, facility maps, exact named map points, and stable no-ferry Seattle routes support the records. Conflicting Oak Bay site totals remain visible in the listing notes rather than being presented as certain.
- **Private/tribal: complete for this pass.** Cove RV Park, Hard Rain Cafe & Campground, and Port Ludlow RV Park were added on 2026-09-09. Halfway, Smitty's, and a proposed Hoh tribal visitor campground were researched and excluded with documented reasons.

## Clallam County

- **Washington DNR: complete for this pass.** Bear Creek, Lyre River, and Sadie Creek were verified and published on 2026-09-11 with exact DNR-linked coordinates, no-ferry Seattle routes, RV limits, current status, and primitive-access notes.
- **Federal: complete for this pass.** Fairholme, Heart O' the Hills, Mora, Ozette, and Sol Duc were rechecked. Log Cabin Resort RV & Campground was added with the current 31-site RV inventory. Deer Park is excluded because NPS lists tents only and says the road is unsuitable for RVs and trailers.
- **County: complete for this pass.** Dungeness and Salt Creek were rechecked against current county campground and facility pages. The review corrected restroom and dump-station facts and added explicit RV access notes.
- **State parks: complete for this pass.** Bogachiel and Sequim Bay were rechecked. Bogachiel now uses the current official locate point; Sequim Bay now lists its 60 RV-capable standard and full-hookup campsites and the Lower Loop construction closure.
- **Private/tribal: complete for this pass.** Quileute Oceanside, Hobuck Beach, Cape Resort, Mason's Resort, Anglers Hideaway, and 3 Rivers Resort were verified and added on 2026-09-11. Four existing private records were rechecked and corrected. Hide-Away, The Village RV, Lost Resort, Van Riper's, and Riverview remain documented as deferred until stable operator and reservation facts are available; Cycle Camp and group-only Camp David Jr. are excluded from RV trip-planning scope.

## Snohomish County

- **County-operated campgrounds: complete for this pass.** Flowing Lake, Kayak Point, and Wenberg were rechecked on 2026-09-12. River Meadows, Squire Creek, Whitehorse, and the general-public Evergreen Fairgrounds RV-2 area were verified and added. Lake Roesiger Group Camp and event-only RV-1 are documented exclusions. The pass corrected 14 unique factual issues in the three existing records, added exact named destinations and towing-buffered Seattle routes for all seven, and published a source-backed county comparison guide.

## Completion evidence

The machine-readable inventory is `coverage-inventory.json`. `trust_workflow.py check` rejects duplicate candidates, missing decisions, malformed sources, unsupported published critical facts, and sections marked complete while candidates remain undecided.
