# Hairline Platform - Product Requirements Document (PRD)

**Version**: 1.0.0  
**Document Type**: System-Level PRD  
**Created**: 2025-10-23  
**Status**: Active  
**Last Updated**: 2025-10-30

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

- **Conversion Rate**: 25% of inquiries to booked procedures
- **Platform NPS**: > 60
- **Provider Response Time**: < 24 hours for quote submission
- **Booking Completion**: 85% of accepted quotes to scheduled procedures
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
- **Travel Convenience**: Book flights and hotels directly through the platform
- **Quality Assurance**: All providers vetted and verified by Hairline
- **Comprehensive Support**: Dedicated aftercare team for post-procedure guidance
- **3D Scanning**: Advanced assessment tools for accurate treatment planning

#### For Providers

- **Lead Generation**: Access to qualified patient leads actively seeking procedures
- **Operational Efficiency**: Streamlined inquiry and quote management
- **Payment Security**: Guaranteed payments through escrow system
- **Marketing Support**: Featured placement in patient-facing app
- **Team Collaboration**: Multi-user access with role-based permissions
- **Analytics**: Insights into performance, conversion rates, and revenue

#### For Hairline (Business)

- **Commission Revenue**: Percentage-based commission on each procedure
- **Travel Revenue**: Commissions from flight/hotel bookings
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
   - Performs 3D scan of head (or uploads photos/videos)

2. **Inquiry Submission**
   - Selects preferred countries/cities for treatment
   - Selects preferred treatment dates
   - Submits inquiry to matching providers
   - System distributes inquiry to providers in selected locations

3. **Quote Comparison**
   - Receives quotes from multiple providers (24-72 hours)
   - Compares pricing, reviews, credentials, package details
   - Asks clarifying questions through chat
   - Reviews before/after photos and provider credentials

4. **Quote Acceptance & Scheduling**
   - Accepts preferred quote (auto-schedules with pre-selected appointment time)
   - Provider must pre-schedule appointment times in quote submission
   - Quote acceptance automatically moves to "Accepted" status
   - Receives preliminary booking details

5. **Payment & Confirmation**
   - Makes payment (deposit or full amount, or selects installment plan)
   - Installment plans: 2-9 months interest-free (must complete 30 days before procedure)
   - Payment completion moves booking to "Confirmed" status
   - Patient anonymization lifted - provider can now see full name and contact details
   - Receives final booking confirmation

6. **Travel Planning**
   - Books flights through integrated travel API
   - Selects hotel from provider-recommended options
   - Confirms airport transport arrangements
   - Downloads travel itinerary and clinic instructions

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
   - Treatment completion moves status to "Aftercare"
   - Receives post-op instructions and medications

9. **Aftercare (6-12 months)**
   - Returns home
   - Receives scheduled notifications for washing, medication, activities
   - Uploads progress photos at milestones (1 week, 1 month, 3 months, 6 months, 12 months)
   - Chats with aftercare specialists for questions/concerns
   - Completes recovery questionnaires
   - Submits final review and rating (status moves to "Completed")

---

### Workflow 2: Provider Quote Management

**Actors**: Provider (Clinic Staff), Patient

**Stages**:

1. **Inquiry Receipt**
   - Receives notification of new inquiry matching clinic's location
   - Reviews patient details, 3D scan, medical history, preferences
   - Reviews medical questionnaire with color-coded alerts

2. **Quote Creation**
   - **Selects treatment** (from admin-created list: FUE, FUT, DHI, etc.) - foundation, same for all providers
   - **Selects optional packages** (from own package list: hotels, transport, flights, medications, PRP) - provider-specific add-ons
   - Analyzes 3D scan to estimate graft count needed
   - **Selects clinician** who will perform the procedure (from clinic's staff list)
   - Customizes graft count, technique specifications
   - Sets pricing for treatment + selected packages
   - Adds photos/videos of similar cases or visual treatment plan
   - **Pre-schedules appointment time slots** (required for auto-accept)
   - Applies any applicable discounts
   - Adds notes for patient

3. **Quote Submission**
   - Submits quote to patient with pre-scheduled appointment times (deadline: 72 hours from inquiry)
   - Quote expires after 48 hours (configurable by admin)
   - Quote enters patient's comparison dashboard

4. **Negotiation (Optional)**
   - Responds to patient questions through chat
   - May adjust quote based on patient feedback
   - Provides additional information or credentials

5. **Quote Acceptance (Auto-Scheduled)**
   - Receives notification of quote acceptance
   - Appointment is AUTOMATICALLY confirmed (patient selected pre-scheduled time)
   - No manual confirmation needed - moves directly to "Accepted" status
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
   - Tracks quote acceptance rates by provider
   - Identifies stuck inquiries or delayed quotes
   - Intervenes in patient-provider disputes

3. **Billing & Commissions**
   - Collects patient payments (deposit and final)
   - Holds funds in escrow until procedure completion
   - Calculates platform commission (typically 15-25%)
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
- Personal data MUST be encrypted at rest
- System MUST maintain audit log of profile changes

---

### FR-002: Medical History & 3D Scanning

**Priority**: P1 (MVP)  
**Module(s)**: P-07: 3D Scan Capture & Viewing | S-01: 3D Scan Processing Service | S-05: Media Storage Service

**Note on Release Scope:**
For V1, the system accepts a guided head video (or photos/clips) for intake and validation. True 3D model capture, generation of multiple 2D views from 3D, and full ARKit/ARCore 3D processing pipeline are deferred to V2 (future enhancement), as patient-side hardware and provider UX matures.

**Requirements**:

- Patients MUST complete comprehensive medical questionnaire before submitting inquiry
- System MUST capture 3D scan of patient's head using mobile camera
- System MUST support alternative upload of photos/videos
- System MUST validate scan quality and provide feedback
- System MUST watermark all patient scans with anonymized patient identifier
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

- MUST support iOS ARKit and Android ARCore
- MUST provide real-time guidance for scan capture
- MUST process scan on device or cloud (based on device capability)
- MUST generate multiple 2D views from 3D scan for provider review

---

### FR-003: Inquiry Submission & Distribution

**Priority**: P1 (MVP)  
**Module(s)**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight

**Requirements**:

- Patients MUST be able to select multiple countries/cities for treatment (max 10 countries)
- Patients MUST indicate preferred treatment dates (max 10 date ranges, up to 2 years in future)
- Patients MUST select preferred providers (max 5 providers) based on reviews and admin curation
- Patients can only have one active inquiry at a time
- System MUST distribute inquiry to providers in selected locations OR explicitly selected by patient
- System MUST limit inquiry distribution to maximum 10 providers
- Providers MUST receive inquiry notification within 5 minutes
- System MUST track inquiry expiration (72 hours for quote submission)
- System MUST allow patients to close/cancel inquiry before receiving quotes
- System MUST support secondary service options: Monitor Hair Loss, Aftercare services
- System MUST generate unique inquiry IDs in HPID format (HPID + YY + MM + 4-digit sequence)

**Business Rules**:

- Inquiry MUST include: patient scan, medical history, destinations, treatment date ranges, and selected providers
- Inquiry MUST NOT include: patient name, exact location, contact information (until booking)
- System MUST filter providers by: location, active status, available capacity, patient explicit selection
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

- Providers MUST select treatment from admin-created list (FUE, FUT, DHI, etc.) - ensures consistency
- Providers MUST be able to select from their own package list (hotels, transport, flights, medications, PRP) - provider-specific
- Providers MUST pre-schedule appointment times as part of quote submission
- Quotes MUST include: selected treatment, graft count, technique, optional packages, pricing breakdown, timeline, pre-scheduled appointment slots
- Quotes MUST support multiple currencies with real-time exchange rates
- Providers MUST be able to attach before/after photos, credentials, facility images
- System MUST calculate total quote amount: treatment price + package prices + fees
- System MUST apply applicable discounts (provider promotions, affiliate codes)
- Providers MUST submit quotes within 72 hours of inquiry receipt
- System MUST validate quote completeness before submission
- Quotes MUST have customizable expiration period (default: 48 hours, admin-configurable)

**Auto-Accept Workflow**:

- When patient accepts quote, appointment is automatically scheduled (no manual provider confirmation needed)
- System immediately moves status from "Quote" to "Accepted"
- Provider receives notification of acceptance with pre-scheduled appointment details
- Patient proceeds directly to payment screen

**Quote Components**:

**1. Treatment (Required - Admin-Created)**:

- Treatment type (FUE, FUT, DHI, etc.) - selected from admin list
- Graft count estimation
- Technique specifications
- Treatment pricing (set by provider)

**2. Packages (Optional - Provider-Created)**:

- Hotel packages (4-star, 5-star, etc.)
- Transport packages (airport pickup, transfers)
- Flight assistance packages
- Medication packages (post-op medications)
- Additional services (PRP therapy, specialized treatments)
- Package pricing (set by provider)

**3. Other Components**:

- Consultation fees
- Clinician selection
- Pre-scheduled appointment time slots

**Pricing Rules**:

- Quote MUST lock exchange rate at time of patient acceptance
- Quote MUST clearly separate provider fees from Hairline platform fees
- Quote MUST show original price and discount if applicable

---

### FR-005: Quote Comparison & Acceptance

**Priority**: P1 (MVP)  
**Module(s)**: P-02: Quote Request & Management | A-01: Patient Management & Oversight

**Requirements**:

- Patients MUST be able to view all received quotes in comparison dashboard
- System MUST display key differentiators: price, graft count, reviews, credentials
- Patients MUST be able to filter and sort quotes by criteria
- Patients MUST be able to ask questions about quotes through secure messaging (see FR-012; MVP channel: Patient ↔ Hairline Support)
- System MUST notify Hairline support of patient questions within 5 minutes
- Patients MUST be able to accept one quote at a time
- System MUST mark other quotes as "cancelled (other accepted)" when one is accepted
- System MUST notify patient and provider immediately upon quote acceptance

**Comparison Features**:

- Side-by-side comparison view (up to 3 quotes)
- Price per graft calculation
- Review rating and count
- Provider credentials summary
- Included services checklist
- Estimated travel costs

---

### FR-006: Booking & Scheduling

**Priority**: P1 (MVP)  
**Module(s)**: P-03: Booking & Payment | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight

**Requirements**:

- Patients MUST be able to select procedure date from provider's available slots
- System MUST integrate with provider's calendar to show real-time availability
- Patients MUST confirm booking by paying deposit (admin-configurable percentage, default 20-30% of total, configured via FR-029)
- System MUST generate booking confirmation with reference number
- System MUST send confirmation emails to patient and provider
- System MUST allow rescheduling up to 14 days before procedure (subject to provider approval)
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
- System MUST support credit/debit cards, bank transfers, digital wallets
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

- Platform commission: 15-25% of total procedure cost (configurable per provider)
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
- System MUST automatically calculate installment amounts (total ÷ number of installments)
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

- System MUST integrate with flight booking API (e.g., Amadeus, Skyscanner)
- System MUST integrate with hotel booking API (e.g., Booking.com, Expedia)
- Patients MUST be able to search and book flights directly in app
- Patients MUST be able to select hotels from provider-recommended list
- System MUST show real-time pricing and availability
- System MUST send booking confirmations for flights and hotels
- System MUST support airport transport booking (future: Uber/Bolt API)
- System MUST aggregate all travel details into unified itinerary

**Flight Cost Preview** (P1 - Required for Inquiry):

- During inquiry date selection, system MUST display estimated flight costs
- System MUST fetch average/cheapest flight prices for selected date ranges
- Flight preview helps patients choose optimal travel dates based on cost
- Display format: "Est. flights: £220 - £450" (cheapest - average)

**Travel Commission**:

- Platform earns commission on flight bookings (3-5%)
- Platform earns commission on hotel bookings (10-15%)
- Commission MUST be tracked separately from procedure commission

---

### FR-009: Provider Team & Role Management

**Priority**: P1 (MVP)  
**Module(s)**: PR-01: Auth & Team Management

**Requirements**:

- Providers MUST be able to invite team members to platform
- System MUST support role-based permissions (Owner, Manager, Clinical Staff, Billing Staff)
- Each role MUST have specific access rights to features and data
- Team members MUST be able to collaborate on inquiries and quotes
- System MUST log all actions by user for audit trail
- Providers MUST be able to remove or suspend team members (within Owner/Manager permissions)
- System MUST send email invitations to new team members

**Role Permissions**:

- **Owner (Main Account Holder)**: Full access, billing, team management, and legal/contract responsibility; only role allowed to manage bank account details and ownership changes (via Admin Platform workflows).
- **Manager (Clinic Manager / Operations)**: Broad operational access across inquiries, quotes, schedules, and day-to-day team management, but no ability to change ownership or bank account details.
- **Clinical Staff**: Access to in-progress and aftercare sections, treatment execution and documentation, and clinical notes; limited or no access to billing configuration.
- **Billing Staff**: Access to financial views (quotes, payouts, revenue metrics) and reconciliation screens; no access to treatment documentation or team structure changes.

---

### FR-010: Treatment Execution & Documentation

**Priority**: P1 (MVP)  
**Module(s)**: PR-03: Treatment Execution & Documentation

**Requirements**:

- Providers MUST be able to mark patient as "arrived" when patient shows up at clinic
- System MUST automatically move status to "In Progress" upon patient arrival
- Providers MUST be able to update treatment progress during procedure (real-time updates)
- System MUST capture: procedure date/time, surgeon name, technique, graft count, donor area, recipient area
- Providers MUST be able to upload before/during/after photos
- System MUST store treatment notes and observations throughout procedure
- Providers MUST be able to prescribe medications and provide instructions
- System MUST generate post-op instruction sheet for patient
- System MUST mark treatment as "completed" to trigger move to "Aftercare" status
- System MUST record final payment collection (if not already completed)

**Status Transitions**:

- Patient arrives → Status: "In Progress"
- Treatment completed → Status: "Aftercare"
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
  - Required 3D scan frequency (daily, every 5 days, weekly, bi-weekly, monthly)
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

**3D Scan Requirements**:

- Patients MUST upload 3D head scans at milestone-defined intervals
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
- System shows "next upcoming task" (e.g., "3D Scan due in 2 days")

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
  - 3D scan history (all uploaded scans with timestamps)
  - Questionnaire responses (pain levels, sleep quality, compliance data)
  - Medication schedule and adherence
  - Activity restrictions for current milestone
  - Provider's custom instructions
- Aftercare specialists can request additional information:
  - Request 3D scan (if patient missed scheduled scan)
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
3. ✅ Patients upload 3D scans at milestone intervals (milestone-defined frequency)
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
**Module(s)**: P-06: Communication | A-10: Communication Monitoring & Support

**Requirements**:

- System MUST provide secure messaging between patients and Hairline support
- System MUST provide secure messaging between patients and aftercare specialists
- Messages MUST support text, images, and video
- System MUST deliver real-time notifications for new messages
- System MUST maintain conversation history
- System MUST support read receipts
- System MUST log all communications for compliance and dispute resolution

**Communication Channels**:

- Patient ↔ Hairline Support (general inquiries, quote questions)
- Patient ↔ Aftercare Team (recovery support, post-op questions)
- Provider ↔ Admin (operational questions, billing issues)
- Admin ↔ Patient (dispute resolution, support escalation)

**Backlog (Future Enhancement)**:

- ⏸️ Patient ↔ Provider direct messaging (quote negotiation, booking coordination)
  - Currently unclear from requirements if this is needed
  - Patients can communicate with Hairline support who can relay messages if needed
  - May be added in V2 if business case is validated
  - Quote Q&A should be specified in FR-012; other FRs (e.g., FR-005) should reference this capability rather than redefining it

---

### FR-013: Reviews & Ratings

**Priority**: P2 (Enhanced)  
**Module(s)**: P-02: Quote Request & Management | A-01: Patient Management & Oversight

**Requirements**:

- Patients MUST be able to submit review and rating after procedure completion (after 3+ months)
- Reviews MUST include: overall rating (1-5 stars), category ratings (facility, staff, results), written feedback
- System MUST verify that only patients who completed procedure can submit reviews
- Patients MUST be able to upload before/after photos with review (optional)
- Reviews MUST be published only after admin moderation (to filter spam/inappropriate content)
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

**Requirements**:

- Providers MUST have access to performance dashboard
- System MUST display: inquiry count, quote count, quote acceptance rate, revenue, patient count
- System MUST provide conversion funnel analytics
- System MUST show average quote amount and price per graft
- System MUST display review ratings and trends over time
- Providers MUST be able to export reports (PDF, CSV)
- System MUST provide comparative benchmarks (anonymized industry averages)

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
- System MUST set provider commission rate per provider using configurable Percentage or Flat Rate models (tier-based commission structures are out of scope for MVP and may be defined in a future FR).
- Admins MUST be able to feature providers in patient-facing app
- System MUST track provider status (draft, active, suspended, deactivated)

**Admin Workflow**:

1. Admin creates provider account (manual entry)
2. Admin uploads provider credentials (licenses, certifications, insurance) for record-keeping
3. Admin sets commission rate (Percentage or Flat Rate)
4. Admin activates provider account (activation is not blocked by document status; documents are assumed to have been pre-verified offline)
5. Provider receives login credentials and can access platform

**Note**: Providers do NOT self-register. All provider accounts are created by admin team.

---

### FR-016: Admin Patient Management

**Priority**: P1 (MVP)  
**Module(s)**: A-01: Patient Management & Oversight

**Requirements**:

- Admins MUST be able to view all patient profiles and inquiries
- Admins MUST be able to search patients by name, email, phone, patient code
- Admins MUST be able to view patient treatment history and status
- Admins MUST be able to manually intervene in patient-provider disputes
- Admins MUST be able to reset patient passwords
- Admins MUST be able to suspend or deactivate patient accounts
- System MUST log all admin actions on patient accounts for audit trail

---

### FR-017: Admin Billing & Financial Management

**Priority**: P1 (MVP)  
**Module(s)**: A-05: Billing & Financial Reconciliation | PR-05: Financial Management & Reporting

**Requirements**:

- Admins MUST be able to view all transactions (deposits, final payments, refunds)
- System MUST calculate provider payouts (total revenue - platform commission)
- Admins MUST be able to process provider payouts on scheduled basis (bi-weekly or monthly)
- System MUST generate invoices for providers
- Admins MUST be able to create and manage discount codes
- System MUST track discount code usage and ROI
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
- System MUST calculate affiliate commission (% of platform commission or fixed amount)
- Affiliates MUST have access to dashboard showing referral count, revenue, commissions
- Admins MUST be able to process affiliate payouts monthly
- System MUST generate affiliate performance reports

**Affiliate Features**:

- Unique referral link/code
- Dashboard with real-time stats
- Commission tracking and payout history
- Marketing materials (banners, templates)

---

### FR-019: Promotions & Discount Management

**Priority**: P2 (Enhanced)  
**Module(s)**: A-06: Discount & Promotion Management

**Requirements**:

- Admins MUST be able to create platform-wide discount codes
- Providers MUST be able to create provider-specific discounts
- System MUST support discount types: percentage, fixed amount, package upgrades
- Discounts MUST have start/end dates and usage limits
- System MUST validate discount codes at quote creation and booking
- System MUST apply only one discount per booking (priority: patient code > provider code > affiliate code)
- System MUST track discount usage and total discount amount

**Discount Approval Workflow**:

- Platform discounts affecting "both fees" (provider + Hairline) MUST require provider approval
- System MUST send approval notifications to providers when new platform discount is created
- Providers can accept or decline participation in each discount
- Accepted discounts appear in provider's quote creation discount selection
- Provider-only discounts do not require approval (auto-active)
- Hairline-only discounts (deducted from platform commission only) not shown to providers

**Discount Categories**:

- **Provider Discount**: Created by provider, affects only their fee
- **Platform Discount (Both Fees)**: Created by admin, requires provider approval, affects total price
- **Hairline Discount**: Created by admin, affects only Hairline commission, invisible to providers
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
- System MUST throttle notifications to prevent spam
- System MUST track notification delivery status

**Implementation Note:**
For patient platform in FR-001 (MVP), notification preferences are limited to global Email/Push toggles; category preferences (e.g., Inquiry, Quote, Payment, Aftercare) are deferred to V2 per product management alignment.

**Provider Notification Preferences:**
Provider notification preferences are managed in FR-032 (Provider Dashboard Settings & Profile Management). Providers configure unified notification preferences including individual notification type toggles (quote, schedule, treatment start, aftercare, review, promotion/discount) and global channel preferences (email, push/in-app). SMS is a future enhancement and is **not** exposed as a configurable channel in MVP.

---

### FR-021: Multi-Language & Localization

**Priority**: P2 (Enhanced)  
**Module(s)**: A-09: System Settings & Configuration | S-02: Payment Processing Service

**Requirements**:

- System MUST support multiple languages (English, Turkish initially, expandable)
- Patients and providers MUST be able to select preferred language
- System MUST translate UI elements, emails, and push notifications
- System MUST support RTL languages (future: Arabic)
- System MUST display dates and times in user's timezone
- System MUST support local currency display with conversion

---

### FR-022: Search & Filtering

**Priority**: P2 (Enhanced)  
**Module(s)**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | PR-03: Treatment Execution & Documentation | PR-04: Aftercare Participation | PR-05: Financial Management & Reporting | PR-06: Profile & Settings Management | A-01: Patient Management & Oversight | A-02: Provider Management & Onboarding | A-03: Aftercare Team Management | A-05: Billing & Financial Reconciliation | A-06: Discount & Promotion Management | A-07: Affiliate Program Management | A-08: Analytics & Reporting | A-09: System Settings & Configuration | A-10: Communication Monitoring & Support

**Requirements**:

- Patients MUST be able to search providers by location, rating, price range
- Patients MUST be able to filter providers by credentials, years of experience, procedures performed
- Admins MUST be able to search patients, providers, transactions, inquiries
- System MUST provide autocomplete for location searches
- System MUST support advanced filtering with multiple criteria

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
- Providers configure **pricing** for each treatment in their clinic
- All providers see the **same treatment list** (FUE, FUT, DHI, etc.)

**Examples of Treatments**:

- FUE (Follicular Unit Extraction)
- FUT (Follicular Unit Transplantation)
- DHI (Direct Hair Implantation)
- Sapphire FUE
- Robotic Hair Transplant

---

#### Part B: Packages (Provider-Created Add-Ons)

**Requirements**:

- **Package Creation Authority**: Each provider creates their own packages
- Packages are **optional add-ons** that supplement the treatment
- Providers configure: package name, description, pricing, availability
- Each provider has **their own package list** (can differ between providers)
- Packages are NOT part of treatment - they are separate selections

**Examples of Packages**:

- Hotel packages (3-star, 4-star, 5-star)
- Transport packages (airport pickup, city transfers)
- Flight assistance packages
- Medication packages (post-op medications to take home)
- PRP therapy add-on
- Extended consultation packages

---

#### Quote Structure

```sh
Quote = Treatment (required) + Packages (optional)
      = Treatment Price + Package Prices = Total Quote
```

**Example Quote Breakdown**:

```sh
Treatment: FUE (3000 grafts)           £2,500
Package: 4-star hotel (5 nights)       £300
Package: Airport transfer              £50
Package: PRP therapy session           £150
                                       ------
Total Quote:                           £3,000
```

---

#### Rationale

**Why Separate Treatments and Packages?**

1. **Consistency**: All providers offer same treatments (FUE, FUT, DHI) with standardized info and videos
2. **Flexibility**: Providers differentiate through their own package offerings
3. **Scalability**: When platform offers direct travel booking, provider packages can be disabled without affecting treatments
4. **Clarity**: Patients understand core procedure vs optional add-ons
5. **Future-Proof**: Easy transition from provider-managed to platform-managed services

---

### FR-025: Medical Questionnaire Management

**Priority**: P1 (MVP)  
**Module(s)**: A-09: System Settings & Configuration

**Requirements**:

- **Centralized Question Management**: Admin MUST be able to add, edit, remove, and reorder medical questionnaire questions
- **Question Content**: Each question MUST have: question text, question type (Yes/No), detailed explanation prompt for "Yes" answers
- **Severity Flagging**: Each question MUST have a severity flag (Critical/Standard/No Alert)
- **Alert System**: When patient answers "Yes" to Critical questions → inquiry flagged with red alerts
- **Alert System**: When patient answers "Yes" to Standard questions → inquiry flagged with yellow/amber alerts  
- **Alert System**: When patient answers "No" to all questions → inquiry flagged with green (no alerts)
- **Question Grouping**: Admin MUST be able to organize questions into categories (Allergies, Cardiovascular, etc.)
- **Version Control**: System MUST track questionnaire changes with timestamps and admin identification
- **Question Validation**: System MUST validate question completeness before activation
- **Questionnaire Preview**: Admin MUST be able to preview questionnaire as patients will see it
- **Bulk Operations**: Admin MUST be able to import/export questionnaire templates
- **Question Templates**: System MUST provide pre-built question templates for common medical conditions

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
  - Changes MUST propagate to dependent UIs within 1 minute

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
- **Deposit Rate Configuration**: Admins MUST be able to configure deposit percentage (default range: 20-30% of total booking amount). This MUST be configurable per provider or globally. Changes apply to new bookings only (existing bookings retain original deposit rate)
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

**Priority**: P1 (MVP)
**Module(s)**: A-09: System Settings & Configuration

**Goal**: Provide role-based access control system for admin platform with granular permission management, team member administration, and audit trail.

**Requirements**:

- Role Management: Admins MUST be able to create and manage admin roles (aftercare staff, billing staff, support staff, super admin)
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
**Module(s)**: A-09: System Settings & Configuration | PR-06: Profile & Settings Management

**Requirements**:

- Admins MUST be able to create, edit, and manage Help Centre content for provider platform
- System MUST support Help Centre categories: FAQ's, Tutorial Guides, Contact Support, Troubleshooting Tips, Resource Library, Community Forum, Feedback & Suggestions, Service Status, Policy Information, Video Tutorials
- Admins MUST be able to organize FAQ content by topics with expandable/collapsible sections
- Admins MUST be able to upload tutorial guides, videos, and resource documents
- System MUST support content versioning and audit trail for Help Centre updates
- Providers view Help Centre content as read-only (content managed exclusively by admins)
- System MUST support multi-language Help Centre content (future enhancement)

**Note**: Detailed requirements to be documented in dedicated FR-033 PRD.

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
- 3D scan processing MUST complete within 60 seconds

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
- System MUST hold booking for 24 hours to allow patient to retry payment
- System MUST release booking if payment not completed within 24 hours
- System MUST notify provider of booking cancellation

### EC-002: Provider Cancellation

**Scenario**: Provider cancels confirmed booking due to emergency or overbooking

**Handling**:

- Provider MUST submit cancellation request with reason
- Admin MUST approve cancellation (emergency only)
- System MUST issue full refund to patient immediately
- System MUST notify patient and suggest alternative providers
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
- System MUST flag booking as "no-show"
- System MUST retain deposit payment per cancellation policy
- Provider MUST receive payout of deposit minus platform commission
- System MUST notify patient and offer to reschedule (subject to provider approval and additional fees)

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

- System MUST lock exchange rate at time of quote acceptance
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

- **Target**: 25% of submitted inquiries result in booked procedures
- **Measurement**: (Booked procedures / Total inquiries) x 100
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

- **Target**: 85% of accepted quotes lead to confirmed bookings
- **Measurement**: (Confirmed bookings / Accepted quotes) x 100
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

1. Patients have access to smartphones with camera (for 3D scanning)
2. Providers have stable internet connection for real-time quote submission
3. Payment processing can be handled via third-party service (Stripe)
4. Travel APIs are available and cost-effective for flight/hotel integration
5. Aftercare can be delivered remotely without in-person clinical visits in most cases
6. Providers are willing to share commission with platform (15-25%)
7. English and Turkish languages cover majority of target market (initially)

### Dependencies

1. **Stripe Payment Gateway**: For payment processing, escrow, and payouts
2. **AWS/GCP Cloud Infrastructure**: For hosting, storage, and scalability
3. **Twilio/SendGrid**: For SMS and email notifications
4. **Firebase/OneSignal**: For push notifications
5. **Flight API** (Amadeus/Skyscanner): For travel booking integration
6. **Hotel API** (Booking.com/Expedia): For hotel booking integration
7. **3D Scanning SDK**: For mobile-based head scanning (ARKit/ARCore)
8. **Currency Exchange API**: For real-time exchange rates
9. **Translation API**: For multi-language support (Google Translate API)

---

## Appendix

### Glossary

- **Patient**: End-user seeking hair transplant procedure
- **Provider**: Clinic or hospital offering hair transplant services
- **Inquiry**: Patient's request for treatment quotes
- **Quote**: Provider's offer with pricing and treatment details
- **Booking**: Confirmed appointment for procedure after quote acceptance
- **Graft**: Unit of hair follicles transplanted (typically 1-4 hairs per graft)
- **FUE**: Follicular Unit Extraction (hair transplant technique)
- **FUT**: Follicular Unit Transplantation (hair transplant technique)
- **Aftercare**: Post-procedure support and monitoring period (6-12 months)
- **Escrow**: Holding patient payment until procedure completion
- **Commission**: Platform's percentage fee on each transaction
- **Affiliate**: Marketing partner who refers patients for commission

### References

- Hairline Overview Transcription: `local-docs/project-requirements/transcriptions/HairlineOverview.txt`
- Constitution Document: `.specify/memory/constitution.md`
- Backend Models: `main/hairline-backend/app/Models/`
- Frontend Routes: `main/hairline-frontend/src/data.jsx`

---

**Document Status**: ✅ Complete  
**Next Steps**: Create Technical Specification and Data Schema documents  
**Maintained By**: Product Team  
**Review Cycle**: Quarterly or upon major feature changes
