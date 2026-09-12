# Accuracy workflow

The public directory is generated from `ops/data/campgrounds.csv`. Research notes or AI output never publish directly. A record moves into the site only after a reviewer updates the canonical row and adds field-level evidence to `verification-evidence.json`.

## Source order

1. Current operator or land-manager page, campground map, alert, or reservation inventory
2. Current government recreation dataset, including Recreation.gov
3. Local tourism or chamber source when the operator has no usable page
4. Aggregators only for discovery; they do not establish a publishable fact

When authoritative sources disagree, preserve the conflict in the evidence ledger and publish the narrower claim or “not confirmed.” Site-specific RV limits take precedence over a broad campground maximum, and the page must say when only a few sites accept the maximum length.

## Required evidence

Before a new campground is publishable, verify:

- operating status and seasonal closure information
- whether RVs or trailers are actually allowed
- correct reservation destination and method
- hookup level
- maximum equipment length, or an explicit “not published” result

Counts, showers, potable water, dump access, generator rules, and accessibility should also be sourced before they are stated as definite. Marketing superlatives and wildlife, ecology, geology, distance, and “every site” claims require direct support or should be rewritten as plain location context.

## Checks

Run `python3 ops/coordinate_sanity.py` before publishing. It checks Washington bounds, consistency between coordinate fields and map links, reviewed-pin drift, and suspiciously close duplicates. Missing coordinate provenance remains a visible warning queue so the source-backed review can expand section by section.

- `python3 ops/content_scrub.py` catches known cross-region contamination, obsolete identities, stale closure wording, and unsupported universal amenity copy.
- `python3 ops/audit_recreation_gov.py` compares every Recreation.gov URL with the live facility name and rejects links to similarly named campgrounds, kitchens, picnic areas, or day-use facilities. It saves `ops/recreation-gov-audit.json` as a dated snapshot.
- `python3 ops/apply_recreation_coordinates.py` accepts a Recreation.gov facility point only when the facility identity matches, the point is inside Washington, and it is within two miles of the prior pin. Larger moves enter the manual review queue.
- `python3 ops/apply_manual_coordinate_resolutions.py` applies the reviewed exception queue in `coordinate-resolutions.json`. A resolution requires agreement among the facility identity, agency access directions, and a named navigation destination; it also stores the reason for moving or retaining the pin.
- Regional `*-location-reviews.json` ledgers preserve every manually matched destination, address, route observation, and precision decision. `coordinate_sanity.py` discovers these ledgers automatically so each completed batch becomes a permanent regression check.
- `python3 ops/route_audit.py` requires every reviewed Seattle estimate to retain its origin, observed minutes, distance, dated Google Maps route, and a public estimate that is never shorter than the observed route.
- `python3 ops/check_external_links.py` checks all public external destinations.
- `python3 ops/trust_workflow.py summary` reports evidence coverage across every campground, including records with no evidence yet.
- `python3 -m unittest discover -s ops -p 'test_*.py'` protects corrected cases during later regeneration.

Run the offline checks on every content change. Run the live source and link checks before deployment and during scheduled data reviews. Recheck operating status and reservation details at least before each camping season; recheck all critical fields when an operator page changes.

## Current baseline — 2026-09-07

The whole 120-record dataset has completed the structural and contamination scrub. After the Olympic Peninsula, North Sound, Hood Canal, and southwest state-park reviews, the evidence ledger fully supports all five critical fields for 37 campgrounds, partially supports 31, and has no accepted critical-field evidence for 52. That internal gap is a research queue, not a badge to place throughout the public experience.

The scrub has found and fixed 73 campground-specific factual issues and seven shared template issues. The template fixes corrected 747 affected page instances. Exact findings and sources are in `scrub-findings.json` and the regional review ledgers.

The first section review completed all ten Olympic National Park records, added coordinate provenance to 33 campgrounds, and added reviewed Seattle routes to 11. Coordinates drive the map, topographic art, structured data, and the directions destination. Public “Get Directions” buttons now open turn-by-turn driving directions to the reviewed point. Olympic routes use a no-ferry option where one offers a more stable towing estimate; route notes preserve that decision.

The first coordinate exception queue resolved all 15 Recreation.gov discrepancies. Fourteen prior pins were materially wrong and Mora's source feed contained an invalid `0,0` point; all 15 now use reviewed named navigation destinations corroborated by agency records and access directions. The same pass reviewed Seattle routes for all 15, uses the agency-recommended Darrington approach for Bedal, and uses a no-ferry baseline for Mora.

The North Sound review resolved six additional locations and Seattle routes: Deception Pass, Larrabee, Birch Bay, Camano Island, Fort Ebey, and Fort Casey. Campground-specific destinations are used at Deception Pass and Fort Ebey, while the other four use the official park address where it converges with the campground entrance. The batch also corrected eight grouped facts, including hookup types, campsite totals, addresses, an unsupported dump station, and Fort Casey's September 15, 2026 through June 15, 2027 campground closure.

The Clallam public-land review added Bear Creek, Lyre River, Sadie Creek, and Log Cabin Resort, bringing the directory to 139 records. It corrected five grouped issues in existing records: Fairholme's RV-capable drive-in count, Sequim Bay's campground inventory, Dungeness facilities, Salt Creek facilities, and Bogachiel's official map point. The evidence baseline is now 84 fully supported, 13 partially supported, and 42 unresearched records. Coordinates have source provenance for 118 records and Seattle routes for 101.

The Clallam private and tribal review added six current transient RV choices: Quileute Oceanside Resort, Hobuck Beach Resort, Cape Resort, Mason's Resort, Anglers Hideaway, and 3 Rivers Resort. It found and fixed nine grouped factual issues across Elwha, Forks RV Park, Crescent Beach, and Gilgal Oasis, including conflicting or unsupported site totals, unsupported maximum lengths, an obsolete seasonal claim, an inaccurate shopping-distance claim, and Elwha's operator-published GPS point. The directory now contains 145 records: 86 fully supported, 21 partially supported, and 38 unresearched. Coordinate provenance covers 124 records and reviewed Seattle routes cover 107. Five lower-confidence private candidates remain explicitly deferred rather than published with guessed details.

The Hood Canal and northeast Olympic Peninsula review resolved six more locations and Seattle routes: Sequim Bay, Fort Worden, Potlatch, Twanoh, Belfair, and Jarrell Cove. Stable no-ferry towing routes are used for Sequim Bay and Fort Worden. This batch corrected 12 grouped facts, including Twanoh's 2026 campground operating status, Sequim Bay's Lower Loop closure and 40-foot RV limit, Jarrell Cove's campsite inventory and lack of an RV dump station, Fort Worden's 80-site campground total, Potlatch's address and inventory, and unsupported park-wide capacity claims at Belfair.

The southwest Washington State Parks review completed 12 more locations and Seattle routes: Penrose Point, Illahee, Saltwater, Dash Point, Schafer, Rainbow Falls, Lewis and Clark, Seaquest, Battle Ground Lake, Beacon Rock, Millersylvania, and Ike Kinswa. It corrected 33 grouped campground facts. High-impact fixes include Saltwater's currently closed campground and removal of residual campsite recommendations, Ike Kinswa's location on Mayfield Lake rather than Riffe Lake, current addresses, current seasonal closures, facility availability, and stale campground totals at seven parks. Dash Point and Beacon Rock now use named campground destinations instead of broad park points, while Illahee uses a stable no-ferry towing route. The current dataset has 78 sourced coordinates and 56 sourced Seattle routes; 42 coordinate reviews and 64 route reviews remain.
