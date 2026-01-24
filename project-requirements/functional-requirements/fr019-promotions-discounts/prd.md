# FR-019 - Promotions & Discount Management

**Module**: A-06: Discount & Promotion Management
**Feature Branch**: `fr019-promotions-discounts`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-019 from local-docs/project-requirements/system-prd.md; Transcriptions (admin/provider references)

---

## Executive Summary

Define, approve, and apply discounts across the Hairline platform with clear governance and auditability. Admins can create platform‑wide promotions (including those that affect both provider and Hairline fees), while providers can create their own discounts. The system validates codes at quote and booking, enforces usage limits and prioritization rules, and tracks usage and financial impact. This increases conversion while safeguarding provider margins and Hairline commission through an approval workflow and transparent reporting.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (P-03 overlay): See applied discount summary in quote/booking flows; enter a discount code when enabled; view final price breakdown.
- Provider Platform (PR-02/PR-05): Create provider-specific discounts; review and accept/decline platform discounts; see eligible discounts during quote creation; view discount impact in reports.
- Admin Platform (A-06): Create and manage platform discounts (platform‑only or both‑fees), configure categories, dates, limits, and code rules; manage approvals and track usage; view financial impact.
- Shared Services (S-03, S-02): Notification Service for approval and status alerts; Payment/Financial service for price calculation and settlement alignment.

### Multi-Tenant Breakdown

Patient Platform (P-03 overlay):

- Input discount code (if allowed at stage), see validation feedback.
- See discounted totals and savings; understand that only one discount applies.

Provider Platform (PR-02/PR-05):

- Create provider discounts with type (percent/fixed/package upgrade), dates, limits.
- Accept/decline platform both‑fees discounts per program; auto‑active provider‑only discounts.
- Select applicable approved discounts within quote creation (where rules allow).

Admin Platform (A-06):

- Create platform discounts: platform‑only, both‑fees, and Hairline‑only.
- Configure targets (all providers or subsets), dates, usage caps, stackability policy (single‑discount rule enforced globally).
- Manage approval workflow for both‑fees discounts; monitor provider responses.
- Track usage and financial impact with exports.

Shared Services (S-03, S-02):

- S-03 sends provider approval notifications and status updates.
- S-02 ensures correct price calculation and settlement attribution.

### Scope Boundaries

In Scope:

- Discount code definition and lifecycle (draft → active → expired), with usage limits and date windows.
- Discount validation and application at quote and booking; one discount per booking.
- Provider approval workflow for platform both‑fees discounts.
- Usage tracking and financial impact reporting.

Out of Scope:

- Stacking multiple discounts on a single booking (explicitly disallowed).
- Loyalty points and referral rewards (covered elsewhere).
- Tax/VAT calculation changes (handled by billing/finance rules).

### Entry Points

- Admin creates a platform discount in A-06; if both‑fees, providers receive approval requests.
- Provider creates a provider discount in PR-02/PR-05; becomes active per dates/limits.
- Patient enters a code (if enabled) at quote/booking; system validates and applies if eligible.

---

## Business Workflows

### Main Flow: Admin Creates Platform Discount (Both‑Fees)

Actors: Admin, Provider, System
Trigger: Admin submits a new platform discount that affects both fees
Outcome: Providers approve participation; discount becomes selectable where applicable

Steps:

1. Admin defines discount (type, value, dates, usage limit, targeted providers).
2. System saves discount as Pending Approval and notifies targeted providers.
3. Providers accept or decline; system logs responses.
4. When provider accepts, discount becomes eligible for that provider’s quotes during active window.
5. System tracks usage and financial impact per provider.

### Alternative Flows

**A1: Provider‑Only Discount**:

- Trigger: Provider creates their own discount.
- Steps: System validates inputs and activates per dates/limits; no approval needed.
- Outcome: Discount immediately eligible in provider’s quote creation.

**A2: Hairline‑Only Discount**:

- Trigger: Admin creates Hairline‑funded discount (commission only).
- Steps: System applies financial impact to Hairline share only; not visible to providers in selection UIs.
- Outcome: Booking reflects reduced platform commission; providers unaffected.

**B1: Code Validation Failure**:

- Trigger: Patient/provider enters invalid/expired/reached‑limit code.
- Steps: System returns reason; prevents application.
- Outcome: No discount applied; user can retry.

**B2: Single‑Discount Rule Conflict**:

- Trigger: Attempt to apply a code when a discount is already applied.
- Steps: System blocks stacking; prompts user to choose one.
- Outcome: Exactly one discount per booking.

---

## Screen Specifications

### Screen 1: Admin – Create/Manage Discount

Purpose: Let admins define and manage platform discounts with approval workflow.

Data Fields:

| Field Name       | Type        | Required | Description                                  | Validation Rules                 |
|------------------|-------------|----------|----------------------------------------------|----------------------------------|
| Discount type    | select      | Yes      | Percentage, fixed amount, package upgrade     | Must be one of allowed types     |
| Value            | number      | Yes      | Discount value                                | Range per type; max configurable |
| Start/End date   | datetime    | Yes      | Active window                                 | End ≥ Start                      |
| Usage limit      | number      | No       | Total uses allowed                            | ≥ 0 or blank for unlimited       |
| Target providers | multiselect | No       | Providers included (if subset)                | Valid provider IDs               |
| Affects fees     | select      | Yes      | Platform only, Both fees, Hairline only       | Controls approval path           |

Business Rules:

- Both‑fees discounts trigger provider approval requests.
- Hairline‑only discounts do not appear in provider selection UIs.

Notes:

- Bulk upload/edit for campaign management.

---

### Screen 2: Provider – Approvals & Discount Setup

Purpose: Allow providers to accept/decline platform discounts and configure their own discounts.

Data Fields:

| Field Name        | Type    | Required | Description                               | Validation Rules        |
|-------------------|---------|----------|-------------------------------------------|-------------------------|
| Approval list     | list    | Yes      | Pending platform discounts to review      | N/A                     |
| Decision          | buttons | Yes      | Accept/Decline with optional comment      | Comment ≤ 500 chars     |
| Provider discount | form    | No       | Create provider discount (type, value…)   | Same rules as admin     |

Business Rules:

- Decisions are logged with timestamp and user.

Notes:

- Display financial impact preview when possible.

---

### Screen 3: Quote/Booking – Apply Discount

Purpose: Validate and apply a single discount during quote/booking.

Data Fields:

| Field Name      | Type  | Required | Description                          | Validation Rules                      |
|-----------------|-------|----------|--------------------------------------|---------------------------------------|
| Code input      | text  | No       | Optional discount code               | Format rules; 1 active code at a time |
| Price breakdown | panel | Yes      | Base price, discount, totals         | Must reflect applied rules            |

Business Rules:

- One discount per booking; entering a new code replaces the current one after confirmation.
- Validation occurs both at quote and booking confirmation.

Notes:

- Clear feedback for invalid/expired/limit‑reached codes.

---

## Success Criteria

### Patient/Provider Experience Metrics

- SC-001: 95% of valid codes validate within 1 second at quote/booking.
- SC-002: 0% of bookings apply more than one discount (enforced at all steps).

### Admin/Operations Metrics

- SC-003: 95% of provider approval responses are processed and reflected within 5 seconds of submission.
- SC-004: Discount usage and impact reports export in ≤ 10 seconds for 95th percentile.

### Financial/Compliance Metrics

- SC-005: 100% of applied discounts have audit entries (who, when, what, amount, context).
- SC-006: Misapplied discounts detected and corrected to ≤ 0.1% of bookings monthly.

### Reliability Metrics

- SC-007: 99.9% monthly uptime for validation and calculation services.
- SC-008: Zero data loss for discount definitions and usage records.

---

## Business Rules

### General Module Rules

- Single‑discount rule enforced globally (patient code > provider code > affiliate code priority when conflicts arise).
- Usage limits and active dates are enforced at validation time.
- All discount creations, approvals, applications, and removals are auditable.

### Data & Privacy Rules

- Display only non‑sensitive discount info to patients; provider/Hairline cost splits remain internal.
- Financial records and discount artifacts retained for ≥ 7 years; takedowns handled by archival, not deletion.
- Access governed by RBAC; only authorized roles can create/approve/apply discounts beyond self‑service code entry.

### Admin Editability Rules

Editable by Admin:

- Discount categories, code format policy, max value caps, and campaign dates.
- Targeting rules (all providers vs. subsets) and approval routing.
- Notification templates for approvals and status.

Fixed in Codebase (Not Editable):

- Single‑discount rule and priority order.
- Calculation order of operations (base → discounts → taxes/fees).

Configurable with Restrictions:

- Max discount value thresholds per policy and region.
- Auto‑decline window for unresponded provider approvals.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- PR-02: Inquiry & Quote Management – discount selection during quote creation.
- P-03: Booking & Payment – validate/apply discount at booking and settlement.
- A-05: Billing & Financial Reconciliation – reflect Hairline vs provider shares.
- S-03: Notification Service – provider approvals and status updates.
- S-02: Payment/Financial Service – price calculation and settlement.

### External Dependencies (APIs, Services)

- Email/Push providers (via S-03) for approval/status notifications.

### Data Dependencies

- Provider catalog and identifiers for targeting.
- Booking/quote entities with price components for calculation.

---

## Assumptions

### User Behavior Assumptions

- Providers respond to approval requests within 3 business days.
- Patients will attempt code entry primarily during quote review.

### Technology Assumptions

- Quote and booking flows expose a single code input surface.
- Calculation service supports deterministic rounding and currency rules.

### Business Process Assumptions

- Finance defines regional caps and policy; legal approves terms for promotions.

---

## Implementation Notes

### Technical Considerations

- Calculation pipeline: base price → discount (single) → taxes/fees; idempotent validation.
- Prevent race conditions across quote/booking with atomic application and revalidation on booking.
- Audit trail for all state changes; soft‑disable discounts without data loss.

### Integration Points

- Admin UI ↔ Promotion service: CRUD, approvals, targeting.
- Provider UI ↔ Promotion service: approvals, provider discounts.
- Quote/Booking ↔ Calculation service: validate/apply discount.

### Scalability Considerations

- Cache active discounts and targeting; invalidate on updates.
- Paginated usage reports; background generation for long ranges.

### Security Considerations

- RBAC on creation/approval/application; input validation on codes and values.
- Encryption in transit/at rest; audit logs tamper‑resistant.

---

## User Scenarios & Testing

### User Story 1 – Admin launches both‑fees discount (P1)

Why: Increase conversion for a campaign spanning multiple providers.

Independent Test: Create both‑fees discount, providers approve, discount appears in eligible quotes.

Acceptance Scenarios:

1. Given a new both‑fees discount, when saved, then targeted providers receive approval requests.
2. Given a provider approves, when a quote is created in active window, then the discount is selectable.

### User Story 2 – Provider creates own discount (P1)

Why: Allow providers to run targeted promotions without admin approval.

Independent Test: Provider creates discount; it appears in their quote creation and validates.

Acceptance Scenarios:

1. Given a provider discount, when dates start, then the discount is available for selection.
2. Given usage limit is reached, when applied, then validation fails with clear reason.

### User Story 3 – Patient applies code at booking (P2)

Why: Ensure final price uses a single validated discount.

Independent Test: Enter valid code at booking; total updates and audit entry recorded.

Acceptance Scenarios:

1. Given a valid code, when applied at booking, then totals update and audit records exist.
2. Given another code is entered while one is active, when confirmed, then the new code replaces the old one.

### Edge Cases

- Ineligible/expired/limit‑reached codes: validation fails with reason.
- Simultaneous attempts to apply codes: last confirmed selection wins; audit both attempts.
- Provider fails to respond to approval: auto‑decline after policy window; visible in audit.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-019-001**: System MUST allow admins to create platform discounts with type, value, dates, usage limits, and targeting.
- **REQ-019-002**: System MUST allow providers to create provider‑specific discounts with similar controls.
- **REQ-019-003**: System MUST validate and apply a single discount at quote and booking.
- **REQ-019-004**: System MUST enforce priority and non‑stacking rules (patient > provider > affiliate when conflicts arise).
- **REQ-019-005**: System MUST track usage and financial impact with exports and dashboards.

### Data Requirements

- **REQ-019-006**: System MUST persist discount definitions, approvals, and usage records with audit details.
- **REQ-019-007**: System MUST link applied discounts to quotes/bookings and participant entities.

### Security & Privacy Requirements

- **REQ-019-008**: System MUST restrict creation/approval/apply actions to authorized roles; patient sees only necessary pricing info.
- **REQ-019-009**: System MUST encrypt sensitive data and preserve tamper‑evident audit logs.

### Integration Requirements

- **REQ-019-010**: System MUST send provider approval notifications via Notification Service.
- **REQ-019-011**: System MUST integrate with calculation/settlement services for consistent totals.

### Marking Unclear Requirements

No unresolved clarifications remain for V1; loyalty/referral programs and stacking are out of scope.

---

## Key Entities

- Discount: id, type, value, active window, usage limit, targeting, affects fees (platform only, both fees, Hairline only).
- Approval: discount id, provider id, decision (accept/decline), comment, timestamp, actor.
- Application: booking/quote id, discount id, amount, actor, timestamp, context (quote/booking).
- ReportSnapshot (optional): aggregated usage and impact metrics for exports.

---

## Appendix: Change Log

| Date       | Version | Changes                                      | Author |
|------------|---------|----------------------------------------------|--------|
| 2025-11-11 | 1.0     | Initial PRD creation                         | AI     |
| 2025-11-11 | 1.1     | Filled scope, workflows, rules, and criteria | AI     |

---

## Appendix: Approvals

| Role           | Name | Date | Signature/Approval |
|----------------|------|------|--------------------|
| Product Owner  |      |      |                    |
| Technical Lead |      |      |                    |
| Stakeholder    |      |      |                    |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Last Updated**: 2025-11-11
