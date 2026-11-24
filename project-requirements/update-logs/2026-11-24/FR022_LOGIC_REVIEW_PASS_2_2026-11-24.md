# FR-022 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 2.25 to 2.26, with a graph change-set)
**Scope**: FR-022 Search and Filtering
**Source of findings**: `plans/reports/tester-261124-fr022-logic-p2.md` (14 findings; 13 fixed, 1 left unchanged; one business decision, taken as recommended)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`

Principle as in pass 1: FR-022 mirrors the owning FR, so each value below was confirmed at the owner's line and FR-022 was corrected.

- **FR-034 Screen 1 (support center)**: Priority is Low, Medium, High, Urgent; Ticket Source (Patient App, Provider Portal, Manual Admin Entry) and Submitter Type (Patient, Provider, Admin) are multi-select; Date Range defaults to Last 90 days; Assigned To, Request Type and Request Status are added; the search also covers phone and description (REQ-022-123).
- **FR-019 Screen 1 (promotions)**: the Status filter no longer offers Pending Approval, which does not exist at program level; the search states its 2-character minimum (REQ-022-106).
- **FR-009 Screens 1 and 10 (team lists)**: Screen 10 is now an admin screen (cross-provider search by provider name, member email or status; filters status Active, Suspended, Invited, role, region) and Role Compatibility is dropped because the owner does not list it (REQ-022-074). The clinic's own team list, FR-009 Screen 1, gets its own entry with name and email search, role and status filters, and the Removed status offered to the Owner only (REQ-022-144, new). The master table, entry points and Executive Summary follow.
- **FR-011 Screens 8 and 13 (aftercare cases)**: Case Status is Pending Activation, Active, Completed, Cancelled, plus a separate Overdue only toggle; Screen 13 also gets an Urgent only toggle (REQ-022-078, REQ-022-100).
- **FR-033 Screens 2 to 5 (help content)**: the Status filter offers Unpublished on all four lists; Article Type adds Policy Information; Resource Category is Templates, Documents, Forms; File Type is PDF, DOCX, XLSX, PNG, JPG; Video Source Type is Upload File or Embed from Third-Party (REQ-022-118 to REQ-022-121).
- **FR-014 Screen 1 (analytics)**: a multi-select Country filter (default all countries) is added and the Benchmarks toggle is removed, because the owner places benchmarks on other screens (REQ-022-079, REQ-022-040).
- **FR-029 (payment configuration)**: Screen 3 gets its provider search by name or ID (REQ-022-146, new); Screen 2A gets its pair list sort and filters by pair name, mode and status (REQ-022-145, new); the Screen 5 search offers only providers with status Active or Suspended that are not already in another active provider-specific scope (REQ-022-112). The master table lists the two new screens.
- **Search audit log**: one scope in every statement, admin searches for patient and provider records only (REQ-022-023). The search type list and REQ-022-027 are unchanged. This is business default 328.
- **Debounce**: searches that run on the server use 500ms (support center, admin conversations, provider and patient messages), as REQ-022-132 states; local filters keep 300ms.
- **One-line alignments**: the FR-006 bookings date filter says appointment date (REQ-022-090); the FR-024 package list purpose no longer says "published" (REQ-022-080).
- Change log row for version 2.26 is added; Last Updated is unchanged (same date).

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr022-logic-p2-fixes.yaml`

- Operations (40): add_node 3, add_edge 15, update_node 19, remove_edge 3.
- New: rules REQ-022-144 (FR-009 Screen 1), REQ-022-145 (FR-029 Screen 2A) and REQ-022-146 (FR-029 Screen 3), each with stage, actor, screen and source edges.
- Updated to mirror the PRD: 19 rules (REQ-022-023, 040, 044, 059, 074, 078, 079, 080, 085, 090, 100, 106, 112, 118 to 123).
- REQ-022-074 moves to the admin platform: its provider stage and provider actor edges are removed and the admin operations stage and platform admin edges added; REQ-022-044 now points to FR-009 Screen 1 instead of Screen 10.
- Edges that touch another FR's node (added only, no node of another FR is updated): REQ-022-144 to SCR-009-01, REQ-022-145 to SCR-029-02, REQ-022-146 to SCR-029-04, REQ-022-044 to SCR-009-01.
- Test-applied on a scratch copy of the graph: 58 change rows, exit 0, the new rules and the moved edges read back as intended; the live graph was not opened for writing and the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

- The hourly-limit and timeout steps stay on the inquiry stage only, because a step carries one stage; recorded as a leftover.
- Neighbour items (FR-009 role compatibility) are queued in the logic review ledger section for FR-022 and are not part of this change. Minor observations and screens not checked are listed under the ledger leftovers.
