# Change Request: MTG-002 Quote Model Alignment for Packages

**Change Request ID**: CR-FR024-20261016-01
**Primary FR**: FR-024
**Triggering FR / Event**: MTG-002 quote-model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v1.2 to v1.4
**Related Commit(s)**: Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

The MTG-002 quote-model verification found that FR-024 still described packages as add-on items (hotel, transport, medication, and so on) summed with one treatment into a quote total, while FR-004 treats each package as one alternative Quote Option. FR-024 also had no included-items structure for FR-004 to copy, let providers choose a currency per package and per treatment, kept a current `QuoteTreatment` record, counted usage through the deprecated `quote_packages` link with statuses FR-004 does not use, and did not separate library edits from quote-local inline edits. The Product Owner decisions of 2026-10-16 redefine a package as a full template that seeds one Quote Option, remove library currency, and fix two distinct edit paths.

**Status change**: FR-024 was `✅ Verified & Approved` at v1.2. With this Change Request the PRD status becomes `🟡 Revised — Pending Consolidated Verification` until the MTG-002 consolidated verification passes.

## Baseline State

**Source version**: FR-024 v1.2, `Main Flow: Provider Creates Package`, `Alternative Flows (Packages)`, Screens 3 to 5, `Business Rules`, `Field Calculation Rules`, User Stories 3, 4 and 6, `Functional Requirements Summary`, and `Key Entities`

- Packages had a type taxonomy (Hotel, Transport, Flights, Medication, PRP Therapy Add-On, Consultation, Custom) and no included-items list, travel services, or relative-day plan.
- REQ-024-010/011 and User Story 4 let a provider select one treatment and zero or more packages and summed them into one quote total.
- Treatments and packages each carried a provider-chosen currency, with an exchange-rate-lock edge case.
- `QuoteTreatment` remained a current linking record, and `QuotePackage` remained a deprecated compatibility link.
- Usage Count used `quote_packages` with statuses `submitted`, `accepted`, and `scheduled`.
- Edit rules said both "cannot modify packages already included in submitted quotes" and "edit creates a new version", and the inline quote edit path was not contrasted with the library edit.
- Treatment identity across versions, package status vocabulary, hard-delete, patient-visible package fields, and the stale-price fallback were unstated or ambiguous.

## Approved State

**Target version**: FR-024 v1.4, same headings plus `Business Rules > Package Edit Paths`, Rules 8 to 11, REQ-024-030 to REQ-024-035, and Entities 6 and 7

The updated [FR-024 PRD](./prd.md) owns the detail. In summary: a package is a full template for one Quote Option holding included items with prices, flight, hotel, transport and other travel services, and a relative-day plan; the date range, notes and documents are never packaged; each selected package is one alternative option, at most five per parent quote, never summed, with the standard price prefilling each date-range price row; library prices use the system quote currency; each library edit creates a new version and leaves earlier versions read-only, while inline quote edits stay quote-local and are never written back. The Screen 3 treatment Base Price is a reference-only, non-binding "starting from" value: it may prefill new FR-004 quote rows only where no other standard value exists and may feed a future post-MVP starting price on provider cards, but it is never binding and never read after a quote is sent.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Package definition | Typed add-on (hotel, transport, medication, PRP, and so on) with one price | Full Quote Option template: included items, travel services, relative-day plan, standard price; date range, notes, and documents never packaged; add-on types removed | D17 (FR-024-2) |
| Package use in a quote | One treatment plus zero or more summed packages | Each selected package seeds one alternative Quote Option, one to five per parent quote, never summed; subquotes number up to options × date ranges; standard price prefills each date-range price row | D17, M1 (FR-024-2) |
| Included items | None | PackageItem (service type, name, description, optional price, included flag) and PackagePlanDay entities for FR-004 to copy | D17 (FR-024-1) |
| Currency | Provider-chosen per package and per treatment; exchange-rate lock edge case | Removed; all library prices use the system quote currency; edge case deleted | D18 (FR-024-3) |
| QuoteTreatment and QuotePackage | Current linking record and deprecated compatibility link | Both removed as records of this module; FR-004 parent Quote and Quote Options own treatment and package provenance | D17, M10 (FR-024-5) |
| Usage Count and deactivation | `quote_packages` count on `submitted`, `accepted`, `scheduled` quotes | Quote Options copied from the package whose parent quote is `draft` or `sent`; warning "used in N open quotes"; status values follow FR-004 | M8 (FR-024-6) |
| Edit paths | Contradictory lock wording; inline path not contrasted | Library edit creates a new version (v1, v2, and so on), earlier versions read-only, existing quotes never change; inline edit in FR-004 is quote-local, never written back, never creates a version; option records source package ID, version, and inline-customised flag | M10, D17 (FR-024-8, FR-024-9) |
| Minor clarifications | Ambiguous treatment identity; `available`/`unavailable` status; hard delete allowed; patient fields read live; last-known-good price fallback; approvals not refreshed | Stable ID plus version; `active`/`inactive`; no hard delete; patient fields from the option copy or recorded version; selection blocked when the API is unavailable; approvals row added | R7-3 (FR-024-4, FR-024-10 to FR-024-14) |
| Treatment Base Price (v1.4) | "Starting price for treatment" with no stated use in quotes | Reference-only, non-binding "starting from" value; may prefill new quote rows only where no other standard value exists; may feed a future post-MVP provider-card starting price; never read after send | Q20 |

## Scope and Impact

### In Scope

- FR-024 module scope, package main flow, Alternative Flows A3 to A5 and B3, Screens 3 to 5, Business Rules (including the new Package Edit Paths section), Field Calculation Rules, Dependencies, Implementation Notes, User Stories 3, 4 and 6, Edge Cases, requirements, Key Entities, and Approvals.
- Correction of the stale traceability line in CR-FR024-20260910-01.

### Out of Scope

- Payment rails, fund release, refunds, and later instalments.
- FR-004 quote-creation screens, draft handling of a package deactivated or edited mid-draft (owned by FR-004), and the schema `packages` version column (owned by `system-data-schema.md`).
- Implementation, API, and migration changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Main Flow: Provider Creates Package, A3, A4, A5, B3, Screens 3 to 5, General Module Rules 3, 5, 8 to 11, Package Edit Paths, Provider Editability Rules, Field Calculation Rules, User Stories 3, 4 and 6, REQ-024-007, 008, 010, 011, 014, 026, 030 to 034, Entities 1 to 7.
- **Related FRs**: FR-004 (Quote Option seeding from one package, up to five options, standard-price prefill of date-range rows, copy of included items, travel services and plan, inline quote-local edits, `isCustomized` flag, status values `draft` and `sent` for Usage Count, behaviour for a source package deactivated mid-draft), FR-005 (patient sees options as alternatives; subquotes up to options × date ranges), FR-008 (included travel services come from the option copy), FR-022 (package filter and status vocabulary), FR-026 and FR-029 (system quote currency and exchange rates).
- **System documents**: `system-prd.md` (package definition and examples), `system-data-schema.md` (`packages` version column and immutable versions, `package_items` with version, plan-day table, no package or treatment currency, removal of `quote_treatments` and `quote_packages`), and `system-technical-spec.md` (package versioning and no stale-price fallback).

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in this documentation phase.
- **Required assessment**: Package data model (types, items, plan days, versions), currency fields on packages and treatment pricing, Usage Count query, quote-creation package selection and price prefill, legacy `QuoteTreatment` and `QuotePackage` consumers, and regression coverage.
- **Compatibility / rollout risk**: High. Existing typed add-on packages and any summed-quote logic must be migrated to option templates.
- **Data migration**: To be assessed.

## Acceptance and Validation

- No "add-on" package type, `QuoteTreatment`, or `quote_packages` remains in FR-024 except removal notes.
- Each selected package seeds one Quote Option, at most five per parent quote, never summed; the standard price prefills each date-range price row.
- Packages carry included items, travel services, and a relative-day plan; the date range, notes, and documents are never packaged.
- No treatment or package carries its own currency.
- Usage Count counts Quote Options whose parent quote is `draft` or `sent`; deactivation warns "used in N open quotes".
- The library edit path (new version, earlier versions read-only, existing quotes unchanged) and the FR-004 inline quote-local path are both stated and contrasted.
- The treatment Base Price is described as reference-only and non-binding, prefills quote rows only where no other standard value exists, and is never read after a quote is sent (REQ-024-035).
- Cross-FR checks against FR-004 and `system-data-schema.md` pass in consolidated verification.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote-model verification)
- **Approved by**: Product Owner — documentation approved 2026-10-16 via the decision log; implementation reconciliation required, not assessed
- **Decision evidence**: SRC-MTG-002; `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (D17, D18, M1, M8, M10, R7-3; Q-series Q20)
- **PRD change log**: FR-024 v1.3 and v1.4 rows dated 2026-10-16
- **Update log**: `../../update-logs/2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md`
- **Supersedes**: CR-FR024-20260910-01 in part (the retained `QuotePackage` compatibility link)
- **Superseded by**: None
