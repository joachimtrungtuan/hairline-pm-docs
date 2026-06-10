# Blocked Follow-Up

Use this reference when a planned sprint check cannot be finished because an earlier bug or missing state blocks the path.

## When To Mark A Check As Blocked

Mark a check as blocked when:

- the sprint should include that validation
- the current path cannot be completed because a previous step fails first
- continuing would not produce reliable evidence for the deeper check

Typical examples:

- role-boundary testing is blocked because invited staff land in the wrong admin/dashboard surface
- suspend/remove lifecycle testing is blocked because the dedicated suspend flow is not wired
- downstream onboarding checks are blocked because activation link or first login is broken

## How To Record A Blocked Follow-Up

Use two layers together:

### 1. Confirm the blocker itself

Record the real defect row that is preventing the later check.

### 2. Preserve the deferred follow-up

Record the blocked follow-up in both places when useful:

- `Review Notes`: mention exactly which checks are blocked
- `Remaining Fixes`: keep a `Review pending` checkpoint row when future re-test could otherwise be forgotten

The checkpoint row is not the blocker itself. It is the reminder that deeper validation still remains after the blocker is fixed.

## How To Resume After A Blocker Is Fixed

When the user says the blocker is fixed:

1. Find the original blocker row.
2. Find the blocked follow-up note and any `Review pending` checkpoint row.
3. Decide whether re-test can be handled through:
   - Flow 2 for straightforward confirmation
   - Flow 3 for deeper PRD/code/API re-verification
4. Re-run only the blocked checks that were previously deferred.
5. Update the report:
   - rewrite or remove outdated blocked wording
   - convert the checkpoint into a confirmed issue if a new problem is found
   - or replace it with pass coverage in `Review Notes` if the re-test now works

## Wording Rules

Good blocked note shape:

- “Role-boundary verification remains blocked because invited staff currently land in the admin-style dashboard surface instead of a provider-scoped role view.”

Good re-test checkpoint shape:

- “Follow-up PR-01 coverage is still required after the current team-management blockers are fixed.”

Bad pattern:

- vague wording that does not say which earlier defect is blocking which later check

## Anti-Patterns

- Do not treat blocked follow-up as a confirmed defect unless there is a separate actual defect to record
- Do not leave stale blocked notes after the blocker has already been re-tested
- Do not create a second blocker row that duplicates the original one just to remember re-test work
