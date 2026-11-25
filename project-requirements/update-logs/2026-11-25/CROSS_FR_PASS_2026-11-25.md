# Cross-FR pass of the logic review

**Date**: 2026-11-25 (Asia/Saigon)
**Type**: Major update (cross-document alignment of 34 FR PRDs and the requirements graph). No Change Request (requirements graph programme: new baseline).

## What changed

The two-pass logic review of each FR left rows queued for the neighbour FR that owns the item. This pass settled all of them, grouped by owner FR, in eight batches.

| Batch | Owner FRs | Rows | Already satisfied | Fixed | Default applied | Not changed | Commit |
|---|---|---|---|---|---|---|---|
| A | FR-030 | 76 | 36 | 38 | 0 | 2 | `51d915f` |
| B | FR-031, FR-026 | 50 | 34 | 13 | 0 | 3 | `f592158` |
| C | FR-001, FR-002, FR-003 | 46 | 15 | 28 | 0 | 3 | `cbc51f8` |
| D | FR-004, FR-005, FR-006 | 51 | 4 | 45 | 0 | 2 | `7393942` |
| E | FR-007, FR-007B, FR-009, FR-010, FR-011 | 51 | 11 | 37 | 0 | 3 | `e6b9ee7` |
| F | FR-012 to FR-018 | 58 | 20 | 33 | 3 | 2 | `23b83ce` |
| G | FR-019 to FR-023 | 61 | 10 | 42 | 0 | 9 | `2c9db1d` |
| H | FR-024, FR-025, FR-027, FR-028, FR-029, FR-032, FR-033, FR-034, FR-035, FR-037, FR-038 | 60 | 27 | 30 | 0 | 3 | `be60070` |
| Total | | 453 | 157 | 266 | 3 | 27 | |

## PRD versions after the pass

FR-001 2.1, FR-002 1.8, FR-003 2.20, FR-004 4.5, FR-005 3.8, FR-006 2.21, FR-007 1.17, FR-007B 1.17, FR-009 1.14, FR-010 2.15, FR-011 1.15, FR-012 2.18, FR-013 1.20, FR-015 1.31, FR-016 1.20, FR-017 2.21, FR-019 3.2, FR-020 2.19, FR-021 1.10, FR-022 2.27, FR-023 1.10, FR-024 2.2, FR-026 1.21, FR-027 1.8, FR-028 1.63, FR-029 1.19, FR-030 1.26, FR-031 1.7, FR-032 1.20, FR-033 2.7, FR-034 3.1, FR-035 1.6, FR-037 2.33, FR-038 1.7. Each PRD has one change-log row dated 2026-11-25. FR-008, FR-014, FR-018 and FR-025 were not edited.

## Graph

- Ten change-sets in `graph/changesets/`: `2026-11-25-crossfr-batch-a.yaml` to `-h.yaml`, plus `-a-fixes-b.yaml` and `-g-fixes-b.yaml` (rewording to clear near-duplicate rule statements).
- After the pass: 12,265 nodes, 2,955 fields, 1,279 enum values, 45,350 edges. Lint is 28, down from 29, because one stale hand-off note was cleared.

## Records

- Row-by-row outcomes: `plans/reports/logic-review-ledger.md`, section "Cross-FR pass (2026-11-25)".
- Two business defaults applied for owner review (329 aftercare participation starts On; 330 handover fee is a credit on the clinic balance record): `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md`.
- Follow-ups and not-changed leftovers: `plans/reports/implementation-backlog-261120.md`, section "Added 2026-11-25 from the cross-FR pass".
