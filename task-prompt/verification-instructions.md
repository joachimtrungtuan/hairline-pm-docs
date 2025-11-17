---
description: Verify module progress checklist accuracy by cross-checking each subflow against the actual codebase implementation.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

**CRITICAL**: The user will specify which checklist file to verify in their prompt. The file path will be provided in `$ARGUMENTS`. If no file is specified, you **MUST** ask the user to provide the checklist file path.

## Outline

Verify module progress checklist accuracy by cross-checking subflows against codebase implementation:

1. **Codebase Analysis**: Search for API endpoints, controllers, models, and frontend components
2. **Status Validation**: Compare checklist status (✅/🟨/🟥) against actual implementation
3. **Gap Identification**: Document discrepancies, missing features, and implementation conflicts
4. **Task Generation**: Create implementation tasks for missing components

## Execution Flow

### Step 1: Parse User Input and Load Required Files

**MUST** first parse the user input to extract:

1. **Checklist File Path**: The file path to the checklist that needs verification
   - Extract from `$ARGUMENTS` or user prompt
   - If not provided, **MUST** ask user: "Please specify the checklist file path to verify"
   - Validate file exists before proceeding
   - Store as `CHECKLIST_FILE` variable

**MUST** then load these files (use absolute paths; convert relative paths to absolute):

1. `CHECKLIST_FILE` - Checklist to verify - **REQUIRED**
2. `.specify/memory/constitution.md` - Module code definitions and architecture - **REQUIRED**
3. `local-docs/project-requirements/system-prd.md` - System-level requirements and FR definitions - **REQUIRED**
   - GitHub: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/system-prd.md`
4. `local-docs/project-requirements/transcriptions/*.txt` - All transcription files for client requirements - **REQUIRED**
   - GitHub: `https://github.com/joachimtrungtuan/hairline-pm-docs/tree/main/project-requirements/transcriptions`

### Step 2: Understand Status Symbols

**CRITICAL**: Status definitions:

- ✅ **Completed** (≥90%): Fully implemented, functional, matches PRD, no critical bugs
- 🟨 **Partially Implemented** (≥50%): Core functionality exists but missing edge cases, validation, or non-critical features
- 🟥 **Not Yet Implemented** (<50%): No implementation found, only placeholders/stubs, or feature missing from codebase

### Step 3: Verification Methodology

**CRITICAL**: Determine module type first - verification scope depends on type:

- **Patient (P-*)**: Backend API only (mobile app is separate project)
- **Provider (PR-*)**: Backend API + Frontend components in `main/hairline-frontend/`
- **Admin (A-*)**: Backend API + Frontend components in `main/hairline-frontend/`
- **Shared Services (S-*)**: Backend only

For **EACH** subflow item, perform checks based on module type:

#### 3.1 Backend Verification (ALL Modules)

**MUST** verify for all modules:

1. **API Routes**: Search `main/hairline-backend/routes/api.php` - document path, HTTP method, controller method
2. **Controller Methods**: Verify in `main/hairline-backend/app/Http/Controllers/` - method exists, implemented (not stub), has validation/error handling/business logic
3. **Model Relationships**: Check `main/hairline-backend/app/Models/` - relationships correct, migrations include required tables/columns
4. **Functionality**: Verify response structure, authentication/authorization middleware, error handling, validation rules

#### 3.2 Frontend Verification (Provider & Admin Modules ONLY)

**CRITICAL**: **DO NOT** verify frontend for Patient modules (P-*) - mobile app is separate project.

**MUST** verify for Provider (PR-*) and Admin (A-*) modules:

1. **React Components**: Search `main/hairline-frontend/src/` - component exists, not placeholder
2. **API Integration**: Verify API calls (`useQuery`, `useMutation`, `fetch`, `axios`) match backend endpoints, proper error handling
3. **UI Components**: Verify UI matches PRD, complete workflows/forms, correct navigation/routing
4. **User Experience**: Check loading states, error messages, success feedback, form validation

#### 3.3 Cross-Reference Verification

**MUST** cross-reference:

1. **PRD Documents**: Load from `local-docs/project-requirements/functional-requirements/fr###-*/prd.md` - compare checklist with PRD, verify implementation matches
   - GitHub: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr###-*/prd.md`
2. **System Technical Spec**: Check `local-docs/project-requirements/system-technical-spec.md` if available - verify API structure matches
3. **System PRD & Client Requirements**: Verify module codes/FR numbers match system PRD, align with client transcriptions, identify discrepancies
   - System PRD GitHub: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/system-prd.md`
   - Transcriptions GitHub: `https://github.com/joachimtrungtuan/hairline-pm-docs/tree/main/project-requirements/transcriptions`

### Step 4: Status Assessment

For **EACH** subflow item, **MUST** determine correct status based on module type:

**Common Criteria**:

- ✅ **Completed**: All required components exist, functional, match PRD, proper validation/error handling/auth, no critical bugs
- 🟨 **Partially Implemented**: Core functionality exists (≥50%) but missing edge cases, validation, or non-critical features
- 🟥 **Not Yet Implemented**: No implementation found, only placeholders/stubs, or <50% complete

**Module-Specific Requirements**:

- **Patient (P-*)**: Backend API only - verify endpoints, controllers, business logic (frontend NOT required)
- **Provider/Admin (PR-*, A-*)**: Backend API + Frontend - verify both complete, API integration works
- **Shared Services (S-*)**: Backend only - verify service implementation, methods, integration points

**CRITICAL**: If checklist status differs from actual implementation, document as a **CONFLICT**.

### Step 5: Document Findings

For **EACH** subflow item, **MUST** document:

1. **Alignment**: "✅ Verified: [feature] - Status matches implementation"
2. **Gaps**: "❌ Gap: [feature] - Checklist shows ✅ but code missing" or "⚠️ Gap: [feature] - Checklist shows 🟨 but should be 🟥"
3. **Conflicts**: "🔴 Conflict: [feature] - Checklist: ✅, Actual: 🟥" or "🟡 Conflict: [feature] - Checklist: 🟨, Actual: ✅"
4. **Recommendations**: "📝 Recommendation: Update [feature] from ✅ to 🟨"

### Step 6: Get Current Date and Generate Verification Report

**MUST** get current date: Run `date +%Y-%m-%d`, store as `CURRENT_DATE` (or use system date/derive from `CHECKLIST_FILE`). Used for:

- Subfolder: `local-docs/task-creation/{CURRENT_DATE}/`
- Files: `verification-report-{CURRENT_DATE}.md`, `implementation-tasks-{CURRENT_DATE}.md`

**MUST** create brief report (under 500 words) with:

1. **Summary**: Total verified, alignment percentage, top 3 critical gaps
2. **Alignment Findings**: Modules matching implementation (codes/FR numbers), 100% alignment modules
3. **Gap Analysis**: Missing features marked complete, incomplete marked done, incorrect status indicators
4. **Conflict Resolution**: All discrepancies, status update recommendations with justification, priority (High/Medium/Low)
5. **Next Steps**: Top 5 priority items, modules needing re-verification, task creation requirements

### Step 7: Create Directory Structure and Files

**CRITICAL**: **MUST** create date-based subfolder first: `local-docs/task-creation/{CURRENT_DATE}/` (create if doesn't exist, use absolute paths). Then create files inside:

1. `verification-report-{CURRENT_DATE}.md` - Verification report
2. `implementation-tasks-{CURRENT_DATE}.md` - Implementation tasks

#### 7.1 Task Structure

For **EACH** missing component, **MUST** create a task with:

1. **Task Name**: Start with prefix `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, or `[BUG]` + descriptive name
   - `[FE+BE TASK]`: Both frontend and backend work
   - `[FE TASK]`: Frontend-only
   - `[BE TASK]`: Backend-only
   - `[BUG]`: Fix existing issues
   - **CRITICAL**: Task name ends at descriptive name line; everything after is description

2. **Status**: `Drafted` (default), `Confirmed`, or `Added to Plane` - part of metadata, not description

3. **Task Description** (under 500 words) with explicit markers. **CRITICAL**:
   - Descriptions must be in HTML format for Plane.so API (`description_html` field)
   - **MUST** include `<h2>` header tags for major sections (e.g., Overview, Reference, Current Status, Expectation, Acceptance Criteria)
   - **MUST** include a persistent note in the Expectation section (marked as "Note (Suggestion)") clarifying that specifications are suggestions, focusing on business requirements and functional needs rather than technical implementation instructions, and that developers should use their expertise to choose the best approach
   - Use HTML tags like `<p>`, `<strong>`, `<code>`, `<ul>`, `<li>`, etc.
   - **NO excessive spacing** - remove unnecessary blank lines and whitespace

   ```markdown
   ## TASK_NAME_START
   [FE+BE TASK] OTP Expiration Implementation
   ## TASK_NAME_END
   
   **Status**: Drafted
   
   ## TASK_DESCRIPTION_START
   <h2>Overview</h2>
   <p>[What needs to be implemented - 2-3 sentences]</p>
   <h2>Reference</h2>
   <p><a href="[GitHub PRD link with section anchor, e.g., https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr001-patient-authentication/prd.md#workflow-1-patient-registration-primary-flow]">PRD Reference</a></p>
   <h2>Current Status</h2>
   <p>[What exists now - specific file paths/endpoints]</p>
   <h2>Expectation (Suggestion)</h2>
   <p><strong>Note:</strong> The specifications provided below are suggestions based on business requirements. This section should focus on <strong>business requirements and functional needs</strong>, not technical implementation instructions. Developers should understand the business needs and use their expertise to choose the most beneficial and optimized implementation approach.</p>
   <p>[What should be implemented - detailed requirements]</p>
   <h2>Acceptance Criteria</h2>
   <p>[How to verify completion - specific, testable criteria]</p>
   ## TASK_DESCRIPTION_END
   ```

   **Alternative Format** (if markers not used):
   - Task name: Heading text after `###` (including prefix)
   - Description: Starts after `**Description**:` line until next task heading

#### 7.2 Task Categories & Summary

**MUST** categorize by: Module code (P-01, PR-01, A-01, etc.), FR number (FR-001, etc.), Priority (P1/P2/P3)

**MUST** include summary at end: Total tasks, status breakdown, priority distribution, next steps

### Step 8: Tools and Commands Reference

**Backend Search**:

```bash
grep -r "Route::" main/hairline-backend/routes/
find main/hairline-backend/app/Http/Controllers -name "*Controller.php"
find main/hairline-backend/app/Models -name "*.php"
```

**Frontend Search** (Provider/Admin ONLY - **DO NOT** search frontend for Patient modules):

```bash
find main/hairline-frontend/src -name "*.jsx" -o -name "*.tsx"
grep -r "useQuery\|useMutation\|fetch\|axios" main/hairline-frontend/src
```

**Semantic Search**: Use for API endpoints, component patterns, missing features, related functionality

**Directory Creation**:

```bash
CURRENT_DATE=$(date +%Y-%m-%d)
mkdir -p "local-docs/task-creation/${CURRENT_DATE}"
```

### Step 9: Verification Checklist Template

**MUST** use appropriate checklist based on module type:

**Patient (P-*) - Backend Only**: API endpoint exists, controller implemented (not stub), model relationships correct, migrations complete, error handling, validation matches PRD, auth middleware, status matches checklist

**Provider/Admin (PR-*, A-*) - Backend + Frontend**: All backend checks above + frontend component exists, API integration complete, error handling (both), validation (both), status matches checklist

**Shared Services (S-*) - Backend Only**: Service implementation exists, methods implemented (not stubs), integration points correct, error handling, business logic matches PRD, status matches checklist

**CRITICAL**: If any item unchecked, document as gap or conflict.

### Step 10: Report Completion

**MUST** report completion with:

1. **Source Information**: Checklist file path, System PRD, client transcriptions
2. **Verification Summary**: Total verified, alignment percentage, conflicts count, gaps count
3. **Files Created**: Verification report and implementation tasks paths (in date subfolder)
4. **Key Findings**: Top 3 critical gaps, top 3 conflicts, priority recommendations
5. **Next Steps**: Review report, confirm tasks, update checklist if needed

## Important Notes

- Focus on P1 modules first (highest priority)
- Verify against actual code, not documentation
- **CRITICAL**: Understand module type - Patient (P-*): backend only; Provider/Admin (PR-*, A-*): backend + frontend; Shared (S-*): backend only
- Document discrepancies clearly, reference specific file paths/line numbers
- If unsure about status, mark as 🟨 and document uncertainty

## Error Handling

If verification cannot be completed: Document missing files, mark unclear implementations as 🟨, document conflicting sources, note codebase accessibility limitations

## Quality Assurance

Before completing, **MUST** ensure: All P1 modules verified, conflicts/gaps documented with references, report under 500 words, tasks follow template, task descriptions under 500 words, correct task prefixes, absolute file paths

## References

**GitHub Documentation**:

- System PRD: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/system-prd.md`
- Functional Requirements PRDs: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr###-*/prd.md` (replace `###` with FR number, e.g., `fr001-patient-authentication/prd.md`)
- Client Transcriptions: `https://github.com/joachimtrungtuan/hairline-pm-docs/tree/main/project-requirements/transcriptions`
