# FR-016 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 1.17 to 1.18, with a graph change-set)
**Scope**: FR-016 Admin Patient Management
**Source of findings**: `plans/reports/tester-261124-fr016-logic-p1.md` (15 findings; all ruled fixes, 2 with owner defaults)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr016-admin-patient-mgmt/prd.md`

- **Cancel Booking states**: Screen 9, Flow A8 and the editability rule name the FR-006 cancel states exactly: the button only for `Accepted`, `Payment Window Expired`, `Confirmed`; `In Progress` links to FR-006 Screen 11 (Alternative Flow B7); `Aftercare` has no cancel button, only Decline Request pointing to FR-006 B6 (REQ-016-078, REQ-016-194).
- **Audit entries for system actions**: admin name and the 20-character justification are required only for admin-performed actions; a system-generated entry shows "System" and the system-stated cause (REQ-016-007, REQ-016-161, REQ-016-162).
- **Audit action list**: Manual Notification, Patient Warning, Provider Warning, Suspension Lifted and Suspension Ended added to the Screen 7 list (REQ-016-160).
- **Suspension cascade**: cancels only `Accepted`, `Payment Window Expired` and `Confirmed` bookings; `In Progress` and `Aftercare` bookings are left untouched and listed on the confirmation dialog; a failed cancellation does not stop the suspension and the failed bookings are listed for follow-up (new REQ-016-217, REQ-016-218). The reason sent to the patient and the provider is a fixed neutral text; the admin justification stays in the audit entry only (REQ-016-219).
- **Way back from a suspension**: Lift Suspension on Screen 2 (Edit Patients, justification, audit entry Suspension Lifted, patient notice) and Unlock Account shown only for a Locked account; the appeal is the patient contacting support (an FR-034 ticket); at automatic end of a timed suspension the system logs Suspension Ended and notifies the patient (new REQ-016-220; REQ-016-201, REQ-016-110, REQ-016-054).
- **Deactivated and archive removed**: the Deactivated status, the archive interface rule and the deactivation wording are gone; Delete Patients now covers approving deletion requests (REQ-016-017, REQ-016-070, REQ-016-076, REQ-016-183; REQ-016-074 retired in the graph).
- **Deletion flow B5**: reduced to the admin steps (review on Screen 8, verification, approve or deny, blocked by obligation); the patient submits from FR-001 Delete Account and FR-023 owns the process (REQ-016-060, REQ-016-061, REQ-016-063, REQ-016-171).
- **Screen 8**: the Status filter offers all five request statuses; badges for Overdue, Blocked by obligation, Jurisdiction review and Needs attention (new REQ-016-222); Approve and Deny only for Pending Admin Review and Verification Required, Approve with a retention confirmation (REQ-016-186, REQ-016-190, REQ-016-191).
- **Deletion certificate dropped**: the Fulfilled request with the actions taken is the audit evidence (REQ-016-062).
- **Edge Case 5**: now follows FR-023 Alternative Flow A3 (request stays pending and blocked, admins notified when the obligation ends, patient told the timeline, deadline keeps running); the example uses USD (REQ-016-067).
- **Permissions**: Rule 3 maps the actions the FR-031 list does not name: Reset Password, Unlock Account and Lift Suspension need Edit Patients; Send Notification needs Respond to Support; Payments tab needs View Patient Billing; Payment Retry needs Issue Refunds; Communications tab needs View Provider-Patient Messages; flagging a conversation needs Flag Communications (REQ-016-070).
- **Refund threshold**: 1,000 US dollars; other currencies are converted at the rate FR-007 applies to that payment (new REQ-016-221; REQ-016-011, REQ-016-020).
- **Notices**: one sentence in the Communication Structure and in REQ-016-027 says the notices raised by this module need FR-020 events.
- The change log row (1.18) and Last Updated are set.

## Owner defaults applied (plain-language entries 208 to 212 in the defaults report)

Neutral cancellation text (208), Lift Suspension and Unlock Account with the appeal as a support contact (209), removal of Deactivated and archive (210), the permission mapping (211), the US dollar refund threshold (212).

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr016-logic-p1-fixes.yaml`

- New: rules REQ-016-217 to REQ-016-222 and step STP-016-120 (failed cancellation branch); five values added to the audit action_type list.
- Rule statements and titles updated to mirror the PRD; step titles of the suspension and deletion flows, two screen descriptions and three audit field descriptions updated; admin_id and justification are no longer required fields (conditional on system_generated).
- Edges: REQ-016-082 gets the same stage and screen edges as REQ-016-020; Screen 8 shows two FR-023 fields (blocked and jurisdiction flags); the suspension chain gets STP-016-120 between the cancellation and notice steps; the deletion chain skips the retired certificate step. REQ-016-074 and STP-016-117 are retired.
- Cross-FR edges: Screen 8 shows ENT-deletion-request.blocked_by_obligation and .jurisdiction_review_required (FR-023 fields). No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 164 change rows, no errors; the copy was deleted.

## Not changed here

Queued in the logic review ledger section for FR-016: FR-020 (five events), FR-031 (default role matrix check for the mapped actions and the Delete Patients description "Archive patient accounts"), FR-001 (enum value `deactivated` on ENT-patient.account_status), FR-023 (the Needs attention signal has no field). Minor observations from the review are left as they are.
