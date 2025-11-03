# Inquiry Creation API Compliance Analysis

**Date**: 2025-11-03  
**Endpoint**: `POST /api/inquiry/create-inquiry`  
**PRD Reference**: FR-003: Inquiry Submission & Distribution Module  
**Status**: ⚠️ **PARTIAL COMPLIANCE** - Critical gaps identified

---

## Executive Summary

The inquiry creation API endpoint (`store` method in `InquiryController.php`) has **partial compliance** with the PRD requirements. While it implements most core data fields, there are **critical missing features** and **validation gaps** that need to be addressed before the feature can be considered production-ready.

### Compliance Score: 65/100

**Breakdown:**

- ✅ Core fields implemented: 12/19 (63%)
- ❌ Critical missing features: 2/2 (0%)
- ⚠️ Validation gaps: 7/9 (22%)
- ⚠️ Business rule compliance: 3/6 (50%)

---

## 1. Data Fields Compliance

### ✅ Implemented Fields

| PRD Requirement | API Implementation | Status | Notes |
|----------------|-------------------|--------|-------|
| **Treatment Type** | `problem` (hair/beard/both) | ✅ Complete | Validated with enum values |
| **3D Head Scan** | `scan_file` (file upload) | ✅ Complete | Required field, stores to `scan_url` |
| **Treatment Schedule** | `treatment_schedule` (JSON) | ✅ Complete | Accepts JSON, but validation needed |
| **Problem Details** | `problem_details` (text) | ✅ Complete | Required field |
| **Nature of Concern** | `nature_of_concern` (string) | ✅ Complete | Optional field |
| **Duration of Concern** | `duration_of_concern` (string) | ✅ Complete | Optional field |
| **Previous Treatments** | `previous_treatments` (string) | ✅ Complete | Optional field |
| **Symptom Severity** | `symptom_severity` (string) | ⚠️ Partial | Should be numeric 1-10, currently string |
| **Lifestyle Factors** | `lifestyle_factors` (string) | ✅ Complete | Optional field |
| **Additional Notes** | `additional_notes` (string) | ✅ Complete | Optional field |
| **Medical History** | `medical_history` (JSON) | ✅ Complete | Required, stored in MedicalHistory table |
| **Preferred Providers** | `providers` (JSON array) | ✅ Complete | Optional, max validation needed |

### ❌ Missing Critical Fields

| PRD Requirement | Status | Impact | Priority |
|----------------|--------|--------|----------|
| **Countries/Destinations Selection** | ❌ Missing | CRITICAL | P0 - Required for distribution logic |
| **Budget Range** | ❌ Missing | HIGH | P1 - Required per system-prd.md |
| **Service Type Selection** | ❌ Missing | MEDIUM | P2 - Secondary service options (Monitor Hair Loss, Aftercare) |
| **Terms & Conditions Acceptance** | ❌ Missing | MEDIUM | P1 - Legal requirement |

### ⚠️ Incomplete/Partial Implementation

| Field | Issue | PRD Requirement | Current Implementation |
|-------|-------|----------------|----------------------|
| **Visual Evidence** | Only single file | Max 5 photos/videos | Only `additional_file` (singular) |
| **Symptom Severity** | Type mismatch | Numeric 1-10 slider | Stored as string |
| **Treatment Schedule** | No validation | Max 10 date ranges, up to 2 years | JSON accepted without validation |

---

## 2. Validation & Business Rules Compliance

### ❌ Missing Validations

#### 2.1 Visual Evidence Validation

**PRD Requirement:**

- Max 5 files total (photos/videos combined)
- Photos: JPG/PNG ≤ 2MB each
- Videos: MP4 ≤ 30s, ≤ 20MB each

**Current Status:** ❌ No validation

- Only supports single `additional_file`
- No file type validation
- No file size validation
- No duration validation for videos

**Required Fix:**

```php
'additional_files' => 'nullable|array|max:5',
'additional_files.*' => 'file|mimes:jpg,jpeg,png,mp4|max:20480', // 20MB in KB
// Need custom validation for video duration (30s max)
```

#### 2.2 Treatment Schedule Validation

**PRD Requirement:**

- Max 10 date ranges
- Up to 2 years in the future
- Non-overlapping ranges
- Minimum 30 days from inquiry date

**Current Status:** ❌ No validation

- Accepts JSON without structure validation
- No date range count validation
- No future date limit validation
- No overlap validation

**Required Fix:**

```php
'treatment_schedule' => [
    'required',
    'json',
    function ($attribute, $value, $fail) {
        $schedules = json_decode($value, true);
        // Validate max 10 ranges
        // Validate 2 years future limit
        // Validate non-overlapping
        // Validate minimum 30 days
    },
],
```

#### 2.3 Countries/Destinations Validation

**PRD Requirement:**

- Max 10 countries selectable

**Current Status:** ❌ Field missing entirely

**Required Fix:**

- Add `countries` or `destinations` field (JSON array)
- Validate max 10 items
- Validate country IDs exist in locations table

#### 2.4 Providers Validation

**PRD Requirement:**

- Max 5 providers

**Current Status:** ⚠️ Partial

- Accepts JSON array
- No max count validation in controller

**Required Fix:**

```php
'providers' => 'nullable|json|max_providers:5', // Custom rule needed
```

#### 2.5 Budget Range Validation

**PRD Requirement:**

- Budget range (min-max in preferred currency)

**Current Status:** ❌ Field missing entirely

**Required Fix:**

- Add `budget_min` and `budget_max` fields
- Add `budget_currency` field
- Validate min < max
- Validate currency code

#### 2.6 Symptom Severity Validation

**PRD Requirement:**

- Numeric value 1-10

**Current Status:** ⚠️ Stored as string, no validation

**Required Fix:**

```php
'symptom_severity' => 'nullable|integer|min:1|max:10',
```

#### 2.7 3D Scan File Validation

**PRD Requirement:**

- Must be valid 3D scan file
- Quality validation

**Current Status:** ⚠️ Partial

- File upload validated
- No format validation (should accept specific 3D formats)
- No quality validation

**Required Fix:**

```php
'scan_file' => 'required|file|mimes:obj,gltf,glb,ply|max:50000', // Add appropriate 3D formats
```

---

## 3. Business Logic Compliance

### ✅ Implemented Features

| Feature | Status | Notes |
|---------|--------|-------|
| Inquiry creation workflow | ✅ Complete | Creates inquiry with timeline entry |
| Medical history storage | ✅ Complete | Stores in separate MedicalHistory table |
| Provider assignment | ✅ Complete | Links to InquiryProvider table |

### ❌ Missing Business Logic

| Feature | PRD Requirement | Status | Impact |
|---------|----------------|--------|--------|
| **Inquiry Distribution** | Auto-distribute to providers in selected countries OR explicitly selected | ❌ Missing | CRITICAL - Core workflow |
| **Inquiry ID Generation** | HPID format (HPID + YY + MM + 4-digit sequence) | ❌ Missing | HIGH - Tracking requirement |
| **One Active Inquiry Rule** | Patient can only have one active inquiry | ❌ Not enforced | MEDIUM - Business rule |
| **Draft Inquiry Support** | Auto-save drafts, expire after 7 days | ❌ Missing | LOW - Enhancement |
| **Terms Acceptance** | Must accept T&C before submission | ❌ Missing | MEDIUM - Legal requirement |

---

## 4. Database Schema Compliance

### Current Schema Issues

#### 4.1 Missing Columns

```php
// Required additions to inquiries table:
$table->json('countries')->nullable(); // Selected countries/locations
$table->decimal('budget_min', 10, 2)->nullable();
$table->decimal('budget_max', 10, 2)->nullable();
$table->string('budget_currency', 3)->nullable(); // ISO currency code
$table->string('service_type')->default('hair_transplant'); // Service type selection
$table->boolean('terms_accepted')->default(false);
$table->string('inquiry_code')->unique(); // HPID format
$table->json('visual_evidence')->nullable(); // Array of file paths
```

#### 4.2 Data Type Issues

```php
// Current:
$table->string('symptom_severity')->nullable();

// Should be:
$table->tinyInteger('symptom_severity')->nullable()->unsigned(); // 1-10

// Current:
$table->string('additional_files')->nullable(); // Only stores one file

// Should be:
$table->json('visual_evidence')->nullable(); // Array of file paths
```

---

## 5. API Endpoint Structure Analysis

### Current Request Structure

```php
POST /api/inquiry/create-inquiry
Content-Type: multipart/form-data

Fields:
- patient_id (required, uuid)
- problem (required, enum: hair|beard|both)
- scan_file (required, file)
- treatment_schedule (required, json)
- problem_details (required, string)
- medical_history (required, json)
- providers (nullable, json)
- nature_of_concern (nullable, string)
- duration_of_concern (nullable, string)
- previous_treatments (nullable, string)
- symptom_severity (nullable, string) ❌ Should be integer
- lifestyle_factors (nullable, string)
- additional_file (nullable, file) ❌ Should support multiple files
- additional_notes (nullable, string)
```

### Required Request Structure (PRD Compliant)

```php
POST /api/inquiry/create-inquiry
Content-Type: multipart/form-data

Required Fields:
- patient_id (required, uuid)
- problem (required, enum: hair|beard|both)
- service_type (required, enum: hair_transplant|monitor_hair_loss|aftercare)
- scan_file (required, file)
- treatment_schedule (required, json) // Max 10 ranges, validated
- problem_details (required, string)
- medical_history (required, json)
- countries (required, json array) // Max 10 countries ❌ MISSING
- budget_min (nullable, decimal) ❌ MISSING
- budget_max (nullable, decimal) ❌ MISSING
- budget_currency (nullable, string) ❌ MISSING
- terms_accepted (required, boolean) ❌ MISSING
- nature_of_concern (required, string) // Should be required per PRD
- duration_of_concern (required, string) // Should be required per PRD
- previous_treatments (required, string) // Should be required per PRD
- symptom_severity (required, integer, 1-10) // Should be required and integer
- lifestyle_factors (nullable, string)
- visual_evidence (nullable, array of files) // Max 5 files ❌ MISSING
- additional_notes (nullable, string)
- providers (nullable, json array) // Max 5 providers, needs validation
```

---

## 6. Critical Issues Summary

### P0 - Critical (Must Fix Before Production)

1. **❌ Countries/Destinations Selection Missing**
   - **Impact**: Cannot implement inquiry distribution logic
   - **Required**: Add `countries` field (JSON array, max 10 items)
   - **Effort**: Medium (requires DB migration + validation)

2. **❌ No Inquiry Distribution Logic**
   - **Impact**: Core feature non-functional
   - **Required**: Implement distribution to providers in selected countries
   - **Effort**: High (requires new service/controller logic)

### P1 - High Priority (Should Fix Before Production)

3. **❌ Budget Range Missing**
   - **Impact**: Required per system-prd.md
   - **Required**: Add budget_min, budget_max, budget_currency fields
   - **Effort**: Low (DB migration + validation)

4. **❌ Multiple Visual Evidence Not Supported**
   - **Impact**: Users can only upload 1 file instead of 5
   - **Required**: Change to array support, add file validation
   - **Effort**: Medium (validation logic + file handling)

5. **❌ Treatment Schedule Validation Missing**
   - **Impact**: Invalid data can be submitted
   - **Required**: Validate max 10 ranges, 2-year future limit, non-overlapping
   - **Effort**: Medium (custom validation rule)

6. **❌ Inquiry ID Generation Missing (HPID Format)**
   - **Impact**: Tracking and reference issues
   - **Required**: Generate HPID format (HPID + YY + MM + 4-digit sequence)
   - **Effort**: Low (add to model/controller)

### P2 - Medium Priority (Can Fix in Next Sprint)

7. **⚠️ Symptom Severity Type Mismatch**
   - **Issue**: Stored as string, should be integer 1-10
   - **Required**: Change to integer with validation
   - **Effort**: Low (DB migration + validation)

8. **❌ Terms & Conditions Acceptance Missing**
   - **Impact**: Legal compliance issue
   - **Required**: Add terms_accepted boolean field
   - **Effort**: Low (DB field + validation)

9. **❌ One Active Inquiry Rule Not Enforced**
   - **Impact**: Business rule violation
   - **Required**: Check for existing active inquiry before creation
   - **Effort**: Low (add validation check)

10. **⚠️ Required Field Mismatch**
    - **Issue**: PRD states nature_of_concern, duration_of_concern, previous_treatments, symptom_severity should be required
    - **Current**: All marked as nullable
    - **Required**: Update validation rules
    - **Effort**: Low (validation update)

---

## 7. Recommendations

### Immediate Actions (P0)

1. **Add Countries/Destinations Field**
   - Create migration to add `countries` JSON column
   - Add validation for max 10 countries
   - Update API documentation

2. **Implement Inquiry Distribution Logic**
   - Create `InquiryDistributionService`
   - Distribute to providers in selected countries
   - Include explicitly selected providers
   - Send notifications (if notification system exists)

3. **Add Inquiry ID Generation**
   - Implement HPID format generation
   - Add `inquiry_code` unique column
   - Generate on inquiry creation

### Short-term Actions (P1 - Next Sprint)

4. **Fix Visual Evidence Support**
   - Change `additional_file` to `visual_evidence` array
   - Implement file validation (type, size, duration)
   - Update database schema

5. **Add Budget Range Fields**
   - Create migration for budget fields
   - Add validation (min < max, valid currency)
   - Update API documentation

6. **Implement Treatment Schedule Validation**
   - Create custom validation rule
   - Validate structure, count, dates, overlaps
   - Return clear error messages

7. **Fix Symptom Severity Type**
   - Migrate existing string data to integer
   - Update validation to integer 1-10
   - Update model fillable array

### Medium-term Actions (P2 - Future Sprints)

8. **Add Service Type Selection**
   - Add `service_type` field
   - Support secondary services (Monitor Hair Loss, Aftercare)
   - Update workflow logic

9. **Implement Terms & Conditions**
   - Add `terms_accepted` field
   - Require acceptance before submission
   - Store acceptance timestamp

10. **Add Draft Inquiry Support**
    - Implement auto-save functionality
    - Add draft expiration logic (7 days)
    - Create resume workflow

---

## 8. Testing Recommendations

### Unit Tests Needed

1. **Validation Tests**
   - Test max 10 countries validation
   - Test max 5 providers validation
   - Test max 10 date ranges validation
   - Test visual evidence file validation (type, size, count)

2. **Business Logic Tests**
   - Test inquiry distribution logic
   - Test HPID generation format
   - Test one active inquiry rule
   - Test treatment schedule validation (overlaps, future dates)

### Integration Tests Needed

1. **API Endpoint Tests**
   - Test complete inquiry creation flow
   - Test with all required fields
   - Test with missing required fields
   - Test file upload handling

2. **Database Tests**
   - Test inquiry creation with relationships
   - Test medical history storage
   - Test provider assignment

---

## 9. API Documentation Updates Needed

The current Swagger/OpenAPI documentation in the controller needs updates:

1. **Add Missing Fields**
   - `countries` (required, JSON array)
   - `budget_min`, `budget_max`, `budget_currency`
   - `terms_accepted` (required, boolean)
   - `service_type` (required, enum)
   - `visual_evidence` (array of files, max 5)

2. **Update Field Types**
   - `symptom_severity`: Change from string to integer
   - `visual_evidence`: Change from single file to array

3. **Add Validation Rules**
   - Document all validation rules
   - Document business rules (max counts, date limits)

---

## 10. Migration Path

### Phase 1: Critical Fixes (Week 1)

1. Add countries field and validation
2. Implement inquiry distribution logic
3. Add HPID generation

### Phase 2: High Priority (Week 2)

1. Add budget range fields
2. Fix visual evidence support
3. Implement treatment schedule validation
4. Fix symptom severity type

### Phase 3: Medium Priority (Week 3-4)

1. Add service type selection
2. Add terms & conditions
3. Enforce one active inquiry rule
4. Update required field validations

---

## Conclusion

The inquiry creation API endpoint has a **solid foundation** but requires **significant enhancements** to fully comply with the PRD requirements. The most critical gaps are:

1. **Missing countries/destinations selection** (blocks distribution logic)
2. **Missing budget range** (required by system PRD)
3. **Incomplete visual evidence support** (only 1 file vs. 5 required)
4. **Missing validation rules** (allows invalid data)

**Estimated effort to achieve full compliance: 2-3 weeks** (assuming 1 developer, full-time focus)

**Recommendation**: Address P0 and P1 issues before releasing to production. P2 issues can be handled in subsequent releases.
