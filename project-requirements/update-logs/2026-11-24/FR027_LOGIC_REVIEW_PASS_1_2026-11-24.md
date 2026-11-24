# FR-027 Logic Review Pass 1 (2026-11-24)

**Scope**: FR-027 Legal Content Management, PRD v1.5 to v1.6. Pass 1 of the logic review; 30 findings, all fixed in FR-027 or queued to the neighbour FR that owns the other half.
**Evidence**: reviewer report `plans/reports/tester-261124-fr027-logic-p1.md`; fixer report `plans/reports/docs-manager-261124-fr027-logic-p1-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr027-logic-p1-fixes.yaml` is prepared and NOT applied (the controller applies it).
**Owner default**: entries 77 to 86 in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md` (Legal settings panel, Scheduled version withdrawal, one general consent, acceptance base, first-run acceptance, acceptance once per version, per-member provider acceptance, gated actions, daily reminder and coverage job, Cancellation Policy through the FR-006 link).

## Changes to the PRD

- Legal settings panel on Screen 1 for the four Admin-set values, each change audited, with the behaviour while a value is unset (no banner or alert, no reminders, export blocked, acceptance rules gate everyone for a Material Change = Yes version) (REQ-027-059, REQ-027-021).
- New Screen 5, the acceptance prompt shared by the patient app and the provider portal, so the user-facing acceptance steps have a screen (REQ-027-058).
- Publish and the audit entry run at the Publish click on both branches (Current at once or Scheduled); prompts start only when the version is Current and Material Change = Yes and Requires Acceptance = Yes (REQ-027-030, REQ-027-007, REQ-027-004). Admin confirms publication explicitly (REQ-027-011).
- Scheduled status added to the version model; a Scheduled version is view-only, at most one per document type, and Admin may withdraw it to Draft (REQ-027-008, REQ-027-060). Audit actions are now create, edit, publish, schedule, activate, archive, withdraw and settings_change; `revert` removed (REQ-027-013).
- Version label, status, effective date, Material Change and change summary belong to the version, and locale texts are children of it (REQ-027-061, REQ-027-040).
- Restore reuses the main edit, preview and publish steps, is always material (Material Change fixed to Yes, No for the Cancellation Policy), and prompts every user whose latest accepted version is not the one restored (REQ-027-031, REQ-027-032, REQ-027-049).
- First-run acceptance at registration and at invitation acceptance; the general consent is asked at first sign-in (REQ-027-062, REQ-027-017).
- Daily job: one reminder per pending user at most every 7 days up to the limit; coverage evaluated daily from 14 days after a version became Current; alert once per version; `reminders_sent_count` is the count of reminder records (REQ-027-063, REQ-027-023, REQ-027-024).
- Acceptance base defined (Active patients and Active providers' team members whose latest accepted version is older); not applicable for the Cancellation Policy and Material Change = No versions (REQ-027-053).
- Acceptance once per version, so FR-003 asks only when the Current Terms are not accepted (REQ-027-035). Every provider team member accepts personally (REQ-027-019).
- Gated actions named: patient inquiry submission, quote acceptance and payment start; provider inquiry acceptance and quote submission; everything else stays available and a non-accepting user may sign out or use the FR-001 account-deletion route (REQ-027-033, REQ-027-034).
- Cancellation Policy: Material Change fixed to No, shown through the FR-006 policy link, refund numbers owned by FR-029 (REQ-027-026, REQ-027-027). The FR-005 dependency is replaced by FR-006.
- Effective date is a UTC date and time, checked at save and again at Publish; the first version's diff summary reads "Initial version"; legal fallback fixed to English (en-US); Locale gap badge on the Screen 1 row; FR-023 retention sentence; Admin Terms of Service out of scope (REQ-027-041, REQ-027-050, REQ-027-036, REQ-027-037, REQ-027-012, REQ-027-025).

## Graph change-set (prepared, not applied)

- 9 new nodes (6 rules REQ-027-058 to REQ-027-063, screen SCR-027-06, steps STP-027-011 and STP-027-012), 6 enum values (scheduled and five audit actions), 1 field update, 40 node updates, 25 edges removed, 112 edges added, 1 enum value retired (`revert`) and 1 step retired (STP-027-031, replaced by the main publish steps).
- Validated by running `build_plan` and applying the file to a scratch copy of the graph; FR-027 lint on the copy is the 2 baseline L17 findings plus one L18 for the open FR-001 hand-off, and the whole graph goes from 28 to 29 findings.

## Cross-FR rows queued

FR-001, FR-003, FR-004, FR-005, FR-006, FR-007, FR-009, FR-020, FR-023, FR-030 and FR-031 (FR-021 needs no change): see the pass 1 section of `plans/reports/logic-review-ledger.md`.
