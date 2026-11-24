# FR-037 Logic Review, Pass 1 (2026-11-24)

## Scope

Applies the triaged logic-review fixes (28 findings) to the FR-037 Monitor Hair Loss PRD and records the matching requirements-graph change-set. PRD version 2.3 becomes 2.31.

- PRD: `local-docs/project-requirements/functional-requirements/fr037-monitor-hair-loss/prd.md`
- Graph change-set: `local-docs/project-requirements/graph/changesets/2026-11-24-fr037-logic-p1-fixes.yaml` (written and test-applied on a scratch copy only; not applied to the live graph)

## What changed in the PRD

- **Scan and conversion contracts:** one FR-002 media-only call per saved scan; staged photos removed after 7 days; a scan set that fails the quality check cannot be saved; conversion photo items are `{ scanRef, photoIndex }` references, copied and never moved; the case stays untouched until the FR-003 inquiry submission succeeds and Step B ends in a hand-off; one idempotency key per case; completion discards an open draft.
- **Summary calculation:** monitoring period starts at the earlier of the case creation date and the earliest log date; trend in date order; Initial Severity (renamed from Current/Starting Severity) is the first trend point; zero logs shows no entries; deleted and superseded entries are excluded from counts and the trend.
- **Scope and status:** reminders are limited to transplant-progress cases (FR-038, REQ-038-031); Admin list covers hair-loss cases only; completed and converted are final and Admin cannot edit status; advice state and case status are labelled separately on Screens 2, 8 and 12.
- **Advice and assignment:** an edit of posted advice sends the same advice notification marked "updated"; only the author may edit, and only while assigned; cadence is the spacing of window openings, windows pause while no provider is assigned, dates are UTC; an assignment ends by withdrawal, Admin ending it with a reason, or automatically on FR-015 suspension or deactivation, returning the case to Pending Reassignment; previews are revoked on assignment, completion and conversion and the case leaves the Admin queue on completion or conversion.
- **Screens:** Retry PDF on Screen 6; continue without the PDF after three failed tries on Screen 7 Step A; End Assignment action on Screen 12; advice count removed from the Screen 7 recap; Screen 5 confirmation shown for Complete and export only.
- **Exclusivity:** every way exclusive routing ends is listed, citing REQ-003-072.

## What changed in the graph (change-set only)

- Nine new FR-037 steps (STP-037-046 to 054) and one new field (ENT-monitoring-case.reminder_preference).
- Reworded rule statements mirror the PRD text; assignment status becomes an enum (active, withdrawn, ended); ENT-monitoring-scan.quality_state is retired; starting_severity is retitled Initial severity.
- Step wiring: provider steps 011 and 012 re-sourced from 010; Screen 10A attached; missing next edges added; boundary edges into FR-003 corrected.
- Cross-FR edges: STP-003-014 to STP-037-043, STP-015-152 and STP-015-174 to STP-037-050, STP-037-041 to STP-003-003, STP-037-044 to STP-003-066, STP-037-045 to STP-003-020, and FR-037 references to REQ-002-038, REQ-002-047, REQ-002-051, REQ-003-072, REQ-038-031.
- The change-set test-applied cleanly on a scratch copy (175 change rows); the copy was deleted.

## Not changed here (queued for neighbour FRs)

FR-003 (STP-003-065 ownership and title, decline-step link, conversion-origin inquiry intake, "summary pending"), FR-020 and FR-030 (provider_assigned initial only; advice-posted event description, owned by FR-030), FR-015 (suspension and deactivation cascade), FR-038 (Reminder Preference control tie-in).
