# Bug Status Lifecycle

Source: `local-docs/testing/TEST-STRATEGY.md` section 5 and 8. This file adds the transition and Plane-mapping rules the script enforces.

## Statuses

| Status | Set by | Bug ID |
|---|---|---|
| `—` | Default, or tester retracting a flag | No |
| `Found` | Tester (in the returned copy) | No |
| `Logged` | This skill, after Plane creation | Yes |
| `Fixed - retest` | This skill, from Plane state | Yes |
| `Closed` | This skill, from a retest Pass | Yes |
| `Reopened` | This skill, from a retest Fail or a user-approved regression | Yes |

## Allowed Transitions (`set-bug`)

| From | To |
|---|---|
| `—` | `Found` |
| `Found` | `Logged` (new Plane key required), `—` |
| `Logged` | `Fixed - retest` |
| `Reopened` | `Fixed - retest` |
| `Fixed - retest` | `Closed`, `Reopened` |
| `Closed` | `Reopened` |

Any other change needs `--force`, used only when the user explicitly instructs it (for example, Plane cancelled the bug and the user decides to reset the row to `—`).

## Bug ID Cell

- Holds readable Plane keys such as `HAIRL-1234`, never internal UUIDs.
- A bug split into FE and BE tasks by `create-bug-tasks` stores both keys comma-separated: `HAIRL-1600, HAIRL-1601`. No `|` character.
- `Reopened` reuses the same key(s). A new key is written only when the user decides a failure is a different bug.

## Plane State Mapping (`apply-states`)

Applies to rows in `Logged`, `Reopened`, or `Fixed - retest` with a Bug ID. The state group comes from the states JSON or from `plane-values.json` (`states[].group`).

| Plane state | Action |
|---|---|
| Group `completed` (for example `Finished`, `Done - Not Tested`) | `fixed` |
| `Waiting for Deployment` (name override, group `completed`) | `hold`: fixed in code but not deployed, so do not send for retest |
| Group `cancelled` (for example `Cancelled`, won't fix) | `cancelled`: ask the user |
| Groups `backlog`, `unstarted`, `started`, `triage` | `open`: no change |
| Key missing from the states file or state name unknown | `unknown`: ask the user |

Row decision:

| Row status | Key actions | Outcome |
|---|---|---|
| `Logged` or `Reopened` | Every key `fixed` | Set `Fixed - retest` |
| Any | Any key `cancelled` | Ask (`plane_cancelled`) |
| Any | Any key `unknown` | Ask (`plane_state_unknown`) |
| `Fixed - retest` | Not every key `fixed` | Ask (`plane_moved_back_after_fix`) |
| Any | Any key `hold` | No change (`awaiting_deployment`) |
| Any | Otherwise | No change (`not_resolved_in_plane`) |

Pass `--hold-state "<name>"` for any other Plane state the team uses to mean "fixed but not deployed". `apply-states` never sets `Closed`.

## Summary Counting

- Batch Summary `Total` excludes `Retired` cases, so Total = Pass + Fail + Blocked + Not tested.
- `Open bugs` counts rows whose Bug status is `Found`, `Logged`, `Fixed - retest`, or `Reopened`, plus `Fail` rows whose Bug status is still `Closed` (a regression not yet reopened), one per row even with two keys. This is the same "open bug" definition the phase exit criteria use (TEST-STRATEGY §5).
- `summary` lists each batch's `Fail` plus `Closed` rows as `fail_on_closed_bug`; `bugs` lists them with an action hint; `retest-list` returns them as `needs_reopen`. Ask the user whether to set `Reopened` (same Bug ID) or log a new bug.
- Run summary (`results/run-<NN>-<YYYY-MM-DD>/summary.md`) Progress Summary `Last tested` is the latest valid date in the batch, or `—`. The **Total** row sums counts and takes the latest date.
- Result files in the run but missing from the summary table are added before the **Total** row and reported as `added`; summary rows with no matching result file are reported as `unmatched_rows` and left as they are.
- A new run (`new-run`) carries each case's Bug ID and Bug status forward from the previous run, so the lifecycle continues across runs; results start empty.
