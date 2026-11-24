# FR-031 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 1.5, with a graph change-set)
**Scope**: FR-031 Admin Access Control and Permissions
**Source of findings**: `plans/reports/tester-261124-fr031-logic-p1.md` (30 findings; each ruled fix, settled by the PRD, or queued for a neighbour FR)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr031-admin-access-control/prd.md`

- **Super Admin protection**: no Super Admin account can be demoted, removed, suspended or deleted inside the product; the Admin Users tab shows no Change Role, Suspend or Delete on a Super Admin row, and the "only one Super Admin" banner is a warning only (REQ-031-009, REQ-031-054, REQ-031-085).
- **Invitation and account status**: the account is created when the invitation is recorded, with the status "Invited", and acceptance sets it Active. The two main flow steps are swapped (record, then email), and "Invited" is the one label for the pre-acceptance status everywhere (REQ-031-012, REQ-031-035, REQ-031-039, REQ-031-093).
- **Pending role**: a role change waits as a pending role with its Effective From; the current role applies until then and a second change replaces the pending one (new REQ-031-125; REQ-031-011, REQ-031-082).
- **Role acknowledgement**: the 24 hours start when the change takes effect; Super Admins see an "Overdue" flag; nothing is blocked (REQ-031-124).
- **Suspend, reactivate, delete**: new flow A8; a Super Admin may delete a suspended non-Super Admin account, which is anonymised under the existing rule (new REQ-031-126; REQ-031-053).
- **Invitations**: Pending Invitations sub-tab with Resend and Cancel (flow A9, new REQ-031-127); Request New Invitation notifies all Super Admins (flow A10, new REQ-031-128); the failure message and Screen 2 wording follow the configured expiry and a 2 to 50 character name (REQ-031-033, REQ-031-037, REQ-031-038, REQ-031-043).
- **Roles**: Edit Admin Role Permissions (flow A7, new REQ-031-131); Delete and Clone for custom roles with "Copy of" naming (flow A11, new REQ-031-129); no active or inactive role status (REQ-031-036, REQ-031-057).
- **Provider role sync failure**: "Sync failed", three automatic retries, an alert to Super Admins and a "not yet applied" indicator (A4 failure branch, new REQ-031-130; REQ-031-079).
- **Permission matrix**: sensitive list widened to financial writes, Manage Roles, Manage Users and Delete Patients, with the warning at Save and at role assignment (REQ-031-073); Select All and bulk actions skip Super Admin-only permissions and the View dependency covers every write permission that has a View (REQ-031-070, REQ-031-072, REQ-031-077); the default tables are full defaults (new REQ-031-134; REQ-031-076).
- **Permission rows**: Issue Refunds approval by another admin, never the requester (REQ-031-069); Document Treatment no longer ticked for Manager and team-row limits for Owner and Manager (REQ-031-068); new or reworded rows for patients, providers, reviews, messaging, localization, treatments, packages, retry charge, affiliates and the legal and help rows; Retry Charge, View Provider-Patient Messages, Flag Communications and emergency intervention get default holders.
- **Super Admin-only list**: now names the Manage Localization actions, the Affiliate Program Settings panel and commission ceiling override, Login as Provider, and the FR-034 Screen 7 settings and support audit export (REQ-031-067).
- **Audit trail**: Screen 5 shows access-control events only, 30 days by default with 100 rows at a time and "Load More", with the extended list of action types (new REQ-031-132; REQ-031-014, REQ-031-094).
- **Admin Terms of Service**: acceptance sits in the main flow at account set-up and belongs to this feature; the legal text stays with FR-027 (new REQ-031-133; REQ-031-046).
- **Wording and settings**: session limits and the throttle follow REQ-026-116 (REQ-031-099); the denial count and time window are each an admin setting (REQ-031-090).
- Dependencies now name FR-007 and FR-027; Status line, change log row (version 1.5) and Last Updated are set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr031-logic-p1-fixes.yaml`

- New: rules REQ-031-125 to -134; setting SET-admin-repeated-denial-window; fields ENT-admin-user-account.pending_role_id and pending_role_effective_from; flows FLW-031-a7 to a11 and 26 steps (STP-031-121 to -123, -131 to -133, -221 to -227, -321 to -324, -417 to -419, -421 to -426).
- Enum values: the account status "invited" added and "pending" retired; 11 audit action types added.
- Rule statements (43 rules, including the category rules) updated to mirror the PRD; step titles, setting, field and screen descriptions updated; the swapped invitation steps exchange their `applies` edges.
- Cross-FR edges: FR-031 references REQ-027-011, REQ-027-025, REQ-015-069, REQ-034-094 and REQ-026-116. No node owned by another FR is updated or retired.
- Test-applied on a scratch copy of the graph: 531 change rows, no errors; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour changes for FR-022 (role filter, "Billing Admin" wording, status values, permission categories, FR-022 edges to FR-031 nodes) and FR-016 (REQ-016-198 wording) are queued in the logic review ledger section for FR-031. FR-030 catalogue entries for the new notices and an FR-026 settings screen entry for the denial time window are listed as leftovers. Manage Treatments, Manage Packages, Manage Review Settings and Export Reviews have no default holder beyond Owner or Super Admin.
