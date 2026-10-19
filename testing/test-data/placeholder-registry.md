# Test Placeholder Registry

**Last Updated:** 2026-10-19

The single list of every account and mailbox placeholder used in the manual test plans. All quotes, prices, invoices and refunds use the system quote currency USD, the FR-029 Default Currency (setup item CUR-USD); only payout currencies differ per provider. Batch files and plans reference placeholders only. Credentials live in [credentials/](credentials/) (internal; sent to the tester privately). Rules: [TEST-STRATEGY.md §6](../TEST-STRATEGY.md).

A placeholder keeps one meaning across all phases. The environment is one shared dev environment whose data persists between phases. Each plan's Phase handoff section lists the account state the team restores before that phase starts.

**Credentials row** says whether a row already exists in `credentials/`. "To create" means the tester creates the account during the pass, at the first batch that needs it, through the product's normal flows using the existing accounts, and shares the login details privately with the plan owner (never in a batch file). The team then adds a row. Seeded data in the environment may stay.

## Accounts

| Placeholder | Kind | Role and state | Phases | Credentials row |
|---|---|---|---|---|
| {A1} | Admin | Super Admin | 1, 2, 3 | Yes |
| {A2} | Admin | Support Staff system role | 1 | To create |
| {A3} | Admin | Billing Viewer role (read-only billing) | 2, 3 | To create |
| {A4} | Admin | Restricted admin 1 | 2 | To create |
| {A6} | Admin | Restricted admin 2 | 2 | To create |
| {A7} | Admin | Second Support Staff admin, needed to reassign a support case away from {A1} | 2 | To create |
| {S1} | Provider staff | {V1} staff, system role Clinical Staff (base and end state of every phase) | 1, 2, 3 | Yes |
| {S2} | Provider staff | {V1} staff, custom role "clinician-front-desk" | 1 | To create |
| {S3} | Provider staff | {V1} staff, Manager role without financial permission | 3 | To create |
| {S4} | Provider staff | {V1} staff, Billing Staff role | 3 | To create |
| {V1} | Provider owner | Primary provider; payout currency USD | 1, 2, 3 | Yes |
| {V2} | Provider owner | Second provider; payout currency EUR | 1, 2, 3 | Yes |
| {V3} | Provider owner | Provider located in Germany; suspended and reactivated within Phase 2; ends Phase 2 Active | 1, 2, 3 | Yes |
| {V4} | Provider owner | Reserved for status changes. Ends Phase 1 Suspended, reactivated in the Phase 2 handoff, ends Phase 2 Suspended, reactivated in the Phase 3 handoff | 1, 2, 3 | Yes |
| {P1}–{P7} | Patient | Owners of prepared inquiry, quote, booking and aftercare data | 1, 2, 3 | Yes |
| {P8} | Patient | No other inquiry; owner of Phase 1 INQ-8, later one Confirmed booking in Phase 2 (TX-8), also used for the B07 BKG-1 conversation | 1, 2 | To create |
| {P9}–{P11} | Patient | No history with {V1} before Phase 2 B07 messaging | 2 | To create |
| {P12}–{P28} | Patient | No earlier history; own the Phase 2 setup records moved off {P3}–{P7} so no patient holds two active inquiries or bookings (FR-003); setup data only | 2 | To create |
| {AF1}–{AF12} | Affiliate | Prepared in the states listed in Phase 3 B04 Shared Preconditions | 3 | To create |

## Mailboxes

All mailboxes are fresh addresses the tester controls (never used on Hairline before the case that uses them; plus-addressing is fine).

| Placeholder | Use | Phases |
|---|---|---|
| {Admin invite mailbox} | Receives the admin invitation | 1 |
| {New provider mailbox 1} | Login email of QA Pilot Clinic 01 | 1 |
| {New provider mailbox 2} | Contact email of QA Pilot Clinic 01; with "+clinic02", of QA Pilot Clinic 02 (plus-addressing) | 1 |
| {New provider mailbox 3} | Login email of QA Pilot Clinic 02 | 1 |
| {Invite mailbox 1} | Admin staff invitation for QA Pilot Clinic 01 | 1 |
| {Invite mailbox 2} | {V1} invitee QA InviteeOne | 1 |
| {Invite mailbox 3} | Validation and rate-limit invitations (plus-addressing) | 1 |
| {Invite mailbox 4} | Expired {V1} invitation setup | 1 |
| {AF13} | Affiliate created during testing | 3 |

## Other Placeholders

| Placeholder | Meaning |
|---|---|
| {Plan owner contact} | Trung Dang (trung.dang@vantaymedia.com): the person the tester contacts for setup requests and questions; written in each plan §3 |
