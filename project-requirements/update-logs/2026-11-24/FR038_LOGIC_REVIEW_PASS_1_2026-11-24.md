# FR-038 Logic Review Pass 1 (2026-11-24)

**Scope**: FR-038 Monitor Transplant Progress, PRD v1.4 to v1.5. Pass 1 of the logic review; 18 findings, all accepted. 16 fixed in FR-038 (several with a neighbour row queued) and 2 (P1-13, P1-17) queued to FR-020, FR-030 and FR-003.
**Evidence**: reviewer report `plans/reports/tester-261124-fr038-logic-p1.md`; fixer report `plans/reports/docs-manager-261124-fr038-logic-p1-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr038-logic-p1-fixes.yaml` is prepared and NOT applied (the controller applies it).
**Owner defaults**: entries 96, 97 and 98 in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md` (provider access to copied data from FR-011 assignment; only the Admin corrects the treatment date; patient reminders on by default).

## Changes to the PRD

- The hand-off lands on FR-011 Screen 6. FR-038 Screen 6 ends at the review of the pre-filled fields and the monitoring PDF; the package and pricing option are chosen on FR-011 Screen 6 (REQ-038-017). The Available Aftercare Services row and the template fields are gone; REQ-038-065 and REQ-038-074 are retired (REQ-038-066).
- REQ-038-016 names the conversion contract: pre-filled fields, the attached monitoring PDF, an optional selected scan and an idempotency key; a repeated key returns the existing request.
- The case is committed as converted only when the FR-011 request exists; the case stays active until then. Screen 5 confirmation wording depends on the choice (REQ-038-081).
- Provider access to copied data begins when the Admin assigns the provider to the FR-011 request, before payment (REQ-038-050).
- PDF lifecycle: Screen 6 shows the PDF status; Retry PDF on Screen 7 when it failed (REQ-038-041); regeneration when logs or the selected scan change, and reuse on a repeated Switch (REQ-038-064); Continue only when the PDF is ready (REQ-038-066); an Admin correction regenerates the next report version (REQ-038-045); each Download issues a new signed link (REQ-038-076).
- A completed or converted case opens Screen 7 read-only from the patient home monitoring card (REQ-038-062). Screen 4 opens from Scan History and head-scan capture (REQ-038-049); Screen 8 has an Admin entry and no Type filter (REQ-038-061).
- Only the Admin corrects the treatment date; logs dated before the new date are corrected or removed in the same edit, otherwise the save is refused (REQ-038-030).
- Initial Severity is the first trend point, dated the case creation date; the period runs from the case creation date to the completion or conversion date; a case with zero logs shows no entries (REQ-038-034, REQ-038-035).
- Reminders are on by default, patient-changeable on Screen 2 and stop at completion or conversion; they use a progress-reminder event that FR-030 adds (REQ-038-031).
- A scan set that fails the quality check cannot be saved (REQ-038-048). The conversion draft is set at Switch and cleared at commit or return (REQ-038-037). Audit History gains an Action column.
- Rule texts changed in the PRD with the same wording in the graph; the change log row records 1.5.

## Graph change-set (prepared, not applied)

- 64 operations: 3 new steps (STP-038-057 Retry PDF regeneration, STP-038-058 report regeneration after an Admin correction, STP-038-059 Admin opens the case list), 29 edges added, 8 removed, 22 node updates (18 rules, 1 step, 2 screens, 1 setting), 2 rules retired (REQ-038-065, REQ-038-074); no new fields or enum values.
- Wiring: the next edge STP-038-055 to STP-038-056 is removed and STP-011-009 next STP-038-056 is added; retry edge STP-038-053 to STP-038-054; the next edges into retired steps STP-038-002 and STP-038-033 removed; STP-038-015 to STP-038-057 to STP-038-016; STP-038-034 to STP-038-058; FLW-038-admin-correction now starts at STP-038-059.
- Applied to a scratch copy of the db (91 change rows, no error), then the copy was deleted. Every active FR-038 step has a done by, one at and an incoming next or flow start. lint.py was not run (the controller lints after applying).

## Cross-FR rows queued

FR-011 (receiving rule, fields, Screen 6 landing, provider access), FR-037 (Initial Severity, reminder field, scan quality field, term, Screen 5 and Screen 6 check), FR-020 and FR-030 (progress-reminder event, export_ready wording, advice and conversion events, stage emits), FR-003 (Treatment Area), and the shared conversion stage join; see the FR-038 pass 1 section of `plans/reports/logic-review-ledger.md`.
