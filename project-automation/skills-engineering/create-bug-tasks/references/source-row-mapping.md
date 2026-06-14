# Source Row Mapping

Use this reference when converting bug report rows or user bug input into tasks.

## Sprint Readiness Backlog Rows

Expected columns:

| Source column | Task usage |
|---|---|
| `Priority` | Source priority and Plane priority mapping |
| `Flow / Story` or `Area` | Task title traceability and reproduction context |
| `Issue` | Overview and task title basis |
| `Steps to Reproduce` | `Steps to Reproduce` section |
| `Actual Outcome` | `Current Status` section |
| `Expected Outcome` | `Expectation (Suggestion)` and acceptance criteria |
| `Evidence Link` | `Evidence` section |
| `Task Status` | Selection/status tracking only; never copy into description |
| `Notes` | `Notes` section and reference-resolution hints |

For `Recorded only` mode, select only rows whose `Task Status` cell is exactly `Recorded only`.

Do not convert rows marked:

- `Review pending`
- `Task created (...)`
- `Resolved - pending re-test`
- `Resolved - verified YYYY-MM-DD`

## General Bug Sources

For pasted bugs or less-structured input, extract or ask for:

- One problem statement
- Reproduction steps
- Actual behavior
- Expected behavior
- Affected module/surface
- Evidence link or explicit evidence summary
- Source document/PRD/design when available

If multiple bugs are mixed together, split them into separate tasks.

## FR And Product Module Mapping

Prefer explicit mappings from source headings and notes.

Examples:

- Section `PR-06 - Profile & Settings Management` with FR-024 treatment package issue -> `Product Module: PR-06`, `FR: FR-024`
- Section `A-09a - Content & Treatment Management` with FR-025 questionnaire issue -> `Product Module: A-09a`, `FR: FR-025`
- Section `A-09a - Content & Treatment Management` with FR-024 admin treatment issue -> `Product Module: A-09a`, `FR: FR-024`

If the section gives module but notes identify a different FR, keep both: module from section, FR from notes/PRD.

If FR is not explicit:

1. Search the row text and notes for `FR-###` or `fr###`.
2. Search likely PRDs under `local-docs/project-requirements/functional-requirements/`.
3. Use launch-plan scope only to clarify, not to invent a new FR.
4. If still uncertain, set `FR: TBD` and explain the missing mapping in `Notes`.

## PRD/Document/Design Reference Mapping

Each task should include the most relevant source requirement link.

1. For FR bugs, include the matching FR PRD link.
2. For sprint readiness bugs, include the source backlog/report link.
3. For design mismatch bugs, include Figma/design link if provided or present in the source.
4. For launch-scope clarification, include launch plan only when it materially clarifies the bug.
5. Do not add unrelated docs just to fill the reference list.

## Priority Mapping

Use source priority and Plane priority separately:

| Source priority | Plane priority | Use when |
|---|---|---|
| `P0` | `Urgent` | Production/security/data-loss blocker or critical launch blocker |
| `P1` | `High` | Major current-sprint bug, broken user path, confirmed PRD mismatch |
| `P2` | `Medium` | Important but not blocking core sprint readiness |
| `P3` | `Low` | Minor polish, copy, low-risk UX issue |

Upgrade to `Urgent` only when the bug blocks a hard sprint dependency, causes privilege/security risk, or prevents a required lifecycle from functioning. Explain the reason in `Notes` or summary.
