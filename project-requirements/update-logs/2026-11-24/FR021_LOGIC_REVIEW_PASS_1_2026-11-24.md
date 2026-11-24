# FR-021 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 1.7 to 1.8, with a graph change-set)
**Scope**: FR-021 Multi-Language and Localization PRD, applying the triaged findings of logic review pass 1.
**Source of findings**: `plans/reports/tester-261124-fr021-logic-p1.md`

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr021-i18n-localization/prd.md`

- One permission, Manage Localization (REQ-021-122), is defined once in Admin Editability. It covers non-English edits, import as draft and machine-translation drafts. The Super Admin holds it and may grant it to another admin role. The four protected operations (edit English source, change default locale, publish, rollback) stay Super Admin only. "Platform Admin" and bare "Admin" gating wording now reads "an admin holding the Manage Localization permission".
- Import into the English source locale is an English source edit with the REQ-021-020 controls; a new key through import needs an English value in the same file (REQ-021-123, REQ-021-094).
- When any import row is skipped for an error, only Import as Draft is offered. The main flow diagram, Rule 5, Screen 8 and REQ-021-095 agree, and Story 4 gains a matching scenario.
- Fallback chain is the selected locale, that locale's fallback locale, then always the English source locale (Rule 9). Screen 5 gains the Fallback locale control. The default locale must be Active.
- Preparation to Active is Super Admin only and needs a published bundle for every surface (REQ-021-125).
- Review Needed: marking happens after the English edit passes validation; the English edit dialog has the non-semantic checkbox; Screen 7 has Accept as reviewed; Review Needed does not block publish and the Screen 9 publish confirmation shows the count (REQ-021-124).
- One machine-translation flow: the main flow refers to Alternative Flow C1, which now has a connection check (failure sets status Error and stops), a preview-and-confirm step, job statuses (Queued, Running, Completed, Partially failed, Failed) and an Enable/Disable provider control on Screen 10.
- Screen 10 gains a Free-text translation panel (switch and monthly budget, uses the active machine-translation provider); REQ-021-119 and REQ-021-120 point to it. Provider-authored package names and descriptions join the REQ-021-119 free-text list.
- New General Module Rule 17 (REQ-021-126): provider and admin screens format dates and numbers by the selected locale; provider screens use the FR-032 provider timezone, admin screens the platform default. Story 6 now uses a GMT offset instead of a named timezone.
- UI language selectors show Active locales only; spoken-language and template-language lists show Active and Preparation locales (REQ-021-025, REQ-021-076).
- Admin-authored library text becomes key groups on Screens 6A and 6B (REQ-021-127); the FR-024 integration and dependency lines are aligned.
- Notification wording lives only in FR-030 templates: the Shared/Notification surface is removed from Screens 5, 7, 8 and 10, and REQ-021-115 states that FR-021 supplies the locale catalog and fallback order to FR-030.
- Version 1.8 change-log row and Last Updated added.

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr021-logic-p1-fixes.yaml`

- Adds six steps (STP-021-056 to 061) and six rules (REQ-021-122 to 127).
- Updates the statements of the rules reworded in the PRD, retitles four steps, and updates two field descriptions.
- Retires the duplicate main-flow machine-translation steps (STP-021-005, 006, 023, 024), turns `ENT-mt-job.status` into an enum with five values, and retires the `shared_notification` value on five surface fields.
- Rewires the patch, import and machine-translation step edges; adds missing `next`, `on`, `applies` and actor edges; adds `FR-021 references REQ-026-121` and `FR-021 references REQ-032-006`.
- Test-applied on a scratch copy of the graph with `--db`: "Applied change-set cs-20261124-105911-22c59d19: 228 change rows". The copy was deleted and the live graph was not touched.

## Not changed here

Neighbour rows are queued, not edited: FR-031 (Manage Localization permission row; Preparation-to-Active as Super Admin only), FR-026 (list FR-021 as a consumer in REQ-026-121), FR-030 and FR-032 (Active plus Preparation language lists; FR-030 confirms it reads no bundle), FR-014 (reference only), FR-024 (handled in its own pass). Minor observations from the review are left as leftovers for the implementation backlog.
