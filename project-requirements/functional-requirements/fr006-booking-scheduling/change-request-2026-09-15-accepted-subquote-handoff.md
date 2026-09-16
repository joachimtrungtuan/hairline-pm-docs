# Change Request: Accepted Subquote Booking Handoff

**Change Request ID**: CR-FR006-20260915-01
**Primary FR**: FR-006
**Triggering FR / Event**: CR-FR005-20260915-01 and approved full reconciliation decision
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-15
**Decision Date**: 2026-09-15
**PRD Version Change**: v1.7 to v2.5
**Related Commit(s)**: Pending

---

## Decision Summary

FR-006 consumes the immutable FR-005 AcceptanceEvent and accepted subquote snapshot as its only commercial booking input. The accepted subquote supplies package, date range, appointment, price, promotion, and treatment plan; its parent quote supplies inherited provider, treatment, graft, clinician, note, requirement, attachment, currency, expiry, version, and audit context. FR-006 must not ask the patient to reselect or reconstruct those terms.

## Baseline State

**Source version**: FR-006 v1.7, `Main Flow: Quote Acceptance → Booking Confirmation`

FR-006 treated a flat accepted quote and `quote ID` as the booking source. Payment-expiry and appointment-conflict flows could return that quote to an available state, without preserving the FR-005 v2.0 distinction between parent quote, accepted subquote, and immutable AcceptanceEvent.

## Approved State

**Target version**: FR-006 v2.5, `Main Flow: Subquote Acceptance → Booking Confirmation`

The updated PRD owns the booking-side handoff, explicit field-level screen provenance, booking linkage, payment retry, slot-conflict, and immutable-selection rules. Patient Screen 1 and the Provider/Admin booking-detail screens enumerate the accepted subquote and inherited parent provider, treatment, graft, clinician, note, visual-plan, requirement, attachment, currency, expiry, version, and acceptance-audit context as read-only snapshot data. `acceptedSubquoteVersion` and `acceptedParentQuoteVersion` identify the same FR-004 aggregate `QuoteVersion`. Acceptance fixes the selected appointment and atomically acquires its exclusive payment-window hold; a second acceptance for a held or blocked slot is rejected before an AcceptanceEvent or booking handoff is created. Successful payment converts the hold into a confirmed booking block. An expired payment window is terminal for that accepted selection: the slot is released and payment is blocked without reopening or rewriting prior quote records. The system PRD carries the matching system-level contract.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Booking input | Accepted parent quote and quote ID | AcceptanceEvent, accepted parent/subquote identifiers and versions, and complete snapshot | Preserve the exact accepted commercial choice |
| Patient flow | Accepted Quote detail | Accepted Subquote detail with inherited parent context | Match the only FR-005 acceptance target |
| Reselection | Implicitly unspecified | Package, date, appointment, and price reselection prohibited | Prevent booking drift |
| Payment hold expiry | Parent quote could return to Quote | Slot is released and payment blocked while AcceptanceEvent remains immutable | Do not reopen a competing parent response |
| Slot conflict | Quote status could revert or competing acceptances could survive until payment | Acceptance atomically acquires one exclusive hold; a competing acceptance is rejected before AcceptanceEvent or booking-handoff creation | Prevent contradictory accepted selections while preserving audit and commercial history |
| Booking relationship | One booking to one accepted quote | One booking to one AcceptanceEvent, accepted subquote, and parent context | Remove ambiguous quote-level linkage |
| Version provenance | Quote/subquote revision source unspecified | Accepted parent and subquote versions equal the same FR-004 aggregate `QuoteVersion` | Reject stale or mismatched handoffs deterministically |
| Hold expiry outcome | Retry/recovery boundary ambiguous | `Payment Window Expired` is terminal for the accepted selection; slot releases and payment is blocked | Preserve the immutable acceptance while preventing payment against an expired slot |
| Appointment lifecycle | Acceptance and confirmation language overlapped | Acceptance fixes the appointment and reserves its slot; successful payment confirms the booking | Separate commercial choice from confirmed booking state |

## Scope and Impact

### In Scope

- FR-006 booking entry, patient/provider/admin screens, payment retry, slot conflict, dependencies, requirements, tests, and Booking entity.
- Targeted FR-005 acceptance eligibility and AcceptanceEvent reservation provenance required to enforce the selected exclusive-hold rule.
- System PRD comparison, acceptance, booking, exception, metric, and glossary language.

### Out of Scope

- Changes to FR-004 or unrelated FR-005 comparison, presentation, commercial, and lifecycle behavior.
- Database schema, API, implementation, migration, or automated-test changes.
- Payment collection rules, installment economics, cancellation economics, or rescheduling policy.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr006-booking-scheduling/prd.md` — `Main Flow: Subquote Acceptance → Booking Confirmation`, Screens 1 through 6, Business Rules, requirements, and Key Entities.
- **Related FRs**: FR-004 supplies versioned parent quote/Option/date-price records; FR-005 atomically acquires the exclusive slot hold and supplies the accepted subquote and immutable AcceptanceEvent with its reserved slot reference.
- **System documents**: `project-requirements/system-prd.md`.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in this documentation phase.
- **Required assessment**: Acceptance API concurrency and slot-hold acquisition, Booking API payloads, data relationships, patient/provider/admin screens, payment retry, stale-handoff rejection, migrations, analytics, and regression coverage.
- **Compatibility / rollout risk**: High. A flat quote ID can lose or ambiguously reconstruct the selected package/date/appointment/price combination.
- **Data migration**: To be assessed.

## Acceptance and Validation

- Every booking is linked to exactly one AcceptanceEvent and its accepted parent/subquote versions and snapshot.
- FR-006 displays and charges the accepted subquote without package, date, appointment, or price reselection.
- Payment-expiry and slot-conflict handling never reopen a parent quote or mutate the accepted selection.
- Concurrent acceptance attempts for the same slot create exactly one exclusive hold, AcceptanceEvent, and booking handoff; the losing attempt makes no quote or inquiry state change.
- Consolidated FR-004/FR-005/FR-006 verification is completed before FR-006 returns to Verified & Approved.
- Implementation and migration evidence are assessed before reconciliation is marked Verified.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner
- **Decision evidence**: CR-FR005-20260915-01 acceptance condition; Product Owner full-reconciliation decision on 2026-09-15; aggregate-version, payment-window, appointment-lifecycle, and exclusive-reservation resolutions recorded on 2026-09-16
- **PRD change log**: FR-006 v2.0 through v2.5 rows dated 2026-09-15 and 2026-09-16
- **Update logs**: `../../update-logs/2026-09-15/FR006_ACCEPTED_SUBQUOTE_HANDOFF_2026-09-15.md`; `../../update-logs/2026-09-16/FR006_SLOT_EXCLUSIVITY_AND_SYSTEM_CONTRACT_2026-09-16.md`
- **Supersedes**: None
- **Superseded by**: None
