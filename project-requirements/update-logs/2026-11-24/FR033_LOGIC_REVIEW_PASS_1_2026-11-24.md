# FR-033 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 2.4 to 2.5, with a graph change-set)
**Scope**: FR-033 Help Centre Content Management
**Source of findings**: `plans/reports/tester-261124-fr033-logic-p1.md` (14 findings; each a ruled fix; five carry a recorded default)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr033-help-centre-management/prd.md`

- **Upload size limit**: stated per upload kind (resource file 50MB whatever its type, uploaded video 500MB, resource thumbnail 1MB, video thumbnail 2MB, image placed inside article or FAQ text 10MB) in the flows, the screens, the fixed-in-code list and the edge case (REQ-033-010, REQ-033-041, REQ-033-057).
- **Helpful vote**: covers FAQs, articles, resources and videos; each tap is one anonymous vote, so repeat votes count; read-only Helpfulness Rating rows added to the resource screens and their patient mirror (REQ-033-087, new REQ-033-096).
- **Views and downloads**: a view of an FAQ, article or resource is counted each time its detail is opened, for both audiences; videos keep the 30-second rule; a resource download counts for both audiences; views are stored with their date (new REQ-033-097).
- **Video publish gate**: an uploaded video cannot be published until processing is Ready (embedded videos exempt); a failed processing sets the new status Failed, the admin is told and can re-upload, and the item stays Draft; A4 now processes before it publishes (REQ-033-077).
- **Virus scan**: a failing file is rejected, not stored, reported to the admin with a fixed message and written to the audit trail; one step added to B2 (new REQ-033-098).
- **Required fields**: the same check on Save as Draft and on Publish, with the real required fields per content kind in place of "category" (REQ-033-056, B1, REQ-033-065, REQ-033-070).
- **Resource category**: its own optional field with Templates, Documents and Forms; "and similar" removed (REQ-033-072).
- **Status moves**: the only way out of Published is Unpublish with its reason; the dropdown offers Draft and Published and is read-only while Published; allowed moves listed (new REQ-033-099, General Rule 4).
- **Restore**: admin-only Archived filter on each content list and a Restore action that returns the item as Draft; Related Content links removed at deletion are not put back; new flow A7 (new REQ-033-100, General Rule 6).
- **Versions**: created on save, not when the editor opens; with two admins editing, the last save wins and both saves are versions (REQ-033-054, A2).
- **Overall service status**: calculated from active component statuses only; incidents and maintenance in progress do not change it; a single Down component is Major Outage; "Status not available" with no active component unless set by hand; maintenance status changes only by admin action (REQ-033-080, REQ-033-084).
- **Patient audience**: content reaches the patient Help Centre within 1 minute (REQ-033-034, REQ-035-028); patient Article Type values are Tutorial Guide and Troubleshooting Tip, and Policy Document is provider-only (REQ-033-036, REQ-033-005).
- Change log row and Last Updated are set.

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr033-logic-p1-fixes.yaml`

- New: rules REQ-033-096 to REQ-033-100; steps STP-033-164 (patient propagation), STP-033-165 (virus scan rejection), STP-033-166 (restore); field ENT-help-centre-content.resource_category with three enum values; enum value `failed` on processing_status.
- Updated: 16 rule statements (some titles) and 5 step titles to mirror the PRD; `calculated_by` of helpfulness_rating set to REQ-033-096.
- Rewired: STP-033-020 retired and STP-033-019 reconnected to STP-033-021; video steps reordered to process then publish; the Resource Category screen rows moved from `topic` to `resource_category`; `on` edges added to the 14 steps that had none; applies edges added for rules that had no step (022, 029, 058, 067, 085, 093, 099, 098, 034, 008, 026).
- The already retired field `category` has its enum values retired and is made not required. REQ-033-089, 090 and 091 are retired and get no edge.
- Cross-FR edges: STP-033-164 on SCR-035-02 and applies REQ-035-028; nine FR-033 steps are put on FR-032 screens. No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 230 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes for FR-032 (Resource Library filter screen row still maps to `topic`; counter rules for FAQ, article and resource views) and FR-035 (REQ-035-028 wording; how a vote and a view are written) are queued in the logic review ledger section for FR-033, not applied. view_count and download_count keep their FR-032 calculating rules; REQ-033-097 only applies to them. Minor observations from the review are left as they are and listed under the ledger leftovers.
