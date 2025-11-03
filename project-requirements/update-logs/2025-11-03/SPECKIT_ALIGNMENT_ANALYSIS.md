# Spec Kit Alignment Analysis & Proposed Changes

**Date**: 2025-11-02
**Purpose**: Analyze misalignments between Constitution requirements and current Spec Kit implementation
**Source of Truth**: `.specify/memory/constitution.md`

---

## Executive Summary

The Hairline Platform Constitution (v1.0.0, ratified 2025-10-23) establishes comprehensive standards for documentation, PRDs, and project structure. However, the current Spec Kit implementation (templates and commands in `.specify/` and `.cursor/`) predates these standards and does not fully comply.

**Critical Misalignments Identified**: 7
**Recommended Changes**: 10
**Estimated Effort**: Medium (2-3 hours for template updates, minimal command changes)

---

## Critical Misalignments

### 1. Documentation Location Structure

**Constitution Requirement** (Lines 793-928):

```sh
local-docs/project-requirements/
├── system-prd.md
├── system-data-schema.md
├── functional-requirements/    # Module-level documentation
│   ├── fr001-[module-name]/
│   │   ├── prd.md
│   │   ├── technical-spec.md
│   │   ├── api-contracts.md
│   │   └── testing-plan.md
```

**Current Spec Kit Implementation**:

```sh
specs/[###-feature-name]/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/
└── tasks.md
```

**Impact**: HIGH
**Issue**: Spec Kit generates documentation in `specs/` folder, completely separate from Constitution's required `local-docs/project-requirements/functional-requirements/` structure.

---

### 2. PRD Template Structure & Content

**Constitution Requirements** (Lines 804-862):

**Mandatory PRD Sections** (10 required):

1. Header Information (module codes, feature branch, date, status, source reference)
2. Executive Summary (purpose, scope, multi-tenant implications, entry points)
3. Module Scope (multi-tenant breakdown, communication structure, entry/exit points)
4. Business Workflows (main flows, alternative flows A1/A2/B1/B2, actors, triggers, outcomes)
5. Screen Specifications (purpose, data fields, business rules, notes)
6. Business Rules (general, data/privacy, admin editability, payment/billing)
7. Success Criteria (patient, provider, admin, system, business metrics)
8. Dependencies (internal, external, data)
9. Assumptions (user behavior, technology, business process)
10. Implementation Notes (technical considerations, integration, scalability, security)

**Current spec-template.md Sections**:

1. User Scenarios & Testing
2. Requirements (Functional Requirements, Key Entities)
3. Success Criteria

**Impact**: HIGH
**Issue**: Current spec template covers only ~30% of the required PRD structure. Missing critical sections:

- Module codes and multi-tenant architecture context
- Business workflows with alternative flows
- Screen specifications
- Business rules (especially data privacy, admin editability)
- Dependencies and assumptions
- Implementation notes

---

### 3. PRD Quality Standards & Verification

**Constitution Requirements** (Lines 863-882):

**Quality Standards**:

- **Completeness**: All sections fully populated (no placeholders)
- **Consistency**: Terminology aligns with system-prd.md
- **Traceability**: Every requirement references source FR and module codes
- **Verification**: Cross-checked against client transcriptions
- **Status Management**: "Draft" → "✅ Verified & Approved"
- **Admin Editability**: Explicitly addressed where applicable
- **Multi-Tenant**: Clearly defines involved tenants/platforms
- **Communication Structure**: Explicitly states in/out of scope features

**Verification Process** (5 steps):

1. Transcription Cross-Check against original client requirements
2. Consistency Check with system-prd.md and constitution
3. Completeness Review of all mandatory sections
4. Stakeholder Approval confirmation
5. Status Update to "✅ Verified & Approved"

**Current Implementation**:

- Spec template has basic quality notes
- No verification process defined
- No status management workflow
- No transcription cross-checks
- No multi-tenant or admin editability requirements

**Impact**: HIGH
**Issue**: No quality assurance or verification process exists for generated specs/PRDs.

---

### 4. Module Codes & Traceability

**Constitution Requirements** (Lines 39-226, 806-807):

Every functional requirement must include module codes:

- **Patient Platform**: P-01 through P-07
- **Provider Platform**: PR-01 through PR-06
- **Admin Platform**: A-01 through A-10
- **Shared Services**: S-01 through S-05

PRD headers must include:

```markdown
# [Feature Name]

**Module**: P-05: Aftercare & Progress Monitoring | PR-04: Aftercare Participation
**Feature Branch**: `fr[###]-[module-name]`
**Created**: [DATE]
**Status**: Draft | ✅ Verified & Approved
**Source**: FR-011 from system-prd.md
```

**Current Implementation**:

```markdown
# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: User description: "$ARGUMENTS"
```

**Impact**: MEDIUM
**Issue**: No module code traceability. Cannot map features to constitutional module structure.

---

### 5. Multi-Tenant Architecture Context

**Constitution Requirements** (Lines 39-60, 813-818):

Every PRD must:

- Identify which tenants are involved (Patient/Provider/Admin)
- Define cross-tenant communication boundaries
- Specify authentication/authorization per tenant
- Document API contracts between tenants
- Address data privacy across tenant boundaries

**Current Implementation**:

- No tenant identification in spec template
- No multi-tenant architecture considerations
- No cross-tenant communication documentation

**Impact**: HIGH (for Hairline project)
**Issue**: The entire platform is built on multi-tenant architecture (Principle I: NON-NEGOTIABLE), but specs don't capture this critical context.

---

### 6. Business Workflows vs User Scenarios

**Constitution Requirements** (Lines 821-826):

**Business Workflows Structure**:

- **Main Flow**: Step-by-step primary workflow
- **Alternative Flows**: All variations (A1, A2, B1, B2, etc.)
- **Actors**: All involved parties clearly identified
- **Triggers**: What initiates each workflow
- **Outcomes**: Expected results and status changes

**Current Implementation**:

- User Stories with acceptance scenarios (Given/When/Then)
- Edge cases listed
- No formal workflow notation
- No alternative flows (A1, B1, etc.)
- No explicit triggers or outcomes

**Impact**: MEDIUM
**Issue**: Different workflow notation styles. Constitution expects more formal business process documentation.

---

### 7. Template Reference & Consistency

**Constitution Requirement** (Line 882):

```sh
Template Reference: Use `functional-requirements/fr011-aftercare-recovery-management/prd.md`
as the definitive template for all future module PRDs.
```

**Current Implementation**:

- Uses `.specify/templates/spec-template.md`
- No reference to FR-011 PRD template
- Different structure and terminology

**Impact**: MEDIUM
**Issue**: Constitution establishes FR-011 as the definitive template, but Spec Kit doesn't use it.

---

## Recommended Changes

### Change 1: Update Documentation Directory Structure

**File**: `.specify/scripts/bash/create-new-feature.sh`

**Current behavior**:

```bash
# Creates: specs/[###-feature-name]/
FEATURE_DIR="specs/${FEATURE_ID}-${SHORT_NAME}"
```

**Proposed change**:

```bash
# Creates: local-docs/project-requirements/functional-requirements/fr[###]-[module-name]/
FEATURE_DIR="local-docs/project-requirements/functional-requirements/fr${FEATURE_ID}-${SHORT_NAME}"
```

**Rationale**: Align with Constitution's required documentation structure (Lines 919-928).

**Impact**:

- ✅ Centralizes all documentation in Constitution-mandated location
- ✅ Enables proper integration with system-level docs
- ⚠️ Requires updating all commands that reference `specs/` directory

---

### Change 2: Rename spec.md to prd.md

**Files**:

- `.specify/templates/spec-template.md` → `.specify/templates/prd-template.md`
- All commands referencing "spec.md" → "prd.md"

**Rationale**:

- Constitution consistently refers to "PRD" (Product Requirements Document), not "spec"
- FR-011 template is named `prd.md`
- Industry standard terminology

**Impact**:

- ✅ Aligns terminology with constitution and industry standards
- ✅ Clearer distinction between requirements (PRD) and implementation (technical spec)
- ⚠️ Requires updating 8 command files

---

### Change 3: Expand PRD Template to Include All Constitutional Sections

**File**: `.specify/templates/spec-template.md` (rename to `prd-template.md`)

**Add the following sections**:

```markdown
# [Feature Name]

**Module**: [Module codes - e.g., P-05, PR-04, A-03]
**Feature Branch**: `fr[###]-[module-name]`
**Created**: [DATE]
**Status**: Draft | ✅ Verified & Approved
**Source**: [Source reference - e.g., FR-011 from system-prd.md, User request, etc.]

## Executive Summary

[Clear module purpose and scope]

**Multi-Tenant Architecture**:
- **Tenants Involved**: [Patient Platform / Provider Platform / Admin Platform / Shared Services]
- **Cross-Tenant Communication**: [How tenants interact via APIs]
- **Entry Points**: [How users/systems enter this feature]

## Module Scope

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:
[What functionality exists in patient mobile app]

**Provider Platform (PR-XX)**:
[What functionality exists in provider web app]

**Admin Platform (A-XX)**:
[What functionality exists in admin web app]

**Shared Services (S-XX)**:
[Any shared/reusable services this feature requires]

### Communication Structure

**In Scope**:
- [Explicit list of communication features included]

**Out of Scope**:
- [Explicit list of communication features NOT included]

### Entry Points & Activation

[How users access this feature, what triggers it]

## Business Workflows

### Main Flow: [Workflow Name]

**Actors**: [List all involved parties]
**Trigger**: [What initiates this workflow]
**Outcome**: [Expected result and status changes]

**Steps**:
1. [Actor] [action]
2. System [response]
3. [Continue step-by-step]

### Alternative Flows

**A1: [Alternative scenario name]**
- **Trigger**: [When this alternative occurs]
- **Steps**: [Modified flow]
- **Outcome**: [Result]

**A2: [Another alternative]**
...

**B1: [Error scenario name]**
- **Trigger**: [What causes this error]
- **Steps**: [Error handling flow]
- **Outcome**: [How system recovers]

[Continue with all alternative flows: A1, A2, B1, B2, etc.]

## Screen Specifications

### Screen 1: [Screen Name]

**Purpose**: [What this screen accomplishes]

**Data Fields**:
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| [field1] | [text/number/date] | Yes/No | [Purpose] |
| [field2] | [type] | Yes/No | [Purpose] |

**Business Rules**:
- [Specific rule governing screen behavior]
- [Validation rule]
- [State change rule]

**Notes**:
- [Implementation guidance]
- [Constraints]

[Repeat for all screens]

## Business Rules

### General Module Rules

- **Rule 1**: [General rule applicable to entire module]
- **Rule 2**: [Another general rule]

### Data & Privacy Rules

- **Privacy Rule 1**: [Data access restriction - e.g., provider anonymization until payment]
- **Privacy Rule 2**: [Encryption requirement]
- **Audit Rule**: [Logging and audit trail requirement]

### Admin Editability Rules

- **Editable by Admin**: [What admins can modify]
- **Fixed in Codebase**: [What is hard-coded and not editable - e.g., password requirements, OTP length]
- **Configurable**: [What can be configured with restrictions]

### Payment & Billing Rules *(if applicable)*

- **Payment Rule 1**: [Payment flow rule]
- **Billing Rule 1**: [Billing/invoicing rule]

## Success Criteria

### Patient Experience Metrics
- [Measurable patient-facing outcome]
- [User satisfaction metric]

### Provider Efficiency Metrics
- [Provider workflow improvement]
- [Time savings metric]

### Admin Management Metrics
- [Administrative efficiency gain]
- [Support ticket reduction]

### System Performance Metrics
- [Response time target]
- [Scalability target]

### Business Impact Metrics
- [Revenue impact]
- [User engagement metric]

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-XXX**: [Dependency description and why needed]
- **Module YYY**: [What functionality from other module is required]

### External Dependencies (APIs, Services)

- **External Service 1**: [What external service/API is needed]
- **External Service 2**: [Another dependency]

### Data Dependencies

- **Entity 1**: [What data must exist for this feature to work]
- **State 2**: [What system state is prerequisite]

## Assumptions

### User Behavior Assumptions

- [Assumption about how users will interact]
- [Expected user pattern]

### Technology Assumptions

- [Platform/browser/device assumption]
- [Connectivity assumption]

### Business Process Assumptions

- [Workflow assumption]
- [Organizational assumption]

## Implementation Notes

### Technical Considerations

- [Architecture note]
- [Technology choice guidance]

### Integration Points

- [How this integrates with module X]
- [API contract with service Y]

### Scalability Considerations

- [Performance targets]
- [Load handling approach]

### Security Considerations

- [Security requirement]
- [Threat mitigation]
- [Compliance note]

---

## User Scenarios & Testing *(from original template - keep)*

[Existing user stories section - maintains compatibility]

## Requirements *(from original template - keep)*

[Existing functional requirements section]

## Edge Cases *(from original template - keep)*

[Existing edge cases section]
```

**Rationale**: Constitution requires all 10 mandatory sections (Lines 804-862).

**Impact**:

- ✅ PRDs now comply with constitutional standards
- ✅ Captures multi-tenant architecture context
- ✅ Includes all required business rules and dependencies
- ⚠️ Longer template - may require more user input or AI inference

---

### Change 4: Add PRD Verification Workflow to `/speckit.specify` Command

**File**: `.cursor/commands/speckit.specify.md`

**Add after spec generation** (new step 7):

```markdown
7. **PRD Verification Workflow**:

   a. **Completeness Check**:
      - Verify all 10 mandatory sections are populated
      - Flag any sections with placeholder text
      - Ensure module codes are assigned
      - Verify multi-tenant architecture sections filled

   b. **Consistency Check**:
      - Cross-reference with `local-docs/project-requirements/system-prd.md`
      - Verify terminology aligns with Constitution glossary
      - Check module codes match Constitution module breakdown (Lines 186-226)
      - Ensure principles compliance (especially NON-NEGOTIABLE ones)

   c. **Transcription Check** *(if applicable)*:
      - If feature maps to existing transcription files in `local-docs/project-requirements/transcriptions/`
      - Cross-check requirements against original transcriptions
      - Flag any discrepancies for review

   d. **Status Management**:
      - PRD starts with **Status**: Draft
      - After verification passes: Update **Status** to "✅ Pending Approval"
      - After stakeholder approval: Update **Status** to "✅ Verified & Approved"
      - Document verification results in update-logs/ directory

   e. **Quality Gates**:
      - GATE 1: All mandatory sections present → Proceed to verification
      - GATE 2: Consistency check passes → Proceed to status update
      - GATE 3: Stakeholder approval → Ready for `/speckit.plan`
      - If any gate fails: Document issues and request clarification

8. **Generate Verification Report**:

   - Create a verification report: `local-docs/project-requirements/update-logs/PRD_VERIFICATION_fr[###]-[name]_YYYY-MM-DD.md`

      ```markdown
      # PRD Verification Report: FR-[###] [Feature Name]

      **Date**: YYYY-MM-DD
      **PRD Path**: local-docs/project-requirements/functional-requirements/fr[###]-[name]/prd.md
      **Reviewer**: AI Agent | [Human Reviewer Name]

   ## Completeness Check

      - [x] Header Information (module codes, branch, date, status, source)
      - [x] Executive Summary (purpose, multi-tenant, entry points)
      - [x] Module Scope (tenant breakdown, communication, entry/exit)
      - [x] Business Workflows (main flow, alternative flows, actors, triggers, outcomes)
      - [x] Screen Specifications (purpose, fields, rules, notes)
      - [x] Business Rules (general, privacy, admin editability, billing)
      - [x] Success Criteria (patient, provider, admin, system, business)
      - [x] Dependencies (internal, external, data)
      - [x] Assumptions (user, technology, business)
      - [x] Implementation Notes (technical, integration, scalability, security)

   ## Consistency Check

      - [x] Terminology aligns with system-prd.md
      - [x] Module codes match Constitution module breakdown
      - [x] Multi-tenant architecture addressed
      - [x] NON-NEGOTIABLE principles respected (Data Privacy, Testing, Audit Trail, etc.)

   ## Transcription Check

      - [ ] N/A - No transcription mapping
      OR
      - [x] Cross-checked against [transcription file name]
      - [x] No discrepancies found

   ## Issues Found

      - [None / List of issues]

   ## Recommendations

      - [None / List of recommended improvements]

   ## Approval Status

      - **Current Status**: Draft | ✅ Pending Approval | ✅ Verified & Approved
      - **Next Step**: [Clarification needed / Stakeholder review / Proceed to planning]
   
9. **Report completion with**:

   - PRD path
   - Verification report path
   - Completeness score (X/10 sections)
   - Status (Draft / Pending Approval / Verified & Approved)
   - Recommended next command
```

**Rationale**: Constitution requires formal verification process (Lines 874-881).

**Impact**:

- ✅ Ensures PRD quality before planning begins
- ✅ Creates audit trail of verification
- ✅ Enforces constitutional standards
- ⚠️ Adds processing time to `/speckit.specify` command

---

### Change 5: Update `/speckit.plan` to Reference prd.md

**File**: `.cursor/commands/speckit.plan.md`

**Current** (Line 4):

```markdown
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`
```

**Proposed**:

```markdown
**Input**: Product Requirements Document from `local-docs/project-requirements/functional-requirements/fr[###]-[module-name]/prd.md`
```

**Additional changes in same file**:

- Line 17: Load `FEATURE_SPEC` → Load `FEATURE_PRD`
- Throughout: References to "spec.md" → "prd.md"
- Update Constitution Check to verify PRD status is "✅ Verified & Approved"

**Rationale**: Align with new directory structure and terminology.

---

### Change 6: Create Constitution Check Automation

**File**: `.specify/scripts/bash/check-constitution-compliance.sh` *(NEW)*

**Purpose**: Automate Constitution Check section in plan.md

**Script behavior**:

```bash
#!/bin/bash
# check-constitution-compliance.sh
# Reads .specify/memory/constitution.md
# Extracts all NON-NEGOTIABLE principles and rules
# Generates Constitution Check section for plan.md
# Outputs: List of gates, verification checklist

# Usage: ./check-constitution-compliance.sh --json --feature-id fr123

# Output:
{
  "constitutionVersion": "1.0.0",
  "nonNegotiablePrinciples": [
    {
      "id": "PRINCIPLE_I",
      "name": "Multi-Tenant Architecture",
      "gates": [
        "Each tenant MUST have its own authentication boundaries",
        "Cross-tenant data access MUST occur only through APIs",
        "No direct database access across tenant boundaries"
      ]
    },
    {
      "id": "PRINCIPLE_II",
      "name": "Medical Data Privacy & Security",
      "gates": [
        "Patient PII MUST be encrypted at rest and in transit",
        "Provider platforms MUST NOT display patient details until payment",
        "All data access MUST be auditable"
      ]
    },
    ...
  ],
  "checklistItems": [
    "[ ] Authentication boundaries per tenant verified",
    "[ ] API-only cross-tenant communication verified",
    ...
  ]
}
```

**Integration**: Called by `/speckit.plan` command during Constitution Check phase.

**Rationale**: Automates gate checking, ensures consistency with constitution.md.

**Impact**:

- ✅ Reduces manual constitution review effort
- ✅ Ensures gates stay in sync with constitution updates
- ⚠️ Requires bash script creation and testing

---

### Change 7: Add Module Code Selection to `/speckit.specify`

**File**: `.cursor/commands/speckit.specify.md`

**Add new step** (after step 1: Generate short name):

```markdown
1.5. **Determine Module Codes**:

   Based on feature description, identify which platform tenants and modules are involved:

   a. **Analyze feature scope**:
      - Keywords: "patient", "mobile app" → Patient Platform
      - Keywords: "provider", "clinic", "doctor" → Provider Platform
      - Keywords: "admin", "manage", "oversight" → Admin Platform
      - Keywords: "3D scan", "payment", "notification" → Shared Services

   b. **Map to module codes** (from Constitution Lines 186-226):

      **Patient Platform Modules**:
      - P-01: Auth & Profile Management
      - P-02: Quote Request & Management
      - P-03: Booking & Payment
      - P-04: Travel & Logistics
      - P-05: Aftercare & Progress Monitoring
      - P-06: Communication
      - P-07: 3D Scan Capture & Viewing

      **Provider Platform Modules**:
      - PR-01: Auth & Team Management
      - PR-02: Inquiry & Quote Management
      - PR-03: Treatment Execution & Documentation
      - PR-04: Aftercare Participation
      - PR-05: Financial Management & Reporting
      - PR-06: Profile & Settings Management

      **Admin Platform Modules**:
      - A-01: Patient Management & Oversight
      - A-02: Provider Management & Onboarding
      - A-03: Aftercare Team Management
      - A-04: Travel Management
      - A-05: Billing & Financial Reconciliation
      - A-06: Discount & Promotion Management
      - A-07: Affiliate Program Management
      - A-08: Analytics & Reporting
      - A-09: System Settings & Configuration
      - A-10: Communication Monitoring & Support

      **Shared Services**:
      - S-01: 3D Scan Processing Service
      - S-02: Payment Processing Service
      - S-03: Notification Service
      - S-04: Travel API Gateway
      - S-05: Media Storage Service

   c. **Select applicable module codes**:
      - List all modules this feature touches
      - Primary module(s) that own the feature
      - Secondary modules that integrate with the feature

   d. **Populate PRD header**:
      ```markdown
      **Module**: [Primary module codes - e.g., P-05: Aftercare | PR-04: Aftercare]
      ```

   e. **If module mapping is unclear**:
      - Mark as: **Module**: [NEEDS CLARIFICATION: Feature scope unclear - could be X or Y]
      - Add to clarification questions
```

**Rationale**: Module codes are mandatory in PRD header (Lines 806-807).

**Impact**:

- ✅ Ensures proper module traceability
- ✅ Helps organize features by architectural boundaries
- ⚠️ Requires AI inference for module mapping

---

### Change 8: Update plan-template.md Path References

**File**: `.specify/templates/plan-template.md`

**Current** (Lines 40-47):

```markdown
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

**Proposed**:

```markdown
local-docs/project-requirements/functional-requirements/fr[###-module-name]/
├── prd.md               # Product Requirements (/speckit.specify command output)
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (technical research)
├── data-model.md        # Phase 1 output (entity definitions)
├── technical-spec.md    # Phase 1 output (detailed technical design)
├── api-contracts.md     # Phase 1 output (API specifications)
├── quickstart.md        # Phase 1 output (setup & test guide)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

**Additional changes**:

- Rename `contracts/` directory → `api-contracts.md` single file (aligns with Constitution Line 923)
- Add `technical-spec.md` (Constitution requirement Line 922)

**Rationale**: Match Constitution's functional requirements directory structure (Lines 919-928).

---

### Change 9: Add Multi-Tenant Context to tasks-template.md

**File**: `.specify/templates/tasks-template.md`

**Add new section after header**:

```markdown
# Tasks: [FEATURE NAME]

**Module**: [Module codes from PRD]
**Input**: Design documents from `local-docs/project-requirements/functional-requirements/fr[###-module-name]/`
**Prerequisites**: prd.md (required), plan.md (required), research.md, data-model.md, api-contracts.md

**Multi-Tenant Context**:
- **Affected Tenants**: [Patient Platform / Provider Platform / Admin Platform / Shared Services]
- **Cross-Tenant APIs**: [List any APIs between tenants this feature creates/modifies]
- **Authentication/Authorization**: [Which tenant authentication boundaries are involved]

[Existing content continues...]
```

**Rationale**: Tasks must respect multi-tenant architecture boundaries (Principle I: NON-NEGOTIABLE).

---

### Change 10: Update .specify/templates/checklist-template.md

**File**: `.specify/templates/checklist-template.md`

**Read current file first to understand structure**, then add new checklist type:

```markdown
## Checklist Type: PRD Quality Verification

**Purpose**: Validate PRD completeness and constitutional compliance before planning

### Mandatory Sections Completeness

- [ ] Header Information (module codes, branch, date, status, source reference)
- [ ] Executive Summary (purpose, scope, multi-tenant implications, entry points)
- [ ] Module Scope (tenant breakdown, communication structure, entry/exit points)
- [ ] Business Workflows (main flows, alternative flows, actors, triggers, outcomes)
- [ ] Screen Specifications (purpose, fields, business rules, notes)
- [ ] Business Rules (general, data/privacy, admin editability, payment/billing)
- [ ] Success Criteria (patient, provider, admin, system, business metrics)
- [ ] Dependencies (internal, external, data)
- [ ] Assumptions (user behavior, technology, business process)
- [ ] Implementation Notes (technical, integration, scalability, security)

### Quality Standards

- [ ] No [NEEDS CLARIFICATION] markers remain (or max 3 with justification)
- [ ] All requirements are testable and unambiguous
- [ ] Success criteria are measurable and technology-agnostic
- [ ] Multi-tenant architecture clearly defined
- [ ] Module codes assigned and valid
- [ ] Admin editability explicitly addressed (where applicable)
- [ ] Data privacy rules defined (where applicable)
- [ ] Communication structure in/out of scope stated

### Constitution Compliance

- [ ] Principle I (Multi-Tenant): Tenant boundaries and APIs documented
- [ ] Principle II (Data Privacy): Encryption, anonymization, audit trails addressed
- [ ] Principle V (Testing): Test requirements included in success criteria
- [ ] Principle VI (Audit Trail): State changes and logging documented
- [ ] Principle IX (i18n): Multi-language/currency requirements noted (if applicable)

### Verification Process

- [ ] Transcription cross-check completed (if applicable)
- [ ] Consistency check with system-prd.md passed
- [ ] Completeness review: All sections populated
- [ ] Stakeholder approval obtained
- [ ] Status updated to "✅ Verified & Approved"

### Readiness Gates

- [ ] PRD ready for `/speckit.clarify` (if clarifications needed)
- [ ] PRD ready for `/speckit.plan` (all gates passed)
```

**Rationale**: Provides concrete checklist for PRD verification workflow (Change 4).

---

## Implementation Roadmap

### Phase 1: Template Updates (Priority: HIGH)

**Estimated Time**: 2 hours

1. ✅ **Change 2**: Rename spec-template.md → prd-template.md
2. ✅ **Change 3**: Expand PRD template with all 10 mandatory sections
3. ✅ **Change 8**: Update plan-template.md path references
4. ✅ **Change 9**: Add multi-tenant context to tasks-template.md
5. ✅ **Change 10**: Update checklist-template.md with PRD verification

**Deliverables**:

- Updated `.specify/templates/prd-template.md`
- Updated `.specify/templates/plan-template.md`
- Updated `.specify/templates/tasks-template.md`
- Updated `.specify/templates/checklist-template.md`

---

### Phase 2: Command Updates (Priority: HIGH)

**Estimated Time**: 1 hour

1. ✅ **Change 5**: Update `/speckit.plan` to reference prd.md
2. ✅ **Change 4**: Add PRD verification workflow to `/speckit.specify`
3. ✅ **Change 7**: Add module code selection to `/speckit.specify`
4. Update all command files to use new paths and terminology:
   - `.cursor/commands/speckit.specify.md`
   - `.cursor/commands/speckit.plan.md`
   - `.cursor/commands/speckit.tasks.md`
   - `.cursor/commands/speckit.clarify.md`
   - `.cursor/commands/speckit.analyze.md`
   - `.cursor/commands/speckit.implement.md`

**Deliverables**:

- Updated command files in `.cursor/commands/`
- Updated references from spec.md → prd.md
- Updated paths from specs/ → local-docs/project-requirements/functional-requirements/

---

### Phase 3: Script Updates (Priority: MEDIUM)

**Estimated Time**: 1 hour

1. ✅ **Change 1**: Update `create-new-feature.sh` directory structure
2. ✅ **Change 6**: Create `check-constitution-compliance.sh`
3. Update other scripts:
   - `setup-plan.sh`: Update paths
   - `check-prerequisites.sh`: Update file references
   - `update-agent-context.sh`: Update paths

**Deliverables**:

- Updated `.specify/scripts/bash/create-new-feature.sh`
- New `.specify/scripts/bash/check-constitution-compliance.sh`
- Updated supporting scripts

---

### Phase 4: Validation & Documentation (Priority: MEDIUM)

**Estimated Time**: 30 minutes

1. Test complete workflow: `/speckit.specify` → `/speckit.plan` → `/speckit.tasks`
2. Verify all constitutional requirements met
3. Update `.cursor/rules/specify-rules.mdc` with new standards
4. Create this alignment analysis document ✅
5. Generate CHANGELOG entry for Spec Kit v2.0.0 (breaking changes)

**Deliverables**:

- Tested workflow
- Updated rules file
- CHANGELOG.md entry
- This analysis document ✅

---

## Breaking Changes & Migration Path

### Breaking Changes

1. **Directory structure**: `specs/` → `local-docs/project-requirements/functional-requirements/`
2. **File naming**: `spec.md` → `prd.md`
3. **PRD template**: Expanded from 3 sections to 10+ sections
4. **Branch naming**: `[###-feature-name]` → `fr[###]-[module-name]`
5. **Module codes**: Now required in PRD headers

### Migration Path

**For new features**:

- Use updated `/speckit.specify` command
- Automatically creates Constitution-compliant structure
- PRD includes all mandatory sections

**For existing features** (if any):

1. Create new directory structure: `local-docs/project-requirements/functional-requirements/fr[###]-[name]/`
2. Manually copy and rename files: `spec.md` → `prd.md`
3. Update PRD header with module codes
4. Add missing mandatory sections using PRD template as guide
5. Run PRD verification workflow
6. Keep old `specs/` directory as backup until migration validated

---

## Compliance Checklist

After implementing all changes, verify:

- [ ] All documentation generated in `local-docs/project-requirements/functional-requirements/`
- [ ] PRD template includes all 10 mandatory sections (Lines 804-862)
- [ ] PRD headers include module codes (Lines 806-807)
- [ ] Multi-tenant architecture context captured (Lines 813-818)
- [ ] Business workflows use constitutional format (Lines 821-826)
- [ ] PRD verification process implemented (Lines 874-881)
- [ ] Constitution Check automated in `/speckit.plan`
- [ ] All commands reference `prd.md` not `spec.md`
- [ ] All commands use Constitution-compliant paths
- [ ] Module codes mapped to Constitution module breakdown (Lines 186-226)
- [ ] FR-011 PRD template referenced as definitive source (Line 882)
- [ ] Quality standards enforced (Lines 863-873)
- [ ] Verification process includes all 5 steps (Lines 874-880)

---

## Risk Assessment

### Low Risk

- ✅ Template updates (no code execution)
- ✅ Documentation path changes (Git handles renames)
- ✅ Terminology changes (spec → PRD)

### Medium Risk

- ⚠️ Script path updates (test thoroughly)
- ⚠️ Command workflow changes (validate end-to-end)
- ⚠️ Module code inference (may require manual correction)

### High Risk

- ❌ None identified

### Mitigation Strategies

1. **Incremental rollout**: Phase 1 (templates) → Phase 2 (commands) → Phase 3 (scripts)
2. **Backup existing work**: Git commits before each phase
3. **Test each phase**: Run complete workflow after each phase
4. **Migration script**: Preserve old structure, create new in parallel
5. **Documentation**: Update all references before going live

---

## Success Criteria

This alignment effort succeeds when:

1. ✅ All PRDs generated comply with Constitution standards (Lines 799-883)
2. ✅ Documentation appears in Constitution-mandated locations (Lines 793-928)
3. ✅ PRD verification process enforces quality gates (Lines 874-881)
4. ✅ Module codes provide full traceability (Lines 186-226)
5. ✅ Multi-tenant architecture context captured (Principle I)
6. ✅ Constitution Check automated in planning workflow
7. ✅ No manual corrections needed for constitutional compliance
8. ✅ All Spec Kit workflows reference single source of truth (constitution.md)

---

## Next Steps

**Immediate Actions**:

1. Review this analysis with project stakeholders
2. Approve proposed changes
3. Prioritize implementation phases
4. Execute Phase 1 (template updates)
5. Test updated templates with sample feature
6. Proceed to Phase 2 if Phase 1 successful

**Recommended Approach**: Implement Phase 1 first, validate with a test feature, then proceed to subsequent phases. This minimizes risk and allows course correction.

---

**Document Status**: ✅ Complete
**Next Review**: After Phase 1 implementation
**Owner**: Technical Lead
**Constitution Version**: 1.0.0
**Spec Kit Current Version**: 1.x (pre-alignment)
**Spec Kit Target Version**: 2.0.0 (Constitution-compliant)
