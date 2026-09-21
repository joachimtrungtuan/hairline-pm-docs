# Phase 1 Readiness and Retest Guideline

**Date:** 2026-09-17
**Type:** Release readiness documentation

## Change

Created [Phase 1 readiness and retest guideline](../../../product-plans/2026-09-17/phase-1-readiness-fix-backlog.md) under the user-approved September commercial-pilot release boundary. The [September roadmap](../../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md#recommended-four-phase-release-roadmap) and September 7 deck own scope; the May launch plan and sprint reports remain unchanged as historical references.

## Coverage

- Six essential module slices: PR-01, PR-02, PR-06, A-01, A-02 and A-09.
- Five dependency-ordered checkpoints with 45 retest cases, prerequisites, steps, expected outcomes, evidence fields, and result recording.
- Carried 48 relevant historical bug records with their existing IDs and task lifecycle references. Historical observations are distinct from current retest results and September static risk signals.
- Explicit boundaries for inquiry ingress, pre-payment privacy, provider isolation, role/session enforcement, quote hierarchy and scheduling, Admin oversight, production data, and performance evidence.
- A quick-start guide and meeting summary distinguish function readiness, failures, blocked checks, and pending performance decisions.

## Evidence and limits

OpenCode GO GLM 5.3 Flash with the high variant assisted drafting after explicit user approval to transmit the scoped document sections. The controller reviewed the draft and corrected gate logic, essential-function coverage, phase attribution, links and table formatting.

All 45 retest results remain **Not tested**. No runtime, API, browser, performance, load, reliability or production-readiness proof was obtained in this preparation pass. Historical task lifecycle values were preserved; existing task states were not refreshed from Plane. No product source, frozen automation, root configuration, or prior sprint report was modified.

- 2026-09-17: Added evidence-backed findings A-02-015 through A-02-020 to the September Phase 1 backlog from the partial Admin A-02 provider-creation review.
- 2026-09-17: Updated A-02-002 with current notification 404 evidence while preserving the existing HAIRL-1312 and HAIRL-1313 task references.
- 2026-09-17: Added the provider-list API document-metadata mismatch based on Postman verification of the created provider record.
- 2026-09-17: Added the provider-list Delete action as `Scout flagged` only because FR-015 contains conflicting lifecycle and soft-delete wording; no destructive action was executed.
- 2026-09-17: Recorded that activation, password setup, and provider login remain untested, so RC-1-02 remains `Not tested`.
- 2026-09-17: Added confirmed defect A-02-021 after the Admin provider-list Suspend action remained unchanged for both the new provider and a known-active provider. Postman confirmed the backend status endpoint worked and both records were restored to `active`.
- 2026-09-17: PR-06 review pass on Provider V1 — marked PR-06-003 `Resolved - verified 2026-09-17` after the Account name field followed a reversible clinic-name change; recorded new confirmed defects PR-06-031 (top-right identity falls back to the Owner personal name after logout/login instead of the synced clinic account name) and PR-06-032 (logout completes noticeably slowly), both with persistent screenshot evidence.
- 2026-09-17: Restored the `HAIRL-1339` Plane key into the PR-06-003 Task Status cell as `Resolved - verified 2026-09-17 (BE: HAIRL-1339)` so the tracking key stays in place while the status wording reflects the verified resolution.
- 2026-09-17: Team Management pass on Provider V1 — marked PR-01-002/003/004/009 `Resolved - verified 2026-09-17` with their HAIRL keys preserved in the Task Status cells; recorded new confirmed defects PR-01-012 (team-list Role shows N/A), PR-01-013 (last login stays Never during active session), PR-01-014 (top-right identity role stale until re-login), PR-01-015 (P0: Clinical Staff reach inquiry/quote surfaces against the FR-031 default denial matrix), PR-01-016 (Clinical Staff reach Team/Provider-Profile edit surfaces), PR-01-017 (P0: Team list Suspend produces no status change and does not block login), and PR-06-033 (Provider Profile staff View All does not navigate).
- 2026-09-17: RBAC pass continuation — updated PR-01-015 after the billing-staff account successfully created and submitted quote `43ece55f-aec4-4639-90fb-f267ddf63550` (server-side acceptance confirmed, not a UI-only gap); added PR-02-012 (P0: quote detail exposes unmasked patient name/phone pre-payment) and converted the privacy half of the PR-02 static Scout row to confirmed.
- 2026-09-17: Suspend/revocation pass — marked PR-01-008 `Resolved - verified 2026-09-17` (staff detail shows the captured phone; historical city/country expectation was mis-scoped against FR-009 Screen 8) and PR-01-010 `Resolved - verified 2026-09-17` (detail-page Suspend persists and blocks fresh login); added PR-01-018 (P0: suspension does not revoke the still-active session) and PR-01-019 (Admin shows `Inactive` while Provider shows `Suspended` for the same member, Admin-side evidence TBD).
- 2026-09-17: Admin roster parity — marked A-02-009 `Resolved - verified 2026-09-17` (Admin Staff list shows the new staff member with current role/status); recorded the A-02-010 partial positive (staff not duplicated as provider in the staff view; Providers-list absence check pending).
- 2026-09-17: Recorded that the Reactivate action works from both the team list and the member detail page; PR-01-011 stays open pending a fresh-login confirmation after reactivation.
- 2026-09-17: Closed the Team Management pass — PR-01-011 marked `Resolved - verified 2026-09-17 (HAIRL-1309)` after fresh login succeeded post-reactivation; PR-01-006 (HAIRL-1304) and PR-01-005 (HAIRL-1303) marked `Resolved - verified 2026-09-17` (context menu shows Suspend/Remove/View Details; invite placeholder spelled correctly); attached the Admin staff-list evidence URL to A-02-009 and PR-01-019.
