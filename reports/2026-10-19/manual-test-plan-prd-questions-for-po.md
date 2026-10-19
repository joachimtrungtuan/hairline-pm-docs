# Manual Test Plan: PRD Questions for the Product Owner

- **Date:** 2026-10-19
- **Purpose:** One list of the PRD conflicts and PRD-silent spots found while writing the manual test cases. The Product Owner decides each one.
- **Source:** `testing/manual/phases/*/v1.0` (plan.md and batch files). Phases 1 to 3 are covered (Phase 4 has no cases yet).
- **PRD paths:** All PRD paths are relative to `project-requirements/functional-requirements/`. Line numbers were checked against the PRDs on 2026-10-19.
- **How to answer:** Write the decision under **Decision** in each item. A short answer is fine (for example "Follow FR-031; FR-016 to be updated"). The team then updates the PRD (Change Log, plus a Change Request if needed) and the affected test cases.

Each item lists the PRD references, what the PRDs say, the question, the affected cases, and how the test plan handles it now.

---

## 1. Cross-phase: Currency

The plans follow the system quote currency from FR-029, FR-026, FR-004 and FR-024: every quote, price, invoice and payment is in the FR-029 Default Currency (`fr004-quote-submission/prd.md` line 370; `fr026-app-settings-security/prd.md` lines 629 and 637). For testing, setup item CUR-GBP sets the Default Currency to GBP with EUR enabled. Payouts follow FR-017, where each provider has its own payout currency. The questions below come from that setup.

### Q-01: Where is a provider's payout currency set?

- **PRD refs:** `fr017-admin-billing-finance/prd.md` line 1160 (Screen 10 Business Rules), line 491 (Screen 3 Business Rules); `fr015-provider-management/prd.md` lines 615–621 (Tab 7 Commission & Financials fields); `fr032-provider-dashboard-settings/prd.md` line 1149 and REQ-032-029 (line 2020).
- **What the PRDs say:** FR-017 says that payouts and their amounts use "the provider's configured payout currency" and that the commission is "converted to the payout currency". No screen sets this value. FR-015 Tab 7 has Commission Model, Commission Value, Flat Rate Currency, Effective Date and Payout Frequency, but no payout currency. The FR-032 provider Commission & Payout panel does not show one either.
- **Question:** Which screen sets a provider's payout currency, and who sets it (admin in FR-015, provider in FR-032, or something derived from the bank account country)? If none is set, should the payout currency fall back to the Flat Rate Currency or the system Default Currency?
- **Affected cases:** Phase 3 Team Setup Checklist item 3 (`{V2}` paid in EUR); PR05-FR017-02; A05-FR017-19, A05-FR017-20, A05-FR017-27; A02-FR015-24.
- **Current handling:** The dev team sets `{V2}`'s payout currency to EUR as a setup step outside any tested screen. Cases check only the result (EUR amounts).
- **Decision:** Deferred (2026-10-19). The payout currency setting comes with the client's updated payout requirements, which will be added to the PRDs first. Payouts are tested in Phase 3, not Phase 1, so this does not block earlier phases. The Phase 3 payout cases will be revised once those requirements are in.

### Q-02: Which currency do the Earnings Tracker (Screen 9) amount columns use?

- **PRD refs:** `fr017-admin-billing-finance/prd.md` line 1077 (Screen 9 Gross Amount, "Display: £X,XXX.XX"), line 1082 (Screen 9 Currency column, "Treatment currency"), line 1150 (Screen 10 Currency column, "Booking currency"), line 1160 (Screen 10 rule: amounts in payout currency).
- **What the PRDs say:** Screen 9 does not say whether Gross Amount, Commission Deducted and Net Earning are in the quote (booking) currency or the payout currency. On Screen 10, the Currency column says "Booking currency", but the Business Rule says that all amounts are shown in the payout currency.
- **Question:** For a provider paid in a currency other than the booking currency (GBP booking, EUR payout), do the Screen 9 and Screen 10 amounts and Currency column show the booking currency, the payout currency, or both?
- **Affected cases:** PR05-FR017-02 (data set DS-PR05-02, setup BK-16); Screen 10 history checks for `{V2}` in Phase 3 B01.
- **Current handling:** PR05-FR017-02 expects EUR amounts in `{V2}`'s payout currency, converted at the locked rate. This applies the Screen 10 rule to Screen 9.
- **Decision:** Payout currency (2026-10-19). Screen 9 and Screen 10 amounts and the Currency column show the provider's payout currency. The current handling stands; the FR-017 Screen 10 Currency column wording ("Booking currency", line 1150) needs a PRD correction.

### Q-03: How is a GBP to EUR rate worked out when all currency pairs are based on USD?

- **PRD refs:** `fr029-payment-system-config/prd.md` line 526 (Screen 2B Base Currency "Always USD — not editable"), line 530 (Manual Base Rate "units of target currency per 1 USD"); `fr017-admin-billing-finance/prd.md` line 491 (conversion at the rate locked at acceptance) and Screen 8 Currency Alert Detail Modal (line 1008).
- **What the PRDs say:** Each FR-029 currency pair is USD to a target currency. With GBP as the Default Currency and EUR as a payout currency, a booking needs a GBP to EUR rate. The PRDs do not say how that rate is derived (for example a cross rate through USD, and whether the markup applies once or on both legs). They also do not say which pair a GBP to EUR currency alert watches.
- **Question:** How is a non-USD rate such as GBP to EUR worked out and locked at acceptance? Does markup apply to each USD leg or to the cross rate? Is the alert threshold checked on the cross rate?
- **Affected cases:** Phase 3 B02 setup item FX-1 (locked rate 1 GBP = 1.20 EUR); PR05-FR017-02; A05-FR017-19, A05-FR017-20, A05-FR017-27; A05-FR017-37 (CA-1, GBP to EUR alert).
- **Current handling:** The dev team sets the FR-029 rates (for example Manual mode, Markup 0%) so that each `{V2}` booking locks 1.20, and records the actual locked rate. If the recorded rate is different, the expected EUR figures are recalculated from it.
- **Decision:**

### Q-04 (note only): Default currency seed is USD

- **PRD refs:** `fr029-payment-system-config/prd.md` line 722 (Screen 6 Notes: "the MVP seed value is USD").
- **What the PRDs say:** The MVP seed Default Currency is USD. The test environment changes it to GBP (setup item CUR-GBP), so the FR-017 Revenue Dashboard reporting currency also starts in GBP.
- **Question:** No decision is needed unless GBP should also be the production seed. Please confirm that testing with GBP as the Default Currency is acceptable.
- **Affected cases:** Phase 1 plan.md Team Setup item 2 (CUR-GBP); every Phase 1 and Phase 3 price expectation.
- **Current handling:** The team sets GBP before B01.
- **Decision:**

---

## 2. Phase 1: Controlled Commercial Pilot

### Q-05: Does a soft-deleted (Archived) quote stay visible to the provider? (FR-004 vs FR-022)

- **PRD refs:** `fr004-quote-submission/prd.md` line 156 (Workflow 4: soft delete "removes from provider listing"), line 80 (Main Flow: provider dashboard has "archive bins"); `fr022-search-filtering/prd.md` line 629 (Module PR-02 provider Quote Status filter includes "Archived"), line 916 (Module A-01 admin filter includes "Archived").
- **What the PRDs say:** FR-004 Workflow 4 removes a soft-deleted quote from the provider listing. However, the FR-004 Main Flow mentions provider "archive bins", and the FR-022 provider Quote Status filter offers "Archived".
- **Question:** After a soft delete (by the provider or an admin), can the provider still find the quote under an Archived filter or bin, and is it read-only there? Or is it fully hidden from the provider (in which case "Archived" is removed from the FR-022 provider filter)?
- **Affected cases:** PR02-FR004-12 (step 4); A01-FR004-06 (step 2).
- **Current handling:** Tester observation only, not a pass or fail condition: the tester records whether the quote appears under the provider Archived filter and with what status.
- **Decision:**

### Q-06: What status does a restored quote return to?

- **PRD refs:** `fr004-quote-submission/prd.md` line 159 (Workflow 4: soft deletes are "revertible only by admin"), line 170 (Workflow 5: admin can soft delete or restore).
- **What the PRDs say:** An admin can restore a soft-deleted quote, but the PRD does not give the status after restore. It also does not say what happens if the quote's expiry time passed while it was archived.
- **Question:** Does a restored quote go back to its status before archiving (for example Sent)? If its expiry time passed while archived, does it become Expired at restore?
- **Affected cases:** A01-FR004-06 (step 3).
- **Current handling:** The case expects Sent (it restores within the 72-hour window) and asks the tester to record what is shown.
- **Decision:**

### Q-07: Admin role model: single Super Admin role (FR-016) or custom roles and several Super Admins (FR-031)?

- **PRD refs:** `fr016-admin-patient-mgmt/prd.md` line 37 (Module Scope: "MVP ships with a single Super Admin role"), line 681 (Business Rule 3: "granular RBAC is deferred"), line 910 (Security: "Single Super Admin role ... additional RBAC tiers deferred"); `fr031-admin-access-control/prd.md` lines 370–371 and 379 (Screen 1 Tab 2 Admin Users), line 995 (Business Rule 4), lines 1334–1338 (User Story 6).
- **What the PRDs say:** FR-016 describes one Super Admin role with no custom roles in MVP. FR-031 defines custom admin roles, several Super Admin accounts, and protection for the last Super Admin. FR-031 also conflicts with itself: line 370 says Super Admin accounts "cannot be suspended by other users", but User Story 6 scenario 2 (line 1336) has a Super Admin suspend one of two Super Admins successfully.
- **Question:** (a) Is FR-031 (custom admin roles plus several Super Admins) the MVP model, so that FR-016 should be updated? (b) Can one Super Admin suspend another when two or more exist?
- **Affected cases:** A09-FR031-01, A09-FR031-03, A09-FR031-09; A01-FR031-01.
- **Current handling:** The cases follow FR-031. A09-FR031-09 tests only the single-Super-Admin protection. The case where one Super Admin suspends another is not tested.
- **Decision:**

### Q-08: Can an admin edit patient medical questionnaire answers? (FR-016 vs FR-003)

- **PRD refs:** `fr016-admin-patient-mgmt/prd.md` line 680 (Business Rule 2: "Admins MUST NOT modify patient medical data"), line 712 (Admin Editability Rules, Fixed: medical questionnaire responses immutable); `fr003-inquiry-submission/prd.md` line 1111 (Admin Editability Rules: "Medical Data: Edit questionnaire responses and alerts"), line 1101 ("Admin can edit ALL inquiry data").
- **What the PRDs say:** FR-016 makes medical data read-only for admins. FR-003 lets admins edit questionnaire responses and alerts on the inquiry.
- **Question:** Can an admin edit the medical questionnaire answers and alerts held on an inquiry, with a reason and an audit entry? Or are they read-only everywhere for admins, in which case FR-003 line 1111 is removed?
- **Affected cases:** A01-FR016-03 (step 4 expects read-only); A01-FR003-05 (edits only the Requested Date Range).
- **Current handling:** The cases follow FR-016: medical data is read-only, and the FR-003 admin edit case avoids medical fields.
- **Decision:**

### Q-09: Who can remove or suspend provider team members? (FR-009 vs FR-031)

- **PRD refs:** `fr009-provider-team-roles/prd.md` lines 238 and 244 (Main Flow: Remove Team Member, actor "Provider Owner/Admin"), line 1148 (REQ-009-005: "Owners and Managers"), line 802 (Admin Editability: "bypasses Owner-only rule"); `fr031-admin-access-control/prd.md` line 763 (Screen 4 Permission Matrix, Team Management: "Remove Team Members ... Write (Owner only)").
- **What the PRDs say:** FR-009 lets the Owner and the Manager (or "Admin") remove non-Owner members. The FR-031 permission matrix and FR-009 line 802 make removal Owner-only.
- **Question:** Can a Manager remove or suspend team members, or only the Owner?
- **Affected cases:** PR01-FR009-14, PR01-FR009-16.
- **Current handling:** Both cases run removal and suspension as the Owner only. Removal by a Manager is not tested.
- **Decision:**

### Q-10: Removal reasons: which predefined list, and is a reason required?

- **PRD refs:** `fr009-provider-team-roles/prd.md` line 407 (Screen 4 Remove or Suspend modal: Removal Reason, Required "Yes", "Predefined reasons"), line 258 (Main Flow step 12: "reason (if provided)").
- **What the PRDs say:** The modal has predefined reasons, but the PRD does not list them. Screen 4 makes the reason required, while the Main Flow treats it as optional.
- **Question:** What are the predefined removal and suspension reasons? Is a reason required?
- **Affected cases:** PR01-FR009-14, PR01-FR009-16 (data set DS-PR01-07).
- **Current handling:** The tester chooses the first predefined reason and records its value.
- **Decision:**

### Q-11: Is a confirmation shown when deactivating a package used in no open quotes?

- **PRD refs:** `fr024-treatment-package-management/prd.md` line 279 (Alternative Flow A5 step 4: warning "This package is used in N open quotes..."), line 467 (Screen 4: warning shown "when open quotes contain an option copied from this package").
- **What the PRDs say:** The warning is defined only when open quotes use the package. The PRD does not say whether any confirmation appears when N is 0.
- **Question:** With 0 open quotes, should Deactivate ask for confirmation (and with what text), or apply at once?
- **Affected cases:** PR06-FR024-15 (step 3).
- **Current handling:** Tester observation: the tester records whether a confirmation is shown and its text.
- **Decision:**

### Q-12: What happens on the 4th activation resend within an hour?

- **PRD refs:** `fr015-provider-management/prd.md` line 185 (Alternative Flow A1: "Rate limited to 3 resend requests per hour per email address").
- **What the PRDs say:** The PRD sets the limit but not what the provider sees when it is exceeded.
- **Question:** Should the 4th request be refused with a visible message, or show a neutral message without sending an email (so that registered addresses are not revealed)?
- **Affected cases:** A02-FR015-10.
- **Current handling:** Either behavior passes as long as no 4th email is sent. The tester records the text.
- **Decision:**

### Q-13: What file format does the provider Activity Log export use?

- **PRD refs:** `fr015-provider-management/prd.md` line 665 (Screen 3 Tab 8: "Admin can export activity log for compliance reporting").
- **What the PRDs say:** Export is required, but the format and columns are not given.
- **Question:** Which format (CSV, PDF, or other) and which columns should the export use?
- **Affected cases:** A02-FR015-19 (step 4).
- **Current handling:** The tester records the format of the downloaded file.
- **Decision:**

---

## 3. Phase 2: Clinical and Patient Operations

### Q-19: Which screen resolves the `supportRequired` marker when an In Progress booking moves to Aftercare?

- **PRD refs:** `fr006-booking-scheduling/prd.md` line 199 (Alternative Flow B7 step 3: "the admin's decision resolves the `supportRequired` marker"), line 187 (Alternative Flow B6 step 4: "The admin's reassignment resolves the `supportRequired` marker"), line 796 (Screen 11: Resolve In-Progress Provider Fault); `fr011-aftercare-recovery-management/prd.md` line 357 (Workflow 4 D5: reassignment "resolves the `supportRequired` marker when one is set"), line 1283 (Screen 19 "Resolve Support Marker" checkbox, checked by default), line 1292 (resolution recorded "when selected").
- **What the PRDs say:** For the B7 route "Move to Aftercare and reassign", FR-006 says the decision on Screen 11 resolves the marker. That route then opens FR-011 Screen 19, where the reassignment resolves it, and an optional checkbox there can leave it unresolved.
- **Question:** Is the marker resolved on FR-006 Screen 11 (decision) or on FR-011 Screen 19 (reassignment)? If an admin decides on Screen 11 but leaves Screen 19 without reassigning, is the booking left in Aftercare with no provider and the marker still set? Can the admin untick "Resolve Support Marker"?
- **Affected cases:** A01-FR006-09 (Phase 2 B02), A03-FR011-07 (Phase 2 B04).
- **Current handling:** A01-FR006-09 passes whether the marker is resolved on Screen 11 or through the ticked Screen 19 checkbox, and the tester notes which route was seen. A03-FR011-07 expects the checkbox shown and ticked and the marker resolved after reassignment.
- **Decision:**

### Q-20: Can admins see earlier versions of a corrected passport record?

- **PRD refs:** `fr008-travel-booking-integration/prd.md` line 695 (Screen 12 Tab 1: "the previous version is retained in the system's backend records"), line 731 (flight correction marks the previous version as superseded), lines 820 and 828 (flight and hotel: "superseded admin-correction versions remain in history"), line 1017 (both versions retained in the audit log).
- **What the PRDs say:** For passports, the earlier version is kept only "in the system's backend records". For flights and hotels, superseded versions "remain in history". Screen 12 defines no version history view for any record.
- **Question:** Should Screen 12 show a visible version history (earlier passport values and photo, who corrected it, and the reason)? Or is the history only in the audit log?
- **Affected cases:** A04-FR008-07 (Phase 2 B05).
- **Current handling:** No on-screen version history is expected; the case checks the correction through Audit & History.
- **Decision:**

### Q-21: Can a patient have a second treatment start while one is In Progress? (FR-010 vs FR-003)

- **PRD refs:** `fr010-treatment-execution/prd.md` line 558 (Rule 7); `fr003-inquiry-submission/prd.md` lines 730 and 1011 (one active inquiry per patient).
- **What the PRDs say:** FR-010 Rule 7 guards against two treatments In Progress for one patient. FR-003 already allows only one active inquiry per patient, so the state Rule 7 guards against cannot be prepared through the product.
- **Question:** Is Rule 7 still needed, or should it be removed from FR-010? If it is needed, how can a patient reach two Confirmed bookings?
- **Affected cases:** PR03-FR010-05 (Phase 2 B01), now Retired because its setup cannot be created.
- **Current handling:** Case retired; it returns if the PO confirms a path to two Confirmed bookings.
- **Decision:**

### Q-22: Treatment reminders: wording and where the Overdue Documentation flag appears

- **PRD refs:** `fr010-treatment-execution/prd.md` line 919 (Rule 6, 12h and 24h reminders).
- **What the PRDs say:** Reminders fire at 12h and 24h and a case becomes overdue, but no reminder text, channel, or location of the Overdue Documentation flag is defined.
- **Question:** What does each reminder say, where does the provider see it, and where is the overdue flag shown?
- **Affected cases:** PR03-FR010-20, PR03-FR010-21 (Phase 2 B01).
- **Current handling:** The team triggers the reminder job (setup RM-1); the tester records the text and where the flag appears.
- **Decision:**

### Q-23: How does a provider assign a clinician to an aftercare case?

- **PRD refs:** `fr011-aftercare-recovery-management/prd.md` Screens 8 to 12 (lines 652 to 859) define no clinician assignment; only the release roadmap names the function.
- **What the PRDs say:** The provider aftercare screens have no assignment control or rule.
- **Question:** Is clinician assignment in scope for PR-04? If so, which screen, which roles can be assigned, and what does the assignee see?
- **Affected cases:** PR04-FR011-14 (Phase 2 B03).
- **Current handling:** Observation only; the tester records whether and where assignment exists.
- **Decision:**

### Q-24: How is the copy-source reference shown after a provider-fault transfer?

- **PRD refs:** `fr008-travel-booking-integration/prd.md` lines 806 and 895 (Acceptance Scenario 9: passport carry-over and travel copied for review).
- **What the PRDs say:** Travel records are copied to the replacement booking for review, but how the link to the source booking is displayed is not stated.
- **Question:** What does the admin see on the copied record that names its source booking?
- **Affected cases:** A04-FR008-13 (Phase 2 B05).
- **Current handling:** The tester records how the source is shown.
- **Decision:**

### Q-25: Which status does a quote show in messaging when its inquiry was cancelled?

- **PRD refs:** `fr012-secure-messaging/prd.md` line 359.
- **What the PRDs say:** The conversation context shows the quote, but the status for a quote whose inquiry was cancelled is not defined.
- **Question:** Should the conversation show the FR-004 status "Cancelled (Inquiry Cancelled)" or something else?
- **Affected cases:** PR07-FR012-02 (Phase 2 B07).
- **Current handling:** The tester records the status shown.
- **Decision:**

### Q-26: Aftercare pricing in "all supported currencies" vs a single system quote currency

- **PRD refs:** `fr011-aftercare-recovery-management/prd.md` line 1127; `fr029-payment-system-configuration/prd.md` Screen 6 (single Default Currency); `fr024-treatment-package-management/prd.md` (providers price in the system quote currency).
- **What the PRDs say:** FR-011 asks for aftercare pricing in all supported currencies; every other price in the system uses the one system quote currency.
- **Question:** Should aftercare plans be priced in the system quote currency only?
- **Affected cases:** A03-FR011-12 (Phase 2 B04).
- **Current handling:** The case expects GBP prices only. If save is blocked only because another currency has no price, the tester copies the message and marks the case Blocked.
- **Decision:**

---

## 4. Phase 3: Settlement and Partner Growth

### Q-14: Can a Paused promotion be resumed? (FR-019 row actions vs lifecycle)

- **PRD refs:** `fr019-promotions-discounts/prd.md` line 238 (Screen 1 Promotion Program Hub row actions: "Pause / Resume"), line 562 (Screen 8 My Promotions row actions: "Edit / Pause / Resume / Archive"), line 281 (Screen 2 Lifecycle State: "Draft → Active → Paused → Expired → Archived", "Forward transitions only").
- **What the PRDs say:** Both row-action lists offer Resume (Paused back to Active). The Screen 2 lifecycle allows forward transitions only.
- **Question:** Is Resume (Paused to Active) allowed? If it is, the Screen 2 lifecycle rule needs that exception. Is Archived final?
- **Affected cases:** A06-FR019-06 (step 3 and step 4).
- **Current handling:** The case tests Resume as the row actions list it, and treats Archived as final (no Resume after Archive).
- **Decision:**

### Q-15: Is promotion code uniqueness case-insensitive?

- **PRD refs:** `fr019-promotions-discounts/prd.md` line 276 (Screen 2 Code(s): "uniqueness enforced"), line 567 (Screen 8 Business Rules: "Code uniqueness enforced platform-wide"), line 589 (Screen 9 Code: "uniqueness platform-wide").
- **What the PRDs say:** Codes must be unique across the platform. The PRD does not say whether "V1SELF15" and "v1self15" count as the same code, or how codes are matched at redemption.
- **Question:** Are codes unique and matched without regard to letter case?
- **Affected cases:** A06-FR019-05 (step 2).
- **Current handling:** The case expects a case-insensitive check. If the lowercase code saves, the tester marks Fail and notes it for product review.
- **Decision:**

### Q-16: What does a staff member see when opening a financial page by direct link without permission?

- **PRD refs:** `fr014-provider-analytics-reporting/prd.md` line 1472 (Rule 15B: widgets the user cannot see are not rendered and not requested), line 1473 (Rule 15F: default role access matrix).
- **What the PRDs say:** The rules cover hiding widgets and navigation. They do not say what happens when a user without financial access pastes the Finance & Payouts page address.
- **Question:** Should the user be redirected (to where), shown an access-denied message, or shown an empty page?
- **Affected cases:** PR05-FR014-05 (step 3).
- **Current handling:** Pass if no financial figures are shown. The tester records whether the page redirects, shows a message, or is empty.
- **Decision:**

### Q-17: Does a later statement pick up a treatment completed after its period's statement was generated?

- **PRD refs:** `fr017-admin-billing-finance/prd.md` lines 485–489 (Screen 3 Business Rules: a payout includes all Completed or Aftercare treatments "within the payout period"; the period is the preceding week, half-month or month), Alternative Flow B1 and Screen 7 Dispute Resolution Panel ("Add to Next Payout").
- **What the PRDs say:** A statement covers treatments within its own payout period. The PRD does not say whether a treatment from an earlier period that becomes Completed after that period's statement was generated is (a) picked up automatically by the next statement, or (b) left out until an admin adds it through the dispute "Add to Next Payout" action.
- **Question:** Which is intended: automatic catch-up in the next statement, or manual add through a dispute? If catch-up is automatic, should the next statement mark the treatment as late?
- **Affected cases:** A05-FR017-35, A05-FR017-36 (setup ST-15 and BK-19, with statements ST-6 and ST-4 for `{V4}` in Phase 3 B02).
- **Current handling:** The plan assumes no automatic catch-up. Before the session, the team confirms that BK-19 is not in ST-6 or ST-4. If a later statement included it, the dispute case cannot run as written.
- **Decision:**

### Q-18: Is an admin change reason over 500 characters rejected or cut off?

- **PRD refs:** `fr015-provider-management/prd.md` line 436 (Screen 3: "Reason for change" min 10 chars, max 500 chars).
- **What the PRDs say:** The PRD gives the limits but not what happens to a longer reason.
- **Question:** Should a reason over 500 characters be blocked with a message, or cut off at 500 characters?
- **Affected cases:** A02-FR015-25 (step 5).
- **Current handling:** Either behavior passes. The tester notes which one happens.
- **Decision:**

---

## Not raised as questions

Many cases ask the tester to record message text, control labels, or menu paths where the PRD gives none (for example "the PRD gives no exact text; record it", "Note the message shown"). These are wording and labeling gaps, not behavior decisions, so they are not listed above. The tester's recorded text can feed later PRD copy updates.
