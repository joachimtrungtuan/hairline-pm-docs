# FR-020 - Notifications & Alerts

**Module**: S-03: Notification Service
**Feature Branch**: `fr020-notifications-alerts`
**Created**: 2025-11-11
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-020 from local-docs/project-requirements/system-prd.md; Transcriptions (patient/admin/provider references); FR-015 v1.9 provider-status cancellation cascade

---

## Executive Summary

Provide reliable, configurable notifications (email, push, optional SMS in future phases) for key lifecycle events across patients and providers. Deliver timely alerts, respect user preferences, prevent spam via throttling, and track delivery for operational visibility. MVP supports global Email/Push toggles on the patient app; fine‑grained category preferences follow in V2, and any SMS delivery is explicitly deferred beyond MVP.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (FR-001: Patient Authentication & Profile Management): Receive push/email notifications; manage global Email/Push toggles (MVP) and view notification history (listing specified in FR-020). (REQ-020-024)
- Provider Platform (FR-032: Provider Dashboard Settings & Profile Management / PR-06): Receive notifications for inquiries, quotes, bookings, payments, and messages; manage notification preferences; view notifications via dropdown. (REQ-020-025)
- Admin Platform (FR-030: Notification Rules & Configuration + FR-020 dropdown): Receive notifications for configurable events per FR-030 event catalog; configure default notification policies, SMS enablement, throttling thresholds, and view delivery dashboards; view notifications via dropdown. (REQ-020-026)
- Affiliate Program (if enabled): Receive affiliate payout notifications; configuration is managed via FR-030 event catalog and rules. (REQ-020-027)
- Shared Services (S-03): Unified Notification Service orchestrating channels (email, push, and SMS in future phases) with templates, throttling, and delivery tracking. SMS delivery is not implemented in MVP and is treated as a future enhancement. (REQ-020-028)

### Scope Boundaries

In Scope:

- Notification event types (MVP):
  - **Source of truth**: `FR-030: Notification Rules & Configuration` (Admin-Configurable Notification Event Catalog). (REQ-020-029)
  - The table below mirrors FR-030 for completeness; **if any mismatch exists, FR-030 prevails**. Each row is a pointer to the FR-030 catalogue entry of the same event, and FR-030 owns that row's recipients, channels, content and whether the notice can be switched off. Events that produce a notification are owned by the FR-030 catalogue (see Event Ownership in Business Rules). (REQ-020-156, REQ-020-157)

| Category | Event (Display Name) | Example Backend Event Key | Primary Recipients | Notes | Rule |
|----------|-----------------------|---------------------------|--------------------|-------|------|
| Account/Auth | Email Verification / OTP Code | `account.email_verification_code` | Patient, Provider, Admin | Details in the FR-030 catalogue entry. | REQ-030-027 |
| Account/Auth | Password Reset Code / Link | `account.password_reset` | Patient, Provider, Admin | **Security-critical** and non-disableable by default | REQ-020-073 |
| Account/Auth | New Account Created (Welcome / Onboarding) | `account.created` | Patient | Optional; can be disabled if not needed. Provider onboarding uses `provider.activation` instead | REQ-020-074 |
| Inquiry | Inquiry Submitted (Provider notified) | `inquiry.submitted` | Provider | “New inquiry matching clinic/location” | REQ-020-075 |
| Inquiry | Inquiry Cancelled | `inquiry.cancelled` | Patient, Provider, Admin (optional) | Patient-initiated inquiry cancellation (FR-003 Workflow 5). Fires when patient cancels inquiry in Inquiry, Quoted, or Accepted stages. Patient receives cancellation confirmation (mandatory — aligns with FR-003 Workflow 5 step 4 and Screen 8b). Cancellation reason is patient-private — provider notification says only "Inquiry cancelled by patient". **MVP default channels: Email + Push.** | REQ-020-076 |
| Inquiry | Inquiry Response SLA Breached | `inquiry.ttfq_sla_breached` | Provider | Details in the FR-030 catalogue entry. (FR-014 REQ-014-113) | REQ-030-032 |
| Quote | Quote Submitted / Ready (Patient notified) | `quote.submitted` | Patient | Fired by FR-004 when the provider sends the parent quote; the quote expiry is set and governed by FR-004. The notice shows the "From" price (the lowest subquote price in the parent quote, in the quote currency), the option count, the treatment and the expiry date. Exact subquote prices are not shown before acceptance, and no single quote total exists (see Quote, Booking and Treatment-Change Notifications in Business Rules) | REQ-030-033 |
| Quote | Quote Revised (New Version) | `quote.updated` | Patient, Provider | Details in the FR-030 catalogue entry. | REQ-030-034 |
| Quote | Quote Expiring Soon | `quote.expiring_soon` | Patient, Provider | Details in the FR-030 catalogue entry. | REQ-030-035 |
| Quote | Quote Expired | `quote.expired` | Patient, Provider | Sent on expiry processing completion | REQ-020-081 |
| Quote | Quote Restored (Expired Quote Reopened by Admin) | `quote.restored` | Patient, Provider | Fired by FR-004 when an admin restores an expired quote. The quote returns to sent with a fresh full expiry window (restore time plus the FR-026 window in force). The notice says the quote is open again and shows the new expiry date. Channels follow the FR-030 default channel policy | REQ-020-153 |
| Quote | Quote Withdrawn | `quote.withdrawn` | Patient, Admin (only when the quote was already accepted) | Details in the FR-030 catalogue entry. | REQ-030-037 |
| Quote | Quote Accepted / Subquote Outcomes | `quote.accepted` | Provider | FR-005 uses the existing event with `outcome` = `selected_subquote_accepted`, `sibling_subquote_not_selected`, or `competing_parent_cancelled_other_subquote_accepted`. Selected-provider payloads may include the accepted subquote details, read from the accepted snapshot. A non-selected provider receives only its own parent quote/subquote references, its outcome, and reason; selected provider identity and accepted price are excluded. Each provider receives one notice per sent parent quote: the provider of the accepted parent quote receives `selected_subquote_accepted`, with that parent's sibling subquotes listed in the same notice as `sibling_subquote_not_selected`; each other sent parent quote produces one not-selected notice (`competing_parent_cancelled_other_subquote_accepted`) to its provider, including another parent quote of the selected provider. Unsent drafts cancelled by FR-004 produce no notice. **The selected-provider and not-selected-provider outcomes are mandatory — admin cannot disable them** (see Quote, Booking and Treatment-Change Notifications in Business Rules). The patient is not a recipient: at acceptance the patient receives only `booking.scheduled`. No admin notification is sent for an acceptance | REQ-030-038 |
| Quote | Quote Cancelled (Inquiry Cancelled) | `quote.cancelled_inquiry` | Provider | Sent to each provider whose quote is auto-cancelled due to patient inquiry cancellation (FR-003 Workflow 5). **Provider receipt is mandatory — admin cannot disable this event.** Cancellation reason is patient-private — provider notification says only "Inquiry cancelled by patient". **MVP default channels: Email + Push.** Not subject to FR-032 provider notification preferences; FR-032 offers no toggle for this event. Available template variables: `quote.id`, `quote.provider_id`, `inquiry.id`, `inquiry.cancelled_at`; `inquiry.cancellation_reason` is excluded per privacy rule. | REQ-030-039 |
| Booking/Schedule | Booking Accepted — Slot Held (Pending Payment) | `booking.scheduled` | Patient | Fired by FR-006 when subquote acceptance creates the slot hold, or when an admin-authored replacement acceptance in the FR-006 provider-fault transfer creates the replacement booking, before the first payment is confirmed; states the payment deadline (hold expiry). The provider is not a recipient: the accepted or replacement provider learns of the booking through `quote.accepted` (`selected_subquote_accepted`). **Mandatory — neither the admin nor the patient can disable this event** | REQ-030-040 |
| Booking/Schedule | Hold Expiring Soon (Payment Reminder) | `booking.hold_expiring_soon` | Patient, Admin | Details in the FR-030 catalogue entry. | REQ-030-041 |
| Booking/Schedule | Payment Window Expired | `booking.payment_window_expired` | Patient, Provider, Admin | Details in the FR-030 catalogue entry. | REQ-030-042 |
| Booking/Schedule | Booking Revived | `booking.revived` | Patient, Provider | Details in the FR-030 catalogue entry. | REQ-030-043 |
| Booking/Schedule | Provider Unable to Proceed — Replacement Being Arranged | `booking.provider_fault_replacement` | Patient, Admin | Fired by FR-006 when an accepted booking is closed for provider fault: the provider withdraws after acceptance, drops out before treatment starts, or is suspended or deactivated after acceptance and before treatment starts (FR-015). An `In Progress` booking is not closed for provider fault and never fires this event; it stays `In Progress` with `supportRequired` for an admin decision. Tells the patient that an admin will arrange a replacement provider within the same inquiry and that the patient pays no cancellation fee; MUST NOT expose confidential suspension or deactivation reasons. Admins receive it as an exception alert so they can arrange the replacement. Providers are not recipients: the replacement provider learns through `quote.accepted` (`selected_subquote_accepted`) from the replacement acceptance, and the faulted provider is not notified by this event. **Mandatory — admin cannot disable this event** | REQ-030-044 |
| Booking/Schedule | Booking Confirmed | `booking.confirmed` | Patient, Provider | Critical | REQ-020-090 |
| Booking/Schedule | Booking Rescheduled | `booking.rescheduled` | Patient, Provider | Details in the FR-030 catalogue entry. | REQ-030-046 |
| Booking/Schedule | Booking Cancelled | `booking.cancelled` | Patient, Provider, Admin (optional) | Include cancellation reason where appropriate | REQ-020-092 |
| Booking/Schedule | Appointment Reminder | `booking.appointment_reminder` | Patient, Provider | Scheduled reminders; policy-driven | REQ-020-093 |
| Treatment | Treatment Start / Day-1 Starting | `treatment.started` | Patient, Provider | “Treatment start notifications” | REQ-020-094 |
| Treatment | Treatment Details Changed After Acceptance | `treatment.plan_changed` | Patient | Details in the FR-030 catalogue entry. | REQ-030-050 |
| Treatment | Treatment Cancelled | `treatment.cancelled` | Patient, Provider, Admin (optional) | Details in the FR-030 catalogue entry. | REQ-030-051 |
| Treatment | Treatment Completed (Post‑Op Instructions) | `treatment.completed` | Patient, Provider, Admin (optional) | Completion confirmation; triggers post-op and aftercare next steps. The patient copy also states the deadline to raise a problem and links to the support request; the provider and admin copies keep their wording without the deadline. No new event | REQ-030-052 |
| Treatment | Treatment Documentation Completed | `treatment.documentation_completed` | Provider | Sent when treatment documentation is successfully saved | REQ-020-098 |
| Treatment | Task In Progress Reminder | `treatment.task_in_progress_reminder` | Provider | Reminder for incomplete treatment tasks or documentation | REQ-020-099 |
| Payment | Payment Received / Receipt | `payment.received` | Patient, Provider, Admin (optional) | Critical | REQ-020-100 |
| Payment | Payment Failed | `payment.failed` | Patient, Admin (optional) | Critical | REQ-020-101 |
| Payment | Payment Due Reminder (Installment / Balance) | `payment.due_reminder` | Patient | “Installment reminder” (split-pay compatible) | REQ-020-102 |
| Billing/Payouts | Provider Payout Processed | `payout.provider_processed` | Provider, Admin (optional) | “They’ve been paid” notification to provider | REQ-020-103 |
| Billing/Payouts | Affiliate Payout Processed | `payout.affiliate_processed` | Affiliate, Admin (optional) | If affiliate program is enabled | REQ-020-104 |
| Billing/Payouts | Payout Failed | `payout.failed` | Admin, Provider (optional), Affiliate (optional) | Failure processing payout; recipients depend on payout type | REQ-020-105 |
| Messaging/Support | New Message Received | `message.received` | Patient, Provider, Admin (optional) | Real-time notification for new messages | REQ-020-106 |
| Messaging/Support | Support Case Created | `support.case_created` | Patient, Provider, Admin | Sent to submitter confirming case creation with case ID; Admin notification if case is urgent or unassigned | REQ-020-107 |
| Messaging/Support | Support Case Assigned | `support.case_assigned` | Admin | Sent to assigned admin when case is assigned to them | REQ-020-108 |
| Messaging/Support | Support Case Status Changed | `support.case_status_changed` | Patient, Provider | Sent when case status changes (Open → In Progress, In Progress → Resolved); includes status update and context | REQ-020-109 |
| Messaging/Support | Support Case Admin Reply | `support.case_admin_reply` | Patient, Provider | Sent when admin replies to case in communication thread; includes message content | REQ-020-110 |
| Messaging/Support | Support Case User Reply | `support.case_user_reply` | Admin | Sent to assigned admin (or all support staff if unassigned) when patient/provider replies to case | REQ-020-111 |
| Messaging/Support | Support Case Resolved | `support.case_resolved` | Patient, Provider | Sent when case is marked as Resolved; includes resolution summary and feedback resolution (if applicable) | REQ-020-112 |
| Messaging/Support | Support Case Reopened | `support.case_reopened` | Patient, Provider, Admin | Sent when closed case is reopened; includes reopening reason | REQ-020-113 |
| Messaging/Support | Support Case Closed | `support.case_closed` | Patient, Provider | Sent when case is closed (final status); includes resolution summary | REQ-020-114 |
| Messaging/Support | Support Case Escalated | `support.case_escalated` | Admin | Sent to escalation recipient (senior admin or technical team) when case is escalated | REQ-020-115 |
| Aftercare | Aftercare Activated | `aftercare.activated` | Patient, Provider | Includes assigned provider/clinician info where applicable | REQ-020-116 |
| Aftercare | Aftercare Milestone Due | `aftercare.milestone_due` | Patient, Provider (optional) | Details in the FR-030 catalogue entry. | REQ-030-072 |
| Aftercare | Scan Due / Missed Scan Reminder | `aftercare.scan_due` / `aftercare.scan_missed` | Patient | Details in the FR-030 catalogue entry. | REQ-030-073 |
| Aftercare | Questionnaire Due / Missed Questionnaire Reminder | `aftercare.questionnaire_due` / `aftercare.questionnaire_missed` | Patient | Details in the FR-030 catalogue entry. | REQ-030-074 |
| Aftercare | Aftercare Escalation / Red Flag Triggered | `aftercare.escalation_triggered` | Provider, Admin, Patient (optional) | Details in the FR-030 catalogue entry. | REQ-030-075 |
| Aftercare | Standalone Aftercare Payment Confirmed | `aftercare.standalone_payment_confirmed` | Patient, Provider (optional), Admin (optional) | Used for standalone aftercare flow payment confirmation | REQ-020-121 |
| Aftercare | Aftercare Provider Reassigned | `aftercare.provider_reassigned` | Patient, Provider (new aftercare provider) | Details in the FR-030 catalogue entry. | REQ-030-077 |
| Monitoring | Monitoring Case Pending Assignment | `monitoring.assignment_pending` | Admin | Advice-mode hair-loss/transplant-progress monitoring case activated and awaiting provider assignment (FR-037/FR-038) | REQ-020-123 |
| Monitoring | Monitoring Provider Assigned | `monitoring.provider_assigned` | Patient, Provider | Initial assignment or reassignment; assignment type distinguished in payload (FR-037/FR-038) | REQ-020-124 |
| Monitoring | Monitoring Provider Withdrawn | `monitoring.provider_withdrawn` | Admin, Patient | Provider withdraws with reason; case returns to Admin as Pending Reassignment (FR-037/FR-038) | REQ-020-125 |
| Monitoring | Monitoring Provider Reassigned | `monitoring.provider_reassigned` | Patient, Provider | Details in the FR-030 catalogue entry. | REQ-030-081 |
| Monitoring | Monitoring Advice Posted | `monitoring.advice_posted` | Patient | Provider submits or edits the one advice-window paragraph for the current window (FR-037/FR-038) | REQ-020-127 |
| Monitoring | Monitoring Case Completed | `monitoring.completed` | Patient | Patient completes the active monitoring case (FR-037/FR-038) | REQ-020-128 |
| Monitoring | Monitoring PDF Export Ready | `monitoring.export_ready` | Patient | Date-to-date summary PDF has finished generating and is downloadable (FR-037/FR-038) | REQ-020-129 |
| Monitoring | Monitoring Converted to Inquiry | `monitoring.converted_to_inquiry` | Patient | Monitoring case successfully converts into a distinct FR-003 inquiry (FR-037/FR-038) | REQ-020-130 |
| Monitoring | Monitoring Aftercare Conversion Started | `monitoring.aftercare_conversion_started` | Patient | The patient selects Switch to Aftercare Package on a transplant-progress monitoring case (FR-038). Patient only | REQ-020-154 |
| Monitoring | Monitoring Converted to Aftercare | `monitoring.converted_to_aftercare` | Patient | The aftercare request is successfully created from the monitoring case (FR-038) | REQ-020-155 |
| Reviews | Review Request | `review.requested` | Patient | “Review notifications” (typically post-treatment) | REQ-020-131 |
| Reviews | Review Published / New Review Posted | `review.published` | Provider | Notifies provider when a new published review appears on their profile; subject to provider Review Notifications preference in FR-032 | REQ-020-132 |
| Reviews | Provider Response Posted | `review.response_posted` | Patient | Notifies reviewer when provider posts a public response to their review | REQ-020-133 |
| Reviews | Review Removed by Admin | `review.removed_by_admin` | Patient | Notifies reviewer when admin removes their published review for policy/compliance reasons | REQ-020-134 |
| Reviews | Takedown Request Decided | `review.takedown_decided` | Patient | Notifies patient of admin approve/reject decision on their takedown request | REQ-020-135 |
| Promotions/Discounts | Provider Approval Needed for Platform Discount | `promotion.discount_approval_requested` | Provider | “Approval notifications to providers when new platform discount is created” | REQ-020-136 |
| Provider/Compliance | Provider Onboarding Requested | `provider.onboarding_requested` | Admin | New provider onboarding request awaiting review/approval. Not triggered at launch (future) | REQ-020-137 |
| Provider/Compliance | Provider-Caused Cancellation / Offer Unavailable | `provider.status_cancellation_patient` | Patient | FR-015 Alternative Flow A5 / Screen 4. One per affected inquiry/case when provider suspension (`ProviderSuspended`) or deactivation (`ProviderDeactivated`) cancels the patient's case or the provider's offer before acceptance. A cancelled unsent draft quote alone does not trigger this notice, because the patient never saw it. For a case already accepted, the patient instead receives `booking.provider_fault_replacement`. Before acceptance, three variants apply (FR-003 Workflow 2 Alternative Flow B4, REQ-003-021): when other offers remain open, the notice says "[Clinic] is no longer available. Your other offers are still open."; when no other live offer remains and the inquiry is redistributed, the notice says "[Clinic] is no longer available. We are finding new offers for you."; when the patient had explicitly selected the affected provider, the notice asks the patient to confirm the redistribution first. Includes inquiry/case reference and a Contact Admin/Support action. MUST NOT say the patient cancelled, instruct payment against the cancelled selection, or expose confidential suspension/deactivation reasons. **Mandatory** (cannot be disabled in FR-030 rules); sent regardless of FR-015's "Notify Provider" checkbox. MVP channels: Email + Push + in-app (global patient toggles still apply to Email/Push; in-app record always created) | REQ-030-094 |
| Provider/Compliance | Provider-Caused Cancellation — Admin Support Required | `provider.status_cancellation_admin_support` | Admin | Same trigger, and also when a provider-status event leaves an `In Progress` booking open and flagged `supportRequired` for an admin decision (move the booking to `Aftercare` with aftercare reassignment, or cancel it with a reason), or leaves an `Aftercare` booking or FR-011 standalone aftercare case flagged for admin aftercare reassignment (FR-006 Alternative Flow B6). Mandatory admin-support alert per affected inquiry/case with patient, inquiry/case reference, prior stage, cause, and FR-016 deep link (Admin Support Required filter). Sent to admins with the FR-031 Respond to Support permission (default roles Super Admin, Aftercare Specialist, and Support Staff); opening the FR-016 list also requires View Patients. Sent regardless of "Notify Provider"; pinned as critical in the admin dropdown. No FR-034 ticket is auto-created | REQ-030-095 |
| Provider/Compliance | Provider Suspended / Deactivated | `provider.suspended` / `provider.deactivated` | Provider (Owner only) | FR-015 Screen 4. Sent only when "Notify Provider" is checked (default); FR-015 locks it on for deactivations from an FR-032 account-closure request (A7), so `provider.deactivated` is always sent then. For a scheduled change it is sent when the scheduled change is created (with the effective date) and again when it takes effect; with "Notify Provider" unchecked it is sent at neither point. Team members are not emailed; they see the FR-032 Rule 6 banner or login message. Email with action taken, admin-provided reason, effective date (if scheduled), and admin support contact. Unaffected by provider FR-032 category preferences (account notice) | REQ-030-096 |
| Provider/Compliance | Provider Account Activation (Welcome / Set Password) | `provider.activation` | Provider | FR-015 Main Flow step 13 and Alternative Flow A1. Welcome email with platform introduction, login email, first-login instructions, and the one-time set-password link (expires in 24 hours). Re-sent on A1 resend (previous link invalidated). **Mandatory**; cannot be disabled in FR-030 rules. Unaffected by FR-032 category preferences. Email only | REQ-020-141 |
| Provider/Compliance | Owner Login Email Changed | `provider.login_email_changed` | Provider (old and new login address) | FR-015 Screen 3 Tab 1, Owner login email change by an admin. One email to each address. To the old address: the login email for [clinic] was changed to [new address, partly masked] by a Hairline admin on [date/time]; contact support if this was unexpected. To the new address: this address is now the login email for [clinic]. If the Owner's `password_set` is false, `provider.activation` is also sent to the new address. **Mandatory** security notice; cannot be disabled in FR-030 rules or by FR-032 category preferences. Email only | REQ-020-142 |
| Provider/Compliance | Provider Reactivated | `provider.reactivated` | Provider (Owner only) | FR-015 Alternative Flow A6 / Screen 5. Sent only when "Notify Provider" is checked (default). Email with reactivation notice, admin-provided reason, and admin support contact; notes that cancelled cases are not restored and, if a scheduled change the provider was notified of was cancelled by the reactivation, that it no longer applies. **Mandatory** in FR-030 rules when triggered. Unaffected by FR-032 category preferences (account notice) | REQ-020-143 |
| Provider/Compliance | Scheduled Status Change Cancelled | `provider.scheduled_change_cancelled` | Provider (Owner only) | FR-015 Screen 4 (Cancel Scheduled Change). Sent when an admin cancels a pending scheduled suspension/deactivation and the scheduled change had "Notify Provider" checked. Email states which change was cancelled and its former effective date. When a reactivation cancels the scheduled change automatically, the note is included in `provider.reactivated` instead. **Mandatory** in FR-030 rules when triggered. Unaffected by FR-032 category preferences (account notice) | REQ-020-144 |
| Provider/Compliance | Provider Account-Closure Requested | `provider.closure_requested` | Admin | FR-032 Request Account Closure (step 10) / FR-015 A7. Sent to admins with View Providers permission when a provider submits a closure request. Includes provider and clinic name, request date, optional reason, and a deep link to the request in the FR-015 provider profile (Closure Requested filter). **Mandatory**; cannot be disabled in FR-030 rules. Email + in-app | REQ-020-145 |
| Provider/Compliance | Provider Account-Closure Request Rejected | `provider.closure_rejected` | Provider | FR-015 A7 step 6 / FR-032 step 16. Sent when an admin rejects a closure request. Email states that the account stays Active, gives the admin review notes, and the admin support contact. **Mandatory**; cannot be disabled in FR-030 rules. Unaffected by FR-032 category preferences (account notice). Email only | REQ-020-146 |
| Provider/Compliance | Provider Document Expiration Warning | `provider.document_expiration_warning` | Admin, Provider (optional) | License/credential expiry warnings; timing is policy-driven. Not triggered at launch (future) | REQ-020-147 |
| System/Operations | System Escalation | `system.escalation` | Admin | Operational escalation events requiring admin action | REQ-020-148 |
| System/Operations | System Alert | `system.alert` | Admin | System health/monitoring alerts surfaced via notifications | REQ-020-149 |
| System/Operations | Analytics Export Ready | `analytics.export_ready` | Provider | Details in the FR-030 catalogue entry. (FR-014 REQ-014-062/063) | REQ-030-105 |

- Channels: email, push; SMS is an optional/configurable channel for urgent events in the target architecture but is **not available in MVP** (no SMS notifications are sent until a later phase explicitly enables this capability). (REQ-020-030)
- User preferences (MVP):
  - **Patients**: global Email/Push toggles (managed in FR-001: Patient Authentication & Profile Management, Settings → Notifications section); per‑category preferences deferred to V2 (not in scope). (REQ-020-031)
  - **Providers**: See REQ-020-023.
- Notification listing screens: See REQ-020-008, REQ-020-009 and REQ-020-010.
- Throttling/de‑duplication and delivery tracking. (REQ-020-006, REQ-020-007)

Out of Scope:

- In‑app messaging content design (covered in FR-012).
- Per‑category user preferences on patient app (explicitly V2).
- Quote Declined (`quote.declined`): Post-MVP and hidden, as in the FR-030 Post-MVP / Hidden Events list. It is reserved for an explicit governed decline flow; no MVP producer exists because patients have no explicit decline action (FR-005). FR-005 sibling Not Selected and competing-parent cancellation outcomes do not use this event. (REQ-020-032)

### Entry Points

- System events published by core modules (inquiry, quote, booking, payment, chat, scheduling, aftercare) trigger notifications via S-03. (REQ-020-033)
- Users access Settings → Notifications to set global Email/Push toggles (MVP). (REQ-020-033)

---

## Business Workflows

### Main Flow: Event → Notification Dispatch

Actors: System, Notification Service, Recipient
Trigger: Business event occurs (e.g., booking confirmed)
Outcome: Recipient receives notification according to channel preferences

Steps:

1. Event emitted with payload (type, actor, subject, recipient id). (REQ-020-034)
2. Notification Service evaluates preferences and throttling. (REQ-020-035)
3. Builds message from template and routes to enabled channels. (REQ-020-035)
4. Records delivery attempt and status; exposes audit. (REQ-020-036)
5. (Post-MVP, future phase: if SMS enabled and urgent) include SMS path; in MVP, email/push only. (REQ-020-037)

### Alternative Flows

- A1: Preference Disabled (REQ-020-038)
  - Trigger: Recipient has disabled Email or Push.
  - Outcome: Channel suppressed; delivery attempted on remaining enabled channels.

- B1: Throttling (REQ-020-039)
  - Trigger: Excessive events in short time window.
  - Outcome: Coalesce or defer per policy; record suppression in audit.

- B2: Channel Failure (REQ-020-040)
  - Trigger: Email/push/SMS provider unavailable.
  - Outcome: Retry with backoff; failover when configured; status reflects failure cause.

---

## Screen Specifications

### Patient Platform Screens

Notification settings UI for patients is defined in `FR-001: Patient Authentication & Profile Management` (Settings → Notifications). FR-020 relies on that screen; it is not re-specified here to avoid duplication.

#### Screen 1: Patient – Notification Listing

Purpose: Display notification history for patients to view all received notifications.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       | Graph field |
|-------------------|--------|----------|-----------------------------|------------------------|------|
| Notification List | list   | Yes      | Chronological list of notifications | Paginated, 20 per page | no graph field (list of the per-notification rows below) |
| Notification Type | badge  | Yes      | Type indicator (quote, booking, payment, etc.) | Read-only | ENT-notification-record.type |
| Title             | text   | Yes      | Notification title/subject  | Read-only | ENT-notification-record.title |
| Message           | text   | Yes      | Notification body content   | Read-only, truncated with "Read more" | ENT-notification-record.message |
| Timestamp         | datetime | Yes    | When notification was sent  | Read-only, relative time | ENT-notification-record.created_at |
| Read Status       | badge  | Yes      | Read/Unread indicator       | Toggle on click | ENT-notification-record.read_status |
| Action Button     | button | No       | Deep link to related content | Context-dependent | no graph field (control) |

Field validation rules (Message, Timestamp): REQ-020-069.

Business Rules:

- Notifications sorted by most recent first (newest at top). (REQ-020-059)
- Unread notifications highlighted with visual indicator. (REQ-020-060)
- Clicking notification marks as read and navigates to related content (if applicable). (REQ-020-061)
- Filter options: All, Unread, By Type (Inquiry, Quote, Booking, Payment, Treatment, Aftercare, Account, Messaging, Review, Monitoring, Support, Provider/Compliance). (REQ-020-062)
- Search functionality: search by notification content. (REQ-020-065)

---

### Provider Platform Screens

#### Screen 2: Provider – Notification Dropdown

Purpose: Display notifications in provider dashboard header dropdown with infinite scroll.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       | Graph field |
|-------------------|--------|----------|-----------------------------|------------------------|------|
| Notification Count | badge | Yes      | Unread notification count   | Real-time update | no graph field (count derived from read status) |
| Notification Items | list   | Yes      | Infinite scroll list of notifications | Load more on scroll | no graph field (list of the per-notification rows below) |
| Notification Type | badge  | Yes      | Type indicator              | Read-only | ENT-notification-record.type |
| Title             | text   | Yes      | Notification title          | Read-only, truncated | ENT-notification-record.title |
| Message           | text   | Yes      | Notification body content   | Read-only, truncated | ENT-notification-record.message |
| Timestamp         | datetime | Yes    | When notification was sent  | Read-only, relative time | ENT-notification-record.created_at |
| Read Status       | indicator | Yes    | Read/Unread dot             | Visual indicator | ENT-notification-record.read_status |
| Load More Trigger | scroll | Yes      | Infinite scroll trigger     | Loads next batch on scroll | no graph field (control) |

Field validation rules (Message, Title, Timestamp): REQ-020-069.

Business Rules:

- See REQ-020-009.
- See REQ-020-059.
- Unread count badge updates in real-time. (REQ-020-066)
- See REQ-020-061.
- Filter options within dropdown: All, Unread, By Type (Quote, Booking, Payment, etc.). (REQ-020-063)
- Search functionality: search by notification content within dropdown. (REQ-020-065)

---

Provider notification settings UI is defined in `FR-032: Provider Dashboard Settings & Profile Management (PR-06)` under Settings → Notifications. FR-020 consumes those preferences; the screen itself is not re-specified here.

---

### Admin Platform Screens

#### Screen 3: Admin – Notification Dropdown

Purpose: Display notifications in admin dashboard header dropdown with infinite scroll.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       | Graph field |
|-------------------|--------|----------|-----------------------------|------------------------|------|
| Notification Count | badge | Yes      | Unread notification count   | Real-time update | no graph field (count derived from read status) |
| Notification Items | list   | Yes      | Infinite scroll list of notifications | Load more on scroll | no graph field (list of the per-notification rows below) |
| Notification Type | badge  | Yes      | Category of the notification (Payment, Aftercare, Booking, Support, etc.) | Read-only | ENT-notification-record.type |
| Title             | text   | Yes      | Notification title          | Read-only, truncated | ENT-notification-record.title |
| Message           | text   | Yes      | Notification body content   | Read-only, truncated | ENT-notification-record.message |
| Timestamp         | datetime | Yes    | When notification was sent  | Read-only, relative time | ENT-notification-record.created_at |
| Read Status       | indicator | Yes    | Read/Unread dot             | Visual indicator | ENT-notification-record.read_status |
| Urgency           | badge  | Yes      | Critical, Warning or Info; the red badge shows for Critical only | Read-only, color-coded | ENT-notification-record.urgency |
| Load More Trigger | scroll | Yes      | Infinite scroll trigger     | Loads next batch on scroll | no graph field (control) |

Field validation rules (Message, Title, Timestamp): REQ-020-069. Notification Type and Urgency: REQ-020-070.

Business Rules:

- See REQ-020-010.
- See REQ-020-059.
- Critical notifications highlighted with red badge and always shown at top (before non-critical). (REQ-020-067)
- See REQ-020-066.
- See REQ-020-061.
- Filter options within dropdown: All, Unread, Critical, By Type (Payment, Aftercare, Booking, Support, etc.). (REQ-020-064)
- Search functionality: search by notification content within dropdown. (REQ-020-065)

---

Notification policy, throttling, and delivery monitoring UI live in `FR-030: Notification Rules & Configuration` (including template editor; OTP templates in `FR-026`). FR-020 depends on those capabilities and does not re-specify the admin screen.

---

### Consolidated Screen Notes

- Patient – Notification Listing: Patient App → Notifications (dedicated tab or menu item); notifications persist for 90 days then archive. (REQ-020-068)
- Provider – Notification Dropdown: Provider dashboard header bell icon; real-time updates (WebSocket or polling); infinite scroll within dropdown at max height.
- Admin – Notification Dropdown: Admin dashboard header bell icon; real-time updates (WebSocket or polling); infinite scroll within dropdown at max height; critical items per REQ-020-067.
- Patient notification settings: Owned by `FR-001: Patient Authentication & Profile Management` (Settings → Notifications).
- Provider notification settings: Owned by `FR-032: Provider Dashboard Settings & Profile Management (PR-06)` (Settings → Notifications).
- Admin policy/config screens: Owned by `FR-030: Notification Rules & Configuration` (template editor) and `FR-026: App Settings & Security Policies` (OTP templates).

---

## Business Rules

- **Patient Preferences**: See REQ-020-031 (Module Scope, User preferences) and REQ-020-004.
- **Provider Preferences**: Providers can choose which notification types to receive (quote notifications, schedule notifications, treatment start notifications, aftercare notifications, review notifications, promotion/discount notifications) via notification preferences settings (managed in FR-032: Provider Dashboard Settings & Profile Management, Settings → Notifications section). Every event that is mandatory for providers (`quote.cancelled_inquiry`, the selected-provider and not-selected-provider outcomes of `quote.accepted`, `booking.payment_window_expired`, `booking.revived` and `booking.rescheduled`) is delivered regardless of these preferences. (REQ-020-023, REQ-020-045)
- **Admin Notifications**: Admin recipients and event coverage are defined by the FR-030 event catalog and configured rules (no additional hard-coded admin event list in FR-020). (REQ-020-046)
- **Notification Rule Owns the Details**: for each notice, the notification Rule (the one in this PRD, or the FR-030 catalogue Rule where this PRD's catalogue row is a pointer) is the one place that states recipients, content and whether the notice can be switched off. A feature FR states only what is its own (when the event happens, what the screen does, what is audited) and points to the notification Rule. (REQ-020-156)
- **Every Feature Uses the Notification Service**: every feature that sends a notice sends it through the Notification Service (S-03), so channel preferences, throttling, templates and delivery tracking apply to every notice (REQ-020-152).
- **Event Ownership**: an event that produces a notification belongs to the FR-030 catalogue, and this PRD cites it. This includes the provider.* events, `inquiry.ttfq_sla_breached` and `analytics.export_ready`. An event that produces no notification belongs to the FR that triggers it. (REQ-020-157)
- **Provider-Status Cancellation Notifications (FR-015 A5)**: See REQ-020-013 and REQ-020-014. Patient content uses provider-caused wording, a Contact Admin/Support action, no payment instruction, and no confidential suspension/deactivation reason.
- **Aftercare Provider Reassignment Notice (FR-011)**: See REQ-020-022. `aftercare.provider_reassigned` is produced only by FR-011, including cases reassigned after an FR-015 provider-status event. It is mandatory, cannot be disabled in FR-030 rules, and is not subject to FR-032 provider notification preferences. No admin alert is sent because the admin performs the reassignment.
- **Provider Lifecycle Notifications (FR-015)**: See REQ-020-014, REQ-020-015 and REQ-020-016. `provider.activation` is mandatory and cannot be disabled, because without it a new provider cannot set a password. `provider.suspended`, `provider.deactivated`, `provider.reactivated`, and `provider.scheduled_change_cancelled` go to the provider Owner only, follow FR-015's "Notify Provider" choice and, when triggered, cannot be disabled in FR-030 rules or by FR-032 category preferences.
- **FR-005 Quote Outcome Privacy**: `quote.accepted` carries an explicit `outcome` code and recipient scope. Payload rendering MUST use an allowlist per recipient; non-selected providers MUST NOT receive the selected provider identity, accepted price, or another provider's quote/subquote identifiers. (REQ-020-051)
- **Quote, Booking and Treatment-Change Notifications** (mirrors the FR-030 Quote, Booking and Treatment-Change Event Rules; FR-030 prevails on any mismatch):
  - **Producers**: FR-004 produces `quote.submitted`, `quote.updated`, `quote.expiring_soon`, `quote.expired` and `quote.withdrawn`. FR-005 produces `quote.accepted` and its outcomes. FR-006 produces `booking.scheduled`, `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.rescheduled` and `booking.provider_fault_replacement`. FR-010 produces `treatment.plan_changed`. Admin sets the quote-expiring-soon and hold-expiring-soon lead times in FR-026. (REQ-020-052)
  - **Recipient grain for `quote.accepted`**: one provider notice per sent parent quote, never one per subquote. The de-duplication key is acceptance record + parent quote + recipient. The recipient matrix below shows each population. (REQ-020-053)
  - **Unsent drafts**: when FR-004 cancels an unsent draft parent quote as `cancelled_other_accepted` because another subquote was accepted, no notification is sent to the drafting provider or anyone else. Only sent parent quotes receive acceptance outcomes. (REQ-020-054)
  - **Pre-acceptance price variables**: `quote.submitted`, `quote.updated`, `quote.expiring_soon`, `quote.expired` and `quote.withdrawn` may use only parent-level variables: the "From" price (lowest subquote price in the parent quote) with its currency, option count, treatment, expiry date, provider name and the parent quote reference. A single quote total does not exist and MUST NOT be offered as a variable. (REQ-020-018)
  - **Post-acceptance money variables**: on `quote.accepted` (selected-provider outcome) and on every `booking.*` event, price, currency, date range and promotion variables resolve from the accepted snapshot recorded at acceptance, never from the live parent quote, Quote Option or package. Appointment variables on `booking.*` events resolve from the booking's current appointment, which an admin may change through FR-006; the snapshot keeps the accepted appointment as the baseline. `booking.rescheduled` carries both the previous and the new appointment. (REQ-020-018, REQ-020-021)
  - **Treatment-detail variables**: `treatment.plan_changed` and other treatment events may use the current treatment plan, clinicians and graft count maintained through FR-010; they MUST NOT carry changed money values. (REQ-020-018)
  - **Locks**: `quote.withdrawn`, the selected-provider and not-selected-provider outcomes of `quote.accepted`, `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement`, `booking.scheduled`, `booking.rescheduled` and `treatment.plan_changed` are mandatory and cannot be disabled in FR-030 rules. The patient cannot disable `booking.scheduled` either. `quote.expiring_soon` and `booking.hold_expiring_soon` are admin-configurable (REQ-020-055). See REQ-020-045 for the mandatory provider events and FR-032 provider notification preferences.
  - **Acceptance recipients**: at acceptance the patient receives only `booking.scheduled`; `quote.accepted` goes to providers only (the accepted provider and each not-selected provider). No admin notification is sent for an acceptance. The same applies to an admin-authored replacement acceptance in the FR-006 provider-fault transfer: the patient receives `booking.scheduled` with the replacement payment deadline, and the replacement provider receives `quote.accepted` (`selected_subquote_accepted`). (REQ-020-019, REQ-020-056)
  - **Admin exception alerts**: admins are alerted only for exceptions on the quote-to-booking path: a slot hold expiring while the first payment is unpaid (`booking.hold_expiring_soon`), Payment Window Expired (`booking.payment_window_expired`), provider fault (`booking.provider_fault_replacement`) and a provider withdrawing a quote that was already accepted (`quote.withdrawn`). Routine acceptances are visible on admin dashboards only. (REQ-020-019)
  - **Payment window scope**: `booking.payment_window_expired` covers only the first payment step (deposit or first instalment). (REQ-020-057)

**`quote.accepted` recipient matrix** (example: provider P has sent parent quotes A and B, and the patient accepts one subquote in A) (REQ-020-058):

| Population | Provider notice | Outcome | Payload allowlist |
|---|---|---|---|
| Accepted subquote in parent A | One notice to P for parent A (mandatory) | `selected_subquote_accepted` | Accepted subquote details from the accepted snapshot |
| Other subquotes in parent A (siblings) | No separate notice; listed inside P's parent A notice | `sibling_subquote_not_selected` | P's own parent A subquote references and outcome |
| Other sent parent quote of the same provider (parent B) | One separate notice to P for parent B (mandatory) | `competing_parent_cancelled_other_subquote_accepted` | Parent B quote and subquote references, outcome and reason |
| Sent parent quote of any other provider | One notice per parent quote to that provider (mandatory) | `competing_parent_cancelled_other_subquote_accepted` | That provider's own parent quote and subquote references, outcome and reason; no selected provider identity and no accepted price |
| Unsent draft parent quote of any provider | No notice (draft cancelled silently by FR-004) | None | None |

See REQ-020-019. The patient never receives sibling or competing outcomes.

- One notification record per attempt with channel, provider, status, and timestamp. (REQ-020-041)
- Throttling and suppression policies are transparent in audit logs. (REQ-020-042)
- **Notification Content Management**: Notification content (titles, messages, templates) is managed in FR-030: Notification Rules & Configuration via the Notification Template Editor. (REQ-020-047)
- **Notification Content Management**: Notification templates (email, push, SMS) are managed in FR-030: Notification Rules & Configuration via the Notification Template Editor, which supports dynamic variables, multi-language content, rich text formatting (email), and preview capabilities.
- **Email Template Management** (REQ-020-048):
  - General notification email templates: Managed in FR-030 (Notification Rules & Configuration) with support for dynamic variables, multi-language content, rich text formatting, and preview capabilities.
  - OTP email templates (verification, password reset): Managed in FR-026 (App Settings & Security Policies) as part of authentication settings.
  - Admins can create/edit templates per event type and channel with variable substitution, multi-language support, and preview.
- Event-driven design; idempotent handlers; retries with backoff. (REQ-020-043)
- Privacy: no sensitive content in notifications; deep links use secure tokens. (REQ-020-044)
- SMS costs are controlled via caps; only urgent categories use SMS. (REQ-020-050)

### Admin Editability

Editable by Admin:

- Throttling thresholds, SMS enablement, default channel policies, templates. (REQ-020-049)

Fixed in Codebase (Not Editable):

- Supported channels (Email/Push; SMS behind config), baseline event types per FR-030 event catalog. (REQ-020-049)

Configurable with Restrictions:

- Maximum SMS volume, high‑priority categories allowed for SMS. (REQ-020-049)

---

## Dependencies

- **FR-001**: Patient Authentication & Profile Management (patient notification preferences UI).
- **FR-012**: Messaging (message received events).
- **FR-004**: Quote Submission & Management (producer of the quote events).
- **FR-005**: Quote Comparison & Acceptance (acceptance outcome and privacy contract).
- **FR-006**: Booking & Scheduling (producer of the booking events).
- **FR-010**: Treatment Execution & Documentation (producer of `treatment.plan_changed`).
- **FR-026**: App Settings & Security Policies (OTP email templates; quote-expiring-soon and hold-expiring-soon lead times).
- **FR-015**: Provider Management (provider lifecycle notices, "Notify Provider" option).
- **FR-016**: Admin Patient Management (Admin Support Required filter and resolution target of the admin-support alert).
- **FR-030**: Notification Rules & Configuration (template management, notification rule configuration).
- **FR-032**: Provider Dashboard Settings & Profile Management (PR-06; provider notification preferences UI).
- **FR-037**/**FR-038**: Monitor Your Hair Loss / Monitor Your Transplant Progress (monitoring events).

---


## User Scenarios & Testing

### User Story 1 – Patient toggles preferences (P1)

Why: Respect user choice on communication channels.

Independent Test: Disable Email and verify only Push is delivered for eligible events.

Acceptance Scenarios:

1. Given Email is disabled, when an event fires, then no email is sent and push is delivered (if enabled).
2. Given both Email and Push disabled, when an event fires, then no notification is sent and suppression is logged.

### User Story 2 – Admin enables SMS for urgent events (P2, post-MVP)

Post-MVP: SMS is not available in MVP; this story applies only once a later phase enables SMS.

Why: Ensure urgent communication reaches users reliably.

Independent Test: Mark “appointment reminder” as SMS‑eligible; verify SMS sent under policy.

Acceptance Scenarios:

1. Given SMS is enabled for urgent reminders, when a reminder event fires, then an SMS is sent and logged.
2. Given SMS volume cap reached, when more SMS would be sent, then they are suppressed and recorded.

### User Story 3 – Spike throttling (P2)

Why: Avoid spamming users during bursts.

Independent Test: Simulate high‑frequency message events; ensure de‑duplication.

Acceptance Scenarios:

1. Given many identical events in a short window, when throttling applies, then only coalesced notifications are sent.
2. Given throttling suppressed some events, when admin reviews logs, then suppression entries are visible.

### User Story 4 – Cancellation notification delivery (P1)

Why: Inquiry cancellation triggers mandatory notifications to patient (confirmation) and affected providers (cascade). Privacy rules must be enforced — provider must not see patient's cancellation reason.

Independent Test: Patient cancels inquiry with 2 active quotes; verify patient receives confirmation via email + push; both providers receive `quote.cancelled_inquiry` via email + push with privacy-compliant content; admin receives optional `inquiry.cancelled` if enabled.

Acceptance Scenarios:

1. Given patient cancels inquiry with 2 active quotes, when cancellation completes, then patient receives `inquiry.cancelled` notification via both email and push within 5 minutes confirming cancellation with reason visible. (REQ-020-071)
2. Given patient cancels inquiry, when providers receive `quote.cancelled_inquiry` notification, then notification says "Inquiry cancelled by patient" without revealing the patient's cancellation reason.
3. Given provider has turned off quote notifications in FR-032 preferences, when inquiry is cancelled, then the provider still receives `quote.cancelled_inquiry`, because the event is mandatory and FR-032 offers no toggle for it.
4. Given patient has disabled push notifications (email only), when inquiry is cancelled, then patient receives `inquiry.cancelled` via email only; push is suppressed per preference.

### User Story 5 – Provider-caused cancellation notifications (P1)

Why: FR-015 provider suspension/deactivation cancels patient cases/offers through no patient action; patients must be directed to admins and admins alerted for special support.

Independent Test: Suspend a provider with "Notify Provider" unchecked while it holds one unaccepted offer on one inquiry and one accepted booking on another; force one email failure.

Acceptance Scenarios:

1. Given the cascade completes, when notifications dispatch, then the patient with the unaccepted offer receives one `provider.status_cancellation_patient` per affected record with its reference and Contact Admin/Support action, no "you cancelled" wording, no payment instruction, and no suspension reason.
2. Given the same event, then admins receive one `provider.status_cancellation_admin_support` per affected record linking to FR-016, and no provider email is sent because "Notify Provider" is unchecked.
3. Given an email attempt fails and retries succeed, then the patient receives exactly one notification per channel for that status event + record, and the cancelled record is not restored.
4. Given the same event, when the accepted booking is closed and handed to the FR-006 admin transfer, then that patient receives `booking.provider_fault_replacement` and no `provider.status_cancellation_patient`.
5. Given "Notify Provider" is checked, then the provider receives `provider.suspended` email with action, reason, effective date, and support contact.
6. Given the suspended provider also has an `In Progress` booking, when the cascade completes, then the booking stays `In Progress` with `supportRequired`, admins receive one `provider.status_cancellation_admin_support` for it, and no `booking.provider_fault_replacement` is sent.
7. Given an admin later reassigns that patient's aftercare to another provider, then the patient and the new aftercare provider each receive one `aftercare.provider_reassigned` and no admin alert is sent.

---

### User Story 6 – Acceptance outcome notifications (P1)

Why: When a patient accepts one subquote, every provider with a sent parent quote must learn the outcome once per parent quote, and competing providers must not learn who was selected or at what price.

Independent Test: Provider P has sent parent quote A (subquotes A-1, A-2, A-3) and sent parent quote B, provider Q has sent parent quote C, and provider R has an unsent draft D on the same inquiry; the patient accepts A-2.

Acceptance Scenarios:

1. Given the patient accepts A-2, when notifications dispatch, then P receives exactly one `quote.accepted` notice for parent A with outcome `selected_subquote_accepted`, and its price, currency, date range and appointment come from the accepted snapshot.
2. Given the same acceptance, then P's parent A notice lists A-1 and A-3 as `sibling_subquote_not_selected`, and no separate notice is sent for each sibling subquote.
3. Given P also has sent parent quote B, then P receives one separate notice for parent B with outcome `competing_parent_cancelled_other_subquote_accepted`, containing only parent B references, the outcome and the reason.
4. Given Q has sent parent quote C, then Q receives one notice with outcome `competing_parent_cancelled_other_subquote_accepted` whose payload contains only Q's own parent quote and subquote references, the outcome and the reason, and does not contain P's identity or the accepted price.
5. Given R's draft D was never sent, then R receives no notice when FR-004 cancels the draft.
6. Given an admin opens the `quote.accepted` rule in FR-030, then the selected-provider and not-selected-provider outcomes are locked on, and the rule offers no patient or admin recipient.
7. Given the acceptance completes and any delivery retries run, then no `quote.declined` event is emitted for any provider, and each provider receives at most one notice per parent quote per channel (de-duplicated on acceptance record + parent quote + recipient).
8. Given the patient accepts A-2, then the patient receives only `booking.scheduled` and no `quote.accepted` notice, and no admin notification is sent for the acceptance.

---

## Functional Requirements Summary

- REQ-020-001: System MUST send email for key events per templates.
- REQ-020-002: System MUST send push notifications to mobile app.
- REQ-020-003: Post-MVP (future phase): System MUST support optional/configurable SMS for urgent events. SMS is not available in MVP; no SMS is sent until a later phase enables it.
- REQ-020-004: System MUST allow patients to configure notification preferences (MVP: global Email/Push toggles managed in FR-001: Patient Authentication & Profile Management).
- REQ-020-005: System MUST support notification event types in the FR-030 MVP event catalog (Admin-Configurable Notification Event Types), routed to enabled channels and templates.
- REQ-020-006: System MUST throttle notifications to prevent spam and log suppression.
- REQ-020-007: System MUST track and expose delivery status per attempt.
- REQ-020-008: System MUST provide notification listing screen for patients to view notification history (paginated, 20 per page).
- REQ-020-009: System MUST provide notification dropdown in provider dashboard header with infinite scroll (loads 20 notifications per batch, no separate listing screen).
- REQ-020-010: System MUST provide notification dropdown in admin dashboard header with infinite scroll (loads 20 notifications per batch, no separate listing screen).
- REQ-020-011: System MUST send notifications to admins for any enabled FR-030 event types where Admin is a primary or optional recipient (per rule configuration).
- REQ-020-012: System MUST route FR-005 acceptance outcomes through `quote.accepted` with an explicit `outcome` code and recipient-scoped payload, sending one provider notice per sent parent quote (de-duplicated on acceptance record + parent quote + recipient) and no notice for unsent drafts; the selected-provider and not-selected-provider outcomes MUST NOT be disableable. Non-selected providers MUST receive only their own outcome context and MUST NOT receive the selected provider identity or accepted price; `quote.declined` MUST NOT represent FR-005 system-generated sibling or competing-parent outcomes.
- REQ-020-013: System MUST send mandatory `provider.status_cancellation_patient` and `provider.status_cancellation_admin_support` notifications for each record affected by an FR-015 provider suspension/deactivation, regardless of the "Notify Provider" checkbox, with privacy-safe patient content (no patient-cancelled wording, no payment instruction, no confidential reason), and MUST use the FR-003 pre-acceptance variants (Workflow 2 Alternative Flow B4, REQ-003-021): "[Clinic] is no longer available. Your other offers are still open." when other offers remain open; "[Clinic] is no longer available. We are finding new offers for you." when the inquiry is redistributed, or a confirmation request first when the patient had explicitly selected the affected provider.
- REQ-020-014: System MUST retry failed provider-status notifications (per Flow B2) without duplicates per provider-status event + affected record + recipient, and a retry MUST NOT restore a cancelled record; System MUST send `provider.suspended` / `provider.deactivated` email to the provider Owner only when "Notify Provider" is checked; for a scheduled change, the email MUST be sent when the change is created and again when it takes effect. `provider.status_cancellation_admin_support` MUST go to admins with the FR-031 Respond to Support permission, and `provider.reactivated` and `provider.scheduled_change_cancelled` MUST go to the provider Owner only.
- REQ-020-015: System MUST always send `provider.activation` (non-disableable) when FR-015 creates a provider or a resend is requested, and MUST send `provider.reactivated` and `provider.scheduled_change_cancelled` to the provider when FR-015's "Notify Provider" applies; these events MUST NOT be suppressed by FR-030 toggles or FR-032 category preferences. System MUST always send `provider.login_email_changed` to the old and the new address when an admin changes the Owner login email in FR-015.
- REQ-020-016: System MUST send `provider.closure_requested` to admins when a provider submits an FR-032 account-closure request and `provider.closure_rejected` to the provider when an admin rejects it, and MUST always send `provider.deactivated` for a deactivation that processes a closure request; these events MUST NOT be suppressed by FR-030 toggles or FR-032 category preferences.
- REQ-020-017: System MUST send `quote.withdrawn` (before and after acceptance), `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement` and `treatment.plan_changed` as mandatory notifications that FR-030 toggles cannot disable, and MUST send `quote.expiring_soon` and `booking.hold_expiring_soon` at the FR-026 lead times when enabled in FR-030.
- REQ-020-018: System MUST render pre-acceptance quote notifications with parent-level variables only ("From" price with currency, option count, treatment, expiry) and no single quote total, MUST resolve post-acceptance money variables (price, currency, date range, appointment, promotion) from the accepted snapshot, and MUST NOT carry changed money values in treatment events.
- REQ-020-019: At acceptance, System MUST send the patient only `booking.scheduled` and no `quote.accepted` notice, MUST send `quote.accepted` only to the accepted provider and the not-selected providers, and MUST NOT send an admin notification for the acceptance. Admins MUST be alerted only for the exceptions `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.provider_fault_replacement` and `quote.withdrawn` when the withdrawn quote was already accepted; `quote.withdrawn` MUST always reach the patient and MUST NOT alert admins for a withdrawal before acceptance.
- REQ-020-020: System MUST always send `quote.cancelled_inquiry` to each provider whose quote is auto-cancelled by an inquiry cancellation; neither FR-030 toggles nor FR-032 provider notification preferences may suppress it.
- REQ-020-021: System MUST send `booking.scheduled` to the patient only, as a mandatory event that the patient cannot disable, both when the patient accepts a subquote and when an admin-authored replacement acceptance creates a replacement booking. System MUST send the mandatory `booking.rescheduled` to the patient and the provider when an admin changes the appointment, with the previous and the new appointment. Booking notices MUST read the booking's current appointment. No mandatory provider event may be suppressed by FR-032 provider notification preferences.
- REQ-020-022: System MUST send the mandatory `aftercare.provider_reassigned` notice, produced by FR-011, to the patient and the new aftercare provider whenever an admin reassigns an aftercare case, with no admin alert, and MUST send `provider.status_cancellation_admin_support` when a provider-status event leaves an `In Progress` booking open and flagged `supportRequired` for an admin decision; such a booking MUST NOT fire `booking.provider_fault_replacement`.
- REQ-020-023: System MUST allow providers to configure notification preferences (choose which notification types to receive: quote, schedule, treatment start, aftercare, review, promotion/discount notifications).
- REQ-020-152: Every feature that notifies a patient, provider, affiliate or admin MUST send its notices through the Notification Service (S-03), so that channel preferences, throttling, templates and delivery tracking apply to every notice; no feature sends its own notices outside the service.

---

## Appendix: Change Log

| Date       | Version | Changes                                       | Author |
|------------|---------|-----------------------------------------------|--------|
| 2026-11-22 | 2.15 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v2.14) and the change requests (CR-FR020-20261014-01, CR-FR020-20261015-01, CR-FR020-20261015-02, CR-FR020-20261016-01, CR-FR020-20261027-01, CR-FR003-20261027-02 (file change-request-2026-10-27-pre-acceptance-redistribution.md in the FR-003 folder), CR-FR015-20261013-01, CR-FR030-20261015-01, CR-FR030-20261015-02, and the file change-request-2026-08-20-fr037-monitoring-events.md) are in `archived/prd-baseline-2026-11-08/fr020-notifications-alerts/` and in git history. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role           | Name | Date | Signature/Approval |
|----------------|------|------|--------------------|
| Product Owner  | Joachim Trung Tuan | 2026-09-16 | Approved FR-005 quote-outcome and recipient-privacy alignment through v2.1 |
| Product Owner  | Joachim Trung Tuan | 2026-10-18 | Approved FR-020 v2.7 to v2.10 via MTG-002 decision log (documentation only), including CR-FR020-20261016-01 |
| Product Owner  | Joachim Trung Tuan | 2026-10-27 | Approved FR-020 v2.12 (documentation only), including CR-FR020-20261027-01 |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Last Updated**: 2026-11-22
