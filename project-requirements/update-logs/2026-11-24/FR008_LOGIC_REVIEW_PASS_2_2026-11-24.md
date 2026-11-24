# FR-008 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 3.3 to 3.4, with a graph change-set)
**Scope**: FR-008 Travel & Logistics Coordination
**Source of findings**: `plans/reports/tester-261124-fr008-logic-p2.md` (16 findings; 13 ruled fixes applied, 1 neighbour-only, 2 wiring or display fixes inside the PRD and graph). This is the final pass; what could not be closed is listed in the logic review ledger under Leftovers.

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`

- **Not needed on the provider and admin views**: Screen 10 Status values and the admin Tab 2 and Tab 3 empty states handle a Not-needed item; it shows "Not needed", is not Awaiting and is not eligible for Re-notify (REQ-008-064, REQ-008-080, REQ-008-081).
- **Screen 5**: in Path B the outbound flight, return flight and hotel rows are always shown, as the record, Awaiting or Not needed (REQ-008-056).
- **No-travel declaration**: Screen 10 shows "Patient declared no travel needed" and the provider is notified when it is made or overridden (REQ-008-059, REQ-008-080). Default recorded for owner review.
- **Replacement booking**: the carry-over also keeps Not-needed marks, the no-travel declaration and an Incomplete passport mark; Screen 11 shows "Carried over from the original booking" for admin review (REQ-008-032). Default recorded for owner review.
- **Path and labels**: the FR-004 `included_services` checklist alone decides the travel path and the Package Travel Items labels; option item names are display detail only (REQ-008-018, REQ-008-044).
- **Overall Status**: when every required Path B item is Not needed the Overall Status is Complete; this stays separate from the no-travel declaration (REQ-008-077). Default recorded for owner review.
- **Incomplete passport**: counts as pending and offers Re-notify patient (REQ-008-060, REQ-008-081).
- **Soft-delete**: the owner of a soft-deleted passport, flight or hotel record receives a notice asking them to enter it again (REQ-008-067, REQ-008-076); the notice needs an FR-030 catalogue entry.
- **Hotel Not needed**: no transportation details are collected (accepted for MVP) (REQ-008-013, REQ-008-083).
- **Travel-date review**: a reschedule on a booking with no flight or hotel records starts no review; submissions and edits stay allowed during a review and the admin still confirms the dates; an early-departure acknowledgment is cleared and asked again when the return flight or hotel check-out is then before the new last treatment plan day (REQ-008-062, REQ-008-031). Default recorded for owner review.
- **Screen 1**: the earlier-passport control is stated as "Use these details" and "Enter new details" (REQ-008-051).
- **Screen 7**: the Graph field column is realigned, one field per row.
- **Provider passport access**: also ends when the booking reaches Completed; flight and hotel stay read-only, admins keep access (REQ-008-050, REQ-008-061). Default recorded for owner review.
- The change log row and the version are set (3.4); Last Updated was already 2026-11-24.

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr008-logic-p2-fixes.yaml`

- New: step STP-008-037 (owner notice after a soft-delete). No node is retired and no edge is removed.
- Edges: STP-008-037 wired from STP-008-019 and back to the entry steps of the re-entered items; the FR-006 cancel step STP-006-303 now has a next edge to STP-008-029, so the closing step is reachable from a plain cancellation; rules REQ-008-028, -049, -051, -080 and -081 attached to the obvious steps; notice and declaration rules attached to STP-008-027 and STP-008-036; SCR-008-10 shows the travel_required field.
- Updates: 17 rule statements, 4 step titles, 4 screen and field descriptions, the overall_status description; the four item status fields now point to REQ-008-064 as the rule defining their values.
- Cross-FR edge: STP-006-303 next STP-008-029 (the FR-006 node is not changed).
- Test-applied on a scratch copy of the graph: 57 change rows, no errors; the copy was deleted.

## Not changed here

- FR-006: the "same travel path" condition on its carry-over text (REQ-006-057 and the transfer step) is queued in the ledger; no FR-006 edit was made.
- FR-030: catalogue entries for the declaration notice and the soft-delete notice are queued in the ledger.
- Owner defaults 213 to 217 are staged for the owner review file; see the staged defaults entries.
- Leftovers (the 18 rules still without a step, other FR-006 cancel routes, the transfer-only edge STP-008-029 to STP-008-030, and the unruled points) are listed in the ledger section; this was the last pass, so no further pass is planned.
