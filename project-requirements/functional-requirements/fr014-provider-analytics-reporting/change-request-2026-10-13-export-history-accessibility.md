# Change Request: Report History UI and Analytics Accessibility Rules

**Change Request ID**: CR-FR014-20261013-02
**Primary FR**: FR-014
**Triggering FR / Event**: Second FR-014 verify-fr pass (2026-10-13), Issues 6 and 9; constitution web-platform rule (WCAG 2.1 Level AA)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-13
**Decision Date**: 2026-10-13
**PRD Version Change**: v3.9 to v3.10
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

The second verify-fr pass found two gaps that could not be closed by correcting existing wording, because each needed new UI or new requirements beyond the approved PRD:

1. Screen 6 referred to a "Report History" section and to edit/pause/resume/delete actions for recurring exports, but neither UI was specified.
2. The constitution requires WCAG 2.1 Level AA for the provider and admin web platforms, yet FR-014 used Green/Amber/Red colour as the only status signal across many widgets and had no contrast or chart-alternative rules.

The Product Owner approved adding a Report History & Recurring Exports sub-section to Screen 6 and a global set of Accessibility Rules, each with a new requirement ID. This request approves documentation only, not implementation readiness.

## Baseline State

**Source version**: FR-014 v3.9, Screen 6 Business Rules, Business Rules, and Functional Requirements Summary

- Screen 6 stored generated reports for 7 days "for re-download from Report History section" and allowed recurring configurations to be edited, paused, resumed, or deleted, but defined no fields, statuses, actions, or empty states for either surface.
- No FR-014 rule addressed accessibility. Tier colours, benchmark variance, health badges, aging buckets, heatmaps, and outlier/gap flags relied on colour alone.

## Approved State

**Target version**: [FR-014 v3.10](prd.md) — Screen 6 "Report History & Recurring Exports", Business Rules "Accessibility Rules" (Rules 15C–15E), and REQ-014-114 / REQ-014-115

The PRD owns the full field tables and rules. In summary, Screen 6 gains two tabs: Generated Reports, which lists the last 7 days with status, expiry, download, and retry; and Recurring Exports, which lists configurations with next run, last run status, and edit/pause/resume/delete. All analytics screens must pair every colour signal with a text label or icon, meet AA contrast for text and chart marks, and provide a text or table alternative for each chart.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Screen 6 Report History | Referenced only; no UI | Generated Reports tab: fields with provenance, Queued/Generating/Ready/Failed status, 7-day expiry, Download and Retry actions, permission-checked access, empty state | Retention and retry rules had no surface to act on |
| Screen 6 recurring management | Actions named only | Recurring Exports tab: frequency, screens, recipients, next run, last run status, Active/Paused, Edit/Pause/Resume/Delete; no back-fill on resume | Make the existing recurring rules usable and testable |
| Accessibility | None | Rules 15C (no colour-only signals), 15D (WCAG AA contrast), 15E (chart text/table alternatives) | Constitution requires WCAG 2.1 AA on web platforms |
| Requirements | REQ-014-001 to REQ-014-113 | Adds REQ-014-114 (Report History) and REQ-014-115 (accessibility) | Traceable acceptance for the new scope |

## Scope and Impact

### In Scope

- New Screen 6 sub-section and REQ-014-114, using existing Entity 8 fields (`next_run_at`, `last_run_status`, `status`) and existing retention, retry, and recipient rules.
- New Accessibility Rules 15C–15E and REQ-014-115, applied to all 13 FR-014 screens.

### Out of Scope

- Changes to the locked Screen 1 layout. Rule 15C adds labels or icons within existing widgets, not new widgets or sections.
- New export formats, retention periods, recipient limits, or permission roles.
- Accessibility rules for other FRs or the patient mobile app.

### Affected Contracts

- **PRD owner**: [FR-014](prd.md) — Screen 6, Accessibility Rules, REQ-014-114, REQ-014-115.
- **Related FRs**: FR-009 (recipient team members), FR-031 (permissions for report visibility), S-03 Notification Service and S-05 Media Storage Service (secure links and stored artifacts). No contract change to these FRs.
- **System documents**: None.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Report history and recurring-configuration endpoints and UI, retry queueing, secure-link download, permission filtering; chart components' labels, icons, contrast, keyboard access, and text/table alternatives.
- **Compatibility / rollout risk**: Adding labels or icons to Screen 1 widgets must not alter its locked structure. Palette changes for contrast may affect the Figma reference and need design sign-off.
- **Data migration**: None.

## Acceptance and Validation

- A provider sees reports generated in the last 7 days, can download Ready reports and retry Failed ones, and does not see reports containing screens they are not permitted to view.
- A provider can edit, pause, resume, and delete a recurring configuration; resuming does not back-fill missed runs; edits apply from the next run.
- Every Green/Amber/Red or variance signal on all 13 screens has a visible text label or icon; automated contrast checks pass WCAG 2.1 AA; each chart exposes an accessible summary or data table.
- Documentation checks cover links, requirement IDs, and Markdown tables across the PRD, this request, and the update log.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-13 (verify-fr second pass: Issue 6 "add a global rule for icons/labels plus contrast"; Issue 9 "Add a Report History sub-section to Screen 6"). Documentation delta only.
- **Decision evidence**: FR-014 verify-fr session, 2026-10-13; constitution "Rules for Web Platforms (Provider & Admin)".
- **PRD change log**: [FR-014 Appendix: Change Log](prd.md#appendix-change-log), v3.10 row dated 2026-10-13.
- **Update log**: [FR014_VERIFICATION_FIXES_2026-10-13.md](../../update-logs/2026-10-13/FR014_VERIFICATION_FIXES_2026-10-13.md).
- **Supersedes**: None.
- **Superseded by**: None.
