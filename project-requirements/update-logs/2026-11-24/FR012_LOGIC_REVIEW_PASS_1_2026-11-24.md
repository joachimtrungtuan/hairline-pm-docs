# FR-012 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 2.15 to 2.16, with a graph change-set)
**Scope**: FR-012 Secure Messaging
**Source of findings**: `plans/reports/tester-261124-fr012-logic-p1.md` (21 findings; each ruled fix, partly fixed, neighbour-only or rejected)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr012-secure-messaging/prd.md`

- **Conversation status and escalation**: status is calculated from the flags (Active, Escalated, Resolved); enabling emergency intervention on Screen 6B is the step that sets the flags to escalated_to_intervention; cancelling does not change them (REQ-012-109, REQ-012-085).
- **Intervention monitoring**: success means no new flag in the 30 days after an intervention; the post-intervention flag is a system flag (category Follow-Up Needed) controlled by a switch, default on; under 5% is a monitoring target on Screen 5 that blocks nothing (REQ-012-089, REQ-012-024).
- **Provider response timers**: the 48-hour clock starts at the patient's oldest unanswered message and stops at any provider reply; the 72-hour flag is a system flag; the follow-up queue is Screen 5 filtered by Follow-Up Needed (REQ-012-098).
- **Notices**: the intervention notice and the admin keyword alert cannot be switched off or held; other chat notices follow user settings (REQ-012-007).
- **Translation**: the reader's switch works only while the platform-wide switch (FR-021) is on (REQ-012-108).
- **Provider masking**: the sender label, avatar and search use the masked identifier until payment; View patient profile is hidden until then.
- **Deletion and retention**: messages and attachments are anonymised in place per FR-023 and kept for the retention period; admin emergency messages are kept (REQ-012-100, REQ-012-020).
- **Lifecycle and clinic-level conversation**: the conversation is open while the pair has a live quote, booking or aftercare, becomes read-only otherwise and opens again on a new quote (REQ-012-018); one conversation per patient and clinic (REQ-012-001).
- **Moderation settings**: emergency reasons are a fixed list; the keyword list and the post-intervention switch are edited in a Moderation settings group on Screen 5 (REQ-012-105).
- **Attachments and calls**: validation and malware scan run on every attachment from a patient, provider or admin, and a refused file does not block the message; calls start from the chat header and leave a system entry in the conversation, and call content is not recorded or monitored (REQ-012-009, REQ-012-040, REQ-012-044, REQ-012-032).
- **Audit**: the audit event list is stated; the reason is recorded when an admin enables emergency intervention (REQ-012-010, REQ-012-023, REQ-012-101).
- **Clean-up**: the undefined "admin-patient communications" reference removed in four places; "medical team" replaced by the on-call Admin (REQ-012-092).
- Dependencies now include FR-021 (REQ-021-119) and FR-023 (REQ-023-044).

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr012-logic-p1-fixes.yaml`

- New: steps STP-012-038 to -041, flows FLW-012-call and FLW-012-moderation-settings.
- Rule statements and titles updated to mirror the PRD (25 rules); step titles and prd_ref values updated for the attachment and escalation steps.
- Enum values added: ENT-flag.flag_type system; ENT-message.sender_type system; five audit event types.
- Removed: the dangling next edge of retired STP-012-011; SET-emergency-reason-options retired.
- Cross-FR edge: FR-012 references REQ-023-044.
- Test-applied on a scratch copy of the graph: 133 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour FR changes (FR-020, FR-030, FR-005, FR-031, FR-016, FR-004, FR-015, FR-011, FR-009, FR-023, FR-022, FR-001) are queued in the logic review ledger section for FR-012, not applied. Leftovers for the implementation backlog are listed there too.
