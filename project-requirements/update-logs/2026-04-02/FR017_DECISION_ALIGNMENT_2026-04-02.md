# FR-017 Decision Alignment — 2026-04-02

**Type**: Major Update  
**FR**: FR-017 Admin Billing & Financial Management  
**PRD Version**: 1.5 → 1.6  
**Files Modified**:
- `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`
- `local-docs/project-requirements/system-prd.md`

---

## Summary

Aligned FR-017 and the system PRD to the final product decisions taken after the verification review. This pass resolves the remaining ownership, payout-processing, and commission-routing ambiguities without changing the agreed feature scope.

---

## Changes Applied

### 1. Affiliate Ownership Boundary Finalized

**What changed**:
- Clarified in FR-017 that **FR-018 owns affiliate management and commission calculation**
- Clarified that **FR-017 owns affiliate billing and payout execution**
- Updated the system PRD so affiliate payout execution now sits under FR-017 instead of FR-018

**Why**: Product direction is that affiliate administration lives in A-07, while all billing and payout execution for patients, providers, and affiliates is centralized in A-05.

---

### 2. MVP Provider Payout Automation Confirmed

**What changed**:
- Replaced the stale manual-payout assumption in FR-017
- Updated system PRD wording so admins approve provider payout statements, and the system auto-processes approved payouts on payout day

**Why**: This matches the accepted workflow decision: approval-first, automated payout-day execution.

---

### 3. Commission Routing Corrected to FR-015

**What changed**:
- Replaced Screen 10 currency-alert action text from `Adjust commission via FR-029` to `Adjust provider commission via FR-015`
- Removed `global commission defaults` from the FR-029 dependency explanation in FR-017

**Why**: Provider commission ownership already sits in FR-015. FR-029 owns payment-system configuration such as Stripe accounts, FX rate sources/markup, deposit rules, and payout buffer settings.

---

### 4. RBAC Requirement Cleaned Up

**What changed**:
- Updated `REQ-017-017` so `Super Admin` is defined as **full access**, not a stale `secondary approval` role

**Why**: Earlier refund-flow fixes had already removed the unsupported secondary-approval concept, but the requirement summary still referenced it.

---

## Minor Follow-Up

- Corrected the `Screen Specifications` heading hierarchy in `fr017-admin-billing-finance/prd.md` so platform group headings remain `###`, individual screens are `####`, and nested screen tabs are `#####`.
- Reordered the admin screen specifications so the Financial Reporting Dashboard is now `Screen 1`, shifted the subsequent admin screens accordingly, updated the affected internal screen references, and noted in the PRD appendix that pre-`v1.7` changelog entries still use the older screen labels.
