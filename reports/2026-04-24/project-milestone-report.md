# Hairline Project - Comprehensive Milestone Report

**Report Date:** April 24, 2026  
**Report Period:** Project inception to April 24, 2026  
**Prepared By:** Project Team  
**Project Phase:** MVP Development

---

## Introduction

This milestone report provides a current business-facing status overview of the Hairline platform as of April 24, 2026. It uses the structure of the January 27, 2026 milestone report, but it does not compare against that report or reuse its status claims as current evidence.

This pass focuses on the Provider Dashboard and Admin Dashboard. The Mobile App section is retained as a structural placeholder for a later review because the current verification scope excludes the outdated mobile app folder.

---

## Executive Summary

**Overall Project Health:** 🟡 In Progress - Broad feature surface exists, but PRD compliance gaps remain in workflow enforcement, backend/frontend contracts, auditability, and financial operations.

### Key Metrics

- **Mobile App Completion:** [Deferred - not reviewed in this pass]
- **Provider Dashboard Completion:** 65.9% verified average across PR-01 through PR-07
- **Admin Dashboard Completion:** 46.0% verified average across A-01 through A-10 table rows
- **Overall Platform Completion:** Not calculated in this pass because Mobile App review is deferred

### Current Capabilities Confirmed

- Provider users can manage teams, review inquiries, create detailed quotes, start treatment documentation, manage aftercare cases, view financial dashboards, update settings, and message patients.
- Admin users can manage patients, providers, aftercare cases, travel coordination records, billing views, provider payout views, discounts, affiliates, content/settings, support cases, and communication-monitoring surfaces at least at a partial operational level.
- The most complete provider areas are inquiry review and quote creation; the weakest provider area is financial management because key payout/earnings APIs are missing or mock-backed.
- The strongest verified admin areas are travel coordination within booking context and system/payment settings; the weakest verified admin areas are analytics, provider payouts, affiliate operations, and financial reconciliation because core workflows are missing, mock-backed, or not PRD-aligned.

### Critical Blockers & Risks

- Provider financial management has a blocking FE/BE gap: the Earnings Tracker frontend calls `provider-dashboard/earnings-tracker`, but no matching backend route was found.
- Provider treatment execution is workflow-incomplete: End Treatment is not wired from the frontend, required FR-010 gates are missing, and treatment completion transitions directly into aftercare against the FR boundary.
- Admin billing and payout workflows are mostly UI-present but backend-incomplete; refund, reminder, override, payout approval/retry, Stripe transfer, and payout statement lifecycle are not implemented end to end.
- Several compliance-heavy requirements are partial or missing: server-side RBAC enforcement, medical data access justification/logging, immutable audit trails, encrypted banking/payment details, and GDPR anonymization after deletion approval.

### Immediate Client Decisions Required

- Confirm whether MVP can proceed with partial provider/admin financial operations, or whether FR-017 payout/refund/installment workflows are launch blockers.
- Confirm whether Admin A-04 travel should remain MVP coordination-only or require admin-wide travel dashboard/API configuration in this release.
- Confirm whether provider/admin support surfaces that currently rely on mock/static data must be production-backed before MVP.

---

## High-Level Status Dashboard

| **Metric** | **Value** | **Status** | **Notes** |
| ---------- | --------- | ---------- | --------- |
| **Mobile App: Total Modules** | [Deferred] | - | Mobile section not reviewed in this pass |
| **Mobile App: Modules Completed** | [Deferred] | [Deferred] | Mobile section not reviewed in this pass |
| **Mobile App: Modules In Progress** | [Deferred] | [Deferred] | Mobile section not reviewed in this pass |
| **Mobile App: Modules Not Started** | [Deferred] | [Deferred] | Mobile section not reviewed in this pass |
| **Mobile App: Overall Progress** | [Deferred] | [Deferred] | Mobile section not reviewed in this pass |
| **Provider Dashboard: Total Modules** | 7 | - | Core provider workflow |
| **Provider Dashboard: Modules Completed** | 0 | 🟡 | No provider module is fully PRD-compliant after verification |
| **Provider Dashboard: Modules In Progress** | 7 | 🟡 | All PR-01 through PR-07 have meaningful implementation with material gaps |
| **Provider Dashboard: Modules Not Started** | 0 | 🟢 | No provider module is absent |
| **Provider Dashboard: Overall Progress** | 65.9% | 🟡 | Average of verified module estimates |
| **Admin Dashboard: Total Modules** | 10 | - | Core admin functions |
| **Admin Dashboard: Modules Completed** | 0 | 🟡 | No admin module row is fully PRD-compliant after verification |
| **Admin Dashboard: Modules In Progress** | 14 rows | 🟡 | A-01 through A-10 all have partial implementation, including A-05 and A-09 submodules |
| **Admin Dashboard: Modules Not Started** | 0 | 🟢 | No admin module row is completely absent |
| **Admin Dashboard: Overall Progress** | 46.0% | 🟡 | Average across verified Admin table rows, including A-05 and A-09 submodules |
| **Current Sprint/Phase** | MVP Completion | 🟡 | Provider/Admin feature surface exists, but compliance gaps remain |
| **Estimated Days to MVP** | 146-227 person-days | 🟡 | Provider/Admin estimate only; Mobile App not included |
| **Total Work Remaining** | 146-227 person-days | - | Provider: 46-69, Admin: 100-158 |

**Legend:**  
🟢 Complete / On Track | 🟡 In Progress / At Risk | 🔴 Not Started / Critical Issue

---

# Section 1: Mobile App (Patient Platform)

> **Reference**: Constitution module codes P-01 through P-10 | System PRD sections FR-001 through FR-013

## Module Progress Details

This section is intentionally deferred. The current verification scope excludes `main/hairline-app/` because that folder is outdated.

| **Module / Component** | **Status** | **Completion %** | **What Users Can Do** | **What Users Cannot Yet Do** | **Category** | **Notes** |
| ---------------------- | ---------- | ---------------- | ---------------------- | ----------------------------- | ------------ | -------- |
| **P-01 through P-10: Mobile App Modules** | [Deferred] | [Deferred] | [Deferred until mobile review] | [Deferred until mobile review] | [Deferred] | Mobile app section saved for later |

## Mobile App Summary

[Deferred until mobile review]

---

# Section 2: Provider Dashboard

> **Reference**: Constitution module codes PR-01 through PR-07 | System PRD sections FR-003, FR-004, FR-005, FR-006, FR-009, FR-010, FR-011, FR-012, FR-014, FR-032

## Module Progress Details

| **Module / Component** | **Status** | **Completion %** | **What Users Can Do** | **What Users Cannot Yet Do** | **Category** | **Notes** |
| ---------------------- | ---------- | ---------------- | ---------------------- | ----------------------------- | ------------ | -------- |
| **PR-01: Auth & Team Management** | 🟡 In Progress | 70% | • Provider users can log in and receive tokens<br>• Inactive/not-activated provider users are blocked<br>• Team UI lists members, roles, status, last login, and invitations<br>• Providers can invite staff, resend/cancel invitations, and open member details<br>• Backend supports Owner, Manager, Clinical Staff, and Billing Staff roles<br>• Role changes, suspend/remove flows, workload checks, last-owner protection, and activity logging exist<br>• Provider profile/security basics exist | • Full server-side per-action RBAC enforcement is not proven<br>• Role changes do not invalidate sessions<br>• Invitation acceptance appears inconsistent with provider auth model (`User` vs `ProviderUser`)<br>• Invitation setup UI labels flow as admin setup and redirects to team login<br>• Invitation email bounce/Pending Send state and 10-invites/hour rate limit not evidenced<br>• Main team table does not cleanly expose all suspend/remove/reassign workflows | ⚠️ Critical | Verified against FR-009 and RBAC docs. Substantial implementation, but not complete because authorization enforcement and invitation/account model are core compliance risks. |
| **PR-02a: Inquiry Management & Review** | 🟡 In Progress | 78% | • Provider inquiry list shows patient code/masked identity, age, problem, location, requested date, medical alerts, and view action<br>• Inquiry detail shows patient info, destinations, requested date ranges, problem details, visual evidence, medical questionnaire summary, medical alert level, and simple timeline<br>• Backend scopes provider list to assigned inquiries<br>• Provider detail response anonymizes patient info until confirmed/paid stage<br>• Medical alert calculation and display exist<br>• Quote handoff from inquiry detail to quote creation exists<br>• Search/filter coverage exists for patient ID/name, age, concern, location, alerts, inquiry date, and requested date | • Provider-side search still searches patient first name, last name, and email, conflicting with pre-payment privacy rules<br>• Detail endpoint does not clearly enforce assigned-provider access<br>• “Need clarification via admin” workflow not evidenced<br>• Opening detail does not clearly mark provider assignment as viewed<br>• Timeline is synthetic/minimal rather than full distribution/view/status timeline<br>• Requested-date filtering uses weak serialized string matching<br>• Full medical Q&A and V1 photo-set metadata are partial | ⚠️ Critical | Verified against FR-003, FR-022, and FR-025. Core inquiry review works, but privacy/access-control and workflow gaps remain. |
| **PR-02b: Quote Creation & Submission** | 🟡 In Progress | 78% | • Provider quote creation route and multi-step wizard exist<br>• Quote form covers treatment, package/customization, travel inclusions, graft estimate, visual plan upload, treatment dates, per-date pricing, appointment time, clinician assignment, notes, attachments, and summary submit<br>• Backend validates inquiry, treatment/package, dates, appointment within treatment range, clinicians, discounts, services, grafts, and decimal precision<br>• Backend creates quote records, treatment dates, services, package selections, clinicians, treatment plan entries, visual plan, attachments, workflow timeline, expiry timestamp, and totals<br>• Quote edit/update, audit/version snapshot, price-change notification, and quote list/search/filter exist<br>• Quote acceptance auto-cancels other quotes and sends notifications | • PRD default quote expiry is 48 hours, but backend defaults to 7 days<br>• Expiry command sends reminders/notifications but status transition to `expired` is unclear<br>• Status taxonomy diverges from PRD beyond naming tolerance<br>• Provider withdrawal/archive is not fully implemented; frontend withdraw is placeholder-like<br>• Patient-cancelled inquiry cascade to distinct quote statuses not evidenced<br>• Direct quote-submitted patient notification path is unclear<br>• Quote table privacy/anonymization is partial | ⚠️ Critical | Verified against FR-004. Core quote creation is strong; lifecycle/status compliance is the main gap. |
| **PR-03: Treatment Execution & Documentation** | 🟡 In Progress | 45% | • Provider can move a confirmed quote into `inprogress` via backend action<br>• Provider UI exposes “Start treatment” and In Progress tab<br>• Day-based treatment plan entries exist with editable daily status and notes<br>• Beginning/end treatment notes are modeled and persisted<br>• Initial/final treatment scan upload exists<br>• Notifications exist for treatment start/completion at a basic level | • “Start treatment” does not enforce FR-required Check In gates: date <= today, no outstanding balance, and role authorization<br>• Backend transitions `inprogress` directly to aftercare, while FR-010 should stop at completion signal<br>• End Treatment frontend does not call the mutation; call is commented out<br>• End Treatment does not enforce required fields, actual graft count, final scan, or all-day-terminal gate<br>• Day status mismatch (`need_attention` vs `need_caution`) likely breaks an update path<br>• Cancel/Close Case, treatment media, autosave, reminders, immutable audit, lock-after-check-in, and admin override are incomplete | ⚠️ Critical | Verified against FR-010. Useful treatment documentation pieces exist, but workflow gates and completion flow are not PRD-compliant. |
| **PR-04: Aftercare Participation** | 🟡 In Progress | 72% | • Provider aftercare case list exists and is scoped to provider cases<br>• Backend supports case listing/details, access checks, milestones, medications, instructions, scans, audit logging, and provider actions<br>• Provider can create an aftercare plan through a multi-step wizard<br>• Backend creates aftercare records, milestones, medications, instructions, emergency contacts, scan/questionnaire schedules from templates<br>• Provider can view aftercare details, request additional scans, submit plan-adjustment requests, escalate cases, and use aftercare chat infrastructure | • Search box does not appear to feed API query as required by FR-022<br>• Required milestone/status/date filters are incomplete<br>• Treatment-completion handoff does not clearly prompt template selection and activation<br>• Plan adjustment is mainly a pending request, not full direct edit workflow<br>• Provider-to-aftercare-team communication is mixed with patient conversation evidence<br>• Standalone aftercare provider activation UI not clearly exposed<br>• Strong role permission enforcement not proven beyond provider ownership checks | 📋 Standard | Verified against FR-011 and FR-022. Backend is relatively broad; search/filter, handoff, and role enforcement remain partial. |
| **PR-05: Financial Management & Reporting** | 🟡 In Progress | 35% | • Provider navigation includes Earnings Tracker and Analytics/Finance areas<br>• Financial chart APIs exist for earnings trend, revenue by treatment, quote-payment aging, and payouts history/upcoming<br>• Earnings Tracker UI has booking, patient, treatment, gross amount, commission, net earning, adjustment, currency, treatment status, payout status, filters, pagination, and CSV concepts<br>• Basic payout amount calculation exists from paid payments/completed quotes | • Frontend calls `provider-dashboard/earnings-tracker`, but no matching backend route/controller method was found<br>• Earnings Tracker defaults to mock data unless disabled<br>• No real provider payout model/migration found despite notification reference<br>• Payout history/upcoming is simplified and does not use provider cadence, approved statements, Stripe transfer state, invoice PDFs, or confirmed-only visibility<br>• Commission deduction is inconsistent; one calculation returns gross paid amount<br>• Provider payout history/detail/invoice download and locked exchange-rate/failure/retry/adjustment workflows are not implemented as provider-backed behavior | ⚠️ Critical | Verified against FR-017. Main reportable risk is a concrete FE/BE contract gap plus mock-backed financial UI. |
| **PR-06: Profile & Settings Management** | 🟡 In Progress | 62% | • Provider can read/update profile basics, clinic logo, languages, awards, documents, and reviews surfaces<br>• Account info, phone/country code, timezone, and password change UI/API exist<br>• Notification preferences exist for quote, schedule, treatment, aftercare, review, promotion/discount, email, and push toggles<br>• Owner-only billing tab is hidden in frontend for non-owner accounts<br>• Banking details can be created/read/updated<br>• Help Centre, FAQ/tutorial/resource/video/contact support APIs exist<br>• Provider support case backend supports list, stats, detail, reply, and reopen | • Profile upload caps at 2MB, while PRD requires 5MB and minimum dimension validation<br>• Audit trail for all profile/account/billing/deletion changes is incomplete<br>• Owner-only billing access is frontend-hidden but backend enforcement is not proven<br>• Banking details appear stored/returned plainly; encrypted/masked flow not proven<br>• Bank validation integration and notification preference synchronization are placeholders/partial<br>• Provider support case frontend is mostly mock/static despite backend APIs<br>• Provider account deletion frontend flow not found | 📋 Standard | Verified against FR-032. Strong settings surface, but security/integration and mock-backed support areas prevent completion. |
| **PR-07: Communication & Messaging** | 🟡 In Progress | 68% | • Provider can access conversations from header popup and full communication route<br>• Conversation list shows unread badges, last message, timestamps, and selected thread<br>• Provider can send/receive text messages with optimistic UI and WebSocket updates<br>• Attachments support JPG/PNG, MP4, and PDF with limits matching FR-012<br>• Read indicators exist for provider-sent messages<br>• Backend supports persistence, history, read marking, attachments, keyword/manual flags, emergency admin intervention fields, and private broadcast channels<br>• Header popup supports recent conversations, unread/date/service filters, and search | • Backend provider conversation search only searches patient name, not inquiry/quote ID or message content<br>• Full provider chat page search is similarly limited<br>• Backend exposes conversations from invited providers, not strictly quote-submitted/first-quote conversations<br>• Message notification delivery is incomplete; broadcast exists but S-03 notification dispatch was not found<br>• Email/push notification integration is not wired end to end<br>• Provider chat UI lacks FR-012 audio/video call buttons<br>• Result caps and message lifecycle audit are partial | 📋 Standard | Verified against FR-012 and FR-022. Core chat works; search, notification dispatch, and quote-triggered conversation rules are the main gaps. |

## Provider Dashboard Summary

### Current Implementation Status

**Overall Progress: 65.9%** (average across verified PR-01 through PR-07)

| **Status** | **Count** | **Modules** | **Notes** |
| ---------- | --------- | ----------- | --------- |
| 🟢 Complete | 0 | None | No provider module is fully PRD-compliant after verification |
| 🟡 In Progress | 7 | PR-01, PR-02a, PR-02b, PR-03, PR-04, PR-05, PR-06, PR-07 | All modules have useful implementation with material gaps |
| 🔴 Not Started | 0 | None | No provider module is absent |
| **Total** | **7** | **Core Modules** | Provider dashboard verification scope |

### Critical Items Analysis

| **Module** | **Status** | **Remaining Work** | **Priority** | **Effort Estimate** |
| ---------- | ---------- | ----------------- | ----------- | ------------------- |
| PR-03: Treatment Execution | 🟡 45% | Correct Check In gates, wire End Treatment, enforce required completion fields/final scan/all-day-terminal rule, fix status mismatch | **HIGH** | ~8-12 person-days |
| PR-05: Financial Management | 🟡 35% | Add missing Earnings Tracker backend, implement payout model/statements, net commission calculations, invoice/download/failure/retry flows | **HIGH** | ~12-18 person-days |
| PR-01: Auth & Team | 🟡 70% | Enforce server-side permissions, fix invitation model/redirect, invalidate sessions after role change, add invite rate limits/bounce handling | **HIGH** | ~6-9 person-days |
| PR-02a/PR-02b: Inquiry + Quote | 🟡 78% | Fix provider privacy/search, detail authorization, quote expiry/status lifecycle, withdrawal/archive, cancellation cascade | **MEDIUM** | ~8-12 person-days |
| PR-04/PR-06/PR-07: Aftercare, Settings, Messaging | 🟡 62-72% | Search/filter gaps, treatment-to-aftercare handoff, secure billing settings, production-backed support cases, notification dispatch | **MEDIUM** | ~12-18 person-days |

### Estimated Effort Remaining

Estimated remaining Provider Dashboard effort: **~46-69 person-days**.

This estimate is higher than simple UI polish because several gaps require backend workflow enforcement, data-model/API completion, and security/compliance hardening.

### Key Achievements

- Inquiry review and quote creation are the most mature provider workflows.
- Provider aftercare has meaningful backend coverage for plans, milestones, scans, escalation, and chat.
- Team management has role, invitation, suspend/remove, and activity logging foundations.
- Communication supports live text/media chat with attachment limits broadly aligned to FR-012.

### Known Gaps Requiring Attention

- Financial management is not production-ready due to missing backend endpoint and mock-backed earnings/payout flows.
- Treatment execution is blocked by unwired End Treatment and missing FR-010 completion gates.
- Provider-side privacy/search rules need tightening before production use.
- Server-side RBAC enforcement is not consistently proven for team/settings/aftercare actions.

### Additional Costs Summary

No confirmed additional scope identified for Provider Dashboard. The remaining work appears to be completion of planned PRD/FR functionality rather than new scope.

---

# Section 3: Admin Dashboard

> **Reference**: Constitution module codes A-01 through A-10 | System PRD sections FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-023, FR-024, FR-025, FR-026, FR-027, FR-029, FR-030, FR-031, FR-033, FR-034

## Module Progress Details

| **Module / Component** | **Status** | **Completion %** | **What Users Can Do** | **What Users Cannot Yet Do** | **Category** | **Notes** |
| ---------------------- | ---------- | ---------------- | ---------------------- | ----------------------------- | ------------ | -------- |
| **A-01: Patient Management & Oversight** | 🟡 In Progress | 55% | • Admin patient list/detail UI exists with debounced search and sortable table<br>• Admin can view patient profile/detail, journey/case tabs, communications, payments, and action logs<br>• Backend supports patient profile update with justification and audit logging<br>• Admin password reset, account unlock, and suspension flows exist with justification, notifications, token revocation, and audit logs<br>• Patient action audit log supports filtering/sorting/pagination and CSV export<br>• Communication oversight and flag/unflag exist<br>• Patient deletion request queue with approve/deny APIs and FE review modal exists | • Patient list backend does not include `patient_code` search and ignores many FE filters<br>• Medical-data access justification and logging not evidenced<br>• Manual booking reschedule/cancel intervention not evidenced<br>• Refund workflow not end to end from A-01 context<br>• Audit immutability is partial<br>• Hard-delete endpoint conflicts with soft-delete/anonymization requirement<br>• GDPR anonymization/certificate flow is placeholder-like<br>• Super Admin/MFA enforcement unclear | ⚠️ Critical | Verified against FR-016 and FR-022. Core management scaffold exists, but privacy/compliance and filtering gaps are material. |
| **A-02: Provider Management & Onboarding** | 🟡 In Progress | 60% | • Admin can list providers with search, pagination, featured/status/commission filters on legacy path<br>• Admin can create provider records when payload values match backend enums<br>• Backend stores provider status, featured flag, documents, commissions, owner user, seat limit, and activity logs<br>• Provider detail exposes profile, documents, staff, reviews, commission/financials, and activity log surfaces<br>• Document upload/download/annotation exists<br>• Activation token endpoints with resend rate limiting and password policy validation exist<br>• Newer admin provider-management API better matches status transitions/auditing | • Frontend create payload can conflict with backend enums (`amount` vs `flat`, `bimonthly` vs `bi-monthly`)<br>• Admin UI still uses legacy provider APIs instead of newer FR-015-aligned APIs<br>• Used activation flow auto-generates password/7-day expiry, diverging from one-time 24-hour setup<br>• Provider list status actions are not wired<br>• Dashboard default is not active-only<br>• Deactivation/suspension workflows are incomplete/mixed<br>• Commission update re-auth not evidenced<br>• Secure document storage and FR-029 commission sync not proven<br>• Draft provider flow not clear | ⚠️ Critical | Verified against FR-015. Main risk is integration mismatch between frontend and backend contracts, not absence of provider-management code. |
| **A-03: Aftercare Team Management** | 🟡 In Progress | 65% | • Admin can view aftercare cases and details with overview, progress tracking, communication log, and admin actions<br>• Admin can reassign provider and escalate cases<br>• Admin can manage standalone aftercare requests, provider assignment, rejection, activation, and completion<br>• Backend has template CRUD with milestones, resources, purchase enablement, pricing mode, multi-currency pricing, discounts flag, validation, usage count, and delete protection<br>• Backend has aftercare audit/escalation models<br>• Admin navigation exposes Aftercare, Standalone Aftercare, Aftercare Support, and Aftercare Settings | • Full “edit all aftercare data” is incomplete; Edit Aftercare Plan and Add Notes are coming soon<br>• Case filters/list fields are incomplete versus PRD<br>• Template management is backend-heavy; existing settings UI is legacy and not full pricing/purchase template editor<br>• Provider performance/system progress analytics are backlog/absent<br>• Full audit/change-history display and edit-reason coverage are partial<br>• Live/video consultation and full aftercare team/provider/patient visibility not fully evidenced | ⚠️ Critical | Verified against FR-011. Backend is ahead of frontend; admin override/editing and template UI are largest gaps. |
| **A-04: Travel Management (API integrations)** | 🟡 In Progress | 70% | • Admin can view travel status inside booking/quote context: travel path, passport, outbound flight, return flight, hotel statuses<br>• Unified itinerary/status/passport data can be retrieved through shared endpoints<br>• Admin can re-notify patient for pending flight/hotel/passport<br>• Admin can submit flight/hotel correction payloads with mandatory reason<br>• MVP flight/hotel/passport coordination records can be stored and retrieved | • No admin-wide travel record list/filter/drilldown across all appointments found<br>• Future external API settings are mostly placeholder and no backend config persistence found<br>• Corrections update existing records rather than creating locked/superseded versions<br>• Dedicated immutable audit log for all travel mutations not evidenced<br>• Backend still uses `baggages_allowance` internally despite normalized PRD naming<br>• Automatic travel request dispatch on Confirmed transition not evidenced<br>• Correction UI is only reachable when logistics data exists | 💰 Additional | Verified against FR-008. MVP coordination boundary is mostly respected, but full admin travel management/API configuration is partial. |
| **A-05a: Patient Billing** | 🟡 In Progress | 38% | • Admin can view patient billing list and single billing detail from backend payments data<br>• Admin can view per-patient transactions with basic filtering<br>• UI exposes invoice list/detail, payment history, installment schedule, refund/reminder/override affordances, and download controls<br>• Backend can retry failed payment history by creating a Stripe PaymentIntent<br>• Payment/installment/config primitives exist: payments, histories, installments, split payment config/service, payment configuration, webhook entrypoint | • Frontend refund/reminder/status-override endpoints have no matching backend implementation found<br>• No real invoice PDF/receipt/tax invoice lifecycle or durable invoice entity<br>• Installment management is not operationally integrated into A-05a<br>• At Risk/Overdue/Partial/Refunded invoice status is mock/enriched<br>• Stripe refund API flow, refund audit, provider payout adjustment, and refund policy calculation are missing<br>• Currency lock/display and FR-029 config consumption are incomplete | ⚠️ Critical | Verified against FR-017, FR-007, FR-007b, FR-029. UI is present, but refund/reminder/invoice/installment operations are backend-incomplete. |
| **A-05b: Provider Payouts** | 🟡 In Progress | 25% | • Admin can view a provider billing list from backend data<br>• Backend list calculates net amount by subtracting quote commission from paid amount<br>• Provider dashboard has read-only payout history/upcoming endpoint<br>• Frontend has provider billing list and payout detail screens with payout breakdown UI | • No real payout approval/unapproval/void/retry/auto-processing<br>• No Stripe transfer initiation<br>• No payout statement entity matching FR statuses, approval metadata, readiness, adjustments, invoice PDF, or audit trail<br>• No scheduled payout statement generation by provider agreement cadence<br>• Payout math is inconsistent; frontend overwrites commission with mock 20%, provider dashboard sums gross amounts<br>• No locked exchange-rate payout calculation<br>• Payout detail backend endpoint missing; detail screen is mock-only<br>• No backend financial re-auth enforcement | ⚠️ Critical | Verified against FR-017. Mostly non-compliant operationally; current value is read-only visibility and partial list math. |
| **A-05c: Financial Reconciliation & Reporting** | 🟡 In Progress | 35% | • Admin/provider billing lists and patient invoice-like lists exist<br>• Basic revenue, average revenue per patient, provider response time, and pending payment charts exist<br>• Designed payout list/detail UI includes batch approval, readiness, failed/overdue states, re-auth modal, adjustments, treatment breakdown, and CSV affordances<br>• Legacy provider bill payment and failed patient payment retry exist<br>• Financial dashboard UI shows KPIs, outstanding aging, refund trend, affiliate summary, and currency alert modal | • Backend payout statement lifecycle, Stripe transfer, webhook statuses, void/unapprove/retry are missing<br>• Frontend payout approval/retry endpoints are not defined in backend<br>• No durable FR-017 payout statement schema<br>• Financial re-auth and complete audit trail are missing<br>• Affiliate payout/reconciliation and discount ROI reconciliation are mock/absent<br>• Multi-currency locked-rate reporting is incomplete<br>• FR-014 Screen 12 financial health/cashflow suite is not implemented with real backend<br>• Provider payout detail is frontend-only mock | ⚠️ Critical | Verified against FR-017 and FR-014. Reporting visuals exist, but financial operations/reconciliation are largely not real backend workflows. |
| **A-06: Discount & Promotion Management** | 🟡 In Progress | 40% | • Admin can create/list/view/update/delete platform discounts<br>• Provider can create/list/view/update/delete provider-specific discounts<br>• Provider quote flow can select/apply Hairline promotions<br>• Backend validates active state, date window, usage limit, patient access, and blocks second discount on same quote/date<br>• Basic usage count and promotion stats endpoint exist | • Both-fees provider approval workflow not implemented<br>• Discount approval notification dispatch not found and references mismatched model<br>• Admin discount catalog is not FR-019/FR-022 compliant<br>• Package-upgrade discount type and provider targeting/subsets not implemented<br>• ROI/financial impact dashboard/export uses static or absent data<br>• Audit trail for discount actions not found<br>• Discount priority across patient/provider/affiliate conflicts is incomplete<br>• Hairline-only invisibility from providers not enforced | 📋 Standard | Verified against FR-019 and FR-022. Basic CRUD/application exists; governance, targeting, audit, and ROI features are missing. |
| **A-07: Affiliate Program Management** | 🟡 In Progress | 25% | • Admin can list, create, view, edit, and delete affiliates<br>• Admin can add commission-rule records and affiliate discount-code records<br>• Code uniqueness check exists<br>• Frontend has affiliate overview, add/edit, detail, and billing pages<br>• Basic affiliate data model exists | • Affiliate codes are not validated in patient checkout<br>• Signups/bookings are not tracked via affiliate codes<br>• Applied vs completed usage is not distinguished<br>• Commission is not auto-calculated on completed paid bookings<br>• Affiliate dashboard/portal, referral revenue, pending payout, payout history are missing<br>• Monthly payout list, payout batch, retry, payout status, and reports are missing<br>• Hairline-fee-only, single discount priority, threshold, refund reversal, payment-detail security, audit, and notifications are missing | 📋 Standard | Verified against FR-018. Current implementation is mostly admin CRUD/onboarding, not the full affiliate program workflow. |
| **A-08: Analytics & Reporting** | 🟡 In Progress | 18% | • Admin analytics navigation and routes exist for overview, Hairline overview, provider performance, treatment outcomes, financial overview, and conversion/marketing<br>• Basic platform KPIs exist: active providers, signups, inquiries, quotes, revenue, profit, average revenue/profit per patient<br>• Some provider performance, financial, treatment-like, patient, and geographic trend signals exist | • FR-014 7-screen admin analytics suite is not implemented<br>• Required TTFQ, engagement, funnel, GMV, commission, payout obligation, cash-at-risk, demand/supply, pricing intelligence, and financial health widgets are absent or simplified<br>• Treatment Outcomes includes prohibited clinical metrics<br>• Analytics access logging, configurable thresholds, default filters, stale-data banner, permission hiding, and FX fallback rules not evidenced<br>• Several endpoints return sample/dummy or legacy simplified metrics | 📋 Standard | Verified against FR-014 v3.5. Implementation is closer to a legacy partial analytics dashboard than the PRD-defined A-08 suite. |
| **A-09a: Content & Treatment Management** | 🟡 In Progress | 50% | • Admin/provider treatment and package screens exist<br>• Treatment CRUD, media upload, package CRUD, provider treatment pricing, active/inactive filtering, and package availability are partially implemented<br>• Regional/location preferences, preview, starting prices, cache invalidation, change reasons, and audit logging exist<br>• Questionnaire catalog UI exists with catalog/detail/question editor/preview, context types, severity fields, and frontend publish/activate actions | • Treatment versioning is not immutable; records are updated in place<br>• Admin-only treatment controls are weak because routes sit under provider auth<br>• Provider package ownership/privacy and quote-level treatment/package version locking are not clear<br>• Questionnaire management is mostly frontend mock/local state; no matching backend catalog/version/category/active-inquiry APIs found<br>• Dynamic inquiry questionnaire delivery, backend publish validation, rollback, immutable audit, and severity-based provider alerts are missing<br>• Regional group overlap enforcement, inactive archive, rate limits, and currency conversion are incomplete | ⚠️ Critical | Verified against FR-024, FR-025, FR-028. Regional pricing is strongest; questionnaire catalog is largely prototype/mock. |
| **A-09b: Aftercare Template Configuration** | 🟡 In Progress | 45% | • Backend has admin CRUD routes for aftercare templates<br>• Backend stores template metadata, treatment compatibility, duration, status, purchasable flag, pricing mode/data, milestones, and resource files/metadata<br>• Backend blocks deletion when templates are linked to aftercare cases/milestones<br>• Backend returns usage/resource/milestone counts<br>• Existing admin UI exposes basic aftercare settings tabs for milestones, questionnaires, and resources | • Admin frontend does not expose the new `settings/aftercare-templates` CRUD workflow or unified Screen 16 editor<br>• UI remains fragmented legacy tabs, not template-level milestone/resource/questionnaire configuration<br>• Questionnaire selection is not integrated with FR-025 aftercare-context questionnaire sets<br>• Questionnaire IDs/frequencies are embedded in scan schedule rather than structured link table<br>• Per-milestone resource assignment semantics are partial<br>• Template usage count, purchasable/internal status, lifecycle, and safe delete controls not clear in frontend<br>• Backend requires resources on create, conflicting with PRD allowance for empty resources | ⚠️ Critical | Verified against FR-011. Backend is ahead of frontend; core template configuration is not end-to-end usable from admin UI. |
| **A-09c: System Settings & Payment Rules** | 🟡 In Progress | 60% | • Admin can manage many FR-026 settings: auth throttling, OTP config/templates, countries, discovery questions, cancellation reasons, account deletion reasons, and version/audit history<br>• Legal document management exists with draft/edit/publish/current/archive, public current legal pages, acceptance detail/export<br>• Key payment rules exist: Stripe country config, encrypted/masked keys, validation, deposit rates, provider-specific deposit rates, split-payment config, installment preview, currency conversion pairs/sources/markup/audit<br>• Notification templates/event types support CRUD, preview/validation, versions, language variants<br>• Backend supports admin users, role changes, suspension/reactivation, audit trail/export/stats, and protected routes | • Notification rules are mostly frontend/mock; backend CRUD beyond templates/event types not found<br>• Admin RBAC frontend pages use mock data in key places<br>• Legal PRD parity is incomplete: immutable audit, reminder tracking, and Cancellation Policy frontend type not strongly evidenced<br>• Payment config lacks regional groupings, global fallback Stripe account, late-payment grace period, complete rate-source scheduling/alerts, and Stripe-account deletion protection<br>• Strict route permission enforcement and mandatory change reasons are inconsistent | ⚠️ Critical | Verified against FR-026, FR-027, FR-029, FR-030, FR-031. Settings are materially implemented, but notification rules and RBAC admin UX remain gaps. |
| **A-10: Communication Monitoring & Support** | 🟡 In Progress | 58% | • Backend can create/update quote-context conversations and maintain inquiry/quote references<br>• Backend can send/read messages, enforce attachment limits, broadcast events, track reads, and auto-create keyword flags<br>• Admin-only keyword rule/flag endpoints, manual observation flags, flag history, and emergency intervention primitives exist<br>• Backend has substantial support case model/API coverage: case IDs, lifecycle, filters/search/stats, manual creation, transitions, assignment, bulk assign/close, timeline, messages, notes, attachments, export, notifications/events<br>• Patient/provider support-ticket creation and two-way replies exist<br>• Frontend routes exist for support messages, tickets, monitoring, flags, intervention, exports, and support case configuration | • Admin Communication Monitoring Center frontend uses mock/local state rather than backend chat/flag APIs<br>• Admin Support Tickets frontend listing/detail are mock/local-state driven, not wired to admin support-case APIs<br>• Monitoring filters are incomplete versus PRD<br>• Emergency intervention UI does not call backend intervention/send-message APIs<br>• Support case frontend does not prove immutable timeline, real thread, backend workflow enforcement, auto-close/reopen, S-03 delivery, or deep links<br>• Malware scanning for uploads not evidenced<br>• FR-033 content management belongs mostly to settings/A-09, not A-10 | ⚠️ Critical | Verified against FR-012, FR-033, FR-034. Backend support-case structure is strong, but admin frontend integration is weak. |

## Admin Dashboard Summary

### Current Implementation Status

**Overall Progress: 46.0%** (average across verified Admin table rows)

| **Status** | **Count** | **Modules** | **Notes** |
| ---------- | --------- | ----------- | --------- |
| 🟢 Complete | 0 | None | No admin module row is fully PRD-compliant after verification |
| 🟡 In Progress | 14 rows | A-01 through A-10, including A-05 and A-09 submodules | All admin areas have partial implementation with material gaps |
| 🔴 Not Started | 0 | None | No admin module row is completely absent |
| **Total** | **10** | **Core Modules** | A-04 travel is tracked as additional/future scope unless PRD review says otherwise |

### Critical Items Analysis

| **Module** | **Status** | **Remaining Work** | **Priority** | **Effort Estimate** |
| ---------- | ---------- | ----------------- | ----------- | ------------------- |
| A-05b: Provider Payouts | 🟡 25% | Payout statement lifecycle, approval/retry/void, Stripe transfers, payout detail API, net commission and FX calculation, audit/re-auth | **CRITICAL** | ~15-25 person-days |
| A-05a/A-05c: Patient Billing + Reconciliation | 🟡 35-38% | Refunds, reminders, status overrides, invoice generation, installment operations, locked-rate reporting, audit/re-auth | **CRITICAL** | ~18-28 person-days |
| A-08: Analytics | 🟡 18% | FR-014 admin analytics suite, PRD-compliant metrics, access logging, filters, stale data/FX behavior | **HIGH** | ~20-30 person-days |
| A-07: Affiliates | 🟡 25% | Checkout attribution, conversion tracking, commission calculation, affiliate portal, payout processing, reports | **HIGH** | ~12-20 person-days |
| A-01/A-02/A-03/A-09/A-10: Operational Admin | 🟡 45-65% | Filtering/privacy, provider API integration, aftercare edit/template UI, settings RBAC/rules, support frontend API wiring | **HIGH** | ~35-55 person-days |

### Estimated Effort Remaining

Estimated remaining Admin Dashboard effort: **~100-158 person-days**.

The largest driver is not missing screens alone; it is converting mock/static UI and legacy/simple backend surfaces into audited, permissioned, production-backed workflows.

### Key Achievements

- Admin can operate partial surfaces for patient/provider management, aftercare oversight, travel coordination, settings, support, and content management.
- Travel coordination is relatively strong for MVP booking-context workflows.
- System/payment/legal settings have broad backend coverage, even though RBAC and notification rules remain incomplete.
- Support case backend has substantial structure for lifecycle, assignment, messages, timeline, notes, attachments, and export.

### Known Gaps Requiring Attention

- Financial operations are the largest admin gap: payout, refund, installment, invoice, reconciliation, affiliate payout, and audit workflows are incomplete.
- Analytics is far below the latest FR-014 admin suite and includes prohibited clinical-style outcome metrics.
- Several admin UIs are mock/local-state backed despite available or planned backend APIs.
- Compliance-heavy requirements need attention: immutable audit, role enforcement, financial re-auth, encrypted/masked payment data, GDPR deletion/anonymization, and malware scanning.

### Additional Costs Summary

No confirmed additional scope identified for Admin Dashboard. Most remaining work maps to existing FRs, especially FR-014, FR-017, FR-018, FR-019, FR-026 through FR-031, FR-033, and FR-034.

---

# Risks, Issues & Dependencies

## Critical Risks

| **Risk** | **Impact** | **Probability** | **Mitigation Plan** | **Owner** | **Status** |
| -------- | ---------- | --------------- | ------------------- | --------- | ---------- |
| Financial operations are not production-ready | High - blocks provider trust, refunds, payouts, reconciliation, and launch finance controls | High | Prioritize FR-017/A-05a/b/c and PR-05 backend workflows before launch readiness | Product + Backend + Frontend | Open |
| Mock/local-state admin screens may overstate readiness | High - support, analytics, payouts, affiliate billing, and some settings appear complete visually but are not production-backed | High | Mark mock-backed screens as not release-ready and replace with API-backed workflows | Frontend + Backend | Open |
| Compliance and audit gaps remain | High - affects patient data, medical data access, financial changes, GDPR deletion, and role enforcement | Medium-High | Add server-side permissions, immutable audit, access justification, encryption/masking, and re-auth gates | Backend + Security | Open |
| Provider treatment execution has workflow-breaking gaps | High - treatment completion and aftercare handoff may fail or violate FR boundaries | Medium | Fix FR-010 gates, End Treatment wiring, status mismatch, and completion-to-aftercare integration | Provider Team | Open |

## Active Issues

| **Issue** | **Affected Tenant(s)** | **Severity** | **Description** | **Resolution Plan** | **ETA** |
| --------- | ---------------------- | ------------ | --------------- | ------------------- | ------- |
| Missing Provider Earnings Tracker backend endpoint | Provider | High | Frontend calls `provider-dashboard/earnings-tracker`, but matching backend route was not found | Add backend route/controller contract or update frontend to existing API | TBD |
| End Treatment action is not wired | Provider | High | End Treatment frontend mutation call is commented out and required fields/gates are missing | Wire mutation and enforce FR-010 completion validation | TBD |
| Admin payout detail/approval flows are mock or missing backend | Admin | Critical | Provider payout approval/retry/detail screens are not backed by real payout statement lifecycle | Implement payout statement model/API and Stripe transfer workflow | TBD |
| Patient billing actions lack backend routes | Admin | High | Refund, reminder, and status override calls are exposed in UI but matching backend implementation was not found | Implement routes/services/audit and wire UI responses | TBD |
| Analytics suite is not aligned to FR-014 | Admin | High | Current analytics is a partial legacy dashboard and includes prohibited clinical-style outcome metrics | Rebuild/extend A-08 around FR-014 Screen 7-13 contracts | TBD |
| Admin support and communication screens are mock/local-state backed | Admin | High | Backend support APIs are stronger than the frontend integration | Replace mock state with support-case/chat/flag APIs | TBD |

## Key Dependencies

| **Dependency** | **Impact** | **Status** | **Required By** | **Notes** |
| -------------- | ---------- | ---------- | --------------- | --------- |
| Stripe payout/refund/transfer implementation | Required for provider payouts, refunds, reconciliation, and financial launch readiness | Partial | A-05a, A-05b, A-05c, PR-05 | PaymentIntent retry exists, but payout/refund/statement lifecycle is incomplete |
| FR-029 payment configuration integration | Required for deposit/installment/Stripe/currency rules to affect billing workflows | Partial | A-05a, A-05c, A-09c | Settings exist, but operational consumption is inconsistent |
| S-03 notification service integration | Required for messaging, payment reminders, quote/treatment alerts, support case updates | Partial | PR-07, A-10, A-05a, A-09c | Broadcast/event pieces exist; end-to-end notification dispatch is incomplete |
| Server-side RBAC and audit framework | Required for Provider/Admin security and compliance | Partial | PR-01, PR-06, A-01, A-09c, A-10 | Role data exists, but per-action enforcement and immutable audit are inconsistent |
| FR-025 questionnaire catalog backend | Required for A-09a/A-09b template/questionnaire compliance | Mostly missing | A-09a, A-09b, PR-04 | Current questionnaire catalog is largely frontend mock/local state |

---

# Roadmap to MVP / Production Release

**Target MVP Date:** TBD after resourcing decision  
**Target Production Release:** TBD after Provider/Admin remediation and Mobile App review

| **Phase** | **Duration** | **Key Deliverables** | **Completion Date** | **Status** |
| --------- | ------------ | -------------------- | ------------------- | ---------- |
| **Provider/Admin Remediation** | 146-227 person-days | Financial operations, treatment execution, RBAC/audit, mock-to-API integration, analytics alignment | TBD | 🟡 |
| **Testing & QA** | TBD | UAT, performance testing, security audit, bug fixes | TBD | 🟡 |
| **Production Launch** | TBD | Soft launch, full launch, post-launch support | TBD | 🔴 Pending remediation and Mobile review |

## Key Milestones

- Complete Provider financial backend and Admin financial operations remediation.
- Wire Provider treatment completion and aftercare handoff to FR-010/FR-011-compliant workflow.
- Replace mock-backed Admin support, payout, affiliate billing, and analytics surfaces with production APIs.
- Complete server-side RBAC/audit/security hardening for Provider/Admin workflows.
- Run separate Mobile App status review before calculating whole-platform completion.

## Client Decisions Required

1. Decide whether FR-017 financial operations are MVP launch blockers.
2. Decide whether A-08 analytics is required for MVP or can be phased after operational launch.
3. Decide whether A-04 remains MVP coordination-only or needs admin-wide travel management.
4. Confirm whether support and help-center surfaces must be fully production-backed before MVP.
5. Confirm team capacity so the 146-227 Provider/Admin person-day estimate can be converted into calendar dates.

---

**End of Report**

**Report Prepared By:** Project Team  
**Date:** April 24, 2026  
**Version:** 1.0 - Current Provider/Admin Status Review
