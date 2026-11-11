# Requirements Graph — Global Scope for Platform-Wide Rules (D53)

**Date:** 2026-11-11
**Type:** Major update — graph data change (Rule attribute `scope: global`; no Rule statement changed, no node created)
**Programme:** `plans/261108-1040-requirements-graph-programme/` (Hairline root)
**Decision:** D53 in `plans/reports/advise-261105-0843-graph-model-decisions.md`
**Report (full lists):** `plans/reports/fullstack-developer-261111-0740-global-scope-apply.md`

## Summary

Decision D53 (2026-11-10): Rules that are clearly platform-wide get `scope: global`; doubtful ones are listed for the user. The candidates were the Rules named by the step 1 completeness gate reports under "Needs user decision" (platform-wide or global scope items) and the held ops whose wait reason names platform-wide placement. Of 93 candidate Rules, 6 were set global, 77 are listed for a user ruling in 10 items, and 10 are not global because they already point at the object their statement is about.

## What changed

| Area | Change |
|---|---|
| `graph/changesets/2026-11-11-fr005-global-scope.yaml` | New, applied: `scope: global` on REQ-005-009 |
| `graph/changesets/2026-11-11-fr007-global-scope.yaml` | New, applied: `scope: global` on REQ-007-008 |
| `graph/changesets/2026-11-11-fr023-global-scope.yaml` | New, applied: `scope: global` on REQ-023-001, REQ-023-002, REQ-023-012, REQ-023-014 |
| `graph/changesets/2026-11-10-fr007-completeness-held.yaml` | The object-level alternative for REQ-007-008 (`applies to` ENT-payment) and its wait comment left the file, with a dated D53 note; every other line unchanged and in order |
| `graph/graph.db`, `graph/graph.json` | Applied and re-exported; backup `project-requirements/graph/backups/graph-20261111-074025.db` taken before the apply |

## Rules set global

- REQ-005-009: data encrypted at rest and in transit, RBAC for actions (PRD: "according to platform policies", "for all actors").
- REQ-007-008: no card numbers stored by the platform.
- REQ-023-001, REQ-023-002: 7-year retention for medical and financial records (FR-023: minimums apply platform-wide).
- REQ-023-012: backups every 6 hours with 30-day retention, per system PRD.
- REQ-023-014: what anonymization must achieve, wherever it happens.

The Rules keep their existing `applies at` edges.

## Held count

| | Ops |
|---|---|
| Held before (all 2026-11-10 completeness held files) | 637 |
| Released | 0 |
| Dropped (REQ-007-008 object-level alternative) | 1 |
| Still held | 636 |

## Checks

- Lint before and after: 4,516 (L10 4,235, L12 194, L18 87); no finding added or resolved. Every candidate already had an `applies at` edge, so L13 and L02 were not affected.
- Tests: 234 passed.
- Query: exactly the six Rules above carry `scope: global`; nothing else in nodes or edges changed.

## Open for the user

Ten items (77 Rules) in the report, each with options: FR-001 UI lines, REQ-005-060 (conflicts with FR-023 deletion rules), FR-007 payment rules, FR-011 aftercare security, FR-012 messaging lines, REQ-019-092, the FR-022 search group, FR-023 analytics and deletion rules, FR-029 payment configuration rules, the FR-030 notification group.
