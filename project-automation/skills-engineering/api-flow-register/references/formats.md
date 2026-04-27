# API Flow Register — Formats

## Proposal Format (Phase 3)

Use this format when presenting a proposed flow to the user for confirmation. Do not write profiles or indexes until the user confirms.

```
## Proposed Flow: [Flow Name]

**Prerequisites:** [what must exist before step 1]
**Roles involved:** Patient / Provider / Admin (list which apply)

### Steps

| Step | Endpoint               | Auth     | Key Inputs                        | Expected Output                  | Expected Status |
|------|------------------------|----------|-----------------------------------|----------------------------------|-----------------|
| 1    | POST /auth/login       | None     | Patient email + password          | PATIENT_TOKEN captured           | 200             |
| 2    | POST /inquiries        | Patient  | transplant_area_id, photo files   | Inquiry created, ID captured     | 201             |
| ...  |                        |          |                                   |                                  |                 |

### State Transitions
- [Entity]: [from state] → [to state]

### Multi-Tenant Notes
- [Any role boundary considerations for this flow]

### Known Edge Cases (if researched)
- [Edge case name]: [trigger condition and expected behavior]

### Known Error Paths (if researched)
- [Error name]: [trigger condition and expected status/message]

### Endpoint Profile Changes
- [endpoint]: [create/update/no change] — [brief reason]
```

For update proposals, show only the changed steps with a before/after diff.

---

## Flow Profile Format (Phase 4)

Use this format when writing a confirmed flow profile to `api-flow-testing/references/flow-profiles/<flow-name>.md`.

```markdown
# Flow: [Flow Name]

## Prerequisites

- [what must exist before step 1]

## Roles

[Patient / Provider / Admin]

## Endpoint Sequence

| Step | Endpoint | Endpoint Profile | Auth | Captures | Expected Status |
|---|---|---|---|---|---|
| 1 | `POST /auth/login` | `api-testing/references/endpoint-profiles/post-auth-login.md` | None | `TOKEN` | 200 |

## State Transitions

- [Entity]: [from state] -> [to state]

## Flow Rules

- [Flow-specific orchestration rule]

## Known Edge Cases

- [edge case name]: [trigger + expected behavior]

## Known Live Notes

- [Live finding or caveat]

## Related Endpoint Profiles

- `api-testing/references/endpoint-profiles/<profile>.md`
```

## Endpoint Profile Format (Phase 4)

Use this format when writing a confirmed endpoint profile to `api-testing/references/endpoint-profiles/<method-path>.md`.

```markdown
# [METHOD] /path

## Purpose

[What this endpoint does.]

## Auth

[None / Patient / Provider / Admin]. Include scope notes.

## Request

| Field | Type | Required | Notes |
|---|---|---|---|
| `field` | string | Yes | [note] |

## File Uploads

- Use bundled files from `api-testing/assets/` unless the user provides another file.
- Document exact multipart field names.

## Dynamic Resolvers

| Needed Value | Resolver |
|---|---|
| `ID` | `[METHOD] /resolver-endpoint` |

## Response Notes

- [Shape and important fields.]

## Captures

| Capture | Source | Notes |
|---|---|---|
| `CAPTURED_ID` | `data.id` | [note] |

## State Effects

- [Entity]: [from] -> [to]

## Known Errors

- [Error condition] -> [status/message]

## Live Notes

- [Reusable live finding.]

## Related Flows

- `api-flow-testing/references/flow-profiles/<flow>.md`
```
