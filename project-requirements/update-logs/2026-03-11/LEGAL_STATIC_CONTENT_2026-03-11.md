# Legal Static Content Creation - March 11, 2026

## Summary

Created the first publishable draft set of public legal and support pages for Hairline under `local-docs/project-static-content/legal-content/`, aligned to the current project requirements, support workflows, deletion workflow, and retention model.

## Files Added

- `local-docs/project-static-content/legal-content/privacy-policy.md`
- `local-docs/project-static-content/legal-content/terms-of-use.md`
- `local-docs/project-static-content/legal-content/contact-support.md`
- `local-docs/project-static-content/legal-content/account-deletion.md`

## What Was Added

### 1. Privacy Policy

- Added a public-facing privacy policy tailored to the Hairline platform's actual product scope: patient account management, inquiry routing, quote and booking workflows, payments, aftercare tracking, support tickets, treatment media, and medical-data handling.
- Reflected current internal requirements for:
  - minimum 7-year retention of medical and financial records;
  - minimum 7-year retention of audit logs;
  - deletion/anonymization of non-protected data after verified requests where legally allowed; and
  - backup retention windows up to 30 days.
- Included explicit caution around health-related data and avoided unsupported claims about diagnostics or emergency care.

### 2. Terms of Use

- Added public-facing Terms of Use that position Hairline as a technology platform supporting patient-provider workflows, while clearly stating that Hairline is not a hospital, clinic, doctor, or emergency medical service.
- Added conservative language covering:
  - account obligations;
  - acceptable use;
  - quote, booking, payment, and provider relationship boundaries;
  - support communications;
  - user content and uploaded media;
  - privacy linkage; and
  - suspension, deletion, disclaimers, and limitation language.

### 3. Contact Support

- Added a public support page with:
  - support email;
  - in-app support guidance;
  - support hours derived from the current backend support controller configuration;
  - response-time expectations;
  - issue categories; and
  - explicit emergency/medical escalation guidance.

### 4. Account Deletion

- Added a dedicated public account-deletion page designed to support store-review expectations for discoverable deletion instructions.
- Included:
  - in-app deletion path;
  - outside-app deletion request route via support email;
  - verification expectations;
  - 30-calendar-day completion target for verified requests;
  - cases where deletion may be delayed or limited; and
  - retained-record explanation aligned to FR-023 and FR-001.

## Source Basis Used

The new pages were written from existing repository requirements and implementation evidence, including:

- `local-docs/project-requirements/functional-requirements/fr027-legal-content-management/prd.md`
- `local-docs/project-requirements/functional-requirements/fr023-data-retention-compliance/prd.md`
- `local-docs/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`
- `local-docs/project-requirements/functional-requirements/fr034-support-center-ticketing/prd.md`
- `local-docs/project-requirements/functional-requirements/fr035-patient-help-support/prd.md`
- backend implementation references for support email, support hours, legal-document plumbing, and account deletion request APIs

## Key Publication Notes

- The documents are intentionally conservative and aligned to what the project currently documents and implements.
- They avoid unverifiable legal details not present in the repository, such as registered office address, governing-law clause, or region-specific statutory wording.
- Before production publication, Hairline should confirm:
  - the legal entity display name;
  - any registered address or jurisdictional wording required by counsel;
  - whether a second support channel (phone or form) should be published in addition to email; and
  - whether the public account-deletion page should eventually be backed by a web form instead of email-only initiation outside the app.
