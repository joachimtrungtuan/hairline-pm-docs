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
