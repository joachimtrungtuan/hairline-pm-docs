# FR-024 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 1.9 to 2.0, with a graph change-set)
**Scope**: FR-024 Treatment and Package Management
**Source of findings**: `plans/reports/tester-261124-fr024-logic-p1.md` (18 findings; each ruled fix, neighbour-only or settled by the PRD)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr024-treatment-package-management/prd.md`

- **Availability after saving pricing**: saving stores the configuration; the treatment is available in quote creation only while the configuration is Offered. Not Offered blocks new quotes, leaves existing drafts and sent quotes unchanged, and a draft can still be sent (REQ-024-006, REQ-024-059).
- **Notices on activation**: the "New treatment available in catalog" notice goes to all active providers the first time a treatment becomes Active, by any route (saved Active, an edit that activates a Draft, or a media upload retry that ends Active). Inactive to Active notifies only providers with a pricing configuration, using the treatment-updated event with "treatment available again" wording; no new event (REQ-024-041, REQ-024-042).
- **Deactivate and reactivate**: Deactivate shows only on Active records (treatments and packages); Draft and Pending Media Upload have none; reactivation is a versioned Edit (REQ-024-003, REQ-024-009, REQ-024-054).
- **Package status and versions**: Draft only for a package that has never been Active; auto-save overwrites the working draft with no version; a version is created only by a successful Update of an Active or Inactive package; status changes are not versioned content (REQ-024-007, REQ-024-008, REQ-024-013, REQ-024-057, REQ-024-069).
- **Deactivation warnings**: the open-quote warning applies on every route to Inactive (Deactivate, the edit form status, bulk); bulk shows one combined count and one confirmation. The treatment warning shows the open booking count, and sent quotes and bookings keep the treatment version they recorded (REQ-024-051, REQ-024-052, REQ-024-072, REQ-024-077).
- **Number of Providers**: counts Offered configurations of Active providers; the treatment warning uses the same count (REQ-024-055).
- **Packages and treatments**: a package is not tied to a treatment (new General Module Rule 12, REQ-024-101).
- **Admin package screen**: Screen 7 lists only Active and Inactive packages; drafts stay with the provider's team (REQ-024-040).
- **Permissions**: REQ-024-082 names the gated actions (package create, edit, clone, deactivate, quick price edit, treatment pricing configuration).
- **Creation limits**: the message when a limit is reached is stated, and only first saves of new records count (a clone counts; auto-save, edits and upload retries do not) (REQ-024-078, REQ-024-098).
- **Media upload**: the chosen status is stored with a Pending Media Upload record and restored on a successful retry; a failed upload on an edit of an Active treatment keeps the previous version and status live and reports the failed file; the same for images and PDFs (REQ-024-049, REQ-024-100).
- **Media processing and image optimisation**: the two paragraphs are marked as implementation notes, not requirements, and format wording is MP4 only for video, JPEG and PNG for images.
- **Translation**: admin-authored library text and UI labels use FR-021 translation keys (a treatment-library key group in FR-021); provider-authored package names and descriptions are free text, machine-translated for the reader only when the FR-021 free-text switch is on (REQ-021-119). The sentence saying FR-021 must be updated is removed (REQ-024-081).
- **Flows**: five short flows added for Screens 6, 7 and 8, Quick Copy Pricing, and quick price edit with bulk deactivate (A7 to A11).
- **Order of the treatment list**: Active, Pending Media Upload, Draft, Inactive (REQ-024-054).
- Dependencies now name FR-030 (notification catalogue); the change log row and Last Updated are set.

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr024-logic-p1-fixes.yaml`

- New: rule REQ-024-101; flows FLW-024-treatment-types, FLW-024-admin-package-review, FLW-024-aftercare-templates, FLW-024-quick-copy-pricing, FLW-024-package-quick-edit-bulk; steps STP-024-128 to -145 (the last is the failed edit upload branch of the media upload flow).
- Rule statements (and some titles) updated to mirror the PRD (25 rules); step titles, event, screen, setting and field descriptions updated.
- Edges: conditions added to the next edges into "notify", "selectable" and "available" steps and to the media upload failure branch; STP-024-086 no longer has a next edge to STP-004-006; FR-024 references REQ-004-056, REQ-004-058 and REQ-021-119.
- Cross-FR edges: the removed next edge ends at an FR-004 step (STP-004-006); the three new references point to rules owned by FR-004 and FR-021. No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 324 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes for FR-004 (line 318 wording, REQ-004-059 scope, Not Offered effect), FR-030 (three catalogue rows), FR-031 and FR-009 (admin permission description and provider package permissions), FR-026 (rate-limit settings screen entries), FR-022 (treatment status filter, Draft option, list order) and FR-021 (treatment-library key group) are queued in the logic review ledger section for FR-024, not applied. Minor observations from the review are left as they are and listed under the ledger leftovers.
