# FR-020 - Notifications & Alerts

**Module**: S-03: Notification Service
**Feature Branch**: `fr020-notifications-alerts`
**Created**: 2025-11-11
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-020 from local-docs/project-requirements/system-prd.md; Transcriptions (patient/admin/provider references); FR-015 v1.9 provider-status cancellation cascade
**Change Request**: [CR-FR020-20261014-01 — Provider status cancellation cascade](change-request-2026-10-14-provider-status-cancellation-cascade.md)
**Change Request**: [CR-FR020-20261015-01 — Mandatory provider lifecycle events](change-request-2026-10-15-provider-lifecycle-events.md)
**Change Request**: [CR-FR020-20261015-02 — Provider closure request events](change-request-2026-10-15-provider-closure-request-events.md)
**Change Request**: [CR-FR020-20261016-01 — MTG-002 quote model alignment](change-request-2026-10-16-mtg002-quote-model-alignment.md)
**Change Request**: [CR-FR020-20261027-01 — Admin-support alert recipients and provider status email timing](change-request-2026-10-27-admin-support-recipients-status-email-timing.md)

---

## Executive Summary

Provide reliable, configurable notifications (email, push, optional SMS in future phases) for key lifecycle events across patients and providers. Deliver timely alerts, respect user preferences, prevent spam via throttling, and track delivery for operational visibility. MVP supports global Email/Push toggles on the patient app; fine‑grained category preferences follow in V2, and any SMS delivery is explicitly deferred beyond MVP.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (FR-001: Patient Authentication & Profile Management): Receive push/email notifications; manage global Email/Push toggles (MVP) and view notification history (listing specified in FR-020).
- Provider Platform (FR-032: Provider Dashboard Settings & Profile Management / PR-06): Receive notifications for inquiries, quotes, bookings, payments, and messages; manage notification preferences; view notifications via dropdown.
- Admin Platform (FR-030: Notification Rules & Configuration + FR-020 dropdown): Receive notifications for configurable events per FR-030 event catalog; configure default notification policies, SMS enablement, throttling thresholds, and view delivery dashboards; view notifications via dropdown.
- Affiliate Program (if enabled): Receive affiliate payout notifications; configuration is managed via FR-030 event catalog and rules.
- Shared Services (S-03): Unified Notification Service orchestrating channels (email, push, and SMS in future phases) with templates, throttling, and delivery tracking. SMS delivery is not implemented in MVP and is treated as a future enhancement.

### Scope Boundaries

In Scope:

- Notification event types (MVP):
  - **Source of truth**: `FR-030: Notification Rules & Configuration` (Admin-Configurable Notification Event Catalog).
  - The table below mirrors FR-030 for completeness; **if any mismatch exists, FR-030 prevails**.

| Category | Event (Display Name) | Example Backend Event Key | Primary Recipients | Notes |
|----------|-----------------------|---------------------------|--------------------|-------|
| Account/Auth | Email Verification / OTP Code | `account.email_verification_code` | Patient, Provider, Admin | Extends FR-026 OTP templates; **security-critical** and non-disableable by default |
| Account/Auth | Password Reset Code / Link | `account.password_reset` | Patient, Provider, Admin | **Security-critical** and non-disableable by default |
| Account/Auth | New Account Created (Welcome / Onboarding) | `account.created` | Patient | Optional; can be disabled if not needed. Provider onboarding uses `provider.activation` instead |
| Inquiry | Inquiry Submitted (Provider notified) | `inquiry.submitted` | Provider | “New inquiry matching clinic/location” |
| Inquiry | Inquiry Cancelled | `inquiry.cancelled` | Patient, Provider, Admin (optional) | Patient-initiated inquiry cancellation (FR-003 Workflow 5). Fires when patient cancels inquiry in Inquiry, Quoted, or Accepted stages. Patient receives cancellation confirmation (mandatory — aligns with FR-003 Workflow 5 step 4 and Screen 8b). Cancellation reason is patient-private — provider notification says only "Inquiry cancelled by patient". **MVP default channels: Email + Push.** |
| Inquiry | Inquiry Response SLA Breached | `inquiry.ttfq_sla_breached` | Provider | FR-014 REQ-014-113. Fires once per distributed inquiry/provider pair when the provider has not submitted a parent quote within the FR-026 Analytics Configuration TTFQ SLA target (default 120 minutes) from distribution. Recipients: provider users permitted to respond to inquiries (FR-009). Not sent if the inquiry is cancelled, the distribution is withdrawn, or the provider responds first; never repeated for the same pair. MVP default channel: in-app only; email/push off by default and admin-configurable |
| Quote | Quote Submitted / Ready (Patient notified) | `quote.submitted` | Patient | Fired by FR-004 when the provider sends the parent quote; the quote expiry is set and governed by FR-004. The notice shows the "From" price (the lowest subquote price in the parent quote, in the quote currency), the option count, the treatment and the expiry date. Exact subquote prices are not shown before acceptance, and no single quote total exists (see Quote, Booking and Treatment-Change Notifications in Business Rules) |
| Quote | Quote Revised (New Version) | `quote.updated` | Patient, Provider | Fired by FR-004 when a new version of an already-sent parent quote is re-sent to the patient. The notice describes the quote as revised (new version). Drafts that were never sent do not fire this event |
| Quote | Quote Expiring Soon | `quote.expiring_soon` | Patient, Provider | Fired by FR-004 once per sent parent quote when the time left before expiry reaches the quote-expiring-soon lead time set by admin in FR-026. Never fired for drafts or for accepted, withdrawn or cancelled quotes. Admin-configurable |
| Quote | Quote Expired | `quote.expired` | Patient, Provider | Sent on expiry processing completion |
| Quote | Quote Withdrawn | `quote.withdrawn` | Patient, Admin (only when the quote was already accepted) | Fired by FR-004 when a provider withdraws a sent parent quote, before or after acceptance. The patient is always told. Admins receive it as an exception alert only when the withdrawn quote was already accepted; a withdrawal before acceptance is a normal provider action and does not alert admins. After acceptance, FR-006 hands the case to the provider-fault transfer and the patient also receives `booking.provider_fault_replacement`. **Mandatory before and after acceptance — admin cannot disable this event** |
| Quote | Quote Accepted / Subquote Outcomes | `quote.accepted` | Provider | FR-005 uses the existing event with `outcome` = `selected_subquote_accepted`, `sibling_subquote_not_selected`, or `competing_parent_cancelled_other_subquote_accepted`. Selected-provider payloads may include the accepted subquote details, read from the accepted snapshot. A non-selected provider receives only its own parent quote/subquote references, its outcome, and reason; selected provider identity and accepted price are excluded. Each provider receives one notice per sent parent quote: the provider of the accepted parent quote receives `selected_subquote_accepted`, with that parent's sibling subquotes listed in the same notice as `sibling_subquote_not_selected`; each other sent parent quote produces one not-selected notice (`competing_parent_cancelled_other_subquote_accepted`) to its provider, including another parent quote of the selected provider. Unsent drafts cancelled by FR-004 produce no notice. **The selected-provider and not-selected-provider outcomes are mandatory — admin cannot disable them** (see Quote, Booking and Treatment-Change Notifications in Business Rules). The patient is not a recipient: at acceptance the patient receives only `booking.scheduled`. No admin notification is sent for an acceptance |
| Quote | Quote Cancelled (Inquiry Cancelled) | `quote.cancelled_inquiry` | Provider | Sent to each provider whose quote is auto-cancelled due to patient inquiry cancellation (FR-003 Workflow 5). **Provider receipt is mandatory — admin cannot disable this event.** Cancellation reason is patient-private — provider notification says only "Inquiry cancelled by patient". **MVP default channels: Email + Push.** Not subject to FR-032 provider notification preferences; FR-032 offers no toggle for this event. Available template variables: `quote.id`, `quote.provider_id`, `inquiry.id`, `inquiry.cancelled_at`; `inquiry.cancellation_reason` is excluded per privacy rule. |
| Booking/Schedule | Booking Accepted — Slot Held (Pending Payment) | `booking.scheduled` | Patient | Fired by FR-006 when subquote acceptance creates the slot hold, or when an admin-authored replacement acceptance in the FR-006 provider-fault transfer creates the replacement booking, before the first payment is confirmed; states the payment deadline (hold expiry). The provider is not a recipient: the accepted or replacement provider learns of the booking through `quote.accepted` (`selected_subquote_accepted`). **Mandatory — admin cannot disable this event** |
| Booking/Schedule | Hold Expiring Soon (Payment Reminder) | `booking.hold_expiring_soon` | Patient, Admin | Fired by FR-006 once per slot hold when the time left before the hold expires reaches the hold-expiring-soon lead time set by admin in FR-026 and the first payment is still outstanding. Reminds the patient to pay before the slot is released; admins receive it as an exception alert (slot hold expiring while unpaid). Admin-configurable |
| Booking/Schedule | Payment Window Expired | `booking.payment_window_expired` | Patient, Provider, Admin | Fired by FR-006 when the slot hold expires before the first payment (deposit or first instalment) succeeds; applies only to that first payment step. Patient is told the booking lapsed and given the recovery routes (cancel and start a new inquiry, or contact support); provider is told the slot is free; admins receive it as an exception alert. **Mandatory — admin cannot disable this event** |
| Booking/Schedule | Booking Revived | `booking.revived` | Patient, Provider | Fired by FR-006 when an admin revives a booking after Payment Window Expired. Patient receives the new payment deadline; provider is told the slot is held again. **Mandatory — admin cannot disable this event** |
| Booking/Schedule | Provider Unable to Proceed — Replacement Being Arranged | `booking.provider_fault_replacement` | Patient, Admin | Fired by FR-006 when an accepted booking is closed for provider fault: the provider withdraws after acceptance, drops out before treatment starts, or is suspended or deactivated after acceptance and before treatment starts (FR-015). An `In Progress` booking is not closed for provider fault and never fires this event; it stays `In Progress` with `supportRequired` for an admin decision. Tells the patient that an admin will arrange a replacement provider within the same inquiry and that the patient pays no cancellation fee; MUST NOT expose confidential suspension or deactivation reasons. Admins receive it as an exception alert so they can arrange the replacement. Providers are not recipients: the replacement provider learns through `quote.accepted` (`selected_subquote_accepted`) from the replacement acceptance, and the faulted provider is not notified by this event. **Mandatory — admin cannot disable this event** |
| Booking/Schedule | Booking Confirmed | `booking.confirmed` | Patient, Provider | Critical |
| Booking/Schedule | Booking Rescheduled | `booking.rescheduled` | Patient, Provider | Fired by FR-006 when an admin changes the appointment date or time of an `Accepted` or `Confirmed` booking (FR-006 Change Appointment). States the previous and the new appointment, read from the booking's current appointment. **Mandatory — admin cannot disable this event**; not subject to FR-032 provider notification preferences |
| Booking/Schedule | Booking Cancelled | `booking.cancelled` | Patient, Provider, Admin (optional) | Include cancellation reason where appropriate |
| Booking/Schedule | Appointment Reminder | `booking.appointment_reminder` | Patient, Provider | Scheduled reminders; policy-driven |
| Treatment | Treatment Start / Day-1 Starting | `treatment.started` | Patient, Provider | “Treatment start notifications” |
| Treatment | Treatment Details Changed After Acceptance | `treatment.plan_changed` | Patient | Fired by FR-010 when the clinic or an admin makes an audited change to the treatment plan, assigned clinicians or graft count from booking confirmation (`Confirmed`) onward. States what changed; price, currency and other money terms never change through this path. **Mandatory — admin cannot disable this event** |
| Treatment | Treatment Cancelled | `treatment.cancelled` | Patient, Provider, Admin (optional) | Used when treatment is cancelled after scheduling/confirmation |
| Treatment | Treatment Completed (Post‑Op Instructions) | `treatment.completed` | Patient, Provider, Admin (optional) | Completion confirmation; triggers post-op and aftercare next steps |
| Treatment | Treatment Documentation Completed | `treatment.documentation_completed` | Provider | Sent when treatment documentation is successfully saved |
| Treatment | Task In Progress Reminder | `treatment.task_in_progress_reminder` | Provider | Reminder for incomplete treatment tasks or documentation |
| Payment | Payment Received / Receipt | `payment.received` | Patient, Provider, Admin (optional) | Critical |
| Payment | Payment Failed | `payment.failed` | Patient, Admin (optional) | Critical |
| Payment | Payment Due Reminder (Installment / Balance) | `payment.due_reminder` | Patient | “Installment reminder” (split-pay compatible) |
| Billing/Payouts | Provider Payout Processed | `payout.provider_processed` | Provider, Admin (optional) | “They’ve been paid” notification to provider |
| Billing/Payouts | Affiliate Payout Processed | `payout.affiliate_processed` | Affiliate, Admin (optional) | If affiliate program is enabled |
| Billing/Payouts | Payout Failed | `payout.failed` | Admin, Provider (optional), Affiliate (optional) | Failure processing payout; recipients depend on payout type |
| Messaging/Support | New Message Received | `message.received` | Patient, Provider, Admin (optional) | Real-time notification for new messages |
| Messaging/Support | Support Case Created | `support.case_created` | Patient, Provider, Admin | Sent to submitter confirming case creation with case ID; Admin notification if case is urgent or unassigned |
| Messaging/Support | Support Case Assigned | `support.case_assigned` | Admin | Sent to assigned admin when case is assigned to them |
| Messaging/Support | Support Case Status Changed | `support.case_status_changed` | Patient, Provider | Sent when case status changes (Open → In Progress, In Progress → Resolved); includes status update and context |
| Messaging/Support | Support Case Admin Reply | `support.case_admin_reply` | Patient, Provider | Sent when admin replies to case in communication thread; includes message content |
| Messaging/Support | Support Case User Reply | `support.case_user_reply` | Admin | Sent to assigned admin (or all support staff if unassigned) when patient/provider replies to case |
| Messaging/Support | Support Case Resolved | `support.case_resolved` | Patient, Provider | Sent when case is marked as Resolved; includes resolution summary and feedback resolution (if applicable) |
| Messaging/Support | Support Case Reopened | `support.case_reopened` | Patient, Provider, Admin | Sent when closed case is reopened; includes reopening reason |
| Messaging/Support | Support Case Closed | `support.case_closed` | Patient, Provider | Sent when case is closed (final status); includes resolution summary |
| Messaging/Support | Support Case Escalated | `support.case_escalated` | Admin | Sent to escalation recipient (senior admin or technical team) when case is escalated |
| Aftercare | Aftercare Activated | `aftercare.activated` | Patient, Provider | Includes assigned provider/clinician info where applicable |
| Aftercare | Aftercare Milestone Due | `aftercare.milestone_due` | Patient, Provider (optional) | Milestone-driven reminders |
| Aftercare | Scan Due / Missed Scan Reminder | `aftercare.scan_due` / `aftercare.scan_missed` | Patient | “Missed scans MUST trigger reminder notifications” |
| Aftercare | Questionnaire Due / Missed Questionnaire Reminder | `aftercare.questionnaire_due` / `aftercare.questionnaire_missed` | Patient | “Questionnaire due” + reminder if missed |
| Aftercare | Aftercare Escalation / Red Flag Triggered | `aftercare.escalation_triggered` | Provider, Admin, Patient (optional) | Critical; escalation recipients configurable |
| Aftercare | Standalone Aftercare Payment Confirmed | `aftercare.standalone_payment_confirmed` | Patient, Provider (optional), Admin (optional) | Used for standalone aftercare flow payment confirmation |
| Aftercare | Aftercare Provider Reassigned | `aftercare.provider_reassigned` | Patient, Provider (new aftercare provider) | Fired by FR-011 when an admin reassigns an aftercare case to another provider or the Hairline aftercare team, including an `Aftercare` booking reassigned through FR-006 Alternative Flow B6, an `In Progress` booking that the admin moves to `Aftercare` with reassignment, and an FR-011 standalone aftercare case. Tells the patient who now provides aftercare and gives the new provider the case reference; MUST NOT expose confidential suspension or deactivation reasons. No admin alert is sent because the admin is the actor. **Mandatory — admin cannot disable this event**; not subject to FR-032 provider notification preferences |
| Monitoring | Monitoring Case Pending Assignment | `monitoring.assignment_pending` | Admin | Advice-mode hair-loss/transplant-progress monitoring case activated and awaiting provider assignment (FR-037/FR-038) |
| Monitoring | Monitoring Provider Assigned | `monitoring.provider_assigned` | Patient, Provider | Initial assignment or reassignment; assignment type distinguished in payload (FR-037/FR-038) |
| Monitoring | Monitoring Provider Withdrawn | `monitoring.provider_withdrawn` | Admin, Patient | Provider withdraws with reason; case returns to Admin as Pending Reassignment (FR-037/FR-038) |
| Monitoring | Monitoring Provider Reassigned | `monitoring.provider_reassigned` | Patient, Provider | Replacement provider assigned after withdrawal; replacement receives history and next eligible advice date (FR-037/FR-038) |
| Monitoring | Monitoring Advice Posted | `monitoring.advice_posted` | Patient | Provider submits or edits the one advice-window paragraph for the current window (FR-037/FR-038) |
| Monitoring | Monitoring Case Completed | `monitoring.completed` | Patient | Patient completes the active monitoring case (FR-037/FR-038) |
| Monitoring | Monitoring PDF Export Ready | `monitoring.export_ready` | Patient | Date-to-date summary PDF has finished generating and is downloadable (FR-037/FR-038) |
| Monitoring | Monitoring Converted to Inquiry | `monitoring.converted` | Patient | Monitoring case successfully converts into a distinct FR-003 inquiry (FR-037/FR-038) |
| Reviews | Review Request | `review.requested` | Patient | “Review notifications” (typically post-treatment) |
| Reviews | Review Published / New Review Posted | `review.published` | Provider | Notifies provider when a new published review appears on their profile; subject to provider Review Notifications preference in FR-032 |
| Reviews | Provider Response Posted | `review.response_posted` | Patient | Notifies reviewer when provider posts a public response to their review |
| Reviews | Review Removed by Admin | `review.removed_by_admin` | Patient | Notifies reviewer when admin removes their published review for policy/compliance reasons |
| Reviews | Takedown Request Decided | `review.takedown_decided` | Patient | Notifies patient of admin approve/reject decision on their takedown request |
| Promotions/Discounts | Provider Approval Needed for Platform Discount | `promotion.discount_approval_requested` | Provider | “Approval notifications to providers when new platform discount is created” |
| Provider/Compliance | Provider Onboarding Requested | `provider.onboarding_requested` | Admin | New provider onboarding request awaiting review/approval |
| Provider/Compliance | Provider-Caused Cancellation / Offer Unavailable | `provider.status_cancellation_patient` | Patient | FR-015 Alternative Flow A5 / Screen 4. One per affected inquiry/case when provider suspension (`ProviderSuspended`) or deactivation (`ProviderDeactivated`) cancels the patient's case or the provider's offer before acceptance. A cancelled unsent draft quote alone does not trigger this notice, because the patient never saw it. For a case already accepted, the patient instead receives `booking.provider_fault_replacement`. Before acceptance, three variants apply (FR-003 Workflow 2 Alternative Flow B4, REQ-003-021): when other offers remain open, the notice says "[Clinic] is no longer available. Your other offers are still open."; when no other live offer remains and the inquiry is redistributed, the notice says "[Clinic] is no longer available. We are finding new offers for you."; when the patient had explicitly selected the affected provider, the notice asks the patient to confirm the redistribution first. Includes inquiry/case reference and a Contact Admin/Support action. MUST NOT say the patient cancelled, instruct payment against the cancelled selection, or expose confidential suspension/deactivation reasons. **Mandatory** (cannot be disabled in FR-030 rules); sent regardless of FR-015's "Notify Provider" checkbox. MVP channels: Email + Push + in-app (global patient toggles still apply to Email/Push; in-app record always created) |
| Provider/Compliance | Provider-Caused Cancellation — Admin Support Required | `provider.status_cancellation_admin_support` | Admin | Same trigger, and also when a provider-status event leaves an `In Progress` booking open and flagged `supportRequired` for an admin decision (move the booking to `Aftercare` with aftercare reassignment, or cancel it with a reason), or leaves an `Aftercare` booking or FR-011 standalone aftercare case flagged for admin aftercare reassignment (FR-006 Alternative Flow B6). Mandatory admin-support alert per affected inquiry/case with patient, inquiry/case reference, prior stage, cause, and FR-016 deep link (Admin Support Required filter). Sent to admins with the FR-031 Respond to Support permission (default roles Super Admin, Aftercare Specialist, and Support Staff); opening the FR-016 list also requires View Patients. Sent regardless of "Notify Provider"; pinned as critical in the admin dropdown. No FR-034 ticket is auto-created |
| Provider/Compliance | Provider Suspended / Deactivated | `provider.suspended` / `provider.deactivated` | Provider (Owner only) | FR-015 Screen 4. Sent only when "Notify Provider" is checked (default); FR-015 locks it on for deactivations from an FR-032 account-closure request (A7), so `provider.deactivated` is always sent then. For a scheduled change it is sent when the scheduled change is created (with the effective date) and again when it takes effect; with "Notify Provider" unchecked it is sent at neither point. Team members are not emailed; they see the FR-032 Rule 6 banner or login message. Email with action taken, admin-provided reason, effective date (if scheduled), and admin support contact. Unaffected by provider FR-032 category preferences (account notice) |
| Provider/Compliance | Provider Account Activation (Welcome / Set Password) | `provider.activation` | Provider | FR-015 Main Flow step 13 and Alternative Flow A1. Welcome email with platform introduction, login email, first-login instructions, and the one-time set-password link (expires in 24 hours). Re-sent on A1 resend (previous link invalidated). **Mandatory**; cannot be disabled in FR-030 rules. Unaffected by FR-032 category preferences. Email only |
| Provider/Compliance | Owner Login Email Changed | `provider.login_email_changed` | Provider (old and new login address) | FR-015 Screen 3 Tab 1, Owner login email change by an admin. One email to each address. To the old address: the login email for [clinic] was changed to [new address, partly masked] by a Hairline admin on [date/time]; contact support if this was unexpected. To the new address: this address is now the login email for [clinic]. If the Owner's `password_set` is false, `provider.activation` is also sent to the new address. **Mandatory** security notice; cannot be disabled in FR-030 rules or by FR-032 category preferences. Email only |
| Provider/Compliance | Provider Reactivated | `provider.reactivated` | Provider (Owner only) | FR-015 Alternative Flow A6 / Screen 5. Sent only when "Notify Provider" is checked (default). Email with reactivation notice, admin-provided reason, and admin support contact; notes that cancelled cases are not restored and, if a scheduled change the provider was notified of was cancelled by the reactivation, that it no longer applies. **Mandatory** in FR-030 rules when triggered. Unaffected by FR-032 category preferences (account notice) |
| Provider/Compliance | Scheduled Status Change Cancelled | `provider.scheduled_change_cancelled` | Provider (Owner only) | FR-015 Screen 4 (Cancel Scheduled Change). Sent when an admin cancels a pending scheduled suspension/deactivation and the scheduled change had "Notify Provider" checked. Email states which change was cancelled and its former effective date. When a reactivation cancels the scheduled change automatically, the note is included in `provider.reactivated` instead. **Mandatory** in FR-030 rules when triggered. Unaffected by FR-032 category preferences (account notice) |
| Provider/Compliance | Provider Account-Closure Requested | `provider.closure_requested` | Admin | FR-032 Request Account Closure (step 10) / FR-015 A7. Sent to admins with View Providers permission when a provider submits a closure request. Includes provider and clinic name, request date, optional reason, and a deep link to the request in the FR-015 provider profile (Closure Requested filter). **Mandatory**; cannot be disabled in FR-030 rules. Email + in-app |
| Provider/Compliance | Provider Account-Closure Request Rejected | `provider.closure_rejected` | Provider | FR-015 A7 step 6 / FR-032 step 16. Sent when an admin rejects a closure request. Email states that the account stays Active, gives the admin review notes, and the admin support contact. **Mandatory**; cannot be disabled in FR-030 rules. Unaffected by FR-032 category preferences (account notice). Email only |
| Provider/Compliance | Provider Document Expiration Warning | `provider.document_expiration_warning` | Admin, Provider (optional) | License/credential expiry warnings; timing is policy-driven |
| System/Operations | System Escalation | `system.escalation` | Admin | Operational escalation events requiring admin action |
| System/Operations | System Alert | `system.alert` | Admin | System health/monitoring alerts surfaced via notifications |
| System/Operations | Analytics Export Ready | `analytics.export_ready` | Provider | FR-014 REQ-014-062/063. A one-off or scheduled provider analytics export (PDF or CSV) has finished generating. Sent to the provider's registered email and each selected recipient; email carries the PDF attachment where applicable plus a secure download link that expires after 48 hours; in-app notification links to Report History. Default channels: email + in-app |

- Channels: email, push; SMS is an optional/configurable channel for urgent events in the target architecture but is **not available in MVP** (no SMS notifications are sent until a later phase explicitly enables this capability).
- User preferences (MVP):
  - **Patients**: global Email/Push toggles (managed in FR-001: Patient Authentication & Profile Management, Settings → Notifications section); per‑category preferences deferred to V2 (not in scope).
  - **Providers**: can choose which notification types to receive (quote notifications, schedule notifications, treatment start notifications, aftercare notifications, review notifications, promotion/discount notifications) via notification preferences settings (managed in PR-06: Profile & Settings Management, Settings → Notifications section).
- Notification listing screens: patient notification history screen (full listing page), provider notification dropdown (infinite scroll), admin notification dropdown (infinite scroll).
- Throttling/de‑duplication and delivery tracking.

Out of Scope:

- In‑app messaging content design (covered in FR-012).
- Per‑category user preferences on patient app (explicitly V2).
- Quote Declined (`quote.declined`): Post-MVP and hidden, as in the FR-030 Post-MVP / Hidden Events list. It is reserved for an explicit governed decline flow; no MVP producer exists because patients have no explicit decline action (FR-005). FR-005 sibling Not Selected and competing-parent cancellation outcomes do not use this event.

### Entry Points

- System events published by core modules (inquiry, quote, booking, payment, chat, scheduling, aftercare) trigger notifications via S-03.
- Users access Settings → Notifications to set global Email/Push toggles (MVP).

---

## Business Workflows

### Main Flow: Event → Notification Dispatch

Actors: System, Notification Service, Recipient
Trigger: Business event occurs (e.g., booking confirmed)
Outcome: Recipient receives notification according to channel preferences

Steps:

1. Event emitted with payload (type, actor, subject, recipient id).
2. Notification Service evaluates preferences and throttling.
3. Builds message from template and routes to enabled channels.
4. Records delivery attempt and status; exposes audit.
5. (If SMS enabled and urgent) include SMS path; else email/push only.

### Alternative Flows

- A1: Preference Disabled
  - Trigger: Recipient has disabled Email or Push.
  - Outcome: Channel suppressed; delivery attempted on remaining enabled channels.

- B1: Throttling
  - Trigger: Excessive events in short time window.
  - Outcome: Coalesce or defer per policy; record suppression in audit.

- B2: Channel Failure
  - Trigger: Email/push/SMS provider unavailable.
  - Outcome: Retry with backoff; failover when configured; status reflects failure cause.

---

## Screen Specifications

### Patient Platform Screens

Notification settings UI for patients is defined in `FR-001: Patient Authentication & Profile Management` (Settings → Notifications). FR-020 relies on that screen; it is not re-specified here to avoid duplication.

#### Screen 1: Patient – Notification Listing

Purpose: Display notification history for patients to view all received notifications.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       |
|-------------------|--------|----------|-----------------------------|------------------------|
| Notification List | list   | Yes      | Chronological list of notifications | Paginated, 20 per page |
| Notification Type | badge  | Yes      | Type indicator (quote, booking, payment, etc.) | Read-only |
| Title             | text   | Yes      | Notification title/subject  | Read-only |
| Message           | text   | Yes      | Notification body content   | Read-only, truncated with "Read more" |
| Timestamp         | datetime | Yes    | When notification was sent  | Read-only, relative time |
| Read Status       | badge  | Yes      | Read/Unread indicator       | Toggle on click |
| Action Button     | button | No       | Deep link to related content | Context-dependent |

Business Rules:

- Notifications sorted by most recent first (newest at top).
- Unread notifications highlighted with visual indicator.
- Clicking notification marks as read and navigates to related content (if applicable).
- Filter options: All, Unread, By Type (Inquiry, Quote, Booking, Payment, Treatment, Aftercare, Account, Messaging).
- Search functionality: search by notification content.

---

### Provider Platform Screens

#### Screen 2: Provider – Notification Dropdown

Purpose: Display notifications in provider dashboard header dropdown with infinite scroll.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       |
|-------------------|--------|----------|-----------------------------|------------------------|
| Notification Count | badge | Yes      | Unread notification count   | Real-time update |
| Notification Items | list   | Yes      | Infinite scroll list of notifications | Load more on scroll |
| Notification Type | badge  | Yes      | Type indicator              | Read-only |
| Title             | text   | Yes      | Notification title          | Read-only, truncated |
| Message           | text   | No       | Notification body content   | Read-only, truncated |
| Timestamp         | datetime | Yes    | When notification was sent  | Read-only, relative time |
| Read Status       | indicator | Yes    | Read/Unread dot             | Visual indicator |
| Load More Trigger | scroll | Yes      | Infinite scroll trigger     | Loads next batch on scroll |

Business Rules:

- Dropdown shows notifications with infinite scroll (loads 20 notifications per batch).
- Notifications sorted by most recent first (newest at top).
- Unread count badge updates in real-time.
- Clicking notification marks as read and navigates to related content.
- Infinite scroll loads more notifications as user scrolls down.
- Filter options within dropdown: All, Unread, By Type (Quote, Booking, Payment, etc.).
- Search functionality: search by notification content within dropdown.

---

Provider notification settings UI is defined in `FR-032: Provider Dashboard Settings & Profile Management (PR-06)` under Settings → Notifications. FR-020 consumes those preferences; the screen itself is not re-specified here.

---

### Admin Platform Screens

#### Screen 3: Admin – Notification Dropdown

Purpose: Display notifications in admin dashboard header dropdown with infinite scroll.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       |
|-------------------|--------|----------|-----------------------------|------------------------|
| Notification Count | badge | Yes      | Unread notification count   | Real-time update |
| Notification Items | list   | Yes      | Infinite scroll list of notifications | Load more on scroll |
| Notification Type | badge  | Yes      | Type indicator (critical, warning, info) | Read-only, color-coded |
| Title             | text   | Yes      | Notification title          | Read-only, truncated |
| Message           | text   | No       | Notification body content   | Read-only, truncated |
| Timestamp         | datetime | Yes    | When notification was sent  | Read-only, relative time |
| Read Status       | indicator | Yes    | Read/Unread dot             | Visual indicator |
| Priority Indicator | badge | No       | Critical/High priority badge | For urgent items |
| Load More Trigger | scroll | Yes      | Infinite scroll trigger     | Loads next batch on scroll |

Business Rules:

- Dropdown shows notifications with infinite scroll (loads 20 notifications per batch).
- Notifications sorted by most recent first (newest at top).
- Critical notifications highlighted with red badge and always shown at top (before non-critical).
- Unread count badge updates in real-time.
- Clicking notification marks as read and navigates to related content.
- Infinite scroll loads more notifications as user scrolls down.
- Filter options within dropdown: All, Unread, Critical, By Type (Payment, Aftercare, Booking, Support, etc.).
- Search functionality: search by notification content within dropdown.

---

Notification policy, throttling, and delivery monitoring UI live in `FR-030: Notification Rules & Configuration` (including template editor; OTP templates in `FR-026`). FR-020 depends on those capabilities and does not re-specify the admin screen.

---

### Consolidated Screen Notes

- Patient – Notification Listing: Patient App → Notifications (dedicated tab or menu item); notifications persist for 90 days then archive.
- Provider – Notification Dropdown: Provider dashboard header bell icon; real-time updates (WebSocket or polling); infinite scroll within dropdown at max height.
- Admin – Notification Dropdown: Admin dashboard header bell icon; real-time updates (WebSocket or polling); infinite scroll within dropdown at max height; critical items pinned above non-critical.
- Patient notification settings: Owned by `FR-001: Patient Authentication & Profile Management` (Settings → Notifications).
- Provider notification settings: Owned by `FR-032: Provider Dashboard Settings & Profile Management (PR-06)` (Settings → Notifications).
- Admin policy/config screens: Owned by `FR-030: Notification Rules & Configuration` (template editor) and `FR-026: App Settings & Security Policies` (OTP templates).

## Success Criteria

- SC-001: 95% of eligible events generate a notification without violating platform performance NFRs (API p95 < 500ms, p99 < 1000ms), and users typically see notifications within ~2 seconds under normal load.
- SC-002: 99% of notifications respect user global Email/Push preferences.
- SC-003: Throttling reduces duplicate notifications by ≥ 90% during spikes.
- SC-004: Delivery status recorded for 100% of attempts.
- SC-005: Notification Settings loads in ≤ 1 second (p95).

---

## Business Rules

- **Patient Preferences**: Global Email/Push toggles available to patients in MVP (managed in FR-001: Patient Authentication & Profile Management, Settings → Notifications); category preferences deferred to V2.
- **Provider Preferences**: Providers can choose which notification types to receive (quote notifications, schedule notifications, treatment start notifications, aftercare notifications, review notifications, promotion/discount notifications) via notification preferences settings (managed in FR-032: Provider Dashboard Settings & Profile Management, Settings → Notifications section). Every event that is mandatory for providers (`quote.cancelled_inquiry`, the selected-provider and not-selected-provider outcomes of `quote.accepted`, `booking.payment_window_expired`, `booking.revived` and `booking.rescheduled`) is delivered regardless of these preferences.
- **Admin Notifications**: Admin recipients and event coverage are defined by the FR-030 event catalog and configured rules (no additional hard-coded admin event list in FR-020).
- **Provider-Status Cancellation Notifications (FR-015 A5)**: `provider.status_cancellation_patient` and `provider.status_cancellation_admin_support` are mandatory and independent of FR-015's "Notify Provider" checkbox. Delivery failures retry per Flow B2 without duplicates: de-duplicate on provider-status event + affected record + recipient, and never restore cancelled records. Patient content uses provider-caused wording, a Contact Admin/Support action, no payment instruction, and no confidential suspension/deactivation reason. Before acceptance, the patient notice has three variants from FR-003 Workflow 2 Alternative Flow B4 and REQ-003-021: "[Clinic] is no longer available. Your other offers are still open." when other offers remain open; "[Clinic] is no longer available. We are finding new offers for you." when no other live offer remains and the inquiry is redistributed, and a request to confirm redistribution first when the patient had explicitly selected the affected provider ([CR-FR003-20261027-02](../fr003-inquiry-submission/change-request-2026-10-27-pre-acceptance-redistribution.md)). SMS remains future.
- **Aftercare Provider Reassignment Notice (FR-011)**: `aftercare.provider_reassigned` is produced only by FR-011 when an admin reassigns an aftercare case, including cases reassigned after an FR-015 provider-status event. It goes to the patient and the new aftercare provider, is mandatory, cannot be disabled in FR-030 rules, and is not subject to FR-032 provider notification preferences. No admin alert is sent because the admin performs the reassignment.
- **Provider Lifecycle Notifications (FR-015)**: `provider.activation` is mandatory and cannot be disabled, because without it a new provider cannot set a password. `provider.suspended`, `provider.deactivated`, `provider.reactivated`, and `provider.scheduled_change_cancelled` go to the provider Owner only, follow FR-015's "Notify Provider" choice and, when triggered, cannot be disabled in FR-030 rules or by FR-032 category preferences. For a scheduled suspension or deactivation, `provider.suspended` / `provider.deactivated` is sent when the change is created and again when it takes effect. `provider.status_cancellation_admin_support` goes to admins with the FR-031 Respond to Support permission ([CR-FR020-20261027-01](change-request-2026-10-27-admin-support-recipients-status-email-timing.md)). See [CR-FR020-20261015-01](change-request-2026-10-15-provider-lifecycle-events.md). Account-closure requests add `provider.closure_requested` (admins) and `provider.closure_rejected` (provider); both are mandatory, and a closure deactivation always sends `provider.deactivated` because FR-015 locks "Notify Provider" on. See [CR-FR020-20261015-02](change-request-2026-10-15-provider-closure-request-events.md). An admin change of the Owner login email sends the mandatory security notice `provider.login_email_changed` to the old and the new address.
- **FR-005 Quote Outcome Privacy**: `quote.accepted` carries an explicit `outcome` code and recipient scope. Payload rendering MUST use an allowlist per recipient; non-selected providers MUST NOT receive the selected provider identity, accepted price, or another provider's quote/subquote identifiers.
- **Quote, Booking and Treatment-Change Notifications** (mirrors the FR-030 Quote, Booking and Treatment-Change Event Rules; FR-030 prevails on any mismatch):
  - **Producers**: FR-004 produces `quote.submitted`, `quote.updated`, `quote.expiring_soon`, `quote.expired` and `quote.withdrawn`. FR-005 produces `quote.accepted` and its outcomes. FR-006 produces `booking.scheduled`, `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.rescheduled` and `booking.provider_fault_replacement`. FR-010 produces `treatment.plan_changed`. Admin sets the quote-expiring-soon and hold-expiring-soon lead times in FR-026.
  - **Recipient grain for `quote.accepted`**: one provider notice per sent parent quote, never one per subquote. The de-duplication key is acceptance record + parent quote + recipient. The recipient matrix below shows each population.
  - **Unsent drafts**: when FR-004 cancels an unsent draft parent quote as `cancelled_other_accepted` because another subquote was accepted, no notification is sent to the drafting provider or anyone else. Only sent parent quotes receive acceptance outcomes.
  - **Pre-acceptance price variables**: `quote.submitted`, `quote.updated`, `quote.expiring_soon`, `quote.expired` and `quote.withdrawn` may use only parent-level variables: the "From" price (lowest subquote price in the parent quote) with its currency, option count, treatment, expiry date, provider name and the parent quote reference. A single quote total does not exist and MUST NOT be offered as a variable.
  - **Post-acceptance money variables**: on `quote.accepted` (selected-provider outcome) and on every `booking.*` event, price, currency, date range and promotion variables resolve from the accepted snapshot recorded at acceptance, never from the live parent quote, Quote Option or package. Appointment variables on `booking.*` events resolve from the booking's current appointment, which an admin may change through FR-006; the snapshot keeps the accepted appointment as the baseline. `booking.rescheduled` carries both the previous and the new appointment.
  - **Treatment-detail variables**: `treatment.plan_changed` and other treatment events may use the current treatment plan, clinicians and graft count maintained through FR-010; they MUST NOT carry changed money values.
  - **Locks**: `quote.withdrawn`, the selected-provider and not-selected-provider outcomes of `quote.accepted`, `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement`, `booking.scheduled`, `booking.rescheduled` and `treatment.plan_changed` are mandatory and cannot be disabled in FR-030 rules. `quote.expiring_soon` and `booking.hold_expiring_soon` are admin-configurable. No mandatory provider event (`quote.cancelled_inquiry`, the selected-provider and not-selected-provider outcomes of `quote.accepted`, `booking.payment_window_expired`, `booking.revived` and `booking.rescheduled`) is subject to FR-032 provider notification preferences.
  - **Acceptance recipients**: at acceptance the patient receives only `booking.scheduled`; `quote.accepted` goes to providers only (the accepted provider and each not-selected provider). No admin notification is sent for an acceptance. The same applies to an admin-authored replacement acceptance in the FR-006 provider-fault transfer: the patient receives `booking.scheduled` with the replacement payment deadline, and the replacement provider receives `quote.accepted` (`selected_subquote_accepted`).
  - **Admin exception alerts**: admins are alerted only for exceptions on the quote-to-booking path: a slot hold expiring while the first payment is unpaid (`booking.hold_expiring_soon`), Payment Window Expired (`booking.payment_window_expired`), provider fault (`booking.provider_fault_replacement`) and a provider withdrawing a quote that was already accepted (`quote.withdrawn`). Routine acceptances are visible on admin dashboards only.
  - **Payment window scope**: `booking.payment_window_expired` covers only the first payment step (deposit or first instalment).

**`quote.accepted` recipient matrix** (example: provider P has sent parent quotes A and B, and the patient accepts one subquote in A):

| Population | Provider notice | Outcome | Payload allowlist |
|---|---|---|---|
| Accepted subquote in parent A | One notice to P for parent A (mandatory) | `selected_subquote_accepted` | Accepted subquote details from the accepted snapshot |
| Other subquotes in parent A (siblings) | No separate notice; listed inside P's parent A notice | `sibling_subquote_not_selected` | P's own parent A subquote references and outcome |
| Other sent parent quote of the same provider (parent B) | One separate notice to P for parent B (mandatory) | `competing_parent_cancelled_other_subquote_accepted` | Parent B quote and subquote references, outcome and reason |
| Sent parent quote of any other provider | One notice per parent quote to that provider (mandatory) | `competing_parent_cancelled_other_subquote_accepted` | That provider's own parent quote and subquote references, outcome and reason; no selected provider identity and no accepted price |
| Unsent draft parent quote of any provider | No notice (draft cancelled silently by FR-004) | None | None |

The patient receives no `quote.accepted` notice; at acceptance the patient receives only `booking.scheduled` (Booking Accepted — Slot Held (Pending Payment)) and never receives sibling or competing outcomes. Admins receive no acceptance notice.

- One notification record per attempt with channel, provider, status, and timestamp.
- Throttling and suppression policies are transparent in audit logs.
- **Notification Content Management**: Notification content (titles, messages, templates) is managed in FR-030: Notification Rules & Configuration via the Notification Template Editor.
- **Email Template Management**:
  - General notification email templates: Managed in FR-030 (Notification Rules & Configuration) with support for dynamic variables, multi-language content, rich text formatting, and preview capabilities.
  - OTP email templates (verification, password reset): Managed in FR-026 (App Settings & Security Policies) as part of authentication settings.

### Admin Editability

Editable by Admin:

- Throttling thresholds, SMS enablement, default channel policies, templates.

Fixed in Codebase (Not Editable):

- Supported channels (Email/Push; SMS behind config), baseline event types per FR-030 event catalog.

Configurable with Restrictions:

- Maximum SMS volume, high‑priority categories allowed for SMS.

---

## Dependencies

- **FR-001**: Patient Authentication & Profile Management (patient notification preferences UI in Settings → Notifications).
- **FR-012**: Messaging (message received events).
- **FR-004**: Quote Submission & Management (producer of `quote.submitted`, `quote.updated`, `quote.expiring_soon`, `quote.expired` and `quote.withdrawn`; cancels unsent drafts silently on acceptance).
- **FR-005**: Quote Comparison & Acceptance (accepted subquote, sibling Not Selected, and competing-parent cancellation outcome/privacy contract; accepted snapshot used for post-acceptance money variables).
- **FR-006**: Booking & Scheduling (producer of `booking.scheduled`, `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.rescheduled` and `booking.provider_fault_replacement`).
- **FR-010**: Treatment Execution & Documentation (producer of `treatment.plan_changed` for audited treatment-detail changes from booking confirmation onward).
- **FR-026**: App Settings & Security Policies (OTP email templates for verification and password reset; quote-expiring-soon and hold-expiring-soon lead times).
- **FR-015**: Provider Management (provider activation email and resend, suspension/deactivation cascade, reactivation, scheduled status change cancellation, Owner login email change notice; Main Flow step 13, Alternative Flows A1, A5, A6, Screens 4–5, "Notify Provider" option).
- **FR-016**: Admin Patient Management (Admin Support Required filter and resolution target of the admin-support alert).
- **FR-030**: Notification Rules & Configuration (notification template management, template editor, notification rule configuration).
- **FR-032**: Provider Dashboard Settings & Profile Management (PR-06; provider notification preferences UI).
- **FR-037**/**FR-038**: Monitor Your Hair Loss / Monitor Your Transplant Progress (monitoring assignment, advice, withdrawal, reassignment, completion, export, and conversion events).
- P-02/P-03/P-05 events for inquiry/quote/booking/aftercare milestones.
- S-03 Notification Service; Email/Push/SMS providers via configured adapters.

---

## Assumptions

- Users understand global Email/Push toggles; granular controls to be introduced later.
- SMS costs are controlled via caps; only urgent categories use SMS.

---

## Implementation Notes

- Event-driven design; idempotent handlers; retries with backoff.
- Delivery provider abstraction; per-channel template library.
- Privacy: no sensitive content in notifications; deep links use secure tokens.
- **Notification Content Management**: Notification templates (email, push, SMS) are managed in FR-030: Notification Rules & Configuration via the Notification Template Editor, which supports dynamic variables, multi-language content, rich text formatting (email), and preview capabilities.
- **Email Template Management**:
  - General notification email templates: Managed in FR-030 (Notification Rules & Configuration) - admins can create/edit templates per event type and channel with variable substitution, multi-language support, and preview.
  - OTP email templates: Managed separately in FR-026 (App Settings & Security Policies) for email verification and password reset flows.
- **Notification Preferences**:
  - Patient preferences: Managed in FR-001 (Patient Authentication & Profile Management) under Settings → Notifications screen.
  - Provider preferences: Managed in FR-032 (Provider Dashboard Settings & Profile Management) under Settings → Notifications section (providers can toggle individual notification types on/off: quote notifications, schedule notifications, treatment start notifications, aftercare notifications, review notifications, promotion/discount notifications).

---

## User Scenarios & Testing

### User Story 1 – Patient toggles preferences (P1)

Why: Respect user choice on communication channels.

Independent Test: Disable Email and verify only Push is delivered for eligible events.

Acceptance Scenarios:

1. Given Email is disabled, when an event fires, then no email is sent and push is delivered (if enabled).
2. Given both Email and Push disabled, when an event fires, then no notification is sent and suppression is logged.

### User Story 2 – Admin enables SMS for urgent events (P2)

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

1. Given patient cancels inquiry with 2 active quotes, when cancellation completes, then patient receives `inquiry.cancelled` notification via both email and push within 5 minutes confirming cancellation with reason visible.
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
- REQ-020-003: System MUST support optional/configurable SMS for urgent events.
- REQ-020-004: System MUST allow patients to configure notification preferences (MVP: global Email/Push toggles managed in FR-001: Patient Authentication & Profile Management).
- REQ-020-004B: System MUST allow providers to configure notification preferences (choose which notification types to receive: quote, schedule, treatment start, aftercare, review, promotion/discount notifications).
- REQ-020-005: System MUST support notification event types in the FR-030 MVP event catalog (Admin-Configurable Notification Event Types), routed to enabled channels and templates.
- REQ-020-006: System MUST throttle notifications to prevent spam and log suppression.
- REQ-020-007: System MUST track and expose delivery status per attempt.
- REQ-020-008: System MUST provide notification listing screen for patients to view notification history (paginated, 20 per page).
- REQ-020-009: System MUST provide notification dropdown in provider dashboard header with infinite scroll (loads 20 notifications per batch, no separate listing screen).
- REQ-020-010: System MUST provide notification dropdown in admin dashboard header with infinite scroll (loads 20 notifications per batch, no separate listing screen).
- REQ-020-011: System MUST send notifications to admins for any enabled FR-030 event types where Admin is a primary or optional recipient (per rule configuration).
- REQ-020-012: System MUST route FR-005 acceptance outcomes through `quote.accepted` with an explicit `outcome` code and recipient-scoped payload, sending one provider notice per sent parent quote (de-duplicated on acceptance record + parent quote + recipient) and no notice for unsent drafts; the selected-provider and not-selected-provider outcomes MUST NOT be disableable. Non-selected providers MUST receive only their own outcome context and MUST NOT receive the selected provider identity or accepted price; `quote.declined` MUST NOT represent FR-005 system-generated sibling or competing-parent outcomes.
- REQ-020-013: System MUST send mandatory `provider.status_cancellation_patient` and `provider.status_cancellation_admin_support` notifications for each record affected by an FR-015 provider suspension/deactivation, regardless of the "Notify Provider" checkbox, with privacy-safe patient content (no patient-cancelled wording, no payment instruction, no confidential reason), and MUST use the FR-003 pre-acceptance variants (Workflow 2 Alternative Flow B4, REQ-003-021): "[Clinic] is no longer available. Your other offers are still open." when other offers remain open; "[Clinic] is no longer available. We are finding new offers for you." when the inquiry is redistributed, or a confirmation request first when the patient had explicitly selected the affected provider.
- REQ-020-014: System MUST retry failed provider-status notifications without duplicates per provider-status event + affected record + recipient, and MUST send `provider.suspended` / `provider.deactivated` email to the provider Owner only when "Notify Provider" is checked; for a scheduled change, the email MUST be sent when the change is created and again when it takes effect. `provider.status_cancellation_admin_support` MUST go to admins with the FR-031 Respond to Support permission, and `provider.reactivated` and `provider.scheduled_change_cancelled` MUST go to the provider Owner only.
- REQ-020-015: System MUST always send `provider.activation` (non-disableable) when FR-015 creates a provider or a resend is requested, and MUST send `provider.reactivated` and `provider.scheduled_change_cancelled` to the provider when FR-015's "Notify Provider" applies; these events MUST NOT be suppressed by FR-030 toggles or FR-032 category preferences. System MUST always send `provider.login_email_changed` to the old and the new address when an admin changes the Owner login email in FR-015.
- REQ-020-016: System MUST send `provider.closure_requested` to admins when a provider submits an FR-032 account-closure request and `provider.closure_rejected` to the provider when an admin rejects it, and MUST always send `provider.deactivated` for a deactivation that processes a closure request; these events MUST NOT be suppressed by FR-030 toggles or FR-032 category preferences.
- REQ-020-017: System MUST send `quote.withdrawn` (before and after acceptance), `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement` and `treatment.plan_changed` as mandatory notifications that FR-030 toggles cannot disable, and MUST send `quote.expiring_soon` and `booking.hold_expiring_soon` at the FR-026 lead times when enabled in FR-030.
- REQ-020-018: System MUST render pre-acceptance quote notifications with parent-level variables only ("From" price with currency, option count, treatment, expiry) and no single quote total, MUST resolve post-acceptance money variables (price, currency, date range, appointment, promotion) from the accepted snapshot, and MUST NOT carry changed money values in treatment events.
- REQ-020-019: At acceptance, System MUST send the patient only `booking.scheduled` and no `quote.accepted` notice, MUST send `quote.accepted` only to the accepted provider and the not-selected providers, and MUST NOT send an admin notification for the acceptance. Admins MUST be alerted only for the exceptions `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.provider_fault_replacement` and `quote.withdrawn` when the withdrawn quote was already accepted; `quote.withdrawn` MUST always reach the patient and MUST NOT alert admins for a withdrawal before acceptance.
- REQ-020-020: System MUST always send `quote.cancelled_inquiry` to each provider whose quote is auto-cancelled by an inquiry cancellation; neither FR-030 toggles nor FR-032 provider notification preferences may suppress it.
- REQ-020-021: System MUST send `booking.scheduled` to the patient only, as a mandatory event, both when the patient accepts a subquote and when an admin-authored replacement acceptance creates a replacement booking. System MUST send the mandatory `booking.rescheduled` to the patient and the provider when an admin changes the appointment, with the previous and the new appointment. Booking notices MUST read the booking's current appointment. No mandatory provider event may be suppressed by FR-032 provider notification preferences.
- REQ-020-022: System MUST send the mandatory `aftercare.provider_reassigned` notice, produced by FR-011, to the patient and the new aftercare provider whenever an admin reassigns an aftercare case, with no admin alert, and MUST send `provider.status_cancellation_admin_support` when a provider-status event leaves an `In Progress` booking open and flagged `supportRequired` for an admin decision; such a booking MUST NOT fire `booking.provider_fault_replacement`.

---

## Key Entities

- **NotificationEvent**: type, subject, recipient, outcome, recipientScope, payloadMetadata, createdAt. FR-005 `quote.accepted` events use recipient-scoped allowlists for selected and non-selected outcomes and are de-duplicated on acceptance record + parent quote + recipient.
- **NotificationAttempt**: channel, provider, status, timestamp, error, correlationId.
- **PatientPreference**: userId, emailEnabled, pushEnabled, updatedAt (MVP scope; managed in FR-001).
- **ProviderPreference**: providerId, quoteNotification, scheduleNotification, startTreatmentNotification, afterCareNotification, reviewNotification, promotionDiscountNotification, updatedAt (allows providers to choose which notification types to receive).
- **NotificationRecord**: notificationId, recipientId, recipientType (patient/provider/admin), type, title, message, readStatus, createdAt, readAt (for notification listing screens).

---

## Appendix: Change Log

| Date       | Version | Changes                                       | Author |
|------------|---------|-----------------------------------------------|--------|
| 2025-11-11 | 1.0     | Initial PRD creation (MVP scope)             | AI     |
| 2025-11-16 | 1.1     | Added admin notifications, additional notification types (payment reminder, task in progress, aftercare standalone, cancellation), notification listing screens (patient, provider dropdown, admin dropdown), clarified notification preference management (FR-001 for patients, provider preferences), clarified notification content and email template management (FR-030, FR-026) | AI     |
| 2025-12-05 | 1.2     | Removed duplicate screen specs (patient settings, provider settings, admin policy) now referenced to their owning FRs (FR-001, PR-06, FR-030/FR-026) | AI     |
| 2025-12-05 | 1.3     | Renumbered screens, consolidated screen notes, and referenced exact FRs (FR-001, FR-032/PR-06, FR-030, FR-026) | AI     |
| 2026-01-16 | 1.4     | Aligned FR-020 notification event types to match FR-030 MVP event catalog; designated FR-030 as source of truth for event coverage | AI     |
| 2026-02-05 | 1.5     | Cancel Inquiry flow (FR-003 Workflow 5): Updated `inquiry.cancelled` event notes to reflect patient-initiated cancellation; added new `quote.cancelled_inquiry` event for quote cascade notifications; added content guideline that cancellation reason is patient-private | AI     |
| 2026-02-09 | 1.6     | Cancellation integrity fixes: Promoted Patient from optional to primary recipient on `inquiry.cancelled` (aligns with FR-003 Workflow 5 mandatory confirmation). Added MVP default channel notes (Email + Push) to both cancellation events. Expanded Screen 1 filter types to enumerate all categories explicitly. Added User Story 4 (cancellation notification delivery with privacy scenarios). Fixed Last Updated date. | AI     |
| 2026-02-10 | 1.7     | FR-003 verification fixes: Updated stale "Screen 11a" reference to "Screen 8b" in `inquiry.cancelled` event notes (FR-003 v1.6 renumbering). Aligned cancellation notification SLA from "within 2 seconds" to "within 5 minutes" to match FR-003 Workflow 5 step 4. | AI     |
| 2026-05-14 | 1.8     | Added three missing review notification events to the event catalog: `review.response_posted` (patient notified when provider responds), `review.removed_by_admin` (patient notified when admin removes review), `review.takedown_decided` (patient notified of takedown approve/reject decision). Required by FR-013 REQ-013-016. | Verification alignment (2026-05-14) |
| 2026-05-14 | 1.9     | Added provider-facing `review.published` event for new published reviews and aligned provider notification preference wording/entity with FR-032 Review Notifications. | Verification alignment (2026-05-14) |
| 2026-08-20 | 2.0     | Added Monitoring category (8 `monitoring.*` events: assignment_pending, provider_assigned, provider_withdrawn, provider_reassigned, advice_posted, completed, export_ready, converted) to the event catalog and FR-037/FR-038 as dependencies, mirroring FR-030's source-of-truth catalog. See [Change Request](./change-request-2026-08-20-fr037-monitoring-events.md) | Verification alignment (2026-08-20) |
| 2026-09-16 | 2.1     | Extended the existing `quote.accepted` event with FR-005 recipient-scoped outcome codes and privacy allowlists; reserved `quote.declined` for explicit decline flows so sibling Not Selected and competing-parent cancellation remain distinct. Aligned with FR-030 v1.6. | Product Owner / Verification alignment |
| 2026-10-13 | 2.2     | Mirrored FR-030 catalog entry `inquiry.ttfq_sla_breached` (Inquiry, Provider) for the FR-014 TTFQ SLA-breach alert (REQ-014-113); in-app default | Claude Code |
| 2026-10-14 | 2.3     | Mirrored FR-030 catalog entry `analytics.export_ready` (System/Operations, Provider) for FR-014 Screen 6 export delivery | AI Assistant |
| 2026-10-14 | 2.4     | Aligned provider suspension/deactivation cancellation cascade per CR-FR015-20261013-01 and FR-015 v1.9. See [Change Request](./change-request-2026-10-14-provider-status-cancellation-cascade.md) | Vân Tay Media |
| 2026-10-15 | 2.5     | FR-015 v1.14 alignment: added mandatory provider events `provider.activation` (cannot be disabled), `provider.reactivated`, and `provider.scheduled_change_cancelled`; `account.created` now Patient only; added Provider Lifecycle Notifications rule and REQ-020-015; expanded FR-015 dependency. Mirrored in FR-030 v1.10 (CR-FR030-20261015-01). See [Change Request](./change-request-2026-10-15-provider-lifecycle-events.md) | Claude |
| 2026-10-15 | 2.6     | FR-015 v1.16 alignment: added mandatory events `provider.closure_requested` (Admin) and `provider.closure_rejected` (Provider); `provider.deactivated` always sent for closure deactivations (Notify Provider locked on); extended Provider Lifecycle Notifications rule; added REQ-020-016. Mirrored in FR-030 v1.11 (CR-FR030-20261015-02). See [Change Request](./change-request-2026-10-15-provider-closure-request-events.md) | Claude |
| 2026-10-16 | 2.7     | MTG-002 quote model alignment, mirroring FR-030 v1.12: `quote.submitted` shows the "From" price, option count, treatment and expiry (no single quote total); `quote.expiring_soon` uses the FR-026 lead time; added `quote.withdrawn` (mandatory), `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement` (all mandatory except the reminder) and `treatment.plan_changed` (mandatory); renamed `booking.scheduled` to Booking Accepted — Slot Held (Pending Payment); locked selected and not-selected `quote.accepted` outcomes with one notice per sent parent quote, a recipient matrix and no notice for unsent drafts; post-acceptance money from the accepted snapshot; `provider.status_cancellation_patient` limited to pre-acceptance; moved `quote.declined` to Post-MVP; synced `quote.cancelled_inquiry` lock and variables; renamed `outcomeCode` to `outcome`; added User Story 6, REQ-020-017 and REQ-020-018, and FR-004/006/010 dependencies. Findings FR-020-1, FR-020-2, FR-020-4, FR-020-7, S4-1, S4-2, S4-3, S4-5, S4-13, S4-14; decisions D5, D20, D21, D22, M2, M9, M13, M16, M17, P2. See [CR-FR020-20261016-01](./change-request-2026-10-16-mtg002-quote-model-alignment.md) | Claude |
| 2026-10-16 | 2.8     | Product Owner follow-up decisions, mirroring FR-030 v1.13: at acceptance the patient receives only `booking.scheduled`, and `quote.accepted` goes to the accepted and not-selected providers only; removed the admin recipient from `quote.accepted` and added admins as exception-alert recipients of `booking.hold_expiring_soon`, `booking.payment_window_expired` and `booking.provider_fault_replacement`; `quote.cancelled_inquiry` cannot be suppressed by FR-032 preferences (User Story 4 scenario 3 corrected); `quote.updated` renamed Quote Revised (New Version) and defined as the FR-004 re-send of a new version of a sent quote; added User Story 6 scenario 8, REQ-020-019 and REQ-020-020. Confirmed `booking.provider_fault_replacement` and `treatment.plan_changed` stay mandatory and lead times stay in FR-026. Decisions Q9, Q10, Q11, Q12, Q13, Q24. See [CR-FR020-20261016-01](./change-request-2026-10-16-mtg002-quote-model-alignment.md) | Claude |
| 2026-10-18 | 2.9     | Consolidated verification corrections ([CR-FR020-20261016-01](./change-request-2026-10-16-mtg002-quote-model-alignment.md)): `quote.withdrawn` always reaches the patient and alerts admins only when the withdrawn quote was already accepted, added to the admin exception list in Business Rules and REQ-020-019 (Q31); `booking.provider_fault_replacement` confirmed as Patient and Admin only, with the replacement provider told through the normal new-booking and acceptance notice (Q32); `treatment.plan_changed` fires from booking confirmation (`Confirmed`) onward, not from acceptance (Q2). | Product Owner / Documentation |
| 2026-10-18 | 2.10    | Final audit corrections ([CR-FR020-20261016-01](./change-request-2026-10-16-mtg002-quote-model-alignment.md)): added `booking.rescheduled` as a mandatory FR-006 event to the patient and provider for the admin appointment change, with previous and new appointment (Q42); `booking.scheduled` now goes to the patient only, is mandatory, and also fires for an admin-authored replacement acceptance, with the replacement provider told through `quote.accepted` (Q42); booking notices read the booking's current appointment while the snapshot keeps the accepted baseline (Q42); every mandatory provider event is exempt from FR-032 preferences, not only `quote.cancelled_inquiry`; `provider.status_cancellation_admin_support` also covers Aftercare cases flagged for aftercare reassignment (Q36); added REQ-020-021. Later the same day (decisions Q45, Q47): added the mandatory FR-011 event `aftercare.provider_reassigned` (Patient and new aftercare provider, no admin alert, exempt from FR-032 preferences); an `In Progress` booking under a provider-status event stays `In Progress` with `supportRequired` and raises `provider.status_cancellation_admin_support`, and `booking.provider_fault_replacement` now applies only before treatment starts; added REQ-020-022 and User Story 5 scenarios 6 and 7. | Product Owner / Documentation |
| 2026-10-26 | 2.11    | Product Owner decisions on FR-015 dev-team questions (Q9): `provider.status_cancellation_admin_support` goes to admins with View Providers permission; an unsent draft quote cancelled by provider suspension or deactivation triggers no patient notice | Claude (AI Assistant) |
| 2026-10-27 | 2.12    | Product Owner decisions on FR-015 dev-team follow-up questions ([CR-FR020-20261027-01](./change-request-2026-10-27-admin-support-recipients-status-email-timing.md)): `provider.status_cancellation_admin_support` now goes to admins with the FR-031 Respond to Support permission (default roles Super Admin, Aftercare Specialist, Support Staff), replacing the v2.11 View Providers rule (F7); with Notify Provider checked, `provider.suspended` / `provider.deactivated` are sent when a scheduled change is created and again when it takes effect (F6); `provider.suspended`, `provider.deactivated`, `provider.reactivated` and `provider.scheduled_change_cancelled` go to the provider Owner only (F20). REQ-020-014 updated. `provider.status_cancellation_patient` adds the two pre-acceptance variants from FR-003 REQ-003-021 ("We are finding new offers for you." on redistribution; confirmation first when the patient had selected the affected provider), mirroring [CR-FR003-20261027-02](../fr003-inquiry-submission/change-request-2026-10-27-pre-acceptance-redistribution.md); catalog row, Provider-Status Cancellation Notifications rule, and REQ-020-013 updated | Product Owner / Documentation |
| 2026-10-28 | 2.13    | Product Owner decision 2026-10-28 (FR-015 backend confirmations); no Change Request. New mandatory provider event `provider.login_email_changed` (catalog, Provider Lifecycle Notifications rule, FR-015 integration note, REQ-020-015): when an admin changes the Owner login email (FR-015), an email goes to the old address (change notice with the partly masked new address, admin, date and time, and a contact-support prompt) and to the new address (it is now the clinic's login email); `provider.activation` is also sent to the new address when `password_set` is false (existing). Mirrored in FR-030 v1.17. Follow-up the same day (Product Owner decision on the FR-003 Screen 8 banner): the pre-acceptance `provider.status_cancellation_patient` text now names the clinic, "[Clinic] is no longer available. Your other offers are still open." when other offers remain open, or "[Clinic] is no longer available. We are finding new offers for you." on redistribution (catalog row, Provider-Status Cancellation Notifications rule, REQ-020-013); event names unchanged | Claude (AI Assistant) |

---

## Appendix: Approvals

| Role           | Name | Date | Signature/Approval |
|----------------|------|------|--------------------|
| Product Owner  |      |      |                    |
| Product Owner  | Joachim Trung Tuan | 2026-09-16 | Approved FR-005 quote-outcome and recipient-privacy alignment through v2.1 |
| Product Owner  | Joachim Trung Tuan | 2026-10-18 | Approved FR-020 v2.7 to v2.10 via MTG-002 decision log (documentation only), including CR-FR020-20261016-01 |
| Product Owner  | Joachim Trung Tuan | 2026-10-27 | Approved FR-020 v2.12 (documentation only), including CR-FR020-20261027-01 |
| Technical Lead |      |      |                    |
| Stakeholder    |      |      |                    |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Last Updated**: 2026-10-28
