# Change Request: Global Provider Email Identity Rule

**Change Request ID**: CR-FR009-20261015-02
**Primary FR**: FR-009
**Triggering FR / Event**: FR-015 seventh verification pass (2026-10-15) found that FR-015 checked login email uniqueness only against Active and Suspended provider owners, while FR-009 enforced single-provider membership for team members. An owner email could therefore collide with another clinic's staff member or pending invitation
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.4 (proposed) to v1.5 (proposed)
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-015 (provider creation and owner login email) and FR-009 (team invitations) each had their own email rule, and neither covered the other's records. The Product Owner chose: (1) one global rule, owned by FR-009, covering Owners, team members, and pending invitations, which FR-015 references; (2) when a provider is Deactivated, its staff and pending-invitation emails are freed for reuse, matching FR-015 Rule 4 for owner emails, and the old records stay archived.

## Baseline State

**Source version**: FR-009 v1.4 (proposed), Rule 3, REQ-009-008, A3, Screen 2 and Screen 12 email validation; FR-015 v1.14 Rule 4, Screen 2 Step 1, Screen 3 Tab 1, REQ-015-014

- FR-009: an email cannot belong to more than one provider team at a time (team members only; Owners and Deactivated providers not mentioned).
- FR-015: Login Email must be unique among Active and Suspended providers only; staff and pending invitations not checked.

## Approved State

**Target version**: [FR-009 v1.5 (proposed)](prd.md), Rule 3, REQ-009-008, A3, Screens 2 and 12, FR-015 dependency note; [FR-015 v1.15](../fr015-provider-management/prd.md), Rule 4, Screen 2 Step 1, Tab 1, REQ-015-014, duplicate-email edge cases

- An email belongs to at most one provider organization at a time, across Owner, team member, and pending invitation.
- FR-009 invitations, FR-015 provider creation, and FR-015 owner login-email edits all apply this rule.
- Memberships and pending invitations of a Deactivated provider do not count; their emails are freed for reuse. Old records stay archived and are not reactivated by reuse.
- FR-015 keeps its own Contact Email rule (Active and Suspended providers only); that rule is unchanged.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Rule owner | FR-009 (staff) and FR-015 (owners) separately | FR-009 Rule 3 / REQ-009-008; FR-015 references it | One source of truth |
| Records checked | FR-009: team members; FR-015: provider owners | Owners, team members, and pending invitations across all providers | Prevent owner/staff collisions |
| Deactivated providers | FR-015 frees owner emails; FR-009 silent | Owner, staff, and pending-invitation emails all freed; records archived | Product Owner decision |
| A3 trigger | Email belongs to another provider team | Email belongs to another provider as Owner, member, or pending invitation (Deactivated providers excluded) | Match the global rule |

## Scope and Impact

### In Scope

- FR-009 Rule 3, REQ-009-008, A3 trigger, Screen 2 and Screen 12 email validation, FR-015 dependency note, header, and change log row.
- FR-015 email validation rows, Rule 4, REQ-015-014, and duplicate-email edge cases (reference to the FR-009 rule).
- This FR-local Change Request.

### Out of Scope

- FR-015 Contact Email uniqueness (unchanged).
- Patient account emails.
- System PRD and technical specification updates.
- Source code, API, or live configuration changes.

### Affected Contracts

- **PRD owner**: [FR-009](prd.md) — Rule 3, REQ-009-008, A3, Screens 2 and 12, Dependencies (FR-015).
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) v1.15 — Screen 2 Step 1, Screen 3 Tab 1, Rule 4, REQ-015-014, edge cases.
- **System documents**: [System data schema](../../system-data-schema.md) v1.6.0 — §3 `users` and §4 `provider_users` business rules state the global rule across owner accounts, team members, and pending `provider_staff_invitations`; the enforcement mechanism is left to reconciliation.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code or runtime behavior was inspected or changed.
- **Required assessment**: A single email check shared by provider creation, owner login-email edit, and staff invitation; inclusion of pending invitations; exclusion of Deactivated providers' records; freeing of emails on deactivation without deleting archived records.
- **Compatibility / rollout risk**: Existing data may already contain an email used by both an owner and another provider's staff member or invitation; such conflicts must be found and resolved before the rule is enforced.
- **Data migration**: Audit for existing cross-provider email conflicts; scope database unique constraints so archived records of Deactivated providers do not block reuse.

## Acceptance and Validation

- Creating a provider with a login email that belongs to another provider's team member or pending invitation is blocked with an error.
- Editing an owner's login email to one used by another provider (Owner, member, or pending invitation) is blocked.
- Inviting an email that is another provider's Owner, member, or pending invitee shows the A3 blocking error.
- After a provider is Deactivated, its Owner, staff, and pending-invitation emails can be used for a new provider or invitation, and the old records remain visible as archived.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan, during FR-015 verification review.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-15; documentation delta only.
- **Decision evidence**: FR-015 seventh verification pass AskUserQuestion answers ("One global rule in FR-009", "Yes, freed on deactivation", "Apply all now").
- **PRD change log**: [FR-009 Appendix: Change Log](prd.md#appendix-change-log), v1.5 (proposed) dated 2026-10-15.
- **Update log**: [FR015_SEVENTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_SEVENTH_VERIFICATION_FIXES_2026-10-15.md).
- **Supersedes**: None.
- **Superseded by**: None.
