# FR-001 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 1.9 to 2.0, with a graph change-set)
**Scope**: FR-001 Patient Authentication and Profile Management
**Source of findings**: `plans/reports/tester-261124-fr001-logic-p2.md` (11 findings, all accepted as fixes)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`

- **Register again with the same email**: only a registration that never had a verified email may be replaced, and only that unfinished record is discarded. Every other record, including an account whose email is unverified after an admin change, is an existing account and gets the neutral "check your email" result plus the owner notice (REQ-001-181; Screen 4, Edge Cases).
- **After a correct code**: a patient whose profile or discovery step is unfinished goes to Screen 6 (then Screen 8); a finished registration goes to the login success step. A patient who verified the email but never finished the profile is sent back to finish it at the next login, on any device, before entering the app (new rule REQ-001-189; Screen 5, Screen 9, B3). Owner default 270.
- **Email change code on Screen 14**: while a pending email exists the screen shows the pending address (read only), the 6-digit code input, Resend and Cancel change. The code lives 15 minutes, follows the same resend and wrong-code limits as the other codes, and on expiry the pending address stays until resend or cancel. The code sent at the next login after an admin email change uses Screen 5 with the same rules (REQ-001-183, REQ-001-184, REQ-001-180, REQ-001-098).
- **Email uniqueness**: the check also runs when a patient saves a pending email, when an admin saves an email, and at code confirmation. The patient sees the neutral message and the owner is emailed; the admin sees "address already in use"; a conflict at confirmation fails with the neutral message and clears the pending address (REQ-001-009). Owner default 271.
- **Locked account**: a wrong password on a Locked account shows the normal "Invalid email or password" message; the lockout message appears only with correct credentials. The failed-attempt count resets after a successful login and when the lock ends; attempts during the lock do not extend it; the account stores the count and the lock start. The IP-level block (FR-026, REQ-026-056) shows the same generic message. B1, B2, B3, Screen 9 and the sign-in user story now agree (REQ-001-007, REQ-001-065, REQ-001-066). Owner default 272.
- **Fulfilled deletion**: when FR-023 sets a request to Fulfilled, every session of the patient ends, the old credentials get the standard "Invalid email or password" result, and the email is free for a new account with no link to the old data (REQ-001-182). Owner default 273.
- **Delete Account path**: the 5-minute re-authentication check is stated only at the Request deletion button on Screen 16, no longer on the Screen 13 link (REQ-001-089, REQ-001-156).
- **Terms and Privacy version**: the acceptance record names the version displayed when the box was ticked; if a newer version is Current when the account is created, the checkbox is shown again with a link to the new text before Screen 4 completes (REQ-001-043, REQ-001-044). Owner default 274.
- **Status wording**: an admin changes account status only through the FR-016 flows; the system also locks after failed logins, unlocks when the lock ends, and returns a Locked account to Active after a password reset (REQ-001-188, REQ-001-026, REQ-001-028; scope, Screen 19, Business Rules, Dependencies).
- **Screen 19**: new Email Verified display with an "email change pending" mark (REQ-001-026, REQ-001-184).
- **Screen 14 Date of Birth**: maximum age 100, as on Screens 6 and 7 (REQ-001-052).
- The change log row for version 2.0 is added. The PRD has no Last Updated line, so only the change log carries the version.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr001-logic-p2-fixes.yaml`

- New: rule REQ-001-189; fields ENT-patient.failed_login_count and ENT-patient.locked_at; steps STP-001-149 (Screen 14 resend or cancel), STP-001-150 to STP-001-152 (Delete Account link, Screen 16 blocks, Request deletion), STP-001-153 (email verified, registration not finished).
- Edges: second next edge from STP-001-004 and from STP-001-132 (back) to the unfinished-registration route; Delete Account path STP-001-031 to STP-001-150 to STP-001-151 to STP-001-152, then to STP-001-146 and STP-023-001, with STP-001-146 back to STP-001-152; STP-001-071 to STP-001-081, STP-001-135 to STP-001-012, STP-001-137 to STP-001-013, STP-001-024 to STP-001-013; Screen 14 and Screen 19 shows edges; REQ-001-009, REQ-001-180 and others linked to Screen 14, the new fields and the pending email.
- Removed: REQ-001-090 applies at STG-patient-05-deleted. Three next edges are relabelled (remove then add): STP-001-003 to STP-001-138, STP-001-003 to STP-001-139, STP-001-004 to STP-001-005.
- Rule statements updated to mirror the PRD (14 rules, two titles); three step titles updated.
- Cross-FR edges (edges only): STP-001-152 next STP-023-001 (FR-023 step); FR-001 references REQ-026-056 (FR-026); REQ-001-182 applies to ENT-deletion-request (FR-023); REQ-001-183 and REQ-001-184 governed by SET-otp-max-resend-attempts (FR-026). No other FR's node is updated.
- Test-applied on a scratch copy of the graph: 153 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes are queued in the logic review ledger section for FR-001 pass 2 and are not part of this change: FR-023 (fulfilment step states sessions end, the login result and the free email), FR-016 (patient Overview shows email verified and email change pending; unlock may read the new lock fields), FR-026 (duplicate OTP setting stubs), FR-027 needs nothing (it already records the version with each acceptance). Minor observations are left as they are and listed under Leftovers in the same section: password reset marking a never-verified email as verified, admin email change as a session-ending event, hand-off STP-001-003 to STP-027-011, "15 minutes" fixed in REQ-001-098 and Screen 18 while Screen 5 says configurable, the SET-reverification-threshold description, order between Locked and unverified email in B3, steps pinned on an early stage, the Screen 5 Help entry after the wrong-code limit, and the four events with no reader.
