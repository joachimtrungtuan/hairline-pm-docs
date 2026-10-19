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
| Phase 1 — Controlled commercial pilot | B01 A-02 onboarding, B02 PR-01 team access, B03 PR-06 profile and pricing, B04 A-09 access and inquiry config, B05 PR-02 inquiry and quote, B06 A-01 oversight | 117 |
| Phase 2 — Clinical and patient operations | B01 PR-03 treatment, B02 A-01 booking and treatment intervention, B03 PR-04 aftercare, B04 A-03 aftercare, B05 A-04 travel, B06 A-05 invoice and refund, B07 PR-07 messaging, B08 A-10 support and message oversight | 138 (plus 1 retired) |
| Phase 3 — Settlement and partner growth | B01 PR-05 earnings and promotions, B02 A-05 reconciliation and payouts, B03 A-06 promotions, B04 A-07 affiliates, B05 A-02 commission settings, B06 PR-06 billing settings | 82 |
| Phase 4 — Scale and optimization | Six planned batches: the roadmap scope (analytics, monitoring, remaining configuration) plus B06 A-02 provider management leftovers; plan skeleton only | Not written |

Cases were written fresh from the FR PRDs (Business Workflows, Screen Specifications, Business Rules); nothing was carried over from the old plans or readiness backlogs. The patient mobile app is out of scope.

A cold dry run of Phase 1 B05 showed that a tester without project context could not run cases as written. Two fixes followed before any batch was issued:

- Tester fill-in rules were rewritten in the batch template, TEST-STRATEGY §7, and every batch: the exact columns the tester fills, evidence file naming, and that the team owns Bug ID and later bug statuses.
- Every case in Phases 1–3 was revised for self-sufficiency: concrete data values, named upload files, navigation paths, numbered expected results mapped to steps, timing tolerances, named cross-batch dependencies, and team-prepared setup items for states the tester cannot create (scheduled jobs, webhooks, patient-app actions). Case IDs stay at `r1` because no case had been issued.

## 5. Consistency Review Fixes

A second pass of fresh reviewers checked structure, rules, the skill script, each phase, and cross-phase consistency. The fixes below follow the user's decisions on that review.

- Shared dev environment with persistent data: Phase 2 and Phase 3 plans now start with a Phase handoff (for example reactivating `{V4}` and closing leftover Phase 1 inquiries). Phase 2 messaging uses new patients `{P9}`–`{P11}` with no earlier history.
- New single placeholder list: `testing/test-data/placeholder-registry.md`. `{S1}` is Clinical Staff in every phase; the Phase 1 custom role moved to new `{S2}`; Billing Viewer is `{A3}` everywhere.
- Currency (corrected in §7): quotes use the one system quote currency and only payout currencies differ per provider.
- Phase 3 payout statements are spread across providers and real billing cycles, and refunds deduct the provider share after commission (FR-017).
- Expectations not backed by a PRD were removed or rewritten as tester observations and flagged.
- Functions previously tested in no phase now have cases: scheduled status change (Phase 1 B01), FR-012 admin message oversight (Phase 2 B08), commission settings and billing settings (Phase 3 B05 and B06). Totals: 117, 135 and 82 cases, 334 unique IDs.
- Phase 4 skeleton narrowed to the roadmap scope; batches that repeated Phase 1 RBAC, Phase 2 support handling and Phase 3 billing settings were removed.
- `TEST-STRATEGY.md` and templates: evidence location and retest-safe naming, one-line rows with `<br>`, version vs revision bumps, accumulating Tester and Build entries, open-bug definition (includes Fixed - retest), uniform exit criteria.
- `manual-test-bug-sync` (frozen; user-approved): a retest Fail on a Closed bug is now flagged and counted as open, table parsing is hardened, and unit tests were added (15 pass). Twelve testing links in four skill files and one Android template path were corrected (user-approved).

## 6. Open Items

- PRD gaps and conflicts found while writing cases are listed in the session report to the Product Owner (for example FR-016 vs FR-031 on Super Admin count, FR-016 vs FR-003 on admin medical edits, FR-009 vs FR-031 on member removal).
- Test accounts and setup items the team must create are listed in each plan's §3 (for example `{A2}`–`{A7}`, `{S3}`, `{S4}`, `{P8}`, `{V4}`, `{AF1}`–`{AF13}`, invite mailboxes) and in each batch's Shared Preconditions. Each plan now has a Team Setup Checklist and the plan owner contact.
- Plane state reads for `manual-test-bug-sync` need a read-only script in `plane-api-commands` (frozen; proposal pending) or states pasted by the user.
- PRD conflicts and PRD-silent spots for the Product Owner: `reports/2026-10-19/manual-test-plan-prd-questions-for-po.md` (Q-01 to Q-26). Decisions there feed PRD updates and case revisions.

## 7. Open Issue Decisions

Decisions taken with the user on the remaining open items, applied before any plan was issued:

- **Currency follows the PRDs.** Quotes, prices, invoices and refunds use the FR-029 system default currency (FR-026, FR-004, FR-024), set to GBP for testing by setup item CUR-GBP. Payout currency is per provider (FR-017): `{V1}` GBP, `{V2}` EUR at a team-prepared locked rate (Phase 3 setup FX-1). This corrects the earlier per-provider quote currency.
- **PRD conflicts stay testable.** The soft-deleted quote must leave the default provider list, and the Archived filter is a tester observation (FR-004 vs FR-022). Promotion Resume is still tested (FR-019). Both are on the PO question list.
- **Evidence is cloud links only.** Testers upload screenshots and recordings to the team's cloud evidence folder and record links. No evidence is committed. `TEST-STRATEGY.md`, the batch template, every batch and `manual-test-bug-sync` (frozen; user-approved) were updated. The script now warns `evidence_not_link` (15 tests pass).
- **One tester per batch run.**
- **Phase 2 coverage:** new cases PR03-FR010-20 and -21 (reminders and overdue flag), PR04-FR011-14 (clinician assignment, observation), A04-FR008-13 (passport carry-over after transfer). PR03-FR010-05 is retired because FR-003 prevents its setup (PO Q-21). Patients `{P12}`–`{P28}` take the setup records that broke FR-003's one-active-inquiry rule.
- **Phase 3 BK-19:** the team completes BK-19 on the day ST-15 is generated, and the missed-booking cases run before a later statement can include it.
- **Phase 4:** featured providers, provider closure requests and "Login as Provider" moved into Phase 4 as planned batch B06.
- **Plan owner contact** filled in every plan and the registry. A Team Setup Checklist was added to each of Phase 1 to 3.
- Totals: Phase 1 117, Phase 2 138 (plus 1 retired), Phase 3 82; 338 unique IDs; 20/20 batches validate with no warnings.

- PO question report: Q-01 decided as deferred until the client's updated payout requirements are in the PRDs (payouts are Phase 3 scope); Q-02 decided as payout currency for FR-017 Screens 9 and 10 (current test handling stands; FR-017 line 1150 wording needs a PRD correction). Q-03 stays open.
