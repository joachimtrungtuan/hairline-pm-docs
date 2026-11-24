# FR-034 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 2.8 to 2.9, with a graph change-set)
**Scope**: FR-034 Support Center and Ticketing System
**Source of findings**: `plans/reports/tester-261124-fr034-logic-p1.md` (19 findings; each ruled fix, neighbour-only or settled by another PRD)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr034-support-center-ticketing/prd.md`

- **Escalation destination**: an escalated case always goes to a Super Admin. When Escalate is ticked, New Assignee lists active Super Admin users only, and the escalation notice goes to the chosen Super Admin; the "technical team" wording is gone (REQ-034-092, REQ-034-103, REQ-034-144).
- **System escalation**: one new flow (A7) for an overdue Urgent or High case: the case is marked escalated on its timeline and all Super Admins get the notice; no reassignment and no priority change; the High clock restarts on any status change; the fixed 1-hour Urgent alert goes to the Support Staff pool (REQ-034-155, REQ-034-173).
- **Resolution time**: Rule 12 now says "target", matching the graph (REQ-034-077).
- **Status routes**: Status is Open on create and not editable on Screen 2 when a case is edited; Update Status offers Open to In Progress only; Resolved only through Resolve Case, Closed only through Close Case, Closed to Open only through Reopen Case; main flow step 16 uses Resolve Case (REQ-034-102).
- **Booking requests from a booking screen**: one new flow (A8); Request Type and Request Status are filters on Screen 1 and Request Type, Request Status, Decline Reason, Outcome and Booking Reference are read-only on Screen 3; declining and recording the outcome stay in FR-016 Screen 9; a case whose request status is Open cannot be Resolved until the request is completed or declined (REQ-034-055, REQ-034-174).
- **Permissions**: REQ-034-094 and REQ-034-042 are written on the FR-031 names (View Support Center reads; Respond to Support writes; Super Admin only for Screen 7, receipt of escalations and audit export); assignee lists are active admins with Respond to Support; a user without View Support Center who sees the case in FR-016 Screen 9 gets the reference without a link (REQ-034-126).
- **Account interventions**: A2 and A6 state that the intervention needs the permission FR-016 requires (Edit Patients, Edit Providers) and that an admin without it escalates to a Super Admin; A2 now lists suspend account and lift suspension in step 3 (REQ-034-180).
- **Provider reply route**: REQ-034-139 names FR-032 Screen 5.8 for provider replies.
- **Provider reopening request**: one new flow (B3a): a provider can only ask; the request is a flagged message, the case stays Closed, the assigned admin or the pool is told through the user-reply notice, and an admin decides with Reopen Case (REQ-034-178).
- **Problem report details**: Screen 3 shows Device, Operating System and App Version read-only; REQ-034-164 names the Technical Issue preset and the 10 per hour per patient limit; provider submissions are limited to 10 new cases per hour per provider user (REQ-034-164, REQ-034-176).
- **Response target**: confirmation texts say "within 24 hours on business days"; new Rule 21 states the first-response target (Monday to Friday, UTC, target only) (REQ-034-098, REQ-034-175).
- **Patient reopen by email**: B3 step 1 says the email carries the case ID in the subject and the admin finds the case by that ID; when the support email setting is empty there is no email route and the patient creates a new ticket (REQ-034-177).
- **A5 start**: A5 steps 1 to 3 start at the Hub "Contact Support" row, hand the form to FR-035 Screen 5, and receive the submission; the numbering stays so the FR-035 pointer to step 11 holds.
- **Scanner unavailable**: one new flow (B4a): the file is refused with a "try again later" message and the case, reply or note can be saved without it (REQ-034-044).
- **Category visibility**: each built-in category carries a fixed Visible To value shown read-only on Screen 7, with one membership table; A3 and A5 step 6 say "categories visible to providers/patients" (REQ-034-101).
- **Deleted patient**: no email of any kind to a deleted patient; the email boxes on Screens 4 and 6 are unchecked and disabled; the case goes to Resolved with a summary and then Closed; anonymisation follows FR-023 (REQ-034-109).
- **No Patient Link**: Screen 2 gets the checkbox, a required Contact Email and an optional Contact Name stored on the case; replies, the confirmation and the resolution email go to that address (B1, REQ-034-179).
- **Inactivity warning**: applies to Open and In Progress cases only; activity means any reply, note, status change or reassignment (REQ-034-058, REQ-034-078).
- The change log row (2.9) and Last Updated are set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr034-logic-p1-fixes.yaml`

- New: rules REQ-034-173 to REQ-034-180; flows FLW-034-system-escalation, FLW-034-booking-request-from-booking-screen, FLW-034-provider-reopening-request, FLW-034-scanner-unavailable; steps STP-034-103 to STP-034-116.
- New fields on ENT-support-case: booking_reference, device, operating_system, app_version, contact_email, contact_name; on ENT-support-case-message: is_reopen_request; on ENT-support-case-reopening: reopened_by_type; on ENT-support-case-category: visible_to (with its values).
- Updated: statements of 18 rules to mirror the PRD, 16 step titles, request_status, reopened_by_admin_id and new_priority no longer required; no edge removed.
- Cross-FR edges (all start at FR-034 nodes, no other FR's node is updated): references to FR-016, FR-023, FR-031 and FR-035 rules; steps on SCR-006-02, SCR-016-09, SCR-032-18; two rules applying to SCR-032-17 and SCR-032-18; one rule governed by the support email setting; one rule applying to the escalation event.
- Test-applied on a scratch copy of the graph: 416 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes for FR-030 (escalation recipient wording, event description), FR-016 (origin shown by Request Type, Screen 9 case reference without a link), FR-032 (Screen 5.8 reply for Resolved cases and banner text, Screen 5.9 must not change status, first-response wording) and FR-035 (pointer to the new first-response rule) are queued in the logic review ledger section for FR-034, not applied. Minor observations from the review are left as they are and listed under the ledger leftovers.
