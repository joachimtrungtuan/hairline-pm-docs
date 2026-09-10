---
source_id: SRC-MTG-002
source_type: stakeholder-meeting
meeting_date: not-provided
captured_on: 2026-09-09
validation_status: partially-validated
incorporation_status: partially-incorporated
---

# Meeting 02: Launch, Quote Options, Fund Release, and Payments

## Context

The meeting reviewed current Admin, Provider, and mobile status; a phased launch roadmap; pilot-provider onboarding; quote construction; payment release; payout methods; cancellations; and selected website work. The supplied evidence was a rough transcript attached outside the repository and was not copied into the project.

Participant names, roles, and the meeting date require confirmation.

## Confirmed Decisions and Directions

### MTG-002-D01: Controlled provider launch

Launch should begin with a small provider cohort across selected target countries. A range of 20 to 30 providers was discussed as an example of the initial cohort. Providers should be enrolled with a clear expected patient-launch date rather than asked to browse an empty system indefinitely.

Initial onboarding should combine project-team setup and one-to-one training. Self-service walkthroughs and scalable training resources were deferred until the system has realistic operating data and the team understands provider behavior better.

### MTG-002-D02: Catalog ownership

Treatment services should come from a shared system catalog. Each provider may opt into relevant services and configure its own pricing. Packages are provider-specific and are overseen rather than authored by Admin.

### MTG-002-D03: One response with multiple quote options

A provider should be able to assess one inquiry once and submit one quote response containing multiple options. Options may differ by treatment type, package, included services, date range, and price.

For operational and conversion analytics, this response counts as one quote with option-level records, not as many unrelated quotes. The transcript used “sub-quotes” as a possible description of the option records.

### MTG-002-D04: Presets with quote-local editing

Provider package presets should populate their included services and standard prices automatically. A provider may edit the selected option inline for the current patient without changing the global preset. Saving an edit for future quotes was discussed as a possible later control, not a current requirement.

### MTG-002-D05: Date and package price matrix

When multiple packages and treatment date ranges are offered, the quote should expose a price for each applicable date-and-package combination. Standard values should be prefilled and remain editable. Treatment facts shared by every package, such as the selected procedure and estimated grafts, should not be duplicated as package-specific facts.

### MTG-002-D06: Quote presentation and analytics

The patient should be able to compare the options offered by one provider. Provider and platform analytics must distinguish a provider response from the options inside that response so quote acceptance rates are not distorted.

### MTG-002-D07: Locale-safe date presentation

Ambiguous numeric dates create booking risk across countries. The preferred direction is to render dates using the user's configured locale or date-format preference. A written month is safer when no reliable preference is available.

### MTG-002-D08: Procedure completion requires patient participation

Marking the procedure complete should begin a patient-confirmation flow. The patient should receive email and push notification and be able to confirm completion or raise a problem. If the patient does not respond within a configurable window, release may proceed automatically.

The meeting mentioned 48 or 72 hours but did not approve a final default.

### MTG-002-D09: Launch payment-account direction

The launch should initially use the UK Stripe setup. A separate Ireland or EU setup may be added later. Payment routing should be based on the applicable billing/payment context, but the detailed entity and routing rules were not completed in this meeting.

### MTG-002-D10: Two provider payout rails

Eligible providers should use Stripe Connect so platform commission and provider funds are separated through Stripe. Providers in markets where that is unavailable should use a manual settlement cycle, potentially followed later by Revolut Business automation.

### MTG-002-D11: Post-booking cancellation ladder

The system needs multiple cancellation-fee tiers based on the interval before the appointment. The discussion also established that provider-initiated cancellation needs an explicit consequence and reassignment/refund treatment.

The actual tier percentages, day boundaries, fee ownership, and provider consequence were not finalized.

## Operational Direction

### MTG-002-P01: Phased launch roadmap

The meeting used a four-phase rollout covering commercial foundations, clinical operations, settlement and growth, then analytics/localization/advanced configuration. Dates and feature groupings were planning inputs rather than permanent requirement contracts.

### MTG-002-P02: Production data and feedback

The pilot needs realistic provider profiles, services, packages, pricing, and treatment data. The project team should establish training, support, notifications, and a structured feedback loop while the cohort is small.

### MTG-002-P03: Website and splash work

The updated splash design could proceed while broader system work continued. Website copy and several placeholder or outdated images also required stakeholder review. These items belong to design and website work rather than the requirement extraction itself.

## Current-State Observations

These statements describe what participants believed existed during the meeting. They require implementation verification before being used as current status:

- Admin, Provider, and mobile foundations were broadly present but used demo data in several areas.
- The current quote flow supported only one package per quote submission.
- Package presets could populate a later customization/pricing step.
- Patient installment support was said to exist but lacked reliable real-payment testing.
- Current payment intake was described as receiving funds into the Hairline Stripe account and paying providers later.
- A provider-withdrawal and reassignment flow was said to exist.

## Open Questions

### MTG-002-O01: Quote-option contract

The exact parent quote, option, package, date-price, acceptance, expiration, editing, and audit model remains to be specified.

#### Product Owner clarification and incorporation (2026-09-09)

The Product Owner approved the FR-004 quote-option model with these refinements:

- An inquiry may contain multiple parent quotes, including multiple quotes from the same provider. Each parent quote has an independent lifecycle, expiry, version history, and audit history.
- Each parent quote contains one to five ordered package-based Quote Options. These are the "sub-quotes" discussed in the meeting.
- Treatment is selected once on the parent quote; estimated grafts, graft description, visual treatment plan, clinicians, common notes, and common requirements are also shared parent fields. This supersedes the earlier wording in MTG-002-D03 that treatment type may differ by option.
- Each option starts from a provider package-library preset. Inline customization creates only a quote-owned snapshot and must not update or create reusable library records.
- Each option owns its included/custom services, applicable patient-requested date ranges, option/date prices and promotions, and a separate relative day-to-day treatment plan.
- Provider Quote Creation/Edit uses an ordered tabbed flow: Treatment Service; Package Options with a quote-local Inline Package Editor; Grafts & Visual Plan; combined Dates & Pricing; Option Treatment Plans; Clinical Details & Notes; and Review & Submit.
- The FR-004 data contract uses a canonical ownership matrix so every parent, option, item, date-price, plan, and system-derived field has one editing surface or an explicit read-only owner. Currency is loaded from system configuration, snapshotted for historical prices, and never entered by the provider.
- Parent quote metrics and Quote Option metrics remain distinct.

This clarification resolves MTG-002-O01 for the FR-004 creation and aggregate data contract. FR-005 acceptance and FR-006 booking reconciliation remain separate later changes.

### MTG-002-O02: Confirmation deadline

Choose one default patient-confirmation window and define how disputes pause or replace automatic release.

### MTG-002-O03: Connect timing and long lead times

The meeting raised uncertainty about Stripe holding or transfer timing when a procedure is more than approximately 90 days away. The final design must be verified against the applicable Stripe product and legal model.

### MTG-002-O04: Patient payment plans

Full payment, deposit plus balance, and installments were discussed. Exact collection dates, transfer dates, failure handling, and which plans use which payout rail were not finalized.

### MTG-002-O05: Cancellation economics

The meeting did not decide the fee ladder, who receives a patient cancellation fee, or what a provider owes after provider-initiated cancellation.

### MTG-002-O06: Scheduling integration

Direct booking against provider availability and possible automated quotes were explicitly described as future enhancements.

## Requirement Routing for Later Work

| Items | Likely owner | Current action |
|---|---|---|
| MTG-002-D01, P01, P02 | Product launch plan and provider onboarding | Record only |
| MTG-002-D02 | Provider management and catalog contracts | Record only |
| MTG-002-D03-D06, O01 | FR-004 and data contracts | Incorporated into FR-004 v2.0–v2.2 through CR-FR004-20260909-01; implementation reconciliation required |
| MTG-002-D07 | Localization and shared presentation rules | Record only |
| MTG-002-D08-D10, O02-O04 | FR-007, FR-017, and FR-029 | Material reconciliation required later |
| MTG-002-D11, O05 | FR-006, FR-007, and legal/commercial terms | Material reconciliation required later |
| MTG-002-P03 | Website and design work | Not a PRD update |

## Validation Needed

- Confirm the meeting date, participant names, and stakeholder roles.
- Confirm whether 20 to 30 providers is an approved cohort or an illustrative range.
- Reconcile FR-005 acceptance and FR-006 booking against the approved parent-quote, option, and option/date-price identifiers in later controlled phases.
- Use the written payments brief as the more detailed source for fund-release and payment questions, while preserving its unresolved status.
