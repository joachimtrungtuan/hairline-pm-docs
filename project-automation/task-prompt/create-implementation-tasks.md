---
description: Generate a date-stamped implementation task list (Plane-ready HTML) from gaps/conflicts found during checklist/FR verification.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## When To Use This Prompt

Use this prompt **ONLY** when the user explicitly asks to:

- Create implementation tasks from checklist verification gaps/conflicts, and/or
- Generate a Plane-ready implementation task list file.

If the user only wants to **update the checklist itself**, use: `local-docs/task-prompt/check-progress.md`.

## Required Inputs

**MUST** ask for these inputs (do not proceed without them):

1. **FR code** (e.g., `FR-001`, `FR-007B`)
2. **Optional**: Module code (e.g., `P-01`, `PR-02`, `A-04`, `S-03`) to scope work to one tenant/module
3. **Optional**: Checklist file path (used to extract the subflow list wording)
4. **Optional**: A pasted/typed subflow list (if no checklist is provided)
5. **Optional**: Figma file link (if provided by user)

**CRITICAL**:

- `FR_CODE` is mandatory for this prompt.
- If a same-day verification report exists (see Step 2), prefer it as the source of truth for codebase progress evidence.
- If the user explicitly requests tasks for a module-FR pair but does not provide `MODULE_CODE`, **DO NOT** proceed; ask them to confirm `MODULE_CODE`.

## Output Rules

- **MUST** create files under `local-docs/task-creation/{CURRENT_DATE}/`
- **MUST NOT** edit product code in this prompt (tasks only)
- **MUST NOT** change the checklist file unless the user explicitly asks
- **MUST** keep each task description concise and **under 300 words**
- **Scope rule**:
  - If `MODULE_CODE` is provided: only create tasks for that `(MODULE_CODE, FR_CODE)` scope.
  - If `MODULE_CODE` is not provided: create tasks for the **whole `FR_CODE`** scope (may include multiple modules).

## Execution Flow

### Step 1: Get Current Date

**MUST** get current date: Run `date +%Y-%m-%d`, store as `CURRENT_DATE`.

### Step 2: Check Same-Day Verification Reports (Highest Priority)

If a folder exists at `local-docs/task-creation/${CURRENT_DATE}/`, **MUST** scan all verification reports in that folder:

- `local-docs/task-creation/${CURRENT_DATE}/verification-report-${CURRENT_DATE}-*.md`

If one or more reports exist, **MUST** check each report for scope match:

- Prefer extracting from the report header lines (as created by `check-progress`):
  - `**Module**: ...`
  - `**FR**: ...`
  - If these lines are missing, fall back to string matching for `FR-...` and `P-/PR-/A-/S-...` codes.
- Match rules:
  - If `MODULE_CODE` is provided: choose a report that contains both `MODULE_CODE` and `FR_CODE`.
  - If `MODULE_CODE` is not provided: choose a report that contains `FR_CODE`.

If multiple reports match, select the newest by suffix (highest `###`) and load it as `VERIFICATION_REPORT_FILE`.

If no same-day verification report exists **or none match the requested scope**, proceed to Step 3.

### Step 3: Choose Task Basis (Priority Order)

Use the following priority, stopping at the first available source:

1. `VERIFICATION_REPORT_FILE` (from Step 2)
2. Subflow list from `CHECKLIST_FILE` (preferred) or a user-provided subflow list
3. The FR PRD itself (analyze and derive a coverage subflow list, then create tasks)

#### 3.1 Basis A: Verification Report (Preferred)

If `VERIFICATION_REPORT_FILE` exists:

- Use it as evidence for what is missing/incomplete and what was appended/rewritten.
- Create tasks to ensure completeness of the system for the requested scope.

#### 3.2 Basis B: Checklist Subflow List (If No Same-Day Report)

If no same-day report matches and `CHECKLIST_FILE` is provided:

- Load the checklist file.
- If `MODULE_CODE` is provided, extract only the row for `(MODULE_CODE, FR_CODE)` and use the “Key Sub-Flows / Completion Items” cell as the subflow list basis.
- If `MODULE_CODE` is not provided, extract all rows that reference `FR_CODE` and create tasks per row (do not merge tenants).

If no checklist is provided but the user pasted a subflow list:

- Use that list as the subflow basis (keep it concise; do not invent extra scope beyond what the FR PRD supports).
- If both checklist and pasted subflows exist, prefer checklist wording and use pasted subflows only to fill obvious gaps.

#### 3.3 Basis C: FR PRD Coverage (If No Report and No Checklist)

If neither a matching same-day report nor a checklist is available:

- Locate the FR PRD locally via `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`.
- Check PRD structure first (headers), then process main sections one-by-one.
- Derive a concise “coverage subflow list” (minimum required subflows/screens/business requirements for the FR).
- Create tasks from that list to ensure FR coverage.

### Step 4: Create Directory Structure and Files

**MUST** create date-based subfolder first: `local-docs/task-creation/{CURRENT_DATE}/` (create if doesn't exist).

**CRITICAL**: Do not overwrite old files. Use an incremental suffix.

1. If the date folder does not exist, create it and start with suffix `001`.
2. If the date folder exists, list existing files and pick the next available suffix.
3. If there are no existing `implementation-tasks-{CURRENT_DATE}-*.md` files, use `001`.

Recommended approach:

- Find the highest existing suffix across:
  - `implementation-tasks-{CURRENT_DATE}-*.md`
  - `verification-report-{CURRENT_DATE}-*.md`
  Then increment it by 1.
- Format suffix as 3 digits: `001`, `002`, `003`, ...

Example (one possible approach):

```bash
mkdir -p "local-docs/task-creation/${CURRENT_DATE}"
ls "local-docs/task-creation/${CURRENT_DATE}"/implementation-tasks-"${CURRENT_DATE}"-*.md 2>/dev/null
ls "local-docs/task-creation/${CURRENT_DATE}"/verification-report-"${CURRENT_DATE}"-*.md 2>/dev/null
```

SEQ derivation rule:

- If there are **no matching files** for either pattern, set `SEQ=001`.
- Otherwise, extract the highest 3-digit suffix across both patterns and increment it by 1 (keep 3 digits).

Then create files:

1. `implementation-tasks-{CURRENT_DATE}-{SEQ}.md` - Implementation tasks (Plane-ready)

### Step 5: Create Implementation Tasks

For **EACH** missing/incomplete component, **MUST** create a task with:

1. **Task Name**: Start with prefix `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, or `[BUG]` + descriptive name
   - `[FE+BE TASK]`: UI + API work
   - `[FE TASK]`: UI-only work (React in `main/hairline-frontend/` or Flutter in `main/hairline-app/`, depending on module)
   - `[BE TASK]`: Backend-only work (`main/hairline-backend/`)
   - `[BUG]`: Fix incorrect behavior in existing implementation
   - **CRITICAL**: Task name ends at descriptive name line; everything after is description

2. **Status**: `Drafted` (default), `Confirmed`, or `Added to Plane` (metadata line, not in HTML)
   - Also include: `**FR**: {FR_CODE}` always
   - Also include: `**Module**: {MODULE_CODE}` when determinable; otherwise use `**Module**: TBD` (for whole-FR tasking where module isn’t known yet)

3. **Task Description** (under 300 words) with explicit markers. **CRITICAL**:
   - Descriptions must be in HTML format for Plane.so API (`description_html`)
   - **MUST** include `<h2>` header tags for major sections (Overview, Reference, Current Status, Expectation, Acceptance Criteria)
   - **MUST** include a persistent note in the Expectation section (marked as "Note (Suggestion)") clarifying that specifications are suggestions, focusing on business requirements and functional needs rather than technical implementation instructions, and that developers should use their expertise to choose the best approach
   - **MUST** keep the full description concise and **under 300 words**
   - Keep lists short:
     - Current Status: prefer ≤5 `<li>`
     - Expectation: prefer ≤7 `<li>`
     - Acceptance Criteria: prefer ≤5 `<li>`
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
**FR**: FR-###
**Module**: P-## (or TBD)

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>[What needs to be implemented - 2-3 sentences as a single paragraph]</p>
<h2>Reference</h2>
<ul>
<li><a href="[GitHub FR PRD link with section anchor]">FR PRD</a></li>
<li><a href="[Figma file link]">Figma</a> (include only if provided)</li>
</ul>
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

### Step 6: Categorize and Summarize

**MUST** categorize by: Module code (P-01, PR-01, A-01, etc.), FR number (FR-001, etc.), Priority (P1/P2/P3).

**MUST** include summary at end: Total tasks, status breakdown, priority distribution, next steps.

## Reference Link Rules

- **MUST** use GitHub links in the task Reference section (not local file paths).
- **Default reference rule**: In each task, include **only** the FR PRD GitHub link (plus Figma if provided).
- Add other high-level docs (System PRD, transcriptions, etc.) **only when needed** for that specific task and only if they materially clarify scope/requirements.
- For the FR PRD link, use the same path as the local PRD but under GitHub `blob/main/` and include a section anchor when possible:
  - Base: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/`
  - Example shape: `.../project-requirements/functional-requirements/fr001-*/prd.md#section-anchor`
- If a Figma link is provided by the user, include it as an additional reference item; otherwise omit it.

## References

**GitHub Documentation**:

- FR PRDs: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr###-*/prd.md`
- Client Transcriptions (use only when needed): `https://github.com/joachimtrungtuan/hairline-pm-docs/tree/main/project-requirements/transcriptions`
- System PRD (use only when needed): `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/system-prd.md`
