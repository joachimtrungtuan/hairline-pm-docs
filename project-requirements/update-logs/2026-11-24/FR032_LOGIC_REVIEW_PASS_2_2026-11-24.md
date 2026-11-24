# FR-032 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 1.18 to 1.19, with a graph change-set)
**Scope**: FR-032 Provider Dashboard Settings
**Source of findings**: `plans/reports/tester-261124-fr032-logic-p2.md` (11 findings; each ruled fix, business default or settled by a closed FR)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md`

- **Help Centre video view**: the view is recorded after 30 seconds of play through the FR-033 view write, not when the player loads (REQ-032-099, REQ-033-097).
- **Support reply**: the provider "replies if needed"; there is no "mark as resolved" control for the provider.
- **Support and feedback form limits**: subject min 10 and max 200, feedback title min 10 and max 100, attachments up to 5 files of 10MB each in JPG, PNG, PDF, DOC and DOCX, as set by FR-034 (REQ-032-102, REQ-032-104).
- **Phone number**: required on Account Settings, can be replaced but not removed, unique per user within the provider, and a changed number is verified as in FR-009 (REQ-032-125, REQ-009-113).
- **Who edits what**: the table has a third column naming the FR-031 permission per row: Edit Profile (clinic profile, languages, awards, documents), Edit Notification Settings (notification preferences), View and Edit Billing Settings (billing), Owner only (account closure). REQ-032-141 and REQ-032-142 name them.
- **Reopen request outcome**: an admin who accepts reopens the case in FR-034 (status Open), which enables the reply box; an admin who answers but keeps the case Closed clears the "Request sent, awaiting admin" banner and the Request Reopen button returns (REQ-032-114, REQ-034-145).
- **Closure card**: while a request is pending the card shows "Closure requested on DD-MM-YYYY, awaiting admin review" with the button disabled; a second submission is refused with "A closure request is already pending." (REQ-032-071).
- **Account Name**: saving the clinic name sets the Owner's Account Name; a staff Account Name defaults to First Name + Last Name at account creation; the Owner handover rule resets the names (REQ-032-061, REQ-032-062, REQ-009-174).
- **Timezone at first login**: no prompt; the system silently sets the nearest listed whole-hour offset (UTC if the browser zone cannot be read), changeable at any time (REQ-032-064, REQ-032-145). The Screen 2 row keeps "Required: Yes" and says it is empty only before first login.
- **Audit**: phone number change (phone values masked) and timezone change are audit-logged (REQ-032-020).
- **Wording**: closure review is a target, "we aim to review within 5 business days" (REQ-032-073).
- Change log row 1.19 and Last Updated are set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr032-logic-p2-fixes.yaml`

- New steps STP-032-333 to STP-032-338: admin reopens the case, Owner Account Name set on clinic name save, closure refusal while pending, first-login timezone, audit after the phone save, audit after the timezone save. Each has done by, at, on and applies edges and is reachable by a next edge.
- Rule statements (and some titles) updated for 12 rules; the ENT-team-member timezone description and three step titles updated.
- Edges: the Help Centre view step now follows the "Watch the video tutorial" step (the "video opened" edge is removed); STP-032-332 next STP-032-268; REQ-032-141 applies to SCR-032-01 to SCR-032-05 and is applied on STP-032-138 (STP-032-139 is retired); FR-032 references REQ-009-113, REQ-009-174, REQ-034-036, REQ-034-037, REQ-034-130 and REQ-034-145.
- Cross-FR edges: only the six references above, from the FR-032 node. No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 106 change rows, no errors; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour changes for FR-031 (Manager gets Edit Profile, new permission Edit Notification Settings, billing permission naming) and FR-009 (account setup writes the default Account Name; the phone number field description) are queued in the logic review ledger section for FR-032 and are not part of this change. FR-015, FR-033 and FR-034 need no change. Minor observations are left as they are and listed under the ledger leftovers.
