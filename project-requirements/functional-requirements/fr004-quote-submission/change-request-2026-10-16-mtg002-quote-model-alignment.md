# Change Request: MTG-002 Quote Model Alignment for Quote Submission

**Change Request ID**: CR-FR004-20261016-01
**Primary FR**: FR-004
**Triggering FR / Event**: MTG-002 quote-model verification and Product Owner decision log (2026-10-16); FR-005 v2.5 (CR-FR005-20261016-01) and FR-006 v2.7 (CR-FR006-20261016-01)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v3.0 to v3.4 (v3.1 and v3.2 on 2026-10-16; v3.3 consolidated verification corrections and v3.4 final audit corrections on 2026-10-18)
**Related Commit(s)**: Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

The 2026-10-16 MTG-002 quote-model audit found that FR-004 still re-routed accepted quotes inside FR-004, priced promotions from a live reference, left drafts, expiry, and currency capture undefined, showed a rate-only commission, and kept a duplicate acceptance flag on the option/date-price record. The Product Owner decision log fixes these points. This request records the FR-004 changes: withdrawal after acceptance hands over to the FR-006 provider-fault transfer; promotion terms are fixed at send; expiry and currency are captured at first send; unsent drafts are cancelled silently on acceptance; the package seeding and two edit paths are restated; and quote edits are blocked after acceptance.

## Baseline State

**Source version**: FR-004 v3.0 — Workflows 3 and 6, Alternative Flows, Screen 1 matrix and Tabs 2, 4, 5 and 7, Screens 3, 4, 6 and 7, Business Rules, REQ-004-002 to 005, 011, 012, 018, 025, 032, Key Entities

- Workflow 6 moved `accepted` to `withdrawn` and asked admin to re-route the case to another provider, reschedule, or cancel with refund inside FR-004.
- Option/date-price records held only a live `promotionId` and an `isAccepted` flag; Screens 3 and 6 resolved the live promotion.
- Expiry and currency were captured "when the quote is created", so drafts were ambiguous; expiry was not limited to sent quotes.
- On acceptance, a drafting provider was notified and the draft locked.
- Commission was a read-only percentage rate.
- Provider suspension or deactivation cancelled the accepted parent quote of an affected case with `cancelled_provider_status` (CR-FR004-20261014-01).
- Screen 7 allowed admin inline edits with no post-acceptance guard; Screen 4 kept a parent-level Accept/Decline and an off-enum status list.

## Approved State

**Target version**: FR-004 v3.4 — same headings, plus Workflow 7 (Admin Replacement Quote), Screen 8 (Admin Replacement Quote Authoring), Business Rules "Package library edits and quote inline edits", "Promotions on quotes" and "Commission display", REQ-004-033 to REQ-004-050, and User Story 5.

See the updated [`prd.md`](./prd.md). In summary:

- Each selected package seeds exactly one alternative Quote Option (maximum five), never summed. The standard price prefills each date-range row and the package's relative day plan prefills the option plan. Providers may leave out pairings; each option needs at least one range; subquotes number up to options × ranges.
- Two edit paths: editing in the FR-024 package management screen creates a new library package version; editing inside quote creation changes only a quote-local copy that is never written back. Each option records source package ID, version, and an inline-customised flag.
- The offered price is stored as entered and the discount separately. Promotion terms are copied into the sent quote version at send; eligible automatic promotions attach at send to eligible rows; later promotion edits never change a sent quote.
- Expiry and currency are captured read-only at first send from the FR-026 quote configuration (currency is the FR-029 Default Currency; packages carry no currency); drafts carry neither; no per-quote extension. Only `sent` quotes expire. FR-004 emits `quote.expiring_soon` once per sent parent quote at the FR-026 lead time.
- On acceptance, every other parent quote becomes `cancelled_other_accepted`; sent quotes get one not-selected notice per parent quote and unsent drafts are cancelled silently.
- `acceptedTotal`, `termsAcknowledgedAt` and `lockedExchangeRateSnapshot` are read-only copies written from the FR-005 acceptance snapshot. Acceptance state is derived from FR-005 and is no longer stored on the option/date-price record.
- After acceptance, FR-004 blocks every quote edit by providers and admins; treatment details (plan, clinicians, grafts) change only through FR-010. An accepted quote is never reopened, expired, or restored, including after `Payment Window Expired`, and no new parent quote may be created or sent for that inquiry.
- Provider withdrawal after acceptance moves the parent quote to `withdrawn`, keeps the AcceptanceEvent unchanged, sends the mandatory `quote.withdrawn` notice, and hands the case to the FR-006 provider-fault transfer (Alternative Flow B5) with its payment placeholder.
- `cancelled_provider_status` applies only to unaccepted quotes; an accepted quote of a suspended or deactivated provider keeps `accepted` and follows the FR-006 provider-fault transfer.
- Commission shows model and value (percentage or flat rate), labelled "indicative, final at booking confirmation".
- `confirmed` is stated as a booking status only, never a quote status.
- The option/date appointment date/time and time zone, with the provider, are the FR-006 slot-hold key.
- Every option/date price must be greater than 0 before send; zero is blocked, and a date range the clinic cannot serve is left out of that option.
- If the Default Currency changes while a draft holds prices, the draft switches to the new currency, typed numbers are kept, and a "currency changed, check your prices" banner must be acknowledged before send.
- A sent quote carrying an automatic promotion holds at most one reserved use of its usage limit. A re-send of a new version keeps that reservation, creates one only if the new version newly qualifies, and releases it if the promotion is dropped. The reservation is released when the quote expires, is withdrawn, or ends not selected or cancelled, and is consumed at acceptance. After acceptance, FR-005 and FR-019 own the return of the consumed use if the booking ends in `Payment Window Expired` or is cancelled before the first payment.
- The parent quote records `firstSentAt` on first send; a re-send or new version never changes it.
- The FR-024 treatment Base Price may prefill new option/date-price rows only where no other standard value exists and is never read after send.
- FR-004 owns `quote.updated`, emitted when a new version of an already-sent quote is re-sent and described as "quote revised (new version)". The old "significant edits" trigger is removed; saving a draft edit without re-sending notifies no one (v3.3).
- FR-004 emits `quote.submitted` on first send and `quote.expired` on expiry processing (v3.3).
- FR-004 is the only producer of `quote.withdrawn`. The patient is always notified; the admin is notified only when the withdrawn quote was already accepted. FR-006 reacts by starting the provider-fault transfer and does not emit the event (v3.3).
- During an FR-006 provider-fault transfer before treatment starts (Accepted or Confirmed), an admin authors a replacement quote for the replacement provider in the same inquiry through Screen 8. This is the only exception to the no-new-quote-after-acceptance block. The quote is marked `authorType = admin`, links to the closed acceptance, emits no `quote.submitted`, and is accepted through an admin-authored acceptance in FR-005. In Aftercare only the aftercare provider or team is reassigned, with no new quote (v3.4).
- Patient cancellation is possible only in Inquiry or Quoted. An admin booking cancellation after acceptance leaves the accepted quote `accepted` (v3.4).
- At most one automatic promotion is attached per quote, chosen by the FR-019 priority order. A reserved use is released with `not_applied` when the accepted row does not carry the promotion (v3.4).
- Price, currency, date range and promotion never change after acceptance; the appointment changes only through the FR-006 admin change and the snapshot keeps the baseline (v3.4).
- An admin edit of a sent quote creates a new version and emits `quote.updated` on re-send. Quote no longer lists fields FR-004 does not own; the last editor is read from QuoteAudit (v3.4).
- No automatic promotion attaches to an admin-authored replacement quote and no promotion reservation is taken; the admin sets the price directly. An unaccepted replacement quote expires under normal expiry, the inquiry stays `supportRequired`, and the admin may author another replacement quote or cancel (v3.4).

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Workflow 6, REQ-004-004, REQ-004-012 | Withdrawal after acceptance re-routed by admin inside FR-004 | `accepted` to `withdrawn`, then FR-006 provider-fault transfer; money per FR-006 placeholder | S1-3; D3, D6, D6-M, D22 |
| Promotion on option/date price | Live `promotionId`; gross or net price undefined | Price as entered, discount separate, terms copied at send, automatic promotions attached at send | FR-004-5; D10, D12, M14 |
| Drafts on acceptance | Drafting provider notified; draft locked | Draft cancelled as `cancelled_other_accepted` silently | FR-020-2; D5, P2 |
| Commission field | Read-only percentage rate | Model and value (percentage or flat rate), labelled indicative | S2-4; D13 |
| Expiry and currency | Captured at quote creation; expiry not limited to sent quotes | Captured at first send from FR-026; drafts carry neither; only sent quotes expire; expiring-soon producer defined | FR-026-2, FR-004-1, S4-6; D15, D16, D18, M11 |
| Quote status enum | No explicit rule on `confirmed` | `confirmed` is a booking status only | S5-6; D23 |
| Post-PWE quote state | Undefined | Accepted quote never reopens; no new quote for the inquiry | S1-1; D1 |
| Package seeding and edit paths | One-to-five options; inline copies local | One package seeds one option; prefill rules; omitted pairings; library versioning contrasted with quote-local copies | FR-024-2, FR-024-8, FR-024-7; D17, M1, M10, R7-2 |
| Screen 7 and post-acceptance edits | No acceptance guard | Edits blocked after acceptance; treatment details via FR-010 | FR-004-4; M2 |
| Appointment fields | Start time only | Named as the FR-006 hold key; no appointment at quote time | S1-6; M4 |
| Provider-status cascade | Accepted parent quote cancelled with `cancelled_provider_status` | Unaccepted quotes only; accepted quote follows FR-006 provider-fault transfer | M18 |
| Acceptance fields | `isAccepted` stored on option/date price; `acceptedTotal` source unstated | Acceptance state derived from FR-005; accepted total written from the snapshot | FR-005 v2.5 handoff; M12 |
| Screen 4 | Parent-level Accept/Decline; off-enum badges | Subquote-scoped acceptance via FR-005; badges mapped to the enum, Not Selected shown | FR-004-6 |
| Minor corrections | Tab 3 lists graft description as editable; Screen 7 item cost rule; provenance row; restricted-recipient "initial quote"; option/date uniqueness and future appointment | Corrected | FR-004-7, 10, 11, 12, 14 |
| CR-FR004-20260909-01 | Schema "reconciled"; FR-005/006/008 reconciliation "open and unscheduled"; v2.7–2.8 untraced | Corrected to point at this pass and the existing CRs | FR-004-8, FR-004-9; M12, R7-1 |
| Option/date price validation (v3.2) | Non-negative price | Greater than 0; zero blocks send; unservable ranges left out | Q3 |
| Default Currency change on a draft (v3.2) | Undefined | New currency, typed numbers kept, acknowledged banner required before send | Q4 |
| Automatic promotion usage limit (v3.2, corrected v3.3) | Undefined between send and acceptance | A sent quote holds at most one reserved use; a re-send of a new version keeps it, creates one only if the new version newly qualifies, and releases it if the promotion is dropped; released on expiry, withdrawal, not selected, or cancellation; consumed at acceptance | Q6, Q29 |
| First-send timestamp (v3.2) | `firstSentAt` captured at first send; re-send effect unstated | Set once on first send; never changed by a re-send or new version | Q15 |
| FR-024 treatment Base Price (v3.2) | Not referenced | Reference-only prefill where no other standard value exists; never read after send | Q20 |
| `quote.updated` producer (v3.2, corrected v3.3) | Undefined; Workflow 2 notified the patient of "significant edits" | FR-004 emits it on re-send of a new version, described as "quote revised (new version)"; the "significant edits" trigger is removed | Q24 |
| `quote.submitted` and `quote.expired` producer (v3.3) | FR-004 did not name these events | FR-004 emits `quote.submitted` on first send and `quote.expired` on expiry processing (REQ-004-046) | Q24 |
| `quote.withdrawn` producer and recipients (v3.3) | Patient and admin on every withdrawal; producer not stated as exclusive | FR-004 is the only producer; patient always, admin only after acceptance (REQ-004-047) | Q11, Q31 |
| Replacement quote during provider-fault transfer (v3.4) | No new quote after acceptance, with no exception | Admin authors a replacement quote through Workflow 7 and Screen 8 (`authorType`, `replacementForAcceptanceEventId`; REQ-004-048); Aftercare reassigns the team only | Q35, Q36, Q43 |
| Patient cancellation cascade (v3.4) | Patient could cancel through Accepted | Patient cancels only in Inquiry or Quoted; admin booking cancellation leaves the accepted quote `accepted` | Q37 |
| Automatic promotions per quote (v3.4) | Several could attach; release reasons excluded `not_applied` | One per quote by the FR-019 priority order; `not_applied` release (REQ-004-035, REQ-004-042) | Q39, Q40 |
| Admin edit of a sent quote (v3.4) | Admin editor role not tied to versioning | New version and `quote.updated` on re-send (REQ-004-049) | Q24, Q43 |
| Replacement quote pricing and expiry (v3.4) | Screen 8 offered a promotion field; one replacement quote per transfer; unaccepted replacement quote undefined | No automatic promotion and no reservation; admin sets the price directly; an unaccepted replacement quote expires normally, the inquiry stays `supportRequired`, and the admin may author another or cancel (REQ-004-050) | Q48, Q49 |

## Scope and Impact

### In Scope

- FR-004 quote lifecycle, promotion capture, expiry and currency capture, package seeding, edit paths, post-acceptance guards, and the handover to FR-006.

### Out of Scope

- Payment rails, fund release, refunds, and later instalments, except the FR-006 provider-fault payment placeholder and the first-payment `Payment Window Expired` boundary that FR-004 references.
- Product code, API, database, or UI implementation changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Quote Hierarchy; Workflows 1, 2, 3, 5, 6 and 7; Alternative Flows; Screen 1 (matrix, Tabs 2, 3, 4, 5, 7, Sub-screen 2A); Screens 3, 4, 6, 7, 8; Business Rules; REQ-004-002 to 005, 011, 012, 018, 025, 032, 033 to 049; Key Entities; Dependencies; Integration Points; Edge Cases; Glossary; User Stories 3 and 5.
- **Related FRs**: FR-005 (subquote identity and acceptance state, acceptance snapshot, supersession record); FR-006 (slot-hold key, provider-fault transfer B4/B5, PWE); FR-010 (post-acceptance treatment-detail changes, drop-out routing); FR-015 (provider-status cascade limited to unaccepted quotes); FR-019 (promotion terms copied at send, automatic promotions); FR-020 and FR-030 (mandatory `quote.withdrawn` with FR-004 as the only producer and admin recipient after acceptance only, `quote.submitted`, `quote.updated` and `quote.expired` producers, one not-selected notice per parent quote, no notice for drafts, `quote.expiring_soon` producer and lead time); FR-022 (quote status filters); FR-024 (package versions, one package per option, day plan in package); FR-026 (expiry, currency, quote-expiring-soon lead time captured at first send); FR-029 (Default Currency, commission model and value).
- **System documents**: `system-data-schema.md` (`quotes.version`, `quote_versions`, `quote_audits`, `first_sent_at`, accepted-total and locked-exchange-rate fields pointing to the acceptance snapshot, promotion terms on option/date prices, removal of `isAccepted` and `confirmed`; `quotes.author_type` and `quotes.replacement_for_acceptance_event_id` for the admin replacement quote; release reason `not_applied`; inquiry-cancellation transitions from draft and expired); `system-technical-spec.md`; `system-prd.md` FR-004 section.
- **Partly supersedes**: CR-FR004-20261014-01, for accepted parent quotes only.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Quote status transitions on acceptance, withdrawal and provider-status events; promotion storage and send-time capture; expiry and currency capture; admin inline edit guards; option/date-price schema; notifications; package version provenance.
- **Compatibility / rollout risk**: Existing sent quotes hold live promotion references; they need their terms copied before the live lookup is removed.
- **Data migration**: To be assessed.

## Acceptance and Validation

- No FR-004 text prices a sent quote from a live `promotionId`.
- Workflow 6 contains no re-routing inside FR-004 and hands over to FR-006 Alternative Flow B5.
- The commission field label reads exactly "indicative, final at booking confirmation".
- No quote status `confirmed` exists in FR-004.
- Both the library edit path and the quote inline edit path are named and contrasted.
- `cancelled_provider_status` is never applied to an accepted quote.
- An option/date price of 0 blocks send (REQ-004-040).
- A Default Currency change on a draft keeps typed numbers and blocks send until the banner is acknowledged (REQ-004-041).
- A sent quote holds at most one reserved use of an automatic promotion's usage limit; a re-send of a new version keeps it, creates one only if the new version newly qualifies, and releases it if the promotion is dropped; the reservation is released on expiry, withdrawal, not selected, or cancellation, and consumed at acceptance (REQ-004-042).
- `firstSentAt` is unchanged after a re-send or new version (REQ-004-043).
- The FR-024 treatment Base Price is never read after send (REQ-004-044).
- `quote.updated` is emitted only by FR-004, on re-send of a new version of a sent quote (REQ-004-045); no FR-004 text uses a "significant edits" trigger.
- FR-004 states that it emits `quote.submitted` on first send and `quote.expired` on expiry processing (REQ-004-046).
- FR-004 is the only producer of `quote.withdrawn`; the admin receives it only for an already-accepted quote (REQ-004-047).
- FR-004 allows a new quote after acceptance only as an admin replacement quote during an FR-006 provider-fault transfer before treatment starts, authored through Screen 8 (REQ-004-048).
- FR-004 attaches at most one automatic promotion per quote and uses `not_applied` for an unused reservation.
- No FR-004 text lets the patient cancel after acceptance or moves the accepted quote out of `accepted` on an admin booking cancellation.
- A replacement quote carries no automatic promotion or reservation, and an unaccepted one expires normally while the inquiry stays `supportRequired` (REQ-004-050).
- Implementation reconciliation stays Required until code, API, data, and regression evidence are verified.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner — documentation approved 2026-10-16 via the decision log; implementation reconciliation required, not assessed
- **Decision evidence**: SRC-MTG-002; `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (D1, D3, D5, D6, D6-M, D10, D12, D13, D15, D16, D17, D18, D22, D23, M1, M2, M4, M10, M11, M12, M14, M18, P2, R7-1, R7-2, R7-3; Q-series Q3, Q4, Q6, Q11, Q15, Q20, Q24, Q29, Q30, Q31, Q35, Q36, Q37, Q39, Q40, Q42, Q43, Q48, Q49); consolidated verification 2026-10-18; fix plan `reports/2026-10-16/mtg002-quote-model-fix-plan-2026-10-16.md` (E004-1 to E004-12)
- **PRD change log**: FR-004 v3.1 and v3.2 rows dated 2026-10-16; v3.3 row dated 2026-10-18 (consolidated verification corrections); v3.4 row dated 2026-10-18 (final audit corrections)
- **Update log**: `../../update-logs/2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md`
- **Supersedes**: CR-FR004-20261014-01 in part (accepted parent quotes under the provider-status cascade)
- **Superseded by**: None
