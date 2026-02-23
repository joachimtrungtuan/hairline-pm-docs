---
description: Comprehensive FR verification against constitution, system PRD, and client requirements with gap analysis and recommendations.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

**CRITICAL**: The user will specify which FR to verify in their prompt. If no FR number is specified, you **MUST** ask the user to provide the FR number (e.g., "FR-001", "FR-011", etc.).

## Outline

Perform comprehensive cross-check and analysis of a Functional Requirement (FR) against:

1. **Constitution Compliance**: Verify alignment with platform principles and architecture
2. **System PRD Alignment**: Cross-check against system-level requirements
3. **Client Requirements**: Validate against original transcriptions
4. **Internal Logic**: Check for contradictions and completeness
5. **Dependency Validation**: Verify linked FRs and module dependencies
6. **Issue Analysis**: Compile critical, medium, and minor issues with solution options

## Execution Flow

### Step 1: Parse FR Number and Initialize Todo List

**MUST** extract FR number:

- Extract from `$ARGUMENTS` or user prompt
- Accept formats: "FR-001", "FR001", "fr-001", "011"
- If not provided, **MUST** ask: "Please specify the FR number (e.g., FR-001)"
- Normalize to: "FR-###"

**MUST** use TodoWrite to create initial todos:

```
1. Parse FR number ✓
2. Check FR-specific PRD structure
3. Load Constitution + System PRD summary
4. [Placeholder: PRD sections will be added after structure check]
5. Constitution compliance check
6. Dependency validation
7. Compile initial report
8. Post-report verification
9. Output final report
```

### Step 2: Check FR-Specific PRD Structure (Do Not Load Full Content)

**CRITICAL**: Only check structure, do NOT load full PRD yet.

1. **Locate PRD**: Use Glob for `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`
2. **Extract H2 Headers**: Use grep to get section names without loading content:

   ```bash
   grep -n "^## " fr###-*/prd.md
   ```

   This returns section names with line numbers (e.g., "45:## Overview", "120:## Workflows")
3. **Update Todo List**: Use TodoWrite to insert one todo per PRD section:

   ```
   4. Analyze PRD: [Section 1 Name]
   5. Analyze PRD: [Section 2 Name]
   ...
   N. Analyze PRD: [Section N Name]
   ```

4. **Mark Step 2 Complete**: Update todo status

### Step 3: Load Reference Documents (Minimal Context)

**MUST** load only what's needed for reference:

1. **Constitution**: Load full `.specify/memory/constitution.md`
2. **System PRD Summary**: Use Grep to extract ONLY FR section:

   ```bash
   grep -A 50 "## FR-${FR_NUMBER}" local-docs/project-requirements/system-prd.md
   ```

   Extract: Title, Priority, Modules, Dependencies
3. **Transcription Paths**: Store paths only (do NOT load content yet):
   - `local-docs/project-requirements/transcriptions/Hairline-AdminPlatform-Part1.txt`
   - `local-docs/project-requirements/transcriptions/Hairline-AdminPlatformPart2.txt`
   - `local-docs/project-requirements/transcriptions/Hairline-ProviderPlatformPart1.txt`
   - `local-docs/project-requirements/transcriptions/Hairline-ProviderPlatformPart2.txt`
   - `local-docs/project-requirements/transcriptions/HairlineApp-Part1.txt`
   - `local-docs/project-requirements/transcriptions/HairlineApp-Part2.txt`
   - `local-docs/project-requirements/transcriptions/HairlineOverview.txt`

**Mark Step 3 Complete**.

### Step 4: Analyze Each PRD Section Incrementally

**CRITICAL**: Process ONE section at a time. DO NOT rely on context from previous sections.

For **EACH** PRD section (from todo list):

#### 4.1 Mark Todo as In-Progress

Use TodoWrite to mark current section as `in_progress`.

#### 4.2 Load Section Content Only

- Use Read with line offset/limit to load ONLY this section
- Example: Section starts at line 200, next section at 350

  ```
  Read(file, offset=200, limit=150)
  ```

#### 4.3 Fresh Grep for Each Section (No Context Reliance)

**MUST** perform fresh searches for this section:

**A. Constitution Grep**:

```bash
# Extract key terms from section content
grep -i "[key_term_1|key_term_2]" .specify/memory/constitution.md
```

Check for: Architecture rules, security requirements, module definitions

**B. System PRD Grep**:

```bash
grep -i "[feature|requirement]" local-docs/project-requirements/system-prd.md
```

Verify: FR consistency, module codes, business rules

**C. Transcription Grep** (all files):

```bash
grep -i "[feature|workflow]" local-docs/project-requirements/transcriptions/*.txt
```

Validate: Client intent, original requirements, workflow descriptions

#### 4.4 Section Analysis (Document Review)

**CRITICAL**: This is PRD document review, NOT code review. Focus on specification quality, completeness, and alignment.

For this section, check:

1. **Constitution Compliance** (Document Alignment):
   - Does PRD specify architecture that aligns with multi-tenant, API-first, modularity?
   - Are security requirements documented (auth methods, encryption, audit trail)?
   - Are performance standards specified (response times, scalability targets)?
   - Are testing requirements mentioned (unit, integration, e2e)?
   - **Flag if**: Specification contradicts or omits Constitution principles

2. **System PRD Alignment** (Cross-Document Consistency):
   - Do module identifiers (P-##, PR-##, A-##, S-##) match what System PRD lists for this FR?
   - Do FR numbers referenced match System PRD definitions?
   - Does this section contradict other FR specifications in System PRD?
   - Are business rules consistent with System PRD?
   - Are dependencies properly documented?
   - **Flag if**: Document contradictions, mismatched module IDs, or incorrect FR references
   - **Note**: This checks document consistency, NOT codebase implementation

3. **Client Requirements Traceability** (Requirement Coverage):
   - Can each requirement be traced back to client transcriptions?
   - Are there client requirements in transcriptions NOT captured in this section?
   - Does specification match client's original intent and wording?
   - Are workflows specified as client described?
   - **Flag if**: Missing client requirements or misinterpretations

4. **Specification Completeness** (Document Quality):
   - Are all requirements clearly and unambiguously specified?
   - Are edge cases, error scenarios, and validations documented?
   - Are acceptance criteria defined and testable?
   - Are workflows complete (no missing steps)?
   - Are data models, APIs, and interfaces fully specified?
   - **Flag if**: Incomplete, vague, or contradictory specifications

5. **Screen Field Provenance** (if section is Screen Specifications):
   - **CRITICAL**: For each screen/UI specification, verify ALL fields have clear origin
   - Every field must have a provenance (source):
     - ✅ User input (form field, text input, selection)
     - ✅ System calculated/derived (formula, computation)
     - ✅ Database/API retrieved (from backend)
     - ✅ Previous screen/workflow step (carried over from earlier flow in this FR)
     - ✅ Inherited from dependent FRs (field defined in another FR's workflow)
     - ✅ Inherited from previous screens in dependent FRs (cross-FR data flow)
     - ✅ Default/preset value (documented default)
     - ✅ Session/context data (user profile, tenant info)
   - **Valid Inheritance**: Fields from other FRs or previous screens are acceptable IF documented
   - **Flag as Critical Issue**: Any field appearing "out of nowhere" without documented source or inheritance path
   - **Validation Method**:
     - List all fields in screen
     - Grep current FR's PRD for field definition/source
     - Grep current FR's workflows for data flow
     - If no source found, grep dependent FRs for field origin (check if inherited)
     - If inherited, verify inheritance is documented in current FR (e.g., "field X from FR-###")
     - Mark field as orphaned ONLY if no provenance found in current FR OR dependent FRs
     - **Key**: Inheritance is valid, but must be documented/traceable

#### 4.5 Document Issues (Per Section)

Store issues found in this section:

- Critical: Constitution violations, security gaps, missing client requirements, orphaned screen fields (no provenance), business rule conflicts with dependencies, data field conflicts breaking integration
- Medium: Incomplete specs, minor contradictions, missing edge cases, inconsistent field naming/formats
- Minor: Documentation gaps, unclear wording

#### 4.6 Clear Context and Mark Complete

**CRITICAL**: After analyzing this section:

1. Clear the section content from context (do not retain in memory)
2. Use TodoWrite to mark section as `completed`
3. Move to next section

Repeat Step 4 for ALL PRD sections.

### Step 5: Dependency Cross-Check

**Mark Step 5 as in-progress**.

For each FR listed in Dependencies section:

1. **Extract Dependency Info**:

   ```bash
   grep -A 30 "## FR-[DEP_NUMBER]" local-docs/project-requirements/system-prd.md
   ```

2. **Check for Conflicts**:
   - Data model mismatches
   - Workflow integration issues
   - Circular dependencies

3. **Business Rules Conflict Check** (CRITICAL):
   - **Extract business rules** from current FR (being verified)
   - **Extract business rules** from each dependent FR
   - **Cross-check for conflicts**:
     - Contradictory validation rules (e.g., age > 18 vs age > 21)
     - Conflicting state transitions (e.g., order can be cancelled vs cannot be cancelled)
     - Incompatible calculations (e.g., different discount formulas)
     - Contradictory authorization rules (e.g., who can approve)
   - **Grep for business rules**:

     ```bash
     grep -A 20 "Business Rules\|Validation\|Constraints" fr###-*/prd.md
     grep -A 20 "Business Rules\|Validation\|Constraints" [dependency-fr]/prd.md
     ```

   - **Flag as Critical**: Any business rule contradiction between FRs

4. **Data Fields Conflict Check** (CRITICAL):
   - **Extract all data fields** from current FR (tables, APIs, forms)
   - **Extract data fields** from each dependent FR
   - **Cross-check for conflicts**:
     - Field type mismatches (e.g., string vs integer)
     - Field format conflicts (e.g., date format differences)
     - Required vs optional conflicts (e.g., FR says required, dependency says optional)
     - Field length/size conflicts (e.g., max 50 chars vs max 100 chars)
     - Enum/dropdown value conflicts (e.g., different status values)
   - **Grep for data definitions**:

     ```bash
     grep -i "field\|column\|attribute\|parameter" fr###-*/prd.md
     grep -A 5 "Data Model\|API\|Schema" fr###-*/prd.md
     ```

   - **Flag as Critical**: Any data field conflict that breaks integration
   - **Flag as Medium**: Inconsistent naming or formats that don't break functionality

5. **Validate Shared Components**:
   - Shared services usage
   - API contracts alignment with both FRs
   - Module boundaries respected

**Mark Step 5 as completed**.

### Step 6: Compile Initial Report

**Mark Step 6 as in-progress**.

**CRITICAL**: This report is for internal compilation only. Do NOT create any files. The report will be output directly to the user in Step 8.

Aggregate all issues found across sections:

1. **Group by Severity**: Critical, Medium, Minor
2. **Deduplicate**: Merge similar issues
3. **Prioritize**: Order by impact
4. **Generate Solutions**: 3+ options per issue with pros/cons/effort

**Report Structure** (under 300 words for single-FR, under 500 words for multi-FR):

```markdown
# FR Verification Report

**FR(s)**: FR-### [, FR-###, ...]
**Priority**: P#
**Modules**: P-##, PR-##, A-##
**Status**: Verified with Issues / Clean

---

## CRITICAL ISSUES

### Issue #1: [Title]
**FR**: FR-### (or Cross-FR)
**Description**: [1-2 sentences]
**Impact**: [What breaks/risks]

**Solutions**:
1. **[Option A]**: [Description] | Pros: [X] | Cons: [Y] | Effort: Low/Med/High
2. **[Option B]**: [Description] | Pros: [X] | Cons: [Y] | Effort: Low/Med/High
3. **[Option C]**: [Description] | Pros: [X] | Cons: [Y] | Effort: Low/Med/High

---

## MEDIUM ISSUES
[Same format]

---

## MINOR ISSUES
[Same format]

---

## SUMMARY

**Total Issues**: X Critical, Y Medium, Z Minor
**Constitution Compliance**: Pass/Fail
**Client Alignment**: assessment
**Dependencies**: Status
**Cross-FR Consistency**: assessment (multi-FR mode only)

**Recommendation**: [Next action]
```

**Mark Step 6 as completed**.

### Step 7: Post-Report Verification (Prevent Hallucination)

**CRITICAL**: Mark Step 7 as in-progress. Verify all findings before output.

For **EACH** issue in report:

1. **Re-Grep Source Documents**:
   - If issue mentions Constitution violation, grep Constitution for exact text
   - If issue mentions client requirement, grep transcriptions for evidence
   - If issue mentions FR conflict, grep System PRD for related FRs

2. **Verify Claims**:

   ```bash
   # Example: Verify security requirement claim
   grep -i "encryption\|security\|authentication" .specify/memory/constitution.md

   # Example: Verify client requirement
   grep -i "[feature_name]" local-docs/project-requirements/transcriptions/*.txt
   ```

3. **Check Evidence Exists**:
   - ✅ Keep issue if grep confirms evidence
   - ❌ Remove issue if no evidence found (hallucination)
   - ⚠️ Downgrade severity if evidence is weaker than claimed

4. **Update Report**: Remove or adjust issues based on verification

**Mark Step 7 as completed**.

### Step 8: Output Final Report

**Mark Step 8 as in-progress**.

**CRITICAL**: Do NOT create any files. Output report directly to user.

Present verified report with:

- All issues confirmed by post-verification grep
- 3+ solution options per issue
- Clear references to source documents
- Under 300 words (single FR) or 500 words (multi-FR)

**Mark Step 8 as completed**.

## Important Notes

- **Incremental Loading**: Never load entire PRD at once
- **Fresh Context**: Grep documents fresh for each section
- **No Memory Reliance**: Do not trust context from previous sections
- **Post-Verification**: Always re-grep to confirm findings
- **Todo Tracking**: Update todo list after every step
- **Constitution Authority**: Violations are ALWAYS critical
- **Screen Field Provenance**: CRITICAL - Every field must have documented origin (user input, calculated, DB, etc.). Flag orphaned fields as critical issues
- **Dependency Conflicts**: CRITICAL - Check business rules and data fields for conflicts with dependent FRs. Contradictions break integration
- **No File Creation**: Report output only, never saved

## Search Commands Reference

**Constitution Grep**:

```bash
grep -i "architecture\|security\|performance\|testing" .specify/memory/constitution.md
grep -A 10 "NON-NEGOTIABLE" .specify/memory/constitution.md
```

**System PRD Grep**:

```bash
grep -A 50 "## FR-###" local-docs/project-requirements/system-prd.md
grep -i "module\|priority\|dependency" local-docs/project-requirements/system-prd.md
```

**Transcription Grep**:

```bash
grep -i "[feature|workflow|requirement]" local-docs/project-requirements/transcriptions/*.txt
grep -C 5 "[keyword]" local-docs/project-requirements/transcriptions/*.txt
```

**PRD Section Loading**:

```bash
# Get section line numbers first
grep -n "^## " fr###-*/prd.md
# Then load specific section with Read(file, offset=X, limit=Y)
```

**Screen Field Provenance Check**:

```bash
# Find all field definitions in screen specifications
grep -i "field\|input\|textbox\|dropdown\|checkbox\|button" fr###-*/prd.md

# Search for field source/origin
grep -i "calculated\|derived\|user input\|database\|api\|retrieved" fr###-*/prd.md

# Check workflow for data flow
grep -i "pass\|carry\|transfer\|populate\|data flow" fr###-*/prd.md
```

**Dependency Conflict Check**:

```bash
# Extract business rules from current FR
grep -A 20 "Business Rules\|Validation\|Constraints\|Rules" fr###-*/prd.md

# Extract business rules from dependent FR
grep -A 20 "Business Rules\|Validation\|Constraints\|Rules" [dependency-fr]/prd.md

# Extract data fields from current FR
grep -i "field\|column\|attribute\|parameter\|data type" fr###-*/prd.md
grep -A 10 "Data Model\|API Schema\|Database\|Table" fr###-*/prd.md

# Extract data fields from dependent FR
grep -i "field\|column\|attribute\|parameter\|data type" [dependency-fr]/prd.md
grep -A 10 "Data Model\|API Schema\|Database\|Table" [dependency-fr]/prd.md
```

## Quality Assurance Checklist

Before output, verify:

- [ ] All PRD sections analyzed individually
- [ ] Fresh grep performed per section
- [ ] Todo list updated after each step
- [ ] Screen field provenance checked (all fields have documented origin)
- [ ] Dependency business rules conflicts checked
- [ ] Dependency data fields conflicts checked
- [ ] All issues verified with post-report grep
- [ ] Each issue has ≥3 solution options
- [ ] Report under 300 words
- [ ] No hallucinated claims in report
- [ ] References to source documents included

## Error Handling

If verification cannot be completed:

- Document missing files/sections in report
- Note incomplete dependencies
- Mark uncertain areas with [UNVERIFIED] tag
- Provide partial analysis with caveats
- List additional info needed

## References

**GitHub**:

- System PRD: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/system-prd.md`
- FR PRDs: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr###-*/prd.md`
- Transcriptions: `https://github.com/joachimtrungtuan/hairline-pm-docs/tree/main/project-requirements/transcriptions`

**Local**:

- Constitution: `.specify/memory/constitution.md`
- System PRD: `local-docs/project-requirements/system-prd.md`
- Transcriptions: `local-docs/project-requirements/transcriptions/`
