# Aftercare role ruling applied (2026-11-23)

**Type**: Cross-document alignment (owner ruling, requirements graph programme)
**Change Request**: none. Programme rulings set the new baseline.

## Ruling

1. The aftercare specialist is clinic staff working for the provider, not a Hairline team member.
2. The Hairline built-in admin role formerly named "Aftercare Specialist" is renamed "Aftercare Coordinator". Its permissions are unchanged: it oversees aftercare cases, reassigns them, handles escalations and admin-side support.

Not changed: who may deliver an aftercare case. FR-011 still lets a provider hand a case to the Hairline aftercare team and lets an admin assign one to it; members of that team hold the Aftercare Coordinator role.

## Documents changed

| Document | Version | Change |
|---|---|---|
| `system-prd.md` | 1.4.0 | Persona 3 heading is "Aftercare Coordinator - Sarah (Hairline Team)"; Workflow 1 actors name both roles; Aftercare Team Access lines say the patient's 24/7 chat is with the clinic's aftercare specialist, with Hairline coordinators as escalation |
| FR-031 | 1.4 | Admin role renamed in 18 places |
| FR-016 | 1.17 | Admin role renamed in 6 places |
| FR-015 | 1.28 | Admin role renamed in the default role list |
| FR-020 | 2.16 | Admin role renamed in 1 place |
| FR-030 | 1.23 | Admin role renamed in 1 place |
| FR-022 | 2.24 | Admin Users List role filter option renamed; the clinic team role option "Aftercare Specialist" is unchanged |
| FR-011 | 1.12 | Module Scope line and REQ-011-004 name both sides of the assignment |

## Graph

Change-set `graph/changesets/2026-11-23-owner-ruling-aftercare-specialist-clinic-staff.yaml` (17 operations): ten Rule statements updated (REQ-011-004, REQ-016-058, REQ-016-070, REQ-016-073, REQ-016-198, REQ-022-115, REQ-030-095, REQ-031-004, REQ-031-055, REQ-031-056); `ACT-aftercare-specialist` described as clinic staff; new admin-group actor `ACT-aftercare-coordinator`, which now performs step STP-011-008 (Hairline aftercare team takes over patient monitoring) and is linked from REQ-011-054 and REQ-011-057. Lint is unchanged at 31 findings. Backup: `graph/backups/graph-2026-11-23-pre-aftercare-ruling.db`.

## Record

Owner decision: project-root `plans/reports/owner-decisions-261123-0810-phase-09-close-and-phase-10-gate.md`.
