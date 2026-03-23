# Missing Mobile Flows Backend API Audit (2026-03-19)

## Summary

Created a new backend-readiness audit report for the missing patient mobile flows defined in `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`. The audit cross-checked all 15 flows against `main/hairline-backend` routes, controllers, supporting docs, and available tests.

## File Created

- `local-docs/reports/2026-03-19/missing-mobile-flows-backend-api-readiness-report.md`

## Key Findings

- Audited all 15 flows using 4 concurrent sub-agents plus main-thread synthesis.
- Overall result: `0 Ready`, `13 Partial`, `2 Missing`.
- Fully missing flow-level API surfaces:
  - `P03.1 Payment Methods Management`
  - `P05.3 Submitted Reviews List`
- High-impact partial gaps:
  - Patient notification inbox APIs are missing; only device-token registration exists.
  - Patient help-centre access is incomplete because many shared help-content routes are not patient-facing.
  - Delete-account flow is missing optional reason capture, patient request-status APIs, and delete-flow OTP support.
  - Passport/travel flows do not enforce the designed lock-after-submit model.

## Notes

- This is a codebase audit report only. No backend code outside `local-docs/` was changed.
- The report records route/controller evidence and distinguishes patient-facing APIs from routes that exist only under provider/admin middleware.
