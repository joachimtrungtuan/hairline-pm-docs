# Change Request: MTG-002 Quote Model Alignment for Quote and Slot-Hold Settings

**Change Request ID**: CR-FR026-20261016-01
**Primary FR**: FR-026
**Triggering FR / Event**: MTG-002 quote-model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v1.11 to v1.13
**Related Commit(s)**: Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

The MTG-002 quote-model verification found that no FR owned the slot-hold duration (FR-006 kept its own "after payment failure" hold setting), that FR-026 captured quote expiry and currency "when a new parent Quote is created" so drafts were ambiguous, that the Quote Configuration currency was a second currency setting beside the FR-029 Default Currency and was never seeded, and that the reminder lead times for an expiring quote and an expiring hold had no owner. The Product Owner decisions of 2026-10-16 make FR-026 the owner of all four quote and hold settings, capture expiry and currency at first send, and use the FR-029 Default Currency as the single quote currency.

**Status change**: FR-026 was `✅ Verified & Approved` at v1.11. With this Change Request the PRD status becomes `🟡 Revised — Pending Consolidated Verification` until the MTG-002 consolidated verification passes.

## Baseline State

**Source version**: FR-026 v1.11, `Alternative Flows > A7`, Screen 1, Screen 5d, `Admin Editability Rules`, `Dependencies`, `Initial Configuration / Seeding`, User Story 8, `Edge Cases`, `Functional Requirements Summary`, and `Key Entities`

- Quote Configuration held an admin-selected "Active Quote Currency" and a "Default Quote Expiry" (default 48 hours).
- FR-004 snapshotted the currency and computed expiry "when a new parent Quote is created"; draft handling was undefined and no configuration version was recorded on the quote.
- No slot-hold duration, hold-expiring-soon lead time, or quote-expiring-soon lead time existed in FR-026.
- Quote Configuration was not seeded, and its currency had no stated relationship to the FR-029 Default Currency.
- The Executive Summary listed three setting groups instead of four, and the FR-020 SLA-breach alert was not traced as a consumer of the Analytics Configuration.

## Approved State

**Target version**: FR-026 v1.13, same headings plus REQ-026-030 and REQ-026-031

The updated [FR-026 PRD](./prd.md) owns the detail. In summary, Quote Configuration is one versioned, audited setting group with four admin-set values and one read-only currency:

| Setting | Default | Consumer |
|---|---|---|
| Quote Expiry Window | 48 hours | FR-004 (copied read-only onto each quote at first send) |
| Quote Expiring Soon Lead Time | 12 hours | FR-004 (emits `quote.expiring_soon`, delivered through FR-030 and FR-020) |
| Slot-Hold Duration | 48 hours | FR-005 (hold placed at acceptance) and FR-006 (hold management and admin revive) |
| Hold Expiring Soon Lead Time | 12 hours | FR-006 (patient "hold expiring soon" reminder, delivered through FR-030 and FR-020) |
| Quote Currency (read-only) | FR-029 Default Currency | FR-004 (copied read-only onto each quote at first send) |

Validation bounds: the quote expiry window is 24 to 336 hours, the slot-hold duration is 24 to 168 hours, and each lead time is at least 1 hour and at most half of the window it warns about. Each FR-029 Default Currency change creates a new Quote Configuration version, so the version recorded on a quote identifies both the hours and the currency used.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Slot-hold duration | No owner; FR-006 kept its own hold setting | FR-026 owns it, versioned and audited, default 48 hours; one fixed hold from acceptance, using the duration in effect when placed; never extended by payment failure | D14, M3 (S2-5, FR-026-1) |
| Reminder lead times | None | Hold-expiring-soon lead time (default 12 hours, FR-006) and quote-expiring-soon lead time (default 12 hours, FR-004); each shorter than its window; changes apply to unsent reminders only | M13, FR-004 v3.1 handoff |
| Capture point | "When a new parent Quote is created" | At first send, read-only, with the configuration version recorded; drafts carry neither value; later changes never affect a sent quote | D15, M11 (FR-026-2, FR-026-5) |
| Expiry setting | "Default Quote Expiry", implying an override | "Quote Expiry Window"; one admin setting, no per-quote extension | M11 (FR-026-4, FR-026-9) |
| Quote currency | Separate admin-selected currency, not seeded | The FR-029 Default Currency, shown read-only; a change in FR-029 records a new Quote Configuration version; seeding takes it from FR-029 | D16 (FR-026-3, S2-6) |
| Settings API outage | Undefined for quote send | FR-004 blocks the first send and keeps the quote as a draft | R7-3 (FR-026-6, part) |
| Minor clarifications | Three setting groups listed; FR-020 alert not traced | Four groups listed; FR-020 traced as a consumer of the Analytics Configuration TTFQ SLA target | R7-3 (FR-026-7 part, FR-026-8) |
| Validation bounds | Positive whole hours; lead time shorter than its window | Quote expiry window 24 to 336 hours; slot-hold duration 24 to 168 hours; each lead time from 1 hour up to half of its window; 12-hour reminder defaults kept | Q13 |
| Currency versioning | A Default Currency change records a new version | Stated as a requirement: each Default Currency change creates a new Quote Configuration version, so the recorded version identifies both hours and currency | Q14 |

## Scope and Impact

### In Scope

- FR-026 Status line, Executive Summary, Module Scope, Alternative Flow A7, Screen 1 setting groups, Screen 5d, Admin Editability Rules, Internal Dependencies, Seeding, User Story 8, Edge Cases, REQ-026-012f, REQ-026-026, REQ-026-027, new REQ-026-030 and REQ-026-031, Entity 11, Change Log, and Approvals.

### Out of Scope

- Payment rails, fund release, refunds, and later instalments.
- Whether the FR-020 SLA-breach check uses the TTFQ target in effect at distribution or at check time (not decided).
- Implementation, API, and migration changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — sections listed under In Scope.
- **Related FRs**: FR-004 (first-send capture, recorded configuration version, `quote.expiring_soon`, outage behaviour), FR-005 (hold placed at acceptance for the FR-026 duration), FR-006 (hold management, admin revive, hold-expiring-soon reminder; no separate hold setting), FR-029 (Default Currency is the quote currency; disable guard should cover the quote currency), FR-030 and FR-020 (quote-expiring-soon and hold-expiring-soon events at the FR-026 lead times; TTFQ SLA alert consumer).
- **System documents**: `system-data-schema.md` (Quote Configuration fields for hold duration and lead times; drop "customizable" from `expiration_hours`; quote records the configuration version), `system-technical-spec.md` (hold placed at acceptance for the FR-026 duration), and `system-prd.md` (settings ownership).
- **Earlier CR**: CR-FR026-20260910-01 is superseded in part (admin-selected quote currency and creation-time capture).

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in this documentation phase.
- **Required assessment**: Quote Configuration storage and Settings API response, quote send path and recorded configuration version, hold placement and expiry jobs, reminder scheduling, FR-029 currency link, and regression coverage.
- **Compatibility / rollout risk**: Medium. Any existing per-booking hold setting and creation-time expiry capture must be migrated.
- **Data migration**: To be assessed.

## Acceptance and Validation

- Screen 5d lists the quote expiry window, quote-expiring-soon lead time, slot-hold duration, and hold-expiring-soon lead time, each with a default and a consumer, and shows the quote currency read-only from FR-029.
- No "when a new parent Quote is created", "Default Quote Expiry", or admin-selected quote currency remains in FR-026.
- The hold is one fixed hold from acceptance, never extended by payment failure, and existing holds keep their end time when the duration changes.
- Screen 5d, A7, REQ-026-012f, and User Story 8 enforce the bounds: expiry window 24 to 336 hours, slot-hold duration 24 to 168 hours, each lead time from 1 hour up to half of its window; out-of-bounds saves are blocked.
- REQ-026-012f states that a Default Currency change in FR-029 creates a new Quote Configuration version.
- Cross-FR checks against FR-004, FR-005, FR-006, FR-029, FR-030, and the schema pass in consolidated verification.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote-model verification)
- **Approved by**: Product Owner — documentation approved 2026-10-16 via the decision log; implementation reconciliation required, not assessed
- **Decision evidence**: SRC-MTG-002; `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (D14, D15, D16, M3, M11, M13, R7-3; Product Owner follow-up decisions Q13, Q14)
- **PRD change log**: FR-026 v1.12 and v1.13 rows dated 2026-10-16
- **Update log**: `../../update-logs/2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md`
- **Supersedes**: CR-FR026-20260910-01 in part (admin-selected quote currency and creation-time capture)
- **Superseded by**: None
