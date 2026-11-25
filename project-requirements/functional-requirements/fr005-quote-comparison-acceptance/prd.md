# FR-005 - Quote Comparison & Acceptance

**Module**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight  
**Feature Branch**: `fr005-quote-comparison-acceptance`  
**Created**: 2025-11-03  
**Status**: ✅ Documentation Approved (baseline 2026-11-25); implementation reconciliation pending
**Source**: FR-005 from system-prd.md; SRC-MTG-002 and CR-FR005-20260915-01

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

- Read-only visibility of the accepted or non-selected outcome for parent quotes and subquotes. (REQ-005-032)
- Competing parent quotes auto-cancelled with reason “Other subquote accepted”; sibling subquotes in the accepted parent quote become “Not Selected”.
- No patient PII is revealed by acceptance; full details remain locked until payment confirmation per constitution.

**Admin Platform (A-01)**:

- Global oversight of quote states and acceptance events across patients/providers.  
- Audited "Add note or correction" annotations on acceptance records. Acceptance events, accepted subquotes, and their parent quotes cannot be deleted or restored, and an annotation never alters the AcceptanceEvent, its snapshot, or any quote state. After acceptance an admin may edit the accepted quote in any field except price, currency, and promotion, with a mandatory reason and full before/after history; the edit is stored as a new version beside the acceptance snapshot, which keeps the terms as accepted (REQ-005-023).
- Investigation of flagged acceptance races or errors (rare): the system sets the flag automatically when a second acceptance is rejected, the first valid acceptance stands, and the admin records findings as an annotation. (REQ-005-033, REQ-005-065)
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
- System → Provider: Notify the provider of patient quote questions within 5 minutes, unless the provider has switched that notice off or held it in their notification preferences (REQ-012-007).
- System → Provider: Accepted-subquote outcome or auto-cancellation updates for non-selected parent quotes.
- Admin → All: Oversight and policy-bound interventions.

**Out of Scope**:

- Direct patient-provider chat (see FR-012: Messaging & Communication).  
- Payment collection and invoice issuance (handled in Booking & Payment FR).  
- Revealing patient contact/identity to provider prior to payment confirmation.

### Entry Points

- Patient accesses from Inquiry Dashboard (FR-003 Screen 8) where quotes are displayed within the inquiry context, or via push/email notification. (REQ-005-031)

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
7. After the exclusive hold succeeds, System records the selected subquote as Accepted, locks its inherited parent context and commercial details, sets the parent quote and inquiry to Accepted, records the acceptance snapshot (including the exchange rate and its timestamp) and the slot-hold reference, and writes the accepted subquote's price after any promotion as the parent quote's accepted total (FR-004 `acceptedTotal`), read from the snapshot. No appointment record is created at acceptance; FR-006 creates it only on successful first payment. (REQ-005-037)
8. System marks every sibling subquote in the accepted parent quote as Not Selected and auto-cancels every competing parent quote for the inquiry with reason "Other subquote accepted." If the accepted subquote carries an auto-applied promotion, the promotion use reserved when its parent quote was sent is consumed now. If the accepted parent quote holds a reserved automatic-promotion use but the accepted subquote does not carry that promotion, the reservation is released with reason `not_applied`. The use reserved by every parent quote that ends Not Selected or auto-cancelled is released (FR-019).
9. System sends notifications to the patient and all affected providers without disclosing the selected provider or accepted price to non-selected providers. Recipients, content, and whether a notice can be switched off are set by the notification Rules: REQ-020-012 for the provider outcome notices (one per sent parent quote, none for unsent drafts, no `quote.declined`) and REQ-020-019 for the patient notice at acceptance (FR-020). (REQ-005-038)
10. System sends the accepted subquote and its inherited context to Booking & Payment; no funds are collected in FR-005.
11. System writes immutable audit entries for the selection and every resulting state transition.

### Alternative Flows

**A1: Parent Quote Expires During Subquote Review**:

- Trigger: Countdown reaches zero while patient is viewing details.  
- Steps: System disables Accept button; shows “Expired” badge and guidance to choose another quote.  
- Outcome: Every subquote under that parent quote becomes ineligible. Patient can choose another eligible subquote from another parent quote if one exists. If none remains, the patient may cancel the inquiry and submit a new one, or contact support. (REQ-005-040)

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
- Steps: System cancels inquiry; the cascade (REQ-003-013) cancels only parent quotes in draft, sent, or expired status, which take status "Cancelled (Inquiry Cancelled)" together with their subquotes, while a quote in any other status keeps its status and cause; no subquote can be accepted, all Accept/Compare actions are disabled; dashboard shows "Cancelled" badge.
- Outcome: Inquiry dashboard becomes read-only. Patient can create a new inquiry immediately.
- After acceptance the patient cannot cancel the inquiry. The patient sees a "Contact support" action instead, and an admin performs any booking cancellation through FR-006 with a mandatory reason and audit. That cancellation moves the booking to `Cancelled` and the inquiry to `Cancelled`, releases any active slot hold immediately, and leaves the accepted subquote and its parent quote `accepted`; refunds and fees follow the refund rules in FR-006 (Payment & Billing Rules: the refund ladder set in FR-029, or the provider-fault terms where the provider is at fault). (REQ-003-012)

**A5: Appointment Slot Already Reserved**:

- Trigger: Patient confirms a subquote whose appointment slot is already held or blocked by another pending or confirmed booking, including a concurrent acceptance by another patient that acquires the active hold for the same provider, appointment date/time, and time zone a moment earlier.
- Steps: System rejects acceptance atomically because an active hold for that slot already exists, before creating an AcceptanceEvent, changing quote/inquiry states, or emitting a booking handoff. The confirmation modal shows the error state "This appointment slot was just taken. Please choose another subquote." and the patient returns to the inquiry dashboard to choose another eligible subquote. The subquote is not recorded as Accepted.
- Outcome: The existing slot reservation remains unchanged and no second accepted selection is created for that slot.

**A6: Provider Becomes Suspended or Deactivated**:

- Trigger: The owning provider's `Suspended` or `Deactivated` status becomes effective (FR-015 Alternative Flow A5 and Screen 4) before, during, or after subquote acceptance.
- Steps: From the effective time, Accept is blocked for every subquote of that provider and a confirmation already in flight is rejected before an AcceptanceEvent or hold is created. If the inquiry is still comparing providers, FR-004 cancels that provider's parent quotes once each; their subquotes become unavailable, while subquotes from other providers remain acceptable and the inquiry keeps its stage with `supportRequired = true` (FR-003 Workflow 2 Alternative Flow B4). If the accepted subquote belongs to that provider, the provider-fault transfer in Business Rule 1 applies: the booking closes with cause `ProviderSuspended` or `ProviderDeactivated` (FR-006 Alternative Flow B4, which routes to B5), any active hold is released, booking-confirming payment from the original provider is blocked, and an admin rehomes the patient to a replacement provider within the same inquiry through a new admin-authored acceptance record (Alternative Flow A9); the supersession record that links the original AcceptanceEvent to the replacement, with that cause, is written at the replacement acceptance. The inquiry is not cancelled, and the AcceptanceEvent, accepted IDs/versions, and acceptance snapshot are retained without rewriting.
- Outcome: Before acceptance, when Accept is blocked, the patient sees the inline error "This provider is no longer available. Please contact support." with a Contact Admin/Support action, not the A4 patient-cancellation messaging. After acceptance, when the deposit or booking-confirming payment is blocked because the provider became Suspended or Deactivated, the patient sees the inline error "This clinic can no longer perform your treatment. An admin will arrange a replacement clinic within the same inquiry."; the patient is not asked to start a new inquiry or re-enter anything. Both are on-screen errors shown in the app, not FR-020 notifications, and are localized through FR-021 like other UI text. The FR-020 patient notices for the same events (`provider.status_cancellation_patient` before acceptance, `booking.provider_fault_replacement` after acceptance; FR-015 and FR-003) are separate and unchanged. Late acceptance requests or payment callbacks cannot revive the original selection, and later reactivation does not restore it. (REQ-005-043, REQ-005-044)

**A7: Payment Window Expires After Acceptance**:

- Trigger: The fixed slot hold that started at acceptance ends before the first payment (deposit or first instalment) succeeds, and FR-006 moves the booking to `Payment Window Expired`.
- Steps: The slot hold is released and no appointment record exists. The accepted subquote is never reopened for acceptance, its sibling subquotes stay Not Selected, competing parent quotes stay cancelled, and the AcceptanceEvent and snapshot stay unchanged. The patient is shown a "Contact support" action with two recovery routes, both performed by an admin in FR-006: an audited admin revive, or an admin booking cancellation (booking and inquiry `Cancelled`, accepted quote stays `accepted`) after which the patient may start a new inquiry. The patient cannot cancel the inquiry directly after acceptance (Alternative Flow A4).
- Outcome: The inquiry keeps its single acceptance. A revive, when an admin grants it, is performed by FR-006 with a fresh slot-availability check and a new hold; FR-005 does not create a second acceptance. Missed later instalments never cause `Payment Window Expired`; they are governed by FR-007 and FR-007b.

**A8: Patient Applies a Promotion Code Before Acceptance**:

- Trigger: Before confirming acceptance, the patient enters a promotion code on Screen 2 for one named subquote.
- Steps: System validates the code for that subquote through FR-019. If valid, the discounted price is shown next to the provider's offered price and carried into the confirmation summary; if invalid, the patient sees the reason, the price is back to what the row carried when the quote was sent, including any promotion attached at send, and the patient may accept without the code or enter another. The offered price is the price the provider entered for the row before any promotion (REQ-004-035); a valid patient code replaces the promotion the row carries, including an automatic one (FR-019). The code applies only to the named subquote; opening another subquote does not carry it over. The applied code is recorded against the patient's selection only and is never written to the provider's quote or promotion records.
- Outcome: On acceptance, the discounted price and the applied promotion are frozen into the AcceptanceEvent snapshot. After acceptance the promotion and price cannot be removed, replaced, re-entered at checkout, or changed by revalidation (including an admin void); the only exception is the provider-fault transfer in Business Rule 1.

**A9: Admin-Authored Replacement Acceptance (Provider-Fault Transfer)**:

- Trigger: Before treatment starts (booking `Accepted` or `Confirmed`), the accepted provider withdraws, drops out, or has a suspension or deactivation take effect, and FR-006 closes the booking with the provider-fault cause (FR-006 Alternative Flows B4 and B5).
- Steps: The closure is recorded on the booking as its cancellation cause; no supersession record is written at closure. The admin authors a replacement quote for the replacement provider inside the same inquiry (FR-004 Screen 8). Through the FR-006 transfer, the admin then records a new AcceptanceEvent with `actorType = admin` that points to that replacement quote, one of its Quote Options, and one of its option/date-price rows, exactly like a patient acceptance. In the same operation the system writes one AcceptanceSupersession record that links the closed AcceptanceEvent to the new one; the record is inserted once and never updated. The new acceptance acquires the slot hold and creates the replacement booking through FR-006. The patient receives the mandatory `booking.scheduled` notice and the replacement provider receives `quote.accepted`.
- Replacement quote not accepted: If no replacement acceptance is recorded, the replacement quote expires under the normal FR-004 quote expiry and no AcceptanceEvent or AcceptanceSupersession record is written. The inquiry stays flagged `supportRequired` and is not cancelled automatically; the admin may author another replacement quote (FR-004 Screen 8) or cancel the inquiry and booking from the FR-006 admin screen. (REQ-005-045)
- Outcome: The inquiry keeps one active acceptance, the original accepted subquote takes the state Superseded (REQ-005-052), the original AcceptanceEvent and snapshot stay unchanged as history, and the patient re-enters nothing.
- Boundary: If the provider fault happens while the booking is `In Progress`, no replacement acceptance is created; the admin either moves the booking to Aftercare with an aftercare reassignment or cancels it in FR-006. If the provider fault happens in Aftercare, after treatment is done, no replacement acceptance is created. The admin reassigns only the aftercare provider or team in FR-006; the booking and treatment record stay, and no new payment is taken. (REQ-005-046)

---

## Screen Specifications

### Patient Platform

#### Screen 1: Inquiry Dashboard with Quote Comparison (Enhanced from FR-003 Screen 8)

**Purpose**: Patient views submitted inquiry status, browses parent quotes, compares complete subquotes, and accepts one subquote

**Note**: This screen extends FR-003's Inquiry Dashboard (Screen 8). Parent quotes remain grouped within the inquiry context, while their complete child subquotes are the comparison and acceptance items.

**Data Fields**:

**Inquiry-Level Fields** (always visible; one instance per screen):

| Field Name | Type | Required | Description | Validation Rules | Graph Fields |
|------------|------|----------|-------------|------------------|-------------|
| Current Stage | badge | Yes | Inquiry stage (Inquiry/Quoted/Accepted/Cancelled/...) | Valid lifecycle value; includes "Cancelled" per FR-003 | ENT-inquiry.stage |
| Timeline | timeline | Yes | Chronological status changes | Timestamps present | ENT-inquiry.status_timeline |
| Inquiry Summary | group | Yes | Read-only inquiry info | Complete and consistent | ENT-inquiry.problem_concern, ENT-inquiry.treatment_countries, ENT-inquiry-date-range.start_date, ENT-inquiry-date-range.end_date |
| Medical Alerts | chips | Yes | Patient medical risk level | Read-only; from FR-003 | ENT-risk-tag.severity |
| Deadlines | datetime | Yes | Response/expiry deadlines | Future or past allowed | ENT-inquiry.response_deadline, ENT-quote.expires_at |
| Next Actions | actions | Yes | Available user actions | Based on stage/permissions | no graph field (control) |

**Parent Quote Group Fields** (repeated for each parent quote):

| Field Name | Type | Required | Description | Validation Rules | Graph Fields |
|------------|------|----------|-------------|------------------|-------------|
| Provider | group | Yes | Provider identity and summary shown under patient privacy rules | Read-only; one provider per parent quote | ENT-provider.name, ENT-quote.provider_id |
| Parent Quote Reference | text | Yes | Stable reference for one provider response | Read-only; must not be presented as the selectable item | ENT-quote.id |
| Treatment and Shared Clinical Information | group | Yes | Treatment, graft information, visual plan, clinicians, notes, requirements, and attachments inherited by every child subquote | Read-only; sourced from the parent quote | ENT-quote.treatment_id, ENT-quote.estimated_grafts, ENT-quote.graft_description, ENT-quote.graft_visual_plan, ENT-quote.clinician_ids, ENT-quote.common_notes, ENT-quote.common_requirements, ENT-quote.attachment_ids |
| Provider Reviews | rating/number | No | Review rating and count | Read-only; sourced from FR-013 | ENT-provider-review-summary.average_rating, ENT-provider-review-summary.review_count |
| Provider Credentials Summary | text | Yes | Certifications and awards summary; the medical license number is never shown to the patient | Read-only; sourced from FR-015 | ENT-provider.awards |
| Expiry Timer | timer | Yes | Countdown for the parent quote; shows static "Expired on [date]" when expired | Applies to every child subquote (REQ-005-040) | ENT-quote.expires_at |
| Subquotes | list | Yes | All patient-visible subquotes contained by the parent quote | One or more; ordered; each rendered using the subquote fields below | no graph field (list of the per-subquote rows below) |
| Message Provider | button | Yes | Ask the provider about this quote response | Opens that provider's conversation in the dedicated FR-012 Messages/Inbox; does not embed chat in the quote screen (REQ-005-015) | no graph field (control) |

**Per-Subquote Fields** (repeated for every selectable subquote):

| Field Name | Type | Required | Description | Validation Rules | Graph Fields |
|------------|------|----------|-------------|------------------|-------------|
| Subquote Reference | text | Yes | Stable identifier and version for the atomic patient choice | Resolves one Quote Option ID and one Option/date-price ID under exactly one parent quote; `subquoteVersion` equals the owning parent aggregate `QuoteVersion` | ENT-subquote.id, ENT-subquote.parent_quote_id, ENT-subquote.quote_option_id, ENT-subquote.option_date_price_id, ENT-subquote.version |
| Package | group | Yes | Selected package snapshot for this subquote | Includes package name, description, and source/version provenance | ENT-subquote.package_snapshot |
| Included and Custom Services | checklist | Yes | Services included in this subquote | Read-only quote-owned snapshot | ENT-subquote.included_and_custom_services |
| Date Range | date range | Yes | Applicable patient-requested treatment range for this subquote | Exactly one range in the selectable subquote | ENT-subquote.date_range |
| Appointment Details | group | Yes | Provider-defined appointment date, time, and timezone | Must fall within the subquote date range | ENT-subquote.appointment_at, ENT-subquote.appointment_timezone |
| Price | amount | Yes | Offered price for this subquote as entered by the provider, before any promotion (FR-004), with the price after promotion shown next to it when a promotion applies | Uses the parent quote currency snapshot; no patient editing (REQ-005-050) | ENT-subquote.offered_price, ENT-subquote.price_after_promotion, ENT-quote.currency_snapshot |
| Promotion | group | No | Structured promotion attached to this subquote, with its discount shown separately from the offered price | Read-only; show terms when present (REQ-005-050) | ENT-subquote.promotion_snapshot |
| Price per Graft | number | Yes | Offered price of the subquote, before any promotion, divided by inherited graft count | Calculated; non-editable (REQ-005-051) | ENT-subquote.price_per_graft |
| Treatment Plan | ordered list | Yes | Relative day-to-day plan for this subquote | Inherits appointment as the schedule anchor; no stored calendar dates derived here | ENT-subquote.treatment_plan |
| State | badge | Yes | Available, Accepted, Not Selected, Expired, Withdrawn, Cancelled, or Superseded | Derived from parent/subquote lifecycle (REQ-005-052) | ENT-subquote.acceptance_state |
| Actions | buttons | Yes | View Details and Accept | Accept enabled only for a current eligible subquote (REQ-005-049) | no graph field (control) |

**Subquote List & Comparison Panel Fields** (list controls always visible; comparison panel renders only when at least two subquotes are selected):

| Field Name | Type | Required | Description | Validation Rules | Graph Fields |
|------------|------|----------|-------------|------------------|-------------|
| Parent Quotes Received | grouped list | Yes | Parent quote responses grouped under their providers | Includes multiple providers and multiple parent quotes from the same provider (REQ-005-001) | ENT-quote.id, ENT-quote.provider_id |
| Sort & Filter | controls | Yes | Sort/filter subquotes. The sort and filter options, the default sort, and the price-order currency handling are owned by FR-022 (`FR-005 / Screen 1`; REQ-005-053 and REQ-005-027 are retired in its favour). | Criteria evaluate the complete subquote plus inherited parent/provider values; see FR-022 (REQ-005-012) | no graph field (control) |
| Compare Selection | checkbox | No | Select subquotes to compare side-by-side | Maximum three eligible subquotes, regardless of parent quote/provider grouping (REQ-005-013) | no graph field (control) |
| Comparison View | panel | No | Side-by-side comparison of complete subquotes | Renders only when at least two are selected (REQ-005-047) | no graph field (control) |
| Comparison Differentiators | table | Conditional | Comparison rows across selected subquotes | Must include package, included/custom services, date range, appointment details, total price, currency, promotion, price per graft, inherited graft count, provider rating/count, provider credentials (certifications and awards only), and treatment plan (REQ-005-014) | ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services, ENT-subquote.date_range, ENT-subquote.appointment_at, ENT-subquote.appointment_timezone, ENT-subquote.offered_price, ENT-subquote.promotion_snapshot, ENT-subquote.treatment_plan, ENT-quote.currency_snapshot, ENT-quote.estimated_grafts, ENT-provider-review-summary.average_rating, ENT-provider-review-summary.review_count, ENT-provider.awards |

**Business Rules**:

- Parent quotes are grouping and inheritance boundaries; they are not patient-selectable acceptance items.
- Every Quote Option has at least one date range (REQ-004-018).
- The comparison panel always shows the current parent quote version. If the provider re-versions a parent quote, the panel refreshes to the current version; if a compared subquote no longer exists or becomes ineligible, it drops out of the panel and the patient is told why. (REQ-005-048)
- A terminal child subquote cannot be accepted: its Accept button is disabled and the reason is shown (REQ-005-004, REQ-005-049).
- Subquote state is Available, Accepted, Not Selected, Expired, Withdrawn, Cancelled, or Superseded, derived from the parent and subquote lifecycle; exactly one subquote across the inquiry is Accepted and not superseded. After an admin-authored replacement acceptance (REQ-005-024) the original accepted subquote is Superseded: read-only, never acceptable again, with its AcceptanceEvent and acceptance snapshot unchanged and closed by the supersession record. (REQ-005-052)
- Patient can view subquote details and accept an eligible subquote directly from the dashboard. (REQ-005-049)
- If inquiry stage is "Cancelled", all Accept buttons and Compare checkboxes are disabled; dashboard is read-only with "Cancelled" badge; quote data remains visible for reference (see FR-003 Workflow 5, Alternative Flow A4 above). (REQ-005-041)

#### Screen 2: Subquote Detail with Accept Action (Extension of FR-004 Screen 4)

**Purpose**: Patient views one complete subquote with inherited parent context and accepts that subquote

**Note**: This extends FR-004's Patient Platform Screen 4 (Quote Review) by adding the Accept button with terms acknowledgment and acceptance confirmation flow.

**Enhancements to FR-004 Screen 4**:

| Field Name | Type | Required | Description | Validation Rules | Graph Fields |
|------------|------|----------|-------------|------------------|-------------|
| Terms Acknowledgment | checkbox | Yes | Confirm understanding of policies | Required to proceed with a patient acceptance (REQ-005-035); an admin-authored replacement acceptance has none and leaves the field empty (REQ-005-024) | ENT-acceptance-event.terms_acknowledged_at |
| Selected Subquote Summary | group | Yes | Package, included/custom services, date range, appointment, price, promotion, and treatment plan | Must identify the exact current parent aggregate `QuoteVersion`, also recorded as `subquoteVersion` | ENT-subquote.id, ENT-subquote.version, ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services, ENT-subquote.date_range, ENT-subquote.appointment_at, ENT-subquote.appointment_timezone, ENT-subquote.offered_price, ENT-subquote.price_after_promotion, ENT-subquote.promotion_snapshot, ENT-subquote.treatment_plan, ENT-quote.currency_snapshot |
| Promotion Code | text input | No | Patient-entered promotion code for this named subquote | Validated through FR-019 before acceptance; applies to this subquote only; held only with the open subquote view until the patient confirms, then stored only on the AcceptanceEvent; discounted price shown when valid; not available after acceptance (REQ-005-026) | ENT-acceptance-event.promotion_code, ENT-acceptance-event.discounted_price |
| Inherited Parent Context | group | Yes | Provider, treatment, graft information, visual plan, clinicians, common notes/requirements, and attachments | Read-only; inherited from parent quote | ENT-provider.name, ENT-quote.treatment_id, ENT-quote.estimated_grafts, ENT-quote.graft_description, ENT-quote.graft_visual_plan, ENT-quote.clinician_ids, ENT-quote.common_notes, ENT-quote.common_requirements, ENT-quote.attachment_ids |
| Accept Button | button | Yes | Accept this subquote | Disabled when the subquote or parent quote is ineligible or another subquote is accepted; blocked with a message until the patient has accepted the current legal documents and an admin has set the acceptance terms text (REQ-005-066, REQ-005-067) | ENT-subquote.acceptance_state |
| Acceptance Confirmation Modal | modal | Yes | Summary confirmation before finalizing | Shows the complete subquote and inherited context | no graph field (control) |

**Business Rules**:

- All relevant parent quote and subquote details from FR-004 Screen 4 are displayed read-only. (REQ-005-054)
- Terms acknowledgment checkbox must be checked before Accept button is enabled. (REQ-005-035)
- Tapping Accept opens the confirmation modal with the complete subquote summary, inherited context, and next steps. (REQ-005-055)
- Detail reflects the latest provider edits. (REQ-005-054)

#### Screen 3: Acceptance Confirmation Modal

**Purpose**: Confirm acceptance and show next steps before finalizing

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph Fields |
|------------|------|----------|-------------|------------------|-------------|
| Subquote Summary | group | Yes | Exact package, services, date range, appointment details, pricing, promotion, treatment plan, provider, and inherited treatment facts | Must reflect the latest subquote and parent versions | ENT-subquote.id, ENT-subquote.version, ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services, ENT-subquote.date_range, ENT-subquote.appointment_at, ENT-subquote.appointment_timezone, ENT-subquote.offered_price, ENT-subquote.price_after_promotion, ENT-subquote.promotion_snapshot, ENT-subquote.treatment_plan, ENT-acceptance-event.discounted_price, ENT-quote.currency_snapshot, ENT-provider.name, ENT-quote.treatment_id, ENT-quote.estimated_grafts |
| Terms Acknowledgment | checkbox | Yes | Confirm understanding (if not already acknowledged) | Required if not already checked | ENT-acceptance-event.terms_acknowledged_at |
| Next Steps | note | Yes | Booking & Payment handoff information | Read-only | no graph field (control) |
| Confirm | action | Yes | Finalize acceptance | Enabled when eligible | no graph field (control) |
| Cancel | action | Yes | Return to quote detail | Always available | no graph field (control) |

**Business Rules**:

- Confirmation is idempotent; duplicate confirmations do nothing. Idempotent acceptance keyed to inquiry and accepted subquote: repeat requests do not create multiple accepted states. (REQ-005-056)
- Post-confirmation, modal closes and patient is directed to booking/payment entry. (REQ-005-057)

### Provider Platform (Read-only in this module)

#### Screen 4: Quote Outcome Notification

**Purpose**: Inform provider of acceptance outcome

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph Fields |
|------------|------|----------|-------------|------------------|-------------|
| Parent Quote Outcome | badge | Yes | Accepted, Expired, Withdrawn, Cancelled (other accepted), Cancelled (Inquiry Cancelled), or Cancelled (Provider Status) | Read-only parent lifecycle state | ENT-quote.status |
| Subquote Outcome | badge/list | Yes | Accepted, Not Selected, Expired, Withdrawn, Cancelled, or Superseded for each child choice | Exactly one Accepted, and not superseded, across the inquiry | ENT-subquote.acceptance_state |
| Selected Subquote | group | Conditional | Package, date range, appointment details, price, currency, and promotion accepted from this provider, read from the acceptance snapshot | Shown only to the selected provider; read-only (REQ-005-058) | ENT-acceptance-event.snapshot |
| Reason | text | No | If non-selected: "Other subquote accepted" or "Inquiry cancelled by patient"; if cancelled because the provider's account was suspended or deactivated: "Provider account suspended or deactivated" | Must not identify another provider or disclose accepted price (REQ-005-039) | ENT-quote.cancellation_provenance |
| Audit Link | link | Yes | View version/audit history | Read-only | ENT-quote-audit.action, ENT-quote-version.version |

### Admin Platform

#### Screen 5: Acceptance Oversight Dashboard

**Purpose**: Monitor acceptance events and manage exceptions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph Fields |
|------------|------|----------|-------------|------------------|-------------|
| Global Acceptance Table | table | Yes | All subquote acceptance events with parent quote/provider references and filters | Admin-only; status filter includes active, booking cancelled (derived from the FR-006 booking cancellation, with no supersession record), and superseded (provider fault, including provider suspension or deactivation, derived from linked supersession records) (REQ-005-059) | ENT-acceptance-event.id, ENT-acceptance-event.inquiry_id, ENT-acceptance-event.accepted_parent_quote_id, ENT-acceptance-event.accepted_subquote_id, ENT-acceptance-event.actor_type, ENT-acceptance-event.accepted_at, ENT-acceptance-event.oversight_status, ENT-quote.provider_id |
| Accepted Selection | group | Yes | Accepted subquote package, date range, appointment details, price, currency, exchange rate and its timestamp, promotion, and inherited context | Immutable acceptance snapshot | ENT-acceptance-event.snapshot |
| Supersession Indicator | badge | No | Shows if acceptance was superseded by a provider-fault transfer, or that its booking was cancelled | "Superseded — Provider Fault" links to the replacement admin-authored acceptance record; "Booking Cancelled" is read from the FR-006 booking cancellation and links to its audit trail; no supersession record exists for a cancellation (REQ-005-059) | ENT-acceptance-event.oversight_status, ENT-acceptance-supersession.cause, ENT-acceptance-supersession.replacement_acceptance_event_id, ENT-booking.status |
| Conflicts | badge | No | Flagged races or errors; the flag is set automatically by the system when a second acceptance is rejected (REQ-005-065) | Investigated by admin; the first valid acceptance stands; findings recorded as an annotation (REQ-005-033) | ENT-acceptance-event.conflict_flagged |
| Annotations | list | No | Admin notes and corrections recorded next to the acceptance | Append-only; each shows author, time, and reason | ENT-acceptance-annotation.author_id, ENT-acceptance-annotation.created_at, ENT-acceptance-annotation.reason, ENT-acceptance-annotation.text, ENT-acceptance-annotation.type |
| Actions | actions | Yes | Add note or correction with reason | Audited; appends an annotation and never alters the AcceptanceEvent, its snapshot, or any quote state; no delete or restore action exists (REQ-005-023) | ENT-acceptance-annotation.type, ENT-acceptance-annotation.text, ENT-acceptance-annotation.reason |

---

## Business Rules

### General Module Rules

1. Subsequent acceptance attempts are blocked with guidance, including after `Payment Window Expired` (Alternative Flow A7). The one exception is a provider-fault transfer handled in FR-006 (REQ-005-002, REQ-005-024; Alternative Flows A6 and A9). The supersession record carries the provider-fault cause (`ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated`), copied from the closed booking's cancellation cause. Money already paid is refunded to the patient in full, with no cancellation fee, and the replacement booking takes a new payment (FR-006 Alternative Flows B4 and B5); the exact payment mechanics are defined in the payment requirements (FR-007, FR-007b, FR-017).
2. Acceptance does not reveal patient full identity to provider; full PII becomes accessible only after successful payment confirmation, per constitution. The identity masking itself is the one platform-wide Rule in the system PRD (REQ-SYS-001; REQ-005-008 is retired in its favour).
3. All acceptance-related state transitions are immutably audited (who, when, what, reason). Audit logs must record the accepted subquote, inherited parent snapshot, actor, presented versions, and every affected parent quote and sibling subquote. (REQ-005-034)
4. See system PRD, Platform-Wide Rules: Soft deletes only (REQ-SYS-003; REQ-005-060 is retired in its favour). How long records are kept follows the single platform retention Rule (REQ-SYS-002; REQ-005-007). What may never be deleted, restored, or edited after acceptance is stated in REQ-005-023.
5. Notifications sent to non-selected providers (due to auto-cancellation) MUST NOT reveal the identity of the selected provider or the accepted price. The non-selected reason reads "Other subquote accepted" or "Inquiry cancelled by patient", and a provider whose parent quote is cancelled because the provider's account was suspended or deactivated sees "Provider account suspended or deactivated". (REQ-005-039)
6. Provider-status handling (Alternative Flow A6; FR-015 A5/Screen 4) uses cause `ProviderSuspended` or `ProviderDeactivated` with an independent `supportRequired` marker (REQ-005-022). It is distinct from patient inquiry cancellation (A4) and Payment Window Expired, and does not reclassify Completed or already-terminal history.
7. Patients do not have an explicit "decline" action; sibling subquotes become Not Selected and competing parent quotes auto-cancel on acceptance or expire by policy. (REQ-005-063)
8. A patient who has not accepted the current legal documents cannot confirm an acceptance; the FR-027 acceptance prompt is shown instead, and viewing and comparing quotes stay available (REQ-005-066, REQ-027-033).
9. Acceptance is blocked with a message, and can be retried, when the acceptance terms text has not been set by an admin (FR-026 A-09) or when the Settings API is unavailable as the slot hold is placed; no stale or guessed hold duration is used and nothing is recorded as accepted (REQ-005-067, REQ-026-118, REQ-026-144).

### Data & Privacy Rules

- See system PRD, Platform-Wide Rules: Encryption in transit and at rest (REQ-SYS-004; REQ-005-009 is retired in its favour); Role-based, audited access (REQ-SYS-009).

### Admin Editability Rules

**Editable by Admin**:

- Add a note or correction next to an acceptance record with reason (audited annotation; REQ-005-023). A flagged race or error is investigated and recorded the same way (REQ-005-033).
- Edit an accepted quote after acceptance in any field except price, currency, and promotion, with a mandatory reason and full before/after history; a change of the date range or appointment runs the FR-006 slot-availability check and emits `booking.rescheduled`, and a change of the treatment details emits `treatment.plan_changed` (REQ-005-023).
- Perform a provider-fault transfer through FR-006 (REQ-005-024; Business Rule 1, Alternative Flow A9).
- Cancel a booking after acceptance, from any booking state, through FR-006 with a mandatory reason and audit, when the patient contacts support (Alternative Flow A4).
- Configure notification behaviors via centralized settings (FR-030).

**Fixed in Codebase (Not Editable)**:

- Patient identity reveal policy: only post-payment confirmation (REQ-SYS-001).
- Subquote acceptance uniqueness constraint per inquiry (REQ-005-024).
- Soft delete policy (no hard deletes) (REQ-SYS-003).
- AcceptanceEvent immutability (REQ-005-023); admin notes are annotations only.

**Configurable with Restrictions**:

- Acceptance confirmation copy/UX notes (content-managed); legal text controlled centrally. (REQ-005-061)

### Payment & Billing Rules (for Handoff)

- The accepted subquote is the complete handoff unit. It carries the selected package, date range, appointment date/time/timezone, offered price, promotion when applicable, and references to the inherited parent quote/provider/treatment context. (REQ-005-011)
- Patient acceptance of the subquote constitutes acceptance of its exact appointment and price. FR-006 must not ask the patient to select another package, date range, appointment, or quote price. (REQ-005-062)
- Auto-applied promotion use: a sent parent quote carrying an auto-applied promotion holds at most one reserved use under FR-019; re-sending a new version keeps it, creates one only if the new version newly carries the promotion, and releases it if the new version no longer does (consumption and release at acceptance: REQ-005-028). If the booking reaches `Payment Window Expired` or is cancelled before the first payment, the consumed use returns to the limit; an admin revive takes it again only if the limit has room, as defined by FR-019. Provider-selected promotions and patient-entered codes keep the FR-019 lifecycle of reserve at acceptance and consume at first payment. Promotion usage limits count reservations plus consumed uses, so they cannot be exceeded.
- Binding snapshot fields: price, currency, date range, appointment, and promotion are read from the acceptance snapshot by every downstream module (REQ-005-006). An admin may later change the booking's appointment through FR-006 or through an admin edit of the accepted quote's date range or appointment (REQ-005-023), each of which emits `booking.rescheduled`. After acceptance, only the clinic or an admin may change the plan, clinicians, or grafts, through FR-010 or, for an admin, the admin edit of the accepted quote (REQ-005-023); each change is audited and the patient is notified.
- Cancellation During Hold: when an admin cancels the booking through FR-006 while the slot hold is active, the slot is returned to the provider's availability (Alternative Flow A4). See FR-026 for the slot-hold duration and FR-006 for the admin cancellation and booking-side guard rules.

---

## Dependencies

Related FRs: FR-003, FR-004, FR-006, FR-010, FR-012, FR-013, FR-015, FR-019, FR-020, FR-022, FR-026, FR-029, FR-030. System settings: A-09 (legal copy and terms acknowledgment text).

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

**Independent Test**: Patient cancels the inquiry in the Quoted stage and tries to cancel after accepting a subquote; verify the pre-acceptance cancellation cancels the draft, sent, and expired parent quotes and their subquotes and leaves quotes in any other status unchanged (REQ-003-013), locks the UI, and notifies the providers whose quotes were cancelled, and verify that after acceptance only "Contact support" is offered and the admin cancellation leaves the accepted quote `accepted`.

**Acceptance Scenarios**:

1. Given the patient has multiple parent quotes and subquotes in Quoted stage, When the patient cancels the inquiry, Then each parent quote in draft, sent, or expired status and its subquotes transition to "Cancelled (Inquiry Cancelled)" while a quote in any other status keeps its status and cause (REQ-003-013); Accept/Compare actions are disabled; dashboard shows "Cancelled" read-only
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

- Network loss during acceptance: system retries safely; no duplicate accept states. (REQ-005-056)
- Simultaneous accept attempts across devices: first valid acceptance wins; others see informative message. (REQ-005-002)
- Admin finds a quote or subquote was cancelled by mistake: no restore action exists; the admin records the finding as an audited annotation, prior acceptance is not overridden, and the patient uses the recovery routes in Alternative Flows A1 and A7. (REQ-005-064)
- Patient accepts a subquote then immediately wants to cancel: no patient cancel action exists after acceptance; the patient is offered "Contact support", and an admin cancellation through FR-006 moves the booking and inquiry to `Cancelled`, keeps the accepted subquote and parent quote `accepted`, writes no supersession record, and releases the slot hold. (REQ-005-042)
- Patient attempts to accept a subquote while inquiry cancellation is being processed: system checks inquiry status at confirmation; if cancelled, blocks acceptance with message "This inquiry has been cancelled." (REQ-005-036)
- Provider edits either the parent quote or selected subquote after the patient opens confirmation: system rejects the stale confirmation and requires review of the current version. (REQ-005-019)
- Patient cancels inquiry while on the acceptance confirmation modal (Screen 3): modal dismissed; inquiry dashboard refreshes to show "Cancelled" badge; all actions disabled. (REQ-005-041)
- Provider becomes `Suspended` or `Deactivated` while the patient is on the confirmation modal: confirmation is rejected at revalidation; the patient sees the inline error "This provider is no longer available. Please contact support." with a Contact Admin/Support action (Alternative Flow A6) and may choose another provider's eligible subquote if the inquiry is still comparing. (REQ-005-043)
- Provider-status cascade is replayed or a stale acceptance request arrives afterward: no duplicate cancellation, notification, AcceptanceEvent, or hold is created. (REQ-005-044)
- A promotion code that was valid when the patient entered it is no longer valid, or its usage limit is exhausted, when the patient confirms: the acceptance does not happen and nothing is recorded as accepted; the patient returns to the subquote detail with the reason shown and the price is back to what the row carried when the quote was sent, including any promotion attached at send, and may accept without the code or enter another. (REQ-005-026)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-005-001**: System MUST show every parent quote received for an inquiry, including multiple parent quotes from the same provider, and MUST expose each child subquote as a complete patient-selectable commercial choice.
- **REQ-005-002**: System MUST allow the patient to accept exactly one valid subquote per inquiry and MUST NOT allow direct acceptance of a parent quote or any upper-level inherited record.
- **REQ-005-003**: On acceptance, System MUST mark sibling subquotes in the accepted parent quote Not Selected and MUST auto-cancel all competing parent quotes for the same inquiry with reasons and notifications.
- **REQ-005-004**: System MUST block subquote acceptance when the subquote or its parent quote is expired, withdrawn, cancelled, archived, superseded, or stale, or when the owning provider is `Suspended` or `Deactivated` (FR-015), with clear messaging.
- **REQ-005-005**: System MUST prepare the booking/payment handoff from the accepted subquote without collecting funds in this module.

### Data Requirements

- **REQ-005-006**: System MUST preserve an immutable acceptance snapshot containing the accepted subquote identifier/version, the underlying Quote Option ID and Option/date-price ID, the source package ID/version, the parent quote identifier/version and expiry, provider and inquiry references, treatment ID/version, package and service snapshot, date range, appointment date/time/timezone, offered price, any patient-applied promotion code and the resulting discounted price, promotion, currency, exchange rate and its timestamp, treatment plan, estimated grafts, graft description, visual plan, clinician IDs, notes, requirements, attachment IDs with versions, actor, and timestamp; `acceptedSubquoteVersion` MUST equal `acceptedParentQuoteVersion` because both identify the same FR-004 aggregate revision; all resulting state changes MUST be audited. Price, currency, date range, appointment, and promotion are the binding fields that downstream modules MUST read from the snapshot; the snapshot appointment is the accepted baseline, and booking notices MUST read the booking's current appointment, which can change only through an FR-006 admin appointment change or an admin edit of the accepted quote's date range or appointment (REQ-005-023). The treatment details are the original record at acceptance; later changes to plan, clinicians, or grafts are made only through FR-010 or an admin edit of the accepted quote (REQ-005-023), with audit and patient notice, and never edit the snapshot.
- **REQ-005-007**: Retention of acceptance and related parent quote/subquote records follows the system PRD, Platform-Wide Rules: One 10-year retention period.

### Security & Privacy Requirements

- **REQ-005-008** (retired; owned by the system PRD): keeping patient identity masked to providers until payment confirmation is one platform-wide Rule in the system PRD, which FR-003, FR-004 and FR-005 cite instead of restating.  
- **REQ-005-009** (retired; owned by the system PRD): encryption at rest and in transit and role-based access for actions are Platform-Wide Rules in the system PRD (see system PRD, Platform-Wide Rules: Encryption in transit and at rest; Role-based, audited access).

### Integration Requirements

- **REQ-005-010**: System MUST integrate with FR-004 for parent quote, Quote Option, option/date-price, lifecycle, aggregate `QuoteVersion`, and audit contracts and with FR-020 for notifications.
- **REQ-005-011**: System MUST emit a booking handoff whose atomic commercial input is the accepted subquote and whose inherited context is resolved from its parent quote.
- **REQ-005-012**: System MUST allow patients to filter and sort subquotes using both subquote-owned and inherited comparison criteria.
- **REQ-005-013**: System MUST support side-by-side comparison of up to three subquotes, regardless of whether they belong to the same or different parent quotes/providers.
- **REQ-005-014**: System MUST display these subquote comparison differentiators: package, included/custom services, date range, appointment details, total price, currency, promotion, price per graft, treatment plan, inherited graft count, provider review rating/count, and provider credentials summary (certifications and awards only; never the medical license number). Estimated travel costs remain deferred pending an approved FR-008 source.
- **REQ-005-015**: A quote screen MAY link to the existing provider conversation. In-app messaging itself is defined in REQ-012-006 (FR-012 Messages/Inbox).
- **REQ-005-016**: System MUST deliver a patient's quote question to the provider as an FR-012 message, and the provider's notification of it MUST arrive within 5 minutes at the latest, unless the provider has switched that notice off or held it in their notification preferences (REQ-012-007).
- **REQ-005-017** (retired; owned by FR-029 REQ-029-044): the exchange rate lock at acceptance, including the rule for a cached rate older than 24 hours, is defined in REQ-029-044; the acceptance snapshot records the rate and its timestamp (REQ-005-006).
- **REQ-005-018**: A subquote MUST resolve exactly one FR-004 Quote Option and one applicable Option/date-price record into one complete package, date range, appointment, and offered-price selection. It MUST inherit shared provider, treatment, graft, visual-plan, clinician, note, requirement, attachment, currency, expiry, and audit context from exactly one parent quote. FR-005 owns the subquote identifier and state: the identifier is derived deterministically from the Quote Option ID and Option/date-price ID, so it stays the same across parent re-versions while both records exist. A parent quote offers up to (number of Quote Options × number of date ranges) subquotes, because a provider may leave out pairings it cannot offer.
- **REQ-005-019**: Acceptance confirmation MUST validate the current parent aggregate `QuoteVersion`, MUST require the derived `subquoteVersion` to equal it, and MUST reject stale selections before creating an AcceptanceEvent.
- **REQ-005-020**: Parent quote and subquote analytics MUST remain distinct: one provider response counts once at parent level (metric: Parent Quote Responses), while comparison and selection behavior is recorded at subquote level (metrics: Subquote Comparisons and Subquote Selections). Drafts, versions, edits, and resends MUST NOT add to the parent count. A parent quote counts once, on its first successful submission; several parent quotes count separately, one each. The parent count and the subquote counts are distinct grains: parents versus subquotes are never summed. Quote Option and subquote counts, when reported, MUST be labelled as such and never substituted into parent metrics.
- **REQ-005-021**: Acceptance MUST atomically acquire an exclusive hold on the selected appointment slot and MUST reject a second acceptance for a slot already held or blocked by another pending or confirmed booking, including a concurrent acceptance that finds an active hold already exists, before creating an AcceptanceEvent, changing quote/inquiry states, or emitting a booking handoff. The rejected patient MUST be told the slot was just taken.
- **REQ-005-022**: System MUST revalidate the owning provider's status at acceptance and MUST block acceptance of any subquote whose provider is `Suspended` or `Deactivated` from the effective time, including in-flight confirmations. For a still-comparing inquiry, System MUST keep other providers' subquotes acceptable. When the status takes effect after acceptance, System MUST release any active hold, retain the AcceptanceEvent and acceptance snapshot without rewriting, record cause `ProviderSuspended` or `ProviderDeactivated` with `supportRequired` on the FR-006 booking and the FR-003 ProviderInquiry (the supersession record is written only when the replacement acceptance is recorded), route the case to the FR-006 provider-fault transfer within the same inquiry, and tell the patient that an admin will arrange a replacement provider instead of showing the patient-cancellation message.
- **REQ-005-023**: System MUST NOT allow an AcceptanceEvent or its acceptance snapshot to be deleted, restored, or edited, and MUST NOT allow an accepted subquote or its parent quote to be deleted or restored. After acceptance an admin MAY edit the accepted quote in any field except its price, currency, and promotion (the date range and the treatment details may be changed), with a mandatory reason and a full before/after history. An edit of the date range or appointment MUST run the same slot-availability check as the FR-006 admin appointment change, update the booking's current appointment, and emit `booking.rescheduled`; an edit of the treatment details MUST notify the patient through `treatment.plan_changed`. The edit MUST be stored as a new version beside the acceptance snapshot, and the snapshot keeps the terms as accepted. Admins MAY also add audited notes or corrections as annotations next to an AcceptanceEvent; an annotation MUST NOT change the event, its snapshot, or any quote, subquote, or inquiry state.
- **REQ-005-024**: System MUST allow exactly one patient acceptance per inquiry. The only additional acceptance record is the admin-authored record created by an FR-006 provider-fault transfer before treatment starts; it MUST point to an admin-authored FR-004 replacement quote, Quote Option, and option/date-price row, and the original MUST be marked superseded by one supersession record inserted at the replacement acceptance rather than by editing it. The admin-authored record carries no patient terms acknowledgment, so its terms acknowledgment time stays empty; it records the admin as actor, and the supersession record written in the same operation carries the actor and the reason.
- **REQ-005-025** (retired; owned by FR-006 REQ-006-005): the one fixed slot hold that starts at acceptance (keyed by provider, appointment date/time, and time zone, for the FR-026 duration), the rule that payment failure never extends it, the creation of the appointment only on first payment, and the "Contact support" recovery route after `Payment Window Expired` are defined in REQ-006-005.
- **REQ-005-026**: System MUST let the patient apply a promotion code to one named subquote before acceptance, validated through FR-019, and MUST freeze the discounted price and promotion into the acceptance snapshot. The code MUST NOT be written to the provider's quote or promotion records, and the price and promotion MUST NOT change after acceptance except through an FR-006 provider-fault transfer. If the code is no longer valid, or its usage limit is exhausted, when the patient confirms, the acceptance MUST NOT happen and nothing is recorded as accepted; the patient MUST return to the subquote detail with the reason shown and the price is back to what the row carried when the quote was sent, including any promotion attached at send, and may accept without the code or enter another. The offered price is the price the provider entered for the row before any promotion (REQ-004-035).
- **REQ-005-027** (retired; owned by FR-022): price sorting across currencies on the quote list (display-currency conversion for ordering only, each subquote shown in its own currency, approximate label for mixed currencies) is defined in FR-022 (REQ-022-058, REQ-022-069).
- **REQ-005-028**: On acceptance, System MUST consume the auto-applied promotion use reserved at send for the accepted parent quote and MUST release the reservations of every parent quote that ends Not Selected or auto-cancelled, as defined by FR-019. When the accepted subquote does not carry the automatic promotion reserved for its parent quote, System MUST release that reservation with reason `not_applied`.
- **REQ-005-029**: At acceptance, System MUST notify the patient and the providers of the outcome, and the patient notice MUST also fire on an admin-authored replacement acceptance. Recipients, content, and whether a notice can be switched off are set by the notification Rule REQ-020-019 (FR-020).
- **REQ-005-030** (retired; owned by FR-003 REQ-003-012): after acceptance the patient is not offered an inquiry cancel action and sees "Contact support" instead; booking cancellation from acceptance onward is performed only by an admin through FR-006.
- **REQ-005-065**: System MUST set the Conflicts flag on an acceptance automatically when a second acceptance is rejected; an admin does not set it. The flagged acceptance is then investigated by an admin (Screen 5).
- **REQ-005-066**: System MUST block the patient's confirmation of an acceptance until the patient has accepted the current legal documents, showing the FR-027 acceptance prompt; viewing and comparing quotes stay available (REQ-027-033).
- **REQ-005-067**: System MUST block acceptance with a message, and let the patient retry, when the acceptance terms text (FR-026 A-09) has not been set, or when the Settings API is unavailable as the slot hold is placed; no stale or guessed hold duration is used and no AcceptanceEvent is created (REQ-026-118, REQ-026-144).

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-20 | 3.0 | Requirements graph programme baseline: owner rulings applied and the PRD compressed to the checklist structure. Earlier history (v1.0 to v2.9) and the change requests CR-FR005-20260915-01 and CR-FR005-20261016-01 are in `archived/prd-baseline-2026-11-08/fr005-quote-comparison-acceptance/`. | Product Owner / Documentation |
| 2026-11-22 | 3.1 | Owner answer of 2026-11-22 (requirements graph programme, Phase 4 re-check): the patient sees the provider's certifications and awards only, never the medical license number. Screen 1 Provider Credentials Summary, Comparison Differentiators and REQ-005-014 reworded. | Product Owner / Documentation |
| 2026-11-22 | 3.2 | Audit follow-up to the owner answers of 2026-11-22: the FR-015 dependency line no longer mentions licenses. | Product Owner / Documentation |
| 2026-11-22 | 3.3 | Owner ruling 2026-11-22 and the earlier provider-fault ruling: on a provider-fault or provider-status replacement the patient is refunded in full and the replacement booking takes a new payment; the credit wording is removed (Business Rule 1). | Product Owner / Documentation |
| 2026-11-22 | 3.4 | Wording clean-up after the cross-FR consistency review: the stale 'payment placeholder' pointer is replaced by a pointer to the refund rules FR-006 already states (the refund ladder set in FR-029, or the provider-fault terms where the provider is at fault). No rule changes. | Product Owner / Documentation |
| 2026-11-22 | 3.5 | Compressed PRD applied (requirements graph programme, Phase 9; draft read and approved by the owner on 2026-11-22): each rule stated once with REQ id citations, field rows tagged with graph field ids, Success Criteria, Assumptions, Implementation Notes and Key Entities removed, Dependencies reduced to one list. No rule changes. The uncompressed text is in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 3.6 | FR-005 r1 logic review fixes (F4, N3, N4, N8): the Screen 1 credentials rows are tagged `ENT-provider.awards`, which holds certifications and awards; REQ-005-037 writes the accepted subquote's price after any promotion as the accepted total and the price per graft row uses the offered price before promotion (REQ-005-051); REQ-005-026 and the edge cases gain the failure path for a code that is no longer valid or is exhausted at confirmation; owner ruling 2026-11-23: the admin edit of the accepted quote is kept and is named as an exception in REQ-005-006, REQ-005-023 and the Admin Editability and Payment & Billing lines (a date or appointment change runs the FR-006 slot-availability check and emits `booking.rescheduled`, a treatment-detail change emits `treatment.plan_changed`, the snapshot never changes). | Product Owner / Documentation |
| 2026-11-23 | 3.7 | FR-005 logic review round 2 fixes: REQ-005-024 and the Screen 2 Terms Acknowledgment row state that an admin-authored replacement acceptance has no terms acknowledgment and records the admin actor and reason; the inquiry cancellation cascade (Alternative Flow A4 and User Story 3) cancels only draft, sent, and expired parent quotes (REQ-003-013); the original accepted subquote takes the state Superseded after a replacement acceptance (REQ-005-052, Screens 1 and 4, Alternative Flow A9); Screen 4 gains the outcome Cancelled (Provider Status) and its reason text (REQ-005-039); REQ-005-016 says the question is an FR-012 message with the provider notice within 5 minutes at the latest. | Product Owner / Documentation |
| 2026-11-25 | 3.8 | Cross-FR alignment. The 5-minute notice promise excludes notices the provider has switched off or held in notification preferences (REQ-005-016). The offered price is the price the provider entered for the row before any promotion; after a failed code the price returns to what the row carried when the quote was sent, and a valid patient code replaces the promotion the row carries (REQ-005-026). The patient code is held only with the open subquote view until confirmation. Acceptance is blocked until the legal documents are accepted, with viewing and comparing kept (REQ-005-066), and is blocked and retryable when the acceptance terms text is unset or the Settings API is unavailable at hold placement (REQ-005-067). | Claude (AI Assistant) |
| 2026-11-25 | 3.9 | Backlog points settled: two Screen 1 citations corrected (every Quote Option has at least one date range is REQ-004-018; a terminal subquote cannot be accepted is REQ-005-004 and REQ-005-049); the other FR-005 backlog points were already settled by the live PRD and graph. No rule changes. | Claude (AI Assistant) |

---

## Appendix: Approvals

Approved by the Product Owner as part of the requirements baseline of 2026-11-25. Record: `project-requirements/baseline-sign-off.md`. Changes after that date are listed in the Change Log above.

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-005 from system-prd.md
**Last Updated**: 2026-11-25
