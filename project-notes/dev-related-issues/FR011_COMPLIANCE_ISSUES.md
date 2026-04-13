# FR-011 Compliance Issues & Gap Analysis

**Project**: Hairline Backend API
**Module**: FR-011 - Aftercare & Recovery Management
**Date**: 2026-04-06
**Status**: 🟡 72% Compliant - Not Production Ready

---

## 📊 Executive Summary

**Overall Compliance**: **72%** 🟡

| Platform | Compliance | Status |
|----------|-----------|--------|
| Patient Platform (P-05) | 65% | 🟡 Needs Work |
| Provider Platform (PR-04) | 70% | 🟡 Acceptable |
| Admin Platform (A-03) | 85% | 🟢 Good |

**Critical Blockers**: 3
**High Priority Issues**: 6
**Medium Priority Issues**: 8

**Estimated Work to 95% Compliance**: **3-4 sprints**

---

## 🔴 P0 - CRITICAL BLOCKERS (Must Fix Before Launch)

### 1. Multiple Photo Upload Not Supported

**Issue**: Current implementation only supports single photo upload, but FR-011 requires "standardized head scan photo set (multiple 2D views)"

**Current State**:
```php
// AftercareMilestoneScanController.php:73
'scan_file' => 'required|string',  // Single base64 string only
```

**FR-011 Requirement**:
> "Screen 2: Scan Upload (V1 Photo Set)"
> "Patient captures head scan photo set (V1) using mobile app"
> "V1: standardized head scan photo set (multiple 2D views)"

**Database Issue**:
```sql
-- Current schema
aftercare_milestone_scans
├─ scan_file VARCHAR  -- ❌ Single file only
```

**Required Solution**:
1. Create new table `aftercare_milestone_scan_photos` for multiple photos
2. Update API endpoint to accept `photos[]` array instead of single `scan_file`
3. Support different photo angles (front, back, left, right, top)
4. Add photo quality validation

**Impact**:
- ❌ Mobile app cannot upload complete photo sets
- ❌ Violates core FR-011 requirement
- ❌ Provider cannot properly review patient progress

**Affected Screens**: Screen 2 (Patient), Screen 9 (Provider), Screen 14 (Admin)

**Reference**: FR-011 Screen 2, Business Rules - "Scan must meet minimum quality threshold", "Maximum file size: 50MB"

---

### 2. Purchase Workflow Completely Missing

**Issue**: Workflow 2 (Standalone Aftercare Service) and Workflow 2b (Post-Treatment Add-On) have no implementation

**Missing Screens**:
- Screen 6: Aftercare Service Purchase
- Screen 7: Aftercare Payment & Checkout

**Missing Endpoints**:
```
POST /api/aftercare/purchase-service
POST /api/aftercare/checkout
GET  /api/aftercare/purchase-status/{id}
POST /api/aftercare/payment/process
```

**FR-011 Requirements**:
- Patient browses available aftercare templates marked "Available for Purchase"
- Patient selects payment method (fixed or subscription)
- System processes payment via FR-007 Payment Processing
- Admin reviews and assigns standalone requests
- 90-day window for post-treatment add-on

**Current State**:
- ✅ Template pricing configuration exists (`enable_for_purchase`, `pricing_mode`, `pricing_data`)
- ❌ No purchase request form
- ❌ No payment integration
- ❌ No admin assignment workflow

**Impact**:
- ❌ Standalone aftercare service cannot be sold
- ❌ Cannot monetize external clinic patients
- ❌ Post-treatment add-on unavailable
- ❌ No revenue from aftercare service

**Affected Workflows**: Workflow 2, Workflow 2b

**Reference**: FR-011 Screens 6-7, Business Rules - Payment and Billing Rules

---

### 3. Progress Calculation Missing

**Issue**: No automated progress calculation as required by FR-011

**FR-011 Requirement**:
> "Progress = (completed tasks / total tasks) * 100"
> "Tasks weighted equally"
> "Progress updates in real-time"

**Current State**:
- ❌ No API endpoint for progress calculation
- ❌ No task completion tracking
- ❌ No overall progress percentage
- ❌ Dashboard cannot show progress metrics

**Missing Endpoints**:
```
GET /api/aftercare/progress/{aftercare_id}
GET /api/aftercare/dashboard/{patient_id}
GET /api/aftercare/tasks/upcoming
```

**Required Components**:
1. Task aggregation (scans, questionnaires, medication doses)
2. Completion percentage calculation
3. Milestone completion tracking
4. Next task determination
5. Overdue task flagging

**Impact**:
- ❌ Screen 1 (Dashboard) cannot be implemented
- ❌ Patients cannot see their progress
- ❌ Providers cannot track patient compliance
- ❌ Admin cannot monitor case performance

**Affected Screens**: Screen 1, Screen 12, Screen 18

**Reference**: FR-011 Screen 1, Workflow 3 - Progress Tracking

---

## 🟡 P1 - HIGH PRIORITY ISSUES

### 4. Questionnaire Mixed with Scan Upload

**Issue**: Current API mixes scan upload and questionnaire submission in same endpoint, violating FR-011 separation of concerns

**Current Implementation**:
```php
// POST /api/aftercare/create-aftercare-milestone-scan
$request->validate([
    'scan_file' => 'required|string',
    'questions_answered' => 'nullable|json',  // ❌ Should be separate
    // ...
]);
```

**FR-011 Requirement**:
- **Screen 2**: Scan Upload (photos only)
- **Screen 3**: Questionnaire Completion (questions only)
- Different workflows, different timings

**Required Solution**:
1. Remove `questions_answered` from scan upload endpoint
2. Create separate questionnaire submission endpoint
3. Link questionnaires to milestones separately

**Impact**:
- ⚠️ Confusion in mobile app implementation
- ⚠️ Cannot track questionnaire completion separately
- ⚠️ Violates single responsibility principle

**Reference**: FR-011 Screens 2-3

---

### 5. No Task Scheduling System

**Issue**: No system to schedule tasks, calculate due dates, or send reminders

**FR-011 Requirement**:
> "System sends notification for upcoming tasks (scan/photo set, questionnaire)"
> "System shows next upcoming tasks with countdown timers"
> "Overdue tasks highlighted in red"

**Missing Features**:
- Task due date calculation
- 7-day upcoming task list
- Overdue task detection
- Task reminder scheduling

**Current State**:
- `scan_date` field exists but no due date concept
- No integration with FR-020 (Notifications)
- No task scheduling table

**Impact**:
- ❌ Patients don't know when tasks are due
- ❌ No reminder notifications
- ❌ Cannot track overdue tasks
- ❌ Compliance monitoring impossible

**Reference**: FR-011 Screen 1, Workflow 3 - Milestone-Based Tasks

---

### 6. Medication Adherence Not Tracked

**Issue**: Screen 4 requirements for medication tracking not implemented

**FR-011 Requirements**:
- Track individual doses (Today's Doses, Mark as Taken)
- Calculate weekly adherence percentage
- Count missed doses
- Show adherence history

**Current State**:
- ✅ `AfterCareMedication` model exists (name, dosage, frequency)
- ❌ No dose logging table
- ❌ No "mark as taken" endpoint
- ❌ No adherence calculation

**Required Solution**:
```sql
CREATE TABLE aftercare_medication_doses (
  id UUID PRIMARY KEY,
  medication_id UUID,
  scheduled_time TIMESTAMP,
  taken_at TIMESTAMP,
  status ENUM('pending', 'taken', 'missed', 'skipped'),
  created_at TIMESTAMP
);
```

**Impact**:
- ❌ Screen 4 incomplete
- ⚠️ Cannot monitor medication compliance
- ⚠️ No adherence data for progress calculation

**Reference**: FR-011 Screen 4

---

### 7. No Scan Quality Validation

**Issue**: FR-011 requires quality threshold validation, but no validation exists

**FR-011 Requirements**:
> "Scan must meet minimum quality threshold"
> "System validates scan quality and provides feedback"
> "Quality Indicator: Real-time scan quality feedback"

**Current State**:
- ❌ No quality validation on upload
- ❌ No quality score field usage
- ❌ No quality feedback to user

**Required Solution**:
1. Implement image quality validation (blur detection, resolution check)
2. Add real-time feedback during capture
3. Store quality score in database
4. Reject poor quality scans with guidance

**Impact**:
- ⚠️ Poor quality scans accepted
- ⚠️ Providers cannot properly review progress
- ⚠️ Medical assessment compromised

**Reference**: FR-011 Screen 2, Business Rules - Task Completion

---

### 8. 90-Day Add-On Window Not Enforced

**Issue**: Workflow 2b requires 90-day window for post-treatment add-on, no validation exists

**FR-011 Requirement**:
> "Workflow 2b: Post-Treatment Aftercare Add-On"
> "Trigger: Hairline-treated patient requests aftercare service after treatment completion (within 90 days)"

**Current State**:
- ❌ No treatment completion date tracking
- ❌ No 90-day window validation
- ❌ No eligibility check endpoint

**Required Solution**:
```php
GET /api/aftercare/eligibility/{patient_id}
Response: {
  "eligible": true/false,
  "treatment_date": "2026-01-15",
  "days_remaining": 45,
  "reason": "within_90_day_window"
}
```

**Impact**:
- ⚠️ Business rule violation
- ⚠️ Incorrect add-on availability

**Reference**: FR-011 Workflow 2b

---

### 9. Missing Escalation Workflow

**Issue**: No automated escalation when tasks are overdue

**FR-011 Requirement**:
> "Overdue tasks trigger escalation after 48 hours"
> "System flags case as 'Urgent'"
> "Aftercare team immediately contacts patient"

**Current State**:
- ✅ `AftercareEscalation` model exists
- ❌ No automation logic
- ❌ No 48-hour trigger
- ❌ No urgent flag system

**Impact**:
- ⚠️ Manual escalation only
- ⚠️ Delayed patient care
- ⚠️ Compliance issues not caught

**Reference**: FR-011 Workflow 3 - Alternative Flow C1

---

## 🟠 P2 - MEDIUM PRIORITY ISSUES

### 10. No Integration with FR-020 Notifications

**Issue**: Dependency on FR-020 (Notifications & Alerts) not integrated

**FR-011 Requirements**:
- Task reminder notifications
- Milestone completion notifications
- Urgent alert notifications
- Progress update notifications

**Current State**: No notification triggers in aftercare module

**Impact**: ⚠️ Patients miss tasks, no automated reminders

---

### 11. No Stripe Payment Integration

**Issue**: Payment processing not integrated despite FR-007 dependency

**FR-011 Requirements**:
- Standalone aftercare payment processing
- Subscription payment setup
- Refund processing
- Payment confirmation

**Current State**:
- ✅ `AftercarePayment` model exists
- ❌ No Stripe integration

**Impact**: ❌ Cannot accept payments for standalone service

---

### 12. No File Size Validation

**Issue**: FR-011 specifies 50MB limit per photo, not enforced

**FR-011 Requirement**:
> "Maximum file size: 50MB"

**Current State**: No validation in API

**Required Fix**:
```php
'photos.*' => 'file|max:51200',  // 50MB in KB
```

**Impact**: ⚠️ Potential storage abuse, performance issues

---

### 13. Educational Resources Viewing Not Tracked

**Issue**: Screen 5 requires tracking which resources patient has viewed

**FR-011 Requirements**:
- Mark as Viewed checkbox
- Resources Viewed Count
- Completion Percentage
- View history

**Current State**:
- ✅ Resources stored
- ❌ No viewing tracking

**Impact**: ⚠️ Cannot monitor patient education compliance

---

### 14. No Provider Performance Metrics

**Issue**: Screen 17 (Provider Performance Dashboard) has no implementation

**FR-011 Requirements**:
- Response time tracking
- Case load monitoring
- Completion rate tracking
- Patient satisfaction scores

**Current State**: No metrics collection

**Impact**: ⚠️ Cannot evaluate provider performance

---

### 15. No Admin Audit Trail

**Issue**: FR-011 requires admin edit tracking, not fully implemented

**FR-011 Requirement**:
> "All admin edits logged with timestamp and admin identification"
> "Change reason required for all modifications"
> "Edit history maintained for audit trail"

**Current State**:
- ✅ `AftercareAuditLog` model exists
- ❌ Not used in controllers
- ❌ No change reason field

**Impact**: ⚠️ Compliance and accountability issues

---

### 16. No Concerning Response Flags

**Issue**: Questionnaire should auto-flag concerning answers

**FR-011 Requirement**:
> "System processes responses and flags concerning answers"
> "Warning for concerning responses"
> "System flags case as 'Urgent'"

**Current State**: No flagging logic

**Impact**: ⚠️ Medical issues may go unnoticed

---

### 17. No Draft Saving for Questionnaires

**Issue**: Screen 3 requires auto-save draft functionality

**FR-011 Requirement**:
> "Save Draft: Save progress without submitting"
> "Drafts saved automatically every 30 seconds"

**Current State**: No draft support

**Impact**: ⚠️ Data loss if patient exits mid-questionnaire

---

## 📋 MISSING ENDPOINTS SUMMARY

### Critical Endpoints

```
🔴 POST   /api/aftercare/scans/upload-photos          (Multiple photo upload)
🔴 GET    /api/aftercare/dashboard/{patient_id}       (Dashboard aggregation)
🔴 GET    /api/aftercare/progress/{aftercare_id}      (Progress calculation)
🔴 POST   /api/aftercare/purchase-service             (Purchase workflow)
🔴 POST   /api/aftercare/payment/checkout             (Payment processing)
```

### High Priority Endpoints

```
🟡 POST   /api/aftercare/questionnaire/submit         (Separate questionnaire)
🟡 GET    /api/aftercare/tasks/upcoming               (7-day task list)
🟡 POST   /api/medication/doses/mark-taken            (Medication tracking)
🟡 GET    /api/aftercare/eligibility/{patient_id}     (90-day window check)
🟡 GET    /api/aftercare/scans/quality-check          (Quality validation)
```

### Medium Priority Endpoints

```
🟠 POST   /api/aftercare/resources/mark-viewed        (Resource tracking)
🟠 GET    /api/aftercare/medication/adherence/{id}    (Adherence calculation)
🟠 GET    /api/admin/provider-performance             (Performance metrics)
🟠 POST   /api/aftercare/escalation/create            (Manual escalation)
```

---

## 🗄️ MISSING DATABASE TABLES

### Critical Tables

```sql
-- Multiple photos per scan
CREATE TABLE aftercare_milestone_scan_photos (
    id UUID PRIMARY KEY,
    scan_id UUID REFERENCES aftercare_milestone_scans(id),
    photo_url TEXT NOT NULL,
    photo_type ENUM('front', 'back', 'left', 'right', 'top'),
    quality_score INT,
    file_size BIGINT,
    order INT,
    created_at TIMESTAMP
);

-- Purchase requests for standalone service
CREATE TABLE aftercare_purchase_requests (
    id UUID PRIMARY KEY,
    patient_id UUID,
    template_id UUID,
    service_type ENUM('standalone', 'post_treatment_addon'),
    treatment_date DATE,
    treatment_type VARCHAR,
    external_clinic VARCHAR,
    payment_method ENUM('fixed_price', 'subscription'),
    status ENUM('pending_payment', 'pending_assignment', 'assigned', 'rejected'),
    created_at TIMESTAMP
);
```

### High Priority Tables

```sql
-- Task scheduling and due dates
CREATE TABLE aftercare_task_schedule (
    id UUID PRIMARY KEY,
    aftercare_id UUID,
    milestone_id UUID,
    task_type ENUM('scan', 'questionnaire', 'medication'),
    due_date TIMESTAMP,
    completed_at TIMESTAMP,
    status ENUM('pending', 'completed', 'overdue', 'skipped'),
    created_at TIMESTAMP
);

-- Medication dose tracking
CREATE TABLE aftercare_medication_doses (
    id UUID PRIMARY KEY,
    medication_id UUID,
    scheduled_time TIMESTAMP,
    taken_at TIMESTAMP,
    status ENUM('pending', 'taken', 'missed', 'skipped'),
    notes TEXT,
    created_at TIMESTAMP
);
```

### Medium Priority Tables

```sql
-- Resource viewing tracking
CREATE TABLE aftercare_resource_views (
    id UUID PRIMARY KEY,
    patient_id UUID,
    resource_id UUID,
    viewed_at TIMESTAMP,
    duration_seconds INT
);

-- Provider performance metrics
CREATE TABLE aftercare_provider_metrics (
    id UUID PRIMARY KEY,
    provider_id UUID,
    metric_date DATE,
    active_cases INT,
    avg_response_time_hours DECIMAL,
    completion_rate DECIMAL,
    patient_satisfaction DECIMAL,
    created_at TIMESTAMP
);
```

---

## 🔄 REQUIRED INTEGRATIONS

### External Service Integrations

| Service | Purpose | Status | Priority |
|---------|---------|--------|----------|
| **Stripe API** | Payment processing, subscriptions, refunds | ❌ Not integrated | 🔴 Critical |
| **FR-020 Notifications** | Task reminders, alerts, progress updates | ❌ Not integrated | 🟡 High |
| **FR-007 Payment Module** | Payment flow coordination | ❌ Not integrated | 🔴 Critical |
| **FR-025 Questionnaires** | Dynamic questionnaire rendering | 🟡 Partial | 🟡 High |
| **Cloud Storage** | Secure photo storage with signed URLs | 🟡 Basic only | 🟡 High |

---

## 📊 WORKFLOW COMPLIANCE STATUS

| Workflow | FR-011 Section | Compliance | Issues |
|----------|---------------|-----------|--------|
| **Workflow 1**: Treatment-Linked Setup | Primary | 🟡 70% | Missing auto-trigger, notification integration |
| **Workflow 2**: Standalone Service | Secondary | 🔴 10% | **Entire purchase flow missing** |
| **Workflow 2b**: Post-Treatment Add-On | Secondary | 🔴 15% | **No 90-day validation, no purchase flow** |
| **Workflow 3**: Patient Activities | Ongoing | 🟡 50% | Missing progress tracking, task scheduling |
| **Workflow 4**: Admin Management | Management | 🟢 80% | Good implementation, minor gaps |

---

## 🎯 SCREEN COMPLIANCE SCORECARD

### Patient Platform (P-05)

| Screen | Name | Compliance | Critical Issues |
|--------|------|-----------|----------------|
| Screen 1 | Aftercare Dashboard | 🔴 25% | No dashboard API, no progress calculation |
| Screen 2 | Scan Upload | 🔴 30% | **Single photo only, no quality validation** |
| Screen 3 | Questionnaire | 🔴 20% | Mixed with scan, no draft saving |
| Screen 4 | Medication Schedule | 🔴 20% | No dose tracking, no adherence % |
| Screen 5 | Educational Resources | 🟡 50% | No viewing tracking |
| Screen 6 | Service Purchase | 🔴 10% | **Entire screen missing** |
| Screen 7 | Payment Checkout | 🔴 0% | **Entire screen missing** |

### Provider Platform (PR-04)

| Screen | Name | Compliance | Notes |
|--------|------|-----------|-------|
| Screen 8 | Cases List | 🟡 60% | Basic listing works, filters incomplete |
| Screen 9 | Patient Details | 🟡 70% | Most data accessible |
| Screen 10 | Aftercare Setup | 🟢 85% | Well implemented |
| Screen 11 | Plan Edit | 🟡 60% | Edit works but limited |
| Screen 12 | Progress Tracking | 🔴 30% | No progress calculation |

### Admin Platform (A-03)

| Screen | Name | Compliance | Notes |
|--------|------|-----------|-------|
| Screen 13 | Cases List | 🟢 80% | Good filtering |
| Screen 14 | Case Details | 🟢 85% | Multi-tab data accessible |
| Screen 15 | Standalone Requests | 🔴 10% | Purchase workflow missing |
| Screen 16 | Template Management | 🟢 **95%** | **Excellent!** |
| Screen 17 | Provider Performance | 🔴 20% | No metrics |
| Screen 18 | Progress Tracking | 🔴 30% | Limited tracking |

---

## ✅ POSITIVE FINDINGS (What's Working Well)

### Excellent Implementations 🌟

1. **Screen 16 - Template Management** (95% compliant)
   - Multi-step wizard complete
   - Pricing configuration robust (fixed/subscription/both)
   - Multi-currency support
   - Resource file handling excellent
   - Validation comprehensive

2. **Data Model Architecture** (80% compliant)
   - UUID primary keys
   - Proper relationships
   - JSON flexibility for complex data
   - Soft deletes & timestamps
   - Good migration history

3. **Admin Override Capabilities** (90% compliant)
   - Full data editability
   - Proper authorization
   - Template customization

4. **Code Quality**
   - Swagger documentation comprehensive
   - Request validation thorough
   - Error handling good
   - Transaction management proper
   - PSR-12 compliant

---

## 📅 RECOMMENDED IMPLEMENTATION ROADMAP

### Sprint 1 (Critical Fixes)

**Goal**: Fix blocking issues preventing core patient workflows

- [ ] Implement multiple photo upload
  - Create `aftercare_milestone_scan_photos` table
  - Update scan upload endpoint to accept `photos[]` array
  - Add photo type/angle support
  - Implement file size validation (50MB)

- [ ] Separate questionnaire endpoint
  - Remove `questions_answered` from scan endpoint
  - Create `POST /aftercare/questionnaire/submit`
  - Update mobile app integration

- [ ] Add basic progress calculation
  - Create progress calculation service
  - Implement `GET /aftercare/progress/{id}` endpoint
  - Calculate task completion percentage

### Sprint 2 (Purchase Workflow)

**Goal**: Enable standalone aftercare service monetization

- [ ] Implement purchase workflow (Screens 6-7)
  - Create `aftercare_purchase_requests` table
  - Add `POST /aftercare/purchase-service` endpoint
  - Add `GET /aftercare/eligibility/{patient_id}` (90-day window)
  - Create admin assignment workflow

- [ ] Integrate Stripe payment
  - Add Stripe SDK
  - Implement checkout endpoint
  - Add subscription management
  - Handle refund processing

- [ ] Dashboard API
  - Create `GET /aftercare/dashboard/{patient_id}` endpoint
  - Aggregate all dashboard data (progress, tasks, milestones)

### Sprint 3 (Task Scheduling & Tracking)

**Goal**: Enable automated task management and reminders

- [ ] Implement task scheduling system
  - Create `aftercare_task_schedule` table
  - Add due date calculation logic
  - Implement `GET /aftercare/tasks/upcoming` endpoint
  - Add overdue detection

- [ ] Medication dose tracking
  - Create `aftercare_medication_doses` table
  - Add `POST /medication/doses/mark-taken` endpoint
  - Calculate weekly adherence percentage
  - Track missed doses

- [ ] Integrate FR-020 Notifications
  - Add task reminder triggers
  - Add escalation notifications
  - Add progress update notifications

### Sprint 4 (Quality & Compliance)

**Goal**: Improve data quality and business rule compliance

- [ ] Add scan quality validation
  - Implement image quality checks
  - Add quality score calculation
  - Provide real-time feedback
  - Store quality metrics

- [ ] Implement escalation automation
  - Add 48-hour overdue trigger
  - Create urgent flag system
  - Add escalation workflow

- [ ] Resource viewing tracking
  - Create `aftercare_resource_views` table
  - Track viewed resources
  - Calculate completion percentage

- [ ] Admin audit logging
  - Integrate `AftercareAuditLog` in all controllers
  - Add change reason field
  - Track all admin edits

---

## 🎯 SUCCESS CRITERIA FOR COMPLETION

### Minimum Viable Product (MVP)

To consider FR-011 "production ready", the following must be completed:

#### Critical Must-Haves (P0)
- ✅ Multiple photo upload working (photo sets)
- ✅ Purchase workflow functional (Screens 6-7)
- ✅ Payment integration complete (Stripe)
- ✅ Progress calculation automated
- ✅ Dashboard API implemented
- ✅ Questionnaire separated from scan upload

#### High Priority (P1)
- ✅ Task scheduling system
- ✅ Medication adherence tracking
- ✅ 90-day add-on window validation
- ✅ Scan quality validation
- ✅ Escalation automation (48-hour trigger)

#### Quality Gates
- 🎯 95%+ API endpoint coverage from FR-011 screens
- 🎯 All critical business rules enforced
- 🎯 All P0 and P1 issues resolved
- 🎯 Integration tests passing for core workflows
- 🎯 Swagger documentation updated

### Target Metrics

After implementation, the system should achieve:

- **Patient Workflow Compliance**: 90%+
- **Provider Workflow Compliance**: 85%+
- **Admin Workflow Compliance**: 95%+
- **API Coverage**: 95%+
- **Business Rules Enforced**: 100% of critical rules

---

## 📝 NOTES FOR PM

### Current Blockers for Mobile App Development

1. **Photo Upload API Incompatible**: Mobile app cannot send multiple photos with current endpoint
2. **No Dashboard Data**: Cannot implement patient dashboard without aggregation API
3. **Purchase Flow Missing**: Cannot build purchase screens (6-7) without backend

### Dependencies Blocking Progress

1. **FR-007 Payment Module**: Must be integrated before purchase workflow works
2. **FR-020 Notifications**: Required for task reminders and alerts
3. **FR-025 Questionnaires**: Needed for dynamic questionnaire rendering

### Technical Debt Items

1. **Scan Photo Storage**: Need to decide on photo storage strategy (S3, local, CDN)
2. **Image Processing**: Need image quality validation library
3. **Payment Provider**: Confirm Stripe as primary payment gateway
4. **Notification Service**: Choose notification delivery mechanism

### Questions for Clarification

1. **Photo Upload Format**: Should photos be uploaded as base64 strings or multipart file uploads?
2. **Payment Timing**: For subscriptions, when is first payment charged? (immediate or 30 days after?)
3. **Quality Threshold**: What specific quality metrics define "acceptable" scan quality?
4. **Escalation Routing**: When task is overdue 48 hours, who receives the escalation notification?
5. **Provider Assignment**: For standalone requests, how does admin choose which provider to assign?

---

## 📞 Contact & Next Steps

**Prepared By**: Development Team
**Review Required By**: Product Manager, Tech Lead
**Target Review Date**: 2026-04-08

### Next Actions

1. **PM Review**: Prioritize issues and confirm roadmap
2. **Tech Lead Review**: Validate technical approach for critical fixes
3. **Sprint Planning**: Allocate issues to upcoming sprints
4. **Dependency Resolution**: Coordinate with FR-007, FR-020 teams
5. **Mobile Sync**: Align with mobile team on API contract changes

---

**Document Version**: 1.0
**Last Updated**: 2026-04-06
**Status**: 🟡 Pending PM Review
