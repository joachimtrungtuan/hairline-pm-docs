# Change Request: Provider Commission & Payout Panel and Account-Status Banner

**Change Request ID**: CR-FR032-20261015-01
**Primary FR**: FR-032
**Triggering FR / Event**: FR-015 v1.11 (third verification pass, Issues 1 and 4)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.5 to v1.6
**Related Commit(s)**: Pending

---

## Decision Summary

FR-015 promises that providers can see their commission rate and payout frequency read-only, and that suspended providers see an "Account Suspended" banner on the Provider Platform. FR-032, the verified Provider Platform settings FR, specified neither. The Product Owner approved adding both to FR-032 so the promise has an owning screen and rule.

## Baseline State

**Source version**: FR-032 v1.5 — Screen 4: Billing Settings; General Module Rules (Rules 1–5)

Screen 4 showed bank account details only. No FR-032 rule described provider-side behavior for Suspended or Deactivated accounts.

## Approved State

**Target version**: FR-032 v1.6 — Screen 4: Billing Settings (Commission & Payout read-only panel); General Module Rules, Rule 6; REQ-032-029 and REQ-032-030

See the [FR-032 PRD](prd.md) for the full contract.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Screen 4 Billing Settings | Bank details only | Adds a read-only Commission & Payout panel (model, value, Flat Rate Currency, Effective Date, scheduled configuration, payout frequency) sourced from FR-015 Tab 7 / FR-029 | FR-015 promised a provider-side read-only view with no owning screen |
| Account status behavior | Not specified | Rule 6: Suspended shows a persistent banner with the admin reason to the Owner and all FR-009 team members, with view-only restrictions and listed exceptions; Deactivated blocks login with a message; Reactivated removes the banner | FR-015 Screen 4 referenced a banner that no Provider Platform FR owned |
| Requirements | REQ-032-001 to REQ-032-028 | Adds REQ-032-029 and REQ-032-030 | Testable acceptance for the new panel and rule |
| Dependencies | No FR-015 entry | FR-015 internal dependency for commission data and provider status | Traceability |

## Scope and Impact

### In Scope

- Read-only provider display of commission and payout configuration
- Provider-side banner and access behavior for Suspended, Deactivated, and Reactivated accounts

### Out of Scope

- Provider editing of commission or payout settings (admin-only in FR-015 Tab 7)
- Changes to the FR-015 suspension cascade or FR-029 commission calculation

### Affected Contracts

- **PRD owner**: `functional-requirements/fr032-provider-dashboard-settings/prd.md` — Screen 4, Rule 6, REQ-032-029, REQ-032-030
- **Related FRs**: FR-015 v1.11 (Tab 7, Screens 4–5, Rule 9), FR-029 (provider commission configuration), FR-009 (team members)
- **System documents**: None

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Provider Platform billing settings UI, provider commission read API, provider status checks at login and per page, banner component, permission gating for team members
- **Compatibility / rollout risk**: Low; additive read-only panel. The banner must use the same status source as the FR-015 cascade to avoid showing Active while cascades run
- **Data migration**: None

## Acceptance and Validation

- A provider Owner sees the panel in Screen 4 with values matching FR-015 Tab 7, and cannot edit them
- A suspended provider's Owner and team members see the banner with the admin reason on every page, and quote submission and acceptance are blocked
- A deactivated provider cannot log in and sees the deactivation message
- Implementation evidence for both behaviors is required before marking reconciliation Verified

## Approval and Traceability

- **Requested by**: verify-fr pass on FR-015 v1.10
- **Approved by**: Product Owner (Joachim Trung Tuan), 2026-10-15
- **Decision evidence**: AskUserQuestion decisions and "Yes" approval in the FR-015 verification session
- **PRD change log**: FR-032 v1.6 row (2026-10-15); FR-015 v1.11 row
- **Update log**: [FR015_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_VERIFICATION_FIXES_2026-10-15.md)
- **Supersedes**: None
- **Superseded by**: None
