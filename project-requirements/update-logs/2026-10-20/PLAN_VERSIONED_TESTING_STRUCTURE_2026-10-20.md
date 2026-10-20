# Plan-Versioned Product Plans and Manual Testing Structure

**Date:** 2026-10-20
**Type:** Structural documentation change (folder model, templates, three skills)
**Plan:** [plans/261020-1449-plan-versioned-structure/plan.md](../../../plans/261020-1449-plan-versioned-structure/plan.md)

## Why

Versioning belongs to the product plan, not to each test phase. Each plan version has its own phase set (v1 had five sprints, v2 has four phases). The old layout versioned each phase alone (`testing/manual/phases/<phase>/v1.0/`), kept plan files inside the testing folder, and had testers fill in the original batch files.

## What Changed

### Product plans

- `product-plans/v1/plan.md`: May 2026 launch plan (was `product-plans/2026-05-13/launch-plan.md`). Sprint readiness backlogs moved to `product-plans/v1/phases/sprint-N/<date>-readiness-fix-backlog.md`.
- `product-plans/v2/plan.md`: September 2026 release roadmap (was `reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md`). Phase readiness backlogs moved to `product-plans/v2/phases/<phase>/<date>-readiness-fix-backlog.md`.

### Manual testing

- `testing/manual/v2/phases/<phase>/` now holds `test-guide.md` (was `v1.0/plan.md`; scope links to the product plan), `batches/` (scaffolds, never filled in), and `results/run-<NN>-<YYYY-MM-DD>/` (one result copy per scaffold plus `summary.md`).
- Each test run creates a new set of result files. Bug ID and Bug status carry forward from the previous run; earlier runs are frozen.
- Batch Control row `Phase / plan version` replaced by `Plan / phase` (`v2 / Phase N`) and `Batch version` (`1.0`) in all 20 scaffolds. Case tables unchanged.
- Template `manual-phase-plan-template.md` renamed to `manual-test-guide-template.md`; new `manual-run-summary-template.md`.
- `TEST-STRATEGY.md`, testing READMEs, `INDEX.md`, root `README.md` and the archive README updated to the new paths and run workflow.

### Skills (updated on explicit user request)

- `manual-test-bug-sync`: new `new-run` command; hub is the result file in the latest run; `find-hub` adds `superseded_run`; `--plan` replaced by `--run`; scaffolds and earlier runs are write-protected (`--allow-frozen` on explicit request); tester copies in the old Batch Control format are accepted as plan v2, batch 1.0. Script tests: 25 pass.
- `sprint-readiness-reporting` and `create-bug-tasks`: paths and wording aligned to the new layout.

## Scope

36 file moves (`git mv`, history kept), one new template, link and text edits. No files deleted. Update logs and plans keep their old paths as history.

## Follow-up

- Plane QA tasks HAIRL-1545 to HAIRL-1550: descriptions updated after the push to link the Phase 1 test guide and batch files at the new paths (all links checked, HTTP 200). The MTG-002 review tasks HAIRL-1539 to HAIRL-1544 link only to unmoved files and were not changed.
- No test run exists yet. Create `run-01` for Phase 1 with `new-run` before the tester starts.
