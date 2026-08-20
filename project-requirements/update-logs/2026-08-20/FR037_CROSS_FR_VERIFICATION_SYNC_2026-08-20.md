# FR-037 Cross-FR Verification Sync

**Date**: 2026-08-20
**Documents**:
- `functional-requirements/fr037-monitor-hair-loss/prd.md` (v1.7 → v1.8)
- `functional-requirements/fr003-inquiry-submission/prd.md` (v1.9 → v2.0)
- `functional-requirements/fr004-quote-submission/prd.md` (v1.8 → v1.9)
- `functional-requirements/fr025-medical-questionnaire-management/prd.md` (v2.2 → v2.3)
- `functional-requirements/fr020-notifications-alerts/prd.md` (v1.9 → v2.0)
- `functional-requirements/fr030-notification-rules-config/prd.md` (v1.4 → v1.5)

**Trigger**: Approved resolutions (Option 1 for Issues 1-3, suggested fix for Issue 4) from the FR-037 verification report

---

## Decisions Applied

- **Issue 1 (Critical)** — FR-037's monitoring-conversion exclusive-provider routing (REQ-037-029, Business Rule 7) is now documented on both sides of the handoff: FR-003 Workflow 2 gains an override branch and Alternative Flow B3 routing conversion inquiries directly to the assigned provider (bypassing country/selection matching and the 10-provider cap), and FR-004 gains a restricted-recipient mode limiting initial quote creation on those inquiries to the assigned provider. Both files add FR-037/FR-038 as dependencies.
- **Issue 2 (Medium)** — FR-025 gains a "System-Triggered (Monitoring Advice)" entry point documenting that FR-037 reuses the active Inquiry-context questionnaire set to gate provider-advice mode access, plus a corresponding FR-037 dependency entry.
- **Issue 3 (Medium)** — FR-037's 8 proposed `monitoring.*` events are added as real catalog rows (not just "candidates") to both FR-030 (source of truth) and FR-020 (mirror), keeping the two tables identical per their own stated mirror relationship. Both files add FR-037/FR-038 as dependencies.
- **Issue 4 (Minor)** — FR-037's own Dependencies section gains a one-line FR-038 cross-reference, for symmetry with FR-038's existing reciprocal references to FR-037.

## Validation

- Confirmed FR-003's Workflow 2 diagram and Alternative Flow B3 correctly gate on an exclusive assigned provider before falling back to normal distribution, and that the 10-provider cap and country matching are only skipped on that branch.
- Confirmed FR-004's restricted-recipient rule is scoped to initial quote creation only, and does not alter Workflows 2-6 (editing, expiry, withdrawal, admin oversight).
- Confirmed FR-020 and FR-030's Monitoring event rows are identical in content and table position (inserted between Aftercare and Reviews) in both files.
- Confirmed FR-025's new entry point is numbered correctly in sequence and does not introduce a new admin toggle or context type, matching FR-037's actual reuse of the existing active Inquiry-context set.
- Confirmed all six PRDs' Appendix: Change Log tables received a new row with the correct next version number and existing column order for that file.
- Checked all edited Markdown tables for stray `|` characters and correct row placement.
