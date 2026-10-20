# Phase 4 Manual Test Guide — Scale and Optimization

## Document Control

| Field | Value |
|---|---|
| Phase | Phase 4 — Scale and Optimization |
| Plan version | v2 |
| Guide version | 1.0 |
| Status | Draft — skeleton |
| Product plan | [Admin and provider implementation status and release roadmap › Recommended four-phase release roadmap, Phase 4 row](../../../../../product-plans/v2/plan.md) |
| Created | 2026-10-19 |
| Last updated | 2026-10-20 |
| Guide owner | Product / QA lead, Vân Tay Media |
| Tester(s) | |

## Change Log

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-10-19 | Initial skeleton plan: scope, criteria, and planned batches; cases not written yet | Product / QA lead |
| 1.0 | 2026-10-19 | Before first issue: A-02 leftovers (featured providers, provider closure requests, "Login as Provider") moved into scope as planned batch B06 | Product / QA lead |
| 1.0 | 2026-10-19 | Before first issue: scope narrowed to the roadmap Phase 4 row; RBAC (Phase 1 B04) and support case handling (Phase 2 B08) removed; A-01 and A-02 leftovers listed as out of scope; uniform exit criteria; provider dashboard URL set | Product / QA lead |
| 1.0 | 2026-10-20 | Moved to the plan-versioned layout (`testing/manual/v2/phases/`): renamed from plan.md to test-guide.md; Document Control links to the product plan (objective and exit gate live there); progress moved to per-run summaries in `results/`; batch Control rows now Plan / phase and Batch version. No case changed | Product / QA lead |

## 1. Test Scope

Phase scope, release objective, and exit gate are owned by the product plan (Document Control › Product plan). This section maps that scope to test batches.

### 1.1 In Scope

| Module | Function slice in this phase | FRs | Batch |
|---|---|---|---|
| PR-05 | Advanced provider analytics and exports (performance, patient, pricing and benchmark analytics; export report configuration; earnings and payout history exports) | FR-014, FR-017 | B01 |
| PR-06 | Remaining provider settings and help, not covered by Phase 1 B03 (profile, pricing, package catalog) or Phase 3 B06 (billing settings): account settings and password change, notification preferences, Help Centre (FAQs, guides, resources, videos, contact support, feedback, own support cases), dashboard language switch, review list and public responses | FR-032 Screens 2, 3 and 5, FR-033 (consumed content), FR-034 (provider-raised cases), FR-021, FR-013 | B02 |
| A-08 | Platform analytics (platform overview, provider performance, acquisition funnel, geographic, outcomes, financial health, pricing intelligence) | FR-014 | B03 |
| A-09 | Remaining configuration and compliance, not covered by Phase 1 B04 (admin access control, throttling, inquiry and quote configuration, questionnaires): localization publish and rollback, data retention and its observability, legal content, regional configuration and pricing, payment system configuration, notification rules, Help Centre content management, admin treatment catalog, remaining app settings | FR-021, FR-023, FR-027, FR-028, FR-029, FR-030, FR-033, FR-024 Screens 1 and 2, remaining FR-026 screens | B04 |
| A-10 | Advanced monitoring and support analytics only: support case reporting and metrics, Support Center Configuration, and messaging monitoring beyond the Phase 2 B08 slice. Case creation, assignment, replies, resolution and reopen stay in Phase 2 B08 | FR-034 Screen 7 and Admin Management Metrics, FR-012 | B05 |
| A-02 | Provider management leftovers not covered by Phase 1 B01: featured provider management and the 10-provider cap, provider closure requests, "Login as Provider" with its audit trail | FR-015, FR-009 | B06 |

### 1.2 Out of Scope

- Functions already released and tested in Phases 1 to 3, except where Phase 4 adds analytics, exports, or configuration on top of them.
- FR-036 (listed under A-09 in the roadmap but not yet defined; deferred until a PRD exists).
- Admin access control and roles (FR-031): tested in Phase 1 B04; Phase 4 cases only use the existing roles.
- Admin support case handling (FR-034 Screens 1 to 6): tested in Phase 2 B08.
- A-01 leftovers (admin patient list and detail, admin review moderation under FR-013, FR-037 and FR-038 monitoring oversight). The roadmap Phase 4 row does not name A-01, and the roadmap action register leaves FR-037 and FR-038 open, so these stay post-MVP until the roadmap assigns them a phase. The A-02 leftovers are in scope as B06 (decision of 2026-10-19).
- The patient mobile app and the affiliate portal.

## 2. Entry and Exit Criteria

**Entry criteria** (all must hold before testing starts):

- Phase 3 exit gate passed.
- A phase handoff note written from the actual Phase 3 end state of the shared test environment (account states, bookings, payouts, promotions, affiliates), and the Phase 4 data sets checked against it. Data persists between phases; nothing is reset.
- Build deployed to the test environment; version recorded below.
- Test accounts available and verified.
- Batch files written and reviewed (this plan is a skeleton).

**Exit criteria** (phase passes when):

- Every High-priority case is Pass.
- No open bug (Bug status Found, Logged, Fixed - retest, or Reopened) on a High-priority case.
- All analytics use live traceable data.
- Exports, drill-downs, and audit work.
- Localization publish and rollback pass.
- Retention observability passes.

## 3. Test Environment and Accounts

| Item | Value |
|---|---|
| Provider dashboard URL | https://admin.hairline.app (shared origin with the admin dashboard; sign in with a provider account) |
| Admin dashboard URL | https://admin.hairline.app |
| Backend API base URL | https://backend.hairline.app/api |
| Build / release under test | |
| Browser(s) | Chrome latest, desktop |

Accounts used (placeholders; credentials sent privately):

| Placeholder | Role | Used in batches |
|---|---|---|
| `{A1}` | Super admin | B03, B04, B05, B06 |
| `{S1}` | `{V1}` staff, system role Clinical Staff | B01, B02 |
| `{V1}` to `{V4}` | Provider owners | B01, B02, B03, B06 |
| `{P1}` to `{P7}` | Patients owning prepared data (setup data only) | B01, B03, B05 |

## 4. Batches and Run Order

| Order | Batch | File | Module | FRs | Cases | Depends on |
|---|---|---|---|---|---|---|
| — | B01 | B01-pr05-advanced-analytics-exports.md (planned) | PR-05 | FR-014, FR-017 | Not written | — |
| — | B02 | B02-pr06-remaining-settings-help.md (planned) | PR-06 | FR-032, FR-033, FR-034, FR-021, FR-013 | Not written | — |
| — | B03 | B03-a08-analytics.md (planned) | A-08 | FR-014 | Not written | — |
| — | B04 | B04-a09-remaining-configuration-compliance.md (planned) | A-09 | FR-021, FR-023, FR-024, FR-026 to FR-030, FR-033 | Not written | — |
| — | B05 | B05-a10-monitoring-support-analytics.md (planned) | A-10 | FR-012, FR-034 | Not written | — |
| — | B06 | B06-a02-provider-management-leftovers.md (planned) | A-02 | FR-015, FR-009 | Not written | — |

**End-to-end journey:** To be written with the batch files. Planned shape: providers and admins use live analytics to make decisions and export traceable reports; admins localize and publish configuration and can roll it back; support and monitoring analytics report on the live cases and conversations created in earlier phases, with their audit trail.

## 5. Test Runs and Progress

Progress is recorded per test run, not in this guide. Each run is a folder `results/run-NN-YYYY-MM-DD/` with one result copy per batch and a `summary.md` holding that run's Progress Summary. The `manual-test-bug-sync` skill creates the run (`new-run`), merges returned results, and refreshes the summary. Never fill in the scaffolds in `batches/`. Rules: TEST-STRATEGY §2 and §7.
