# Change Request: Analytics Configuration Ownership

**Change Request ID**: CR-FR026-20261013-01
**Primary FR**: FR-026
**Triggering FR / Event**: FR-014 v3.7 verification (verify-fr), critical Issue 4: admin-configurable analytics settings had no owning FR, screen, or defaults
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-13
**Decision Date**: 2026-10-13
**PRD Version Change**: v1.8 to v1.9; follow-up v1.10 (same day)
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-026/A-09 owns one versioned Analytics Configuration consumed by FR-014: TTFQ SLA target, At Risk and Dormant thresholds, price outlier threshold, benchmark refresh frequency, and an optional target monthly commission. FR-014 applies the active version at calculation time and records that version with its aggregates. Exports that were already generated are not rewritten. See Recalculation Rule below.

## Baseline State

**Source version**: FR-026 v1.8; FR-014 v3.7 Admin Editability Rules, Assumption 4, and the FR-026 dependency line

FR-014 listed these values as admin-editable and named FR-026 as the "admin settings store", but FR-026 had no screen, workflow, requirement, entity, or seed data for them. Only the outlier threshold (30%) had a documented default.

## Approved State

**Target version**: [FR-026 v1.10](./prd.md), Module Scope, Entry Points, Workflow A8, Screen 1 Analytics section and App Data list (Quote Configuration added in v1.10), Screen 5e, Admin Editability Rules, Dependencies, Seeding, User Story 9, REQ-026-012g, REQ-026-028, REQ-026-029, and Entity 12

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| TTFQ SLA target | Admin-editable in FR-014; no owner or default | FR-026 Screen 5e; positive whole minutes; default 120 | Product Owner chose 120 minutes |
| Engagement thresholds | Admin-editable in FR-014; no owner | At Risk default 7 days, Dormant default 30 days; Dormant must exceed At Risk | Match current FR-014 day boundaries |
| Price outlier threshold | FR-014 default 30%; no owner | Whole percent 1-100; default 30 | Keep FR-014 default |
| Benchmark refresh frequency | Admin-editable in FR-014; no options or default | Daily, Weekly, or Monthly; default Weekly | Give FR-014 a bounded cadence |
| Target monthly commission | Reference line always implied | Optional; blank by default; FR-014 hides the line until a value is set | Product Owner chose "hidden until set" |
| Change effect | Undefined | See Recalculation Rule: live views recalculate all displayed periods with the active version; generated exports are never rewritten; aggregates record the configuration version | Keep analytics auditable and simple |
| Screen 1 setting groups (v1.10) | App Data list omitted Quote Configuration although Screen 5d and REQ-026-012f define it | App Data lists Quote Configuration (active ISO 4217 currency, default expiry hours) | Consistency fix found during FR-014 verification |

## Recalculation Rule

In plain terms: settings change how numbers are coloured and grouped, not the raw data. When an admin saves a new Analytics Configuration version:

1. **Live dashboards and benchmarks** use the new version from their next calculation or benchmark refresh. This applies to every period shown on screen, including past months. Example: if the SLA target moves from 120 to 60 minutes, last month's TTFQ chart is recoloured against 60 minutes after the next calculation. Past periods are not frozen at older values.
2. **Version stamp**: every aggregate records which configuration version produced it, so any number can be traced to the settings used.
3. **Exports**: PDF/CSV exports and scheduled-export files already generated are never rewritten. They keep the values and version from the moment they were generated. Recurring exports generated after the change use the new version.
4. **Raw counts do not change**: inquiries, quotes, bookings, payments, and TTFQ minutes are the same under any version; only tiers, colours, engagement buckets, outlier flags, and the commission reference line can change.

The Product Owner confirmed this rule on 2026-10-13 and chose not to freeze past periods at the version active at the time.

## Scope and Impact

### In Scope

- FR-026 analytics-configuration UI, versioning, API, dependency, seeding, story, requirement, and entity contracts.
- Matching FR-014 v3.8 references (Admin Editability Rules defaults, Assumption 4, FR-026 dependency, Screen 12 Widget 2 reference line).

### Out of Scope

- Per-provider SLA overrides (remain out of scope per FR-014 Assumption 4).
- The FR-014 definition of what counts as provider activity for engagement status; FR-026 owns only the day boundaries.
- Implementation changes, schema migrations, and commits.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Workflow A8, Screen 5e, Dependencies, Seeding, User Story 9, REQ-026-012g, REQ-026-028, REQ-026-029, Entity 12
- **Related FRs**: [FR-014](../fr014-provider-analytics-reporting/prd.md) consumes the configuration (Screens 1, 2, 7, 8, 12, 13)
- **System documents**: [System data schema](../../system-data-schema.md) entity 36 `analytics_configurations` (added 2026-10-13); system PRD FR-014 section synced

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Settings UI/API/storage, cache invalidation, analytics reads of one consistent version, version recording on aggregates, permissions, and regression tests.
- **Compatibility / rollout risk**: Analytics must use the last valid cached configuration if the Settings API is unavailable. Changing thresholds alters colour bands and engagement counts from the next calculation, so trend charts may show a step change.
- **Data migration**: Seed one active configuration version with the defaults above.

## Acceptance and Validation

- Admin can version and audit all six values with a reason; invalid values (including Dormant not greater than At Risk) block the save.
- After an SLA change, the next calculation recolours past periods shown on live dashboards using the new value, and each aggregate shows the new configuration version.
- Screen 1 App Data lists Quote Configuration.
- FR-014 reads all values from one configuration version and records that version with its aggregates.
- With no commission target set, Screen 12 Widget 2 shows no reference line; once set, the line appears.
- Exports and scheduled-export files generated before a change are not rewritten.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-13 (verify-fr FR-014 Issue 4, option to add the settings to FR-026 through a change request; SLA default 120 minutes; commission target hidden until set); follow-up 2026-10-13: Screen 1 Quote Configuration fix and explicit recalculation rule requested by the Product Owner
- **Decision evidence**: FR-014 verification report, 2026-10-13
- **PRD change log**: FR-026 v1.9 and v1.10; FR-014 v3.8 and v3.9
- **Update log**: [`FR014_VERIFICATION_FIXES_2026-10-13.md`](../../update-logs/2026-10-13/FR014_VERIFICATION_FIXES_2026-10-13.md)
- **Supersedes**: None
- **Superseded by**: None
