# API Flow Register — Formats

## Proposal Format (Phase 3)

Use this format when presenting a proposed flow to the user for confirmation. Do not write to the dictionary until the user confirms.

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
```

For update proposals, show only the changed steps with a before/after diff.

---

## Dictionary Entry Format (Phase 4)

Use this format when writing a confirmed flow entry to `api-flow-testing/references/flow-dictionary.md`.

```markdown
## Flow: [Flow Name]

**Registered:** YYYY-MM-DD
**Last updated:** YYYY-MM-DD
**Prerequisites:** [what must exist before step 1]
**Roles involved:** [Patient / Provider / Admin]

### Steps

| Step | Endpoint               | Auth     | Key Inputs                      | Expected Output                  | Expected Status |
|------|------------------------|----------|---------------------------------|----------------------------------|-----------------|
| 1    | POST /auth/login       | None     | Patient credentials             | PATIENT_TOKEN captured           | 200             |
| 2    | POST /inquiries        | Patient  | transplant_area_id, photos      | Inquiry ID captured              | 201             |

### State Transitions
- [Entity]: [from state] → [to state]

### Multi-Tenant Notes
- [Role boundary notes or cross-tenant test hooks]

### Known Edge Cases
- [edge case name]: [trigger + expected behavior]

### Known Error Paths
- [error name]: [trigger + expected status/message]

### Notes
- [Any caveats, dependencies, or prerequisites that aren't obvious]

---
```
