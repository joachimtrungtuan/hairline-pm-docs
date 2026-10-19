# Testing Hub Consolidation and Phase Manual Test Plans

**Date**: 2026-10-19
**Update Type**: Major — structural reorganization of all testing artifacts, new test strategy and templates, phase manual test plans v1.0, new `manual-test-bug-sync` skill
**Scope source**: `reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md` (four-phase roadmap)

Paths are relative to `local-docs/`.

## 1. Summary

All testing material now lives under one hub, `testing/`. Old plans and mobile test reports were moved there unchanged, test material owned by the testing skills moved out of the skill folders, and new versioned manual test plans were written for the provider and admin dashboards, following the release roadmap phases. The external tester now gets one plan per phase and one batch file per module, and each batch file doubles as the report they fill in. A new skill merges the tester's filled files back and runs the bug lifecycle with Plane.

## 2. Structural Changes

| Before | After |
|---|---|
| `testing-automation/` | `testing/automated/web-e2e/` (runtime config and docs paths updated; unit tests 40/40 pass) |
| `testing-plans/testing-credentials/` | `testing/test-data/credentials/` |
| `testing-plans/2026-01-27` to `2026-04-09` | `testing/archive/testing-plans/` (unchanged) |
| Mobile test reports in `reports/2026-03-27` to `2026-04-22` (9 files) | `testing/archive/reports/` (unchanged) |
| `api-testing/references` and `assets` test material | `testing/automated/api/endpoints/` |
| `api-flow-testing/references` flow material | `testing/automated/api/flows/` |
| `android-flow-test/references` flows, `android-emulator-qa/references/datasets.json` | `testing/automated/android/` |

Skill SKILL.md files stay in place with path-only edits (api-testing, api-flow-testing, api-flow-register, android-emulator-qa, android-flow-test, android-flow-register, web-e2e-register, web-e2e-review). Android QA report output now goes to `testing/results/YYYY-MM-DD/`. The web E2E `TESTING-CONSTITUTION.md` Amendment Log records the relocation (version unchanged).

## 3. New Documents

- `testing/README.md`: hub index.
- `testing/TEST-STRATEGY.md`: tracks, structure, versioning, case ID format `<MODULE><NN>-FR<NNN>-<SEQ> r<REV>`, result and bug status values, tester workflow, bug lifecycle.
- `testing/templates/`: `manual-phase-plan-template.md` and `manual-batch-template.md` (one case per table row; tester-fillable result columns plus Bug ID and Bug status).
- `testing/archive/README.md`, `testing/results/README.md`, `testing/automated/README.md`.
- `project-automation/skills-engineering/manual-test-bug-sync/`: new skill (symlinked into `.claude/skills` and `.agents/skills`) with a stdlib `scripts/batch-sync.py` for validate, diff, merge, bug write-back, retest list, and summary refresh.

## 4. Manual Test Plans v1.0

| Phase | Batches | Cases |
|---|---|---|
| Phase 1 — Controlled commercial pilot | B01 A-02 onboarding, B02 PR-01 team access, B03 PR-06 profile and pricing, B04 A-09 access and inquiry config, B05 PR-02 inquiry and quote, B06 A-01 oversight | 114 |
| Phase 2 — Clinical and patient operations | B01 PR-03 treatment, B02 A-01 booking and treatment intervention, B03 PR-04 aftercare, B04 A-03 aftercare, B05 A-04 travel, B06 A-05 invoice and refund, B07 PR-07 messaging, B08 A-10 support | 128 |
| Phase 3 — Settlement and partner growth | B01 PR-05 earnings and promotions, B02 A-05 reconciliation and payouts, B03 A-06 promotions, B04 A-07 affiliates | 73 |
| Phase 4 — Scale and optimization | Five planned batches; plan skeleton only | Not written |

Cases were written fresh from the FR PRDs (Business Workflows, Screen Specifications, Business Rules); nothing was carried over from the old plans or readiness backlogs. The patient mobile app is out of scope.

A cold dry run of Phase 1 B05 showed that a tester without project context could not run cases as written. Two fixes followed before any batch was issued:

- Tester fill-in rules were rewritten in the batch template, TEST-STRATEGY §7, and every batch: the exact columns the tester fills, evidence file naming, and that the team owns Bug ID and later bug statuses.
- Every case in Phases 1–3 was revised for self-sufficiency: concrete data values, named upload files, navigation paths, numbered expected results mapped to steps, timing tolerances, named cross-batch dependencies, and team-prepared setup items for states the tester cannot create (scheduled jobs, webhooks, patient-app actions). Case IDs stay at `r1` because no case had been issued.

## 5. Open Items

- PRD gaps and conflicts found while writing cases are listed in the session report to the Product Owner (for example FR-016 vs FR-031 on Super Admin count, FR-016 vs FR-003 on admin medical edits, FR-009 vs FR-031 on member removal).
- Test accounts and setup items the team must create are listed in each plan's §3 (for example `{A2}`–`{A7}`, `{S3}`, `{S4}`, `{P8}`, `{V4}`, `{AF1}`–`{AF13}`, invite mailboxes) and in each batch's Shared Preconditions. The plan owner contact and the provider dashboard URL are not yet filled in.
- Plane state reads for `manual-test-bug-sync` need a read-only script in `plane-api-commands` (frozen; proposal pending) or states pasted by the user.
