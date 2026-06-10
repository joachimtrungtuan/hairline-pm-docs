---
name: sprint-readiness-reporting
description: Create, scaffold, update, and re-test Hairline sprint readiness reports and fix backlogs. Use when the user wants to start a new sprint readiness report from the launch plan, continue an existing readiness report, record product-review findings, convert user-reported system state into report updates, or resume blocked follow-up checks after earlier blockers are fixed.
---

# Sprint Readiness Reporting

## Overview

Run the Hairline sprint-readiness workflow from context resolution through report updates. Reuse the active readiness-report path and launch-plan path inside the same conversation, keep the report aligned to launch-plan scope, and record product-review findings with evidence-backed backlog rows.

## Read This Skill

Load these files only when needed:

- `references/context-resolution.md` before resolving or reusing the readiness report path or launch-plan path
- `references/flow-basic-vs-advanced.md` before choosing how deep the investigation should go
- `references/reporting-rules.md` before writing or rewriting any report content
- `references/blocked-follow-up.md` when the current task is blocked by an earlier defect or when the user says a blocker was fixed and re-test should resume
- `assets/sprint-readiness-fix-backlog-template.md` only when Flow 1 needs to create a new report scaffold

## Hard Rules

- Treat `local-docs/product-plans/.../sprint-*-readiness-*.md` or equivalent user-confirmed readiness/backlog file as the primary output target
- Resolve exactly two context files before substantial work: the readiness report file and the launch-plan file
- Reuse those two paths for the rest of the same conversation once they have been resolved; do not ask again unless the user changes scope
- Do not ask for a file path immediately if the conversation already names one or if one obvious candidate can be discovered locally
- Anchor scope, modules, stories, and deferrals to the launch plan; do not silently reinterpret sprint scope
- Treat all user-reported information first as a report about current system state; decide later whether it belongs in `Review Notes`, `Remaining Fixes`, `Sprint-Level Blockers`, or `Not For This Sprint`
- Only record a confirmed defect row when there is enough evidence to describe the symptom, reproduction path, actual outcome, and expected outcome clearly
- Never use local screenshot paths as evidence links; use only persistent uploaded URLs, stable report paths, or explicit API/log evidence
- If a screenshot would materially help but no persistent URL exists yet, leave `Evidence Link` as `TBD` and ask the user for the uploaded raw URL
- Read PRDs, source code, and APIs only as needed to clarify expected behavior or gather stronger evidence; do not modify product code
- When reporting code or API evidence, point to the smallest relevant surface instead of dumping wide code scans
- After significant edits in `local-docs/`, update the project update log according to `references/reporting-rules.md`

## Workflow Decision

1. Resolve context with Flow 0.
2. If no readiness report exists yet for the requested sprint, run Flow 1.
3. If the user is providing a straightforward observation, status update, or narrow bug report, start with Flow 2.
4. If expected behavior is unclear, the issue spans multiple surfaces, the user explicitly asks for deeper checking, or source/API evidence is needed, use Flow 3.
5. If the task is blocked by an earlier defect or the user wants to continue checks after a blocker was fixed, run the blocked-follow-up subflow through Flow 2 or Flow 3 rather than inventing a separate reporting format.

## Flow 0: Resolve Context

Follow `references/context-resolution.md`.

Outcome required before deeper work:

- one resolved readiness-report path
- one resolved launch-plan path

Resolution order:

1. Use the explicit path already named in the current user message.
2. Else reuse the path already resolved earlier in the same conversation.
3. Else search `local-docs/product-plans/` for the most likely readiness report and launch plan candidates.
4. Ask the user only if multiple plausible candidates remain or no confident candidate exists.

Do not keep re-asking for these paths once they are settled in the same conversation.

## Flow 1: Create Scaffold From Launch Plan

Use this flow when the user wants to start a new sprint readiness report or when the sprint report does not exist yet.

1. Resolve the target readiness-report path and launch-plan path through Flow 0.
2. Copy `assets/sprint-readiness-fix-backlog-template.md` into the requested sprint folder under `local-docs/product-plans/YYYY-MM-DD/`.
3. Read only the relevant sprint section from the launch plan.
4. Fill the scaffold sections that must mirror the launch plan:
   - Document Control & Sprint Summary
   - Modules In Scope
   - User Stories In Scope
   - Explicitly Deferred / Out Of Scope
5. Create one module subsection per in-scope module in `2.2 Module Fix Backlog`.
6. Seed placeholder rows only where the workflow requires sprint-level evidence gaps or known deferred checks; mark them `Review pending`.
7. Preserve the separation between placeholders/evidence gaps and confirmed product defects.

Use the template wording as the structural baseline. Adjust only sprint-specific values and rows required by the launch plan.

## Flow 2: Basic Report Update

Use this flow when the user provides a narrow observation and the report can be updated without deep investigation.

Follow `references/flow-basic-vs-advanced.md` and `references/reporting-rules.md`.

1. Resolve the active readiness report through Flow 0.
2. Read the relevant module section only.
3. Interpret the user input as one of these update types:
   - completion/progress note
   - confirmed issue with enough direct evidence
   - evidence gap or placeholder reminder
   - blocked follow-up note
   - out-of-scope note
4. Update the smallest correct location:
   - `Review Notes` when the user is reporting working coverage, current state, limits, or blocked checks
   - `Remaining Fixes` when the issue still requires developer action
   - `Sprint-Level Blockers` when the problem blocks sprint DoD, staging validation, or a cross-module journey
   - `Not For This Sprint` when the finding is real but outside current sprint commitments
5. Keep the row or note operational:
   - symptom
   - concise reproduction path
   - actual outcome
   - expected outcome
   - evidence link or `TBD`
6. Update the daily log if the edit is significant enough to change project documentation state.

Use Flow 2 by default for short, direct observations. Escalate to Flow 3 only when the evidence or expected behavior is still unclear.

## Flow 3: Advanced Investigation Update

Use this flow when the issue is structurally ambiguous, crosses tenants or surfaces, or needs stronger grounding in PRD, code, or APIs.

Follow `references/flow-basic-vs-advanced.md`, `references/reporting-rules.md`, and `references/blocked-follow-up.md` when applicable.

1. Resolve the active readiness report and launch plan through Flow 0.
2. Identify the affected scope:
   - sprint/module
   - tenant/surface
   - feature or FR
3. Read the minimum PRD context needed to define expected behavior.
4. If product behavior still needs clarification, do targeted source-code review:
   - open only the relevant frontend/backend files
   - identify likely data source, route, controller, component, or state path
   - do not modify code
5. If data contract or runtime state must be verified, run targeted API checks using approved workflows or direct endpoint inspection.
6. Distill the result into one of these outcomes:
   - the issue is confirmed and should become or update a backlog row
   - the user report is actually a progress note and should update `Review Notes`
   - the issue remains unconfirmed and should stay as `Review pending` or blocked follow-up
7. Update the report with both product evidence and, when useful, supporting code/API evidence.

Do not over-investigate simple issues. The purpose of Flow 3 is to resolve ambiguity efficiently, not to turn every report into a full audit.

## Blocked-Follow-Up Subflow

Use this subflow when current-sprint checks cannot be completed because an earlier defect or missing system state blocks the path, or when the user says the blocker has been fixed and the report should be resumed.

Follow `references/blocked-follow-up.md`.

When a blocker prevents completion:

1. Record the confirmed blocker itself in `Remaining Fixes` or `Sprint-Level Blockers`.
2. Update `Review Notes` to say which deeper checks are currently blocked.
3. If the blocked checks matter for future re-test, keep a dedicated `Review pending` checkpoint row describing what must be re-tested after the blocker is cleared.

When the user later says the blocker is fixed:

1. Locate the earlier blocker row and the blocked-follow-up notes/checkpoint row.
2. Decide whether Flow 2 is enough or whether Flow 3 must re-verify through PRD/code/API.
3. Re-run only the blocked checks that were deferred earlier.
4. Update the report cleanly:
   - remove or rewrite outdated blocked notes
   - convert the checkpoint row into a confirmed issue if a new defect is found
   - or replace the checkpoint with pass coverage in `Review Notes` if the blocked path now works

Do not leave stale blocker notes in the report once the blocker has been re-tested and superseded.

## Finish Conditions

Before finishing:

- confirm the right report file was updated
- confirm launch-plan scope was not drifted
- confirm status wording matches the conventions in `references/reporting-rules.md`
- confirm evidence links do not use local screenshot paths
- confirm blocked-follow-up notes and rows remain consistent with current reality
- confirm the update log was created or appended when required
