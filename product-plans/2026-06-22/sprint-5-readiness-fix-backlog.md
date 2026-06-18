# Sprint 5 Readiness & Fix Backlog — Launch

> Note: Sprint 5 is the **Launch** event (June 22–23), not a module-based development sprint. This scaffold adapts the standard readiness template: "Modules In Scope" is replaced by the launch activities, go-live checklist, and critical smoke-test flows from the launch plan. The backlog tracks launch-readiness gates and go/no-go evidence rather than per-module feature defects.

---

## Document Control & Sprint Summary

| Field | Value |
|---|---|
| Sprint | Sprint 5 — Launch |
| Theme | Launch: Production Deployment, Smoke Test & Go-Live |
| Dates | June 22 (Mon) - June 23 (Tue), 2026 |
| Working days | 2 (launch day + post-launch review) |
| Goal | Execute production deployment and go-live: database backup + artifact tag, production migrations, zero-downtime deployment, launch smoke test across all eight critical flows, explicit go/no-go decision, public store release trigger (or TestFlight/Google internal-track vendor-demo fallback), website DNS cutover, monitoring activation, and post-launch review + client debrief. |
| Definition of Done | Production database backed up and previous artifact tagged for rollback; migrations run and zero-downtime deployment executed; all eight critical smoke-test flows verified on production; explicit go/no-go call made before public store trigger or beta fallback; public store release triggered (or beta/internal fallback confirmed); website DNS cutover complete and go-live confirmed; all monitoring dashboards active; post-launch monitoring review and client debrief completed. |
| Source launch plan | `local-docs/product-plans/2026-05-13/launch-plan.md` |
| Prepared by | Claude AI agent |
| Prepared date | 2026-06-14 |
| Product review date(s) | Not performed in this pass; this report scaffolds the launch-readiness backlog from the launch plan. |
| Product environment(s) checked | No staging or production environment was checked in this pass. |
| Review scope boundary | Source review only. Launch activities, smoke-test flows, integrated stories, and readiness gates are derived from the Sprint 5 (Launch) section of the launch plan. Production launch evidence must be added during the go-live window with persistent evidence links. |

<!--
AI agent guidance: Keep this guidance hidden from Markdown preview. It exists only to preserve the intended workflow for future agents editing this report.

## How To Use This Template (Launch adaptation)

- Section 1 mirrors the launch plan's Sprint 5 (Launch) section. Do not invent new launch activities; copy the go-live checklist, smoke-test flows, and integrated launch stories.
- Section 2 is the launch-readiness backlog. Capture go/no-go gates and production verification gaps in enough detail to act on during the launch window.
- Section 3 is for items explicitly out of launch scope or deferred to post-launch.
- Do not include Plane ticket IDs, assignees, estimates, or ownership fields. Those belong to the later Plane-ticket creation workflow.

### Priority Scale

| Priority | Meaning |
|---|---|
| P0 | Blocks go-live or the go/no-go decision. |
| P1 | Major launch-readiness gap that must be resolved before public release. |
| P2 | Contained issue that does not block go-live but needs early post-launch attention. |
| P3 | Minor polish or cleanup that can follow launch. |

-->

# 1. Launch Scope From Launch Plan

## 1.1 Launch Activities & Critical Flows In Scope

> Replaces "Modules In Scope" for the launch event. Go-live checklist activities and the eight critical smoke-test flows from the launch plan.

| Phase | Activity / Flow | Owner | Launch Plan Reference |
|---|---|---|---|
| Pre-deploy | Production database backup taken; previous deployment artifact tagged for rollback | DevOps | Go-Live Checklist |
| Deploy | Production database migrations run; zero-downtime deployment executed | DevOps | Go-Live Checklist |
| Verify | Launch smoke test — all eight critical user flows verified on production | QA | Go-Live Checklist |
| Decision | Go / No-Go decision point before public store trigger or beta fallback | PM | Go-Live Checklist |
| Release | Public store release trigger if both stores approved; otherwise TestFlight / Google internal-track vendor-demo fallback | Dev + PM | Go-Live Checklist |
| Release | Website DNS cutover; website go-live confirmed | DevOps | Go-Live Checklist |
| Monitor | All monitoring dashboards active — errors, payments, signups, API health | DevOps | Go-Live Checklist |
| Post-launch | Post-launch monitoring review (error rates, sign-up volumes, payment flows) | PM + DevOps | Go-Live Checklist |
| Post-launch | Post-launch debrief with client | PM + Client | Go-Live Checklist |

### Critical Smoke-Test Flows

| # | Flow | Tenants |
|---|---|---|
| 1 | Patient registers → inquiry details → selects providers → submits inquiry → receives quote → asks quote question → accepts quote → pays deposit/first installment | Mobile + Provider + Admin |
| 2 | Patient clears final balance → provider verifies fully-paid booking → provider checks in patient for treatment | Mobile + Provider + Admin |
| 3 | Confirmed booking triggers travel → patient submits Path A/Path B travel → provider reviews/enters records → admin reviews status/exceptions from booking context | All three |
| 4 | Provider completes treatment → aftercare plan activates → patient submits milestone scan → provider reviews → admin monitors case | All three |
| 5 | Patient sends message/call request → provider responds and initiates video call → admin monitoring/intervention remains auditable | Mobile + Provider + Admin |
| 6 | Patient/provider support ticket lifecycle: submit → admin reply → user follow-up → reopen/close → audit trail | Mobile + Provider + Admin |
| 7 | Promotion/affiliate: admin creates campaign → provider accepts/self-creates → patient applies one code at checkout → affiliate attribution visible | Mobile + Provider + Admin + Affiliate |
| 8 | Compliance/i18n/search: language selectors persist; DSR erasure queue works; quote/help/support and major admin/provider list filters work | All tenants |

## 1.2 Integrated Launch User Stories In Scope

> Cross-sprint business-level acceptance layer for launch readiness and final regression.

- As a new patient, I register, complete inquiry details, upload head-scan photos, select providers, receive quotes, ask a quote-specific question, accept one quote, and pay the deposit or first installment.
- As an admin, I monitor a delayed or zero-quote inquiry and intervene only through PRD-supported oversight actions.
- As a patient who cancels or requests a refund, I expect inquiry, quote, slot, payment, refund, and notification state to remain consistent.
- As a provider, I confirm treatment readiness only after the patient has cleared payment, check the patient in, document treatment day-by-day, complete it, and trigger aftercare activation.
- As a patient after treatment or standalone aftercare purchase, I follow milestones, submit scans/symptoms, and receive escalation when recovery attention is needed.
- As a patient, provider, or admin handling support/messaging, I expect each communication path to stay in its correct PRD boundary.
- As an affiliate-driven booking, the platform carries attribution from code creation to checkout, completed booking, commission accrual, dashboard visibility, and payout processing.
- As a multilingual/compliance-sensitive user, I set locale preferences, receive localized communications where available, submit/view DSR status, and rely on retention/audit behavior.
- As an operator preparing the soft launch, I run cross-tenant search/filter checks on the agreed P1 surfaces and verify public-store fallback readiness.

## 1.3 Explicitly Deferred / Out Of Scope

| Item | Launch Plan Reason / Destination | Notes |
|---|---|---|
| New app-store-affecting mobile code | Frozen since June 16 RC build | If a P0/P1 mobile-code fix is found post-freeze, public store release defers and the vendor-facing soft launch proceeds through internal/beta distribution. |
| Public store release if approvals delayed | Fallback to TestFlight / Google internal track | Vendor demos proceed through approved internal/beta distribution until public approval lands. |
| P2 post-MVP scope (patient provider-discovery search, FR-012 messaging search/filter) | Out of launch scope | Smoke flow 9 explicitly avoids pulling these in. |
| FR-036 Admin Profile & Settings Management | Outside launch delivery | Acknowledged future requirement; not a launch dependency. |

---

# 2. Launch Readiness Backlog

## 2.1 Launch-Level Blockers (Go / No-Go Gates)

| Bug ID | Priority | Area | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Production deployment | Launch cannot proceed from this report alone because no production backup/migration/zero-downtime-deployment evidence is attached. | 1. Take production DB backup and tag the rollback artifact.<br>2. Run migrations.<br>3. Execute zero-downtime deployment.<br>4. Attach evidence. | No production deployment was performed in this pass. | Backup taken, artifact tagged, migrations run, and deployment executed with evidence. | TBD | Review pending | Go/no-go gate; not a confirmed product defect. |
|  | P0 | Production smoke test | All eight critical smoke-test flows must pass on production before the go/no-go decision; not yet evidenced. | 1. Run each of the 8 smoke flows on production.<br>2. Capture pass/fail evidence per flow. | No production smoke test was run in this pass. | All 8 flows pass on production with attached evidence. | TBD | Review pending | Direct input to the go/no-go decision. |
|  | P0 | Go / No-Go decision | Explicit go/no-go call must be made (and recorded) before public store trigger or beta fallback. | 1. Review smoke-test results.<br>2. Record the explicit go/no-go decision. | Decision not made in this pass. | A recorded go/no-go decision exists before release trigger. | TBD | Review pending | PM-owned decision point. |
|  | P0 | Store release / fallback | Public store release trigger (or TestFlight/Google internal-track fallback) must be confirmed depending on approval status. | 1. Confirm both store approval statuses.<br>2. Trigger public release, or confirm beta/internal fallback. | Release status not confirmed in this pass. | Public release triggered, or beta/internal fallback confirmed. | TBD | Review pending | Approvals or fallback due by June 21 evening. |
|  | P0 | Website go-live | Website DNS cutover and go-live confirmation are not yet evidenced. | 1. Execute DNS cutover.<br>2. Confirm website is live. | DNS cutover not performed in this pass. | Website live and confirmed post-cutover. | TBD | Review pending | DNS pre-check was a Sprint 4 milestone (June 18). |
|  | P1 | Monitoring activation | All monitoring dashboards (errors, payments, signups, API health) must be active at go-live; not yet evidenced. | 1. Confirm each monitoring dashboard is active and receiving data. | Monitoring status not checked in this pass. | All dashboards active and reporting at launch. | TBD | Review pending | Required for post-launch review on June 23. |

## 2.2 Critical Flow Readiness Backlog

> One subsection per critical smoke-test flow. Capture production verification evidence or defects found during the launch window.

## Flow 1 - Inquiry → Quote → Booking → Deposit/First Installment

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Not verified on production in this pass.
- Review limits: Requires production run of registration → inquiry → provider selection → quote → quote question → acceptance → deposit/first installment.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Core commercial journey | Evidence gap: Flow 1 has not been verified on production for this report. | Run the full inquiry-to-deposit journey on production across patient/provider/admin. | Not reviewed in this pass. | Quote/slot statuses update, admin can inspect context, payment/audit records created, expired/rejected quotes handled cleanly. | TBD | Review pending | Add production defects here during launch. |

## Flow 2 - Final Balance → Check-In → Treatment

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Not verified on production in this pass.
- Review limits: Requires production run of final-balance payment → provider verification → check-in.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Final balance & check-in | Evidence gap: Flow 2 has not been verified on production for this report. | Clear final balance, verify fully-paid booking, and check in the patient on production. | Not reviewed in this pass. | Final-balance blocking works; check-in is provider-owned; states stay synchronized. | TBD | Review pending | Add production defects here during launch. |

## Flow 3 - Travel Path A/B Coordination

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Not verified on production in this pass.
- Review limits: Requires production run of travel submission (Path A/B) → provider review/entry → admin oversight from booking context.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Travel coordination | Evidence gap: Flow 3 has not been verified on production for this report. | Trigger travel from a confirmed booking, submit Path A/B, provider reviews/enters records, admin reviews status/exceptions. | Not reviewed in this pass. | Travel records flow through one shared record with correlation IDs across tenants. | TBD | Review pending | Add production defects here during launch. |

## Flow 4 - Treatment Completion → Aftercare Activation

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Not verified on production in this pass.
- Review limits: Requires production run of treatment completion → aftercare activation → milestone scan → provider review → admin monitoring.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Aftercare activation | Evidence gap: Flow 4 has not been verified on production for this report. | Complete treatment, activate aftercare, submit a milestone scan, provider reviews, admin monitors. | Not reviewed in this pass. | Aftercare plan, milestones, check-ins, escalation, and monitoring work as one connected flow. | TBD | Review pending | Add production defects here during launch. |

## Flow 5 - Messaging & Video Call with Admin Auditability

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Not verified on production in this pass.
- Review limits: Requires production run of patient message/call → provider response/video call → admin monitoring/intervention.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Secure communication | Evidence gap: Flow 5 has not been verified on production for this report. | Patient sends a message/call request, provider responds and initiates a video call, admin monitoring/intervention path verified. | Not reviewed in this pass. | Messaging/calls stay in FR-012 boundary; admin intervention remains auditable. | TBD | Review pending | Add production defects here during launch. |

## Flow 6 - Support Ticket Lifecycle

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Not verified on production in this pass.
- Review limits: Requires production run of ticket submit → admin reply → user follow-up → reopen/close → audit trail.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Support lifecycle | Evidence gap: Flow 6 has not been verified on production for this report. | Submit a patient/provider ticket, admin replies, user follows up, reopen/close, and confirm audit trail. | Not reviewed in this pass. | Full support lifecycle works within FR-034/FR-035 boundary with audit trail. | TBD | Review pending | Add production defects here during launch. |

## Flow 7 - Promotion / Affiliate Attribution

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Not verified on production in this pass.
- Review limits: Requires production run of campaign creation → provider accept/self-create → patient single-code checkout → affiliate attribution.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Promotion & affiliate | Evidence gap: Flow 7 has not been verified on production for this report. | Admin creates a campaign, provider accepts/self-creates, patient applies one code at checkout, confirm affiliate attribution and payout reconciliation. | Not reviewed in this pass. | A-06/A-07/AF-01/A-05 agree on attribution and amounts; single-code enforcement holds. | TBD | Review pending | Add production defects here during launch. |

## Flow 8 - Compliance / i18n / Search Smoke

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Not verified on production in this pass.
- Review limits: Requires production run of language selector persistence, DSR erasure queue, and P1 search/filter surfaces.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Compliance/i18n/search | Evidence gap: Flow 8 has not been verified on production for this report. | Confirm patient/provider/admin language persistence, DSR erasure queue, and quote/help/support + major admin/provider list filters. | Not reviewed in this pass. | Locale persistence, DSR queue, and P1 search/filter work; no P2 scope pulled in. | TBD | Review pending | Add production defects here during launch. |

---

# 3. Not For This Launch

| Item | Why It Is Not In This Launch | Follow-Up Notes |
|---|---|---|
| New app-store-affecting mobile code | Mobile binary frozen since June 16 RC build | Post-freeze P0/P1 mobile fixes defer public release; soft launch proceeds via internal/beta distribution. |
| P2 post-MVP scope (patient provider-discovery search, FR-012 messaging search/filter) | Out of launch scope | Smoke flow 9 explicitly avoids these. |
| FR-036 Admin Profile & Settings Management | Outside launch delivery | Acknowledged future requirement; not a launch dependency. |
| Driver assignment / pickup-dispatch travel operations | Out of MVP unless separately approved | Admin travel oversight is monitoring/coordination only. |
