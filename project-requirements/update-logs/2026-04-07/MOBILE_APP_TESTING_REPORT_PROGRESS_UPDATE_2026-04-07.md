# Mobile App Testing Report Progress Update

**Date**: 2026-04-07
**Type**: Testing report progress update
**Scope**: `local-docs/reports/2026-04-06/mobile-app-testing-report.md`, `local-docs/testing-plans/2026-04-06/manual/mobile-app-manual-testing-plan.md`

## Summary

Updated the April 6 patient mobile testing artifacts so the report and manual testing plan both reflect the currently observed notification, settings, reviews, payment-method, delete-account, help/support, and travel/logistics states, including dependency blocks and newly confirmed defects.

## Updated Documents

- `local-docs/reports/2026-04-06/mobile-app-testing-report.md`
- `local-docs/testing-plans/2026-04-06/manual/mobile-app-manual-testing-plan.md`

## Changes Made

### 0. Recorded initial Settings-screen confirmation

- Marked `TC-M-002 / Step 1` as passing because the Settings screen opens successfully
- Marked `TC-M-002 / Step 2` as passing because all 4 expected rows are present: `Notification Settings`, `Privacy & Security`, `Help & Support`, and `Terms & Conditions`
- Updated the report so `TC-M-002` is now tracked as partially verified instead of untouched pending

### 0a. Recorded Notification Settings toggle failure

- Marked `TC-M-002 / Step 3` and `Step 4` as passing because the Notification Settings screen and both toggles are present
- Marked `TC-M-002 / Step 5` and `Step 6` as failing because toggle changes do not persist despite a success toast
- Marked `TC-M-002 / Step 7` as passing because the informational notes are present
- Added `BUG-M-002` to the testing report with screenshot and recording evidence links for the non-persisting toggle behavior

### 0b. Recorded Settings back-navigation confirmation

- Marked the Settings sub-screen back-navigation checks as passing
- Recorded that all 4 Settings destinations can return to the main Settings screen using both the in-app back button and the Android hardware back button

### 0c. Recorded agreed external-browser behavior for legal content

- Marked the Privacy Policy and Terms & Conditions checks as passing
- Recorded that both pages open in the phone's external browser
- Closed `RC-02` as confirmed/accepted behavior rather than a defect because this delivery method is aligned between the client and the dev team

### 0d. Recorded Change Password regression result

- Marked `RC-03` as partially verified because the Change Password flow works and a different new password can be used for login
- Added `BUG-M-003` because the form incorrectly allows the new password to match the current password
- Marked the `Forgot your password?` regression sub-check as passing: OTP is sent by email, password reset succeeds, and the app auto-logs out afterward so the user can sign in again with the new password

### 0e. Recorded My Reviews functional coverage

- Updated `TC-M-003` to partially verified because the review list, average score, total review count, card metadata, and detail view are all loading correctly
- Recorded that the `No reviews yet` empty state is present when the account has no reviews
- Recorded that back navigation from My Reviews returns correctly to the Profile screen
- Recorded that Request Takedown can be submitted successfully from the review flow
- Recorded that review editing is reachable and additional images can be added, but edit/save is not reliable
- Added `BUG-M-006` because the My Reviews list is currently missing sorting controls/functionality
- Added `BUG-M-004` for the stuck `Saving` state and lost review edits after reopening the app
- Added `BUG-M-005` for the rating controls moving together instead of allowing independent scoring per criterion
- Added `BUG-M-007` because the completed-case submit-review screen has no image-upload control even though the edit-review screen supports photos
- Added `BUG-M-008` because the submit-review and edit-review screens are not aligned in structure and available controls
- Marked `RC-11` as only partially rechecked because list/detail/takedown are working, but review sorting is missing, edit has new bugs, and the submit-review screen still has coverage gaps
- Synced the testing-plan status rows so `My Reviews` sorting now shows as partial/missing and review-photo coverage now reflects that only edit-mode photo handling is exposed while initial submit-photo upload is still missing
- Completed the remaining `sorting` execution row in the testing plan by marking the sort-action step as `N/A` because there is no sorting control to interact with
### 1. Marked notification scope as blocked by external dependency

- Updated the report so `TC-M-001` is no longer treated as fully pending; the notification shell is partially verified while data-driven behavior remains blocked
- Recorded that notification scenarios are not fully testable yet because Firebase registration is still pending and the backend is not yet returning notification data
- Clarified that notification validation must be rerun on the patient app after Firebase registration is completed

### 2. Synced the manual testing plan to current observed UI

- Corrected the notification entry-point assumption from top-nav bell to bottom-nav icon
- Recorded the currently observed empty state: `No notifications yet`
- Captured that the notification screen already shows search, filter, `Clear Read`, and `Mark All as Read` controls
- Marked swipe/filter/bulk-action behavior as not yet verifiable without notification data
- Filled the remaining notification-plan rows with explicit `Pass`, `Fail`, or `N/A` outcomes so the section no longer has blank steps; card-dependent actions now clearly state they are blocked by the absence of notification items

### 3. Aligned the carried-over regression item

- Updated `RC-12` to show that swipe-action recheck is also blocked for the same Firebase dependency
- Added explicit retest guidance so the regression table does not look unresolved for product reasons alone

### 4. Added round-level execution note

- Inserted a report note and summary observation to distinguish external-environment blocking from application defects

### 5. Recorded the first concrete notification defect

- Logged that the Notification List currently lacks pull-down to refresh
- Marked `TC-M-001 / Step 9` as `Fail` in the manual testing plan
- Added `BUG-M-001` to the testing report as an open minor bug

### 6. Recorded initial Payment Methods coverage and persistent nickname bug

- Updated `TC-M-004` from untouched pending to partially verified because the Payment Methods screen now has observed coverage for both empty-state and populated-state scenarios
- Marked the empty-state checks as passing because the `No payment methods saved yet` screen and `Add Payment Method` CTA are present
- Recorded that the embedded add-card gateway form opens correctly and a test card can be added successfully, returning to the list with masked last 4 digits and a `Default` badge
- Marked the gateway-form field check as only partial because the observed embedded form shows card/expiry/CVC/billing inputs, Link checkout options, and the `Set as default` toggle, but cardholder name and nickname were still not confirmed from the captured add-card form in this round
- Marked the edit/details check as partial because the Payment Method Details screen opens with masked card data and metadata fields, but saving `Method Nickname` does not persist
- Added `BUG-M-009` to the testing report for the nickname-persistence failure: the app shows a success toast, but the list still shows the brand name and reopening details shows the nickname field blank again
- Updated regression row `RC-06` in both artifacts to show that the nickname-display bug is still reproducible rather than resolved
- Synced the Payment Methods completeness tracker so `List + empty state` and `Add card` are now marked complete, while `Edit card metadata`, `Remove card + modal`, `Set as default`, and `RC-06` explicitly show either partial coverage or the still-open nickname bug
- Updated the Payment Methods coverage again after confirmation that `Set as Default` is functioning correctly from both the three-dot context menu and the Edit Payment Method screen
- Marked the `Set as default` capability as complete in the testing plan, while leaving `Edit card metadata` only partial because the nickname-persistence bug still remains open
- Reclassified the expired-card validation check as pass because Stripe prevents expired cards from being added at the gateway layer, so the expected protection is still confirmed even though the app does not own that validation logic directly
- Reclassified the empty-form validation check as pass because the Stripe-managed payment form blocks empty submission and shows inline validation feedback on required fields
- Marked additional-card creation as pass after confirming that adding second and third saved cards works correctly
- Marked remove-card coverage as pass after confirming that deletion works for saved cards and that default-card removal correctly warns about default reassignment
- Recorded the accepted confirmation-modal behavior difference: non-default-card removal does not show last 4 digits, while default-card removal identifies the reassigned default card using last 4 digits
- Reclassified the saved-card rendering check as pass because brand icon, masked last 4 digits, and default state are confirmed on the list, expiry is confirmed in the detail view, and Stripe blocks expired-card insertion at the gateway layer
- Marked the remove-modal cancel path as pass after confirming that tapping `Cancel` closes the modal and aborts deletion without side effects

### 7. Recorded initial Delete Account flow coverage

- Updated `TC-M-005` from untouched pending to partially verified because the Delete Account flow is now covered through path access, reason confirmation, identity verification, and submitted-state confirmation
- Marked the top-level navigation into `Profile > Delete Account` as passing
- Marked the warning-screen content inventory and CTA presence checks as passing after confirming the warning icon, consequence text, retained-data explanation, processing timeline notice, `Request Deletion`, and `Go Back` controls are all present
- Recorded that the flow includes a separate reason-confirm step before `Verify Identity`
- Recorded that the deletion reason must currently be selected before proceeding to Verify Identity, and this behavior is accepted for the current build rather than tracked as a defect
- Recorded that Verify Identity supports both password and email OTP methods
- Marked the Verify Identity static-content check as passing after confirming the screen title, security icon, and instruction text are present
- Recorded that password validation works and that a `Forgot password` path is available directly from the password verification step
- Marked the successful password-verification action as passing
- Marked incorrect password / incorrect OTP handling as passing
- Recorded that switching to the OTP tab immediately sends an email OTP, `Resend code` is available, and OTP resend is rate-limited to 3 requests within 30 minutes
- Recorded that successful password verification and successful OTP verification both lead to the same submitted-state screen where the delete request is pending admin review
- Marked the submitted-state metadata check as passing after confirming pending-admin-review status, request reference ID, submitted timestamp, processing timeline, what-happens-next guidance, and email confirmation notice
- Recorded that the submitted-state screen does not expose a separate `Cancel` action; it provides `Back to Profile` instead, and this is accepted behavior for the current build
- Recorded that blocking-condition coverage for `active treatment / pending payment` is accepted as pass for this round under the same delete-flow restriction
- Updated `RC-01` to partially rechecked because blocking-condition coverage, wrong-password / wrong-OTP handling, and OTP resend limiting are now confirmed, while full lockout-threshold coverage still needs dedicated repro coverage

### 8. Recorded initial Help & Support coverage and article-feedback bug

- Updated `TC-M-006` from untouched pending to partially verified because the Help & Support hub, Help Center, FAQ flow, and Articles flow now have concrete screen coverage
- Marked the Help & Support hub screen as loading correctly with title `Help & Support`, navigation rows, `99+` support-ticket badge, and emergency phone/email section
- Marked the hub-layout check as passing because the hub title/rows/badge/emergency contacts are present, and lack of a separate search bar on the hub is accepted for the current build
- Marked Help Center as loading correctly with `FAQs`, `Articles`, `Resources`, and `Videos`
- Marked FAQ coverage as passing because topic tabs, accordion expansion/collapse, and rich-text answers are visible
- Marked Articles coverage as partial because the list/detail flows work and show filters, table of contents, related articles, and feedback controls, but article-level `Helpful / Not Helpful` feedback does not persist
- Recorded that the `Tutorial Guides` / `Troubleshooting` article tabs are currently UI-only and do not functionally filter content
- Recorded that the Help Center search bar is visible but cannot currently be typed into or used
- Marked Resources and Video Tutorials coverage as partial because their list/detail screens are reachable, but they currently appear to behave only as UI shells and no end-to-end functional actions were confirmed as truly working
- Added `BUG-M-010` to the testing report for the non-persisting `Helpful / Not Helpful` feedback state on article detail screens
- Added `BUG-M-012` to the testing report for non-functional `Tutorial Guides` / `Troubleshooting` tabs on the Articles screen
- Added `BUG-M-013` to the testing report for the unusable Help Center search bar
- Added `BUG-M-011` to the testing report for Resources / Video Tutorials currently behaving as UI-level shells rather than fully working content features
- Recorded that ticket submission is available under `My Support Tickets > Create New Ticket`, while the `Contact Support` entry point currently opens a `Support Team` screen with live-chat / email options instead
- Marked My Support Tickets coverage as working for list loading, status filtering, ticket detail, replies, reply attachments, and new-ticket creation
- Reframed `BUG-M-014` as a misplaced Contact Support entry point rather than a fully missing ticket-submission capability
- Recorded that the closed-ticket recovery-path expectation is accepted as-is for the current build/design, so the absence of a separate recovery / `Create New Ticket` path is not treated as a defect
- Updated `RC-13` to passing for the currently accepted hub structure: title/rows/badge/emergency contacts are present, and lack of a separate search bar on the hub is accepted for this build

### 9. Recorded initial Travel & Logistics field coverage

- Updated `TC-M-007` from untouched pending to partially verified because the current round now has concrete screen evidence for the Confirmed-view travel/logistics entry surface, Travel Requirement Check, Outbound Flight field inventory, and Hotel Information submitted/locked detail state
- Marked the Confirmed-view access step as passing because the current build shows booking summary, `View scheduled details`, hotel/flight/passport CTAs, offer CTA, and request-overview CTA from the travel/logistics surface
- Marked `Travel Requirement Check` as passing because the screen shows appointment summary plus both `Yes — I need to arrange travel` and `No — I am local / no travel needed`
- Marked `Outbound Flight` field coverage as passing because the visible form includes airline name, flight number, departure/arrival airports, departure/arrival date and time, ticket confirmation number, ticket class, baggage allowance, and special requests with no obvious field gaps in the observed captures
- Marked Hotel field coverage and hotel submission as passing because the current `Hotel Information` screenshots show a saved locked record with `Submitted` status, submitted timestamp/by-user metadata, and the expected hotel/logistics fields plus `Contact Support to Request a Correction`
- Marked Passport coverage only as partial because the current `Passport Details` screenshot confirms booking context, `Awaiting` status, upload area, and guidance text, but does not yet show the lower manual personal/passport fields or a submitted passport read-only record
- Upgraded the passport-photo upload interaction steps to pass after confirmation that passport photo upload is functioning correctly in the current build
- Upgraded the passport-form field-inventory check to pass after receiving the lower passport-form capture showing the visible manual field set: gender, location/country, place of birth, passport number, passport issue date, and passport expiry date
- Reframed the passport submit-related steps as UI-only pass-through coverage for this round, with explicit notes that deeper submit logic and submitted passport read-only behavior were not verified end-to-end on the temporary passport test form
- Reframed the outbound-flight submit-related steps in the same way: the current flight form is also being used as a UI-only test surface in this round, so deeper submit logic and submitted-flight locked-state behavior were intentionally not verified end-to-end
- Corrected the `BUG-M-005` step reference in the testing report from `TC-M-003 / Step 7` to `TC-M-003 / Step 9` so the findings table matches the actual My Reviews plan note where the linked-rating bug is recorded
- Marked `RC-07` and `RC-08` as partially rechecked rather than still untouched pending, since Passport and Flight/Hotel are no longer blocked by `ParseFailure` and now have concrete UI coverage in this round
- Synced the Travel rows in the manual-plan completeness tracker so the artifacts now explicitly distinguish what has been confirmed (`Travel Requirement Check`, outbound flight field inventory, hotel submitted detail) from what remains only partially evidenced (passport lower fields, return-flight coverage, separate itinerary view)

## Outcome

The April 6 testing report and manual testing plan now consistently capture the currently verified UI coverage for notifications, settings, reviews, payment methods, delete account, help/support, and travel/logistics, while also separating confirmed bugs from scenarios that remain blocked or not yet exercised in this round.
