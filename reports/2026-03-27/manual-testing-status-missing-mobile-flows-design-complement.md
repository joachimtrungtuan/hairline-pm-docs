# Missing Mobile Flows Manual Testing Tracker

**Report Date**: 2026-03-27
**Report Type**: Manual UI Testing Tracker
**Platform**: Patient Mobile App
**Source Flows**: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
**Status**: In Progress

## Purpose

Use this table to track manual testing outcomes for the mobile UI updates covering the missing flows listed in the design complement report. Each row is one flow. As manual testing results come in, update the row instead of creating separate ad hoc notes.

## Column Fill Guide

| Column | What to put here |
| --- | --- |
| Test Progress | Current execution state only: `Pending`, `In Progress`, or `Completed`. |
| Approval Status | Final outcome after review: `Pending`, `Approved`, `Not Approved`, or `Needs Further Checking`. |
| Confirmed Coverage | Use short bullet points describing confirmed UI behavior that matches expectation, including screens, states, copy, layout, interaction, or data display. |
| Findings / Gaps | Use short bullet points for concrete gaps, mismatches, bugs, missing states, wrong copy, wrong behavior, or off-spec UI details. |
| Follow-up Required | Use short bullet points only. Keep them concise and action-oriented. |

## Flow Tracking Table

| Flow | Test Progress | Approval Status | Confirmed Coverage | Findings / Gaps | Follow-up Required |
| --- | --- | --- | --- | --- | --- |
| P01.1 Delete Account | Completed | Needs Further Checking | - Core delete-account flow is implemented and generally works.<br>- The identity-verification step is present in the UI.<br>- The OTP verification path leads to the `Deletion Request Submitted Confirmation` state. | - After successful email + password verification, the UI returns to the previous screen instead of proceeding to `Deletion Request Submitted Confirmation`.<br>- This is inconsistent with the OTP verification path, which navigates correctly.<br>- The `Cannot delete account` blocking state shown in design has not been seen in the current app UI.<br>- The `Something went wrong` error state shown in design has not been seen in the current app UI.<br>- The `Too many attempts` / rate-limit state shown in design has not been seen in the current app UI. | - Recheck email + password success navigation.<br>- Confirm whether blocking/error/rate-limit states exist in the delivered UI. |
| P01.2 Settings Screen | In Progress | Needs Further Checking | - Notification settings screen includes both required switches: email and push notifications. | - `Privacy Policy` does not open the in-app read-only viewer defined in `P01.2-S4`; it opens an external link instead.<br>- `Terms & Conditions` does not open the in-app read-only viewer defined in `P01.2-S5`; it opens an external link instead. | - Confirm whether external-link behavior is intentional.<br>- Recheck in-app legal-viewer coverage for `P01.2-S4` / `P01.2-S5`. |
| P01.3 Change Password | Completed | Approved | - The in-session change-password flow is working in the app.<br>- The change-password API is integrated.<br>- The `Forgot your password?` link routes correctly to the existing password-recovery flow. | - No concrete mismatch was reported in the current pass. | - None. |
| P02.1 Compare Offers Side-by-Side | Completed | Not Approved | - The app shows an offers list and an offer detail screen.<br>- Filter and sort controls are present on the offers list. | - The app does not match the source-of-truth `P02.1-S1` inquiry dashboard with embedded comparison flow.<br>- Compare selection checkboxes and the in-screen comparison panel are not evidenced in the app.<br>- The app uses a simpler offers list/detail pattern instead of the approved side-by-side comparison experience.<br>- The app does not evidence the documented inquiry-level context required by `P02.1-S1`, such as stage, timeline, inquiry summary, medical alerts, deadlines, and next actions. | - Recheck whether compare-offers capability exists elsewhere in the app.<br>- Confirm whether the current offers UI is an interim version or a spec mismatch. |
| P02.2 Cancel Inquiry | Completed | Approved | - Cancel Inquiry is represented fully in line with the documented flow and design. | - No concrete mismatch was reported in the current pass. | - No follow-up at this stage. |
| P02.3 Expired Offers/Quotes | Completed | Needs Further Checking | - The source-of-truth design includes dedicated expired-quote states for mixed and all-expired scenarios. | - The app does not yet evidence the expired-quote states defined in `P02.3-S1` / `P02.3-S2`.<br>- The offer-area implementation does not yet show clear alignment with the approved expired-state patterns from the design set. | - Recheck expired-quote states in the app. |
| P02.4 Legal/Policy Screens (Quote Context) | Completed | Approved | - In-app screens for `Cancellation Policy`, `Privacy Commitment`, and `Terms of Service` are present within the offer flow.<br>- The screens use the correct titles.<br>- Back navigation returns to Quote Detail.<br>- The content is read-only.<br>- Version information is present. | - No concrete mismatch was reported in the current pass. | - Optional reminder: verify load-error handling in a later pass. |
| P03.1 Payment Methods Management | Pending | Pending | - [List confirmed matching screens, states, copy, and interactions.] | - [List missing, wrong, or off-spec UI details.] | - [List unclear items or cases that need another pass.] |
| P04.1 Passport Submission (Path A) | Pending | Pending | - [List confirmed matching screens, states, copy, and interactions.] | - [List missing, wrong, or off-spec UI details.] | - [List unclear items or cases that need another pass.] |
| P04.2 Flight & Hotel Submission (Path B) | Pending | Pending | - [List confirmed matching screens, states, copy, and interactions.] | - [List missing, wrong, or off-spec UI details.] | - [List unclear items or cases that need another pass.] |
| P05.1 Day-to-Day Treatment Progress | Pending | Pending | - [List confirmed matching screens, states, copy, and interactions.] | - [List missing, wrong, or off-spec UI details.] | - [List unclear items or cases that need another pass.] |
| P05.2 Previous Treatments List | Pending | Pending | - [List confirmed matching screens, states, copy, and interactions.] | - [List missing, wrong, or off-spec UI details.] | - [List unclear items or cases that need another pass.] |
| P05.3 Submitted Reviews List | Pending | Pending | - [List confirmed matching screens, states, copy, and interactions.] | - [List missing, wrong, or off-spec UI details.] | - [List unclear items or cases that need another pass.] |
| P06.1 Notification Listing & Bubble | Pending | Pending | - [List confirmed matching screens, states, copy, and interactions.] | - [List missing, wrong, or off-spec UI details.] | - [List unclear items or cases that need another pass.] |
| P08.1 Help & Support | Completed | Not Approved | - A support entry screen exists in the current app.<br>- The current screen exposes direct support contact options, including `Contact Live Chat` and a support email address. | - The current screen does not match the `Help & Support Hub (P08.1-S1)` defined in the source-of-truth report.<br>- The delivered screen is titled `Support Team`, whereas the approved hub is titled `Help & Support`.<br>- The current screen does not evidence the required hub structure: search bar, `Help Center`, `Contact Support`, and `My Support Tickets` entry points.<br>- The current screen does not evidence the always-visible emergency contact section required by `P08.1-S1`.<br>- The current screen appears to route users into a simplified contact page rather than the documented hub + help-center + ticketing flow. | - Confirm whether this is a legacy shortcut or the intended replacement.<br>- Recheck `P08.1-S2` / `P08.1-S3` / `P08.1-S5` coverage. |
