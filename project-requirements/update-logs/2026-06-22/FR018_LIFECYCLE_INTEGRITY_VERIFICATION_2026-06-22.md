# FR-018 Lifecycle Integrity Verification & Revision

**Date**: 2026-06-22
**Documents**:
- `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md` (v1.6 → v1.7)
- `.specify/memory/constitution.md` (Principle I — Multi-Tenant Architecture; amended with explicit user approval)

**Author**: Claude (Opus 4.8)

---

## Summary

Ran a verification pass on FR-018 (Affiliate Management) focused not only on the standard checklist but on whether the PRD can govern the **full affiliate lifecycle** end-to-end. The active lifecycle (onboard → earn → pay) was already comprehensive; gaps were concentrated at the **terminal end (offboarding)** and at **money correctness (FX)**. Eight issues were raised, decisioned with the user, and resolved in a single revision (v1.7). The constitution was amended (with explicit approval) to recognize the affiliate portal as a scoped external surface.

---

## Issues Resolved

1. **Affiliate Offboarding / Inactive state (was Critical)** — `Inactive` previously had no workflow or behavior. Added workflow **B5 (Offboarding/Deactivation)**, **Screen 3.3 (Deactivate/Offboard modal)**, **Rule 12 (lifecycle states)**, and **REQ-018-039**. Inactive is now a defined terminal state: codes disabled, portal read-only, historical data retained, and explicit final settlement (pay net ≥ $50 / forfeit residual below $50 / write off negative balance), each audited. Distinct from temporary, reversible Suspension (B3 / Screen 3.1).

2. **Currency standardization to USD (was Medium)** — Replaced the GBP-hardcoded currency rule. All affiliate amounts are now denominated in **USD (platform base currency owned by FR-029)**, and all non-USD-to-USD conversion/FX draws **exclusively from FR-029** using the rate locked for the underlying booking (no discrepancy with billing/finance). Added **REQ-018-040** and an FR-029 dependency entry; converted all `£`→`$` literals (numerals unchanged, per decision).

3. **Code-based attribution accepted & documented (was Medium)** — Added **Rule 11**: affiliate commission/referral credit is earned only when the affiliate's code is the *applied* discount; if a higher-priority code (Patient > Provider > Affiliate) supersedes it, no commission/credit accrues. Accepted as business policy (matches client intent); now stated in affiliate-facing terms and as an edge case.

4. **Affiliate portal vs. 3-tenant constitution (was Medium)** — Amended **constitution Principle I** to recognize the Affiliate Portal as a **scoped external surface operated within the Admin Platform tenant boundary** (not a fourth tenant). Added a matching Module Scope note in FR-018.

5. **Usage-limit basis (was Minor/Medium)** — Added **Rule 13**: `Maximum Usage Count` / `Per-Patient Usage Limit` decrement on **completed (paid) redemptions only**, with a separate soft rate-limit on "applied" events to prevent application spam. Updated REQ-018-004 and the code-config screen.

6. **Pending status (was Minor)** — Onboarding now sets initial status **Pending** (system-set, not admin-selectable), flipping to Active on activation. Updated main flow, entity status enum, Screen 1 dropdown/badges, and portal Account Status.

7. **Name made admin-controlled (was Minor)** — `Affiliate Name` (legal/payout name used for attribution & Stripe) is now admin-controlled and removed from affiliate self-service. Updated Profile tab (Screen 9.4), editability rules, REQ-018-031, and acceptance criteria.

8. **Negative-balance terminal handling (was Minor)** — Folded into B5: an unrecoverable negative balance is written off on deactivation with an audit entry (no future payouts to net against).

---

## Verification Outcome

- **Constitution compliance**: Pass (Principle I amended to close the tenant flag).
- **Client alignment**: Strong — applied-vs-completed, monthly-on-7th payouts, paid/unpaid split, and code-based attribution all trace to transcripts.
- **Cross-FR consistency**: Clean — discount priority matches FR-019; FX ownership delegated to FR-029; payout rails/bank details mirror FR-017/029/032.
