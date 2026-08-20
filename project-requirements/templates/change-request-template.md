# Change Request: [Short Decision Title]

**Change Request ID**: CR-[FR]-[YYYYMMDD]-[sequence]
**Primary FR**: FR-###
**Triggering FR / Event**: FR-### or approved requirement restructure
**Decision Status**: Proposed / Approved / Rejected / Superseded
**Implementation Reconciliation**: Not assessed / Required / In progress / Verified
**Requested Date**: YYYY-MM-DD
**Decision Date**: YYYY-MM-DD or Pending
**PRD Version Change**: vX.Y to vX.Y
**Related Commit(s)**: commit hash or Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

[State the approved product decision and why this Change Request exists.]

## Baseline State

**Source version**: [PRD version and stable heading]

[Describe the verified or implemented contract before this request.]

## Approved State

**Target version**: [PRD version and stable heading]

[Describe the approved contract after this request. Point to the updated PRD instead of duplicating full implementation detail.]

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| [Workflow, rule, screen, entity, event, dependency, or interface] | [Previous contract] | [Approved contract] | [Decision rationale] |

## Scope and Impact

### In Scope

- [Changed product contract]

### Out of Scope

- [Explicit boundary]

### Affected Contracts

- **PRD owner**: `path/to/prd.md` — [stable heading or requirement ID]
- **Related FRs**: [FR identifiers and handoff]
- **System documents**: [system PRD, schema, technical specification, or none]

### Implementation Reconciliation

- **Existing implementation evidence**: [Not assessed, or link to current evidence]
- **Required assessment**: [Code, API, data, notification, permissions, UI, migration, or test surfaces to compare]
- **Compatibility / rollout risk**: [Risk and safe transition boundary]
- **Data migration**: None / Required / To be assessed

## Acceptance and Validation

- [Observable acceptance condition]
- [Cross-FR contract check]
- [Required implementation or regression evidence before marking reconciliation Verified]

## Approval and Traceability

- **Requested by**: [Role or name]
- **Approved by**: [Role or name]
- **Decision evidence**: [Meeting, issue, transcript, approval message, or update log]
- **PRD change log**: [Version row]
- **Update log**: [Relative link]
- **Supersedes**: None or prior Change Request ID
- **Superseded by**: None or later Change Request ID
