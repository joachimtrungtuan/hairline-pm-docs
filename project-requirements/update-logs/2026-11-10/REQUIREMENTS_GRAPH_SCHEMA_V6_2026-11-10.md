# Requirements Graph — Schema v6 Flow Model, PO Decision Sources and CR Check

**Date:** 2026-11-10
**Type:** Major update — graph schema migration (version 5 to 6) and data additions
**Programme:** `plans/261108-1040-requirements-graph-programme/` (Hairline root), Phases 3 and 4
**Decisions:** D42 in `plans/reports/advise-261105-0843-graph-model-decisions.md` (Hairline root)

## Summary

The graph can now hold the order of steps in a flow, not only the rules. Schema version 6 adds Step and Flow nodes and six edge verbs, with lint checks L14 to L19. The MTG-002 Product Owner decision log is loaded as 100 Source nodes so rules can cite the exact decision. The quote author field was renamed. A new script checks that every approved Change Request is cited in its PRD change log. No PRD was edited.

## What changed

| Area | Change |
|---|---|
| `graph/schema.yaml` | Version 6. Node types `Step` (`STP-NNN-NNN`, FR-owned) and `Flow` (`FLW-...`, no owner, `kind` main, alternative or journey). Verbs `done by`, `at`, `on`, `applies`, `next` (attrs `condition`, `label`, `back`), `starts at`. An Event may be emitted at several Stages (D7 superseded) |
| `graph/graph.db` | Migrated by `scripts/migrate_schema_v6.py` (backup `backups/graph-20261110-002035.db`); every table copied row for row, lint unchanged. Then two change-sets applied (backup `backups/graph-20261110-002543.db`) |
| `graph/changesets/2026-11-10-fr004-quote-authored-by-type.yaml` | Retires `ENT-quote.author_type`; adds `ENT-quote.authored_by_type` with enum values provider and admin |
| `graph/changesets/2026-11-10-po-001-decision-sources.yaml` | Adds `SRC-PO-001` (decision log) and 100 decision items `SRC-PO-001-<code>`: D1 to D24 plus D6-M, R7-1 to R7-4, M1 to M18, P1 to P3, Q1 to Q50. Q26 and Q27 are pending review (deferred to the payment pass), Q33 is superseded by Q38, the rest are incorporated |
| `graph/scripts/lint.py` | L04 fires only when an Event has no producer Stage. New L14 (Step not reachable from a Flow), L15 (backward `next` without `back`), L16 (Actor not acting at the Step's Stage), L17 (missing `done by` or not exactly one `at`), L18 (open cross-FR hand-off), L19 (`next` condition not an active Rule) |
| `graph/scripts/check_crs.py` (new) | Checks each Approved CR ID appears in its PRD's Appendix: Change Log; Proposed CRs listed, not checked |
| `graph/scripts/` tests | New flow-lint, v6 migration and CR-check tests; 182 tests pass |
| `graph/viewer/index.html` | Step and Flow types shown |
| `graph/checklists/` | `migrate-fr.md` and `completeness-check.md` to 1.3 (flow steps, hand-offs, several `emits`, `SRC-PO-001` citations, review step 1 fix change-set); README to 1.5 |
| `graph/README.md` | Schema version 6 section; `check_crs.py` and `migrate_schema_v6.py` listed; lint range L01 to L19; version 5 section reworded as applied |
| `graph/graph.json` | Re-exported: 8306 nodes, 2866 fields, 1087 enum values, 13046 edges, 184 sources, 62 change-sets |

## Results

- Lint: 4,322 findings (L10 4,144, L12 178), the same as before the migration. No Steps exist yet, so L14 to L19 report nothing until the completeness checks add them.
- CR check: 74 Approved CRs, 20 not cited by ID. 19 have a change-log row on the CR's decision date that omits the ID; CR-FR037-20260820-01 has no row on its decision date. Listed for the user; PRD change logs are not edited during the freeze.
- `ENT-quote.authored_by_admin_id` is not in the graph; to be raised by the FR-004 completeness check.

## Next

The 34 remaining completeness checks run as D37 review step 1 under checklist 1.3, building each FR's Steps and Flows.

## Addendum: schema v7, system Actor (same day, D44)

The user chose one system actor (option A in D44). Steps the platform performs by itself had no Actor and sat in the held change-sets; they can now be `done by` `ACT-system`. This change only prepares the ground.

| Item | Change |
|---|---|
| `graph/schema.yaml` | Version 7; `system` added to the `actor_group` enum (the platform itself, acting for automatic steps) |
| `graph/scripts/migrate_schema_v7.py` | New. `actor_group` is stored only in Actor attrs, so no table changes: it checks the DDL equals the version 7 DDL, backs up, and sets `user_version` 7 |
| `graph/scripts/test_dedup.py` | Five migration tests added (224 tests pass, was 219); the v5 and v6 migration tests now derive their old schemas from a v6 schema |
| `graph/README.md` | "Schema version 7" section and script entry |
| `graph/changesets/2026-11-10-system-actor.yaml` | Adds node `ACT-system` (Actor, group `system`); no `acts in` edges, they are added per FR later |
| `graph/graph.db`, `graph/graph.json` | Migrated and re-exported (9143 nodes); backup `graph/backups/graph-20261110-121140.db` (git-ignored) |

Lint is unchanged at 4,365 findings (L10 4,151, L12 180, L18 34), checked on a copy of the DB first and again on the real one. No Rule was changed. No script or viewer code assumed three groups.

Still open with the user: whether external services (payment gateway, email and SMS providers) count as the system. Steps attributed to an external service stay held. The held change-sets were not touched.

