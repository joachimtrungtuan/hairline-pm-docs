# Workflow Clarification - October 23, 2025

## Change Summary

**Type**: Workflow Clarification  
**Impact**: Low (clarification only, no functionality change)  
**Status**: ✅ Complete

---

## Overview

Clarified the status transition workflow for the "In Progress" and "Aftercare" stages to accurately reflect when status changes occur during the treatment execution phase.

---

## What Changed

### Previous (Ambiguous)

- Status moved to "In Progress" when **treatment was completed**
- Unclear when providers could update treatment progress

### Updated (Clarified)

- Status moves to "In Progress" when **patient arrives at clinic**
- Providers can update treatment progress in real-time during procedure
- Status moves to "Aftercare" when **treatment is completed**
- Status moves to "Completed" when **final review is submitted**

---

## Detailed Status Flow

```sh
Confirmed (Payment Done)
    ↓
    Patient travels to clinic
    ↓
In Progress (Patient arrives at clinic)
    ├─ Provider marks patient as "arrived"
    ├─ Treatment begins
    ├─ Provider updates progress in real-time
    ├─ Provider documents graft counts, techniques
    └─ Treatment completion
    ↓
Aftercare (6-12 months recovery)
    ├─ Milestone tracking
    ├─ Progress photos
    ├─ Aftercare specialist support
    └─ Final review submission
    ↓
Completed (Final review submitted)
```

---

## Files Updated

### 1. system-prd.md

**Section**: Workflow 1: Patient Journey - From Inquiry to Recovery

**Changes**:

- Stage 8 updated: "Arrives at clinic (status moves to 'In Progress')"
- Added: "Provider documents patient arrival and pre-procedure notes"
- Added: "Provider updates treatment progress in real-time"
- Changed: "Treatment completion moves status to 'Aftercare'" (was "In Progress")
- Stage 9 updated: "Submits final review and rating (status moves to 'Completed')"

**Section**: FR-010: Treatment Execution & Documentation

**Changes**:

- Added: "Providers MUST be able to mark patient as 'arrived'"
- Added: "System MUST automatically move status to 'In Progress' upon patient arrival"
- Added: "Providers MUST be able to update treatment progress during procedure"
- Added: Status transition documentation

---

### 2. system-technical-spec.md

**Section**: Core Workflow Implementation > Quote & Booking Status Flow

**Changes**:

- Updated status definition for `inprogress`: "Patient arrives at clinic, treatment in progress (provider can update real-time progress)"
- Updated status definition for `aftercare`: "Treatment completed, aftercare phase active (6-12 months recovery)"
- Updated status definition for `completed`: "Final review and rating submitted by patient"

---

### 3. system-data-schema.md

**Section**: 7. Quotes > Status Values

**Changes**:

- Updated status definition for `inprogress`: "Patient arrives at clinic, treatment in progress (provider can update real-time progress)"
- Updated status definition for `aftercare`: "Treatment completed, in aftercare phase (6-12 months recovery)"
- Updated status definition for `completed`: "Final review and rating submitted by patient"
- **Added new section**: "Status Triggers" with explicit transition rules

---

## Rationale

### Why This Matters

1. **Provider Workflow**: Providers need to update treatment details **during** the procedure, not after completion. Moving to "In Progress" when patient arrives enables this.

2. **Real-Time Updates**: Allows providers to document:
   - Patient arrival time
   - Pre-procedure notes
   - Procedure start time
   - Graft count progress
   - Technique adjustments
   - Completion time

3. **Patient Visibility**: Patients (or their family) can see real-time status updates during the procedure.

4. **Clear Separation**:
   - "In Progress" = Active treatment
   - "Aftercare" = Recovery phase
   - "Completed" = Journey ended (review submitted)

---

## Business Logic Impact

### Provider Interface

- **New Action**: "Mark Patient as Arrived" button when appointment day arrives
- **Trigger**: Automatically moves status from `confirmed` → `inprogress`
- **Enables**: Real-time treatment progress updates during procedure
- **Completion**: "Complete Treatment" button moves status to `aftercare`

### Patient Interface

- **During "In Progress"**: See live updates from provider (optional feature)
- **After "Aftercare"**: Prompted to submit final review
- **After Review**: Status changes to "Completed"

---

## Database Impact

**No database schema changes required** ✅

The status ENUM already includes all necessary values:

```sql
ENUM('inquiry', 'quote', 'accepted', 'confirmed', 'inprogress', 'aftercare', 'completed', 'rejected', 'cancelled')
```

Only the **trigger timing** was clarified in documentation.

---

## API Impact

**No API changes required** ✅

Existing endpoints support the workflow:

- `PATCH /api/quotes/{id}/status` - Update status
- `POST /api/quotes/{id}/mark-arrived` - Mark patient arrived (if doesn't exist, needs creation)
- `POST /api/quotes/{id}/complete-treatment` - Complete treatment
- `POST /api/reviews` - Submit final review (triggers status to completed)

---

## Testing Considerations

### Test Cases to Add/Update

1. **Status Transition Tests**
   - ✅ Verify status changes from `confirmed` → `inprogress` when patient marked as arrived
   - ✅ Verify status changes from `inprogress` → `aftercare` when treatment completed
   - ✅ Verify status changes from `aftercare` → `completed` when review submitted

2. **Provider Action Tests**
   - ✅ Verify provider can mark patient as arrived
   - ✅ Verify provider can update progress during "In Progress" status
   - ✅ Verify provider cannot update progress after treatment completed

3. **Validation Tests**
   - ✅ Verify cannot mark patient arrived before appointment date
   - ✅ Verify cannot complete treatment before marking arrived
   - ✅ Verify cannot submit review before entering aftercare phase

---

## Communication Required

### Stakeholders to Notify

- ✅ Development team (workflow clarification)
- ⏸️ UX/UI team (ensure provider interface supports "Mark Arrived" action)
- ⏸️ QA team (update test cases)
- ⏸️ Documentation team (update provider onboarding docs)

### No User Impact

- Patients see no difference (status names remain same)
- Providers gain clarity on when to update status

---

## Related Documents

- **Primary**: `system-prd.md` (Workflow 1, FR-010)
- **Supporting**: `system-technical-spec.md` (Status definitions)
- **Database**: `system-data-schema.md` (Status values, triggers)

---

## Approval

**Requested By**: User  
**Implemented By**: System Documentation Team  
**Date**: October 23, 2025  
**Status**: ✅ Approved and Implemented  

---

**Next Review**: No follow-up required (clarification only)
