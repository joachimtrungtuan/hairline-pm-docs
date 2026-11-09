# Requirements Graph and PRD Baseline Freeze

**Date:** 2026-11-08
**Type:** Documentation structure change (new requirements authority, baseline freeze)

## Summary

The requirements graph becomes the author of the functional requirements, and the 38 FR PRDs with their change requests are frozen as an immutable baseline that migration into the graph reads from.

## Requirements graph folder (introduced 2026-11-05)

`local-docs/project-requirements/graph/` was added on 2026-11-05 and had no update-log entry until now. It holds:

- `graph.db`: the SQLite graph (nodes, typed edges, fields, enum values, sources, append-only change history).
- `schema.yaml`: node types, edge verbs and enum values.
- `scripts/`: create, write, query, lint, export and render scripts with their tests.
- `viewer/`: the browser viewer for the graph export.
- `changesets/`: every change to the graph is applied as a change-set file.
- `README.md`: documents the folder, its scripts and the database rules.

FR-004 and FR-005 are loaded in the graph. The other FRs are not migrated yet.

## Review checklists (added today)

[`graph/checklists/`](../../graph/checklists/) was added today by Phase 1 of the requirements graph programme (all files version 1.0). It holds five files: `README.md`, `migrate-fr.md`, `completeness-check.md`, `source-priority.md` and `agent-brief-template.md`. Every repeated review task runs from one of these checklists. Later the same day `completeness-check.md` and `agent-brief-template.md` went to version 1.1 after the FR-005 completeness dry run; `graph/README.md` gained a `checklists/` bullet.

## Freeze

| Field | Value |
|---|---|
| Archive | root `archived/prd-baseline-2026-11-08/`, outside the `local-docs` repository |
| Git tag | `prd-frozen-2026-11-08` (annotated) |
| Source commit | `ce737db5c7fdf6946ada49bd8988605086161bd1` |
| Files | 117 copied: 38 `prd.md`, 76 change requests, 2 transcription notes, and one untracked `.DS_Store` |
| Checksums | `BASELINE.md` and `SHA256SUMS` in the archive; run `shasum -a 256 -c SHA256SUMS` there |

What the freeze means: the live PRDs are working copies. In Phase 9 they are re-rendered from the graph and the change request files leave the live FR folders; after that the CRs survive only in the archive. PRDs and CRs are not hand-edited. Every change goes through a graph change-set under `graph/changesets/`.

## Files changed

- Updated `INDEX.md` §B File Registry: one line for the graph folder. The freeze itself is an operational record (archive folder, tag, this log); the `functional-requirements/` folder carries no marker file and stays the final set for the dev team.
- Created this log and updated the update-logs README.

## Documentation impact

- No PRD, CR or system document content changed.
- No implementation source was modified.
