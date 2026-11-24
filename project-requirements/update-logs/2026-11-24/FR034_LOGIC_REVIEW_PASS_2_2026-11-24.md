# FR-034 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 2.9 to 3.0, with a graph change-set)
**Scope**: FR-034 Support Center and Ticketing
**Source of findings**: `plans/reports/tester-261124-fr034-logic-p2.md` (11 findings; all ruled fixes, five of them owner defaults 244 to 248)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr034-support-center-ticketing/prd.md`

- **System escalation flow**: the missing Alternative Flow A7 is written out (an Open or In Progress case reaches the Urgent or High threshold; the case is marked escalated on its timeline and all Super Admins are told; assignee and priority are unchanged). REQ-034-173 to REQ-034-182 are now listed in the FR summary, and the Screen 3 "Case Escalated" timeline entry is split into the manual and the system case (REQ-034-103, REQ-034-173).
- **Escalation clocks**: both are stall alarms that run only while a case is Open or In Progress. The Urgent clock starts when a case is Urgent and unassigned (at creation or later) and stops on assignment; the High clock starts when a case is High and restarts on any status change; each escalates once per start, with no repeat. Screen 7 threshold rows say the same (REQ-034-155, REQ-034-173).
- **Manual escalation priority**: never lowers the priority; the admin picks High or Urgent from values at or above the current one, an Urgent case stays Urgent with no choice shown, and the value is written to the case priority and shown on the timeline (REQ-034-103, A1 steps 4 and 6, Screen 5).
- **Three plain system emails with a recipient**: the Urgent 1-hour alert (Support Staff pool), the orphaned-case notice (Support Staff pool, as REQ-034-108 already said) and the manually-contact alert after exhausted retries (the assigned admin, or the pool when unassigned) (REQ-034-092, REQ-034-108, REQ-034-113, Notification Rule 3, Edge Cases).
- **Support Staff pool**: defined once in Authorization as all active admin users who hold Respond to Support (REQ-034-094).
- **Admin Editability**: status removed from the list; status changes follow REQ-034-102 (REQ-034-086).
- **Filter Bar**: default date range 90 days, and the Request Type and Request Status filters listed (REQ-034-116; the graph statement also lost a stray table-row fragment).
- **Bulk Assign**: opens the Screen 5 modal once for all selected cases with one new assignee and one required reason; only Open and In Progress cases are included and the skipped count is shown; no Escalate in bulk; each case gets the normal assignment notice and timeline entry (REQ-034-119).
- **Reopen Case on Resolved cases**: an admin can reopen a Resolved case directly, with a required reason, the auto-close timer cancelled, the case returning to Open, no reopening request involved and the normal reopened notice. Screens 1, 3, 6, flow B3, Rule 3 and REQ-034-102 aligned (new REQ-034-181).
- **No Patient Link**: every notice that would go to the patient goes to the contact email (REQ-034-179, Screen 2, flow B1).
- **Blocked booking screens**: Contact Support on the Payment Window Expired and Cancelled screens creates a plain case that carries the booking reference and no request type; only cancellation and change requests carry a request type (A8, new REQ-034-182, REQ-034-167).
- Version 3.0, one change-log row, Last Updated 2026-11-24.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr034-logic-p2-fixes.yaml`

- New: rules REQ-034-181 and REQ-034-182, with their `decided by`, `applies at`, `applies to` edges; STP-034-093 and STP-034-095 apply REQ-034-181.
- Updated: 13 rule statements to mirror the PRD (REQ-034-086, 092, 094, 102, 103, 108, 113, 116, 119, 145, 155, 173, 179), 5 step titles, 2 setting descriptions, 2 field descriptions and 1 screen description. REQ-034-167 already says request types apply only to cancellation and change requests, so it is unchanged.
- No edge removed, no node retired. EVT-support-case-escalated is not touched (FR-030 owns it).
- Cross-FR edge: REQ-034-182 applies to SCR-006-01 (FR-006 screen, edge from an FR-034 node). No other FR's node is updated.
- Test-applied on a scratch copy of the graph: 47 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes for FR-006 (Contact Support on the two blocked booking screens carries the booking reference and no request type), FR-035 (the form must pass the booking reference) and FR-030 (three catalogue events for the three plain emails) are queued in the logic review ledger section for FR-034 pass 2. Minor observations are listed there under Leftovers and are not fixed.
