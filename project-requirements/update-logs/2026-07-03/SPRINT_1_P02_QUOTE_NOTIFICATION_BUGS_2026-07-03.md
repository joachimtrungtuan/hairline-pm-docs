# Sprint 1 P-02 Quote Notification Bugs

- Updated `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md` after patient-side quote-notification review during Sprint 1 quote-management testing.
- Replaced the old P-02 `not checked` note with partial coverage for quote-ready notification delivery after provider quote submission.
- Added confirmed bug row `P-02-001` for triplicated patient quote-ready emails from one quote submission.
- Added confirmed bug row `P-02-002` for the quote-ready email CTA and fallback URL exposing a `backend.hairline.app` patient-quote route instead of a valid patient-facing destination.
- Added confirmed bug row `P-02-003` for triplicated patient in-app `New quote` notifications from one quote submission.
- Added confirmed bug row `P-02-004` for wrong relative notification timestamps (`7 hours ago`) on newly submitted quotes in GMT+7 testing.
- Correction: the non-clickable left-side step navigation issue belongs to Provider `PR-02`, not Patient `P-02`; the readiness backlog was updated to move that row to `PR-02-005` while preserving the same evidence link.
- Added provider quote-detail follow-up rows `PR-02-006` through `PR-02-009` for broken visual-plan rendering and clinician-card overflow, missing persisted travel/accommodation selections on reopen, essential day-by-day treatment data being split into a separate `Treatment Plan (Legacy)` tab, and a misleading delete affordance shown for attachments in read-only mode.
- Replaced the placeholder evidence mapping for `PR-02-006` through `PR-02-009` with the persistent uploaded screenshot URLs from the provider quote-detail review set.
- Added confirmed bug row `PR-02-010` for provider quote edit saves failing with `The package field must be a valid UUID` even when unrelated fields are edited.
- Updated the `PR-02` module review notes and provider quote-and-booking checkpoint to mark provider quote list status behavior after create/edit and provider quote-detail re-verification after successful edit save as blocked follow-up coverage behind `PR-02-010`, and to re-scope confirmed-booking visibility as pending only if a provider-side accepted-booking fixture can be prepared without fresh patient-side testing.
- Added confirmed bug row `PR-02-011` for provider quote withdrawal being inaccessible from quote detail and miswired from the quote-list context menu, with launch-plan and FR-004 notes clarifying that provider withdrawal must capture a reason and that accepted-stage withdrawal remains in scope through admin-resolution workflow.
