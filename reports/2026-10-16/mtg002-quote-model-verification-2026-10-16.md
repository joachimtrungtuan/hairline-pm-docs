# MTG-002 Quote/Subquote Data-Model Verification Report

| Field | Value |
|---|---|
| Date | 2026-10-16 (Asia/Saigon) |
| Source | SRC-MTG-002, `local-docs/project-requirements/sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md`, including the PO clarifications of 2026-09-09, 2026-09-15 and 2026-09-16 |
| Scope | Quote/subquote data model only: parent quote, Quote Option, option/date-price record, subquote, AcceptanceEvent and snapshot, slot hold, booking handoff, `Payment Window Expired` (PWE) |
| Out of scope | Payment, fund release and Meeting 03 (see section 8) |
| Documents | FR-004, 005, 006, 007, 007b, 008, 010, 014, 015, 017, 019, 020, 022, 024, 026, 029, 030; `system-prd.md`, `system-data-schema.md`, `system-technical-spec.md` |
| Status | Read-only audit. No PRD, CR or system document was edited |

`frNNN:line` means that FR's `prd.md` at that line. Locations are the verifiers' corrected ones.

## 1. Executive summary

The core MTG-002 model is in place. FR-004, 005, 006, 007, 008, 014 and 017 consistently describe a parent quote with 1–5 Quote Options, the subquote as the single accepted unit, and an immutable AcceptanceEvent snapshot that bookings, payments and invoices read. The model is not yet safe to build end to end. After verification and de-duplication the audit holds **4 Critical, 45 Major, 87 Minor and 24 Observation** findings; 66 of the Minors and all Observations are unverified first-pass findings.

The most serious problems are these:

1. FR-010 reads the live quote instead of the snapshot, and FR-019 lets promotions change the price after acceptance.
2. FR-024 still models one treatment plus summed add-on packages, not 1–5 alternative options, and its packages have no items to copy.
3. PWE has no stated recovery route, and FR-006 contradicts itself on when the hold starts.
4. Provider withdrawal after acceptance is undefined, and admins can soft-delete acceptances or revive expired bookings.
5. The schema has no AcceptanceEvent, Booking, hold or quote-version storage.

Twenty-four PO decisions are needed; about 20 of the 49 Critical/Major fixes can start without one.

## 2. Method

Seventeen FRs were audited individually, plus five seam audits: S1 commercial chain, S2 configuration/catalogue, S3 downstream consumers, S4 events and S5 system documents. One shared brief set the baseline and severity scale. The tools were a traceability matrix, state-transition probes, a data-ownership check, an event producer/consumer check and evidence-quoted findings. Seven reviewers (V1, V2, V3, V4a, V4b, V5, V6) then adversarially re-checked all 108 Critical/Major findings, confirming, revising, rejecting, parking or merging each. Their verdicts override first-pass severity. Minor and Observation findings were not re-checked.

## 3. Requirements traceability matrix

| Baseline point | Main FR locations | Status | Blocking finding IDs |
|---|---|---|---|
| D03 one assessment, one quote with option-level records | FR-004 Key Entities, REQ-004-014; FR-005 Screen 1; FR-014; FR-015 | Partial | FR-030-3 |
| D03 refinement: multi-parent, 1–5 options, treatment once | fr004:578-581, REQ-004-015; REQ-005-001/018; REQ-024-010/011 | Partial | FR-024-2, FR-024-5, FR-024-6 |
| D04 presets seed options; local edits; no save-for-future | fr004:582-583, REQ-004-016/017; FR-024 Screen 5, Entity 3 | Partial | FR-024-1, FR-024-8 |
| D05 price per date range × package; shared facts on parent | FR-004 Tab 4, REQ-004-018/020; FR-024 Entity 4 | Partial | FR-024-5 |
| D06 option comparison; parent vs option analytics | REQ-004-030; REQ-005-013/020; fr014:1422-1431 | Partial (complied in FR-014) | FR-024-6, FR-014-2 |
| O01 ownership matrix and currency snapshot | fr004:196-249, REQ-004-024/025; FR-026 Screen 5d; FR-029 Screen 6 | Partial | FR-004-5, FR-019-1, FR-024-3, S2-4, FR-026-2, FR-026-3, FR-026-4, FR-007b-2, S5-5 |
| FR-005 subquote atomic acceptance | fr005:298, A2, A5, REQ-005-018/019; REQ-004-022 | Partial | FR-005-4, FR-019-3, S5-1 |
| FR-006 handoff, no reselection | REQ-006-001/007; REQ-007-016–019; REQ-008-026; FR-017 Entity 1 | Partial (contradicted in FR-010 and FR-019) | FR-010-1, FR-019-2, FR-010-3, FR-010-4, FR-010-6, FR-006-3, FR-017-1, S4-5, S5-2 |
| FR-006 slot hold | fr005:339; fr006:686 vs fr006:116, 661, 902; FR-006 Entity 2 | Partial | S1-2, S2-5, S1-6, S5-3, S5-4 |
| FR-006 Payment Window Expired | fr006:118-120, 687, 693; REQ-007-017; REQ-014-109 | Partial | S1-1, S1-3, FR-006-3, FR-019-4, S4-2, FR-022-3, S5-3 |
| D07 locale-safe dates (record only) | fr006:216, 646; fr010:265 | Complied | None (Observations FR-029-8, FR-006-10) |

## 4. Cross-cutting themes

### 4.1 Changes after acceptance (Critical)
FR-010 keys treatment records to the live Quote Option (fr010:587, 619, 876) while FR-004 Screen 7 still allows edits. FR-019 lets providers swap promotions "until the booking is confirmed" (fr019:609) and patients enter codes at checkout with recalculation (fr019:613, 635-636). Before acceptance FR-004 stores only a live `promotionId` (fr004:673), so promotion edits change displayed prices without a version bump.
- **Affected:** FR-010, FR-019, FR-004, FR-005, FR-006, FR-017.
- **Findings:** FR-010-1 C (merged S3-1, FR-010-5); FR-019-2 C (merged S2-1, FR-019-8, FR-017-3); FR-019-1 C; FR-004-5 M (merged FR-005-6, S2-3, FR-019-5).
- **Fix owner:** FR-010, FR-019, FR-004. **PO decision:** yes for FR-019 and FR-004-5 (decisions 8–10); FR-010-1 is a pure edit.

### 4.2 FR-024 package model (Critical)
REQ-024-010/011 and US4 describe one treatment plus summed packages (fr024:846-847, 915), contradicting FR-004's 1–5 alternative options (fr004:570). Packages hold only a markdown description (fr024:958), so FR-004 has no items to copy. The schema `packages` table has no version although `source_package_version` is NOT NULL. QuoteTreatment is still current, Usage Count reads `quote_packages`, and providers can set package currency.
- **Findings:** FR-024-2 C; FR-024-1 M (from Critical); FR-024-3, FR-024-5, FR-024-6 (merged S2-8), FR-024-8 M.
- **Fix owner:** FR-024 and the schema. **PO decision:** yes (17, 18).

### 4.3 PWE recovery (Major)
FR-006 requires "a new current subquote or an audited admin intervention" (fr006:118, 120, 693), but FR-005 Rule 1 allows one acceptance per inquiry (fr005:298). A workaround exists (cancel the inquiry via FR-003 and start a new one per FR-005 A4), but no FR states it, the post-expiry states, or what admin intervention may do. FR-019 never releases usage limits on PWE.
- **Findings:** S1-1 M from Critical (merged FR-004-2, FR-005-1, FR-006-1, FR-014-5); FR-019-4 M.
- **Fix owner:** FR-006, with FR-005 and FR-004. **PO decision:** yes (1, 2).

### 4.4 Hold start, duration owner, slot identity (Major)
fr006:686 and fr005:339 start the hold at acceptance, but fr006:116, 661 and 902 run it "after payment failure"; FR-007 forbids extension (fr007:148). Duration points to setting "A-09", which neither FR-026 nor FR-029 defines. Nobody creates the Calendar Slot, and FR-004 gives only a start time (fr004:335).
- **Findings:** S1-2 M (merged FR-005-3, FR-006-2, FR-007-1); S2-5 M (merged FR-026-1); S1-6 M.
- **Fix owner:** FR-006; FR-026 or FR-029 for duration. **PO decision:** only the duration owner (14). MTG-002 2026-09-16 already fixes the start at acceptance.

### 4.5 Provider withdrawal after acceptance (Major)
FR-004 Workflow 6 moves `accepted` to `withdrawn` and re-routes to another provider (fr004:168-172). FR-006 never mentions withdrawal, and FR-005 A3 covers only pre-acceptance. Hold, booking status, AcceptanceEvent and re-routing are undefined, and re-routing conflicts with the immutable snapshot.
- **Findings:** S1-3 M (merged FR-004-3, FR-005-5, FR-006-4); event side S4-1.
- **Fix owner:** FR-006 (new flow modelled on B4). **PO decision:** yes (3).

### 4.6 Admin powers after acceptance (Major)
FR-005 allows admin soft-delete/restore of acceptances and undefined "Resolve conflicts" (fr005:290, 318-319). FR-006 allows Modify Status and Modify Appointment Date "Always" (fr006:608-609), so PWE can be reversed without a slot check. FR-010 permits treatment overrides and provider reassignment (fr010:453-458, 470, 490).
- **Findings:** FR-005-4 M (merged S1-8); FR-006-3 M; FR-010-4 M; FR-004-4 m.
- **Fix owner:** each FR. **PO decision:** yes (2, 4, 6).

### 4.7 Commission timing, base and field (Major)
FR-029 and FR-015 snapshot commission at confirmation (REQ-029-045). FR-004 shows a rate-only quote field (fr004:218, 384), FR-006 says commissions are "already resolved before booking stage" (fr006:785), FR-029 Rule 1 says quotes keep original configuration (fr029:727), and the "booking total" base is undefined (fr029:660, 677, 783, 787).
- **Findings:** S2-4 M from Critical (merged FR-029-3, S3-5, FR-017-2); FR-029-1 M; FR-029-2 M.
- **Fix owner:** FR-029, FR-004, FR-006. **PO decision:** yes (12, 13).

### 4.8 Notification events and recipients (Major)
FR-030, mirrored by FR-020, has no withdrawal or PWE event, lets admins disable `quote.accepted`, defines no recipient grain or same-provider outcome, sends nothing for competing drafts, does not require snapshot-sourced variables, and uses a single `quote.total_amount`.
- **Findings:** S4-1 (merged FR-030-2), S4-2 (merged FR-030-1, FR-020-3), S4-3 (merged FR-020-8), S4-5 (merged FR-030-4), FR-020-1 (merged S4-4, FR-030-6), FR-020-2, FR-020-4, FR-030-3, all M.
- **Fix owner:** FR-030 with FR-020; FR-004 for drafts. **PO decision:** yes (5, 20–22).

### 4.9 Stale status lists (Major)
The FR-022 bookings filter uses non-FR-006 states (fr022:962), and its quote filters omit `cancelled_provider_status` (fr022:626, 913) although FR-022 is Verified. FR-014 B3 counts bookings without a status filter (fr014:197, 1782).
- **Findings:** FR-022-3 (merged S3-2), FR-022-2 (merged S3-3), FR-014-2, all M.
- **Fix owner:** FR-022, FR-014. **PO decision:** no.

### 4.10 System schema gaps and enum conflicts (Major)
The schema lacks AcceptanceEvent, snapshot, Booking, hold and version storage and the `accepted → cancelled_inquiry_cancelled` transition. Quote statuses conflict (`confirmed`, `rejected`). The tech spec calls the appointment confirmed at acceptance (tech-spec:148) and reads deprecated fields (tech-spec:165-174). The FR-005/006 CRs deferred reconciliation, but it blocks Verified status.
- **Findings:** S5-1, S5-2 (both from Critical), S5-3, S5-4, S5-5, S5-6, FR-024-8, FR-026-4, all M.
- **Fix owner:** schema and tech spec. **PO decision:** yes (23, 24).

### 4.11 Promotion redemption lifecycle (Major)
FR-019 Applications have no creation trigger or AcceptanceEvent link (fr019:853-854), are never voided on Not Selected or PWE, and usage limits have no consume/release rule (fr019:676). CR acceptance items have no PRD criteria.
- **Findings:** FR-019-3 (merged S2-2), FR-019-4, FR-019-7, all M.
- **Fix owner:** FR-019. **PO decision:** yes (11).

### 4.12 Remaining Major themes
- **FR-007b alignment.** The total comes through the booking (fr007b:90) but is called "accepted quote" (fr007b:193, 582-584), and the plan has no currency snapshot or promotion basis. FR-007b-2 M (merged FR-007b-4, S1-7). Owner FR-007b. No PO decision.
- **FR-026 settings and draft expiry.** Expiry and currency are captured "when a new parent Quote is created" (fr026:255, 867; fr004:338), so drafts are ambiguous. No Quote Configuration is seeded, and the schema keeps a customizable `expiration_hours`. FR-026-2 (merged S2-7), FR-026-3, FR-026-4, all M. Owners FR-004, FR-026 and the schema. Decisions 15 and 16.
- **FX review at acceptance.** FR-017 flags acceptance for manual review if the rate is over 24 hours old (fr017:1709-1715); FR-005 has no such outcome. FR-017-1 M. Owner FR-005. Decision 19.
- **FR-008 travel review exit.** `travel-date-review-required` has no exit (fr008:774, 1025). FR-008-2 M. Decision 7.
- **Testability.** FR-010-6, FR-019-7 and FR-020-4 (all M) lack scenarios. Each FR owns its fix. No PO decision.

### 4.13 Stale CR "open" claims (Minor)
CR-0909 still says reconciliation is open, and CR system-document status lines are stale. FR-004-8, FR-004-9, S5-12, FR-010-7 (m); FR-005-13, FR-020-9, FR-022-9 (O). All unverified. No PO decision.

## 5. Findings register

These tables list kept findings only. Merged IDs are named in the verdict column of the finding that absorbed them. C = Critical, M = Major, m = Minor.

### FR-004
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-004-5 | M | Live promotion reference; gross/net undefined | FR-004, FR-019 | CONFIRMED-REVISED; absorbs FR-005-6, S2-3, FR-019-5 |
| FR-004-1 | m | Expiry not scoped away from `accepted` | FR-004 | Revised M to m; absorbs S1-12 |
| FR-004-4 | m | Screen 7 lacks post-acceptance guard | FR-004 | Revised M to m |
| FR-004-6 | m | Screen 4 label drift | FR-004 | Revised M to m |
| FR-004-7 | m | No future-appointment or zero-price rule | FR-004 | Revised M to m |

### FR-005
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-005-4 | M | Admin soft-delete/restore of acceptance | FR-005 | CONFIRMED; absorbs S1-8 |

### FR-006
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-006-3 | M | Admin Modify Status/Date "Always" | FR-006 | CONFIRMED |
| FR-006-5 | m | B3 "no booking created" stale | FR-006 | Revised M to m; absorbs S1-11 |

### FR-007 and FR-007b
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-007b-2 | M | No currency snapshot or promotion basis on plan | FR-007b | CONFIRMED-REVISED; absorbs FR-007b-4, S1-7 |
| FR-007b-1 | m | "Accepted quote" vocabulary | FR-007b | Revised M to m |
| FR-007b-3 | m | Retry rule lacks FR-007 hold cross-reference | FR-007b | Revised M to m |

FR-007-1 merged into S1-2; FR-007-2 was parked.

### FR-008
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-008-2 | M | Travel-date review has no exit | FR-008 | CONFIRMED |
| FR-008-1 | m | Appointment-window anchor undefined | FR-008 | Revised M to m |
| FR-008-3 | m | Closed TravelContext not guarded | FR-008 | Revised M to m |

### FR-010
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-010-1 | C | Reads live FR-004 records, not snapshot | FR-010 | CONFIRMED; absorbs S3-1, FR-010-5 |
| FR-010-3 | M | No day-to-date derivation | FR-010 | CONFIRMED |
| FR-010-4 | M | Unbounded admin overrides and reassignment | FR-010 | CONFIRMED |
| FR-010-6 | M | No handoff scenarios | FR-010 | CONFIRMED |
| FR-010-2 | m | Identifier lists disagree (587 vs 876) | FR-010 | Revised M to m |

### FR-014, FR-015 and FR-017
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-014-2 | M | `bookings_on_day` has no status filter | FR-014 | CONFIRMED-REVISED (narrowed) |
| FR-017-1 | M | Acceptance-time FX review state | FR-005, FR-017 | CONFIRMED |
| FR-015-1 | m | "Transaction Amount" commission wording | FR-015 | Revised M to m |

FR-014-1 was rejected (Appendix A). FR-017-2 merged into S2-4, and FR-017-3 into FR-019-2.

### FR-019
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-019-1 | C | Patient code writes provider-owned promotion | FR-019, FR-004, FR-005 | CONFIRMED |
| FR-019-2 | C | Post-acceptance price changes | FR-019 | CONFIRMED; absorbs FR-019-8, S2-1, FR-017-3 |
| FR-019-3 | M | Application trigger and acceptance link | FR-019 | CONFIRMED; absorbs S2-2 |
| FR-019-4 | M | Usage-limit consume/release | FR-019 | CONFIRMED |
| FR-019-7 | M | CR items lack PRD criteria; auto-apply target | FR-019 | CONFIRMED |
| FR-019-6 | m | Fixed discounts lack currency | FR-019 | Revised M to m |

### FR-020 and FR-030
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-020-1 | M | Recipient grain and same-provider matrix | FR-020, FR-030 | CONFIRMED; absorbs S4-4 |
| FR-020-2 | M | Draft parents on acceptance | FR-004, FR-020 | CONFIRMED-REVISED owner |
| FR-020-4 | M | No acceptance-outcome scenarios | FR-020, FR-005 | CONFIRMED |
| FR-030-3 | M | Single `quote.total_amount` | FR-030 | CONFIRMED |

FR-020-3 merged into S4-2 and S4-1; FR-030-1, FR-030-2 and FR-030-4 merged into S4-2, S4-1 and S4-5.

### FR-022
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-022-2 | M | Filters omit `cancelled_provider_status` | FR-022 | CONFIRMED; absorbs S3-3 |
| FR-022-3 | M | Bookings filter uses non-FR-006 states (fr022:962) | FR-022 | CONFIRMED-REVISED location; absorbs S3-2 |
| FR-022-1 | m | Sort basis not named | FR-022 | Revised M to m |

### FR-024
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-024-2 | C | Additive packages vs alternative options | FR-024 | CONFIRMED |
| FR-024-1 | M | No package item structure | FR-024 | Revised C to M |
| FR-024-3 | M | Provider-chosen currency | FR-024 | CONFIRMED |
| FR-024-5 | M | QuoteTreatment still current | FR-024 | CONFIRMED |
| FR-024-6 | M | Usage Count deprecated link and statuses | FR-024 | CONFIRMED; absorbs S2-8 |
| FR-024-8 | M | Schema `packages` unversioned | Schema | CONFIRMED |
| FR-024-4 | m | Pinned-version resolution unstated | FR-024 | Revised M to m |
| FR-024-7 | m | "Active" check point ambiguous | FR-004 | Revised M to m |

### FR-026 and FR-029
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| FR-026-2 | M | Draft expiry/currency capture point | FR-004, FR-026 | CONFIRMED-REVISED owner; absorbs S2-7 |
| FR-026-3 | M | Quote Configuration not seeded | FR-026 | CONFIRMED |
| FR-026-4 | M | Customizable `expiration_hours` in schema | Schema | CONFIRMED |
| FR-029-1 | M | Rule 1 vs confirmation-time resolution | FR-029 | CONFIRMED |
| FR-029-2 | M | "Booking total" undefined | FR-029 | CONFIRMED |
| FR-029-4 | m | PRD lacks commission user story | FR-029 | Revised M to m |

FR-026-1 merged into S2-5, and FR-029-3 into S2-4.

### Seams S1–S5
| ID | Final severity | Title | Fix owner | Verification verdict |
|---|---|---|---|---|
| S1-1 | M | PWE recovery undefined | FR-006 | Revised C to M; absorbs FR-004-2, FR-005-1, FR-006-1 |
| S1-2 | M | Hold start contradiction | FR-006 | CONFIRMED; absorbs FR-005-3, FR-006-2, FR-007-1 |
| S1-3 | M | Withdrawal after acceptance | FR-006 | CONFIRMED; absorbs FR-004-3, FR-005-5, FR-006-4 |
| S1-6 | M | No slot producer | FR-006, FR-004 | CONFIRMED-REVISED |
| S2-4 | M | Commission fixing point inconsistent | FR-004, FR-006 | Revised C to M; absorbs FR-029-3, S3-5, FR-017-2 |
| S2-5 | M | Hold duration has no owner | FR-026 or FR-029 | CONFIRMED; absorbs FR-026-1 |
| S4-1 | M | No `quote.withdrawn` event | FR-030 | CONFIRMED; absorbs FR-030-2 |
| S4-2 | M | No PWE event | FR-030 | CONFIRMED; absorbs FR-030-1, FR-020-3 |
| S4-3 | M | `quote.accepted` not locked | FR-030 | CONFIRMED |
| S4-5 | M | No snapshot-sourcing rule or allowlists | FR-030 | CONFIRMED-REVISED; absorbs FR-030-4 |
| S5-1 | M | No AcceptanceEvent/snapshot/Booking tables | Schema | Revised C to M |
| S5-2 | M | Tech spec reads deprecated fields | Tech spec | Revised C to M (narrowed) |
| S5-3 | M | Hold/PWE and transition missing | Schema, tech spec | CONFIRMED-REVISED |
| S5-4 | M | "Appointment confirmed" at acceptance | Tech spec | CONFIRMED |
| S5-5 | M | No version/audit columns | Schema | CONFIRMED |
| S5-6 | M | Quote status enum conflict | FR-004, schema, tech spec | CONFIRMED |
| S1-4 | m | REQ-005-006 narrower than Key Entities | FR-005 | Revised M to m |
| S1-5 | m | Subquote id/state derivation unstated | FR-005 | Revised M to m; absorbs FR-005-2 |
| S1-9 | m | REQ-006-010 "lock exchange rate" | FR-006 | Revised M to m |
| S2-6 | m | Default vs quote currency | FR-026, FR-029 | Revised M to m |
| S4-6 | m | Misleading expiring-soon note | FR-030, FR-004 | Revised M to m |

S3-4 was parked.

## 6. Product Owner decisions

### Acceptance and recovery
1. **How does a patient recover after PWE?** (a) Cancel the inquiry and start a new one. (b) An audited reopening allows one new acceptance. Unblocks S1-1, FR-019-4. **Recommend (a):** MTG-002 never reopens the accepted quote and keeps one acceptance per inquiry.
2. **May an admin revive an expired booking?** (a) Never. (b) Through an audited override with a fresh hold. Unblocks FR-006-3. **Recommend (a):** MTG-002 blocks payment against an expired selection.
3. **What happens on withdrawal after acceptance?** (a) Cancel with a withdrawal cause, keep the AcceptanceEvent, and re-route by new inquiry. (b) The admin edits the booking. Unblocks S1-3, S4-1. **Recommend (a):** it mirrors B4, and MTG-002 forbids reselection.
4. **May an AcceptanceEvent be soft-deleted?** (a) No; annotation only. (b) Yes, without re-enabling acceptance. Unblocks FR-005-4. **Recommend (a):** MTG-002 makes it immutable.
5. **What happens to draft parents on acceptance?** (a) Cancel as `cancelled_other_accepted`. (b) Lock them. Unblocks FR-020-2. **Recommend (a):** it adds no new state.
6. **May FR-010 reassign the provider?** (a) Remove it. (b) Route it through FR-006 rebooking. Unblocks FR-010-4. **Recommend (a):** rescheduling is deferred to V2.
7. **Who clears travel-date review?** (a) The admin confirms or corrects. (b) The admin reopens submission. Unblocks FR-008-2. **Recommend (a):** one accountable owner.

### Promotions
8. **May patients use codes?** (a) Yes, before acceptance, on one named subquote, captured in the AcceptanceEvent. (b) Provider-only promotions. Unblocks FR-019-1. **Recommend (a):** the subquote stays atomic, and O01 keeps a single owner.
9. **May the promotion change after acceptance?** (a) It is frozen. (b) Only via a new version and acceptance. Unblocks FR-019-2. **Recommend (a):** MTG-002 2026-09-16 makes it read-only.
10. **When are promotion terms frozen on open quotes?** (a) At send, in the QuoteVersion. (b) Live until acceptance, with a version bump. Unblocks FR-004-5. **Recommend (a):** the patient compares exactly what was sent.
11. **When is the usage limit consumed?** (a) Reserve at acceptance, consume at confirmation, release on PWE or cancellation. (b) At capture. Unblocks FR-019-3, FR-019-4. **Recommend (a):** it covers every subquote outcome.

### Commission
12. **What is the commission base?** (a) Post-promotion, in the quote currency. (b) Pre-promotion. Unblocks FR-029-2, FR-015-1. **Recommend (a):** FR-017 already charges after discount.
13. **What does the FR-004 commission field show?** (a) Remove it. (b) Model and value, labelled "indicative until booking confirmation". Unblocks S2-4. **Recommend (b):** it informs without creating a second binding owner.

### Hold and settings
14. **Who owns the hold duration?** (a) FR-026. (b) FR-029. Default 48 hours, versioned. Unblocks S2-5. **Recommend (a):** FR-026 already owns quote expiry. The start at acceptance is already decided.
15. **When are expiry and currency captured?** (a) Both at first send. (b) Currency at draft creation, expiry at send. Unblocks FR-026-2. **Recommend (a):** one capture point.
16. **Which default currency is seeded?** (a) A code the PO names. (b) FR-029's Default Currency. Unblocks FR-026-3, S2-6. **Recommend (b):** avoids two currency settings.

### Packages and currency
17. **What is a package?** (a) A preset that seeds one Quote Option, with add-ons as items. (b) Keep add-on types. Unblocks FR-024-2, FR-024-1, FR-024-5. **Recommend (a):** it matches the D03 refinement and D04.
18. **Remove library currency?** (a) Yes. (b) Keep it and convert at selection. Unblocks FR-024-3. **Recommend (a):** MTG-002 says currency is never provider-entered.
19. **What if the FX rate is stale at acceptance?** (a) Proceed and record the rate timestamp. (b) Block acceptance. (c) Add a pending state. Unblocks FR-017-1. **Recommend (a):** no unmodelled state.

### Notifications
20. **How are provider acceptance notices grouped?** (a) One per provider. (b) One per parent quote. Unblocks FR-020-1. **Recommend (b):** matches FR-005 Screen 4.
21. **How much of `quote.accepted` is locked?** (a) The whole event. (b) The selected-provider and competing-parent outcomes. Unblocks S4-3. **Recommend (b):** matches `quote.cancelled_inquiry`.
22. **Is the withdrawal notice mandatory?** (a) Always. (b) Only after acceptance. Unblocks S4-1. **Recommend (b):** after acceptance a held slot is affected.

### Schema and storage
23. **Is `confirmed` a quote status?** (a) Add it. (b) Booking/case only. Unblocks S5-6. **Recommend (b):** MTG-002 places confirmation on the booking.
24. **How is the Booking persisted?** (a) New `bookings` and `acceptance_events` tables. (b) Extend `schedules`. Unblocks S5-1, S5-3. **Recommend (a):** it makes one acceptance per inquiry enforceable.

## 7. Suggested fix sequencing

**Pure edits (start now):**
- FR-010-1 with FR-010-2, FR-010-3 and FR-010-6.
- S1-2 (anchor the hold to acceptance) and S1-6.
- FR-022-2, FR-022-3 and FR-014-2.
- FR-007b-2.
- FR-024-5, FR-024-6 and FR-024-8.
- FR-029-1.
- FR-030-3, S4-5 and the S4-2 event.
- S5-2, S5-4 and S5-5.
- FR-019-7 and FR-020-4.
- All Minors.

**Waiting on decisions:**

| Decision(s) | Findings |
|---|---|
| 1 | S1-1, FR-019-4 |
| 2 | FR-006-3 |
| 3 and 22 | S1-3, S4-1 |
| 4 | FR-005-4 |
| 5 | FR-020-2 |
| 6 | FR-010-4 |
| 7 | FR-008-2 |
| 8–11 | FR-019-1, FR-019-2, FR-004-5, FR-019-3 |
| 12 and 13 | FR-029-2, S2-4 |
| 14–16 | S2-5, FR-026-2, FR-026-3, FR-026-4 |
| 17 and 18 | FR-024-1, FR-024-2, FR-024-3 |
| 19 | FR-017-1 |
| 20 and 21 | FR-020-1, S4-3 |
| 23 and 24 | S5-1, S5-3, S5-6 |

Order the work as FR-005/006 first, then FR-004, FR-019 and FR-024, then the consumers, then the system documents.

**Process.** Per CLAUDE.md "Template & Requirement Change Control", a Change Request is needed only for major events: changes to an already verified or implemented contract, such as the FR-010 snapshot rebase, the FR-024 model rewrite, the FR-019 freeze, FR-007b (which has no CR) and FR-022 (Verified). Smaller corrections go in each PRD's Appendix: Change Log. Per the "Update Log Protocol", major updates need a dated log file and a README entry; minor updates add a bullet to the same-day log.

## 8. Parked for the payment pass

- A locked currency later disabled (FR-007-2). Cancellation rate by cause (S3-4).
- FR-004 Workflow 6 refund/penalty depth. FR-019 post-payment Reverse/Refund and Applied→Completed timing.
- FR-006 retry backoff vs the fixed window. Captures racing PWE (FR-006, FR-007, FR-017-7).
- The deposit lock point and the deposit/instalment configuration lock (parts of FR-029-1).
- Commission base vs gross / "total procedure cost" (FR-007, FR-007b). Payout currency and Flat Rate conversion (FR-007, FR-015, FR-029).
- FR-007 scope omits the first instalment. FR-007b: first-instalment type, refund ladder, payout on Fully Paid, defaulted plans, ≥60-day window vs 48-hour hold, and the instalment arithmetic in S5-2.
- Payment-driven states vs TravelContext closure (FR-008). Cash-risk deposit view (FR-014). Late captures and commission (FR-015).
- FR-017: B2 config change, partial refunds, Due Date vs FR-007b. FR-019 funding split.
- `payment.failed` excludes the Provider and has no retry content (FR-020, FR-030).
- FR-026 Target Monthly Commission currency. FR-029 rounding and cache vs FR-026 invalidation.
- No automatic refund on provider-status cancellation. Flat-rate commission after an aftercare cascade.
- The system-prd refund ladder example. The schema `quotes.commission` placement.

## Appendix A. Rejected on verification

| ID | Original severity | Reason |
|---|---|---|
| FR-014-1 | Major | fr014:1423 already retains acceptance after cancellation or PWE, and fr014:1429 does not rewrite price observations. The missing recovery route is S1-1. |

## Appendix B. Minor and Observation findings (unverified, first pass)

m = Minor, O = Observation. Merged first-pass items appear in brackets.

- **FR-004:** 8 m CR-0909 says reconciliation is open; 9 m v2.7–2.8 untraced; 10 m provenance row omits provider-status; 11 m graft description editable; 12 m Screen 7 vs 2A item rule; 14 m "initial quote" wording; 15 O build-time slot conflicts. [13 → S1-9]
- **FR-005:** 7 m promotion/currency missing from comparison; 8 m `acceptedTotal` not written; 9 m compare-tray staleness; 10 m testability; 11 m mutable superseded flag and stale approvals [absorbs FR-006-8, S1-13]; 12 O no price range; 13 O CR predates v2.3/2.4.
- **FR-006:** 6 m quote-level wording; 7 m amount currency and source; 9 O slot capacity; 10 O per-day plan vs calendar.
- **FR-007:** 3 m guard paraphrase; 4 m "View Quote" opens the live quote. [5 → S1-10]
- **FR-007b:** 5 m confirmation vs first-charge order; 6 m status drift and provenance IDs; 7 O admin reschedule recalculation.
- **FR-008:** 4 m package wording; 5 m `included_services_snapshot` has two owners; 6 m `no_travel_required` has no field; 7 m other travel services; 8 m no scenarios; 9 O FR-004 timing wording.
- **FR-010:** 7 m stale CR screen numbers; 8 m vocabulary drift; 9 O approvals missing v2.1.
- **FR-014:** 3 m TTFQ cohorts; 4 O no leakage metric. [5 → S1-1]
- **FR-015:** 2 m snapshot on AcceptanceEvent; 3 m cancelling accepted vs terminal; 4 m rebooking path; 5 O scheduled suspension; 6 O "Accepted" overloaded.
- **FR-017:** 4 m lock wording; 5 m B2 renegotiation; 6 m Entity 7 duplicates the snapshot; 7 O no invoice rule after PWE.
- **FR-019:** 9 m quote-level wording; O1 O "save as reusable program".
- **FR-020:** 7 m `outcomeCode` vs `outcome`; 9 O no CR for v2.1. [5 → S4-7; 6 → S4-6; 8 → S4-3]
- **FR-022:** 4 m tie-breaking; 5 m no REQ-022-057 scenario; 6 m row unit; 7 m stale footer; 8 O no package filter; 9 O no CR for v2.13.
- **FR-024:** 9 m edit-lock wording [absorbs S2-10]; 10 m treatment identity; 11 m status vocabulary; 12 m last-known-good pricing; 13 m hard-delete not excluded; 14 O approvals.
- **FR-026:** 5 m no config version on quote; 6 m bounds and fallback; 7 m FR-020 consumer untraced; 8 m stale summary; 9 O "Default" label.
- **FR-029:** 5 m FX lock wording; 6 m snapshot lacks `config_id`; 7 O FX vs commission timing; 8 O Effective Date time zone.
- **FR-030:** 7 m event-name drift. [5 → S4-7; 6 → FR-020-1; 8 → S4-9]
- **S1:** 10 m AcceptanceEvent has no id [absorbs FR-007-5]. [11 → FR-006-5; 12 → FR-004-1; 13 → FR-005-11]
- **S2:** O1 O analytics configuration; O2 O commission between FR-015 and FR-029. [9 → S1-9; 10 → FR-024-9]
- **S3:** 6 m cascade omits drafts; 7 m `included_services` not named; 8 m cascade-cancelled shown Active; 9 O cascade omits FR-008.
- **S4:** 7 m `quote.updated` drift [absorbs FR-020-5, FR-030-5]; 8 m `quote.submitted` expiry claim; 9 m "Pending Payment" [absorbs FR-030-8]; 10 m reason drift; 11 m Screen 4 omits provider-status; 12 m event keys unnamed; 13 m FR-020 mirror; 14 O `quote.declined` has no producer.
- **S5:** 7 m package example; 8 m one-accepted not enforceable; 9 m analytics wording; 10 m add-on pricing; 11 m option tables omitted; 12 m stale CR status lines.

## Unresolved questions

1. Should the 66 unverified Minors and 24 Observations get a light verification pass before fixing?
2. The V4a header reports CONFIRMED=8, but its table shows 9 confirmed findings. This report follows the table.
3. Several cross-verifier merges were made at consolidation: FR-006-1 into S1-1; S2-1 and FR-017-3 into FR-019-2; S1-7 into FR-007b-2; FR-029-3 and S3-5 into S2-4. Should these stand?
4. Should decisions 14 and 16 be deferred to the payment pass?
5. Should this read-only report get an update-log entry?
