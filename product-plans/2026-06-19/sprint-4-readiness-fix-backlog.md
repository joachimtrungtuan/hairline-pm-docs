# Sprint 4 Readiness & Fix Backlog

---

## Document Control & Sprint Summary

| Field | Value |
|---|---|
| Sprint | Sprint 4 |
| Theme | Wrap-Up: Financial, Analytics & Non-Critical |
| Dates | June 15 (Mon) - June 19 (Fri), 2026 · 5 working days |
| Working days | 5 |
| Goal | Complete all financial processing and analytics modules; complete client UAT; run final integration regression (Sprint 3 + Sprint 4 modules + cross-tenant flows — Sprint 1+2 regression already completed in Sprint 3); submit final App Store builds; bring website to staging; verify production environment. |
| Definition of Done | All Sprint 4 modules pass QA on staging; final integration regression completed across Sprint 3 + Sprint 4 modules and cross-tenant flows with no open critical bugs; client UAT completed and sign-off received; website finalized, QA passed, and deployed to staging; release-candidate App Store builds submitted to Apple and Google on June 16 with no app-store-affecting mobile code merged afterward unless public release is explicitly deferred; production Stripe configured and verified (carry-forward from Sprint 3); production environment fully provisioned and validated by DevOps. |
| Source launch plan | `local-docs/product-plans/2026-05-13/launch-plan.md` |
| Prepared by | Claude AI agent |
| Prepared date | 2026-06-14 |
| Product review date(s) | Not performed in this pass; this report scaffolds the Sprint 4 scope and readiness backlog from the launch plan. |
| Product environment(s) checked | No staging, production, local build, or app build was checked in this pass. |
| Review scope boundary | Source review only. Scope, DoD, modules, stories, deferrals, and readiness gaps are derived from the Sprint 4 section of the launch plan. Product defects must be added after real staging/product review with evidence links. |

<!--
AI agent guidance: Keep this guidance hidden from Markdown preview. It exists only to preserve the intended workflow for future agents editing this report.

## How To Use This Template

- Section 1 mirrors the launch plan. Do not add new scope, reinterpret the sprint, or silently move work between sprints.
- Section 2 is the working fix backlog. Capture issues found from real product review in enough detail that the dev team can reproduce and fix them quickly. Rows marked as evidence gaps are not confirmed product bugs; they are required product-review checks that must be backed by staging evidence before Sprint 4 can be treated as complete.
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
| Provider Web | PR-05 Financial Management & Reporting | FR-014 provider-side; FR-017 provider earnings/payout visibility (cockpit, conversion, patient analytics, finance & payouts, pricing benchmarks, export). | Sprint 4 Modules |
| Provider Web | PR-06 Provider i18n & Compliance Visibility (added Sprint 4) | FR-021 provider runtime switch; FR-023 provider-side compliance/audit visibility. | Sprint 4 Modules |
| Admin Web | A-04 Travel Oversight | FR-008 admin-side embedded workflows only (monitoring in booking/inquiry detail, exception handling, coordination notes). | Sprint 4 Modules |
| Admin Web | A-05 Billing & Financial Reconciliation | FR-017 (patient billing, approved-statement provider payouts, affiliate billing, discount reconciliation, financial reporting, currency alerts). | Sprint 4 Modules |
| Admin Web | A-07 Affiliate Program Management | FR-018 (affiliate CRUD, commission tracking, discount-code assignment, monthly payout on 7th, £50 threshold + roll-over). | Sprint 4 Modules |
| Affiliate / Partner | AF-01 Affiliate Dashboard | FR-018 affiliate-facing launch surface (read-only earnings, attribution, payout status). | Sprint 4 Modules |
| Admin Web | A-08 Analytics & Reporting | FR-014 admin-side (platform overview, provider performance, acquisition funnel, geographic intelligence, treatment outcomes, financial health, pricing intelligence, with anonymization). | Sprint 4 Modules |
| Admin Web | A-09c System Settings & Payment Rules — Part 3 (i18n & compliance, added Sprint 4) | FR-021 admin runtime + authoring; FR-023 (supported locales, translation registry, JSON import/export, publish/version/rollback, coverage; retention policies; GDPR DSR workflow; compliance exports). | Sprint 4 Modules |
| Admin Web | A-01 Patient i18n + Compliance Surfaces (added Sprint 4) | FR-021, FR-023 (patient language preference visibility, DSR request handling). | Sprint 4 Modules |
| Cross-cutting (all tenants) | Search & Filtering Capability (added Sprint 4) | FR-022 P1 MVP scope across provider, admin, and patient list surfaces; patient provider-discovery is P2 post-MVP. | Sprint 4 Modules |
| Shared Service | S-02 / S-03 Localization Support | FR-021 shared dependencies (localized currency/timezone display, notification-template fallback and locale routing). | Sprint 4 Modules |
| Shared Service | S-06 Audit Log Service | FR-023 audit log layer; FR-031 admin-action logging (immutable capture, retention enforcement, admin retrieval/export). | Sprint 4 Modules |

## 1.2 User Stories In Scope

### Patient

- As a patient, I want my language preference and DSR (deletion/erasure) request handling to be visible and actionable from the admin side (A-01), so that my compliance requests are processed in context. *(Patient-facing language/DSR surfaces shipped in Sprint 3 under P-01.)*

### Provider

- As a provider, I want a main cockpit showing revenue, pending payouts, and completed treatments, so that I have a one-glance financial view.
- As a provider, I want my inquiry → consultation → booking → completion funnel with per-stage drop-off.
- As a provider, I want anonymised patient analytics (acquisition source, demographics, treatment-type mix).
- As a provider, I want my payout schedule with the 3-day buffer applied and full payout history with fee/commission breakdown.
- As a provider, I want pricing benchmarks versus regional peers (aggregated).
- As a provider, I want to export reports (CSV/PDF) for any date range, with scheduled exports available for 7-day re-download.
- As a provider, I want a dashboard language selector that persists across sessions, and read-only privacy/retention/compliance visibility.

### Admin

- As an admin, I want travel information visible from booking/inquiry detail plus an exception-focused list, without a standalone travel dashboard.
- As an admin, I want to review provider-entered and patient-submitted travel records, resolve exceptions, and leave coordination notes with audit trail.
- As an admin, I want a full ledger of patient charges, refunds, and installments.
- As an admin, I want payout statements generated before payout day, approved during the 3-day buffer, then processed automatically only when approved.
- As an admin, I want discount applications reconciled against A-06 records and FX-rate alerts.
- As an admin, I want to create/edit/suspend affiliate partners with payout/tax details, automatic commission calculation on completion, monthly payout on the 7th (£50 threshold + roll-over), and discount-code attribution.
- As an admin, I want a platform overview dashboard, acquisition funnel, geographic/pricing intelligence, and financial health views on real data.
- As an admin, I want to switch my own dashboard language; manage a translation registry with per-key editing, JSON import/export, and versioned publish/rollback; and see a coverage report flagging missing keys before publish.
- As an admin or compliance officer, I want to configure retention policies per category (7-year for medical/financial), run a GDPR DSR workflow with SLA timer and legal retention overrides, and produce DSR notifications and tamper-evident compliance exports.
- As an admin, I want to see a patient's language preference/locale activity and action DSR tickets from their A-01 record with reason and legal-basis tag.

### Shared Services / Platform Foundations

- As any user, I want prices, dates, times, and notifications to follow my selected locale with safe fallback to the default locale when translation data is missing.
- As an admin or compliance officer, I want all significant actions recorded in a tamper-evident, append-only audit log with category-based retention, and retrievable/exportable filtered by actor/action/entity/date range.

### Affiliate / Partner

- As an affiliate or partner, I want read-only access to my assigned codes, attributed bookings, commissions, and payout status, so that I can verify performance without manual reports.

### Cross-cutting

- As a provider or admin, I want consistent search and filter behaviour on all major list views (with shareable filter state).
- As a patient, I want to filter quote comparison results, search help articles, and filter my support tickets.

## 1.3 Explicitly Deferred / Out Of Scope

| Item | Launch Plan Reason / Destination | Notes |
|---|---|---|
| FR-036 Admin Profile & Settings Management | Acknowledged outside launch delivery | No composed implementation PRD; Sprint 4 does not carry FR-036 scope. Admin profile/security uses existing shared admin-auth/settings stack. |
| Patient provider-discovery search | Deferred — P2 post-MVP | Search & Filtering P1 MVP excludes patient provider discovery. |
| Driver assignment / pickup-dispatch travel operations | Out of MVP unless separately approved | A-04 covers monitoring, exception handling, and coordination notes only. |
| Patient data export beyond DSR scope | Out of launch scope | DSR deletion/erasure workflow ships; broad patient data export is not promised. |
| App-store-affecting mobile code after June 16 RC freeze | Frozen after RC submission | Post-freeze Sprint 4 work must be web/backend/admin/provider-side only unless public release is deferred. |

---

# 2. Sprint Fix Backlog

## 2.1 Sprint-Level Blockers

| Bug ID | Priority | Area | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Sprint QA evidence | Sprint 4 cannot be closed from this report alone because no staging QA evidence is attached for all Sprint 4 modules. | 1. Open this report.<br>2. Review Document Control and module sections.<br>3. Check for staging/build evidence links. | No product environment was checked in this pass. | Each Sprint 4 module has staging QA evidence and clear pass/fail status. | TBD | Review pending | Readiness blocker, not a confirmed product defect. |
|  | P0 | Final integration regression | Final integration regression across Sprint 3 + Sprint 4 modules and cross-tenant flows must pass with no open critical bugs; not yet evidenced. | 1. Run the final integration regression suite on staging.<br>2. Capture pass/fail evidence for each cross-tenant flow. | No final regression evidence is attached in this report. | Final regression is green across Sprint 3 + Sprint 4 + cross-tenant journeys. | TBD | Review pending | Direct Sprint 4 DoD gate; gates the launch decision. |
|  | P0 | Client UAT sign-off | Client UAT must be completed and sign-off received; not yet evidenced. | 1. Run client UAT (June 17–18).<br>2. Capture sign-off record. | UAT status was not checked in this pass. | Client UAT completed with recorded sign-off. | TBD | Review pending | Non-dev Sprint 4 milestone (sign-off June 18). |
|  | P0 | Production readiness | Production environment must be fully provisioned and validated, and production Stripe verified (carry-forward from Sprint 3); not yet evidenced. | 1. Validate production provisioning with DevOps.<br>2. Confirm production Stripe verification.<br>3. Run pre-launch staging smoke test. | Production readiness was not checked in this pass. | Production fully provisioned/validated; Stripe verified; pre-launch smoke passes. | TBD | Review pending | Required before June 22 go-live. |
|  | P1 | RC App Store submission & website staging | RC App Store builds (June 16, mobile binary frozen after) and website finalized/QA/deployed to staging are not yet evidenced. | 1. Confirm RC submission to Apple + Google on June 16.<br>2. Confirm no post-freeze app-store-affecting code.<br>3. Confirm website deployed to staging + DNS pre-check. | Submission and website status were not checked in this pass. | RC builds submitted; mobile binary frozen; website on staging with DNS pre-check complete. | TBD | Review pending | Non-dev Sprint 4 milestones (June 16/18). |

## 2.2 Module Fix Backlog

## PR-05 - Financial Management & Reporting

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of cockpit, conversion funnel, patient analytics, finance/payouts, pricing benchmarks, and export/scheduled-export behavior.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Provider financial reporting | Evidence gap: PR-05 cockpit, analytics, payouts, and exports have not been verified in staging. | Open the cockpit, conversion funnel, and anonymised patient analytics; review payout schedule (3-day buffer) and history; check pricing benchmarks; export CSV/PDF and confirm scheduled-export 7-day re-download. | Not reviewed in this pass. | All PR-05 surfaces show correct live data with anonymization and working exports per FR-014/FR-017. | TBD | Review pending | A-05b provider payouts flagged as high-risk (20% at sprint start). |

## PR-06 - Provider i18n & Compliance Visibility

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of dashboard language selector persistence, runtime bundle fetch + fallback, and read-only compliance/audit visibility.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Provider i18n & compliance | Evidence gap: provider language selector and compliance visibility have not been verified in staging. | Switch dashboard language and confirm persistence + runtime re-render with fallback; view privacy/retention content and read-only audit/retention visibility. | Not reviewed in this pass. | Language switch and read-only compliance visibility work per FR-021/FR-023 without granting admin compliance privileges. | TBD | Review pending | Added to Sprint 4 scope. |

## A-04 - Travel Oversight (admin-side)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of embedded travel monitoring, exception list, coordination notes, status summary, and correlation-ID audit.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Admin travel oversight | Evidence gap: admin embedded travel oversight has not been verified in staging. | From booking/inquiry detail, review provider-entered and patient-submitted travel records, resolve an exception with reason, add coordination notes, and confirm correlation-ID audit linking to S-04. | Not reviewed in this pass. | Embedded oversight, exception handling, status summary, and audit work per FR-008 admin-side. | TBD | Review pending | No standalone travel dashboard; dispatch ops out of MVP. |

## A-05 - Billing & Financial Reconciliation

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of patient billing ledger, provider payout buffer/cron, affiliate billing, discount reconciliation, financial reporting, and currency alerts on live data.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Billing & reconciliation | Evidence gap: A-05 billing, payout buffer/cron, and reconciliation have not been verified in staging. | Inspect patient ledger; generate pending payout statements; approve within the 3-day buffer; run payout-day cron on approved statements only; reconcile discounts vs A-06; check FX-rate alerts and financial reporting. | Not reviewed in this pass. | All A-05 surfaces operate on live data with correct buffer/approval/cron behavior per FR-017. | TBD | Review pending | A-05b provider payouts flagged high-risk in the launch plan. |

## A-07 - Affiliate Program Management

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of affiliate CRUD, commission tracking, discount-code assignment, and monthly payout rules.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Affiliate program management | Evidence gap: affiliate CRUD, commission, and payout rules have not been verified in staging. | Create/edit/suspend an affiliate, link A-06 discount codes, complete a booking to trigger commission, and confirm monthly-on-7th payout with £50 threshold + roll-over. | Not reviewed in this pass. | Affiliate CRUD, attribution, commission, and payout rules work per FR-018. | TBD | Review pending | Feeds AF-01 dashboard and A-05c affiliate billing. |

## AF-01 - Affiliate Dashboard

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of affiliate login/access and read-only attribution/commission/payout visibility.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Affiliate dashboard | Evidence gap: affiliate-facing dashboard has not been verified in staging. | Log in as an affiliate and confirm read-only visibility of assigned codes, attributed bookings, commission earned, payout status, and history. | Not reviewed in this pass. | Affiliate dashboard shows correct read-only data per FR-018; admin retains CRUD/payout authority. | TBD | Review pending | First affiliate/partner-facing surface in the launch. |

## A-08 - Analytics & Reporting

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of platform overview, provider performance, acquisition funnel, geographic/pricing intelligence, treatment outcomes, and financial health on real data.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Admin analytics | Evidence gap: A-08 analytics dashboards have not been verified in staging. | Open platform overview, provider performance (with anonymization), acquisition funnel, geographic/pricing intelligence, treatment outcomes, and financial health; confirm all are on real data. | Not reviewed in this pass. | All A-08 screens show correct real data with anonymization per FR-014; no mocks. | TBD | Review pending | Add confirmed defects here after product review. |

## A-09c - System Settings & Payment Rules (Part 3 — i18n & Compliance)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of admin runtime language, translation registry/import-export/publish/rollback, coverage report, retention policies, GDPR DSR workflow, and compliance exports.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | i18n authoring & compliance | Evidence gap: A-09c Part 3 i18n authoring and compliance workflows have not been verified in staging. | Switch admin language; edit translation keys; JSON import/export; publish with versioned rollback; review coverage/missing-key alerts; configure retention (7-year medical/financial); run a GDPR DSR with SLA timer + retention override; generate a tamper-evident compliance export. | Not reviewed in this pass. | i18n authoring, retention, DSR workflow, and compliance exports work per FR-021/FR-023. | TBD | Review pending | Patient data export beyond DSR is out of scope. |

## A-01 - Patient i18n + Compliance Surfaces

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of patient locale visibility, DSR ticket actioning from A-01, status/outcome history, and audit logging.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Patient DSR actioning | Evidence gap: admin-side patient i18n/DSR handling has not been verified in staging. | From a patient A-01 record, view language preference/locale activity, action a DSR ticket (erasure approved/denied, retention override), and confirm status history + audit with reason and legal-basis tag. | Not reviewed in this pass. | Patient locale visibility and DSR actioning work per FR-021/FR-023 with full audit. | TBD | Review pending | Completes the DSR loop opened by P-01 in Sprint 3. |

## Cross-cutting - Search & Filtering (FR-022)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of P1 MVP search/filter across provider, admin, and patient list surfaces; persistence and shareable filter state.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Search & filtering | Evidence gap: FR-022 P1 search/filter surfaces have not been verified in staging. | Exercise search/filter on provider (PR-01/02/03/04/05/06) and admin (A-01/02/03/05/06/07/09/10) list views, plus patient quote-comparison/help/ticket filters; confirm chips persist across pagination/session and URL-shareable state. | Not reviewed in this pass. | All P1 MVP search/filter surfaces work with persistence per FR-022; patient provider-discovery remains P2. | TBD | Review pending | Patient provider-discovery search is explicitly P2 post-MVP. |

## S-02 / S-03 - Localization Support

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of localized currency display, timezone-aware date/time, and notification-template locale routing/fallback.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Localization support | Evidence gap: shared localization support has not been verified in staging. | Confirm localized currency display with rate/timestamp, timezone-aware date/time across tenants, and notification-template language routing with fallback to default locale. | Not reviewed in this pass. | Currency, timezone, and notification locale routing/fallback work per FR-021 shared dependencies. | TBD | Review pending | Notification delivery rules already delivered in Sprint 3. |

## S-06 - Audit Log Service

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of immutable capture, retention enforcement, admin retrieval/export, and append-only guarantees.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Audit log service | Evidence gap: immutable audit capture, retention, and export have not been verified in staging. | Trigger admin/financial/DSR/aftercare/moderation/role actions; confirm immutable append-only capture, category retention (7-year medical/financial), and a tamper-evident filtered export (hash + timestamp). | Not reviewed in this pass. | Audit capture, retention, and tamper-evident export work per FR-023/FR-031 with no UPDATE/DELETE from app layer. | TBD | Review pending | Underpins compliance gates across the launch. |

---

# 3. Not For This Sprint

| Item | Why It Is Not In This Sprint | Follow-Up Notes |
|---|---|---|
| FR-036 Admin Profile & Settings Management | Acknowledged outside launch delivery | No composed implementation PRD; uses existing shared admin-auth/settings stack until FR-036 is composed. |
| Patient provider-discovery search | Deferred — P2 post-MVP | FR-022 P1 MVP excludes it. |
| Driver assignment / pickup-dispatch travel operations | Out of MVP unless separately approved | A-04 covers monitoring, exceptions, and coordination notes only. |
| Patient data export beyond DSR scope | Out of launch scope | DSR deletion/erasure ships; broad patient data export is not promised. |
| App-store-affecting mobile code after the June 16 RC freeze | Frozen after RC submission | Post-freeze work must be web/backend/admin/provider-side unless public release is deferred. |
