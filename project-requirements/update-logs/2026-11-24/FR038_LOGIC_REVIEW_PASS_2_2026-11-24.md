# FR-038 Logic Review Pass 2 (2026-11-24)

**Scope**: FR-038 Monitor Transplant Progress, PRD v1.5 to v1.6. Pass 2 (the last pass) of the logic review; 18 findings, all accepted or ruled. All 18 fixed in FR-038, several with a neighbour row queued to FR-037, FR-011 and FR-030.
**Evidence**: reviewer report `plans/reports/tester-261124-fr038-logic-p2.md`; fixer report `plans/reports/docs-manager-261124-fr038-logic-p2-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr038-logic-p2-fixes.yaml` is prepared and NOT applied (the controller applies it).
**Owner defaults**: numbers 101 to 104 as ruled by the controller for this pass (End Monitoring with an open draft; previous cases on the home card; Admin cannot edit case status; reminder schedule from case creation); the owner-review defaults report is the controller's to update.

## Changes to the PRD

- Monitoring Period starts at the earlier of the case creation date and the earliest log date; the trend is in date order with the Initial Severity plotted on the case creation date (REQ-038-034, REQ-038-035). A case with no log shows the Initial Severity as first, latest, minimum, maximum and average with a one-point trend.
- Screen 6 no longer cites retired REQ-038-074. After a failed or abandoned request the patient returns to Screen 6 with the draft intact and corrects copied fields there (REQ-038-068, flow B2). Screen 6 gains a conditional Retry PDF row, and flow A2 a step 2a (REQ-038-041). The export-ready notice opens Screen 6 only while the draft is open, otherwise Screen 7 (REQ-038-064).
- The patient may end monitoring while a conversion draft is open; completion discards the draft and a later request creation is refused (REQ-038-037, REQ-038-044, Rule 5, Screen 2). The idempotency key is created once per case at the first Switch and kept when the draft is cleared (REQ-038-016).
- The home card also lists previous completed and converted cases, each opening its read-only Screen 7 (REQ-038-062, Entry Points).
- Screen 4 also opens from the Screen 6 retake; a scan captured from Screen 1 is held with the intake draft and saved when the case is created (REQ-038-049).
- The Admin cannot edit case status; completed and converted are final (REQ-038-055, Screen 9, Admin Editability).
- A file or PDF that fails the malware scan is rejected or ends as failed (REQ-038-077). The default reminder schedule runs once a month for 12 months from the case creation date (REQ-038-031).
- Main flow: the separate check step is folded into the entry branch of step 1 (otherwise flow B1) and the steps are renumbered 1 to 7.
- Rule texts changed in the PRD with the same wording in the graph; the change log row records 1.6.

## Graph change-set (prepared, not applied)

- 53 operations: 11 edges removed, 27 node updates (13 rules, 6 rules with a rationale-only change, 7 steps, 1 setting), 15 edges added; no new node, field, enum value or event.
- Wiring: the failure edge moves from STP-038-055 to STP-011-009 (next STP-038-051); conditions added on the three unconditional sibling next edges; STP-038-043 next STP-038-006 and STP-038-011; STP-038-053 next STP-038-006; STP-038-022 next STP-038-057 next STP-038-054 with STP-038-057 on SCR-038-06; STP-038-021, -053, -056 apply REQ-038-037; the stale REQ-011-046 reference and the leftover edges of retired REQ-038-065 and REQ-038-074 removed; the Screen 9 status edge is no longer editable.
- Applied to a scratch copy of the db (56 change rows, no error), then the copy was deleted. Every active non-start FR-038 step has an incoming next from an active step; the only steps without one are the flow starts STP-038-021 and STP-038-059. lint.py was not run (the controller lints after applying).

## Cross-FR rows queued

FR-037 (calculation rules for the monitoring period and severity values; storage field for the idempotency key), FR-030 (REQ-030-225 reminder anchor; export-ready notice target), FR-011 (failure landing on FR-038 Screen 6; refusal of a request created after completion), and the stage join to FR-038 conversion. The rows are in the logic-review ledger section for FR-038 pass 2.
