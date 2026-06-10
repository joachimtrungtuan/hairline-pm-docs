# Basic vs Advanced Flow

Use this reference to choose the lightest workflow that can still produce a reliable report update.

## Choose Basic Flow When

Use Flow 2 when most of these are true:

- the user reports one narrow symptom or one narrow completion update
- the affected module or report section is already obvious
- the expected behavior is already clear from the current report, launch plan, or prior confirmed context
- the user already supplied enough evidence to describe the outcome
- no code or API verification is needed to avoid a wrong conclusion

Typical examples:

- add a screenshot URL to an existing row
- note that one working flow has now passed
- record a typo, dead button, broken link, or simple mismatch already visible from user evidence
- convert a short user report into `Review Notes`

## Escalate To Advanced Flow When

Use Flow 3 when any of these are true:

- the issue touches multiple surfaces or tenants
- the user explicitly asks to check PRD, codebase, or API
- expected behavior is unclear without reading the PRD
- the same symptom could come from multiple data models or API paths
- the report needs stronger evidence than the user has already provided
- the finding may actually be a structural contract issue rather than a UI-only issue

Typical examples:

- admin and provider surfaces disagree on the same dataset
- a role or ownership structure appears fundamentally wrong
- a user account lands in the wrong dashboard surface
- a UI symptom needs controller/route/API confirmation before it can be written confidently

## Token Discipline

- Default to Basic Flow for short, direct observations
- Do not open PRD, code, and API all at once unless the issue really demands all three
- Escalate progressively:
  1. read the relevant report/module section
  2. read PRD only if expected behavior needs clarification
  3. read code only if root-cause/evidence surface needs clarification
  4. call API only if runtime state or contract must be verified

## What Not To Do

- Do not over-think a simple report update into a full investigation
- Do not under-think a structural issue that could be recorded incorrectly without deeper checks
- Do not keep circling through the same files when a conclusion is already clear enough to update the report
