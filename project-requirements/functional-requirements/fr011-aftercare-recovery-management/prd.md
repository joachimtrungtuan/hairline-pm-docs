# Aftercare & Recovery Management Module - Product Requirements Document

**Module**: P-05: Aftercare & Progress Monitoring | PR-05: Aftercare Participation | A-03: Aftercare Team Management  
**Feature Branch**: `fr011-aftercare-recovery-management`  
**Created**: 2025-10-23  
**Status**: ✅ Verified & Approved  
**Source**: FR-011 from system-prd.md

## Executive Summary

The Aftercare & Recovery Management module provides comprehensive post-procedure support for hair transplant patients through milestone-based tracking, 3D scan monitoring, questionnaire assessments, and multi-tenant communication. The module supports both treatment-linked aftercare (for Hairline platform patients) and standalone aftercare services (for external clinic patients).

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-05)**: Aftercare & Progress Monitoring
- **Provider Platform (PR-05)**: Aftercare Participation (optional)
- **Admin Platform (A-03)**: Aftercare Team Management

### Communication Structure

**Note**: Direct patient-provider chat functionality is currently **not in scope** for V1 and has been moved to the backlog. Communication within the aftercare module is structured through:

- **Patient ↔ Aftercare Team**: Direct communication through structured messaging, questionnaires, and 3D scan submissions
- **Provider ↔ Aftercare Team**: Communication regarding patient cases and escalations
- **Admin ↔ All Parties**: Admin can monitor all communications and intervene as needed
- **Structured Updates**: Progress updates, milestone notifications, and system-generated alerts

If direct patient-provider chat is implemented in the future, it would be handled through a separate FR (FR-012: Messaging & Communication).

### Entry Points

1. **Treatment-Linked Aftercare**: Automatic activation after Hairline platform treatment completion
2. **Standalone Aftercare**: Patient-purchased service for external clinic treatments
3. **Admin-Managed**: Direct assignment by admin team

## Business Workflows

### Workflow 1: Treatment-Linked Aftercare Setup (Primary Flow)

**Actors**: Provider, System, Patient, Aftercare Team

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

**Main Flow**:

1. **Service Request**
   - Patient navigates to "Request Aftercare Service" in app
   - Patient fills out treatment details form
   - Patient selects aftercare duration and payment option
   - Patient submits request and makes payment

2. **Admin Review & Assignment**
   - Request appears in admin dashboard as "Pending Assignment"
   - Admin reviews patient information and treatment details
   - Admin assigns suitable provider to oversee case
   - System notifies assigned provider

3. **Provider Activation**
   - Assigned provider reviews patient case
   - Provider selects appropriate aftercare template
   - Provider customizes plan based on patient's specific situation
   - Provider activates aftercare plan

4. **Patient Onboarding**
   - Patient receives activation notification
   - Patient gains access to aftercare dashboard
   - Aftercare team begins monitoring

**Alternative Flows**:

- **B1**: Admin rejects request
  - Admin marks request as "Not suitable for aftercare"
  - Patient receives rejection notification with reason
  - Refund processed automatically

- **B2**: No suitable provider available
  - Admin marks as "Awaiting provider availability"
  - Patient notified of delay
  - Admin manually assigns when provider becomes available

### Workflow 3: Patient Aftercare Activities (Ongoing Flow)

**Actors**: Patient, System, Aftercare Team

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

- **Progress Overview**
  - Overall progress percentage (calculated field)
  - Current milestone name and phase
  - Days remaining in current milestone
  - Next upcoming task with countdown timer

- **Recent Activity**
  - Last 3D scan date and status
  - Last questionnaire completion date
  - Medication adherence percentage
  - Upcoming tasks list (next 7 days)

- **Quick Actions**
  - "Upload 3D Scan" button (if due)
  - "Complete Questionnaire" button (if due)
  - "View Instructions" button
  - "Contact Support" button

**Business Rules**:

- Progress percentage = (completed tasks / total tasks) * 100
- Tasks include: 3D scans, questionnaires, medication adherence
- Overdue tasks highlighted in red
- Completed tasks shown in green

#### Screen 2: 3D Scan Upload

**Purpose**: Patient uploads milestone 3D head scans

**Data Fields**:

- **Scan Information**
  - Milestone name (read-only)
  - Scan due date (read-only)
  - Days overdue (if applicable)
  - Scan guidance instructions

- **Scan Capture**
  - Camera viewfinder
  - Scan quality indicator
  - "Capture Scan" button
  - "Retake" button (if quality poor)

- **Upload Status**
  - Upload progress bar
  - Upload success/error message
  - "View Previous Scans" link

**Business Rules**:

- Scan must meet minimum quality threshold
- Maximum file size: 50MB
- Only one scan per milestone allowed
- Previous scans remain accessible for comparison

#### Screen 3: Questionnaire Completion

**Purpose**: Patient completes milestone-specific questionnaires

**Data Fields**:

- **Questionnaire Header**
  - Milestone name and phase
  - Questionnaire type (Pain Assessment, Sleep Quality, etc.)
  - Due date and completion status

- **Question Fields** (dynamic based on questionnaire type)
  - **Pain Assessment**: Scale 1-10, description text area
  - **Sleep Quality**: Hours slept (number), quality rating (1-5), disruptions (checkbox list)
  - **Compliance Check**: Medication adherence (yes/no), activity restrictions (yes/no), washing instructions (yes/no)
  - **Symptom Check**: Swelling (yes/no), redness (yes/no), bleeding (yes/no), infection signs (yes/no)

- **Submission**
  - "Save Draft" button
  - "Submit" button
  - Warning for concerning responses

**Business Rules**:

- All required fields must be completed
- Concerning responses (pain >7, infection signs) trigger urgent flag
- Drafts saved automatically every 30 seconds
- One submission per questionnaire allowed

#### Screen 4: Medication Schedule

**Purpose**: Patient views and tracks medication adherence

**Data Fields**:

- **Current Medications**
  - Medication name
  - Dosage and frequency
  - Special instructions
  - Start and end dates

- **Today's Schedule**
  - Upcoming doses with times
  - "Mark as Taken" buttons
  - Missed dose indicators

- **Adherence Tracking**
  - Weekly adherence percentage
  - Missed doses count
  - "View History" link

**Business Rules**:

- Medications prescribed by provider during aftercare setup
- Adherence calculated as (taken doses / total doses) * 100
- Missed doses trigger reminder notifications
- History available for entire aftercare period

#### Screen 5: Educational Resources

**Purpose**: Patient accesses milestone-specific educational content

**Data Fields**:

- **Resource Categories**
  - Instructional videos
  - Best practice guides
  - FAQ documents
  - When to seek help guide

- **Resource Details**
  - Resource title and description
  - Duration (for videos)
  - "Mark as Viewed" checkbox
  - Download/view buttons

- **Progress Tracking**
  - Resources viewed count
  - Completion percentage per category
  - "Mark All as Viewed" option

**Business Rules**:

- Resources specific to current milestone
- Viewing progress tracked for compliance
- Resources remain accessible throughout aftercare
- New resources added by admin appear automatically

### Provider Platform Screens

#### Screen 6: Aftercare Cases List

**Purpose**: Provider views all patients in aftercare (similar to existing "In Progress" list)

**Data Fields**:

- **Table Headers** (sortable with up/down arrows):
  - **Patient ID**: Unique identifier (e.g., HPID2509-0001)
  - **Patient Name**: Avatar icon + full patient name + email (e.g., "Aylin Kaya", "@gmail.com")
  - **Phone Number**: Contact number
  - **Age**: Patient age
  - **Problem**: Treatment area (Hair, Both, Beard)
  - **Treatment & Package**: Treatment type + package name
  - **Aftercare Start Date**: When aftercare began
  - **Current Milestone**: Current phase name
  - **Progress**: Visual progress bar (e.g., "3/5 day", "2/3 day")
  - **Med Alerts**: Color-coded status (Critical-red, Standard-yellow, None-green)
  - **Last Activity**: Time since last patient interaction
  - **Action**: Ellipsis menu (View, Edit, Message, Escalate)

- **Search and Filter Controls**:
  - Search bar: "Search aftercare cases"
  - Filter button with funnel icon
  - Sortable columns with arrow indicators

- **Pagination**:
  - "Total X items" display
  - Page navigation: "< 1 2 3 4 5 ... 50 >"
  - Items per page dropdown: "10/page"

**Business Rules**:

- Only shows patients assigned to this provider
- Overdue cases shown with amber indicators
- Patient names are fully visible as aftercare occurs post-payment confirmation
- Progress calculated automatically by system
- All data editable by admin (admin override capability)

#### Screen 7: Patient Aftercare Details

**Purpose**: Provider views comprehensive patient aftercare progress with full historical context

**Data Fields**:

- **Patient Information**
  - Patient ID and treatment details (if Hairline-treated patient)
  - Aftercare start date and duration
  - Assigned aftercare template
  - Provider's custom instructions
  - **Note**: For standalone aftercare patients, treatment details will show "N/A" or be blank

- **Progress Overview**
  - Current milestone and phase
  - Overall progress percentage (auto-calculated)
  - Milestone completion timeline
  - Upcoming tasks

- **Activity History** (Chronological, Additive)
  - 3D scan uploads with dates and quality scores
  - Questionnaire responses with timestamps
  - Medication adherence history
  - Communication log with aftercare team
  - **Data Persistence**: All historical data retained, new data added without removing old data

- **Actions**
  - "Adjust Aftercare Plan" button
  - "Request Additional Scan" button
  - "Contact Aftercare Team" button
  - "Escalate Case" button

**Business Rules**:

- **Data Persistence**: Screen displays all historical data from patient's entire journey (inquiry → treatment → aftercare) without removing older data, providing complete context
- **Dual Case Handling**:
  - **Hairline-treated patients**: Shows complete lifecycle data including pre-treatment inquiry, quote, treatment details, and aftercare
  - **Standalone aftercare patients**: Shows only aftercare-specific data with initial intake information provided during standalone request
- Full patient details visible as aftercare occurs post-payment confirmation
- All activities logged with timestamps
- Provider can modify plan only for their assigned patients
- Escalation creates audit trail

#### Screen 8: Aftercare Setup (Multi-Step Process)

**Purpose**: Provider sets up aftercare plan after treatment completion

##### **Step 1: Template Selection**

- **Available Templates**: List of admin-created templates
  - Template name and description
  - Treatment type compatibility
  - Duration (6 months, 12 months, etc.)
  - Milestone count and structure
- **Template Preview**: Shows template details before selection
- **Selection**: "Select Template" button

##### **Step 2: Milestone Customization**

- **Milestone List**: All milestones from selected template
  - Milestone name and duration
  - 3D scan frequency
  - Questionnaire types and frequency
  - Educational resources
  - Activity restrictions
- **Customization Options**:
  - Modify milestone durations
  - Add/remove questionnaires
  - Add custom instructions per milestone
  - Override activity restrictions

##### **Step 3: Medication Setup**

- **Medication List**: Add medications for patient
  - Medication name (dropdown from database)
  - Dosage and frequency
  - Start and end dates
  - Special instructions
  - "Add Medication" button
- **Medication Schedule**: Visual timeline of all medications

##### **Step 4: Custom Instructions**

- **General Instructions**: Free-text area for provider notes
- **Milestone-Specific Instructions**: Instructions per milestone
- **Emergency Contact**: Provider contact information for patient
- **Special Considerations**: Patient-specific notes

##### **Step 5: Review and Confirm**

- **Plan Summary**: Complete aftercare plan overview
- **Patient Information**: Confirmation of patient details
- **Provider Information**: Provider contact details
- **Confirmation**: "Activate Aftercare Plan" button

**Business Rules**:

- All steps must be completed before activation
- Provider can go back to previous steps
- System validates all required fields
- Admin can edit any step after activation
- Patient receives notification upon activation

#### Screen 9: Aftercare Plan Edit

**Purpose**: Provider or Admin modifies existing aftercare plan

**Data Fields**:

- **Current Plan Overview**
  - Selected template name
  - Milestone structure with progress
  - Medication schedule
  - Custom instructions

- **Edit Options** (Provider):
  - Modify medication schedule
  - Update custom instructions
  - Add milestone-specific notes
  - Request milestone duration changes

- **Edit Options** (Admin):
  - All provider options plus:
  - Change milestone structure
  - Modify template assignments
  - Override any aftercare settings
  - Reassign to different provider

- **Change Tracking**
  - Change reason (required)
  - Change timestamp
  - Changed by (user identification)
  - Approval status

**Business Rules**:

- Provider changes logged and tracked
- Admin changes override provider settings
- Major changes require admin approval
- All changes logged with reason and timestamp
- Patient notified of approved changes
- Change history maintained for audit trail

#### Screen 9: Aftercare Progress Tracking (Provider View)

**Purpose**: Provider monitors ongoing aftercare progress for assigned patients

**Data Fields**:

- **Patient Progress Overview**
  - Patient name and current milestone
  - Overall progress percentage (auto-calculated)
  - Days remaining in current milestone
  - Next upcoming tasks

- **Milestone Timeline**
  - Visual timeline of all milestones
  - Completed milestones (green)
  - Current milestone (blue)
  - Upcoming milestones (gray)
  - Overdue tasks (red indicators)

- **Task Completion Status**
  - 3D scans: Completed/Pending/Overdue with dates
  - Questionnaires: Completed/Pending/Overdue with dates
  - Medication adherence: Percentage and missed doses
  - Activity compliance: Adherence to restrictions

- **Patient Activity Feed**
  - Recent 3D scan uploads
  - Questionnaire completions
  - Medication adherence updates
  - Communication interactions

- **Quick Actions**
  - "Request Additional Scan" button
  - "Send Message to Patient" button
  - "Schedule Consultation" button
  - "Escalate Case" button

**Business Rules**:

- Progress calculated automatically by system
- Provider can only view assigned patients
- Real-time updates when patient completes tasks
- Overdue tasks highlighted prominently
- All actions logged for audit trail

### Admin Platform Screens

#### Screen 10: Aftercare Cases List

**Purpose**: Admin views all aftercare cases (similar to existing provider lists)

**Data Fields**:

- **Table Headers** (sortable with up/down arrows):
  - **Case ID**: Unique identifier (e.g., AC2509-0001)
  - **Patient Name**: Avatar icon + full patient name + email
  - **Phone Number**: Contact number
  - **Age**: Patient age
  - **Problem**: Treatment area (Hair, Both, Beard)
  - **Treatment & Package**: Treatment type + package name
  - **Provider**: Assigned provider name
  - **Aftercare Type**: Treatment-linked or Standalone
  - **Start Date**: When aftercare began
  - **Current Milestone**: Current phase name
  - **Progress**: Visual progress bar
  - **Med Alerts**: Color-coded status (Critical-red, Standard-yellow, None-green)
  - **Status**: Active, Overdue, Completed
  - **Action**: Ellipsis menu (View, Edit, Reassign, Escalate)

- **Search and Filter Controls**:
  - Search bar: "Search aftercare cases"
  - Filter button with funnel icon
  - Advanced filters: Provider, Milestone, Status, Date range
  - Sortable columns with arrow indicators

- **Pagination**:
  - "Total X items" display
  - Page navigation: "< 1 2 3 4 5 ... 50 >"
  - Items per page dropdown: "10/page"

**Business Rules**:

- Shows all aftercare cases across all providers
- Admin can edit any case data (full editability)
- Overdue cases shown with amber indicators
- Progress calculated automatically by system
- All actions logged for audit trail

#### Screen 11: Aftercare Case Details (Multi-Tab View)

**Purpose**: Admin views comprehensive aftercare case information

##### **Tab 1: Case Overview**

- **Patient Information**: Full patient details (admin can see all)
- **Treatment Information**: Original treatment details
- **Provider Information**: Assigned provider details
- **Aftercare Plan**: Selected template and customizations
- **Current Status**: Milestone progress and completion

##### **Tab 2: Progress Tracking**

- **Milestone Progress**: Visual timeline of all milestones
- **3D Scan History**: All uploaded scans with dates and quality scores
- **Questionnaire Responses**: All responses with timestamps
- **Medication Adherence**: Compliance tracking and history
- **Activity Compliance**: Activity restriction adherence

##### **Tab 3: Communication Log**

- **Patient Messages**: All patient communications
- **Provider Messages**: Provider communications
- **Aftercare Team Messages**: Internal team communications
- **Escalation History**: All escalations and resolutions
- **System Notifications**: Automated notifications sent

##### **Tab 4: Admin Actions**

- **Edit Aftercare Plan**: Modify any aspect of the plan
- **Reassign Provider**: Change provider assignment
- **Escalate Case**: Escalate to medical supervisor
- **Add Notes**: Internal admin notes
- **Change History**: Audit trail of all changes

**Business Rules**:

- Admin has full access to all tabs and data
- All changes logged with admin identification
- Patient anonymization rules don't apply to admin
- All communications monitored and logged
- Admin can override any provider settings

#### Screen 12: Standalone Aftercare Requests

**Purpose**: Admin manages standalone aftercare service requests

**Data Fields**:

- **Request List**
  - Request ID and submission date
  - Patient information (anonymized until payment)
  - Treatment details (date, type, clinic)
  - Requested duration and payment method
  - Status (Pending, Assigned, Active, Rejected)

- **Request Details**
  - Full patient information
  - Treatment documentation
  - Current concerns or issues
  - Uploaded photos and surgeon notes
  - Payment status

- **Assignment Options**
  - Available providers list
  - Provider specializations and availability
  - "Assign Provider" button
  - "Reject Request" button with reason

**Business Rules**:

- Requests expire after 7 days if not assigned
- Provider assignment based on specialization and availability
- Rejection requires reason and triggers refund
- All actions logged for audit trail

#### Screen 13: Milestone Template Management

**Purpose**: Admin creates and manages aftercare milestone templates

**Data Fields**:

- **Template List**
  - Template name and description
  - Treatment type (FUE, FUT, DHI, etc.)
  - Duration (6 months, 12 months, etc.)
  - Number of milestones
  - Usage count (how many patients using)

- **Template Editor**
  - Template name and description
  - Treatment type selection
  - Milestone configuration:
    - Milestone name and duration
    - 3D scan frequency
    - Questionnaire types and frequency
    - Educational resources
    - Activity restrictions

- **Resource Management**
  - Upload instructional videos
  - Add best practice guides
  - Create FAQ documents
  - Manage help guides

**Business Rules**:

- Templates cannot be deleted if in use
- Changes to active templates require approval
- New templates must be tested before activation
- Resource files limited to 100MB each

#### Screen 14: Provider Performance Dashboard

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

#### Screen 15: Aftercare Progress Tracking (Admin View)

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

## Business Rules

### General Aftercare Rules

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

### Internal Dependencies

- **FR-010**: Treatment Execution & Documentation (triggers aftercare activation)
- **FR-002**: Medical History & 3D Scanning (scan capture technology)
- **FR-007**: Payment Processing (standalone aftercare payments)
- **FR-020**: Notifications & Alerts (task reminders and updates)

### External Dependencies

- **3D Scanning SDK**: ARKit (iOS) and ARCore (Android) for mobile scan capture
- **Cloud Storage**: Secure storage for 3D scans and documents
- **Payment Gateway**: Stripe integration for standalone aftercare payments
- **Notification Service**: Email, SMS, and push notification delivery

### Data Dependencies

- **Patient Data**: From patient registration and treatment records
- **Provider Data**: From provider onboarding and treatment execution
- **Treatment Data**: From treatment completion and documentation
- **Payment Data**: From payment processing and billing systems

## Assumptions

1. **Patient Engagement**: Patients will actively participate in aftercare activities and complete required tasks
2. **Provider Participation**: Providers will engage with aftercare features and respond to escalations promptly
3. **Technology Access**: Patients have access to smartphones with camera capabilities for 3D scanning
4. **Internet Connectivity**: Patients have reliable internet access for uploading scans and completing questionnaires
5. **Medical Compliance**: Patients will follow medication schedules and activity restrictions as prescribed
6. **Provider Availability**: Sufficient provider capacity exists to handle aftercare case load
7. **Admin Resources**: Admin team has capacity to manage aftercare operations and respond to escalations
8. **Data Quality**: 3D scans and questionnaire responses will be of sufficient quality for medical assessment
9. **Payment Processing**: Standalone aftercare payments will be processed successfully without significant failures
10. **System Performance**: Infrastructure can handle concurrent aftercare operations without degradation

## Implementation Notes

### Technical Considerations

- **Real-time Updates**: Progress tracking and notifications require real-time data synchronization
- **File Management**: 3D scan storage and retrieval must be optimized for performance
- **Mobile Optimization**: Patient screens must work seamlessly on mobile devices
- **Offline Capability**: Core aftercare features should work with limited connectivity

### Integration Points

- **Treatment Module**: Seamless transition from treatment completion to aftercare activation
- **Payment Module**: Integration for standalone aftercare service payments
- **Notification Module**: Automated reminders and alerts for aftercare tasks
- **Communication Module**: Secure messaging between all stakeholders

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

**Document Status**: ✅ Verified & Approved  
**Next Steps**: Technical specification and implementation planning  
**Maintained By**: Product & Engineering Teams  
**Review Cycle**: Monthly or upon major changes  
**Verification Date**: 2025-10-23 - Cross-checked against client transcriptions and confirmed alignment
