# Design Layout Verification Report — {FR_IDENTIFIERS}

**Report Date**: {YYYY-MM-DD}
**Report Type**: Design Layout Verification
**FR Scope**: {FR-### — Feature Name} {(repeat for multi-FR)}
**Flow Scope**: {All flows / List of specific flows checked}
**Layout Source**: `layout-temp/` {(note subfolder if relevant)}
**Platform**: {Patient Mobile / Provider Web / Admin Web / Mixed}
**Status**: {Overall status — see below}

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| {Flow ID} | {Flow Name} | {Module ID}: {Module Name} | {N} | {N} | {🟢/🟡/🔴} {COMPLETE/PARTIAL/BLOCKED} | ~{XX}% |

**Overall**: {X} of {Y} flows verified. {Summary sentence — e.g., "2 flows BLOCKED due to missing design files."}
**Screens**: {X} of {Y} specified screens have layouts (~{XX}% coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `{subfolder/filename.ext}` | {Flow ID} | {Screen ID} ({Screen Name}) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `{subfolder/filename.ext}` | {Description} | {Outside scope / Unknown / Different FR} |

---

## Detailed Verification by Flow

---

### Flow {FLOW_ID}: {Flow Name}

**Status**: {🟢/🟡/🔴} {COMPLETE/PARTIAL/BLOCKED} — {one-line description}
**Screens required**: {N}
**Layout files**: `{file1.ext}`, `{file2.ext}`, ...

#### Screen {SCREEN_ID}: {Screen Name}

**Layout**: `{subfolder/filename.ext}`

##### Flow Context

- **User arrives from**: {previous screen/action in flow}
- **Screen purpose**: {what this screen accomplishes in the user journey}
- **Entry point**: {Present / Missing — description}
- **Exit path**: {Present / Missing — what action leads to next step}
- **Data continuity**: {Correct / Issues — data from previous screens that should appear}
- **Flow context issues**: {List or "None"}

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| {Field Name} | {Yes/No/Conditional} | {✅/⚠️/❌⚠️/❌/➕} | {Details — label mismatch, wrong type, missing, etc.} |

**Extra Elements**:

- {Element description} — {Notes}

**Screen Status**: {🟢/🟡/🔴/⬜} {COMPLETE/GOOD/PARTIAL/FAIL/NO DESIGN}
**Field Coverage**: {pass+minor}/{total required} ({XX}%)
**Critical Issues**: {List or "None"}

##### UX/UI Design Evaluation

**Skills invoked**: {ui-ux-pro-max, mobile-design / web-design-guidelines}

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| {🔴 Critical UX / ⚠️ UX Improvement / 💡 UX Suggestion} | {Description of the UX/UI issue} | {What to change} |

{Repeat #### Screen block for each screen in the flow}

**Flow Coverage Gaps**:

- {Gap description — e.g., "No error state layout for Screen S2"}
- {Gap description}

---

{Repeat ### Flow block for each flow}

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | {Flow ID} | {Screen ID} | {Issue description} | {What to fix} |
| 🔴 Critical UX | {Flow ID} | {Screen ID} | {UX issue description} | {What to fix} |
| ⚠️ Important | {Flow ID} | {Screen ID} | {Issue description} | {What to fix} |
| ⚠️ UX Improvement | {Flow ID} | {Screen ID} | {UX issue description} | {What to fix} |
| 💡 Suggestion | {Flow ID} | {Screen ID} | {Issue description} | {What to improve} |
| 💡 UX Suggestion | {Flow ID} | {Screen ID} | {UX issue description} | {What to improve} |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- {Any overall observations, patterns, or recommendations}
- {Reference to source FR documents used}
- {Note if any layout files were unreadable or corrupted}
