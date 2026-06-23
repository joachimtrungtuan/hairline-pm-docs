# FR-018 Screen Architecture Restructure & Affiliate Activation Flow

**Date**: 2026-06-22
**Report Type**: Functional Requirement Update
**FR**: FR-018 — Affiliate Management (Module A-07)
**File changed**: `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md`
**Version**: 1.2 → 1.3
**Author**: Claude (AI)

---

## Summary

Restructured the FR-018 Screen Specifications from 6 screens into a fuller admin + affiliate architecture (9 admin screens, 3 admin modals, 1 tabbed affiliate portal), added an affiliate account activation flow mirroring the provider activation flow (FR-015), introduced two shared detail screens, and folded the standalone Billing History into a consolidated Payout Management area. Added supporting fields, business rules, requirements, entities, and user stories.

This was a user-directed product change (not a verification pass): the user defined the target admin/affiliate screen structure, confirmed the shared Promo Code Detail and Payout/Transaction Detail screens, and approved the additional modals and fields.

---

## Changes

### Screen Specifications (restructured)

**Admin Platform (A-07)** — now Screens 1–9 plus Modals A–C:

1. **Screen 1: Affiliate Management Dashboard (Overview)** — kept; added Performance Tier column, "View Details → Screen 3" navigation, and updated the bulk-generate reference (now Screen 4).
2. **Screen 2: Add/Edit Affiliate Form** — kept; added fields (see below).
3. **Screen 3: Affiliate Detail** — NEW. Per-affiliate hub: account details, assigned promo codes list, payout history + upcoming payout, activity/audit, internal notes, and status/activation actions.
4. **Screen 4: Affiliate Code Generation** — reframed from the old Screen 3 as the single/selected/filtered generation tool.
5. **Screen 5: Code Generation Results** — NEW. Created/skipped/failed summary with per-row reasons and retry-failed-only (backs B4).
6. **Screen 6: Promo Code Management** — NEW. System-wide registry of all affiliate-bound codes.
7. **Screen 7: Promo Code Detail (Shared)** — NEW. Single shared screen reached from both Screen 6 and the assigned-codes list inside Screen 3.
8. **Screen 8: Affiliate Payout Management** — reworked old Screen 4 and folded the old Screen 5 Billing History into it as a sub-view (Overview / Transactions / Billing History), preserving 7-year retention and CSV export.
9. **Screen 9: Payout / Transaction Detail (Shared)** — NEW. Single shared screen reached from both Screen 8 and the payout list inside Screen 3.
10. **Modal A: Suspend / Reinstate Affiliate** — NEW (backs B3; mirrors FR-015 provider suspension).
11. **Modal B: Edit Commission Structure** — NEW (backs A2; captures effective date, no retroactive recalculation).
12. **Modal C: Confirm Batch Payout** — NEW (confirmation before gateway transfers; £50 threshold note).

**Affiliate Platform** — Screen 10:

- **Screen 10: Affiliate Portal** — reworked old Screen 6 into a tabbed portal: Overview, Promo Codes, Payouts, Profile. Profile is self-service for non-sensitive fields (name, phone, language); payment details, commission, and status are read-only/admin-controlled.

### Affiliate Activation Flow (NEW)

- Main Flow updated so account creation sends a one-time secure set-password link (expires 24h) instead of emailing raw credentials; added password-set and first-login steps.
- Added Alternative Flow **A5: Affiliate Activation & Resend** (self-service + admin-triggered, rate-limited to 3/hour/email, link invalidation, generic security messaging) — mirrors FR-015 A1.
- Entry Points updated to describe activation before first login.

### Field Additions (Screen 2: Add/Edit Affiliate)

- **Phone Number**, **Language(s)**, **Tax / VAT / Business Reg ID** (compliance for international payouts).
- **Performance Tier** (read-only, system-calculated) and **Language** now exist as fields — previously the Dashboard filtered by these but the form never collected them.
- **Activation Status** (Invited until password set / Active) and **Last Login** (read-only).

### Business Rules

- Added General Rule 10 (activation link mirrors provider flow; no raw credentials emailed).
- Admin Editability Rules: added an "Editable by Affiliate (Self-Service)" section (name, phone, language only); expanded admin-editable list (phone, language, country, type, tax/VAT ID, status via Modal A, commission via Modal B); added activation link expiry/resend rate limit to "Fixed in Codebase".

### Requirements, Entities, Testing

- Added **REQ-018-027 … REQ-018-036** (Affiliate Detail, Promo Code Management + shared detail, shared Payout detail, activation flow, tabbed portal/self-service, code generation results, suspend/reinstate, commission effective date, batch payout confirmation, activation state/last login).
- Key Entities updated: Affiliate Account (phone, language, tax/VAT ID, activation status, performance tier, last login); Affiliate Payout (reversals/refunds, net amount, failure reason); Generation Batch (skipped count); Transaction Log (status changed, activation sent).
- Added User Story 1b (Affiliate Account Activation) and a new activation edge case; updated US-1, US-4 (Modal C), US-6 (Modal B) scenarios.
- Added FR-015 to internal dependencies (activation/self-service pattern reuse).

---

## Rationale

- **Shared detail screens**: Promo Code Detail and Payout/Transaction Detail are each implemented once and reached from two entry points (global list and the corresponding list inside Affiliate Detail), avoiding duplicate specs and keeping admin navigation consistent.
- **Consistency with provider lifecycle**: the affiliate activation and profile self-service patterns mirror FR-015/FR-032 so onboarding behaves the same across roles of the same nature.
- **Closed workflow/screen gaps**: B3 (suspension), B4 (bulk partial failure), and A2 (commission edit) were documented flows with no backing screen; Dashboard filters referenced fields (language, performance tier) the form never collected.

---

## Cross-Document Impact / Follow-ups

- No changes made to FR-019; FR-018 still owns affiliate-bound code generation while FR-019 remains the shared validation/redemption engine.
- Potential later alignment (not changed here): FR-015/FR-032 activation-template reuse and FR-017 affiliate billing/payout execution boundary may want a cross-reference once these screens are designed.
- Status remains **Draft**; approvals still pending.

---

## Addendum (same day) — Payout method standardized on Stripe + provider-mirrored bank details (v1.3 → v1.4)

Follow-up user-directed change: affiliate payouts should use Stripe (consistent with the rest of the system) and affiliates should supply bank details the same way providers do.

**Changes:**

- **Stripe-only payouts**: Removed PayPal and "Other" payout methods throughout. Affiliate payouts are now executed as **Stripe transfers** to the affiliate's bank account, consistent with provider payouts (executed via FR-017 / S-02 using the Stripe accounts configured in FR-029; status driven by `transfer.*` webhooks).
- **Provider-mirrored bank details**: Replaced the generic Payment Method / Bank Account Details / PayPal Email fields on Screen 2 with the same field set providers provide in FR-032 — **Account Holder Name, Bank Name, Account Number (masked, encrypted), Routing/SWIFT Code, IBAN (optional)** — with S-02 format validation, AES-256 at rest, and last-4 masking.
- **Propagated** the Stripe/bank model across Main Flow + B2, Screens 3/8/9, Modal C, the affiliate Profile tab, business/editability/billing rules (new Billing Rule 3: complete bank details required before payout), dependencies, external services, integrations, security, requirements (REQ-018-001/008/015/016/021 reworded; **REQ-018-037 added**), key entities (Affiliate Account bank-detail attributes; Affiliate Payout now carries Stripe Transfer ID), user stories, and the gateway-down edge case.

No change to payout ownership split (FR-018 calculates commissions; FR-017 executes billing/payouts) — only the payout mechanism and bank-detail collection were standardized.

---

## Addendum (same day) — Decimal sub-screen notation + per-tab affiliate screens (v1.4 → v1.5)

Follow-up user-directed change for screen-numbering consistency with other FRs (e.g., FR-033) and to make each affiliate tab its own screen.

**Changes:**

- **Modals now carry screen codes** under their parent (FR-033-style decimal notation), each labeled "(Modal)" and placed immediately after its parent:
  - **Screen 3.1** — Suspend / Reinstate Affiliate (was Modal A)
  - **Screen 3.2** — Edit Commission Structure (was Modal B)
  - **Screen 7.1** — Confirm Batch Payout (was Modal C)
- **Code Generation Results confirmed as a full screen** (not a transient modal — it persists the batch, supports retry-failed and CSV export, and is revisitable), renumbered **Screen 4.1** (child of the generation screen, Screen 4).
- **Sequential renumber** of the remaining admin screens after pulling the results screen under Screen 4: Promo Code Management 6→**5**, Promo Code Detail (shared) 7→**6**, Affiliate Payout Management 8→**7**, Payout/Transaction Detail (shared) 9→**8**.
- **Affiliate portal split into one screen per tab**: former combined Screen 10 is now a portal shell (**Screen 9**) plus **Screen 9.1 Overview**, **9.2 Promo Codes**, **9.3 Payouts**, **9.4 Profile** — each with its own purpose, data fields, business rules, and acceptance criteria.
- **Propagated** every cross-reference: tenant-scope note (added a sub-screen-notation explainer), the shared-screen pointers, Screen 1/2/3/4 navigation references, Implementation Notes shared-screens line, and User Stories 4 and 6 (modal references → Screen 7.1 / Screen 3.2).

Final admin screen set: 1, 2, 3 (+3.1, 3.2), 4 (+4.1), 5, 6, 7 (+7.1), 8. Affiliate set: 9 (+9.1–9.4).

---

## Addendum (same day) — Detailed affiliate tab fields + missing onboarding screens (v1.5 → v1.6)

Follow-up user-directed change: give the affiliate tab screens fuller field lists, and add the affiliate onboarding/activation screens that were described in the workflows but never specced as screens.

**Changes:**

- **Expanded affiliate tab field lists**:
  - **Screen 9.2 (Promo Codes)** — split into a list-row field set (code, campaign, status, active window, discount, application method, applied/completed, conversion, revenue, commission, created date) and a per-code detail set (usage-over-time, last-used date, copy/share), plus sort/filter rules.
  - **Screen 9.3 (Payouts)** — split into an upcoming-payout panel (next date, pending amount, included bookings, £50-threshold note), a history list (period, net amount, status, completed bookings, payout date, transaction reference), and a per-payout detail (gross, reversals/refunds, net, included bookings, Stripe transfer to masked bank account, receipt).
  - **Screen 9.4 (Profile)** — grouped into account information, payout & commission (admin-controlled, read-only), and account security (affiliate-managed change-password / optional MFA); clarified editable (name, phone, language) vs read-only fields and the immutable email rule.
- **Added the affiliate onboarding/activation screen group** (previously only in the workflows): **Screen 10 — Affiliate Onboarding & Activation**, with **10.1 Set Password (activation landing)**, **10.2 Resend Activation Email**, and **10.3 Welcome / Get Started (first login)** — mirroring the provider activation flow (FR-015), backing Main Flow steps 9-12 and Alternative Flow A5.
- **Added REQ-018-038** (affiliate onboarding/activation screens), updated the tenant-scope note to include Screen 10, and corrected the REQ-018-035 wording to "Stripe transfers".

## Formatting pass (same day)

- Normalized **all 26 markdown table divider rows** in the PRD to the `| --- | --- | … |` form (exactly three dashes per column, single-pipe-plus-space delimiters; no colons or long dash runs), per the project table convention.
