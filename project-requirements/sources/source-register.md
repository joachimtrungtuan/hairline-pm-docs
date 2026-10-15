# Subsequent Stakeholder Source Register

## Status Key

- **Pending review**: extracted by the project team but not yet confirmed as a faithful stakeholder record.
- **Partially incorporated**: specific items were validated and reconciled into an owning contract while the rest of the source remains pending.
- **Validated**: source owner or Product Owner confirmed the extraction.
- **Incorporated**: validated items were reconciled into their owning product contracts.
- **Superseded**: a later validated source replaced the applicable items.

## Registered Sources

| Source ID | Source | Type | Source date | Captured / received | Status | Authority note |
|---|---|---|---|---|---|---|
| SRC-MTG-001 | [Service routes, onboarding, and product recommendations](meetings/meeting-01-service-routes-onboarding-and-product-recommendations.md) | Stakeholder meeting extraction | Not provided | 2026-09-09 | Pending review | Mixed confirmed direction, working models, future direction, and open questions |
| SRC-MTG-002 | [Launch, quote options, fund release, and payments](meetings/meeting-02-launch-quote-options-fund-release-and-payments.md) | Stakeholder meeting extraction | Not provided | 2026-09-09 | Partially incorporated | D03–D06 and O01 were refined and incorporated into FR-004, FR-005, and FR-006 v2.3 through their approved Change Requests; D06 analytics is also incorporated into FR-014 v3.7 through CR-FR014-20261007-01; downstream payment/billing consumption is documentation-aligned in FR-007 v1.6 and FR-017 v2.7; all other items remain pending |
| SRC-MTG-003 | [Quote flow feedback, localization, and website](meetings/meeting-03-quote-flow-feedback-localization-and-website.md) | Stakeholder meeting extraction | 2026-09-17 | 2026-09-18 | Pending review | Stakeholder feedback and new direction on the quote flow, localization, website, and billing; the revised quote hierarchy is reported status, not a new decision |
| SRC-DOC-001 | [Fund release and payments brief](briefs/2026-09-08-fund-release-and-payments-brief.md) | Stakeholder-provided document extraction | 2026-09-08 | 2026-09-08 | Pending review | Mixed requirements, dated code audit, author recommendations, and open decisions |

## Missing Provenance

- Exact dates for SRC-MTG-001 and SRC-MTG-002.
- Confirmed participant names and stakeholder roles for SRC-MTG-003, and confirmation of the clinic-diary and banking providers it names.
- Confirmed participant names and stakeholder roles for both meetings.
- Durable external locations for the three meeting recordings or rough transcripts.
- The `Hairline Payment Routing Spec (developer) v1.0` referenced by SRC-DOC-001.

## Incorporation Status

- SRC-MTG-002 items D03–D06 and O01 were refined by the Product Owner for FR-004 on 2026-09-09, FR-005 on 2026-09-15, and the FR-006 booking handoff on 2026-09-16. They are incorporated through `CR-FR004-20260909-01`, `CR-FR005-20260915-01`, and `CR-FR006-20260915-01` respectively.
- SRC-MTG-002 item D06 and the refined D03–D05/O01 hierarchy were reconciled into [FR-014 v3.7](../functional-requirements/fr014-provider-analytics-reporting/prd.md) on 2026-10-07 through [CR-FR014-20261007-01](../functional-requirements/fr014-provider-analytics-reporting/change-request-2026-10-07-parent-quote-subquote-analytics.md). Parent/inquiry counting, immutable accepted-price analytics, valid-hold aging, accepted-price-bracket distribution, and the metric-only locked-cockpit exception are documentation-approved; implementation reconciliation and consolidated verification remain pending. No additional fund-release/payment-routing decisions were incorporated by this step.
- No SRC-MTG-001, SRC-DOC-001, SRC-MTG-003, or remaining SRC-MTG-002 item has been incorporated.
- The refined D03–D05/O01 model is consumed by [FR-007 v1.6](../functional-requirements/fr007-payment-processing/prd.md) and clarified in [FR-017 v2.7](../functional-requirements/fr017-admin-billing-finance/prd.md) on 2026-10-13: one accepted subquote's immutable commercial base via FR-006, original initial-payment hold, locked currency, and booking-based financial history. [CR-FR007-20261013-01](../functional-requirements/fr007-payment-processing/change-request-2026-10-13-accepted-subquote-payment-context.md) and the [payment/billing update log](../update-logs/2026-10-13/FR007_ACCEPTED_SUBQUOTE_PAYMENT_BILLING_ALIGNMENT_2026-10-13.md) record documentation approval; implementation reconciliation and consolidated verification remain pending. Existing FR-019 checkout applications are preserved, not a new source decision; no payment-rail, fund-release, or cancellation-economics items are incorporated.
- SRC-MTG-003 reports the implementation status of the already-incorporated SRC-MTG-002 quote-option items and does not supersede them. Its own decisions, principally the reduced quote flow, head-scan annotation, localization, and the billing/payout rails, require Change Requests before implementation.
