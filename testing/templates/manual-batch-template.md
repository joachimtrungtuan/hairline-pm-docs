# {B01} — {Module code} {Module / function slice name}

> **Template.** Copy this file to `testing/manual/phases/{phase-folder}/v{major}.0/batches/{B01}-{module}-{slug}.md`, then replace every `{placeholder}`. Remove this note in the copy. Rules: `testing/TEST-STRATEGY.md`.

## Batch Control

| Field | Value |
|---|---|
| Batch | {B01} |
| Phase / plan version | Phase {N} / v{1.0} |
| Module | {PR-01 — Auth & Team Management} |
| FRs | {FR-002, FR-031} |
| PRD sources | {Relative links to the PRD sections used} |
| Platform | {Provider dashboard / Admin dashboard} |
| Tester | {Name} |
| Build tested | {Version or date} |

## How to Fill In This File

1. Run cases in table order unless a case says otherwise.
2. Fill only: **Actual result / data**, **Result**, **Notes**, **Evidence**, **Bug status**, **Last tested**.
3. **Result** values: `Not tested`, `Pass`, `Fail`, `Blocked`. **Bug status** values: `—`, `Found`, `Logged`, `Fixed - retest`, `Closed`, `Reopened` (set `Found` when you see a bug; the team logs it in Plane).
4. Put usability observations in **Notes**: what you did, what happened, and why it was confusing or slow, even when the case passes.
5. Do not edit IDs, steps, or expected results, and do not use the vertical-bar character inside cells. Put questions in **Notes**.

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
