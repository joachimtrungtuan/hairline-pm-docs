# FR-004 - Quote Submission & Management

**Module**: PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr004-quote-submission-management`
**Created**: 2025-10-30
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-004 from system-prd.md; SRC-MTG-002 (MTG-002-D03 through D06 and O01); FR-005 v2.5; FR-006 v2.7; Product Owner clarifications dated 2026-09-09, 2026-09-10, and 2026-09-16; Product Owner MTG-002 quote-model decision log dated 2026-10-16

## Executive Summary

The Quote Submission & Management module enables providers to create, edit, submit, and manage detailed quote responses for distributed patient inquiries. An inquiry may receive multiple quotes, including multiple quotes from the same provider. Each quote is one auditable parent response containing one to five package-based Quote Options that the patient can compare. Treatment facts shared across the options remain on the parent quote, while package inclusions, package-specific day plans, applicable date ranges, and prices belong to the individual options.

Package options begin from provider-owned package-library presets. Providers may customize each selected package inline for the current quote, but those changes are quote-local snapshots and never update or create reusable package-library records.

### Quote Hierarchy

```text
Parent Quote
└── Quote Option
    └── Option/Date-Price Record
```

- **Parent Quote**: One provider response and the aggregate/version boundary. It owns the provider, treatment, graft facts, visual plan, clinicians, shared notes/requirements, attachments, currency, expiry, lifecycle, and audit history.
- **Quote Option**: One package alternative inside the parent quote. It owns the package snapshot, included/custom services, and relative day-to-day treatment plan.
- **Option/Date-Price Record**: One applicable patient-requested date range for that option, with its pre-scheduled appointment, offered price, and optional promotion. A provider may leave out any option/date-range pairing it cannot offer, but every option must apply to at least one range.
- **Subquote (FR-005 patient view)**: One Quote Option plus one applicable Option/Date-Price Record, combined with inherited Parent Quote context. This is the complete item the patient views, compares, and accepts. Parent Quotes, Quote Options, and Option/Date-Price Records are not accepted independently.

Each selected package seeds exactly one Quote Option; packages are never summed or merged into one option. A parent quote therefore yields up to (number of options × number of patient-requested date ranges) subquotes. For example, three packages offered across two date ranges give up to six subquotes, and the patient accepts exactly one of them.

The Parent Quote is versioned as one aggregate. Every derived subquote uses that aggregate `QuoteVersion`; Quote Options and Option/Date-Price Records retain stable identifiers but do not have independent revision counters.

## Module Scope

### Multi-Tenant Architecture

- **Provider Platform (PR-02)**: Core quote management and submission
- **Patient Platform (P-02)**: Quote review/acceptance/cancellation (read-only for submission)
- **Admin Platform (A-01)**: Audit, visibility, and override authority on all quote objects

### Multi-Tenant Breakdown

**Patient Platform (P-02)**:

- View parent quotes and their derived subquotes per inquiry; compare and accept exactly one eligible subquote; see expiry timers and status
- Receive notifications for quote creation/updates/expiry

**Provider Platform (PR-02)**:

- Create multiple quotes for an inquiry when needed; configure one to five comparable package options within each quote
- Customize package inclusions inline without changing the provider's reusable package library
- Edit and submit quotes; manage lifecycle (draft, sent, expired, withdrawn, archived) (REQ-004-070)
- See inquiry context (append-only)

**Admin Platform (A-01)**:

- Oversight of all quotes; inline edit (policy-bound), soft delete/restore; full audit trail
- Configure expiry window. Only the provider withdraws a quote; an admin never withdraws one
- Restore an expired quote with a fresh window and a reason, or a quote archived from draft or sent, while the restore guards hold (REQ-004-077, REQ-004-105)
- Author the replacement quote of an FR-006 provider-fault transfer on Screen 8 (Workflow 7)

**Shared Services (S-XX)**:

- Notification service; audit logging; retention/soft-delete utilities

### Communication Structure

**In Scope**:

- System → Provider: New inquiry notifications and time-bound updates
- Provider → System: Draft, edit, status transitions, soft delete/archive
- System → Patient: Quote creation/expiry/status notifications (FR-004 produces `quote.submitted`, `quote.updated`, `quote.expiring_soon`, `quote.expired`, `quote.withdrawn` and `quote.restored`)
- System → Provider: `quote.cancelled_inquiry`, sent only to the providers whose quotes the inquiry-cancellation cascade cancelled; `quote.restored` also reaches the provider of a restored quote
- Admin → All Parties: Oversight, intervention, audit logging

**Out of Scope**:

- Direct patient-provider chat (handled by FR-012)

### Entry Points

1. Provider receives auto-distributed inquiry from FR-003
2. Provider opens the unified Quote List (Screen 2; one list, no tabs)
3. Provider creates and edits a quote by selecting the shared treatment, then configuring one to five package options
4. Patient receives parent quote(s) and views their complete subquotes in the patient app
5. Admin can access, search, or override quote status from admin platform
6. Admin opens Screen 8 from the FR-006 provider-fault transfer to author the replacement quote (Workflow 7)

## Business Workflows

### Workflow 1: Provider Quote Creation (Primary Flow)

**Actors**: Provider, System, Admin (observer/audit)

**Trigger**: Provider opens a distributed inquiry and starts composing a quote

**Outcome**: A valid parent quote with one to five package options is delivered to the patient; the complete quote aggregate is versioned and audited

- Provider receives inquiry and opens details
- System verifies parent inquiry status is not Cancelled before allowing quote creation. If inquiry is cancelled, system blocks with error: "Inquiry no longer active — this inquiry was cancelled by the patient."
- **Restricted recipient check**: If the inquiry carries an exclusive assigned provider from an FR-037 monitoring conversion, system verifies the opening provider is the assigned provider; any other provider is blocked with error "This inquiry is restricted to its assigned provider." (see Business Rules)
- **Legal acceptance check**: A provider who has not accepted the current legal documents cannot submit a quote; the acceptance prompt is shown and the draft is kept (REQ-004-112, REQ-027-033).
- **Provider status check**: System verifies the provider is `Active` before quote creation and again at submission. A `Suspended` or `Deactivated` provider (FR-015 Screen 4) cannot create or submit quotes; an in-flight submission received after the effective time is rejected and creates no sent quote.
- In Tab 1, Provider selects one treatment service for the parent quote
- In Tab 2, Provider selects between one and five packages from the provider's active package library; each selected package seeds exactly one alternative Quote Option (never summed with another package) and may be opened in the inline package editor
- System copies the selected package version into the Quote Option: its services and their pricing, its included travel services (transport, hotel, flight, and other travel services), its standard price, and its relative day-by-day treatment plan. The option records the source package ID, the source package version, and whether it has been customised inline. Date ranges, additional notes, and documents are never packaged; they are entered per quote
- Inline additions, edits, inclusions, or removals apply only to that option and are never written back to the package library (see Business Rules, "Package library edits and quote inline edits")
- In Tab 3, Provider enters the shared graft estimate and visual treatment plan
- In Tab 4, Provider configures the combined date-and-price matrix by selecting applicable patient-requested ranges for each option and pricing every applicable option/date combination; the package standard price prefills each applicable row, and the provider may leave out any pairing it cannot offer
- In Tab 5, Provider reviews and adjusts each option's relative day-to-day treatment plan, which is prefilled from the source package
- In Tab 6, Provider selects the shared clinicians and enters common notes/requirements and attachments
- In Tab 7, Provider reviews the complete quote aggregate and submits it
- Provider submits quote (system validates required/optional fields; re-validates that the inquiry is still active and the provider is still `Active` at submission time)
- On first send, System records the first-send timestamp and captures the quote expiry and the quote currency read-only from the active FR-026 quote configuration and records that configuration's version on the quote; drafts carry neither. If the FR-026 configuration cannot be read, first send is blocked and the draft is kept unchanged
- On every send, System copies the terms of each attached promotion into the sent quote version and attaches at most one automatic FR-019 promotion per quote to each eligible option/date-price row; when several automatic promotions qualify, the FR-019 priority order picks one (see Business Rules, "Promotions on quotes"). A sent quote carrying an automatic promotion holds exactly one reserved use of that promotion's usage limit, and a re-send of a new version keeps that reservation rather than adding a second one
- System delivers the parent quote and its ordered options to the patient and records one atomic version/audit snapshot of the aggregate
- On first send only, System emits `quote.submitted` for FR-020 notification; a re-send of a new version emits `quote.updated` instead (Workflow 2)
- A sent quote opens the FR-012 conversation between that provider and the patient when it is the provider's first quote for the inquiry, and otherwise adds to the existing conversation (REQ-004-107)

### Workflow 2: Quote Editing

**Actors**: Provider, System, Admin (editor through Screen 7 while the quote is draft or sent, and after acceptance within the limits below)

**Trigger**: Provider opens an existing draft or sent (pre-expiry) quote to modify fields

**Outcome**: Changes are saved with versioning/audit; the patient is notified when a new version of a sent quote is re-sent (`quote.updated`)

- Provider may edit draft or sent (pre-expiry) quotes, including shared fields, options, option-local inclusions, date-price combinations, and option-specific plans
- Admin may edit draft or sent quotes through Screen 7 with a mandatory reason; an admin edit of a sent quote creates a new version and emits `quote.updated` when that version is re-sent
- After acceptance an admin may change any quote field except price, currency, and promotion, with a mandatory reason and full history. The change is stored as a new version beside the acceptance snapshot, which stays unchanged, and payment records never change
- Package-library changes made after an option was created do not alter the quote snapshot
- All parent and option changes are versioned/audited as one quote aggregate
- Edits on expired, withdrawn, archived, or cancelled quotes are prohibited for providers and admins. After acceptance providers are blocked from every quote edit, and their treatment-detail changes (plan, clinicians, grafts) go only through FR-010; price, currency, and promotion never change; the booking's appointment changes only through the FR-006 admin appointment change or an admin edit of the accepted quote's date range or appointment (REQ-005-023), each of which emits `booking.rescheduled`, while the acceptance snapshot keeps the accepted appointment as the baseline
- When a new version of an already-sent quote is re-sent, System emits `quote.updated` (described as "quote revised (new version)") for FR-020 notification; FR-004 is the only producer of this event. Saving draft edits without re-sending emits nothing
- A re-send or new version never changes the quote's first-send timestamp or its expiry

### Workflow 3: Quote Expiry & Status Transitions

**Actors**: System, Provider, Patient, Admin (observer)

**Trigger**: Time-based expiry reached; patient accepts a subquote through FR-005; provider initiates withdrawal/archive; patient cancels parent inquiry (FR-003 Workflow 5); or the owning provider becomes `Suspended` or `Deactivated` (FR-015 Alternative Flow A5 and Screen 4)

**Outcome**: Quote transitions to correct status; notifications sent; audit recorded

- Expiry is captured at first send: the system copies the quote expiry setting from the active FR-026 quote configuration (default 48 hours) read-only onto the quote and computes the expiry timestamp from the first send time. Drafts have no expiry. Later edits and re-sends do not reset it, later setting changes never affect a sent quote, and there is no per-quote extension, except that an admin who restores an expired quote gives it a fresh full window (REQ-004-105). Providers cannot modify the window and only see the computed expiry timestamp. The admin-authored replacement quote of a provider-fault transfer has no expiry (Workflow 7).
- Expiry applies only to `sent` parent quotes. Upon expiry, system updates the parent quote to `expired`, emits `quote.expired` once per expiry window of that parent quote (FR-030, REQ-030-036); a restore opens a fresh window, and every child subquote becomes ineligible for acceptance. `accepted` quotes and every cancelled, withdrawn, or archived quote are never moved to `expired`.
- When a sent parent quote reaches the "quote expiring soon" lead time set by admin in FR-026, the system emits `quote.expiring_soon` once per expiry window of that parent quote (FR-030). It is never emitted for drafts, for accepted or terminal quotes, or for the replacement quote. A lead time raised after the send applies only to reminders not yet sent; a reminder whose time has already passed is skipped, not sent late (REQ-026-031).
- Provider may withdraw a `sent` quote before acceptance with an optional reason, from the quote detail screen (Screen 3). Only an admin archives a sent quote; a provider soft-deletes drafts only (Workflow 4). The `quote.withdrawn` notification is always mandatory, before and after acceptance. FR-004 is its only producer. The patient is always notified; the admin is notified only when the withdrawn quote was already accepted (Workflow 6), because a withdrawal before acceptance is a normal provider action.
- FR-005 subquote acceptance moves the selected subquote and its parent quote to `accepted`, marks sibling subquotes `not_selected`, and moves every other parent quote for the inquiry, from any provider, to `cancelled_other_accepted`; the parent quote, Quote Option, and Option/Date-Price Record are never direct acceptance targets. Each sent parent quote that is cancelled this way produces one not-selected notice per parent quote. Unsent draft parent quotes are cancelled silently with the same status and no notice. The cascade runs on the patient's acceptance only: the admin-authored replacement acceptance of a provider-fault transfer leaves the original quote's status as it is and cancels every other open replacement draft silently, with no notice to its provider (REQ-004-082).
- An accepted parent quote stays `accepted` and is never reopened for acceptance or moved to `expired`, including after FR-006 moves the booking to `Payment Window Expired`; its status changes only through provider withdrawal (Workflow 6), allowed only while the booking is `Accepted` or `Confirmed`, before check-in, and without a provider-fault marker. An admin booking cancellation in FR-006 moves the booking and inquiry to `Cancelled` but leaves the accepted parent quote `accepted`. Competing parent quotes stay cancelled, and no new parent quote can be created or sent for an inquiry that has an active acceptance (REQ-004-110); the only exception is the admin-authored replacement quote for an FR-006 provider-fault transfer (Workflow 7). The patient cannot cancel the inquiry after acceptance; through "Contact support" the patient reaches an admin, who performs the audited FR-006 revive or an FR-006 booking cancellation, after which the patient may start a new inquiry.
- **Admin restores an expired quote**: An admin may restore an `expired` quote to `sent` with a fresh full window (restore time plus the FR-026 window in force) and a mandatory reason, unless a guard fails: the inquiry is not open, the provider is not `Active`, the inquiry has an active acceptance (REQ-004-110), or the booking carries a provider-fault marker (REQ-004-109); a blocked restore shows a message that names the guard. Before restoring, the system re-checks the promotion and takes a new reservation only when the quote holds none; if the promotion limit is used up or the promotion has ended, the restore is blocked with a message and the provider may send a new quote. The patient and the provider are notified through `quote.restored` (REQ-004-105, REQ-004-106).
- **Patient cancels parent inquiry**: The patient can cancel only in the Inquiry or Quoted stage, before any subquote is accepted. Only quotes for that inquiry in draft, sent, or expired status transition to "Cancelled (Inquiry Cancelled)"; quotes in any other status (for example Cancelled (Provider Status), Withdrawn, Cancelled (Other Accepted), Accepted, or Archived) keep their status and cause. This is a system-initiated cascade owned by FR-003 (REQ-003-013), not a provider or patient action on the quote itself. Only providers whose quotes were cancelled by this cascade are notified via `quote.cancelled_inquiry` event (FR-020).
- **Provider becomes Suspended or Deactivated**: At the effective time, the system cancels every unaccepted draft or sent parent quote of that provider with status `cancelled_provider_status` and `cancellationProvenance` = `ProviderSuspended` or `ProviderDeactivated`. Cancelling an unsent draft is silent to the patient: the patient never saw it, so it triggers no `provider.status_cancellation_patient` notice on its own (admin support alerts still follow FR-020). Cancellation is recorded once per parent quote; its Quote Options and option/date-price alternatives become unavailable with the parent and are not cancelled or counted separately. `cancelled_provider_status` never applies to an accepted parent quote: if the provider's quote was already accepted, the parent quote keeps `accepted` and the FR-005 AcceptanceEvent stays unchanged. FR-006 Alternative Flow B4 records the closure on the booking as its cause, and no supersession record is written at that point. FR-005 writes the single linked supersession record only when the admin accepts the replacement quote in the FR-006 provider-fault transfer (FR-006 Alternative Flow B5). The FR-005 AcceptanceEvent, accepted IDs/versions, and quote-local package snapshots are not rewritten. Quotes already expired, withdrawn, archived, or otherwise terminal are not reclassified. Other providers' quotes are unaffected. Later reactivation does not restore cancelled quotes.
- All state transitions are logged and result in notifications as appropriate

### Workflow 4: Quote Deletion (Soft Delete)

**Actors**: Provider, System, Admin

**Trigger**: Provider chooses to remove an obsolete draft quote, or an admin archives a quote

**Outcome**: Quote becomes Archived with rationale; remains visible in audit/archive; only admin can restore

- Provider may soft-delete a draft quote only (removes it from the provider listing, not from the audit/archive). A sent quote cannot be soft-deleted by the provider: it leaves the offered state only by provider withdrawal before acceptance (Workflow 3), by expiry, or through the patient's choice
- Drafts and archived quotes are never shown to patients. An admin may archive a sent quote, which removes it from the patient's view
- Quotes in any status other than draft (sent, accepted, expired, withdrawn, cancelled_other_accepted, cancelled_inquiry_cancelled, cancelled_provider_status) cannot be soft-deleted by the provider
- System sets status = Archived with rationale
- Soft-deletes are fully auditable and revertible only by admin
- Restore is offered only for a quote archived from `draft` or `sent`, read from its archive audit entry; any other archived quote shows no Restore action. A restore is blocked, with a message that names the guard, when the inquiry is not open, the provider is not `Active`, the inquiry has an active acceptance, or the booking carries a provider-fault marker. An admin restore returns an archived draft to `draft` with a fresh 7-day count. An archived sent quote (admin archive only) is restored to `sent` when its original expiry has not passed, with no renewal, and to `expired` otherwise; an expired quote is then restored under REQ-004-105 (REQ-004-077, REQ-004-109, REQ-004-110)

### Workflow 5: Admin Oversight

**Actors**: Admin, System

**Trigger**: Admin monitors quotes or intervenes per policy or escalation

**Outcome**: Administrative action applied; full audit trail preserved; re-notifications triggered if needed

- Admin dashboard lists all provider quotes, searchable/filterable by state/date/provider/inquiry
- Admin can perform soft delete or restore and view the immutable audit trail and full quote history; soft delete and restore are unavailable for a quote in `accepted` status, which is never deleted or restored
- Admin can restore an expired quote to `sent` with a fresh window and a mandatory reason, unless a restore guard fails (Workflow 3), and only after the promotion re-check (REQ-004-105)
- Admin authors a quote only as the replacement quote of an FR-006 provider-fault transfer (Workflow 7, Screen 8)

### Workflow 6: Provider Withdrawal After Acceptance

**Actors**: Provider, Admin, Patient, System

**Trigger**: Provider withdraws the accepted quote while the booking is `Accepted` or `Confirmed` and before check-in

**Outcome**: The parent quote moves from `accepted` to `withdrawn` and the case is handed to the FR-006 provider-fault transfer; FR-004 does not re-route the case

- In rare cases, provider may withdraw from giving treatment after patient acceptance.
- The Withdraw action on Screen 3 is offered for an accepted quote only while the booking is `Accepted` or `Confirmed`, before the patient has checked in, and while the booking carries no provider-fault marker. The action opens a confirmation that states the consequence: the booking goes to the admin for a transfer or refund. In every other booking state the action is hidden and Screen 3 shows a short note that the quote can no longer be withdrawn.
- Provider submits a withdrawal with a mandatory reason; the parent quote moves from `accepted` to `withdrawn`. This is the only status change FR-004 makes after acceptance; no quote field, option, or option/date-price record is edited.
- The FR-005 AcceptanceEvent, accepted IDs/versions, acceptance snapshot, and quote-local package snapshots are kept unchanged as history. FR-005 marks the AcceptanceEvent superseded by provider fault through a linked supersession record, never by editing it.
- FR-004 hands the case to the FR-006 provider-fault transfer (FR-006 Alternative Flow B5). The booking keeps its status and its slot hold and carries the provider-fault marker; payment and reminders stop until the admin submits the replacement on FR-006 Screen 10, which then cancels the original booking with cause `ProviderFault` and releases the hold. The admin assigns a replacement provider within the same inquiry, authors a replacement quote for that provider (Workflow 7), and records a new admin-authored acceptance against it that is linked to the original. The patient keeps the same inquiry and re-enters nothing. FR-004 does not reopen competing quotes or re-route the case itself; its only part in the transfer is the admin-authored replacement quote.
- While the booking carries the provider-fault marker, whether the fault is pending or the booking is already cancelled, no provider edit and no admin edit of the accepted quote, except admin notes, is allowed, an admin restore is blocked, and a second withdrawal is hidden; the replacement quote on Screen 8 is the only quote write allowed (REQ-004-109).
- Money already paid follows the FR-006 payment terms: the patient is refunded in full everything paid, pays no cancellation fee, and the replacement booking takes a new payment. Exact mechanics are defined in FR-007, FR-007B, and FR-017.
- The `quote.withdrawn` notification to the patient and admin is mandatory; FR-004 emits it, and FR-006 reacts by starting the provider-fault transfer without emitting it again. All actions are audited.
- Provider drop-out after acceptance, including an FR-010 reassignment, is not a quote withdrawal; FR-010 routes it to FR-006. The provider-fault transfer with a replacement quote and a new acceptance applies only before treatment starts (booking `Accepted` or `Confirmed`). If the fault happens in Aftercare, the admin reassigns only the aftercare provider or team in FR-006; the booking and treatment record stay, and no replacement quote, new acceptance, or new payment is created.

### Workflow 7: Admin Replacement Quote (Provider-Fault Transfer)

**Actors**: Admin, System

**Trigger**: The booking carries a provider fault before treatment started (pending, or already closed with `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated`), and the admin has chosen a replacement provider in the FR-006 transfer

**Outcome**: One admin-authored replacement quote exists for the replacement provider inside the same inquiry and is ready for the FR-006 admin-authored replacement acceptance

- The admin opens Screen 8 from the FR-006 transfer. The system checks that the booking carries a provider fault (pending, or closed with a provider-fault cause), that the booking is `Accepted`, `Confirmed`, or `Cancelled` with the provider-fault marker, that no replacement acceptance has been recorded for this transfer, that treatment had not started, and that the replacement provider is `Active` and is not the provider at fault. When a check fails, Screen 8 is blocked with a message that names the failed check. The original acceptance stays the active one until the replacement acceptance is recorded (REQ-004-110).
- The admin builds the quote with the same structure as a provider quote: shared treatment facts, one or more Quote Options seeded from the replacement provider's active packages, and option/date-price rows with appointment date/time, time zone, and price. The accepted quote and snapshot of the original acceptance are shown read-only for reference.
- The admin may adjust the package and price for the replacement; a mandatory reason is required.
- The admin sets the replacement price directly. No automatic FR-019 promotion attaches to a replacement quote and no promotion usage reservation is taken for it. The replacement quote carries no promotion; the promotion application of the original acceptance is marked Superseded and the use it held returns to the promotion's usage limit (FR-019).
- On the first save, the system records the quote as admin-authored for a replacement (`authorType = admin`, linked to the AcceptanceEvent it replaces), captures its currency from the active FR-026 quote configuration, shows it on Screen 8, and fixes it from then on (REQ-004-082). The system keeps its version and audit history like any quote. The quote stays a `draft` with no expiry and no `quote.expiring_soon` notice. It is hidden from the replacement provider and from the patient until it is accepted: it is not listed on Screen 2, Screen 4, or Screen 7, Screen 8 is its only edit surface, and it does not emit `quote.submitted` or `quote.expired` (REQ-004-048).
- The admin then records the replacement acceptance in FR-006 against one option/date-price row of this quote; FR-005 Alternative Flow A9 records the AcceptanceEvent and the supersession link. At that moment the system moves the quote from `draft` through `sent` to `accepted`, records its first-send time, and the patient sees it on Screen 4 as the accepted quote. The acceptance runs no cancel-other-quotes cascade: the original quote keeps its status, and every other open replacement draft of the inquiry is cancelled as `cancelled_other_accepted` silently, with no notice to its provider (REQ-004-082).
- This is the only case in which a quote is created for an inquiry that already had an accepted subquote. One replacement acceptance is recorded per transfer.
- A replacement draft that is never accepted never expires. It is archived by the same 7-day draft rule as any draft (counted from its last edit); an archived replacement draft cannot be restored while the provider-fault marker stays (REQ-004-109), so the admin authors a new replacement quote on Screen 8. It is cancelled with status `cancelled_inquiry_cancelled`, without any notice to the replacement provider, when an admin closes or cancels the inquiry (REQ-004-111). The inquiry stays flagged `supportRequired` and is not cancelled automatically. The admin may then author another replacement quote through Screen 8, or end the case: close the inquiry with Close inquiry on FR-006 Screen 6 when the booking is already `Cancelled` with the marker, or cancel through FR-006 Alternative Flow B2 (Screen 9) when the fault is still pending.

### Alternative Flows

- Provider starts draft but abandons (system retains drafts for 7 days after the last edit, then auto-archives; the 7 days are a fixed platform rule with no admin setting)
- Provider attempts late edit or deletion (system disallows and shows user message)
- Provider creates an additional quote for the same inquiry (system treats it as a separate parent response with its own options, expiry, versions, and audit history)
- Provider customizes a selected package inline (system stores a quote-local option snapshot and leaves the package library unchanged)
- Provider removes an option before submission (system permits removal while at least one valid option remains)
- Patient accepts no subquote (system expires all open sent quotes automatically; there is no parent-level Decline action)
- Another quote is accepted → System marks all other parent quotes for the same inquiry as "cancelled (other accepted)"; each sent parent quote produces one not-selected notice per parent quote to its provider.
- While a provider is drafting a quote, if another quote is accepted → the unsent draft is cancelled silently as "cancelled (other accepted)" with no notice; on next open the draft is read-only with the "Another Quote Accepted" badge and cannot be submitted.
- Patient cancels parent inquiry (FR-003 Workflow 5) → only draft, sent, and expired quotes for that inquiry are auto-cancelled with status "Cancelled (Inquiry Cancelled)"; quotes in any other status keep their status and cause; only providers whose quotes were cancelled by this cascade are notified via `quote.cancelled_inquiry` event; drafting providers see locked quote with "Inquiry Cancelled" banner upon next save/refresh. Cancellation reason is patient-private and NOT shared with providers.
- Owning provider becomes `Suspended` or `Deactivated` (FR-015 A5/Screen 4) → that provider's unaccepted parent quotes are cancelled once each with `cancelled_provider_status` and the provider-caused `cancellationProvenance` (Workflow 3); drafting and submission are blocked; patients see the offer as unavailable with a Contact Admin/Support action rather than the patient-cancellation message. An already-accepted quote of that provider keeps `accepted` and is handled by the FR-006 provider-fault transfer.
- Provider withdraws a sent quote before acceptance (Workflow 3) → on Screen 3 the provider chooses Withdraw with an optional reason; the quote moves to `withdrawn`, the promotion reservation is released, and the patient receives `quote.withdrawn`.
- Provider withdraws the accepted quote (Workflow 6) → on Screen 3, only while the booking is `Accepted` or `Confirmed`, before check-in, and with no provider-fault marker; a confirmation names the consequence and a mandatory reason is required, the quote moves to `withdrawn`, and the case is handed to FR-006 Alternative Flow B5.
- Admin authors a replacement quote after a provider fault (Workflow 7) → the admin opens Screen 8, builds and saves the quote as a draft that stays hidden from the provider and the patient, and then records the replacement acceptance in FR-006.
- Admin restores an expired quote or a quote archived from draft or sent (Workflow 3, Workflow 4) → the admin restores it with a mandatory reason while the guards hold (inquiry open, provider `Active`, no active acceptance, no provider-fault marker); an expired quote returns to `sent` with a fresh window, subject to the promotion re-check in REQ-004-105; a failed guard blocks the restore with a message, and other archived quotes show no Restore.
- Provider soft-deletes a draft quote (Workflow 4) → on Screen 2 the provider archives the draft with a rationale; a sent quote cannot be soft-deleted.
- A sent quote reaches the expiring-soon lead time (Workflow 3) → the system emits `quote.expiring_soon` once per expiry window of that parent quote.
- An admin closes or cancels the inquiry while a replacement draft exists (Workflow 7) → the system moves the draft to `cancelled_inquiry_cancelled` without any notice to the replacement provider (REQ-004-111).

## Screen Specifications

### Provider Platform

#### Screen 1: Quote Creation/Edit

**Purpose**: Provider creates or edits one parent quote and its package options with full inquiry context

**Quote Data Ownership Matrix**:

This matrix is the canonical completeness check for Screen 1. Tabs organize editing, but they do not change entity ownership. Fields marked system-owned or derived are never provider inputs.

| Entity / Field | Ownership | Provider Surface | Contract | Graph field |
| --- | --- | --- | --- | --- |
| Quote ID | System-owned | Persistent context and Tab 7 | Stable generated identifier; read-only | ENT-quote.id |
| Inquiry ID and inquiry context | System-owned from FR-003 | Persistent context and Tab 7 | Read-only; quote appends to the inquiry and never overwrites it | ENT-quote.inquiry_id |
| Provider ID | System-owned from authenticated tenant | Tab 7 | Read-only; never selected in the quote | ENT-quote.provider_id |
| Treatment ID and version | Provider-selected relationship | Tab 1 | References the exact immutable FR-024 Treatment version shared by every option; the quote does not copy treatment-owned data | ENT-quote.treatment_id, ENT-quote.treatment_version |
| Technique details | Database/API retrieved from Treatment | Tabs 1 and 7 | Loaded read-only through the exact Treatment-version relationship; never separate provider input or duplicated quote data | ENT-treatment.technique_details |
| Estimated grafts | Provider-edited parent field | Tab 3 | Positive integer shared by every option | ENT-quote.estimated_grafts |
| Graft description | System-derived parent field | Tab 3 | Generated from the fixed template (Business Rules, Graft Description template) and estimated grafts; read-only | ENT-quote.graft_description |
| Visual treatment plan / graft markup | Provider-edited parent field | Tab 3 | Optional shared drawing/media snapshot | ENT-quote.graft_visual_plan |
| Clinician IDs | Provider-edited parent field | Tab 6 | One or more eligible clinicians shared by every option | ENT-quote.clinician_ids |
| Common notes | Provider-edited parent field | Tab 6 | Optional text applying to every option | ENT-quote.common_notes |
| Common requirements | Provider-edited parent field | Tab 6 | Optional structured/text requirements applying to every option | ENT-quote.common_requirements |
| Attachments | Provider-edited parent field | Tab 6 | Optional quote-level files applying to every option | ENT-quote.attachment_ids |
| Currency snapshot | System-configured parent field | Read-only in Tabs 4 and 7 | Captured read-only at first send from the active FR-026 quote configuration, whose currency is the FR-029 Default Currency; drafts carry none; never provider input | ENT-quote.currency_snapshot |
| Status | System-owned lifecycle field | Persistent context and Tab 7 | Read-only; changed only by governed workflow actions | ENT-quote.status |
| Expiry | System-derived parent field | Tab 7 | Captured read-only at first send from the FR-026 quote expiry setting; drafts carry none; no per-quote extension | ENT-quote.expires_at |
| Calculated price range / accepted total | System-derived parent summary | Tabs 4 and 7 | Price range is derived from all option/date prices; accepted total is written only at FR-005 acceptance from the acceptance snapshot (price after promotion) and is a read-only copy; neither is entered separately (REQ-004-086, REQ-004-093) | ENT-quote.calculated_price_range, ENT-quote.accepted_total |
| Commission | System-derived financial field | Tab 7 subject to permissions | Shows the commission model and value (percentage or flat rate) from the active FR-029 configuration, labelled "indicative, final at booking confirmation"; the binding commission is fixed at booking confirmation on the accepted price after promotion (FR-029); never provider input | ENT-quote.commission |
| Affiliate attribution reference | System-captured financial provenance | Tab 7 subject to permissions | Inherited from validated referral context; never provider input; display-only here, data owned by FR-018 | ENT-affiliate-attribution.reference |
| Terms acknowledged timestamp | System-owned FR-005 acceptance field | Tab 7 after acceptance | Null during quote creation; read-only copy of the FR-005 acceptance snapshot value (REQ-004-086) | ENT-quote.terms_acknowledged_at |
| Locked exchange-rate value and pair | System-owned FR-005/FR-029 acceptance snapshot | Tab 7 subject to permissions | Null before acceptance; read-only copy of the FR-005 acceptance snapshot value when conversion is required (REQ-004-086) | ENT-quote.locked_exchange_rate_snapshot |
| Cancellation and supersession provenance | System-owned lifecycle fields | Tab 7 / Audit | Records inquiry cancellation, another accepted quote, or provider suspension/deactivation of an unaccepted quote; never provider input | ENT-quote.cancellation_provenance |
| Travel path | System-owned FR-008 downstream field | Tab 7 after applicable workflow action | Derived from the accepted option (FR-008); display-only; not edited during quote creation | ENT-travel-context.travel_path |
| Created and updated timestamps | System-owned audit metadata | Tab 7 / Audit | System-generated; read-only | ENT-quote.created_at, ENT-quote.updated_at |
| Quote Option ID and parent Quote ID | System-owned | Tabs 2, 4, 5, and 7 | Stable identifiers; read-only | ENT-quote-option.id, ENT-quote-option.quote_id |
| Source Package ID and version | System-captured option provenance | Tab 2 and Sub-screen 2A | Captured when selected (the exact FR-024 package version); read-only after snapshot creation | ENT-quote-option.source_package_id, ENT-quote-option.source_package_version |
| Option display order | Provider-edited option field | Tab 2 | Unique consecutive patient-facing order | ENT-quote-option.display_order |
| Package name, description, and standard price snapshots | System-copied option fields | Tab 2 and Sub-screen 2A | Copied from the selected library version; retained for history | ENT-quote-option.package_name_snapshot, ENT-quote-option.package_description_snapshot, ENT-quote-option.standard_price_snapshot |
| Option customization state (inline-customised flag) | System-derived option field | Tab 2 and Tab 7 | Indicates whether the quote-local copy has been edited inline and differs from its source package version | ENT-quote-option.is_customized |
| Included travel services (`included_services`) | Provider-edited option field | Sub-screen 2A | Flight, hotel, transport, and other travel services included in this option; stored only in the option snapshot | ENT-quote-option.included_services |
| Option item ID and parent Option ID | System-owned | Sub-screen 2A and Audit | Stable identifiers; read-only | ENT-quote-option-item.id, ENT-quote-option-item.quote_option_id |
| Option item source ID | System-captured item provenance | Sub-screen 2A | Read-only; null for an item created inside the quote | ENT-quote-option-item.source_package_item_id |
| Option item type | Provider-edited item field | Sub-screen 2A | Controlled service type | ENT-quote-option-item.item_type |
| Option item name and description | Provider-edited item fields | Sub-screen 2A | Required name; optional description | ENT-quote-option-item.name, ENT-quote-option-item.description |
| Option item price | Provider-edited item field | Sub-screen 2A | Optional component price; does not replace the final Tab 4 offered price | ENT-quote-option-item.price |
| Option item inclusion state | Provider-edited item field | Sub-screen 2A | Explicit included or excluded state | ENT-quote-option-item.is_included |
| Option item display order | Provider-edited item field | Sub-screen 2A | Unique consecutive order within the option | ENT-quote-option-item.display_order |
| Option item metadata | System-retained item field | Sub-screen 2A / Audit | Read-only extension/source metadata; never free-form provider input | ENT-quote-option-item.metadata |
| Option/date-price ID | System-owned | Tab 4 and Tab 7 | Stable identifier for FR-005 acceptance | ENT-quote-option-date-price.id |
| Source inquiry date-range ID | Provider-selected reference | Tab 4 | Must reference a patient-requested FR-003 range | ENT-quote-option-date-price.source_inquiry_date_range_id |
| Start and end dates | System-copied date fields | Tab 4 | Read-only values from the selected inquiry range | ENT-quote-option-date-price.start_date, ENT-quote-option-date-price.end_date |
| Appointment date/time and timezone | Provider-edited option/date fields | Tab 4 | Appointment must fall within the selected range and be in the future when sent; timezone required. Together with the provider, these fields are the key of the FR-006 slot hold placed at acceptance; no appointment record is created at quote time (REQ-004-062) | ENT-quote-option-date-price.appointment_at, ENT-quote-option-date-price.appointment_time_zone |
| Offered price | Provider-edited option/date field | Tab 4 | Price greater than 0 in the quote currency, stored as entered before any promotion; prefilled from the package standard price, or from the FR-024 treatment Base Price only where no other standard value exists | ENT-quote-option-date-price.price |
| Promotion and promotion terms | Provider-selected option/date reference; system-copied terms | Tab 4 | Optional structured FR-019 promotion. At send, its terms and discount are copied into the sent quote version and shown separately from the offered price; eligible automatic promotions are attached by the system at send | ENT-quote-option-date-price.promotion_id, ENT-quote-option-date-price.promotion_terms_snapshot, ENT-quote-option-date-price.discount_amount |
| Acceptance state | Derived from FR-005 | Tab 7 after FR-005 action | Read-only; derived from the FR-005 subquote state and never stored on the option/date-price record | ENT-subquote.acceptance_state |
| Option plan-day ID and parent Option ID | System-owned | Tab 5 | Stable identifiers; read-only | ENT-quote-option-plan-day.id, ENT-quote-option-plan-day.quote_option_id |
| Plan day number and description | Provider-edited option fields | Tab 5 | Consecutive relative day number and required description | ENT-quote-option-plan-day.day_number, ENT-quote-option-plan-day.description |
| Child-record created and updated metadata | System-owned audit metadata | Tab 7 / Audit | Applies to options, items, date-price rows, and plan days; read-only | ENT-quote-option.created_at, ENT-quote-option.updated_at, ENT-quote-option-item.created_at, ENT-quote-option-item.updated_at, ENT-quote-option-date-price.created_at, ENT-quote-option-date-price.updated_at, ENT-quote-option-plan-day.created_at, ENT-quote-option-plan-day.updated_at |
| Quote version and audit records | System-owned compliance records | Tab 7 / Audit | Complete immutable history of parent and option changes | ENT-quote.version, ENT-quote-audit.action, ENT-quote-audit.actor_id, ENT-quote-audit.created_at |

**Tab Structure**:

| Tab | Purpose | Editable Content | Completion Gate |
| --- | --- | --- | --- |
| 1. Treatment Service | Establish the single treatment shared by the quote | Treatment service | One active treatment selected |
| 2. Package Options | Select and customize the alternatives offered to the patient | One to five packages; option order; option-local inclusions and services | One to five complete option snapshots |
| 3. Grafts & Visual Plan | Record clinical facts shared by every option | Estimated grafts; visual treatment plan (graft description is system-generated and read-only) | Valid graft estimate; optional visual saved if supplied |
| 4. Dates & Pricing | Combine date-range selection and price setup into one package-driven matrix | Applicable ranges; appointment slots; prices; promotions | Every applicable option/date cell complete |
| 5. Option Treatment Plans | Define how the treatment schedule differs by package | Relative day plan for each option, prefilled from the source package | Consecutive day sequence for every option |
| 6. Clinical Details & Notes | Record remaining information shared by every option | Clinicians; common notes; common requirements; attachments | Eligible clinicians selected; text/file rules satisfied |
| 7. Review & Submit | Validate and submit the complete parent-and-options aggregate | No direct field editing; links return to the owning tab | All tab gates pass and inquiry remains active |

##### Tab 1: Treatment Service

**Purpose**: Select the treatment before package options are introduced.

| Field Name | Scope | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- | --- |
| Treatment Service | Quote | select | Yes | One admin-curated treatment shared by every option | Must be active and offered by the provider; package choices in Tab 2 are the provider's own Active packages | ENT-quote.treatment_id, ENT-quote.treatment_version |
| Technique Details | Treatment relationship | read-only text | N/A | Technique information loaded from the selected immutable Treatment version when documented in FR-024 | Never provider-editable or copied into a separate Quote field; show "Not specified" when the Treatment has no technique specifications | ENT-treatment.technique_details |

**Behavior**:

- Tab 2 is unavailable until an active treatment is selected. (REQ-004-058)
- See REQ-024-052.
- The system persists the exact Treatment ID/version relationship and loads technique details through that relationship for display and API responses.
- Changing the treatment after options exist requires confirmation. Packages are not tied to a treatment (REQ-024-101), so the package choices stay; the system must identify the option pricing and plan data that depend on the old treatment and must not silently retain or discard them. (REQ-004-059)

##### Tab 2: Package Options

**Purpose**: Choose the package alternatives and manage their quote-local content.

| Field Name | Scope | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- | --- |
| Package Options | Quote | ordered multiselect | Yes | Packages selected from the authenticated provider's active library; each selected package seeds one Quote Option | Minimum 1; maximum 5; must match Tab 1 treatment; package must be active when selected; packages are never summed into one option | ENT-quote-option.source_package_id, ENT-quote-option.source_package_version, ENT-package.status |
| Option Order | Option | reorder control | Yes | Patient-facing comparison order | Unique consecutive order within the quote | ENT-quote-option.display_order |
| Package Snapshot | Option | read-only summary | Yes | Source package identity/version, standard price, services, included travel services, and relative day plan copied into the quote | Later library edits must not alter the snapshot | ENT-quote-option.source_package_id, ENT-quote-option.source_package_version, ENT-quote-option.standard_price_snapshot, ENT-quote-option.package_name_snapshot, ENT-quote-option.package_description_snapshot, ENT-quote-option.included_services, ENT-quote-option-item.name, ENT-quote-option-plan-day.day_number, ENT-quote-option-plan-day.description |
| Edit Package Inline | Option | action | No | Opens Sub-screen 2A for the selected option | Available independently for every option | no graph field (control) |

###### Sub-screen 2A: Inline Package Editor

**Purpose**: Customize one package option for this quote without modifying the provider's reusable package library.

| Field Name | Scope | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- | --- |
| Option Name and Source | Option | read-only header | Yes | Identifies the option and its source package/version | Must remain traceable to the selected source package | ENT-quote-option.package_name_snapshot, ENT-quote-option.source_package_id, ENT-quote-option.source_package_version |
| Source Item | Option item | read-only reference | No | Identifies the package-library item from which this row was copied | Null only for a service created inside the quote | ENT-quote-option-item.source_package_item_id |
| Item Type | Option item | select | Yes | Controlled medical, travel, accommodation, transport, flight, or other service category | Must use an allowed service type | ENT-quote-option-item.item_type |
| Item Name | Option item | text | Yes | Patient-facing service name | Required; maximum 255 characters | ENT-quote-option-item.name |
| Item Description | Option item | textarea | No | Patient-facing service details | Maximum 1,000 characters | ENT-quote-option-item.description |
| Item Price | Option item | amount | No | Optional component price for transparency | Non-negative; displayed in configured currency; final offered price remains in Tab 4 | ENT-quote-option-item.price |
| Included | Option item | toggle | Yes | Whether the service is included in this package option | Explicit true or false | ENT-quote-option-item.is_included |
| Item Order | Option item | reorder control | Yes | Patient-facing order inside the option | Unique consecutive order | ENT-quote-option-item.display_order |
| Item Metadata | Option item | read-only metadata | No | Source or extension data retained by the system | Never free-form provider input | ENT-quote-option-item.metadata |
| Included Travel Services (`included_services`) | Option | checklist | No | Flight, hotel, transport, and other travel services included in this option | Stored only in the option snapshot; no cross-field dependency | ENT-quote-option.included_services |
| Add Custom Service | Option | action | No | Adds a patient-specific item with the same type, name, description, price, inclusion, and ordering fields | New item has no source package-item ID | no graph field (control) |
| Remove Service | Option item | action | No | Removes an item from this option snapshot | Confirmation required; source package remains unchanged | no graph field (control) |
| Standard Package Price | Option | read-only amount | Yes | Library price used to prefill Tab 4 | Final offered prices are edited only in Tab 4 | ENT-quote-option.standard_price_snapshot |
| Save Option Changes | Option | action | Yes | Returns the customized snapshot to Tab 2 | Must update only this Quote Option and its aggregate audit/version state | no graph field (control) |

**Behavior**:

- Providers may add, edit, include, exclude, or remove services in the option snapshot.
- Sub-screen 2A is the quote inline edit path: it edits a quote-local copy of the package that is saved only on this Quote Option and is never written back to the package library. The first inline change sets the option's inline-customised flag; the source package ID and version stay recorded for provenance.
- Closing or saving Sub-screen 2A never creates or updates a reusable `Package`, a package version, or a package-library item. Changing the reusable package is done only in the FR-024 package management screen.
- Customization examples include medical consultation, maximum graft coverage, PRP injection, Day-3 wash, lifetime warranty, language translator, hotel, local transport, airport transfer, and flight.
- Removing an option also removes its draft date-price rows and draft treatment plan after explicit confirmation; at least one option must remain before submission. (REQ-004-064)

##### Tab 3: Grafts & Visual Plan

**Purpose**: Record treatment facts that apply equally to every package option.

| Field Name | Scope | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- | --- |
| Estimated Grafts | Quote | number | Yes | Provider-entered estimate shared by every option | Provider may enter and revise a positive integer | ENT-quote.estimated_grafts |
| Graft Description | Quote | read-only text | Yes | System-generated explanation based on the fixed template (see Business Rules) and the current Estimated Grafts value | Regenerated whenever Estimated Grafts changes; providers cannot edit it directly; retained in aggregate versions | ENT-quote.graft_description |
| Visual Treatment Plan / 3D Markup | Quote | drawing/upload | No | Shared visual plan or markup | Supported file/media rules; stored in the aggregate version | ENT-quote.graft_visual_plan |

##### Tab 4: Dates & Pricing

**Purpose**: Combine treatment-date selection and pricing in one package-first configuration surface.

| Field Name | Scope | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- | --- |
| Package Option | Option | repeated section | Yes | One section per option selected in Tab 2 | All options shown in Tab 2 order | ENT-quote-option.id, ENT-quote-option.display_order |
| Applicable Treatment Dates | Option | multiselect | Yes | Patient-requested ranges for which this option is offered | At least one per option; subset of FR-003 ranges | ENT-quote-option-date-price.source_inquiry_date_range_id |
| Appointment Slot | Option/date | datetime | Yes | Appointment start for this option/date combination | Must fall within its selected range; timezone required | ENT-quote-option-date-price.appointment_at, ENT-quote-option-date-price.appointment_time_zone |
| Offered Price | Option/date | amount | Yes | Price for this package option on this date range, as entered by the provider before any promotion | Must be greater than 0; a zero or negative price blocks send; quote currency; prefilled from the package standard price, or from the FR-024 treatment Base Price only where no other standard value exists, and editable | ENT-quote-option-date-price.price |
| Promotion | Option/date | select-or-create | No | Structured promotion applied to this option/date price; the discount is shown separately from the offered price | Must resolve to a valid `PromotionProgram`; no free-text promotion; terms are copied into the quote version at send (REQ-004-100) | ENT-quote-option-date-price.promotion_id, ENT-quote-option-date-price.promotion_terms_snapshot, ENT-quote-option-date-price.discount_amount |
| Configured Currency | Quote | read-only label | Yes | Quote currency from the active FR-026 quote configuration (the FR-029 Default Currency), used across every option/date price | Never provider-editable; captured onto the quote at first send; packages carry no currency of their own; if the Default Currency changes while the draft holds prices, the draft switches to the new currency with typed numbers kept and shows a "currency changed, check your prices" banner | ENT-quote.currency_snapshot |

**Behavior**:

- The selected packages drive the screen: configure date applicability and pricing option by option until the option list is complete.
- An option may apply to all patient-requested ranges or only a subset, but at least one. The provider may leave out any option/date pairing it cannot offer.
- Each option/date-range pairing appears at most once per option. (REQ-004-061)
- Every range marked applicable must have its own appointment slot and offered price; unavailable combinations are omitted rather than priced. Each priced pairing becomes one subquote for FR-005.
- Every option/date price must be greater than 0. A zero price is blocked with an inline error on that row; a date range the clinic cannot serve is left out of that option instead of being priced at zero. (REQ-004-040)
- The FR-024 treatment Base Price is a reference-only, non-binding "starting from" value. It may prefill a new row only where no other standard value exists, such as a package standard price, and it is never read after the quote is sent.
- If the FR-029 Default Currency changes while a draft holds prices (REQ-029-053), the draft switches to the new currency, every typed number is kept unchanged, and a "currency changed, check your prices" banner is shown. The provider must acknowledge the banner before the quote can be sent.
- `included_services` comes from the corresponding Tab 2 option snapshot. After FR-005 acceptance, FR-008 derives `travel_path` from the accepted option.

##### Tab 5: Option Treatment Plans

**Purpose**: Define a different day-to-day treatment plan for each package option.

| Field Name | Scope | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- | --- |
| Package Option | Option | selector/section | Yes | Chooses the option whose plan is being edited | Every option requires a plan | ENT-quote-option.id |
| Day Number | Option | number | Yes | Relative sequential day index | Starts at 1; consecutive with no gaps | ENT-quote-option-plan-day.day_number |
| Day Description | Option | text | Yes | What happens on that relative treatment day | Required; maximum 1,000 characters | ENT-quote-option-plan-day.description |

**Behavior**:

- Each option's plan is prefilled from the relative day-by-day plan of its source package version; edits apply only to this option.
- Plans use relative day numbers because one option can be offered across multiple date ranges.
- Relative day numbers are never resolved to stored calendar dates. Downstream consumers (FR-005 comparison, FR-010 In Progress) present the plan by day number against the accepted appointment. (REQ-004-065)

##### Tab 6: Clinical Details & Notes

**Purpose**: Record remaining information that applies to all options in the parent quote.

| Field Name | Scope | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- | --- |
| Clinicians | Quote | multiselect | Yes | One or more responsible clinicians shared by every option | At least one; every clinician must be active, eligible, and belong to the provider | ENT-quote.clinician_ids |
| Common Notes | Quote | textarea | No | Additional provider information applying to every option | Maximum 5,000 characters | ENT-quote.common_notes |
| Common Requirements | Quote | textarea/repeater | No | Patient or treatment requirements shared by every option | Maximum 5,000 characters per entry; empty entries rejected | ENT-quote.common_requirements |
| Attachments | Quote | multi-file upload | No | Quote-level images, videos, or documents applying to every option | Maximum 5 files; JPG/PNG up to 5 MB each; MP4/PDF up to 10 MB each; virus scan, retention, and access rules enforced | ENT-quote.attachment_ids |

##### Tab 7: Review & Submit

**Purpose**: Review the complete quote aggregate and resolve missing information before submission.

| Field Name | Scope | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- | --- |
| Quote, Inquiry, and Provider References | Quote | read-only context | Yes | Stable quote ID plus source inquiry and authenticated provider | System-owned; must match the active quote context | ENT-quote.id, ENT-quote.inquiry_id, ENT-quote.provider_id |
| Shared Quote Summary | Quote | read-only group | Yes | Treatment, graft facts, visual plan, clinicians, notes, requirements, and attachments | Must reflect the latest saved values from Tabs 1, 3, and 6 | ENT-quote.treatment_id, ENT-quote.estimated_grafts, ENT-quote.graft_visual_plan, ENT-quote.clinician_ids, ENT-quote.common_notes, ENT-quote.common_requirements, ENT-quote.attachment_ids |
| Package Comparison | Quote aggregate | read-only cards/table | Yes | Ordered options with inclusions, date prices, and plans | Must reflect Tabs 2, 4, and 5 | ENT-quote-option.id, ENT-quote-option.display_order, ENT-quote-option.package_name_snapshot, ENT-quote-option.included_services, ENT-quote-option-date-price.price, ENT-quote-option-plan-day.day_number |
| Configured Currency | Quote | read-only label | Yes | Currency applied to all displayed prices | From the active FR-026 quote configuration; captured at first send; never provider-editable | ENT-quote.currency_snapshot |
| Calculated Price Range / Accepted Total | Quote | read-only amount | Yes | Price range before acceptance and accepted total after FR-005 acceptance | Price range derived from the complete Tab 4 matrix; accepted total written from the FR-005 acceptance snapshot | ENT-quote.calculated_price_range, ENT-quote.accepted_total |
| Commission | Quote | read-only model and value (percentage or flat rate) | Conditional | Commission model and value shown only to authorized roles, labelled "indicative, final at booking confirmation" | From the active FR-029 configuration; never provider input; the binding commission is fixed at booking confirmation | ENT-quote.commission |
| Quote Status | Quote | read-only badge | Yes | Current governed lifecycle state | System-owned enum | ENT-quote.status |
| Expiry | Quote | read-only datetime | Yes | Deadline for the complete quote; shown as "set on first send" while drafting | Captured at first send from the FR-026 quote expiry setting | ENT-quote.expires_at |
| Created and Updated | Quote | read-only metadata | Yes | System timestamps for creation and last update | System-generated | ENT-quote.created_at, ENT-quote.updated_at |
| Option Customization State | Option | read-only badge | Yes | Shows the source package and version and whether each option has been customised inline; warns when the source package has since been edited or deactivated | System-derived from option-item changes and the FR-024 package state | ENT-quote-option.is_customized, ENT-quote-option.source_package_id, ENT-quote-option.source_package_version, ENT-package.status |
| Downstream Acceptance and Lifecycle Metadata | Quote | read-only group | Conditional | Terms acknowledgment, exchange-rate lock, cancellation/supersession provenance, affiliate attribution (data owned by FR-018), and the travel path derived from the accepted option (FR-008) | Display-only; visible only when populated and authorized; never edited in Screen 1 | ENT-quote.terms_acknowledged_at, ENT-quote.locked_exchange_rate_snapshot, ENT-quote.cancellation_provenance, ENT-affiliate-attribution.reference, ENT-travel-context.travel_path |
| Version and Audit Summary | Quote aggregate | read-only links | Yes | Current version and immutable change history | Must cover parent and all option-owned records | ENT-quote.version, ENT-quote-audit.action, ENT-quote-audit.actor_id, ENT-quote-audit.created_at |
| Validation Summary | Quote aggregate | read-only checklist | Yes | Shows complete tabs and links each issue to its owning tab | No unresolved blocking issue | no graph field (read-only checklist) |
| Submit Quote | Quote aggregate | action | Yes | Submits parent and options as one transaction | Revalidate inquiry, authorization, option count, and every tab gate; blocked while any option/date price is not greater than 0 or an unacknowledged "currency changed, check your prices" banner is shown | no graph field (control) |

#### Screen 2: Quote List (Unified; no tabs)

**Purpose**: Provider views all quotes in a single unified list

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Patient ID | column | Yes | Anonymized ID | Searchable | ENT-patient.anonymized_id |
| Name | column | Yes | Partly censored name | Masking applies | ENT-patient.name |
| Age | column | No | Patient age | Number; sortable | ENT-patient.age |
| Problem/Concern | column | No | Primary concern | Filterable | ENT-inquiry.problem_concern |
| Treatment & Options | column | Yes | Shared treatment and option count | Read-only; show 1–5 options | ENT-quote.treatment_id, ENT-quote-option.id |
| Date Ranges Quoted | column | Yes | Distinct ranges offered across options | Tooltip groups ranges by option | ENT-quote-option-date-price.start_date, ENT-quote-option-date-price.end_date |
| Price Range | column | Yes | Lowest to highest option/date price | Currency formatting; derived from matrix (REQ-004-093) | ENT-quote.calculated_price_range |
| Location | column | No | Patient country | Filterable | ENT-patient.country |
| Medical Alerts | column | Yes | Alert chips | Severity colors | ENT-risk-tag.severity |
| Quoted Date | column | Yes | Quote created date | Relative formatting rules | ENT-quote.created_at |
| Action | column | Yes | Edit, Soft Delete (drafts only), View Details | State-aware; Soft Delete is offered for drafts only | no graph field (control) |
| Search/Filters | control | No | Patient/Inquiry/Treatment/Date/Status/Location/Alerts | Valid enums/ranges | no graph field (control) |

**Notes**:

- Unified list (no tabs) to reflect global case statuses
- Quotes with status "Cancelled (Inquiry Cancelled)" are displayed with greyed-out row styling and an "Inquiry Cancelled" badge; all action buttons disabled (REQ-004-098)
- Quotes with status "cancelled (other accepted)" are similarly greyed-out with "Another Quote Accepted" badge (REQ-004-098)
- The admin-authored replacement draft is not listed here; it stays hidden from the provider until it is accepted (REQ-004-048)

#### Screen 3: Quote Details Screen

**Purpose**: Inspect full quote details and act (patient-first continuation from inquiry)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Patient (Anonymized) | group | Yes | Anonymized ID, masked name, age, location | Contact hidden until payment | ENT-patient.anonymized_id, ENT-patient.name, ENT-patient.age, ENT-patient.country |
| Inquiry Context | group | Yes | Continuation data from FR-003 | Read-only | no graph field (group of the rows below) |
|  • Countries | list | Yes | Selected treatment countries | From inquiry | ENT-inquiry.treatment_countries |
|  • Problem Details | group | Yes | Concern, duration, previous treatments | From inquiry | ENT-inquiry.problem_concern, ENT-inquiry.problem_duration, ENT-inquiry.previous_treatments |
|  • Medical Alerts | chips | Yes | Critical/Standard/None | Derived from questionnaire | ENT-risk-tag.severity |
|  • Requested Date Ranges | list | Yes | All patient-requested ranges | Read-only | ENT-inquiry-date-range.start_date, ENT-inquiry-date-range.end_date |
|  • Media/Scan | links/viewer | No | Photos/videos/3D scan viewer | Read-only | ENT-inquiry.media |
| Quote Summary | group | Yes | Shared treatment facts, common notes, expiry, and option count | Read-only | ENT-quote.treatment_id, ENT-quote.common_notes, ENT-quote.expires_at, ENT-quote-option.id |
| Quote Options | comparison cards/table | Yes | Ordered package snapshots with option-local inclusions and services | One to five options | ENT-quote-option.display_order, ENT-quote-option.package_name_snapshot, ENT-quote-option.included_services, ENT-quote-option-item.name, ENT-quote-option-item.is_included |
| Option Date Prices | matrix | Yes | Applicable date ranges, appointment slots, and prices for each option | Every applicable combination shown; currency rules | ENT-quote-option-date-price.start_date, ENT-quote-option-date-price.end_date, ENT-quote-option-date-price.appointment_at, ENT-quote-option-date-price.appointment_time_zone, ENT-quote-option-date-price.price, ENT-quote.currency_snapshot |
| Option Treatment Plan | table | Yes | Package-specific relative day plan | Grouped by option; consecutive day numbers | ENT-quote-option-plan-day.day_number, ENT-quote-option-plan-day.description |
| Estimated Grafts | number | Yes | Estimated graft count | Positive integer | ENT-quote.estimated_grafts |
| Promotion | reference | No | Structured promotion applied to an option/date price, with its discount shown separately from the offered price | Read-only; shows the promotion terms copied into the sent quote version, never the live FR-019 terms | ENT-quote-option-date-price.promotion_id, ENT-quote-option-date-price.promotion_terms_snapshot, ENT-quote-option-date-price.discount_amount |
| Clinicians | list | Yes | Responsible clinicians shared by every option | At least one; each must be eligible | ENT-quote.clinician_ids |
| 3D Markup | viewer | No | Drawings over 3D image | Read-only snapshot | ENT-quote.graft_visual_plan |
| Common Notes and Requirements | text | No | Provider information applying to every option | Read-only | ENT-quote.common_notes, ENT-quote.common_requirements |
| Attachments | file list/viewer | No | Quote-level files applying to every option | Read-only; access and retention rules enforced | ENT-quote.attachment_ids |
| Expiry | datetime | Cond. | Computed deadline; empty for a draft and for the replacement quote | From admin window | ENT-quote.expires_at |
| Provider Info | group | Yes | Provider/practice info | Read-only per policy | ENT-provider.name |
| Withdrawal Reason | text | Conditional | Reason given when withdrawing a quote | Optional before acceptance; mandatory for an accepted quote (REQ-004-079); shown only when the provider chooses Withdraw | ENT-quote-audit.reason |
| Actions | actions | Yes | Edit and Soft Delete (drafts only), Withdraw (when eligible) | State policy enforced. Withdraw is offered for a `sent` quote before acceptance, and for an accepted quote only while the booking is `Accepted` or `Confirmed`, before check-in, with no provider-fault marker. Withdrawing an accepted quote opens a confirmation that names the consequence: the booking goes to the admin for a transfer or refund. In every other state the Withdraw action is hidden and a short note says the quote can no longer be withdrawn (REQ-004-070, REQ-004-079, REQ-004-109) | no graph field (control) |
| Audit/Version | modal | Yes | Version history and audit log | Immutable audit | ENT-quote-version.version, ENT-quote-audit.action |

**Notes**:

- UI may use a tabbed interface defaulting to Patient tab, then Inquiry, then Quote, then Audit
- Patient-first ordering ensures natural continuation from inquiry to quote data
- If quote is in "Cancelled (Inquiry Cancelled)" status, display a prominent "Inquiry Cancelled" banner at the top of the detail view; all edit/delete actions disabled; quote data remains read-only for reference (REQ-004-098)
- If provider was actively drafting when inquiry was cancelled, the banner appears on next save/refresh with message: "This inquiry was cancelled by the patient. Your draft can no longer be submitted."
- When an admin closed or cancelled the inquiry, the banner wording is neutral: "This inquiry was closed. Your quote can no longer be changed." (REQ-004-098)

### Patient Platform (Read-only for this module)

#### Screen 4: Quote Review

**Purpose**: Patient reviews parent quotes and their subquotes; acceptance of one subquote is governed by FR-005

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Quote List | list | Yes | Parent quotes grouped by inquiry and provider | Read-only; separate quote and option counts | ENT-quote.id, ENT-quote.inquiry_id, ENT-quote.provider_id |
| Treatment | text | Yes | Selected treatment | Read-only | ENT-quote.treatment_id |
| Quote Options | comparison cards/table | Yes | One to five package options within the selected quote | Read-only in FR-004; selection governed by FR-005 | ENT-quote-option.display_order, ENT-quote-option.package_name_snapshot |
| Price Breakdown | matrix | Yes | Price for every applicable option/date combination, with any promotion discount shown separately | Currency rules | ENT-quote-option-date-price.start_date, ENT-quote-option-date-price.end_date, ENT-quote-option-date-price.price, ENT-quote-option-date-price.discount_amount, ENT-quote.currency_snapshot |
| Inclusions and Services | list | Yes | Snapshot of inclusions and quote-local customizations | Grouped by option; read-only | ENT-quote-option.included_services, ENT-quote-option-item.name, ENT-quote-option-item.is_included |
| Treatment Plan | table | Yes | Different day-to-day plan for each option | Grouped by option; read-only | ENT-quote-option-plan-day.day_number, ENT-quote-option-plan-day.description |
| Attachments | file list/viewer | No | Quote-level supporting files | Read-only; patient access rules enforced | ENT-quote.attachment_ids |
| Status | badge | Yes | Parent quote status mapped from the Key Entities enum: Sent (shown as Awaiting Decision), Accepted, Expired, Withdrawn, Cancelled (Inquiry Cancelled), Cancelled (Other Accepted), and Cancelled (Provider Status) shown as Offer Unavailable; each subquote also shows its FR-005 state, including Not Selected | Enum validation; drafts and archived quotes are never shown to patients; visual treatment per state (e.g., greyed-out for cancelled/expired) (REQ-004-075, REQ-004-097) | ENT-quote.status, ENT-subquote.acceptance_state |
| Expiration Timer | timer | Cond. | Countdown to expiry; none for the replacement quote | From admin window | ENT-quote.expires_at |
| Provider Info | group | Yes | Allowed provider details | Privacy rules | ENT-provider.name |
| Actions | actions | Yes | Accept one subquote (FR-005); there is no parent-level Accept or Decline action | State & confirmation rules owned by FR-005 (REQ-004-095) | no graph field (control) |
| Notifications | note | No | New/updated/expired indicators | Read-only | no graph field (read-only indicator) |

**Governance Note**: This screen’s field/visual specification is defined here in FR-004, but the end-to-end patient quote comparison and acceptance flows (including edge cases, blocking rules, and booking handoff) are governed primarily by **FR-005: Quote Comparison & Acceptance (P-02)**. FR-005 may extend or refine the actions on this screen while preserving the privacy constraints and data structure specified in FR-004.

### Admin Platform

#### Screen 5: Quote List (Admin)

**Purpose**: Admin lists and filters all quotes (multiple providers per inquiry)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Global Quote Table | table | Yes | All quotes with columns & filters | Admin-only | no graph field (table of the columns below) |
| Patient ID | column | Yes | Anonymized ID | Searchable | ENT-patient.anonymized_id |
| Name | column | Yes | Partly censored name | Masking applies | ENT-patient.name |
| Age | column | No | Patient age | Number; sortable | ENT-patient.age |
| Problem/Concern | column | No | Primary concern | Filterable | ENT-inquiry.problem_concern |
| Treatment & Options | column | Yes | Shared treatment and option count | Read-only; show 1–5 options | ENT-quote.treatment_id, ENT-quote-option.id |
| Date Ranges Quoted | column | Yes | Distinct ranges offered across options | Tooltip groups ranges by option | ENT-quote-option-date-price.start_date, ENT-quote-option-date-price.end_date |
| Price Range | column | Yes | Lowest to highest option/date price | Currency formatting; derived from matrix | ENT-quote.calculated_price_range |
| Location | column | No | Patient country | Filterable | ENT-patient.country |
| Medical Alerts | column | Yes | Alert chips | Severity colors | ENT-risk-tag.severity |
| Quoted Date | column | Yes | Quote created date | Relative formatting rules | ENT-quote.created_at |
| Provider | column | Yes | Provider/clinic | Filterable | ENT-provider.name |
| Actions | column | Yes | Restore/Archive/View Detail | State-aware; Restore and Archive are hidden for `accepted` quotes. Restore is offered only for an expired quote or a quote archived from `draft` or `sent`; any other archived quote shows no Restore and a short note. A failed guard (inquiry not open, provider not `Active`, active acceptance, provider-fault marker) blocks the restore with a message that names it (REQ-004-077, REQ-004-105) | no graph field (control) |
| Search/Filters | control | No | Patient/Inquiry/Treatment/Date/Status/Location/Alerts/Provider. Status filter includes: draft, sent, expired, withdrawn, archived, accepted, cancelled_other_accepted, cancelled_inquiry_cancelled, cancelled_provider_status | Valid enums/ranges | no graph field (control) |
| Inquiry Grouping | control | Yes | Default: grouped by inquiry | Toggle grouping (REQ-004-108) | no graph field (control) |
| Multi-Quote Cue | badge/icon | No | Visual cue for multiple quotes in inquiry | Shows count or indicator | no graph field (read-only indicator) |
| Audit Trail | modal | Yes | Per-quote audit (who/what/when/prev value) | Immutable | ENT-quote-audit.action, ENT-quote-audit.actor_id, ENT-quote-audit.before, ENT-quote-audit.created_at |
| Version History | modal | Yes | Full version history | Immutable | ENT-quote-version.version, ENT-quote-version.created_at |

#### Screen 6: Quote Detail (Admin)

**Purpose**: Admin views complete quote with inquiry continuation

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Quote Selector | dropdown/list | Yes | Switch between quotes for this inquiry | Must belong to same inquiry | ENT-quote.id |
| Quote Summary | group | Yes | Shared treatment facts, common notes, expiry, and option count | Read-only | ENT-quote.treatment_id, ENT-quote.common_notes, ENT-quote.expires_at, ENT-quote-option.id |
| Quote Options | comparison cards/table | Yes | Package snapshots, option-local inclusions, and source-package provenance | One to five options | ENT-quote-option.display_order, ENT-quote-option.package_name_snapshot, ENT-quote-option.included_services, ENT-quote-option-item.name, ENT-quote-option-item.is_included, ENT-quote-option.source_package_id, ENT-quote-option.source_package_version |
| Option Date Prices | matrix | Yes | Applicable date ranges, appointment slots, and prices by option | Complete for every applicable combination | ENT-quote-option-date-price.start_date, ENT-quote-option-date-price.end_date, ENT-quote-option-date-price.appointment_at, ENT-quote-option-date-price.appointment_time_zone, ENT-quote-option-date-price.price, ENT-quote.currency_snapshot |
| Option Treatment Plans | table | Yes | Relative day plan grouped by package option | Consecutive day numbers per option | ENT-quote-option-plan-day.day_number, ENT-quote-option-plan-day.description |
| Estimated Grafts | number | Yes | Estimated graft count | Positive integer | ENT-quote.estimated_grafts |
| Promotion | reference | No | Structured promotion applied to an option/date price, with its discount shown separately from the offered price | Read-only; shows the promotion terms copied into the sent quote version, never the live FR-019 terms | ENT-quote-option-date-price.promotion_id, ENT-quote-option-date-price.promotion_terms_snapshot, ENT-quote-option-date-price.discount_amount |
| Clinicians | list | Yes | Responsible clinicians shared by every option | At least one; each must be eligible | ENT-quote.clinician_ids |
| 3D Markup | viewer | No | Drawings over 3D image | Read-only snapshot | ENT-quote.graft_visual_plan |
| Common Notes and Requirements | text/list | No | Provider information applying to every option | Read-only | ENT-quote.common_notes, ENT-quote.common_requirements |
| Attachments | file list/viewer | No | Quote-level supporting files | Read-only; access and retention rules enforced | ENT-quote.attachment_ids |
| Expiry | datetime | Cond. | Computed deadline; empty for a draft and for the replacement quote | From admin window | ENT-quote.expires_at |
| Provider Info | group | Yes | Provider/practice info | Read-only | ENT-provider.name |
| Inquiry Context | group | Yes | Countries, problem, alerts, ranges, media/scan | From FR-003 | ENT-inquiry.treatment_countries, ENT-inquiry.problem_concern, ENT-risk-tag.severity, ENT-inquiry-date-range.start_date, ENT-inquiry-date-range.end_date, ENT-inquiry.media |
| Audit Trail | log | Yes | Full change history | Immutable | ENT-quote-audit.action |
| Version History | list | Yes | Quote versions | Immutable | ENT-quote-version.version |

#### Screen 7: Admin Inline Quote Edit

**Purpose**: Admin performs inline edits with audit on draft, sent, and accepted quotes (price, currency, and promotion stay read-only once accepted)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Quote Selector | dropdown/list | Yes | Select target quote under inquiry | Must belong to same inquiry; the replacement draft is not offered, because Screen 8 is its only edit surface (REQ-004-048) | ENT-quote.id |
| Quote Option | selector | Yes | Select the package option being edited | Must belong to the selected quote | ENT-quote-option.id |
| Option/Date Price | matrix | Cond. | Edit applicability, appointment slot, or price for an option/date combination | Reason required; matrix must remain complete | ENT-quote-option-date-price.source_inquiry_date_range_id, ENT-quote-option-date-price.appointment_at, ENT-quote-option-date-price.appointment_time_zone, ENT-quote-option-date-price.price |
| Package Inclusions | inline option editor | Cond. | Edit the option snapshot without changing the package library | Reason required | ENT-quote-option.included_services, ENT-quote-option-item.name, ENT-quote-option-item.is_included |
| Estimated Grafts | number | Cond. | Adjust graft count. Saving a new value regenerates Graft Description from the fixed template (see Business Rules); the prior text stays in quote history | Positive integer; reason required (REQ-004-101) | ENT-quote.estimated_grafts, ENT-quote.graft_description |
| Option Items | repeater | Cond. | Add/edit/remove items within the selected option snapshot | Same fields as Sub-screen 2A — Item Name, Item Type, Included flag, Item Order, and Item Price (optional); item order consecutive with no gaps; reason required | ENT-quote-option-item.name, ENT-quote-option-item.item_type, ENT-quote-option-item.is_included, ENT-quote-option-item.display_order, ENT-quote-option-item.price |
| Treatment Plan (per-day) | repeater | Cond. | Edit the selected option's relative day plan | Consecutive day numbers; reason required | ENT-quote-option-plan-day.day_number, ENT-quote-option-plan-day.description |
| Promotion | select-or-create | Cond. | Add, replace, or remove the structured promotion on an option/date price of a draft or sent quote. Inline create permitted with `scope = AD_HOC_QUOTE_BOUND` per FR-019 Screen 9 Mode 2 | Must resolve to a valid PromotionProgram id or null; reason required; the change creates a new quote version into which the current promotion terms are copied (REQ-004-099, REQ-004-100) | ENT-quote-option-date-price.promotion_id, ENT-promotion-program.scope |
| Notes | textarea | No | Admin note | Stored with audit | ENT-quote-audit.note |
| Clinicians | multiselect | Cond. | Change the shared clinician assignments | At least one; each must be active, eligible, and belong to the provider; reason required | ENT-quote.clinician_ids |
| Attachments | multi-file upload | Cond. | Add or remove quote-level supporting files | File/access rules and reason required | ENT-quote.attachment_ids |
| Audit Reason | textarea | Yes | Reason for change | Required for any edit | ENT-quote-audit.reason |

**Notes**:

- All inline edits auditable (who/when/before/after, reason). An admin edit of a sent quote creates a new quote version and emits `quote.updated` when that version is re-sent; draft edits emit nothing (REQ-004-049, REQ-004-069)
- Screen 7 is available for `draft`, `sent`, and accepted quotes. After acceptance, price, currency, and promotion are read-only; every other field can be changed, each change needs a mandatory reason, and it is stored as a new version beside the acceptance snapshot, which stays unchanged. Payment records are never changed. A provider cannot edit an accepted quote; the provider's treatment-detail changes (plan, clinicians, grafts) are made only through FR-010 with audit and patient notice. Expired, withdrawn, archived, and cancelled quotes are read-only. While the booking carries a provider-fault marker, pending or cancelled with the marker, Screen 7 edits of the accepted quote are blocked, except admin notes (REQ-004-109).

#### Screen 8: Admin Replacement Quote Authoring

**Purpose**: Admin authors a quote for the replacement provider during an FR-006 provider-fault transfer (Workflow 7)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Transfer Context | group | Yes | Inquiry, booking, provider-fault cause, and the AcceptanceEvent it replaces with its snapshot | Read-only; opened only from the FR-006 transfer; the booking must carry the provider-fault marker, pending or closed with `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated`, and be `Accepted`, `Confirmed`, or `Cancelled` with that marker before treatment started (REQ-004-081) | ENT-booking.status, ENT-booking.closure_cause, ENT-booking.support_required, ENT-quote.inquiry_id, ENT-quote.replacement_for_acceptance_event_id, ENT-acceptance-event.snapshot |
| Replacement Provider | reference | Yes | Provider chosen in the FR-006 transfer | Read-only here; must be `Active` and must not be the provider at fault | ENT-quote.provider_id |
| Currency | text | Yes | Quote currency from the active FR-026 quote configuration (FR-029 Default Currency), captured at the first save | Read-only; fixed after the first save (REQ-004-082) | ENT-quote.currency_snapshot |
| Treatment | select | Yes | Shared treatment for the replacement quote | From the admin-curated catalog; prefilled from the original acceptance | ENT-quote.treatment_id |
| Quote Options | inline option editor | Yes | One to five options seeded from the replacement provider's active packages | Same option rules as Screen 1; quote-local copies only | ENT-quote-option.package_name_snapshot, ENT-quote-option.source_package_id, ENT-quote-option.included_services, ENT-quote-option-item.name, ENT-quote-option-item.is_included |
| Option/Date Price | matrix | Yes | Date range, appointment date/time, time zone, and price for each applicable option/date pairing | Price greater than 0; date range from the inquiry; appointment within the range | ENT-quote-option-date-price.source_inquiry_date_range_id, ENT-quote-option-date-price.appointment_at, ENT-quote-option-date-price.appointment_time_zone, ENT-quote-option-date-price.price |
| Estimated Grafts | number | Yes | Shared graft estimate | Positive integer; Graft Description regenerated from the template | ENT-quote.estimated_grafts, ENT-quote.graft_description |
| Treatment Plan (per-day) | repeater | Yes | Relative day plan per option | Consecutive day numbers | ENT-quote-option-plan-day.day_number, ENT-quote-option-plan-day.description |
| Clinicians | multiselect | Yes | Shared clinicians of the replacement provider | At least one; each active, eligible, and belonging to that provider | ENT-quote.clinician_ids |
| Notes and Attachments | text/files | No | Common notes, requirements, and supporting files | Same limits as Screen 1 | ENT-quote.common_notes, ENT-quote.common_requirements, ENT-quote.attachment_ids |
| Adjustment Reason | textarea | Yes | Why the package or price differs from the original acceptance, or why it is unchanged | Required; stored in the quote audit | ENT-quote-audit.reason |
| Actions | buttons | Yes | Save Draft, Save and Continue to Acceptance, Cancel | Save and Continue validates every field and returns to the FR-006 transfer to record the acceptance | no graph field (control) |

**Notes**:

- Confirmation: Save and Continue shows a confirmation that summarises the replacement provider, options, prices, and appointment, and states that the patient will not compare this quote and that the admin records the acceptance next.
- Audit: every save writes a quote audit entry with admin, time, before and after values, and the adjustment reason; the quote is marked admin-authored for a replacement and linked to the AcceptanceEvent it replaces.
- Notices: authoring the quote sends no notice. When the replacement acceptance is recorded, the patient receives `booking.scheduled` and the replacement provider receives `quote.accepted`; the patient and admin are told of the transfer through FR-006 `booking.provider_fault_replacement`. (REQ-004-083)
- Screen 8 is unavailable for a booking in `In Progress` or later stages and once a replacement acceptance has been recorded for this transfer. The original acceptance stays the active one until then. (REQ-004-080, REQ-004-110)
- Price: the admin sets each option/date price directly. Screen 8 offers no promotion field, no automatic FR-019 promotion attaches, and no promotion usage reservation is taken.
- Expiry: the replacement quote has no expiry and never emits `quote.expiring_soon` or `quote.expired`. It stays a `draft`, even after Save and Continue, hidden from the replacement provider and the patient, and is not listed on Screen 2, Screen 4, or Screen 7 until the admin records the acceptance in FR-006. At that moment it moves from `draft` through `sent` to `accepted` and its first-send time is recorded. (REQ-004-048, REQ-004-050, REQ-004-082)
- Currency: captured from the active FR-026 quote configuration at the first save, shown in the Currency row, and fixed after that. (REQ-004-082)
- Blocked: when a precondition fails, Screen 8 is blocked with a message that names the failed check. (REQ-004-081)
- Unaccepted drafts: a replacement draft that is never accepted is archived by the 7-day draft rule counted from its last edit, and is cancelled without notice when an admin closes or cancels the inquiry. The inquiry stays `supportRequired`; the admin may open Screen 8 again to author another replacement quote, close the inquiry with Close inquiry on FR-006 Screen 6 when the booking is already `Cancelled` with the marker, or cancel through FR-006 Alternative Flow B2 (Screen 9) when the fault is still pending. (REQ-004-050, REQ-004-111)

## Business Rules

- Quotes MUST reference distributed inquiry ID and be linked to original patient object (REQ-004-006)
- Quote data MUST append to inquiry data; no reduction or overwriting of inquiry-supplied fields. Downstream stages inherit upstream data. (REQ-004-006)
- Only assigned clinic staff may submit/edit quotes for assigned inquiries (REQ-004-053)
- Treatment type selection MUST use admin-curated treatment catalog; no free text. A treatment the provider has set to Not Offered blocks new quotes only: existing drafts and sent quotes are unchanged and a draft can still be sent (REQ-004-054, REQ-024-006)
- Graft/quantity, option/date prices, and scheduled slots MUST be present and valid (REQ-004-055)
- See REQ-004-040.
- See REQ-004-014.
- See REQ-004-015.
- Every Quote Option MUST originate from a package that is active in the authenticated provider's package library when it is selected. If the source package is later edited or deactivated, existing draft and sent options keep their snapshot; a draft may still be submitted, and Tab 7 shows a warning that the source package has changed or is inactive (REQ-004-056)
- See REQ-004-033, REQ-004-057.
- Package selection occurs after the shared treatment is selected; every option in the quote MUST use that parent treatment (REQ-004-058)
- See REQ-024-052.
- See REQ-004-016, REQ-004-017.
- Package-library changes after snapshot creation MUST NOT alter existing draft or sent options unless the provider explicitly replaces the source package and confirms a new snapshot. Patients see only the option's own copy of the package content, never the live library package (REQ-004-060)
- **Package library edits and quote inline edits**: There are two distinct edit paths. (1) Editing a package in the FR-024 package management screen changes the reusable library package: each saved edit creates a new package version, earlier versions stay read-only, and existing quotes never change. (2) Editing a package inside quote creation (Sub-screen 2A, Tab 5, and Tab 4 prices) changes only a quote-local copy saved on that Quote Option; it is never written back to the library and never creates a package version. Each Quote Option records its source package ID, source package version, and whether it was customised inline (REQ-004-034)
- See REQ-004-018, REQ-004-033, REQ-004-061.
- See REQ-004-020.
- See REQ-004-026.
- See REQ-004-025, REQ-004-036, REQ-029-053.
- See REQ-004-043.
- See REQ-004-044.
- See REQ-004-036, REQ-004-066, REQ-004-067, REQ-004-105.
- Providers MAY enter and revise the Estimated Grafts value. The system MUST automatically generate and regenerate the Graft Description from the fixed template text below and the current Estimated Grafts value. Providers MUST NOT directly edit the Graft Description. Earlier Graft Description text is kept in quote history. (REQ-004-028)
- **Graft Description template**: The text is written once here, with no admin setting and no admin screen: "The provider estimates about {Estimated Grafts} grafts for this treatment. This is an estimate, not a final count." The placeholder is replaced by the current Estimated Grafts value. (REQ-004-028)
- Included services, custom services, date applicability/pricing, promotions, and the day-to-day plan belong to the Quote Option or its option/date price record (REQ-004-063)
- See REQ-004-030.
- See REQ-004-030.
- See REQ-004-009, REQ-004-076.
- See REQ-004-007.
- See REQ-004-005, REQ-004-037, REQ-004-084, REQ-004-085.
- See REQ-004-068.
- See REQ-004-014, REQ-004-030.
- Discounts are provider-managed with no admin review. A percentage discount above the maximum discount value (the FR-019 setting, starts at 50 percent) is refused as a hard cap; a fixed-amount discount has no cap (REQ-004-090, REQ-019-114)
- **Promotions on quotes**: The offered price is stored as entered by the provider, and any promotion discount is stored and shown separately. At each send, the system copies the terms and discount value of every attached promotion into the sent quote version; later edits to the FR-019 promotion never change a sent quote. At send, the system also attaches at most one automatic FR-019 promotion per quote to each eligible option/date-price row; when several automatic promotions qualify, the FR-019 priority order picks one. The accepted price is the price after promotion, which FR-005 freezes into the acceptance snapshot; FR-004 never changes it after acceptance. A sent quote carrying an automatic promotion holds exactly one reserved use of that promotion's usage limit, and a re-send of a new version keeps that reservation rather than adding a second one; the reservation is released when the quote expires, is withdrawn, is archived, or ends not selected or cancelled, or when the accepted row does not carry the promotion (`not_applied`), and the use is consumed when the accepted row carries it, so the usage limit can never be exceeded. When an admin restores an expired quote, the system re-checks the promotion's validity and usage limit and takes a new reservation only when the quote holds none; if the limit is used up or the promotion has ended, the restore is blocked with a message and the provider may send a new quote instead. An automatic promotion with no uses left is not eligible and is not attached (REQ-004-035, REQ-004-042, REQ-004-089, REQ-004-105)
- **Commission display**: Owned by FR-029 (REQ-029-051), including the binding commission fixed at booking confirmation. The quote only displays the commission model and value (percentage or flat rate) as an indicative figure labelled "indicative, final at booking confirmation"
- All notifications MUST comply with platform notfication/audit/logging rules (REQ-004-091)
- GDPR/data compliance: all quote objects are archived; retention follows the system PRD, Platform-Wide Rules: One 10-year retention period (REQ-004-092)
- Patient information remains censored at this stage until payment confirmation; only anonymized identifiers and allowed fields are visible to providers. The platform-wide rule "Patient identity hidden until booking confirmation" owns this (REQ-SYS-001; the Patient ID plus masked name display follows FR-022 REQ-022-026).
- See REQ-004-018.
- Only a provider in `Active` status may create, edit, or submit quotes. A provider's effective `Suspended` or `Deactivated` status revokes quote submission and cancels that provider's unaccepted parent quotes under Workflow 3 and FR-015 A5/Screen 4; the provider-caused cause is distinct from patient inquiry cancellation and Payment Window Expired. An already-accepted quote is never cancelled this way; FR-006 handles it through the provider-fault transfer. (REQ-004-031, REQ-004-032, REQ-004-073, REQ-004-074)
- See REQ-004-004, REQ-004-079.
- See REQ-004-048, REQ-004-050, REQ-004-078.
- While the booking carries a provider-fault marker, pending or cancelled with the marker, the accepted quote is frozen for provider edits, admin edits other than admin notes, admin restore, and a second withdrawal; the replacement quote on Screen 8 is the only quote write allowed (REQ-004-109). An active acceptance is the latest AcceptanceEvent on the inquiry that has no supersession record (REQ-004-110). A replacement draft is cancelled without notice when an admin closes or cancels the inquiry (REQ-004-111).
- `confirmed` is a booking status owned by FR-006, never a quote status; an accepted quote stays `accepted`. (REQ-004-071, REQ-004-087)
- System MUST verify parent inquiry is not in Cancelled status before accepting quote creation or submission. If inquiry is cancelled mid-draft (race condition), system rejects submission with error "Inquiry no longer active" and locks the draft with "Inquiry Cancelled" banner. See FR-003 Workflow 5 edge case. (REQ-004-051, REQ-004-072)
- **Restricted recipient mode**: If the inquiry was created via an FR-037 monitoring-case conversion with an active exclusive provider assignment (REQ-037-029, Business Rule 7; see FR-003 Workflow 2 Alternative Flow B3), only that assigned provider may create quotes for the inquiry, including any additional parent quote. Any other provider attempting to open the inquiry for quote creation is blocked with error "This inquiry is restricted to its assigned provider." The restriction does not change the other workflows (editing, expiry, withdrawal, admin oversight) on quotes that already exist. FR-038 is self-service and does not create an FR-004 inquiry or provider assignment. (REQ-004-052)
- Rate limiting on edit/submit endpoints to prevent abuse
- Update acceptance consumers to identify one Quote Option and one option/date price; do not infer acceptance from the parent quote alone
- Encrypt quote data at rest and in transit; enforce RBAC for provider staff (REQ-004-009)

## Functional Requirements Summary

### Core Requirements

- **REQ-004-001**: Providers MUST create, edit, and submit parent quotes with one shared immutable Treatment-version relationship and one to five package-based Quote Options. Technique details MUST be loaded read-only through that relationship and MUST NOT be duplicated as provider-entered Quote data.
- **REQ-004-002**: System MUST enforce the admin-controlled FR-026 expiry window (default 48h), captured at first send, and compute the deadline per sent quote. The only renewal is the admin restore of an expired quote (REQ-004-105). The admin-authored replacement quote has no expiry (REQ-004-050).
- **REQ-004-003**: System MUST cancel every other parent quote for the same inquiry as `cancelled_other_accepted` upon one subquote acceptance by the patient. Each sent parent quote MUST produce one not-selected notice per parent quote; unsent drafts MUST be cancelled silently without notice. The not-selected notice is the FR-030 `quote.accepted` event with `outcome` = `competing_parent_cancelled_other_subquote_accepted` (REQ-030-038). The admin-authored replacement acceptance of a provider-fault transfer MUST NOT run this cascade (REQ-004-082).
- **REQ-004-004**: System MUST support provider withdrawal after acceptance, only while the booking is `Accepted` or `Confirmed`, before check-in, and without a provider-fault marker, by moving the parent quote to `withdrawn`, keeping the AcceptanceEvent and snapshot unchanged, and handing the case to the FR-006 provider-fault transfer, with full audit and the mandatory `quote.withdrawn` notice.
- **REQ-004-005**: Admin MUST be able to inline edit policy-bound fields of `draft` and `sent` quotes with required reason and re-notifications. After a subquote is accepted, an admin MUST still be able to change any quote field except price, currency, and promotion (the date range and treatment details can be changed), with a mandatory reason and full before and after history; the change MUST be stored as a new version beside the acceptance snapshot, which stays unchanged, and payment records MUST NOT change. While the booking carries a provider-fault marker, this admin edit right is suspended, except for admin notes (REQ-004-109). A replacement draft is edited only on Screen 8 and is not opened on Screen 7 (REQ-004-048).

### Data Requirements

- **REQ-004-006**: Quotes MUST reference original inquiry and patient; quote data appends, never overwrites inquiry data.
- **REQ-004-007**: All quote edits and state transitions MUST be versioned and auditable.

### Security & Privacy Requirements

- **REQ-004-008** (retired): Hiding patient identity from providers until payment confirmation is owned by the single platform-wide identity-protection Rule in the system PRD, "Patient identity hidden until booking confirmation" (REQ-SYS-001). FR-004 cites it.
- **REQ-004-009**: All quote data MUST be encrypted at rest and in transit; soft deletes only.

### Integration Requirements

- **REQ-004-010**: Module MUST integrate with FR-003 for inquiry context and FR-020 for notifications.
- **REQ-004-011**: Admin settings (quote expiry window, quote-expiring-soon lead time, and quote currency) MUST be applied from the FR-026 quote configuration.

### Clarifications

- **REQ-004-012**: Money handling for provider withdrawal after acceptance follows the FR-006 provider-fault placeholder; exact refund and payment-allocation mechanics are owned by FR-007, FR-007B, and FR-017.

### Cancellation Cascade Requirements

- **REQ-004-013** (retired): The inquiry cancellation cascade onto draft, sent, and expired quotes is owned by FR-003 (REQ-003-013). FR-004 applies it as described in Workflow 3 and produces `quote.cancelled_inquiry` at the Quote Stage.
- **REQ-004-031**: System MUST revalidate provider status at quote creation and submission and MUST reject quote submission by a `Suspended` or `Deactivated` provider from the effective time, including in-flight requests.
- **REQ-004-032**: When a provider becomes `Suspended` or `Deactivated`, System MUST cancel that provider's unaccepted parent quotes with status `cancelled_provider_status` and `cancellationProvenance` `ProviderSuspended` or `ProviderDeactivated`, once per parent quote rather than per option or option/date alternative, without rewriting the AcceptanceEvent, accepted IDs/versions, or quote-local package snapshots, and without reclassifying terminal or completed history. An accepted parent quote MUST NOT receive `cancelled_provider_status`; it keeps `accepted` and is handled by the FR-006 provider-fault transfer. Processing MUST be deduplicated per provider-status event and quote.

### Quote Option Requirements

- **REQ-004-014**: System MUST allow the same provider to create multiple parent quotes for one active inquiry; every quote retains an independent lifecycle, expiry, version history, and audit history.
- **REQ-004-015**: Each quote MUST contain between one and five ordered Quote Options, and submission MUST be blocked outside that range.
- **REQ-004-016**: Each Quote Option MUST retain the selected provider package ID/version and a stable, versioned quote-owned snapshot of its inclusions and standard values. The parent quote MUST retain the Treatment ID/version that every option belongs to.
- **REQ-004-017**: Providers MUST be able to customize every selected package inline for the current quote without updating or creating reusable package-library records, and without creating a new package version.
- **REQ-004-018**: Each Quote Option MUST define at least one applicable patient-requested date range and a price, appointment date/time, timezone, and optional structured promotion for every applicable option/date combination. Pairings the provider cannot offer MAY be left out.
- **REQ-004-019**: Each Quote Option MUST own a separate ordered day-to-day treatment plan using consecutive relative day numbers.
- **REQ-004-020**: Estimated grafts, graft description, visual treatment plan, clinicians, common notes, and common requirements MUST remain shared parent-quote fields.
- **REQ-004-021**: Quote version and audit records MUST capture the complete parent-and-options aggregate atomically, including option additions/removals, package snapshots, inclusion changes, date-price changes, and option plan changes.
- **REQ-004-022**: FR-004 MUST expose stable identifiers for the parent quote, Quote Option, and option/date price so FR-005 can record exactly one accepted option/date combination. FR-004 versions the complete parent quote aggregate atomically; therefore, the FR-005 `subquoteVersion` MUST equal the owning parent quote's current `QuoteVersion`. Quote Options and option/date-price records do not have independent revision counters.
- **REQ-004-023**: Provider Quote Creation/Edit MUST use the ordered seven-tab flow defined in Screen 1, including Sub-screen 2A for quote-local package editing and one combined Dates & Pricing tab driven by the selected package options.
- **REQ-004-024**: Every Quote, Quote Option, option item, option/date price, and option plan-day field MUST follow the Screen 1 Quote Data Ownership Matrix, with exactly one provider-editing surface or an explicit read-only/system-derived owner.
- **REQ-004-025**: Quote currency MUST come from the active FR-026 quote configuration (the FR-029 Default Currency), MUST NOT be provider input, and MUST be captured on the quote at first send so historical prices retain their original currency. The admin-authored replacement quote captures it at its first Screen 8 save (REQ-004-082).
- **REQ-004-026**: Providers MUST be able to attach quote-level supporting files that apply to every option; file security, access, audit, and retention rules MUST be enforced.
- **REQ-004-027**: A quote MUST support one or more eligible clinician assignments shared across every option. When a team member is removed or suspended, has a role change that takes away the rights needed to work their open items, or is force-suspended or force-removed by an admin, the system rewrites the clinician list of every draft, sent and accepted quote of that provider that names the member to the replacement clinician chosen at that moment, as a system change recorded in the quote's audit history; reactivating the member does not give the quotes back (REQ-009-191).
- **REQ-004-028**: Graft description MUST be generated from the fixed template text written in this PRD (Business Rules, "Graft Description template") and the estimated graft count, displayed read-only, and versioned with the quote. There is no admin setting for the template.
- **REQ-004-029**: System-owned identifiers, lifecycle status, price summaries, commission, timestamps, customization state, and version/audit metadata MUST be visible only where authorized and MUST NOT be provider-editable.
- **REQ-004-030**: Quote-amount analytics MUST be computed from the accepted option/date price only. Unaccepted quotes MUST be excluded from amount metrics and counted once as a parent response in volume and conversion metrics; Quote Options MUST NOT be counted as responses. The counting boundary is the parent quote: each submitted parent quote MUST be counted once, on its first successful submission; several parent quotes from one provider are separate responses; and drafts, edits, re-sends, aggregate versions, Quote Options, and option/date-price records MUST NOT add responses. Response, option, subquote, acceptance, and confirmed-booking counts are different grains and MUST NOT be interchanged. FR-014 reads this Rule and keeps its references to it.

### Quote Lifecycle and Pricing Requirements

- **REQ-004-033**: A quote MUST be built from one treatment plus one to five Active packages. Each selected Active package MUST seed exactly one alternative Quote Option (maximum five per parent quote), never summed with another package. The package standard price MUST prefill each applicable option/date-price row, and the package's relative day plan MUST prefill the option plan.
- **REQ-004-034**: Editing a package in the FR-024 package management screen MUST change only the library (as a new package version), and editing inside quote creation MUST change only a quote-local copy that is never written back. Each Quote Option MUST record its source package ID, source package version, and an inline-customised flag.
- **REQ-004-035**: System MUST store the offered price as entered and any promotion discount separately, MUST copy the terms of every attached promotion into the sent quote version at send, and MUST attach at most one automatic FR-019 promotion per quote to each eligible option/date-price row at send, chosen by the FR-019 priority order when several qualify. Later FR-019 promotion edits MUST NOT change a sent quote.
- **REQ-004-036**: System MUST capture the quote expiry and quote currency read-only at first send from the FR-026 quote configuration. Drafts MUST carry neither, and there MUST be no per-quote expiry extension other than the admin restore of an expired quote (REQ-004-105). The admin-authored replacement quote is the exception: it has no expiry and captures its currency at its first Screen 8 save (REQ-004-082).
- **REQ-004-037**: After a subquote is accepted, System MUST block every FR-004 quote edit by providers; their treatment-detail changes (plan, clinicians, grafts) MUST go through FR-010. Admin edits after acceptance follow REQ-004-005 and are blocked, except admin notes, while the booking carries a provider-fault marker (REQ-004-109). Price, currency, and promotion MUST never change after acceptance. An accepted parent quote MUST never be reopened, expired, or restored to an acceptable state, including after `Payment Window Expired`, and no new parent quote MAY be created or sent for an inquiry with an active acceptance (REQ-004-110), except the admin-authored replacement quote of REQ-004-048.
- **REQ-004-038**: The Quote Option appointment date/time and time zone, together with the provider, MUST be the key FR-006 uses for the slot hold placed at acceptance; FR-004 MUST NOT create an appointment record.
- **REQ-004-039**: System MUST emit `quote.expiring_soon` once per expiry window of a sent parent quote when it reaches the FR-026 quote-expiring-soon lead time, and MUST NOT emit it for draft, accepted, or terminal quotes, including the replacement quote, which has no expiry. A lead time raised after the send applies only to reminders not yet sent; a reminder whose time has already passed is skipped, not sent late (REQ-026-031).
- **REQ-004-040**: Every option/date price MUST be greater than 0 before send, and a zero price MUST block send. A date range the clinic cannot serve MUST be left out of that option rather than priced.
- **REQ-004-041** (retired): The Default Currency change on a draft that holds prices is owned by FR-029 (REQ-029-053), including the "currency changed, check your prices" banner. FR-004 only applies it on Tab 4 and Tab 7.
- **REQ-004-042**: A sent quote carrying an automatic FR-019 promotion MUST hold exactly one reserved use of that promotion's usage limit. A re-send of a new version MUST keep the existing reservation, create one only if the new version newly qualifies, and release it if the new version no longer carries the promotion. The reservation MUST be released when the quote expires, is withdrawn, is archived, or ends not selected or cancelled, MUST be released with reason `not_applied` when the accepted row does not carry the promotion, and MUST be consumed at acceptance when the accepted row carries it, so the usage limit is never exceeded. When an admin restores an expired quote, System MUST re-check the promotion's validity and usage limit and take a new reservation only when the quote holds none; if the limit is used up or the promotion has ended, the restore MUST be blocked with a message and the provider MAY send a new quote (REQ-004-105). If the booking later ends in `Payment Window Expired` or is cancelled before the first payment, FR-005 and FR-019 own the return of the consumed use to the limit.
- **REQ-004-043**: System MUST set the parent quote's `firstSentAt` on its first send, and a re-send or new version MUST NOT change it.
- **REQ-004-044**: The FR-024 treatment Base Price MAY prefill a new option/date-price row only where no other standard value exists; it MUST be treated as a non-binding reference and MUST NOT be read after the quote is sent.
- **REQ-004-045**: FR-004 MUST be the producer of `quote.updated` and MUST emit it when a new version of an already-sent quote is re-sent, described as "quote revised (new version)".
- **REQ-004-046**: System MUST emit `quote.submitted` on the first send of a parent quote and `quote.expired` when expiry processing moves a sent parent quote to `expired`. Recipients, content, and whether the notice can be switched off are set in the FR-030 notification Rules (REQ-030-033 and REQ-030-036).
- **REQ-004-047**: FR-004 MUST be the only producer of `quote.withdrawn`. The notice MUST go to the patient for every withdrawal and to the admin only when the withdrawn quote was already accepted.
- **REQ-004-048**: During an FR-006 provider-fault transfer before treatment starts, System MUST let an admin author a replacement quote for the replacement provider inside the same inquiry through Screen 8, with a mandatory reason and full audit. The quote MUST be marked admin-authored for a replacement and linked to the AcceptanceEvent it replaces, MUST NOT be offered for patient comparison, MUST stay a `draft` that is hidden from the replacement provider and the patient until it is accepted, MUST be editable only on Screen 8 and be excluded from Screen 2 and Screen 7, MUST NOT emit `quote.submitted` or `quote.expired`, and MUST be the target of the FR-005 admin-authored replacement acceptance.
- **REQ-004-049**: An admin edit of a sent quote through Screen 7 MUST create a new quote version and MUST emit `quote.updated` when that version is re-sent.
- **REQ-004-050**: System MUST NOT attach an automatic FR-019 promotion to an admin-authored replacement quote or take a promotion usage reservation for it; the admin sets the replacement price directly, so the replacement quote carries no promotion, and the use held by the original acceptance's promotion, which FR-019 marks Superseded, returns to the usage limit. A replacement quote MUST have no expiry and MUST NOT emit `quote.expiring_soon`; it stays a `draft` until the admin records the replacement acceptance, and a replacement draft that is never accepted follows the 7-day draft rule. It MUST leave the inquiry flagged `supportRequired` without cancelling it automatically, and the admin MAY author another replacement quote, close the inquiry with Close inquiry on FR-006 Screen 6 when the booking is already `Cancelled` with the marker, or cancel through FR-006 Alternative Flow B2 (Screen 9) when the fault is still pending.
- **REQ-004-109**: While the booking carries the provider-fault marker, whether the fault is pending or the booking is already `Cancelled` with the marker, System MUST block provider edits and admin Screen 7 edits of every field of the accepted quote except admin notes, MUST block an admin restore of any quote of the inquiry, and MUST hide a second Withdraw action. The replacement quote on Screen 8 is the only quote write allowed. The marker stops payment, reminders, and revive in FR-006 (REQ-006-081).
- **REQ-004-110**: An active acceptance is the latest AcceptanceEvent on the inquiry that has no supersession record, whatever the status of its parent quote or subquote. The original acceptance stays active, even after its quote is withdrawn, until the replacement acceptance is recorded; once it is superseded, superseded takes precedence over withdrawn for the original subquote. The original parent quote keeps its own status, and only the replacement parent quote counts as the inquiry's accepted quote. A restore stays blocked between a withdrawal and the replacement acceptance.
- **REQ-004-111**: When an admin closes the inquiry (Close inquiry on FR-006 Screen 6) or cancels it (FR-006 Screen 9), System MUST move any draft replacement quote of that inquiry to `cancelled_inquiry_cancelled`, MUST NOT send `quote.cancelled_inquiry` to the replacement provider, and no `quote.expired` follows. The cascade trigger is owned by FR-003 (REQ-003-013) and FR-006.
- **REQ-004-112**: A provider who has not accepted the current legal documents MUST NOT be able to submit a quote (first send or re-send). The acceptance prompt of FR-027 is shown and the draft is kept unchanged; creating and editing a draft is not blocked (REQ-027-033).

### Display, Restore, and Messaging Requirements

- **REQ-004-102**: Tab 7 (Review & Submit) MUST show a read-only Validation Summary checklist of every tab's completion, linking each unresolved issue to its owning tab; Submit Quote MUST stay blocked while any blocking issue is unresolved.
- **REQ-004-103**: The patient Quote Review screen MUST show read-only indicators that a quote is new, updated, or expired.
- **REQ-004-104**: The admin Quote List MUST show a badge or icon, with a count or indicator, on an inquiry that holds more than one quote.
- **REQ-004-105**: Only an admin, with a mandatory reason, MAY restore an expired quote. The restore MUST be blocked, with a message that names the failed guard, when the inquiry is not open, the provider is not `Active`, the inquiry has an active acceptance (REQ-004-110), or the booking carries a provider-fault marker (REQ-004-109); the same guards apply to every restore of an archived quote (REQ-004-077). Before restoring, System MUST re-check the validity and usage limit of the promotion on the quote's rows and take a new reservation only when the quote holds none; if the limit is used up or the promotion has ended, the restore MUST be blocked with a message and the provider MAY send a new quote. The same re-check applies when an archived sent quote is restored to `sent`. The restored quote MUST return to `sent` with a fresh full window: its new expiry is the restore time plus the FR-026 quote expiry window in force at that time. This is the only case in which a quote's expiry is renewed.
- **REQ-004-106**: When an admin restores an expired quote, System MUST notify both the patient and the provider through `quote.restored`; FR-004 is the only producer. Drafted default channels are Email and Push; recipients, content, and whether the notice can be switched off are set in the FR-030 catalogue (REQ-030-218).
- **REQ-004-107**: When a provider sends a quote, the patient and that provider MUST be able to message each other: the first quote from a provider to a patient opens their FR-012 conversation, and a later quote from the same provider is added to it. FR-012 owns the conversation itself.

## Dependencies

- FR-003: Inquiry Submission (quote distribution and reference)
- FR-015: Provider Management (provider status eligibility and the suspension/deactivation cancellation cascade)
- FR-005: Quote Comparison & Acceptance (owns sibling/competing outcomes)
- FR-008: Travel & Logistics Coordination (accepted-option inclusion routing)
- FR-010: Treatment Progress Management (accepted-option plan handoff)
- FR-024: Treatment Package Management (provider package presets and source versions)
- FR-020: Notifications & Alerts (quote distribution/updates)
- FR-012: Messaging (conversation opened or updated when a quote is sent; REQ-004-107)
- FR-026 / A-09: Quote configuration (quote currency, expiry window, and quote-expiring-soon lead time)
- FR-006: Booking & Scheduling (slot hold; provider-fault transfer after acceptance)
- FR-029: Payment System Configuration (indicative commission model and value)
- Admin-managed treatment catalog (A-09)
- FR-019: Promotions & Discount Management (A-06)
- FR-037: Monitor Your Hair Loss (exclusive assigned provider restricts initial quote creation)

## Edge Cases

- Provider starts, then abandons, a draft: the draft is retained for 7 days after its last edit and then auto-archived (REQ-004-094)
- Patient does not respond: quote expires, status auto-updated, provider notified
- Admin must audit archived/soft-deleted quote: accessible in "Archived" tab, audit trail modal enabled
- Provider or admin attempts deletion, archive, or restore of an accepted quote: disallowed; an accepted quote is never deleted, archived, or restored
- Recovery from expired state: only admin can restore expired/archived quotes if justified (GDPR-compliant log); a restore is offered only for an expired quote or a quote archived from draft or sent, and is blocked while the inquiry is not open, the provider is not `Active`, the inquiry has an active acceptance, or the booking carries a provider-fault marker. A restored expired quote returns to `sent` with a fresh full window (restore time plus the FR-026 window in force), a reason is required, the promotion is re-checked and re-reserved when the quote holds no reservation (the restore is blocked when its limit is used up or it has ended), and the patient and provider are notified through `quote.restored`. An archived draft returns to `draft`; an archived sent quote returns to `sent` if its original expiry has not passed, otherwise to `expired` (REQ-004-077, REQ-004-105, REQ-004-106)
- Treatment deactivated while a draft holds it: see REQ-024-052
- Provider opens quote creation for an inquiry that was just cancelled: system blocks with "Inquiry no longer active" error; no draft created
- Provider is mid-draft when inquiry is cancelled (race condition): on next save/refresh, system locks draft with "Inquiry Cancelled" banner; submission blocked; draft retained for provider reference but cannot be submitted
- Provider attempts to edit a quote in "Cancelled (Inquiry Cancelled)" status: system blocks with "This quote was cancelled because the patient cancelled their inquiry" message, or with the neutral "This inquiry was closed. Your quote can no longer be changed." when an admin closed or cancelled the inquiry; all edit actions disabled (REQ-004-098)
- Provider submits a quote at or after the effective time of its suspension or deactivation: submission is rejected; no sent quote, patient notification, or version is created
- Provider with several parent quotes, each with multiple options/date alternatives, is suspended: each unaccepted parent quote is cancelled once; option and date alternatives become unavailable with their parent and are not reported as separate cancellations
- Provider is suspended after one of its quotes was accepted: that parent quote keeps `accepted` and FR-006 handles the case through the provider-fault transfer; only the provider's unaccepted quotes become `cancelled_provider_status`
- Patient accepts at the last moment before the quote expiry: the parent quote is `accepted` and is never moved to `expired` during the payment hold
- Source package is edited or deactivated while a draft is open: the draft keeps its snapshot and may still be submitted with a warning
- Provider enters 0 for an option/date price: send is blocked with an inline error on that row; the provider either enters a price greater than 0 or leaves that date range out of the option
- Default Currency changes while a draft holds prices: the draft switches to the new currency with typed numbers kept, and send is blocked until the provider acknowledges the "currency changed, check your prices" banner
- An automatic promotion's last use is reserved by another quote before this quote is sent: the promotion is not attached at send, because the usage limit can never be exceeded (REQ-004-089)

## Glossary

- **Quote**: Provider-generated cost and treatment proposal for a given inquiry
- **Soft Delete**: Archive status, not a hard delete; record remains for compliance/audit
- **Treatment Catalog**: Admin-defined set of available treatments displayed to all providers for selection
- **Package**: Provider-owned, versioned FR-024 library template that seeds exactly one Quote Option (services and pricing, travel services, and a relative day plan); there are no add-on package types
- **Quote-local copy**: The inline-edited package content saved only on one Quote Option, never written back to the library
- **Provider-fault marker**: The marker that FR-006 sets on a booking while a provider fault is pending or after the booking closed with a provider-fault cause (`ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated`); it is a marker, not a status
- **Replacement quote**: The admin-authored quote for the replacement provider of an FR-006 provider-fault transfer; it has no expiry and stays a hidden draft until the admin records the replacement acceptance

## References

- system-prd.md: FR-004, Notification/Retention/Audit policies
- Hairline-ProviderPlatformPart1.txt lines 50-130: treatment/package selection, quote-local customization, date-price configuration, and discount context
- HairlineApp-Part1.txt lines 105-159 and 175-186: patient quote review, package comparison, pricing/discount display, expiry, and pre-scheduled appointment intent
- [SRC-MTG-002, MTG-002-D03 through D06 and O01](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md)
- [CR-FR004-20260909-01](../../../../archived/prd-baseline-2026-11-08/fr004-quote-submission/change-request-2026-09-09-quote-options-model.md)
## User Scenarios & Testing

### User Story 1 - Create and Submit Quote (Priority: P1)

Why: Core provider action enabling patient decision-making.

Independent Test: Provider opens a distributed inquiry, selects one treatment, configures one to five package options with complete date-price matrices and option plans, and submits; patient sees the quote aggregate with expiry.

Acceptance Scenarios:

1. Given a distributed inquiry, When provider submits a quote containing one to five valid options, Then patient receives the parent quote, ordered options, and expiry timer
2. Given required fields are missing, When submitting, Then system blocks with clear validation messages
3. Given a quote has zero or more than five options, When submitting, Then system blocks with a clear option-count validation message
4. Given a submitted quote, When viewing provider list, Then the parent quote appears once with its option count, price range, correct status, and audit entry
5. Given the provider already has a quote for the inquiry, When creating another valid quote, Then the system permits it and assigns an independent quote identity and lifecycle
6. Given a provider is creating or editing a quote, When navigating the seven tabs, Then each field is editable only in its owning tab and the Review & Submit validation links incomplete data back to that tab
7. Given the quote is reviewed, When comparing the aggregate against the Quote Data Ownership Matrix, Then every field has one provider-editing tab or an explicit read-only/system-derived owner
8. Given the provider opens Dates & Pricing, When the configured currency is displayed, Then it is read-only and the same currency snapshot applies to every option/date price
9. Given the provider selects a Treatment, When the quote is saved and later displayed, Then the quote retains the exact immutable Treatment ID/version relationship and loads its technique details read-only without a duplicated Quote field

### User Story 1A - Customize Package Options Inline (Priority: P1)

Why: Providers need patient-specific flexibility without polluting their reusable package library.

Independent Test: Select a package preset, customize services inline, submit the quote, then compare the option snapshot with the unchanged library package.

Acceptance Scenarios:

1. Given an active provider package, When selected for a quote, Then its identity/version, standard values, and items are copied into a quote-owned option snapshot
2. Given a selected option, When provider adds, edits, includes, or removes a service, Then only that option snapshot changes
3. Given a sent quote, When the source package later changes, Then the sent option remains unchanged
4. Given multiple options, When provider enters applicability and price, Then every applicable option/date combination is present and independently priced
5. Given two options, When provider enters their day plans, Then each option retains its own consecutive relative-day sequence

### User Story 2 - Edit Quote Before Expiry (Priority: P2)

Why: Providers need controlled flexibility prior to patient acceptance.

Independent Test: Provider edits a sent (pre-expiry) quote; changes versioned and patient notified.

Acceptance Scenarios:

1. Given a sent quote not yet expired, When editing shared data or option-owned data, Then the aggregate version increments and audit logs identify the affected option/entity
2. Given a new version of a sent quote, When it is re-sent, Then the patient is notified automatically through `quote.updated`; saving a draft edit without re-sending notifies no one
3. Given an expired quote, When editing, Then system blocks and shows policy notice

### User Story 3 - Auto-Expiry and Status Transitions (Priority: P1)

Why: Enforces time-bound decision windows.

Independent Test: Allow quote to reach expiry; verify status transitions and notifications.

Acceptance Scenarios:

1. Given a sent quote, When expiry time is reached, Then status becomes Expired and provider/patient are notified
2. Given patient selects one option/date combination through FR-005, When acceptance is recorded, Then the parent quote and selected option/date identifiers are preserved, other sent parent quotes are cancelled with one not-selected notice per parent quote, and stakeholders are notified
3. Given another provider has an unsent draft for the inquiry, When a subquote is accepted, Then the draft becomes `cancelled_other_accepted` and no notice is sent (REQ-004-096)
4. Given a quote was accepted shortly before its expiry, When the expiry time passes, Then the parent quote stays `accepted`
5. Given a draft quote, When it is saved, Then it has no expiry and no captured currency; When it is first sent, Then both are captured read-only from the FR-026 quote configuration and later setting changes do not alter them

### User Story 4 - Provider Experience During Inquiry Cancellation (Priority: P2)

Why: Providers must see clear, immediate feedback when a patient cancels an inquiry, preventing wasted effort on quotes that can no longer be submitted.

Independent Test: Patient cancels inquiry with active quotes; verify provider sees correct status, banners, locked actions, and notifications from FR-004's perspective.

Acceptance Scenarios:

1. Given provider has a sent quote for an active inquiry, When patient cancels the inquiry, Then quote status becomes "Cancelled (Inquiry Cancelled)" in provider quote list (Screen 2) with greyed-out styling and "Inquiry Cancelled" badge
2. Given provider opens the cancelled quote detail (Screen 3), When viewing, Then a prominent "Inquiry Cancelled" banner is displayed at top; all Edit/Delete actions are disabled; quote data remains read-only
3. Given provider is drafting a quote when patient cancels the inquiry, When provider attempts to save or submit, Then system locks draft with banner: "This inquiry was cancelled by the patient. Your draft can no longer be submitted."
4. Given provider opens quote creation for a newly cancelled inquiry, When system loads, Then system blocks creation with error: "Inquiry no longer active" and returns provider to quote list
5. Given provider receives `quote.cancelled_inquiry` notification (FR-020), When provider taps notification, Then system navigates to the cancelled quote detail view with banner

---

### User Story 5 - Pricing, Promotions, and Post-Acceptance Lifecycle (Priority: P1)

Why: The patient must accept exactly what was sent, and accepted quotes must hand provider faults to booking without being rewritten.

Independent Test: Send a quote with selected and automatic promotions, edit the promotion in FR-019, accept one subquote, then attempt edits, suspension, and withdrawal.

Acceptance Scenarios:

1. Given three packages and two requested date ranges, When the provider selects all three packages, Then three Quote Options are created and up to six option/date-price rows can be priced; a pairing the provider leaves out is not offered
2. Given a selected package, When it is seeded, Then its standard price prefills every applicable date-range row and its relative day plan prefills the option plan
3. Given a provider edits a package inline in quote creation, When the quote is saved, Then only the quote-local copy changes, the option records the source package version and the inline-customised flag, and the library package and its versions are unchanged
4. Given a provider edits a package in the package management screen, When saved, Then a new library package version is created and existing draft and sent options keep their copies
5. Given a promotion is attached to an option/date row, When the quote is sent and the FR-019 promotion is later edited, Then the sent quote keeps the copied terms and the offered price stays as entered with the discount shown separately
6. Given an automatic FR-019 promotion is eligible for some option/date rows, When the quote is sent, Then it is attached to every eligible row and to no other row
7. Given an authorized role views Tab 7, When the commission is shown, Then it shows the model and value (percentage or flat rate) labelled "indicative, final at booking confirmation"
8. Given a subquote is accepted, When a provider attempts any FR-004 edit, Then the edit is blocked and treatment-detail changes are directed to FR-010; When an admin edits any field except price, currency, and promotion with a reason, Then the change is saved as a new version beside the unchanged acceptance snapshot with full before and after history, and an attempt to change price, currency, or promotion is blocked
9. Given a subquote is accepted and the booking is `Accepted` or `Confirmed` before check-in with no provider-fault marker, When the provider withdraws after a confirmation that names the consequence and with a mandatory reason, Then the parent quote moves to `withdrawn`, the AcceptanceEvent is unchanged, the mandatory `quote.withdrawn` notice is sent, and the case is handed to the FR-006 provider-fault transfer without FR-004 re-routing
10. Given a provider with one accepted and one sent quote is suspended, When the suspension takes effect, Then only the sent quote becomes `cancelled_provider_status` and the accepted quote keeps `accepted` for the FR-006 provider-fault transfer
11. Given the booking reaches `Payment Window Expired`, When anyone tries to accept again or create a new quote for the inquiry, Then the accepted quote is not reopened and no new parent quote can be created or sent
12. Given an option/date row priced at 0, When the provider tries to send, Then send is blocked with an inline error on that row
13. Given a draft holds prices and the Default Currency changes, When the provider reopens the draft, Then the prices are kept as typed in the new currency and send is blocked until the "currency changed, check your prices" banner is acknowledged
14. Given an automatic promotion with a usage limit, When a quote carrying it is sent and later expires, is withdrawn, is archived, or ends not selected or cancelled, Then the reserved use is released; When the quote is accepted, Then the use is consumed
15. Given a sent quote, When the provider re-sends a new version, Then `quote.updated` is emitted as "quote revised (new version)" and `firstSentAt` is unchanged
16. Given a booking that carries a provider-fault marker (pending or closed) before treatment started, When the admin authors a replacement quote on Screen 8 with a reason, Then the quote is saved as admin-authored for a replacement inside the same inquiry, no `quote.submitted` is emitted, and the FR-006 transfer can record the admin-authored acceptance against one of its option/date-price rows
17. Given a booking in Aftercare whose provider is at fault, When the admin handles it, Then Screen 8 is unavailable and only the aftercare provider or team is reassigned in FR-006
18. Given two automatic promotions qualify for the same quote, When the quote is sent, Then only the one ranked first by the FR-019 priority order is attached
19. Given an admin authors a replacement quote on Screen 8, When it is saved, Then no automatic promotion is attached, no promotion usage reservation is taken, and the price is the one the admin entered
20. Given a replacement quote that is not accepted, When time passes, Then it has no expiry and stays a `draft` that the patient does not see, the inquiry stays `supportRequired`, and the admin can author another replacement quote, close the inquiry with Close inquiry on FR-006 Screen 6 when the booking is already `Cancelled` with the marker, or cancel through FR-006 Alternative Flow B2 (Screen 9) when the fault is still pending
21. Given an expired quote on an inquiry with no active acceptance, When an admin restores it with a reason and its promotion is still available, Then the quote returns to `sent` with a fresh full window (restore time plus the FR-026 window in force), a new promotion reservation is taken, and the patient and provider receive `quote.restored`; When the promotion limit is used up or the promotion has ended, Then the restore is blocked with a message
22. Given a provider sends a quote to a patient, When the quote is sent, Then the patient and that provider can message each other in the FR-012 conversation, and a later quote from the same provider is added to that conversation
23. Given a draft quote whose treatment an admin has since deactivated, When the provider tries to send it, Then the provider must first pick another treatment; sent quotes and bookings with that treatment are unaffected
24. Given a sent quote that the patient has not accepted, When the provider withdraws it from Screen 3 with an optional reason, Then the quote moves to `withdrawn`, its promotion reservation is released, and the patient receives `quote.withdrawn`
25. Given a booking that carries a pending provider-fault marker and an active acceptance, When a provider or an admin tries to edit the accepted quote (admin notes excepted), restore a quote of the inquiry, or withdraw again, Then every action is blocked or hidden, and a new parent quote cannot be created or sent; the replacement quote on Screen 8 is the only quote write
26. Given an expired quote, a quote archived from draft or sent, or a quote archived from any other status, When an admin looks for Restore, Then only the first two offer it; When the inquiry is not open, the provider is not `Active`, the inquiry has an active acceptance, or the booking carries a provider-fault marker, Then the restore is blocked with a message that names the failed guard
27. Given a replacement draft whose currency was fixed at its first Screen 8 save, When the admin records the replacement acceptance in FR-006, Then the quote moves from `draft` through `sent` to `accepted`, its first-send time is recorded, the original quote keeps its status, and no cancel-other-quotes cascade runs
28. Given two open replacement drafts for one inquiry, When the admin records the replacement acceptance against one of them, Then the other is cancelled as `cancelled_other_accepted` silently and its provider receives no notice

### Edge Cases (User Scenarios)

- Provider starts draft then abandons: auto-archive 7 days after the last edit
- Patient does not respond: quote expires and provider notified
- Provider or admin attempts deletion, archive, or restore of an accepted quote: disallowed; an accepted quote is never deleted, archived, or restored
- Admin audits archived/soft-deleted quote: available in Archived view with full audit trail
- Provider removes options until none remain: submission blocked until at least one valid option exists
- One option has no applicable date range or an incomplete option/date price: submission blocked for that option
- Source package becomes inactive after snapshot creation: existing sent quote remains stable; replacing the package requires a new snapshot and audit entry
- Provider edits one option: sibling options and the reusable package remain unchanged

### Required Verification Matrix

| Test Layer | Required Coverage | Minimum Evidence |
| --- | --- | --- |
| Unit | Option-count gates, consecutive ordering, price-range derivation, lifecycle guards, and Treatment-version resolution | Passing domain-service tests for valid and invalid boundaries |
| Integration | Inquiry, Treatment version, package library, promotion, notification, audit, and accepted-option handoffs | Passing persistence and service-integration tests without cross-tenant database access |
| Contract | Create, update, list, detail, submit, withdraw, archive, and acceptance-handoff APIs | Versioned request, response, and error-schema tests for parent and option-owned records |
| End-to-End | Seven-tab submission, second parent quote, quote-local customization, edit, expiry, withdrawal, cancellation, and admin oversight | Passing Provider, Patient, and Admin journeys with immutable audit assertions |
| Security | RBAC, tenant isolation, anonymization, file validation, rate limits, and tamper-resistant audit history | Passing authorization and abuse-case tests with anonymized test data |
| Performance | Quote list/detail, aggregate submission, expiry processing, and notification fan-out | p95 and p99 evidence against Constitution targets plus peak-load results |

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 4.0 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v3.9) and the change requests (CR-FR004-20260820-01, CR-FR004-20260909-01, CR-FR004-20261014-01, CR-FR004-20261016-01, CR-FR004-20261027-01, and CR-FR015-20261013-01 named in v3.0) are in `archived/prd-baseline-2026-11-08/` and in git history. | Claude (AI Assistant) |
| 2026-11-23 | 4.1 | Table format repair: the Graph field values of 16 field tables moved into their own last column (they sat inside the previous cell). Cell text unchanged. No rule changes. | Claude (AI Assistant) |
| 2026-11-23 | 4.2 | FR-005 r1 logic review, finding N8 and the owner ruling of 2026-11-23 (the admin edit of the accepted quote is kept): REQ-004-084 names the admin edit of the accepted quote's date range or appointment (REQ-005-023) beside the FR-006 admin appointment change as a path that changes the booking's appointment. | Product Owner / Documentation |
| 2026-11-24 | 4.3 | FR-004 logic review, first pass. A provider withdraws a sent quote before acceptance from the quote detail screen (optional reason), and may soft-delete drafts only; an accepted quote can be withdrawn only while the booking is Confirmed, before check-in, with no provider-fault marker. The provider-fault transfer now follows FR-006: the booking keeps its status and slot hold with the support-required marker until the admin submits the replacement, and Screen 8 opens for a pending or closed fault until a replacement acceptance is recorded. While the marker is on, the accepted quote is frozen (REQ-004-109), and one definition of an active acceptance is added (REQ-004-110). The replacement quote has no expiry, stays a draft the patient does not see until accepted, and is cancelled without notice when an admin closes or cancels the inquiry (REQ-004-111); the case ends by Close inquiry (FR-006 Screen 6) or the FR-006 cancel flow. Archiving a quote releases its promotion reservation, and restoring an expired quote re-checks and re-reserves the promotion. Restore targets for archived drafts and archived sent quotes are stated. The 7-day draft archive counts from the last edit and is a fixed platform rule. The identity rule cites the platform-wide rule, and the restore notice cites its catalogue entry. | Claude (AI Assistant) |
| 2026-11-24 | 4.4 | FR-004 logic review, second pass. An accepted quote can be withdrawn while the booking is Accepted or Confirmed (before check-in, no provider-fault marker), after a confirmation that names the consequence; an ineligible quote shows no Withdraw and a short note instead of a contact-support pointer. The provider-fault marker freezes every field of the accepted quote except admin notes. The replacement quote keeps its currency from the first Screen 8 save, is hidden from the provider and the patient until accepted, is edited only on Screen 8, and moves from draft through sent to accepted at the replacement acceptance, which cancels no original quote and silently cancels other open replacement drafts. Restore is offered only for an expired quote or a quote archived from draft or sent, with guards (inquiry open, provider Active, no active acceptance, no provider-fault marker), and re-takes a promotion reservation only when none is held. Expiry events fire once per expiry window. Neutral banner wording for an admin-closed inquiry. Screen 8 added to the Admin Platform and Entry Points lists; new scenarios 24 to 28; one term, provider-fault marker. | Claude (AI Assistant) |
| 2026-11-25 | 4.5 | Cross-FR alignment. A provider who has not accepted the current legal documents cannot submit a quote, first send or re-send, while drafts stay editable (REQ-004-112, REQ-027-033). A replacement quote carries no promotion and the original promotion application is marked Superseded (REQ-004-050). A percentage discount above the FR-019 maximum is a hard cap with no admin review, and a fixed-amount discount has no cap (REQ-004-090). Tab 2 package choices are the provider's own Active packages, packages are not tied to a treatment, and a Tab 1 treatment change makes the system identify the dependent option pricing and plan data (REQ-004-059). A treatment set to Not Offered blocks new quotes only (REQ-004-054). A team member who leaves or loses rights is replaced on the clinician list of the provider's open quotes by a recorded system change (REQ-004-027). A lead time raised after the send applies only to reminders not yet sent, and a passed reminder is skipped (REQ-004-039). | Claude (AI Assistant) |


## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Joachim Trung Tuan | 2026-09-16 | Approved through FR-004 v2.8 — quote hierarchy, FR-005 subquote projection, aggregate `QuoteVersion` source, and subquote-driven lifecycle reconciliation |
| Product Owner | Joachim Trung Tuan | 2026-10-16 | Documentation approved through v3.2 via the MTG-002 quote-model decision log (CR-FR004-20261016-01); v3.3 consolidated verification corrections on 2026-10-18 apply decisions Q24 and Q29 to Q31; implementation reconciliation required |
| Product Owner | Joachim Trung Tuan | 2026-10-18 | Approved via MTG-002 decision log (documentation only), v3.4 final audit corrections (CR-FR004-20261016-01); implementation reconciliation required |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-004 from system-prd.md
**Last Updated**: 2026-11-25
