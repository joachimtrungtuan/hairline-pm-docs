# FR-014 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 3.22 to 3.23, with a graph change-set)
**Scope**: FR-014 Provider Analytics and Reporting
**Source of findings**: `plans/reports/tester-261124-fr014-logic-p2.md` (9 findings, all ruled fixes; three had a business decision, all taken as recommended)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`

- **Active cash risk is a snapshot everywhere**: Screen 1 C3 joins the fixed-window list and ignores the time range filter, so it always shows the same total as Screen 4 Widget 7 and Screen 12 Widget 4; the time-scoping sentence is removed from the cash-at-risk rule (REQ-014-317, REQ-014-139, REQ-014-192).
- **Recurring export owner**: the configuration records its owner, the user who last saves an edit, and a generated report records the user it was generated for. A configuration paused because its owner was removed or lost access cannot be resumed until an eligible user saves an edit; Resume is unavailable on Screen 6 meanwhile (REQ-014-322, REQ-014-324, REQ-014-232, Entity 8).
- **Payouts waiting for clinic setup**: shown to providers as Upcoming with the note "Payout setup incomplete" and a link to the payout setup in provider settings; the Screen 12 W5 status list and its 30-day total include them (REQ-014-218, REQ-014-294; business default 325).
- **Fixed windows on Screens 7 and 8**: Screen 8 Widgets 3 and 5 and the Screen 7 Tile 5 Dormant count keep their own windows and ignore the time range filter; Tile 5 uses the Screen 8 Widget 3 Dormant definition, stated once and cited by both (REQ-014-317, REQ-014-249, REQ-014-259, REQ-014-262, REQ-014-264).
- **"No data" tier filter**: Screen 8 offers No data as a TTFQ health tier filter option, and the Screen 7 Tile 4 No data count opens it (REQ-014-320, REQ-014-248).
- **Inquiry drill-downs**: each opens the FR-003 provider inquiry list with the stage, country and period of the clicked element pre-applied (REQ-014-008, REQ-014-014, REQ-014-022, REQ-014-195, REQ-014-197, REQ-014-199, A1 flow).
- **Admin Screen 7 permissions**: an admin sees only what the admin's permissions cover; financial tiles need the permission that opens Screen 12, and a drill-down link appears only when the admin may open its destination; otherwise the tile shows its value without a link, or is hidden when its data is financial. New rule in Rule 15G and a note on Screen 7 (REQ-014-326; business default 326).
- **Provider financial permissions**: where the matrix says "Only with financial permission", View Financial Dashboard gates income and revenue widgets, View Payouts gates payout widgets and payout history, and View Financial Reports gates financial exports; a table is added under Rule 15F (REQ-014-161, REQ-031-118; business default 327).
- **Role-aware entry**: Main Flow step 2 says steps 3 to 5 apply only to the screens the role can see (REQ-014-314).
- **One-line alignment**: the export generation time on Screen 6 now says PDF under 60 seconds, CSV under 30 seconds, as Rule 18 does (REQ-014-169).
- Change log row for version 3.23 is added; Last Updated is unchanged (same date). Screen 1 is layout locked: only the C3 snapshot note and drill-down destination wording changed there.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr014-logic-p2-fixes.yaml`

- New: rule REQ-014-326; fields ENT-export-report-config.owner_user_id and ENT-analytics-generated-report.generated_by_user_id (both id). No new step.
- Updated to mirror the PRD: 24 rule statements, 2 entity descriptions, the Screen 8 description (TTFQ tier filter).
- Edges: REQ-014-326 wiring; STP-014-006 applies REQ-014-316 and REQ-014-326; STP-014-001 to STP-014-005 apply REQ-014-314; REQ-014-317 applies to SCR-014-08; REQ-014-232 and REQ-014-322 to 324 apply to ENT-export-report-config.
- Removed edges: none.
- Cross-FR edges (edge only): REQ-014-008, 014, 022, 182, 186, 189, 195, 197 and 199 apply to SCR-003-12 (the FR-003 provider inquiry list). No other FR's node is updated.
- Test-applied on a scratch copy of the graph: 75 change rows, no errors, all 20 active FR-014 steps still reachable through next edges from the flow starts; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour changes for FR-003 (the provider inquiry list needs a stage filter and must accept a pre-applied period and country), FR-031 and FR-009 (check the provider financial permission mapping against the FR-014 split) and FR-017 (a Connect payout has a release date, not a Period) are queued in the logic review ledger section for FR-014 and are not part of this change. Minor observations from the review are left as they are and listed under the ledger leftovers.
