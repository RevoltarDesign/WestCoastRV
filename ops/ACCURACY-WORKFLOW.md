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

- `python3 ops/content_scrub.py` catches known cross-region contamination, obsolete identities, stale closure wording, and unsupported universal amenity copy.
- `python3 ops/audit_recreation_gov.py` compares every Recreation.gov URL with the live facility name and rejects links to similarly named campgrounds, kitchens, picnic areas, or day-use facilities. It saves `ops/recreation-gov-audit.json` as a dated snapshot.
- `python3 ops/apply_recreation_coordinates.py` accepts a Recreation.gov facility point only when the facility identity matches, the point is inside Washington, and it is within two miles of the prior pin. Larger moves enter the manual review queue.
- `python3 ops/apply_manual_coordinate_resolutions.py` applies the reviewed exception queue in `coordinate-resolutions.json`. A resolution requires agreement among the facility identity, agency access directions, and a named navigation destination; it also stores the reason for moving or retaining the pin.
- `python3 ops/route_audit.py` requires every reviewed Seattle estimate to retain its origin, observed minutes, distance, dated Google Maps route, and a public estimate that is never shorter than the observed route.
- `python3 ops/check_external_links.py` checks all public external destinations.
- `python3 ops/trust_workflow.py summary` reports evidence coverage across every campground, including records with no evidence yet.
- `python3 -m unittest discover -s ops -p 'test_*.py'` protects corrected cases during later regeneration.

Run the offline checks on every content change. Run the live source and link checks before deployment and during scheduled data reviews. Recheck operating status and reservation details at least before each camping season; recheck all critical fields when an operator page changes.

## Current baseline — 2026-09-06

The whole 120-record dataset has completed the structural and contamination scrub. After the first section review, the evidence ledger fully supports all five critical fields for 13 campgrounds, partially supports 55, and has no accepted critical-field evidence for 52. That internal gap is a research queue, not a badge to place throughout the public experience.

The scrub found and fixed 20 campground-specific factual issues and six shared template issues. The template fixes corrected 627 affected page instances. Exact findings and sources are in `scrub-findings.json`.

The first section review completed all ten Olympic National Park records, added coordinate provenance to 33 campgrounds, and added reviewed Seattle routes to 11. Coordinates drive the map, topographic art, structured data, and the directions destination. Public “Get Directions” buttons now open turn-by-turn driving directions to the reviewed point. Olympic routes use a no-ferry option where one offers a more stable towing estimate; route notes preserve that decision.

The first coordinate exception queue resolved all 15 Recreation.gov discrepancies. Fourteen prior pins were materially wrong and Mora's source feed contained an invalid `0,0` point; all 15 now use reviewed named navigation destinations corroborated by agency records and access directions. The same pass reviewed Seattle routes for all 15, uses the agency-recommended Darrington approach for Bedal, and uses a no-ferry baseline for Mora.
