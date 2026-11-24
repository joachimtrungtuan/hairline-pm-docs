# FR-014 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 3.21 to 3.22, with a graph change-set)
**Scope**: FR-014 Provider Analytics and Reporting
**Source of findings**: `plans/reports/tester-261124-fr014-logic-p1.md` (18 findings; each ruled fix, neighbour-only or settled by an earlier decision)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`

- **Two meanings of "Confirmed bookings"**: the word keeps its payment-milestone meaning. The booking load figure on Screen 1 B3 and its heatmap is renamed "Scheduled bookings" (appointment on the day, status Confirmed, In Progress, Aftercare or Completed) and no other widget uses it. Confirmed booking = the first successful initial charge of the chosen option (full payment, deposit, or first installment) (REQ-014-116, REQ-014-135, REQ-014-014, REQ-014-017, REQ-014-018).
- **Time range scope**: on Screen 7 only Sections A and B and the GMV and commission tiles follow the time range; fixed-window and snapshot tiles (Screen 1 C4, Screen 4 Widgets 7 and 8, Screen 7 C3 and C4, Screen 12 Widgets 4 and 5) say they ignore it (REQ-014-259, REQ-014-317).
- **Live records versus aggregate**: the Inquiry Queue and the Accepted Quotes drill-down read live records; charts and tiles read the aggregate (REQ-014-318).
- **Payment option split**: Screen 4 Widget 6 counts bookings by the payment option chosen (Full payment, Deposit plus balance, Installment plan), one observation per booking (REQ-014-216, REQ-014-053).
- **Entry points and empty state**: the provider Analytics nav item opens the first of Screens 2 to 5 the role can see and is hidden when none; Screen 1 shows a role only the sections it may see, with an empty state "No analytics available for your role" (REQ-014-314, REQ-014-161).
- **Admin access**: admins have no analytics export in this version, so the FR-031 permission "Export Reports" gates nothing in FR-014; a table in the access rules names the FR-031 permission each of Screens 7 to 13 needs, and the admin nav item opens the first screen the admin may see (REQ-014-315, REQ-014-316, REQ-014-300).
- **Response-time drill-down**: reported per provider only; the drill-downs open the FR-003 provider inquiry list filtered to the inquiries in the period, and "grouped by coordinator" is removed (REQ-014-009, REQ-014-015, REQ-014-183, REQ-014-187).
- **Export**: the button is on Screens 2 to 5 only; Screen 1 has none; a screen with no visible widget cannot be selected in the form (REQ-014-126, REQ-014-127, REQ-014-060, REQ-014-231).
- **Recurring exports**: a configuration whose owner is removed or loses access to every widget is paused and the clinic Owner is notified; a run that fails its final retry sends the configuration owner an in-app notice; any user who can see every widget may edit or delete it (REQ-014-322, REQ-014-323, REQ-014-324, REQ-014-237, REQ-014-238).
- **Workflows**: a cockpit step (Screen 1) before the first provider step, and a Report History step on Screen 6 after the export step; the admin "take action" step now points at the provider league table and activity table (provider flow is 7 steps).
- **No data tier**: a provider with no TTFQ observation is a grey "No data" tier with a text label, kept out of the donut percentages and the scatter; "platform median" on Screen 8 is the Shared Benchmark Rule median (REQ-014-320, REQ-014-065, REQ-014-248, REQ-014-260, REQ-014-261).
- **Growth from zero**: a zero prior period shows "New" when the current count is above zero (above the stated minimum where the widget has one); otherwise N/A (REQ-014-321, REQ-014-084, REQ-014-246, REQ-014-247, REQ-014-279).
- **Revived bookings**: a booking an admin revives from expiry re-enters the accepted-but-unpaid figures and its age counts from the start of its current hold (REQ-014-139, REQ-014-192, REQ-014-217, REQ-014-257, REQ-014-293).
- **Commission and refunds**: commission on refunded money is reversed with the refund, so platform commission and Screen 12 net revenue count money kept; the provider tile is relabelled "Income after commission (before refunds)" with a tooltip that flat-rate commission is recognised at completion (REQ-014-325, REQ-014-214, REQ-014-051, REQ-014-255, REQ-014-290, REQ-014-291, REQ-014-299).
- **Quote metric names**: Dependencies cite REQ-005-018 to REQ-005-020 only; Parent Quote Responses and Subquote Selections are shown; Subquote Comparisons is recorded by FR-005 and not shown in this version (REQ-014-319).
- **Payout widgets**: the payout fields point at the FR-017 payout statement (`ENT-provider-payout`) instead of a payment-level entity.
- **Cancellation and no-show**: both rates use the confirmation cohort, like Screen 11 Widget 1 (REQ-014-313, REQ-014-200, REQ-014-288, REQ-014-282).
- **Cross-reference slips**: the "Entity 7" Payout Record bullet is replaced by a pointer to the FR-017 payout statement, and the missing SC-010 citation now points at Rule 6, the 15-minute pipeline rule.
- A new summary subsection lists the thirteen new rules (REQ-014-313 to REQ-014-325); the change log row and Last Updated are set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr014-logic-p1-fixes.yaml`

- New: rules REQ-014-313 to REQ-014-325; steps STP-014-019 (cockpit) and STP-014-020 (report history).
- Flow start of the provider analytics flow moves to STP-014-019, which continues to STP-014-001; STP-014-005 continues to STP-014-020. The provider step prd_ref values are renumbered.
- STP-014-013 applies the league table and activity table rules instead of the threshold and identity rules.
- Screens 1 and 4 show the `ENT-provider-payout` fields in place of the `ENT-payout` fields; REQ-014-116 no longer applies to Screens 3 and 10, which follow REQ-014-135.
- Rule statements (and a few titles) updated to mirror the PRD; the booking intensity entity description names the Scheduled bookings statuses.
- Cross-FR edges: four rules apply to SCR-003-12 (the FR-003 provider inquiry list). No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 273 change rows, no errors, every step reachable from a flow start; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour changes are queued in the logic review ledger section for FR-014: FR-031 (Export Reports gates nothing in FR-014), FR-020 and FR-030 (the two recurring-export notices), FR-017 and FR-015 (commission reversed with a refund), FR-003 (optional response-time column on the inquiry list), FR-005 (Subquote Comparisons recorded, not shown), FR-006 (revival semantics, age from the current hold) and FR-007 (first-initial-charge wording, already settled there).
