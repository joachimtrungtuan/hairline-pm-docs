# FR-005 Dependency Reconciliation

**Date**: 2026-09-16
**Status**: Documentation contracts reconciled; implementation reconciliation and consolidated verification remain pending
**Decision owner**: Product Owner

## Summary

Applied the Product Owner-selected resolutions from the FR-005 verification of `CR-FR005-20260915-01`. The documentation now presents one consistent Parent Quote → Quote Option → Option/Date-Price structure, with FR-005 composing one option and one applicable date-price record into the patient-visible Subquote.

## Updated Contracts

- **FR-004 v2.8**: Added the canonical quote hierarchy before the detailed specification and replaced remaining direct-parent-quote acceptance wording with FR-005 subquote acceptance and deterministic selected-parent, sibling, and competing-parent outcomes.
- **FR-006 v2.2**: Added terminal `Payment Window Expired` behavior after the payment hold expires. The slot is released, payment against that accepted selection is blocked, the acceptance snapshot remains immutable, and recovery requires a new current subquote or audited admin intervention.
- **FR-006 v2.3 and traceability**: Clarified in FR-006 and the system PRD that acceptance reserves the chosen appointment while payment confirms the booking; synchronized CR-FR006-20260915-01, SRC-MTG-002 routing, the source register, and the September 15 FR-006 update log to the current contract.
- **FR-020 v2.1 and FR-030 v1.6**: Extended the existing `quote.accepted` event with explicit FR-005 outcome codes and recipient-scoped privacy allowlists. `quote.declined` is not used for sibling Not Selected or competing-parent cancellation outcomes.
- **FR-022 v2.13**: Changed FR-005 Screen 1 criteria from flat quotes to complete subquotes, added Appointment Date sorting, and bound Date Range filtering to the selected Option/Date-Price Record.
- **FR-005 v2.2**: Aligned quote questions with FR-012's Patient ↔ Provider channel through the dedicated Messages/Inbox, and aligned the accepted-slot hold with FR-006/A-09 as configurable with a 48-hour default.

## Boundaries

- No implementation source, schema, API, migration, or test files were changed.
- FR-005 and FR-006 remain pending consolidated verification and implementation reconciliation.
- Existing unrelated workspace changes were preserved.

## Validation

- Targeted searches confirm the old direct-quote acceptance and post-expiry retry wording was removed from the affected contracts.
- FR-020 and FR-030 expose the same three outcome codes and recipient privacy rules.
- FR-005 and FR-022 both include Appointment Date in the subquote sort contract.
- FR-005, FR-012, and the system PRD now agree that quote questions use Patient ↔ Provider messaging, while Hairline Support remains outside the FR-012 MVP channel.
- FR-005, FR-006, and the system PRD now describe the accepted-slot hold as configurable with a 48-hour default.
- `git diff --check` passes for the `local-docs` repository.
