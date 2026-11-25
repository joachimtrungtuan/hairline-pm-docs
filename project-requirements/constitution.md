# Hairline Platform Constitution

**Version**: 1.1.1
**Ratified**: 2025-10-23
**Last amended**: 2026-11-25 (rules corrected to agree with the system PRD and the FR PRDs; see the change log)
**Structure revised**: 2026-11-25 (restructure and merge of the executive summary)

This is the single canonical constitution for the Hairline medical tourism platform (four tenants: Patient app, Provider web, Admin web, Affiliate web portal). It states the principles, security and compliance rules, PRD standards and governance that every functional requirement, PRD, plan and code change is checked against. Part E (Constitution Authority) states what it supersedes and how a deviation is justified. The path `.specify/memory/constitution.md` is kept for Spec Kit and the project skills.

Rule wording is the ratified wording except where the change log records a correction. Rule ids (`C-I-1`, `C-SEC-3`, and so on) are labels added for citation; they carry no meaning beyond identifying a line. The original Roman numerals and section headings are kept, so a citation such as "Principle II" resolves to the heading "II. Medical Data Privacy & Security".

The system PRD (`system-prd.md`, section "Platform-Wide Rules") and this document both state some cross-cutting rules. Where this document disagrees with the system PRD or the FR PRDs, it is corrected to match them (owner ruling 2026-11-25).

## How to use this document

| Task | Read | Notes |
|---|---|---|
| Verify an FR against the constitution | Part A, then Part B | Cite rule ids. A NON-NEGOTIABLE principle (I, II, V) or the NON-NEGOTIABLE PRD Standards in Part C cannot be waived without the Part E complexity process. |
| Review code or a plan | Part A, Part B, Part D (Development Standards) | Lines labelled `C-DEV` carry the code-review, commit, coverage and test-data rules. |
| Write or review a PRD | Part C | Section structure of a compressed PRD follows `graph/checklists/prd-structure.md`; see Part C. |
| Place a new document | Part C (Documentation Organization) | Layout trees are in Part D and are historical; `local-docs/INDEX.md` is the current wayfinder. |
| Understand tenants, modules, platform stack | Part D, then Appendix | Product scope is owned by `system-prd.md`. The former technical spec is archived in `local-docs/archived/technical-docs/` and is history only. |
| Amend the constitution or justify a deviation | Part E | |

## Part A. Principles (checkable rules)

Original section: Core Principles. Each rule line has an id of the form `C-<Roman numeral>-<n>`; `C-<Roman numeral>-0` is the principle statement.

### I. Multi-Tenant Architecture (NON-NEGOTIABLE)

C-I-0 The Hairline platform MUST be architected as four independent, loosely-coupled tenants that
communicate through well-defined APIs:

1. **Patient Platform (Mobile App)**: Patient-facing iOS/Android application
2. **Provider Platform (Web)**: Clinic/hospital management web application
3. **Admin Platform (Web)**: Internal operations and oversight web application
4. **Affiliate Platform (Web Portal)**: External-facing portal for influencers and marketing partners

C-I-0a **Affiliate Platform**: The Affiliate Portal (FR-018) is the fourth application, matching the
four applications of `system-prd.md` (section "System Architecture"). It exposes only
affiliate-scoped self-service (performance, payouts, profile) and enforces its own authentication
and authorization boundary like every other tenant (C-I-1). Affiliates are managed from the Admin
Platform (A-07). Any further application MUST be added to this list by amending this constitution.

**Rationale**: Each tenant serves distinct user groups with different security clearances,
workflows, and data access requirements. Strict separation ensures data privacy, independent
scalability, and parallel development velocity.

**Rules**:

- C-I-1 Each tenant MUST have its own authentication and authorization boundaries
- C-I-2 Cross-tenant data access MUST occur only through authenticated API contracts
- C-I-3 Shared services (e.g., 3D scan processing, payment processing) MUST be independently
  deployable microservices
- C-I-4 No direct database access across tenant boundaries
- C-I-5 Each tenant can be developed, tested, and deployed independently

### II. Medical Data Privacy & Security (NON-NEGOTIABLE)

C-II-0 All patient medical data MUST be treated as Protected Health Information (PHI) and handled
with healthcare-grade security measures.

**Rules**:

- C-II-1 Patient personal identifiable information (PII) MUST be encrypted at rest and in transit
- C-II-2 Provider platforms MUST NOT display patient full names or contact details until booking
  confirmation (the first successful payment); admins are exempt and see the full patient identity
- C-II-3 All patient-provider communications MUST be logged and monitored for compliance
- C-II-4 Every record type, including medical records, MUST be retained for one period of 10 years;
  no record type has a shorter period (`system-prd.md`, "One 10-year retention period")
- C-II-5 Data deletion requests MUST result in archival, not permanent deletion
- C-II-6 All data access MUST be auditable with tamper-proof audit trails
- C-II-7 Role-Based Access Control (RBAC) MUST be enforced across all platforms
- C-II-8 Multi-Factor Authentication (MFA) is a **future feature**: planned for Admin and Provider
  platforms, not enforced at launch, and WILL be enforced platform-wide once the shared MFA stack
  (FR-026 / FR-031) is delivered. Until then, Admin and Provider platforms MUST implement strong password
  policies, throttling, and re-authentication flows, and any FR that references MFA MUST
  clearly mark it as a future (non-MVP) requirement.
- C-II-9 Payment card data MUST never be stored; use PCI-compliant payment processors (Stripe)

**Compliance Standards**:

- C-II-10 GDPR (General Data Protection Regulation) for EU patients
- C-II-11 HIPAA-equivalent standards for medical data handling
- C-II-12 PCI-DSS for payment processing
- C-II-13 Data residency requirements based on patient location

### III. API-First Design

C-III-0 All platform features MUST be accessible through well-documented, versioned REST APIs before
any UI implementation.

**Rules**:

- C-III-1 Backend API development MUST precede frontend development
- C-III-2 All APIs MUST be documented using OpenAPI/Swagger specification
- C-III-3 API contracts MUST be versioned (semantic versioning: MAJOR.MINOR.PATCH)
- C-III-4 Breaking changes require MAJOR version increment and deprecation period (minimum 3 months)
- C-III-5 All endpoints MUST return consistent error response formats
- C-III-6 All endpoints MUST implement proper HTTP status codes
- C-III-7 API responses MUST support both JSON format (machine-readable) and include clear error
  messages (human-readable)
- C-III-8 Rate limiting MUST be implemented on all public-facing APIs

### IV. User Experience & Accessibility

C-IV-0 User interfaces MUST prioritize intuitive workflows, accessibility, and mobile-first design.

**Rules for Patient Mobile App**:

- C-IV-1 MUST support iOS 14+ and Android 10+
- C-IV-2 MUST function offline for core features (view bookings, aftercare instructions)
- C-IV-3 MUST support multiple languages (internationalization/i18n)
- C-IV-4 Loading states MUST not exceed 3 seconds for 95th percentile
- C-IV-5 MUST follow native platform design guidelines (iOS Human Interface Guidelines, Material Design)
- C-IV-6 MUST support device accessibility features (VoiceOver, TalkBack, dynamic text sizing)

**Rules for Web Platforms (Provider & Admin)**:

- C-IV-7 MUST be responsive (mobile, tablet, desktop viewports)
- C-IV-8 MUST support modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
- C-IV-9 MUST achieve WCAG 2.1 Level AA accessibility compliance
- C-IV-10 Critical user flows MUST be completable within 3 clicks/taps
- C-IV-11 MUST provide clear feedback for all user actions (success, error, loading)

**Rules for 3D Scanning Features**:

- C-IV-12 MUST provide clear visual instructions for scan capture
- C-IV-13 MUST validate scan quality before submission
- C-IV-14 MUST support interactive 3D model viewing (rotate, zoom)
- C-IV-15 MUST work with standard smartphone cameras (no special hardware required)

### V. Testing Discipline (NON-NEGOTIABLE)

C-V-0 Comprehensive testing MUST be performed at multiple levels before production deployment.

**Test Hierarchy** (all mandatory unless feature specification explicitly excludes):

1. **Unit Tests**: Individual function/method validation
2. **Integration Tests**: Multi-component interaction validation
3. **Contract Tests**: API endpoint contract validation (request/response schemas)
4. **End-to-End Tests**: Complete user journey validation
5. **Security Tests**: Penetration testing and vulnerability scanning
6. **Performance Tests**: Load testing and stress testing for critical paths

**Rules**:

- C-V-1 Critical user flows (booking, payment, quote submission) MUST have end-to-end test coverage
- C-V-2 All API endpoints MUST have contract tests validating request/response schemas
- C-V-3 Payment flows MUST be tested in sandbox environments before production
- C-V-4 3D scan processing MUST have integration tests with sample scan data
- C-V-5 Regression testing MUST be performed before each production deployment
- C-V-6 Test data MUST NOT contain real patient information

**Test-First Development** (for critical features):

- C-V-7 Security-critical features MUST follow TDD: write tests → tests fail → implement → tests pass
- C-V-8 Payment processing MUST follow TDD
- C-V-9 Authentication/authorization MUST follow TDD

### VI. Data Integrity & Audit Trail

C-VI-0 All system state changes MUST be auditable and recoverable.

**Rules**:

- C-VI-1 All database mutations MUST be logged with timestamp, user, and action
- C-VI-2 Financial transactions (quotes, bookings, payments) MUST be immutable once confirmed
- C-VI-3 State transitions (inquiry → quoted → scheduled → confirmed → in-progress → complete)
  MUST be auditable
- C-VI-4 "Delete" operations on medical/booking data MUST be soft-deletes (archive) not hard-deletes
- C-VI-5 System MUST support point-in-time recovery for critical data (bookings, payments)
- C-VI-6 All provider-patient communication MUST be logged and retained
- C-VI-7 Admin actions that modify provider/patient data MUST be logged with reason/justification

**Version Control**:

- C-VI-8 Treatment packages MUST be versioned; modifications create new versions
- C-VI-9 Aftercare milestone templates MUST be versioned
- C-VI-10 Price changes MUST preserve historical pricing for existing bookings

**Deletion**:

- C-VI-11 Every delete MUST be a soft delete (the record is archived); hard deletion is prohibited for
  every record type (`system-prd.md`, "Soft deletes only")

### VII. Modularity & Independent Deployment

C-VII-0 The system MUST be architected to allow independent module development and deployment.

Module names and scope notes follow the module lines of `system-prd.md`. Head scan media: V1 is a standardized photo set and V2 is true 3D (`system-prd.md`, FR-002 release scope note); wherever this document says "3D scan", read it as head scan media in that sense.

**Module Breakdown**:

**Patient Platform Modules**:

- **P-01**: Auth & Profile Management
- **P-02**: Quote Request & Management
- **P-03**: Booking & Payment
- **P-04**: Travel & Logistics (flights, hotels, transport)
- **P-05**: Aftercare & Progress Monitoring
- **P-06**: Communication (chat with providers, aftercare team)
- **P-07**: 3D Scan Capture & Viewing *(head scan media: V1 photo set; V2 true 3D)*
- **P-08**: Help Center & Support Access

**Provider Platform Modules**:

- **PR-01**: Auth & Team Management
- **PR-02**: Inquiry & Quote Management (includes appointment management, Part D Tenant 2 item 4)
- **PR-03**: Treatment Execution & Documentation
- **PR-04**: Aftercare Participation (optional)
- **PR-05**: Financial Management & Reporting
- **PR-06**: Profile & Settings Management
- **PR-07**: Communication & Messaging

**Admin Platform Modules**:

- **A-01**: Patient Management & Oversight
- **A-02**: Provider Management & Onboarding
- **A-03**: Aftercare Team Management
- **A-04**: Travel Management (API integrations)
- **A-05**: Billing & Financial Reconciliation (patient & provider)
- **A-06**: Discount & Promotion Management
- **A-07**: Affiliate Program Management
- **A-08**: Analytics & Reporting
- **A-09**: System Settings & Configuration
- **A-10**: Communication Monitoring & Support

**Shared Services** (independently deployable):

- **S-01**: 3D Scan Processing Service *(V1 photo set; V2 true 3D)*
- **S-02**: Payment Processing Service (Stripe integration)
- **S-03**: Notification Service (email, SMS, push notifications)
- **S-04**: Travel API Gateway (flights, hotels) *(MVP: travel record storage and itinerary coordination; Phase 2: flight and hotel API integrations)*
- **S-05**: Media Storage Service (images, head scan photo sets (V1), 3D scans (V2), documents)
- **S-06**: Audit Log Service (centralized, immutable audit trail)

**Traceability**: Each Functional Requirement in `local-docs/project-requirements/system-prd.md` includes its corresponding module code(s) for full traceability.

**Rules**:

- C-VII-1 Modules MUST communicate through defined interfaces (APIs, message queues)
- C-VII-2 Module dependencies MUST be explicitly documented in architecture diagrams
- C-VII-3 Shared services MUST have their own repositories and deployment pipelines
- C-VII-4 Modules MUST be deployable without requiring full system redeployment

### VIII. Performance & Scalability

C-VIII-0 The system MUST be designed to handle growth in users, providers, and data volume.

**Performance Targets**:

- C-VIII-1 API response time: p95 < 500ms, p99 < 1000ms (excluding external API calls)
- C-VIII-2 Patient mobile app: Core screens load in < 3 seconds on 4G connection (same threshold as C-IV-4 and `system-prd.md` NFR-001)
- C-VIII-3 3D scan upload: Support files up to 50MB with progress indication
- C-VIII-4 Database queries: No N+1 queries; use eager loading and indexing
- C-VIII-5 Search operations: Patient/provider search results in < 300ms

**Scalability Targets**:

- C-VIII-6 Support 10,000+ concurrent patient users
- C-VIII-7 Support 1,000+ active provider clinics
- C-VIII-8 Handle 100+ simultaneous 3D scan uploads
- C-VIII-9 Process 500+ payment transactions per hour during peak times

**Rules**:

- C-VIII-10 Database queries MUST use indexes on frequently queried columns
- C-VIII-11 Large file uploads (3D scans, documents) MUST use chunked upload with resume capability
- C-VIII-12 Real-time features (chat, notifications) MUST use WebSocket or SSE, not polling
- C-VIII-13 Static assets (images, documents) MUST be served via CDN
- C-VIII-14 Caching MUST be implemented for frequently accessed, rarely changing data
- C-VIII-15 Background jobs (email sending, 3D scan processing) MUST use job queues (Redis, SQS)

### IX. Internationalization & Localization

C-IX-0 The platform MUST support multiple countries, languages, and currencies.

**Rules**:

- C-IX-1 All user-facing text MUST be externalized (i18n resource files)
- C-IX-2 Initial language support: English (en-US, en-GB), Turkish (tr-TR)
- C-IX-3 Currency handling MUST support multi-currency bookings:
  - Patient pays in their local currency
  - Provider receives in their local currency
  - Admin platform tracks all currencies with exchange rates
- C-IX-4 Currency conversion rates MUST be fetched from reliable APIs (xe.com) with configurable
  markup percentage
- C-IX-5 Date/time MUST be displayed in user's local timezone
- C-IX-6 Number formatting (decimals, thousand separators) MUST follow locale conventions
- C-IX-7 Country-specific provider listings (UK patients see Turkey, UK, Poland first)

### X. Versioning & Change Management

C-X-0 All system components MUST follow semantic versioning and maintain backward compatibility.

**Versioning Format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (API contract changes, database schema breaking changes)
- **MINOR**: New features, non-breaking additions
- **PATCH**: Bug fixes, security patches

**Rules**:

- C-X-1 API endpoints MUST support at least 2 concurrent major versions during deprecation period
- C-X-2 Mobile app MUST gracefully handle API version mismatches
- C-X-3 Database migrations MUST be backward-compatible (blue-green deployment support)
- C-X-4 Breaking changes MUST be announced 3 months in advance
- C-X-5 Deprecated features MUST be documented in CHANGELOG.md
- C-X-6 Each production release MUST be tagged in version control with release notes

## Part B. Security and compliance rules

Original section: Security & Compliance Requirements. Each rule line has an id of the form `C-SEC-<n>`.

### Data Protection & Privacy

**Encryption**:

- C-SEC-1 All patient PII and medical data MUST be encrypted at rest (AES-256)
- C-SEC-2 All data in transit MUST use TLS 1.3 (HTTPS, WSS)
- C-SEC-3 Database backups MUST be encrypted
- C-SEC-4 3D scan files MUST be encrypted in storage

**Data Access Control**:

- C-SEC-5 Database credentials MUST be stored in secure vaults (AWS Secrets Manager, HashiCorp Vault)
- C-SEC-6 API keys and secrets MUST never be committed to version control
- C-SEC-7 Environment-specific configurations MUST use environment variables
- C-SEC-8 Admin actions that access patient data MUST be logged with justification

**Patient Privacy Rules**:

- C-SEC-9 Providers MUST NOT see patient full names until booking confirmation (the first successful payment); admins are exempt
- C-SEC-10 Providers MUST see only the anonymized patient ID, shown as "Mark P." followed by the ID,
  until booking confirmation (the first successful payment); this does not apply to admins
- C-SEC-11 Patient contact details (phone number and email address) MUST be revealed only at booking
  confirmation (the first successful payment)
- C-SEC-12 Patient medical history MUST be visible to providers only for active inquiries/bookings
- C-SEC-13 Patient 3D scans MUST be watermarked with patient ID (prevent unauthorized distribution)

**Data Retention & Deletion**:

- C-SEC-14 Medical records MUST be retained for 10 years, the same single period as every other record type (compliance requirement; see C-II-4)
- C-SEC-15 Patient data deletion requests MUST result in anonymization + archival, not hard deletion
- C-SEC-16 Archived data MUST NOT be reachable through normal application interfaces, and MUST remain
  retrievable for compliance audits
- C-SEC-17 Audit trails MUST be immutable and retained for 10 years

### Authentication & Authorization

**Authentication Requirements**:

- C-SEC-18 Passwords MUST be hashed using bcrypt (minimum cost factor: 12)
- C-SEC-19 Password minimum requirements: 12 characters, with at least 1 uppercase, 1 lowercase, 1 number, and 1 special character from !@#$%^&(),.?":{}|<> (not configurable in admin)
- C-SEC-20 Password changes MUST NOT reuse any of the last 5 passwords (password history enforcement)
- C-SEC-21 Account lockout is an admin setting (maximum login attempts and lockout duration); the default
  is 5 failed login attempts and a 15-minute lockout
- C-SEC-22 Session timeout: 30 minutes of inactivity (admin/provider), 24 hours (patient mobile app)
- C-SEC-23 Multi-Factor Authentication (MFA) is a future feature, planned and not enforced at launch;
  the interim controls are in C-II-8. When delivered, it is planned for:
  - All Admin Platform users
  - Provider admin accounts
  - Optional for provider staff accounts

**Authorization Requirements**:

- C-SEC-24 Role-Based Access Control (RBAC) MUST be implemented
- C-SEC-25 Permissions MUST be granular (read, write, delete per resource type)
- C-SEC-26 Principle of least privilege: Users have minimum permissions needed for their role
- C-SEC-27 API endpoints MUST verify user permissions before data access
- C-SEC-28 Cross-tenant data access MUST be explicitly authorized (admin accessing patient data)

**Session Management**:

- C-SEC-29 Tokens MUST be signed and tamper-proof (JWT with RS256 or HS256)
- C-SEC-30 Refresh tokens MUST be rotated on each use
- C-SEC-31 Tokens MUST include expiration time (short-lived: 15 minutes for access tokens)
- C-SEC-32 Revoked tokens MUST be blacklisted (Redis cache for revocation list)

### Payment Security

**PCI-DSS Compliance**:

- C-SEC-33 Payment card data MUST NEVER be stored in Hairline databases
- C-SEC-34 All payment processing MUST use Stripe or equivalent PCI-compliant processor
- C-SEC-35 Stripe publishable keys MUST be used on client-side (no secret keys in frontend code)
- C-SEC-36 Webhook signatures MUST be verified to prevent spoofing
- C-SEC-37 Payment intents MUST be idempotent (prevent double-charging)

**Financial Transaction Security**:

- C-SEC-38 All payment transactions MUST be logged with transaction ID, amount, currency, timestamp
- C-SEC-39 Failed payments MUST trigger retry mechanisms with exponential backoff
- C-SEC-40 Refunds MUST require documented justification and full audit trail before execution
- C-SEC-41 Currency conversion rates MUST be locked at time of booking (no rate fluctuation after booking)
- C-SEC-42 Provider payout calculations MUST be auditable (itemized breakdown of commissions)

### Vulnerability Management

**Security Testing Requirements**:

- C-SEC-43 Penetration testing MUST be performed quarterly by third-party security firm
- C-SEC-44 Dependency vulnerability scanning MUST run on every build (npm audit, Snyk, Dependabot)
- C-SEC-45 Static Application Security Testing (SAST) MUST run on every pull request
- C-SEC-46 Dynamic Application Security Testing (DAST) MUST run on staging environment weekly
- C-SEC-47 Security patches MUST be applied within 48 hours for critical vulnerabilities

**Secure Development Practices**:

- C-SEC-48 Input validation MUST be performed on all user inputs (XSS prevention)
- C-SEC-49 SQL injection MUST be prevented using parameterized queries or ORM
- C-SEC-50 CSRF tokens MUST be used for all state-changing requests
- C-SEC-51 CORS MUST be configured with explicit origin whitelisting (no wildcard in production)
- C-SEC-52 File uploads MUST be validated (file type, size, virus scanning)
- C-SEC-53 Rate limiting MUST prevent brute-force attacks

## Part C. PRD standards and documentation placement

Original sections: Governance, Documentation Organization and PRD Standards & Requirements. Ids are `C-DOC-<n>` for documentation placement and `C-PRD-<n>` for PRD standards.

The PRD structure below is the compressed structure of `local-docs/project-requirements/graph/checklists/prd-structure.md` (v1.0) and `local-docs/INDEX.md` section C.1 (owner ruling 2026-11-25). Sections dropped there are no longer required; the ids of dropped sections are retired in place and not reused.

### Documentation Organization

C-DOC-1 **IMPORTANT**: All project documentation generated based on this Constitution MUST be placed in:

```sh
local-docs/project-requirements/
```

### PRD Standards & Requirements (NON-NEGOTIABLE)

C-PRD-1 All Product Requirements Documents (PRDs) MUST follow the compressed structure and quality standards below. New PRDs start from the canonical templates in `local-docs/project-requirements/templates/`.

**Mandatory PRD Structure**:

1. C-PRD-2 **Header Information** (REQUIRED):
   - Module codes and names (e.g., "P-05: Aftercare & Progress Monitoring | PR-04: Aftercare Participation")
   - Feature branch name (format: `fr[###]-[module-name]`)
   - Creation date and status
   - Source reference (e.g., "FR-011 from system-prd.md")

2. C-PRD-3 **Executive Summary** (REQUIRED):
   - Clear module purpose and scope
   - Multi-tenant architecture implications
   - Entry points and activation triggers

3. C-PRD-4 **Module Scope** (REQUIRED):
   - Multi-tenant architecture breakdown
   - Communication structure (explicitly state what's in/out of scope)
   - Entry points and activation methods

4. C-PRD-5 **Business Workflows** (REQUIRED):
   - **Main Flow**: Step-by-step primary workflow
   - **Alternative Flows**: All possible variations (A1, A2, B1, B2, etc.)
   - **Actors**: Clear identification of all involved parties
   - **Triggers**: What initiates each workflow
   - **Outcomes**: Expected results and status changes

5. C-PRD-6 **Screen Specifications** (REQUIRED):
   - **Purpose**: Clear screen objective
   - **Data Fields**: Complete field list with types and descriptions; every field-table row carries its graph field id
   - **Business Rules**: Specific rules governing screen behavior
   - **Notes**: Implementation guidance and constraints

6. C-PRD-7 **Business Rules** (REQUIRED):
   - General module rules
   - Data and privacy rules
   - Admin editability rules (if applicable)
   - Payment and billing rules (if applicable)
   - Each rule is stated once and cited elsewhere by its REQ id; rules rescued from dropped sections sit here in their original wording

7. C-PRD-8 **RETIRED** (formerly Success Criteria). Success metrics are no longer a PRD section; they stay in the frozen baseline.

8. C-PRD-9 **Dependencies** (REQUIRED): one short list of related FR ids.

9. C-PRD-10 **RETIRED** (formerly Assumptions). Rules stated inside assumptions were moved to Business Rules; the section is no longer part of a PRD.

10. C-PRD-11 **RETIRED** (formerly Implementation Notes). Technical notes are no longer a PRD section; any business rule found there was moved to Business Rules.

11. C-PRD-25 **User Scenarios & Testing** (REQUIRED): user stories, acceptance scenarios, and edge cases. Edge cases stay in the PRD because they are business rules.

12. C-PRD-26 **Functional Requirements Summary** (REQUIRED)

13. C-PRD-27 **Appendix: Change Log** (REQUIRED): restarted with one first entry pointing to the frozen baseline `archived/prd-baseline-2026-11-08/`; earlier history stays in that archive.

14. C-PRD-28 **Appendix: Approvals** (REQUIRED): kept short.

Key Entities is also no longer a PRD section: entities and fields live in the requirements graph. The pre-compression PRDs and all change-request files are kept in `archived/prd-baseline-2026-11-08/`.

**Quality Standards**:

- C-PRD-12 **Completeness**: Every section above MUST be fully populated (no placeholders)
- C-PRD-13 **Consistency**: Terminology and concepts MUST align with system-prd.md
- C-PRD-14 **Traceability**: Every requirement MUST reference source FR and module codes; every field-table row also carries its graph field id (C-PRD-6)
- C-PRD-15 **Verification**: PRD MUST be cross-checked against client transcriptions
- C-PRD-16 **Status Management**: PRD status MUST progress from "Draft" → "Verified & Approved"
- C-PRD-17 **Admin Editability**: MUST explicitly address admin override capabilities where applicable
- C-PRD-18 **Multi-Tenant**: MUST clearly define which tenants/platforms are involved
- C-PRD-19 **Communication Structure**: MUST explicitly state what communication features are in/out of scope

**Verification Process**:

1. C-PRD-20 **Transcription Cross-Check**: PRD MUST be verified against original client requirements
2. C-PRD-21 **Consistency Check**: PRD MUST align with system-prd.md and constitution principles
3. C-PRD-22 **Completeness Review**: All mandatory sections MUST be present and detailed
4. C-PRD-23 **Stakeholder Approval**: PRD MUST be confirmed as OK by project stakeholders
5. C-PRD-24 **Status Update**: PRD status MUST be updated to "✅ Verified & Approved" upon confirmation

**Template Reference**: The canonical templates are in `local-docs/project-requirements/templates/` (change control in the project instructions). `prd-template.md` there still carries the pre-compression section list; until it is updated, the section list in this Part and in `local-docs/INDEX.md` section C.1 governs, and a new PRD omits the retired sections.

### Documentation placement rules

These rules are the "Rules" list that closed the original Governance documentation layout. In the original they sat under the heading "PRD Standards & Requirements (NON-NEGOTIABLE)", and that status still covers them. The layout trees they refer to are kept in Part D under "Documentation layout (historical)".

**Rules**:

- C-DOC-2 **System-Level Documentation**: Core system documents (`system-prd.md`, `constitution.md`) remain at the root of
  `project-requirements/`. (`system-data-schema.md` and `system-technical-spec.md` were archived to
  `local-docs/archived/technical-docs/` on 2026-11-25; `constitution-summary.md` was merged into this file.)
- C-DOC-3 **Update Logs**: All documentation update reports and verification logs MUST be placed in
  `update-logs/` to maintain an audit trail of changes.
- C-DOC-4 **Transcriptions**: Original requirement transcriptions remain in `transcriptions/` as source material.
- C-DOC-5 **System Design** (future): High-level design artifacts (architecture diagrams, ERDs, user flows)
  go in `system-design/` subdirectories. These describe flows and design, not implementation details.
- C-DOC-6 **Functional Requirements Documentation** (future): Each FR gets its own subfolder under `functional-requirements/` containing ALL
  its documentation (PRD, technical specs, API contracts, testing plans, etc.). This keeps related
  documentation together and avoids scattered files.
- C-DOC-7 **API Specifications** (future): Shared/cross-module API specifications go in `api-specs/` (e.g.,
  authentication APIs, payment gateway APIs used by multiple modules).
- C-DOC-8 **Security** (future): All security-related documentation centralized in `security/` for easy auditing.

Create additional subfolders within functional-requirements directories as needed for structure and clarity. This
organization ensures documentation stays together and is easy to manage as the system grows.

Editorial note: `constitution-summary.md`, named in the first rule above, has been merged into this document and no longer holds content.

## Part D. Reference and development standards

Description of the four tenants, development standards and the original documentation layout. This part is reference: product scope is owned by `system-prd.md` (Functional Requirements and Platform-Wide Rules). The former technical spec and data schema named in this part are archived in `local-docs/archived/technical-docs/`. Lines in Development Standards that carry MUST wording or numeric thresholds are labelled `C-DEV-<n>` and are checked in code review.

The per-tenant module lists are kept in full because no single section of `system-prd.md` reproduces them: that document is organised by Functional Requirement, not by these per-tenant module lists with priority labels. Replacing them with pointers is a possible later pass (see `constitution-open-items.md`, remaining points). Head scan media follows the scope note in Principle VII (V1 photo set; V2 true 3D).

### System Architecture & Tenants


#### Tenant 1: Patient Platform (Mobile App)

**Target Platform**: iOS 14+ (Swift/SwiftUI), Android 10+ (Kotlin/Jetpack Compose) OR
React Native/Flutter for cross-platform

**Core Modules**:

1. **Authentication & Profile** (P1 - MVP Required)
   - User registration, login, password reset
   - Profile management (personal details, medical history)
   - Multi-language support

2. **Quote Request & Management** (P1 - MVP Required)
   - Destination selection (country-based clinic search)
   - Treatment type selection (hair transplant, beard transplant)
   - Head scan media capture (V1 photo set; V2 true 3D)
   - Medical questionnaire completion
   - Treatment date range selection
   - Quote submission to multiple providers
   - Quote comparison and acceptance

3. **Booking & Payment** (P1 - MVP Required)
   - Treatment package selection
   - Travel package selection (flights, hotels, transport)
   - Discount code application
   - Payment processing (Stripe integration)
   - Split payment plans (installment payments)
   - Booking confirmation and itinerary
   - Travel detail capture + coordination (passport + flight/hotel details, unified itinerary view)

4. **Travel & Logistics** (P2 - Post-MVP)
   - Phase 2: Flight search and booking (in-app via flight API integration)
   - Phase 2: Hotel search and booking (in-app via hotel API integration)
   - Transport tracking (driver details, pickup times)

5. **Treatment Progress** (P1 - MVP Required)
   - Appointment details and countdown
   - Daily itinerary (day 1: consultation, day 2: procedure, etc.)
   - Provider contact information
   - Check-in notifications

6. **Aftercare & Monitoring** (P1 - MVP Required)
   - Aftercare milestone tracking
   - Medication reminders
   - Progress head scan media (before/after comparison)
   - Symptom logging (pain levels, sleep quality)
   - Chat with aftercare team
   - Video consultation scheduling
   - Educational resources

7. **Communication** (P2 - Post-MVP)
   - In-app chat with providers (pre-booking questions)
   - In-app chat with aftercare team (post-procedure support)
   - Notification center

8. **Reviews & Feedback** (P2 - Post-MVP)
   - Leave provider reviews (with before/after photos)
   - View provider ratings and reviews

**Monitoring** (P1 - built with the clinical release; FR-037, FR-038):

- Monitor hair loss (3D scan tracking for non-patients)
- Monitor transplant progress (for patients who booked outside the app)

**Additional Features** (P3 - Future):

- Standalone aftercare service purchase

#### Tenant 2: Provider Platform (Web Application)

**Target Platform**: Responsive web application (React/Vue.js + Laravel API backend)

**Core Modules**:

1. **Authentication & Team Management** (P1 - MVP Required)
   - Provider login
   - Staff invitation and role assignment
   - Permission management (front desk, clinical staff, billing staff)

2. **Inquiry Management** (P1 - MVP Required)
   - View incoming quote requests
   - Review patient head scan media and medical history
   - View patient medical questionnaire (highlight risk factors)
   - Filter inquiries by date, treatment type, location

3. **Quote Submission** (P1 - MVP Required)
   - Treatment selection from predefined catalog
   - Package customization (base treatment + hotel + transport options)
   - Graph count estimation (number of hair follicles)
   - Pricing configuration per date range
   - Clinician assignment
   - Discount application
   - Quote preview and submission
   - Multi-date range quote support (quote for 3 different patient-proposed dates)

4. **Appointment Management** (P1 - MVP Required) *(PR-02)*
   - View quotes sent (pending patient acceptance)
   - View accepted appointments (pending payment)
   - View scheduled appointments (paid, awaiting arrival)
   - View confirmed appointments (patient details available post-payment)
   - Appointment itinerary configuration (day-by-day treatment plan)
   - Hotel/flight/transport detail collection (if provider offers these)

5. **Treatment Execution** (P1 - MVP Required)
   - Check-in patients on arrival
   - Head scan media capture (pre-procedure, post-procedure)
   - Procedure notes and documentation
   - Medication prescription
   - Aftercare plan assignment (from templates)

6. **Aftercare Management** (P1 - MVP; provider participation is optional) *(PR-04)*
   - View assigned aftercare patients (if provider participates in aftercare)
   - Monitor patient progress (milestones, questionnaires, scans)
   - Schedule video consultations
   - Chat with patients
   - Escalate concerns to admin aftercare team

7. **Financial Management** (P1 - MVP Required)
   - View upcoming payments (based on payment schedule: weekly/bi-weekly/monthly)
   - View payment history
   - Invoice generation
   - Earnings analytics (breakdown by procedure type)
   - Commission structure display

8. **Profile & Settings** (P1 - MVP Required)
   - Clinic profile management (name, logo, location, certifications, awards)
   - Staff member profiles (photos, specialties, certifications)
   - Treatment catalog management (enable/disable treatments, base pricing)
   - Package configuration (hotel tiers, transport options, add-ons)
   - Payment schedule preference (weekly, bi-weekly, monthly)
   - Discount creation (provider-specific discounts)
   - Discount approval (accept/reject admin-proposed discounts)
   - Bank account details for payouts
   - Notification preferences

9. **Analytics & Reporting** (P2 - Post-MVP)
   - Quote conversion rates
   - Patient demographics
   - Revenue trends
   - Treatment outcome tracking

10. **Communication & Messaging** (P2 - Enhanced) *(PR-07)*
   - Secure patient ↔ provider in-app messaging (quote clarification, booking coordination, post-procedure questions)
   - Text + media (images/video/PDF), read receipts, real-time notifications
   - Communication history retained and auditable for compliance; admin monitoring and emergency-only intervention per system policy

#### Tenant 3: Admin Platform (Web Application)

**Target Platform**: Responsive web application (React/Vue.js + Laravel API backend)

**Core Modules**:

1. **Patient Management** (P1 - MVP Required)

   - View all patients (with stage filters: inquiry, quoted, scheduled, in-progress, aftercare, complete)
   - Search patients by name, ID, email, location
   - View patient details (full profile, medical history, head scan media)
   - View patient quote history (all quotes received from providers)
   - View patient booking details
   - View patient payment history
   - Manual quote/booking modification (emergency rescheduling)
   - Communication log (all patient-provider messages)
   - Patient support ticketing

2. **Provider Management** (P1 - MVP Required)
   - View all providers (with filters by location, status, specialties)
   - Provider onboarding workflow
   - Provider profile editing
   - Provider verification (licenses, certifications, insurance)
   - Provider staff management
   - Provider treatment catalog management
   - Provider package approval
   - Provider reviews management (import external reviews, moderate user reviews)
   - Provider suspension/activation

3. **Aftercare Management** (P1 - MVP Required) *(A-03)*
   - View all aftercare patients
   - Assign aftercare clinicians
   - Monitor patient progress (milestones, compliance, red flags)
   - Chat with patients
   - Chat with assigned provider clinicians (for patients with provider aftercare)
   - Schedule video consultations
   - Request additional head scan media
   - Generate aftercare reports
   - Aftercare milestone template management
   - Aftercare questionnaire management

4. **Travel Management** (P3 - Future)
   - Flight API integration configuration
   - Hotel API integration configuration
   - Transport service provider management (drivers, vehicles)
   - Transport assignment and tracking
   - Travel package pricing and commission configuration

5. **Financial Management** (P1 - MVP Required)
   - **Patient Billing**:
     - View all patient invoices
     - View payment status (pending, partial, complete)
     - Payment reminders
     - Refund processing
     - Split payment plan management
   - **Provider Billing**:
     - View provider payment schedules
     - Approve/process provider payouts
     - Payment reconciliation
     - Invoice generation
     - Commission tracking
   - **Affiliate Billing**:
     - View affiliate commissions
     - Process affiliate payouts
     - Payment history
   - **Stripe Account Management**:
     - Multiple Stripe account configuration (per region/currency)
     - Currency conversion rate management
   - **Financial Reporting**:
     - Revenue analytics
     - Commission breakdowns
     - Outstanding balance reports

6. **Discount & Promotion Management** (P2 - Post-MVP)
   - Create platform-wide discounts (applies to all providers)
   - Create admin-only discounts (reduces Hairline commission only)
   - Discount code generation
   - Discount approval workflow (providers accept/reject discount participation)
   - Discount usage tracking
   - Automatic discount application rules

7. **Affiliate Program Management** (P2 - Post-MVP)
   - Affiliate registration and onboarding
   - Discount code assignment to affiliates
   - Commission structure configuration (percentage or fixed amount)
   - Affiliate payout schedule (monthly)
   - Affiliate dashboard access provisioning
   - Affiliate performance analytics

8. **Settings & Configuration** (P1 - MVP Required)
   - **General Settings**:
     - Terms & conditions management
     - Privacy policy management
     - Consent form templates
     - Process timing configuration (quote expiry time, payment deadline)

   - **App Settings** (Patient Mobile App):
     - Landing page media (splash screen, logos, videos)
     - Service section images
     - Discovery question options (centrally managed list)
     - Country and country calling code lists (centrally managed)
     - Location presentation rules (which countries to show first per patient region)
     - Starting price per location per currency

   - **Treatment Settings**:
     - Treatment catalog (add/edit treatments with videos, descriptions)
     - Treatment package templates

   - **Aftercare Settings**:
     - Aftercare pricing (per currency)
     - Payment options (fixed or subscription)
     - Milestone creation (duration, questionnaires, scan frequency)
     - Questionnaire creation (question types, frequency)
     - Aftercare resource library

   - **Travel Settings**:
     - API integration settings (flight, hotel APIs)
     - Commission configuration per service per region
     - Enable/disable travel features per country

   - **Notification Settings**:
     - Email template editor (signup, booking confirmation, payment receipt, etc.)
     - Notification trigger configuration (when to send notifications)
     - Notification preferences per user type

   - **Security Settings**:
     - Password policy (min length and character requirements) is FIXED in codebase (not editable in Admin)
     - Authentication throttling (max login attempts, lockout duration)
     - OTP configuration: length is FIXED at 6 in codebase; expiry time and resend cooldown configurable via FR-026 App Settings & Security admin UI within defined security bounds (audited and versioned)

   - **User & Permission Management**:
     - Admin staff management
     - Role-based access control (aftercare staff, billing staff, support staff, super admin)
     - Permission matrix configuration

9. **Analytics & Reporting** (P2 - Post-MVP)
   - Patient conversion funnel (inquiry → quote → booking → complete)
   - Provider performance metrics
   - Treatment outcome analysis
   - Financial dashboards (revenue, outstanding, commission)
   - Geographic analytics (patient origin, provider location, revenue by region)
   - Response time metrics (provider quote response time)

10. **Communication Monitoring** (P1 - MVP Required)
    - View all patient-provider messages
    - Keyword flagging (detect attempts to transact outside platform)
    - Support ticket management (patient inquiries, issues)
    - Provider support ticketing

#### Tenant 4: Affiliate Platform (Web Portal)

**Target Platform**: Web portal for influencers and marketing partners. Affiliates are onboarded and
managed from the Admin Platform (Tenant 3, item 7). Scope and screens are owned by FR-018 (P2 - Enhanced).

**Core Modules**:

1. **Affiliate Portal** (P2 - Enhanced) *(A-07)*
   - Account activation by one-time link, then login with the affiliate's own authentication boundary
   - Performance dashboard (referral count, revenue, commissions)
   - Assigned promo codes, commission structure and payout schedule
   - Payout history and profile
   - Affiliate-scoped data access only


### Development Standards


#### Code Quality

**Linting & Formatting**:

- Backend (Laravel/PHP): PHP CS Fixer, PHPStan (level 8)
- Frontend (React/Vue): ESLint (Airbnb style guide), Prettier
- Mobile (React Native/Flutter): ESLint or dart analyze

**Code Review Requirements**:

- C-DEV-1 All code MUST be peer-reviewed before merge (minimum 1 approval)
- C-DEV-2 Security-sensitive code MUST be reviewed by senior developer
- C-DEV-3 Pull requests MUST be linked to task/issue tracking (Plane, Jira, GitHub Issues)
- C-DEV-4 Pull requests MUST have descriptive titles and descriptions
- C-DEV-5 Pull requests MUST pass all CI checks before merge

**Documentation Requirements**:

- C-DEV-6 All API endpoints MUST be documented in OpenAPI/Swagger
- C-DEV-7 Complex business logic MUST have inline code comments explaining "why" not "what"
- C-DEV-8 Public functions/classes MUST have docblock comments
- C-DEV-9 Database schema MUST have entity-relationship diagrams (ERD)
- C-DEV-10 Architecture decisions MUST be documented in ADR (Architecture Decision Records)

#### Version Control

**Branching Strategy**:

- `main`: Production-ready code (protected branch)
- `develop`: Integration branch for features (protected branch)
- `fr[###]-[module-name]`: Functional requirement feature branches (from develop)
- `hotfix/[###-issue-name]`: Emergency production fixes (from main)
- `release/[version]`: Release preparation (from develop)

**Commit Standards**:

- C-DEV-11 Commit messages MUST follow Conventional Commits format:
  - `feat:` new feature
  - `fix:` bug fix
  - `docs:` documentation changes
  - `refactor:` code refactoring
  - `test:` test additions/modifications
  - `chore:` maintenance tasks
- C-DEV-12 Commits MUST reference issue/task number (e.g., `feat(quotes): add multi-date quote support (#123)`)

**Release Process**:

1. Feature branch merged to develop
2. QA testing on develop branch (staging environment)
3. Create release branch from develop
4. Version bump and changelog generation
5. Final testing on release branch
6. Merge release branch to main
7. Tag release in version control
8. Deploy to production
9. Merge main back to develop

#### Continuous Integration / Continuous Deployment (CI/CD)

**CI Pipeline** (runs on every push to feature/develop/main):

1. Install dependencies
2. Run linters and formatters
3. Run unit tests
4. Run integration tests
5. Run contract tests
6. Run security scans (SAST, dependency vulnerabilities)
7. Build application artifacts
8. Generate code coverage report (minimum 70% for critical paths)

**CD Pipeline** (deployment):

- C-DEV-13 **Develop branch** → Auto-deploy to **Staging environment**
- C-DEV-14 **Main branch** → Manual approval → Deploy to **Production environment**
- C-DEV-15 Blue-green deployment strategy (zero-downtime deployments)
- C-DEV-16 Automated database migrations with rollback capability
- C-DEV-17 Health checks before marking deployment as successful

#### Testing Standards

**Test Coverage Requirements**:

- C-DEV-18 Critical user flows (booking, payment): 90%+ coverage
- C-DEV-19 API endpoints: 80%+ coverage
- C-DEV-20 Business logic: 75%+ coverage
- Utility functions: 70%+ coverage

**Test Data Management**:

- C-DEV-21 Test databases MUST be isolated from production
- C-DEV-22 Test data MUST be anonymized (no real patient data)
- C-DEV-23 Seed data scripts for local development and staging environments
- C-DEV-24 Factories for generating test entities (Laravel factories, Faker library)

**Performance Testing**:

- C-DEV-25 Load testing MUST simulate peak traffic (3x normal load)
- C-DEV-26 Stress testing MUST identify breaking points
- C-DEV-27 Database query performance MUST be monitored (no queries > 1 second)

### Documentation layout (historical)

The two trees below are kept word for word from the original. They are not maintained: file names, table counts and the future structure have moved on. The current map of `local-docs` is `local-docs/INDEX.md`. The line naming `constitution-summary.md` is stale because that file was merged into this document.

#### Current Structure (System-Level Documentation)

```sh
local-docs/project-requirements/
├── constitution-summary.md      # Core principles & governance
├── system-data-schema.md        # Database design (91 tables)
├── system-prd.md                # Product requirements (all platforms)
├── system-technical-spec.md     # Technical architecture
├── transcriptions/              # Original requirement transcriptions
│   ├── Hairline-AdminPlatform-Part1.txt
│   ├── Hairline-AdminPlatformPart2.txt
│   ├── Hairline-ProviderPlatformPart1.txt
│   ├── Hairline-ProviderPlatformPart2.txt
│   ├── HairlineApp-Part1.txt
│   ├── HairlineApp-Part2.txt
│   └── HairlineOverview.txt
└── update-logs/                 # Documentation update & verification reports
    ├── README.md
    ├── DOCUMENTATION_UPDATES_2025-10-23.md
    └── VERIFICATION_REPORT_2025-10-23.md
```

#### Future Structure (Module-Level Documentation)

When breaking down the system into independent modules, the structure will evolve to:

```sh
local-docs/project-requirements/
├── [system-level docs as above]
├── system-design/              # High-level system design (before implementation)
│   ├── architecture/           # System architecture diagrams, deployment diagrams
│   ├── data-models/            # Database schemas, ERDs, entity definitions
│   └── user-flows/             # User journey maps, wireframes, UX specifications
├── api-specs/                  # Shared API specifications (OpenAPI/Swagger)
├── security/                   # Security assessments, compliance docs, audit reports
└── functional-requirements/    # Functional Requirements documentation (all docs per FR)
    ├── fr001-patient-auth/
    │   ├── prd.md              # Product Requirements Document
    │   ├── technical-spec.md   # Detailed technical specifications
    │   ├── api-contracts.md    # FR-specific API contracts
    │   └── testing-plan.md     # Test cases and coverage plans
    ├── fr002-medical-history/
    ├── fr003-inquiry-submission/
    └── [fr-code-name]/         # Repeat structure for each FR
```

## Part E. Governance

Original section: Governance (Constitution Authority, Amendment Process, Compliance Verification, Complexity Justification, Continuous Improvement). Ids are `C-GOV-<n>`.

### Constitution Authority

C-GOV-1 This Constitution supersedes all other development practices, coding standards, and architectural
decisions. Any deviation from the principles defined herein MUST be explicitly justified,
documented, and approved by the project technical lead or steering committee.

### Amendment Process

1. C-GOV-2 **Proposal**: Any team member may propose an amendment by creating a document outlining:
   - The current principle or section to be amended
   - The proposed change
   - Rationale for the change
   - Impact analysis (affected systems, migration effort, risk assessment)
   - Alternatives considered and rejected

2. C-GOV-3 **Review**: The proposal is reviewed by the technical steering committee (TSC) consisting of:
   - Project Technical Lead
   - Backend Lead Developer
   - Frontend Lead Developer
   - Security Lead
   - Product Owner

3. C-GOV-4 **Approval**: Amendments require majority approval from TSC. Breaking changes (e.g.,
   removing a non-negotiable principle) require unanimous approval.

4. C-GOV-5 **Migration Plan**: Approved amendments MUST include:
   - Timeline for implementation
   - Migration tasks for affected code/systems
   - Communication plan for team members
   - Rollback plan if migration fails

5. C-GOV-6 **Documentation**: Approved amendments are documented with:
   - Version increment (following semantic versioning)
   - Amendment date
   - Rationale summary
   - Update to Sync Impact Report

### Compliance Verification

**Pre-Development Phase** (before starting any feature):

- C-GOV-7 Feature specification MUST reference relevant Constitution principles
- C-GOV-8 Implementation plan MUST include "Constitution Check" section
- C-GOV-9 Identified violations MUST be justified or resolved

**During Development**:

- C-GOV-10 Code reviews MUST verify adherence to Constitution principles
- C-GOV-11 CI pipeline MUST enforce automated checks where possible (linting, test coverage, security scans)

**Post-Development**:

- C-GOV-12 Retrospective reviews to identify recurring Constitution violations
- C-GOV-13 Quarterly Constitution health checks to assess adherence across codebase
- C-GOV-14 Annual Constitution review to identify outdated principles or needed additions

### Complexity Justification

C-GOV-15 When a feature requires deviation from Constitution principles (especially "NON-NEGOTIABLE" ones),
the following justification process MUST be followed:

1. C-GOV-16 Document the violation in the feature's `plan.md` file under "Complexity Tracking"
2. C-GOV-17 Explain why the violation is necessary (business requirement, technical constraint)
3. C-GOV-18 Describe simpler alternatives that were considered and why they were rejected
4. C-GOV-19 Get explicit approval from TSC before implementation
5. C-GOV-20 Create a technical debt ticket to resolve the violation in a future sprint (if feasible)

### Continuous Improvement

The Constitution is a living document. The team is encouraged to propose improvements based on:

- Lessons learned from development sprints
- New best practices in the industry (SDLC, security, UX)
- Feedback from users (patients, providers, admin staff)
- Performance metrics and system monitoring data
- Security audit findings

**Review Cadence**:

- **Monthly**: Quick review of new principles proposed by team members
- **Quarterly**: Comprehensive review of Constitution adherence and effectiveness
- **Annually**: Major Constitution revision to incorporate industry changes and platform evolution

## Appendix: content carried from the old executive summary

Carried from the former `constitution-summary.md` (version 1.0.0) and aligned with the system PRD on 2026-11-25. This appendix is descriptive, not rule text. Module codes are owned by the module line of each Functional Requirement in `system-prd.md`; where this list and an FR differ, the FR and the system PRD govern.

### Module Breakdown

**Traceability**: Each Functional Requirement in `system-prd.md` includes its corresponding module code(s) for full traceability.

#### Patient Platform Modules (8 core)

- **P-01**: Auth & Profile Management (P1)
- **P-02**: Quote Request & Management (P1)
- **P-03**: Booking & Payment (P1)
- **P-04**: Travel & Logistics (P2)
- **P-05**: Aftercare & Progress Monitoring (P1)
- **P-06**: Communication (P2)
- **P-07**: 3D Scan Capture & Viewing *(V1 photo set; V2 true 3D)* (P1)
- **P-08**: Help Center & Support Access (P1)

#### Provider Platform Modules (7 core)

- **PR-01**: Auth & Team Management (P1)
- **PR-02**: Inquiry & Quote Management (P1) - Includes Appointment Management & Pre-scheduling
- **PR-03**: Treatment Execution & Documentation (P1)
- **PR-04**: Aftercare Participation (P1 - provider participation optional)
- **PR-05**: Financial Management & Reporting (P1)
- **PR-06**: Profile & Settings Management (P1)
- **PR-07**: Communication & Messaging (P2)

#### Admin Platform Modules (10 core)

- **A-01**: Patient Management & Oversight (P1)
- **A-02**: Provider Management & Onboarding (P1)
- **A-03**: Aftercare Team Management (P1)
- **A-04**: Travel Management (API integrations) (P3)
- **A-05**: Billing & Financial Reconciliation (P1)
- **A-06**: Discount & Promotion Management (P2)
- **A-07**: Affiliate Program Management (P2)
- **A-08**: Analytics & Reporting (P2)
- **A-09**: System Settings & Configuration (P1)
- **A-10**: Communication Monitoring & Support (P1)

#### Shared Services (independently deployable)

- **S-01**: 3D Scan Processing Service *(V1 photo set; V2 true 3D)* (P1)
- **S-02**: Payment Processing Service (Stripe integration) (P1)
- **S-03**: Notification Service (email, SMS, push notifications) (P1)
- **S-04**: Travel API Gateway (MVP travel record storage + itinerary coordination; Phase 2 flight/hotel API integrations) (P2)
- **S-05**: Media Storage Service (images, head scan photo sets (V1), 3D scans (V2), documents) (P1)
- **S-06**: Audit Log Service (centralized, immutable audit trail) (P1)

### Implementation Priority

Carried from the old summary and not re-verified, except that aftercare is placed in Phase 1 (owner ruling 2026-11-25). The priority of each FR is owned by the `Priority` line of its section in `system-prd.md`.

#### Phase 1: MVP (P1 modules)

- Patient: Auth, Quote Request, Booking/Payment (includes travel detail capture + itinerary coordination), Treatment Progress, Aftercare & Progress Monitoring
- Provider: Auth, Inquiry, Quote Submission, Appointments, Treatment Execution, Financial, Aftercare Participation (optional for a clinic)
- Admin: Patient Management, Provider Management, Financial Management, Settings, Communication Monitoring, Aftercare Team Management

#### Phase 2: Enhanced Features (P2 modules)

- Travel & Logistics (Phase 2: in-app flight/hotel booking via APIs; transport tracking)
- Discounts & Promotions
- Affiliate Program
- Analytics & Reporting

#### Phase 3: Future Expansion (P3 modules)

- Travel Management (admin configuration surfaces for travel APIs)
- Advanced monitoring features
- Outcome tracking and analytics

### Statements found only in the old summary

These statements are kept here, word for word, as history. They are not rules; the rules are in Parts A and B. The hard-deletion prohibition is now `C-VI-11`, archived-data retrieval for audits is stated in `C-SEC-16`, and the retention period is `C-II-4`; the "7-year minimum" below is superseded by the single 10-year period. The other summary-only statements (the NON-NEGOTIABLE heading on Principle VI, numeric targets such as coverage, compliance and sprint cadence, and the table count) are not carried as rules; the original text governs.

- Principle VI was headed "Data Integrity & Audit Trail (NON-NEGOTIABLE)" in the summary; the original heading has no NON-NEGOTIABLE marker.
- **HARD DELETES STRICTLY PROHIBITED**: System MUST NOT allow hard deletion of any medical, financial, or patient data
- Soft-deletes ONLY for all critical entities (7-year minimum retention for healthcare/tax compliance) *(superseded: 10 years, see `C-II-4`)*
- Archived data MUST remain accessible for compliance audits

### Planned Functional Requirements

FR-035 (Patient Help Center and Support Submission) was listed here as planned. It now has its own section in `system-prd.md` and a PRD folder under `functional-requirements/`; use those for its scope and status.

## Change log

- 1.0.0 (2025-10-23): initial ratification (ten principles; System Architecture & Tenants; Security & Compliance Requirements; Development Standards; Governance). The original file carried a Spec Kit sync report (templates plan, PRD and tasks reviewed as compatible); that comment is not kept.
- 1.0.0 restructure (2026-11-25): original constitution and executive summary merged into this file in Parts A to E plus an Appendix. Rule wording unchanged; rule ids added; original headings kept. Replaced by pointers or dropped from the summary: overview, core-principles digest, security and development digests, governance digest, "Key Gaps Addressed", "Next Steps", "Success Metrics", the repeated PRD standards and layout trees, "Planned Functional Requirements" detail and the document-status footer.
- File placement update (2026-11-25): C-DOC-2 and two pointer lines updated after `system-technical-spec.md` and `system-data-schema.md` were archived to `local-docs/archived/technical-docs/` and the `constitution-summary.md` stub was removed. No principle changed.
- 1.1.0 (2026-11-25): rules corrected to agree with `system-prd.md` and the FR PRDs, on owner rulings of 2026-11-25. Corrected rules and reasons:
  - `C-I-0`, `C-I-0a`, Tenant 4 in Part D: the Affiliate Portal is a fourth application (system PRD "System Architecture").
  - Aftercare is P1 and part of the first release: Part D Tenant 1 item 6, Tenant 2 item 6 (`PR-04`, per the system PRD FR-011 module line), Tenant 3 item 3, Appendix module priorities and Implementation Priority (aftercare moved from Phase 2 to Phase 1).
  - `C-II-8`, `C-SEC-23`: MFA is a future feature, not enforced at launch; the interim controls of `C-II-8` are kept.
  - `C-SEC-21`: account lockout is an admin setting with default 5 attempts and 15 minutes.
  - `C-VI-11` (new): every delete is a soft delete; hard deletion is prohibited (system PRD "Soft deletes only").
  - `C-II-4`, `C-SEC-14`, Appendix "7-year" text: one 10-year retention period for every record type including medical records.
  - `C-IV-1`, Part D Tenant 1 target platform: minimum Android version is Android 10+ (system PRD NFR-006).
  - `C-VIII-2`: mobile load time under 3 seconds, aligned with `C-IV-4` and system PRD NFR-001.
  - `C-II-2`, `C-SEC-9`, `C-SEC-10`, `C-SEC-11`: patient identity before booking confirmation (the first successful payment) uses the system PRD wording; admins exempt.
  - `C-SEC-16`: states both halves (not reachable through normal application interfaces; retrievable for compliance audits).
  - Principle VII and Part D tenant lists: module scope notes (head scan media V1 photo set, V2 true 3D; S-04, S-05, PR-02).
  - Part C: PRD structure replaced by the compressed structure; `C-PRD-1`, `C-PRD-6`, `C-PRD-7`, `C-PRD-9`, `C-PRD-12`, `C-PRD-14` reworded; `C-PRD-8`, `C-PRD-10`, `C-PRD-11` retired in place; `C-PRD-25` to `C-PRD-28` added; the FR-011 template statement replaced by the canonical templates directory.
- 1.1.1 (2026-11-25): Part D Tenant 1 feature list: "Monitor hair loss" and "Monitor transplant progress" moved from Additional Features (P3) to their own P1 line, built with the clinical release, on the owner decision of 2026-11-25 (system PRD FR-037 and FR-038).

**Version**: 1.1.1 | **Ratified**: 2025-10-23 | **Last Amended**: 2026-11-25
