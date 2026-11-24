# FR-024 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 2.0 to 2.1, with a graph change-set)
**Scope**: FR-024 Treatment and Package Management
**Source of findings**: `plans/reports/tester-261124-fr024-logic-p2.md` (12 findings, all ruled fixes; two had a business decision, both taken as recommended)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr024-treatment-package-management/prd.md`

- **Draft status**: a treatment is Draft only while it has never been saved as Active or Inactive; a package only while it has no version. On a treatment already saved as Active or Inactive (or a package with a version), auto-save and Save as Draft keep a working draft and change neither the live version nor the status until Update (REQ-024-057, REQ-024-007, REQ-024-048).
- **Drafts and the creation limit**: a draft needs a name; a new record counts toward the limit once, when it is first saved as Active or Inactive (a clone included), not when the draft is created. The admin or provider team that owns a never-published draft can discard it; the removal is audited. Screens 1 and 4 get a Discard Draft action (REQ-024-057, REQ-024-098, REQ-024-078, REQ-024-022).
- **Every route to Inactive for a treatment**: the warning, confirmation and notices (REQ-024-051, REQ-024-043, REQ-024-052) apply both to the Deactivate button and to setting Inactive on the edit form (A1 step 5, A2, Screen 2).
- **Versions on the Inactive route (packages)**: only the Deactivate button and the bulk Deactivate create no version; setting Inactive on the edit form is an Update and creates one (REQ-024-072, REQ-024-008, A4 steps 5 and 7, A5 step 6, Screen 5, Rule 3).
- **Package list**: order is Active, Draft, Inactive; the quick-edit pencil is hidden on a Draft package (REQ-024-076, REQ-024-077).
- **Quick price edit**: applies the package price rule (above 0, two decimals) before saving a version (REQ-024-065, A11 step 2).
- **Media upload failure**: the chosen status stored with a Pending Media Upload record may be Active, Inactive or Draft; a failed upload on an edit of any treatment keeps the previous saved media and status; saving again without the failed file leaves Pending Media Upload and restores the stored status; one error text, "Media upload failed, please try again" (B2, edge case, Screen 2, REQ-024-049, REQ-024-100).
- **Notices**: the update notice goes only when the treatment is Active after the save (listed now in Communication Structure); the "back to Active" notice applies only to a treatment that has been Active before; a never-Active treatment made Active follows REQ-024-041 by any route (REQ-024-042, REQ-024-041, REQ-024-003, A1 step 9).
- **Aftercare templates**: each template is Active or Inactive with Deactivate and Reactivate on Screen 8; an Inactive template is not offered to providers; prescriptions and plans already given keep a copy of their text (REQ-024-085, A9, Screen 8).
- **Export to CSV**: one step added to A11 (REQ-024-077).
- Change log row for version 2.1 is added; Last Updated is unchanged (same date).

## Graph change-set (not applied to the live graph)

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr024-logic-p2-fixes.yaml`

- New: step STP-024-146 (Export to CSV); fields ENT-treatment.ever_active (bool) and ENT-treatment.pending_media_saved_status (enum active, inactive, draft); field ENT-aftercare-content-template.status (enum active, inactive).
- Updated to mirror the PRD: 20 rule statements, 15 step titles, 4 screen descriptions, 2 settings, the treatment-updated event, 2 status field descriptions.
- Edges: rule wiring (REQ-024-098 at the treatment save steps, REQ-024-078 at the package save steps, REQ-024-051, 043 and 052 at the edit-form steps, REQ-024-065 at the quick price edit, REQ-024-057 at the treatment status step); STP-024-139 moved to the configuration stage; the edit-upload branch edge relabelled; new rule-to-field links; Screen 8 shows the template status.
- Removed edges: STP-024-139 at STG-provider-03-active (replaced); STP-024-064 next STP-024-145 (re-added with a new label).
- Cross-FR edge: REQ-024-101 applies at STG-main-02-quote (an FR-004 stage, edge only). No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 105 change rows, no errors, graph lint findings unchanged (29 before and after); the copy was deleted and the real graph was not touched.

## Not changed here

Neighbour changes for FR-011 and FR-010 (template Active or Inactive and the copy of given text), FR-023 (retention of discarded drafts), FR-004 (stage wording for REQ-024-101), FR-026 (counting-rule wording of the two creation-limit settings), FR-022 (package list order with Draft) and FR-030 (update-notice row, if listed) are queued in the logic review ledger section for FR-024, not applied. Minor observations from the review are left as they are and listed under the ledger leftovers.
