# Missing Mobile Flows Manual Testing Tracker

**Report Date**: 2026-03-30
**Report Type**: Manual UI Testing Tracker
**Platform**: Patient Mobile App
**Source Flows**: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
**Status**: In Progress
**Baseline Source**: Copied from `local-docs/reports/2026-03-27/manual-testing-status-missing-mobile-flows-design-complement.md`

## Purpose

Use this table to track manual testing outcomes for the mobile UI updates covering the missing flows listed in the design complement report. Each row is one flow. This `2026-03-30` version starts as a carry-forward baseline from the `2026-03-27` report so new findings can be compared cleanly against the previous test round. If a flow has no change in the new app version, keep the existing entry unchanged.

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
| P01.1 Delete Account | Completed | Approved | - Core delete-account flow is implemented and generally works.<br>- The identity-verification step is present in the UI.<br>- Both authentication methods now route correctly to the `Deletion Request Submitted Confirmation` screen. | - The error-state screens have not yet been reproduced in the current pass. | - Optional reminder: confirm blocking / error / rate-limit state coverage with the team. |
| P01.2 Settings Screen | Completed | Approved | - Notification settings screen includes both required switches: email and push notifications.<br>- `Privacy Policy` opens successfully via external browser.<br>- `Terms & Conditions` opens successfully via external browser. | - External-browser behavior is confirmed for `Privacy Policy` and `Terms & Conditions`, rather than using the in-app legal viewer described in the earlier baseline. | - None. |
| P01.3 Change Password | Completed | Approved | - The in-session change-password flow is working in the app.<br>- The change-password API is integrated.<br>- The `Forgot your password?` link routes correctly to the existing password-recovery flow. | - No concrete mismatch was reported in the current pass. | - None. |
| P02.1 Compare Offers Side-by-Side | Pending | Pending | - Full flow verification is currently blocked in the app. | - The flow could not be reviewed because quote creation is still failing with `ParseFailure`. | - Recheck after the `ParseFailure` issue is fixed in the app. |
| P02.2 Cancel Inquiry | Completed | Approved | - Cancel Inquiry is represented fully in line with the documented flow and design. | - No concrete mismatch was reported in the current pass. | - No follow-up at this stage. |
| P02.3 Expired Offers/Quotes | Completed | Needs Further Checking | - No confirmed in-app coverage was recorded in the current pass. | - The app does not yet evidence the expired-quote states defined in `P02.3-S1` / `P02.3-S2`.<br>- The offer-area implementation does not yet show clear alignment with the approved expired-state patterns. | - Recheck expired-quote states in the app. |
| P02.4 Legal/Policy Screens (Quote Context) | Completed | Approved | - In-app screens for `Cancellation Policy`, `Privacy Commitment`, and `Terms of Service` are present within the offer flow.<br>- The screens use the correct titles.<br>- Back navigation returns to Quote Detail.<br>- The content is read-only.<br>- Version information is present. | - No concrete mismatch was reported in the current pass. | - Optional reminder: verify load-error handling in a later pass. |
| P03.1 Payment Methods Management | Completed | Approved | - The app can display the saved payment-method list.<br>- Add Payment Method is available.<br>- Edit and view-detail behavior for a payment method are available.<br>- A saved payment method can be removed.<br>- When the removed method is the default method, the app informs the user that the next card will be assigned as default.<br>- The default payment method can be changed. | - When a method nickname is set, the list still displays the card brand name (`Visa` / `Mastercard`) instead of surfacing the saved nickname. | - Optional reminder: confirm the intended display rule for method nickname on the payment-method list. |
| P04.1 Passport Submission (Path A) | Pending | Pending | - Full flow verification is currently blocked in the app. | - The flow could not be reviewed because the app is hitting `ParseFailure` on data from the created quote. | - Recheck after the `ParseFailure` issue is fixed in the app. |
| P04.2 Flight & Hotel Submission (Path B) | Pending | Pending | - Full flow verification is currently blocked in the app. | - The flow could not be reviewed because the app is hitting `ParseFailure` on data from the created quote. | - Recheck after the `ParseFailure` issue is fixed in the app. |
| P05.1 Day-to-Day Treatment Progress | Pending | Pending | - Full flow verification is currently blocked in the app. | - The flow could not be reviewed because the app is hitting `ParseFailure` on data from the created quote. | - Recheck after the `ParseFailure` issue is fixed in the app. |
| P05.2 Previous Treatments List | Completed | Approved | - The app includes a previous-treatments list.<br>- The list is split across the required four tabs: `All`, `In Progress`, `Completed`, and `Cancelled`.<br>- Sorting is available for `Provider`, `Most Recent`, and `Status`. | - The empty state defined in the design was not evidenced in the current pass. | - Optional reminder: verify the empty state in a later pass. |
| P05.3 Submitted Reviews List | Completed | Approved | - The app can display the list of submitted reviews.<br>- The app can open the detail view for each submitted review.<br>- The app supports editing a submitted review.<br>- The app supports requesting review takedown.<br>- The app supports loading more reviews when the user reaches the end of the list.<br>- The removed-review state is represented while the review still remains visible in the list. | - No concrete mismatch was reported in the current pass. | - None. |
| P06.1 Notification Listing & Bubble | Completed | Needs Further Checking | - The notification list screen exists in the app.<br>- Search is present and usable.<br>- Filter is present and usable, including reset filter behavior.<br>- `Mark All as Read` is present. | - Swipe action to reveal `Mark as Read` / `Archive` could not be verified in the current pass because the seeded notifications were no longer available. | - Recheck swipe-action behavior when seeded notifications are available again. |
| P08.1 Help & Support | Completed | Needs Further Checking | - A support entry screen exists in the current app.<br>- The current screen exposes direct support contact options, including `Contact Live Chat` and a support email address. | - The current screen does not match the `Help & Support Hub (P08.1-S1)` defined in the source-of-truth report.<br>- The delivered screen is titled `Support Team`, whereas the approved hub is titled `Help & Support`.<br>- The current screen does not evidence the required hub structure: search bar, `Help Center`, `Contact Support`, and `My Support Tickets` entry points.<br>- The current screen does not evidence the always-visible emergency contact section required by `P08.1-S1`.<br>- The current screen appears to route users into a simplified contact page rather than the documented hub + help-center + ticketing flow. | - Confirm whether this is a legacy shortcut or the intended replacement.<br>- Recheck `P08.1-S2` / `P08.1-S3` / `P08.1-S5` coverage. |

## Supporting Findings

### `duration_of_concern` Schema Compatibility

**Legacy Logic**

- `duration_of_concern` was handled as a string field.
- Existing flows and downstream consumers were built around the string-based representation.

**Updated Logic**

- The data model now also supports an enum-based representation so the field can scale more cleanly in the future.
- The updated structure uses `duration_of_concern_id` as the new integer enum reference while keeping the legacy string-based value for compatibility during the transition period.

**Current Impact**

- The current inquiry-detail payload is returning `duration_of_concern_id`, but the top-level `duration_of_concern` value is still `null`.
- Because the quote / offer flow is still depending on the older expectation at this integration point, quote creation is failing with `ParseFailure`.
- This issue is currently blocking offer-related verification that depends on successful quote creation.

**Current API Response Excerpt**

```json
{
  "status": "success",
  "data": {
    "id": "8f65ec79-9295-4a22-a197-23f72db35dd7",
    "status": "quoted",
    "problem": "hair",
    "duration_of_concern": null,
    "duration_of_concern_id": 3,
    "problem_detail": {
      "nature_of_concern": "thin 3103",
      "duration_of_concern": "1-2 years",
      "duration_of_concern_detail": {
        "id": 3,
        "value": "1-2-years",
        "label": "1-2 years"
      },
      "previous_treatments": "no",
      "symptom_severity": 7
    },
    "quotes": []
  }
}
```

- The key mismatch is that top-level `duration_of_concern` is `null`, while the structured value exists under `problem_detail`.
- This explains why downstream quote / offer logic can still fail if it is reading the legacy field at the old location.
