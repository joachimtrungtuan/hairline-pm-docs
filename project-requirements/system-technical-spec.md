# Hairline Platform - Technical Specification

**Version**: 1.0.0  
**Document Type**: System-Level Technical Specification  
**Created**: 2025-10-23  
**Status**: Active  
**Last Updated**: 2025-10-23

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
- 3D Scanning: ARKit (iOS), ARCore (Android)

**Infrastructure**:

- Cloud Provider: AWS (or GCP)
- Container Orchestration: Docker + Kubernetes (future)
- CDN: CloudFront
- Storage: S3 (media files, 3D scans)

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
│ - Booking Service   │                  │ - 3D Scan Processor │
│ - Payment Service   │                  │ - Travel API        │
│ - Aftercare Service │                  └─────────────────────┘
│ - Provider Service  │
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

**Status Progression**:

```sh
Inquiry → Quote → Accepted → Confirmed → In Progress → Aftercare → Completed
```

**Status Definitions**:

- `inquiry`: Patient inquiry submitted, waiting for provider quotes
- `quote`: Quote submitted by provider with pre-scheduled appointment times (expires in 48 hours by default)
- `accepted`: Patient accepted quote → appointment auto-scheduled (no manual provider confirmation)
- `confirmed`: Payment completed → patient details revealed to provider (anonymization lifted)
- `inprogress`: Patient arrives at clinic, treatment in progress (provider can update real-time progress)
- `aftercare`: Treatment completed, aftercare phase active (6-12 months recovery)
- `completed`: Final review and rating submitted by patient

**Critical Business Logic**:

1. **Auto-Accept**: When patient accepts quote, status immediately changes to `accepted` and appointment is confirmed (provider receives notification only)
2. **Anonymization Control**:
   - Before `confirmed`: Provider sees "Mark P. - PAT-00123" (anonymized)
   - After payment (`confirmed`): Provider sees full name, contact details, passport information
3. **Quote Expiration**: Configurable per admin settings (default 48 hours)

### Payment Processing Architecture

**Installment Payment System**:

```php
// Calculate available installments
$procedureDate = $quote->treatment_date;
$daysUntilProcedure = now()->diffInDays($procedureDate);
$maxInstallments = floor(($daysUntilProcedure - 30) / 30); // 30-day buffer

// Create installment plan
$plan = InstallmentPaymentPlan::create([
    'quote_id' => $quote->id,
    'total_amount' => $quote->quote_amount,
    'number_of_installments' => min($selectedInstallments, $maxInstallments),
    'installment_amount' => $quote->quote_amount / $selectedInstallments,
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

**Package Structure** (Base + Add-ons):

```php
// Quote composition
$quote = Quote::create([
    'base_package_id' => $basePackage->id,
    'base_amount' => $basePackage->price
]);

// Add selected add-ons
$quote->addons()->attach([
    $hotelAddon->id => ['amount' => 500],
    $transportAddon->id => ['amount' => 100]
]);

$quote->quote_amount = $quote->base_amount + $quote->addons->sum('amount');
```

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

- `Patient`, `Provider`, `ProviderUser`, `Inquiry`, `Quote`, `Treatment`, `AfterCare`, `Affiliate`

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
```

#### Database Migrations

**Migration Naming Convention**:

- `YYYY_MM_DD_HHMMSS_action_table_name.php`
- Examples: `2024_02_18_044253_create_inquiries_table.php`

**Migration Best Practices**:

1. **Atomic Changes**: One schema change per migration
2. **Reversible**: Always implement `down()` method
3. **Data Migrations**: Separate from schema migrations
4. **Foreign Keys**: Defined with cascade rules

```php
// Example migration
Schema::create('quotes', function (Blueprint $table) {
    $table->uuid('id')->primary();
    $table->uuid('inquiry_id');
    $table->uuid('provider_id');
    $table->uuid('treatment_id');
    $table->decimal('quote_amount', 10, 2);
    $table->string('currency');
    $table->string('status');
    $table->timestamps();
    
    // Foreign keys with cascade
    $table->foreign('inquiry_id')
          ->references('id')
          ->on('inquiries')
          ->onDelete('cascade');
    
    // Indexes
    $table->index(['provider_id', 'status']);
});
```

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
        
        // Calculate pricing
        $pricing = $this->calculateQuotePricing($data);
        
        // Create quote
        $quote = Quote::create([
            'inquiry_id' => $inquiry->id,
            'provider_id' => $provider->id,
            'quote_amount' => $pricing['total'],
            'commission' => $pricing['commission'],
            'status' => 'quote',
            ...
        ]);
        
        // Attach package items
        $this->attachPackageItems($quote, $data['package_items']);
        
        // Send notification to patient
        event(new QuoteSubmitted($quote));
        
        return $quote;
    }
    
    private function calculateQuotePricing(array $data)
    {
        // Business logic for pricing calculation
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
- 3D scanning library availability

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

### 3D Scanning Integration

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
    public function createPaymentIntent(Request $request)
    {
        Stripe::setApiKey(config('services.stripe.secret'));
        
        $paymentIntent = PaymentIntent::create([
            'amount' => $request->amount * 100, // Convert to cents
            'currency' => $request->currency,
            'payment_method_types' => ['card'],
            'metadata' => [
                'quote_id' => $request->quote_id,
                'patient_id' => $request->patient_id,
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
            'quote_amount' => 'required|numeric|min:0|max:100000',
            'currency' => 'required|in:USD,EUR,GBP,TRY',
            'treatment_date' => 'required|date|after:today',
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
    public function test_calculate_quote_pricing()
    {
        $service = new QuoteService();
        
        $pricing = $service->calculateQuotePricing([
            'base_price' => 3000,
            'graft_count' => 2500,
            'discount_percentage' => 10,
        ]);
        
        $this->assertEquals(2700, $pricing['total']);
        $this->assertEquals(450, $pricing['commission']);
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
        
        $response = $this->actingAs($provider, 'provider')
            ->postJson('/api/quote/create-quote', [
                'inquiry_id' => $inquiry->id,
                'quote_amount' => 3500,
                'currency' => 'USD',
                'treatment_date' => ['2025-11-01', '2025-11-02'],
            ]);
        
        $response->assertStatus(201)
                 ->assertJsonStructure(['data' => ['id', 'quote_amount']]);
        
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
  await page.fill('input[name="quote_amount"]', '3500');
  await page.selectOption('select[name="currency"]', 'USD');
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
    'amount' => $quote->quote_amount,
    'currency' => $quote->currency,
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

**Document Status**: ✅ Complete  
**Next Steps**: Create Data Schema document  
**Maintained By**: Technical Team  
**Review Cycle**: Quarterly or upon major architectural changes
