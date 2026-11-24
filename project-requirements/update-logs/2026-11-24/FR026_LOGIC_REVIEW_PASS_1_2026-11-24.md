# FR-026 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 1.18 to 1.19, with a graph change-set)
**Scope**: FR-026 App Settings and Security Policies
**Source of findings**: `plans/reports/tester-261124-fr026-logic-p1.md` (22 findings; each ruled fix, settled by another FR, or covered by an owner default)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr026-app-settings-security/prd.md`

- **Permissions**: the working role names (Settings Manager, Settings Viewer, Security Admin, "Settings Management") are replaced by the FR-031 permissions. View Settings views every screen; Edit Settings is Super Admin only; Manage Authentication Policies, Manage App Data and Manage Notification Templates edit the screens named in a new table under Security Controls. One gate replaces the two (REQ-026-001, REQ-026-054).
- **Treatment areas**: seeded with Hair, Beard and Both, as FR-003 expects (REQ-026-034). The problem-duration list keeps its five starting values in the seeding section, and a deactivated duration is no longer offered while stored answers stay readable (REQ-026-139).
- **Head scan Settings**: the maximum file size, maximum total size and required views rows are removed because FR-002 fixes them as product constants. Two admin-editable minimums remain, brightness and blur, each 0 to 100 with a starting value of 40; the head video limit is marked unused until head video ships (REQ-026-117).
- **Admin sign-in and sessions**: the shared Max Login Attempts lockout and the fixed FR-031 throttle of 5 attempts per 15 minutes both apply, whichever trips first (REQ-026-116). A Login as Provider session ends after its own fixed 30 minutes or when the admin's session ends, whichever comes first. Admin inactivity timeout is 5 to 240 minutes; re-verification threshold is 1 to 60 minutes (REQ-026-112).
- **Version history**: a new Change Type "System" for a Quote Configuration version created by an FR-029 Default Currency change, with a fixed reason text and Changed By set to the confirming admin; the change reason rule covers FR-026 screens (REQ-026-142, REQ-026-002).
- **Quote Configuration**: the quote extension rule names its two exceptions, the admin restore and the admin-authored replacement quote (REQ-026-027). A reminder whose time has passed after a lead time is raised is skipped, not sent late (REQ-026-031).
- **Screen 8**: a group "Limits owned by other features" lists the treatment and package creation limits and the admin invitation token expiry and repeated denial threshold (REQ-026-140). Emergency contact cells cite the current Settings, and at least one of phone and email must be set (REQ-026-143). Acceptance terms text blocks quote acceptance until set; landing images show nothing when none are set; timezones, notification types and head scan minimums have starting values.
- **OTP**: the expiry setting governs registration email verification and password reset; re-verification and email-change codes follow FR-001 (REQ-026-072).
- **Countries**: CSV columns defined with no flag column, imported countries saved Inactive until a flag is uploaded (REQ-026-128); the final active country cannot be deactivated (REQ-026-141); the deactivation warning lists FR-028 groupings and fallback price rows (REQ-026-129).
- **Other**: no FR-026 setting is sensitive at launch, so the masking and Show rules apply only to a setting later marked sensitive (REQ-026-014, REQ-026-016, REQ-026-052). Settings API outage at slot hold placement blocks the action (REQ-026-144). The password policy is defined by REQ-SYS-007 (FR-026 holds it only as the stored value). FR-021 added as consumer of the timezone options and UTC rule; Screen 2 says changes apply within 60 seconds.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr026-logic-p1-fixes.yaml`

- New: rules REQ-026-140 to REQ-026-144; Settings SET-head-scan-min-brightness-score and SET-head-scan-min-blur-score; enum value `system` on the version change type.
- Retired: REQ-026-107 and the Settings SET-head-scan-max-file-size, SET-head-scan-max-total-size, SET-head-scan-quality-thresholds and SET-head-scan-required-views.
- Updated: rule statements, Setting descriptions and four Screen descriptions to mirror the PRD.
- Cross-FR edges: FR-026 references eight rules owned by other FRs; the FR-002 rule REQ-002-034 is now governed by the two new Settings and no longer by the retired one. No node owned by another FR is updated or retired.
- Test-applied on a scratch copy of the graph: 136 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes for FR-001, FR-002, FR-004, FR-005, FR-006, FR-009, FR-015, FR-028, FR-029, FR-031 and FR-032 are queued in the logic review ledger section for FR-026 and are not part of this change. Minor observations other than the FR-021 consumer and 60-second wording are left as they are.
