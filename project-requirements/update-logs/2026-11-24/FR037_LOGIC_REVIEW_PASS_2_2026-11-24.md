# FR-037 Logic Review, Pass 2 (2026-11-24)

## Scope

Applies the triaged second-pass logic-review fixes (18 findings and three minor observations) to the FR-037 Monitor Hair Loss PRD and records the matching requirements-graph change-set. PRD version 2.31 becomes 2.32.

- PRD: `local-docs/project-requirements/functional-requirements/fr037-monitor-hair-loss/prd.md`
- Graph change-set: `local-docs/project-requirements/graph/changesets/2026-11-24-fr037-logic-p2-fixes.yaml` (written and test-applied on a scratch copy only; not applied to the live graph)

## What changed in the PRD

- **Advice windows and assignment end:** an open, unanswered window expires when the assignment ends for any cause; the replacement's first window opens one cadence period after the new assignment. Completion or conversion sets the advice state to ended (added to the Screen 2 label and the Screen 12 filter). Assign Provider and Share Case Preview need an active case.
- **Assignment-end handling:** the assignment records how it ended (end cause) and, for an Admin end, the reason, shown on Screens 12 and 13. The patient and Admin are always told when an assignment ends other than by provider withdrawal; the provider is also told, in neutral wording, when Admin ends it, and receives no notice on completion or conversion. An Admin change to advice text sends the same "updated" notice; other corrections send none.
- **Conversion:** Request Treatment shows no confirmation (Step A states that monitoring ends when the inquiry is submitted); the assigned provider is evaluated when the FR-003 inquiry submission succeeds; after three PDF failures the PDF is marked failed, conversion proceeds, Admin sees the failure on Screen 13, and Retry PDF works on a converted case and attaches the result; a resumed draft rebuilds the PDF and carried-over values.
- **Intake and summary:** Duration stores the FR-026-managed option reference and label, only active options are offered, and the patient chooses again if the option was retired. The intake rating is a trend point under the same-date rule; the summary value is named First recorded severity.
- **Admin:** assignment state and conversion links removed from the Admin-editable list; assignment changes happen only through the assignment controls.
- **Minor:** Screen 8 Advice Filter gets expired-unsubmitted; Preview Expiry has a minimum of 1 day; advice-cadence changes are on the audit list.

## What changed in the graph (change-set only)

- Two new FR-037 steps (STP-037-055 Admin opens the case list; STP-037-056 system attaches the PDF) and three new fields (end_cause, end_reason, duration_option_id).
- Steps STP-037-044 and STP-037-045 retired (they duplicated the single FR-003 router STP-003-019); the Screen 12 Admin flow now starts at STP-037-055.
- Reworded rule statements and field descriptions mirror the PRD text; missing return, applies and shows edges added.
- Cross-FR edges: none added; removed STP-037-044 to STP-003-066 and STP-037-045 to STP-003-020.
- The change-set test-applied cleanly on a scratch copy (128 change rows); the copy was deleted.

## Not changed here (queued for neighbour FRs)

FR-030 and FR-020 (monitoring.assignment_ended event row), FR-003 (problem_duration may need the option reference), FR-026 (retire semantics for the problem-duration list).
