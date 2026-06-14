# Bug Task Format

Use this exact block structure for every task.

```markdown
## TASK_NAME_START
[BUG] MODULE_CODE / FR-### - Descriptive bug title
## TASK_NAME_END

**Status**: Drafted
**Plane Task ID**:
**Plane Task Key**:
**FR**: FR-###
**Product Module**: MODULE_CODE
**Labels**: Bugs, FE Task, BE Task
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
- Do not move references below `Current Status`, `Evidence`, or `Notes`.
- Include FR PRD/document/design links before details so developers can quickly recall the source requirement.

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
