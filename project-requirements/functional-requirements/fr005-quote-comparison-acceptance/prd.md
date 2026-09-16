# FR-005 - Quote Comparison & Acceptance

**Module**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight  
**Feature Branch**: `fr005-quote-comparison-acceptance`  
**Created**: 2025-11-03  
**Status**: 🟡 Revised — Pending Consolidated Verification
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

- Read-only visibility of the accepted or non-selected outcome for parent quotes and subquotes.
- Competing parent quotes auto-cancelled with reason “Other subquote accepted”; sibling subquotes in the accepted parent quote become “Not Selected”.
- No patient PII is revealed by acceptance; full details remain locked until payment confirmation per constitution.

**Admin Platform (A-01)**:

- Global oversight of quote states and acceptance events across patients/providers.  
- Soft-delete/restore capabilities with audit trail.  
- Conflict resolution (rare): e.g., simultaneous accept attempts; manual remediation with rationale.

**Shared Services (S-03, S-06)**:

- Notifications for subquote acceptance, parent quote expiry, sibling outcomes, and auto-cancellation of competing parent quotes.
- Audit logging service for all state transitions.  
- Retention/archival utilities (soft delete only; no hard deletes).

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
4. Patient opens one subquote and taps "Accept".
5. Patient confirms the exact subquote with terms acknowledgment and a complete selection summary.
6. System atomically revalidates the inquiry, parent quote, and subquote; confirms that no prior subquote has been accepted for the inquiry; verifies that the presented parent aggregate `QuoteVersion` is current; and acquires the appointment slot's exclusive payment-window hold. The derived `subquoteVersion` MUST equal that same version. If another pending or confirmed booking already holds or blocks the same slot, acceptance is rejected before an AcceptanceEvent or booking handoff is created.
7. After the exclusive hold succeeds, System records the selected subquote as Accepted, locks its inherited parent context and commercial details, sets the parent quote and inquiry to Accepted, and records the acceptance snapshot and reserved slot reference.
8. System marks every sibling subquote in the accepted parent quote as Not Selected and auto-cancels every competing parent quote for the inquiry with reason "Other subquote accepted."
9. System sends notifications to the patient and all affected providers without disclosing the selected provider or accepted price to non-selected providers.
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

**A4: Patient Cancels Inquiry During Quote Review**:

- Trigger: Patient cancels the parent inquiry (FR-003 Workflow 5) while quotes are available for review or one is already accepted.
- Steps: System cancels inquiry; all parent quotes and their subquotes become ineligible with status "Cancelled (Inquiry Cancelled)"; all Accept/Compare actions are disabled; dashboard shows "Cancelled" badge. If an accepted subquote has an active appointment hold, the hold is released immediately (see FR-006; configurable duration, default 48 hours).
- Outcome: Inquiry dashboard becomes read-only. Patient can create a new inquiry immediately.

**A5: Appointment Slot Already Reserved**:

- Trigger: Patient confirms a subquote whose appointment slot is already held or blocked by another pending or confirmed booking.
- Steps: System rejects acceptance atomically before creating an AcceptanceEvent, changing quote/inquiry states, or emitting a booking handoff; the patient is told that the appointment is no longer available and may choose another eligible subquote.
- Outcome: The existing slot reservation remains unchanged and no second accepted selection is created for that slot.

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
| Price | amount | Yes | Complete offered price for this subquote | Uses the parent quote currency snapshot; no patient editing |
| Promotion | group | No | Structured promotion included in the offered price | Read-only; show terms when present |
| Price per Graft | number | Yes | Subquote price divided by inherited graft count | Calculated; non-editable |
| Treatment Plan | ordered list | Yes | Relative day-to-day plan for this subquote | Inherits appointment as the schedule anchor; no stored calendar dates derived here |
| State | badge | Yes | Available, Accepted, Not Selected, Expired, Withdrawn, or Cancelled | Derived from parent/subquote lifecycle |
| Actions | buttons | Yes | View Details and Accept | Accept enabled only for a current eligible subquote |

**Subquote List & Comparison Panel Fields** (list controls always visible; comparison panel renders only when at least two subquotes are selected):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Parent Quotes Received | grouped list | Yes | Parent quote responses grouped under their providers | Includes multiple providers and multiple parent quotes from the same provider |
| Sort & Filter | controls | Yes | Sort/filter subquotes. Sort options: Price (Low–High), Price (High–Low), Graft Count, Rating, Appointment Date, Quote Date. Filter: by patient-submitted date range. Default sort: Quote Date (most recent). | Criteria evaluate the complete subquote plus inherited parent/provider values; see FR-022 / `FR-005 / Screen 1` |
| Compare Selection | checkbox | No | Select subquotes to compare side-by-side | Maximum three eligible subquotes, regardless of parent quote/provider grouping |
| Comparison View | panel | No | Side-by-side comparison of complete subquotes | Renders only when at least two are selected |
| Comparison Differentiators | table | Conditional | Comparison rows across selected subquotes | Must include package, included/custom services, date range, appointment details, total price, price per graft, inherited graft count, provider rating/count, provider credentials, and treatment plan |

**Business Rules**:

- Parent quotes are grouping and inheritance boundaries; they are not patient-selectable acceptance items.
- A subquote is the lowest-level complete commercial choice and the only selectable acceptance item.
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
| Inherited Parent Context | group | Yes | Provider, treatment, graft information, visual plan, clinicians, common notes/requirements, and attachments | Read-only; inherited from parent quote |
| Accept Button | button | Yes | Accept this subquote | Disabled when the subquote or parent quote is ineligible or another subquote is accepted |
| Acceptance Confirmation Modal | modal | Yes | Summary confirmation before finalizing | Shows the complete subquote and inherited context |

**Business Rules**:

- All relevant parent quote and subquote details from FR-004 Screen 4 are displayed read-only.
- Terms acknowledgment checkbox must be checked before Accept button is enabled.  
- Accept button is disabled if the subquote or parent quote is expired, withdrawn, cancelled, superseded, or stale, or another subquote is already accepted.
- Tapping Accept opens the confirmation modal with the complete subquote summary, inherited context, and next steps.
- Detail reflects the latest provider edits; confirmation rejects a stale version; the accepted subquote and inherited context lock on acceptance.

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
| Selected Subquote | group | Conditional | Package, date range, appointment details, and price accepted from this provider | Shown only to the selected provider; read-only |
| Reason | text | No | If non-selected: "Other subquote accepted" or "Inquiry cancelled by patient" | Must not identify another provider or disclose accepted price |
| Audit Link | link | Yes | View version/audit history | Read-only |

### Admin Platform

#### Screen 5: Acceptance Oversight Dashboard

**Purpose**: Monitor acceptance events and manage exceptions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Global Acceptance Table | table | Yes | All subquote acceptance events with parent quote/provider references and filters | Admin-only; status filter includes active and superseded_by_cancellation |
| Accepted Selection | group | Yes | Accepted subquote package, date range, appointment details, price, and inherited context | Immutable acceptance snapshot |
| Cancellation Indicator | badge | No | Shows if acceptance was superseded by inquiry cancellation | "Superseded — Inquiry Cancelled" badge; links to FR-003 cancellation audit trail |
| Conflicts | badge | No | Flagged races or errors | Investigated by admin |
| Actions | actions | Yes | Soft delete/restore with reason | Audit enforced |

---

## Business Rules

### General Module Rules

1. A patient can accept exactly one subquote per inquiry; a parent quote cannot be accepted directly. Subsequent acceptance attempts are blocked with guidance.
2. A valid subquote acceptance atomically acquires an exclusive hold on its appointment slot, locks that subquote and its inherited parent context, marks its sibling subquotes Not Selected, and auto-cancels every competing parent quote for the same inquiry with clear reasons and notifications. If the slot is already held or blocked, the acceptance attempt fails before any of those state changes.
3. Acceptance does not reveal patient full identity to provider; full PII becomes accessible only after successful payment confirmation, per constitution.  
4. All acceptance-related state transitions are immutably audited (who, when, what, reason).  
5. A subquote is ineligible if it or its parent quote is expired, withdrawn, cancelled, archived, superseded, or no longer the version presented to the patient.
6. All deletes are soft deletes; no hard deletes permitted.
7. Notifications sent to non-selected providers (due to auto-cancellation) MUST NOT reveal the identity of the selected provider or the accepted price.

### Data & Privacy Rules

1. Patient identifiers remain anonymized to providers at this stage.  
2. All data in transit and at rest is protected according to platform policies.  
3. Audit logs must record the accepted subquote, inherited parent snapshot, actor, presented versions, and every affected parent quote and sibling subquote.
4. Retention: acceptance and related quote/subquote records retained ≥ 7 years.

### Admin Editability Rules

**Editable by Admin**:

- Resolve rare conflicts (e.g., simultaneous accept attempts) with reason.  
- Soft delete/restore acceptance, parent quote, or subquote records with justification (audited).
- Configure notification behaviors via centralized settings (separate FR).

**Fixed in Codebase (Not Editable)**:

- Patient identity reveal policy: only post-payment confirmation.  
- Subquote acceptance uniqueness constraint per inquiry.
- Soft delete policy (no hard deletes).

**Configurable with Restrictions**:

- Acceptance confirmation copy/UX notes (content-managed); legal text controlled centrally.

### Payment & Billing Rules (for Handoff)

- Acceptance prepares booking/payment handoff; no funds are collected in this module.  
- The accepted subquote is the complete handoff unit. It carries the selected package, date range, appointment date/time/timezone, offered price, promotion when applicable, and references to the inherited parent quote/provider/treatment context.
- Patient acceptance of the subquote constitutes acceptance of its exact appointment and price. FR-006 must not ask the patient to select another package, date range, appointment, or quote price.
- On acceptance, the system MUST ensure the quote exchange rate is locked at the time of acceptance per FR-004 / System PRD pricing rules.  
- Pricing and promotions shown are those attached to the subquote; acceptance does not modify financial terms.
- Post-Acceptance Hold: Acceptance and exclusive slot reservation are one atomic operation. After acceptance, the system holds the pre-selected appointment slot for the FR-006 configurable duration, default 48 hours, to allow the patient to complete the initial payment (deposit or first installment). A second acceptance targeting the held or blocked slot is rejected. If payment is not completed within the configured hold period, the reservation is released and the slot may be reallocated by the provider.
- Inquiry Cancellation During Hold: If the patient cancels the inquiry (FR-003 Workflow 5) while the appointment slot hold is active, the hold is released immediately and the slot is returned to the provider's availability. The accepted subquote and its parent quote transition to "Cancelled (Inquiry Cancelled)". See FR-006 for hold configuration and booking-side guard rules.

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
- **FR-015 / A-02**: Provider Management & Onboarding (source for provider credentials/licenses/certifications summary).  
- **FR-006 / P-03, PR-02, A-01**: Booking & Scheduling consumes the FR-005 `AcceptanceEvent`, accepted parent quote ID/version, accepted subquote ID/version, immutable acceptance snapshot, and pre-scheduled slot without package, date, appointment, or price reselection; it owns payment initiation, booking confirmation, and post-payment PII reveal.
- **A-09**: System settings (legal copy, terms acknowledgment text, and the FR-006 payment-failure slot-hold duration whose default is 48 hours).

### External Dependencies

- None specific beyond shared notification services and standard platform integrations.

### Data Dependencies

- Inquiry (from FR-003), parent quotes and complete subquotes (from FR-004), Notification endpoints (FR-020), and legal/policy plus slot-hold configuration (A-09 through FR-006).

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

Patient cancels the inquiry while subquotes are available for review or after accepting a subquote.

**Independent Test**: Patient cancels the inquiry at multiple points in the subquote review/acceptance lifecycle; verify all parent quotes and subquotes are cancelled, UI is locked, providers are notified, and admin oversight is updated.

**Acceptance Scenarios**:

1. Given the patient has multiple parent quotes and subquotes in Quoted stage, When the patient cancels the inquiry, Then all parent quotes and subquotes transition to "Cancelled (Inquiry Cancelled)"; Accept/Compare actions are disabled; dashboard shows "Cancelled" read-only
2. Given the patient cancels after accepting a subquote with an active appointment slot hold, When cancellation processes, Then the accepted subquote and parent quote become "Cancelled (Inquiry Cancelled)"; AcceptanceEvent is marked superseded; slot hold is released immediately regardless of its configured duration
3. Given provider views their quote outcome after patient cancels inquiry, When opening Screen 4, Then Outcome badge shows "Cancelled (Inquiry Cancelled)" with reason "Inquiry cancelled by patient"
4. Given admin views acceptance oversight after patient cancels inquiry post-acceptance, When filtering, Then superseded acceptance event is visible with "Superseded — Inquiry Cancelled" badge and linked to cancellation audit trail

### Edge Cases

- Network loss during acceptance: system retries safely; no duplicate accept states.  
- Simultaneous accept attempts across devices: first valid acceptance wins; others see informative message.  
- Provider withdraws the parent quote during confirmation: subquote acceptance is blocked with explanation; return to inquiry dashboard.
- Admin restores mistakenly cancelled quote (with reason): does not override prior acceptance; remains read-only history.
- Patient accepts a subquote then immediately cancels the inquiry: system processes cancellation; AcceptanceEvent is superseded; accepted subquote and parent quote become "Cancelled (Inquiry Cancelled)"; slot hold is released; booking handoff is aborted.
- Patient attempts to accept a subquote while inquiry cancellation is being processed: system checks inquiry status at confirmation; if cancelled, blocks acceptance with message "This inquiry has been cancelled."
- Provider edits either the parent quote or selected subquote after the patient opens confirmation: system rejects the stale confirmation and requires review of the current version.
- Patient cancels inquiry while on the acceptance confirmation modal (Screen 3): modal dismissed; inquiry dashboard refreshes to show "Cancelled" badge; all actions disabled.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-005-001**: System MUST show every parent quote received for an inquiry, including multiple parent quotes from the same provider, and MUST expose each child subquote as a complete patient-selectable commercial choice.
- **REQ-005-002**: System MUST allow the patient to accept exactly one valid subquote per inquiry and MUST NOT allow direct acceptance of a parent quote or any upper-level inherited record.
- **REQ-005-003**: On acceptance, System MUST mark sibling subquotes in the accepted parent quote Not Selected and MUST auto-cancel all competing parent quotes for the same inquiry with reasons and notifications.
- **REQ-005-004**: System MUST block subquote acceptance when the subquote or its parent quote is expired, withdrawn, cancelled, archived, superseded, or stale, with clear messaging.
- **REQ-005-005**: System MUST prepare the booking/payment handoff from the accepted subquote without collecting funds in this module.

### Data Requirements

- **REQ-005-006**: System MUST preserve an immutable acceptance snapshot containing the accepted subquote identifier/version, parent quote identifier/version, provider and inquiry references, package and service snapshot, date range, appointment date/time/timezone, offered price, promotion, currency/exchange-rate snapshots, treatment plan, inherited clinical references, actor, and timestamp; `acceptedSubquoteVersion` MUST equal `acceptedParentQuoteVersion` because both identify the same FR-004 aggregate revision; all resulting state changes MUST be audited.
- **REQ-005-007**: System MUST retain acceptance and related parent quote/subquote records for ≥ 7 years.

### Security & Privacy Requirements

- **REQ-005-008**: System MUST keep patient identity masked to providers until payment confirmation.  
- **REQ-005-009**: System MUST encrypt data at rest and in transit and enforce RBAC for actions.

### Integration Requirements

- **REQ-005-010**: System MUST integrate with FR-004 for parent quote, Quote Option, option/date-price, lifecycle, aggregate `QuoteVersion`, and audit contracts and with FR-020 for notifications.
- **REQ-005-011**: System MUST emit a booking handoff whose atomic commercial input is the accepted subquote and whose inherited context is resolved from its parent quote.
- **REQ-005-012**: System MUST allow patients to filter and sort subquotes using both subquote-owned and inherited comparison criteria.
- **REQ-005-013**: System MUST support side-by-side comparison of up to three subquotes, regardless of whether they belong to the same or different parent quotes/providers.
- **REQ-005-014**: System MUST display these subquote comparison differentiators: package, included/custom services, date range, appointment details, total price, price per graft, treatment plan, inherited graft count, provider review rating/count, and provider credentials summary. Estimated travel costs remain deferred pending an approved FR-008 source.
- **REQ-005-015**: Patients MUST be able to ask providers questions about quotes through the dedicated FR-012 Messages/Inbox; quote screens MAY navigate to the existing provider conversation but MUST NOT embed a chat surface.
- **REQ-005-016**: System MUST notify the provider of patient quote questions within 5 minutes.
- **REQ-005-017**: System MUST lock quote exchange rate at time of patient acceptance (per FR-004 pricing rules).
- **REQ-005-018**: A subquote MUST resolve exactly one FR-004 Quote Option and one applicable Option/date-price record into one complete package, date range, appointment, and offered-price selection. It MUST inherit shared provider, treatment, graft, visual-plan, clinician, note, requirement, attachment, currency, expiry, and audit context from exactly one parent quote.
- **REQ-005-019**: Acceptance confirmation MUST validate the current parent aggregate `QuoteVersion`, MUST require the derived `subquoteVersion` to equal it, and MUST reject stale selections before creating an AcceptanceEvent.
- **REQ-005-020**: Parent quote and subquote analytics MUST remain distinct: one provider response counts once at parent level, while comparison and selection behavior is recorded at subquote level.
- **REQ-005-021**: Acceptance MUST atomically acquire an exclusive hold on the selected appointment slot and MUST reject a second acceptance for a slot already held or blocked by another pending or confirmed booking before creating an AcceptanceEvent, changing quote/inquiry states, or emitting a booking handoff.

---

## Key Entities

- **Subquote**: id, parentQuoteId, quoteOptionId, optionDatePriceId, version, packageSnapshot, includedAndCustomServices, dateRange, appointmentAt, appointmentTimezone, offeredPrice, promotionSnapshot, treatmentPlan, state
  - Atomic unit displayed, compared, and accepted by the patient.
  - Resolves one FR-004 Quote Option and one applicable Option/date-price record; neither underlying record is accepted independently in FR-005.
  - `version` is the owning parent quote's aggregate `QuoteVersion`; a subquote has no independent revision counter.
  - Inherits provider and shared treatment/clinical context from exactly one parent Quote.
- **AcceptanceEvent**: inquiryId, acceptedParentQuoteId, acceptedParentQuoteVersion, acceptedSubquoteId, acceptedSubquoteVersion, reservedSlotId, actorId (patient), acceptedAt, acceptanceSnapshot, handoffMetadata, supersededByCancellation
  - `acceptedSubquoteVersion` MUST equal `acceptedParentQuoteVersion`.
  - `acceptanceSnapshot` preserves the complete subquote plus inherited parent context at acceptance.
  - If the patient cancels after acceptance, the event is retained and marked superseded; the accepted subquote and parent Quote transition to "Cancelled (Inquiry Cancelled)".
  - Relationships: belongsTo Inquiry; belongsTo accepted parent Quote; belongsTo accepted Subquote.
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
| 2026-04-12 | 1.5 | Screen 1 Sort & Filter: replaced "Criteria list must be defined" placeholder with defined sort/filter options; added cross-reference to FR-022 as authoritative source. | AI |
| 2026-02-11 | 1.5 | Clarified Alternative Flow A1 outcome: removed ambiguous "await new quotes" phrasing; explicitly stated patient options are to pick another non-expired quote, cancel inquiry and start new, or contact support. No re-quoting mechanism exists for the same inquiry. Restructured Screen 1 Data Fields into 3 grouped sub-tables (Inquiry-Level Fields, Per-Quote Card Fields, Quote List & Comparison Panel Fields) with explicit Comparison Differentiators field per REQ-005-014. Updated comparison criteria business rule to reference the new table structure. Added "Expired on [date]" display to Expiry Timer for expired state. Added "disabled for expired/withdrawn quotes" to Compare Selection. Renamed "Ask Question" button to "Contact Support" with routing to Hairline Support via FR-012 secure messaging. | AI |
| 2026-09-15 | 2.0 | Replaced parent-quote acceptance with atomic subquote comparison and acceptance. A subquote now represents one complete package/date-range/appointment/price choice and inherits upper-level provider and clinical context. Added grouped parent quote presentation, subquote comparison/detail fields, version-safe acceptance snapshot, sibling Not Selected handling, competing parent quote cancellation, complete FR-006 handoff, distinct parent/subquote analytics, REQ-005-018 through REQ-005-020, and CR-FR005-20260915-01. Status reset pending consolidated verification. | Product Owner / Documentation |
| 2026-09-16 | 2.1 | Resolved post-verification contract findings: bound `subquoteVersion` and `acceptedSubquoteVersion` to the owning parent aggregate `QuoteVersion`, and replaced the generic Upcoming FR dependency with the explicit FR-006 accepted-subquote handoff contract. Verification status remains pending consolidated review. | Product Owner / Verification alignment |
| 2026-09-16 | 2.2 | Aligned quote questions with FR-012 Patient ↔ Provider messaging through the dedicated Messages/Inbox, and aligned the post-acceptance slot hold with FR-006/A-09 as configurable with a 48-hour default. Consolidated verification remains pending. | Product Owner / Verification alignment |
| 2026-09-16 | 2.3 | Resolved the acceptance-slot concurrency contract: subquote acceptance now atomically acquires an exclusive appointment hold and rejects a second acceptance before creating an AcceptanceEvent or booking handoff. Consolidated verification remains pending. | Product Owner / Verification resolution |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Product Owner | 2026-09-16 | Approved through v2.3, including atomic exclusive slot reservation at acceptance; consolidated verification pending |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |
