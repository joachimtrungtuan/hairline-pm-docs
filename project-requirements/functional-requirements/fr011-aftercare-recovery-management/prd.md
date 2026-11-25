# FR-011 - Aftercare & Recovery Management

**Module**: P-05: Aftercare & Progress Monitoring | PR-04: Aftercare Participation *(elevated to P1 scope for FR-011 delivery)* | A-03: Aftercare Team Management  
**Feature Branch**: `fr011-aftercare-recovery-management`  
**Created**: 2025-10-23  
**Status**: ✅ Documentation Approved (baseline 2026-11-25); implementation reconciliation pending  
**Source**: FR-011 from system-prd.md; FR-015 v1.9 provider-status cancellation cascade  

## Executive Summary

The Aftercare & Recovery Management module provides comprehensive post-procedure support for hair transplant patients through milestone-based tracking, scan monitoring, questionnaire assessments, and multi-tenant communication. The module supports both treatment-linked aftercare (for Hairline platform patients) and standalone aftercare services (for external clinic patients).

**Note on Scan Media (V1 vs V2)**: In V1, all references to "3D scans" in this FR refer to standardized head scan photo sets (multiple 2D views). True 3D scanning (ARKit/ARCore) is deferred to V2. (REQ-011-079)

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-05)**: Aftercare & Progress Monitoring
- **Provider Platform (PR-04)**: Aftercare Participation (P1 scope for FR-011)
- **Admin Platform (A-03)**: Aftercare Team Management
- **Shared Services (S-03: Notification Service, S-05: Media Storage Service, S-02: Payment Processing Service)**: Notifications & Alerts, Media Storage, Payment (Standalone), Messaging/Communication (if enabled)

### Multi-Tenant Breakdown

**Patient Platform (P-05)**:

- View aftercare dashboard (milestones, tasks, progress)
- Upload head scan photo sets per schedule *(V1; true 3D in V2)*; complete questionnaires; track medications
- Receive reminders and urgent alerts; contact aftercare team

**Provider Platform (PR-04)**:

- Review assigned aftercare cases and patient progress
- Configure/activate aftercare plans; customize milestones/medications/instructions
- Manage reschedules, escalations, and communications with aftercare team

**Admin Platform (A-03)**:

- Global oversight; case reassignment; plan overrides; escalations
- Template management (milestones, questionnaires, resources)
- Standalone aftercare request intake and assignment
- Aftercare specialist assignment (who delivers a case: an aftercare provider, whose clinic staff are the aftercare specialists, or a Hairline aftercare team member, an admin with the FR-031 Aftercare Coordinator role). FR-011 owns it; other modules only cite it (REQ-011-004)

**Shared Services (S-03, S-05, S-02)**:

- Notifications & alerts; media storage for scans/documents
- Payment for standalone activation; secure messaging (if enabled)

### Communication Structure

**In Scope**:

- Patient ↔ Aftercare Team: Structured messaging, questionnaires, and scan/photo set submissions. The patient's message goes through Contact Support on the Aftercare Dashboard and is recorded in the aftercare communication log, not in an FR-012 conversation (REQ-011-102). The team's messages and replies appear in the Messages list on the same dashboard, with a push and email notification (REQ-011-103)
- Provider ↔ Aftercare Team: Case updates and escalations
- Admin ↔ All Parties: Oversight and interventions
- System-generated updates: Milestone reminders, progress updates, urgent flags

**Out of Scope**:

- Direct patient ↔ provider chat (handled by FR-012; that conversation stays open while the pair has live aftercare and becomes read-only once nothing live is left between them (FR-012 REQ-012-018)) (REQ-011-080)
- Payment flows beyond standalone activation (handled in Payment FR) (REQ-011-080)

### Entry Points

Aftercare has exactly three entry sources:

1. **Treatment-Linked Aftercare**: Starts from the patient's accepted Hairline quote whose treatment was performed (the FR-006 booking reached Aftercare). It covers Workflow 1 (set up at treatment completion) and the Workflow 2b post-treatment add-on (bought later within 90 days). The aftercare record is linked to that accepted quote.
2. **Standalone Aftercare**: Bought directly by patients treated at an outside clinic (Workflow 2). It has no inquiry or quote.
3. **Standalone Aftercare from an FR-038 conversion**: A standalone request created when a patient converts a transplant-progress monitoring case to an aftercare package (Workflow 2, step 1; REQ-011-093 and REQ-011-094).

Admin assignment is not a separate entry route. It is a step inside these routes that decides who delivers the aftercare, for example the Workflow 2 provider assignment, the Workflow 1 A2 Hairline aftercare team takeover, and Workflow 4 reassignment. (REQ-011-016)

## Business Workflows

### Workflow 1: Treatment-Linked Aftercare Setup (Primary Flow)

**Actors**: Provider, System, Patient, Aftercare Team

**Trigger**: FR-010 signals that the treatment is complete (REQ-011-055, REQ-011-091). FR-006 owns the move of the booking to Aftercare, and FR-010 owns marking the treatment complete and retrying a failed signal (REQ-010-086)

**Outcome**: Aftercare plan is configured, activated, and patient/aftercare team are notified

**Main Flow**:

1. **Treatment Completion Signal**
   - System receives the treatment-completion signal from FR-010 (the booking is already in Aftercare under FR-006)
   - Aftercare setup starts automatically and the provider is prompted to configure the aftercare plan (REQ-011-017)
   - The plan row opens as Pending activation and becomes Active when the plan is confirmed or an admin activates it (REQ-011-092)

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
   - The plan activates when the provider confirms it (REQ-011-055) or an admin activates it manually (REQ-011-019, A3)
   - System generates complete aftercare plan with milestones
   - System creates patient aftercare dashboard
   - System sends activation notification to patient
   - Aftercare team receives case assignment notification

**Alternative Flows**:

- **A1**: Provider provides only paperwork/instructions (REQ-011-056)
  - Provider marks "Paperwork only - no aftercare service"
  - Provider uploads aftercare instructions document
  - Patient receives instructions but no active monitoring
  - Patient status moves to "Completed" after instruction delivery; the setup row closes with no plan, and the closing rule applies: reminders stop and the completion event carries the outcome "paperwork only" (REQ-011-056, REQ-011-101)

- **A2**: Provider requests Hairline aftercare service (REQ-011-057)
  - Provider marks "Assign to Hairline aftercare team"
  - Admin receives notification for aftercare assignment
  - Hairline aftercare team takes over patient monitoring; the Aftercare Coordinator works on the admin Screens 13 to 19 (REQ-011-004)
  - The coordinator confirms the plan on Screen 14 Tab 4 (Configure Plan) and the system activates it (REQ-011-049, REQ-011-055)
  - The setup clock of A3 restarts at the handover and addresses the coordinator (REQ-011-090)
  - Provider receives the fixed handover fee set by the admin (default 0, so nothing is paid until the admin sets an amount); this flow has no separate aftercare price, so Hairline pays the fee from its own revenue (REQ-011-057)

- **A3**: Plan setup is not confirmed in time (REQ-011-090, REQ-011-019)
  - If no plan is confirmed, the provider gets a reminder after 2 days and the case is escalated to the admin after 4 days; both day counts are admin settings
  - The clock starts at the completion signal, restarts at a handover or an admin assignment, and addresses the current assignee (REQ-011-090)
  - Admin opens the case on Screen 14 and either reassigns on Screen 19 (Workflow 4, D5) or activates the plan manually with a mandatory reason; the activation is written to the audit trail

- **A4**: Treatment closed early by an admin decision (REQ-011-091)
  - FR-010 sends the completion signal after the early close
  - Admin assigns the aftercare team or the reassigned provider on Screen 19, and setup opens for them

- **A5**: Completion signal arrives again (REQ-011-091)
  - A repeated signal for the same booking returns the existing plan and creates no second plan

### Workflow 2: Standalone Aftercare Service (Secondary Flow)

**Actors**: Patient, Admin, Assigned Provider, Aftercare Team

**Trigger**: Patient requests standalone aftercare service, directly or by converting an FR-038 monitoring case (REQ-011-093)

**Outcome**: Aftercare plan is assigned, configured, paid for, and activated for the patient

**Order**: Request, then admin assigns a provider, then the provider configures the plan, and payment activates the aftercare (assign first, pay last). (REQ-011-018)

**Main Flow**:

1. **Service Request & Package Selection**
   - Patient navigates to "Request Aftercare Service" in app (Screen 6)
   - Patient selects service type (standalone for external clinic patients)
   - Patient fills out treatment details form (treatment date, type, clinic)
   - Patient browses available aftercare templates marked "Available for Purchase"
   - Patient selects desired template and views pricing breakdown
   - Patient chooses pricing option (fixed price or monthly subscription, if both available)
   - Patient submits the request; no payment is taken at this point
   - Request appears as "Pending Assignment"
   - Coming from an FR-038 conversion, Screen 6 opens with the copied fields, the monitoring report and the selected scan already filled in; the patient still picks the template and pricing option, and a repeated submit with the same key returns the existing request (REQ-011-093, REQ-011-094)

2. **Admin Review & Assignment** (REQ-011-048)
   - Request appears in admin dashboard as "Pending Assignment" (Screen 15)
   - Admin reviews patient information and treatment details
   - Admin assigns suitable provider to oversee case
   - System notifies assigned provider; the provider sees the patient's details from this moment (REQ-011-010)
   - From the assignment, the 2-day reminder and the 4-day escalation to the admin of REQ-011-090 run while the provider has not finished the plan

3. **Provider Plan Configuration** (REQ-011-049)
   - Assigned provider reviews patient case
   - Provider selects appropriate aftercare template (same as requested template, or an alternative that offers the pricing option the patient chose; REQ-011-100)
   - Provider customizes plan based on patient's specific situation
   - Provider completes the plan; the plan is not active until payment succeeds
   - System sets the request to "Payment due" and notifies the patient that payment is now due; the patient's 48 hours start at this notice (REQ-011-050)

4. **Payment & Activation**
   - Patient reviews order summary of the final template, with template details, pricing option, and total (Screen 7); if the price differs from the requested one the patient accepts the new price or cancels at no charge (B4)
   - Patient selects payment method (credit card, PayPal, etc.)
   - Patient enters payment and billing information
   - Patient accepts terms and conditions
   - Patient submits payment
   - System processes payment via FR-007 Payment Processing module
   - On success: Payment confirmation displayed, email sent, and the aftercare plan is activated
   - On failure: Error message displayed, retry option provided

5. **Patient Onboarding**
   - Patient receives activation notification
   - Patient gains access to aftercare dashboard (Screen 1)
   - Aftercare team begins monitoring

**Alternative Flows**:

- **B1**: Payment fails (REQ-011-050)
  - Patient receives payment failure notification
  - Patient can retry payment with different method
  - Request becomes "Expired" when 48 hours after the payment-due notice pass without successful payment; nothing was charged, so there is nothing to refund

- **B2**: Admin rejects request (REQ-011-051)
  - Admin marks request as "Not suitable for aftercare"
  - Patient receives rejection notification with reason
  - Any payment already taken is refunded in full automatically (REQ-011-037)

- **B3**: No suitable provider available (REQ-011-052)
  - Admin marks as "Awaiting provider availability"
  - Patient notified of delay
  - Admin manually assigns when provider becomes available
  - The 7-day unassigned timer counts from submission, pauses while the request is "Awaiting provider availability" and resumes when that mark is cleared (REQ-011-053)
  - A request still unassigned after 7 days is rejected by the system with a system reason and any payment already taken is refunded in full (REQ-011-053, REQ-011-037)
  - The admin sets and clears the "Awaiting provider availability" mark on Screen 15 with a note, and both actions are audited (REQ-011-052)

- **B4**: Final template price differs from the requested price (REQ-011-100)
  - Screen 7 shows the order summary of the final template and the new price
  - Patient accepts the new price and pays, or cancels at no charge
  - A cancelled request becomes "Rejected" with the system reason "cancelled by patient"

- **B5**: A request converted from FR-038 monitoring ends Rejected or Expired (REQ-011-093, REQ-011-094)
  - The notice says the patient may start a new standalone request, pre-filled from the same source data, with a new idempotency key
  - The monitoring case stays final and is not reopened

### Workflow 2b: Post-Treatment Aftercare Add-On (Secondary Flow)

**Actors**: Patient (Hairline-treated), Admin, Assigned Provider (original or new), Aftercare Team

**Trigger**: Hairline-treated patient requests aftercare service after treatment completion (within 90 days)

**Outcome**: Aftercare plan is configured, activated, and patient receives ongoing monitoring

**Linkage**: The add-on creates treatment-linked aftercare (`treatment_linked`), linked to the accepted quote of the completed Hairline treatment. It is not standalone aftercare; it is only activated later and paid separately (system data schema §13).

**Main Flow**:

1. **Add-On Service Request**
   - Patient navigates to "Add Aftercare Service" in patient dashboard (Screen 6)
   - System verifies patient has completed Hairline treatment within 90 days (REQ-011-044)
   - Patient selects service type (post-treatment add-on)
   - System auto-populates treatment information from patient's treatment history
   - Patient browses available aftercare templates (filtered by treatment type compatibility)
   - Patient selects desired template and pricing option (fixed price or monthly subscription)
   - System refuses the add-on while a plan for the same booking is Pending activation, Active or Completed; it is allowed after a paperwork-only plan (REQ-011-092)
   - Patient proceeds to payment

2. **Payment & Checkout**
   - Patient reviews order summary with template details (Screen 7)
   - Patient completes payment via checkout screen
   - System processes payment via FR-007 Payment Processing module
   - On success: Payment confirmed, request moves to automatic assignment
   - On failure: Error message, retry option

3. **Automatic Assignment** (REQ-011-054)
   - Payment confirmation triggers automatic assignment
   - System assigns to the original treatment provider if the provider is Active and has the aftercare participation setting on (a standing profile yes or no owned by FR-015; REQ-011-054)
   - If the provider does not participate or is not Active, system assigns to the Hairline aftercare team
   - Assigned provider receives notification and sees the patient's details from the payment (REQ-011-010)
   - Assignment is automatic at payment, so an add-on has no unassigned expiry; the 2-day reminder and 4-day escalation of REQ-011-090 run from the payment while the plan is not activated (REQ-011-053, REQ-011-090)
   - An admin rejection after payment still refunds in full (REQ-011-037)

4. **Provider Activation** (REQ-011-049)
   - Provider reviews patient's treatment history (pre-populated from treatment records)
   - Provider selects the aftercare template: the one purchased, or an alternative only if its price for the chosen pricing option equals the price already paid (REQ-011-047, REQ-011-100)
   - Provider customizes plan based on patient's treatment and package selection
   - Provider activates aftercare plan

5. **Patient Onboarding**
   - Patient receives activation notification
   - Patient gains access to aftercare dashboard (Screen 1)
   - Aftercare team begins monitoring

**Alternative Flows**:

- **B1a**: Original provider does not participate or is not Active (REQ-011-054)
  - System automatically assigns to Hairline aftercare team
  - Patient notified of provider assignment
  - The Aftercare Coordinator configures and activates the plan on Screen 14 Tab 4 (REQ-011-049)

- **B1b**: Payment fails (REQ-011-050)
  - Patient receives payment failure notification
  - Patient can retry payment with different method
  - Request becomes "Expired" when 48 hours pass without successful payment, counted from the failed payment (nothing was charged)

### Workflow 3: Patient Aftercare Activities (Ongoing Flow)

**Actors**: Patient, System, Aftercare Team

**Trigger**: Scheduled milestone/task becomes due or patient initiates activity

**Outcome**: Task completed, progress updated, and alerts/escalations generated when needed

**Main Flow**:

1. **Milestone-Based Tasks** (REQ-011-058)
   - System sends notification for upcoming tasks (scan/photo set, questionnaire)
   - Patient completes required activities
   - System tracks completion and progress

2. **Scan Upload (Head Scan Photo Set in V1)** (REQ-011-059)
   - Patient receives scan reminder notification
   - Patient captures head scan photo set (V1) using mobile app
   - System validates scan quality and provides feedback
   - Scan stored and made available to aftercare team

3. **Questionnaire Completion** (REQ-011-060)
   - Patient receives questionnaire notification
   - Patient completes milestone-specific questionnaire
   - System processes responses and flags concerning answers
   - Aftercare team reviews responses

4. **Progress Tracking** (REQ-011-027)
   - System automatically calculates overall recovery progress percentage as completed tasks over total tasks; the tasks counted are scan, questionnaire and education tasks, a Missed task counts as not done, and medication tick-offs are adherence tracking only and stay out of the percentage and out of milestone closing (REQ-011-023, REQ-011-024)
   - Patient views progress dashboard with real-time updates
   - System shows next upcoming tasks with countdown timers

**Alternative Flows**:

- **C1**: Patient misses scheduled task
  - System sends reminder notification
  - After 24 hours, system sets the Overdue flag on the task (Overdue is a flag, not a status) (REQ-011-026)
  - If still overdue after 48 hours counted from the task due date (the 24 hours above are part of those 48), the task escalates (REQ-011-025)
  - Aftercare team contacts patient
  - Time ends a milestone: a required task still not done at the end of its milestone becomes Missed, and the milestone closes on schedule (REQ-011-023)

- **C2**: Concerning symptoms reported
  - System flags case as "Urgent" (REQ-011-028): the plan carries an urgent flag and the time it was raised, set by an urgent questionnaire answer or by a manual flag (REQ-011-099)
  - Aftercare team immediately contacts patient
  - The assigned provider, or the coordinator when the Hairline team delivers, clears the flag with a note; clearing the flag is the response, and if it is not cleared within 2 hours of the raised time the system escalates the case to the admin (REQ-011-099)
  - Dashboards count the plans that have the flag set (REQ-011-099)

- **C3**: Plan completes (REQ-011-096)
  - At the end of the last milestone, or the end of the subscription term for a subscription (whichever is later), the system completes the plan
  - The system stops all reminders for the plan, including the scheduled progress reminders (REQ-011-088), and emits the completion event with the outcome "completed"; FR-006 reads the event and the booking moves to Completed
  - Every other ending follows the same closing rule: paperwork-only completion, a patient subscription cancellation once the paid period ends, and an admin cancellation each stop all reminders and emit the completion event with their own outcome (REQ-011-101)

- **C4**: Patient cancels the subscription (REQ-011-097)
  - Patient cancels from the plan payment screen (Screen 7)
  - Monthly subscription: care runs to the end of the paid month, later months are not charged, and the plan then becomes Cancelled with no refund; the closing rule applies once the paid period ends (REQ-011-101)
  - Paid in full upfront: care stops at the end of the current month and the unused full months are refunded pro rata; commission and provider payout follow the refund in the same proportion (REQ-011-083)

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
   - **Admin Editability**: Admin can edit ALL aftercare data including: (REQ-011-034)
     - Patient aftercare plans and milestones
     - Provider assignments and customizations
     - Medication schedules and instructions
     - Questionnaire responses and flags
     - Scan data and progress tracking
     - Communication logs and escalations

3. **Template Management**
   - Admin creates and modifies milestone templates
   - Admin configures questionnaire types and frequencies
   - Admin manages educational resources
   - **Admin Editability**: Admin can edit all template components: (REQ-011-035)
     - Milestone durations and descriptions
     - Scan schedules and frequencies
     - Questionnaire types and question content
     - Educational resources and activity restrictions

**Alternative Flows**:

- **D1**: Provider withdraws from aftercare (REQ-011-072)
  - Provider notifies admin of inability/unwillingness to continue aftercare for a patient
  - Admin receives notification and reviews the case
  - Admin can either:
    - Reassign the case to another suitable provider
    - Assign the case to the Hairline internal aftercare team
    - Mark the aftercare as cancelled (with reason); the closing rule applies (REQ-011-101)
  - All changes are logged, and the patient is notified of the new arrangement or cancellation

- **D2**: Provider performance issues
  - Admin identifies underperforming providers
  - Admin reassigns cases to better-performing providers
  - Admin provides feedback to provider

- **D3**: System-wide aftercare issues
  - Admin identifies patterns in patient complaints
  - Admin updates templates or processes
  - Admin communicates changes to all providers

- **D4**: Provider suspended or deactivated during Aftercare
  - Trigger: the assigned provider's `Suspended` or `Deactivated` status becomes effective under [FR-015 Alternative Flow A5 and Screen 4](../fr015-provider-management/prd.md#screen-4-provider-suspensiondeactivation-modal)
  - Scope covers every non-terminal Aftercare case assigned to that provider, including post-treatment (Workflow 1), add-on (Workflow 2b), and standalone aftercare for external-clinic patients (Workflow 2); standalone cases keep their intake data and payment history for admin follow-up
  - For standalone aftercare cases (Workflow 2), the case is not cancelled: the system records the provider-status cause (`ProviderSuspended` or `ProviderDeactivated`) and sets the independent `supportRequired` marker, and an admin reassigns the aftercare provider or the Hairline aftercare team through Screen 19 (REQ-011-014)
  - For treatment-linked cases (Workflow 1 and Workflow 2b), the aftercare case is not cancelled and the FR-006 booking stays `Aftercare`: the system records the provider-status cause and sets the `supportRequired` marker, and an admin reassigns the aftercare provider or team through Screen 19 (Alternative Flow D5) (REQ-011-073)
  - In both cases the provider loses aftercare actions on those cases (REQ-011-074)
  - The FR-010 completion milestone, aftercare plan, milestones, scans, questionnaire responses, medications, and communication history are retained read-only (REQ-011-074)
  - Patient/admin notifications follow FR-015 Screen 4; recovery continuity is routed to admins, who use this workflow's existing reassignment/recovery tools (reassign to another provider, assign to the Hairline aftercare team, or cancel the aftercare with a reason) and record audited resolution of the support marker (REQ-011-014)
  - Boundary: no automatic reassignment, refund, or restoration on provider reactivation; a later deactivation does not overwrite an earlier `ProviderSuspended` cause. Distinct from D1 provider withdrawal, which remains admin-reviewed without an automatic cancellation (REQ-011-014, REQ-011-074)

- **D5**: Provider fault during treatment-linked aftercare (aftercare reassignment) (REQ-011-075)
  - Trigger: the FR-006 booking is `Aftercare` and the assigned aftercare provider withdraws, drops out, is suspended or deactivated, or an admin decides the aftercare must move to another provider or to the Hairline aftercare team (FR-006 Alternative Flow B6); it also applies when an admin moves an `In Progress` booking to `Aftercare` after a provider fault (FR-006 Alternative Flow B7, FR-006 Screen 11)
  - The admin opens Screen 19 from Screen 14 or from the FR-006 admin booking detail and reassigns only the aftercare provider or team
  - The FR-006 booking stays `Aftercare` and the FR-010 treatment record stays unchanged; there is no new quote, acceptance, or payment (REQ-011-015, REQ-011-075)
  - The aftercare plan, milestones, scans, questionnaire responses, medications, and communication history move with the case unchanged; the previous provider keeps read-only access to the history it recorded and loses all aftercare actions (REQ-011-075)
  - The reassignment needs a mandatory reason and confirmation, is recorded in the audit trail, resolves the `supportRequired` marker when one is set, and sends the `aftercare.provider_reassigned` notice (recipients, content, and the mandatory status of the notice are defined by the FR-030 notification Rule, not here) (REQ-011-015, REQ-011-076)
  - The setup clock of REQ-011-090 restarts at the admin assignment and addresses the new assignee (REQ-011-090)
  - Boundary: a reassignment has no automatic refund and no refund ladder; for a standalone plan any refund is an admin manual refund (REQ-007-100); for a treatment-linked case reached through the FR-006 B7 decision, the refund and payout hold are those set on FR-006 Screen 11 (REQ-006-019); this flow never reassigns the treating provider of an earlier treatment stage (REQ-011-075)

- **D6**: Provider or coordinator proposes an extension or major change (REQ-011-098)
  - The assigned provider, or the coordinator when the Hairline team delivers, proposes an extension or major change to the plan with a reason
  - The admin approves or rejects it on the admin case screen (Screen 14); the patient is notified of the decision
  - When the coordinator proposes, the approving admin must be a different person (REQ-011-098)
  - If the change costs more, it takes effect only after the patient accepts and pays
  - A rejection leaves the plan unchanged, and the proposer is told why

- **D7**: Admin cancels the aftercare (REQ-011-101)
  - The admin uses Cancel Aftercare on Screen 14 Tab 4 with a mandatory reason; the cancellation is written to the audit trail
  - The closing rule applies: all reminders stop and the completion event carries the outcome "cancelled by an admin"; the booking then moves to Completed

## Screen Specifications

### Patient Platform Screens

#### Screen 1: Aftercare Dashboard

**Purpose**: Central hub for patient aftercare activities

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Overall Progress | derived | Yes | Percentage of completed tasks for current plan | 0–100%; auto-calculated | ENT-aftercare-plan.overall_progress |
| Current Milestone | text | Yes | Name and phase of current milestone | Must exist in plan | ENT-aftercare-plan.current_milestone |
| Days Remaining | number | No | Days left in current milestone | Non-negative integer | ENT-aftercare-plan.days_remaining |
| Next Task | text/datetime | No | Next upcoming task with countdown | Shows due date/time | ENT-aftercare-task.due_at, ENT-aftercare-task.task_type |
| Last Scan Upload | datetime/status | No | Timestamp and status of last scan upload | Valid status enum | ENT-aftercare-scan-artifact.uploaded_at, ENT-aftercare-scan-artifact.upload_status |
| Last Questionnaire | datetime | No | Timestamp of last questionnaire completion | ISO 8601 | ENT-aftercare-questionnaire-response.responded_at |
| Medication Adherence | percent | No | Adherence percentage for current period | 0–100% | ENT-aftercare-plan.medication_adherence |
| Upcoming Tasks | list | No | Next 7 days tasks | Items must exist in schedule | ENT-aftercare-task.due_at, ENT-aftercare-task.task_type |
| Upload Scan | action | Cond. | Action to capture/upload scan/photo set | Enabled if due | no graph field (control) |
| Complete Questionnaire | action | Cond. | Action to complete due questionnaire | Enabled if due | no graph field (control) |
| View Instructions | action | No | Open instructions content | Always available | no graph field (control) |
| Contact Support | action | No | Send a text message to the aftercare team; recorded as an aftercare communication entry (message, from the patient) and shown in the team's communication log; not an FR-012 conversation (REQ-011-102) | Always available while the plan is open | no graph field (control) |
| Messages | list | No | The patient's Contact Support messages and the aftercare team's messages and replies (REQ-011-103) | Chronological order | ENT-aftercare-communication-entry.sent_at, ENT-aftercare-communication-entry.sender_role |

**Business Rules**:

- Progress percentage = (completed tasks / total tasks) * 100 (REQ-011-027)
- Tasks counted in the percentage: scan uploads, questionnaires and education tasks; a milestone closes on schedule at its end, and a required task not done by then becomes Missed and counts as not done (REQ-011-023, REQ-011-027)
- Medication adherence is shown beside the progress as a separate figure; it is adherence tracking only and is left out of the percentage and out of milestone closing (REQ-011-027)
- Overdue tasks highlighted in red (REQ-011-086)
- Completed tasks shown in green (REQ-011-087)

**Notes**:

- Dashboard serves as the primary patient interface for aftercare engagement
- Real-time progress updates when tasks are completed
- Countdown timers for upcoming tasks create urgency and improve compliance
- Quick action buttons provide easy access to most common patient activities
- Mobile-first design optimized for smartphone screens

#### Screen 2: Scan Upload (V1 Photo Set)

**Purpose**: Patient uploads milestone scan media (V1 head scan photo sets; true 3D in V2)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Milestone Name | text | Yes | Current milestone name (read-only) | Display only | ENT-aftercare-milestone.name |
| Scan Due Date | datetime | Yes | Due date for this scan (read-only) | ISO 8601 format | ENT-aftercare-task.due_at |
| Days Overdue | number | No | Days past due date (if applicable) | Non-negative integer | ENT-aftercare-task.days_overdue |
| Scan Guidance | text | No | Instructions for proper scan capture | Display only | ENT-aftercare-milestone.scan_guidance |
| Camera Viewfinder | component | Yes | Live camera preview for photo set capture | Standard camera capture | no graph field (control) |
| Quality Indicator | status | Yes | Real-time scan quality feedback | Valid quality enum | ENT-aftercare-scan-artifact.quality_score |
| Capture Scan | action | Yes | Button to capture scan/photo set | Enabled when quality threshold met | ENT-aftercare-scan-artifact.media |
| Retake | action | Cond. | Button to retake if quality poor | Enabled when quality below threshold | no graph field (control) |
| Upload Progress | progress | No | Upload progress bar (0-100%) | 0-100% | no graph field (control) |
| Upload Status | message | No | Success/error message after upload | Valid status enum | ENT-aftercare-scan-artifact.upload_status |
| View Previous Scans | link | No | Link to view historical scans | Always available | no graph field (control) |

**Business Rules**:

- Scan must meet minimum quality threshold (REQ-011-059)
- Maximum file size: 50MB (REQ-011-059)
- Multiple scans within a milestone are supported per the configured scan schedule (e.g., every X days for Y repetitions); one upload is allowed per scheduled instance (REQ-011-059)
- Previous scans remain accessible for comparison (REQ-011-059)
- The upload uses the FR-002 media-only call with at least one photo, and the scan id is the idempotency key so a retried upload never creates a second scan; staged photos that are never attached to a scan are removed after 7 days (REQ-011-095, REQ-002-047, REQ-002-051)

**Notes**:

- V1: Guided photo capture (standardized photo set)
- V2 (future): Use ARKit (iOS) or ARCore (Android) for true 3D head scanning
- Quality validation should provide real-time feedback during capture
- Implement resumable upload for unreliable network connections
- Store scans in secure cloud storage

#### Screen 3: Questionnaire Completion

**Purpose**: Patient completes milestone-specific questionnaires

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Milestone Name | text | Yes | Current milestone and phase | Display only | ENT-aftercare-milestone.name |
| Questionnaire Set | text | Yes | Questionnaire set assigned to this milestone | Must exist in FR-025 catalog | ENT-aftercare-milestone.questionnaire_set_id |
| Questionnaire Set Version | text | Yes | Version of the set the response was started on (system-kept, not shown to the patient) | A response keeps the version it started on, also if the set is replaced later (REQ-011-071) | ENT-aftercare-questionnaire-response.questionnaire_set_version |
| Due Date | datetime | Yes | Questionnaire due date | ISO 8601 format | ENT-aftercare-task.due_at |
| Completion Status | status | Yes | Completed/Pending/Missed, plus an Overdue flag when past due | Valid status enum | ENT-aftercare-task.status, ENT-aftercare-task.overdue_flag |
| Questions | dynamic form | Yes | Full question list rendered from the assigned Questionnaire Set | Validation per question type (required fields, min/max ranges, option sets) | ENT-aftercare-questionnaire-response.answers |
| Save Draft | action | No | Save progress without submitting | Always available | ENT-aftercare-questionnaire-response.is_draft |
| Submit | action | Yes | Submit completed questionnaire | Enabled when all required fields complete | no graph field (control) |
| Warning Message | alert | No | Warning for concerning responses | Shown when responses trigger urgent flag per milestone rules | ENT-aftercare-questionnaire-response.urgent_flag |

**Business Rules**:

- All required fields must be completed (REQ-011-060)
- Concerning responses trigger urgent flag per milestone rules (REQ-011-028)
- Drafts saved automatically every 30 seconds (REQ-011-060)
- Patient may retake and resubmit the questionnaire while its task is open; the latest answer counts and earlier answers are kept in the history (REQ-011-060)

**Notes**:

- Questionnaire structure and questions managed in FR-025 (Medical Questionnaire Management)
- Dynamic form rendering based on the assigned Questionnaire Set questions from FR-025
- Auto-save draft functionality to prevent data loss
- Real-time validation for concerning responses (triggers urgent flag immediately)
- Mobile-optimized form layout for easy completion on small screens

#### Screen 4: Medication Schedule

**Purpose**: Patient views and tracks medication adherence

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Medication Name | text | Yes | Name of medication | Must be an Active medication template from the admin-managed list owned by FR-024 (see FR-024); the plan keeps its own copy of the text, so a later template edit or deactivation does not change it (REQ-011-089) | ENT-aftercare-medication.name |
| Dosage | text | Yes | Dosage amount and unit | Valid dosage format | ENT-aftercare-medication.dosage |
| Frequency | text | Yes | Frequency (e.g., "2x daily", "Every 8 hours") | Valid frequency format | ENT-aftercare-medication.frequency |
| Special Instructions | text | No | Additional instructions from provider | Max 500 chars | ENT-aftercare-medication.special_instructions |
| Start Date | date | Yes | Medication start date | ISO 8601 format | ENT-aftercare-medication.start_date |
| End Date | date | Yes | Medication end date | Must be after start date | ENT-aftercare-medication.end_date |
| Today's Doses | list | Yes | Upcoming doses for today with times | Sorted by time | ENT-aftercare-dose.scheduled_time |
| Dose Time | time | Yes | Scheduled time for each dose | HH:MM format | ENT-aftercare-dose.scheduled_time |
| Mark as Taken | action | Yes | Button to mark dose as taken | Enabled when dose time reached | ENT-aftercare-dose.taken_at |
| Missed Dose Indicator | status | No | Visual indicator for missed doses | Shown if dose not taken within 2 hours | ENT-aftercare-dose.missed |
| Weekly Adherence | percent | Yes | Percentage of doses taken this week | 0-100%; auto-calculated | ENT-aftercare-plan.weekly_medication_adherence |
| Missed Doses Count | number | Yes | Total missed doses count | Non-negative integer | ENT-aftercare-plan.missed_doses_count |
| View History | link | No | Link to view full adherence history | Always available | no graph field (control) |

**Business Rules**:

- Medications prescribed by provider during aftercare setup (REQ-011-061)
- Adherence calculated as (taken doses / total doses) * 100 (REQ-011-061)
- Adherence is tracking only: it does not block a milestone from closing and is not part of the overall progress percentage (REQ-011-023, REQ-011-027)
- Missed doses trigger reminder notifications (REQ-011-058)
- History available for entire aftercare period (REQ-011-061)

**Notes**:

- Medications defined during aftercare plan setup (Screen 10)
- Push notifications for upcoming doses follow the patient notification preferences owned by FR-030; FR-011 has no aftercare-specific setting for them
- History view shows complete timeline of all medications and adherence
- Visual indicators (colors/icons) for easy recognition of adherence status
- Support for multiple medications with overlapping schedules

#### Screen 5: Educational Resources

**Purpose**: Patient accesses milestone-specific educational content

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Resource Category | text | Yes | Category (Videos, Guides, FAQs, Help) | Valid category enum | ENT-aftercare-resource.category |
| Resource Title | text | Yes | Title of educational resource | Max 200 chars | ENT-aftercare-resource.title |
| Resource Description | text | No | Description of resource content | Max 1000 chars | ENT-aftercare-resource.description |
| Resource Type | text | Yes | Type (video, PDF, webpage, etc.) | Valid resource type enum | ENT-aftercare-resource.resource_type |
| Resource URL | url | Yes | URL or file path to resource | Valid URL or file path | ENT-aftercare-resource.url |
| Duration | time | Cond. | Duration in minutes (for videos) | Valid time format | ENT-aftercare-resource.duration_minutes |
| File Size | size | Cond. | File size for downloadable resources | Display only | ENT-aftercare-resource.file_size_bytes |
| Mark as Viewed | checkbox | No | Checkbox to mark resource as viewed | Boolean | ENT-aftercare-resource-view.viewed_at |
| View/Download | action | Yes | Button to view or download resource | Always available | no graph field (control) |
| Resources Viewed Count | number | Yes | Count of viewed resources | Non-negative integer | ENT-aftercare-milestone.resources_viewed_count |
| Total Resources | number | Yes | Total resources in current milestone | Non-negative integer | ENT-aftercare-milestone.total_resources |
| Completion Percentage | percent | Yes | Percentage of resources viewed | 0-100%; auto-calculated | ENT-aftercare-milestone.resource_completion_percentage |
| Mark All as Viewed | action | No | Button to mark all resources as viewed | Enabled when resources available | no graph field (control) |

**Business Rules**:

- Resources specific to current milestone (REQ-011-062)
- Viewing progress tracked for compliance (REQ-011-062)
- Resources remain accessible throughout aftercare (REQ-011-062)
- New resources added by admin appear automatically (REQ-011-062)

**Notes**:

- Resources managed in Screen 16 (Milestone Template Management) by admin
- Support for various media types: videos (streaming), PDFs (download), web pages (in-app browser)
- Progress tracking helps ensure patients review critical educational content
- Resources organized by category for easy navigation
- Offline viewing capability for downloaded resources

#### Screen 6: Aftercare Service Purchase

**Purpose**: Patient purchases aftercare service (post-treatment add-on or standalone)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Service Type | radio | Yes | Post-Treatment Add-On or Standalone Service | Enum: "post_treatment", "standalone" | ENT-aftercare-request.service_type |
| Treatment Information | component | Cond. | Treatment details (if post-treatment add-on) | Auto-populated for post_treatment type | ENT-quote.treatment_id |
| External Treatment Details | form | Cond. | Treatment info form (if standalone) | Required for standalone type | ENT-aftercare-request.treatment_date, ENT-aftercare-request.treatment_type, ENT-aftercare-request.treating_clinic, ENT-aftercare-request.documentation |
| Treatment Date | date | Cond. | Date treatment performed | ISO 8601; required for standalone | ENT-aftercare-request.treatment_date |
| Treatment Type | select | Cond. | Type of treatment received | Value from the admin-managed treatment catalog; required for standalone | ENT-aftercare-request.treatment_type |
| Treating Clinic | text | Cond. | Name of external clinic | Max 200 chars; required for standalone | ENT-aftercare-request.treating_clinic |
| Upload Treatment Documentation | file | No | Optional treatment documentation | Max 10MB; PDF/JPG/PNG | ENT-aftercare-request.documentation |
| Available Aftercare Services | list | Yes | List of purchasable aftercare templates | Filtered by treatment type compatibility | no graph field (list of the rows below) |
| Service Name | text | Yes | Template name (e.g., "Standard 6-Month FUE Aftercare") | Display only | ENT-aftercare-template.name |
| Service Description | text | Yes | Template description with features | Display only | ENT-aftercare-template.service_description |
| Duration | text | Yes | Service duration (from template) | Display only | ENT-aftercare-template.duration |
| Milestones Included | list | Yes | Milestone summary | Display only | ENT-aftercare-milestone.name |
| Features Included | list | Yes | Features (scan uploads, questionnaires, etc.) | Display only | ENT-aftercare-template.features_included |
| Pricing Options | component | Yes | Available pricing for this template | Based on template configuration | ENT-aftercare-template-price.fixed_price, ENT-aftercare-template-price.monthly_price |
| Pricing Option | radio | Cond. | Fixed Price or Monthly Subscription | Based on template's pricing model | ENT-aftercare-request.pricing_option |
| Price (Fixed) | currency | Cond. | One-time payment amount | Shown if Fixed or Both | ENT-aftercare-template-price.fixed_price |
| Price (Monthly) | currency | Cond. | Monthly subscription amount | Shown if Subscription or Both | ENT-aftercare-template-price.monthly_price |
| Total Amount | currency | Yes | Total amount for selected pricing option | Auto-calculated | ENT-aftercare-request.total |
| Currency | text | Yes | Patient's currency (auto-detected) | Based on location | ENT-aftercare-request.currency |
| Selected Service | radio | Yes | User selection of template | Required before checkout | ENT-aftercare-request.template_id |
| Selected Pricing Option | radio | Cond. | If template offers both pricing models | Required if Both available | ENT-aftercare-request.pricing_option |
| Current Concerns | textarea | No | Patient's current concerns or symptoms | Max 2000 chars | ENT-aftercare-request.current_concerns |
| Upload Photos | file[] | No | Optional photos of current condition | Max 5 files; 10MB each; JPG/PNG | ENT-aftercare-request.photos |
| Booking | id | Cond. | Booking the add-on belongs to (post-treatment add-on only; empty for standalone) | System-filled; add-on refused while a plan for the same booking is Active or Completed (REQ-011-092) | ENT-aftercare-request.booking_id |
| Accepted Quote | id | Cond. | Quote of that booking (post-treatment add-on only; empty for standalone) | System-filled | ENT-aftercare-request.quote_id |
| Request Source | text | Yes | How the request started: add-on, standalone, or conversion from FR-038 monitoring | System-set; see the conversion rules below (REQ-011-093) | ENT-aftercare-request.source |
| Monitoring Case | id | Cond. | FR-038 monitoring case the request was converted from | Conversion only; pre-filled | ENT-aftercare-request.monitoring_case_id |
| Monitoring Scan or Photo Set | id | Cond. | Scan or photo set carried over from the monitoring case | Conversion only; pre-filled | ENT-aftercare-request.scan_set_id |
| Monitoring Report File | file | Cond. | Report file carried over from the monitoring case | Conversion only; pre-filled | ENT-aftercare-request.report_file_id |
| Request Key | text | Cond. | Idempotency key of the conversion | System-set; a repeated key returns the existing request (REQ-011-093) | ENT-aftercare-request.idempotency_key |
| Proceed to Payment | action | Yes | Post-treatment add-on: button to proceed to checkout. Standalone: submits the request; the patient pays later, after the admin has assigned a provider and the provider has configured the plan (Workflow 2) | Enabled when service selected | no graph field (control) |

**Business Rules**:

- Only templates marked "Available for Purchase" are shown (REQ-011-046)
- Templates filtered by treatment type compatibility (FUE templates for FUE patients, etc.) (REQ-011-046)
- Pricing shown in patient's local currency (based on location detection) (REQ-011-041)
- If template offers both Fixed and Subscription, patient chooses preferred pricing option (REQ-011-042)
- Service name uses template name for consistency across provider and patient views (REQ-011-046)
- Post-treatment add-on only available within 90 days of Hairline treatment completion (REQ-011-044)
- No add-on while a plan for the same booking is Active or Completed; an add-on is allowed after a paperwork-only completion (REQ-011-092)
- A request converted from FR-038 monitoring is a standalone request with the source, monitoring case, scan or photo set and report file pre-filled; the patient confirms the treatment details and chooses a template as in any standalone request (REQ-011-093, REQ-011-094)
- A repeated conversion with the same idempotency key returns the existing request; a conversion is refused once the monitoring case is completed; when the request fails or is abandoned, the patient returns to FR-038 Screen 6 with the draft intact (REQ-011-093, REQ-011-094, REQ-038-068)
- Treatment documentation optional but helps provider customize plan

**Notes**:

- Service offerings are directly pulled from aftercare templates (Screen 16)
- Each template defines its own pricing, features, and duration
- Visual presentation similar to treatment package selection for consistency
- Pricing transparency with clear breakdown of what's included
- The patient chooses the service type (post-treatment add-on or standalone); a Hairline-treated patient may also choose standalone. The post-treatment add-on is offered only within 90 days of Hairline treatment completion

#### Screen 7: Aftercare Payment & Checkout

**Purpose**: Patient completes payment for aftercare service

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Order Summary | component | Yes | Selected aftercare service details | Display only | ENT-aftercare-template.name, ENT-aftercare-template.duration, ENT-aftercare-request.pricing_option, ENT-aftercare-request.subtotal, ENT-aftercare-request.tax, ENT-aftercare-request.total |
| Final Template | text | Cond. | Template the provider finally chose when it differs from the requested one (standalone) | Display only; offers the pricing option the patient chose (REQ-011-100) | ENT-aftercare-request.final_template_id |
| Payment Due By | datetime | Cond. | Time by which the patient must pay (standalone): 48 hours from the payment-due notice | Display only; after this time the request becomes Expired (REQ-011-050) | ENT-aftercare-request.payment_due_at |
| Service Name | text | Yes | Selected template name | Display only | ENT-aftercare-template.name |
| Duration | text | Yes | Service duration | Display only | ENT-aftercare-template.duration |
| Pricing Option Selected | text | Yes | Fixed or Monthly Subscription | Display only | ENT-aftercare-request.pricing_option |
| Subtotal | currency | Yes | Service price (from template); the platform fee is taken out of this price and is not shown as an extra charge | Display only | ENT-aftercare-request.subtotal |
| Tax | currency | Yes | Applicable tax | Display only; location-based | ENT-aftercare-request.tax |
| Total Amount | currency | Yes | Final amount to pay | Display only | ENT-aftercare-request.total |
| Monthly Payment Details | component | Cond. | Breakdown of subscription payments | Shown if subscription selected | ENT-aftercare-request.monthly_amount, ENT-aftercare-request.number_of_months, ENT-aftercare-request.total_subscription_amount |
| Monthly Amount | currency | Yes | Amount charged per month | Display only | ENT-aftercare-request.monthly_amount |
| Number of Months | number | Yes | Total subscription duration | Display only | ENT-aftercare-request.number_of_months |
| Total Subscription Amount | currency | Yes | Monthly amount × number of months | Display only | ENT-aftercare-request.total_subscription_amount |
| Payment Method Selection | radio | Yes | Credit/Debit Card, PayPal, etc. | Valid payment method enum | ENT-aftercare-request.payment_method |
| Card Number | text | Cond. | Credit/debit card number | Valid card format; required if card payment | no graph field (card input) |
| Expiry Date | text | Cond. | Card expiry date | MM/YY format; required if card payment | no graph field (card input) |
| CVV | text | Cond. | Card security code | 3-4 digits; required if card payment | no graph field (card input) |
| Cardholder Name | text | Cond. | Name on card | Max 200 chars; required if card payment | no graph field (card input) |
| Billing Address | component | Yes | Billing address details | Required for all payment methods | ENT-aftercare-request.billing_address |
| Street Address | text | Yes | Street address | Max 500 chars | ENT-aftercare-request.billing_address |
| City | text | Yes | City | Max 100 chars | ENT-aftercare-request.billing_address |
| State/Province | text | Yes | State/province | Max 100 chars | ENT-aftercare-request.billing_address |
| Postal Code | text | Yes | Postal/ZIP code | Valid postal format | ENT-aftercare-request.billing_address |
| Country | select | Yes | Country | Valid country enum | ENT-aftercare-request.billing_address |
| Terms & Conditions | checkbox | Yes | Agreement to terms | Boolean; must be checked | ENT-aftercare-request.terms_accepted |
| Privacy Policy | checkbox | Yes | Agreement to privacy policy | Boolean; must be checked | ENT-aftercare-request.privacy_accepted |
| Payment Processing | status | No | Payment processing status | Display during payment | ENT-aftercare-request.payment_status |
| Complete Payment | action | Yes | Button to submit payment | Enabled when all fields valid; when the final price differs from the requested price the patient must first accept the new price (REQ-011-100) | no graph field (control) |
| Accept New Price | action | Cond. | Accept the final template's price and continue to payment | Shown only when the final price differs from the requested price (REQ-011-100) | no graph field (control) |
| Cancel Request | action | Cond. | Cancel the request at no charge when the new price is not acceptable | Shown only when the final price differs; the request becomes Rejected with the system reason cancelled by patient (REQ-011-100) | ENT-aftercare-request.rejection_reason |
| Cancel Subscription | action | Cond. | Cancel an active subscription or a plan paid in full | Shown on the plan payment screen of an Active plan; outcome per REQ-011-097 | no graph field (control) |

**Business Rules**:

- Payment integration with FR-007 (Payment Processing module) (REQ-011-063)
- Support for multiple payment methods (credit/debit cards, PayPal, local payment methods) (REQ-011-063)
- Secure payment processing with PCI compliance (REQ-011-063)
- Payment confirmation activates the aftercare plan for a standalone request (Workflow 2, after the provider has configured the plan) and triggers automatic assignment for a post-treatment add-on (Workflow 2b) (REQ-011-018, REQ-011-063)
- The platform fee is one amount taken from the aftercare price; it is never added on top of the patient's total (REQ-011-040)
- Failed payments allow retry with different payment method (REQ-011-050)
- Standalone: the request is "Payment due" from the payment-due notice; the patient has 48 hours from that notice, and with no successful payment by then the request becomes Expired, with nothing charged and nothing to refund (REQ-011-050)
- If the final template's price differs from the requested price, the order summary shows the final template and the patient accepts the new price before paying or cancels at no charge (REQ-011-100)
- Cancelling a subscription: a monthly subscription runs to the end of the paid month with no refund; a plan paid in full stops at the end of the current month with a pro-rata refund of the unused full months; commission and provider payout follow in the same proportion (REQ-011-097, REQ-011-083)
- Any payment already taken is refunded automatically if the request is rejected by admin (REQ-011-037)
- Subscription payments charged automatically on monthly basis (REQ-011-043)
- First subscription payment charged immediately; subsequent payments on monthly anniversary (REQ-011-043)

**Notes**:

- Integrate with Stripe payment gateway (see Integration and Security Rules: Payment Gateway - Stripe)
- Order summary clearly shows all fees and charges with transparent breakdown
- Payment method selection supports region-specific payment options
- Secure payment form with SSL encryption and PCI compliance
- Payment confirmation email sent immediately after successful payment
- Payment status tracked and visible in patient dashboard
- For subscriptions, clear communication of recurring payment schedule
- Subscription management interface for patients to view/cancel subscriptions (cancellation outcome per REQ-011-097)

### Provider Platform Screens

#### Screen 8: Aftercare Cases List

**Purpose**: Provider views all patients in aftercare (similar to existing "In Progress" list)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Patient ID | column | Yes | Unique identifier (e.g., HPID2509-0001) | Searchable; sortable | ENT-aftercare-plan.patient_id |
| Patient Name | column | Yes | Avatar + full name + email | PII per role; sortable | ENT-patient.name, ENT-patient.email |
| Phone Number | column | No | Contact number | E.164 format | ENT-patient.phone |
| Age | column | No | Patient age | Integer 18–100 | ENT-patient.age |
| Problem | column | No | Treatment area (Hair/Both/Beard) | Value from the catalog-driven list (per FR-003) | ENT-inquiry.treatment_area_id |
| Treatment & Package | column | Yes | Treatment + package | Read-only | ENT-quote.treatment_id, ENT-subquote.package_snapshot |
| Aftercare Start Date | column | Yes | Start date | ISO 8601; sortable | ENT-aftercare-plan.activated_at |
| Current Milestone | column | Yes | Phase name | Must exist in plan | ENT-aftercare-plan.current_milestone |
| Progress | column | Yes | Visual progress (e.g., 3/5 days) | Derived; non-negative | ENT-aftercare-plan.overall_progress |
| Med Alerts | column | Yes | Critical/Standard/None | Enum with color coding | ENT-aftercare-plan.medication_alert_level |
| Last Activity | column | No | Time since last interaction | Relative format | ENT-aftercare-plan.last_activity_at |
| Action | column | Yes | View/Edit/Message/Escalate | RBAC enforced | no graph field (control) |
| Search | control | No | Search aftercare cases | Debounced input | no graph field (control) |
| Filters | control | No | Provider/Milestone/Status/Date range | Valid enums/ranges | no graph field (control) |
| Pagination | control | No | Page controls and size | Standard UX pattern | no graph field (control) |

**Business Rules**:

- Only shows patients assigned to this provider (REQ-011-064)
- Overdue cases shown with amber indicators (REQ-011-064)
- Patient names are fully visible to the assigned provider from assignment in the standalone flow, and from payment in the post-treatment add-on flow where assignment follows payment (REQ-011-010)
- Progress calculated automatically by system (REQ-011-064)
- All data editable by admin (admin override capability) (REQ-011-034)

**Notes**:

- Similar table structure to existing "In Progress" treatment list for consistency
- Color-coded medication alerts (red=critical, yellow=standard, green=none) provide quick visual status
- Filters allow providers to focus on specific patient groups (by milestone, status, date range)
- Sortable columns help providers prioritize cases (e.g., sort by Last Activity to find inactive patients)
- Action menu provides quick access to common provider tasks without navigating away

#### Screen 9: Patient Aftercare Details

**Purpose**: Provider views comprehensive patient aftercare progress with full historical context

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Patient ID | text | Yes | Unique patient identifier | Display only | ENT-aftercare-plan.patient_id |
| Treatment Details | text | Cond. | Treatment info (if Hairline-treated patient) | Display only; N/A for standalone | ENT-quote.treatment_id |
| Aftercare Start Date | date | Yes | When aftercare began | ISO 8601 format | ENT-aftercare-plan.activated_at |
| Aftercare Duration | text | Yes | Planned duration (e.g., "12 months") | Display only | ENT-aftercare-plan.duration |
| Assigned Template | text | Yes | Aftercare template name | Display only | ENT-aftercare-plan.template_id |
| Custom Instructions | text | No | Provider's patient-specific instructions | Max 2000 chars; editable | ENT-aftercare-plan.custom_instructions |
| Current Milestone | text | Yes | Current milestone name and phase | Must exist in plan | ENT-aftercare-plan.current_milestone |
| Overall Progress | percent | Yes | Completion percentage (auto-calculated) | 0-100% | ENT-aftercare-plan.overall_progress |
| Milestone Timeline | component | Yes | Visual timeline of all milestones | Display only | no graph field (display component) |
| Upcoming Tasks | list | Yes | List of next due tasks | Sorted by due date | ENT-aftercare-task.due_at |
| 3D Scan History | list | Yes | All uploaded scans with dates and quality | Chronological order | no graph field (list of the rows below) |
| Scan Upload Date | datetime | Yes | Date scan was uploaded | ISO 8601 format | ENT-aftercare-scan-artifact.uploaded_at |
| Scan Quality Score | number | Yes | Quality score (0-100) | Integer 0-100 | ENT-aftercare-scan-artifact.quality_score |
| Questionnaire Responses | list | Yes | All questionnaire completions | Chronological order | ENT-aftercare-questionnaire-response.answers |
| Response Date | datetime | Yes | Date questionnaire was submitted | ISO 8601 format | ENT-aftercare-questionnaire-response.responded_at |
| Questionnaire Set | text | Yes | Questionnaire set completed | Display only | ENT-aftercare-questionnaire-response.questionnaire_set_id |
| Medication Adherence History | list | Yes | Historical adherence data | Chronological order | ENT-aftercare-plan.medication_adherence |
| Adherence Period | date range | Yes | Start and end date of the adherence period, calculated from the medication doses | Calculated; valid date range | ENT-aftercare-plan.adherence_period |
| Adherence Percentage | percent | Yes | Percentage for that period | 0-100% | ENT-aftercare-plan.medication_adherence |
| Communication Log | list | Yes | All communications with aftercare team | Chronological order | no graph field (list of the rows below) |
| Message Date | datetime | Yes | Date/time of message | ISO 8601 format | ENT-aftercare-communication-entry.sent_at |
| Message Type | text | Yes | Type (message, escalation, alert) | Valid message type enum | ENT-aftercare-communication-entry.entry_type |
| Adjust Plan | action | No | Button to modify aftercare plan | Enabled for assigned patients | no graph field (control) |
| Request Additional Scan | action | No | Button to request extra scan | Always available | no graph field (control) |
| Contact Aftercare Team | action | No | Button to send message | Always available | no graph field (control) |
| Escalate Case | action | No | Button to escalate urgent case | Always available | no graph field (control) |
| Urgent Flag | indicator | No | Shows when the plan is flagged urgent and since when | Display only; clearing needs a note (REQ-011-099) | ENT-aftercare-plan.urgent_flag, ENT-aftercare-plan.urgent_raised_at |
| Clear Urgent Flag | action | Cond. | Clear the urgent flag with a note (assigned provider) | Shown only while the flag is set; note required; clearing it is the response (REQ-011-099) | no graph field (control) |
| Withdraw from Aftercare | action | No | Provider tells the admin they cannot continue aftercare for this patient | Reason required; admin reviews the case (REQ-011-072) | no graph field (control) |

**Business Rules**:

- **Data Persistence**: Screen displays all historical data from patient's entire journey (inquiry → treatment → aftercare) without removing older data, providing complete context (REQ-011-065)
- **Dual Case Handling**:
  - **Hairline-treated patients**: Shows complete lifecycle data including pre-treatment inquiry, quote, treatment details, and aftercare (REQ-011-065)
  - **Standalone aftercare patients**: Shows only aftercare-specific data with initial intake information provided during standalone request (REQ-011-065)
- Full patient details are visible to the assigned provider from assignment (standalone) or from payment (post-treatment add-on, where assignment follows payment) (REQ-011-010)
- All activities logged with timestamps (REQ-011-065)
- Provider can modify plan only for their assigned patients (REQ-011-065)
- Escalation creates audit trail (REQ-011-065)
- Withdraw from Aftercare notifies the admin, who reviews the case and reassigns it, assigns the Hairline team or cancels it with a reason (Alternative Flow D1) (REQ-011-072)

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

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| **Step 1: Template Selection** | | | | |  |
| Available Templates | list | Yes | List of admin-created templates | Must have at least one template | no graph field (list of the rows below) |
| Template Name | text | Yes | Selected template name | Must exist in template catalog | ENT-aftercare-template.name |
| Template Description | text | Yes | Template description | Display only | ENT-aftercare-template.description |
| Treatment Type | text | Yes | Treatment type compatibility | Valid treatment type enum | ENT-aftercare-template.treatment_type |
| Duration | text | Yes | Duration (e.g., "12 months") | Display only | ENT-aftercare-template.duration |
| Milestone Count | number | Yes | Number of milestones in template | Display only | ENT-aftercare-template.milestone_count |
| Template Preview | component | No | Preview of template details | Display only | no graph field (display component) |
| Select Template | action | Yes | Button to select template | Enabled when template selected | no graph field (control) |
| **Step 2: Milestone Customization** | | | | |  |
| Milestone List | list | Yes | All milestones from selected template | Must have at least one milestone | no graph field (list of the rows below) |
| Milestone Name | text | Yes | Name of milestone | Max 200 chars | ENT-aftercare-milestone.name |
| Milestone Duration | number | Yes | Duration in days | Positive integer; editable | ENT-aftercare-milestone.duration_days |
| 3D Scan Frequency | text | Yes | Frequency of scans (e.g., "Weekly") | Valid frequency enum; editable | ENT-aftercare-milestone.scan_frequency |
| Questionnaire Set | select | Yes | Questionnaire set assigned to this milestone | Must exist in FR-025 catalog | ENT-aftercare-milestone.questionnaire_set_id |
| Questionnaire Frequency | text | Yes | Frequency of questionnaires | Valid frequency enum; editable | ENT-aftercare-milestone.questionnaire_frequency |
| Educational Resources | list | Yes | Resources assigned to milestone | May be empty | ENT-aftercare-resource.title |
| Activity Restrictions | text | No | Restrictions for this milestone | Max 500 chars; editable | ENT-aftercare-milestone.activity_restrictions |
| Modify Duration | action | No | Button to modify milestone duration | Always available | no graph field (control) |
| Custom Instructions | text | No | Instructions specific to this milestone | Max 1000 chars | ENT-aftercare-milestone.instructions |
| Override Restrictions | action | No | Button to override activity restrictions | Always available | no graph field (control) |
| **Step 3: Medication Setup** | | | | |  |
| Medication Name | select | Yes | Medication picked only from the admin-managed medication list (the FR-024 medication templates); no free-text medication names | Must be an Active medication template owned by FR-024 (see FR-024); the plan keeps its own copy of the text, so a later template edit or deactivation does not change it (REQ-011-089) | ENT-aftercare-medication.name |
| Dosage | text | Yes | Dosage amount and unit | Valid dosage format | ENT-aftercare-medication.dosage |
| Frequency | text | Yes | Frequency (e.g., "2x daily") | Valid frequency format | ENT-aftercare-medication.frequency |
| Start Date | date | Yes | Medication start date | ISO 8601 format; must be today or future | ENT-aftercare-medication.start_date |
| End Date | date | Yes | Medication end date | ISO 8601 format; must be after start date | ENT-aftercare-medication.end_date |
| Special Instructions | text | No | Additional instructions | Max 500 chars | ENT-aftercare-medication.special_instructions |
| Add Medication | action | Yes | Button to add medication to list | Enabled when all fields complete | no graph field (control) |
| Medication List | list | Yes | List of all added medications | May be empty | no graph field (list of the rows below) |
| Medication Timeline | component | Yes | Visual timeline of all medications | Display only | no graph field (display component) |
| **Step 4: Custom Instructions** | | | | |  |
| General Instructions | textarea | No | Free-text area for provider notes | Max 2000 chars | ENT-aftercare-plan.general_instructions, ENT-aftercare-plan.custom_instructions |
| Milestone Instructions | textarea[] | No | Instructions per milestone | Max 1000 chars per milestone | ENT-aftercare-milestone.instructions |
| Emergency Contact | text | No | Provider contact information | Max 200 chars | ENT-aftercare-plan.emergency_contact |
| Special Considerations | textarea | No | Patient-specific notes | Max 1000 chars | ENT-aftercare-plan.special_considerations |
| **Step 5: Review and Confirm** | | | | |  |
| Plan Summary | component | Yes | Complete aftercare plan overview | Display only | no graph field (display component) |
| Patient Information | component | Yes | Confirmation of patient details | Display only | ENT-aftercare-plan.patient_id |
| Provider Information | component | Yes | Provider contact details | Display only | ENT-aftercare-plan.provider_id |
| Activate Plan | action | Yes | Button to activate aftercare plan | Enabled when all steps complete | no graph field (control) |

**Business Rules**:

- All steps must be completed before activation (REQ-011-066)
- Provider can go back to previous steps (REQ-011-066)
- System validates all required fields (REQ-011-066)
- Admin can edit any step after activation (REQ-011-066)
- Patient receives notification upon activation (REQ-011-066)
- Setup starts automatically; Activate Plan (the provider's confirmation) activates the plan, and an admin can activate it instead when setup stalls (REQ-011-055, REQ-011-019)
- In the standalone flow, completing the plan sets the request to Payment due; the patient then pays and the plan activates on payment as set out in Workflow 2 (REQ-011-050)

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

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Selected Template | text | Yes | Current template name | Display only | ENT-aftercare-plan.template_id |
| Milestone Structure | component | Yes | Visual structure with progress indicators | Display only | ENT-aftercare-milestone.name |
| Medication Schedule | component | Yes | Visual timeline of medications | Display only | ENT-aftercare-medication.name |
| Custom Instructions | textarea | No | Current custom instructions | Max 2000 chars; editable | ENT-aftercare-plan.custom_instructions |
| Modify Medication Schedule | action | Cond. | Button to modify medications (Provider) | Enabled for providers | no graph field (control) |
| Update Custom Instructions | action | Cond. | Button to update instructions (Provider) | Enabled for providers | no graph field (control) |
| Add Milestone Notes | action | Cond. | Button to add milestone-specific notes (Provider) | Enabled for providers | no graph field (control) |
| Request Duration Change | action | Cond. | Button to request milestone duration change (Provider) | Enabled for providers | no graph field (control) |
| Propose Extension or Major Change | action | Cond. | Propose an extension or major change with a reason (assigned provider; the coordinator uses Screen 14 Tab 4 when the Hairline team delivers) | Reason required; goes to the admin for approval (REQ-011-098) | no graph field (control) |
| Change Milestone Structure | action | Cond. | Button to modify milestones (Admin only) | Enabled for admins | no graph field (control) |
| Modify Template Assignment | action | Cond. | Button to change template (Admin only) | Enabled for admins | no graph field (control) |
| Override Settings | action | Cond. | Button to override any settings (Admin only) | Enabled for admins | no graph field (control) |
| Reassign Provider | action | Cond. | Button to reassign case (Admin only) | Enabled for admins | no graph field (control) |
| Change Reason | textarea | Yes | Required reason for changes | Max 500 chars; required | ENT-aftercare-audit-entry.reason |
| Change Timestamp | datetime | Yes | When change was made | Auto-generated | ENT-aftercare-audit-entry.changed_at |
| Changed By | text | Yes | User who made the change | Auto-populated | ENT-aftercare-audit-entry.changed_by |
| Approval Status | status | Yes | Status (Proposed/Approved/Rejected) | Valid status enum | ENT-aftercare-audit-entry.approval_status |
| Change History | list | Yes | Historical list of all changes | Chronological order | ENT-aftercare-audit-entry.plan_id |

**Business Rules**:

- Provider changes logged and tracked (REQ-011-067)
- Admin changes override provider settings (REQ-011-067)
- Major changes and extensions require admin approval: the admin approves or rejects on the admin case screen, the patient is notified, extra cost needs the patient's acceptance and payment, and a rejection leaves the plan unchanged and tells the proposer why (REQ-011-067, REQ-011-098)
- All changes logged with reason and timestamp (REQ-011-067)
- Patient notified of approved changes (REQ-011-067)
- Change history maintained for audit trail (REQ-011-067)

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

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Patient Name | text | Yes | Full patient name | Display only | ENT-patient.name |
| Current Milestone | text | Yes | Current milestone name and phase | Display only | ENT-aftercare-plan.current_milestone |
| Overall Progress | percent | Yes | Completion percentage (auto-calculated) | 0-100% | ENT-aftercare-plan.overall_progress |
| Days Remaining | number | Yes | Days left in current milestone | Non-negative integer | ENT-aftercare-plan.days_remaining |
| Next Upcoming Tasks | list | Yes | List of next due tasks | Sorted by due date | ENT-aftercare-task.due_at |
| Milestone Timeline | component | Yes | Visual timeline of all milestones | Display only | no graph field (display component) |
| Completed Milestones | indicator | Yes | Green indicators for completed | Display only | ENT-aftercare-milestone.status |
| Current Milestone Indicator | indicator | Yes | Blue indicator for current | Display only | ENT-aftercare-milestone.status |
| Upcoming Milestones | indicator | Yes | Gray indicators for upcoming | Display only | ENT-aftercare-milestone.status |
| Overdue Tasks Indicator | indicator | Yes | Red indicators for overdue | Display only | ENT-aftercare-task.overdue_flag |
| 3D Scan Status | status | Yes | Completed/Pending/Missed with dates, plus an Overdue flag when past due | Valid status enum | ENT-aftercare-task.status, ENT-aftercare-task.overdue_flag |
| Scan Due Date | datetime | Yes | Due date for scan | ISO 8601 format | ENT-aftercare-task.due_at |
| Questionnaire Status | status | Yes | Completed/Pending/Missed with dates, plus an Overdue flag when past due | Valid status enum | ENT-aftercare-task.status, ENT-aftercare-task.overdue_flag |
| Questionnaire Due Date | datetime | Yes | Due date for questionnaire | ISO 8601 format | ENT-aftercare-task.due_at |
| Medication Adherence | percent | Yes | Adherence percentage | 0-100% | ENT-aftercare-plan.medication_adherence |
| Missed Doses | number | Yes | Count of missed doses | Non-negative integer | ENT-aftercare-plan.missed_doses_count |
| Activity Compliance | percent | Yes | Compliance with activity restrictions | 0-100% | ENT-aftercare-plan.activity_compliance |
| Recent Scan Uploads | list | Yes | Recent 3D scan uploads | Chronological order | ENT-aftercare-scan-artifact.uploaded_at |
| Questionnaire Completions | list | Yes | Recent questionnaire submissions | Chronological order | ENT-aftercare-questionnaire-response.responded_at |
| Medication Updates | list | Yes | Recent adherence updates | Chronological order | ENT-aftercare-dose.taken_at |
| Communication Interactions | list | Yes | Recent messages/interactions | Chronological order | ENT-aftercare-communication-entry.sent_at |
| Request Additional Scan | action | No | Button to request extra scan | Always available | no graph field (control) |
| Send Message to Patient | action | No | Button to send message | Always available | no graph field (control) |
| Schedule Consultation | action | No | Button to schedule consultation | Always available | no graph field (control) |
| Escalate Case | action | No | Button to escalate urgent case | Always available | no graph field (control) |
| Urgent Flag | indicator | No | Shows when the plan is flagged urgent and since when | Display only (REQ-011-099) | ENT-aftercare-plan.urgent_flag, ENT-aftercare-plan.urgent_raised_at |
| Clear Urgent Flag | action | Cond. | Clear the urgent flag with a note (assigned provider) | Shown only while the flag is set; note required; clearing it is the response, and if it is not cleared within 2 hours of the raised time the system escalates to the admin (REQ-011-099) | no graph field (control) |

**Business Rules**:

- Progress calculated automatically by system (REQ-011-064)
- Provider can only view assigned patients (REQ-011-021, REQ-011-064)
- Real-time updates when patient completes tasks (REQ-011-027)
- Overdue tasks highlighted prominently (REQ-011-086)
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

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Case ID | column | Yes | Unique identifier (e.g., AC2509-0001) | Searchable; sortable | ENT-aftercare-plan.id |
| Patient Name | column | Yes | Avatar + full name + email | PII admin-only | ENT-patient.name, ENT-patient.email |
| Phone Number | column | No | Contact number | E.164 format | ENT-patient.phone |
| Age | column | No | Patient age | Integer 18–100 | ENT-patient.age |
| Problem | column | No | Treatment area | Value from the catalog-driven list (per FR-003) | ENT-inquiry.treatment_area_id |
| Treatment & Package | column | Yes | Treatment + package | Read-only | ENT-quote.treatment_id, ENT-subquote.package_snapshot |
| Provider | column | Yes | Assigned provider name | Must exist | ENT-provider.name |
| Aftercare Type | column | Yes | Treatment-linked or Standalone | Enum | ENT-aftercare-plan.aftercare_type |
| Start Date | column | Yes | Aftercare start date | ISO 8601; sortable | ENT-aftercare-plan.activated_at |
| Current Milestone | column | Yes | Current phase | Must exist in plan | ENT-aftercare-plan.current_milestone |
| Progress | column | Yes | Visual progress bar | Derived; non-negative | ENT-aftercare-plan.overall_progress |
| Med Alerts | column | Yes | Critical/Standard/None | Enum with color coding | ENT-aftercare-plan.medication_alert_level |
| Status | column | Yes | Pending activation/Active/Completed/Cancelled, with a separate Overdue flag shown on cases that have overdue tasks | Enum plus flag | ENT-aftercare-plan.status, ENT-aftercare-plan.overdue_flag |
| Urgent Flag | column | No | Shows the plans with the urgent flag set; the list can be filtered on it and the dashboard counts them | Display only (REQ-011-099) | ENT-aftercare-plan.urgent_flag |
| Action | column | Yes | View/Edit/Reassign/Escalate | RBAC enforced | no graph field (control) |
| Search/Filters | control | No | Provider/Milestone/Status/Date range/Risk Level/Specialist/Completion Rate | Valid enums/ranges | no graph field (control) |
| Pagination | control | No | Page and size controls | Standard UX pattern | no graph field (control) |

**Business Rules**:

- Shows all aftercare cases across all providers (REQ-011-068)
- The Aftercare Coordinator is an admin role (REQ-011-004) and works on the admin aftercare Screens 13 to 19 for plan configuration, scan review and escalations when the Hairline team delivers; no separate coordinator screens exist (REQ-011-004)
- Admin can edit any case data (full editability) (REQ-011-068)
- Overdue cases shown with amber indicators (REQ-011-068)
- Progress calculated automatically by system (REQ-011-068)
- All actions logged for audit trail (REQ-011-068)

**Notes**:

- Admin view shows all cases across all providers (unlike provider view which is filtered)
- Full editability allows admins to override any data when needed
- Color-coded alerts and status indicators help admins quickly identify cases needing attention
- Search and filter capabilities enable admins to find specific cases efficiently
- Action menu provides quick access to admin interventions (reassign, escalate, edit)

#### Screen 14: Aftercare Case Details (Multi-Tab View)

**Purpose**: Admin views comprehensive aftercare case information

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| **Tab 1: Case Overview** | | | | |  |
| Patient Information | component | Yes | Full patient details (admin can see all) | Display only | ENT-patient.name, ENT-patient.email, ENT-patient.phone, ENT-patient.address |
| Patient ID | text | Yes | Unique patient identifier | Display only | ENT-aftercare-plan.patient_id |
| Patient Name | text | Yes | Full patient name | Display only | ENT-patient.name |
| Contact Information | text | Yes | Email, phone, address | Display only | ENT-patient.email, ENT-patient.phone, ENT-patient.address |
| Treatment Information | component | Yes | Original treatment details | Display only | ENT-aftercare-plan.treatment_date, ENT-aftercare-plan.treatment_type |
| Treatment Date | date | Yes | Date treatment was performed | ISO 8601 format | ENT-aftercare-plan.treatment_date |
| Treatment Type | text | Yes | Type of treatment | Display only | ENT-aftercare-plan.treatment_type |
| Provider Information | component | Yes | Assigned provider details | Display only | ENT-provider.name, ENT-provider.phone, ENT-provider.email |
| Provider Name | text | Yes | Assigned provider name | Display only | ENT-provider.name |
| Provider Contact | text | Yes | Provider contact information | Display only | ENT-provider.phone, ENT-provider.email |
| Aftercare Plan | component | Yes | Selected template and customizations | Display only | ENT-aftercare-plan.template_id |
| Template Name | text | Yes | Selected template name | Display only | ENT-aftercare-plan.template_id |
| Current Status | component | Yes | Milestone progress and completion | Display only | ENT-aftercare-plan.current_milestone, ENT-aftercare-plan.overall_progress |
| Current Milestone | text | Yes | Current milestone name | Display only | ENT-aftercare-plan.current_milestone |
| Progress Percentage | percent | Yes | Overall progress | 0-100% | ENT-aftercare-plan.overall_progress |
| **Tab 2: Progress Tracking** | | | | |  |
| Milestone Progress | component | Yes | Visual timeline of all milestones | Display only | ENT-aftercare-milestone.status |
| 3D Scan History | list | Yes | All uploaded scans with dates and quality | Chronological order | no graph field (list of the rows below) |
| Scan Upload Date | datetime | Yes | Date scan was uploaded | ISO 8601 format | ENT-aftercare-scan-artifact.uploaded_at |
| Scan Quality Score | number | Yes | Quality score (0-100) | Integer 0-100 | ENT-aftercare-scan-artifact.quality_score |
| Questionnaire Responses | list | Yes | All responses with timestamps | Chronological order | ENT-aftercare-questionnaire-response.answers |
| Response Date | datetime | Yes | Date questionnaire was submitted | ISO 8601 format | ENT-aftercare-questionnaire-response.responded_at |
| Questionnaire Set | text | Yes | Questionnaire set | Display only | ENT-aftercare-questionnaire-response.questionnaire_set_id |
| Medication Adherence | component | Yes | Compliance tracking and history | Display only | ENT-aftercare-plan.medication_adherence |
| Adherence Percentage | percent | Yes | Overall adherence percentage | 0-100% | ENT-aftercare-plan.medication_adherence |
| Activity Compliance | percent | Yes | Compliance with activity restrictions | 0-100% | ENT-aftercare-plan.activity_compliance |
| **Tab 3: Communication Log** | | | | |  |
| Patient Messages | list | Yes | All patient communications | Chronological order | ENT-aftercare-communication-entry.sender_role |
| Provider Messages | list | Yes | Provider communications | Chronological order | ENT-aftercare-communication-entry.sender_role |
| Aftercare Team Messages | list | Yes | Internal team communications | Chronological order | ENT-aftercare-communication-entry.sender_role |
| Escalation History | list | Yes | All escalations and resolutions | Chronological order | ENT-aftercare-communication-entry.entry_type |
| System Notifications | list | Yes | Automated notifications sent | Chronological order | ENT-aftercare-communication-entry.entry_type |
| Message Date | datetime | Yes | Date/time of message | ISO 8601 format | ENT-aftercare-communication-entry.sent_at |
| Message Type | text | Yes | Type of message | Valid message type enum | ENT-aftercare-communication-entry.entry_type |
| **Tab 4: Admin Actions** | | | | |  |
| Edit Aftercare Plan | action | No | Button to modify any aspect of plan | Always available | no graph field (control) |
| Reassign Provider | action | No | Opens Screen 19 to reassign the aftercare provider or team | Available while the case is not completed or cancelled; standalone cases use the same screen | no graph field (control) |
| Escalate Case | action | No | Button to escalate to supervisor | Always available | no graph field (control) |
| Add Notes | action | No | Button to add internal admin notes | Always available | ENT-aftercare-plan.admin_notes |
| Activate Plan Manually | action | Cond. | Activate a plan whose setup the provider has not confirmed | Shown while the plan is not active; mandatory reason; recorded in the audit trail (REQ-011-019) | ENT-aftercare-audit-entry.reason |
| Configure Plan | action | Cond. | Configure and confirm the plan when the Hairline team delivers the case (Aftercare Coordinator); the system then activates it | Shown while the plan is Pending activation and the Hairline team delivers (REQ-011-049, REQ-011-055) | no graph field (control) |
| Cancel Aftercare | action | Cond. | Cancel the aftercare and close the case | Shown while the case is not completed or cancelled; mandatory reason; recorded in the audit trail; the closing rule applies (REQ-011-101) | ENT-aftercare-audit-entry.reason |
| Propose Extension or Change | action | Cond. | Propose an extension or major change with a reason when the Hairline team delivers (Aftercare Coordinator) | Reason required; a different admin approves it (REQ-011-098) | no graph field (control) |
| Set Urgent Flag | action | Cond. | Set the urgent flag by hand when the Hairline team delivers (Aftercare Coordinator) | Records the raised time (REQ-011-099) | no graph field (control) |
| Clear Urgent Flag | action | Cond. | Clear the urgent flag with a note when the Hairline team delivers (Aftercare Coordinator) | Shown only while the flag is set; note required; clearing it is the response (REQ-011-099) | no graph field (control) |
| Approve Proposed Change | action | Cond. | Approve a proposed extension or major change | Shown while a proposal is waiting; the patient is notified (REQ-011-098) | ENT-aftercare-audit-entry.approval_status |
| Reject Proposed Change | action | Cond. | Reject a proposed extension or major change | Reason required; the plan stays unchanged and the proposer is told why (REQ-011-098) | ENT-aftercare-audit-entry.approval_status |
| Urgent Flag | indicator | No | Shows when the plan is flagged urgent and since when; the case escalates here when nobody responds within 2 hours | Display only (REQ-011-099) | ENT-aftercare-plan.urgent_flag, ENT-aftercare-plan.urgent_raised_at |
| Change History | list | Yes | Audit trail of all changes | Chronological order | no graph field (list of the rows below) |
| Change Date | datetime | Yes | Date of change | ISO 8601 format | ENT-aftercare-audit-entry.changed_at |
| Changed By | text | Yes | User who made change | Display only | ENT-aftercare-audit-entry.changed_by |
| Change Reason | text | Yes | Reason for change | Display only | ENT-aftercare-audit-entry.reason |

**Business Rules**:

- Admin has full access to all tabs and data (REQ-011-021)
- All changes logged with admin identification (REQ-011-036)
- Patient anonymization rules don't apply to admin (REQ-011-010)
- All communications monitored and logged (REQ-011-030)
- Admin can override any provider settings (REQ-011-067)
- Manual activation needs a mandatory reason and creates an audit entry; it is the route for a plan whose setup stays unconfirmed after the escalation (REQ-011-019, REQ-011-090)
- The admin decides each proposed extension or major change here; a change proposed by the coordinator is approved by a different admin (REQ-011-098)
- Cancel Aftercare needs a mandatory reason, writes an audit entry and applies the closing rule (REQ-011-101)
- When the Hairline team delivers, the Aftercare Coordinator does the plan configuration, the extension or change proposal and the urgent flag actions here (REQ-011-004)

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

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Request ID | text | Yes | Unique request identifier | Searchable; sortable | ENT-aftercare-request.request_id |
| Submission Date | datetime | Yes | Date request was submitted | ISO 8601 format; sortable | ENT-aftercare-request.submitted_at |
| Patient Name | text | Yes | Full patient name (admin full visibility) | Display only | ENT-patient.name, ENT-aftercare-request.patient_id |
| Patient Email | email | Yes | Patient email address | Valid email format | ENT-patient.email |
| Patient Phone | text | Yes | Patient phone number | E.164 format | ENT-patient.phone |
| Treatment Date | date | Yes | Date treatment was performed | ISO 8601 format | ENT-aftercare-request.treatment_date |
| Treatment Type | text | Yes | Type of treatment | Valid treatment type enum | ENT-aftercare-request.treatment_type |
| Treatment Clinic | text | Yes | Name of clinic where treatment performed | Display only | ENT-aftercare-request.treating_clinic |
| Requested Duration | text | Yes | Duration requested (e.g., "12 months") | Valid duration enum | ENT-aftercare-request.requested_duration |
| Pricing Option | text | Yes | Pricing option selected (Fixed price or Monthly subscription) | Valid pricing option enum | ENT-aftercare-request.pricing_option |
| Payment Method | text | Yes | Payment method selected (Card, PayPal, etc.) | Valid payment method enum | ENT-aftercare-request.payment_method |
| Payment Status | status | Yes | Payment status (Paid/Pending/Failed) | Valid status enum | ENT-aftercare-request.payment_status |
| Request Status | status | Yes | Status (Pending/Awaiting provider availability/Assigned/Payment due/Active/Rejected/Expired); Rejected comes from an admin rejection, the 7-day unassigned expiry or a patient cancellation at a changed price, and Expired only from 48 hours without payment | Valid status enum | ENT-aftercare-request.request_status |
| Payment Due By | datetime | Cond. | Time the patient must pay by (48 hours from the payment-due notice) | Display only; after it the request becomes Expired (REQ-011-050) | ENT-aftercare-request.payment_due_at |
| Request Source | text | Yes | Add-on, standalone, or conversion from FR-038 monitoring | Display only (REQ-011-093) | ENT-aftercare-request.source |
| Final Template | text | Cond. | Template the provider finally chose, when it differs from the requested one | Display only (REQ-011-100) | ENT-aftercare-request.final_template_id |
| Monitoring Case | id | Cond. | FR-038 monitoring case a converted request came from | Display only | ENT-aftercare-request.monitoring_case_id |
| Full Patient Information | component | Yes | Complete patient details | Display only | ENT-patient.name, ENT-patient.email, ENT-patient.phone |
| Treatment Documentation | component | Yes | Treatment documentation files | Display/download | ENT-aftercare-request.documentation |
| Current Concerns | textarea | No | Patient's current concerns or issues | Max 2000 chars | ENT-aftercare-request.current_concerns |
| Uploaded Photos | list | Yes | Photos uploaded by patient | Display only | ENT-aftercare-request.photos |
| Surgeon Notes | text | No | Conclusion notes read from the FR-010 Hairline treatment record; empty for standalone requests | Display only | ENT-aftercare-request.surgeon_notes |
| Available Providers | list | Yes | List of available providers | Display only | no graph field (list of the rows below) |
| Provider Name | text | Yes | Provider name | Display only | ENT-provider.name |
| Provider Specialization | text | Yes | Provider specialization areas | Display only | ENT-provider.specialty |
| Provider Availability | status | Yes | Current availability status | Valid status enum | ENT-provider.availability_status |
| Assign Provider | action | Yes | Button to assign provider to request | Enabled when provider selected | ENT-aftercare-request.assigned_provider_id |
| Reject Request | action | Yes | Button to reject request with reason | Always available | no graph field (control) |
| Rejection Reason | textarea | Yes | Required reason for rejection | Max 500 chars; required when rejecting | ENT-aftercare-request.rejection_reason |
| Mark Awaiting Provider Availability | action | No | Mark the request as awaiting provider availability (pauses the 7-day timer) | Note required; recorded in the audit trail (REQ-011-052, REQ-011-053) | no graph field (control) |
| Clear Awaiting Mark | action | Cond. | Clear the awaiting mark (the 7-day timer resumes) | Shown while the mark is set; note required; recorded in the audit trail (REQ-011-052, REQ-011-053) | no graph field (control) |
| Availability Note | textarea | Cond. | Note given when the awaiting mark is set or cleared | Max 500 chars; required with either action | ENT-aftercare-audit-entry.reason |

**Business Rules**:

- A standalone request not assigned within 7 days becomes Rejected with a system reason, and the refund below applies. The 7 days count from submission, pause while the request is "Awaiting provider availability" and resume when that mark is cleared. The post-treatment add-on has no unassigned expiry because assignment is automatic at payment (REQ-011-053, REQ-011-037)
- "Expired" is a different outcome: a standalone request not paid within 48 hours of the payment-due notice becomes Expired, with nothing charged and nothing to refund (REQ-011-050)
- Assignment starts the 2-day reminder and the 4-day escalation of REQ-011-090 while the provider has not finished the plan (REQ-011-090)
- Provider assignment based on specialization and availability (REQ-011-069)
- Rejection requires reason and triggers a full refund of any payment already taken (REQ-011-037, REQ-011-051)
- All actions logged for audit trail

**Notes**:

- Admin has full visibility into patient information (unlike providers, who see patient details from assignment in the standalone flow and from payment in the add-on flow) (REQ-011-010)
- Request list provides quick overview of all pending standalone requests
- Detailed request view shows all patient-submitted information for informed assignment decisions
- Provider assignment interface helps match requests to appropriate providers based on specialization
- Rejection workflow ensures proper documentation and automatic refund processing
- Expiration tracking helps admins prioritize requests that are approaching deadline

#### Screen 16: Milestone Template Management

**Purpose**: Admin creates and manages aftercare milestone templates

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| **Template List** | | | | |  |
| Template Name | text | Yes | Name of template | Max 200 chars; unique | ENT-aftercare-template.name |
| Template Description | text | No | Description of template | Max 1000 chars | ENT-aftercare-template.description |
| Treatment Type | text | Yes | Treatment type (FUE, FUT, DHI, etc.) | Value from the admin-managed treatment catalog | ENT-aftercare-template.treatment_type |
| Duration | text | Yes | Duration (e.g., "12 months") | Valid duration enum | ENT-aftercare-template.duration |
| Number of Milestones | number | Yes | Count of milestones in template | Positive integer | ENT-aftercare-template.milestone_count |
| Usage Count | number | Yes | How many patients currently using | Non-negative integer | ENT-aftercare-template.usage_count |
| **Template Editor** | | | | |  |
| Template Name (Edit) | text | Yes | Template name | Max 200 chars; unique | ENT-aftercare-template.name |
| Template Description (Edit) | textarea | No | Template description | Max 1000 chars | ENT-aftercare-template.description |
| Treatment Type Selection | select | Yes | Treatment type dropdown | Value from the admin-managed treatment catalog | ENT-aftercare-template.treatment_type |
| Milestone Name | text | Yes | Name of milestone | Max 200 chars | ENT-aftercare-milestone.name |
| Milestone Duration | number | Yes | Duration in days | Positive integer | ENT-aftercare-milestone.duration_days |
| 3D Scan Frequency | text | Yes | Frequency of scans (e.g., "Weekly") | Valid frequency enum | ENT-aftercare-milestone.scan_frequency |
| Questionnaire Set | select | Yes | Questionnaire Set selection for this milestone | Must exist in FR-025 catalog | ENT-aftercare-milestone.questionnaire_set_id |
| Questionnaire Frequency | text | Yes | Frequency of questionnaires | Valid frequency enum | ENT-aftercare-milestone.questionnaire_frequency |
| Educational Resources | list | Yes | Resources assigned to milestone | May be empty | no graph field (list of the rows below) |
| Resource Title | text | Yes | Resource title | Max 200 chars | ENT-aftercare-resource.title |
| Resource Type | select | Yes | Type (video, PDF, webpage) | Valid resource type enum | ENT-aftercare-resource.resource_type |
| Resource URL | url | Yes | URL or file path | Valid URL or file path | ENT-aftercare-resource.url |
| Activity Restrictions | textarea | No | Restrictions for milestone | Max 500 chars | ENT-aftercare-milestone.activity_restrictions |
| **Resource Management** | | | | |  |
| Upload Video | action | No | Button to upload instructional videos | File size max 100MB | no graph field (control) |
| Add Guide | action | No | Button to add best practice guides | File size max 100MB | no graph field (control) |
| Create FAQ | action | No | Button to create FAQ documents | File size max 100MB | no graph field (control) |
| Manage Help Guides | action | No | Button to manage help guides | File size max 100MB | no graph field (control) |
| Resource File | file | Yes | Uploaded resource file | Max 100MB per file | ENT-aftercare-resource.file |
| **Pricing Configuration** | | | | |  |
| Enable for Purchase | checkbox | Yes | Make template available for standalone/add-on purchase | Boolean; default false | ENT-aftercare-template.available_for_purchase |
| Service Description | textarea | Cond. | Marketing description for patients | Max 500 chars; required if enabled for purchase | ENT-aftercare-template.service_description |
| Pricing Model | radio | Cond. | Fixed Price or Subscription or Both | Enum: "fixed", "subscription", "both"; required if enabled for purchase | ENT-aftercare-template.pricing_model |
| Multi-Currency Pricing | component | Cond. | Currency-specific pricing table | Required if enabled for purchase | ENT-aftercare-template-price.currency, ENT-aftercare-template-price.fixed_price, ENT-aftercare-template-price.monthly_price |
| Currency | select | Yes | Currency (USD, GBP, EUR, etc.) | Valid currency enum | ENT-aftercare-template-price.currency |
| Fixed Price | currency | Cond. | One-time payment amount | Required if "fixed" or "both" selected | ENT-aftercare-template-price.fixed_price |
| Monthly Subscription Price | currency | Cond. | Monthly payment amount | Required if "subscription" or "both" selected | ENT-aftercare-template-price.monthly_price |
| Add Currency | action | Yes | Button to add another currency | Always available | no graph field (control) |
| Default Pricing Option | radio | Cond. | Default shown to patient (if Both enabled) | Enum: "fixed", "subscription"; required if "both" selected | ENT-aftercare-template.default_pricing_option |

**Business Rules**:

- Discount codes do not apply to aftercare purchases in this release, so a template has no discount setting
- Templates cannot be deleted if in use (REQ-011-070)
- Changes to active templates require approval (REQ-011-070)
- New templates must be tested before activation (REQ-011-070)
- Resource files limited to 100MB each (REQ-011-070)
- Templates can be marked as "Internal Use Only" (providers only) or "Available for Purchase" (standalone/add-on) (REQ-011-046)
- Purchasable templates require pricing configuration for all supported currencies (REQ-011-085)
- If "Both" pricing model selected, patient can choose between fixed or subscription at purchase (REQ-011-042)
- Monthly subscription price is per month; total subscription amount = monthly price × template duration in months (REQ-011-043)
- Pricing changes to active templates require admin approval and don't affect existing patients (locked at purchase time) (REQ-011-047)
- Multi-currency pricing uses real-time exchange rates as baseline but allows admin override for final pricing (REQ-011-084)
- Template Name is used as service name for patient-facing display (no separate service name needed) (REQ-011-046)
- Questionnaire sets and questions are not authored here; they are centrally managed in FR-025 (Medical Questionnaire Management). Screen 16 selects among existing Questionnaire Sets and configures schedule/frequency per milestone. (REQ-011-071)
- Screen 16 surfaces Questionnaire Sets with context type "Aftercare" plus every Multi-Context Questionnaire Set from FR-025 (see FR-025, REQ-025-071); no compatibility flag is needed. A response keeps the set version it started on, and each assignment or replacement of a set on a milestone is recorded in the audit trail. (REQ-011-071)
- Each milestone independently selects a Questionnaire Set (single-select per milestone). Different milestones within the same template may reference different sets (e.g., Week 1: Pain Assessment; Week 4: Sleep Quality). (REQ-011-071)

**Cross-Module Reference**:

- Questionnaire content ownership and lifecycle: see FR-025: Medical Questionnaire Management (REQ-011-013)
- After selecting Questionnaire Sets here, their delivery and response handling follow the schedules defined per milestone (REQ-011-071)

**Notes**:

- Template management enables standardization of aftercare plans across providers
- Template list shows usage count to prevent deletion of active templates
- Template editor provides comprehensive configuration for all milestone aspects
- Questionnaire integration with FR-025 ensures consistent questionnaire management
- Per-milestone Questionnaire Set selection enables phase-specific assessments without duplicating templates
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

- Performance scores calculated monthly (REQ-011-077)
- Poor performance triggers review process (REQ-011-077)
- Provider suspension requires admin approval (REQ-011-077)
- Retention of performance data follows the system PRD, Platform-Wide Rules: One 10-year retention period, REQ-SYS-002 (REQ-011-077)
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

- Admin can view all cases across all providers (REQ-011-078)
- Real-time updates from all aftercare activities (REQ-011-078)
- Performance metrics calculated daily (REQ-011-078)
- Alerts generated automatically for issues (REQ-011-078)
- All actions logged with admin identification (REQ-011-078)
- This screen is deferred to a later phase as it represents system-wide analytics beyond case operations covered by Screens 11–12.

**Notes**:

- System-wide analytics dashboard for monitoring all aftercare progress across all providers
- Real-time updates provide current status of all active cases
- Provider performance grid enables comparison and identification of performance patterns
- Case status distribution helps identify systemic issues or bottlenecks
- Real-time alerts notify admins of urgent cases requiring immediate attention
- Quick action buttons enable rapid interventions across multiple cases
- Deferred to post-MVP phase as it extends beyond core case management operations

#### Screen 19: Reassign Aftercare Provider (Admin)

**Purpose**: Let an admin reassign the aftercare provider or team on an aftercare case, including a treatment-linked case whose booking is `Aftercare`, without changing the booking or the treatment record (Workflow 4 D1, D4, and D5).

**Entry points**: Reassign Provider on Screen 14 (Tab 4), the Reassign Aftercare link on the FR-006 admin booking detail (FR-006 Screen 6), or the Move to Aftercare route of the FR-006 In-Progress provider-fault decision (FR-006 Screen 11).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Case Reference | text | Yes (read-only) | Aftercare case identifier, patient ID, and linked booking reference for a treatment-linked case | Display only | ENT-aftercare-plan.id, ENT-aftercare-plan.booking_id |
| Current Aftercare Provider or Team | text | Yes (read-only) | Provider or Hairline aftercare team now assigned | Display only | ENT-aftercare-plan.provider_id, ENT-aftercare-plan.assigned_team_member_id |
| Provider Status and Cause | text | No (read-only) | Current provider status and any recorded cause, such as `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated`, with the `supportRequired` marker | Display only | ENT-provider.status, ENT-aftercare-plan.cancellation_reason, ENT-aftercare-plan.support_required |
| Reassignment Type | text | Yes (read-only) | Marker telling a provider handover from an admin reassignment | Display only; set by the system (REQ-011-057, REQ-011-075) | ENT-aftercare-audit-entry.reassignment_type |
| Reassignment Target Type | radio | Yes | Another provider or the Hairline aftercare team | One option must be selected | no graph field (control) |
| New Provider | searchable select | Conditional | Replacement aftercare provider | Required when the target type is another provider; only `Active` providers; cannot be the current provider | ENT-aftercare-audit-entry.new_assignee_id |
| New Aftercare Team Member | select | Conditional | Hairline aftercare team member who takes the case | Required when the target type is the Hairline aftercare team | ENT-aftercare-audit-entry.new_assignee_id |
| Reassignment Reason | text area | Yes | Why the aftercare is reassigned | Mandatory; 10 to 1000 characters | ENT-aftercare-audit-entry.reason |
| Resolve Support Marker | checkbox | Conditional | Marks the `supportRequired` marker resolved | Shown only when the marker is set; checked by default | ENT-aftercare-plan.support_required_resolution |
| Confirmation Summary | panel | Yes (read-only) | Shows the current and new assignee, the reason, and that the booking, treatment record, plan, and payments stay unchanged | Shown on the confirmation step | no graph field (display component) |
| Confirm Reassignment | button | Yes | Saves the reassignment after the admin confirms | Enabled only when every required field is valid | no graph field (control) |
| Cancel | button | No | Closes the screen without saving | — | no graph field (control) |

**Business Rules**:

- The reassignment changes only the aftercare provider or team. For a treatment-linked case, the FR-006 booking stays `Aftercare` and the FR-010 treatment record stays unchanged; no quote, acceptance, or payment is created. (REQ-011-015, REQ-011-075)
- The aftercare plan, milestones, scans, questionnaire responses, medications, and communication history stay with the case. The new assignee gets the case's aftercare actions from the moment of confirmation; the previous provider loses them. (REQ-011-075)
- The change is saved only after confirmation, is recorded in the audit trail with admin identity, timestamp, reason, previous assignee, and new assignee, and, when selected, records the audited resolution of the `supportRequired` marker. (REQ-011-076)
- On save, System sends the `aftercare.provider_reassigned` notice. FR-011 is the producer of this FR-030 event; recipients, content, and the mandatory status of the notice are defined by the FR-030 notification Rule. (REQ-011-015)
- A reassignment has no automatic refund and no refund ladder. For a standalone plan any refund is an admin manual refund (REQ-007-100); for a treatment-linked case reached through the FR-006 B7 decision, the refund and payout hold are those set on FR-006 Screen 11 (REQ-006-019). (REQ-011-075)
- The same screen opens setup for the aftercare team or the reassigned provider when FR-010 closes treatment early; the new assignee then sets up the plan as in Workflow 1 (REQ-011-091)
- Who is paid follows the Reassignment Type marker. After an admin reassignment to the Hairline team, Hairline keeps the full price with no commission line and no provider payment. After a provider handover the previous provider is paid the fixed handover fee set in the admin handover-fee setting (default 0, so nothing is paid until the admin sets an amount); in the treatment-linked flow there is no separate aftercare price, so Hairline pays that fee from its own revenue, and in the add-on and standalone flows Hairline keeps the rest of the price (REQ-011-057)

## Business Rules

### General Module Rules

1. **Activation Rules**
   - Treatment-linked setup starts automatically on the FR-010 completion signal; the plan activates when the provider confirms it (REQ-011-055) or an admin activates it (REQ-011-019); FR-006 owns the booking move to Aftercare (REQ-011-017, REQ-011-091)
   - If no plan is confirmed, the provider gets a reminder after 2 days and the case escalates to the admin after 4 days; both day counts are admin settings; the same two settings also run for a paid add-on whose plan is not activated (from payment) and for a standalone request whose assigned provider has not finished the plan (from assignment), and the clock restarts at a handover or an admin assignment (REQ-011-090)
   - No post-treatment add-on while a plan for the same booking is Pending activation, Active or Completed (REQ-011-092)
   - Standalone aftercare requires payment before activation (REQ-011-018)
   - Admin can manually activate aftercare for special cases (REQ-011-019)

2. **Duration Rules**
   - Standard aftercare duration: 6-12 months (REQ-011-020)
   - Duration determined by treatment type and complexity (REQ-011-020)
   - Extensions are proposed by the provider (or the coordinator) with a reason and need admin approval; extra cost needs the patient's acceptance and payment (REQ-011-020, REQ-011-098)

3. **Access Rules**
   - Patients can only access their own aftercare data (REQ-011-021)
   - Providers can only access assigned patients (REQ-011-021)
   - Admin has full access to all aftercare data (REQ-011-021)
   - Hiding and unlocking patient identity around payment is one platform rule in the system PRD (REQ-SYS-001); it is not restated here

4. **Provider Status Cancellation Rules**
   - An effective provider suspension/deactivation does not cancel that provider's non-terminal standalone aftercare cases; it marks them for Screen 19 reassignment with cause `ProviderSuspended` or `ProviderDeactivated` and an independent `supportRequired` marker (Workflow 4 D4; FR-015 A5/Screen 4) (REQ-011-014)
   - For treatment-linked cases the aftercare case is not cancelled and the booking stays `Aftercare`; the cause and the `supportRequired` marker are recorded and an admin reassigns the aftercare provider or team on Screen 19 (Workflow 4 D5) (REQ-011-073)
   - The cancellation keeps the FR-010 completion milestone and all aftercare records; it is not a patient cancellation or a provider withdrawal (D1) (REQ-011-074)
   - Recovery continuity is an admin decision through the existing reassignment/recovery workflow; nothing is reassigned automatically and reactivation never restores the case (REQ-011-014, REQ-011-074)

5. **Closing Rule**
   - Every ending of aftercare (completed, paperwork-only completion, cancelled by the patient once the paid period ends, cancelled by an admin) stops all reminders and emits the completion event with an outcome value; the booking then moves to Completed, which FR-006 reads (REQ-011-101, REQ-011-096)

### Milestone and Task Rules

1. **Milestone Progression**
   - Milestones progress automatically based on time elapsed (REQ-011-023)
   - Patients cannot skip milestones (REQ-011-023)
   - Time ends a milestone: a required scan, questionnaire or education task not done by the milestone end becomes Missed, the milestone closes on schedule, and the plan completes at the end of the last milestone (REQ-011-023, REQ-011-096)

2. **Task Completion**
   - Scan uploads must meet quality threshold (REQ-011-024)
   - Questionnaires must be completed in full (REQ-011-024)
   - Medication adherence is tracked only: not mandatory for milestone completion and not part of the progress percentage (REQ-011-024, REQ-011-027)
   - Overdue tasks trigger escalation after 48 hours counted from the task due date (REQ-011-025)

3. **Progress Calculation**
   - Progress = (completed tasks / total tasks) * 100 (REQ-011-027)
   - Tasks weighted equally; only scan, questionnaire and education tasks count, and Missed tasks count as not done (REQ-011-027)
   - Progress updates in real-time (REQ-011-027)

### Communication Rules

1. **Patient Communication**
   - Patients can contact aftercare team 24/7 (REQ-011-029)
   - Urgent cases receive priority response (within 2 hours of the time the urgent flag was raised); clearing the flag with a note is the response, and if it is not cleared in time the case escalates to the admin (REQ-011-029, REQ-011-099)
   - Standard cases receive response within 24 hours (REQ-011-029)

2. **Provider Communication**
   - Providers can communicate with aftercare team about assigned cases (REQ-011-030)
   - Escalations require immediate response (REQ-011-030)
   - All communications logged for audit (REQ-011-030)

3. **Admin Communication**
   - Admin can communicate with any stakeholder (REQ-011-031)
   - System-wide announcements sent to all relevant parties (REQ-011-031)
   - Emergency communications bypass normal channels (REQ-011-031)

4. **Default Patient Progress Reminder**
   - By default the patient receives a progress reminder once a month for 12 months after treatment (REQ-011-088)
   - The patient may change the reminder or switch it off (REQ-011-088)
   - The default is an admin-editable setting (REQ-011-088)

### Data and Privacy Rules

1. **Data Retention**
   - Retention of aftercare data, scan media and communication logs follows the system PRD, Platform-Wide Rules: One 10-year retention period, REQ-SYS-002 (REQ-011-032)

2. **Data Access**
   - Patient details are visible to the assigned provider from assignment in the standalone flow, and from payment in the post-treatment add-on flow where assignment follows payment; the admin always sees them (REQ-011-010; REQ-011-022 is retired in favour of the system PRD, Platform-Wide Rules: Patient identity hidden until booking confirmation, REQ-SYS-001)
   - Provider access limited to assigned patients (REQ-011-021)
   - Admin access logged for audit trail (REQ-011-033)

3. **Data Security**
   - Encryption of aftercare data in transit and at rest follows the system PRD, Platform-Wide Rules: Encryption in transit and at rest (REQ-SYS-004)
   - Scan media stored securely with access controls (REQ-011-012)
   - Access attempts logged and monitored (REQ-011-033)

### Admin Editability Rules

1. **Full Admin Override**
   - Admin can edit ALL aftercare data in the system (REQ-011-034)
   - Admin can modify any provider's aftercare plans (REQ-011-034)
   - Admin can change patient assignments and providers (REQ-011-034)
   - Admin can override any system-calculated progress (REQ-011-034)

2. **Edit Capabilities**
   - **Aftercare Plans**: Modify templates, milestones, medications, instructions (REQ-011-035)
   - **Patient Data**: Edit patient information, treatment details, contact info (REQ-011-035)
   - **Provider Data**: Modify provider assignments, customizations, settings (REQ-011-035)
   - **Progress Data**: Override progress calculations, milestone completions (REQ-011-035)
   - **Communication Data**: Edit messages, escalations, notifications; the original text of an edited message is kept in the edit history (REQ-011-035)
   - **Template Data**: Modify milestone templates, questionnaires, resources (REQ-011-035)

3. **Edit Tracking**
   - All admin edits logged with timestamp and admin identification (REQ-011-036)
   - Change reason required for all modifications (REQ-011-036)
   - Edit history maintained for audit trail (REQ-011-036)
   - Provider and patient notified of significant changes (REQ-011-036)

### Payment and Billing Rules

1. **Standalone Aftercare Payment**
   - Payment activates the service: for a standalone request it is taken last, after the admin has assigned a provider and the provider has configured the plan (Workflow 2) (REQ-011-018)
   - Any payment already taken is refunded automatically for rejected requests (REQ-011-037)
   - A request not paid within 48 hours of the payment-due notice becomes Expired; nothing was charged, so nothing is refunded (REQ-011-050)
   - Payment disputes handled by admin team (REQ-011-038)

2. **Provider Compensation**
   - Who is paid depends on who delivers (REQ-011-057): the provider who delivers is paid the price less commission; when the Hairline team delivers by default (add-on flow) or after an admin reassignment, Hairline keeps the full price with no commission line and no provider payment; when the team takes over after a provider handover, the provider is paid the fixed handover fee set in the admin handover-fee setting (default 0); in the treatment-linked flow Hairline pays it from its own revenue because there is no separate aftercare price, and in the add-on and standalone flows Hairline keeps the rest; the fee is a Handover Fee credit entry on the clinic's balance record owned by FR-017 (REQ-017-203)
   - Providers compensated for aftercare participation (REQ-011-039)
   - Compensation based on case complexity and duration (REQ-011-039)
   - Payment processed monthly (REQ-011-039)

3. **Platform Commission**
   - Platform commission deducted from standalone and post-treatment add-on aftercare payments when a provider delivers; no commission line applies when the Hairline team keeps the full price (REQ-011-040, REQ-011-057)
   - Commission rate: 15-25% (configurable); it is a percentage of the aftercare price for aftercare payments, one amount under one setting, taken from the aftercare price and never added to the patient's total (REQ-011-040)
   - Commission calculated at time of payment (REQ-011-040)

4. **Aftercare Service Payment Rules**
   - **Template-based pricing**: Each aftercare template defines its own pricing (fixed, subscription, or both) in Screen 16 (REQ-011-041)
   - **Multi-currency support**: Pricing configured per currency; patient sees price in local currency based on location (REQ-011-041)
   - **Pricing option selection**: If template offers both fixed and subscription, patient chooses the pricing option at purchase time (the pricing option is separate from the payment method, such as card or PayPal) (REQ-011-042)
   - **Subscription payments**: Monthly installments charged automatically for template duration; first payment immediate, subsequent on monthly anniversary (REQ-011-043)
   - **Post-treatment add-on availability**: Available to Hairline-treated patients within 90 days of treatment completion (REQ-011-044)
   - **Standalone service availability**: Available to all patients regardless of treatment source (REQ-011-045)
   - **Template filtering**: Only templates marked "Available for Purchase" are shown; filtered by treatment type compatibility (REQ-011-046)
   - **Pricing immutability**: Patients locked into price at time of purchase (future template price changes don't affect existing patients) (REQ-011-047)
    - **Discount codes**: Discount codes do not apply to aftercare purchases in this release
   - **Payment timing**: Payment activates the service for both standalone and post-treatment add-on; for a standalone request payment comes last, after provider assignment and plan configuration (Workflow 2), and for a post-treatment add-on it comes before automatic assignment (Workflow 2b) (REQ-011-018)
   - **Refund policy**: Full refund of any payment already taken if a request is rejected by an admin (an add-on too, after payment) or a standalone request stays unassigned for 7 days; pro-rata refund of the unused full months when a plan paid in full is cancelled, and no refund for a monthly subscription cancelled mid-month (REQ-011-097, REQ-011-083, REQ-011-037); a reassignment has no automatic refund (REQ-011-075)

### Integration and Security Rules

- **FR-010 integration point**: The FR-010 treatment completion signal starts aftercare setup and a repeated signal for the same booking returns the existing plan; uses treatment details to pre-populate aftercare plan; the retry of a failed signal stays in FR-010 (REQ-010-086) (REQ-011-091)
- **FR-002 integration point**: Reuses scan quality validation and scan storage infrastructure; the scan task uses the FR-002 media-only call and its staged-photo clean-up (REQ-011-095, REQ-002-047, REQ-002-051)
- **FR-007 integration point**: Payment completion activates the aftercare plan for a standalone request (payment comes last, after provider assignment and plan configuration, Workflow 2) and triggers automatic assignment for a post-treatment add-on (Workflow 2b); payment status determines service activation eligibility
- **FR-020 why needed**: Sends task reminders, progress updates, and urgent alerts to patients, providers, and aftercare team
- **FR-020 integration point**: Aftercare events (task due, milestone completion, escalations) trigger notification delivery; notification preferences managed per user
- **Payment Data why needed**: Payment confirmation required for standalone aftercare activation; it also unlocks provider access to patient information in the add-on flow (REQ-011-010)
- **Head Scan Capture (V1) integration**: Native camera capture + guided instructions + upload (JPG/PNG)
- **Head Scan Capture (V1) failure handling**: Retry capture; allow partial save as draft where supported; show clear remediation guidance
- **3D Scanning SDK - ARKit/ARCore (V2) integration**: Native SDK integration in mobile apps (iOS ARKit, Android ARCore) for real-time 3D capture
- **3D Scanning SDK - ARKit/ARCore (V2) failure handling**: Fallback to V1 photo set capture; user notification of degraded functionality
- **Cloud Storage Service integration**: RESTful API for file upload/download with signed URLs for secure access
- **Cloud Storage Service failure handling**: Retry with exponential backoff; queue uploads for retry if service unavailable; notify user of upload delays
- **Payment Gateway - Stripe integration**: Stripe API integration for payment processing and refund handling
- **Payment Gateway - Stripe failure handling**: Payment failures trigger retry queue; user notified of payment issues; automatic refund processing on rejection
- **Notification Service purpose**: Delivers email and push notifications for reminders and alerts in MVP; SMS delivery is planned as a future enhancement once S-03 SMS support is enabled
- **Notification Service integration**: RESTful API for notification delivery with delivery status tracking
- **Notification Service failure handling**: Retry failed notifications; fallback to alternative channels where available (e.g., push if email fails); notification delivery failures logged for monitoring
- **Real-time Updates**: Progress tracking and notifications require real-time data synchronization
- **Offline Capability**: Core aftercare features should work with limited connectivity
- **Integration 1 - Treatment Module, authentication**: OAuth 2.0 bearer tokens for service-to-service communication
- **Integration 1 - Treatment Module, error handling**: Retry with exponential backoff on 5xx errors; queue activation requests if treatment module unavailable
- **Integration 2 - Payment Module, authentication**: API key authentication for payment gateway integration
- **Integration 2 - Payment Module, error handling**: Payment failures trigger user notification and retry queue; automatic refund processing on rejection
- **Integration 3 - Notification Module, authentication**: OAuth 2.0 bearer tokens for service-to-service communication
- **Integration 3 - Notification Module, error handling**: Retry failed notifications with exponential backoff; fallback to alternative delivery channels
- **Integration 4 - Communication Module, authentication**: OAuth 2.0 bearer tokens with role-based access control
- **Integration 4 - Communication Module, error handling**: Message delivery failures logged and retried; user notified of delivery status
- **Provider Assignment**: Future phase: Automated assignment algorithms for standalone cases (manual admin assignment is the requirement)
- **Audit Logging**: Comprehensive logging of all aftercare activities
- **Compliance**: Healthcare data protection regulations compliance
- **AftercareAuditEntry**: immutable audit record
- **SC-008**: Admin can assign standalone aftercare request within 24 hours

- **REQ-011-102**: Contact Support on the patient Aftercare Dashboard (Screen 1) MUST let the patient send a text message to the aftercare team at any time while the aftercare plan is open. System MUST record it as an aftercare communication entry (entry type message, sender role patient) on the plan and show it in the aftercare team's communication log for that patient. It is not an FR-012 conversation, and FR-012 chat with the provider stays separate (REQ-011-080).
- **REQ-011-103**: When a member of the aftercare team sends the patient a message from the aftercare case, including a reply to a Contact Support message, System MUST record it as an aftercare communication entry (entry type message, sender role aftercare_team), MUST show it to the patient in the Messages list on the Aftercare Dashboard (Screen 1) together with the patient's own Contact Support messages in chronological order, and MUST send the patient the `aftercare.team_message` notification by push and email (FR-030 REQ-030-295). The patient answers through Contact Support (REQ-011-102).

## Dependencies

Related FRs:

- **FR-001**: Patient registration module (Patient Data)
- **FR-010**: Treatment Execution & Documentation (cites REQ-010-006, REQ-010-009, REQ-010-023, REQ-010-086)
- **FR-002**: Medical History & 3D Scanning (cites REQ-002-034, REQ-002-024, REQ-002-023, REQ-002-036, REQ-002-047, REQ-002-051)
- **FR-006**: Booking & Scheduling (owns the move to Aftercare and reads the plan completion event; see REQ-006-060)
- **FR-038**: Monitor Your Transplant Progress (a monitoring case can be converted into a standalone request; see REQ-038-068)
- **FR-007**: Payment Processing (cites REQ-007-088, the FR-007 Rule that processes the standalone aftercare payment)
- **FR-017**: Admin Billing & Financial Management (cites REQ-017-203 for the handover fee entry and REQ-017-202 for the commission reversal on a subscription cancellation refund)
- **FR-020**: Notifications & Alerts (cites the four aftercare events REQ-020-117, REQ-020-118, REQ-020-119, REQ-020-120, each reaching its FR-030 Rule: REQ-030-072, REQ-030-073, REQ-030-074, REQ-030-075)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-011-001**: System MUST support treatment-linked and standalone aftercare activation paths; a standalone request may also start as a conversion from FR-038 monitoring (REQ-011-093)
- **REQ-011-002**: Patients MUST be able to complete milestone tasks (scan uploads, questionnaires) with reminders and quality validation
- **REQ-011-003**: Providers MUST be able to configure and activate aftercare plans with template customization
- **REQ-011-004**: Admin MUST be able to oversee cases, reassign providers, and override plans with full audit. Admin assignment of who delivers the aftercare (a provider, whose clinic staff are the aftercare specialists, or a Hairline aftercare team member, an admin with the FR-031 Aftercare Coordinator role) is owned by FR-011. The Aftercare Coordinator works on the admin aftercare Screens 13 to 19 (plan configuration, scan review, escalations) when the Hairline team delivers
- **REQ-011-014**: When a provider's suspension or deactivation becomes effective, System MUST NOT cancel that provider's non-terminal standalone aftercare cases; it MUST record cause `ProviderSuspended` or `ProviderDeactivated` and an independent `supportRequired` marker and route them to Screen 19 reassignment (treatment-linked cases follow REQ-011-015), retain the completion milestone and aftercare records, and route recovery continuity to admins for resolution through the existing reassignment/recovery workflow, without automatic reassignment or restoration on reactivation (Workflow 4 D4; FR-015 A5/Screen 4)
- **REQ-011-015**: System MUST let an admin reassign the aftercare provider or team on Screen 19 with a mandatory reason, confirmation, audit entry, and the `aftercare.provider_reassigned` notice (recipients, content, and the mandatory status of the notice are defined by the FR-030 notification Rules REQ-030-026 and REQ-030-077); for a treatment-linked case the booking MUST stay `Aftercare` and the treatment record MUST stay unchanged, with no new quote, acceptance, or payment
- **REQ-011-088**: By default System MUST send each patient a progress reminder once a month for 12 months after treatment; the patient MAY change or switch off the reminder, and the default is admin-editable
- **REQ-011-090**: When no plan is confirmed, System MUST remind the provider after 2 days and escalate the case to the admin after 4 days; both day counts are admin settings; the same settings MUST also run for a paid add-on whose plan is not activated (from payment) and for a standalone request whose assigned provider has not finished the plan (from assignment), and the clock MUST restart at a handover or an admin assignment and address the current assignee
- **REQ-011-091**: System MUST open Workflow 1 on the FR-010 completion signal (early close opens setup for the team or the reassigned provider on Screen 19), and a repeated signal for the same booking MUST return the existing plan; the retry of a failed signal stays in FR-010 (REQ-010-086)
- **REQ-011-092**: System MUST refuse a post-treatment add-on while a plan for the same booking is Pending activation, Active or Completed, and allow it after a paperwork-only completion; a plan is Pending activation from the opening of setup (treatment-linked) or from configuration until payment (standalone)
- **REQ-011-093**: System MUST accept a standalone request converted from FR-038 monitoring carrying source, monitoring case, scan or photo set, report file and an idempotency key; a repeated key returns the existing request
- **REQ-011-094**: System MUST refuse a conversion once the monitoring case is completed, and after a failed or abandoned request MUST return the patient to FR-038 Screen 6 with the draft intact; when a converted request ends Rejected or Expired the notice MUST say the patient may start a new standalone request pre-filled from the same source data with a new idempotency key, and the monitoring case stays final
- **REQ-011-095**: The scan task MUST use the FR-002 media-only call with at least one photo and the scan id as idempotency key; staged photos never attached to a scan are removed after 7 days
- **REQ-011-096**: System MUST complete the plan at the end of the last milestone or the subscription term (whichever is later), stop its reminders including REQ-011-088, and emit a completion event that FR-006 reads; every other ending follows REQ-011-101
- **REQ-011-097**: The patient MUST be able to cancel from the plan payment screen: a monthly subscription runs to the end of the paid month with no refund; a plan paid in full stops at the end of the current month with a pro-rata refund of the unused full months; commission and provider payout follow in proportion, the commission reversal being FR-017 REQ-017-202
- **REQ-011-098**: The provider (or the coordinator) MUST be able to propose an extension or major change with a reason; the admin approves or rejects it; the patient is notified and extra cost needs the patient's acceptance and payment; a rejection leaves the plan unchanged; when the coordinator proposes, the approving admin MUST be a different person
- **REQ-011-099**: The plan MUST carry an urgent flag and its raised-at time; the assigned provider or coordinator clears it with a note; when the flag is not cleared within 2 hours (clearing it is the response) the case escalates to the admin; dashboards count flagged plans
- **REQ-011-100**: The provider MAY pick an alternative template only among templates offering the pricing option the patient chose; when the final price differs the patient accepts the new price or cancels at no charge; in the already paid add-on flow an alternative is allowed only if its price for the chosen pricing option equals the price already paid (REQ-011-047)
- **REQ-011-101**: Every ending of aftercare (completed, paperwork-only completion, cancelled by the patient through subscription cancellation once the paid period ends, cancelled by an admin) MUST stop all reminders and emit the completion event with an outcome value, after which the booking moves to Completed; the admin MUST be able to cancel aftercare on Screen 14 Tab 4 with a mandatory reason that is written to the audit trail

### Data Requirements

- **REQ-011-005**: System MUST track milestones, tasks, progress, and adherence as structured entities
- **REQ-011-006**: System MUST retain all aftercare artifacts (scans, questionnaires, communications) per retention policy
- **REQ-011-007**: Progress MUST be derived deterministically from plan and task completion (completed scan, questionnaire and education tasks over total such tasks; medication adherence is tracked separately)

### Security & Privacy Requirements

- **REQ-011-008**: Aftercare data encryption in transit and at rest MUST follow the system PRD, Platform-Wide Rules: Encryption in transit and at rest (REQ-SYS-004)
- **REQ-011-009**: *Retired.* Role-based (patient, provider, admin) and audited access is one platform rule in the system PRD, Platform-Wide Rules: Role-based, audited access (REQ-SYS-009)
- **REQ-011-010**: The assigned provider sees patient details from assignment in the standalone flow and from payment in the post-treatment add-on flow where assignment follows payment; the admin is exempt and always sees them. *(REQ-011-022, "identity hidden until payment", is retired in favour of the system PRD, Platform-Wide Rules: Patient identity hidden until booking confirmation, REQ-SYS-001.)*

### Integration Requirements

- **REQ-011-011**: *Retired.* Every feature uses the notification service through the one FR-020 notification-service Rule
- **REQ-011-012**: System MUST store media artifacts in secure storage with controlled access
- **REQ-011-013**: System MUST reference questionnaires managed in FR-025 for aftercare context

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

Independent Test: Patient receives reminders; uploads scan/photo set; completes questionnaire; progress updates; alerts generated if concerning.

Acceptance Scenarios:

1. Given task due, When patient uploads scan meeting quality, Then task is completed and progress updates
2. Given concerning questionnaire responses, When submitted, Then case is flagged urgent and team notified
3. Given missed tasks, When overdue by 24 hours, Then the task carries the Overdue flag and reminders trigger; When still overdue at 48 hours, Then the task escalates

### User Story 3 - Standalone Aftercare Onboarding (Priority: P2)

Why: Opens service to external clinic patients.

Independent Test: Patient requests standalone service, admin assigns provider, provider configures plan, payment completes and activates the plan.

Acceptance Scenarios:

1. Given a submitted request, When admin assigns provider, Then provider configures the plan and the patient is asked to pay
2. Given a configured plan, When payment succeeds, Then the plan is activated
3. Given activation, When patient opens app, Then aftercare dashboard is available with schedule

### Edge Cases

- Provider withdrawal: admin reassigns or cancels with reason; patient notified (REQ-011-072)
- Provider suspended or deactivated mid-aftercare: a standalone case and a treatment-linked case both stay active with the cause and `supportRequired` until an admin reassigns it on Screen 19; records and completion milestone retained; admin decides reassignment or recovery support (Workflow 4 D4). Suspension followed by deactivation keeps the `ProviderSuspended` cause (REQ-011-014, REQ-011-073)
- Network loss during scan upload: resumable upload; no duplicate entries (REQ-011-081, REQ-011-095)
- Repeated completion signal for the same booking: the existing plan is returned (REQ-011-091); repeated conversion key: the existing request is returned (REQ-011-093)
- Conflicting schedule changes: latest confirmed change supersedes prior; audit preserved (REQ-011-082)

**Document Status**: ✅ Verified & Approved  
**Next Steps**: Technical specification and implementation planning  
**Maintained By**: Product & Engineering Teams  
**Review Cycle**: Monthly or upon major changes  
**Verification Date**: 2025-10-23 - Cross-checked against client transcriptions and confirmed alignment

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 1.11 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.10) and the change requests (CR-FR011-20261014-01 in change-request-2026-10-14-provider-status-cancellation-cascade.md, CR-FR011-20261016-01 in change-request-2026-10-16-mtg002-quote-model-alignment.md, CR-FR011-20261026-01 in change-request-2026-10-26-standalone-aftercare-reassignment.md, and CR-FR015-20261013-01) are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 1.12 | Owner ruling 2026-11-23: the aftercare specialist is clinic staff on the provider side; the Hairline admin role is renamed Aftercare Coordinator with unchanged permissions. Assignment wording in Module Scope and REQ-011-004 now names both sides: clinic aftercare specialists and Hairline aftercare team members (Aftercare Coordinator role). Who may deliver a case is unchanged. | Product Owner / Documentation |
| 2026-11-24 | 1.13 | Logic review: plan activation by provider confirmation or admin activation with a stalled-setup reminder and escalation; three entry sources including the FR-038 conversion; milestone closing on scan, questionnaire and education with medication outside the percentage; payment-due and expiry handling with the paused 7-day timer; final-template price acceptance; who is paid by who delivers; subscription cancellation, plan completion, extension approval and the urgent flag clock; Coordinator on admin Screens 13 to 19; wording alignment with FR-002, FR-006, FR-025 and FR-038. | Product Owner / Documentation |
| 2026-11-25 | 1.15 | Cross-FR alignment: the medication pick offers only Active templates and the plan keeps its own copy of the text (FR-024); the out-of-scope patient and provider chat states its lifecycle (FR-012). The conversion hand-off rows were already stated and are unchanged. | Documentation |
| 2026-11-24 | 1.14 | Logic review pass 2: one closing rule for every ending of aftercare with an admin Cancel Aftercare control; time ends a milestone and a task not done becomes Missed; reminder and escalation clock for a paid add-on and an assigned standalone request in place of the add-on unassigned expiry; Pending activation plan status; Hairline-team actions on Screen 14 and a confirm-and-activate step after a handover; reassignment has no automatic refund and the handover fee in the treatment-linked flow is paid from Hairline revenue; add-on alternative template only at the price already paid; aftercare participation as a provider profile setting owned by FR-015; a new standalone request after a rejected or expired FR-038 conversion; discount codes removed from templates; Screen 15 availability marks. | Product Owner / Documentation |
| 2026-11-25 | 1.15 | New rule REQ-011-102: Contact Support on the patient Aftercare Dashboard sends a text message to the aftercare team, recorded in the aftercare communication log, not in FR-012 messaging. Closes the gap between this FR (contact the aftercare team) and FR-012 (aftercare-team chat out of scope). | Claude (AI Assistant) |
| 2026-11-25 | 1.16 | Owner ruling 2026-11-25: the Contact Support route of REQ-011-102 is confirmed, and new rule REQ-011-103 says how the aftercare team's reply reaches the patient: a Messages list on the Aftercare Dashboard plus the `aftercare.team_message` notification by push and email. | Claude (AI Assistant) |
| 2026-11-25 | 1.17 | Backlog points settled: system PRD Platform-Wide Rules are cited by id (REQ-SYS-001, -002, -004, -009); the handover fee and the subscription refund cite FR-017 REQ-017-203 and REQ-017-202; the dangling line reference in the Screen 7 notes and the uncited communication-logging line are fixed. No requirement behaviour changed. | Claude (AI Assistant) |

## Appendix: Approvals

Approved by the Product Owner as part of the requirements baseline of 2026-11-25. Record: `project-requirements/baseline-sign-off.md`. Changes after that date are listed in the Change Log above.

---

**Last Updated**: 2026-11-25
