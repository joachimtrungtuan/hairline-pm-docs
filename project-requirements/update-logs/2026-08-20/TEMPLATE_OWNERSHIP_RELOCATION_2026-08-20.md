# Template Ownership Relocation

**Date**: 2026-08-20
**Tracked owner**: `project-requirements/templates/`
**Compatibility path**: `.specify/templates/`

**Trigger**: Product-owner correction that every project template, including Spec Kit-compatible templates, must be managed from the project requirements documentation boundary.

---

## Decision Applied

- Moved `agent-file-template.md`, `checklist-template.md`, `plan-template.md`, `prd-template.md`, and `tasks-template.md` into `project-requirements/templates/` beside `change-request-template.md`.
- Replaced the previous physical `.specify/templates/` directory with a relative symlink to `../local-docs/project-requirements/templates`.
- Kept all template filenames unchanged so the existing Spec Kit script paths continue to resolve without script modifications.
- Changed `INDEX.md` so `project-requirements/templates/` is the canonical ownership surface and `.specify/templates/` is documented only as a compatibility path.

## Before and After

| Concern | Before | After |
|---|---|---|
| Physical ownership | Spec Kit templates lived under `.specify/templates/`; the Change Request template lived under project requirements | All templates live under `project-requirements/templates/` |
| Spec Kit lookup | Scripts read `.specify/templates/<filename>` directly | The same path resolves through the directory symlink |
| Versioned project management | Spec Kit templates sat outside the nested `local-docs` repository | Canonical template files are tracked with project requirements |

## Validation

- Recorded SHA-256 hashes before the move and confirmed identical content through both the canonical and compatibility paths afterwards.
- Confirmed `create-new-feature.sh`, `setup-plan.sh`, and `update-agent-context.sh` can resolve their existing template paths through the symlink.
- Confirmed all six template files are present under the canonical project-requirements directory.
- No Spec Kit script content changed.

## Portability Boundary

The canonical template files are tracked by the nested `local-docs` repository. The workspace-root `.specify/templates` symlink and the rest of `.specify` are outside that Git boundary, so provisioning a new full workspace must recreate the relative compatibility symlink when it installs the external Spec Kit tooling. A clone of `local-docs` alone still contains every canonical template but does not include the external `.specify` consumer surface.
