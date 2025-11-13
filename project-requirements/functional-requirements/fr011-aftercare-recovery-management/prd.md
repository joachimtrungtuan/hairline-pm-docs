# Aftercare & Recovery Management Module - Product Requirements Document

**Module**: P-05: Aftercare & Progress Monitoring | PR-04: Aftercare Participation *(elevated to P1 scope for FR-011 delivery)* | A-03: Aftercare Team Management  
**Feature Branch**: `fr011-aftercare-recovery-management`  
**Created**: 2025-10-23  
**Status**: ✅ Verified & Approved  
**Source**: FR-011 from system-prd.md

## Executive Summary

The Aftercare & Recovery Management module provides comprehensive post-procedure support for hair transplant patients through milestone-based tracking, 3D scan monitoring, questionnaire assessments, and multi-tenant communication. The module supports both treatment-linked aftercare (for Hairline platform patients) and standalone aftercare services (for external clinic patients).

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-05)**: Aftercare & Progress Monitoring
- **Provider Platform (PR-04)**: Aftercare Participation (P1 scope for FR-011)
- **Admin Platform (A-03)**: Aftercare Team Management
- **Shared Services (S-XX)**: Notifications & Alerts, Media Storage, Payment (Standalone), Messaging/Communication (if enabled)

### Multi-Tenant Breakdown

**Patient Platform (P-05)**:

- View aftercare dashboard (milestones, tasks, progress)
- Upload 3D scans per schedule; complete questionnaires; track medications
- Receive reminders and urgent alerts; contact aftercare team

**Provider Platform (PR-04)**:

- Review assigned aftercare cases and patient progress
- Configure/activate aftercare plans; customize milestones/medications/instructions
- Manage reschedules, escalations, and communications with aftercare team

**Admin Platform (A-03)**:

- Global oversight; case reassignment; plan overrides; escalations
- Template management (milestones, questionnaires, resources)
- Standalone aftercare request intake and assignment

**Shared Services (S-XX)**:

- Notifications & alerts; media storage for scans/documents
- Payment for standalone activation; secure messaging (if enabled)

### Communication Structure

**In Scope**:

- Patient ↔ Aftercare Team: Structured messaging, questionnaires, and 3D scan submissions
- Provider ↔ Aftercare Team: Case updates and escalations
- Admin ↔ All Parties: Oversight and interventions
- System-generated updates: Milestone reminders, progress updates, urgent flags

**Out of Scope**:

- Direct patient ↔ provider chat (handled by FR-012 backlog)
- Payment flows beyond standalone activation (handled in Payment FR)

### Entry Points

1. **Treatment-Linked Aftercare**: Automatic activation after Hairline platform treatment completion
2. **Standalone Aftercare**: Patient-purchased service for external clinic treatments
3. **Admin-Managed**: Direct assignment by admin team

## Business Workflows

### Workflow 1: Treatment-Linked Aftercare Setup (Primary Flow)

**Actors**: Provider, System, Patient, Aftercare Team

**Trigger**: Provider marks treatment as completed and initiates aftercare setup

**Outcome**: Aftercare plan is configured, activated, and patient/aftercare team are notified

**Main Flow**:

1. **Treatment Completion Trigger**
   - Provider marks treatment as "completed" in system
   - System automatically moves patient status to "Aftercare"
   - System prompts provider to configure aftercare plan

2. **Aftercare Template Selection**
   - Provider views available milestone templates (admin-created)
   - Provider selects appropriate template (e.g., "Standard FUE Aftercare - 12 months")
   - System displays template details: milestones, scan frequency, questionnaire schedule, educational resources, activity restrictions

3. **Customization & Medication Setup**
   - Provider adds patient-specific instructions
   - Provider specifies post-op medications:
     - Medication name, dosage, frequency, special instructions
   - Provider can modify milestone durations if needed
   - Provider confirms aftercare plan

4. **Plan Generation & Activation**
   - System generates complete aftercare plan with milestones
   - System creates patient aftercare dashboard
   - System sends activation notification to patient
   - Aftercare team receives case assignment notification

**Alternative Flows**:

- **A1**: Provider provides only paperwork/instructions
  - Provider marks "Paperwork only - no aftercare service"
  - Provider uploads aftercare instructions document
  - Patient receives instructions but no active monitoring
  - Patient status moves to "Completed" after instruction delivery

- **A2**: Provider requests Hairline aftercare service
  - Provider marks "Assign to Hairline aftercare team"
  - Admin receives notification for aftercare assignment
  - Hairline aftercare team takes over patient monitoring
  - Provider receives compensation for aftercare participation

### Workflow 2: Standalone Aftercare Service (Secondary Flow)

**Actors**: Patient, Admin, Assigned Provider, Aftercare Team

**Trigger**: Patient requests standalone aftercare service and completes payment

**Outcome**: Aftercare plan is assigned, configured, and activated for the patient

**Main Flow**:

1. **Service Request & Package Selection**
   - Patient navigates to "Request Aftercare Service" in app (Screen 6)
   - Patient selects service type (standalone for external clinic patients)
   - Patient fills out treatment details form (treatment date, type, clinic)
   - Patient browses available aftercare templates marked "Available for Purchase"
   - Patient selects desired template and views pricing breakdown
   - Patient chooses payment method (fixed or subscription, if both available)
   - Patient proceeds to payment screen

2. **Payment & Checkout**
   - Patient reviews order summary with template details, fees, and total (Screen 7)
   - Patient selects payment method (credit card, PayPal, etc.)
   - Patient enters payment and billing information
   - Patient accepts terms and conditions
   - Patient submits payment
   - System processes payment via FR-007 Payment Processing module
   - On success: Payment confirmation displayed, email sent, request moves to "Pending Assignment"
   - On failure: Error message displayed, retry option provided

3. **Admin Review & Assignment**
   - Request appears in admin dashboard as "Pending Assignment" (Screen 15)
   - Admin reviews patient information and treatment details
   - Admin assigns suitable provider to oversee case
   - System notifies assigned provider

4. **Provider Activation**
   - Assigned provider reviews patient case
   - Provider selects appropriate aftercare template (same as purchased template or alternative if needed)
   - Provider customizes plan based on patient's specific situation
   - Provider activates aftercare plan

5. **Patient Onboarding**
   - Patient receives activation notification
   - Patient gains access to aftercare dashboard (Screen 1)
   - Aftercare team begins monitoring

**Alternative Flows**:

- **B1**: Payment fails
  - Patient receives payment failure notification
  - Patient can retry payment with different method
  - Request expires after 48 hours without successful payment

- **B2**: Admin rejects request
  - Admin marks request as "Not suitable for aftercare"
  - Patient receives rejection notification with reason
  - Refund processed automatically

- **B3**: No suitable provider available
  - Admin marks as "Awaiting provider availability"
  - Patient notified of delay
  - Admin manually assigns when provider becomes available

### Workflow 2b: Post-Treatment Aftercare Add-On (Secondary Flow)

**Actors**: Patient (Hairline-treated), Admin, Assigned Provider (original or new), Aftercare Team

**Trigger**: Hairline-treated patient requests aftercare service after treatment completion (within 90 days)

**Outcome**: Aftercare plan is configured, activated, and patient receives ongoing monitoring

**Main Flow**:

1. **Add-On Service Request**
   - Patient navigates to "Add Aftercare Service" in patient dashboard (Screen 6)
   - System verifies patient has completed Hairline treatment within 90 days
   - Patient selects service type (post-treatment add-on)
   - System auto-populates treatment information from patient's treatment history
   - Patient browses available aftercare templates (filtered by treatment type compatibility)
   - Patient selects desired template and payment method
   - Patient proceeds to payment

2. **Payment & Checkout**
   - Patient reviews order summary with template details (Screen 7)
   - Patient completes payment via checkout screen
   - System processes payment via FR-007 Payment Processing module
   - On success: Payment confirmed, request moves to automatic assignment
   - On failure: Error message, retry option

3. **Automatic Assignment**
   - Payment confirmation triggers automatic assignment
   - System assigns to original treatment provider (if provider participates in aftercare)
   - If provider doesn't participate, system assigns to Hairline aftercare team
   - Assigned provider receives notification

4. **Provider Activation**
   - Provider reviews patient's treatment history (pre-populated from treatment records)
   - Provider selects appropriate aftercare template (same as purchased or alternative)
   - Provider customizes plan based on patient's treatment and package selection
   - Provider activates aftercare plan

5. **Patient Onboarding**
   - Patient receives activation notification
   - Patient gains access to aftercare dashboard (Screen 1)
   - Aftercare team begins monitoring

**Alternative Flows**:

- **B1a**: Original provider declines aftercare participation
  - System automatically assigns to Hairline aftercare team
  - Patient notified of provider assignment
  - Aftercare team provider configures and activates plan

- **B1b**: Payment fails
  - Patient receives payment failure notification
  - Patient can retry payment with different method
  - Request expires after 48 hours without successful payment

### Workflow 3: Patient Aftercare Activities (Ongoing Flow)

**Actors**: Patient, System, Aftercare Team

**Trigger**: Scheduled milestone/task becomes due or patient initiates activity

**Outcome**: Task completed, progress updated, and alerts/escalations generated when needed

**Main Flow**:

1. **Milestone-Based Tasks**
   - System sends notification for upcoming tasks (3D scan, questionnaire)
   - Patient completes required activities
   - System tracks completion and progress

2. **3D Scan Upload**
   - Patient receives scan reminder notification
   - Patient captures 3D head scan using mobile app
   - System validates scan quality and provides feedback
   - Scan stored and made available to aftercare team

3. **Questionnaire Completion**
   - Patient receives questionnaire notification
   - Patient completes milestone-specific questionnaire
   - System processes responses and flags concerning answers
   - Aftercare team reviews responses

4. **Progress Tracking**
   - System automatically calculates overall recovery progress percentage based on:
     - Milestone completion (timeframe-based)
     - Task completion (3D scans, questionnaires)
     - Compliance rates (medication adherence, activity restrictions)
   - Patient views progress dashboard with real-time updates
   - System shows next upcoming tasks with countdown timers

**Alternative Flows**:

- **C1**: Patient misses scheduled task
  - System sends reminder notification
  - After 24 hours, system flags as "Overdue"
  - Aftercare team contacts patient

- **C2**: Concerning symptoms reported
  - System flags case as "Urgent"
  - Aftercare team immediately contacts patient
  - Escalation workflow triggered

### Workflow 4: Admin Aftercare Management (Management Flow)

**Actors**: Admin, Aftercare Team, Providers

**Trigger**: Admin opens case for oversight or receives event requiring intervention

**Outcome**: Case updated (reassignment/plan edits/escalations) with full audit and re-notifications as needed

**Main Flow**:

1. **Dashboard Overview**
   - Admin views aftercare dashboard with key metrics
   - Admin monitors active cases, completion rates, flagged cases
   - Admin reviews provider performance

2. **Case Management**
   - Admin can reassign cases between providers
   - Admin can modify aftercare plans for complex cases
   - Admin can escalate urgent cases to medical supervisor
   - **Admin Editability**: Admin can edit ALL aftercare data including:
     - Patient aftercare plans and milestones
     - Provider assignments and customizations
     - Medication schedules and instructions
     - Questionnaire responses and flags
     - 3D scan data and progress tracking
     - Communication logs and escalations

3. **Template Management**
   - Admin creates and modifies milestone templates
   - Admin configures questionnaire types and frequencies
   - Admin manages educational resources
   - **Admin Editability**: Admin can edit all template components:
     - Milestone durations and descriptions
     - 3D scan schedules and frequencies
     - Questionnaire types and question content
     - Educational resources and activity restrictions

**Alternative Flows**:

- **D1**: Provider withdraws from aftercare
  - Provider notifies admin of inability/unwillingness to continue aftercare for a patient
  - Admin receives notification and reviews the case
  - Admin can either:
    - Reassign the case to another suitable provider
    - Assign the case to the Hairline internal aftercare team
    - Mark the aftercare as cancelled (with reason)
  - All changes are logged, and the patient is notified of the new arrangement or cancellation

- **D2**: Provider performance issues
  - Admin identifies underperforming providers
  - Admin reassigns cases to better-performing providers
  - Admin provides feedback to provider

- **D3**: System-wide aftercare issues
  - Admin identifies patterns in patient complaints
  - Admin updates templates or processes
  - Admin communicates changes to all providers

## Screen Specifications

### Patient Platform Screens

#### Screen 1: Aftercare Dashboard

**Purpose**: Central hub for patient aftercare activities

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Overall Progress | derived | Yes | Percentage of completed tasks for current plan | 0–100%; auto-calculated |
| Current Milestone | text | Yes | Name and phase of current milestone | Must exist in plan |
| Days Remaining | number | No | Days left in current milestone | Non-negative integer |
| Next Task | text/datetime | No | Next upcoming task with countdown | Shows due date/time |
| Last 3D Scan | datetime/status | No | Timestamp and status of last scan | Valid status enum |
| Last Questionnaire | datetime | No | Timestamp of last questionnaire completion | ISO 8601 |
| Medication Adherence | percent | No | Adherence percentage for current period | 0–100% |
| Upcoming Tasks | list | No | Next 7 days tasks | Items must exist in schedule |
| Upload 3D Scan | action | Cond. | Action to capture/upload scan | Enabled if due |
| Complete Questionnaire | action | Cond. | Action to complete due questionnaire | Enabled if due |
| View Instructions | action | No | Open instructions content | Always available |
| Contact Support | action | No | Contact aftercare support | Always available |

**Business Rules**:

- Progress percentage = (completed tasks / total tasks) * 100
- Tasks include: 3D scans, questionnaires, medication adherence
- Overdue tasks highlighted in red
- Completed tasks shown in green

**Notes**:

- Dashboard serves as the primary patient interface for aftercare engagement
- Real-time progress updates when tasks are completed
- Countdown timers for upcoming tasks create urgency and improve compliance
- Quick action buttons provide easy access to most common patient activities
- Mobile-first design optimized for smartphone screens

#### Screen 2: 3D Scan Upload

**Purpose**: Patient uploads milestone 3D head scans

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Milestone Name | text | Yes | Current milestone name (read-only) | Display only |
| Scan Due Date | datetime | Yes | Due date for this scan (read-only) | ISO 8601 format |
| Days Overdue | number | No | Days past due date (if applicable) | Non-negative integer |
| Scan Guidance | text | No | Instructions for proper scan capture | Display only |
| Camera Viewfinder | component | Yes | Live camera preview for 3D scan | ARKit/ARCore required |
| Quality Indicator | status | Yes | Real-time scan quality feedback | Valid quality enum |
| Capture Scan | action | Yes | Button to capture 3D scan | Enabled when quality threshold met |
| Retake | action | Cond. | Button to retake if quality poor | Enabled when quality below threshold |
| Upload Progress | progress | No | Upload progress bar (0-100%) | 0-100% |
| Upload Status | message | No | Success/error message after upload | Valid status enum |
| View Previous Scans | link | No | Link to view historical scans | Always available |

**Business Rules**:

- Scan must meet minimum quality threshold
- Maximum file size: 50MB
- Multiple scans within a milestone are supported per the configured scan schedule (e.g., every X days for Y repetitions); one upload is allowed per scheduled instance
- Previous scans remain accessible for comparison

**Notes**:

- Use ARKit (iOS) or ARCore (Android) for 3D head scanning
- Quality validation should provide real-time feedback during capture
- Implement resumable upload for unreliable network connections
- Store scans in secure cloud storage with patient ID watermarking

#### Screen 3: Questionnaire Completion

**Purpose**: Patient completes milestone-specific questionnaires

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Milestone Name | text | Yes | Current milestone and phase | Display only |
| Questionnaire Type | text | Yes | Type (Pain Assessment, Sleep Quality, etc.) | Must exist in FR-025 catalog |
| Due Date | datetime | Yes | Questionnaire due date | ISO 8601 format |
| Completion Status | status | Yes | Completed/Pending/Overdue | Valid status enum |
| Pain Scale | number | Cond. | Pain level 1-10 (if Pain Assessment type) | Integer 1-10 |
| Pain Description | text | No | Text description of pain | Max 500 chars |
| Hours Slept | number | Cond. | Hours slept (if Sleep Quality type) | Integer 0-24 |
| Sleep Quality Rating | number | Cond. | Quality rating 1-5 (if Sleep Quality type) | Integer 1-5 |
| Sleep Disruptions | checkbox[] | Cond. | List of disruptions (if Sleep Quality type) | Valid disruption types |
| Medication Adherence | boolean | Cond. | Yes/no (if Compliance Check type) | Boolean |
| Activity Restrictions | boolean | Cond. | Yes/no (if Compliance Check type) | Boolean |
| Washing Instructions | boolean | Cond. | Yes/no (if Compliance Check type) | Boolean |
| Swelling | boolean | Cond. | Yes/no (if Symptom Check type) | Boolean |
| Redness | boolean | Cond. | Yes/no (if Symptom Check type) | Boolean |
| Bleeding | boolean | Cond. | Yes/no (if Symptom Check type) | Boolean |
| Infection Signs | boolean | Cond. | Yes/no (if Symptom Check type) | Boolean |
| Save Draft | action | No | Save progress without submitting | Always available |
| Submit | action | Yes | Submit completed questionnaire | Enabled when all required fields complete |
| Warning Message | alert | No | Warning for concerning responses | Shown when pain >7 or infection signs detected |

**Business Rules**:

- All required fields must be completed
- Concerning responses (pain >7, infection signs) trigger urgent flag
- Drafts saved automatically every 30 seconds
- One submission per questionnaire allowed

**Notes**:

- Questionnaire structure and questions managed in FR-025 (Medical Questionnaire Management)
- Dynamic form rendering based on questionnaire type from template
- Auto-save draft functionality to prevent data loss
- Real-time validation for concerning responses (triggers urgent flag immediately)
- Mobile-optimized form layout for easy completion on small screens

#### Screen 4: Medication Schedule

**Purpose**: Patient views and tracks medication adherence

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Medication Name | text | Yes | Name of medication | Must exist in medication catalog |
| Dosage | text | Yes | Dosage amount and unit | Valid dosage format |
| Frequency | text | Yes | Frequency (e.g., "2x daily", "Every 8 hours") | Valid frequency format |
| Special Instructions | text | No | Additional instructions from provider | Max 500 chars |
| Start Date | date | Yes | Medication start date | ISO 8601 format |
| End Date | date | Yes | Medication end date | Must be after start date |
| Today's Doses | list | Yes | Upcoming doses for today with times | Sorted by time |
| Dose Time | time | Yes | Scheduled time for each dose | HH:MM format |
| Mark as Taken | action | Yes | Button to mark dose as taken | Enabled when dose time reached |
| Missed Dose Indicator | status | No | Visual indicator for missed doses | Shown if dose not taken within 2 hours |
| Weekly Adherence | percent | Yes | Percentage of doses taken this week | 0-100%; auto-calculated |
| Missed Doses Count | number | Yes | Total missed doses count | Non-negative integer |
| View History | link | No | Link to view full adherence history | Always available |

**Business Rules**:

- Medications prescribed by provider during aftercare setup
- Adherence calculated as (taken doses / total doses) * 100
- Missed doses trigger reminder notifications
- History available for entire aftercare period

**Notes**:

- Medications defined during aftercare plan setup (Screen 8)
- Push notifications for upcoming doses (configurable by patient)
- History view shows complete timeline of all medications and adherence
- Visual indicators (colors/icons) for easy recognition of adherence status
- Support for multiple medications with overlapping schedules

#### Screen 5: Educational Resources

**Purpose**: Patient accesses milestone-specific educational content

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Resource Category | text | Yes | Category (Videos, Guides, FAQs, Help) | Valid category enum |
| Resource Title | text | Yes | Title of educational resource | Max 200 chars |
| Resource Description | text | No | Description of resource content | Max 1000 chars |
| Resource Type | text | Yes | Type (video, PDF, webpage, etc.) | Valid resource type enum |
| Resource URL | url | Yes | URL or file path to resource | Valid URL or file path |
| Duration | time | Cond. | Duration in minutes (for videos) | Valid time format |
| File Size | size | Cond. | File size for downloadable resources | Display only |
| Mark as Viewed | checkbox | No | Checkbox to mark resource as viewed | Boolean |
| View/Download | action | Yes | Button to view or download resource | Always available |
| Resources Viewed Count | number | Yes | Count of viewed resources | Non-negative integer |
| Total Resources | number | Yes | Total resources in current milestone | Non-negative integer |
| Completion Percentage | percent | Yes | Percentage of resources viewed | 0-100%; auto-calculated |
| Mark All as Viewed | action | No | Button to mark all resources as viewed | Enabled when resources available |

**Business Rules**:

- Resources specific to current milestone
- Viewing progress tracked for compliance
- Resources remain accessible throughout aftercare
- New resources added by admin appear automatically

**Notes**:

- Resources managed in Screen 16 (Milestone Template Management) by admin
- Support for various media types: videos (streaming), PDFs (download), web pages (in-app browser)
- Progress tracking helps ensure patients review critical educational content
- Resources organized by category for easy navigation
- Offline viewing capability for downloaded resources

#### Screen 6: Aftercare Service Purchase

**Purpose**: Patient purchases aftercare service (post-treatment add-on or standalone)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Service Type | radio | Yes | Post-Treatment Add-On or Standalone Service | Enum: "post_treatment", "standalone" |
| Treatment Information | component | Cond. | Treatment details (if post-treatment add-on) | Auto-populated for post_treatment type |
| External Treatment Details | form | Cond. | Treatment info form (if standalone) | Required for standalone type |
| Treatment Date | date | Cond. | Date treatment performed | ISO 8601; required for standalone |
| Treatment Type | select | Cond. | Type of treatment received | Valid treatment type enum; required for standalone |
| Treating Clinic | text | Cond. | Name of external clinic | Max 200 chars; required for standalone |
| Upload Treatment Documentation | file | No | Optional treatment documentation | Max 10MB; PDF/JPG/PNG |
| Available Aftercare Services | list | Yes | List of purchasable aftercare templates | Filtered by treatment type compatibility |
| Service Name | text | Yes | Template name (e.g., "Standard 6-Month FUE Aftercare") | Display only |
| Service Description | text | Yes | Template description with features | Display only |
| Duration | text | Yes | Service duration (from template) | Display only |
| Milestones Included | list | Yes | Milestone summary | Display only |
| Features Included | list | Yes | Features (3D scans, questionnaires, etc.) | Display only |
| Pricing Options | component | Yes | Available pricing for this template | Based on template configuration |
| Payment Method | radio | Cond. | Fixed Price or Monthly Subscription | Based on template's pricing model |
| Price (Fixed) | currency | Cond. | One-time payment amount | Shown if Fixed or Both |
| Price (Monthly) | currency | Cond. | Monthly subscription amount | Shown if Subscription or Both |
| Total Amount | currency | Yes | Total amount for selected payment method | Auto-calculated |
| Currency | text | Yes | Patient's currency (auto-detected) | Based on location |
| Selected Service | radio | Yes | User selection of template | Required before checkout |
| Selected Payment Method | radio | Cond. | If template offers both pricing models | Required if Both available |
| Current Concerns | textarea | No | Patient's current concerns or symptoms | Max 2000 chars |
| Upload Photos | file[] | No | Optional photos of current condition | Max 5 files; 10MB each; JPG/PNG |
| Proceed to Payment | action | Yes | Button to proceed to checkout | Enabled when service selected |

**Business Rules**:

- Only templates marked "Available for Purchase" are shown
- Templates filtered by treatment type compatibility (FUE templates for FUE patients, etc.)
- Pricing shown in patient's local currency (based on location detection)
- If template offers both Fixed and Subscription, patient chooses preferred payment method
- Service name uses template name for consistency across provider and patient views
- Post-treatment add-on only available within 90 days of Hairline treatment completion
- Treatment documentation optional but helps provider customize plan

**Notes**:

- Service offerings are directly pulled from aftercare templates (Screen 16)
- Each template defines its own pricing, features, and duration
- Visual presentation similar to treatment package selection for consistency
- Pricing transparency with clear breakdown of what's included
- Service type auto-detected based on patient's treatment history

#### Screen 7: Aftercare Payment & Checkout

**Purpose**: Patient completes payment for aftercare service

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Order Summary | component | Yes | Selected aftercare service details | Display only |
| Service Name | text | Yes | Selected template name | Display only |
| Duration | text | Yes | Service duration | Display only |
| Payment Method Selected | text | Yes | Fixed or Monthly Subscription | Display only |
| Subtotal | currency | Yes | Base service price (from template) | Display only |
| Platform Fee | currency | Yes | Platform service fee | Display only; 15-25% |
| Tax | currency | Yes | Applicable tax | Display only; location-based |
| Total Amount | currency | Yes | Final amount to pay | Display only |
| Monthly Payment Details | component | Cond. | Breakdown of subscription payments | Shown if subscription selected |
| Monthly Amount | currency | Yes | Amount charged per month | Display only |
| Number of Months | number | Yes | Total subscription duration | Display only |
| Total Subscription Amount | currency | Yes | Monthly amount × number of months | Display only |
| Payment Method Selection | radio | Yes | Credit/Debit Card, PayPal, etc. | Valid payment method enum |
| Card Number | text | Cond. | Credit/debit card number | Valid card format; required if card payment |
| Expiry Date | text | Cond. | Card expiry date | MM/YY format; required if card payment |
| CVV | text | Cond. | Card security code | 3-4 digits; required if card payment |
| Cardholder Name | text | Cond. | Name on card | Max 200 chars; required if card payment |
| Billing Address | component | Yes | Billing address details | Required for all payment methods |
| Street Address | text | Yes | Street address | Max 500 chars |
| City | text | Yes | City | Max 100 chars |
| State/Province | text | Yes | State/province | Max 100 chars |
| Postal Code | text | Yes | Postal/ZIP code | Valid postal format |
| Country | select | Yes | Country | Valid country enum |
| Terms & Conditions | checkbox | Yes | Agreement to terms | Boolean; must be checked |
| Privacy Policy | checkbox | Yes | Agreement to privacy policy | Boolean; must be checked |
| Payment Processing | status | No | Payment processing status | Display during payment |
| Complete Payment | action | Yes | Button to submit payment | Enabled when all fields valid |

**Business Rules**:

- Payment integration with FR-007 (Payment Processing module)
- Support for multiple payment methods (credit/debit cards, PayPal, local payment methods)
- Secure payment processing with PCI compliance
- Payment confirmation triggers aftercare request workflow (Workflow 2 or 2b)
- Failed payments allow retry with different payment method
- Refunds processed automatically if request is rejected by admin
- Subscription payments charged automatically on monthly basis
- First subscription payment charged immediately; subsequent payments on monthly anniversary

**Notes**:

- Integrate with Stripe payment gateway (per dependencies, line 1232-1236)
- Order summary clearly shows all fees and charges with transparent breakdown
- Payment method selection supports region-specific payment options
- Secure payment form with SSL encryption and PCI compliance
- Payment confirmation email sent immediately after successful payment
- Payment status tracked and visible in patient dashboard
- For subscriptions, clear communication of recurring payment schedule
- Subscription management interface for patients to view/cancel subscriptions

### Provider Platform Screens

#### Screen 8: Aftercare Cases List

**Purpose**: Provider views all patients in aftercare (similar to existing "In Progress" list)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient ID | column | Yes | Unique identifier (e.g., HPID2509-0001) | Searchable; sortable |
| Patient Name | column | Yes | Avatar + full name + email | PII per role; sortable |
| Phone Number | column | No | Contact number | E.164 format |
| Age | column | No | Patient age | Integer 18–100 |
| Problem | column | No | Treatment area (Hair/Both/Beard) | Enum |
| Treatment & Package | column | Yes | Treatment + package | Read-only |
| Aftercare Start Date | column | Yes | Start date | ISO 8601; sortable |
| Current Milestone | column | Yes | Phase name | Must exist in plan |
| Progress | column | Yes | Visual progress (e.g., 3/5 days) | Derived; non-negative |
| Med Alerts | column | Yes | Critical/Standard/None | Enum with color coding |
| Last Activity | column | No | Time since last interaction | Relative format |
| Action | column | Yes | View/Edit/Message/Escalate | RBAC enforced |
| Search | control | No | Search aftercare cases | Debounced input |
| Filters | control | No | Provider/Milestone/Status/Date range | Valid enums/ranges |
| Pagination | control | No | Page controls and size | Standard UX pattern |

**Business Rules**:

- Only shows patients assigned to this provider
- Overdue cases shown with amber indicators
- Patient names are fully visible as aftercare occurs post-payment confirmation
- Progress calculated automatically by system
- All data editable by admin (admin override capability)

**Notes**:

- Similar table structure to existing "In Progress" treatment list for consistency
- Color-coded medication alerts (red=critical, yellow=standard, green=none) provide quick visual status
- Filters allow providers to focus on specific patient groups (by milestone, status, date range)
- Sortable columns help providers prioritize cases (e.g., sort by Last Activity to find inactive patients)
- Action menu provides quick access to common provider tasks without navigating away

#### Screen 9: Patient Aftercare Details

**Purpose**: Provider views comprehensive patient aftercare progress with full historical context

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient ID | text | Yes | Unique patient identifier | Display only |
| Treatment Details | text | Cond. | Treatment info (if Hairline-treated patient) | Display only; N/A for standalone |
| Aftercare Start Date | date | Yes | When aftercare began | ISO 8601 format |
| Aftercare Duration | text | Yes | Planned duration (e.g., "12 months") | Display only |
| Assigned Template | text | Yes | Aftercare template name | Display only |
| Custom Instructions | text | No | Provider's patient-specific instructions | Max 2000 chars; editable |
| Current Milestone | text | Yes | Current milestone name and phase | Must exist in plan |
| Overall Progress | percent | Yes | Completion percentage (auto-calculated) | 0-100% |
| Milestone Timeline | component | Yes | Visual timeline of all milestones | Display only |
| Upcoming Tasks | list | Yes | List of next due tasks | Sorted by due date |
| 3D Scan History | list | Yes | All uploaded scans with dates and quality | Chronological order |
| Scan Upload Date | datetime | Yes | Date scan was uploaded | ISO 8601 format |
| Scan Quality Score | number | Yes | Quality score (0-100) | Integer 0-100 |
| Questionnaire Responses | list | Yes | All questionnaire completions | Chronological order |
| Response Date | datetime | Yes | Date questionnaire was submitted | ISO 8601 format |
| Questionnaire Type | text | Yes | Type of questionnaire completed | Valid questionnaire type |
| Medication Adherence History | list | Yes | Historical adherence data | Chronological order |
| Adherence Period | date range | Yes | Date range for adherence period | Valid date range |
| Adherence Percentage | percent | Yes | Percentage for that period | 0-100% |
| Communication Log | list | Yes | All communications with aftercare team | Chronological order |
| Message Date | datetime | Yes | Date/time of message | ISO 8601 format |
| Message Type | text | Yes | Type (message, escalation, alert) | Valid message type enum |
| Adjust Plan | action | No | Button to modify aftercare plan | Enabled for assigned patients |
| Request Additional Scan | action | No | Button to request extra scan | Always available |
| Contact Aftercare Team | action | No | Button to send message | Always available |
| Escalate Case | action | No | Button to escalate urgent case | Always available |

**Business Rules**:

- **Data Persistence**: Screen displays all historical data from patient's entire journey (inquiry → treatment → aftercare) without removing older data, providing complete context
- **Dual Case Handling**:
  - **Hairline-treated patients**: Shows complete lifecycle data including pre-treatment inquiry, quote, treatment details, and aftercare
  - **Standalone aftercare patients**: Shows only aftercare-specific data with initial intake information provided during standalone request
- Full patient details visible as aftercare occurs post-payment confirmation
- All activities logged with timestamps
- Provider can modify plan only for their assigned patients
- Escalation creates audit trail

**Notes**:

- Comprehensive view consolidates all patient aftercare information in one place
- Chronological activity feed provides full context for provider decision-making
- Historical data persistence ensures complete patient journey visibility
- Visual timeline helps providers quickly identify where patient is in recovery process
- Quick action buttons enable providers to make interventions without leaving the screen
- Escalation workflow creates immediate audit trail for urgent cases

#### Screen 10: Aftercare Setup (Multi-Step Process)

**Purpose**: Provider sets up aftercare plan after treatment completion

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| **Step 1: Template Selection** | | | | |
| Available Templates | list | Yes | List of admin-created templates | Must have at least one template |
| Template Name | text | Yes | Selected template name | Must exist in template catalog |
| Template Description | text | Yes | Template description | Display only |
| Treatment Type | text | Yes | Treatment type compatibility | Valid treatment type enum |
| Duration | text | Yes | Duration (e.g., "12 months") | Display only |
| Milestone Count | number | Yes | Number of milestones in template | Display only |
| Template Preview | component | No | Preview of template details | Display only |
| Select Template | action | Yes | Button to select template | Enabled when template selected |
| **Step 2: Milestone Customization** | | | | |
| Milestone List | list | Yes | All milestones from selected template | Must have at least one milestone |
| Milestone Name | text | Yes | Name of milestone | Max 200 chars |
| Milestone Duration | number | Yes | Duration in days | Positive integer; editable |
| 3D Scan Frequency | text | Yes | Frequency of scans (e.g., "Weekly") | Valid frequency enum; editable |
| Questionnaire Types | list | Yes | Types of questionnaires per milestone | Must exist in FR-025 catalog |
| Questionnaire Frequency | text | Yes | Frequency of questionnaires | Valid frequency enum; editable |
| Educational Resources | list | Yes | Resources assigned to milestone | May be empty |
| Activity Restrictions | text | No | Restrictions for this milestone | Max 500 chars; editable |
| Modify Duration | action | No | Button to modify milestone duration | Always available |
| Add Questionnaire | action | No | Button to add questionnaire | Always available |
| Remove Questionnaire | action | No | Button to remove questionnaire | Enabled when questionnaires exist |
| Custom Instructions | text | No | Instructions specific to this milestone | Max 1000 chars |
| Override Restrictions | action | No | Button to override activity restrictions | Always available |
| **Step 3: Medication Setup** | | | | |
| Medication Name | select | Yes | Medication from dropdown database | Must exist in medication catalog |
| Dosage | text | Yes | Dosage amount and unit | Valid dosage format |
| Frequency | text | Yes | Frequency (e.g., "2x daily") | Valid frequency format |
| Start Date | date | Yes | Medication start date | ISO 8601 format; must be today or future |
| End Date | date | Yes | Medication end date | ISO 8601 format; must be after start date |
| Special Instructions | text | No | Additional instructions | Max 500 chars |
| Add Medication | action | Yes | Button to add medication to list | Enabled when all fields complete |
| Medication List | list | Yes | List of all added medications | May be empty |
| Medication Timeline | component | Yes | Visual timeline of all medications | Display only |
| **Step 4: Custom Instructions** | | | | |
| General Instructions | textarea | No | Free-text area for provider notes | Max 2000 chars |
| Milestone Instructions | textarea[] | No | Instructions per milestone | Max 1000 chars per milestone |
| Emergency Contact | text | No | Provider contact information | Max 200 chars |
| Special Considerations | textarea | No | Patient-specific notes | Max 1000 chars |
| **Step 5: Review and Confirm** | | | | |
| Plan Summary | component | Yes | Complete aftercare plan overview | Display only |
| Patient Information | component | Yes | Confirmation of patient details | Display only |
| Provider Information | component | Yes | Provider contact details | Display only |
| Activate Plan | action | Yes | Button to activate aftercare plan | Enabled when all steps complete |

**Business Rules**:

- All steps must be completed before activation
- Provider can go back to previous steps
- System validates all required fields
- Admin can edit any step after activation
- Patient receives notification upon activation

**Notes**:

- Multi-step wizard guides providers through setup process systematically
- Progress indicator shows current step and completion status
- Template selection reduces setup time by providing pre-configured plans
- Customization options allow providers to tailor plans to individual patient needs
- Review step allows providers to verify all settings before activation
- Medication management interface supports multiple medications with overlapping schedules
- Visual timeline helps providers understand medication schedule at a glance

#### Screen 11: Aftercare Plan Edit

**Purpose**: Provider or Admin modifies existing aftercare plan

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Selected Template | text | Yes | Current template name | Display only |
| Milestone Structure | component | Yes | Visual structure with progress indicators | Display only |
| Medication Schedule | component | Yes | Visual timeline of medications | Display only |
| Custom Instructions | textarea | No | Current custom instructions | Max 2000 chars; editable |
| Modify Medication Schedule | action | Cond. | Button to modify medications (Provider) | Enabled for providers |
| Update Custom Instructions | action | Cond. | Button to update instructions (Provider) | Enabled for providers |
| Add Milestone Notes | action | Cond. | Button to add milestone-specific notes (Provider) | Enabled for providers |
| Request Duration Change | action | Cond. | Button to request milestone duration change (Provider) | Enabled for providers |
| Change Milestone Structure | action | Cond. | Button to modify milestones (Admin only) | Enabled for admins |
| Modify Template Assignment | action | Cond. | Button to change template (Admin only) | Enabled for admins |
| Override Settings | action | Cond. | Button to override any settings (Admin only) | Enabled for admins |
| Reassign Provider | action | Cond. | Button to reassign case (Admin only) | Enabled for admins |
| Change Reason | textarea | Yes | Required reason for changes | Max 500 chars; required |
| Change Timestamp | datetime | Yes | When change was made | Auto-generated |
| Changed By | text | Yes | User who made the change | Auto-populated |
| Approval Status | status | Yes | Status (Pending/Approved/Rejected) | Valid status enum |
| Change History | list | Yes | Historical list of all changes | Chronological order |

**Business Rules**:

- Provider changes logged and tracked
- Admin changes override provider settings
- Major changes require admin approval
- All changes logged with reason and timestamp
- Patient notified of approved changes
- Change history maintained for audit trail

**Notes**:

- Edit capabilities differ based on user role (Provider vs Admin)
- Admin has full override capabilities on all plan aspects
- Change tracking ensures full audit trail for compliance
- Change reason required for all modifications to document rationale
- Approval workflow for major changes ensures quality control
- Patient notifications keep them informed of plan modifications

#### Screen 12: Aftercare Progress Tracking (Provider View)

**Purpose**: Provider monitors ongoing aftercare progress for assigned patients

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient Name | text | Yes | Full patient name | Display only |
| Current Milestone | text | Yes | Current milestone name and phase | Display only |
| Overall Progress | percent | Yes | Completion percentage (auto-calculated) | 0-100% |
| Days Remaining | number | Yes | Days left in current milestone | Non-negative integer |
| Next Upcoming Tasks | list | Yes | List of next due tasks | Sorted by due date |
| Milestone Timeline | component | Yes | Visual timeline of all milestones | Display only |
| Completed Milestones | indicator | Yes | Green indicators for completed | Display only |
| Current Milestone Indicator | indicator | Yes | Blue indicator for current | Display only |
| Upcoming Milestones | indicator | Yes | Gray indicators for upcoming | Display only |
| Overdue Tasks Indicator | indicator | Yes | Red indicators for overdue | Display only |
| 3D Scan Status | status | Yes | Completed/Pending/Overdue with dates | Valid status enum |
| Scan Due Date | datetime | Yes | Due date for scan | ISO 8601 format |
| Questionnaire Status | status | Yes | Completed/Pending/Overdue with dates | Valid status enum |
| Questionnaire Due Date | datetime | Yes | Due date for questionnaire | ISO 8601 format |
| Medication Adherence | percent | Yes | Adherence percentage | 0-100% |
| Missed Doses | number | Yes | Count of missed doses | Non-negative integer |
| Activity Compliance | percent | Yes | Compliance with activity restrictions | 0-100% |
| Recent Scan Uploads | list | Yes | Recent 3D scan uploads | Chronological order |
| Questionnaire Completions | list | Yes | Recent questionnaire submissions | Chronological order |
| Medication Updates | list | Yes | Recent adherence updates | Chronological order |
| Communication Interactions | list | Yes | Recent messages/interactions | Chronological order |
| Request Additional Scan | action | No | Button to request extra scan | Always available |
| Send Message to Patient | action | No | Button to send message | Always available |
| Schedule Consultation | action | No | Button to schedule consultation | Always available |
| Escalate Case | action | No | Button to escalate urgent case | Always available |

**Business Rules**:

- Progress calculated automatically by system
- Provider can only view assigned patients
- Real-time updates when patient completes tasks
- Overdue tasks highlighted prominently
- All actions logged for audit trail

**Notes**:

- Focused view for providers to monitor patient progress at a glance
- Visual timeline provides quick understanding of patient's recovery journey
- Color-coded indicators help providers quickly identify status and issues
- Activity feed shows recent patient engagement for quick assessment
- Quick action buttons enable providers to take immediate interventions
- Real-time updates ensure providers have current information for decision-making

### Admin Platform Screens

#### Screen 13: Aftercare Cases List

**Purpose**: Admin views all aftercare cases (similar to existing provider lists)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Case ID | column | Yes | Unique identifier (e.g., AC2509-0001) | Searchable; sortable |
| Patient Name | column | Yes | Avatar + full name + email | PII admin-only |
| Phone Number | column | No | Contact number | E.164 format |
| Age | column | No | Patient age | Integer 18–100 |
| Problem | column | No | Treatment area | Enum |
| Treatment & Package | column | Yes | Treatment + package | Read-only |
| Provider | column | Yes | Assigned provider name | Must exist |
| Aftercare Type | column | Yes | Treatment-linked or Standalone | Enum |
| Start Date | column | Yes | Aftercare start date | ISO 8601; sortable |
| Current Milestone | column | Yes | Current phase | Must exist in plan |
| Progress | column | Yes | Visual progress bar | Derived; non-negative |
| Med Alerts | column | Yes | Critical/Standard/None | Enum with color coding |
| Status | column | Yes | Active/Overdue/Completed | Enum |
| Action | column | Yes | View/Edit/Reassign/Escalate | RBAC enforced |
| Search/Filters | control | No | Provider/Milestone/Status/Date range | Valid enums/ranges |
| Pagination | control | No | Page and size controls | Standard UX pattern |

**Business Rules**:

- Shows all aftercare cases across all providers
- Admin can edit any case data (full editability)
- Overdue cases shown with amber indicators
- Progress calculated automatically by system
- All actions logged for audit trail

**Notes**:

- Admin view shows all cases across all providers (unlike provider view which is filtered)
- Full editability allows admins to override any data when needed
- Color-coded alerts and status indicators help admins quickly identify cases needing attention
- Search and filter capabilities enable admins to find specific cases efficiently
- Action menu provides quick access to admin interventions (reassign, escalate, edit)

#### Screen 14: Aftercare Case Details (Multi-Tab View)

**Purpose**: Admin views comprehensive aftercare case information

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| **Tab 1: Case Overview** | | | | |
| Patient Information | component | Yes | Full patient details (admin can see all) | Display only |
| Patient ID | text | Yes | Unique patient identifier | Display only |
| Patient Name | text | Yes | Full patient name | Display only |
| Contact Information | text | Yes | Email, phone, address | Display only |
| Treatment Information | component | Yes | Original treatment details | Display only |
| Treatment Date | date | Yes | Date treatment was performed | ISO 8601 format |
| Treatment Type | text | Yes | Type of treatment | Display only |
| Provider Information | component | Yes | Assigned provider details | Display only |
| Provider Name | text | Yes | Assigned provider name | Display only |
| Provider Contact | text | Yes | Provider contact information | Display only |
| Aftercare Plan | component | Yes | Selected template and customizations | Display only |
| Template Name | text | Yes | Selected template name | Display only |
| Current Status | component | Yes | Milestone progress and completion | Display only |
| Current Milestone | text | Yes | Current milestone name | Display only |
| Progress Percentage | percent | Yes | Overall progress | 0-100% |
| **Tab 2: Progress Tracking** | | | | |
| Milestone Progress | component | Yes | Visual timeline of all milestones | Display only |
| 3D Scan History | list | Yes | All uploaded scans with dates and quality | Chronological order |
| Scan Upload Date | datetime | Yes | Date scan was uploaded | ISO 8601 format |
| Scan Quality Score | number | Yes | Quality score (0-100) | Integer 0-100 |
| Questionnaire Responses | list | Yes | All responses with timestamps | Chronological order |
| Response Date | datetime | Yes | Date questionnaire was submitted | ISO 8601 format |
| Questionnaire Type | text | Yes | Type of questionnaire | Display only |
| Medication Adherence | component | Yes | Compliance tracking and history | Display only |
| Adherence Percentage | percent | Yes | Overall adherence percentage | 0-100% |
| Activity Compliance | percent | Yes | Compliance with activity restrictions | 0-100% |
| **Tab 3: Communication Log** | | | | |
| Patient Messages | list | Yes | All patient communications | Chronological order |
| Provider Messages | list | Yes | Provider communications | Chronological order |
| Aftercare Team Messages | list | Yes | Internal team communications | Chronological order |
| Escalation History | list | Yes | All escalations and resolutions | Chronological order |
| System Notifications | list | Yes | Automated notifications sent | Chronological order |
| Message Date | datetime | Yes | Date/time of message | ISO 8601 format |
| Message Type | text | Yes | Type of message | Valid message type enum |
| **Tab 4: Admin Actions** | | | | |
| Edit Aftercare Plan | action | No | Button to modify any aspect of plan | Always available |
| Reassign Provider | action | No | Button to change provider assignment | Always available |
| Escalate Case | action | No | Button to escalate to supervisor | Always available |
| Add Notes | action | No | Button to add internal admin notes | Always available |
| Change History | list | Yes | Audit trail of all changes | Chronological order |
| Change Date | datetime | Yes | Date of change | ISO 8601 format |
| Changed By | text | Yes | User who made change | Display only |
| Change Reason | text | Yes | Reason for change | Display only |

**Business Rules**:

- Admin has full access to all tabs and data
- All changes logged with admin identification
- Patient anonymization rules don't apply to admin
- All communications monitored and logged
- Admin can override any provider settings

**Notes**:

- Multi-tab interface organizes comprehensive case information logically
- Tab 1 provides quick overview of case status and key information
- Tab 2 shows detailed progress tracking across all milestones and activities
- Tab 3 maintains complete communication history for audit and context
- Tab 4 provides admin intervention capabilities with full audit trail
- All tabs provide full admin visibility without restrictions
- Change history ensures complete audit trail for compliance

#### Screen 15: Standalone Aftercare Requests

**Purpose**: Admin manages standalone aftercare service requests

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Request ID | text | Yes | Unique request identifier | Searchable; sortable |
| Submission Date | datetime | Yes | Date request was submitted | ISO 8601 format; sortable |
| Patient Name | text | Yes | Full patient name (admin full visibility) | Display only |
| Patient Email | email | Yes | Patient email address | Valid email format |
| Patient Phone | text | Yes | Patient phone number | E.164 format |
| Treatment Date | date | Yes | Date treatment was performed | ISO 8601 format |
| Treatment Type | text | Yes | Type of treatment | Valid treatment type enum |
| Treatment Clinic | text | Yes | Name of clinic where treatment performed | Display only |
| Requested Duration | text | Yes | Duration requested (e.g., "12 months") | Valid duration enum |
| Payment Method | text | Yes | Payment method selected | Valid payment method enum |
| Payment Status | status | Yes | Payment status (Paid/Pending/Failed) | Valid status enum |
| Request Status | status | Yes | Status (Pending/Assigned/Active/Rejected) | Valid status enum |
| Full Patient Information | component | Yes | Complete patient details | Display only |
| Treatment Documentation | component | Yes | Treatment documentation files | Display/download |
| Current Concerns | textarea | No | Patient's current concerns or issues | Max 2000 chars |
| Uploaded Photos | list | Yes | Photos uploaded by patient | Display only |
| Surgeon Notes | text | No | Notes from treating surgeon | Max 2000 chars |
| Available Providers | list | Yes | List of available providers | Display only |
| Provider Name | text | Yes | Provider name | Display only |
| Provider Specialization | text | Yes | Provider specialization areas | Display only |
| Provider Availability | status | Yes | Current availability status | Valid status enum |
| Assign Provider | action | Yes | Button to assign provider to request | Enabled when provider selected |
| Reject Request | action | Yes | Button to reject request with reason | Always available |
| Rejection Reason | textarea | Yes | Required reason for rejection | Max 500 chars; required when rejecting |

**Business Rules**:

- Requests expire after 7 days if not assigned
- Provider assignment based on specialization and availability
- Rejection requires reason and triggers refund
- All actions logged for audit trail

**Notes**:

- Admin has full visibility into patient information (unlike providers who see anonymized data until payment)
- Request list provides quick overview of all pending standalone requests
- Detailed request view shows all patient-submitted information for informed assignment decisions
- Provider assignment interface helps match requests to appropriate providers based on specialization
- Rejection workflow ensures proper documentation and automatic refund processing
- Expiration tracking helps admins prioritize requests that are approaching deadline

#### Screen 16: Milestone Template Management

**Purpose**: Admin creates and manages aftercare milestone templates

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| **Template List** | | | | |
| Template Name | text | Yes | Name of template | Max 200 chars; unique |
| Template Description | text | No | Description of template | Max 1000 chars |
| Treatment Type | text | Yes | Treatment type (FUE, FUT, DHI, etc.) | Valid treatment type enum |
| Duration | text | Yes | Duration (e.g., "12 months") | Valid duration enum |
| Number of Milestones | number | Yes | Count of milestones in template | Positive integer |
| Usage Count | number | Yes | How many patients currently using | Non-negative integer |
| **Template Editor** | | | | |
| Template Name (Edit) | text | Yes | Template name | Max 200 chars; unique |
| Template Description (Edit) | textarea | No | Template description | Max 1000 chars |
| Treatment Type Selection | select | Yes | Treatment type dropdown | Valid treatment type enum |
| Milestone Name | text | Yes | Name of milestone | Max 200 chars |
| Milestone Duration | number | Yes | Duration in days | Positive integer |
| 3D Scan Frequency | text | Yes | Frequency of scans (e.g., "Weekly") | Valid frequency enum |
| Questionnaire Set | select | Yes | Single Questionnaire Set selection | Must exist in FR-025 catalog |
| Questionnaire Selection | list | Yes | Questions from selected set (aftercare context) | Filtered by context type |
| Questionnaire Frequency | text | Yes | Frequency of questionnaires | Valid frequency enum |
| Educational Resources | list | Yes | Resources assigned to milestone | May be empty |
| Resource Title | text | Yes | Resource title | Max 200 chars |
| Resource Type | select | Yes | Type (video, PDF, webpage) | Valid resource type enum |
| Resource URL | url | Yes | URL or file path | Valid URL or file path |
| Activity Restrictions | textarea | No | Restrictions for milestone | Max 500 chars |
| **Resource Management** | | | | |
| Upload Video | action | No | Button to upload instructional videos | File size max 100MB |
| Add Guide | action | No | Button to add best practice guides | File size max 100MB |
| Create FAQ | action | No | Button to create FAQ documents | File size max 100MB |
| Manage Help Guides | action | No | Button to manage help guides | File size max 100MB |
| Resource File | file | Yes | Uploaded resource file | Max 100MB per file |
| **Pricing Configuration** | | | | |
| Enable for Purchase | checkbox | Yes | Make template available for standalone/add-on purchase | Boolean; default false |
| Service Description | textarea | Cond. | Marketing description for patients | Max 500 chars; required if enabled for purchase |
| Pricing Model | radio | Cond. | Fixed Price or Subscription or Both | Enum: "fixed", "subscription", "both"; required if enabled for purchase |
| Multi-Currency Pricing | component | Cond. | Currency-specific pricing table | Required if enabled for purchase |
| Currency | select | Yes | Currency (USD, GBP, EUR, etc.) | Valid currency enum |
| Fixed Price | currency | Cond. | One-time payment amount | Required if "fixed" or "both" selected |
| Monthly Subscription Price | currency | Cond. | Monthly payment amount | Required if "subscription" or "both" selected |
| Add Currency | action | Yes | Button to add another currency | Always available |
| Default Payment Method | radio | Cond. | Default shown to patient (if Both enabled) | Enum: "fixed", "subscription"; required if "both" selected |
| Enable Discounts | checkbox | No | Allow discount codes for this template | Boolean; default false |

**Business Rules**:

- Templates cannot be deleted if in use
- Changes to active templates require approval
- New templates must be tested before activation
- Resource files limited to 100MB each
- Templates can be marked as "Internal Use Only" (providers only) or "Available for Purchase" (standalone/add-on)
- Purchasable templates require pricing configuration for all supported currencies
- If "Both" pricing model selected, patient can choose between fixed or subscription at purchase
- Monthly subscription price is per month; total subscription amount = monthly price × template duration in months
- Pricing changes to active templates require admin approval and don't affect existing patients (locked at purchase time)
- Multi-currency pricing uses real-time exchange rates as baseline but allows admin override for final pricing
- Template Name is used as service name for patient-facing display (no separate service name needed)
- Questionnaires are not authored here; they are centrally managed in FR-025 (Medical Questionnaire Management). Screen 16 only selects among existing questionnaires and configures schedule/frequency per milestone.
- Screen 16 must surface only questionnaires with context type "Aftercare" from FR-025 (see FR-025), while still allowing explicit inclusion of multi-context questionnaires if flagged as compatible.
- Each aftercare template references exactly one Questionnaire Set (single-select). All milestones within the template schedule questions only from that selected set. Changing the selected set replaces questionnaire references across all milestones in the template.

**Cross-Module Reference**:

- Questionnaire content ownership and lifecycle: see FR-025: Medical Questionnaire Management
- After selecting questionnaires here, their delivery and response handling follow the schedules defined per milestone

**Notes**:

- Template management enables standardization of aftercare plans across providers
- Template list shows usage count to prevent deletion of active templates
- Template editor provides comprehensive configuration for all milestone aspects
- Questionnaire integration with FR-025 ensures consistent questionnaire management
- Single Questionnaire Set per template simplifies configuration while maintaining flexibility
- Resource management supports various media types for educational content
- File size limits (100MB) ensure reasonable storage usage while supporting high-quality content
- Approval workflow for active template changes prevents disruption to ongoing aftercare plans
- Templates serve dual purpose: clinical configuration for providers AND purchasable service offerings for patients
- Pricing configuration allows templates to be sold as standalone/add-on services with flexible payment options
- Multi-currency pricing ensures patients see prices in their local currency
- Template Name serves as both internal reference and patient-facing service name for consistency

#### Screen 17: Provider Performance Dashboard

**Status**: Backlog (post-MVP analytics)

**Purpose**: Admin monitors provider aftercare performance

**Data Fields**:

- **Provider List**
  - Provider name and clinic
  - Active aftercare cases count
  - Average completion rate
  - Patient satisfaction score
  - Response time to escalations

- **Performance Metrics**
  - Cases completed on time percentage
  - Patient compliance rates
  - Escalation frequency
  - Communication response time
  - Patient satisfaction trends

- **Case Details**
  - Individual case performance
  - Patient feedback and complaints
  - Escalation history
  - Communication logs

- **Actions**
  - "Send Feedback" button
  - "Reassign Cases" button
  - "Suspend Provider" button (if performance poor)

**Business Rules**:

- Performance scores calculated monthly
- Poor performance triggers review process
- Provider suspension requires admin approval
- All performance data retained for 2 years
- This screen is deferred to a later phase as it represents system-wide analytics beyond case operations covered by Screens 11–12.

**Notes**:

- Analytics dashboard for monitoring provider performance across all aftercare cases
- Performance metrics calculated monthly to identify trends and issues
- Provider list enables comparison of performance across providers
- Case details provide drill-down capability for specific performance issues
- Action buttons enable admin interventions (feedback, reassignment, suspension)
- Deferred to post-MVP phase as it extends beyond core case management operations

#### Screen 18: Aftercare Progress Tracking (Admin View)

**Status**: Backlog (post-MVP analytics)

**Purpose**: Admin monitors all aftercare progress across all providers

**Data Fields**:

- **System-Wide Progress Overview**
  - Total active cases
  - Average completion rate
  - Cases by milestone phase
  - Overdue cases count
  - Urgent cases requiring attention

- **Provider Performance Grid**
  - Provider name and case count
  - Average completion rate per provider
  - Overdue cases per provider
  - Patient satisfaction scores
  - Response time metrics

- **Case Status Distribution**
  - Active cases by milestone
  - Overdue cases by provider
  - Urgent cases requiring escalation
  - Completed cases (last 30 days)

- **Real-Time Alerts**
  - New urgent cases
  - Overdue tasks requiring attention
  - Provider performance issues
  - System-wide aftercare issues

- **Quick Actions**
  - "View All Overdue Cases" button
  - "Reassign Cases" button
  - "Generate Progress Report" button
  - "Contact Provider" button

**Business Rules**:

- Admin can view all cases across all providers
- Real-time updates from all aftercare activities
- Performance metrics calculated daily
- Alerts generated automatically for issues
- All actions logged with admin identification
- This screen is deferred to a later phase as it represents system-wide analytics beyond case operations covered by Screens 11–12.

**Notes**:

- System-wide analytics dashboard for monitoring all aftercare progress across all providers
- Real-time updates provide current status of all active cases
- Provider performance grid enables comparison and identification of performance patterns
- Case status distribution helps identify systemic issues or bottlenecks
- Real-time alerts notify admins of urgent cases requiring immediate attention
- Quick action buttons enable rapid interventions across multiple cases
- Deferred to post-MVP phase as it extends beyond core case management operations

## Business Rules

### General Module Rules

1. **Activation Rules**
   - Treatment-linked aftercare activates automatically upon treatment completion
   - Standalone aftercare requires payment before activation
   - Admin can manually activate aftercare for special cases

2. **Duration Rules**
   - Standard aftercare duration: 6-12 months
   - Duration determined by treatment type and complexity
   - Extensions require provider and admin approval

3. **Access Rules**
   - Patients can only access their own aftercare data
   - Providers can only access assigned patients
   - Admin has full access to all aftercare data
   - Patient anonymization lifted after payment confirmation

### Milestone and Task Rules

1. **Milestone Progression**
   - Milestones progress automatically based on time elapsed
   - Patients cannot skip milestones
   - Milestone completion requires all tasks completed

2. **Task Completion**
   - 3D scans must meet quality threshold
   - Questionnaires must be completed in full
   - Medication adherence tracked but not mandatory for milestone completion
   - Overdue tasks trigger escalation after 48 hours

3. **Progress Calculation**
   - Progress = (completed tasks / total tasks) * 100
   - Tasks weighted equally
   - Progress updates in real-time

### Communication Rules

1. **Patient Communication**
   - Patients can contact aftercare team 24/7
   - Urgent cases receive priority response (within 2 hours)
   - Standard cases receive response within 24 hours

2. **Provider Communication**
   - Providers can communicate with aftercare team about assigned cases
   - Escalations require immediate response
   - All communications logged for audit

3. **Admin Communication**
   - Admin can communicate with any stakeholder
   - System-wide announcements sent to all relevant parties
   - Emergency communications bypass normal channels

### Data and Privacy Rules

1. **Data Retention**
   - Aftercare data retained for 7 years minimum
   - 3D scans retained for 2 years after aftercare completion
   - Communication logs retained for 3 years

2. **Data Access**
   - Patient data anonymized until payment confirmation
   - Provider access limited to assigned patients
   - Admin access logged for audit trail

3. **Data Security**
   - All aftercare data encrypted at rest and in transit
   - 3D scans watermarked with patient ID
   - Access attempts logged and monitored

### Admin Editability Rules

1. **Full Admin Override**
   - Admin can edit ALL aftercare data in the system
   - Admin can modify any provider's aftercare plans
   - Admin can change patient assignments and providers
   - Admin can override any system-calculated progress

2. **Edit Capabilities**
   - **Aftercare Plans**: Modify templates, milestones, medications, instructions
   - **Patient Data**: Edit patient information, treatment details, contact info
   - **Provider Data**: Modify provider assignments, customizations, settings
   - **Progress Data**: Override progress calculations, milestone completions
   - **Communication Data**: Edit messages, escalations, notifications
   - **Template Data**: Modify milestone templates, questionnaires, resources

3. **Edit Tracking**
   - All admin edits logged with timestamp and admin identification
   - Change reason required for all modifications
   - Edit history maintained for audit trail
   - Provider and patient notified of significant changes

### Payment and Billing Rules

1. **Standalone Aftercare Payment**
   - Payment required before service activation
   - Refunds processed automatically for rejected requests
   - Payment disputes handled by admin team

2. **Provider Compensation**
   - Providers compensated for aftercare participation
   - Compensation based on case complexity and duration
   - Payment processed monthly

3. **Platform Commission**
   - Platform commission deducted from standalone aftercare payments
   - Commission rate: 15-25% (configurable)
   - Commission calculated at time of payment

4. **Aftercare Service Payment Rules**
   - **Template-based pricing**: Each aftercare template defines its own pricing (fixed, subscription, or both) in Screen 16
   - **Multi-currency support**: Pricing configured per currency; patient sees price in local currency based on location
   - **Payment method selection**: If template offers both fixed and subscription, patient chooses at purchase time
   - **Subscription payments**: Monthly installments charged automatically for template duration; first payment immediate, subsequent on monthly anniversary
   - **Post-treatment add-on availability**: Available to Hairline-treated patients within 90 days of treatment completion
   - **Standalone service availability**: Available to all patients regardless of treatment source
   - **Template filtering**: Only templates marked "Available for Purchase" are shown; filtered by treatment type compatibility
   - **Pricing immutability**: Patients locked into price at time of purchase (future template price changes don't affect existing patients)
   - **Payment timing**: Payment required before service activation for both standalone and post-treatment add-on
   - **Refund policy**: Full refund if request rejected by admin; prorated refund for subscription cancellations based on unused months

## Success Criteria

### Patient Experience Metrics

- **SC-001**: 90% of patients complete their first milestone within 7 days of activation
- **SC-002**: 85% of patients maintain 80%+ task completion rate throughout aftercare
- **SC-003**: 95% of patients can successfully upload 3D scans on first attempt
- **SC-004**: Patient satisfaction score of 4.5+ stars for aftercare experience

### Provider Efficiency Metrics

- **SC-005**: Providers can set up aftercare plan for new patient in under 10 minutes
- **SC-006**: 90% of providers respond to aftercare escalations within 4 hours
- **SC-007**: Provider aftercare case load of 50-100 patients without quality degradation

### Admin Management Metrics

- **SC-008**: Admin can assign standalone aftercare request within 24 hours
- **SC-009**: 95% of aftercare cases complete without admin intervention
- **SC-010**: Admin dashboard loads with all metrics in under 3 seconds

### System Performance Metrics

- **SC-011**: 3D scan upload completes in under 60 seconds for 95% of uploads
- **SC-012**: Questionnaire completion rate of 90% within scheduled timeframe
- **SC-013**: System supports 1000+ concurrent aftercare patients
- **SC-014**: 99.5% uptime for aftercare module during business hours

### Business Impact Metrics

- **SC-015**: 70% of patients actively engage with aftercare features (vs. passive monitoring)
- **SC-016**: 25% reduction in post-procedure complications through early detection
- **SC-017**: 40% increase in patient retention for future procedures
- **SC-018**: Standalone aftercare service achieves 15% profit margin

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-010 / Module PR-XX**: Treatment Execution & Documentation
  - **Why needed**: Triggers automatic aftercare activation when treatment is marked as completed
  - **Integration point**: Treatment completion event triggers aftercare setup workflow; uses treatment details to pre-populate aftercare plan

- **FR-002 / Module P-XX**: Medical History & 3D Scanning
  - **Why needed**: Provides 3D scan capture technology and infrastructure for patient milestone scans
  - **Integration point**: Shares 3D scanning SDK integration and scan storage infrastructure; reuses scan quality validation logic

- **FR-007 / Module S-XX**: Payment Processing
  - **Why needed**: Processes standalone aftercare service payments before activation
  - **Integration point**: Payment completion triggers aftercare request assignment; payment status determines service activation eligibility

- **FR-020 / Module S-XX**: Notifications & Alerts
  - **Why needed**: Sends task reminders, progress updates, and urgent alerts to patients, providers, and aftercare team
  - **Integration point**: Aftercare events (task due, milestone completion, escalations) trigger notification delivery; notification preferences managed per user

### External Dependencies (APIs, Services)

- **3D Scanning SDK - ARKit/ARCore**:
  - **Purpose**: Provides 3D head scanning capabilities on mobile devices for patient milestone scans
  - **Integration**: Native SDK integration in mobile apps (iOS ARKit, Android ARCore) for real-time 3D capture
  - **Failure handling**: Fallback to 2D photo capture if 3D scanning unavailable; user notification of degraded functionality

- **Cloud Storage Service**:
  - **Purpose**: Secure storage for 3D scans, documents, and educational resources
  - **Integration**: RESTful API for file upload/download with signed URLs for secure access
  - **Failure handling**: Retry with exponential backoff; queue uploads for retry if service unavailable; notify user of upload delays

- **Payment Gateway - Stripe**:
  - **Purpose**: Processes standalone aftercare service payments
  - **Integration**: Stripe API integration for payment processing and refund handling
  - **Failure handling**: Payment failures trigger retry queue; user notified of payment issues; automatic refund processing on rejection

- **Notification Service**:
  - **Purpose**: Delivers email, SMS, and push notifications for reminders and alerts
  - **Integration**: RESTful API for notification delivery with delivery status tracking
  - **Failure handling**: Retry failed notifications; fallback to alternative channels (e.g., SMS if email fails); notification delivery failures logged for monitoring

### Data Dependencies

- **Patient Data**:
  - **Why needed**: Patient profile information required for aftercare plan creation and patient identification
  - **Source**: Patient registration module (FR-001) and treatment records (FR-010)

- **Provider Data**:
  - **Why needed**: Provider information required for aftercare plan assignment and provider capabilities
  - **Source**: Provider onboarding module and treatment execution records (FR-010)

- **Treatment Data**:
  - **Why needed**: Treatment completion status and details trigger aftercare activation and inform plan configuration
  - **Source**: Treatment Execution & Documentation module (FR-010)

- **Payment Data**:
  - **Why needed**: Payment confirmation required for standalone aftercare activation and provider access to patient information
  - **Source**: Payment Processing module (FR-007)

## Assumptions

### User Behavior Assumptions

- Patients will actively participate in aftercare activities and complete required tasks
- Patients will follow medication schedules and activity restrictions as prescribed
- Providers will engage with aftercare features and respond to escalations promptly

### Technology Assumptions

- Patients have smartphones with camera capabilities for 3D scanning
- Patients have reliable internet access for uploading scans and completing questionnaires
- Infrastructure can handle concurrent aftercare operations without degradation

### Business Process Assumptions

- Sufficient provider capacity exists to handle aftercare case load
- Admin team can manage operations and respond to escalations
- 3D scans and questionnaire responses will be of sufficient quality for assessment
- Standalone aftercare payments will process successfully without significant failures

## Implementation Notes

### Technical Considerations

- **Real-time Updates**: Progress tracking and notifications require real-time data synchronization
- **File Management**: 3D scan storage and retrieval must be optimized for performance
- **Mobile Optimization**: Patient screens must work seamlessly on mobile devices
- **Offline Capability**: Core aftercare features should work with limited connectivity

### Integration Points

- **Integration 1 - Treatment Module**: Seamless transition from treatment completion to aftercare activation
  - **Data format**: JSON payload with treatment ID, completion status, patient ID, provider ID, treatment details
  - **Authentication**: OAuth 2.0 bearer tokens for service-to-service communication
  - **Error handling**: Retry with exponential backoff on 5xx errors; queue activation requests if treatment module unavailable

- **Integration 2 - Payment Module**: Integration for standalone aftercare service payments
  - **Data format**: JSON payload with payment ID, amount, currency, payment method, patient ID, service type
  - **Authentication**: API key authentication for payment gateway integration
  - **Error handling**: Payment failures trigger user notification and retry queue; automatic refund processing on rejection

- **Integration 3 - Notification Module**: Automated reminders and alerts for aftercare tasks
  - **Data format**: JSON payload with recipient ID, notification type, message content, priority, delivery channels
  - **Authentication**: OAuth 2.0 bearer tokens for service-to-service communication
  - **Error handling**: Retry failed notifications with exponential backoff; fallback to alternative delivery channels

- **Integration 4 - Communication Module**: Secure messaging between all stakeholders
  - **Data format**: JSON payload with sender ID, recipient ID, message content, message type, attachments
  - **Authentication**: OAuth 2.0 bearer tokens with role-based access control
  - **Error handling**: Message delivery failures logged and retried; user notified of delivery status

### Scalability Considerations

- **Database Design**: Efficient querying for large numbers of aftercare cases
- **File Storage**: Scalable storage solution for 3D scans and documents
- **Notification Delivery**: Reliable delivery of high-volume notifications
- **Provider Assignment**: Automated assignment algorithms for standalone cases

### Security Considerations

- **Data Encryption**: All aftercare data encrypted at rest and in transit
- **Access Control**: Strict role-based access to aftercare data
- **Audit Logging**: Comprehensive logging of all aftercare activities
- **Compliance**: Healthcare data protection regulations compliance

---

## Functional Requirements Summary

### Core Requirements

- FR-011-CR1: System MUST support treatment-linked and standalone aftercare activation paths
- FR-011-CR2: Patients MUST be able to complete milestone tasks (3D scans, questionnaires) with reminders and quality validation
- FR-011-CR3: Providers MUST be able to configure and activate aftercare plans with template customization
- FR-011-CR4: Admin MUST be able to oversee cases, reassign providers, and override plans with full audit

### Data Requirements

- FR-011-DR1: System MUST track milestones, tasks, progress, and adherence as structured entities
- FR-011-DR2: System MUST retain all aftercare artifacts (scans, questionnaires, communications) per retention policy
- FR-011-DR3: Progress MUST be derived deterministically from plan and task completion

### Security & Privacy Requirements

- FR-011-SP1: All aftercare data MUST be encrypted in transit and at rest
- FR-011-SP2: Access MUST be role-based (patient, provider, admin) and fully audited
- FR-011-SP3: PII visibility MUST follow payment-confirmation policy and admin exemptions

### Integration Requirements

- FR-011-IR1: System MUST integrate with Notification Service for reminders/alerts
- FR-011-IR2: System MUST store media artifacts in secure storage with controlled access
- FR-011-IR3: System MUST reference questionnaires managed in FR-025 for aftercare context

## User Scenarios & Testing

### User Story 1 - Treatment-Linked Setup & Activation (Priority: P1)

Why: Core path for Hairline-treated patients entering aftercare.

Independent Test: Provider completes treatment; selects template; activates plan; patient and aftercare team receive notifications.

Acceptance Scenarios:

1. Given treatment completion, When provider selects and activates an aftercare template, Then patient dashboard and team assignment are created
2. Given activation, When notifications are sent, Then patient and assigned team receive activation messages
3. Given activation, When viewing patient dashboard, Then milestones, tasks, and schedule are visible

### User Story 2 - Patient Completes Milestone Tasks (Priority: P1)

Why: Ensures ongoing patient engagement and monitoring.

Independent Test: Patient receives reminders; uploads 3D scan; completes questionnaire; progress updates; alerts generated if concerning.

Acceptance Scenarios:

1. Given task due, When patient uploads scan meeting quality, Then task is completed and progress updates
2. Given concerning questionnaire responses, When submitted, Then case is flagged urgent and team notified
3. Given missed tasks, When overdue by 24 hours, Then status is Overdue and reminders/escalations trigger

### User Story 3 - Standalone Aftercare Onboarding (Priority: P2)

Why: Opens service to external clinic patients.

Independent Test: Patient requests standalone service, payment completes, admin assigns provider, provider activates plan.

Acceptance Scenarios:

1. Given paid request, When admin assigns provider, Then provider configures and activates plan
2. Given activation, When patient opens app, Then aftercare dashboard is available with schedule

### Edge Cases

- Provider withdrawal: admin reassigns or cancels with reason; patient notified
- Network loss during scan upload: resumable upload; no duplicate entries
- Conflicting schedule changes: latest confirmed change supersedes prior; audit preserved

## Key Entities

- AftercarePlan: patientId, providerId, templateId, status, milestones[], medications[], customInstructions, activatedAt
  - Key attributes: plan status, schedule, customization
  - Relationships: belongsTo Patient; belongsTo Provider; references Template

- Milestone: planId, name, durationDays, scanSchedule, questionnaireSchedule, resources[]
  - Key attributes: schedule and required tasks
  - Relationships: belongsTo AftercarePlan

- AftercareTask: planId, milestoneId, type (scan|questionnaire|medication|education), dueAt, completedAt, status
  - Key attributes: task status and timestamps
  - Relationships: belongsTo Milestone

- ScanArtifact: planId, milestoneId, storageUrl, qualityScore, capturedAt, validated
  - Key attributes: media reference, quality
  - Relationships: belongsTo AftercarePlan; referenced by tasks

- QuestionnaireResponse: planId, milestoneId, questionnaireId, answers, flagged, submittedAt
  - Key attributes: responses and flags
  - Relationships: belongsTo AftercarePlan; references FR-025 questionnaire

- AftercareAuditEntry: entityType, entityId, action, actorId, reason, before, after, createdAt
  - Key attributes: immutable audit record
  - Relationships: belongsTo AftercarePlan (or nested entities)

**Document Status**: ✅ Verified & Approved  
**Next Steps**: Technical specification and implementation planning  
**Maintained By**: Product & Engineering Teams  
**Review Cycle**: Monthly or upon major changes  
**Verification Date**: 2025-10-23 - Cross-checked against client transcriptions and confirmed alignment

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-23 | 1.0 | Initial PRD creation | Product & Engineering |
| 2025-11-04 | 1.1 | Template compliance: added Shared Services; Communication Structure (In/Out of Scope); Triggers/Outcomes for workflows; restructured Assumptions; added User Scenarios & Testing; Appendices | Product & Engineering |

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |
