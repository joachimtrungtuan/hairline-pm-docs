# FR-018 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 2.7 to 2.8, with a graph change-set)
**Scope**: FR-018 Affiliate Management
**Source of findings**: `plans/reports/tester-261124-fr018-logic-p1.md` (20 findings; each ruled fix, neighbour-only or settled by the PRD)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md`

- **Usage caps**: a code's Maximum Usage Count and Per-Patient Usage Limit count active reservations plus consumed uses, as FR-019 rules; "applied" means the FR-019 Application made at quote acceptance, and FR-018 adds no separate rate limit (Rule 13, REQ-018-004, REQ-018-053, REQ-018-109).
- **Code entry**: no "checkout" code entry remains. The code is entered or auto-applied on the sub-quote review before the quote is accepted; if validation is unavailable the patient continues without the discount (REQ-018-179, REQ-018-201).
- **Discount priority**: FR-019 owns the priority order and the patient prompt; Rule 3 points to it. Attribution still goes to the affiliate when another discount wins on price (Rule 3, Rule 11, REQ-018-010).
- **Lifecycle**: Rule 12 lists the six allowed transitions (Pending to Active, Pending to Inactive, Active to Suspended, Suspended to Active, Active to Inactive, Suspended to Inactive); Inactive is terminal; the set-password step changes the status only from Pending (REQ-018-052).
- **First code**: onboarding stores the first code's settings; the code is generated only after the affiliate is Active. The Linked Affiliate dropdown lists Active affiliates only. The duplicate activation email is removed so one email is sent at account creation (REQ-018-307, REQ-018-240).
- **Payout figures**: two named figures are used everywhere, "Unpaid balance" and "Next payout amount"; the screen labels are renamed and the field keys are kept (REQ-018-136).
- **Effective date**: "on or after the effective date" everywhere (REQ-018-034, REQ-018-092).
- **Attribution capture**: the last valid affiliate code or link the patient used before accepting the quote gets the attribution; a link click counts for 30 days, a typed code replaces an earlier link, the link carries the affiliate's one Auto-apply code, and the capture is stored with the inquiry journey and read by FR-019 at acceptance (Rule 11, REQ-018-308).
- **FR-019 registration**: generated codes are registered under the affiliate-bound program FR-019 holds; FR-019 owns the rejection reasons, FR-018 shows the returned reason on the failed row and allows retry; the FR-018 code status is FR-018's own on/off record, usage state is read from FR-019 (REQ-018-316, REQ-018-202).
- **Code status by account status**: a disabled-by-account-status marker, separate from the admin Inactive toggle, is set on suspension and offboarding and cleared on reinstatement; Revoked, Inactive and Expired are defined; the Screen 5 toggle and the bulk toggle are blocked while the affiliate is not Active (REQ-018-310, REQ-018-108, REQ-018-120).
- **Suspension and reinstatement**: suspension sets the unpaid commission to payout readiness Manual Review Required with the reason, the monthly run lists it as held, and reinstatement clears the hold and pays all held commission in the next run; the four readiness values are listed. B3 gains three reinstatement steps (Payment Rule 4, REQ-018-311).
- **Bookings in flight and balances**: a booking accepted with the code or link before a status change still earns commission when its final payment is confirmed (held while Suspended, paid in the next run after a normal offboarding, forfeited after a ban); an Inactive affiliate's final balance settles in the next scheduled run, with no admin-initiated final payout; a refund after a Paid payout is a reversal carried forward until cleared (Payment Rules 2, 5 and 6, REQ-018-312, REQ-018-313, REQ-018-097).
- **Completed booking**: means the booking's final payment is confirmed (FR-007); that event sets the accrual month, the effective-date test and Total Referrals (Rule 1, Payment Rule 1, REQ-018-309).
- **Ban**: Screen 3.3 gets a required Offboarding type (Normal offboarding or Permanent ban); a ban sets Settlement Outcome to Forfeit whole balance (ban) and stores a ban flag on the affiliate; permissions follow the FR-031 matrix (Rule 16, B5, B6, REQ-018-317, REQ-018-297).
- **Margin check**: Rule 15 uses the platform default Hairline commission rate at code creation, runs again when the commission is set at onboarding or edited, and at accrual a breaching booking is paid in full and flagged for admin review (REQ-018-041, REQ-018-055, REQ-018-111).
- **Program settings**: a small Affiliate Program Settings panel on Screen 1 edits the payout day (whole number 1 to 28, applied from the next run) and the performance tier bands; each save writes an audit entry (REQ-018-314).
- **Emails**: affiliate account emails go through the notification service (Rule 17, REQ-018-315).
- **Minor**: Pending added to the Screen 1 status list; the duplicate activation email removed.
- Change log row (2.8) and Last Updated set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr018-logic-p1-fixes.yaml`

- New: rules REQ-018-307 to REQ-018-317; steps STP-018-137 to STP-018-139 (reinstatement); fields ENT-affiliate.ban_flag and ENT-affiliate-discount-code.disabled_by_account_status; audit action value settings_changed.
- Retired: STP-018-009 (duplicate activation email), after its edges are removed. The onboarding steps are re-linked so the first code is generated after the password step, at the Active stage.
- Rule statements and some titles updated to mirror the PRD; step, flow, field, screen and setting titles and descriptions updated; Pending payout field renamed Unpaid balance.
- Edges: shows edges relabelled for Unpaid balance and added for the ban flag, the marker and payout readiness; writes edges for the Suspended and Inactive stages; Inactive follows Active and Pending; the new rules are wired with applies at, applies to, governed by and decided by.
- Cross-FR edges: FR-018 references REQ-019-088, REQ-019-116 and REQ-007-036 (rules owned by FR-019 and FR-007). No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 301 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes for FR-019 (attribution read at acceptance, rejection reasons, program picker), FR-005 (storing the attribution capture), FR-031 (permissions for suspend, reinstate, offboard, ban, code generation, commission edit and the settings panel), FR-030 and FR-020 (affiliate account email events) and FR-017 (held and flagged commission on the commission list, readiness values, final-balance pointer) are queued in the logic review ledger section for FR-018 and are not part of this change. Minor observations other than the two fixed above are left as they are and listed under the ledger leftovers.
