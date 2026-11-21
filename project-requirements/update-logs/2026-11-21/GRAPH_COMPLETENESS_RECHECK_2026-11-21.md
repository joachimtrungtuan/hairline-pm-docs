# Requirements Graph — Completeness Re-check on the New Baseline

**Date:** 2026-11-21
**Type:** Major update — requirements graph data changes across 36 FRs; no PRD text changed
**Programme:** `plans/261108-1040-requirements-graph-programme/` (Hairline root), Phase 4
**Owner decisions waiting:** `plans/reports/owner-decisions-261121.md` (Hairline root)
**Backlog:** `plans/reports/implementation-backlog-261120.md`, section "Added 2026-11-21 after the completeness re-check"

## Summary

An independent audit of Phase 4 (`plans/reports/code-reviewer-261121-0018-phase-04-dod-audit.md`) found that the completeness reports dated from before the 2026-11-20 baseline. Every open row of the 36 reports was re-checked against today's PRD and today's graph, one agent per FR, and the fixes were applied. Every report now shows zero requirements missing from the graph, except one FR-001 line that waits on an owner decision.

## What changed

- 36 per-FR change-sets `graph/changesets/2026-11-21-frNNN-completeness-recheck.yaml` (FR-032 has a second one): missing Rules, Steps, Flows, screen-to-field links and required flags added from PRD lines; Rule texts brought in line with the PRD where they differed.
- Rule rationales: PRD line numbers refreshed where the 2026-11-20 PRD edits had shifted them.
- Support-case Field descriptions corrected against the FR-034 and FR-035 PRDs (`2026-11-21-support-case-field-descriptions.yaml`).
- Lint clean-up (`2026-11-21-lint-cleanup-after-recheck.yaml`): eleven near-duplicate Rule pairs marked as distinct, one back-link marked.
- Filing clean-up (`2026-11-21-filing-cleanup-after-recheck.yaml`): the four aftercare catalogue Rules `REQ-020-117` to `120` merged into `REQ-030-072` to `075` (ruling Q-fr020-030-19); `SET-discovery-source-options` folded into `SET-discovery-question-options` and `SET-cancellation-policy-schedule` into `SET-refund-ladder`; a stale actor link removed from `REQ-007-040`; `EVT-legal-coverage-below-threshold` also recorded at the configuration Stage; two stale texts fixed.

## Result

- Graph: schema v11, 11,507 nodes, 40,415 edges; `graph.json` re-exported; 3D viewer opened on the new export.
- Lint: 102 findings. L18 90 (hand-offs between FRs, Phase 8), L17 10 (Steps at several Stages, accepted exception), L03 1 and L09 1 (recorded in the backlog). L10 and L12 at 0. No live node links to a retired one.
- Scripts unchanged, so the test suite was not re-run (245 passing on 2026-11-20).

## Not done

- 15 business decisions and 2 confirmations wait on the owner (`plans/reports/owner-decisions-261121.md`), including the move of 55 notification Events to FR-030 and the review of 76 layout-only PRD lines.
- Leftovers that need no owner answer are in the backlog section named above.
