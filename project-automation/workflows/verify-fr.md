---
description: Verify FR specs against constitution, system PRD, client transcriptions, and dependency integrity. Returns evidence-backed issue report.
---

# Verify FR

Verify one or more FR specifications through incremental section analysis and evidence-based cross-checking. Output the report directly — do not create files.

## Modes

- **Single FR**: Verify one FR specification
- **Multi-FR**: Verify multiple interconnected FRs — each analyzed individually, then cross-checked for consistency, conflicts, and shared dependency issues

## Inputs

At least one FR identifier, normalized to `FR-###`. Accepted: `FR-001`, `FR001`, `fr-001`, `001`. For multi-FR, comma-separated list. If no FR is provided, ask before proceeding.

## Hard Rules

- Process PRD structure first, then sections one-by-one — never load full PRD at once
- Re-grep evidence before final output to avoid unsupported claims
- Output report only — do not create files
- In multi-FR mode, complete individual analysis of each FR before cross-checking

## Progress Tracking (Mandatory)

**Before starting work**, use the platform's task/todo tracking tools (task lists, todo items, progress trackers) to create a checklist of all workflow steps below. Mark each step in-progress when starting and completed when done. This prevents step-skipping and keeps the workflow auditable.

## Steps

1. Parse the FR identifier(s) from user input. Normalize each to `FR-###` format. Create a step checklist covering: parse, structure scan, reference loading, **[PLACEHOLDER — PRD sections added in Step 2]**, dependency checks, draft report, post-verification, final output. Do not add per-section items yet.

2. Locate the FR PRD file at `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`. Extract H2 headers with line numbers — do not load full content yet. **MANDATORY**: Add one tracking item per H2 section found — replacing the placeholder from Step 1. Every section must appear as its own checklist item (e.g., "Analyze PRD: Overview", "Analyze PRD: Workflows", "Analyze PRD: Screen Specifications"). Do not proceed to Step 3 until all PRD sections are in the checklist.

3. Load reference documents (minimal):
   - Full constitution: `.specify/memory/constitution.md`
   - FR-specific section from `local-docs/project-requirements/system-prd.md`
   - Transcription file paths under `local-docs/project-requirements/transcriptions/` (store paths only; load via targeted grep per section)

4. For each PRD section (one at a time):
   - Mark section tracking item in-progress
   - Load only that section's line range
   - Run fresh searches in constitution, system PRD, and transcriptions
   - Evaluate against criteria A–E:

   **A. Constitution Alignment**: Multi-tenant, API-first, modularity compliance. Security (auth, encryption, audit trail). Performance and testing standards. Flag: contradicts or omits principles.

   **B. Cross-Document Consistency**: Module IDs match system PRD. FR references and business rules consistent. Dependencies documented. Flag: contradictions, mismatched IDs.

   **C. Client Requirement Traceability**: Each requirement traceable to transcriptions. No client requirements missing. Workflows match client intent. Flag: missing or misinterpreted.

   **D. Specification Completeness**: Clear, unambiguous. Edge cases, error scenarios, validations. Acceptance criteria testable. Data models and interfaces specified. Flag: incomplete, vague, contradictory.

   **E. Screen Field Provenance** (UI sections only): Every field must have a documented origin.

   Valid provenance types:

   | Source | Example |
   |--------|---------|
   | User input | Form field, text input, selection |
   | System calculated | Formula, computation, derived value |
   | Database/API retrieved | Backend data fetch |
   | Previous screen/step | Data carried from earlier in this FR's workflow |
   | Inherited from dependent FR | Field defined in another FR (must document which FR) |
   | Default/preset value | Documented default |
   | Session/context data | User profile, tenant info |

   Validation: (1) list all fields, (2) grep PRD for field definition, (3) grep workflows for data flow, (4) if not found, grep dependent FRs, (5) verify inheritance is documented, (6) mark orphaned if no provenance found. Flag orphaned as **critical**.

   - Record issues with severity
   - Clear section context before next

5. Cross-check dependencies for each dependent FR from system PRD:
   - Extract dependency definitions
   - **Business rule conflicts**: contradictory validation, state transitions, calculations, authorization
   - **Data field conflicts**: type mismatches, format conflicts, required vs optional, length/size, enum values
   - **Shared component alignment**: API contracts, module boundaries
   - Flag integration-breaking contradictions as critical

6. Compile issue report: group by severity, deduplicate, prioritize by impact. Generate 3+ solution options per issue with pros, cons, and effort estimate.

7. Post-verify every claim by re-running targeted searches. Keep only evidence-backed findings. Remove unsupported. Downgrade severity when evidence weaker than claimed.

8. Output the final verified report. Format: Critical Issues, Medium Issues, Minor Issues, Summary. Under 300 words (single FR) or 500 words (multi-FR).

## Multi-FR Extension

**Phase 1 — Individual verification**: Run Steps 1–7 for each FR separately. Maintain per-FR issue lists.

**Phase 2 — Cross-FR consistency**:
1. Shared data model consistency (field names, types, formats, validation rules)
2. Workflow integration points (FR-A output matches FR-B expected input)
3. Business rule coherence (no contradictions across FRs)
4. Module boundary alignment (no conflicting ownership assumptions)
5. Dependency graph integrity (no circular/missing dependencies)

**Phase 3 — Combined report**: Per-FR issues + Cross-FR issues + Overall consistency assessment.

## Report Template

```
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
**Impact**: [What breaks or risks]

**Solutions**:
1. **[Option A]**: [Desc] | Pros: [X] | Cons: [Y] | Effort: Low/Med/High
2. **[Option B]**: [Desc] | Pros: [X] | Cons: [Y] | Effort: Low/Med/High
3. **[Option C]**: [Desc] | Pros: [X] | Cons: [Y] | Effort: Low/Med/High

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

## Severity

- **Critical**: constitution violations, missing client must-haves, orphaned UI fields without provenance, dependency rule/data conflicts that break integration, cross-FR business rule contradictions
- **Medium**: incomplete specs, inconsistent field formats/names, missing edge cases, minor cross-FR inconsistencies
- **Minor**: clarity and documentation quality gaps

## Search Commands Reference

**Constitution**:

```
rg -i "architecture|security|performance|testing" .specify/memory/constitution.md
rg -A 10 "NON-NEGOTIABLE" .specify/memory/constitution.md
```

**System PRD**:

```
rg -A 50 "## FR-###" local-docs/project-requirements/system-prd.md
rg -i "module|priority|dependency" local-docs/project-requirements/system-prd.md
```

**Transcriptions**:

```
rg -i "keyword" local-docs/project-requirements/transcriptions/*.txt
rg -C 5 "keyword" local-docs/project-requirements/transcriptions/*.txt
```

**PRD section loading**:

```
rg -n "^## " local-docs/project-requirements/functional-requirements/fr###-*/prd.md
```

**Screen field provenance**:

```
rg -i "field|input|textbox|dropdown|checkbox|button" fr###-*/prd.md
rg -i "calculated|derived|user input|database|api|retrieved" fr###-*/prd.md
rg -i "pass|carry|transfer|populate|data flow" fr###-*/prd.md
```

**Dependency conflict check**:

```
rg -A 20 "Business Rules|Validation|Constraints|Rules" fr###-*/prd.md
rg -i "field|column|attribute|parameter|data type" fr###-*/prd.md
rg -A 10 "Data Model|API Schema|Database|Table" fr###-*/prd.md
```

## Quality Checklist

- [ ] All PRD sections analyzed individually
- [ ] Fresh searches per section
- [ ] Todo list updated after each step
- [ ] Screen field provenance checked for all UI sections
- [ ] Dependency business rule and data field conflicts checked
- [ ] All findings post-verified
- [ ] Each issue has 3+ solution options
- [ ] Report within word limit
- [ ] No unsupported claims
- [ ] Cross-FR consistency checked (multi-FR mode)

## Error Handling

If verification cannot be completed:

- Document missing files/sections in report
- Note incomplete dependencies
- Mark uncertain areas with [UNVERIFIED] tag
- Provide partial analysis with caveats
- List additional info needed

## Deployment

Copy this file to `.agent/workflows/verify-fr.md` for Antigravity to detect it.
