# FR-013 Logic Review Pass 1 (2026-11-24)

**Scope**: FR-013 Reviews & Ratings, PRD v1.17 to v1.18. Pass 1 of the logic review; 23 findings: none rejected, 3 owned by neighbour FRs and only queued (P1-18, P1-20, P1-21), 20 fixed on the FR-013 side (P1-08 and P1-19 also queue neighbour rows).
**Evidence**: reviewer report `plans/reports/tester-261124-fr013-logic-p1.md`; fixer report `plans/reports/docs-manager-261124-fr013-logic-p1-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr013-logic-p1-fixes.yaml` is prepared and NOT applied (the controller applies it).
**Owner defaults**: numbers 108 to 113 as ruled by the controller for this pass (seeded reviews count and any visibility or rating change recalculates; one review per case and no restore; takedown limits; deadline bounds and Overdue; full-name option removed; invitation on the eligibility date); the owner-review defaults report is the controller's to update.

## Changes to the PRD

- A Flagged review counts as Published for visibility, patient Edit and Request Takedown, and provider Respond; the status value is unchanged (REQ-013-042, -057, -059, -079).
- Flag lifecycle: the system sets Flagged and queues; the admin resolves on Screen 8 with uphold (back to Published, flag reason cleared), redact or unpublish (B2, Screen 8 Resolve flag row).
- New workflows A5 (admin removes a review) and B3 (admin removes a provider response), each with a Screen 8 action; Respond returns after a response removal.
- Every change of a review's visibility or rating recalculates the aggregates and invalidates the cache; seeded reviews count in the average and distribution (REQ-013-031, -023, -008, -035).
- One published review per treatment case: one further review after a removal, whether an approved takedown (existing rule kept) or an admin policy removal (new), no Restore (REQ-013-002, -016). Provider Screen 5 loses its patient and case filters and gains an alias search (P1-17).
- Takedown limits: one Pending request, one further request after a rejection, no edit while Pending, an admin removal closes a Pending request as Approved (REQ-013-043, -042, -030).
- Takedown deadline 12 hours to 7 days, default 48 hours; a breach shows Overdue on Screen 9 and notifies admins, with no automatic decision (REQ-013-078, -069).
- Notice list extended (REQ-013-017): edited by the patient (provider, informational only), edited by an admin (patient), takedown requested, takedown overdue; notices to a placeholder patient are not sent (REQ-013-077).
- Respond requires an active provider account and no active response (REQ-013-057); Screen 5 shows No response after a removal.
- Audit actor type and id for patient and provider actions; admin add form gains provider, treatment, ratings, text, review date and a required reason; admin edits set the Edited marker and notify the patient; a patient edit is compared with the last admin redaction.
- Reviewer display policy removed: the alias is always shown (REQ-013-014, -022, -052, -070; Screen 10 row removed).
- The invitation fires on the eligibility date and reminders count from it (Entry Points, REQ-013-024, -017); Screen 10 keeps one reminder link-out. Screen 4 photo wording is photos attached to a published review.

## Graph change-set (prepared, not applied)

- 145 operations: 11 nodes added (2 flows, 9 steps), 2 fields and 5 enum values added, 9 edges removed, 36 node updates (26 rules), 2 nodes retired (the display-policy setting and field), 80 edges added.
- Wiring: next edges to retired STP-013-002 and -054 removed; STP-013-005 gets an on edge to Screen 1 and a next to STP-013-061 on a flag match; STP-013-062 branches to uphold, redact (STP-013-021) and unpublish (STP-013-071); the two new flows start at STP-013-071 and -081.
- Applied to a scratch copy of the db (207 change rows, no error after two duplicate edges were dropped), then the copy was deleted. Every active non-start FR-013 step has an incoming next from an active step and no next points to a retired node. lint.py was not run (the controller lints after applying).

## Cross-FR rows queued

FR-032 (Tab 5 embeds or links Screens 5 and 6), FR-006 (REQ-006-060 Completed without final review), FR-031 (REQ-031-106 permissions for the FR-013 admin actions), FR-020 and FR-030 (catalogue rows for the four notices; invitation on the eligibility date and reminders counted from it). The rows are in the logic-review ledger section for FR-013 pass 1.
