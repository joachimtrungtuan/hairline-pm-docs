# FR-019 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 3.0 to 3.1, with a graph change-set)
**Scope**: FR-019 Promotions and Discounts
**Source of findings**: `plans/reports/tester-261124-fr019-logic-p2.md` (11 findings; each ruled fix or wiring-only)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr019-promotions-discounts/prd.md`

- **A use returns**: the "returns only when" sentence also names the provider-fault transfer (Superseded) (General Module Rules, REQ-019-014).
- **Admin revive**: a revive that goes through returns the Application from Voided to its Active status and clears `use_returned_at`; a Voided Application is terminal except through that revive (General Module Rules, Screen 6 rules, REQ-019-014, REQ-019-015, REQ-019-070).
- **Per-patient usage limit**: counts reserved plus consumed uses by the same patient on the same program and is checked where the total limit is checked: at send for a known patient, at code validation and at confirm (new REQ-019-116; REQ-019-035, REQ-019-038, REQ-019-039, REQ-019-040, REQ-019-086).
- **Fixed amount at or above the row price**: the promotion is not attached (or the patient's code is refused), the reason is shown and the price is unchanged (new REQ-019-117; Value row, attach-failure reasons in REQ-019-086, REQ-019-114).
- **Fixed-amount conversion for a patient code**: converted at the rate in effect at validation; the amount shown at confirm is the one frozen at acceptance (REQ-019-018, REQ-019-084).
- **Auto-applied eligibility**: "explicit eligibility rules" replaced by the Screen 2 fields that define it: Start / End Date, the usage limits and, for a Hairline Only program, Issuance Channel and Recipient Binding (REQ-019-052).
- **Application Mode for Hairline-Funded programs**: only Auto-applied or Code-only; List-selection and Either are not offered. The Screen 2 field row, the rule, the Notes line, the Screen 9 validation wording and a new acceptance criterion are aligned (REQ-019-056).
- **Terms change on an adopted Both Fees program**: when an admin changes Value or Hairline Share %, every adopting provider is notified with the old and new terms; the change applies to later quotes only; the adoption stays Accepted and can be revoked (new REQ-019-118; new acceptance criterion).
- **Notices**: the S-03 line lists the provider notices that exist (approval request, terms changed), and states that Force-Revoke, admin Pause and admin Resume of an adopted program notify the adopting providers and that a provider's own revoke notifies admins (REQ-019-010).

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr019-logic-p2-fixes.yaml`

- New: rules REQ-019-116 to -118 and steps STP-019-024 to -028 (Force-Revoke, Re-invite, provider revoke, pause or resume, code revoke).
- Rule statements updated to mirror the PRD (13 rules, REQ-019-056 also retitled); descriptions corrected for application status, hairline portion, provider portion, application mode, the reconciliation event, use returned at, per-user usage limit and value.
- Edges: new rules linked to stages, fields and sources, and to the steps that check them; the new steps are placed on screens and stages, apply their rules and are reached by branch `next` links with conditions from STP-019-003, -005, -014 and -021.
- Cross-FR edges: none; all new edges end at FR-019 nodes or at platform stages, actors and the FR-019 source.
- Test-applied on a scratch copy of the graph: 123 change rows, no errors; the copy was deleted.

## Not changed here

FR-030 catalogue rows for the terms-changed notice, the Force-Revoked, Paused and Resumed notices to adopting providers and the provider-revoked notice to admins; an FR-006 echo of the revive result; FR-004 and FR-005 wording for the new attach and validation checks. They are queued in the logic review ledger section for FR-019, not applied. Leftovers for the implementation backlog are listed there too.
