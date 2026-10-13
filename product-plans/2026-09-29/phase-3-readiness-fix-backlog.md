# Phase 3 Readiness & Fix Backlog — Settlement and Partner Growth

> **Preparation status, 2026-09-29:** No Phase 3 product review or retest was performed for this file. Every case below is `Not tested`. The September roadmap owns release scope; the old Sprint 3/4 backlogs are historical scaffolds.

## Document Control & Phase Summary

| Field | Value |
|---|---|
| Phase | Phase 3 — Settlement and partner growth, P1 sequential release gate |
| Goal | Reconcile real care transactions, enable controlled payout, and operate promotion and affiliate programs with approved commercial rules. |
| Original roadmap window | Sep 22–Oct 5, 2026; Oct 5 target in the [deck](../../reports/2026-09-07/admin-provider-release-roadmap-deck/index.html). Rebaseline against Phase 1/2 evidence. |
| Definition of Done | Financial UI uses authoritative APIs without simulated/fallback values; payout, refund, re-authentication and audit rules pass; promotion and affiliate lifecycle contracts align; finance/partner owners approve reconciliation. |
| Scope authority | [September roadmap Phase 3 and release rule](../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md#recommended-four-phase-release-roadmap) |
| Prior-phase report | [Phase 2 readiness and fix backlog](phase-2-readiness-fix-backlog.md) |
| Historical sources | [May launch plan](../2026-05-13/launch-plan.md), [old Sprint 3](../2026-06-12/sprint-3-readiness-fix-backlog.md), [old Sprint 4](../2026-06-19/sprint-4-readiness-fix-backlog.md) for traceability only. |
| Prepared date | 2026-09-29 |
| Product review date(s) | None for this file. |
| Environment / build checked | None. |
| Scope boundary | Provider and Admin dashboard settlement/growth slices below. Affiliate-facing portal inclusion requires a separate decision. |

## How to use this report

1. Verify Phase 2's paid booking, invoice, refund and completed-treatment evidence. Record environment, build, browser, role, time and disposable test-record labels before running Phase 3 cases.
2. Run checkpoints in order where prerequisites exist. Update each `Not tested` result to `Pass`, `Fail` or `Blocked` with persistent evidence. A required Fail/Blocked keeps the phase gate open; unrelated cases may continue.
3. Log confirmed product defects only with reproducible actual/expected behavior and a stable module Bug ID. September source findings stay `Scout flagged` with blank Bug ID until product confirmation.
4. Keep transaction correctness, security/audit, financial reconciliation and performance/reliability as separate evidence. No numeric performance target is assumed.

| Retest summary | Value |
|---|---|
| Pass / Fail / Blocked / Not tested | 0 / 0 / 0 / 29 |
| Phase decision | Not assessed |
| Finance / partner acceptance owners | TBD |
| Workload / reliability threshold / owner | Decision pending |

# 1. Phase Scope From September Roadmap

## 1.1 Modules and functions in scope

| Surface | Module slice | FR / source | Phase 3 boundary |
|---|---|---|---|
| Provider | PR-05 earnings and payout essentials; promotion visibility | [FR-017](../../project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md#business-rules), [FR-019](../../project-requirements/functional-requirements/fr019-promotions-discounts/prd.md#business-rules) | Real earnings, eligible payout status and promotion participation; advanced analytics/exports are Phase 4. |
| Admin | A-05 reconciliation and payouts | [FR-017](../../project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md#business-rules) | Reconcile invoices/refunds from Phase 2; approve/execute payout and handle disputes with audit. |
| Admin | A-06 promotions | [FR-019](../../project-requirements/functional-requirements/fr019-promotions-discounts/prd.md#business-rules) | Program/code lifecycle, approval, participation, usage and commercial rules. |
| Admin | A-07 affiliate operations | [FR-018](../../project-requirements/functional-requirements/fr018-affiliate-management/prd.md#business-rules) | Admin affiliate lifecycle, codes, attribution, commission and payout controls. |

## 1.2 User stories in scope

### Provider

- As a provider, I can see authoritative earnings and payout status for eligible completed work, and see relevant promotion participation without fabricated metrics.

### Admin and finance

- As an authorized finance Admin, I can reconcile treatment, invoice, refund and payout records, resolve approved exceptions and execute payouts with re-authentication/audit where required.
- As an authorized program Admin, I can manage promotion lifecycle and affiliate attribution, codes, commissions and payout controls according to approved commercial rules.

### Shared commercial data

- The same transaction, discount and attribution facts flow consistently through Provider and Admin views; a missing or disputed source is visible and traceable.

## 1.3 Explicitly deferred / outside this phase

| Item | Destination / decision | Reason |
|---|---|---|
| Basic invoices/refunds and treatment completion | [Phase 2](phase-2-readiness-fix-backlog.md) prerequisite | Phase 3 consumes and reconciles those events. |
| Provider advanced analytics/exports, Admin A-08 analytics, advanced localization/settings/support insight | [Phase 4](phase-4-readiness-fix-backlog.md) | Scale and optimization. |
| Affiliate-facing portal/dashboard | Inclusion decision | Roadmap specifies Admin A-07 operations, not affiliate-tenant certification. |
| Patient app and public consumer launch | Separate scope/evidence decision | Dashboard roadmap did not assess them. |

# 2. Retest Checkpoints

## 2.0 Run metadata and safe financial test data

| Field | Value |
|---|---|
| Environment / build / date | TBD / TBD / TBD |
| Browser / authorized role labels | TBD / TBD |
| Designated provider, transaction, promotion and affiliate record labels | TBD; no personal or account data in report |
| Finance and partner policy/version owner | TBD |

Use approved sandbox or designated test records for money movement, refunds, re-authentication failures and negative permission checks. Do not run real payouts merely to complete a checklist. Mask identifiers and amounts where evidence leaves the test environment. `Not tested / Pass / Fail / Blocked` applies only to this matrix; backlog Task Status uses the reporting vocabulary.

### Checkpoint 1 — Financial source and reconciliation

Prerequisite: Phase 2 gate evidence, completed-treatment event, invoices, payments and any test refund/dispute state.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P3-01 | Phase 2 gate | Phase 2 report/sign-off | 1. Read release decision<br>2. List failed or blocked clinical/finance paths | Required Phase 2 paths passed before settlement enablement | Not tested | TBD | |
| P3-02 | A-05 / FR-017 | Designated completed booking and invoice | 1. Follow payment→invoice→treatment completion in finance view<br>2. Compare source identifiers/states | One traceable transaction chain with matching currency and amounts | Not tested | TBD | |
| P3-03 | A-05 / FR-017 | Designated refund and dispute cases | 1. Open each case<br>2. Compare original charge, refund/dispute and net balance | Financial state reflects approved refund/dispute logic; no silent fallback value | Not tested | TBD | |
| P3-04 | PR-05 / FR-017 | Provider with eligible and ineligible work | 1. Open earnings/payout view<br>2. Compare with authoritative finance records | Only eligible real earnings shown; status and totals reconcile | Not tested | TBD | |
| P3-05 | A-05 / PR-05 | Two provider organizations | 1. Compare Provider A statement and Admin ledger<br>2. Try Provider B access to A data | Values agree; Provider B cannot read A finances | Not tested | TBD | Privacy and tenant gate. |
| P3-06 | A-05 | Missing-data test record | 1. Open finance view with absent/invalid source in approved test environment<br>2. Inspect error/empty state | Missing data is explicit; no sample amounts, metrics or export substitution | Not tested | TBD | |

Exit: source records and displayed financial results reconcile without simulated values.

### Checkpoint 2 — Controlled payout

Prerequisite: approved commission/payout policy and eligible test statement; finance approver and denied-role account.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P3-07 | A-05 / FR-017 | Eligible statement | 1. Review line items and deductions<br>2. Approve under authorized role | Approved payout matches policy and source events; actor/time recorded | Not tested | TBD | Policy owner TBD. |
| P3-08 | A-05 / FR-017 | Approved sandbox payout | 1. Execute payout via current route<br>2. Reload status and Provider view | One execution; authoritative state visible to Admin and Provider | Not tested | TBD | No real funds. |
| P3-09 | A-05 / FR-017 | Same test statement | 1. Retry execution or replay request<br>2. Inspect external and internal records | Idempotent handling; no second payout or duplicated ledger entry | Not tested | TBD | |
| P3-10 | A-05 / FR-017 | Unauthorized finance role | 1. Attempt approval/execution<br>2. Inspect status/audit | Action denied server-side; funds/state unchanged; denial recorded as required | Not tested | TBD | |
| P3-11 | A-05 / FR-017 | Authorized role | 1. Exercise sensitive payout/refund action<br>2. Verify required re-authentication and audit | Configured re-authentication and immutable audit are enforced before mutation | Not tested | TBD | |
| P3-12 | A-05 / FR-017 | Failed or disputed payout | 1. Inspect failure handling<br>2. Resolve/retry through approved path | Exception remains visible and traceable; no false paid state | Not tested | TBD | |

Exit: approvals, one-time execution, denied access, re-authentication and exception handling Pass with finance sign-off.

### Checkpoint 3 — Promotion lifecycle and provider visibility

Prerequisite: approved program rules and test code; Admin and Provider roles.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P3-13 | A-06 / FR-019 | Draft program | 1. Create and validate a program/code<br>2. Save and reload | Program persists with approved dates, eligibility and discount rules | Not tested | TBD | |
| P3-14 | A-06 / FR-019 | Draft/active program | 1. Submit for approval<br>2. Approve, pause or end via authorized lifecycle path | Correct state transitions and permission/audit; invalid transition denied | Not tested | TBD | |
| P3-15 | A-06 / PR-05 | Shared provider participation | 1. Enable approved provider participation<br>2. Open Provider promotion view | Provider sees only applicable live program and accurate participation state | Not tested | TBD | |
| P3-16 | A-06 / FR-019 | Eligible and ineligible quote/booking paths | 1. Apply valid code on designated path<br>2. Try ineligible/expired or competing code | Approved discount is applied once under policy; invalid/stacked use rejected | Not tested | TBD | Patient checkout path owner to confirm. |
| P3-17 | A-06 / FR-019 | Used code | 1. Inspect usage/adoption<br>2. Compare to source transaction | Usage and amount reconcile; no always-on fixture metric | Not tested | TBD | |
| P3-18 | A-06 / FR-019 | Unauthorized role | 1. Attempt program mutation directly<br>2. Inspect audit/state | Denied action causes no program change or data leak | Not tested | TBD | |

Exit: program lifecycle, code application, provider visibility and usage data Pass.

### Checkpoint 4 — Affiliate operations

Prerequisite: approved affiliate contract and attribution/commission rules; Admin test affiliate and booking/code records.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P3-19 | A-07 / FR-018 | Designated affiliate | 1. Create/edit/activate affiliate<br>2. Reload list/detail | Lifecycle state and contract terms persist through current API | Not tested | TBD | |
| P3-20 | A-07 / FR-018 | Approved code and source inquiry/booking | 1. Assign code<br>2. Follow attribution into eligible transaction | Attribution links to the correct affiliate and transaction once | Not tested | TBD | |
| P3-21 | A-07 / FR-018 | Eligible and ineligible transactions | 1. Calculate commission<br>2. Compare exclusions/refunds with approved rules | Commission base, rate, threshold and rollover match policy | Not tested | TBD | |
| P3-22 | A-07 / A-05 | Eligible affiliate statement | 1. Approve/exercise sandbox affiliate payout<br>2. Reload finance and affiliate status | Single traceable payout consistent across Admin finance and affiliate operations | Not tested | TBD | No real funds. |
| P3-23 | A-07 / FR-018 | Several affiliate records | 1. Use list/search/filter and bulk code operation if in approved scope<br>2. Inspect outputs | Live records and code results match filter/action; no fixture metrics blended in | Not tested | TBD | Confirm bulk action inclusion. |
| P3-24 | A-07 / FR-018 | Unauthorized Admin role | 1. Attempt lifecycle/code/payout mutation<br>2. Inspect state and audit | Denied server-side with no unauthorized state or value change | Not tested | TBD | |

Exit: affiliate lifecycle, attribution, commission, payout and permissions Pass; portal inclusion decided explicitly.

### Checkpoint 5 — Commercial acceptance

Prerequisite: prior checkpoints and named finance/partner owners.

| Check ID | Source | Prerequisites | Steps | Expected Outcome | Result | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| P3-25 | Integrated commercial path | Phase 2 test care records | 1. Follow completed care through invoice, refund, earnings, payout and attribution<br>2. Reconcile sources | One consistent real-data chain without fallback or unexplained differences | Not tested | TBD | |
| P3-26 | Security/audit | Role and tenant matrix | 1. Consolidate payout, promotion, affiliate denied-action tests<br>2. Verify audit and re-authentication | Required sensitive actions and denials have complete traceability | Not tested | TBD | |
| P3-27 | Contract gate | Released screens/routes | 1. Compare FE action and current API method/payload/response<br>2. Exercise approved missing-data state | No legacy caller, silent fixture, simulated export or fallback number for enabled functions | Not tested | TBD | |
| P3-28 | Owner acceptance | Finance and partner owners | 1. Review reconciliations and exceptions<br>2. Record operating-policy and release approval | Commercial rules and evidence signed off; unresolved differences explicit | Not tested | TBD | |
| P3-29 | Performance/reliability and release | Defined workload and all required cases | 1. Link separate measured report<br>2. Reconcile Pass/Fail/Blocked<br>3. Record go/no-go | Threshold/workload evidence and sequential gate approved; no required Fail/Blocked | Not tested | TBD | Threshold and owner pending. |

**Phase 3 result:** Not assessed. This matrix has 29 `Not tested` cases.

# 3. Phase Fix Backlog

The September [static dashboard audit](../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md) supplies review signals, not confirmed runtime defects. The old Sprint 3/4 readiness scaffolds contain no confirmed Bug ID rows for these module slices. Assign a stable ID only after a real finding is reproduced.

## 3.1 Phase-level blockers and evidence gaps

| Bug ID | Priority | Area | Issue / evidence gap | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P0 | Clinical financial source | Phase 2 invoice, refund and completed-treatment records are not verified in this report. | Run P3-01 to P3-06. | Not checked in this pass. | Valid source events precede settlement. | TBD | Review pending | Dependency, not product bug. |
|  | P0 | Commercial rule approval | Finance and affiliate/promotion policy owners and versions are not recorded here. | Name owners before P3-07, P3-13 and P3-19. | Decision pending. | Approved rules permit objective comparison. | TBD | Review pending | |
|  | P1 | Affiliate-facing portal | The dashboard roadmap does not decide whether AF-01/affiliate portal is released. | Record inclusion/exclusion before P3-24/29 decision. | Not decided in this file. | Explicit scope and separate evidence if included. | [Roadmap Phase 3](../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md#recommended-four-phase-release-roadmap) | Review pending | |

## 3.2 PR-05 — Earnings, payout essentials and promotion visibility

### Review Notes

- No Phase 3 runtime review; test P3-04, P3-05, P3-15 and P3-25. Advanced analytics/exports remain Phase 4.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Provider finance | Static audit reports hard-coded analytics, simulated exports and payout/promotion fallbacks in PR-05. | Run P3-04, P3-05 and P3-15 on real test records. | Runtime behavior not tested. | Released earnings/payout/promotion slice uses authoritative values and status. | [September PR-05 finding](../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md#provider-dashboard-status) | Scout flagged | Advanced analytics/export aspects belong to Phase 4. |

## 3.3 A-05 — Reconciliation and payout

### Review Notes

- No Phase 3 runtime review; test P3-02 to P3-12. Phase 2 minimum invoice/refund control remains baseline.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P0 | Finance contracts | Static audit reports static finance reporting, legacy invoice actions and disconnected search/audit/payout paths. | Run P3-02, P3-03 and P3-07 to P3-12. | Runtime behavior not tested. | Reconciliation and payout actions use current real contracts with audit. | [September A-05 finding](../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md#admin-dashboard-status) | Scout flagged | Invoice/refund UI repair is Phase 2; settlement here. |

## 3.4 A-06 — Promotions

### Review Notes

- No Phase 3 runtime review; test P3-13 to P3-18.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Program lifecycle | Static audit reports lifecycle/adoption route mismatch and always-on portfolio fixture. | Run P3-13 to P3-18. | Runtime behavior not tested. | Program, code, approval and usage paths align to live API. | [September A-06 finding](../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md#admin-dashboard-status) | Scout flagged | |

## 3.5 A-07 — Affiliate operations

### Review Notes

- No Phase 3 runtime review; test P3-19 to P3-24. Portal inclusion is an unresolved scope decision.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
|  | P1 | Affiliate operations | Static audit reports billing/lifecycle/bulk-code contract mismatch and fixture metrics mixed with live data. | Run P3-19 to P3-24. | Runtime behavior not tested. | Affiliate lifecycle and finance contracts use authoritative data. | [September A-07 finding](../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md#admin-dashboard-status) | Scout flagged | |

# 4. Not For This Phase

| Item | Reason / destination | Follow-up |
|---|---|---|
| Treatment, aftercare, travel, messaging and basic support | Phase 2 baseline | Regression as needed, not a new Phase 3 module claim. |
| PR-05 advanced analytics/exports, A-08 analytics, localization and advanced settings/support | Phase 4 | Do not treat finance reconciliation evidence as full analytics release. |
| Affiliate-facing portal/dashboard | Undecided | Separate tenant scope and proof if stakeholders include it. |
| Public consumer launch, patient app certification, FR-036 | Outside this dashboard roadmap | Separate decision. |
