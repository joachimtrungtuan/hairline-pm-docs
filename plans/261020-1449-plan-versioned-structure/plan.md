# Plan-Versioned Structure for Product Plans and Manual Testing

**Status:** Done (2026-10-20)
**Created:** 2026-10-20

## Outcome

Versioning belongs to the product plan. Each plan version owns its own phase set. Manual testing mirrors the plan version and phase, keeps batch files as scaffolds, and records every test run as a new set of result files.

## Decisions (user-approved 2026-10-20)

- `product-plans/v1/` = May 2026 launch plan (sprints as phases); `product-plans/v2/` = September 2026 release roadmap (four phases). Folders are `v<major>`; minor versions live inside the documents.
- The September roadmap report moves to `product-plans/v2/plan.md`. Readiness backlogs keep a date prefix inside their phase folder.
- `testing/manual/v2/phases/<phase>/` holds `test-guide.md` (test-only content; scope links to the product plan), `batches/` (scaffolds, never filled in), and `results/run-<NN>-<YYYY-MM-DD>/` (one result file per batch run, plus `summary.md`).
- Each test run creates a new set of result files. Bug ID and Bug status carry forward from the previous run; earlier runs are frozen once a newer run exists.
- Batch Control `Phase / plan version` becomes `Plan / phase` plus `Batch version`. Tester copies in the old format are accepted as plan v2, batch version 1.x.
- Skills updated on explicit user request: `manual-test-bug-sync`, `sprint-readiness-reporting`, `create-bug-tasks`.
- Plane QA tasks HAIRL-1545 to HAIRL-1550 get their GitHub links updated after the change is pushed.

## Moves

| From | To |
|---|---|
| `product-plans/2026-05-13/launch-plan.md` | `product-plans/v1/plan.md` |
| `product-plans/2026-MM-DD/sprint-N-readiness-fix-backlog.md` | `product-plans/v1/phases/sprint-N/2026-MM-DD-readiness-fix-backlog.md` |
| `reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md` | `product-plans/v2/plan.md` |
| `product-plans/2026-MM-DD/phase-N-readiness-fix-backlog.md` | `product-plans/v2/phases/<phase-folder>/2026-MM-DD-readiness-fix-backlog.md` |
| `testing/manual/phases/<phase>/v1.0/plan.md` | `testing/manual/v2/phases/<phase>/test-guide.md` |
| `testing/manual/phases/<phase>/v1.0/batches/*` | `testing/manual/v2/phases/<phase>/batches/*` |
| `testing/templates/manual-phase-plan-template.md` | `testing/templates/manual-test-guide-template.md` |

New: `testing/templates/manual-run-summary-template.md`.

## Steps

1. `git mv` every file above; rewrite relative links in all live docs (update logs left as history).
2. Update `TEST-STRATEGY.md`, testing READMEs, templates, test guides, batch control rows, `INDEX.md`, `README.md`.
3. Update the three skills (docs, script, tests); run the script tests.
4. Verify links; write the update log.
5. Commit and push (after user confirmation), then update the six Plane tasks (dry-run first).

## Acceptance

- No live doc links to a moved path; link check passes.
- Batch case tables unchanged byte-for-byte except the Batch Control version rows and the fill-in instructions.
- `batch-sync.py` tests pass, including new-run creation and legacy-copy acceptance.
