# Phase 4 Readiness & Fix Backlog — Scale and Optimization

> **Preparation status, 2026-09-29:** No Phase 4 product review or retest was performed for this file. Every case below is `Not tested`. The September roadmap owns release scope; old Sprint reports are historical evidence, not a new readiness verdict.

## Document Control & Phase Summary

| Field | Value |
|---|---|
| Phase | Phase 4 — Scale and optimization, P2 sequential release gate |
| Goal | Add traceable analytics, real exports, deeper settings/localization, and advanced operational insight after the commercial and clinical gates pass. |
| Original roadmap window | Oct 6–19, 2026; Oct 19 broader-rollout target in the [deck](../../../../reports/2026-09-07/admin-provider-release-roadmap-deck/index.html). Rebaseline against prior-phase evidence and audience approval. |
| Definition of Done | Provider and Admin analytics use live traceable data; drill-down, filters, exports and audit pass; localization publish/rollback and retention observability pass; support insight is sourced and actionable; performance/reliability and expansion decision are approved. |
| Scope authority | [September roadmap Phase 4 and release rule](../../plan.md#recommended-four-phase-release-roadmap) |
| Prior-phase report | [Phase 3 readiness and fix backlog](../phase-3-settlement-partner-growth/2026-09-29-readiness-fix-backlog.md) |
| Historical sources | [May launch plan](../../../v1/plan.md), [old Sprint 4](../../../v1/phases/sprint-4/2026-06-19-readiness-fix-backlog.md), and [old Sprint 1 PR-06 findings](../../../v1/phases/sprint-1/2026-05-29-readiness-fix-backlog.md#pr-06---profile-settings-management); use only for traceability. |
| Prepared date | 2026-09-29 |
| Product review date(s) | None for this file. |
| Environment / build checked | None. |
| Scope boundary | Provider and Admin dashboard slices below. Earlier access, privacy, audit and legally required controls remain prior-phase gates; this phase adds depth rather than postponing them. |

## How to use this report

1. Verify Phase 3's clinical and commercial data sources and sequential release decision. Record environment, build, browser, role, time and disposable test-record labels before running cases.
2. Run each checkpoint with named owners. Replace `Not tested` with `Pass`, `Fail` or `Blocked`, attach persistent evidence and record a phase decision only after required checks pass. Unrelated cases may continue when a dependency blocks one path.
3. Reproduce historical PR-06 issues on the current build before treating them as current defects. Keep their original IDs and task links; do not duplicate tasks. New static signals remain `Scout flagged` with blank Bug ID until confirmed.
4. Keep functional correctness, tenant/security, export/audit, retention, localization, and measured reliability evidence distinct. Agree workload and thresholds before judging performance.

| Retest summary | Value |
|---|---|
| Pass / Fail / Blocked / Not tested | 0 / 0 / 0 / 31 |
| Phase decision | Not assessed |
| Analytics / localization / compliance / support owners | TBD |
| Performance workload / threshold / owner | Decision pending |
| Broader audience / approval owner | Decision pending |

# 1. Phase Scope From September Roadmap

## 1.1 Modules and functions in scope

| Surface | Module slice | FR / source | Phase 4 boundary |
|---|---|---|---|
| Provider | Advanced PR-05 analytics and exports | [FR-014](../../../../project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md#business-rules) | Performance views, period/filter drill-down and real export; Phase 3 owns earnings and payout essentials. |
| Provider | Remaining PR-06 settings and help | [FR-032](../../../../project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md#business-rules), [FR-021](../../../../project-requirements/functional-requirements/fr021-i18n-localization/prd.md#business-rules), [FR-033](../../../../project-requirements/functional-requirements/fr033-help-centre-management/prd.md#business-rules) | Remaining provider settings, localization and help; Phase 1 owns essential profile/pricing. |
| Admin | A-08 analytics | [FR-014](../../../../project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md#business-rules) | Live reporting, drill-down, permissioned export and audit. |
| Admin | Remaining A-09 configuration/compliance | [FR-021](../../../../project-requirements/functional-requirements/fr021-i18n-localization/prd.md#business-rules), [FR-023](../../../../project-requirements/functional-requirements/fr023-data-retention-compliance/prd.md#functional-requirements-summary), [FR-027](../../../../project-requirements/functional-requirements/fr027-legal-content-management/prd.md#functional-requirements-summary), [FR-028](../../../../project-requirements/functional-requirements/fr028-regional-config-pricing/prd.md#business-rules), [FR-030](../../../../project-requirements/functional-requirements/fr030-notification-rules-config/prd.md#business-rules) | Advanced localization, retention observability, legal version/coverage controls, regional display-pricing configuration and notification-rule history. Earlier required legal, pricing and notification safeguards are prerequisites. |
| Admin | Advanced A-10 support insight | [FR-034](../../../../project-requirements/functional-requirements/fr034-support-center-ticketing/prd.md#business-rules) | Monitoring, support analytics and operational trends; Phase 2 owns basic ticket lifecycle. |

## 1.2 User stories in scope

### Provider

- As a provider, I can inspect my authorized performance trends, drill down to source records, and export accurate filtered data without seeing another provider's records.
- As a provider, I can configure remaining approved settings, use localized/help content, and return to safe provider-scoped destinations.

### Admin and operations

- As an authorized Admin, I can compare live service and commercial measures, inspect their source, export within my role, and see an audit trail.
- As a configuration or compliance owner, I can publish and roll back localization, inspect legal-content versions and acceptance coverage, manage approved regional display-pricing configuration, review notification-rule history, and observe applicable retention controls.
- As a support lead, I can monitor case load and outcomes from real tickets and drill into permitted records.

## 1.3 Explicitly deferred / outside this phase

| Item | Destination / decision | Reason |
|---|---|---|
| Phase 1 onboarding/inquiry/quote, Phase 2 clinical/aftercare, Phase 3 settlement/growth | Prerequisite and regression basis | These functions keep their earlier owners; analytics consumes their verified records. |
| Essential access, privacy, audit, legal acceptance, pricing correctness and critical notification safeguards | Earlier phase gate | They cannot wait for advanced A-09 tooling. |
| Provider review responses and other unnamed PR-06 work | Scope decision | The roadmap does not automatically assign them to remaining settings/help. |
| FR-036, affiliate-facing portal, patient app certification and public consumer launch | Separate scope and proof | The dashboard roadmap did not assess or assign these as Phase 4 deliverables. |

# 2. Retest Checkpoints

## 2.0 Run metadata and safe test data

| Field | Value |
|---|---|
| Environment / build / date | TBD / TBD / TBD |
| Browser / authorized and denied roles | TBD / TBD |
| Source booking, finance, ticket, locale and retention test-record labels | TBD; no personal data in report |
| Analytics definition, locale, retention and rollout owners | TBD |

Use designated test data and masked evidence. For exports, verify content in a controlled location and avoid placing personal, clinical or financial values in this report. `Not tested / Pass / Fail / Blocked` applies only to this matrix; backlog Task Status uses the reporting vocabulary.

### Checkpoint 1 — Prior gates, source lineage and permissions

Prerequisite: approved Phase 1–3 release evidence and named definitions for each displayed metric.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P4-01 | Phase 3 gate | Phase 1–3 reports and sign-offs | 1. Read sequential decisions<br>2. List required unresolved Fail/Blocked cases | Required prior gates passed for this audience before enabling Phase 4 | Not tested | TBD | Date is not evidence. |
| P4-02 | PR-05 / A-08 / FR-014 | Approved metric definitions and source records | 1. Select one clinical and one commercial metric<br>2. Trace each displayed value to source events and formula | Values reconcile to current authoritative records and approved definitions | Not tested | TBD | |
| P4-03 | PR-05 / A-08 | Provider A/B and Admin role matrix | 1. Open same period by Provider A and B<br>2. Attempt cross-tenant drill-down/API access | Each provider sees only owned records; Admin scope matches role; denied calls expose no data | Not tested | TBD | Tenant/privacy gate. |
| P4-04 | PR-05 / A-08 | Missing, delayed and corrected source records | 1. Open report during source exception<br>2. Refresh after correction | Missing/stale state is explicit; no sample metric, cached wrong total or silent fallback | Not tested | TBD | |
| P4-05 | A-08 / FR-014 | Approved metric and date range | 1. Compare Provider and Admin aggregate where scope overlaps<br>2. Check time zone, currency and date boundaries | Shared facts reconcile under documented aggregation/filter rules | Not tested | TBD | |

Exit: metric lineage, source freshness and access scope are explicit before reporting is used for decisions.

### Checkpoint 2 — Provider analytics, drill-down and export

Prerequisite: Provider PR-05 advanced screens, test source records and allowed export role.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P4-06 | PR-05 / FR-014 | Multiple periods and service types | 1. Change date/service filters<br>2. Compare chart, summary and underlying records | All views apply the same filters and show real data with defined empty states | Not tested | TBD | |
| P4-07 | PR-05 / FR-014 | Provider source transaction | 1. Open chart/table detail<br>2. Follow drill-down to allowed source | Drill-down lands on the correct provider-owned record with consistent figure | Not tested | TBD | |
| P4-08 | PR-05 / FR-014 | Filtered report and allowed role | 1. Request export<br>2. Compare file rows/totals/filter/time zone with UI and source | Real file generated once with correct scoped content, format and audit event | Not tested | TBD | Mask stored proof. |
| P4-09 | PR-05 / FR-014 | Denied role and other provider | 1. Request export directly by UI/API<br>2. Inspect response, file access and audit | Unauthorized export and file retrieval denied; no cross-tenant leakage | Not tested | TBD | |
| P4-10 | PR-05 / FR-014 | Source absent or export service unavailable | 1. Trigger approved failure path<br>2. Inspect UI and resulting artifacts | Clear failure/empty state; no simulated download or fallback numbers | Not tested | TBD | |

Exit: provider analytics, drill-down, export and negative access checks Pass on traceable records.

### Checkpoint 3 — Admin analytics and support insight

Prerequisite: A-08/A-10 screens, real clinical/finance/support test records and permitted/denied Admin roles.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P4-11 | A-08 / FR-014 | Multiple providers and time periods | 1. Apply permitted date/provider/status filters<br>2. Compare charts, totals and source records | Live data honors all filters and permitted scope, including empty state | Not tested | TBD | |
| P4-12 | A-08 / FR-014 | Identified metric anomaly | 1. Drill from aggregate to record<br>2. Reconcile detail and aggregate | Drill-down and source identifier explain the metric; no dead detail route | Not tested | TBD | |
| P4-13 | A-08 / FR-014 | Permitted and denied export roles | 1. Export filtered result<br>2. Compare file with source/UI<br>3. Retry as denied role | Accurate scoped file and audit for allowed role; denied export has no file/data | Not tested | TBD | |
| P4-14 | A-10 / FR-034 | Basic Phase 2 ticket records across statuses | 1. Open volume, response and escalation views<br>2. Compare counts/timing with ticket timeline | Support measures are computed from real cases and defined clocks | Not tested | TBD | |
| P4-15 | A-10 / FR-034 | Selected support trend | 1. Drill into included tickets<br>2. Inspect permissions and masked detail | Tickets explain trend; sensitive data limited to authorized support role | Not tested | TBD | |
| P4-16 | A-08 / A-10 | Missing ticket/report source | 1. Exercise missing-data path<br>2. Inspect dashboard and export behavior | Explicit missing-data state; no fixture insight or misleading generated file | Not tested | TBD | |

Exit: Admin decision and support views are live, explainable, permissioned and auditable.

### Checkpoint 4 — Remaining settings, localization and retention

Prerequisite: approved locale/content/configuration and retention policies, version owners and rollback test records.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P4-17 | PR-06 / FR-032 | Provider role and remaining settings | 1. Open each in-scope setting/help route<br>2. Save/reload a safe option | Correct provider-scoped navigation, persistence and permission; essential Phase 1 settings still work | Not tested | TBD | Include historical PR-06-020/021 retest. |
| P4-18 | PR-06 / FR-021 / FR-033 | Published locale and help content | 1. Switch supported locale<br>2. Open related help/settings content | Correct published translation, fallback and route; missing content is identified | Not tested | TBD | Confirm supported locales. |
| P4-19 | A-09 / FR-021 | Draft translation/content version | 1. Edit and preview<br>2. Publish as authorized owner<br>3. Inspect Provider/Admin delivery | Approved version becomes visible only after publish; actor/time/version recorded | Not tested | TBD | |
| P4-20 | A-09 / FR-021 | Published version and prior version | 1. Roll back in approved test environment<br>2. Reload affected locale/content | Prior approved version restored consistently with traceable history | Not tested | TBD | |
| P4-21 | A-09 / FR-021 / FR-023 | Denied configuration role | 1. Attempt publish, rollback and retention-policy mutation via UI/API<br>2. Inspect state | Mutation denied server-side; published and retention state unchanged | Not tested | TBD | |
| P4-22 | A-09 / FR-023 | Approved retention policy and designated record | 1. Inspect policy/version and lifecycle events<br>2. Compare observed state with schedule and exceptions | Retention status, exceptions and audit are observable and policy-consistent | Not tested | TBD | Use non-sensitive test record. |
| P4-23 | A-09 / FR-023 | Approved deletion/retention exception test | 1. Exercise a designated deletion request with legally retained records<br>2. Inspect restricted access, outcome and audit | Protected records follow retention policy; request and exception remain observable without exposing restricted data | Not tested | TBD | Confirm policy owner and scope. |
| P4-24 | A-09 / FR-027 | Approved legal-content version and acceptance records | 1. Publish a safe test version and inspect history/coverage<br>2. Check authorized access and acceptance trace | Version, effective date, actor and acceptance coverage are traceable; earlier legal gating remains effective | Not tested | TBD | Use approved non-production text. |
| P4-25 | A-09 / FR-028 | Approved region and starting-price test data | 1. Edit region/display starting price with reason<br>2. Inspect version/audit and patient-facing API after cache window | No overlapping region; approved public estimate and change history propagate without changing provider quote price | Not tested | TBD | FR-029 currency baseline is prerequisite. |
| P4-26 | A-09 / FR-030 | Approved notification rule and delivery log | 1. Inspect rule/version and masked delivery history<br>2. Change allowed template/rule and attempt disabling mandatory event | Allowed edit is audited and delivered by policy; mandatory event cannot be disabled; logs mask contact data | Not tested | TBD | Critical notification behavior already belongs to earlier gates. |

Exit: provider settings/help, localization, retention, legal version/coverage, regional display pricing and advanced notification controls Pass under approved policy.

### Checkpoint 5 — Expansion and release decision

Prerequisite: prior checkpoints, pilot feedback, monitoring plan, named owners and agreed audience/workload/thresholds.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P4-27 | Cross-phase regression | Approved journey set | 1. Recheck selected inquiry→care→settlement records<br>2. Inspect analytics after correction/refund | Earlier gates remain valid and analytics reflects changed source states | Not tested | TBD | |
| P4-28 | Audit/privacy gate | Export, config and retention actions | 1. Consolidate positive and denied-role actions<br>2. Verify audit, file access and retention evidence | Required events trace to actor/time/source without leaking tenant data | Not tested | TBD | |
| P4-29 | Reliability/performance | Approved workloads and thresholds | 1. Run measured workload/reliability suite<br>2. Link separate result and compare thresholds | Evidence meets approved thresholds for enabled cohort and expected expansion | Not tested | TBD | Threshold and owner pending. |
| P4-30 | Operations readiness | Support capacity, monitoring and rollback owner | 1. Review pilot feedback and incident plan<br>2. Exercise rollback/alert path as approved | Owners can detect, triage and roll back material failure; support capacity accepted | Not tested | TBD | |
| P4-31 | Release approval | All required cases and explicit audience | 1. Reconcile Pass/Fail/Blocked and open risks<br>2. Record stakeholder go/no-go and audience | No required Fail/Blocked; signed decision names exact dashboard cohort or expansion scope | Not tested | TBD | Public consumer/patient launch needs separate proof. |

**Phase 4 result:** Not assessed. This matrix has 31 `Not tested` cases.

# 3. Phase Fix Backlog

The September [static dashboard audit](../../plan.md) supplies review signals, not confirmed runtime defects. Historical PR-06 Bug IDs retain their old task state but have not been retested on this build. Assign a new stable ID only after a new product finding is reproduced.

## 3.1 Phase-level blockers and evidence gaps

| Bug ID | Priority | Area | Issue / evidence gap | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P0 | Sequential gate | Phase 3 commercial acceptance and source-data proof are not recorded in this report. | Run P4-01 and compare prior reports. | Not checked in this pass. | Required prior gates pass before Phase 4 enablement. | TBD | Review pending | Dependency, not product bug. |
|  | P1 | Metric/policy ownership | Metric definitions, supported locales, retention policy and expansion audience are not approved here. | Name owners and versions before P4-02, P4-19, P4-22 and P4-31. | Decision pending. | Objective assertions and bounded rollout decision. | TBD | Review pending | |
|  | P1 | Historical PR-06 placement | The Phase 1 report leaves other historical settings/profile rows outside its essential slice; their owner is not settled here. | Review old PR-06-005, 007–013 and 022–029 with product and the earlier access gate. | Scope not decided in this pass. | Assign only approved remaining settings/help here; raise access, validation or legally required fixes in the earliest owning gate. | [Phase 1 PR-06 review](../phase-1-controlled-commercial-pilot/2026-09-17-readiness-fix-backlog.md#34-pr-06---profile-settings-essential-profilepricingpackages) | Review pending | Do not silently import reviews, awards or documents. |
|  | P1 | Measured release proof | Workload, thresholds and monitoring/rollback owner are undefined in this file. | Define then run P4-29/30. | No performance run recorded. | Measured evidence and operational owner support the chosen audience. | TBD | Review pending | |

## 3.2 PR-05 — Advanced analytics and export

### Review Notes

- No Phase 4 runtime review; test P4-02 to P4-10. Earnings/payout correctness remains Phase 3 baseline.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Provider analytics | Static audit reports hard-coded analytics, simulated export and fallback values. | Run P4-02 to P4-10 using real source records and missing-data cases. | Runtime behavior not tested. | Traceable, scoped analytics and real export without production fallback. | [September PR-05 finding](../../plan.md#provider-dashboard-status) | Scout flagged | |

## 3.3 PR-06 — Remaining settings and help

### Review Notes

- No Phase 4 runtime review; test P4-17/18 and prior security gates. Historical records below are not proof of a current-build defect. If the Admin route exposure persists, it affects the earlier access gate and must be raised there immediately.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| PR-06-020 | P1 | Provider Languages Cancel | Historical review found Cancel routed a provider to an Admin provider-management surface. | Re-run P4-17; follow Languages Cancel and attempt Admin-only path as provider. | Current build not retested. | Return to provider-scoped route; no Admin access. | [Old Sprint 1 record](../../../v1/phases/sprint-1/2026-05-29-readiness-fix-backlog.md#pr-06---profile-settings-management) | Task created (FE: HAIRL-1380) | Existing task state copied for traceability; escalate to earlier access gate if still present. |
| PR-06-021 | P1 | Provider navbar Profile Setting | Historical review found the shortcut self-linked to the current route. | Re-run P4-17 from two provider screens and inspect destination. | Current build not retested. | Stable provider-scoped settings route. | [Old Sprint 1 record](../../../v1/phases/sprint-1/2026-05-29-readiness-fix-backlog.md#pr-06---profile-settings-management) | Task created (FE: HAIRL-1381) | Existing task state copied for traceability. |
|  | P1 | Remaining settings/help | Static audit reports incomplete localization, disconnected support cases and help fallback content. | Run P4-17/18 with saved setting and published help content. | Runtime behavior not tested. | Remaining released settings and help use authoritative state. | [September PR-06 finding](../../plan.md#provider-dashboard-status) | Scout flagged | Unassigned review-response work is excluded. |

## 3.4 A-08 — Analytics and reporting

### Review Notes

- No Phase 4 runtime review; test P4-02 to P4-05 and P4-11 to P4-13.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Admin analytics | Static audit reports fixture-driven screens and aggregate-route/response mismatches; audit, drill-down and export need proof. | Run P4-11 to P4-13 on real records and denied roles. | Runtime behavior not tested. | Traceable metrics, live drill-down and permissioned export. | [September A-08 finding](../../plan.md#admin-dashboard-status) | Scout flagged | |

## 3.5 A-09 — Advanced configuration, localization and compliance

### Review Notes

- No Phase 4 runtime review; test P4-19 to P4-26. Earlier required access, privacy, legal acceptance, pricing and critical notifications are not deferred here.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Localization publish/rollback | Static audit reports localization demo data; published version and rollback behavior need proof. | Run P4-19 to P4-21 with approved versions. | Runtime behavior not tested. | Authorized versioned publish/rollback reaches Provider/Admin surfaces. | [September A-09 finding](../../plan.md#admin-dashboard-status) | Scout flagged | |
|  | P1 | Retention observability | Static audit reports incomplete retention/compliance workflow. | Run P4-22/23 against approved policy/test record. | Runtime behavior not tested. | Retention state, exceptions and audit are observable. | [September A-09 finding](../../plan.md#admin-dashboard-status) | Scout flagged | |
|  | P1 | Regional display pricing | Static audit reports regional-pricing CRUD/version evidence remains incomplete. | Run P4-25 with an approved region and estimate. | Runtime behavior not tested. | Scoped price configuration persists, propagates and retains reason/version/audit. | [September A-09 finding](../../plan.md#admin-dashboard-status) | Scout flagged | Quote/payment correctness remains an earlier gate. |
|  | P1 | Notification configuration history | Static audit reports notification-history demo data. | Run P4-26 with real delivery and rule history. | Runtime behavior not tested. | Real masked history and permitted rule/version actions; mandatory events stay protected. | [September A-09 finding](../../plan.md#admin-dashboard-status) | Scout flagged | Critical notification delivery belongs to earlier gates. |

## 3.6 A-10 — Advanced support monitoring and analytics

### Review Notes

- No Phase 4 runtime review; test P4-14 to P4-16. Basic ticket intake/response remains Phase 2.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Support insight | Static audit reports mock-backed support lists/forms/configuration; advanced measures need real ticket-source proof. | Run P4-14 to P4-16 with real test tickets. | Runtime behavior not tested. | Real, scoped support measures and drill-down. | [September A-10 finding](../../plan.md#admin-dashboard-status) | Scout flagged | |

# 4. Not For This Phase

| Item | Reason / destination | Follow-up |
|---|---|---|
| Inquiry/quote, paid care, aftercare and settlement | Earlier phase gates | Regression where needed; no reclassification of module ownership. |
| Essential access, privacy, audit and compliance | Earlier gate required for safe operation | Escalate any persistent leak to owning phase immediately. |
| Provider review responses, FR-036, affiliate-facing portal | Unassigned or separate scope | Record explicit stakeholder decision and evidence before addition. |
| Public consumer launch and patient app certification | Outside the dashboard audit | Separate end-to-end and app release decision. |
