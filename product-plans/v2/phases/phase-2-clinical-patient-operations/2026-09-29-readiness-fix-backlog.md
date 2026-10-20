# Phase 2 Readiness & Fix Backlog — Clinical and Patient Operations

> **Preparation status, 2026-09-29:** No Phase 2 product review or retest was performed for this file. Every case below is `Not tested`. The September roadmap defines the release boundary; the May/June sprint reports are historical references, not the Phase 2 acceptance baseline.

## Document Control & Phase Summary

| Field | Value |
|---|---|
| Phase | Phase 2 — Clinical and patient operations, P0 sequential release gate |
| Goal | Extend the validated commercial pilot through paid booking, treatment, aftercare and essential operational support for the enabled provider cohort. |
| Original roadmap window | Sep 15–21, 2026; Sep 21 deployment target in the [deck](../../../../reports/2026-09-07/admin-provider-release-roadmap-deck/index.html). Date must be rebaselined against actual evidence. |
| Definition of Done | Phase 1 passed; current invoice routes and paid-booking handoff work; treatment and aftercare invariants pass; messaging uses real transport with quote eligibility and durable notifications; calls are proven or explicitly excluded; clinical stakeholder scenarios, authorization and operational support pass. |
| Scope authority | [September roadmap Phase 2 and release rule](../../plan.md#recommended-four-phase-release-roadmap) |
| Prior-phase report | [Phase 1 readiness and fix backlog](../phase-1-controlled-commercial-pilot/2026-09-17-readiness-fix-backlog.md) |
| Historical sources | [May launch plan](../../../v1/plan.md), [old Sprint 2](../../../v1/phases/sprint-2/2026-06-05-readiness-fix-backlog.md) and [old Sprint 3](../../../v1/phases/sprint-3/2026-06-12-readiness-fix-backlog.md); use only for traceability. |
| Prepared date | 2026-09-29 |
| Product review date(s) | None for this file. |
| Environment / build checked | None. |
| Scope boundary | Provider and Admin dashboard functions below. Patient acceptance, booking/payment and aftercare participation are required integration paths but were not certified by the dashboard roadmap. |

## How to use this report

1. Confirm Phase 1 gate evidence and the named owner for patient acceptance, payment and aftercare participation. Record environment, build, browser/device, role, time and approved test-record labels below.
2. Run checkpoints in order when their prerequisites exist. Change `Not tested` to `Pass`, `Fail` or `Blocked` per case; add persistent evidence and observations. A required `Fail` or `Blocked` prevents phase sign-off, while independent cases may continue.
3. Enter a confirmed bug only after recording reproduction, actual and expected behavior and evidence. Give it a stable module Bug ID. Static findings remain `Scout flagged` with blank Bug ID; evidence gaps remain `Review pending`.
4. Keep functional/security results separate from performance and reliability results. Agree workload, threshold and sign-off owner before claiming those qualities pass.

| Retest summary | Value |
|---|---|
| Pass / Fail / Blocked / Not tested | 0 / 0 / 0 / 36 |
| Phase decision | Not assessed |
| Clinical acceptance owner / date | TBD |
| Performance workload / threshold / owner | Decision pending |

# 1. Phase Scope From September Roadmap

## 1.1 Modules and functions in scope

| Surface | Module slice | FR / source | Phase 2 boundary |
|---|---|---|---|
| Provider | PR-03 treatment execution | [FR-010](../../../../project-requirements/functional-requirements/fr010-treatment-execution/prd.md#business-rules) | Check-in, daily evidence, completion/cancellation and handoff from a valid paid booking. |
| Provider | PR-04 aftercare | [FR-011](../../../../project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md#business-rules) | Assigned case, plan, progress, clinician actions and escalation. |
| Provider | Core PR-07 messaging | [FR-012](../../../../project-requirements/functional-requirements/fr012-secure-messaging/prd.md#business-rules), [FR-020](../../../../project-requirements/functional-requirements/fr020-notifications-alerts/prd.md#business-rules) | Eligible real messages and durable notifications. Call service must be proven or excluded. |
| Admin | A-01 booking/treatment intervention | [FR-016](../../../../project-requirements/functional-requirements/fr016-admin-patient-mgmt/prd.md#business-rules) | Booking and clinical oversight beyond Phase 1 inquiry/quote controls. |
| Admin | A-03 aftercare team | [FR-011](../../../../project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md#business-rules) | Case detail, assignment, plan/notes and escalation. |
| Admin | A-04 travel | [FR-008](../../../../project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md#business-rules) | Booking-level travel review, correction and exception handling. |
| Admin | Basic A-10 support | [FR-034](../../../../project-requirements/functional-requirements/fr034-support-center-ticketing/prd.md#business-rules) | Minimum case intake, assignment, reply and escalation; settle the exact subset before sign-off. |
| Admin | Minimum A-05 invoice/refund | [FR-007](../../../../project-requirements/functional-requirements/fr007-payment-processing/prd.md#business-rules), [FR-017](../../../../project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md#business-rules) | Current invoice and refund routes only; reconciliation and payout are Phase 3. |

**Required integration, not a dashboard module claim:** one current [FR-005 accepted subquote](../../../../project-requirements/functional-requirements/fr005-quote-comparison-acceptance/prd.md#business-rules) holds its slot; [FR-006 booking](../../../../project-requirements/functional-requirements/fr006-booking-scheduling/prd.md#business-rules) becomes Confirmed after successful deposit/first installment; [FR-007 payment](../../../../project-requirements/functional-requirements/fr007-payment-processing/prd.md#business-rules) supplies the paid state. Name and verify the patient-side route and evidence before clinical tests.

## 1.2 User stories in scope

### Provider

- As authorized clinical staff, I can check in a paid, date-eligible booking, record each treatment day and required evidence, finish treatment and initiate the aftercare handoff.
- As an assigned provider, I can manage the aftercare plan and case progress without accessing another provider's patient.
- As an eligible care participant, I can send and receive real messages with durable notification history.

### Admin

- As an authorized Admin, I can intervene in booking/treatment and aftercare with a reason and audit trail, manage travel exceptions, and operate basic support.
- As an authorized finance Admin, I can see current invoices and execute only the approved minimum refund controls.

### Shared journey

- The accepted quote, slot hold, paid booking, treatment, aftercare and patient participation are traceable end to end; a missing upstream path is `Blocked`, never presumed complete.

## 1.3 Explicitly deferred / outside this phase

| Item | Destination / decision | Reason |
|---|---|---|
| PR-05 earnings/payout, A-05 reconciliation/payout, A-06 promotions, A-07 affiliate | [Phase 3](../phase-3-settlement-partner-growth/2026-09-29-readiness-fix-backlog.md) | Financial settlement and partner growth. |
| Advanced PR-05 analytics, remaining PR-06 settings/help, A-08 analytics, advanced A-09 configuration, advanced A-10 insight | [Phase 4](../phase-4-scale-optimization/2026-09-29-readiness-fix-backlog.md) | Scale and optimization. |
| FR-037/FR-038 Admin monitoring | Stakeholder decision before clinical scope lock | September roadmap explicitly asks whether it belongs to the first clinical release or is formally deferred. |
| Patient app certification and public consumer launch | Separate scope/evidence decision | The roadmap's audit covers dashboards only. Patient actions needed here remain integration gates. |

# 2. Retest Checkpoints

## 2.0 Run metadata and safe test data

| Field | Value |
|---|---|
| Environment / build / date | TBD / TBD / TBD |
| Browser or device / role labels | TBD / TBD |
| Test-record labels and upstream channel | TBD; no personal data in report |
| Approved clinical, travel, finance and support testers | TBD |

Use designated records in an approved test environment for payment, refund, treatment, travel, messaging, permission-denial and cancellation tests. Do not create failures against real patient or provider records. Record the actual route, response and audit reference without secrets or personal data. `Not tested / Pass / Fail / Blocked` applies only to this matrix; backlog `Task Status` uses the reporting vocabulary.

### Checkpoint 1 — Paid booking and access handoff

Prerequisite: Phase 1 gate passes; a designated patient can receive and accept a current subquote through an agreed existing path. If that path is unavailable, dependent cases are `Blocked`.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P2-01 | Phase 1 gate | Phase 1 report and sign-off | 1. Review the Phase 1 matrix and release decision<br>2. List unresolved failures/blocks | All required Phase 1 gates passed before Phase 2 enablement | Not tested | TBD | Do not infer readiness from the date. |
| P2-02 | FR-005 / FR-006 | Current unaccepted subquote and free slot | 1. Accept the exact subquote through approved patient path<br>2. Inspect version, competing outcomes and slot hold | One accepted selection/version; exclusive hold; sibling and competing outcomes consistent; no money collected at acceptance | Not tested | TBD | Patient path owner TBD. |
| P2-03 | FR-006 / FR-007 | Held appointment and approved payment sandbox | 1. Complete deposit/first installment<br>2. Open booking and calendar | Booking becomes Confirmed only on successful payment; held slot becomes confirmed block | Not tested | TBD | No live financial transaction. |
| P2-04 | FR-006 / FR-007 | Separate approved failed-payment record | 1. Fail or abandon payment<br>2. Reopen booking and slot | No false Confirmed booking; hold/failure state follows configured policy; no duplicate charge | Not tested | TBD | |
| P2-05 | FR-006 / FR-010 | Paid booking plus pre-payment comparator | 1. Compare provider identity fields before/after confirmed payment<br>2. Try unrelated provider access | Identity opens only at the permitted state and only to assigned provider; unrelated provider denied | Not tested | TBD | Privacy gate. |
| P2-06 | A-01 / FR-016 | Authorized and read-only Admin roles | 1. Open booking/treatment oversight<br>2. Perform one authorized intervention on test record<br>3. Retry with denied role | Authorized action works with reason/audit; denied role cannot mutate | Not tested | TBD | |
| P2-07 | A-05 / FR-007 / FR-017 | Approved test invoice/refund record | 1. Open generated invoice<br>2. Exercise approved refund control and audit view | Current live invoice/refund contract works; amount/state/audit agree; no fallback amount | Not tested | TBD | Minimum Phase 2 finance only. |

Exit: all required handoff, privacy and paid-state cases Pass; a missing patient/payment route blocks clinical sign-off.

### Checkpoint 2 — Treatment execution

Prerequisite: designated confirmed, paid booking for procedure date; Owner/Manager/Clinical and Billing roles.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P2-08 | PR-03 / FR-010 | Future and eligible bookings | 1. Inspect Check In availability on each<br>2. Attempt future-date and unpaid entry | Only eligible Confirmed booking can check in; future/unpaid entry is rejected server-side | Not tested | TBD | |
| P2-09 | PR-03 / FR-010 | Differing provider roles | 1. Check in as permitted role<br>2. Try treatment mutation as Billing or unrelated clinic | Permitted roles act; Billing cannot edit; unrelated clinic cannot view or mutate | Not tested | TBD | |
| P2-10 | PR-03 / FR-010 | In-progress multi-day treatment | 1. Add daily entry, notes and permitted scans<br>2. Save and reload | Separate day records and media persist with correct patient, clinician and timezone display | Not tested | TBD | |
| P2-11 | PR-03 / FR-010 | In-progress treatment | 1. Change day status through allowed values<br>2. Attempt invalid or duplicate in-progress state | Only allowed states accepted; one active treatment per patient; all transitions audited | Not tested | TBD | |
| P2-12 | PR-03 / FR-010 | Checked-in treatment | 1. Try changing locked plan/clinicians as Provider<br>2. Apply authorized Admin override with reason | Provider change denied; Admin override preserves prior value and reason in audit | Not tested | TBD | |
| P2-13 | PR-03 / FR-010 | Incomplete then complete treatment | 1. Attempt completion with missing required evidence<br>2. Supply evidence and complete | Missing required data blocks completion; valid completion creates the specified aftercare handoff | Not tested | TBD | |
| P2-14 | PR-03 / A-01 | Disposable case with cancellation reason | 1. Exercise Cancel/Close Case path<br>2. Inspect status, finance and Admin queue | No automatic financial action or silent terminal transition; Admin handles required closure steps | Not tested | TBD | |

Exit: treatment lifecycle, payment/date/role gates, completion and handoff cases Pass.

### Checkpoint 3 — Aftercare and clinical ownership

Prerequisite: completed treatment and approved aftercare template/configuration source; separate standalone case only if that service is included by the clinical owner.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P2-15 | PR-04 / A-03 / FR-011 | Completed treatment | 1. Open linked case in Provider and Admin<br>2. Compare activation and ownership | One correctly linked case activates per rule; provider and Admin see authorized views | Not tested | TBD | |
| P2-16 | PR-04 / FR-011 | Two provider organizations | 1. Open assigned case as owning provider<br>2. Try detail, notes, media and mutations as other provider | All case resources enforce provider ownership, including direct API access | Not tested | TBD | |
| P2-17 | A-03 / FR-011 | Admin and available clinician records | 1. Assign/reassign clinician<br>2. Reload both dashboards | Assigned clinician and availability come from live data; changes persist with audit | Not tested | TBD | |
| P2-18 | PR-04 / A-03 / FR-011 | Active plan and template | 1. Select/edit permitted plan milestones and medication<br>2. Save and reopen | Plan reflects authoritative template and permitted edits; Provider/Admin views agree | Not tested | TBD | Template owner TBD. |
| P2-19 | FR-011 patient dependency | Agreed patient channel | 1. Open assigned aftercare plan as patient<br>2. Submit permitted progress/check-in | Patient can access only own case; activity reaches Provider/Admin and preserves status | Not tested | TBD | If channel unavailable, Blocked. |
| P2-20 | PR-04 / A-03 / FR-011 | Escalation case | 1. Escalate from assigned provider<br>2. Review Admin queue and respond | Escalation routes to authorized Admin with traceable status, actor and response | Not tested | TBD | |
| P2-21 | PR-04 / A-03 / FR-011 | Several designated cases | 1. Search/filter/page case lists<br>2. Open selected case | Live results and detail match filters and ownership; no hard-coded provider choices | Not tested | TBD | |

Exit: case creation, ownership, plan, patient participation and escalation Pass; missing template or patient path blocks release.

### Checkpoint 4 — Travel, messaging, support and finance controls

Prerequisite: eligible cohort booking/case and approved test records for messages, travel and support.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P2-22 | A-04 / FR-008 | Confirmed booking from accepted Path A subquote | 1. Confirm initial payment and inspect booking Travel section plus automated passport request<br>2. Retry the booking event<br>3. Correct permitted hotel/flight data with reason and reopen history | One booking-owned TravelContext and passport request; no duplicate on replay; latest travel state, prior version and audit visible with required re-notification | Not tested | TBD | Provider books included services externally; no separate travel dashboard. |
| P2-23 | A-04 / FR-008 | Confirmed booking from accepted Path B subquote | 1. Inspect automated flight/hotel request after payment<br>2. Retry event and submit/review patient travel details through approved channel<br>3. Inspect exception handling | One booking-owned TravelContext/request; no passport prompt or duplicate; Admin/provider see current Path B details and can resolve an exception without losing history | Not tested | TBD | Patient channel owner TBD; no mixed Path A/B submission. |
| P2-24 | PR-07 / FR-012 | Eligible quoted conversation | 1. Send text/media via Provider path<br>2. Read on recipient path<br>3. Reload history | Real transport persists message, media/access, timestamps and read state; no mock send | Not tested | TBD | |
| P2-25 | PR-07 / FR-012 | Ineligible and unrelated-provider accounts | 1. Attempt new conversation before eligibility<br>2. Request another provider's thread | Both denied without leaking thread or patient data | Not tested | TBD | |
| P2-26 | PR-07 / FR-020 | Delivered message | 1. Inspect notification event/delivery record<br>2. Retry or simulate transient failure in approved environment | Notification is durable with correct recipient/state; retry does not duplicate the message | Not tested | TBD | |
| P2-27 | Call decision | Product/QA decision recorded | 1. If included, run authenticated audio/video call path with evidence<br>2. Otherwise verify it is absent from enabled cohort | Call is proven on its real service or explicitly excluded from Phase 2 release | Not tested | TBD | Required explicit decision. |
| P2-28 | A-10 / FR-034 | Designated support request | 1. Create case via agreed entry point<br>2. Assign, reply and escalate<br>3. Reopen history | Basic ticket lifecycle uses live API, correct roles and durable audit; no fixture case | Not tested | TBD | Minimum action set to approve. |
| P2-29 | A-05 / FR-017 | Approved finance roles/test invoice | 1. Retry invoice/refund action with unauthorized role<br>2. Inspect audit and amount | Denied mutation; no money/status change; authorized action remains traceable | Not tested | TBD | |

Exit: required operational paths and negative permissions Pass; call scope resolved.

### Checkpoint 5 — Clinical release decision

Prerequisite: prior checkpoint evidence, stakeholder scenarios and provider feedback channel.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P2-30 | Integrated care path | Approved cohort records | 1. Trace accepted quote through payment, check-in, completion and aftercare<br>2. Verify Admin interventions | One coherent lifecycle with no undocumented workaround or sample fallback | Not tested | TBD | |
| P2-31 | Security gate | Two providers; multiple roles | 1. Collect tenant/role denials across treatment, aftercare, messages, support, travel and finance<br>2. Check audit | No cross-provider access or excess Admin privilege; audit follows each sensitive action | Not tested | TBD | |
| P2-32 | Route/data gate | Released screens and routes | 1. Compare each FE action to authoritative API<br>2. Force approved missing-data state | No stale route or silent fixture fallback in released functions | Not tested | TBD | |
| P2-33 | Stakeholder acceptance | Clinical owner, Provider and QA | 1. Walk agreed realistic care, exception and escalation scenarios<br>2. Record sign-off/feedback | Clinical owner accepts the actual enabled scope and unresolved items are explicit | Not tested | TBD | |
| P2-34 | Performance/reliability | Agreed workload and owner | 1. Run separate measured workload/reliability assessment<br>2. Link report | Threshold and observed evidence recorded; manual timings alone do not count | Not tested | TBD | No numeric SLA invented. |
| P2-35 | FR-037/FR-038 decision | Stakeholder decision owner | 1. Record include/defer decision<br>2. If included, add its acceptance evidence; if deferred, check disabled access | Monitoring scope explicit; no invisible Phase 2 dependency | Not tested | TBD | Decision pending. |
| P2-36 | Release decision | All required cases | 1. Reconcile Pass/Fail/Blocked and known bugs<br>2. Record cohort and go/no-go owner | No required Fail/Blocked; sequential Phase 1→2 gates and owners signed | Not tested | TBD | |

**Phase 2 result:** Not assessed. This matrix has 36 `Not tested` cases. Do not mark a phase passed from document preparation alone.

# 3. Phase Fix Backlog

The September [static dashboard audit](../../plan.md) supplies risk signals, **not confirmed product defects**. The old Sprint 2–4 reports contain no confirmed bug-ID rows for these slices. When testing begins, preserve any newly confirmed Bug ID across reports and update its actual task lifecycle.

## 3.1 Phase-level blockers and evidence gaps

| Bug ID | Priority | Area | Issue / evidence gap | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P0 | Clinical entry | Phase 1 and accepted paid-booking handoff have no Phase 2 retest evidence in this file. | Run P2-01 to P2-07. | Not checked in this preparation pass. | Prior gate and paid state proven before clinical activation. | TBD | Review pending | Dependency, not a product bug. |
|  | P0 | Patient participation | Patient app/accepted-booking/aftercare channels were outside the dashboard audit. | Name and run the approved patient path in P2-02, P2-19 and P2-23. | Channel and owner not established here. | Required cross-surface path has named owner and runtime evidence. | TBD | Review pending | Do not invent a substitute route. |
|  | P1 | Monitoring scope | FR-037/FR-038 inclusion for the first clinical release remains a stakeholder decision. | Record decision in P2-35. | No decision recorded in this file. | Inclusion plus tests, or explicit deferral. | [Roadmap decisions](../../plan.md#decisions-required-in-the-meeting) | Review pending | |

## 3.2 PR-03 — Treatment execution

### Review Notes

- No Phase 2 runtime review; test P2-08 to P2-14. The September static audit identifies a divergent legacy lifecycle and incomplete payment/date/role gates.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P0 | Treatment lifecycle | Static source review found legacy and current lifecycle paths that may disagree. | Run P2-08 to P2-14 on one paid case. | Runtime behavior not tested. | One authoritative lifecycle enforces all entry, documentation and completion rules. | [September PR-03 finding](../../plan.md#provider-dashboard-status) | Scout flagged | No new confirmed bug ID. |

## 3.3 PR-04 — Aftercare

### Review Notes

- No Phase 2 runtime review; test P2-15 to P2-21. The September static audit flags case ownership, search/pagination and clinician assignment.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P0 | Case access | Static source review indicates provider ownership may be missing on aftercare resources and mutations. | Run P2-15, P2-16 and P2-21 as two providers. | Runtime behavior not tested. | Only assigned provider can read and change case data. | [September PR-04 finding](../../plan.md#provider-dashboard-status) | Scout flagged | |

## 3.4 PR-07 — Core messaging

### Review Notes

- No Phase 2 runtime review; test P2-24 to P2-27. Calls need a separate prove-or-exclude decision.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P0 | Message delivery | Static source review reports mock-default send transport and incomplete eligibility/notification behavior. | Run P2-24 to P2-26. | Runtime behavior not tested. | Eligible real messages and durable notifications; denied ineligible sends. | [September PR-07 finding](../../plan.md#provider-dashboard-status) | Scout flagged | |

## 3.5 A-01 — Booking and treatment intervention

### Review Notes

- No Phase 2 runtime review; test P2-06 and P2-30 to P2-31. Phase 1 inquiry/quote oversight is a prerequisite, not a new A-01 scope here.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P0 | Admin intervention | Static audit reports missing live booking/medical-access workflows and payment-action alignment. | Run P2-06 and P2-30 with authorized/denied roles. | Runtime behavior not tested. | Required intervention works through current route with reason, role and audit. | [September A-01 finding](../../plan.md#admin-dashboard-status) | Scout flagged | FR-037/038 requires separate decision. |

## 3.6 A-03 — Aftercare team

### Review Notes

- No Phase 2 runtime review; test P2-15 to P2-21. Required aftercare template/configuration ownership is pending.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Case management | Static audit identifies unrouted case detail, hard-coded availability and missing plan/notes controls. | Run P2-17 to P2-21. | Runtime behavior not tested. | Live case detail, assignment, plan/notes and escalation work with RBAC/audit. | [September A-03 finding](../../plan.md#admin-dashboard-status) | Scout flagged | |

## 3.7 A-04 — Travel

### Review Notes

- No Phase 2 runtime review; test P2-22 to P2-23. Current FR-008 starts at Confirmed booking and places travel in booking detail; it does not require a separate travel dashboard.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Travel corrections | September static audit flagged incomplete correction history; current FR-008 also requires booking-owned requests and idempotent initiation. | Run P2-22 and P2-23. | Runtime behavior not tested. | Correct booking travel state, versions, audit and notifications remain traceable. | [September A-04 finding](../../plan.md#admin-dashboard-status), [current FR-008](../../../../project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md#business-rules) | Scout flagged | Historical system-wide dashboard concern is superseded by current booking-detail scope. |

## 3.8 A-05 — Minimum invoice/refund

### Review Notes

- No Phase 2 runtime review; test P2-07 and P2-29. Settlement and payouts have a separate [Phase 3](../phase-3-settlement-partner-growth/2026-09-29-readiness-fix-backlog.md) section.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P0 | Invoice/refund | Static audit reports legacy invoice actions and fallback financial values. | Run P2-07 and P2-29. | Runtime behavior not tested. | Current invoice/refund routes and amounts with authorized, audited actions. | [September A-05 finding](../../plan.md#admin-dashboard-status) | Scout flagged | |

## 3.9 A-10 — Basic support

### Review Notes

- No Phase 2 runtime review; test P2-28. Agree the minimum support action set before a pass verdict; advanced monitoring/analytics is Phase 4.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Support ticket | Static audit reports mock-backed case lists/forms/configuration. | Run P2-28 with a real designated support case. | Runtime behavior not tested. | Basic ticket lifecycle uses the authoritative API with role and audit. | [September A-10 finding](../../plan.md#admin-dashboard-status) | Scout flagged | |

# 4. Not For This Phase

| Item | Reason / destination | Follow-up |
|---|---|---|
| Provider earnings/payout and Admin reconciliation/payout | Phase 3 settlement | Keep Phase 2 invoice/refund evidence for later reconciliation. |
| Promotions and affiliate operations | Phase 3 growth | Do not treat quote content as a released promotion program. |
| Advanced analytics/exports, localization/settings depth and support insight | Phase 4 scale | Earlier legal/security baseline still applies. |
| Public consumer launch and affiliate-facing portal | Not established by dashboard roadmap | Separate scope and evidence decision. |
| FR-036 | Deferred | No implementation-ready Phase 2 scope. |
