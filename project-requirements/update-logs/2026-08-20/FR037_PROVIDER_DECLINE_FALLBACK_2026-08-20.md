# FR-037 Provider-Decline Distribution Fallback

**Date**: 2026-08-20
**Documents**:
- `functional-requirements/fr037-monitor-hair-loss/prd.md` (v1.8 to v1.9)
- `functional-requirements/fr003-inquiry-submission/prd.md` (v2.0 to v2.1)
- `system-prd.md`

**Trigger**: Product-owner clarification that an exclusive provider's explicit decline must return the converted inquiry to normal FR-003 distribution.

---

## Decision Applied

- An FR-037/FR-038 monitoring conversion still routes initially and exclusively to the assigned provider.
- If that provider explicitly declines before creating a quote, FR-003 records the reason, removes the exclusive-provider restriction, and immediately runs its normal distribution workflow.
- The transition is idempotent and does not require a patient release action.
- Expiry is intentionally separate: inquiry and quote expiry continue to use the existing FR-003/FR-004 rules and do not trigger the explicit-decline fallback.

## Validation

- Confirmed FR-003 owns the provider action, audit requirement, routing transition, idempotency rule, and acceptance coverage.
- Confirmed FR-037 states only the conversion handoff and fallback contract without duplicating FR-003's normal matching algorithm.
- Confirmed the system PRD matches both detailed PRDs.
