# Requirements Graph — Cross-FR Consistency Checks Added (Phase 8 Start)

**Date:** 2026-11-22
**Type:** Major update — new graph query commands, a new checklist, and derived graph links. No PRD text changed.
**Programme:** `plans/261108-1040-requirements-graph-programme/` (Hairline root), Phase 8 (in progress)

## Summary

Phase 8 checks the 38 FRs against each other. Its first step is in place: five query commands that list where FR boundaries or the flow of data between stages look inconsistent. Every row they print is a finding for a person to judge, not an error.

## What changed

- `graph/scripts/consistency.py` (new) and `graph/scripts/query.py`: commands `boundary`, `ownership`, `flow`, `joins`, `coverage`. Tests in `graph/scripts/test_consistency.py`; the suite now has 259 tests, all passing.
- `graph/checklists/consistency-review.md` v1.0 (new): what each finding means, the verdicts, and how a decision request is phrased. `checklists/README.md` to v1.6.
- Graph, `changesets/2026-11-22-consistency-stage-data-links.yaml`: 266 Stage links derived from links the graph already had. A Stage reads an Entity when a Screen at that Stage shows one of its Fields (197 links), and writes it when the Field is editable there (69 links).
- Graph, `changesets/2026-11-22-consistency-stage-data-links-steps.yaml`: 166 more Stage links (110 reads, 56 writes) derived the same way through Steps: a Step at a Stage done on a Screen that shows the Field. After it the flow check lists 45 rows.
- Graph, `changesets/2026-11-22-consistency-rule-stages.yaml`: REQ-024-100 and REQ-026-139, added earlier the same day, now carry a Stage.

## Findings after these changes

| Check | Rows |
|---|---|
| boundary (FR pairs sharing data with no reference link) | 108 |
| ownership (Fields owned by another FR than their Entity) | 34 |
| flow (unused Events, Entities written or read on one side only, Stages with no incoming data) | 53, down from 150 |
| joins (data read on entering a timeline that was not written before) | 12 |
| coverage (Stages with no Actor) | 2 |

Lint is unchanged at 102. The findings are reviewed FR by FR next; only real conflicts between PRDs go to the owner.

## Later the same day

- FR-007B PRD v1.8: Alternative Flow B4 step 2 and REQ-007b-027 aligned with the earlier ruling already written in FR-006 (Alternative Flow B5) and FR-007: a provider withdrawal or drop-out refunds every paid installment in full; a suspension or deactivation keeps the placeholder. Graph: `changesets/2026-11-22-provider-fault-refund-wording.yaml`.
- Per-FR consistency reviews started; each applied change-set is `changesets/2026-11-22-frNNN-consistency.yaml` (reference links to data-owner FRs and stitched hand-offs between flows).
- FR-016 PRD: Alternative Flow B5 step 8 aligned with FR-023 (the system sends the deletion outcome notice with actions taken and legal basis). Graph: `changesets/2026-11-22-fr016-deletion-notice-wording.yaml`.
- Per-FR consistency reviews finished for all 38 FRs (one review per FR; reports in `plans/reports/docs-manager-261122-frNNN-consistency.md`).
- Back links: 9 cross-FR `next` links that return to an earlier stage are marked `back: true`; three hand-off notes without a single receiving step were cleared (STP-017-008 already linked; STP-014-014 and STP-014-018 name no single receiver). Graph: `changesets/2026-11-22-consistency-back-links.yaml`.
- Wording aligned to the owning FR (each PRD has a Change Log row): FR-023 v1.6 (AcceptanceEvents retained, per FR-005), FR-028 v1.4 (conversion rate with markup, per FR-029), FR-038 v1.3 (standalone aftercare request continues in FR-011), FR-011 v1.9 (treatment area and type come from the catalog lists, per FR-003 and FR-004), FR-032 v1.16 (Account Email uniqueness per FR-009 Rule 3), FR-022 v2.21 (patient Status and Account Status filters per FR-016; Closure Requested filter and 50-row provider list per FR-015; stale treatment type search field retired). Graph: `changesets/2026-11-22-consistency-wording-fixes.yaml`, `changesets/2026-11-22-consistency-wording-fixes-2.yaml`.
- Lint after these changes: 24 findings (L18 12 hand-offs that wait for flows not yet written, L17 10 accepted, L03 1, L09 1).
- System-check Steps removed from the flows (owner ruling: Steps that only say the system validates, detects or compares are not wanted): 114 Steps across 23 FRs retired; each flow now passes from the Step before to the Step after, 16 flow starts moved to the next Step, and the Rules a check applied are attached to the Step that triggers it. The Rules themselves are unchanged and no PRD text changed. Graph: `changesets/2026-11-22-remove-system-check-steps.yaml`. Left in place: STP-012-012 (starts a flow and has two exits) and the Steps the reviews marked mixed or borderline (they also record or decide something).
