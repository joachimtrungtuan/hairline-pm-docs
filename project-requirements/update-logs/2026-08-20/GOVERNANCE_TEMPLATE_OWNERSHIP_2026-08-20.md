# Governance Alignment for Template Ownership

**Date**: 2026-08-20
**Documents**:
- Workspace-root `CLAUDE.md`
- Workspace-root `AGENTS.md`
- `INDEX.md`
- `README.md`

**Trigger**: Project-owner decision that only the cross-agent governance entrypoints remain at the workspace root while documentation authority stays under `local-docs/`.

---

## Decision Applied

- Kept `CLAUDE.md` and `AGENTS.md` as the root governance entrypoints.
- Kept `INDEX.md`, documentation onboarding, templates, Change Requests, and update logs under `local-docs/` rather than creating competing root copies.
- Declared `project-requirements/templates/` as the only canonical template directory.
- Preserved `.specify/templates` as a workspace-root compatibility symlink for existing Spec Kit paths; it is not a second source of template content.
- Added the major-event Change Request threshold and the separation between documentation approval and implementation reconciliation to both governance files and human onboarding.

## Alternative Considered

Adopting the governance skill's generic root `INDEX.md` and root `update-logs/` layout was rejected because this document-focused project already owns those surfaces inside its nested `local-docs` repository. Duplicating them would introduce competing navigation and history sources.

## Validation

- Confirmed `CLAUDE.md` and `AGENTS.md` remain byte-identical after the runtime-neutral governance update.
- Confirmed `.specify/templates` resolves to `../local-docs/project-requirements/templates` and its canonical template files remain accessible through both paths.
- Confirmed `INDEX.md` and `README.md` point to the canonical template and Change Request locations.
- The generic governance validator still reports compatibility findings because this project intentionally keeps `INDEX.md` and update logs under `local-docs/`, and its established index also carries task/scaffold routing beyond the validator's location-only format. Pre-existing model-tier and platform-section warnings remain outside this scoped ownership update.
