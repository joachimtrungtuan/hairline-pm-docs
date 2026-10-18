# Change Request: MTG-002 Quote Model Alignment for Inquiry Submission and Distribution

**Change Request ID**: CR-FR003-20261016-01
**Primary FR**: FR-003
**Triggering FR / Event**: SRC-MTG-002 quote model verification and Product Owner decision log (2026-10-16); cross-FR check against FR-006 and FR-015
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.8 to v2.11 (v2.9 on 2026-10-16; v2.10 consolidated verification corrections on 2026-10-18; v2.11 final audit corrections on 2026-10-18)
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner decided that a provider suspended or deactivated after acceptance follows the FR-006 provider-fault transfer: the booking is closed and an admin rehomes the patient to a replacement provider in the same inquiry. FR-003 still cancelled the whole inquiry in that case, which would leave no inquiry to rehome into. FR-003 now keeps the inquiry open.

## Baseline State

**Source version**: FR-003 v2.8, Workflow 2 Alternative Flow B4, business rules on provider status, REQ-003-020

When a provider became `Suspended` or `Deactivated`, an inquiry whose accepted treatment belonged to that provider (stage Accepted, Confirmed, In Progress, or Aftercare) moved to `Cancelled` with cause `ProviderSuspended` or `ProviderDeactivated` and `supportRequired = true`.

## Approved State

- The inquiry is not cancelled. It keeps its current stage and is flagged `supportRequired = true`.
- FR-006 Alternative Flow B4 records cause `ProviderSuspended` or `ProviderDeactivated` on the booking. Before treatment starts (Accepted or Confirmed) it closes the booking.
- For a booking before treatment starts, an admin rehomes the patient to a replacement provider in the same inquiry through FR-006 Alternative Flow B5, recorded as a linked admin-authored acceptance record.
- An `In Progress` booking is not closed or transferred: it stays `In Progress` with `supportRequired`, and an admin either moves it to Aftercare with aftercare reassignment or cancels it with a reason (FR-006 Alternative Flow B7). An `Aftercare` booking follows FR-006 Alternative Flow B6 (round-two correction, 2026-10-18).
- Behaviour for inquiries still comparing providers (stage Inquiry or Quoted) is unchanged: only the affected provider's participation and quotes are cancelled.
- Patient messaging depends on the stage. Before acceptance, the patient receives the offer-unavailability message (`provider.status_cancellation_patient`) with Contact Admin/Support. After acceptance and before treatment starts, the patient receives `booking.provider_fault_replacement`, which says that an admin will arrange a replacement provider within the same inquiry, with no cancellation copy (added 2026-10-18).
- The patient can cancel only in the Inquiry and Quoted stages. From acceptance onward the patient sees "Contact support" and an admin cancels the booking through FR-006, from any booking state, with a mandatory reason and audit. The booking and inquiry become `Cancelled` and the accepted quote stays `accepted`; refunds and fees follow the payment placeholder (v2.11).
- Each inquiry date range carries a stable ID (`inquiry_date_ranges`) so quote date-price rows can reference it (v2.11).

## Requirement Delta

- Workflow 2 Alternative Flow B4: step 2 and Outcome rewritten.
- Business rule on provider status (accepted-treatment bullet) rewritten.
- REQ-003-020: first clause changed from "MUST cancel each inquiry" to "MUST NOT cancel"; keeps the inquiry open for the FR-006 transfer. Its patient-message sentence now separates the before-acceptance and after-acceptance notices (v2.10).
- Workflow 2 Alternative Flow B4 step 4 and Screen 8 Notes: patient message split by stage; B4 step 5 says reactivation does not restore cancelled participation or quotes (v2.10).
- A4, Workflow 5, Alternative Flow E2, Screens 8, 8a and 8b, Cancellation Rules, REQ-003-012, REQ-003-014 and User Story 4: patient cancellation limited to Inquiry and Quoted; Contact support and admin cancellation from acceptance; Screen 8 gains a Contact Support action (v2.11).
- Key Entities: stable date-range ID (v2.11).
- Workflow 2 Alternative Flow B4 steps 2 and 4, Outcome, the provider-status business rule and REQ-003-020: B5 transfer and `booking.provider_fault_replacement` limited to bookings before treatment; `In Progress` follows FR-006 Alternative Flow B7 and `Aftercare` follows B6 (round-two correction, 2026-10-18).

## Scope and Impact

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr003-inquiry-submission/prd.md`
- **Related FRs**: FR-006 (Alternative Flows B4 and B5, provider-fault transfer and payment placeholder), FR-015 (Alternative Flow A5 and Screen 4, cascade owner), FR-004 (`cancelled_provider_status` for unaccepted quotes), FR-020 and FR-030 (`booking.provider_fault_replacement` for accepted cases; `provider.status_cancellation_patient` before acceptance only), FR-005 and FR-006 (admin booking cancellation after acceptance; accepted quote stays `accepted`)
- **System documents**: `system-prd.md` and `system-data-schema.md` (inquiry stays open with `supportRequired`; the booking carries the provider-caused cause; `inquiry_date_ranges` with stable IDs; FR-003 owns the inquiry stage list Inquiry, Quoted, Accepted, Confirmed, In Progress, Aftercare, Completed, Cancelled)

### Out of Scope

Refund, credit transfer and fund-release mechanics (payment pass); the FR-006 placeholder applies.

## Acceptance and Validation

- No FR-003 text cancels an inquiry because the provider of its accepted booking was suspended or deactivated.
- FR-003, FR-006 and FR-015 describe the same post-acceptance route.
- No FR-003 text sends an `In Progress` booking to the FR-006 Alternative Flow B5 transfer; it follows the FR-006 Alternative Flow B7 admin decision.
- After acceptance, FR-003 shows no provider-caused cancellation copy; the patient is told through `booking.provider_fault_replacement` that an admin will arrange a replacement provider within the same inquiry.
- FR-003 offers no patient cancellation from the Accepted stage onward; it shows "Contact support" and routes cancellation to the FR-006 admin action.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation only)
- **Decision evidence**: SRC-MTG-002; decision log 2026-10-16 (M18, D6, D6-M, Q9, Q37, Q43, Q45); consolidated verification 2026-10-18; final audit 2026-10-18
- **Implementation reconciliation**: Required, not assessed
- **PRD change log**: v2.9 (2026-10-16); v2.10 (2026-10-18, consolidated verification corrections); v2.11 (2026-10-18, final audit corrections)
- **Update log**: Combined 2026-10-16 MTG-002 log
- **Supersedes**: CR-FR003-20261014-01 in part
- **Superseded by**: None
