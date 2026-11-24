# FR-022 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 2.24 to 2.25, with a graph change-set)
**Scope**: FR-022 Search and Filtering
**Source of findings**: `plans/reports/tester-261124-fr022-logic-p1.md` (22 findings; each ruled fix, business default or neighbour-only)

FR-022 only mirrors the search and filter criteria of screens owned by other FRs. Where it disagreed with the owning FR's current rule, list or screen, the owning FR won and FR-022 was corrected.

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`

- **Provider selection (patient app, Screen 7a)**: Country is OR within the selection (REQ-022-066, REQ-022-067). The Active Status control is removed because patients see Active providers only (REQ-022-131). The screen gets a sort control that defaults to the provider search default sort setting and a destination autocomplete for Alternative Flow A3; the Available Capacity filter and sort are out of launch scope because no data source exists (REQ-022-067, REQ-022-130).
- **Main Flow 3**: the flow proceeds with 1 to 5 selected providers, a deselect step is added, and at 5 the remaining cards are blocked (REQ-022-017).
- **Price sort**: sorts by the price after promotion where one applies, otherwise the offered price; the offered price is the price before any promotion (REQ-022-069, REQ-005-050).
- **Admin and provider list filters now match the owner lists**:
  - Payment status uses the FR-007 list on all three screens, with Overdue as a separate flag (REQ-022-087, REQ-022-090, REQ-022-091).
  - Inquiry Stage uses the inquiry stage values; "Scheduled" is removed (REQ-022-087).
  - FR-016 Account Status, Action Type and Request Status follow REQ-016-183, REQ-016-160 and REQ-016-186 (REQ-022-094, REQ-022-095, REQ-022-096).
  - FR-027 Status, Document Type and default Acceptance Status (Pending) follow FR-027, and the Reminder Status and Acceptance Timestamp filters are removed (REQ-022-110, REQ-022-111).
  - FR-031 roles, statuses and permission categories follow FR-031, and the permission search sits on Screen 4 (REQ-022-115, REQ-022-116, REQ-022-117).
  - FR-024 package status includes Draft (REQ-022-080); REQ-022-041 reads Active, Draft or Inactive.
- **Reviews lists**: the provider review list searches by reviewer alias and filters by Treatment, with no Patient or Treatment Case dropdown; the admin review list gains a Treatment filter. The FR-032 Reviews tab points to the FR-013 list for its criteria and adds only the sort (REQ-022-092, REQ-022-093, REQ-022-084).
- **Provider Messages search**: by Patient ID, inquiry or quote ID and message content; patient name only after payment is confirmed (REQ-022-085, REQ-022-026).
- **Name protection**: the rule applies at every stage until payment is confirmed (REQ-022-026).
- **Page size**: one statement. The page-size setting (default 25, range 10 to 100) is the default for admin and provider lists; the owning screen wins where it states its own size or selector (FR-015 at 50, FR-016 selectable 25, 50 or 100, FR-024 at 20); the patient app is fixed at 10 (REQ-022-006).
- **Help search**: FR-035 Hub and Help Center search are server queries at 500ms; Hub search covers FAQs, Articles, Resources and Videos (REQ-022-071, REQ-022-072, REQ-022-132, REQ-035-036).
- **Rate limit and timeout**: Alternative Flow B2 gains an hourly-limit step and a timeout step with one timeout message (REQ-022-025, REQ-022-136).
- **Search audit log**: written for admin searches only, read on the FR-031 audit trail, kept for the same period as the FR-031 admin audit trail (REQ-022-023, REQ-022-027, REQ-022-140, REQ-031-015).
- **Settings**: the page-size and default-sort settings are edited on the FR-026 app settings screens.
- **Housekeeping**: REQ-022-043 now names FR-032 (REQ-032-107) and FR-034 (REQ-034-114) as owners of the support case criteria; the REQ-022-070 priority is corrected; FR-013 Screen 5 and FR-032 Screen 5.7 sit under the provider platform headings.
- The change log row, version and Last Updated are set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr022-logic-p1-fixes.yaml`

- New steps: STP-022-052 (hourly limit), STP-022-053 (timeout), STP-022-054 (deselect a provider). Each is wired into its flow with `next` edges, and two Main Flow 3 edges are relabelled (removed, then added).
- Rule statements and titles updated to mirror the PRD (REQ-022-006, 017, 023, 025, 026, 027, 041, 043, 069, 070, 136, 140 and 19 screen rules); both setting descriptions updated.
- Edges: REQ-022-026 applies at the acceptance and booking stages; the audit log writer edges move from the patient and provider active stages to the admin operations stage, and the configuration stage reads the audit log; REQ-022-116 moves from SCR-031-01 to SCR-031-04; FR-022 references 13 rules owned by FR-005, FR-013, FR-016, FR-027, FR-031 and FR-035.
- Cross-FR edges: added only (references to those FRs' rules, REQ-022-116 applies to SCR-031-04, STG-admin-01-configuration reads the audit log). No node owned by another FR is updated or retired.
- Test-applied on a scratch copy of the graph: no errors; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour changes are queued in the logic review ledger section for FR-022: FR-026 (screen rows for the two settings), FR-031 (whether the audit trail lists the search entry type, and its Screen 5 being per user), FR-006 (own At Risk wording).
