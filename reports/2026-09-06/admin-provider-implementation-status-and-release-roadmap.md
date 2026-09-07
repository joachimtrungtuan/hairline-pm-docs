# Admin and Provider Dashboard Implementation Status and Release Roadmap

**Date:** 2026-09-06
**Purpose:** Meeting decision support for implementation completeness and release sequencing
**Scope:** Admin Dashboard and Provider Dashboard only
**Excluded:** Mobile app and runtime reliability testing

## Executive conclusion

The static repository audit found that the two dashboards are **not fully implemented against the current functional requirements**. Every module has meaningful code, but none is confirmed launch-ready as a complete module. The recurring issue is not a lack of screens: backend capabilities are often ahead of the frontend, while several visible screens still use fixtures, legacy routes, or incomplete authorization.

**Recommendation:** do not launch everything at once. Use four gated releases, beginning with a controlled provider inquiry-and-quote pilot. Clinical, financial, and scale capabilities should enter production only after their own contract and security gates pass.

### Status language

- **Substantial partial:** core workflow exists; focused gaps prevent release.
- **Partial:** important documented behavior is missing, divergent, or not exposed.
- **Backend-led:** backend coverage is substantial, but the user-facing workflow is mock-backed or not connected to the authoritative API.
- All statuses are based on static source inspection, not runtime proof.

## Provider Dashboard status

| Module | FR focus | Static status | What is present | Decisive gap and required action |
|---|---|---|---|---|
| PR-01 Authentication and Team | FR-009 | Substantial partial | Login, team directory, invitations, roles, suspension, and activity foundations | Align refresh-token routes, remove invitation fallback data, enforce actor permissions on mutations, and revoke sessions after role/status changes. |
| PR-02 Inquiry and Quote | FR-003, FR-004, FR-005, FR-022 | Substantial partial | Inquiry discovery, quote creation/listing, and scheduling foundations | Prevent pre-payment patient identity exposure, align pagination/search contracts, remove hard-coded quote status, and validate slot/overlap rules. |
| PR-03 Treatment Execution | FR-010 | Partial | Treatment list, daily entries, notes, scans, start/end controls, reminders | Replace the divergent legacy quote-based lifecycle with one authoritative flow; enforce payment/date/role gates, required completion evidence, autosave, and correct cancellation ownership. |
| PR-04 Aftercare | FR-011 | Partial | Case list/detail, setup, plans, scans, chat, and escalation foundations | Add provider ownership checks to all case resources and mutations; wire search/pagination and clinician assignment; verify case creation ownership. |
| PR-05 Financial and Reporting | FR-014, FR-017, FR-019 | Backend-led | Earnings, payout, performance, pricing, and reporting screen structures | Replace hard-coded analytics and simulated exports, remove payout/promotion fallbacks, and connect every filter and action to live contracts. |
| PR-06 Profile and Settings | FR-013, FR-021, FR-024, FR-032, FR-033 | Partial | Profile, clinic, pricing, package, review, locale, and help/settings foundations | Persist review responses, complete provider package management and localization, connect support cases, and remove help/review fallbacks. |
| PR-07 Communication | FR-012, FR-020, FR-022 | Partial | Conversations, text/media, read receipts, unread state, notifications, and call routes | Remove the mock-default send transport, require quote eligibility, dispatch durable message notifications, and prove the external call service separately. |

## Admin Dashboard status

| Module | FR focus | Static status | What is present | Decisive gap and required action |
|---|---|---|---|---|
| A-01 Patient Oversight | FR-003–008, FR-013, FR-016, FR-034, FR-037, FR-038 | Partial | Patient list/detail, audit-log read path, communication review, and several backend intervention endpoints | Add live Admin inquiry/quote/booking and medical-access workflows; align payment actions; remove review fixtures; implement or formally de-scope monitoring oversight. |
| A-02 Provider Management | FR-015 | Substantial partial | Onboarding wizard, provider profiles, documents, commissions, staff, and backend activation/status controls | Reconcile legacy and canonical APIs, finish list-level status actions and activation flows, and enforce operation-specific Admin permissions. |
| A-03 Aftercare Team | FR-011 | Partial | Overview, standalone requests, assignment, escalation, and backend audit foundations | Route the real multi-tab case detail, replace hard-coded provider availability/options, implement plan editing and notes, and cover all mutations with RBAC/audit. |
| A-04 Travel Management | FR-008 | Partial | Booking-level hotel/flight review, corrections, status changes, and re-notification | Add system-wide travel oversight and passport correction; implement immutable correction versions, soft deletion, and complete audit history. |
| A-05 Billing and Finance | FR-007, FR-017 | Backend-led | Payout statements, invoices, finance search, disputes, currency alerts, and audit endpoints | Replace static reporting; connect finance search/audit, currency alerts, and payout execution; migrate legacy invoice actions to current routes; remove fallback financial values. |
| A-06 Promotions | FR-019 | Partial | Program hub, detail, adoption, portfolio, code, and analytics foundations | Correct method/path mismatches for lifecycle and adoption actions and remove the always-on portfolio fixture. |
| A-07 Affiliate | FR-018 | Partial | Affiliate CRUD, codes, portal, lifecycle, payout, and commission backend foundations | Connect the UI to current billing/lifecycle/bulk-code APIs and stop blending fixture metrics into live affiliate data. |
| A-08 Analytics and Reporting | FR-014 | Backend-led | Seven routed Admin analytics workspaces and backend endpoint families | Screens 7, 8, and 11 are fixture-driven; Screens 9, 10, 12, and 13 have aggregate-route or response-contract mismatches. Align contracts, remove silent fallback, and add audit/drill-down/export proof. |
| A-09 System Settings | FR-021, FR-023–031, FR-036 | Mixed partial | Strong static questionnaire, legal-content, payment-configuration, and core settings foundations | Remove localization/RBAC/notification-history demo data, add retention observability, complete regional-pricing CRUD/version evidence, resolve package authorization, and keep undefined FR-036 explicitly deferred. |
| A-10 Communication and Support | FR-012, FR-034 | Backend-led | Basic chat/emergency controls plus comprehensive support-case and configuration backend routes | Current support lists/forms/configuration are mock-backed; connect case CRUD, assignment, replies, escalation, categories, priorities, and audit to live APIs. |

## Cross-cutting diagnosis

| Pattern | Business consequence | Required response |
|---|---|---|
| Legacy and current APIs coexist | A screen can look complete while calling a stale or absent endpoint | Choose one authoritative contract per workflow and remove or migrate legacy callers. |
| Fixtures and fallback values remain in visible workflows | Sample data may be mistaken for operational truth | Production must fail visibly; fixtures must be development-only and clearly isolated. |
| Route authentication is broader than operation authorization | Cross-provider access or excessive Admin privilege remains possible | Add tenant ownership, role, re-authentication, and negative authorization tests to release gates. |

## Recommended four-phase release roadmap

| Priority and phase | Release objective | Provider functions | Admin functions | Exit gate |
|---|---|---|---|---|
| **P0 — Phase 1: Controlled commercial pilot** | Conditional target for onboarding selected providers and completing inquiry-to-quote work | PR-01 team access, PR-02 inquiry/quote, essential PR-06 profile/pricing | A-02 onboarding, implement A-01 inquiry/quote oversight, essential A-09 access and inquiry configuration | One authoritative API per flow; no production fixtures; live RBAC, session revocation, provider isolation, pre-payment identity privacy, quote-state consistency, and scheduling rules pass. |
| **P0 — Phase 2: Clinical and patient operations** | Safely execute paid treatment and aftercare | PR-03 treatment, PR-04 aftercare, core PR-07 messaging | A-01 booking/treatment intervention, A-03 aftercare, A-04 travel, basic A-10 support, minimum A-05 invoice/refund controls | Billing uses current invoice routes; treatment and aftercare invariants pass; messaging uses real transport with quote eligibility and durable notifications; call functionality is either proven or excluded; clinical acceptance tests pass. |
| **P1 — Phase 3: Settlement and partner growth** | Reconcile money and activate scalable partner acquisition | PR-05 earnings/payout essentials and promotion visibility | A-05 reconciliation/payouts, A-06 promotions, A-07 affiliate operations | Financial UI uses authoritative APIs with no simulated/fallback values; payout/refund/re-auth/audit rules pass; promotion and affiliate lifecycle contracts align. |
| **P2 — Phase 4: Scale and optimization** | Add decision intelligence, localization depth, and advanced self-service | Advanced PR-05 analytics/exports and remaining PR-06 settings/help | A-08 analytics, remaining A-09 configuration/compliance, advanced A-10 monitoring/support analytics | All analytics use live traceable data; exports/drill-downs/audit work; localization publish/rollback and retention observability pass. |

**Release rule:** phases are sequential gates. Phase 1 and Phase 2 are both P0 because both are required for the core business journey, but Phase 2 cannot run in parallel with or bypass Phase 1. A phase may be enabled for a limited provider cohort only after its exit gate passes.

## Immediate action register

| Order | Action | Suggested owner | Completion evidence |
|---|---|---|---|
| 1 | Publish an authoritative FE-to-BE route matrix for Phase 1 and remove legacy callers | FE and BE leads | Every Phase 1 action resolves to an existing route with matching method, payload, response, and error contract. |
| 2 | Inventory and eliminate production mock/fixture/fallback paths in Phase 1 and Phase 2 | FE lead | Production build contains no silent sample-data substitution for released functions. |
| 3 | Close tenant ownership, role, re-authentication, and audit gaps | BE and security leads | Positive and negative authorization cases pass for Provider and Admin actors. |
| 4 | Define one treatment lifecycle and an explicit aftercare handoff | Clinical product and engineering | Server-enforced states cover start, daily execution, completion, cancellation, handoff, aftercare, and escalation. |
| 5 | Deliver Admin intervention surfaces with their owning phase | Admin FE lead and operations | Inquiry/quote controls pass in Phase 1; booking, payment, travel, and support controls pass before their later phases. |
| 6 | Build phase-level acceptance matrices, then run reliability testing separately | QA lead | Each released requirement has static evidence plus runtime pass/fail evidence; reliability results remain a separate report. |

## Decisions required in the meeting

1. Approve the four-phase approach and reject a big-bang launch.
2. Make pilot approval conditional on signed-off Phase 1 route, privacy/RBAC, session, quote-state, and scheduling gates.
3. Decide whether FR-037/FR-038 Admin monitoring is required for the first clinical release or formally deferred.
4. Assign accountable FE, BE, security, product, and QA owners to the six immediate actions.
5. Approve a separate runtime reliability assessment after the implementation gaps for each phase are closed.

## Evidence boundary

This report compared current FR/module documentation with the current `main/hairline-frontend` and `main/hairline-backend` source. Code maps were used only to locate owners; conclusions were confirmed in source components, API slices, routes, controllers, services, and configuration. It does **not** claim that a statically present capability works at runtime, and it does not assess the mobile app.

Representative anchors include `main/hairline-backend/routes/api.php`, Provider team/inquiry/treatment/aftercare/chat API owners, Admin patient/billing/analytics/settings/support owners, and their matching controllers. Particularly decisive sources include `TreatmentExecutionController`, `AfterCareController`, `ChatController`, `AdminAnalyticsController`, the Admin analytics API slice, and the support-center pages and API slice.
