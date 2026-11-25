# Developer guide added; technical documents archived

**Date**: 2026-11-25
**Type**: Major (new document, archive, cross-document pointer alignment)

## What changed

- **New `DEVELOPER-GUIDE.md`** at the docs repo root: the entry point for developers and their AI agents. It lists the four repositories, states which documents are authoritative, and explains how to read the system picture, one FR in detail, and the requirements graph (model, viewer, queries), plus the steps for implementing a feature.
- **Archived** to `archived/technical-docs/` (with a README that says what replaces them): `project-requirements/system-technical-spec.md` and `project-requirements/system-data-schema.md`. The requirements graph (Entity and Field nodes) and the FR PRDs are now the source for the data model; neither file is maintained.
- **New `project-requirements/implementation-backlog.md`**: the per-FR list of open points left for the implementation phase, copied in from the programme's working reports so developers can read it; linked from the guide.
- **Removed**: `project-requirements/constitution-summary.md` (a stub left after the constitution consolidation) and the empty `project-requirements/plans/` folder.
- **Pointers repaired** so nothing live points at the archived files:
  - `project-requirements/constitution.md`: header note, C-DOC-2, Part D introduction, change-log line.
  - FR-014 PRD (version 3.24) and FR-015 PRD (version 1.32): one reference each, with change-log rows.
  - `project-notes/code-map-backend.md`: four lines now point to graph Entity nodes.
  - `INDEX.md` and `README.md`: task rows for the guide, the graph and the archive; registry tree; C.3 is now "Data model (requirements graph)", C.4 "Archived technical documents".
- **Protected files edited with the owner's double approval**:
  - Workspace-root `CLAUDE.md` and `AGENTS.md`: the default-read line now names the FR PRDs and the requirements graph.
  - `project-automation/skills-engineering/gen-code-map/references/generation-rules.md`: technical-spec step removed, models point to graph Entity nodes.
  - `project-automation/skills-engineering/code-review-conformance/references/checker-brief.md` and `item-derivation.md`: technical-spec mention removed.

## Checks

- Every path, node id and command in the guide was run or resolved against the repo and the graph (graph lint unchanged at 28).
- A search of live documents finds no remaining pointer to the two archived files outside history.

## Notes

- Left as history, not edited: skill plans under `project-automation/plans/`, `constitution-open-items.md` (cites the technical spec as evidence), `testing/archive/`, and earlier update logs.
- No requirement wording changed; no Change Request is needed.
