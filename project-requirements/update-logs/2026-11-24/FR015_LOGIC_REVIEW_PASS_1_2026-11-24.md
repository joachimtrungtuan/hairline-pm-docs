# FR-015 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 1.28 to 1.29, with a prepared graph change-set)
**Scope**: FR-015 Provider Management (Admin-Initiated)
**Source of findings**: `plans/reports/tester-261124-fr015-logic-p1.md` (10 findings; all accepted, each a fix or settled by a neighbour PRD)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr015-provider-management/prd.md`

- **Owner records at creation**: creating a provider also creates the Owner's team-member record (ownership flag set; the Owner does not count toward the Seat Limit, FR-009 Rule 6) and the Owner's org-role record in the same transaction (FR-009 REQ-009-196) (new REQ-015-136, Main Flow step 12).
- **Admin Owner handover**: a handover (FR-009 Rule 11, REQ-009-174) applies the Owner login email change steps to the new Owner's email: re-authentication, a reason, notices to the old and new address, the old Owner signed out. If the password is not set, the pending activation link is invalidated and a new activation email goes to the new Owner automatically (REQ-015-114).
- **Deactivation and invitations**: deactivation cancels every Pending team invitation (FR-009 REQ-009-194) in the same transaction as the status change, with an audit entry in Tab 8; a scheduled deactivation does this on the Effective Date. Stated in Alternative Flow A5, Screen 4 and General Module Rule 4 (new REQ-015-137).
- **Tab 1 for a Deactivated provider**: read-only, so no email edit and no activation email can happen there (REQ-015-032, Tab 1 rule and Rule 4).
- **Activation email and Resend**: Resend Activation Email shows for Active and Suspended providers whose password is not set, never for Deactivated ones; the self-service resend (Alternative Flow A1) matches; the activation email on an email change is sent only for Active or Suspended (REQ-015-058, REQ-015-056, REQ-015-114).
- **Tab 3 admin actions**: the FR-009 admin actions, now including Owner handover, remain available for Active and Suspended providers; for a Deactivated provider only "view audit log" remains and impersonation follows the Login as Provider rules (REQ-015-121). Handover is unavailable for Deactivated providers and needs the Edit Providers permission and admin re-authentication (REQ-015-116).
- **Starting Price**: shown in the package's own currency; conversion to the patient's currency happens only on patient-facing screens.
- **Suspension cascade (A5)**: unsent draft quotes are cancelled with the same status, silently to the patient (FR-004 REQ-004-073); when the cascade cancels the last live offer before acceptance, FR-015 hands the event to FR-003 (REQ-003-021) and FR-003 sends the patient message instead of the Contact Admin/Support-only notice.
- **Wording**: the default admin role is named Billing Admin (FR-031 naming), not Billing Staff; a rejected closure request leaves the provider with its current status instead of "stays Active" (REQ-015-087).
- Change log row, version and Last Updated set.

Two business questions took owner defaults (entries 242 and 243 in the Phase 10 defaults report): handover applies the login email steps and re-sends activation automatically; a Suspended clinic without a password can receive an activation email.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr015-logic-p1-fixes.yaml`

- New rules REQ-015-136 and REQ-015-137, with their stage, object and source edges.
- Updated statements: REQ-015-032, REQ-015-056, REQ-015-058, REQ-015-087, REQ-015-114, REQ-015-116; field description of `ENT-provider.starting_price`.
- Edges: steps STP-015-012, STP-015-153, STP-015-155 and STP-015-174 apply the new or neighbour rules; FR-015 references REQ-009-174 and REQ-009-194; the two A1 `next` edges into STP-015-107 are replaced by edges with a Suspended-aware label.
- Cross-FR edges all start at an FR-015 node and end at FR-009, FR-004 or FR-003 rules; no other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 40 change rows, no errors; the copy was deleted.

## Not changed here

FR-009 (a pointer that a handover applies the FR-015 login email steps) and FR-032 (confirm Rule 6 lets a Suspended clinic set its password from an activation link) are queued in the logic review ledger section for FR-015. FR-003, FR-004 and FR-031 need no change. Minor observations (stage wiring of five rules, scheduled-change edge cases, email-conflict wording, Key Entity citations, FR-010 and FR-014 dependency wording) are left as they are and listed under the ledger leftovers.
