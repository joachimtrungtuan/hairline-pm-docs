# Change Request: Parent Quotes with Package Options

**Change Request ID**: CR-FR004-20260909-01
**Primary FR**: FR-004
**Triggering FR / Event**: SRC-MTG-002 quote-options decisions and Product Owner clarification
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-09
**Decision Date**: 2026-09-09
**PRD Version Change**: v1.9 to v2.6 (v2.0 aggregate restructure, v2.1 seven-tab flow, v2.2 ownership matrix — one approval event on 2026-09-09; v2.3-v2.6 verification fixes approved through 2026-09-10)
**Related Commit(s)**: Pending

---

## Decision Summary

FR-004 is restructured from a single-package quote into an auditable parent quote containing one to five package-based Quote Options. Providers may create multiple parent quotes for the same inquiry, including multiple quotes from the same provider. Every option begins from a provider package-library preset, supports quote-local inline customization, has its own applicable date-price combinations and day-to-day plan, and leaves the reusable package library unchanged.

## Baseline State

**Source version**: FR-004 v1.9, Workflow 1, Screen 1, Business Rules, and Key Entities. Screen 1 was a single flat provider field table with no canonical statement of which fields are provider-editable, system-derived, or read-only.

FR-004 allowed multiple quotes for general multi-provider or package cases but did not distinguish a parent response from its alternatives or explicitly permit multiple parent quotes from the same provider. It represented one optional package, one set of customizations, quote-level date prices, and one quote-level treatment plan. The current backend additionally blocks a second provider quote, stores one `package_id` on `quotes`, creates a new `Package` during inline customization, and owns treatment dates, custom services, selections, and plan days directly under the quote.

## Approved State

**Target version**: FR-004 v2.6, Workflows, Screens 1–7, REQ-004-001 and REQ-004-014 through REQ-004-030, Key Entities, Dependencies, References, and User Scenarios & Testing

The updated [FR-004 PRD](./prd.md) defines Quote as the parent aggregate. Shared treatment facts remain on Quote. One to five ordered Quote Options hold package snapshots and customized inclusions. Option/date price records hold applicability, appointment, price, and promotion data. Each option owns a relative day-to-day plan. Versioning and audit capture the complete aggregate atomically.

Provider Quote Creation/Edit uses an ordered seven-tab flow (Treatment Service; Package Options with the Inline Package Editor; Grafts & Visual Plan; combined Dates & Pricing; Option Treatment Plans; Clinical Details & Notes; Review & Submit), and every Quote, Quote Option, option item, option/date price, and option plan-day field is governed by the canonical Quote Data Ownership Matrix, which gives each field exactly one provider-editing surface or an explicit read-only/system-derived owner.

The quote retains an exact immutable Treatment ID/version relationship and loads technique details through that relationship without duplicating treatment-owned data. Restricted-recipient handling applies only to FR-037 advice-mode conversions; lifecycle terms use `accepted` and `withdrawn`; and the Constitution-required verification layers are explicit. FR-010 v2.0 consumes the accepted Quote Option and its relative plan days.

## Requirement Delta

| Contract Area | Before | After | Reason |
| --- | --- | --- | --- |
| Provider quote cardinality | One provider quote per inquiry in the current implementation | Same provider may create multiple independent parent quotes for one active inquiry | Support distinct provider responses when operationally needed |
| Package cardinality | Zero or one package per quote | One to five ordered package-based Quote Options per quote | Give patients comparable choices without cluttering the quote |
| Package customization | Customized data may create a new reusable `Package` record | Customization is stored only in the Quote Option snapshot | Prevent patient-specific edits from polluting the package library |
| Treatment ownership | Treatment stored on Quote | Unchanged; one treatment shared by every option | Treatment is selected before packages and is common to the quote |
| Service ownership | Package/custom-service data attached to the quote or package | Inclusion and custom-service snapshots belong to the Quote Option | Allow each package option to differ independently |
| Date and price ownership | Date ranges and prices belong directly to Quote | Every Quote Option selects applicable inquiry ranges and prices each applicable option/date combination | Implement the package-first date-price matrix |
| Treatment plan | One quote-level calendar-date plan | Separate consecutive relative-day plan per Quote Option | Different packages may deliver different schedules |
| Common clinical information | Grafts, visual plan, clinician, and notes stored on Quote | Retained once on the parent Quote with common requirements | Avoid duplicating facts shared by all options |
| Acceptance handoff | Quote and treatment-date selection | Stable Quote, Quote Option, and option/date-price identifiers | Allow FR-005 to preserve the exact patient choice |
| Version and audit | Primarily quote scalar fields | Complete parent-and-options aggregate snapshot and option-aware audit | Preserve legally meaningful quote history |
| Analytics | Quote records used as the response unit | Parent quotes and contained options counted separately | Prevent option volume from distorting quote-response conversion |
| Provider editing surface | One flat Screen 1 field table | Ordered seven-tab flow with per-tab completion gates and Sub-screen 2A | Make a 1–5 option aggregate editable without one unmanageable form |
| Field ownership | Implicit; provider-editable versus system-derived not stated | Canonical Quote Data Ownership Matrix; one editing surface or explicit read-only owner per field | Remove ambiguity over who writes each field in a multi-level aggregate |
| Quote currency | Treated as a quote-level value without a stated owner | Loaded from active system configuration, snapshotted on the quote, never provider input | Preserve historical price integrity and stop per-quote currency drift |
| Clinician cardinality | Single clinician on the quote | One or more clinicians shared by every option | Reflect team-delivered procedures; propagated to FR-010 by CR-FR010-20260909-01 |
| Graft description | Free provider field | Generated from the approved system template and the graft estimate; read-only | Keep patient-facing wording consistent across providers |
| Plan day resolution | Plan days stated as resolvable to calendar dates | Day numbers stay relative for the life of the record and are never persisted as calendar dates | Confirmed prior product decision; FR-010 consumes the plan by day number |
| Quote-amount analytics | Quote amount assumed to be a single value | Amount metrics use the accepted option/date price only; unaccepted quotes count in volume/conversion but not amount | A 1–5 option quote has a price range, not an amount, until acceptance |
| Treatment technique | Technique appeared as a required quote component without an owner | Technique details load read-only through the exact immutable Treatment-version relationship and are not duplicated on Quote | Preserve one source of truth while keeping historical quote display stable |
| Restricted-recipient source | FR-037 and FR-038 were both named | Only FR-037 advice-mode conversions can carry an exclusive assigned provider | FR-038 is self-service and converts only to FR-011 |
| Quote lifecycle vocabulary | Workflow used `accepted/booked` and `provider-withdrawn` variants | Canonical Quote statuses are `accepted` and `withdrawn` | Keep API, entity, and workflow state contracts identical |
| Verification coverage | Acceptance scenarios only | Unit, integration, contract, end-to-end, security, and performance coverage is required | Satisfy the Constitution testing hierarchy |
| Audit administration | Workflow wording implied Admin could edit audit history | Admin may view immutable audit/version history; corrections are append-only governed actions | Preserve Constitution-required tamper resistance |
| Validation bounds | Several text and attachment rules referenced unspecified limits | Field lengths and file count/type/size limits are explicit | Make UI and API validation testable |
| Evidence and approvals | Empty References section, stale transcription locators, and placeholder approval metadata | Correct source locators and recorded/absent approvals are explicit | Keep verification evidence auditable without inventing approvals |
| Dependent owner contracts | FR-019, FR-024, and FR-026 retained pre-option or missing ownership contracts | Promotion attachment, package provenance, and quote configuration align to the FR-004 aggregate | Remove non-deferred integration ambiguity |

## Scope and Impact

### In Scope

- FR-004 provider creation, editing, display, lifecycle, and aggregate data contract.
- Multiple parent quotes from the same provider for an active inquiry.
- One-to-five option validation.
- Package snapshotting and quote-local inline customization.
- Option/date pricing and option-specific relative day plans.
- Aggregate versioning, audit, migration, and stable downstream identifiers.
- The ordered seven-tab provider creation/edit flow and the canonical Quote Data Ownership Matrix.
- System-configured currency snapshot, system-generated graft description, plural clinician assignment, and quote-level attachments.
- Relative-only option plan days and the accepted-price-only basis for quote-amount analytics.
- Exact immutable Treatment-version relationship with read-only related technique details and no duplicate Quote technique field.
- Canonical `accepted` and `withdrawn` lifecycle terms, FR-037-only restricted routing, and the mandatory verification matrix.
- Immutable Admin audit access, explicit field/file limits, corrected evidence, and honest approval metadata.
- FR-019 option/date promotion attachment, FR-024 Quote Option package provenance, and FR-026 quote-currency/expiry configuration ownership.

### Out of Scope

- Editing FR-005 or FR-006 in this change.
- Final patient comparison/acceptance behavior, booking creation, payment collection, fund release, payout, or cancellation economics.
- Saving quote-local customization back into the provider package library.
- Product-code, API, database, or UI implementation changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Workflow 1, Screens 1–7, Business Rules, REQ-004-001 and REQ-004-014 through REQ-004-030, Key Entities, Implementation Notes, and User Scenarios
- **Related FRs**: FR-005 must later select one option/date combination; FR-006 must later book that accepted choice; FR-008 consumes accepted-option travel inclusions; FR-010 consumes the accepted option plan; FR-019 supplies structured promotions; FR-024 owns reusable package presets
- **System documents**: the system PRD FR-004 section and the system data schema `quotes` family (tables 7 and 7A–7F, Treatment-version relationship, quote status enum, deprecated columns) are reconciled as of 2026-09-10. Still open: the system technical specification, and the system PRD FR-005 section, whose one-quote-at-a-time acceptance wording predates the option/date acceptance contract

### Implementation Reconciliation

- **Existing implementation evidence**: `main/hairline-backend/app/Http/Controllers/Quotes/QuotesController.php::store()` blocks a second provider quote, validates one package, creates customized `Package` records, and writes quote-level dates/services/plans. `app/Models/Quote.php` exposes singular package ownership. `app/Services/QuoteVersionService.php` snapshots only the current parent/singular-package shape. `app/Services/BookingService.php` calculates booking value from accepted quote-level treatment dates.
- **Required assessment**: Provider and Admin web flows; patient quote payload; create/update/detail/list/accept APIs; Quote aggregate models; package isolation; option/date-price acceptance; version/audit snapshots; notifications; analytics; booking/travel/treatment consumers; authorization; concurrency; and regression tests.
- **Compatibility / rollout risk**: A destructive one-step replacement would break existing single-package clients and downstream acceptance/booking consumers. Roll out additively with a temporary single-option compatibility adapter and explicit consumer cutover.
- **Data migration**: Required. Create option-owned records, backfill every legacy quote as one Quote Option, move or associate its package snapshot, dates, services, selections, and plan, verify parity, then deprecate direct quote ownership only after all consumers migrate.

## Acceptance and Validation

- The same provider can create more than one parent quote for one active inquiry without overwriting or merging their histories.
- Every submitted quote contains at least one and no more than five ordered options.
- Each option retains its source package identity/version and a stable quote-owned snapshot.
- Inline option edits never change or create reusable package-library records.
- Every applicable option/date combination has a valid appointment slot, timezone, and price.
- Each option retains an independent consecutive relative-day plan; common clinical facts exist only on the parent quote.
- Quote list, detail, version, audit, and analytics outputs distinguish parent quotes from options.
- FR-005 can identify exactly one accepted Quote Option and option/date-price record without ambiguity.
- Legacy single-package quotes remain readable and produce equivalent values throughout the migration period.
- Every field on Screen 1 resolves to exactly one row of the Quote Data Ownership Matrix, with one provider-editing surface or an explicit read-only/system-derived owner.
- Option plan days are stored and consumed as relative day numbers only; no surface persists them as calendar dates.
- Quote-amount analytics read the accepted option/date price; unaccepted quotes appear in volume and conversion metrics only.
- Technique details resolve read-only through the exact immutable Treatment ID/version relationship and are not copied onto Quote.
- Restricted-recipient handling identifies FR-037 only; no FR-038 provider-assignment path remains.
- Quote lifecycle workflows and entities use only the canonical `accepted` and `withdrawn` terms.
- The PRD defines required unit, integration, contract, end-to-end, security, and performance coverage.
- Admin surfaces never edit audit history; corrections create append-only audited records.
- Text and attachment validation limits are explicit and traceable to current schema/platform conventions.
- FR-019, FR-024, and FR-026 expose the option-aware promotion, package-provenance, currency, and expiry contracts consumed by FR-004.
- FR-010 references the accepted Quote Option and its relative plan days, with no singular `packageId` or quote-level `plan` dependency.
- Implementation reconciliation remains `Required` until database migration, API contract, UI flows, downstream consumers, and regression evidence are verified.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-09-09; v2.3-v2.6 verification amendments approved 2026-09-10
- **Decision evidence**: [SRC-MTG-002, MTG-002-D03 through D06 and O01](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md), followed by Product Owner clarification and approval in the 2026-09-09 project task
- **PRD change log**: FR-004 v2.0 through v2.6
- **Update log**: [`FR004_QUOTE_OPTIONS_MODEL_2026-09-09.md`](../../update-logs/2026-09-09/FR004_QUOTE_OPTIONS_MODEL_2026-09-09.md) and [`FR004_VERIFICATION_FIXES_2026-09-09.md`](../../update-logs/2026-09-09/FR004_VERIFICATION_FIXES_2026-09-09.md)
- **Downstream change requests**: [CR-FR010-20260909-01](../fr010-treatment-execution/change-request-2026-09-09-clinician-cardinality-alignment.md) (clinician cardinality), [CR-FR010-20260910-01](../fr010-treatment-execution/change-request-2026-09-10-quote-option-consumer-alignment.md) (accepted-option package and plan consumption), [CR-FR019-20260910-01](../fr019-promotions-discounts/change-request-2026-09-10-option-date-promotion-alignment.md), [CR-FR024-20260910-01](../fr024-treatment-package-management/change-request-2026-09-10-quote-option-provenance-alignment.md), and [CR-FR026-20260910-01](../fr026-app-settings-security/change-request-2026-09-10-quote-configuration-ownership.md). FR-005, FR-006, and FR-008 reconciliation of the option/date acceptance contract remains open and unscheduled.
- **Supersedes**: None
- **Superseded by**: None
