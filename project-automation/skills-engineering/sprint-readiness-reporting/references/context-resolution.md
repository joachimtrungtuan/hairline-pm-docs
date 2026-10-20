# Context Resolution

Use this reference before creating or updating any sprint readiness report.

## Goal

Resolve and reuse two files with minimal user friction:

1. readiness report file
2. launch-plan file (the product plan: `local-docs/product-plans/v<N>/plan.md`)

## Path Resolution Rules

### 1. Readiness report file

Resolve in this order:

1. Explicit path already named by the user in the current message
2. Explicit path already used earlier in the same conversation
3. Search `local-docs/product-plans/` for likely report candidates such as:
   - `v*/phases/*/*-readiness-fix-backlog.md` (one folder per phase or sprint of a plan version, for example `v2/phases/phase-1-controlled-commercial-pilot/2026-09-17-readiness-fix-backlog.md` or `v1/phases/sprint-1/2026-05-29-readiness-fix-backlog.md`)
4. If exactly one strong candidate matches the current sprint/module context, use it
5. Ask the user only when:
   - multiple plausible report files exist
   - no plausible file exists
   - the user appears to be changing to a different sprint/report

### 2. Launch-plan file

Resolve in this order:

1. Explicit path already named by the user in the current message
2. Explicit path already used earlier in the same conversation
3. Use the plan of the version that owns the readiness report (`product-plans/v<N>/plan.md`, the folder above `phases/`); for a new report, use the highest version folder in `local-docs/product-plans/`
4. If there is one clearly current plan version, use it
5. Ask the user only when multiple launch plans are equally plausible or no candidate exists

## Reuse Rules

- Once the readiness report path is resolved in the current conversation, reuse it by default
- Once the launch-plan path is resolved in the current conversation, reuse it by default
- Do not ask for either path again unless the user changes sprint scope or the earlier path is no longer valid

## Anti-Patterns

- Do not ask “file nằm ở đâu?” if the user already named the file earlier in the same conversation
- Do not ask for the launch plan if there is one obvious current candidate and nothing in the conversation suggests ambiguity
- Do not silently switch to a different sprint report just because another file exists nearby

## Search Scope

- Prefer targeted search in `local-docs/product-plans/`
- Read only enough of a candidate file to verify it matches the sprint or workflow in context
- Ignore template files after you already know the user is asking to continue an existing report
