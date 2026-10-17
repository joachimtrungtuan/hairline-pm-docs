# FR-019 - Promotions & Discount Management

**Module**: A-06: Discount & Promotion Management | PR-05: Financial Management & Reporting
**Feature Branch**: `fr019-promotions-discounts`
**Created**: 2025-11-11
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-019 from local-docs/project-requirements/system-prd.md; Transcriptions (admin/provider references)
**Change Request**: [CR-FR019-20261016-01 — MTG-002 quote model alignment](change-request-2026-10-16-mtg002-quote-model-alignment.md)

---

## Executive Summary

Define, approve, and apply discounts across the Hairline platform with clear governance and auditability. Admins can create platform‑wide promotions (including those that affect both provider and Hairline fees), while providers can create their own discounts. Promotions attach to individual option/date-price rows (subquotes) when a quote is sent, and a patient may enter a code on one named subquote before accepting it. Promotion terms are fixed when the quote is sent and frozen when the subquote is accepted. The system enforces usage limits and prioritization rules, and tracks usage and financial impact. This increases conversion while safeguarding provider margins and Hairline commission through an approval workflow and transparent reporting.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (P-03 overlay): See the discount on each offered subquote; enter a discount code on one named subquote before acceptance when enabled; view the final price breakdown, which is read-only after acceptance.
- Provider Platform (PR-02/PR-05): Create provider-specific discounts; review and accept/decline platform discounts; see eligible discounts during quote creation; view discount impact in reports.
- Admin Platform (A-06): Create and manage platform discounts (platform‑only or both‑fees), configure categories, dates, limits, and code rules; manage approvals and track usage; view financial impact.
- Shared Services (S-03, S-02): Notification Service for approval and status alerts; Payment/Financial service for price calculation and settlement alignment.

### Multi-Tenant Breakdown

Patient Platform (P-03 overlay):

- Input a discount code on one named subquote before acceptance (if enabled), see validation feedback.
- See discounted totals and savings; understand that only one discount applies to a subquote and that the accepted price cannot change after acceptance.

Provider Platform (PR-02/PR-05):

- Create provider discounts with type (percent/fixed/package upgrade), dates, limits.
- Accept/decline platform both‑fees discounts per program; auto‑active provider‑only discounts.
- Select applicable approved discounts for each option/date-price row within quote creation (where rules allow); the selection and its terms are fixed when the quote is sent.

Admin Platform (A-06):

- Create platform discounts: platform‑only, both‑fees, and Hairline‑only.
- Configure targets (all providers or subsets), dates, usage caps, stackability policy (single‑discount rule enforced globally).
- Manage approval workflow for both‑fees discounts; monitor provider responses.
- Track usage and financial impact with exports.

Shared Services (S-03, S-02):

- S-03 sends provider approval notifications and status updates.
- S-02 ensures correct price calculation and settlement attribution.

### Scope Boundaries

In Scope:

- Discount code definition and lifecycle (draft → active → expired), with usage limits and date windows.
- Promotion attachment to option/date-price rows when a quote is sent, patient code validation on one named subquote before acceptance, and freezing of the discounted price at acceptance; one discount per subquote.
- Promotion usage-limit reservation at acceptance, consumption at the first successful payment, and release on `Payment Window Expired` or cancellation; for auto-applied promotions, at most one reservation per sent quote, made at send, consumption at acceptance, and release when the quote expires, is withdrawn, or ends Not Selected or cancelled.
- Provider approval workflow for platform both‑fees discounts.
- Usage tracking and financial impact reporting.

Out of Scope:

- Stacking multiple discounts on a single subquote or booking (explicitly disallowed).
- Any change to the promotion or discounted price after acceptance, including code entry at checkout or booking, except the provider-fault transfer defined in FR-006.
- Payment, refund, and fund-release mechanics (FR-007, FR-007b, FR-017).
- Loyalty points and referral rewards (covered elsewhere).
- Tax/VAT calculation changes (handled by billing/finance rules).
- Affiliate-specific promo code generation, bulk assignment to affiliates, affiliate dashboard display, and affiliate payout attribution are owned by FR-018 / A-07. FR-019 owns the shared promotion engine: validation, active windows, usage limits, single-discount conflict behavior, applied/completed redemption state, and financial-impact logging.

### Entry Points

- Admin creates a platform discount in A-06; if both‑fees, providers receive approval requests.
- Provider creates a provider discount in PR-02/PR-05; becomes active per dates/limits.
- Patient enters a code (if enabled) on one named subquote before acceptance (FR-005 Alternative Flow A8); system validates it for that subquote and shows the discounted price if eligible.
- Provider sends a quote; system attaches the selected promotion and any eligible automatic promotion to each option/date-price row and copies the promotion terms into the sent quote version.

---

## Business Workflows

### Main Flow: Admin Creates Platform Discount (Both‑Fees)

Actors: Admin, Provider, System
Trigger: Admin submits a new platform discount that affects both fees
Outcome: Providers approve participation; discount becomes selectable where applicable

Steps:

1. Admin defines discount (type, value, dates, usage limit, targeted providers).
2. System saves discount as Pending Approval and notifies targeted providers.
3. Providers accept or decline; system logs responses.
4. When provider accepts, discount becomes eligible for that provider’s option/date-price rows during the active window.
5. System tracks usage and financial impact per provider.

### Alternative Flows

**A1a: Provider‑Only Discount (Reusable — Pre-Defined)**:

- Trigger: Provider creates their own discount from the standalone Promotion Detail screen (Screen 9).
- Steps: System validates inputs, persists the program with `scope = REUSABLE`, and activates per dates/limits; no approval needed.
- Outcome: Discount immediately eligible for **list-selection** during the provider's quote creation flow (FR-004 Screen 1).

**A1b: Provider‑Only Discount (Inline — On-the-Spot from Quote)**:

- Trigger: Provider opens the inline promotion creator from within FR-004 Screen 1 during quote drafting.
- Steps: Provider enters name, type, value, applies-to, and optional code in a mini-form for one FR-004 option/date-price row; system creates a new `PromotionProgram` with `scope = AD_HOC_QUOTE_BOUND`, `bound_quote_id` set to the parent quote, and `bound_quote_option_date_price_id` set to that row. Provider may toggle "Save as reusable program for future quotes" to promote the record to `scope = REUSABLE`.
- Outcome: Discount is attached through `QuoteOptionDatePrice.promotionId` and is governed by the same caps, validation, and admin-override rules as A1a. Ad-hoc records appear in FR-019 Screen 1 Hub (filterable by `scope`) and Screen 4 Portfolio.

**A2: Hairline‑Only Discount**:

- Trigger: Admin creates a Hairline‑funded discount.
- Steps: System applies the discount to the patient's price; the program is not visible to providers in selection UIs. Commission is calculated on the accepted price after the promotion, as for every discount type.
- Outcome: Both the platform commission and the provider's payout are reduced; the provider bears most of the discount. Settlement of the funding split is defined by FR-017.

**B1: Code Validation Failure**:

- Trigger: Patient/provider enters invalid/expired/reached‑limit code.
- Steps: System returns reason; prevents application.
- Outcome: No discount applied; user can retry.

**B2: Single‑Discount Rule Conflict (User‑Initiated)**:

- Trigger: Before the quote is sent (provider) or before the subquote is accepted (patient), the user manually enters or selects a second discount for an option/date-price row (subquote) that already has one.
- Steps: System blocks the new entry; prompts the user to confirm replacement or keep the existing discount. A patient's replacement applies only to the patient's selection on that subquote and never changes the provider's promotion.
- Outcome: Exactly one discount per subquote; the user's confirmed choice is applied. After acceptance no entry, selection, or replacement is accepted (Alternative Flow B4).

**B3: Single‑Discount Rule Conflict (Auto‑Applied)**:

- Trigger: When a quote is sent, two auto-applied discounts are eligible for the same option/date-price row (e.g., a Hairline-funded auto-applied program and a provider's auto-applied program).
- Steps: System silently resolves the conflict using priority order: patient-entered code > provider discount > affiliate discount. Lower-priority discount is not applied; no user prompt is shown.
- Outcome: Exactly one discount affects the patient's final price; audit records which program was applied and which was superseded. If a valid affiliate-bound code/link was already captured as the patient acquisition source, FR-019 preserves that affiliate attribution metadata for FR-018 even when a provider-side promotion wins the price-discount priority.

**C1: Hairline-Funded / Direct-Issued Code Redemption**:

- Trigger: Admin issues a Hairline-funded code (open code, segment-bound, or affiliate-distributed) and the patient enters it on one named subquote before acceptance.
- Steps: System validates the code against issuance binding (open vs recipient-bound), records the redemption against the issuing channel (e.g., affiliate id), and calculates commission on the accepted price after the promotion, as for every discount type. For affiliate-bound codes, code generation and affiliate assignment are initiated from FR-018; FR-019 receives the registered code and manages redemption lifecycle.
- Outcome: Patient receives discount; the platform commission and the provider's payout are both reduced, with the provider bearing most of the discount; affiliate (if applicable) accrues the configured incentive (see FR-018).

**A3: Automatic Promotion Attachment at Send**:

- Trigger: A provider sends a quote while an auto-applied program is active and eligible for one or more of its option/date-price rows.
- Steps: System attaches the program to every eligible option/date-price row of the sent quote and copies its terms into the sent quote version. The provider's entered price on each row stays unchanged, and the discount is shown as a separate line next to it. Rows that are not eligible receive no automatic promotion. Conflicts with another discount on the same row are resolved by Alternative Flow B3. Sending a quote carrying the automatic promotion reserves one use against the program's usage limits. A sent quote holds at most one reserved use: re-sending a new version keeps the existing reservation, creates one only if the new version newly carries the promotion, and releases it if the new version no longer carries the promotion. If the limit is already fully reserved or consumed, the promotion does not attach.
- Outcome: Each eligible row carries the automatic promotion with terms fixed at send; later edits to the program do not change the sent rows. The reserved use is consumed if a subquote of that quote is accepted, and released when the quote expires, is withdrawn, or ends Not Selected or cancelled.

**A4: Patient Applies a Code Before Acceptance**:

- Trigger: While reviewing one named subquote and before confirming acceptance, the patient enters a code (FR-005 Alternative Flow A8).
- Steps: System validates the code for that subquote only (active window, eligibility, usage limits, recipient binding). If valid, the discounted price is shown next to the provider's offered price; if invalid, the reason is shown and the offered price is unchanged. The code is recorded against the patient's selection on that subquote and is never written to the provider's promotion or quote records. Opening another subquote does not carry the code over.
- Outcome: On acceptance, the discounted price and the applied promotion are frozen into the AcceptanceEvent snapshot.

**A5: Subquote Accepted With a Promotion**:

- Trigger: The patient accepts a subquote that carries a promotion attached at send or a valid patient-entered code.
- Steps: In the same atomic step as the acceptance, the system creates one Application linked to the AcceptanceEvent, the parent quote and version, and the accepted option/date-price row, and reserves one use against the program's usage limits. For an automatic promotion attached at send, the use already reserved at send is consumed instead. Sibling subquotes marked Not Selected and competing quotes never create an Application; any use reserved for them at send is released. A patient code entered on a subquote that was not accepted is discarded.
- Outcome: The Application is in state Applied with its use reserved, or consumed for an automatic promotion; the discounted price is read from the acceptance snapshot by every later step.

**B4: Promotion Change Attempted After Acceptance**:

- Trigger: Any actor (patient, provider, or admin) tries to remove, replace, enter, or revalidate a promotion on an accepted subquote, including at checkout or booking.
- Steps: System rejects the action, leaves the Application and the AcceptanceEvent snapshot unchanged, and logs the attempt.
- Outcome: The accepted price stands. The only exception is the provider-fault transfer in FR-006 (Alternative Flow B5), which creates a new linked acceptance record; promotion handling for that case follows the post-acceptance freeze rule in General Module Rules.

---

## Screen Specifications

This module exposes **three promotion programs** under one unified governance model:

1. **Admin-via-Provider** — Admin defines a campaign that affects both Hairline and provider fees; targeted providers must opt-in before the code becomes selectable on their quotes.
2. **Provider Self-Created** — Provider defines a discount on their own quotes; no admin approval required.
3. **Hairline-Funded & Direct-Issued** — Admin defines a Hairline-only discount that is issued directly to patients (open-entry code, patient-segment-bound, affiliate-distributed, or individually issued); providers are not involved in approval.

For every program type, commission is calculated on the accepted price after the promotion, so a discount reduces both the provider's payout and Hairline's commission, and the provider bears most of it. The funding model identifies who creates, approves, and governs a program; it does not keep commission on the price before the promotion.

All three program types share a single `PromotionProgram` entity (see Key Entities) and are managed through a unified screen system with type-aware filters, forms, and analytics. Admin retains override authority on every program (pause, revoke adoption) and may record a refund through FR-017 regardless of program type. No actor, including admin, may void, remove, or change the promotion on an accepted subquote (Alternative Flow B4).

### Screen Inventory

| # | Platform | Screen | Replaces |
|---|----------|--------|----------|
| 1 | Admin | Promotion Program Hub | Expands prior Screen 4 (Discount Code Catalog) |
| 2 | Admin | Promotion Detail (Create/Edit) | Expands prior Screen 1 |
| 3 | Admin | Provider Adoption Manager | New |
| 4 | Admin | Provider Promotion Portfolio | New (scope expansion — see Notes on Screen 4) |
| 5 | Admin | Hairline-Funded & Direct-Issued Codes Manager | New |
| 6 | Admin | Promotion Analytics & Applications | New (consolidates prior client-mentioned "Applied" + "Completed" screens) |
| 7 | Provider | Admin Campaigns (Inbox + Adoptions) | Splits prior Screen 2 |
| 8 | Provider | My Promotions (List) | Splits prior Screen 2 |
| 9 | Provider | Promotion Detail (Create/Edit) — Provider | Splits prior Screen 2 |
| 10 | Provider | Provider Promotion Analytics & Applications | New |
| 11 | Patient | Apply Discount Before Acceptance | Retains prior Screen 3 (minor additions) |

---

### Admin Platform Screens (A-06)

#### Screen 1: Admin — Promotion Program Hub

**Purpose**: Master catalog of every promotion program across the platform, regardless of program type, with type-aware filters and row actions.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Code / keyword search | text input | No | Search by code text, program name, or keyword | Min 2 chars; 500ms debounce; case-insensitive fuzzy match |
| Filter: Program Type | multi-select | No | Admin-via-Provider, Provider Self-Created, Hairline-Funded & Direct-Issued | OR within field |
| Filter: Scope | multi-select | No | Reusable, Ad-Hoc Quote-Bound | Applies primarily to Provider Self-Created programs (see Screen 9 modes) |
| Filter: Status | multi-select | No | Draft, Pending Approval, Active, Paused, Expired, Archived | OR within field |
| Filter: Funding Model | multi-select | No | Both Fees, Hairline Only, Provider Only | Derived from program definition |
| Filter: Provider Participation | dropdown | No | All / specific provider | Provider list from DB; exact match |
| Filter: Date Range | date range picker | No | Active-window overlap | Start/end overlap logic |
| Filter: Usage | range | No | Redeemed count threshold | Min-Max range |
| Filter: ROI | dropdown | No | Admin-defined ROI tier | Exact match |
| Result Count | label | Yes | Number of matched programs | Updates after every search/filter operation |
| Results Table | table | Yes | Displays matched programs with row actions | Columns fixed for MVP |

**Results Table Columns**:

| Column | Meaning | Notes |
|--------|---------|-------|
| Code / Program Name | Code text (or program name when no code) | Primary identifier |
| Program Type | Admin-via-Provider / Provider Self-Created / Hairline-Funded & Direct-Issued | Type badge |
| Owner | Admin user or Provider entity that created the program | |
| Funding Model | Both Fees / Hairline Only / Provider Only | Derived |
| Participating Providers | `All Providers`, provider count, or `N/A` for Direct-Issued | |
| Status | Draft / Pending Approval / Active / Paused / Expired / Archived | Lifecycle state |
| Active Window | Start and end dates | |
| Usage | Reserved plus redeemed count vs limit | |
| ROI Tier | Admin-defined band | `Not yet calculated` until data exists |
| Last Updated | Most recent mutation timestamp | Default descending sort |

**Row Actions**:

- View Detail (opens Screen 2)
- Pause / Resume
- Archive
- View Adoptions (Screen 3) — only for Admin-via-Provider programs
- View Applications (Screen 6, Applications tab pre-filtered to the program)

**Business Rules**:

- All three program types appear in this hub; the Program Type filter narrows the view.
- Provider Self-Created programs appear here so admins can monitor and intervene; admins may pause or archive any program but typically do not edit provider-owned definitions (see Screen 4 Notes).
- Search, filter, result count, and reset behavior must stay aligned with FR-022 control standards.
- Access restricted to authorized admin roles (RBAC enforced per FR-031).

**Acceptance Criteria**:

1. Given the admin opens the Hub, when the screen loads, then the system shows all program types in one list with the default descending Last Updated sort and the result count for the default query.
2. Given the admin applies any combination of Program Type, Status, Funding Model, Provider Participation, Date Range, Usage, and ROI filters, then the catalog returns only rows satisfying all active filters and updates the result count.
3. Given the admin selects a row, then the system opens Screen 2 for that program without losing catalog context.
4. Given the admin triggers Pause on an Active program row, then the program lifecycle transitions to Paused, all existing redemptions remain intact, the program is not attached to newly sent quotes and does not validate new patient codes, and option/date-price rows already sent keep the terms copied at send.

**Notes**:

- Search and filter field definitions are co-owned with FR-022. Any change must be updated in both FR-019 and FR-022.

---

#### Screen 2: Admin — Promotion Detail (Create / Edit)

**Purpose**: Type-aware form to define and govern a promotion program across its full lifecycle.

**Common Data Fields** (all program types):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Program Name | text | Yes | Internal name for the campaign | 3–120 chars |
| Description | textarea | No | Internal notes / patient-facing copy | ≤ 1000 chars |
| Discount Type | select | Yes | Percentage / Fixed amount / Package upgrade | Must be one of allowed types |
| Value | number | Yes | Discount value | Range per type; max configurable |
| Applies To | select | Yes | Whole price / Treatment cost only / Travel cost only / Other component | Per HairlineApp Part 1 (partial-scope discounts) |
| Code(s) | text or chip list | Conditional | One or many codes per program | Format rules; uniqueness enforced |
| Application Mode | select | Yes | Auto-applied / Code-only entry | Per Admin Part 1 transcription |
| Start / End Date | datetime | Yes | Active window | End ≥ Start |
| Total Usage Limit | number | No | Total redemptions allowed across the program | ≥ 0; blank = unlimited |
| Per-User Usage Limit | number | No | Per-patient cap | ≥ 0; blank = unlimited |
| Lifecycle State | controlled | Yes | Draft → Active → Paused → Expired → Archived | Forward transitions only |

**Type-Specific Fields**:

| Field Name | Applies To | Description |
|------------|-----------|-------------|
| Funding Model | All | Both Fees (Admin-via-Provider only) / Provider Only (Provider Self-Created only) / Hairline Only (Hairline-Funded only) — auto-set by program type |
| Target Providers | Admin-via-Provider | Multi-select: All Providers, by region, or explicit list |
| Approval Routing | Admin-via-Provider | Default vs custom approver per provider entity |
| Auto-Decline Window | Admin-via-Provider | Days before unresponded approval auto-declines |
| Issuance Channel | Hairline-Funded & Direct-Issued | Open code / Affiliate-bound (links to FR-018) / Patient-segment-bound / Individually-issued |
| Recipient Binding | Hairline-Funded & Direct-Issued | Affiliate ID, segment definition, or recipient list (when channel is bound) |
| Bulk Generate Codes | Hairline-Funded & Direct-Issued | Generate N unique codes for distribution; quantity 1–10,000 |

**Audit Trail Panel**:

- All state changes, edits, approvals, and override actions are listed in chronological order with actor, timestamp, and reason.

**Business Rules**:

- `Funding Model` is derived from `Program Type` and cannot be set independently.
- For Admin-via-Provider, saving transitions the program to `Pending Approval` and notifies targeted providers (S-03).
- Hairline-Funded programs do not appear in provider selection UIs (per Provider Part 2 L3–8).
- `Application Mode = Auto-applied` is only allowed for programs with `Funding Model = Hairline Only` or `Provider Only` and explicit eligibility rules (cannot be auto-applied across multiple providers without consent). Auto-applied programs attach when a quote is sent (Alternative Flow A3).
- A `Fixed amount` value carries a currency. When the program is attached to a sent quote, the discount is expressed in the quote currency and that amount is part of the terms fixed at send.
- Bulk upload / bulk edit available for campaign management.

**Acceptance Criteria**:

1. Given the admin creates an Admin-via-Provider program and submits, then the program enters Pending Approval and the targeted providers receive S-03 notifications.
2. Given the admin creates a Hairline-Funded program with `Issuance Channel = Open code` and a single code, when the program is published, then the code is immediately redeemable by any patient on a named subquote before acceptance and the program does not appear in any provider's adoption inbox.
3. Given the admin edits the Value of a Paused program and republishes, then the new value applies only to quotes sent and patient codes validated from that point forward; quotes already sent keep the terms copied at send, and prior redemptions retain their original values in audit.
4. Given the admin sets `Application Mode = Auto-applied` on an Admin-via-Provider program and attempts to save, then the system rejects the submission with an inline validation error: "Auto-applied is not permitted for Both-Fees programs."

**Notes**:

- The form must hide irrelevant sections based on Program Type to reduce cognitive load (e.g., no Approval Routing for Hairline-Funded).
- `Application Mode` options differ by Program Type by design: admin programs use `Auto-applied / Code-only` (no list-selection because admin programs are not shown in a provider's quote-creation picker — they are adopted via the approval workflow and then selected from the provider's adopted campaigns list); provider programs use `List-selection / Code-only / Either`.

---

#### Screen 3: Admin — Provider Adoption Manager

**Purpose**: For a given Admin-via-Provider program, show every targeted provider's adoption status and let admins override decisions.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Program Header | panel | Yes | Program name, dates, value, funding model | Read-only summary |
| Provider Row | table row | Yes | One row per targeted provider | |

**Adoption Row Columns**:

| Column | Meaning |
|--------|---------|
| Provider | Provider name + region |
| Status | Pending / Accepted / Declined / Auto-Declined / Revoked-by-Provider / Revoked-by-Admin |
| Decided At | Timestamp of last decision |
| Decided By | Provider user or admin user (for overrides) |
| Comment | Optional comment from the deciding actor (≤ 500 chars) |
| Redemptions | Count of redemptions on this provider's quotes under this program |
| Admin Actions | Re-invite / Force-Revoke / Mark Exempt |

**Business Rules**:

- Force-Revoke immediately removes the program from the provider's quote-creation selection list; in-flight quotes with the program already applied are preserved.
- Re-invite resets the provider's status from Declined or Auto-Declined back to Pending and re-sends the S-03 notification.
- All admin overrides are logged with mandatory reason text in the audit trail.

**Acceptance Criteria**:

1. Given a provider has Status = Accepted, when the admin triggers Force-Revoke with reason, then the provider's status changes to Revoked-by-Admin and the program disappears from that provider's quote-creation list within 5 seconds.
2. Given the program's Auto-Decline Window elapses without a provider decision, then the provider's status updates to Auto-Declined and is visible in this manager.

---

#### Screen 4: Admin — Provider Promotion Portfolio

**Purpose**: Per-provider drill-down showing every promotion record tied to that provider — both admin programs they have adopted and their self-created programs — so admins can assess each provider's promotional behaviour and impact.

**Data Fields**:

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| Provider Header | panel | Yes | Provider name, region, contact, adoption-rate KPIs |
| Filter: Record Type | multi-select | No | Adopted-Admin / Self-Created |
| Filter: Status | multi-select | No | Draft / Active / Paused / Expired / Archived |
| Filter: Date Range | date range picker | No | Active-window overlap |
| Results Table | table | Yes | Promotion records for this provider |

**Results Table Columns**:

| Column | Meaning |
|--------|---------|
| Program Name | Internal name |
| Record Type | Adopted-Admin / Self-Created |
| Funding Model | Both Fees / Provider Only |
| Status | Lifecycle state |
| Active Window | Start–End |
| Redemptions | Count under this provider |
| Revenue Impact | Total discount issued (Hairline portion + provider portion split) |
| Row Action | Open program detail (Screen 2 in read-only mode for self-created) |

**KPI Header Strip**:

- Adoption Rate: % of admin programs offered that this provider accepted
- Self-Created Active Count
- Total Redemptions (last 30 / 90 / 365 days)
- Total Discount Issued (currency)

**Business Rules**:

- Admin may open Screen 2 in read-only mode for provider self-created programs; editing is reserved for the provider unless an override is needed (governance action, logged in audit).
- Admin may pause or archive any provider self-created program via row action with mandatory reason text.

**Notes — Scope Expansion**:

- Per client transcription (Admin Part 1 L295–300), the client originally stated admin would *"never going to pick them or change them or amend them in reality"* for provider self-created discounts. This portfolio screen **deliberately extends beyond that original scope** to give admins governance visibility and override authority across the entire promotion system. Recorded in Change Log v1.4.

---

#### Screen 5: Admin — Hairline-Funded & Direct-Issued Codes Manager

**Purpose**: Specialized manager for the third program type — codes that Hairline funds and issues directly through open distribution, patient segments, or affiliate channels.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Program Selector | dropdown | Yes | Choose a Hairline-Funded program | From Screen 1 filtered list |
| Issuance Channel | label | Yes | Open / Affiliate-bound / Segment-bound / Individually-issued | From program definition |
| Codes Table | table | Yes | One row per code (or per recipient for bound channels) | |
| Bulk Generate | action | No | Generate N unique codes | Per program total-limit |
| Bulk Revoke | action | No | Revoke selected codes | Mandatory reason |
| Export | action | No | CSV / XLSX export of code list with redemption status | |

**Codes Table Columns**:

| Column | Meaning |
|--------|---------|
| Code | Unique code string |
| Recipient Binding | Affiliate name / Segment name / Patient identifier / `Open` |
| Issued At | Generation timestamp |
| Issued By | Admin user |
| Redemption Status | Unused / In-Progress (use reserved by an accepted subquote) / Redeemed (first successful payment) / Revoked / Expired |
| Redeemed By | Patient identifier when redeemed |
| Redeemed At | Timestamp |
| Discount Issued | Currency amount |

**Business Rules**:

- Open codes have one code that any eligible patient may use until the total usage limit is reached.
- Affiliate-bound codes integrate with FR-018; FR-018 owns generation and one-affiliate-per-code assignment, while FR-019 owns validation and redemption state. Redemptions accrue incentive to the linked affiliate.
- Segment-bound codes validate the patient against the segment definition at entry time.
- Individually-issued codes are single-use and bound to a specific patient identifier.
- Revoking a code stops it from validating on any subquote not yet accepted. A use already reserved by an accepted subquote (`In-Progress`) stays frozen with the acceptance and is not cancelled by the revoke.

**Acceptance Criteria**:

1. Given the admin selects a Hairline-Funded program with channel = Affiliate-bound and triggers Bulk Generate for 50 selected affiliates, when generation completes, then 50 unique codes are created, each code is bound to exactly one affiliate, and each appears in the table with status = Unused.
2. Given a patient enters an Affiliate-bound code on a named subquote and accepts it, when the first payment succeeds, then the corresponding row updates to Redeemed and the affiliate's incentive accrual (per FR-018) is triggered.

---

#### Screen 6: Admin — Promotion Analytics & Applications

**Purpose**: Combined operational + analytical surface that consolidates the prior client-mentioned "Applied discounts" and "Completed discounts" screens (Admin Part 1 L333–344) into one place with two complementary tabs.

##### Tab 1: Overview (Analytics)

**KPI Cards**:

- Active Programs (count by program type)
- Total Redemptions (last 7 / 30 / 90 / 365 days)
- Total Discount Value Issued (Hairline portion + provider portion + total)
- Redemption Funnel: Issued → Code Entered → Validated → In-Progress → Completed
- ROI by Program Type
- Top 10 Programs by Redemptions
- Top 10 Programs by Discount Value

**Filters**: Date range, program type, funding model, provider, region.

##### Tab 2: Applications (Redemption Log)

One row per redemption event with the full state lifecycle preserved.

**Columns**:

| Column | Meaning |
|--------|---------|
| Redemption ID | Unique identifier |
| Code | Code redeemed (or auto-applied marker) |
| Program | Program name + type |
| State | **Applied** (created at subquote acceptance; one use reserved) vs **Completed** (first successful payment; use consumed) — distinct states per client transcription |
| Patient | Patient identifier |
| Provider | Provider on the accepted subquote |
| Quote / Subquote / Acceptance / Booking ID | Links to the parent quote and version, the accepted option/date-price row, the AcceptanceEvent, and the booking |
| Source | Provider-selected at send, automatic at send, or patient-entered code |
| Discount Value | Amount in the quote currency, read from the acceptance snapshot |
| Funding Split | Hairline portion / Provider portion |
| Applied At | Timestamp of state = Applied |
| Completed At | Timestamp of state = Completed (blank if not yet) |
| Status | Active / Voided / Superseded / Reversed / Refunded |
| Admin Actions | View Detail; Reverse and Refund on Completed rows only |

**Business Rules**:

- The two-state distinction (Applied vs Completed) is preserved per client request (Admin Part 1 L341–344). Applied = the subquote carrying the promotion has been accepted and one use is reserved; Completed = the first payment for that booking has succeeded and the use is consumed.
- Voided is set only by the system, when the booking reaches `Payment Window Expired` or is cancelled; the reserved use is then released. For an automatic promotion, the use consumed at acceptance returns to the usage limit when the row is Voided before the first payment. Superseded is set only by the system when a provider-fault transfer replaces the accepted record. There is no admin Void action.
- Reverse / Refund actions are logged with mandatory reason and integrate with FR-017 (Billing & Finance) for monetary reconciliation. They never change the accepted price or the AcceptanceEvent snapshot.
- Drilling from a KPI card on the Overview tab filters the Applications tab accordingly.

**Acceptance Criteria**:

1. Given an accepted subquote with an Applied redemption, when the first payment for the booking succeeds, then the redemption row transitions from State = Applied to State = Completed, the reserved use is consumed, and the change is reflected in Overview KPIs within 5 seconds.
2. Given an admin triggers Refund on a Completed redemption with reason, then the row Status updates to Refunded, the audit log captures actor/time/reason, and FR-017 receives a reconciliation event.
3. Given an Applied redemption, when its booking reaches `Payment Window Expired` or is cancelled, then the row Status becomes Voided, the reserved use is released, and the AcceptanceEvent snapshot is unchanged.
4. Given an admin opens an Applied redemption, then no void, remove, replace, or price-change action is offered.

---

### Provider Platform Screens (PR-02 / PR-05)

#### Screen 7: Provider — Admin Campaigns

**Purpose**: Single hub for admin-originated campaigns offered to this provider, covering both pending invitations and current adoptions.

**Tabs**:

- **Pending** — Campaigns awaiting accept / decline decision
- **Active** — Accepted campaigns currently in their active window; revoke control available
- **Past** — Declined, Auto-Declined, Revoked, or Expired campaigns

**Campaign Card / Row Fields**:

| Field | Description |
|-------|-------------|
| Program Name | From admin definition |
| Description | Patient-facing copy |
| Discount Type / Value | e.g. "40% off" |
| Active Window | Start–End |
| Financial Impact Preview | Estimated impact on provider revenue based on recent booking volume |
| Decision Buttons (Pending tab) | Accept / Decline with optional comment (≤ 500 chars) |
| Revoke Adoption (Active tab) | Removes the program from this provider's quote-creation list |
| Decision Timestamp | When the provider decided |

**Business Rules**:

- All decisions logged with timestamp and user (Provider Part 2 L11–14).
- Revoking adoption does not affect quotes that already have the program applied; only new selections are blocked.
- Auto-Decline triggers if the Auto-Decline Window (Screen 2) elapses without a decision.

**Acceptance Criteria**:

1. Given a Pending campaign is shown, when the provider clicks Accept and confirms, then the campaign moves to the Active tab and becomes selectable in quote creation per FR-004 within 5 seconds.
2. Given an Active campaign, when the provider clicks Revoke Adoption with reason, then the campaign moves to Past with state = Revoked-by-Provider and is no longer offered in quote creation.

---

#### Screen 8: Provider — My Promotions (List)

**Purpose**: List view of every provider self-created promotion.

**Filter Bar**: Status (Draft / Active / Paused / Expired / Archived), date range, keyword search.

**Results Table Columns**:

| Column | Meaning |
|--------|---------|
| Promotion Name | Internal name |
| Code | Code text (or `—` if none) |
| Type / Value | e.g. "Percentage / 15%" |
| Applies To | Whole price / Treatment cost / Travel cost / Other |
| Active Window | Start–End |
| Status | Lifecycle state |
| Redemptions | Count |
| Savings Issued | Currency total |
| Row Actions | Edit / Pause / Resume / Archive / View Applications (links to Screen 10 pre-filtered) |

**Business Rules**:

- Provider may have an arbitrary number of self-created promotions concurrently active, subject to the platform's single-discount-per-booking rule at redemption time.
- Code uniqueness enforced platform-wide (cannot collide with admin codes or other providers' codes).

---

#### Screen 9: Provider — Promotion Detail (Create / Edit)

**Purpose**: Form for the provider to create or edit a self-created promotion. The screen is reachable through **two entry modes**, which together cover both of the patterns described in FR-004 Screen 1 (Quote Creation):

- **Mode 1 — Standalone (from PR-02 / PR-05 navigation):** Provider creates a reusable promotion ahead of time. `scope = REUSABLE`. The promotion is selectable from the list on FR-004 Screen 1 (Promotion field) for any future quote.
- **Mode 2 — Inline (modal opened from FR-004 Screen 1 during quote drafting):** Provider creates an on-the-spot promotion for one option/date-price row. `scope = AD_HOC_QUOTE_BOUND`, with `bound_quote_id` retaining parent-quote containment and `bound_quote_option_date_price_id` identifying the only row that may apply it. A "Save as reusable program for future quotes" toggle, when enabled, promotes the record to `scope = REUSABLE` on submit and clears both bindings.

Both modes use the same form schema below; mode-specific behaviour is noted in the rules.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Promotion Name | text | Yes | Display name | 3–120 chars |
| Description | textarea | No | Patient-facing copy | ≤ 1000 chars |
| Discount Type | select | Yes | Percentage / Fixed amount / Package upgrade | Per policy caps |
| Value | number | Yes | Discount value | Per type rules |
| Applies To | select | Yes | Whole price / Treatment cost / Travel cost / Other | |
| Code | text | **Optional** | Optional code for marketing distribution | Format rules; uniqueness platform-wide |
| Application Mode | select | Yes | List-selection during quote (default) / Code-only / Either | Code-only requires Code field |
| Start / End Date | datetime | Yes | Active window | Mode 1: end ≥ start. Mode 2: defaults to the active window of the bound quote |
| Total Usage Limit | number | No | Total redemptions | ≥ 0; blank = unlimited. Mode 2 forces total limit = 1 unless "Save as reusable" is toggled |
| Per-User Usage Limit | number | No | Per-patient cap | ≥ 0; blank = unlimited |
| Save as reusable (Mode 2 only) | toggle | No | Promote ad-hoc record to a reusable program after this quote | When ON, `scope` becomes `REUSABLE` on submit |

**Business Rules**:

- The **Code field is optional** per a deliberate scope decision. The client transcription (Provider Part 2 L27–33) stated codes are not relevant for provider self-created discounts since providers select them from a list during quote creation. This FR retains the field as **optional** so providers may also issue code-based promotions for marketing distribution (e.g., flyer codes, partner promos). Default Application Mode is `List-selection during quote`.
- **Mode 2 ad-hoc records** are scoped to a single quote and are not shown in the list-selection picker on other quotes' creation screens. They remain visible to admin in Screen 1 Hub (Scope filter = Ad-Hoc Quote-Bound) and Screen 4 Portfolio.
- Free-text "promotion note" entries are **not supported**: every discount applied to an option/date-price row must correspond to a structured `PromotionProgram` record (Mode 1 or Mode 2). FR-004's legacy `promotionNote` field is removed in FR-004 v1.8.
- Funding Model is fixed at `Provider Only` and is not user-editable.
- No admin approval required for activation in either mode.
- A promotion selected on an option/date-price row may be changed only while the quote is drafted or revised in FR-004 before acceptance. Its terms are copied into the sent quote version when the quote is sent, and a promotion can apply only to a row it was attached to at send.

**Acceptance Criteria**:

1. Given the provider saves a Mode 1 (standalone) promotion with no Code and Application Mode = List-selection, then the promotion is available for list-selection during FR-004 Screen 1 quote creation within its active window.
2. Given the provider saves a Mode 1 promotion with a Code and Application Mode = Code-only, then the promotion is not shown in the quote-creation selection list but is redeemable when the patient enters the code on a named subquote of that provider's quote before acceptance.
3. Given the provider opens the inline modal for an FR-004 option/date-price row and saves an ad-hoc promotion without enabling "Save as reusable", then a new `PromotionProgram` with `scope = AD_HOC_QUOTE_BOUND` is created, both binding IDs are set, that row's `promotionId` is set, and the record is not offered on any other option/date-price row's selection list.
4. Given the provider saves a Mode 2 ad-hoc promotion with "Save as reusable" enabled, then `scope = REUSABLE` is recorded and the promotion becomes selectable on future quotes within its active window.
5. Given an ad-hoc promotion bound to one option/date-price row, when any request tries to apply it to another row or another quote, then the system rejects the request with a clear reason and no row price changes.

**Notes — Scope Note**:

- Retaining the optional Code field for provider self-created promotions is an extension beyond the client transcription. Recorded in Change Log v1.4.
- The Mode 1 / Mode 2 split aligns FR-019 with FR-004's existing `select/text` Promotion field on Quote Creation (FR-004 Screen 1). The unstructured free-text path (`quote.promotionNote`) is removed in FR-004 v1.8 in favour of structured Mode 2 ad-hoc records. Recorded in Change Log v1.5.

---

#### Screen 10: Provider — Promotion Analytics & Applications

**Purpose**: Provider-scoped mirror of Screen 6, covering both the provider's self-created promotions and admin campaigns they have adopted.

##### Tab 1: Overview (Analytics)

- Redemptions (last 7 / 30 / 90 / 365 days)
- Savings Issued (total + per-program)
- Conversion Lift vs baseline (per program where measurable)
- ROI Estimate per program
- Adopted-Admin vs Self-Created split
- Top performing programs

##### Tab 2: Applications (Quote / Case Manager)

One row per redemption tied to this provider's quotes / treatment cases.

**Columns**:

| Column | Meaning |
|--------|---------|
| Redemption ID | Unique identifier |
| Code / Program | Code or program name |
| State | Applied / Completed (preserves admin-side semantics) |
| Patient | Patient identifier |
| Quote / Case ID | Link to FR-004 / FR-010 entity |
| Discount Value | Currency amount |
| Applied At / Completed At | Timestamps |
| Row Actions | View Quote / View Case |

**Business Rules**:

- Screen 10 offers no remove or replace action. A provider changes the promotion on an option/date-price row only while drafting or revising the quote in FR-004 before acceptance (Screen 9 Business Rules); once the subquote is accepted, the promotion is frozen in the AcceptanceEvent snapshot.
- The provider cannot reverse a Completed redemption; that authority sits with admin (Screen 6).

**Acceptance Criteria**:

1. Given an Applied redemption on an accepted subquote, when the provider opens the row, then no remove, replace, or price-change action is available and the discount shown matches the acceptance snapshot.

---

### Patient Platform Screens (P-03 overlay)

#### Screen 11: Patient — Apply Discount Before Acceptance

**Purpose**: Validate and apply a single discount code on one named subquote while the patient reviews it, before acceptance (FR-005 Screen 2, Alternative Flow A8).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Code input | text | No | Optional discount code for the named subquote | Format rules; 1 active code at a time on that subquote; not available after acceptance |
| Price breakdown | panel | Yes | Provider's offered price, discount line, discount scope, totals | Provider price shown as entered; discount shown as a separate line |
| Discount Scope label | label | Yes | Shows which fee component the discount applies to (e.g., "Applies to transplant cost only") | Per HairlineApp Part 1 L156–158 |

**Business Rules**:

- One discount per subquote; entering a new code prompts the patient to confirm replacement of the current discount on that subquote.
- The code applies only to the named subquote and is not carried to another subquote. It is recorded against the patient's selection and is never written to the provider's promotion or quote records.
- Validation occurs when the code is entered and again when the patient confirms acceptance. On acceptance, the discounted price is frozen into the AcceptanceEvent snapshot.
- No code entry, removal, or replacement is available after acceptance, including at checkout or payment; payment screens show the frozen accepted price.
- Clear feedback for invalid / expired / limit-reached / segment-mismatched codes.
- Where a discount applies only to a sub-component (e.g., treatment cost, not travel), the breakdown explicitly shows which line is reduced.

**Acceptance Criteria**:

1. Given a patient enters a valid code, when validation succeeds, then the price breakdown updates within 1 second and shows the discount scope label.
2. Given a patient enters a code on a subquote that already has a discount, when the patient confirms replacement, then the previous discount is replaced on the patient's selection for that subquote only, the provider's promotion record is unchanged, and audit records both events.
3. Given a patient applies a valid code on subquote A, when the patient opens subquote B, then subquote B shows its own offered price without the code.
4. Given a patient has accepted a subquote, when the patient reaches checkout or payment, then no code input is shown, the price equals the acceptance snapshot, and any request to apply a code is rejected.

---

## Success Criteria

### Patient/Provider Experience Metrics

- SC-001: 95% of valid codes validate within 1 second on subquote review before acceptance.
- SC-002: 0% of accepted subquotes carry more than one discount (enforced at all steps).

### Admin/Operations Metrics

- SC-003: 95% of provider approval responses are processed and reflected within 5 seconds of submission.
- SC-004: Discount usage and impact reports export in ≤ 10 seconds for 95th percentile.

### Financial/Compliance Metrics

- SC-005: 100% of applied discounts have audit entries (who, when, what, amount, context).
- SC-006: Misapplied discounts detected and corrected to ≤ 0.1% of bookings monthly.

### Reliability Metrics

- SC-007: 99.9% monthly uptime for validation and calculation services.
- SC-008: Zero data loss for discount definitions and usage records.

---

## Business Rules

### General Module Rules

- Single‑discount rule enforced globally. Conflict resolution depends on how the conflict arises: (a) **user-initiated** — system prompts the user to confirm replacement (see Alt Flow B2); (b) **auto-applied** — system silently resolves using priority order: patient-entered code > provider discount > affiliate discount, with no user prompt (see Alt Flow B3).
- Promotion terms are fixed at send. When a quote is sent, the terms of each option/date-price row's promotion (type, value, applies-to, funding model, and the discount amount in the quote currency) are copied into the sent quote version. Later edits, pausing, expiry, or archiving of the program do not change a sent row.
- Active dates, eligibility, and usage limits are checked when a promotion is attached to a row at send and when a patient code is validated before acceptance.
- Auto-applied programs attach at send to every eligible option/date-price row. The provider's entered price stays unchanged and the discount is shown separately.
- A promotion applies only to an option/date-price row it was attached to at send, or to the one named subquote on which the patient entered a code. Any other application is rejected.
- Promotion usage lifecycle for provider-selected promotions and patient-entered codes: one use is reserved when the subquote is accepted, consumed when the first payment succeeds, and released when the booking reaches `Payment Window Expired` or is cancelled; when an admin revives a `Payment Window Expired` booking (FR-006), the use is re-reserved, and the revive is rejected if the usage limit is exhausted.
- Promotion usage lifecycle for auto-applied promotions: sending a quote carrying the promotion reserves one use. A sent quote holds at most one reserved use: re-sending a new version keeps the existing reservation, creates one only if the new version newly carries the promotion, and releases it if the new version no longer carries the promotion. The reservation is released when the quote expires, is withdrawn, or ends Not Selected or cancelled, and consumed when a subquote of that quote is accepted. If the booking then reaches `Payment Window Expired` or is cancelled before the first payment, the consumed use returns to the usage limit. When an admin revives a `Payment Window Expired` booking (FR-006), the use is taken again if the limit still has room; if it has no room, the revive is rejected, because the accepted price already includes the promotion and cannot change.
- Usage limits count active reservations plus consumed uses, so a limit can never be exceeded. A promotion whose limit is fully reserved or consumed does not attach at send and fails code validation.
- Rows that are not accepted (sibling subquotes marked Not Selected, competing quotes, expired or withdrawn quotes) never create an Application; any use reserved for them at send by an auto-applied promotion is released.
- Post-acceptance freeze: after acceptance, the promotion and discounted price of the accepted subquote are frozen in the AcceptanceEvent snapshot. No removal, replacement, code entry at checkout or booking, price-changing revalidation, or admin void is allowed. The only exception is the provider-fault transfer in FR-006 (Alternative Flow B5): the original Application is kept as history and marked Superseded, and any promotion on the replacement is recorded as a new Application linked to the new admin-authored acceptance record; a use already reserved or consumed carries over and is not counted twice. Money handling for that transfer is defined by FR-006, FR-007, FR-007b, and FR-017.
- Commission is calculated on the accepted price after the promotion, in the quote currency, read from the acceptance snapshot (FR-015, FR-029). This applies to every discount type, including Hairline-funded programs; no program keeps commission on the price before the promotion. Settlement of the funding split between Hairline and the provider is defined by FR-017.
- All discount creations, approvals, applications, and removals are auditable.

### Data & Privacy Rules

- Display only non‑sensitive discount info to patients; provider/Hairline cost splits remain internal.
- Financial records and discount artifacts retained for ≥ 7 years; takedowns handled by archival, not deletion.
- Access governed by RBAC; only authorized roles can create/approve/apply discounts beyond self‑service code entry.

### Admin Editability Rules

Editable by Admin:

- Discount categories, code format policy, max value caps, and campaign dates.
- Targeting rules (all providers vs. subsets) and approval routing.
- Notification templates for approvals and status.

Fixed in Codebase (Not Editable):

- Single‑discount rule and priority order.
- Promotion terms fixed at send and frozen at acceptance.
- Calculation order of operations (base → discounts → taxes/fees).

Configurable with Restrictions:

- Max discount value thresholds per policy and region.
- Auto‑decline window for unresponded provider approvals.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- PR-02: Inquiry & Quote Management – discount selection during quote creation.
- P-03: Booking & Payment – read the frozen discounted price from the acceptance snapshot; the first successful payment consumes the reserved use.
- A-05: Billing & Financial Reconciliation – reflect Hairline vs provider shares.
- S-03: Notification Service – provider approvals and status updates.
- S-02: Payment/Financial Service – price calculation and settlement.
- FR-004: Quote Submission & Management – Screen 9 Mode 1/Mode 2 entry points live within FR-004 Screen 1; `QuoteOptionDatePrice.promotionId`, parent/row binding provenance, the copy of promotion terms into the sent quote version, and removal of legacy `promotionNote` are co-owned contracts.
- FR-005: Quote Comparison & Acceptance – patient code entry on one named subquote before acceptance (Alternative Flow A8); the AcceptanceEvent snapshot freezes the discounted price and is the source each Application links to.
- FR-006: Booking & Scheduling – `Payment Window Expired` and cancellation release the reserved use; the audited admin revive re-reserves it; the provider-fault transfer (Alternative Flow B5) is the only post-acceptance exception.
- FR-015 / FR-029: Provider Management and Payment System Configuration – commission base is the accepted price after the promotion.
- FR-018: Affiliate Management – Affiliate-bound code redemptions accrue incentive to the linked affiliate; FR-019 triggers the incentive event consumed by FR-018.
- FR-022: Search & Filtering – Screen 1 search/filter controls are co-owned with FR-022; any field change must be updated in both FRs.
- FR-031: Admin Access Control & Permissions – all admin create/approve/override actions are RBAC-gated per FR-031 role definitions.
- FR-010: Treatment & Recovery Case Management – Screen 10 Applications tab links redemptions to FR-010 treatment case entities; treatment changes never change the accepted promotion.

### External Dependencies (APIs, Services)

- Email/Push providers (via S-03) for approval/status notifications.

### Data Dependencies

- Provider catalog and identifiers for targeting.
- Booking/quote entities with price components for calculation.

---

## Assumptions

### User Behavior Assumptions

- Providers respond to approval requests within 3 business days.
- Patients enter codes only while reviewing a subquote before acceptance.

### Technology Assumptions

- The subquote review and acceptance flow (FR-005 Screen 2) exposes the only patient code input surface.
- Calculation service supports deterministic rounding and currency rules.

### Business Process Assumptions

- Finance defines regional caps and policy; legal approves terms for promotions.

---

## Implementation Notes

### Technical Considerations

- Calculation pipeline: base price → discount (single) → taxes/fees; idempotent validation.
- Create the Application and reserve usage atomically with the subquote acceptance. Payment and booking read the discounted price from the acceptance snapshot and never revalidate or recompute it.
- Audit trail for all state changes; soft‑disable discounts without data loss.

### Integration Points

- Admin UI ↔ Promotion service: CRUD, approvals, targeting.
- Provider UI ↔ Promotion service: approvals, provider discounts.
- Quote send ↔ Promotion service: attach selected and eligible automatic promotions and copy their terms.
- Subquote acceptance ↔ Promotion service: validate any patient code, reserve usage, and create the Application.
- Payment ↔ Promotion service: consume the reserved use on the first successful payment; booking `Payment Window Expired` or cancellation releases it.

### Scalability Considerations

- Cache active discounts and targeting; invalidate on updates.
- Paginated usage reports; background generation for long ranges.

### Security Considerations

- RBAC on creation/approval/application; input validation on codes and values.
- Encryption in transit/at rest; audit logs tamper‑resistant.

---

## User Scenarios & Testing

### User Story 1 – Admin launches both‑fees discount (P1)

Why: Increase conversion for a campaign spanning multiple providers.

Independent Test: Create both‑fees discount, providers approve, discount appears in eligible quotes.

Acceptance Scenarios:

1. Given a new both‑fees discount, when saved, then targeted providers receive approval requests.
2. Given a provider approves, when a quote is created in active window, then the discount is selectable.

### User Story 2 – Provider creates own discount (P1)

Why: Allow providers to run targeted promotions without admin approval.

Independent Test: Provider creates discount; it appears in their quote creation and validates.

Acceptance Scenarios:

1. Given a provider discount, when dates start, then the discount is available for selection.
2. Given usage limit is reached, when applied, then validation fails with clear reason.

### User Story 3 – Patient applies code before acceptance (P2)

Why: Ensure the accepted price uses a single validated discount that cannot change afterwards.

Independent Test: Enter a valid code on one named subquote, accept it, and verify the discounted price is frozen in the AcceptanceEvent and no code entry is offered at payment.

Acceptance Scenarios:

1. Given a valid code entered on a named subquote before acceptance, when applied, then that subquote's totals update, the provider's promotion record is unchanged, and audit records exist.
2. Given another code is entered on the same subquote while one is active, when confirmed, then the new code replaces the old one for that subquote only.
3. Given the patient accepts the subquote, when the acceptance is confirmed, then the discounted price and promotion are frozen into the AcceptanceEvent snapshot.
4. Given an accepted subquote, when the patient, provider, or admin tries to enter, remove, replace, or revalidate a promotion, then the action is rejected and the accepted price is unchanged.

### User Story 4 – Promotion attachment, provenance, and usage lifecycle (P1)

Why: Ensure each promotion is tied to the exact row the patient accepted and that usage limits count each acceptance once.

Independent Test: Send a quote with an eligible automatic promotion, accept one subquote, complete the first payment, and verify attachment, Application provenance, and usage counts at each step.

Acceptance Scenarios:

1. Given an active auto-applied program eligible for some option/date-price rows of a quote, when the quote is sent, then the program is attached to every eligible row and no other row, each row keeps the provider's entered price, the discount is shown as a separate line, and one use is reserved for that quote.
2. Given a program attached to a sent row, when the program's value is edited or the program is paused or expires before acceptance, then the sent row keeps the terms copied at send.
3. Given a subquote carrying a promotion, when the patient accepts it, then one Application is created in state Applied, linked to the AcceptanceEvent, the parent quote and version, and the accepted option/date-price row, and one use is reserved.
4. Given a promotion that was not attached to a row at send and was not entered by the patient on that subquote, when any request tries to apply it to that row, then the request is rejected with a clear reason and no price changes.
5. Given an Applied redemption, when the first payment succeeds, then the state becomes Completed and the use is consumed.
6. Given an Applied redemption, when the booking reaches `Payment Window Expired` or is cancelled, then the status becomes Voided and the use is released.
7. Given a `Payment Window Expired` booking whose promotion has a usage limit, when an admin revives it, then one use is re-reserved; if the limit is exhausted, the revive is rejected.
8. Given sibling subquotes marked Not Selected and competing quotes cancelled by the acceptance, then none of them creates an Application, and any use reserved for them at send by an auto-applied promotion is released.
9. Given an auto-applied program with one use left and two quotes eligible for it, when the first quote is sent, then one use is reserved; when the second quote is sent, then the promotion does not attach because the limit is fully reserved, and the limit is never exceeded.
10. Given a sent quote carrying an auto-applied promotion with a reserved use, when a subquote of that quote is accepted, then the reservation is consumed; when instead the quote expires, is withdrawn, or ends Not Selected or cancelled, then the reservation is released.
11. Given a sent quote holding one reserved use for an auto-applied promotion, when the provider re-sends a new version that still carries the promotion, then the existing reservation is kept and no second use is reserved; when the new version no longer carries the promotion, then the reservation is released; and given a sent quote with no reservation, when a new version newly carries the promotion, then one use is reserved.
12. Given an accepted subquote whose auto-applied promotion use was consumed at acceptance, when the booking reaches `Payment Window Expired` or is cancelled before the first payment, then the use returns to the limit; when an admin later revives the booking, then the use is taken again if the limit has room, and otherwise the revive is rejected and the accepted price stays unchanged.

### Edge Cases

- Ineligible/expired/limit‑reached codes: validation fails with reason.
- Simultaneous attempts to apply codes on one subquote before acceptance: last confirmed selection wins; audit both attempts. Attempts after acceptance are rejected.
- Program paused, edited, or expired after a quote is sent: the sent rows keep the terms copied at send.
- Patient code no longer valid when the patient confirms acceptance (for example, its usage limit was reached): the reason is shown and the patient may accept at the offered price or cancel.
- Provider fails to respond to approval: auto‑decline after policy window; visible in audit.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-019-001**: System MUST allow admins to create platform discounts with type, value, dates, usage limits, and targeting.
- **REQ-019-002**: System MUST allow providers to create provider‑specific discounts with similar controls.
- **REQ-019-003**: System MUST attach provider-selected and eligible automatic promotions to option/date-price rows when a quote is sent, validate patient codes on one named subquote before acceptance, and apply at most one discount per subquote.
- **REQ-019-004**: System MUST enforce priority and non‑stacking rules (patient > provider > affiliate when conflicts arise).
- **REQ-019-005**: System MUST track usage and financial impact with exports and dashboards.
- **REQ-019-012**: System MUST copy each row's promotion terms into the sent quote version at send; later program changes MUST NOT change a sent row.
- **REQ-019-013**: System MUST freeze the promotion and discounted price of an accepted subquote in the AcceptanceEvent snapshot and MUST reject any later removal, replacement, code entry, price-changing revalidation, or admin void, except through the FR-006 provider-fault transfer, which creates a new linked record.
- **REQ-019-014**: For provider-selected promotions and patient-entered codes, System MUST reserve one promotion use at acceptance, consume it at the first successful payment, release it on `Payment Window Expired` or cancellation, and re-reserve it on an admin revive, rejecting the revive if the usage limit is exhausted.
- **REQ-019-015**: For an auto-applied promotion, System MUST reserve one use when a quote carrying it is sent, MUST hold at most one reserved use per sent quote across re-sent versions (keeping the existing reservation, creating one only when a new version newly carries the promotion, and releasing it when a new version no longer carries the promotion), MUST release the reservation when the quote expires, is withdrawn, or ends Not Selected or cancelled, and MUST consume it at acceptance. If the booking reaches `Payment Window Expired` or is cancelled before the first payment, System MUST return the consumed use to the limit; on an admin revive, System MUST take the use again if the limit has room and otherwise MUST reject the revive, so the accepted price never changes. Usage limits MUST count active reservations plus consumed uses so that a limit can never be exceeded.
- **REQ-019-016**: System MUST calculate commission on the accepted price after the promotion for every discount type, including Hairline-funded programs.

### Data Requirements

- **REQ-019-006**: System MUST persist discount definitions, approvals, and usage records with audit details.
- **REQ-019-007**: System MUST link each Application to the parent quote and version, the accepted option/date-price row (subquote), the AcceptanceEvent, the booking, and participant entities.

### Security & Privacy Requirements

- **REQ-019-008**: System MUST restrict creation/approval/apply actions to authorized roles; patient sees only necessary pricing info.
- **REQ-019-009**: System MUST encrypt sensitive data and preserve tamper‑evident audit logs.

### Integration Requirements

- **REQ-019-010**: System MUST send provider approval notifications via Notification Service.
- **REQ-019-011**: System MUST integrate with calculation/settlement services for consistent totals.

### Marking Unclear Requirements

No unresolved clarifications remain for V1; loyalty/referral programs and stacking are out of scope.

---

## Key Entities

- **PromotionProgram**: id, program_type (`ADMIN_VIA_PROVIDER` | `PROVIDER_SELF` | `HAIRLINE_FUNDED_DIRECT_ISSUED`), scope (`REUSABLE` | `AD_HOC_QUOTE_BOUND` — applies to `PROVIDER_SELF` only; other program types are always `REUSABLE`), bound_quote_id (nullable parent containment), bound_quote_option_date_price_id (nullable application target; both bindings set only for `AD_HOC_QUOTE_BOUND`), owner (admin user id or provider id), name, description, discount_type, value, applies_to (whole price / treatment / travel / other), application_mode (auto / code-only / list-selection / either), funding_model (derived), active window, total usage limit, per-user usage limit, targeting, issuance_channel (for Hairline-Funded), lifecycle_state, audit timestamps.
- **PromotionCode**: id, program_id, code text, recipient_binding (open / affiliate id / segment id / patient id), issued_at, issued_by, status (unused / in-progress / redeemed / revoked / expired). Note: `in-progress` = a use of the code is reserved by an accepted subquote and the first payment has not yet succeeded; distinct from `Application.state = APPLIED` which is the redemption-level view of the same moment.
- **Adoption**: id, program_id, provider_id, status (pending / accepted / declined / auto_declined / revoked_by_provider / revoked_by_admin), decided_at, decided_by, comment.
- **Application** (Redemption): created only at subquote acceptance. id, program_id, code_id (nullable), source (provider_selected / auto_attached / patient_code), acceptance_event_id, quote_id, quote_version, quote_option_date_price_id (the accepted subquote), booking_id, patient_id, provider_id (nullable for Hairline-Funded), state (`APPLIED` at acceptance with one use reserved / `COMPLETED` at the first successful payment with the use consumed), status (active / voided / superseded / reversed / refunded), supersedes_application_id (nullable; set on a replacement created by a provider-fault transfer), terms snapshot (type, value, applies-to, funding model as fixed at send), currency (quote currency from the acceptance snapshot), discount_value, funding_split (hairline_portion, provider_portion), applied_at, completed_at, audit context.
- **UsageReservation**: id, program_id, quote_id, quote_version (the version that created it; a later re-sent version keeps the same record), with at most one active record per sent quote, reserved_at, state (reserved / consumed / released), release_reason (expired / withdrawn / not_selected / cancelled / removed_in_new_version; nullable), application_id (set when consumed at acceptance), resolved_at. Used for auto-applied promotions; usage limits count reserved plus consumed records.
- **ReportSnapshot** (optional): aggregated usage and impact metrics for exports.

---

## Appendix: Change Log

| Date       | Version | Changes                                      | Author |
|------------|---------|----------------------------------------------|--------|
| 2025-11-11 | 1.0     | Initial PRD creation                         | AI     |
| 2025-11-11 | 1.1     | Filled scope, workflows, rules, and criteria | AI     |
| 2026-04-12 | 1.2     | Added Screen 4 (Admin Discount Code Catalog) as placeholder with TODO note; screen code FR-019/Screen 4 reserved for FR-022 Master Reference Table | AI     |
| 2026-04-13 | 1.3     | Finalized Screen 4 (Admin Discount Code Catalog): replaced placeholder with full catalog field definitions, fixed result-table columns, business rules, and acceptance criteria aligned to FR-022 search/filter contract | Codex |
| 2026-05-12 | 1.4     | Major restructure of Screen Specifications: introduced unified three-program model (Admin-via-Provider, Provider Self-Created, Hairline-Funded & Direct-Issued); expanded screen inventory from 3 to 11 screens (6 admin, 4 provider, 1 patient); added Provider Adoption Manager, Provider Promotion Portfolio, Hairline-Funded & Direct-Issued Codes Manager, and merged Analytics & Applications screens for both admin and provider; preserved client's Applied vs Completed state distinction; expanded Key Entities to include PromotionProgram, PromotionCode, Adoption, and Application; added Alt Flow C1 for direct-issued redemptions. Two deliberate scope expansions beyond client transcription, both flagged in-screen: (a) admin visibility into provider self-created discounts via Hub + Portfolio (transcription L295–300 said admin would not need this); (b) optional Code field retained on provider self-created promotions (transcription L27–33 said codes are irrelevant for provider-side). | Claude |
| 2026-05-12 | 1.5     | FR-004 alignment: introduced `scope` field (`REUSABLE` / `AD_HOC_QUOTE_BOUND`) and `bound_quote_id` on PromotionProgram; split Alt Flow A1 into A1a (pre-defined reusable) and A1b (inline ad-hoc); Screen 9 expanded with two entry modes (Standalone vs Inline-from-Quote) including a "Save as reusable" toggle and Mode-2 default behaviour; Screen 1 Hub adds a Scope filter. Free-text `promotionNote` path is removed — every discount must correspond to a structured `PromotionProgram` (FR-004 v1.8 drops `promotionNote`). | Claude |
| 2026-05-12 | 1.6     | Verification fixes (5 issues): (1) Split B2 into B2 (user-initiated prompt) and B3 (auto-applied silent priority); updated Business Rules to clarify when each mechanism applies. (2) Added FR-004, FR-018, FR-022, FR-031, FR-010 to Dependencies section. (3) Added Screen 2 AC-4 for Auto-applied rejection on Both-Fees programs. (4) Renamed PromotionCode status `reserved` → `in-progress` across Screen 5, Screen 6 funnel, and Key Entities; added disambiguation note. (5) Added Screen 2 Note explaining Application Mode option asymmetry between admin and provider forms. | Claude |
| 2026-05-12 | 1.7     | Added PR-05: Financial Management & Reporting to Module header (provider tenant ownership); updated system-prd.md to match. Status updated to Verified & Approved. | Claude |
| 2026-05-14 | 1.8     | Approval metadata cleanup: completed Technical Lead and Stakeholder approvals. | Codex |
| 2026-06-22 | 1.9     | Added explicit ownership note that FR-018 owns affiliate-specific promo code generation, bulk affiliate assignment, dashboard display, and payout attribution; FR-019 remains the shared validation/redemption engine for affiliate-bound codes. | Codex |
| 2026-06-23 | 2.0     | FR-018 dependency cleanup: corrected affiliate-bound bulk-generation acceptance wording to one unique code per selected affiliate, and clarified that price-discount priority does not erase valid affiliate attribution metadata needed by FR-018. | Codex |
| 2026-09-10 | 2.1     | FR-004 v2.6 reconciliation: moved promotion attachment from the parent Quote to `QuoteOptionDatePrice.promotionId`; added the option/date binding for ad-hoc quote-bound programs while retaining parent-quote containment; and updated redemption provenance. See [Change Request](./change-request-2026-09-10-option-date-promotion-alignment.md). | Product Owner / Documentation |
| 2026-10-16 | 2.2     | MTG-002 quote-model alignment ([CR-FR019-20261016-01](./change-request-2026-10-16-mtg002-quote-model-alignment.md)). Patient codes only before acceptance on one named subquote, never written to the provider promotion (FR-019-1, D8); post-acceptance freeze with no provider remove/replace, checkout or booking code entry, booking revalidation, or admin Void, except the provider-fault transfer linked record (FR-019-2, D9, D6); promotion terms fixed at send (D10); Application created at acceptance and linked to the AcceptanceEvent (FR-019-3); usage reserved at acceptance, consumed at first successful payment, released on Payment Window Expired or cancellation, re-reserved on admin revive (FR-019-4, D11, D2); automatic promotions attach at send to every eligible row with new User Story 4 criteria (FR-019-7, M14); commission base sentence (D12); fixed-amount currency and Application currency (FR-019-6); subquote wording (FR-019-9). Status changed to Revised — Pending Consolidated Verification. | Product Owner / Documentation |
| 2026-10-16 | 2.3     | Product Owner Q-series alignment ([CR-FR019-20261016-01](./change-request-2026-10-16-mtg002-quote-model-alignment.md)). Commission is calculated on the price after promotion for every discount type, including Hairline-funded programs; removed wording that Hairline-only discounts leave providers unaffected or affect Hairline's share only (A2, C1, program overview, General Module Rules, REQ-019-016; Q5). Auto-applied promotions reserve one use at each send, release it on expiry, withdrawal, or Not Selected or cancelled outcomes, and consume it at acceptance; usage limits count reservations plus consumed uses (scope, A3, A5, Screen 1 Usage, Screen 6 rules, General Module Rules, User Story 4 scenarios 1 and 8 to 11, REQ-019-014 and REQ-019-015, UsageReservation entity; Q6). A sent quote holds at most one reserved use across re-sent versions: kept on re-send, created only when a new version newly qualifies, released when a new version drops the promotion (Q29). An auto-applied use consumed at acceptance returns to the limit on `Payment Window Expired` or cancellation before the first payment, and an admin revive takes it again only if the limit has room, otherwise the revive is rejected (Screen 6 rules, General Module Rules, User Story 4 scenario 12, REQ-019-015; Q30). Consolidated verification remains pending. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role           | Name | Date       | Signature/Approval |
|----------------|------|------------|--------------------|
| Product Owner  | TBD  | 2026-05-12 | Approved           |
| Technical Lead | TBD  | 2026-05-14 | Approved           |
| Stakeholder    | TBD  | 2026-05-14 | Approved           |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Last Updated**: 2026-10-16
