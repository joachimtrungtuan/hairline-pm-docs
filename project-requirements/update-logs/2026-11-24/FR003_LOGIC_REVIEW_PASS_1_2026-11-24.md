# FR-003 Logic Review Pass 1 - Update Log

**Date**: 2026-11-24
**Scope**: FR-003 Inquiry Submission & Distribution PRD v2.18 and a prepared graph change-set
**Type**: Major update (structural rule changes, new requirement rules, new flows and steps)

## Documents changed

- `functional-requirements/fr003-inquiry-submission/prd.md`: v2.17 to v2.18
- Prepared, not applied: `graph/changesets/2026-11-24-fr003-logic-p1-fixes.yaml` (applying it is the controller's step)

## What changed

- **Archive guard (owner default).** An admin can archive an inquiry only when it has no live quote (a sent quote that has not expired) and no accepted quote or booking. Otherwise the archive is refused with a message and nothing changes. Archiving sends no patient or provider notice.
- **No automatic inquiry expiry at launch (owner default).** The inquiry expiry window setting, the inquiry expiry timestamp and the expired provider-inquiry status are retired. Draft expiry (a fixed 7 days) and quote expiry (FR-004) are unchanged. The admin override now covers distribution only.
- **Account-deletion cancellation (owner default).** The open inquiry is cancelled when an admin approves the deletion request (FR-023), not when the patient submits it. A deletion request is blocked while the patient has an inquiry at the Accepted stage or later (FR-001).
- **Redistribution needs the patient's confirmation (owner default).** When the patient had selected the affected provider, the patient confirms or declines. Confirm sends the inquiry back to matching; decline leaves it as it is; with no answer after a fixed 48 hours one reminder is sent and the inquiry appears in the admin queue. REQ-003-128 and the `redistribution_state` values `declined` and `admin_follow_up` carry this, and Screen 11 gains a follow-up column.
- **Critical medical alert (owner default).** "Critical" means the FR-025 Red tier. It shows as a badge in the admin inquiry queue and sends no separate notification.
- **Cancel flows.** The quote-review cancel on FR-005 Screen 1 now enters the same confirmation modal and commit steps. Admin cancel and Close inquiry also cancel a replacement draft with no provider notice (new REQ-003-127, quote side in REQ-004-111). The cancel preview count (`preview_quote_count`) is separate from the committed `cascade_quote_count`, and the modal and success wording no longer says "active". Who cancelled is stored in `cancelled_by`.
- **Counts and access.** REQ-003-129 defines `quotes_count` and `responses_count`. REQ-003-074 is now an access rule: a provider sees an inquiry only through a ProviderInquiry row that is not cancelled.
- **Smaller fixes.** The 7-day draft rule is stated as fixed; an expired draft sends the patient to a new inquiry; admin re-notification, the 5-minute provider notice target (owned here, delivered by FR-020), the Inquiry-stage provider-cancel branch, and a vocabulary note (graph Quote and Acceptance are the PRD stages Quoted and Accepted) were added.
- **Graph change-set.** Updates 18 rule statements, adds 3 rules and 8 steps, adds 2 fields and 5 enum values, retires 1 setting and 1 field, retires 1 enum value, and removes 17 edges (edges to retired steps, edges replaced by relabelled ones, and edges to the retired expiry field and setting), adds 82 edges.

## Open items for neighbouring FRs (not edited here)

- FR-001 and FR-023: the account-deletion request must be blocked from the Accepted stage onward, and the inquiry is cancelled at admin approval.
- FR-005: Screen 1 cancel must enter the shared modal (REQ-005-041 read-only state); the replacement-quote text should match REQ-003-127.
- FR-006: Close inquiry (Screen 6) and the booking cancel (Screen 9) must call the replacement-draft cancel.
- FR-020: delivery of the provider cancel notice stays at the 5-minute target (REQ-020-020); the admin-queue badge needs no event.
- FR-025: the Red tier is the meaning of "critical" for the admin badge.
- The Payment stage of the requirements graph has no `inquiry.stage` value in the FR-003 PRD.
