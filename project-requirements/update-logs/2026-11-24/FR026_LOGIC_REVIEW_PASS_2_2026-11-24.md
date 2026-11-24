# FR-026 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 1.19 to 1.20, with a graph change-set)
**Scope**: FR-026 App Settings and Security Policies
**Source of findings**: `plans/reports/tester-261124-fr026-logic-p2.md` (10 findings, all accepted; none was a false positive)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr026-app-settings-security/prd.md`

- **Failed-attempt counter**: one counter per account, shared by sign-in and verification-code entry; it returns to zero after a successful sign-in or code entry and when a lockout ends; a lowered Max Login Attempts applies from the next failed attempt and saving it locks nobody (new REQ-026-145; Screen 2; REQ-026-071 context).
- **Admin sessions**: at the concurrent-session limit the oldest session is ended and the new one opens; a changed limit or inactivity timeout applies from each open session's next request, oldest first above a lowered limit (REQ-026-116; Screen 8).
- **Add Country scenario**: step 4 uploads the flag and the system checks type and size, so the scenario reaches its outcome (REQ-026-122).
- **OTP email**: `{expiry_minutes}` is the lifetime of the code being sent (the OTP Expiry Time, or 15 minutes for re-verification and email-change codes); a resend is a new code under the template version and expiry in force at the moment of the resend, and codes already sent keep theirs (REQ-026-072, REQ-026-073, REQ-026-106; Screens 3 and 6; Alternative Flow A2 step 12).
- **Admin timezone**: admin screens show times in the admin's browser timezone with the zone named; the Timezone Options list is for patients and providers only; REQ-026-050 no longer cites FR-021 (Rule 5; Screen 7).
- **Emergency contact**: the at-least-one check runs only on a save that changes the phone or the email; other Screen 8 rows can be saved while both are blank; the patient help screen hides the section while both are blank (REQ-026-143, REQ-026-115; Screen 8).
- **Country flag**: required when an admin adds a country; a seeded country may have none and an imported one has none until uploaded; "flag missing" means an empty flag and blocks activation (REQ-026-011, REQ-026-128; Screen 4).
- Stale "head scan intake limits" wording replaced; change log row 1.20 added.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr026-logic-p2-fixes.yaml`

- New: rule REQ-026-145; step STP-026-105 (flag type and size check, between STP-026-020 and STP-026-021); fields ENT-settings-audit-entry.admin_user_agent and ENT-settings-audit-entry.version_id.
- Updated: eight rule statements (REQ-026-011, 050, 072, 073, 106, 116, 128, 143), field flag_url (now optional) and version_number (now text), steps STP-026-020 and STP-026-036, settings SET-max-login-attempts and SET-timezone-options descriptions.
- Edges: eight `next` edges from active steps to retired validation steps removed (STP-026-007, 022, 068, 075, 080, 088, 093, 096); the A1 chain now runs 020, 105, 021.
- Cross-FR edges: none; no node of another FR is updated.
- Test-applied on a scratch copy of the graph: 73 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour wording queued in the logic review ledger: FR-001 (counter reset at REQ-001-180; REQ-001-125 timezone wording and its edge), FR-021 (REQ-021-126 back-reference), FR-031 (REQ-031-099 session rule), FR-035 (REQ-035-040 empty emergency contact section). Minor observations and the unstated blur and brightness direction stay as leftovers.

## Owner defaults recorded

Entries 266 to 269 (attempt counter reset, oldest session ended, admin browser timezone, emergency contact check scope) are written for the defaults file; each lists the other option.
