# Design Layout Verification Report — Missing Mobile Flows Design Complement

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-001, FR-023, FR-026
**Flow Scope**: P01.1 Delete Account
**Layout Source**: `layout-temp/`
**Platform**: Patient Mobile App
**Status**: 🟡 PARTIAL
**Approval Status**: 🟢 Approved with minor issues

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P01.1 | Delete Account | P-01: Auth & Profile Management | 3 | 3 | 🟡 PARTIAL | 31/34 (~91%) |

**Overall**: 1 of 1 flows verified. P01.1 is no longer blocked because all three screens now have layouts, and it is approved despite minor remaining mismatches in S1, S2, and S3.
**Screens**: 3 of 3 specified screens have layouts (100% screen coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/Delete your account.jpg` | P01.1 | P01.1-S1 | Primary warning screen candidate |
| `layout-temp/Deletion Reason.jpg` | P01.1 | P01.1-S1 | Deletion-reason selector state candidate |
| `layout-temp/Cannot delete account.jpg` | P01.1 | P01.1-S1 | Blocking-state candidate |
| `layout-temp/Final Confirmation.jpg` | P01.1 | P01.1-S1 | Final-confirmation modal candidate |
| `layout-temp/Verify Your Identity/Password.jpg` | P01.1 | P01.1-S2 | Verification screen candidate |
| `layout-temp/Verify Your Identity/Password-1.jpg` | P01.1 | P01.1-S2 | Verification screen variant candidate |
| `layout-temp/Verify Your Identity/Password/Error.jpg` | P01.1 | P01.1-S2 | Verification error-state candidate |
| `layout-temp/Verify Your Identity/Password/Error-1.jpg` | P01.1 | P01.1-S2 | Verification error-state variant candidate |
| `layout-temp/Show error message and allow retry.jpg` | P01.1 | P01.1-S2 | Retry/error-state candidate from flow diagram wording |
| `layout-temp/Show rate-limit/lockout message and prevent retry.jpg` | P01.1 | P01.1-S2 | Rate-limit/lockout-state candidate from flow diagram wording |
| `layout-temp/Deletion Request Submitted Confirmation.jpg` | P01.1 | P01.1-S3 | Submission confirmation screen candidate |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Profile.jpg` | Profile entry screen | Outside direct P01.1 screen-spec scope; may provide entry context only |

---

## Detailed Verification by Flow

---

### Flow P01.1: Delete Account

**Status**: 🟡 PARTIAL — all required screens now exist, but S1 and S2 still contain behavior/copy mismatches
**Approval**: 🟢 Approved with minor issues — user approved the flow despite the remaining discrepancies documented below
**Screens required**: 3
**Layout files**: `Delete your account.jpg`, `Deletion Reason.jpg`, `Cannot delete account.jpg`, `Final Confirmation.jpg`, `Verify Your Identity/Password.jpg`, `Verify Your Identity/Password-1.jpg`, `Verify Your Identity/Password/Error.jpg`, `Verify Your Identity/Password/Error-1.jpg`, `Show error message and allow retry.jpg`, `Show rate-limit/lockout message and prevent retry.jpg`, `Deletion Request Submitted Confirmation.jpg`

#### Screen P01.1-S1: Delete Account Warning

**Layout**: `layout-temp/Delete your account.jpg`, `layout-temp/Deletion Reason.jpg`, `layout-temp/Cannot delete account.jpg`, `layout-temp/Final Confirmation.jpg`

##### Flow Context

- **User arrives from**: Profile -> Delete Account entry point, per the source flow diagram at `missing-mobile-flows-design-complement.md:67`
- **Screen purpose**: Explain the consequences of account deletion, optionally collect a reason, and gate the user into re-auth or final submission
- **Entry point**: Present. `Delete your account.jpg` shows the warning screen with a back arrow to return to Profile
- **Exit path**: Present. `Delete your account.jpg` shows `Request Deletion` and `Go Back`; `Cannot delete account.jpg` adds `Contact support` and `Cancel`; `Final Confirmation.jpg` adds `Cancel` and `Request Deletion`
- **Data continuity**: Correct. This screen does not require carried-over form data; it introduces the delete-account request and its consequences
- **Flow context issues**: None

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Warning Icon | Yes | ✅ | `Delete your account.jpg`, `Deletion Reason.jpg`, `Cannot delete account.jpg`, and `Final Confirmation.jpg` all show a red warning icon consistent with the spec |
| Screen Title | Yes | ❌⚠️ | `Delete Your Account` is visible in all four S1 states, but it is rendered in a neutral dark color instead of the required red/destructive styling |
| Back Navigation | Yes | ✅ | A back arrow is visible at top-left in `Delete your account.jpg`, `Deletion Reason.jpg`, and `Final Confirmation.jpg` |
| Blocking Message (Conditional) | Conditional | ✅ | `Cannot delete account.jpg` shows the blocked state with the required message that deletion is unavailable during active care or payment processing |
| Contact Support Link (Conditional) | Conditional | ❌⚠️ | The support path exists in `Cannot delete account.jpg`, but it is implemented as a large green primary button labeled `Contact support` rather than a link-style action |
| Consequences Header | Yes | ✅ | `Delete your account.jpg` shows `What may be deleted or anonymized` as the section header |
| Consequences List | Yes | ✅ | `Delete your account.jpg` lists all four required categories: profile/preferences, messages/communications, reviews content, and uploaded media |
| Retained Data Header | Yes | ✅ | `Delete your account.jpg` shows `What will be retained (legal requirement)` as a clear section header |
| Retained Data Explanation | Yes | ✅ | `Delete your account.jpg` states that medical and financial transaction records are retained for at least 7 years and access is restricted |
| Processing Timeline Notice | Yes | ✅ | `Delete your account.jpg` includes an info box stating verified deletion requests are completed within 30 calendar days |
| Deletion Reason Selector (Optional) | No | ✅ | `Delete your account.jpg` shows the selector, and `Deletion Reason.jpg` shows the expanded option sheet with centrally managed choices |
| Final Confirmation Modal (Conditional) | Conditional | ✅ | `Final Confirmation.jpg` shows the confirmation modal with `Cancel` and `Request Deletion`, matching the required safeguard |
| Request Deletion Button | Yes | ✅ | `Delete your account.jpg` shows a red destructive CTA labeled `Request Deletion`; the same action remains visible behind the modal in `Final Confirmation.jpg` |
| Go Back Button | Yes | ✅ | `Delete your account.jpg` shows a secondary `Go Back` button beneath the destructive CTA |

**Extra Elements**:

- None

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 11/13 (85%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-23 Terminology consistency`: the screen title says `Delete Your Account`, while the CTA and modal use `Request Deletion`, which creates a mismatch between immediate deletion language and the request-and-review flow | Rename the title to `Request Account Deletion` or align all destructive copy around the request-based workflow |
| 💡 UX Suggestion | `U-14 Semantic color usage`: the main title is neutral dark text even though the spec calls for destructive/red styling on the title | Either apply destructive styling to the title as specified or soften the destructive framing in the spec and keep the red emphasis on the CTA/modal only |

#### Screen P01.1-S2: Identity Verification Step

**Layout**: `layout-temp/Verify Your Identity/Password.jpg`, `layout-temp/Verify Your Identity/Password-1.jpg`, `layout-temp/Verify Your Identity/Password/Error.jpg`, `layout-temp/Verify Your Identity/Password/Error-1.jpg`, `layout-temp/Show error message and allow retry.jpg`, `layout-temp/Show rate-limit/lockout message and prevent retry.jpg`

##### Flow Context

- **User arrives from**: `Request Deletion` on P01.1-S1 when re-authentication is required, per the flow diagram at `missing-mobile-flows-design-complement.md:77-86`
- **Screen purpose**: Verify the patient by password or email OTP before allowing the deletion request to reach final confirmation
- **Entry point**: Present. The refreshed layout set now includes dedicated identity-verification screens for password and email OTP methods
- **Exit path**: Present but inconsistent. Base screens show `Verify` and `Cancel`, while the lockout state exits through `Go back to the Setting Page`, which conflicts with the flow’s Profile-based entry/exit path
- **Data continuity**: Correct. The screen stays within the delete-account journey and preserves the destructive verification context across password, OTP, error, retry, and lockout variants
- **Flow context issues**: Lockout variant points the user to `Setting Page` rather than a Profile/flow exit label that matches the rest of P01.1

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | All verification variants show `Verify Your Identity` prominently |
| Back Navigation | Yes | ✅ | A back arrow is visible at top-left across the verification variants |
| Security Icon | Yes | ✅ | All verification variants show a shield/security icon at the top center |
| Instruction Text | Yes | ✅ | Base password and OTP variants show `For your security, please verify your identity before proceeding` |
| Verification Method Selector | Yes | ✅ | `Password` and `Email OTP` selectors are present as two switchable tabs, which is functionally equivalent to the required method chooser |
| Password Field | Conditional | ✅ | `Password.jpg` and `Error.jpg` show a masked password field with a visibility toggle when the password method is selected |
| Email OTP Field | Conditional | ✅ | `Password-1.jpg` and `Error-1.jpg` show a 6-digit OTP input when the email method is selected |
| Resend OTP Link | Conditional | ✅ | `Password-1.jpg` and `Error-1.jpg` show a `Resend code` action for the OTP method |
| Error Message | Conditional | ✅ | `Error.jpg` shows `Invalid password. Please try again.` and `Error-1.jpg` shows `Invalid OTP. Please try again.` |
| Verify Button | Yes | ✅ | All base/error states show a destructive `Verify` CTA that is disabled until input is present and enabled on populated error states |
| Cancel Button | Yes | ❌⚠️ | Base verification states show `Cancel`, but the rate-limit/lockout variant replaces the exit action with `Go back to the Setting Page`, which does not match the required cancel/return behavior for this flow |

**Extra Elements**:

- `Forgot your password?` link on password variants — useful recovery path, but not specified in the P01.1-S2 field table
- `Something went wrong` retry modal — additional generic/system error state beyond the specified invalid password/OTP inline validation

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 10/11 (91%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17 CTA label clarity`: the lockout-state CTA says `Go back to the Setting Page`, which is inconsistent with the Profile-based entry point and does not clearly describe the user’s next step in the delete-account flow | Rename the CTA to `Back to Profile` or another flow-consistent exit label and route it to the actual intended destination |
| ⚠️ UX Improvement | `U-14 Semantic color usage`: the blocking/lockout exit CTA is styled green even though it appears inside an error/attempt-limit state | Use a neutral secondary style for the exit CTA or reserve green for clearly positive outcomes only |
| 💡 UX Suggestion | `U-19 Error state clarity`: the generic `Something went wrong` modal is less actionable than the strong inline invalid-password/OTP messages and does not tell the user whether the issue is network, server, or auth-policy related | Add a more specific cause label or recovery hint if this generic error state is kept as a separate modal |

#### Screen P01.1-S3: Deletion Request Submitted Confirmation

**Layout**: `layout-temp/Deletion Request Submitted Confirmation.jpg`

##### Flow Context

- **User arrives from**: Successful confirmation after the deletion request is created and queued for Admin review, per the flow diagram at `missing-mobile-flows-design-complement.md:95-101`
- **Screen purpose**: Confirm that the deletion request was submitted, show its status/reference metadata, and explain next steps
- **Entry point**: Present. `Deletion Request Submitted Confirmation.jpg` shows a dedicated success/confirmation screen for the submitted request
- **Exit path**: Present. The screen provides `Back to Profile`, and `Profile.jpg` shows the matching destination screen with the `Delete account` item in the profile menu
- **Data continuity**: Correct. The screen carries forward the request state, reference, submitted timestamp, legal-retention reminder, and closed-inquiry note expected after submission
- **Flow context issues**: None

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Confirmation Icon | Yes | ✅ | A green confirmation/check icon is shown at the top of `Deletion Request Submitted Confirmation.jpg` |
| Screen Title | Yes | ✅ | `Deletion Request Submitted` is displayed prominently |
| Request Status | Yes | ✅ | A `Pending Admin Review` badge is visible below the title |
| Request Reference | Yes | ✅ | A request reference ID is displayed in the `Request Details` section |
| Submitted Timestamp | Yes | ✅ | The screen shows `Submitted: 10:15 AM, 26 June 2026` |
| Processing Timeline Notice | Yes | ✅ | The info box states `We complete verified deletion requests within 30 calendar days.` |
| What Happens Next Section | Yes | ✅ | The `What Happens Next` section includes review, additional verification, status updates/final outcome, and closed inquiries |
| Retained Data Reminder | Yes | ✅ | The legal-retention section states medical and financial transaction records are retained for at least 7 years with restricted access |
| Email Confirmation Notice | Yes | ⚠️ | The email notice exists, but it still shows placeholder text `[patient email address]` instead of the patient’s actual registered email |
| Back to Profile Button | Yes | ✅ | A prominent `Back to Profile` CTA is shown at the bottom of the screen |

**Extra Elements**:

- `Request Details` section heading — useful grouping enhancement, not explicitly listed in the spec field table

**Screen Status**: 🟢 GOOD
**Field Coverage**: 10/10 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-11 Label clarity`: the confirmation email line still uses bracketed placeholder text, which weakens the perceived credibility of the submitted-success state | Replace the placeholder with the actual bound patient email in the rendered design example |

**Flow Coverage Gaps**:

- `P01.1-S1` still has a title/copy semantics issue and a support-action styling mismatch
- `P01.1-S2` still has an inconsistent lockout exit action (`Go back to the Setting Page`) relative to the flow’s Profile-based path
- `P01.1-S3` is substantially complete but still uses placeholder email text instead of bound sample data

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | P01.1 | P01.1-S1 | Screen title uses immediate deletion language and neutral styling, while the flow actually submits a deletion request for review | Rename the title to match the request-based workflow and align the title styling with the chosen destructive semantics in a follow-up pass |
| ⚠️ Important | P01.1 | P01.1-S1 | Conditional support escape path is implemented as a green primary button instead of the specified link-style action | Either restyle the support action as a link or update the underlying spec if a primary support button is the intended behavior in a follow-up pass |
| ⚠️ Important | P01.1 | P01.1-S2 | Lockout state exits to `Setting Page` instead of the flow-consistent Profile/cancel destination | Rename and reroute the lockout CTA to match the actual exit destination for the delete-account flow in a follow-up pass |
| 💡 Suggestion | P01.1 | P01.1-S3 | Confirmation email notice still shows placeholder text instead of a bound patient email value | Replace the placeholder with representative bound sample data in the design in a follow-up pass |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Source spec: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
- Verification limited to flow P01.1 and the current refreshed `layout-temp/` contents
- All three required P01.1 screens are now represented in the current layout set
- `Profile.jpg` was used only to confirm that the success CTA destination exists in the broader flow context
- Approval decision: user approved the flow on 2026-03-24 despite the minor remaining issues listed in Action Items
