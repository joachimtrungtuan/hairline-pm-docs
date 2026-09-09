---
source_id: SRC-DOC-001
source_type: stakeholder-provided-document
source_date: 2026-09-08
received_on: 2026-09-08
validation_status: pending-review
incorporation_status: not-incorporated
raw_source: ../raw/Hairline Fund Release & Payments Brief.mhtml
---

# Fund Release and Payments Brief

## Provenance and Authority

This is a normalized extraction of the stakeholder-provided `Hairline Fund Release & Payments Brief.mhtml`. The raw MHTML is preserved unchanged.

The artifact states that its implementation-status column came from a code audit dated 2026-09-08 and refers to a companion `Hairline Payment Routing Spec (developer) v1.0`. That companion document was not supplied with this source package.

This brief mixes four kinds of information. They remain separate below:

1. Requirement statements.
2. Dated implementation-audit observations.
3. Open product, legal, and commercial decisions.
4. Author recommendations and suggested implementation order.

Nothing in this extraction has been incorporated into a PRD.

## Requirement Statements

### DOC-001-R01: Procedure-completion release trigger

Provider procedure completion should start a patient-confirmation clock. The patient receives email and push notification and may confirm completion or raise a problem. No response by the configured deadline allows automatic release; a dispute pauses release for Admin resolution.

The trigger is procedure completion, not completion of a longer aftercare programme.

### DOC-001-R02: Configurable confirmation window

Admin needs one editable completion-confirmation window used consistently by notification, dispute, and release behavior. The document recommends 72 hours, but also records a conflicting seven-day figure from another specification. The default remains unresolved.

### DOC-001-R03: Release by provider payout rail

Released provider funds should route through Stripe Connect when the provider has an eligible connected account. Otherwise, released amounts should enter a configured settlement cycle for manual payment or later payment-service automation.

### DOC-001-R04: Manual settlement cycle

The manual rail needs configurable settlement period, cutoff day, payout day, approval, transfer-result recording, retry/failure handling, and provider-facing statement status. Automating manual-rail payments through Revolut Business is separable from launching with an operational “mark as paid” process.

### DOC-001-R05: Launch and future Stripe accounts

Launch should use one UK platform account. An Ireland or EU account may be enabled later when justified by volume and operating entities. This is separate from provider connected-account onboarding.

### DOC-001-R06: Provider payout-method onboarding

Each provider needs an explicit payout method: Stripe Connect or manual bank settlement. The Admin provider-creation flow and Provider billing settings should show the method and its readiness state.

### DOC-001-R07: Patient payment-plan selection

Checkout should allow the patient to select among eligible full-payment, deposit-and-balance, and installment plans and preview the resulting schedule.

### DOC-001-R08: Balance collection

For a deposit plan, the remaining balance should be collected at a configured interval before the procedure, with patient reminders, retry/failure handling, early manual payment, and a configured cancellation point if the balance remains unpaid.

### DOC-001-R09: Financial ledger and actual processing fees

Payment, refund, transfer, and payout events should record actual processor fees and support per-booking reconciliation rather than relying only on configured commission values.

### DOC-001-R10: Configurable cancellation-fee ladder

Cancellation fees should use multiple editable tiers based on days before the appointment. The patient must see the applicable fee and expected refund before confirming cancellation. The policy must operate consistently across full payment, deposit, and installment plans.

The example percentages and intervals in the raw brief are illustrative, not approved values.

### DOC-001-R11: Provider-initiated cancellation

Provider cancellation requires full patient refund handling and an explicit provider consequence that can be reconciled through future payouts. The commercial rule is unresolved and must align with the clinic agreement.

### DOC-001-R12: Configurable billing settings

The document identifies these configuration concepts:

- completion-confirmation window;
- settlement period;
- settlement cutoff day;
- payout day;
- provider payout method;
- cancellation-fee tiers;
- balance-charge interval before treatment; and
- unpaid-balance cancellation interval.

Defaults remain subject to the decisions below.

## Dated Implementation-Audit Observations

The following statements are audit evidence attributed to 2026-09-08, not product requirements and not verified by this extraction task:

### DOC-001-A01: Configuration versus money movement

The artifact reports that commission configuration, deposit rates, installments, saved cards, and payout-statement structures largely existed, while hold-and-release, Stripe Connect, automated settlement generation, and patient plan selection did not.

### DOC-001-A02: Treatment-completion behavior

The artifact reports that a provider completion action and an unused treatment-completed notification existed, but no patient completion confirmation, dispute flow, confirmation deadline, or release orchestration was wired end to end.

### DOC-001-A03: Manual payout statements

The artifact reports that payout statements and several statuses existed, but generation required an Admin request for one provider/date range and list actions were not fully connected to real settlement behavior.

### DOC-001-A04: Payment routing

The artifact reports that per-country platform Stripe configuration existed, but provider connected accounts, Connect onboarding, transfers, and destination-charge behavior did not.

### DOC-001-A05: Patient payment options

The artifact reports partial full-payment and deposit support, implemented installment scheduling, and no Flutter payment-plan picker. It also reports missing automated balance charging, early balance payment, actual Stripe-fee capture, and Connect-dependent transfer behavior.

### DOC-001-A06: Cancellation behavior

The artifact reports a hard-coded patient refund ladder, no recorded cancellation-fee allocation, no complete interaction with deposit/installment shortfalls, and no provider-side cancellation consequence.

These observations should be moved into or cited by a dated implementation report if the team later verifies them against the named source branches.

## Open Decisions

### DOC-001-O01: Confirmation default

Choose 72 hours, seven days, or another approved value. One setting must own the behavior across every contract.

### DOC-001-O02: Provider cancellation consequence

Choose a percentage, fixed amount, patient-refund plus processing costs, or another contractually approved model.

### DOC-001-O03: Patient cancellation-fee allocation

Decide whether Hairline, the provider, or both parties receive the fee and how any split is calculated.

### DOC-001-O04: Cancellation configuration scope

Decide whether launch supports only a global ladder or also provider-specific overrides. The document recommends allowing provider ownership in the data model while initially shipping global administration.

### DOC-001-O05: Revolut timing

Decide whether the Revolut Business integration is required for launch or follows a manual settlement process later.

### DOC-001-O06: Missing companion specification

Obtain and review the referenced Payment Routing Spec before treating routing timings, destination-charge behavior, long-lead-time handling, or reversal logic as approved.

## Author Recommendations

The raw artifact recommends this broad order:

1. Cancellation tiers and policy administration.
2. Completion confirmation, dispute, and release approval.
3. Manual settlement-cycle automation.
4. Patient plan selection, balance collection, and fee capture.
5. Stripe Connect.
6. Revolut Business automation.

This ordering is advice from the artifact, not an approved roadmap.

The raw artifact also contains endpoint names, field names, command names, UI placements, and implementation suggestions. Those details remain available in the raw source but are not reproduced as requirements because they require technical review and may drift with implementation.

## Requirement Routing for Later Work

| Items | Likely owner | Current action |
|---|---|---|
| DOC-001-R01-R04, R11-R12 | FR-017, FR-029, and financial operations | Record only |
| DOC-001-R05-R09 | FR-007, FR-017, and FR-029 | Record only |
| DOC-001-R10-R11 | FR-006, FR-007, legal terms, and clinic agreement | Record only |
| DOC-001-A01-A06 | Dated implementation-status report | Verify separately before reuse |
| DOC-001-O01-O06 | Product, legal, commercial, and technical decisions | Resolve before PRD reconciliation |

## Validation Needed

- Confirm which requirement statements came directly from the stakeholder and which were authored during preparation of the artifact.
- Obtain the companion Payment Routing Spec.
- Resolve the six open decisions.
- Re-run any implementation claims against the intended branches before treating them as current.
