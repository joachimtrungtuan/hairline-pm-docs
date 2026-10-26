# Change Request: Aftercare Reassignment for Provider Fault During Aftercare

**Change Request ID**: CR-FR011-20261016-01
**Primary FR**: FR-011
**Triggering FR / Event**: SRC-MTG-002 quote model alignment, Product Owner decision log (2026-10-16) and final decisions (2026-10-18); FR-006 Alternative Flow B6
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-18
**PRD Version Change**: v1.4 to v1.5 (v1.5 final audit corrections)
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner decided that a provider fault while a booking is in `Aftercare` reassigns only the aftercare provider or team. The booking and the treatment record stay, and there is no new quote, acceptance or payment; the provider-fault transfer applies only before treatment starts (Q36). Every admin intervention also needs its own admin screen with fields, validation, mandatory reason, confirmation, audit entry and notice (Q43). FR-011 had a Reassign Provider button with no screen, and its provider-status cascade cancelled treatment-linked aftercare cases. FR-011 now specifies the reassignment screen and keeps treatment-linked cases active for reassignment.

## Baseline State

**Source version**: FR-011 v1.4, Workflow 4 (Admin Aftercare Management) D1 and D4, Screen 14: Aftercare Case Details Tab 4, General Module Rule 4, Edge Cases, REQ-011-004 and REQ-011-014

Screen 14 offered "Reassign Provider" as an always-available button with no fields, reason, confirmation or notice. D4 and Rule 4 cancelled every non-terminal aftercare case of a suspended or deactivated provider, including treatment-linked cases, and left recovery to the existing tools. There was no flow for a provider fault during treatment-linked aftercare.

## Approved State

**Target version**: FR-011 v1.5, same headings plus Workflow 4 Alternative Flow D5, Screen 19: Reassign Aftercare Provider (Admin) and REQ-011-015

- A provider fault during treatment-linked aftercare reassigns only the aftercare provider or team (Alternative Flow D5). The FR-006 booking stays `Aftercare`, the FR-010 treatment record stays unchanged, and no quote, acceptance or payment is created (Q36).
- Screen 19 specifies the reassignment: target type, new provider or aftercare team member, mandatory reason, optional resolution of the `supportRequired` marker, a confirmation summary, an audit entry and the mandatory `aftercare.provider_reassigned` notice (FR-011 producer) to the patient and the new aftercare provider, with no admin alert and no notice to the previous provider (Q43, Q47).
- Screen 19 is opened from Screen 14 Reassign Provider, from the FR-006 admin booking detail Reassign Aftercare link, and from the Move to Aftercare route of the FR-006 In-Progress provider-fault decision (FR-006 Screen 11) (Q45).
- On provider suspension or deactivation, standalone aftercare cases are still cancelled with the provider-status cause and `supportRequired`. Treatment-linked cases are not cancelled; the cause and marker are recorded and an admin reassigns them on Screen 19.
- Money effects, if any, follow the FR-006 payment placeholder.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Provider fault during treatment-linked aftercare | No flow | Workflow 4 D5: aftercare provider or team reassigned; booking and treatment record kept; no new quote, acceptance or payment | Q36 |
| Admin reassignment screen | Screen 14 button only, always available | Screen 19 with fields, validation, mandatory reason, confirmation, audit entry and notice; Screen 14 button opens it | Q43 |
| Provider suspension or deactivation (D4, Rule 4, Edge Cases, REQ-011-014) | Every non-terminal aftercare case cancelled | Standalone cases cancelled; treatment-linked cases stay active and are reassigned on Screen 19 | Q36 |
| Reassignment notice | Patient, new assignee and previous provider; event not registered | Mandatory `aftercare.provider_reassigned` to the patient and the new aftercare provider; no admin alert | Q47 |
| Entry from an In Progress provider fault | None | Screen 19 opened after the FR-006 In-Progress provider-fault decision moves the booking to `Aftercare` | Q45 |
| Functional requirements | REQ-011-001 to 014 | REQ-011-014 revised; REQ-011-015 added | Q36, Q43 |

## Scope and Impact

### In Scope

- FR-011 admin aftercare reassignment, the treatment-linked provider-fault route and the provider-status cascade split between standalone and treatment-linked cases.

### Out of Scope

- Refunds, payout and any money movement for the reassignment (payment placeholder in FR-006).
- Registration of the `aftercare.provider_reassigned` event key in the FR-020 and FR-030 catalogues (owned by those FRs; FR-011 is the producer).

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md` — Workflow 4 D4 and D5; Screen 14 Tab 4; Screen 19; General Module Rule 4; Edge Cases; REQ-011-014 and REQ-011-015
- **Related FRs**: FR-006 (Alternative Flow B6 and the Screen 6 Reassign Aftercare link; Alternative Flow B4 keeps `Aftercare` bookings in `Aftercare`), FR-010 (treatment record unchanged), FR-015 (suspension and deactivation cascade must stop cancelling treatment-linked `Aftercare` bookings), FR-020 and FR-030 (register mandatory `aftercare.provider_reassigned` for the patient and the new aftercare provider)
- **System documents**: `system-data-schema.md` (aftercare case assignee history and reassignment audit), `system-technical-spec.md` (provider-status cascade)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Aftercare reassignment API and audit, provider-status cascade for treatment-linked cases, admin UI for Screen 19, notification dispatch, permissions, tests
- **Compatibility / rollout risk**: Treatment-linked aftercare cases already cancelled by the old cascade need an admin review
- **Data migration**: To be assessed

## Acceptance and Validation

- An admin can reassign a treatment-linked aftercare case on Screen 19 only with a reason and after confirmation, and the change appears in the audit trail.
- After the reassignment, the FR-006 booking is still `Aftercare`, the treatment record is unchanged, and no quote, acceptance or payment exists for it.
- The patient and the new aftercare provider receive `aftercare.provider_reassigned`; no admin alert is sent; the previous provider has no aftercare actions on the case.
- A provider suspension cancels that provider's standalone aftercare cases but leaves treatment-linked cases active with the cause and `supportRequired` set.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-18, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation only)
- **Decision evidence**: SRC-MTG-002; final decisions Q36, Q43, Q45 and Q47 (2026-10-18); final audit lifecycle and notification findings
- **Implementation reconciliation**: Required, not assessed
- **PRD change log**: v1.5 final audit corrections (2026-10-18)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: CR-FR011-20261014-01 in part (cancellation of treatment-linked aftercare cases on provider suspension or deactivation)
- **Superseded by**: [CR-FR011-20261026-01](change-request-2026-10-26-standalone-aftercare-reassignment.md) in part (standalone aftercare cases are no longer cancelled on provider suspension or deactivation; they are reassigned on Screen 19)
