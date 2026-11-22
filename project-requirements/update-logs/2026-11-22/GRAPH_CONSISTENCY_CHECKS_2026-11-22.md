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
