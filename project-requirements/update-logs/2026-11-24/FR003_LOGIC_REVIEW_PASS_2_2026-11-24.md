# FR-003 Logic Review Pass 2 - Update Log

**Date**: 2026-11-24
**Scope**: FR-003 Inquiry Submission & Distribution PRD v2.19 and a prepared graph change-set
**Type**: Major update (one owner default replaced, rule changes, one new step)

## Documents changed

- `functional-requirements/fr003-inquiry-submission/prd.md`: v2.18 to v2.19
- Prepared, not applied: `graph/changesets/2026-11-24-fr003-logic-p2-fixes.yaml` (applying it is the controller's step)

## What changed

- **Archive (owner default, replaces the pass 1 guard).** An admin can archive an inquiry only when its stage is Completed or Cancelled; any other stage is refused with a message. Archive hides the inquiry in admin list views, sends no patient or provider notice and changes no status. The word "reversible" is removed from the Screen 12 Soft Delete row, and the rule that an inquiry stays open until an admin "cancels or archives it" now says cancels only.
- **Redistribution confirmation is scoped.** The patient is asked to confirm only when the last live offer was cancelled and the patient had explicitly selected the affected provider. A new system step asks the patient and sets `awaiting_patient_confirmation`; the confirm, decline and no-answer steps follow it. Otherwise the redistribution is automatic, and nothing is redistributed while another live offer remains.
- **Pending states have an exit.** `redistribution_state` returns to `none`, and any pending reminder is dropped, when the inquiry is cancelled, when an admin reassigns or reruns distribution on Screen 12, or when an admin clears `supportRequired`. The 48-hour reminder is sent only while the state is `awaiting_patient_confirmation`, and the patient can still confirm after it.
- **Screen 8.** New row for the Confirm and Decline actions, shown only while the state is `awaiting_patient_confirmation` or `admin_follow_up`.
- **Admin cancel and Close inquiry.** Both set `cancelled_by = admin` and leave `cancellation_reason` empty; the admin's reason is the booking's cancellation reason in FR-006. `cancelled_by` is now shown in the Full Inquiry group on Screen 12.
- **ProviderInquiry status.** A row becomes `viewed` when the provider first opens the inquiry detail and `quoted` when the provider first sends a quote (FR-004); it stays `quoted` afterwards, and a draft quote does not count toward `responses_count` (REQ-003-129).
- **Graph change-set.** Updates 18 nodes, adds 1 step, removes 6 edges (relabelled or moved) and adds 22 edges.

## Open items for neighbouring FRs (not edited here)

- FR-020: the confirm variant of `provider.status_cancellation_patient` needs the confirm and decline actions, and a one-time 48-hour reminder event that STP-003-095 emits.
- FR-016: the "Cancelled by Patient" indicator must read `cancelled_by`; for `admin` it reads the booking cancellation reason.
- FR-004: the first-send step should apply REQ-003-129 (sets the ProviderInquiry to `quoted`), and REQ-004-111 should reference REQ-003-127 instead of REQ-003-013.
