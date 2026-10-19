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
- `Open bugs` counts rows whose Bug status is `Found`, `Logged`, `Fixed - retest`, or `Reopened` (one per row, even with two keys).
- Plan Progress Summary `Last tested` is the latest valid date in the batch, or `—`. The **Total** row sums counts and takes the latest date.
- Batches found in `batches/` but missing from the plan table are added before the **Total** row and reported as `added`; plan rows with no matching batch file are reported as `unmatched_rows` and left as they are.
