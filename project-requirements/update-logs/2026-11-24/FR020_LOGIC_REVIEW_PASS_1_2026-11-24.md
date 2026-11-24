# FR-020 Logic Review Pass 1 (2026-11-24)

**Scope**: FR-020 Notifications and Alerts, PRD v2.16 to v2.17. Pass 1 of the logic review; 17 findings, all accepted and fixed in FR-020, with the changes to other FRs queued.
**Evidence**: reviewer report `plans/reports/tester-261124-fr020-logic-p1.md`; fixer report `plans/reports/docs-manager-261124-fr020-logic-p1-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr020-logic-p1-fixes.yaml` is prepared and NOT applied (the controller applies it).
**Owner defaults**: entries 89 to 93 in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md` (only providers holding a quote are told of an inquiry cancel; a locked notice is critical; a mandatory patient notice goes by email when every channel is off; the legal acceptance reminder cannot be switched off; affiliate notices by email only).

## Changes to the PRD

- New rule: a notice whose toggle is locked (mandatory) is critical; it is sent at once and is exempt from quiet hours, the hourly rate limit and coalescing. The Urgency badge only displays. The legal acceptance reminder is the one locked notice that is not critical (REQ-020-158, Alternative Flow B1).
- Inquiry cancellation: the trigger is a patient cancel in the Inquiry or Quoted stage, or an admin Close inquiry (FR-006); providers are no longer recipients of `inquiry.cancelled`. Only providers holding a draft, sent or expired quote are told, by `quote.cancelled_inquiry`, which is critical with a first-attempt target of 5 minutes, retried under the FR-030 retry rule; the reason stays patient-private (REQ-020-076, REQ-020-020).
- A mandatory patient notice is sent by email when the patient has switched off every channel and always appears in the in-app list; a non-mandatory notice with no channel left is recorded as `suppressed` (Alternative Flow A1, User Story 1).
- The confirm variant of `provider.status_cancellation_patient` carries Confirm and Decline links to FR-003 Screen 8; a new mandatory reminder row `provider.status_redistribution_reminder` is sent once at 48 hours (REQ-020-013, REQ-020-159).
- New mirror rows: account deletion requested, the five data request patient notices, deadline approaching, obligation block ended; installment failed, overdue and plan defaulted; legal version published, coverage below threshold and acceptance reminder. An Admin recipient may be defined by a held permission (REQ-020-160 to REQ-020-169, REQ-020-046).
- `booking.cancelled` lists its causes (Admin cancellation, patient drop-out, unpaid balance or installment plan default, provider fault) with the FR-006 reason text (REQ-020-092).
- Delivery audit: one record per recipient and event with one attempt row per channel attempt; attempt status is an enum (queued, sent, delivered, failed, suppressed, deferred, coalesced); a suppressed, deferred or coalesced notice is an attempt row with that status (REQ-020-041, REQ-020-042).
- Retry: "backoff" and "failover" replaced by the FR-030 retry rule (up to 3 retries, 1 hour apart by default) in Alternative Flow B2 and the Implementation Notes (REQ-020-040, REQ-020-043).
- The 90-day window covers the provider and admin lists; an archived notice leaves the lists and its deep link opens the list with a "no longer available" message (REQ-020-068).
- Affiliate notices go by email only, with no preference setting (REQ-020-027, REQ-020-104, REQ-020-105).
- Flow steps A1, B1 and B2 rejoin the main flow; the post-MVP SMS sentence moved into Main Flow step 3 (REQ-020-037).

## Graph change-set (prepared, not applied)

- 120 operations (204 change rows): 12 new Rule nodes (REQ-020-158 to REQ-020-169), 1 new field (`ENT-notification-attempt.notification_id`), the attempt status turned into an enum with 7 values, the `affiliate` recipient type, 22 node updates (15 rules, 4 steps, 3 entity and field descriptions), 7 edges removed and 69 added (new rows, step `next` edges, stage moves).
- The 5 notification entity read and write edges at STG-main-01-inquiry moved to STG-platform-01-all-stages.
- Applied to a scratch copy: whole-graph lint stays at 29 findings (L03 1, L09 1, L12 6, L17 12, L18 9); no FR-020 finding was added.

## Cross-FR rows queued

FR-030 (catalogue rows, rules, delivery log as a view of the attempt rows, `affiliate` values, retry and critical-rule alignment), FR-003, FR-001, FR-023, FR-027, FR-007B and FR-006; see the pass 1 section of `plans/reports/logic-review-ledger.md`.
