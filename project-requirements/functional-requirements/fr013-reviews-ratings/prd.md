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

- Patient Platform (P-02): Submit a review for a treatment case marked Completed in FR-010 (time-gated: 3 months from the day it was marked Completed), provide overall and category ratings, feedback, and optional photos; review is published immediately. Patient can browse provider/clinic reviews during provider review/offer evaluation, browse all submitted reviews, view review detail, and submit takedown requests.
- Provider Platform (PR-06 display context): View all published reviews across treatment cases, search by reviewer alias, filter by treatment, rating, date, response status and source type, sort, open review detail, and post public responses.
- Admin Platform (A-01): Monitor all reviews with patient/provider/case filters, view and edit review details, remove reviews for policy/compliance reasons, insert authenticated reviews for provider profiles, and process takedown requests (approve/reject) with audit trail.
- Shared Services (S-05, S-03): Media Storage for review photos; Notification Service for invite reminders, provider reply alerts, admin review removal notices (sent to the reviewing patient only), provider response removal notices (sent to the provider), and takedown request status updates.

### Multi-Tenant Breakdown

Patient Platform (P-02):

- Receive invitation to review once the eligibility date is reached (3 months after the case was marked Completed).
- Submit ratings (overall 1–5 stars; category ratings) and feedback; optionally attach photos; review published immediately.
- View all submitted reviews across treatment cases and open review detail.
- Cannot directly delete submitted reviews; can submit takedown request to admin for decision.

Provider Platform (display + response):

- View published reviews on their profile across all treatment cases, with list filters and sorting.
- Open review detail to inspect ratings, feedback, photos, and treatment context.
- Post a public response to individual reviews; receive notification on new published reviews.

Admin Platform (A-01):

- Review management dashboard with filters (provider, patient, case, treatment, date, rating, status).
- View full review detail; edit or remove published reviews for policy/compliance violations (with reason).
- Insert authenticated reviews for provider profiles (flagged as "Verified Off-platform").
- Takedown request queue to review and approve/reject patient takedown requests.
- Manage review categories, moderation settings, and export reports; link out to FR-030 for reminder cadence.

Shared Services (S-05, S-03):

- S-05 handles secure photo storage and retrieval.
- S-03 delivers invite/reminder emails/push and status notifications.

### Entry Points

- The review invitation fires on the eligibility date (3 months after the treatment case was marked Completed in FR-010) and triggers the review flow; reminders count from that date. (REQ-013-024; REQ-013-017)
- Patient navigates to “Write a Review” from provider history. (REQ-013-024)
- Patient views published reviews from provider profile/offer evaluation surfaces. (REQ-013-024)
- Patient navigates to “Submitted Reviews” to view review history and request takedown from detail page. (REQ-013-024)
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

- Patient has a treatment case linked to the provider that FR-010 has marked Completed (Closed Early and Cancelled cases cannot be reviewed).
- Review submission is within allowed review window (≥ 3 months from the day the case was marked Completed).

Steps:

1. Patient completes overall and category ratings, enters feedback, and optionally attaches photos.
2. System validates inputs (rating ranges, feedback length, file type/size) and verifies eligibility.
3. System publishes (or republishes, on edit) the review immediately and recalculates provider rating metrics (average, count, distribution) with associated cache invalidation. Recalculation applies whether the action is an initial submission or an edit to an already-published review, and, under the same rule, to every other change of a review's visibility or rating (REQ-013-031): admin add, admin edit of a rating, admin removal, unpublish from flag resolution, and approved takedown. Published and Flagged reviews count in the aggregates, so setting or clearing a flag needs no recalculation. Admin-seeded reviews count in the average and distribution and are labelled Verified Off-platform.
4. On edit (republish), system also: (a) re-runs B2 automated flagging (keyword/duplicate/rate-limit checks) against the new payload, including a comparison with the last admin redaction so an edit cannot restore redacted content, (b) sets `last_edited_at` and increments `edit_count`, (c) writes a full audit record (before/after values, actor=patient), and (d) notifies the provider, for information only, that a review they may have responded to was edited; the provider has no action on the notice because responses are immutable (REQ-013-055).
5. Patient sees confirmation; review is live on provider profile and appears in Patient “Submitted Reviews” list. If the submission or edit matches a flagging rule, the review is also queued as B2. Edited reviews (patient or admin edit) surface an "Edited {relative_time}" marker on all public surfaces (Patient list, Patient detail, Provider list/detail, Provider Profile Reviews Section) so readers can distinguish current content from the original publish. An admin edit sets the marker but does not change the edit count, which counts patient edits.

### A1: Admin Inserts Authenticated Review

- Trigger: Admin receives authenticated external review evidence for provider profile seeding.
- Steps:
  1. Admin enters review payload (provider, treatment, ratings, feedback, review date, source evidence) and the required reason.
  2. System validates fields and stores source provenance.
  3. System publishes review flagged as "Verified Off-platform".
  4. System recalculates provider rating metrics and invalidates the cache (REQ-013-031); the seeded review counts in the average and distribution.
- Outcome: Provider profile receives seeded review with explicit provenance marker and full audit record. Notices that would go to the placeholder patient (REQ-013-077) are not sent.

### A2: Admin Edits Existing Review

- Trigger: Admin identifies correction or compliance need on an existing review.
- Steps:
  1. Admin opens review detail and applies edits/redactions.
  2. System records before/after values, reason, and admin identity, sets the Edited marker, and notifies the reviewing patient.
  3. If a rating changed, System recalculates provider rating metrics and invalidates the cache (REQ-013-031).
- Outcome: Review is updated per admin action; audit trail preserved.

### A3: Patient Submits Takedown Request

- Trigger: Patient opens submitted review detail and chooses "Request Takedown".
- Steps:
  1. Patient taps "Request Takedown"; system opens confirmation bottom sheet/modal over review detail.
  2. Patient enters a required takedown reason and confirms takedown request.
  3. System records patient reason, creates takedown request with `Pending` status, and links it to review/case.
  4. System notifies admin takedown queue.
  5. If no decision is made when the takedown decision deadline passes (REQ-013-078), System shows the request as Overdue on Screen 9 and notifies admins; no request is approved or rejected automatically.
- Limits (REQ-013-043): a review has at most one Pending request; after a rejection the patient may file one further request with a new reason; the review cannot be edited while a request is Pending; an admin removal of the review while a request is Pending closes the request as Approved.
- Outcome: Takedown request enters admin processing queue; review remains visible until decision.

### A4: Admin Processes Takedown Request

- Trigger: Admin opens pending takedown request from queue.
- Steps:
  1. Admin reviews request reason, review content, and compliance context.
  2. Admin approves or rejects request with decision note.
  3. System applies decision: approved -> review unpublished/archived (any flag on it is cleared) and provider rating metrics recalculated; rejected -> review remains published.
  4. System notifies patient of decision and reason; the decision note is also shown on Review Detail (Screen 3).
- Outcome: Takedown request resolved with audit log, provider metrics updated, and patient notification.

### A5: Admin Removes a Review

- Trigger: Admin finds a policy or compliance violation on a review (also reached from B2 when the admin unpublishes a flagged review).
- Steps:
  1. Admin opens the review on Screen 8, selects "Remove review", and enters the removal reason (at least 10 characters).
  2. System sets the status to Removed (clearing any flag reason), stores the reason as the admin removal reason, writes the audit record as a `remove` action carrying the takedown request id when one is closed, closes any Pending takedown request on the review as Approved (decided by the removing admin, at the removal time, with the removal reason as its decision note), and notifies the reviewing patient with the single removal notice (no second takedown notice).
  3. System recalculates provider rating metrics and invalidates the cache (REQ-013-031).
- Outcome: Review is unpublished and archived, never restored (REQ-013-016). Under REQ-013-002 the patient may submit one further review for the case, up to two reviews in total.

### B1: Provider Response

- Trigger: Provider posts a response to a published review.
- Steps:
  1. Provider opens Review Detail (Screen 6) and taps "Respond as Provider" (shown only while the provider account is active, the review has no active response and no replacement response was ever published).
  2. System opens inline response composer/modal state within Screen 6.
  3. Provider writes response; system validates length and policy.
  4. Provider confirms submission; system publishes response under provider identity.
- Outcome: Response visible with the review; patient notified.

### B2: Flagging/Inappropriate Content

- Trigger: Content flagged by system-automated detection (keyword matching, duplicate submission patterns, rate-limit triggers) after a submission or an edit. User-initiated flagging is a future enhancement.
- Steps:
  1. System sets the review status to Flagged and queues the content for admin review.
  2. Admin resolves the flag on Screen 8 with a reason: uphold (the review returns to Published and the flag reason is cleared), redact (an admin edit, A2; the review returns to Published and the flag reason is cleared), or unpublish (an admin removal, A5).
- Outcome: Policy-compliant content remains; violations are removed with audit record. A flagged review stays publicly visible (shown as Published) until an admin removes it.

### B3: Admin Removes a Provider Response

- Trigger: Admin finds a policy violation in a provider response.
- Steps:
  1. Admin opens the review on Screen 8, selects "Remove provider response", and enters the reason.
  2. System sets the response status to removed, writes the audit record, and the review shows "No response" again.
  3. System notifies the provider that the response was removed, with the removal reason.
- Outcome: After the first removal the provider may submit the one replacement response (REQ-013-055, REQ-013-056); if the replacement is removed too, Respond stays hidden.

---

## Screen Specifications

### Patient Platform

#### Screen 1: Patient – Submit Review

Purpose: Allow eligible patients to submit a structured review post-procedure.

Data Fields:

| Field Name         | Type        | Required | Description                                  | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Clinic Name        | text        | Yes      | Read-only clinic/provider label at top of form | Read-only; derived from booked provider | ENT-review.clinic_name |
| Treatment Name     | text        | Yes      | Read-only treatment label at top of form       | Read-only; derived from completed procedure | ENT-review.treatment_name |
| Overall Rating     | 1-5 stars   | Yes      | Overall experience                              | Integer 1-5 | ENT-review.overall_rating |
| Facility Rating    | 1-5 stars   | Yes      | Facility cleanliness                            | Integer 1-5 | ENT-review.facility_rating |
| Staff Rating       | 1-5 stars   | Yes      | Staff professionalism                           | Integer 1-5 | ENT-review.staff_rating |
| Results Rating     | 1-5 stars   | Yes      | Results satisfaction                            | Integer 1-5 | ENT-review.results_rating |
| Value Rating       | 1-5 stars   | Yes      | Value for money                                 | Integer 1-5 | ENT-review.value_rating |
| Feedback           | textarea    | Yes      | Narrative experience                            | 100-2000 chars; 100-char minimum ensures reviews contain enough substance to be useful to other patients | ENT-review.feedback_text |
| Photos             | image list  | No       | Optional before/after images                    | Up to 5 files; jpg/png; max 10MB each | ENT-review.photos |

Business Rules:

- Eligibility: see General Module Rules (REQ-013-001) and REQ-013-002.
- One published review per treatment case; after a removal (approved takedown or admin policy removal) the patient may submit one further review for the case, so a case has at most two reviews in total and the submission screen then says no more reviews can be submitted for it (removed reviews are kept in the archive and are never restored); patient can edit their published review at any time except while a takedown request on it is Pending. (REQ-013-002; REQ-013-030)
- See REQ-013-003.
- Clear photo guidelines; sensitive/identifying content discouraged. (REQ-013-029)
- The save action persists the current review payload and immediately publishes valid patient submissions.

Data Contract (Patient Form Payload):

See REQ-013-013 for the payload fields; `clinic_name` and `treatment_name` are display only, read-only context.

Notes:

- Rating rows use a row-select interaction pattern (tap row to set/update score); selected values display in `X/5 star` format. (REQ-013-026)
- Disclose display policies and admin's right to remove for violations. (REQ-013-029)
- Feedback length bounds (100–2000 chars): 100-char minimum ensures substantive content for other patients; 2000-char ceiling deters off-topic walls of text and reduces spam/abuse surface area without truncating genuine narrative experience. (REQ-013-026)

---

#### Screen 2: Patient – Submitted Reviews List (My Reviews)

Purpose: Allow patient to view all submitted reviews across treatment cases.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Screen title | text | Yes | "My Reviews" | Display only | no graph field (control) |
| Header sort icon | action icon | No | Sort/reorder action in top-right header | Opens sort options | no graph field (control) |
| Review list | list | Yes | All patient-submitted reviews grouped by treatment case/provider | Sorted by newest first; paginated | ENT-review.created_at, ENT-review.last_edited_at, ENT-review |
| Rating + time row | group | Yes | Star rating with relative time (e.g., "5 days ago") | Read-only | ENT-review.overall_rating, ENT-review.created_at |
| Status | badge | Yes | Published / Removed | Patient-facing review visibility status; color-coded | ENT-review.status |
| Takedown request status | badge | Conditional | Pending / Approved / Rejected | Shown only when a takedown request exists; shows the latest request (earlier requests stay in the admin history); sourced from takedown request workflow, not review status | ENT-takedown-request.status |
| Treatment line | text | Yes | "Treatment: {treatment_name}" | Read-only | ENT-review.treatment_name |
| Review excerpt | text | Yes | Truncated narrative preview | Max 2 lines + "See more" affordance | ENT-review.feedback_text |
| Provider row | group | Yes | Provider avatar + provider name | Read-only | ENT-provider.avatar, ENT-provider.name |
| Sort option | select | No | Reorder list by selected criterion | Default: Most recent first | no graph field (control) |
| Open detail | action | Yes | Opens selected review detail | Navigates to Screen 3 | no graph field (control) |
| Empty state | text | No | "No reviews yet - complete a treatment to leave a review" | Shown when patient has no submitted reviews | no graph field (control) |

Business Rules:

- Includes all submitted reviews for the logged-in patient across all completed treatment cases.
- Review status badge uses app-facing labels: `Published`, `Removed`. A review with status `Flagged` shows as `Published` to the patient: see REQ-013-079. (REQ-013-040)
- `Submitted` is not a review status in V1; successful review submission immediately creates a `Published` review.
- Takedown request state is displayed separately from review status when applicable (`Pending`, `Approved`, `Rejected`), for the latest request only; earlier requests stay in the admin history.
- `Removed` means no longer publicly visible due to admin action or approved takedown.
- Default list sort is latest submission date descending. (REQ-013-041)

---

#### Screen 3: Patient – Review Detail & Takedown Request

Purpose: Show full submitted review content (including provider response when available), allow edit for published reviews, and allow takedown request via confirmation modal.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Review detail payload | card | Yes | Full ratings, feedback, photos, provider, treatment context | Read-only in detail mode | ENT-review.overall_rating, ENT-review.facility_rating, ENT-review.staff_rating, ENT-review.results_rating, ENT-review.value_rating, ENT-review.feedback_text, ENT-review.photos, ENT-review.treatment_name, ENT-review.last_edited_at, ENT-provider.name |
| Review submission date | datetime | Yes | Date/time the review was submitted | Read-only | ENT-review.created_at |
| Current status | badge | Yes | Published / Removed | Read-only review visibility status | ENT-review.status |
| Takedown request status | badge | Conditional | Pending / Approved / Rejected | Shown when the review has an associated takedown request; shows the latest request (earlier requests stay in the admin history) | ENT-takedown-request.status |
| Provider response block | card | No | Provider response content, timestamp, and role badge | Shown only when provider response exists | ENT-provider-response.response_text, ENT-provider-response.created_at, ENT-provider-response.author_role |
| Admin removal reason | text | No | Reason supplied by admin when review is removed | Shown only when status = Removed | ENT-review.admin_removal_reason |
| Takedown decision note | text | Conditional | Admin's note explaining the takedown decision | Shown only after the latest takedown request has been decided (Approved or Rejected) | ENT-takedown-request.decision_note |
| Edit review | button | Conditional | Opens pre-filled edit form | Visible only when status = Published (a Flagged review shows as Published) and no takedown request is Pending | no graph field (control) |
| Request takedown | button | Conditional | Opens takedown confirmation bottom sheet/modal | Visible only when status = Published (a Flagged review shows as Published) and no request is Pending; after a rejection one further request is allowed, with a new reason | no graph field (control) |
| Takedown reason | textarea | Yes (when requesting) | Required patient reason for admin context | 10–1000 chars (REQ-013-045) | ENT-takedown-request.reason |
| Retention notice | info text | Yes (when requesting) | "Review content will be removed from public view but archived for 10 years. Audit records of this takedown are kept for the same 10 years." | Display-only policy text; reflects the one 10-year retention period (see Data & Privacy Rules) (REQ-013-075) | no graph field (control) |
| Submit takedown request | action | Yes (when requesting) | Sends request to admin queue | Confirmation required | no graph field (control) |

Business Rules:

- See REQ-013-005.
- For `Published` status (a `Flagged` review counts as `Published`, REQ-013-079), `Edit Review` is available unless a takedown request is `Pending`, and `Request Takedown` is available unless a request is `Pending` or the one further request after a rejection has been used. (REQ-013-042)
- For `Removed` status, detail is read-only and shows admin removal reason; edit/takedown actions are hidden. (REQ-013-042)
- Patient can edit their published review at any time except while a takedown request on it is `Pending`. `Edit Review` opens pre-filled form fields; saved edits are published immediately (no moderation gate). (REQ-013-030; on edit see also Main Flow steps 4 and 5: REQ-013-032, REQ-013-033)
- See REQ-013-020.
- See REQ-013-044.
- A review has at most one `Pending` takedown request. While a request is `Pending`, review remains `Published` unless manually removed by admin (which closes the request as `Approved`), and the patient cannot edit it. After a rejection the patient may file one further request with a new reason. (REQ-013-043)

#### Screen 4: Patient – Provider Profile Reviews Section

Purpose: Define the reviews section embedded inside the patient-facing provider profile shown during quote/provider evaluation.

Context Note:

- This is not a standalone full provider profile screen. It specifies only the FR-013 review-related section and interactions inside the existing provider profile screen used in the quoting process.
- Non-review provider profile content (about text, languages, staff, certifications, awards, location, and provider messaging entry points) belongs to the provider profile / quote-review screen specifications and is not duplicated here.
- The embedded review section must connect to the same review data model used by patient-submitted reviews, provider response surfaces, and admin review management.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Host provider context | reference | Yes | Current provider/clinic profile being reviewed in the quote flow | Read-only; supplied by host provider profile screen | ENT-provider.name |
| Rating summary teaser | stats row | Yes | Average rating, star display, total review count, and `View all` entry point near provider heading | Read-only; cached summary allowed | ENT-provider-review-summary.average_rating, ENT-provider-review-summary.review_count |
| Reviews section heading | text/action row | Yes | Reviews heading with optional `View all` action | Display only; action opens full review list state | no graph field (control) |
| Review preview list | list | Yes | Preview reviews shown within provider profile screen | Published reviews only; limited count before `View all` (REQ-013-062) | ENT-review, ENT-review.last_edited_at |
| Full reviews list state | list/overlay/subview | Conditional | Expanded review list opened from `View all` | Paginated; newest first by default (REQ-013-062) | ENT-review |
| Reviewer alias | text | Yes | Public reviewer display name | Always the alias; no PII exposure | ENT-review.reviewer_name |
| Rating + date row | group | Yes | Overall rating and submitted date/relative time | Read-only | ENT-review.overall_rating, ENT-review.created_at |
| Treatment context | text | No | Treatment/procedure context when display-safe | Read-only; no sensitive details | ENT-review.treatment_name |
| Review excerpt/body | text | Yes | Review feedback preview or full content | Preview truncates with "See more" affordance | ENT-review.feedback_text |
| Photos | image list | No | Public review photos/thumbnails | Display only photos attached to a published review | ENT-review.photos |
| Provider response block | card | No | Provider response content and timestamp | Shown only when response exists | ENT-provider-response.response_text, ENT-provider-response.created_at |
| Verified off-platform badge | badge | Conditional | Provenance marker for admin-seeded authenticated reviews | Required for admin-seeded reviews | ENT-review.source_type |
| Sort/filter controls | controls | No | Sort by recency/rating and filter by rating | Full reviews list state only (REQ-013-062) | no graph field (control) |
| Open review detail | action | No | Opens expanded review content | May use in-screen expansion, modal, or host-defined subview | no graph field (control) |

Business Rules:

- Only `Published` reviews (a `Flagged` review counts as `Published`, REQ-013-079) are visible on patient-facing provider/clinic profile surfaces. (REQ-013-059)
- The embedded preview must not redefine or duplicate the full provider profile layout; it inherits provider identity and navigation from the host provider profile screen. (REQ-013-060)
- `View all` opens the complete review list for the same provider without changing review ownership or source rules. (REQ-013-061)
- See REQ-013-014.
- See REQ-013-006 for the `Verified Off-platform` marker and the provider response display on these surfaces.
- Review photos shown publicly must follow the same media privacy and removal rules as submitted review photos. (REQ-013-064)

---

### Provider Platform

#### Screen 5: Provider – Reviews List & Filters

Purpose: Show all provider reviews across treatment cases with filtering.

Context Note:

- This review list can appear as a dedicated Provider Dashboard reviews list and may also be embedded or linked from the provider's own profile detail section.
- Final placement is a UX/UI design decision; the designer may place this list wherever it best fits the provider dashboard/profile experience.
- When embedded in provider profile detail, this screen specifies only the review list/filter behavior; non-review provider profile fields remain owned by the provider profile detail specification.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Ratings summary | stats | Yes | Average rating, count, distribution | Read-only | ENT-provider-review-summary.average_rating, ENT-provider-review-summary.review_count, ENT-provider-review-summary.rating_distribution |
| Review list | list | Yes | All published reviews tied to provider | Paginated; newest first by default (REQ-013-063) | ENT-review, ENT-review.created_at, ENT-review.overall_rating, ENT-review.last_edited_at |
| Review source type | badge | Yes | Patient-submitted / Verified Off-platform | Read-only | ENT-review.source_type |
| Reviewer alias | text | Yes | Patient alias or off-platform reviewer label | Read-only; no PII exposure | ENT-review.reviewer_name |
| Treatment context | text | Yes | Treatment name only (no case identifier, so the alias is not tied to a case record) | Read-only | ENT-review.treatment_name |
| Response status | badge | Yes | No response / Responded | Read-only; shows No response when the only response was removed by an admin | ENT-review.response_status |
| Filters | controls | No | Search by reviewer alias; filter by treatment, rating range, date range, response status, source type (no patient or case filter, so the alias is not tied to an identity) | Multi-filter | no graph field (control) |
| Sort | select | No | Sort reviews by recency or rating | Default: recency (REQ-013-063) | no graph field (control) |
| Open detail | action | Yes | Opens selected review detail | Navigates to Screen 6 | no graph field (control) |

Business Rules:

- Multi-case histories are told apart by treatment name and date; the list has no patient or case filter. (REQ-013-058)
- Only published reviews (including a `Flagged` review) appear in provider list surfaces. (REQ-013-059)

---

#### Screen 6: Provider – Review Detail & Response

Purpose: Let provider inspect review details and post public response.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Review detail payload | card | Yes | Canonical review payload (ratings, feedback, photos, treatment name) | Read-only | ENT-review.overall_rating, ENT-review.facility_rating, ENT-review.staff_rating, ENT-review.results_rating, ENT-review.value_rating, ENT-review.feedback_text, ENT-review.photos, ENT-review.treatment_name, ENT-review.last_edited_at |
| Review source type | badge | Yes | Patient-submitted / Verified Off-platform | Read-only | ENT-review.source_type |
| Reviewer alias | text | Yes | Public reviewer label | Read-only; no PII exposure | ENT-review.reviewer_name |
| Photos | image list | No | Review photos and thumbnails | Read-only | ENT-review.photos |
| Provider response card | display block | No | Persisted provider response content, author, role, timestamp | Shown when response exists | ENT-provider-response.response_text, ENT-provider-response.author_id, ENT-provider-response.author_role, ENT-provider-response.created_at |
| Respond as Provider | button | Conditional | Opens response composer | Visible only when the review is published (a Flagged review counts as published), the provider account is active, and the review has no active response and no replacement response was ever published (a removed original response does not count; once a replacement is published, Respond stays hidden even if the replacement is later removed) | no graph field (control) |
| Response composer | inline panel/modal | Conditional | Non-navigating response input surface within this screen | Opens from `Respond as Provider` | no graph field (control) |
| Response text | textarea | Yes (when composing) | Provider's public response body | 50-1000 chars | ENT-provider-response.response_text |
| Character counter | indicator | Yes (when composing) | Remaining character count | Live update; blocks submit outside limits | no graph field (control) |
| Cancel response | button | Yes (when composing) | Close composer without publishing | Confirmation prompt if unsaved content exists | no graph field (control) |
| Submit response | action | Yes (when composing) | Publish provider response | Enabled only when validation passes | no graph field (control) |

Business Rules:

- Provider responses are public and immutable while published; admins may remove a response for policy violation. After an admin removal, the provider may submit exactly one replacement response (see one-active-response rule below) — outside of that single replacement, posted responses cannot be edited or re-posted by the provider. (REQ-013-055)
- Detail and list show the treatment name and date, so multi-case histories are told apart by treatment and date, not by case identifier. (REQ-013-058)
- Provider may have at most one active public response per review in V1. If admin removes a prior response for policy violation, provider may submit one replacement response; both the removed and replacement responses are retained in the audit trail (`AdminAction` for the removal, `ProviderResponse` history for the lifecycle). If the replacement is removed too, the provider may not respond again: a review has at most one original and one replacement response. (REQ-013-056)
- See REQ-013-021.
- Submission records provider identity and timestamp and triggers patient notification (not sent when the review is an admin-seeded review linked to a placeholder patient, REQ-013-077). A suspended provider sees the review view-only, with no Respond control. (REQ-013-057)
- When the reviewing patient edits a review, the provider receives an informational notice only; there is no control on this screen to edit or re-open a response. (REQ-013-032; REQ-013-055)

Notes:

- Encourage professional tone; display response timestamp and provider role.
- Response length bounds (50–1000 chars): 50-char minimum prevents single-word or non-substantive replies that erode trust; 1000-char ceiling keeps public responses scannable on review surfaces and discourages defensive long-form rebuttals. (REQ-013-054)

---

### Admin Platform

#### Screen 7: Admin – Reviews Management List

Purpose: Monitor all reviews in the system with operational filters.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Reviews list | list | Yes | Global list of all reviews | Paginated; system-wide | ENT-review, ENT-review.created_at, ENT-review.overall_rating, ENT-review.status |
| Source type | badge/filter | No | Patient-submitted / Verified Off-platform | Read-only badge; filterable | ENT-review.source_type |
| Flagged status | badge/filter | No | Flagged / Not flagged | Read-only badge; filterable | ENT-review.status |
| Response status | badge/filter | No | No response / Responded | Read-only badge; filterable | ENT-review.response_status |
| Filters | controls | No | Provider, patient, treatment case, treatment, status, date, rating, source type, response status, flagged status | Multi-filter | no graph field (control) |
| Search | text | No | Search by patient/provider/case identifiers | Min 2 chars | no graph field (control) |
| Open detail | action | Yes | Open selected review detail/edit view | Navigates to Screen 8 | no graph field (control) |
| Open takedown queue | action | Yes | Navigate to takedown requests | Navigates to Screen 9 | no graph field (control) |
| Open review settings | action | No | Navigate to review settings/export | Navigates to Screen 10 | no graph field (control) |

Business Rules:

- Admin list includes patient-submitted and admin-seeded reviews, in any status (Published, Flagged, Removed). (REQ-013-065)
- Review visibility/filter results must preserve complete audit traceability. (REQ-013-065)

---

#### Screen 8: Admin – Review Detail, Insert & Edit

Purpose: Let admin inspect review details, edit/remove reviews, and insert new authenticated reviews.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Review detail payload | card/form | Yes | Full review content and metadata | Canonical schema | ENT-review.overall_rating, ENT-review.facility_rating, ENT-review.staff_rating, ENT-review.results_rating, ENT-review.value_rating, ENT-review.feedback_text, ENT-review.photos, ENT-review.created_at |
| Source type | badge/select | Yes | Patient-submitted / Verified Off-platform | Read-only for existing patient reviews; required for admin add | ENT-review.source_type |
| Flagged status | badge | No | Automatic flag state and reason | Read-only; changes through Resolve flag, an admin removal or an approved takedown (an edit made outside Resolve flag leaves the flag open) | ENT-review.status, ENT-review.flag_reason |
| Resolve flag | action | Conditional | Visible only while status is Flagged: uphold (review returns to Published and the flag reason is cleared), redact (admin edit; the review returns to Published and the flag reason is cleared), or unpublish (admin removal) | Reason required; uphold and redact clear ENT-review.flag_reason | no graph field (control) |
| Remove provider response | action | Conditional | Visible only while the review has an active provider response | Reason required; sets the response status to removed, which re-enables Respond for the provider after the first removal only, because a review gets one replacement (REQ-013-055) | ENT-provider-response.status, ENT-provider-response.removed_at |
| Audit trail preview | timeline | Yes | Recent admin, patient and provider actions and state changes | Read-only; full audit retained; each entry shows actor type and actor | ENT-admin-action.action_type, ENT-admin-action.actor_type, ENT-admin-action.actor_id, ENT-admin-action.admin_id, ENT-admin-action.changes, ENT-admin-action.created_at, ENT-admin-action.reason |
| Edit fields | form controls | No | Redaction/correction fields for existing review | Visible only while the review is Published or Flagged; reason required for edit | ENT-review |
| Remove review | action | No | Unpublish + archive review; there is no Restore action | Visible only while the review is Published or Flagged; removal reason min 10 chars (REQ-013-039); closes any Pending takedown request as Approved | no graph field (control) |
| Add review | action | No | Create new authenticated provider review | Requires provenance inputs and a reason | no graph field (control) |
| Seeded review inputs | form group | Yes (for add) | Provider, treatment, overall and category ratings, review text and review date of the seeded review | Same rating and text rules as patient reviews (REQ-013-026); review date not in the future | ENT-review.provider_id, ENT-review.treatment_id, ENT-review.overall_rating, ENT-review.facility_rating, ENT-review.staff_rating, ENT-review.results_rating, ENT-review.value_rating, ENT-review.feedback_text, ENT-review.created_at |
| Source verification | form group | Yes (for add) | Structured `source_metadata` payload (see below) capturing provenance and consent for seeded review | All required sub-fields must be provided for admin-seeded items; persisted to `Review.source_metadata` (REQ-013-036) | ENT-review.source_metadata |
| → Source platform | select | Yes (for add) | Origin of the off-platform review (e.g., Google, Trustpilot, Doctolify, Provider Website, Email Testimonial, Other) | Enum; "Other" requires free-text platform name | ENT-review-source-metadata.source_platform, ENT-review-source-metadata.other_platform_name |
| → Source URL | url | Conditional (for add) | Public link to original review when available | Valid URL; required unless `source_platform = Email Testimonial` | ENT-review-source-metadata.source_url |
| → Evidence file(s) | file upload | Yes (for add) | Screenshot/PDF/email capture of the original review | 1–5 files; jpg/png/pdf; max 10MB each; stored via S-05 | ENT-review-source-metadata.evidence_file_ids |
| → Capture date | date | Yes (for add) | Date the evidence was captured/observed | ISO date; not in future | ENT-review-source-metadata.capture_date |
| → Permission record | file or text + checkbox | Yes (for add) | Patient/reviewer consent artifact (signed permission, email screenshot, or written consent reference) + admin attestation checkbox confirming consent was obtained | Either file upload OR text reference + mandatory admin attestation (REQ-013-037) | ENT-review-source-metadata.permission_record_file_id, ENT-review-source-metadata.permission_record_reference, ENT-review-source-metadata.admin_attestation_bool |
| → Reviewer display name | text | Yes (for add) | Admin-entered alias to show publicly (see reviewer alias rule under Data & Privacy Rules) | PII-safe; no full last name; no contact info (REQ-013-037) | ENT-review-source-metadata.reviewer_display_name |
| Patient/reviewer photo | image upload | No (for add) | Optional reviewer image for authenticated seeded reviews | Must follow media policy | ENT-review.reviewer_avatar_url |
| Removal/edit reason | select + textarea | Yes | Reason catalog plus optional details | Required for add, edit, remove, resolve flag and remove provider response | ENT-admin-action.reason, ENT-review.admin_removal_reason |

Business Rules:

- Every admin add/edit/remove action records admin identity, timestamp, reason, and before/after changes. Audit records of patient edits and provider responses use the same entity, with an actor type and actor id. (REQ-013-038)
- Admin-seeded reviews must be flagged as "Verified Off-platform" with verification provenance; they count in the average and distribution. Notices that would go to the placeholder patient are not sent. (REQ-013-035; REQ-013-077)
- Removed reviews are unpublished + archived (not hard deleted), are never restored, and are read-only for admins. (REQ-013-016)
- An admin edit sets the Edited marker and notifies the reviewing patient; the patient's next edit is compared with the last admin redaction. (REQ-013-032; REQ-013-033)

---

#### Screen 9: Admin – Takedown Requests Queue

Purpose: Review and decide patient takedown requests.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Request queue | list | Yes | Pending/resolved takedown requests | Filterable by status/date (REQ-013-076) | ENT-takedown-request.status, ENT-takedown-request.created_at |
| Request metadata | group | Yes | Request ID, created date, requester, provider, treatment case | Read-only | ENT-takedown-request.id, ENT-takedown-request.created_at, ENT-takedown-request.requester_id, ENT-review.provider_id, ENT-review.procedure_id |
| Linked review preview | card | Yes | Review summary linked to request | Read-only | ENT-review.feedback_text, ENT-review.overall_rating |
| Current review status | badge | Yes | Published / Flagged / Removed | Read-only | ENT-review.status |
| Overdue badge | badge | Conditional | Shown on a Pending request once the takedown decision deadline has passed (REQ-013-078) | Read-only; display only, no automatic decision | no graph field (control) |
| Request reason | text | Yes | Patient-submitted reason | Read-only | ENT-takedown-request.reason |
| Decision action | controls | Yes | Approve / Reject takedown | Decision note required | no graph field (control) |
| Decision note | textarea | Yes | Admin justification for decision | 10-1000 chars | ENT-takedown-request.decision_note |
| Admin removal reason | textarea | Conditional | Patient-facing reason shown on Screen 3 after approved takedown/removal | Required when approving takedown; persisted to removed review record | ENT-review.admin_removal_reason |
| Decision history | timeline | No | Prior decisions/updates on resolved requests | Read-only | ENT-admin-action.action_type |
| Decision timestamp | datetime | Conditional | When request was resolved | Read-only after decision | ENT-takedown-request.decided_at |

Notes:

- Approve and reject decisions, and notifying the patient of both outcomes: see REQ-013-046.
- A request still Pending when an admin removes the review directly closes as Approved. After a rejection the patient may file one further request with a new reason (REQ-013-043).
- Past the deadline the queue shows Overdue and admins are notified; nothing is approved or rejected automatically. (REQ-013-078)
- Approved takedown must persist `Admin removal reason` on the removed review so Patient Review Detail (Screen 3) can display the same reason consistently. (REQ-013-047)
- Admin tooling must read/write the same canonical review schema as patient/provider surfaces to prevent cross-tenant drift. (REQ-013-013)

---

#### Screen 10: Admin – Review Settings & Export

Purpose: Configure review moderation settings and operational exports, with link-outs to FR-030 for review reminder cadence.

Data Fields:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Review categories/labels | editable list | Yes | Category rating labels used by review forms and displays | Admin-editable labels; canonical keys remain fixed | ENT-review-settings.category_labels |
| Reminder settings link-out | navigation | No | Entry point to FR-030 Notification Rules & Configuration for reminder count/timing on review invitations; reminders count from the eligibility date, and the invitation itself fires on the eligibility date (3 months after the case was marked Completed) | Read-only here; configured in FR-030 | no graph field (control) |
| Photo guidelines text | rich text/textarea | Yes | Patient-facing photo upload guidance | Required; audit-logged (all edits captured via AdminAction with before/after values; no formal version model) (REQ-013-071) | ENT-review-settings.photo_guidelines |
| Removal reason catalog | editable list | Yes | Standard reasons for admin removals/redactions | At least one active reason (REQ-013-072) | ENT-review-settings.removal_reasons |
| Flagging thresholds | controls | No | Duplicate/spam/keyword flag settings | Restricted safe ranges only | ENT-review-settings.flagging_thresholds |
| Takedown SLA settings | controls | No | Queue priority/SLA target and takedown decision deadline | Deadline from 12 hours to 7 days, default 48 hours; a breach shows Overdue and notifies admins (REQ-013-078) | ENT-review-settings.takedown_sla |
| Export reviews report | action | No | Export reviews/audit/takedown reports | RBAC-restricted; audit logged | no graph field (control) |

Business Rules:

- Settings changes are admin-only and audit logged. (REQ-013-066)
- Settings must not weaken fixed eligibility, rating scale, text length, retention, or privacy rules. (REQ-013-067)
- Export actions must preserve RBAC, PII handling, and audit traceability. (REQ-013-068)

---

## Business Rules

### General Module Rules

- Eligibility check required: only patients whose treatment case is marked Completed in FR-010 may review; Closed Early and Cancelled cases cannot. (REQ-013-001)
- Time gating: review invitation and entry allowed ≥ 3 months after the case was marked Completed; the invitation fires on that eligibility date. (REQ-013-002; REQ-013-024)
- One published review per treatment case: after a removal (approved takedown or admin policy removal) the patient may submit one further review for the case, so at most two reviews per case in total; removed reviews are never restored. (REQ-013-002)
- Any change of a review's visibility or rating (insert, edit, removal, unpublish, approved takedown) recalculates the provider aggregates and invalidates the cache; admin-seeded reviews count. (REQ-013-031)
- The status `Flagged` counts as `Published` for every rule keyed on visibility, patient actions, Respond and the rating aggregates. (REQ-013-079)
- See REQ-013-002.
- See REQ-013-005.
- Ratings use 1–5 scale with half‑stars display allowed for averages. (REQ-013-053)
- Anti‑abuse: Duplicate detection, keyword flags, rate limits for submissions.

### Data & Privacy Rules

- Patient display name is always the alias; see canonical reviewer alias algorithm below. (REQ-013-014)
- Photos and text must not expose sensitive personal information; admin may redact or remove post-publication. (REQ-013-051)
- Review content (review record + photos + provider responses + takedown requests) retained per the system PRD, Platform-Wide Rules: One 10-year retention period; approved takedown requests are processed by unpublish + archival with restricted access — never hard-deleted. (REQ-013-048; REQ-SYS-002)
- `AdminAction` and all audit-log records (patient self-edits, admin edits/removals/seeded reviews, takedown decisions, settings changes, provider responses) are immutable (Constitution §VI, Audit Trail); retention follows the system PRD, Platform-Wide Rules: One 10-year retention period. (REQ-013-049; REQ-SYS-002)
- All review mutations are fully auditable (who, when, what, before/after, reason where applicable), including patient self-edits to published reviews, admin actions (edits, removals, seeded reviews, takedown decisions, settings changes), and provider response creation. Audit records preserve actor type (patient / provider / admin) and prior field values to satisfy constitution Auditability requirements. (REQ-013-050)
- Reviewer alias algorithm (canonical, applied uniformly across Patient, Provider, and Admin public surfaces): `{first_name} {last_initial}.` (e.g., "Sarah M."); collisions within the same provider's review list are deduplicated with a numeric suffix (`Sarah M. 2`, `Sarah M. 3`, …). Admin-seeded reviews use an admin-entered `reviewer_display_name` field (free text, subject to the same PII-safety policy — no full last name, no contact info) instead of the algorithmic alias; the `Verified Off-platform` badge accompanies the display name. Public surfaces always show the alias; there is no setting or option to change that. Admin views may unmask the patient identity per RBAC for review handling; this is not a public display option. (REQ-013-052)
- Enforce RBAC for submit/moderate/respond actions. (REQ-013-074)

### Admin Editability Rules

Editable by Admin:

- Review categories/labels. (Reminder cadence is configured in FR-030, not here.) (REQ-013-070)
- Photo guidelines text; removal reasons catalogue. (REQ-013-070)
- Insert authenticated reviews and edit/remove existing reviews with mandatory reasons. (REQ-013-039)

Fixed in Codebase (Not Editable):

- Eligibility logic requires a case marked Completed and the time threshold. (REQ-013-027)
- Minimum and maximum lengths for text fields and rating scale bounds. (REQ-013-027)

Configurable with Restrictions:

- Flagging thresholds and auto-flag rules for admin review (within safe bounds approved by policy). (REQ-013-069)
- Takedown decision SLA/queue prioritization parameters; the takedown decision deadline runs from 12 hours to 7 days and defaults to 48 hours. (REQ-013-069; REQ-013-078)

Admin-Seeded Review Policy:

- Admin-imported authenticated reviews must be flagged as "Verified Off‑platform" with verification source and date. These are published directly by admin (no patient submission flow). See REQ-013-077 for the placeholder patient and procedure. (REQ-013-035)

---

## Dependencies

Related FRs: FR-010 (review eligibility is proven by the FR-010 treatment record marked Completed; the day it was marked Completed starts the 3 months), FR-014 (consumes published ratings, category sub-scores and recalculated averages; REQ-014-207, REQ-014-284), FR-020 (invite/reminder delivery, new published review alerts to providers, provider response alerts, admin removal notices sent to the reviewing patient only, and takedown decision notifications; REQ-020-131, REQ-020-132, REQ-020-133, REQ-020-134, REQ-020-135, REQ-020-152), FR-022 (provider/admin review list filters and search fields must remain represented in the FR-022 master reference when filter criteria change; REQ-022-092, REQ-022-093), FR-030 (configurable review event mapping, recipient/channel rules, reminder cadence, and notification templates, including the notice to the provider when an admin removes a response; REQ-030-086, REQ-030-087, REQ-030-088, REQ-030-089, REQ-030-090), FR-032 (provider organization-level review notification preference toggle and channel settings; REQ-032-050). Related modules: P-01 (identity and role context), P-03 (confirm procedure completion and dates for eligibility/time gating), PR-06 (provider review display context, provider response surface, and provider review notification preference consumption), S-03 (invitations, reminders, admin removal notifications, and provider response alerts), S-05 (secure handling of review photos).

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

1. Given an eligible patient, when they submit required ratings and feedback, then the review is published immediately and the patient sees confirmation. (REQ-013-034)
2. Given valid photos, when uploaded, then the system accepts and associates them with the review.
3. Given a published review, when the provider profile loads, then averages and distribution reflect the new review. (REQ-013-031)

### User Story 3 – Patient requests takedown for submitted review (P1)

Why: Give patient a governed way to remove review visibility without direct hard delete.

Independent Test: Patient submits takedown request from review detail; admin receives pending request and patient receives final decision notification.

Acceptance Scenarios:

1. Given a published review, when patient submits takedown request with reason, then request is created with `Pending` status and visible in admin queue.
2. Given a pending request, when admin approves it, then review is unpublished/archived, metrics are recalculated, and patient is notified.
3. Given a pending request, when admin rejects it, then review remains published and patient receives rejection reason, which is also shown on Review Detail (Screen 3).

### User Story 4 – Provider reviews feedback across treatment cases (P1)

Why: Provider needs operational visibility for multi-case patient histories.

Independent Test: Provider opens reviews list, filters by treatment/rating/date, and opens review detail.

Acceptance Scenarios:

1. Given provider with many reviews, when they apply filters (treatment/rating/date), then list returns only matching reviews.
2. Given selected review, when provider opens detail, then full canonical payload and treatment context are displayed.

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

Why: Admin needs controlled configuration for review labels, flagging thresholds, takedown deadline, and reporting without changing fixed compliance rules; reminder cadence is configured through FR-030 link-outs.

Independent Test: Admin updates review settings and exports a report; changes are audit logged and fixed eligibility/privacy/retention rules remain unchanged.

Acceptance Scenarios:

1. Given admin updates review labels or moderation settings, when settings are saved, then the change is audit logged and future review flows use the updated setting.
2. Given admin exports reviews or takedown data, when export completes, then the export is RBAC-restricted and audit logged.

### Edge Cases

- Ineligible attempts (too early, case not marked Completed, or both reviews of the case already used) are blocked with clear messaging; the submission screen says no more reviews can be submitted for the case. (REQ-013-025)
- Photos exceed limits: user informed, upload prevented until compliant. (REQ-013-028)
- Duplicate or spam reviews: auto‑flag for admin review post-publication; see REQ-013-073 and REQ-013-079.
- Takedown request approved: see REQ-013-046.
- Takedown request rejected: see REQ-013-046.
- Takedown request approved: the patient may submit one further review for the case (REQ-013-002).
- Admin removes a review while a takedown request is Pending: the request closes as Approved (REQ-013-016).
- Admin policy removal: the patient may submit one further review for the case (REQ-013-002).

---

## Functional Requirements Summary

### Core Requirements

- **REQ-013-001**: System MUST allow eligible patients, those with a treatment case marked Completed in FR-010 (not Closed Early or Cancelled), to submit reviews (overall + categories, feedback, optional photos).
- **REQ-013-002**: System MUST enforce time gating (≥ 3 months counted from the day the case was marked Completed) and one published review per treatment case. After a removal (approved takedown or admin policy removal) the patient MAY submit one further review for the case; a case has at most two reviews in total, so once the further review is removed the case cannot be reviewed again. Removed reviews are kept in the archive and are never restored.
- **REQ-013-003**: System MUST publish reviews immediately upon patient submission (no pre-publication moderation gate).
- **REQ-013-004**: System MUST provide patient submitted-review list and review-detail views across treatment cases.
- **REQ-013-005**: System MUST provide patient takedown request flow (submit -> pending -> admin decision -> notification), and MUST NOT allow direct patient deletion of submitted reviews.
- **REQ-013-006**: System MUST display published reviews on patient-facing provider/clinic profile and offer-evaluation surfaces with ratings summary, review list, provider responses, public-safe media, and `Verified Off-platform` markers when applicable.
- **REQ-013-007**: System MUST provide admin capabilities to insert authenticated reviews, edit existing reviews, remove reviews, and process takedown requests with full audit trail.
- **REQ-013-008**: System MUST calculate and display provider average rating, count, and distribution over Published or Flagged reviews, including admin-seeded `Verified Off-platform` reviews.
- **REQ-013-009**: System MUST provide provider-side list/filter/detail screens across treatment cases, including search by reviewer alias and filtering by treatment, rating, date, response status, and source type.

### Data Requirements

- **REQ-013-010**: System MUST link reviews to patient, provider, and completed procedure records.
- **REQ-013-011**: System MUST securely store and retrieve review photos with metadata.
- **REQ-013-012**: System MUST persist takedown request records including reason, status, decision note, requester, decider, and timestamps.
- **REQ-013-013**: System MUST preserve a single canonical review schema across Patient, Provider, and Admin platforms (`overall_rating`, `facility_rating`, `staff_rating`, `results_rating`, `value_rating`, `feedback_text`, `photos[]`, plus read-only clinic/treatment context fields).
- **REQ-013-077**: Each admin-seeded (off-platform) review MUST be linked to a placeholder patient and a placeholder procedure, so REQ-013-010 holds for every review. The admin add form takes the provider, treatment, ratings, text and review date, and a reason. The placeholder patient is not a person, so notices addressed to it are suppressed.

### Security & Privacy Requirements

- **REQ-013-014**: System MUST always alias reviewer identity and prevent exposure of PII in public views.
- **REQ-013-015**: System MUST encrypt review data and photos in transit and at rest and maintain auditable logs.
- **REQ-013-016**: System MUST support unpublish + archival for compliance removals and approved takedown requests; an admin removal of a review also closes any Pending takedown request on it as Approved, decided by the removing admin at the removal time with the removal reason as its decision note (audited as the `remove` action with the takedown request id; the patient gets the removal notice only). A removal or approved takedown clears any flag reason, and a Removed review is read-only for admins. There is no Restore action.
- **REQ-013-079**: A review with status Flagged MUST stay publicly visible until an admin removes it; patients and the public see it as Published. Every rule keyed on Published (visibility, patient Edit and Request Takedown, provider Respond, the rating aggregates and the sub-score endpoint) also covers Flagged, so setting or clearing a flag needs no recalculation. An admin resolves a flag as uphold or redact (back to Published, flag reason cleared) or unpublish.

### Integration Requirements

- **REQ-013-017**: The review module raises a notification on each of these events: new published review, provider reply, admin removal of a review (to the reviewing patient), admin removal of a provider response (to the provider, with the reason), takedown decision, review edited by the patient (to the provider, informational only), review edited by an admin (to the reviewing patient), takedown requested (to admins), and takedown overdue (to admins). Notices that would go to the placeholder patient of an admin-seeded review are not sent. The invitation fires on the eligibility date (3 months after the treatment case was marked Completed in FR-010) and reminder timing counts from that date; reminder cadence is owned by FR-030. Delivery, recipients, content and opt-out follow the notification-service Rule in FR-020 and the FR-030 notification catalogue.
- **REQ-013-018**: System MUST provide ratings summary endpoints for provider profiles with caching.
- **REQ-013-018a**: System MUST additionally expose a per-treatment aggregated sub-scores endpoint that returns, for a given provider, `{treatment_id → {avg_overall, avg_facility, avg_staff, avg_results, avg_value, review_count, distribution}}` over Published or Flagged reviews only. This endpoint is the data contract consumed by FR-014 "review sub-scores per treatment" analytics; cache invalidation MUST be triggered on every change of a review's visibility or rating (publish, edit republish, admin add, admin edit of a rating, removal, unpublish from flag resolution, and approved takedown). (graph id REQ-013-023)
- **REQ-013-019**: Patient Review Detail MUST display provider response (when available), admin removal reason (when removed), and support pre-filled edit flow for published reviews.
- **REQ-013-020**: Takedown request submission MUST use a confirmation modal/bottom-sheet with required patient reason and explicit 10-year retention-policy notice before submission.
- **REQ-013-021**: Provider Review Detail MUST include a documented inline response-composer model/state (not separate screen navigation) with validation, cancel/confirm behavior, and immutable post-publish response rendering.
- **REQ-013-022**: Admin Review Settings MUST support review category labels, photo guidelines, removal reason catalog, restricted flagging/SLA settings, and RBAC-restricted export actions with audit logging. Reviewer identity is always shown as the alias, so there is no display-policy setting. Review reminder cadence is owned by FR-030 (Notification Rules & Configuration); Screen 10 provides link-outs only.
- **REQ-013-078**: Admin Review Settings MUST include a takedown decision deadline setting, from 12 hours to 7 days, that defaults to 48 hours. When the deadline passes on a Pending request, the queue shows it as Overdue and admins are notified; no request is approved or rejected automatically.

---

## Appendix: Change Log

| Date       | Version | Changes                                        | Author |
| --- | --- | --- | --- |
| 2026-11-24 | 1.19 | Logic review closing fixes: provider list and detail show the treatment name only (no case identifier), filter by treatment, response status and source type, with an alias search and no patient or case filter, and Screen 7 gains treatment and response status filters; an admin removal that closes a Pending takedown records the admin, time and removal reason as its decision, is audited as `remove` with the request id, and sends the patient one notice; a redact or removal clears the flag; Respond is hidden once a replacement response was published; the provider gets one notice with the reason when an admin removes its response; a case has at most two reviews in total, with a message when none remain; only cases marked Completed in FR-010 can be reviewed, counted from the day marked Completed (Closed Early and Cancelled cannot); aggregates count Published or Flagged reviews; admin Edit and Remove shown only for Published or Flagged reviews and Removed reviews are read-only; Screens 2 and 3 show the latest takedown request; the alias is always shown publicly with the admin unmask an RBAC view only; admin edit sets the Edited marker without changing the edit count; rate limits cover submissions only; seeded review inputs carry no review photos. | Product Owner / Documentation |
| 2026-11-24 | 1.18 | Logic review fixes: flagged status handled like published; flag resolve, admin review removal and admin response removal specified; recalculation on every visibility or rating change, seeded reviews counted; one published review per case, with one further review after a removal (approved takedown, as before, or admin policy removal), no restore; provider review list loses its patient and case filters and gains an alias search; takedown limits (one open request, one further after rejection, no edit while pending, admin removal closes it); takedown deadline bounds 12 hours to 7 days with Overdue and admin notice; Respond needs an active provider account and no active response; audit actor type and id; admin add form inputs and reason; admin edit marker and patient notice; reviewer display policy removed (alias only); invitation anchored to the eligibility date. | Product Owner / Documentation |
| 2026-11-22 | 1.17 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.16) is in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |

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
**Last Updated**: 2026-11-24
