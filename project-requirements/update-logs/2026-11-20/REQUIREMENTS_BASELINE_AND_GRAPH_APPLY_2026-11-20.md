# Requirements Baseline Reset — PRDs and Requirements Graph

**Date:** 2026-11-20
**Type:** Major update — all 38 feature PRDs and the system PRD revised; requirements graph schema v10 and data changes
**Programme:** `plans/261108-1040-requirements-graph-programme/` (Hairline root)
**Final report:** `plans/reports/final-261120-1530-requirements-baseline-graph-apply.md`
**Backlog:** `plans/reports/implementation-backlog-261120.md`

## Summary

The owner's answers from the programme's question rounds were applied as the new requirements baseline. The PRDs were edited first, then the graph was brought in line with them. By owner ruling this baseline needs no Change Request files.

## What changed

### PRDs

- The 38 feature PRDs and the system PRD were edited from the decision manifests and then reconciled against each other (41 files in commit `ef2178a`).
- Each PRD's Appendix: Change Log carries a row for this baseline.
- Platform-wide rules now live once in the system PRD; feature PRDs cite them instead of restating them.

### Requirements graph

- Schema v10; platform-wide Rules `REQ-SYS-001` to `REQ-SYS-014`; the Stage list set by the GLOBAL change-set.
- 51 change-sets dated 2026-11-20 in `graph/changesets/`: one baseline per FR (38), eleven cross-FR files, one cleanup file. Each was applied after a backup in `graph/backups/`.
- `graph.json` re-exported.

## Verification

- Lint on the final graph: 4,449 findings (L03 10, L10 4,274, L12 76, L18 89; L15 0), down from 4,516.
- Test suites: 237 tests pass.

## Follow-up the same day

- Duplicate-rule lint (L12) triaged in `graph/changesets/2026-11-20-l12-triage.yaml`: `REQ-030-128` merged into `REQ-020-052`, `REQ-018-265` merged into `REQ-018-263`, and 40 similar pairs marked as different rules. Lint is now 4,371 findings (L03 10, L10 4,272, L18 89; L12 0); 237 tests pass; `graph.json` re-exported.
- After an independent verification of the triage (`graph/changesets/2026-11-20-l12-triage-followup.yaml`): FR-030 now references `REQ-020-052`, and `REQ-001-147` was merged into `REQ-001-146` (one six-digit code input rule on two screens). Lint is 4,370 findings (L03 10, L10 4,271, L18 89).
- Links from live nodes to retired nodes cut from 45 to 8 (`graph/changesets/2026-11-20-retired-links.yaml`, `2026-11-20-retired-links-2.yaml`): Steps and FRs now point at the replacement Rules, and the FR-028 location preview Screen shows the grouping and starting-price Fields it is computed from. Lint is 4,369 findings (L03 9, L10 4,271, L18 89); 237 tests pass; `graph.json` re-exported. The 8 remaining links are in the backlog.
- Schema v11: a Screen may be marked `display_only` with a `display_only_reason` (owner-approved marker). Lint L03 skips such a Screen, and flags one that no Step is on or that shows a Field. Eight Screens marked (`graph/changesets/2026-11-20-display-only-screens.yaml`); `SCR-024-08` now shows the Fields of a new Entity `ENT-aftercare-content-template`.
- Sources: the 23 cited "pending review" Sources are now "incorporated" (`2026-11-20-pending-sources-incorporated.yaml`); 63 uncited ones stay pending. By owner ruling the PRD a Rule came from is an acceptable deciding Source: 38 Sources `SRC-PRD-NNN` added and 3,531 Rules linked to their own PRD (`2026-11-20-prd-sources.yaml`).
- Lint after these: 836 findings (L03 6, L10 741, L18 89), down from 4,369; 245 tests pass; `graph.json` re-exported.
- A further 420 Rules whose statement matches a line of their own PRD (line recorded in the rationale) and 134 Entities named in their owning PRD were linked to the PRD Source (`2026-11-20-prd-sources-matched.yaml`; `SRC-PRD-SYS` added for the system PRD). 120 Rules and 67 Entities remain without a Source.
- The remainder was closed: 38 Rules and the 67 Entities linked to their owning PRD (`2026-11-20-prd-sources-checked.yaml`), and the last 86 Rules (FR-007, FR-008, FR-009, FR-029) checked line by line against their PRD and linked (`2026-11-20-prd-sources-agent-checked.yaml`). Nine Rule texts that differed from the PRD were brought in line with it: `REQ-004-101`, `REQ-007-029`, `REQ-007-050`, `REQ-007-058`, `REQ-007-076`, `REQ-009-042`, `REQ-009-049`, `REQ-009-109`, `REQ-009-142`.
- Final lint: 95 findings (L03 6, L18 89; L10 0). Every active Rule now has a deciding Source. `graph.json` re-exported (11,194 nodes, 38,746 edges).

## Not done

Items the inputs left open are listed per FR in `plans/reports/graph-result-261120-frNNN.md` and collected in the backlog file above.
