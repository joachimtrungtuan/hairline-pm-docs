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
