# Change Request: Last-Save-Wins Edits, At-Rest Encryption of Provider Contact Data, and Seat Usage

**Change Request ID**: CR-FR015-20261027-01
**Primary FR**: FR-015
**Triggering FR / Event**: FR-015 dev-team follow-up questions F13, F15 and F17, Product Owner decision 2026-10-27; also aligns FR-009 (seat usage) and FR-032 (provider saves)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-26
**Decision Date**: 2026-10-27
**PRD Version Change**: v1.21 to v1.22 (FR-009 v1.5 to v1.6; FR-032 v1.12 to v1.13)
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner changed three verified FR-015 contracts after the dev team raised follow-up questions:

- **Concurrent edits (F15)**: optimistic locking is removed. The last save wins for admin saves (FR-015) and provider saves (FR-032), with no conflict message. The old rule covered only two admins, and FR-032 had no matching rule, so a provider save could still be overwritten without warning.
- **Encryption of provider contact data (F17)**: application-level encryption of email, phone and medical license number is removed. These values are protected by database/disk encryption at rest, HTTPS/TLS and access control. Application-level encryption would have broken the Screen 1 partial search and the global login email uniqueness check.
- **Seat usage (F13)**: seat usage counts accepted non-Owner team members plus invitations still pending. The Owner and expired invitations do not count. The old wording ("active members plus pending invitations") did not say whether the Owner counts, and the backend counts the Owner.

## Baseline State

**Source version**: FR-015 v1.21. The rules appear in User Scenarios & Testing, Edge Cases (concurrent edits and seat limit below team size); Implementation Notes, Security Considerations (Encryption); and Screen 2 Step 1 and Screen 3 Tab 1 (Seat Limit). FR-009 v1.5 Rule 6 and Screen 12 Seat Usage carry the matching seat rule.

- A second admin saving a stale provider profile got the error "Provider profile was modified by another admin. Please refresh and re-enter your changes." The stale save was rejected.
- Provider email, phone and medical license number were encrypted in the database with application-level encryption.
- Seat usage was "current members and pending invitations" (FR-009) or "active members plus pending invitations" (FR-015), with the Owner not addressed.

## Approved State

**Target version**: FR-015 v1.22, same headings; FR-009 v1.6; FR-032 v1.13.

- Admin and provider profile saves are last-save-wins. No conflict check runs and no conflict message is shown. Every save stays in the Tab 8 and FR-032 audit trail, so an overwritten value can be traced.
- Clarification 2026-10-28 (Product Owner): a save applies only the fields the user changed; untouched fields are not rewritten. Last save wins therefore applies only when two people change the same field. No conflict check or conflict message is added (FR-015 v1.23, FR-032 v1.14).
- Provider email, phone and medical license number are stored in the database protected by database/disk encryption at rest, HTTPS/TLS in transit and access control. They are not encrypted at application level. Uploaded documents keep AES-256 encryption at rest.
- Seat usage counts accepted non-Owner team members plus invitations still pending. The Owner and expired invitations do not count. The Seat Limit blocks invitations when seat usage reaches it.
- Clarification 2026-10-28 (Product Owner): "accepted non-Owner team members" means non-Owner team members with status Active or Suspended, and "invitations still pending" means invitations with status Pending that are not past expiry. The invitation and team member model behind this count is recorded in [CR-FR009-20261028-01](../fr009-provider-team-roles/change-request-2026-10-28-invitation-member-model.md).

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Concurrent provider profile edits (FR-015 Edge Cases; FR-032 Data & Privacy Rules) | Optimistic locking for admin saves; the stale save is rejected with a conflict message; no rule for provider saves | Last save wins for admin and provider saves; no conflict check or message; every save audited | One simple rule for both platforms; the lock did not cover provider saves |
| Provider contact data encryption (FR-015 Security Considerations) | Application-level encryption of email, phone and medical license number | Database/disk encryption at rest, HTTPS/TLS and access control | Keeps the Screen 1 partial search and the login email uniqueness check working |
| Seat usage (FR-015 Seat Limit fields and edge case; FR-009 Rule 6, Screen 2 Team Size Meter, Screen 12 Seat Usage) | Members (or active members) plus pending invitations; Owner not addressed | Accepted non-Owner team members plus pending invitations; Owner and expired invitations excluded | The Seat Limit is the number of staff the provider can invite; the Owner is not invited |

## Scope and Impact

### In Scope

- The FR-015 concurrent-edit rule and the matching FR-032 provider save rule.
- How FR-015 protects provider email, phone and medical license number in storage.
- The seat usage definition in FR-015 and FR-009.

### Out of Scope

- Encryption of uploaded documents and bank details, which is unchanged.
- The Seat Limit range, default and the "Request more seats" flow, which are unchanged.
- The other FR-015 v1.22 changes, which are clarifications recorded only in the FR-015 change log.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr015-provider-management/prd.md`: Screen 2 Step 1 and Screen 3 Tab 1 Seat Limit; Implementation Notes, Security Considerations; Edge Cases (concurrent edits, seat limit below team size).
- **Related FRs**:
  - FR-009 v1.6: Rule 6, Screen 2 Team Size Meter, Screen 12 Seat Usage.
  - FR-032 v1.13: Data & Privacy Rules, Concurrent Edits Rule.
- **System documents**: `system-data-schema.md` and `system-technical-spec.md` should be checked for any encrypted-column or optimistic-lock version field on provider records. This change does not edit them.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed. The dev team reports that the backend counts the Owner in seat usage.
- **Required assessment**:
  - Remove any optimistic-lock version check and conflict error on provider profile saves.
  - Confirm provider email, phone and license number are stored as plain columns on encrypted storage, with search and the unique index working.
  - Change the seat usage count to exclude the Owner and expired invitations.
  - Tests for the three rules.
- **Compatibility / rollout risk**: Low. The current backend is a dev/test environment with no production data.
- **Data migration**: None expected, unless application-level encrypted values already exist; then decrypt them once.

## Acceptance and Validation

- When two admins, or an admin and the provider, save the same provider field one after the other, the later value is stored, no conflict message appears, and both saves are in the audit trail.
- The Screen 1 search finds a provider by part of its email or medical license number, and creating a provider with a login email already in use is blocked.
- For a provider with the Owner, 3 accepted team members, 2 pending invitations and 1 expired invitation, seat usage shows 5.
- Inviting is blocked once seat usage equals the Seat Limit.

## Approval and Traceability

- **Requested by**: Dev team, via `FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md` F13, F15 and F17.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-27.
- **Decision evidence**: Product Owner decisions of 2026-10-27 on the FR-015 follow-up questions; [FR-015 dev-team questions answer report](../../../reports/2026-10-26/fr015-dev-questions-answers-2026-10-26.md), §7.
- **PRD change log**: [FR-015 Appendix: Change Log](prd.md#appendix-change-log), v1.22 dated 2026-10-27; FR-009 v1.6 and FR-032 v1.13 change log rows.
- **Update log**: [FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md](../../update-logs/2026-10-27/FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md).
- **Supersedes**: None.
- **Superseded by**: None.
