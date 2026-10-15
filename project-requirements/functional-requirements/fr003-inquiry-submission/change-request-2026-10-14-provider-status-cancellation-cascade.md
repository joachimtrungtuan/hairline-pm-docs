# Change Request: Provider Status Cancellation Cascade for Inquiries

**Change Request ID**: CR-FR003-20261014-01
**Primary FR**: FR-003
**Triggering FR / Event**: FR-015 v1.8/v1.9 provider suspension and deactivation cascade ([CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md)); Product Owner decision of 2026-10-14 extending deactivation to the suspension scope
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-14
**Decision Date**: 2026-10-14
**PRD Version Change**: v2.6 to v2.7
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-015 defines a provider-status cancellation cascade: when a provider becomes `Suspended` or `Deactivated`, all of that provider's non-terminal Accepted, Confirmed, In Progress, and Aftercare cases are cancelled with a provider-caused cause and an independent admin-support marker. As of 2026-10-14, deactivation matches suspension scope. FR-003 owns inquiry distribution, inquiry cancellation, and patient inquiry messaging, so it must apply the inquiry-level part of that contract. FR-003 was Verified & Approved, so this alignment is recorded as a controlled change.

## Baseline State

**Source version**: FR-003 v2.6, Workflow 2, General Inquiry Rules 2 and 4, Screen 8, Cancellation Requirements, Key Entities

- Distribution and reassignment did not revalidate provider status; a suspended or deactivated provider could still receive allocation through in-flight jobs or retries.
- Inquiry cancellation was defined only for patient-initiated and account-deletion causes. No provider-caused cause or support marker existed.
- Patients had only the patient-cancellation messaging path.

## Approved State

**Target version**: [FR-003 v2.7](prd.md), Workflow 2 Alternative Flow B4, General Inquiry Rules 2/4/6, Screen 8 notes, REQ-003-019/020, Key Entities, Edge Cases

- From the effective time of `Suspended` or `Deactivated`, the provider is ineligible for allocation, exclusive routing, and reassignment; eligibility is revalidated at allocation and in-flight work cannot revive participation.
- An inquiry whose accepted treatment belongs to the affected provider is cancelled with cause `ProviderSuspended` or `ProviderDeactivated` and `supportRequired = true`.
- An inquiry still comparing providers keeps its stage; only that provider's ProviderInquiry participation and quotes are cancelled, the inquiry is flagged for support, and other providers' offers remain.
- Patients receive the provider-caused cancellation or offer-unavailability message with Contact Admin/Support, not the patient-cancellation message.
- Completed and already-cancelled inquiries are not reclassified; reactivation restores nothing and does not clear the marker. Clearing requires audited admin resolution.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Distribution eligibility | No provider-status revalidation | Only `Active` providers eligible; revalidated at allocation, exclusive routing, and reassignment | FR-015 REQ-015-020 eligibility revalidation |
| Accepted-provider inquiry | Cancelled only by patient or account deletion | Cancelled with `ProviderSuspended` or `ProviderDeactivated` plus `supportRequired` | FR-015 A5 step 4 |
| Comparing inquiry | No partial provider cancellation | Only affected ProviderInquiry participation and quotes cancelled; stage kept; flagged for support | Preserve unrelated providers' offers |
| Cancellation identity | Patient reasons and "Account Deleted (System)" only | Distinct provider-caused causes and an independent support marker, not a stage | Separate cause from patient cancellation and Payment Window Expired |
| Patient messaging | Patient-cancellation confirmation only | Provider-caused message with Contact Admin/Support | FR-015 REQ-015-019 |

## Scope and Impact

### In Scope

- FR-003 distribution eligibility, inquiry-level cascade outcomes, patient dashboard messaging, requirements, entity notes, and edge cases.
- This FR-local Change Request.

### Out of Scope

- Triggering the provider status event, provider notifications, admin filters, and support resolution UI (FR-015, FR-016, FR-020).
- Quote cancellation mechanics (FR-004), acceptance and hold release (FR-005/FR-006), payment blocking and refunds (FR-006/FR-007), and care-stage cancellation (FR-010/FR-011).
- System PRD, data schema, and technical specification edits.

### Affected Contracts

- **PRD owner**: [FR-003](prd.md) — Workflow 2 Alternative Flow B4, General Inquiry Rules 2/4/6, Screen 8, REQ-003-019/020, Key Entities.
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) owns the trigger and cascade (A5, Screen 4); [FR-004](../fr004-quote-submission/prd.md) cancels quotes (CR-FR004-20261014-01); [FR-005](../fr005-quote-comparison-acceptance/prd.md) blocks acceptance; FR-006, FR-016, and FR-020 own holds/payment, admin visibility, and message delivery.
- **System documents**: Unchanged here; cancellation cause values and the `supportRequired` marker require schema assessment during reconciliation.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Distribution and reassignment eligibility guards; job/retry revalidation; inquiry and ProviderInquiry cancellation storage; support marker storage and audited resolution; patient dashboard messaging; deduplication per provider-status event.
- **Compatibility / rollout risk**: Must deploy together with FR-004/FR-005/FR-006 cascade handling so inquiries and quotes are cancelled consistently.
- **Data migration**: To be assessed. Do not relabel existing terminal inquiries.

## Acceptance and Validation

- A suspended or deactivated provider receives no new allocation, including through retries started before the effective time.
- An inquiry accepted with the affected provider is Cancelled with the provider-caused cause and `supportRequired`; a comparing inquiry keeps its stage, loses only the affected provider's participation and quotes, and is flagged.
- The patient sees the provider-caused message with Contact Admin/Support; no patient cancellation reason is requested.
- Replay of the same event produces no duplicate cancellations, flags, or messages; reactivation restores nothing.
- Cross-FR verification with FR-004/FR-005/FR-006/FR-015 and implementation evidence are required before reconciliation is marked Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-14 (FR-015 verification review, Issue 4 option 1).
- **Decision evidence**: [CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md) Affected Contracts; FR-015 Alternative Flow A5, Screen 4, Rules 9-10, REQ-015-017 to REQ-015-021.
- **PRD change log**: [FR-003 Appendix: Change Log](prd.md#appendix-change-log), v2.7 dated 2026-10-14.
- **Update log**: [FR015_VERIFICATION_ALIGNMENT_2026-10-14.md](../../update-logs/2026-10-14/FR015_VERIFICATION_ALIGNMENT_2026-10-14.md).
- **Supersedes**: None.
- **Superseded by**: None.
