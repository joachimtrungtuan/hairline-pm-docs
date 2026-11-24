# FR-019 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 2.9 to 3.0, with a graph change-set)
**Scope**: FR-019 Promotions and Discounts
**Source of findings**: `plans/reports/tester-261124-fr019-logic-p1.md` (20 findings; each ruled fix, neighbour-only or settled by the PRD)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr019-promotions-discounts/prd.md`

- **Release and restore**: `archived` is a release reason; restoring an archived quote re-checks the promotion, takes a new reservation and is refused when the limit is used up or the promotion has ended (REQ-019-015, REQ-019-086).
- **Provider-selected promotion that cannot be used**: at send the provider sees the reason and the quote is sent without it only after the provider confirms; at acceptance an exhausted limit is handled like an invalid code (FR-005 REQ-005-026). A draft quote drops a revoked or paused program at send. Pause, revoke or end after send does not affect a sent quote (already stated, kept).
- **Patient code and the row's promotion**: a patient code replaces the promotion the row carries; an automatic promotion's reservation is released as `not_applied`; a failed code falls back to the price the row carried at send, including its promotion (REQ-019-034, REQ-019-039, REQ-019-040, REQ-019-099).
- **Ranking**: a provider-selected promotion wins over a provider auto-applied one on a row; the usage limit is checked before ranking, so a full automatic program is skipped (REQ-019-035, REQ-019-038). An admin edit that creates a new version of a sent quote counts as a re-send.
- **Provider-fault transfer**: the replacement quote carries no promotion; the original Application is Superseded (which takes precedence over Voided) and its use returns to the limit (REQ-019-019, REQ-019-070, REQ-019-089).
- **Lifecycle and approval**: no program-level Pending Approval; an Admin-via-Provider program is Active on publish and applies only to providers whose adoption is Accepted; if every provider declines the program stays Active with no participants; a provider activates its own Draft; only the side that paused may resume, and who paused is recorded (REQ-019-023, REQ-019-027, REQ-019-028, REQ-019-049, REQ-019-051).
- **Admin overrides and re-invite**: an admin can never force a provider into a program; the overrides are Force-Revoke and Re-invite, and Re-invite works from Declined, Auto-Declined, Revoked-by-Provider and Revoked-by-Admin; Expired in the Past tab means the program end date has passed (REQ-019-060, REQ-019-109).
- **Auto-decline window**: default 3 business days on the form, the assumption line and the setting (REQ-019-094).
- **Provider selection and options**: a provider picks a promotion from the list and types no code (FR-004 select-or-create field); the package-upgrade type and the treatment-only, travel-only and other scopes are removed, so Applies To is a fixed Whole price label (REQ-019-033, REQ-019-085).
- **Usage rules**: affiliate codes follow the same usage rule (reserved at acceptance, consumed at first payment, no code entry at checkout); Applied means reserved at acceptance; code status on release or void, revoked codes and refunds after first payment are stated (REQ-019-014, REQ-019-068, REQ-019-069).
- **Data and reporting**: the pre-acceptance code is held with the open subquote view and stored only on the AcceptanceEvent; funnel counts for Code Entered and Validated come from logged validation requests; the Audit Trail Panel shows old and new values for edits (REQ-019-057).
- **Wording**: "95% of valid codes within 1 second" in both places; REQ-019-075 reads per subquote.

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr019-logic-p1-fixes.yaml`

- New: steps STP-019-021 to -023 (decline or auto-decline, consume at first payment, release or void) and field ENT-promotion-program.paused_by with values admin and provider.
- Rule statements and titles updated to mirror the PRD (25 rules); step titles, flow descriptions, the auto-decline setting and field descriptions updated.
- Enum values: release_reason `archived` added; lifecycle_state `pending_approval`, discount_type `package_upgrade` and applies_to `treatment_cost`, `travel_cost`, `other` retired.
- Edges: dead `next` edges of STP-019-019 and -020 removed; decline and consume or release branches added; approval-requested event emitted at STG-main-02-quote; reconciliation event emitted at STG-admin-02-operations; admin stage writes ENT-promotion-adoption; `shows applies_to` edges re-wired.
- Cross-FR edges: STG-provider-03-active no longer emits, and STG-main-02-quote now emits, EVT-promotion-discount-approval-requested (FR-030-owned event).
- Test-applied on a scratch copy of the graph: 120 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes for FR-004 (line 211, REQ-004-090), FR-005 (offered-price definition, acceptance-event code description), FR-018 (Rule 13, applied definition, checkout code entry, registration claim), FR-017 (ENT-discount-code, SCR-017-07, SCR-017-08) and FR-030 (approval-requested event description) are queued in the logic review ledger section for FR-019, not applied. Leftovers for the implementation backlog are listed there too.
