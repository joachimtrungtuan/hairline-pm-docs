# Hairline Testing Hub

Single home for all testing artifacts, manual and automated. Rules: [TEST-STRATEGY.md](TEST-STRATEGY.md).

## Where Things Are

| Folder | What it holds | Who uses it |
|---|---|---|
| [TEST-STRATEGY.md](TEST-STRATEGY.md) | Tracks, structure, versioning, case IDs, allowed values, tester workflow, bug lifecycle | Everyone; read first |
| [manual/v2/phases/](manual/v2/phases/) | Manual testing per product plan version (`v2` = September 2026 roadmap): one folder per phase with a test guide, batch scaffolds, and one results folder per test run | Plan owner, external tester |
| [templates/](templates/) | Blank test guide, batch scaffold, and run summary templates; copy, never fill in place | Anyone creating a test guide, batch, or run |
| [test-data/credentials/](test-data/credentials/) | Test accounts (`A#`, `S#`, `V#`, `P#`, `AF#` rows). Internal only. Placeholder list: `test-data/placeholder-registry.md` | Team; shared privately with the tester |
| [automated/](automated/README.md) | Web E2E framework and registry, API endpoint and flow material, Android flows | Testing skills, QA |
| [results/](results/README.md) | Dated reports and screenshots from the Android testing skills (API skills report in the conversation) | QA |
| [archive/](archive/README.md) | Pre-2026-10-19 plans and reports, kept unchanged | Reference only |

## Manual Testing: Current Plan Version (v2)

Phases come from the product plan, not from this folder: [product-plans/v2/plan.md](../product-plans/v2/plan.md), four-phase table. A new plan version gets a new `manual/v{N}/` folder with its own phase set.

| Phase | Test guide | Batch scaffolds | Test runs |
|---|---|---|---|
| 1. Controlled commercial pilot | [test-guide.md](manual/v2/phases/phase-1-controlled-commercial-pilot/test-guide.md) | [batches/](manual/v2/phases/phase-1-controlled-commercial-pilot/batches/) | `results/run-NN-YYYY-MM-DD/` (created per run) |
| 2. Clinical and patient operations | [test-guide.md](manual/v2/phases/phase-2-clinical-patient-operations/test-guide.md) | [batches/](manual/v2/phases/phase-2-clinical-patient-operations/batches/) | `results/run-NN-YYYY-MM-DD/` (created per run) |
| 3. Settlement and partner growth | [test-guide.md](manual/v2/phases/phase-3-settlement-partner-growth/test-guide.md) | [batches/](manual/v2/phases/phase-3-settlement-partner-growth/batches/) | `results/run-NN-YYYY-MM-DD/` (created per run) |
| 4. Scale and optimization | [test-guide.md](manual/v2/phases/phase-4-scale-optimization/test-guide.md) (skeleton) | none yet | none yet |

## Common Tasks

| I want to… | Do this |
|---|---|
| Start a manual test run | Create the run folder with the `manual-test-bug-sync` skill (`new-run`), open the phase `test-guide.md`, follow its run order, and fill the result copies in `results/run-NN-YYYY-MM-DD/`. Never fill the scaffolds in `batches/` |
| Merge results the tester sent back | Run the `manual-test-bug-sync` skill. Never paste results by hand |
| Log bugs from failed cases, check fix status, get the retest list | Run the `manual-test-bug-sync` skill |
| Add a test guide or batch for a phase | Copy from [templates/](templates/), then follow TEST-STRATEGY §2–4 |
| Change cases after scope changes, or start a new plan version | Follow TEST-STRATEGY §3 (versioning) |
| Run or register web E2E tests | `web-e2e-register` and `web-e2e-review` skills; [automated/web-e2e/](automated/web-e2e/) |
| Test an API endpoint or flow | `api-testing`, `api-flow-testing`, `api-flow-register` skills |
