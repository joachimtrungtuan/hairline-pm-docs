# Reporting Rules

Use this reference immediately before writing or rewriting a readiness report.

## Source-Of-Truth Order

1. active readiness report file
2. active launch-plan file
3. relevant PRD for expected behavior
4. user-supplied evidence
5. targeted code/API evidence

Do not let source-code guesses override launch-plan scope or PRD expectations.

## Classify User Input By Meaning

Treat every user message first as a report about current system state. Then decide where it belongs.

### 1. Completion or progress note

Use `Review Notes` when the user is saying something now works, partially works, or was checked successfully.

Typical phrases:

- “đã tạo thành công”
- “flow này khá ổn”
- “đăng nhập được”
- “đã check xong phần này”

### 2. Confirmed issue

Use `Remaining Fixes` or `Sprint-Level Blockers` when the system still needs a fix.

A confirmed issue row should have:

- one concrete problem
- reproducible path
- actual outcome
- expected outcome
- evidence link or `TBD`

### 3. Evidence gap or scaffold reminder

Use `Review pending` when the row exists as a placeholder, a deferred re-test checkpoint, or a reminder that the product still has not been checked.

### 4. Blocked follow-up

Use `Review Notes` plus a `Review pending` checkpoint row when a later check should exist but is currently blocked by an earlier defect.

### 5. Out-of-scope finding

Use `Not For This Sprint` when the item is real but should not become a current-sprint commitment.

## Status Rules

Use only these `Task Status` values in the readiness backlog:

- `Review pending`
- `Recorded only`
- `Task created (HAIRL-123)`

Interpretation:

- `Review pending` = placeholder, evidence gap, or blocked re-test checkpoint
- `Recorded only` = confirmed issue from real review evidence, but not yet turned into a Plane task
- `Task created (HAIRL-123)` = implementation task exists and the Plane key is known

Do not invent extra status labels inside this report.

## Evidence Rules

- Never use local screenshot file paths
- Prefer persistent uploaded screenshot URLs
- Accept stable API or log references when screenshots are not the main evidence
- Use `TBD` temporarily only when the issue is already clear enough to record but the persistent evidence URL is still missing
- If the screenshot materially matters and no uploaded URL exists yet, ask the user to upload it

## Writing Rules For Backlog Rows

Each confirmed issue row should stay independently understandable.

Minimum row quality:

- `Flow / Story` or `Area` clearly identifies the affected journey
- `Issue` states one core problem
- `Steps to Reproduce` are concise and ordered
- `Actual Outcome` describes observed behavior
- `Expected Outcome` describes required behavior from launch plan, DoD, or PRD
- `Notes` capture environment, account, scope limit, or code/API evidence when useful

Formatting rules:

- Use `<br>` inside long cells
- Keep one row focused on one fixable problem
- Split different problems into separate rows even if they were found in the same session

## Scope-Attribution Rules

- If the evidence comes from Admin dashboard testing, record it under the Admin module unless the same issue was directly confirmed in another tenant
- Confirm `PR-01`, `PR-06`, or other Provider rows only when the Provider dashboard itself was actually tested
- Use cross-tenant notes only when evidence truly spans more than one surface

## Code And API Evidence Rules

- Read code and APIs to support the report, not to replace product evidence
- When writing code evidence, cite the smallest relevant surface such as a controller, query path, component, or route
- When writing API evidence, describe what the endpoint returned and why that matters to the report
- Only claim likely root cause when the evidence is strong enough; otherwise phrase it as a likely source or mismatch

## Update Log Rules

After significant edits in `local-docs/`:

- create a same-day update log file when no same-day log exists yet for this work
- otherwise append a concise bullet to the same-day relevant log
- update `local-docs/project-requirements/update-logs/README.md` when a new log file is created

## Anti-Patterns

- Do not overclaim a confirmed bug when only an evidence gap exists
- Do not collapse multiple defects into one vague row
- Do not paste implementation speculation into the `Issue` field
- Do not create Plane-style ownership tracking columns inside the readiness report
