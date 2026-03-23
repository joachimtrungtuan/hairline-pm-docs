# UX/UI Evaluation Rules — Design Layout Verification

This document defines the concrete checklist and severity benchmarks for evaluating screen layout design quality. Every UX/UI finding MUST reference a specific rule from this document. No finding should be based on subjective impression alone.

---

## Table of Contents

1. [How to Use This Document](#1-how-to-use-this-document)
2. [Severity Classification](#2-severity-classification)
3. [Universal Checks (All Platforms)](#3-universal-checks-all-platforms)
4. [Mobile-Specific Checks](#4-mobile-specific-checks)
5. [Web-Specific Checks](#5-web-specific-checks)
6. [Output Format](#6-output-format)

---

## 1. How to Use This Document

For every screen being evaluated:

1. Run through **all applicable checks** in Sections 3–5
2. For each check: evaluate → assign PASS / ISSUE → if ISSUE, assign severity using Section 2
3. Every reported finding MUST cite the **rule ID** (e.g., `U-03`, `M-07`) and the **specific criterion** that was violated
4. If a check cannot be evaluated from the provided layout (e.g., interaction behavior from a static image), mark as `N/A — cannot verify from static layout` — do not guess

**Which sections apply:**

| Platform | Apply Sections |
|----------|---------------|
| Patient Mobile, Provider Mobile | Section 3 (Universal) + Section 4 (Mobile) |
| Admin Web, Provider Web | Section 3 (Universal) + Section 5 (Web) |
| Mixed / Unknown | Section 3 (Universal) + both Sections 4 & 5 |

---

## 2. Severity Classification

Every UX/UI issue receives exactly one severity. Use these criteria — not intuition.

### 🔴 Critical UX

The issue **blocks the user from completing their task** or **causes them to take the wrong action**.

**Criteria (any one is enough):**

- Primary CTA is invisible, unlabeled, or indistinguishable from non-interactive elements
- User cannot determine what action to take next (no clear exit path)
- Destructive action has no visual differentiation from safe actions (e.g., "Delete" button styled same as "Save")
- Text is unreadable (contrast ratio below 3:1 for large text, below 4.5:1 for body text)
- Critical information is hidden below the fold with no scroll indicator
- Touch target is too small to tap reliably (<32pt on mobile) for a primary action
- Two adjacent interactive elements are so close they would cause frequent mis-taps on primary actions

### ⚠️ UX Improvement

The issue **causes user confusion, friction, or inefficiency** but does not block task completion.

**Criteria (any one is enough):**

- Visual hierarchy doesn't match information priority (secondary info is more prominent than primary)
- Inconsistent component styling within the same screen (e.g., two buttons with different styles for same-level actions)
- Form labels are ambiguous or could be misinterpreted
- Error states don't clearly indicate what went wrong or how to fix it
- Navigation pattern breaks platform conventions (e.g., Android back gesture leads nowhere)
- Information density is too high — screen feels cluttered, hard to scan
- Touch targets are between 32–44pt on mobile (functional but below recommended)
- Color usage contradicts semantic meaning (e.g., green for an error message, red for a success state)
- Missing visual feedback for interactive state (e.g., button doesn't look tappable)

### 💡 UX Suggestion

The issue is **a polish opportunity** — the screen works but could be better.

**Criteria (any one is enough):**

- Spacing is slightly inconsistent but doesn't harm readability
- Typography hierarchy could be clearer (e.g., section headers same weight as body)
- Icon style is inconsistent with the rest of the app but still understandable
- Alignment is slightly off but not distracting
- Empty states could be more helpful (e.g., add illustration or guidance text)
- Minor platform convention deviation that most users won't notice

---

## 3. Universal Checks (All Platforms)

Apply these to every screen regardless of platform.

### Visual Hierarchy

| ID | Check | Pass Criteria | Common Failures |
|----|-------|---------------|-----------------|
| U-01 | **Primary action prominence** | The most important action (submit, confirm, next) is the most visually prominent element on screen — larger, bolder, or higher contrast than secondary actions | Primary CTA same size/color as secondary buttons |
| U-02 | **Information priority** | The most important information (screen title, key data, status) appears at the top or in the most prominent position | Key info buried below less important content |
| U-03 | **Visual grouping** | Related fields/information are visually grouped (proximity, borders, background) and separated from unrelated content | All fields in a flat list with no grouping |
| U-04 | **Section headings** | Distinct sections have clear headings that describe the content below | Large blocks of content with no section breaks |

### Spacing & Alignment

| ID | Check | Pass Criteria | Common Failures |
|----|-------|---------------|-----------------|
| U-05 | **Consistent padding** | Padding between elements follows a consistent rhythm (e.g., 8/16/24pt increments) | Random padding values — 12pt here, 19pt there |
| U-06 | **Horizontal alignment** | Elements within a group are left-aligned (LTR) or consistently aligned | Labels and fields misaligned |
| U-07 | **Vertical spacing** | Space between sections > space between items within a section | Items within a section have more space than between sections |
| U-08 | **Edge margins** | Content has consistent margins from screen edges | Content touches screen edge or has inconsistent margins |

### Typography

| ID | Check | Pass Criteria | Common Failures |
|----|-------|---------------|-----------------|
| U-09 | **Text readability** | Body text ≥14pt (mobile) or ≥14px (web). Caption/helper text ≥12pt/12px | Body text too small to read comfortably |
| U-10 | **Heading hierarchy** | Clear visual distinction between heading levels (size, weight, or color) | H2 and H3 look identical |
| U-11 | **Label clarity** | Field labels are concise, descriptive, and positioned consistently (above or beside the field) | Labels are vague ("Item 1"), or positioned inconsistently |
| U-12 | **Text truncation** | Long text is handled gracefully (ellipsis, expand, wrap) — not clipped without indication | Text appears cut off with no ellipsis or "more" option |

### Color & Contrast

| ID | Check | Pass Criteria | Common Failures |
|----|-------|---------------|-----------------|
| U-13 | **Text contrast** | Body text has ≥4.5:1 contrast ratio against background. Large text (≥18pt bold or ≥24pt) has ≥3:1 | Light gray text on white background |
| U-14 | **Semantic color usage** | Red/warm colors for destructive/error. Green/cool for success/positive. Yellow/amber for warning | Red "Success" banner, green "Delete" button |
| U-15 | **Color not sole indicator** | Information conveyed by color is also conveyed by text, icon, or shape (accessibility) | Status shown only by dot color with no label |
| U-16 | **Interactive vs static distinction** | Interactive elements (buttons, links, toggles) are visually distinct from static text/labels | Buttons look like plain text, or text looks like buttons |

### Interaction Patterns

| ID | Check | Pass Criteria | Common Failures |
|----|-------|---------------|-----------------|
| U-17 | **CTA label clarity** | Button/action labels describe what will happen ("Save Changes", "Delete Account") not vague ("Submit", "OK", "Continue") | Generic "Submit" on a critical action |
| U-18 | **Destructive action safeguard** | Destructive actions (delete, cancel, remove) are visually distinct (red/outlined) and not positioned where users might accidentally tap | "Delete" as primary blue button next to "Save" |
| U-19 | **Error state clarity** | Error messages are visible, near the relevant field, and explain what's wrong + how to fix it | Generic "Error occurred" with no field indication |
| U-20 | **Empty state design** | Empty lists/sections show a message explaining why empty and suggesting next action | Blank white space with no guidance |
| U-21 | **Loading/progress indication** | Long operations show progress indicator or skeleton screen (if spec defines loading state) | No indication that something is loading |

### Consistency

| ID | Check | Pass Criteria | Common Failures |
|----|-------|---------------|-----------------|
| U-22 | **Component consistency** | Same type of component looks the same across the screen (all buttons same style, all cards same structure) | Two different button styles for same-level actions |
| U-23 | **Terminology consistency** | Same concept uses same term throughout the screen and flow (e.g., always "Inquiry" not sometimes "Request") | "Booking" on one part, "Reservation" on another |
| U-24 | **Icon style consistency** | Icons use the same style family (all outline, all filled, or all material) | Mix of filled and outline icons |

### Navigation & Flow

| ID | Check | Pass Criteria | Common Failures |
|----|-------|---------------|-----------------|
| U-25 | **Back navigation** | User can navigate back to previous screen (back button, swipe, breadcrumb) | No way to go back |
| U-26 | **Progress indication** | Multi-step flows show progress (step indicator, progress bar, breadcrumb) | User doesn't know they're on step 3 of 5 |
| U-27 | **Scroll indicator** | If content extends below visible area, there's visual indication of more content | Content cut off with no shadow/gradient/scroll indicator |

---

## 4. Mobile-Specific Checks

Apply these only when the platform is mobile (Patient Mobile, Provider Mobile).

| ID | Check | Pass Criteria | Common Failures |
|----|-------|---------------|-----------------|
| M-01 | **Touch target size** | All interactive elements ≥44x44pt (iOS) or ≥48x48dp (Android). Minimum acceptable: 32x32pt | Small checkbox or radio button with no tap padding |
| M-02 | **Touch target spacing** | Adjacent interactive elements have ≥8pt gap between tap areas | Two buttons touching edge-to-edge |
| M-03 | **Thumb zone placement** | Primary actions are in the bottom 60% of the screen (comfortable thumb reach on one-handed use) | Critical CTA at the very top of a long screen |
| M-04 | **Safe area compliance** | Content does not extend into device notch, home indicator, or status bar areas | Text overlapping status bar |
| M-05 | **Native navigation patterns** | Uses platform-standard navigation (iOS: back chevron top-left, tab bar bottom. Android: back arrow, bottom nav) | Custom navigation that breaks platform muscle memory |
| M-06 | **Bottom sheet / modal usage** | Secondary selections use bottom sheets (mobile standard). Full-screen modals reserved for complex forms | Full-screen takeover for a simple date picker |
| M-07 | **Keyboard awareness** | Input fields are not positioned where they would be hidden by the keyboard (or screen scrolls to accommodate) | Form field hidden behind keyboard with no scroll |
| M-08 | **Single-column layout** | Content follows single-column layout (mobile standard). Side-by-side elements only when justified (e.g., comparison table) | Desktop-style multi-column layout on mobile |
| M-09 | **Gesture affordance** | Swipeable elements have visual hints (cards with peek, drag handles, pagination dots) | Swipeable content with no visual indication |
| M-10 | **Status bar integration** | Status bar is visible and uses appropriate style (light/dark) for the screen background | Status bar hidden or unreadable against background |

---

## 5. Web-Specific Checks

Apply these only when the platform is web (Admin Web, Provider Web).

| ID | Check | Pass Criteria | Common Failures |
|----|-------|---------------|-----------------|
| W-01 | **Layout grid** | Content follows a recognizable grid system (12-column or similar). Elements align to grid | Elements placed at arbitrary positions |
| W-02 | **Responsive awareness** | Layout suggests adaptation for different widths (sidebar collapses, table scrolls, cards reflow) | Fixed-width layout that would break on narrow screens |
| W-03 | **Navigation structure** | Clear primary navigation (top bar, sidebar) with current location indicated | No navigation or no indication of current page |
| W-04 | **Breadcrumbs / page title** | Page has a clear title and breadcrumb trail for deep pages | No breadcrumb on a page 3 levels deep |
| W-05 | **Form layout** | Labels above or left-of fields (consistent). Related fields grouped. Clear required-field indicators | Labels in random positions, no grouping |
| W-06 | **Table design** | Data tables have clear headers, consistent column alignment, row hover/selection state, and pagination for large datasets | Headers indistinct from data, no pagination |
| W-07 | **Action placement** | Page-level actions (save, cancel) in consistent position (top-right or bottom-right). Inline actions near their target | Save button in a different spot on each page |
| W-08 | **Whitespace usage** | Adequate whitespace between sections for scannability. Not too dense, not too sparse | Wall of text/fields with no breathing room |
| W-09 | **Link styling** | Links are visually distinct from plain text (underline, color, or both). Visited state differs from unvisited | Links look like regular text |
| W-10 | **Keyboard accessibility indicators** | Focus states visible on interactive elements (outline, highlight) | No visible focus ring when tabbing |

---

## 6. Output Format

For each screen, report UX/UI findings in this format:

```md
UX/UI EVALUATION: [Screen ID]
Platform checks applied: [Universal + Mobile / Universal + Web]

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-14 | Semantic color usage | 🔴 Critical UX | "Delete Account" button uses green/positive styling — spec requires destructive/red | Layout file: Delete your account.png — green button visible at bottom |
| M-01 | Touch target size | ⚠️ UX Improvement | Checkbox appears smaller than 44pt minimum | Layout file: Settings.png — checkbox visual size ~24pt |
| U-05 | Consistent padding | 💡 UX Suggestion | Spacing between form fields varies (some ~16pt, some ~24pt) | Layout file: Payment Form.png — inconsistent gaps |

UX/UI Summary:
- Checks evaluated: [N]
- Critical UX: [N] | UX Improvement: [N] | UX Suggestion: [N] | N/A: [N]
```

**Every finding row MUST have:**

- **Rule ID**: From this document (e.g., U-14, M-01, W-06)
- **Severity**: From Section 2, based on the criteria — not on feeling
- **Evidence**: Which layout file and what was observed
