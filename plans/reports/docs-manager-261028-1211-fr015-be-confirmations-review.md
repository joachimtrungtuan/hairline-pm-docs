# Review: FR-015 backend confirmations (V1–V9), uncommitted doc changes

**Scope**: 15 modified files plus 2 new ones (CR-FR009-20261028-01, update-logs/2026-10-28/), checked against the backend sources `FR015-BA-CONFIRMATIONS-2026-10-28.md` and `FR015-WS1-INVENTORY-AND-ENDPOINTS-2026-10-28.md`. This was a read-only review; no file was edited.
**Paths**: relative to `local-docs/`.

## Verdict in brief

Report §8 answers every backend question (V1.1–V1.5, V2, V3 a/b/limitation, V4 a/b/c, V5 a/b, V6, V7 a/b/c, V8 a–d, V9). The touched PRDs and CRs match §8, with no decision reversed or invented. Version bumps, change-log rows, the new CR, the update log and the README entries are present. Links resolve, table column counts match their headers, and no added cell contains a literal `|`. The one `git diff --check` hit is the schema's `**Version**: 1.13.1␠␠` line. That markdown hard break was already in HEAD, so it is not a defect.

The real problems are in the member/invitation storage model, which the V3 decision introduced but did not fully specify, and in untouched PRDs that still contradict V9.

## Findings

### Critical

**C1. Schema §4 makes `inactive` mean "legacy pending invitee", but the backend stores Removed members as `inactive`. If the backend follows the doc literally, removed members get counted as seats.**
- `project-requirements/system-data-schema.md:337`: "Account status (active, suspended). `inactive` is a legacy value for an invited person who has not accepted"
- `system-data-schema.md:350`: "Legacy rows created with `inactive` before activation are pending invitations … and count toward seat usage"
- Backend V3: "Không tính: … thành viên đã gỡ (`inactive`)" (removed members are `inactive`), and "luồng mời cũ tạo thành viên với trạng thái `inactive`" (the old invite flow also creates members as `inactive`).
- FR-009 v1.7 Rule 9 and REQ-009-009 define member status Removed, but the schema status column has no value for Removed. The backend also reported a member status `pending` (V3 b), and neither the schema nor §8.4 says what happens to existing `pending` rows.
- **Fix**: decide how Removed is stored (see Open decision 1). Then list every stored `provider_users.status` value in §4: target values plus legacy `inactive` and `pending`, each with its meaning and migration. Add a rule that tells a legacy invitee apart from a removed member, for example "never activated: `password_set` false and no acceptance" against "removed: has `removed_at`/`deleted_at`". Mirror the same rule in CR-FR009-20261028-01 Implementation Reconciliation.

### Major

**M1. FR-003 and FR-004 still say inquiry cancellation cancels ALL quotes. That contradicts V9 and schema §7.**
- `functional-requirements/fr004-quote-submission/prd.md:144`: "All quotes for that inquiry transition to 'Cancelled (Inquiry Cancelled)' regardless of current state (draft, sent, expired)"
- `fr004-quote-submission/prd.md:216`: "ALL quotes for that inquiry are auto-cancelled … each affected provider notified via `quote.cancelled_inquiry`"
- `fr004-quote-submission/prd.md:715` (REQ-004-013): "auto-cancel ALL quotes"
- `fr003-inquiry-submission/prd.md:381` ("all associated quotes auto-cancelled") and `:1239` (REQ-003-013)
- Schema `system-data-schema.md:665` now keeps `cancelled_provider_status`, `withdrawn`, `cancelled_other_accepted`, `accepted` and `archived`. Under the current FR-004 text, a provider whose quote is already `cancelled_provider_status` or `withdrawn` would also get a `quote.cancelled_inquiry` notice.
- **Fix**: in FR-004 lines 144 and 216 and REQ-004-013, and in FR-003 Workflow 5 Outcome and REQ-003-013, say "only `draft`, `sent`, and `expired` quotes", state that quotes in any other status keep their status and cause, and limit `quote.cancelled_inquiry` to the quotes that actually change. Bump FR-003 and FR-004, and add change-log rows.

**M2. `provider_staff_invitations` has no table definition, yet the schema and FR-009 now depend on it for seat counting and for legacy-row validity.**
- `system-data-schema.md:306` and `:350` reference it. It appears only in the table list (`:3424`). CR-FR009-20261028-01 admits: "The `provider_staff_invitations` table is referenced in §3 but has no table definition."
- `system-data-schema.md:350` says legacy `inactive` rows count "while the invitation is valid". A legacy row may have no invitation row and no `expires_at`, so its validity cannot be computed.
- **Fix**: add a §4A `provider_staff_invitations` definition from FR-009 Key Entity 3: id, provider_id, email, first_name, last_name, role_id, invited_by_type/id, token hash, status (pending/accepted/expired/cancelled), expires_at, accepted_at, provider_user_id (set on accept), and the partial unique key on email for pending rows. Also state how a legacy invitee's expiry is determined (Open decision 2). A table addition belongs in a schema minor version (1.14.0), not a patch.

**M3. The V2 staging cleanup does not say what happens to the records that depend on the deleted rows.**
- §8.3 and the CR-FR006 addendum (`functional-requirements/fr006-booking-scheduling/change-request-2026-10-27-legacy-status-value-migration.md:79-80`) say to delete or recreate the legacy rows. Several of them carry `after_cares` rows (inventory §1.1: `accepted`/`confirmed`/`completed` with aftercare), and they may also carry `schedules`, payments and conversations. Deleting only quotes leaves orphaned aftercare and payment rows, which breaks the new §13 rule that treatment-linked aftercare must reference an accepted quote.
- **Fix**: add one line to the CR-FR006 addendum and §8.3: "Cleanup removes or recreates the whole case: the inquiry, its quotes, `inquiry_providers`, aftercare, schedules, payments and their conversations. No dependent row may be left referencing a deleted quote. The dry-run lists the dependent rows before deletion."

### Minor

**m1. The CR-FR004 addendum maps legacy `accepted` only when no deposit was paid.**
`fr004-quote-submission/change-request-2026-10-27-legacy-status-value-migration.md:75-76`: "`accepted` (treated like `scheduled` with no paid deposit)". A legacy `accepted` quote with a paid deposit has no row and would go back to the backend as "unlisted". **Fix**: add "`accepted` with a paid deposit → quote `accepted`, booking `confirmed`, inquiry `confirmed`", or say that legacy `accepted` follows all three `scheduled` rows.

**m2. The aftercare-wins rule says "active" aftercare only.**
CR-FR006 addendum `:75`: "an active treatment-linked aftercare record exists". A quote still labelled `accepted`/`confirmed` whose aftercare is completed or cancelled is not covered. See Open decision 7.

**m3. A staging count is hard-coded in an evergreen CR.**
CR-FR006 addendum `:79`: "(11 rows on staging)". The backend figures also do not reconcile with each other:
- V1.2 says 3 `accepted`/`confirmed` quotes with active aftercare, while inventory §1.1 shows 4 + 2 = 6 rows.
- The inventory §1.1 row counts add up to 28, against "23 quote" in the dry-run.

So the §1.1 rows are joined rows, not distinct quotes. **Fix**: drop the count from the CR, or label it "backend-reported, 2026-10-28". Ask the backend to reconcile the 3/6/11/23 figures in the next dry-run.

**m4. The FR-003 submit-time error does not match the flow diagram.**
`fr003-inquiry-submission/prd.md:710` says the submit-time error "is the 'Provider selection valid? No → …' step". In the flowchart (`:111-116`), that check runs before Review, and a failed submit goes to "Show submission error + allow retry" → Review. **Fix**: add a `SubmitOk` branch, "Selected provider no longer eligible → ProviderSel", or reword the note to say it reuses that error presentation from the submit step.

**m5. FR-009 Rule 10 cites FR-032 Rule 6, but FR-032 Rule 6 does not cover team management.**
`fr009-provider-team-roles/prd.md:357, 788` cite "view-only (FR-032 Rule 6)". `fr032-provider-dashboard-settings/prd.md:1627` lists only "profile, documents, reviews, and billing" as view-only. Nothing defines the blocked-invite message or the other team actions while Suspended. **Fix**: add team management to FR-032 Rule 6, or drop the citation and state the rule in FR-009 itself. See Open decision 4.

**m6. FR-009 still has an invitation status "Pending Send".**
`fr009-provider-team-roles/prd.md:183, 907`: "marks invitation as 'Pending Send'". That status is not in the Pending/Accepted/Expired/Cancelled set, and seat usage counts only "status Pending". **Fix**: make "Pending Send" a delivery flag on a Pending invitation, not a status.

**m7. FR-015 integration lists omit the new event.**
`fr015-provider-management/prd.md:900` and `:980` list the provider lifecycle FR-020 events without `provider.login_email_changed`. **Fix**: add it to both lists.

**m8. The schema changelog row is internally inconsistent.**
`system-data-schema.md:3473`: "clarifications, no Change Request" but ends with "(FR-009 v1.7, CR-FR009-20261028-01)". The §4 business-rules header `:348` still reads "(FR-015 v1.15, FR-009 v1.5)". **Fix**: say "§4 under CR-FR009-20261028-01; other items clarifications", and update the header to FR-009 v1.7.

**m9. The FR-011 header Status is stale.**
`fr011-aftercare-recovery-management/prd.md:6` still reads "Revised 2026-10-26 (standalone aftercare reassignment …)". FR-015 updated its Status line for 1.23; FR-011 did not.

**m10. CR-FR009-20261028-01 Requested Date is 2026-10-27** (`:8`). The question (V3) was raised in the 2026-10-28 backend document. Use 2026-10-28, or name the 2026-10-27 source in the CR.

**m11. The update log and the report disagree on open items.**
`update-logs/2026-10-28/FR015_BE_CONFIRMATIONS_RESOLUTION_2026-10-28.md:32` lists only V8. Report §8.12 also lists V7 situation 4 (global email check on every change) and cascade-dependent testing. Copy both into the update log.

**m12. Copy naming drifts between docs.**
FR-005 now says "Contact Support" with "replacement clinic". FR-003 (`:279, :735`, REQ-003-020) and FR-015 (`:229, :730`) say "Contact Admin/Support" with "replacement provider". No contract breaks, but pick one label for the action.

**m13. Pre-existing and outside this change set: the tech spec still cancels standalone aftercare.**
`system-technical-spec.md:167`: "cancels that provider's … bookings and its standalone aftercare". That contradicts schema 1.12.0+ and FR-011 v1.6+, where standalone aftercare is reassigned, not cancelled. Fix it in the next tech-spec touch.

**m14. Report §8.9 does not explicitly assign WS1 §1.2 item 2** ("only 2 bookings exist"). It is implied by V2. Add it to the closing list in §8.9.

### Checked and correct (no action)

- FR-011 Entry Points, Workflow 2b linkage, and schema §13 match §8.2 V1.4.
- FR-020/FR-030 event rows (mandatory, email only, toggle locked) match §8.8(b).
- FR-015 already required the change reason for the email change (line 457, pre-existing), so V7(c) needs no doc change.
- The CR-FR004 addendum API rules match §8.9 (a), (b) and (d), and the endpoint completion rules match §8.9(c).
- The CR-FR003 addendum matches V1.5.
- The schema §11A NOT NULL columns cited in V2 are correct (`acceptance_event_id`, the four hold fields, `booking_total`).
- The CR-FR009 seat example (3 Active + 1 Suspended + 2 valid Pending = 6) is correct, and so is the §8.4 example (2 + 1 + 1 = 4).
- CR-FR009 follows every template heading and header field.
- Not creating a CR for the new FR-020 event is justified: FR-020 is pending consolidated verification, and FR-015 v1.22 already required both notices.

## Open decisions needing the Product Owner

1. **How is a Removed team member stored?**
   - (a) New status value `removed`, with `removed_at`.
   - (b) Soft delete (`deleted_at`), with status left as is.
   - (c) Keep `inactive` = removed, and migrate legacy never-activated `inactive` rows into `provider_staff_invitations`.

   Recommendation: (a) plus the migration in (c), so that each stored value has exactly one meaning.

2. **How long does a legacy never-activated `inactive` invitee count toward seats?**
   - (a) Use the expiry of its existing activation token.
   - (b) Treat it as Expired at migration, so the provider must resend.
   - (c) Give it a fresh 7-day expiry at migration.

   Recommendation: (a) where a token expiry exists, otherwise (b). Staging has no real data, so the impact is nil.

3. **Should the schema define `provider_staff_invitations` now?**
   - (a) Yes, add §4A from FR-009 Key Entity 3 (schema 1.14.0).
   - (b) Leave the columns to the backend and document them afterwards.

   Recommendation: (a). The seat rule and the email identity rule both depend on it.

4. **While a provider is Suspended, which team actions are allowed, and what does the provider see when Invite is blocked?**
   - (a) All team management is view-only.
   - (b) Removing or suspending a member and cancelling an invitation stay allowed (they reduce access); invite, resend and role change are blocked.
   - (c) Only invite and resend are blocked.

   Recommendation: (b), with the copy "Your account is suspended. You can invite team members again after it is reactivated." Add this to FR-032 Rule 6 and FR-009 Screen 2.

5. **Does an invitation in "Pending Send" (email delivery failed) take a seat?**
   - (a) Yes, because it is a Pending invitation with a delivery flag.
   - (b) No, not until the email is delivered.

   Recommendation: (a). Otherwise a provider can exceed its limit through failed sends.

6. **How should a legacy `accepted` quote with a paid deposit migrate?**
   - (a) Quote `accepted`, booking `confirmed`, inquiry `confirmed`, the same as `scheduled` with a deposit.
   - (b) The BA decides row by row.

   Recommendation: (a).

7. **Does aftercare-wins (V1.2) apply only to active aftercare?**
   - (a) Active only (the backend's current rule).
   - (b) Any treatment-linked aftercare record.
   - (c) Active → booking `aftercare`; completed → booking `completed`; cancelled → follow `quotes.status`, and list the row for review.

   Recommendation: (c).

8. **What exact text does FR-003 Screen 8 show for a provider-unavailable offer before acceptance?** Line 735 gives no exact copy.
   - (a) Reuse the FR-005 string "This provider is no longer available. Please contact support."
   - (b) Write a dashboard-specific string that names the offer, for example "[Provider name]'s offer is no longer available."

   Recommendation: (b) for the dashboard card and (a) for the Accept error, both with the same Contact Support action.

9. **What happens when an admin adds an ineligible provider to an inquiry (V5 admin-add path)?** Only the patient-side error is specified.
   - (a) The admin picker shows only eligible providers, and the API rejects with "[Provider name] is not eligible to receive inquiries (status or Owner password not set)."
   - (b) The provider is skipped with an audit note.

   Recommendation: (a), for the same reason "nothing is skipped silently" was decided for patients. Place it in the FR that owns admin inquiry reassignment (FR-016).

10. **How far does the V2 staging cleanup reach?**
    - (a) Delete the whole case graph (inquiry, quotes, participation, aftercare, schedules, payments, conversations).
    - (b) Recreate every case through the current accept flow.
    - (c) Delete only quotes and bookings.

    Recommendation: (a) for test-only rows and (b) where testers need the case. Never (c).

Status: DONE_WITH_CONCERNS
Summary: Report §8 answers every backend question, and the doc edits match it with correct process, links and tables. One critical gap remains: `inactive` now means "legacy invitee" while the backend uses it for Removed members, and the invitations table is undefined. FR-003 and FR-004 still say inquiry cancellation cancels all quotes, which contradicts V9.
