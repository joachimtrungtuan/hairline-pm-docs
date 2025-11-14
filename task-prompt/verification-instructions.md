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

The user wants to verify the accuracy of a module progress checklist file by cross-checking each subflow against the actual codebase implementation. The specific checklist file to verify will be specified in the user's prompt. This process involves:

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

**MUST** then load the following files:

1. `CHECKLIST_FILE` - The checklist to verify (from user input) - **REQUIRED**
2. `.specify/memory/constitution.md` - For module code definitions and architecture principles - **REQUIRED**
3. `local-docs/project-requirements/system-prd.md` - For system-level requirements and FR definitions - **REQUIRED**
4. `local-docs/project-requirements/transcriptions/` - All transcription files for client requirements alignment - **REQUIRED**
   - Load all `.txt` files in this directory
   - Files include: HairlineOverview.txt, HairlineApp-Part1.txt, HairlineApp-Part2.txt, Hairline-AdminPlatform-Part1.txt, Hairline-AdminPlatformPart2.txt, Hairline-ProviderPlatformPart1.txt, Hairline-ProviderPlatformPart2.txt

**IMPORTANT**: All file paths **MUST** be absolute paths. If user provides relative path, convert to absolute path based on workspace root.

### Step 2: Understand Status Symbols

**CRITICAL**: Understand these status definitions before verification:

- ✅ **Completed**: Feature is fully implemented and functional (≥90% complete)
  - All API endpoints exist and are functional
  - Frontend components are implemented and connected
  - Business logic matches PRD requirements
  - No critical bugs or missing features

- 🟨 **In Progress / Partially Implemented**: Feature is partially implemented (≥50% complete) but missing some functionality
  - Core functionality exists but missing edge cases
  - Backend implemented but frontend incomplete (or vice versa)
  - Feature works but missing validation/error handling
  - Missing non-critical sub-features

- 🟥 **Not Yet Implemented**: Feature is not implemented or below 50% complete
  - No API endpoints found
  - No frontend components found
  - Feature mentioned in PRD but not in codebase
  - Only placeholders or stubs exist

### Step 3: Verification Methodology

**CRITICAL**: Verification scope depends on module type. **MUST** determine module type first:

- **Patient Modules (P-01, P-02, P-03, etc.)**: Patient mobile app - **ONLY verify backend API endpoints** (frontend is separate mobile app project, not in this codebase)
- **Provider Modules (PR-01, PR-02, PR-03, etc.)**: Provider web dashboard - **Verify both backend API endpoints AND frontend components** in `main/hairline-frontend/`
- **Admin Modules (A-01, A-02, A-03, etc.)**: Admin web dashboard - **Verify both backend API endpoints AND frontend components** in `main/hairline-frontend/`
- **Shared Services (S-01, S-02, S-03, etc.)**: Backend services - **ONLY verify backend implementation**

For **EACH** subflow item in the checklist, perform these checks based on module type:

#### 3.1 Backend Verification (ALL Modules)

**MUST** verify for all modules:

1. **API Routes**:
   - Search `main/hairline-backend/routes/api.php` for relevant routes
   - Use `grep` or semantic search to find route definitions
   - Document route path, HTTP method, and controller method
   - **IMPORTANT**: For Patient modules, verify patient-facing API endpoints exist

2. **Controller Methods**:
   - Locate controller file in `main/hairline-backend/app/Http/Controllers/`
   - Verify method exists and is implemented (not just a stub)
   - Check for proper validation, error handling, and business logic
   - For Patient modules: Check `PatientController`, `InquiryController`, `QuotesController`, etc.
   - For Provider modules: Check provider-specific controllers
   - For Admin modules: Check admin-specific controllers

3. **Model Relationships**:
   - Check model files in `main/hairline-backend/app/Models/`
   - Verify relationships are defined correctly
   - Check database migrations for required tables/columns

4. **Functionality**:
   - Verify endpoint returns expected response structure
   - Check for proper authentication/authorization middleware
   - Verify error handling and validation rules

#### 3.2 Frontend Verification (Provider & Admin Modules ONLY)

**MUST** verify **ONLY** for Provider (PR-*) and Admin (A-*) modules:

**CRITICAL**: **DO NOT** verify frontend for Patient modules (P-*) - patient mobile app is a separate project.

1. **React Components**:
   - Search `main/hairline-frontend/src/` for component files
   - Use `find` command or semantic search: `find main/hairline-frontend/src -name "*.jsx" -o -name "*.tsx"`
   - Verify component exists and is not just a placeholder
   - **Provider modules**: Look for provider dashboard components
   - **Admin modules**: Look for admin dashboard components

2. **API Integration**:
   - Search for API calls: `grep -r "useQuery\|useMutation\|fetch\|axios" main/hairline-frontend/src`
   - Verify API endpoints are called correctly
   - Check for proper error handling in API calls
   - Verify API calls match backend endpoints found in Step 3.1

3. **UI Components**:
   - Verify UI matches PRD specifications (if PRD available)
   - Check for missing UI workflows or incomplete forms
   - Verify navigation and routing is correct

4. **User Experience**:
   - Check for loading states, error messages, success feedback
   - Verify form validation on frontend
   - Check for missing user interactions

#### 3.3 Cross-Reference Verification

**MUST** cross-reference:

1. **PRD Documents**:
   - Load relevant PRD from `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`
   - Compare checklist item with PRD requirements
   - Verify implementation matches PRD specifications

2. **System Technical Spec**:
   - Check `local-docs/project-requirements/system-technical-spec.md` if available
   - Verify API structure matches technical spec

3. **System PRD & Client Requirements**:
   - Cross-reference with `system-prd.md` for system-level requirements and FR definitions
   - Cross-reference with transcription files for original client requirements
   - Verify checklist items align with client's stated requirements from transcriptions
   - Verify module codes and FR numbers match system PRD definitions
   - Identify any discrepancies between checklist and original client requirements

### Step 4: Status Assessment

For **EACH** subflow item, **MUST** determine correct status based on module type:

#### 4.1 Patient Modules (P-*) - Backend API Only

**Mark as ✅ (Completed)** if:

- All required API endpoints exist and are functional
- Controller methods are fully implemented (not stubs)
- Business logic matches PRD requirements
- Proper validation, error handling, and authentication
- No critical bugs or missing features
- **Note**: Frontend verification NOT required (mobile app is separate project)

**Mark as 🟨 (Partially Implemented)** if:

- Core API endpoints exist but missing some endpoints
- Endpoints exist but missing validation/error handling
- Business logic partially matches PRD requirements
- Missing non-critical API endpoints
- **AND** at least 50% of required endpoints are complete

**Mark as 🟥 (Not Yet Implemented)** if:

- No API endpoints found
- Only placeholder/stub endpoints exist
- Feature mentioned in PRD but no backend implementation
- **OR** less than 50% of required endpoints are complete

#### 4.2 Provider & Admin Modules (PR-*, A-*) - Backend + Frontend

**Mark as ✅ (Completed)** if:

- All required API endpoints exist and are functional
- All required frontend components exist and are connected
- API integration is complete (frontend calls correct endpoints)
- Business logic matches PRD requirements
- No critical bugs or missing features
- **AND** both backend and frontend are complete

**Mark as 🟨 (Partially Implemented)** if:

- Backend implemented but frontend incomplete (or vice versa)
- Core functionality exists but missing edge cases
- Feature works but missing validation/error handling
- Missing non-critical sub-features
- **AND** at least 50% of functionality is complete

**Mark as 🟥 (Not Yet Implemented)** if:

- No API endpoints found AND no frontend components found
- Only placeholders or stubs exist
- Feature mentioned in PRD but not in codebase
- **OR** less than 50% of functionality is complete

#### 4.3 Shared Services (S-*) - Backend Only

**Mark as ✅ (Completed)** if:

- Service implementation exists and is functional
- Service methods are fully implemented
- Business logic matches PRD requirements
- Proper error handling and integration points
- No critical bugs or missing features

**Mark as 🟨 (Partially Implemented)** if:

- Core service functionality exists but missing edge cases
- Service works but missing validation/error handling
- Missing non-critical service methods
- **AND** at least 50% of functionality is complete

**Mark as 🟥 (Not Yet Implemented)** if:

- No service implementation found
- Only placeholders or stubs exist
- Feature mentioned in PRD but not in codebase
- **OR** less than 50% of functionality is complete

**CRITICAL**: If checklist status differs from actual implementation, document as a **CONFLICT**.

### Step 5: Document Findings

For **EACH** subflow item, **MUST** document:

1. **Alignment**: Features where checklist status matches actual implementation
   - Note: "✅ Verified: [feature name] - Status matches implementation"

2. **Gaps**: Missing implementations not reflected in checklist
   - Note: "❌ Gap: [feature name] - Checklist shows ✅ but code is missing"
   - Note: "⚠️ Gap: [feature name] - Checklist shows 🟨 but should be 🟥"

3. **Conflicts**: Discrepancies between checklist and codebase
   - Note: "🔴 Conflict: [feature name] - Checklist: ✅, Actual: 🟥"
   - Note: "🟡 Conflict: [feature name] - Checklist: 🟨, Actual: ✅"

4. **Recommendations**: Status updates needed for checklist
   - Note: "📝 Recommendation: Update [feature name] from ✅ to 🟨"

### Step 6: Get Current Date and Generate Verification Report

**MUST** first get the current date (if not already obtained):

1. **Get Current Date**:
   - Run command: `date +%Y-%m-%d` to get current date in YYYY-MM-DD format
   - Store result as `CURRENT_DATE` variable
   - **Alternative**: If command not available, use system date or derive from `CHECKLIST_FILE` name pattern if it contains date
   - **Note**: This date will be used for both verification report and implementation tasks filenames

**MUST** then create a brief report (under 500 words) with these sections:

#### 6.1 Summary Section

**MUST** include:

- Total modules/subflows verified (count)
- Overall alignment percentage (aligned items / total items × 100)
- Critical gaps identified (count and list top 3)

#### 6.2 Alignment Findings

**MUST** list:

- Modules where status matches implementation (list module codes and FR numbers)
- Highlight well-documented progress areas
- Note any modules with 100% alignment

#### 6.3 Gap Analysis

**MUST** document:

- Missing features marked as completed (list with module/FR reference)
- Incomplete implementations marked as done (list with details)
- Features with incorrect status indicators (list current vs correct status)

#### 6.4 Conflict Resolution

**MUST** include:

- All discrepancies between checklist and codebase (list each conflict)
- Specific recommendations for status updates (with justification)
- Priority level for each conflict (High/Medium/Low)

#### 6.5 Next Steps

**MUST** specify:

- Priority items requiring immediate attention (list top 5)
- Modules needing re-verification (list module codes)
- Task creation requirements (reference to Step 7)

**CRITICAL**: Report **MUST** be under 500 words total. Be concise but comprehensive.

### Step 7: Create Implementation Tasks File

**MUST** create `implementation-tasks-{CURRENT_DATE}.md` file in `local-docs/task-creation/` directory.

**Note**: `CURRENT_DATE` variable should already be set from Step 6. If not set, get current date using `date +%Y-%m-%d` command.

**Example**: If current date is 2025-11-14, file should be `implementation-tasks-2025-11-14.md`

#### 7.1 Task Structure

For **EACH** missing component identified, **MUST** create a task with:

1. **Task Name**:
   - **MUST** start with prefix: `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, or `[BUG]`
   - Prefix selection rules:
     - `[FE+BE TASK]`: Requires both frontend and backend work
     - `[FE TASK]`: Frontend-only implementation
     - `[BE TASK]`: Backend-only implementation
     - `[BUG]`: Fix existing implementation issues
   - Follow with descriptive name (e.g., "OTP Expiration Implementation")

2. **Status**:
   - **MUST** be one of: `Drafted`, `Confirmed`, or `Added to Plane`
   - Default to `Drafted` for new tasks

3. **Description** (under 500 words):
   - **MUST** follow this template:

   ```markdown
   **Overview**: [What needs to be implemented - 2-3 sentences]
   **Reference**: [PRD document path and/or Figma link if available]
   **Current Status**: [What exists now - be specific with file paths/endpoints]
   **Expectation**: [What should be implemented - detailed requirements]
   **Acceptance Criteria**: [How to verify completion - specific, testable criteria]
   ```

#### 7.2 Task Categories

**MUST** categorize tasks by:

- Module code (P-01, P-02, PR-01, A-01, etc.)
- Functional Requirement (FR-001, FR-003, etc.)
- Priority (P1, P2, P3 based on module priority)

#### 7.3 Task Summary

**MUST** include at end of file:

- Total tasks created (count)
- Status breakdown (Drafted/Confirmed/Added to Plane counts)
- Priority distribution (P1/P2/P3 counts)
- Next steps for task management

### Step 8: Tools and Commands Reference

**MUST** use these tools for verification:

#### 8.1 Backend Search

```bash
# Search for routes
grep -r "Route::" main/hairline-backend/routes/

# Search for specific route pattern
grep -r "patient-register\|activate-patient" main/hairline-backend/routes/

# Find controllers
find main/hairline-backend/app/Http/Controllers -name "*Controller.php"

# Search for models
find main/hairline-backend/app/Models -name "*.php"

# Search for specific method
grep -r "function patientRegister\|function patientActivation" main/hairline-backend/app/Http/Controllers/
```

#### 8.2 Frontend Search (Provider & Admin Modules ONLY)

**CRITICAL**: **ONLY** use these commands for Provider (PR-*) and Admin (A-*) modules. **DO NOT** search frontend for Patient modules (P-*).

```bash
# Find components
find main/hairline-frontend/src -name "*.jsx" -o -name "*.tsx"

# Search for API calls
grep -r "useQuery\|useMutation\|fetch\|axios" main/hairline-frontend/src

# Search for specific component usage (Provider/Admin specific)
grep -r "ProviderDashboard\|AdminDashboard" main/hairline-frontend/src
```

#### 8.3 Semantic Search

**MUST** use semantic search for:

- API endpoint implementations
- Component usage patterns
- Missing feature implementations
- Related functionality across codebase

**Example queries**:

- **Patient Modules (P-*)**: "Where is patient registration API endpoint implemented?" (backend only)
- **Patient Modules (P-*)**: "Where are OTP verification endpoints for patient activation?" (backend only)
- **Provider/Admin Modules (PR-*, A-*)**: "Where is the provider quote management component?" (frontend)
- **Provider/Admin Modules (PR-*, A-*)**: "Where is the admin patient management dashboard?" (frontend)

### Step 9: Verification Checklist Template

**MUST** use appropriate checklist based on module type:

#### 9.1 Patient Modules (P-*) - Backend API Only

- [ ] Backend API endpoint exists
- [ ] Controller method implemented (not stub)
- [ ] Model relationships correct
- [ ] Database migrations include required tables/columns
- [ ] Error handling present
- [ ] Validation rules match PRD
- [ ] Authentication/authorization middleware correct
- [ ] Status matches checklist

**Note**: Frontend verification NOT required for Patient modules (mobile app is separate project).

#### 9.2 Provider & Admin Modules (PR-*, A-*) - Backend + Frontend

- [ ] Backend API endpoint exists
- [ ] Controller method implemented (not stub)
- [ ] Model relationships correct
- [ ] Database migrations include required tables/columns
- [ ] Frontend component exists (in `main/hairline-frontend/src/`)
- [ ] API integration complete (frontend calls backend endpoints)
- [ ] Error handling present (both BE and FE)
- [ ] Validation rules match PRD (both BE and FE)
- [ ] Authentication/authorization middleware correct
- [ ] Status matches checklist

#### 9.3 Shared Services (S-*) - Backend Only

- [ ] Service implementation exists
- [ ] Service methods implemented (not stubs)
- [ ] Integration points correct
- [ ] Error handling present
- [ ] Business logic matches PRD
- [ ] Status matches checklist

**CRITICAL**: If any item is unchecked, document as gap or conflict.

### Step 10: Output Files

**MUST** create these files:

1. **Verification Report**:
   - File: `local-docs/task-creation/verification-report-{CURRENT_DATE}.md`
   - **MUST** use `CURRENT_DATE` variable obtained in Step 6
   - Format: Brief summary (under 500 words) of alignments, gaps, and conflicts
   - **MUST** include all sections from Step 6
   - **MUST** reference the source checklist file in the report header

2. **Implementation Tasks**:
   - File: `local-docs/task-creation/implementation-tasks-{CURRENT_DATE}.md`
   - Format: List of all missing component tasks
   - **MUST** follow structure from Step 7
   - **MUST** reference the source checklist file in the file header
   - **MUST** include date in filename using `CURRENT_DATE` variable

### Step 11: Report Completion

**MUST** report completion with:

1. **Source Information**:
   - Checklist file verified: `CHECKLIST_FILE` (absolute path)
   - System PRD referenced: `local-docs/project-requirements/system-prd.md`
   - Client transcriptions referenced: `local-docs/project-requirements/transcriptions/` (all files)

2. **Verification Summary**:
   - Total items verified
   - Alignment percentage
   - Conflicts found (count)
   - Gaps identified (count)

3. **Files Created**:
   - Verification report path (absolute): `local-docs/task-creation/verification-report-{CURRENT_DATE}.md`
   - Implementation tasks path (absolute): `local-docs/task-creation/implementation-tasks-{CURRENT_DATE}.md`

4. **Key Findings**:
   - Top 3 critical gaps
   - Top 3 conflicts requiring resolution
   - Priority recommendations

5. **Next Steps**:
   - Review verification report
   - Confirm implementation tasks
   - Update checklist status if needed

## Important Notes

- **Focus on P1 modules first** (highest priority)
- **Verify against actual code**, not documentation
- **CRITICAL**: Understand module type before verification:
  - **Patient modules (P-*)**: Only verify backend API endpoints (mobile app is separate project)
  - **Provider modules (PR-*)**: Verify both backend API and frontend dashboard components
  - **Admin modules (A-*)**: Verify both backend API and frontend dashboard components
  - **Shared services (S-*)**: Only verify backend service implementation
- **Document discrepancies clearly** for task creation
- **Reference specific file paths and line numbers** when possible
- **Be thorough but efficient** - don't skip verification steps
- **If unsure about status**, mark as 🟨 (Partially Implemented) and document uncertainty

## Error Handling

If verification cannot be completed:

1. **Missing Files**: Document which files are missing and why verification cannot proceed
2. **Unclear Implementation**: Mark as 🟨 and document what needs clarification
3. **Conflicting Information**: Document all conflicting sources and recommend resolution
4. **Incomplete Codebase**: Note what percentage of codebase was accessible and limitations

## Quality Assurance

Before completing verification, **MUST** ensure:

- [ ] All P1 modules verified
- [ ] All conflicts documented with specific references
- [ ] All gaps identified with file paths/endpoints
- [ ] Verification report is under 500 words
- [ ] Implementation tasks follow template structure
- [ ] All task descriptions are under 500 words
- [ ] Task prefixes are correct ([FE+BE TASK], [FE TASK], [BE TASK], [BUG])
- [ ] File paths are absolute paths
