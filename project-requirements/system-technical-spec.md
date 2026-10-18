# Hairline Platform - Technical Specification

**Version**: 1.4.0  
**Document Type**: System-Level Technical Specification  
**Created**: 2025-10-23  
**Status**: Active  
**Last Updated**: 2026-10-18

---

## Executive Summary

This document provides the technical architecture, design decisions, and implementation guidelines for the Hairline Platform. It is intended for developers, architects, and technical stakeholders who need to understand how the system is built and how components interact.

### Technology Stack Overview

**Backend**:

- Framework: Laravel 10+ (PHP 8.1+)
- API: REST with OpenAPI/Swagger documentation
- Authentication: Laravel Passport (OAuth 2.0)
- Database: MySQL 8.0+ (primary), Redis (cache, sessions, queues)

**Frontend (Web)**:

- Framework: React 18+ with Vite
- State Management: Redux Toolkit with RTK Query
- UI Library: Ant Design
- Styling: SCSS/CSS Modules

**Mobile**:

- Framework: React Native (iOS/Android) OR Flutter (to be decided)
- State Management: Redux/Provider
- Head Scan Capture: V1 standardized photo set; V2 true 3D scanning via ARKit (iOS) / ARCore (Android)

**Infrastructure**:

- Cloud Provider: AWS (or GCP)
- Container Orchestration: Docker + Kubernetes (future)
- CDN: CloudFront
- Storage: S3 (media files, head scan photo sets (V1), 3D scans (V2))

**Third-Party Services**:

- Payment: Stripe
- Email: SendGrid
- SMS: Twilio
- Push Notifications: Firebase Cloud Messaging (FCM)
- Real-time: Laravel Reverb / Pusher
- Maps/Geocoding: Google Maps API

---

## System Architecture

### High-Level Architecture

```sh
┌────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                            │
├──────────────────┬──────────────────┬──────────────────────────┤
│  Patient App     │  Provider Web    │  Admin Web               │
│  (Mobile)        │  (React)         │  (React)                 │
│  iOS/Android     │                  │                          │
└────────┬─────────┴────────┬─────────┴────────┬─────────────────┘
         │                  │                  │
         └──────────────────┴──────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────────┐
         │          API GATEWAY / LOAD BALANCER     │
         │          (Nginx / AWS ALB)               │
         └──────────────────┬───────────────────────┘
                            │
         ┌──────────────────┴───────────────────────┐
         │                                          │
         ▼                                          ▼
┌─────────────────────┐                  ┌─────────────────────┐
│  BACKEND SERVICES   │                  │  SHARED SERVICES    │
├─────────────────────┤                  ├─────────────────────┤
│ - Auth Service      │◄────────────────►│ - Notification Svc  │
│ - Inquiry Service   │                  │ - Payment Svc       │
│ - Quote Service     │                  │ - Media Svc         │
│ - Payment Service   │                  │ - 3D Scan Processor │
│ - Aftercare Service │                  │ - Travel API        │
│ - Provider Service  │                  └─────────────────────┘
│ - Admin Service     │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│         DATA LAYER                       │
├────────────────┬─────────────────────────┤
│  MySQL DB      │  Redis Cache            │
│  (Primary)     │  (Sessions, Queue)      │
└────────────────┴─────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│         STORAGE LAYER                    │
├────────────────┬─────────────────────────┤
│  AWS S3        │  CloudFront CDN         │
│  (Media)       │  (Static Assets)        │
└────────────────┴─────────────────────────┘
```

### Multi-Tenant Architecture

The Hairline platform implements a **logical multi-tenant architecture** where all tenants (Patient, Provider, Admin) share the same database and infrastructure but are isolated through:

1. **Authentication Guards**: Separate auth guards for `api` (admin/users), `provider`, and `patient`
2. **Middleware**: Role-based access control enforces tenant boundaries
3. **API Routing**: Separate route groups with distinct prefixes and middleware
4. **Data Scoping**: Query scopes ensure users only access their authorized data

**Rationale**: Logical multi-tenancy is chosen over physical isolation to:

- Reduce infrastructure costs and complexity
- Simplify cross-tenant analytics and reporting
- Enable easier data migrations and backups
- Maintain consistency across tenants

---

## Core Workflow Implementation

### Quote & Booking Status Flow

Quote status, booking status, and case stages are separate enums and MUST NOT be merged (`system-data-schema.md`).

**Flow**:

```sh
Inquiry → Quote (sent) → Subquote accepted → Booking: Accepted (slot held) → Confirmed (first payment) → In Progress → Aftercare → Completed
                                                       ↘ Payment Window Expired (hold lapsed before first payment)
Any booking state after acceptance → Cancelled (admin-only, with reason; inquiry Cancelled, quote stays accepted)
Accepted, Confirmed → Cancelled (provider fault, suspension or deactivation)
In Progress + provider fault, suspension or deactivation → stays In Progress (supportRequired) → admin: Aftercare with aftercare-provider reassignment, or Cancelled with reason
```

**Quote Status (FR-004)**: `draft`, `sent`, `expired`, `withdrawn`, `archived`, `accepted`, `cancelled_other_accepted`, `cancelled_inquiry_cancelled`, `cancelled_provider_status`. `confirmed` is not a quote status; booking confirmation is an FR-006 booking status. A sent parent quote carries one to five Quote Options; each option/date-price row is a subquote, and the patient accepts exactly one subquote per inquiry.

**Booking Status (FR-006)**:

- `Accepted`: Patient accepted one subquote (FR-005). The booking links to the AcceptanceEvent and the appointment slot is held, not booked. No manual provider confirmation is needed (provider receives a notification only).
- `Payment Window Expired`: The slot hold lapsed before the first payment step succeeded.
- `Confirmed`: First payment step (deposit or first installment) succeeded; the appointment record is created and the slot is blocked; patient details are revealed to the provider (anonymization lifted).
- `In Progress`: Patient arrives at clinic, treatment in progress (provider can update real-time progress).
- `Aftercare`: Treatment completed, aftercare phase active (6-12 months recovery).
- `Completed`: Final review and rating submitted by patient.
- `Cancelled`: Closed with a recorded cancellation cause. The patient can cancel only while the inquiry is in Inquiry or Quoted; after acceptance the patient contacts support. Only an admin can cancel a booking after acceptance, from any booking state, with a mandatory reason and an audit entry; the inquiry moves to Cancelled and the accepted quote stays `accepted`. A provider fault, suspension, or deactivation cancels an `Accepted` or `Confirmed` booking with cause `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated`. In `In Progress` the booking is not cancelled automatically: it stays `In Progress` with `supportRequired`, and an admin either moves it to `Aftercare` and reassigns the aftercare provider, or cancels it with a mandatory reason. In `Aftercare` the booking is not cancelled; an admin reassigns the aftercare provider.

**Critical Business Logic**:

1. **Auto-Accept and Slot Hold**: When the patient accepts a subquote, the system records an append-only AcceptanceEvent with an immutable acceptance snapshot, sets the booking to `Accepted`, and places one exclusive slot hold keyed by provider, appointment date/time, and time zone. A unique index on that active hold key allows one active booking per slot, so a concurrent second acceptance fails and the patient is told the slot was just taken. Acceptance holds the slot only; no appointment is created and the calendar is not blocked at acceptance (provider receives notification only).
2. **Fixed Hold and First Payment**: The hold lasts for the FR-026 slot-hold duration (default 48 hours) from acceptance and is fixed: payment failure or retry never extends or restarts it. On successful first payment (deposit or first installment) the booking moves to `Confirmed`, the appointment record is created, and the held slot becomes a calendar block. A "hold expiring soon" reminder is sent at the FR-026 lead time.
3. **Payment Window Expired**: A scheduled job moves an `Accepted` booking whose hold has lapsed to `Payment Window Expired`: the hold is released, payment against that accepted selection is rejected, the AcceptanceEvent and snapshot stay unchanged, the parent quote and accepted subquote are not reopened, and patient and provider are notified. This applies only to the first payment step; a missed later installment or final payment never causes `Payment Window Expired` or inquiry cancellation (FR-007, FR-007B).
4. **Admin Revive**: An admin may move a `Payment Window Expired` booking back to `Accepted` only with a mandatory reason. The system re-checks that the slot (provider, appointment date/time, time zone) is free, takes the promotion use again when the accepted promotion has a usage limit (for an automatic promotion only if the limit still has room, because the accepted price includes the promotion), and rejects the revive if either check fails. On success a new hold of the FR-026 slot-hold duration starts at the revive time. The action is audited.
5. **Anonymization Control**:
   - Before `Confirmed`: Provider sees "Mark P. - PAT-00123" (anonymized)
   - After first payment (`Confirmed`): Provider sees full name, contact details, passport information
6. **Quote Expiration and Configuration Read**: At first send the system copies the quote expiry (default 48 hours) and the quote currency read-only from the active FR-026 quote configuration and records that configuration's version on the quote; drafts carry neither. If the FR-026 configuration cannot be read, first send is blocked and the draft is kept unchanged. Later setting changes never affect a sent quote. A Default Currency change creates a new quote-configuration version, so the recorded version identifies both the hours and the currency. A draft that already holds prices switches to the new currency with its prices kept as typed, and send is blocked until the provider acknowledges a "currency changed, check your prices" banner. Every option/date-price row must have a price greater than 0 before send; a date range the clinic cannot serve is left out of that option. `first_sent_at` is set once at first send and never changed by a re-send, and TTFQ ends at the `first_sent_at` of the provider's earliest parent quote for the inquiry.
7. **Quote Option Aggregate (FR-004)**: The quote is the parent aggregate; the acceptance unit is one `quote_option_date_prices` row, not the quote itself. Until acceptance a quote has a price range rather than an amount, so quote-amount analytics MUST read the accepted option/date price only and MUST count an unaccepted quote in volume and conversion metrics only. Quote Options are never counted as separate provider responses.
8. **Multiple Quotes per Inquiry**: One provider may submit several parent quotes for the same inquiry, each with an independent lifecycle, expiry, version, and audit history. `(inquiry_id, provider_id)` MUST NOT be treated as unique.
9. **Acceptance Snapshot as Source of Truth (FR-005)**: Price after promotion, currency, date range, appointment, and promotion are the binding money fields. Booking, payment, commission, and every other downstream service read them from the acceptance snapshot (or the booking money fields copied from it), never from the live quote, option, or date-price rows. The exchange rate and its timestamp are locked at acceptance and stored in the snapshot. The snapshot's appointment is the accepted baseline: an admin appointment change moves the booking's current appointment and never edits the snapshot, and booking notices read the booking's current appointment.
10. **Provider-Status Cancellation Cascade (FR-015, FR-006)**: When a provider suspension or deactivation becomes effective, the system cancels that provider's `Accepted` (including unpaid within the hold) and `Confirmed` bookings and its standalone aftercare, and hands those bookings to the FR-006 Alternative Flow B5 admin transfer; the inquiry stays open. An `In Progress` booking is not cancelled automatically: it stays `In Progress` with `supportRequired`, and an admin decides the case on the FR-006 intervention screen (move to `Aftercare` with aftercare-provider reassignment, or cancel with a mandatory reason). An `Aftercare` booking is not cancelled: the booking and treatment record stay, `supportRequired` is set, and an admin reassigns the aftercare provider with a reason and an audit entry; the reassignment sends the mandatory `aftercare.provider_reassigned` to the patient and the new aftercare provider. Each cancelled booking, standalone aftercare record and provider inquiry participation stores the cancellation cause (`ProviderSuspended` or `ProviderDeactivated`), the provider status event reference, its effective time, and the prior stage, and sets an independent boolean `supportRequired` marker (not a status). Any active hold or calendar block is released. Only the provider's unaccepted parent quotes move to `cancelled_provider_status` (displayed "Cancelled (Provider Status)" and shown to the patient as "Offer Unavailable") with the cause in `cancellationProvenance`; an accepted quote keeps `accepted`. `supportRequired` is cleared only by an audited admin resolution (resolution reason, admin, timestamp). An earlier `ProviderSuspended` cause is never overwritten by a later deactivation, and reactivation restores nothing. Field-level storage: `system-data-schema.md` §5, §7, §11A, §13.
11. **Provider-Fault Transfer (FR-006)**: When the provider withdraws or drops out after acceptance, or a suspension or deactivation takes effect, an `Accepted` or `Confirmed` booking is cancelled with the matching cause and `supportRequired`, and the inquiry stays open. A transfer to a replacement provider is available only for bookings cancelled in `Accepted` or `Confirmed`. A provider fault in `In Progress` leaves the booking `In Progress` with `supportRequired`; it is not cancelled automatically, no replacement acceptance is created, and an admin either moves it to `Aftercare` and reassigns the aftercare provider or cancels it with a mandatory reason. A provider fault in `Aftercare` is handled by reassigning the aftercare provider instead. For a transfer, an admin authors a replacement quote in the same inquiry on behalf of the replacement provider, linked to the original AcceptanceEvent. No automatic promotion attaches to the replacement quote and no promotion use is reserved for it; the admin sets the replacement price directly, and the original acceptance's promotion use is returned or kept under the normal rules. A replacement quote that is not accepted expires normally; the inquiry stays `supportRequired` and is not cancelled automatically, and the admin may author another replacement quote or cancel the inquiry and booking. When that replacement quote is accepted, the system creates a new admin-authored acceptance record and, in the same transaction, inserts one supersession record linking the original acceptance to the replacement; the original AcceptanceEvent is never edited, and no supersession record exists for a cancellation that is never replaced. The replacement booking is created from the new acceptance. The patient re-enters nothing. Money mechanics are defined in FR-007, FR-007B, and FR-017.
12. **Provider Eligibility Revalidation**: Provider status MUST be `active` at inquiry allocation, quote submission, quote acceptance, and the booking-confirming payment; each step rejects a suspended or deactivated provider.
13. **Commission Model (FR-029, FR-015)**: Provider commission is either Percentage (0-100%) of the booking total or Flat Rate (fixed amount > 0, in an enabled currency) deducted once per FR-010 completed procedure. The booking total is the accepted subquote price after promotion, in the quote currency, read from the acceptance snapshot; commission uses it for every discount type, including Hairline-funded discounts, and the deposit percentage and instalment amounts use the same booking total. The global default is percentage-only within 15-25%. At booking confirmation the booking snapshots commission model, value, and Flat Rate currency, together with the deposit and installment settings; payouts and analytics read that snapshot, never the provider's current settings.
14. **Promotion Use Reservations (FR-019, FR-004, FR-005)**: Promotion programs and codes are stored in `promotion_programs` and `promotion_codes`; the legacy `discounts` table is not used for them. At most one automatic promotion attaches to a quote, chosen in priority order: provider discount, then Hairline-funded promotion, then affiliate; a patient-entered code takes priority over all of them at acceptance. An automatically applied promotion reserves one use per sent parent quote in `promotion_use_reservations`; if the promotion's usage limit is already full, the promotion does not attach and the send proceeds without it; a re-send of a new version keeps the reservation, creates one only if the new version newly qualifies, and releases it if the new version no longer carries the promotion. The reservation is released when the quote expires, is withdrawn, is not selected, or is cancelled before acceptance because the inquiry was cancelled or the provider's status changed (release reason `cancelled`), and at acceptance is consumed if the accepted row carries the promotion or released with reason `not_applied` if it does not, so the usage limit is never exceeded. If the booking ends in `Payment Window Expired` or is cancelled before the first payment, the use returns to the limit; an admin revive takes it again only if the limit has room, otherwise the revive is rejected. Provider-selected promotions and patient codes reserve one use at acceptance and consume it at the first successful payment. An admin-authored replacement quote never carries an automatic promotion and never takes a reservation. Field-level storage: `system-data-schema.md`.
15. **Acceptance Notifications (FR-030, FR-020)**: At acceptance the patient receives only `booking.scheduled` ("Booking Accepted — Slot Held (Pending Payment)"), which is mandatory, goes to the patient only, and also fires at the acceptance of an admin-authored replacement quote; the provider learns of the acceptance through `quote.accepted`, whose outcomes go to providers only. `booking.rescheduled` is mandatory and goes to the patient and the provider when an admin changes the appointment (FR-006); it shows the booking's current appointment. `aftercare.provider_reassigned` (FR-011) is mandatory and goes to the patient and the new aftercare provider when an admin reassigns the aftercare provider; no admin alert is sent because the admin is the actor. Admins receive no per-acceptance alert, only exception alerts (hold expiring soon while unpaid, `Payment Window Expired`, provider fault, and `quote.withdrawn` after acceptance). `quote.cancelled_inquiry` is mandatory with no provider toggle. FR-004 emits `quote.updated` (quote revised, new version) when a new version of a sent quote is re-sent.
16. **Treatment-Detail Changes (FR-010)**: The treatment record is created at booking confirmation (first successful payment) with status `Awaiting Check In`; its statuses are Awaiting Check In, In Progress (set at Check In), Completed, and Cancelled. Treatment details are locked while the booking is `Accepted` (unpaid). From `Confirmed`, the clinic may change treatment plan days, clinicians, or estimated grafts until Check In, and an admin may change them at any time from `Confirmed` onward, each with a mandatory reason; each change is audited, emits the mandatory `treatment.plan_changed`, and never changes the acceptance snapshot or money fields.
17. **Travel Records (FR-008)**: The itinerary is a read view assembled from the travel context, flight and hotel records, and the booking; there is no stored itineraries table. A return flight or hotel check-out before the last treatment plan day raises a soft warning that must be acknowledged; the record can still be saved and the provider sees the flag. In a provider-fault transfer the passport carries to the replacement booking, flights and hotel are copied with `travel_date_review_required` set, and the originals stay read-only on the closed booking.
18. **Currency Disable Guard (FR-029)**: A currency cannot be disabled while any non-terminal sent quote, unpaid accepted booking, or open booking or instalment plan uses it; the admin sees the count of records still using it.
19. **Price Sort Across Currencies (FR-005, FR-022)**: Price sort converts each price to the patient's display currency at the current rate for ordering only; each card shows its own quote currency, and the ordering is labelled approximate when currencies are mixed.

### Payment Processing Architecture

**Installment Payment System**:

```php
// Read binding money fields from the booking (copied read-only from the FR-005
// acceptance snapshot) and the AcceptanceEvent, never from live
// quote/option/date-price rows.
// Instalment arithmetic below is unchanged and pending the payment review.
$acceptance = $booking->acceptanceEvent;
$bookingTotal = $booking->booking_total; // accepted price after promotion, in $booking->currency
// Procedure date comes from the booking's current appointment (moved by an admin
// appointment change), not from the acceptance snapshot.
$procedureDate = Carbon::parse($booking->hold_appointment_at, $booking->hold_appointment_timezone);

// Calculate available installments
$daysUntilProcedure = now()->diffInDays($procedureDate);
$maxInstallments = floor(($daysUntilProcedure - 30) / 30); // 30-day buffer

// Create installment plan
$plan = InstallmentPaymentPlan::create([
    'quote_id' => $acceptance->accepted_parent_quote_id,
    'total_amount' => $bookingTotal,
    'currency' => $booking->currency, // quote currency from the acceptance snapshot
    'exchange_rate' => $acceptance->exchange_rate, // locked at acceptance
    'number_of_installments' => min($selectedInstallments, $maxInstallments),
    'installment_amount' => $bookingTotal / $selectedInstallments,
    'final_payment_date' => $procedureDate->subDays(30)
]);
```

**Medical Alert System**:

```php
// Classify medical conditions
$alertLevel = 'none'; // green
if ($hasAllergies || $hasMedications) {
    $alertLevel = 'standard'; // yellow/amber
}
if ($hasHIV || $hasBloodDisorder || $hasHeartCondition) {
    $alertLevel = 'critical'; // red
    $requiresAcknowledgment = true;
}

MedicalHistory::create([
    'critical_conditions' => $criticalConditions,
    'alert_level' => $alertLevel
]);
```

**Package Structure** (Quote Options from versioned package templates, FR-004 and FR-024):

```php
// Each Quote Option copies one versioned library package template (packages carry
// no currency). Inline edits change only this quote's copy and never write back
// to the library or create a package version.
$option = $quote->options()->create([
    'source_package_id' => $package->id,
    'source_package_version' => $package->version,
    'package_name_snapshot' => $package->name,
    'standard_price_snapshot' => $package->standard_price,
    'is_customized' => $inlineEdited,
    'display_order' => $order, // one to five options per parent quote
]);

// Prices live on option/date-price rows (subquotes) in the quote currency;
// the patient accepts exactly one row.
$option->datePrices()->create([
    'source_inquiry_date_range_id' => $range->id,
    'start_date' => $range->start_date, // copied from the selected inquiry range
    'end_date' => $range->end_date,
    'appointment_at' => $appointmentAt,
    'appointment_timezone' => $timezone,
    'price' => $offeredPrice,
]);
```

### Provider Lifecycle & Admin Controls (FR-015 v1.9)

- **Status**: `active`, `suspended`, `deactivated` only; there is no `draft` provider status. Suspension and deactivation trigger the cancellation cascade above and automatically clear the `featured` flag.
- **Creation fields**: `payout_frequency` (`weekly`, `twice_monthly`, `monthly`) is required at creation; `commission_start_date` is today or later; commission model and value per the Commission Model rule above. Clinic name is 3-200 characters and the contact email is unique.
- **Provider documents**: `document_type` is one of `medical_license`, `board_certification`, `insurance`, `malpractice_insurance`, `business_license`, `other`; upload validation accepts PDF, JPG, PNG, DOCX, XLSX. Each document records `uploader_type` (`provider` or `admin`) and `uploader_id`; `notes` are admin-only; deletion is a soft delete.
- **Retention**: data of a deactivated provider is retained for at least 7 years and then archived; provider records are never hard-deleted.
- **Audit**: every admin edit of provider data requires a change reason stored in the audit log. Login as Provider sessions are audited (reason, admin re-authentication, 30-minute session timeout).
- **Notification events (FR-020)**: `provider.suspended`, `provider.deactivated`, `provider.status_cancellation_patient` (affected patient), and `provider.status_cancellation_admin_support` (admin support queue for `supportRequired` cases).

---

## Backend Architecture

### Framework & Structure

**Laravel Application Structure**:

```sh
hairline-backend/
├── app/
│   ├── Console/           # Scheduled tasks, commands
│   ├── Events/            # Event classes (e.g., QuoteSubmitted)
│   ├── Exceptions/        # Custom exception handlers
│   ├── Http/
│   │   ├── Controllers/   # API controllers organized by domain
│   │   │   ├── Authentication/
│   │   │   ├── Patients/
│   │   │   ├── Providers/
│   │   │   ├── Quotes/
│   │   │   ├── Inquiry/
│   │   │   ├── Analytics/
│   │   │   └── ...
│   │   ├── Middleware/    # Custom middleware
│   │   └── Requests/      # Form request validation
│   ├── Jobs/              # Queued jobs (e.g., SendQuoteNotification)
│   ├── Mail/              # Email templates
│   ├── Models/            # Eloquent models (75+ models)
│   ├── Notifications/     # Notification classes
│   ├── Observers/         # Model observers for audit trails
│   ├── Providers/         # Service providers
│   ├── Rules/             # Custom validation rules
│   └── Services/          # Business logic services
├── config/                # Configuration files
├── database/
│   ├── factories/         # Model factories for testing
│   ├── migrations/        # Database migrations (116 files)
│   └── seeders/           # Database seeders
├── routes/
│   ├── api.php            # API routes (primary)
│   ├── web.php            # Web routes (minimal)
│   └── channels.php       # Broadcast channels
├── storage/               # Logs, cache, uploads
├── tests/                 # PHPUnit tests
└── vendor/                # Composer dependencies
```

### API Design Principles

#### RESTful Conventions

All APIs follow REST principles:

- **Resources**: Nouns in plural form (`/patients`, `/quotes`, `/providers`)
- **HTTP Methods**: GET (read), POST (create), PUT/PATCH (update), DELETE (delete)
- **Status Codes**: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 422 (Validation Error), 500 (Server Error)
- **Versioning**: URL-based versioning (e.g., `/api/v1/patients`, `/api/v2/patients`)

#### Response Format

**Success Response**:

```json
{
  "status": "success",
  "message": "Resource retrieved successfully",
  "data": {
    "id": "uuid-here",
    "attribute": "value"
  }
}
```

**Collection Response**:

```json
{
  "status": "success",
  "message": "Resources retrieved successfully",
  "data": [...],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total": 150,
    "last_page": 8
  }
}
```

**Error Response**:

```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": {
    "email": ["The email field is required."],
    "password": ["The password must be at least 8 characters."]
  }
}
```

#### Authentication

**OAuth 2.0 via Laravel Passport**:

1. **Password Grant** (Patient/Provider login):

   ```json
   POST /api/auth/login
   {
     "email": "user@example.com",
     "password": "password123"
   }
   
   Response:
   {
     "access_token": "eyJ0eXAiOiJKV1...",
     "token_type": "Bearer",
     "expires_in": 86400
   }
   ```

2. **Authorization Header**:

   ```sh
   Authorization: Bearer eyJ0eXAiOiJKV1...
   ```

3. **Token Expiration**: 24 hours for patients, 7 days for providers
4. **Refresh Token**: Supported for extending sessions without re-login

**Guard Configuration**:

```php
// config/auth.php
'guards' => [
    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],
    'patient' => [
        'driver' => 'passport',
        'provider' => 'patients',
    ],
    'provider' => [
        'driver' => 'passport',
        'provider' => 'provider_users',
    ],
],
```

#### Authorization (RBAC)

**Spatie Laravel Permission** package used for role and permission management:

**Roles**:

- **Admin Roles**: `super_admin`, `admin`, `support`
- **Provider Roles**: `provider_owner`, `provider_admin`, `provider_doctor`, `provider_coordinator`
- **Patient Role**: `patient` (default)

**Permissions**:

- Pattern: `{action}_{resource}` (e.g., `create_quote`, `view_patient`, `manage_billing`)
- Assigned to roles, not individual users
- Middleware: `permission:create_quote` or `role:provider_owner`

**Implementation Example**:

```php
// Route middleware
Route::middleware(['auth:provider', 'permission:create_quote'])
    ->post('/quote/create-quote', [QuotesController::class, 'store']);

// Controller check
if (!$user->can('view_patient', $patient)) {
    abort(403, 'Unauthorized action');
}
```

### Database Design

#### Connection Configuration

```php
// config/database.php
'mysql' => [
    'driver' => 'mysql',
    'host' => env('DB_HOST', '127.0.0.1'),
    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'hairline'),
    'username' => env('DB_USERNAME', 'root'),
    'password' => env('DB_PASSWORD', ''),
    'charset' => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'strict' => true,
    'engine' => 'InnoDB',
],
```

#### UUID Primary Keys

All user-facing entities use UUIDs as primary keys for:

- **Security**: Prevents enumeration attacks
- **Scalability**: Enables distributed ID generation
- **Privacy**: Obscures record counts

**Implementation**:

```php
// Model trait
use App\Models\Traits\HasUuid;

class Patient extends Authenticatable
{
    use HasUuid;
    
    protected $keyType = 'string';
    public $incrementing = false;
}

// Trait implementation
trait HasUuid
{
    protected static function boot()
    {
        parent::boot();
        static::creating(function ($model) {
            if (empty($model->{$model->getKeyName()})) {
                $model->{$model->getKeyName()} = (string) Str::uuid();
            }
        });
    }
}
```

#### Soft Deletes

Critical entities use soft deletes to:

- Maintain data integrity for audit trails
- Enable data recovery
- Comply with healthcare data retention regulations

**Models with Soft Deletes**:

- `Patient`, `Provider`, `ProviderUser`, `Treatment`, `AfterCare`, `Affiliate`

`Inquiry` and `Quote` are not soft-deleted. An inquiry is closed by moving it to `cancelled`, and its rows are retained because acceptance and booking records reference it. A quote is retained in the same way: once an acceptance record references a quote, the quote is retained permanently and cannot be deleted.

```php
use Illuminate\Database\Eloquent\SoftDeletes;

class Patient extends Authenticatable
{
    use SoftDeletes;
    
    protected $dates = ['deleted_at'];
}

// Query excluding soft-deleted
$patients = Patient::all(); // excludes deleted

// Query including soft-deleted
$patients = Patient::withTrashed()->get();

// Query only soft-deleted
$patients = Patient::onlyTrashed()->get();
```

#### Indexing Strategy

**Primary Indexes**:

- Primary keys (UUIDs)
- Foreign keys
- Unique constraints (email, username, patient_code)

**Secondary Indexes**:

```sql
-- Performance-critical queries
CREATE INDEX idx_quotes_status ON quotes(status);
CREATE INDEX idx_quotes_provider_id ON quotes(provider_id);
CREATE INDEX idx_patients_location_id ON patients(location_id);
CREATE INDEX idx_inquiries_created_at ON inquiries(created_at);

-- Composite indexes
CREATE INDEX idx_quotes_provider_status ON quotes(provider_id, status);
CREATE INDEX idx_quotes_inquiry_provider ON quotes(inquiry_id, provider_id);

-- Quote option aggregate (FR-004 v2.2)
CREATE INDEX idx_quote_options_quote_id ON quote_options(quote_id);
CREATE UNIQUE INDEX idx_quote_options_order ON quote_options(quote_id, display_order);
CREATE INDEX idx_quote_option_items_option ON quote_option_items(quote_option_id);
CREATE INDEX idx_qodp_option ON quote_option_date_prices(quote_option_id);
CREATE UNIQUE INDEX idx_qodp_option_range ON quote_option_date_prices(quote_option_id, source_inquiry_date_range_id);
CREATE UNIQUE INDEX idx_qopd_option_day ON quote_option_plan_days(quote_option_id, day_number);
```

**Note**: `idx_quotes_inquiry_provider` is a lookup index only — it MUST NOT be made unique, because one provider may submit multiple parent quotes for the same inquiry.

#### Database Migrations

**Migration Naming Convention**:

- `YYYY_MM_DD_HHMMSS_action_table_name.php`
- Examples: `2024_02_18_044253_create_inquiries_table.php`

**Migration Best Practices**:

1. **Atomic Changes**: One schema change per migration
2. **Reversible**: Always implement `down()` method
3. **Data Migrations**: Separate from schema migrations
4. **Foreign Keys**: Defined with explicit ON DELETE rules; quotes and acceptance records use RESTRICT and are never cascade-deleted

```php
// Example migration
Schema::create('quotes', function (Blueprint $table) {
    $table->uuid('id')->primary();
    $table->uuid('inquiry_id');
    $table->uuid('provider_id');
    $table->uuid('treatment_id');
    // No quote amount: prices live on quote_option_date_prices rows
    $table->string('currency')->nullable(); // copied at first send from FR-026
    $table->string('status');
    $table->timestamps();
    
    // Restrict, never cascade: accepted quotes referenced by acceptance
    // records are retained (see system-data-schema.md, Foreign Key Constraints)
    $table->foreign('inquiry_id')
          ->references('id')
          ->on('inquiries')
          ->onDelete('restrict');
    
    // Indexes
    $table->index(['provider_id', 'status']);
});
```

**Quote aggregate migration (FR-004 v2.2)**: The option model is additive. New migrations create `quote_options`, `quote_option_items`, `quote_option_date_prices`, and `quote_option_plan_days` (see `system-data-schema.md` §7A-§7D). A data migration converts each existing quote into a one-option quote seeded from `quotes.package_id`, `quotes.treatment_date`, and `quotes.quote_amount`. Those three columns are deprecated and stay readable through a compatibility adapter until every consumer moves to the option contract (CR-FR004-20260909-01); they are not dropped in the same release.

### Business Logic Layer

#### Service Classes

Complex business logic is abstracted into service classes to:

- Keep controllers thin and focused on HTTP concerns
- Enable code reuse across controllers
- Simplify testing

**Service Example**:

```php
// app/Services/QuoteService.php
namespace App\Services;

class QuoteService
{
    public function createQuote(Inquiry $inquiry, Provider $provider, array $data)
    {
        // Validate provider can quote on inquiry
        if (!$this->canProviderQuote($provider, $inquiry)) {
            throw new UnauthorizedException('Provider cannot quote on this inquiry');
        }
        
        // Create the parent quote as a draft. NOTE (FR-004): `quote_amount` is
        // deprecated — price lives on each option/date combination and an accepted
        // amount only exists after FR-005 selection. No commission is set on the
        // quote: the binding commission snapshot is captured on the booking at
        // booking confirmation (FR-029).
        $quote = Quote::create([
            'inquiry_id' => $inquiry->id,
            'provider_id' => $provider->id,
            'status' => 'draft', // FR-004 quote status
            ...
        ]);
        
        // Attach one to five quote options, each a quote-local package snapshot
        // (never writes back to the FR-024 package library), with its option/date
        // price matrix and relative-day plan
        $this->attachQuoteOptions($quote, $data['options']);
        
        $this->sendQuote($quote);
        
        return $quote;
    }
    
    public function sendQuote(Quote $quote)
    {
        // First send copies expiry and currency read-only from the active FR-026
        // quote configuration and records its version; never provider input. If
        // the configuration cannot be read, first send is blocked and the draft is
        // kept unchanged.
        $config = $this->quoteConfiguration->current(); // throws when unreadable
        $now = now();
        
        $quote->update([
            'status' => 'sent', // exposed as `quote` through the API
            'currency' => $config->default_currency,
            'expiration_hours' => $config->expiration_hours,
            'quote_config_version' => $config->version,
            'expires_at' => $now->copy()->addHours($config->expiration_hours),
            'sent_at' => $now,
            'first_sent_at' => $quote->first_sent_at ?? $now, // set once at first send; a re-send keeps it; TTFQ ends here
        ]);
        
        // Send notification to patient
        event(new QuoteSubmitted($quote));
    }
}

// Controller usage
class QuotesController extends Controller
{
    protected $quoteService;
    
    public function __construct(QuoteService $quoteService)
    {
        $this->quoteService = $quoteService;
    }
    
    public function store(Request $request)
    {
        $quote = $this->quoteService->createQuote(
            $inquiry, 
            $provider, 
            $request->validated()
        );
        
        return response()->json(['data' => $quote], 201);
    }
}
```

#### Model Observers

Observers handle side effects of model events (creating, updating, deleting):

```php
// app/Observers/QuoteObserver.php
class QuoteObserver
{
    public function created(Quote $quote)
    {
        // Log to workflow timeline
        WorkflowTimeline::create([
            'inquiry_id' => $quote->inquiry_id,
            'event' => 'quote_submitted',
            'metadata' => ['quote_id' => $quote->id]
        ]);
        
        // Update patient status
        $quote->inquiry->patient->updateStatus();
    }
    
    public function updated(Quote $quote)
    {
        // Track status changes
        if ($quote->isDirty('status')) {
            WorkflowTimeline::create([
                'inquiry_id' => $quote->inquiry_id,
                'event' => 'quote_status_changed',
                'metadata' => [
                    'quote_id' => $quote->id,
                    'old_status' => $quote->getOriginal('status'),
                    'new_status' => $quote->status
                ]
            ]);
        }
    }
}

// Register observer in AppServiceProvider
public function boot()
{
    Quote::observe(QuoteObserver::class);
}
```

### Queue System

#### Job Queue Configuration

**Queue Driver**: Redis (production), Database (local development)

**Queue Names**:

- `default`: Low priority jobs (email notifications, analytics)
- `high`: High priority jobs (payment processing, booking confirmations)
- `notifications`: Push notifications and SMS
- `media`: Image/video processing, 3D scan processing

```php
// config/queue.php
'connections' => [
    'redis' => [
        'driver' => 'redis',
        'connection' => 'default',
        'queue' => env('REDIS_QUEUE', 'default'),
        'retry_after' => 90,
        'block_for' => null,
    ],
],
```

#### Job Examples

```php
// app/Jobs/SendQuoteNotification.php
class SendQuoteNotification implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;
    
    public $tries = 3;
    public $timeout = 60;
    
    protected $quote;
    
    public function __construct(Quote $quote)
    {
        $this->quote = $quote;
    }
    
    public function handle()
    {
        // Send email
        Mail::to($this->quote->inquiry->patient->email)
            ->send(new QuoteReceived($this->quote));
        
        // Send push notification
        $this->quote->inquiry->patient->notify(
            new NewQuoteNotification($this->quote)
        );
    }
    
    public function failed(Throwable $exception)
    {
        // Handle job failure
        Log::error('Quote notification failed', [
            'quote_id' => $this->quote->id,
            'error' => $exception->getMessage()
        ]);
    }
}

// Dispatch job
SendQuoteNotification::dispatch($quote)->onQueue('notifications');
```

### Caching Strategy

#### Cache Driver: Redis

**Cache Keys Naming Convention**: `{entity}:{id}:{attribute}`

Examples:

- `provider:abc123:profile`
- `patient:def456:inquiries`
- `quote:ghi789:details`

#### Caching Patterns

**1. Query Result Caching**:

```php
// Cache expensive queries
$providers = Cache::remember('providers:active:turkey', 3600, function () {
    return Provider::where('country', 'Turkey')
                   ->where('status', 'active')
                   ->with('languages', 'awards')
                   ->get();
});
```

**2. Model Caching**:

```php
// Cache model attributes
public function getProfileAttribute()
{
    return Cache::remember("provider:{$this->id}:profile", 3600, function () {
        return [
            'name' => $this->provider_name,
            'bio' => $this->provider_bio,
            'rating' => $this->averageRating(),
            'procedures_count' => $this->treatmentsCount()
        ];
    });
}
```

**3. Cache Invalidation**:

```php
// Model observer for cache invalidation
class ProviderObserver
{
    public function updated(Provider $provider)
    {
        Cache::forget("provider:{$provider->id}:profile");
        Cache::forget("providers:active:{$provider->country}");
    }
}
```

**4. Cache Tags** (for grouped invalidation):

```php
// Cache with tags
Cache::tags(['providers', 'turkey'])->put('providers:turkey:active', $providers, 3600);

// Flush all provider caches
Cache::tags('providers')->flush();
```

### File Storage

#### Storage Configuration

**Driver**: AWS S3 (production), Local (development)

**S3 Bucket Structure**:

```sh
hairline-storage/
├── patients/
│   ├── {patient_id}/
│   │   ├── profile/
│   │   │   └── avatar.jpg
│   │   ├── scans/
│   │   │   ├── {inquiry_id}_scan.obj
│   │   │   └── {inquiry_id}_scan_preview.jpg
│   │   └── aftercare/
│   │       ├── milestone_1week.jpg
│   │       ├── milestone_1month.jpg
│   │       └── milestone_3months.jpg
├── providers/
│   ├── {provider_id}/
│   │   ├── profile/
│   │   ├── credentials/
│   │   ├── before_after/
│   │   └── facility/
├── treatments/
│   ├── {treatment_id}/
│   │   ├── before/
│   │   ├── during/
│   │   └── after/
└── public/
    ├── logos/
    └── banners/
```

**File Upload Example**:

```php
// Controller
public function uploadScan(Request $request)
{
    $request->validate([
        'scan' => 'required|file|mimes:obj,fbx|max:50000', // 50MB
    ]);
    
    $path = $request->file('scan')->storeAs(
        "patients/{$patient->id}/scans",
        "{$inquiry->id}_scan.obj",
        's3'
    );
    
    // Generate signed URL (expires in 24 hours)
    $url = Storage::disk('s3')->temporaryUrl($path, now()->addDay());
    
    return response()->json(['url' => $url]);
}
```

**Image Optimization**:

```php
// Use Intervention Image for processing
use Intervention\Image\Facades\Image;

public function uploadPhoto(Request $request)
{
    $image = Image::make($request->file('photo'))
                  ->resize(1200, null, function ($constraint) {
                      $constraint->aspectRatio();
                  })
                  ->encode('jpg', 85);
    
    $path = "patients/{$patient->id}/aftercare/" . Str::random(40) . '.jpg';
    Storage::disk('s3')->put($path, $image);
}
```

### Real-Time Features

#### Broadcasting with Laravel Reverb

**Configuration**:

```php
// config/broadcasting.php
'connections' => [
    'reverb' => [
        'driver' => 'reverb',
        'app_id' => env('REVERB_APP_ID'),
        'app_key' => env('REVERB_APP_KEY'),
        'app_secret' => env('REVERB_APP_SECRET'),
        'host' => env('REVERB_HOST'),
        'port' => env('REVERB_PORT', 8080),
    ],
],
```

**Event Broadcasting**:

```php
// app/Events/MessageSent.php
class MessageSent implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;
    
    public $message;
    
    public function __construct(Message $message)
    {
        $this->message = $message;
    }
    
    public function broadcastOn()
    {
        return new PrivateChannel('conversation.' . $this->message->conversation_id);
    }
    
    public function broadcastWith()
    {
        return [
            'id' => $this->message->id,
            'content' => $this->message->content,
            'sender' => $this->message->sender,
            'created_at' => $this->message->created_at
        ];
    }
}

// Trigger event
event(new MessageSent($message));
```

**Channel Authorization**:

```php
// routes/channels.php
Broadcast::channel('conversation.{conversationId}', function ($user, $conversationId) {
    $conversation = Conversation::find($conversationId);
    
    // Check if user is participant
    return $conversation->participants->contains('id', $user->id);
});
```

---

## Frontend Architecture (Web)

### Framework: React 18 + Vite

**Project Structure**:

```sh
hairline-frontend/
├── public/              # Static assets
├── src/
│   ├── app/
│   │   ├── api/         # RTK Query API slices
│   │   └── store.jsx    # Redux store configuration
│   ├── assets/          # Images, icons, fonts
│   ├── components/
│   │   ├── shared/      # Reusable components
│   │   ├── providerComponents/  # Provider-specific components
│   │   └── teamComponents/      # Admin-specific components
│   ├── features/        # Feature-based modules with Redux slices
│   │   ├── auth/
│   │   ├── hairlineProvider/
│   │   └── hairlineTeam/
│   ├── hooks/           # Custom React hooks
│   ├── pages/           # Page components
│   │   ├── providerDashboard/
│   │   └── teamDashboard/
│   ├── utils/           # Utility functions
│   ├── App.jsx          # Root component
│   └── main.jsx         # Entry point
├── index.html
├── package.json
└── vite.config.js
```

### State Management

**Redux Toolkit** with RTK Query for API calls:

```javascript
// src/app/store.jsx
import { configureStore } from '@reduxjs/toolkit';
import { apiSlice } from './api/apiSlice';
import authReducer from '../features/auth/authSlice';

export const store = configureStore({
  reducer: {
    [apiSlice.reducerPath]: apiSlice.reducer,
    auth: authReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware),
});
```

**API Slice with RTK Query**:

```javascript
// src/app/api/apiSlice.jsx
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL,
    prepareHeaders: (headers, { getState }) => {
      const token = getState().auth.token;
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Patient', 'Provider', 'Quote', 'Inquiry'],
  endpoints: (builder) => ({}),
});
```

**Feature API Slice**:

```javascript
// src/features/hairlineProvider/inquiries/inquiriesApiSlice.jsx
import { apiSlice } from '../../../app/api/apiSlice';

export const inquiriesApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getInquiries: builder.query({
      query: (params) => ({
        url: '/inquiry/get-all-inquiries',
        params,
      }),
      providesTags: ['Inquiry'],
    }),
    getInquiry: builder.query({
      query: (id) => `/inquiry/get-single-inquiry?inquiry_id=${id}`,
      providesTags: (result, error, id) => [{ type: 'Inquiry', id }],
    }),
  }),
});

export const { useGetInquiriesQuery, useGetInquiryQuery } = inquiriesApiSlice;
```

### Routing

**React Router v6**:

```javascript
// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        
        {/* Protected Provider Routes */}
        <Route element={<PrivateRoute allowedRoles={['provider']} />}>
          <Route path="/" element={<ProviderDashboard />}>
            <Route index element={<Dashboard />} />
            <Route path="inquiries" element={<Inquiries />} />
            <Route path="inquiries/:id" element={<InquiriesDetails />} />
            <Route path="appointments/quotes" element={<Quotes />} />
            {/* ... */}
          </Route>
        </Route>
        
        {/* Protected Admin Routes */}
        <Route element={<PrivateRoute allowedRoles={['hairline']} />}>
          <Route path="/hairline-overview/*" element={<HairlineOverview />} />
          {/* ... */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

### UI Component Library

**Ant Design** for consistent UI:

```javascript
import { Table, Button, Modal, Form, Input } from 'antd';

function InquiriesTable() {
  const { data, isLoading } = useGetInquiriesQuery();
  
  const columns = [
    { title: 'Patient', dataIndex: 'patient_name', key: 'patient_name' },
    { title: 'Location', dataIndex: 'location', key: 'location' },
    { title: 'Created', dataIndex: 'created_at', key: 'created_at' },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Button type="primary" onClick={() => viewInquiry(record.id)}>
          View Details
        </Button>
      ),
    },
  ];
  
  return <Table columns={columns} dataSource={data} loading={isLoading} />;
}
```

### Authentication Flow

```javascript
// src/features/auth/authSlice.jsx
import { createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    token: localStorage.getItem('token'),
    profileType: localStorage.getItem('profileType'),
  },
  reducers: {
    setCredentials: (state, action) => {
      const { user, token, profileType } = action.payload;
      state.user = user;
      state.token = token;
      state.profileType = profileType;
      localStorage.setItem('token', token);
      localStorage.setItem('profileType', profileType);
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.profileType = null;
      localStorage.removeItem('token');
      localStorage.removeItem('profileType');
    },
  },
});

export const { setCredentials, logout } = authSlice.actions;
export default authSlice.reducer;
```

### Build Configuration

**Vite Configuration**:

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          antd: ['antd'],
          redux: ['@reduxjs/toolkit', 'react-redux'],
        },
      },
    },
  },
});
```

---

## Mobile Architecture

### Framework Decision: React Native vs Flutter

**Current Status**: To be decided based on:

- Team expertise
- Development timeline
- Performance requirements
- 3D scanning library availability (V2)

**Recommended**: **React Native** for code sharing with web frontend and existing team React expertise

### React Native Architecture (If Selected)

**Project Structure**:

```sh
hairline-mobile/
├── android/           # Android native code
├── ios/               # iOS native code
├── src/
│   ├── api/           # API integration
│   ├── assets/        # Images, fonts
│   ├── components/    # Reusable components
│   ├── navigation/    # React Navigation
│   ├── screens/       # Screen components
│   ├── services/      # Business logic services
│   ├── store/         # Redux store
│   └── utils/         # Utility functions
├── App.tsx
└── package.json
```

### V1: Head Scan Photo Set Capture

**Release scope note**: In V1, "3D scan" capture is implemented as a standardized head scan photo set (multiple 2D views; JPG/PNG). No true 3D model capture/viewing is required for V1.

**Implementation sketch**:

- Guided camera flow captures required viewpoints (e.g., front/top/left/right/back)
- Client uploads multiple images; backend validates file types/size and stores via media service
- Viewer is an image gallery (zoom + compare), not an interactive 3D model viewer

### V2: 3D Scanning Integration (ARKit/ARCore)

**iOS (ARKit)**:

```javascript
import { ARView } from 'react-native-arkit';

function ScanScreen() {
  const onScanComplete = (scanData) => {
    // Process 3D scan data
    uploadScan(scanData);
  };
  
  return (
    <ARView
      onScanComplete={onScanComplete}
      sessionConfiguration="ARFaceTrackingConfiguration"
    />
  );
}
```

**Android (ARCore)**:

```javascript
import { ArCoreView } from 'react-native-arcore';

function ScanScreen() {
  const onScanComplete = (scanData) => {
    uploadScan(scanData);
  };
  
  return (
    <ArCoreView
      onScanComplete={onScanComplete}
      meshingEnabled={true}
    />
  );
}
```

### Offline Support

**AsyncStorage** for local data persistence:

```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';

// Save data offline
await AsyncStorage.setItem('draft_inquiry', JSON.stringify(inquiryData));

// Retrieve when online
const draftData = await AsyncStorage.getItem('draft_inquiry');
if (draftData) {
  const inquiry = JSON.parse(draftData);
  // Submit to server
  submitInquiry(inquiry);
  // Clear cache
  await AsyncStorage.removeItem('draft_inquiry');
}
```

---

## Third-Party Integrations

### Payment Processing (Stripe)

**Setup**:

```php
// config/services.php
'stripe' => [
    'key' => env('STRIPE_KEY'),
    'secret' => env('STRIPE_SECRET'),
],

// Use Stripe PHP SDK
composer require stripe/stripe-php
```

**Payment Intent Flow**:

```php
use Stripe\Stripe;
use Stripe\PaymentIntent;

class PaymentController extends Controller
{
    public function createPaymentIntent(Request $request, Booking $booking)
    {
        // Amount and currency are never taken from the client. The booking must
        // belong to the authenticated patient, and a first payment requires the
        // booking to be `accepted` with an active hold (before `hold_expires_at`).
        abort_unless($booking->patient_id === $request->user()->id, 403);
        if ($booking->status === 'accepted' && now()->gte($booking->hold_expires_at)) {
            abort(409, 'Payment window expired');
        }
        
        Stripe::setApiKey(config('services.stripe.secret'));
        
        // Amount due now (deposit or instalment) is derived server-side from
        // booking_total; the payment rules own the split (FR-007)
        $amountDue = $this->paymentService->amountDueNow($booking);
        
        $paymentIntent = PaymentIntent::create([
            'amount' => (int) round($amountDue * 100), // smallest currency unit
            'currency' => strtolower($booking->currency), // quote currency from the acceptance snapshot
            'payment_method_types' => ['card'],
            'metadata' => [
                'booking_id' => $booking->id,
                'patient_id' => $booking->patient_id,
            ],
        ]);
        
        return response()->json([
            'client_secret' => $paymentIntent->client_secret,
        ]);
    }
    
    public function handleWebhook(Request $request)
    {
        $payload = $request->getContent();
        $sig_header = $request->header('Stripe-Signature');
        $endpoint_secret = config('services.stripe.webhook_secret');
        
        try {
            $event = \Stripe\Webhook::constructEvent(
                $payload, $sig_header, $endpoint_secret
            );
        } catch (\Exception $e) {
            return response()->json(['error' => 'Invalid signature'], 400);
        }
        
        switch ($event->type) {
            case 'payment_intent.succeeded':
                $this->handlePaymentSuccess($event->data->object);
                break;
            case 'payment_intent.payment_failed':
                $this->handlePaymentFailure($event->data->object);
                break;
        }
        
        return response()->json(['status' => 'success']);
    }
}
```

### Email (SendGrid)

```php
// config/mail.php
'sendgrid' => [
    'transport' => 'sendgrid',
    'api_key' => env('SENDGRID_API_KEY'),
],

// Email notification
Mail::to($patient->email)->send(new QuoteReceived($quote));
```

### SMS (Twilio)

```php
use Twilio\Rest\Client;

class SmsService
{
    protected $twilio;
    
    public function __construct()
    {
        $this->twilio = new Client(
            config('services.twilio.sid'),
            config('services.twilio.token')
        );
    }
    
    public function send($to, $message)
    {
        $this->twilio->messages->create($to, [
            'from' => config('services.twilio.from'),
            'body' => $message
        ]);
    }
}

// Usage
$smsService = new SmsService();
$smsService->send('+905551234567', 'Your appointment is confirmed!');
```

### Push Notifications (Firebase)

```php
use Kreait\Firebase\Factory;
use Kreait\Firebase\Messaging\CloudMessage;

class PushNotificationService
{
    protected $messaging;
    
    public function __construct()
    {
        $factory = (new Factory)
            ->withServiceAccount(config('firebase.credentials'));
        
        $this->messaging = $factory->createMessaging();
    }
    
    public function sendToDevice($deviceToken, $title, $body, $data = [])
    {
        $message = CloudMessage::withTarget('token', $deviceToken)
            ->withNotification([
                'title' => $title,
                'body' => $body,
            ])
            ->withData($data);
        
        $this->messaging->send($message);
    }
}
```

### Travel APIs

**Flight Booking (Amadeus API)**:

```php
class FlightService
{
    public function searchFlights($origin, $destination, $date)
    {
        $response = Http::withToken(config('services.amadeus.api_key'))
            ->get('https://api.amadeus.com/v2/shopping/flight-offers', [
                'originLocationCode' => $origin,
                'destinationLocationCode' => $destination,
                'departureDate' => $date,
                'adults' => 1,
            ]);
        
        return $response->json();
    }
}
```

**Hotel Booking (Booking.com Affiliate API)**:

```php
class HotelService
{
    public function searchHotels($city, $checkIn, $checkOut)
    {
        $response = Http::get('https://distribution-xml.booking.com/2.0/json/hotels', [
            'city_ids' => $city,
            'checkin' => $checkIn,
            'checkout' => $checkOut,
            'extras' => 'hotel_info,hotel_photos',
        ]);
        
        return $response->json();
    }
}
```

---

## Security Implementation

### Data Encryption

**At Rest** (Database):

```php
// Model attribute encryption
use Illuminate\Database\Eloquent\Casts\Encrypted;

class Patient extends Model
{
    protected $casts = [
        'medical_history' => Encrypted::class,
        'phone_number' => Encrypted::class,
    ];
}
```

**In Transit** (HTTPS/TLS):

- All API communication over HTTPS (TLS 1.3)
- Nginx SSL configuration with Let's Encrypt certificates

### Input Validation

**Form Request Validation**:

```php
class CreateQuoteRequest extends FormRequest
{
    public function rules()
    {
        return [
            'inquiry_id' => 'required|uuid|exists:inquiries,id',
            'provider_id' => 'required|uuid|exists:providers,id',
            // No quote_amount, currency or treatment_date: currency is copied from
            // the FR-026 quote configuration at first send, and prices live on
            // option/date-price rows.
            'options' => 'required|array|min:1|max:5',
            'options.*.date_prices' => 'required|array|min:1',
            'options.*.date_prices.*.source_inquiry_date_range_id' => 'required|uuid',
            'options.*.date_prices.*.appointment_at' => 'required|date|after:today',
            'options.*.date_prices.*.price' => 'required|numeric|gt:0',
        ];
    }
}
```

### SQL Injection Prevention

- **Eloquent ORM**: Automatic parameter binding prevents SQL injection
- **Raw Queries**: Use parameter binding

```php
// Safe (Eloquent)
$patients = Patient::where('email', $email)->get();

// Safe (Raw query with bindings)
$patients = DB::select('SELECT * FROM patients WHERE email = ?', [$email]);

// UNSAFE (Never do this)
$patients = DB::select("SELECT * FROM patients WHERE email = '$email'");
```

### XSS Prevention

- **Blade Templates**: Automatic escaping with `{{ }}`
- **API Responses**: JSON encoding prevents XSS

```php
// Blade (automatic escaping)
<p>{{ $patient->name }}</p>

// Raw output (only when safe)
<div>{!! $trustedHtmlContent !!}</div>
```

### CSRF Protection

- **Web Forms**: CSRF token validation
- **API**: Not applicable (stateless token-based auth)

### Rate Limiting

```php
// routes/api.php
Route::middleware('throttle:60,1')->group(function () {
    // 60 requests per minute per user
    Route::post('/login', [AuthController::class, 'login']);
});

Route::middleware(['auth:api', 'throttle:100,1'])->group(function () {
    // 100 requests per minute for authenticated users
});
```

### Security Headers

**Nginx Configuration**:

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

---

## Performance Optimization

### Database Query Optimization

**Eager Loading** (N+1 Prevention):

```php
// BAD: N+1 queries
$quotes = Quote::all();
foreach ($quotes as $quote) {
    echo $quote->provider->provider_name; // Each iteration queries DB
}

// GOOD: Eager loading
$quotes = Quote::with('provider', 'inquiry.patient')->get();
foreach ($quotes as $quote) {
    echo $quote->provider->provider_name; // No additional queries
}
```

**Pagination**:

```php
// API pagination
$patients = Patient::paginate(20);

return response()->json([
    'data' => $patients->items(),
    'meta' => [
        'current_page' => $patients->currentPage(),
        'per_page' => $patients->perPage(),
        'total' => $patients->total(),
        'last_page' => $patients->lastPage(),
    ]
]);
```

**Database Indexing**: See Database Design section

### API Response Optimization

**API Resources** (Transform & Hide Sensitive Data):

```php
class PatientResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'name' => $this->first_name . ' ' . $this->last_name,
            'email' => $this->email,
            'location' => $this->location,
            'created_at' => $this->created_at->toDateString(),
            // Hide sensitive fields
        ];
    }
}

// Controller
return PatientResource::collection($patients);
```

### Frontend Performance

**Code Splitting**:

```javascript
// Lazy load routes
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Inquiries = lazy(() => import('./pages/Inquiries'));

<Suspense fallback={<Loading />}>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/inquiries" element={<Inquiries />} />
  </Routes>
</Suspense>
```

**Image Optimization**:

- Use WebP format with JPEG fallback
- Lazy load images below the fold
- Serve responsive images with `srcset`

```javascript
<img 
  src="image.jpg" 
  srcSet="image-320w.jpg 320w, image-640w.jpg 640w, image-1280w.jpg 1280w"
  sizes="(max-width: 320px) 280px, (max-width: 640px) 600px, 1200px"
  loading="lazy"
  alt="Provider facility"
/>
```

---

## Testing Strategy

### Backend Testing (PHPUnit)

**Unit Tests**:

```php
// tests/Unit/QuoteServiceTest.php
class QuoteServiceTest extends TestCase
{
    public function test_percentage_commission_uses_booking_total_after_promotion()
    {
        // Commission is never calculated at quote creation. It is computed from
        // the booking total (accepted price after promotion) and the commission
        // snapshot captured at booking confirmation.
        $booking = Booking::factory()->make([
            'booking_total' => 2700, // 3000 less a 10% promotion
            'commission_model' => 'percentage',
            'commission_value' => 15,
        ]);
        
        $this->assertEquals(405, (new CommissionService())->commissionFor($booking));
    }
}
```

**Feature Tests**:

```php
// tests/Feature/QuoteApiTest.php
class QuoteApiTest extends TestCase
{
    use RefreshDatabase;
    
    public function test_provider_can_create_quote()
    {
        $provider = Provider::factory()->create();
        $inquiry = Inquiry::factory()->create();
        $range = $inquiry->dateRanges()->first();
        $package = Package::factory()->for($provider)->create();
        
        $response = $this->actingAs($provider, 'provider')
            ->postJson('/api/quote/create-quote', [
                'inquiry_id' => $inquiry->id,
                'options' => [[
                    'source_package_id' => $package->id,
                    'date_prices' => [[
                        'source_inquiry_date_range_id' => $range->id,
                        'appointment_at' => '2025-11-01 09:00:00',
                        'price' => 3500,
                    ]],
                ]],
            ]);
        
        $response->assertStatus(201)
                 ->assertJsonStructure(['data' => ['id', 'version', 'status']]);
        
        $this->assertDatabaseHas('quotes', [
            'inquiry_id' => $inquiry->id,
            'provider_id' => $provider->id,
        ]);
    }
}
```

### Frontend Testing

**Component Tests (React Testing Library)**:

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { InquiryCard } from './InquiryCard';

test('displays inquiry details correctly', () => {
  const inquiry = {
    id: '123',
    patient_name: 'John Doe',
    problem: 'Hair Loss',
    created_at: '2025-10-20',
  };
  
  render(<InquiryCard inquiry={inquiry} />);
  
  expect(screen.getByText('John Doe')).toBeInTheDocument();
  expect(screen.getByText('Hair Loss')).toBeInTheDocument();
});

test('navigates to detail page on click', async () => {
  const user = userEvent.setup();
  const mockNavigate = jest.fn();
  
  render(<InquiryCard inquiry={inquiry} onNavigate={mockNavigate} />);
  
  await user.click(screen.getByRole('button', { name: /view details/i }));
  
  expect(mockNavigate).toHaveBeenCalledWith('/inquiries/123');
});
```

**End-to-End Tests (Playwright)**:

```typescript
import { test, expect } from '@playwright/test';

test('provider can create quote for inquiry', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('input[name="email"]', 'provider@test.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  
  // Navigate to inquiries
  await page.click('text=Inquiries');
  await expect(page).toHaveURL('/inquiries');
  
  // Click first inquiry
  await page.click('table >> tr >> nth=1 >> text=View Details');
  
  // Create quote
  await page.click('text=Create Quote');
  // Currency comes from system configuration; the provider prices each option/date-price row
  await page.fill('input[name="options[0][date_prices][0][price]"]', '3500');
  await page.click('button:has-text("Submit Quote")');
  
  // Verify success
  await expect(page.locator('text=Quote submitted successfully')).toBeVisible();
});
```

---

## Deployment

### Environment Configuration

**.env Files**:

```env
# .env.production
APP_ENV=production
APP_DEBUG=false
APP_URL=https://api.hairline.com

DB_HOST=rds-instance.amazonaws.com
DB_DATABASE=hairline_prod
DB_USERNAME=hairline_user
DB_PASSWORD=${DB_PASSWORD_SECRET}

REDIS_HOST=redis-cluster.amazonaws.com

AWS_BUCKET=hairline-production
AWS_DEFAULT_REGION=eu-west-1

STRIPE_KEY=${STRIPE_LIVE_KEY}
STRIPE_SECRET=${STRIPE_LIVE_SECRET}
```

### Docker Configuration

**Dockerfile** (Backend):

```dockerfile
FROM php:8.2-fpm

# Install dependencies
RUN apt-get update && apt-get install -y \
    git curl zip unzip \
    libpng-dev libjpeg-dev libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install pdo pdo_mysql gd

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www

# Copy application
COPY . .

# Install dependencies
RUN composer install --optimize-autoloader --no-dev

# Set permissions
RUN chown -R www-data:www-data /var/www

EXPOSE 9000
CMD ["php-fpm"]
```

**docker-compose.yml**:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./:/var/www
    networks:
      - hairline-network
    environment:
      - DB_HOST=mysql
      - REDIS_HOST=redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./:/var/www
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    networks:
      - hairline-network

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: hairline
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - hairline-network

  redis:
    image: redis:alpine
    networks:
      - hairline-network

networks:
  hairline-network:
    driver: bridge

volumes:
  mysql-data:
```

### CI/CD Pipeline

**GitHub Actions** (Example):

```yaml
name: Deploy Backend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: 8.2
      
      - name: Install dependencies
        run: composer install --prefer-dist --no-dev
      
      - name: Run tests
        run: php artisan test
      
      - name: Build Docker image
        run: docker build -t hairline-backend:${{ github.sha }} .
      
      - name: Push to ECR
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
          docker tag hairline-backend:${{ github.sha }} $ECR_REGISTRY/hairline-backend:latest
          docker push $ECR_REGISTRY/hairline-backend:latest
      
      - name: Deploy to ECS
        run: aws ecs update-service --cluster hairline --service backend --force-new-deployment
```

---

## Monitoring & Logging

### Application Logging

**Laravel Log Channels**:

```php
// config/logging.php
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['daily', 'slack'],
    ],
    'daily' => [
        'driver' => 'daily',
        'path' => storage_path('logs/laravel.log'),
        'level' => 'debug',
        'days' => 14,
    ],
    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'level' => 'error',
    ],
],
```

**Structured Logging**:

```php
Log::info('Quote created', [
    'quote_id' => $quote->id,
    'provider_id' => $quote->provider_id,
    'version' => $quote->version,
    'status' => $quote->status,
]);

Log::error('Payment failed', [
    'payment_intent_id' => $paymentIntent->id,
    'error' => $exception->getMessage(),
    'patient_id' => $patient->id,
]);
```

### Error Tracking

**Sentry Integration**:

```php
// config/sentry.php
'dsn' => env('SENTRY_LARAVEL_DSN'),
'environment' => env('APP_ENV'),

// Automatic error reporting
if ($exception instanceof \Exception) {
    app('sentry')->captureException($exception);
}
```

### Performance Monitoring

**Laravel Telescope** (Development):

```bash
composer require laravel/telescope --dev
php artisan telescope:install
```

**New Relic** (Production):

- APM for backend performance monitoring
- Real User Monitoring (RUM) for frontend

---

## Appendix

### API Endpoint Reference

See separate API documentation: `local-docs/project-requirements/api-specs/`

### Database Schema

See separate schema document: `local-docs/project-requirements/system-data-schema.md`

### Environment Variables

Complete list maintained in: `.env.example`

### Third-Party Service Credentials

Stored in secure secret management system (AWS Secrets Manager, HashiCorp Vault)

---

### Document Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1.0 | 2026-10-14 | Vân Tay Media | Aligned with FR-015 v1.9 verification decisions and FR-029 flat-rate commission: provider-status cancellation cascade, `supportRequired` marker, eligibility revalidation, commission model snapshot, provider lifecycle and admin controls, FR-020 provider status notification events |
| 1.1.1 | 2026-10-14 | Vân Tay Media | Provider commission settings stored in `provider_commissions` (schema §2B), flat model named `flat_rate` |
| 1.2.0 | 2026-10-16 | Vân Tay Media | MTG-002 quote model alignment (S5-2, S5-3, S5-4, S5-6, S5-7; decisions D1, D2, D6, D12, D17, D23, D24, M2, M3): split quote and booking status enums and removed `confirmed` as a quote status; acceptance holds the slot (fixed FR-026 hold keyed by provider, appointment date/time, and time zone) and the appointment is created and the slot blocked only at first payment; added `Payment Window Expired` (first payment only) and audited admin revive; provider-fault transfer via linked admin-authored acceptance record with inquiry kept open; downstream services read the acceptance snapshot; FX locked at acceptance; FR-026 configuration read at first send with outage blocking first send; instalment example reads `bookings.booking_total` and AcceptanceEvent appointment fields per the final schema; package example uses versioned templates and Quote Options; quote migration, validation, feature-test and logging examples no longer carry provider-supplied amount, currency or treatment date |
| 1.3.0 | 2026-10-16 | Vân Tay Media | Product Owner Q-series alignment (Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q10, Q11, Q12, Q14, Q15, Q17, Q18, Q21, Q23, Q24, Q25, Q29, Q30; Q26 and Q27 deferred to the payment pass): active-hold unique index with "slot just taken" message; admin revive retakes an automatic promotion use only if the limit has room; Default Currency change creates a new quote-configuration version with a draft acknowledgement banner; option/date-price rows require price greater than 0 (validation `gt:0`); TTFQ ends at `first_sent_at`; commission, deposit and instalments share one booking total after promotion for every discount type (unit test corrected); new rules for promotion use reservations, acceptance notifications, treatment-detail lock and audited changes, travel records, currency disable guard and approximate cross-currency price sort |
| 1.4.0 | 2026-10-18 | Vân Tay Media | 2026-10-18 consolidated verification corrections (Q15, Q33; D4, D11, D12, M2, M5; no Change Request, system document): promotion reservation also released with reason `cancelled` when the quote is cancelled before acceptance, and admin revive takes an automatic promotion use again only if the limit has room, otherwise rejected; `Quote` removed from soft-delete models and the quotes migration sample uses RESTRICT on `inquiry_id`; QuoteService sample creates a draft without commission and captures currency, expiry, configuration version, `sent_at` and `first_sent_at` at first send; commission unit test moved to the booking total and booking commission snapshot; Stripe PaymentIntent sample checks booking ownership and the active hold and takes amount and currency from the booking, never the client; instalment sample reads the booking's current appointment and stores currency and exchange rate; package sample reads `standard_price` and copies `start_date` and `end_date` to the date-price row. Final audit corrections (Q31, Q35 to Q44; f1 F5; f2 F2, F4, F5; f3 F5; f4 F13; f5 F4; no Change Request, system document): booking flow and `Cancelled` status show the cancellation exits (patient cancels only in Inquiry or Quoted; after acceptance only an admin cancels, from any booking state, the inquiry becomes Cancelled and the quote stays accepted); provider-status cascade and provider-fault transfer limited to Accepted, Confirmed and In Progress bookings, with transfer only for Accepted and Confirmed and aftercare provider reassignment in Aftercare; replacement quote authored by an admin and a single supersession record inserted at the replacement acceptance; one automatic promotion per quote in priority order, limit-full sends proceed without the promotion, release reason `not_applied`, storage in `promotion_programs` and `promotion_codes`; `booking.scheduled` is patient-only and also fires at the replacement acceptance, new `booking.rescheduled` for patient and provider, `quote.withdrawn` after acceptance added to admin exception alerts; treatment-detail changes by the clinic until Check In and by an admin at any time from Confirmed; `Inquiry` removed from the soft-delete list; QuoteService keeps `first_sent_at` on re-send; header version and change log aligned; round-2 additions (Q45 to Q49, Q42 check): a provider fault, suspension, or deactivation on an In Progress booking keeps it In Progress with `supportRequired` for an admin decision (Aftercare with aftercare-provider reassignment, or cancellation with reason) instead of cancelling it; treatment record created at confirmation in Awaiting Check In; new mandatory `aftercare.provider_reassigned` for patient and new aftercare provider; no automatic promotion or reservation on an admin-authored replacement quote; an unaccepted replacement quote expires normally with the inquiry staying support-required; booking notices read the current appointment while the snapshot keeps the accepted baseline |

---

**Document Status**: ✅ Complete  
**Next Steps**: Create Data Schema document  
**Maintained By**: Technical Team  
**Review Cycle**: Quarterly or upon major architectural changes
