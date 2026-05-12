# Task Format Reference

## Block Structure

Every task must use this exact marker structure:

```markdown
## TASK_NAME_START
[PREFIX] Descriptive Task Name
## TASK_NAME_END

**Status**: Drafted
**Plane Task ID**:
**Plane Task Key**:
**FR**: FR-###
**Product Module**: P-## (or TBD)
**Labels**:
**Priority**: Medium
**Plane Module**:
**Cycle**:
**Parent Task**:

## TASK_DESCRIPTION_START
(HTML content here)
## TASK_DESCRIPTION_END
```

## HTML Description Template

```html
<h2>Overview</h2>
<p>[Business problem and expected outcome — 2-3 sentences as a single paragraph. Describe WHAT and WHY, not HOW.]</p>
<h2>Reference</h2>
<ul>
<li>FR PRD: <a href="[GitHub FR PRD link with section anchor]">[GitHub FR PRD link with section anchor]</a></li>
<li>Figma: <a href="[Figma link]">[Figma link]</a></li>
</ul>
<h2>Current Status</h2>
<ul>
<li>[What currently exists or doesn't — observable behavior only]</li>
</ul>
<h2>Expectation (Suggestion)</h2>
<p><strong>Note:</strong> The requirements below describe business needs and functional expectations. Developers should use their expertise to choose the most beneficial and optimized implementation approach.</p>
<ul>
<li>[Business requirement item]</li>
</ul>
<h2>Acceptance Criteria</h2>
<ol>
<li>[Testable criterion from a user/reviewer perspective]</li>
</ol>
```

## HTML Formatting Rules

- Use `<h2>` for section headers
- Use `<p>` for **single paragraphs only** — never use multiple `<p>` tags for a list of items
- Use `<ul>` or `<ol>` with `<li>` for multiple items
- Use `<strong>`, `<code>`, `<a>` as needed
- Reference links must be raw-clickable links: the label is plain text before the anchor, and the anchor text is the URL itself
- No excessive whitespace or blank lines between tags

## Section Length Limits

- Current Status: prefer ≤5 `<li>` items
- Expectation: prefer ≤7 `<li>` items
- Acceptance Criteria: prefer ≤5 `<li>` items
- Full description: under 300 words

## Content Rules (CRITICAL)

### What to include

- Business requirements and functional behavior
- User-facing outcomes and observable states
- Data field lists (field name, expected type/format, business validation rules)
- Business rules and constraints
- Success/failure scenarios from user perspective

### What to NEVER include

- Database schema, table names, column definitions
- Class names, function signatures, code snippets
- Framework-specific patterns (e.g., "use a Laravel migration", "create a React context")
- API endpoint paths or HTTP methods as implementation instructions
- Technology choices or architectural decisions

Data fields should be described as business data (e.g., "Patient must provide: full name, email, phone number, date of birth") not as database columns (e.g., "Create patients table with varchar(255) name column").

## Prefix Reference

| Prefix | Use When |
|--------|----------|
| `[FE+BE TASK]` | Change spans both frontend UI and backend logic |
| `[FE TASK]` | Frontend-only (React in `hairline-frontend` or Flutter in `hairline-app`) |
| `[BE TASK]` | Backend-only (`hairline-backend`) |
| `[UX/UI TASK]` | Design/experience work — screen layouts, user flows, wireframes, interaction patterns |
| `[BUG]` | Fix incorrect existing behavior |

## Reference Section Rules

- Include only the FR PRD GitHub link by default
- Include Figma link only if provided by user — omit `<li>` entirely when no Figma link available
- Add System PRD or transcription links only when they materially clarify that specific task
- Format every link as `Label: <a href="URL">URL</a>`; do not use the label as the anchor text
- GitHub base: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/`
- **Path mapping**: The GitHub repo root corresponds to the contents **inside** `local-docs/`. When converting a local path to a GitHub URL, **strip the `local-docs/` prefix** before appending to the base.
  - Correct: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`
  - Incorrect: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/local-docs/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`

## Plane Metadata Rules

- Plane metadata is per task block. A single file may contain different labels, priorities, Plane modules, cycles, and parent tasks for different tasks.
- `Plane Task ID` stores the internal Plane UUID returned by the API and remains blank before creation
- `Plane Task Key` stores the readable key such as `HAIRL-1131` and remains blank before creation
- `Product Module` stores the PRD/product module code such as `PR-05`, `A-08`, or `S-XX`
- `Labels` defaults to blank in the template; when creating issues, `[FE TASK]` maps to `FE Task`, `[BE TASK]` maps to `BE Task`, `[BUG]` maps to `Bugs`, and `[UX/UI TASK]` maps to `UX/UI` unless explicitly set
- `Priority` defaults to `Medium` unless the user explicitly specifies another priority
- `Plane Module` stores the Plane module name or UUID, for example `[2] Dashboard > Provider`
- `Cycle` stores the active Plane cycle name or UUID resolved for the current date
- `Parent Task` may store a readable key such as `HAIRL-1131` during review; the Plane creation script resolves it to the internal UUID before assigning the parent
