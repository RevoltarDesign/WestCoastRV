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
- **County/city/port: complete for this pass.** Quilcene, Lake Leland, Upper Oak Bay, Lower Oak Bay, Point Hudson, and Jefferson County Fairgrounds were verified and published on 2026-09-09. Current operator pages, facility maps, exact named map points, and stable no-ferry Seattle routes support the records. Conflicting Oak Bay site totals remain visible in the listing notes rather than being presented as certain.
- **Private/tribal: complete for this pass.** Cove RV Park, Hard Rain Cafe & Campground, and Port Ludlow RV Park were added on 2026-09-09. Halfway, Smitty's, and a proposed Hoh tribal visitor campground were researched and excluded with documented reasons.

## Completion evidence

The machine-readable inventory is `coverage-inventory.json`. `trust_workflow.py check` rejects duplicate candidates, missing decisions, malformed sources, unsupported published critical facts, and sections marked complete while candidates remain undecided.
