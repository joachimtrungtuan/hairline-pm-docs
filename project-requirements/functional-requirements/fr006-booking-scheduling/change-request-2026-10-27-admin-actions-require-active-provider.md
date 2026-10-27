# Change Request: Admin Booking Actions Require an Active Provider

**Change Request ID**: CR-FR006-20261027-02
**Primary FR**: FR-006
**Triggering FR / Event**: Backend follow-up question F14 (`FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md`); Product Owner decision 2026-10-27; aligns with FR-015 Rule 9
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-26
**Decision Date**: 2026-10-27
**PRD Version Change**: v2.10 to v2.11
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner decided that an admin revive, an admin appointment change, and an admin-authored acceptance must check that the provider concerned is `Active`. If the provider is `Suspended` or `Deactivated`, the action is blocked and the admin is directed to the provider-fault transfer.

The backend team found the gap (F14). A booking that reached `Payment Window Expired` before its provider was suspended is not touched by the provider-status cascade, and FR-006 Screen 7 had no provider-status condition. An admin could revive it, and the patient could then pay a suspended provider.

## Baseline State

**Source version**: FR-006 v2.10, Screen 7 (Revive Booking), Screen 8 (Change Appointment), Screen 10 (Provider-Fault Transfer and Replacement Quote), Admin Status and Date Intervention Rules, REQ-006-017.

- Screen 7 re-checked slot availability and the promotion limit, but not the provider's status.
- Screen 8 re-checked slot availability, but not the provider's status.
- Screen 10 required the replacement provider to be `Active` when selected, with no re-check at acceptance.

## Approved State

**Target version**: FR-006 v2.11, same headings, and new REQ-006-020.

- On submit, the admin revive (Screen 7) and the admin appointment change (Screen 8) check that the booking's provider is `Active`. If it is `Suspended` or `Deactivated`, the action is blocked, nothing changes, and the admin sees:
  - revive: "This provider is suspended or deactivated, so this booking cannot be revived. Use the provider-fault transfer instead."
  - appointment change: "This provider is suspended or deactivated, so this appointment cannot be changed. Use the provider-fault transfer instead."
- The admin-authored replacement acceptance (Alternative Flow B5, Screen 10) re-checks on submit that the replacement provider is still `Active`. If not, it is blocked with: "This provider is suspended or deactivated, so this replacement quote cannot be accepted. Choose another replacement provider."
- These checks follow FR-015 Rule 9, which owns the list of points where provider status is revalidated.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Screen 7 Revive Booking | Slot and promotion checks only | Also blocked when the provider is `Suspended` or `Deactivated` | Prevents a patient paying a provider who cannot treat |
| Screen 8 Change Appointment | Slot check only | Also blocked when the provider is `Suspended` or `Deactivated` | Same rule for every admin action that keeps the booking with the provider |
| Screen 10 replacement acceptance | Replacement provider `Active` at selection | Also re-checked at acceptance | The provider may be suspended between selection and acceptance |
| Admin Status and Date Intervention Rules; REQ-006-020 | No provider-status rule | One rule with an action-specific message | Single place for the rule |

## Scope and Impact

### In Scope

- Provider-status checks on FR-006 admin revive, admin appointment change, and admin-authored replacement acceptance.

### Out of Scope

- The provider-status cascade itself, which is unchanged.
- The FR-015 Rule 9 and REQ-015-020 revalidation list, which FR-015 owns and updates.
- Patient payment against an expired booking, which stays blocked.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr006-booking-scheduling/prd.md`: Screen 7, Screen 8, Screen 10, Admin Status and Date Intervention Rules, REQ-006-020.
- **Related FRs**: FR-015 Rule 9 and REQ-015-020 (revalidation points); FR-005 (admin-authored acceptance record).
- **System documents**: None.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Admin revive, appointment change, and replacement acceptance endpoints; admin UI error messages; tests.
- **Compatibility / rollout risk**: Low. The check only blocks actions that would leave a booking with a provider who cannot treat.
- **Data migration**: None.

## Acceptance and Validation

- An admin cannot revive a `Payment Window Expired` booking whose provider is `Suspended` or `Deactivated`; the revive message is shown and the booking stays `Payment Window Expired`.
- An admin cannot change the appointment of a booking whose provider is `Suspended` or `Deactivated`; the appointment and hold or calendar block stay unchanged.
- A replacement acceptance is blocked when the replacement provider became `Suspended` or `Deactivated` after it was selected.
- Each blocked action leaves no audit entry for a status or appointment change and sends no notice.

## Approval and Traceability

- **Requested by**: Backend team, follow-up question F14.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-27.
- **Decision evidence**: Product Owner decision dated 2026-10-27 on `FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md` F14.
- **PRD change log**: [FR-006 Appendix: Change Log](prd.md#appendix-change-log), v2.11 dated 2026-10-27.
- **Update log**: [FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md](../../update-logs/2026-10-27/FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md).
- **Supersedes**: None.
- **Superseded by**: None.
