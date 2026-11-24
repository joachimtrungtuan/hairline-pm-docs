# FR-012 Logic Review, Pass 2 (final) - 2026-11-24

**Scope**: FR-012 Messaging and Communication, PRD v2.16 to v2.17. Thirteen findings from the adversarial second pass plus two minor observations, applied under the owner's triage rulings. The graph change-set is written but not applied to the live graph.

**Files changed**

- `local-docs/project-requirements/functional-requirements/fr012-secure-messaging/prd.md` (v2.17, one new change-log row)
- `local-docs/project-requirements/graph/changesets/2026-11-24-fr012-logic-p2-fixes.yaml` (new; test-applied on a scratch copy of the graph, 93 change rows, copy deleted)

**What changed in the requirements**

- Notices: the intervention notice and the admin keyword alert are always delivered; the service rule applies to the rest (REQ-012-026).
- Emergency intervention: the reason is recorded with the intervention message; the "enabled" audit entry has no reason and is written even if the session is cancelled (REQ-012-101). Only one session can be open per conversation; Resolve Flag is disabled for a flag under intervention (REQ-012-085). The conversation shows Escalated while a session is open, with or without a flag (REQ-012-109).
- Response timers: a provider reply closes the system no-response flag automatically; the 48-hour reminder is sent once per unanswered stretch; the clock stops while the conversation is read-only and restarts from the next unanswered patient message (REQ-012-098).
- Read-only conversations: composer, attach control and call buttons are disabled with a banner giving the reason; Enable Emergency Intervention is not available (REQ-012-018, Screens 2, 4, 6A).
- Screen 4 flag indicator covers an open flag of any type; Screen 5 shows an intervention success rate worked out when read (REQ-012-089).
- Calls: ENT-message gets call_type, call_started_at, call_duration_seconds and call_outcome (answered, missed, declined, failed); call entries are shown in the thread but are not unread messages, the last-message preview, or part of the monthly conversations-with-a-message figure (REQ-012-032, REQ-012-033, REQ-012-024).
- Moderation settings: Save control on Screen 5, defaults set (switch on, keyword list empty), new audit event type for a setting change, keyword list filled by the admin team before go-live (REQ-012-010, REQ-012-023, REQ-012-105).
- Clinic team: "You" only on the viewer's own messages and the colleague's name on others; one unread count per clinic (REQ-012-001, REQ-012-060, REQ-012-055).
- Minor: "support audit export" removed from REQ-012-020; SCR-012-03 linked to REQ-012-028.

**Graph (change-set only)**: 4 fields, 24 node updates, 7 enum values, 22 edges. No cross-FR edges and no nodes owned by another FR were touched.

**Leftovers**: supply the starting keyword list before go-live; SET-escalation-routing-rules has no consumer; SET-conversation-export-controls is future phase; SET-emergency-intervention-permissions is queued for FR-031; STP-012-033 stays retired with its dangling edge; audit term drift and steps pinned at STG-main-02-quote.

**Queued for neighbour FRs**: FR-020 (exempt the intervention notice and keyword alert from holding), FR-030 (reminder once per unanswered stretch, not while read-only), FR-009 (colleague name and one unread count per clinic).
