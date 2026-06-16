# Bug Task Format

Use this exact block structure for every task.

```markdown
## TASK_NAME_START
[BUG][FE] MODULE_CODE / FR-### - Descriptive bug title
## TASK_NAME_END

**Status**: Drafted
**Plane Task ID**:
**Plane Task Key**:
**FR**: FR-###
**Product Module**: MODULE_CODE
**Labels**: Bugs, FE Task
**Priority**: High
**Plane Module**: [2] Dashboard > Admin
**Cycle**: 2026_Jun_C3
**Parent Task**: HAIRL-1234

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>One concise paragraph describing the observed bug and why it blocks or degrades the intended product behavior.</p>
<h2>Reference</h2>
<ul>
<li>FR PRD: <a href="https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr025-medical-questionnaire-management/prd.md">https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr025-medical-questionnaire-management/prd.md</a></li>
<li>Source backlog: <a href="https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md">https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md</a></li>
<li>Figma: <a href="https://figma.com/example">https://figma.com/example</a></li>
</ul>
<h2>Scope Boundary</h2>
<ul>
<li><strong>This task covers:</strong> FE side only.</li>
<li><strong>Counterpart task:</strong> [BUG][BE] MODULE_CODE / FR-### - Descriptive bug title</li>
<li><strong>Contract/handoff:</strong> the shared API shape or data contract both sides depend on, stated in business/behavioral terms.</li>
</ul>
<h2>Current Status</h2>
<ul>
<li>Observable current behavior only.</li>
</ul>
<h2>Steps to Reproduce</h2>
<ol>
<li>Step from source report.</li>
</ol>
<h2>Expectation (Suggestion)</h2>
<p><strong>Note:</strong> The requirements below describe business needs and functional expectations. Developers should use their expertise to choose the most beneficial and optimized implementation approach.</p>
<ul>
<li>Expected behavior from source bug report and linked PRD/design.</li>
</ul>
<h2>Evidence</h2>
<ul>
<li>Evidence: <a href="https://s.letweb.net/s/example">https://s.letweb.net/s/example</a></li>
</ul>
<h2>Notes</h2>
<ul>
<li>Relevant notes from the source report. Do not include source Task Status.</li>
</ul>
<h2>Acceptance Criteria</h2>
<ol>
<li>Testable criterion from reviewer perspective.</li>
</ol>
## TASK_DESCRIPTION_END
```

## Ordering Rules

- `Reference` must appear immediately after `Overview`, near the top of the description.
- `Scope Boundary` (split tasks only) appears immediately after `Reference`, before `Current Status`.
- Do not move references below `Current Status`, `Evidence`, or `Notes`.
- Include FR PRD/document/design links before details so developers can quickly recall the source requirement.

## Scope Boundary Rules (FE/BE Split)

- Include the `Scope Boundary` section only for tasks created by splitting a bug that spans both sides. Omit it entirely for FE-only and BE-only tasks.
- The section has exactly three fields:
  - **This task covers**: `FE side only.` or `BE side only.`
  - **Counterpart task**: the full name of the sibling task, using the opposite side prefix (`[BUG][BE] ...` on the FE task, `[BUG][FE] ...` on the BE task). Plane keys are unknown at draft time, so reference by name.
  - **Contract/handoff**: the shared API shape or data contract both sides depend on, stated in business/behavioral terms (not implementation detail).
- Both split tasks restate the same `Current Status`, `Steps to Reproduce`, `Evidence`, and `Notes` faithfully from the source.
- Each split task's `Expectation (Suggestion)` describes only that side's expected behavior.
- Labels follow the single-side rule: FE task uses `Bugs, FE Task`; BE task uses `Bugs, BE Task`. Never `Bugs, FE Task, BE Task`.

## Description Rules

- Keep each full task description under 300 words when practical.
- Use only business requirements, observable behavior, user-facing outcomes, and testable acceptance criteria.
- Do not include database schema, table/column designs, class names, function names, framework choices, or endpoint implementation instructions.
- Code/API evidence may appear in `Notes` only as evidence of observed mismatch; do not tell developers how to implement the fix.
- For backlog/report sources, preserve issue, steps, actual, expected, evidence, and notes closely.
- For direct user input, rewrite the bug to be clear, single-minded, and actionable without inventing additional requirements.

## Link Rules

- Use GitHub links in `Reference`, not local paths.
- GitHub base: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/`
- Strip the `local-docs/` prefix before appending the path.
- Every link must be raw-clickable: label text before the anchor, URL as anchor text.
- Include Figma/design only when provided or present in the source.
