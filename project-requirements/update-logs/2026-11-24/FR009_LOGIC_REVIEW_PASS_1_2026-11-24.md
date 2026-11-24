# FR-009 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 1.11 to 1.12, with a graph change-set)
**Scope**: FR-009 Provider Team & Role Management
**Source of findings**: `plans/reports/tester-261124-fr009-logic-p1.md` (16 findings; each ruled fix, neighbour-only or settled by the PRD)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md`

- **Who may remove or suspend**: the Owner removes or suspends any non-Owner member; a Manager only Clinical Staff and Billing Staff. The same limit applies to cancelling an invitation. The force-remove line no longer says it bypasses an "Owner-only" rule (REQ-009-005, REQ-009-162, REQ-009-192, REQ-009-193).
- **Work belongs to the clinic**: inquiries, bookings and messages belong to the clinic; a named person is only the responsible clinician on quotes and treatment records and on appointments. Removal lists draft quotes, treatment records and appointments and asks for a replacement clinician. "Inquiries assigned" and unread-message counts are gone from the workload summary, Screens 4 to 6, 9 and 11 (new Rule 12, REQ-009-191, REQ-009-067, REQ-009-070, REQ-009-099).
- **Removal and conversations**: B6 now only states that clinic conversations are unchanged by a removal; no message routing and no automated patient message (REQ-009-077).
- **Suspend and Reactivate**: actions on Screens 1 and 6, a short flow (A9), and the Manager limit; a suspension records who set it (clinic or platform) in the new field `suspended_by`, and a platform suspension can be lifted only by a Hairline admin; admin rows on Screens 10 to 12 gain Reactivate (new Rule 13, REQ-009-192, REQ-009-082, REQ-009-090, REQ-009-107).
- **Owner row**: Force suspend and Force remove are not offered on the Owner row; the admin uses the Owner handover first (REQ-009-161, REQ-009-162).
- **Owner handover**: "Hand over Owner role" button and dialog on Screen 12 and a three-step admin flow; the provider's Owner login email follows the new Owner; the Owner's onboarding records are stated (REQ-009-174, REQ-009-196).
- **Invitations**: expiry is always 7 days and the admin setting is removed (REQ-009-016, REQ-009-160); seat check on resend (A2, REQ-009-048); Screen 7 check worded as "still Pending and its seat is held" (REQ-009-043); Cancel Invitation flow (A8, REQ-009-193); admin "reset invitation" is the A2 resend (REQ-009-117, REQ-009-145); bounce text says to cancel and invite again (REQ-009-168); First Name and Last Name on the admin invite form (Screen 12).
- **Provider status**: a Deactivated provider cancels all Pending invitations; Screen 7 shows "This invitation is no longer valid." for a Deactivated provider and "This clinic is temporarily unavailable" for a Suspended one (new Rule 14, REQ-009-194, REQ-009-195).
- **Account deletion**: through support (FR-034); a Hairline admin removes the account (status Removed) and anonymizes personal data; audit entries keep an anonymous label for the existing retention period; an Owner hands over first (REQ-009-159, REQ-009-165).
- **Wording**: Manager access is "within the Manager permissions defined in FR-031" (REQ-009-037); the notices need FR-030 catalogue entries (REQ-009-007); Dependencies now name FR-030 and FR-012.
- The header, change log row and Last Updated all say version 1.12 (they had disagreed).

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr009-logic-p1-fixes.yaml`

- New: rules REQ-009-191 to REQ-009-196; flows FLW-009-cancel-invitation, FLW-009-suspend-reactivate-member, FLW-009-owner-handover; steps STP-009-074 to STP-009-081; field ENT-team-member.suspended_by with values clinic and platform.
- Rule statements and step titles updated to mirror the PRD (28 rules, 6 steps); field and flow descriptions updated.
- Retired: steps STP-009-012, 071, 072, 073; event EVT-team-patient-handler-changed; fields ENT-team-member.active_inquiries_count and unread_messages_count; setting SET-invitation-expiry-period (no other FR governs or reads them).
- Edges: STP-009-009 now goes to the new seat check STP-009-074, which goes on to STP-009-025; six shows edges and nine other edges to retired nodes removed; four shows edges added.
- Cross-FR edges: REQ-009-191 applies to ENT-quote.clinician_ids (FR-004) and ENT-treatment-record.clinician_ids (FR-010); REQ-009-196 applies to ENT-provider.email (FR-015). No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 255 change rows, no errors; every FR-009 step stays reachable; the copy was deleted.

## Not changed here

Neighbour changes for FR-031 (Owner-only removal row), FR-004 and FR-010 (clinician lists on records), FR-015 (Owner records, login email, deactivation cascade), FR-030 and FR-020 (catalogue rows for the team notices) and FR-032 (REQ-032-089 wording) are queued in the logic review ledger section for FR-009, not applied. Stage pinning of FR-009 rules and steps, FR-024 role gating, B4 ordering, the invitation rate limit scope and the Accepted/Active wording are left as they are.
