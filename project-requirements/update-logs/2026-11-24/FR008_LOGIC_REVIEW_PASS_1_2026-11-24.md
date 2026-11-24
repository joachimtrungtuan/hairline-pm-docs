# FR-008 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 3.2 to 3.3, with a graph change-set)
**Scope**: FR-008 Travel and Logistics Coordination
**Source of findings**: `plans/reports/tester-261124-fr008-logic-p1.md` (13 findings; all fixed in FR-008, two of them also queued for neighbour FRs)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`

- **Replacement booking after a provider-fault transfer**: the passport carry-over and the flight and hotel copy apply only when the replacement's travel path (A or B) matches the original's. Items carried over are not requested again; the normal initial requests go out only for items not carried over. If the paths differ, nothing is carried over, the replacement starts `active` and the normal requests for its own path are sent (REQ-008-032, REQ-008-005, REQ-008-034).
- **Overall Status**: required items per path. Path A is the passport plus each of flight and hotel that the accepted option includes. Path B is the outbound flight, return flight and hotel, except items marked Not needed. A booking marked `no_travel_required` is Complete (REQ-008-077).
- **Passport marked Incomplete**: an admin marks a submitted passport Incomplete from the Screen 12 passport tab with a mandatory reason, and the patient is notified. The mark clears when the patient submits one new passport or an admin correction is saved (REQ-008-065, REQ-008-052).
- **Flight and hotel re-entry**: after an admin soft-delete the status returns to Awaiting and the item's owner (provider in Path A, patient in Path B) enters one replacement; until then the item counts as not submitted (REQ-008-067).
- **Not needed in Path B** (default for owner review): the patient can mark the outbound flight, the return flight or the hotel Not needed, one item at a time, recorded with time and actor; such an item is not required and Re-notify is not offered for it. The all-or-nothing no-travel declaration stays (new REQ-008-083; Screens 2 to 6, 11 and 12).
- **Admin actions placement**: Re-notify, Confirm Travel Dates and the new "Override no-travel declaration" action sit on the Screen 11 Travel section; Apply Correction and the Incomplete mark stay on Screen 12 (REQ-008-059, REQ-008-060).
- **Travel-date review trigger**: named as the FR-006 `booking.rescheduled` event (REQ-006-011), sent when the admin appointment change is confirmed (REQ-008-062, REQ-008-028).
- **Notices**: every travel notice is an MVP notice that needs an FR-030 catalogue entry (REQ-008-071). There are no automatic reminders at MVP; the only follow-up after the initial request is the admin's manual Re-notify (REQ-008-060, REQ-008-058, REQ-008-028).
- **Provider access on closed bookings** (default for owner review): when a booking is cancelled or closed by a provider-fault transfer, the original provider loses access to the passport record; flight and hotel details stay read-only for them; admins keep access (REQ-008-050, REQ-008-061).
- **Package Travel Items**: names come from the accepted option's included-services list saved at confirmation, in a new optional text-list field `included_services_labels_snapshot` (REQ-008-044; Screen 5).
- **Travel section placement**: the patient entry, the provider section and the admin section sit in FR-006 Screens 2, 4 and 6 (Screens 5, 6 and 11 now say so).
- **Hotel mapping**: `hotel` in `included_services` is the FR-004 `accommodation` item type; a provider who includes it puts the booking on Path A (REQ-008-018).
- Acceptance scenarios 5 and 9 reworded; scenarios for a differing replacement path and for a Not-needed item added. Dependencies now name FR-030. The audit action list names the Incomplete mark and the Not-needed mark. Change log row and Last Updated set (header and footer).

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr008-logic-p1-fixes.yaml`

- New: rule REQ-008-083; steps STP-008-034 (admin marks the passport Incomplete), STP-008-035 (admin re-notifies), STP-008-036 (admin overrides the no-travel declaration); field `ENT-travel-context.included_services_labels_snapshot`; enum value `not_needed` on the three flight and hotel status fields; audit action values `mark_incomplete` and `mark_not_needed`.
- Edges: the new steps are wired into the flows (STP-008-018, STP-008-021, STP-008-025 and STP-008-027 next edges), STP-008-020 is also placed on SCR-008-11, the hand-off steps STP-008-021 and STP-008-025 apply REQ-008-032, and SCR-008-05 shows the new label field in place of the old one (one edge removed).
- Rule statements (16 rules) and five step titles updated to mirror the PRD.
- Cross-FR edges: `FR-008 references REQ-006-011` (the node is owned by FR-006 and not changed). No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 91 change rows, no errors; the FR-008 lint run reported no findings; the copy was deleted.

## Not changed here

- FR-006: add a Travel section or entry to booking detail Screens 2, 4 and 6 (queued in the logic review ledger).
- FR-030: add catalogue entries for the FR-008 notices (queued in the ledger).
- Open for the owner: whether a Not-needed mark can be reversed, closed-booking Overall Status, Path A one-way flights, and the link from the FR-006 travel review notice step to FR-008 (see the ledger leftovers).
