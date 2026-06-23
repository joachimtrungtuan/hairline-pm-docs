# FR-019 - Promotions & Discount Management

**Module**: A-06: Discount & Promotion Management | PR-05: Financial Management & Reporting
**Feature Branch**: `fr019-promotions-discounts`
**Created**: 2025-11-11
**Status**: ✅ Verified & Approved
**Source**: FR-019 from local-docs/project-requirements/system-prd.md; Transcriptions (admin/provider references)

---

## Executive Summary

Define, approve, and apply discounts across the Hairline platform with clear governance and auditability. Admins can create platform‑wide promotions (including those that affect both provider and Hairline fees), while providers can create their own discounts. The system validates codes at quote and booking, enforces usage limits and prioritization rules, and tracks usage and financial impact. This increases conversion while safeguarding provider margins and Hairline commission through an approval workflow and transparent reporting.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (P-03 overlay): See applied discount summary in quote/booking flows; enter a discount code when enabled; view final price breakdown.
- Provider Platform (PR-02/PR-05): Create provider-specific discounts; review and accept/decline platform discounts; see eligible discounts during quote creation; view discount impact in reports.
- Admin Platform (A-06): Create and manage platform discounts (platform‑only or both‑fees), configure categories, dates, limits, and code rules; manage approvals and track usage; view financial impact.
- Shared Services (S-03, S-02): Notification Service for approval and status alerts; Payment/Financial service for price calculation and settlement alignment.

### Multi-Tenant Breakdown

Patient Platform (P-03 overlay):

- Input discount code (if allowed at stage), see validation feedback.
- See discounted totals and savings; understand that only one discount applies.

Provider Platform (PR-02/PR-05):

- Create provider discounts with type (percent/fixed/package upgrade), dates, limits.
- Accept/decline platform both‑fees discounts per program; auto‑active provider‑only discounts.
- Select applicable approved discounts within quote creation (where rules allow).

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
- Discount validation and application at quote and booking; one discount per booking.
- Provider approval workflow for platform both‑fees discounts.
- Usage tracking and financial impact reporting.

Out of Scope:

- Stacking multiple discounts on a single booking (explicitly disallowed).
- Loyalty points and referral rewards (covered elsewhere).
- Tax/VAT calculation changes (handled by billing/finance rules).
- Affiliate-specific promo code generation, bulk assignment to affiliates, affiliate dashboard display, and affiliate payout attribution are owned by FR-018 / A-07. FR-019 owns the shared promotion engine: validation, active windows, usage limits, single-discount conflict behavior, applied/completed redemption state, and financial-impact logging.

### Entry Points

- Admin creates a platform discount in A-06; if both‑fees, providers receive approval requests.
- Provider creates a provider discount in PR-02/PR-05; becomes active per dates/limits.
- Patient enters a code (if enabled) at quote/booking; system validates and applies if eligible.

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
4. When provider accepts, discount becomes eligible for that provider’s quotes during active window.
5. System tracks usage and financial impact per provider.

### Alternative Flows

**A1a: Provider‑Only Discount (Reusable — Pre-Defined)**:

- Trigger: Provider creates their own discount from the standalone Promotion Detail screen (Screen 9).
- Steps: System validates inputs, persists the program with `scope = REUSABLE`, and activates per dates/limits; no approval needed.
- Outcome: Discount immediately eligible for **list-selection** during the provider's quote creation flow (FR-004 Screen 1).

**A1b: Provider‑Only Discount (Inline — On-the-Spot from Quote)**:

- Trigger: Provider opens the inline promotion creator from within FR-004 Screen 1 during quote drafting.
- Steps: Provider enters name, type, value, applies-to, and optional code in a mini-form; system creates a new `PromotionProgram` with `scope = AD_HOC_QUOTE_BOUND` and `bound_quote_id` set to the current quote. Provider may toggle "Save as reusable program for future quotes" to promote the record to `scope = REUSABLE`.
- Outcome: Discount is attached to the originating quote (`quote.promotionId` set) and is governed by the same caps, validation, and admin-override rules as A1a. Ad-hoc records appear in FR-019 Screen 1 Hub (filterable by `scope`) and Screen 4 Portfolio.

**A2: Hairline‑Only Discount**:

- Trigger: Admin creates Hairline‑funded discount (commission only).
- Steps: System applies financial impact to Hairline share only; not visible to providers in selection UIs.
- Outcome: Booking reflects reduced platform commission; providers unaffected.

**B1: Code Validation Failure**:

- Trigger: Patient/provider enters invalid/expired/reached‑limit code.
- Steps: System returns reason; prevents application.
- Outcome: No discount applied; user can retry.

**B2: Single‑Discount Rule Conflict (User‑Initiated)**:

- Trigger: Patient or provider manually enters or selects a second discount when one is already applied to the quote/booking.
- Steps: System blocks the new entry; prompts the user to confirm replacement or keep the existing discount.
- Outcome: Exactly one discount per booking; the user's confirmed choice is applied.

**B3: Single‑Discount Rule Conflict (Auto‑Applied)**:

- Trigger: Two auto-applied discounts become simultaneously eligible for the same quote (e.g., a Hairline-funded auto-applied program activates while a provider's auto-applied program is already on the quote).
- Steps: System silently resolves the conflict using priority order: patient-entered code > provider discount > affiliate discount. Lower-priority discount is not applied; no user prompt is shown.
- Outcome: Exactly one discount affects the patient's final price; audit records which program was applied and which was superseded. If a valid affiliate-bound code/link was already captured as the patient acquisition source, FR-019 preserves that affiliate attribution metadata for FR-018 even when a provider-side promotion wins the price-discount priority.

**C1: Hairline-Funded / Direct-Issued Code Redemption**:

- Trigger: Admin issues a Hairline-funded code (open code, segment-bound, or affiliate-distributed) and patient enters it at quote/booking.
- Steps: System validates the code against issuance binding (open vs recipient-bound), records the redemption against the issuing channel (e.g., affiliate id), and attributes the financial impact to Hairline's share only. For affiliate-bound codes, code generation and affiliate assignment are initiated from FR-018; FR-019 receives the registered code and manages redemption lifecycle.
- Outcome: Patient receives discount; provider's settlement is unaffected; affiliate (if applicable) accrues the configured incentive (see FR-018).

---

## Screen Specifications

This module exposes **three promotion programs** under one unified governance model:

1. **Admin-via-Provider** — Admin defines a campaign that affects both Hairline and provider fees; targeted providers must opt-in before the code becomes selectable on their quotes.
2. **Provider Self-Created** — Provider defines a discount that affects only their own fees; no admin approval required.
3. **Hairline-Funded & Direct-Issued** — Admin defines a Hairline-only discount that is issued directly to patients (open-entry code, patient-segment-bound, affiliate-distributed, or individually issued); providers are not involved in approval.

All three program types share a single `PromotionProgram` entity (see Key Entities) and are managed through a unified screen system with type-aware filters, forms, and analytics. Admin retains override authority on every record (pause, revoke adoption, void redemption, refund) regardless of program type.

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
| 11 | Patient | Apply Discount at Quote/Booking | Retains prior Screen 3 (minor additions) |

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
| Usage | Redeemed count vs limit | |
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
4. Given the admin triggers Pause on an Active program row, then the program lifecycle transitions to Paused, all existing redemptions remain intact, and new redemptions are blocked.

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
- `Application Mode = Auto-applied` is only allowed for programs with `Funding Model = Hairline Only` or `Provider Only` and explicit eligibility rules (cannot be auto-applied across multiple providers without consent).
- Bulk upload / bulk edit available for campaign management.

**Acceptance Criteria**:

1. Given the admin creates an Admin-via-Provider program and submits, then the program enters Pending Approval and the targeted providers receive S-03 notifications.
2. Given the admin creates a Hairline-Funded program with `Issuance Channel = Open code` and a single code, when the program is published, then the code is immediately redeemable by any patient at quote/booking and the program does not appear in any provider's adoption inbox.
3. Given the admin edits the Value of a Paused program and republishes, then the new value applies to redemptions from that point forward; prior redemptions retain their original values in audit.
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
| Redemption Status | Unused / In-Progress (entered at quote) / Redeemed (completed at booking) / Revoked / Expired |
| Redeemed By | Patient identifier when redeemed |
| Redeemed At | Timestamp |
| Discount Issued | Currency amount |

**Business Rules**:

- Open codes have one code that any eligible patient may use until the total usage limit is reached.
- Affiliate-bound codes integrate with FR-018; FR-018 owns generation and one-affiliate-per-code assignment, while FR-019 owns validation and redemption state. Redemptions accrue incentive to the linked affiliate.
- Segment-bound codes validate the patient against the segment definition at entry time.
- Individually-issued codes are single-use and bound to a specific patient identifier.
- Revoking a code already in `In-Progress` state cancels the in-progress quote application and notifies the patient.

**Acceptance Criteria**:

1. Given the admin selects a Hairline-Funded program with channel = Affiliate-bound and triggers Bulk Generate for 50 selected affiliates, when generation completes, then 50 unique codes are created, each code is bound to exactly one affiliate, and each appears in the table with status = Unused.
2. Given a patient enters an Affiliate-bound code at booking, when redemption completes, then the corresponding row updates to Redeemed and the affiliate's incentive accrual (per FR-018) is triggered.

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
| State | **Applied** (entered at checkout / quote) vs **Completed** (booking confirmed and payment captured) — distinct states per client transcription |
| Patient | Patient identifier |
| Provider | Provider on the quote/booking |
| Quote / Booking ID | Link to source entity |
| Discount Value | Currency amount applied |
| Funding Split | Hairline portion / Provider portion |
| Applied At | Timestamp of state = Applied |
| Completed At | Timestamp of state = Completed (blank if not yet) |
| Status | Active / Reversed / Refunded / Voided |
| Admin Actions | View Detail / Reverse / Refund / Void |

**Business Rules**:

- The two-state distinction (Applied vs Completed) is preserved per client request (Admin Part 1 L341–344). Applied = the code is on the quote/booking but not yet finalised; Completed = booking confirmed and payment captured.
- Reverse / Refund / Void actions are logged with mandatory reason and integrate with FR-017 (Billing & Finance) for monetary reconciliation.
- Drilling from a KPI card on the Overview tab filters the Applications tab accordingly.

**Acceptance Criteria**:

1. Given a quote with a discount code applied moves to a confirmed booking, when payment is captured, then the redemption row transitions from State = Applied to State = Completed and is reflected in Overview KPIs within 5 seconds.
2. Given an admin triggers Refund on a Completed redemption with reason, then the row Status updates to Refunded, the audit log captures actor/time/reason, and FR-017 receives a reconciliation event.

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
- **Mode 2 — Inline (modal opened from FR-004 Screen 1 during quote drafting):** Provider creates an on-the-spot promotion attached to the current quote. `scope = AD_HOC_QUOTE_BOUND` with `bound_quote_id` set. A "Save as reusable program for future quotes" toggle, when enabled, promotes the record to `scope = REUSABLE` on submit.

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
- Free-text "promotion note" entries are **not supported**: every discount applied to a quote must correspond to a structured `PromotionProgram` record (Mode 1 or Mode 2). FR-004's legacy `promotionNote` field is removed in FR-004 v1.8.
- Funding Model is fixed at `Provider Only` and is not user-editable.
- No admin approval required for activation in either mode.

**Acceptance Criteria**:

1. Given the provider saves a Mode 1 (standalone) promotion with no Code and Application Mode = List-selection, then the promotion is available for list-selection during FR-004 Screen 1 quote creation within its active window.
2. Given the provider saves a Mode 1 promotion with a Code and Application Mode = Code-only, then the promotion is not shown in the quote-creation selection list but is redeemable when the patient enters the code at quote/booking.
3. Given the provider opens the inline modal from FR-004 Screen 1 (Mode 2) and saves an ad-hoc promotion without enabling "Save as reusable", then a new `PromotionProgram` with `scope = AD_HOC_QUOTE_BOUND` is created, `bound_quote_id` is set, `quote.promotionId` is set, and the record is not offered on any other quote's selection list.
4. Given the provider saves a Mode 2 ad-hoc promotion with "Save as reusable" enabled, then `scope = REUSABLE` is recorded and the promotion becomes selectable on future quotes within its active window.

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
| Row Actions | View Quote / Remove Discount (if quote not yet booked) / Replace with Different Promotion |

**Business Rules**:

- Provider may remove or replace a discount on a quote that has not yet transitioned to a confirmed booking, subject to the single-discount-per-booking rule.
- Removal or replacement of an Adopted-Admin campaign discount is logged and visible to admin on Screen 6.
- The provider cannot reverse a Completed redemption; that authority sits with admin (Screen 6).

**Acceptance Criteria**:

1. Given a Quote in Applied state with a self-created discount, when the provider triggers Remove Discount, then the discount is detached from the quote, the redemption row moves to status = Voided, and quote totals recalculate.

---

### Patient Platform Screens (P-03 overlay)

#### Screen 11: Patient — Apply Discount at Quote / Booking

**Purpose**: Validate and apply a single discount during the patient-side quote review and booking confirmation flow.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Code input | text | No | Optional discount code | Format rules; 1 active code at a time |
| Price breakdown | panel | Yes | Base price, discount line, discount scope, totals | Must reflect applied rules |
| Discount Scope label | label | Yes | Shows which fee component the discount applies to (e.g., "Applies to transplant cost only") | Per HairlineApp Part 1 L156–158 |

**Business Rules**:

- One discount per booking; entering a new code prompts the patient to confirm replacement of the current discount.
- Validation occurs both at quote review and booking confirmation.
- Clear feedback for invalid / expired / limit-reached / segment-mismatched codes.
- Where a discount applies only to a sub-component (e.g., treatment cost, not travel), the breakdown explicitly shows which line is reduced.

**Acceptance Criteria**:

1. Given a patient enters a valid code, when validation succeeds, then the price breakdown updates within 1 second and shows the discount scope label.
2. Given a patient enters a code while another discount is already applied, when the patient confirms replacement, then the previous discount is removed and the new one is applied; audit records both events.

---

## Success Criteria

### Patient/Provider Experience Metrics

- SC-001: 95% of valid codes validate within 1 second at quote/booking.
- SC-002: 0% of bookings apply more than one discount (enforced at all steps).

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
- Usage limits and active dates are enforced at validation time.
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
- Calculation order of operations (base → discounts → taxes/fees).

Configurable with Restrictions:

- Max discount value thresholds per policy and region.
- Auto‑decline window for unresponded provider approvals.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- PR-02: Inquiry & Quote Management – discount selection during quote creation.
- P-03: Booking & Payment – validate/apply discount at booking and settlement.
- A-05: Billing & Financial Reconciliation – reflect Hairline vs provider shares.
- S-03: Notification Service – provider approvals and status updates.
- S-02: Payment/Financial Service – price calculation and settlement.
- FR-004: Quote Submission & Management – Screen 9 Mode 1/Mode 2 entry points live within FR-004 Screen 1; `quote.promotionId` field and removal of legacy `promotionNote` are co-owned changes (FR-004 v1.8).
- FR-018: Affiliate Management – Affiliate-bound code redemptions accrue incentive to the linked affiliate; FR-019 triggers the incentive event consumed by FR-018.
- FR-022: Search & Filtering – Screen 1 search/filter controls are co-owned with FR-022; any field change must be updated in both FRs.
- FR-031: Admin Access Control & Permissions – all admin create/approve/override actions are RBAC-gated per FR-031 role definitions.
- FR-010: Treatment & Recovery Case Management – Screen 10 Applications tab links redemptions to FR-010 treatment case entities.

### External Dependencies (APIs, Services)

- Email/Push providers (via S-03) for approval/status notifications.

### Data Dependencies

- Provider catalog and identifiers for targeting.
- Booking/quote entities with price components for calculation.

---

## Assumptions

### User Behavior Assumptions

- Providers respond to approval requests within 3 business days.
- Patients will attempt code entry primarily during quote review.

### Technology Assumptions

- Quote and booking flows expose a single code input surface.
- Calculation service supports deterministic rounding and currency rules.

### Business Process Assumptions

- Finance defines regional caps and policy; legal approves terms for promotions.

---

## Implementation Notes

### Technical Considerations

- Calculation pipeline: base price → discount (single) → taxes/fees; idempotent validation.
- Prevent race conditions across quote/booking with atomic application and revalidation on booking.
- Audit trail for all state changes; soft‑disable discounts without data loss.

### Integration Points

- Admin UI ↔ Promotion service: CRUD, approvals, targeting.
- Provider UI ↔ Promotion service: approvals, provider discounts.
- Quote/Booking ↔ Calculation service: validate/apply discount.

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

### User Story 3 – Patient applies code at booking (P2)

Why: Ensure final price uses a single validated discount.

Independent Test: Enter valid code at booking; total updates and audit entry recorded.

Acceptance Scenarios:

1. Given a valid code, when applied at booking, then totals update and audit records exist.
2. Given another code is entered while one is active, when confirmed, then the new code replaces the old one.

### Edge Cases

- Ineligible/expired/limit‑reached codes: validation fails with reason.
- Simultaneous attempts to apply codes: last confirmed selection wins; audit both attempts.
- Provider fails to respond to approval: auto‑decline after policy window; visible in audit.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-019-001**: System MUST allow admins to create platform discounts with type, value, dates, usage limits, and targeting.
- **REQ-019-002**: System MUST allow providers to create provider‑specific discounts with similar controls.
- **REQ-019-003**: System MUST validate and apply a single discount at quote and booking.
- **REQ-019-004**: System MUST enforce priority and non‑stacking rules (patient > provider > affiliate when conflicts arise).
- **REQ-019-005**: System MUST track usage and financial impact with exports and dashboards.

### Data Requirements

- **REQ-019-006**: System MUST persist discount definitions, approvals, and usage records with audit details.
- **REQ-019-007**: System MUST link applied discounts to quotes/bookings and participant entities.

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

- **PromotionProgram**: id, program_type (`ADMIN_VIA_PROVIDER` | `PROVIDER_SELF` | `HAIRLINE_FUNDED_DIRECT_ISSUED`), scope (`REUSABLE` | `AD_HOC_QUOTE_BOUND` — applies to `PROVIDER_SELF` only; other program types are always `REUSABLE`), bound_quote_id (nullable; set when scope = `AD_HOC_QUOTE_BOUND`), owner (admin user id or provider id), name, description, discount_type, value, applies_to (whole price / treatment / travel / other), application_mode (auto / code-only / list-selection / either), funding_model (derived), active window, total usage limit, per-user usage limit, targeting, issuance_channel (for Hairline-Funded), lifecycle_state, audit timestamps.
- **PromotionCode**: id, program_id, code text, recipient_binding (open / affiliate id / segment id / patient id), issued_at, issued_by, status (unused / in-progress / redeemed / revoked / expired). Note: `in-progress` = code entered at quote stage but booking not yet confirmed; distinct from `Application.state = APPLIED` which is the redemption-level view of the same moment.
- **Adoption**: id, program_id, provider_id, status (pending / accepted / declined / auto_declined / revoked_by_provider / revoked_by_admin), decided_at, decided_by, comment.
- **Application** (Redemption): id, program_id, code_id (nullable), quote_id, booking_id (nullable until completed), patient_id, provider_id (nullable for Hairline-Funded), state (`APPLIED` at checkout / `COMPLETED` after payment), status (active / reversed / refunded / voided), discount_value, funding_split (hairline_portion, provider_portion), applied_at, completed_at, audit context.
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
**Last Updated**: 2026-06-22
