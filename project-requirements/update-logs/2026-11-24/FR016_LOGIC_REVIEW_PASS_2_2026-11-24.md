# FR-016 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 1.18 to 1.19, with a graph change-set)
**Scope**: FR-016 Admin Patient Management
**Source of findings**: `plans/reports/tester-261124-fr016-logic-p2.md` (12 findings: 4 contradiction, 7 missing piece, 1 wiring only; all ruled fixes, 2 with owner defaults). This is the last pass for FR-016; what is not fixed is in the ledger leftovers.

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr016-admin-patient-mgmt/prd.md`

- **Deletion approval**: Approve is shown only for Pending Admin Review; a Verification Required request is validated first and returns to Pending Admin Review; Deny stays available from both; a denied request ends Denied and the patient is notified with the reason (Screen 8, Flow B5 step 3; REQ-016-190, REQ-016-191, REQ-016-173).
- **Refunds**: "Issue Refund" enters an FR-007 manual refund, which another admin with billing permission approves or denies and the requesting admin never approves; the FR-016 enhanced confirmation for amounts above 1,000 US dollars applies in addition. No threshold is restated from FR-007 (Flow A3 step 4, Screen 5, General Module Rule 4; REQ-016-011, REQ-016-020).
- **Payment Retry and Send Payment Reminder**: use the same access as the FR-007B Retry Charge action; Retry Payment calls that action and FR-016 has no retry of its own. This replaces the pass 1 mapping of payment retry to Issue Refunds (Rule 3, Screen 5; REQ-016-070, REQ-016-079, REQ-016-140).
- **Suspension cascade**: the cause is named "Patient account suspended"; the suspension audit entry lists the booking ids cancelled, failed and left untouched; a failed booking is marked "Cancellation failed" on the patient's Overview tab and retried through the FR-006 cancel action; a suspension started from any admin screen runs this flow (Flow A6, Rule 10; REQ-016-012, REQ-016-217, REQ-016-218, REQ-016-219).
- **Suspended patient, conversations and inquiries**: conversations are read-only; open inquiries and quotes stay as they are and follow their own expiry; nothing is cancelled except the cascade bookings; conversations reopen when the suspension is lifted or ends (new REQ-016-224, Rule 10, Flow A6 step 14; owner default 225).
- **Password reset**: never changes a Suspended status; Reset Password is hidden for a Suspended patient; a Locked account becomes Active after a reset (new REQ-016-223, Rule 12, Flow A4, Screen 2, User Story 4 scenario 4).
- **Audit action list**: Payment Reminder, Provider Medical Report Request and Data Export (export name in the entry) added; Provider Warning removed; Patient Warning reworded (REQ-016-160).
- **Take Action**: on a flagged conversation it offers one step, a formal warning to the patient or suspension through the existing flow; it needs Edit Patients; provider warnings are not sent from the patient page (new REQ-016-225, Screen 6, Rule 3, User Story 5 scenario 4; owner default 226).
- **New flows**: A9 Lift Suspension, A10 Unlock Account, A11 automatic end of a timed suspension, A12 Take Action, each wired to its existing rules (REQ-016-009, REQ-016-110, REQ-016-201, REQ-016-220).
- The change log row (1.19) is added; Last Updated is unchanged (2026-11-24).

## Owner defaults applied (plain-language entries 225 and 226 in the defaults report)

Suspended patient's inquiries, quotes and conversations (225); Take Action warnings (226).

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr016-logic-p2-fixes.yaml`

- New: rules REQ-016-223 to REQ-016-225; steps STP-016-121 to STP-016-129; flows FLW-016-lift-suspension, FLW-016-unlock-account, FLW-016-suspension-auto-end, FLW-016-take-action; audit action values payment_reminder, provider_medical_report_request, data_export; provider_warning retired.
- Wiring: the deletion review (STP-016-112 and STP-016-113) gets conditional exits to the Denied outcome step STP-016-121, and STP-016-114 gets a back edge to STP-016-113; STP-016-118 and STP-016-119 are done by the system; the cascade step STP-016-080 branches on failure (STP-016-120) or success (STP-016-081); REQ-016-201 applies to the system actor.
- Rule statements, step titles and three descriptions (audit action type field, Screens 6 and 8) updated to mirror the PRD.
- Cross-FR edges (from FR-016 nodes only): FR-016 references REQ-007-015, REQ-007-097, REQ-007B-080 and REQ-007B-090; STP-016-034 applies REQ-007-015. No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 203 change rows, no errors; the copy was deleted.

## Not changed here

Queued in the logic review ledger section for FR-016: FR-006 (cause "Patient account suspended" on Screen 9), FR-001 (login rule and message for Suspended; Screen 19 Suspend opens the FR-016 flow), FR-012 (REQ-012-018, read-only conversations while suspended), FR-030 (patient warning notice event), FR-031 (Issue Refunds approval wording, permission for Retry Charge and Take Action). Minor observations are listed under Leftovers in the ledger section.
