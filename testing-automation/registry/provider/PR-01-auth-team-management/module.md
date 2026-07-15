# PR-01 — Auth & Team Management

**Surface:** Provider Dashboard
**Registry status:** Provider login suite `ACTIVE`
**Primary source:** `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md`

## Registered Functions

| Function ID | Title | Status | Cases |
| --- | --- | --- | --- |
| `PR-01-FN-001` | Provider login | `ACTIVE` | `PR-01-TC-0001` through `PR-01-TC-0006` |

The function verifies the approved Provider browser journey from role selection through authentication and arrival at the Provider Dashboard. The live PRDs remain authoritative; this index does not restate their requirements.

## Manual Run

Run the complete active Provider login function from `local-docs/testing-automation/`:

```bash
pnpm test:function PR-01 PR-01-FN-001
```

The command executes all six active cases. Use `--case <case-id>` only to diagnose or re-run one selected case.

## Governed Coverage Gaps

The function registry records four open requirements that are not yet safe or deterministic to automate:

- suspended Provider login and restriction banner;
- deactivated Provider login rejection;
- removed team-member access revocation;
- user/IP login throttling and lockout.

See the function's `test-cases.md` coverage matrix for the missing fixtures or isolation controls. These gaps must remain visible until they can be registered safely; they are not treated as passing coverage.
