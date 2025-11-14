# Module Progress Checklist – PRD Alignment Notes (2025‑11‑12)

This note captures where the **module progress checklist** and the **PRDs** differ, and suggests concrete adjustments per row.  
Conventions:

- `P-xx` – Patient app (API endpoints only; mobile UI is separate)
- `PR-xx` – Provider dashboard (frontend + backend)
- `A-xx` – Admin dashboard (frontend + backend)

Only rows with meaningful gaps or scope mixups are listed.

---

## Patient app – API‑only rows

### P-01 / FR-001 – Auth & Profile

- **Add**: API sub-flow “View & revoke active device sessions”.

### P-02 / FR-003 – Inquiry Submission

- **Add**: “Start inquiry for non‑procedure services (Monitor Hair Loss, Aftercare services)”.
- **Add**: “Enforce system limits: max countries/date ranges/providers, inquiry expiry (72h), max distributed providers (≤10)”.

### P-02 / FR-005 – Quote Comparison & Acceptance

- **Add**: “On acceptance, auto‑cancel all other quotes for the same inquiry with ‘Other quote accepted’ reason”.
- **Add**: “Block acceptance for expired/withdrawn/archived quotes”.

### P-03 / FR-006 – Booking & Scheduling

- **Add**: “Request booking reschedule within allowed window (creates reschedule request)”.
- **Add**: “Apply cancellation policy tiers when cancelling booking (refund calculation)”.

### P-03 / FR-007B – Split Payments / Installments

- **Add**: “Handle failed installment payments (3 retries, then mark plan defaulted and notify admin)”.
- **Add**: “When procedure date changes, recalc remaining schedule or require immediate payoff per rules”.

### P-04 / FR-008 – Travel Booking Integration

- **Add**: “Search roundtrip flights for procedure destination and date range”.
- **Add**: “Select provider‑recommended hotel and book stay”.
- **Add**: “Return booking confirmation and update unified itinerary (flights + hotels)”.

### P-05 / FR-011 – Aftercare & Recovery

- **Add**: “Purchase standalone aftercare service (fixed/subscription pricing via payment API) before request assignment”.

### P-02 / FR-022 – Search & Filtering

- **Clarify scope**: Mark P‑02 search/filter as **P2 / Enhanced (post‑MVP)** to match FR‑022.

### P-06 / FR-012 – Messaging & Communication

- **Add**: “Start conversation with Hairline Support / Aftercare Specialist”.
- **Add**: “Send text + media, view conversation history, see read receipts”.

---

## Provider dashboard – frontend + backend

### PR-01 / FR-009 – Provider Team & Role Management

- **Add**: “Support team member account belonging to multiple provider organizations (multi‑clinic membership)”.
- **Add**: “Protect last Owner role (cannot demote/remove final Owner; must promote another Owner first)”.

### PR-02 / FR-004/005 – Quote Management & Acceptance

- **Add** (FR‑005 side-effect visibility): “Surface auto‑cancel status ‘Other quote accepted’ and final quote state changes in provider quote list/detail”.

### PR-03 / FR-010 – Treatment Execution & Documentation

- **Add**: “Mark booking as No‑Show and apply configured no‑show policy”.
- **Add**: “Mark booking as Postponed – Medical reasons (pre‑start medical issue)”.
- **Add**: “Handle Interrupted treatment (pause, or mark incomplete and reschedule)”.
- **Add**: “Support multi‑day procedures (pause/resume sessions under one treatment record)”.
- **Add**: “Handle ‘patient withdraws consent’ mid‑procedure (mark incomplete, document, trigger follow‑up)”.

### PR-05 / FR-014 – Provider Analytics & Reporting

- **Add**: “Configure scheduled/recurring analytics reports (e.g., weekly/monthly email exports)”.

### PR-06 / FR-012 – Provider Messaging & Communication

- **Add**: “Provider ↔ Admin operational messaging (billing/scheduling clarifications) with notifications and history”.

---

## Admin dashboard – frontend + backend

### A-01 / FR-003 – Admin Inquiry Management

- **Add under FR‑003 (not just FR‑016)**:
  - “Edit inquiry details with warnings + audit trail”.
  - “Reassign inquiries between providers”.
  - “Soft‑delete/archive inquiries with reason”.
  - “Configure inquiry expiration and distribution rules (time limits, provider caps)”.

### A-02 / FR-015 – Provider Management (Admin‑Initiated)

- **Add**: “Configure tier‑based commission structure (tiers by procedure volume; automatic tiering)”.
- **Add**: “Manage document expiry reminders and re‑verification workflows (licenses, insurance, etc.)”.

### A-04 / FR-008 – Travel Management

- **Clarify scope**:
  - Either explicitly mark current “travel inventory & vendor contracts CRUD” as **extended scope beyond FR‑008**,  
  - Or split into a dedicated follow‑up FR (e.g., “Travel Vendor Inventory”) if treated as a separate commitment.

### A-08 / FR-014 – Platform Analytics (Admin)

- **Add**: “Configure and view benchmark settings (segments, thresholds)”.
- **Add**: “Configure scheduled analytics reports for internal stakeholders (e.g., monthly platform analytics email)”.

### A-09 / FR-026 – App Settings & Security Policies

- **Keep in FR‑026**:
  - Auth throttling (max attempts, lockout duration).
  - OTP expiry and resend cooldown configuration.
  - Centrally managed country/calling code lists.
  - Discovery question options.
  - OTP email templates (verification & password reset) with preview and audited changes.

- **Move out of FR‑026 row**:
  - “Configure Stripe account metadata or split payment settings” → move to **FR‑029**.
  - Generic “configure global alerts and notification toggles” (for all event types) → move to **FR‑030**.

- **Re-label**:
  - “Enforce multi‑factor authentication (MFA)” → mark as **future/backlog** (PRDs treat MFA as a future enhancement, not current scope).

### A-09 / FR-027 – Legal Content Management

- **Add**:
  - “Track per‑user legal acceptance (user, document type, version, timestamp, locale)”.
  - “View acceptance coverage dashboard (accepted vs pending, with filters and export)”.

### A-09 / FR-028 – Regional Configuration & Pricing

- **Add**:
  - “Define and edit regional groupings (assign countries to regions)”.
  - “Configure destination display order per region (e.g., Turkey → Poland → UK for UK patients)”.

### A-09 / FR-029 – Payment System Configuration

- **Add**:
  - “Configure deposit percentage (20–30%) globally and/or per provider”.
  - “Configure currency conversion markup (%) and rate‑protection thresholds”.
  - “Map Stripe accounts to specific regions/countries”.

- **Move here from FR‑026**:
  - “Configure Stripe account metadata (credentials per region)”.
  - “Manage split payment rules and toggles (2–9 installments, cutoff rules like 30 days before procedure)”.

### A-09 / FR-030 – Notification Rules & Configuration

- **Add**:
  - “Create/edit non‑OTP notification templates with multi‑language support”.
  - “Test notification rules/templates (preview and send test notification to admin)”.

- **Optionally centralize here**:
  - Any remaining “global alerts & notification categories per tenant” items currently sitting under FR‑026.

### A-10 / FR-012 – Communication Monitoring & Support

- **Add**:
  - “Configure keyword flags and moderation rules; review flagged conversation queue”.
  - “Export/download conversation logs for disputes and compliance reviews”.

- **Ensure explicitly listed**:
  - “Trigger request for 3D scan or schedule review directly from chat context, with audit logging”.

