# Hairline Platform - Product Requirements Document (PRD)

**Version**: 1.2.0  
**Document Type**: System-Level PRD  
**Created**: 2025-10-23  
**Status**: Active  
**Last Updated**: 2026-10-18

---

## Executive Summary

The Hairline Platform is a comprehensive medical tourism ecosystem designed to revolutionize the hair transplant industry by connecting patients with verified clinics worldwide. The platform streamlines the entire patient journey from initial consultation through post-treatment aftercare, while providing clinics with powerful tools to manage their operations and Hairline administrators with oversight capabilities.

### Vision

To become the world's leading platform for medical hair restoration by creating a seamless, transparent, and trustworthy experience that empowers patients to make informed decisions while enabling clinics to efficiently manage their practice.

### Business Goals

1. **Patient Acquisition**: Onboard 10,000+ patients in first year
2. **Provider Network**: Build network of 100+ verified clinics across 20+ countries
3. **Transaction Volume**: Facilitate $10M+ in medical procedures in year one
4. **Patient Satisfaction**: Achieve 4.5+ star average rating
5. **Market Position**: Become top-3 medical tourism platform for hair restoration

### Success Metrics

- **Conversion Rate**: 25% of inquiries to confirmed bookings
- **Platform NPS**: > 60
- **Provider Response Time**: < 24 hours for quote submission
- **Booking Completion**: 85% of accepted subquotes to confirmed bookings
- **Aftercare Engagement**: 70% of patients actively using aftercare features

---

## Product Overview

### System Architecture

The Hairline Platform consists of four distinct applications serving different user personas:

1. **Patient Platform** (Mobile App - iOS/Android)
   - Primary users: Patients seeking hair transplant procedures
   - Core function: Request quotes, book procedures, manage treatment journey

2. **Provider Platform** (Web Application)
   - Primary users: Clinics, hospitals, medical staff
   - Core function: Manage inquiries, submit quotes, execute treatments

3. **Admin Platform** (Web Application)
   - Primary users: Hairline internal team
   - Core function: Platform oversight, billing, provider management, aftercare coordination

4. **Affiliate Platform** (Web Portal)
   - Primary users: Influencers, marketing partners
   - Core function: Promote platform, track referrals, manage commissions

### Core Value Propositions

#### For Patients

- **Simplified Discovery**: Compare multiple clinics and quotes in one place
- **Price Transparency**: Clear, itemized pricing with no hidden fees
- **Travel Convenience (Phase 2)**: Book flights and hotels directly through the platform (MVP focuses on travel detail capture + coordination)
- **Quality Assurance**: All providers vetted and verified by Hairline
- **Comprehensive Support**: Dedicated aftercare team for post-procedure guidance
- **Head Scan Media** *(V1 photo set; true 3D in V2)*: Visual assessment inputs for treatment planning

#### For Providers

- **Lead Generation**: Access to qualified patient leads actively seeking procedures
- **Operational Efficiency**: Streamlined inquiry and quote management
- **Payment Security**: Guaranteed payments through escrow system
- **Marketing Support**: Featured placement in patient-facing app
- **Team Collaboration**: Multi-user access with role-based permissions
- **Analytics**: Insights into performance, conversion rates, and revenue

#### For Hairline (Business)

- **Commission Revenue**: Commission on each completed procedure, set per provider as either a Percentage (0 to 100%) of the booking total or a Flat Rate (FR-029); the global default is a percentage between 15% and 25%
- **Travel Revenue (Phase 2)**: Commissions from flight/hotel bookings (once in-app booking is live)
- **Subscription Revenue**: Provider subscription tiers (future)
- **Affiliate Partnerships**: Influencer-driven marketing channel
- **Data Assets**: Market intelligence on pricing, demand, and trends

---

## User Personas

### 1. Patient - David (Primary)

**Demographics**: 35-year-old professional from UK, married with kids  
**Income**: £50,000-£80,000/year  
**Hair Loss Stage**: Norwood 3-4  

**Goals**:

- Find affordable, high-quality hair transplant abroad
- Minimize time away from family (< 1 week)
- Ensure safety and quality of procedure
- Get ongoing support during recovery

**Pain Points**:

- Overwhelmed by options when researching clinics
- Uncertain about quality and credentials of foreign clinics
- Concerned about language barriers and logistics
- Worried about post-procedure complications without local support

**Motivation**: Restore confidence and appearance while maximizing value

---

### 2. Clinic Manager - Dr. Mehmet (Provider)

**Demographics**: 42-year-old surgeon operating clinic in Istanbul, Turkey  
**Experience**: 15 years in hair restoration, 200+ procedures/year  
**Clinic Size**: 3 surgeons, 8 technicians, 2 admin staff

**Goals**:

- Increase international patient volume
- Streamline patient communication and booking process
- Reduce no-shows and cancellations
- Build reputation through verified reviews
- Optimize pricing competitiveness

**Pain Points**:

- Time-consuming manual inquiry management across multiple channels
- Difficulty showcasing expertise to international patients
- Payment processing complexities with international clients
- Managing post-procedure support across time zones

**Motivation**: Grow clinic revenue while maintaining operational efficiency

---

### 3. Aftercare Specialist - Sarah (Hairline Team)

**Demographics**: 28-year-old nurse with telemedicine experience  
**Role**: Hairline aftercare coordinator  
**Workload**: 50-100 active aftercare cases

**Goals**:

- Provide timely support to recovering patients
- Identify and escalate complications early
- Maintain high patient satisfaction scores
- Document recovery progress for quality assurance

**Pain Points**:

- Managing multiple chat channels simultaneously
- Identifying patients who need urgent attention
- Language barriers with international patients
- Tracking milestones across different recovery timelines

**Motivation**: Deliver excellent patient outcomes and reduce complications

---

### 4. Platform Administrator - James (Hairline Operations)

**Demographics**: 33-year-old operations manager  
**Responsibilities**: Provider onboarding, billing, platform configuration  
**Reports To**: CEO/CFO

**Goals**:

- Onboard and verify new providers efficiently
- Ensure timely billing and commission payments
- Monitor platform health and key metrics
- Configure promotions and discounts
- Resolve payment disputes

**Pain Points**:

- Manual verification processes for new providers
- Complex multi-currency billing reconciliation
- Limited visibility into individual transaction details
- Time-consuming discount code management

**Motivation**: Scale platform operations while maintaining quality and profitability

---

## Core Workflows

### Workflow 1: Patient Journey - From Inquiry to Recovery

**Actors**: Patient, Provider(s), Hairline Admin Team, Aftercare Specialist

**Stages**:

1. **Discovery & Registration**
   - Patient downloads app and creates account
   - Completes health questionnaire
   - Captures head scan photo set *(V1; true 3D scan in V2)* (and uploads optional photos/videos)

2. **Inquiry Submission**
   - Selects preferred countries/cities for treatment
   - Selects preferred treatment dates
   - Submits inquiry to matching providers
   - System distributes inquiry to providers in selected locations

3. **Subquote Comparison**
   - Receives parent quotes from multiple providers, including multiple parent quotes from one provider (24-72 hours)
   - Compares complete subquotes across parent quotes by package, date range, appointment, price, reviews, credentials, and inherited clinical context
   - Asks clarifying questions through chat
   - Reviews before/after photos and provider credentials

4. **Subquote Acceptance & Slot Hold**
   - Accepts exactly one preferred subquote per inquiry; acceptance atomically places one fixed exclusive hold on the appointment slot (keyed by provider, appointment date/time, and time zone) for the FR-026 slot-hold duration (default 48 hours) and rejects a competing acceptance before creating an AcceptanceEvent or booking handoff
   - Provider must pre-schedule appointment times in quote submission
   - Accepted subquote and its inherited parent context are snapshotted (price after promotion, currency, date range, appointment, promotion, and the exchange rate with its timestamp); its parent quote and inquiry move to "Accepted"
   - Sibling subquotes become "Not Selected" and competing parent quotes auto-cancel
   - Sees the booking as "Booking Accepted — Slot Held (Pending Payment)" (booking status `Accepted`): the slot is held, not yet booked, and no appointment record exists until payment

5. **Payment & Confirmation**
   - Makes payment (deposit or full amount, or selects installment plan)
   - Installment plans: 2-9 months interest-free (must complete 30 days before procedure)
   - The first successful payment (deposit or first installment) before the hold expires moves the booking to "Confirmed", creates the appointment record, and blocks the slot in the provider calendar
   - Payment failure or retry never extends or restarts the hold; if no payment succeeds before the hold expires, the booking moves to "Payment Window Expired" (final except for the audited admin revive), the slot is released, and the accepted quote is not reopened. The patient cannot cancel after acceptance; they contact support, who can either revive the booking through the audited admin revive (back to "Accepted" with a new hold) or cancel it as an admin so the patient can start a new inquiry
   - A missed later installment or final payment never causes "Payment Window Expired"
   - Patient anonymization lifted - provider can now see full name and contact details
   - Receives final booking confirmation

6. **Travel Planning**
   - If provider included travel: submits passport details so provider can book externally
   - If patient self-books: submits confirmed flight + hotel details for coordination
   - Reviews unified itinerary and clinic instructions (Phase 2: in-app flight/hotel booking via APIs)

7. **Pre-Procedure**
   - Receives pre-op instructions and medication list
   - Confirms arrival details with clinic
   - Checks in to hotel
   - Attends pre-procedure consultation

8. **Procedure Day - Treatment Execution**
   - Arrives at clinic (status moves to "In Progress")
   - Provider documents patient arrival and pre-procedure notes
   - Undergoes hair transplant procedure
   - Provider updates treatment progress in real-time
   - Provider documents procedure details, graft counts, techniques used
   - From `Confirmed`, treatment plan days, clinicians, or estimated grafts can change only through FR-010, by the clinic until Check In or by an admin at any time from `Confirmed` onward, each with a reason, an audit record, and a patient notice; they are locked while the booking is unpaid, and locked for the clinic after Check In. Price, currency, date range, and promotion never change, and only an admin can change the appointment date/time (FR-006)
   - Treatment completion moves status to "Aftercare"
   - Receives post-op instructions and medications

9. **Aftercare (6-12 months)**
   - Returns home
   - Receives scheduled notifications for washing, medication, activities
   - Uploads progress photos at milestones (1 week, 1 month, 3 months, 6 months, 12 months)
   - Chats with aftercare specialists for questions/concerns
   - Completes recovery questionnaires
   - Submits final review and rating (status moves to "Completed")

**Exception - provider fault after acceptance**: If the selected provider withdraws the accepted quote, drops out before or during treatment, or is suspended or deactivated after acceptance, a booking in Accepted or Confirmed is cancelled with a provider-fault cause and the inquiry stays open and is flagged for admin support. For such a booking, an admin authors a replacement quote on behalf of a replacement provider in the same inquiry; when the patient accepts it, the original acceptance is superseded by a single linked record and the patient re-enters nothing. A booking in In Progress is not cancelled automatically: it stays In Progress, is flagged for admin support, and an admin either moves it to Aftercare and reassigns the aftercare provider or cancels it with a reason. During Aftercare the booking is not cancelled; an admin reassigns the aftercare provider instead (FR-003, FR-006, FR-015).

---

### Workflow 2: Provider Quote Management

**Actors**: Provider (Clinic Staff), Patient

**Stages**:

1. **Inquiry Receipt**
   - Receives notification of new inquiry matching clinic's location
   - Reviews patient details, head scan capture assets *(V1 photo set; true 3D scan in V2)*, medical history, preferences
   - Reviews medical questionnaire with color-coded alerts

2. **Quote Creation**
   - **Selects treatment** (from admin-created list: FUE, FUT, DHI, etc.) - foundation, same for all providers
   - **Selects one to five packages** from own package library (versioned templates holding included services and their prices, travel services such as hotel, transport, and flights, and a relative-day treatment plan); each package seeds one Quote Option and may be customised inline for this quote only
   - Analyzes head scan capture assets *(V1 photo set; true 3D scan in V2)* to estimate graft count needed
   - **Selects clinician** who will perform the procedure (from clinic's staff list)
   - Customizes graft count, technique specifications
   - Sets an offered price for every applicable option/date-range combination (prefilled from the package standard price); package prices are never summed
   - Adds photos/videos of similar cases or visual treatment plan
   - **Pre-schedules an appointment for every applicable option/date combination** (required for auto-accept)
   - Eligible automatic promotions attach to option/date-price rows when the quote is sent, with their terms fixed at send
   - Adds notes for patient

3. **Quote Submission**
   - Submits quote to patient with pre-scheduled appointment times (deadline: 72 hours from inquiry)
   - Quote expiry (FR-026 Quote Expiry Window, default 48 hours, admin-configurable) and quote currency are captured at first send; there is no per-quote extension
   - Quote enters patient's comparison dashboard

4. **Negotiation (Optional)**
   - Responds to patient questions through chat
   - May revise a sent quote before acceptance; each revision creates a new parent quote version with audit history
   - Provides additional information or credentials

5. **Subquote Acceptance (Auto-Scheduled)**
   - Receives notification when one of the provider's subquotes is accepted or its parent quote is auto-cancelled
   - Appointment is AUTOMATICALLY selected from the accepted subquote's Option/date-price record
   - No manual confirmation needed - the selected subquote and parent quote move directly to "Accepted" status
   - The slot is held for the patient's first payment; the booking becomes "Confirmed" and the appointment record is created only on successful payment
   - The accepted quote is locked: treatment-detail changes go through FR-010, and a provider withdrawal or drop-out follows the FR-006 provider-fault transfer
   - Patient proceeds to payment

6. **Pre-Procedure Preparation**
   - Sends pre-op instructions
   - Confirms appointment 48 hours prior
   - Prepares treatment room and materials

---

### Workflow 3: Admin Oversight & Billing

**Actors**: Admin Team, Providers, Patients, Payment Gateway (Stripe)

**Stages**:

1. **Provider Onboarding**
   - Reviews provider application and credentials
   - Verifies medical licenses and certifications
   - Conducts video interview and facility tour
   - Sets up provider account with commission structure
   - Approves provider for live patient inquiries

2. **Transaction Monitoring**
   - Monitors all quotes, bookings, and payments
   - Tracks parent quote response rates and subquote selection rates separately by provider
   - Identifies stuck inquiries or delayed quotes
   - Intervenes in patient-provider disputes

3. **Billing & Commissions**
   - Collects patient payments (deposit and final)
   - Holds funds in escrow until procedure completion
   - Calculates platform commission using the provider's FR-029 model (Percentage or Flat Rate; global percentage default 15-25%)
   - Processes provider payouts on monthly/bi-weekly cycle
   - Generates invoices and tax documents

4. **Aftercare Coordination**
   - Assigns aftercare specialists to new patients
   - Monitors aftercare engagement and milestone completion
   - Escalates medical concerns to clinic or local providers
   - Manages aftercare questionnaires and satisfaction surveys

5. **Promotions & Discounts**
   - Creates discount codes for marketing campaigns
   - Configures provider-specific promotions
   - Tracks discount code usage and ROI
   - Manages affiliate commission structures

6. **Analytics & Reporting**
   - Generates platform-wide performance reports
   - Analyzes conversion funnels and drop-off points
   - Reviews provider performance metrics
   - Prepares executive dashboards for leadership

---

## Functional Requirements

### FR-001: Patient Authentication & Profile Management

**Priority**: P1 (MVP)  
**Module(s)**: P-01: Auth & Profile Management

**Requirements**:

- System MUST allow patients to register with email/password (registration available ONLY via mobile app; admins cannot create new patients)
- System SHOULD support social authentication (Google, Apple, Facebook) [future]
- System MUST verify email addresses via 6-digit OTP (not link); OTP expiry and resend rate limits MUST be configurable
- System MUST allow password reset via 6-digit OTP sent to email
- Patients MUST be able to update profile information (name, phone, birthday, location)
- System MUST store profile images securely
- System MUST support multi-factor authentication (future enhancement)

**Security & Policy Configuration (centrally managed via A-09)**:

- Password policy: FIXED in codebase — at least 12 characters, at least one uppercase, one lowercase, one digit, and one special character from !@#$%^&(),.?":{}|<> (not editable in Admin)
- Authentication throttling: maximum login attempts before lockout and lockout duration MUST be configurable
- OTP settings: code length is FIXED at 6 (not editable in Admin); expiry time and resend cooldown MUST be configurable
- Country list and country calling codes used in profile MUST be centrally managed
- Discovery question options MUST be centrally managed

**Data Security**:

- Passwords MUST be hashed using bcrypt (cost factor 12+)
- Password changes MUST NOT reuse any of the last 5 passwords (password history enforcement)
- Personal data MUST be encrypted at rest
- System MUST maintain audit log of profile changes

---

### FR-002: Medical History & 3D Scanning

**Priority**: P1 (MVP)  
**Module(s)**: P-07: 3D Scan Capture & Viewing | S-01: 3D Scan Processing Service | S-05: Media Storage Service

**Note on Release Scope:**
For V1, the system implements "3D scan" capture as a standardized head scan **photo set** (multiple 2D views). True 3D model capture and the full ARKit/ARCore 3D processing pipeline are deferred to V2 (future enhancement), as patient-side hardware and provider UX mature.

**Requirements**:

- Patients MUST complete comprehensive medical questionnaire before submitting inquiry
- System MUST capture head scan media of patient's head using mobile camera *(V1: standardized photo set; V2: true 3D scan)*
- System MUST support upload of additional photos/videos as supplemental evidence
- System MUST validate scan quality and provide feedback
- Medical history MUST include allergies, medications, previous procedures, health conditions
- System MUST anonymize patient data in provider-facing views until payment completion

**Medical Condition Alert System**:

- System MUST flag medical conditions with 3-tier alert system:
  - **Critical (Red)**: High-risk conditions (HIV, blood disorders, heart conditions, uncontrolled diabetes, bleeding disorders)
  - **Standard (Yellow/Amber)**: Moderate concerns (allergies, current medications, controlled conditions, high blood pressure)
  - **None (Green)**: No medical concerns flagged
- Provider interface MUST color-code medical questionnaire responses
- Critical conditions MUST require provider acknowledgment before quote submission

**3D Scanning**:

- V1: MUST provide real-time guidance for standardized head scan photo set capture
- V1: MUST capture multiple predefined 2D views for provider review
- V2 (future): MUST support iOS ARKit and Android ARCore for true 3D capture
- V2 (future): MAY generate multiple 2D views from a 3D scan for provider review

---

### FR-003: Inquiry Submission & Distribution

**Priority**: P1 (MVP)  
**Module(s)**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight

**Requirements**:

- Patients MUST be able to select multiple countries/cities for treatment (max 10 countries)
- Patients MUST indicate preferred treatment dates (max 10 date ranges, up to 2 years in future)
- Patients MUST select one active treatment-area option from the Admin-managed FR-026 catalog; the client receives the option ID, label, and image/icon URL from the backend.
- The earliest selectable treatment date MUST use the Admin-configured inquiry lead time in days (default 3), consistently in the patient calendar and backend submission validation.
- Patients MUST select preferred providers (max 5 providers) based on reviews and admin curation
- Patients can only have one active inquiry at a time
- System MUST distribute inquiry to providers in selected locations OR explicitly selected by patient
- System MUST limit inquiry distribution to maximum 10 providers
- Providers MUST receive inquiry notification within 5 minutes
- System MUST track inquiry expiration (72 hours for quote submission)
- System MUST allow patients to close or cancel an inquiry only in the Inquiry or Quoted stages (FR-003 Workflow 5); after acceptance the patient contacts support, and only an admin can cancel the booking, from any booking state, with a mandatory reason and an audit entry. The inquiry then moves to Cancelled and the accepted quote stays accepted
- When the accepted provider withdraws or drops out after acceptance, or its suspension or deactivation takes effect, the inquiry MUST NOT be cancelled: it keeps its stage, is flagged `supportRequired`, and an admin resolves it through FR-006: a transfer to a replacement provider in the same inquiry for a booking in `Accepted` or `Confirmed`, a case-by-case decision (move to `Aftercare` with aftercare-provider reassignment, or cancellation with a reason) for a booking in `In Progress`, and aftercare-provider reassignment for a booking in `Aftercare`
- System MUST support secondary service options: Monitor Hair Loss, Aftercare services
- System MUST generate unique inquiry IDs in HPID format (HPID + YY + MM + 4-digit sequence)

**Business Rules**:

- Inquiry MUST include: patient scan, medical history, destinations, treatment date ranges, and selected providers
- Inquiry MUST retain a snapshot of its selected treatment-area option so later catalog changes do not alter historical inquiry display.
- Inquiry MUST NOT include: patient name, exact location, contact information (until booking)
- System MUST allow patients to search/filter providers by country, rating, and specialty, then explicitly select providers for inquiry distribution (see FR-022 / FR-003 / Screen 7a for full search/filter criteria)
- Provider suggestions MUST be based on: positive reviews, admin curation
- Patient names MUST be partially masked for providers until booking/payment confirmation (full identity only visible after successful payment, per Constitution)
- Admins MAY see full patient identity (unmasked) in A-01 views for compliance and support purposes
- Medical alerts MUST be color-coded: red (critical), yellow (standard), green (no alerts)
- Date ranges MUST display primary range prominently with tooltip for additional ranges
- Time display MUST use relative format for recent inquiries, specific format for older ones

---

### FR-004: Quote Submission & Management

**Priority**: P1 (MVP)  
**Module(s)**: PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight

**Requirements**:

- Providers MUST select treatment from the admin-created list (FUE, FUT, DHI, etc.). The quote MUST retain the exact immutable Treatment ID/version relationship so treatment name, type, and technique details can be loaded without duplicating treatment-owned data on the Quote.
- Providers MUST offer one to five package-based Quote Options per quote; each selected package version from the provider's own library (hotels, transport, flights, medications, PRP) seeds exactly one option, and packages are never summed into one option
- Providers MUST be able to customize a selected package inline for the current quote; the customization is a quote-local copy and MUST NOT create or update a reusable package-library record or package version
- Each Quote Option MUST record its source package ID, source package version, and an inline-customised flag
- A provider MAY submit multiple parent quotes for the same inquiry, each with an independent lifecycle, expiry, version history, and audit history
- Providers MUST pre-schedule an appointment time for every applicable option/date combination as part of quote submission
- Quotes MUST include: the exact selected Treatment version, its related read-only technique details when documented in FR-024, graft count, one to five package options, per-option pricing, timeline, and a pre-scheduled appointment slot for every applicable option/date combination. Technique details are loaded through the Treatment relationship and are not separate provider input or duplicated Quote data.
- Quote currency MUST be captured read-only at first send from the active FR-026 quote configuration (the FR-029 Default Currency); it is never provider input, and packages carry no currency. The platform supports multiple currencies across quotes, and the exchange rate is locked at acceptance rather than entered per quote
- If the Default Currency changes while a draft holds prices, the draft MUST switch to the new currency with its prices kept as typed, and the provider MUST acknowledge a "currency changed, check your prices" banner before the quote can be sent
- Providers MUST be able to attach before/after photos, credentials, facility images
- Providers MUST set an offered price greater than 0 for every applicable option/date combination before send; that price covers the treatment and the option's inclusions, and a date range the clinic cannot serve is left out of that option rather than priced at 0. System MUST derive the quote's price range from the complete option/date matrix, and the accepted total only after the patient selects one option/date combination
- System MUST store the offered price as entered with any promotion discount kept separate, MUST attach every eligible automatic promotion to each eligible option/date-price row at send, and MUST copy the attached promotion terms into the sent quote version; later promotion edits never change a sent quote
- Providers MUST submit quotes within 72 hours of inquiry receipt
- System MUST validate quote completeness before submission
- Quote expiry MUST be captured at first send from the FR-026 Quote Expiry Window (default: 48 hours, admin-configurable); drafts carry no expiry and there is no per-quote extension
- Quote statuses are: draft, sent, expired, withdrawn, archived, accepted, cancelled_other_accepted, cancelled_inquiry_cancelled, and cancelled_provider_status (unaccepted quotes only). `Confirmed` is a booking status, not a quote status
- Re-sending a new version of a sent quote MUST emit `quote.updated` ("quote revised (new version)"); FR-004 owns this event
- After a subquote is accepted, System MUST block every FR-004 quote edit by providers and admins; treatment-detail changes (plan, clinicians, grafts) go through FR-010. An accepted parent quote is never reopened, including after `Payment Window Expired`
- A provider withdrawal of an accepted quote moves it to `withdrawn` and hands the case to the FR-006 provider-fault transfer

**Subquote Acceptance Handoff**:

- When the patient accepts a subquote, its exact appointment is selected and the system atomically acquires one fixed exclusive hold on the slot, keyed by provider, appointment date/time, and time zone, for the FR-026 slot-hold duration (default 48 hours); if another pending or confirmed booking already holds or blocks that slot, acceptance is rejected before any AcceptanceEvent, quote/inquiry state change, or booking handoff is created. FR-004 creates no appointment record
- System immediately moves the inquiry and selected parent quote to "Accepted" and creates the pending booking handoff in booking status `Accepted`; the booking becomes `Confirmed`, and the appointment record is created, only on successful deposit or first-installment payment
- Provider receives notification of the accepted subquote and reserved appointment details; the patient receives only the booking notice "Booking Accepted — Slot Held (Pending Payment)"
- Patient proceeds directly to payment screen

**Quote Components**:

**1. Treatment (Required - Admin-Created)**:

- Treatment type (FUE, FUT, DHI, etc.) - selected from admin list and retained as an exact immutable Treatment-version relationship
- Graft count estimation
- Technique specifications - loaded read-only through the related Treatment version; not stored as a duplicate Quote field
- No separate treatment price on the quote; each option/date offered price covers the treatment and the option's inclusions

**2. Quote Options (Required - One to Five, Provider-Created)**:

Each option is a quote-local copy of one package version that the patient can compare. Options share the parent quote's treatment, graft facts, visual plan, clinicians, and common notes; they differ by inclusions, applicable date ranges, prices, promotions, and day-to-day plan.

- Hotel packages (4-star, 5-star, etc.)
- Transport packages (airport pickup, transfers)
- Flight assistance packages
- Medication packages (post-op medications)
- Additional services (PRP therapy, specialized treatments)
- Offered price per applicable option/date combination, prefilled from the package standard price and set by the provider
- Option-local custom services added for this patient only
- A separate relative day-to-day treatment plan per option (Day 1, Day 2, ...; never converted to calendar dates)

**3. Other Components**:

- Clinician selection
- Pre-scheduled appointment time slots

**Pricing Rules**:

- Quote MUST lock exchange rate at time of patient acceptance; the rate and its timestamp are recorded in the acceptance snapshot
- Commission shown on the quote is indicative only; the binding commission is fixed at booking confirmation on the booking total (accepted subquote price after promotion, in the quote currency, from the acceptance snapshot)
- Quote-amount analytics MUST use the accepted option/date price only; an unaccepted quote has a price range, not an amount
- Quote MUST clearly separate provider fees from Hairline platform fees
- Quote MUST show original price and discount if applicable

---

### FR-005: Quote Comparison & Acceptance

**Priority**: P1 (MVP)  
**Module(s)**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight

**Requirements**:

- Patients MUST be able to view all received parent quotes grouped by provider and expose each eligible child subquote as a complete selectable choice
- System MUST display subquote-owned package, date-range, appointment, price, promotion, and treatment-plan details together with inherited graft, review, credential, provider, and clinical context
- Patients MUST be able to filter and sort subquotes using both subquote-owned and inherited criteria (see FR-022 / FR-005 / Screen 1 for full filter criteria)
- Price sort MUST compare each price converted to the patient's display currency at the current rate, for ordering only; each card still shows its own quote currency, and the ordering MUST be labelled approximate when currencies are mixed
- Patients MUST be able to ask questions about quotes through secure messaging (see FR-012; MVP channel: Patient ↔ Provider)
- System MUST notify providers of patient questions within 5 minutes (via real-time messaging notifications)
- Patients MUST be able to accept exactly one current subquote per inquiry; parent quotes and upper-level records MUST NOT be direct acceptance targets
- Acceptance MUST atomically acquire an exclusive hold on the selected appointment slot (one active hold per provider, appointment date/time, and time zone) and reject a second acceptance for a held or blocked slot before creating an AcceptanceEvent or booking handoff; the patient is told the slot was just taken
- Patients MAY enter a promotion code on one named subquote before acceptance; the system validates it for that subquote only
- System MUST snapshot the accepted subquote identifier/version, parent quote identifier/version, complete commercial terms (price after promotion, currency, date range, appointment, promotion, and the exchange rate with its timestamp), and inherited context; the subquote version MUST equal the owning parent aggregate `QuoteVersion`
- The AcceptanceEvent and its snapshot MUST be append-only and never edited; supersession (causes `ProviderFault`, `ProviderSuspended`, `ProviderDeactivated`) and annotations are separate linked records. A supersession record is inserted only once, at the acceptance of the admin-authored replacement quote in the FR-006 provider-fault transfer, and links the original acceptance to the new admin-authored acceptance record
- System MUST mark sibling subquotes in the accepted parent quote "Not Selected" and auto-cancel competing parent quotes with reason "Other subquote accepted"
- System MUST notify affected providers immediately (`quote.accepted` outcomes go to providers only) without exposing the selected provider or accepted price to non-selected providers; the patient receives only `booking.scheduled` ("Booking Accepted — Slot Held (Pending Payment)"), and admins receive no alert for a routine acceptance
- Parent quote response metrics and subquote comparison/selection metrics MUST remain distinct

**Comparison Features**:

- Side-by-side comparison view (up to 3 subquotes across any parent/provider grouping)
- Price per graft calculation
- Review rating and count
- Provider credentials summary
- Included services checklist
- **Future (Phase 2)**: Estimated travel costs (requires flight API integration; not MVP)

---

### FR-006: Booking & Scheduling

**Priority**: P1 (MVP)  
**Module(s)**: P-03: Booking & Payment | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight

**Requirements**:

- Booking uses an **auto-scheduled** model: provider pre-schedules appointment slots on FR-004 Option/date-price records; patient accepts one complete subquote in FR-005, and FR-006 consumes that accepted subquote plus its immutable inherited parent context without package, date, appointment, or price reselection.
- Every pending or confirmed Booking MUST link to exactly one FR-005 AcceptanceEvent, accepted parent quote identifier/version, accepted subquote identifier/version, immutable acceptance snapshot, and provider calendar slot; accepted parent and subquote versions MUST identify the same FR-004 aggregate `QuoteVersion`.
- Booking statuses are: `Accepted` (slot held pending first payment; shown to the patient as "Booking Accepted — Slot Held (Pending Payment)"), `Payment Window Expired`, `Confirmed`, `In Progress`, `Aftercare`, `Completed`, and `Cancelled`. Apart from the automatic transitions, payment, Check In and the audited admin revive, the only manual status changes are an admin cancellation, allowed from any booking state with a mandatory reason and an audit entry, and the admin move of an `In Progress` booking to `Aftercare` with aftercare-provider reassignment after a provider fault.
- Acceptance places one fixed exclusive hold keyed by provider, appointment date/time, and time zone for the FR-026 slot-hold duration (default 48 hours), starting at acceptance; payment failure or retry never extends or restarts it. FR-006 MUST verify that the AcceptanceEvent owns the slot's valid exclusive hold before payment initiation. Successful deposit or first-installment payment moves the booking to `Confirmed`, creates the appointment record, and converts that hold into the confirmed calendar block.
- If the payment window expires, the Booking MUST transition to `Payment Window Expired` (final except for the audited admin revive), release the slot, block payment against that accepted selection unless an admin revives the booking, preserve the immutable AcceptanceEvent/snapshot, and MUST NOT reopen the parent quote or accepted subquote. `Payment Window Expired` applies only to the first payment step; a missed later installment or final payment never causes it.
- Admin MAY revive a `Payment Window Expired` booking to `Accepted` only with a mandatory reason, a slot availability re-check, a new hold of the FR-026 duration, the promotion use taken again for an automatic promotion or reserved again for a provider-selected promotion or patient code (the revive is rejected if the limit has no room), an audit entry, an unchanged AcceptanceEvent, and a mandatory "booking revived" notice to patient and provider. No other manual status change is allowed apart from the admin cancellation and the provider-fault move from `In Progress` to `Aftercare`.
- An admin appointment change MUST move the booking's current appointment and send the mandatory `booking.rescheduled` to patient and provider. Booking notices MUST read the booking's current appointment, while the acceptance snapshot keeps the accepted appointment as the baseline and is never edited.
- When the provider withdraws or drops out after acceptance, or its suspension or deactivation takes effect, a booking in `Accepted` or `Confirmed` MUST be cancelled with cause `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated` and a `supportRequired` marker, the hold or calendar block released, and the AcceptanceEvent kept unchanged. For a booking in `Accepted` or `Confirmed`, an admin authors a replacement quote on behalf of a replacement provider in the same inquiry; when the patient accepts it, a new admin-authored acceptance record is created and a single supersession record linking it to the original is inserted in the same transaction. No automatic promotion attaches to the replacement quote and no promotion use is reserved for it; the admin sets the replacement price directly. A replacement quote that is not accepted expires normally; the inquiry stays `supportRequired` and is not cancelled automatically, and the admin may author another replacement quote or cancel the inquiry and booking. In `In Progress` the booking MUST NOT be cancelled automatically: it stays `In Progress` with `supportRequired`, and an admin either moves it to `Aftercare` and reassigns the aftercare provider, or cancels it with a mandatory reason; no replacement acceptance is created. In `Aftercare` the booking is not cancelled; an admin reassigns the aftercare provider, which sends the mandatory `aftercare.provider_reassigned` to the patient and the new aftercare provider. Paid amounts move with the patient as credit toward the replacement booking, any unused part is refunded, and the patient pays no cancellation fee; exact mechanics are defined in FR-007, FR-007B, and FR-017.
- System MUST integrate with provider's calendar to validate availability at quote creation time and to block the slot upon payment-confirmed booking
- Patients MUST confirm booking by paying deposit (admin-configurable percentage, default 20-30% of the booking total, configured via FR-029); the booking total is the accepted subquote price after promotion, in the quote currency, read from the acceptance snapshot
- System MUST generate booking confirmation with reference number
- System MUST send confirmation emails to patient and provider
- **Rescheduling is deferred to V2**; in MVP, an admin MAY change the appointment date/time of an `Accepted` or `Confirmed` booking only with a mandatory reason and a slot availability check; the change is audited and triggers an FR-008 travel review of linked travel records (see FR-006 PRD)
- System MUST enforce cancellation policy with graduated refund schedule
- System MUST block out provider calendar upon confirmed booking

**Cancellation Policy** (example):

- > 30 days before: 90% refund
- 15-30 days before: 50% refund
- < 15 days before: No refund (unless medical emergency with documentation)

---

### FR-007: Payment Processing

**Priority**: P1 (MVP)  
**Module(s)**: P-03: Booking & Payment | A-01: Patient Management & Oversight | A-05: Billing & Financial Reconciliation | S-02: Payment Processing Service

**Requirements**:

- System MUST integrate with Stripe for payment processing
- System MUST support credit/debit cards and bank transfers
- System MUST process payments in multiple currencies (USD, EUR, GBP, TRY, etc.)
- Deposit payment MUST be processed at booking confirmation
- Final payment MUST be processed on procedure day or before
- System MUST support split payments (deposit + final payment)
- System MUST generate receipts and invoices for all transactions
- System MUST support refunds per cancellation policy
- System MUST calculate and track platform commission on each transaction

**Payment Flow** (V1 - Direct Payment):

- Payments processed directly through Stripe
- Provider payouts initiated after treatment completion (admin-triggered)
- Platform commission deducted at time of payout
- **Future Enhancement**: Escrow/fund holding (V2) - funds held until procedure completion

**Payment Security**:

- System MUST be PCI-DSS compliant (via Stripe)
- System MUST NOT store credit card numbers
- All payment data MUST be transmitted over TLS 1.3
- System MUST support 3D Secure (3DS) for card authentication

**Commission Structure**:

- Platform commission: the provider's FR-029 model, either a Percentage (0 to 100%) or a Flat Rate per completed procedure (global percentage default 15-25%), applied to the booking total, which is the accepted price after promotion from the acceptance record; the deposit percentage, instalment amounts and commission all use this same booking total
- Commission MUST be deducted from provider payout
- System MUST generate commission reports for accounting
- Admin triggers provider payout after treatment completion

---

### FR-007B: Split Payment / Installment Plans

**Priority**: P1 (MVP)  
**Module(s)**: P-03: Booking & Payment | S-02: Payment Processing Service

**Requirements**:

- System MUST offer interest-free installment payment plans to patients
- Installment options: 2, 3, 4, 5, 6, 7, 8, or 9 monthly payments
- System MUST calculate maximum available installments based on time until procedure
- Final payment MUST be completed 30 days before scheduled procedure date
- System MUST automatically calculate installment amounts (booking total ÷ number of installments), using the same booking total as the deposit and commission (accepted price after promotion, from the acceptance record)
- Patients MUST be able to select installment plan at checkout
- System MUST automatically charge installments on scheduled dates
- System MUST send payment reminders 3 days before each installment
- System MUST handle failed installment payments (3 retry attempts)
- If installment plan defaults, booking MUST be flagged and admin notified

**Business Rules**:

- Example: Procedure in 6 months = maximum 5 installments (30-day buffer)
- Example: Procedure in 3 months = maximum 2 installments
- Patient can choose fewer installments than maximum available
- Single full payment always available as alternative

---

### FR-008: Travel Booking Integration

**Priority**: P2 (Enhanced)  
**Module(s)**: P-04: Travel & Logistics | A-04: Travel Management | S-04: Travel API Gateway

**Requirements**:

- In MVP, the system MUST NOT support in-app flight or hotel booking; all bookings occur externally (patient self-booked or provider-booked) and the platform is used for travel detail capture + coordination (see FR-008 PRD).
- System MUST support two travel paths per confirmed appointment:
  - **Path A (Provider-included travel)**: provider books externally for the travel services included in the accepted package (any mix of flight, hotel, transport). System requests passport details from patient. Patient does not submit flight/hotel records in Path A.
  - **Path B (Patient self-booked travel)**: patient books externally. System requests flight/hotel details from patient. Provider does not enter travel records in Path B. No passport request is sent.
- System MUST trigger the appropriate travel request automatically when an inquiry transitions to **Confirmed** status (post-payment confirmation); no manual trigger required.
- System MUST store passport, flight, and hotel travel records against the booking's travel context (`travel_context_id`, one per booking) and assemble a unified itinerary view for patient, provider, and admin.
- Travel records MUST be locked after submission; patients/providers cannot edit submitted records; admin corrections MUST be versioned and auditable with mandatory reason notes.
- The itinerary is a read view assembled from the travel context, flight and hotel records, and the booking; it is not stored as a separate record.
- System MUST show a soft warning when a return flight or hotel check-out falls before the last treatment plan day; the warning must be acknowledged, the record can still be saved, and the provider sees the flag.
- In an FR-006 provider-fault transfer, the passport record MUST carry over to the replacement booking, and flight and hotel records MUST be copied and flagged "travel-date review required"; the originals stay read-only on the closed booking.
- System MUST send email + in-app notifications for travel record requests, submissions, provider-entered records, and admin corrections.

**Phase 2 (Post-MVP): In-App Travel Booking + Cost Preview**

- System SHOULD integrate with a flight booking API (e.g., Amadeus, Skyscanner) to enable in-app flight search/booking and travel cost preview.
- System SHOULD integrate with a hotel booking API (e.g., Booking.com, Expedia) to enable in-app hotel selection/booking.
- During inquiry date selection, system SHOULD display estimated flight costs once flight API integration is live.

**Phase 2 (Post-MVP): Travel Commission**

- Platform MAY earn commission on flight/hotel bookings once in-app booking is live; this commission MUST be tracked separately from procedure commission.

---

### FR-009: Provider Team & Role Management

> The custom-role extension below is proposed in [CR-FR009-20260929-01](functional-requirements/fr009-provider-team-roles/change-request-2026-09-29-custom-provider-role-assignment.md); the four protected-role baseline remains approved.

**Priority**: P1 (MVP)  
**Module(s)**: PR-01: Auth & Team Management

**Requirements**:

- Providers MUST be able to invite team members to platform
- System MUST support four protected provider roles (Owner, Manager, Clinical Staff, Billing Staff) and global custom provider roles defined by Super Admins in FR-031
- Each role MUST have specific access rights to features and data
- Team members MUST be able to collaborate on inquiries and quotes
- System MUST log all actions by user for audit trail
- Providers MUST be able to remove or suspend team members (within Owner/Manager permissions)
- System MUST send email invitations to new team members

**Role Permissions**:

- **Owner (Main Account Holder)**: Full access, billing, team management, and legal/contract responsibility; only role allowed to manage bank account details.
- **Manager (Clinic Manager / Operations)**: Broad operational access across inquiries, quotes, schedules, and day-to-day team management, but no ability to change bank account details or assign/change the primary Owner role.
- **Clinical Staff**: Access to in-progress and aftercare sections, treatment execution and documentation, and clinical notes; limited or no access to billing configuration.
- **Billing Staff**: Access to financial views (quotes, payouts, revenue metrics) and reconciliation screens; no access to treatment documentation or team structure changes.
- **Custom provider roles**: Globally defined by Super Admins from a non-Owner base type; assignable to non-Owner staff by provider organizations. The base type and explicit permission grants preserve role-limited actions, and no custom role can replace the primary Owner.

---

### FR-010: Treatment Execution & Documentation

**Priority**: P1 (MVP)  
**Module(s)**: PR-03: Treatment Execution & Documentation

**Requirements**:

- System MUST create the treatment record at booking confirmation (first successful payment) with status Awaiting Check In; treatment statuses are Awaiting Check In, In Progress, Completed, and Cancelled
- Providers MUST be able to **Check In** a confirmed booking when the patient arrives at clinic
- System MUST automatically move status to **"In Progress"** upon Check In
- System MUST block Check In when there is an outstanding balance (Payment Status ≠ Full paid)
- Providers MUST be able to update day-based treatment progress during procedure (real-time updates)
- System MUST capture treatment documentation: procedure date/time, assigned clinician/surgeon, treatment type (from treatmentId), estimated vs. actual graft count, and treatment notes/observations
- Providers MUST be able to upload before/during/after photos and head-scan capture assets *(V1: standardized photo set; V2: true 3D capture)* via S-05
- Providers MUST be able to prescribe medications and provide post-op instructions
- System MUST generate post-op instruction sheet for patient
- System MUST record treatment completion and signal FR-011 to activate aftercare plan and transition status to **"Aftercare"**
- System MUST read price, currency, date range, and promotion only from the accepted snapshot reached through the booking's AcceptanceEvent, MUST read the procedure appointment from the booking's current appointment (the snapshot keeps the accepted appointment as the baseline), and MUST seed the case's treatment plan days, clinician set, and estimated graft count from the same snapshot; FR-010 never edits the snapshot or reads accepted data from live quote records
- FR-010 MUST be the only path for post-acceptance changes to treatment plan days, clinician set, and estimated graft count, limited to the clinic (Owner, Manager, or Clinical Staff, from `Confirmed` until Check In) and admins (at any time from `Confirmed` onward); treatment details are locked while the booking is `Accepted` (unpaid); each change requires a reason, is audited with before/after values, notifies the patient (`treatment.plan_changed`), leaves the accepted snapshot unchanged, and never changes money fields
- Treatment plan days MUST be displayed and stored as relative day numbers only (Day 1, Day 2, ...), never as calendar dates
- FR-010 MUST NOT reassign the treating provider; provider withdrawal, drop-out, or replacement after acceptance is handed to the FR-006 provider-fault transfer

**Status Transitions**:

- Patient Check In → Status: "In Progress"
- Treatment completed (End Treatment saved) → Status: "Aftercare" *(via FR-011 aftercare activation)*
- Final review submitted → Status: "Completed"

---

### FR-011: Aftercare & Recovery Management

**Priority**: P1 (MVP)  
**Module(s)**: P-05: Aftercare & Progress Monitoring | PR-04: Aftercare Participation *(elevated to P1 scope for FR-011 delivery)* | A-03: Aftercare Team Management

---

#### Part A: Treatment-Linked Aftercare Setup

**Provider Aftercare Template Selection**:

- Providers MUST select aftercare template during treatment completion
- System MUST provide pre-defined milestone templates created by admin
- Providers MUST be able to customize template with patient-specific instructions
- Providers MUST specify post-op medications for patient
- System MUST generate complete aftercare plan with milestones based on selected template

**Aftercare Template Structure** (Admin-Created):

- Admin creates milestone templates: Post-Op Phase, Recovery Phase, Growth Phase, Final Assessment
- Each milestone defines:
  - Duration (e.g., 7 days, 30 days, 90 days, 180 days, 12 months)
  - Required scan/photo set frequency (daily, every 5 days, weekly, bi-weekly, monthly)
  - Required questionnaires (pain assessment, sleep quality, compliance check, activity restrictions)
  - Questionnaire frequency (daily, weekly, bi-weekly, monthly)
  - Educational resources (videos, instruction guides, best practice documents)
  - Activity restrictions for this phase
- Template selection triggers automatic aftercare plan generation

**Provider Workflow**:

1. Provider marks treatment as "completed" in system
2. System prompts provider to select aftercare template
3. Provider selects template (e.g., "Standard FUE Aftercare - 12 months")
4. Provider adds custom instructions (specific to patient's procedure)
5. Provider specifies medications:
   - Medication name
   - Dosage
   - Frequency (e.g., 2x daily for 7 days)
   - Instructions (e.g., "Take with food")
6. System generates complete aftercare plan
7. Status changes to "Aftercare" and patient receives aftercare activation notification

---

#### Part B: Patient Aftercare Activities

**Head Scan Requirements** *(V1 photo set; true 3D in V2)*:

- Patients MUST upload head scan photo sets (V1) at milestone-defined intervals
- System MUST notify patients when scan is due
- System MUST provide scan guidance (same as initial scan during inquiry)
- System MUST track scan completion progress
- Scans used by aftercare specialists to monitor hair growth progress
- Missed scans MUST trigger reminder notifications

**Scan Frequency Examples**:

- Post-Op Phase (Days 1-7): Daily scan
- Early Recovery (Weeks 2-4): Every 5 days
- Mid Recovery (Months 2-3): Every 2 weeks
- Growth Phase (Months 4-6): Monthly
- Final Assessment (Months 6-12): Every 2 months

**Questionnaire Requirements**:

- Patients MUST complete questionnaires at milestone-defined intervals
- System MUST send notification when questionnaire is due
- Questionnaire types:
  - **Pain Assessment**: Visual scale (1-10) + description
  - **Sleep Quality Assessment**: Hours slept, quality rating, disruptions
  - **Compliance Assessment**: Following washing instructions, medication adherence, activity restrictions
  - **Activity Restrictions Check**: Confirming they're avoiding restricted activities
  - **Symptom Check**: Swelling, redness, bleeding, infection signs
- System MUST track questionnaire completion
- Missed questionnaires MUST trigger reminder notifications
- High pain levels or concerning symptoms MUST flag case as "urgent"

**Medication & Instructions**:

- Patients receive personalized medication schedule from provider
- System sends medication reminders based on provider-specified frequency
- Patients can view activity restrictions timeline for current milestone
- Patients can access milestone-specific resources:
  - Instructional videos (washing technique, sleeping position, etc.)
  - Best practice guides
  - FAQ documents
  - When to seek help guide
- Patients can mark instructions as "completed" or "viewed"

**Progress Tracking**:

- System calculates overall recovery progress percentage
- Based on: scans completed, questionnaires completed, milestone time elapsed
- Patients can see their progress in app dashboard
- System shows "next upcoming task" (e.g., "Scan due in 2 days")

---

#### Part C: Standalone Aftercare Service

**Business Model**:

- Hairline offers aftercare as **standalone service** (separate from treatment booking)
- Patients can purchase aftercare even if treatment was performed at external clinic (not through Hairline platform)
- Aftercare service provided by Hairline aftercare team
- Optional: Hairline may partner with providers to oversee aftercare cases

**Pricing Options**:

- Fixed amount (e.g., £500 for 6-month aftercare, £800 for 12-month aftercare)
- Monthly subscription (e.g., £80/month for 6 months, £70/month for 12 months)
- Patient selects preferred payment method at purchase
- Pricing varies by currency (multi-currency support)

**Standalone Aftercare Request Workflow**:

1. Patient navigates to "Request Aftercare Service" in app
2. Patient fills out form:
   - Treatment date (when procedure was performed)
   - Clinic name (where procedure was done)
   - Treatment type (FUE, FUT, DHI, etc.)
   - Graft count (if known)
   - Current concerns or issues
   - Upload recent photos (optional)
   - Upload surgeon notes (optional)
3. Patient selects aftercare duration (6 months, 12 months)
4. Patient selects payment option (fixed or monthly subscription)
5. Patient submits request
6. Request appears in admin dashboard as "Pending Assignment"

**Admin Assignment Workflow**:

- Admin reviews standalone aftercare request
- Admin assigns a provider to oversee the aftercare case
- System notifies assigned provider
- Provider reviews patient information and activates aftercare plan
- Provider selects appropriate aftercare template
- Patient receives activation notification with assigned provider information
- Aftercare begins (scans, questionnaires, milestone tracking)

**Requirements for Standalone Aftercare**:

- System MUST allow patients to request standalone aftercare service
- System MUST capture: treatment details, clinic information, current status
- System MUST support fixed pricing and monthly subscription models
- Admin MUST be able to view all standalone aftercare requests
- Admin MUST be able to assign provider to each standalone request
- Assigned provider MUST be able to activate aftercare plan
- System MUST track standalone aftercare cases separately from treatment-linked cases
- System MUST generate invoices for standalone aftercare purchases

---

#### Part D: Communication & Support

**Aftercare Team Access**:

- Patients MUST be able to chat with aftercare team (Hairline staff) 24/7
- Aftercare specialists can view:
  - Patient's complete aftercare plan
  - Milestone progress (current phase, completion percentage)
  - Scan history (head scan photo sets in V1) with timestamps
  - Questionnaire responses (pain levels, sleep quality, compliance data)
  - Medication schedule and adherence
  - Activity restrictions for current milestone
  - Provider's custom instructions
- Aftercare specialists can request additional information:
  - Request scan/photo set (if patient missed scheduled scan)
  - Request live video consultation (if visual assessment needed)
  - Request updated photos
- System MUST flag urgent cases for immediate attention

**Provider Access** (for treatment-linked aftercare):

- Providers can view their patients' aftercare progress
- Providers can see milestone completion, scan history, questionnaires
- Providers can communicate with aftercare team about specific cases
- Providers can adjust aftercare plan if needed (add milestones, modify instructions)

**Escalation Workflow**:

- Aftercare specialist identifies concerning symptom (high pain, infection signs, poor progress)
- Specialist escalates case to lead physician
- Lead physician reviews case and can:
  - Request video consultation with patient
  - Recommend patient visit local clinic for assessment
  - Adjust medication or instructions
  - Escalate to original provider (for treatment-linked cases)
- System logs all escalations for audit trail

---

#### Part E: Reporting & Analytics

**Aftercare Dashboard** (Admin View):

- Total active aftercare cases (treatment-linked + standalone)
- Average completion rate (% of scans and questionnaires completed on time)
- Flagged cases (urgent issues, overdue tasks)
- Provider performance (for assigned standalone cases)
- Patient satisfaction scores
- Most common complications or concerns

**Provider Dashboard** (Provider View):

- Active aftercare patients
- Milestone completion rates
- Overdue tasks (scans, questionnaires)
- Flagged cases requiring attention
- Patient compliance scores

---

#### Summary of Changes from Original

**Added Requirements**:

1. ✅ Provider selects aftercare template during treatment completion
2. ✅ Provider adds custom instructions and medications
3. ✅ Patients upload scan photo sets at milestone intervals (milestone-defined frequency)
4. ✅ Patients complete questionnaires at milestone intervals (pain, sleep, compliance)
5. ✅ Standalone aftercare service (patients can purchase separately)
6. ✅ Admin assigns provider for standalone aftercare requests
7. ✅ Milestone-based aftercare structure (admin creates templates)
8. ✅ Progress tracking based on scans + questionnaires + time
9. ✅ Educational resources per milestone
10. ✅ Escalation workflow for urgent cases

---

### FR-012: Messaging & Communication

**Priority**: P2 (Enhanced)  
**Module(s)**: P-06: Communication | PR-07: Communication & Messaging | A-10: Communication Monitoring & Support

**Requirements**:

- System MUST provide secure messaging between patients and providers (quote clarification, booking coordination, post-procedure questions)
- Messages MUST support text, images, video, and PDFs
- System MUST deliver real-time notifications for new messages
- System MUST maintain conversation history
- System MUST support read receipts
- System MUST log all communications for compliance and dispute resolution
- Admins MUST be able to monitor patient ↔ provider conversations with audit-ready exports
- Admins MUST be able to intervene ONLY in emergency situations with mandatory reason logging

**Communication Channels**:

- Patient ↔ Provider (in-app)
- Admin ↔ Patient/Provider (emergency-only intervention within a monitored conversation)

**Backlog (Future Enhancement)**:

- ⏸️ Patient ↔ Hairline Support Support Center / ticketing (general support and escalations; see FR-034)
- ⏸️ Patient ↔ Aftercare Team secure messaging (recovery support)
- ⏸️ Provider ↔ Admin operational messaging (billing/ops questions)

---

### FR-013: Reviews & Ratings

**Priority**: P2 (Enhanced)  
**Module(s)**: P-02: Quote Request & Management | PR-06: Profile & Settings Management | A-01: Patient Management & Oversight | S-03: Notification Service | S-05: Media Storage Service

**Requirements**:

- Patients MUST be able to submit review and rating after procedure completion (after 3+ months)
- System MUST enforce one review per completed procedure (uniqueness keyed to patient + completed procedure record); the edit flow operates on the existing review rather than creating additional reviews
- Patients MUST be able to edit their published review at any time
- Reviews MUST include: overall rating (1-5 stars), category ratings (facility, staff, results), written feedback
- System MUST verify that only patients who completed procedure can submit reviews
- Patients MUST be able to upload before/after photos with review (optional)
- Reviews MUST be published immediately upon valid patient submission, with post-publication admin flagging/removal available for spam, inappropriate content, or compliance concerns
- Providers MUST be able to respond to reviews
- System MUST calculate and display provider average rating
- System MUST display review count and distribution (5-star, 4-star, etc.)

**Review Categories**:

- Overall experience (1-5 stars)
- Facility cleanliness (1-5 stars)
- Staff professionalism (1-5 stars)
- Results satisfaction (1-5 stars)
- Value for money (1-5 stars)

---

### FR-014: Provider Analytics & Reporting

**Priority**: P2 (Enhanced)  
**Module(s)**: PR-05: Financial Management & Reporting | A-08: Analytics & Reporting

**Scope**: Delivers a 13-screen suite — 6 provider-facing screens (cockpit dashboard, performance & conversion, patient analytics, finance & payouts, pricing & benchmarks, export configuration) and 7 admin-facing screens (platform overview, provider performance & engagement, patient acquisition & funnel, geographic intelligence, treatment outcomes, financial health & cashflow, pricing intelligence).

**Provider Requirements**:

- Providers MUST have access to performance dashboard
- System MUST display: inquiry count, quote count, quote acceptance rate, revenue, patient count
- System MUST provide conversion funnel analytics using four stages: Inquiries → Quoted (first submitted parent quote) → Accepted (parent quote with an accepted subquote, FR-005) → Confirmed booking (FR-006)
- System MUST show accepted-price metrics (average accepted subquote price and price distribution); quote estimates are not presented as clinical results
- System MUST display review ratings (average overall rating, benchmark comparison, and per-treatment sub-scores)
- Providers MUST be able to export reports (PDF, CSV)
- System MUST provide comparative benchmarks against an anonymised peer median (active providers with ≥30 inquiries in a rolling 12-month window, minimum 5 providers), colour-coded by direction (Green at or better than median, Amber up to 10% worse, Red more than 10% worse)
- System MUST show provider commission as a percentage per completed payment or a flat rate once per completed procedure (FR-010 completion), matching FR-015

**Admin Requirements**:

- Admins MUST have access to a platform overview dashboard showing operational, performance, and financial summaries across all providers
- System MUST display provider TTFQ health distribution (Green/Amber/Red tiers) and provider engagement rate (active, at risk, dormant)
- System MUST provide a provider league table sortable by TTFQ, conversion rate, quote acceptance rate, rating, and quote response rate, with platform variance indicators
- System MUST display provider performance scatter (TTFQ vs. conversion rate) and a new-provider ramp chart for onboarding cohorts
- System MUST provide patient acquisition analytics: inquiry volume trend, platform funnel trend (same four stages: Inquiries → Quoted → Accepted → Confirmed booking), new vs. returning patient split, patient journey time distribution, inquiry seasonality heatmap, and affiliate acquisition breakdown
- System MUST provide geographic intelligence: patient demand by country, provider coverage by country, demand vs. supply gap table, conversion rate by patient country, and emerging patient origins
- System MUST provide treatment outcome analytics (operational and satisfaction-based only — no clinical outcome metrics): completion rate per treatment, cancellation/no-show rate per treatment, treatment volume trend, review sub-scores per treatment, aftercare activation rate per treatment, provider distribution by treatment specialisation
- System MUST provide financial health & cashflow analytics: platform GMV (gross), Net GMV (GMV minus refunds), and net revenue (platform commission earned in the period, accrual basis), commission earned trend with configurable target, refund and failed payment rates, platform-wide cash-at-risk aging, upcoming provider payout obligations, installment plan health, affiliate commission obligations, and revenue by currency
- System MUST provide pricing intelligence based on accepted subquote prices: average accepted price by treatment, accepted price range per treatment, accepted price by provider country, accepted selection count and share by accepted-price bracket (not an offered-price conversion rate), accepted price trend per treatment, and price outlier provider detection
- System MUST anonymise providers in cross-provider benchmark views (providers cannot identify each other); admin views MUST retain provider identity for operational support
- Admin-configurable parameters are owned by FR-026 Analytics Configuration (versioned): platform-wide TTFQ SLA target (default 120 minutes), engagement thresholds (At Risk 7 days, Dormant 30 days), price outlier threshold (30%), benchmark refresh frequency (Weekly), and target monthly commission reference line (unset by default; line hidden until set)
- System MUST send providers an in-app TTFQ SLA-breach alert (`inquiry.ttfq_sla_breached`, FR-020/FR-030) once per distributed inquiry/provider pair when that provider has not submitted a parent quote within the SLA target from the inquiry's distribution to the provider
- System MUST log all analytics access (user ID, timestamp, screen, filters) to the S-06 Audit Log Service as an immutable audit trail retained for 10 years, per the constitution

---

### FR-015: Provider Management (Admin-Initiated)

**Priority**: P1 (MVP)  
**Module(s)**: A-02: Provider Management & Onboarding

**Scope**: Admin creates and manages provider accounts. **NO self-service provider registration**.

**Requirements**:

- Admins MUST be able to create new provider accounts
- System MUST capture provider details: clinic name, location, credentials, licenses, certifications
- Admins MUST be able to upload provider documents (licenses, insurance, certifications) for record-keeping; document authenticity verification is handled manually outside the system and MUST NOT block account activation.
- Admins MUST be able to activate or deactivate provider accounts
- Admins MUST be able to suspend providers for policy violations
- System MUST set provider commission rate per provider using configurable Percentage or Flat Rate models; a Flat Rate MUST record its currency (from the FR-029 enabled currency list). The Commission Start Date is the FR-029 Effective Date of the rate; later edits set their own Effective Date, and payout cycles follow the provider's Payout Frequency (tier-based commission structures are out of scope for MVP and may be defined in a future FR).
- Admins MUST be able to mark providers as featured (flag and 10-provider cap are MVP); the patient-facing featured display is **P2 (Post-MVP)** and ships with FR-022 patient provider search
- System MUST track provider status (active, suspended, deactivated); there is no draft status. Suspension or deactivation automatically cancels the provider's `Accepted` and `Confirmed` bookings for admin support, keeps `In Progress` bookings open with `supportRequired` for an admin decision (move to `Aftercare` with aftercare-provider reassignment, or cancellation with a reason), and an admin reassigns the aftercare provider for bookings in `Aftercare`, while the inquiry stays open so that an admin can transfer the patient to another provider, and reactivation of a suspended provider restores nothing (see FR-015)
- Admins MUST be able to schedule a suspension or deactivation for a future Effective Date (at most one pending change per provider, shown as "Scheduled" and applied automatically on that date) and cancel it with a reason and password re-authentication before it takes effect

**Admin Workflow**:

1. Admin creates provider account (manual entry)
2. Admin uploads provider credentials (licenses, certifications, insurance) for record-keeping
3. Admin sets commission rate (Percentage, or Flat Rate with its currency), Commission Start Date, and Payout Frequency
4. Admin activates provider account (activation is not blocked by document status; documents are assumed to have been pre-verified offline)
5. Provider receives login credentials and can access platform

**Note**: Providers do NOT self-register. All provider accounts are created by admin team.

---

### FR-016: Admin Patient Management

**Priority**: P1 (MVP)  
**Module(s)**: A-01: Patient Management & Oversight

**Requirements**:

- Admins MUST be able to view all patient profiles and inquiries
- Admins MUST be able to search patients by name, email, phone, patient code (see FR-022 / FR-016 / Screen 1 for full search and filter criteria)
- Admins MUST be able to view patient treatment history and status
- Admins MUST be able to manually intervene in patient-provider disputes
- Admins MUST be able to reset patient passwords
- Admins MUST be able to suspend or deactivate patient accounts
- Admins SHOULD be able to access patient support case context via Support Center (see FR-034)
- System MUST log all admin actions on patient accounts for audit trail

---

### FR-017: Admin Billing & Financial Management

**Priority**: P1 (MVP)  
**Module(s)**: A-05: Billing & Financial Reconciliation | PR-05: Financial Management & Reporting

**Requirements**:

- Admins MUST be able to view all transactions (deposits, final payments, refunds)
- System MUST calculate provider payouts (total revenue - platform commission)
- Admins MUST be able to review and approve provider payout statements on scheduled basis (weekly, bi-weekly/2x a month, or monthly — per provider agreement)
- System MUST auto-process approved provider payouts on payout day
- System MUST generate invoices for providers
- Admins MUST be able to process affiliate payouts monthly using commission data from FR-018 / A-07
- System MUST track discount code usage and ROI (discount creation and management owned by FR-019 / A-06: Discount & Promotion Management)
- Admins MUST be able to view revenue reports by period, provider, country
- System MUST support multi-currency reporting with conversions

---

### FR-018: Affiliate Management

**Priority**: P2 (Enhanced)  
**Module(s)**: A-07: Affiliate Program Management

**Requirements**:

- Admins MUST be able to onboard affiliate partners
- System MUST generate unique affiliate codes for each partner
- System MUST track patient sign-ups and bookings via affiliate codes
- System MUST calculate affiliate commission (% of booking revenue or fixed amount), funded from Hairline's commission (not the provider payout)
- Affiliates MUST have access to dashboard showing referral count, revenue, commissions
- System MUST expose affiliate commission data and payout status to FR-017 / A-05 for monthly billing and payout execution
- System MUST generate affiliate performance reports

**Affiliate Features**:

- Unique referral link/code
- Dashboard with real-time stats
- Commission tracking and payout history
- Marketing materials (banners, templates)

---

### FR-019: Promotions & Discount Management

**Priority**: P2 (Enhanced)  
**Module(s)**: A-06: Discount & Promotion Management | PR-05: Financial Management & Reporting

**Requirements**:

- Admins MUST be able to create platform-wide discount codes
- Providers MUST be able to create provider-specific discounts
- System MUST support discount types: percentage, fixed amount, package upgrades
- Discounts MUST have start/end dates and usage limits
- Promotions MUST attach to individual option/date-price rows (subquotes) when a quote is sent, with their terms fixed at send; later promotion edits never change a sent quote
- Patients MAY enter a code on one named subquote before acceptance; the system validates it for that subquote only
- System MUST apply only one discount per subquote (priority: patient code > provider discount > Hairline-funded promotion > affiliate code) and attach at most one automatic promotion per quote
- If an automatic promotion's usage limit is already full when the quote is sent, the promotion MUST NOT attach and the send MUST proceed without it
- At acceptance, a reserved automatic promotion use MUST be consumed if the accepted row carries the promotion, and released with reason `not_applied` if it does not
- At acceptance, the promotion and discounted price MUST be frozen into the acceptance snapshot; no removal, replacement, or code entry is allowed afterwards, including at checkout or booking. The only exception is the FR-006 provider-fault transfer, handled through a new linked acceptance record
- An admin-authored replacement quote MUST NOT carry an automatic promotion, and no new promotion use is reserved for it; the admin sets the replacement price directly, and the original acceptance's promotion use is returned or kept under the normal rules
- For an automatically applied promotion, the system MUST reserve one use per sent quote that carries it; a re-send of a new quote version keeps the existing reservation, creates one only if the new version newly qualifies, and releases it if the new version no longer carries the promotion. The reservation MUST be released when the quote expires, is withdrawn, is not selected, or is cancelled before acceptance because the inquiry was cancelled or the provider's status changed, and MUST be consumed at acceptance, so the usage limit can never be exceeded
- If a booking that consumed an automatic promotion use ends in `Payment Window Expired` or is cancelled before the first payment, the use MUST return to the limit; an admin revive MUST take the use again only if the limit still has room, otherwise the revive is rejected
- For provider-selected promotions and patient codes, the system MUST reserve one use at acceptance, consume it at the first successful payment, and release it on `Payment Window Expired` or cancellation before the first payment
- System MUST track discount usage and total discount amount

**Discount Approval Workflow**:

- Platform discounts affecting "both fees" (provider + Hairline) MUST require provider approval
- System MUST send approval notifications to providers when new platform discount is created
- Providers can accept or decline participation in each discount
- Accepted discounts appear in provider's quote creation discount selection
- Provider-only discounts do not require approval (auto-active)
- Hairline-only discounts do not require provider approval and do not appear in the provider's quote discount selection
- For every discount type, including Hairline-only discounts, commission MUST be calculated on the accepted price after the promotion, so a discount reduces both the provider's payout and Hairline's commission and the provider bears most of it

**Discount Categories**:

- **Provider Discount**: Created by provider and reduces the total price; commission is calculated on the price after the promotion, as for every discount type, so it reduces both the provider's payout and Hairline's commission
- **Platform Discount (Both Fees)**: Created by admin, requires provider approval, affects total price; the discount cost is split by the program's Hairline Share % (0 to 100), with the provider funding the rest
- **Hairline Discount**: Created and governed by admin without provider approval; commission is still calculated on the price after the promotion, so both the provider's payout and Hairline's commission are reduced
- **Affiliate Discount**: Linked to affiliate code, typically Hairline-funded

---

### FR-020: Notifications & Alerts

**Priority**: P1 (MVP)  
**Module(s)**: S-03: Notification Service

**Requirements**:

- System MUST send email notifications for key events
- System MUST send push notifications to mobile app
- System MAY support SMS notifications for urgent events in future phases (optional, configurable, **not in MVP scope**)
- Patients and providers MUST be able to configure notification preferences
- System MUST support notification types: inquiry received, quote submitted, booking confirmed, payment received, message received, appointment reminder, aftercare milestone
- Quote, booking and treatment-change notifications MUST use the FR-030 event registry: `quote.submitted` (shows the "From" price), `quote.updated` (quote revised (new version), produced by FR-004 when a new version of a sent quote is re-sent), `quote.expiring_soon`, `quote.withdrawn` (mandatory), `quote.cancelled_inquiry` (mandatory), `quote.accepted` (one event with recipient-scoped outcomes for the selected subquote, its siblings, and other sent parent quotes, delivered to providers only; unsent drafts get no notice), `booking.scheduled` (shown as "Booking Accepted — Slot Held (Pending Payment)"; mandatory, patient only, and also sent at the acceptance of an admin-authored replacement quote), `booking.rescheduled` (mandatory, patient and provider, sent when an admin changes the appointment and showing the current appointment), `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement`, `aftercare.provider_reassigned` (mandatory, patient and the new aftercare provider, sent when an admin reassigns the aftercare provider) and `treatment.plan_changed`. `quote.declined` is Post-MVP; `provider.status_cancellation_patient` applies before acceptance only
- At acceptance the patient MUST receive only `booking.scheduled`, and the provider learns of it through `quote.accepted`; admins MUST NOT be alerted on each acceptance and receive only exception alerts (hold expiring soon while unpaid, `Payment Window Expired`, provider fault, `quote.withdrawn` after acceptance)
- System MUST throttle notifications to prevent spam
- System MUST track notification delivery status

**Implementation Note:**
For patient platform in FR-001 (MVP), notification preferences are limited to global Email/Push toggles; category preferences (e.g., Inquiry, Quote, Payment, Aftercare) are deferred to V2 per product management alignment.

**Provider Notification Preferences:**
Provider notification preferences are managed in FR-032 (Provider Dashboard Settings & Profile Management). Providers configure unified notification preferences including individual notification type toggles (quote, schedule, treatment start, aftercare, review, promotion/discount) and global channel preferences (email, push/in-app). Mandatory events such as `quote.cancelled_inquiry` have no provider toggle. SMS is a future enhancement and is **not** exposed as a configurable channel in MVP.

---

### FR-021: Multi-Language & Localization

**Priority**: P2 (Enhanced)  
**Module(s)**: P-01: Patient Account & Settings | PR-06: Profile & Settings Management | A-09: System Settings & Configuration | S-02: Payment Processing Service | S-03: Notification Service

**Requirements**:

- System MUST support multiple languages (English, Turkish initially, expandable)
- Patients and providers MUST be able to select preferred language
- System MUST translate UI elements, emails, and push notifications
- System MUST support RTL languages (future: Arabic)
- System MUST display dates and times in user's timezone
- System MUST support local currency display with conversion

---

### FR-022: Search & Filtering

**Priority**: P1 (MVP) for Provider Platform operational workflows and Admin Platform; P2 (Post-MVP) for patient provider search and FR-012 messaging search surfaces  
**Module(s)**: P-02, P-06, P-08 (Patient) | PR-01, PR-02, PR-03, PR-04, PR-05, PR-06, PR-07 (Provider) | A-01, A-02, A-03, A-05, A-06, A-07, A-09, A-10 (Admin)

**Requirements**:

- System MUST provide search and filter functionality across all three tenants (Patient, Provider, Admin) — see FR-022 for the complete screen-by-screen criteria
- For all search and filter field definitions, filter option lists, control behavior states, and screen-level specifications, refer to **FR-022: Search & Filtering** (`local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`) — FR-022 is the single source of truth
- System MUST support case-insensitive partial matching, debounced search inputs, cumulative AND-logic filtering, and result count display across all search-enabled screens
- System MUST provide autocomplete for location searches (patient provider discovery, P2)
- **Maintenance**: Whenever search fields or filter criteria change in any module FR, the FR-022 Master Reference Table must be updated to reflect those changes

---

### FR-023: Data Retention & Compliance

**Priority**: P1 (MVP)  
**Module(s)**: A-09: System Settings & Configuration (Cross-Cutting Concern)

**Requirements**:

- System MUST retain patient medical records for minimum 7 years (healthcare compliance)
- System MUST retain financial transaction records for minimum 7 years (tax/audit compliance)
- System MUST support soft-deletes only (no hard deletion of critical data)
- System MUST anonymize patient data in analytics and reports
- System MUST provide data export functionality for GDPR compliance
- System MUST allow patients to request data deletion (GDPR right to be forgotten)
- System MUST maintain audit logs for all data access and modifications

---

### FR-024: Treatment & Package Management

**Priority**: P1 (MVP)  
**Module(s)**: A-09: System Settings & Configuration | PR-06: Profile & Settings Management

---

#### Part A: Treatments (Admin-Created Foundation)

**Requirements**:

- **Treatment Creation Authority**: ONLY admin can create treatments
- Treatments are the **foundation** that all providers select from (ensures consistency)
- Admin creates treatments with: name, description, type (FUE, FUT, DHI), video, images, technique details
- Providers can ONLY select from pre-created treatment list (cannot create custom treatments)
- Providers may record a reference **price** for each treatment in their clinic, in the system quote currency; this price is a non-binding reference only, the binding price is the offered price set on each quote, and treatments carry no currency of their own
- Treatment versions are immutable once saved; every edit creates a new version, and quotes keep the version they copied
- All providers see the **same treatment list** (FUE, FUT, DHI, etc.)

**Examples of Treatments**:

- FUE (Follicular Unit Extraction)
- FUT (Follicular Unit Transplantation)
- DHI (Direct Hair Implantation)
- Sapphire FUE
- Robotic Hair Transplant

---

#### Part B: Packages (Provider-Created Quote Option Templates)

**Requirements**:

- **Package Creation Authority**: Each provider creates their own packages
- A package is a **reusable, versioned template for one quote option**: it holds the included services and their prices, flight, hotel, transport, and other travel services, a standard price, and the day-by-day relative treatment plan. Date ranges, additional notes, and documents are never packaged
- Packages carry **no currency**; all library prices use the system quote currency
- Each provider has **their own package library** (can differ between providers)
- Packages are NOT part of treatment - the treatment is selected separately on the parent quote
- Every library edit creates a new immutable package version; earlier versions stay read-only, and quotes keep the version they copied
- Inline edits during quote creation change only that quote option's copy; they are never written back to the library and never create a package version
- Each package selected in FR-004 seeds exactly one quote option (at most five per parent quote); package prices are never summed, and the standard price prefills each date-range price row of that option
- A quote option records the source package ID, the source package version, and whether it was customised inline; patient-visible package fields are read from that copy or exact version, never from the latest library version
- Packages are deactivated or archived, never hard-deleted

**Examples of Packages**:

- Hotel packages (3-star, 4-star, 5-star)
- Transport packages (airport pickup, city transfers)
- Flight assistance packages
- Medication packages (post-op medications to take home)
- PRP therapy package
- Extended consultation packages

---

#### Quote Structure

```sh
Parent Quote = Treatment version + shared grafts, plan visuals, clinicians, notes,
               documents, quote currency, expiry, version, audit
  Quote Option (1 to 5) = quote-local copy of one package version
                          (services, travel services, relative-day plan)
    Option/date-price row = one applicable date range + offered price + appointment
Subquote = one Quote Option x one option/date-price row (the patient accepts exactly one)
```

**Example Quote** (quote currency GBP, captured from system configuration at first send):

```sh
Treatment: FUE, 3000 grafts (shared by every option)

Option A - "Comfort" package (v3): 4-star hotel 5 nights, airport transfer
   Date range 1 (10-20 Mar)      £3,000
   Date range 2 (5-15 Apr)       £2,850
Option B - "Premium" package (v2): 5-star hotel 5 nights, transfers, PRP session
   Date range 1 (10-20 Mar)      £3,600

Subquotes offered: A x range 1, A x range 2, B x range 1 (three choices)
Patient accepts exactly one, for example A x range 2 at £2,850.
Option prices are never added together.
```

---

#### Rationale

**Why Separate Treatments and Packages?**

1. **Consistency**: All providers offer same treatments (FUE, FUT, DHI) with standardized info and videos
2. **Flexibility**: Providers differentiate through their own package offerings
3. **Scalability**: When platform offers direct travel booking, provider packages can be disabled without affecting treatments
4. **Clarity**: Patients understand the core procedure vs the package options offered around it
5. **Future-Proof**: Easy transition from provider-managed to platform-managed services

---

### FR-025: Medical Questionnaire Management

**Priority**: P1 (MVP)  
**Module(s)**: A-09: System Settings & Configuration

**Requirements**:

- **Centralized Question Management**: Admin MUST be able to add, edit, remove, and reorder medical questionnaire questions
- **Question Content**: Each question MUST have: question text, question type (system-defined: Yes/No, Visual Scale 1–10, Numeric Scale 1–10, Multi-select, Free Text), and type-specific content. **MVP**: Inquiry-context sets MUST be Yes/No only. **Future (V2+)**: additional question types may be allowed once inquiry response schema supports typed answers (then enforce via publish-time warning and validation)
- **Severity Flagging**: Each question MUST have a severity flag (Critical/Standard/No Alert)
- **Alert System**: When patient answers "Yes" to Critical questions → inquiry flagged with red alerts
- **Alert System**: When patient answers "Yes" to Standard questions → inquiry flagged with yellow/amber alerts  
- **Alert System**: When patient answers "No" to all questions → inquiry flagged with green (no alerts)
- **Set-Level Categorisation**: Admin MUST be able to organise questionnaire sets into categories (Allergies, Cardiovascular, etc.) for catalog filtering — categories apply at the set level, not individual question level (per FR-025 PRD)
- **Version Control**: System MUST track questionnaire changes with timestamps and admin identification
- **Question Validation**: System MUST validate question completeness before activation
- **Questionnaire Preview**: Admin MUST be able to preview questionnaire as patients will see it
- **Bulk Operations** *(V2)*: Admin SHOULD be able to import/export questionnaire templates — deferred to V2; not requested by client in transcriptions
- **Question Templates** *(V2)*: System SHOULD provide pre-built question templates for common medical conditions — deferred to V2; not requested by client in transcriptions

**Question Examples**:

- **Critical Questions**: HIV/AIDS, Hepatitis B/C, Blood disorders, Heart conditions
- **Standard Questions**: Allergies, Medications, Previous surgeries, Chronic conditions
- **No Alert Questions**: General health status, Lifestyle factors

**Admin Interface Requirements**:

- Question list with drag-and-drop reordering
- Question editor with rich text support
- Severity flag assignment (dropdown)
- Category management
- Preview mode
- Change history and audit trail

---

### FR-026: App Settings & Security Policies

**Priority**: P1 (MVP Cross-Cutting)  
**Module(s)**: A-09: System Settings & Configuration

**Goal**: Provide a centralized, audited, and versioned configuration surface for application settings and security policies that affect multiple modules and tenants.

**Requirements**:

- Settings Management UI (Admin)
  - Admins MUST be able to view, create, update, and version settings within clearly defined groups:
    - Authentication & Security
    - App Data (Lists)
    - Notifications
  - All changes MUST require a reason and be fully audited (who/when/old value/new value)

- Authentication & Security (affects P-01 and others)
  - Password policy is FIXED in codebase (not editable in Admin): min length ≥ 12 and must include upper, lower, digit, special from !@#$%^&(),.?":{}|<>
  - Authentication throttling MUST be configurable: max login attempts before lockout and lockout duration
  - OTP configuration: length is FIXED at 6 in codebase; expiry (default 15 min) and resend cooldown/rate limits MUST be configurable
  - System MUST support IP/device-level rate limiting for anti–brute force protections

- App Data (Centrally Managed Lists)
  - Discovery question options ("How did you find out about us?") MUST be centrally managed
  - Country list and country calling codes MUST be centrally managed
  - Inquiry treatment-area options with display assets and the minimum inquiry lead time MUST be centrally managed for FR-003
  - Changes MUST propagate to dependent UIs within 1 minute

- Quote Configuration (versioned; consumed by FR-004, FR-005, and FR-006)
  - Quote expiry window MUST be 24 to 336 hours (default 48) and slot-hold duration 24 to 168 hours (default 48)
  - Quote-expiring-soon and hold-expiring-soon lead times (default 12 hours each) MUST each be at least 1 hour and at most half of the window they warn about
  - Quote currency is shown read-only and is the FR-029 Default Currency; each Default Currency change creates a new quote-configuration version, so the version recorded on a quote identifies both the hours and the currency used

- Notifications
  - Templates for OTP delivery (verification/reset) MUST be editable with variables and preview
  - Changes MUST NOT affect delivery to users already in a flow

**Data Security & Governance**:

- All setting changes MUST be versioned and auditable; hard deletes are PROHIBITED (archive only)
- System MUST support forward-only changes (no automated rollback); admins can manually recreate previous configurations using version history as reference
  - **Rationale**: Security policies should never be automatically rolled back as this could reintroduce vulnerabilities. Forward-only changes ensure security improvements are never accidentally regressed. Admins retain full audit trail and can manually restore previous values if needed.
- Access MUST be restricted to authorized admin roles; sensitive values must be masked in UI and logs

**Impacted Modules**:

- P-01: Auth & Profile (password policy, OTP, throttling, countries/calling codes, discovery options)
- PR-06: Provider Settings (indirect consumption of lists)
- S-03: Notification Service (OTP templates)

**Success Criteria**:

- 100% of changes to settings captured with who/when/what-before/after
- Setting changes propagate to dependent services within ≤ 1 minute
- Zero production incidents linked to settings drift after enabling versioning and rollback
- Security scanning shows no exposure of sensitive setting values in UI or logs

---

### FR-027: Legal Content Management

**Priority**: P1 (MVP Cross-Cutting)
**Module(s)**: A-09: System Settings & Configuration

**Goal**: Provide centralized management of legal content (Terms & Conditions, Privacy Policy, Consent forms) with versioning, preview, and audit trail capabilities.

**Requirements**:

- Content Management: Admins MUST be able to create, edit, and publish legal content documents
- Version Control: System MUST maintain version history with timestamps and change tracking
- Preview & Publishing: Admins MUST be able to preview content before publishing to users
- Consent Tracking: System MUST track which users have accepted which versions of legal documents
- Audit Trail: All legal content changes MUST be logged with who/when/what changed

**Impacted Modules**:

- P-01: Auth & Profile (T&C acceptance during registration)
- PR-01: Auth & Team Management (provider T&C acceptance)

**Note**: Detailed requirements to be documented in dedicated FR-027 PRD.

---

### FR-028: Regional Configuration & Pricing

**Priority**: P2 (Enhanced)
**Module(s)**: A-09: System Settings & Configuration

**Goal**: Enable admins to configure location presentation rules, regional groupings, and starting price configurations for different countries and currencies.

**Requirements**:

- Location Grouping: Admins MUST be able to group countries into regions (e.g., "Europe", "Eastern Europe")
- Location Ordering: Admins MUST be able to define provider display order per region (e.g., Turkey first for Europe)
- Starting Prices: Admins MUST be able to set starting prices per location and currency
- Fallback Pricing: System MUST support fallback pricing for locations without preset configurations
- Regional Display: Patient app MUST display providers based on configured regional rules

**Impacted Modules**:

- P-02: Quote Request & Management (location selection, pricing display)
- PR-02: Inquiry & Quote Management (regional filtering)

**Dependencies**:

- FR-026 provides country list consumed by this module

**Note**: Detailed requirements to be documented in dedicated FR-028 PRD.

---

### FR-029: Payment System Configuration

**Priority**: P1 (MVP)
**Module(s)**: A-09: System Settings & Configuration

**Goal**: Provide comprehensive payment infrastructure configuration including Stripe account management, currency conversion settings, deposit rate configuration, and split payment rules.

**Requirements**:

- Stripe Account Management: Admins MUST be able to manage multiple Stripe accounts
- Account-to-Region Mapping: Admins MUST be able to assign Stripe accounts to countries/regions
- Currency Support: System MUST support multiple currencies per Stripe account
- Conversion Rate Configuration: Admins MUST be able to configure currency conversion rate sources and markup percentages
- Currency Disable Guard: System MUST block disabling a currency while any non-terminal sent quote, unpaid accepted booking, or open booking or instalment plan uses it, and MUST show the admin the count of records still using it
- **Deposit Rate Configuration**: Admins MUST be able to configure deposit percentage (default range: 20-30% of the booking total, which is the accepted price after promotion and the same base used for instalments and commission). This MUST be configurable per provider or globally. Changes apply to new bookings only (existing bookings retain original deposit rate)
- Split Payment Rules: Admins MUST be able to configure installment plan options (2-9 installments) and cutoff dates (e.g., 30 days before procedure)
- Rate Protection: System MUST handle rapid currency fluctuations and protect against unfavorable rates

**Impacted Modules**:

- P-03: Booking & Payment (payment processing, deposit calculation, installment calculations)
- S-02: Payment Processing Service (Stripe integration, currency conversion)
- FR-006: Booking & Scheduling (deposit rate used for booking confirmation)
- FR-007: Payment Processing (extends with configuration capabilities)
- FR-007B: Split Payment / Installment Plans (extends with configuration capabilities)

**Note**: Detailed requirements to be documented in dedicated FR-029 PRD.

---

### FR-030: Notification Rules & Configuration

**Priority**: P2 (Enhanced)
**Module(s)**: A-09: System Settings & Configuration | S-03: Notification Service

**Goal**: Enable admins to configure event-to-notification mappings, channel preferences (email/SMS/push), and recipient rules for platform-wide notification system.

**Requirements**:

- Event Mapping: Admins MUST be able to configure which events trigger notifications (quote received, treatment start, aftercare review)
- Channel Configuration: Admins MUST be able to define notification channels per event type (email, SMS, push)
- Recipient Preferences: Admins MUST be able to set notification preferences per recipient type (patient, provider, admin)
- Template Management: System MUST support notification template creation and editing (extends FR-026 OTP templates to general notifications)
- Testing: Admins MUST be able to test notification rules before activation

**Impacted Modules**:

- S-03: Notification Service (notification delivery)
- FR-020: Notifications & Alerts (extends with configuration capabilities)

**Dependencies**:

- FR-026 provides OTP template foundation extended by this module

**Note**: Detailed requirements to be documented in dedicated FR-030 PRD.

---

### FR-031: Admin Access Control & Permissions

> The custom provider role creation and cloning extension below is proposed in [CR-FR031-20260929-01](functional-requirements/fr031-admin-access-control/change-request-2026-09-29-global-custom-provider-roles.md); implementation reconciliation is pending.

**Priority**: P1 (MVP)
**Module(s)**: A-09: System Settings & Configuration

**Goal**: Provide role-based access control system for admin platform with granular permission management, team member administration, and audit trail.

**Requirements**:

- Role Management: Admins MUST be able to create and manage admin roles (aftercare staff, billing staff, support staff, super admin)
- Provider Role Management: Super Admins MUST be able to create and clone global custom provider roles from non-Owner base types while preserving protected provider roles and Owner-only capabilities
- Permission Matrix: Admins MUST be able to assign granular permissions per role (feature access control)
- Team Member Management: Admins MUST be able to invite, manage, and remove admin team members
- Role Assignment: Admins MUST be able to assign roles to team members with effective date tracking
- Audit Trail: System MUST log all permission changes with who/when/what changed
- Access Validation: System MUST enforce permission checks on all admin actions and API calls

**Impacted Modules**:

- A-01 through A-10: All Admin modules (permission enforcement)
- All admin-facing features require access control integration

**Note**: Detailed requirements to be documented in dedicated FR-031 PRD.

---

### FR-032: Provider Dashboard Settings & Profile Management

**Priority**: P1 (MVP)  
**Module(s)**: PR-06: Profile & Settings Management

**Requirements**:

**Profile Management**:

- Providers MUST be able to upload and update clinic logo/profile picture
- Providers MUST be able to select languages from system language options (matches FR-021)
- Providers MUST be able to add, edit, and delete awards with direct image upload (name, description, year, award image)
- Providers MUST be able to update basic clinic information (name, description, contact details)

**Account Settings**:

- Providers MUST be able to update phone number with worldwide country code selection (consumes FR-026 country list)
- Providers MUST be able to select timezone from multiple timezone options
- Providers MUST be able to change password
- Providers MUST be able to request account deletion (soft-delete, admin approval required)

**Notification Preferences** (Unified Settings):

- Providers MUST be able to configure notification preferences in a single unified settings location
- Providers MUST be able to toggle individual notification types: quote notifications, schedule notifications, treatment start notifications, aftercare notifications, review notifications, promotion/discount notifications
- Providers MUST be able to configure global channel preferences: email and push/in-app notifications (SMS channel is reserved for future enhancement and is not available in MVP)
- Notification preferences MUST be profile-specific (applies to provider organization, not individual team members)
- System MUST respect provider notification preferences when sending notifications (integrates with FR-020)

**Billing Settings** (Separate Section):

- Providers MUST have access to a dedicated billing settings section
- Main account holder (Owner) MUST be able to manage bank account details for payouts
- System MUST support bank account information: account holder name, bank name, account number, routing/SWIFT code, IBAN (if applicable)
- Billing settings MUST be accessible only to Owners (per FR-009 role permissions)

**Help Centre**:

- Providers MUST have access to Help Centre page with categories: FAQ's, Tutorial Guides, Contact Support, Troubleshooting Tips, Resource Library, Community Forum, Feedback & Suggestions, Service Status, Policy Information, Video Tutorials
- Help Centre content MUST be admin-managed (see FR-033)
- Providers view read-only content; content updates managed by admins

**Integration Points**:

- FR-020: Notification preferences integration
- FR-021: Language options (profile languages match system languages)
- FR-026: Country codes and timezone lists
- FR-009: Role-based access control (billing settings Owner-only)
- FR-017: Billing integration (bank account details for payouts)

**Note**: Detailed requirements to be documented in dedicated FR-032 PRD.

---

### FR-033: Help Centre Content Management

**Priority**: P1 (MVP)
**Module(s)**: A-09: System Settings & Configuration | PR-06: Profile & Settings Management | P-08: Help Center & Support Access

**Requirements**:

- Admins MUST be able to create, edit, and manage Help Centre content for both provider and patient platforms
- System MUST support separate Help Centre content repositories for provider and patient audiences
- System MUST support Help Centre categories: FAQ's, Tutorial Guides, Contact Support, Troubleshooting Tips, Resource Library, Community Forum, Feedback & Suggestions, Service Status, Policy Information, Video Tutorials
- Admins MUST be able to organize FAQ content by topics with expandable/collapsible sections
- Admins MUST be able to upload tutorial guides, videos, and resource documents
- System MUST support content versioning and audit trail for Help Centre updates
- Providers and patients view Help Centre content as read-only (content managed exclusively by admins)
- System MUST support multi-language Help Centre content (future enhancement)

**Note**: Detailed requirements to be documented in dedicated FR-033 PRD.

---

### FR-034: Patient Support Center & Ticketing

**Priority**: P2 (Enhanced)  
**Module(s)**: A-10: Communication Monitoring & Support | A-01: Patient Management & Oversight

**Requirements**:

- System MUST provide a formal Support Center for patient support case intake, tracking, and resolution
- Staff MUST be able to create support cases, categorize them, set priority, and assign ownership
- System MUST support a case lifecycle: Open → In Progress → Resolved → Closed, with immutable history
- Support cases MUST be linkable to patient records (HPID/email/phone) and deep-link to A-01 for interventions
- System MUST maintain an auditable case timeline (messages, notes, attachments) for disputes/compliance
- System MUST support patient notifications on meaningful updates (status changes/replies) via S-03 when enabled

**Note**: Detailed requirements documented in dedicated FR-034 PRD at `functional-requirements/fr034-support-center-ticketing/prd.md`. FR-034 has been extended to support patient submissions (via FR-035), provider submissions (via FR-032 Screen 5.5/5.6), and manual admin entries in a unified support ticketing system with consistent status workflow (Open → In Progress → Resolved → Closed). The system supports full two-way threaded communication between patients/providers and admin staff within support cases, with message history tracked in Communication Thread and comprehensive Timeline.

---

### FR-035: Patient Help Center & Support Submission

**Priority**: P2 (Enhanced)
**Module(s)**: P-08: Help Center & Support Access | Integrates with FR-033 (Content Management) and FR-034 (Ticketing System)

**Goal**: Enable patients to access help center content (FAQs, articles, resources, videos) and submit support requests and feedback directly from the patient mobile app.

**Requirements**:

**Patient Help Center Access**:

- Patients MUST be able to access Help Center from patient mobile app navigation
- System MUST display patient-specific Help Center content managed by admins in FR-033 (FAQs, Articles, Resources, Videos)
- Patients MUST be able to browse Help Center content by category and search for specific topics
- Content separation MUST be enforced: Patients see ONLY patient content, never provider content

**Patient Support Submission**:

- Patients MUST be able to submit support requests via "Contact Support" form with category, priority, description, and optional attachments
- Patients MUST be able to submit feedback and feature requests via "Submit Feedback" form
- System MUST automatically create support cases in FR-034 with Ticket Source = "Patient App" and Submitter Type = "Patient"
- Patients MUST be able to view status of their submitted tickets with unified status workflow (Open → In Progress → Resolved → Closed)
- Patients MUST receive email notifications (via S-03) when admin responds or updates ticket status
- For feedback submissions, patients MUST be able to view Feedback Resolution status (Implemented, Planned, Declined, Under Review)

**Two-Way Communication with Admin**:

- Patients MUST be able to view complete communication thread for their submitted cases, including all messages from admin and patient
- Patients MUST be able to reply to admin messages within the case, enabling two-way threaded conversation
- System MUST display full case timeline showing status changes, feedback resolution updates (if applicable), and message history
- When patient replies to case, system MUST notify assigned admin (or all support staff if unassigned) via email notification
- Patient replies MUST appear in admin's case detail view (FR-034 Screen 3) in Communication Thread and Timeline
- Two-way communication MUST maintain full conversation context and history for each case

**Integration Points**:

- FR-033: Consumes patient-specific Help Center content (read-only)
- FR-034: Creates support cases for patient submissions, provides two-way communication capability via Communication Thread, and displays ticket status/responses/conversation thread to patients
- Communication architecture: Patient messages ↔ FR-034 Communication Thread & Timeline ↔ Admin responses (synchronized via FR-034 case management system)

**Note**: This FR is planned for future implementation to complete the multi-tenant support system architecture. Patient submissions will integrate with the unified FR-034 ticketing system with full two-way communication capability mirroring the provider support experience (FR-032 Screen 5.5/5.6). Detailed requirements to be documented in dedicated FR-035 PRD when implementation begins.

---

### FR-036: Admin Profile & Settings Management

**Priority**: P1 (MVP)
**Module(s)**: A-09: System Settings & Configuration

**Goal**: Enable admin users to manage their own profile information, account settings, and personal preferences independently of team management and RBAC configuration.

**Requirements**:

**Profile Management**:

- Admin users MUST be able to update their own profile information (first name, last name, profile picture)
- Admin users MUST be able to view their assigned role and permissions (read-only)
- Admin users MUST be able to update their contact information (email, phone number)
- Profile picture uploads MUST support common image formats (JPEG, PNG) with size validation

**Account Settings**:

- Admin users MUST be able to change their own password with current password verification
- Admin users MUST be able to configure timezone preferences for date/time display
- Admin users MUST be able to configure language preferences (when i18n is implemented)
- Password changes MUST require current password verification and meet security policy (FR-026)

**Notification Preferences**:

- Admin users MUST be able to configure personal notification preferences
- Admin users MUST be able to toggle notification types (email, in-app) for different event categories
- Notification preferences MUST be user-specific (not role-based)
- System MUST respect admin notification preferences when sending notifications (integrates with FR-020)

**Activity & Audit**:

- Admin users MUST be able to view their own activity log (login history, actions performed)
- Activity log MUST display: timestamp, action type, affected entities, IP address
- Activity log MUST be read-only (no deletion or modification)
- Activity log MUST be filterable by date range and action type (see FR-022 / FR-031 / Screen 5 for full filter criteria)

**Integration Points**:

- FR-031: Consumes role and permission data (read-only display)
- FR-020: Notification preferences integration
- FR-026: Password policy enforcement, timezone/language options
- FR-021: Language preferences (when i18n is implemented)

**Note**: This FR is planned for future implementation. Detailed requirements to be documented in dedicated FR-035 PRD when implementation begins. This mirrors the pattern of FR-001 (Patient Profile) and FR-032 (Provider Profile) to ensure consistency across all three platforms.

---

### FR-037: Monitor Your Hair Loss

**Priority**: P1 (Next Phase)
**Module(s)**: P-05: Aftercare & Progress Monitoring, P-07: 3D Scan Capture & Viewing, PR-07: Communication & Messaging, A-01: Patient Management & Oversight, A-09: System Settings & Configuration, S-03: Notification Service, S-05: Media Storage Service

**Goal**: Enable patients to monitor hair loss longitudinally through self-monitoring or limited provider-advice mode, then complete/export the case or convert it into a treatment inquiry without re-entering existing information.

**Requirements**:

- Patient MUST be limited to one active hair-loss monitoring case; this limit applies independently from transplant-progress monitoring.
- Patient MUST choose self-monitoring or provider-advice mode at creation, and MUST NOT change mode while the case remains active.
- Patient MUST be able to submit optional dated logs containing severity from 1 to 10, notes, photos, and standardized V1 head scan photo sets without a required logging frequency.
- Advice-mode cases MUST wait for Admin provider assignment while patient logging remains available.
- Advice mode MUST require the active FR-025 Inquiry medical questionnaire before the assigned provider can access the case.
- Assigned provider MUST be able to post one limited advice paragraph per Admin-configurable weekly or bi-weekly window. The cadence is a single global setting captured on each case at creation; a change applies only to cases created afterwards.
- Each advice window MUST open on its calculated start date and remain actionable with no ordinary deadline until its single advice is submitted. When a successor window opens first, only the older unsubmitted window MUST expire, and the successor MUST become the sole actionable window.
- Submitted advice MUST be a separate provider-authored case-calendar record, MUST NOT attach to or modify any patient log, and MUST be editable with immutable version history plus a visible edited cue and latest-edit timestamp.
- Before assignment or reassignment, Admin MUST be able to generate and revoke an expiring, read-only, audited case-preview link for a candidate provider, selecting its expiry at share time. Preview access MUST NOT create an assignment or ongoing case access, and FR-037 MUST NOT add an embedded chat surface for this exchange.
- Provider-facing FR-037 screens MUST show an anonymized patient identifier for the entire case lifetime.
- Assigned provider MUST be able to withdraw with a reason; withdrawal MUST remove provider access and return the case to Admin as a clearly identified reassignment case while patient logging continues.
- Patient MUST be able to complete the case and export a date-to-date PDF containing all logs, scan photos, logged-day count, and severity summary/trend.
- Patient MUST be able to convert an active monitoring case into a distinct FR-003 inquiry. Conversion MUST pre-fill compatible information, allow every copied field to be edited, select the latest scan by default while allowing another scan or retake, require medical-answer review/reconfirmation, and attach the monitoring-summary PDF.
- Previous monitoring history MUST NOT be attached to a newly created monitoring case. Full history linkage applies only when that source monitoring case converts into an FR-003 inquiry.
- If an assigned advice provider exists at conversion, that provider MUST be the only initial provider selected to quote. If no provider is assigned, FR-003 normal distribution MUST apply.
- If that exclusive provider explicitly declines before creating a quote, FR-003 MUST audit the decline reason, remove the exclusive-provider restriction, and execute normal distribution exactly once. Inquiry or quote expiry MUST continue to follow FR-003/FR-004's existing configured rules and MUST NOT invoke this decline fallback.
- Admin MUST be able to edit all monitoring information with immutable actor, reason, timestamp, before-value, and after-value history.

**Integration Points**:

- FR-002: V1 standardized head scan photo-set capture and quality validation.
- FR-003: Service entry point, inquiry conversion, active-inquiry gate, and provider distribution.
- FR-004: Quote creation after conversion.
- FR-020: Assignment, advice, withdrawal, completion, export, and conversion notifications.
- FR-025: Advice-mode medical questionnaire and conversion reconfirmation.

**Detailed PRD**: `functional-requirements/fr037-monitor-hair-loss/prd.md`

---

### FR-038: Monitor Your Transplant Progress

**Priority**: P1 (Next Phase)
**Module(s)**: P-05: Aftercare & Progress Monitoring, P-07: 3D Scan Capture & Viewing, A-01: Patient Management & Oversight

**Goal**: Provide a provider-free, self-paced utility for tracking transplant progress outside a managed aftercare package, with optional conversion into FR-011 standalone aftercare.

**Requirements**:

- Patient MUST be limited to one active transplant-progress monitoring case; this limit applies independently from hair-loss monitoring.
- FR-038 MUST be self-service only and MUST NOT include provider advice, provider assignment, provider access, required cadence, milestones, overdue states, or compliance obligations.
- Intake MUST capture FR-011-compatible external-treatment details, including treatment date, treatment type, treating clinic, optional documentation, current concerns, and optional initial scan/photos.
- Patient MUST be able to submit optional dated logs containing severity from 1 to 10, notes, photos, and standardized V1 head scan photo sets.
- Patient MUST be able to complete the case and export a date-to-date PDF containing treatment summary, all logs, scan photos, logged-day count, and severity summary/trend.
- Patient MUST be able to convert an active monitoring case into a distinct FR-011 standalone-aftercare request. Conversion MUST pre-fill compatible information, allow every copied field to be edited, select the latest scan by default while allowing another scan or retake, and attach the monitoring-summary PDF.
- Conversion MUST complete the monitoring case only after successful standalone-request creation. A failed or abandoned conversion MUST leave monitoring active.
- Previous monitoring history MUST NOT be attached to a newly created monitoring case. Conversion provenance MUST link only the source monitoring case and destination FR-011 request.
- After successful handoff, FR-011 MUST exclusively own package selection, payment, Admin assignment, provider activation, milestones, and provider-managed aftercare.
- Admin MUST be able to view and edit all monitoring information with immutable actor, reason, timestamp, before-value, and after-value history, but MUST NOT assign a provider directly to FR-038.

**Integration Points**:

- FR-002: V1 standardized head scan photo-set capture and quality validation.
- FR-003: Service Selection entry point.
- FR-007: Payment after handoff into FR-011 checkout only.
- FR-011: Standalone-aftercare request, package selection, payment, assignment, activation, and managed aftercare.
- FR-020: Completion, export-ready, and conversion notifications.

**Detailed PRD**: `functional-requirements/fr038-monitor-transplant-progress/prd.md`

---

## Non-Functional Requirements

### NFR-001: Performance

### Error Handling Standard

All Hairline engines and platform APIs MUST return structured errors complying with the shared Hairline error schema. Error payloads MUST include at least: `error_code`, `message`, `remediation` (if available), `source` (system/context), and `severity`. Reference: Error handling requirements in technical specification.

- API response time MUST be < 500ms for p95 requests
- API response time MUST be < 1000ms for p99 requests
- Mobile app load time MUST be < 3 seconds
- System MUST support 10,000+ concurrent patients
- System MUST support 1,000+ concurrent providers
- Scan media processing MUST complete within 60 seconds

### NFR-002: Scalability

- System architecture MUST support horizontal scaling
- Database MUST support read replicas for query performance
- System MUST use CDN for static asset delivery
- System MUST implement caching for frequently accessed data
- Background jobs MUST be processed asynchronously via job queue

### NFR-003: Security

- All data in transit MUST be encrypted using TLS 1.3
- All sensitive data at rest MUST be encrypted using AES-256
- System MUST implement role-based access control (RBAC)
- System MUST log all security events (login attempts, permission changes, data access)
- System MUST support multi-factor authentication for providers and admins
- System MUST comply with GDPR and equivalent healthcare data protection regulations
- System MUST pass quarterly penetration testing

### NFR-004: Availability

- System uptime MUST be 99.5%+ (excluding scheduled maintenance)
- System MUST have automated backups every 6 hours with 30-day retention
- System MUST have disaster recovery plan with RTO < 4 hours, RPO < 1 hour
- System MUST have automated health checks and alerting

### NFR-005: Accessibility

- Web applications MUST be WCAG 2.1 Level AA compliant
- Mobile app MUST support screen readers and accessibility features
- System MUST support keyboard navigation
- System MUST provide alternative text for all images

### NFR-006: Browser & Device Support

- Web applications MUST support: Chrome, Firefox, Safari, Edge (latest 2 versions)
- Mobile app MUST support: iOS 14+, Android 10+
- Mobile app MUST support: iPhone 8+, modern Android devices with ARCore support
- Web applications MUST be responsive (desktop, tablet, mobile views)

---

## Edge Cases & Exception Handling

### EC-001: Payment Failures

**Scenario**: Patient's payment fails during booking confirmation

**Handling**:

- System MUST retry payment up to 3 times
- System MUST notify patient of payment failure with clear error message
- System MUST keep the one fixed slot hold that started at subquote acceptance (FR-026 slot-hold duration, default **48 hours**, admin-configurable); payment failure or retry never extends or restarts it, and the patient may retry while it is active
- System MUST release the reservation if payment not completed within the hold window
- System MUST notify provider and patient of slot release
- System MUST transition the pending booking to `Payment Window Expired` (final except for the audited admin revive), block payment against that accepted selection unless an admin revives the booking, preserve the immutable AcceptanceEvent/snapshot, and MUST NOT reopen the parent quote or accepted subquote
- This applies only to the first payment step; a missed later installment or final payment never causes `Payment Window Expired`

### EC-002: Provider Cancellation

**Scenario**: After subquote acceptance, the provider withdraws the accepted quote, drops out before or during treatment, or is suspended or deactivated

**Handling**:

- System MUST cancel a booking in `Accepted` or `Confirmed` with cause `ProviderFault` (or `ProviderSuspended` / `ProviderDeactivated`) and a `supportRequired` marker, release the hold or calendar block, and keep the AcceptanceEvent unchanged; in `In Progress` the booking is not cancelled automatically, stays flagged `supportRequired`, and an admin either moves it to `Aftercare` with aftercare-provider reassignment or cancels it with a reason; in `Aftercare` the booking is not cancelled and an admin reassigns the aftercare provider
- The inquiry MUST stay open; for a booking in `Accepted` or `Confirmed`, an admin authors a replacement quote on behalf of a replacement provider in the same inquiry, and its acceptance creates a new admin-authored acceptance record with a single supersession record linking it to the original (FR-006 provider-fault transfer); a replacement quote that is not accepted expires normally and the inquiry stays `supportRequired` without automatic cancellation
- Amounts already paid move with the patient as credit toward the replacement booking, any unused part is refunded, and the patient pays no cancellation fee; exact mechanics are defined in FR-007, FR-007B, and FR-017
- System MUST notify the patient and both providers of the transfer
- System MUST apply penalty to provider (e.g., commission increase on next booking)
- System MUST track provider cancellation rate and flag high-cancellation providers

### EC-003: No Quotes Received

**Scenario**: Patient submits inquiry but receives zero quotes within 72 hours

**Handling**:

- System MUST notify patient of situation
- System MUST offer to extend inquiry to additional providers
- System MUST offer alternative locations/countries
- Admin MUST manually review and potentially contact providers to encourage quote submission

### EC-004: Patient No-Show

**Scenario**: Patient does not arrive for scheduled procedure

**Handling**:

- Provider MUST report no-show within 24 hours
- System MUST flag the booking as **No-Show** (case flag/label; not a booking pipeline status)
- Admin MUST review the case and handle cancellation policy enforcement (deposit retention/refunds) and payout reconciliation
- System MUST notify patient and offer to reschedule (subject to provider approval and any additional fees)

### EC-005: Medical Complication During Recovery

**Scenario**: Patient reports concerning symptoms during aftercare period

**Handling**:

- Aftercare specialist MUST escalate to medical supervisor immediately
- System MUST flag case as "urgent" with red indicator
- System MUST notify original provider of complication
- Admin MUST facilitate communication between patient and provider
- If necessary, system MUST help patient find local medical care
- System MUST document all actions taken for liability protection

### EC-006: Currency Exchange Rate Fluctuation

**Scenario**: Exchange rate changes significantly between quote and payment

**Handling**:

- System MUST lock exchange rate at time of subquote acceptance and record the rate and its timestamp in the acceptance snapshot
- Patient MUST pay based on locked rate, regardless of current market rate
- Provider MUST receive payout based on locked rate
- Platform bears currency risk during escrow period
- System MUST hedge large transactions (future enhancement)

### EC-007: Duplicate Account Detection

**Scenario**: Patient attempts to create multiple accounts to exploit first-booking discounts

**Handling**:

- System MUST detect duplicate accounts by: email, phone number, device ID
- System MUST flag suspicious accounts for admin review
- Admin MUST investigate and merge or suspend duplicate accounts
- System MUST prevent discount abuse

### EC-008: Provider Document Expiration

**Scenario**: Provider's medical license or certification expires

**Handling**:

- System MUST track expiration dates of provider credentials
- System MUST send reminder emails to provider 60/30/7 days before expiration
- System MUST suspend provider from receiving new inquiries if credentials expire
- Admin MUST review and re-verify renewed credentials
- System MUST reactivate provider upon successful verification

---

## Success Criteria

### SC-001: Conversion Rate

- **Target**: 25% of submitted inquiries result in confirmed bookings (FR-006 `Confirmed`, reached at the first successful payment)
- **Measurement**: (Confirmed bookings / Total inquiries) x 100
- **Timeframe**: Measured quarterly

### SC-002: Platform NPS

- **Target**: Net Promoter Score > 60
- **Measurement**: Post-recovery survey sent at 6-month milestone
- **Timeframe**: Measured quarterly

### SC-003: Provider Response Time

- **Target**: 90% of providers submit quotes within 48 hours
- **Measurement**: Time from inquiry distribution to quote submission
- **Timeframe**: Measured monthly

### SC-004: Payment Success Rate

- **Target**: 95% of payment attempts succeed on first try
- **Measurement**: (Successful payments / Total payment attempts) x 100
- **Timeframe**: Measured weekly

### SC-005: Aftercare Engagement

- **Target**: 70% of patients actively use aftercare features (upload photos, complete questionnaires)
- **Measurement**: Patients who complete at least 2 milestones / Total patients in aftercare
- **Timeframe**: Measured monthly

### SC-006: Average Transaction Value

- **Target**: $4,000 per booking (range: $2,500 - $8,000)
- **Measurement**: Total procedure revenue / Number of bookings
- **Timeframe**: Measured monthly

### SC-007: Provider Retention

- **Target**: 80% of onboarded providers remain active after 12 months
- **Measurement**: Providers with at least 1 booking in last 90 days / Total onboarded providers
- **Timeframe**: Measured quarterly

### SC-008: Patient Satisfaction

- **Target**: 4.5+ average rating from patient reviews
- **Measurement**: Sum of ratings / Number of reviews
- **Timeframe**: Measured monthly

### SC-009: Time to First Quote

- **Target**: Patients receive first quote within 12 hours of inquiry submission (median)
- **Measurement**: Time from inquiry submission to first quote received
- **Timeframe**: Measured weekly

### SC-010: Booking Completion Rate

- **Target**: 85% of accepted subquotes lead to confirmed bookings
- **Measurement**: (Confirmed bookings / Accepted subquotes) x 100
- **Timeframe**: Measured monthly

---

## Out of Scope (Future Enhancements)

### V2 Enhancements

1. **AI-Powered Matching**: Machine learning to match patients with ideal providers based on history
2. **Virtual Consultations**: Built-in video conferencing for pre-procedure consultations
3. **Treatment Financing**: Integration with medical financing providers for payment plans
4. **Multi-Procedure Support**: Expand beyond hair transplants to other cosmetic procedures
5. **Provider Subscription Tiers**: Premium provider memberships with featured placement and analytics
6. **Patient Loyalty Program**: Rewards for referrals and repeat procedures

### V3 Enhancements

1. **Standalone Aftercare App**: Separate app for long-term hair health monitoring and product recommendations
2. **AI Scan Analysis**: Automated graft count estimation and treatment recommendations
3. **Outcome Prediction**: AI models to predict expected results based on historical data
4. **Social Features**: Patient community for sharing experiences and tips
5. **Medical Tourism Insurance**: Built-in insurance products for procedure coverage
6. **Blockchain Medical Records**: Decentralized, portable medical record system

---

## Assumptions & Dependencies

### Assumptions

1. Patients have access to smartphones with camera (for head scan photo set capture)
2. Providers have stable internet connection for real-time quote submission
3. Payment processing can be handled via third-party service (Stripe)
4. Phase 2 travel APIs are available and cost-effective for flight/hotel integration
5. Aftercare can be delivered remotely without in-person clinical visits in most cases
6. Providers are willing to share commission with platform (15-25%)
7. English and Turkish languages cover majority of target market (initially)

### Dependencies

1. **Stripe Payment Gateway**: For payment processing, escrow, and payouts
2. **AWS/GCP Cloud Infrastructure**: For hosting, storage, and scalability
3. **Twilio/SendGrid**: For SMS and email notifications
4. **Firebase/OneSignal**: For push notifications
5. **Flight API** (Amadeus/Skyscanner): For Phase 2 travel booking integration
6. **Hotel API** (Booking.com/Expedia): For Phase 2 hotel booking integration
7. **3D Scanning SDK (V2)**: For true 3D head scanning (ARKit/ARCore); V1 uses photo sets
8. **Currency Exchange API**: For real-time exchange rates
9. **Translation API**: For multi-language support (Google Translate API)

---

## Appendix

### Glossary

- **Patient**: End-user seeking hair transplant procedure
- **Provider**: Clinic or hospital offering hair transplant services
- **Inquiry**: Patient's request for treatment quotes
- **Parent Quote**: Provider response that owns shared provider, treatment, clinical, lifecycle, version, and audit context and groups one or more Quote Options
- **Quote Option**: One alternative within a parent quote, seeded from exactly one package version as a quote-local copy (at most five per parent quote)
- **Package**: Provider-owned, versioned, currency-free template for one quote option (included services and prices, travel services, standard price, relative-day treatment plan)
- **Subquote**: Complete patient-visible choice resolving one Quote Option plus one applicable Option/date-price record; the atomic comparison and acceptance unit
- **AcceptanceEvent**: Append-only record of the patient's acceptance of exactly one subquote, with an immutable snapshot of price after promotion, currency, date range, appointment, promotion, and the exchange rate with its timestamp; supersession and annotations are separate linked records
- **Booking**: Pending or confirmed booking record derived from exactly one AcceptanceEvent, accepted subquote, and immutable inherited parent context. `Accepted` (shown to the patient as "Booking Accepted — Slot Held (Pending Payment)") awaits initial payment under one fixed exclusive slot hold; successful first payment moves it to `Confirmed` and creates the appointment; hold expiry moves it to `Payment Window Expired`, which is final except for an audited admin revive that returns the booking to `Accepted` with a new hold.
- **Graft**: Unit of hair follicles transplanted (typically 1-4 hairs per graft)
- **FUE**: Follicular Unit Extraction (hair transplant technique)
- **FUT**: Follicular Unit Transplantation (hair transplant technique)
- **Aftercare**: Post-procedure support and monitoring period (6-12 months)
- **Escrow**: Holding patient payment until procedure completion
- **Commission**: Platform's fee on each booking under the provider's commission model (FR-029): a Percentage of the booking total (the accepted price after promotion), or a Flat Rate fixed amount deducted once per completed procedure
- **Affiliate**: Marketing partner who refers patients for commission

### References

- Hairline Overview Transcription: `local-docs/project-requirements/transcriptions/HairlineOverview.txt`
- Constitution Document: `.specify/memory/constitution.md`
- Backend Models: `main/hairline-backend/app/Models/`
- Frontend Routes: `main/hairline-frontend/src/data.jsx`

### Document Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-16 | Vân Tay Media | MTG-002 quote model alignment and Product Owner Q-series follow-up (decisions D1 to D24, M2 to M18, Q2 to Q30; Q26 and Q27 deferred; recorded here retrospectively, as the version was not bumped at the time): parent quote, quote option and subquote model; acceptance record and booking with a fixed slot hold, `Payment Window Expired` and audited admin revive; provider-fault transfer; offered prices greater than 0 and `quote.updated` on re-send; commission, deposit and instalments on one booking total after promotion for every discount type; promotion use reservations; acceptance notifications; Quote Configuration and currency disable guard; approximate cross-currency price sort; itinerary read view and travel-record carry-over; treatment-detail changes through FR-010 |
| 1.1.0 | 2026-10-18 | Vân Tay Media | Consolidated verification corrections (Q2, Q5, Q17, Q18, Q20, Q34; D2, D11, D12, M18; no Change Request, system document): Workflow 1 treatment-detail changes bounded to `Confirmed` until Check In with admin-only appointment changes; FR-006 admin revive takes an automatic promotion use again or reserves a provider-selected or patient-code use again, rejected when the limit has no room; FR-008 travel records stored against the booking's travel context; FR-015 provider status change cancels bookings and the inquiry stays open for transfer; FR-019 reservation released when the quote is cancelled before acceptance, and a provider discount reduces the commission base like every discount type; FR-024 treatment pricing is a non-binding reference; glossary Commission and Booking entries updated; version bumped and change log added |
| 1.2.0 | 2026-10-18 | Vân Tay Media | Final audit corrections (Q31, Q35 to Q44; f1 F5, F8, F10; f2 F2, F4, F5, F8, F10; f3 F5; no Change Request, system document): commission described as the FR-029 Percentage (0 to 100%) or Flat Rate models with a 15 to 25% global percentage default; patients cancel only in Inquiry or Quoted and contact support after acceptance, including after Payment Window Expired; after acceptance only an admin cancels a booking, from any state, the inquiry becomes Cancelled and the quote stays accepted; provider-fault transfer limited to Accepted and Confirmed, with aftercare provider reassignment in Aftercare; replacement quote authored by an admin with one supersession record inserted at the replacement acceptance; treatment-detail changes by the clinic until Check In and by an admin at any time from Confirmed; promotion priority adds Hairline-funded promotions, one automatic promotion per quote, `not_applied` release, limit-full sends proceed without the promotion, Both Fees uses the Hairline share percentage; `booking.scheduled` is patient-only and also fires at the replacement acceptance, new `booking.rescheduled`, and `quote.withdrawn` after acceptance added to admin exception alerts; round-2 additions (Q45 to Q49, Q42 check): a provider fault, suspension, or deactivation on an In Progress booking keeps it In Progress with `supportRequired` for an admin decision (Aftercare with aftercare-provider reassignment, or cancellation with reason) instead of cancelling it; FR-010 treatment record created at confirmation in Awaiting Check In; new mandatory `aftercare.provider_reassigned` for patient and new aftercare provider; no automatic promotion or reservation on an admin-authored replacement quote; an unaccepted replacement quote expires normally with the inquiry staying support-required; booking notices and FR-010 read the booking's current appointment while the acceptance snapshot keeps the accepted baseline |

---

**Document Status**: ✅ Complete  
**Next Steps**: Create Technical Specification and Data Schema documents  
**Maintained By**: Product Team  
**Review Cycle**: Quarterly or upon major feature changes
