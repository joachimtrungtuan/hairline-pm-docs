# FR-022 Scope Alignment

**Date**: 2026-04-12  
**Type**: Functional requirement alignment  
**Scope**: FR-022, FR-035, FR-033

---

## Summary

Applied the selected post-verification resolutions for FR-022 search/filter consistency:

1. **Issue 1 → Option 1**: Trimmed FR-022 patient provider-search scope to match the current source-of-truth definition in FR-003 Screen 7a.
2. **Issue 2 → Option 2**: Promoted Help Centre full-text search from conditional/future wording to explicit P1 scope across FR-035 and FR-033.
3. **Issue 3 → Option 1**: Removed deferred/untracked search requirements from FR-022 that did not have active screen coverage in the master reference table.

---

## Documents Updated

### `fr022-search-filtering/prd.md`

- Reduced Patient Platform P2 provider-search scope from `name, location, specialty + price/experience sorting/filtering` to the current FR-003-backed set: `name, specialty` search and `country, rating, specialty` filtering.
- Updated Main Flow 3 provider discovery language to remove unsupported `price range`, `experience`, and `reviews` filter claims.
- Removed stale requirement lines for:
  - provider team activity-log filtering
  - provider work-queue filtering
  - patient booking-list search/filtering
- Removed unsupported P2 provider-sort requirements tied to `Recommended`, `Price`, and `Experience`.

### `fr035-patient-help-support/prd.md`

- Replaced all conditional/deferred wording around Help Center full-text search with explicit P1 language.
- Made relevance-ranked results and inline suggestions part of the firm patient Help Center MVP behavior.
- Removed the fallback instruction that allowed browse-only behavior in place of search.

### `fr033-help-centre-management/prd.md`

- Updated `SC-010` from future enhancement wording to a P1 requirement for both audiences.
- Updated Implementation Notes so full-text search is treated as required baseline behavior, with dedicated search infrastructure remaining optional.

---

## Rationale

These changes restore one authoritative contract per screen:

- FR-022 no longer claims search/filter/sort behavior that the referenced source screens do not define.
- FR-035 and FR-033 now align with FR-022 on Help Center search being a real MVP requirement rather than a conditional enhancement.

---

## Follow-Up

- If the team later wants richer patient provider discovery (price, experience, recommended sorting), those fields should be added first to FR-003 Screen 7a and only then reintroduced into FR-022.
- If patient booking-list search/filtering is later formalized, it should be added back only after a source screen is defined and entered into the FR-022 master reference table.
