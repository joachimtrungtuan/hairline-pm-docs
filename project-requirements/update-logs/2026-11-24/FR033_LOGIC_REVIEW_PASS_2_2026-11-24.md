# FR-033 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 2.5 to 2.6, with a graph change-set)
**Scope**: FR-033 Help Centre Content Management
**Source of findings**: `plans/reports/tester-261124-fr033-logic-p2.md` (9 findings; 6 fixed here, 3 queued for FR-031, FR-032 and FR-035; two had a business decision, both taken as recommended)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr033-help-centre-management/prd.md`

- **Replacing a Published video**: when the file of a Published video is replaced or its source is switched, the previous video stays live for viewers until the new one is Ready; if the new file fails, the old one stays in place and the admin is told. A new item still stays Draft on a failed upload (A4 step 12, Screen 5.1 rules and notes, REQ-033-077, REQ-033-094).
- **Delete of a Published item**: an admin may delete a Published item directly (Rule 4, any state to Archived by Delete) and it leaves the audience's view within 1 minute; the FR-035 propagation line and REQ-033-034 now name deleting next to publish, edit, reorder and unpublish. The REQ-033-099 title no longer says only Unpublish leaves Published.
- **Bulk actions**: a bulk status change offers Publish and Unpublish only, a bulk Unpublish takes one shared reason, and a bulk delete follows the single-item delete rules (Rule 4, the bulk line of Screens 2, 3, 4 and 5, REQ-033-062).
- **Draft for an Unpublished item**: one shared sentence in Rule 4 and REQ-033-099 says Draft is not selectable for an Unpublished item; the eight Publish Status rows are left as they are.
- **Deleting a service component**: the component is kept on past incidents and maintenance windows and shown there as removed; it cannot be deleted while it is on an open incident (not Resolved) or on a Scheduled or In Progress maintenance window, and the message names the incident or window (Screen 6 delete rule, Screen 6.1, REQ-033-081).
- Change log row for version 2.6 is added; Last Updated is unchanged (same date).

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr033-logic-p2-fixes.yaml`

- New: field ENT-service-component.is_active (bool, required), the in-use flag behind "active component" in REQ-033-080; no new entity.
- Edges: STP-033-049 next STP-033-041 (processing failed); the virus-scan step STP-033-165 is now entered from the resource upload steps STP-033-148 and 151 and the video upload step STP-033-041, and leaves back to each (file rejected) and on to the thumbnail or validation step (file clean); REQ-033-081 and REQ-033-080 apply to the new field; patient list screens SCR-033-20, 22 and 24 show the same Last Updated (and View Count on articles) columns as the provider lists.
- Updated to mirror the PRD: 6 rule statements (REQ-033-034, 062, 077, 081, 094, 099; two with new titles) and 2 step titles (STP-033-049, STP-033-164). No edge is removed.
- Test-applied on a scratch copy of the graph: 35 change rows, no errors; the copy was deleted and the real graph was not touched.

## Not changed here

Neighbour changes are queued in the logic review ledger section for FR-033, not applied: FR-035 (video description mapped to the summary field and optional, article list excerpt built from the start of the body), FR-032 (Screen 5.7 fourth overall value "Status not available"), FR-031 (the Help Centre permission covers provider and patient content as one permission). Minor observations other than the Draft sentence are left as they are and listed under the ledger leftovers.
