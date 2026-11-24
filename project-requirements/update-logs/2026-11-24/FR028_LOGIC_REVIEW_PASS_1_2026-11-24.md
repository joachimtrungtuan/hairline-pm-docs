# FR-028 Logic Review Pass 1 (2026-11-24)

**Scope**: FR-028 Regional Configuration & Pricing, PRD change-log row 1.61 (the PRD carries no Version line). Pass 1 of the logic review; 26 findings: 1 partly rejected (P1-17), 2 owned by neighbour FRs and only queued (P1-22, P1-23), the rest fixed on the FR-028 side (P1-03, -05, -09, -20, -21 also queue neighbour rows).
**Evidence**: reviewer report `plans/reports/tester-261124-fr028-logic-p1.md`; fixer report `plans/reports/docs-manager-261124-fr028-logic-p1-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr028-logic-p1-fixes.yaml` is prepared and NOT applied (the controller applies it).
**Owner defaults**: numbers 120 to 130 as ruled by the controller for this pass (patient currency and approx. marking; display cap with Show all destinations; Manage App Data permission; inactive equals archived and releases countries; 51st-grouping warning; FR-026 active-country destinations; profile country as the matching key; fixed distance table; on-screen save confirmation; Stripe-assigned grouping blocked; deactivated country keeps applying); the owner-review defaults report is the controller's to update.

## Changes to the PRD

- One price lookup chain, stated once in REQ-028-040: patient currency, then the fallback for the patient's country, then the system-wide default, then the location default currency converted, then "Price available on request" with an error logged for admin review. A converted price is marked approx. Other places point to the chain.
- The destination cap only sets how many destinations show first (default 10, 5 to 20, a field of the grouping); the rest sit behind "Show all destinations". The earlier setting for it is retired.
- The grouping is matched on the profile country; no IP geolocation. Proximity ordering uses a fixed distance table in the product code.
- Permission is the FR-031 "Manage App Data" for groupings and starting prices.
- Inactive and archived are one state that releases countries; the country check counts active groupings only; switching back to Active re-runs the check (new flow A7). The 51st grouping warns and may continue.
- A destination is an FR-026 active country, the same key as treatment countries in an inquiry. A deactivated country keeps applying until an Admin edits it (REQ-028-092).
- A grouping with an assigned Stripe account cannot be archived or lose a country (REQ-028-091); FR-029 is a consumer in Dependencies.
- New flows for effective and expiry dates, location default currency (A8, same on every row of a location), system-wide default price (A9) and the preview screen; preview currency defaults to the FR-029 system default currency.
- Dated rows: a future change is a new row, the lookup picks the row whose window contains today, dates are UTC with the expiry day included, history comes from the audit log (REQ-028-090, -063).
- Audit and cache clear on every save step; checks on amount, decimals (FR-029 minor units) and currency on fallback, bulk and system-wide prices; a bulk apply that would break them is blocked.
- The stale-edit warning covers groupings, price rows and the bulk apply; the "last save wins" wording is gone.
- Save confirmation is the on-screen message only; expiry and missing-price warnings are banners on Screen 2. The audit rules REQ-028-011 and REQ-028-014 are merged.

## Graph change-set (prepared, not applied)

- 249 operations: 26 nodes added (3 rules, 4 flows, 19 steps), 1 field added, 12 edges removed, 44 node updates (33 rules, 6 steps), 2 field type updates, 1 node retired (the display-cap setting), 1 merge (REQ-028-011 into REQ-028-014), 162 edges added.
- Wiring: the next edges into retired STP-028-008 and -209 are removed (the live bypass edges already existed); new steps STP-028-213, -428 and -429 are inserted in the price flow, A6 and the patient flow; four flows start at STP-028-151, -501, -511 and -521. SCR-028-01, -02, -03 and the save event move to STG-admin-01-configuration. Two cross-FR edges: REQ-028-038 governed by SET-default-currency, and REQ-028-055 applies to ENT-currency.minor_units; also REQ-028-003 to ENT-patient.country and REQ-028-086 to ENT-inquiry.treatment_countries.
- Applied to a scratch copy of the db (421 change rows, no error), then the copy was deleted. Every active FR-028 step has an incoming next or flow start. lint.py was not run (the controller lints after applying).

## Files touched

- `local-docs/project-requirements/functional-requirements/fr028-regional-config-pricing/prd.md`
- `local-docs/project-requirements/graph/changesets/2026-11-24-fr028-logic-p1-fixes.yaml`
- this log and `update-logs/README.md`

## Cross-FR rows queued

FR-003 (display cap on Screen 2; description, provider count, range indicator, ordering note and a link from STP-003-003), FR-031 (Manage App Data row mentions starting prices), FR-001 (country line mentions regional presentation), FR-029 (Stripe assignment block), FR-026 (deactivation warning lists groupings and fallback prices), FR-038 (Treating Country should name the FR-026 active country list). The rows are in the logic-review ledger section for FR-028 pass 1.
