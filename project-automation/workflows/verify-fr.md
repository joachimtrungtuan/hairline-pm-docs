---
description: Verify FR specs against constitution, system PRD, client transcriptions, and dependency integrity. Returns evidence-backed issue report.
---

# Verify FR

Verify one or more FR specifications through incremental section analysis and evidence-based cross-checking. Output the report directly — do not create files.

## Modes

- **Single FR**: Verify one FR specification
- **Multi-FR**: Verify multiple interconnected FRs — each analyzed individually, then cross-checked for consistency, conflicts, and shared dependency issues

## Inputs

At least one FR identifier, normalized to `FR-###`. Accepted: `FR-001`, `FR001`, `fr-001`, `001`. For multi-FR, comma-separated list.

## Hard Rules

- Process PRD structure first, then sections one-by-one — never load full PRD at once
- Re-grep evidence before final output to avoid unsupported claims
- Output report only — do not create files
- In multi-FR mode, complete individual analysis of each FR before cross-checking

## Steps

1. Parse the FR identifier(s) from user input. Normalize each to `FR-###` format. Create a step checklist covering: parse, structure scan, reference loading, per-section analysis, dependency checks, draft report, post-verification, final output.

2. Locate the FR PRD file at `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`. Extract H2 headers with line numbers — do not load full content yet. Add one tracking item per section.

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

   **E. Screen Field Provenance** (UI sections only): Every field must have documented origin — user input, system calculated, DB/API retrieved, previous screen/step, inherited from dependent FR (document which FR), default/preset, session/context. Validation: (1) list all fields, (2) grep PRD for field definition, (3) grep workflows for data flow, (4) if not found, grep dependent FRs, (5) verify inheritance documented, (6) mark orphaned if no provenance found. Flag orphaned as **critical**.

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

After completing steps 1-7 for each FR individually:

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

## CRITICAL ISSUES
### Issue #1: [Title]
**FR**: FR-### (or Cross-FR)
**Description**: [1-2 sentences]
**Impact**: [What breaks or risks]
**Solutions**:
1. **[Option A]**: [Desc] | Pros | Cons | Effort
2. **[Option B]**: [Desc] | Pros | Cons | Effort
3. **[Option C]**: [Desc] | Pros | Cons | Effort

## MEDIUM ISSUES / ## MINOR ISSUES — same format

## SUMMARY
**Total Issues**: X Critical, Y Medium, Z Minor
**Constitution Compliance**: Pass/Fail
**Client Alignment**: assessment
**Dependencies**: Status
**Cross-FR Consistency**: assessment (multi-FR only)
**Recommendation**: [Next action]
```

## Severity

- **Critical**: constitution violations, missing must-haves, orphaned UI fields, dependency rule/data conflicts breaking integration, cross-FR contradictions
- **Medium**: incomplete specs, inconsistent formats, missing edge cases
- **Minor**: clarity and documentation quality gaps

## Quality Checklist

- [ ] All PRD sections analyzed individually
- [ ] Fresh searches per section
- [ ] Screen field provenance checked for UI sections
- [ ] Dependency business rule and data field conflicts checked
- [ ] All findings post-verified
- [ ] Each issue has 3+ solutions
- [ ] Report within word limit
- [ ] No unsupported claims
- [ ] Cross-FR consistency checked (multi-FR mode)

## Deployment

Copy this file to `.agent/workflows/verify-fr.md` for Antigravity to detect it.
