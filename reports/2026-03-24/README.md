# Design Layout Verification Reports

This folder contains the design-layout verification outputs created on `2026-03-24`.

## File Rules

- Create **one full verification report per flow**.
- Use a **flow-specific suffix** in the full report filename so flows are clearly separated.
- Keep **one shared status file** for the whole report set:
  - `design-layout-verification-status-missing-mobile-flows-design-complement.md`
- The shared status file must list **all checked flows** and their current `Verification Status` and `Approval Status`.
- Do **not** create a separate status file per flow.

## Naming Convention

- Full report:
  - `design-layout-verification-missing-mobile-flows-design-complement-p01.1.md`
  - `design-layout-verification-missing-mobile-flows-design-complement-p01.2.md`
- Shared status file:
  - `design-layout-verification-status-missing-mobile-flows-design-complement.md`

## Update Rules

- When a new flow is verified, add or update its row in the shared status file.
- When a flow-specific report is renamed, update any local references in update logs or related docs.
- Keep findings in the full per-flow report; keep the shared status file lean.

## Scope of Each File

- Full per-flow report:
  - Detailed screen-by-screen verification
  - Field coverage
  - UX/UI findings
  - Action items
- Shared status file:
  - Flow name
  - Verification status
  - Approval status
