# FR-028 Logic Review Pass 2 (2026-11-24)

**Scope**: FR-028 Regional Configuration & Pricing, PRD change-log row 1.62 (the PRD carries no Version line). Final pass of the logic review; 11 findings (P2-01 to P2-11), all fixed on the FR-028 side, plus five minor observations. Neighbour FRs are only queued.
**Evidence**: reviewer report `plans/reports/tester-261124-fr028-logic-p2.md`; fixer report `plans/reports/docs-manager-261124-fr028-logic-p2-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr028-logic-p2-fixes.yaml` is prepared and NOT applied (the controller applies it).
**Owner defaults**: numbers 153 to 156 as ruled by the controller for this pass (read-only Change history panel; Screen 3 simulates saved configuration only; price rows do not overlap with a stated tie-break; country deactivated in FR-026 replaces the provider-location warning); the owner-review defaults report is the controller's to update.

## Changes to the PRD

- Setting a grouping Inactive is blocked while a Stripe account is assigned, like archiving it or removing a country (REQ-028-091); reactivation also checks the unique grouping name.
- A price lookup step that cannot show a price passes to the next step; "Price available on request" shows only when the last step also fails (REQ-028-040, -041). The fallback tie-break is the destination default currency, then the FR-029 system default currency, then the earliest created.
- Price rows for the same destination and currency (and patient country on a fallback row) may not overlap in dates: a new dated row ends the previous open row the day before; bulk apply changes the row current today (REQ-028-090).
- The deactivated-country rule covers groupings and starting prices (destination and fallback rows); the active check runs only when a country is newly selected (REQ-028-092, -086). The provider-location edge case becomes "country deactivated in FR-026" (REQ-028-083); every active FR-026 country is listed, with provider count 0 where there is none.
- The expiry and missing-price banners are shown when the pricing tab opens.
- A read-only Change history panel on Screens 1 and 2 (one new step each); the link to the FR-031 audit screen is dropped.
- Screen 3 simulates saved configuration only; unsaved edits are previewed on Screen 1 (pane) and Screen 2 (formatted amount); user story 5 rewritten.
- The destination default currency and the system-wide default price get a stored home (new entity, see below); the audit log gains two entity types.
- Patient currency is the profile preference, else the FR-029 system default currency.
- Minor: user story 3 independent test wording; error text for Locations Displayed outside 5 to 20; only active groupings count toward the 51st-grouping warning; the save event description covers every configuration save.

## Graph change-set (prepared, not applied)

- 211 operations: 3 nodes added (1 entity, 2 steps), 5 fields added, 66 edges removed, 22 node updates, 1 node retired (the old default currency field on the price row), 4 enum values added, 110 edges added.
- New entity ENT-pricing-default (one record per destination default currency, one system-wide record); enum values location_default_currency and system_default_price on the audit log entity type and on the new default_type field.
- Admin-side rules move to STG-admin-01-configuration: 62 rules moved, 5 rules applied by both admin and patient steps keep the inquiry edge and gain the admin edge.
- Cross-FR edges: REQ-028-038 applies to ENT-patient.preferred_currency (FR-001 field, added); the FR-028 edge REQ-028-014 applies to SCR-031-05 (FR-031 screen) removed.
- Applied to a scratch copy of the db (273 change rows, no error), then the copy was deleted. lint.py was not run (the controller lints after applying).

## Files touched

- `local-docs/project-requirements/functional-requirements/fr028-regional-config-pricing/prd.md`
- `local-docs/project-requirements/graph/changesets/2026-11-24-fr028-logic-p2-fixes.yaml`
- this log and `update-logs/README.md`

## Cross-FR rows queued

FR-003 (REQ-003-033 "with fallback currency" wording; every active country listed with provider count 0), FR-029 (Stripe block now covers Inactive; system default currency as patient fallback), FR-026 (deactivation warning lists groupings and starting prices), FR-031 (no audit-log screen link from FR-028), FR-001 (profile currency preference read by FR-028). The rows are in the logic-review ledger section for FR-028 pass 2.
