# Missing Mobile Flows Manual Testing Tracker

**Date**: 2026-03-27
**Type**: Documentation update
**Scope**: Created a reusable manual-testing tracker for all flows defined in the Missing Mobile Flows design complement report
**Source Spec**: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
**Output**: `local-docs/reports/2026-03-27/manual-testing-status-missing-mobile-flows-design-complement.md`
**Platform**: Patient Mobile App

## Summary

Created a new report skeleton to support manual UI verification of the updated missing mobile flows. The new tracker consolidates all 15 flows into one table so testing can be recorded incrementally as raw observations are collected.

## What Was Added

- One row per flow from the source design complement report
- Separate status fields for execution progress and approval outcome
- Dedicated columns for:
  - already correct items
  - not correct items
  - items needing further checking
  - raw tester notes
- A column-fill guide so future updates stay consistent even when notes are provided in shorthand

## Notes

- This change created the skeleton only. No flow results were recorded yet.
- No files outside `local-docs/` were modified.
- Minor follow-up update: removed the `Flow` and `Related FRs` columns from the tracker table at user request.
- Minor follow-up update: removed the raw-notes column and renamed the outcome columns to `Confirmed Coverage`, `Findings / Gaps`, and `Follow-up Required` for a leaner external-facing presentation.
- Minor follow-up update: corrected the table structure to keep the `Flow` column and remove `Module` instead.
- Minor follow-up update: populated `P01.1 Delete Account` from manual testing, marking the flow as completed with follow-up required due to inconsistent post-verification navigation and unresolved clarity on some blocking/error-state coverage.
- Minor follow-up update: standardized the descriptive columns to bullet-style formatting for cleaner external presentation and easier future updates.
- Minor follow-up update: corrected `P01.1 Delete Account` after tester clarification that the three referenced blocking/error/rate-limit screens were design states not currently seen in the app UI, so they are now recorded as gaps or pending confirmation instead of confirmed coverage.
- Minor follow-up update: populated `P01.2 Settings Screen` with a confirmed finding that the notification settings screen includes both required switches (`email` and `push notifications`); the flow remains in progress pending broader verification.
- Minor follow-up update: aligned new manual-testing findings to the source-of-truth flow spec by updating `P01.2 Settings Screen`, `P01.3 Change Password`, and `P08.1 Help & Support`. Recorded that Privacy Policy / Terms currently open external links instead of the approved in-app legal viewers, the change-password flow and API appear integrated but still need state-by-state verification, and the current Help & Support screen does not match the documented hub flow.
- Minor follow-up update: shortened the `Follow-up Required` wording across populated rows for a leaner external-facing report and added the tester note that the `Forgot your password?` link in `P01.3` routes correctly to the existing password-recovery flow.
- Minor follow-up update: aligned the `P02.*` offer rows to the source-of-truth report. Recorded that `P02.1` does not match the approved compare-offers flow, `P02.2` is fully represented as documented, `P02.3` still needs expired-state verification in the current app, and `P02.4` has in-app legal content screens present within the offer flow.
- Minor follow-up update: normalized wording to treat the app itself as the verification target rather than referring separately to screenshots, and finalized `P01.3 Change Password` as approved with no remaining follow-up.
- Minor follow-up update: upgraded `P02.4 Legal/Policy Screens (Quote Context)` with confirmed coverage for titles, back navigation, read-only behavior, and version display; the only remaining follow-up is load-error handling verification.
- Minor follow-up update: finalized `P02.4 Legal/Policy Screens (Quote Context)` as approved and downgraded load-error handling to an optional reminder rather than a blocking follow-up item.
