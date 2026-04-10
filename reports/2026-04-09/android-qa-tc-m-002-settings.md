# Android QA Report — TC-M-002: Profile > Settings

Date: 2026-04-09
Session ID: tc-m-002-settings-20260409
Mode: flow-validation
Tool mode: Raw ADB
Device: emulator-5554
App version: unknown (installed; no upgrade performed)
Flow script: local-docs/testing-plans/android-flow-scripts/settings-navigation.md (new — recorded this session)

## Summary

Pass: 15 / Fail: 2 / Partial: 0 / N/A: 0

## PRD References

- local-docs/testing-plans/2026-04-09/mobile-app-manual-testing-plan.md#TC-M-002

## Test Steps

| # | Action | Expected | Result | Screenshot | Notes |
|---|--------|----------|--------|------------|-------|
| 1 | Navigate to Profile tab → tap Settings | Settings screen loads with title "Settings" | Pass | step-1-after.png | |
| 2 | [CHECK] 4 rows: Notification settings, Privacy & Security, Terms & Conditions, Help & Support | All 4 rows visible with icons and chevrons | Pass | step-1-after.png | Row order in app: Notification settings, Privacy and security, Help and support, Terms and Conditions |
| 3 | Tap "Notification Settings" | Screen loads with title "Notification Settings" | Pass | step-3-after.png | |
| 4 | [CHECK] Email Notifications and Push Notifications toggles present | Both toggles visible with ON/OFF state | Pass | step-3-after.png | Both Switches confirmed via uiautomator dump (checkable=true, checked=true) |
| 5 | Toggle Email Notifications OFF then ON | Toggle animates; state changes | Pass | step-5-email-off.png, step-5-after.png | Toggle changed state correctly (checked=false then checked=true) |
| 6 | Toggle Push Notifications OFF then ON | Toggle animates; state changes | Pass | step-6-push-off.png, step-6-after.png | Toggle changed state correctly |
| 7 | [CHECK] Mandatory notifications note and system event notifications note displayed | Informational text present below toggles | Pass | step-3-after.png | Security note and booking/payment status note both present |
| 8 | Tap back | Returns to Settings Main Screen | Pass | step-8-after.png | Hardware back (keyevent 4) works correctly |
| 9 | Tap "Privacy & Security" | Screen loads with Change Password and Privacy Policy rows | Pass | step-9-after.png | |
| 10 | Tap "Privacy Policy" | Opens correctly in external browser | Pass | step-10-after.png | Chrome opened; Chrome notification permission dialog appeared and was dismissed first |
| 11 | [DATA] Check policy content renders | Readable, scrollable, no blank screen | Pass | step-11-browser.png | WebView loaded at hairline.app/privacy-policy; scrollable=true confirmed via uiautomator |
| 12 | Tap back to Privacy & Security, then back to Settings | Navigation stack correct | Pass | step-12-after.png | Both back navigations (browser → P&S → Settings) work correctly |
| 13 | Tap "Terms & Conditions" | Terms content opens correctly in external browser | Fail | step-13-after.png | Browser opened but page returned 404 Not Found at hairline.app/terms-of-use |
| 14 | [DATA] Check Terms content renders | Readable, no blank/error state | Fail | step-14-404-evidence.png | 404 error page displayed — content does not render |
| 15 | Tap back | Returns to Settings | Pass | step-15-after.png | Hardware back returns to Settings correctly |
| 16 | Tap "Help & Support" | Navigates to Help & Support Hub | Pass | step-16-after.png | Help Center, Contact Support, My Support Tickets all visible |
| 17 | Tap back | Returns to Settings | Pass | step-17-after.png | |

## Defects

| # | Step | Severity | Description | Screenshot |
|---|------|----------|-------------|------------|
| 1 | 13–14 | Minor | Terms & Conditions link opens `hairline.app/terms-of-use` which returns **404 Not Found**. Page does not exist at this URL. Fix: correct the URL or create the page. | step-14-404-evidence.png |

## Additional Observations

- **Steps 5–6 (toggle persistence):** Previous round noted "success toast appears but toggle state does not actually change/persist." This round, the toggle state DID change in the UI (checked=false when toggled OFF). Backend persistence was not explicitly verified — would require re-entering the screen after navigating away to confirm.
- **Chrome notification dialog (Step 10):** A one-time Chrome dialog appeared before the browser loaded the Privacy Policy URL. This is expected Chrome first-run behavior and does not indicate an app bug.
- **Notification Settings Switch discovery:** Flutter Switches appear in uiautomator dump as `android.widget.Switch` with `checkable=true`. This is more reliable than coordinate-only analysis.

## Screenshots Index

- pre-session.png — Dashboard/Home screen at session start (logged in)
- step-1-before.png / step-1-after.png — Profile screen → Settings screen
- step-3-before.png / step-3-after.png — Notification Settings screen
- step-5-before.png / step-5-email-off.png / step-5-after.png — Email toggle OFF→ON
- step-6-before.png / step-6-push-off.png / step-6-after.png — Push toggle OFF→ON
- step-8-before.png / step-8-after.png — Back to Settings
- step-9-before.png / step-9-after.png — Privacy & Security screen
- step-10-before.png / step-10-after.png — Privacy Policy in Chrome
- step-11-browser.png — Privacy Policy WebView content
- step-12-before.png / step-12-after.png — Back nav to Settings
- step-13-before.png / step-13-after.png — Terms & Conditions → 404
- step-14-404-evidence.png — 404 error evidence
- step-15-after.png — Back to Settings after Terms
- step-16-before.png / step-16-after.png — Help & Support Hub
- step-17-before.png / step-17-after.png — Back to Settings
- session-end.png — Final app state (Settings screen)
- logcat-final.txt — Full device logcat

## Credentials Used

[REDACTED]
