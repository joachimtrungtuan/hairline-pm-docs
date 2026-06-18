# Sprint 2 Readiness & Fix Backlog

---

## Document Control & Sprint Summary

| Field | Value |
|---|---|
| Sprint | Sprint 2 |
| Theme | Config & Aftercare: Quoting Rules, Payment Sub-features & Aftercare Activation |
| Dates | June 1 (Mon) - June 5 (Fri), 2026 · 5 working days |
| Working days | 5 |
| Goal | Complete the configuration layer that pricing and aftercare depend on (commission, deposit, installment, regional rules, aftercare templates); complete the patient payment sub-features (installment, multi-currency display, payment confirmation references, refunds) so they ship close behind the core booking flow; and activate the full aftercare journey across all three tenants (P-05, PR-04, A-03). |
| Definition of Done | All Sprint 2 modules pass QA on staging; no open critical bugs on any Sprint 2 module; cumulative regression on Sprint 1 modules (inquiry → consultation → quote → booking → deposit) passes; all financial flows produce immutable audit log entries (actor, before/after value, timestamp, IP) per FR-029; website brief, sitemap, and content plan complete and signed off by PM (by June 3) and website design & development kicked off (June 4–5); App Store metadata, screenshots, and preview video complete enough for release-candidate submission. |
| Source launch plan | `local-docs/product-plans/2026-05-13/launch-plan.md` |
| Prepared by | Claude AI agent |
| Prepared date | 2026-06-14 |
| Product review date(s) | Not performed in this pass; this report scaffolds the Sprint 2 scope and readiness backlog from the launch plan. |
| Product environment(s) checked | No staging, production, local build, or app build was checked in this pass. |
| Review scope boundary | Source review only. Scope, DoD, modules, stories, deferrals, and readiness gaps are derived from the Sprint 2 section of the launch plan. Product defects must be added after real staging/product review with evidence links. |

<!--
AI agent guidance: Keep this guidance hidden from Markdown preview. It exists only to preserve the intended workflow for future agents editing this report.

## How To Use This Template

- Section 1 mirrors the launch plan. Do not add new scope, reinterpret the sprint, or silently move work between sprints.
- Section 2 is the working fix backlog. Capture issues found from real product review in enough detail that the dev team can reproduce and fix them quickly. Rows marked as evidence gaps are not confirmed product bugs; they are required product-review checks that must be backed by staging evidence before Sprint 2 can be treated as complete.
- Section 3 is for findings that should not distract the current sprint. Use it to prevent out-of-scope issues from being treated as sprint commitments.
- Do not include Plane ticket IDs, assignees, estimates, or ownership fields. Those belong to the later Plane-ticket creation workflow.

### Priority Scale

| Priority | Meaning |
|---|---|
| P0 | Blocks sprint completion, staging validation, or a core end-to-end journey. |
| P1 | Major required feature gap or broken required flow for this sprint. |
| P2 | Required but contained issue that does not block the whole sprint. |
| P3 | Minor UX, copy, polish, or cleanup issue that should not block sprint completion. |

-->

# 1. Sprint Scope From Launch Plan

## 1.1 Modules In Scope

| Surface | Module | FR / Scope Notes | Launch Plan Reference |
|---|---|---|---|
| Patient Mobile | P-03b Payment Sub-features | FR-007 Payment Processing sub-features only (refund flow, multi-currency display, patient-facing payment confirmation/status); FR-007b Payment Installments. | Sprint 2 Modules |
| Patient Mobile | P-04 Travel & Logistics (patient-side) | FR-008 patient-side travel only — Path A passport capture for provider-included, Path B self-booked submission. Admin-side travel mgmt deferred to Sprint 4. | Sprint 2 Modules |
| Patient Mobile | P-05 Aftercare & Progress Monitoring (patient-side) | FR-011 patient-side: plan view, progress check-ins, follow-up, status tracking, standalone aftercare purchase. | Sprint 2 Modules |
| Provider Web | PR-04 Booking Detail Travel Coordination | FR-008 provider-side Path A/Path B workflows embedded in confirmed booking detail. | Sprint 2 Modules |
| Provider Web | PR-04 Aftercare Participation | FR-011 provider-side: template selection, milestone & medication customisation, case monitoring, participation confirmation, follow-up submission. | Sprint 2 Modules |
| Admin Web | A-03 Aftercare Team Management | FR-011 admin-side case mgmt: staff assignment, case override, team configuration. | Sprint 2 Modules |
| Admin Web | A-09b Aftercare Template Configuration | FR-011 admin template authority: admin-managed template catalog, milestone structure, pricing, activation/deactivation. | Sprint 2 Modules |
| Admin Web | A-09c System Settings & Payment Rules — Part 1 | FR-029 Payment System Configuration; FR-028 Regional Config & Pricing (commission rates, deposit rules, installment plan rules, regional groupings, destination pricing, Stripe accounts, currency conversion). | Sprint 2 Modules |
| Shared Service | S-04 Travel API Gateway | FR-008 shared travel integration layer. | Sprint 2 Modules |

## 1.2 User Stories In Scope

### Patient

- As a patient, I want to enrol in an installment plan at checkout, with the schedule and per-installment amount shown clearly, so that I can commit without paying the full amount upfront.
- As a patient, I want scheduled installments auto-charged with retries during a grace period if a charge fails, and to see each failure/retry/expiry state reflected in the product (full push/email/in-app delivery completed in Sprint 3), so that I can update my payment method before the booking is at risk.
- As a patient, I want to clear my final balance before treatment check-in, so that my provider can start treatment without unresolved billing risk.
- As a patient, I want the payment screen to display prices in my local currency with the FX rate and timestamp visible, so that I understand exactly what I am paying and at what rate.
- As a patient, I want an itemised receipt by email and a matching payment confirmation reference in-app, so that I have a record without a full in-app invoice archive at launch.
- As a patient, I want to submit a refund request, see the applicable refund tier (full / partial / non-refundable), and track the admin decision, so that I have transparent recourse if I cancel.
- As a patient on a provider-included travel package, I want to upload passport details from the app, so that the clinic can arrange flights and hotel records.
- As a patient self-booking travel, I want to submit my booked flight numbers, dates, and accommodation details, so that the provider can coordinate arrival with my treatment schedule.
- As a patient, I want a travel status tracker (Submitted → Acknowledged → Confirmed) with timestamps, so that I know where my travel stands without chasing anyone.
- As a patient post-treatment, I want to view my aftercare plan with milestones, medication schedule, and care-team contacts, so that I always know what to do next.
- As a patient, I want to submit progress check-ins (photos, symptom notes, milestone responses), so that my care team can monitor recovery and intervene early.
- As a patient with no prior treatment, I want to purchase a standalone aftercare plan and have it activated once an admin assigns me a provider.
- As a patient, I want reminders for overdue milestones and missed medications, and to know when my care team has been escalated.

### Provider

- As a provider, I want to review passport details for provider-included travel, enter confirmed flight/hotel records, and acknowledge self-booked travel details, so that travel status stays synchronized before the patient arrives.
- As a provider, I want to set up an aftercare plan immediately after marking treatment complete — selecting a template, customising milestones and medications, and adding patient-specific instructions — so that the patient has a structured recovery programme from day one.
- As a provider, I want to monitor my assigned aftercare cases, review patient progress, and submit follow-up notes and participation confirmations.

### Admin

- As an admin, I want to assign and reassign aftercare team members (lead, nurse, coordinator) to cases with a logged reason, so that each patient has an accountable care team and reassignments are auditable.
- As an admin, I want to create, version, price, and activate/deactivate aftercare templates (including standalone-sellable templates), so that aftercare quality is standardised and commercially controllable.
- As an admin, I want to keep reusable aftercare templates under admin authority while allowing providers to customise a selected template per case.
- As an admin, I want to configure platform-wide commission rates and per-provider overrides with audit trail.
- As an admin, I want to configure deposit percentages and installment plan rules (2–9 installments, cutoff days, grace period 0–14 days, FR-007b fixed retry behavior).
- As an admin, I want to enter Stripe API keys and webhook secrets per region with a pre-save API test, so that I cannot save broken payment credentials.
- As an admin, I want to configure currency pairs and FX sync cadence (with manual override + reason logging).
- As an admin, I want to configure regional groupings, destination display ordering, and per-region destination pricing tiers.

### Shared Services / Platform Foundations

- As a patient and provider, I want travel submissions and provider confirmations to move through one shared travel record with clear status changes, without external travel API dependency at launch.
- As an admin, I want all travel submissions logged with a correlation ID across tenants, so that I can trace any travel issue from patient submission to provider acknowledgement.

### Affiliate / Partner

- No affiliate or partner module is assigned to Sprint 2.

## 1.3 Explicitly Deferred / Out Of Scope

| Item | Launch Plan Reason / Destination | Notes |
|---|---|---|
| Admin-side travel management / oversight | Deferred to Sprint 4 (A-04) | Sprint 2 covers patient-side and provider-side travel only. |
| Full push/email/in-app notification delivery verification | Deferred to Sprint 3 under S-03 | Sprint 2 generates grace-period and aftercare activation events; delivery-channel verification is later. |
| Provider-submitted reusable aftercare template variants | Deferred until separately specified | Admin remains sole authority for reusable templates in launch scope; providers customise admin templates per case. |
| Full in-app invoice/receipt history archive | Outside launch scope per FR-017 backlog | Sprint 2 delivers receipt email + in-app payment status/reference only. |
| External travel-provider API integration | Out of launch scope | S-04 provides MVP storage and event-dispatch only; no external travel API for launch. |
| A-09c Part 2 (notifications, team & roles) | Deferred to Sprint 3 | Only A-09c Part 1 (payment/regional rules) is Sprint 2 scope. |
| A-09c Part 3 (i18n & compliance) | Deferred to Sprint 4 | Only A-09c Part 1 is Sprint 2 scope. |

---

# 2. Sprint Fix Backlog

## 2.1 Sprint-Level Blockers

| Bug ID | Priority | Area | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Sprint QA evidence | Sprint 2 cannot be closed from this report alone because no staging QA evidence is attached for all Sprint 2 modules. | 1. Open this report.<br>2. Review Document Control and module sections.<br>3. Check for staging/build evidence links. | No product environment was checked in this pass. | Each Sprint 2 module has staging QA evidence and clear pass/fail status. | TBD | Review pending | Readiness blocker, not a confirmed product defect. |
|  | P0 | Cumulative regression (Sprint 1) | Cumulative regression over the Sprint 1 core journey (inquiry → consultation → quote → booking → deposit) is still required and not yet evidenced. | 1. Re-run the Sprint 1 core journey on staging.<br>2. Capture pass/fail evidence for each stage. | No regression evidence is attached in this report. | Sprint 1 core journey still passes alongside Sprint 2 additions. | TBD | Review pending | Direct Sprint 2 DoD gate. |
|  | P1 | Financial audit logging | All financial flows must produce immutable audit log entries (actor, before/after value, timestamp, IP) per FR-029; this is not yet verified. | 1. Execute commission/deposit/installment/refund changes on staging.<br>2. Inspect audit log entries for required fields. | Audit completeness was not checked in this pass. | Every financial mutation writes an immutable audit entry with all required fields. | TBD | Review pending | FR-029 audit requirement; cross-cuts payment modules. |
|  | P1 | A-09c Part 1 dependency risk | Payment/regional configuration (A-09c Part 1) gates correct behavior of P-03b installments, deposit display, multi-currency, and destination pricing; readiness not yet evidenced. | 1. Review A-09c Part 1 staging screens/API.<br>2. Configure deposit, installment, Stripe, FX, and regional rules.<br>3. Validate downstream P-03b consumption. | No A-09c Part 1 product evidence is attached. | Config layer is ready enough that payment sub-features and pricing consume it correctly. | TBD | Review pending | Config-before-feature dependency; high risk if config slips. |
|  | P1 | Website & App Store milestones | Sprint 2 non-dev milestones (website brief/sitemap/content sign-off by June 3, design/dev kickoff June 4–5; App Store metadata/screenshots/preview video) are not yet evidenced. | 1. Confirm website brief/sitemap/content sign-off.<br>2. Confirm App Store metadata, screenshots, and preview video status. | Milestone status was not checked in this pass. | Website and App Store deliverables meet the launch-plan Sprint 2 deadlines. | TBD | Review pending | Non-dev Sprint 2 milestones in the launch plan. |

## 2.2 Module Fix Backlog

## P-03b - Payment Sub-features

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of installment enrollment, auto-charge/retry/grace, final-balance path, multi-currency display, receipt/confirmation, and refund request flow.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Installments & final balance | Evidence gap: installment enrollment, auto-charge/retry/grace, and final-balance-before-check-in have not been verified in staging for this report. | Enrol in an installment plan against A-09c rules, trigger a failed charge and retry/grace, then clear the final balance and confirm check-in unblocks. | Not reviewed in this pass. | Installment flow, retry/grace model, and final-balance gating work end-to-end per FR-007b. | TBD | Review pending | Add confirmed defects here after product review. |
|  | P1 | Multi-currency, receipt & refund | Evidence gap: multi-currency display, payment confirmation/receipt, and refund request flow have not been verified in staging. | Open payment screen in a non-base currency (check FX rate + timestamp), confirm email receipt + in-app reference, then submit a refund request and track tier/decision. | Not reviewed in this pass. | Local-currency display, receipt/confirmation, and tier-based refund flow work per FR-007. | TBD | Review pending | Full in-app invoice archive is out of launch scope. |

## P-04 - Travel & Logistics (patient-side)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of Path A passport capture, Path B self-booked submission, status tracker, and edge cases.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Patient travel submission | Evidence gap: patient-side Path A/Path B travel submission and status tracking have not been verified in staging. | Submit passport details (Path A) and self-booked flight/hotel details (Path B); confirm status tracker (Submitted → Acknowledged → Confirmed) and edge-case handling. | Not reviewed in this pass. | Both travel paths submit correctly, store with correlation ID, and surface accurate status with edge-case warnings. | TBD | Review pending | Admin-side travel oversight is Sprint 4 (A-04). |

## P-05 - Aftercare & Progress Monitoring (patient-side)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of plan view, check-ins, follow-up, standalone purchase, escalation, and status board.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Patient aftercare journey | Evidence gap: patient aftercare plan view, check-ins, standalone purchase, and 48-hour escalation have not been verified in staging. | View active aftercare plan, submit a milestone check-in, purchase a standalone aftercare plan via Stripe, and trigger the 48-hour escalation rule. | Not reviewed in this pass. | Plan view, check-ins, standalone purchase activation, escalation flag, and status board all work per FR-011. | TBD | Review pending | Full delivery-channel verification of escalation events is Sprint 3 (S-03). |

## PR-04 - Booking Detail Travel Coordination (provider-side)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of provider travel status indicators, passport review, confirmed record entry, and self-booked acknowledgement from confirmed booking detail.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Provider travel coordination | Evidence gap: provider-side travel coordination from booking detail has not been verified in staging. | From a confirmed booking detail, view travel status indicators, review submitted passport details, enter confirmed flight/hotel records, and acknowledge a self-booked travel record. | Not reviewed in this pass. | Provider travel actions update the patient tracker and are visible to admin with correlation ID. | TBD | Review pending | Tightly coupled to P-04 and S-04. |

## PR-04 - Aftercare Participation (provider-side)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of post-treatment aftercare setup (Screen 10), template selection/customisation, medication prescription, case monitoring, and follow-up submission.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Provider aftercare setup & monitoring | Evidence gap: provider aftercare plan setup, customisation, and case monitoring have not been verified in staging. | Mark a treatment complete, configure an aftercare plan from an admin template, customise milestones/medications/instructions, activate, then monitor the case and submit a follow-up. | Not reviewed in this pass. | Plan setup, activation events, case monitoring, and follow-up submission work per FR-011. | TBD | Review pending | Provider-submitted reusable template variants are deferred. |

## A-03 - Aftercare Team Management

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of staff assignment/reassignment, case override with reason, and team configuration.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Aftercare team management | Evidence gap: aftercare staff assignment, case override, and team configuration have not been verified in staging. | Assign aftercare staff to a case, reassign with a logged reason, and configure team roles/on-call/capacity. | Not reviewed in this pass. | Assignment, override-with-reason, and team configuration work with audit trail per FR-011. | TBD | Review pending | Add confirmed defects here after product review. |

## A-09b - Aftercare Template Configuration

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of template CRUD/versioning, independent pricing, treatment-type tagging, and deactivation behavior on active cases.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Aftercare template authority | Evidence gap: aftercare template create/edit/version/activate/price has not been verified in staging. | Create, edit, version, and activate/deactivate an aftercare template; price it for standalone purchase; confirm deactivated templates stay on active cases but cannot be selected for new ones. | Not reviewed in this pass. | Template authority, pricing, tagging, and deactivation semantics work per FR-011. | TBD | Review pending | Feeds P-05 standalone purchase and PR-04 provider setup. |

## A-09c - System Settings & Payment Rules (Part 1)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of commission rates/overrides, deposit rate, installment rules, Stripe config with pre-save test, currency-pair sequencing, FX sync, regional groupings, and destination pricing.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Payment & regional configuration | Evidence gap: A-09c Part 1 payment and regional configuration has not been verified in staging. | Configure global/per-provider commission, deposit rate (20–30%), installment rules (2–9, cutoff, grace 0–14), Stripe keys with pre-save API test, currency pairs in dependency order, FX cadence, regional groupings, and destination pricing. | Not reviewed in this pass. | All config controls save with audit trail and are correctly consumed by patient payment and pricing surfaces. | TBD | Review pending | Gating dependency for P-03b and FR-028/FR-029 behavior. |

## S-04 - Travel API Gateway

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of travel data routing, MVP storage/event-dispatch, and correlation-ID logging.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Shared travel gateway | Evidence gap: travel gateway routing and correlation-ID logging have not been verified in staging. | Submit patient-side and provider-side travel data and confirm both flow through one shared travel record with correlation IDs and event dispatch. | Not reviewed in this pass. | Gateway routes both sides into one record with correlation IDs; no external travel API required for launch. | TBD | Review pending | Underpins P-04 and PR-04 travel coordination. |

---

# 3. Not For This Sprint

| Item | Why It Is Not In This Sprint | Follow-Up Notes |
|---|---|---|
| Admin travel oversight (A-04) | Deferred to Sprint 4 | Patient/provider travel surfaces ship in Sprint 2; admin embedded oversight follows. |
| Full notification delivery verification (push/email/in-app) | Deferred to Sprint 3 (S-03) | Sprint 2 generates the events; delivery-channel verification is later. |
| A-09c Part 2 (notifications, team & roles) and Part 3 (i18n & compliance) | Sprint 3 and Sprint 4 respectively | Only A-09c Part 1 belongs to Sprint 2. |
| Provider-submitted reusable aftercare template variants | Deferred until separately specified | Out of launch scope unless approved. |
| Full in-app invoice/receipt history archive | Out of launch scope per FR-017 backlog | Receipt email + in-app status/reference only at launch. |
| External travel-provider API integration | Out of launch scope | S-04 is MVP storage/event-dispatch only. |
