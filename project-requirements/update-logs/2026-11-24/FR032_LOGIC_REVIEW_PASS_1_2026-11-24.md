# FR-032 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 1.17 to 1.18, with a graph change-set)
**Scope**: FR-032 Provider Dashboard Settings and Profile Management
**Source of findings**: `plans/reports/tester-261124-fr032-logic-p1.md` (19 findings; each ruled fix, neighbour-only or settled by the PRD)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md`

- **Who edits what**: one table under Screen 1 General Business Rules names the editors per area: clinic profile, languages, awards and documents by the Owner and a Manager; notification settings by the Owner and a Manager; the account closure request by the Owner only; personal account settings by every role for their own account; billing by the holder of the permission "View and Edit Billing Settings", held by FR-031 with the default Owner only (REQ-032-141, REQ-032-011, REQ-032-022, REQ-032-013).
- **Personal account settings per person**: phone number, timezone, password and account name belong to the signed-in person on the team member record; the browser timezone is offered at first login, otherwise UTC (REQ-032-005, REQ-032-006, REQ-032-007, REQ-032-015, REQ-032-064, REQ-032-145).
- **Account Email**: read-only for every role; the Owner's login email is changed by a Hairline admin through FR-015, a team member's by contacting support (REQ-032-063, REQ-032-144).
- **Notifications**: only the Owner and a Manager change the clinic's settings, other roles see them read-only, every change is audit-logged with the user; support case notices are always sent and ignore the Email and Push toggles (REQ-032-078 to REQ-032-082, REQ-032-142, REQ-032-143).
- **Billing**: the bank form is shown and required only for Manual bank transfer; Stripe Connect shows a status panel and a "Complete Stripe sign-up" link; Payout Readiness is display only and owned by FR-017; a Suspended Owner can still update the bank details; bank details stay with the clinic after an Owner role change (REQ-032-067, REQ-032-089, REQ-032-146).
- **Account closure**: the card and the request are for the Owner only; the account keeps its current status while the request is pending or rejected (REQ-032-013, REQ-032-067, REQ-032-074, REQ-032-076).
- **Language list**: offers Active and Preparation locales, shows every saved locale, and keeps a saved entry when its locale becomes Inactive (REQ-032-002, REQ-032-147).
- **Reviews tab**: filter, sort and paging run on the server over the whole list; the Edited marker and links to the FR-013 review screens are stated (REQ-032-148).
- **Help Centre**: the view of an FAQ, guide, resource and video and the helpful vote are recorded through the FR-033 view and vote writes; the resource category filter maps to the resource category field.
- **Support cases**: the reply box is enabled for Open, In Progress and Resolved cases and a reply to a Resolved case reopens it; a reopen request is a flagged message to FR-034, the case stays Closed until the admin decides, the admin is notified through the user-reply notice; the 24-hour response note says business days; the Quick Stats bar ignores the filters; a case opened from a notification link ignores the filters (REQ-032-103, REQ-032-105, REQ-032-109, REQ-032-110, REQ-032-112 to REQ-032-114, REQ-032-117).
- **Service Status**: a fourth display value, "Status not available"; subscription to status notifications is a future enhancement (REQ-032-115).
- **Removed**: the 4-hour note of the old Resolved banner (REQ-032-139).
- The change log row (version 1.18) and Last Updated are set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr032-logic-p1-fixes.yaml`

- New: rules REQ-032-141 to REQ-032-148; steps STP-032-326 to STP-032-332 (five Help Centre view and vote records, the Stripe Connect panel branch, the reply to a Resolved case); two fields on ENT-team-member owned by FR-032 (timezone, account_name).
- Retired: REQ-032-139 and seven fields on ENT-provider-account-settings (the personal settings moved to the team member record); the entity description now says clinic-level.
- Edges: Screen 2 shows and the rules for phone, timezone, password and account name now point at ENT-team-member fields; Account Email shows edge is read-only; the support notice steps and REQ-032-112 point at the case detail screen; 23 edges removed, with the Account Email edge and the two notice step edges re-added after their removal.
- Rule statements (and some titles) updated for 29 rules; step titles and screen descriptions updated to mirror the PRD.
- Cross-FR edges: FR-032 references REQ-013-032, REQ-015-114, REQ-017-064, REQ-021-119, REQ-026-121, REQ-031-005, REQ-033-096, REQ-033-097 and REQ-034-139; screens and steps point at FR-013, FR-033 and FR-034 fields and rules. No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 302 change rows, no errors; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour changes for FR-009 (team member email change action), FR-031 (permission row "View and Edit Billing Settings"), FR-033 (overall status value "Status not available", REQ-033-080), FR-017 (corrected bank details for a Deactivated clinic), FR-020, FR-015, FR-021, FR-026 and FR-034 are queued in the logic review ledger section for FR-032 and are not part of this change. Minor observations are left as they are and listed under the ledger leftovers.
