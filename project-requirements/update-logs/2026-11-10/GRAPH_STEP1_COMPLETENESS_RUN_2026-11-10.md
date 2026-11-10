# Requirements Graph — D37 Review Step 1 Completeness Run (All 38 FRs)

**Date:** 2026-11-10
**Type:** Major update — graph data additions (fix change-sets applied; held change-sets not applied)
**Programme:** `plans/261108-1040-requirements-graph-programme/` (Hairline root)
**Run ledger:** `plans/261108-1040-requirements-graph-programme/overnight-run-261110.md`
**Decision list:** `plans/reports/morning-list-261110-step1-decisions.md`

## Summary

D37 review step 1 (completeness check, checklist 1.3: every PRD line compared with the graph) ran across all 38 FRs overnight. Each FR got a headless DeepSeek draft, then a Sonnet gate that owned the verdict, wrote a fixes change-set and a held change-set for anything needing a decision. The fixes were applied to the graph in 11 groups. The held change-sets were committed but not applied; they wait on user decisions. No PRD text changed.

## What changed

| Area | Change |
|---|---|
| `graph/graph.db` | Fix change-sets for all 38 FRs applied in 11 groups, each with a backup in `project-requirements/graph/backups/` taken before the apply. Local-docs commits: 02d7f90, cfb21cb, fd11e99, 640d414, e7a2bc0, 58a68f7, 1854f17, 1d9a7b9, 60d92f3, 6a1bc8c, a68dd3d |
| `graph/changesets/2026-11-10-frNNN-completeness-fixes.yaml` | Applied. New Steps, Flows, Rules, `applies to` and `references` edges, flow-model edges |
| `graph/changesets/2026-11-10-frNNN-completeness-held.yaml` | 38 files, about 10,287 ops in total. Committed, NOT applied |

## Controller policies applied during the run

- New Rules are added only when their text is a verbatim PRD line; paraphrased or fragment Rules are held for wording review.
- Enum operations are held.
- Decision-code mappings that are ambiguous (a change log names a code without saying which Rule it governs) are held.
- Rules drawn from lines the migration excluded are held.
- System-performed Steps are held, because the graph has no system Actor (the largest single blocker).

## Results

- Lint: 4,322 at the start, 4,365 after the last group. Tests OK after every group.
- Held ops: about 10,287 across 38 files; applying them is gated on the decisions in the morning list.
- Per-FR gate verdicts, decision counts and the open items are in the morning decision list, not repeated here.

## Next

The user works through `plans/reports/morning-list-261110-step1-decisions.md` (system actor gap first), then applies the freed held files with `apply.sh` after a backup. D37 step 2 (cross-FR hand-off links and duplicates) follows.

## System-step release (decision D44), applied 2026-11-10 afternoon

Decision D44 made `ACT-system` the one actor for system Steps. The held ops whose only hold reason was the missing system Actor were split into 31 `graph/changesets/2026-11-10-frNNN-system-steps.yaml` files and applied to the live graph.

- **Correction before applying.** Whether external services (payment gateway, email and SMS providers) count as "the system" is still open. The three Payment Service capture and retry Steps (STP-006-005, STP-006-201, STP-007-042) and the 61 ops that depend on them (their edges, Flow FLW-006-b1, and downstream Steps no Flow would reach) went back to the FR-006 and FR-007 held files under `# waits on: external-service question (payment capture)`. Ops were moved unaltered. Local-docs commit 315e7be.
- **Applied.** 7,299 original ops, plus 879 generated `done by ACT-system` edges and 17 generated `acts in` edges (8,195 ops), in FR number order in 8 groups of up to 4 files. Each group was backed up first to `project-requirements/graph/backups/` (graph-20261110-163237.db to graph-20261110-163951.db; the folder is not tracked by git). Local-docs commits: eb8cd14, 3c218fb, 459eaeb, f8d5516, 21ab3eb, 402899c, bb0eae0, 9e8299a.
- **Graph size.** Nodes 9,144 to 10,533 (+1,389). Edges 24,522 to 31,328 (+6,806).
- **Lint.** 4,365 to 4,403. Only L18 rose, 34 to 72 (+38): `handoff_to` and `handoff_from` attributes on released Steps that point at another FR, open until D37 step 2 stitches cross-FR links. L10 (4,151) and L12 (180) unchanged; no L14, L15, L16, L17 or L19. Tests (224) passed after every group; `graph.json` re-exported after every group.
- **Still held: 2,988 ops** in the 38 `*-completeness-held.yaml` files, each under its `# waits on:` comment:
  - 81 system Steps that carry a human `done by` edge (conflicts; most of FR-003, all of FR-004 and FR-015);
  - 7 Steps an external service performs, plus the 3 payment-capture Steps above (external-service question);
  - 7 no-doer Steps whose title names a person who receives or sees something (doer reading);
  - ops waiting on other decisions (stage placement, enum, Rule wording, review-queue items), and everything that depends on a held op or that no Flow would reach.
- **Report:** `plans/reports/fullstack-developer-261110-1630-system-steps-apply.md` (Hairline root).

## External-service and payment-capture release (decisions D45 and D46), applied 2026-11-10 evening

D45 gave each external service its own Actor (schema v8, group `external`: `ACT-stripe`, `ACT-email-provider`, `ACT-rate-source`). D46 placed the Payment Service (S-02) in the system. The 10 Steps held under the external-service question, and the ops held only because of them, moved from 7 held files into `graph/changesets/2026-11-10-frNNN-external-steps.yaml` (FR-006, FR-007, FR-017, FR-018, FR-029, FR-030, FR-031) and were applied to the live graph in FR number order.

- **Doers.** STP-017-045, STP-017-046, STP-018-084 and STP-029-112 are `done by ACT-stripe`; STP-029-119 `done by ACT-rate-source`; STP-030-050 and STP-031-732 `done by ACT-email-provider`; STP-006-005, STP-006-201 and STP-007-042 `done by ACT-system`. 34 released downstream system Steps with no doer got `done by ACT-system` as under D44. 4 `acts in` edges were added for the external Actors. No existing doer was changed.
- **Ops.** 271 held ops released unaltered (including the 61 ops held with the payment-capture Steps in commit 315e7be), plus 48 generated edges (319 ops applied). The count proof passes for all 38 FRs: 2,988 held before = 271 released + 2,717 still held. A control run with the 10 Steps kept held releases nothing. Ops with any other wait reason were not touched.
- **Backup and lint.** Backup `graph/backups/graph-20261110-174348.db` (git-ignored). Lint 4,403 to 4,404: one new L18, the open hand-off on STP-017-008 to FR-032 and FR-034; no L14, L15, L16, L17 or L19. Tests (229) passed; `graph.json` re-exported (10592 active nodes). Local-docs commits f544f4d, 45f8a98, 09095eb, 26d2650.
- **Still held: 2,717 ops**, none of them on the external-service question: the 81 conflict Steps, the 7 doer-reading Steps, ops waiting on other decisions, and everything that depends on them.
- **Report:** `plans/reports/fullstack-developer-261110-1740-external-actors-payment-capture.md` (Hairline root).

## Conflict and doer-reading release (decisions D47 and D48), applied 2026-11-10 evening

D47 put the 81 held "conflict" Steps (system actions that carried a human doer) on `ACT-system`, and split STP-003-015. D48 gave doers to the 7 doer-reading Steps. The released Steps, and the ops held only because of them, moved from 7 held files into `graph/changesets/2026-11-10-frNNN-doer-decisions.yaml` (FR-001, FR-003, FR-004, FR-012, FR-015, FR-033, FR-035) and were applied to the live graph in FR number order.

- **Doers.** All 81 conflict Steps (FR-003 36, FR-004 16, FR-012 1, FR-015 28) are `done by ACT-system`: in each, the one held human `done by` op now points at ACT-system, and nothing else in the op changed. STP-003-015 keeps its ID as "Submission fails and an error is shown"; the new Step STP-003-087 "Patient retries" (`done by ACT-patient`, Stage Inquiry, Screen SCR-003-07) follows it and carries the retry link back to STP-003-014. STP-001-123, STP-033-083 and STP-035-057 are `done by ACT-system`. 4 released FR-012 system Steps with no doer got `done by ACT-system` as under D44. 4 `acts in` edges were added from ACT-system to the provider Stages Invited, Onboarding, Suspended and Offboarded. No other doer was changed.
- **Kept held.** STP-017-059: its flow (FLW-017-schedule-change) waits on decision 4. STP-031-742: every neighbouring Step in its flow is done by ACT-system, so the D48 rule names no admin Actor. STP-032-044 and STP-032-070: the following Steps (STP-032-045, STP-032-071) are themselves held and have no doer.
- **Ops.** 811 held ops released, plus 16 new ops (7 `done by`, 4 `acts in`, 5 for STP-003-087), so 827 ops were applied. The count proof passes for all 38 FRs: 2,717 held before = 811 released + 1,906 still held. A control run with the target Steps kept held releases nothing. Ops with any other wait reason were not touched.
- **Backup and lint.** Backup `graph/backups/graph-20261110-175520.db` (git-ignored). Lint went from 4,404 to 4,416: 12 new L18 open hand-offs, and no L14, L15, L16, L17 or L19. All 229 tests passed, and `graph.json` was re-exported (10,735 active nodes). Local-docs commits 4b752ea and f2d307d.
- **Still held: 1,906 ops.** None of them waits on the conflict question. They are the 4 Steps above, ops waiting on other decisions, and everything that depends on them.
- **Report:** `plans/reports/fullstack-developer-261110-1750-doer-decisions-apply.md` (Hairline root).

## Platform administration release (decision D49), applied 2026-11-10 evening

D49 gave admin settings and configuration Steps their own timeline, `platform-admin`, with one Stage STG-admin-01-configuration "Configuration" (schema version 9; see the v9 addendum in `REQUIREMENTS_GRAPH_SCHEMA_V6_2026-11-10.md`). The Stage is added by `graph/changesets/2026-11-10-platform-admin-stage.yaml`. The held admin settings Steps, and the ops held only because of them, moved from 3 held files into `graph/changesets/2026-11-10-frNNN-admin-stage.yaml` (FR-002, FR-025, FR-026). Two more files (FR-021, FR-030) move live Steps. All were applied in FR number order.

- **Placement.** The one change made to a held op: the `at` edge of 123 released Steps now points at STG-admin-01-configuration instead of the placeholder Stage (FR-002 4 and FR-025 16 from STG-main-01-inquiry, FR-026 103 from STG-provider-03-active). Nothing else in any op changed. 55 released system Steps with no doer got `done by ACT-system` as under D44 (FR-002 3, FR-026 52). 2 `acts in` edges were added (ACT-platform-admin and ACT-system to Configuration).
- **Live moves.** 53 live ACT-platform-admin Steps that a tester report flags as placed at Inquiry only for lack of an admin Stage moved to Configuration: FR-021 15 (item 11) and FR-030 38 (item 10). STP-030-056 and STP-030-057 stayed at Inquiry because they are operational, not settings. Other admin or system Steps at placeholder Stages were not moved because no record flags them; the report lists them.
- **Ops.** 698 held ops released, plus 55 `done by`, 2 `acts in` and 106 live-move ops (53 add and 53 remove), plus the Stage: 862 ops applied. The count proof passes for all 38 FRs: 1,906 held before = 698 released + 1,208 still held. A control run with the admin-placement reasons kept held releases nothing.
- **Kept held.** FR-025: 13 ops (12 also wait on item 2, the incomplete-question contradiction; 1 on the Aftercare-stage emission placement choice). FR-026: 5 ops (STP-026-037 is flagged for a doer reading, its edges stay with it, and 1 op waits on the Q13 and Q14 Quote Rule question). Ops with any other wait reason were not touched.
- **Backup and lint.** Backup `graph/backups/graph-20261110-190500.db` (git-ignored); the migration also wrote `graph-20261110-190500-1.db`. Lint went from 4,416 to 4,417: 1 new L18 open hand-off (STP-002-017), and no L14, L15, L16, L17 or L19. All 234 tests passed, and `graph.json` was re-exported (10,882 nodes). Local-docs commits 462631b, d7a8c82 and ff68d15.
- **Still held: 1,208 ops.** None waits only on the admin settings placement.
- **Report:** `plans/reports/fullstack-developer-261110-1852-platform-admin-timeline.md` (Hairline root).

## Rule wording release (decision D52), applied 2026-11-10 evening

D52 settled the wording of the 31 Rules held for the new Rule wording review (FR-001, FR-013, FR-016, FR-017, FR-019, FR-021, FR-030, FR-034, FR-035). Their ops, and the new Rules from the splits, moved into `graph/changesets/2026-11-10-frNNN-rule-wording.yaml` (9 files) and were applied to the live graph in FR number order.

- **Wordings.** 21 Rules keep their proposed statement. 10 get the decided statement (REQ-001-148, 150, 152, 153, 156, REQ-017-168, REQ-021-116, 117, REQ-030-213, REQ-034-160); for the split Rules the title and the PRD citation in `rationale` changed too. No other op was altered, apart from one edge moved to its new half (REQ-001-153 `applies to` SCR-001-17 now leaves REQ-001-161).
- **New Rules (11).** REQ-001-157 (15-minute reset-code expiry, beside REQ-001-147), REQ-001-158 to 162 (the second halves of 148, 150, 152, 153, 156), REQ-017-171 (currency pairs configurable in FR-029), REQ-030-214 to 217 (one Rule per FR-030 Out of Scope bullet). Each copies only the source edges that fit its half.
- **Ops.** 109 held ops released, plus 26 new ops: 135 applied. The count proof passes for all 38 FRs: 1,208 held before = 109 released + 1,099 still held. A control run releases nothing.
- **Kept held.** REQ-001-152 and REQ-001-160 `applies to` SCR-001-22 (the Settings Main Screen is itself held). Two copied edges whose half is unclear, under `# waits on: split edge placement (decision D52)`: REQ-001-157 `applies to` ENT-otp-code.code and REQ-017-171 `applies to` ENT-currency-rate-lock. REQ-034-161, 162 and 163 (12 ops) were not in the review and still wait on their wording.
- **Backup and lint.** Backup `graph/backups/graph-20261110-203726.db` (git-ignored). Lint went from 4,417 to 4,461: L10 +42 (the released and new Rules have no `decided by` Source yet) and L12 +2 (REQ-001-146 and REQ-001-147 read alike; they cover the sign-up and reset codes). No L14, L15, L16, L17 or L19. All 234 tests passed, and `graph.json` was re-exported (10,924 nodes). Local-docs commits 3b08258 and 9314968.
- **Still held: 1,102 ops.** None waits on the reviewed wordings.
- **Report:** `plans/reports/fullstack-developer-261110-2030-rule-wording-apply.md` (Hairline root).
- **Follow-up (2026-11-10, user decisions).** REQ-001-162 now reads "On the Delete Account screen, the confirmation modal's Confirm submits the deletion request and Cancel returns to the Delete Account screen." REQ-034-161, 162 and 163 were released with the decided statements ("The ... checkbox is checked by default.") and all 9 of their edges. The change-sets are `2026-11-10-fr001-rule-wording-followup.yaml` (1 op) and `2026-11-10-fr034-rule-wording-followup.yaml` (12 ops). For FR-034, 15 held before = 12 released + 3 still held (the F8 emits edges). Held total is now 1,090. Lint went from 4,461 to 4,466: L10 +3 (no `decided by` Source yet) and L12 +2 (REQ-034-162 and 163 read alike but are different checkboxes on Screens 5 and 6, so both are kept). There are no other new findings. Backup `graph/backups/graph-20261110-205403.db`. Local-docs commits b503abb and 9041cbb. The FR-001 split halves and the "Out of scope: " prefix on REQ-030-213 to 217 were confirmed as they are.

## Doer follow-up (D48 follow-up rulings), applied 2026-11-10 night

- **Rulings.** STP-031-742 "Admin reaches a restricted feature" is `done by ACT-platform-admin`. STP-032-044 "Network connection drops" and STP-032-070 "Network connection times out" are `done by ACT-system`. STP-003-087 "Patient retries" now leads `next` to STP-003-013 (review and accept the terms) instead of STP-003-014, as the FR-003 PRD diagram shows.
- **Released.** FR-031: all 22 held ops (the B5 unauthorized-access chain, STP-031-742 to 746). FR-032: 52 of 56 (the B3 and B4 network-error chains, STP-032-044 to 049 and 070 to 074). The system Steps they unblock got `done by ACT-system` under D44 (FR-031 4, FR-032 7); no existing doer was changed and no `acts in` edge was needed.
- **Ops.** 74 held ops released plus 12 new `done by` ops, and the FR-003 edge swap (1 `remove_edge`, 1 `add_edge`): 88 ops in `graph/changesets/2026-11-10-fr003-doer-followup.yaml`, `-fr031-` and `-fr032-`. The count proof passes: FR-031 22 = 22 + 0, FR-032 56 = 52 + 4; the other 36 held files are unchanged. A control run releases nothing.
- **Still held: 1,016 ops.** The 4 FR-032 `applies to ACT-provider` ops wait on decision 4 (which Actor stands for all provider roles). STP-017-059 and STP-026-037 were out of scope.
- **Backup and lint.** Backup `graph/backups/graph-20261110-210547.db` (git-ignored). Lint is unchanged at 4,466 (L10 4,196, L12 184, L18 86), with no new finding. All 234 tests passed, and `graph.json` was re-exported (10,943 active nodes). Local-docs commits 160703d and d94f22f.
- **Report:** `plans/reports/fullstack-developer-261110-1750-doer-decisions-apply.md`, Follow-up section (Hairline root).

## Admin-stage follow-up (D49 follow-up rulings), applied 2026-11-10 night

- **Rulings.** FR-028 regional configuration and pricing Steps and FR-025 STP-025-040 to 045 move from STG-main-01-inquiry to STG-admin-01-configuration. The leftover FR-021, FR-030 and FR-002 Steps at Inquiry move only where the system replies to the admin inside the settings flow; Steps that describe an effect on patients, providers or later journey behaviour stay at Inquiry. The FR-026 patient-side effect Steps stay at Configuration. STP-026-037 is dropped as a Step because Rule REQ-026-106 covers it.
- **Moved (110 Steps, 220 ops).** FR-021 18, FR-025 6, FR-028 68 (the admin flows Main Flows 1 and 2, A1 to A4 and B1 to B5, 42 admin and 26 system Steps) and FR-030 18, in `graph/changesets/2026-11-10-frNNN-admin-stage-followup.yaml` (4 files, applied in FR number order). Each move removes the Inquiry `at` edge and adds the Configuration one. No `acts in` edge was needed, and no Screen or Rule moved.
- **Not moved.** FR-002 STP-002-018, 020 and 021; FR-021 STP-021-030; FR-030 STP-030-024, 036 and 048 to 055 (each describes a later effect on patients, providers or the running platform), plus STP-030-056 and 057 by ruling. The 18 FR-028 Steps of the patient destination flow (STP-028-401 to 425) wait for the user to confirm, because they describe what the patient sees. The report lists each Step with its reason.
- **STP-026-037.** Its 3 held ops (the Step, its `at` edge and the `next` edge from STP-026-036) are kept in `graph/changesets/2026-11-10-fr026-completeness-held.yaml` as comments marked "excluded by user decision". For FR-026, 5 held before = 3 excluded + 2 still held (the Q13 and Q14 `decided by` edges). STP-026-036 `applies` REQ-026-106 was already live, and no other graph file or live edge references STP-026-037.
- **Still held: 1,013 ops.**
- **Backup and lint.** Backup `graph/backups/graph-20261110-211631.db` (git-ignored). Lint is unchanged at 4,466 (L10 4,196, L12 184, L18 86), with no new or resolved finding. All 234 tests passed, and `graph.json` was re-exported. Local-docs commits f280585, eb7c581 and 138de40.
- **Report:** `plans/reports/fullstack-developer-261110-1852-platform-admin-timeline.md`, Follow-up section (Hairline root).

## Split edge placement (decision D52 follow-up), applied 2026-11-10 night

- **Rulings.** REQ-001-157 (the reset code expires after 15 minutes) `applies to` the field ENT-otp-code.expires_at, not the copied target ENT-otp-code.code. REQ-017-171 (supported currency pairs are configurable in FR-029) `applies to` ENT-currency-pair, not the copied target ENT-currency-rate-lock.
- **Released (2 ops).** One edge each in `graph/changesets/2026-11-10-fr001-rule-data-links.yaml` and `graph/changesets/2026-11-10-fr017-rule-data-links.yaml`, with the decided targets. The two held edges and their wait notes were removed from the FR-001 and FR-017 held files, which now carry a dated note; every other held line is unchanged. Neither copied target is linked from these Rules in the live graph.
- **Still held: 1,011 ops.**
- **Backup and lint.** Backup `graph/backups/graph-20261110-212422.db` (git-ignored). Lint is unchanged at 4,466 (L10 4,196, L12 184, L18 86), with no new or resolved finding. All 234 tests passed, and `graph.json` was re-exported.
- **Report:** `plans/reports/fullstack-developer-261110-2030-rule-wording-apply.md`, Follow-up 2 section (Hairline root).

## Decision-code links by topic (decision D50), applied 2026-11-10 night

- **Ruling.** A Rule gets a `decided by` link to a decision-code Source (MTG-002 Product Owner decision log codes D, M, Q and R7) where the decision text and the PRD change-log row are clearly about the same subject as the Rule. Unclear matches are not linked; they stay held and are listed for the user.
- **Scope.** The 79 held `decided by` ops of FR-004, FR-008, FR-010, FR-016, FR-019 and FR-026, which were the only held ops waiting on decision-code mappings. No Rule statement, other node or PRD was changed.
- **Released (63 ops).** FR-004 19, FR-008 1, FR-010 5, FR-016 1, FR-019 35 and FR-026 2, in `graph/changesets/2026-11-10-frNNN-decision-links.yaml`. Each op carries a one-line reason for the topic match. The released lines left the six held files, a wait note left only where every op under it left, and each held file carries a dated D50 note; every other held line is unchanged.
- **Kept held as unclear (16 ops).** FR-008 1, FR-010 6, FR-016 3 and FR-019 6 (including two Entity links to Q38, which D50 does not cover because they do not start at a Rule). They are listed for the user in the report.
- **Still held: 948 ops** (1,011 before).
- **Backup and lint.** Backup `graph/backups/graph-20261110-222511.db` (git-ignored). Lint went from 4,466 to 4,449 (L10 4,179, L12 184, L18 86): 17 L10 findings resolved, none new. All 234 tests passed, and `graph.json` was re-exported.
- **Report:** `plans/reports/fullstack-developer-261110-2220-decision-links-apply.md` (Hairline root).

## Admin-stage follow-up 2 and FR-014 two-doer split, applied 2026-11-10 night

- **Ruling 1 (D49 follow-up 2).** The mixed Steps STP-002-018, STP-002-020 and STP-030-036 move from STG-main-01-inquiry to STG-admin-01-configuration. Each had exactly one `at` edge, to Inquiry, and its doer ACT-system already acts in Configuration, so no `acts in` edge was needed. No other Step moved: STP-002-021, STP-021-030, STP-030-024, STP-030-048 to 057 and STP-028-401 to 425 stay at Inquiry by ruling. Applied in `graph/changesets/2026-11-10-fr002-admin-stage-followup-2.yaml` (4 ops) and `graph/changesets/2026-11-10-fr030-admin-stage-followup-2.yaml` (2 ops).
- **Ruling 2 (two-doer Step split).** STP-014-014 had two doers. It keeps ACT-provider and is retitled "Provider clicks a chart element to open the filtered operational list". The new Step STP-014-018 "Admin clicks a chart element to open the filtered operational list" is done by ACT-platform-admin, with the same owner FR-014, attrs (`prd_ref`, `handoff_to`), Stage STG-provider-03-active and `applies` REQ-014-145. FLW-014-drill-down-from-chart now starts at both Steps (the schema sets no limit on `starts at`, and FLW-008-edit-blocked already has two). Applied in `graph/changesets/2026-11-10-fr014-split-two-doer-step.yaml` (7 ops). Every active Step now has exactly one `at` and one `done by` edge.
- **Still held: 948 ops** (unchanged; no held file changed).
- **Backup and lint.** Backup `graph/backups/graph-20261110-223436.db` (git-ignored). Lint went from 4,449 to 4,450 (L10 4,179, L12 184, L18 87): one new finding, L18:STP-014-018#handoff_to, because the new Step carries the same open hand-off as STP-014-014; none resolved and no L14 to L19 finding other than that L18. All 234 tests passed, and `graph.json` was re-exported.
- **Report:** `plans/reports/fullstack-developer-261110-1852-platform-admin-timeline.md`, Follow-up 2 section (Hairline root).
