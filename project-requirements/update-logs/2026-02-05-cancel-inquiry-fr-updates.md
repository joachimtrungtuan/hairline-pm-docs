# FR Update Log — Cancel Inquiry Flow (P02.2)

**Date**: 2026-02-05
**Trigger**: Reactivation of patient-initiated Cancel Inquiry flow (P02.2)
**Primary FR**: FR-003 (Inquiry Submission & Distribution)
**Impact Report**: `local-docs/reports/2026-02-05/cancel-inquiry-fr-impact-report.md`

---

## Summary

Added patient-initiated inquiry cancellation across **9 FRs** with **~37 section-level changes**. Patients can now cancel their own inquiry in stages Inquiry, Quoted, or Accepted (before Confirmed). Cancellation cascades to all related quotes, releases appointment slot holds, and notifies providers.

---

## Changes by FR

### Tier 1 — Primary Append

#### FR-003: Inquiry Submission & Distribution (v1.3 → v1.4)

| # | Section | Change |
|---|---------|--------|
| 1 | Alternative Flows | Added **A4**: Patient cancels inquiry (references Workflow 5) |
| 2 | Business Workflows | Added **Workflow 5**: Patient-Initiated Inquiry Cancellation — full flow with actors, trigger, outcome, 5 main steps, 2 alternative sub-flows (E1: no quotes, E2: Accepted stage with slot release) |
| 3 | Screen 8: Inquiry Dashboard | Added `Cancel Inquiry` action field (conditional on Inquiry/Quoted/Accepted stage) |
| 4 | Screen 8: Inquiry Dashboard | Added "Cancelled" to Current Stage badge valid values |
| 5 | Business Rules: General | Added **Cancellation Rules** (rule #4) with 11 sub-rules covering eligibility, irreversibility, cascade, no cooldown |
| 6 | Business Rules: Data & Privacy | Added retention clarification for cancelled inquiries (per FR-023 soft-delete policy) |
| 7 | Functional Requirements | Added **REQ-003-013** (patient cancellation), **REQ-003-014** (quote cascade), **REQ-003-015** (slot release) |
| 8 | Key Entities: Inquiry | Added `cancelledAt`, `cancellationReason`, `cancellationFeedback` fields; "Cancelled" to status enum |
| 9 | User Scenarios | Added **User Story 4** with 5 acceptance scenarios and 2 edge cases |

---

### Tier 2 — Inline Stage & Cascade Updates

#### FR-004: Quote Submission & Management (v1.1 → v1.2)

| # | Section | Change |
|---|---------|--------|
| 1 | Workflow 3: Status Transitions | Added "patient cancels parent inquiry" as trigger |
| 2 | Workflow 3 | Added cascade logic bullet: "Patient cancels parent inquiry" → all quotes auto-cancelled |
| 3 | Alternative Flows | Added inquiry cancellation cascade flow with `"Cancelled (Inquiry Cancelled)"` terminal status |
| 4 | Functional Requirements | Added **REQ-004-013** under new "Cancellation Cascade Requirements" section |
| 5 | Key Entities: Quote | Added `cancelled_inquiry_cancelled` to status enum |

#### FR-005: Quote Comparison & Acceptance (v1.2 → v1.3)

| # | Section | Change |
|---|---------|--------|
| 1 | Alternative Flows | Added **A4**: Inquiry cancelled during quote review |
| 2 | Screen 1: Current Stage badge | Added "Cancelled" to valid values |
| 3 | Screen 1: Business Rules | Added blocking rule: all Accept/Compare actions disabled when inquiry cancelled |
| 4 | Payment & Billing Rules | Added appointment slot hold release rule on Accepted-stage cancellation |

#### FR-006: Booking & Scheduling (v1.4 → v1.5)

| # | Section | Change |
|---|---------|--------|
| 1 | Pre-Booking Validation | Added guard: system verifies inquiry not cancelled before booking |
| 2 | Alternative Flows | Added **B3**: Patient Cancels Inquiry During 48-Hour Slot Hold (6 detailed steps) |

---

### Tier 3 — Light-Touch Updates

#### FR-020: Notifications & Alerts (v1.4 → v1.5)

| # | Section | Change |
|---|---------|--------|
| 1 | Event Catalog: `inquiry.cancelled` | Updated notes to reflect patient-initiated cancellation (FR-003 Workflow 5), stages, and privacy rule |
| 2 | Event Catalog | Added `quote.cancelled_inquiry` event row for quote cascade notifications to providers |

#### FR-030: Notification Rules & Configuration (v1.1 → v1.2)

| # | Section | Change |
|---|---------|--------|
| 1 | Event Catalog: `inquiry.cancelled` | Updated notes to reflect patient-initiated cancellation and privacy rule |
| 2 | Event Catalog | Added `quote.cancelled_inquiry` event with mandatory provider receipt (admin cannot disable) |

#### FR-001: Patient Authentication & Profile Management (v1.1 → v1.2)

| # | Section | Change |
|---|---------|--------|
| 1 | Screen 14: Profile Overview | Added clarifying note distinguishing account deletion auto-close from explicit inquiry cancellation |
| 2 | Screen 16: Settings | Added "Inquiry Cancelled" to system event notification triggers list |

#### FR-016: Admin Patient Management (v1.2 → v1.3)

| # | Section | Change |
|---|---------|--------|
| 1 | Screen 1: Status Filter | Added "Cancelled" and "Accepted" to filter options |
| 2 | Screen 1: Stage column | Updated badge description to include "Cancelled" with explanation of patient-initiated cancellation |
| 3 | Screen 7: Admin Actions | Added "Patient Inquiry Cancellation" as system-generated audit event type |

#### FR-023: Data Retention & Compliance (v1.1 → v1.2)

| # | Section | Change |
|---|---------|--------|
| 1 | REQ-023-003 | Added clarifying note: cancelled inquiries subject to same retention rules as completed inquiries |

---

## Design Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Cancellation allowed in Inquiry, Quoted, Accepted stages | Accepted stage included; appointment slot released immediately |
| 2 | Primary flow appended to FR-003 | FR-003 owns inquiry lifecycle; cross-references keep other FRs lean |
| 3 | Admin has oversight only, no reversal | Keeps flow simple; consistent with patient autonomy |
| 4 | No cooldown after cancellation | FR-003 one-active-inquiry rule is sufficient guard |
| 5 | Appointment slot released immediately on Accepted-stage cancel | Immediate release; cleaner cascade logic |
| 6 | All affected FRs get inline stage updates | All stage enums updated inline for consistency |

---

## Files Modified

| File | Path |
|------|------|
| FR-003 PRD | `local-docs/project-requirements/functional-requirements/fr003-inquiry-submission/prd.md` |
| FR-004 PRD | `local-docs/project-requirements/functional-requirements/fr004-quote-submission/prd.md` |
| FR-005 PRD | `local-docs/project-requirements/functional-requirements/fr005-quote-comparison-acceptance/prd.md` |
| FR-006 PRD | `local-docs/project-requirements/functional-requirements/fr006-booking-scheduling/prd.md` |
| FR-020 PRD | `local-docs/project-requirements/functional-requirements/fr020-notifications-alerts/prd.md` |
| FR-030 PRD | `local-docs/project-requirements/functional-requirements/fr030-notification-rules-config/prd.md` |
| FR-001 PRD | `local-docs/project-requirements/functional-requirements/fr001-patient-authentication/prd.md` |
| FR-016 PRD | `local-docs/project-requirements/functional-requirements/fr016-admin-patient-mgmt/prd.md` |
| FR-023 PRD | `local-docs/project-requirements/functional-requirements/fr023-data-retention-compliance/prd.md` |
| Impact Report | `local-docs/reports/2026-02-05/cancel-inquiry-fr-impact-report.md` |

---

**Document Status**: Complete
**Maintained By**: Product & Engineering Teams
