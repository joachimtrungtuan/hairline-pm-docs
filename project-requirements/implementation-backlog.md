# Implementation-phase backlog (requirements graph programme, 2026-11-20)

> Copied into the docs repository on 2026-11-25 so developers can read it. Report files it cites as `plans/reports/...` are working records kept outside this repository; ask the product owner if one is needed.

Points the owner rulings leave open, collected from the per-document apply results. None blocks the new baseline. They are not owner questions for this programme: each is to be settled when the feature is implemented or next revised. Source: the Backlog section of each `apply-result-261120-*.md` file; `[L..]` is the ledger line in `plans/261108-1040-requirements-graph-programme/overnight-run-261110.md`.

## FR-001

- [L415] Q-fr001-009-13 (D-B10, pairs P15, P19, P54, P71, "Decide each pair"): no closing ruling for FR-001 in the manifest; nothing decided here.
- Notes (not bullet counts): (1) L447 gives the entry flow as splash, explanation screens, "Get Started" then registration; it does not say whether the existing Landing Screen (Screen 2) stays between the explanation screens and "Get Started". The PRD keeps Screen 2 after the explanation screens, so "Get Started" and the login link stay there; confirm with the owner. (2) L447 does not name the four services or the Service Selection screen's wording; Screen 8a refers to "the four Hairline services" without naming them. (3) L429 leaves open how a Locked patient returns to Active (after the lockout period or admin unlock); the PRD states the four values only. (4) L394 added city and age to the Patient entity as ruled, but no FR-001 screen collects city, and age is derived from date of birth; confirm the intended source. (5) L1747: the FR-020 Rule id is not fixed in the ledger, so the PRD pointer names FR-020 only.

## FR-002

- [L507] Still open, no later closing line found: which of the five FR-002 media policy Settings remain (Q-fr001-009-37). Not decided: the photo limits (5 photos, JPG/PNG, 2 MB) are applied; the viewpoint requirement follows L1436; quality-check thresholds (Media Rules 4) and video duration (Media Rules 5) were left as "policy" in the PRD, and the old "maximum total size" policy wording was dropped because the ruled limits fix it. The owner should confirm which Settings stay.
- [L480 gap] FR-025 has no Step for template deprecation (see Graph changes); owner to be shown per L480.

## FR-003

- [L382] FR-003 F1/F2/F9 "remain separate questions": no later bullet closes it. The PRD already records the F1, F2, F9 outcomes (Change Log 2.12, redistribution), so nothing is left unstated in the PRD; the controller should confirm whether the open item is only about change-log link codes.
- [L496] Renumbering FR-003 requirement ids "in order": ledger 847 and 622 make renumbering a programme-wide final step with an old-to-new id table kept centrally, and the PRD cannot be renumbered alone without breaking citations in other PRDs. Ids in this PRD are left as they are; the PRD's Functional Requirements Summary is not in numeric order across its groups. Ledger answers on whether graph node ids change are still owed.
- [L515] REQ-003-015 stays; the name or number of the planned provider capacity management FR, and where planned FRs are recorded, were not given in the ledger. The PRD still says "Future FR: Provider Capacity Management" and "TBD".
- [L470 note, applied] Follow-up still unruled: the rule for one overall alert level (Critical, Standard, None) when an inquiry has several risk tags. The PRD only cites REQ-025-064, which defines the tier from questionnaire answers; the aggregation across several FR-002 risk tags is not stated.
- [L513, L514, L485 note, applied] Drafted values (duration choices, ProviderInquiry statuses, redistribution_state values) were applied without an owner approval round, per the process reset; they are drafts the owner may edit.
- [L1672 note, applied] The system-PRD identity Rule and the 10-year retention Rule have no ids yet; the PRD cites them by description until they exist.

## FR-004

- [L2114] FR-016 cites REQ-004-077, but the "restore expired/archived" clause of REQ-004-077 stays open under ledger 533. L549 settles restoring an expired quote only. There is no ruling on the state and expiry window of an archived quote that an admin restores. The FR-016 citation itself is a link and is left to the graph.

## FR-005

- [L1654] Gap list, no ruling: no FR-005 Rule states the identifiers the notification event carries. No later bullet closes it by name. L1733 ("Notification doc owns details") suggests the notification Rule owns payload content, but that is not a ruling on this gap. PRD left as is.
- Notes without a manifest bullet (decisions for the controller or owner, nothing applied):
  - System-PRD identity Rule (L510, L1672) has no id yet; the PRD pointers name it by description until it exists.
  - Retention: REQ-005-007 and Data and Privacy Rule 4 still say 7 years (at least). L893 ("10 years for everything") names REQ-005-060 for FR-005 but not these; the full list of lines that change is still owed. FR-023 REQ-023-001, 002, 013 need reconciling with the platform-wide no-hard-delete wording.
  - REQ-005-029: REQ-020-019 as read does not say that `booking.scheduled` is mandatory (cannot be disabled). The FR-020 pass should carry it, since FR-005 no longer states it.
  - REQ-005-023: L2059 allows an admin to change treatment details, while the Payment and Billing Rules say post-acceptance treatment changes go through FR-010 only. The Rule currently says treatment-detail changes also follow the FR-010 route; confirm. How an admin date-range edit relates to the FR-006 appointment change is not ruled either.
  - L545: the PRD does not name the fourth FR-014 repeat; the FR-014 pass should confirm the list.
  - Not decided by any bullet: whether the patient or provider is notified of an admin edit after acceptance.

## FR-006

- [L1795] Emergency edit scope: whether it reaches beyond bookings ("any edit within the system") and how it relates to the appointment change are not ruled. The PRD states only what L1793 and L2175 settle: non-money booking details, mandatory reason, full before and after history, never sets status, payment records immutable, guarded actions keep their checks.
- Note on [L1447] (counted as applied): the B4 provider-status cancellation and the B7 in-treatment fault were not ruled for the full-refund terms. The PRD keeps the credit placeholder for B4 (re-labelled as its own placeholder) and the generic placeholder for B7. Owner decision needed later if they should match B5.
- Note on [L1439] (counted as applied): the ledger does not say what "the point set for it" is or which actor performs the cancellation. The PRD says the booking is cancelled "at the point set for it (FR-029)", records the system as the actor in Key Entities Cancelled entry (4), and does not name a cancellation cause value.
- Note on [L583] (counted as applied): the ledger does not record which new Ticket Source values FR-034 gains or which FR-006 requests use them. The PRD only states that the support case's Ticket Source comes from the FR-034 list.
- Note on [L1566] (counted as applied): whether patients may see the "At Risk" and "Refunded" labels on Screen 2 is not ruled; the PRD shows the single FR-007 list on Screen 2 and points to it elsewhere.
- Note on [L565] (counted as applied): whether `booking.confirmed` and `booking.appointment_reminder` are mandatory, and exact timing of the reminder, are left to FR-020 and FR-030; FR-030 lists patient and provider as recipients.

## FR-007

- [L1655 OPEN] No FR-007 Rule sends a payment-failed notification (REQ-007-017, 041, 042, 043, 048, 085 cover retry and on-screen errors only; REQ-007B-017 exists in FR-007B and the owner did not add it). No closing ruling found; PRD left unchanged on this point.

## FR-007B

- [L332] Fund-release brief requirements for FR-007B beyond the money-movement decisions of L339 and L340 are not applied: the ledger says the drafts must be reworded before use (L351), the brief's remaining decisions were still to be asked, and no ruling for FR-007B in this manifest settles them. Only the L336 note and the O06 decisions were written.
- Not a manifest bullet, for the controller: L339 leaves open when a postponement would break Stripe's 90-day limit on clinic balances; the PRD note does not cover it.
- Not a manifest bullet, for the controller: no ruling says when a plan with a hard-declined installment becomes Defaulted; the PRD states only that automatic retries do not run and the patient must retry or update the card.
- Not a manifest bullet, for the controller: L624 and L635 left open the rescheduling-fee trigger and what a percentage fee is taken of; these belong to FR-029.

## FR-008

- [L621] Q-149 (validation limits as Rules?), Q-151 (passport-upload progress indicator; "declaring no travel does not block the procedure") and the display-strings half of Q-162 (Screens 10 and 12 contract or UI copy; also noted on L633) were folded into the FR-008 marking list owed under ruling A9. No ruling on the content exists, so no PRD text was written. The marking list for the owner is still owed.
- Drafting note, not a backlog item: in the Overall Status rule I added "counting only items the accepted option includes" so it agrees with REQ-008-018 (services not included are not collected). The ledger wording lists the required items without this clause. Remove it if the owner wants every Path A item always required.

## FR-009

- [L583] Q-115 "Extend the source list": the new FR-034 Ticket Source values and which FR-009 requests use them are not recorded in the ledger or any file I may read, and FR-034's PRD still lists three sources. No FR-009 text added. The only FR-009 touchpoint is "Request More Seats" (Screen 1 banner, Screen 2), which already opens an FR-034 support case pre-filled as a seat-increase request; add the source value once the FR-034 values exist.
- [L661] Whether a Manager is limited to Clinical Staff and Billing Staff when changing a role (REQ-009-004, change-role flow) is not ruled; PRD left silent on it. To bring back to the owner. Settled 2026-11-22: a Manager changes roles only of Clinical Staff and Billing Staff (REQ-009-004).
Notes for the controller (not bullets):
- Owner handover (L656): I placed it in FR-009 (Rule 11, REQ-009-174) because the Owner rules live here. Drafted details beyond "Hairline admin does it": a reason is required, audit entry, and both people notified by email. Not decided: whether the new Owner must already be an Active member, what role the previous Owner then holds (Rule 1 needs exactly one Owner), and which FR-031 admin permission allows it. FR-015 may need a pointer. Settled 2026-11-22: stays in FR-009; new Owner must be an active member, previous Owner becomes Manager, reason required, both emailed (REQ-009-174).
- The rejected change request `change-request-2026-09-29-custom-provider-role-assignment.md` is in this FR folder; marking it Rejected was outside my allowed files.
- Screen 11 Tab 1 Phone Number row still says Required "No"; not in the ruling, left unchanged.

## FR-010

- [L496] Renumbering FR-010 requirement ids "in order" is not applied. The ruling's follow-ups are still owed (old-to-new map shown to the owner first, whether graph node ids change, which outside places are updated), and the cross-FR citations written in this round (L2039 to L2089, FR-011 and FR-014 lines) still use the current ids. The PRD inline ids keep their current numbers (gaps remain, for example no REQ-010-005); new ids continue from REQ-010-106 (graph highest was REQ-010-105).
Notes on bullets counted as applied above (not backlog items):
- [L1718] The one system-PRD identity-hiding Rule does not exist yet (it waits on the system-PRD owner ruling). FR-010 Privacy Rule 1 therefore keeps its reworded unlock-point statement and says it is retired in favour of that Rule; remove the statement once the system Rule exists and carries the unlock point.
- [L1862] Open follow-up from the ledger: whether the FR-011 "medication catalog" is the same list as these templates and who owns it. FR-010 only points to FR-024.
- [L692] The control name and placement (Report Issue Before Check In, Screen 4 Stage A) were drafted without an approval round, as the brief directs; the owner may rename it.

## FR-011

- [L702] Q-33 check done by direct query. Aftercare assignee history exists: ENT-aftercare-audit-entry.previous_assignee_id and new_assignee_id (shown on SCR-011-19), plus ENT-aftercare-plan.assigned_team_member_id. The support-request-to-booking link is one-way only: ENT-booking.support_ticket_reference (FR-006) exists, but ENT-support-case (FR-034) has no booking reference Field, and no edge joins the two. For the owner: is the one-way booking reference enough?
- [L1656] Gap list, no ruling: no FR-011 Rule names a milestone-due or an escalation-alert notification. The dependency line now cites REQ-020-117 and REQ-020-120 and their FR-030 Rules, but no new FR-011 Rule was added.
- Concern, not a bullet: L711 (expiry ends as Rejected with full refund) and L1519 (payment comes last) interact, because an unassigned request has no payment yet. The PRD words the refund as "any payment already taken", so both rulings hold without a new business decision; owner may want to confirm that no deposit is taken at request time.
- Concern: L1718 and L725 say the system-PRD Rules do not yet exist in the system PRD or graph; PRD pointers name "the system PRD" without ids and need the ids added once they exist.

## FR-012

No manifest bullet is left unresolved. Follow-ups for the controller:
- [L732] The ruling says "Resolved when all flags are closed, otherwise Active". A conversation with no flags at all is not covered (Active by the literal wording, since nothing was resolved). The PRD repeats the owner's wording and states no zero-flag case; confirm if it matters for the Resolved filter. "Closed" was read as resolved or intervention_completed (the four flag states) and "under way" as a flag in escalated_to_intervention.
- [L2069, L2070, L1718, L725, L744] The system-PRD masking Rule, the system-PRD encryption record, the role-based access Rule, the timezone and compliance Rules, and the FR-004 chat Rule do not exist in the graph yet. The PRD cites them by name only. Add their ids to the dependency lines when those Rules are created.
- [L385] Move list for FR-012 Events is owed (see Graph changes).

## FR-013

- None. L385 depends on the move list the owner was owed; I recorded a proposed list above rather than deciding.

## FR-014

- [L496] Renumbering of FR-014 Rule ids ("Renumber and update citations") not applied. Ledger L847 (Q-109) sets renumbering at the final apply across all FRs with an old-to-new table, and the old-to-new map owed in L496 does not exist yet. Renumbering FR-014 alone would break citations in other PRDs, the graph and reports.
- Note on L780 (bullet counted as applied): the owed check on FR-029 "Rate History" (FR-029 prd line 570) found it is a 30-day rate-change view for one currency pair in the admin screen, not the daily fetched-rate record that FR-014 Entity 9 described. They look related but not identical; the FR-029 agent should decide whether its entity covers the daily record.

## FR-015

- [L656] Q-166 owner handover home (FR-009 vs FR-015) never chosen; PRD left as is. Settled 2026-11-22: FR-009.
- [L802 OPEN] `availability_status` meaning is owed; provider phone/email versus public phone/contact email carried from Q-91 and never asked. Attribute added by name only.
- [L1662 OPEN] No Rule says the admin-support alert deep-links to the Admin Support Required filter; no ruling, no PRD text.

## FR-016

- [L504] REQ-016-022 / REQ-035-026 encryption merge into one system-PRD Rule: the system-PRD Rule does not exist yet (no system-PRD node in the graph), so retiring REQ-016-022 would leave a dangling pointer. Not applied; REQ-016-022 and the encryption lines stay as they are.
- [L509] REQ-016-167 / REQ-026-019 audit-log retention merge into one system-PRD Rule: same reason (target Rule not yet written; the 10-year period is also still marked open in the ledger line, though ledger lines 567 and 893 later set 10 years for everything). Not applied.
- [L834 OPEN] Q-107: whether admins may edit patient scans is not ruled. Rule 2 and the Fixed list keep scans (and uploaded photos) as unchanged by admins.
- [L847] Q-109 renumbering without gaps: the ledger says it is done at the final apply for all FRs, in the graph and the new PRD package, with an old-to-new table. A per-FR renumber now would break the REQ-016 ids that other FRs cite (for example REQ-016-028 and REQ-016-058). Inline ids REQ-016-001 to REQ-016-032 are kept; REQ-016-018 stays a gap.
- Residual open points inside applied bullets (not counted above): [L831] which document types a patient uploads besides photos (settled 2026-11-22: PDF and image files only, at most 5); [L836] free text or templates, and which channels, for manual notifications, and Screen 7 has no action type for a manual notification; [L834] Screen 7 has no action type for a medical data edit (Medical Data Access and Admin Note exist); [L429] return path from Locked after the lockout period or an admin unlock; [L583] the new Ticket Source value names are defined in FR-034.
- Not in the manifest, so not edited: ledger line 893 ("10 years for everything") would change the 7-year retention wording in this PRD (REQ-016-016, Rule 6, Privacy wording, Screen 4 compliance note, flow B5); the controller should confirm whether another bullet or step covers it.

## FR-017

- [L844] Q-121, Q-122, Q-126, Q-127 were moved to the fund-release batch; the Release Rules above cover the fund-release rulings, but no bullet records answers for those questions individually. Q-123 waits for the FR-007 payment entity. Not applied beyond that.
- [L623] The final single payout status list for FR-017 was proposed to the owner but its final wording is not in the manifest; Entity 2 and REQ-017-015 keep the existing status lists.
- [L1004] The mapping of Screen 4 invoice values "Partial" and "Pending" to the FR-007 payment status list is not recorded; Screen 4 invoice statuses are unchanged (only the instalment status list was aligned, via L2177).
- Also noted (no bullet): L1533 field and status mapping for the merged discount entity is owed; Billing Rule 3 and the affiliate cron line still use "buffer" wording because no ruling covers the affiliate monthly statement timing; the manual "mark as paid" rail sits beside Main Flow steps that describe Stripe transfers only; Rule 13 now says the full refund is issued through admin financial resolution (a wording choice that reconciles "no automatic refund" with L1447); the B1 and B2 diagrams both use the B2S prefix after the ruled relabel.

## FR-018

- [L426 WORDING-OWED] P19 merged wording is drafted here: "Bank account details (account holder name, bank name, account number, routing/SWIFT code, IBAN) of affiliates and providers MUST be encrypted at rest using AES-256." Home FR and `scope: global` are not settled by any later ledger line (L462 says a system-PRD owner ruling is still owed). PRD unchanged: REQ-018-015 in FR-018 stays as is.
- Sub-items of applied bullets, not counted above: (a) L864 and L896/L1870: no ruling names the admin screen that edits the payout day or the tier bands; the PRD states both as platform settings without naming a screen. (b) L862: not asked whether 25% caps percentage commissions; unchanged.
- Notes for the controller (not bullets): (1) L2171 "Manually paid clinic Ready" is about clinics (FR-015/FR-017 owner); FR-018's affiliate-side equivalent (Billing Rule 3 and Campaign Eligibility require complete bank details) already holds, so counted as already true with no edit. (2) L2170 is worded for providers; it was applied to affiliates because L865/L1872 S-44 tie the Banned-status follow-up to FR-018. (3) Rule 15 still states the ceiling as `discount % + commission %`; with commission now on net revenue after the discount, the arithmetic differs slightly. No ruling covers it, left unchanged. (4) L1878 asks to align REQ-019-037 and REQ-017-134 in their own PRDs. (5) Q-142 (booking total to USD) was not applied here; FR-018's Currency Rule already converts at the locked rate.

## FR-019

- [L875 / L1872 S-46] Pending Approval state: Screen 1 and Alternative Flow list it, the lifecycle field at Screen 2 (Draft, Active, Paused, Expired, Archived) does not; no ruling closes it. PRD left as is on the Screen 2 field.
- [L881 Q-152] Where the admin sets the ROI bands: not ruled. PRD says the bands are admin-defined only; no Setting named.
- [L899 owed] Which promotion status changes send a notice and to whom: not ruled; PRD states only that a separate status-change event exists in FR-030.
- Note for the controller: L589 (retire REQ-019-016, FR-029 keeps it) and L881 Q-160 (REQ-019-016 gains the full clause) point opposite ways; applied the later line (L881) and cited REQ-029-054 beside it. If the owner wants the retirement, remove the Rule and keep the pointer.
- Note for the controller: List-selection and Either for a Hairline-Funded program: line "Hairline-Funded programs do not appear in provider selection UIs" stands, so what those two modes mean for that program type is not ruled.
- Note for the controller: ledger L1878 names REQ-019-037; the graph's REQ-019-037 is the direct-issued code Rule (Alternative Flow C1), so the edit sits there; confirm no other Rule was meant.

## FR-020

- [L518] Q-71: the check of the FR-020/FR-030 catalogue recipients of `inquiry.cancelled` after "Only providers with quotes" was owed to the owner and no closing ruling is in this manifest. Ledger L913 (not in the manifest) says providers with a live quote get only `quote.cancelled_inquiry`, with the Rule wording still owed. The PRD rows for `inquiry.cancelled` (Provider recipient) and User Story 4 are left unchanged.
- [L1734] The six sibling pairs settled from the Q-157 links stay "linked" unless the owner extends the notification-pairs answer to them; REQ-006-011, REQ-004-046, REQ-015-019 appear on both sides. Not extended, so nothing applied.
- Superseded (no action): [L383] by L384; [L349] by L1570 and T122.

## FR-021

- [L1573] Where the Step "runtime clients fetch published translation bundles" (doer the system) is filed, now that an "all stages" place is ruled: still open, not asked yet; no later bullet for FR-021 closes it.

## FR-022

No manifest bullet is left open. The points below are observations for the controller, not decisions taken.
- Technical lines outside the lines named in L1002 remain in the PRD (Future Enhancement P3 Elasticsearch/Algolia, Technical Considerations bullets on indexing, query builder, pagination and caching, Assumption 3 on full-text support, Data Dependencies Entity 3 migration scripts, Key Entities Database Index, Rule 2 and Performance Rule 2 wording on database indexes). Not removed because the ruling named specific lines and L982 keeps the Database Index text.
- [L1600] Gap carried over: how a patient or clinic user reaches support from a failed search is not written anywhere.
- [L1578] Gap carried over: no provider search Screen exists in the graph for the third doer of B1 and B2.
- [L1713] REQ-032-106 was merged under an earlier follow-up (survivor in FR-034, FR-032 refers to it); the PRD cites it as the ruling names it. Reconcile the id when FR-032 and FR-034 are applied.
- [L985] FR-003 / Screen 7a "Active Status: All, Active Only" in patient provider search: the ruling says "All includes suspended (admin use)" and FR-003 line 433 stands; FR-022 did not change the Screen 7a filter.
- REQ-022-043 (provider support case search) is still stated in the summary alongside the FR-032 pointer; the ruling named only REQ-022-086 for retirement.

## FR-023

- [L272] OPEN: the conflict between REQ-005-060 (no hard deletes, scope global per Q-fr001-009-96) and REQ-023-013 ("purge search indexes and caches") is not closed by a later ruling for REQ-023-013. REQ-023-013 wording left unchanged; the 10-year Rule already forbids hard deletion of the protected records.
- [L555] OPEN: follow-up owed to the owner on how the purge rule (REQ-023-013) changes under "Whole platform"; L893 and L1028 list REQ-023-013 as affected but record no ruling on the new wording. Same item as above.
- [L331] WORDING-OWED: the new Stage name "Deletion requested" is a working name the owner has not confirmed; no PRD text depends on it.
Superseded or closed: L327 (OPEN, closed by L331), L383 (OPEN, closed by L567 and L893), L1016 (marked SUPERSEDED by L1025).

## FR-024

- [L496] Q-fr001-009-59 "Renumber and update citations": not applied. The ledger (L847, Q-109) makes renumbering a final-apply step across all FRs with an old-to-new table, and doing it here would put the PRD ids out of step with the graph. The FR-024 PRD ids today equal the graph ids; the retirements and the new REQ-024-085 above will leave gaps (010, 011, 012, 030, 031, 034, 047, 066) for the final renumbering to close.
- Note, not a manifest bullet: REQ-024-035 and Screen 3 still say Base Price MAY feed a future post-MVP starting price on provider cards, while L400 says the provider starting price is the lowest standard price among active packages. No bullet orders a change to the Base Price sentence; left as it was, flagged for the controller.
- Note, not a manifest bullet: after a Pending Media Upload treatment gets its media, the PRD does not say which status it takes (L1046 says only "hidden until media is added"); left unspecified.
- Note, not a manifest bullet: L1035 "Setting ranges owed": only a lower bound (whole number of 1 or more) was drafted; no upper limit was invented.

## FR-025

- None. [L1057] was SUPERSEDED by [L1075] (Q-93 answered "No; only replace or archive") and is not applied separately.

## FR-026

- [L509] The pair REQ-026-019 (audit logs kept 10 years) and the system-PRD Rule: ledger 509 says it waits on the system-PRD owner ruling and that the 10-year period itself stays an open question. REQ-026-019, Audit Rule 3, SC-016 context, and the "Audit logs retained for 10 years" lines in Implementation Notes are left unchanged in the PRD. Only the REQ-026-018 half is applied (via L1124). Needs: system-PRD Rule for audit retention, then retire REQ-026-019 here with a pointer.
- [L1079] Quiet-hours Setting (one platform-wide, admin-set, default 10 PM to 7 AM recipient local time): the ruling leaves the owning FR and the screen field open (FR-026 or FR-030). No bullet in the manifest closes it, so the PRD is unchanged on this point. Needs: owner of the Setting; if FR-026, add a Screen 8 row and a Rule.
Notes for the controller (not counted as bullets):
- FR-026 Screen 8 rows with no stated value (head scan limits, admin maximum failed logins) are described but no value is invented; they are implementation-phase items.
- The Q-100 names for FR-031 and the REQ-026-001/054/107 role and permission wording remain as working names in FR-026 until the FR-031 work records the names.

## FR-027

- None. The Q-90 list of the 8 FR-027 flags is not in the ledger text read; it is a graph-side step, not an open owner question.

## FR-028

- None.

## FR-029

- [L635] Not defined by any ruling, so the PRD is silent: when the rescheduling fee is charged, what a percentage fee is taken of, and the currency handling for fixed amounts (Screen 7 states only that fixed amounts use the system default currency).
- [L1449] The base amount that the refund ladder percentage applies to (deposit, amount paid so far, or booking total) is not ruled. The old Refund Rule said deposit refunds; Screen 7 and the Refund Rule leave the base open. FR-007 and FR-006 wording should be aligned by the controller.
- [L780] The Entity 7 attributes (date, base and target currency, rate, fetch time) were drafted from the FR-014 daily-rate use; the ruling gives no field list, so the controller should confirm them against FR-014's rate-history wording.
- [L1133] D09 link on REQ-029-004 was to be reviewed with the owner at apply; the owner did not pick "UK account first", so the link needs a graph decision.
- [L881 / L589] FR-019 still holds REQ-019-016 as a matching Rule; confirm it is retired in the FR-019 apply.
- [L1144] AES-256 for Stripe keys (Privacy Rule 1, Implementation Notes, Security Considerations, Fixed in Codebase list) is left in FR-029 because the ruling names only TLS 1.3 and PCI DSS.

## FR-030

- [L899] Q-171: the new promotion status-change Event is owned by FR-030, but no ruling says which status changes notify and whom, and no later bullet closes it. The PRD is unchanged on this point.
- [L914] Not a count: the ruling cites "line 405", which is only a table header in FR-030; the owner FR was inferred from "line numbers near 416" and is probably FR-020. The generic rule (in-app entry always created when Email and Push are both off) was added to FR-030 as an edge case; the controller should confirm the owning FR.
- [L1661] Not a count: gap noted in the bullet itself. No FR-030 Rule uses the `monitoring.*` name or says those events are published to the notification service (OPEN, no ruling).
- Not a count: event 3 `monitoring.converted_to_aftercare` is not in the FR-030 catalog, and the manifest has no bullet for it.
- Not a count: `monitoring.converted` was renamed `monitoring.converted_to_inquiry` from L956, which is not in the FR-030 manifest; revert the one catalog row if the controller does not want it here.

## FR-031

None unresolved. Notes for the controller (not counted as bullets):
- Q-174 scope: the ledger names only FR-031 lines 16 and 52, but the rejected change request had introduced custom provider roles across the whole PRD; I removed them everywhere, as the FR-009 result did. The change request file `change-request-2026-09-29-global-custom-provider-roles.md` in the FR-031 folder is still not marked Rejected (outside my allowed files); the Change Log history row for v1.1 is left as it was.
- Q-78 versus L1188: the ledger adds an actor "Finance admin" and also names the admin finance role "Billing Admin". I recorded Finance admin as the actor who holds the Billing Admin role. If the owner meant a separate role, that line needs a change.
- L1193: I read "Custom Role 1 column follows Reject both" as removing that example column from the admin default grid; custom admin roles themselves stay.
- L1062: FR-026 names no admin roles; the two permission names added (View Sensitive Settings, Manage Authentication Policies) are the only gaps against FR-026's use.
- L1210 and L1211 carry PRD line numbers that do not exist in FR-031; no FR-031 text was changed for them.

## FR-032

- [L426 WORDING-OWED] P19 merged Rule wording, home FR and `scope: global` are not settled by any later ledger line (L462 says a system-PRD owner ruling is still owed). Suggested wording from the FR-018 result: "Bank account details (account holder name, bank name, account number, routing/SWIFT code, IBAN) of affiliates and providers MUST be encrypted at rest using AES-256." FR-032 PRD left as it is: REQ-032-018, Privacy Rule 1, Billing Rule 4 and the "Fixed in Codebase" line stay until the home is settled.
- [L1541] The per-FR marking list of screen-row requirements (Q-moved-14, ruling A9) is owed to the owner; the owner marks each FR-032 screen line there. No Rule added to FR-032 meanwhile.

## FR-033

- None. Every bullet was closed by a later line or settled directly. The Q-38b follow-up (L1233) was answered at L1243.

## FR-034

- [L381] A7 item 24b ("FR-034 24b", a missing fact on which events fire at which Stage): no later ledger line closes it (L1341 explicitly leaves the assigned and admin-reply event parts as separate questions). PRD left unchanged on that point.
- [L583] Q-115 "Extend the source list": the new Ticket Source values and the requests that use them are not recorded in the ledger or any readable file (the FR-009 result file reports the same). PRD still lists three sources (Patient App, Provider Portal, Manual Admin Entry).
- Note, drafted wording to confirm (owner-visible drafts, not open rulings): L1270 "what remains editable" on built-in categories is drafted as label and display order; L1255/L1417 the Escalate tick takes its New Assignee from the existing Support Staff list, so whether Super Admin appears in that list for a manual escalation is not stated; L1877 how request status sits beside case status is drafted as two separate values with no automatic coupling; L389 the throttle limit for problem reports is not given a number.
- Note, left as is (would need a ruling): "Case analytics" wording in Business Value (Executive Summary) and SC-019 still mention analytics although the reporting view is dropped (L1259); case-level Feedback Resolution on Screens 2 and 3 was kept because only the resolution details named in L1347 were removed from the case.

## FR-035

- None. Notes: [L452] superseded by [L457]; [L1271] superseded by [L1277]. [L504] says it "waits on the system-PRD owner ruling"; the owner ruling itself ("Move to the system PRD", and "security lines once in the system PRD") is recorded, so the pointer was applied, but the system PRD Rule id is not known and is not cited by id.

## FR-037

- [L2172] Launch default (3), "conversion-lift minimum: 20 quotes on each side", was filed under FR-037 but nothing in FR-037 measures a conversion lift. The ledger (L925) ties that lift to the FR-019 promotion report, so the setting probably belongs to FR-019. Not applied here; the owning FR needs confirming.
- Note (not a bullet, not counted): the graph may hold REQ-037-049 as a separate Rule; confirm it is retired together with REQ-037-048, since the 7-year raw scan period no longer exists under "10 years for everything".
- Note (not a bullet, not counted): whether "at least one view" also applies to FR-002's treatment-request photo set is a follow-up for FR-002, not decided here.

## FR-038

- [L2172] Launch default (3), "conversion-lift minimum: 20 quotes on each side", is listed under FR-038 but concerns the FR-019 Conversion Lift formula (ledger L908, L925: lift in acceptance of quotes with versus without a promotion). The FR-038 PRD has no quotes, promotions or lift measure, so no text was added. Likely a manifest mis-assignment; the Setting belongs to FR-019 (the FR-037 section of the manifest also lists it "also under FR-038").
- Note (not a bullet, no count): the manifest's L2172 default (2), "default patient progress reminder: once a month for 12 months after treatment, patient may change or switch off", is listed only under FR-011, but it matches the FR-038 reminder default asked at L1309 ("what the default schedule is"). I did not state the value in FR-038 because L1316 says FR-038 only refers to the FR-030 schedule. The owner of the FR-030 and FR-011 sections should confirm where the value is written.
- Note (not a bullet, no count): L1290 says "six FR-038 entities retired" but L1293 (later) keeps the FR-038 audit entry, so five are retired. The conversion record shape (inquiry in FR-037, standalone-aftercare request in FR-038) was left as a held modelling question at L1290; the PRD says only that the shared conversion record's destination is an FR-011 request.
- Note (not a bullet, no count): the system-level download-link Rule (L1704) and the single retention Rule are cited by home, not by id. The system PRD currently has no download-link statement; the pointer stays valid only once the system-PRD owner ruling is applied. FR-037 REQ-037-040, 041, 045, 054 and others cited by id exist in the graph but the FR-037 PRD does not yet show them inline.
- Note (not a bullet, no count): proposed wording for the monitoring.aftercare_conversion_started notice (L979, wording and timing owed) is in the PRD marked "to be confirmed in notification copy review"; the owner was not asked.

## GLOBAL

Open bullets that no later bullet closes, and items outside the allowed files. None needs an owner question; each carries the controller's reading where one exists.
| Bullet | Ledger line | Item | Reading or reason |
|---|---|---|---|
| 11 | 297 | Eleven changes applied without an owner answer need ratify-or-revert (provisional Stage placements for FR-008 and FR-033, FR-014 Rules linked to 13 Screens, FR-037 entry-point Flows and others) | No later bullet closes it. |
| 25 | 385 | Events with no key and keys with no Event (H3-25) remain open | No later bullet closes it. |
| 26 | 402 | Twelve misplaced passages in eleven PRDs, to be asked one by one at the compression phase | Ruled "ask me for each one"; each needs a proposed place first. |
| 49 | 652 | List of variant names for the same clinic role or actor, owed to the owner | Owner note: "please also fix the wording to make sure they point to the same thing, not so many different things in the system". The Actor merge (bullet 50) does not replace the list. |
| 56 | 824 | Vocabulary list entry: graph `uploaded_by` versus PRD `uploader_type` | No later bullet closes it. |
| 60 | 900 | Cross-FR items Q-fr010-019-3, 18, 41, 72, 74, 98, 101, 114, 115, 133 wait for prepared lists | No later bullet closes it. |
| 67 | 1242 | Same business and technical mix in the stored-data lists of other FRs | Facts to gather first. |
| 71 | 1329 | End-of-programme pass that walks the whole journey, then one more fix round | Placement in the plan owed; may overlap the flow-scenario phase. |
| 72 | 1327 | Mark Phase 7 done with the recorded figures in the phase file | The phase file is outside the files this pass may edit. |
| 81 | 1455 | Q-fund-release-11: Stripe facts STR-1 to STR-6 | Owner selected no option and asked to use Stripe public documentation and the brief. Controller's reading: record STR-1 to STR-6 once as "not confirmed with Stripe". |
| 83 | 1457 | Q-fund-release-12: completion confirmation | Owner selected no option, gave a note. Controller's reading: no new patient screen; the completion email carries a link to the support-request route; no support request in the confirmation window means completion is confirmed; no separate confirm button. This reading is already how the system PRD payment text is written. |
| 98 | 1487 | Q-fund-release-24: currency of a payment amount | Owner selected no option; quoted note: "Then that amount is exchanged into the other currency as per the exchange rate config". Controller's reading: one base-currency amount converted with the exchange-rate configuration. |
| 124 | 1742 | Row B32 stays open (C54 is closed by the provider payout timeline) | "B32 and C54 stay open"; C54 is resolved by [T118], B32 is not closed in this slice. |
Other items for the owner of the work, not counted: the 10-year retention period has no legal document behind it (the owner was told no document confirms 7 or 10 years); other system PRD text still says "escrow" in the overview, the payment dependency lines and the glossary, and was left because it is consistent with the locked-balance flow.

## Reconciliation pass leftovers

**fr006.md**

- Pointer follow-up "align payment text to the payment flow lines in the system PRD": not applied. The B4 provider-status cancellation placeholder (paid amounts move as credit, unused part refunded; Alternative Flow B4 step 4, Payment & Billing Rules Provider-Status Cancellation, Screen 10 text) was left, because ledger L1443 area says the B4 and B7 cases were not ruled (Q-fund-release-2). The "other cancellations follow the ladder" wording in the PRD therefore sits beside that unruled B4 placeholder; controller to confirm whether B4 should also move to the ladder or to a full refund.

**fr007b.md**

- Pointer follow-up, align payment text with the system payment flow: Money movement in Payment & Billing Rules already matches. Alternative Flow B4 step 2 and REQ-007b-027 still say paid installments move as credit toward the replacement booking when the provider withdraws, drops out or is suspended/deactivated. Ledger 1447 (Q-fund-release-3) rules a full refund for withdrawal or drop-out only and states suspension/deactivation (B4 case) was not ruled, so a clean edit needs a business decision on that case. Not in the FR-007B brief section; left unchanged. Controller to rule on whether to apply "full refund" to withdrawal/drop-out in FR-007B B4 and REQ-007b-027 (as done for FR-007) and what to say for suspension/deactivation.

**fr013.md**

- A2: no FR-013 id appears in the global Id table; REQ-013-015 (encryption) is not listed as retired, so no edit. A3: no follow-up row for FR-013. A4 and A5: no mentions of custom provider roles or payout frequency found.

**fr022.md**

- Technical requirement rows kept: REQ-022-021 (JWT for search endpoints), REQ-022-024 (SQL injection and XSS sanitising), REQ-022-028 (create database indexes), REQ-022-029 (cache autocomplete 5 minutes), REQ-022-032 (database queries under 100ms), Performance Rule 2 (database indexes) and Performance Rule 4 (autocomplete cache). They are numbered requirements, not leftover notes, and L1002 does not name them; removing them is a scope decision for the controller.

**fr030.md**

- Not changed on purpose: the 90-day operational notification-log period (REQ-030-013, Privacy Rule 6, Scalability) is an operational window, not the ruled retention period; archive retention already points to the platform policy.
- Note: REQ-SYS-005 in the system PRD speaks of payment webhooks; the citation follows the Id table as given.

**fr034.md**

- Assumption 5 (User Behavior Assumptions, line about "consistent case analytics") and Screen 3/Screen 7 "for analytics" notes on Root Cause (resolution fields captured for analytics and trend identification) were left: the brief names only the Executive Summary and SC-019, and root-cause capture itself was not ruled out. Controller may decide whether the wording should also drop "analytics".
- The 2.3 change log row (2026-01-26) still mentions "7-year minimum": it is history, not a live retention statement, so left untouched.


## Graph apply leftovers

Added 2026-11-20 after the graph change-sets were applied. Each FR's own list is the "Not done" section of `plans/reports/graph-result-261120-frNNN.md`; the points below cut across FRs or came from the controller's checks.

- Links from live nodes to retired nodes: 37 of the 45 were re-pointed or removed on 2026-11-20 (`graph/changesets/2026-11-20-retired-links.yaml` and `-retired-links-2.yaml`). 8 remain because the replacement Field is a judgement the PRDs do not settle: `SCR-005-01` shows retired `ENT-provider.credentials_summary`; `SCR-014-01` shows retired `ENT-payout.cadence`, `.period_start`, `.period_end`, `.scheduled_date`; `SCR-014-04` shows retired `ENT-payout.cadence`, `.period_start`, `.period_end`. Candidate replacements for the payout screens: `ENT-provider-payout.payout_period`, `.payout_date`, `ENT-payout.payout_method`.
- Fields dropped with no replacement: the support-case auto-closure deadline (countdown on SCR-035-03 and SCR-035-04; the FR-035 PRD still shows it at lines 375 and 394, and it can be computed from `ENT-support-case-resolution.resolved_at` plus the auto-close period Setting, so no stored Field may be needed) and case type (Type column on SCR-032-16 and SCR-032-17; the FR-032 PRD still lists the column at lines 1443 and 1494 while FR-034 retired `ENT-support-case.case_type`: the two PRDs conflict and one must change).
- FR-034: about 16 Rules keep old "Support Manager" and "Support Agent" wording (REQ-034-031, 083, 086, 087, 088, 092, 094, 100, 101, 108, 117, 136, 149, 151, 155, 158); the admin-only flows are not moved to the Operations Stage because the move list was never written.
- FR-037 and FR-038: the conversion record shape between monitoring and aftercare is held; the field mapping from the retired transplant-progress entities to the shared monitoring fields was done by name and should be confirmed; A2 steps 5 to 8 of FR-038 are not in the graph.
- FR-033: no Field or Setting for the "Return to Automatic" control and the hand-set flag; no Steps for the provider video embed URL or audience selection on create.
- FR-035: navigation Rules REQ-035-033 to 038 left active; Ticket Detail message rows not split into history and reply box.
- FR-032: aggregate review Fields, the REQ-018-015 and REQ-032-018 merge, the SCR-032-17 row split and the Payout Readiness and Payout Timing rows are not linked.
- Earlier items: ENT-discount-code not merged into ENT-promotion-program; promotion status-change Event missing; payout Events without a producing Stage; FR-021 flow A1 Steps and the bundle-fetch Step; FR-022 flows B1 and B2; optional-again fields not identified in FR-026 (5) and FR-027 (8); FR-to-FR reference links the schema does not allow (FR-025 to FR-031, FR-027 to FR-009); the `SET-discovery-source-options` merge; REQ-031-099 governed by both the shared lockout Settings and `SET-admin-max-failed-logins`; seven FR-031 Events still at the inquiry Stage; the FR-028 destination-location default-currency field and stale STP-028-422 and STP-028-424 titles; two L18 hand-offs (STP-007B-408/605, STP-005-016); the `quote.restored` Event; STP-029-126 applying retired REQ-029-090; REQ-029-146 and REQ-029-147 with no Setting; stale Event links on REQ-013-017; REQ-023-011 and REQ-001-012 flagged as near-duplicates.
- Display-only Screens with no Step on them (lint L03, 6 findings): `SCR-001-20` (splash), `SCR-001-21` (explanation), `SCR-001-24` (settings main), `SCR-001-25` (privacy and security menu), `SCR-001-26` (password changed confirmation), `SCR-026-14` (platform settings editor). The owner's marker ruling requires a marked Screen to be used by a Step; the flows that pass through these Screens need a Step linked `on` each.
- `ENT-aftercare-content-template` (new, FR-024 Screen 8) has no Stage `writes` or `reads` edge and no Rule `applies to` it yet (`REQ-024-085` and an admin configuration Stage are the candidates).
- `SCR-001-23` (FR-001 service selection) is marked display-only because the PRD stores no choice at registration. If the choice should be remembered, FR-001 needs a Field and a PRD statement.
- 63 Sources are still "pending review" and cited by nothing; the list is in `plans/reports/docs-manager-261120-2140-pending-sources.md`.
- `REQ-007-054` says the payout is visible "only after treatment marked complete by admin"; the FR-007 PRD line it matches says "after the provider has marked the procedure complete". The Rule wording should follow the PRD (found while linking Rules to PRD lines by text match; other matched Rules may carry similar small differences, which the consistency check should catch).
- 89 hand-offs between FRs are not stitched (lint L18). The earlier stitch draft was thrown away by owner ruling, to be redone later; this is carried to the programme's consistency check (Phase 8).
- Nine Rule texts were brought in line with their PRD on 2026-11-20 after a line-by-line check (`graph/changesets/2026-11-20-prd-sources-agent-checked.yaml`). `REQ-008-064` lists "Not included" among the badge values for all four badges, while the FR-008 PRD gives the passport badge Awaiting, Submitted and Incomplete only; left as is.

### Added 2026-11-21 after the completeness re-check

- Owner items from the re-check were in `plans/reports/owner-decisions-261121.md`; all 17 were answered and applied on 2026-11-22.
- Lint findings accepted or recorded: L17 on ten Steps that sit at several Stages (`STP-021-036`, `040`; `STP-022-037`, `041`, `042`, `043`, `050`, `051`; `STP-027-032`, `033`), an accepted exception the checker cannot mark; L03 on `SCR-026-14` (the PRD gives no step on it); L09 on `ENT-provider-team-notification-routing` (the PRD names no Fields). L18 is now 90.
- Steps that only say the system checks or validates something are still in the graph (ids in section 7 of each `plans/reports/tester-261121-frNNN-completeness-recheck.md`). The owner dropped such Steps; retiring them needs each flow re-linked, to be done with the Phase 8 stitching.
- The Step "runtime clients fetch published translation bundles" (FR-021) still has no Stage; file it at the all-stages place when Phase 8 stitches FR-021.
- Edges that start at a retired node are kept by the writer as history (about 590); no live node links to a retired one.
- Stale texts to fix with the next PRD pass: `REQ-028-062` rationale ("question raised"); FR-009 `action_type` description; FR-019 "reversed" in the promotion application status description and "open item" in `hairline_portion`; `reopened_by_admin_id` is required although the system can reopen a case; this file's line about the FR-033 provider embed URL (drop the provider half).
- PRD wording to fix: FR-002 lines 42 and 211 give two different example lists of security settings; FR-016 cites the retired `REQ-020-091` and line 1065 says "Scheduled"; FR-022 line 66; FR-023 lines 84 to 90 against 132 to 133; FR-027 line 331 (status list); FR-029 line 1193 ("patient's country location"); FR-030 pause prompt 401 against 304; FR-032 Entity 2 line 2041 and the My Support Cases Type column.
- 94 Sources are cited by nothing, and 395 Rule rationales cite a PRD line that the line-refresh script could not confirm by text match (the list was a working file of the 2026-11-21 session and was not kept; re-run the text-match check before acting on it).
- Three payout Events named by the FR-030 PRD have no producing Stage in any PRD, so no Event nodes exist for them.

### Added 2026-11-22 after the owner answers

- The country flag is now required (FR-026 Screen 4, REQ-026-011): the starting country list and the bulk CSV import need a flag asset for every country; the PRD does not yet say how the import supplies it.
- FR-031 and FR-003 PRD text already matched the answers on the shared failed-login setting and the problem-duration list, so those PRDs carry no 2026-11-22 change-log line.
- Patient additional documents (owner answer 6: PDF and image files, up to 5 more): the rule sits on the admin screen only (FR-016 Screen 4, REQ-016-216). No patient-facing PRD yet says on which screen the patient uploads them; recommended home is the patient profile (FR-001). Needs a PRD line before development.
- FR-022 Payment Status filter lists (PRD lines 958 and 985) still include "Overdue". That is the booking payment status, not the installment plan status that owner answer 8 changed; left as is.

### Added 2026-11-22 after the cross-FR consistency review (Phase 8)

Per-FR detail is in `plans/reports/docs-manager-261122-frNNN-consistency.md`. None of these is a business decision; each needs a PRD or graph edit.

- **Flows a PRD points to but the receiving FR has not written** (12 hand-off notes stay open in the graph for these):
  - FR-006 has no Change Appointment flow; FR-007B (STP-007B-601), FR-010 (STP-010-030, 031) and FR-016 (STP-016-094) hand to it.
  - FR-007 has no Payment Options step (STP-007B-001) and no aftercare payment flow (STP-011-011, STP-011-024).
  - FR-004 Workflows 2 to 7 have no Flow in the graph; STP-006-604 hands to Workflow 7.
  - FR-015 has no Commission and Financials tab step (STP-017-033, STP-029-056) and no view-provider-profile step (STP-022-014).
  - FR-001 has no Delete Account flow (STP-003-085; FR-026 A5 also points there).
- **Other flows or steps missing from a PRD or the graph:** FR-017 affiliate payout flow (FR-018 B2 hands to it); FR-003 step for choosing Aftercare; FR-032 Browse Reviews flow; FR-034 receivers for provider reply and reopen, and for the deep links to FR-015 and FR-016; FR-029 B6 steps 6 and 7 and a Currency Management flow (FR-028 B5 hands to it); FR-026 A2 step 12; FR-037 conversion retry branch; FR-031 A4 step 14 permission sync into FR-009; FR-005 main flow step 10 into FR-006.
- **Notification catalog:** 13 Events that send notifications are missing from the FR-030 catalog (8 owned by FR-009, 5 by FR-017; ids in the FR-030 report). Add catalog rows to the FR-030 PRD, then move the Events to FR-030. Notification Steps in FR-012, FR-019 and FR-024 are not linked to an FR-030 flow.
- **Steps filed at the wrong Stage:** STP-018-011 and 012; FR-016 B5 Steps 111 to 114; FR-006 B2 admin cancellation Steps; ten FR-026 Steps (015, 016, 025, 046, 055, 064, 077, 078, 084, 092); STP-031-414 and 416; STP-030-024, 048 and 049 to 057; STP-015-151.
- **Records described twice (merge during compression):** medication instructions (FR-010) and the medication field on the Treatment Record; discount code (FR-019) and promotion program or code; currency config (FR-021) and currency conversion settings (FR-029); notification attempt (FR-020) and notification delivery log (FR-030); provider Fields location and country, specialties and specialty, total procedures and completed procedures count. `ENT-provider.active_patients` does not say what "active" means.
- **System-check Steps left in the flows:** STP-012-012 (starts a flow and has two exits) and the Steps marked mixed or borderline in the reports (they also record or decide something). Rewrite each as its action when the PRD is compressed.
- **Hand-off notes cleared without a link:** STP-014-014 and STP-014-018 (drill-down into "operational modules", no single receiving step).
- **PRD tidy-ups:** FR-032 alternative flow labels (A1 and A13 used twice, A4 missing); FR-038 lines 441 and 503 still say "FR-011 checkout" (the request is submitted first and paid later); Dependencies lists missing FR-013 and FR-027 (FR-003), FR-007B and FR-024 (FR-017), FR-015 (FR-012, FR-024), FR-032 (FR-012); FR-016 B5 step 1 names FR-034 while Screen 8 names FR-023; FR-007 line 125 "Patient cancels booking" against FR-006 B2 (admin-only cancellation).
- **Check rows accepted as they are:** 23 Fields owned by a different FR than their record (payment fields on the booking by FR-007, conversion fields on the monitoring case by FR-038, admin flags on the patient by FR-016, language, region and timezone preferences by FR-021); records read but never written because they are fixed lists or computed views (permission, questionnaire context type, team summary, installment plan metrics); audit records written and never shown on a screen (search audit log, travel audit entry); Stages that hold no steps yet (Monitoring, Dormant, Deletion requested).


### Added 2026-11-23 after PRD compression (Phase 9)

Filing items found while compressing the 38 PRDs and in the independent reviews. None blocks Phase 9.

- FR-034 Screen 1: the Filter Bar row sets the Date Range default to "Last 30 days" (REQ-034-116) while the screen rule says the default view shows cases "from last 90 days". One of the two numbers is wrong; owner or Phase 10 to settle.
- FR-034 Rule 12 refers to "success-criteria goals", a section removed by compression.
- FR-009 header Status line (v1.8) and footer Last Updated (v1.10) are stale against the change log version.
- FR-031: REQ-031-075 graph text "Changes will take effect for all [Role] members on next page load" vs PRD "within 5 seconds and apply on their next request"; REQ-031-085 graph message "You are the last Super Admin..." vs PRD line (Super Admin cannot change own role, REQ-031-009) — graph and PRD differ. Footer Last Updated 2026-11-20 stale. Dependencies list (FR-009, 015, 020, 026, 001) differs from graph edges (FR-007, 020, 022, 030).
- FR-029: FRS REQ-029-004 "patient's country location" shorter than Payment Rule 1; clauses with no graph Rule: webhook secret required, one global configuration no tiers, "decrypted only in memory", "alert admin, retry" on config API unavailable; Screen 1 "Enabled Payment Methods" has no graph field (setting SET-supported-payment-methods); graph has incoming edges from FR-014, 018, 019 not in the Dependencies list.
- FR-015: restored lines carry a link to a FR-029 change-request file (fix at CR removal).
- FR-033: REQ-033-055 says unpublished content is removed "immediately" vs flow A5 step 7 and REQ-033-034 "within 1 minute"; Integration 3 queue-and-sync failure line has no graph Rule; graph screens SCR-033-17..26 (Screens 8-13) have no PRD field tables; processing_status (Screens 5, 5.1) no PRD row.
- FR-003: ENT-inquiry.support_required shown by Screen 12 in the graph has no PRD row; rescued Access Control, Audit Logging, Compliance and Offline Capability lines have no graph Rule; dropped line 'Intelligent provider matching based on capacity and specialization' conflicted with the advisory-capacity rule.
- FR-026: REQ-026-012a..012h are graph ids REQ-026-032..039 (PRD keeps both labels); 17 Screen 5c/Screen 8 rows are graph Setting nodes, not Fields; REQ-026-045 and REQ-026-138 had no PRD sentence outside flows (graph statements appended to the FR Summary).
- FR-011: SC-008 (admin assigns a standalone aftercare request within 24 hours) restored into Business Rules, has no graph Rule; SC-006 (90% of providers respond to escalations within 4 hours) dropped as a metric, no graph Rule; Screen 7 Notes points to 'line 1232-1236' (dangling before compression); 74 screen rows with no graph field; uncited lines with no graph Rule: task types, treatment documentation optional, 'All communications monitored and logged'.
- FR-018: 7 screen rows with an empty Graph field cell (live lines 752, 971, 1097-1099, 1127, 1152), 17 controls; Rules 160, 163, 165 and others cited at nearby non-flow lines because their substance sits in flows; live line 1302 (FR-007/S-02 'calls Payment Service API to initiate Stripe transfers') reads close to FR-017 owning transfers, wording kept.
- FR-017: field-tag choices to review (Payment Type and Method rows tagged ENT-booking.payment_history; filter rows carry the field they filter; graph field affiliate-commission.commission_amount has no clear Screen 6 row); 22 display rows and 42 controls with no graph field; flow-carried Rules 041, 042, 043, 045, 046 cited at nearby lines; restored link in rescued line 1382 points to FR-006 '#key-entities' anchor, which no longer exists after compression.
- FR-022: graph REQ-022-043 cites REQ-034-114 and REQ-032-107 while the PRD says REQ-032-106 (retired) and REQ-032-107; graph REQ-022-059 marks PR-07 messaging P2, PRD says P1; graph REQ-022-094 status list and REQ-022-103 installment statuses older than the PRD (v2.21, v2.20); Maintenance Convention has no graph Rule; FR-022 owns no Screen nodes so all 230 control rows have no graph field; SC-001 and SC-005 restored into Business Rules with no graph Rule; live Source FR table omitted FR-013 Screen 5 and FR-032 Screen 5.7.
- FR-014: SC-001 to SC-009 (task-time targets) sit in Business Rules under "Task-Time Limits" with no graph Rule; decide whether they are rules or UX targets. Restored with no graph Rule: FR-004, FR-005, FR-013, FR-015 data-contract lines, Assumption 6 (patient country legacy fallback), pipeline line (15-minute aggregation, late-arriving events recalculate affected periods). 143 of 259 graph fields have no PRD row (stored-only or non-table widgets); metric rows tagged to graph fields by name; eight lines cited with partial overlap (live L251, L363, L666, L667, L696, L842, L944, L1122).
- FR-032: citations appended to 14 flow lines (text unchanged); five graph fields on SCR-032-04, -06, -07, -08 have no table row; tag judgement calls at live rows 1154, 1197, 1443, 1494; SC-005 (support first response within 24 hours) in Business Rules with no graph Rule.
- FR-012 (independent review): graph node REQ-012-061 still lists "Export conversation" as an option while the PRD and REQ-012-077 defer export.
- FR-012: `ENT-message.admin_badge` and `sent_at` have no PRD row.
- FR-008: `ENT-travel-context.status`, `travel_required` and `ENT-passport-record.status` have no PRD row; REQ-008-047 and REQ-008-072 have weak carriers in the PRD.
- FR-007: remaining balance and payment history fields have no PRD row.
- FR-030: `account.email_change_code` row has no graph Rule; `ENT-notification-template.version_number` has no PRD row.
- FR-010: EC-004 numbering gap; REQ-010-007A and REQ-010-032 state the same rule.
- FR-004: Screen 4 Status cell says "mapped from the Key Entities enum", a section removed by compression.
- FR-006: nine screen rows have no graph field.
- FR-021: Translation Vendor failure-handling line differs from flow E1.
- Several FRs: the Dependencies FR list differs from the graph's cross-FR edges (verify-fr check 3 will flag these).
- `templates/prd-template.md` still has the pre-compression section list.
- FR-005 (independent review): citations at PRD lines 229 (REQ-005-018) and 231 (REQ-005-004) point to rules that do not state the cited clause; the Approvals table lost its two empty placeholder rows and one approval date.
- FR-007B (independent review): four restored clauses (scheduler failure handling, plan provenance, payment method record, FR-029 ownership of the Stripe account and split-payment setting) sit in Business Rules; the scheduler alert has no graph Rule.
- FR-020 (independent review): template management is stated more than once (PRD lines 329 to 334), as it was before compression.
- Graph lint L12: REQ-010-046 and six per-FR pointers to the system 10-year retention rule read alike; merge into one system rule reference or accept.
- FR-038 (independent review): graph nodes REQ-038-052 (7 years) and REQ-038-053 (2 years) contradict the PRD's single 10-year retention period; the dropped open-question check "technical design must validate the final FR-011 request-creation boundary" has no carrier; PRD line 404 cites REQ-038-070 loosely.
- FR-013 (independent review): entity facts are now graph-only (admin action_type values, attested_by and attested_at, ProviderResponse status, removed_at, photo alt text, last_synced_at); REQ-013-002 is cited twice (PRD lines 478 and 479).
- FR-004 (independent review): REQ-004-012 still says "FR-006 provider-fault placeholder" although the owner ruled provider fault on 2026-11-22; four entity clauses are graph-only (baseline lines 782, 785, 786, 792).
- FR-015 (independent review): provider-record attribute facts have no PRD carrier (address, country and avatar copies, availability_status, activation_email_sent_count).
- FR-025 (independent review): REQ-025-065 is worded slightly narrower than the PRD sentence it is cited on.
- FR-008 (independent review): the "No OCR" sentence was trimmed in one place and survives elsewhere.
- FR-030 (independent review): REQ-030-164 says "previous filters preserved" while the PRD (restored) says filters and search context; align the graph statement.
- FR-010 (independent review): "REQ-010-007A" (PRD lines 304, 388, 820) is a PRD-local label, not a graph node (its content is REQ-010-032); the accepted-selection identifier list is graph-only (ENT-treatment-record).
- FR-019 (independent review): graph attributes disagree with the PRD change-log ruling 2.6 (`ENT-promotion-application.status` lists `reversed`; `ENT-promotion-program.application_mode` splits the modes by admin and provider); REQ-019-043 still says "see Key Entities"; eight former success-criteria lines sit as uncited bullets in Business Rules (PRD lines 716 to 723).
- FR-009 (independent review): the audit action names InviteSent, RoleChanged and MemberRemoved are graph-only; the PRD header still reads "Proposed revision (v1.8)" (as before compression).
- FR-016 (independent review): the note that `approval_status` is reserved for a future approval workflow is graph-only; former Assumption bullets (PRD lines 731 to 735) read as rules.
- FR-002 (independent review): PRD line 58 cites REQ-002-039 loosely; REQ-002-018 is cited nowhere; PRD line 210 cites REQ-002-021 for a different subject (as before compression).
- FR-027 (independent review, all present before compression): REQ-014 does not state the admin-set reminder limit; REQ-008 omits the Scheduled status; Screen 4A Document Type omits Cancellation Policy.
- FR-024 (independent review): REQ-024-072, -074, -051 and -052 have their full statement only in the graph.
- FR-001 (independent review): `ENT-patient.flags_alerts` and `ENT-patient.preferred_region` carry no owner text in the graph (owners are FR-016 and FR-021 per the PRD).
- FR-023 (independent review): PRD line 162 states the 30-day deletion completion in the wording of REQ-001-094 (owned by FR-001), not the former success-criterion wording; meaning unchanged. CL-3 (PRD line 156) cites REQ-023-016 for compliance reporting.
- FR-011 (independent review): the baseline line "Patient screens must work seamlessly on mobile devices" was dropped as a design opinion.
- FR-014 (independent review): PRD lines 728, 729 and 1587 still point to dropped sections ("Entity 8", "SC-010", "Key Entities 1 and 4"); the graph fields in the last column carry the entity reference. The reliability and percentage targets of SC-010, SC-012 and SC-013 were dropped as performance targets.
- FR-017 (independent review): Rules 14 and 15, Privacy Rule 2, Billing Rule 1 and Currency Rule 2 carry no REQ citation; whether each has a graph Rule was not checked.
- FR-034 (independent review): Rule 12 (PRD line 764) still says "separate from the success-criteria goals" though that section is gone (wording as before compression); the future-scope note on external ticketing systems (Zendesk, Freshdesk) was dropped; clauses moved from Assumptions and Implementation Notes sit as uncited bullets.
- FR-026 (independent review): PRD line 1042 is a misplaced "Why needed" line about the slot-hold duration under the Analytics seed values; the Graph field ids were not checked against the graph.
- FR-006 (independent review): whether the graph and PRD agree on the installment count in REQ-006-075 was not checked.
- FR-018 (independent review): PRD line 1320 is a stray FR-029 "Why needed" bullet under Business Process Assumptions (duplicates the Currency Rule); REQ-018-167 covers only the failed-payout alert while its citing line also states retry and read-only display.
- FR-022 (independent review): PRD line 1855 cites REQ-022-013 for "patient searches occur during quote request flow", which that Rule does not state; REQ-022-023 does not name the search type and applied filters that the audit log entity records.
- FR-031 (independent review): eight former Assumption bullets (PRD lines 980 to 987) read as rules with no REQ id; PRD line 978 cites REQ-031-057 and line 979 cites REQ-031-050 for clauses those Rules do not state; clock, architecture and integration bullets (PRD lines 996 to 1012) sit under "Data & Privacy Rules"; the System Clock line has no citation.
- FR-029 (independent review): PRD lines 844 to 847 are stray bullets under "Failure Handling and Operational Rules" (placement only); REQ-029-033 has no caller-authentication clause; `ENT-currency-exchange-rate` has only an attribute-list description in the graph.
- FR-033 (compression review): the carried lines at the end of Business Rules (about lines 1105 to 1118 of the live PRD) have no REQ citation; REQ-033-030, cited on the technical-operations line, does not cover its ownership wording. Decide at Phase 10 whether these become Rules or stay uncited prose.
- PRD field rows tagged with a graph field retired on 2026-11-20 (found by the Phase 9 graph cross-check): FR-005 line 195 `ENT-provider.credentials_summary`; FR-026 lines 797 and 798 `ENT-support-emergency-contact.phone` and `.email`; FR-032 lines 1438 and 1489 `ENT-support-case.case_type`. Retag each row to the field that replaced it, or remove the row if the ruling removed the field. Settle in Phase 10.

### Added 2026-11-23 from the FR-005 logic review (Phase 10 pilot, round 1)

- **Data home for a patient-entered promotion code before acceptance (FR-005, FR-019).** The code and its discounted price are bound to `ENT-acceptance-event.promotion_code` and `.discounted_price`, which exist only after acceptance. REQ-019-039 says the code is "recorded against the patient's selection on that subquote", but no entity holds it between entry and acceptance. Provide one (for example a selection draft record). Source: reviewer B finding N6.
- **No Step for "Contact support" after no eligible subquote is left (FR-005).** The PRD names the action; no FR owns a step for it.

### Added 2026-11-23 from the FR-006 logic review (Phase 10, two passes)

- **FR-006 Screens 8, 9 and 11 fields have no Field nodes** (Installment Plan Outcome, Refund Amount rows). Add them in the graph.
- **28 FR-006 rules still have no applying step** (list in `plans/reports/docs-manager-261123-fr006-logic-p1-fixes.md`). No behaviour gap found in pass 2; link steps when the graph is next extended.
- **REQ-006-014 graph text differs from the PRD wording** (pre-existing). Re-sync the node text.
- **Clinic charge in the pending provider-fault window** is not stated. Payment is blocked from the fault, so only an earlier charge can exist; the Screen 10 refund covers it. Confirm when payments are built.

### Added 2026-11-23 from the FR-007 logic review (Phase 10, two passes)

- **FR-007 rules with no step:** REQ-007-065 and REQ-007-087; REQ-007-014 (commission order) and the clinic withdrawal charge in REQ-007-092 are only partly covered; the reschedule share movement in REQ-007-091 has no step.
- **Late fee on a full refund** is not stated (REQ-007-063). Decide when payments are built.


### Added 2026-11-23 from the FR-007B logic review (Phase 10, two passes)

- **Installment build items the PRD now requires:** pause later installments on a Defaulted plan; one void step that also handles a charge already in flight; a second-approval record for Mark as Resolved (bank transfer with amount, date, reference); plan snapshot columns for late fee, grace period and cancellation point; a once-only catch-up charge for paused past-due installments when the plan returns to Active; cancel pending retries on a hard decline.
- **Known approximation:** the single void step (STP-007B-701) serves the B2, B4 and B8 cases, so the provider notice after it is reachable from all three. Check when the flow is built.

### Added 2026-11-23 from the FR-029 logic review (Phase 10, two passes)

Source: `plans/reports/docs-manager-261123-fr029-logic-p1-fixes.md` and `plans/reports/docs-manager-261123-fr029-logic-p2-fixes.md`; PRD `local-docs/project-requirements/functional-requirements/fr029-payment-system-config/prd.md` v1.18.

- Screen 7 (refund, fees and settlement): Not set states for the cancellation point, Hairline's share, late fee, rescheduling fee and clinic deduction; fixed amounts above 0; range and ordering checks (balance due days 1 to 30, cancellation point 1 to 30 and smaller than balance due days and the cutoff, window 1 to 30, cutoff day and payout day differ); a non-blocking warning when the cancellation point falls before the late fee day; amounts stored with their currency code; save blocked after a Default Currency change until each fixed amount is re-entered.
- Dashboard banner for holders of the Screen 7 permission while Hairline's share is Not set; clears on save.
- Screen 4 (installments): grace period starting at 0; the minimum booking lead time (cutoff plus 30 days) always shown, with a warning above 60; counts that do not fit are not offered; the retry end day read from FR-007B for the warning.
- Screen 6 (currencies): block disabling a currency in use as the Fee Currency or as an active account's Default Currency; the "Manage Supported Currencies" flow.
- Screen 2B (rate protection): the Acknowledge action (logged); compare with the rate at acknowledgement until back within the threshold; no check for 24 hours after a mode switch or pair creation.
- Screen 3 (provider deposit overrides): "Reset to global default" in place of delete.
- Quote acceptance: store the full rate set (base rate and markup with timestamps, for the quote currency, the shown currency and the Fee Currency); a locked rate set survives deletion of its currency pair; markup applied once on the shown pair; installment eligibility uses the base rate.
- Stripe routing: Archived account status and delete block while bookings or plans use the account; Inactive or Archived accounts' countries treated as unassigned (Global Fallback, else B6 block); Live accounts only on production, Test elsewhere; routing returns when the next connection test passes; the routed account stored on the booking and used for every later charge and refund; USD fallback when the account does not support the booking currency; payment methods checked against the charge currency.
- B6: profile country prompt with no alert when none is set; unsupported-country alert de-duplicated to once per country per day.
- Booking confirmation (FR-007): store the balance due date and the locked Screen 7 values on the booking.
- The account Default Currency has no consumer yet; confirm its use before building it.

### Added 2026-11-23 from the FR-010 logic review (Phase 10, two passes)

Source: `plans/reports/docs-manager-261123-fr010-logic-p1-fixes.md` and `plans/reports/docs-manager-261123-fr010-logic-p2-fixes.md`; PRD `local-docs/project-requirements/functional-requirements/fr010-treatment-execution/prd.md` v2.14.

- Check In: compare the date in the booking's appointment timezone. There is no upper limit, but a check-in after the appointment date shows a late check-in prompt and raises an admin flag. The block reason names Defaulted plans.
- End Treatment: allowed only when every day is Finished, Cancelled or Deferred and at least one is Finished. "Need caution" counts as finished and cannot be resumed. The admin End Treatment button on Screen 8 uses the same gate. Plan days, clinicians and the estimated graft count lock at End Treatment.
- End Treatment save marks completion, starts the FR-007 confirmation window and sends the completion signal to FR-006 and FR-011. On a failed signal the case keeps an admin flag, and Screen 8 shows a Retry button.
- New treatment record status "Closed Early" for an admin early close with no provider fault (FR-006 Screen 11). It stops documentation reminders and the overdue flag, hands the case to FR-011 aftercare from the decision date, and makes the provider's share eligible for payout on the decision date after the admin-set refund.
- Admin can record a provider fault from Screen 8, with a mandatory, audited reason.
- Documentation deadline runs from when End Treatment becomes available. The reminder must be earlier than the deadline (range check), and its default is 6 hours.
- Screen 7 lists every case status, with a Case Status filter, a Flag filter and a Flags column (late check-in, failed signal, overdue documentation, close request). Screen 8 opens for any status.
- Events use the dotted FR-030 names. `treatment.cancelled` fires when the record becomes Cancelled.
- The no-show report has no fixed wait. No-Show is an admin case label only.

### Added 2026-11-24 from the FR-004 logic review (Phase 10, two passes)

Source: `plans/reports/docs-manager-261124-fr004-logic-p1-fixes.md` and `plans/reports/docs-manager-261124-fr004-logic-p2-fixes.md`; PRD `local-docs/project-requirements/functional-requirements/fr004-quote-submission/prd.md` v4.4.

- Provider Withdraw on the quote detail screen: for a sent quote before acceptance, and for an accepted quote while the booking is Accepted or Confirmed, before Check In, with no provider-fault marker. A confirmation names the consequence (the booking goes to the admin for a transfer or refund) and a reason is required. An ineligible accepted quote shows no Withdraw and a short note. The after-acceptance withdrawal emits `quote.withdrawn`.
- Provider-fault freeze: while the marker is pending, every field of the accepted quote except admin notes is locked for provider and admin, and a second withdrawal is blocked.
- "Active acceptance" is the latest acceptance with no supersession record; the original accepted quote keeps its status after a transfer.
- Replacement quote (admin Screen 8): saved as a draft, hidden from the replacement provider and the patient until accepted, not on the provider list or the admin quote edit screen, no expiry. Currency is captured at the first save, shown, and fixed. Screen 8 is blocked with a message when a precondition fails. When FR-005 records the replacement acceptance, the system moves it to sent and accepted, sets the first-send time, keeps the original's status and silently cancels other open replacement drafts. Closing or cancelling the inquiry cancels an open replacement draft with no provider notice. A draft auto-archived after 7 days must be re-authored.
- The cancel-other-quotes cascade runs on patient acceptance only.
- Admin archive and restore: archive releases the promotion reservation; restore takes a new one only when none is held, and is blocked when the promotion is used up or ended. Restore is offered only for an expired quote or a quote archived from draft or sent, and only while the inquiry is open, the provider is Active, and there is no active acceptance and no provider-fault marker; a failed guard shows a message naming it.
- Providers can soft-delete drafts only; drafts auto-archive 7 days after the last edit.
- Expiry and expiring-soon events fire once per expiry window.


### Added 2026-11-24 from the FR-002 logic review pass 2

Source: `plans/reports/docs-manager-261124-fr002-logic-p2-fixes.md`; PRD `local-docs/project-requirements/functional-requirements/fr002-medical-history/prd.md` v1.7.

- Head scan quality score: define it as the lower of the brightness score and the blur score (each 0 to 100), the same on the device and on the server, and have FR-026 hold one minimum per measure. FR-002 still says one 0 to 100 score is compared with the FR-026 thresholds (REQ-002-034, REQ-002-050); the PRD wording is not changed until FR-026 is aligned.

### Added 2026-11-24 from the FR-020 logic review pass 2

Source: `plans/reports/tester-261124-fr020-logic-p2.md` finding P2-13; PRD `local-docs/project-requirements/functional-requirements/fr020-notifications-alerts/prd.md` v2.18.

- SMS path (post-MVP): define what makes a notice "urgent" (REQ-020-037, STP-020-005) and who sets `ENT-notification-record.urgency`, when SMS enters scope. Today the Urgency badge is display only (REQ-020-158).
- `booking.provider_fault_replacement` row lists "drops out before treatment starts", which overlaps the provider drop-out at the FR-006 Screen 10 submit that sends `booking.cancelled`; settle with FR-006 and FR-030 in the cross-FR pass.

### Added 2026-11-24 from the FR-013 logic review pass 2

- FR-014 (about prd:423) still says rating aggregates use "Published reviews only"; FR-013 now counts Published and Flagged reviews. Align FR-014 when it is reviewed.
- The provider notice sent when an Admin removes a provider's response (FR-013 REQ-013-017, STP-013-083) has no notification catalogue row yet in FR-030 or FR-020.
- An Admin edit made outside "Resolve flag" leaves the flag open: confirm during implementation.

### Added 2026-11-24 from the FR-035 logic review pass 2

- STP-035-056 should be done by the system actor (graph edge swap).
- REQ-035-024 and the not-logged-in help lines still say "phone and email"; they should say "whichever is set".
- A reply whose attachment cannot be scanned: the file is refused with a try-again message and the reply can go without it; confirm during implementation.
- A second support request submitted while one waits offline is refused with a wait message; confirm during implementation.


### Added 2026-11-24 from the FR-028 logic review pass 2

- STP-028-413 (A5, "displays all available destinations in the default order") has no cap step; the cap step STP-028-429 is on the main path only. Add the cap to the A5 path or reword 413.
- No step covers the "Show all destinations" expansion; the prices of the destinations behind it are fetched by no step (STP-028-407 covers each displayed location).
- STP-028-306, 504, 514, 154 and 114 have no stale-edit warning (REQ-028-082 is only on 105, 208 and 317).
- The chain puts the one system-wide default amount before the destination's own converted price (REQ-028-040 step 3 before step 4), so a single amount can show for every destination. Original design, left as is.
- The bulk actions "duplicate grouping" and "import from template" (REQ-028-077) are not tied to the 51st-grouping warning or to the one-country rule; a duplicate copies its countries into a second active grouping.
- Messages differ between flow and user stories ("Changes will be live for patients within 1 minute" versus "within 1 minute"; "Starting price for [Location] in [Currency] set to [Amount]" versus "Starting prices for Turkey updated for 3 currencies", which implies a three-currency batch save no flow has).
- A4 and Screen 2 enable bulk update when at least one row is checked, but the flow selects one destination; with rows from several destinations "[Location]" in the confirmation is undefined. Fallback rows (several per currency) cannot be shown in a per-currency preview table.
- A currency disabled in FR-029 after prices exist: FR-028 does not say whether price rows, a location default currency or the system-wide default in a disabled currency still apply.
- FR-029 says an Inactive or Archived Stripe account's holdings are "ignored for routing"; REQ-028-091 blocks while an account is "assigned" and does not say whether an inactive account still blocks.
- Schema note for the P2-08 fix: ENT-pricing-default holds one record per destination default currency and one system-wide record, told apart by default_type; a split into two entities is possible if the data model owner prefers.

### Added 2026-11-24 from the FR-037 logic review pass 2

- The assignment end cause value `reassigned` cannot occur while Assign Provider is allowed only in pending states; drop it or define when it applies.
- The assignment-ended notice on completion or conversion may duplicate the completed and converted notices; settle the final copy in technical design.
- Resuming a kept conversion draft rebuilds the carried-over values and may overwrite edits the patient already made in the draft.
- The audit entry (REQ-037-026) needs a case id, but an advice-cadence change is global.
- The routing rule's "withdrawn or not eligible" case overlaps "no provider assigned".
- The provider is not told when an advice window opens.
- The PDF copy already attached to the inquiry is not refreshed after a later Admin correction.
- The active-inquiry check is not repeated when a kept draft is resumed (FR-003 refuses at submit).
- Events are emitted by stage nodes, so no step shows which event it sends.


### Added 2026-11-24 from the FR-030 logic review pass 2

- `aftercare.escalation_triggered` is a clinical red-flag alert that is now switchable and not locked; whether it should be locked is not decided.
- A held notice (quiet hours or rate limit) has no maximum age; a switchable time-sensitive notice such as `booking.appointment_reminder` or `quote.expiring_soon` can arrive after its moment. Skip If Too Late only acts at scheduling.
- Two appointment reminders (7 days and 1 day) need two timings for one event, but the overlap refusal and the single seeded Active rule per event do not obviously allow a second rule for the same recipient type and channel; how the second timing is configured is not stated.
- `ENT-notification-delivery-log` and its fields stay in the graph; its status values (sent, delivered, failed and so on) differ from the FR-020 attempt statuses and need a mapping.
- Event On or Off when rules are only Paused or Draft (no Active rule) is not covered.
- Escalation Wait Time has no minimum tied to the retry window (retries times interval).
- The shorthand "locked (critical)" still appears in several lines; it is correct for every locked notice except `legal.acceptance_reminder`, which the definition now names.
- Not checked in this pass: manifest sections other than Flows, template variable allowlists, REQ-030-003 and REQ-030-004 against the FR-020 first-attempt target.


### Added 2026-11-24 from the FR-012 logic review pass 2

- Supply the starting keyword list before go-live: the list starts empty, and with no words no keyword flag is raised (P2-10).
- SET-escalation-routing-rules has no consumer: nothing records who receives the keyword alert and the 72-hour flag (P2-11).
- SET-conversation-export-controls belongs to a future phase because conversation export is deferred (P2-11).
- SET-emergency-intervention-permissions is queued for FR-031 (P2-11).
- STP-012-033 stays retired with its dangling next edge (P2-11).
- A session that is open when a conversation turns read-only is not described; the session simply cannot be started on a read-only conversation (P2-08).
- Audit term drift: flag resolved in REQ-012-010 and flag_status_change in the graph name the same event; the change-log row of the previous version still contains a removed phrase; steps and rules still sit at STG-main-02-quote except REQ-012-098.

### Added 2026-11-24 from the FR-019 logic review pass 2

- Revive, supersede and refund steps are not in the graph flow.
- A 100 percent percentage discount (possible if the maximum-discount setting is raised) has the same zero-price issue as P2-04, which was ruled for fixed amounts only.
- EVT-promotion-approval-requested and EVT-promotion-discount-approval-requested overlap in their descriptions; left for FR-030.
- The graph flow has a reachable loop (STP-019-004, -021, -025, back to -004); lint has no cycle rule, so confirm the loop is intended.

### Added 2026-11-24 from the FR-021 logic review pass 2

- Group-scoped partial bundles versus the singular "latest published bundle" (Rule 14, REQ-021-059); revalidation trigger and polling interval undefined (REQ-021-113).
- Stale window and import size limit have no owner, screen or value.
- Translation key status is key-level while statuses are per locale; translation value and version status fields are free text.
- "Change reason", "publish summary" and "change summary" name the same input in different places (REQ-021-087, REQ-021-102).
- No inactive-locale rule for admin users; Screen 1 Region label reads like a currency selector; missing-translation logging has no volume cap.
- `ENT-locale.review_needed_count` keeps one calculated-by rule (REQ-021-020); the Screen 9 count has no second rule link.
- Screen 10 has no control to mark which provider is used for free-text translation; left to design.
- The free-text panel has no graph step; whether an Active right-to-left locale needs a rule against REQ-021-057 is open.

### Added 2026-11-24 from the FR-024 logic review pass 2

- Base Price "required if offering" versus REQ-024-060.
- REQ-024-072 repeats the confirmation sentence, and the case of zero affected quotes is unclear.
- A permission bullet in the PRD names no actor.
- Renaming a treatment type versus its historical versions is not stated.
- Discard Draft is an action on Screens 1 and 4 and a rule (REQ-024-057) but has no workflow step.
- The two new treatment fields are linked to their rules with `applies to`; the graph allows reads and writes only between a Stage and an Entity.
- Security review note: drafts do not count toward the hourly package creation limit (REQ-024-078, REQ-024-098), and no draft cap or draft expiry exists, so a provider could create unlimited drafts. Owner to decide whether to add a draft cap; logged with defaults 204 and 205.

### Added 2026-11-24 from the FR-008 logic review pass 2

- 18 FR-008 rules still have no step: REQ-008-029, -035 to -039 (future phase), -040, -041, -043, -045, -063, -068, -070, -075, -077, -078, -079, -082. The tester counted 25; the recount gives 24 before this pass (REQ-008-083 was already attached) and 18 after it. The rest need a step that does not exist; none was invented.
- FR-006 cancel routes STP-006-502 and STP-006-902 still do not reach STP-008-029; only STP-006-303 was linked.
- STP-008-029 next STP-008-030 ("Replacement booking confirmed") is specific to the provider-fault transfer; after a plain cancellation the flow ends at STP-008-029 without a condition on that branch.
- No step carries the hand-off at Completed (provider passport access ends); it is stated as a rule only.
- Screen 6 status badges still read Awaiting for items when the patient has declared no travel (the declaration shows on Screen 10 only).
- Who is asked again for the early-departure acknowledgment after a reschedule is not ruled (the PRD says "asked again").
- Carry-over when the replacement booking includes different services on the same path is not ruled.
- Pass 1 leftovers stay: reversing a Not-needed mark, Overall Status of a closed TravelContext, Path A one-way flight, STP-006-208 next edge, early-departure warning with a Not-needed return flight.

### Added 2026-11-24 from the FR-016 logic review pass 2

- The Overview tab has no separate bookings panel or booking-status field in the PRD or graph; the "Cancellation failed" mark is stated on the patient's Overview tab without adding a field or screen. A field for it is a design step for a later change.
- The Screen 8 default filter shows only Pending Admin Review, so Verification Required and Denied requests are visible only after the filter changes.
- REQ-016-201 and REQ-016-220 stay pinned at the active-patient stage although the patient is Suspended (accepted early-stage leftover).
- US5 AC4 and Rule 10 say "suspend account" with no reference to the duration step of Flow A6; Take Action reuses the A6 flow, which asks for the duration.
- The Operational and Security Rules line says failed refunds are retried automatically; FR-007 was not checked for the same rule.
- Step prd_ref values of the graph were corrected only where this pass changed the step numbering (STP-016-081, STP-016-082); the other suspension and deletion step references were not rechecked.
- The enum value `deactivated` of ENT-patient.account_status remains until FR-001 is reviewed (owned by FR-001).
- FR-005 quote behaviour for a suspended patient beyond the stated rule (open quotes follow their own expiry) was not checked.

### Added 2026-11-24 from the FR-009 logic review pass 2

- A Suspend requires a reason in the shared modal, but where a suspension reason is stored is not named.
- A Manager can resend an Expired invitation for the Manager role (A2 has no role limit), although cancelling is limited.
- A6 self-removal by the Owner can only be reached through the API (the Owner row has no Remove button).
- The A3 error tells the inviter that an email belongs to another provider team (accepted trade-off against Privacy Rule 1).
- FR-009 rules and steps stay pinned to the active-provider stage, except those on the configuration and offboarded stages (accepted early-stage leftover).
- Neighbour sides still open: FR-004 and FR-010 clinician lists rewritten on suspension, role change and admin actions; FR-015 Owner login email controls and the deactivation trigger; FR-030 and FR-020 events for Reactivate, Cancel Invitation and Owner handover; FR-031 Manager role-change row.

### Added 2026-11-24 from the FR-033 logic review pass 2

- Eight Publish Status rows in the FR-033 screens still say "Dropdown offers Draft and Published only".
- The virus-scan step STP-033-165 is a parallel branch: the direct edges 148 to 149, 151 to 152 and 041 to 042 are kept, and STP-033-007 attachments and thumbnail uploads are not wired to the scan.
- The patient video upload shares step STP-033-041 with the admin upload.
- 44 FR-033 rules have no applying step (pass 1 leftover).
- Neighbour sides still open: FR-035 (video description maps to `summary` and is optional; article excerpt comes from `body`); FR-032 (Screen 5.7 fourth value "Status not available"; counters, Resource Category filter, vote and view write paths); FR-031 (Help Centre permission covers providers and patients).

### Added 2026-11-24 from the FR-034 logic review pass 2

- "Support Staff" is both an FR-031 role name and the FR-034 notice pool (all active admins holding Respond to Support); the name can mislead.
- REQ-034-171 and REQ-034-172 are missing from the FR summary list in the PRD.
- Root Cause and Resolution Category are "for analytics", but the analytics view REQ-034-072 is retired.
- The Urgent threshold minimum of 1 hour equals the fixed 1-hour alert, so the alert and the escalation can fire together.
- The per-provider-user throttle (REQ-034-176) has no submitter-user field on ENT-support-case; only provider_id is stored.
- Edit Case is enabled for all statuses, against the archive step for Closed cases; reopen templates may be deleted against "cannot delete while in use".
- SET-support-case-auto-closure-period has no Screen 7 control; the timeline actor_type enum has no "system" value; the REQ-034-148 graph statement lacks the permission filter on Assign To.
- Neighbour sides still open: FR-030 (three catalogue events: Urgent 1-hour alert, orphaned-case notice, manually-contact alert; EVT-support-case-escalated description); FR-006 and FR-035 (Contact Support on the Payment Window Expired and Cancelled screens passes the booking reference, no request type); FR-032 (Provider Priority Update on Screen 5.9 dropped by flow B3a); FR-031 ("within 24 hours" without "business days").

### Added 2026-11-24 from the FR-015 logic review pass 2

- The provider status event requires `admin_id`, but a scheduled change applied by the midnight job has no acting admin.
- Screen 3 says write actions "allowed below" apply only to an Active provider, but no list of allowed write actions follows.
- The cap of 10 featured providers is checked only on the list quick action and the Tab 1 toggle.
- Commission Start Date "today or a future date" is validated by UTC date, not the admin's local date.
- The Screen 4 affected list shows no count of monitoring cases ended by the cascade.
- FR-038 does not mention provider suspension or deactivation.
- Stage pinning of the closure-request steps (STP-015-171, 172, 176) is an accepted early-stage leftover.
- Neighbour sides still open: FR-017 (the admin financial resolution route must also release earnings on normally completed bookings of a Suspended or Deactivated clinic, default 253); FR-032 (REQ-032-074 and REQ-032-076 "remains Active" should read "keeps its current status"; a Suspended clinic can set its password from the activation link); FR-013 (review actions in Tab 5 for a Deactivated provider); FR-031 (Reject Request under Suspend Providers); FR-009 (pointer that Owner handover applies the FR-015 login-email steps).

### Added 2026-11-24 from the FR-026 logic review pass 2

- The direction of the blur and brightness scores is not stated (FR-002 is silent on it).
- An admin who lowers the session limit may have their own session ended by the change.
- The seeded countries (Turkey, UK, USA, Germany) have no flag assets.
- Retired validation steps keep their own outgoing `next` edges in the graph.
- The provider creation rate limit is not shown on Screen 8.
- The timezone seed lists whole-hour offsets only.
- The "Limits owned by other features" rows state no range.
- Minor wording: "immediately" beside a 60-second propagation; Profile Photo size and format ranges; the screen placement of STP-026-077; the Acceptance Terms Text permission against FR-031 and FR-027.
- Neighbour sides still open: FR-001 (counter reset sentence, REQ-001-125 timezone wording, re-verification range, duplicate OTP setting stubs); FR-021 (REQ-021-126); FR-031 (permission names, session wording in REQ-031-099, throttle wording); FR-035 (REQ-035-040 hide the section when blank); FR-002 (score per photo against two minimums); smaller pointers for FR-004, FR-005, FR-006, FR-009, FR-015, FR-028, FR-029.

### Added 2026-11-24 from the FR-018 logic review pass 2

- The readiness field exists twice (ENT-affiliate-payout.payout_readiness in FR-018, ENT-affiliate-commission.payout_readiness_status in FR-017) with no edge tying them.
- Readiness is described for the affiliate's unpaid commission but stored per payout or commission row; rows accrued during a suspension are not named.
- Screen 2 Edit and Screen 3.2 have no status condition, so an Inactive affiliate's commission and bank details appear editable.
- REQ-018-301 allows a fixed commission of at least $50 per booking; the $50 floor may be a copy of the payout threshold.
- "Incomplete payout setup" as an ineligibility reason is unreachable because all bank fields are required at onboarding.
- "Total Referrals" is defined as completed bookings, yet A3 lists the two as separate counts.
- "Real-time" on dashboards sits beside a 5-minute refresh; receipt availability is Paid-only on the affiliate side and unconditional on Screen 8.
- FR-017 and FR-018 show different code status sets; no graph field holds the stored initial code settings.
- Stage pinning of the Inactive steps in B5 and B6 is an accepted early-stage leftover.
- Neighbour sides still open: FR-017 (Inactive affiliates in the payout run with no threshold, hold cleared on a normal offboarding, Screen 6); FR-019 and FR-005 (capture honoured only when the affiliate is Active at acceptance); FR-020 and FR-030 (Pending affiliate offboarded: activation email and link-no-longer-valid message); FR-029 (affiliate discount wording against the shared model); FR-031 (permission to override the commission ceiling); FR-007 and FR-007B (name the fully-paid payment event).

### Added 2026-11-24 from the FR-001 logic review pass 2

- A successful password reset on a never-verified email does not mark the email verified.
- An admin email change is not among the session-ending events of REQ-001-182.
- STP-001-003 hands off to STP-027-011: confirm in FR-027 that it is the same prompt as the Screen 3 checkbox.
- REQ-001-098 and Screen 18 fix "15 minutes" while Screen 5 says configurable; the SET-reverification-threshold description names Screens 16 and 18 only.
- B3 gives no order between a Locked account and an unverified email.
- The Screen 5 Help entry is not shown after the wrong-code limit is reached.
- Four events have no reader: EVT-patient-account-locked, EVT-patient-password-changed, EVT-patient-profile-changed-by-admin, EVT-reauth-otp-sent.
- Stage pinning of early steps and rules, including the registration-time code step, is an accepted early-stage leftover.
- Neighbour sides still open: FR-023 (fulfilment step states sessions end, old credentials get the standard message, the email is free); FR-016 (email verified and email change pending on the patient Overview; auto-unlock may read the new lock fields); FR-026 (unused stubs SET-otp-validity-window and SET-otp-resend-rate-limit).

### Added 2026-11-24 from the FR-031 logic review pass 2

- FR-007B: replace the role list in REQ-007B-090 and "billing admin" in REQ-007B-081 and REQ-007B-109 with the Resolve Installments permission (REQ-031-135).
- FR-007: REQ-007-015 says "billing permission" and escalates to a super-admin; align with Issue Refunds and the single-holder rule (refunds blocked until a second holder exists).
- FR-032: name the gating FR-031 permission in each row of its who-edits-what table (being done in the FR-032 pass 2 fix).
- FR-026: the "Acknowledge role change" banner belongs to the admin shell; no dashboard screen node exists, so STP-031-214 and STP-031-215 have no screen.
- FR-030: the provider role sync-failure in-app alert (A4) has no catalogue entry.
- An Invited account is removed only with Cancel: carried by REQ-031-126, no graph step.

### Added 2026-11-24 from the FR-032 logic review pass 2

- FR-009: account setup must write the default Account Name; ENT-team-member.phone_number description still says "optional on Screen 6" although the phone is required.
- ENT-provider-account-settings.last_updated_at and ENT-team-member.password_changed_at have no writer step (STP-032-093 should set the second).
- SCR-032-08 title still says "(Owner only)"; the new title is "Billing Settings (Owner edits, Billing Staff views)", and access is the permissions View Billing Settings (grantable, default Owner and Billing Staff) and Edit Billing Settings (Owner only).
- The phone-only and timezone-only alternative flows (STP-032-099, STP-032-102) do not reach the audit steps STP-032-337 and STP-032-338.
- STP-032-307 and STP-032-321 share a title.

### Added 2026-11-24 from the FR-017 logic review pass 2

- Commission on the clinic's share of a cancellation fee is not stated: REQ-017-200 does not say whether Hairline commission is taken from the share.
- No admin control raises the payout flag of REQ-017-161; only the system flags a payout over 2x the clinic's average.
- Not stated whether Mark as Paid is blocked while a statement is flagged Manual Review Required (Approve and retry are).
- Screen 7 states no re-authentication for Release Earnings, so the one-off statement is Approved by the admin's release decision with its note and audit entry; add re-authentication only if the owner wants it.
- Where the provider-status hold sits in STP-017-087 (at the window end) is unchanged; a provider-status cancellation has no confirmation window either.
- ENT-provider-earning.payout_status has no value for a held earning or for Waiting for clinic setup.
- REQ-017-123 provider payout history omits Waiting for clinic setup.
- Release Rules 5 and 6 (share moves 60 or 30 days before treatment, pull back on cancel or reschedule) have no steps in the graph (early-stage pinning leftover).
- STP-017-008 "invalid bank account" is on the Stripe path while the readiness values missing and invalid bank details are manual-rail words.
- Affiliate payout (Screen 6, REQ-017-197, REQ-017-198) has rules and edges but no graph steps.
- Payout flag check is wired from the statement calculation, the release steps and the admin release step; the cancellation fee share, Pay Now and one-off statement payouts are not checked by it.

### Added 2026-11-24 from the FR-011 logic review pass 2

- Screen 1 has no stated entry to Screen 7 for Cancel Subscription.
- FR-006 REQ-006-060 lists two exits to Completed ("aftercare complete / final review submitted"); whether a submitted review before plan completion can complete the booking is FR-006's to settle.
- STP-011-062, STP-011-001 and REQ-011-014 stay pinned on the early platform stage STG-main-07-aftercare.
- STP-011-039 (team contacts the patient) does not stop the 2-hour urgent clock; only clearing the flag does (now defined).
- Paperwork-only completion closes the opened setup row with no plan, so an add-on stays allowed afterwards (REQ-011-056, REQ-011-092); this is the fixer's reading, not an owner ruling.

### Added 2026-11-24 from the FR-014 logic review pass 2

- Fixed here from the minor observations: the export generation time on Screen 6 now matches Rule 18 (PDF under 60 seconds, CSV under 30 seconds).
- Screen 1 is layout locked: only the C3 snapshot note and drill-down destination wording changed there.
- Classification used for default 327 (confirm in the next pass if wanted): active cash risk, being a Section C widget, is gated by View Financial Dashboard, not View Payouts.
- Not changed: Screen 4 Widget 8 Period column versus Connect per-booking payouts; Screen 2 Widget 2 "list of quoted inquiries for that treatment" (the FR-003 list has no treatment filter); the REQ-014-004 cross-filter note; Rule 16 (3-second budget) against live reads; partial-widget loss in recurring exports; the registered email in a recurring export gets no permission check; FR-006 and FR-010 drill-down filters; the graph statement of REQ-014-186 still carries the old "successful deposit or first installment charge" wording; alternative flows without next edges; stage pins.

### Added 2026-11-24 from the FR-022 logic review pass 2

- Wiring (P2-13): the hourly-limit and timeout steps sit on the inquiry stage only; the graph lint rule allows one stage per step.
- FR-014 Screen 1: the owner header lists Time range and Country; FR-022 still lists a Treatment Type filter, kept because no ruling removed it. FR-014 to confirm.
- FR-005 Screen 1 (REQ-022-069): the sort rule names Not Selected, Expired, Withdrawn and Cancelled as last; the owner State list also has Accepted and Superseded, whose position is not stated.
- FR-007 Screen 5 (REQ-022-091): Date Range says "Filters by booking date"; FR-007 does not state its date filter, so it was not changed (the FR-006 table was aligned to Appointment Date).
- FR-013 Screen 7: Review Status offers Published and Removed; the enum also has flagged, covered by the Flagged toggle.
- FR-033 lists: the owner describes an admin-only Archived filter used for restore; FR-022's default of All may show archived items in the live list. The owner gives no default.
- REQ-022-123 applies at the patient and provider stages and not at STG-admin-02-operations, although it is an admin screen; REQ-022-145 follows the same early-stage pinning as its neighbour REQ-022-113 (accepted leftover from pass 1).
- The hourly-limit decline (STP-022-052) has no stated user-visible message, unlike the timeout.
- Master Reference Table has no stated counts, so none were updated; the Requirements Summary lines were not rechecked.
- Not checked: FR-012 Screens 1, 3 and 5 against their owner, FR-030, FR-032 Screens 5.2 and 5.4, FR-035; the FR-006 "At Risk" and FR-007 neighbours beyond the rows cited. FR-014 Screen 1 is now compared with its PRD (v3.23), not the graph row.

### Added 2026-11-25 from the cross-FR pass

Follow-ups are items a batch found for an FR outside its own set; leftovers are queued rows closed as not changed. Source: `logic-review-ledger.md`, section "Cross-FR pass (2026-11-25)".

**Batch B, follow-ups**

- FR-016: the Admin Platform Role Model line names the default roles "Billing Staff"; FR-031 calls the admin role Billing Admin (REQ-031-004).
- FR-016: "Retry Payment" and "Send Payment Reminder" say they use the same access as Retry Charge; FR-031 keeps two permissions (Retry Charge, Send Payment Reminders) with identical default holders. Reword to name both permissions.
- FR-017: name the permissions behind its role wording: Process Payouts for the payout actions, and a read-only finance permission (View Transactions is the natural fit, not decided here), instead of the role names Billing Admin and Super Admin (REQ-017-047, REQ-017-017).
- FR-022: Privacy Rule 2 (REQ-022-140) says the search audit log is read on the FR-031 admin audit trail, but FR-031 Screen 5 shows access-control events only (REQ-031-132). Reword to say the log is kept for the same period and name where it is read once decided.
- FR-009: confirm the provider permission mapping for treatment pricing and packages uses the FR-031 names Manage Treatments and Manage Packages (line 1543, FR-009 side).
- FR-011: optional, name the FR-031 permission each admin Screen 13 to 19 action needs (View Aftercare Cases, Manage Aftercare), as FR-031 now only names the screens.

**Batch B, leftovers**

- Line 2823 (FR-022, FR-031): no place exists to read the admin search audit log; naming one needs a new view or an owner decision on whether Screen 5 may list it.
- Lines 2603 and 2618 (FR-031, FR-026): the role-change banner has no owning screen node because the admin dashboard and shell are not specified in any FR; FR-031 states the banner on every admin page.

Batch B applied in commit `f592158`.

**Batch C, follow-ups**

- FR-004: REQ-004-111 still carries the replacement-provider carve-out for `quote.cancelled_inquiry`; an admin cancel or close now sends it to no provider (FR-003 REQ-003-127, REQ-020-020).
- FR-006: REQ-006-082 (Close inquiry) should state that the close sends no provider notice.
- FR-016: the ledger rows asking to remove `deactivated` from ENT-patient.account_status should follow FR-001 REQ-001-188 (kept as a reserved value).
- FR-026: of the minor observations at line 2307, the "immediately" in main flow step 16 against 60 seconds on Screen 2, Acceptance Terms Text permission against FR-031 and FR-027, Profile Photo size and format ranges, STP-026-077 screen placement and the "Impact preview" wording belong to FR-026 or other owners.
- FR-014: the drill-down rows can rely on FR-003 REQ-003-124 (stage, country and an inquiry date period pre-applied); a response-time column is not provided.

**Batch C, leftovers**

- Line 1717 (FR-001): remove `deactivated` from ENT-patient.account_status. Not changed; FR-001 keeps it as a reserved value (REQ-001-188) and FR-016 states the value stays.
- Line 2633 (FR-003): optional response-time column on the provider inquiry list. Not changed; new scope.
- Line 2652 (FR-003): same item as 2633. Not changed.

Batch C applied in commit `cbc51f8`.

**Batch A, follow-ups**

- FR-034: Notification Rule 3, REQ-034-092, REQ-034-108 and REQ-034-113 call the urgent alert, orphaned-case notice and failed-notice alert fixed plain system emails; they are now configurable catalogue events (REQ-030-258 to REQ-030-260), so the FR-034 wording should point to them.
- FR-001: confirm whether a password-changed or account-locked notice exists; FR-001 states none, so FR-030 added no row (ledger line 2198).
- FR-007B: confirm Patient as the recipient of `installment.charged` and `installment.plan_completed` (ledger line 648).
- FR-016: its other patient notices (suspension, suspension end, password reset by admin, manual and bulk notices) have no catalogue row; state which of them send a notice and FR-030 will add rows.
- FR-017: its other billing notices (statements ready, overdue payout alert, outstanding invoice alert, payout schedule updated, manual payment reminder) have no catalogue row; FR-017 states no notice for a voided Approved statement or for Waiting for clinic setup.
- FR-009: the patient handler-changed notice and the compliance-flag notice to the admin compliance team have no catalogue row; FR-009 sends no notice for Cancel Invitation.
- FR-011: `aftercare.completed` produces no notification; if a completion notice is wanted, FR-011 must state it and FR-030 then adds the row.
- FR-020: if FR-020 keeps its own list of catalogue rows, mirror REQ-030-254 to REQ-030-294.
- FR-009, FR-011, FR-012, FR-014, FR-016, FR-019, FR-031: the new event keys were proposed by FR-030 from their wording; those PRDs may cite the keys.

**Batch A, leftovers**

- Ledger line 691 (not changed): separating FR-038 stage emits from the shared FR-037 ones needs FR-038 stages that do not exist; the progress reminder and export_ready parts were already satisfied.
- Ledger line 2506 (not changed): `aftercare.completed` produces no notification, so it stays an FR-011 event outside the catalogue (REQ-030-233).

Batch A applied in commit `51d915f`.

**Batch D, follow-ups**

- FR-003: REQ-003-013, REQ-003-014, REQ-003-100 and REQ-003-127 still carry carve-outs for the replacement provider that an admin close no longer needs, since an admin close is not a cascade trigger (row 761).
- FR-010: REQ-010-078 and the line 52 wording describe a no-fault early close on FR-006 Screen 11 that FR-006 does not support; either drop it or the owner decides a no-fault path (row 286).
- FR-020: REQ-020-093 still says the appointment reminder is "policy-driven" while FR-030 REQ-030-048 sets 7 days and 1 day (row 1329).
- FR-035: the support form must carry the booking reference for a plain case (row 2075).
- FR-030: register the aftercare completion event with its outcome values (row 2506).
- FR-018 and FR-019: confirm the affiliate capture is stored with the inquiry journey and read at acceptance (row 2335).
- FR-027: REQ-027-026 says the Cancellation Policy needs no acceptance, while FR-006 Screen 1 and REQ-006-038 keep a Cancellation Policy Ack checkbox; the owner should rule on one of them.

**Batch D, leftovers**

- Row 286 (FR-006, from FR-010): no-fault early close on Screen 11 is not built in FR-006; needs an owner decision and new design.
- Row 2335 (FR-005, from FR-018): the affiliate capture is not stored by FR-005; FR-018 and FR-019 own it.

Batch D applied in commit `7393942`.

**Batch E, follow-ups**

- FR-017: commission and the provider payout follow the pro-rata refund of a cancelled subscription in proportion, and the handover fee payout (paid from Hairline revenue) needs its payout wording (lines 2522 and 2771; FR-007 states the refund and the revenue source only).
- FR-030: FR-007B now states the Patient as recipient of both installment events; the catalogue rows for them should say the same, and the retired overdue alert and insufficient-time notice stay without rows (line 648).
- FR-030 and FR-015: REQ-030-156 says any account type, but only ENT-patient.email_delivery_issue exists (line 1188).
- Controller: stage-to-stage `next` edges for the FR-038 conversion (lines 686 and 803).

**Batch E, leftovers**

- Line 1188 (FR-009): provider email-delivery-issue indicator. A new flag field on the team member (the Owner is a team member) and a display on FR-009 Screens 6 and 11 and the FR-015 provider detail would be new design; REQ-030-156 already states the rule for any account type.
- Line 686 (FR-011): stage join from STG-monitoring-03-conversion to STG-aftercare-01-recovery-plan and the updated conversion stage description; shared stage nodes.
- Line 803 (FR-011): stage join from the aftercare stage to FR-038 conversion; shared stage nodes.

Batch E applied in commit `e6b9ee7`.

**Batch G, follow-ups**

- FR-005: confirm no sentence says FR-005 stores the affiliate capture; FR-018 REQ-018-308 owns it (stored with the inquiry journey) and FR-019 reads it at acceptance.
- FR-017: Screen 5 Type and Status still point to ENT-discount-code; update them so FR-019 can retire ENT-discount-code.
- FR-030: add catalogue events for patient.suspended, patient.suspension_ended, patient.password_reset_by_admin, admin.manual_notice and admin.policy_warning (the first four mandatory), for password changed and account locked, and for a cancelled team invitation, then FR-020 follows through the pointer sentence.
- FR-030: the locked-list wording "overrides the recipient's opt-out" is looser than the FR-020 rule that a locked notice still goes by email; align the wording.
- FR-006: if its PRD still says the appointment reminder is policy-driven, use two reminders at 7 days and 1 day (REQ-030-048).

**Batch G, leftovers**

- FR-019 line 2524 (FR-011 gap in review): not changed, no defect named.
- FR-019 line 2577 and line 2593 (ENT-discount-code and Screen 5 vocabulary): not changed, waits on the FR-017 Screen 5 edit.
- FR-020 line 766 (define urgent for the SMS gate): not changed, deferred to the backlog with SMS.
- FR-020 line 1714 (five FR-016 events): not changed, not FR-030 catalogue events yet.
- FR-020 line 1935 (Cancel Invitation notice): not changed, no FR-030 event exists.
- FR-020 line 2198 (password changed and account locked notices): not changed, no FR-030 event exists.
- FR-020 line 2325 and line 2331 (Pending affiliate offboarding activation email): not changed, FR-020 lists no such email and FR-018 owns the link invalidation.

Batch G applied in commit `2c9db1d`.

**Batch H, follow-ups**

- FR-001: Screen 15 says Help & Support routes to the Help Center & Support Access module (FR-033/FR-034) (REQ-001-103); it should name FR-035, the patient Help & Support Hub.
- FR-006: the Contact Support control on the Payment Window Expired and Cancelled screens should pass the booking reference; the receiving side is REQ-034-182 and REQ-035-090.
- Stage graph (controller, shared nodes): the join from the aftercare stage to monitoring conversion (ledger lines 686, 691, 803) has no owning FR.
- FR-030: ledger line 994 (confirm the patient resolution email also follows the notification settings) is not in this batch; FR-035 flow A6 step 1 already says the settings apply.

**Batch H, leftovers**

- 2524 (FR-037): no actionable item, FR-037 had its own review.
- 803 (FR-038): stage joins are shared stage nodes, not FR-038-owned.
- new, stage joins near lines 686, 691 and 803 (FR-038): same reason as 803.

Batch H applied in commit `be60070`.

**Batch F, follow-ups**

- FR-019: retire or mark ENT-discount-code. Stage edges from other FRs still point at it.
- FR-014: Widget 8 and Screen 4 Period column should show a release date for a Stripe Connect payout (ledger line 2859).
- FR-011 and FR-007: confirm they cite REQ-017-203 for the handover fee and REQ-017-202 for the subscription cancellation refund.

**Batch F, leftovers**

- Ledger line 1188 (FR-015): provider email-delivery-issue indicator needs a new feature; REQ-030-156 still points at the patient field.
- Ledger line 2524 (FR-012): a note that the review did not check FR-012 backlog status; nothing to edit.

Batch F applied in commit `23b83ce`.
