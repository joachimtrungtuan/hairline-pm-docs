## Project Accounts Register

This document tracks external service accounts used by the Hairline project in a **structured, expandable** format for easy later querying.

### Conventions

- **ID**: Stable identifier you can reference in other docs/tasks (e.g. `ACCT-001`).
- **Environment**: `prod`, `staging`, `sandbox`, `dev`, or `shared`.
- **Owner**: Person primarily responsible for managing the account.
- **Credential storage**: Prefer a password manager; try to avoid long-term plaintext passwords in this file.

> Note: If you must temporarily record secrets here, mark them clearly and plan to migrate them into a secure vault as soon as possible.

---

### Account Index

| ID       | Service | Purpose                          | Environment | Account Email         | Owner      | Notes                          |
|----------|---------|----------------------------------|-------------|-----------------------|------------|--------------------------------|
| ACCT-001 | Twilio  | Audio/video chat functionality   | shared      | (TBD)                 | Mr. Phương | Used for realtime A/V features |
| ACCT-002 | Stripe  | Payments and billing             | shared      | <admin@hairline.app>    | Mr. Mohamed Taha | Main Stripe account            |

---

### ACCT-001 – Twilio (Audio/Video Chat)

- **Service**: Twilio
- **Purpose**: Audio/video chat functionality for Hairline applications
- **Environment**: `shared` (used across multiple environments; refine later if needed)
- **Owner / Creator**: Mr. Phương
- **Account Email / Login**: **TBD** (update once confirmed)
- **Console URL**: `https://www.twilio.com/console`
- **Credential Storage**: **TBD** (e.g. password manager entry name, vault path)
- **Notes**:
  - Used for realtime audio/video chat features.
  - API keys, secrets, and auth tokens should be stored in a secure vault or environment variables, not directly in source control.

---

### ACCT-002 – Stripe (Payments)

- **Service**: Stripe
- **Purpose**: Payment processing, subscriptions, and billing for Hairline
- **Environment**: `shared` (refine into separate prod/test accounts if applicable)
- **Owner / Creator**: **TBD** (e.g. project owner or finance contact)
- **Account Email / Login**: `admin@hairline.app`
- **Console URL**: `https://dashboard.stripe.com/`
- **Credential Storage**:
  - Find in the Slack thread about Stripe account creation.
  - Move this password into a secure password manager or vault and then remove/obfuscate it here.
- **Notes**:
  - Consider creating and documenting separate Stripe accounts or API keys for `test` vs `prod`.
  - API keys and webhook secrets should be managed via environment variables and not committed to repositories.
