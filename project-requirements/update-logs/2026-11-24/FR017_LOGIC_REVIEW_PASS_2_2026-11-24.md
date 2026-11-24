# FR-017 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 2.19 to 2.20, with a graph change-set)
**Scope**: FR-017 Admin Billing and Financial Management
**Source of findings**: `plans/reports/tester-261124-fr017-logic-p2.md` (9 findings, all ruled fixes; three had a business decision: a bank charge, voiding an Approved statement, the clinic share of a cancellation fee; all taken as recommended)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`

- **Interrupted treatment**: the payout hold of a booking In Progress ends when the FR-006 route the admin chose completes, not through the Screen 7 outcomes, which stay for Completed bookings only. The refund set in the FR-006 decision is taken from the held payout, a shortfall becomes a clinic balance entry, and the rest is released (Rule 19, REQ-017-185, REQ-017-190, Alternative Flow B4, edge case).
- **Bank charge**: a bank charge on a manual transfer is carried to the clinic's next payout as a clinic balance entry and is never deducted from the statement being marked as paid. Screen 3 (adjustment type, Mark as Paid note, bank charge row), Release Rule 3, the main flow steps 15 and 16, REQ-017-176 and REQ-017-188 now agree with Alternative Flow B5 and Release Rule 9 (default 312).
- **Cancellation fee share**: the clinic's share of a retained patient cancellation fee is an earning with no confirmation window, released into the next payout; the treatment amount of a cancelled booking and provider-fault cancellations stay excluded and carry no share. New REQ-017-200 in Release Rule 7, with Rule 13, the Screen 2 inclusion rule and the entry points aligned (default 314).
- **Manual Review Required**: set on either rail by the payout flag of REQ-017-161 (a payout over 2x the clinic's average), and on a Stripe Connect payout also by three failed attempts. Clear Manual Review is offered on a statement as well; a cleared statement returns to its earlier state and a cleared Stripe Connect payout returns to Failed, so Retry Payout applies (REQ-017-161, REQ-017-194, REQ-017-177, REQ-017-066, Screen 2, Release Rule 4, Security considerations).
- **One-off statement of Release Earnings**: created Approved (the admin's release is the approval), outside the weekly cycle, paid with Mark as Paid (REQ-017-193, Screen 7, Alternative Flow B4).
- **Void after the payout day**: an Approved statement past its payout day may be voided with a mandatory reason and an audit entry; its bookings return to the next cycle's statement. Unapprove stays limited to before the payout day (REQ-017-068, Screen 2, main flow step 12a; default 313).
- **Clinic balance entry**: Entity 9 lists its attributes (entry type, clinic, source booking or payout, signed amount, state, applied-to payout, write-off reason, created at); Clinic Balance is added to the audit Affected Entity filter (REQ-017-191, REQ-017-192).
- **Pay Now**: on Screen 7, for a Stripe Connect clinic Target Payout Cycle is hidden and Add to Next Payout is replaced by Pay Now, which starts a direct per-booking payout; Confirm Already Paid and Escalate Technical Investigation stay. New REQ-017-201.
- **Wording**: the Carry-Forward Adjustment row no longer says it is a balance record entry.
- Change log row for version 2.20 is added; Last Updated is unchanged (same date).

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr017-logic-p2-fixes.yaml`

- New: rules REQ-017-200 and REQ-017-201; steps STP-017-100 to STP-017-106 (interrupted-treatment hold and exit, cancellation fee share earning, payout flag check, manual-rail clearing exit, Pay Now, void after the payout day); seven fields of ENT-clinic-balance-entry with two enums; enum values clinic_balance (audit affected entity type) and pay_now (dispute resolution action).
- Updated to mirror the PRD: 14 rule statements (two with new titles), 6 step titles, 2 screen descriptions.
- Wiring: STP-017-056, STP-017-091 and STP-017-092 now have onward steps; STP-017-096 has inbound steps (STP-017-086 and STP-017-101); STP-017-100 and STP-017-102 are extra starts of the per-booking payout flow.
- Removed edges: STP-017-087 applies REQ-017-185; STP-017-087 next STP-017-088, STP-017-080 next STP-017-081 and STP-017-095 next STP-017-044 (all three re-added with new labels or conditions).
- Cross-FR edges: none. No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 212 change rows, no errors; no unreachable FR-017 step; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour wording that may follow (FR-014 payout history for voided and one-off statements, FR-030 notices for Pay Now and a voided Approved statement, FR-031 audit entity type Clinic Balance) is queued in the logic review ledger section for FR-017 pass 2; those rows are inferred from what FR-017 now adds, not read in the neighbour PRDs. FR-006 and FR-007 need no wording change. Minor observations, the open commission question on the cancellation fee share, the missing admin control that raises the payout flag, and whether Mark as Paid is blocked while a statement is flagged are listed under Leftovers there.
