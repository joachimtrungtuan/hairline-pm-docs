# FR-030 Logic Review, Pass 1: PRD Fixes (2026-11-24)

**Type**: Major update (substantially revised PRD, cross-document alignment)
**Document**: `local-docs/project-requirements/functional-requirements/fr030-notification-rules-config/prd.md` (v1.23 to v1.24)
**Graph change-set**: `local-docs/project-requirements/graph/changesets/2026-11-24-fr030-logic-p1-fixes.yaml` (test-applied on a scratch copy, 377 change rows; not applied to the live graph, the controller applies it)
**Review source**: `plans/reports/tester-261124-fr030-logic-p1.md` (24 findings; the triage rulings were applied as given)
**Author report**: `plans/reports/docs-manager-261124-fr030-logic-p1-fixes.md`

## What changed

- **Cancellation and booking notices**: `inquiry.cancelled` fires only in Inquiry or Quoted and also on an admin Close inquiry; providers holding a quote get `quote.cancelled_inquiry` only. `booking.cancelled` lists its causes, and a provider drop-out follows FR-006 and FR-020 (one `booking.cancelled`, then `booking.provider_fault_replacement`).
- **Catalogue**: new rows for the Confirm and Decline links and the reminder event on `provider.status_cancellation_patient`, account-deletion, data-request and legal notices, installment, overdue and refund-escalation notices, `review.response_removed` and `monitoring.progress_reminder`. `payment.received` and `payment.failed` are locked. `review.requested` counts from the eligibility date.
- **Critical and locked**: one definition (the locked notices); quiet hours, rate limit and coalescing exempt them; the Critical toggle on Screen 2 is a read-only indicator.
- **Rule behaviour**: one pause rule (events skipped, queued notices still delivered, Purge Queue); seeded Active rules and catalogue defaults; refusal of overlapping Active rules; escalation as a fixed condition list plus wait time for locked notices only; hard bounce, outage and permanent-failure outcomes; bounce flag for any account type with a `system.alert` event; in-app entry built from the push template; Delay before/after plus Skip If Too Late; held notices sent in order; aftercare progress reminder schedule field; template archive and draft block while an Active rule uses it; secondary-contact options removed; one payment reminder setting.
- **Graph**: 3 new Events, 17 catalogue Rules plus the aftercare schedule rule (REQ-030-235 to REQ-030-252), 1 new Step, 2 new Fields, rewording of existing Rule, Event and Step nodes, new enum values (`affiliate`, `before`, `after`, `not_delivered`, `not_opened`), 3 retired Fields, 11 system steps moved to the configuration stage, and the cross-FR edges listed in the author report.

## Left for later

- Neighbour FRs queued in the ledger section for this pass: FR-020, FR-007, FR-007B, FR-009, FR-015 and FR-013.
- About 152 other `applies at` rule edges and the entity reads and writes edges of FR-030 still sit at the Inquiry stage.
- REQ-030-004 and REQ-030-022 keep the FCM and Web Push integration wording on purpose.
