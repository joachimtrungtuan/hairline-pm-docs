# Owner rulings applied (Phase 10 review list closed)

**Date**: 2026-11-25 (Asia/Saigon)
**Type**: Major update (owner rulings applied across FR PRDs, the constitution and the requirements graph). No Change Request (requirements graph programme: new baseline).

## What changed

- **Replacement quote expiry (FR-004 v4.6)**: an admin-authored replacement quote expires like any quote. Save Draft keeps it a draft; "Save and Continue to Acceptance" is the first send and starts the FR-026 expiry.
- **Cancellation policy checkbox (FR-027 v1.9, FR-006 v2.23)**: the checkbox stays on every booking as a stated exception to "once per document version"; the booking stores the policy version shown.
- **No-fault early close (FR-006 v2.23)**: the flow stays admin only. Screen 11 is renamed "Resolve In-Progress Case (Admin Modal)" and gains the route "Move to Aftercare, no fault"; the patient booking detail gains a read-only Early Close Note; new closure cause `no_fault_early_close`.
- **Locked notifications (FR-030 v1.27, FR-001 v2.2, FR-032 v1.21)**: locked guarantees email only; push follows the recipient's own setting.
- **Search audit log (FR-022 v2.28)**: a back-office record with no screen.
- **Email delivery issue flag (FR-015 v1.33, FR-030 v1.28, FR-016 v1.21)**: providers carry the same flag as patients; admins see it read-only on the provider detail and the patient overview; it clears automatically on a later delivered email or a verified address change.
- **Billing settings (FR-032 v1.21, FR-031 v1.8, system-prd.md)**: the permission is split into View Billing Settings (grantable; default Owner and Billing Staff) and Edit Billing Settings (Owner only, not grantable).
- **Constitution 1.1.0**: corrected to match the system PRD and the FR PRDs (affiliate portal as a fourth application, aftercare P1, MFA as a future feature, lockout as an admin setting, hard deletion prohibited, one 10-year retention period, Android 10+, mobile load under 3 seconds, Part C aligned to the PRD structure checklist). `constitution-open-items.md` now holds only the remaining technical points.
- **Neighbour wording (FR-003 v2.21, FR-006 v2.24, FR-020 v2.20, FR-030 v1.29, FR-014 v3.25, FR-018 v2.10)**: admin cancel and Close inquiry cover any open replacement quote, draft or sent; Time to First Quote leaves out admin-authored replacement quotes; the affiliate portal is described as a fourth application; system PRD NFR-003 marks MFA as a future enhancement.

## Graph

Change-sets `graph/changesets/2026-11-25-owner-rulings-*.yaml` (ten files). Lint count unchanged at 28.

## Follow-up

Three business defaults were applied while filing and are open to reversal: when the email delivery issue flag clears, the replacement quote expiry starting at "Save and Continue to Acceptance", and the admin starting a no-fault close without a provider flag.
