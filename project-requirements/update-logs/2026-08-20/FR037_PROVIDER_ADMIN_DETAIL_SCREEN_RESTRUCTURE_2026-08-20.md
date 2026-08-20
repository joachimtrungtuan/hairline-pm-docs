# FR-037 Provider and Admin Detail-Screen Restructure

**Date**: 2026-08-20
**Document**: `functional-requirements/fr037-monitor-hair-loss/prd.md` (v1.4 → v1.5)
**Trigger**: Product-owner decision to separate single-case overviews from daily-log and provider-advice detail pages

---

## Decision

Provider and Admin case-overview screens remain the navigation and summary surfaces for one monitoring case. A selected patient daily log and a selected provider-advice record now open dedicated detail screens rather than expanding their complete fields inside the overview.

## Provider Screen Structure

- **Screen 8**: full assigned monitoring/advice case list.
- **Screen 9**: overall information, patient-parity dashboard, calendar, questionnaire, advice-window summary, and advice history for one case.
- **Screen 10A**: complete read-only patient daily-log detail and media for one selected day.
- **Screen 10B**: dedicated provider-advice detail, submission, and versioned edit surface.
- **Screen 11**: provider withdrawal confirmation, moved from Screen 10.

## Admin Screen Structure

- **Screen 12**: full system-wide monitoring case list, moved from Screen 11.
- **Screen 13**: overall information, patient-parity dashboard, calendar, assignment/configuration controls, and audit context for one case, moved and narrowed from Screen 12.
- **Screen 14A**: complete patient daily-log detail with audited Admin correction controls.
- **Screen 14B**: complete provider-advice detail, advice-window context, and audited Admin correction/version history.

## Preserved Contracts

- Patient logs and provider advice remain separate record types and separate calendar events, including when they share a date.
- Provider advice-window availability, supersession-only expiry, submission, editing, and visible edit metadata remain unchanged.
- Provider access remains assigned-case-only; Admin edits remain permission-controlled, reason-gated, versioned, and audited.

## Validation

- Confirmed the Provider section contains Screens 8, 9, 10A, 10B, and 11 in order.
- Confirmed the Admin section contains Screens 12, 13, 14A, and 14B in order.
- Confirmed overview calendar routes and REQ-037-027 point to the new dedicated detail screens.
- Checked Markdown tables, whitespace, conflict markers, and stale legacy screen headings.
