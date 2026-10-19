# Hairline Testing Hub

Single home for all testing artifacts, manual and automated. Rules: [TEST-STRATEGY.md](TEST-STRATEGY.md).

## Where Things Are

| Folder | What it holds | Who uses it |
|---|---|---|
| [TEST-STRATEGY.md](TEST-STRATEGY.md) | Tracks, structure, versioning, case IDs, allowed values, tester workflow, bug lifecycle | Everyone; read first |
| [manual/phases/](manual/phases/) | Manual test plans per release phase, one folder per plan version, split into module batches | Plan owner, external tester |
| [templates/](templates/) | Blank phase plan and batch templates; copy, never fill in place | Anyone creating a plan or batch |
| [test-data/credentials/](test-data/credentials/) | Test accounts (`A#`, `S#`, `V#`, `P#` rows). Internal only | Team; shared privately with the tester |
| [automated/](automated/README.md) | Web E2E framework and registry, API endpoint and flow material, Android flows | Testing skills, QA |
| [results/](results/README.md) | Dated reports from the API and Android testing skills | QA |
| [archive/](archive/README.md) | Pre-2026-10-19 plans and reports, kept unchanged | Reference only |

## Manual Testing Phases

| Phase | Folder | Current version |
|---|---|---|
| 1. Controlled commercial pilot | [phase-1-controlled-commercial-pilot/](manual/phases/phase-1-controlled-commercial-pilot/) | [v1.0 plan](manual/phases/phase-1-controlled-commercial-pilot/v1.0/plan.md) |
| 2. Clinical and patient operations | [phase-2-clinical-patient-operations/](manual/phases/phase-2-clinical-patient-operations/) | [v1.0 plan](manual/phases/phase-2-clinical-patient-operations/v1.0/plan.md) |
| 3. Settlement and partner growth | [phase-3-settlement-partner-growth/](manual/phases/phase-3-settlement-partner-growth/) | [v1.0 plan](manual/phases/phase-3-settlement-partner-growth/v1.0/plan.md) |
| 4. Scale and optimization | [phase-4-scale-optimization/](manual/phases/phase-4-scale-optimization/) | [v1.0 plan](manual/phases/phase-4-scale-optimization/v1.0/plan.md) (skeleton) |

Scope source: [release roadmap](../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md), four-phase table.

## Common Tasks

| I want to… | Do this |
|---|---|
| Start a manual test session | Open the phase `plan.md`, follow its run order, fill the batch files (see "How to Fill In This File" in each batch) |
| Merge results the tester sent back | Run the `manual-test-bug-sync` skill. Never paste results by hand |
| Log bugs from failed cases, check fix status, get the retest list | Run the `manual-test-bug-sync` skill |
| Add a new phase plan or batch | Copy from [templates/](templates/), then follow TEST-STRATEGY §2–4 |
| Change cases after scope changes | Follow TEST-STRATEGY §3 (versioning) |
| Run or register web E2E tests | `web-e2e-register` and `web-e2e-review` skills; [automated/web-e2e/](automated/web-e2e/) |
| Test an API endpoint or flow | `api-testing`, `api-flow-testing`, `api-flow-register` skills |
