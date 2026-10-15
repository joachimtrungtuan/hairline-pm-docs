# Change Request: Provider Status Cancellation Cascade for Quotes

**Change Request ID**: CR-FR004-20261014-01
**Primary FR**: FR-004
**Triggering FR / Event**: FR-015 v1.8/v1.9 provider suspension and deactivation cascade ([CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md)); Product Owner decision of 2026-10-14 extending deactivation to the suspension scope
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-14
**Decision Date**: 2026-10-14
**PRD Version Change**: v2.9 to v3.0
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-015 defines a provider-status cancellation cascade: when a provider becomes `Suspended` or `Deactivated`, that provider's outstanding quotes and the accepted quotes of its cancelled non-terminal cases are cancelled with a provider-caused cause. As of 2026-10-14, deactivation matches suspension scope. FR-004 owns quote submission and quote lifecycle status, so it must apply the quote-level part of that contract. FR-004 was Verified & Approved, so this alignment is recorded as a controlled change.

## Baseline State

**Source version**: FR-004 v2.9, Workflows 1/3/4, Alternative Flows, Screens 4/5, Business Rules, Cancellation Cascade Requirements, Key Entities

- Quote creation and submission revalidated inquiry status and restricted-recipient mode, but not provider status.
- Quote cancellation statuses covered other-accepted and patient inquiry cancellation only. No provider-caused status or provenance existed.

## Approved State

**Target version**: [FR-004 v3.0](prd.md), Workflow 1 provider status check, Workflow 3 provider-status trigger, Workflow 4 terminal states, Alternative Flows, Screens 4/5 status values, Business Rules, REQ-004-031/032, Key Entities, Edge Cases

- Only `Active` providers may create, edit, or submit quotes; provider status is revalidated at creation and submission and in-flight submissions after the effective time are rejected.
- At the effective time, the provider's unaccepted draft/sent parent quotes and the accepted parent quote of each case cancelled by FR-015 move to `cancelled_provider_status` with `cancellationProvenance` `ProviderSuspended` or `ProviderDeactivated`.
- Cancellation is recorded once per parent quote; Quote Options and option/date alternatives become unavailable with their parent and are not cancelled or counted separately.
- The AcceptanceEvent, accepted IDs/versions, and quote-local package snapshots are not rewritten; terminal and completed-case history is not reclassified; other providers' quotes are unaffected; reactivation restores nothing.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Submission eligibility | Inquiry-active and restricted-recipient checks only | Provider must be `Active`; revalidated at creation and submission | FR-015 REQ-015-020 eligibility revalidation |
| Unaccepted quotes | Remained sent after provider suspension or deactivation | Cancelled once per parent quote with `cancelled_provider_status` | FR-015 A5 step 3 |
| Accepted quote of cancelled case | No provider-caused outcome | Cancelled with provider-caused provenance; AcceptanceEvent, IDs/versions, and snapshots unchanged | Preserve immutable accepted provenance |
| Status and provenance | No provider-caused status | `cancelled_provider_status` plus `ProviderSuspended` or `ProviderDeactivated` in `cancellationProvenance` | Distinguish from patient inquiry cancellation and Payment Window Expired |

## Scope and Impact

### In Scope

- FR-004 provider eligibility checks, quote-lifecycle outcomes, status values, requirements, entity notes, and edge cases.
- This FR-local Change Request.

### Out of Scope

- Triggering the provider status event and support handling (FR-015, FR-016, FR-020).
- Inquiry-level cancellation (FR-003), acceptance blocking and hold release (FR-005/FR-006), payment blocking and refunds (FR-006/FR-007), and care-stage cancellation (FR-010/FR-011).
- Package-library changes, quote editing screens, and System PRD, data schema, or technical specification edits.

### Affected Contracts

- **PRD owner**: [FR-004](prd.md) — Workflows 1/3/4, Alternative Flows, Screens 4/5, Business Rules, REQ-004-031/032, Key Entities.
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) owns the trigger and cascade (A5, Screen 4); [FR-003](../fr003-inquiry-submission/prd.md) owns inquiry-level outcomes (CR-FR003-20261014-01); [FR-005](../fr005-quote-comparison-acceptance/prd.md) blocks acceptance and retains the AcceptanceEvent; FR-014 analytics must not count option alternatives as separate cancellations.
- **System documents**: Unchanged here; the new status value and provenance require schema assessment during reconciliation.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Provider status guards on quote create/submit APIs; quote status enum and `cancellationProvenance`; cascade job deduplication per provider-status event and quote; immutability of AcceptanceEvent and option snapshots; provider/admin list and filter display.
- **Compatibility / rollout risk**: Must deploy together with FR-003/FR-005/FR-006 cascade handling; in-flight submissions racing the effective time must be rejected rather than published.
- **Data migration**: To be assessed. Do not relabel existing terminal quotes.

## Acceptance and Validation

- A suspended or deactivated provider cannot create or submit a quote; an in-flight submission after the effective time creates no sent quote.
- Each affected parent quote is cancelled exactly once, regardless of how many options or date alternatives it holds; other providers' quotes stay unchanged.
- Accepted quotes of cancelled cases keep their AcceptanceEvent, IDs/versions, and snapshots; completed and terminal history is not reclassified.
- Replay of the same event produces no duplicate cancellations or notifications; reactivation restores nothing.
- Cross-FR verification with FR-003/FR-005/FR-006/FR-015 and implementation evidence are required before reconciliation is marked Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-14 (FR-015 verification review, Issue 4 option 1).
- **Decision evidence**: [CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md) Affected Contracts; FR-015 Alternative Flow A5, Screen 4, Rules 9-10, REQ-015-017 to REQ-015-021.
- **PRD change log**: [FR-004 Appendix: Change Log](prd.md#appendix-change-log), v3.0 dated 2026-10-14.
- **Update log**: [FR015_VERIFICATION_ALIGNMENT_2026-10-14.md](../../update-logs/2026-10-14/FR015_VERIFICATION_ALIGNMENT_2026-10-14.md).
- **Supersedes**: None.
- **Superseded by**: None.
