# Mobile Bug Report Template - 2026-05-06

## Summary

Created a new dated mobile bug report template for the next testing cycle by copying the April 23 report structure and replacing prior bug content with a reusable `HL71` starter row.

## What Was Created

- **File**: `local-docs/reports/2026-05-06/mobile-bug-report-hl71.md`
- New report date folder for the next mobile app testing run
- Starting bug code updated from `HL61` to `HL71`
- Original table structure preserved: Date, Description & Screenshot / video, Bug Status, Reported By, Issue Type, Platform, Device & OS version, Comments

## Template Changes

- Replaced prior bug-specific content with a reusable `HL71` row template
- Kept the report skeleton while removing previous bug evidence and screenshots
- Added explicit fill-in guidance for:
  - bug title
  - pre-condition
  - test steps
  - test data
  - expected result
  - actual result
  - backend evidence
  - suspected layer / root cause direction
  - screenshot / video evidence
- Added a quality checklist so future AI agents write bug rows that are actionable for developers and traceable to API-level evidence

## Intended Use

Duplicate the `HL71` row for `HL72` onward during the new testing process and replace the instructional text with real bug content as each issue is verified.

## Follow-up Updates

- Replaced the placeholder `HL71` row with the first real verified bug for the new cycle: the patient confirmed screen exposes `Book hotel` / `Book flight` actions for a quote whose backend travel path is already `provider_included`, and the user only sees the restriction after entering the invalid subflows.
- Added `HL72` for the `Thin 0505 2` Path B travel inconsistency: the backend still retains submitted outbound-flight and hotel records while also accepting `no_travel_required=true` for the same quote, and the app keeps routing the patient back into an outbound submission flow instead of a read-only or correction state.
- Refined `HL72` with the follow-up toast evidence `Already marked as no travel required` and narrowed the bug scope to the mobile app only; backend/API state remains in the row strictly as reference evidence for the state the app should render.
- Replaced `HL73` with the narrower mobile UX/UI finding for `Thin 0505 2` and removed the unnecessary return-flight discussion. The row now stays focused only on fields the patient actually entered but which later render as `Not provided` in the app.
- Added `HL74` for the patient Help Center content mismatch: backend already contains FAQ, article, resource, and video datasets, but the app does not reflect those datasets consistently across counters, resources, and videos.
- Attached the 6 LetWeb screenshot links for `HL74`: `https://s.letweb.net/s/emoz99`, `https://s.letweb.net/s/ejnl19`, `https://s.letweb.net/s/dkmo17`, `https://s.letweb.net/s/gl9r3m`, `https://s.letweb.net/s/emoz98`, `https://s.letweb.net/s/dn5r1j`.
- Added `HL75` for the patient support-ticket reply validation UX. The backend reply endpoint works and enforces `message|min:10`, but the app currently surfaces only a generic `Validation failed` toast instead of telling the patient that the reply must be at least 10 characters.
- Attached the LetWeb screenshot link for `HL75`: `https://s.letweb.net/s/gxj9zw`.
- Added `HL76` for the patient support-ticket list refresh UX, then narrowed it to the missing pull-to-refresh interaction only so the scope stays on the requested app affordance rather than broader auto-refresh behavior.
- Added `HL77` for the patient notifications UX: notification cards are visible for support-ticket and quote/travel updates, but tapping them does not deep-link the patient into the related support ticket, quote, or treatment destination in the app.
