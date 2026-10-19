# Phase 4 Manual Test Plan — Scale and Optimization

## Document Control

| Field | Value |
|---|---|
| Phase | Phase 4 — Scale and Optimization |
| Plan version | 1.0 |
| Status | Draft — skeleton |
| Scope source | [Admin and provider implementation status and release roadmap › Recommended four-phase release roadmap, Phase 4 row](../../../../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md) |
| Release objective | Add decision intelligence, localization depth, and advanced self-service |
| Exit gate | All analytics use live traceable data; exports, drill-downs, and audit work; localization publish and rollback and retention observability pass |
| Created | 2026-10-19 |
| Last updated | 2026-10-19 |
| Plan owner | Product / QA lead, Vân Tay Media |
| Tester(s) | |

## Change Log

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-10-19 | Initial skeleton plan: scope, criteria, and planned batches; cases not written yet | Product / QA lead |

## 1. Scope

### 1.1 In Scope

| Module | Function slice in this phase | FRs | Batch |
|---|---|---|---|
| PR-05 | Advanced provider analytics and exports (performance, patient, pricing and benchmark analytics; export report configuration; earnings and payout history exports) | FR-014, FR-017 | B01 |
| PR-06 | Remaining provider settings and help | FR-013, FR-021, FR-024, FR-032, FR-033 | B02 |
| A-08 | Platform analytics (platform overview, provider performance, acquisition funnel, geographic, outcomes, financial health, pricing intelligence) | FR-014 | B03 |
| A-09 | Remaining configuration and compliance (localization, RBAC, notification history, retention observability, regional pricing, package authorization) | FR-021, FR-023 to FR-031 | B04 |
| A-10 | Advanced monitoring and support analytics (support case management, assignment, replies, escalation, categories, priorities, audit) | FR-012, FR-034 | B05 |

### 1.2 Out of Scope

- Functions already released and tested in Phases 1 to 3, except where Phase 4 adds analytics, exports, or configuration on top of them.
- FR-036 (listed under A-09 in the roadmap but not yet defined; deferred until a PRD exists).
- The patient mobile app and the affiliate portal.

## 2. Entry and Exit Criteria

**Entry criteria** (all must hold before testing starts):

- Phase 3 exit gate passed.
- Build deployed to the test environment; version recorded below.
- Test accounts available and verified.
- Batch files written and reviewed (this plan is a skeleton).

**Exit criteria** (phase passes when):

- Every High-priority case is Pass.
- No open bug with Bug status Found, Logged, or Reopened at High priority.
- All provider and admin analytics use live, traceable data; no fixture or hard-coded figures remain.
- Exports, drill-downs, and their audit entries work.
- Localization publish and rollback work.
- Retention observability passes.

## 3. Test Environment and Accounts

| Item | Value |
|---|---|
| Provider dashboard URL | {Provider dashboard URL} |
| Admin dashboard URL | https://admin.hairline.app |
| Backend API base URL | https://backend.hairline.app/api |
| Build / release under test | |
| Browser(s) | Chrome latest, desktop |

Accounts used (placeholders; credentials sent privately):

| Placeholder | Role | Used in batches |
|---|---|---|
| `{A1}` | Super admin | B03, B04, B05 |
| `{S1}` | Provider staff (clinician / front desk) | B01, B02 |
| `{V1}` to `{V4}` | Provider owners | B01, B02, B03 |
| `{P1}` to `{P7}` | Patients owning prepared data (setup data only) | B01, B03, B05 |

## 4. Batches and Run Order

| Order | Batch | File | Module | FRs | Cases | Depends on |
|---|---|---|---|---|---|---|
| — | B01 | B01-pr05-advanced-analytics-exports.md (planned) | PR-05 | FR-014, FR-017 | Not written | — |
| — | B02 | B02-pr06-remaining-settings-help.md (planned) | PR-06 | FR-013, FR-021, FR-024, FR-032, FR-033 | Not written | — |
| — | B03 | B03-a08-analytics.md (planned) | A-08 | FR-014 | Not written | — |
| — | B04 | B04-a09-remaining-configuration-compliance.md (planned) | A-09 | FR-021, FR-023 to FR-031 | Not written | — |
| — | B05 | B05-a10-advanced-monitoring-support-analytics.md (planned) | A-10 | FR-012, FR-034 | Not written | — |

**End-to-end journey:** To be written with the batch files. Planned shape: providers and admins use live analytics to make decisions and export traceable reports; admins localize and publish configuration and can roll it back; support and monitoring analytics show live cases and their audit trail.

## 5. Progress Summary

Update after each test session (the `manual-test-bug-sync` skill can refresh this).

| Batch | Total | Pass | Fail | Blocked | Not tested | Open bugs | Last tested |
|---|---|---|---|---|---|---|---|
| B01 | — | — | — | — | — | — | — |
| B02 | — | — | — | — | — | — | — |
| B03 | — | — | — | — | — | — | — |
| B04 | — | — | — | — | — | — | — |
| B05 | — | — | — | — | — | — | — |
| **Total** | — | — | — | — | — | — | — |
