# Sprint 1 PR-06 Awards Review

**Date**: 2026-06-25
**Area**: Sprint 1 readiness backlog, `PR-06 - Profile & Settings Management`
**Primary Files Updated**:
- `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`

## Summary

Updated the Sprint 1 readiness backlog after direct Provider-dashboard review of the `Profile Setting -> Awards` tab for the third provider testing account.

## Changes Applied

- Added positive `Review Notes` coverage that the provider `Awards and recognition` flow now:
  - opens the add-award modal
  - accepts image upload and award details
  - persists a newly added award after `Save changes` plus reload
  - persists award deletion after save plus reload
- Added confirmed bug row `PR-06-022` for the add-award modal showing a false `Profile updated successfully!` toast immediately on modal open.
- Added confirmed bug row `PR-06-023` for the add-award form presenting optional-field labels that do not match actual save validation, including a confirmed `Description is required` validation error.
- Added confirmed bug row `PR-06-024` for provider-side duplicate award creation when `Save changes` is clicked a second time without reloading after the first successful save.
- Tightened the PR-06 pending-coverage row so `Awards` is no longer treated as untested; the remaining pending PR-06 follow-up now focuses on `Reviews`, `Documents`, and still-exposed provider package-catalog entries.

## Evidence Anchors

- `https://s.letweb.net/s/dn553m`
- `https://s.letweb.net/s/govv96`
- `https://s.letweb.net/s/epmm3q`
- `https://s.letweb.net/s/dqvv3j`
- `https://s.letweb.net/s/gryy0n`
- `https://s.letweb.net/s/evqq3l`
- `https://s.letweb.net/s/dw77y8`
- `https://s.letweb.net/s/gxjj74`
- `https://s.letweb.net/s/eykk0z`
- `https://s.letweb.net/s/dz663m`
- `https://s.letweb.net/s/d1qqy7`
- `https://s.letweb.net/s/g2xxzr`

## Notes

- The duplicate-save defect recorded as `PR-06-024` matches the same core pattern already documented in Admin row `A-02-008`, so the final fix should be treated as a shared awards-editor regression across both Admin and Provider surfaces.
- FR-032 Awards tab source of truth used for this pass: `issuer/organization` is explicitly optional, award image is JPEG/PNG up to 2MB, and award changes should save cleanly without misleading pre-save success feedback.
- Same-day follow-up expanded the PR-06 review coverage into the `Reviews` tab and embedded provider-profile review section. The readiness backlog now records that row-level detail open from `Profile Setting -> Reviews` does work and exposes the inline provider response composer, but two additional defects were confirmed: `PR-06-025` for cross-surface review-dataset mismatch between profile preview, settings list, and detail payload; and `PR-06-026` for the broken `View all` / breadcrumb route chain that leads to empty state and 404 pages.
- Same-day follow-up expanded the PR-06 review coverage into `Documents (Record Keeping)`. The backlog now records that the provider can upload into the currently exposed document cards and still see those cards after save plus reload, but three additional document defects were added: `PR-06-027` for the provider documents surface being narrower than the FR-032 Tab 6 document model, `PR-06-028` for missing file preview / type-specific rendering, and `PR-06-029` as a code-backed scout flag that the current replace path does not clearly satisfy the PRD's replace-with-versioning rule.
- Live backend verification of the just-uploaded provider documents was attempted in the same pass, but the environment blocked the required escalated API call. The PR-06 documents note therefore distinguishes between directly observed UI behavior (upload, save, reload) and the still-open backend versioning verification risk.
- Same-day follow-up created Plane tasks for the confirmed `Recorded only` PR-06 rows and wrote the created keys back into the readiness backlog: `PR-06-020` -> `HAIRL-1380`, `PR-06-021` -> `HAIRL-1381`, `PR-06-022` -> `HAIRL-1382`, `PR-06-023` -> `FE: HAIRL-1383; BE: HAIRL-1384`, `PR-06-024` -> `HAIRL-1385`, `PR-06-025` -> `FE: HAIRL-1386; BE: HAIRL-1387`, `PR-06-026` -> `HAIRL-1388`, `PR-06-027` -> `HAIRL-1389`, and `PR-06-028` -> `HAIRL-1390`.
