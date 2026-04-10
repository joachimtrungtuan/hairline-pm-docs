# Update Log Archive Reorganization

**Date**: 2026-04-09
**Type**: Documentation archive maintenance
**Scope**: `local-docs/project-automation/logs/`, `local-docs/project-requirements/update-logs/README.md`

## Summary

Reorganized misplaced documentation reports from `local-docs/project-automation/logs/` into the canonical `local-docs/project-requirements/update-logs/` archive and aligned their filenames to the update-log naming convention.

## Changes Made

1. Created `local-docs/project-requirements/update-logs/2026-02-13/` as the missing date bucket for the February 13, 2026 reports.
2. Moved `IMPROVEMENTS-2026-02-13.md` to `PLANE_API_IMPROVEMENTS_2026-02-13.md`.
3. Moved `SECRETS-SCAN-REPORT.md` to `SECRETS_SCAN_REPORT_2026-02-13.md`.
4. Updated `local-docs/project-requirements/update-logs/README.md` so the moved files are indexed in both the dated listing and the quick-reference section.

## Notes

- The report contents were preserved; only their archive location and filenames were standardized.
- `local-docs/project-automation/logs/` no longer holds update-log reports after this reorganization.
- Adjusted the two February 13 filenames to match the shorter report-type-first naming style used elsewhere in `update-logs/`.
- Same-day minor follow-up: updated the 2026-04-09 mobile patient testing artifacts to copy the `TC-M-002 Settings` emulator results into the report/plan, mark the Settings steps as passing, and record that the current Terms & Conditions 404 target is accepted because no dedicated T&C page has been set up yet.
- Same-day second follow-up: restructured the 2026-04-09 mobile patient testing artifacts to behave as a true regression-round document set by explicitly labeling carried-over `2026-04-06` results as prefilled baseline context and reserving `Retested 2026-04-09` only for the Settings flow / `RC-02` legal-content recheck that was actually rerun.
- Same-day final reset: replaced the `2026-04-09` mobile testing report and plan with verbatim copies of the `2026-04-06` files, then blanked all non-pass result/status cells so only previously passed statuses remain prefilled for regression retest.
- Same-day regression update: marked `TC-M-002` Steps 5-6 as passing in the `2026-04-09` testing plan, updated the Settings summary in the `2026-04-09` testing report to reflect that both notification toggles now work with confirmed backend-side state changes, and changed `BUG-M-002` to `Fixed`.
- Same-day regression follow-up: marked `TC-M-002` Step 16 as passing in the `2026-04-09` testing plan after confirming that tapping `Help & Support` from Settings correctly routes to the Help & Support hub.
- Same-day My Reviews regression follow-up: marked the My Reviews sorting checks as passing in the `2026-04-09` testing plan after confirming that sorting is visible and works with 4 modes (`highest rating`, `lowest rating`, `newest`, `oldest`), updated the My Reviews summary in the `2026-04-09` testing report, and changed `BUG-M-006` to `Fixed`.
- Apr 10 notification follow-up: updated the `2026-04-09` mobile testing plan so the remaining data-driven notification steps are marked `Pending` based on confirmed backend/email dispatch with no mobile-app delivery, updated the related notification summaries/recheck notes in the `2026-04-09` testing report, and added `BUG-M-015` for the mobile-app notification delivery/rendering issue.
- Apr 10 payment-method follow-up: updated the `2026-04-09` payment-method notes in the testing plan/report so `BUG-M-009` explicitly records that the nickname is not being saved to the database, the payment-method list label never changes from the card brand, and the attached CleanShot screenshots should ignore the teal Android Studio overlay annotation.
- Apr 10 Help Center follow-up: updated the `2026-04-09` Help & Support notes in the testing plan/report to reflect that Help Center search and article `Helpful / Not Helpful` feedback are now working, reduced the Help & Support open-finding count accordingly, and changed `BUG-M-010` and `BUG-M-013` to `Fixed`.
- Apr 10 Contact Support follow-up: updated the `2026-04-09` Help & Support notes in the testing plan/report to reflect that `Contact Support` now routes correctly into the support-ticket flow via My Support Tickets / `Create New Ticket`, reduced the Help & Support open-finding count again, and changed `BUG-M-014` to `Fixed`.
- Apr 10 support-ticket creation follow-up: marked the `2026-04-09` Help & Support ticket-creation step as passing after confirming that creating a new support ticket works and the newly created ticket appears in the My Support Tickets list, and updated the related Help & Support summary notes in the report/plan.
- Apr 10 My Reviews follow-up: corrected the `2026-04-09` My Reviews notes so the edit-save long-loading defect remains open, but the per-aspect rating control issue is marked fixed; updated the My Reviews summary/open-finding count accordingly and changed `BUG-M-005` to `Fixed` while keeping `BUG-M-004` open.
- Apr 10 ticket-form follow-up: updated the `2026-04-09` Help & Support submission-flow test results to mark the Create New Ticket form fields, category picker, and priority options as passing based on the observed Create New Ticket screens, and updated the Help & Support summary notes in the report/plan to reflect that the submission form is compliant for the current documented flow.
- Apr 10 support-ticket persistence follow-up: corrected the `2026-04-09` Help & Support ticket-creation notes to reflect that new-ticket creation works only in-session, added `BUG-M-016` for the issue where newly created support tickets disappear from My Support Tickets after app restart, and updated the Help & Support summary/open-finding count accordingly.
- Apr 10 travel-itinerary follow-up: updated the `2026-04-09` Travel & Logistics notes to reflect the provided In Progress screenshots, marking itinerary access/layout coverage as evidenced with booking context, submitted outbound-flight details, pending `Return Flight` state plus `Submit Return Flight` CTA, and submitted hotel-information details; kept the separate return-flight submission form and itinerary-to-detail interaction as still unverified.
- Apr 10 ticket-validation follow-up: marked the `2026-04-09` Create New Ticket empty-submit validation step as passing after confirming inline/toast validation for missing required fields, and updated the Help & Support summary notes in the report/plan accordingly.
- Apr 10 findings-table cleanup: removed all rows marked `Fixed` from the `2026-04-09` testing report Findings Table, as requested, while leaving the active/open findings intact.
