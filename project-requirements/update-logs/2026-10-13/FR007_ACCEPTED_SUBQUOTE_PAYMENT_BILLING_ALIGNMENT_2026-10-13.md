# FR-007 Accepted Subquote Payment and FR-017 Billing Alignment

**Date**: 2026-10-13
**Status**: Documentation approved; scoped document checks passed; consolidated verification and implementation reconciliation pending
**Scope**: Remaining Meeting 02 quote-model payment/billing consumer alignment only

## Changes

- [FR-007 v1.6](../../functional-requirements/fr007-payment-processing/prd.md): consume one accepted subquote through FR-006/FR-005; display accepted package/services, date/appointment, price, attached promotion, locked currency and provenance across checkout and provider/admin financial/refund views; validate the original initial-payment hold; preserve terminal expiry and no quote reopening; distinguish optional itemization from the final offered price; retain existing FR-019 applications and later payment balances. Added REQ-007-016–019 and scoped regression scenarios.
- [CR-FR007-20261013-01](../../functional-requirements/fr007-payment-processing/change-request-2026-10-13-accepted-subquote-payment-context.md): approved major event affecting the previously verified payment source/eligibility contract; before/after, scope, legacy-data risk, validation criteria, and implementation reconciliation recorded separately from documentation approval.
- [FR-017 v2.7](../../functional-requirements/fr017-admin-billing-finance/prd.md): clarify accepted-snapshot invoice amounts/itemization/currency and Booking Reference provenance; retain one invoice record per booking across installments; correct acceptance/invoice dependency ownership and exchange-rate test timing. No new financial policy, controls, entity, or major restructure; this small clarification uses the PRD change log and this normal log, not an additional Change Request.
- [Source register](../../sources/source-register.md): record downstream payment/billing incorporation without validating unrelated source items.
- [Update-log index](../README.md): add this date/topic entry and refresh Last Updated while retaining prior records.

## Evidence and Approval

- [Meeting 02 D03–D05](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md#mtg-002-d03-one-response-with-multiple-quote-options): parent options, quote-local package customization, and package/date pricing.
- [Meeting 02 O01 clarifications](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md#mtg-002-o01-quote-option-contract): multiple parent quotes per provider/inquiry, atomic complete subquote acceptance, immutable AcceptanceEvent, booking handoff, and terminal payment-window expiry.
- [FR-005 Key Entities](../../functional-requirements/fr005-quote-comparison-acceptance/prd.md#key-entities) and [FR-006 Key Entities](../../functional-requirements/fr006-booking-scheduling/prd.md#key-entities): owning provenance/snapshot contracts; accepted versions identify the same parent aggregate revision.
- [FR-019 patient overlay](../../functional-requirements/fr019-promotions-discounts/prd.md#patient-platform-screens-p-03-overlay): existing checkout-code validation/replacement rules remain unchanged; separately recorded applications do not overwrite quote acceptance.
- Product Owner approval in this chat: “Please help me make all those pending works,” after remaining work was scoped to FR-007 and conditional FR-017 alignment. This records documentation approval, not technical/finance sign-off or implementation proof.

## Validation

- Scoped checks passed: FR-007 has 19 unique sequential requirement definitions and 37 well-formed tables; FR-017 has 27 unique sequential requirement definitions and 40 well-formed tables. All 38 new/changed local links and anchors resolve; the 2026-10-13 index count matches its 3 files.
- Checked accepted identifiers/version invariant, current metadata/approval separation, and removal of generic FR-007 quote-price/package-source and checkout-currency-selection wording. Compared pre-existing requirement definitions against the baseline: all 13 unchanged FR-007 definitions and 24 unchanged FR-017 definitions remain intact outside the explicitly revised requirements. Reviewed the changed source/eligibility/billing contracts and delta scope.
- `git diff --check` passed. Existing financial policy differences beyond quote-source alignment remain for the separate consolidated review, not silently changed here.
- No source-code changes or processor/runtime tests. Full cross-FR verification is not performed or implied by these edits.

## Deferred / Preserved Boundaries

- Provider-suspension/cancellation/admin-support follow-ups stay deferred.
- Meeting 01/03, fund-release brief, payment rails, and unresolved payment/cancellation economics are not incorporated.
- Existing deposit/commission/refund/installment/payout/fee/attribution policies remain unchanged; their broader reconciliation belongs to subsequent verification, not this quote-source alignment.
- System PRD/schema/technical-spec edits, implementation/data migration, and commits/pushes are not part of this step.
