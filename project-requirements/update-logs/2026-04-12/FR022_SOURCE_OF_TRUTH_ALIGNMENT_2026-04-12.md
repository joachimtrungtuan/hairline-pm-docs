# FR-022 Source-of-Truth Alignment

**Date**: 2026-04-12  
**Scope**: FR-022 follow-up corrections after verification issue resolution choices were approved

## Summary

This update applies the selected follow-up resolutions from the FR-022 verification review to tighten FR-022 as the actual source of truth for search and filter behavior.

## Changes Applied

1. Added the remaining missing Help & Support search/filter screens to `FR-022`:
   - `FR-035 / Screen 1` Help & Support Hub
   - `FR-032 / Screen 5` Help Centre
   - `FR-032 / Screen 5.1` FAQs
   - `FR-032 / Screen 5.3` Resource Library
2. Corrected the provider messaging reference in `FR-022` from `FR-012 / Screen 2` to the actual source screen `FR-012 / Screen 3`.
3. Replaced the FR-022 provider-message criteria with the source-backed FR-012 Screen 3 contract:
   - search by patient name, inquiry/quote ID, or message content
   - read-status toggle (`All`, `Unread Only`)
   - preset activity-date filter (`Today`, `Last 7 days`, `Last 30 days`, `All`)
   - service-type dropdown sourced from the service catalog
4. Aligned the A-02 provider-management summary/search wording in `FR-022` to the admin dashboard model in `FR-015`.
5. Corrected the stale `Tier-based` commission filter option in `FR-015 / Screen 1` to `Flat Rate` so the list filter matches the documented commission model.

## Files Updated

- `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`
- `local-docs/project-requirements/functional-requirements/fr015-provider-management/prd.md`
- `local-docs/project-requirements/update-logs/README.md`

## Rationale

The verification report found that FR-022 still had gaps between its source-of-truth claim and the actual referenced screen contracts. This update closes the remaining documented gaps without changing product behavior beyond what the source FRs already specify.
