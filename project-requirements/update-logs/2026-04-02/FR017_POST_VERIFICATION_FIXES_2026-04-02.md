# FR-017 Post-Verification Fixes (Round 2) — 2026-04-02

**Type**: Major Update  
**FR**: FR-017 Admin Billing & Financial Management  
**PRD Version**: 1.2 → 1.3  
**Files Modified**:
- `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`
- `local-docs/project-requirements/system-prd.md`

---

## Changes Applied

### 1. Installment Cutoff: Hardcoded → FR-029-Configurable (Issue #1)

**What changed**: Removed "Installment cutoff date (30 days before treatment)" from the "Fixed in Codebase" list. Added it to the Admin Editability → "Not in scope — see FR-029" section. Updated Business Rule 6 to reference FR-029 as the source of the cutoff days.

**Why**: FR-006 (Booking & Scheduling) explicitly states the cutoff days are configured via FR-029 split payment settings. FR-017 had a contradictory "hardcoded" classification. Aligned to FR-029 as single source of truth.

---

### 2. System PRD: Removed Discount Creation from FR-017 (Issue #2)

**What changed**: Removed "Admins MUST be able to create and manage discount codes" from FR-017 requirements in system-prd.md. Kept only "System MUST track discount code usage and ROI" with a note that creation is owned by FR-019 / A-06.

**Why**: FR-017 PRD (v1.1) had already moved discount creation to FR-019. The system PRD was not updated, creating a stale ownership conflict.

---

### 3. Removed 2-Person Secondary Approval for Refunds (Issue #3)

**What changed**:
- Business Rules: "emergency refunds ONLY with secondary admin approval (2-person authorization)" → "refunds with mandatory reason + audit trail; no secondary approver required"
- Security: Removed "Super Admin secondary approval capability for high-value transactions (>£10,000)"; Super Admin now has identical refund flow to Billing Admin
- User Story 6 Scenario 2: Replaced broken secondary approval scenario (£1,800 refund triggering a >£10,000 threshold check) with: admin enters mandatory reason and confirms
- User Story 6 Scenario 3: Adjusted from "secondary approval received" → "admin confirms; Stripe refund initiated; audit trail logged"

**Why**: Transcription search across all 7 client transcription files found zero mentions of secondary approval, 2-person authorization, or high-value payment thresholds. This requirement was AI-generated with no client basis and inflates the business workflow unnecessarily. The audit trail (mandatory reason + logging) is the actual control mechanism needed.

---

### 4. Replaced FR-005 Dependency with FR-006 (Issue #4)

**What changed**: Dependency "FR-005 / Module P-03: Booking & Payment" replaced with "FR-006 / Module P-03: Booking & Scheduling". Updated description to accurately reflect that booking confirmation (not payment intents) triggers invoice generation and that FR-006 owns the cancellation policy.

**Why**: FR-005 in system PRD is "Quote Comparison & Acceptance" (Module P-02) — not a payment or booking module. The described integration (booking confirmation triggering billing) maps to FR-006.

---

### 5. Screen 6 Affiliate Billing: Two-Tab Layout Required (Issue #5)

**What changed**: Added a business requirement note to Screen 6 Notes section specifying a two-tab layout: "Pending Payouts" tab (default) and "Paid Payouts" tab.

**Why**: Client transcription (Hairline-AdminPlatform-Part1.txt:405): "it should really be split into two. So once this is paid, it should be, you know, a paid section, not, they shouldn't be on one list like this."

---

### 6. Screen 3 Due Date: Provenance Documented (Issue #6)

**What changed**: Updated the `Due Date` field description in Screen 3 (Patient Invoice List) to document its derivation: FR-007B installment schedule (if installment plan) or booking confirmation terms — 7 days before treatment per Payment Rule 2 (if full/deposit payment).

---

### 7. Integration Numbering: Renumbered 1/4/5 → 1/2/3 (Issue #7)

**What changed**: Integration 4 (Currency Exchange API) → Integration 2. Integration 5 (Provider Platform Read-Only API) → Integration 3. Gaps were left from prior revision cleanup.

---

### 8. SC-019: Corrected Concurrent Admin Target (Issue #8)

**What changed**: SC-019 changed from "500+ concurrent admin users" to "50 concurrent admin users" with a note to revisit at 12-month growth review.

**Why**: Expected launch scale is a small admin team (not 500 admins). 500 concurrent was inconsistent with the scalability section's own stated launch team size.
