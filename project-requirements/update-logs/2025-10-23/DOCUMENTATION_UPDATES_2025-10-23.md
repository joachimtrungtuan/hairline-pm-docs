# Documentation Updates - October 23, 2025

## Overview

This document summarizes critical updates made to all system documentation to ensure alignment with client requirements from transcriptions and to address identified gaps.

---

## Summary of Changes

### 1. Quote/Booking Status Workflow

**Previous**: Inquiry → Quote → Accepted → Scheduled → Confirmed → In Progress → Aftercare → Completed (8 stages)

**Updated**: Inquiry → Quote → Accepted → Confirmed → In Progress → Aftercare → Completed (7 stages)

**Key Changes**:
- **Merged "Accepted" and "Scheduled"** into single "Accepted" status
- **Auto-accept workflow**: Patient acceptance immediately confirms appointment (no manual provider confirmation)
- **Providers must pre-schedule appointment times** when creating quotes
- **Quote expiration**: Configurable, default 48 hours (was 30 days)

---

### 2. Patient Anonymization Rules

**Updated Logic**:
- **Before payment (`Confirmed` status)**: Provider sees anonymized data only (e.g., "Mark P. - PAT-00123")
- **After payment completion**: Provider gains access to full name, contact details, passport information
- **Previous incorrect assumption**: Anonymization lifted at "booking" (before payment)

**Implementation**:
- Added `anonymization_level` column to `patients` table
- Values: `full` (before payment), `partial` (payment pending), `none` (payment completed)

---

### 3. Medical Questionnaire Alert System

**Three-Tier Alert System**:

| Alert Level | Color | Conditions | Provider Action |
|-------------|-------|------------|-----------------|
| **Critical** | Red | HIV, blood disorders, heart conditions, uncontrolled diabetes, bleeding disorders | Requires acknowledgment before quote submission |
| **Standard** | Yellow/Amber | Allergies, current medications, controlled conditions, high blood pressure | Review required |
| **None** | Green | No medical concerns | Proceed normally |

**Database Changes**:
- Added `critical_conditions` (JSON) to `medical_histories` table
- Added `alert_level` (VARCHAR) to `medical_histories` table

---

### 4. Split Payment / Installment Plans

**New Feature** (was completely missing):
- **Interest-free installments**: 2-9 monthly payments
- **30-day buffer rule**: Final payment must complete 30 days before procedure
- **Auto-calculation**: System calculates max installments based on time until procedure

**Example**:
- Procedure in 6 months = max 5 installments (30-day buffer)
- Procedure in 3 months = max 2 installments

**Database Changes**:
- **New table**: `installment_payment_plans` (91st table)
- Added to `payments` table:
  - `installment_plan_id` (UUID)
  - `installment_number` (INTEGER)
  - `total_installments` (INTEGER)
  - `is_installment` (BOOLEAN)

**New Functional Requirement**: FR-007B in system-prd.md

---

### 5. Treatment Package Structure (Base + Add-Ons)

**Previous**: All-inclusive bundled packages

**Updated**: Modular base + add-on structure

**Structure**:
```
Quote = Base Treatment + Selected Add-Ons
```

**Add-On Categories**:
- Hotels (4-star, 5-star)
- Transport
- Flights
- Medications
- PRP therapy

**Database Changes** (`packages` table):
- `is_base_package` (BOOLEAN)
- `is_addon` (BOOLEAN)
- `addon_category` (VARCHAR)

**Rationale**: Allows platform to take over travel/logistics without providers recreating packages

---

### 6. Treatment Creation Authority

**Updated Rule**: 
- **ONLY admin** can create treatment package templates
- **Providers** can ONLY select from pre-created templates (cannot create custom treatments)

**Previous incorrect implementation**: Providers could create custom treatments

**Benefits**:
- Ensures consistency in treatment videos and information
- Simplifies platform-managed service transition
- Maintains quality control

**New Functional Requirement**: FR-024 in system-prd.md

---

### 7. Discount Approval Workflow

**New Feature** (was missing):
- Platform discounts affecting **"both fees"** (provider + Hairline) require provider approval
- System sends approval notifications to providers
- Providers can accept/decline participation

**Discount Categories**:
1. **Provider Discount**: Provider-created, affects only provider fee (no approval needed)
2. **Platform Discount (Both Fees)**: Admin-created, requires provider approval, affects total
3. **Hairline Discount**: Admin-created, affects only Hairline commission (invisible to providers)
4. **Affiliate Discount**: Linked to affiliate code, typically Hairline-funded

**Database Changes** (`discounts` table):
- `requires_provider_approval` (BOOLEAN)
- `approval_status` (VARCHAR): pending, approved, rejected
- `approved_by_provider_id` (UUID)

**Updated**: FR-019 in system-prd.md

---

### 8. Quote Management Updates

**Added to `quotes` table**:
- `expiration_hours` (INTEGER, default 48) - customizable quote validity
- `auto_accepted` (BOOLEAN) - tracks auto-accept
- `appointment_pre_scheduled` (BOOLEAN) - provider pre-scheduled times

**Status ENUM Updated**:
- Removed: `scheduled` (merged into `accepted`)
- Added: `inquiry` (for consistency)

---

### 9. Data Retention Policy (CRITICAL)

**Added to Constitution** (Non-Negotiable Principle):
> **HARD DELETES STRICTLY PROHIBITED**: System MUST NOT allow hard deletion of any medical, financial, or patient data. Soft-deletes ONLY for all critical entities (7-year minimum retention for healthcare/tax compliance).

**Updated**:
- constitution-summary.md: Principle #6 now marked as NON-NEGOTIABLE
- system-data-schema.md: Added "Hard Deletes: PROHIBITED" to schema overview

---

### 10. Flight Cost Preview

**New Feature** (P1 requirement):
- During inquiry date selection, display estimated flight costs
- Format: "Est. flights: £220 - £450" (cheapest - average)
- Helps patients choose optimal dates based on travel costs

**Updated**: FR-008 in system-prd.md

---

## Files Modified

### 1. system-data-schema.md
- Updated quote status ENUM values
- Added medical alert columns to `medical_histories`
- Added quote expiration and auto-accept columns to `quotes`
- Added anonymization level to `patients`
- Added discount approval columns to `discounts`
- Added package structure columns to `packages`
- Added installment payment columns to `payments`
- Created new table: `installment_payment_plans`
- Updated total table count: 85+ → 91 tables
- Added hard delete prohibition to schema overview

### 2. system-prd.md
- Updated Patient Journey workflow (9 stages)
- Updated Provider Quote Management workflow
- Enhanced FR-002: Added 3-tier medical alert system
- Enhanced FR-004: Added auto-accept workflow and pre-scheduling
- **New FR-007B**: Split payment/installment plans
- Enhanced FR-008: Added flight cost preview (P1)
- Enhanced FR-019: Added discount approval workflow with 4 categories
- **New FR-024**: Treatment package management (admin-only creation, base + add-ons)
- Updated all workflow descriptions for correct status transitions

### 3. system-technical-spec.md
- **New section**: Core Workflow Implementation
  - Quote & booking status flow documentation
  - Payment processing architecture
  - Medical alert system implementation
  - Package structure (base + add-ons) code examples
- Added PHP code examples for:
  - Installment calculation logic
  - Medical condition classification
  - Quote composition with add-ons

### 4. constitution-summary.md
- **Updated Principle #6**: Data Integrity & Audit Trail (now NON-NEGOTIABLE)
- Added explicit prohibition on hard deletes
- Clarified 7-year retention requirement

---

## Critical Business Rules Codified

1. **Auto-Accept Eliminates Manual Step**: Reduces patient drop-off between acceptance and payment
2. **Anonymization Until Payment**: Protects patient privacy and prevents off-platform communication
3. **30-Day Payment Buffer**: Ensures providers have guaranteed payment before procedure
4. **48-Hour Quote Expiration**: Prevents pricing staleness and encourages timely decisions
5. **Admin-Only Treatment Creation**: Maintains quality and consistency across platform
6. **Provider Approval for Platform Discounts**: Ensures providers consent to margin impact
7. **Medical Alert Color-Coding**: Enables rapid risk assessment by providers
8. **Hard Delete Prohibition**: Ensures compliance with healthcare data retention laws

---

## Implementation Priority

### P1 (MVP - Must Implement):
1. ✅ Quote status workflow (7 stages)
2. ✅ Auto-accept with pre-scheduling
3. ✅ Patient anonymization until payment
4. ✅ Medical alert system (3 tiers)
5. ✅ Split payment / installments
6. ✅ Quote expiration (48 hours default)
7. ✅ Base + add-on package structure
8. ✅ Admin-only treatment creation
9. ✅ Flight cost preview during inquiry
10. ✅ Hard delete prohibition

### P2 (Enhanced):
1. Discount approval workflow
2. Advanced installment retry logic
3. Medical condition auto-flagging
4. Interactive quote expiration configuration

---

## Testing Requirements

### New Test Cases Required:

1. **Auto-Accept Workflow**
   - Verify status changes: Quote → Accepted (skips Scheduled)
   - Verify provider receives notification only (no manual confirmation)

2. **Anonymization**
   - Verify provider cannot see patient details before payment
   - Verify details revealed after payment completion

3. **Medical Alerts**
   - Test critical condition flagging (red alerts)
   - Test standard condition flagging (yellow alerts)
   - Verify provider acknowledgment requirement

4. **Installment Payments**
   - Test max installment calculation (30-day buffer)
   - Test automatic installment charging
   - Test payment failure retry logic
   - Test default notification to admin

5. **Quote Expiration**
   - Test 48-hour default expiration
   - Test admin configuration of expiration period
   - Test expired quote handling

6. **Package Structure**
   - Test base package + add-on selection
   - Test quote total calculation
   - Test add-on removal/replacement

---

## Next Steps

1. **Review & Approve**: Technical team review of all changes
2. **Technical Implementation**: Development team will handle:
   - API endpoint updates
   - Database migration scripts
   - Test suite enhancements
   - Frontend UI alignment
3. **Provider Onboarding Docs**: Update provider documentation with new quote submission requirements (pre-scheduling, expiration, base+add-on structure)
4. **Patient Communications**: Update help center and FAQs with new workflow information

---

## Questions for Stakeholders

1. **Installment Payment Processor**: Which Stripe feature should we use for automated recurring charges? (Subscriptions API vs Scheduled Payments?)
2. **Medical Alert Acknowledgment**: Should critical alerts block quote submission or just require checkbox?
3. **Quote Expiration**: Should expired quotes automatically delete or archive?
4. **Discount Approval**: How long should providers have to approve/decline platform discounts?
5. **Flight Cost Preview**: Which API should we integrate? (Amadeus, Skyscanner, or Kiwi.com?)

---

## Documentation Organization

All documentation updates have been made to:
- ✅ **system-data-schema.md** - Database design and entity relationships
- ✅ **system-prd.md** - Product requirements and user workflows
- ✅ **system-technical-spec.md** - Technical architecture and implementation guidance
- ✅ **constitution-summary.md** - Core principles and governance

These documents serve as the **single source of truth** for the Hairline platform requirements and should be referenced by all development, design, and product teams.

---

**Document Status**: ✅ Complete  
**Created**: 2025-10-23  
**Author**: System Documentation Team  
**Next Review**: After implementation kick-off

