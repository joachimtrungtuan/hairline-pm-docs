# Validation And Merge Rules

These are the rules `scripts/batch-sync.py` applies in `validate`, `diff`, and `merge`. Use this file to explain results to the user; do not re-implement the checks by hand.

## Column Ownership

| Owner | Columns | Merge behavior |
|---|---|---|
| Plan owner (definition) | ID, Title, Priority, PRD flow ref, Preconditions, Test data, Steps, Expected result | Tester edits reject the case and are reported as proposals |
| Tester | Actual result / data, Result, Notes, Evidence, Bug status, Last tested | Merged under the rules below |
| Team | Bug ID | Tester blank is ignored (hub is newer); a different non-blank value rejects the case |
| Batch Control | Tester, Build tested | Accumulated: tester entries (`Name (YYYY-MM-DD)`, separated by `; `) not already in the hub are appended to the hub value; a `{placeholder}` hub value is replaced. Never overwritten |
| Batch Control | Every other field | Edits reported as proposals, never merged |
| Other sections | Title, How to Fill In, Flow Overview, Shared Preconditions, Test Data Sets, Case Change Log | Edits reported as proposals (whitespace-insensitive comparison), never merged. When the tester copy has an older minor version, differences are reported as `section_stale` (the copy predates a team edit), not as proposals |
| Computed | Batch Summary | Ignored in the tester copy; recomputed from the hub after merge |

## File-Level Errors (Nothing Merges)

| Code | Meaning |
|---|---|
| `missing_section`, `missing_table`, `bad_table` | `## Batch Control` or `## Test Cases` missing or malformed |
| `noncanonical_header` | Hub Test Cases header differs from the template's 15 columns |
| `header_changed` | Tester renamed, added, removed, or reordered columns |
| `column_count`, `pipe_in_cell` | A row has the wrong number of cells: a vertical-bar character (plain or backslash-escaped) typed in a cell, a deleted cell, or a real line break that split the row (use `<br>`) |
| `bad_case_id`, `duplicate_case` | ID not `<MODULE><NN>-FR<NNN>-<SEQ> r<REV>` (module `P`, `PR`, `A`, or `S` plus two digits, no letter suffix) or repeated |
| `batch_mismatch`, `version_mismatch` | Different Batch ID, phase, or major version |
| `minor_version_mismatch` | Same major, different minor. Error unless the user approves `--allow-minor-mismatch` |

`find-hub` also reports `frozen_version` when a newer major version folder exists for the phase: the old folder is frozen and must not receive results.

## Case-Level Errors (Case Rejected)

| Code | Rule |
|---|---|
| `stale_revision` | Tester copy has an older `r<REV>` than the hub: the case changed after the copy was issued. Results are not merged; the tester reruns the current revision. No `definition_changed` is reported for it |
| `revision_mismatch` | Tester copy has a newer `r<REV>` than the hub |
| `column_shift_suspected` | Cells appear shifted, usually a vertical-bar typed in a cell plus a deleted cell keeping the count at 15: Evidence holds free text with spaces, or two or more of Result, Bug status, and Last tested are invalid. Fix the row in the tester copy |
| `definition_changed` | A definition column differs (hub and tester values are in the output) |
| `team_column_changed` | Tester wrote a different Bug ID |
| `bad_result` | Result not in `Not tested`, `Pass`, `Fail`, `Blocked` |
| `bad_bug_status` | Bug status not in `—`, `Found`, `Logged`, `Fixed - retest`, `Closed`, `Reopened` |
| `bad_date` | Last tested not a real `YYYY-MM-DD` date |
| `last_tested_missing` | Result `Pass`, `Fail`, or `Blocked` without Last tested |
| `tester_set_retired` | Only the plan owner sets `Retired` |
| `case_retired` | Hub case is `Retired`; tester results are not merged |
| `bug_id_required` | A `Logged`, `Fixed - retest`, `Closed`, or `Reopened` status without any Bug ID |

Unknown cases (in the tester copy, not the hub) are listed as proposals and block a full merge. Missing cases (in the hub, not the tester copy) are left unchanged and reported.

## Normalization (Warning Only)

Trivially equivalent values are normalized and reported: different letter case, hyphen or en-dash variants (`Fixed – retest`, `fixed-retest`), `-` or `N/A` for `—`, empty Result as `Not tested`, empty Bug status as `—`. `<br/>`, `<br />`, and `<BR>` are treated as `<br>` everywhere, so they never count as a definition edit. Anything else is an error, for example `Passed`.

Other warnings:

- `fail_without_actual`, `blocked_without_reason`, `fail_without_bug_flag` (ask whether to log), `future_date`.
- `tester_bug_status_ignored`: the tester copy shows a team status that differs from the hub; the hub wins.
- `open_bug_case_passed`: case passed while its bug is still `Logged` or `Reopened`; status kept, confirm with the team.
- `fail_on_closed_bug`: a `Fail` result on a row whose bug is `Closed` (a regression); paired with the `closed_bug_failed_again` conflict, and reported by `bugs` and `summary` for hub rows.
- `evidence_name`: an Evidence entry is neither a link nor named `<case base ID>-<YYYYMMDD>-<n>.<ext>` (checked only when Evidence changed).
- `control_field_blank`: Tester or Build tested is blank or a `{placeholder}` although the copy has run results.
- `control_entry_format`: a Tester or Build tested entry is not in `Name (YYYY-MM-DD)` form.
- `tester_changed`: the copy adds a tester name not seen before in the hub; confirm the new tester.
- `section_stale`: see Column Ownership.

## Conflict Rules

Run columns are Actual result / data, Result, Notes, Evidence, Last tested. For each run column that differs:

1. The hub cell is empty (or `Not tested`): take the tester value.
2. The tester's Last tested is later than the hub's (or the hub has none): take the tester value. Retests overwrite in place; git keeps history.
3. Otherwise the hub already holds the same or a later run: conflict `hub_has_same_or_newer_run`.

Bug status, after the run decision:

| Hub status | Tester run | Result |
|---|---|---|
| `Fixed - retest` | Newer, Pass | `Closed` |
| `Fixed - retest` | Newer, Fail | `Reopened` (same Bug ID) |
| `—` or `Found` | Tester sets `—` or `Found` | Tester value |
| `Logged`, `Reopened`, `Fixed - retest` | Anything else | Hub kept (team-owned) |
| `Closed` | Newer, Fail | Conflict `closed_bug_failed_again` plus warning `fail_on_closed_bug` (decided from the hub status, whatever status the tester copy shows) |

## Resolutions

Pass `--resolve "<case base ID>=<choice>"` to `diff` and `merge` (repeatable; the revision suffix is optional):

- `tester`: take every differing run column from the tester copy. A `Fixed - retest` row still moves to `Closed` or `Reopened` by result.
- `hub`: keep the hub row unchanged.
- `reopen`: only for `closed_bug_failed_again`; take the tester run and set `Reopened` with the same Bug ID. If the user says it is a different bug, keep `hub` and log the new bug through a new case or an explicit `set-bug --force` instruction from the user.

## Merge Modes

- Default: merge only when there are no file errors, rejected cases, unresolved conflicts, or unknown cases.
- `--partial`: merge clean cases; skip rejected and conflicted ones. Use only after the user agrees.
- `--apply` requires `--expect-sha` equal to the `hub_sha256` of the preview the user confirmed.
