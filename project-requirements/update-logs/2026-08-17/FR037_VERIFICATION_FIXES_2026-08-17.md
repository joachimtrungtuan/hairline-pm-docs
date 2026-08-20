# FR-037 Verification Fixes

**Date**: 2026-08-17
**Document**: `functional-requirements/fr037-monitor-hair-loss/prd.md` (v1.2 → v1.3)
**Trigger**: FR-037 verification pass; product-owner decisions on six findings

---

## Context

Verification raised six issues. Two were rejected as scope misunderstandings (reminders and interactive timeline are aftercare-package mechanics, not self-service monitoring). Four were accepted and applied. The rejected pair is now written into the PRD as an explicit boundary so the same false findings are not raised again.

## Changes Applied

### 1. Service boundary — self-service vs aftercare package (new, NON-NEGOTIABLE)

Added a boundary section at the top of Module Scope with a capability comparison table. Records that FR-037 has no cadence, no patient reminders, no overdue/missed-day/compliance state, no milestone-bound entities, and no ongoing care team. States that an aftercare capability absent from FR-037 is correct scope, not a defect.

Reinforced in three places:

- Communication Structure → Out of Scope: patient-configurable logging/scan reminders and any nudge, streak, or adherence notification.
- Business Rule 8: no logging cadence, milestones, or reminders; the only cadence is the provider advice window, which limits the provider, not the patient.
- New REQ-037-022.

### 2. Raw scan media retention → 7 years

Was 2 years, conflicting with the 7-year medical-record minimum in the constitution while the same rule set classifies scans as medical data. Now aligned to 7 years with no shorter raw-media lifecycle. Implementation Notes permit cold-storage tiering but not earlier deletion.

### 3. Duration field bound to FR-003 enum

Screen 1 Duration validation changed from "Active configured value" to the FR-003 Duration enum with an identical value set, so conversion copies the value without remapping or validation failure.

### 4. Conversion flow — explicit summary step

Screen 7 split into two FR-037-owned steps ahead of the FR-003 handoff:

- **Step A (Conversion Summary)**: read-only monitoring recap, carried-over data preview grouped by category, items still needed, summary PDF, and provider-routing notice. No inquiry record exists yet; leaving does not alter the monitoring case.
- **Step B (Review and Edit)**: the previous editable pre-fill review, ending in handoff to the standard FR-003 inquiry screens, which FR-037 does not duplicate.

Business Rule 7 (release to normal FR-003 distribution) is now documented as an FR-003-owned action exercised after conversion, resolving its missing surface. Lifecycle mermaid and Screen 2 action target updated. New REQ-037-021.

### 5. Advice cadence — global, snapshotted at case creation

Rule 5 marked global with no per-case, per-provider, or per-patient override. New Rule 5a: a cadence change applies only to cases created after the change; each case captures the active cadence at creation and keeps it for its lifetime, including through reassignment, so no in-flight window is recomputed. Existing patients get the new cadence on their next case.

Propagated to Screen 12 validation and business rules, the cadence edge case, REQ-037-008, MonitoringCase entity (cadence-at-creation snapshot), and Implementation Notes.

## Not Changed

- Patient reminder feature — out of scope by decision (aftercare package owns it).
- Interactive draggable scan timeline — out of scope by decision; calendar, logged-day count, and severity trend remain the progress presentation.

## Follow-Up

- FR-038 carries the same 2-year raw-media retention rule and was not touched by this pass; it needs the same 7-year alignment.
- FR-003 must add the post-conversion release-to-normal-distribution action that Business Rule 7 now delegates to it.
- Scan watermarking (constitution: patient-ID watermark on scans) is unspecified across all FR PRDs — repo-wide gap, not FR-037-specific.
