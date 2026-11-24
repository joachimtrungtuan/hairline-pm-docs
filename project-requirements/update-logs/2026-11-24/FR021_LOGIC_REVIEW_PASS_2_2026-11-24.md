# FR-021 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 1.8 to 1.9, with a graph change-set)
**Scope**: FR-021 Multi-Language and Localization PRD, applying the triaged findings of logic review pass 2 (the final pass).
**Source of findings**: `plans/reports/tester-261124-fr021-logic-p2.md`

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr021-i18n-localization/prd.md`

- Import decision follows rows skipped for an error: a file with warnings only still goes to the Import decision; the main flow, Rule 5 and the Screen 8 rows use the same wording.
- English source import: Screen 8 gains a Change reason field; only Import as Draft is offered for the English source locale (REQ-021-123); it is published later from Screen 9.
- New keys come only from an import into the English source locale, with the English value in that file; an unknown key in any other locale's file is an error. The "explicit permission to create new registry keys" wording is removed (REQ-021-094).
- Any move of a locale to Active (from Preparation or from Inactive) is Super Admin only and needs a published bundle for every surface; Active to Preparation is not offered (REQ-021-125, REQ-021-046, REQ-021-006).
- Default locale: shown to a user with no stored language preference whose device language is not supported (REQ-021-049). A failed bundle fetch uses the cached bundle, else the English source bundle (REQ-021-114). Notification templates follow the Rule 9 order (REQ-021-115). The Screen 1 notice says "fallback language".
- Rule 18 (REQ-021-128): after a rollback the registry's published values follow the rolled-back version, drafts stay drafts, and each publish builds from the active bundle plus the drafts in scope.
- Admin screens use the admin's local timezone (REQ-026-050) in Rule 17 and REQ-021-126.
- Free-text translation (REQ-021-119, REQ-021-120): provider, blank or missing provider, budget in the platform currency per calendar month in UTC, zero stops translation, Super Admin notified once at the limit.
- Manage Localization covers every Editable-by-Admin item except the Super Admin only ones; the free-text switch and budget, provider credentials and provider activation are Super Admin only (REQ-021-122, REQ-021-046, REQ-021-013a, Screen 10).
- Spoken-language and template-language lists show all catalog locales; an existing entry or template in a locale that becomes Inactive is kept (REQ-021-025, REQ-021-076).
- The FR-024 treatment form is the authoring screen for the English library text, exempt from the Super Admin only source-edit rule (REQ-021-127).
- Machine-translation job: created as Queued, run sets Running; a Failed job shows its error summary and ends (new Alternative Flow C1 branch); one job per language at a time (REQ-021-111).
- Screen 4 gains a rule and a main-flow step for locale status, default and fallback management; Screen 7 gains a Review Needed flag row; "fallback order" wording becomes "fallback locale".
- Version 1.9 change-log row and Last Updated added.

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr021-logic-p2-fixes.yaml`

- Adds two steps (STP-021-062, 063) and one rule (REQ-021-128).
- Rewires the Failed job branch and the import decision edges, moves provider actors to Super Admin, adds Super Admin to the English source import steps, adds two `shows` edges and `FR-021 references REQ-026-050`.
- Updates rule statements and titles, step titles, two field descriptions and the two free-text settings.
- Test-applied on a scratch copy of the graph with `--db`: "Applied change-set cs-20261124-112821-278d9c05: 92 change rows". Lint on the copy shows the same two findings as before (STP-021-036 and 040 sit on three Stages). The copy was deleted and the live graph was not touched.

## Not changed here

Neighbour rows are queued, not edited: FR-001 (default and fallback wording), FR-026 (list FR-021 as a consumer of REQ-026-050), FR-030 and FR-032 (all-catalog language lists), FR-024 (treatment form as English authoring screen). Owner defaults 198 to 203 are appended to `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md`.
