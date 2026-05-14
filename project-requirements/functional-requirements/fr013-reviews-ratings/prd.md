# FR-013 - Reviews & Ratings

**Module**: P-02: Quote Request & Management | PR-06: Profile & Settings Management | A-01: Patient Management & Oversight | S-03: Notification Service | S-05: Media Storage Service
**Feature Branch**: `fr013-reviews-ratings`
**Created**: 2025-11-11
**Status**: ✅ Verified & Approved
**Source**: FR-013 from local-docs/project-requirements/system-prd.md; Transcriptions (patient app, admin platform)

---

## Executive Summary

Enable patients with completed treatment cases to submit post-procedure reviews with structured ratings and optional photos, published immediately upon submission (no pre-publication moderation gate). The patient flow includes provider/clinic review display during provider evaluation, submitted-review list/detail views, and a takedown-request mechanism (patients cannot directly delete submitted reviews). Admin can insert authenticated reviews for provider profiles, edit existing reviews, remove reviews for policy/compliance reasons, configure review settings, export reports, and process takedown requests (approve/reject). Provider and Admin surfaces include list/filter/detail review management across treatment cases to support operational visibility and moderation.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (P-02): Submit review after confirmed completed treatment case (time-gated 3+ months), provide overall and category ratings, feedback, and optional photos; review is published immediately. Patient can browse provider/clinic reviews during provider review/offer evaluation, browse all submitted reviews, view review detail, and submit takedown requests.
- Provider Platform (PR-06 display context): View all published reviews across treatment cases, filter/sort reviews by key criteria (case, rating, date), open review detail, and post public responses.
- Admin Platform (A-01): Monitor all reviews with patient/provider/case filters, view and edit review details, remove reviews for policy/compliance reasons, insert authenticated reviews for provider profiles, and process takedown requests (approve/reject) with audit trail.
- Shared Services (S-05, S-03): Media Storage for review photos; Notification Service for invite reminders, provider reply alerts, admin removal notices, and takedown request status updates.

### Multi-Tenant Breakdown

Patient Platform (P-02):

- Receive invitation to review after procedure completion threshold.
- Submit ratings (overall 1–5 stars; category ratings) and feedback; optionally attach photos; review published immediately.
- View all submitted reviews across treatment cases and open review detail.
- Cannot directly delete submitted reviews; can submit takedown request to admin for decision.

Provider Platform (display + response):

- View published reviews on their profile across all treatment cases, with list filters and sorting.
- Open review detail to inspect ratings, feedback, photos, and case context.
- Post a public response to individual reviews; receive notification on new published reviews.

Admin Platform (A-01):

- Review management dashboard with filters (provider, patient, case, date, rating, status).
- View full review detail; edit or remove published reviews for policy/compliance violations (with reason).
- Insert authenticated reviews for provider profiles (flagged as "Verified Off-platform").
- Takedown request queue to review and approve/reject patient takedown requests.
- Manage review categories, display rules, moderation settings, and export reports; link out to FR-030 for invite/reminder cadence.

Shared Services (S-05, S-03):

- S-05 handles secure photo storage and retrieval.
- S-03 delivers invite/reminder emails/push and status notifications.

### Entry Points

- Time-gated invite after confirmed procedure completion (≥ 3 months) triggers review flow.
- Patient navigates to “Write a Review” from provider history.
- Patient views published reviews from provider profile/offer evaluation surfaces.
- Patient navigates to “Submitted Reviews” to view review history and request takedown from detail page.
- Providers access “Reviews” in dashboard to list/filter/detail reviews and respond.
- Admins access “Review Management”, “Takedown Requests”, and “Review Settings” from Admin platform navigation.

---

### Backlog (Future Enhancements)

- Interactive before/after progress timeline (including optional 3D scan timeline overlays) on review detail screens.

---

## Business Workflows

### Main Flow: Patient Submits a Review

Actors: Patient, System
Trigger: Patient opens “Write a Review” from invite or history
Outcome: Review published immediately with ratings, feedback, and optional photos; provider rating metrics updated

Prerequisites:

- Patient has a completed treatment case linked to the provider.
- Review submission is within allowed review window (≥ 3 months post-completion).

Steps:

1. Patient completes overall and category ratings, enters feedback, and optionally attaches photos.
2. System validates inputs (rating ranges, feedback length, file type/size) and verifies eligibility.
3. System publishes (or republishes, on edit) the review immediately and recalculates provider rating metrics (average, count, distribution) with associated cache invalidation. Recalculation applies whether the action is an initial submission or an edit to an already-published review.
4. On edit (republish), system also: (a) re-runs B2 automated flagging (keyword/duplicate/rate-limit checks) against the new payload, (b) sets `last_edited_at` and increments `edit_count`, (c) writes a full audit record (before/after values, actor=patient), and (d) notifies the provider that an existing review they may have responded to was edited so they can re-evaluate their response.
5. Patient sees confirmation; review is live on provider profile and appears in Patient “Submitted Reviews” list. Edited reviews surface an "Edited {relative_time}" marker on all public surfaces (Patient list, Patient detail, Provider list/detail, Provider Profile Reviews Section) so readers can distinguish current content from the original publish.

### A1: Admin Inserts Authenticated Review

- Trigger: Admin receives authenticated external review evidence for provider profile seeding.
- Steps:
  1. Admin enters review payload (ratings, feedback, optional photos, source evidence).
  2. System validates fields and stores source provenance.
  3. System publishes review flagged as "Verified Off-platform".
- Outcome: Provider profile receives seeded review with explicit provenance marker and full audit record.

### A2: Admin Edits Existing Review

- Trigger: Admin identifies correction or compliance need on an existing review.
- Steps:
  1. Admin opens review detail and applies edits/redactions.
  2. System records before/after values, reason, and admin identity.
- Outcome: Review is updated per admin action; audit trail preserved.

### A3: Patient Submits Takedown Request

- Trigger: Patient opens submitted review detail and chooses "Request Takedown".
- Steps:
  1. Patient taps "Request Takedown"; system opens confirmation bottom sheet/modal over review detail.
  2. Patient enters a required takedown reason and confirms takedown request.
  3. System records patient reason, creates takedown request with `Pending` status, and links it to review/case.
  4. System notifies admin takedown queue.
- Outcome: Takedown request enters admin processing queue; review remains visible until decision.

### A4: Admin Processes Takedown Request

- Trigger: Admin opens pending takedown request from queue.
- Steps:
  1. Admin reviews request reason, review content, and compliance context.
  2. Admin approves or rejects request with decision note.
  3. System applies decision: approved -> review unpublished/archived and provider rating metrics recalculated; rejected -> review remains published.
  4. System notifies patient of decision and reason.
- Outcome: Takedown request resolved with audit log, provider metrics updated, and patient notification.

### B1: Provider Response

- Trigger: Provider posts a response to a published review.
- Steps:
  1. Provider opens Review Detail (Screen 6) and taps "Respond as Provider".
  2. System opens inline response composer/modal state within Screen 6.
  3. Provider writes response; system validates length and policy.
  4. Provider confirms submission; system publishes response under provider identity.
- Outcome: Response visible with the review; patient notified.

### B2: Flagging/Inappropriate Content

- Trigger: Content flagged by system-automated detection (keyword matching, duplicate submission patterns, rate-limit triggers). User-initiated flagging is a future enhancement.
- Steps: System queues flagged content for admin review; Admin may redact, unpublish, or uphold.
- Outcome: Policy-compliant content remains; violations are removed with audit record.

---

## Screen Specifications

### Patient Platform

#### Screen 1: Patient – Submit Review

Purpose: Allow eligible patients to submit a structured review post-procedure.

Data Fields:

| Field Name         | Type        | Required | Description                                  | Validation Rules                         |
| --- | --- | --- | --- | --- |
| Clinic Name        | text        | Yes      | Read-only clinic/provider label at top of form | Read-only; derived from booked provider |
| Treatment Name     | text        | Yes      | Read-only treatment label at top of form       | Read-only; derived from completed procedure |
| Overall Rating     | 1-5 stars   | Yes      | Overall experience                              | Integer 1-5 |
| Facility Rating    | 1-5 stars   | Yes      | Facility cleanliness                            | Integer 1-5 |
| Staff Rating       | 1-5 stars   | Yes      | Staff professionalism                           | Integer 1-5 |
| Results Rating     | 1-5 stars   | Yes      | Results satisfaction                            | Integer 1-5 |
| Value Rating       | 1-5 stars   | Yes      | Value for money                                 | Integer 1-5 |
| Feedback           | textarea    | Yes      | Narrative experience                            | 100-2000 chars; 100-char minimum ensures reviews contain enough substance to be useful to other patients |
| Photos             | image list  | No       | Optional before/after images                    | Up to 5 files; jpg/png; max 10MB each |

Business Rules:

- Eligibility enforced (completed procedure and ≥ 3 months).
- One review per completed procedure; patient can edit their published review at any time.
- Review is published immediately upon submission — no pre-publication moderation gate.
- Clear photo guidelines; sensitive/identifying content discouraged.
- The save action persists the current review payload and immediately publishes valid patient submissions.

Data Contract (Patient Form Payload):

- `clinic_name` (display only, read-only context)
- `treatment_name` (display only, read-only context)
- `overall_rating` (1-5)
- `facility_rating` (1-5)
- `staff_rating` (1-5)
- `results_rating` (1-5)
- `value_rating` (1-5)
- `feedback_text`
- `photos[]`

Notes:

- Rating rows use a row-select interaction pattern (tap row to set/update score); selected values display in `X/5 star` format.
- Disclose display policies and admin's right to remove for violations.
- Feedback length bounds (100–2000 chars): 100-char minimum ensures substantive content for other patients; 2000-char ceiling deters off-topic walls of text and reduces spam/abuse surface area without truncating genuine narrative experience.

---

#### Screen 2: Patient – Submitted Reviews List (My Reviews)

Purpose: Allow patient to view all submitted reviews across treatment cases.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Screen title | text | Yes | "My Reviews" | Display only |
| Header sort icon | action icon | No | Sort/reorder action in top-right header | Opens sort options |
| Review list | list | Yes | All patient-submitted reviews grouped by treatment case/provider | Sorted by newest first; paginated |
| Rating + time row | group | Yes | Star rating with relative time (e.g., "5 days ago") | Read-only |
| Status | badge | Yes | Published / Removed | Patient-facing review visibility status; color-coded |
| Takedown request status | badge | Conditional | Pending / Approved / Rejected | Shown only when a takedown request exists; sourced from takedown request workflow, not review status |
| Treatment line | text | Yes | "Treatment: {treatment_name}" | Read-only |
| Review excerpt | text | Yes | Truncated narrative preview | Max 2 lines + "See more" affordance |
| Provider row | group | Yes | Provider avatar + provider name | Read-only |
| Sort option | select | No | Reorder list by selected criterion | Default: Most recent first |
| Open detail | action | Yes | Opens selected review detail | Navigates to Screen 3 |
| Empty state | text | No | "No reviews yet - complete a treatment to leave a review" | Shown when patient has no submitted reviews |

Business Rules:

- Includes all submitted reviews for the logged-in patient across all completed treatment cases.
- Review status badge uses app-facing labels: `Published`, `Removed`.
- `Submitted` is not a review status in V1; successful review submission immediately creates a `Published` review.
- Takedown request state is displayed separately from review status when applicable (`Pending`, `Approved`, `Rejected`).
- `Removed` means no longer publicly visible due to admin action or approved takedown.
- Default list sort is latest submission date descending.

---

#### Screen 3: Patient – Review Detail & Takedown Request

Purpose: Show full submitted review content (including provider response when available), allow edit for published reviews, and allow takedown request via confirmation modal.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Review detail payload | card | Yes | Full ratings, feedback, photos, provider, treatment context | Read-only in detail mode |
| Review submission date | datetime | Yes | Date/time the review was submitted | Read-only |
| Current status | badge | Yes | Published / Removed | Read-only review visibility status |
| Takedown request status | badge | Conditional | Pending / Approved / Rejected | Shown when the review has an associated takedown request |
| Provider response block | card | No | Provider response content, timestamp, and role badge | Shown only when provider response exists |
| Admin removal reason | text | No | Reason supplied by admin when review is removed | Shown only when status = Removed |
| Edit review | button | Conditional | Opens pre-filled edit form | Visible only when status = Published |
| Request takedown | button | Conditional | Opens takedown confirmation bottom sheet/modal | Visible only when status = Published |
| Takedown reason | textarea | Yes (when requesting) | Required patient reason for admin context | 10–1000 chars |
| Retention notice | info text | Yes (when requesting) | "Review content will be removed from public view but archived for a 7-year minimum (medical-records retention). Audit records of this takedown are retained for 10 years (audit-log policy)." | Display-only policy text; reflects split retention per Data & Privacy Rules |
| Submit takedown request | action | Yes (when requesting) | Sends request to admin queue | Confirmation required |

Business Rules:

- Patient cannot directly delete a submitted review.
- For `Published` status, both `Edit Review` and `Request Takedown` actions are available.
- For `Removed` status, detail is read-only and shows admin removal reason; edit/takedown actions are hidden.
- `Edit Review` opens pre-filled form fields; saved edits are published immediately (no moderation gate).
- Takedown request is submitted from a bottom sheet/modal with required reason and mandatory retention-policy notice.
- Takedown request creates a pending admin review record.
- While request status is `Pending`, review remains `Published` unless manually removed by admin.

#### Screen 4: Patient – Provider Profile Reviews Section

Purpose: Define the reviews section embedded inside the patient-facing provider profile shown during quote/provider evaluation.

Context Note:

- This is not a standalone full provider profile screen. It specifies only the FR-013 review-related section and interactions inside the existing provider profile screen used in the quoting process.
- Non-review provider profile content (about text, languages, staff, certifications, awards, location, and provider messaging entry points) belongs to the provider profile / quote-review screen specifications and is not duplicated here.
- The embedded review section must connect to the same review data model used by patient-submitted reviews, provider response surfaces, and admin review management.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Host provider context | reference | Yes | Current provider/clinic profile being reviewed in the quote flow | Read-only; supplied by host provider profile screen |
| Rating summary teaser | stats row | Yes | Average rating, star display, total review count, and `View all` entry point near provider heading | Read-only; cached summary allowed |
| Reviews section heading | text/action row | Yes | Reviews heading with optional `View all` action | Display only; action opens full review list state |
| Review preview list | list | Yes | Preview reviews shown within provider profile screen | Published reviews only; limited count before `View all` |
| Full reviews list state | list/overlay/subview | Conditional | Expanded review list opened from `View all` | Paginated; newest first by default |
| Reviewer alias | text | Yes | Public reviewer display name | Uses alias by default; no PII exposure |
| Rating + date row | group | Yes | Overall rating and submitted date/relative time | Read-only |
| Treatment context | text | No | Treatment/procedure context when display-safe | Read-only; no sensitive details |
| Review excerpt/body | text | Yes | Review feedback preview or full content | Preview truncates with "See more" affordance |
| Photos | image list | No | Public review photos/thumbnails | Display only approved/public photos |
| Provider response block | card | No | Provider response content and timestamp | Shown only when response exists |
| Verified off-platform badge | badge | Conditional | Provenance marker for admin-seeded authenticated reviews | Required for admin-seeded reviews |
| Sort/filter controls | controls | No | Sort by recency/rating and filter by rating | Full reviews list state only |
| Open review detail | action | No | Opens expanded review content | May use in-screen expansion, modal, or host-defined subview |

Business Rules:

- Only `Published` reviews are visible on patient-facing provider/clinic profile surfaces.
- The embedded preview must not redefine or duplicate the full provider profile layout; it inherits provider identity and navigation from the host provider profile screen.
- `View all` opens the complete review list for the same provider without changing review ownership or source rules.
- Reviewer identity is aliased by default and must not expose patient PII.
- Admin-seeded reviews must display the `Verified Off-platform` marker.
- Provider response displays with the review when available.
- Review photos shown publicly must follow the same media privacy and removal rules as submitted review photos.

---

### Provider Platform

#### Screen 5: Provider – Reviews List & Filters

Purpose: Show all provider reviews across treatment cases with filtering.

Context Note:

- This review list can appear as a dedicated Provider Dashboard reviews list and may also be embedded or linked from the provider's own profile detail section.
- Final placement is a UX/UI design decision; the designer may place this list wherever it best fits the provider dashboard/profile experience.
- When embedded in provider profile detail, this screen specifies only the review list/filter behavior; non-review provider profile fields remain owned by the provider profile detail specification.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Ratings summary | stats | Yes | Average rating, count, distribution | Read-only |
| Review list | list | Yes | All published reviews tied to provider | Paginated; newest first by default |
| Review source type | badge | Yes | Patient-submitted / Verified Off-platform | Read-only |
| Reviewer alias | text | Yes | Patient alias or off-platform reviewer label | Read-only; no PII exposure |
| Case/treatment context | text | Yes | Treatment case and treatment/procedure context | Read-only |
| Response status | badge | Yes | No response / Responded | Read-only |
| Filters | controls | No | Filter by patient, case, rating range, date range, response status, source type | Multi-filter |
| Sort | select | No | Sort reviews by recency or rating | Default: recency |
| Open detail | action | Yes | Opens selected review detail | Navigates to Screen 6 |

Business Rules:

- One patient may have multiple treatment cases; list must support case-specific filtering.
- Only published reviews appear in provider list surfaces.

---

#### Screen 6: Provider – Review Detail & Response

Purpose: Let provider inspect review details and post public response.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Review detail payload | card | Yes | Canonical review payload (ratings, feedback, photos, treatment case context) | Read-only |
| Review source type | badge | Yes | Patient-submitted / Verified Off-platform | Read-only |
| Reviewer alias | text | Yes | Public reviewer label | Read-only; no PII exposure |
| Photos | image list | No | Review photos and thumbnails | Read-only |
| Provider response card | display block | No | Persisted provider response content, author, role, timestamp | Shown when response exists |
| Respond as Provider | button | Conditional | Opens response composer | Visible only when review is published and no response exists |
| Response composer | inline panel/modal | Conditional | Non-navigating response input surface within this screen | Opens from `Respond as Provider` |
| Response text | textarea | Yes (when composing) | Provider's public response body | 50-1000 chars |
| Character counter | indicator | Yes (when composing) | Remaining character count | Live update; blocks submit outside limits |
| Cancel response | button | Yes (when composing) | Close composer without publishing | Confirmation prompt if unsaved content exists |
| Submit response | action | Yes (when composing) | Publish provider response | Enabled only when validation passes |

Business Rules:

- Provider responses are public and immutable while published; admins may remove a response for policy violation. After an admin removal, the provider may submit exactly one replacement response (see one-active-response rule below) — outside of that single replacement, posted responses cannot be edited or re-posted by the provider.
- Detail view must preserve treatment-case context so provider can differentiate multi-case patient histories.
- Provider may have at most one active public response per review in V1. If admin removes a prior response for policy violation, provider may submit one replacement response; both the removed and replacement responses are retained in the audit trail (`AdminAction` for the removal, `ProviderResponse` history for the lifecycle).
- Composer is an inline state of this screen, not a separate navigation screen.
- Submission records provider identity and timestamp and triggers patient notification.

Notes:

- Encourage professional tone; display response timestamp and provider role.
- Response length bounds (50–1000 chars): 50-char minimum prevents single-word or non-substantive replies that erode trust; 1000-char ceiling keeps public responses scannable on review surfaces and discourages defensive long-form rebuttals.

---

### Admin Platform

#### Screen 7: Admin – Reviews Management List

Purpose: Monitor all reviews in the system with operational filters.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Reviews list | list | Yes | Global list of all reviews | Paginated; system-wide |
| Source type | badge/filter | No | Patient-submitted / Verified Off-platform | Read-only badge; filterable |
| Flagged status | badge/filter | No | Flagged / Not flagged | Read-only badge; filterable |
| Response status | badge/filter | No | No response / Responded | Read-only badge; filterable |
| Filters | controls | No | Provider, patient, treatment case, status, date, rating, source type, flagged status | Multi-filter |
| Search | text | No | Search by patient/provider/case identifiers | Min 2 chars |
| Open detail | action | Yes | Open selected review detail/edit view | Navigates to Screen 8 |
| Open takedown queue | action | Yes | Navigate to takedown requests | Navigates to Screen 9 |
| Open review settings | action | No | Navigate to review settings/export | Navigates to Screen 10 |

Business Rules:

- Admin list includes patient-submitted and admin-seeded reviews.
- Review visibility/filter results must preserve complete audit traceability.

---

#### Screen 8: Admin – Review Detail, Insert & Edit

Purpose: Let admin inspect review details, edit/remove reviews, and insert new authenticated reviews.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Review detail payload | card/form | Yes | Full review content and metadata | Canonical schema |
| Source type | badge/select | Yes | Patient-submitted / Verified Off-platform | Read-only for existing patient reviews; required for admin add |
| Flagged status | badge | No | Auto/manual flag state and reason | Read-only unless admin resolves flag |
| Audit trail preview | timeline | Yes | Recent admin actions and state changes | Read-only; full audit retained |
| Edit fields | form controls | No | Redaction/correction fields for existing review | Reason required for edit |
| Remove review | action | No | Unpublish + archive review | Removal reason min 10 chars |
| Add review | action | No | Create new authenticated provider review | Requires provenance inputs |
| Source verification | form group | Yes (for add) | Structured `source_metadata` payload (see below) capturing provenance and consent for seeded review | All required sub-fields must be provided for admin-seeded items; persisted to `Review.source_metadata` |
| → Source platform | select | Yes (for add) | Origin of the off-platform review (e.g., Google, Trustpilot, Doctolify, Provider Website, Email Testimonial, Other) | Enum; "Other" requires free-text platform name |
| → Source URL | url | Conditional (for add) | Public link to original review when available | Valid URL; required unless `source_platform = Email Testimonial` |
| → Evidence file(s) | file upload | Yes (for add) | Screenshot/PDF/email capture of the original review | 1–5 files; jpg/png/pdf; max 10MB each; stored via S-05 |
| → Capture date | date | Yes (for add) | Date the evidence was captured/observed | ISO date; not in future |
| → Permission record | file or text + checkbox | Yes (for add) | Patient/reviewer consent artifact (signed permission, email screenshot, or written consent reference) + admin attestation checkbox confirming consent was obtained | Either file upload OR text reference + mandatory admin attestation |
| → Reviewer display name | text | Yes (for add) | Admin-entered alias to show publicly (see reviewer alias rule under Data & Privacy Rules) | PII-safe; no full last name; no contact info |
| Patient/reviewer photo | image upload | No (for add) | Optional reviewer image for authenticated seeded reviews | Must follow media policy |
| Removal/edit reason | select + textarea | Conditional | Reason catalog plus optional details | Required for edit/remove |

Business Rules:

- Every admin add/edit/remove action records admin identity, timestamp, reason, and before/after changes.
- Admin-seeded reviews must be flagged as "Verified Off-platform" with verification provenance.
- Removed reviews are unpublished + archived (not hard deleted).

---

#### Screen 9: Admin – Takedown Requests Queue

Purpose: Review and decide patient takedown requests.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Request queue | list | Yes | Pending/resolved takedown requests | Filterable by status/date |
| Request metadata | group | Yes | Request ID, created date, requester, provider, treatment case | Read-only |
| Linked review preview | card | Yes | Review summary linked to request | Read-only |
| Current review status | badge | Yes | Published / Removed | Read-only |
| Request reason | text | Yes | Patient-submitted reason | Read-only |
| Decision action | controls | Yes | Approve / Reject takedown | Decision note required |
| Decision note | textarea | Yes | Admin justification for decision | 10-1000 chars |
| Admin removal reason | textarea | Conditional | Patient-facing reason shown on Screen 3 after approved takedown/removal | Required when approving takedown; persisted to removed review record |
| Decision history | timeline | No | Prior decisions/updates on resolved requests | Read-only |
| Decision timestamp | datetime | Conditional | When request was resolved | Read-only after decision |

Notes:

- Approve decision: review unpublished + archived.
- Approved takedown must persist `Admin removal reason` on the removed review so Patient Review Detail (Screen 3) can display the same reason consistently.
- Reject decision: review remains published.
- Patient must be notified for both outcomes.
- Admin tooling must read/write the same canonical review schema as patient/provider surfaces to prevent cross-tenant drift.

---

#### Screen 10: Admin – Review Settings & Export

Purpose: Configure review display policy controls and operational exports, with link-outs to FR-030 for review invitation cadence and reminders.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Review categories/labels | editable list | Yes | Category rating labels used by review forms and displays | Admin-editable labels; canonical keys remain fixed |
| Invitation cadence link-out | navigation | Yes | Entry point to FR-030 Notification Rules & Configuration where `review.requested` event timing/cadence is owned | Read-only here; configured in FR-030 |
| Reminder settings link-out | navigation | No | Entry point to FR-030 for reminder count/timing on review invitations | Read-only here; configured in FR-030 |
| Photo guidelines text | rich text/textarea | Yes | Patient-facing photo upload guidance | Required; audit-logged (all edits captured via AdminAction with before/after values; no formal version model) |
| Removal reason catalog | editable list | Yes | Standard reasons for admin removals/redactions | At least one active reason |
| Reviewer display policy | controls | Yes | Alias/full-name policy settings | Defaults to alias; PII-safe |
| Flagging thresholds | controls | No | Duplicate/spam/keyword flag settings | Restricted safe ranges only |
| Takedown SLA settings | controls | No | Queue priority/SLA target | Restricted policy range |
| Export reviews report | action | No | Export reviews/audit/takedown reports | RBAC-restricted; audit logged |

Business Rules:

- Settings changes are admin-only and audit logged.
- Settings must not weaken fixed eligibility, rating scale, text length, retention, or privacy rules.
- Export actions must preserve RBAC, PII handling, and audit traceability.

---

## Business Rules

### General Module Rules

- Eligibility check required: only patients with a completed procedure may review.
- Time gating: review invitation and entry allowed ≥ 3 months post-procedure.
- One review per completed procedure.
- Patient cannot directly delete submitted reviews; takedown requires admin decision workflow.
- Ratings use 1–5 scale with half‑stars display allowed for averages.

### Data & Privacy Rules

- Patient display name uses aliasing by default; see canonical reviewer alias algorithm below.
- Photos and text must not expose sensitive personal information; admin may redact or remove post-publication.
- Review content (review record + photos + provider responses + takedown requests) retained for minimum 7 years (medical-records baseline, Constitution §III.A); approved takedown requests are processed by unpublish + archival with restricted access — never hard-deleted.
- `AdminAction` and all audit-log records (patient self-edits, admin edits/removals/seeded reviews, takedown decisions, settings changes, provider responses) are immutable and retained for minimum 10 years per Constitution §VI (Audit Trail). The 10-year audit-log retention is independent of and longer than the 7-year review-content retention.
- All review mutations are fully auditable (who, when, what, before/after, reason where applicable), including patient self-edits to published reviews, admin actions (edits, removals, seeded reviews, takedown decisions, settings changes), and provider response creation. Audit records preserve actor type (patient / provider / admin) and prior field values to satisfy constitution Auditability requirements.
- Reviewer alias algorithm (canonical, applied uniformly across Patient, Provider, and Admin public surfaces): `{first_name} {last_initial}.` (e.g., "Sarah M."); collisions within the same provider's review list are deduplicated with a numeric suffix (`Sarah M. 2`, `Sarah M. 3`, …). Admin views may unmask to full identity per RBAC. Admin-seeded reviews use an admin-entered `reviewer_display_name` field (free text, subject to the same PII-safety policy — no full last name, no contact info) instead of the algorithmic alias; the `Verified Off-platform` badge accompanies the display name. Patients have no opt-in to expose full name in V1; reviewer display policy toggle on Screen 10 governs only future policy expansion and MUST default to alias-only.

### Admin Editability Rules

Editable by Admin:

- Review categories/labels; invitation cadence and reminders.
- Photo guidelines text; removal reasons catalogue.
- Visibility rules for display name (alias/full name toggle policy).
- Insert authenticated reviews and edit/remove existing reviews with mandatory reasons.

Fixed in Codebase (Not Editable):

- Eligibility logic requires completed procedure and time threshold.
- Minimum and maximum lengths for text fields and rating scale bounds.

Configurable with Restrictions:

- Flagging thresholds and auto-flag rules for admin review (within safe bounds approved by policy).
- Takedown decision SLA/queue prioritization parameters (within policy bounds).

Admin-Seeded Review Policy:

- Admin-imported authenticated reviews must be flagged as "Verified Off‑platform" with verification source and date. These are published directly by admin (no patient submission flow).

---

## Success Criteria

### Patient Experience Metrics

- SC-001: 90% of eligible patients can complete a review in ≤ 3 minutes.
- SC-002: ≥ 30% invite‑to‑review conversion within 14 days of invite.
- SC-003: 95% of photo uploads validate on first attempt (guidelines clear).
- SC-004: 95% of provider profile review sections load enough summary context for patient comparison without opening admin/provider tools.

### Provider Efficiency Metrics

- SC-005 *(Business KPI — tracked via FR-014 analytics, not enforced by this module)*: 80% of published reviews receive a provider response within 5 business days.
- SC-006: Providers can locate any review and respond in ≤ 60 seconds.

### Admin Management Metrics

- SC-007: 95% of flagged reviews receive an admin review decision within 48 hours.
- SC-008: 95% of takedown requests receive an admin decision within 48 hours.
- SC-009: 100% of admin actions (insert, edit, remove, takedown decision, settings change, export) capture admin identity, timestamp, and reason/action context in audit log.

### System Performance Metrics

- SC-010: Ratings summary loads in ≤ 1 second for 95th percentile.
- SC-011: Zero data loss of submitted reviews; photos stored reliably with secure access.
- SC-012: 99.9% monthly uptime for review submission and viewing.

### Business Impact Metrics

- SC-013: Provider profile conversion rate improves by ≥ 10% after launch.
- SC-014: Average content volume reaches ≥ 3 new reviews per active provider/month by month 3.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- P-01: Auth & Profile Management – identity and role context.
- P-03: Booking & Payment – confirm procedure completion and dates for eligibility/time gating.
- PR-06: Provider Profile & Settings Management – provider review display context, provider response surface, and provider review notification preference consumption.
- FR-014: Provider Analytics & Reporting – consumes review ratings, sub-scores per treatment, and aggregate trends; FR-013 must expose published ratings, category sub-scores, and recalculated averages to FR-014's analytics pipeline.
- FR-020: Notifications & Alerts / S-03 Notification Service – invite/reminder delivery, new published review alerts to providers, provider response alerts, admin removal notices, and takedown decision notifications.
- FR-022: Search & Filtering – provider/admin review list filters and search fields must remain represented in the FR-022 master reference when filter criteria change.
- FR-030: Notification Rules & Configuration – configurable review event mapping, recipient/channel rules, reminder cadence, and notification templates.
- FR-032: Provider Dashboard Settings & Profile Management – provider organization-level review notification preference toggle and channel settings.
- S-05: Media Storage Service – secure handling of review photos.
- S-03: Notification Service – invitations, reminders, admin removal notifications, and provider response alerts.

### External Dependencies (APIs, Services)

- Email/push delivery providers for notifications (through S-03).

### Data Dependencies

- Completed procedure records with completion date and provider association.
- Provider profile identifiers for correct attribution and display.

---

## Assumptions

### User Behavior Assumptions

- Patients are willing to leave reviews when prompted and informed of display policies.
- Providers will respond to reviews to improve public trust.

### Technology Assumptions

- Modern mobile and web clients used; stable connectivity for uploads.
- Secure media storage available; common image formats supported.

### Business Process Assumptions

- Admin team monitors flagged reviews and review management dashboard during business hours.
- Legal/compliance guidance exists for defamation and takedown handling.

---

## Implementation Notes

### Technical Considerations

- Architecture: Reviews published immediately on write; admin audit logs for post-publication edits and removals.
- Media handling: Validate size/type, generate thumbnails; protect access.
- Anti‑abuse: Duplicate detection, keyword flags, rate limits for submissions and responses.
- Takedown workflow: separate `takedown_requests` state machine with decision history and notification hooks.

### Integration Points

- Patient app → Review service: submit (published immediately), list submitted reviews, review detail, request takedown, status tracking.
- Patient app/provider profile surfaces → Review service: published review display, ratings summary, public-safe media, provider responses, verified off-platform markers.
- Admin dashboard → Review service: global review list/filter, review detail, add/edit/remove, takedown queue decisioning, review settings, exports, audits.
- Provider dashboard → Review service: list/filter/detail published reviews, post responses.

### Scalability Considerations

- Caching of ratings summary and distribution per provider.
- Paging and lazy load for reviews lists; background processing for photo thumbnails.

### Security Considerations

- Enforce RBAC for submit/moderate/respond actions.
- Encrypt data in transit and at rest; signed URLs for media.
- Full audit trail for all state changes; soft‑delete (unpublish) for takedowns.

---

## User Scenarios & Testing

### User Story 1 – Patient views provider/clinic reviews (P1)

Why: Patients need credible review evidence while comparing providers or reviewing an offer.

Independent Test: Patient opens a provider profile or offer provider section and can inspect published reviews, ratings summary, review photos, provider responses, and verified off-platform markers without seeing private reviewer data.

Acceptance Scenarios:

1. Given a provider with published reviews, when the provider profile review section loads, then the patient sees rating summary, review count, distribution, and review cards.
2. Given a review has a provider response, when the patient expands or opens the review, then the provider response appears with timestamp/context.
3. Given an admin-seeded review, when it appears publicly, then it is marked `Verified Off-platform`.

### User Story 2 – Patient submits a review (P1)

Why: Capture authentic post‑procedure experience to inform others.

Independent Test: Eligible test patient submits review with photos; review is published immediately and visible on provider profile.

Acceptance Scenarios:

1. Given an eligible patient, when they submit required ratings and feedback, then the review is published immediately and the patient sees confirmation.
2. Given valid photos, when uploaded, then the system accepts and associates them with the review.
3. Given a published review, when the provider profile loads, then averages and distribution reflect the new review.

### User Story 3 – Patient requests takedown for submitted review (P1)

Why: Give patient a governed way to remove review visibility without direct hard delete.

Independent Test: Patient submits takedown request from review detail; admin receives pending request and patient receives final decision notification.

Acceptance Scenarios:

1. Given a published review, when patient submits takedown request with reason, then request is created with `Pending` status and visible in admin queue.
2. Given a pending request, when admin approves it, then review is unpublished/archived, metrics are recalculated, and patient is notified.
3. Given a pending request, when admin rejects it, then review remains published and patient receives rejection reason.

### User Story 4 – Provider reviews feedback across treatment cases (P1)

Why: Provider needs operational visibility for multi-case patient histories.

Independent Test: Provider opens reviews list, filters by treatment case/rating/date, and opens review detail.

Acceptance Scenarios:

1. Given provider with many reviews, when they apply filters (case/rating/date), then list returns only matching reviews.
2. Given selected review, when provider opens detail, then full canonical payload and case context are displayed.

### User Story 5 – Admin inserts/edits/removes reviews (P1)

Why: Admin must maintain provider profile quality and policy compliance.

Independent Test: Admin creates authenticated seeded review, edits an existing review, and removes a policy-violating review with complete audit trail.

Acceptance Scenarios:

1. Given verification evidence, when admin inserts review, then review is published with `Verified Off-platform` marker and provenance.
2. Given existing review, when admin edits or redacts fields, then system logs before/after with reason.
3. Given policy violation, when admin removes review, then review is unpublished/archived and patient is notified.

### User Story 6 – Provider responds to a review (P2)

Why: Encourage constructive dialogue and trust.

Independent Test: Provider posts a response; response appears under the review and patient is notified.

Acceptance Scenarios:

1. Given a published review, when a provider posts a response, then it appears publicly under the review.
2. Given a new response, when notifications trigger, then the reviewer receives a notification.

### User Story 7 – Admin configures review settings and exports reports (P2)

Why: Admin needs controlled configuration for review labels, display policy, flagging thresholds, and reporting without changing fixed compliance rules; invite/reminder timing is configured through FR-030 link-outs.

Independent Test: Admin updates review settings and exports a report; changes are audit logged and fixed eligibility/privacy/retention rules remain unchanged.

Acceptance Scenarios:

1. Given admin updates review labels or review display settings, when settings are saved, then the change is audit logged and future review flows use the updated setting.
2. Given admin exports reviews or takedown data, when export completes, then the export is RBAC-restricted and audit logged.

### Edge Cases

- Ineligible attempts (too early/no completed procedure) are blocked with clear messaging.
- Photos exceed limits: user informed, upload prevented until compliant.
- Duplicate or spam reviews: auto‑flag for admin review post-publication.
- Takedown request approved: review unpublished and archived; provider metrics recalculated.
- Takedown request rejected: review stays published; decision reason visible to patient.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-013-001**: System MUST allow eligible patients to submit reviews (overall + categories, feedback, optional photos).
- **REQ-013-002**: System MUST enforce time gating (≥ 3 months) and single review per completed procedure.
- **REQ-013-003**: System MUST publish reviews immediately upon patient submission (no pre-publication moderation gate).
- **REQ-013-004**: System MUST provide patient submitted-review list and review-detail views across treatment cases.
- **REQ-013-005**: System MUST provide patient takedown request flow (submit -> pending -> admin decision -> notification), and MUST NOT allow direct patient deletion of submitted reviews.
- **REQ-013-006**: System MUST display published reviews on patient-facing provider/clinic profile and offer-evaluation surfaces with ratings summary, review list, provider responses, public-safe media, and `Verified Off-platform` markers when applicable.
- **REQ-013-007**: System MUST provide admin capabilities to insert authenticated reviews, edit existing reviews, remove reviews, and process takedown requests with full audit trail.
- **REQ-013-008**: System MUST calculate and display provider average rating, count, and distribution.
- **REQ-013-009**: System MUST provide provider-side list/filter/detail screens across treatment cases, including filtering by patient, case, rating, date, response status, and source type.

### Data Requirements

- **REQ-013-010**: System MUST link reviews to patient, provider, and completed procedure records.
- **REQ-013-011**: System MUST securely store and retrieve review photos with metadata.
- **REQ-013-012**: System MUST persist takedown request records including reason, status, decision note, requester, decider, and timestamps.
- **REQ-013-013**: System MUST preserve a single canonical review schema across Patient, Provider, and Admin platforms (`overall_rating`, `facility_rating`, `staff_rating`, `results_rating`, `value_rating`, `feedback_text`, `photos[]`, plus read-only clinic/treatment context fields).

### Security & Privacy Requirements

- **REQ-013-014**: System MUST alias reviewer identity by default and prevent exposure of PII in public views.
- **REQ-013-015**: System MUST encrypt review data and photos in transit and at rest and maintain auditable logs.
- **REQ-013-016**: System MUST support unpublish + archival for compliance removals and approved takedown requests.

### Integration Requirements

- **REQ-013-017**: System MUST send invite/reminder and status notifications (new published review to provider, provider reply, admin removal, takedown decision) via Notification Service.
- **REQ-013-018**: System MUST provide ratings summary endpoints for provider profiles with caching.
- **REQ-013-018a**: System MUST additionally expose a per-treatment aggregated sub-scores endpoint that returns, for a given provider, `{treatment_id → {avg_overall, avg_facility, avg_staff, avg_results, avg_value, review_count, distribution}}` over Published reviews only. This endpoint is the data contract consumed by FR-014 "review sub-scores per treatment" analytics; cache invalidation MUST be triggered on every review publish, edit republish, removal, and approved takedown.
- **REQ-013-019**: Patient Review Detail MUST display provider response (when available), admin removal reason (when removed), and support pre-filled edit flow for published reviews.
- **REQ-013-020**: Takedown request submission MUST use a confirmation modal/bottom-sheet with required patient reason and explicit 7-year retention-policy notice before submission.
- **REQ-013-021**: Provider Review Detail MUST include a documented inline response-composer model/state (not separate screen navigation) with validation, cancel/confirm behavior, and immutable post-publish response rendering.
- **REQ-013-022**: Admin Review Settings MUST support review category labels, photo guidelines, removal reason catalog, reviewer display policy, restricted flagging/SLA settings, and RBAC-restricted export actions with audit logging. Review invitation and reminder cadence are owned by FR-030 (Notification Rules & Configuration); Screen 10 provides link-outs only.

### Marking Unclear Requirements

No unresolved clarifications remain for V1 scope. Patient can view provider/clinic reviews, submit reviews, and request takedown, but cannot directly delete submitted reviews. Admin can insert/edit/remove reviews, configure review settings/export reports, and approve/reject takedown requests.

---

## Key Entities

- Review: `overall_rating`, `facility_rating`, `staff_rating`, `results_rating`, `value_rating`, `feedback_text`, status (Published / Removed; admin-internal Flagged state), timestamps (`created_at`, `last_edited_at`, `edit_count`), links (patient, procedure, provider, `treatment_id`), context (`clinic_name`, `treatment_name`), source type (patient-submitted / admin-seeded "Verified Off-platform"), flagged status, `source_metadata` (for admin-seeded reviews: `source_platform` enum, `source_url`, `evidence_file_ids[]`, `capture_date`, `permission_record` {file_id or text reference, admin_attestation_bool, attested_by, attested_at}, `reviewer_display_name`).
- ReviewPhoto: file references, thumbnails, alt text; associated review ID.
- TakedownRequest: review ID, requester (patient), reason (required), status (Pending / Approved / Rejected), decision note, decision actor (admin), created/decided timestamps.
- AdminAction: action type (insert/edit/remove/takedown_approve/takedown_reject), reason, admin identity, timestamp, changes made; associated review ID and/or takedown request ID.
- ProviderResponse: text, author (provider), timestamp; associated review ID.
- ReviewSettings: category labels, photo guidelines, removal reasons, display policy, flagging thresholds, takedown SLA settings, updated by/timestamp. Review invite/reminder cadence is owned by FR-030 and linked from Screen 10.

---

## Appendix: Change Log

| Date       | Version | Changes                                        | Author |
| --- | --- | --- | --- |
| 2025-11-11 | 1.0     | Initial PRD creation                           | AI     |
| 2025-11-11 | 1.1     | Filled scope, workflows, rules, and criteria   | AI     |
| 2026-03-03 | 1.2     | **Removed pre-publication moderation gate** — reviews now publish immediately upon patient submission (per client transcription: no moderation gate was requested). Admin retains post-publication edit/remove capability for policy violations. Key changes: (1) Main Flow updated — review published immediately, no "Pending Moderation" status; (2) A1/A2 workflows replaced — from approve/reject to post-publication remove/edit; (3) Screen 2 renamed from "Moderation Queue" to "Review Management"; (4) Patient can edit published review at any time; (5) Status values simplified to Published / Removed by Admin; (6) ModerationDecision entity replaced with AdminAction entity; (7) Admin-seeded reviews moved from Backlog to main admin scope per client transcription (AdminPlatform-Part1, lines 91–100); (8) All metrics, requirements, and business rules updated to reflect no-moderation model. | Product alignment (2026-03-03) |
| 2026-05-14 | 1.3     | Aligned Screen Specifications to the current patient review form data structure: added read-only clinic/treatment context fields, canonicalized rating field names (`overall/facility/staff/results/value`), added explicit patient payload contract, and synchronized Provider/Admin screens + requirements to consume the same canonical schema across tenants. | Product alignment (2026-05-14) |
| 2026-05-14 | 1.4     | Scope uplift per transcription and current UI flow: (1) Admin insert/edit reviews moved to in-phase scope; (2) patient direct delete removed and replaced with takedown-request workflow + admin approve/reject decisioning; (3) main flow prerequisite clarified as completed treatment case; (4) screen model expanded to 8 screens (Patient list/detail+takedown, Provider list/filter/detail, Admin list/detail+takedown queue); (5) workflows, user stories, requirements, entities, and metrics aligned to multi-case/provider-admin operations. | Product alignment (2026-05-14) |
| 2026-05-14 | 1.5     | Takedown flow UI alignment pass using current visual flow + P05.3 design-complement references: added patient review detail provider-response section, pre-filled edit behavior, bottom-sheet takedown submission with optional message and mandatory 7-year retention notice, list sort/empty-state details, and corresponding requirement/entity refinements. | Product alignment (2026-05-14) |
| 2026-05-14 | 1.6     | Patient "My Reviews" list visual alignment pass: updated Screen 2 to match card UI (title, header sort icon, rating+time row, treatment line, excerpt with "See more", provider avatar/name row, and status badges), then synchronized related status vocabulary in patient detail and review entity definitions. | Product alignment (2026-05-14) |
| 2026-05-14 | 1.7     | Provider review operations refinement: added patient filter to provider review list filters and introduced detailed inline Provider Response Composer interaction model within Review Detail, including validation, cancel/submit behavior, and post-publish immutability rules. | Product alignment (2026-05-14) |
| 2026-05-14 | 1.8     | Screen specification cleanup and coverage pass: replaced non-incremental screen labeling with strict Screen 1-10 numbering, added patient-facing Provider Profile Reviews Section as an embedded part of the provider profile/quote-review flow, merged provider response composer into Provider Review Detail, added Admin Review Settings & Export screen, expanded display/settings/export requirements, and synchronized user stories/entities/metrics. | Product alignment (2026-05-14) |
| 2026-05-14 | 1.9     | Verification follow-up: aligned system PRD source-of-truth to immediate review publication with post-publication admin flagging/removal, and expanded FR-013 module/dependency traceability for PR-06, S-03, S-05, FR-020, FR-022, FR-030, and FR-032. | Product alignment (2026-05-14) |
| 2026-05-14 | 1.10    | Backend-aligned review status vocabulary: removed `Submitted` as a review status, kept patient-facing review status to `Published` / `Removed`, documented `Flagged` as admin-internal, and separated takedown request states (`Pending` / `Approved` / `Rejected`) from review visibility status. | Product alignment (2026-05-14) |
| 2026-05-14 | 1.11    | Verification fixes: (1) B2 trigger narrowed to system-automated detection only — user-initiated flagging moved to future enhancement; (2) Screen 1 feedback field validation note expanded to document 100-char minimum rationale; (3) A4 step 3 updated to include provider rating metrics recalculation on approved takedown; (4) SC-005 reclassified as a Business KPI tracked via FR-014, not a system-enforced success criterion. | Verification alignment (2026-05-14) |
| 2026-05-14 | 1.12    | Verification fixes (round 2): (1) FR-013 ↔ FR-030 boundary — Screen 10 invitation cadence and reminder settings rewritten as read-only link-outs to FR-030, which now owns review-invite cadence/timing; REQ-013-022 updated accordingly; (2) Screen 6 — provider may submit one replacement response after admin removal (prior response retained in audit trail); (3) requirements summary — REQ-013-021 renumbered to REQ-013-009 so Core Requirements run sequentially, with subsequent IDs shifted by one; (4) Screen 10 photo guidelines validation note clarified — "versioned" replaced with "audit-logged via AdminAction" (no formal version model); (5) Screen 3 takedown message — when provided, enforced minimum length of 10 chars to prevent trivial submissions while keeping field optional. | Verification alignment (2026-05-14) |
| 2026-05-14 | 1.13    | Verification fixes (round 3): (1) **Issue #1 — audit retention** — Data & Privacy Rules now state review-content retention is 7y while `AdminAction`/audit-log retention is 10y per Constitution §VI; Screen 3 takedown notice text updated to surface both retention windows. (2) **Issue #2 — admin-seeded provenance schema** — Screen 8 source verification replaced with structured `source_metadata` form (source_platform enum, source_url, evidence_file[], capture_date, permission_record + admin attestation, reviewer_display_name); Key Entities Review extended with `source_metadata` payload. (3) **Issue #3 — 3-month review gate** — confirmed as a product-owner additional requirement (no client-transcription evidence required); recorded here as the authoritative source. The "≥ 3 months post-procedure" eligibility threshold remains canonical and continues to live under "Fixed in Codebase". (4) **Issue #4 — per-treatment aggregation** — added **REQ-013-018a** committing to a per-treatment aggregated sub-scores endpoint (`{treatment_id → {avg_overall, avg_facility, avg_staff, avg_results, avg_value, review_count, distribution}}`) as FR-014's data contract, with cache invalidation on publish/edit/remove/takedown. (5) **Issue #5 — patient-edit safeguards** — Main Flow Step 4 now requires re-running B2 automated flagging on edit, setting `last_edited_at` / `edit_count`, notifying provider on edit, and showing an "Edited {relative_time}" marker on all public surfaces. (6) **Issue #6 — reviewer alias algorithm** — Data & Privacy Rules now define the canonical alias (`{first_name} {last_initial}.` with `Sarah M. 2/3/…` dedup), admin-seeded `reviewer_display_name` rule, and reaffirm alias-only default in V1. (7) **Issue #7 — FR-022 master reference sync** — FR-022 prd.md updated: FR-013/Screen 7 filter row refreshed to current backend-aligned status vocabulary (Published/Removed; admin-internal Flagged) plus Patient/Treatment Case/Source Type/Response Status filters and search; added FR-013/Screen 5 row for provider review list with the patient filter added in FR-013 v1.7. (8) **Issue #8 — provider response immutability wording** — Screen 6 business rule re-worded to "immutable while published; one replacement allowed only after admin removal", clarifying the previously misleading "immutable once posted" phrasing. | Verification alignment (2026-05-14) |
| 2026-05-14 | 1.14    | Verification fixes (round 5): selected Issue #2 Option 2 — takedown requests now require a patient reason (10–1000 chars) instead of an optional message, with workflow, Screen 3, REQ-013-020, and TakedownRequest entity aligned. Cleaned remaining Screen 10 wording so review invite/reminder cadence stays owned by FR-030 link-outs, while FR-013 owns review labels/display policy/export settings. | Verification alignment (2026-05-14) |
| 2026-05-14 | 1.15    | Status closeout: marked PRD as `✅ Verified & Approved` and updated Appendix Approvals to the PRD template format with verified approval status for Product Owner, Technical Lead, and Stakeholder rows. | Verification closeout (2026-05-14) |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | TBD | 2026-05-14 | ✅ Verified & Approved |
| Technical Lead | TBD | 2026-05-14 | ✅ Verified & Approved |
| Stakeholder | TBD | 2026-05-14 | ✅ Verified & Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-05-14
