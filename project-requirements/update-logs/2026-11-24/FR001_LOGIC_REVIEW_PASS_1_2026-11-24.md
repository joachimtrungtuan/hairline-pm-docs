# FR-001 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 1.8 to 1.9, with a graph change-set)
**Scope**: FR-001 Patient Authentication and Profile Management
**Source of findings**: `plans/reports/tester-261124-fr001-logic-p1.md` (18 findings; each ruled fix, narrowed fix or neighbour-only)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`

- **Deletion request**: open inquiries (Inquiry or Quoted) are cancelled when an admin approves the request, a refused request cancels nothing, and a patient with an inquiry at Accepted or later is blocked as FR-003 rules (REQ-001-090, REQ-001-091). The notice reads "Deletion requests are completed within 30 calendar days of submission" (REQ-001-094). Screen 16 gets a free-text reason, an extra-verification input and a read-only request status line; the Request button is hidden while a request is open (REQ-001-186).
- **Account status**: changes only through the FR-016 flows (suspension is FR-016 A6); FR-001 shows the status and no longer describes its own admin status edit. Deactivated stays as a reserved value that nothing sets or shows and is removed from the Screen 19 badge list (REQ-001-025, REQ-001-026, REQ-001-028, REQ-001-029, REQ-001-188).
- **Login outcomes**: one list on the login flow and Screen 9. Suspended is blocked with a contact-support message; an unverified email goes to the verification screen with a new code; Locked is blocked until the FR-026 lock period ends and then login works again; an open deletion request allows login (REQ-001-068, REQ-001-069).
- **Password reset outcomes**: Active gets a new session; Locked becomes Active and gets a new session; Suspended has the password updated, gets no session and stays Suspended with a neutral contact-support message (REQ-001-076, REQ-016-223).
- **Sessions**: a patient reset, an admin reset and a suspension each end every existing session, as Change Password does (REQ-001-182).
- **Wrong codes**: a wrong 6-digit code counts toward the failed-login limit (FR-026 setting, default 5); after the limit the code stops working and a new one is requested; no new setting (REQ-001-180).
- **Registration**: a duplicate email gets the neutral result and an email to the existing owner; an unverified account may register again and the old record is replaced; Screen 5 gets the Help entry (REQ-001-181, REQ-001-170).
- **Legal texts**: "Current version (FR-027)" replaces "latest published". One checkbox covers Terms and Privacy; both acceptances are recorded at account creation, not before (REQ-001-043, REQ-001-044, REQ-001-113, REQ-001-144).
- **Consent**: a first-sign-in consent gate after login for a patient without the general consent (REQ-001-187). Settings Main gets a Consent row and a Language row (REQ-001-185).
- **Notifications**: mandatory notices are those FR-020 defines (REQ-020-038), replacing the FR-001 list (REQ-001-105, REQ-001-106). The admin-edit notice lists the changed fields; there is no review screen (REQ-001-034, REQ-001-035).
- **Email change**: the 6-digit code goes to the new address, the old email stays the login email until the code is confirmed, and a notice goes to the old address; Screen 14 is added to the Screen 18 caller list (REQ-001-183, REQ-001-016, REQ-001-131). An admin email change saves the new address as unverified, notifies the old address, and the patient confirms a code at the next login (REQ-001-184).
- **Wording**: "soft-delete" for deletion requests is now "anonymised as FR-023 rules" (Scope and REQ-001-031). Edge Cases rule the duplicate email and the lock expiry; Dependencies add an FR-016 line.
- The Change Log row for version 1.9 is added; the PRD has no separate Last Updated line.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr001-logic-p1-fixes.yaml`

- New: rules REQ-001-180 to REQ-001-188; field ENT-patient.pending_email; flows FLW-001-login-outcomes and FLW-001-reset-by-status; steps STP-001-132 to STP-001-148 (login outcomes, reset by status, duplicate email, consent gate, email change, Screens 15a, 15c, 15d, 18, Logout and the admin email change notice).
- Rule statements and titles updated to mirror the PRD (22 rules), plus step titles, the STP-001-003 hand-off and the account status field description; one edge removed (STP-001-002 no longer applies REQ-001-044, because the acceptance is recorded at account creation).
- Cross-FR edges (edges only, no other FR's node is updated): STP-001-003 and STP-001-140 next to FR-027 steps; STP-001-140 applies REQ-027-062; REQ-001-044 applies to five ENT-legal-acceptance fields (FR-027); REQ-001-180 governed by SET-max-login-attempts (FR-026); REQ-001-186 applies to ENT-deletion-request.reason (FR-023); STP-001-136 and STP-001-137 apply REQ-016-223 (FR-016).
- Test-applied on a scratch copy of the graph: 371 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes for FR-016 (session ending on suspension and admin reset, the admin email edit rule), FR-020 and FR-030 (catalogue events for password changed, account locked, admin profile change and re-verification code), FR-035 (Settings owner label) and FR-023 (one sentence stating that login is allowed while a deletion request is open) are queued in the logic review ledger section for FR-001, not applied. The four events without a reader stay that way, because a reads edge runs only from a Stage to an Entity. Minor observations from the review are left as they are and listed under the ledger leftovers.
