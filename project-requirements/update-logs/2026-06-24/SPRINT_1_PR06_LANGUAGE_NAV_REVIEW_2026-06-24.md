# Sprint 1 PR-06 Language Navigation Review

**Date**: 2026-06-24
**Area**: Sprint 1 readiness backlog, `PR-06 - Profile & Settings Management`
**Primary Files Updated**:
- `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`

## Summary

Updated the Sprint 1 readiness backlog after direct Provider-dashboard review of the `Profile Setting -> Languages` tab.

## Changes Applied

- Added positive `Review Notes` coverage that the provider `Languages` tab now:
  - loads available language options
  - supports search
  - allows adding additional spoken languages
  - persists additions and removals after save and reload
- Added confirmed bug row `PR-06-020` for the `Languages -> Cancel` path routing providers into the admin `/providers` list and exposing the admin `Add New Provider` wizard.
- Added confirmed bug row `PR-06-021` for the top-right navbar `Profile Setting` shortcut being wired to the current browser URL instead of a stable provider profile-settings route.
- Tightened the PR-06 pending-coverage row so `Languages` is no longer treated as untested; the remaining pending PR-06 follow-up now focuses on `Awards`, `Reviews`, `Documents`, and provider package-catalog coverage.

## Evidence Anchors

- `https://s.letweb.net/s/d7kkyj`
- `https://s.letweb.net/s/g8yy82`
- `https://s.letweb.net/s/e9yy8o`
- `https://s.letweb.net/s/g0ooy0`
- `https://s.letweb.net/s/ejnn73`
- `https://s.letweb.net/s/gl9957`
- `https://s.letweb.net/s/emoo59`

## Notes

- Follow-up evidence removed the earlier ambiguity around the top-right `Profile Setting` shortcut: hover-target screenshots from both `Dashboard` and `Inquiries` now show the menu item inheriting the current page URL itself, so the report now records that behavior as confirmed bug `PR-06-021`.
