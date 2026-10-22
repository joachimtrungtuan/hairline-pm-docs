# Deferred Backlog

The record of issues the team decided **not** to fix now, so they can be revisited later. Most
gaps and bugs go straight to planned tasks through other skills; only the ones the team pushes
back on ("not now", "too costly for this release", "not necessary yet") are recorded here, with
the reason and who decided.

Owned by the `deferred-backlog` skill (`project-automation/skills-engineering/deferred-backlog/`).
Edit these files through that skill so IDs, counts, and carry-forward stay consistent.

## Current version

**Current**: [v01-2026-10-22.md](v01-2026-10-22.md)

The current version is the only one that changes. New deferrals and resolutions go into it.
A version is cut only on demand: cutting freezes the current file and starts the next one with
every open item carried forward.

## Versions

| Version | File | Opened | Frozen | Carried in | New | Resolved | Open at freeze |
|---|---|---|---|---|---|---|---|
| v01 | [v01-2026-10-22.md](v01-2026-10-22.md) | 2026-10-22 | - | 0 | 7 | 0 | - |

## How items work

- **ID**: `DEF-nnn`, assigned once and never reused, stable across versions. Search any DEF ID
  to trace an item back to the version that first recorded it.
- **Sources**: any document, such as a code review gap (`FR-004/W3-G1`), a manual-test bug, or
  a readiness backlog row. One item may list several source IDs when they share a root cause.
- **Status**: `Open`, `Revisit due` (its revisit trigger has been met), `Resolved-fixed`,
  `Resolved-dropped` (no longer needed), or `Reopened → task` (moved to planned work).
- **Who reads it**: `code-review-conformance` Delta mode tags matching gaps `Deferred
  (DEF-nnn)` and never re-raises them; it flags items whose code now complies as candidates to
  resolve, but never resolves them itself.
