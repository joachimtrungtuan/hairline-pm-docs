# FR-030 - Notification Rules & Configuration

**Module**: A-09: System Settings & Configuration | S-03: Notification Service
**Feature Branch**: `fr030-notification-rules-config`
**Created**: 2025-11-13
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-030 from system-prd.md

---

## Executive Summary

The Notification Rules & Configuration module provides comprehensive administrative control over the Hairline platform's notification system. This module enables admins to configure event-to-notification mappings, define delivery channels (email, push, and SMS in future phases), manage notification templates, and establish recipient preferences across all three platform tenants (Patient, Provider, Admin). By centralizing notification configuration, the system ensures consistent, timely, and appropriate communication with all platform users while maintaining flexibility to adapt notification strategies as the business evolves. **In MVP, only email and push are available; SMS is an optional channel planned for later phases once S-03 SMS support is enabled.**

This module extends the foundational OTP template management capabilities from FR-026 (App Settings & Security Policies) to encompass all notification types across the platform, creating a unified notification governance system.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (Mobile App)**: Receives notifications based on configured rules; users cannot modify system-level notification rules but can manage their personal preferences
- **Provider Platform (Web)**: Receives notifications based on configured rules; providers can manage personal notification preferences within admin-defined boundaries
- **Admin Platform (A-09)**: Full administrative control over notification rule configuration, template management, channel preferences, and testing capabilities
- **Shared Services (S-03)**: Notification Service executes configured rules, manages delivery across channels, tracks delivery status, and maintains notification logs

### Multi-Tenant Breakdown

**Patient Platform (Mobile App)**:

- Patients receive notifications triggered by system events (quote submitted, booking confirmed, payment due, aftercare milestone, etc.)
- Patients can view notification history in-app (REQ-030-107)
- Patients can manage personal notification preferences within boundaries set by admin (e.g., cannot disable critical payment notifications) (REQ-030-106)
- Notifications delivered via email and push notifications in MVP; SMS delivery is optional and only becomes available in later phases when enabled in S-03/FR-020. (REQ-030-108)

**Provider Platform (Web)**:

- Providers receive notifications for inquiries, quote responses, booking confirmations, payment receipts, patient arrivals, aftercare escalations
- Provider team notifications are routed by team role only, fixed by the system; the clinic cannot choose which team member receives which notification (REQ-030-109)
- Notifications delivered via email and web push notifications (REQ-030-111)

**Admin Platform (A-09)**:

- Admins configure notification rules: which events trigger notifications, to whom, via which channels
- Admins create and edit notification templates with dynamic variables and multi-language support
- Admins define channel preferences per event type and recipient type (REQ-030-112)
- Admins test notification rules before activation
- Admins monitor notification delivery metrics and troubleshoot failed deliveries (REQ-030-113)
- Admins manage notification escalation rules for time-sensitive events (REQ-030-114)
- Admins set one platform-wide quiet-hours period for non-urgent notifications (REQ-030-224)

**Shared Services (S-03)**:

- S-03 Notification Service consumes configured rules from A-09 (REQ-030-115)
- Evaluates event triggers in real-time and determines recipients and channels
- Renders notification templates with dynamic data (REQ-030-116)
- Manages delivery queue and retry logic for failed deliveries
- Tracks delivery status (sent, delivered, opened, failed) per channel (REQ-030-117)
- Provides delivery logs and metrics to A-09 for monitoring

### Communication Structure

**In Scope**:

- Email notification configuration and template management
- Push notification (mobile and web) configuration and template management
- SMS notification configuration for critical events (optional, admin-enabled, **not available in MVP; SMS becomes usable only when S-03 SMS delivery is implemented in a later phase**)
- Event-to-notification mapping (which events trigger which notifications)
- Recipient rule configuration (who receives notifications based on role, relationship, preferences)
- Channel preference configuration per event type and recipient type
- Notification template editor with variable substitution and preview
- Multi-language notification template support (REQ-030-152, REQ-030-154)
- Notification testing and preview capabilities
- Delivery status tracking and retry management
- Notification analytics and delivery metrics
- Notification preference records: patient preferences (including messaging notification preferences) and provider preferences, which the profile screens in FR-001 and FR-032 show and edit; the provider team routing record is also owned here but no screen edits it

**Out of Scope**:

- Real-time chat/messaging between users (handled by P-06: Communication) (REQ-030-213)
- Video consultation notifications (covered under aftercare-specific notifications) (REQ-030-214)
- Third-party notification platform integrations beyond email, SMS, push (e.g., WhatsApp, Telegram - future enhancement) (REQ-030-215)
- User-to-user notification forwarding or sharing (REQ-030-216)
- Notification content personalization based on AI/ML (future enhancement) (REQ-030-217)
- Per-member editing of provider team notification routing (which team member receives which notification): not in launch scope; at launch routing is by team role only and fixed by the system

### Entry Points

Admins access notification configuration through:

1. **Admin Dashboard → Settings → Alerts & Notifications**: Primary entry point for notification rule management and notification template setup (REQ-030-118)
2. **Event-driven**: System events automatically trigger notification evaluation based on configured rules (S-03)
3. **Template Testing**: Admins can send test notifications to themselves before activating rules (REQ-030-120)

Activation method: A new notification rule starts as Draft and is not executed until an admin activates it; activation takes effect immediately after the confirmation prompt. Changes saved to an already active rule apply immediately to future events. Template changes apply to new notifications immediately; in-flight notifications use the template version active at creation time. (REQ-030-119, REQ-030-149, REQ-030-150, REQ-030-174)

---

## Admin-Configurable Notification Event Catalog (Preset by Backend)

### Core Rule

- The list of notification events that appear in **`Settings → Alerts & Notifications`** is a **preset backend event catalog**.
- Admins can **only configure events that appear in this catalog UI** (enable/disable, channels, timing, templates, retries, escalation). (REQ-030-121)
- **If an event does not appear in the catalog UI, it cannot be configured** (it is either not implemented, not enabled for the current environment, or intentionally not exposed).
- Event payloads are recipient-scoped. Configurable templates may reference only the allowlisted variables exposed for that event, outcome, and recipient type. (REQ-030-122)
- **Event ownership**: every event that produces a notification is owned by FR-030 and listed in this catalog, including events triggered by other features (the producing feature is named in the Notes). An event that produces no notification is owned by the feature that triggers it and is not listed here. (REQ-030-233)

### MVP: Admin-Configurable Event Types (Shown in UI)

Below is the platform-wide set of events that MUST be configurable by admins in MVP. This table is the **source of truth** for MVP notification event coverage (FR-020 must align to this catalog). (REQ-030-123)

Notes:

- **Backend event keys** below are the **final canonical keys**. They MUST remain stable identifiers exposed via the event catalog API. (REQ-030-124)
- If an event is not present in this table, it should **not appear** in `Settings → Alerts & Notifications` and therefore **cannot be configured**.

| Category | Event (Display Name) | Backend Event Key | Primary Recipients | Notes | Rule |
|----------|-----------------------|---------------------------|--------------------|-------|------|
| Account/Auth | Email Verification / OTP Code | `account.email_verification_code` | Patient, Provider, Admin | Extends FR-026 OTP templates; **security-critical** and non-disableable by default | REQ-030-027 |
| Account/Auth | Email Change Code | `account.email_change_code` | Patient | 6-digit code sent to the new address when a patient changes the profile email (FR-001); its own event, separate from the registration code; **security-critical** and non-disableable by default | no graph Rule |
| Account/Auth | Password Reset Code / Link | `account.password_reset` | Patient, Provider, Admin | **Security-critical** and non-disableable by default | REQ-030-028 |
| Account/Auth | New Account Created (Welcome / Onboarding) | `account.created` | Patient | Optional; can be disabled if not needed. Provider onboarding uses `provider.activation` instead | REQ-030-029 |
| Inquiry | Inquiry Submitted (Provider notified) | `inquiry.submitted` | Provider | “New inquiry matching clinic/location” | REQ-030-030 |
| Inquiry | Inquiry Cancelled | `inquiry.cancelled` | Patient, Provider, Admin (optional) | Patient-initiated inquiry cancellation (FR-003 Workflow 5). Fires when patient cancels inquiry in Inquiry, Quoted, or Accepted stages. Patient receives mandatory cancellation confirmation (aligns with FR-003 Workflow 5 step 4 and Screen 8b). Cancellation reason is patient-private — provider notification says only "Inquiry cancelled by patient". **MVP default channels: Email + Push.** Available template variables differ by recipient: Patient receives `inquiry.id`, `inquiry.cancellation_reason`, `inquiry.cancelled_at`; Provider receives `inquiry.id`, `inquiry.cancelled_at` only (reason excluded per privacy rule). **Provider exclusion**: a provider that has a live quote on the inquiry does not receive `inquiry.cancelled`; that provider receives only `quote.cancelled_inquiry`. A provider without a quote on the inquiry still receives `inquiry.cancelled`. | REQ-030-031, REQ-030-219 |
| Inquiry | Inquiry Response SLA Breached | `inquiry.ttfq_sla_breached` | Provider | FR-014 REQ-014-113. Fires once per distributed inquiry/provider pair when the provider has not submitted a parent quote within the FR-026 Analytics Configuration TTFQ SLA target (default 120 minutes) from distribution. Recipients: provider users permitted to respond to inquiries (FR-009). Not sent if the inquiry is cancelled, the distribution is withdrawn, or the provider responds first; never repeated for the same pair. MVP default channel: in-app only; email/push off by default and admin-configurable | REQ-030-032 |
| Quote | Quote Submitted / Ready (Patient notified) | `quote.submitted` | Patient | Fired by FR-004 when the provider sends the parent quote; the quote expiry is set and governed by FR-004. The notice shows the "From" price (the lowest subquote price in the parent quote, in the quote currency), the option count, the treatment and the expiry date. Exact subquote prices are not shown before acceptance (see Quote, Booking and Treatment-Change Event Rules) | REQ-030-033 |
| Quote | Quote Revised (New Version) | `quote.updated` | Patient, Provider | Fired by FR-004 when a new version of an already-sent parent quote is re-sent to the patient. The notice describes the quote as revised (new version). Drafts that were never sent do not fire this event | REQ-030-034 |
| Quote | Quote Expiring Soon | `quote.expiring_soon` | Patient, Provider | Fired by FR-004 once per sent parent quote when the time left before expiry reaches the quote-expiring-soon lead time set by admin in FR-026. Never fired for drafts or for accepted, withdrawn or cancelled quotes. Admin-configurable | REQ-030-035 |
| Quote | Quote Expired | `quote.expired` | Patient, Provider | Sent on expiry processing completion | REQ-030-036 |
| Quote | Quote Restored | `quote.restored` | Patient, Provider | Fired by FR-004 when an admin restores an expired quote (a reason is required). The quote returns to sent status with a fresh full expiry window: the restore time plus the FR-026 quote validity window in force. The patient is told the quote is available again with its new expiry date; the provider is told the quote was restored and its new expiry date. Admin-configurable; MVP default channels: Email + Push | REQ-030-218 |
| Quote | Quote Withdrawn | `quote.withdrawn` | Patient, Admin (only when the quote was already accepted) | Fired by FR-004 when a provider withdraws a sent parent quote, before or after acceptance. The patient is always told. Admins receive it as an exception alert only when the withdrawn quote was already accepted; a withdrawal before acceptance is a normal provider action and does not alert admins. After acceptance, FR-006 hands the case to the provider-fault transfer and the patient also receives `booking.provider_fault_replacement`. **Mandatory before and after acceptance — admin cannot disable this event** (see Non-Disableable by Default section) | REQ-030-037 |
| Quote | Quote Accepted / Subquote Outcomes | `quote.accepted` | Provider | FR-005 uses the existing event with `outcome` = `selected_subquote_accepted`, `sibling_subquote_not_selected`, or `competing_parent_cancelled_other_subquote_accepted`. Selected-provider templates may use accepted-subquote details. Non-selected-provider templates are restricted to that provider's own parent quote/subquote references, outcome, and reason; selected provider identity and accepted price are unavailable. Each provider receives one notice per sent parent quote: the provider of the accepted parent quote receives `selected_subquote_accepted`, with that parent's sibling subquotes listed in the same notice as `sibling_subquote_not_selected`; each other sent parent quote produces one not-selected notice (`competing_parent_cancelled_other_subquote_accepted`) to its provider, including another parent quote of the selected provider. Unsent drafts cancelled by FR-004 produce no notice. **The selected-provider and not-selected-provider outcomes are mandatory — admin cannot disable them** (see Non-Disableable by Default section). The patient is not a recipient: at acceptance the patient receives only `booking.scheduled`. No admin notification is sent for an acceptance; admins follow acceptances on their dashboards | REQ-030-038, REQ-030-133 |
| Quote | Quote Cancelled (Inquiry Cancelled) | `quote.cancelled_inquiry` | Provider | Auto-cancelled quote due to patient inquiry cancellation (FR-003 Workflow 5). **Provider receipt is mandatory — admin cannot disable this event** (see Non-Disableable by Default section). Cancellation reason is patient-private; provider notification says only "Inquiry cancelled by patient". **MVP default channels: Email + Push.** Not subject to FR-032 provider notification preferences; FR-032 offers no toggle for this event. Available template variables: `quote.id`, `quote.provider_id`, `inquiry.id`, `inquiry.cancelled_at`; `inquiry.cancellation_reason` is excluded per privacy rule. A provider with a live quote receives this notice only, never also `inquiry.cancelled`; a provider without a quote still receives `inquiry.cancelled`. | REQ-030-039 |
| Booking/Schedule | Booking Accepted — Slot Held (Pending Payment) | `booking.scheduled` | Patient | Fired by FR-006 when subquote acceptance creates the slot hold, or when an admin-authored replacement acceptance in the FR-006 provider-fault transfer creates the replacement booking, before the first payment is confirmed; states the payment deadline (hold expiry). The provider is not a recipient: the accepted or replacement provider learns of the booking through `quote.accepted` (`selected_subquote_accepted`). **Mandatory — admin cannot disable this event** | REQ-030-040 |
| Booking/Schedule | Hold Expiring Soon (Payment Reminder) | `booking.hold_expiring_soon` | Patient, Admin | Fired by FR-006 once per slot hold when the time left before the hold expires reaches the hold-expiring-soon lead time set by admin in FR-026 and the first payment is still outstanding. Reminds the patient to pay before the slot is released; admins receive it as an exception alert (slot hold expiring while unpaid). Admin-configurable | REQ-030-041 |
| Booking/Schedule | Payment Window Expired | `booking.payment_window_expired` | Patient, Provider, Admin | Fired by FR-006 when the slot hold expires before the first payment (deposit or first instalment) succeeds; applies only to that first payment step. Patient is told the booking lapsed and given the recovery routes (cancel and start a new inquiry, or contact support); provider is told the slot is free; admins receive it as an exception alert. **Mandatory — admin cannot disable this event** | REQ-030-042 |
| Booking/Schedule | Booking Revived | `booking.revived` | Patient, Provider | Fired by FR-006 when an admin revives a booking after Payment Window Expired. Patient receives the new payment deadline; provider is told the slot is held again. **Mandatory — admin cannot disable this event** | REQ-030-043 |
| Booking/Schedule | Provider Unable to Proceed — Replacement Being Arranged | `booking.provider_fault_replacement` | Patient, Admin | Fired by FR-006 when an accepted booking is closed for provider fault: the provider withdraws after acceptance, drops out before treatment starts, or is suspended or deactivated after acceptance and before treatment starts (FR-015). An `In Progress` booking is not closed for provider fault and never fires this event; it stays `In Progress` with `supportRequired` for an admin decision. Tells the patient that an admin will arrange a replacement provider within the same inquiry and that the patient pays no cancellation fee; MUST NOT expose confidential suspension or deactivation reasons. Admins receive it as an exception alert so they can arrange the replacement. Providers are not recipients: the replacement provider learns through the normal new-booking and acceptance notice, and the faulted provider is not notified by this event. **Mandatory — admin cannot disable this event** | REQ-030-044 |
| Booking/Schedule | Booking Confirmed | `booking.confirmed` | Patient, Provider | Critical | REQ-030-045 |
| Booking/Schedule | Booking Rescheduled | `booking.rescheduled` | Patient, Provider | Fired by FR-006 when an admin changes the appointment date or time of an `Accepted` or `Confirmed` booking (FR-006 Change Appointment). States the previous and the new appointment, read from the booking's current appointment. **Mandatory — admin cannot disable this event**; not subject to FR-032 provider notification preferences | REQ-030-046 |
| Booking/Schedule | Booking Cancelled | `booking.cancelled` | Patient, Provider, Admin (optional) | Include cancellation reason where appropriate | REQ-030-047 |
| Booking/Schedule | Appointment Reminder | `booking.appointment_reminder` | Patient, Provider | Scheduled reminders; policy-driven | REQ-030-048 |
| Treatment | Treatment Start / Day-1 Starting | `treatment.started` | Patient, Provider | “Treatment start notifications” | REQ-030-049 |
| Treatment | Treatment Details Changed After Acceptance | `treatment.plan_changed` | Patient | Fired by FR-010 when the clinic or an admin makes an audited change to the treatment plan, assigned clinicians or graft count from booking confirmation (`Confirmed`) onward. States what changed; price, currency and other money terms never change through this path. **Mandatory — admin cannot disable this event** | REQ-030-050 |
| Treatment | Treatment Cancelled | `treatment.cancelled` | Patient, Provider, Admin (optional) | Used when treatment is cancelled after scheduling/confirmation | REQ-030-051 |
| Treatment | Treatment Completed (Post‑Op Instructions) | `treatment.completed` | Patient, Provider, Admin (optional) | Completion confirmation; triggers post-op and aftercare next steps. The patient copy also states the deadline to raise a problem with the treatment and links to the support request; the provider and admin copies keep their wording without the deadline. No separate event is created for this | REQ-030-052 |
| Treatment | Treatment Documentation Completed | `treatment.documentation_completed` | Provider | Sent when treatment documentation is successfully saved | REQ-030-053 |
| Treatment | Task In Progress Reminder | `treatment.task_in_progress_reminder` | Provider | Reminder for incomplete treatment tasks or documentation | REQ-030-054 |
| Payment | Payment Received / Receipt | `payment.received` | Patient, Provider, Admin (optional) | Critical | REQ-030-055 |
| Payment | Payment Failed | `payment.failed` | Patient, Admin (optional) | Critical | REQ-030-056 |
| Payment | Payment Due Reminder (Installment / Balance) | `payment.due_reminder` | Patient | “Installment reminder” (split-pay compatible). When the reminder goes out is the single payment reminder timing setting owned by FR-007; this entry does not keep a second reminder schedule | REQ-030-057 |
| Billing/Payouts | Provider Payout Processed | `payout.provider_processed` | Provider, Admin (optional) | “They’ve been paid” notification to provider. Also sent when a manual statement is marked paid, not only for Stripe payouts; no separate event exists for manual statements | REQ-030-058 |
| Billing/Payouts | Affiliate Payout Processed | `payout.affiliate_processed` | Affiliate, Admin (optional) | If affiliate program is enabled | REQ-030-059 |
| Billing/Payouts | Payout Failed | `payout.failed` | Admin, Provider (optional), Affiliate (optional) | Failure processing payout; recipients depend on payout type | REQ-030-060 |
| Billing/Payouts | Payout Paused — Problem Raised | `payout.paused_problem_raised` | Admin | Fired when a problem is raised on a completed treatment and the clinic's money for that booking is paused; tells admins which booking and clinic are affected, with a link to the support request. MVP default channels: Email + Push | REQ-030-220 |
| Billing/Payouts | Funds Released to Clinic | `payout.funds_released` | Provider | Fired when money held for a booking is released to the clinic; states the booking and the amount released. MVP default channels: Email + Push | REQ-030-221 |
| Billing/Payouts | Cancellation Charge Deducted | `payout.cancellation_charge_deducted` | Provider | Fired when a cancellation charge is deducted from the clinic's money; states the booking, the amount deducted and that the reason is a cancellation. MVP default channels: Email + Push | REQ-030-222 |
| Messaging/Support | New Message Received | `message.received` | Patient, Provider, Admin (optional) | Real-time notification for new messages | REQ-030-061 |
| Messaging/Support | Support Case Created | `support.case_created` | Patient, Provider, Admin | Sent to submitter confirming case creation with case ID; Admin notification if case is urgent or unassigned | REQ-030-062 |
| Messaging/Support | Support Case Assigned | `support.case_assigned` | Admin | Sent to assigned admin when case is assigned to them | REQ-030-063 |
| Messaging/Support | Support Case Status Changed | `support.case_status_changed` | Patient, Provider | Sent when case status changes (Open → In Progress, In Progress → Resolved); includes status update and context | REQ-030-064 |
| Messaging/Support | Support Case Admin Reply | `support.case_admin_reply` | Patient, Provider | Sent when admin replies to case in communication thread; includes message content | REQ-030-065 |
| Messaging/Support | Support Case User Reply | `support.case_user_reply` | Admin | Sent to assigned admin (or all support staff if unassigned) when patient/provider replies to case | REQ-030-066 |
| Messaging/Support | Support Case Resolved | `support.case_resolved` | Patient, Provider | Sent when case is marked as Resolved; includes resolution summary and feedback resolution (if applicable) | REQ-030-067 |
| Messaging/Support | Support Case Reopened | `support.case_reopened` | Patient, Provider, Admin | Sent when closed case is reopened; includes reopening reason | REQ-030-068 |
| Messaging/Support | Support Case Closed | `support.case_closed` | Patient, Provider | Sent when case is closed (final status); includes resolution summary | REQ-030-069 |
| Messaging/Support | Support Case Escalated | `support.case_escalated` | Admin | Sent to escalation recipient (senior admin or technical team) when case is escalated | REQ-030-070 |
| Aftercare | Aftercare Activated | `aftercare.activated` | Patient, Provider | Includes assigned provider/clinician info where applicable | REQ-030-071 |
| Aftercare | Aftercare Milestone Due | `aftercare.milestone_due` | Patient, Provider (optional) | Milestone-driven reminders | REQ-030-072 |
| Aftercare | Scan Due / Missed Scan Reminder | `aftercare.scan_due` / `aftercare.scan_missed` | Patient | “Missed scans MUST trigger reminder notifications” | REQ-030-073 |
| Aftercare | Questionnaire Due / Missed Questionnaire Reminder | `aftercare.questionnaire_due` / `aftercare.questionnaire_missed` | Patient | “Questionnaire due” + reminder if missed | REQ-030-074 |
| Aftercare | Aftercare Escalation / Red Flag Triggered | `aftercare.escalation_triggered` | Provider, Admin, Patient (optional) | Critical; escalation recipients configurable | REQ-030-075 |
| Aftercare | Standalone Aftercare Payment Confirmed | `aftercare.standalone_payment_confirmed` | Patient, Provider (optional), Admin (optional) | Used for standalone aftercare flow payment confirmation | REQ-030-076 |
| Aftercare | Aftercare Provider Reassigned | `aftercare.provider_reassigned` | Patient, Provider (new aftercare provider) | Fired by FR-011 when an admin reassigns an aftercare case to another provider or the Hairline aftercare team, including an `Aftercare` booking reassigned through FR-006 Alternative Flow B6, an `In Progress` booking that the admin moves to `Aftercare` with reassignment, and an FR-011 standalone aftercare case. Tells the patient who now provides aftercare and gives the new provider the case reference; MUST NOT expose confidential suspension or deactivation reasons. No admin alert is sent because the admin is the actor. **Mandatory — admin cannot disable this event**; not subject to FR-032 provider notification preferences | REQ-030-077 |
| Monitoring | Monitoring Case Pending Assignment | `monitoring.assignment_pending` | Admin | Advice-mode hair-loss/transplant-progress monitoring case activated and awaiting provider assignment (FR-037/FR-038) | REQ-030-078 |
| Monitoring | Monitoring Provider Assigned | `monitoring.provider_assigned` | Patient, Provider | Initial assignment or reassignment; assignment type distinguished in payload (FR-037/FR-038) | REQ-030-079 |
| Monitoring | Monitoring Provider Withdrawn | `monitoring.provider_withdrawn` | Admin, Patient | Provider withdraws with reason; case returns to Admin as Pending Reassignment (FR-037/FR-038) | REQ-030-080 |
| Monitoring | Monitoring Provider Reassigned | `monitoring.provider_reassigned` | Patient, Provider | Replacement provider assigned after withdrawal; replacement receives history and next eligible advice date (FR-037/FR-038) | REQ-030-081 |
| Monitoring | Monitoring Advice Posted | `monitoring.advice_posted` | Patient | Provider submits or edits the one advice-window paragraph for the current window (FR-037/FR-038) | REQ-030-082 |
| Monitoring | Monitoring Case Completed | `monitoring.completed` | Patient | Patient completes the active monitoring case (FR-037/FR-038) | REQ-030-083 |
| Monitoring | Monitoring PDF Export Ready | `monitoring.export_ready` | Patient | Date-to-date summary PDF has finished generating and is downloadable (FR-037/FR-038) | REQ-030-084 |
| Monitoring | Monitoring Converted to Inquiry | `monitoring.converted_to_inquiry` | Patient | Monitoring case successfully converts into a distinct FR-003 inquiry (FR-037/FR-038) | REQ-030-085 |
| Monitoring | Monitoring Aftercare Conversion Started | `monitoring.aftercare_conversion_started` | Patient | Fired by FR-038 when the patient selects Switch to Aftercare Package on a transplant-progress case, before the aftercare request is created; tells the patient the switch has started. Patient only; sent immediately | REQ-030-223 |
| Monitoring | Monitoring Converted to Aftercare | `monitoring.converted_to_aftercare` | Patient | Fired by FR-038 when the standalone aftercare request from the Switch to Aftercare Package flow is successfully created; tells the patient the switch is complete. Patient only (FR-037/FR-038) | REQ-030-229 |
| Reviews | Review Request | `review.requested` | Patient | “Review notifications” (typically post-treatment). The admin sets when the review invitation and any reminder are sent through this event's delivery timing; FR-013 does not set its own invitation timing | REQ-030-086 |
| Reviews | Review Published / New Review Posted | `review.published` | Provider | Notifies provider when a new published review appears on their profile; subject to provider Review Notifications preference in FR-032 | REQ-030-087 |
| Reviews | Provider Response Posted | `review.response_posted` | Patient | Notifies reviewer when provider posts a public response to their review | REQ-030-088 |
| Reviews | Review Removed by Admin | `review.removed_by_admin` | Patient | Notifies reviewer when admin removes their published review for policy/compliance reasons | REQ-030-089 |
| Reviews | Takedown Request Decided | `review.takedown_decided` | Patient | Notifies patient of admin approve/reject decision on their takedown request | REQ-030-090 |
| Promotions/Discounts | Provider Approval Needed for Platform Discount | `promotion.discount_approval_requested` | Provider | “Approval notifications to providers when new platform discount is created” | REQ-030-091 |
| Provider/Compliance | Provider Onboarding Requested | `provider.onboarding_requested` | Admin | New provider onboarding request awaiting review/approval. Not triggered at launch (future) | REQ-030-092 |
| Provider/Compliance | Provider Document Expiration Warning | `provider.document_expiration_warning` | Admin, Provider (optional) | License/credential expiry warnings; timing is policy-driven. Not triggered at launch (future) | REQ-030-093 |
| Provider/Compliance | Provider-Caused Cancellation / Offer Unavailable | `provider.status_cancellation_patient` | Patient | FR-015 Alternative Flow A5 / Screen 4 (FR-020 REQ-020-013). One per affected inquiry/case when provider suspension (`ProviderSuspended`) or deactivation (`ProviderDeactivated`) cancels the patient's case or the provider's offer before acceptance. For a case already accepted, the patient instead receives `booking.provider_fault_replacement`. Before acceptance, three variants apply (FR-003 Workflow 2 Alternative Flow B4, REQ-003-021): when other offers remain open, the notice says "[Clinic] is no longer available. Your other offers are still open."; when no other live offer remains and the inquiry is redistributed automatically, the notice says "[Clinic] is no longer available. We are finding new offers for you."; when the patient had explicitly selected the affected provider, the notice asks the patient to confirm the redistribution first. Includes inquiry/case reference and a Contact Admin/Support action. MUST NOT say the patient cancelled, instruct payment against the cancelled selection, or expose confidential suspension/deactivation reasons. **Mandatory — admin cannot disable this event** (see Non-Disableable by Default section); sent regardless of FR-015's "Notify Provider" checkbox. **MVP default channels: Email + Push + in-app** (global patient toggles still apply to Email/Push; in-app record always created). Retries de-duplicated per provider-status event + affected record + recipient | REQ-030-094 |
| Provider/Compliance | Provider-Caused Cancellation — Admin Support Required | `provider.status_cancellation_admin_support` | Admin | Same trigger (FR-020 REQ-020-013), and also when a provider-status event leaves an `In Progress` booking open and flagged `supportRequired` for an admin decision (move the booking to `Aftercare` with aftercare reassignment, or cancel it with a reason), or leaves an `Aftercare` booking or FR-011 standalone aftercare case flagged for admin aftercare reassignment (FR-006 Alternative Flow B6). Mandatory admin-support alert per affected inquiry/case with patient, inquiry/case reference, prior stage, cause, and FR-016 deep link (Admin Support Required filter). Sent to admins with the FR-031 Respond to Support permission (default roles Super Admin, Aftercare Specialist, and Support Staff); opening the FR-016 list also requires View Patients. **Mandatory — admin cannot disable this event**; sent regardless of "Notify Provider"; pinned as critical in the admin dropdown. No FR-034 ticket is auto-created. Retries de-duplicated per provider-status event + affected record + recipient | REQ-030-095 |
| Provider/Compliance | Provider Suspended / Deactivated | `provider.suspended` / `provider.deactivated` | Provider (Owner only) | FR-015 Screen 4 (FR-020 REQ-020-014). Sent only when "Notify Provider" is checked (default); always sent for a deactivation that processes an FR-032 account-closure request (FR-015 A7 locks Notify Provider on; FR-020 REQ-020-016). For a scheduled change it is sent when the scheduled change is created (with the effective date) and again when it takes effect; with "Notify Provider" unchecked it is sent at neither point. Team members are not emailed. Email with action taken, admin-provided reason, effective date (if scheduled), and admin support contact. Unaffected by provider FR-032 category preferences (account notice) | REQ-030-096 |
| Provider/Compliance | Provider Account Activation (Welcome / Set Password) | `provider.activation` | Provider | FR-015 Main Flow step 13 and Alternative Flow A1 (FR-020 REQ-020-015). Welcome email with login email, first-login instructions, and the one-time set-password link (expires in 24 hours); re-sent on A1 resend. **Mandatory; toggle locked.** Email only | REQ-030-097 |
| Provider/Compliance | Owner Login Email Changed | `provider.login_email_changed` | Provider (old and new login address) | FR-015 Screen 3 Tab 1 Owner login email change by an admin (FR-020 REQ-020-015). One email to the old address (the login email for [clinic] was changed to [new address, partly masked] by a Hairline admin on [date/time]; contact support if unexpected) and one to the new address (this address is now the login email for [clinic]). `provider.activation` is also sent to the new address when `password_set` is false. **Mandatory security notice; toggle locked.** Unaffected by FR-032 category preferences. Email only | REQ-030-098 |
| Provider/Compliance | Provider Reactivated | `provider.reactivated` | Provider (Owner only) | FR-015 Alternative Flow A6 / Screen 5 (FR-020 REQ-020-015). Sent only when "Notify Provider" is checked (default). Email with reactivation notice, admin-provided reason, admin support contact, and a note that cancelled cases are not restored (and that any notified scheduled change no longer applies). **Mandatory when triggered; toggle locked.** Unaffected by FR-032 category preferences | REQ-030-099 |
| Provider/Compliance | Scheduled Status Change Cancelled | `provider.scheduled_change_cancelled` | Provider (Owner only) | FR-015 Screen 4 Cancel Scheduled Change (FR-020 REQ-020-015). Sent when an admin cancels a pending scheduled suspension/deactivation that had "Notify Provider" checked; states the cancelled change and its former effective date. **Mandatory when triggered; toggle locked.** Unaffected by FR-032 category preferences | REQ-030-100 |
| Provider/Compliance | Provider Account-Closure Requested | `provider.closure_requested` | Admin | FR-032 Request Account Closure / FR-015 A7 (FR-020 REQ-020-016). Sent to admins with View Providers permission when a provider submits a closure request; includes provider, clinic, request date, optional reason, and a deep link to the request in the FR-015 provider profile. **Mandatory; toggle locked.** Email + in-app | REQ-030-101 |
| Provider/Compliance | Provider Account-Closure Request Rejected | `provider.closure_rejected` | Provider | FR-015 A7 step 6 (FR-020 REQ-020-016). Sent when an admin rejects a closure request; states that the account stays Active and gives the admin review notes and support contact. **Mandatory; toggle locked.** Unaffected by FR-032 category preferences. Email only | REQ-030-102 |
| System/Operations | System Escalation | `system.escalation` | Admin | Operational escalation events requiring admin action | REQ-030-103 |
| System/Operations | System Alert | `system.alert` | Admin | System health/monitoring alerts surfaced via notifications | REQ-030-104 |
| System/Operations | Analytics Export Ready | `analytics.export_ready` | Provider | FR-014 REQ-014-062/063. A one-off or scheduled provider analytics export (PDF or CSV) has finished generating. Sent to the provider's registered email and each selected recipient; email carries the PDF attachment where applicable plus a secure download link that expires after 48 hours; in-app notification links to Report History. Default channels: email + in-app | REQ-030-105 |

### Quote, Booking and Treatment-Change Event Rules

- **Producers**: FR-004 produces `quote.submitted`, `quote.updated`, `quote.expiring_soon`, `quote.expired`, `quote.restored` and `quote.withdrawn`. FR-005 produces `quote.accepted` and its outcomes. FR-006 produces `booking.scheduled`, `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.rescheduled` and `booking.provider_fault_replacement`. FR-010 produces `treatment.plan_changed`.
- **Recipient grain for `quote.accepted`**: one provider notice per sent parent quote, never one per subquote. The de-duplication key is acceptance record + parent quote + recipient. Drafts produce no notice. (REQ-030-129)
- **Pre-acceptance price variables**: `quote.submitted`, `quote.updated`, `quote.expiring_soon`, `quote.expired` and `quote.withdrawn` may use only parent-level variables: the "From" price (lowest subquote price in the parent quote) with its currency, option count, treatment, expiry date, provider name and the parent quote reference. A single quote total does not exist and MUST NOT be offered as a variable. (REQ-030-130)
- **Post-acceptance money variables**: on `quote.accepted` (selected-provider outcome) and on every `booking.*` event, price, currency, date range and promotion variables resolve from the accepted snapshot recorded at acceptance, never from the live parent quote, Quote Option or package. Appointment variables on `booking.*` events resolve from the booking's current appointment, which an admin may change through FR-006; the snapshot keeps the accepted appointment as the baseline. `booking.rescheduled` carries both the previous and the new appointment. Allowed references are the parent quote, accepted subquote, quote version and acceptance record identifiers. (REQ-030-131)
- **Treatment-detail variables**: `treatment.plan_changed` and other treatment events may use the current treatment plan, clinicians and graft count maintained through FR-010; they MUST NOT carry changed money values. (REQ-030-132)
- **Not-selected allowlist**: See REQ-030-038.
- **Locks**: `quote.withdrawn`, the selected-provider and not-selected-provider outcomes of `quote.accepted`, `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement`, `booking.scheduled`, `booking.rescheduled` and `treatment.plan_changed` are mandatory. `quote.expiring_soon` and `booking.hold_expiring_soon` are admin-configurable (REQ-030-134). See REQ-030-138.
- **Acceptance recipients**: at acceptance the patient receives only `booking.scheduled`; `quote.accepted` goes to providers only (the accepted provider and each not-selected provider). No admin notification is sent for an acceptance. The same applies to an admin-authored replacement acceptance in the FR-006 provider-fault transfer: the patient receives `booking.scheduled` with the replacement payment deadline, and the replacement provider receives `quote.accepted` (`selected_subquote_accepted`). (REQ-030-135)
- **Admin exception alerts**: admins are alerted only for exceptions on the quote-to-booking path: a slot hold expiring while the first payment is unpaid (`booking.hold_expiring_soon`), Payment Window Expired (`booking.payment_window_expired`), provider fault (`booking.provider_fault_replacement`) and a provider withdrawing a quote that was already accepted (`quote.withdrawn`). Routine acceptances are visible on admin dashboards only. (REQ-030-136)

### Post‑MVP / Hidden Events (Not Shown in UI Until Enabled)

These event types may exist in backend roadmap but MUST NOT appear in admin UI until the backend supports them end-to-end and product enables them. (REQ-030-126, REQ-030-127)

| Category | Event (Display Name) | Backend Event Key | Notes |
|----------|-----------------------|---------------------------|-------|
| Channels | SMS Delivery Enabled | `channel.sms_enabled` | SMS is future; **not available in MVP** |
| Aftercare | Medication / Washing / Activity Reminders | `aftercare.medication_reminder` / `aftercare.washing_reminder` / `aftercare.activity_reminder` | Scheduled reminders referenced in system PRD; enable when milestone engine supports schedules |
| Travel | Passport / Travel Document Required | `travel.passport_required` | Only show once travel module + event publishing exists |
| Travel | Flight / Hotel Itinerary Updates | `travel.itinerary_updated` | Post‑release travel roadmap |
| Quote | Quote Declined | `quote.declined` | Reserved for an explicit governed decline flow; no MVP producer exists because patients have no explicit decline action (FR-005). FR-005 sibling Not Selected and competing-parent cancellation outcomes do not use this event |

## Business Workflows

### Main Flow: Admin Reviews Event Catalog and Toggles / Configures Notification Rules

**Actors**: Admin (Hairline operations team), S-03 Notification Service (system), Recipient (Patient/Provider)
**Trigger**: Admin opens `Settings → Alerts & Notifications` to review the backend event catalog and (per event) enable/disable notifications and configure channels/timing/templates.
**Outcome**: Selected event(s) are enabled/disabled and/or configured; S-03 uses the saved configuration when those backend events occur

**Steps**:

1. Admin navigates to Admin Platform → `Settings → Alerts & Notifications`
2. System displays the **backend event catalog** (grouped by category) with each row showing current status (Enabled/Disabled), channels, and last modified
3. Admin selects an event row (e.g., "Payment Due Reminder") and reviews its current configuration
4. Admin toggles the event **On/Off**:
   - If toggled **Off**, S-03 will not send notifications for this event (except where policy marks it critical/non-disableable). **Security-critical events (OTP verification, password reset) are non-disableable by default** and must show a locked toggle.
   - If toggled **On**, the event becomes active using its saved configuration
5. Admin clicks **Configure** (or expands the row) to edit settings for that event
6. System displays event-specific configuration options (channels, timing, templates, retries, escalation)
7. Admin configures recipient rules (where applicable):
   - Recipient type: Patient (booking owner)
   - Additional recipients: None (or specify admin roles if escalation needed)
8. Admin configures channel preferences:
   - Email: Enabled (required for payment reminders)
   - Push notification: Enabled
   - SMS: Optional (admin can enable for critical payment reminders in future phases; **SMS is not available in MVP**)
9. Admin selects notification template for each enabled channel:
   - Email template: "Payment Reminder - 3 Days Before Due"
   - Push template: "Payment Due Soon"
   - SMS template: "Payment Reminder" (if enabled in a later phase)
10. Admin configures delivery timing:
    - Trigger: 3 days (72 hours) before installment due date (example only; the payment reminder schedule itself is the single payment reminder timing setting owned by FR-007)
    - Delivery time: 9:00 AM in recipient's local timezone
    - Retry logic: the platform default retry rule (retry on, up to 3 retries, 1 hour apart), or different values set for this notification
11. Admin configures escalation rules (optional):
    - If payment still not received 24 hours after reminder, escalate to admin billing team
12. Admin previews notification templates with sample data
13. System renders templates with placeholder data and displays preview
14. Admin clicks "Save Draft" to save configuration without activating (if Draft supported for this event)
15. System validates rule configuration and saves as draft
16. Admin clicks "Test Rule" to send test notification to themselves
17. System generates test notification and delivers to admin's email/phone
18. Admin receives test notification and verifies content, formatting, and delivery
19. Admin clicks "Activate Rule" (or toggles status to Active)
20. System prompts: "This rule will activate immediately and apply to all matching events. Continue?"
21. Admin confirms activation
22. System activates rule and notifies S-03 Notification Service of new rule
23. System displays confirmation: "Notification rule activated successfully"
24. S-03 Notification Service begins monitoring for event triggers matching this rule

### Alternative Flows

**A1: Admin Edits Existing Notification Rule**:

- **Trigger**: Admin needs to modify delivery timing or add SMS channel to existing rule
- **Steps**:
  1. Admin navigates to Settings → Alerts & Notifications and filters by event type
  2. Admin clicks "Edit" on existing rule
  3. Admin modifies delivery timing from 3 days to 5 days before due date
  4. Admin enables SMS channel and selects SMS template
  5. Admin previews changes
  6. Admin saves changes (applies immediately to future events)
  7. System logs change with timestamp and admin user ID
- **Outcome**: Rule updated; future notifications use new configuration; in-flight notifications use old configuration

**A2: Admin Deactivates Notification Rule Temporarily**:

- **Trigger**: Admin wants to pause notifications during system maintenance or holiday period
- **Steps**:
  1. Admin navigates to Settings → Alerts & Notifications
  2. Admin toggles rule status from "Active" to "Paused"
  3. System prompts: "Paused rules will not trigger notifications. Reactivate when ready."
  4. Admin confirms pause
  5. System pauses rule and stops triggering notifications for this event
  6. Admin reactivates rule when ready by toggling status back to "Active"
- **Outcome**: Notifications paused temporarily; no notifications lost (system queues events and evaluates when rule reactivated if within retry window)
- **Note**: A rule for an event on the Non-Disableable list cannot be paused; its toggle is locked. Rules are never deleted, only switched off

**A3: Admin Creates Multi-Language Notification Template**:

- **Trigger**: Admin needs to support multiple locales for the same event (initially English and Turkish per FR-021)
- **Steps**:
  1. Admin navigates to Settings → Alerts & Notifications and opens the Templates section
  2. Admin selects event type: "Quote Submitted / Ready"
  3. Admin selects language: English (default) from the **supported locales list** (managed in FR-021)
  4. Admin edits email template with subject, body, variables
  5. Admin clicks "Add Translation"
  6. System displays language dropdown populated from **FR-021 supported locales**
  7. Admin selects Turkish
  8. Admin edits Turkish version of template (subject, body, same variables)
  9. Admin saves template with both languages
  10. System validates both templates have matching variables
  11. S-03 Notification Service selects template language based on recipient's language preference and fallback rules (FR-021)
- **Outcome**: Template supports multiple languages; recipients receive notification in their preferred language

**B1: Notification Delivery Fails (Email Bounce)**:

- **Trigger**: Email delivery fails due to invalid email address or mailbox full
- **Steps**:
  1. S-03 Notification Service attempts email delivery via SMTP
  2. Email server returns bounce error (invalid address or mailbox full)
  3. System logs failed delivery with error code and timestamp
  4. System evaluates retry configuration for this notification type
  5. If retry enabled, system queues a retry after the retry interval (platform default 1 hour; see General Module Rule 7)
  6. After retries are exhausted (platform default 3; an admin may set 1 to 5), system marks notification as "Failed - Permanent"
  7. System flags patient account with "Email delivery issue" indicator
  8. Admin receives alert if event is critical (e.g., payment confirmation)
  9. Admin contacts patient via alternative channel (phone, in-app message) to update email address
- **Outcome**: Failed delivery logged; admin alerted for critical notifications; patient account flagged for follow-up

**B2: Template Variable Missing or Invalid**:

- **Trigger**: Admin creates template with variable that doesn't exist in event payload
- **Steps**:
  1. Admin creates notification template with variable `{{patient.procedure_date}}`
  2. Admin saves template
  3. System validates template against event payload schema
  4. System detects `patient.procedure_date` not available in event payload (should be `booking.procedure_date`)
  5. System displays error: "Variable `patient.procedure_date` not available for this event. Available variables: [list]"
  6. Admin corrects variable to `{{booking.procedure_date}}`
  7. System validates successfully and saves template
- **Outcome**: Template validation prevents runtime errors; admin corrects variable before activation

**B3: Admin Adds Another Rule for the Same Event**:

- **Trigger**: Admin wants a second rule for an event that already has one (e.g., different recipients, channels or timing)
- **Steps**:
  1. Admin navigates to `Settings → Alerts & Notifications`
  2. Admin clicks "Add Rule" and selects the event from the event catalog (e.g., "Quote Submitted")
  3. System opens the Rule Editor with a new rule in Draft status for that event
  4. Admin enters a Rule Name; if another rule for the same event already uses that name, system shows an error and does not save
  5. Admin saves the rule and, when ready, activates it
- **Outcome**: An event can have several rules, each switched on and off separately. Rule Name is unique per event. Rules are never deleted, only switched off

---

## Screen Specifications

### Screen 1: Alerts & Notifications (Rules Dashboard)

**Purpose**: Provides admin with overview of all configurable notification events (from the backend event catalog) and their configured rules, grouped by category, with quick access to edit, test, and pause/activate rules. (REQ-030-140)

**Data Fields**: (REQ-030-167)

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Event Category | select (dropdown) | No | Filter rules by category (All, Account/Auth, Inquiry, Quote, Booking/Schedule, Treatment, Payment, Billing/Payouts, Messaging/Support, Aftercare, Reviews, Promotions/Discounts, Provider/Compliance, System/Operations) | Predefined categories matching event catalog | ENT-notification-rule.event_category |
| Rule Status | select (dropdown) | No | Filter by status (All, Active, Paused, Draft) | Predefined statuses only | ENT-notification-rule.rule_status |
| Search Rules | text | No | Search by event name, template name, or recipient type | Max 100 characters | no graph field (control) |
| Rules List | table | Yes | Displays all rules matching filters | Sortable by event name, status, last modified; **each row is a “Rule Row” described by the fields below** | no graph field (list of the rows below) |
| Rules List – Rule Row: Event Name | link | Yes | Event that triggers notification (e.g., "Quote Submitted", "Payment Received") | Sourced from backend event catalog; click opens this event’s Rule Editor | ENT-notification-rule.event_type |
| Rules List – Rule Row: Recipient Type | badge | Yes | Who receives notification (Patient, Provider, Admin, Multiple) | Display only | ENT-notification-rule.recipient_types |
| Rules List – Rule Row: Channels | icon set | Yes | Enabled channels (email icon, push icon; SMS icon shown only post‑MVP when SMS is enabled) | Display only | ENT-notification-rule.channel_preferences |
| Rules List – Rule Row: Status | badge | Yes | Active (green), Paused (yellow), Draft (gray) | Display only | ENT-notification-rule.rule_status |
| Rules List – Rule Row: Last Modified | datetime | Yes | Timestamp of last modification | Display in admin's local timezone | ENT-notification-rule.updated_at |
| Rules List – Rule Row: Actions | button group | Yes | Configure, Test, Pause/Activate. There is no Delete action; a rule is only switched off | Permission-based visibility; Pause is not offered for events on the Non-Disableable list | no graph field (control) |
| Add Rule | button | Yes | Starts a new rule in Draft status for a chosen event from the event catalog, including an event that already has a rule (see Workflow B3) | Permission-based visibility; Rule Name must be unique for that event | no graph field (control) |
| Notification Analytics | dashboard panel | Yes | Delivery metrics for the selected period: total sent, delivered, failed, opened (email) and clicked (email), grouped by event type, channel and recipient type (REQ-030-010) | Display only; date range filter; read from the delivery logs | no graph field (dashboard panel) |
| Failed Deliveries | drill-down list | No | Opens from the failed count in Notification Analytics and lists each failed delivery with masked recipient, event type, channel, failure reason, status (Failed - Permanent or Failed - Service Outage) and timestamp; admin can filter by failure reason and export to CSV (REQ-030-226) | Recipient contact masked per Privacy Rule 1 | no graph field (drill-down list) |
| Quiet Hours | time range | Yes | The one platform-wide period during which non-urgent notifications are held and sent after it ends. Set only here by an admin; recipients and providers cannot set their own (REQ-030-224) | Default: 10 PM to 7 AM in the recipient's local time; start and end must differ; critical notifications are not held | no graph field (setting SET-messaging-notification-preferences) |
| Notification Rate Limit | number | Yes | Maximum number of notifications one recipient receives per hour (critical notifications exempt) (REQ-030-017) | Whole number, min 1; default 10 | no graph field (setting) |
| Transplant Progress Reminder Schedule | number + unit | Yes | How often the default patient progress reminder is sent after treatment, and for how long. The patient may change or switch off their own reminders; FR-038 refers to this schedule (REQ-030-225) | Default: once a month for 12 months after treatment | no graph field (setting SET-transplant-progress-reminder-defaults) |

**Business Rules**:

- Rules grouped by event category (Booking, Payment, Aftercare, etc.) for easier navigation
- Active rules displayed with green status badge; paused rules with yellow badge (REQ-030-160)
- Rules are never deleted; an admin switches a rule off (Pause) and on again (Activate). A rule for an event on the Non-Disableable list (Business Rules, Admin Editability Rules) cannot be paused and its toggle is locked (REQ-030-141)
- Pausing a rule requires confirmation prompt: "This will stop notifications for this event. Continue?" (REQ-030-232)
- See REQ-030-159 and REQ-030-228.
- Testing a rule sends sample notification to admin's registered email/phone immediately
- Clicking a rule row (or the Event Name link / "Configure" action) opens **Screen 2: Alerts & Notifications (Rule Editor)** for that event (REQ-030-164)
- Rule Editor MUST include a clear "Back to list" / breadcrumb link returning to the Rules Dashboard with the previous filters preserved

**Notes**:

- Table should support column sorting and filtering (REQ-030-165)
- Pagination if more than 50 rules configured
- Export rules to CSV for audit/backup purposes (REQ-030-166)

---

### Screen 2: Alerts & Notifications (Rule Editor)

**Purpose**: Allows admin to create or edit notification rules, configure recipient targeting, channel preferences, delivery timing, and template selection. (REQ-030-142, REQ-030-143, REQ-030-144, REQ-030-145)

**Data Fields**: (REQ-030-177)

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Rule Name | text | Yes | Internal name for rule (not shown to recipients) | Max 100 chars, unique per event | ENT-notification-rule.rule_name |
| Event Type | select (dropdown) | Yes | System event that triggers notification | Predefined event list from backend; admin cannot create or rename event types here | ENT-notification-rule.event_type |
| Event Category | text (read-only) | Yes | Auto-populated based on event type | Display only | ENT-notification-rule.event_category |
| Recipient Type | multi-select | Yes | Who receives notification (Patient, Provider, Admin, Affiliate) | At least one recipient type required | ENT-notification-rule.recipient_types |
| Recipient Filter Rules | JSON editor | No | Advanced filtering (e.g., only patients in specific regions) | Valid JSON schema | ENT-notification-rule.recipient_targeting_rules |
| Email Channel | toggle (on/off) | No | Enable email delivery | Default: on | ENT-notification-rule.email_channel_enabled |
| Email Template | select (dropdown) | Conditional | Template to use for email (required if email enabled) | Must select template if channel enabled | ENT-notification-rule.email_template_id |
| Push Notification Channel | toggle (on/off) | No | Enable push notification delivery | Default: on for patients/providers | ENT-notification-rule.push_channel_enabled |
| Push Template | select (dropdown) | Conditional | Template for push notification (required if push enabled) | Must select template if channel enabled | ENT-notification-rule.push_template_id |
| SMS Channel | toggle (on/off) | No | Enable SMS delivery (premium feature). **Hidden/disabled in MVP**; only shown when SMS delivery is enabled in S-03 in a post‑MVP phase. **Future phase:** this channel is kept in the rule design but is not offered until that phase | Default: off; admin approval required | ENT-notification-rule.sms_channel_enabled |
| SMS Template | select (dropdown) | Conditional | Template for SMS (required if SMS enabled in a future phase) | Must select template if channel enabled | ENT-notification-rule.sms_template_id |
| Delivery Timing | select (dropdown) | Yes | When to send notification (Immediate, Scheduled, Delayed) | Predefined options | ENT-notification-rule.delivery_timing |
| Schedule Time | datetime picker | Conditional | Specific time to send (required if Scheduled selected) | Future datetime only | ENT-notification-rule.schedule_time |
| Delay Duration | number + unit | Conditional | Delay before sending (required if Delayed selected; e.g., "3 days before event", "1 hour after event") | Min 1 hour, max 90 days | ENT-notification-rule.delay_duration |
| Delivery Timezone | select (dropdown) | Yes | Timezone for delivery (Recipient Local Time, UTC, Specific Timezone) | Default: Recipient Local Time | ENT-notification-rule.delivery_timezone |
| Retry Configuration | toggle (on/off) | No | Enable automatic retry for failed deliveries | Default: on | ENT-notification-rule.retry_enabled |
| Max Retry Attempts | number | Conditional | Maximum retry attempts (required if retry enabled) | Min 1, max 5, default 3 | ENT-notification-rule.max_retry_attempts |
| Retry Interval | number + unit | Conditional | One fixed time between retries (e.g., "1 hour", "6 hours") | Min 1 hour, max 24 hours, default 1 hour | ENT-notification-rule.retry_interval |
| Escalation Rules | toggle (on/off) | No | Enable escalation if condition not met | Default: off for non-critical events | ENT-notification-rule.escalation_enabled |
| Escalation Condition | textarea | Conditional | Condition for escalation (e.g., "Payment not received within 24 hours") | Max 500 chars | ENT-notification-rule.escalation_conditions |
| Escalation Recipients | multi-select | Conditional | Admin roles to notify on escalation | Required if escalation enabled | ENT-notification-rule.escalation_recipients |
| Critical - Cannot Opt Out | toggle (on/off) | No | Marks this notification type as critical: it is delivered through at least one channel even when the recipient has opted out (REQ-030-227) | Default: off; admin only | no graph field (control) |
| Rule Status | select (dropdown) | Yes | Active, Paused, Draft | Default: Draft for new rules; Paused is not allowed for events on the Non-Disableable list | ENT-notification-rule.rule_status |

**Business Rules**:

- **MVP**: At least one delivery channel (email or push) must be enabled (SMS is hidden/disabled) (REQ-030-168)
- **Post‑MVP**: SMS may be enabled where available, but at least one channel must be enabled overall
- Retry follows the platform default (General Module Rule 7) unless the admin sets different values for this notification (REQ-030-169)
- See REQ-030-230.
- SMS channel requires admin approval and incurs additional cost per message (REQ-030-170)
- Template selection filtered by channel type (only email templates shown for email channel) (REQ-030-171)
- Delivery timezone "Recipient Local Time" automatically adjusts delivery time based on recipient's profile timezone (REQ-030-172)
- Escalation rules only available for critical event types (payment, booking, medical concerns) (REQ-030-173, REQ-030-146)
- See REQ-030-174.
- Paused rules can be reactivated without losing configuration (REQ-030-175, REQ-030-151)

**Notes**:

- Preview pane on right side shows live template preview with sample data (REQ-030-147)
- "Test Rule" button sends test notification to admin's contact info
- "Save Draft" allows saving without activating; "Save & Activate" activates immediately (REQ-030-231, REQ-030-148)
- Change log displayed at bottom showing rule modification history (REQ-030-176)
- See REQ-030-164.

---

### Screen 3: Alerts & Notifications (Template Editor)

**Purpose**: Allows admin to create and edit notification templates for email and push (and SMS post‑MVP) with support for dynamic variables, multi-language content, and rich formatting.

**Data Fields**: (REQ-030-186)

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Template Name | text | Yes | Internal name for template | Max 100 chars, unique per event, channel and language | ENT-notification-template.template_name |
| Event Type | select (dropdown) | Yes | Event this template applies to | Predefined event list | ENT-notification-template.event_type |
| Channel Type | select (dropdown) | Yes | Delivery channel (Email, Push Notification; SMS post‑MVP only) | Fixed at creation (cannot change) | ENT-notification-template.channel_type |
| Language | select (dropdown) | Yes | Template language (locale) | Must be in supported locales list (FR-021); can create multiple language versions | ENT-notification-template.language |
| Email Subject | text | Conditional | Email subject line (required for email channel) | Max 200 chars, supports variables | ENT-notification-template.content |
| Email Body | rich text editor | Conditional | Email body content (required for email channel) | Max 10,000 chars, supports HTML/variables | ENT-notification-template.content |
| Push Title | text | Conditional | Push notification title (required for push channel) | Max 100 chars, supports variables | ENT-notification-template.content |
| Push Body | textarea | Conditional | Push notification body (required for push channel) | Max 500 chars, supports variables | ENT-notification-template.content |
| SMS Body | textarea | Conditional | SMS message body (required for SMS channel) | Max 160 chars (1 SMS segment), supports variables | ENT-notification-template.content |
| Available Variables | list (read-only) | Yes | Variables available for this event type (e.g., `{{patient.display_name}}`, `{{booking.date}}`) | Display only; click to insert | ENT-notification-template.available_variables |
| Variable Preview Values | JSON editor | No | Sample values for template preview | Valid JSON; used only for preview | no graph field (preview only) |
| Template Status | select (dropdown) | Yes | Active, Draft, Archived | Default: Draft | ENT-notification-template.status |

**Business Rules**:

- Email templates support rich text formatting (bold, italic, links, images, buttons) (REQ-030-178)
- Push notification templates support plain text only with limited formatting (bold, italic via markdown) (REQ-030-179)
- SMS templates support plain text only; no formatting; 160 characters per SMS segment (platform warns if exceeds 1 segment) (REQ-030-180)
- Variables must be enclosed in double curly braces: `{{variable.name}}` (REQ-030-181)
- System validates all variables exist in event payload before allowing template activation (recipient-specific payload schemas apply; provider recipients pre-confirmation MUST NOT have access to unmasked patient PII fields per the platform masking rules) (REQ-030-182)
- Templates can be versioned; changes create new version while preserving previous versions for audit (REQ-030-183)
- Archived templates cannot be selected in notification rules but remain for historical records (REQ-030-184)
- Multi-language templates must have matching variable usage across all language versions (REQ-030-153)

**Notes**:

- Split-screen layout: editor on left, live preview on right
- Preview automatically updates as admin types
- "Insert Variable" dropdown inserts variable at cursor position
- "Send Test" button sends test notification to admin with preview values
- Template version history displayed at bottom with **“Revert by Creating New Version”** capability (no in-place rollback; reverting creates a new version from a selected prior version)

---

## Business Rules

### General Module Rules

- **Rule 1**: Every change to a notification rule is recorded in the audit trail as set out in REQ-030-020
- **Rule 2**: Notification rules are never deleted, only switched off (paused). A rule for an event on the Non-Disableable list (see Admin Editability Rules) cannot be paused (REQ-030-230)
- **Rule 3**: An event type can have **several** notification rules. Rule Name must be unique among the rules of one event; an admin adds another rule for an event with "Add Rule" (REQ-030-159)
- **Rule 4**: Notification templates must be activated before they can be selected in notification rules (REQ-030-185)
- **Rule 5**: All timestamps in notifications displayed in recipient's local timezone (derived from profile settings) (REQ-030-187)
- **Rule 6**: See REQ-030-017.
- **Rule 7**: **General retry rule for every notification.** An email, push or in-app notification that fails to deliver is retried using the platform default: retry on, up to 3 retries, one fixed interval of 1 hour between attempts. An admin may set different values for an individual notification (1 to 5 retries, interval 1 to 24 hours). This rule is written once, here; every other feature states only that its notification retries follow it. Retries of work that is not a notification (for example failed payments, report generation or saving settings) are not covered (REQ-030-155)
- If SMTP service unavailable, queue emails for retry; alert admin if outage exceeds 15 minutes; fallback to secondary SMTP provider if configured (REQ-030-201)
- If push service unavailable, queue notifications for retry; alert admin if outage exceeds 15 minutes; notifications expire after 24 hours (recipient sees notification history in-app instead) (REQ-030-201)
- If SMS gateway unavailable, queue SMS for retry (max 3 attempts); fallback to email/push notification if SMS fails; alert admin of SMS delivery issues. **This behaviour is future-facing; no SMS is sent in MVP.**
- If template rendering fails due to invalid template syntax, log error, alert admin, fallback to plain text notification template (REQ-030-202)
- If profile API unavailable, fallback to basic notification template without personalization; retry profile fetch before next notification delivery attempt (REQ-030-202)
- If message queue unavailable, retry publishing event with exponential backoff; alert admin if queue outage exceeds 5 minutes
- If external service returns 5xx error, retry following the general retry rule (General Module Rule 7); if all retries fail, mark notification as failed and alert admin
- Critical notifications (payment confirmations, appointment reminders, medical escalations) must be delivered with higher priority and stricter SLAs than non-critical notifications (marketing, general updates) (REQ-030-200)

### Data & Privacy Rules

- **Privacy Rule 1**: See REQ-030-016 and REQ-030-009.
- **Privacy Rule 2**: Notification content must not include sensitive medical information unless encrypted (email encryption via TLS, SMS not used for sensitive data) (REQ-030-189)
- **Privacy Rule 3**: See REQ-030-015.
- **Privacy Rule 4**: Recipients can opt out of non-critical notifications via profile preferences; system must respect opt-out for all non-critical notification types (REQ-030-019)
- **Privacy Rule 5**: **Provider-facing notifications MUST follow the existing patient-identity masking rules used across the platform**: until treatment is confirmed via completed payment, patient identifiers remain masked/hidden (examples in FR-003 and FR-006). Provider templates MUST NOT be able to reference unmasked patient name/email/phone pre-confirmation; they may only use the same masked display fields used elsewhere (e.g., `patient.display_name` which renders masked pre-confirmation and unmasked post-confirmation). (REQ-030-190)
- **Privacy Rule 6**: Notification logs retained for 90 days for operational purposes; then archived (immutable) for audit/compliance retention. **No hard deletes** of notification logs; when a user requests deletion, the system must **anonymize/redact personal identifiers** in archived logs per platform retention/compliance policy (see FR-023). (REQ-030-013)
- **GDPR**: Recipients can request export of all notifications sent to them; system provides notification history in machine-readable format (JSON/CSV) (REQ-030-191)
- **Authentication**: Admin access to notification configuration requires authentication via FR-031 admin authentication system; admins cannot impersonate recipients for notification testing (REQ-030-196)
- **Authorization**: Granular permission checks enforced via FR-031 permission matrix; some admins can configure rules, others only view analytics (REQ-030-197)
- **PII Redaction (Provider Pre-Confirmation)**: When the recipient is a provider and treatment is not yet confirmed via completed payment, S-03 MUST apply the same patient-identity masking rules used elsewhere in the platform (e.g., FR-003/FR-006) and MUST NOT include unmasked patient identifiers (full name, email, phone) in the provider recipient payload.
- **CAN-SPAM**: Email notifications include unsubscribe link for marketing emails (transactional emails exempt) (REQ-030-198)
- **TCPA (US)**: SMS notifications only sent with explicit recipient consent; opt-out via "STOP" keyword supported (REQ-030-199)
- Patients can view notification history in-app and access past notifications for 90 days (REQ-030-107)
- SMTP authentication and SPF/DKIM/DMARC configured to prevent email spoofing
- **Authentication**: API keys stored in secure vault (AWS Secrets Manager, HashiCorp Vault)
- **Authentication**: Internal service-to-service authentication via JWT or API key

### Admin Editability Rules

**Editable by Admin**: (REQ-030-192)

- Event-to-notification mappings (which events trigger which notifications)
- Notification templates (subject, body, formatting, variables) for all channels
- Recipient targeting rules (who receives notifications based on role, relationship, event context)
- Channel preferences per event type (enable/disable email, push, SMS)
- Delivery timing configuration (immediate, scheduled, delayed)
- Retry logic parameters (max attempts, interval between retries). See REQ-030-008.
- Notification rate limit per recipient. See REQ-030-017.
- Transplant progress reminder schedule. See REQ-030-225.
- Escalation rules for time-sensitive notifications
- Quiet hours. See REQ-030-224.

**Fixed in Codebase (Not Editable)**: (REQ-030-193)

- Core event definitions (system events that can trigger notifications - e.g., "Quote Submitted / Ready", "Payment Received / Receipt")
- Variable schema per event type (which variables available in notification templates per event)
- Maximum retry attempts (hard limit: 5 retries to prevent infinite loops)
- Encryption algorithms for notification content (AES-256 at rest, TLS 1.3 in transit)
- Delivery channel integrations (SMTP provider, push notification service, SMS gateway API)

**Non-Disableable by Default (Security-Critical and Mandatory)**:

- **Account/Auth notifications (OTP verification, password reset)** are security-critical and MUST be **non-disableable by default** in the admin UI (toggle locked; no pause). (REQ-030-137)
- **Quote Cancelled — Inquiry Cancelled (`quote.cancelled_inquiry`)** is a mandatory provider notification. Provider MUST be notified when their quote is auto-cancelled due to inquiry cancellation. Admin cannot disable this event because the provider needs to know the slot is released and the quote is no longer active. Toggle is locked for this event, and FR-032 provider notification preferences cannot suppress it.
- **Preference exemption for mandatory provider events**: every event that is mandatory for providers (`quote.cancelled_inquiry`, the selected-provider and not-selected-provider outcomes of `quote.accepted`, `booking.payment_window_expired`, `booking.revived` and `booking.rescheduled`) is delivered regardless of FR-032 provider notification preferences. A provider's category toggles in FR-032 never suppress these events. (REQ-030-138)
- **Booking Accepted — Slot Held (`booking.scheduled`)** is mandatory for the patient, because it is the patient's only acceptance notice and states the payment deadline. It also fires for an admin-authored replacement acceptance. Toggle is locked.
- **Booking Rescheduled (`booking.rescheduled`)** is mandatory for patient and provider: both must learn the new appointment after an admin changes it. Toggle is locked.
- **Quote Withdrawn (`quote.withdrawn`)** is mandatory before and after acceptance: the patient MUST always learn that the provider has withdrawn the quote, and the admin MUST be alerted only when the withdrawn quote was already accepted. Toggle is locked.
- **Quote Accepted (`quote.accepted`)**: the selected-provider outcome and the not-selected-provider outcome are mandatory, because the selected provider must learn that its slot is held and every other provider with a sent parent quote must learn that the quote is no longer active. These outcome toggles are locked. `quote.accepted` has no patient or admin recipient.
- **Payment Window Expired (`booking.payment_window_expired`)** and **Booking Revived (`booking.revived`)** are mandatory for patient and provider: both must know whether the slot is released or held again and what the payment deadline is. Toggles are locked.
- **Provider Unable to Proceed — Replacement Being Arranged (`booking.provider_fault_replacement`)** is mandatory: the patient MUST learn that an admin will arrange a replacement provider. Toggle is locked.
- **Treatment Details Changed After Acceptance (`treatment.plan_changed`)** is mandatory: every audited change to plan, clinicians or grafts from booking confirmation (`Confirmed`) onward MUST be notified to the patient. Toggle is locked.
- **Provider-Caused Cancellation (`provider.status_cancellation_patient`) and Admin Support Required (`provider.status_cancellation_admin_support`)** are mandatory notifications for each inquiry/case affected by an FR-015 provider suspension or deactivation. Affected patients and admins MUST be informed regardless of FR-015's "Notify Provider" checkbox; toggles are locked for both events. Failed deliveries retry per FR-020 without duplicates (de-duplicated per provider-status event + affected record + recipient) and never restore cancelled records. See REQ-030-094 and REQ-030-095.
- **Aftercare Provider Reassigned (`aftercare.provider_reassigned`)** is mandatory: when an admin reassigns an aftercare case through FR-011, the patient and the new aftercare provider MUST learn who now provides aftercare. Toggle is locked, FR-032 provider preferences cannot suppress it, and no admin alert is sent because the admin is the actor.
- **Provider Account Activation (`provider.activation`)** is mandatory and non-disableable: without it a new provider cannot set a password and log in. **Provider Reactivated (`provider.reactivated`)** and **Scheduled Status Change Cancelled (`provider.scheduled_change_cancelled`)** follow FR-015's "Notify Provider" choice; when triggered they cannot be disabled here. Toggles are locked for all three events. `provider.suspended`, `provider.deactivated`, `provider.reactivated`, and `provider.scheduled_change_cancelled` go to the provider Owner only. See REQ-030-096. **Owner Login Email Changed (`provider.login_email_changed`)** is a mandatory security notice to the old and the new login address; its toggle is locked.
- **Provider Account-Closure Requested (`provider.closure_requested`)** and **Provider Account-Closure Request Rejected (`provider.closure_rejected`)** are mandatory: admins must learn of every closure request, and a provider whose request is rejected must be told the account stays Active. Toggles are locked for both. See [CR-FR030-20261015-02](./change-request-2026-10-15-provider-closure-request-events.md).
- If the product explicitly allows a break-glass disable path for any non-disableable event, it MUST: (REQ-030-139)
  - Require Super Admin permission (FR-031) + re-authentication
  - Show an imminent critical warning explaining impact (users cannot sign up/reset passwords; providers not informed of cancellation)
  - Require multiple confirmation steps (e.g., typed event name + final confirm)
  - Require an audit reason and log it as a security event

**Event Catalog Source**:

- The list of available notification events is maintained by backend services (S-03 + core modules) as a central "event catalog".
- Admin UIs (e.g., `Settings → Alerts & Notifications`) can only **select from this catalog**; they cannot create arbitrary new event types. (REQ-030-125)
- New event types are introduced via backend/product releases and then exposed to the admin as selectable items for configuration (rule on/off, channels, timing, templates).

**Configurable with Restrictions**:

- **Future phase:** SMS channel availability: Admin can enable SMS for specific event types, but each SMS incurs cost; requires budget approval for high-volume events (REQ-030-194)
- Notification testing: Admins can send test notifications to themselves or designated test accounts; cannot send to production recipients without rule activation (REQ-030-195)
- Template versioning: Admins can create new template versions; system retains previous versions for audit; “revert” creates a **new** version copied from a selected prior version and requires admin confirmation (REQ-030-212)

---

## Dependencies

- **FR-026**: App Settings & Security Policies; OTP template management extended to all notification types.
- **FR-021**: Multi-Language & Localization; supported locales, user language preference and fallback rules.
- **FR-001**: Auth & Profile Management (Patient); recipient profile data and patient notification preferences.
- **FR-009**: Auth & Team Management (Provider); provider profile and team roles for notification routing.
- **FR-020**: Notification Service; delivers and lists the notifications these rules and templates produce, and follows the general retry rule.
- **FR-032**: Profile & Settings Management (Provider); shows and edits provider notification preferences.
- **FR-031**: Admin Access Control & Permissions; permission matrix for notification configuration.
- **FR-003**: Inquiry Submission & Distribution; inquiry events.
- **FR-004 / FR-005**: Quote Submission; Quote Comparison & Acceptance; quote lifecycle events, `quote.accepted` with its outcomes, and the accepted snapshot.
- **FR-006**: Booking & Scheduling; booking events.
- **FR-010**: Treatment Execution; `treatment.plan_changed`.
- **FR-007 / FR-007B**: Payment Processing; Split Payment / Installment Plans; payment events and payment transaction data.
- **FR-011**: Aftercare & Recovery Management; aftercare events.
- **FR-037 / FR-038**: Monitor Your Hair Loss; Monitor Your Transplant Progress; monitoring events and the transplant progress reminder schedule.
- **FR-015 / FR-016**: Provider Management & Onboarding; Patient Management & Oversight; provider status and lifecycle events, Admin Support Required filter.



---

## User Scenarios & Testing

### User Story 1 - Admin Configures Payment Reminder Notifications (Priority: P1)

Admin needs to configure automated payment reminder notifications to reduce overdue installments. Patient should receive email and push notifications 3 days before installment due date. (SMS is post‑MVP only.)

**Why this priority**: Payment reminders are critical for cash flow and reducing payment defaults. This is the highest-value notification type for the business.

**Independent Test**: Can be fully tested by creating notification rule, triggering test payment due event, verifying admin receives test notification with correct timing, content, and delivery channels.

**Acceptance Scenarios**:

1. **Given** admin is logged into Admin Platform → Settings → Alerts & Notifications, **When** admin selects the "Payment Due Reminder" event from the event catalog and clicks "Configure", **Then** system displays the event configuration form with event-specific configuration options
2. **Given** admin configures rule with email and push channels enabled, delivery timing "3 days before due date at 9:00 AM recipient local time", retry enabled (platform default of 3 retries, or different values the admin sets), **When** admin clicks "Save Draft", **Then** system validates rule configuration and saves as draft status
3. **Given** admin clicks "Test Rule", **When** system generates test notification with sample payment data (patient name "Test Patient", amount due "$200", due date "2025-11-16"), **Then** admin receives test email and push notification within 2 minutes with correct personalized content
4. **Given** admin reviews test notification and verifies content correct, **When** admin clicks "Activate Rule", **Then** system prompts for confirmation, activates rule upon confirmation, and displays success message "Notification rule activated successfully"
5. **Given** notification rule active, **When** patient has installment payment due in 3 days (due date 2025-11-16, current date 2025-11-13), **Then** system triggers notification at 9:00 AM patient local time on 2025-11-13 and delivers email and push notification to patient
6. **Given** email delivery fails due to invalid email address, **When** system detects bounce error, **Then** system logs failed delivery, queues a retry after the retry interval (platform default 1 hour), and alerts admin if the retries also fail

---

### User Story 2 - Admin Creates Multi-Language Notification Template (Priority: P1)

Admin needs to create email notification template for the "Quote Submitted / Ready" event in both English and Turkish to support patients in UK and Turkey. Template must include patient name, the "From" price, option count, treatment, provider name, and expiry date with consistent formatting across languages.

**Why this priority**: Multi-language support is critical for international patient base. Quote submitted notification is high-volume and directly impacts conversion rates.

**Independent Test**: Can be fully tested by creating template in both languages, sending test notifications in each language, verifying correct language selection based on recipient language preference.

**Acceptance Scenarios**:

1. **Given** admin navigates to Admin Platform → Settings → Alerts & Notifications, **When** admin clicks "Create New Template" and selects event type "Quote Submitted / Ready", channel "Email", language "English", **Then** system displays email template editor with available variables for the Quote Submitted / Ready event
2. **Given** admin edits template with subject "Your Hair Transplant Quote from {{provider.name}}", body "Hello {{patient.first_name}}, You've received a quote for {{quote.treatment_type}} from {{provider.name}} with {{quote.option_count}} options from {{quote.from_price}} {{quote.currency}}. Quote expires on {{quote.expiry_date}}. View your quote in the app.", **When** admin clicks "Save Draft", **Then** system validates template variables against event payload schema and saves template as draft
3. **Given** admin clicks "Add Translation", **When** admin selects language "Turkish" and edits Turkish template with translated subject and body (same variables), **Then** system validates both templates have matching variables and saves Turkish version
4. **Given** admin clicks "Activate Template", **When** system validates both language versions active, **Then** system activates template and displays success message
5. **Given** notification rule configured with "Quote Submitted / Ready" event and template activated, **When** patient with language preference "Turkish" receives quote from provider, **Then** S-03 Notification Service renders Turkish template and sends Turkish-language email to patient
6. **Given** patient with language preference "English" receives quote, **When** S-03 evaluates notification rule, **Then** system renders English template and sends English-language email

---

### User Story 3 - Admin Monitors Notification Delivery and Troubleshoots Failures (Priority: P2)

Admin needs to monitor notification delivery performance to identify and resolve delivery issues. Admin should see real-time delivery rates, failure reasons, and drill down into specific failed notifications for troubleshooting.

**Why this priority**: Monitoring and troubleshooting capabilities are essential for maintaining high delivery rates and quickly resolving issues before they impact large numbers of users.

**Independent Test**: Can be fully tested by triggering mix of successful and failed notification deliveries (via test rules), verifying admin can view metrics in dashboard, filter by failure reason, and retry failed deliveries.

**Acceptance Scenarios**:

1. **Given** admin navigates to Admin Platform → Settings → Alerts & Notifications, **When** admin views delivery/log information for an event or runs a test notification, **Then** system displays delivery status and failure reasons (where applicable) and allows export to CSV for troubleshooting
2. **Given** dashboard shows 950 emails sent, 900 delivered (94.7%), 50 failed (5.3%), **When** admin clicks on "Failed Deliveries" metric, **Then** system displays detailed list of 50 failed notifications with recipient (masked), event type, channel, failure reason, timestamp
3. **Given** failed notifications list shows 30 failures with reason "Invalid email address", 15 with reason "Mailbox full", 5 with reason "SMTP timeout", **When** admin filters by failure reason "Invalid email address", **Then** system displays 30 failed notifications with invalid email addresses
4. **Given** admin identifies pattern (all failures for email domain "@oldprovideremail.com"), **When** admin contacts affected patients to update email addresses, **Then** patients update their profiles with new email addresses
5. **Given** patient updates email address from invalid to valid, **When** admin clicks "Retry" on failed notification in dashboard, **Then** system re-triggers notification delivery to updated email address and marks as successfully delivered if delivery succeeds
6. **Given** admin marks resolved failures as "Resolved", **When** admin refreshes dashboard, **Then** resolved failures removed from active failures list but retained in notification logs for audit trail

---

### Edge Cases

- What happens when **admin creates notification rule with delivery timing "3 days before event" but event occurs in less than 3 days**?
  - System evaluates notification rule when event created; if delivery timing already passed, system triggers notification immediately with note "Delivery timing adjusted due to short notice" in admin logs
  - Alternatively, admin can configure rule to skip notification if timing not feasible (e.g., don't send "3 days before" reminder if event is tomorrow) (REQ-030-203)

- How does system handle **template variable missing in event payload at runtime** (e.g., template uses `{{patient.phone}}` but phone number not provided in patient profile)?
  - System renders template with placeholder text for missing variable (e.g., "[Phone number not provided]") or omits section containing missing variable if template designed with conditional logic
  - System logs warning in admin notification logs: "Variable `patient.phone` not available for notification [notification_id]; rendered with placeholder"
  - Admin receives alert if missing variable affects critical notification (e.g., appointment reminder missing appointment time) (REQ-030-204)

- What occurs if **recipient has multiple email addresses or phone numbers in profile** (e.g., primary and secondary)?
  - System prioritizes primary contact info (primary email, primary phone); delivers to primary only
  - If delivery to primary fails, system can optionally retry with secondary contact info (configurable per notification rule via "Retry with secondary contact" toggle)
  - Admin can configure notification rule to send to both primary and secondary simultaneously for critical events (e.g., payment confirmation sent to both primary and secondary email) (REQ-030-205)

- How to manage **notification delivery during recipient timezone changes** (e.g., daylight saving time transitions)?
  - System automatically adjusts delivery timing based on recipient's current timezone setting at time of delivery
  - If recipient travels to different timezone and updates profile, future notifications use new timezone
  - Scheduled notifications (e.g., "9:00 AM recipient local time") calculated dynamically at delivery time, not statically when notification scheduled (REQ-030-206)

- What happens when **admin deactivates notification rule while notifications queued for delivery**?
  - System immediately stops adding new notifications to queue for deactivated rule
  - Notifications already queued (not yet delivered) remain in queue and delivered as scheduled
  - If admin wants to cancel queued notifications, admin must explicitly "Purge Queue" (with confirmation prompt: "This will cancel X pending notifications. Continue?") (REQ-030-207)

- How does system handle **conflicting notification preferences** (e.g., admin rule requires email delivery but recipient opted out of emails)?
  - System respects recipient opt-out for non-critical notifications (marketing, general updates) and does not deliver
  - For critical notifications (payment confirmations, appointment reminders), system overrides opt-out and delivers via at least one channel (displays banner in-app explaining why critical notification delivered despite opt-out)
  - Admin can designate notification types as "Critical - Cannot Opt Out" in rule configuration (REQ-030-208)

- What happens when a recipient has **both Email and Push switched off**?
  - Nothing is sent by email or push, and the in-app entry is still always created (REQ-030-234)

- What occurs if **external notification service (SMTP, push, SMS) experiences prolonged outage** (e.g., 24 hours)?
  - System queues notifications for retry at the retry interval (up to 24-hour window)
  - If service restored within 24 hours, queued notifications delivered (may result in burst of deliveries)
  - If outage exceeds 24 hours, system marks notifications as "Failed - Service Outage" and alerts admin
  - Admin can manually re-trigger notifications after service restored or switch to backup notification provider if configured (REQ-030-209)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-030-001**: System MUST allow admins to create notification rules by selecting event type, configuring recipient targeting, enabling delivery channels (email, push, and SMS in future phases), selecting templates per channel, and defining delivery timing. In MVP, only email and push can actually be enabled; SMS is reserved for later phases once S‑03 SMS support is implemented.
- **REQ-030-002**: System MUST evaluate notification rules in real-time (<30 seconds) when system events occur and trigger notifications for all matching rules
- **REQ-030-003**: System MUST deliver email notifications via SMTP service within 2 minutes of trigger for 95% of emails
- **REQ-030-004**: System MUST deliver push notifications via FCM/Web Push within 1 minute of trigger for 95% of push notifications
- **REQ-030-005**: System MUST support optional SMS notifications for critical events (payment reminders, appointment alerts) with admin approval and cost tracking in post‑MVP phases; **MVP does not send SMS**.
- **REQ-030-006**: System MUST provide notification template editor supporting rich text (email), plain text (push, SMS), dynamic variables, and multi-language content. SMS templates, if configured, are only used when SMS delivery is enabled in a later phase.
- **REQ-030-007**: System MUST validate notification templates before activation to ensure all variables exist in event payload and template syntax is valid
- **REQ-030-008**: System MUST automatically retry failed notification deliveries using the general retry rule (General Module Rule 7): by default up to 3 retries at one interval of 1 hour; an admin may set 1 to 5 attempts and a different interval for an individual notification
- **REQ-030-009**: System MUST log all notification deliveries (successful and failed) with recipient (masked), event, channel, timestamp, delivery status, and failure reason (if applicable)
- **REQ-030-010**: System MUST provide real-time notification delivery analytics dashboard with metrics: total sent, delivered, failed, opened (email), clicked (email), grouped by event type, channel, recipient type

### Data Requirements

- **REQ-030-011**: System MUST store notification rules with: event type, recipient targeting rules, channel preferences, template IDs, delivery timing, retry configuration, escalation rules, rule status (active/paused/draft)
- **REQ-030-012**: System MUST store notification templates with: template name, event type, channel type, language, content (subject, body), variables, status (active/draft/archived), version history
- **REQ-030-013**: System MUST maintain notification delivery logs for 90 days in operational database; archive logs for audit/compliance retention (no hard delete). If a user requests deletion, the system MUST anonymize/redact personal identifiers in those logs per platform retention/compliance policy (see FR-023).
- **REQ-030-014**: System MUST track notification engagement metrics (email opens, email clicks) via pixel tracking and link tracking from SMTP service

### Security & Privacy Requirements

- **REQ-030-015**: System MUST encrypt notification templates at rest using AES-256; decrypt only during template rendering in S-03 Notification Service
- **REQ-030-016**: System MUST mask recipient contact information (email, phone) in admin interfaces to protect privacy (e.g., "mar***@example.com", "+44***1234")
- **REQ-030-017**: System MUST enforce rate limiting to prevent notification spam: a maximum number of notifications per hour per recipient, set by admins with a default of 10 (critical notifications exempt from rate limiting)
- **REQ-030-018**: System MUST HTML-escape all template variables during rendering to prevent XSS attacks from user-generated content
- **REQ-030-019**: System MUST respect recipient opt-out preferences for non-critical notifications (marketing, general updates); critical notifications (payment, appointment) override opt-out with in-app explanation
- **REQ-030-020**: System MUST record every notification rule change in the audit trail with admin user ID, timestamp, change summary, old and new configuration, IP address and reason (if provided); audit log retention follows the system PRD, Platform-Wide Rules: One 10-year retention period

### Integration Requirements

- **REQ-030-021**: System MUST integrate with SMTP service (SendGrid, Amazon SES, Mailgun) for email delivery via RESTful API or SMTP protocol
- **REQ-030-022**: System MUST integrate with push notification services (Firebase Cloud Messaging for mobile, Web Push API for web) for push notification delivery
- **REQ-030-023**: System MUST integrate with SMS gateway (Twilio, Vonage) for SMS delivery via RESTful API (optional, admin-enabled)
- **REQ-030-024**: System MUST receive delivery status updates (bounces, opens, clicks) from external services via webhooks; webhook signature verification: See system PRD, Platform-Wide Rules: No card numbers stored
- **REQ-030-025**: System MUST publish notification events to audit log service (Elasticsearch, CloudWatch Logs) for compliance and troubleshooting
- **REQ-030-026**: System MUST list `aftercare.provider_reassigned` (FR-011 producer; Patient and new aftercare provider) as a locked mandatory event that FR-032 preferences cannot suppress, and MUST raise `provider.status_cancellation_admin_support`, never `booking.provider_fault_replacement`, when a provider-status event leaves an `In Progress` booking open with `supportRequired` for an admin decision
- **REQ-030-156**: System flags patient account with "Email delivery issue" indicator
- **REQ-030-157**: Admin receives alert if event is critical (e.g., payment confirmation) Admin contacts patient via alternative channel (phone, in-app message) to update email address
- **REQ-030-158**: System displays error: "Variable `patient.procedure_date` not available for this event. Available variables: [list]"

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 1.21 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (versions 1.0 to 1.20) and the change requests (CR-FR030-20261014-01, CR-FR030-20261015-01, CR-FR030-20261015-02, CR-FR030-20261016-01, change-request-2026-08-20-fr037-monitoring-events.md, CR-FR020-20261027-01, CR-FR003-20261027-02) are in `archived/prd-baseline-2026-11-08/` and in git history. | Claude (AI Assistant) |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | TBD | 2025-12-22 | ✅ Verified & Approved |
| Technical Lead | TBD | 2025-12-22 | ✅ Verified & Approved |
| Stakeholder | TBD | 2025-12-22 | ✅ Verified & Approved |
| Product Owner | Joachim Trung Tuan | 2026-09-16 | Approved FR-005 quote-outcome and recipient-privacy alignment through v1.6 |
| Product Owner | Joachim Trung Tuan | 2026-10-18 | Approved FR-030 v1.12 to v1.15 via MTG-002 decision log (documentation only), including CR-FR030-20261016-01 |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-11-22
