# Android QA Report — New Inquiry Creation

Date: 2026-04-09
Session ID: 20260409-new-inquiry-anr
Mode: flow-validation
Tool mode: Raw ADB
Device: emulator-5554 (sdk_gphone64_arm64)
App version: 1.0.0 (versionCode 3)
Flow script: none — new flow not recorded because the session ended in an ANR before the flow could be completed

## Summary

Pass: 1 / Fail: 1 / Partial: 0 / N/A: 0

The app was already open and logged in as a patient account on the Dashboard. Tapping the primary CTA `Create request for full service` did not open FR-003 Screen 1. Instead, the app became unresponsive and Android showed an Application Not Responding dialog for `com.samasu.hairline`.

## PRD References

- `local-docs/project-requirements/functional-requirements/fr003-inquiry-submission/prd.md#workflow-1-patient-inquiry-creation-primary-flow`
- `local-docs/project-requirements/functional-requirements/fr003-inquiry-submission/prd.md#screen-1-service-selection`

## Test Steps

| # | Action | Expected | Result | Screenshot | Notes |
|---|--------|----------|--------|------------|-------|
| 1 | Verify logged-in patient Dashboard is visible and primary CTA `Create request for full service` is present | Dashboard is usable and ready to start a new inquiry flow | Pass | `pre-session.png` | Patient account was already authenticated; no credentials were entered during this run |
| 2 | Tap `Create request for full service` from the Dashboard | FR-003 Screen 1 `Service Selection` should open | Fail | `step-1b-after.png` | Android displayed `Process system isn't responding` while the app froze behind the modal; no inquiry creation screen appeared |

## Defects

| # | Step | Severity | Description | Screenshot |
|---|------|----------|-------------|------------|
| 1 | 2 | Critical | The primary patient entry point for inquiry creation triggers an ANR instead of opening the inquiry flow. This blocks all downstream FR-003 behavior. Logcat shows `ANR in com.samasu.hairline (com.samasu.hairline/.MainActivity)` and `Input dispatching timed out ... Waited 5062ms for MotionEvent`. | `step-1b-after.png` |

## Logcat Highlights

- `local-docs/reports/2026-04-09/android-qa-new-inquiry/logcat-final.txt:56140` — `Window ... com.samasu.hairline/.MainActivity ... is unresponsive`
- `local-docs/reports/2026-04-09/android-qa-new-inquiry/logcat-final.txt:56195` — `ANR in Window{... com.samasu.hairline/.MainActivity}`
- `local-docs/reports/2026-04-09/android-qa-new-inquiry/logcat-final.txt:59339` — `ANR in com.samasu.hairline (com.samasu.hairline/.MainActivity)`
- `local-docs/reports/2026-04-09/android-qa-new-inquiry/logcat-final.txt:59341` — `Reason: Input dispatching timed out ... Waited 5062ms for MotionEvent`

## Screenshots Index

- `local-docs/reports/2026-04-09/android-qa-new-inquiry/pre-session.png`
- `local-docs/reports/2026-04-09/android-qa-new-inquiry/step-1-after.png`
- `local-docs/reports/2026-04-09/android-qa-new-inquiry/step-1b-after.png`
- `local-docs/reports/2026-04-09/android-qa-new-inquiry/session-end.png`
- `local-docs/reports/2026-04-09/android-qa-new-inquiry/session-end2.png`
- `local-docs/reports/2026-04-09/android-qa-new-inquiry/logcat-final.txt`

## Credentials Used

[REDACTED]
