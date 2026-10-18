# Change Request: Mandatory Inquiry-Cancelled Quote Notice (No Provider Toggle)

**Change Request ID**: CR-FR032-20261016-01
**Primary FR**: FR-032
**Triggering FR / Event**: SRC-MTG-002 quote model alignment and Product Owner follow-up decision log (2026-10-16); FR-020 v2.8 and FR-030 v1.13
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v1.9 to v1.12 (v1.10 MTG-002 alignment; v1.11 consolidated verification corrections; v1.12 final audit corrections)
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner decided that the inquiry-cancelled quote notice (`quote.cancelled_inquiry`) is mandatory and cannot be switched off. FR-030 already locked it for admins, but FR-020 and FR-030 described it as subject to FR-032 provider preference toggles, and FR-032's Quote Notifications toggle, Disable All and channel preferences could suppress it. FR-032 now removes provider control over this notice so a provider always learns that its quote is no longer active.

## Baseline State

**Source version**: FR-032 v1.9, Main Flow (Notification Preferences) step 4, Alternative Flow A5, Screen 3: Notification Preferences, Business Rules Rule 2, REQ-032-008 and REQ-032-009

Providers could turn off Quote Notifications, all notification types or a delivery channel. S-03 enforced these preferences for every notification except critical system alerts, so the inquiry-cancelled quote notice could be suppressed.

## Approved State

**Target version**: FR-032 v1.12, same headings plus REQ-032-031

- Screen 3 offers no toggle for the inquiry-cancelled quote notice. The Quote Notifications toggle states that it does not cover this notice.
- The notice is delivered to each affected provider regardless of notification type preferences, "Disable All" and channel preferences, in the same way as critical system alerts.
- The mandatory aftercare reassignment notice (`aftercare.provider_reassigned`, produced by FR-011) is listed with the other mandatory provider notices that no preference can suppress.
- All other notification preferences are unchanged.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Main Flow step 4 (Quote Notifications) | Toggle covered quote notices without exception | Toggle states that the inquiry-cancelled quote notice is mandatory and has no toggle | MTG-002, Q12 |
| Alternative Flow A5 step 6 | Only critical system alerts survive "all disabled" | Critical system alerts and mandatory notices, including `quote.cancelled_inquiry`, are still sent | Q12 |
| Screen 3 field table and business rules | No mandatory-notice rule | Quote Notifications row excludes the notice; new rule says no toggle exists and no preference can suppress it | Q12 |
| Rule 2 | Preferences apply to all notifications except critical system alerts | Mandatory notices such as `quote.cancelled_inquiry` also bypass preferences | Q12 |
| Functional requirements | None | REQ-032-031 added | Q12 |
| Mandatory provider notice exemption (Main Flow step 4, Screen 3, Rule 2, REQ-032-031) | Only `quote.cancelled_inquiry` named as preference-exempt | Every mandatory provider notice is exempt: `quote.cancelled_inquiry`, the `quote.accepted` outcomes, `booking.payment_window_expired`, `booking.revived` and `booking.rescheduled` | Q42; final audit notification finding F6 |
| User Story 2 scenario 2 | "All disabled" stops everything except critical system alerts | Critical system alerts and mandatory notices such as `quote.cancelled_inquiry` are still sent | Q12 |
| Aftercare reassignment notice (Screen 3 rules, Rule 2, REQ-032-031) | No aftercare reassignment notice listed | The mandatory FR-011 notice `aftercare.provider_reassigned` to the new aftercare provider is listed among the mandatory provider notices that preferences cannot suppress | Q47 |

## Scope and Impact

### In Scope

- Provider notification preference behaviour for `quote.cancelled_inquiry` in FR-032.
- Preference exemption for every other mandatory provider notice (final audit corrections).

### Out of Scope

- Other notification types, channel defaults and the event catalogue (owned by FR-030).
- Admin-side rule locking (FR-030) and dispatch rules (FR-020).

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md` — Main Flow step 4, Alternative Flow A5, Screen 3: Notification Preferences, Rule 2, User Story 2 scenario 2, REQ-032-031
- **Related FRs**: FR-020 (v2.8: `quote.cancelled_inquiry` delivered regardless of FR-032 preferences; REQ-020-020; User Story 4 scenario 3), FR-030 (v1.13: event locked and not subject to FR-032 preferences)
- **System documents**: None

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: S-03 preference enforcement for `quote.cancelled_inquiry`; Notification Preferences UI copy for Quote Notifications; "Disable All" behaviour
- **Compatibility / rollout risk**: Providers who turned off Quote Notifications or a channel will start receiving this notice again
- **Data migration**: None

## Acceptance and Validation

- A provider with Quote Notifications off, all types disabled, or a channel disabled still receives `quote.cancelled_inquiry` when the patient cancels the inquiry.
- Screen 3 shows no toggle that controls the inquiry-cancelled quote notice.
- FR-020, FR-030 and FR-032 all describe `quote.cancelled_inquiry` as mandatory and outside FR-032 preferences.
- The Quote and Schedule Notifications toggles, Disable All and channel preferences never suppress the `quote.accepted` outcomes, `booking.payment_window_expired`, `booking.revived` or `booking.rescheduled`.
- No provider preference suppresses `aftercare.provider_reassigned` for the new aftercare provider (Screen 3 rules, Rule 2, REQ-032-031).

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation approval); implementation reconciliation required, not assessed
- **Decision evidence**: SRC-MTG-002; decision log 2026-10-16, Post-execution open questions Q12; final decisions Q42 and Q47 (2026-10-18); final audit notification finding F6 and doc-control findings F1, F2
- **PRD change log**: v1.10 row (2026-10-16); v1.11 and v1.12 rows (2026-10-18)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: None
- **Superseded by**: None
