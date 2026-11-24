# FR-002 Logic Review Pass 1 (2026-11-24)

**Scope**: FR-002 Medical History and head scan intake engine, PRD v1.5 to v1.6, plus a prepared graph change-set that is **not applied yet**.
**Type**: Major update (the engine contract changed: persisted result, derive-only and media-only calls, one version stamp, per-photo response, provider access rules).
**Source of findings**: `plans/reports/tester-261124-fr002-logic-p1.md` (14 findings). Fixer report: `plans/reports/docs-manager-261124-fr002-logic-p1-fixes.md`.

## Files changed

- `functional-requirements/fr002-medical-history/prd.md` (v1.6).
- NEW `graph/changesets/2026-11-24-fr002-logic-p1-fixes.yaml` (prepared, not applied; `write.py` has not been run).

## What changed in the PRD

- **Persisted result**: the engine stores the processing result and returns it on a read by processingId; "no session state between calls" replaces "stateless except artifacts" (new REQ-002-043). Retention follows REQ-SYS-002.
- **One producer of risk tags**: FR-002 derives them, with a derive-only call that persists nothing (new REQ-002-044); highest severity among the Yes answers sets the tier, all No returns one tag with severity none, mapped to Red, Amber and Green as FR-025 REQ-025-064 states.
- **Fixed head scan limits** (owner default 74): photo count, per-file size, formats and views are fixed by the product; the max-file-size, max-total-size and required-views settings no longer govern them. Quality thresholds and video duration stay in FR-026.
- **Active set, not "latest published"**: the request names the set and the version; a prior version or the prior Active set is accepted and recorded, an unknown or never-published version is rejected, and "no Active set" is an error code.
- **One version stamp**: templateVersionUsed with the set identifier; the ruleset stamp is removed.
- **Flow wiring**: the paths around the retired steps are rebuilt, a questionnaire-rejected alternative flow (A3) and a derive-only workflow (Workflow 4) are added, and the distribution step that FR-003 owns is retired.
- **Error codes and audit**: codes cover format, count, size, quality, no photo, unknown version, no Active set and a missing answer, with per-photo detail; a rejected attempt writes an audit row with the rejection reason and stores nothing. The server check is authoritative and the device check advisory (new REQ-002-050).
- **Staging and retries**: photos are staged at capture and promoted at submit; the same idempotency key replaces an earlier artifact set; staged files are removed on the 7-day draft expiry and sit outside the retention rule (new REQ-002-045, REQ-002-046).
- **Request and response**: the V1 request carries the head scan photo set only; headVideo is a future note; the response gives one item per photo (storedUri, validationStatus, qualityScore 0 to 100) and a scanRef.
- **Provider access** (owner default 75): a visible face and free-text answers are a documented exception to REQ-SYS-001; providers get a transformed copy with device and location metadata stripped; access is by a time-limited signed link scoped to the distributed providers (new REQ-002-048, REQ-002-049).
- **Media-only call** for FR-011 and FR-037, with no responses or templateVersion (new REQ-002-047).

## Prepared graph change-set (not applied)

Adds 8 rules (REQ-002-043 to 050), 4 steps, 2 flows and 6 fields (159 operations in all); rewords 22 rules and the affected step and field descriptions; removes the three setting edges named above; moves the photo-set rules to a new request field and retires 4 fields and 1 step. One independent check against graph.db found every id present or created earlier, every removed edge present and no edge touching a retired node.

## Neighbour rows queued (not changed here)

FR-003, FR-025, FR-026, FR-011, FR-037 and the system PRD each have queued rows in `plans/reports/logic-review-ledger.md` (section "FR-002, pass 1").

## Defaults chosen without an owner ruling

Defaults 74 and 75 in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md`; default 75 (face and free text visible before payment) is flagged for the owner to confirm.
