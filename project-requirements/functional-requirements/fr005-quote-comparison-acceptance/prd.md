# FR-005 - Quote Comparison & Acceptance

**Module**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight  
**Feature Branch**: `fr005-quote-comparison-acceptance`  
**Created**: 2025-11-03  
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-005 from system-prd.md; SRC-MTG-002 and CR-FR005-20260915-01
**Change Request**: [CR-FR005-20261016-01 — MTG-002 quote model alignment](change-request-2026-10-16-mtg002-quote-model-alignment.md)

---

## Executive Summary

The Quote Comparison & Acceptance module enables patients to review quotes from multiple providers, including multiple parent quotes from the same provider. Each parent quote may contain multiple subquotes. The subquote is the atomic patient comparison and acceptance unit: it contains one package selection, one applicable date range, its appointment details, and its price, while inheriting the provider and shared clinical information from its parent quote. A patient accepts exactly one subquote per inquiry to proceed to Booking & Payment. The module preserves privacy, expiry enforcement, full auditability, and deterministic handling of every non-selected parent quote and sibling subquote.

**Canonical FR-005 hierarchy**: Provider → Parent Quote → Subquote. For interoperability with FR-004, one FR-005 Subquote resolves one `Quote Option` package snapshot together with exactly one applicable `Option/date-price` record. Those implementation records form one patient-visible and patient-acceptable entity in this module; neither is accepted independently. Because FR-004 versions the complete parent-and-options aggregate atomically, `subquoteVersion` is the owning parent quote's `QuoteVersion`, not a separate revision counter.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02)**: Quote Request & Management  
- **Provider Platform (PR-02)**: Inquiry & Quote Management  
- **Admin Platform (A-01)**: Patient Management & Oversight  
- **Shared Services (S-03, S-06)**: Notification service, audit logging, retention/archival utilities

### Multi-Tenant Breakdown

**Patient Platform (P-02)**:

- View all parent quotes and their subquotes within the Inquiry Dashboard (FR-003 Screen 8).
- Inspect inherited parent information and complete subquote details via FR-004's patient quote detail screen (Screen 4) with added acceptance functionality.
- Compare subquotes and accept exactly one subquote per inquiry; see the parent quote expiry countdown.
- Receive notifications for quote updates, expiries, and acceptance confirmation.  
- After acceptance, proceed to booking/payment flow entry point (next FR).

**Provider Platform (PR-02)**:

- Read-only visibility of the accepted or non-selected outcome for parent quotes and subquotes.
- Competing parent quotes auto-cancelled with reason “Other subquote accepted”; sibling subquotes in the accepted parent quote become “Not Selected”.
- No patient PII is revealed by acceptance; full details remain locked until payment confirmation per constitution.

**Admin Platform (A-01)**:

- Global oversight of quote states and acceptance events across patients/providers.  
- Audited "Add note or correction" annotations on acceptance records. Acceptance events, accepted subquotes, and their parent quotes cannot be deleted or restored, and an annotation never alters the AcceptanceEvent, its snapshot, or any quote state.
- Investigation of flagged acceptance races or errors (rare): the first valid acceptance stands, and the admin records findings as an annotation.
- Provider-fault transfer after acceptance is performed through FR-006; it creates a new admin-authored acceptance record linked to the original instead of changing the original.

**Shared Services (S-03, S-06)**:

- Notifications for subquote acceptance, parent quote expiry, sibling outcomes, and auto-cancellation of competing parent quotes.
- Audit logging service for all state transitions.  
- Retention/archival utilities (no hard deletes; acceptance records are never deleted or restored).

### Communication Structure

**In Scope**:

- System → Patient: Quote update/expiry/acceptance notifications.  
- Patient → System: Accept action on one eligible subquote (sibling and competing outcomes follow the rules below).
- Patient → Provider: Ask questions about quotes through the dedicated FR-012 Messages/Inbox conversation with that provider.
- System → Provider: Notify the provider of patient quote questions within 5 minutes.
- System → Provider: Accepted-subquote outcome or auto-cancellation updates for non-selected parent quotes.
- Admin → All: Oversight and policy-bound interventions.

**Out of Scope**:

- Direct patient-provider chat (see FR-012: Messaging & Communication).  
- Payment collection and invoice issuance (handled in Booking & Payment FR).  
- Revealing patient contact/identity to provider prior to payment confirmation.

### Entry Points

- Patient accesses from Inquiry Dashboard (FR-003 Screen 8) where quotes are displayed within the inquiry context, or via push/email notification.  
- Acceptance is available only while the target subquote and its parent quote are eligible.
- Upon subquote acceptance, system locks the accepted selection, resolves sibling/competing outcomes, and triggers booking handoff.

---

## Business Workflows

### Main Flow: Patient Accepts a Subquote

**Actors**: Patient, System, Provider (notified), Admin (observer)
**Trigger**: Patient taps “Accept” on a valid subquote within an unexpired parent quote
**Outcome**: Inquiry transitions to Accepted; one subquote and its inherited parent context are locked as the accepted selection; competing outcomes are resolved; booking handoff is prepared

**Steps**:

1. Patient opens Inquiry Dashboard (FR-003 Screen 8) and views parent quotes grouped by provider and quote response.
2. Patient expands a parent quote and reviews its available subquotes. Each subquote presents its package, date range, appointment details, pricing, and inherited parent information as one complete choice.
3. Patient compares eligible subquotes, including subquotes from different parent quotes or from the same parent quote.
4. Patient opens one subquote and taps "Accept". Before confirming, the patient may enter a promotion code on that named subquote (Alternative Flow A8).
5. Patient confirms the exact subquote with terms acknowledgment and a complete selection summary.
6. System atomically revalidates the inquiry, parent quote, and subquote, and confirms the owning provider is still `Active` (not `Suspended` or `Deactivated` under FR-015); confirms that no prior subquote has been accepted for the inquiry; verifies that the presented parent aggregate `QuoteVersion` is current; and acquires one fixed, exclusive slot hold keyed by provider, appointment date/time, and time zone for the FR-026 slot-hold duration (default 48 hours), starting at acceptance. The derived `subquoteVersion` MUST equal that same version. If another pending or confirmed booking already holds or blocks the same slot, acceptance is rejected before an AcceptanceEvent or booking handoff is created.
7. After the exclusive hold succeeds, System records the selected subquote as Accepted, locks its inherited parent context and commercial details, sets the parent quote and inquiry to Accepted, records the acceptance snapshot (including the exchange rate and its timestamp) and the slot-hold reference, and writes the accepted subquote price as the parent quote's accepted total (FR-004 `acceptedTotal`), read from the snapshot. No appointment record is created at acceptance; FR-006 creates it only on successful first payment.
8. System marks every sibling subquote in the accepted parent quote as Not Selected and auto-cancels every competing parent quote for the inquiry with reason "Other subquote accepted." If the accepted subquote carries an auto-applied promotion, the promotion use reserved when its parent quote was sent is consumed now. If the accepted parent quote holds a reserved automatic-promotion use but the accepted subquote does not carry that promotion, the reservation is released with reason `not_applied`. The use reserved by every parent quote that ends Not Selected or auto-cancelled is released (FR-019).
9. System sends notifications to the patient and all affected providers without disclosing the selected provider or accepted price to non-selected providers. Each provider receives one notice per sent parent quote (selected or not selected); an unsent draft quote cancelled by FR-004 because another quote was accepted produces no notice. No `quote.declined` event is emitted for these outcomes. At acceptance the patient receives one notice only, `booking.scheduled` ("Booking Accepted — Slot Held (Pending Payment)"), which is sent to the patient only and is mandatory, so it cannot be disabled; the provider learns of the acceptance through `quote.accepted`, whose outcome notices go to providers only and are never sent to the patient (FR-020).
10. System sends the accepted subquote and its inherited context to Booking & Payment; no funds are collected in FR-005.
11. System writes immutable audit entries for the selection and every resulting state transition.

### Alternative Flows

**A1: Parent Quote Expires During Subquote Review**:

- Trigger: Countdown reaches zero while patient is viewing details.  
- Steps: System disables Accept button; shows “Expired” badge and guidance to choose another quote.  
- Outcome: Every subquote under that parent quote becomes ineligible. Patient can choose another eligible subquote from another parent quote if one exists. If none remains, the patient may cancel the inquiry and submit a new one, or contact support.

**A2: Simultaneous Acceptance Attempt**:

- Trigger: Patient attempts to accept a second subquote after already accepting another (or after a race condition).
- Steps: System prevents the second acceptance and shows guidance referencing the accepted subquote.
- Outcome: Exactly one accepted subquote per inquiry is enforced.

**A3: Provider Withdraws Parent Quote Before Acceptance Completes**:

- Trigger: Provider withdraws the subquote's parent quote just before patient confirms acceptance.
- Steps: System re-validates the parent quote and subquote at confirmation; if withdrawn, acceptance is blocked with explanation.
- Outcome: Patient returns to inquiry dashboard to select another eligible subquote.
- Withdrawal after acceptance is not handled here. FR-006 owns it as a provider-fault case: the booking closes with cause provider fault, the slot hold is released, the AcceptanceEvent and its snapshot are kept unchanged, and an admin rehomes the patient within the same inquiry by direct transfer to a replacement provider through the admin-authored replacement acceptance (Alternative Flow A9 and Business Rule 1).

**A4: Patient Cancels Inquiry During Quote Review**:

- Trigger: Patient cancels the parent inquiry (FR-003 Workflow 5) while the inquiry is in the Inquiry or Quoted stage, before any subquote is accepted.
- Steps: System cancels inquiry; all parent quotes and their subquotes become ineligible with status "Cancelled (Inquiry Cancelled)"; all Accept/Compare actions are disabled; dashboard shows "Cancelled" badge.
- Outcome: Inquiry dashboard becomes read-only. Patient can create a new inquiry immediately.
- After acceptance the patient cannot cancel the inquiry. The patient sees a "Contact support" action instead, and an admin performs any booking cancellation through FR-006 with a mandatory reason and audit. That cancellation moves the booking to `Cancelled` and the inquiry to `Cancelled`, releases any active slot hold immediately, and leaves the accepted subquote and its parent quote `accepted`; refunds and fees follow the FR-006 payment placeholder.

**A5: Appointment Slot Already Reserved**:

- Trigger: Patient confirms a subquote whose appointment slot is already held or blocked by another pending or confirmed booking, including a concurrent acceptance by another patient that acquires the active hold for the same provider, appointment date/time, and time zone a moment earlier.
- Steps: System rejects acceptance atomically because an active hold for that slot already exists, before creating an AcceptanceEvent, changing quote/inquiry states, or emitting a booking handoff. The confirmation modal shows the error state "This appointment slot was just taken. Please choose another subquote." and the patient returns to the inquiry dashboard to choose another eligible subquote. The subquote is not recorded as Accepted.
- Outcome: The existing slot reservation remains unchanged and no second accepted selection is created for that slot.

**A6: Provider Becomes Suspended or Deactivated**:

- Trigger: The owning provider's `Suspended` or `Deactivated` status becomes effective (FR-015 Alternative Flow A5 and Screen 4) before, during, or after subquote acceptance.
- Steps: From the effective time, Accept is blocked for every subquote of that provider and a confirmation already in flight is rejected before an AcceptanceEvent or hold is created. If the inquiry is still comparing providers, FR-004 cancels that provider's parent quotes once each; their subquotes become unavailable, while subquotes from other providers remain acceptable and the inquiry keeps its stage with `supportRequired = true` (FR-003 Workflow 2 Alternative Flow B4). If the accepted subquote belongs to that provider, the provider-fault transfer in Business Rule 1 applies: the booking closes with cause `ProviderSuspended` or `ProviderDeactivated` (FR-006 Alternative Flow B4, which routes to B5), any active hold is released, booking-confirming payment from the original provider is blocked, and an admin rehomes the patient to a replacement provider within the same inquiry through a new admin-authored acceptance record (Alternative Flow A9); the supersession record that links the original AcceptanceEvent to the replacement, with that cause, is written at the replacement acceptance. The inquiry is not cancelled, and the AcceptanceEvent, accepted IDs/versions, and acceptance snapshot are retained without rewriting.
- Outcome: Before acceptance, when Accept is blocked, the patient sees the inline error "This provider is no longer available. Please contact support." with a Contact Admin/Support action, not the A4 patient-cancellation messaging. After acceptance, when the deposit or booking-confirming payment is blocked because the provider became Suspended or Deactivated, the patient sees the inline error "This clinic can no longer perform your treatment. An admin will arrange a replacement clinic within the same inquiry."; the patient is not asked to start a new inquiry or re-enter anything. Both are on-screen errors shown in the app, not FR-020 notifications, and are localized through FR-021 like other UI text. The FR-020 patient notices for the same events (`provider.status_cancellation_patient` before acceptance, `booking.provider_fault_replacement` after acceptance; FR-015 and FR-003) are separate and unchanged. Late acceptance requests or payment callbacks cannot revive the original selection, and later reactivation does not restore it.

**A7: Payment Window Expires After Acceptance**:

- Trigger: The fixed slot hold that started at acceptance ends before the first payment (deposit or first instalment) succeeds, and FR-006 moves the booking to `Payment Window Expired`.
- Steps: The slot hold is released and no appointment record exists. The accepted subquote is never reopened for acceptance, its sibling subquotes stay Not Selected, competing parent quotes stay cancelled, and the AcceptanceEvent and snapshot stay unchanged. The patient is shown a "Contact support" action with two recovery routes, both performed by an admin in FR-006: an audited admin revive, or an admin booking cancellation (booking and inquiry `Cancelled`, accepted quote stays `accepted`) after which the patient may start a new inquiry. The patient cannot cancel the inquiry directly after acceptance (Alternative Flow A4).
- Outcome: The inquiry keeps its single acceptance. A revive, when an admin grants it, is performed by FR-006 with a fresh slot-availability check and a new hold; FR-005 does not create a second acceptance. Missed later instalments never cause `Payment Window Expired`; they are governed by FR-007 and FR-007b.

**A8: Patient Applies a Promotion Code Before Acceptance**:

- Trigger: Before confirming acceptance, the patient enters a promotion code on Screen 2 for one named subquote.
- Steps: System validates the code for that subquote through FR-019. If valid, the discounted price is shown next to the provider's offered price and carried into the confirmation summary; if invalid, the patient sees the reason and the offered price is unchanged. The code applies only to the named subquote; opening another subquote does not carry it over. The applied code is recorded against the patient's selection only and is never written to the provider's quote or promotion records.
- Outcome: On acceptance, the discounted price and the applied promotion are frozen into the AcceptanceEvent snapshot. After acceptance the promotion and price cannot be removed, replaced, re-entered at checkout, or changed by revalidation (including an admin void); the only exception is the provider-fault transfer in Business Rule 1.

**A9: Admin-Authored Replacement Acceptance (Provider-Fault Transfer)**:

- Trigger: Before treatment starts (booking `Accepted` or `Confirmed`), the accepted provider withdraws, drops out, or has a suspension or deactivation take effect, and FR-006 closes the booking with the provider-fault cause (FR-006 Alternative Flows B4 and B5).
- Steps: The closure is recorded on the booking as its cancellation cause; no supersession record is written at closure. The admin authors a replacement quote for the replacement provider inside the same inquiry (FR-004 Screen 8). Through the FR-006 transfer, the admin then records a new AcceptanceEvent with `actorType = admin` that points to that replacement quote, one of its Quote Options, and one of its option/date-price rows, exactly like a patient acceptance. In the same operation the system writes one AcceptanceSupersession record that links the closed AcceptanceEvent to the new one; the record is inserted once and never updated. The new acceptance acquires the slot hold and creates the replacement booking through FR-006. The patient receives the mandatory `booking.scheduled` notice and the replacement provider receives `quote.accepted`.
- Replacement quote not accepted: If no replacement acceptance is recorded, the replacement quote expires under the normal FR-004 quote expiry and no AcceptanceEvent or AcceptanceSupersession record is written. The inquiry stays flagged `supportRequired` and is not cancelled automatically; the admin may author another replacement quote (FR-004 Screen 8) or cancel the inquiry and booking from the FR-006 admin screen.
- Outcome: The inquiry keeps one active acceptance, the original AcceptanceEvent and snapshot stay unchanged as history, and the patient re-enters nothing.
- Boundary: If the provider fault happens while the booking is `In Progress`, no replacement acceptance is created; the admin either moves the booking to Aftercare with an aftercare reassignment or cancels it in FR-006. If the provider fault happens in Aftercare, after treatment is done, no replacement acceptance is created. The admin reassigns only the aftercare provider or team in FR-006; the booking and treatment record stay, and no new payment is taken.

---

## Screen Specifications

### Patient Platform

#### Screen 1: Inquiry Dashboard with Quote Comparison (Enhanced from FR-003 Screen 8)

**Purpose**: Patient views submitted inquiry status, browses parent quotes, compares complete subquotes, and accepts one subquote

**Note**: This screen extends FR-003's Inquiry Dashboard (Screen 8). Parent quotes remain grouped within the inquiry context, while their complete child subquotes are the comparison and acceptance items.

**Data Fields**:

**Inquiry-Level Fields** (always visible; one instance per screen):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Current Stage | badge | Yes | Inquiry stage (Inquiry/Quoted/Accepted/Cancelled/...) | Valid lifecycle value; includes "Cancelled" per FR-003 |
| Timeline | timeline | Yes | Chronological status changes | Timestamps present |
| Inquiry Summary | group | Yes | Read-only inquiry info | Complete and consistent |
| Medical Alerts | chips | Yes | Patient medical risk level | Read-only; from FR-003 |
| Deadlines | datetime | Yes | Response/expiry deadlines | Future or past allowed |
| Next Actions | actions | Yes | Available user actions | Based on stage/permissions |

**Parent Quote Group Fields** (repeated for each parent quote):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Provider | group | Yes | Provider identity and summary shown under patient privacy rules | Read-only; one provider per parent quote |
| Parent Quote Reference | text | Yes | Stable reference for one provider response | Read-only; must not be presented as the selectable item |
| Treatment and Shared Clinical Information | group | Yes | Treatment, graft information, visual plan, clinicians, notes, requirements, and attachments inherited by every child subquote | Read-only; sourced from the parent quote |
| Provider Reviews | rating/number | No | Review rating and count | Read-only; sourced from FR-013 |
| Provider Credentials Summary | text | Yes | Licenses/certifications summary | Read-only; sourced from FR-015 |
| Expiry Timer | timer | Yes | Countdown for the parent quote; shows static "Expired on [date]" when expired | Applies to every child subquote |
| Subquotes | list | Yes | All patient-visible subquotes contained by the parent quote | One or more; ordered; each rendered using the subquote fields below |
| Message Provider | button | Yes | Ask the provider about this quote response | Opens that provider's conversation in the dedicated FR-012 Messages/Inbox; does not embed chat in the quote screen |

**Per-Subquote Fields** (repeated for every selectable subquote):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Subquote Reference | text | Yes | Stable identifier and version for the atomic patient choice | Resolves one Quote Option ID and one Option/date-price ID under exactly one parent quote; `subquoteVersion` equals the owning parent aggregate `QuoteVersion` |
| Package | group | Yes | Selected package snapshot for this subquote | Includes package name, description, and source/version provenance |
| Included and Custom Services | checklist | Yes | Services included in this subquote | Read-only quote-owned snapshot |
| Date Range | date range | Yes | Applicable patient-requested treatment range for this subquote | Exactly one range in the selectable subquote |
| Appointment Details | group | Yes | Provider-defined appointment date, time, and timezone | Must fall within the subquote date range |
| Price | amount | Yes | Offered price for this subquote as entered by the provider, before any promotion (FR-004), with the price after promotion shown next to it when a promotion applies | Uses the parent quote currency snapshot; no patient editing |
| Promotion | group | No | Structured promotion attached to this subquote, with its discount shown separately from the offered price | Read-only; show terms when present |
| Price per Graft | number | Yes | Subquote price divided by inherited graft count | Calculated; non-editable |
| Treatment Plan | ordered list | Yes | Relative day-to-day plan for this subquote | Inherits appointment as the schedule anchor; no stored calendar dates derived here |
| State | badge | Yes | Available, Accepted, Not Selected, Expired, Withdrawn, or Cancelled | Derived from parent/subquote lifecycle |
| Actions | buttons | Yes | View Details and Accept | Accept enabled only for a current eligible subquote |

**Subquote List & Comparison Panel Fields** (list controls always visible; comparison panel renders only when at least two subquotes are selected):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Parent Quotes Received | grouped list | Yes | Parent quote responses grouped under their providers | Includes multiple providers and multiple parent quotes from the same provider |
| Sort & Filter | controls | Yes | Sort/filter subquotes. Sort options: Price (Low–High), Price (High–Low), Graft Count, Rating, Appointment Date, Quote Date. Filter: by patient-submitted date range. Default sort: Quote Date (most recent). | Criteria evaluate the complete subquote plus inherited parent/provider values. Price sorting converts each price to the patient's display currency at the current rate for ordering only; each card still shows its own quote currency, and when the listed subquotes use more than one currency the price order is labelled approximate; see FR-022 / `FR-005 / Screen 1` |
| Compare Selection | checkbox | No | Select subquotes to compare side-by-side | Maximum three eligible subquotes, regardless of parent quote/provider grouping |
| Comparison View | panel | No | Side-by-side comparison of complete subquotes | Renders only when at least two are selected |
| Comparison Differentiators | table | Conditional | Comparison rows across selected subquotes | Must include package, included/custom services, date range, appointment details, total price, currency, promotion, price per graft, inherited graft count, provider rating/count, provider credentials, and treatment plan |

**Business Rules**:

- Parent quotes are grouping and inheritance boundaries; they are not patient-selectable acceptance items.
- A subquote is the lowest-level complete commercial choice and the only selectable acceptance item.
- A parent quote offers up to (number of Quote Options × number of date ranges) subquotes. A provider may leave out an option and date-range pairing it cannot offer, so the actual count can be lower; every Quote Option has at least one date range.
- The comparison panel always shows the current parent quote version. If the provider re-versions a parent quote, the panel refreshes to the current version; if a compared subquote no longer exists or becomes ineligible, it drops out of the panel and the patient is told why.
- Expired or withdrawn parent quotes make all child subquotes ineligible; terminal child subquotes are visually disabled.
- Exactly one subquote acceptance is permitted per inquiry.
- Patient can sort/filter subquotes and compare up to three side-by-side, including siblings under one parent quote or subquotes from different parent quotes/providers.
- Patient can view subquote details and accept an eligible subquote directly from the dashboard.
- If inquiry stage is "Cancelled", all Accept buttons and Compare checkboxes are disabled; dashboard is read-only with "Cancelled" badge; quote data remains visible for reference (see FR-003 Workflow 5, Alternative Flow A4 above).

#### Screen 2: Subquote Detail with Accept Action (Extension of FR-004 Screen 4)

**Purpose**: Patient views one complete subquote with inherited parent context and accepts that subquote

**Note**: This extends FR-004's Patient Platform Screen 4 (Quote Review) by adding the Accept button with terms acknowledgment and acceptance confirmation flow.

**Enhancements to FR-004 Screen 4**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Terms Acknowledgment | checkbox | Yes | Confirm understanding of policies | Required to proceed with acceptance |
| Selected Subquote Summary | group | Yes | Package, included/custom services, date range, appointment, price, promotion, and treatment plan | Must identify the exact current parent aggregate `QuoteVersion`, also recorded as `subquoteVersion` |
| Promotion Code | text input | No | Patient-entered promotion code for this named subquote | Validated through FR-019 before acceptance; applies to this subquote only; discounted price shown when valid; not available after acceptance |
| Inherited Parent Context | group | Yes | Provider, treatment, graft information, visual plan, clinicians, common notes/requirements, and attachments | Read-only; inherited from parent quote |
| Accept Button | button | Yes | Accept this subquote | Disabled when the subquote or parent quote is ineligible or another subquote is accepted |
| Acceptance Confirmation Modal | modal | Yes | Summary confirmation before finalizing | Shows the complete subquote and inherited context |

**Business Rules**:

- All relevant parent quote and subquote details from FR-004 Screen 4 are displayed read-only.
- Terms acknowledgment checkbox must be checked before Accept button is enabled.  
- Accept button is disabled if the subquote or parent quote is expired, withdrawn, cancelled, superseded, or stale, or another subquote is already accepted.
- Tapping Accept opens the confirmation modal with the complete subquote summary, inherited context, and next steps.
- Detail reflects the latest provider edits; confirmation rejects a stale version; the accepted subquote and inherited context lock on acceptance.
- A patient-entered promotion code (Alternative Flow A8) applies only to this subquote; the discounted price is shown in the summary and frozen into the acceptance snapshot on confirmation.

#### Screen 3: Acceptance Confirmation Modal

**Purpose**: Confirm acceptance and show next steps before finalizing

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Subquote Summary | group | Yes | Exact package, services, date range, appointment details, pricing, promotion, treatment plan, provider, and inherited treatment facts | Must reflect the latest subquote and parent versions |
| Terms Acknowledgment | checkbox | Yes | Confirm understanding (if not already acknowledged) | Required if not already checked |
| Next Steps | note | Yes | Booking & Payment handoff information | Read-only |
| Confirm | action | Yes | Finalize acceptance | Enabled when eligible |
| Cancel | action | Yes | Return to quote detail | Always available |

**Business Rules**:

- Modal appears after patient taps Accept on a subquote detail screen.
- Confirmation is idempotent; duplicate confirmations do nothing.  
- If the slot is taken by another acceptance before confirmation completes, the modal shows the error state "This appointment slot was just taken. Please choose another subquote.", no acceptance is recorded, and the patient returns to the inquiry dashboard (Alternative Flow A5).
- Post-confirmation, modal closes and patient is directed to booking/payment entry.  
- Patient can cancel to return to quote detail screen.

### Provider Platform (Read-only in this module)

#### Screen 4: Quote Outcome Notification

**Purpose**: Inform provider of acceptance outcome

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Parent Quote Outcome | badge | Yes | Accepted, Expired, Withdrawn, Cancelled (other accepted), or Cancelled (Inquiry Cancelled) | Read-only parent lifecycle state |
| Subquote Outcome | badge/list | Yes | Accepted, Not Selected, Expired, Withdrawn, or Cancelled for each child choice | Exactly one Accepted across the inquiry |
| Selected Subquote | group | Conditional | Package, date range, appointment details, price, currency, and promotion accepted from this provider, read from the acceptance snapshot | Shown only to the selected provider; read-only |
| Reason | text | No | If non-selected: "Other subquote accepted" or "Inquiry cancelled by patient" | Must not identify another provider or disclose accepted price |
| Audit Link | link | Yes | View version/audit history | Read-only |

### Admin Platform

#### Screen 5: Acceptance Oversight Dashboard

**Purpose**: Monitor acceptance events and manage exceptions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Global Acceptance Table | table | Yes | All subquote acceptance events with parent quote/provider references and filters | Admin-only; status filter includes active, booking cancelled (derived from the FR-006 booking cancellation, with no supersession record), and superseded (provider fault, including provider suspension or deactivation, derived from linked supersession records) |
| Accepted Selection | group | Yes | Accepted subquote package, date range, appointment details, price, currency, exchange rate and its timestamp, promotion, and inherited context | Immutable acceptance snapshot |
| Supersession Indicator | badge | No | Shows if acceptance was superseded by a provider-fault transfer, or that its booking was cancelled | "Superseded — Provider Fault" links to the replacement admin-authored acceptance record; "Booking Cancelled" is read from the FR-006 booking cancellation and links to its audit trail; no supersession record exists for a cancellation |
| Conflicts | badge | No | Flagged races or errors | Investigated by admin; the first valid acceptance stands; findings recorded as an annotation |
| Annotations | list | No | Admin notes and corrections recorded next to the acceptance | Append-only; each shows author, time, and reason |
| Actions | actions | Yes | Add note or correction with reason | Audited; appends an annotation and never alters the AcceptanceEvent, its snapshot, or any quote state; no delete or restore action exists |

---

## Business Rules

### General Module Rules

1. A patient can accept exactly one subquote per inquiry; a parent quote cannot be accepted directly. Subsequent acceptance attempts are blocked with guidance, including after `Payment Window Expired` (Alternative Flow A7). The one exception is a provider-fault transfer handled in FR-006: when, after acceptance, the accepted provider withdraws, drops out, or has a suspension or deactivation take effect (Alternative Flow A6), an admin authors a replacement quote for the replacement provider (FR-004 Screen 8) and records a new admin-authored acceptance that points to that quote, option, and option/date-price row (Alternative Flow A9). The original AcceptanceEvent is never edited. The closure itself is recorded on the booking as its cause; one supersession record, written once at the replacement acceptance, links the closed acceptance to the new one with the provider-fault cause (`ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated`). This applies only before treatment starts; in Aftercare an admin reassigns only the aftercare provider or team, with no new acceptance or payment. The patient keeps the same inquiry and re-enters nothing. Money already paid moves with the patient as credit toward the replacement booking, with any unused part refunded and no cancellation fee for the patient; the exact payment mechanics are defined in the payment requirements (FR-007, FR-007b, FR-017).
2. A valid subquote acceptance atomically acquires an exclusive hold on its appointment slot, locks that subquote and its inherited parent context, marks its sibling subquotes Not Selected, and auto-cancels every competing parent quote for the same inquiry with clear reasons and notifications. If the slot is already held or blocked, the acceptance attempt fails before any of those state changes.
3. Acceptance does not reveal patient full identity to provider; full PII becomes accessible only after successful payment confirmation, per constitution.  
4. All acceptance-related state transitions are immutably audited (who, when, what, reason).  
5. A subquote is ineligible if it or its parent quote is expired, withdrawn, cancelled, archived, superseded, or no longer the version presented to the patient, or if its owning provider is `Suspended` or `Deactivated` (FR-015).
6. All deletes are soft deletes; no hard deletes permitted. AcceptanceEvents, accepted subquotes, and their parent quotes are never deleted or restored; admins may only add audited annotations next to them.
7. Notifications sent to non-selected providers (due to auto-cancellation) MUST NOT reveal the identity of the selected provider or the accepted price.
8. Provider-status handling (Alternative Flow A6; FR-015 A5/Screen 4) uses cause `ProviderSuspended` or `ProviderDeactivated` with an independent `supportRequired` marker. Before acceptance, it blocks Accept and cancels that provider's parent quotes. After acceptance, it follows the provider-fault transfer in Business Rule 1: the booking closes with that cause, the hold is released, and an admin rehomes the patient within the same inquiry; the AcceptanceEvent is superseded through a linked supersession record written when the replacement acceptance is recorded. It is distinct from patient inquiry cancellation (A4) and Payment Window Expired, and does not reclassify Completed or already-terminal history.

### Data & Privacy Rules

1. Patient identifiers remain anonymized to providers at this stage.  
2. All data in transit and at rest is protected according to platform policies.  
3. Audit logs must record the accepted subquote, inherited parent snapshot, actor, presented versions, and every affected parent quote and sibling subquote.
4. Retention: acceptance and related quote/subquote records retained ≥ 7 years.

### Admin Editability Rules

**Editable by Admin**:

- Add a note or correction next to an acceptance record with reason (audited annotation). An annotation never alters the AcceptanceEvent, its snapshot, the accepted IDs/versions, or any quote, subquote, or inquiry state. A flagged race or error is investigated and recorded the same way; the first valid acceptance stands.
- Perform a provider-fault transfer through FR-006, authoring the replacement quote on FR-004 Screen 8 and recording the new linked admin-authored acceptance record (Business Rule 1, Alternative Flow A9).
- Cancel a booking after acceptance, from any booking state, through FR-006 with a mandatory reason and audit, when the patient contacts support (Alternative Flow A4).
- Configure notification behaviors via centralized settings (separate FR).

**Fixed in Codebase (Not Editable)**:

- Patient identity reveal policy: only post-payment confirmation.  
- Subquote acceptance uniqueness constraint per inquiry.
- Soft delete policy (no hard deletes).
- AcceptanceEvent immutability: no delete, restore, or edit of an AcceptanceEvent, accepted subquote, or its parent quote; annotation only.

**Configurable with Restrictions**:

- Acceptance confirmation copy/UX notes (content-managed); legal text controlled centrally.

### Payment & Billing Rules (for Handoff)

- Acceptance prepares booking/payment handoff; no funds are collected in this module.  
- The accepted subquote is the complete handoff unit. It carries the selected package, date range, appointment date/time/timezone, offered price, promotion when applicable, and references to the inherited parent quote/provider/treatment context.
- Patient acceptance of the subquote constitutes acceptance of its exact appointment and price. FR-006 must not ask the patient to select another package, date range, appointment, or quote price.
- On acceptance, the system MUST ensure the quote exchange rate is locked at the time of acceptance per FR-004 / System PRD pricing rules, and MUST record the rate and its timestamp in the acceptance snapshot. If the cached rate is older than 24 hours at acceptance, acceptance proceeds on the cached rate and records it with its timestamp; no review state is added, and operations may review afterwards.
- Pricing and promotions shown are those attached to the subquote, plus any patient-entered promotion code applied to that subquote before acceptance (Alternative Flow A8). The resulting price and promotion are frozen into the acceptance snapshot; nothing after acceptance changes them except the provider-fault transfer in Business Rule 1, which creates a new linked record.
- Auto-applied promotion use: a sent parent quote carrying an auto-applied promotion holds at most one reserved use under FR-019; re-sending a new version keeps it, creates one only if the new version newly carries the promotion, and releases it if the new version no longer does. Acceptance consumes the reservation for the accepted parent quote and releases the reservations of sibling and competing parent quotes when they end Not Selected or auto-cancelled. If the booking reaches `Payment Window Expired` or is cancelled before the first payment, the consumed use returns to the limit; an admin revive takes it again only if the limit has room, as defined by FR-019. Provider-selected promotions and patient-entered codes keep the FR-019 lifecycle of reserve at acceptance and consume at first payment. Promotion usage limits count reservations plus consumed uses, so they cannot be exceeded.
- Binding snapshot fields: price, currency, date range, appointment, and promotion are the binding fields and are read from the acceptance snapshot by every downstream module; the snapshot never changes after acceptance. The appointment in the snapshot is the accepted baseline: an admin may later change the booking's appointment through FR-006, which emits `booking.rescheduled`, and every booking notice reads the booking's current appointment rather than the snapshot. The treatment details in the snapshot (treatment plan, clinicians, graft information) are the original record at acceptance. After acceptance, only the clinic or an admin may change the plan, clinicians, or grafts, through FR-010 only; each change is audited and the patient is notified, and the snapshot itself is never edited.
- Post-Acceptance Hold: Acceptance and exclusive slot reservation are one atomic operation. Acceptance places one fixed hold keyed by provider, appointment date/time, and time zone for the FR-026 slot-hold duration (default 48 hours), starting at acceptance, so the patient can complete the first payment (deposit or first instalment). The hold blocks other patients from that slot for the hold period. Payment failures or retries never extend the hold. A second acceptance targeting the held or blocked slot is rejected. The appointment record is created by FR-006 only when the first payment succeeds. If the first payment does not succeed before the hold ends, the hold is released, no appointment exists, and the booking moves to `Payment Window Expired` (Alternative Flow A7).
- Cancellation During Hold: The patient cannot cancel the inquiry after acceptance and is offered "Contact support" instead. If an admin cancels the booking through FR-006 while the appointment slot hold is active, the hold is released immediately and the slot is returned to the provider's availability; the booking and the inquiry become `Cancelled`, and the accepted subquote and its parent quote stay `accepted`. See FR-026 for the slot-hold duration and FR-006 for the admin cancellation and booking-side guard rules.
- Provider Status Change During Hold: If the accepted subquote's provider becomes `Suspended` or `Deactivated` while the hold is active, the hold is released even if time remains, FR-006 closes the booking with cause `ProviderSuspended` or `ProviderDeactivated` and blocks booking-confirming payment to that provider, and the provider-fault transfer in Business Rule 1 applies: an admin rehomes the patient to a replacement provider within the same inquiry, and the supersession record is written when the replacement acceptance is recorded (Alternative Flow A9). The acceptance snapshot and locked price/exchange rate are retained unchanged, and money already paid follows the Business Rule 1 placeholder.

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: 95% of patients can compare and accept a subquote within 3 minutes.
- **SC-002**: <2% of acceptance attempts fail due to expired quotes (clear guidance shown).  
- **SC-003**: Patient satisfaction for quote review flow ≥ 4.5/5.

### Provider Efficiency Metrics

- **SC-004**: 100% of sibling subquotes and competing parent quotes receive the correct non-selected/cancelled outcome within 10 seconds of acceptance.
- **SC-005**: 100% acceptance outcomes correctly reflected in provider dashboards.

### Admin Management Metrics

- **SC-006**: 100% acceptance events fully auditable with immutable logs.  
- **SC-007**: 95% of conflicts (if any) resolved within one business day.

### System Performance Metrics

- **SC-008**: Acceptance action completes in ≤ 2 seconds for 95th percentile.  
- **SC-009**: Notifications delivered within 30 seconds for 95% of events.  
- **SC-010**: Zero hard deletes; archival retrieval success = 100%.

### Business Impact Metrics

- **SC-011**: ≥ 30% of inquiries with quotes proceed to acceptance.  
- **SC-012**: ≥ 90% of accepted subquotes proceed to booking initiation (next FR) within the configured hold window (default 48 hours).

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-003 / P-02, PR-02, A-01**: Inquiry submission & distribution (source inquiry and medical context).  
- **FR-004 / PR-02**: Parent quote, Quote Option, option/date-price, expiry, withdrawal, aggregate `QuoteVersion`, and audit contracts. FR-005 combines one Quote Option and one option/date-price record into one complete patient-selectable subquote whose `subquoteVersion` equals the owning parent `QuoteVersion`.
- **FR-020 / S-03**: Notifications & alerts (event delivery).  
- **FR-012 / P-06, PR-07, A-10**: Messaging & communication (Patient ↔ Provider quote questions through the dedicated Messages/Inbox; Admin monitors and intervenes only under FR-012 policy).
- **FR-013 / P-02, A-01**: Reviews & Ratings (source for provider review rating/count shown in comparison).  
- **FR-015 / A-02**: Provider Management & Onboarding (source for provider credentials/licenses/certifications summary, provider status eligibility, and the suspension/deactivation cancellation cascade in Alternative Flow A5 and Screen 4).  
- **FR-006 / P-03, PR-02, A-01**: Booking & Scheduling consumes the FR-005 `AcceptanceEvent`, accepted parent quote ID/version, accepted subquote ID/version, immutable acceptance snapshot, and pre-scheduled slot without package, date, appointment, or price reselection; it owns payment initiation, booking confirmation, and post-payment PII reveal.
- **A-09**: System settings (legal copy and terms acknowledgment text).
- **FR-026 / A-09**: App Settings & Security owns the versioned, audited slot-hold duration (default 48 hours) applied from acceptance.
- **FR-019**: Promotions & Discounts validates patient-entered promotion codes before acceptance and owns promotion usage-limit handling.
- **FR-010**: Treatment Execution is the only route for post-acceptance changes to treatment plan, clinicians, and grafts, with audit and patient notice.

### External Dependencies

- None specific beyond shared notification services and standard platform integrations.

### Data Dependencies

- Inquiry (from FR-003), parent quotes and complete subquotes (from FR-004), Notification endpoints (FR-020), and legal/policy configuration (A-09) and slot-hold configuration (FR-026).

---

## Assumptions

### User Behavior Assumptions

- Patient has exactly one active inquiry for which quotes exist.  
- Patients do not have an explicit "decline" action; sibling subquotes become Not Selected and competing parent quotes auto-cancel on acceptance or expire by policy.

### Technology Assumptions

- Providers have submitted valid parent quotes containing one or more complete, patient-visible subquotes per FR-004.
- Booking & Payment module is available for immediate handoff post-acceptance.

### Business Process Assumptions

- Acceptance alone does not disclose patient full identity to provider; reveal occurs after successful payment confirmation.  
- Admin legal copy and acknowledgment text are centrally managed.  

---

## Implementation Notes

### Technical Considerations

- Idempotent acceptance keyed to inquiry and accepted subquote: repeat requests do not create multiple accepted states.
- Concurrency control prevents races across any subquotes belonging to the same inquiry.
- Confirmation validates the presented parent aggregate `QuoteVersion` and rejects the selection unless `subquoteVersion` equals that current version before locking an immutable acceptance snapshot.
- Append-only audit trail covers acceptance, sibling Not Selected outcomes, and competing parent quote cancellations.

### Integration Points

- Consumes parent quote and subquote data from FR-004; updates inquiry, parent quote, and subquote states; triggers notification service; emits the accepted subquote handoff payload.

### Scalability Considerations

- Support high-volume acceptance during peak times without delays to notification or state transitions.

### Security Considerations

- Enforce privacy rules: no PII reveal on acceptance; RBAC for all actors; full audit of state transitions; encryption at rest/in transit.

---

## User Scenarios & Testing

### User Story 1 - Accept a Subquote (Priority: P1)

Patient compares complete subquotes across all received parent quotes and accepts one to proceed to booking.

**Independent Test**: Accept one subquote; verify its complete commercial selection and inherited context are snapshotted, siblings become Not Selected, competing parent quotes auto-cancel, and audit/notifications are emitted.

**Acceptance Scenarios**:

1. Given multiple providers and multiple parent quotes, when the patient opens the inquiry, then every eligible package/date/appointment/price combination is presented as a complete subquote under its parent quote.
2. Given eligible sibling subquotes, when the patient compares them, then each comparison column represents one complete subquote and displays inherited parent/provider facts without duplicating their ownership.
3. Given a valid subquote, when the patient accepts it, then that exact subquote and inherited parent context are locked, its parent quote becomes Accepted, sibling subquotes become Not Selected, and competing parent quotes auto-cancel.
4. Given an already accepted inquiry, when the patient attempts to accept another subquote, then the system blocks the request with guidance.
5. Given acceptance success, when the system prepares handoff, then Booking receives the accepted package, date range, appointment details, price, promotion, currency/exchange-rate snapshots, and inherited quote/provider/treatment references without collecting payment in FR-005.

### User Story 2 - Handle Expired Parent Quote (Priority: P2)

Patient attempts to accept a subquote whose parent quote has expired.

**Independent Test**: Confirm every child subquote is blocked when its parent expires; display expiry; allow selection of eligible subquotes from other parent quotes.

**Acceptance Scenarios**:

1. Given an expired parent quote, when the patient views any child subquote or taps Accept, then the system shows "Expired" and disables acceptance for every child subquote.
2. Given multiple parent quotes with one expired, when the patient views the inquiry dashboard, then the expired group and its subquotes are visually distinguished while eligible subquotes elsewhere remain available.

### User Story 3 - Inquiry Cancellation During Subquote Review (Priority: P2)

Patient cancels the inquiry while subquotes are available for review; after acceptance the patient is routed to support and an admin cancels the booking.

**Independent Test**: Patient cancels the inquiry in the Quoted stage and tries to cancel after accepting a subquote; verify the pre-acceptance cancellation cancels all parent quotes and subquotes, locks the UI, and notifies providers, and verify that after acceptance only "Contact support" is offered and the admin cancellation leaves the accepted quote `accepted`.

**Acceptance Scenarios**:

1. Given the patient has multiple parent quotes and subquotes in Quoted stage, When the patient cancels the inquiry, Then all parent quotes and subquotes transition to "Cancelled (Inquiry Cancelled)"; Accept/Compare actions are disabled; dashboard shows "Cancelled" read-only
2. Given the patient has accepted a subquote with an active appointment slot hold, When the patient looks for a cancel action, Then only "Contact support" is offered; and When an admin cancels the booking through FR-006 with a reason, Then the booking and inquiry become `Cancelled`, the accepted subquote and parent quote stay `accepted`, the AcceptanceEvent stays unchanged with no supersession record, and the slot hold is released immediately regardless of its configured duration
3. Given provider views their quote outcome after patient cancels inquiry, When opening Screen 4, Then Outcome badge shows "Cancelled (Inquiry Cancelled)" with reason "Inquiry cancelled by patient"
4. Given an admin cancelled a booking after acceptance, When an admin filters acceptance oversight, Then the acceptance event is visible with the "Booking Cancelled" badge, linked to the FR-006 cancellation audit trail, and has no supersession record

### User Story 4 - Acceptance Outcome Notices (Priority: P1)

Providers learn the outcome of each sent parent quote when the patient accepts a subquote, without any leak of the winner's identity or price.

**Independent Test**: Accept one subquote in an inquiry with a same-provider sibling parent quote, a competing provider, and an unsent draft; verify each notice, its content, and that no `quote.declined` event is emitted.

**Acceptance Scenarios**:

1. Given the patient accepts a subquote, When outcome notices are sent, Then the selected provider receives one "selected" notice for the accepted parent quote showing the accepted package, date range, appointment, price, currency, and promotion read from the acceptance snapshot.
2. Given the selected provider also sent another parent quote for the same inquiry, When outcome notices are sent, Then that provider receives one separate "not selected" notice for the other parent quote, and sibling subquotes inside the accepted parent quote are shown as Not Selected without a separate notice per subquote.
3. Given a competing provider sent a parent quote, When outcome notices are sent, Then that provider receives one "not selected" notice per sent parent quote with reason "Other subquote accepted", and the notice does not contain the selected provider's identity or the accepted price.
4. Given a provider holds an unsent draft quote for the inquiry, When another quote is accepted, Then FR-004 cancels the draft silently and no notice is sent for it.
5. Given any acceptance, When outcome events are emitted, Then no `quote.declined` event is emitted for any provider (FR-020).
6. Given the patient accepts a subquote, When notices are sent, Then the patient receives only `booking.scheduled` ("Booking Accepted — Slot Held (Pending Payment)") and no `quote.accepted` notice; `quote.accepted` outcome notices go to providers only.

### User Story 5 - Acceptance Exceptions and Hold Expiry (Priority: P2)

The system rejects unsafe acceptances and handles the end of the payment window predictably.

**Independent Test**: Exercise slot conflict, stale version, same-provider competing parent cancellation, hold expiry, provider suspension, promotion code entry, and admin annotation; verify the stated outcome for each.

**Acceptance Scenarios**:

1. Given the subquote's appointment slot is already held or blocked by another booking, When the patient confirms, Then acceptance is rejected before any AcceptanceEvent, state change, or handoff, and the patient sees "This appointment slot was just taken. Please choose another subquote." (Alternative Flow A5).
2. Given the provider re-versioned the parent quote after the patient opened confirmation, When the patient confirms, Then the stale confirmation is rejected and the patient must review the current version.
3. Given the same provider sent two parent quotes and the patient accepts a subquote in one, When acceptance completes, Then the other parent quote from that provider is auto-cancelled with reason "Other subquote accepted", like any competing parent quote.
4. Given an accepted subquote whose hold ends without a successful first payment, When the hold expires, Then the hold is released, no appointment exists, the accepted subquote cannot be accepted again, and the patient is offered "Contact support" for an admin revive or an admin booking cancellation (Alternative Flow A7).
5. Given the owning provider becomes `Suspended` while the patient is confirming, When confirmation is revalidated, Then acceptance is rejected and no AcceptanceEvent or hold is created (Alternative Flow A6).
6. Given the patient enters a valid promotion code on a named subquote, When the patient accepts it, Then the discounted price and promotion are frozen into the acceptance snapshot; and Given acceptance is complete, When anyone tries to remove, replace, or re-enter a promotion, Then the request is rejected (Alternative Flow A8).
7. Given the cached exchange rate is older than 24 hours, When the patient accepts, Then acceptance proceeds and the snapshot records the rate and its timestamp.
8. Given an admin adds a note or correction to an AcceptanceEvent, When the annotation is saved, Then it is audited and the AcceptanceEvent, snapshot, and all quote states are unchanged; no delete or restore action is offered.
9. Given acceptances and parent quote responses occur, When analytics are recorded, Then each parent quote counts once in Parent Quote Responses and each acceptance counts once in Subquote Selections (REQ-005-020).
10. Given two patients confirm subquotes for the same provider, appointment date/time, and time zone at the same moment, When both acceptances are processed, Then the first acquires the active hold and the second fails because that hold already exists; the second patient sees "This appointment slot was just taken. Please choose another subquote." and no Accepted state, AcceptanceEvent, or handoff is created for the second patient (Alternative Flow A5).
11. Given the accepted parent quote and a competing parent quote each carry an auto-applied promotion with a use reserved at send, When acceptance completes, Then the accepted quote's reservation is consumed and the competing quote's reservation is released (FR-019).
12. Given a sent parent quote holds a reserved automatic-promotion use on some of its rows, When the patient accepts a subquote whose row does not carry that promotion, Then the reservation is released with reason `not_applied` and no use is consumed.
13. Given a provider-fault closure before treatment starts, When the admin records the replacement acceptance against an admin-authored replacement quote, Then a new AcceptanceEvent with `actorType = admin` points to that quote, option, and option/date-price row, one supersession record links the closed acceptance to it, the patient receives `booking.scheduled`, and the replacement provider receives `quote.accepted` (Alternative Flow A9).

### Edge Cases

- Network loss during acceptance: system retries safely; no duplicate accept states.  
- Simultaneous accept attempts across devices: first valid acceptance wins; others see informative message.  
- Provider withdraws the parent quote during confirmation: subquote acceptance is blocked with explanation; return to inquiry dashboard.
- Admin finds a quote or subquote was cancelled by mistake: no restore action exists; the admin records the finding as an audited annotation, prior acceptance is not overridden, and the patient uses the recovery routes in Alternative Flows A1 and A7.
- Patient accepts a subquote then immediately wants to cancel: no patient cancel action exists after acceptance; the patient is offered "Contact support", and an admin cancellation through FR-006 moves the booking and inquiry to `Cancelled`, keeps the accepted subquote and parent quote `accepted`, writes a linked supersession record, and releases the slot hold.
- Patient attempts to accept a subquote while inquiry cancellation is being processed: system checks inquiry status at confirmation; if cancelled, blocks acceptance with message "This inquiry has been cancelled."
- Provider edits either the parent quote or selected subquote after the patient opens confirmation: system rejects the stale confirmation and requires review of the current version.
- Patient cancels inquiry while on the acceptance confirmation modal (Screen 3): modal dismissed; inquiry dashboard refreshes to show "Cancelled" badge; all actions disabled.
- Provider becomes `Suspended` or `Deactivated` while the patient is on the confirmation modal: confirmation is rejected at revalidation; the patient sees the inline error "This provider is no longer available. Please contact support." with a Contact Admin/Support action (Alternative Flow A6) and may choose another provider's eligible subquote if the inquiry is still comparing.
- Provider-status cascade is replayed or a stale acceptance request arrives afterward: no duplicate cancellation, notification, AcceptanceEvent, or hold is created.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-005-001**: System MUST show every parent quote received for an inquiry, including multiple parent quotes from the same provider, and MUST expose each child subquote as a complete patient-selectable commercial choice.
- **REQ-005-002**: System MUST allow the patient to accept exactly one valid subquote per inquiry and MUST NOT allow direct acceptance of a parent quote or any upper-level inherited record.
- **REQ-005-003**: On acceptance, System MUST mark sibling subquotes in the accepted parent quote Not Selected and MUST auto-cancel all competing parent quotes for the same inquiry with reasons and notifications.
- **REQ-005-004**: System MUST block subquote acceptance when the subquote or its parent quote is expired, withdrawn, cancelled, archived, superseded, or stale, with clear messaging.
- **REQ-005-005**: System MUST prepare the booking/payment handoff from the accepted subquote without collecting funds in this module.

### Data Requirements

- **REQ-005-006**: System MUST preserve an immutable acceptance snapshot containing the accepted subquote identifier/version, the underlying Quote Option ID and Option/date-price ID, the source package ID/version, the parent quote identifier/version and expiry, provider and inquiry references, treatment ID/version, package and service snapshot, date range, appointment date/time/timezone, offered price, any patient-applied promotion code and the resulting discounted price, promotion, currency, exchange rate and its timestamp, treatment plan, estimated grafts, graft description, visual plan, clinician IDs, notes, requirements, attachment IDs with versions, actor, and timestamp; `acceptedSubquoteVersion` MUST equal `acceptedParentQuoteVersion` because both identify the same FR-004 aggregate revision; all resulting state changes MUST be audited. Price, currency, date range, appointment, and promotion are the binding fields that downstream modules MUST read from the snapshot; the snapshot appointment is the accepted baseline, and booking notices MUST read the booking's current appointment, which only an FR-006 admin appointment change can alter. The treatment details are the original record at acceptance; later changes to plan, clinicians, or grafts are made only through FR-010 with audit and patient notice, and never edit the snapshot.
- **REQ-005-007**: System MUST retain acceptance and related parent quote/subquote records for ≥ 7 years.

### Security & Privacy Requirements

- **REQ-005-008**: System MUST keep patient identity masked to providers until payment confirmation.  
- **REQ-005-009**: System MUST encrypt data at rest and in transit and enforce RBAC for actions.

### Integration Requirements

- **REQ-005-010**: System MUST integrate with FR-004 for parent quote, Quote Option, option/date-price, lifecycle, aggregate `QuoteVersion`, and audit contracts and with FR-020 for notifications.
- **REQ-005-011**: System MUST emit a booking handoff whose atomic commercial input is the accepted subquote and whose inherited context is resolved from its parent quote.
- **REQ-005-012**: System MUST allow patients to filter and sort subquotes using both subquote-owned and inherited comparison criteria.
- **REQ-005-013**: System MUST support side-by-side comparison of up to three subquotes, regardless of whether they belong to the same or different parent quotes/providers.
- **REQ-005-014**: System MUST display these subquote comparison differentiators: package, included/custom services, date range, appointment details, total price, currency, promotion, price per graft, treatment plan, inherited graft count, provider review rating/count, and provider credentials summary. Estimated travel costs remain deferred pending an approved FR-008 source.
- **REQ-005-015**: Patients MUST be able to ask providers questions about quotes through the dedicated FR-012 Messages/Inbox; quote screens MAY navigate to the existing provider conversation but MUST NOT embed a chat surface.
- **REQ-005-016**: System MUST notify the provider of patient quote questions within 5 minutes.
- **REQ-005-017**: System MUST lock quote exchange rate at time of patient acceptance (per FR-004 pricing rules) and MUST record the rate and its timestamp in the acceptance snapshot. When the cached rate is older than 24 hours, acceptance MUST proceed on the cached rate and record it with its timestamp, without adding a review state.
- **REQ-005-018**: A subquote MUST resolve exactly one FR-004 Quote Option and one applicable Option/date-price record into one complete package, date range, appointment, and offered-price selection. It MUST inherit shared provider, treatment, graft, visual-plan, clinician, note, requirement, attachment, currency, expiry, and audit context from exactly one parent quote. FR-005 owns the subquote identifier and state: the identifier is derived deterministically from the Quote Option ID and Option/date-price ID, so it stays the same across parent re-versions while both records exist. A parent quote offers up to (number of Quote Options × number of date ranges) subquotes, because a provider may leave out pairings it cannot offer.
- **REQ-005-019**: Acceptance confirmation MUST validate the current parent aggregate `QuoteVersion`, MUST require the derived `subquoteVersion` to equal it, and MUST reject stale selections before creating an AcceptanceEvent.
- **REQ-005-020**: Parent quote and subquote analytics MUST remain distinct: one provider response counts once at parent level (metric: Parent Quote Responses), while comparison and selection behavior is recorded at subquote level (metrics: Subquote Comparisons and Subquote Selections).
- **REQ-005-021**: Acceptance MUST atomically acquire an exclusive hold on the selected appointment slot and MUST reject a second acceptance for a slot already held or blocked by another pending or confirmed booking, including a concurrent acceptance that finds an active hold already exists, before creating an AcceptanceEvent, changing quote/inquiry states, or emitting a booking handoff. The rejected patient MUST be told the slot was just taken.
- **REQ-005-022**: System MUST revalidate the owning provider's status at acceptance and MUST block acceptance of any subquote whose provider is `Suspended` or `Deactivated` from the effective time, including in-flight confirmations. For a still-comparing inquiry, System MUST keep other providers' subquotes acceptable. When the status takes effect after acceptance, System MUST release any active hold, retain the AcceptanceEvent and acceptance snapshot without rewriting, record cause `ProviderSuspended` or `ProviderDeactivated` with `supportRequired` on the FR-006 booking and the FR-003 ProviderInquiry (the supersession record is written only when the replacement acceptance is recorded), route the case to the FR-006 provider-fault transfer within the same inquiry, and tell the patient that an admin will arrange a replacement provider instead of showing the patient-cancellation message.
- **REQ-005-023**: System MUST NOT allow an AcceptanceEvent, accepted subquote, or its parent quote to be deleted, restored, or edited. Admins MAY add audited notes or corrections as annotations next to an AcceptanceEvent; an annotation MUST NOT change the event, its snapshot, or any quote, subquote, or inquiry state.
- **REQ-005-024**: System MUST allow exactly one patient acceptance per inquiry. The only additional acceptance record is the admin-authored record created by an FR-006 provider-fault transfer before treatment starts; it MUST point to an admin-authored FR-004 replacement quote, Quote Option, and option/date-price row, and the original MUST be marked superseded by one supersession record inserted at the replacement acceptance rather than by editing it.
- **REQ-005-025**: Acceptance MUST place one fixed slot hold keyed by provider, appointment date/time, and time zone for the FR-026 slot-hold duration, starting at acceptance. Payment failure MUST NOT extend the hold, and the appointment record MUST be created by FR-006 only on successful first payment. After `Payment Window Expired`, the accepted subquote MUST NOT be reopened; the patient's recovery route is "Contact support", through which an admin performs the FR-006 revive or an FR-006 booking cancellation.
- **REQ-005-026**: System MUST let the patient apply a promotion code to one named subquote before acceptance, validated through FR-019, and MUST freeze the discounted price and promotion into the acceptance snapshot. The code MUST NOT be written to the provider's quote or promotion records, and the price and promotion MUST NOT change after acceptance except through an FR-006 provider-fault transfer.
- **REQ-005-027**: When sorting subquotes by price, System MUST convert each price to the patient's display currency at the current rate for ordering only, MUST keep showing each subquote in its own quote currency, and MUST label the price order approximate when the listed subquotes use more than one currency.
- **REQ-005-028**: On acceptance, System MUST consume the auto-applied promotion use reserved at send for the accepted parent quote and MUST release the reservations of every parent quote that ends Not Selected or auto-cancelled, as defined by FR-019. When the accepted subquote does not carry the automatic promotion reserved for its parent quote, System MUST release that reservation with reason `not_applied`.
- **REQ-005-029**: At acceptance, System MUST send the patient only `booking.scheduled` ("Booking Accepted — Slot Held (Pending Payment)"); `quote.accepted` outcome notices MUST go to providers only. `booking.scheduled` MUST go to the patient only, MUST be mandatory (not disableable), and MUST also fire on an admin-authored replacement acceptance.
- **REQ-005-030**: After acceptance, System MUST NOT offer the patient an inquiry cancel action and MUST show "Contact support" instead; booking cancellation from acceptance onward is performed only by an admin through FR-006.

---

## Key Entities

- **Subquote**: id, parentQuoteId, quoteOptionId, optionDatePriceId, version, packageSnapshot, includedAndCustomServices, dateRange, appointmentAt, appointmentTimezone, offeredPrice, promotionSnapshot, treatmentPlan, state
  - Atomic unit displayed, compared, and accepted by the patient.
  - Resolves one FR-004 Quote Option and one applicable Option/date-price record; neither underlying record is accepted independently in FR-005.
  - `version` is the owning parent quote's aggregate `QuoteVersion`; a subquote has no independent revision counter.
  - Inherits provider and shared treatment/clinical context from exactly one parent Quote.
  - FR-005 owns `id` and `state`; `id` is derived deterministically from `quoteOptionId` and `optionDatePriceId`.
- **AcceptanceEvent**: id, inquiryId, acceptedParentQuoteId, acceptedParentQuoteVersion, acceptedSubquoteId, acceptedSubquoteVersion, quoteOptionId, optionDatePriceId, reservedSlotId, actorId, actorType (patient, or admin for a provider-fault transfer record), acceptedAt, acceptanceSnapshot, handoffMetadata
  - `acceptedSubquoteVersion` MUST equal `acceptedParentQuoteVersion`.
  - `acceptanceSnapshot` preserves the complete subquote plus inherited parent context at acceptance, including the exchange rate and its timestamp and any patient-applied promotion code (REQ-005-006).
  - `reservedSlotId` references the fixed slot hold keyed by provider, appointment date/time, and time zone; it is not an appointment record.
  - The event is append-only: it is never edited, deleted, or restored. Supersession and admin notes are separate linked records.
  - If an admin cancels the booking after acceptance, the event is retained unchanged and no AcceptanceSupersession record is written; the accepted subquote and parent Quote stay `accepted`.
  - If the provider becomes `Suspended` or `Deactivated` after acceptance, the event, accepted IDs/versions, and snapshot are retained unchanged; the cause is recorded on the booking, and the AcceptanceSupersession record with cause `ProviderSuspended` or `ProviderDeactivated` is written when the provider-fault transfer records the replacement acceptance (Alternative Flows A6 and A9).
  - An admin-authored replacement event (`actorType = admin`) references an admin-authored FR-004 replacement quote, Quote Option, and option/date-price row like any other event.
  - Relationships: belongsTo Inquiry; belongsTo accepted parent Quote; belongsTo accepted Subquote.
- **AcceptanceSupersession**: id, supersededAcceptanceEventId, cause (ProviderFault, ProviderSuspended, or ProviderDeactivated, copied from the closed booking's cancellation cause), replacementAcceptanceEventId (always set), actorId, reason, createdAt
  - Linked, append-only record that marks an AcceptanceEvent superseded without editing it. It is inserted only at a provider-fault replacement acceptance, once, and never updated; no other event (including admin cancellation) writes one.
- **AcceptanceAnnotation**: id, acceptanceEventId, authorId (admin), type (note or correction), text, reason, createdAt
  - Audited, append-only admin note; never alters the AcceptanceEvent, its snapshot, or any state.
- **Quote** (from FR-004): id, providerId, version, status, expiresAt; parent and inheritance boundary, never the direct patient acceptance target.
- **AuditEntry**: entityType, entityId, action, actorId, reason, before, after, timestamp

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-03 | 1.0 | Initial PRD creation for FR-005 | Product & Engineering |
| 2025-11-04 | 1.1 | PRD reviewed and verified | Product Owner |
| 2025-11-04 | 1.2 | Template compliance: moved Multi-Tenant Architecture to Module Scope; added MTA bullets; renamed Entry Points; restructured Assumptions into subsections | Product & Engineering |
| 2026-02-05 | 1.3 | Added Alternative Flow A4 (inquiry cancelled during quote review), "Cancelled" to Screen 1 stage badge, read-only blocking rule for cancelled inquiries, appointment slot hold release on inquiry cancellation in Payment & Billing Rules. See FR-003 Workflow 5 and cancel-inquiry-fr-impact-report.md | Product & Engineering |
| 2026-02-08 | 1.4 | Cancellation integrity fixes: Added "Cancelled (Inquiry Cancelled)" to Screen 4 (Provider Outcome) badge and Key Entities Quote status. Added supersededByCancellation field to AcceptanceEvent entity. Added cancellation visibility to Admin Screen 5. Added User Story 3 (inquiry cancellation during quote review) with 4 acceptance scenarios. Added 3 cancellation race-condition edge cases. | AI |
| 2026-02-11 | 1.5 | Clarified Alternative Flow A1 outcome: removed ambiguous "await new quotes" phrasing; explicitly stated patient options are to pick another non-expired quote, cancel inquiry and start new, or contact support. No re-quoting mechanism exists for the same inquiry. Restructured Screen 1 Data Fields into 3 grouped sub-tables (Inquiry-Level Fields, Per-Quote Card Fields, Quote List & Comparison Panel Fields) with explicit Comparison Differentiators field per REQ-005-014. Updated comparison criteria business rule to reference the new table structure. Added "Expired on [date]" display to Expiry Timer for expired state. Added "disabled for expired/withdrawn quotes" to Compare Selection. Renamed "Ask Question" button to "Contact Support" with routing to Hairline Support via FR-012 secure messaging. | AI |
| 2026-04-12 | 1.5.1 | Screen 1 Sort & Filter: replaced "Criteria list must be defined" placeholder with defined sort/filter options; added cross-reference to FR-022 as authoritative source. Originally recorded as a second v1.5 revision; renumbered 1.5.1 on 2026-10-18 so each version has one date. | AI |
| 2026-09-15 | 2.0 | Replaced parent-quote acceptance with atomic subquote comparison and acceptance. A subquote now represents one complete package/date-range/appointment/price choice and inherits upper-level provider and clinical context. Added grouped parent quote presentation, subquote comparison/detail fields, version-safe acceptance snapshot, sibling Not Selected handling, competing parent quote cancellation, complete FR-006 handoff, distinct parent/subquote analytics, REQ-005-018 through REQ-005-020, and CR-FR005-20260915-01. Status reset pending consolidated verification. | Product Owner / Documentation |
| 2026-09-16 | 2.1 | Resolved post-verification contract findings: bound `subquoteVersion` and `acceptedSubquoteVersion` to the owning parent aggregate `QuoteVersion`, and replaced the generic Upcoming FR dependency with the explicit FR-006 accepted-subquote handoff contract. Verification status remains pending consolidated review. | Product Owner / Verification alignment |
| 2026-09-16 | 2.2 | Aligned quote questions with FR-012 Patient ↔ Provider messaging through the dedicated Messages/Inbox, and aligned the post-acceptance slot hold with FR-006/A-09 as configurable with a 48-hour default. Consolidated verification remains pending. | Product Owner / Verification alignment |
| 2026-09-16 | 2.3 | Resolved the acceptance-slot concurrency contract: subquote acceptance now atomically acquires an exclusive appointment hold and rejects a second acceptance before creating an AcceptanceEvent or booking handoff. Consolidated verification remains pending. | Product Owner / Verification resolution |
| 2026-10-14 | 2.4 | Aligned provider suspension/deactivation cancellation cascade per CR-FR015-20261013-01 and FR-015 v1.9: provider-status revalidation at acceptance (Main Flow step 6), Alternative Flow A6, General Module Rules 5 and 8, provider-status hold release in Payment & Billing Rules, edge cases, REQ-005-022, AcceptanceEvent retention note, and FR-015 dependency. Consolidated verification remains pending. | Vân Tay Media |
| 2026-10-16 | 2.5 | MTG-002 quote-model alignment (CR-FR005-20261016-01). Removed soft-delete/restore of acceptance, parent quote, and subquote records and the undefined conflict resolution; added audited annotation only (FR-005-4, D4). Rule 1 and REQ-005-024 now name the single exception: a provider-fault transfer creates a new admin-authored acceptance record linked to the original through a supersession record, with the paid-money placeholder (S1-3, D6, D6-M, D3). Added Alternative Flow A7 for Payment Window Expired recovery with the first-payment-only boundary (S1-1, D1, D2) and REQ-005-025. Hold restated as one fixed hold from acceptance for the FR-026 duration, keyed by provider, appointment date/time, and time zone; appointment created only at first payment (S1-2, S1-6, M3, M4, D14). Snapshot records exchange rate and timestamp; stale cached rate proceeds and is recorded (FR-017-1, D19). Added Alternative Flow A8, Screen 2 Promotion Code, and REQ-005-026 for patient promotion codes frozen at acceptance (FR-019-1, D8, D9). Defined binding money fields and the FR-010-only route for treatment changes (M2), with full snapshot field list (S1-4). Up to options × date ranges subquotes (M1). A3 points to FR-006 for withdrawal after acceptance (S1-3, D3). Added User Story 4 acceptance-outcome notices (FR-020-4, M16, D20, P2) and User Story 5 exception scenarios (FR-005-10). Minors: currency and promotion in comparison and provider outcome (FR-005-7), acceptedTotal write (FR-005-8), compare-panel refresh (FR-005-9), subquote ID ownership and option IDs on AcceptanceEvent (S1-5), AcceptanceEvent id (S1-10), append-only supersession replacing the mutable flag, approvals row, and change-log order (FR-005-11). Corrected stale system-documents line in CR-FR005-20260915-01 (R7-1). Provider suspension or deactivation after acceptance now follows the provider-fault transfer: booking closes with cause ProviderSuspended or ProviderDeactivated (FR-006 B4 to B5), hold released, AcceptanceEvent superseded through the linked record with these causes, admin rehomes the patient in the same inquiry, paid-money placeholder applies; before acceptance unchanged (A6, Rules 1 and 8, Provider Status Change During Hold, REQ-005-022, Key Entities; M18). Consolidated verification remains pending. | Product Owner / Documentation |
| 2026-10-16 | 2.6 | Product Owner Q-series alignment (CR-FR005-20261016-01). Price sort converts to the display currency at the current rate for ordering only, cards keep their own currency, mixed-currency order labelled approximate (Screen 1, REQ-005-027; Q8). Auto-applied promotion use reserved at send is consumed at acceptance and released for quotes that end Not Selected or auto-cancelled (Main Flow step 8, Payment and Billing Rules, US5 scenario 11, REQ-005-028; Q6, Q29 at most one reservation per sent quote across re-sent versions; Q30 consumed use returns to the limit on Payment Window Expired or cancellation before first payment and is re-taken on revive if room remains). Patient receives only `booking.scheduled` at acceptance; `quote.accepted` goes to providers only (Main Flow step 9, US4 scenario 6, REQ-005-029; Q10). Concurrent second acceptance fails on the existing active hold with the "slot was just taken" message and no Accepted state (A5, Screen 3, US5 scenarios 1 and 10, REQ-005-021; Q23). Consolidated verification remains pending. | Product Owner / Documentation |
| 2026-10-18 | 2.7 | Consolidated verification corrections (CR-FR005-20261016-01; decision D14): Payment & Billing Rules, Inquiry Cancellation During Hold, now points to FR-026 for the slot-hold duration and to FR-006 for booking-side guard rules. Consolidated verification remains pending. | Product Owner / Verification alignment |
| 2026-10-18 | 2.8 | Final audit corrections (CR-FR005-20261016-01; decisions Q35, Q36, Q37, Q39, Q42): added Alternative Flow A9 for the admin-authored replacement acceptance, with supersession written once at the replacement acceptance and no new acceptance in Aftercare. Patient cancellation is limited to Inquiry and Quoted; from acceptance onward the patient uses Contact support and an admin cancels the booking, the hold is released and the accepted quote stays `accepted` (A4, A7, Cancellation During Hold, User Story 3, REQ-005-030). Unselected reserved automatic promotions are released with `not_applied`. `booking.scheduled` is patient-only and mandatory; the provider is told through `quote.accepted`; booking notices read the current appointment while the snapshot keeps the baseline. Screen 1 price and promotion fields aligned with FR-004; `supportRequired` named on the booking and ProviderInquiry (REQ-005-022). Renumbered the 2026-04-12 change log row to 1.5.1 and added a document footer. Round-two corrections (Q45, Q49): in Alternative Flow A9 a replacement quote that is not accepted expires under the normal quote expiry, the inquiry stays `supportRequired`, and the admin may author another replacement quote or cancel; the A9 boundary states that an `In Progress` provider fault creates no replacement acceptance. AcceptanceSupersession causes now match the schema (`ProviderFault`, `ProviderSuspended`, `ProviderDeactivated`; `InquiryCancelled` removed), and admin booking cancellation writes no supersession record (AcceptanceEvent entity, Screen 3 acceptance table and indicator, User Story 3 scenarios 2 and 4). | Product Owner |
| 2026-10-28 | 2.9 | Product Owner decision 2026-10-28 (FR-015 backend confirmations); clarification, no Change Request. Alternative Flow A6 Outcome and the confirmation-modal edge case now give the patient copy for a Suspended or Deactivated provider: before acceptance (Accept blocked) "This provider is no longer available. Please contact support." with a Contact Admin/Support action; after acceptance (deposit or booking-confirming payment blocked) "This clinic can no longer perform your treatment. An admin will arrange a replacement clinic within the same inquiry." Both are inline on-screen errors localized through FR-021, not FR-020 notifications. Review follow-up (same day): the action is named Contact Admin/Support, the existing UI action label used in FR-003 and FR-015 | Claude (AI Assistant) |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Product Owner | 2026-10-18 | Documentation approved through v2.7: v2.0 to v2.3 on 2026-09-16, v2.4 alignment per CR-FR015-20261013-01, v2.5 and v2.6 via the MTG-002 quote-model decision log of 2026-10-16 (CR-FR005-20261016-01), and the v2.7 consolidated verification correction of 2026-10-18 applying decision D14; consolidated verification pending |
| Product Owner | Product Owner | 2026-10-18 | Approved via MTG-002 decision log (documentation only), v2.8 final audit corrections (CR-FR005-20261016-01); consolidated verification pending |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-005 from system-prd.md
**Last Updated**: 2026-10-28
