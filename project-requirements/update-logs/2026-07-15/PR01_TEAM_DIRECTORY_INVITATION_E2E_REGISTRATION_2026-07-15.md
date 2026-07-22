# PR-01 Team Directory and Invitation E2E Registration

**Date:** 2026-07-15
**Status:** Eighteen cases registered as `DRAFT`; activation pending controlled validation and human review

## Summary

Registered `PR-01-FN-002` as the first grouped PR-01 Team function. The boundary includes the Team directory, invite-team-member dialog, and invitation management on `/team`. Invitation acceptance through a mailbox remains a separate later flow.

The registry now contains `PR-01-TC-0007` through `PR-01-TC-0024`, with deterministic dataset recipes and pure Playwright automation for:

- Team access and required directory information;
- matching and empty-state search across name, email, and status;
- Role, Status, and Region filters individually, together with a shared match, and together with no shared match;
- filter control/reset behavior and default pagination;
- invite-form fields and validation;
- fresh invitation creation and email delivery;
- same-Provider duplicate prevention;
- assignable-role enforcement;
- pending invitation actions, resend, and cancel.

Nine requirements remain governed gaps because deterministic role accounts, Provider isolation, seat/rate boundaries, email-failure control, expired-invitation fixtures, concurrency control, or the later audit-log flow are unavailable.

## Live Implementation Mapping

The retry through the Product Owner's authenticated Chrome session confirmed that Invite Staff is accessible. The earlier apparent blocker was caused by an overly strict accessible-name locator, not a missing control.

Current development UI/API mapping confirmed:

- Invite Staff opens the implemented dialog;
- Manager, Clinical Staff, and Billing Staff are assignable while Owner is absent;
- fresh invitation, resend, and cancel behaviors are implemented;
- the generated expiry is seven days;
- the current Team table, search, filters, page size, and invite-form fields differ from the referenced PRD expectations.

These discrepancies remain draft-case assertions and human-review inputs. They are not automatically classified as bugs.

## Mailbox Safety Gate

Maildrop inboxes are public and invitation messages contain an access link. Invitation-mutation datasets now stop before sending unless a human explicitly exports `HAIRLINE_ALLOW_PUBLIC_INVITE_MAILBOX=true` after accepting that exposure. The automation never persists the link or raw invitation token. A private controlled mailbox is preferred when available.

No invitation email was sent during the automated validation recorded here.

## Validation

- Full deterministic framework suite passed: 36 tests.
- Read-only dataset validation confirmed name/email/status matching search, unavailable search, Role matching, and Status matching are ready with current development data.
- Region-only, matching combined, and empty combined filter datasets correctly block before browser execution because the current member API exposes no member-region relationship; no value is guessed or fabricated.
- Development preflight passed with the existing global `@playwright/mcp` runtime and system Chrome; no Playwright package or browser was installed.
- `PR-01-TC-0007` run `RUN-20260715T085339Z-6e36c5fb` produced `POTENTIAL_ISSUE / NEEDS_HUMAN_REVIEW` because the implemented directory does not expose the registered PRD-required structure.
- Locator-hardening runs for `PR-01-TC-0015` remain in the human-review queue as non-clean registration evidence.
- Corrected `PR-01-TC-0015` run `RUN-20260715T090941Z-8daa99fb` passed on the initial attempt with no retained screenshot or trace.
- Product Owner approved the expanded eighteen-case draft design for Playwright implementation.
- Playwright synchronization now waits on observable Team member responses rather than fixed debounce sleeps.
- `PR-01-TC-0019` run `RUN-20260715T101539Z-e2254a55` reached the visible empty state but consistently observed a Team members request without the entered term, producing `POTENTIAL_ISSUE / NEEDS_HUMAN_REVIEW`; no product/test classification was made.
- A runner persistence guard now converts post-attempt infrastructure failures into a reviewable blocked attempt instead of risking a duplicate-attempt SQLite constraint crash.

## Manual Draft Command

From `local-docs/testing-automation/`, an explicitly approved controlled run is:

```bash
pnpm test:function PR-01 PR-01-FN-002 --allow-draft
```

The normal interactive console continues to hide this function until its cases are activated.
