# Change Request: Automatic Redistribution When a Provider-Status Cascade Removes the Last Live Offer

**Change Request ID**: CR-FR003-20261027-02
**Primary FR**: FR-003
**Triggering FR / Event**: Backend follow-up question F9 (`FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md`); Product Owner decision 2026-10-27; FR-015 provider-status cascade
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-26
**Decision Date**: 2026-10-27
**PRD Version Change**: v2.11 to v2.12
**Related Commit(s)**: Pending

---

## Decision Summary

Before acceptance, when a provider's suspension or deactivation cancels its offer and the patient has no other live offer on that inquiry, the system now redistributes the inquiry automatically to eligible providers that have not yet received it. The patient is told "We are finding new offers for you." If the patient had explicitly selected that provider, the patient is asked to confirm first.

Before this decision, FR-003 did not redistribute the inquiry: the patient saw that the offer was unavailable and could only contact admin support. The backend team asked what a patient whose only offer disappeared should see and do (F9). This reverses the earlier "no automatic redistribution" position, so it is recorded as a Change Request.

## Baseline State

**Source version**: FR-003 v2.11, Workflow 2 Alternative Flow B4 steps 3 and 4, Rule 6 (Provider Status Cancellation Rules), Screen 8 Notes, REQ-003-020.

- Before acceptance, the cascade cancelled only the affected provider's participation and quotes, kept the inquiry stage, and set `supportRequired = true`.
- The patient received the offer-unavailability message (`provider.status_cancellation_patient`) with a Contact Admin/Support action.
- The inquiry was never redistributed automatically. Recovery depended on admin action.

## Approved State

**Target version**: FR-003 v2.12, same headings, and new REQ-003-021.

- When the cascade cancels a live offer (a sent quote that has not expired) and the patient has no other live offer on the inquiry, the system redistributes the inquiry to eligible providers that have not yet received it, using the normal Workflow 2 matching, eligibility, and cap rules. An FR-037 exclusive inquiry is released from its restriction in the same way as the explicit-decline fallback.
- The patient is told "We are finding new offers for you."
- If the patient had explicitly selected the affected provider, the patient is asked to confirm first, and the inquiry is redistributed only after the patient confirms.
- If another live offer remains, the inquiry is not redistributed.
- If no eligible provider is found, Workflow 2 Alternative Flow B1 applies.
- The `supportRequired` marker is kept as before. Redistribution runs at most once per provider-status event and inquiry.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Workflow 2 Alternative Flow B4 step 3; Rule 6 | No automatic redistribution | Automatic redistribution when no live offer remains; patient confirmation first when the patient had selected the provider | The patient should not be left without offers through no fault of their own |
| B4 step 4; Screen 8 Notes | Offer-unavailability message with Contact Admin/Support | Same message, plus "We are finding new offers for you." or a request to confirm redistribution | The patient knows what happens next |
| REQ-003-021 | Not present | New requirement for automatic redistribution | Testable contract |
| `supportRequired` marker | Set by the cascade | Still set; unchanged | Admin keeps visibility of the case |

## Scope and Impact

### In Scope

- Pre-acceptance redistribution after a provider-status cascade on FR-003 inquiries in the Inquiry or Quoted stage.
- The patient message and confirmation step.

### Out of Scope

- Post-acceptance cases, which still follow FR-006 Alternative Flows B4 to B7.
- Changes to the normal Workflow 2 distribution rules.
- Notification template wording beyond the approved sentence, which FR-020 owns.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr003-inquiry-submission/prd.md`: Workflow 2 Alternative Flow B4 steps 3 and 4 and Outcome, Rule 6, Screen 8 Notes, REQ-003-021, Edge Cases.
- **Related FRs**:
  - FR-015 (Alternative Flow A5 and Screen 4) owns the triggering event.
  - FR-020 owns the `provider.status_cancellation_patient` message, which needs the redistribution and confirmation variants.
  - FR-004 shows the cancelled offer as unavailable; unchanged.
  - FR-014 reads `distributed_at`, which is set on first distribution to each new provider.
- **System documents**: `project-requirements/system-data-schema.md` v1.13.0 §5 `inquiries`: new nullable columns `redistribution_state` (`awaiting_patient_confirmation`, `confirmed`, `declined`, `completed`), `redistribution_state_at`, and `redistribution_provider_status_event_id` (references §41 `provider_status_events`) record the confirmation step and enforce one redistribution per provider status event. Redistribution itself creates normal `inquiry_providers` rows.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Cascade job, live-offer check, redistribution call into normal distribution, patient confirmation prompt and its handling, patient message variants, idempotency per provider-status event, and tests.
- **Compatibility / rollout risk**: Medium. New providers receive inquiries they did not receive before; the normal eligibility and cap rules apply.
- **Data migration**: None.

## Acceptance and Validation

- When the cascade cancels the only live offer and the patient had not selected that provider, the inquiry is distributed to new eligible providers, the patient sees "We are finding new offers for you.", and `supportRequired` stays set.
- When the patient had selected that provider, no redistribution happens until the patient confirms.
- When another live offer remains, no redistribution happens.
- A suspended, deactivated, or password-not-set provider never receives the redistributed inquiry.
- A replayed cascade does not distribute the inquiry again.

## Approval and Traceability

- **Requested by**: Backend team, follow-up question F9.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-27.
- **Decision evidence**: Product Owner decision dated 2026-10-27 on `FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md` F9.
- **PRD change log**: [FR-003 Appendix: Change Log](prd.md#appendix-change-log), v2.12 dated 2026-10-27.
- **Update log**: [FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md](../../update-logs/2026-10-27/FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md).
- **Supersedes**: CR-FR003-20261014-01 and CR-FR003-20261016-01 in part (pre-acceptance handling, which did not redistribute).
- **Superseded by**: None.
