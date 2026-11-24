# Constitution consolidation

**Date**: 2026-11-25 (Asia/Saigon)
**Type**: Major update (structural change to a governance document). No rule wording changed. No Change Request (requirements graph programme: new baseline).

## What changed

- **One canonical constitution**: `local-docs/project-requirements/constitution.md` (new, versioned in this repo). It is the original `.specify/memory/constitution.md` (1,060 lines, outside any repository) restructured into: header, "How to use this document", Part A principles, Part B security and compliance, Part C PRD standards and documentation placement, Part D reference and development standards, Part E governance, an Appendix carrying the still-current content of the old summary, and a change log.
- **Rule ids added** as citation labels only (`C-I-n` to `C-X-n`, `C-SEC-n`, `C-PRD-n`, `C-DOC-n`, `C-DEV-n`, `C-GOV-n`). The Roman numerals and original headings are kept, so "Principle II" still resolves.
- **Old path kept as a link**: `.specify/memory/constitution.md` is now a symbolic link to the canonical file (owner approval given twice, the second on 2026-11-24 naming the file). Frozen skills, commands, workflows, task prompts and the Spec Kit commands keep their path and were not edited. The original file is backed up at project root `plans/261123-0836-constitution-consolidation/constitution-original-2025-06-22.md`.
- **Summary merged**: `constitution-summary.md` is now a three-line pointer to `constitution.md`.
- **Open items listed, not resolved**: `constitution-open-items.md` (new) lists rules that look outdated, and disagreements between the original, the old summary, `system-prd.md` and `graph/checklists/prd-structure.md`. Each waits for an owner ruling.
- **References repointed**: `system-prd.md` (Constitution Document line, change-log row, no version change), FR-007 PRD and FR-007B PRD (Source line, change-log row, no version change), `INDEX.md`, `local-docs/README.md`. Update logs, old reports and archived test plans are history and were left as they are.

## Checks

- Script check: all 197 lines of the original that carry MUST, SHALL, NON-NEGOTIABLE, a named standard (GDPR, HIPAA, PCI, WCAG) or a number with a unit appear word for word in the new file.
- Independent review: line diff of the original against the new file shows no reworded, reordered or deleted original line; 20 sampled rules pass. Two review findings were fixed before the switch (editorial precedence wording removed; pointers to a report outside this repo replaced by `constitution-open-items.md`).
- `.specify/memory/constitution.md` resolves to the new file.

## Notes

- A future Spec Kit upgrade or `/speckit.constitution` run writes to `.specify/memory/constitution.md`; through the link that write lands in the canonical file. If the link is ever replaced by a plain file, recreate it.
- The Spec Kit sync-report comment that opened the original file was dropped; its facts are in the new file's change log.
- Proposed, not applied (frozen or root files): mention the new canonical path in the frozen `verify-fr` and `check-progress` files, and add a one-line note on the constitution link beside the templates rule in the project `CLAUDE.md`.
