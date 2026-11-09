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
