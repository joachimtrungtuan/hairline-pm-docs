# Missing Mobile Flows Manual Testing Tracker Refresh

**Date**: 2026-03-30
**Type**: Documentation update
**Scope**: Created a new dated baseline copy of the missing mobile flows manual-testing tracker for a fresh regression / retest pass against the latest app version
**Source Report**: `local-docs/reports/2026-03-27/manual-testing-status-missing-mobile-flows-design-complement.md`
**Output**: `local-docs/reports/2026-03-30/manual-testing-status-missing-mobile-flows-design-complement.md`
**Platform**: Patient Mobile App

## Summary

Created a new `2026-03-30` report by copying the latest `2026-03-27` tracker so the next round of app testing can reuse the existing findings as a baseline. The new file is intended to be refilled during retesting: update rows only where the latest app version changes the result, and keep unchanged rows as-is.

## What Was Added

- New dated report folder: `local-docs/reports/2026-03-30/`
- New tracker file copied from the latest available manual-testing baseline
- Updated report metadata to reflect the new test round date
- Added a baseline note so future edits clearly reference the prior test round

## Notes

- No previous findings were reset or deleted in the copied report.
- No files outside `local-docs/` were modified.
- Minor follow-up update: refreshed `P01.1 Delete Account` for the new app version. The row is now approved because both authentication methods route correctly to the submission-confirmation screen; unreproduced error states were downgraded to an optional team reminder instead of a blocker.
- Minor follow-up update: refreshed `P01.2 Settings Screen` for the new app version. The external-browser behavior for `Privacy Policy` and `Terms & Conditions` is now treated as confirmed and approved, so the flow has been upgraded to approved status.
- Minor follow-up update: reset `P02.1 Compare Offers Side-by-Side` to `Pending` / `Pending` because the flow is still blocked by the same `ParseFailure` issue during quote creation in the latest app round.
- Minor follow-up update: added a short technical finding section documenting the transitional schema handling for `duration_of_concern` and `duration_of_concern_id`, and noting that the current payload mismatch is contributing to the `ParseFailure` blocking offer-related verification.
- Minor follow-up update: restructured the `duration_of_concern` supporting note into `Legacy Logic`, `Updated Logic`, and `Current Impact` so external readers can understand the schema-transition context more clearly without implementation-level detail.
- Minor follow-up update: added a focused API response excerpt under the `duration_of_concern` supporting finding so external readers can see the current payload mismatch directly.
- Minor follow-up update: refreshed `P03.1 Payment Methods Management` for the new app version. Add, edit, remove, set-default, and view-detail behaviors are now evidenced in the app; the remaining follow-up is that a saved method nickname does not currently replace the card brand label in the payment-method list.
- Minor follow-up update: refreshed `P05.2 Previous Treatments List` for the new app version. The flow is now approved because the app includes the list, the required four tabs, and sorting by provider, most recent, and status; the empty state remains only as a non-blocking reminder for a later pass.
- Minor follow-up update: upgraded `P03.1 Payment Methods Management` to approved status. The remaining nickname-display issue is now treated as a small non-blocking UI reminder because it does not materially affect the core payment-method workflow.
- Minor follow-up update: refreshed `P05.3 Submitted Reviews List` for the new app version. The flow is now approved because the app supports review listing, detail view, editing, takedown requests, and load-more behavior at the end of the list.
- Minor follow-up update: extended `P05.3 Submitted Reviews List` coverage to include the removed-review state, where a review is marked as removed while still remaining visible in the list.
- Minor follow-up update: refreshed `P06.1 Notification Listing & Bubble`. `Mark All as Read` is now confirmed in the app, but swipe-action behavior could not be verified in the current pass because the seeded notifications were no longer available, so the row was moved to `Needs Further Checking`.
- Minor follow-up update: moved `P08.1 Help & Support` to `Needs Further Checking` while keeping the same findings, so the row reflects that the flow still needs confirmation rather than a final rejection.
