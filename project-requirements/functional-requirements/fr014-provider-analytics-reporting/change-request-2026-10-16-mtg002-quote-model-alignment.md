# Change Request: Confirmed-Only Booking Load and Country Booking Figures (MTG-002 Quote Model Alignment)

**Change Request ID**: CR-FR014-20261016-01
**Primary FR**: FR-014
**Triggering FR / Event**: MTG-002 quote model audit and Product Owner decision log of 2026-10-16 (FR-006 booking lifecycle with audited Payment Window Expired revive)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v3.14 to v3.16
**Related Commit(s)**: Pending

> Created under decision P1: FR-014 implementation status is unknown, so this delta is recorded as a Change Request to be safe.

---

## Decision Summary

The Product Owner confirmed (decision M7, finding FR-014-2) that provider booking load and country booking figures count Confirmed bookings only. FR-006 creates a Booking at acceptance (`Accepted`, held) and keeps it through `Payment Window Expired`, so an unfiltered booking count would show released or never-paid slots as load and inflate country booking rates above the funnel conversion rate. No separate held figure is added. The TTFQ and inquiry response rate cohort difference (finding FR-014-3) is kept as approved and now disclosed. The FR-006 dependency note reflects the audited admin revive of `Payment Window Expired` bookings (decision D2).

## Baseline State

**Source version**: v3.14 — Screen 1 B3 and B4, Screen 3 Widget 1, Screen 10 Widget 1, Analytics Counting & Time Basis, Dependencies (FR-006), Key Entities (Entity 2)

`Bookings_on_day` had no booking status filter. Screen 1 B4, Screen 3 Widget 1 and Screen 10 Widget 1 used the label "Booked" without naming which FR-006 statuses count. The TTFQ cohort (inquiry-created) and the response rate cohort (distribution period) differed without disclosure. The FR-006 dependency described Payment Window Expired as terminal.

## Approved State

**Target version**: v3.16 — same headings plus REQ-014-116

TTFQ ends at the `first_sent_at` of the provider's earliest parent quote for the inquiry, set by FR-004 on first send; a re-send or new version never changes it.

Booking load and country booking figures count only FR-006 Bookings in `Confirmed` or `In Progress` status; `Accepted` (held), `Payment Window Expired` and `Cancelled` bookings never count, and no held figure is shown. "Booked" is relabelled "Confirmed bookings" and follows the funnel's inquiry cohort and Confirmed booking stage. TTFQ keeps the inquiry-created cohort; tooltips and exports state each metric's cohort basis. The FR-006 dependency names the audited revive to `Accepted` with a fresh hold.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Screen 1 B3 Booking Intensity and Entity 2 | `bookings_on_day` counted Bookings with no status filter | Counts `Confirmed` and `In Progress` Bookings by appointment date; held, Payment Window Expired and Cancelled excluded; no held figure; tooltip reads "Confirmed bookings" | MTG-002; FR-014-2; M7 |
| Screen 1 B4, Screen 3 Widget 1, Screen 10 Widget 1 | "Booked" and "Booked rate" with undefined status basis | "Confirmed bookings" and "Confirmed booking rate", using the funnel inquiry cohort and Confirmed booking stage | MTG-002; FR-014-2; M7 |
| REQ-014-045, new REQ-014-116 | "booked count"; no requirement for booking status filter | Confirmed booking count; REQ-014-116 fixes the Confirmed-only rule across the affected widgets | FR-014-2; M7 |
| TTFQ cohort disclosure | Inquiry-created cohort, silently different from response rate's distribution cohort | Same cohort, difference stated as intentional and shown in tooltips and exports | FR-014-3; confirmed by Q16 |
| TTFQ end point (v3.16) | Earliest parent first-submission `sent_at` | `first_sent_at` of the provider's earliest parent quote for the inquiry, set by FR-004 on first send and never changed by a re-send or new version | Q15 |
| FR-006 dependency | Payment Window Expired described as terminal | Payment Window Expired outcome and audited admin revive to `Accepted` with a fresh hold | D2 |

## Scope and Impact

### In Scope

- Booking status filter and labels for booking load and country booking figures.
- Cohort disclosure for TTFQ next to the response rate.
- Dependency wording for the FR-006 revive.

### Out of Scope

- Screen 1 layout (locked); only formula definitions and labels change.
- Payment rails, fund release, refunds, later instalments and any deposit-based cash-risk view (payment pass).
- A Payment Window Expired leakage metric (observation FR-014-4; not required now).

### Affected Contracts

- **PRD owner**: `prd.md` — Screen 1 B3/B4, Screen 3 Widget 1, Screen 10 Widget 1, Analytics Counting & Time Basis, Dependencies (FR-006), REQ-014-045, REQ-014-116, Key Entities Entity 2
- **Related FRs**: FR-006 (Booking statuses `Accepted`, `Confirmed`, `In Progress`, `Payment Window Expired`, `Cancelled`, and the audited revive); FR-005 (AcceptanceEvent, accepted snapshot price as the only amount source); FR-004 (parent quote statuses, no `confirmed` quote status); FR-022 (booking status vocabulary must match FR-006)
- **System documents**: `system-prd.md` (FR-014 section labels, if "Booked" is used), `system-data-schema.md` (booking status enum used by the intensity aggregate)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Analytics aggregation queries for booking intensity and country booking counts; dashboard labels and tooltips; export definitions
- **Compatibility / rollout risk**: Historical intensity and country figures will drop where held or expired bookings were counted; recompute cached aggregates on rollout
- **Data migration**: To be assessed (aggregate recompute only)

## Acceptance and Validation

- B3 shows no load for a day whose only Bookings are `Accepted`, `Payment Window Expired` or `Cancelled`.
- Country confirmed booking rate never exceeds the funnel's Confirmed booking conversion for the same cohort.
- No "Booked" label remains on Screens 1, 3 and 10; Screen 8 and exports state the TTFQ and response rate cohorts.
- Booking states in FR-014 match FR-006, FR-022 and the schema.
- TTFQ ends at the provider's earliest parent quote `first_sent_at`; a re-send or new version of that quote leaves the TTFQ observation unchanged.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner — documentation approved 2026-10-16 via the decision log; implementation reconciliation required, not assessed
- **Decision evidence**: `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (M7, D2, P1; Q-series Q15, Q16); `reports/2026-10-16/mtg002-quote-model-fix-plan-2026-10-16.md` (E014-1)
- **PRD change log**: v3.15 and v3.16 rows (2026-10-16)
- **Update log**: Pending (written by the controller for 2026-10-16)
- **Supersedes**: None
- **Superseded by**: None
