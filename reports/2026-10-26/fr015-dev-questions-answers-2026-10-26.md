# FR-015 Dev-Team Questions — Consolidated Answers

**Date**: 2026-10-26
**Sources answered**:
- `FR-015-BE-PM-DECISIONS.md` (2026-10-22): shared decisions A1–A5 plus per-task items for HAIRL-1558, 1571, 1573, 1577, 1582, 1584, 1587, 1597, 1599, 1601, 1602, 1603, 1605, 1607, 1609, 1620 and 1622.
- `FR015-BA-QUESTIONS-2026-10-22.md` (2026-10-22): cascade, scheduled changes and Admin Support Required, questions Q1–Q14.

**Authority**: [FR-015 PRD v1.21](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) and [system data schema v1.12.0](../../project-requirements/system-data-schema.md). The dev team's PRD copy was out of date. For example, it cites Clinic Name max 100 at "L266/L336"; the current PRD says 3–200. Always re-pull `main` before citing lines.

**Answer types**:
- **PRD**: already specified in the docs. Follow the cited line.
- **PO**: Product Owner decision made on 2026-10-26, written into the docs.
- **Delivery**: a Product Owner decision about sequencing or rollout. It is recorded in this report only, not in a PRD.
- **BE**: an implementation choice the docs leave to the dev team. A recommendation is given where useful.

Line numbers (`L…`) refer to the files as of 2026-10-26.

### Link shortcuts

- **FR-015**: [`fr015-provider-management/prd.md`](../../project-requirements/functional-requirements/fr015-provider-management/prd.md)
- **Schema**: [`system-data-schema.md`](../../project-requirements/system-data-schema.md)
- **FR-011**: [`fr011-aftercare-recovery-management/prd.md`](../../project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md)
- **FR-006**: [`fr006-booking-scheduling/prd.md`](../../project-requirements/functional-requirements/fr006-booking-scheduling/prd.md)
- **FR-004**: [`fr004-quote-submission/prd.md`](../../project-requirements/functional-requirements/fr004-quote-submission/prd.md)
- **FR-020**: [`fr020-notifications-alerts/prd.md`](../../project-requirements/functional-requirements/fr020-notifications-alerts/prd.md)
- **FR-032**: [`fr032-provider-dashboard-settings/prd.md`](../../project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md)
- **FR-009**: [`fr009-provider-team-roles/prd.md`](../../project-requirements/functional-requirements/fr009-provider-team-roles/prd.md)
- **FR-013**: [`fr013-reviews-ratings/prd.md`](../../project-requirements/functional-requirements/fr013-reviews-ratings/prd.md)

---

## 1. Plain-Language Explanations

### 1.1 What is the "provider status event"? (Q1)

Think of it as a **receipt number for each status change**.

Suppose an admin suspends Clinic X at 10:00 on 3 November. The system writes **one row**:

> "Clinic X: Active → Suspended, cause `ProviderSuspended`, reason '…', by Admin Y, effective 10:00 UTC."

That row gets an ID, for example `evt-123`.

The suspension then affects a number of records: 2 quotes, 3 bookings, 1 aftercare case and 1 payment. **Each of those records is stamped with `evt-123`.**

The stamp matters for three reasons:

- **Tracing.** Weeks later someone asks why a booking was cancelled. The booking points to `evt-123`, which shows who did it, when, and why.
- **Safe retries.** If the cascade crashes halfway and runs again, it can see that the work for `evt-123` is already done. It does not cancel twice or send duplicate emails.
- **No overwriting.** If Clinic X is later deactivated, that creates a new receipt, `evt-456`. Records already cancelled under `evt-123` keep their original cause `ProviderSuspended` ([FR-015 L1163](../../project-requirements/functional-requirements/fr015-provider-management/prd.md)).

The schema mentioned `provider_status_event_id` in four tables but never defined the event table itself. The dev team proposed reusing the Tab 8 activity-log row.

**Decision (PO): a dedicated, append-only `provider_status_events` table.** It is a clean foreign-key target and stays separate from the activity log, which is a display feed mixed with every other kind of edit. Tab 8 still shows these events.

See [Schema §41 (L3261)](../../project-requirements/system-data-schema.md) and [FR-015 Key Entity 5 (L1228)](../../project-requirements/functional-requirements/fr015-provider-management/prd.md).

### 1.2 Booking created at acceptance vs at payment (Q2, Q11)

**What the docs say** ([Schema §11A L1326](../../project-requirements/system-data-schema.md), [FR-006](../../project-requirements/functional-requirements/fr006-booking-scheduling/prd.md)):

1. The patient accepts a quote.
2. In the same step, a **booking row is created** with status `accepted`, and the treatment slot is held on that booking.
3. When the deposit is paid, the same booking moves to `confirmed`.

**What BE does today:**

1. Acceptance creates only an `AcceptanceEvent`, which holds the slot.
2. The booking row appears only when the patient pays.

**Why it matters.** Patient P accepted Clinic X's quote yesterday and hasn't paid yet. Today Clinic X is suspended. The cascade must mark P's case "Cancelled — Provider Suspended + Admin Support Required" and release the slot. Under the BE model there is **no booking row for P**, so there is nowhere to put the mark. The slot hold also lives in two places, which is why the dev team raised Q11 about duplicate-slot protection.

**Decision (PO): align FR-006 first.** BE implements booking-at-acceptance as documented, with the hold on the booking, before the FR-015 cascade ships. This also settles Q11: there is one hold location, and the one-active-booking-per-slot index lives on `bookings`.

### 1.3 "Unresolved Support Items" (Q8)

This is a **number shown in the Reactivate Provider modal** (Screen 5). It tells the admin how much clean-up from the suspension is still open, meaning records flagged **Admin Support Required** and not yet resolved.

- It is only a heads-up. It **does not block** reactivation.
- It links to the FR-016 list filtered to this provider.

Example: Clinic X was suspended, which affected three patients.

- **Patient A** had an unaccepted quote. One inquiry is flagged.
- **Patient B** had a confirmed booking. Both the booking and the inquiry are flagged, but they are one case.
- **Patient C** was in aftercare. One aftercare case is flagged.

**Decision (PO): count one per affected inquiry/case**, so the number shown is **3**. B's booking and inquiry count once. This matches how FR-020 sends one admin alert "per affected inquiry/case" ([FR-020 L105–113](../../project-requirements/functional-requirements/fr020-notifications-alerts/prd.md)). See [FR-015 Screen 5 L744](../../project-requirements/functional-requirements/fr015-provider-management/prd.md).

### 1.4 Legacy status values (Q3, Q5)

The schema renamed several stages:

- Inquiry `requested` → `inquiry` and `offers` → `quoted`.
- Booking stages now live on `bookings` and `inquiries`, not on `quotes.status`.
- Provider participations gain `cancelled`.

BE still uses the old values, and FE and Flutter read them directly.

**Decision (PO): migrate to the schema values in this release.** BE must also **write and deliver a migration note to the FE (React) and Flutter devs** covering:

- the old-to-new value mapping per field;
- which endpoints and response fields change;
- new values the apps must render, such as `inquiry_providers.status = cancelled`, which patients see as "Offer Unavailable" ([FR-004 L512](../../project-requirements/functional-requirements/fr004-quote-submission/prd.md));
- the release or cut-over date.

The apps update in lock-step.

### 1.5 Standalone aftercare on suspension (Q4)

FR-015 said a suspended provider's standalone aftercare (for patients treated elsewhere) **moves to admin reassignment**. FR-011 D4 and schema §13 said it is **auto-cancelled**.

**Decision (PO): reassign, don't cancel**, the same as treatment-linked aftercare. FR-011 and the schema are now fixed:

- The case keeps its status and gets the cause plus `supportRequired`.
- An admin reassigns it on FR-011 Screen 19.
- The **`after_cares` row is the source of truth**. `standalone_aftercare_requests` is intake only and **does not need a `cancelled` value**.

See [FR-011 D4](../../project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md) and [Schema §13 L1451](../../project-requirements/system-data-schema.md).

---

## 2. Combined Question List and Answers

The questions from both documents are merged by topic.

### 2.1 Data contracts shared by many tasks

| # | Question | Answer | Type / Source |
|---|---|---|---|
| A1 / HAIRL-1577 | Commission `type` values: BE uses `percentage,flat` in one place and `amount,percentage` in another. | Use one value set everywhere, the schema's: `commission_model` = `percentage` or `flat_rate`. Migrate the stored `amount` and `flat` rows to `flat_rate`, and have reads return `flat_rate`. This also fixes the Flat Rate create failure. | PRD/Schema: [Schema §2B L231, L243](../../project-requirements/system-data-schema.md); [FR-015 Step 5 L351](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| A2 | `payment_cycle` values. | `payout_frequency` = `weekly`, `twice_monthly` or `monthly`, with UI labels "Weekly", "2x a Month" and "Monthly". Drop `quarterly`. Replace `bi-monthly` with `twice_monthly`, because "bi-monthly" can also mean every two months. Periods are Mon–Sun, the 1st–15th and 16th–end, and the calendar month. | PRD/Schema: [Schema L152](../../project-requirements/system-data-schema.md); [FR-015 L358, L620](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| A3 | Field names and types. | Commission fields: `commission_model`, `commission_percentage` / `flat_rate_amount`, `flat_rate_currency`, and `effective_date` (not `start_date`). Admin change reason: `reason`, 10–500 chars after trim. Re-auth: `password` (MVP). Concurrency token: the PRD doesn't name it, so BE picks `updated_at` or `version`, but it must be **required** on every save. | PRD/Schema: [Schema §2B](../../project-requirements/system-data-schema.md); [FR-015 L439, L1183](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); token name is BE |
| A4 / HAIRL-1558 | Admin saves through the admin PUT or the self-service route? | The PRD defines **what** an admin may edit: the Tab 1 field table's "Admin/Provider Editable" column, plus Tabs 2, 4, 6 and 7. The route is BE's choice. **Recommendation:** extend the admin route rather than reuse the provider self-service route. Provider self-edits are exempt from the reason rule, so a shared route could let admin saves skip the required reason, audit and optimistic lock. | BE (rule source: [FR-015 Tab 1 L401+, L439](../../project-requirements/functional-requirements/fr015-provider-management/prd.md)) |
| HAIRL-1558 | Should the admin profile save still send `commission.*`? | No. Commission is edited only in Tab 7, and Tab 1 shows it read-only. The profile save should ignore or reject commission fields. | PRD: [FR-015 L442](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| A4 / HAIRL-1558 | The admin save doesn't store `staff`, `reviews` or `reset_*_image`. | These have separate owners. **Staff** is managed through FR-009 Screen 12, embedded as Tab 3. **Reviews** go through FR-013, via Tab 5. **Profile and cover images** are editable by both admin and provider, so the admin profile save must support removing them. | PRD: [FR-009 L875](../../project-requirements/functional-requirements/fr009-provider-team-roles/prd.md); [FR-015 Tab 5 L521+, L409–410](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1558 | `awards.*.is_deleted` type. | A BE fix with no PRD impact; added to the BE checklist. | BE |
| A5 / HAIRL-1582 | Conflict error code and text; what happens after a conflict; merge? | Text: "Provider profile was modified by another admin. Please refresh and re-enter your changes." The stale save is rejected, with no last-write-wins. **No merge**: keeping the admin's input on screen plus a Refresh action is enough. Apply this to every save route: profile, commission, seat limit and document notes. The PRD doesn't fix the HTTP code. **Recommendation: 409** for conflicts, keeping 422 for validation. | PRD: [FR-015 Edge Cases L1149](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); HTTP code is BE |

### 2.2 Commission (Tab 7, wizard Step 5)

| # | Question | Answer | Type / Source |
|---|---|---|---|
| HAIRL-1571 | Currency list and default. | The FR-029 enabled currency list, **defaulting to the system default currency**, so it is preselected. It is required only when the model is Flat Rate. | PRD: [FR-015 L357, L621](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1571 / 1599 | Effective Date rules; backdating in Tab 7? | Today or a future date in both the wizard and Tab 7. **No backdating.** "Today" = **current UTC date**. | PRD [FR-015 L359, L622](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) + PO (UTC) |
| HAIRL-1571 | Scheduled Configuration in the wizard? | No. The wizard's start date is simply the first configuration's Effective Date. If it is in the future, the FR-029 global default applies until then. The Scheduled Configuration display and cancel action exist **only in Tab 7**. | PRD: [FR-015 L625, L636](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); [Schema L267](../../project-requirements/system-data-schema.md) (a provider without an active provider-specific row uses the global default) |
| HAIRL-1571 / 1599 | Value range; is 0% valid? | Percentage **0–100 with 0.1 precision, so 0% is valid.** Flat rate must be > 0 in the currency's minor units. The FE wizard must stop rejecting 0%. BE's commission edit already accepts 0–100; the create and store paths must add the same ≤ 100 cap. The dev team's proposed "0 < value" rule should not be adopted. | PRD: [FR-015 L356, L619](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1599 | Error code and wording (PRD said 400; BE returns 422). | **422 validation error**. The messages are "Percentage must be between 0-100%" and "Flat rate must be greater than 0." The PRD now says 422. | PO, written into [FR-015 L1152](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1584 | History is wiped on edit; is the reason optional? | Never delete rows. Insert a new configuration and archive the old one (`pending`/`active`/`archived`), and keep Commission History. A reason is **required (10–500)**, and re-authentication by password is required. | PRD: [FR-015 L626, L640, L1183](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); [Schema §2B L263](../../project-requirements/system-data-schema.md) ("An edit archives the current row and inserts a new one") |
| HAIRL-1584 | Permission. | Admins with the FR-031 **Edit Providers** permission, which covers commission, seat limit, documents and the featured flag. The route must check this; `auth:api` alone is not enough. | PRD: [FR-015 L867](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1584 | Gating by status. | Active and Suspended providers are editable, so terms can be fixed before reactivation. Deactivated providers are read-only. FR-029 Screen 5 follows the same rule. | PRD: [FR-015 L631](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1584 | Scheduled configuration behaviour. | At most one pending configuration per provider; a new future edit replaces it and both are logged. Cancelling needs a reason and re-auth. It applies automatically on its date and is shown read-only to the provider in the FR-032 Screen 4 panel. | PRD: [FR-015 L625, L636](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1584 | Shared FR-029 scope. | Saving splits this provider out into its own single-provider scope; the others are unchanged. Warn before saving and log the split in both places. | PRD: [FR-015 L639](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |

### 2.3 Profile editing and validation (Tabs 1, 2, seat limit)

| # | Question | Answer | Type / Source |
|---|---|---|---|
| HAIRL-1573 | Scope of "every admin save needs a reason". | Tabs 1, 2, 4 and 7, plus Tab 6 **notes**. This includes seat limit, awards and languages. **Excluded:** the Featured toggle and quick action (new), document upload, replace and delete, and provider self-edits. Status changes and Login as Provider have their own 20-character reason. | PRD [FR-015 L439, REQ-015-025 L1183](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) + PO (Featured, Replace) |
| HAIRL-1597 | Clinic Name 100 or 200; min 3? | **Min 3, max 200.** The dev team's "max 100" comes from an outdated copy. | PRD: [FR-015 L332](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1597 | Over-limit behaviour (block typing or show an error). | The PRD doesn't specify. The FE's "block typing + character counter" is acceptable; just keep it consistent. | BE/FE |
| HAIRL-1597 | Specialty: free text or list? | Select from the managed **Provider Specialties** list (FR-026 Screen 5f), active values only. A stored value that is later deactivated still displays but can't be newly picked. The endpoint that serves the list is a BE choice. | PRD: [FR-015 L322, L416](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1597 | Phone country code; website. | Phone = Country Code dropdown (FR-026) plus a numeric number validated per country, so the code is required when a phone is entered. Website: http/https, auto-prepend `https://`. | PRD: [FR-015 L337, L338](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1597 | Other limits. | The dev team's list is correct: name max 50, years 0–60, licence max 50, bio 50–500, seat 1–500, and the award limits. The owner email follows the FR-009 global identity rule. | PRD: [FR-015 Screen 2 L297+](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1605 | Which Tab 1 fields are editable? Featured cap error? | Use the Tab 1 field table's last column (Admin only / Both / Display only). Featured-cap message: "Maximum of 10 featured providers reached. Unfeature another provider first." It is enforced server-side on every path. | PRD: [FR-015 Tab 1 L401+, Rule 8 L770](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) (copy added by PO) |
| HAIRL-1605 | `show()` is missing fields: profile and cover images, Contact Phone, Contact Email separate from the owner email, Commission Summary, Featured, Seat Limit, Status, Completed Procedures, Average Rating. | Return every field in the Tab 1 table. Completed Procedures counts the FR-010 treatment-completion milestone. | PRD: [FR-015 L407–432, L441](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); BE checklist |
| HAIRL-1607 | Last-language rule and message; reorder method. | At least 1 language. Message: "At least one language is required." Reorder by **drag-and-drop**. A reason is required (Tab 2). | PRD: [FR-015 L467, L475](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) (copy added by PO) |
| HAIRL-1620 | Seat limit below team size: reason, warning text, what happens to extra members? | Re-auth by password. Warning: "Current team size (50) exceeds new seat limit (30). Existing team members will not be removed, but no new invitations can be sent until limit is increased or team size is reduced." The save goes ahead after the admin confirms. Team size = FR-009 seat usage (**members + pending invitations**). Nobody is removed; only new invites are blocked. A reason **is required** because Seat Limit is a Tab 1 save. Use the shared `reason` field (10–500 characters); the existing `justification` field should be renamed or dropped. **Every path that writes Seat Limit** must apply the same rules, including the general admin profile save, which currently checks only 1–500. FR-015 L1154 now defines team size as FR-009 seat usage. | PRD: [FR-015 L443, L1154, L1183](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); [FR-009 seat usage](../../project-requirements/functional-requirements/fr009-provider-team-roles/prd.md) |
| HAIRL-1558 | Which task owns test cases 13/14 (seat-limit password and warning)? | These are seat-limit rules, so they belong to **HAIRL-1620**. | PRD mapping ([FR-015 L443, L1154](../../project-requirements/functional-requirements/fr015-provider-management/prd.md)) |

### 2.4 Documents and uploads (Tab 6)

| # | Question | Answer | Type / Source |
|---|---|---|---|
| HAIRL-1602 | Document file types (PRD looked inconsistent). | **PDF, JPG, PNG, DOCX, XLSX**, max 10MB. This is now consistent across the wizard, Tab 6 and the entities. | PRD: [FR-015 L135, L592](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1602 | Cover image minimum size? | **None**: max 10MB, JPEG/PNG, recommended 1920×300. Profile picture: min 200×200, max 5MB. Server-side minimum-size checks are recommended (BE). | PRD: [FR-015 L309, L310](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1602 | English and Turkish error copy. | **Approved English copy** (inline, under the field; file not saved): "Unsupported file type. Allowed: {types}." / "File is too large. Maximum size is {limit} MB." / "Image is too small. Minimum size is 200 × 200 pixels." (logo only). Limits: logo 5, cover 10, award image 2, documents 10 MB. Turkish follows the normal translation workflow (FR-021). | PRD: [FR-015 Upload error messages, L371](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1609 | Admin delete or replace of provider-uploaded documents. | Admins can view, download and add notes, but **cannot replace or delete**. Only the provider can, through FR-032. Admin-uploaded documents: full control. | PRD: [FR-015 L586](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); error code and message are BE (403 recommended) |
| HAIRL-1609 | Does Replace need a reason? Keep the old file? | **No reason. The old file is archived**: soft-deleted, retained for compliance and logged in Tab 8. The new file becomes current. | PO, written into [FR-015 L588](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |

### 2.5 Provider creation and wizard

| # | Question | Answer | Type / Source |
|---|---|---|---|
| HAIRL-1603 | Success message. | "Provider [Clinic Name] created successfully. An activation email has been sent to [email]." | PO, written into [FR-015 L147](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1603 | Email failure: wording and retry. | Warning: "Provider activated but notification email not yet delivered. Email delivery in progress." **Retry is required**: up to 3 attempts over 1 hour (BE job plus status). The admin can also use "Resend Activation Email". | PRD: [FR-015 L1148](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| HAIRL-1603 | Legacy `provider.onboarding_requested` firing. | Admin-initiated creation sends only `provider.activation`, which is mandatory. The onboarding-request event should not fire from this path. | PRD: [FR-015 Main Flow step 13](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); [FR-020 L106, L110](../../project-requirements/functional-requirements/fr020-notifications-alerts/prd.md) |
| HAIRL-1601 | Leave-wizard dialog: wording, scope, drafts. | "You have unsaved changes. Are you sure you want to leave?" with **Stay / Leave**, the same text as FR-032. It covers in-app navigation, browser Back, and tab close/reload (the browser's native prompt). **No drafts**; Leave discards. | PO, written into [FR-015 L369](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); text from [FR-032 L1637](../../project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md) |

### 2.6 Login as Provider (HAIRL-1587)

| Question | Answer | Type / Source |
|---|---|---|
| Reason and password? | Yes: a reason (min 20 chars) plus admin password re-authentication. Super Admin only. | PRD: [FR-015 L390+](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| Restrictions and banner. | A persistent banner reads "You are viewing as [Provider Name] — admin session by [Admin Name]" with "End Session". The admin cannot change the provider's password, login email, or payout, bank or financial settings. Start, end and every write are logged in Tab 8. | PRD: same section |
| New tab or replace the session? Token lifetime? | **New tab**; the admin's own tab stays open. The session ends on **End Session or 30 minutes of inactivity**, with **no absolute cap**. BE: use a sliding inactivity expiry on the impersonation token. | PO, written into [FR-015 L396–397](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |

### 2.7 Reviews tab (HAIRL-1622)

| Question | Answer | Type / Source |
|---|---|---|
| How does Tab 5 relate to FR-013? | Tab 5 is a provider-scoped view of FR-013. Add, Edit and Remove open FR-013 Screen 8, and FR-013's rules apply. FR-015 adds no reason, and Tab 5 is not part of REQ-015-025. | PRD: [FR-015 Tab 5 L521+](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| Keyword search. | Required ("search by keyword"). BE either adds `search` to `get-reviews-by-provider-id` or lets the FE use `admin/reviews?provider_id=` once it is unmocked. | PRD (same); endpoint is BE |
| Role, removal reason, delete or hide? | **Role:** adding a review needs **review management permission**, which is separate from provider management. **Reason:** an edit or removal reason is required, and a removal reason must be at least 10 characters. **Remove = unpublish and archive**, never a permanent delete. An admin may also redact text or photos after publication. | PRD: [FR-015 L533](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); [FR-013 L105, L408, L418, L496](../../project-requirements/functional-requirements/fr013-reviews-ratings/prd.md) |
| When do the FR-013 mock flags turn off? | **Dependency:** HAIRL-1622 Add/Edit/Remove ships only after the FR-013 tasks (HAIRL-1249/1250/1252/1254) turn their mock flags off against real BE endpoints. Until then the Tab 5 buttons stay off. Not a PRD change. | PO *(delivery decision, report only)* |

### 2.8 Lifecycle cascade, scheduled changes, Admin Support Required (BA Q1–Q14)

**Section A** of the BA document lists topics the dev team considered already answered. Each row is correct, with two citation updates. FR-015 Rule 3 is now at [L765](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) (not L761). §40 `deactivation_event_id` now references the new §41 `provider_status_events` table ([Schema §40](../../project-requirements/system-data-schema.md)).

**Section C** (what the backend will handle itself):
- **Interim adapters are not needed.** Item 1 offered temporary routes for "accepted but not paid" cases and a legacy-status adapter. Q2 and Q3 were decided against both: implement booking-at-acceptance and migrate the status values.
- **The "additive only" principle (Source B, L7) is overridden** for this release. Q2 and Q3 change behaviour for all providers, not only suspended ones. Plan regression testing for Active providers.
- **The field-name notes in item 3 are correct.** `quotes.cancellation_provenance` is JSON ([Schema L597](../../project-requirements/system-data-schema.md)). The booking cause lives in `bookings.cancellation_reason` ([Schema L1362](../../project-requirements/system-data-schema.md)).
- **Add `provider_status_events`** (§41) to the list of additive tables.


| # | Question | Answer | Type / Source |
|---|---|---|---|
| Q1 | What table is the "provider status event"? | Dedicated `provider_status_events`; see §1.1. | PO → [Schema §41](../../project-requirements/system-data-schema.md), [FR-015 Key Entity 5](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| Q2 | Booking at acceptance or at payment? | Align FR-006 first; see §1.2. | Delivery |
| Q3 | Legacy status values. | Migrate now and deliver a migration note to FE and Flutter; see §1.4. | Delivery |
| Q4 | Standalone aftercare: which table, cancel or not? | `after_cares` is the source; reassign, not cancel; no `cancelled` request status. See §1.5. | PO → [FR-011 D4](../../project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md), [Schema §13](../../project-requirements/system-data-schema.md) |
| Q5 | `cancelled` in `inquiry_providers.status`: does FE know? | Not yet. It is part of the Q3 migration note. The patient sees "Offer Unavailable". For `after_cares.status`, the cascade **never** sets `cancelled`; that value is used only when an admin cancels a case explicitly with a reason ([Schema §13 L1505](../../project-requirements/system-data-schema.md)). | PRD [FR-004 L512](../../project-requirements/functional-requirements/fr004-quote-submission/prd.md); [Schema §5A L455](../../project-requirements/system-data-schema.md) |
| Q6 | `password_set` on the owner's `provider_users` row instead of `providers`. | **Accepted.** The flag lives on the Owner's `provider_users` row, and allocation reads the Owner's flag. The schema now matches (§4 `provider_users.password_set`; removed from §2 `providers`). Rollout: yes, Active providers without a set password stop receiving new inquiries. This is intended ([FR-003 CR](../../project-requirements/functional-requirements/fr003-inquiry-submission/change-request-2026-10-15-distribution-requires-password-set.md)). Add a release note, and on staging resend activation emails using the Resend Activation Email action ([FR-015 Alternative Flow A1, L169](../../project-requirements/functional-requirements/fr015-provider-management/prd.md)). | PRD: [FR-015 Rule 3 L765](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); [Schema §4 L334, §2 rule L174](../../project-requirements/system-data-schema.md) |
| Q7 | Can a suspended provider act on an `In Progress` booking? | **No, read-only.** No check-in, End Treatment or treatment-plan edits. The admin decides via FR-006 B7: move to Aftercare with reassignment, or cancel. | PO; PRD [FR-015 L703](../../project-requirements/functional-requirements/fr015-provider-management/prd.md), [FR-032 Rule 6](../../project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md), [FR-006 B7 L191](../../project-requirements/functional-requirements/fr006-booking-scheduling/prd.md) |
| Q8 | Unit of "Unresolved Support Items". | Per affected inquiry/case, linking to the FR-016 list filtered by provider and Admin Support Required. See §1.3. | PO → [FR-015 L744](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| Q9 | Do cancelled draft quotes notify the patient? Who gets the admin alert? | **Drafts are silent**: the patient never saw them, so a cancelled draft alone triggers no patient notice. `provider.status_cancellation_admin_support` goes to **admins with View Providers permission**, one per affected inquiry/case. | PO, written into [FR-004 L145](../../project-requirements/functional-requirements/fr004-quote-submission/prd.md) and [FR-020 L107–108](../../project-requirements/functional-requirements/fr020-notifications-alerts/prd.md) |
| Q10 | "Today": UTC or admin timezone? | **UTC.** | PO → [FR-015 L691, L622](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) |
| Q10 | A pending deactivation falls due when the provider is already suspended. | Apply it. Cascade any records still non-terminal, but **don't overwrite** an existing `ProviderSuspended` cause or re-cancel terminal records. Write a new status event. | PRD: [FR-015 L1163](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); [Schema §41](../../project-requirements/system-data-schema.md) |
| Q10 | Replace the legacy `POST /suspend/{id}` (`effective_date` TODO)? | Yes. Replace it with the Screen 4 contract: reason, notify flag, password, an optional Effective Date where a future date creates a §38 pending row, and the confirm flag. | PRD: [FR-015 Screen 4 L678+, L720](../../project-requirements/functional-requirements/fr015-provider-management/prd.md); [Schema §38](../../project-requirements/system-data-schema.md) |
| Q11 | Slot hold and duplicate-slot guard. | Resolved by Q2: the hold lives on the booking, and the unique index sits on `bookings`. | PO (via Q2); [Schema §11A](../../project-requirements/system-data-schema.md) |
| Q12 | Providers already Suspended or Deactivated before release: run the cascade once? | **No backfill; apply to new events only.** The current backend is a dev/test environment with no production or real patient data, so no live cases need relabelling. Revisit only if production data exists before release. | Delivery (PO confirmed) |
| Q13 | The repo's `docs/domain/booking-states.md` conflicts with PRD/schema. | **PRD and schema are canonical.** BE updates that doc. | PRD authority |
| Q14 | Notification content: official templates or BE/FE drafts? | FR-020 defines each event and its required content. Templates are managed by admins in **FR-030**. BE seeds default templates from the FR-020 content descriptions, and final wording can be edited in FR-030 without code changes. | PRD: [FR-020 L105–113, L331–332](../../project-requirements/functional-requirements/fr020-notifications-alerts/prd.md) |

---

## 3. Product Owner Decisions (2026-10-26)

| # | Topic | Decision |
|---|---|---|
| 1 | Provider status event | Dedicated `provider_status_events` table |
| 2 | Standalone aftercare | Reassign, don't cancel |
| 3 | Booking timing | Align FR-006 (booking at acceptance) before the cascade ships *(delivery decision, report only)* |
| 4 | Legacy statuses | Migrate in this release; BE delivers a migration note to the FE and Flutter devs *(delivery decision, report only)* |
| 5 | Suspended provider on In Progress | Read-only; admin decides via FR-006 B7 |
| 6 | Unresolved Support Items | One per affected inquiry/case |
| 7 | "Today" | UTC date everywhere |
| 8 | Validation error code | 422 + PRD wording |
| 9 | Draft quotes on suspension | Silent to patient (FR-004, FR-020) |
| 10 | Login as Provider | New tab; ends on End Session or 30-min inactivity; no absolute cap |
| 11 | Document Replace | Old file archived; no reason |
| 12 | Featured toggle | No change reason (still logged) |
| 13 | Leave-wizard prompt | FR-032 text, Stay / Leave, no drafts; added to PRD |
| 14 | UI copy (create success, featured cap, empty language) | Approved and added to PRD |
| 15 | Admin support alert recipient | Admins with View Providers permission (FR-020) |
| 16 | Seat-limit team size | FR-009 seat usage: members plus pending invitations (FR-015 L1154) |
| 17 | Pre-release Suspended/Deactivated providers (Q12) | No backfill *(delivery decision, report only)* |
| 18 | Upload error copy (HAIRL-1602) | English messages approved and added to FR-015 |
| 19 | FR-013 mock flags (HAIRL-1622) | Tab 5 Add/Edit/Remove waits for the FR-013 tasks to unmock *(delivery decision, report only)* |
| 20 | `password_set` storage (Q6) | Owner's `provider_users` row (BE placement); schema updated |

---

## 4. BE / FE Action Checklist

**BE**

1. **Shared contracts:**
   - Unify commission model values (`percentage`/`flat_rate`) and payout frequency values (`weekly`/`twice_monthly`/`monthly`), and migrate old rows.
   - Add `flat_rate_currency` and `effective_date`.
   - Require the concurrency token on every save, with a row lock.
   - Return 409 with the PRD text for conflicts and 422 with the PRD wording for validation errors.
2. **Commission:**
   - Insert and archive rows; never delete them.
   - Require a reason (10–500) and a password, and check permissions.
   - Validate 0 ≤ % ≤ 100 (0.1 precision) and flat > 0.
   - Effective Date ≥ today (UTC).
   - At most one scheduled configuration per provider; split shared scopes.
3. **Profile save:**
   - Persist languages (with order), awards (with issuer and order), information fields and documents.
   - Fix `years_experience` ↔ `years_of_experience`.
   - Accept multipart `POST` + `_method=PUT`.
   - Require a reason per REQ-015-025, except for Featured.
   - Enforce min 1 language server-side.
   - Stop accepting `commission.*` on the profile save.
   - Support removing the profile and cover images.
   - Send `awards.*.is_deleted` with the right type.
   - Return every Tab 1 field from `show()` (HAIRL-1605).
4. **Seat limit:**
   - Allow values below team size after the admin confirms, plus a password and a reason.
   - Count team size as members + pending invitations.
   - Apply the same rules on every path that writes Seat Limit; replace `justification` with `reason`.
5. **Documents:**
   - Add a Replace endpoint that archives the old file.
   - Block admin delete/replace of provider-uploaded documents with a clear error (403 recommended).
   - Return each file's correct MIME type and `uploaded_by`.
6. **Creation:**
   - Return the clinic name and the activation-email result.
   - Retry the email 3 times over 1 hour.
   - Stop firing `provider.onboarding_requested` on admin creation.
7. **Login as Provider:** take a reason and a password, use a sliding 30-minute inactivity expiry, and log the session.
8. **Cascade:**
   - Build booking-at-acceptance (FR-006) first.
   - Add `provider_status_events` and stamp its ID on affected records.
   - Treat standalone aftercare as reassignment.
   - Replace the legacy suspend route with the Screen 4 contract and §38.
   - Count Unresolved Support Items per inquiry/case.
   - Keep the provider read-only on In Progress bookings.
9. **Legacy status migration:** migrate the values, then **write a migration note for the FE and Flutter devs** covering the mapping, affected endpoints, new values such as `cancelled` / "Offer Unavailable", and the cut-over date.
10. **Housekeeping:** update `docs/domain/booking-states.md` to match the PRD and schema.

**FE**

- Send `flat_rate` and `twice_monthly` (not `flat` or `bi-monthly`).
- Allow 0% commission.
- Preselect the system currency.
- Add the leave-wizard prompt.
- Use the approved copy.
- Add a reason dialog (10–500 characters) to admin saves in Tabs 1, 2, 4 and 7, Tab 6 notes, and the seat limit.
- On a save conflict, keep the admin's input and offer Refresh.
- Reorder languages by drag-and-drop.
- Use a select list for Specialty.
- Accept PDF, JPG, PNG, DOCX and XLSX documents.
- Open Login as Provider in a new tab.
- Render the new status values from the BE migration note.

---

## 5. Documentation Changes Made

| Document | Version | Change |
|---|---|---|
| [FR-015 PRD](../../project-requirements/functional-requirements/fr015-provider-management/prd.md) | 1.21 | Key Entity 5 Provider Status Event; Screen 5 count unit; In Progress read-only; UTC "today"; Login as Provider tab and timeout; leave-wizard prompt; success, language and featured-cap copy; Featured and Replace need no reason; Replace archives the old file; 422; REQ-015-025; UTC on the wizard Commission Start Date; team size as FR-009 seat usage; upload error messages; REQ-015-011 owner `password_set`; change log and approval |
| [FR-011 PRD](../../project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md) | 1.6 | Standalone aftercare is reassigned, not cancelled (D4, Rule 4, REQ-011-014, edge case) |
| [FR-011 Change Request CR-FR011-20261026-01](../../project-requirements/functional-requirements/fr011-aftercare-recovery-management/change-request-2026-10-26-standalone-aftercare-reassignment.md) | — | Records the change from cancel to reassign for standalone aftercare; the 2026-10-14 and 2026-10-16 FR-011 Change Requests are marked partially superseded |
| [FR-004 PRD](../../project-requirements/functional-requirements/fr004-quote-submission/prd.md) | 3.5 | A draft quote cancelled by provider suspension or deactivation is silent to the patient |
| [FR-020 PRD](../../project-requirements/functional-requirements/fr020-notifications-alerts/prd.md) | 2.11 | Admin support alert goes to admins with View Providers permission; a cancelled unsent draft triggers no patient notice |
| [System data schema](../../project-requirements/system-data-schema.md) | 1.12.0 | New §41 `provider_status_events`; FK references updated; §13 standalone rule; table list; `password_set` moved to §4 `provider_users` |
| [Update log](../../project-requirements/update-logs/2026-10-26/FR015_DEV_QUESTIONS_RESOLUTION_2026-10-26.md) | — | Major-change log and README entries |

## 6. Still Open

None. The three items left open earlier were settled on 2026-10-26 (§3 items 18 to 20):

- **HAIRL-1602 English error copy:** approved and added to FR-015.
- **FR-013 mock flags (HAIRL-1622):** a delivery dependency; Tab 5 Add/Edit/Remove waits for the FR-013 tasks to unmock.
- **`password_set` storage (Q6):** BE placement accepted; the schema now matches.
