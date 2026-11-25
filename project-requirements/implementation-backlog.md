# Implementation-phase backlog

Last cleaned: 2026-11-25.

This file lists the points that are still open after the clean-up of 2026-11-25. The earlier list held 507 points. Each was checked against the live PRDs and the requirements graph: 264 were already settled, 125 were filing or wording fixes and have been applied in the PRDs and the graph, and the rest are below. None of them blocks the baseline.

The `[Bnnn]` tag on each point is its line number in the earlier list. The Product Owner question list and the working records use the same tags. References such as `[L415]` and `plans/reports/...` point to working records kept outside this repository; ask the Product Owner if one is needed.

| Section | Who settles it |
|---|---|
| 1. Waiting for a Product Owner decision | Product Owner. Build to the PRD as written until the decision is recorded. |
| 2. Developer matters | Development team, during implementation. |
| 3. Fixes owed in another FR document | Documentation owner. |
| 4. Housekeeping of the requirements graph and documents | Documentation owner. |

## 1. Waiting for a Product Owner decision

Each point is a business choice nobody has made yet. Nothing in the requirements was changed for these points. Do not guess the answer: where a point touches what you are building, ask the Product Owner.

### FR-001

- [B10] Notes (not bullet counts): (1) L447 gives the entry flow as splash, explanation screens, "Get Started" then registration; it does not say whether the existing Landing Screen (Screen 2) stays between the explanation screens and "Get Started". The PRD keeps Screen 2 after the explanation screens, so "Get Started" and the login link stay there; confirm with the owner. (2) L447 does not name the four services or the Service Selection screen's wording; Screen 8a refers to "the four Hairline services" without naming them. (3) L429 leaves open how a Locked patient returns to Active (after the lockout period or admin unlock); the PRD states the four values only. (4) L394 added city and age to the Patient entity as ruled, but no FR-001 screen collects city, and age is derived from date of birth; confirm the intended source. (5) L1747: the FR-020 Rule id is not fixed in the ledger, so the PRD pointer names FR-020 only.
- [B686] A successful password reset on a never-verified email does not mark the email verified.
- [B687] An admin email change is not among the session-ending events of REQ-001-182.
- [B688] STP-001-003 hands off to STP-027-011: confirm in FR-027 that it is the same prompt as the Screen 3 checkbox.
- [B690] B3 gives no order between a Locked account and an unverified email.
- [B691] The Screen 5 Help entry is not shown after the wrong-code limit is reached.
- [B692] Four events have no reader: EVT-patient-account-locked, EVT-patient-password-changed, EVT-patient-profile-changed-by-admin, EVT-reauth-otp-sent.
- [B794] FR-001: confirm whether a password-changed or account-locked notice exists; FR-001 states none, so FR-030 added no row (ledger line 2198).

### FR-003

- [B21] [L515] REQ-003-015 stays; the name or number of the planned provider capacity management FR, and where planned FRs are recorded, were not given in the ledger. The PRD still says "Future FR: Provider Capacity Management" and "TBD".
- [B786] Line 2633 (FR-003): optional response-time column on the provider inquiry list. Not changed; new scope.
- [B787] Line 2652 (FR-003): same item as 2633. Not changed.

### FR-006

- [B43] [L1795] Emergency edit scope: whether it reaches beyond bookings ("any edit within the system") and how it relates to the appointment change are not ruled. The PRD states only what L1793 and L2175 settle: non-money booking details, mandatory reason, full before and after history, never sets status, payment records immutable, guarded actions keep their checks.

### FR-007

- [B443] **Late fee on a full refund** is not stated (REQ-007-063). Decide when payments are built.

### FR-007b

- [B57] Not a manifest bullet, for the controller: L339 leaves open when a postponement would break Stripe's 90-day limit on clinic balances; the PRD note does not cover it.

### FR-008

- [B63] [L621] Q-149 (validation limits as Rules?), Q-151 (passport-upload progress indicator; "declaring no travel does not block the procedure") and the display-strings half of Q-162 (Screens 10 and 12 contract or UI copy; also noted on L633) were folded into the FR-008 marking list owed under ruling A9. No ruling on the content exists, so no PRD text was written. The marking list for the owner is still owed.
- [B604] Screen 6 status badges still read Awaiting for items when the patient has declared no travel (the declaration shows on Screen 10 only).
- [B605] Who is asked again for the early-departure acknowledgment after a reschedule is not ruled (the PRD says "asked again").
- [B606] Carry-over when the replacement booking includes different services on the same path is not ruled.
- [B607] Pass 1 leftovers stay: reversing a Not-needed mark, Overall Status of a closed TravelContext, Path A one-way flight, STP-006-208 next edge, early-departure warning with a Not-needed return flight.

### FR-009

- [B836] Line 1188 (FR-009): provider email-delivery-issue indicator. A new flag field on the team member (the Owner is a team member) and a display on FR-009 Screens 6 and 11 and the FR-015 provider detail would be new design; REQ-030-156 already states the rule for any account type.

### FR-010

- [B77] [L496] Renumbering FR-010 requirement ids "in order" is not applied. The ruling's follow-ups are still owed (old-to-new map shown to the owner first, whether graph node ids change, which outside places are updated), and the cross-FR citations written in this round (L2039 to L2089, FR-011 and FR-014 lines) still use the current ids. The PRD inline ids keep their current numbers (gaps remain, for example no REQ-010-005); new ids continue from REQ-010-106 (graph highest was REQ-010-105).

### FR-011

- [B85] [L702] Q-33 check done by direct query. Aftercare assignee history exists: ENT-aftercare-audit-entry.previous_assignee_id and new_assignee_id (shown on SCR-011-19), plus ENT-aftercare-plan.assigned_team_member_id. The support-request-to-booking link is one-way only: ENT-booking.support_ticket_reference (FR-006) exists, but ENT-support-case (FR-034) has no booking reference Field, and no edge joins the two. For the owner: is the one-way booking reference enough?
- [B729] Screen 1 has no stated entry to Screen 7 for Cancel Subscription.
- [B766] FR-011: optional, name the FR-031 permission each admin Screen 13 to 19 action needs (View Aftercare Cases, Manage Aftercare), as FR-031 now only names the screens.
- [B799] FR-011: `aftercare.completed` produces no notification; if a completion notice is wanted, FR-011 must state it and FR-030 then adds the row.

### FR-012

- [B563] SET-escalation-routing-rules has no consumer: nothing records who receives the keyword alert and the 72-hour flag (P2-11).
- [B565] SET-emergency-intervention-permissions is queued for FR-031 (P2-11).
- [B567] A session that is open when a conversation turns read-only is not described; the session simply cannot be started on a read-only conversation (P2-08).

### FR-014

- [B880] FR-014: Widget 8 and Screen 4 Period column should show a release date for a Stripe Connect payout (ledger line 2859).

### FR-015

- [B109] [L802 OPEN] `availability_status` meaning is owed; provider phone/email versus public phone/contact email carried from Q-91 and never asked. Attribute added by name only.
- [B110] [L1662 OPEN] No Rule says the admin-support alert deep-links to the Admin Support Required filter; no ruling, no PRD text.
- [B650] The provider status event requires `admin_id`, but a scheduled change applied by the midnight job has no acting admin.
- [B654] The Screen 4 affected list shows no count of monitoring cases ended by the cascade.

### FR-016

- [B118] Residual open points inside applied bullets (not counted above): [L831] which document types a patient uploads besides photos (settled 2026-11-22: PDF and image files only, at most 5); [L836] free text or templates, and which channels, for manual notifications, and Screen 7 has no action type for a manual notification; [L834] Screen 7 has no action type for a medical data edit (Medical Data Access and Admin Note exist); [L429] return path from Locked after the lockout period or an admin unlock; [L583] the new Ticket Source value names are defined in FR-034.
- [B342] Patient additional documents (owner answer 6: PDF and image files, up to 5 more): the rule sits on the admin screen only (FR-016 Screen 4, REQ-016-216). No patient-facing PRD yet says on which screen the patient uploads them; recommended home is the patient profile (FR-001). Needs a PRD line before development.
- [B611] The Overview tab has no separate bookings panel or booking-status field in the PRD or graph; the "Cancellation failed" mark is stated on the patient's Overview tab without adding a field or screen. A field for it is a design step for a later change.
- [B612] The Screen 8 default filter shows only Pending Admin Review, so Verification Required and Denied requests are visible only after the filter changes.
- [B615] The Operational and Security Rules line says failed refunds are retried automatically; FR-007 was not checked for the same rule.

### FR-017

- [B715] Commission on the clinic's share of a cancellation fee is not stated: REQ-017-200 does not say whether Hairline commission is taken from the share.
- [B716] No admin control raises the payout flag of REQ-017-161; only the system flags a payout over 2x the clinic's average.
- [B717] Not stated whether Mark as Paid is blocked while a statement is flagged Manual Review Required (Approve and retry are).
- [B720] ENT-provider-earning.payout_status has no value for a held earning or for Waiting for clinic setup.
- [B721] REQ-017-123 provider payout history omits Waiting for clinic setup.

### FR-018

- [B675] Screen 2 Edit and Screen 3.2 have no status condition, so an Inactive affiliate's commission and bank details appear editable.
- [B679] "Real-time" on dashboards sits beside a 5-minute refresh; receipt availability is Paid-only on the affiliate side and unconditional on Screen 8.

### FR-019

- [B137] [L881 Q-152] Where the admin sets the ROI bands: not ruled. PRD says the bands are admin-defined only; no Setting named.
- [B573] A 100 percent percentage discount (possible if the maximum-discount setting is raised) has the same zero-price issue as P2-04, which was ruled for fixed amounts only.

### FR-020

- [B503] Source: `plans/reports/tester-261124-fr020-logic-p2.md` finding P2-13; PRD `local-docs/project-requirements/functional-requirements/fr020-notifications-alerts/prd.md` v2.18.
- [B505] SMS path (post-MVP): define what makes a notice "urgent" (REQ-020-037, STP-020-005) and who sets `ENT-notification-record.urgency`, when SMS enters scope. Today the Urgency badge is display only (REQ-020-158).
- [B854] FR-020 line 766 (define urgent for the SMS gate): not changed, deferred to the backlog with SMS.

### FR-021

- [B580] Stale window and import size limit have no owner, screen or value.
- [B586] The free-text panel has no graph step; whether an Active right-to-left locale needs a rule against REQ-021-057 is open.

### FR-022

- [B746] FR-005 Screen 1 (REQ-022-069): the sort rule names Not Selected, Expired, Withdrawn and Cancelled as last; the owner State list also has Accepted and Superseded, whose position is not stated.
- [B747] FR-007 Screen 5 (REQ-022-091): Date Range says "Filters by booking date"; FR-007 does not state its date filter, so it was not changed (the FR-006 table was aligned to Appointment Date).
- [B749] FR-033 lists: the owner describes an admin-only Archived filter used for restore; FR-022's default of All may show archived items in the live list. The owner gives no default.
- [B751] The hourly-limit decline (STP-022-052) has no stated user-visible message, unlike the timeout.

### FR-024

- [B175] Note, not a manifest bullet: L1035 "Setting ranges owed": only a lower bound (whole number of 1 or more) was drafted; no upper limit was invented.
- [B590] Base Price "required if offering" versus REQ-024-060.
- [B591] REQ-024-072 repeats the confirmation sentence, and the case of zero affected quotes is unclear.
- [B593] Renaming a treatment type versus its historical versions is not stated.
- [B596] Security review note: drafts do not count toward the hourly package creation limit (REQ-024-078, REQ-024-098), and no draft cap or draft expiry exists, so a provider could create unlimited drafts. Owner to decide whether to add a draft cap; logged with defaults 204 and 205.

### FR-028

- [B530] A4 and Screen 2 enable bulk update when at least one row is checked, but the flow selects one destination; with rows from several destinations "[Location]" in the confirmation is undefined. Fallback rows (several per currency) cannot be shown in a per-currency preview table.
- [B532] FR-029 says an Inactive or Archived Stripe account's holdings are "ignored for routing"; REQ-028-091 blocks while an account is "assigned" and does not say whether an inactive account still blocks.

### FR-029

- [B465] The account Default Currency has no consumer yet; confirm its use before building it.

### FR-030

- [B550] `aftercare.escalation_triggered` is a clinical red-flag alert that is now switchable and not locked; whether it should be locked is not decided.
- [B551] A held notice (quiet hours or rate limit) has no maximum age; a switchable time-sensitive notice such as `booking.appointment_reminder` or `quote.expiring_soon` can arrive after its moment. Skip If Too Late only acts at scheduling.
- [B552] Two appointment reminders (7 days and 1 day) need two timings for one event, but the overlap refusal and the single seeded Active rule per event do not obviously allow a second rule for the same recipient type and channel; how the second timing is configured is not stated.
- [B554] Event On or Off when rules are only Paused or Draft (no Active rule) is not covered.
- [B555] Escalation Wait Time has no minimum tied to the retry window (retries times interval).
- [B846] FR-030: add catalogue events for patient.suspended, patient.suspension_ended, patient.password_reset_by_admin, admin.manual_notice and admin.policy_warning (the first four mandatory), for password changed and account locked, and for a cancelled team invitation, then FR-020 follows through the pointer sentence.

### FR-031

- [B701] FR-026: the "Acknowledge role change" banner belongs to the admin shell; no dashboard screen node exists, so STP-031-214 and STP-031-215 have no screen.
- [B771] Lines 2603 and 2618 (FR-031, FR-026): the role-change banner has no owning screen node because the admin dashboard and shell are not specified in any FR; FR-031 states the banner on every admin page.

### FR-032

- [B226] [L1541] The per-FR marking list of screen-row requirements (Q-moved-14, ruling A9) is owed to the owner; the owner marks each FR-032 screen line there. No Rule added to FR-032 meanwhile.

### FR-034

- [B235] [L583] Q-115 "Extend the source list": the new Ticket Source values and the requests that use them are not recorded in the ledger or any readable file (the FR-009 result file reports the same). PRD still lists three sources (Patient App, Provider Portal, Manual Admin Entry).
- [B642] The Urgent threshold minimum of 1 hour equals the fixed 1-hour alert, so the alert and the escalation can fire together.
- [B644] Edit Case is enabled for all statuses, against the archive step for Closed cases; reopen templates may be deleted against "cannot delete while in use".

### FR-035

- [B311] Fields dropped with no replacement: the support-case auto-closure deadline (countdown on SCR-035-03 and SCR-035-04; the FR-035 PRD still shows it at lines 375 and 394, and it can be computed from `ENT-support-case-resolution.resolved_at` plus the auto-close period Setting, so no stored Field may be needed) and case type (Type column on SCR-032-16 and SCR-032-17; the FR-032 PRD still lists the column at lines 1443 and 1494 while FR-034 retired `ENT-support-case.case_type`: the two PRDs conflict and one must change).

### FR-037

- [B538] The assignment-ended notice on completion or conversion may duplicate the completed and converted notices; settle the final copy in technical design.
- [B539] Resuming a kept conversion draft rebuilds the carried-over values and may overwrite edits the patient already made in the draft.
- [B542] The provider is not told when an advice window opens.
- [B543] The PDF copy already attached to the inquiry is not refreshed after a later Admin correction.
- [B544] The active-inquiry check is not repeated when a kept draft is resumed (FR-003 refuses at submit).

### FR-038

- [B255] Note (not a bullet, no count): proposed wording for the monitoring.aftercare_conversion_started notice (L979, wording and timing owed) is in the PRD marked "to be confirmed in notification copy review"; the owner was not asked.

## 2. Developer matters

Technical or implementation choices. The requirements do not decide them and do not need to.

### FR-003

- [B20] [L496] Renumbering FR-003 requirement ids "in order": ledger 847 and 622 make renumbering a programme-wide final step with an old-to-new id table kept centrally, and the PRD cannot be renumbered alone without breaking citations in other PRDs. Ids in this PRD are left as they are; the PRD's Functional Requirements Summary is not in numeric order across its groups. Ledger answers on whether graph node ids change are still owed.

### FR-007b

- [B448] **Installment build items the PRD now requires:** pause later installments on a Defaulted plan; one void step that also handles a charge already in flight; a second-approval record for Mark as Resolved (bank transfer with amount, date, reference); plan snapshot columns for late fee, grace period and cancellation point; a once-only catch-up charge for paused past-due installments when the plan returns to Active; cancel pending retries on a hard decline.
- [B449] **Known approximation:** the single void step (STP-007B-701) serves the B2, B4 and B8 cases, so the provider notice after it is reachable from all three. Check when the flow is built.

### FR-008

- [B600] 18 FR-008 rules still have no step: REQ-008-029, -035 to -039 (future phase), -040, -041, -043, -045, -063, -068, -070, -075, -077, -078, -079, -082. The tester counted 25; the recount gives 24 before this pass (REQ-008-083 was already attached) and 18 after it. The rest need a step that does not exist; none was invented.
- [B603] No step carries the hand-off at Completed (provider passport access ends); it is stated as a rule only.

### FR-009

- [B624] A6 self-removal by the Owner can only be reached through the API (the Owner row has no Remove button).
- [B626] FR-009 rules and steps stay pinned to the active-provider stage, except those on the configuration and offboarded stages (accepted early-stage leftover).

### FR-010

- [B358] **Records described twice (merge during compression):** medication instructions (FR-010) and the medication field on the Treatment Record; discount code (FR-019) and promotion program or code; currency config (FR-021) and currency conversion settings (FR-029); notification attempt (FR-020) and notification delivery log (FR-030); provider Fields location and country, specialties and specialty, total procedures and completed procedures count. `ENT-provider.active_patients` does not say what "active" means.

### FR-011

- [B731] STP-011-062, STP-011-001 and REQ-011-014 stay pinned on the early platform stage STG-main-07-aftercare.

### FR-012

- [B95] [L385] Move list for FR-012 Events is owed (see Graph changes).
- [B359] **System-check Steps left in the flows:** STP-012-012 (starts a flow and has two exits) and the Steps marked mixed or borderline in the reports (they also record or decide something). Rewrite each as its action when the PRD is compressed.

### FR-014

- [B103] [L496] Renumbering of FR-014 Rule ids ("Renumber and update citations") not applied. Ledger L847 (Q-109) sets renumbering at the final apply across all FRs with an old-to-new table, and the old-to-new map owed in L496 does not exist yet. Renumbering FR-014 alone would break citations in other PRDs, the graph and reports.

### FR-015

- [B656] Stage pinning of the closure-request steps (STP-015-171, 172, 176) is an accepted early-stage leftover.

### FR-016

- [B117] [L847] Q-109 renumbering without gaps: the ledger says it is done at the final apply for all FRs, in the graph and the new PRD package, with an old-to-new table. A per-FR renumber now would break the REQ-016 ids that other FRs cite (for example REQ-016-028 and REQ-016-058). Inline ids REQ-016-001 to REQ-016-032 are kept; REQ-016-018 stays a gap.

### FR-018

- [B680] FR-017 and FR-018 show different code status sets; no graph field holds the stored initial code settings.

### FR-021

- [B579] Group-scoped partial bundles versus the singular "latest published bundle" (Rule 14, REQ-021-059); revalidation trigger and polling interval undefined (REQ-021-113).
- [B581] Translation key status is key-level while statuses are per locale; translation value and version status fields are free text.

### FR-022

- [B156] Technical lines outside the lines named in L1002 remain in the PRD (Future Enhancement P3 Elasticsearch/Algolia, Technical Considerations bullets on indexing, query builder, pagination and caching, Assumption 3 on full-text support, Data Dependencies Entity 3 migration scripts, Key Entities Database Index, Rule 2 and Performance Rule 2 wording on database indexes). Not removed because the ruling named specific lines and L982 keeps the Database Index text.
- [B293] Technical requirement rows kept: REQ-022-021 (JWT for search endpoints), REQ-022-024 (SQL injection and XSS sanitising), REQ-022-028 (create database indexes), REQ-022-029 (cache autocomplete 5 minutes), REQ-022-032 (database queries under 100ms), Performance Rule 2 (database indexes) and Performance Rule 4 (autocomplete cache). They are numbered requirements, not leftover notes, and L1002 does not name them; removing them is a scope decision for the controller.
- [B750] REQ-022-123 applies at the patient and provider stages and not at STG-admin-02-operations, although it is an admin screen; REQ-022-145 follows the same early-stage pinning as its neighbour REQ-022-113 (accepted leftover from pass 1).

### FR-023

- [B165] [L272] OPEN: the conflict between REQ-005-060 (no hard deletes, scope global per Q-fr001-009-96) and REQ-023-013 ("purge search indexes and caches") is not closed by a later ruling for REQ-023-013. REQ-023-013 wording left unchanged; the 10-year Rule already forbids hard deletion of the protected records.
- [B166] [L555] OPEN: follow-up owed to the owner on how the purge rule (REQ-023-013) changes under "Whole platform"; L893 and L1028 list REQ-023-013 as affected but record no ruling on the new wording. Same item as above.

### FR-026

- [B664] Retired validation steps keep their own outgoing `next` edges in the graph.

### FR-028

- [B533] Schema note for the P2-08 fix: ENT-pricing-default holds one record per destination default currency and one system-wide record, told apart by default_type; a split into two entities is possible if the data model owner prefers.

### FR-030

- [B356] **Notification catalog:** 13 Events that send notifications are missing from the FR-030 catalog (8 owned by FR-009, 5 by FR-017; ids in the FR-030 report). Add catalog rows to the FR-030 PRD, then move the Events to FR-030. Notification Steps in FR-012, FR-019 and FR-024 are not linked to an FR-030 flow.
- [B553] `ENT-notification-delivery-log` and its fields stay in the graph; its status values (sent, delivered, failed and so on) differ from the FR-020 attempt statuses and need a mapping.
- [B557] Not checked in this pass: manifest sections other than Flows, template variable allowlists, REQ-030-003 and REQ-030-004 against the FR-020 first-attempt target.

### FR-034

- [B643] The per-provider-user throttle (REQ-034-176) has no submitter-user field on ENT-support-case; only provider_id is stored.

### FR-037

- [B541] The routing rule's "withdrawn or not eligible" case overlaps "no provider assigned".
- [B545] Events are emitted by stage nodes, so no step shows which event it sends.

## 3. Fixes owed in another FR document

The answer is already written; the edit belongs in a different FR document from the one that raised the point.

### FR-001

- [B318] Display-only Screens with no Step on them (lint L03, 6 findings): `SCR-001-20` (splash), `SCR-001-21` (explanation), `SCR-001-24` (settings main), `SCR-001-25` (privacy and security menu), `SCR-001-26` (password changed confirmation), `SCR-026-14` (platform settings editor). The owner's marker ruling requires a marked Screen to be used by a Step; the flows that pass through these Screens need a Step linked `on` each.

### FR-009

- [B798] FR-009: the patient handler-changed notice and the compliance-flag notice to the admin compliance team have no catalogue row; FR-009 sends no notice for Cancel Invitation.

### FR-017

- [B797] FR-017: its other billing notices (statements ready, overdue payout alert, outstanding invoice alert, payout schedule updated, manual payment reminder) have no catalogue row; FR-017 states no notice for a voided Approved statement or for Waiting for clinic setup.

## 4. Housekeeping of the requirements graph and documents

Clean-up work on the documents and the graph themselves. None of it changes what the product does.

- [B263] Events with no key and keys with no Event (H3-25) remain open (No later bullet closes it.)
- [B264] Twelve misplaced passages in eleven PRDs, to be asked one by one at the compression phase (Ruled "ask me for each one"; each needs a proposed place first.)
- [B265] List of variant names for the same clinic role or actor, owed to the owner (Owner note: "please also fix the wording to make sure they point to the same thing, not so many different things in the system". The Actor merge (bullet 50) does not replace the list.)
- [B266] Vocabulary list entry: graph `uploaded_by` versus PRD `uploader_type` (No later bullet closes it.)
- [B267] Cross-FR items Q-fr010-019-3, 18, 41, 72, 74, 98, 101, 114, 115, 133 wait for prepared lists (No later bullet closes it.)
- [B268] Same business and technical mix in the stored-data lists of other FRs (Facts to gather first.)
- [B271] Q-fund-release-11: Stripe facts STR-1 to STR-6 (Owner selected no option and asked to use Stripe public documentation and the brief. Controller's reading: record STR-1 to STR-6 once as "not confirmed with Stripe".)
- [B273] Q-fund-release-24: currency of a payment amount (Owner selected no option; quoted note: "Then that amount is exchanged into the other currency as per the exchange rate config". Controller's reading: one base-currency amount converted with the exchange-rate configuration.)
- [B274] Row B32 stays open (C54 is closed by the provider payout timeline) ("B32 and C54 stay open"; C54 is resolved by [T118], B32 is not closed in this slice.)
- [B275] Other items for the owner of the work, not counted: the 10-year retention period has no legal document behind it (the owner was told no document confirms 7 or 10 years); other system PRD text still says "escrow" in the overview, the payment dependency lines and the glossary, and was left because it is consistent with the locked-balance flow.
- [B321] 63 Sources are still "pending review" and cited by nothing; the list is in `plans/reports/docs-manager-261120-2140-pending-sources.md`.
- [B330] Steps that only say the system checks or validates something are still in the graph (ids in section 7 of each `plans/reports/tester-261121-frNNN-completeness-recheck.md`). The owner dropped such Steps; retiring them needs each flow re-linked, to be done with the Phase 8 stitching.
- [B335] 94 Sources are cited by nothing, and 395 Rule rationales cite a PRD line that the line-refresh script could not confirm by text match (the list was a working file of the 2026-11-21 session and was not kept; re-run the text-match check before acting on it).
- [B393] Several FRs: the Dependencies FR list differs from the graph's cross-FR edges (verify-fr check 3 will flag these).
- [B866] Stage graph (controller, shared nodes): the join from the aftercare stage to monitoring conversion (ledger lines 686, 691, 803) has no owning FR.
