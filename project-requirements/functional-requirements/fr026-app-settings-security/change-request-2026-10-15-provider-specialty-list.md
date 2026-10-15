# Change Request: Centrally Managed Provider Specialties List

**Change Request ID**: CR-FR026-20261015-01
**Primary FR**: FR-026
**Triggering FR / Event**: FR-015 fifth verification pass (2026-10-15) found that the required "Specialty" select in FR-015 Screen 2 Step 2 (provider creation wizard) and Screen 3 Tab 1 (provider profile editing) listed open-ended values ("Hair Transplant, Dermatology, etc.") with no owner, seed list, or rule for changing them
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.10 to v1.11
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-015 required a provider Specialty but did not say where its values come from or who can change them. The Product Owner chose to make the specialty values a centrally managed App Data list in FR-026, following the same pattern as the existing country and reason lists.

The new list is **Provider Specialties** (Settings → App Data → Provider Specialties, FR-026 Screen 5f). Admins can add, rename, reorder, and deactivate values; there is no hard delete. FR-015 shows only active values for selection, while providers that already hold a deactivated value keep it and still display it.

## Baseline State

**Source version**: FR-026 v1.10, Module Scope, Alternative Flows A1 to A8, Screens 5 to 5e, Admin Editability Rules, REQ-026-012 to REQ-026-012g

- FR-026 had no provider specialty list; FR-015 Specialty values were described only as "Hair Transplant, Dermatology, etc."
- No seed values, uniqueness rule, deactivation behavior, or audit requirement existed for specialty values.
- Admin A-02 (FR-015) was not listed as a consumer of FR-026 App Data.

## Approved State

**Target version**: [FR-026 v1.11](prd.md), Module Scope (Admin Platform A-02), Alternative Flow A9, Screen 1 App Data setting groups, Screen 5f: Provider Specialties Manager, Admin Editability Rules, Downstream Consumers, Initial Configuration / Seeding, REQ-026-012h, Entity 7a

- Fields: specialty name (max 100 chars, unique case-insensitive), display order, active status; providers reference a stable specialty ID.
- Seed values, in order: Hair Transplant Surgeon, Dermatologist, Trichologist, Plastic Surgeon, Other.
- Admins can add, rename, reorder, and deactivate values; hard delete is not supported. At least one value must remain active.
- Deactivated values disappear from FR-015 selection; existing providers keep the stored value and it still displays.
- Renames apply to the display everywhere, including existing provider profiles.
- Every change requires a change reason, is versioned, audit-logged, and propagates to FR-015 within 1 minute.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| List ownership | No owner; values implied in FR-015 | FR-026 Provider Specialties list (Screen 5f) | One auditable source, consistent with other managed lists |
| Seed values | "Hair Transplant, Dermatology, etc." | Hair Transplant Surgeon, Dermatologist, Trichologist, Plastic Surgeon, Other | Product Owner decision |
| Admin actions | Undefined | Add, rename, reorder, deactivate; no hard delete; at least one active value | Keep historical provider references valid |
| Deactivated values | Undefined | Hidden from new selection; kept and displayed on existing providers | Avoid data loss on existing provider records |
| Renames | Undefined | Apply to display everywhere through the stable specialty ID | Keep one current name per value |
| Consumers | A-02 not listed | Admin A-02 (FR-015 Screen 2 Step 2, Screen 3 Tab 1) added to Module Scope and Downstream Consumers | Traceability |
| Requirements | REQ-026-012 to 012g | Added REQ-026-012h and Entity 7a | Make the rules testable |

## Scope and Impact

### In Scope

- FR-026 Module Scope, workflow A9, Screen 1 setting groups, Screen 5f, Admin Editability Rules, Downstream Consumers, seeding, REQ-026-012h, Entity 7a, and the PRD change log row.
- This FR-local Change Request.

### Out of Scope

- FR-015 PRD edits (handled in the FR-015 v1.13 fifth verification fixes).
- Provider-facing display of specialty in patient or provider apps.
- Multiple specialties per provider.
- System PRD, technical specification, and data schema updates.
- Source code, API, or live configuration changes.

### Affected Contracts

- **PRD owner**: [FR-026](prd.md) — Screen 5f, workflow A9, REQ-026-012h, Entity 7a.
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) v1.13 Screen 2 Step 2 and Screen 3 Tab 1 Specialty select consume the active list.
- **System documents**: None updated in this change; data schema alignment for a provider specialty reference is to be assessed.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code or runtime behavior was inspected or changed.
- **Required assessment**: Storage of the Provider Specialties list and provider-to-specialty reference, Settings → App Data admin screen, versioning and audit logging, FR-015 Specialty select data source and display of deactivated values.
- **Compatibility / rollout risk**: Existing providers may hold free-text or hardcoded specialty values that do not match the seed list; these must be mapped to list values (or to "Other") before the reference is enforced.
- **Data migration**: To be assessed. Map existing provider specialty values to seeded list IDs without losing the displayed value.

## Acceptance and Validation

- Settings → App Data → Provider Specialties shows the five seed values in order on a new environment.
- Adding a name that matches an existing one ignoring case is rejected; names over 100 characters are rejected.
- Deactivating the last active value is blocked; there is no delete action.
- After deactivating "Trichologist", FR-015 Screen 2 Step 2 no longer offers it, while a provider already set to "Trichologist" still shows it in Screen 3 Tab 1.
- Renaming "Dermatologist" changes the displayed name on existing provider profiles within 1 minute.
- Each add, rename, reorder, and deactivation requires a change reason and appears in version history and the audit log with old and new values.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan, during FR-015 fifth verification review.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-15; FR-026 documentation delta only.
- **Decision evidence**: FR-015 fifth verification pass decision (2026-10-15) to move the Specialty values into a centrally managed FR-026 App Data list.
- **PRD change log**: [FR-026 Appendix: Change Log](prd.md#appendix-change-log), v1.11 dated 2026-10-15.
- **Update log**: [FR015_FIFTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_FIFTH_VERIFICATION_FIXES_2026-10-15.md).
- **Supersedes**: None.
- **Superseded by**: None.
