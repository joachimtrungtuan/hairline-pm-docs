# FR-027 Logic Review Pass 2 (2026-11-24)

**Scope**: FR-027 Legal Content Management, PRD v1.6 to v1.7. Pass 2 (the last pass) of the logic review; 16 findings, 15 fixed in FR-027 and one (P2-14) queued to FR-022.
**Evidence**: reviewer report `plans/reports/tester-261124-fr027-logic-p2.md`; fixer report `plans/reports/docs-manager-261124-fr027-logic-p2-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr027-logic-p2-fixes.yaml` is prepared and NOT applied (the controller applies it). It follows the pass 1 change-set, which is already applied.
**Owner defaults**: entries 87 and 88 in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md` (adding a missing locale text to a Current version; fixed audience per document type).

## Changes to the PRD

- One acceptance base and Pending set, stated at the Screen 4 fields: the Active patient accounts and the team members of Active providers, in the document type's audience, that existed when the version became Current; accepted means a ledger row for the version or, for a restored version, for the version it was restored from; an account that leaves Active leaves the base. Prompts, reminders, the Screen 3 re-accept count and the rate all use it (REQ-027-053, REQ-027-032, REQ-027-052, REQ-027-063).
- A user must accept the Current text of a type while the latest Material Change = Yes version up to and including it is not accepted by them; first run asks for the Current text whatever its flag (REQ-027-035).
- Fixed audience per document type (Terms & Conditions and Privacy Policy: patients and provider team members; general Consent: patients only; Cancellation Policy: nobody); the acceptance rules can only switch the requirement of a type off for an audience (REQ-027-021, REQ-027-059). Providers are not asked for the general consent (REQ-027-062).
- The Screen 1 banner starts 14 days after the version became Current, as the alert does; the PRD now carries the 14 days and the once-per-version alert (REQ-027-024, REQ-027-063).
- Screen 5 gets Continue with limited access, sign-out and the FR-001 account-deletion link; the blocked state applies only at the gated actions, where the screen is shown again (REQ-027-058, REQ-027-033).
- Admin may add a missing locale text to a Current version, audited as `edit`, with no new version and no re-acceptance; this clears the Locale gap badge (REQ-027-037, REQ-027-049).
- Audit trail list also opens unfiltered from the Legal settings panel; the object reference is empty for `settings_change`. Audit actions per event are stated (create, edit, publish and activate and archive, publish and schedule, withdraw); the restore no longer says "one" entry (REQ-027-013, REQ-027-031).
- Recipients: the publication notice goes to the publishing Admin, the coverage alert to Admins holding A-09 Edit Settings (REQ-027-022, REQ-027-023).
- Settings → Consent added to the patient entry points (REQ-027-016, REQ-027-017). Screen 2 Material Change fixed to Yes on a draft created from an earlier version (REQ-027-031).
- A second Publish for a type with a Scheduled version is rejected on the Publish step, and Screen 3 keeps the Admin on the screen (REQ-027-060).
- Provider first-run and sign-in prompts have their own steps and stages; a new member of an Active clinic is covered (REQ-027-062).

## Graph change-set (prepared, not applied)

- 4 new steps (STP-027-035 settings, 036 withdraw, 037 provider first-run at STG-provider-01-invited, 038 provider sign-in prompt at STG-provider-03-active); 42 edges added, 3 removed, 35 node updates (17 rules, 1 setting, 9 entity and field descriptions, 2 events, 6 steps); no new fields or enum values.
- Back edges STP-027-002 and 003 to 001 and STP-027-004 to 003 (rejected second Publish); the REQ-027-060 applies edge moved from STP-027-005 to STP-027-004; STP-027-010 and 011 are patient-only.
- Applied to a scratch copy: whole-graph lint stays at 29 findings (L03 1, L09 1, L12 6, L17 12, L18 9); no FR-027 finding was added.

## Cross-FR rows queued

FR-022 (filter statuses, types and defaults), FR-009 (invitation hand-off to STP-027-037), FR-001 (patient Settings entry for the Consent); see the pass 2 section of `plans/reports/logic-review-ledger.md`.
