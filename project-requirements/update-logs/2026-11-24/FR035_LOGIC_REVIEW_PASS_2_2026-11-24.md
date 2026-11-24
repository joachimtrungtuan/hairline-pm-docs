# FR-035 Logic Review Pass 2 - 2026-11-24

**Scope**: FR-035 Patient Help Center and Support Submission. PRD version 1.4 to 1.5.
**Type**: PRD logic fixes (final pass) plus a prepared graph change-set. Neighbour rows for FR-026, FR-034 and FR-030 are queued, not edited.
**Findings addressed**: 11 reviewed; all 11 closed on the FR-035 side. Owner defaults used: 135 (at least one support contact value always set) and 136 (one queued request, 24 hours).

## What changed in the PRD

- Closed Case Banner: the reopen clause and the link, now named "Email support", show only when the support email setting has a value.
- Support contact: FR-026 must keep at least one of phone or email set; the Hub section is always rendered and each row shows when it has a value.
- Ticket list: a Resolved case opened from the list reaches the reopen path (flow A5).
- Replies: a reply that cannot be sent is refused with a retry message and the text is kept; reply files follow the case-file scan rules.
- Offline queue: one request waits at a time; one not sent within 24 hours is reported as not sent and the text is kept.
- Emails: the resolution email depends on the Send Resolution Email option on the case (FR-034) and the notification settings; the confirmation email follows the notification settings.
- Lifecycle: forward only, except a patient reply to a Resolved case and an Admin reopen of a Closed case; after an Admin reopen the patient sees the case as Open with the reply box and gets the FR-034 reopen notice.
- Report a Problem: part of the A3 trigger; Screen 5 opens with the category preset to Technical Issue.
- Flow A6: notices stop for a deleted patient; the auto-close is attributed to FR-034 REQ-034-062.
- Flow B3: a file that fails the virus scan has its own branch; a case notice tap is an entry to Ticket Detail.
- Minor: an empty content type card is greyed out but still tappable.

## Graph

Change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr035-logic-p2-fixes.yaml` is prepared, test-applied on a copy of the graph without errors (53 change rows), and not applied to the live graph by the author. The controller applies it. It adds one edge from an FR-034 step into flow A6.

## Neighbour rows queued (not edited here)

FR-026 (validation: not both support contact values blank), FR-034 (problem report category preset, resolution email owner, reopen cross-reference), FR-030 (confirm resolution email follows notification settings).

## Evidence

Findings: `plans/reports/tester-261124-fr035-logic-p2.md`. Fix detail per finding: `plans/reports/docs-manager-261124-fr035-logic-p2-fixes.md`.
