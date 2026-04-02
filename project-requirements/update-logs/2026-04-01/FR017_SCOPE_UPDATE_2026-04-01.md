# FR-017 Scope Update — 2026-04-01

**Document**: `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`
**Status Before**: Draft
**Change Type**: Scope clarification — MVP backlog deferral + provider flow distinction

---

## Changes Made

### 1. Patient Platform (P-03) — Invoice History Deferred to Backlog

**Rationale**: The patient-facing invoice history and in-app receipt viewing feature was not included in the missing flow review for the mobile app. The client transcription (HairlineApp-Part1.txt) confirms the patient payment flow covers making payments via Stripe but does not include in-app invoice browsing. This feature is excessive for MVP.

**What changed**:
- Removed `Patients view invoice history and payment receipts` as an active MVP scope item under Patient Platform (P-03)
- Marked it as **BACKLOG (Future Phase)** with rationale: patients receive invoices via email (PDF) at payment confirmation; in-app access deferred
- Added matching **BACKLOG** entry to the Communication Structure > Out of Scope section

**What stays in scope**:
- Patient payment initiation (deposit, installments, final payment via Stripe) — covered by FR-007
- Discount code entry at checkout
- Admin-side patient billing management (Screen 3: Patient Billing - Invoice Management) — remains fully in scope

---

### 2. Provider Platform (PR-05) — Earnings vs. Payout Flow Distinction

**Rationale**: The previous description blended two conceptually separate stages. Separating them makes implementation and testing boundaries clearer.

**What changed** in the Provider Platform multi-tenant breakdown:

Restructured into two stages:

- **Stage 1 — Treatment Earnings Tracking (per case)**: Provider sees booking-level income visibility as treatments complete, including commission breakdown and running total of pending earnings
- **Stage 2 — Payout Consolidation & Processing (admin-initiated)**: Admin groups eligible earnings into scheduled payouts (weekly/bi-weekly/monthly); provider views payout schedule, history, and downloads invoices after payout is processed

**Note**: This is a documentation clarification only — no change to the underlying payment model or business rules. Both stages were already implied; this makes the separation explicit.

---

---

### 3. Discount Management — Removed Duplicate Screen 4 and Conflicting Rules

**Conflict identified**: FR-017 Screen 4 "Discount Management - Create Discount Code" fully duplicated FR-019 / A-06: Discount & Promotion Management Screen 1. FR-017 also had two business rules (Rule 7: expiration required; Rule 8: both-fees provider approval) that are owned by FR-019, and a direct contradiction on the provider approval model:
- FR-017 (removed): discount Active only when **all** providers accept (unanimous)
- FR-019 (canonical): each provider becomes eligible **independently** on acceptance (per-provider)

**What changed**:
- Screen 4 replaced with a read-only "Discount Usage Overview" screen — A-05's legitimate role is consuming discount data for reconciliation, not managing it
- Added cross-reference note on Screen 4 directing to FR-019 for creation/management
- Rules 7 and 8 marked as "Moved to FR-019"
- Admin Editability items for discount creation/lifecycle marked as "Moved to FR-019"
- Executive Summary Key Capabilities updated to clarify tracking vs. creation

---

### 4. Stripe Account Management — Removed Duplicate Scope Item

**Conflict identified**: FR-017 line 71 listed "Stripe Account Management — configure multiple Stripe accounts per region/currency, manage currency conversion rates" as an A-05 Admin Platform capability. This is fully owned by FR-029 / A-09: Payment System Configuration (Verified & Approved).

**What changed**:
- Removed "Stripe Account Management" from Admin Platform scope, replaced with "Not in scope" note referencing FR-029/A-09
- Executive Summary reconciliation reference updated to clarify FR-017 consumes but does not configure Stripe accounts
- Admin Editability item for "Currency conversion markup percentage" marked as "Moved to FR-029"

---

---

### 5. Communication Structure — Rewritten with Explicit Event Table

**Change**: Replaced a generic bullet list of email notifications with a structured event table that FR-017 owns as the authoritative source. FR-020/S-03 handles delivery; FR-017 defines which billing events require notifications.

Added clarity on notification channels:
- Both admin and provider have in-app notification dropdowns (push) — not just email
- Channels: Email + Push for all billing events in MVP; SMS deferred
- Added "Outstanding invoice alert" as an admin-specific notification (was implied but not listed)
- Removed "In-app chat for payment disputes" reference updated to correct FR-034 (was A-10 only)

---

### 6. Manual Payment Status Override — New Requirement

**Rationale**: Stripe API may fail, be delayed, or require manual correction in edge cases. Admins need the ability to override payment status without waiting for an automated webhook.

**What was added** to Screen 3 (Patient Billing - Invoice Management):
- New "Override Status" action button available for all invoice statuses
- Business rule: requires mandatory reason text (max 500 chars), confirms new status, logs to audit trail
- Overridden invoices display admin-only badge: "Status manually adjusted — [date]"
- Override does NOT automatically trigger Stripe refund or charge — admin is responsible for off-system actions
- New SC-012b success criterion: admin can process override within 2 minutes with immediate audit confirmation

---

### 7. Remaining Overlap Fixes (Cross-FR Audit)

Addressed all remaining conflicts identified in systematic cross-FR audit:

| Item | Action |
|---|---|
| Admin Editability — commission rate (15-25%) | Marked [Not in scope — see FR-029] |
| Admin Editability — payment reminder schedule | Marked [Not in scope — see FR-030] |
| SC-012 discount approval SLA | Marked [Not in scope — see FR-019] |
| SC-020 discount conversion metric | Marked [Not in scope — see FR-019] |
| Screen 6 affiliate scope | Added ownership boundary note: FR-018 owns affiliate scheme/tracking; FR-017 owns payout execution |
| Executive Summary affiliate capability | Updated to "Process affiliate commission payouts (calculation owned by FR-018/A-07)" |
| Integration 1 Stripe Payment Intents | Marked [Not in scope — see FR-007] |
| Integration 3 Stripe Webhooks (payment events) | Marked [Not in scope — see FR-007]; retained payout-specific transfer webhooks |
| Business Process Assumption 2 (discount approval timing) | Marked [Not in scope — see FR-019] |
| All strike-through formatting | Replaced with **[Not in scope — see FR-X]** / **[BACKLOG — Future Phase]** markers |

---

---

### 8. Two-Stage Payout Billing Cycle — New Requirement

**Rationale**: Previously FR-017 had no buffer period and generated the invoice only after Stripe confirmed the transfer. The correct flow requires a payout statement to be generated before payment so admin has a review window before money moves.

**The two stages now defined:**

| Stage | Timing | Who sees it |
|---|---|---|
| Payout Statement (dashboard view) | Auto-generated at start of buffer window (default: 3 days before payout day) | Admin only — provider cannot see draft statements |
| Invoice PDF | Generated after Stripe `transfer.paid` webhook confirms | Provider receives via email + push |

**Changes applied:**

- **Automated Triggers**: Added statement generation cron job (buffer window start) and overdue status trigger (end of payout day)
- **Main Flow**: Restructured into three explicit stages — Stage 1 (statement generation), Stage 2 (admin review window), Stage 3 (payout day approval + Stripe transfer + invoice)
- **Alternative Flow A4**: New "Overdue Payout" flow — if admin misses payout day, status → "Overdue", push + email notification triggered, overdue section appears in billing list
- **Screen 1**: Added "Overdue" status to Status field; list divided into Overdue (top) and Upcoming sections; "Approve Payout" button now enabled for both "Pending Approval" and "Overdue" statuses; updated business rules to reflect statement-first model
- **Billing Rules 2–5**: Rewrote Billing Rule 2 to distinguish statement (pre-payout, dashboard view) from invoice (post-payout, PDF). Added Rules 3–5 for buffer window, affiliate alignment, and overdue handling.
- **Communication Structure**: Added `payout.overdue` notification event (Admin, Email + Push)
- **Admin Editability**: Buffer window configuration referenced as [Not in scope — see FR-029]

**Provider visibility decision**: Provider sees nothing until admin approves and Stripe transfer is initiated. Per-treatment earnings are always visible (Stage 1 earnings tracking); payout history updates only after confirmation.

---

---

### 9. Per-Provider Payout Frequency — Confirmed and Documented (FR-015 + FR-017)

**Rationale**: The FR-015 design screen contains a "Commission & Financials" tab (currently labelled "Affiliate Pay Details" — legacy mislabeling) with three radio options for payout frequency, applied per provider. This confirms that per-provider scheduling is the intended design. A universal platform-wide frequency was considered but rejected once the FR-015 screen was reviewed.

**What changed in FR-015** (Tab 7 — Commission & Financials):
- Added note clarifying that the "Affiliate Pay Details" screen label is a legacy mislabeling
- **Payout Frequency** field corrected: type changed to `radio`, option names and period definitions made explicit:
  - **Weekly**: Monday to Sunday
  - **2x a Month**: 1st–15th then 16th–last day of month
  - **Monthly**: Full calendar month
- Added **Commission Start Date** field: date from which commission and payout cycle tracking begins; includes "number of days from end of last cycle" offset
- Added **Featured Provider** toggle field (confirmed present on this screen)
- Updated Current Configuration display format to show period definition (e.g., "Paid Weekly (Mon–Sun)")

**What changed in FR-017**:
- **Alternative Flow A3** restored to "Provider Payment Schedule Change" (per-provider): admin changes frequency in FR-015 / A-02; FR-017 cron reads the updated value on next run
- **Screen 1** (Provider Billing list): Restored per-provider "Payment Schedule" column; "Next Payout Date" now reflects individual provider schedule; "global frequency" rule removed; statement generation rule updated to per-provider
- **Screen 1 Notes**: Added "payment schedule" to filter options
- **Screen 2** (Payout Detail Modal): "Bi-Weekly" corrected to "2x a Month" with explicit period definitions aligned to FR-015
- **Automated Triggers**: Updated from "all providers simultaneously at platform-wide payout date" to "daily cron checks each provider's individual schedule"
- **Admin Editability**: "Global provider payout frequency" replaced with `[Not in scope — see FR-015/A-02]` note; FR-017 reads this setting, does not own it

**Ownership boundary**: FR-015 / A-02 owns payout frequency configuration per provider. FR-017 / A-05 reads it to determine statement generation timing and payout date per provider.

---

---

### 10. Provider Platform Screens Added (Screen 7 & Screen 8) + Affiliate Detail Sub-Table

**Rationale**: Screen Specifications section only covered admin-facing screens. The Provider Platform has two distinct billing views per the two-stage payout model, and the affiliate billing screen lacked a formal spec for the treatment case breakdown.

**What changed**:

- **Tenant scope note** added at the top of Screen Specifications section: clarifies which tenants have screens in this FR (Admin: Screens 1–6; Provider: Screens 7–8; Patient: none; Affiliate: none in FR-017)
- **Screen 6 — Affiliate Billing**: Added formal "Referral Booking Sub-Table" specification showing per-treatment case breakdown (Booking ID, Patient Name, Treatment Date, Treatment Type, Booking Amount, Commission Rate, Commission Earned, Currency, Referral Code)
- **Screen 7 — Provider Earnings Tracker (Stage 1)**: New provider-facing screen. Shows per-treatment income records with Booking ID links to treatment cases, commission breakdown, net earning, and payout status (Pending / Included in Payout). Summary bar shows total pending earnings and next payout date.
- **Screen 8 — Provider Payout History (Stage 2)**: New provider-facing screen. Shows confirmed payouts with Treatment Breakdown Sub-Table linking each payout to the Booking IDs it covers. Invoice PDF download available post-Stripe confirmation.
- **Business Rule 1a**: Added treatment case traceability rule — every payment record (invoice, payout, affiliate commission) must maintain a Booking ID link to the treatment case(s) that generated it (1:1 for patient invoices; 1:N for provider payouts and affiliate commissions).

---

### 11. Currency Conversion Constraint Documented

**Rationale**: USD is the base currency; only two pairs (USD/GBP, USD/TRY) are supported at MVP. This was not reflected in the FR.

**What changed**:
- **Rule 3**: Updated to state USD is the base currency, all conversions route through USD, and only USD/GBP and USD/TRY pairs are supported at MVP. Pair configuration ownership noted as FR-029 / A-09.
- **Fixed in Codebase**: Updated currency exchange API note to specify USD as base and two supported pairs.

---

### 12. Business Workflows — Converted to Mermaid with Conditional Logic

**Rationale**: All business workflow steps were in prose format (numbered lists) which adds no structural value over plain text. Mermaid diagrams are only meaningful when they show decisions, branching, and error paths.

**What changed**:
- All 8 workflow flows replaced with Mermaid `flowchart TD` diagrams
- Main Flow restructured: A1 (Add Note), A4 (Overdue Payout), and B1 (Payout Failure) merged INTO the main diagram as decision branches — these are all part of the same payout lifecycle, not separate alternative flows
- Main flow now contains 5 decision nodes: note optional?, admin confirms?, any statements overdue?, Stripe webhook result?, failure cause?
- Alternative Flows reduced from 7 to 4 (A2, A3, B2, B3) — the other three absorbed into Main Flow
- A2 (Bulk Approval): added decisions for selection adjustment and any-failures-after-batch
- A3 (Schedule Change): added confirmation decision with cancel path back to start
- B2 (Dispute Resolution): added decisions for booking-found-in-system? and already-paid?; two resolution paths
- B3 (Currency Alert): added monitoring loop (threshold check), three-way admin action decision (accept/contact/adjust)

---

### 13. Booking Reference — Field Name Aligned with FR-006 and FR-007

**Rationale**: FR-017 used "Booking ID" as the UI field label in all screens. FR-006 (Booking & Scheduling) and FR-007 (Payment Processing) consistently use "Booking Reference" as the canonical display label. The internal schema attribute `booking_id` remains unchanged.

**What changed** (UI field labels only; schema attributes unchanged):
- Screen 2 sub-table: `Booking ID` → `Booking Reference`
- Screen 3: `Booking ID` → `Booking Reference`
- Screen 6 Referral Booking Sub-Table: `Booking ID` → `Booking Reference`
- Screen 7 Provider Earnings Tracker: `Booking ID` → `Booking Reference`
- Screen 8 Treatment Breakdown Sub-Table: `Booking ID` → `Booking Reference`
- Screen 2 Notes: "Clicking on 'Booking ID'" → "Clicking on 'Booking Reference'"
- Screen 7 Business Rules: "via Booking ID" → "via Booking Reference"
- Screen 8 Business Rules: "(Booking ID → FR-001)" → "(Booking Reference → FR-001)"
- General Module Rule 2: "via Booking ID" → "via Booking Reference"

---

## Client Requirements Alignment

- Admin-side patient billing: **explicitly confirmed** in Hairline-AdminPlatform-Part1.txt (line 230–243) — invoice numbers, amounts, status, reminders, download invoice
- Patient-facing invoice history: **not mentioned** in mobile app transcription; only payment initiation screen described
- Provider earnings per booking + payout schedule: consistent with admin transcription describing provider billing section

