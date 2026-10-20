# {Phase N} Test Run {NN} Summary — {YYYY-MM-DD}

> **Template.** The `manual-test-bug-sync` skill copies this file to `testing/manual/v{N}/phases/{phase-folder}/results/run-{NN}-{YYYY-MM-DD}/summary.md` when it creates a run. Do not fill it by hand. Rules: `testing/TEST-STRATEGY.md` §2.

## Run Control

| Field | Value |
|---|---|
| Plan / phase | {v2 / Phase 1} |
| Run | {run-01-2026-10-20} |
| Run type | {Full / Retest} |
| Started | {YYYY-MM-DD} |
| Previous run | {run-NN-YYYY-MM-DD or —} |
| Test guide | [test-guide.md](../../test-guide.md) |

## Batches in This Run

| Batch | Result file | Batch version |
|---|---|---|
| {B01} | [{B01-pr01-slug}]({B01-pr01-slug}.md) | {1.0} |

## Progress Summary

Refreshed by the `manual-test-bug-sync` skill (`summary`).

| Batch | Total | Pass | Fail | Blocked | Not tested | Open bugs | Last tested |
|---|---|---|---|---|---|---|---|
| {B01} | {n} | 0 | 0 | 0 | {n} | 0 | — |
| **Total** | **{n}** | **0** | **0** | **0** | **{n}** | **0** | **—** |

## Run Notes

- {Build, environment, or scope notes for this run; for a retest run, the retest list it covers}
