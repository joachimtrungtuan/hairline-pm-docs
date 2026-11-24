# FR-013 Logic Review, Pass 2 (Closing Fixes)

**Date**: 2026-11-24
**Scope**: FR-013 Reviews and Ratings PRD, v1.18 to v1.19, plus a prepared graph change-set
**Source**: `plans/reports/tester-261124-fr013-logic-p2.md` (20 findings, all accepted)
**Fixer report**: `plans/reports/docs-manager-261124-fr013-logic-p2-fixes.md`

## What changed

PRD: `local-docs/project-requirements/functional-requirements/fr013-reviews-ratings/prd.md`

- Provider-side filtering reads "alias search, treatment, rating, date, response status, source type" everywhere; Screens 5 and 7 gain a Treatment filter, and Screen 7 gains response status.
- Provider Screens 5 and 6 show the treatment name only, with no case identifier.
- An admin removal that closes a Pending takedown request records the removing admin, the removal time and the removal reason as its decision, is audited as a `remove` action carrying the request id, and sends the patient the single removal notice.
- Redact returns a flagged review to Published and clears the flag reason; a removal or approved takedown also clears the flag.
- Respond stays hidden once a replacement response was published, even if the replacement is later removed.
- The provider gets one notice with the reason when an admin removes its response (new flow B3 step 3).
- A case has at most two reviews in total; the submission screen shows a "no more reviews" message afterwards.
- Only cases marked Completed in FR-010 can be reviewed; the 3 months count from the day marked Completed; Closed Early and Cancelled cannot be reviewed.
- Rating aggregates count Published and Flagged reviews, so setting or clearing a flag needs no recalculation.
- Admin Edit fields and Remove review controls are shown only for Published or Flagged reviews; Removed reviews are read-only for admins.
- Screens 2 and 3 show the latest takedown request; an admin edit sets the Edited marker without changing the edit count; public surfaces always show the alias, with the admin unmask an RBAC view only; rate limits cover submissions only; A1 step 1 no longer lists optional photos.

Graph change-set: `local-docs/project-requirements/graph/changesets/2026-11-24-fr013-logic-p2-fixes.yaml`

- Prepared and **not applied** to the live graph. Test-applied to a scratch copy: 71 change rows, no error; the copy was deleted.
- One new Step (the provider response removal notice), four edge removals (procedure_id on Screens 5 and 6 and on REQ-013-058, and the old B3 link), nine new edges, one field flag change (audit admin id optional), and rule, step, screen and entity text updates that mirror the reworded PRD.
- No cross-FR edges and no nodes owned by another FR were changed.

## Neighbour FRs queued (not edited)

- FR-022: REQ-022-092 and REQ-022-093 (provider and admin review list filters).
- FR-030: catalogue row for the provider response removal notice (FR-020 mirror to follow).
- FR-010: hand-off of the Completed date to FR-013.

## Notes

- No existing PRD rule was reversed by a ruling.
- FR-014 still says aggregates use Published reviews only; no ruling named it, so it is left for the implementation backlog.
