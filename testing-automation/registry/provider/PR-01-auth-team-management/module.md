# PR-01 — Auth & Team Management

**Surface:** Provider Dashboard
**Registry status:** Provider login suite `ACTIVE`; Team directory and invitation-management suite `DRAFT`
**Primary source:** `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md`

## Registered Functions

| Function ID | Title | Status | Cases |
| --- | --- | --- | --- |
| `PR-01-FN-001` | Provider login | `ACTIVE` | `PR-01-TC-0001` through `PR-01-TC-0006` |
| `PR-01-FN-002` | Team directory and invitation management | `DRAFT` | `PR-01-TC-0007` through `PR-01-TC-0024` |

The login function verifies the approved Provider browser journey from role selection through authentication and arrival at the Provider Dashboard. The draft Team function groups the Team directory, invite-team-member, and invitation-management surfaces that share `/team`; invitation acceptance through a mailbox remains a separate later flow. The live PRDs remain authoritative.

## Manual Run

Run the complete active Provider login function from `local-docs/testing-automation/`:

```bash
pnpm test:function PR-01 PR-01-FN-001
```

The command executes all six active cases. Use `--case <case-id>` only to diagnose or re-run one selected case.

The draft Team function is intentionally excluded from the normal interactive console until validation and activation. During an explicitly approved controlled validation, run:

```bash
pnpm test:function PR-01 PR-01-FN-002 --allow-draft
```

## Governed Coverage Gaps

The function registry records four open requirements that are not yet safe or deterministic to automate:

- suspended Provider login and restriction banner;
- deactivated Provider login rejection;
- removed team-member access revocation;
- user/IP login throttling and lockout.

The Team function separately records nine governed gaps for unsafe or unavailable fixtures such as role-specific accounts, Provider isolation, seat/rate boundaries, expired invitations, and concurrency. See each function's `test-cases.md` coverage matrix for the missing fixtures or isolation controls. Gaps are never treated as passing coverage.
