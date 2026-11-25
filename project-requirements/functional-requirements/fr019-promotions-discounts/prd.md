# FR-019 - Promotions & Discount Management

**Module**: A-06: Discount & Promotion Management | PR-05: Financial Management & Reporting
**Feature Branch**: `fr019-promotions-discounts`
**Created**: 2025-11-11
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-019 from local-docs/project-requirements/system-prd.md; Transcriptions (admin/provider references)

---

## Executive Summary

Define, approve, and apply discounts across the Hairline platform with clear governance and auditability. Admins can create platform‑wide promotions (including those that affect both provider and Hairline fees), while providers can create their own discounts. Promotions attach to individual option/date-price rows (subquotes) when a quote is sent, and a patient may enter a code on one named subquote before accepting it. Promotion terms are fixed when the quote is sent and frozen when the subquote is accepted. The system enforces usage limits and prioritization rules, and tracks usage and financial impact. This increases conversion while safeguarding provider margins and Hairline commission through an approval workflow and transparent reporting.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (P-03 overlay): See the discount on each offered subquote; enter a discount code on one named subquote before acceptance when enabled; view the final price breakdown, which is read-only after acceptance. (REQ-019-020)
- Provider Platform (PR-02/PR-05): Create provider-specific discounts; review and accept/decline platform discounts; see eligible discounts during quote creation; view discount impact in reports.
- Admin Platform (A-06): Create and manage platform discounts (platform‑only or both‑fees), configure categories, dates, limits, and code rules; manage approvals and track usage; view financial impact.
- Shared Services (S-03, S-02): Notification Service for approval and status alerts; Payment/Financial service for price calculation and settlement alignment.

### Multi-Tenant Breakdown

Patient Platform (P-03 overlay):

- Input a discount code on one named subquote before acceptance (if enabled), see validation feedback.
- See discounted totals and savings; understand that only one discount applies to a subquote and that the accepted price cannot change after acceptance.

Provider Platform (PR-02/PR-05):

- Create provider discounts with type (percent/fixed), dates, limits.
- Accept/decline platform both‑fees discounts per program; auto‑active provider‑only discounts. (REQ-019-021)
- Select applicable approved discounts for each option/date-price row within quote creation (where rules allow), choosing admin programs only from the list of programs the provider has adopted; the selection and its terms are fixed when the quote is sent.

Admin Platform (A-06):

- Create platform discounts: platform‑only, both‑fees, and Hairline‑only.
- Configure targets (all providers or subsets), dates, usage caps, stackability policy (single‑discount rule enforced globally).
- Manage approval workflow for both‑fees discounts; monitor provider responses. (REQ-019-022)
- Track usage and financial impact with exports.

Shared Services (S-03, S-02):

- S-03 sends the provider notices that exist: the approval request (on publish and on Re-invite) and the notice that the terms of an adopted program changed (REQ-019-118). It also notifies the adopting providers when an admin Force-Revokes, pauses or resumes an adopted program, and notifies admins when a provider revokes its own adoption. Each notice is its own event in the FR-030 notification catalogue.
- S-02 ensures correct price calculation and settlement attribution.

### Scope Boundaries

In Scope:

- Discount code definition and lifecycle (draft, active, paused, expired, archived), with usage limits and date windows; approval of an Admin-via-Provider program is per provider adoption, not a program state. (REQ-019-023)
- Promotion attachment to option/date-price rows when a quote is sent, patient code validation on one named subquote before acceptance, and freezing of the discounted price at acceptance; one discount per subquote.
- Promotion usage-limit reservation at acceptance, consumption at the first successful payment, and release on `Payment Window Expired` or cancellation; for auto-applied promotions, at most one reservation per sent quote, made at send, consumption when the accepted subquote carries the promotion, and release when the quote expires, is withdrawn, is archived, ends Not Selected or cancelled, or a subquote that does not carry the promotion is accepted; at most one automatic promotion per quote.
- Provider approval workflow for platform both‑fees discounts.
- Usage tracking and financial impact reporting.

Out of Scope:

- Stacking multiple discounts on a single subquote or booking (explicitly disallowed).
- Any change to the promotion or discounted price after acceptance, including code entry at checkout or booking, except the provider-fault transfer defined in FR-006.
- Payment, refund, and fund-release mechanics (FR-007, FR-007b, FR-017). (REQ-019-024)
- Loyalty points and referral rewards (covered elsewhere). (REQ-019-024)
- Tax/VAT calculation changes (handled by billing/finance rules). (REQ-019-024)
- Affiliate-specific promo code generation, bulk assignment to affiliates, affiliate dashboard display, and affiliate payout attribution are owned by FR-018 / A-07. FR-019 owns the shared promotion engine: validation, active windows, usage limits, single-discount conflict behavior, applied/completed redemption state, and financial-impact logging. (REQ-019-025)

### Entry Points

- Admin creates a platform discount in A-06; if both‑fees, providers receive approval requests. (REQ-019-026)
- Provider creates a provider discount in PR-02/PR-05; becomes active per dates/limits. (REQ-019-026)
- Patient enters a code (if enabled) on one named subquote before acceptance (FR-005 Alternative Flow A8); system validates it for that subquote and shows the discounted price if eligible. (REQ-019-026)
- Provider sends a quote; system attaches the selected promotion and any eligible automatic promotion to each option/date-price row and copies the promotion terms into the sent quote version. (REQ-019-026)

---

## Business Workflows

### Main Flow: Admin Creates Platform Discount (Both‑Fees) (REQ-019-027, REQ-019-028, REQ-019-029)

Actors: Admin, Provider, System
Trigger: Admin submits a new platform discount that affects both fees
Outcome: Providers approve participation; discount becomes selectable where applicable

Steps:

1. Admin defines discount (type, value, Hairline share %, dates, usage limit, targeted providers).
2. Admin publishes the discount; the system sets it Active and notifies targeted providers (approval-requested event of the FR-030 notification catalogue). Approval is per provider: the discount applies only to providers whose adoption is Accepted.
3. Providers accept or decline; system logs responses. A provider who does not answer within the auto-decline window is Auto-Declined. If every provider declines, the program stays Active with no participants until an admin archives it.
4. When provider accepts, discount becomes eligible for that provider’s option/date-price rows during the active window.
5. System tracks usage and financial impact per provider.

### Alternative Flows

**A1a: Provider‑Only Discount (Reusable — Pre-Defined)**: (REQ-019-030)

- Trigger: Provider creates their own discount from the standalone Promotion Detail screen (Screen 9).
- Steps: System validates inputs, persists the program with `scope = REUSABLE`, and activates per dates/limits; no approval needed.
- Outcome: Discount immediately eligible for **list-selection** during the provider's quote creation flow (FR-004 Screen 1).

**A1b: Provider‑Only Discount (Inline — On-the-Spot from Quote)**: (REQ-019-031)

- Trigger: Provider opens the inline promotion creator from within FR-004 Screen 1 during quote drafting.
- Steps: Provider enters name, type, value, applies-to, and optional code in a mini-form for one FR-004 option/date-price row; system creates a new `PromotionProgram` with `scope = AD_HOC_QUOTE_BOUND`, `bound_quote_id` set to the parent quote, and `bound_quote_option_date_price_id` set to that row. Provider may toggle "Save as reusable program for future quotes" to promote the record to `scope = REUSABLE`.
- Outcome: Discount is attached through `QuoteOptionDatePrice.promotionId` and is governed by the same caps, validation, and admin-override rules as A1a. Ad-hoc records appear in FR-019 Screen 1 Hub (filterable by `scope`) and Screen 4 Portfolio.

**A2: Hairline‑Only Discount**: (REQ-019-032)

- Trigger: Admin creates a Hairline‑funded discount.
- Steps: System applies the discount to the patient's price; the program is not visible to providers in selection UIs. Commission is calculated on the accepted price after the promotion, as for every discount type.
- Outcome: Both the platform commission and the provider's payout are reduced; the provider bears most of the discount. The funding of each program is defined in General Module Rules; FR-017 applies it in payout settlement.

**B1: Code Validation Failure**: (REQ-019-033)

- Trigger: A patient enters an invalid, expired or limit-reached code, or a provider picks from the list a promotion that no longer qualifies for the row (a provider types no code: FR-004 Screen 1 offers a select-or-create Promotion field).
- Steps: System returns reason; prevents application.
- Outcome: No discount applied; user can retry.

**B2: Single‑Discount Rule Conflict (User‑Initiated)**: (REQ-019-034)

- Trigger: Before the quote is sent, the provider picks a second promotion for an option/date-price row that already has one; or before the subquote is accepted, the patient enters a code on a subquote (option/date-price row) that already carries a promotion.
- Steps: System blocks the new entry; prompts the user to confirm replacement or keep the existing discount. A patient's replacement applies only to the patient's selection on that subquote and never changes the provider's promotion. A patient code replaces the promotion the row carries, including an automatic one (Alternative Flow A5 states the reservation outcome).
- Outcome: Exactly one discount per subquote; the user's confirmed choice is applied. After acceptance no entry, selection, or replacement is accepted (Alternative Flow B4).

**B3: Single‑Discount Rule Conflict (Auto‑Applied)**: (REQ-019-035, REQ-019-036)

- Trigger: When a quote is sent, more than one automatic promotion is eligible for the quote, or an automatic promotion is eligible for an option/date-price row that already carries another discount.
- Steps: A quote carries at most one automatic promotion. System silently resolves the conflict using the priority order: patient-entered code > provider discount (provider-selected or provider auto-applied) > Hairline-funded discount > affiliate discount. The usage limit is checked before ranking: an automatic program whose limit is fully reserved or consumed, or whose per-patient limit is reached for a known patient, is skipped, and the next-ranked qualifying program may attach. When several automatic programs qualify, only the highest-ranked remaining one attaches, to every row it is eligible for; the others attach to no row of that quote and reserve no use. On a row that already carries a higher-ranked discount, the automatic promotion is not applied to that row; a provider-selected promotion wins over a provider auto-applied one on the same row. No user prompt is shown.
- Example: A Hairline-funded automatic program and a provider's automatic program are both eligible when a quote is sent. The provider's program ranks higher, so it attaches to every row it is eligible for and one use is reserved for it; the Hairline-funded program attaches to no row of that quote and no use is reserved for it.
- Outcome: Exactly one discount affects the patient's final price; audit records which program was applied and which was superseded. If a valid affiliate-bound code/link was already captured as the patient acquisition source, FR-019 preserves that affiliate attribution metadata for FR-018 even when a provider-side promotion wins the price-discount priority. The capture is stored with the patient's inquiry journey (FR-018 REQ-018-308) and FR-019 reads it at quote acceptance; it is honoured only when the affiliate is Active at that moment, otherwise it earns no credit, no commission and no attribution.

**C1: Hairline-Funded / Direct-Issued Code Redemption**: (REQ-019-037)

- Trigger: Admin issues a Hairline-funded code (open code, segment-bound, or affiliate-distributed) and the patient enters it on one named subquote before acceptance.
- Steps: System validates the code against issuance binding (open vs recipient-bound), records the redemption against the issuing channel (e.g., affiliate id), and calculates commission on the accepted price after the promotion, as for every discount type. For affiliate-bound codes, code generation and affiliate assignment are initiated from FR-018; FR-019 receives the registered code and manages redemption lifecycle.
- Outcome: Patient receives discount; the platform commission and the provider's payout are both reduced, with the provider bearing most of the discount; affiliate (if applicable) accrues the configured incentive (see FR-018), where a percentage affiliate commission is calculated on net revenue after discounts and refunds.

**A3: Automatic Promotion Attachment at Send**: (REQ-019-038)

- Trigger: A provider sends a quote while an auto-applied program is active and eligible for one or more of its option/date-price rows.
- Steps: A quote carries at most one automatic promotion; when several qualify, Alternative Flow B3 picks one. System attaches that program to every eligible option/date-price row of the sent quote and copies its terms into the sent quote version. The provider's entered price on each row stays unchanged, and the discount is shown as a separate line next to it. Rows that are not eligible receive no automatic promotion. Conflicts with another discount on the same row are resolved by Alternative Flow B3. Sending a quote carrying the automatic promotion reserves one use against the program's usage limits. A sent quote holds at most one reserved use: re-sending a new version keeps the existing reservation, creates one only if the new version newly carries the promotion, and releases it if the new version no longer carries the promotion. An admin edit that creates a new version of a sent quote (FR-004) counts as a re-send for these rules. If the limit is already fully reserved or consumed, or the per-patient limit is reached for a known patient, that program is skipped and Alternative Flow B3 picks the next-ranked qualifying program, if any; a promotion never attaches past a full limit.
- Outcome: Each eligible row carries the automatic promotion with terms fixed at send; later edits to the program do not change the sent rows. The reserved use is consumed if the accepted subquote carries the automatic promotion. It is released when the quote expires, is withdrawn, is archived (release reason `archived`), or ends Not Selected or cancelled, and also when a subquote of that quote is accepted that does not carry the automatic promotion (release reason `not_applied`). Restoring an archived quote re-checks the promotion and takes a new reservation; the restore is refused when the limit is used up or the promotion has ended (FR-004 REQ-004-105).
- Exception: an admin-authored replacement quote from an FR-004 provider-fault transfer (Workflow 7) is not sent by a provider. No automatic promotion attaches to it and no use is reserved for it; the admin sets the replacement price directly. The replacement carries no promotion; the original Application is marked Superseded and the use it held returns to the usage limit (General Module Rules, post-acceptance freeze).

**A4: Patient Applies a Code Before Acceptance**: (REQ-019-039)

- Trigger: While reviewing one named subquote and before confirming acceptance, the patient enters a code (FR-005 Alternative Flow A8).
- Steps: System validates the code for that subquote only (active window, eligibility, total and per-patient usage limits, recipient binding, and, for a fixed amount, that the converted amount stays below the row's offered price). If valid, the discounted price is shown next to the provider's offered price; if invalid, the reason is shown and the price stays what the row carried at send, including its attached promotion. The code is held with the open subquote view and stored only on the AcceptanceEvent at acceptance; it is never written to the provider's promotion or quote records. Opening another subquote does not carry the code over.
- Outcome: On acceptance, the discounted price and the applied promotion are frozen into the AcceptanceEvent snapshot.

**A5: Subquote Accepted With a Promotion**: (REQ-019-040)

- Trigger: The patient accepts a subquote that carries a promotion attached at send or a valid patient-entered code.
- Steps: In the same atomic step as the acceptance, the system creates one Application linked to the AcceptanceEvent, the parent quote and version, and the accepted option/date-price row, and reserves one use against the program's usage limits. For an automatic promotion attached at send, the use already reserved at send is consumed instead. If the accepted subquote does not carry the automatic promotion that reserved a use for its parent quote, that reservation is released with reason `not_applied` and the use returns to the limit. Sibling subquotes marked Not Selected and competing quotes never create an Application; any use reserved for them at send is released. A patient code replaces the promotion the row carried: when the replaced promotion is the automatic one, its reservation is released with reason `not_applied` and the code's use is reserved instead. If the total or per-patient usage limit of a provider-selected promotion is used up when the patient confirms, it is handled like an invalid code (FR-005 REQ-005-026): the acceptance does not happen, the reason is shown, and the patient returns to the subquote detail, which shows the row without that promotion. Pausing, revoking or ending the program after send does not affect a sent quote (General Module Rules); only the usage limit can refuse it at acceptance. A patient code entered on a subquote that was not accepted is discarded.
- Outcome: The Application is in state Applied with its use reserved, or consumed for an automatic promotion; the discounted price is read from the acceptance snapshot by every later step.

**B4: Promotion Change Attempted After Acceptance**: (REQ-019-041)

- Trigger: Any actor (patient, provider, or admin) tries to remove, replace, enter, or revalidate a promotion on an accepted subquote, including at checkout or booking.
- Steps: System rejects the action, leaves the Application and the AcceptanceEvent snapshot unchanged, and logs the attempt.
- Outcome: The accepted price stands. The only exception is the provider-fault transfer in FR-006 (Alternative Flow B5), which creates a new linked acceptance record; promotion handling for that case follows the post-acceptance freeze rule in General Module Rules.

---

## Screen Specifications

This module exposes **three promotion programs** under one unified governance model: (REQ-019-042)

1. **Admin-via-Provider** — Admin defines a campaign that affects both Hairline and provider fees; targeted providers must opt-in before the code becomes selectable on their quotes.
2. **Provider Self-Created** — Provider defines a discount on their own quotes; no admin approval required.
3. **Hairline-Funded & Direct-Issued** — Admin defines a Hairline-only discount that is issued directly to patients (open-entry code, patient-segment-bound, affiliate-distributed, or individually issued); providers are not involved in approval.

For every program type, commission is calculated on the accepted price after the promotion, so a discount reduces both the provider's payout and Hairline's commission, and the provider bears most of it. The funding model identifies who creates, approves, and governs a program; it does not keep commission on the price before the promotion. For a Both Fees program, Hairline also reimburses the program's Hairline share % of the discount to the provider at payout, on top of the commission effect (General Module Rules).

All three program types share a single `PromotionProgram` entity (ENT-promotion-program) and are managed through a unified screen system with type-aware filters, forms, and analytics. Admin retains override authority on every program (pause, revoke adoption) and may record a refund through FR-017 regardless of program type. An admin can never force a provider to take part in a program; the overrides an admin has on a provider's adoption are Force-Revoke and Re-invite. No actor, including admin, may void, remove, or change the promotion on an accepted subquote (Alternative Flow B4). (REQ-019-043)

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

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Code / keyword search | text input | No | Search by code text, program name, or keyword | Min 2 chars; 500ms debounce; case-insensitive fuzzy match (REQ-019-107) | ENT-promotion-code.code, ENT-promotion-program.name |
| Filter: Program Type | multi-select | No | Admin-via-Provider, Provider Self-Created, Hairline-Funded & Direct-Issued | OR within field | ENT-promotion-program.program_type |
| Filter: Scope | multi-select | No | Reusable, Ad-Hoc Quote-Bound | Applies primarily to Provider Self-Created programs (see Screen 9 modes) | ENT-promotion-program.scope |
| Filter: Status | multi-select | No | Draft, Active, Paused, Expired, Archived | OR within field | ENT-promotion-program.lifecycle_state |
| Filter: Funding Model | multi-select | No | Both Fees, Hairline Only, Provider Only | Derived from program definition | ENT-promotion-program.funding_model |
| Filter: Provider Participation | dropdown | No | All / specific provider | Provider list from DB; exact match | ENT-promotion-program.targeting |
| Filter: Date Range | date range picker | No | Active-window overlap | Start/end overlap logic | ENT-promotion-program.start_at, ENT-promotion-program.end_at |
| Filter: Usage | range | No | Redeemed count threshold | Min-Max range | ENT-promotion-program.usage_count |
| Filter: ROI | dropdown | No | Admin-defined ROI tier | Exact match | ENT-promotion-program.roi_tier |
| Result Count | label | Yes | Number of matched programs | Updates after every search/filter operation | no graph field (control) |
| Results Table | table | Yes | Displays matched programs with row actions | Columns fixed for MVP | no graph field (control) |

**Results Table Columns**:

| Column | Meaning | Notes | Graph field |
|--------|---------|-------|---|
| Code / Program Name | Code text (or program name when no code) | Primary identifier | ENT-promotion-code.code, ENT-promotion-program.name |
| Program Type | Admin-via-Provider / Provider Self-Created / Hairline-Funded & Direct-Issued | Type badge | ENT-promotion-program.program_type |
| Owner | Admin user or Provider entity that created the program | | ENT-promotion-program.owner |
| Funding Model | Both Fees / Hairline Only / Provider Only | Derived | ENT-promotion-program.funding_model |
| Participating Providers | `All Providers`, provider count, or `N/A` for Direct-Issued | | ENT-promotion-program.targeting |
| Status | Draft / Active / Paused / Expired / Archived | Lifecycle state | ENT-promotion-program.lifecycle_state |
| Active Window | Start and end dates | | ENT-promotion-program.start_at, ENT-promotion-program.end_at |
| Usage | Reserved plus redeemed count vs limit | | ENT-promotion-program.usage_count, ENT-promotion-program.total_usage_limit |
| ROI Tier | Admin-defined band | `Not yet calculated` until data exists | ENT-promotion-program.roi_tier |
| Last Updated | Most recent mutation timestamp | Default descending sort | ENT-promotion-program.updated_at |

**Row Actions**:

- View Detail (opens Screen 2)
- Pause / Resume
- Archive
- View Adoptions (Screen 3) — only for Admin-via-Provider programs
- View Applications (Screen 6, Applications tab pre-filtered to the program)

**Business Rules**:

- All three program types appear in this hub; the Program Type filter narrows the view. (REQ-019-044)
- Provider Self-Created programs appear here so admins can monitor and intervene; admins may pause or archive any program and may change a provider-owned definition only as a logged governance override (see Screen 4). (REQ-019-045)
- Search, filter, result count, and reset behavior must stay aligned with FR-022 control standards. (REQ-019-046)
- Access restricted to authorized admin roles (RBAC enforced per FR-031).

**Acceptance Criteria**:

1. Given the admin opens the Hub, when the screen loads, then the system shows all program types in one list with the default descending Last Updated sort and the result count for the default query. (REQ-019-044)
2. Given the admin applies any combination of Program Type, Status, Funding Model, Provider Participation, Date Range, Usage, and ROI filters, then the catalog returns only rows satisfying all active filters and updates the result count. (REQ-019-044)
3. Given the admin selects a row, then the system opens Screen 2 for that program without losing catalog context. (REQ-019-044)
4. Given the admin triggers Pause on an Active program row, then the program lifecycle transitions to Paused, all existing redemptions remain intact, the program is not attached to newly sent quotes and does not validate new patient codes, and option/date-price rows already sent keep the terms copied at send. (REQ-019-047)

**Notes**:

- Search and filter field definitions are co-owned with FR-022. Any change must be updated in both FR-019 and FR-022. (REQ-019-046)

---

#### Screen 2: Admin — Promotion Detail (Create / Edit)

**Purpose**: Type-aware form to define and govern a promotion program across its full lifecycle.

**Common Data Fields** (all program types):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Program Name | text | Yes | Internal name for the campaign | 3–120 chars (REQ-019-048) | ENT-promotion-program.name |
| Description | textarea | No | Internal notes / patient-facing copy | ≤ 1000 chars (REQ-019-048) | ENT-promotion-program.description |
| Discount Type | select | Yes | Percentage / Fixed amount | Must be one of allowed types | ENT-promotion-program.discount_type |
| Value | number | Yes | Discount value | Percentage: 1 to 100 and not above the configurable maximum discount value (starts at 50 percent); fixed amount: above 0, no cap, but not applied to a row whose offered price it equals or exceeds (REQ-019-114, REQ-019-117) | ENT-promotion-program.value, ENT-promotion-program.currency |
| Applies To | fixed label | Yes | Whole price: the discount reduces the row's single offered price | Not editable; there is no treatment-only or travel-only scope because a quote row has one offered price (FR-004) | ENT-promotion-program.applies_to |
| Code(s) | text or chip list | Conditional | One or many codes per program; required when Application Mode is Code-only, optional otherwise | Format rules; uniqueness enforced (REQ-019-105) | ENT-promotion-code.code |
| Application Mode | select | Yes | Both Fees: List-selection / Code-only / Either. Hairline Only: Auto-applied / Code-only | Auto-applied is rejected on a Both Fees program (REQ-019-103); List-selection and Either are rejected on a Hairline Only program (REQ-019-056); Auto-applied limits in Business Rules | ENT-promotion-program.application_mode |
| Start / End Date | datetime | Yes | Active window | End ≥ Start (REQ-019-048) | ENT-promotion-program.start_at, ENT-promotion-program.end_at |
| Total Usage Limit | number | No | Total redemptions allowed across the program | ≥ 0; blank = unlimited (REQ-019-048) | ENT-promotion-program.total_usage_limit |
| Per-User Usage Limit | number | No | Per-patient cap | ≥ 0; blank = unlimited (REQ-019-048) | ENT-promotion-program.per_user_usage_limit |
| Lifecycle State | controlled | Yes | Draft → Active → Paused → Expired → Archived. Publishing an Admin-via-Provider program makes it Active at once; each targeted provider then accepts or declines (adoption), so there is no program-level approval state. A provider's own Draft is activated by the provider. Who paused is recorded | Forward transitions only, except Pause and Resume; only the side that paused (admin or provider) may resume (REQ-019-049) | ENT-promotion-program.lifecycle_state, ENT-promotion-program.paused_by |

**Type-Specific Fields**:

| Field Name | Applies To | Description | Graph field |
|------------|-----------|-------------|---|
| Funding Model | All | Both Fees (Admin-via-Provider only) / Provider Only (Provider Self-Created only) / Hairline Only (Hairline-Funded only) — auto-set by program type | ENT-promotion-program.funding_model |
| Hairline Share % | Admin-via-Provider (Both Fees) | Required number from 0 to 100: the share of each discount that Hairline reimburses to the provider at payout, on top of the commission effect. Copied into the terms fixed at send | ENT-promotion-program.hairline_share_percent |
| Target Providers | Admin-via-Provider | Multi-select: All Providers, by country (the provider's country), or explicit list | ENT-promotion-program.targeting |
| Approval Routing | Admin-via-Provider | Default vs custom approver per provider entity | ENT-promotion-program.approval_routing |
| Auto-Decline Window | Admin-via-Provider | Business days before an unanswered approval auto-declines; the form shows the default of 3 business days (Setting: promotion approval auto-decline window) | ENT-promotion-program.auto_decline_window_days |
| Issuance Channel | Hairline-Funded & Direct-Issued | Open code / Affiliate-bound (links to FR-018) / Patient-segment-bound / Individually-issued | ENT-promotion-program.issuance_channel |
| Recipient Binding | Hairline-Funded & Direct-Issued | Affiliate ID, segment definition, or recipient list (when channel is bound) | ENT-promotion-code.recipient_binding |
| Bulk Generate Codes | Hairline-Funded & Direct-Issued | Generate N unique codes for distribution; quantity 1–10,000 (REQ-019-058) | no graph field (control) |

**Audit Trail Panel**:

- All state changes, edits, approvals, and override actions are listed in chronological order with actor, timestamp, reason, and the old and new values for edits. (REQ-019-057) (ENT-audit-entry.action, ENT-audit-entry.actor_id, ENT-audit-entry.timestamp, ENT-audit-entry.reason, ENT-audit-entry.before, ENT-audit-entry.after)

**Business Rules**:

- `Funding Model` is derived from `Program Type` and cannot be set independently. (REQ-019-050)
- For Admin-via-Provider, publishing the program (Draft to Active) notifies targeted providers, who each accept or decline (S-03; approval-requested event of the FR-030 notification catalogue). There is no program-level Pending Approval: approval is per provider adoption, and the program applies only to providers whose adoption is Accepted. If every provider declines, the program stays Active with no participants until archived. (REQ-019-051)
- Hairline-Funded programs do not appear in provider selection UIs (per Provider Part 2 L3–8).
- `Application Mode = Auto-applied` is only allowed for programs with `Funding Model = Hairline Only` or `Provider Only` and only when the program's own fields on this screen define who it applies to: Start / End Date, the usage limits and, for a Hairline Only program, Issuance Channel and Recipient Binding (together the eligibility checked at send and at code validation); it cannot be auto-applied across multiple providers without consent. A Hairline Only program may use only Auto-applied or Code-only: List-selection and Either are not offered for it, because providers never see it in selection UIs. Auto-applied programs attach when a quote is sent (Alternative Flow A3). They never attach to an admin-authored replacement quote, and no use is reserved for one. (REQ-019-052)
- `Hairline Share %` is required for Both Fees programs and must be a number from 0 to 100; it is hidden for other funding models. It is part of the terms fixed at send and frozen at acceptance, so an edit applies only to quotes sent afterwards. Every change is recorded in the Audit Trail Panel with actor, timestamp, and old and new values. (REQ-019-053)
- When an admin changes the Value or the Hairline Share % of a Both Fees program that providers have adopted, every adopting provider is notified with the old and new terms. The change applies only to quotes sent afterwards; each adoption stays Accepted, and the provider may revoke it as before (Screen 7). (REQ-019-118)
- A `Fixed amount` value carries a currency. When the program is attached to a sent quote, the discount is converted from the program currency into the quote currency at the FR-029 currency conversion rate (including markup) in effect at the moment of send; no conversion is needed when the currencies match. The converted amount is part of the terms fixed at send and does not change if rates move later. For a patient-entered code the amount is converted at the rate in effect when the code is validated, and the amount shown at confirm is the one frozen at acceptance. When the converted fixed amount would be equal to or more than the offered price of the row, the promotion is not attached (or the patient's code is refused), the reason is shown, and the price is unchanged. (REQ-019-117)
- Bulk upload / bulk edit available for campaign management. (REQ-019-054)

**Acceptance Criteria**:

1. Given the admin creates an Admin-via-Provider program and publishes it, then the program is Active and the targeted providers receive S-03 notifications, each with its own accept or decline.
2. Given the admin creates a Hairline-Funded program with `Issuance Channel = Open code` and a single code, when the program is published, then the code is immediately redeemable by any patient on a named subquote before acceptance and the program does not appear in any provider's adoption inbox. (REQ-019-055)
3. Given the admin edits the Value of a Paused program and republishes, then the new value applies only to quotes sent and patient codes validated from that point forward; quotes already sent keep the terms copied at send, and prior redemptions retain their original values in audit. (REQ-019-108)
4. Given the admin sets `Application Mode = Auto-applied` on an Admin-via-Provider program and attempts to save, then the system rejects the submission with an inline validation error: "Auto-applied is not permitted for Both-Fees programs." (REQ-019-103)
5. Given the admin saves an Admin-via-Provider program, when `Hairline Share %` is blank or outside 0 to 100, then the save is rejected with an inline validation error; when it is valid, then the value is saved, recorded in the Audit Trail Panel, and shown with the program terms in the provider's adoption request.
6. Given the admin sets `Application Mode = List-selection` or `Either` on a Hairline-Funded program and attempts to save, then the system rejects the submission with an inline validation error. (REQ-019-056)
7. Given an admin changes the Value or the Hairline Share % of an Admin-via-Provider program that providers have adopted, then each adopting provider is notified with the old and new terms, the adoptions stay Accepted, and the new terms apply only to quotes sent afterwards. (REQ-019-118)

**Notes**:

- The form must hide irrelevant sections based on Program Type to reduce cognitive load (e.g., no Approval Routing for Hairline-Funded). (REQ-019-101)
- Application Mode choices follow the funding model. Both Fees programs offer `List-selection / Code-only / Either` and never `Auto-applied`. Hairline Only programs offer only `Auto-applied / Code-only`, because Hairline-Funded programs do not appear in provider selection UIs and List-selection or Either would never reach a patient. Provider Self-Created programs offer all four choices, with `Auto-applied` limited as stated on Screen 2. A provider selects an admin program on a quote only from the list of programs the provider has adopted through the approval workflow (Screen 7), never before adoption. (REQ-019-056)

---

#### Screen 3: Admin — Provider Adoption Manager

**Purpose**: For a given Admin-via-Provider program, show every targeted provider's adoption status and let admins Force-Revoke or Re-invite.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Program Header | panel | Yes | Program name, dates, value, funding model | Read-only summary | ENT-promotion-program.name, ENT-promotion-program.start_at, ENT-promotion-program.end_at, ENT-promotion-program.value, ENT-promotion-program.funding_model |
| Provider Row | table row | Yes | One row per targeted provider | | ENT-promotion-adoption |

**Adoption Row Columns**:

| Column | Meaning | Graph field |
|--------|---------|---|
| Provider | Provider name + country | ENT-provider.name, ENT-provider.country |
| Status | Pending / Accepted / Declined / Auto-Declined / Revoked-by-Provider / Revoked-by-Admin | ENT-promotion-adoption.status |
| Decided At | Timestamp of last decision | ENT-promotion-adoption.decided_at |
| Decided By | Provider user or admin user (for overrides) | ENT-promotion-adoption.decided_by |
| Comment | Optional comment from the deciding actor (≤ 500 chars) (REQ-019-106) | ENT-promotion-adoption.comment |
| Redemptions | Count of redemptions on this provider's quotes under this program | ENT-promotion-adoption.redemption_count |
| Admin Actions | Re-invite / Force-Revoke | no graph field (control) |

**Business Rules**:

- Force-Revoke immediately removes the program from the provider's quote-creation selection list; in-flight quotes with the program already applied are preserved. (REQ-019-059)
- Re-invite resets the provider's status from Declined, Auto-Declined, Revoked-by-Provider or Revoked-by-Admin back to Pending and re-sends the S-03 notification. (REQ-019-060)
- All admin overrides are logged with mandatory reason text in the audit trail. (REQ-019-061)
- Force-Revoke and Re-invite are the only admin overrides on an adoption; an admin can never accept on a provider's behalf or force a provider into a program. (REQ-019-109)

**Acceptance Criteria**:

1. Given a provider has Status = Accepted, when the admin triggers Force-Revoke with reason, then the provider's status changes to Revoked-by-Admin and the program disappears from that provider's quote-creation list within 5 seconds. (REQ-019-059)
2. Given the program's Auto-Decline Window elapses without a provider decision, then the provider's status updates to Auto-Declined and is visible in this manager. (REQ-019-062)

---

#### Screen 4: Admin — Provider Promotion Portfolio

**Purpose**: Per-provider drill-down showing every promotion record tied to that provider — both admin programs they have adopted and their self-created programs — so admins can assess each provider's promotional behaviour and impact.

**Data Fields**:

| Field Name | Type | Required | Description | Graph field |
|------------|------|----------|-------------|---|
| Provider Header | panel | Yes | Provider name, country, contact, adoption-rate KPIs | ENT-provider.name, ENT-provider.country, ENT-provider.email, ENT-provider.phone, ENT-promotion-report-snapshot.adoption_rate |
| Filter: Record Type | multi-select | No | Adopted-Admin / Self-Created | ENT-promotion-program.program_type |
| Filter: Status | multi-select | No | Draft / Active / Paused / Expired / Archived | ENT-promotion-program.lifecycle_state |
| Filter: Date Range | date range picker | No | Active-window overlap | ENT-promotion-program.start_at, ENT-promotion-program.end_at |
| Results Table | table | Yes | Promotion records for this provider | no graph field (control) |

**Results Table Columns**:

| Column | Meaning | Graph field |
|--------|---------|---|
| Program Name | Internal name | ENT-promotion-program.name |
| Record Type | Adopted-Admin / Self-Created | ENT-promotion-program.program_type |
| Funding Model | Both Fees / Provider Only | ENT-promotion-program.funding_model |
| Status | Lifecycle state | ENT-promotion-program.lifecycle_state |
| Active Window | Start–End | ENT-promotion-program.start_at, ENT-promotion-program.end_at |
| Redemptions | Count under this provider | ENT-promotion-adoption.redemption_count |
| Revenue Impact | Total discount issued (Hairline portion + provider portion split) | ENT-promotion-application.hairline_portion, ENT-promotion-application.provider_portion |
| Row Action | Open program detail (Screen 2 in read-only mode for self-created) | no graph field (control) |

**KPI Header Strip**:

- Adoption Rate: % of admin programs offered that this provider accepted (ENT-promotion-report-snapshot.adoption_rate)
- Self-Created Active Count (ENT-promotion-report-snapshot.self_created_active_count)
- Total Redemptions (last 7 / 30 / 90 / 365 days) (ENT-promotion-report-snapshot.total_redemptions)
- Total Discount Issued (currency) (ENT-promotion-report-snapshot.total_discount_issued)

**Business Rules**:

- Admin may open Screen 2 in read-only mode for provider self-created programs; editing is reserved for the provider unless an override is needed (governance action, logged in audit). (REQ-019-045)
- Admin may pause or archive any provider self-created program via row action with mandatory reason text. (REQ-019-045)

**Notes — Scope Expansion**:

- Per client transcription (Admin Part 1 L295–300), the client originally stated admin would *"never going to pick them or change them or amend them in reality"* for provider self-created discounts. This portfolio screen **deliberately extends beyond that original scope** to give admins governance visibility and override authority across the entire promotion system. Recorded in Change Log v1.4.

---

#### Screen 5: Admin — Hairline-Funded & Direct-Issued Codes Manager

**Purpose**: Specialized manager for the third program type — codes that Hairline funds and issues directly through open distribution, patient segments, or affiliate channels.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Program Selector | dropdown | Yes | Choose a Hairline-Funded program | From Screen 1 filtered list | ENT-promotion-program.name |
| Issuance Channel | label | Yes | Open / Affiliate-bound / Segment-bound / Individually-issued | From program definition | ENT-promotion-program.issuance_channel |
| Codes Table | table | Yes | One row per code (or per recipient for bound channels) | | ENT-promotion-code.code |
| Bulk Generate | action | No | Generate N unique codes | Per program total-limit | no graph field (control) |
| Bulk Revoke | action | No | Revoke selected codes | Mandatory reason (REQ-019-104) | no graph field (control) |
| Export | action | No | CSV / XLSX export of code list with redemption status | | no graph field (control) |

**Codes Table Columns**:

| Column | Meaning | Graph field |
|--------|---------|---|
| Code | Unique code string | ENT-promotion-code.code |
| Recipient Binding | Affiliate name / Segment name / Patient identifier / `Open` | ENT-promotion-code.recipient_binding |
| Issued At | Generation timestamp | ENT-promotion-code.issued_at |
| Issued By | Admin user | ENT-promotion-code.issued_by |
| Redemption Status | Unused / In-Progress (use reserved by an accepted subquote) / Redeemed (first successful payment) / Revoked / Expired | ENT-promotion-code.status |
| Redeemed By | Patient identifier when redeemed | ENT-patient.anonymized_id |
| Redeemed At | Timestamp | ENT-promotion-application.completed_at |
| Discount Issued | Currency amount | ENT-promotion-application.discount_value |

**Business Rules**:

- Open codes have one code that any eligible patient may use until the total usage limit is reached. (REQ-019-063)
- Affiliate-bound codes integrate with FR-018; FR-018 owns generation and one-affiliate-per-code assignment, while FR-019 owns validation and redemption state. Redemptions accrue incentive to the linked affiliate. Affiliate codes follow the same usage rule as every code: one use is reserved at acceptance and consumed at the first payment, and there is no code entry at checkout.
- Segment-bound codes validate the patient against the segment definition at entry time. (REQ-019-064)
- Individually-issued codes are single-use and bound to a specific patient identifier. (REQ-019-065)
- When FR-018 registers a generated code, FR-019 rejects the registration with a named reason when the code text already exists on the platform (REQ-019-076) or the chosen program is not an Affiliate-bound program; FR-018 shows the returned reason on that row and the admin retries. (REQ-019-119)
- Revoking a code stops it from validating on any subquote not yet accepted. A use already reserved by an accepted subquote (`In-Progress`) stays frozen with the acceptance and is not cancelled by the revoke. (REQ-019-066)

**Acceptance Criteria**:

1. Given the admin starts affiliate-bound code generation in FR-018 for 50 selected affiliates and the program's channel = Affiliate-bound, when FR-018 completes generation, then 50 unique codes are registered with this program, each bound to exactly one affiliate, and each appears in the table with status = Unused. (REQ-019-067)
2. Given a patient enters an Affiliate-bound code on a named subquote and accepts it, when the first payment succeeds, then the corresponding row updates to Redeemed and the affiliate's incentive accrual (per FR-018) is triggered. (REQ-019-068)

---

#### Screen 6: Admin — Promotion Analytics & Applications

**Purpose**: Combined operational + analytical surface that consolidates the prior client-mentioned "Applied discounts" and "Completed discounts" screens (Admin Part 1 L333–344) into one place with two complementary tabs.

##### Tab 1: Overview (Analytics)

**KPI Cards**:

- Active Programs (count by program type) (ENT-promotion-report-snapshot.active_programs_count)
- Total Redemptions (last 7 / 30 / 90 / 365 days) (ENT-promotion-report-snapshot.total_redemptions)
- Total Discount Value Issued (Hairline portion + provider portion + total) (ENT-promotion-report-snapshot.total_discount_value_issued, ENT-promotion-report-snapshot.hairline_portion_total, ENT-promotion-report-snapshot.provider_portion_total)
- Redemption Funnel: Issued → Code Entered → Validated → In-Progress → Completed; Code Entered and Validated are counted from the logged code validation requests (ENT-promotion-report-snapshot.redemption_funnel)
- ROI by Program Type (Hairline's share; see Analytics Definitions below) (ENT-promotion-report-snapshot.roi_by_program_type)
- Top 10 Programs by Redemptions (ENT-promotion-report-snapshot.top_programs_by_redemptions)
- Top 10 Programs by Discount Value (ENT-promotion-report-snapshot.top_programs_by_discount_value)

**Filters**: Date range, program type, funding model, provider, country.

**Analytics Definitions** (apply to Screen 6, Screen 10 and the Screen 7 preview):

- **ROI Estimate (per program)**: net gain over discount cost, shown as a percentage: (revenue from bookings that used the program minus the discount given) divided by the discount given. Admin screens count Hairline's share of the revenue and the discount; provider screens count the provider's share. It shows `Not yet calculated` until the program has at least one redemption. The ROI Tier on Screen 1 is the admin-defined band that the ROI falls in. (REQ-019-111)
- **Conversion Lift**: the acceptance percentage of quotes carrying the program minus the acceptance percentage of quotes without any promotion, for the same provider (the whole platform on admin screens) and the same period, in percentage points. "Where measurable" means both sides have at least the admin-set minimum number of quotes (launch default: 20 quotes on each side); below that the lift is not shown. (REQ-019-112)
- **Financial Impact Preview** (Screen 7): the provider's booking value in the last 30 days x the discount % x the provider's funded share of the discount. (REQ-019-113)

##### Tab 2: Applications (Redemption Log)

One row per redemption event with the full state lifecycle preserved.

**Columns**:

| Column | Meaning | Graph field |
|--------|---------|---|
| Redemption ID | Unique identifier | ENT-promotion-application.id |
| Code | Code redeemed (or auto-applied marker) | ENT-promotion-code.code |
| Program | Program name + type | ENT-promotion-program.name, ENT-promotion-program.program_type |
| State | **Applied** (created at subquote acceptance; one use reserved for a provider-selected promotion or patient code, or already consumed for an automatic promotion) vs **Completed** (first successful payment; the reserved use is consumed, and for an automatic promotion Completed only marks the first payment) — distinct states per client transcription | ENT-promotion-application.state |
| Patient | Patient identifier | ENT-patient.anonymized_id |
| Provider | Provider on the accepted subquote | ENT-provider.name |
| Quote / Subquote / Acceptance / Booking ID | Links to the parent quote and version, the accepted option/date-price row, the AcceptanceEvent, and the booking | ENT-promotion-application.quote_id, ENT-promotion-application.quote_version, ENT-promotion-application.quote_option_date_price_id, ENT-promotion-application.acceptance_event_id, ENT-promotion-application.booking_id |
| Source | Provider-selected at send, automatic at send, or patient-entered code | ENT-promotion-application.source |
| Discount Value | Amount in the quote currency, read from the acceptance snapshot | ENT-promotion-application.discount_value |
| Funding Split | Hairline portion / Provider portion (follows the commission effect for every program type; see General Module Rules) | ENT-promotion-application.hairline_portion, ENT-promotion-application.provider_portion |
| Applied At | Timestamp of state = Applied | ENT-promotion-application.applied_at |
| Completed At | Timestamp of state = Completed (blank if not yet) | ENT-promotion-application.completed_at |
| Status | Active / Voided / Superseded / Refunded | ENT-promotion-application.status |
| Admin Actions | View Detail; Refund on Completed rows only | no graph field (control) |

**Business Rules**:

- The two-state distinction (Applied vs Completed) is preserved per client request (Admin Part 1 L341–344). Applied = the subquote carrying the promotion has been accepted and, for a provider-selected promotion or patient code, one use is reserved at that moment (entering a code never counts against a limit); Completed = the first payment for that booking has succeeded and that reserved use is consumed. For an automatic promotion the use is already consumed at acceptance, so Completed only marks the first payment. (REQ-019-069)
- Voided is set only by the system, when the booking reaches `Payment Window Expired` or is cancelled, except for a provider-fault transfer, where Superseded takes precedence; the reserved use is then released. For an automatic promotion, the use consumed at acceptance returns to the usage limit when the row is Voided before the first payment. Superseded is set only by the system when a provider-fault transfer replaces the accepted record, and the use it held returns to the usage limit. A Voided Application returns to its Active status only through an admin revive of the booking, which also clears `use_returned_at`. There is no admin Void action. (REQ-019-070)
- Refund actions are logged with mandatory reason and integrate with FR-017 (Billing & Finance) for monetary reconciliation. They never change the accepted price or the AcceptanceEvent snapshot. (REQ-019-071)
- Drilling from a KPI card on the Overview tab filters the Applications tab accordingly. (REQ-019-102)

**Acceptance Criteria**:

1. Given an accepted subquote with an Applied redemption, when the first payment for the booking succeeds, then the redemption row transitions from State = Applied to State = Completed, the reserved use is consumed (for an automatic promotion the use was already consumed at acceptance and is not counted again), and the change is reflected in Overview KPIs within 5 seconds. (REQ-019-072)
2. Given an admin triggers Refund on a Completed redemption with reason, then the row Status updates to Refunded, the audit log captures actor/time/reason, and FR-017 receives a reconciliation event.
3. Given an Applied redemption, when its booking reaches `Payment Window Expired` or is cancelled, then the row Status becomes Voided, the reserved use is released (or, for an automatic promotion, the use consumed at acceptance returns to the limit), and the AcceptanceEvent snapshot is unchanged.
4. Given an admin opens an Applied redemption, then no void, remove, replace, or price-change action is offered.

---

### Provider Platform Screens (PR-02 / PR-05)

#### Screen 7: Provider — Admin Campaigns

**Purpose**: Single hub for admin-originated campaigns offered to this provider, covering both pending invitations and current adoptions.

**Tabs**: (ENT-promotion-adoption.status)

- **Pending** — Campaigns awaiting accept / decline decision
- **Active** — Accepted campaigns currently in their active window; revoke control available
- **Past** — Declined, Auto-Declined or Revoked campaigns, and campaigns whose program end date has passed (an end-date filter on the program, not an adoption status)

**Campaign Card / Row Fields**:

| Field | Description | Graph field |
|-------|-------------|---|
| Program Name | From admin definition | ENT-promotion-program.name |
| Description | Patient-facing copy | ENT-promotion-program.description |
| Discount Type / Value | e.g. "40% off" | ENT-promotion-program.discount_type, ENT-promotion-program.value |
| Active Window | Start–End | ENT-promotion-program.start_at, ENT-promotion-program.end_at |
| Financial Impact Preview | Estimated impact on provider revenue: the provider's booking value in the last 30 days x discount % x the provider's funded share of the discount | ENT-promotion-adoption.financial_impact_preview |
| Decision Buttons (Pending tab) | Accept / Decline with optional comment (≤ 500 chars) (REQ-019-106) | ENT-promotion-adoption.comment |
| Revoke Adoption (Active tab) | Removes the program from this provider's quote-creation list | no graph field (control) |
| Decision Timestamp | When the provider decided | ENT-promotion-adoption.decided_at |

**Business Rules**:

- All decisions logged with timestamp and user (Provider Part 2 L11–14).
- Revoking adoption does not affect quotes that already have the program applied; only new selections are blocked. (REQ-019-073)
- Auto-Decline triggers if the Auto-Decline Window (Screen 2) elapses without a decision. (REQ-019-062)

**Acceptance Criteria**:

1. Given a Pending campaign is shown, when the provider clicks Accept and confirms, then the campaign moves to the Active tab and becomes selectable in quote creation per FR-004 within 5 seconds. (REQ-019-029)
2. Given an Active campaign, when the provider clicks Revoke Adoption with reason, then the campaign moves to Past with state = Revoked-by-Provider and is no longer offered in quote creation. (REQ-019-074)

---

#### Screen 8: Provider — My Promotions (List)

**Purpose**: List view of every provider self-created promotion.

**Filter Bar**: Status (Draft / Active / Paused / Expired / Archived), date range, keyword search.

**Results Table Columns**:

| Column | Meaning | Graph field |
|--------|---------|---|
| Promotion Name | Internal name | ENT-promotion-program.name |
| Code | Code text (or `—` if none) | ENT-promotion-code.code |
| Type / Value | e.g. "Percentage / 15%" | ENT-promotion-program.discount_type, ENT-promotion-program.value |
| Active Window | Start–End | ENT-promotion-program.start_at, ENT-promotion-program.end_at |
| Status | Lifecycle state | ENT-promotion-program.lifecycle_state |
| Redemptions | Count | ENT-promotion-program.redemption_count |
| Savings Issued | Currency total | ENT-promotion-program.savings_issued |
| Row Actions | Edit / Activate (Draft only) / Pause / Resume (only a pause the provider made) / Archive / View Applications (links to Screen 10 pre-filtered) | no graph field (control) |

**Business Rules**:

- Provider may have an arbitrary number of self-created promotions concurrently active, subject to the platform's single-discount-per-subquote rule at redemption time. (REQ-019-075)
- Code uniqueness enforced platform-wide (cannot collide with admin codes or other providers' codes). (REQ-019-076)

---

#### Screen 9: Provider — Promotion Detail (Create / Edit)

**Purpose**: Form for the provider to create or edit a self-created promotion. The screen is reachable through **two entry modes**, which together cover both of the patterns described in FR-004 Screen 1 (Quote Creation):

- **Mode 1 — Standalone (from PR-02 / PR-05 navigation):** Provider creates a reusable promotion ahead of time. `scope = REUSABLE`. The promotion is selectable from the list on FR-004 Screen 1 (Promotion field) for any future quote.
- **Mode 2 — Inline (modal opened from FR-004 Screen 1 during quote drafting):** Provider creates an on-the-spot promotion for one option/date-price row. `scope = AD_HOC_QUOTE_BOUND`, with `bound_quote_id` retaining parent-quote containment and `bound_quote_option_date_price_id` identifying the only row that may apply it. A "Save as reusable program for future quotes" toggle, when enabled, promotes the record to `scope = REUSABLE` on submit and clears both bindings.

Both modes use the same form schema below; mode-specific behaviour is noted in the rules.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Promotion Name | text | Yes | Display name | See REQ-019-048. | ENT-promotion-program.name |
| Description | textarea | No | Patient-facing copy | See REQ-019-048. | ENT-promotion-program.description |
| Discount Type | select | Yes | Percentage / Fixed amount | Per policy caps | ENT-promotion-program.discount_type |
| Value | number | Yes | Discount value | Same as the admin form: percentage 1 to 100 and not above the configurable maximum (starts at 50 percent); fixed amount above 0, no cap | ENT-promotion-program.value |
| Applies To | fixed label | Yes | Whole price | Not editable (see Screen 2) | ENT-promotion-program.applies_to |
| Code | text | **Optional** | Optional code for marketing distribution | Format rules; uniqueness platform-wide | ENT-promotion-code.code |
| Application Mode | select | Yes | List-selection during quote (default) / Auto-applied / Code-only / Either | Code-only requires Code field; all four choices; Auto-applied limits as stated on Screen 2 (REQ-019-105) | ENT-promotion-program.application_mode |
| Start / End Date | datetime | Yes | Active window | Mode 1: end ≥ start. Mode 2: defaults to the active window of the bound quote (REQ-019-082) | ENT-promotion-program.start_at, ENT-promotion-program.end_at |
| Total Usage Limit | number | No | Total redemptions | ≥ 0; blank = unlimited. Mode 2 forces total limit = 1 unless "Save as reusable" is toggled (REQ-019-082) | ENT-promotion-program.total_usage_limit |
| Per-User Usage Limit | number | No | Per-patient cap | See REQ-019-048. | ENT-promotion-program.per_user_usage_limit |
| Save as reusable (Mode 2 only) | toggle | No | Promote ad-hoc record to a reusable program after this quote | When ON, `scope` becomes `REUSABLE` on submit | ENT-promotion-program.scope |

**Business Rules**:

- The **Code field is optional** per a deliberate scope decision. The client transcription (Provider Part 2 L27–33) stated codes are not relevant for provider self-created discounts since providers select them from a list during quote creation. This FR retains the field as **optional** so providers may also issue code-based promotions for marketing distribution (e.g., flyer codes, partner promos). Default Application Mode is `List-selection during quote`. (REQ-019-077)
- **Mode 2 ad-hoc records** are scoped to a single quote and are not shown in the list-selection picker on other quotes' creation screens. They remain visible to admin in Screen 1 Hub (Scope filter = Ad-Hoc Quote-Bound) and Screen 4 Portfolio. (REQ-019-078)
- Free-text "promotion note" entries are **not supported**: every discount applied to an option/date-price row must correspond to a structured `PromotionProgram` record (Mode 1 or Mode 2). FR-004's legacy `promotionNote` field is removed in FR-004 v1.8.
- Funding Model is fixed at `Provider Only` and is not user-editable. (ENT-promotion-program.funding_model)
- No admin approval is required for activation in either mode; the provider activates its own Draft.
- A promotion selected on an option/date-price row may be changed only while the quote is drafted or revised in FR-004 before acceptance. Its terms are copied into the sent quote version when the quote is sent, and a promotion can apply only to a row it was attached to at send. (REQ-019-079)

**Acceptance Criteria**:

1. Given the provider saves a Mode 1 (standalone) promotion with no Code and Application Mode = List-selection, then the promotion is available for list-selection during FR-004 Screen 1 quote creation within its active window.
2. Given the provider saves a Mode 1 promotion with a Code and Application Mode = Code-only, then the promotion is not shown in the quote-creation selection list but is redeemable when the patient enters the code on a named subquote of that provider's quote before acceptance. (REQ-019-080)
3. Given the provider opens the inline modal for an FR-004 option/date-price row and saves an ad-hoc promotion without enabling "Save as reusable", then a new `PromotionProgram` with `scope = AD_HOC_QUOTE_BOUND` is created, both binding IDs are set, that row's `promotionId` is set, and the record is not offered on any other option/date-price row's selection list.
4. Given the provider saves a Mode 2 ad-hoc promotion with "Save as reusable" enabled, then `scope = REUSABLE` is recorded and the promotion becomes selectable on future quotes within its active window. (REQ-019-081)
5. Given an ad-hoc promotion bound to one option/date-price row, when any request tries to apply it to another row or another quote, then the system rejects the request with a clear reason and no row price changes.

**Notes — Scope Note**:

- Retaining the optional Code field for provider self-created promotions is an extension beyond the client transcription. Recorded in Change Log v1.4.
- The Mode 1 / Mode 2 split aligns FR-019 with FR-004's existing `select/text` Promotion field on Quote Creation (FR-004 Screen 1). The unstructured free-text path (`quote.promotionNote`) is removed in FR-004 v1.8 in favour of structured Mode 2 ad-hoc records. Recorded in Change Log v1.5.

---

#### Screen 10: Provider — Promotion Analytics & Applications

**Purpose**: Provider-scoped mirror of Screen 6, covering both the provider's self-created promotions and admin campaigns they have adopted.

##### Tab 1: Overview (Analytics)

- Redemptions (last 7 / 30 / 90 / 365 days) (ENT-promotion-report-snapshot.total_redemptions)
- Savings Issued (total + per-program) (ENT-promotion-report-snapshot.savings_issued)
- Conversion Lift vs baseline (per program where measurable; definition under Analytics Definitions on Screen 6) (ENT-promotion-report-snapshot.conversion_lift)
- ROI Estimate per program (provider screens count the provider's share; definition under Analytics Definitions on Screen 6) (ENT-promotion-report-snapshot.roi_estimate)
- Adopted-Admin vs Self-Created split (ENT-promotion-report-snapshot.adopted_vs_self_created_split)
- Top performing programs (ENT-promotion-report-snapshot.top_programs_by_redemptions)

##### Tab 2: Applications (Quote / Case Manager)

One row per redemption tied to this provider's quotes / treatment cases.

**Columns**:

| Column | Meaning | Graph field |
|--------|---------|---|
| Redemption ID | Unique identifier | ENT-promotion-application.id |
| Code / Program | Code or program name | ENT-promotion-code.code, ENT-promotion-program.name |
| State | Applied / Completed (preserves admin-side semantics) | ENT-promotion-application.state |
| Patient | Masked patient code until the first payment succeeds (anonymised until payment); the patient identifier once it has | ENT-patient.anonymized_id |
| Quote / Case ID | Link to FR-004 / FR-010 entity | ENT-promotion-application.quote_id, ENT-treatment-record.id |
| Discount Value | Currency amount | ENT-promotion-application.discount_value |
| Applied At / Completed At | Timestamps | ENT-promotion-application.applied_at, ENT-promotion-application.completed_at |
| Row Actions | View Quote / View Case | no graph field (control) |

**Business Rules**:

- Screen 10 offers no remove or replace action. A provider changes the promotion on an option/date-price row only while drafting or revising the quote in FR-004 before acceptance (Screen 9 Business Rules); once the subquote is accepted, the promotion is frozen in the AcceptanceEvent snapshot.
- The provider cannot refund a Completed redemption; that authority sits with admin (Screen 6). (REQ-019-083)

**Acceptance Criteria**:

1. Given an Applied redemption on an accepted subquote, when the provider opens the row, then no remove, replace, or price-change action is available and the discount shown matches the acceptance snapshot.

---

### Patient Platform Screens (P-03 overlay)

#### Screen 11: Patient — Apply Discount Before Acceptance

**Purpose**: Validate and apply a single discount code on one named subquote while the patient reviews it, before acceptance (FR-005 Screen 2, Alternative Flow A8).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Code input | text | No | Optional discount code for the named subquote | Format rules; 1 active code at a time on that subquote; not available after acceptance | ENT-acceptance-event.promotion_code |
| Price breakdown | panel | Yes | Provider's offered price, discount line, totals | Provider price shown as entered; discount shown as a separate line | ENT-subquote.offered_price, ENT-subquote.price_after_promotion, ENT-acceptance-event.discounted_price |

**Business Rules**:

- One discount per subquote; entering a new code prompts the patient to confirm replacement of the current discount on that subquote.
- The code applies only to the named subquote and is not carried to another subquote. It is held with the open subquote view, stored only on the AcceptanceEvent at acceptance, and never written to the provider's promotion or quote records.
- Validation occurs when the code is entered and again when the patient confirms acceptance. A fixed amount is converted at the rate in effect at each validation, and the amount shown at confirm is the one frozen at acceptance. On acceptance, the discounted price is frozen into the AcceptanceEvent snapshot. (REQ-019-084)
- No code entry, removal, or replacement is available after acceptance, including at checkout or payment; payment screens show the frozen accepted price.
- Clear feedback for invalid / expired / limit-reached / segment-mismatched codes. (REQ-019-033)
- The discount is shown as one separate line that reduces the whole price. (REQ-019-085)

**Acceptance Criteria**:

1. Given a patient enters a valid code, when validation succeeds, then for 95% of valid codes the price breakdown updates within 1 second and shows the discount as a separate line. (REQ-019-085)
2. Given a patient enters a code on a subquote that already has a discount, when the patient confirms replacement, then the previous discount is replaced on the patient's selection for that subquote only, the provider's promotion record is unchanged, and audit records both events.
3. Given a patient applies a valid code on subquote A, when the patient opens subquote B, then subquote B shows its own offered price without the code.
4. Given a patient has accepted a subquote, when the patient reaches checkout or payment, then no code input is shown, the price equals the acceptance snapshot, and any request to apply a code is rejected.

---

## Business Rules

### General Module Rules

- Single‑discount rule enforced globally. Conflict resolution depends on how the conflict arises: (a) **user-initiated** — system prompts the user to confirm replacement (see Alt Flow B2); (b) **auto-applied** — system silently resolves using priority order: patient-entered code > provider discount (provider-selected or provider auto-applied) > Hairline-funded discount > affiliate discount, with no user prompt; a provider-selected promotion wins over a provider auto-applied one on the same row (see Alt Flow B3).
- Promotion terms are fixed at send. When a quote is sent, the terms of each option/date-price row's promotion (type, value, applies-to, funding model, Hairline share % for Both Fees programs, and the discount amount in the quote currency) are copied into the sent quote version. Later edits, pausing, expiry, or archiving of the program do not change a sent row.
- Active dates, eligibility, and usage limits (the total limit and the per-patient limit, REQ-019-116) are checked when a promotion is attached to a row at send (the per-patient limit only for a known patient), when a patient code is validated before acceptance, and, for the usage limits of a provider-selected promotion, when the patient confirms acceptance (Alternative Flow A5). If a promotion the provider selected cannot attach at send (its limit is used up, the program is paused or ended, the provider's adoption is revoked, or its fixed amount equals or exceeds the row's offered price), the provider sees the reason and the quote is sent without that promotion only after the provider confirms; a draft quote that holds a revoked or paused program drops it the same way. An archived quote that is restored re-checks its promotion and takes a new reservation, and the restore is refused when the limit is used up or the promotion has ended (FR-004 REQ-004-105). (REQ-019-086)
- A quote carries at most one automatic promotion. The automatic program chosen by the priority order attaches at send to every eligible option/date-price row that does not already carry a higher-ranked discount. The provider's entered price stays unchanged and the discount is shown separately.
- A promotion applies only to an option/date-price row it was attached to at send, or to the one named subquote on which the patient entered a code. Any other application is rejected. (REQ-019-087)
- Promotion usage lifecycle for provider-selected promotions and patient-entered codes: one use is reserved when the subquote is accepted, consumed when the first payment succeeds, and released when the booking reaches `Payment Window Expired` or is cancelled; when an admin revives a `Payment Window Expired` booking (FR-006), the use is re-reserved and the Application returns from Voided to its Active status, and the revive is rejected if the usage limit is exhausted.
- Code status on release or void: the code's In-Progress count drops and a single-use code returns to Unused. A revoked code stays revoked, and its reservations run their course. A refund after the first payment does not return the use; a use returns only when the booking is cancelled or expires before the first payment, or when a provider-fault transfer replaces the booking (Superseded).
- Promotion usage lifecycle for auto-applied promotions: sending a quote carrying the promotion reserves one use. A sent quote holds at most one reserved use: re-sending a new version keeps the existing reservation, creates one only if the new version newly carries the promotion, and releases it if the new version no longer carries the promotion. The reservation is released when the quote expires (`expired`), is withdrawn (`withdrawn`), is archived (`archived`), ends Not Selected because another subquote or quote was accepted (`not_selected`), loses the promotion in a re-sent version (`dropped_on_resend`), is cancelled before acceptance because the inquiry was cancelled or the provider's status changed (`cancelled`), or a subquote of that quote is accepted that does not carry the promotion (`not_applied`); it is consumed when the accepted subquote carries the promotion. If the booking then reaches `Payment Window Expired` or is cancelled before the first payment, the consumed use returns to the usage limit. When an admin revives a `Payment Window Expired` booking (FR-006), the use is taken again if the limit still has room; if it has no room, the revive is rejected, because the accepted price already includes the promotion and cannot change. An accepted revive returns the Application from Voided to its Active status and clears `use_returned_at`.
- Usage limits count active reservations plus consumed uses, so a limit can never be exceeded. A promotion whose limit is fully reserved or consumed does not attach at send and fails code validation. (REQ-019-088)
- The per-patient usage limit counts the reserved plus consumed uses by the same patient on the same program, the same basis as the total limit, and is checked at the same points: when a promotion is attached at send (for a known patient), when a patient code is validated, and when the patient confirms acceptance. A promotion whose per-patient limit the patient has reached does not attach and fails code validation. (REQ-019-116)
- Rows that are not accepted (sibling subquotes marked Not Selected, competing quotes, expired or withdrawn quotes) never create an Application; any use reserved for them at send by an auto-applied promotion is released.
- Post-acceptance freeze: after acceptance, the promotion and discounted price of the accepted subquote are frozen in the AcceptanceEvent snapshot. No removal, replacement, code entry at checkout or booking, price-changing revalidation, or admin void is allowed. The only exception is the provider-fault transfer in FR-006 (Alternative Flow B5): the replacement quote carries no promotion, the original Application is kept as history and marked Superseded (Superseded takes precedence over Voided when the original booking is cancelled for the transfer), and the use it held returns to the usage limit. Money handling for that transfer is defined by FR-006, FR-007, FR-007b, and FR-017. (REQ-019-089)
- Commission is calculated on the accepted price after the promotion, in the quote currency, read from the acceptance snapshot (FR-015, FR-029). This applies to every discount type, including Hairline-funded programs; no program keeps commission on the price before the promotion.
- Funding of a Both Fees program: this FR owns the definition. Hairline reimburses the program's Hairline share % (0 to 100, fixed at send and frozen at acceptance) of the discount to the provider at payout, on top of the commission effect. FR-017 applies this reimbursement in payout settlement and does not define its own split; payout mechanics belong to the payment work. (REQ-019-017)
- Funding split of each Application: for every program type, the Hairline portion and the provider portion of the discount value follow the commission effect (commission on the accepted price after the promotion, so the provider bears most of the discount). A Both Fees program adds Hairline's reimbursement of the Hairline share % on top of that effect. (REQ-019-110)
- All discount creations, approvals, applications, and removals are auditable. (REQ-019-090)
- 95% of valid codes validate within 1 second on subquote review before acceptance.
- 0% of accepted subquotes carry more than one discount (enforced at all steps).
- 95% of provider approval responses are processed and reflected within 5 seconds of submission.
- Discount usage and impact reports export in ≤ 10 seconds for 95th percentile.
- 100% of applied discounts have audit entries (who, when, what, amount, context).
- Misapplied discounts detected and corrected to ≤ 0.1% of bookings monthly.
- 99.9% monthly uptime for validation and calculation services.
- Zero data loss for discount definitions and usage records.
- Providers respond to approval requests within the auto-decline window (Setting: promotion approval auto-decline window, default 3 business days).
- Patients enter codes only while reviewing a subquote before acceptance.
- The subquote review and acceptance flow (FR-005 Screen 2) exposes the only patient code input surface.
- Calculation service supports deterministic rounding and currency rules.
- Finance defines regional caps and policy; legal approves terms for promotions.
- Calculation pipeline: base price → discount (single) → taxes/fees; idempotent validation. (REQ-019-095)
- Create the Application and reserve usage atomically with the subquote acceptance. Payment and booking read the discounted price from the acceptance snapshot and never revalidate or recompute it. (REQ-019-096)
- Audit trail for all state changes; soft‑disable discounts without data loss. (REQ-019-115)
- Cache active discounts and targeting; invalidate on updates.
- Paginated usage reports; background generation for long ranges.
- RBAC on creation/approval/application; input validation on codes and values.
- Encryption in transit/at rest; audit logs tamper‑resistant.
- `scope` (`REUSABLE` | `AD_HOC_QUOTE_BOUND` — applies to `PROVIDER_SELF` only; other program types are always `REUSABLE`)
- Released and consumed records are terminal: after consumption, the return of the use to the limit on `Payment Window Expired` or cancellation before the first payment, and taking it again on an admin revive (only if the limit has room, otherwise the revive is rejected), are recorded on the linked Application (`use_returned_at`). A Voided Application is terminal except through an admin revive, which returns it to its Active status and clears `use_returned_at`.

### Data & Privacy Rules

- Display only non‑sensitive discount info to patients; provider/Hairline cost splits remain internal. (REQ-019-091)
- Financial records and discount artifacts: retention follows the system PRD, Platform-Wide Rules: One 10-year retention period; takedowns handled by archival, not deletion.
- Access governed by RBAC; only authorized roles can create/approve/apply discounts beyond self‑service code entry.

### Admin Editability Rules

Editable by Admin:

- Discount categories, code format policy, the maximum discount value (one Setting; applies to percentage discounts only and starts at 50 percent; fixed amounts have no cap), and campaign dates. (REQ-019-093)
- Targeting rules (all providers vs. subsets) and approval routing. (REQ-019-093)
- Notification templates for approvals and status: managed in FR-030 (setting: promotion notification templates). (REQ-019-093)
- Minimum number of quotes on each side before Conversion Lift is shown (launch default: 20 quotes on each side). (REQ-019-093)

Fixed in Codebase (Not Editable):

- Single‑discount rule and priority order (apply to the whole platform). (REQ-019-095)
- Promotion terms fixed at send and frozen at acceptance. (REQ-019-095)
- Calculation order of operations (base → discounts → taxes/fees). (REQ-019-095)

Configurable with Restrictions:

- Maximum discount value per policy and region (the same single Setting as above). (REQ-019-094)
- Auto‑decline window for unresponded provider approvals; default 3 business days. (REQ-019-094)

**Carried from dropped sections (original wording)**:

- **PromotionProgram**: id, program_type (`ADMIN_VIA_PROVIDER` | `PROVIDER_SELF` | `HAIRLINE_FUNDED_DIRECT_ISSUED`), scope (`REUSABLE` | `AD_HOC_QUOTE_BOUND` — applies to `PROVIDER_SELF` only; other program types are always `REUSABLE`), bound_quote_id (nullable parent containment), bound_quote_option_date_price_id (nullable application target; both bindings set only for `AD_HOC_QUOTE_BOUND`), owner (admin user id or provider id), name, description, discount_type, value, applies_to (whole price), application_mode (auto / code-only / list-selection / either), funding_model (derived), hairline_share_percent (0 to 100; Both Fees programs only), active window, total usage limit, per-user usage limit, targeting, issuance_channel (for Hairline-Funded), lifecycle_state, audit timestamps. Stored in the `promotion_programs` table; references to PromotionProgram point to that table. The legacy `discounts` table does not hold promotion programs.

---

## Dependencies

- FR-004: Quote Submission & Management – Screen 9 Mode 1/Mode 2 entry points live within FR-004 Screen 1; `QuoteOptionDatePrice.promotionId`, parent/row binding provenance, the copy of promotion terms into the sent quote version, and removal of legacy `promotionNote` are co-owned contracts.
- FR-005: Quote Comparison & Acceptance – patient code entry on one named subquote before acceptance (Alternative Flow A8); the AcceptanceEvent snapshot freezes the discounted price and is the source each Application links to.
- FR-006: Booking & Scheduling – `Payment Window Expired` and cancellation release the reserved use; the audited admin revive re-reserves it; the provider-fault transfer (Alternative Flow B5) is the only post-acceptance exception.
- FR-015 / FR-029: Provider Management and Payment System Configuration – commission base is the accepted price after the promotion (FR-029 REQ-029-054 states the same Rule).
- FR-030: Notification Rules & Configuration – owns the notification catalogue events for platform discounts awaiting provider approval and for promotion status changes, and the promotion notification templates.
- FR-020: Notifications & Alerts – defines the notification service used for provider approval notices.
- FR-018: Affiliate Management – FR-018 generates affiliate-bound codes and assigns one affiliate per code; affiliate-bound code redemptions accrue incentive to the linked affiliate; FR-019 triggers the incentive event consumed by FR-018. (REQ-019-068)
- FR-022: Search & Filtering – Screen 1 search/filter controls are co-owned with FR-022; any field change must be updated in both FRs.
- FR-031: Admin Access Control & Permissions – all admin create/approve/override actions are RBAC-gated per FR-031 role definitions.
- FR-010: Treatment & Recovery Case Management – Screen 10 Applications tab links redemptions to FR-010 treatment case entities; treatment changes never change the accepted promotion. (REQ-019-097)


---

## User Scenarios & Testing

### User Story 1 – Admin launches both‑fees discount (P1)

Why: Increase conversion for a campaign spanning multiple providers.

Independent Test: Create both‑fees discount, providers approve, discount appears in eligible quotes.

Acceptance Scenarios:

1. Given a new both‑fees discount, when published, then targeted providers receive approval requests.
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
3. Given a subquote carrying a promotion, when the patient accepts it, then one Application is created in state Applied, linked to the AcceptanceEvent, the parent quote and version, and the accepted option/date-price row; for a provider-selected promotion or patient code one use is reserved, and for an auto-applied promotion the use reserved at send is consumed instead.
4. Given a promotion that was not attached to a row at send and was not entered by the patient on that subquote, when any request tries to apply it to that row, then the request is rejected with a clear reason and no price changes.
5. Given an Applied redemption, when the first payment succeeds, then the state becomes Completed and the reserved use is consumed; for an auto-applied promotion the use was already consumed at acceptance and only the state changes.
6. Given an Applied redemption, when the booking reaches `Payment Window Expired` or is cancelled, then the status becomes Voided and the use is released (or, for an auto-applied promotion, returned to the limit).
7. Given a `Payment Window Expired` booking whose promotion has a usage limit, when an admin revives it, then one use is re-reserved and the Application returns from Voided to Active; if the limit is exhausted, the revive is rejected.
8. Given sibling subquotes marked Not Selected and competing quotes cancelled by the acceptance, then none of them creates an Application, and any use reserved for them at send by an auto-applied promotion is released.
9. Given an auto-applied program with one use left and two quotes eligible for it, when the first quote is sent, then one use is reserved; when the second quote is sent, then the promotion does not attach because the limit is fully reserved, and the limit is never exceeded.
10. Given a sent quote carrying an auto-applied promotion with a reserved use, when a subquote carrying the promotion is accepted, then the reservation is consumed; when a subquote of that quote that does not carry the promotion is accepted, then the reservation is released with reason `not_applied`; when instead the quote expires, is withdrawn, is archived, ends Not Selected, loses the promotion in a re-sent version, or is cancelled before acceptance because the inquiry was cancelled or the provider's status changed, then the reservation is released with the matching reason.
11. Given a sent quote holding one reserved use for an auto-applied promotion, when the provider re-sends a new version that still carries the promotion, then the existing reservation is kept and no second use is reserved; when the new version no longer carries the promotion, then the reservation is released; and given a sent quote with no reservation, when a new version newly carries the promotion, then one use is reserved.
12. Given an accepted subquote whose auto-applied promotion use was consumed at acceptance, when the booking reaches `Payment Window Expired` or is cancelled before the first payment, then the use returns to the limit; when an admin later revives the booking, then the use is taken again and the Application returns from Voided to Active if the limit has room, and otherwise the revive is rejected and the accepted price stays unchanged.
13. Given a Hairline-funded automatic program and a provider's automatic program both eligible for a quote, when the quote is sent, then only the provider's program attaches, to every row it is eligible for, one use is reserved for it, and the Hairline-funded program attaches to no row of that quote and reserves no use.

### Edge Cases

- Ineligible/expired/limit‑reached codes: validation fails with reason.
- Simultaneous attempts to apply codes on one subquote before acceptance: last confirmed selection wins; audit both attempts. Attempts after acceptance are rejected. (REQ-019-098)
- Program paused, edited, or expired after a quote is sent: the sent rows keep the terms copied at send.
- Patient code no longer valid when the patient confirms acceptance (for example, its usage limit was reached): the acceptance does not happen, the reason is shown, and the patient returns to the subquote detail, where the patient may accept without the code or enter another; the price falls back to what the row carried at send, including its attached promotion (FR-005 REQ-005-026). (REQ-019-099)
- Provider fails to respond to approval: auto‑decline after policy window; visible in audit.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-019-001**: System MUST allow admins to create platform discounts with type, value, dates, usage limits, and targeting.
- **REQ-019-002**: System MUST allow providers to create provider‑specific discounts with similar controls.
- **REQ-019-003**: System MUST attach provider-selected and eligible automatic promotions to option/date-price rows when a quote is sent, validate patient codes on one named subquote before acceptance, and apply at most one discount per subquote.
- **REQ-019-004**: System MUST enforce priority and non‑stacking rules across the whole platform (patient-entered code > provider discount > Hairline-funded discount > affiliate discount when conflicts arise) and MUST attach at most one automatic promotion per quote.
- **REQ-019-005**: System MUST track usage and financial impact with exports and dashboards.
- **REQ-019-012**: System MUST copy each row's promotion terms into the sent quote version at send; later program changes MUST NOT change a sent row.
- **REQ-019-013**: System MUST freeze the promotion and discounted price of an accepted subquote in the AcceptanceEvent snapshot and MUST reject any later removal, replacement, code entry, price-changing revalidation, or admin void, except through the FR-006 provider-fault transfer, which creates a new linked record.
- **REQ-019-014**: For provider-selected promotions and patient-entered codes, System MUST reserve one promotion use at acceptance, consume it at the first successful payment, release it on `Payment Window Expired` or cancellation, and re-reserve it on an admin revive, rejecting the revive if the usage limit is exhausted; an accepted revive returns the Application from Voided to its Active status and clears `use_returned_at`. On release or void, System MUST drop the code's In-Progress count and return a single-use code to Unused; a refund after the first payment MUST NOT return the use, which returns only on a release before the first payment or when a provider-fault transfer replaces the booking (Superseded).
- **REQ-019-015**: For an auto-applied promotion, System MUST reserve one use when a quote carrying it is sent, MUST hold at most one reserved use per sent quote across re-sent versions (keeping the existing reservation, creating one only when a new version newly carries the promotion, and releasing it when a new version no longer carries the promotion), MUST release the reservation when the quote expires, is withdrawn, is archived (`archived`), ends Not Selected, drops the promotion in a re-sent version, or is cancelled before acceptance because the inquiry was cancelled or the provider's status changed, or when a subquote of that quote is accepted that does not carry the promotion (`not_applied`), and MUST consume it when the accepted subquote carries the promotion. If the booking reaches `Payment Window Expired` or is cancelled before the first payment, System MUST return the consumed use to the limit; on an admin revive, System MUST take the use again if the limit has room and otherwise MUST reject the revive, so the accepted price never changes; an accepted revive returns the Application from Voided to its Active status and clears `use_returned_at`. Restoring an archived quote MUST re-check the promotion and take a new reservation, and the restore MUST be refused when the limit is used up or the promotion has ended (FR-004 REQ-004-105). Usage limits MUST count active reservations plus consumed uses so that a limit can never be exceeded.
- **REQ-019-016**: System MUST calculate commission on the accepted price after the promotion, in the quote currency and read from the acceptance snapshot, for every discount type, including Hairline-funded programs; no program keeps commission on the price before the promotion. FR-029 carries the matching Rule REQ-029-054.
- **REQ-019-017**: System MUST record a Hairline share % from 0 to 100 on every Both Fees program, copy it into the terms fixed at send, and provide it to FR-017, which reimburses that share of the discount to the provider at payout on top of the commission effect.
- **REQ-019-018**: System MUST convert a fixed-amount discount into the quote currency at the FR-029 conversion rate in effect at send (for a patient-entered code, in effect when the code is validated) and keep the converted amount in the terms fixed at send.
- **REQ-019-019**: System MUST NOT attach an automatic promotion to an admin-authored replacement quote (FR-004 Workflow 7) or reserve a use for it; the admin sets the replacement price directly, the replacement carries no promotion, the original Application MUST be marked Superseded, and the use it held MUST return to the usage limit.
- **REQ-019-109**: System MUST NOT let an admin force a provider to take part in a program; the overrides an admin has on a provider's adoption are Force-Revoke and Re-invite (moved in from FR-017).
- **REQ-019-110**: System MUST record the Hairline portion and the provider portion of every Application's discount value according to the commission effect for every program type, and for a Both Fees program MUST add Hairline's reimbursement of the Hairline share % on top.

### Data Requirements

- **REQ-019-006**: System MUST persist discount definitions, approvals, and usage records with audit details.
- **REQ-019-007**: System MUST link each Application to the parent quote and version, the accepted option/date-price row (subquote), the AcceptanceEvent, the booking, and participant entities.

### Security & Privacy Requirements

- **REQ-019-008**: System MUST restrict creation/approval/apply actions to authorized roles; patient sees only necessary pricing info.
- **REQ-019-009**: System MUST encrypt sensitive data and preserve tamper‑evident audit logs.

### Integration Requirements

- **REQ-019-010**: System MUST notify targeted providers when a platform discount awaits their approval (on publish and on Re-invite), using the approval-requested event of the FR-030 notification catalogue and the notification service defined in FR-020. System MUST also notify the adopting providers when the terms of an adopted program change and when an admin Force-Revokes, pauses or resumes an adopted program, and MUST notify admins when a provider revokes its own adoption; each notice is its own event in that catalogue.
- **REQ-019-011**: System MUST integrate with calculation/settlement services for consistent totals.

---

## Appendix: Change Log

| Date       | Version | Changes                                      | Author |
|------------|---------|----------------------------------------------|--------|
| 2026-11-22 | 2.8 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v2.7) and the change requests (CR-FR019-20261016-01 in `change-request-2026-10-16-mtg002-quote-model-alignment.md`, and `change-request-2026-09-10-option-date-promotion-alignment.md`) are in `archived/prd-baseline-2026-11-08/fr019-promotions-discounts/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 2.9 | Independent compression review: 1 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | Product Owner / Documentation |
| 2026-11-24 | 3.0 | Logic review fixes: archived release reason and restore re-check; send-time and acceptance-time handling of a provider-selected promotion that cannot be used; patient code replaces the row's promotion and the fallback price; a failed code at confirm follows FR-005; tie-break and limit-before-ranking for automatic programs; provider-fault transfer replacement carries no promotion and the original use returns; no program-level Pending Approval, activation, pause and resume ownership; admin overrides limited to Force-Revoke and Re-invite, with Re-invite from revoked states; auto-decline window default of 3 business days; provider code entry removed (select from the list); package-upgrade type and treatment or travel scope removed; affiliate codes follow the same usage rule and Applied means reserved at acceptance; admin edit of a sent quote counts as a re-send; code status on release or void; pre-acceptance code storage and funnel source; audit panel old and new values. | Product Owner / Documentation |
| 2026-11-24 | 3.1 | Logic review fixes, second pass: a use also returns on a provider-fault transfer; an admin revive returns the Application from Voided to Active; per-patient usage limit basis and check points; a fixed amount at or above the row price is not attached; fixed-amount conversion for a patient code; auto-applied eligibility named by Screen 2 fields; Hairline-Funded programs limited to Auto-applied or Code-only; notice to adopting providers when Value or Hairline Share % changes; provider and admin notices listed. | Product Owner / Documentation |
| 2026-11-25 | 3.2 | Cross-FR alignment: the affiliate capture is stated as stored with the inquiry journey, read at acceptance and honoured only for an Active affiliate; code registration from FR-018 is rejected with a named reason for a duplicate code text or a non-affiliate program. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role           | Name | Date       | Signature/Approval |
|----------------|------|------------|--------------------|
| Product Owner  | TBD  | 2026-05-12 | Approved           |
| Technical Lead | TBD  | 2026-05-14 | Approved           |
| Stakeholder    | TBD  | 2026-05-14 | Approved           |
| Product Owner  | Joachim Trung Tuan | 2026-10-18 | Approved FR-019 v2.2 to v2.5 via MTG-002 decision log (documentation only) |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Last Updated**: 2026-11-25
