# FR-004 - Quote Submission & Management

**Module**: PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr004-quote-submission-management`
**Created**: 2025-10-30
**Status**: ✅ Verified & Approved
**Source**: FR-004 from system-prd.md; SRC-MTG-002 (MTG-002-D03 through D06 and O01); FR-005 v2.1; Product Owner clarifications dated 2026-09-09, 2026-09-10, and 2026-09-16

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
- **Option/Date-Price Record**: One applicable patient-requested date range for that option, with its pre-scheduled appointment, offered price, and optional promotion.
- **Subquote (FR-005 patient view)**: One Quote Option plus one applicable Option/Date-Price Record, combined with inherited Parent Quote context. This is the complete item the patient views, compares, and accepts. Parent Quotes, Quote Options, and Option/Date-Price Records are not accepted independently.

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
- System → Patient: Quote creation/expiry/status notifications
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
- In Tab 1, Provider selects one treatment service for the parent quote
- In Tab 2, Provider selects between one and five packages from the provider's active package library; each selection creates a Quote Option and may be opened in the inline package editor
- System snapshots each selected package and its service inclusions into the Quote Option; inline additions, edits, inclusions, or removals apply only to that option and are never written back to the package library
- In Tab 3, Provider enters the shared graft estimate and visual treatment plan
- In Tab 4, Provider configures the combined date-and-price matrix by selecting applicable patient-requested ranges for each option and pricing every applicable option/date combination
- In Tab 5, Provider enters a separate day-to-day treatment plan for each option
- In Tab 6, Provider selects the shared clinicians and enters common notes/requirements and attachments
- In Tab 7, Provider reviews the complete quote aggregate and submits it
- Provider submits quote (system validates required/optional fields; re-validates inquiry is still active at submission time)
- System delivers the parent quote and its ordered options to the patient and records one atomic version/audit snapshot of the aggregate

### Workflow 2: Quote Editing

**Actors**: Provider, System, Admin (observer/audit)

**Trigger**: Provider opens an existing draft or sent (pre-expiry) quote to modify fields

**Outcome**: Changes are saved with versioning/audit; patient notified if significant and not yet accepted

- Provider may edit draft or sent (pre-expiry) quotes, including shared fields, options, option-local inclusions, date-price combinations, and option-specific plans
- Package-library changes made after an option was created do not alter the quote snapshot
- All parent and option changes are versioned/audited as one quote aggregate
- Edits on expired/withdrawn/archived quote are prohibited
- Patient auto-notified of significant edits if not yet accepted

### Workflow 3: Quote Expiry & Status Transitions

**Actors**: System, Provider, Patient, Admin (observer)

**Trigger**: Time-based expiry reached; patient accepts a subquote through FR-005; provider initiates withdrawal/archive; or patient cancels parent inquiry (FR-003 Workflow 5)

**Outcome**: Quote transitions to correct status; notifications sent; audit recorded

- Each quote has an explicit expiry date (admin-controlled). Default expiry window is 48 hours; providers cannot modify this window and only see the computed expiry timestamp.
- Upon expiry, system updates the parent quote to `expired`; every child subquote becomes ineligible for acceptance
- Provider may withdraw or archive quotes pre-acceptance
- FR-005 subquote acceptance moves the selected subquote and its parent quote to `accepted`, marks sibling subquotes `not_selected`, and moves every competing parent quote for the inquiry to `cancelled_other_accepted`; the parent quote, Quote Option, and Option/Date-Price Record are never direct acceptance targets
- **Patient cancels parent inquiry**: All quotes for that inquiry transition to "Cancelled (Inquiry Cancelled)" regardless of current state (draft, sent, expired). This is a system-initiated cascade, not a provider or patient action on the quote itself. Providers are notified via `quote.cancelled_inquiry` event (FR-020).
- All state transitions are logged and result in notifications as appropriate

### Workflow 4: Quote Deletion (Soft Delete)

**Actors**: Provider, System, Admin

**Trigger**: Provider chooses to remove an ineligible or obsolete quote prior to acceptance

**Outcome**: Quote becomes Archived with rationale; remains visible in audit/archive; only admin can restore

- Provider may soft-delete a quote before acceptance (removes from provider listing, not from audit/archive or patient record)
- Quotes in terminal states (accepted, expired, withdrawn, cancelled_other_accepted, cancelled_inquiry_cancelled) cannot be soft-deleted by provider — these are already terminal
- System sets status = Archived with rationale
- Soft-deletes are fully auditable and revertible only by admin

### Workflow 5: Admin Oversight

**Actors**: Admin, System

**Trigger**: Admin monitors quotes or intervenes per policy or escalation

**Outcome**: Administrative action applied; full audit trail preserved; re-notifications triggered if needed

- Admin dashboard lists all provider quotes, searchable/filterable by state/date/provider/inquiry
- Admin can perform soft delete or restore and view the immutable audit trail and full quote history

### Workflow 6: Provider Withdrawal After Acceptance

**Actors**: Provider, Admin, Patient, System

**Trigger**: Provider requests withdrawal after a patient has accepted the quote

**Outcome**: Quote moves to `withdrawn`; system notifies stakeholders and opens the admin resolution path

- In rare cases, provider may withdraw from giving treatment after patient acceptance.
- Provider submits a withdrawal request with reason; quote status transitions to `withdrawn` and admin resolution begins.
- System notifies patient and admin; admin must resolve: re-route case to alternate provider, offer reschedule, or cancel with refund per policy.
- All actions audited. Note: This flow may be extracted into a separate FR if policy complexity (refunds/penalties/SLAs) increases.

### Alternative Flows

- Provider starts draft but abandons (system retains drafts for 7 days then auto-archives)
- Provider attempts late edit or deletion (system disallows and shows user message)
- Provider creates an additional quote for the same inquiry (system treats it as a separate parent response with its own options, expiry, versions, and audit history)
- Provider customizes a selected package inline (system stores a quote-local option snapshot and leaves the package library unchanged)
- Provider removes an option before submission (system permits removal while at least one valid option remains)
- Patient declines all quotes (system expires all open quotes automatically)
- Another provider's quote is accepted → System marks all other quotes for the same inquiry as "cancelled (other accepted)" and notifies their providers.
- While a provider is drafting a quote, if another quote is accepted → drafting provider is notified immediately; drafting quote is locked with banner referencing the accepted quote and case status updates.
- Patient cancels parent inquiry (FR-003 Workflow 5) → ALL quotes for that inquiry are auto-cancelled with status "Cancelled (Inquiry Cancelled)"; each affected provider notified via `quote.cancelled_inquiry` event; drafting providers see locked quote with "Inquiry Cancelled" banner upon next save/refresh. Cancellation reason is patient-private and NOT shared with providers.

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
| Currency snapshot | System-configured parent field | Read-only in Tabs 4 and 7 | Loaded from active system configuration and snapshotted for historical prices; never provider input |
| Status | System-owned lifecycle field | Persistent context and Tab 7 | Read-only; changed only by governed workflow actions |
| Expiry | System-derived parent field | Tab 7 | Computed from Admin configuration; read-only |
| Calculated price range / accepted total | System-derived parent summary | Tabs 4 and 7 | Price range is derived from all option/date prices; accepted total exists only after FR-005 selection; neither is entered separately |
| Commission | System-derived financial field | Tab 7 subject to permissions | Calculated from configured policy; never provider input |
| Affiliate attribution reference | System-captured financial provenance | Tab 7 subject to permissions | Inherited from validated referral context; never provider input |
| Terms acknowledged timestamp | System-owned FR-005 acceptance field | Tab 7 after acceptance | Null during quote creation; recorded only when patient acceptance terms are acknowledged |
| Locked exchange-rate value and pair | System-owned FR-005/FR-029 acceptance snapshot | Tab 7 subject to permissions | Null before acceptance; recorded by the system when conversion is required |
| Cancellation and supersession provenance | System-owned lifecycle fields | Tab 7 / Audit | Records inquiry cancellation or another accepted quote; never provider input |
| Travel-responsibility state and declaration metadata | System-owned FR-008 downstream fields | Tab 7 after applicable workflow action | Derived from the accepted option or recorded by the governed travel flow; not edited during quote creation |
| Created, updated, and last-edited metadata | System-owned audit metadata | Tab 7 / Audit | Generated from authenticated actions; read-only |
| Quote Option ID and parent Quote ID | System-owned | Tabs 2, 4, 5, and 7 | Stable identifiers; read-only |
| Source Package ID and version | System-captured option provenance | Tab 2 and Sub-screen 2A | Captured when selected; read-only after snapshot creation |
| Option display order | Provider-edited option field | Tab 2 | Unique consecutive patient-facing order |
| Package name, description, and standard price snapshots | System-copied option fields | Tab 2 and Sub-screen 2A | Copied from the selected library version; retained for history |
| Option customization state | System-derived option field | Tab 2 and Tab 7 | Indicates whether the snapshot differs from its source package |
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
| Appointment date/time and timezone | Provider-edited option/date fields | Tab 4 | Appointment must fall within the selected range; timezone required |
| Offered price | Provider-edited option/date field | Tab 4 | Non-negative price in the configured currency |
| Promotion ID | Provider-selected option/date reference | Tab 4 | Optional structured FR-019 promotion |
| Acceptance state | System-owned downstream field | Tab 7 after FR-005 action | Read-only; not set during quote creation/edit |
| Option plan-day ID and parent Option ID | System-owned | Tab 5 | Stable identifiers; read-only |
| Plan day number and description | Provider-edited option fields | Tab 5 | Consecutive relative day number and required description |
| Child-record created and updated metadata | System-owned audit metadata | Tab 7 / Audit | Applies to options, items, date-price rows, and plan days; read-only |
| Quote version and audit records | System-owned compliance records | Tab 7 / Audit | Complete immutable history of parent and option changes |

**Tab Structure**:

| Tab | Purpose | Editable Content | Completion Gate |
| --- | --- | --- | --- |
| 1. Treatment Service | Establish the single treatment shared by the quote | Treatment service | One active treatment selected |
| 2. Package Options | Select and customize the alternatives offered to the patient | One to five packages; option order; option-local inclusions and services | One to five complete option snapshots |
| 3. Grafts & Visual Plan | Record clinical facts shared by every option | Estimated grafts; graft description; visual treatment plan | Valid graft estimate; optional visual saved if supplied |
| 4. Dates & Pricing | Combine date-range selection and price setup into one package-driven matrix | Applicable ranges; appointment slots; prices; promotions | Every applicable option/date cell complete |
| 5. Option Treatment Plans | Define how the treatment schedule differs by package | Relative day plan for each option | Consecutive day sequence for every option |
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
| Package Options | Quote | ordered multiselect | Yes | Packages selected from the authenticated provider's active library | Minimum 1; maximum 5; must match Tab 1 treatment |
| Option Order | Option | reorder control | Yes | Patient-facing comparison order | Unique consecutive order within the quote |
| Package Snapshot | Option | read-only summary | Yes | Source package identity/version, standard price, and standard inclusions copied into the quote | Later library edits must not alter the snapshot |
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
- Closing or saving Sub-screen 2A never creates or updates a reusable `Package` or package-library item.
- Customization examples include medical consultation, maximum graft coverage, PRP injection, Day-3 wash, lifetime warranty, language translator, hotel, local transport, airport transfer, and flight.
- Removing an option also removes its draft date-price rows and draft treatment plan after explicit confirmation; at least one option must remain before submission.

##### Tab 3: Grafts & Visual Plan

**Purpose**: Record treatment facts that apply equally to every package option.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Estimated Grafts | Quote | number | Yes | Estimated graft count shared by every option | Positive integer |
| Graft Description | Quote | read-only text | Yes | System-generated explanation based on the estimate and approved template | Regenerated when estimated grafts change; retained in aggregate versions |
| Visual Treatment Plan / 3D Markup | Quote | drawing/upload | No | Shared visual plan or markup | Supported file/media rules; stored in the aggregate version |

##### Tab 4: Dates & Pricing

**Purpose**: Combine treatment-date selection and pricing in one package-first configuration surface.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Package Option | Option | repeated section | Yes | One section per option selected in Tab 2 | All options shown in Tab 2 order |
| Applicable Treatment Dates | Option | multiselect | Yes | Patient-requested ranges for which this option is offered | At least one per option; subset of FR-003 ranges |
| Appointment Slot | Option/date | datetime | Yes | Appointment start for this option/date combination | Must fall within its selected range; timezone required |
| Offered Price | Option/date | amount | Yes | Price for this package option on this date range | Non-negative; quote currency; standard package price may prefill |
| Promotion | Option/date | select-or-create | No | Structured promotion applied to this option/date price | Must resolve to a valid `PromotionProgram`; no free-text promotion |
| Configured Currency | Quote | read-only label | Yes | Currency loaded from system configuration and used across every option/date price | Never provider-editable; snapshotted when the quote is created |

**Behavior**:

- The selected packages drive the screen: configure date applicability and pricing option by option until the option list is complete.
- An option may apply to all patient-requested ranges or only a subset.
- Every range marked applicable must have its own appointment slot and offered price; unavailable combinations are omitted rather than priced.
- `included_services` comes from the corresponding Tab 2 option snapshot. After FR-005 acceptance, FR-008 derives `travel_path` from the accepted option.

##### Tab 5: Option Treatment Plans

**Purpose**: Define a different day-to-day treatment plan for each package option.

| Field Name | Scope | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- | --- |
| Package Option | Option | selector/section | Yes | Chooses the option whose plan is being edited | Every option requires a plan |
| Day Number | Option | number | Yes | Relative sequential day index | Starts at 1; consecutive with no gaps |
| Day Description | Option | text | Yes | What happens on that relative treatment day | Required; maximum 1,000 characters |

**Behavior**:

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
| Configured Currency | Quote | read-only label | Yes | Currency snapshot applied to all displayed prices | Loaded from system configuration; never provider-editable |
| Calculated Price Range / Accepted Total | Quote | read-only amount | Yes | Price range before acceptance and selected total after FR-005 acceptance | Derived from the complete Tab 4 matrix and accepted option/date identifier |
| Commission | Quote | read-only rate (percentage) | Conditional | System-calculated commission rate shown only to authorized roles | Derived from configured policy; never provider input |
| Quote Status | Quote | read-only badge | Yes | Current governed lifecycle state | System-owned enum |
| Expiry | Quote | read-only datetime | Yes | Computed deadline for the complete quote | From admin-configured window |
| Created, Updated, and Last Edited | Quote | read-only metadata | Yes | System timestamps and last authenticated editor | System-generated |
| Option Customization State | Option | read-only badge | Yes | Shows whether each option differs from its source package snapshot | System-derived from option-item changes |
| Downstream Acceptance and Lifecycle Metadata | Quote | read-only group | Conditional | Terms acknowledgment, exchange-rate lock, cancellation/supersession provenance, affiliate attribution, and travel-responsibility state | Visible only when populated and authorized; never edited in Screen 1 |
| Version and Audit Summary | Quote aggregate | read-only links | Yes | Current version and immutable change history | Must cover parent and all option-owned records |
| Validation Summary | Quote aggregate | read-only checklist | Yes | Shows complete tabs and links each issue to its owning tab | No unresolved blocking issue |
| Submit Quote | Quote aggregate | action | Yes | Submits parent and options as one transaction | Revalidate inquiry, authorization, option count, and every tab gate |

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
| Promotion | reference | No | Structured promotion applied to an option/date price | Read-only; resolves from `promotionId` |
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

**Purpose**: Patient reviews and accepts/declines quotes

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote List | list | Yes | Parent quotes grouped by inquiry and provider | Read-only; separate quote and option counts |
| Treatment | text | Yes | Selected treatment | Read-only |
| Quote Options | comparison cards/table | Yes | One to five package options within the selected quote | Read-only in FR-004; selection governed by FR-005 |
| Price Breakdown | matrix | Yes | Price for every applicable option/date combination | Currency rules |
| Inclusions and Services | list | Yes | Snapshot of inclusions and quote-local customizations | Grouped by option; read-only |
| Treatment Plan | table | Yes | Different day-to-day plan for each option | Grouped by option; read-only |
| Attachments | file list/viewer | No | Quote-level supporting files | Read-only; patient access rules enforced |
| Status | badge | Yes | Pending/Accepted/Expired/Cancelled (Inquiry Cancelled)/Cancelled (Other Accepted)/Withdrawn | Enum validation; visual treatment per state (e.g., greyed-out for cancelled/expired) |
| Expiration Timer | timer | Yes | Countdown to expiry | From admin window |
| Provider Info | group | Yes | Allowed provider details | Privacy rules |
| Actions | actions | Yes | Accept/Decline | State & confirmation rules |
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
| Actions | column | Yes | Restore/Archive/View Detail | State-aware |
| Search/Filters | control | No | Patient/Inquiry/Treatment/Date/Status/Location/Alerts/Provider. Status filter includes: draft, sent, expired, withdrawn, archived, accepted, cancelled_other_accepted, cancelled_inquiry_cancelled | Valid enums/ranges |
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
| Promotion | reference | No | Structured promotion applied to an option/date price | Read-only; resolves from `promotionId` |
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

**Purpose**: Admin performs limited inline edits with audit

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Selector | dropdown/list | Yes | Select target quote under inquiry | Must belong to same inquiry |
| Quote Option | selector | Yes | Select the package option being edited | Must belong to the selected quote |
| Option/Date Price | matrix | Cond. | Edit applicability, appointment slot, or price for an option/date combination | Reason required; matrix must remain complete |
| Package Inclusions | inline option editor | Cond. | Edit the option snapshot without changing the package library | Reason required |
| Estimated Grafts | number | Cond. | Adjust graft count. Saving a new value regenerates Graft Description from the approved template; the prior text is not preserved | Positive integer; reason required |
| Option Items | repeater | Cond. | Add/edit/remove items within the selected option snapshot | Same required fields as Sub-screen 2A — Item Name, Item Type, Included flag, Item Order, and Cost when the item is chargeable; item order consecutive with no gaps; reason required |
| Treatment Plan (per-day) | repeater | Cond. | Edit the selected option's relative day plan | Consecutive day numbers; reason required |
| Promotion | select-or-create | Cond. | Add, replace, or remove the structured promotion on an option/date price. Inline create permitted with `scope = AD_HOC_QUOTE_BOUND` per FR-019 Screen 9 Mode 2 | Must resolve to a valid PromotionProgram id or null; reason required |
| Notes | textarea | No | Admin note | Stored with audit |
| Clinicians | multiselect | Cond. | Change the shared clinician assignments | At least one; each must be active, eligible, and belong to the provider; reason required |
| Attachments | multi-file upload | Cond. | Add or remove quote-level supporting files | File/access rules and reason required |
| Audit Reason | textarea | Yes | Reason for change | Required for any edit |

**Notes**:

- All inline edits auditable (who/when/before/after, reason); system re-notifies on impactful changes

## Business Rules

- Quotes MUST reference distributed inquiry ID and be linked to original patient object
- Quote data MUST append to inquiry data; no reduction or overwriting of inquiry-supplied fields. Downstream stages inherit upstream data.
- Only assigned clinic staff may submit/edit quotes for assigned inquiries
- Treatment type selection MUST use admin-curated treatment catalog; no free text
- Graft/quantity, option/date prices, and scheduled slots MUST be present and valid
- A provider may submit multiple parent quotes for the same inquiry; each quote has an independent identity, lifecycle, expiry, versions, and audit history
- Each quote MUST contain at least one and at most five ordered Quote Options
- Every Quote Option MUST originate from an active package in the authenticated provider's package library
- Package selection occurs after the shared treatment is selected; every option in the quote MUST use that parent treatment
- Selecting a package MUST create a quote-owned snapshot. Inline option customization MUST NOT update or create reusable package-library records
- Package-library changes after snapshot creation MUST NOT alter existing draft or sent options unless the provider explicitly replaces the source package and confirms a new snapshot
- Each option MUST identify at least one applicable patient-requested date range and provide a price and appointment slot for every applicable option/date combination
- Estimated grafts, graft description, visual treatment plan, clinicians, common notes, and common requirements belong to the parent quote and MUST NOT be duplicated as option-specific facts
- Quote-level attachments apply to every option and MUST follow platform file-access, audit, and retention rules
- Quote currency MUST be loaded from active system configuration, snapshotted for historical integrity, and displayed read-only; providers MUST NOT enter or change it in the quote
- Graft description MUST be generated from the approved system template and estimated graft count; providers edit the graft estimate, not the generated description
- Included services, custom services, date applicability/pricing, promotions, and the day-to-day plan belong to the Quote Option or its option/date price record
- Analytics MUST distinguish parent quote responses from Quote Options so option counts do not inflate quote-response or conversion metrics
- Quote-amount analytics MUST use only the accepted option/date price. A quote with no acceptance has a price range rather than an amount and MUST be excluded from amount metrics, while still counting as one response in volume and conversion metrics
- Quotes CANNOT be hard deleted (only archived/soft deleted)
- All state transitions (draft→sent→expired, etc.) MUST be fully auditable
- Quotes may be edited only until accepted or expired
- Quotes MUST expire automatically on reaching set expiry date
- Each inquiry may have multiple parent quotes from multiple providers or from the same provider. Package alternatives within a parent quote are Quote Options, not independent quote responses
- Discounts are provider-managed (reviewed by admin if above configured threshold)
- All notifications MUST comply with platform notfication/audit/logging rules
- GDPR/data compliance: all quote objects are archived for ≥7 years
- Patient information remains censored at this stage until payment confirmation; only anonymized identifiers and allowed fields are visible to providers.
- Providers must select option applicability from patient-requested date ranges; each applicable option/date combination must have a specific price and appointment slot.
- System MUST verify parent inquiry is not in Cancelled status before accepting quote creation or submission. If inquiry is cancelled mid-draft (race condition), system rejects submission with error "Inquiry no longer active" and locks the draft with "Inquiry Cancelled" banner. See FR-003 Workflow 5 edge case.
- **Restricted recipient mode**: If the inquiry was created via an FR-037 monitoring-case conversion with an active exclusive provider assignment (REQ-037-029, Business Rule 7; see FR-003 Workflow 2 Alternative Flow B3), only that assigned provider may create the initial quote for the inquiry. Any other provider attempting to open the inquiry for quote creation is blocked with error "This inquiry is restricted to its assigned provider." The restriction applies only to initial quote creation and does not affect subsequent workflows (editing, expiry, withdrawal, admin oversight) once a quote exists. FR-038 is self-service and does not create an FR-004 inquiry or provider assignment.

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
- **REQ-004-002**: System MUST enforce admin-controlled expiry window (default 48h) and compute deadlines per quote.
- **REQ-004-003**: System MUST auto-cancel other quotes for the same inquiry upon one acceptance and notify affected providers.
- **REQ-004-004**: System MUST support provider withdrawal after acceptance with admin resolution workflow and full audit.
- **REQ-004-005**: Admin MUST be able to inline edit policy-bound fields with required reason and re-notifications.

### Data Requirements

- **REQ-004-006**: Quotes MUST reference original inquiry and patient; quote data appends, never overwrites inquiry data.
- **REQ-004-007**: All quote edits and state transitions MUST be versioned and auditable.

### Security & Privacy Requirements

- **REQ-004-008**: Patient identifiers MUST remain anonymized to providers until payment confirmation.
- **REQ-004-009**: All quote data MUST be encrypted at rest and in transit; soft deletes only.

### Integration Requirements

- **REQ-004-010**: Module MUST integrate with FR-003 for inquiry context and FR-020 for notifications.
- **REQ-004-011**: Admin settings (expiry window) MUST be applied from A-09.

### Clarifications

- **REQ-004-012**: Refund/penalty policy depth for provider withdrawal may move to a dedicated FR if expanded.

### Cancellation Cascade Requirements

- **REQ-004-013**: System MUST auto-cancel ALL quotes for an inquiry when that inquiry is cancelled by the patient (FR-003 Workflow 5), with distinct status "Cancelled (Inquiry Cancelled)" and provider notifications via `quote.cancelled_inquiry` event (FR-020).

### Quote Option Requirements

- **REQ-004-014**: System MUST allow the same provider to create multiple parent quotes for one active inquiry; every quote retains an independent lifecycle, expiry, version history, and audit history.
- **REQ-004-015**: Each quote MUST contain between one and five ordered Quote Options, and submission MUST be blocked outside that range.
- **REQ-004-016**: Each Quote Option MUST retain the selected provider package ID/version and a stable, versioned quote-owned snapshot of its inclusions and standard values.
- **REQ-004-017**: Providers MUST be able to customize every selected package inline for the current quote without updating or creating reusable package-library records.
- **REQ-004-018**: Each Quote Option MUST define its applicable patient-requested date ranges and a price, appointment date/time, timezone, and optional structured promotion for every applicable option/date combination.
- **REQ-004-019**: Each Quote Option MUST own a separate ordered day-to-day treatment plan using consecutive relative day numbers.
- **REQ-004-020**: Estimated grafts, graft description, visual treatment plan, clinicians, common notes, and common requirements MUST remain shared parent-quote fields.
- **REQ-004-021**: Quote version and audit records MUST capture the complete parent-and-options aggregate atomically, including option additions/removals, package snapshots, inclusion changes, date-price changes, and option plan changes.
- **REQ-004-022**: FR-004 MUST expose stable identifiers for the parent quote, Quote Option, and option/date price so FR-005 can record exactly one accepted option/date combination. FR-004 versions the complete parent quote aggregate atomically; therefore, the FR-005 `subquoteVersion` MUST equal the owning parent quote's current `QuoteVersion`. Quote Options and option/date-price records do not have independent revision counters.
- **REQ-004-023**: Provider Quote Creation/Edit MUST use the ordered seven-tab flow defined in Screen 1, including Sub-screen 2A for quote-local package editing and one combined Dates & Pricing tab driven by the selected package options.
- **REQ-004-024**: Every Quote, Quote Option, option item, option/date price, and option plan-day field MUST follow the Screen 1 Quote Data Ownership Matrix, with exactly one provider-editing surface or an explicit read-only/system-derived owner.
- **REQ-004-025**: Quote currency MUST come from active system configuration, MUST NOT be provider input, and MUST be snapshotted on the quote so historical prices retain their original currency.
- **REQ-004-026**: Providers MUST be able to attach quote-level supporting files that apply to every option; file security, access, audit, and retention rules MUST be enforced.
- **REQ-004-027**: A quote MUST support one or more eligible clinician assignments shared across every option.
- **REQ-004-028**: Graft description MUST be generated from the approved system template and estimated graft count, displayed read-only, and versioned with the quote.
- **REQ-004-029**: System-owned identifiers, lifecycle status, price summaries, commission, timestamps, customization state, and version/audit metadata MUST be visible only where authorized and MUST NOT be provider-editable.
- **REQ-004-030**: Quote-amount analytics MUST be computed from the accepted option/date price only. Unaccepted quotes MUST be excluded from amount metrics and counted once as a parent response in volume and conversion metrics; Quote Options MUST NOT be counted as responses.

## Key Entities

- **Quote**: id, inquiryId, providerId, treatmentId, treatmentVersion, estimatedGrafts, graftDescription, graftVisualPlan, clinicianIds[], commonNotes, commonRequirements, attachmentIds[], currencySnapshot, calculatedPriceRange, acceptedTotal, commission, affiliateAttributionId, termsAcknowledgedAt, lockedExchangeRateSnapshot, cancellationProvenance, travelResponsibilityState, status, expiresAt, createdAt, updatedAt, lastEditedBy, lastEditedAt
  - One provider may own multiple Quote records for the same inquiry.
  - `treatmentId` identifies the exact immutable FR-024 Treatment record, while `treatmentVersion` retains its version metadata. Treatment name, type, and technique details are resolved through the relationship rather than copied onto Quote.
  - Relationships: belongsTo Inquiry; belongsTo exact Treatment version; belongsTo Provider; hasMany QuoteOption; hasMany QuoteVersion; hasMany QuoteAudit
  - Status enum includes: draft, sent, expired, withdrawn, archived, accepted, cancelled_other_accepted, **cancelled_inquiry_cancelled**
- **QuoteOption**: id, quoteId, sourcePackageId, sourcePackageVersion, displayOrder, packageNameSnapshot, packageDescriptionSnapshot, standardPriceSnapshot, includedServices[], isCustomized, createdAt, updatedAt
  - Relationships: belongsTo Quote; belongsTo source Package for provenance; hasMany QuoteOptionItem; hasMany QuoteOptionDatePrice; hasMany QuoteOptionPlanDay
- **QuoteOptionItem**: id, quoteOptionId, sourcePackageItemId, itemType, name, description, price, isIncluded, displayOrder, metadata
  - Stores the option's quote-local inclusion snapshot; `sourcePackageItemId` may be null for a service added inline.
- **QuoteOptionDatePrice**: id, quoteOptionId, sourceInquiryDateRangeId, startDate, endDate, appointmentAt, appointmentTimeZone, price, promotionId, isAccepted
  - `promotionId` resolves to a structured `PromotionProgram` (FR-019), either `REUSABLE` or `AD_HOC_QUOTE_BOUND`.
- **QuoteOptionPlanDay**: id, quoteOptionId, dayNumber, description
  - Day numbers remain relative for the life of the record and are never persisted as calendar dates. The selected plan seeds FR-010's In Progress day descriptions by day number.
- **QuoteVersion**: quoteId, version, changeset, createdAt, createdBy
  - Snapshot includes the full Quote aggregate and all option-owned children.
  - This aggregate version is the version source for every FR-005 subquote derived from the Quote: `subquoteVersion = QuoteVersion.version`.
  - Relationships: belongsTo Quote
- **QuoteAudit**: quoteId, action, actorId, reason, before, after, createdAt
  - Relationships: belongsTo Quote

## Dependencies

### Internal Dependencies

- FR-003: Inquiry Submission (quote distribution and reference)
- FR-005: Quote Comparison & Acceptance (combines one Quote Option and one Option/Date-Price Record into the complete accepted subquote and owns sibling/competing outcomes)
- FR-008: Travel & Logistics Coordination (accepted-option inclusion routing)
- FR-010: Treatment Progress Management (accepted-option plan handoff)
- FR-024: Treatment Package Management (provider package presets and source versions)
- FR-020: Notifications & Alerts (quote distribution/updates)
- FR-026 / A-09: System configuration supplies the active quote currency snapshot and expiry policy
- Admin-managed treatment catalog (A-09); provider-owned package library and versions (FR-024)
- FR-019: Promotions & Discount Management (A-06)
- FR-037: Monitor Your Hair Loss (advice-mode conversion inquiries may carry an exclusive assigned provider that restricts initial quote creation — see Business Rules)

### External Dependencies (APIs, Services)

- Calendar/appointment APIs for appointment integration
- Currency conversion/exchange-rate API is a downstream FR-029 dependency at acceptance, not a quote-creation dependency; FR-004 reads configured currency from FR-026

### Data Dependencies

- Inquiry ID, Patient anonymized ID, Provider ID, Promotion ID (from A-06/FR-019), Audit log IDs

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
- FR-024: Provider package library supplies presets; quote-local option snapshots never write back to it
- FR-019 / A-06: Promotions & Discount Management for promotionId, promotion configuration, and discount application rules

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
- Recovery from expired state: only admin can restore expired/archived quotes if justified (GDPR-compliant log)
- Provider opens quote creation for an inquiry that was just cancelled: system blocks with "Inquiry no longer active" error; no draft created
- Provider is mid-draft when inquiry is cancelled (race condition): on next save/refresh, system locks draft with "Inquiry Cancelled" banner; submission blocked; draft retained for provider reference but cannot be submitted
- Provider attempts to edit a quote in "Cancelled (Inquiry Cancelled)" status: system blocks with "This quote was cancelled because the patient cancelled their inquiry" message; all edit actions disabled

## Glossary

- **Quote**: Provider-generated cost and treatment proposal for a given inquiry
- **Soft Delete**: Archive status, not a hard delete; record remains for compliance/audit
- **Treatment Catalog**: Admin-defined set of available treatments displayed to all providers for selection
- **Add-On/Package**: Optional offering by provider (e.g., hotel, transport, medications)

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
2. Given a significant change, When saved, Then patient is notified automatically
3. Given an expired quote, When editing, Then system blocks and shows policy notice

### User Story 3 - Auto-Expiry and Status Transitions (Priority: P1)

Why: Enforces time-bound decision windows.

Independent Test: Allow quote to reach expiry; verify status transitions and notifications.

Acceptance Scenarios:

1. Given a sent quote, When expiry time is reached, Then status becomes Expired and provider/patient are notified
2. Given patient selects one option/date combination through FR-005, When acceptance is recorded, Then the parent quote and selected option/date identifiers are preserved, other parent quotes are cancelled, and stakeholders are notified

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

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Joachim Trung Tuan | 2026-09-16 | Approved through FR-004 v2.8 — quote hierarchy, FR-005 subquote projection, aggregate `QuoteVersion` source, and subquote-driven lifecycle reconciliation |
| Technical Lead | Not recorded | Not recorded | No separate approval recorded |
| Stakeholder | Not recorded | Not recorded | No separate approval recorded |
