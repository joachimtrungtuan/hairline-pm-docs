# Hairline Mobile App - Comprehensive Testing Plan

**Version**: 1.0
**Created**: 2026-01-27
**Purpose**: Manual & Usability Testing for Pre-Release Approval
**Scope**: Patient-facing mobile app (iOS/Android)
**Testing Focus**: End-to-end flows, UX/UI, error scenarios, edge cases

---

## Executive Summary

This testing plan provides a comprehensive, end-to-end manual testing strategy for the Hairline mobile app from the patient perspective. The goal is to:

1. **Verify implementation** matches PRD requirements and client specifications
2. **Identify gaps, bugs, and UX issues** before official release
3. **Ensure smooth user experience** for complex multi-step workflows
4. **Test error-prone scenarios** (technical and usability)
5. **Foundation for progress reporting** - detect missing/incomplete features

**Testing Philosophy**: Focus on real-world user scenarios, not just happy paths. Test as if you are a patient with limited technical knowledge.

---

## Testing Methodology

### Test Execution Strategy

1. **Test on both platforms**: iOS and Android (different OS versions if possible)
2. **Test with real data**: Use realistic patient information, not dummy data
3. **Document everything**: Screenshots, screen recordings, detailed notes
4. **Report issues immediately**: Categorize by severity (Critical, High, Medium, Low)
5. **Test in sequence**: Follow the patient journey chronologically
6. **Re-test fixes**: Verify bug fixes don't introduce new issues

### Issue Severity Levels

- **Critical**: App crashes, data loss, security vulnerabilities, payment failures
- **High**: Feature doesn't work as specified, major UX issues, blocking user progress
- **Medium**: Minor functional issues, confusing UI, missing validation
- **Low**: Cosmetic issues, minor text errors, nice-to-have improvements

---

## Pre-Testing Checklist

Before starting testing, ensure:

- [ ] Latest app build installed on test devices (iOS & Android)
- [ ] Test accounts created (patient accounts with different profiles)
- [ ] Backend services are running and accessible
- [ ] Payment gateway configured for test mode
- [ ] Access to admin panel for verification
- [ ] Screen recording tools ready
- [ ] Note-taking app/spreadsheet prepared for issue tracking
- [ ] Network simulation tools available (for connectivity testing)

---

## Test Scenarios by Module

## Module 1: Authentication & Profile Management (FR-001)

**Reference**: `local-docs/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`

### 1.1 New User Registration (Critical Path)

**Objective**: Verify patients can successfully create accounts via mobile app

**Test Steps**:

1. **App Launch**
   - [ ] Launch app on clean install
   - [ ] Verify splash screen displays with Hairline branding (max 3 seconds)
   - [ ] Verify landing screen appears with "Get Started" button
   - [ ] Verify "Already have an account? Get Started" link visible

2. **Name Collection**
   - [ ] Tap "Get Started"
   - [ ] Verify "First, tell us your name" screen displays
   - [ ] Test validation: Try submitting with empty fields
   - [ ] Test validation: Try 1-character names (should fail - min 2 chars)
   - [ ] Test validation: Try 51+ character names (should fail - max 50 chars)
   - [ ] Enter valid first and last name
   - [ ] Verify "Continue" button enables when both fields valid
   - [ ] Verify back navigation works

3. **Email & Password Creation**
   - [ ] Verify "Let's create an account with your email" screen displays
   - [ ] Test email validation: Try invalid email formats
   - [ ] Test email validation: Try duplicate email (if possible)
   - [ ] Test password strength: Try weak passwords (should fail)
   - [ ] Verify password requirements shown clearly (12+ chars, 1 upper, 1 lower, 1 digit, 1 special from !@#$%^&(),.?":{}|<>)
   - [ ] Test password mismatch: Different confirm password
   - [ ] Enter valid email and strong password
   - [ ] Verify password visibility toggle works
   - [ ] Verify "Create account" button enables when all fields valid
   - [ ] Verify Terms of Service and Privacy Policy links work

4. **Email Verification (OTP)**
   - [ ] Tap "Create account"
   - [ ] Verify OTP sent to email within 30 seconds
   - [ ] Verify "Enter verification code" screen displays with 6 input boxes
   - [ ] Test invalid OTP: Enter wrong code
   - [ ] Test expired OTP: Wait 15+ minutes, then try code
   - [ ] Verify "Resend code" link available
   - [ ] Test resend with rate limiting
   - [ ] Enter correct 6-digit OTP
   - [ ] Verify OTP auto-validates and proceeds

5. **Profile Completion**
   - [ ] Verify "Create your profile" screen displays
   - [ ] Test gender selection (Male, Female, Other, Prefer not to say)
   - [ ] Test date of birth picker:
     - [ ] Try selecting age under 18 (should fail - min age 18)
     - [ ] Try selecting age over 100 (should fail - max age 100)
     - [ ] Select valid DOB (18-100 years)
   - [ ] Test phone number input:
     - [ ] Verify country code dropdown works
     - [ ] Try invalid phone format
     - [ ] Enter valid phone with country code
   - [ ] Test country selection:
     - [ ] Verify country list displays
     - [ ] Search for country
     - [ ] Select country
   - [ ] Verify all fields required before "Create account" enables
   - [ ] Tap "Create account"

6. **Discovery Question**
   - [ ] Verify "How did you find out about us?" screen displays
   - [ ] Verify dropdown shows centrally-managed options
   - [ ] Select an option
   - [ ] Verify "Continue" proceeds to main app

**Expected Results**:

- Account created successfully
- User redirected to main app dashboard
- Profile complete and accessible
- All validation messages clear and helpful

**Error-Prone Areas to Watch**:

- OTP delivery delays (email server issues)
- Password validation edge cases
- Country code/phone number validation
- Age validation (18-100 years)
- Back navigation data persistence

---

### 1.2 User Login (Critical Path)

**Test Steps**:

1. **Login Screen Access**
   - [ ] From landing screen, tap "Already have an account? Get Started"
   - [ ] Verify login screen displays with email/password fields

2. **Valid Login**
   - [ ] Enter correct email and password
   - [ ] Tap "Login"
   - [ ] Verify login completes within 2 seconds
   - [ ] Verify redirect to main dashboard
   - [ ] Verify session maintained on app restart (token refresh)

3. **Invalid Login Scenarios**
   - [ ] Test wrong password: Verify clear error message
   - [ ] Test wrong email: Verify clear error message
   - [ ] Test non-existent account: Verify secure error (no email enumeration)
   - [ ] Test 5+ failed attempts: Verify account lockout after 5 failures
   - [ ] Verify lockout message explains 15-minute wait

4. **Password Reset Flow**
   - [ ] Tap "Forgot your password?"
   - [ ] Verify "Forgot password?" screen displays
   - [ ] Enter email address
   - [ ] Tap "Send code"
   - [ ] Verify OTP sent to email
   - [ ] Verify "Enter reset code" screen displays
   - [ ] Test invalid reset code
   - [ ] Test expired reset code (1+ hour old)
   - [ ] Verify "Resend code" works
   - [ ] Enter correct 6-digit reset code
   - [ ] Verify "Reset password" screen displays
   - [ ] Enter new password (test password strength validation)
   - [ ] Confirm new password
   - [ ] Tap "Save and login"
   - [ ] Verify auto-login and redirect to dashboard

**Error-Prone Areas**:

- Account lockout behavior (5 failures)
- OTP expiration (1 hour for reset)
- Session token refresh
- Password visibility toggle

---

### 1.3 Profile Management & Settings

**Test Steps**:

1. **Profile Overview**
   - [ ] Navigate to Profile tab
   - [ ] Verify avatar, name, email displayed
   - [ ] Verify "Profile edit" and "Settings" buttons accessible
   - [ ] Verify menu items: Payment method, Previous treatment, Reviews, Delete account, Logout

2. **Profile Edit**
   - [ ] Tap "Profile edit"
   - [ ] Verify all profile fields editable:
     - [ ] Avatar (upload/change)
     - [ ] First name, Last name
     - [ ] Email (should trigger re-verification if changed)
     - [ ] Phone with country code
     - [ ] Birthday (date picker)
     - [ ] Gender
     - [ ] Location/Country
   - [ ] Test avatar upload:
     - [ ] Try invalid file types
     - [ ] Try oversized images
     - [ ] Upload valid image
   - [ ] Test email change:
     - [ ] Change email
     - [ ] Verify re-verification OTP sent
     - [ ] Complete re-verification
   - [ ] Tap "Save and update"
   - [ ] Verify changes reflected in profile

3. **Settings - Notifications**
   - [ ] Navigate to Settings > Notification
   - [ ] Verify global toggles: Email, Push (MVP - no per-category yet)
   - [ ] Toggle Email OFF > Save > Verify change persists
   - [ ] Toggle Push OFF > Save > Verify change persists
   - [ ] Test save failure: Disconnect network, toggle, verify UI rollback
   - [ ] Verify changes effective within 1 minute

4. **Settings - Privacy & Security**
   - [ ] Navigate to Settings > Privacy and security
   - [ ] **Change Password**:
     - [ ] Tap "Change password"
     - [ ] Verify requires old password and new password
     - [ ] Test wrong old password
     - [ ] Test weak new password
     - [ ] Enter valid old and new password
     - [ ] Verify password change success
     - [ ] Verify existing sessions NOT revoked (stays logged in)
     - [ ] Test requires re-auth if > 5 min since last re-auth
   - [ ] **Device Sessions**:
     - [ ] View active sessions list
     - [ ] Verify current session highlighted
     - [ ] Test revoke single session (if multiple devices)
     - [ ] Test "Revoke all sessions" (requires re-auth)
   - [ ] **Download My Data (GDPR)**:
     - [ ] Request data export
     - [ ] Verify confirmation message
     - [ ] Verify email sent with secure link (may take time)

5. **Settings - Help & Support**
   - [ ] Navigate to Settings > Help and support
   - [ ] **Report a Problem**:
     - [ ] Tap "Report a problem"
     - [ ] Verify device/OS/app version auto-attached
     - [ ] Submit feedback
     - [ ] Verify throttling prevents spam (multiple submissions)

6. **Settings - About**
   - [ ] Navigate to Settings > About
   - [ ] Verify app version displayed
   - [ ] Verify Terms & Conditions link works
   - [ ] Verify Privacy Policy link works
   - [ ] Verify Open-source licenses link works

7. **Account Deletion**
   - [ ] Tap "Delete account" from Profile menu
   - [ ] **Test blocking scenarios**:
     - [ ] Create active treatment/aftercare case > Try delete > Verify blocked with message
     - [ ] Create active payment in progress > Try delete > Verify blocked until payment completes
     - [ ] Create active inquiry > Try delete > Verify allowed and inquiry auto-closes
   - [ ] **Test re-auth requirement**:
     - [ ] Try delete account (no recent re-auth > 5 min)
     - [ ] Verify prompted for password or 6-digit OTP
     - [ ] Complete re-auth
   - [ ] Confirm deletion
   - [ ] Verify soft-delete request submitted
   - [ ] Verify cannot login after deletion

8. **Logout**
   - [ ] Tap "Logout"
   - [ ] Verify session tokens revoked
   - [ ] Verify return to Landing screen
   - [ ] Verify cannot access protected screens without re-login

**Error-Prone Areas**:

- Email change re-verification flow
- Session management (token refresh)
- Re-auth timing (5-minute window)
- Delete account blocking logic
- Notification preference persistence

---

## Module 2: Inquiry Submission & Distribution (FR-003)

**Reference**: `local-docs/project-requirements/functional-requirements/fr003-inquiry-submission/prd.md`

### 2.1 Service Selection & Destination

**Test Steps**:

1. **Service Selection**
   - [ ] From dashboard, tap "Get a Hair Transplant"
   - [ ] Verify service selection screen displays:
     - [ ] "Get a Hair Transplant" (primary)
     - [ ] "Monitor Hair Loss" (secondary - future)
     - [ ] "Aftercare: Monitor Transplant Progress" (secondary - future)
     - [ ] "Aftercare for Transplant" (secondary - future)
   - [ ] Select "Get a Hair Transplant"
   - [ ] Verify treatment type selection: Hair, Beard, Both
   - [ ] Test validation: Must select at least one
   - [ ] Select treatment type and continue

2. **Destination Selection**
   - [ ] Verify country list displays with starting prices
   - [ ] Verify countries ordered by proximity to patient location (or FR-028 config)
   - [ ] Test search for country
   - [ ] Test multi-select (max 10 countries)
   - [ ] Try selecting 11 countries (should fail - max 10)
   - [ ] Verify starting prices displayed for transparency
   - [ ] Select 3-5 countries and continue

**Expected Results**:

- Clear treatment selection
- Countries ordered intelligently
- Starting prices visible
- Max 10 countries enforced

**Error-Prone Areas**:

- Country ordering logic
- Pricing display (currency conversion)
- Max 10 validation

---

### 2.2 Detailed Information Collection

**Test Steps**:

1. **Hair Concern Details**
   - [ ] Verify "Detailed Information" screen displays
   - [ ] **Nature of concern** (required text):
     - [ ] Test empty submission
     - [ ] Enter detailed concern description
   - [ ] **Duration** (required dropdown):
     - [ ] Verify dropdown options available
     - [ ] Select duration
   - [ ] **Previous treatments** (required text):
     - [ ] Enter previous treatments or "None"
   - [ ] **Symptom severity** (1-10 slider):
     - [ ] Test slider drag
     - [ ] Verify value updates
     - [ ] Select severity level
   - [ ] **Lifestyle factors** (optional text):
     - [ ] Leave empty or add details
   - [ ] **Additional notes** (optional text):
     - [ ] Leave empty or add notes
   - [ ] Continue to media upload

2. **Visual Evidence Upload**
   - [ ] **Photos**:
     - [ ] Test upload invalid format (e.g., GIF)
     - [ ] Test upload oversized image (> 2MB)
     - [ ] Upload valid JPG/PNG image (≤ 2MB)
     - [ ] Verify thumbnail preview
     - [ ] Upload up to 5 photos total
     - [ ] Try uploading 6th photo (should fail - max 5 total)
   - [ ] **Videos**:
     - [ ] Test upload invalid format (e.g., AVI)
     - [ ] Test upload oversized video (> 20MB)
     - [ ] Test upload too-long video (> 30s)
     - [ ] Upload valid MP4 video (≤ 30s, ≤ 20MB)
     - [ ] Verify video preview
   - [ ] **Combined limit**:
     - [ ] Upload 3 photos + 2 videos (total 5) - should work
     - [ ] Try uploading 6th media file - should fail
   - [ ] Continue to 3D scan

**Expected Results**:

- All required fields validated
- Clear file size/format errors
- Max 5 total media files enforced
- Thumbnails/previews generated

**Error-Prone Areas**:

- File upload validation (size, format, duration)
- Max 5 files total (not per type)
- Media preview generation
- Upload progress indication

---

### 2.3 3D Head Scan Capture

**Test Steps**:

1. **Scan Instructions**
   - [ ] Verify scan instructions screen displays
   - [ ] Read through instructions (front, top, left, right angles)
   - [ ] Tap "Start Scan"

2. **Scan Capture Process**
   - [ ] Verify camera access permission requested
   - [ ] Grant camera permission
   - [ ] Verify camera view opens with guidance overlay
   - [ ] Follow on-screen guidance (front, top, left, right)
   - [ ] **Test quality validation**:
     - [ ] Try poor lighting - verify quality warning
     - [ ] Try distance too far - verify quality warning
     - [ ] Try moving too fast - verify quality warning
   - [ ] Capture complete scan with good quality
   - [ ] Verify quality indicators show "good" or "acceptable"
   - [ ] If quality poor, test "Retake" option

3. **Scan Review**
   - [ ] Verify scan preview displays
   - [ ] Test rotating/viewing scan if viewer available
   - [ ] Verify scan saved
   - [ ] Continue to date selection

**Expected Results**:

- Clear scan guidance
- Quality validation works
- Retake option available if poor quality
- Scan securely uploaded

**Error-Prone Areas**:

- Camera permission handling
- Quality validation thresholds
- Lighting/distance detection
- Scan upload reliability (large file)
- Offline/poor network handling

---

### 2.4 Treatment Date Selection

**Test Steps**:

1. **Date Range Selection**
   - [ ] Verify "Select preferred treatment dates" screen
   - [ ] Open calendar picker
   - [ ] Test selecting single day (should require range)
   - [ ] Select valid date range (e.g., 1 week)
   - [ ] Add 2nd date range
   - [ ] Add up to 10 date ranges
   - [ ] Try adding 11th range (should fail - max 10)
   - [ ] **Test validation**:
     - [ ] Try overlapping ranges (should fail)
     - [ ] Try dates in the past (should fail)
     - [ ] Try dates > 2 years out (should fail)
     - [ ] Try dates < 30 days from now (should fail - min 30 days)
   - [ ] Verify all ranges non-overlapping and valid
   - [ ] Continue to medical questionnaire

**Expected Results**:

- Max 10 date ranges
- Non-overlapping validation
- Date constraints enforced (30 days - 2 years)
- Clear error messages

**Error-Prone Areas**:

- Overlap detection
- Date validation (min/max)
- Calendar UX on mobile
- Multiple range management

---

### 2.5 Medical Questionnaire Completion

**Test Steps**:

1. **Questionnaire Navigation**
   - [ ] Verify "Medical Questionnaire" screen displays
   - [ ] Verify comprehensive question list (allergies, medications, chronic diseases, previous surgeries, etc.)
   - [ ] Scroll through all questions

2. **Question Answering**
   - [ ] **Test Yes/No validation**:
     - [ ] Leave question unanswered > Try continue > Verify blocked
     - [ ] Answer "No" > Verify can proceed to next
     - [ ] Answer "Yes" > Verify details field appears (required)
     - [ ] Try proceeding without details > Verify blocked
     - [ ] Enter details > Verify can proceed
   - [ ] Answer all questions (mix of Yes/No)
   - [ ] For "Yes" answers, provide detailed explanations
   - [ ] Continue to review

3. **Medical Alerts Verification**
   - [ ] **Test critical alert triggers** (e.g., severe allergies, cardiovascular disease):
     - [ ] Answer with critical condition
     - [ ] Verify alert level marked as "Critical" (red)
   - [ ] **Test standard alert triggers** (e.g., hypertension, diabetes):
     - [ ] Answer with moderate condition
     - [ ] Verify alert level marked as "Standard" (amber)
   - [ ] **Test no alerts**:
     - [ ] Answer all "No"
     - [ ] Verify alert level "None" (green)
   - [ ] Verify alerts prominently displayed

**Expected Results**:

- All questions answerable
- Detailed explanations required for "Yes"
- Medical alerts auto-generated correctly
- 3-tier color coding (Critical/red, Standard/amber, None/green)

**Error-Prone Areas**:

- Required details for "Yes" answers
- Alert generation logic
- Questionnaire length (user fatigue)
- Back navigation data persistence

---

### 2.6 Inquiry Review & Submission

**Test Steps**:

1. **Review Summary**
   - [ ] Verify all sections summarized:
     - [ ] Service and treatment type
     - [ ] Selected countries with prices
     - [ ] Concern details
     - [ ] Media files (thumbnails)
     - [ ] 3D scan reference
     - [ ] Date ranges
     - [ ] Medical questionnaire summary (alerts)
   - [ ] **Test editing**:
     - [ ] Tap edit on any section
     - [ ] Modify data
     - [ ] Return to summary
     - [ ] Verify changes reflected

2. **Provider Selection (Optional)**
   - [ ] Verify "Would you like to request a quote from some of our popular providers?" section
   - [ ] View provider list (based on reviews/admin curation)
   - [ ] Select up to 5 providers
   - [ ] Try selecting 6th provider (should fail - max 5)
   - [ ] Deselect providers
   - [ ] Note: Can skip this and let system auto-distribute

3. **Terms & Submission**
   - [ ] Verify Terms & Conditions checkbox
   - [ ] Try submitting without accepting terms (should fail)
   - [ ] Check Terms & Conditions
   - [ ] Tap "Submit inquiry"
   - [ ] Verify inquiry ID generated (HPID format: HPID + YY + MM + 4-digit sequence, e.g., HPID2501001)
   - [ ] Verify submission success message
   - [ ] Verify redirect to Inquiry Dashboard

**Expected Results**:

- Complete summary visible
- Can edit before submission
- Max 5 providers selectable
- Terms acceptance required
- Unique inquiry ID generated

**Error-Prone Areas**:

- Data persistence across edit flows
- Max 5 providers validation
- Terms acceptance validation
- Inquiry ID uniqueness

---

### 2.7 Inquiry Dashboard & Draft Management

**Test Steps**:

1. **View Inquiry Dashboard**
   - [ ] Navigate to Inquiry Dashboard (from FR-003 Screen 8)
   - [ ] Verify current stage badge (Inquiry/Quoted/Accepted/etc.)
   - [ ] Verify timeline with timestamps
   - [ ] Verify inquiry summary displayed
   - [ ] Verify responses count (0 initially)
   - [ ] Verify deadlines and expiry times
   - [ ] Verify next actions available

2. **Draft Autosave & Resume**
   - [ ] Start new inquiry
   - [ ] Fill out first few steps (e.g., name, destination)
   - [ ] Exit app (force close or background)
   - [ ] Reopen app within 7 days
   - [ ] Verify "continue with your request" option shown
   - [ ] Tap continue
   - [ ] Verify resume from last completed step
   - [ ] Verify previous data preserved
   - [ ] Complete and submit inquiry

3. **Draft Expiry**
   - [ ] (If possible, simulate time or wait 7 days)
   - [ ] Start inquiry, abandon for 7+ days
   - [ ] Return to app
   - [ ] Verify draft expired
   - [ ] Verify must start new inquiry

**Expected Results**:

- Inquiry dashboard shows real-time status
- Draft saved for 7 days
- Resume works seamlessly
- Draft expires after 7 days

**Error-Prone Areas**:

- Draft data persistence
- Resume from correct step
- 7-day expiry enforcement
- Multiple incomplete inquiries handling

---

## Module 3: Quote Comparison & Acceptance (FR-005)

**Reference**: `local-docs/project-requirements/functional-requirements/fr005-quote-comparison-acceptance/prd.md`

### 3.1 View & Compare Quotes

**Test Steps**:

1. **Quote Notifications**
   - [ ] Wait for providers to submit quotes (or use admin to create test quotes)
   - [ ] Verify push/email notifications received when quotes arrive
   - [ ] Tap notification > Verify deep-link to Inquiry Dashboard

2. **Inquiry Dashboard - Quotes Received**
   - [ ] Navigate to Inquiry Dashboard
   - [ ] Verify "Quotes Received" section displays
   - [ ] Verify quote count shown (e.g., "4 offers")
   - [ ] Tap "View Details" on a quote
   - [ ] Verify quote detail screen opens (FR-004 Screen 4)

3. **Quote Comparison View**
   - [ ] From Inquiry Dashboard, verify quote comparison interface
   - [ ] **Test filtering**:
     - [ ] Filter by price (low to high, high to low)
     - [ ] Filter by graft count
     - [ ] Filter by review rating
     - [ ] Filter by soonest appointment slot
   - [ ] **Test sorting**:
     - [ ] Sort by total price
     - [ ] Sort by price per graft
     - [ ] Sort by rating
   - [ ] **Test side-by-side comparison**:
     - [ ] Select 2 quotes for comparison
     - [ ] Verify comparison view displays key differentiators:
       - [ ] Total price, price per graft
       - [ ] Graft count
       - [ ] Review rating/count
       - [ ] Provider credentials summary
       - [ ] Included services checklist
       - [ ] Estimated travel costs
       - [ ] Pre-scheduled appointment slot
     - [ ] Select 3rd quote
     - [ ] Verify comparison works with 3 quotes (max 3)
     - [ ] Try selecting 4th quote (should replace one of 3)
   - [ ] Deselect quotes
   - [ ] View individual quote details

**Expected Results**:

- Quotes sortable/filterable
- Side-by-side comparison (max 3)
- Key differentiators clearly displayed
- Easy navigation between quotes

**Error-Prone Areas**:

- Comparison UX on mobile (3 columns)
- Price per graft calculation
- Expired quotes shown/hidden
- Appointment slot clarity

---

### 3.2 Quote Detail Review

**Test Steps**:

1. **View Full Quote Details**
   - [ ] Tap "View Details" on a quote
   - [ ] Verify quote detail screen displays all information from FR-004:
     - [ ] Treatment type and technique
     - [ ] Estimated graft count
     - [ ] Packages selected (hotel, transport, medication)
     - [ ] Pricing breakdown (treatment, packages, discounts, total)
     - [ ] Pre-scheduled appointment slot (date/time) - READ-ONLY
     - [ ] Provider information
     - [ ] Clinician assigned
     - [ ] Treatment plan (per-day breakdown)
     - [ ] Included services checklist
     - [ ] Estimated travel costs
     - [ ] Provider reviews (rating/count)
     - [ ] Provider credentials summary
     - [ ] Medical alerts (patient medical risk level)
   - [ ] Scroll through all details
   - [ ] Verify all data readable on mobile

2. **Provider Information**
   - [ ] Tap on provider name/link
   - [ ] Verify provider overview displays:
     - [ ] Clinic/hospital information
     - [ ] Staff details
     - [ ] Certifications and awards
     - [ ] Reviews
   - [ ] Return to quote detail

3. **Video & Information**
   - [ ] If treatment type has informative video, verify:
     - [ ] Video link/thumbnail displayed
     - [ ] Tap video > Verify plays
     - [ ] Video explains procedure type clearly
   - [ ] Verify text description available

**Expected Results**:

- All quote details visible
- Provider info accessible
- Videos play smoothly
- Readable on mobile devices

**Error-Prone Areas**:

- Long content scrolling on mobile
- Video playback issues
- Provider info navigation
- Medical alerts visibility

---

### 3.3 Ask Questions About Quote (FR-012 Integration)

**Test Steps**:

1. **Access Messaging from Quote**
   - [ ] From quote detail, look for "Ask Question" or messaging option
   - [ ] Note: Per FR-012, chat NOT accessible from quote detail screens
   - [ ] Navigate to Messages/Inbox (main navigation)
   - [ ] Verify conversation with provider exists (auto-created when provider submitted quote)
   - [ ] Open conversation with provider

2. **Send Question**
   - [ ] Compose question about quote (e.g., package options, dates, pricing)
   - [ ] Send message
   - [ ] Verify message sent successfully
   - [ ] Verify message appears in conversation history
   - [ ] Wait for provider response (or simulate via admin)
   - [ ] Verify notification received when provider replies
   - [ ] Open conversation and read response
   - [ ] Verify read receipt sent to provider

**Expected Results**:

- Can message provider about quote
- Conversation auto-created per patient-provider pair
- Messages delivered in real-time
- Notifications work

**Error-Prone Areas**:

- Conversation auto-creation
- Deep-linking from notification
- Message delivery reliability
- Read receipt accuracy

---

### 3.4 Quote Acceptance Flow

**Test Steps**:

1. **Pre-Acceptance Checks**
   - [ ] Navigate to quote detail screen
   - [ ] Verify "Accept" button visible (FR-005 enhancement)
   - [ ] Verify Terms Acknowledgment checkbox
   - [ ] Try tapping "Accept" without checking terms (should be disabled)
   - [ ] Check Terms Acknowledgment

2. **Accept Quote**
   - [ ] Tap "Accept" button
   - [ ] Verify Acceptance Confirmation Modal displays:
     - [ ] Quote summary (treatment, price, dates, provider)
     - [ ] Pre-scheduled appointment slot (already confirmed)
     - [ ] Terms acknowledgment (if not already checked)
     - [ ] Next steps: Booking & Payment handoff info
     - [ ] "Confirm" button
     - [ ] "Cancel" button
   - [ ] Tap "Cancel" > Verify modal closes, no acceptance
   - [ ] Tap "Accept" again > Check terms > Confirm acceptance

3. **Post-Acceptance Validation**
   - [ ] Verify acceptance success message
   - [ ] Verify auto-cancellation of other quotes (if multiple):
     - [ ] Check Inquiry Dashboard
     - [ ] Verify other quotes show "Cancelled (other accepted)" status
   - [ ] Verify inquiry stage updated to "Accepted"
   - [ ] Verify redirect to Booking & Payment flow (FR-006)

4. **Prevent Duplicate Acceptance**
   - [ ] Try accepting another quote (should fail)
   - [ ] Verify error message: "You have already accepted a quote for this inquiry"

5. **Expired Quote Handling**
   - [ ] If quote expired, verify:
     - [ ] "Accept" button disabled
     - [ ] "Expired" badge displayed
     - [ ] Guidance shown to select another quote

**Expected Results**:

- Acceptance confirmation modal clear
- Pre-scheduled appointment slot visible (no further selection needed)
- One acceptance per inquiry enforced
- Other quotes auto-cancelled
- Expired quotes not acceptable

**Error-Prone Areas**:

- Duplicate acceptance prevention
- Auto-cancellation of competing quotes
- Expiry countdown accuracy
- Modal UX on mobile
- Handoff to booking flow

---

## Module 4: Booking & Payment (FR-006, FR-007)

**Reference**: `local-docs/project-requirements/functional-requirements/fr006-booking-scheduling/prd.md`
**Reference**: `local-docs/project-requirements/functional-requirements/fr007-payment-processing/prd.md`

### 4.1 Review Accepted Quote & Proceed to Payment

**Test Steps**:

1. **Payment & Booking Confirmation Screen**
   - [ ] After quote acceptance, verify redirect to Payment screen (FR-006 Screen 1)
   - [ ] Verify all quote details displayed (read-only):
     - [ ] Treatment, packages, pricing
     - [ ] Pre-scheduled appointment slot (already confirmed - no selection)
     - [ ] Provider name
     - [ ] Total amount
   - [ ] **Verify deposit calculation**:
     - [ ] Verify deposit percentage displayed (admin-configured, default 20-30%)
     - [ ] Verify deposit amount calculated correctly
     - [ ] Verify remaining balance shown (Total - Deposit)
   - [ ] **Verify payment options**:
     - [ ] Full payment option available
     - [ ] Installment options displayed if eligible (based on FR-029 + FR-007B rules)
     - [ ] If no installment options feasible, verify Pay-in-Full only with explanation
   - [ ] **Verify currency**:
     - [ ] Correct currency displayed (from quote)
     - [ ] All amounts in same currency
   - [ ] Verify cancellation policy summary displayed
   - [ ] Verify cancellation policy acknowledgment checkbox
   - [ ] Verify Terms & Conditions acknowledgment checkbox

2. **Select Payment Option**
   - [ ] Select "Full Payment" option
   - [ ] Verify total amount updates
   - [ ] Switch to "Deposit" option
   - [ ] Verify deposit amount and remaining balance displayed
   - [ ] If installments available:
     - [ ] Select installment plan (e.g., 3 installments)
     - [ ] Verify installment schedule displayed
     - [ ] Verify completion date ≥ 30 days before procedure
     - [ ] Verify first installment amount shown

3. **Pre-Payment Validation**
   - [ ] Try tapping "Pay" without checking acknowledgments (should be disabled)
   - [ ] Check cancellation policy acknowledgment
   - [ ] Check Terms & Conditions acknowledgment
   - [ ] Verify "Pay" button enables

**Expected Results**:

- All quote details visible
- Deposit calculated correctly (admin-configured %)
- Payment options clear (full, deposit, installments if eligible)
- Acknowledgments required before payment

**Error-Prone Areas**:

- Deposit percentage calculation
- Installment eligibility logic
- Currency consistency
- Acknowledgment validation

---

### 4.2 Deposit Payment Flow

**Test Steps**:

1. **Payment Method Selection**
   - [ ] Tap "Pay" button
   - [ ] Verify payment methods displayed:
     - [ ] Card (Stripe or payment processor)
     - [ ] Bank transfer (if available)
     - [ ] Digital wallet (if available)
   - [ ] Select payment method (e.g., Card)

2. **Enter Payment Details**
   - [ ] Verify payment form displays:
     - [ ] Card number
     - [ ] Expiry date
     - [ ] CVV
     - [ ] Billing name
     - [ ] Billing address
   - [ ] **Test invalid inputs**:
     - [ ] Enter invalid card number
     - [ ] Enter expired card
     - [ ] Enter invalid CVV
     - [ ] Try submitting > Verify validation errors
   - [ ] Enter valid payment details
   - [ ] Verify amount displayed (deposit amount)
   - [ ] Tap "Pay Now"

3. **Payment Processing**
   - [ ] Verify loading indicator while processing
   - [ ] **Test successful payment**:
     - [ ] Payment authorizes successfully
     - [ ] Verify redirect to Booking Confirmation (FR-006 Screen 2)
   - [ ] **Test payment failure scenarios** (if test cards available):
     - [ ] Try declined card > Verify clear error message
     - [ ] Verify retry option available
     - [ ] Verify alternative payment method option
   - [ ] **Test 3DS/Additional Authentication** (if required):
     - [ ] Payment triggers 3DS challenge
     - [ ] Complete 3DS authentication
     - [ ] Verify payment completes after auth
   - [ ] **Test payment timeout**:
     - [ ] (Simulate slow network)
     - [ ] Verify timeout message
     - [ ] Verify retry option

4. **Payment Confirmation**
   - [ ] Verify payment success message
   - [ ] Verify booking status updated to "Confirmed"
   - [ ] Verify receipt/invoice issued
   - [ ] Verify confirmation email sent (check inbox)

**Expected Results**:

- Payment methods available
- Clear validation errors
- Payment processes within 30 seconds (95th percentile)
- Success confirmation clear
- Receipt/invoice generated

**Error-Prone Areas**:

- Payment gateway integration
- 3DS authentication flow
- Error message clarity
- Retry logic (idempotency)
- Network timeout handling

---

### 4.3 Payment Failure & Retry Flow (FR-007 B1, B2)

**Test Steps**:

1. **Transient Failure - Auto Retry**
   - [ ] Simulate transient network error during payment
   - [ ] Verify Payment Service performs up to 3 automatic retries (exponential backoff)
   - [ ] Verify no duplicate charges (idempotency)
   - [ ] If retries succeed, verify payment completes
   - [ ] If retries exhaust, verify clear error shown to patient

2. **Hard Decline - Manual Retry**
   - [ ] Use test card that triggers hard decline
   - [ ] Verify clear error message displayed
   - [ ] Verify suggested next steps (retry, use different method)
   - [ ] Tap "Retry" button
   - [ ] Enter different payment method
   - [ ] Complete payment successfully

3. **Payment Failure - 48-Hour Hold Period**
   - [ ] Simulate payment failure after quote acceptance
   - [ ] Verify system holds accepted quote and appointment slot for 48 hours
   - [ ] During hold period:
     - [ ] Navigate back to Accepted Quote view
     - [ ] Verify "Retry Payment" option available
     - [ ] Retry payment successfully
     - [ ] Verify booking confirms
   - [ ] Test hold period expiry:
     - [ ] (Simulate 48+ hours passing)
     - [ ] Verify slot released
     - [ ] Verify quote status reverts to "Quote" (available for acceptance again)
     - [ ] Verify both patient and provider notified of release

**Expected Results**:

- Auto-retry for transient errors (up to 3)
- Clear error messages for hard declines
- 48-hour hold period enforced
- Retry option available during hold
- Slot released after hold expires

**Error-Prone Areas**:

- Idempotency (no duplicate charges)
- Retry backoff timing
- Hold period countdown accuracy
- Notification delivery on release

---

### 4.4 Booking Confirmation & Itinerary

**Test Steps**:

1. **View Booking Confirmation**
   - [ ] After successful deposit payment, verify Booking Confirmation screen (FR-006 Screen 2)
   - [ ] Verify booking reference displayed (unique format)
   - [ ] Verify booking status badge: "Confirmed"
   - [ ] Verify all booking details displayed:
     - [ ] Quote reference
     - [ ] Provider name and contact (now unmasked after payment)
     - [ ] Procedure date and time (pre-scheduled appointment)
     - [ ] Treatment type
     - [ ] Total amount, deposit paid, remaining balance
     - [ ] Payment status (Deposit paid / Installments scheduled / Full paid)
     - [ ] Payment method used
   - [ ] If installments, verify next payment due date displayed
   - [ ] Verify itinerary summary (pre-op steps)
   - [ ] Verify cancellation policy link

2. **Add to Calendar**
   - [ ] Tap "Add to Calendar" button
   - [ ] Verify ICS file download or native calendar integration
   - [ ] Add to device calendar
   - [ ] Verify event created with correct date/time

3. **Travel Booking Integration** (if applicable)
   - [ ] If travel packages NOT included in quote:
     - [ ] Verify "Book Hotel" option displayed
     - [ ] Verify "Book Flights" option displayed
     - [ ] Tap "Book Hotel" > Verify redirect to hotel booking (FR-008)
     - [ ] Tap "Book Flights" > Verify redirect to flight booking (FR-008)
   - [ ] If travel packages included:
     - [ ] Verify travel details displayed in itinerary
     - [ ] Verify no additional booking needed

4. **Passport Details Upload** (if required by provider)
   - [ ] Verify "Upload Passport" option if provider needs it for hotel/flight booking
   - [ ] Tap "Upload Passport"
   - [ ] Take photo or select from gallery
   - [ ] Verify image upload successful
   - [ ] Verify passport details submitted

5. **Confirmation Email**
   - [ ] Check email inbox
   - [ ] Verify confirmation email received within 1 minute
   - [ ] Verify email contains:
     - [ ] Booking reference
     - [ ] Appointment details
     - [ ] Provider contact
     - [ ] Receipt/invoice attached or linked

**Expected Results**:

- Booking confirmed immediately after payment
- All details visible
- Add to calendar works
- Confirmation email received
- Travel/passport options available if needed

**Error-Prone Areas**:

- Calendar integration (iOS/Android differences)
- Passport upload validation
- Email delivery timing
- Provider contact unmasking (only after payment)

---

### 4.5 Final Payment Flow

**Test Steps**:

1. **Access Booking Details**
   - [ ] Navigate to "My Bookings" or "Previous Treatments" section
   - [ ] Select confirmed booking with remaining balance
   - [ ] Verify booking details displayed

2. **Final Payment Screen**
   - [ ] Verify "Pay Remaining Balance" button/option visible
   - [ ] Tap "Pay Remaining Balance"
   - [ ] Verify Final Payment screen displays (FR-006 Screen 2 equivalent)
   - [ ] Verify remaining balance amount displayed
   - [ ] Verify due date and countdown to procedure date
   - [ ] Verify payment method options
   - [ ] Verify billing details pre-filled or editable

3. **Complete Final Payment**
   - [ ] Select payment method
   - [ ] Enter/confirm payment details
   - [ ] Tap "Pay Now"
   - [ ] Verify payment processes
   - [ ] Verify success confirmation
   - [ ] Verify booking status updated to "Full Paid"
   - [ ] Verify final receipt/invoice issued
   - [ ] Verify confirmation email sent

4. **Final Payment Reminders**
   - [ ] Test reminder notifications:
     - [ ] 3 days before due date > Verify reminder sent
     - [ ] On due date > Verify reminder sent
     - [ ] After overdue > Verify booking flagged and admin notified

**Expected Results**:

- Final payment accessible before/on procedure date
- Reminders sent timely (3 days, on due date)
- Payment completes successfully
- Booking marked "Full Paid"

**Error-Prone Areas**:

- Reminder timing accuracy
- Overdue payment handling
- Payment amount calculation (remaining balance)

---

### 4.6 Cancellation & Refund Scenarios

**Test Steps**:

1. **Patient-Initiated Cancellation**
   - [ ] Navigate to booking details
   - [ ] Tap "Cancel Booking" option
   - [ ] Verify cancellation policy displayed with refund schedule:
     - [ ] > 30 days before: 90% refund
     - [ ] 15-30 days before: 50% refund
     - [ ] < 15 days before: No refund (unless medical emergency)
   - [ ] Verify days before procedure displayed
   - [ ] Verify refund amount calculated and shown
   - [ ] Verify cancellation reason required
   - [ ] Enter cancellation reason
   - [ ] Confirm cancellation
   - [ ] Verify cancellation request submitted
   - [ ] Verify admin notified for approval

2. **Refund Processing** (Admin side - verify patient receives notification)
   - [ ] Wait for admin to process refund (or simulate)
   - [ ] Verify refund confirmation notification received
   - [ ] Verify refund amount matches policy
   - [ ] Verify booking status updated to "Cancelled"
   - [ ] Check payment method for refund (may take 5-10 business days)

3. **Medical Emergency Exception**
   - [ ] Cancel booking < 15 days before procedure
   - [ ] Verify refund amount = 0% per policy
   - [ ] Upload medical documentation (doctor's note, medical certificate)
   - [ ] Submit cancellation request
   - [ ] Verify admin review required
   - [ ] Wait for admin approval
   - [ ] If approved, verify full refund processed

**Expected Results**:

- Cancellation policy clear
- Refund amounts calculated correctly per policy
- Exceptions handled (medical emergency)
- Booking status updated
- Refund processed timely

**Error-Prone Areas**:

- Refund calculation accuracy
- Policy thresholds (30 days, 15 days)
- Medical documentation upload
- Refund timing (5-10 business days)

---

## Module 5: Messaging & Communication (FR-012)

**Reference**: `local-docs/project-requirements/functional-requirements/fr012-secure-messaging/prd.md`

### 5.1 Messages Inbox Navigation

**Test Steps**:

1. **Access Messages Inbox**
   - [ ] Navigate to Messages/Inbox from main navigation
   - [ ] Verify inbox displays all patient-provider conversations
   - [ ] Verify conversation list shows:
     - [ ] Provider avatar
     - [ ] Provider name and clinic
     - [ ] Last message preview (truncated, max 100 chars)
     - [ ] Unread badge (if unread messages)
     - [ ] Timestamp (relative or absolute)

2. **Search & Filter**
   - [ ] **Test search**:
     - [ ] Search by provider name
     - [ ] Search by message content (keyword)
     - [ ] Verify results update in real-time
   - [ ] **Test filter by status**:
     - [ ] Filter "All" > Verify all conversations shown
     - [ ] Filter "Unread" > Verify only unread shown
     - [ ] Filter "Read" > Verify only read shown
   - [ ] **Test sort**:
     - [ ] Sort by "Latest Activity" (default)
     - [ ] Sort by "Provider Name"
     - [ ] Sort by "Date Created"

3. **Empty State**
   - [ ] If no conversations exist:
     - [ ] Verify empty state message: "No messages yet. When a provider sends you a quote, a conversation will start here."

4. **Pull-to-Refresh**
   - [ ] Pull down on conversation list
   - [ ] Verify refresh animation
   - [ ] Verify latest messages synced

**Expected Results**:

- Inbox accessible from main navigation
- Conversations display correctly
- Search and filter work
- Empty state clear

**Error-Prone Areas**:

- Real-time updates (new messages)
- Search performance (large conversation lists)
- Unread badge accuracy
- Timestamp formatting (relative vs absolute)

---

### 5.2 Patient ↔ Provider Chat

**Test Steps**:

1. **Open Conversation**
   - [ ] Tap on a conversation from inbox
   - [ ] Verify chat screen opens (FR-012 Screen 2)
   - [ ] Verify conversation header shows:
     - [ ] Provider name and clinic
     - [ ] Audio call button
     - [ ] Video call button
   - [ ] Verify message history loads
   - [ ] Verify messages display chronologically
   - [ ] Verify timestamps per message
   - [ ] Verify read receipts per message

2. **Send Text Message**
   - [ ] Compose message in text field
   - [ ] Test max length (2000 chars):
     - [ ] Type 2001+ chars > Verify truncated or blocked
   - [ ] Tap "Send" button
   - [ ] Verify message sent successfully
   - [ ] Verify message appears in conversation
   - [ ] Verify sending/sent states
   - [ ] Verify timestamp displayed

3. **Attach Media**
   - [ ] Tap attachment button
   - [ ] **Test image upload**:
     - [ ] Select image from gallery
     - [ ] Test invalid format (e.g., GIF) > Verify error
     - [ ] Test oversized image (> 5MB) > Verify error
     - [ ] Upload valid JPG/PNG (≤ 5MB)
     - [ ] Verify thumbnail preview in compose area
     - [ ] Send message with image
     - [ ] Verify image displays in conversation
   - [ ] **Test video upload**:
     - [ ] Select video from gallery
     - [ ] Test invalid format > Verify error
     - [ ] Test oversized video (> 10MB) > Verify error
     - [ ] Upload valid MP4 (≤ 10MB)
     - [ ] Send message with video
     - [ ] Verify video plays inline or modal
   - [ ] **Test PDF upload**:
     - [ ] Select PDF file
     - [ ] Test oversized PDF (> 10MB) > Verify error
     - [ ] Upload valid PDF (≤ 10MB)
     - [ ] Send message with PDF
     - [ ] Verify PDF download link displays
   - [ ] **Test max attachments**:
     - [ ] Attach 5 files (images/videos/PDFs combined)
     - [ ] Try attaching 6th file > Verify error: "Maximum 5 attachments per message"

4. **Receive Messages**
   - [ ] Wait for provider to reply (or simulate via admin)
   - [ ] Verify push notification received
   - [ ] Verify unread badge updates in inbox
   - [ ] Open conversation from notification
   - [ ] Verify new message displayed
   - [ ] Verify read receipt sent to provider
   - [ ] Verify unread badge clears

5. **Read Receipts**
   - [ ] Send message to provider
   - [ ] Verify message status: "Sent"
   - [ ] Wait for provider to read
   - [ ] Verify message status: "Read" with timestamp

6. **Typing Indicators** (if implemented)
   - [ ] Start typing message
   - [ ] Verify provider sees typing indicator (test via admin)
   - [ ] Stop typing
   - [ ] Verify typing indicator disappears

**Expected Results**:

- Messages send/receive in real-time
- Media uploads with proper validation
- Max 5 attachments enforced
- Read receipts accurate
- Notifications work

**Error-Prone Areas**:

- Real-time message delivery
- Media upload reliability (large files)
- Push notification deep-linking
- Read receipt timing
- Max attachment validation

---

### 5.3 Audio & Video Calls (Twilio Integration)

**Test Steps**:

1. **Initiate Audio Call**
   - [ ] From chat screen, tap "Audio Call" button
   - [ ] Verify call initiation (Twilio connection)
   - [ ] Verify ringing state for recipient
   - [ ] **Test successful call**:
     - [ ] Provider answers (simulate via admin)
     - [ ] Verify audio call active
     - [ ] Test microphone mute/unmute
     - [ ] Test speaker toggle
     - [ ] End call
     - [ ] Verify call ended successfully
   - [ ] **Test declined call**:
     - [ ] Initiate call
     - [ ] Provider declines
     - [ ] Verify call ended message
   - [ ] **Test missed call**:
     - [ ] Initiate call
     - [ ] No answer
     - [ ] Verify timeout and missed call message

2. **Receive Audio Call**
   - [ ] Wait for provider to call (simulate via admin)
   - [ ] Verify incoming call notification
   - [ ] Verify "Answer" and "Decline" options
   - [ ] **Test answer**:
     - [ ] Tap "Answer"
     - [ ] Verify audio call active
     - [ ] Test audio quality
     - [ ] End call
   - [ ] **Test decline**:
     - [ ] Tap "Decline"
     - [ ] Verify call declined

3. **Initiate Video Call**
   - [ ] From chat screen, tap "Video Call" button
   - [ ] Verify camera permission requested (if first time)
   - [ ] Grant camera permission
   - [ ] Verify call initiation
   - [ ] **Test successful video call**:
     - [ ] Provider answers
     - [ ] Verify video call active
     - [ ] Verify local and remote video visible
     - [ ] Test camera switch (front/back)
     - [ ] Test video mute (camera off)
     - [ ] Test microphone mute
     - [ ] End call
   - [ ] **Test connection issues**:
     - [ ] Simulate poor network
     - [ ] Verify connection error message
     - [ ] Verify fallback or retry option

4. **Receive Video Call**
   - [ ] Wait for provider to call
   - [ ] Verify incoming video call notification
   - [ ] Answer call
   - [ ] Verify video call active
   - [ ] End call

**Expected Results**:

- Audio/video calls initiate successfully
- Call controls work (mute, speaker, camera)
- Call quality acceptable
- Connection errors handled gracefully

**Error-Prone Areas**:

- Twilio integration stability
- Camera/microphone permissions
- Call quality (network dependent)
- Connection timeout handling
- Deep-linking from call notification

---

### 5.4 Admin Intervention Visibility (Patient Side)

**Test Steps**:

1. **Receive Admin Emergency Message**
   - [ ] Wait for admin to send emergency intervention message (simulate via admin)
   - [ ] Verify push notification received
   - [ ] Open conversation
   - [ ] Verify admin message displays with "Hairline Admin" badge
   - [ ] Verify message clearly identified as from admin
   - [ ] Verify patient cannot reply directly to admin (chat remains with provider)

2. **Admin Observation Flags** (should NOT be visible to patient)
   - [ ] Admin flags conversation for observation
   - [ ] Verify patient sees NO indication of flag
   - [ ] Verify patient can continue messaging normally

**Expected Results**:

- Admin messages visible with badge
- Admin intervention rare (<5% conversations)
- No visibility of observation flags to patient

**Error-Prone Areas**:

- Admin badge display
- Notification for admin messages
- Ensuring flags not visible to patient

---

## Module 6: Aftercare & Recovery Management (FR-011)

**Reference**: `local-docs/project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md`

### 6.1 Aftercare Dashboard & Milestones

**Test Steps**:

1. **Access Aftercare**
   - [ ] After procedure completion (or simulate), navigate to Aftercare section
   - [ ] Verify aftercare dashboard displays
   - [ ] Verify milestone-based tracking interface shows:
     - [ ] Current milestone (e.g., "Day 3 Post-Surgery")
     - [ ] Milestone progress (X of Y milestones)
     - [ ] Timeline visualization
   - [ ] Verify all milestones listed with status (Upcoming/Active/Completed)

2. **Milestone Questionnaires**
   - [ ] Navigate to active milestone
   - [ ] Verify questionnaire for current milestone displays
   - [ ] **Test questionnaire types**:
     - [ ] Pain level assessment (slider 1-10)
     - [ ] Sleep quality assessment (e.g., "Sleep well?" Yes/No)
     - [ ] Symptom checks (e.g., swelling, redness)
   - [ ] Answer all questions
   - [ ] Submit questionnaire
   - [ ] Verify responses saved
   - [ ] Verify milestone updated to "Completed"

3. **3D Scan Monitoring**
   - [ ] Navigate to "3D Scan" section
   - [ ] Verify scan schedule displayed (e.g., every 2 weeks)
   - [ ] Tap "Capture Scan"
   - [ ] Follow scan instructions (similar to inquiry submission scan)
   - [ ] Complete scan
   - [ ] Verify scan uploaded and saved
   - [ ] Verify scan added to timeline
   - [ ] **Test interactive timeline** (client requirement):
     - [ ] Verify timeline UI displays all scan dates
     - [ ] Drag/scroll through timeline
     - [ ] Select different scan dates
     - [ ] Verify 3D scan viewer updates for selected date
     - [ ] Compare before/after (initial scan vs latest)
     - [ ] Verify visual progress indicators

4. **Medication Tracking**
   - [ ] Navigate to "Medications" section
   - [ ] Verify medication list displays based on current milestone
   - [ ] Verify instructions for each medication (dosage, frequency, duration)
   - [ ] Mark medication as taken (if feature available)
   - [ ] Verify reminders set for medication times

5. **Instructions & Helpful Guides**
   - [ ] Navigate to "Instructions" section
   - [ ] Verify instructions for current milestone (e.g., "How to wash your hair")
   - [ ] Tap on instruction guide
   - [ ] Verify content displays (text, images, videos)
   - [ ] Verify guidance clear and helpful

**Expected Results**:

- Milestone-based tracking clear
- Questionnaires adaptive per milestone
- 3D scan timeline interactive
- Medication tracking helpful
- Instructions accessible

**Error-Prone Areas**:

- Milestone progression logic
- Questionnaire frequency (every 2 days vs every month)
- 3D scan upload reliability
- Timeline interaction UX on mobile
- Medication reminder timing

---

### 6.2 Chat with Aftercare Support

**Test Steps**:

1. **Access Aftercare Chat**
   - [ ] From aftercare dashboard, tap "Chat with Support" or similar
   - [ ] Verify aftercare support chat opens
   - [ ] Note: This is separate from provider messaging

2. **Send Message to Support**
   - [ ] Compose question/concern about recovery
   - [ ] Send message
   - [ ] Verify message sent successfully
   - [ ] Wait for support team response (or simulate)
   - [ ] Verify response received
   - [ ] Verify notification received

3. **Request 3D Scan Review**
   - [ ] In chat, look for preset action: "Request 3D scan review"
   - [ ] Tap request
   - [ ] Verify support team notified
   - [ ] Wait for response with scan analysis

4. **Request Live Video Consultation**
   - [ ] In chat, look for preset action: "Request live video chat"
   - [ ] Tap request
   - [ ] Verify consultation request sent
   - [ ] Wait for scheduling/confirmation
   - [ ] If scheduled, receive video call from support team

**Expected Results**:

- Aftercare support accessible
- Preset actions work (scan review, video chat)
- Support team responsive
- Professional and helpful guidance

**Error-Prone Areas**:

- Support team availability
- Video consultation scheduling
- Scan review turnaround time

---

## Module 7: Reviews & Ratings (FR-013)

**Reference**: Mentioned in FR-001 Profile screens and client transcriptions

### 7.1 Leave Review After Treatment

**Test Steps**:

1. **Access Review Section**
   - [ ] Navigate to Profile > Reviews
   - [ ] Verify review eligibility:
     - [ ] If treatment completed ≥ 3 months ago, "Write review" CTA visible
     - [ ] If treatment < 3 months or not completed, read-only history only
   - [ ] Tap "Write review"

2. **Write Review**
   - [ ] Verify review form displays:
     - [ ] Overall rating (1-5 stars)
     - [ ] Individual ratings (e.g., quality, cleanliness, communication)
     - [ ] Text review (description)
     - [ ] Optional: Before/after photo upload
   - [ ] **Test interactive before/after** (client requirement):
     - [ ] If opted in, verify 3D scan before/after included
     - [ ] Verify interactive progress visualization (scan timeline)
   - [ ] Select overall rating
   - [ ] Enter text review
   - [ ] Optionally upload before/after photos
   - [ ] Submit review

3. **Review Submission**
   - [ ] Verify review submitted successfully
   - [ ] Verify confirmation message
   - [ ] Verify review appears in "My Reviews" section
   - [ ] Note: Review may require admin approval before public display

4. **View Provider Reviews**
   - [ ] From quote detail or provider profile, navigate to Reviews section
   - [ ] Verify all provider reviews displayed
   - [ ] Verify ratings visible (overall and breakdown)
   - [ ] Verify before/after photos visible (if shared)
   - [ ] Verify interactive 3D scan timeline (if opted in by reviewer)
   - [ ] Scroll through reviews
   - [ ] Verify reviews sorted (recent first or highest rated)

**Expected Results**:

- Review form clear and easy
- Before/after with 3D scans interactive
- Review submission successful
- Provider reviews visible to patients

**Error-Prone Areas**:

- Review eligibility (3-month rule)
- Before/after photo upload validation
- Interactive 3D timeline performance
- Review approval workflow (admin side)

---

## Cross-Module Integration Testing

These scenarios test interactions between multiple modules.

### Integration 1: End-to-End Happy Path (Critical)

**Objective**: Complete patient journey from registration to aftercare

**Test Steps**:

1. **Register & Login**
   - [ ] Complete new user registration (Module 1.1)
   - [ ] Verify account created and logged in

2. **Submit Inquiry**
   - [ ] Submit complete inquiry with all required data (Module 2)
   - [ ] Verify inquiry submitted successfully

3. **Receive & Compare Quotes**
   - [ ] Wait for quotes (or create via admin)
   - [ ] View and compare quotes (Module 3.1)
   - [ ] Select best quote

4. **Accept Quote**
   - [ ] Accept selected quote (Module 3.4)
   - [ ] Verify other quotes auto-cancelled

5. **Pay Deposit**
   - [ ] Complete deposit payment (Module 4.2)
   - [ ] Verify booking confirmed

6. **Message Provider**
   - [ ] Send question to provider about procedure (Module 5.2)
   - [ ] Receive response

7. **Pay Final Balance**
   - [ ] Complete final payment before procedure date (Module 4.5)
   - [ ] Verify booking fully paid

8. **Attend Procedure** (simulate completion)
   - [ ] Admin marks treatment complete
   - [ ] Verify status updated

9. **Engage with Aftercare**
   - [ ] Access aftercare dashboard (Module 6.1)
   - [ ] Complete milestone questionnaires
   - [ ] Upload 3D scan for monitoring
   - [ ] Chat with support team

10. **Leave Review**
    - [ ] Wait 3+ months (or simulate)
    - [ ] Write and submit review (Module 7.1)

**Expected Results**:

- Complete journey successful
- Data flows between modules seamlessly
- No broken links or missing data
- Professional and smooth user experience

**Critical Success Metrics**:

- Total time from registration to inquiry submission: < 20 minutes
- Total time from quote acceptance to booking confirmation: < 10 minutes
- Zero data loss between steps
- All notifications delivered timely

---

### Integration 2: Multi-Quote Journey

**Test Steps**:

1. Submit inquiry
2. Receive quotes from 4 different providers
3. Message 2 providers with questions
4. Compare all 4 quotes side-by-side
5. Accept 1 quote
6. Verify other 3 quotes auto-cancelled
7. Complete payment
8. Verify booking confirmed with correct provider

**Expected Results**:

- Multiple quotes handled correctly
- Messaging works with multiple providers
- Auto-cancellation accurate
- Final booking matches accepted quote

---

### Integration 3: Payment Failure & Recovery

**Test Steps**:

1. Accept quote
2. Attempt deposit payment > Payment fails
3. Verify 48-hour hold period active
4. Wait 24 hours
5. Retry payment > Success
6. Verify booking confirmed
7. Verify appointment slot still reserved

**Expected Results**:

- Hold period enforced
- Retry successful
- Slot not lost during hold

---

### Integration 4: Cancellation & Refund

**Test Steps**:

1. Complete booking with deposit paid
2. Wait 40 days before procedure
3. Cancel booking
4. Verify 90% refund calculated (> 30 days before)
5. Admin approves refund
6. Verify refund processed
7. Verify booking status "Cancelled"

**Expected Results**:

- Cancellation policy applied correctly
- Refund amount accurate
- Status updated

---

## Edge Cases & Error Scenarios

### Edge Case 1: Network Interruptions

**Test Steps**:

1. **During Inquiry Submission**:
   - [ ] Fill out inquiry to 50% completion
   - [ ] Disable network mid-submission
   - [ ] Verify error message clear
   - [ ] Re-enable network
   - [ ] Verify draft saved and can resume

2. **During Payment**:
   - [ ] Initiate payment
   - [ ] Disable network during processing
   - [ ] Re-enable network
   - [ ] Verify payment status queried correctly (not duplicate charged)

3. **During Messaging**:
   - [ ] Send message
   - [ ] Disable network
   - [ ] Verify message queued locally
   - [ ] Re-enable network
   - [ ] Verify message sends when reconnected

**Expected Results**:

- Graceful degradation
- Clear offline indicators
- Data not lost
- Retry mechanisms work

---

### Edge Case 2: App Backgrounding/Foregrounding

**Test Steps**:

1. **During Inquiry Submission**:
   - [ ] Fill out inquiry partially
   - [ ] Background app (go to home screen)
   - [ ] Wait 10 minutes
   - [ ] Foreground app
   - [ ] Verify data preserved

2. **During Payment**:
   - [ ] Initiate payment
   - [ ] Background app during 3DS authentication
   - [ ] Foreground app
   - [ ] Complete authentication
   - [ ] Verify payment completes

3. **During Video Call**:
   - [ ] Start video call
   - [ ] Background app
   - [ ] Verify call paused or continues in background
   - [ ] Foreground app
   - [ ] Verify call resumes

**Expected Results**:

- Data preserved on backgrounding
- Sessions maintained
- Payment flows resume correctly
- Calls handled gracefully

---

### Edge Case 3: Multiple Device Login

**Test Steps**:

1. Login on Device A
2. Login on Device B with same account
3. Verify both sessions active (or older session invalidated, depending on design)
4. Send message from Device A
5. Verify message syncs to Device B
6. Logout from Device A
7. Verify Device B still logged in

**Expected Results**:

- Multi-device support (or clear single-session enforcement)
- Message sync across devices
- Session management clear

---

### Edge Case 4: Expired Quotes & Timing Issues

**Test Steps**:

1. Receive quote with 48-hour expiry
2. Wait 47 hours
3. Accept quote > Verify success
4. Wait 49 hours on another quote
5. Try to accept expired quote > Verify blocked
6. Verify clear "Expired" badge and guidance

**Expected Results**:

- Expiry countdown accurate
- Acceptance blocked after expiry
- Clear expired state messaging

---

### Edge Case 5: Overlapping Appointment Slots (FR-006 Conflict Prevention)

**Test Steps**:

1. Two patients accept quotes from same provider with overlapping appointment slots
2. Patient A completes payment first > Verify booking confirmed and slot blocked
3. Patient B attempts payment > Verify conflict error
4. Verify Patient B's quote status reverts to "Quote" (available for acceptance)
5. Verify Patient B notified of conflict
6. Verify Provider notified of Patient B's slot release

**Expected Results**:

- First payment confirmation wins
- Second booking attempt fails with clear error
- No double-booking
- Both parties notified

---

### Edge Case 6: Incomplete Profile & Inquiry Submission

**Test Steps**:

1. Register account but skip optional profile fields
2. Attempt to submit inquiry
3. Verify profile completion check
4. If incomplete profile blocks inquiry, verify clear message
5. Complete profile
6. Submit inquiry successfully

**Expected Results**:

- Profile completion enforced if required
- Clear guidance to complete profile
- Inquiry submits after completion

---

## Usability & UX Testing

These scenarios focus on user experience, not just functionality.

### UX Test 1: Form Validation & Error Messages

**Objective**: Ensure all validation messages are clear, helpful, and timely

**Test Steps**:

1. **Test every form in the app**:
   - [ ] Registration forms
   - [ ] Inquiry submission forms
   - [ ] Payment forms
   - [ ] Profile edit forms
   - [ ] Review forms
   - [ ] Messaging compose

2. **For each form, test**:
   - [ ] Leave required fields empty > Submit > Verify clear error messages
   - [ ] Enter invalid data > Verify real-time validation (if implemented)
   - [ ] Verify error messages specific (not generic "Invalid input")
   - [ ] Verify error messages positioned near relevant fields
   - [ ] Verify error messages actionable (tell user how to fix)

**Expected Results**:

- All validation clear and helpful
- Real-time validation where appropriate
- Error messages specific and actionable
- No confusing or generic errors

**Critical UX Issues to Flag**:

- "Error occurred" without details
- Validation only on submit (no real-time)
- Errors not near relevant fields
- Unclear password requirements

---

### UX Test 2: Loading States & Progress Indicators

**Objective**: Ensure users always know what's happening

**Test Steps**:

1. **Test all loading scenarios**:
   - [ ] App launch > Splash screen
   - [ ] Login > Loading after submit
   - [ ] Inquiry submission > Uploading media/scan
   - [ ] Payment processing > Waiting for authorization
   - [ ] Messaging > Sending message
   - [ ] 3D scan capture > Processing scan

2. **For each scenario, verify**:
   - [ ] Loading indicator visible (spinner, progress bar, skeleton UI)
   - [ ] No blank screens for > 2 seconds
   - [ ] Long operations show progress (e.g., "Uploading 2 of 5 photos")
   - [ ] User can cancel or go back if appropriate

**Expected Results**:

- Always clear what's happening
- No unexplained wait times
- Progress visible for long operations
- User retains control

**Critical UX Issues to Flag**:

- Blank screens with no indicator
- No progress for long uploads
- Can't cancel long operations
- UI freezes during processing

---

### UX Test 3: Navigation & Back Button Behavior

**Objective**: Ensure navigation is intuitive and predictable

**Test Steps**:

1. **Test navigation patterns**:
   - [ ] Tap bottom navigation tabs > Verify correct screens
   - [ ] Use back button on each screen > Verify returns to previous
   - [ ] Test deep-linking from notifications > Verify navigates to correct screen
   - [ ] Test breadcrumbs (if any) > Verify navigation hierarchy

2. **Test multi-step flows (inquiry, payment)**:
   - [ ] Navigate forward through steps
   - [ ] Use back button mid-flow > Verify data preserved
   - [ ] Exit flow mid-way > Return > Verify can resume

3. **Test edge cases**:
   - [ ] Back button on first screen > Verify exits app or prompts
   - [ ] Back button on modal/overlay > Verify closes modal
   - [ ] Back button during loading > Verify cancels or waits appropriately

**Expected Results**:

- Back button behavior predictable
- Data preserved when navigating back
- Deep-linking works correctly
- No navigation dead-ends

**Critical UX Issues to Flag**:

- Back button unexpected behavior
- Data lost on navigation back
- Deep-links broken
- Can't escape from screen

---

### UX Test 4: Accessibility & Readability

**Objective**: Ensure app usable by all users, including those with disabilities

**Test Steps**:

1. **Text Readability**:
   - [ ] Check all text sizes > Verify readable on various screen sizes
   - [ ] Test high contrast mode (if supported)
   - [ ] Test large text mode (device accessibility settings)
   - [ ] Verify font weights appropriate (headings vs body)

2. **Color Contrast**:
   - [ ] Verify sufficient contrast for all text (WCAG AA minimum)
   - [ ] Verify colors not sole indicator (use icons, labels too)
   - [ ] Test color blindness simulation (if tools available)

3. **Touch Targets**:
   - [ ] Verify all buttons/links large enough (min 44x44 points)
   - [ ] Verify sufficient spacing between tappable elements
   - [ ] Test on small device (e.g., iPhone SE)

4. **Screen Reader Support**:
   - [ ] Enable VoiceOver (iOS) or TalkBack (Android)
   - [ ] Navigate through app with screen reader
   - [ ] Verify all elements announced clearly
   - [ ] Verify images have alt text
   - [ ] Verify buttons have descriptive labels

5. **Keyboard Navigation** (if applicable for tablets):
   - [ ] Test tab navigation through forms
   - [ ] Verify focus indicators visible
   - [ ] Verify logical tab order

**Expected Results**:

- Text readable at all sizes
- Sufficient color contrast
- Touch targets large enough
- Screen reader usable
- Keyboard navigation works

**Critical Accessibility Issues to Flag**:

- Small text (< 14pt body)
- Low contrast text
- Tiny touch targets (< 44x44)
- Screen reader navigation broken
- Missing alt text on images

---

### UX Test 5: Empty States & First-Time User Experience

**Objective**: Ensure new users understand how to use the app

**Test Steps**:

1. **Test all empty states**:
   - [ ] Messages inbox (no conversations yet)
   - [ ] Bookings/treatments (none yet)
   - [ ] Reviews (none yet)
   - [ ] Aftercare (not enrolled yet)

2. **For each empty state, verify**:
   - [ ] Clear message explaining why empty
   - [ ] Helpful guidance on what to do next
   - [ ] Call-to-action button if applicable

3. **First-time user onboarding**:
   - [ ] After registration, check if onboarding tips shown
   - [ ] Verify tips contextual and helpful
   - [ ] Verify can skip or dismiss tips
   - [ ] Verify tips don't show again after dismissed

**Expected Results**:

- Empty states not confusing
- Clear guidance for new users
- Onboarding helpful but skippable

**Critical UX Issues to Flag**:

- Blank screens with no explanation
- No guidance for new users
- Forced onboarding with no skip
- Onboarding repeats annoyingly

---

### UX Test 6: Notification Clarity & Timing

**Objective**: Ensure notifications are timely, clear, and actionable

**Test Steps**:

1. **Test all notification scenarios**:
   - [ ] New quote received
   - [ ] Provider message received
   - [ ] Payment reminder (final payment due)
   - [ ] Aftercare milestone reminder
   - [ ] Review eligible (3 months post-treatment)
   - [ ] Admin intervention message

2. **For each notification, verify**:
   - [ ] Notification title clear and specific
   - [ ] Notification body provides context
   - [ ] Notification arrives timely (within 5 seconds for real-time events)
   - [ ] Tap notification > Deep-links to relevant screen correctly
   - [ ] Notification badge updates (e.g., unread count)

3. **Notification Settings**:
   - [ ] Navigate to Settings > Notifications
   - [ ] Toggle Email notifications OFF > Verify no emails received
   - [ ] Toggle Push notifications OFF > Verify no push received
   - [ ] Re-enable > Verify notifications resume

**Expected Results**:

- Notifications clear and specific
- Timely delivery (< 5 seconds for real-time)
- Deep-linking works
- Notification settings respected

**Critical UX Issues to Flag**:

- Generic notification titles ("New message")
- Delayed notifications (> 30 seconds for real-time)
- Deep-links broken or wrong screen
- Settings not respected

---

## Performance & Stress Testing

### Performance Test 1: App Launch Time

**Test Steps**:

1. Close app completely
2. Launch app (cold start)
3. Measure time from tap to splash screen
4. Measure time from splash screen to landing/dashboard
5. Repeat 5 times, calculate average

**Expected Results**:

- Splash screen appears < 1 second
- Landing/dashboard appears < 3 seconds total
- Consistent performance across launches

**Flag if**: Launch time > 5 seconds

---

### Performance Test 2: Screen Load Times

**Test Steps**:

For each major screen, measure load time:

1. Inquiry Dashboard
2. Quote comparison screen
3. Messages inbox
4. Aftercare dashboard
5. Booking details

**Expected Results**:

- All screens load within 2 seconds (95th percentile)
- Critical screens (payment, booking) load within 1 second

**Flag if**: Any screen > 3 seconds load time

---

### Performance Test 3: Large Data Handling

**Test Steps**:

1. **Messages Inbox with 50+ Conversations**:
   - [ ] Create or populate 50+ conversations
   - [ ] Open Messages inbox
   - [ ] Scroll through list
   - [ ] Verify smooth scrolling (no lag/jank)
   - [ ] Open a conversation from bottom of list
   - [ ] Verify loads quickly

2. **Long Conversation (100+ Messages)**:
   - [ ] Create conversation with 100+ messages
   - [ ] Open conversation
   - [ ] Verify messages load (paginated or virtual scrolling)
   - [ ] Scroll to top (oldest messages)
   - [ ] Verify smooth scrolling
   - [ ] Send new message
   - [ ] Verify performance not degraded

3. **Multiple Media Attachments**:
   - [ ] Open conversation with many image/video attachments
   - [ ] Scroll through messages
   - [ ] Verify images load with lazy loading
   - [ ] Tap image to view full-size
   - [ ] Verify performance acceptable

**Expected Results**:

- Smooth scrolling with large datasets
- Pagination or virtualization for long lists
- Lazy loading for images
- No memory leaks or crashes

**Flag if**: Laggy scrolling, crashes, or OOM errors

---

### Performance Test 4: Media Upload Performance

**Test Steps**:

1. **Large Image Upload**:
   - [ ] Select 2MB image for upload
   - [ ] Start upload
   - [ ] Verify progress indicator displays
   - [ ] Measure upload time
   - [ ] Verify upload completes successfully

2. **Large Video Upload**:
   - [ ] Select 10MB, 30-second video
   - [ ] Start upload
   - [ ] Verify progress indicator
   - [ ] Measure upload time
   - [ ] Verify upload completes

3. **Multiple File Uploads**:
   - [ ] Select 5 files (mix of images/videos)
   - [ ] Start upload
   - [ ] Verify uploads queued or parallel
   - [ ] Verify progress for each file
   - [ ] Verify all uploads complete

**Expected Results**:

- Upload progress visible
- 2MB image uploads < 30 seconds (on decent connection)
- 10MB video uploads < 2 minutes
- Multiple uploads don't block UI

**Flag if**: Uploads fail frequently, no progress indication, or UI freezes

---

## Security & Privacy Testing

### Security Test 1: Authentication & Session Management

**Test Steps**:

1. **Login Session Persistence**:
   - [ ] Login to app
   - [ ] Close app completely
   - [ ] Wait 10 minutes
   - [ ] Reopen app
   - [ ] Verify still logged in (token refresh)
   - [ ] Wait 24+ hours (session timeout)
   - [ ] Reopen app
   - [ ] Verify logged out and prompted to login

2. **Password Security**:
   - [ ] During registration, inspect password field
   - [ ] Verify password masked (not visible)
   - [ ] Use password visibility toggle
   - [ ] Verify password becomes visible
   - [ ] Submit form
   - [ ] Verify password NOT sent in plain text (check network logs if possible)

3. **Session Invalidation on Logout**:
   - [ ] Login
   - [ ] Logout
   - [ ] Try navigating to protected screen
   - [ ] Verify redirected to login

**Expected Results**:

- Session tokens securely stored
- Token refresh works
- Session timeout enforced (24 hours)
- Passwords masked
- Logout clears session

**Flag if**: Passwords visible in network logs, session never expires, or logout doesn't clear token

---

### Security Test 2: Payment Security

**Test Steps**:

1. **Payment Data Handling**:
   - [ ] Enter payment details (card number, CVV)
   - [ ] Verify card number masked (e.g., **** 1234)
   - [ ] Verify CVV not stored after payment
   - [ ] Check network logs (if possible)
   - [ ] Verify payment details sent to processor, not Hairline backend

2. **PCI Compliance**:
   - [ ] Verify Hairline app does NOT store card numbers
   - [ ] Verify only payment processor handles sensitive card data
   - [ ] Verify tokenization used (card token, not actual card)

**Expected Results**:

- Card numbers masked in UI
- CVV not stored
- Payment data sent to processor only (PCI DSS compliant)

**Flag if**: Card data visible, stored locally, or sent to Hairline backend

---

### Security Test 3: Data Privacy & Encryption

**Test Steps**:

1. **Patient Identity Masking**:
   - [ ] Before payment, verify provider CANNOT see patient full name/contact
   - [ ] Verify patient displayed as "Mark P. - PAT-00123" or similar
   - [ ] Complete payment
   - [ ] Verify provider NOW sees full patient name/contact (unmasked)

2. **Secure Messaging**:
   - [ ] Send message with sensitive information (e.g., medical details)
   - [ ] Verify message encrypted in transit (HTTPS)
   - [ ] Verify message stored securely on backend

3. **Account Deletion**:
   - [ ] Request account deletion
   - [ ] Verify soft-delete (not hard-delete)
   - [ ] Verify cannot login after deletion
   - [ ] Verify data archived securely (not fully deleted for 7-year compliance)

**Expected Results**:

- Patient identity masked until payment
- All data encrypted in transit (HTTPS)
- Soft-delete with data retention for compliance

**Flag if**: Patient identity revealed before payment, unencrypted data transmission, or hard-delete without retention

---

## Platform-Specific Testing

### iOS-Specific Tests

1. **Device Compatibility**:
   - [ ] Test on iPhone SE (small screen)
   - [ ] Test on iPhone 14/15 (standard)
   - [ ] Test on iPhone 14/15 Pro Max (large screen)
   - [ ] Test on iPad (tablet)
   - [ ] Verify UI adapts to screen sizes

2. **iOS Version Compatibility**:
   - [ ] Test on iOS 15 (minimum supported?)
   - [ ] Test on iOS 16
   - [ ] Test on latest iOS 17+
   - [ ] Verify no breaking issues

3. **iOS-Specific Features**:
   - [ ] Test Face ID / Touch ID (if supported for login/payments)
   - [ ] Test Apple Pay (if supported)
   - [ ] Test push notifications (APNS)
   - [ ] Test camera/photo library permissions
   - [ ] Test calendar integration (Add to Calendar)

4. **iOS Settings Integration**:
   - [ ] Disable notifications in iOS Settings > Verify app respects
   - [ ] Disable camera access > Verify app handles gracefully
   - [ ] Disable location access (if used) > Verify app handles

**Flag if**: UI broken on any device, features don't work on older iOS versions, or permissions not handled

---

### Android-Specific Tests

1. **Device Compatibility**:
   - [ ] Test on small screen Android (e.g., Pixel 6a)
   - [ ] Test on standard Android (e.g., Samsung Galaxy S22)
   - [ ] Test on large screen Android (e.g., Samsung Galaxy S22 Ultra)
   - [ ] Test on Android tablet
   - [ ] Verify UI adapts to screen sizes

2. **Android Version Compatibility**:
   - [ ] Test on Android 10 (minimum supported?)
   - [ ] Test on Android 11
   - [ ] Test on Android 12+
   - [ ] Verify no breaking issues

3. **Android-Specific Features**:
   - [ ] Test fingerprint auth (if supported)
   - [ ] Test Google Pay (if supported)
   - [ ] Test push notifications (FCM)
   - [ ] Test camera/gallery permissions
   - [ ] Test calendar integration
   - [ ] Test back button navigation (hardware back)

4. **Android Settings Integration**:
   - [ ] Disable notifications in Android Settings > Verify app respects
   - [ ] Disable camera access > Verify app handles gracefully
   - [ ] Disable location access (if used) > Verify app handles

5. **OEM Variations**:
   - [ ] Test on Samsung device (One UI)
   - [ ] Test on Google Pixel (stock Android)
   - [ ] Verify consistent behavior across OEMs

**Flag if**: UI broken on any device, features don't work on older Android versions, or OEM-specific bugs

---

## Test Deliverables & Reporting

### Test Execution Report Template

For each test session, document:

1. **Session Information**:
   - Date & Time
   - Tester Name
   - App Version/Build Number
   - Device Model & OS Version
   - Network Condition (WiFi, 4G, 5G, Simulated slow)

2. **Tests Executed**:
   - Module tested
   - Test scenarios completed
   - Pass/Fail status

3. **Issues Found**:
   - Issue ID (unique number)
   - Severity (Critical, High, Medium, Low)
   - Module affected
   - Screen/Feature
   - Steps to reproduce
   - Expected vs Actual result
   - Screenshots/Video
   - Network logs (if relevant)

4. **Summary**:
   - Total tests executed
   - Passed tests
   - Failed tests
   - Critical issues count
   - High issues count
   - Recommendations (Approve/Revise/Reject)

---

### Issue Tracking Spreadsheet

Create a spreadsheet with columns:

| Issue ID | Severity | Module | Screen | Description | Steps to Reproduce | Expected | Actual | Status | Assigned To | Notes |
|----------|----------|--------|--------|-------------|-------------------|----------|--------|--------|-------------|-------|
| 001 | Critical | Payment | Checkout | Payment fails without error | 1. Enter invalid card... | Clear error message | Blank screen | Open | Dev Team | Blocks release |
| 002 | High | Messaging | Inbox | Unread badge not updating | 1. Receive message... | Badge updates | Badge shows 0 | Open | Dev Team | |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

### Final Approval Checklist

Before recommending approval for release, verify:

- [ ] All Critical issues resolved
- [ ] All High issues resolved or acceptable workarounds documented
- [ ] Medium/Low issues documented for future sprints
- [ ] End-to-end happy path successful on both iOS and Android
- [ ] Payment flows work correctly (deposit, final payment, refunds)
- [ ] No data loss or corruption observed
- [ ] Performance acceptable (screens load < 3 seconds)
- [ ] Accessibility minimums met (readable text, tappable buttons)
- [ ] Security basics verified (auth, payment, data privacy)
- [ ] No app crashes during testing
- [ ] All PRD requirements implemented (or gaps documented)
- [ ] Client requirements from transcriptions verified (3D scan timeline, monitoring, messaging)

**Recommendation**:

- [ ] **Approve for Release**: All critical issues resolved, app ready for production
- [ ] **Approve with Conditions**: Minor issues remain but release acceptable with plan to fix
- [ ] **Request Revisions**: Significant issues must be fixed before release
- [ ] **Reject**: Critical flaws, not ready for release

---

## Appendix: Testing Tools & Resources

### Recommended Tools

1. **Screen Recording**:
   - iOS: Built-in screen recording
   - Android: ADB screenrecord or built-in
   - Third-party: Loom, OBS

2. **Network Simulation**:
   - iOS: Xcode Network Link Conditioner
   - Android: Chrome DevTools Remote Debugging
   - Charles Proxy (HTTP/HTTPS debugging)

3. **Accessibility Testing**:
   - iOS: VoiceOver
   - Android: TalkBack
   - Color contrast checker: WebAIM Contrast Checker

4. **Issue Tracking**:
   - Google Sheets / Excel
   - Jira, Linear, or similar
   - Screenshot annotation: Skitch, Markup

5. **Test Account Management**:
   - Password manager for test accounts
   - Spreadsheet with test user credentials

---

## Conclusion

This comprehensive testing plan covers all critical patient-facing features of the Hairline mobile app. By following this plan systematically, you will:

1. Verify all PRD requirements implemented correctly
2. Identify technical and UX/UI issues before release
3. Ensure smooth end-to-end user experience
4. Provide clear recommendation for release approval
5. Document gaps for future development

**Next Steps**:

1. Review this testing plan and adjust based on your needs
2. Set up test environment (devices, accounts, tools)
3. Execute tests module by module
4. Document all findings in issue tracking spreadsheet
5. Prepare final test report with recommendation

**Estimated Testing Time**: 40-60 hours for comprehensive coverage (depending on tester familiarity and issue count)

Good luck with testing! 🚀
