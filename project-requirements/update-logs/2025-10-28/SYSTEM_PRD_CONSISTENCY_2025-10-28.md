# system-prd Consistency Update - October 28, 2025

**Status**: ✅ Complete  
**Scope**: Align FR-001 and FR-026 with centrally managed settings and code-fixed security constants; ensure no conflicts with prior rules.

## Changes

### FR-001: Patient Authentication & Profile Management

- Locked email verification to 6-digit OTP (no links); reset also 6-digit OTP.
- Marked password policy as FIXED in codebase: 12+ chars with upper, lower, digit, special from !@#$%^&(),.?":{}|<>.
- Marked OTP length FIXED at 6; kept expiry/resend cooldown configurable.
- Added mobile-only registration; admins cannot create patients.
- Noted centrally managed datasets (discovery options, countries, calling codes) via A-09.

### FR-026: App Settings & Security Policies (A-09)

- Reflected code-fixed password policy and OTP length; kept throttling and OTP expiry/cooldown configurable.
- Centralized lists: discovery options, countries, calling codes.
- Added governance: audit, versioning, rollback, RBAC, masking.

## Conflict Check

- Removed any prior implication of email verification via link (none remain).
- No remaining references to configurable password complexity or OTP length outside A-09 constants.
- Admin patient creation policy consistent with Admin Patient Management (A-01): admins oversee but do not create patients.
- Central lists referenced consistently in FR-001 and FR-026.

## Impact

- Improves security posture with code-enforced constants.
- Clarifies ownership: operational knobs in A-09; invariants fixed in code.
- Reduces ambiguity for engineering and QA.

## Follow-ups

- Optional: add Technical Spec note documenting constant locations and unit tests.
