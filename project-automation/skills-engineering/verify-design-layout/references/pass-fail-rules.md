# Pass/Fail Rules — Design Layout Verification

This document defines the evaluation criteria for verifying Figma design layouts against FR screen specifications. Used by both the main orchestrator and sub-agents.

---

## Table of Contents

1. [Field-Level Statuses](#1-field-level-statuses)
2. [Screen-Level Statuses](#2-screen-level-statuses)
3. [Flow-Level Statuses](#3-flow-level-statuses)
4. [Critical Field Definition](#4-critical-field-definition)
5. [Edge Cases and Judgment Calls](#5-edge-cases-and-judgment-calls)
6. [Scoring Formula](#6-scoring-formula)

---

## 1. Field-Level Statuses

Each data field listed in the FR's Screen Specification table receives exactly one status.

### ✅ PASS

The field is **present** in the layout AND **matches** the spec.

**All of these must be true:**
- Field is visually identifiable in the layout (image) or structurally present (JSON)
- Field type matches: a `select` field shows a dropdown/picker, a `text` field shows text display, a `checkbox` shows a toggleable control, etc.
- Label is functionally equivalent — exact wording match not required, but meaning must be the same (e.g., "Email" vs "Email Address" = PASS)
- If the spec defines validation rules visible in the UI (e.g., "Must be checked before payment"), the corresponding UI affordance exists (e.g., checkbox is present)
- Required/conditional visibility matches — if spec says "Conditional: only shown if X", the layout includes a corresponding state file or the field is absent in the default state (both acceptable)

### ⚠️ MINOR ISSUE

The field is **present** and **functionally correct** but has a **cosmetic discrepancy**.

**Triggers (any one is enough):**
- Label casing differs: "Notification settings" vs "Notification Settings"
- Minor label wording: "Go Back" vs "Back" (same function)
- Styling deviates from spec but doesn't break functionality: wrong color on a non-critical element, different icon style
- Placeholder/dummy data present where real data would go (e.g., "Turkish Airlines" as booking reference)
- Field order within a group differs from spec order (but all fields present)

### ❌⚠️ MISMATCH

The field is **present** but **wrong** — it would mislead users or break logic.

**Triggers (any one is enough):**
- Wrong field type: spec says `password` input but layout shows `email` input
- Wrong data displayed: field shows data from a different entity or context
- Contradicts spec behavior: spec says "disabled until X" but layout shows enabled state
- Label communicates different meaning: "Delete Account" vs "Request Deletion" (different user expectation about immediacy)
- Required acknowledgment/checkbox present but with wrong or missing policy text
- Button style contradicts spec intent: spec says "destructive/red" but layout shows "positive/green"
- A conditional state shows the wrong variant (e.g., showing success when error state was expected)

### ❌ MISSING

The field is **not present** in the layout at all.

**Criteria:**
- The field is listed as `Required: Yes` in the FR data fields table
- No visual element in the layout corresponds to this field
- No JSON node matches this field's name or type
- The field is not in any variant/state file for this screen

**Exception:** If the field is `Required: Conditional` and the layout shows the non-triggering state, mark as ✅ PASS (the field correctly does not appear).

### ➕ EXTRA

An element exists in the layout that has **no corresponding spec entry**.

**Criteria:**
- A visible UI element (field, button, label, section) appears in the layout
- No matching entry in the FR's data fields table or business rules
- Not a standard navigation element (back button, status bar, tab bar) unless those are explicitly specified

**What to note:** Describe the element and flag whether it appears intentional (designer enhancement) or accidental (wrong screen content pasted in).

---

## 2. Screen-Level Statuses

Computed by aggregating field-level statuses for all fields in that screen's spec.

### 🟢 COMPLETE

- 100% of required fields are ✅ PASS
- Zero ❌ MISSING or ❌⚠️ MISMATCH
- May have ⚠️ MINOR or ➕ EXTRA (these don't prevent COMPLETE)

### 🟢 GOOD

- ≥90% of required fields are ✅ PASS
- Remaining fields are ⚠️ MINOR only
- Zero ❌ MISSING
- Zero ❌⚠️ MISMATCH

### 🟡 PARTIAL

Any of these:
- 50–89% of required fields are ✅ PASS or ⚠️ MINOR
- Has 1–2 ❌ MISSING required fields (non-critical)
- Has 1–2 ❌⚠️ MISMATCH fields
- Screen is recognizable and most of the intended flow is achievable

### 🔴 FAIL

Any of these:
- <50% required field coverage
- ≥3 ❌ MISSING required fields
- Any **critical field** (see Section 4) is ❌ MISSING or ❌⚠️ MISMATCH
- Screen is unrecognizable or would completely block the user flow
- Layout file exists but shows wrong screen content entirely

### ⬜ NO DESIGN

- No layout file (PNG/JPG/JSON) exists for this screen
- No file in `layout-temp/` can be reasonably mapped to this screen

---

## 3. Flow-Level Statuses

Computed by aggregating screen-level statuses for all screens in the flow.

### 🟢 COMPLETE

- All screens are 🟢 COMPLETE or 🟢 GOOD
- Flow transitions are logically sound (user can navigate the full flow)

### 🟡 PARTIAL

- At least one screen is 🟡 PARTIAL
- No screen is 🔴 FAIL or ⬜ NO DESIGN
- The flow is understandable despite gaps

### 🔴 BLOCKED

Any of these:
- Any screen is 🔴 FAIL
- Any screen is ⬜ NO DESIGN
- Flow transitions are broken (no visible path from Screen N to Screen N+1)
- A screen required for conditional/error handling is entirely absent

---

## 4. Critical Field Definition

A field is **critical** if its absence or mismatch would:

1. **Block flow progression**: Submit/confirm/next button, required acknowledgment checkbox, required input that gates the next screen
2. **Break data integrity**: Primary identifier (booking reference, user ID), amount fields in payment flows, status badges that drive conditional rendering
3. **Cause security/legal risk**: Authentication inputs (password, OTP), policy acknowledgment checkboxes, consent toggles
4. **Mislead the user about state**: Status badges, confirmation messages, error indicators

**Examples of critical fields:**
- Submit/confirm/action buttons (any flow)
- Password/OTP input fields (authentication flows)
- Payment amount + deposit breakdown (payment flows)
- Booking reference number (confirmation screens)
- Cancellation policy acknowledgment checkbox (booking flows)
- Error state indicators (any flow with validation)

**When a critical field is ❌ MISSING or ❌⚠️ MISMATCH, the screen is automatically 🔴 FAIL regardless of other field coverage.**

---

## 5. Edge Cases and Judgment Calls

### Combined screens

If one layout file contains two screens combined (e.g., a list view with an expanded detail panel), evaluate both screens from that single file. Note in the report that screens are combined.

### State variants

Many screens have multiple states (empty, populated, error, loading, blocked). Each state that is explicitly defined in the FR should have a corresponding layout file or be visibly represented. If a state is missing:
- If it's an error/blocked state → ❌ MISSING (these are often critical)
- If it's an empty state → ⚠️ MINOR (unless the FR marks it as required)
- If it's a loading state → ⚠️ MINOR (usually not designed separately)

### Navigation elements

Standard navigation (back arrow, tab bar, status bar) is evaluated only if the FR explicitly lists them in the data fields table. If the FR says "Back Navigation: Required" and it's missing, that's ❌ MISSING.

### Extra screens in layout

If `layout-temp/` contains screens that don't map to any in-scope flow, list them in the "Unmapped Files" section. Do not evaluate them — just catalog.

### Approximate field coverage percentage

```
coverage% = (count of ✅ PASS + count of ⚠️ MINOR) / (total required fields) × 100
```

❌⚠️ MISMATCH counts as neither pass nor miss — it reduces confidence but doesn't reduce coverage percentage. Report it separately.

---

## 6. Scoring Formula

### Screen score

```
required_fields = count of fields where Required = Yes or Required = Conditional (when condition is met)
pass_count = count of ✅ PASS fields
minor_count = count of ⚠️ MINOR fields
missing_count = count of ❌ MISSING fields
mismatch_count = count of ❌⚠️ MISMATCH fields
has_critical_issue = any critical field is ❌ MISSING or ❌⚠️ MISMATCH

coverage = (pass_count + minor_count) / required_fields × 100

if has_critical_issue → 🔴 FAIL
elif coverage == 100 and mismatch_count == 0 and missing_count == 0 → 🟢 COMPLETE
elif coverage >= 90 and missing_count == 0 and mismatch_count == 0 → 🟢 GOOD
elif coverage >= 50 or (missing_count <= 2 and mismatch_count <= 2) → 🟡 PARTIAL
else → 🔴 FAIL
```

### Flow score

```
screen_statuses = [status for each screen in flow]

if all status in (COMPLETE, GOOD) → 🟢 COMPLETE
elif any status in (FAIL, NO_DESIGN) → 🔴 BLOCKED
elif any status == PARTIAL → 🟡 PARTIAL
```
