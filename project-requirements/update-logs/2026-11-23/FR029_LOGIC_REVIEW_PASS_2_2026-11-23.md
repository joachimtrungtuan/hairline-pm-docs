# FR-029 Logic Review Pass 2 (2026-11-23)

## What changed

- **PRD:** `functional-requirements/fr029-payment-system-config/prd.md` is now v1.18.
- **Graph:** a prepared change-set `graph/changesets/2026-11-23-fr029-logic-p2-fixes.yaml` (148 operations). It is written and checked on a scratch copy of `graph.db`. It is **not applied** to the live graph.
- Nothing outside FR-029 was edited. Items in neighbour PRDs are queued, not fixed.

## Decisions applied in the PRD

- **Rate set locked at quote acceptance:** the acceptance snapshot stores, for the quote currency, the currency shown to the patient and the Fee Currency, the base rate and the markup, each with its timestamp. Every later conversion reads that set only: displays and payments in the shown currency, the USD charge, the installment eligibility check (base rate, no markup) and fixed fees. The USD fallback now converts at the quote-to-USD rate in the set, with the markup; "no conversion is attempted" is removed.
- **Fixed fee amounts and the default currency:** Screen 7 cannot be saved after a Default Currency change until each fixed amount (late fee, rescheduling fee, clinic cancellation deduction) is re-entered in the new currency. Each amount is stored and locked with its currency code. A currency in use as the Fee Currency cannot be disabled.
- **Starting values:** the late fee, the rescheduling fee and the clinic deduction start as "Not set" and no such fee is charged while unset; a fixed amount, once set, must be above 0; the grace period starts at 0 days (the fee still waits for the automatic retries to end).
- **Balance due days:** locked at booking confirmation; FR-007 stores the balance due date on the booking. A booking confirmed with this many days left, or fewer, gets full payment only. One term, "procedure date", throughout.
- **Cancellation point:** counted from the oldest unpaid due date (the oldest installment or balance that is unpaid right now); a late payment restarts the count from the next unpaid one. Screen 4 and Screen 7 warn, without blocking the save, when the point falls before the day the late fee would be charged (the later of the end of the grace period and the day the last FR-007B retry runs).
- **Routing:** countries of an Inactive or Archived account are treated as unassigned (Global Fallback, else blocked with the missing-account alert), and such an account may hold no countries; Alternative Flow A1 refuses an override that leaves another account with no countries. Live accounts on production and Test accounts elsewhere. When the mapped account fails authentication new bookings use the Global Fallback, routing returns when the account's next connection test passes, and a failing Global Fallback blocks the booking through B6. Payment methods are checked against the charge currency.
- **Rate protection:** after Acknowledge the pair is compared with the rate at that moment until the 24-hour change is again within the threshold; no comparison runs for 24 hours after a pair is created or switched between modes.
- **Provider deposit rates:** a provider-specific rate is reset to the global default (new Alternative Flow A2b), never deleted; existing bookings keep their rate.
- **Unset share:** holders of the Screen 7 permission see a dashboard banner while Hairline's share is Not set; it clears when the share is saved.
- New requirements REQ-029-157 (cancellation point warning) and REQ-029-158 (Reset to global default).

## Graph change-set summary

- 30 Rules, 11 Settings, 15 entity fields, 2 entities, 15 Steps, 7 Screens and 1 Event updated; the four fee type and value fields become optional.
- New Rules REQ-029-157 and 158; new Steps STP-029-179 (override check in A1) and STP-029-180 to 184; new flow FLW-029-alt-provider-deposit-reset. The A1 step chain gains the new step and later steps are renumbered in their PRD references.
- Wording residue fixed: "deposit plan", "treatment date", "fewer days" and the "never cancels" lines.
- Scratch validation: `write.py` applied it (197 change rows); `lint.py --json` count 27, the same as the baseline, with the same findings.

## Queued, not fixed here

- FR-005: the acceptance snapshot field list (rate set with the Fee Currency).
- FR-031: the role that holds the Screen 7 permission.
- FR-007: stored balance due date; handling of the Not set fees and share.
- FR-007B and FR-006 B8: "oldest unpaid due date" wording; FR-007B reading the retry end day.

Full per-finding detail: `plans/reports/docs-manager-261123-fr029-logic-p2-fixes.md`.

## Applied

The controller applied the change-set to the live graph on 2026-11-23 (197 change rows, backup `graph/backups/graph-2026-11-23-pre-fr029-logic-p2.db`). Lint count 27, equal to the baseline. `graph.json` re-exported.
