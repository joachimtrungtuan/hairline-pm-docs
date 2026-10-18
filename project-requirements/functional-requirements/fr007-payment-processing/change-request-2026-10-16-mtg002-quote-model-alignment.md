# Change Request: MTG-002 Quote Model Alignment for Payment Processing

**Change Request ID**: CR-FR007-20261016-01
**Primary FR**: FR-007
**Triggering FR / Event**: SRC-MTG-002 quote model verification and Product Owner decision log (2026-10-16); FR-005, FR-006 and FR-019 revisions of the same date
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v1.6 to v1.10
**Related Commit(s)**: Pending

> This CR exists because FR-007's implementation status is unknown (decision P1) and the change touches the payment-to-booking workflow and integration contracts.

---

## Decision Summary

FR-007 consumes the corrected MTG-002 quote model. Initial payment runs against one fixed slot hold that starts at subquote acceptance and lasts the FR-026 slot-hold duration (default 48 hours); payment failure never extends or restarts it, and only the FR-006 audited admin revive creates a new hold. The appointment record is created at successful initial payment. `Payment Window Expired` applies to the first payment step only. Payment amount and currency come from the FR-005 accepted snapshot; the promotion is frozen at acceptance, so checkout code entry is removed, and the first successful payment consumes the reserved promotion usage. Provider fault after acceptance follows FR-006 Alternative Flow B5, with money handled under its placeholder until the payment pass.

## Baseline State

**Source version**: FR-007 v1.6 (Business Workflows, Screens 1 to 6, Business Rules, Dependencies, Functional Requirements Summary, Key Entities)

Payment required the "original FR-006 hold" and said retry did not extend it, but did not state the hold length, owner setting or revive behaviour. A successful payment "converted its hold to a calendar block"; no step created an appointment record. Payment Window Expired recovery pointed to a "new-selection" route. FR-019 checkout-code applications were allowed as separate discount records on the accepted booking. The Initial Payment Guard paraphrased FR-006 eligibility. "View Quote" on Screens 4 and 6 opened the live FR-004 quote. No rule covered later missed payments or provider fault money.

## Approved State

**Target version**: FR-007 v1.10 (same headings; new Alternative Flow B4; REQ-007-020 to REQ-007-022; REQ-007-014 reworded)

See the updated [PRD](./prd.md). The hold, appointment, first-payment boundary, snapshot-read, promotion freeze and provider-fault references now match FR-006 v2.7, FR-005 v2.5 and FR-019 v2.2.

Commission is calculated on the accepted price after promotion (the FR-029 booking total), using the commission type (Percentage or Flat Rate) and value from the snapshot taken at booking confirmation; commission fields on Screens 3, 4 and 5B read that snapshot, never live configuration. Provider fault (Alternative Flow B4) applies only to `Accepted` and `Confirmed` bookings and moves the patient through an admin-authored replacement quote with a single supersession at replacement acceptance; a provider fault in `Aftercare` reassigns only the aftercare provider (FR-011). The same booking total, read from the acceptance snapshot, is the single base for the deposit percentage, instalment amounts, and commission. Missed later instalments and payout release rules are unchanged and remain with the payment pass.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Slot hold (B1, B2, B3, Business Rules, Screen 1, REQ-007-017) | Original FR-006 hold; retry does not extend it | One fixed hold from acceptance for the FR-026 duration (default 48 hours); payment failure never extends or restarts it; admin revive starts a new hold and takes one promotion use again (re-reserved for provider-selected promotions and patient codes, taken again for automatic promotions) | MTG-002; D2, D14, M3, Q30 |
| Appointment (Main Flow step 5, Screens 3 and 5B, Business Rules, REQ-007-020) | Hold converted to a calendar block | Appointment record created from the hold at successful initial payment; none exists on hold expiry | M4 |
| PWE recovery (B3) | New-selection or admin-intervention route | Cancel the inquiry and start a new one, or FR-006 audited admin revive | D1, D2 |
| First-payment boundary (Business Rules, Screen 2, REQ-007-021) | Not stated | PWE applies to the first payment step only; missed later installment or final payment never causes PWE or cancellation | D1, R7-1 |
| Amount and currency (Executive Summary, Screens, Payment & Billing Rules, REQ-007-016, REQ-007-018) | Accepted price plus permitted FR-019 checkout-code applications | Amount and currency read from the FR-005 accepted snapshot, never recomputed; no code entry, removal or replacement at checkout or payment | D9, M2, R7-1 |
| Promotion usage (Main Flow, FR-019 dependency, REQ-007-020) | Not stated | For provider-selected promotions and patient codes, the first successful initial payment consumes the use reserved at acceptance; an automatic promotion's use is consumed at acceptance per FR-019 REQ-019-015 | D11, Q30 |
| Provider fault (new Alternative Flow B4, REQ-007-022, Edge Cases) | Not covered | Follows FR-006 B5; paid money moves as credit, unused part refunded, no patient fee; mechanics deferred to the payment pass | D3, D6, D6-M, M18 |
| Initial Payment Guard | "Inquiry and accepted selection remain eligible" | Explicit checks: booking Accepted, inquiry not Cancelled, parent quote and subquote Accepted, provider Active, versions match, unexpired hold; FR-006 owns them | Minor FR-007-3 |
| Screens 4 and 6 actions | View Quote opened the live FR-004 quote | View Accepted Selection opens the snapshot via FR-006 | Minor FR-007-4 |
| Commission base (REQ-007-014) | Commission deducted on the "total procedure cost" | Commission calculated on the accepted price after promotion (FR-029 booking total), locked at booking confirmation; deduction timing at payout unchanged | Q28, Q5 |
| Commission fields (Screens 3, 4, 5B; payout rule) | Commission Rate as a percentage read from live FR-029 configuration | Commission type (Percentage or Flat Rate) and value read from the booking-confirmation snapshot | Q28; FR-029 alignment |
| Provider fault scope (Alternative Flow B4) | Any time after acceptance; transfer through a new linked acceptance record | Only `Accepted` and `Confirmed`; replacement quote in the same inquiry with a single supersession at replacement acceptance; provider-status cause for suspension or deactivation; `Aftercare` handled by FR-011 | Q35, Q36 |
| Deposit base (Screens 1, 3, 5, 5B; FR-029 dependency) | "Calculated from admin-configured percentage" with no stated base | FR-029 deposit percentage of the booking total from the acceptance snapshot; one base for deposit, instalments, and commission | Q25 |

## Scope and Impact

### In Scope

- Quote-model consumption by payment: hold, appointment creation, first-payment boundary, snapshot reads, promotion freeze and usage consumption, provider-fault reference.

### Out of Scope

- Payment rails, deposit and installment mechanics, refunds, fund release and payout; these stay for the payment pass. The commission base is in scope through the Q28 rewording of REQ-007-014.
- Exact credit, refund and allocation-override mechanics for provider fault (D6-M placeholder only).

### Affected Contracts

- **PRD owner**: `fr007-payment-processing/prd.md` — Business Workflows (Main Flow, B1 to B4), Screens 1 to 6 (including commission fields), Business Rules, Dependencies, REQ-007-016 to REQ-007-022, Key Entities.
- **Related FRs**: FR-005 (accepted snapshot), FR-006 (hold, revive, REQ-006-016, Alternative Flow B5), FR-007B (first installment uses the same boundary and snapshot), FR-015 (provider Active check), FR-017 (provider-fault money and refunds in the payment pass), FR-019 (post-acceptance freeze, usage consumption), FR-026 (slot-hold duration).
- **System documents**: `system-data-schema.md` (bookings hold fields and appointment creation, promotion usage consumption), `system-technical-spec.md` (slot held at acceptance, blocked only after successful payment).

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Payment service guard checks, hold expiry handling, appointment creation on payment, checkout promotion-code input removal, promotion usage consumption, admin and provider "View Quote" links.
- **Compatibility / rollout risk**: Any implemented checkout-code entry after acceptance must be removed; existing bookings with such applications need review.
- **Data migration**: To be assessed.

## Acceptance and Validation

- Payment failure or retry never changes the hold deadline; a revived booking shows the new hold deadline.
- Successful initial payment creates exactly one appointment record and, for a provider-selected promotion or patient code, consumes the reserved promotion use; an automatic promotion's use is not consumed again.
- An overdue final payment flags the booking but never sets `Payment Window Expired`.
- Checkout shows no promotion code input; charged amount and currency equal the acceptance snapshot.
- REQ-007-014 no longer mentions "total procedure cost" and names the accepted price after promotion, locked at booking confirmation.
- Every deposit amount field and the FR-029 integration point name the booking total as the deposit base.
- Commission fields show Percentage or Flat Rate from the booking-confirmation snapshot; a later FR-029 change does not alter an existing booking's commission.
- Alternative Flow B4 is not offered for `In Progress` or `Aftercare` bookings, and the replacement booking's amount comes from the replacement quote's acceptance snapshot.
- Cross-FR: hold wording matches FR-006; PWE boundary references FR-006 REQ-006-016; commission and deposit base match FR-029.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, documentation approved 2026-10-16 via the decision log and 2026-10-18 via the MTG-002 decision log (documentation only); implementation reconciliation required, not assessed
- **Decision evidence**: SRC-MTG-002; decision log 2026-10-16 (D1, D2, D3, D6, D6-M, D9, D11, D14, M2, M3, M4, M18, R7-1, R7-3, P1); findings S1-2, FR-007-3, FR-007-4; Product Owner follow-up decisions Q25, Q28 (with Q5), Q30; final decisions Q35 and Q36 (2026-10-18)
- **PRD change log**: v1.7 and v1.8 rows (2026-10-16); v1.9 consolidated verification corrections and v1.10 final audit corrections (2026-10-18)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: CR-FR007-20261013-01 in part ( its "FR-019 checkout discounts preserved as separate applications" statement is replaced by the post-acceptance freeze)
- **Superseded by**: None
