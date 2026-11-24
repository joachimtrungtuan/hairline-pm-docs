# FR-035 Logic Review Pass 1 - 2026-11-24

**Scope**: FR-035 Patient Help Center and Support Submission. PRD version 1.3 to 1.4.
**Type**: PRD logic fixes plus a prepared graph change-set (cross-document alignment with FR-034, FR-030, FR-026, FR-001, FR-033, FR-022, FR-023 queued as neighbour rows).
**Findings addressed**: 24 reviewed; 21 closed on the FR-035 side; 3 queued for neighbours only (P1-16, P1-17, P1-20).

## What changed in the PRD

- Entry Points: a Report a Problem row on the Hub, and a not-logged-in entry that shows only the support phone and email.
- Hub: emergency phone and email rows are shown only when their setting has a value.
- Notices: confirmation and resolution emails follow the Admin notification settings; the in-app confirmation always shows. Patient-facing response time reads "within 24 hours on business days" everywhere.
- Closure: with the Immediately period there is no Resolved window and no countdown; the last day reads "closes today". The Closed Case Banner Contact Support link opens an email to the support address with the case ID in the subject.
- Ticket Detail: shows the original request (description and initial attachments); a reply sent after closure is refused, the typed text is kept.
- Flows: A3 redrawn without the retired validation step (email and confirmation in parallel); A5 gains the reopening notice to the admin; new A6 (Resolved case closes) and B3 (submission cannot complete now: offline queue, rate limit, scanner unavailable, storage unavailable).
- Content: content-type visibility toggle removed (four cards always shown); related content is up to 4 when configured in FR-033; the Contact Support prompt follows No on every content type; category picker shows current labels with the two internal categories hidden.
- Account deletion: open, In Progress and Resolved cases stay with the Admin; notices stop.
- Scan failure message is taken from FR-034 by reference.

## Graph

Change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr035-logic-p1-fixes.yaml` is prepared, test-applied on a copy of the graph without errors, and not applied to the live graph by the author. The controller applies it.

## Neighbour rows queued (not edited here)

FR-001 (not-logged-in entry, Settings route), FR-034 (banner email wording, A5 duplicate chain, category patient-visible attribute, deleted-patient notices, "business days" wording, optional scanner-unavailable line), FR-026 (emergency settings required or blank hides a row), FR-030 (stub event descriptions, switchability check), FR-033 (patient write endpoints), FR-022 (search and list rules), FR-023 (anonymised address and no notices). The rows are in the logic review ledger section for FR-035 pass 1.

## Evidence

Findings: `plans/reports/tester-261124-fr035-logic-p1.md`. Fix detail per finding: `plans/reports/docs-manager-261124-fr035-logic-p1-fixes.md`.
