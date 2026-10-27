# FR-004 - Quote Submission & Management

**Module**: PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr004-quote-submission-management`
**Created**: 2025-10-30
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-004 from system-prd.md; SRC-MTG-002 (MTG-002-D03 through D06 and O01); FR-005 v2.5; FR-006 v2.7; Product Owner clarifications dated 2026-09-09, 2026-09-10, and 2026-09-16; Product Owner MTG-002 quote-model decision log dated 2026-10-16
**Change Requests**: [CR-FR004-20260820-01 — FR-037 monitoring conversion alignment](change-request-2026-08-20-fr037-monitoring-conversion-alignment.md); [CR-FR004-20260909-01 — Quote options model](change-request-2026-09-09-quote-options-model.md); [CR-FR004-20261014-01 — Provider status cancellation cascade](change-request-2026-10-14-provider-status-cancellation-cascade.md); [CR-FR004-20261016-01 — MTG-002 quote model alignment](change-request-2026-10-16-mtg002-quote-model-alignment.md); [CR-FR004-20261027-01 — Legacy status value migration](change-request-2026-10-27-legacy-status-value-migration.md)

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
- Edit and submit quotes; manage lifecycle (draft, sent, expired, withdrawn, archived)
- See inquiry context (append-only)

**Admin Platform (A-01)**:

- Oversight of all quotes; inline edit (policy-bound), soft delete/restore; full audit trail
- Configure expiry window and manage exceptional withdrawals

**Shared Services (S-XX)**:

- Notification service; audit logging; retention/soft-delete utilities

### Communication Structure

**In Scope**:

- System → Provider: New inquiry notifications and time-bound updates
- Provider → System: Draft, edit, status transitions, soft delete/archive
- System → Patient: Quote creation/expiry/status notifications (FR-004 produces `quote.submitted`, `quote.updated`, `quote.expiring_soon`, `quote.expired` and `quote.withdrawn`)
- Admin → All Parties: Oversight, intervention, audit logging

**Out of Scope**:

- Direct patient-provider chat (handled by FR-012)

### Entry Points

1. Provider receives auto-distributed inquiry from FR-003
2. Provider opens Quote Management dashboard (new, draft, sent, history, archive bins)
3. Provider creates and edits a quote by selecting the shared treatment, then configuring one to five package options
4. Patient receives parent quote(s) and views their complete subquotes in the patient app
5. Admin can access, search, or override quote status from admin platform

## Business Workflows

### Workflow 1: Provider Quote Creation (Primary Flow)

**Actors**: Provider, System, Admin (observer/audit)

**Trigger**: Provider opens a distributed inquiry and starts composing a quote

**Outcome**: A valid parent quote with one to five package options is delivered to the patient; the complete quote aggregate is versioned and audited

- Provider receives inquiry and opens details
- System verifies parent inquiry status is not Cancelled before allowing quote creation. If inquiry is cancelled, system blocks with error: "Inquiry no longer active — this inquiry was cancelled by the patient."
- **Restricted recipient check**: If the inquiry carries an exclusive assigned provider from an FR-037 monitoring conversion, system verifies the opening provider is the assigned provider; any other provider is blocked with error "This inquiry is restricted to its assigned provider." (see Business Rules)
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

### Workflow 2: Quote Editing

**Actors**: Provider, System, Admin (editor while the quote is draft or sent, through Screen 7)

**Trigger**: Provider opens an existing draft or sent (pre-expiry) quote to modify fields

**Outcome**: Changes are saved with versioning/audit; the patient is notified when a new version of a sent quote is re-sent (`quote.updated`)

- Provider may edit draft or sent (pre-expiry) quotes, including shared fields, options, option-local inclusions, date-price combinations, and option-specific plans
- Admin may edit draft or sent quotes through Screen 7 with a mandatory reason; an admin edit of a sent quote creates a new version and emits `quote.updated` when that version is re-sent
- Package-library changes made after an option was created do not alter the quote snapshot
- All parent and option changes are versioned/audited as one quote aggregate
- Edits on accepted, expired, withdrawn, archived, or cancelled quotes are prohibited for providers and admins. After acceptance, treatment details (plan, clinicians, grafts) change only through FR-010; price, currency, date range, and promotion never change; the booking's appointment changes only through the FR-006 admin appointment change, which emits `booking.rescheduled`, while the acceptance snapshot keeps the accepted appointment as the baseline
- When a new version of an already-sent quote is re-sent, System emits `quote.updated` (described as "quote revised (new version)") for FR-020 notification; FR-004 is the only producer of this event. Saving draft edits without re-sending emits nothing
- A re-send or new version never changes the quote's first-send timestamp or its expiry

### Workflow 3: Quote Expiry & Status Transitions

**Actors**: System, Provider, Patient, Admin (observer)

**Trigger**: Time-based expiry reached; patient accepts a subquote through FR-005; provider initiates withdrawal/archive; patient cancels parent inquiry (FR-003 Workflow 5); or the owning provider becomes `Suspended` or `Deactivated` (FR-015 Alternative Flow A5 and Screen 4)

**Outcome**: Quote transitions to correct status; notifications sent; audit recorded

- Expiry is captured at first send: the system copies the quote expiry setting from the active FR-026 quote configuration (default 48 hours) read-only onto the quote and computes the expiry timestamp from the first send time. Drafts have no expiry. Later edits and re-sends do not reset it, later setting changes never affect a sent quote, and there is no per-quote extension. Providers cannot modify the window and only see the computed expiry timestamp.
- Expiry applies only to `sent` parent quotes. Upon expiry, system updates the parent quote to `expired`, emits `quote.expired` once for that parent quote (FR-030), and every child subquote becomes ineligible for acceptance. `accepted` quotes and every cancelled, withdrawn, or archived quote are never moved to `expired`.
- When a sent parent quote reaches the "quote expiring soon" lead time set by admin in FR-026, the system emits `quote.expiring_soon` once for that parent quote (FR-030). It is never emitted for drafts or for accepted or terminal quotes.
- Provider may withdraw or archive quotes pre-acceptance. The `quote.withdrawn` notification is always mandatory, before and after acceptance. FR-004 is its only producer. The patient is always notified; the admin is notified only when the withdrawn quote was already accepted (Workflow 6), because a withdrawal before acceptance is a normal provider action.
- FR-005 subquote acceptance moves the selected subquote and its parent quote to `accepted`, marks sibling subquotes `not_selected`, and moves every other parent quote for the inquiry, from any provider, to `cancelled_other_accepted`; the parent quote, Quote Option, and Option/Date-Price Record are never direct acceptance targets. Each sent parent quote that is cancelled this way produces one not-selected notice per parent quote. Unsent draft parent quotes are cancelled silently with the same status and no notice.
- An accepted parent quote stays `accepted` and is never reopened for acceptance or moved to `expired`, including after FR-006 moves the booking to `Payment Window Expired`; its status changes only through provider withdrawal (Workflow 6). An admin booking cancellation in FR-006 moves the booking and inquiry to `Cancelled` but leaves the accepted parent quote `accepted`. Competing parent quotes stay cancelled, and no new parent quote can be created or sent for an inquiry that has an accepted subquote; the only exception is the admin-authored replacement quote for an FR-006 provider-fault transfer (Workflow 7). The patient cannot cancel the inquiry after acceptance; through "Contact support" the patient reaches an admin, who performs the audited FR-006 revive or an FR-006 booking cancellation, after which the patient may start a new inquiry.
- **Patient cancels parent inquiry**: The patient can cancel only in the Inquiry or Quoted stage, before any subquote is accepted. All quotes for that inquiry transition to "Cancelled (Inquiry Cancelled)" regardless of current state (draft, sent, expired). This is a system-initiated cascade, not a provider or patient action on the quote itself. Providers are notified via `quote.cancelled_inquiry` event (FR-020).
- **Provider becomes Suspended or Deactivated**: At the effective time, the system cancels every unaccepted draft or sent parent quote of that provider with status `cancelled_provider_status` and `cancellationProvenance` = `ProviderSuspended` or `ProviderDeactivated`. Cancelling an unsent draft is silent to the patient: the patient never saw it, so it triggers no `provider.status_cancellation_patient` notice on its own (admin support alerts still follow FR-020). Cancellation is recorded once per parent quote; its Quote Options and option/date-price alternatives become unavailable with the parent and are not cancelled or counted separately. `cancelled_provider_status` never applies to an accepted parent quote: if the provider's quote was already accepted, the parent quote keeps `accepted` and the FR-005 AcceptanceEvent stays unchanged. FR-006 Alternative Flow B4 records the closure on the booking as its cause, and no supersession record is written at that point. FR-005 writes the single linked supersession record only when the admin accepts the replacement quote in the FR-006 provider-fault transfer (FR-006 Alternative Flow B5). The FR-005 AcceptanceEvent, accepted IDs/versions, and quote-local package snapshots are not rewritten. Quotes already expired, withdrawn, archived, or otherwise terminal are not reclassified. Other providers' quotes are unaffected. Later reactivation does not restore cancelled quotes.
- All state transitions are logged and result in notifications as appropriate

### Workflow 4: Quote Deletion (Soft Delete)

**Actors**: Provider, System, Admin

**Trigger**: Provider chooses to remove an ineligible or obsolete quote prior to acceptance

**Outcome**: Quote becomes Archived with rationale; remains visible in audit/archive; only admin can restore

- Provider may soft-delete a quote before acceptance (removes from provider listing, not from audit/archive or patient record)
- Quotes in terminal states (accepted, expired, withdrawn, cancelled_other_accepted, cancelled_inquiry_cancelled, cancelled_provider_status) cannot be soft-deleted by provider — these are already terminal
- System sets status = Archived with rationale
- Soft-deletes are fully auditable and revertible only by admin

### Workflow 5: Admin Oversight

**Actors**: Admin, System

**Trigger**: Admin monitors quotes or intervenes per policy or escalation

**Outcome**: Administrative action applied; full audit trail preserved; re-notifications triggered if needed

- Admin dashboard lists all provider quotes, searchable/filterable by state/date/provider/inquiry
- Admin can perform soft delete or restore and view the immutable audit trail and full quote history; soft delete and restore are unavailable for a quote in `accepted` status, which is never deleted or restored
- Admin authors a quote only as the replacement quote of an FR-006 provider-fault transfer (Workflow 7, Screen 8)

### Workflow 6: Provider Withdrawal After Acceptance

**Actors**: Provider, Admin, Patient, System

**Trigger**: Provider withdraws the accepted quote before treatment

**Outcome**: The parent quote moves from `accepted` to `withdrawn` and the case is handed to the FR-006 provider-fault transfer; FR-004 does not re-route the case

- In rare cases, provider may withdraw from giving treatment after patient acceptance.
- Provider submits a withdrawal with a mandatory reason; the parent quote moves from `accepted` to `withdrawn`. This is the only status change FR-004 makes after acceptance; no quote field, option, or option/date-price record is edited.
- The FR-005 AcceptanceEvent, accepted IDs/versions, acceptance snapshot, and quote-local package snapshots are kept unchanged as history. FR-005 marks the AcceptanceEvent superseded by provider fault through a linked supersession record, never by editing it.
- FR-004 hands the case to the FR-006 provider-fault transfer (FR-006 Alternative Flow B5): the booking closes with cause `ProviderFault`, the slot hold is released, and an admin assigns a replacement provider within the same inquiry, authors a replacement quote for that provider (Workflow 7), and records a new admin-authored acceptance against it that is linked to the original. The patient keeps the same inquiry and re-enters nothing. FR-004 does not reopen competing quotes or re-route the case itself; its only part in the transfer is the admin-authored replacement quote.
- Money already paid follows the FR-006 placeholder: it moves with the patient as credit toward the replacement booking, any unused part is refunded, and the patient pays no cancellation fee. Exact mechanics are defined in FR-007, FR-007B, and FR-017.
- The `quote.withdrawn` notification to the patient and admin is mandatory; FR-004 emits it, and FR-006 reacts by starting the provider-fault transfer without emitting it again. All actions are audited.
- Provider drop-out after acceptance, including an FR-010 reassignment, is not a quote withdrawal; FR-010 routes it to FR-006. The provider-fault transfer with a replacement quote and a new acceptance applies only before treatment starts (booking `Accepted` or `Confirmed`). If the fault happens in Aftercare, the admin reassigns only the aftercare provider or team in FR-006; the booking and treatment record stay, and no replacement quote, new acceptance, or new payment is created.

### Workflow 7: Admin Replacement Quote (Provider-Fault Transfer)

**Actors**: Admin, System

**Trigger**: FR-006 has closed a booking with a provider-fault cause (`ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated`) before treatment started, and the admin has chosen a replacement provider in the FR-006 transfer

**Outcome**: One admin-authored replacement quote exists for the replacement provider inside the same inquiry and is ready for the FR-006 admin-authored replacement acceptance

- The admin opens Screen 8 from the FR-006 transfer. The system checks that the booking was closed with a provider-fault cause, that the inquiry has no active acceptance, that treatment had not started, and that the replacement provider is `Active` and is not the provider at fault.
- The admin builds the quote with the same structure as a provider quote: shared treatment facts, one or more Quote Options seeded from the replacement provider's active packages, and option/date-price rows with appointment date/time, time zone, and price. The accepted quote and snapshot of the closed acceptance are shown read-only for reference.
- The admin may adjust the package and price for the replacement; a mandatory reason is required.
- The admin sets the replacement price directly. No automatic FR-019 promotion attaches to a replacement quote and no promotion usage reservation is taken for it. Any promotion use held by the closed acceptance is returned or kept under the normal FR-019 rules.
- On save, the system records the quote as admin-authored for a replacement (`authorType = admin`, linked to the closed AcceptanceEvent) and keeps its version and audit history like any quote. Currency is captured from the active FR-026 quote configuration. The quote is not offered to the patient for comparison and does not emit `quote.submitted`.
- The admin then records the replacement acceptance in FR-006 against one option/date-price row of this quote; FR-005 Alternative Flow A9 records the AcceptanceEvent and the supersession link, and the quote moves to `accepted`.
- This is the only case in which a quote is created for an inquiry that already had an accepted subquote. One replacement acceptance is recorded per transfer.
- A replacement quote that is not accepted expires under the normal quote expiry (Workflow 3); its expiry is captured from the active FR-026 quote configuration when it is saved for acceptance. The inquiry stays flagged `supportRequired` and is not cancelled automatically. The admin may then author another replacement quote through Screen 8 or cancel the inquiry and booking from the FR-006 admin screen.

### Alternative Flows

- Provider starts draft but abandons (system retains drafts for 7 days then auto-archives)
- Provider attempts late edit or deletion (system disallows and shows user message)
- Provider creates an additional quote for the same inquiry (system treats it as a separate parent response with its own options, expiry, versions, and audit history)
- Provider customizes a selected package inline (system stores a quote-local option snapshot and leaves the package library unchanged)
- Provider removes an option before submission (system permits removal while at least one valid option remains)
- Patient accepts no subquote (system expires all open sent quotes automatically; there is no parent-level Decline action)
- Another quote is accepted → System marks all other parent quotes for the same inquiry as "cancelled (other accepted)"; each sent parent quote produces one not-selected notice per parent quote to its provider.
- While a provider is drafting a quote, if another quote is accepted → the unsent draft is cancelled silently as "cancelled (other accepted)" with no notice; on next open the draft is read-only with the "Another Quote Accepted" badge and cannot be submitted.
- Patient cancels parent inquiry (FR-003 Workflow 5) → ALL quotes for that inquiry are auto-cancelled with status "Cancelled (Inquiry Cancelled)"; each affected provider notified via `quote.cancelled_inquiry` event; drafting providers see locked quote with "Inquiry Cancelled" banner upon next save/refresh. Cancellation reason is patient-private and NOT shared with providers.
- Owning provider becomes `Suspended` or `Deactivated` (FR-015 A5/Screen 4) → that provider's unaccepted parent quotes are cancelled once each with `cancelled_provider_status` and the provider-caused `cancellationProvenance` (Workflow 3); drafting and submission are blocked; patients see the offer as unavailable with a Contact Admin/Support action rather than the patient-cancellation message. An already-accepted quote of that provider keeps `accepted` and is handled by the FR-006 provider-fault transfer.

## Screen Specifications

### Provider Platform

#### Screen 1: Quote Creation/Edit

**Purpose**: Provider creates or edits one parent quote and its package options with full inquiry context

**Quote Data Ownership Matrix**:

This matrix is the canonical completeness check for Screen 1. Tabs organize editing, but they do not change entity ownership. Fields marked system-owned or derived are never provider inputs.

| Entity / Field | Ownership | Provider Surface | Contract |
| --- | --- | --- | --- |
| Quote ID | System-owned | Persistent context and Tab 7 | Stable generated identifier; read-only |
| Inquiry ID and inquiry context | System-owned from FR-003 | Persistent context and Tab 7 | Read-only; quote appends to the inquiry and never overwrites it |
| Provider ID | System-owned from authenticated tenant | Tab 7 | Read-only; never selected in the quote |
| Treatment ID and version | Provider-selected relationship | Tab 1 | References the exact immutable FR-024 Treatment version shared by every option; the quote does not copy treatment-owned data |
| Technique details | Database/API retrieved from Treatment | Tabs 1 and 7 | Loaded read-only through the exact Treatment-version relationship; never separate provider input or duplicated quote data |
| Estimated grafts | Provider-edited parent field | Tab 3 | Positive integer shared by every option |
| Graft description | System-derived parent field | Tab 3 | Generated from the approved template and estimated grafts; read-only |
| Visual treatment plan / graft markup | Provider-edited parent field | Tab 3 | Optional shared drawing/media snapshot |
| Clinician IDs | Provider-edited parent field | Tab 6 | One or more eligible clinicians shared by every option |
| Common notes | Provider-edited parent field | Tab 6 | Optional text applying to every option |
| Common requirements | Provider-edited parent field | Tab 6 | Optional structured/text requirements applying to every option |
| Attachments | Provider-edited parent field | Tab 6 | Optional quote-level files applying to every option |
| Currency snapshot | System-configured parent field | Read-only in Tabs 4 and 7 | Captured read-only at first send from the active FR-026 quote configuration, whose currency is the FR-029 Default Currency; drafts carry none; never provider input |
| Status | System-owned lifecycle field | Persistent context and Tab 7 | Read-only; changed only by governed workflow actions |
| Expiry | System-derived parent field | Tab 7 | Captured read-only at first send from the FR-026 quote expiry setting; drafts carry none; no per-quote extension |
| Calculated price range / accepted total | System-derived parent summary | Tabs 4 and 7 | Price range is derived from all option/date prices; accepted total is written only at FR-005 acceptance from the acceptance snapshot (price after promotion) and is a read-only copy; neither is entered separately |
| Commission | System-derived financial field | Tab 7 subject to permissions | Shows the commission model and value (percentage or flat rate) from the active FR-029 configuration, labelled "indicative, final at booking confirmation"; the binding commission is fixed at booking confirmation on the accepted price after promotion (FR-029); never provider input |
| Affiliate attribution reference | System-captured financial provenance | Tab 7 subject to permissions | Inherited from validated referral context; never provider input |
| Terms acknowledged timestamp | System-owned FR-005 acceptance field | Tab 7 after acceptance | Null during quote creation; read-only copy of the FR-005 acceptance snapshot value |
| Locked exchange-rate value and pair | System-owned FR-005/FR-029 acceptance snapshot | Tab 7 subject to permissions | Null before acceptance; read-only copy of the FR-005 acceptance snapshot value when conversion is required |
| Cancellation and supersession provenance | System-owned lifecycle fields | Tab 7 / Audit | Records inquiry cancellation, another accepted quote, or provider suspension/deactivation of an unaccepted quote; never provider input |
| Travel-responsibility state and declaration metadata | System-owned FR-008 downstream fields | Tab 7 after applicable workflow action | Derived from the accepted option or recorded by the governed travel flow; not edited during quote creation |
| Created, updated, and last-edited metadata | System-owned audit metadata | Tab 7 / Audit | Generated from authenticated actions; read-only |
| Quote Option ID and parent Quote ID | System-owned | Tabs 2, 4, 5, and 7 | Stable identifiers; read-only |
| Source Package ID and version | System-captured option provenance | Tab 2 and Sub-screen 2A | Captured when selected (the exact FR-024 package version); read-only after snapshot creation |
| Option display order | Provider-edited option field | Tab 2 | Unique consecutive patient-facing order |
| Package name, description, and standard price snapshots | System-copied option fields | Tab 2 and Sub-screen 2A | Copied from the selected library version; retained for history |
| Option customization state (inline-customised flag) | System-derived option field | Tab 2 and Tab 7 | Indicates whether the quote-local copy has been edited inline and differs from its source package version |
| Included travel services (`included_services`) | Provider-edited option field | Sub-screen 2A | Flight, hotel, transport, and other travel services included in this option; stored only in the option snapshot |
| Option item ID and parent Option ID | System-owned | Sub-screen 2A and Audit | Stable identifiers; read-only |
| Option item source ID | System-captured item provenance | Sub-screen 2A | Read-only; null for an item created inside the quote |
| Option item type | Provider-edited item field | Sub-screen 2A | Controlled service type |
| Option item name and description | Provider-edited item fields | Sub-screen 2A | Required name; optional description |
| Option item price | Provider-edited item field | Sub-screen 2A | Optional component price; does not replace the final Tab 4 offered price |
| Option item inclusion state | Provider-edited item field | Sub-screen 2A | Explicit included or excluded state |
| Option item display order | Provider-edited item field | Sub-screen 2A | Unique consecutive order within the option |
| Option item metadata | System-retained item field | Sub-screen 2A / Audit | Read-only extension/source metadata; never free-form provider input |
| Option/date-price ID | System-owned | Tab 4 and Tab 7 | Stable identifier for FR-005 acceptance |
| Source inquiry date-range ID | Provider-selected reference | Tab 4 | Must reference a patient-requested FR-003 range |
| Start and end dates | System-copied date fields | Tab 4 | Read-only values from the selected inquiry range |
| Appointment date/time and timezone | Provider-edited option/date fields | Tab 4 | Appointment must fall within the selected range and be in the future when sent; timezone required. Together with the provider, these fields are the key of the FR-006 slot hold placed at acceptance; no appointment record is created at quote time |
| Offered price | Provider-edited option/date field | Tab 4 | Price greater than 0 in the quote currency, stored as entered before any promotion; prefilled from the package standard price, or from the FR-024 treatment Base Price only where no other standard value exists |
| Promotion and promotion terms | Provider-selected option/date reference; system-copied terms | Tab 4 | Optional structured FR-019 promotion. At send, its terms and discount are copied into the sent quote version and shown separately from the offered price; eligible automatic promotions are attached by the system at send |
| Acceptance state | Derived from FR-005 | Tab 7 after FR-005 action | Read-only; derived from the FR-005 subquote state and never stored on the option/date-price record |
| Option plan-day ID and parent Option ID | System-owned | Tab 5 | Stable identifiers; read-only |
| Plan day number and description | Provider-edited option fields | Tab 5 | Consecutive relative day number and required description |
| Child-record created and updated metadata | System-owned audit metadata | Tab 7 / Audit | Applies to options, items, date-price rows, and plan days; read-only |
| Quote version and audit records | System-owned compliance records | Tab 7 / Audit | Complete immutable history of parent and option changes |

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

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Treatment Service | Quote | select | Yes | One admin-curated treatment shared by every option | Must be active; package choices in Tab 2 must belong to this treatment |
| Technique Details | Treatment relationship | read-only text | N/A | Technique information loaded from the selected immutable Treatment version when documented in FR-024 | Never provider-editable or copied into a separate Quote field; show "Not specified" when the Treatment has no technique specifications |

**Behavior**:

- Tab 2 is unavailable until an active treatment is selected.
- The system persists the exact Treatment ID/version relationship and loads technique details through that relationship for display and API responses.
- Changing the treatment after options exist requires confirmation. The system must identify incompatible options and must not silently retain or discard dependent package, pricing, or plan data.

##### Tab 2: Package Options

**Purpose**: Choose the package alternatives and manage their quote-local content.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Package Options | Quote | ordered multiselect | Yes | Packages selected from the authenticated provider's active library; each selected package seeds one Quote Option | Minimum 1; maximum 5; must match Tab 1 treatment; package must be active when selected; packages are never summed into one option |
| Option Order | Option | reorder control | Yes | Patient-facing comparison order | Unique consecutive order within the quote |
| Package Snapshot | Option | read-only summary | Yes | Source package identity/version, standard price, services, included travel services, and relative day plan copied into the quote | Later library edits must not alter the snapshot |
| Edit Package Inline | Option | action | No | Opens Sub-screen 2A for the selected option | Available independently for every option |

###### Sub-screen 2A: Inline Package Editor

**Purpose**: Customize one package option for this quote without modifying the provider's reusable package library.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Option Name and Source | Option | read-only header | Yes | Identifies the option and its source package/version | Must remain traceable to the selected source package |
| Source Item | Option item | read-only reference | No | Identifies the package-library item from which this row was copied | Null only for a service created inside the quote |
| Item Type | Option item | select | Yes | Controlled medical, travel, accommodation, transport, flight, or other service category | Must use an allowed service type |
| Item Name | Option item | text | Yes | Patient-facing service name | Required; maximum 255 characters |
| Item Description | Option item | textarea | No | Patient-facing service details | Maximum 1,000 characters |
| Item Price | Option item | amount | No | Optional component price for transparency | Non-negative; displayed in configured currency; final offered price remains in Tab 4 |
| Included | Option item | toggle | Yes | Whether the service is included in this package option | Explicit true or false |
| Item Order | Option item | reorder control | Yes | Patient-facing order inside the option | Unique consecutive order |
| Item Metadata | Option item | read-only metadata | No | Source or extension data retained by the system | Never free-form provider input |
| Included Travel Services (`included_services`) | Option | checklist | No | Flight, hotel, transport, and other travel services included in this option | Stored only in the option snapshot; no cross-field dependency |
| Add Custom Service | Option | action | No | Adds a patient-specific item with the same type, name, description, price, inclusion, and ordering fields | New item has no source package-item ID |
| Remove Service | Option item | action | No | Removes an item from this option snapshot | Confirmation required; source package remains unchanged |
| Standard Package Price | Option | read-only amount | Yes | Library price used to prefill Tab 4 | Final offered prices are edited only in Tab 4 |
| Save Option Changes | Option | action | Yes | Returns the customized snapshot to Tab 2 | Must update only this Quote Option and its aggregate audit/version state |

**Behavior**:

- Providers may add, edit, include, exclude, or remove services in the option snapshot.
- Sub-screen 2A is the quote inline edit path: it edits a quote-local copy of the package that is saved only on this Quote Option and is never written back to the package library. The first inline change sets the option's inline-customised flag; the source package ID and version stay recorded for provenance.
- Closing or saving Sub-screen 2A never creates or updates a reusable `Package`, a package version, or a package-library item. Changing the reusable package is done only in the FR-024 package management screen.
- Customization examples include medical consultation, maximum graft coverage, PRP injection, Day-3 wash, lifetime warranty, language translator, hotel, local transport, airport transfer, and flight.
- Removing an option also removes its draft date-price rows and draft treatment plan after explicit confirmation; at least one option must remain before submission.

##### Tab 3: Grafts & Visual Plan

**Purpose**: Record treatment facts that apply equally to every package option.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Estimated Grafts | Quote | number | Yes | Provider-entered estimate shared by every option | Provider may enter and revise a positive integer |
| Graft Description | Quote | read-only text | Yes | System-generated explanation based on the approved template and the current Estimated Grafts value | Regenerated whenever Estimated Grafts changes; providers cannot edit it directly; retained in aggregate versions |
| Visual Treatment Plan / 3D Markup | Quote | drawing/upload | No | Shared visual plan or markup | Supported file/media rules; stored in the aggregate version |

##### Tab 4: Dates & Pricing

**Purpose**: Combine treatment-date selection and pricing in one package-first configuration surface.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Package Option | Option | repeated section | Yes | One section per option selected in Tab 2 | All options shown in Tab 2 order |
| Applicable Treatment Dates | Option | multiselect | Yes | Patient-requested ranges for which this option is offered | At least one per option; subset of FR-003 ranges |
| Appointment Slot | Option/date | datetime | Yes | Appointment start for this option/date combination | Must fall within its selected range; timezone required |
| Offered Price | Option/date | amount | Yes | Price for this package option on this date range, as entered by the provider before any promotion | Must be greater than 0; a zero or negative price blocks send; quote currency; prefilled from the package standard price, or from the FR-024 treatment Base Price only where no other standard value exists, and editable |
| Promotion | Option/date | select-or-create | No | Structured promotion applied to this option/date price; the discount is shown separately from the offered price | Must resolve to a valid `PromotionProgram`; no free-text promotion; terms are copied into the quote version at send |
| Configured Currency | Quote | read-only label | Yes | Quote currency from the active FR-026 quote configuration (the FR-029 Default Currency), used across every option/date price | Never provider-editable; captured onto the quote at first send; packages carry no currency of their own; if the Default Currency changes while the draft holds prices, the draft switches to the new currency with typed numbers kept and shows a "currency changed, check your prices" banner |

**Behavior**:

- The selected packages drive the screen: configure date applicability and pricing option by option until the option list is complete.
- An option may apply to all patient-requested ranges or only a subset, but at least one. The provider may leave out any option/date pairing it cannot offer.
- Each option/date-range pairing appears at most once per option.
- Every range marked applicable must have its own appointment slot and offered price; unavailable combinations are omitted rather than priced. Each priced pairing becomes one subquote for FR-005.
- Every option/date price must be greater than 0. A zero price is blocked with an inline error on that row; a date range the clinic cannot serve is left out of that option instead of being priced at zero.
- The FR-024 treatment Base Price is a reference-only, non-binding "starting from" value. It may prefill a new row only where no other standard value exists, such as a package standard price, and it is never read after the quote is sent.
- If the FR-029 Default Currency changes while a draft holds prices, the draft switches to the new currency, every typed number is kept unchanged, and a "currency changed, check your prices" banner is shown. The provider must acknowledge the banner before the quote can be sent.
- `included_services` comes from the corresponding Tab 2 option snapshot. After FR-005 acceptance, FR-008 derives `travel_path` from the accepted option.

##### Tab 5: Option Treatment Plans

**Purpose**: Define a different day-to-day treatment plan for each package option.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Package Option | Option | selector/section | Yes | Chooses the option whose plan is being edited | Every option requires a plan |
| Day Number | Option | number | Yes | Relative sequential day index | Starts at 1; consecutive with no gaps |
| Day Description | Option | text | Yes | What happens on that relative treatment day | Required; maximum 1,000 characters |

**Behavior**:

- Each option's plan is prefilled from the relative day-by-day plan of its source package version; edits apply only to this option.
- Plans use relative day numbers because one option can be offered across multiple date ranges.
- Relative day numbers are never resolved to stored calendar dates. Downstream consumers (FR-005 comparison, FR-010 In Progress) present the plan by day number against the accepted appointment.

##### Tab 6: Clinical Details & Notes

**Purpose**: Record remaining information that applies to all options in the parent quote.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Clinicians | Quote | multiselect | Yes | One or more responsible clinicians shared by every option | At least one; every clinician must be active, eligible, and belong to the provider |
| Common Notes | Quote | textarea | No | Additional provider information applying to every option | Maximum 5,000 characters |
| Common Requirements | Quote | textarea/repeater | No | Patient or treatment requirements shared by every option | Maximum 5,000 characters per entry; empty entries rejected |
| Attachments | Quote | multi-file upload | No | Quote-level images, videos, or documents applying to every option | Maximum 5 files; JPG/PNG up to 5 MB each; MP4/PDF up to 10 MB each; virus scan, retention, and access rules enforced |

##### Tab 7: Review & Submit

**Purpose**: Review the complete quote aggregate and resolve missing information before submission.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Quote, Inquiry, and Provider References | Quote | read-only context | Yes | Stable quote ID plus source inquiry and authenticated provider | System-owned; must match the active quote context |
| Shared Quote Summary | Quote | read-only group | Yes | Treatment, graft facts, visual plan, clinicians, notes, requirements, and attachments | Must reflect the latest saved values from Tabs 1, 3, and 6 |
| Package Comparison | Quote aggregate | read-only cards/table | Yes | Ordered options with inclusions, date prices, and plans | Must reflect Tabs 2, 4, and 5 |
| Configured Currency | Quote | read-only label | Yes | Currency applied to all displayed prices | From the active FR-026 quote configuration; captured at first send; never provider-editable |
| Calculated Price Range / Accepted Total | Quote | read-only amount | Yes | Price range before acceptance and accepted total after FR-005 acceptance | Price range derived from the complete Tab 4 matrix; accepted total written from the FR-005 acceptance snapshot |
| Commission | Quote | read-only model and value (percentage or flat rate) | Conditional | Commission model and value shown only to authorized roles, labelled "indicative, final at booking confirmation" | From the active FR-029 configuration; never provider input; the binding commission is fixed at booking confirmation |
| Quote Status | Quote | read-only badge | Yes | Current governed lifecycle state | System-owned enum |
| Expiry | Quote | read-only datetime | Yes | Deadline for the complete quote; shown as "set on first send" while drafting | Captured at first send from the FR-026 quote expiry setting |
| Created, Updated, and Last Edited | Quote | read-only metadata | Yes | System timestamps and last authenticated editor | System-generated |
| Option Customization State | Option | read-only badge | Yes | Shows the source package and version and whether each option has been customised inline; warns when the source package has since been edited or deactivated | System-derived from option-item changes and the FR-024 package state |
| Downstream Acceptance and Lifecycle Metadata | Quote | read-only group | Conditional | Terms acknowledgment, exchange-rate lock, cancellation/supersession provenance, affiliate attribution, and travel-responsibility state | Visible only when populated and authorized; never edited in Screen 1 |
| Version and Audit Summary | Quote aggregate | read-only links | Yes | Current version and immutable change history | Must cover parent and all option-owned records |
| Validation Summary | Quote aggregate | read-only checklist | Yes | Shows complete tabs and links each issue to its owning tab | No unresolved blocking issue |
| Submit Quote | Quote aggregate | action | Yes | Submits parent and options as one transaction | Revalidate inquiry, authorization, option count, and every tab gate; blocked while any option/date price is not greater than 0 or an unacknowledged "currency changed, check your prices" banner is shown |

#### Screen 2: Quote List (Unified; no tabs)

**Purpose**: Provider views all quotes in a single unified list

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient ID | column | Yes | Anonymized ID | Searchable |
| Name | column | Yes | Partly censored name | Masking applies |
| Age | column | No | Patient age | Number; sortable |
| Problem/Concern | column | No | Primary concern | Filterable |
| Treatment & Options | column | Yes | Shared treatment and option count | Read-only; show 1–5 options |
| Date Ranges Quoted | column | Yes | Distinct ranges offered across options | Tooltip groups ranges by option |
| Price Range | column | Yes | Lowest to highest option/date price | Currency formatting; derived from matrix |
| Location | column | No | Patient country | Filterable |
| Medical Alerts | column | Yes | Alert chips | Severity colors |
| Quoted Date | column | Yes | Quote created date | Relative formatting rules |
| Action | column | Yes | Edit, Soft Delete, View Details | State-aware |
| Search/Filters | control | No | Patient/Inquiry/Treatment/Date/Status/Location/Alerts | Valid enums/ranges |

**Notes**:

- Unified list (no tabs) to reflect global case statuses
- Quotes with status "Cancelled (Inquiry Cancelled)" are displayed with greyed-out row styling and an "Inquiry Cancelled" badge; all action buttons disabled
- Quotes with status "cancelled (other accepted)" are similarly greyed-out with "Another Quote Accepted" badge

#### Screen 3: Quote Details Screen

**Purpose**: Inspect full quote details and act (patient-first continuation from inquiry)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient (Anonymized) | group | Yes | Anonymized ID, masked name, age, location | Contact hidden until payment |
| Inquiry Context | group | Yes | Continuation data from FR-003 | Read-only |
|  • Countries | list | Yes | Selected treatment countries | From inquiry |
|  • Problem Details | group | Yes | Concern, duration, previous treatments | From inquiry |
|  • Medical Alerts | chips | Yes | Critical/Standard/None | Derived from questionnaire |
|  • Requested Date Ranges | list | Yes | All patient-requested ranges | Read-only |
|  • Media/Scan | links/viewer | No | Photos/videos/3D scan viewer | Read-only |
| Quote Summary | group | Yes | Shared treatment facts, common notes, expiry, and option count | Read-only |
| Quote Options | comparison cards/table | Yes | Ordered package snapshots with option-local inclusions and services | One to five options |
| Option Date Prices | matrix | Yes | Applicable date ranges, appointment slots, and prices for each option | Every applicable combination shown; currency rules |
| Option Treatment Plan | table | Yes | Package-specific relative day plan | Grouped by option; consecutive day numbers |
| Estimated Grafts | number | Yes | Estimated graft count | Positive integer |
| Promotion | reference | No | Structured promotion applied to an option/date price, with its discount shown separately from the offered price | Read-only; shows the promotion terms copied into the sent quote version, never the live FR-019 terms |
| Clinicians | list | Yes | Responsible clinicians shared by every option | At least one; each must be eligible |
| 3D Markup | viewer | No | Drawings over 3D image | Read-only snapshot |
| Common Notes and Requirements | text | No | Provider information applying to every option | Read-only |
| Attachments | file list/viewer | No | Quote-level files applying to every option | Read-only; access and retention rules enforced |
| Expiry | datetime | Yes | Computed deadline | From admin window |
| Provider Info | group | Yes | Provider/practice info | Read-only per policy |
| Actions | actions | Yes | Edit / Soft Delete (if eligible) | State policy enforced |
| Audit/Version | modal | Yes | Version history and audit log | Immutable audit |

**Notes**:

- UI may use a tabbed interface defaulting to Patient tab, then Inquiry, then Quote, then Audit
- Patient-first ordering ensures natural continuation from inquiry to quote data
- If quote is in "Cancelled (Inquiry Cancelled)" status, display a prominent "Inquiry Cancelled" banner at the top of the detail view; all edit/delete actions disabled; quote data remains read-only for reference
- If provider was actively drafting when inquiry was cancelled, the banner appears on next save/refresh with message: "This inquiry was cancelled by the patient. Your draft can no longer be submitted."

### Patient Platform (Read-only for this module)

#### Screen 4: Quote Review

**Purpose**: Patient reviews parent quotes and their subquotes; acceptance of one subquote is governed by FR-005

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote List | list | Yes | Parent quotes grouped by inquiry and provider | Read-only; separate quote and option counts |
| Treatment | text | Yes | Selected treatment | Read-only |
| Quote Options | comparison cards/table | Yes | One to five package options within the selected quote | Read-only in FR-004; selection governed by FR-005 |
| Price Breakdown | matrix | Yes | Price for every applicable option/date combination, with any promotion discount shown separately | Currency rules |
| Inclusions and Services | list | Yes | Snapshot of inclusions and quote-local customizations | Grouped by option; read-only |
| Treatment Plan | table | Yes | Different day-to-day plan for each option | Grouped by option; read-only |
| Attachments | file list/viewer | No | Quote-level supporting files | Read-only; patient access rules enforced |
| Status | badge | Yes | Parent quote status mapped from the Key Entities enum: Sent (shown as Awaiting Decision), Accepted, Expired, Withdrawn, Cancelled (Inquiry Cancelled), Cancelled (Other Accepted), and Cancelled (Provider Status) shown as Offer Unavailable; each subquote also shows its FR-005 state, including Not Selected | Enum validation; drafts and archived quotes are never shown to patients; visual treatment per state (e.g., greyed-out for cancelled/expired) |
| Expiration Timer | timer | Yes | Countdown to expiry | From admin window |
| Provider Info | group | Yes | Allowed provider details | Privacy rules |
| Actions | actions | Yes | Accept one subquote (FR-005); there is no parent-level Accept or Decline action | State & confirmation rules owned by FR-005 |
| Notifications | note | No | New/updated/expired indicators | Read-only |

**Governance Note**: This screen’s field/visual specification is defined here in FR-004, but the end-to-end patient quote comparison and acceptance flows (including edge cases, blocking rules, and booking handoff) are governed primarily by **FR-005: Quote Comparison & Acceptance (P-02)**. FR-005 may extend or refine the actions on this screen while preserving the privacy constraints and data structure specified in FR-004.

### Admin Platform

#### Screen 5: Quote List (Admin)

**Purpose**: Admin lists and filters all quotes (multiple providers per inquiry)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Global Quote Table | table | Yes | All quotes with columns & filters | Admin-only |
| Patient ID | column | Yes | Anonymized ID | Searchable |
| Name | column | Yes | Partly censored name | Masking applies |
| Age | column | No | Patient age | Number; sortable |
| Problem/Concern | column | No | Primary concern | Filterable |
| Treatment & Options | column | Yes | Shared treatment and option count | Read-only; show 1–5 options |
| Date Ranges Quoted | column | Yes | Distinct ranges offered across options | Tooltip groups ranges by option |
| Price Range | column | Yes | Lowest to highest option/date price | Currency formatting; derived from matrix |
| Location | column | No | Patient country | Filterable |
| Medical Alerts | column | Yes | Alert chips | Severity colors |
| Quoted Date | column | Yes | Quote created date | Relative formatting rules |
| Provider | column | Yes | Provider/clinic | Filterable |
| Actions | column | Yes | Restore/Archive/View Detail | State-aware; Restore and Archive are hidden for `accepted` quotes |
| Search/Filters | control | No | Patient/Inquiry/Treatment/Date/Status/Location/Alerts/Provider. Status filter includes: draft, sent, expired, withdrawn, archived, accepted, cancelled_other_accepted, cancelled_inquiry_cancelled, cancelled_provider_status | Valid enums/ranges |
| Inquiry Grouping | control | Yes | Default: grouped by inquiry | Toggle grouping |
| Multi-Quote Cue | badge/icon | No | Visual cue for multiple quotes in inquiry | Shows count or indicator |
| Audit Trail | modal | Yes | Per-quote audit (who/what/when/prev value) | Immutable |
| Version History | modal | Yes | Full version history | Immutable |

#### Screen 6: Quote Detail (Admin)

**Purpose**: Admin views complete quote with inquiry continuation

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Selector | dropdown/list | Yes | Switch between quotes for this inquiry | Must belong to same inquiry |
| Quote Summary | group | Yes | Shared treatment facts, common notes, expiry, and option count | Read-only |
| Quote Options | comparison cards/table | Yes | Package snapshots, option-local inclusions, and source-package provenance | One to five options |
| Option Date Prices | matrix | Yes | Applicable date ranges, appointment slots, and prices by option | Complete for every applicable combination |
| Option Treatment Plans | table | Yes | Relative day plan grouped by package option | Consecutive day numbers per option |
| Estimated Grafts | number | Yes | Estimated graft count | Positive integer |
| Promotion | reference | No | Structured promotion applied to an option/date price, with its discount shown separately from the offered price | Read-only; shows the promotion terms copied into the sent quote version, never the live FR-019 terms |
| Clinicians | list | Yes | Responsible clinicians shared by every option | At least one; each must be eligible |
| 3D Markup | viewer | No | Drawings over 3D image | Read-only snapshot |
| Common Notes and Requirements | text/list | No | Provider information applying to every option | Read-only |
| Attachments | file list/viewer | No | Quote-level supporting files | Read-only; access and retention rules enforced |
| Expiry | datetime | Yes | Computed deadline | From admin window |
| Provider Info | group | Yes | Provider/practice info | Read-only |
| Inquiry Context | group | Yes | Countries, problem, alerts, ranges, media/scan | From FR-003 |
| Audit Trail | log | Yes | Full change history | Immutable |
| Version History | list | Yes | Quote versions | Immutable |

#### Screen 7: Admin Inline Quote Edit

**Purpose**: Admin performs limited inline edits with audit on draft or sent quotes only

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Selector | dropdown/list | Yes | Select target quote under inquiry | Must belong to same inquiry |
| Quote Option | selector | Yes | Select the package option being edited | Must belong to the selected quote |
| Option/Date Price | matrix | Cond. | Edit applicability, appointment slot, or price for an option/date combination | Reason required; matrix must remain complete |
| Package Inclusions | inline option editor | Cond. | Edit the option snapshot without changing the package library | Reason required |
| Estimated Grafts | number | Cond. | Adjust graft count. Saving a new value regenerates Graft Description from the approved template; the prior text is not preserved | Positive integer; reason required |
| Option Items | repeater | Cond. | Add/edit/remove items within the selected option snapshot | Same fields as Sub-screen 2A — Item Name, Item Type, Included flag, Item Order, and Item Price (optional); item order consecutive with no gaps; reason required |
| Treatment Plan (per-day) | repeater | Cond. | Edit the selected option's relative day plan | Consecutive day numbers; reason required |
| Promotion | select-or-create | Cond. | Add, replace, or remove the structured promotion on an option/date price of a draft or sent quote. Inline create permitted with `scope = AD_HOC_QUOTE_BOUND` per FR-019 Screen 9 Mode 2 | Must resolve to a valid PromotionProgram id or null; reason required; the change creates a new quote version into which the current promotion terms are copied |
| Notes | textarea | No | Admin note | Stored with audit |
| Clinicians | multiselect | Cond. | Change the shared clinician assignments | At least one; each must be active, eligible, and belong to the provider; reason required |
| Attachments | multi-file upload | Cond. | Add or remove quote-level supporting files | File/access rules and reason required |
| Audit Reason | textarea | Yes | Reason for change | Required for any edit |

**Notes**:

- All inline edits auditable (who/when/before/after, reason). An admin edit of a sent quote creates a new quote version and emits `quote.updated` when that version is re-sent; draft edits emit nothing
- Screen 7 is available only for `draft` and `sent` quotes. Once a subquote of the quote is accepted, every Screen 7 edit is blocked; the accepted snapshot is the record, and later treatment-detail changes (plan, clinicians, grafts) are made only through FR-010 with audit and patient notice. Accepted, expired, withdrawn, archived, and cancelled quotes are read-only.

#### Screen 8: Admin Replacement Quote Authoring

**Purpose**: Admin authors a quote for the replacement provider during an FR-006 provider-fault transfer (Workflow 7)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Transfer Context | group | Yes | Inquiry, closed booking, provider-fault cause, and the closed AcceptanceEvent with its snapshot | Read-only; opened only from the FR-006 transfer; booking must be closed with `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated` before treatment started |
| Replacement Provider | reference | Yes | Provider chosen in the FR-006 transfer | Read-only here; must be `Active` and must not be the provider at fault |
| Treatment | select | Yes | Shared treatment for the replacement quote | From the admin-curated catalog; prefilled from the closed acceptance |
| Quote Options | inline option editor | Yes | One to five options seeded from the replacement provider's active packages | Same option rules as Screen 1; quote-local copies only |
| Option/Date Price | matrix | Yes | Date range, appointment date/time, time zone, and price for each applicable option/date pairing | Price greater than 0; date range from the inquiry; appointment within the range |
| Estimated Grafts | number | Yes | Shared graft estimate | Positive integer; Graft Description regenerated from the template |
| Treatment Plan (per-day) | repeater | Yes | Relative day plan per option | Consecutive day numbers |
| Clinicians | multiselect | Yes | Shared clinicians of the replacement provider | At least one; each active, eligible, and belonging to that provider |
| Notes and Attachments | text/files | No | Common notes, requirements, and supporting files | Same limits as Screen 1 |
| Adjustment Reason | textarea | Yes | Why the package or price differs from the closed acceptance, or why it is unchanged | Required; stored in the quote audit |
| Actions | buttons | Yes | Save Draft, Save and Continue to Acceptance, Cancel | Save and Continue validates every field and returns to the FR-006 transfer to record the acceptance |

**Notes**:

- Confirmation: Save and Continue shows a confirmation that summarises the replacement provider, options, prices, and appointment, and states that the patient will not compare this quote and that the admin records the acceptance next.
- Audit: every save writes a quote audit entry with admin, time, before and after values, and the adjustment reason; the quote is marked admin-authored for a replacement and linked to the closed AcceptanceEvent.
- Notices: authoring the quote sends no notice. When the replacement acceptance is recorded, the patient receives `booking.scheduled` and the replacement provider receives `quote.accepted`; the patient and admin are told of the transfer through FR-006 `booking.provider_fault_replacement`.
- Screen 8 is unavailable for a booking in `In Progress` or later stages and for any inquiry with an active acceptance.
- Price: the admin sets each option/date price directly. Screen 8 offers no promotion field, no automatic FR-019 promotion attaches, and no promotion usage reservation is taken.
- Expiry: a replacement quote that is not accepted expires under the normal quote expiry. The inquiry stays `supportRequired`, and the admin may open Screen 8 again to author another replacement quote or cancel the inquiry and booking in FR-006.

## Business Rules

- Quotes MUST reference distributed inquiry ID and be linked to original patient object
- Quote data MUST append to inquiry data; no reduction or overwriting of inquiry-supplied fields. Downstream stages inherit upstream data.
- Only assigned clinic staff may submit/edit quotes for assigned inquiries
- Treatment type selection MUST use admin-curated treatment catalog; no free text
- Graft/quantity, option/date prices, and scheduled slots MUST be present and valid
- Every option/date price MUST be greater than 0 before send; a zero price is blocked. A date range the clinic cannot serve is left out of that option rather than priced at zero
- A provider may submit multiple parent quotes for the same inquiry; each quote has an independent identity, lifecycle, expiry, versions, and audit history
- Each quote MUST contain at least one and at most five ordered Quote Options
- Every Quote Option MUST originate from a package that is active in the authenticated provider's package library when it is selected. If the source package is later edited or deactivated, existing draft and sent options keep their snapshot; a draft may still be submitted, and Tab 7 shows a warning that the source package has changed or is inactive
- Each selected package seeds exactly one alternative Quote Option, up to five per parent quote; packages are never summed or merged into one option. The package seeds services and their pricing, included travel services, the standard price, and the relative day-by-day plan; date ranges, additional notes, and documents are entered per quote
- Package selection occurs after the shared treatment is selected; every option in the quote MUST use that parent treatment
- Selecting a package MUST create a quote-owned snapshot. Inline option customization MUST NOT update or create reusable package-library records
- Package-library changes after snapshot creation MUST NOT alter existing draft or sent options unless the provider explicitly replaces the source package and confirms a new snapshot
- **Package library edits and quote inline edits**: There are two distinct edit paths. (1) Editing a package in the FR-024 package management screen changes the reusable library package: each saved edit creates a new package version, earlier versions stay read-only, and existing quotes never change. (2) Editing a package inside quote creation (Sub-screen 2A, Tab 5, and Tab 4 prices) changes only a quote-local copy saved on that Quote Option; it is never written back to the library and never creates a package version. Each Quote Option records its source package ID, source package version, and whether it was customised inline
- Each option MUST identify at least one applicable patient-requested date range and provide a price and appointment slot for every applicable option/date combination. The provider MAY leave out any option/date pairing it cannot offer, so a parent quote yields up to (options × date ranges) subquotes. Each pairing MAY appear only once per option, and the package standard price prefills each applicable row
- Estimated grafts, graft description, visual treatment plan, clinicians, common notes, and common requirements belong to the parent quote and MUST NOT be duplicated as option-specific facts
- Quote-level attachments apply to every option and MUST follow platform file-access, audit, and retention rules
- Quote currency MUST come from the active FR-026 quote configuration, whose currency is the FR-029 Default Currency; it MUST be captured onto the quote at first send, kept for historical integrity, and displayed read-only. Drafts carry no captured currency. Packages carry no currency of their own. Providers MUST NOT enter or change it in the quote. If the Default Currency changes while a draft holds prices, the draft switches to the new currency, the typed numbers are kept, and a "currency changed, check your prices" banner must be acknowledged before the quote can be sent
- The parent quote MUST record its first-send timestamp (`firstSentAt`) when it is first sent; a re-send or new version never changes it
- The FR-024 treatment Base Price is a reference-only, non-binding "starting from" value. It MAY prefill a new option/date-price row only where no other standard value exists, and it is never read after the quote is sent
- Quote expiry MUST be captured at first send by copying the FR-026 quote expiry setting read-only onto the quote. Drafts carry no expiry; later setting changes never affect sent quotes; there is no per-quote extension
- Providers MAY enter and revise the Estimated Grafts value. The system MUST automatically generate and regenerate the Graft Description from the approved system template and the current Estimated Grafts value. Providers MUST NOT directly edit the Graft Description.
- Included services, custom services, date applicability/pricing, promotions, and the day-to-day plan belong to the Quote Option or its option/date price record
- Analytics MUST distinguish parent quote responses from Quote Options so option counts do not inflate quote-response or conversion metrics
- Quote-amount analytics MUST use only the accepted option/date price. A quote with no acceptance has a price range rather than an amount and MUST be excluded from amount metrics, while still counting as one response in volume and conversion metrics
- Quotes CANNOT be hard deleted (only archived/soft deleted)
- All state transitions (draft→sent→expired, etc.) MUST be fully auditable
- Providers and admins may edit a quote only while it is `draft` or `sent`. Once a subquote is accepted, FR-004 blocks every quote edit; treatment details (plan, clinicians, grafts) change only through FR-010 with audit and patient notice; price, currency, date range, and promotion never change; and the booking's appointment changes only through the FR-006 admin appointment change, with the acceptance snapshot keeping the accepted appointment as the baseline
- `sent` quotes MUST expire automatically on reaching their expiry timestamp; `accepted`, withdrawn, archived, and cancelled quotes are never expired
- Each inquiry may have multiple parent quotes from multiple providers or from the same provider. Package alternatives within a parent quote are Quote Options, not independent quote responses
- Discounts are provider-managed (reviewed by admin if above configured threshold)
- **Promotions on quotes**: The offered price is stored as entered by the provider, and any promotion discount is stored and shown separately. At each send, the system copies the terms and discount value of every attached promotion into the sent quote version; later edits to the FR-019 promotion never change a sent quote. At send, the system also attaches at most one automatic FR-019 promotion per quote to each eligible option/date-price row; when several automatic promotions qualify, the FR-019 priority order picks one. The accepted price is the price after promotion, which FR-005 freezes into the acceptance snapshot; FR-004 never changes it after acceptance. A sent quote carrying an automatic promotion holds exactly one reserved use of that promotion's usage limit, and a re-send of a new version keeps that reservation rather than adding a second one; the reservation is released when the quote expires, is withdrawn, or ends not selected or cancelled, or when the accepted row does not carry the promotion (`not_applied`), and the use is consumed when the accepted row carries it, so the usage limit can never be exceeded. An automatic promotion with no uses left is not eligible and is not attached
- **Commission display**: The quote shows the commission model and value (percentage or flat rate) only as an indicative figure labelled "indicative, final at booking confirmation"; the binding commission is fixed at booking confirmation on the accepted price after promotion, in the quote currency, read from the acceptance snapshot (FR-029)
- All notifications MUST comply with platform notfication/audit/logging rules
- GDPR/data compliance: all quote objects are archived for ≥7 years
- Patient information remains censored at this stage until payment confirmation; only anonymized identifiers and allowed fields are visible to providers.
- Providers must select option applicability from patient-requested date ranges; each applicable option/date combination must have a specific price and appointment slot.
- Only a provider in `Active` status may create, edit, or submit quotes. A provider's effective `Suspended` or `Deactivated` status revokes quote submission and cancels that provider's unaccepted parent quotes under Workflow 3 and FR-015 A5/Screen 4; the provider-caused cause is distinct from patient inquiry cancellation and Payment Window Expired. An already-accepted quote is never cancelled this way; FR-006 handles it through the provider-fault transfer.
- Provider withdrawal after acceptance moves the parent quote from `accepted` to `withdrawn` and hands the case to the FR-006 provider-fault transfer (Workflow 6); FR-004 never re-routes, reopens, or edits the accepted quote.
- During an FR-006 provider-fault transfer before treatment starts, an admin may author a replacement quote for the replacement provider inside the same inquiry (Workflow 7, Screen 8). It is the only exception to the block on new quotes after acceptance, is marked admin-authored for a replacement, and is never offered for patient comparison. The admin sets its price directly; no automatic promotion attaches and no promotion reservation is taken. If it is not accepted it expires under the normal quote expiry, the inquiry stays `supportRequired`, and the admin may author another replacement quote or cancel.
- `confirmed` is a booking status owned by FR-006, never a quote status; an accepted quote stays `accepted`.
- System MUST verify parent inquiry is not in Cancelled status before accepting quote creation or submission. If inquiry is cancelled mid-draft (race condition), system rejects submission with error "Inquiry no longer active" and locks the draft with "Inquiry Cancelled" banner. See FR-003 Workflow 5 edge case.
- **Restricted recipient mode**: If the inquiry was created via an FR-037 monitoring-case conversion with an active exclusive provider assignment (REQ-037-029, Business Rule 7; see FR-003 Workflow 2 Alternative Flow B3), only that assigned provider may create quotes for the inquiry, including any additional parent quote. Any other provider attempting to open the inquiry for quote creation is blocked with error "This inquiry is restricted to its assigned provider." The restriction does not change the other workflows (editing, expiry, withdrawal, admin oversight) on quotes that already exist. FR-038 is self-service and does not create an FR-004 inquiry or provider assignment.

## Success Criteria

- **SC-001**: 100% of distributed inquiries receiving valid quotes from ≥1 provider within 72h
- **SC-002**: 100% of quote edits and deletions reflected in version/audit history
- **SC-003**: 95% of subquote acceptance actions complete with the correct selected-parent, sibling, and competing-parent status updates and notifications
- **SC-004**: <5% of provider quote rejections due to missing/invalid fields
- **SC-005**: 0 hard deletes of quotes; 100% retrievable from archive for ≥7 years
- **SC-006**: 100% of submitted quotes contain one to five complete options, with no quote-local customization written into the reusable package library

## Functional Requirements Summary

### Core Requirements

- **REQ-004-001**: Providers MUST create, edit, and submit parent quotes with one shared immutable Treatment-version relationship and one to five package-based Quote Options. Technique details MUST be loaded read-only through that relationship and MUST NOT be duplicated as provider-entered Quote data.
- **REQ-004-002**: System MUST enforce the admin-controlled FR-026 expiry window (default 48h), captured at first send, and compute the deadline per sent quote.
- **REQ-004-003**: System MUST cancel every other parent quote for the same inquiry as `cancelled_other_accepted` upon one subquote acceptance. Each sent parent quote MUST produce one not-selected notice per parent quote; unsent drafts MUST be cancelled silently without notice.
- **REQ-004-004**: System MUST support provider withdrawal after acceptance by moving the parent quote to `withdrawn`, keeping the AcceptanceEvent and snapshot unchanged, and handing the case to the FR-006 provider-fault transfer, with full audit and the mandatory `quote.withdrawn` notice.
- **REQ-004-005**: Admin MUST be able to inline edit policy-bound fields of `draft` and `sent` quotes with required reason and re-notifications; admin edits MUST be blocked once a subquote is accepted.

### Data Requirements

- **REQ-004-006**: Quotes MUST reference original inquiry and patient; quote data appends, never overwrites inquiry data.
- **REQ-004-007**: All quote edits and state transitions MUST be versioned and auditable.

### Security & Privacy Requirements

- **REQ-004-008**: Patient identifiers MUST remain anonymized to providers until payment confirmation.
- **REQ-004-009**: All quote data MUST be encrypted at rest and in transit; soft deletes only.

### Integration Requirements

- **REQ-004-010**: Module MUST integrate with FR-003 for inquiry context and FR-020 for notifications.
- **REQ-004-011**: Admin settings (quote expiry window, quote-expiring-soon lead time, and quote currency) MUST be applied from the FR-026 quote configuration.

### Clarifications

- **REQ-004-012**: Money handling for provider withdrawal after acceptance follows the FR-006 provider-fault placeholder; exact refund and payment-allocation mechanics are owned by FR-007, FR-007B, and FR-017.

### Cancellation Cascade Requirements

- **REQ-004-013**: System MUST auto-cancel ALL quotes for an inquiry when that inquiry is cancelled by the patient (FR-003 Workflow 5), with distinct status "Cancelled (Inquiry Cancelled)" and provider notifications via `quote.cancelled_inquiry` event (FR-020).
- **REQ-004-031**: System MUST revalidate provider status at quote creation and submission and MUST reject quote submission by a `Suspended` or `Deactivated` provider from the effective time, including in-flight requests.
- **REQ-004-032**: When a provider becomes `Suspended` or `Deactivated`, System MUST cancel that provider's unaccepted parent quotes with status `cancelled_provider_status` and `cancellationProvenance` `ProviderSuspended` or `ProviderDeactivated`, once per parent quote rather than per option or option/date alternative, without rewriting the AcceptanceEvent, accepted IDs/versions, or quote-local package snapshots, and without reclassifying terminal or completed history. An accepted parent quote MUST NOT receive `cancelled_provider_status`; it keeps `accepted` and is handled by the FR-006 provider-fault transfer. Processing MUST be deduplicated per provider-status event and quote.

### Quote Option Requirements

- **REQ-004-014**: System MUST allow the same provider to create multiple parent quotes for one active inquiry; every quote retains an independent lifecycle, expiry, version history, and audit history.
- **REQ-004-015**: Each quote MUST contain between one and five ordered Quote Options, and submission MUST be blocked outside that range.
- **REQ-004-016**: Each Quote Option MUST retain the selected provider package ID/version and a stable, versioned quote-owned snapshot of its inclusions and standard values.
- **REQ-004-017**: Providers MUST be able to customize every selected package inline for the current quote without updating or creating reusable package-library records.
- **REQ-004-018**: Each Quote Option MUST define at least one applicable patient-requested date range and a price, appointment date/time, timezone, and optional structured promotion for every applicable option/date combination. Pairings the provider cannot offer MAY be left out.
- **REQ-004-019**: Each Quote Option MUST own a separate ordered day-to-day treatment plan using consecutive relative day numbers.
- **REQ-004-020**: Estimated grafts, graft description, visual treatment plan, clinicians, common notes, and common requirements MUST remain shared parent-quote fields.
- **REQ-004-021**: Quote version and audit records MUST capture the complete parent-and-options aggregate atomically, including option additions/removals, package snapshots, inclusion changes, date-price changes, and option plan changes.
- **REQ-004-022**: FR-004 MUST expose stable identifiers for the parent quote, Quote Option, and option/date price so FR-005 can record exactly one accepted option/date combination. FR-004 versions the complete parent quote aggregate atomically; therefore, the FR-005 `subquoteVersion` MUST equal the owning parent quote's current `QuoteVersion`. Quote Options and option/date-price records do not have independent revision counters.
- **REQ-004-023**: Provider Quote Creation/Edit MUST use the ordered seven-tab flow defined in Screen 1, including Sub-screen 2A for quote-local package editing and one combined Dates & Pricing tab driven by the selected package options.
- **REQ-004-024**: Every Quote, Quote Option, option item, option/date price, and option plan-day field MUST follow the Screen 1 Quote Data Ownership Matrix, with exactly one provider-editing surface or an explicit read-only/system-derived owner.
- **REQ-004-025**: Quote currency MUST come from the active FR-026 quote configuration (the FR-029 Default Currency), MUST NOT be provider input, and MUST be captured on the quote at first send so historical prices retain their original currency.
- **REQ-004-026**: Providers MUST be able to attach quote-level supporting files that apply to every option; file security, access, audit, and retention rules MUST be enforced.
- **REQ-004-027**: A quote MUST support one or more eligible clinician assignments shared across every option.
- **REQ-004-028**: Graft description MUST be generated from the approved system template and estimated graft count, displayed read-only, and versioned with the quote.
- **REQ-004-029**: System-owned identifiers, lifecycle status, price summaries, commission, timestamps, customization state, and version/audit metadata MUST be visible only where authorized and MUST NOT be provider-editable.
- **REQ-004-030**: Quote-amount analytics MUST be computed from the accepted option/date price only. Unaccepted quotes MUST be excluded from amount metrics and counted once as a parent response in volume and conversion metrics; Quote Options MUST NOT be counted as responses.

### Quote Lifecycle and Pricing Requirements

- **REQ-004-033**: Each selected package MUST seed exactly one alternative Quote Option (maximum five per parent quote), never summed with another package. The package standard price MUST prefill each applicable option/date-price row, and the package's relative day plan MUST prefill the option plan.
- **REQ-004-034**: Editing a package in the FR-024 package management screen MUST change only the library (as a new package version), and editing inside quote creation MUST change only a quote-local copy that is never written back. Each Quote Option MUST record its source package ID, source package version, and an inline-customised flag.
- **REQ-004-035**: System MUST store the offered price as entered and any promotion discount separately, MUST copy the terms of every attached promotion into the sent quote version at send, and MUST attach at most one automatic FR-019 promotion per quote to each eligible option/date-price row at send, chosen by the FR-019 priority order when several qualify. Later FR-019 promotion edits MUST NOT change a sent quote.
- **REQ-004-036**: System MUST capture the quote expiry and quote currency read-only at first send from the FR-026 quote configuration. Drafts MUST carry neither, and there MUST be no per-quote expiry extension.
- **REQ-004-037**: After a subquote is accepted, System MUST block every FR-004 quote edit by providers and admins. Treatment-detail changes (plan, clinicians, grafts) MUST go through FR-010. An accepted parent quote MUST never be reopened, expired, or restored to an acceptable state, including after `Payment Window Expired`, and no new parent quote MAY be created or sent for an inquiry with an accepted subquote, except the admin-authored replacement quote of REQ-004-048.
- **REQ-004-038**: The Quote Option appointment date/time and time zone, together with the provider, MUST be the key FR-006 uses for the slot hold placed at acceptance; FR-004 MUST NOT create an appointment record.
- **REQ-004-039**: System MUST emit `quote.expiring_soon` once per sent parent quote when it reaches the FR-026 quote-expiring-soon lead time, and MUST NOT emit it for draft, accepted, or terminal quotes.
- **REQ-004-040**: Every option/date price MUST be greater than 0 before send, and a zero price MUST block send. A date range the clinic cannot serve MUST be left out of that option rather than priced.
- **REQ-004-041**: If the FR-029 Default Currency changes while a draft holds prices, System MUST switch the draft to the new currency, keep every typed number unchanged, and show a "currency changed, check your prices" banner that the provider MUST acknowledge before send.
- **REQ-004-042**: A sent quote carrying an automatic FR-019 promotion MUST hold exactly one reserved use of that promotion's usage limit. A re-send of a new version MUST keep the existing reservation, create one only if the new version newly qualifies, and release it if the new version no longer carries the promotion. The reservation MUST be released when the quote expires, is withdrawn, or ends not selected or cancelled, MUST be released with reason `not_applied` when the accepted row does not carry the promotion, and MUST be consumed at acceptance when the accepted row carries it, so the usage limit is never exceeded. If the booking later ends in `Payment Window Expired` or is cancelled before the first payment, FR-005 and FR-019 own the return of the consumed use to the limit.
- **REQ-004-043**: System MUST set the parent quote's `firstSentAt` on its first send, and a re-send or new version MUST NOT change it.
- **REQ-004-044**: The FR-024 treatment Base Price MAY prefill a new option/date-price row only where no other standard value exists; it MUST be treated as a non-binding reference and MUST NOT be read after the quote is sent.
- **REQ-004-045**: FR-004 MUST be the producer of `quote.updated` and MUST emit it when a new version of an already-sent quote is re-sent, described as "quote revised (new version)".
- **REQ-004-046**: System MUST emit `quote.submitted` on the first send of a parent quote and `quote.expired` when expiry processing moves a sent parent quote to `expired` (FR-030).
- **REQ-004-047**: FR-004 MUST be the only producer of `quote.withdrawn`. The notice MUST go to the patient for every withdrawal and to the admin only when the withdrawn quote was already accepted.
- **REQ-004-048**: During an FR-006 provider-fault transfer before treatment starts, System MUST let an admin author a replacement quote for the replacement provider inside the same inquiry through Screen 8, with a mandatory reason and full audit. The quote MUST be marked admin-authored for a replacement and linked to the closed AcceptanceEvent, MUST NOT be offered for patient comparison or emit `quote.submitted`, and MUST be the target of the FR-005 admin-authored replacement acceptance.
- **REQ-004-049**: An admin edit of a sent quote through Screen 7 MUST create a new quote version and MUST emit `quote.updated` when that version is re-sent.
- **REQ-004-050**: System MUST NOT attach an automatic FR-019 promotion to an admin-authored replacement quote or take a promotion usage reservation for it; the admin sets the replacement price directly. A replacement quote that is not accepted MUST expire under the normal quote expiry, MUST leave the inquiry flagged `supportRequired` without cancelling it automatically, and MUST allow the admin to author another replacement quote or cancel the inquiry and booking.

## Key Entities

- **Quote**: id, inquiryId, providerId, treatmentId, treatmentVersion, estimatedGrafts, graftDescription, graftVisualPlan, clinicianIds[], commonNotes, commonRequirements, attachmentIds[], currencySnapshot, calculatedPriceRange, acceptedTotal, commission, termsAcknowledgedAt, lockedExchangeRateSnapshot, cancellationProvenance, authorType, replacementForAcceptanceEventId, status, version, firstSentAt, expiresAt, createdAt, updatedAt
  - Last editor and edit time are read from QuoteAudit rather than stored on Quote.
  - `authorType` is `provider` for every quote except the admin-authored replacement quote (`admin`, Workflow 7), which also carries `replacementForAcceptanceEventId`, the closed AcceptanceEvent it replaces.
  - One provider may own multiple Quote records for the same inquiry.
  - `currencySnapshot`, `firstSentAt`, and `expiresAt` are null on drafts and are captured at first send from the FR-026 quote configuration. `firstSentAt` is set once on the first send of the parent quote and never changes on a re-send or new version; FR-014 Time to First Quote reads it.
  - `acceptedTotal`, `termsAcknowledgedAt`, and `lockedExchangeRateSnapshot` are read-only copies written at FR-005 acceptance from the acceptance snapshot; the FR-005 snapshot is authoritative, and downstream FRs read money fields from it.
  - `commission` holds only the indicative commission model and value shown on the quote; the binding commission is fixed at booking confirmation (FR-029).
  - `treatmentId` identifies the exact immutable FR-024 Treatment record, while `treatmentVersion` retains its version metadata. Treatment name, type, and technique details are resolved through the relationship rather than copied onto Quote.
  - Relationships: belongsTo Inquiry; belongsTo exact Treatment version; belongsTo Provider; hasMany QuoteOption; hasMany QuoteVersion; hasMany QuoteAudit
  - Status enum includes: draft, sent, expired, withdrawn, archived, accepted, cancelled_other_accepted, **cancelled_inquiry_cancelled**, **cancelled_provider_status**. `confirmed` is not a quote status; booking confirmation is an FR-006 booking status.
  - For `cancelled_provider_status`, `cancellationProvenance` records `ProviderSuspended` or `ProviderDeactivated` and the triggering provider-status event (FR-015 A5/Screen 4). This status applies only to quotes that were not accepted.
- **QuoteOption**: id, quoteId, sourcePackageId, sourcePackageVersion, displayOrder, packageNameSnapshot, packageDescriptionSnapshot, standardPriceSnapshot, includedServices[], isCustomized, createdAt, updatedAt
  - `sourcePackageId` and `sourcePackageVersion` identify the exact FR-024 package version that seeded the option; `isCustomized` is the inline-customised flag. The option is a quote-local copy and is never written back to the library.
  - Relationships: belongsTo Quote; belongsTo source Package version for provenance; hasMany QuoteOptionItem; hasMany QuoteOptionDatePrice; hasMany QuoteOptionPlanDay
- **QuoteOptionItem**: id, quoteOptionId, sourcePackageItemId, itemType, name, description, price, isIncluded, displayOrder, metadata
  - Stores the option's quote-local inclusion snapshot; `sourcePackageItemId` may be null for a service added inline.
- **QuoteOptionDatePrice**: id, quoteOptionId, sourceInquiryDateRangeId, startDate, endDate, appointmentAt, appointmentTimeZone, price, promotionId, promotionTermsSnapshot, discountAmount, isAutoAttachedPromotion
  - `(quoteOptionId, sourceInquiryDateRangeId)` is unique. Each record combined with its Quote Option is one FR-005 subquote.
  - `price` is the provider price as entered, before any promotion, and must be greater than 0.
  - When an automatic promotion is attached at send, one use of its usage limit is reserved for the quote (one automatic promotion and at most one reservation per quote, kept across re-sent versions); the reservation is released on expiry, withdrawal, not selected, or cancellation, or with reason `not_applied` when the accepted row does not carry it, and consumed at acceptance when the accepted row carries it.
  - `promotionId` identifies the structured `PromotionProgram` (FR-019), either `REUSABLE` or `AD_HOC_QUOTE_BOUND`, selected by the provider or attached automatically at send. `promotionTermsSnapshot` and `discountAmount` are copied at send into the sent quote version; consumers read these copied terms and never resolve live FR-019 terms for a sent quote.
  - `appointmentAt` and `appointmentTimeZone`, with the provider, form the FR-006 slot-hold key at acceptance.
  - Acceptance state is not stored here. FR-005 owns subquote identity and acceptance state (accepted, not selected, superseded), and any acceptance flag shown for this record is derived from FR-005.
- **QuoteOptionPlanDay**: id, quoteOptionId, dayNumber, description
  - Day numbers remain relative for the life of the record and are never persisted as calendar dates. The selected plan seeds FR-010's In Progress day descriptions by day number.
- **QuoteVersion**: quoteId, version, changeset, createdAt, createdBy
  - Snapshot includes the full Quote aggregate and all option-owned children, including the promotion terms copied at send. One version is kept for each sent version of the quote.
  - This aggregate version is the version source for every FR-005 subquote derived from the Quote: `subquoteVersion = QuoteVersion.version`.
  - Relationships: belongsTo Quote
- **QuoteAudit**: quoteId, action, actorId, reason, before, after, createdAt
  - Relationships: belongsTo Quote

## Dependencies

### Internal Dependencies

- FR-003: Inquiry Submission (quote distribution and reference)
- FR-015: Provider Management (provider status eligibility and the suspension/deactivation cancellation cascade — Alternative Flow A5 and Screen 4)
- FR-005: Quote Comparison & Acceptance (combines one Quote Option and one Option/Date-Price Record into the complete accepted subquote and owns sibling/competing outcomes)
- FR-008: Travel & Logistics Coordination (accepted-option inclusion routing)
- FR-010: Treatment Progress Management (accepted-option plan handoff)
- FR-024: Treatment Package Management (provider package presets and source versions)
- FR-020: Notifications & Alerts (quote distribution/updates)
- FR-026 / A-09: Quote configuration supplies the quote currency (seeded from the FR-029 Default Currency), the expiry window, and the quote-expiring-soon lead time, all captured at first send
- FR-006: Booking & Scheduling (slot hold keyed by the option/date appointment fields; provider-fault transfer after acceptance, including withdrawal)
- FR-029: Payment System Configuration (indicative commission model and value; binding commission at booking confirmation)
- Admin-managed treatment catalog (A-09); provider-owned package library and versions (FR-024)
- FR-019: Promotions & Discount Management (A-06)
- FR-037: Monitor Your Hair Loss (advice-mode conversion inquiries may carry an exclusive assigned provider that restricts initial quote creation — see Business Rules)

### External Dependencies (APIs, Services)

- Calendar/appointment APIs for appointment integration
- Currency conversion/exchange-rate API is a downstream FR-029 dependency at acceptance, not a quote-creation dependency; FR-004 reads configured currency from FR-026

### Data Dependencies

- Inquiry ID, Patient anonymized ID, Provider ID, Promotion ID and promotion terms copied at send (from A-06/FR-019), Audit log IDs

## Assumptions

### User Behavior Assumptions

- Providers are trained and will use the quote management UI in compliance with platform audit rules
- Patients will review parent quotes and their subquotes, then accept one eligible subquote, cancel the inquiry, or allow the parent quotes to expire

### Technology Assumptions

- Providers have reliable access to the web app; network supports quote operations and media viewing
- Integration services (notifications and versioned settings) are available with acceptable latency

### Business Process Assumptions

- All patients/inquiries are distributed only to eligible providers within jurisdiction
- Admin-curated treatment definitions and provider-owned package-library presets are up to date and applied consistently
- Providers use package-library presets as starting points; quote-local customization does not become reusable library content

## Implementation Notes

### Technical Considerations

- No free text for core treatment field (catalog enforced)
- Treat Quote as an aggregate root and persist the parent, options, option items, option/date prices, and option plans in one transaction
- Enforce the one-to-five option limit in request validation and the quote-domain service; use stable option ordering and parent/child indexes
- Snapshot source package identity/version and item values into Quote Option-owned records; do not clone custom options into the package library
- Use an additive migration: create option-owned records, backfill every legacy quote as one option, provide a temporary single-option compatibility adapter, then deprecate direct quote ownership of `package_id`, `quote_amount`, treatment dates, custom services, item selections, and plan days
- Update acceptance consumers to identify one Quote Option and one option/date price; do not infer acceptance from the parent quote alone
- Immutable audit/versioning must cover all parent and option edits and state transitions
- Expiry, soft-delete, and audit patterns conform to platform standards

### Integration Points

- FR-003: Inquiry context and distribution inputs
- FR-005: Select one Quote Option and one option/date price, then preserve that accepted snapshot for booking
- FR-008: Derive travel responsibility from the accepted option's included services
- FR-010: Seed In Progress day descriptions from the accepted option's relative day plan
- FR-020: Notifications for creation/updates/expiry/status
- Admin (A-09): Treatment catalog plus FR-026 versioned quote currency/expiry configuration
- FR-024: Provider package library supplies versioned presets; quote-local option snapshots never write back to it
- FR-006: Slot hold keyed by provider and the accepted option/date appointment fields; provider-fault transfer for withdrawal after acceptance
- FR-010: Post-acceptance treatment-detail changes (plan, clinicians, grafts)
- FR-019 / A-06: Promotions & Discount Management for promotionId, promotion configuration, automatic-promotion eligibility, and discount application rules; promotion terms are copied into the quote version at send

### Scalability Considerations

- Efficient querying/indexing for provider quote lists and filters
- Parent quote metrics and option metrics must be aggregated separately so multiple options do not inflate quote-response conversion rates
- Amount metrics read the accepted option/date price; unaccepted quotes contribute to volume and conversion aggregates only
- Background jobs for mass notifications and expiry processing
- Rate limiting on edit/submit endpoints to prevent abuse

### Security Considerations

- Encrypt quote data at rest and in transit; enforce RBAC for provider staff
- Anonymize patient identifiers until payment confirmation
- Comprehensive audit logging (who/when/what-before/after, reason)

## Edge Cases

- Provider starts, then abandons, a draft: auto-archive to Drafts after 7 days
- Patient does not respond: quote expires, status auto-updated, provider notified
- Admin must audit archived/soft-deleted quote: accessible in "Archived" tab, audit trail modal enabled
- Provider attempts deletion post-acceptance: disallowed; only admin can archive with rationale
- Recovery from expired state: only admin can restore expired/archived quotes if justified (GDPR-compliant log); restore to an acceptable state is blocked when the inquiry already has an accepted subquote
- Provider opens quote creation for an inquiry that was just cancelled: system blocks with "Inquiry no longer active" error; no draft created
- Provider is mid-draft when inquiry is cancelled (race condition): on next save/refresh, system locks draft with "Inquiry Cancelled" banner; submission blocked; draft retained for provider reference but cannot be submitted
- Provider attempts to edit a quote in "Cancelled (Inquiry Cancelled)" status: system blocks with "This quote was cancelled because the patient cancelled their inquiry" message; all edit actions disabled
- Provider submits a quote at or after the effective time of its suspension or deactivation: submission is rejected; no sent quote, patient notification, or version is created
- Provider with several parent quotes, each with multiple options/date alternatives, is suspended: each unaccepted parent quote is cancelled once; option and date alternatives become unavailable with their parent and are not reported as separate cancellations
- Provider is suspended after one of its quotes was accepted: that parent quote keeps `accepted` and FR-006 handles the case through the provider-fault transfer; only the provider's unaccepted quotes become `cancelled_provider_status`
- Patient accepts at the last moment before the quote expiry: the parent quote is `accepted` and is never moved to `expired` during the payment hold
- Source package is edited or deactivated while a draft is open: the draft keeps its snapshot and may still be submitted with a warning
- Provider enters 0 for an option/date price: send is blocked with an inline error on that row; the provider either enters a price greater than 0 or leaves that date range out of the option
- Default Currency changes while a draft holds prices: the draft switches to the new currency with typed numbers kept, and send is blocked until the provider acknowledges the "currency changed, check your prices" banner
- An automatic promotion's last use is reserved by another quote before this quote is sent: the promotion is not attached at send, because the usage limit can never be exceeded

## Glossary

- **Quote**: Provider-generated cost and treatment proposal for a given inquiry
- **Soft Delete**: Archive status, not a hard delete; record remains for compliance/audit
- **Treatment Catalog**: Admin-defined set of available treatments displayed to all providers for selection
- **Package**: Provider-owned, versioned FR-024 library template that seeds exactly one Quote Option (services and pricing, travel services, and a relative day plan); there are no add-on package types
- **Quote-local copy**: The inline-edited package content saved only on one Quote Option, never written back to the library

## References

- system-prd.md: FR-004, Notification/Retention/Audit policies
- Hairline-ProviderPlatformPart1.txt lines 50-130: treatment/package selection, quote-local customization, date-price configuration, and discount context
- HairlineApp-Part1.txt lines 105-159 and 175-186: patient quote review, package comparison, pricing/discount display, expiry, and pre-scheduled appointment intent
- [SRC-MTG-002, MTG-002-D03 through D06 and O01](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md)
- [CR-FR004-20260909-01](./change-request-2026-09-09-quote-options-model.md)
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
3. Given another provider has an unsent draft for the inquiry, When a subquote is accepted, Then the draft becomes `cancelled_other_accepted` and no notice is sent
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
8. Given a subquote is accepted, When a provider or admin attempts any FR-004 edit, Then the edit is blocked and treatment-detail changes are directed to FR-010
9. Given a subquote is accepted, When the provider withdraws, Then the parent quote moves to `withdrawn`, the AcceptanceEvent is unchanged, the mandatory `quote.withdrawn` notice is sent, and the case is handed to the FR-006 provider-fault transfer without FR-004 re-routing
10. Given a provider with one accepted and one sent quote is suspended, When the suspension takes effect, Then only the sent quote becomes `cancelled_provider_status` and the accepted quote keeps `accepted` for the FR-006 provider-fault transfer
11. Given the booking reaches `Payment Window Expired`, When anyone tries to accept again or create a new quote for the inquiry, Then the accepted quote is not reopened and no new parent quote can be created or sent
12. Given an option/date row priced at 0, When the provider tries to send, Then send is blocked with an inline error on that row
13. Given a draft holds prices and the Default Currency changes, When the provider reopens the draft, Then the prices are kept as typed in the new currency and send is blocked until the "currency changed, check your prices" banner is acknowledged
14. Given an automatic promotion with a usage limit, When a quote carrying it is sent and later expires, is withdrawn, or ends not selected or cancelled, Then the reserved use is released; When the quote is accepted, Then the use is consumed
15. Given a sent quote, When the provider re-sends a new version, Then `quote.updated` is emitted as "quote revised (new version)" and `firstSentAt` is unchanged
16. Given a booking closed with a provider-fault cause before treatment started, When the admin authors a replacement quote on Screen 8 with a reason, Then the quote is saved as admin-authored for a replacement inside the same inquiry, no `quote.submitted` is emitted, and the FR-006 transfer can record the admin-authored acceptance against one of its option/date-price rows
17. Given a booking in Aftercare whose provider is at fault, When the admin handles it, Then Screen 8 is unavailable and only the aftercare provider or team is reassigned in FR-006
18. Given two automatic promotions qualify for the same quote, When the quote is sent, Then only the one ranked first by the FR-019 priority order is attached
19. Given an admin authors a replacement quote on Screen 8, When it is saved, Then no automatic promotion is attached, no promotion usage reservation is taken, and the price is the one the admin entered
20. Given a replacement quote that is not accepted, When its expiry is reached, Then it moves to `expired`, the inquiry stays `supportRequired`, and the admin can author another replacement quote or cancel the inquiry and booking

### Edge Cases (User Scenarios)

- Provider starts draft then abandons: auto-archive after 7 days
- Patient does not respond: quote expires and provider notified
- Provider attempts deletion post-acceptance: disallowed; admin-only archive with rationale
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
| 2025-10-30 | 1.0 | Initial PRD creation | Product & Engineering |
| 2025-11-03 | 1.1 | Template normalization; added tenant breakdown, comms structure, screen tables, FR summary, entities | Product & Engineering |
| 2025-11-04 | 1.2 | Template compliance: added Actors/Trigger/Outcome to workflows; normalized Dependencies; restructured Assumptions; formalized Implementation Notes; added User Scenarios & Testing | Product & Engineering |
| 2026-02-05 | 1.3 | Added inquiry cancellation cascade: new trigger in Workflow 3, "Cancelled (Inquiry Cancelled)" quote status, alternative flow for patient inquiry cancellation, REQ-004-013, updated Key Entities status enum. See FR-003 Workflow 5 and cancel-inquiry-fr-impact-report.md | Product & Engineering |
| 2026-02-08 | 1.4 | Cancellation integrity fixes: Added inquiry-active guard to Workflow 1 and business rules (concurrent submission rejection). Fixed changelog version collision and chronological order. Updated Screen 4 Status badge to include all patient-visible states. Added terminal-state exclusion to Workflow 4. Added "Inquiry Cancelled" banner specs to Screen 2 and Screen 3. Added cancellation statuses to Admin Screen 5 filters. Added User Story 4 (provider experience during cancellation) and cancellation edge cases. | AI |
| 2026-02-24 | 1.5 | Added `travel_path` + `included_services` fields to Quote Creation/Edit (Screen 1) to define post-confirmation travel responsibilities and package travel inclusions consumed by FR-008. | AI |
| 2026-02-25 | 1.6 | Removed `travel_path` as a manual select field. Travel path is now automatically derived from `included_services`: if flight or hotel is included → Path A (provider_included), otherwise → Path B (patient_self_booked). Simplified `included_services` to a standalone checklist without cross-field conditional gating. | AI |
| 2026-03-03 | 1.7 | Clarified Treatment Plan (per-day) schema: defined per-day entry fields (dayNumber/date/description) and documented `plan` structure used downstream by FR-010 In Progress day descriptions. | AI |
| 2026-05-12 | 1.8 | FR-019 alignment: Promotion field on Screen 1 retyped from `select/text` to `select-or-create` requiring resolution to a structured `PromotionProgram` (FR-019 Screen 9 Mode 1 list-selection OR Mode 2 inline create with `scope = AD_HOC_QUOTE_BOUND`). Screen 3 and Screen 5 Promotion fields retyped to `reference` (read-only resolution of `promotionId`). Screen 7 Admin Inline Edit Promotion field documented for admin override with inline-create permitted. Quote entity `promotionNote` free-text field **removed** — every applied discount must correspond to a structured PromotionProgram record. | Claude |
| 2026-08-20 | 1.9 | Cross-FR sync (FR-037 verification): Added restricted recipient mode — for monitoring-case conversion inquiries with an active exclusive provider assignment (REQ-037-029, Business Rule 7), only the assigned provider may create the initial quote. Added restricted-recipient check to Workflow 1, corresponding Business Rule, and FR-037/FR-038 as dependencies. See [Change Request](./change-request-2026-08-20-fr037-monitoring-conversion-alignment.md) | Verification alignment (2026-08-20) |
| 2026-09-09 | 2.0 | Approved quote-option restructure: allows multiple parent quotes from the same provider per inquiry; introduces one to five package-based Quote Options per quote; makes inline customization quote-local; moves inclusions, date-price applicability, promotions, and relative day plans to option ownership; retains treatment, graft facts, visual plan, clinicians, and common notes/requirements at parent level; defines aggregate versioning and FR-005 acceptance identifiers. See [Change Request](./change-request-2026-09-09-quote-options-model.md). | Product Owner / Documentation |
| 2026-09-09 | 2.1 | Replaced the flat Quote Creation/Edit field table with an ordered seven-tab workflow: Treatment Service; Package Options with Inline Package Editor; Grafts & Visual Plan; combined Dates & Pricing; Option Treatment Plans; Clinical Details & Notes; and Review & Submit. Added per-tab purpose, editable fields, completion gates, behaviors, and REQ-004-023. | Product Owner / Documentation |
| 2026-09-09 | 2.2 | Added the canonical Quote Data Ownership Matrix and completed missing field ownership: detailed option-item fields, quote-level attachments, multiple clinicians, system-generated graft description, configured currency snapshot, IDs/context, lifecycle status, derived price summaries/accepted total, commission, customization state, timestamps, and version/audit metadata. Currency remains system-configured and is never provider input. Added REQ-004-024 through REQ-004-029 and coverage scenarios. | Product Owner / Documentation |
| 2026-09-09 | 2.3 | Post-verification fixes: (1) removed both claims that relative option plan days are resolved to calendar dates — day numbers stay relative end-to-end and FR-010 consumes them by day number; (2) added the missing `included_services` row to the Quote Data Ownership Matrix as a provider-edited option field; (3) defined the quote-amount analytics basis as the accepted option/date price only, with unaccepted quotes excluded from amount metrics (new REQ-004-030 and business rule); (4) corrected the Approvals row to v2.2. See [Change Request](./change-request-2026-09-09-quote-options-model.md). | Verification issue resolution (2026-09-09) |
| 2026-09-10 | 2.4 | Second verification pass (system-integrity focus): (1) Screen 7 admin inline edit renamed Custom Services to Option Items and aligned its required fields with Sub-screen 2A (Item Name, Item Type, Included flag, Item Order, chargeable Cost) so admins cannot create option items that fail option-snapshot validation; (2) documented that adjusting Estimated Grafts on Screen 7 regenerates Graft Description from the approved template; (3) Quote Data Ownership Matrix Commission row restated as a read-only rate (percentage) to match the integer percentage stored in the schema. See [Change Request](./change-request-2026-09-09-quote-options-model.md). | Verification issue resolution (2026-09-10) |
| 2026-09-10 | 2.5 | Third verification pass: technique details now load read-only through the exact immutable Treatment ID/version relationship without duplicating treatment-owned data on Quote; restricted-recipient wording now applies only to FR-037; quote lifecycle terminology is normalized to `accepted` and `withdrawn`; and the mandatory unit, integration, contract, end-to-end, security, and performance verification matrix is defined. FR-010 v2.0 aligns its downstream package and plan consumers to the accepted Quote Option. See [Change Request](./change-request-2026-09-09-quote-options-model.md). | Product Owner / Verification alignment (2026-09-10) |
| 2026-09-10 | 2.6 | Fourth verification pass: removed the erroneous implication that Admin can edit immutable audit history; completed text and attachment validation limits; moved corrected source evidence into References; completed approval metadata; and reconciled FR-019 promotion attachment, FR-024 package provenance, and FR-026 quote-configuration ownership through their approved Change Requests. | Product Owner / Verification alignment (2026-09-10) |
| 2026-09-16 | 2.7 | Post-verification clarification: defined the parent aggregate `QuoteVersion` as the sole revision source for FR-005 subquotes. `subquoteVersion` equals the owning parent quote version; Quote Options and option/date-price records retain stable IDs without independent revision counters. | Product Owner / Verification alignment |
| 2026-09-16 | 2.8 | Added the canonical Parent Quote → Quote Option → Option/Date-Price hierarchy and its FR-005 Subquote projection; replaced remaining direct-quote acceptance wording with the approved subquote-driven selected-parent, sibling, and competing-parent lifecycle outcomes. | Product Owner / Verification alignment |
| 2026-09-21 | 2.9 | Clarified that providers may enter and revise Estimated Grafts, while Graft Description is regenerated from the approved template and current estimate and is never directly provider-editable. | Product Owner / Documentation |
| 2026-10-14 | 3.0 | Aligned provider suspension/deactivation cancellation cascade per CR-FR015-20261013-01 and FR-015 v1.9: provider status checks in Workflow 1, Workflow 3 provider-status trigger and `cancelled_provider_status` outcome (once per parent quote, accepted provenance preserved), terminal-state and alternative-flow updates, Screen 4/5 status values, business rule, REQ-004-031/032, Quote entity provenance note, FR-015 dependency, and edge cases. See [Change Request](./change-request-2026-10-14-provider-status-cancellation-cascade.md). Status reset pending consolidated verification. | Vân Tay Media |
| 2026-10-16 | 3.1 | MTG-002 quote-model alignment (CR-FR004-20261016-01). Cross-FR alignment with FR-026: first send records the quote configuration version and is blocked when the configuration cannot be read. Workflow 6 now moves an accepted quote to `withdrawn` and hands the case to the FR-006 provider-fault transfer instead of re-routing in FR-004 (E004-1; S1-3, D3, D6, D22). Promotion terms are copied into the sent quote version at send, the offered price is kept as entered with the discount separate, and automatic promotions attach at send to eligible rows (E004-2; FR-004-5, D10, D12, M14). On acceptance, unsent drafts are cancelled as `cancelled_other_accepted` silently (E004-3; FR-020-2, D5, P2). Commission field shows model and value labelled indicative (E004-4; S2-4, D13). Expiry and currency captured read-only at first send from FR-026, currency from the FR-029 Default Currency, no package currency (E004-5; FR-026-2, D15, D16, D18, M11). `confirmed` stated as not a quote status (E004-6; S5-6, D23). Accepted quotes never reopen after PWE and no new quote is allowed (E004-7; S1-1, D1). Package seeding restated: one package seeds one option, never summed, standard price and relative day plan prefill, pairings may be left out, subquotes up to options × ranges (E004-8; FR-024-2, D17, M1, R7-2). Library and quote inline edit paths defined (E004-9; FR-024-8, M10). Post-acceptance edit block with FR-010 route (E004-10; M2, FR-004-4). Appointment fields named as the FR-006 hold key (E004-11; S1-6, M4). `cancelled_provider_status` limited to unaccepted quotes (M18). `acceptedTotal` written from the acceptance snapshot and `isAccepted` removed in favour of FR-005-derived state (FR-005 v2.5). CR-FR004-20260909-01 stale reconciliation lines corrected (E004-12; FR-004-8, M12). Minors: FR-004-1, 6, 7 (partly), 9, 10, 11, 12, 14; FR-024-7; S4-6. New REQ-004-033 to REQ-004-039 and User Story 5. | Vân Tay Media |
| 2026-10-16 | 3.2 | Product Owner Q-series follow-up (CR-FR004-20261016-01): every option/date price must be greater than 0 and a date range the clinic cannot serve is left out (Q3); Default Currency change on a draft keeps typed numbers, switches currency, and requires an acknowledged banner before send (Q4); automatic promotions reserve one use at send, released on expiry, withdrawal, not selected, or cancellation and consumed at acceptance (Q6); `firstSentAt` set on first send and never changed by a re-send (Q15); FR-024 treatment Base Price is a reference-only prefill where no other standard value exists and is never read after send (Q20); FR-004 owns `quote.updated`, emitted on re-send of a new version as "quote revised (new version)" (Q24); a quote holds at most one promotion reservation, kept across re-sent versions (Q29). New REQ-004-040 to REQ-004-045, edge cases, and User Story 5 scenarios 12 to 15. Status remains pending consolidated verification. | Vân Tay Media |
| 2026-10-18 | 3.3 | Consolidated verification corrections (CR-FR004-20261016-01; decisions Q24, Q29, Q30, Q31): FR-004 now states that it emits `quote.submitted` on first send and `quote.expired` on expiry processing (Workflow 1, Workflow 3, new REQ-004-046); the old "significant edits" trigger is replaced by `quote.updated` on a re-sent new version (Workflow 2 Outcome, Acceptance Scenario 2); FR-004 is the only producer of `quote.withdrawn`, which goes to the patient always and to the admin only after acceptance (Workflow 3, Workflow 6, new REQ-004-047); REQ-004-042 points to FR-005 and FR-019 for the return of a consumed automatic promotion use; Approvals row refreshed. | Product Owner / Verification alignment |
| 2026-10-18 | 3.4 | Final audit corrections (CR-FR004-20261016-01; decisions Q35, Q36, Q37, Q39, Q40, Q42, Q43): added Workflow 7 and Screen 8 for the admin replacement quote authored during an FR-006 provider-fault transfer, the only exception to the no-new-quote-after-acceptance block (Quote gains `authorType` and `replacementForAcceptanceEventId`; REQ-004-048). The provider-fault transfer applies only before treatment starts; in Aftercare only the aftercare provider or team is reassigned. Patient cancellation is limited to Inquiry and Quoted; an admin booking cancellation leaves the accepted quote `accepted`. One automatic promotion per quote, chosen by the FR-019 priority order; new release reason `not_applied`. The appointment changes only through the FR-006 admin change and the snapshot keeps the baseline. Admin edits of a sent quote create a new version and emit `quote.updated` on re-send (Workflow 2, Screen 7, REQ-004-049). Removed Quote fields not owned by FR-004 (`affiliateAttributionId`, `travelResponsibilityState`, `lastEditedBy`, `lastEditedAt`). Added User Story 5 scenarios 16 to 18 and a document footer. Later the same day (decisions Q48, Q49): no automatic promotion attaches to an admin-authored replacement quote and no reservation is taken, the admin sets the price directly (Promotion field removed from Screen 8); an unaccepted replacement quote expires normally, the inquiry stays `supportRequired`, and the admin may author another replacement quote or cancel (REQ-004-050, scenarios 19 and 20). | Product Owner |
| 2026-10-26 | 3.5 | Product Owner decision on FR-015 dev-team questions (Q9): a draft quote cancelled by provider suspension or deactivation is silent to the patient; admin support alerts follow FR-020 | Claude (AI Assistant) |
| 2026-10-27 | 3.6 | Clarification on the FR-015 follow-up questions (F4): Workflow 3 "Provider becomes Suspended or Deactivated" now states that an accepted parent quote keeps `accepted`, the AcceptanceEvent stays unchanged, and FR-005 writes the linked supersession record only when the admin accepts the replacement quote in FR-006 Alternative Flow B5, matching FR-006 B4 and B5. No behaviour change. The legacy quote status value migration is recorded in [CR-FR004-20261027-01](./change-request-2026-10-27-legacy-status-value-migration.md); the requirement values are unchanged. | Product Owner |

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Joachim Trung Tuan | 2026-09-16 | Approved through FR-004 v2.8 — quote hierarchy, FR-005 subquote projection, aggregate `QuoteVersion` source, and subquote-driven lifecycle reconciliation |
| Product Owner | Joachim Trung Tuan | 2026-10-16 | Documentation approved through v3.2 via the MTG-002 quote-model decision log (CR-FR004-20261016-01); v3.3 consolidated verification corrections on 2026-10-18 apply decisions Q24 and Q29 to Q31; implementation reconciliation required |
| Product Owner | Joachim Trung Tuan | 2026-10-18 | Approved via MTG-002 decision log (documentation only), v3.4 final audit corrections (CR-FR004-20261016-01); implementation reconciliation required |
| Technical Lead | Not recorded | Not recorded | No separate approval recorded |
| Stakeholder | Not recorded | Not recorded | No separate approval recorded |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-004 from system-prd.md
**Last Updated**: 2026-10-27
