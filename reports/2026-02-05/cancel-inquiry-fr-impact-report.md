# Cancel Inquiry Flow — FR Impact Report

**Report Date**: 2026-02-05
**Report Type**: Cross-FR Impact Analysis
**Trigger**: Reactivation of patient-initiated Cancel Inquiry flow (P02.2)
**Primary FR**: FR-003 (Inquiry Submission & Distribution)

---

## Executive Summary

The patient-initiated Cancel Inquiry flow allows patients to cancel their own inquiry in stages **Inquiry**, **Quoted**, or **Accepted** (before Confirmed). This flow was not present in any existing FR PRD — only admin-initiated soft-delete existed. Reactivating this flow requires updates across **9 FRs** totaling ~36 section-level changes.

---

## Design Decisions

| # | Decision | Alternatives Considered | Rationale |
|---|---|---|---|
| 1 | Cancellation allowed in Inquiry, Quoted, Accepted stages | Limit to Inquiry+Quoted only | Accepted stage included; appointment slot released immediately |
| 2 | Primary flow appended to FR-003 | Standalone FR; inline updates to all FRs | FR-003 owns inquiry lifecycle; cross-references keep other FRs lean |
| 3 | Admin has oversight only, no reversal | Admin approval; admin reversal within grace | Keeps flow simple; consistent with patient autonomy |
| 4 | No cooldown after cancellation | 24h cooldown; admin-configurable cooldown | FR-003 one-active-inquiry rule is sufficient guard |
| 5 | Appointment slot released immediately on Accepted-stage cancel | Keep 48h hold; not applicable in MVP | Immediate release; cleaner cascade logic |
| 6 | All affected FRs get inline stage updates | Cross-reference only for Tier 2/3 | All stage enums updated inline for consistency |

---

## Impact Matrix

| FR | Tier | Change Type | Sections Affected | Priority |
|---|---|---|---|---|
| **FR-003** | 1 — Primary | New workflow, screen updates, rules, requirements, entities | 9 | Critical |
| **FR-004** | 2 — Inline | New quote status, cascade rules, provider screen update | 6 | High |
| **FR-005** | 2 — Inline | Stage badge, blocking rules, alternative flow, payment hold | 4 | High |
| **FR-006** | 2 — Inline | Pre-booking guard, slot release rule, scenario | 4 | High |
| **FR-020** | 3 — Light | Verify event, add quote cascade event, template guidance | 4 | Medium |
| **FR-030** | 3 — Light | Verify config row, add quote event row, template IDs | 4 | Medium |
| **FR-001** | 3 — Light | Clarify distinction, add notification event reference | 2 | Low |
| **FR-016** | 3 — Light | Filter, visibility, audit trail | 3 | Low |
| **FR-023** | 3 — Light | One clarifying note | 1 | Low |

**Total: 9 FRs, ~37 section-level changes**

---

## Tier 1: FR-003 — Inquiry Submission & Distribution (Primary Append)

### Changes Made

| # | Section | Change Type | Detail |
|---|---|---|---|
| 1 | Business Workflows | **New Workflow 5** | "Patient-Initiated Inquiry Cancellation" — full flow with actor, trigger, outcome, steps |
| 2 | Alternative Flows | **New flow A4** | "Patient cancels inquiry" under Workflow 1 alternatives |
| 3 | Screen 8: Inquiry Dashboard | **Add field** | "Cancel Inquiry" action button in Next Actions, visible only in Inquiry/Quoted/Accepted stages |
| 4 | Screen 8: Inquiry Dashboard | **Update field** | "Cancelled" added as valid Current Stage badge value |
| 5 | Business Rules: General | **New section** | "Cancellation Rules" covering eligibility, irreversibility, cascade, no cooldown |
| 6 | Business Rules: Data & Privacy | **Add rule** | Cancelled inquiry retained per FR-023 soft-delete policy |
| 7 | Functional Requirements | **New REQ-003-013** | Patient-initiated cancellation requirement |
| 8 | Key Entities: Inquiry | **Update** | Add `cancelledAt`, `cancellationReason` fields; "Cancelled" to status enum |
| 9 | User Scenarios | **New User Story 4** | Cancel Inquiry with acceptance scenarios per stage |

---

## Tier 2: Inline Stage & Cascade Updates

### FR-004 — Quote Submission & Management

| # | Section | Change Type | Detail |
|---|---|---|---|
| 1 | Workflow 3: Status Transitions | **Add trigger** | "Parent inquiry cancelled by patient" |
| 2 | Workflow 3 | **Add terminal state** | `"Cancelled (Inquiry Cancelled)"` as distinct quote status |
| 3 | Alternative Flows | **Add flow** | "Patient cancels inquiry while quotes active" cascade |
| 4 | Business Rules | **Add rule** | All quotes auto-cancelled when parent inquiry cancelled |
| 5 | Key Entities: Quote | **Update status enum** | Add `cancelled_inquiry_cancelled` |
| 6 | Functional Requirements | **New REQ-004-013** | Quote auto-cancellation on inquiry cancellation |

### FR-005 — Quote Comparison & Acceptance

| # | Section | Change Type | Detail |
|---|---|---|---|
| 1 | Screen 1: Stage badge | **Update** | "Cancelled" added to valid Current Stage values |
| 2 | Screen 1: Business Rules | **Add rule** | All Accept/Compare actions disabled when inquiry cancelled |
| 3 | Alternative Flows | **New flow A4** | "Inquiry cancelled during quote review" |
| 4 | Payment & Billing Rules | **Add rule** | Appointment slot hold released immediately on Accepted-stage cancellation |

### FR-006 — Booking & Scheduling

| # | Section | Change Type | Detail |
|---|---|---|---|
| 1 | Pre-booking validation | **Add guard** | System verifies inquiry not cancelled before booking |
| 2 | Payment hold rules | **Add rule** | Inquiry cancellation releases 48h slot hold immediately |
| 3 | Booking stage transitions | **Update** | "Cancelled" as valid upstream inquiry state blocking booking |
| 4 | User Scenarios | **New scenario** | Inquiry cancelled during 48h payment hold |

---

## Tier 3: Light-Touch Updates

### FR-020 — Notifications & Alerts

| # | Section | Change Type | Detail |
|---|---|---|---|
| 1 | Event Catalog | **Verify** | `inquiry.cancelled` event exists — confirm recipients match |
| 2 | Event Catalog | **Add row** | `quote.cancelled_inquiry` for quote cascade notifications |
| 3 | MVP channel rules | **Verify** | Both events fire on Email + Push |
| 4 | Content guidelines | **Add note** | Cancellation reason is patient-private; provider sees only "Inquiry cancelled by patient" |

### FR-030 — Notification Rules & Configuration

| # | Section | Change Type | Detail |
|---|---|---|---|
| 1 | Event Catalog | **Verify** | `inquiry.cancelled` row exists with correct defaults |
| 2 | Event Catalog | **Add row** | `quote.cancelled_inquiry` with default config |
| 3 | Template definitions | **Add** | Default template IDs for both events |
| 4 | Admin override rules | **Add note** | Provider receipt is mandatory (admin cannot disable) |

### FR-001 — Patient Authentication & Profile Management

| # | Section | Change Type | Detail |
|---|---|---|---|
| 1 | Screen 14: Profile Overview | **Add note** | Distinguish account deletion auto-close from explicit inquiry cancellation |
| 2 | Screen 16: Settings | **Add event** | `inquiry.cancelled` in system event notification list |

### FR-016 — Admin Patient Management

| # | Section | Change Type | Detail |
|---|---|---|---|
| 1 | Patient detail view | **Add visibility** | Cancelled inquiries visible with badge, reason, timestamp |
| 2 | Dashboard filters | **Add value** | "Cancelled" as inquiry stage filter |
| 3 | Audit trail | **Add event type** | Patient-initiated cancellation with who/when/what/reason |

### FR-023 — Data Retention & Compliance

| # | Section | Change Type | Detail |
|---|---|---|---|
| 1 | Retention rules | **Add clarifying note** | Cancelled inquiries subject to same retention as completed inquiries |

---

## Cascade Logic Summary

```md
Patient taps "Cancel Inquiry"
├── Inquiry status → "Cancelled"
├── All related quotes → "Cancelled (Inquiry Cancelled)"
│   └── Each affected provider → notification (inquiry.cancelled + quote.cancelled_inquiry)
├── If Accepted stage:
│   └── 48h appointment slot hold → released immediately
│       └── Provider → notified of slot availability
├── Patient → confirmation notification
├── Admin → audit log entry (oversight, no action required)
└── Inquiry → read-only in dashboard with "Cancelled" badge
```

---

## Assumptions

1. The `inquiry.cancelled` event already defined in FR-020/FR-030 is sufficient — no new event type needed for the inquiry-level notification
2. A new `quote.cancelled_inquiry` event is needed to distinguish quote cancellation due to inquiry cancellation from other quote cancellation reasons
3. Cancellation reason is required (application-defined options, not PRD-mandated list)
4. FR-006 booking flow is not reachable when cancellation is allowed (Accepted → 48h hold → Confirmed), so cascade applies to slot hold only, not confirmed bookings
5. Cancelled inquiries remain visible in patient dashboard (read-only with "Cancelled" badge) and admin dashboard

---

**Document Status**: Complete
**Next Steps**: Apply changes to all 9 FR PRDs; write update log
**Maintained By**: Product & Engineering Teams
