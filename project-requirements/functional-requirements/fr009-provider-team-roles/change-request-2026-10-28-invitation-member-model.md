# Change Request: Invitation and Team Member Model, Seat Usage, and Suspended Provider Invitations

**Change Request ID**: CR-FR009-20261028-01
**Primary FR**: FR-009
**Triggering FR / Event**: FR-015 backend confirmations, Product Owner decision 2026-10-28; refines the seat usage rule of CR-FR015-20261027-01
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-28
**Decision Date**: 2026-10-28
**PRD Version Change**: v1.6 to v1.7 (FR-015 v1.22 to v1.23)
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner fixed how an invited person is represented and how seats are counted:

- **Invitation and member model**: an invited person exists only as an invitation (Pending, Accepted, Expired, Cancelled) until they accept. A team member record is created only when the invitation is accepted. Team member statuses are Active, Suspended, and Removed. "Invited" is only the badge that team lists show for a Pending invitation row; it is not a team member status.
- **Seat usage**: seat usage counts non-Owner team members with status Active or Suspended plus invitations with status Pending that are not past `expires_at`. Each person is counted once. The Owner, Removed members, and Expired, Cancelled, or Accepted invitations do not count. A Suspended member keeps the seat; only removal frees it.
- **Suspended provider team management**: while the provider organization is Suspended, its Team page is view-only. Provider users cannot invite, resend an invitation, change a role, suspend, or remove a member, and the Team page shows "Your account is suspended. Team changes are unavailable. Please contact support." Admin invitations to a Suspended or Deactivated provider were already blocked (REQ-009-024).
- **Stored member statuses** (follow-up decision, 2026-10-28): the stored team member statuses are `active`, `suspended`, and `inactive`. `inactive` means Removed and is kept for compatibility. Legacy invitees that the old invite flow stored as member rows (`inactive` or `pending` rows whose person never set a password or accepted) are migrated into invitations, and the placeholder member row is then deleted. After migration, `inactive` means Removed only, and Removed members never take a seat.
- **Failed invitation email**: "Pending Send" is a delivery state of a Pending invitation, not a separate invitation status. The invitation takes a seat while it is Pending.

This Change Request exists because FR-009 v1.6 used "Invited" as a team member status (REQ-009-009, Key Entity 1) while also keeping a separate invitation record with status Pending (REQ-009-010, Key Entity 3). The two records described the same person, and the seat rule "accepted non-Owner team members" did not say which member statuses count.

## Baseline State

**Source version**: FR-009 v1.6. The rules appear in Business Workflows, Main Flow: Invite Team Member; Screens 1, 6, 10, 11 and 12; Business Rules, Rule 6; REQ-009-009 and REQ-009-010; Key Entities 1 and 3. FR-015 v1.22 Screen 2 Step 1 and Screen 3 Tab 1 Seat Limit and the seat-limit edge case carry the same seat rule.

- Main Flow step 10 created a "pending invitation record with status 'Invited'".
- Team member status included Invited (REQ-009-009, Key Entity 1, the Status fields of Screens 1, 6, 10, 11 and 12); Screen 11 Tab 5 Membership Status listed Active, Pending, Suspended, Removed.
- Seat usage counted "accepted non-Owner team members plus invitations still pending"; the Owner and expired invitations did not count.
- FR-009 did not say whether a Suspended provider organization could send invitations from the provider platform.

## Approved State

**Target version**: FR-009 v1.7, same headings, plus new Rule 9 (Invitation and Team Member Model) and Rule 10 (Suspended Provider Team Management); FR-015 v1.23.

- An invitation is the only record of an invited person until acceptance. Accepting the invitation creates the team member record with status Active and marks the invitation Accepted.
- Team member statuses are Active, Suspended, and Removed. They are stored as `active`, `suspended`, and `inactive`, where `inactive` means Removed. Screens that list pending invitations show them with the "Invited" badge and the Resend and Cancel actions.
- A Pending invitation whose email could not be delivered keeps status Pending with the delivery state "Pending Send", and it still takes a seat.
- Seat usage is as stated in the Decision Summary. FR-015 Seat Limit fields and the seat-limit edge case point to FR-009 Rule 6.
- While the provider organization is Suspended, the provider Team page is view-only: invite, resend, role change, suspend, and remove are unavailable, and the page shows "Your account is suspended. Team changes are unavailable. Please contact support." (Main Flow step 6, Screens 1 and 2, Rule 10, REQ-009-001). Admin invitations keep the existing REQ-009-024 block.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Invited person record (Main Flow steps 10 and 16; REQ-009-009, REQ-009-010; Key Entities 1 and 3) | Invitation record created with status "Invited"; team member status included Invited | Invitation only (Pending, Accepted, Expired, Cancelled) until acceptance; team member record created on acceptance | One record per invited person; no member exists before acceptance |
| Team member status (Screens 1, 6, 10, 11 and 12; Screen 11 Tab 5 Membership Status) | Active, Invited, Suspended; Tab 5 also listed Pending and Removed | Active, Suspended, Removed; "Invited" is the badge for a Pending invitation row | "Invited" and "Pending" describe an invitation, not a membership |
| Seat usage (FR-009 Rule 6, Screen 1 Team Size Meter, Screen 12 Seat Usage; FR-015 Seat Limit fields and edge case) | Accepted non-Owner team members plus pending invitations; Owner and expired invitations excluded | Non-Owner members with status Active or Suspended plus Pending invitations not past expires_at, each person once; Owner, Removed members, and Expired, Cancelled, or Accepted invitations excluded | States which statuses count; a Suspended member keeps the seat until removed |
| Suspended provider team management (Main Flow step 6, Screens 1 and 2, Rule 10, REQ-009-001) | Not stated for provider-side team actions | Team page is view-only while the provider organization is Suspended: no invite, resend, role change, suspend, or remove, with the suspended message shown | Consistent with the FR-032 Rule 6 suspended state and the admin block in REQ-009-024 |
| Stored member status values (schema §4 `provider_users.status`) | `inactive` described as a legacy invitee value | `active`, `suspended`, `inactive` (= Removed); legacy invitee rows migrated into invitations | Each stored value has one meaning; Removed members never take a seat |
| Failed invitation email (Alternative Flow B4, External Dependencies) | "Pending Send" read as an invitation status | "Pending Send" is a delivery state of a Pending invitation, which takes a seat | Keeps the four invitation statuses and prevents exceeding the seat limit through failed sends |
| Screen 1 quick stats | "Pending" | "Pending Invitations" (count of invitations with status Pending) | Consistent labelling |

## Scope and Impact

### In Scope

- The invited person and team member records and their statuses.
- The seat usage count in FR-009 and FR-015.
- Provider-side team management while the provider organization is Suspended.
- Stored team member status values and the migration of legacy invitee rows.
- The delivery state of an invitation whose email failed.

### Out of Scope

- Invitation expiry (7 days), resend, rate limit, and token rules, which are unchanged.
- The Seat Limit range, default, and "Request more seats" flow, which are unchanged.
- Owner records, which are created through FR-015 and do not use invitations.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr009-provider-team-roles/prd.md`: Main Flow: Invite Team Member; Screens 1, 2, 6, 7, 10, 11 and 12; Rules 6, 9 and 10; REQ-009-001, REQ-009-009, REQ-009-010; Key Entities 1 and 3.
- **Related FRs**:
  - FR-015 v1.23: Screen 2 Step 1 and Screen 3 Tab 1 Seat Limit; the seat-limit edge case. The 2026-10-27 [CR-FR015-20261027-01](../fr015-provider-management/change-request-2026-10-27-save-conflict-encryption-seat-usage.md) Approved State carries a 2026-10-28 clarification pointing here.
  - FR-032: Rule 6 defines the Suspended provider state and banner. Its view-only list does not name team management, so FR-009 Rule 10 states the Team page rule itself; FR-032 is not changed.
- **System documents**: `system-data-schema.md` v1.13.1 §4 `provider_users`: the status column lists `active`, `suspended`, and `inactive` (= Removed) and the business rules describe the legacy invitee migration; new §4A `provider_staff_invitations` defines the invitation table.

### Implementation Reconciliation

- **Existing implementation evidence**: The dev team reports that the legacy implementation creates an invited person as a team member with status `inactive` before activation, also reports a member status `pending`, and stores Removed members as `inactive`.
- **Required assessment**:
  - Migrate every legacy invitee row (an `inactive` or `pending` member row whose person never set a password or accepted) into a `provider_staff_invitations` row: status Pending if its invite or activation link has not expired, otherwise Expired. Then delete the placeholder member row. After migration, `inactive` means Removed only.
  - Compare the backend's actual invitation table with schema §4A and reconcile differences.
  - Create the team member record only on acceptance.
  - Seat usage query: non-Owner members in Active or Suspended plus Pending, unexpired invitations, deduplicated per person.
  - Block provider-side invite, resend, role change, suspend, and remove endpoints while the provider is Suspended.
  - Keep a failed-send invitation in status Pending with a delivery state, counted toward seat usage.
  - Tests for the four rules.
- **Compatibility / rollout risk**: Low. The current backend is a dev/test environment with no production data.
- **Data migration**: Required for legacy invitee rows, as described above. Removed members stored as `inactive` are kept.

## Acceptance and Validation

- Sending an invitation creates only an invitation with status Pending; the team list shows the row with the "Invited" badge; no team member record exists until acceptance.
- Accepting the invitation creates a team member with status Active and sets the invitation to Accepted; the person is still counted once.
- For a provider with the Owner, 3 Active members, 1 Suspended member, 1 Removed member, 2 Pending unexpired invitations, 1 Pending invitation past expiry, and 1 Cancelled invitation, seat usage is 6.
- Suspending a member does not change seat usage; removing that member lowers it by one.
- A provider user of a Suspended provider organization sees the Team page as view-only with the suspended message and cannot invite, resend, change a role, suspend, or remove a member; an admin cannot invite to a Suspended or Deactivated provider (REQ-009-024).
- After migration, no `provider_users` row with status `inactive` or `pending` belongs to a person who never accepted; each such person has an invitation that is Pending or Expired according to its original link expiry.
- An invitation whose email failed stays Pending with the "Pending Send" delivery state and counts toward seat usage.

## Approval and Traceability

- **Requested by**: Dev team, FR-015 backend confirmation questions.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-28.
- **Decision evidence**: Product Owner decisions of 2026-10-28 on the FR-015 backend confirmations; update log below.
- **PRD change log**: [FR-009 Appendix: Change Log](prd.md#appendix-change-log), v1.7 dated 2026-10-28; FR-015 v1.23 change log row.
- **Update log**: [FR015_BE_CONFIRMATIONS_RESOLUTION_2026-10-28.md](../../update-logs/2026-10-28/FR015_BE_CONFIRMATIONS_RESOLUTION_2026-10-28.md).
- **Supersedes**: None. Refines the seat usage rule of CR-FR015-20261027-01.
- **Superseded by**: None.
