# {B01} — {Module code} {Module / function slice name}

> **Template.** Copy this file to `testing/manual/v{N}/phases/{phase-folder}/batches/{B01}-{module}-{slug}.md` as the batch scaffold, then replace every `{placeholder}` except Tester and Build tested. Remove this note in the copy. The scaffold is never filled in: each test run gets a result copy in `results/run-NN-YYYY-MM-DD/` (created by the `manual-test-bug-sync` skill). Rules: `testing/TEST-STRATEGY.md`.

## Batch Control

| Field | Value |
|---|---|
| Batch | {B01} |
| Plan / phase | v{N} / Phase {N} |
| Batch version | {1.0} |
| Module | {PR-01 — Auth & Team Management} |
| FRs | {FR-002, FR-031} |
| PRD sources | {Relative links to the PRD sections used} |
| Platform | {Provider dashboard / Admin dashboard} |
| Tester | {Name (YYYY-MM-DD)} |
| Build tested | {Build or version (YYYY-MM-DD)} |

## How to Fill In This File

Fill in the **result copy** for your run (`results/run-NN-YYYY-MM-DD/`), never the scaffold in `batches/`.

1. One tester runs a batch at a time; do not share a result copy with another tester during a run. Before starting, fill **Tester** (`Name (YYYY-MM-DD)`) and **Build tested** (`<build> (YYYY-MM-DD)`) in Batch Control, replacing the `{...}` placeholder. If the tester or build changes during the run, add the new entry after `; `, for example `Linh (2026-10-20); Minh (2026-10-22)`; never delete earlier entries.
2. Run cases in table order unless a case says otherwise.
3. In each case row, fill only these columns:
   - **Actual result / data**: what you observed and the exact values you entered, for example "Saved; status shows Draft; total 2,450 USD".
   - **Result**: `Not tested`, `Pass`, `Fail`, or `Blocked` (give the reason in Notes). `Retired` is set by the plan owner only.
   - **Notes**: usability observations (what you did, what happened, why it was confusing or slow), even when the case passes, plus any questions.
   - **Evidence**: links to your screenshots or recordings, separated by `, `. Upload each file to any file-sharing service you choose, with a link the team can open, named `<case base ID>-<YYYYMMDD>-<n>.<ext>` (run date, then a counter), for example `PR02-FR004-03-20261019-1.png`, so files from different runs never collide. Record only the links; do not send files with the batch.
   - **Bug status**: set `Found` when you see a bug; otherwise leave `—`.
   - **Last tested**: the date you ran the case, `YYYY-MM-DD`.
4. The team fills **Bug ID** and moves Bug status to `Logged`, `Fixed - retest`, `Closed`, or `Reopened`. Bug ID and Bug status carry over from the previous run. When you retest a `Fixed - retest` case, fill the result columns as usual and leave Bug status to the team.
5. Do not edit IDs (keep the ` r1` suffix), Batch Control version rows, titles, preconditions, test data, steps, or expected results, and do not use the vertical-bar character inside cells. Put questions or proposed changes in **Notes**.
6. Keep each case row on one physical line. For a line break inside a cell, type `<br>`; pressing Enter splits the row and the file is rejected.

## Flow Overview

{Plain-language description of the business flow under test, the actors, and how this batch fits the phase journey. Cite PRD flows, for example FR-002 › Main Flow 1.}

## Shared Preconditions

- {Environment, account state, or data that must exist before any case in this batch}

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| {DS-PR01-01} | {Valid invite} | {Email: newstaff+01@example.com; Role: Clinician} | {V1} |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| {PR01-FR002-01 r1} | {Owner invites a clinician} | {High} | {FR-002 › Main Flow 2, steps 1–5} | {Signed in as {V1}} | {DS-PR01-01} | {1. …<br>2. …<br>3. …} | {1. …<br>2. …} | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| {n} | 0 | 0 | 0 | {n} | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| {PR01-FR002-01} | r1 | {YYYY-MM-DD} | Created |
