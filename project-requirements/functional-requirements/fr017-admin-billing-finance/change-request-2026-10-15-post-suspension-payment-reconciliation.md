# Change Request: Post-Suspension Payment Reconciliation

**Change Request ID**: CR-FR017-20261015-01
**Primary FR**: FR-017
**Triggering FR / Event**: FR-015 fifth verification pass (2026-10-15) found that FR-015 v1.13 Rule 9 requires payments captured after provider suspension/deactivation to stay recorded and reach admin financial reconciliation, while FR-007 only rejects payments before the processor call and no FR covered late captures or remaining scheduled installments on cancelled bookings
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v2.9 to v2.10
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

When FR-015 suspends or deactivates a provider, it cancels all non-terminal cases with cause `ProviderSuspended` / `ProviderDeactivated` and marks them Admin Support Required. A delayed processor callback can still report a capture after that point, and installment plans could keep charging. FR-015 Rule 9 says such captures must be recorded and reconciled, but no FR owned the reconciliation.

The Product Owner assigned ownership to FR-017 (A-05 Billing & Financial Reconciliation): (1) a late capture is recorded as a real transaction, does not confirm a booking or revive the case, is excluded from provider earnings, payout, and commission recognition, and is flagged "Captured after provider cancellation" for admin resolution through the existing refund/adjustment workflow; (2) remaining scheduled installments are cancelled, and already-paid installments go to admin financial resolution; (3) amounts on these bookings are held from provider payout statements until admin resolution.

## Baseline State

**Source version**: FR-017 v2.9, Business Rules (Rule 13), Edge Cases (provider suspended or deactivated), REQ-017-001 to REQ-017-027

- Rule 13 excluded provider-status-cancelled bookings from payout calculation, issued no automatic refund, and routed captured payments (including those captured while the cascade ran) to admin financial resolution.
- No rule covered a capture arriving after cancellation: whether it could confirm a booking, how it was flagged, or whether it counted toward earnings and commission.
- No rule stopped remaining scheduled installments; Payment Rule 3 retries could still apply.
- Completed-procedure payout on such bookings was left to admin financial resolution without a stated hold.

## Approved State

**Target version**: [FR-017 v2.10](prd.md), Workflow B3, Business Rules 14 to 16, Screen 4 (Reconciliation Flag), Entities 1 and 3, REQ-017-028 and REQ-017-029

- Late captures are recorded, flagged, linked to the case/inquiry and the FR-015 provider-status event, and excluded from earnings, payout, and commission until resolved via Screen 4b with mandatory reason and audit entry.
- Remaining unpaid installments are set to Cancelled with no further charges or retries; paid installments stay recorded for resolution.
- Booking amounts are held from payout statements until resolution; release uses the existing Screen 7 "Add to Next Payout" path under normal eligibility and approval rules.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Late capture after provider-status cancellation | Not defined | Recorded as a real transaction; no booking confirmation or case revival; excluded from earnings, payout, commission; flagged for admin (Rule 14) | Implements FR-015 Rule 9 reconciliation |
| Scheduled installments | Could continue charging and retrying | Remaining installments cancelled; paid installments to admin resolution (Rule 15) | Prevents charges on a booking that cannot proceed |
| Payout handling | Excluded from payout calculation (Rule 13) | Held from payout statements until admin resolution; release via existing "Add to Next Payout" (Rule 16) | Makes completed-procedure handling explicit without changing payout timing |
| Reconciliation view | No exception flag | Screen 4 Reconciliation Flag field, filter, and exceptions section | Gives admin a place to find and resolve these cases |
| Workflow | None | Alternative Flow B3 | Documents the end-to-end path |
| Data | Entity 1 and 3 without flag or Cancelled installment status | Entity 1 `reconciliation_flag`, `provider_status_event_id`; Entity 3 `Cancelled` payment status | Supports the flag and installment cancellation |
| Requirements | REQ-017-001 to 027 | Added REQ-017-028 and REQ-017-029 | Make the rules testable |

## Scope and Impact

### In Scope

- FR-017 Workflow B3, Rules 14 to 16, Screen 4 field and filter notes, Entities 1 and 3, FR-007 and FR-015 dependency notes, edge-case bullets, REQ-017-028/029, change log v2.10, and approval row.
- This FR-local Change Request.

### Out of Scope

- New refund percentages, fees, or payout rails; Rule 7 tiers remain not auto-applied to provider-status cancellations.
- Payout timing, cycle, and buffer redesign.
- FR-007 behavior: captures and charges are still executed by FR-007 / S-02, which is unchanged.
- System PRD, schema, and technical specification updates.
- Source code, API, or live configuration changes.

### Affected Contracts

- **PRD owner**: [FR-017](prd.md) — Workflow B3, Business Rules 13 to 16, Screen 4, Entities 1 and 3, REQ-017-028, REQ-017-029.
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) v1.13 Rule 9 (source of the reconciliation obligation and the provider-status event). [FR-007](../fr007-payment-processing/prd.md) unchanged; captures and charges still executed by FR-007 / S-02, with A-05 classifying post-cancellation captures. FR-016 Admin Support Required marker unchanged.
- **System documents**: None changed.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code or runtime behavior was inspected or changed.
- **Required assessment**: Webhook/capture handling for bookings or cases already cancelled with a provider-status cause; installment scheduler and retry job behavior on such bookings; invoice flag storage and Screen 4 filter/section; payout statement generation exclusion and hold; earnings and commission calculation exclusion; refund/adjustment audit entries.
- **Compatibility / rollout risk**: Existing provider-status-cancelled bookings may already have late captures recorded as normal payments or active installment schedules; these need review and flagging before the new rules are enforced.
- **Data migration**: To be assessed.

## Acceptance and Validation

- A capture reported after a `ProviderSuspended` cancellation is stored, leaves the booking cancelled, shows the "Captured after provider cancellation" flag with links to the case/inquiry and provider-status event, and does not appear in provider earnings, payout statements, or commission totals.
- After a provider is deactivated, no further installment charges or retries run for affected bookings; remaining installments show Cancelled and paid installments remain on the invoice.
- Admin resolution via Screen 4b requires a reason, writes an audit entry, and clears the flag.
- A completed procedure on a cancelled booking is not included in a payout statement until admin records a resolution.
- FR-015 Rule 9 and FR-007 contracts are consistent with FR-017 v2.10.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan, during FR-015 verification review.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-15; FR-017 documentation delta only.
- **Decision evidence**: FR-015 fifth verification pass decision approved 2026-10-15 assigning post-suspension payment reconciliation to FR-017.
- **PRD change log**: [FR-017 Appendix: Change Log](prd.md#appendix-change-log), v2.10 dated 2026-10-15.
- **Update log**: [FR015_FIFTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_FIFTH_VERIFICATION_FIXES_2026-10-15.md).
- **Supersedes**: None.
- **Superseded by**: CR-FR017-20261016-01 in part (a provider suspended or deactivated after acceptance now follows the FR-006 provider-fault transfer, so the patient is rehomed instead of left without rebooking).
