---
description: Generate a date-stamped verification report and implementation task list (Plane-ready HTML) from gaps/conflicts found during checklist verification.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## When To Use This Prompt

Use this prompt **ONLY** when the user explicitly asks to:

- Create implementation tasks from checklist verification gaps/conflicts, and/or
- Produce a verification report file for sharing.

If the user only wants to **update the checklist itself**, use: `local-docs/task-prompt/check-progress.md`.

## Required Inputs

**MUST** ask for these inputs (do not proceed without them):

1. **Checklist file path** used as the base
2. **Verification findings source**, one of:
   - The agent’s verified findings from the same session, or
   - A pasted “findings” block from the user, or
   - The exact module+FR rows/items in the checklist to convert into tasks

## Output Rules

- **MUST** create files under `local-docs/task-creation/{CURRENT_DATE}/`
- **MUST NOT** edit product code in this prompt (tasks/report only)
- **MUST NOT** change the checklist file unless the user explicitly asks

## Execution Flow

### Step 1: Get Current Date

**MUST** get current date: Run `date +%Y-%m-%d`, store as `CURRENT_DATE`.

### Step 2: Create Directory Structure and Files

**MUST** create date-based subfolder first: `local-docs/task-creation/{CURRENT_DATE}/` (create if doesn't exist). Then create files inside:

1. `verification-report-{CURRENT_DATE}.md` - Verification report (brief)
2. `implementation-tasks-{CURRENT_DATE}.md` - Implementation tasks (Plane-ready)

### Step 3: Write Verification Report (Under 500 Words)

**MUST** include:

1. **Summary**: Total checked, alignment percentage (if available), top 3 critical gaps
2. **Gap Analysis**: What is missing or incomplete
3. **Conflict Resolution**: Items where checklist status differs from reality; recommend updates
4. **Next Steps**: Top 5 actions, ordered by impact

### Step 4: Create Implementation Tasks From Findings

For **EACH** missing/incomplete component, **MUST** create a task with:

1. **Task Name**: Start with prefix `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, or `[BUG]` + descriptive name
   - `[FE+BE TASK]`: UI + API work
   - `[FE TASK]`: UI-only work (React in `main/hairline-frontend/` or Flutter in `main/hairline-app/`, depending on module)
   - `[BE TASK]`: Backend-only work (`main/hairline-backend/`)
   - `[BUG]`: Fix incorrect behavior in existing implementation
   - **CRITICAL**: Task name ends at descriptive name line; everything after is description

2. **Status**: `Drafted` (default), `Confirmed`, or `Added to Plane` (metadata line, not in HTML)

3. **Task Description** (under 500 words) with explicit markers. **CRITICAL**:
   - Descriptions must be in HTML format for Plane.so API (`description_html`)
   - **MUST** include `<h2>` header tags for major sections (Overview, Reference, Current Status, Expectation, Acceptance Criteria)
   - **MUST** include a persistent note in the Expectation section (marked as "Note (Suggestion)") clarifying that specifications are suggestions, focusing on business requirements and functional needs rather than technical implementation instructions, and that developers should use their expertise to choose the best approach
   - **CRITICAL - HTML Formatting Rules**:
     - Use `<p>` tag for **single paragraphs only**
     - Use `<ul>` / `<ol>` with `<li>` tags for **multiple items**
     - **DO NOT** use multiple `<p>` tags for multiple items
     - Use `<strong>`, `<code>`, `<a>`, etc. as needed
   - **NO excessive spacing**

```markdown
## TASK_NAME_START
[FE+BE TASK] OTP Expiration Implementation
## TASK_NAME_END

**Status**: Drafted

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>[What needs to be implemented - 2-3 sentences as a single paragraph]</p>
<h2>Reference</h2>
<p><a href="[PRD link with section anchor]">PRD Reference</a></p>
<h2>Current Status</h2>
<ul>
<li>[Existing component/file/endpoint]</li>
<li>[Add as many items as needed]</li>
</ul>
<h2>Expectation (Suggestion)</h2>
<p><strong>Note:</strong> The specifications provided below are suggestions based on business requirements. This section should focus on <strong>business requirements and functional needs</strong>, not technical implementation instructions. Developers should understand the business needs and use their expertise to choose the most beneficial and optimized implementation approach.</p>
<ul>
<li>[Requirement item]</li>
<li>[Add as many items as needed]</li>
</ul>
<h2>Acceptance Criteria</h2>
<ol>
<li>[Testable criterion]</li>
<li>[Add as many items as needed]</li>
</ol>
## TASK_DESCRIPTION_END
```

### Step 5: Categorize and Summarize

**MUST** categorize by: Module code (P-01, PR-01, A-01, etc.), FR number (FR-001, etc.), Priority (P1/P2/P3).

**MUST** include summary at end: Total tasks, status breakdown, priority distribution, next steps.

