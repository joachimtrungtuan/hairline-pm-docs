# FR-032 - Provider Dashboard Settings & Profile Management

**Module**: PR-06: Profile & Settings Management
**Feature Branch**: `fr032-provider-dashboard-settings`
**Created**: 2025-11-17
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-032 from system-prd.md

---

## Executive Summary

Provider Dashboard Settings & Profile Management enables clinic administrators and staff to configure their organization's profile, account settings, notification preferences, billing information, and team member permissions. This module provides providers with full control over their public-facing clinic information (logo, awards, languages), account security (password, phone, timezone), unified notification preferences (email, push), billing setup (bank accounts for payouts), and access to comprehensive help resources. The module serves as the centralized configuration hub for all provider-level settings, ensuring providers can efficiently manage their presence on the Hairline platform while maintaining security and compliance.

**Key Value Delivered**:

- **Providers**: Complete control over clinic branding, communication preferences, and payout settings
- **Hairline Admin**: Reduced support tickets through self-service settings and help center
- **Platform**: Consistent provider data quality and secure credential management

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: No direct patient-facing functionality (patients view provider profiles, which may be initially curated by admin but subsequent provider-made changes propagate directly)
- **Provider Platform (PR-06)**: Full settings and profile management for clinic staff
- **Admin Platform (A-XX)**: Admin manages Help Centre content, views provider profile quality metrics
- **Shared Services (S-XX)**: S-03 (Notification Service) for preference enforcement, S-02 (Payment Service) for billing validation

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- Patients view read-only provider profiles (managed through PR-06) during quote comparison
- No direct patient interaction with this module

**Provider Platform (PR-06)**:

- Providers upload and manage clinic logo/profile picture
- Providers select supported languages from system language options
- Providers add, edit, delete awards with direct image upload
- Providers update basic clinic information (name, description, contact)
- Providers manage account settings (phone, timezone, password)
- Providers configure unified notification preferences (individual toggles + global channel preferences)
- Providers (Owner role only) manage billing settings (bank account details)
- Providers access Help Centre with read-only content
- Providers submit support requests via Contact Support form (Screen 5.5) and feedback via Feedback & Suggestions form (Screen 5.6)
- Providers view all their submitted support cases and feedback via My Support Cases screen (Screen 5.7) with complete case details, communication thread, and status tracking
- Providers engage in two-way communication with admin by replying to admin messages within their support cases
- Providers request to reopen closed cases if issue persists or resolution was unsatisfactory (the admin decides; the case stays Closed until then)
- The Owner requests account closure (admin processes the request by deactivating the provider in FR-015; no self-service deactivation)
- Providers browse Reviews as a tab within the Provider Profile detailed page to read patient feedback, filter by rating, and post public responses to individual reviews (response composer defined in FR-013 Screen 6)

**Admin Platform (A-XX)**:

- Admins create and manage Help Centre content (FAQs, guides, videos, resources)
- Admins process provider account-closure requests by deactivating the provider in FR-015

**Shared Services (S-XX)**:

- **S-03 (Notification Service)**: Enforces provider notification preferences when sending alerts
- **S-02 (Payment Service)**: Validates bank account information format for payouts

### Communication Structure

**In Scope**:

- Email notifications based on provider preferences (quote alerts, schedule updates, review notifications)
- Push/In-app notifications for web portal activity
- Help Centre contact support form submission

**Out of Scope**:

- Real-time chat between provider and patient (handled by P-06: Communication)
- Video consultations (handled by aftercare modules)
- Internal team messaging (future enhancement)

### Entry Points

**Provider-Initiated**:

- Provider navigates to "Settings & Support > Settings" from main dashboard navigation (REQ-032-032)
- Provider clicks on notification icon to configure preferences (REQ-032-032)
- Provider accesses Help Centre from footer or help icon (REQ-032-032)
- Provider Owner role accesses billing settings from financial dashboard (REQ-032-032)

**System-Initiated**:

- System prompts provider to complete profile setup during onboarding (REQ-032-032)
- System sends notification approval requests when admin creates platform-wide discount (REQ-032-032)

---

## Business Workflows

### Main Flow: Update Provider Profile Information

**Actors**: Provider (Owner, Manager), System
**Trigger**: Provider navigates to "Profile" section and clicks "Edit Profile"
**Outcome**: Provider profile information updated and visible to patients during quote comparison

**Steps**:

1. Provider navigates to Settings & Support > Provider profile
2. System displays current profile data (logo, name, description, languages, awards) in tabs
3. Provider clicks "Edit Profile" button
4. System loads profile editor with existing data pre-filled
5. Provider uploads new clinic logo/profile picture (optional)
   - System validates image format (JPEG, PNG) and size (<5MB)
   - System displays image preview
6. Provider selects supported languages from multi-select dropdown (consumes the FR-021 language/locale catalog surfaced through settings)
7. Provider edits clinic name, description, contact email, Location - City
8. Provider clicks "Add Award" to add new award entry
   - System opens award form (name, issuer/organization, description, year, award image)
   - Provider fills award details and uploads award image
   - System validates award image (<2MB)
9. Provider clicks "Save Changes" on the current tab
10. System validates all required fields for the current tab (clinic name, description)
11. System saves profile updates for the current tab with timestamp
    - On clinic name save, System sets the Owner's Account Name to the clinic name (REQ-032-061)
12. System displays success message "Profile updated successfully"
13. System logs profile change in audit trail (user, timestamp, fields changed)
14. System updates provider profile in quote comparison views (visible to patients)
15. System removes unsaved changes indicator for the saved tab

### Alternative Flows

**A1: Provider Edits Existing Award**:

- **Trigger**: Provider clicks "Edit" icon on existing award entry
- **Steps**:
  1. System opens award editor pre-filled with existing award data
  2. Provider modifies award name, issuer/organization, description, year, or replaces award image
  3. Provider clicks "Save"
  4. System validates changes and updates award entry
  5. System displays success message
- **Outcome**: Award information updated in provider profile

**A2: Provider Deletes Award**:

- **Trigger**: Provider clicks "Delete" icon on award entry
- **Steps**:
  1. System displays confirmation dialog "Are you sure you want to delete this award?"
  2. Provider confirms deletion
  3. System removes award from profile (soft-delete, retained in archive) (REQ-032-046)
  4. System displays success message "Award deleted"
- **Outcome**: Award removed from public provider profile

**A3: Provider Selects Multiple Languages**:

- **Trigger**: Provider opens language selection dropdown
- **Steps**:
  1. System displays the languages from the FR-021 language/locale catalog surfaced through settings: the offered list holds the Active and Preparation locales, every catalog locale already saved on the profile is shown, and a saved language stays on the profile when its locale becomes Inactive (REQ-032-147)
  2. Provider selects multiple languages (e.g., English, Turkish, Spanish)
  3. System updates language tags in profile
  4. System saves language preferences
- **Outcome**: Provider profile shows all selected languages to patients

**B1: Image Upload Fails Validation**:

- **Trigger**: Provider uploads image exceeding size limit or unsupported format
- **Steps**:
  1. System validates uploaded image
  2. System detects validation failure (e.g., 8MB PNG file, limit is 5MB)
  3. System displays error message "Image too large. Maximum size is 5MB. Please compress or choose a smaller image."
  4. Provider either compresses image or selects different file
  5. Provider re-uploads valid image
- **Outcome**: Valid image uploaded or user cancels operation

**B2: Required Field Missing**:

- **Trigger**: Provider attempts to save profile with empty required field
- **Steps**:
  1. Provider clicks "Save Changes" with clinic name field empty
  2. System validates form
  3. System detects missing required field
  4. System highlights clinic name field in red
  5. System displays error message "Clinic name is required"
  6. Provider fills in clinic name
  7. Provider clicks "Save Changes" again
  8. System successfully saves profile
- **Outcome**: Profile saved after required field completed

**B3: Network Connection Lost During Upload**:

- **Trigger**: Network disconnects while provider is uploading award image
- **Steps**:
  1. Provider uploads award image (3MB file)
  2. Upload progress reaches 50%
  3. Network connection drops
  4. System detects upload failure
  5. System displays error message "Upload failed due to network issue. Please check your connection and try again."
  6. Provider checks network connection
  7. Provider clicks "Retry Upload"
  8. System resumes upload from beginning (or uses resumable upload if implemented)
- **Outcome**: Upload completes after retry or user cancels

---

### Main Flow: Configure Notification Preferences

**Actors**: Provider (holders of the FR-031 permission "Edit Notification Settings", by default the Owner and a Manager, can change; other roles see the settings read-only, REQ-032-142), System
**Trigger**: Provider navigates to "Settings" → "Notifications"
**Outcome**: Provider notification preferences updated and enforced by S-03 Notification Service

**Steps**:

1. Provider navigates to Settings → Notifications
2. System displays unified notification settings with two sections:
   - **Section A: Notification Types** (individual toggles)
   - **Section B: Global Channel Preferences** (email, push)
3. Provider reviews current settings (all loaded from database)
4. Provider toggles individual notification types (all six are on by default; the unchecked Aftercare line below is only an example):
   - ☑ Quote Notifications (new inquiry received, quote expiring soon). This toggle does not cover mandatory quote notices (the inquiry-cancelled quote notice and the quote-accepted outcomes), which have no toggle
   - ☑ Schedule Notifications (appointment confirmed, appointment reminder). This toggle does not cover mandatory booking notices (payment window expired, booking revived, booking rescheduled), which have no toggle
   - ☑ Treatment Start Notifications (patient checked in, procedure started)
   - ☐ Aftercare Notifications (patient milestone completed, urgent aftercare alert) — DISABLED
   - ☑ Review Notifications (new review posted, review requires response)
   - ☑ Promotion/Discount Notifications (new platform discounts created by admin that require provider acceptance/opt-in)
   - Support case notices (admin reply, status change, resolved) have no toggle and are always sent (REQ-032-143)
5. Provider configures global channel preferences:
   - Email: ☑ Enabled (default email address from profile)
   - Push/In-App: ☑ Enabled (web portal notifications)
   - Email and Push may both be off for a type; mandatory notices ignore the setting and are still sent (REQ-032-143)
6. Provider clicks "Save Preferences" on the Notifications tab
7. System validates settings
8. System saves notification preferences to database
9. System displays success message "Notification preferences updated"
10. System logs preference change in audit trail (REQ-032-082, REQ-032-142)
11. System updates S-03 Notification Service with new preference rules
12. S-03 enforces preferences for all future notifications (e.g., aftercare notifications will NOT be sent)

### Supporting Flow: Browse Reviews

**Actors**: Provider (any role), System  
**Trigger**: Provider selects `Reviews` tab within the Provider Profile detailed page  
**Outcome**: Provider views Reviews tab to filter/sort reviews and read full feedback that corresponds to review notifications.

**Steps**:

1. Provider opens Provider Profile page and selects Reviews tab.
2. System loads rating summary, distribution bars, filters, and first page of review cards; a card for a review the patient edited after publishing shows the "Edited" marker (FR-013 REQ-013-032, REQ-032-148).
3. Provider applies rating filters or changes sort order (e.g., "Most recent").
4. System runs the filter, sort and paging on the server over the whole review list (not only the page on screen) and updates the list; provider paginates if needed to view more results (REQ-032-148).
5. If provider arrived via a Review Notification, the associated review is auto-highlighted/highlighted within list.

**Outcome**: Provider can quickly review patient sentiment and correlate it with notifications without modifying review content.

### Alternative Flows

**A5: Provider Disables All Notification Types**:

- **Trigger**: Provider unchecks all notification type toggles
- **Steps**:
  1. Provider disables all six notification types
  2. Provider clicks "Save Preferences"
  3. System displays confirmation dialog "Warning: You have disabled all notifications. You may miss important updates about inquiries, appointments, and reviews. Are you sure?"
  4. Provider confirms or cancels
  5. If confirmed, system saves "all disabled" preference
  6. S-03 stops sending notifications to this provider (except critical system alerts and mandatory notices such as the inquiry-cancelled quote notice (FR-020 `quote.cancelled_inquiry`))
- **Outcome**: Provider receives no notifications except critical platform alerts

**B4: Network Error During Save**:

- **Trigger**: Network connection fails while saving notification preferences
- **Steps**:
  1. Provider clicks "Save Preferences"
  2. System sends save request to backend
  3. Network connection times out
  4. System displays error message "Failed to save preferences. Please check your connection and try again."
  5. Provider checks connection
  6. Provider clicks "Save Preferences" again
  7. System successfully saves preferences
- **Outcome**: Preferences saved after retry

---

### Main Flow: Update Account Settings (Phone, Timezone, Password)

**Actors**: Provider (any role, for their own account only, REQ-032-141), System
**Trigger**: Provider navigates to "Settings" → "Account Settings"
**Outcome**: Provider account settings updated (phone number with country code, timezone, password)

**Steps**:

1. Provider navigates to Settings → Account Settings
   - First login only: when a person signs in for the first time, System silently sets their timezone to the listed whole-hour offset nearest to the browser's time zone, or to UTC when the browser zone cannot be read; there is no prompt, and the person can change it at any time (REQ-032-145)
2. System displays account settings form with current values:
   - Phone Number: +90 555 123 4567 (country code + number)
   - Timezone: (GMT+3) Istanbul
   - Account Email: shown read-only for every role (REQ-032-144)
   - Password: ●●●●●●●● (masked)
3. Provider clicks "Edit Phone Number"
4. System displays phone number editor with country code dropdown (consumes FR-026 country calling codes list)
5. Provider selects country code from worldwide list (e.g., +44 for UK)
6. Provider enters phone number (e.g., 7700 900123)
7. System validates phone number format for selected country code
8. Provider clicks "Save Phone Number"
9. System saves phone number in international format (+44 7700 900123) after checking that it is unique per user within the provider; a changed number is verified as in FR-009 (REQ-009-113, REQ-032-125)
   - System logs the account settings change in the audit trail, with the phone values masked (REQ-032-020)
10. Provider clicks "Change Timezone"
11. System displays timezone dropdown with multiple timezone options (GMT-12 to GMT+14)
12. Provider selects timezone (e.g., (GMT+0) London)
13. System saves the timezone preference for this person only; dates display with the fixed offsets of the FR-026 list (REQ-026-121, REQ-032-145)
    - System logs the account settings change in the audit trail (REQ-032-020)
14. Provider clicks "Change Password"
15. System displays password change form:
    - Current Password: [input field]
    - New Password: [input field]
    - Confirm New Password: [input field]
16. Provider enters current password and new password (following REQ-SYS-007)
17. System validates:
    - Current password matches database
    - New password meets the password policy. See system PRD, Platform-Wide Rules: Password and one-time-code policy
    - New password matches confirmation
18. System hashes new password using bcrypt (cost factor 12+)
19. System saves new password hash
20. System logs password change event in audit trail (timestamp, user ID, IP address)
21. System displays success message "Password changed successfully"
22. System sends email notification to provider's email address "Your password was changed on [date] at [time]"

### Alternative Flows

**A6: Provider Changes Only Phone Number**:

- **Trigger**: Provider only needs to update phone number
- **Steps**:
  1. Provider edits phone number field
  2. Provider saves phone number
  3. System validates and saves phone number
  4. Other account settings (timezone, password) remain unchanged
- **Outcome**: Phone number updated, other settings unchanged

**A7: Provider Changes Timezone for Different Region**:

- **Trigger**: Provider works in a different timezone from the one saved
- **Steps**:
  1. Provider selects new timezone from dropdown
  2. System saves timezone preference for this person only; other team members keep their own (REQ-032-145)
  3. All future timestamps in this person's provider dashboard display in new timezone
  4. Existing data timestamps remain in UTC but display converted to new timezone
- **Outcome**: Provider sees all dates/times in new local timezone (fixed offsets of the FR-026 list, REQ-026-121)

**B5: Invalid Phone Number Format**:

- **Trigger**: Provider enters phone number in incorrect format for selected country
- **Steps**:
  1. Provider selects country code +1 (USA)
  2. Provider enters phone number "123" (too short)
  3. Provider clicks "Save Phone Number"
  4. System validates phone number
  5. System detects invalid format (USA requires 10 digits)
  6. System displays error "Invalid phone number for United States. Expected format: (XXX) XXX-XXXX"
  7. Provider corrects phone number to "555-123-4567"
  8. System validates and saves phone number
- **Outcome**: Valid phone number saved after correction

**B6: Current Password Incorrect**:

- **Trigger**: Provider enters wrong current password when changing password
- **Steps**:
  1. Provider enters incorrect current password
  2. Provider enters new password and confirmation
  3. Provider clicks "Change Password"
  4. System validates current password against database
  5. System detects password mismatch
  6. System displays error "Current password is incorrect"
  7. Provider re-enters correct current password
  8. Provider clicks "Change Password" again
  9. System successfully changes password
- **Outcome**: Password changed after entering correct current password

**B7: New Password Does Not Meet Security Policy**:

- **Trigger**: Provider enters new password that fails password policy validation
- **Steps**:
  1. Provider enters current password correctly
  2. Provider enters new password "password123" (missing uppercase, special char)
  3. Provider clicks "Change Password"
  4. System validates new password against the platform password policy (REQ-SYS-007)
  5. System detects policy violations
  6. System displays error "Password must contain at least 12 characters, one uppercase letter, one lowercase letter, one digit, and one special character from !@#$%^&(),.?\":{}|<>"
  7. Provider enters stronger password "MyP@ssw0rd2024!"
  8. System validates and accepts new password
- **Outcome**: Password changed after meeting security requirements

**B8: Password Confirmation Mismatch**:

- **Trigger**: Provider's new password and confirmation do not match
- **Steps**:
  1. Provider enters new password "MyP@ssw0rd2024!"
  2. Provider enters confirmation "MyP@ssword2024!" (typo in confirmation)
  3. Provider clicks "Change Password"
  4. System compares new password and confirmation
  5. System detects mismatch
  6. System displays error "Password confirmation does not match"
  7. Provider re-enters confirmation correctly
  8. System successfully changes password
- **Outcome**: Password changed after correct confirmation

---

### Main Flow: Manage Billing Settings (Owner Role Only)

**Actors**: Provider (Owner role), System
**Trigger**: Provider Owner navigates to "Settings" → "Billing" or "Billing Settings"
**Outcome**: Bank account details saved for provider payouts (FR-017 integration)

**Steps**:

1. Provider Owner navigates to Settings → Billing
2. System validates the user holds the "View and Edit Billing Settings" permission (FR-031, default Owner only, REQ-032-141)
3. System shows the form for the clinic's Payout Method (REQ-032-146). For Manual bank transfer it displays the bank account details (if previously saved); for Stripe Connect it displays a status panel with a "Complete Stripe sign-up" link instead of the bank form:
   - Account Holder Name: [text field]
   - Bank Name: [text field]
   - Account Number: [masked, e.g., ●●●●●●1234]
   - Routing/SWIFT Code: [text field]
   - IBAN (if applicable): [text field]
4. Provider Owner clicks "Edit Bank Account Details"
5. System displays editable form with current values (account number unmasked)
6. Provider Owner updates bank account information (Manual bank transfer only; the bank form is shown and required only for this Payout Method, REQ-032-146):
   - Account Holder Name: "Istanbul Hair Clinic Ltd"
   - Bank Name: "Garanti BBVA"
   - Account Number: "TR123456789012345678901234"
   - SWIFT Code: "TGBATRISXXX"
   - IBAN: "TR12 0001 0012 3456 7890 1234 56"
7. System validates bank account information:
   - Account holder name required
   - Account number format valid for selected country
   - SWIFT/routing code format valid
   - IBAN format valid (if provided)
8. Provider Owner clicks "Save Bank Account"
9. System sends validation request to S-02 Payment Service (verify bank account details format)
10. S-02 validates bank account details structure
11. System saves bank account information with encryption at rest
12. System logs billing settings change in audit trail (Owner user, timestamp, action)
13. System displays success message "Bank account details saved successfully"
14. System sends confirmation email to Owner email address
15. Bank account details now used for provider payouts (FR-017 billing workflow)

### Alternative Flows

**A8: Provider Owner Views Billing Settings (Read-Only)**:

- **Trigger**: Provider Owner wants to review current bank account details
- **Steps**:
  1. Provider Owner navigates to Settings → Billing
  2. System displays current bank account details (masked account number)
  3. Provider Owner reviews information
  4. Provider Owner does not make changes
- **Outcome**: Provider confirms bank account details are correct

**A9: Provider Owner Adds Bank Account for First Time**:

- **Trigger**: Provider Owner has not yet added bank account details
- **Steps**:
  1. Provider Owner navigates to Settings → Billing
  2. System displays empty billing form with message "No bank account on file. Add your bank account details to receive payouts."
  3. Provider Owner (Payout Method Manual bank transfer) fills in all bank account fields; for Stripe Connect the panel with the "Complete Stripe sign-up" link is shown instead (REQ-032-146)
  4. System validates and saves bank account details
  5. System displays success message "Bank account added successfully. You will now receive payouts to this account."
- **Outcome**: Bank account details saved, provider can receive payouts

**B9: Non-Owner Role Attempts to Access Billing Settings**:

- **Trigger**: Any non-Owner provider role (Manager, Clinical Staff, Billing Staff) tries to access billing settings
- **Steps**:
  1. Provider (non-Owner role) navigates to Settings & Support > Settings > Billing tab
  2. System validates user role
  3. System detects user role ≠ Owner
  4. System hides the Billing tab from navigation (non-owner cannot see or access billing settings)
- **Outcome**: Non-owner cannot see or access billing settings (permission "View and Edit Billing Settings", FR-031, default Owner only, REQ-032-141)

**B10: Invalid Bank Account Format**:

- **Trigger**: Provider Owner enters bank account information in invalid format
- **Steps**:
  1. Provider Owner enters IBAN "TR1234" (too short, invalid format)
  2. Provider Owner clicks "Save Bank Account"
  3. System validates IBAN format
  4. System detects invalid IBAN (Turkey IBAN requires 26 characters)
  5. System displays error "Invalid IBAN format. Turkey IBAN must be 26 characters (e.g., TR12 0001 0012 3456 7890 1234 56)"
  6. Provider Owner corrects IBAN to valid format
  7. System validates and saves bank account details
- **Outcome**: Valid bank account details saved after correction

**B11: S-02 Payment Service Validation Fails**:

- **Trigger**: S-02 Payment Service detects bank account details cannot be validated
- **Steps**:
  1. Provider Owner submits bank account details
  2. System sends validation request to S-02
  3. S-02 attempts to validate bank account details
  4. S-02 returns validation error (e.g., bank not found, SWIFT code mismatch)
  5. System displays error "Bank account validation failed: [error detail from S-02]. Please verify your bank details and try again."
  6. Provider Owner reviews and corrects bank details
  7. Provider Owner re-submits
  8. S-02 successfully validates bank account
  9. System saves bank account details
- **Outcome**: Valid bank account saved after correction

---

### Main Flow: Access Help Centre Resources

**Actors**: Provider (any role), System
**Trigger**: Provider navigates to "Help Centre" from settings menu or footer
**Outcome**: Provider accesses help resources, FAQs, guides, and contact support backed by admin-managed content (FR-033) and unified ticketing (FR-034)

**Steps**:

1. Provider clicks "Help Centre" from settings menu or footer link
2. System loads Help Centre page with content categories (managed by admin via FR-033)
3. System displays Help Centre categories:
   - **FAQs** (expandable/collapsible sections organized by topic; content from FR-033)
   - **Tutorial Guides / Troubleshooting Tips / Policy Information** (article layout; content from FR-033)
   - **Resource Library** (downloadable documents, templates; content from FR-033)
   - **Video Tutorials** (video guides for key workflows; content from FR-033)
   - **Service Status** (platform uptime and incident reports; status data managed in FR-033)
   - **Contact Support** (support form submission; cases managed in FR-034)
   - **Feedback & Suggestions** (submit feature requests; cases managed in FR-034)
   - **Community Forum** (provider discussions - future enhancement)
4. Provider clicks on "FAQs" category
5. System displays FAQ topics (e.g., "Quote Management", "Payment Settings", "Aftercare")
6. Provider clicks on topic "Quote Management"
7. System displays expandable FAQ questions within topic
8. Provider clicks on question "How do I edit a quote after submission?"
9. System expands answer with detailed instructions and records the view through the FR-033 view write (REQ-033-097)
10. Provider reads answer
11. Provider clicks "Was this helpful?" feedback (Yes/No)
12. System records the vote through the FR-033 vote write for admin analytics (REQ-033-096)
13. Provider navigates to "Tutorial Guides" category
14. System displays guide list (e.g., "How to Create Your First Quote", "Setting Up Notifications")
15. Provider clicks on guide "How to Create Your First Quote"
16. System displays step-by-step guide with screenshots and records the view through the FR-033 view write (REQ-033-097)
17. Provider reads guide
18. Provider returns to Help Centre home
19. Provider clicks "Contact Support"
20. System displays support contact form:
    - Subject: [text field]
    - Category: [dropdown - optional]
    - Message: [textarea]
    - Priority: [dropdown - optional, default Medium]
    - Attachment: [file upload - optional]
21. Provider fills form and submits support request
22. System sends support request to admin team
23. System displays confirmation "Support request submitted. Case #[number]. We aim to respond within 24 hours on business days."

### Alternative Flows

**A10: Provider Downloads Resource from Resource Library**:

- **Trigger**: Provider needs downloadable template or document
- **Steps**:
  1. Provider navigates to "Resource Library" category
  2. System displays list of downloadable resources (PDFs, templates, guides)
  3. Provider clicks "Download Quote Template"
  4. System records the view through the FR-033 view write (REQ-033-097) and initiates file download
  5. Provider saves file to local device
- **Outcome**: Provider downloads resource file

**A11: Provider Watches Video Tutorial**:

- **Trigger**: Provider prefers video learning format
- **Steps**:
  1. Provider navigates to "Video Tutorials" category
  2. System displays video list with thumbnails
  3. Provider clicks on video "How to Manage Inquiries"
  4. System loads video player
  5. Provider watches video tutorial
  6. After 30 seconds of play the system records the view through the FR-033 view write (REQ-033-097, REQ-032-099)
  7. Provider clicks "Was this helpful?" feedback; System records the vote through the FR-033 vote write (REQ-033-096)
- **Outcome**: Provider learns from video tutorial

**A12: Provider Submits Feedback/Feature Request**:

- **Trigger**: Provider has suggestion for platform improvement
- **Steps**:
  1. Provider navigates to "Feedback & Suggestions" category
  2. System displays feedback submission form
  3. Provider describes feature request or improvement idea
  4. Provider submits feedback
  5. System saves feedback for admin review
  6. System displays "Thank you for your feedback!"
- **Outcome**: Provider feedback submitted to admin team
- **Integration**: Feedback case is created and managed in FR-034 Support Center & Ticketing

**A13: Provider Checks Service Status**:

- **Trigger**: Provider experiences platform issues and wants to check if it's a known system outage
- **Steps**:
  1. Provider navigates to Help Centre and selects "Service Status" category
  2. System calls Service Status endpoint backed by FR-033 and loads status page interface
  3. System displays overall platform status indicator (All Systems Operational, Partial Outage, Major Outage, or Status not available when no status can be shown; the status values are owned by FR-033, REQ-033-080)
  4. System shows list of service components with current status and last updated time
  5. System displays recent incident history timeline and upcoming maintenance schedule (if any)
  6. Provider reviews status information to determine whether issue is platform-wide or local
  7. Provider decides whether to wait, retry, or contact support (Contact Support flows above)
- **Outcome**: Provider is informed of current platform status and can plan accordingly

**B12: Help Centre Content Not Loading**:

- **Trigger**: Network issue or server error prevents Help Centre content from loading
- **Steps**:
  1. Provider navigates to Help Centre
  2. System attempts to load content from admin-managed content database
  3. Request times out or fails
  4. System displays error "Unable to load Help Centre content. Please check your connection and try again."
  5. Provider refreshes page
  6. System successfully loads content
- **Outcome**: Help Centre content loads after retry

**B13: Provider Cannot Find Needed Content (Content Gap Feedback)**:

- **Trigger**: Provider cannot find relevant help content in Help Centre
- **Steps**:
  1. Provider browses categories and/or uses search but does not find an answer
  2. Provider clicks "Was this helpful? No" or similar feedback control on an article/FAQ
  3. System prompts provider to briefly describe what they were looking for
  4. Provider submits content-gap feedback form
  5. System records feedback with reference to the viewed content item and provider account (REQ-032-095)
  6. System forwards feedback to admin/content team via FR-034 (e.g., as a low-priority ticket or feedback case) (REQ-032-095)
- **Outcome**: Content gap is captured for admins to review and action in FR-033 content management / FR-034 ticketing

**B14: Uploaded File or Video Fails to Load**:

- **Trigger**: Provider attempts to download a resource or play a video but the file fails to load
- **Steps**:
  1. Provider clicks on tutorial guide, resource file, or video link in the Help Centre
  2. System attempts to fetch file from media storage (S-05) using metadata from FR-033
  3. File fetch fails (e.g., network error, file missing, permission issue)
  4. System displays a clear error message with retry option
  5. System offers a "Report issue" or similar action
  6. Provider clicks "Report issue"
  7. System creates an issue/support case in FR-034 including file identifier, provider, and error details (REQ-032-096)
  8. System confirms to provider that the issue has been reported
- **Outcome**: File loading problem is surfaced to admins/ops via FR-034 while provider receives clear feedback

---

### Main Flow: View and Reply to Support Cases (Two-Way Communication)

**Actors**: Provider (any role), Admin, System, S-03 Notification Service
**Trigger**: Provider wants to check status of submitted support cases or reply to admin messages
**Outcome**: Provider views case details, reads admin responses, and sends reply message creating two-way conversation

**Steps**:

1. Provider navigates to Help Centre from main navigation
2. Provider clicks "My Support Cases" in category navigation
3. System displays Screen 5.7 with list of provider's submitted cases (both support requests and feedback)
4. System shows default filter: Open and In Progress cases from last 90 days, sorted by Last Updated descending
5. Provider sees unread message indicator (badge with count) on cases where admin has replied since last view
6. Provider clicks on case with unread messages (e.g., "Cannot access quote dashboard - CASE-2025-12345")
7. System opens case detail view (expandable panel or modal) with complete case information:
   - Case ID, Title, Status, Type, Priority, Feedback Resolution (if feedback)
   - Original Description (provider's initial submission)
   - Communication Thread (all messages from admin and provider in chronological order)
   - Case Timeline (all events in reverse chronological order)
8. System marks admin messages as read when provider opens case detail
9. Provider reads admin's latest reply in Communication Thread: "Hi [Provider Name], I've reviewed your issue. It appears to be related to browser cache. Please try clearing your browser cache and cookies, then log in again. Steps: [detailed instructions]. Let me know if this resolves the issue. Best regards, Support Team"
10. Provider scrolls through Communication Thread to see full conversation history
11. Provider decides to reply to admin with update
12. Provider types message in Reply Message Box: "Thank you! I cleared the cache as instructed, but I'm still seeing the same error. I've attached a screenshot of the error message I'm getting."
13. Provider clicks "Attach Files" button
14. System opens file picker
15. Provider selects screenshot file (PNG, 2MB)
16. System validates file (size, format) and displays file preview with remove option
17. Provider clicks "Send Reply" button
18. System validates message (not empty; case is Open, In Progress or Resolved; a reply to a Resolved case reopens it, REQ-032-109)
19. System sends message to FR-034 with:
    - Case ID
    - Sender: Provider (provider ID)
    - Message content
    - Attachment metadata
20. FR-034 receives message and:
    - Adds message to case Communication Thread
    - Logs "Message Received from Provider" event in case Timeline
    - Updates case Last Updated timestamp
    - Triggers support.case_user_reply notification event to S-03
21. S-03 sends email notification to assigned admin (or all support staff if unassigned): "Provider [Name] replied to case CASE-2025-12345"
22. System displays confirmation to provider: "Reply sent. The support team will respond soon."
23. System refreshes case detail view showing provider's reply in Communication Thread
24. Provider can continue monitoring case or close detail view
25. When admin replies again, provider receives email notification (support.case_admin_reply) with link to case
26. Provider returns to My Support Cases later to see admin's response

**Alternative Flows**:

**A1: Provider Requests to Reopen Closed Case**:

- **Trigger**: Provider's issue persists after case was marked as Resolved and Closed
- **Steps**:
  1. Provider opens closed case in My Support Cases view
  2. System displays case detail with status "Closed" and previous resolution summary
  3. Reply Message Box is disabled with message: "This case is closed. Click 'Request Reopen' if issue persists."
  4. Provider clicks "Request Reopen" button
  5. System opens reopen request modal with fields:
     - Reopening Reason (required textarea: "The issue is still occurring. After clearing cache, I still can't access the dashboard.")
     - Priority Update (dropdown: Keep Current / Low / Medium / High / Urgent)
  6. Provider fills reopening reason and selects "High" priority
  7. Provider clicks "Submit Reopen Request"
  8. System validates reason (min 20 chars) and sends it to FR-034 as a flagged reopen-request message in the case thread (reason and, optionally, the requested priority as text) (REQ-032-113)
  9. FR-034 notifies the admin through the user-reply notice (support.case_user_reply, REQ-034-178); the case stays Closed
  10. System displays confirmation: "Reopen request submitted. We'll review your case shortly." and Screen 5.8 shows "Request sent, awaiting admin" with the reply box still disabled (REQ-032-114)
  11. Admin reviews the flagged message
  12. If the admin accepts the request, the admin reopens the case in FR-034 (Reopen Case, status Open, REQ-034-145), which enables the reply box again (REQ-032-114)
  13. Provider receives the FR-034 notice and conversation continues
- **Alternative outcome**: If an admin answers but keeps the case Closed, the "Request sent, awaiting admin" banner clears and the Request Reopen button returns, so the provider may ask again (REQ-032-114)
- **Outcome**: Reopen request delivered to the admin; the case stays Closed until an admin reopens it

**A2: Provider Filters and Searches Cases**:

- **Trigger**: Provider wants to find specific past case or filter by status
- **Steps**:
  1. Provider opens My Support Cases screen
  2. Provider uses Filter Bar to select "Resolved" and "Closed" statuses
  3. Provider enters search term in Search Bar: "payment"
  4. System filters cases matching: Status = Resolved OR Closed, AND keyword "payment" in Case ID, Title, Description, or Messages
  5. System displays filtered results
  6. Provider clicks case to view details
- **Outcome**: Provider finds historical case for reference

**A3: Provider Receives Admin Reply Notification**:

- **Trigger**: Admin replies to provider's support case
- **Steps**:
  1. Admin sends reply to provider's case in FR-034 Screen 3
  2. FR-034 triggers support.case_admin_reply notification event to S-03
  3. S-03 sends email to provider: "Your support case CASE-2025-12345 has a new reply from our team"
  4. Email includes link to case: "View case in My Support Cases"
  5. Provider clicks link in email
  6. System opens provider platform and opens the case directly on Screen 5.8, whatever the filters of the case list (REQ-032-112)
  7. System shows the case with the new reply in the Communication Thread (REQ-032-112)
  8. Provider reads admin's response in Communication Thread
  9. Provider replies if needed
- **Outcome**: Provider notified of admin reply and can continue conversation seamlessly

---

### Main Flow: Request Account Closure

**Actors**: Provider (Owner only, REQ-032-141), Admin, System
**Trigger**: Provider Owner navigates to "Settings" → "Account Settings" → "Request account closure"
**Outcome**: Provider account-closure request submitted to admin; when the admin processes it, the provider is deactivated through FR-015 (Provider Management) Screen 4 (status "Deactivated", standard deactivation cascade). There is no separate "Deleted" status and no self-service deactivation.

**Steps**:

1. Provider navigates to Settings → Account Settings
2. Provider scrolls to bottom of page
3. Provider clicks "Request account closure" button (in red/warning color)
4. System displays account closure warning dialog:
   - "Closing your account permanently deactivates it. You will no longer be able to log in or receive inquiries."
   - "Deactivation cannot be reversed. To rejoin Hairline, our team must create a new account for you."
   - "When our team deactivates your account, all open inquiries, quotes, and active bookings are cancelled and the affected patients are notified. Payments already captured are reconciled by our finance team."
   - "Your quotes, bookings, and financial data will be archived per our data retention policy."
   - [Checkbox] "I understand that closing my account is permanent and my account data will be archived." (REQ-032-070)
   - Reason for closure: [textarea] (optional) (REQ-032-070)
5. Provider checks "I understand" checkbox
6. Provider enters reason for closure (optional): "Closing clinic permanently"
7. Provider clicks "Submit Closure Request"
8. System creates account closure request record with status "Pending Admin Review" (only one pending request per provider; no booking or payout check blocks submission; a Suspended Owner can still submit) (REQ-032-071, REQ-032-067)
   - If a request is already pending, System refuses the submission with "A closure request is already pending." and creates nothing (REQ-032-071)
9. System logs closure request in audit trail (user, timestamp, reason)
10. System notifies admins of the request (FR-020 `provider.closure_requested`, a mandatory notice; recipients and content are defined by the notification Rules REQ-020-016 and REQ-030-101), and FR-015 Screen 1 shows the provider with the Closure Requested marker and filter (REQ-032-072)
11. System displays confirmation to provider "Account closure request submitted. We aim to review and process your request within 5 business days. You will receive an email once your account is deactivated." (REQ-032-073)
12. Provider account keeps its current status until admin processes the request. If the admin schedules the deactivation for a future date, the request stays "Pending Admin Review" until the deactivation takes effect; if the scheduled deactivation is cancelled, the request stays "Pending Admin Review" and no rejection email is sent (REQ-032-074)
13. Admin reviews the closure request in FR-015 (A-02: Provider Management) and processes it per FR-015 Alternative Flow A7: deactivates the provider via FR-015 Screen 4 (immediate or scheduled), with a reason that references the request
14. System applies the FR-015 deactivation:
    - Provider account status changed to "Deactivated"
    - Provider login blocked with the Rule 6 deactivation message
    - Provider profile hidden from patients and new inquiries
    - All non-terminal inquiries, quotes, and bookings cancelled under the FR-015 Screen 4 cascade, with patient and admin-support notifications (FR-020); captured payments reconciled by FR-017
    - All provider data retained in archive (retention follows the system PRD, Platform-Wide Rules: One 10-year retention period)
    - Bank account details encrypted and archived
15. When the deactivation takes effect, the system sets the closure request status to "Approved", links it to the FR-015 deactivation status event, and sends the FR-015 deactivation email (`provider.deactivated`, FR-020). FR-015 locks "Notify Provider" on for closure deactivations, so this email is always sent, as step 11 promises (REQ-032-075)
16. If the admin rejects the request instead (e.g., the provider asks to withdraw it), the system sets the request status to "Rejected" with review notes, the provider account keeps its current status, and the provider receives the FR-020 `provider.closure_rejected` email with the review notes (mandatory). The provider may submit a new request later (REQ-032-076)

### Alternative Flows

**A13: Provider Cancels Closure Request Dialog**:

- **Trigger**: Provider changes mind before submitting closure request
- **Steps**:
  1. Provider clicks "Request account closure"
  2. System displays warning dialog
  3. Provider reads warning
  4. Provider clicks "Cancel" button
  5. System closes dialog without creating closure request (REQ-032-070)
- **Outcome**: No closure request created; provider account is unchanged

---

## Screen Specifications

### Screen 1: Profile Management

**Purpose**: Allow provider to update clinic profile information visible to patients during quote comparison. This screen is organized as 6 tabs within the Provider Profile page (Settings & Support > Provider profile).

**Tab Structure**:

#### Tab 1: Basic Information

**Purpose**: Display and edit core clinic profile information including profile picture, name, rating, and contact details.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing | Graph field |
|------------|------|----------|-------------|------------------|----------------|---|
| Profile Picture | image upload | No | Clinic branding image displayed in patient app | Max 5MB, JPEG/PNG only, min 200x200px, recommended 500x500px | **Inline Edit**: Click image area to open upload dialog with file picker; shows preview before save; crop/resize tool available; save/cancel buttons appear during edit | ENT-provider-profile.logo_url |
| Cover Image | image upload | No | Large banner image for clinic profile | Max 10MB, JPEG/PNG only, recommended 1920x300px (REQ-032-034) | **Inline Edit**: Click image area to open upload dialog with file picker; shows preview before save; crop/resize tool available; save/cancel buttons appear during edit | ENT-provider-profile.cover_image_url |
| Clinic Name | text | Yes | Official clinic name | Max 200 chars, min 3 chars (REQ-032-033) | **Inline Edit**: Click text to activate edit mode; field becomes editable input; save (✓) and cancel (✗) buttons appear; validation on blur; saves immediately on save button click | ENT-provider-profile.clinic_name |
| Review Rating | display | No | Average rating from patient reviews (read-only) | Display format: X.X/5.0 stars with total review count (e.g., "4.8/5.0 - Based on 127 reviews") | **Read-only**: Displays current average rating; clicking rating or "View all reviews" text navigates to Reviews tab (Tab 5) | ENT-provider-review-summary.average_rating, ENT-provider-review-summary.review_count |
| Edit Profile Button | button | N/A | Quick access to edit mode for all fields in tab | N/A | **Toggle Action**: Clicking button toggles all editable fields in tab into edit mode simultaneously; button text changes to "Cancel Edit" when active; allows bulk editing of multiple fields (REQ-032-119) | no graph field (control) |
| About/Description | textarea | Yes | Brief clinic description for patients | Max 500 chars, min 50 chars (REQ-032-033) | **Inline Edit**: Click textarea to activate edit mode; expands to show full textarea with character counter (e.g., "245/500 characters"); save/cancel buttons appear; real-time validation; saves on save button click | ENT-provider-profile.clinic_description |
| Contact Phone (Public) | object | No | Public-facing clinic phone number shown in profile "About" section | Contains `Country Code` (dropdown, FR-026) and `Number` (text, numeric only, length validated per country code) (REQ-032-037) | **Inline Edit**: Click to activate edit mode; field becomes object with dropdown for country code and input for number; auto-formats on blur (e.g., "+90 555 123 4567"); save/cancel buttons appear; saves on save button click | ENT-provider-profile.public_phone |
| Contact Email | email | Yes | Clinic contact email shown on provider public profile and used for communications | Valid email format; must be unique among Active and Suspended providers if changed (Deactivated records ignored, per FR-015 Rule 4) (REQ-032-036) | **Inline Edit**: Click email to activate edit mode; field becomes editable input with email validation; shows validation error if invalid format; save/cancel buttons appear; saves on save button click | ENT-provider-profile.contact_email |
| Location - City | text | No | City where clinic is located | Max 100 chars (REQ-032-033) | **Inline Edit**: Click city name to activate edit mode; field becomes editable input; save/cancel buttons appear; saves on save button click | ENT-provider-profile.city |
| Location - Country | dropdown | No | Country where clinic is located | Values from centrally managed country list (FR-026); optional but recommended (REQ-032-038) | **Inline Edit**: Click country name to activate edit mode; field becomes dropdown selector with search; shows country list from FR-026; save/cancel buttons appear; saves on save button click | ENT-provider-profile.country |
| Website URL | url | No | Public-facing clinic website shown in profile "About" section | Valid URL format (http/https); auto-prepends https:// if protocol missing (REQ-032-039) | **Inline Edit**: Click URL to activate edit mode; field becomes editable input with URL validation; auto-formats on blur (adds https:// if missing); shows validation error if invalid; save/cancel buttons appear; saves on save button click | ENT-provider-profile.website_url |

**Business Rules**:

- Profile picture displayed in profile section; clicking opens upload dialog
- Cover image displayed as a banner on the top of the provider profile in patient app; (REQ-032-034)
- If no logo uploaded, system displays clinic name initials as fallback (REQ-032-035)
- Review rating displays average rating (e.g., "4.8/5.0") with total review count (e.g., "Based on 127 reviews"); clicking navigates to Reviews tab (REQ-032-116)
- All fields support inline editing: clicking a field activates edit mode with save/cancel buttons
- Unsaved changes indicator (dot/asterisk) appears on tab label when edits are made (REQ-032-040)
- Each field can be edited independently; changes saved per field or via "Save All" button
- Profile changes logged in audit trail with timestamp and user (REQ-032-020)
- Profile updates propagate to patient app within 1 minute (REQ-032-014)

**Notes**:

- **Profile Picture**: Image upload via file picker; shows preview after upload before saving; crop/resize functionality available to ensure proper aspect ratio; if no image uploaded, displays clinic name initials as fallback
- **Cover Image**: Image upload via file picker; shows preview after upload before saving; crop/resize functionality available to ensure proper aspect ratio;
- **Inline Editing Behavior**: Clicking any editable field highlights it with border/background change and shows save (✓) and cancel (✗) buttons; field becomes editable input/textarea/dropdown; validation occurs on blur or save; changes persist immediately on save button click; cancel button discards changes and reverts to original value
- **Character Counter**: About/Description field shows real-time character counter (e.g., "245/500 characters") with color change when approaching limit (yellow at 80%, red at 95%)
- **Bulk Edit Mode**: "Edit Profile" button toggles all editable fields in tab into edit mode simultaneously; button text changes to "Cancel Edit" when active; allows editing multiple fields before saving all at once via "Save All" button (REQ-032-119)
- **Unsaved Changes**: Unsaved changes indicator (dot or asterisk) appears on tab label when any field has unsaved edits; indicator disappears when all changes saved
- **Field Validation**: Real-time validation feedback shown inline (e.g., red border for invalid email, green checkmark for valid); error messages appear below field when invalid

---

#### Tab 2: Languages

**Purpose**: Manage languages spoken at the clinic.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing | Graph field |
|------------|------|----------|-------------|------------------|----------------|---|
| Supported Languages | chip/pill list | Yes | Languages spoken at clinic | At least 1 language required; consumes the FR-021 language/locale catalog surfaced through settings | **Inline Edit**: Add language: click "+ Add Language" button to open dropdown with the offered languages from FR-021 (Active and Preparation locales, REQ-032-147); select language to add chip immediately; Remove language: click X icon on chip to remove (confirmation required if last language); Reorder: drag-and-drop chips to prioritize; changes save automatically or via "Save" button; unsaved changes indicator appears on tab label | ENT-provider-profile.supported_languages |

**Business Rules**:

- Languages displayed as removable chips/pills with X button on each chip
- Clicking "+ Add Language" opens dropdown with the offered languages from FR-021: the Active and Preparation locales. Every catalog locale already saved is displayed, and a saved language stays when its locale becomes Inactive (REQ-032-147)
- Selected languages immediately appear as chips; removing a chip removes it from selection
- At least 1 language must be selected (validation prevents removing last language) (REQ-032-043)
- Changes saved automatically when language added/removed, or via "Save" button
- Unsaved changes indicator appears on tab label when edits are made (REQ-032-040)
- Language changes logged in audit trail (REQ-032-020)

**Notes**:

- Each language chip displays language name (e.g., "English", "Turkish", "Spanish")
- Chips support drag-and-drop reordering to prioritize languages (most important first) (REQ-032-044)
- Visual feedback: chip highlights on hover; removal requires confirmation if it's the last language
- Language list consumed from FR-021; FR-026 may surface the list through the broader settings shell but does not own provider language-capacity semantics.

---

#### Tab 3: Staff List

**Purpose**: Manage clinic staff members and team roles.

**Implementation**: This tab displays **FR-009: Provider Team & Roles Management > Screen 1**.

See FR-009 Screen 1 for complete field specifications, business rules, and staff management functionality.

---

#### Tab 4: Awards

**Purpose**: Manage clinic awards, certifications, and recognitions.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing | Graph field |
|------------|------|----------|-------------|------------------|----------------|---|
| Awards List | card/list | No | Clinic awards, certifications, recognitions | Each award: name (max 100 chars), issuer/organization (max 150 chars, optional), description (max 300 chars), year (1900-current year), award image (max 2MB, JPEG/PNG) (REQ-032-045) | **Inline Edit**: Add award: click "+ Add Award" button to open award form (modal or inline expansion) with fields: name (text), issuer/organization (text, optional), description (textarea, max 300 chars), year (number dropdown 1900-current), image upload (drag-and-drop or file picker, max 2MB); Edit award: click "Edit" icon/button on award card to expand inline editor with all fields editable; Delete award: click "Delete" icon/button on award card, confirmation dialog appears; Reorder: drag-and-drop award cards to prioritize; each award saves independently or via "Save All" button; unsaved changes indicator appears on tab label | ENT-provider-award.name, ENT-provider-award.issuer, ENT-provider-award.description, ENT-provider-award.year, ENT-provider-award.image_url |

**Business Rules**:

- Awards displayed as cards/rows with: award image thumbnail, name, issuer/organization, year, description snippet
- Clicking "Edit" on an award card opens inline editor (or modal) with all award fields editable
- Clicking "+ Add Award" opens award form (name, issuer/organization, description, year, image upload)
- Awards support drag-and-drop reordering to prioritize most important awards (REQ-032-047)
- Award image upload supports drag-and-drop; max 2MB, JPEG/PNG only
- Changes saved per award (inline save) or via "Save All" button
- Unsaved changes indicator appears on tab label when edits are made (REQ-032-040)
- Award changes logged in audit trail (REQ-032-020)

**Notes**:

- Each award card displays: image thumbnail (or placeholder), award name (bold), issuer/organization, year, description (truncated with "Read more" if long)
- Inline editing: clicking "Edit" expands award card to show editable fields with save/cancel buttons
- Award image upload: click image area to upload/replace; supports drag-and-drop
- Awards list supports reordering via drag-and-drop handles
- Empty state: "No awards added yet. Click '+ Add Award' to showcase your achievements." (REQ-032-120)

---

#### Tab 5: Reviews

**Purpose**: Browse all patient reviews with filtering and sorting capabilities, and post public responses to individual reviews via the FR-013 response composer.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing | Graph field |
|------------|------|----------|-------------|------------------|----------------|---|
| Overall Rating Summary | display | No | Average rating and total review count (e.g., "4.8/5.0 - Based on 127 reviews") | Read-only; calculated from Reviews service | **Read-only**: Displays current average rating with star display and total review count; updates automatically when new reviews added | ENT-provider-review-summary.average_rating, ENT-provider-review-summary.review_count |
| Rating Distribution | bar chart | No | Percentage/count visualization for 5★ through 1★ reviews | Read-only; calculated from Reviews service | **Read-only**: Bar chart showing distribution of ratings (e.g., 60% 5-star, 25% 4-star, etc.) with counts; updates automatically | ENT-provider-review-summary.rating_distribution |
| Rating Filters | checkbox/pill group | No | Filter reviews by rating (5★, 4★, 3★, 2★, 1★); multiple selections allowed | Filtering runs on the server over the whole review list (REQ-032-148); selections persist per session | **Interactive**: Click rating pill/checkbox to toggle filter; multiple ratings can be selected; filtered results update immediately; filter state persists during session | no graph field (control) |
| Sort Dropdown | dropdown | No | Sort order options: "Most recent" (default), "Highest rated", "Lowest rated", "Oldest first" | Sorting runs on the server over the whole review list (REQ-032-148); selection persists per session | **Interactive**: Select from dropdown to change sort order; results update immediately; sort preference persists during session | no graph field (control) |
| Review Cards | list | No | List of review cards displaying: reviewer avatar/name, treatment type, rating stars, review date, review text (truncated), optional "Read more" link | Read-only content from Reviews service; pagination supported; a review edited by the patient after publishing carries the "Edited" marker (FR-013 REQ-013-032, REQ-032-148) | **Read-only**: Review cards display review information; click "Read more" to expand full review text; click reviewer name/avatar (if implemented) may show reviewer profile; cards update automatically when new reviews added | ENT-review.reviewer_avatar_url, ENT-review.reviewer_name, ENT-review.treatment_name, ENT-review.overall_rating, ENT-review.created_at, ENT-review.feedback_text |
| Pagination Controls | control group | No | Page navigation: page numbers, next/previous buttons, page-size selector (10/20/50 per page) | Paging runs on the server over the whole review list (REQ-032-148) | **Interactive**: Click page numbers or next/previous to navigate; select page size from dropdown; pagination state persists during session (REQ-032-122) | no graph field (control) |

**Business Rules**:

- Review content (ratings, feedback, photos) is read-only — providers cannot edit or delete patient-submitted reviews (REQ-032-050)
- Providers may post a public response to any published review via the inline response composer defined in FR-013 Screen 6; see FR-013 for response rules and immutability (REQ-032-050)
- Overall rating displays average (e.g., "4.8/5.0") with total count (e.g., "Based on 127 reviews") (REQ-032-116)
- Rating distribution shows bar chart with counts/percentages for each star rating
- Rating filter and sort options, defaults and per-session persistence are defined by FR-022 (REQ-022-084); filter, sort and paging run on the server over the whole list, and the tab links to the FR-013 provider review list and review detail screens (REQ-032-148)
- Clicking a review notification (from notifications) opens this tab with relevant review auto-highlighted (REQ-032-052)
- Data sourced from Reviews service; loading/empty/error states handled
- Reviews update automatically when new reviews are posted

**Notes**:

- Review cards display: reviewer avatar/name, treatment type, rating stars, review date, review text (truncated with "Read more")
- Filters and sort controls at top of reviews list
- Pagination controls: page numbers, next/previous, page-size selector (10/20/50 per page) (REQ-032-122)
- Empty state: "No reviews yet. Reviews will appear here once patients leave feedback." (REQ-032-121)
- Timestamp of last sync with Reviews service displayed at bottom

---

#### Tab 6: Documents

**Purpose**: Manage clinic documents including medical licenses, certifications, insurance, and other compliance documents. Providers can upload, replace, delete, and view their documents. Admins can also upload additional documents via FR-015 for oversight purposes.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing | Graph field |
|------------|------|----------|-------------|------------------|----------------|---|
| Upload Document Button | button | No | Primary action to upload new document | Opens upload modal | **Interactive**: Click to open "Upload Document" modal with fields: Document Type (dropdown), Document File (file picker), optional notes | no graph field (control) |
| Document List | list/cards | No | List of uploaded documents with metadata | Displays all provider and admin-uploaded documents | **Interactive**: Document cards in list/grid format; each card shows document name, type badge, upload date, file size, uploaded by (Provider/Admin), and action buttons (View, Replace, Delete) | ENT-provider-document.document_name, ENT-provider-document.document_type, ENT-provider-document.uploaded_at, ENT-provider-document.file_size, ENT-provider-document.uploaded_by |
| Document Name | text (display/edit) | Yes | Filename of document | Auto-generated from uploaded file; max 200 chars; editable via "Rename" action | **Editable**: Click "Rename" icon/button on document card to edit filename; save on blur or Enter key | ENT-provider-document.document_name |
| Document Type | dropdown | Yes | Document type selection | Options: "Medical License", "Board Certification", "Insurance", "Malpractice Insurance", "Business License", "Other" | **Editable**: Select from dropdown when uploading; can be changed via "Edit" action on document card | ENT-provider-document.document_type |
| Document File | file upload | Yes | Upload document file | Accepted formats: PDF, JPG, PNG, DOCX, XLSX; Max 10MB per file (REQ-032-060) | **Interactive**: Drag-and-drop or click to browse; file picker validates format/size before upload | ENT-provider-document.file_url |
| Upload Date | date (display) | N/A | Date when document was uploaded | Timestamp format: "MMM DD, YYYY" (e.g., "Jan 15, 2025"); auto-generated | **Read-only**: Displays upload date with relative time on hover (e.g., "Uploaded 3 months ago") | ENT-provider-document.uploaded_at |
| Uploaded By | badge (display) | N/A | Who uploaded the document: "Provider" or "Admin" | Badge displays "You" for provider uploads, "Admin" for admin uploads | **Read-only**: Badge color: green for "You", blue for "Admin" | ENT-provider-document.uploaded_by |
| File Size | text (display) | N/A | Document file size | Format: "X.X MB" or "X KB"; auto-calculated | **Read-only**: Displays file size | ENT-provider-document.file_size |
| Notes | text (optional) | No | Optional notes about document | Max 500 chars; editable | **Editable**: Click "Edit Notes" on document card to add/edit notes; save on blur or via Save button | ENT-provider-document.notes |
| View/Download Button | button | No | Action button to view or download document | Opens document in new browser tab or downloads file depending on file type | **Interactive**: Click to view PDF in browser or download file; button label: "View" for PDFs, "Download" for other file types | no graph field (control) |
| Replace Button | button | No | Action button to replace existing document with new version | Opens file picker to upload replacement | **Interactive**: Click "Replace" button on document card; file picker opens; validates format/size; on upload, old version archived (soft delete) and new version becomes active; confirmation toast: "Document replaced successfully" | no graph field (control) |
| Delete Button | button | No | Action button to delete document | Opens confirmation dialog; performs soft delete | **Interactive**: Click "Delete" button on document card; confirmation dialog: "Are you sure you want to delete [document name]? This action cannot be undone." On confirm, document soft-deleted; confirmation toast: "Document deleted successfully" | no graph field (control) |

**Business Rules**:

- **Provider Document Management**: Providers can upload, replace, delete, and view their own documents (REQ-032-053)
- **Admin Oversight**: Admins can upload additional documents via FR-015 Tab 6 (e.g., documents received via email, external verifications). Admin-uploaded documents display "Admin" badge (REQ-032-054)
- **Document Sync**: Documents uploaded by provider in FR-032 sync to FR-015 within 1 minute for admin visibility (REQ-032-055)
- **Empty State**: If no documents uploaded yet, display message: "No documents on file. Upload your clinic documents (medical license, certifications, insurance) to get started." with prominent "Upload Document" button (REQ-032-135)
- **Upload Modal Fields**:
  - Document Type: Dropdown (required) - "Medical License", "Board Certification", "Insurance", "Malpractice Insurance", "Business License", "Other"
  - Document File: File picker (required) - Accepted formats: PDF, JPG, PNG, DOCX, XLSX; Max 10MB
  - Notes: Text area (optional) - Max 500 chars; helpful for adding context (e.g., "License expires Dec 2026")
  - On submit: Document uploaded, confirmation toast: "Document uploaded successfully"
- **Replace Document**: Clicking "Replace" on a document card opens file picker; uploading new file replaces current version; old version archived (soft delete) with timestamp (REQ-032-056)
- **Delete Document**: Clicking "Delete" opens confirmation dialog; on confirm, document soft-deleted (not permanently removed); admin can view deleted documents in FR-015 for audit purposes (REQ-032-057)
- **Document Permissions**: Providers can only delete/replace documents they uploaded; Admin-uploaded documents display "View Only" (providers cannot delete/replace, but can download) (REQ-032-053)
- **Audit Logging**: All document actions (upload/replace/delete/view/download) logged with timestamp, user, action type, and IP address (visible in FR-015 Tab 8: Activity Log) (REQ-032-058)
- **Security**: Document URLs are secure, time-limited signed URLs; direct file access not allowed (REQ-032-059)
- **File Validation**: (REQ-032-060)
  - Accepted formats: PDF, JPG, PNG, DOCX, XLSX
  - Max file size: 10MB per document
  - File name sanitization: Remove special characters, limit to 200 chars
  - Virus scanning: All uploaded files scanned before storage
- **Sort/Filter Options**:
  - Sort by: Upload Date (newest first - default), Document Type, File Name
  - Filter by: Document Type, Uploaded By (Provider/Admin)

**Notes**:

- Providers have full control over documents they upload; admin-uploaded documents are view-only for providers
- Admin can view all provider-uploaded documents in FR-015 Tab 6 for oversight and compliance verification
- Document versioning: When replaced, old versions archived with timestamp (not shown to provider, but admin can view in FR-015)
- Document list sorted by upload date (most recent first) by default
- Loading state: Display skeleton loaders while fetching documents
- Error state: If document fetch fails, display "Unable to load documents. Please refresh or contact support." (REQ-032-123)
- Document cards display icon based on file type (PDF icon for PDFs, image icon for JPG/PNG, generic doc icon for DOCX/XLSX)
- Drag-and-drop upload: Providers can drag files directly onto the Documents tab to upload (opens upload modal with file pre-selected) (REQ-032-124)

---

**General Business Rules (All Tabs)**:

- Each tab can be saved independently; system displays unsaved changes indicator (dot/asterisk) on tab label when edits are made (REQ-032-040)
- See REQ-032-040.
- All profile changes logged in audit trail with timestamp and user (REQ-032-020)
- Profile updates propagate to patient app within 1 minute (REQ-032-014)
- All profile fields are provider-editable from the provider dashboard (subject to role/permissions defined in FR-009 where applicable) (REQ-032-041)
- **Who edits what** (REQ-032-141; the per-feature permission matrix is configured in FR-031):

| Area | Who can edit | Gated by (FR-031 permission) |
|------|--------------|------------------------------|
| Clinic profile, languages, awards, documents | Owner and Manager by default | Edit Profile |
| Notification preferences (REQ-032-142) | Owner and Manager by default; other roles see them read-only | Edit Notification Settings |
| Account closure request | Owner only | Owner only (no permission) |
| Personal account settings (Screen 2) | Every role, for their own account only | None (own account) |
| Billing settings | Owner only by default (FR-031, REQ-031-005) | View and Edit Billing Settings |

- Inline editing: clicking editable fields activates edit mode with save/cancel buttons; changes persist immediately on save
- **Tab Editability**:
  - **Fully Editable**: Tab 1 (Basic Information), Tab 2 (Languages), Tab 4 (Awards), Tab 6 (Documents) - providers can add, edit, delete content inline
  - **External Module**: Tab 3 (Staff List) - displays FR-009 Screen 1; see FR-009 for functionality
  - **Read/Respond**: Tab 5 (Reviews) - review content is read-only; providers can post public responses via FR-013 response composer; managed by Reviews service, providers cannot edit/delete reviews

---

### Screen 2: Account Settings

**Purpose**: Allow each team member (any role) to manage their own account details: display name, phone number, timezone, and password, for account security and localization. Account Email is shown read-only (REQ-032-144). These values belong to the person, not the clinic (REQ-032-141). This screen is organized as a tab within the Settings page (Settings & Support > Settings > Account Information tab).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Role-Based Behavior | Graph field |
|------------|------|----------|-------------|------------------|-------------------|---|
| Account Name | text/display | Yes | Display name for the account | Max 200 chars (REQ-032-063) | **Owner**: Unified with clinic name (read-only, synced from Tab 1: Basic Information); **Staff**: Editable display name (defaults to First Name + Last Name, can be customized) | ENT-team-member.account_name |
| First Name | text | Yes | User's first name | 2-50 characters, letters, spaces, hyphens (same as FR-009) (REQ-032-063) | Editable by all roles (Owner and Staff) | ENT-team-member.first_name |
| Last Name | text | Yes | User's last name | 2-50 characters, letters, spaces, hyphens (same as FR-009) (REQ-032-063) | Editable by all roles (Owner and Staff) | ENT-team-member.last_name |
| Account Email | email | Yes | Email address for login and communications | Valid email format, unique per FR-009 Rule 3 (an email belongs to at most one provider organization at a time) (REQ-032-063) | **Read-only for every role.** The Owner's login email is changed only by a Hairline admin (FR-015, REQ-015-114); a team member's email is changed by contacting support (REQ-032-144) | ENT-team-member.email |
| Phone Number - Country Code | dropdown | Yes (REQ-032-125) | Worldwide country calling code | Consumes FR-026 country calling codes list (e.g., +1, +44, +90, +234) | Editable by all roles, for their own account | ENT-team-member.phone_number (country code and number saved together in international format) |
| Phone Number - Number | text | Yes (REQ-032-125) | Provider phone number; it can be replaced but not removed | Numeric only, length validated per country code format; unique per user within the provider (REQ-032-125) | Editable by all roles, for their own account | ENT-team-member.phone_number |
| Timezone | dropdown | Yes (empty only before the person's first login) | This person's local timezone for date/time display; set at first login to the listed whole-hour offset nearest to the browser time zone, or UTC when the browser zone cannot be read, and changeable at any time (REQ-032-145) | Fixed-offset options from the FR-026 timezone list (GMT-12 to GMT+14, REQ-026-121) | Editable by all roles, for their own account | ENT-team-member.timezone |
| Current Password | password | Yes (for password change) | Current password for verification | Must match existing password hash | Editable by all roles | no graph field (input checked against the stored hash) |
| New Password | password | Yes (for password change) | New password | See system PRD, Platform-Wide Rules: Password and one-time-code policy | Editable by all roles, for their own account | ENT-team-member.password |
| Confirm New Password | password | Yes (for password change) | Confirm new password | Must match New Password field (REQ-032-065) | Editable by all roles | no graph field (input that must match New Password) |

**Business Rules**:

- **Account Name Unification (Owner Role)**:
  - For Owner accounts (main account holder/provider admin): Account Name is unified with the clinic name from Tab 1: Basic Information (clinic name field)
  - Account Name field is read-only for Owner role; it automatically syncs when clinic name is updated in Tab 1 (REQ-032-061)
  - If Owner updates clinic name in Tab 1, Account Name in Tab 2 updates automatically (within 1 minute) (REQ-032-061)
  - When the Owner role is handed over (REQ-009-174), the new Owner's Account Name is set to the clinic name and the previous Owner's is reset to First Name + Last Name (REQ-032-061)
  - Account Name displays clinic name with read-only indicator (e.g., "Istanbul Hair Clinic" with lock icon or "Synced with clinic name" helper text)
  - Rationale: Owner account represents the clinic organization, so account name should match clinic name for consistency across the platform
  
- **Account Name (Staff Roles)**:
  - For Staff roles (Manager, Clinical Staff, Billing Staff): Account Name is editable and independent from clinic name (REQ-032-062)
  - Default Account Name for staff is "First Name + Last Name" (e.g., "John Smith"), set when the account is created (FR-009 account setup) (REQ-032-062)
  - Staff can customize Account Name to any display name (e.g., "Dr. John Smith", "John S.", "J. Smith")
  - Account Name for staff is used for display purposes in dashboard, notifications, activity logs, and team member listings
  - Staff Account Name changes do not affect clinic name or other staff members' account names (REQ-032-062)
  - Rationale: Staff are individual team members, not the clinic itself, so they should have personalized display names
  
- Phone number country code and number stored together in international format (e.g., +44 7700 900123) (REQ-032-015)
- The phone number stays required: it can be replaced but not removed; it is unique per user within the provider, and a changed number is verified as in FR-009 (REQ-009-113) (REQ-032-125)
- Timezone is saved per person and applies to all date/time displays in that person's provider dashboard session; at first login it is set without a prompt to the listed whole-hour offset nearest to the browser time zone (UTC when the browser zone cannot be read) and the person can change it at any time (REQ-032-064, REQ-032-145)
- Phone and timezone changes are logged in the audit trail, with phone values masked (REQ-032-020)
- Existing timestamps in database remain in UTC, converted for display with the fixed offsets of the FR-026 timezone list (REQ-032-064, REQ-026-121)
- Password change requires correct current password (security measure) (REQ-032-007)
- New password must meet the password policy. See system PRD, Platform-Wide Rules: Password and one-time-code policy
- Password change event logged in audit trail (timestamp, user ID, IP address) (REQ-032-020)
- Email notification sent to provider email address after successful password change (security alert) (REQ-032-021)
- All account-level fields (account name, first name, last name, phone number, timezone, password) are editable by the logged-in user for their own account only; Account Email is read-only for every role (REQ-032-144). Editing is subject to role-based restrictions (Account Name read-only for Owner) and FR-026 security rules and FR-009 role permissions (REQ-032-041)

**Notes**:

- **Account Name Field**:
  - For Owner: Display Account Name with read-only indicator (lock icon or "Synced with clinic name" helper text); clicking may show tooltip "Account name is unified with clinic name. Update clinic name in Profile tab to change this."
  - For Staff: Display Account Name as editable text field with placeholder "e.g., Dr. John Smith" and helper text "This is how your name appears in the dashboard and notifications"
  - Account Name field appears at the top of the Account Information tab for clarity
  
- Phone number field should auto-format based on selected country code (e.g., (555) 123-4567 for USA)
- Provide real-time password strength indicator for new password field
- Show password requirements checklist with visual checkmarks as user types
- Timezone dropdown should include offset and city examples (e.g., "(GMT+3) Istanbul")
- Provide "Show/Hide Password" toggle icon for password fields
- Display last password change date below password section
- Include a dedicated **Account Closure** warning card (shown to the Owner only, REQ-032-141) at the bottom of the Account Information tab with explanatory copy and a red `Request account closure` button; clicking the button opens the Account Closure dialog described in the "Request Account Closure" flow, where the reason textarea remains provider-editable while approval status stays admin-controlled. While a request is Pending Admin Review the card shows "Closure requested on DD-MM-YYYY, awaiting admin review" (plus "Deactivation scheduled for DD-MM-YYYY" when the admin scheduled a date) and the button is disabled; the card returns to normal when the request is Rejected (REQ-032-071)
- Account Settings shares the Settings page with Notification Preferences as a two-tab interface; the `Account Information` tab (this screen) is the default tab when landing on Settings
- Each tab can be saved independently; system displays unsaved changes indicator on tabs with edits (REQ-032-040)
- When provider attempts to navigate away or quit, system displays reminder dialog for unsaved changes (REQ-032-040)

---

### Screen 3: Notification Preferences

**Purpose**: Allow provider to configure unified notification preferences (individual notification types + global channel preferences). This screen is organized as a tab within the Settings page (Settings & Support > Settings > Notification Preferences tab).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Quote Notifications | toggle/checkbox | No (default enabled) | New inquiry received, quote expiring soon. Does not cover mandatory quote notices (the inquiry-cancelled quote notice and the quote-accepted outcomes), which are always sent | Toggle on/off | ENT-provider-notification-preferences.quote_notifications |
| Schedule Notifications | toggle/checkbox | No (default enabled) | Appointment confirmed, appointment reminder. Does not cover mandatory booking notices (payment window expired, booking revived, booking rescheduled), which are always sent | Toggle on/off | ENT-provider-notification-preferences.schedule_notifications |
| Treatment Start Notifications | toggle/checkbox | No (default enabled) | Patient checked in, procedure started | Toggle on/off | ENT-provider-notification-preferences.treatment_start_notifications |
| Aftercare Notifications | toggle/checkbox | No (default enabled) | Patient milestone completed, urgent aftercare alert | Toggle on/off | ENT-provider-notification-preferences.aftercare_notifications |
| Review Notifications | toggle/checkbox | No (default enabled) | New review posted, review requires response | Toggle on/off | ENT-provider-notification-preferences.review_notifications |
| Promotion/Discount Notifications | toggle/checkbox | No (default enabled) | New platform discounts created by admin that require provider acceptance/opt-in | Toggle on/off | ENT-provider-notification-preferences.promotion_notifications |
| Email Notifications | toggle/checkbox | No (default enabled) | Send notifications via email | Toggle on/off, email address from profile | ENT-provider-notification-preferences.email_enabled |
| Push/In-App Notifications | toggle/checkbox | No (default enabled) | Show notifications in web portal | Toggle on/off | ENT-provider-notification-preferences.push_enabled |

**Business Rules**:

- Notification preferences are profile-specific (apply to entire provider organization, not individual team members) (REQ-032-078); only holders of the FR-031 permission "Edit Notification Settings" (by default the Owner and a Manager) can change them, other roles see them read-only (REQ-032-142)
- If all notification types disabled, show confirmation dialog warning provider may miss important updates (REQ-032-079); Email and Push may both be off for a type, and mandatory notices ignore the setting (REQ-032-143)
- Notification preferences saved and enforced by S-03 Notification Service (FR-020) (REQ-032-009)
- Global channel preferences override individual notification types (e.g., if Email disabled, no notifications sent via email regardless of individual toggles) (REQ-032-080)
- Each tab (Profile, Account Information, Notification Preferences, Billing) can be saved independently; system displays unsaved changes indicator (e.g., dot or asterisk) on tabs with unsaved edits (REQ-032-040)
- See REQ-032-040.
- Critical system alerts (e.g., payment failure, security breach) bypass preferences and always sent via all available channels (REQ-032-081)
- Mandatory provider notices (defined in FR-030 Non-Disableable by Default; for the inquiry-cancelled quote notice, FR-020 REQ-020-020) are exempt from these preferences. This screen offers no toggle for them, and neither the Quote or Schedule Notifications toggles, "Disable All" nor the channel preferences can suppress them (REQ-032-031)
- Every preference change is logged in audit trail with the user who made it (REQ-032-082, REQ-032-142)
- Support case notices (admin reply, status change, resolved) have no toggle on this screen and are always sent (REQ-032-143)
- Preference updates propagate to S-03 within 1 minute (REQ-032-016)
- All notification type and channel toggles are editable by the holders of "Edit Notification Settings" (by default the Owner and a Manager) from the `Settings → Notification Preferences` tab in the provider dashboard (REQ-032-041, REQ-032-142)

**Notes**:

- Display notification types in collapsible sections with examples (expand to show what notifications are included)
- Provide "Enable All" / "Disable All" quick action buttons (REQ-032-126)
- Show real-time preview of notification channels (e.g., "You will receive Quote Notifications via Email and Push")
- Display last preference update timestamp
- Provide "Test Notification" button to send sample notification and verify settings work (REQ-032-127)
- Notification Preferences appears as the second tab on the Settings page beside Account Information; toggling between tabs should maintain unsaved changes warning if applicable
- Each tab has its own "Save" button; unsaved changes indicator appears on tab label when edits are made

---

### Screen 4: Billing Settings (Owner Role Only)

**Purpose**: Allow provider Owner to manage bank account details for receiving payouts from Hairline platform. This screen is organized as a tab within the Settings page (Settings & Support > Settings > Billing tab). Non-owner roles cannot see or access this tab. The bank form below is shown and required only when the Payout Method is Manual bank transfer; for Stripe Connect the tab shows a status panel and a "Complete Stripe sign-up" link instead (REQ-032-146).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Account Holder Name | text | Yes (Manual bank transfer only) | Full name or business name on bank account | Max 200 chars, alphabetic and spaces only (REQ-032-085) | ENT-provider-billing-settings.account_holder_name |
| Bank Name | text | Yes (Manual bank transfer only) | Official name of bank | Max 200 chars | ENT-provider-billing-settings.bank_name |
| Account Number | text | Yes (Manual bank transfer only) | Bank account number | Format varies by country, validated by S-02 Payment Service | ENT-provider-billing-settings.account_number |
| Routing/SWIFT Code | text | Yes (Manual bank transfer only) | Bank routing code (USA) or SWIFT code (international) | 8-11 chars for SWIFT, 9 digits for USA routing (REQ-032-085) | ENT-provider-billing-settings.routing_swift_code |
| IBAN | text | Conditional (if applicable) | International Bank Account Number | Format validated per country (e.g., Turkey = 26 chars) (REQ-032-085) | ENT-provider-billing-settings.iban |

**Commission & Payout (Read-Only Panel)**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Commission Model | display | N/A | "Percentage" or "Flat Rate" | Retrieved from FR-015 Tab 7 (FR-029 provider-specific commission configuration); read-only | ENT-commission-rate-config.commission_model |
| Commission Value | display | N/A | e.g., "15%" or "£200 per completed procedure" | Retrieved from FR-015 Tab 7; Flat Rate shown with its Flat Rate Currency; read-only | ENT-commission-rate-config.commission_percentage, ENT-commission-rate-config.flat_rate_amount, ENT-commission-rate-config.flat_rate_currency |
| Effective Date | display | N/A | Date from which the current configuration applies to newly confirmed bookings | Retrieved from FR-015 Tab 7 (FR-029 `effective_date`); format DD-MM-YYYY; read-only | ENT-commission-rate-config.effective_date |
| Scheduled Configuration | display | N/A | Next configuration and its Effective Date, if an admin has set a future-dated change. At most one pending configuration exists per provider; a newer future-dated edit by an admin replaces it (FR-015 Tab 7, FR-029) | Retrieved from FR-015 Tab 7; hidden when none is pending; read-only | ENT-commission-rate-config.status, ENT-commission-rate-config.effective_date |
| Payout Method | display | N/A | "Stripe Connect" or "Manual bank transfer"; chosen by the admin when the clinic is created in FR-015 | Read-only; the provider cannot change it | ENT-provider.payout_method |
| Payout Readiness | display | N/A | Whether the clinic's payout set-up is ready; for Stripe Connect the clinic completes Stripe's own sign-up itself through the "Complete Stripe sign-up" link in the status panel | Read-only, display only; readiness is owned by FR-017 (REQ-017-064) (REQ-032-146) | no graph field (display) |
| Payout Timing | display | N/A | Stripe Connect: "Released automatically after completion" (FR-017). Manual bank transfer: follows the one platform-wide settlement period set in FR-029 (default weekly, Sunday cutoff, Wednesday payout). There is no per-clinic payout frequency | Read-only; shown according to the clinic's payout method | no graph field (display) |

**Business Rules**:

- Billing settings accessible ONLY to the Owner by default: the permission "View and Edit Billing Settings" is held by FR-031 with the default Owner only (REQ-031-005); the Billing tab is hidden from roles without it (REQ-032-011, REQ-032-141)
- See REQ-032-022.
- Account number masked in read-only view (e.g., ●●●●●●1234), unmasked in edit mode (REQ-032-086)
- See REQ-032-017.
- Bank account information validated by S-02 Payment Service before saving (REQ-032-025)
- Bank account changes logged in audit trail (Owner user, timestamp, action) (REQ-032-020)
- Email confirmation sent to Owner after bank account details updated (REQ-032-088)
- Bank account details used by FR-017 billing workflow for provider payouts
- **Commission & Payout panel**: Read-only; values are set by admins in FR-015 Tab 7 and synchronized with FR-029. Providers cannot edit them and must contact support to discuss changes. The panel notes that existing confirmed bookings keep the commission snapshot taken at their confirmation (FR-029) (REQ-032-090)
- **Suspended clinic**: while the provider is Suspended, the Owner can still update the bank details (the change is audit-logged); the rest of billing is view-only (REQ-032-067)
- **Payout method and readiness**: The admin chooses the payout method (Stripe Connect or manual bank transfer) when creating the clinic in FR-015. The Owner sees the method and the readiness read-only and cannot change the method
- If bank account validation fails, display error message from S-02 and prevent saving (REQ-032-087)

**Notes**:

- Provide country selector to determine required fields (e.g., IBAN required for EU, routing number required for USA) (REQ-032-128)
- Show bank account format examples based on selected country
- Provide "Verify Bank Account" button to test bank account details with S-02 before saving (REQ-032-129)
- Display last bank account update timestamp
- Show next scheduled payout date and amount (if available)
- Provide link to payout history (handled by PR-05: Financial Management & Reporting)

---

### Screen 5: Help Centre

**Purpose**: Provide provider access to help resources, FAQs, guides, and contact support (content managed by admin via FR-033). Help Centre is organized as a main landing page with subscreens for each content type, each with distinct layouts optimized for their content format.

**Entry Point**: Provider navigates to "Help Centre" from settings menu or footer link

**Main Landing Page**:

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Search Bar | text | No | Global search across all Help Centre content | Max 200 chars, autocomplete suggestions | no graph field (control) |
| Category Navigation | navigation menu | No | Links to subscreens: FAQs, Tutorial Guides, Troubleshooting Tips, Policy Information, Resource Library, Video Tutorials, Contact Support, Feedback & Suggestions, My Support Cases, Service Status | N/A | ENT-help-centre-content.content_type |
| Most Popular Articles | card list | No | Top 5 most viewed/helpful articles across all categories (REQ-032-093) | Read-only, sorted by view count/helpfulness | ENT-help-centre-content.title, ENT-help-centre-content.view_count, ENT-help-centre-content.helpfulness_rating |
| Recently Updated | card list | No | Latest 5 updated articles across all categories (REQ-032-093) | Read-only, sorted by update date | ENT-help-centre-content.title, ENT-help-centre-content.updated_at |

**Business Rules**:

- All Help Centre content is read-only for providers (content managed exclusively by admins via FR-033) (REQ-032-012)
- Help Centre search behaviour (content types searched, 200-character limit, autocomplete) is defined by FR-022 (REQ-022-081)
- When a Help Centre search returns no results, the system shows "No results for '[query]'. Try different keywords or Contact Support." (same message as the patient Help Centre, FR-035) (REQ-032-130)
- Help Centre content updates (from admin) propagate to providers within 1 minute (REQ-032-092)
- Breadcrumb navigation available on all subscreens for easy return to home

---

#### Screen 5.1: FAQs

**Purpose**: Display frequently asked questions organized by topic with expandable/collapsible layout

**Layout Type**: Distinct FAQ layout (accordion/expandable sections)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| FAQ Topic Filter | category filter | No | Filter FAQs by topic (e.g., "Quote Management", "Payment Settings", "Aftercare") | Pre-defined topics from admin | ENT-help-centre-content.topic |
| FAQ Questions | accordion list | No | List of FAQ items with question and expandable answer | Each FAQ: question (text), answer (rich text/HTML), topic category, helpfulness rating | ENT-help-centre-content.title, ENT-help-centre-content.body, ENT-help-centre-content.topic, ENT-help-centre-content.helpfulness_rating |
| "Was this helpful?" Feedback | button group | No | Yes/No buttons for each FAQ | Records feedback for admin analytics | no graph field (control) |

**Business Rules**:

- FAQs organized by topic with expandable/collapsible accordion sections
- Clicking question expands to show answer; clicking again collapses
- Multiple FAQs can be expanded simultaneously
- Topic filter updates list instantly (client-side filtering)
- Feedback (Yes/No) recorded per FAQ for admin analytics (REQ-032-094)
- Search results highlight matching keywords in questions and answers

**Notes**:

- Accordion layout: question as header, answer expands below when clicked
- Visual indicator (chevron/arrow) shows expanded/collapsed state
- Related FAQs displayed at bottom of each FAQ answer
- FAQ topics displayed as filter pills/chips at top of page

---

#### Screen 5.2: Tutorial Guides, Troubleshooting Tips, Policy Information

**Purpose**: Display step-by-step guides, troubleshooting articles, and policy documents in article layout

**Layout Type**: Article layout (rich text content with formatting)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Article Title | display | No | Title of tutorial guide/tip/policy | Read-only | ENT-help-centre-content.title |
| Article Content | rich text/HTML | No | Formatted article content with headings, lists, images, screenshots | Read-only, supports HTML formatting | ENT-help-centre-content.body |
| Article Metadata | display | No | Publication date, last updated date, author (admin), category | Read-only | ENT-help-centre-content.published_at, ENT-help-centre-content.updated_at, ENT-help-centre-content.created_by_admin_id, ENT-help-centre-content.content_type |
| Table of Contents | navigation | No | Auto-generated from article headings (for long articles) | Read-only, clickable anchor links | no graph field (display) |
| Related Articles | card list | No | Related articles from same or other categories | Read-only, links to other articles | ENT-help-centre-content.related_content_ids |
| "Was this helpful?" Feedback | button group | No | Yes/No buttons | Records feedback for admin analytics | no graph field (control) |

**Business Rules**:

- Tutorial guides include step-by-step instructions with numbered lists and screenshots
- Troubleshooting tips organized by common issues with solutions
- Policy information displayed as formatted documents
- Table of contents auto-generated for articles with multiple headings (articles >1000 words)
- Related articles displayed at bottom based on category and tags
- Feedback recorded for admin analytics
- Print-friendly view available (removes navigation, optimizes for printing)

**Notes**:

- Article layout: full-width content area with formatted text, images, code blocks, lists
- Screenshots/images displayed inline with captions
- Step-by-step tutorials use numbered lists with visual separators
- Breadcrumb navigation: Help Centre > [Category] > [Article Title]
- Share article functionality (copy link, email link) (REQ-032-140)

---

#### Screen 5.3: Resource Library

**Purpose**: Display downloadable resources (templates, documents, PDFs) in file viewer layout

**Layout Type**: File viewer/download interface

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Resource List | card/grid | No | List of downloadable resources with thumbnails/icons | Each resource: name, description, file type, file size, download count, last updated | ENT-help-centre-content.title, ENT-help-centre-content.summary, ENT-help-centre-content.file_type, ENT-help-centre-content.file_size, ENT-help-centre-content.download_count, ENT-help-centre-content.updated_at, ENT-help-centre-content.thumbnail_url |
| Resource Category Filter | filter | No | Filter by resource type (Templates, Documents, Forms, etc.) | Pre-defined categories from admin | ENT-help-centre-content.resource_category |
| File Type Filter | filter | No | Filter by file format (PDF, DOCX, XLSX, etc.) | Pre-defined file types | ENT-help-centre-content.file_type |
| Preview Button | button | No | Preview resource before download (if supported format) | Opens preview modal or new tab | no graph field (control) |
| Download Button | button | No | Download resource file | Initiates file download | ENT-help-centre-content.attachments |

**Business Rules**:

- Resources displayed as cards/grid with file type icons and metadata
- Clicking resource card shows details: description, file size, download count, last updated date
- Preview available for PDF and image files (opens in modal or new tab) (REQ-032-131)
- Download initiates file download; download count incremented (REQ-032-098); opening a resource records the view through the FR-033 view write (REQ-033-097)
- Resources can be filtered by category and file type
- Search functionality searches resource names and descriptions

**Notes**:

- Grid/card layout: resource thumbnail/icon, name, file type badge, file size, download button
- File type icons: PDF, DOCX, XLSX, PNG, etc.
- Preview modal for PDFs with zoom controls
- Download tracking: shows "Downloaded X times" on resource card
- Empty state: "No resources available" when filters return no results

---

#### Screen 5.4: Video Tutorials

**Purpose**: Display video tutorials with embedded video player

**Layout Type**: Video viewer interface

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Video List | card/grid | No | List of video tutorials with thumbnails | Each video: title, description, duration, thumbnail, view count, publish date | ENT-help-centre-content.title, ENT-help-centre-content.summary, ENT-help-centre-content.duration, ENT-help-centre-content.thumbnail_url, ENT-help-centre-content.view_count, ENT-help-centre-content.published_at |
| Video Player | embedded player | No | Video player with play controls | Supports play, pause, volume, fullscreen, playback speed | ENT-help-centre-content.attachments |
| Video Transcript | expandable section | No | Text transcript of video (if available) | Read-only, expandable/collapsible | ENT-help-centre-content.transcript |
| Related Videos | card list | No | Related video tutorials | Read-only, links to other videos | ENT-help-centre-content.related_content_ids |
| "Was this helpful?" Feedback | button group | No | Yes/No buttons | Records feedback for admin analytics | no graph field (control) |

**Business Rules**:

- Videos embedded with standard video player controls (play, pause, volume, fullscreen, playback speed)
- Video thumbnails displayed in grid/list view
- Clicking video card opens video player (inline or modal)
- Video transcripts available (if provided by admin) in expandable section below player
- View count incremented when video plays for >30 seconds (REQ-032-099)
- Related videos displayed based on category and tags
- Feedback recorded for admin analytics

**Notes**:

- Video player: embedded HTML5 video player or YouTube/Vimeo embed
- Thumbnail grid: video thumbnail, title, duration badge, view count
- Video player supports: play/pause, volume control, fullscreen, playback speed (0.5x, 1x, 1.5x, 2x), progress bar
- Transcript: expandable section below video with searchable text
- Related videos: horizontal scrollable list or grid below current video

---

#### Screen 5.5: Contact Support

**Purpose**: Submit support requests via contact form with submission tracking

**Layout Type**: Form interface with submission tracking

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Support Request Form - Subject | text | Yes | Support request subject line | Min 10, max 200 chars (REQ-032-102, FR-034 REQ-034-130) | ENT-support-case.title |
| Support Request Form - Category | dropdown | No | Request category (Technical Issue, Payment Question, Feature Request, etc.) | Pre-defined categories | ENT-support-case.category |
| Support Request Form - Message | textarea | Yes | Detailed support request message | Max 5000 chars, min 20 chars (REQ-032-102) | ENT-support-case.description |
| Support Request Form - Priority | dropdown | No | Request priority (Low, Medium, High, Urgent) | Default: Medium (REQ-032-102) | ENT-support-case.priority |
| Support Request Form - Attachment | file upload | No | Optional screenshots or documents | Up to 5 files, 10MB each, formats JPG, PNG, PDF, DOC, DOCX (REQ-032-102, FR-034 REQ-034-036, REQ-034-037) | ENT-support-case.attachments |
| Submission Tracking | list | No | List of submitted support requests with status | Each request: subject, category, status (Open, In Progress, Resolved, Closed), submitted date, last updated, case number | ENT-support-case.case_id, ENT-support-case.title, ENT-support-case.category, ENT-support-case.status, ENT-support-case.submitted_at, ENT-support-case.last_updated_at |

**Business Rules**:

- Support contact form auto-populates provider contact information (name, email, clinic name) (REQ-032-101)
- Form submission creates a support case with a unique case number
- Support request confirmation displayed: "Support request submitted. Case #[number]. We aim to respond within 24 hours on business days." (REQ-032-103)
- Form submissions automatically create support cases in FR-034 Support Center & Ticketing System with status 'Open'; case management, admin responses, and status updates are handled in FR-034 (REQ-032-100)
- Submission tracking shows all user's support requests with status updates
- Status updates: Open → In Progress → Resolved → Closed (REQ-032-105)
- Provider can view request details and add follow-up messages (REQ-032-109)
- Email notification sent to provider when admin responds or updates status (REQ-032-111)

**Notes**:

- Form layout: fields stacked vertically with clear labels and validation
- File upload: drag-and-drop or file picker, shows upload progress
- Submission tracking: table/list view with status badges, sortable by date/status
- Ticket details: expandable view showing the full conversation thread (Screen 5.8)
- Response time note displayed: "We aim to respond within 24 hours on business days" (REQ-032-103)

---

#### Screen 5.6: Feedback & Suggestions

**Purpose**: Submit feedback and feature requests with submission tracking

**Layout Type**: Form interface with submission tracking

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Feedback Form - Type | dropdown | Yes | Feedback type (Feature Request, Bug Report, Suggestion, Other) | Pre-defined types | ENT-support-case.feedback_type |
| Feedback Form - Title | text | Yes | Brief title for feedback | Min 10, max 100 chars (REQ-032-104, FR-034 REQ-034-130) | ENT-support-case.title |
| Feedback Form - Description | textarea | Yes | Detailed feedback description | Max 5000 chars, min 20 chars (REQ-032-104) | ENT-support-case.description |
| Feedback Form - Priority | dropdown | No | Suggested priority (Low, Medium, High) | Default: Low (REQ-032-104) | ENT-support-case.priority |
| Submission Tracking | list | No | List of submitted feedback with status | Each submission: title, type, status (Open, In Progress, Resolved, Closed), feedback resolution (if applicable: Implemented, Planned, Declined, Under Review), submitted date, admin response | ENT-support-case.title, ENT-support-case.feedback_type, ENT-support-case.status, ENT-support-case.feedback_resolution, ENT-support-case.submitted_at, ENT-support-case-message.content |

**Business Rules**:

- Feedback form allows providers to submit feature requests, bug reports, and suggestions
- Form submission creates feedback record with unique ID
- Confirmation displayed: "Thank you for your feedback! We'll review your submission."
- Form submissions automatically create feedback cases in FR-034 Support Center & Ticketing System with status 'Open'; case tracking, admin responses, and resolution status are handled in FR-034 (REQ-032-100)
- Submission tracking shows all user's feedback submissions with status
- Status updates follow unified workflow: Open → In Progress → Resolved → Closed (feedback resolution outcome—Implemented, Planned, Declined, Under Review—tracked separately in FR-034) (REQ-032-105)
- Admin can respond to feedback; response visible in tracking list
- Feedback helps prioritize platform improvements

**Notes**:

- Form layout: similar to Contact Support form
- Feedback type selector determines form fields (e.g., Bug Report may include "Steps to Reproduce")
- Submission tracking: table/list view with status badges
- Status badges: color-coded (Open: blue, In Progress: yellow, Resolved: green, Closed: gray)
- Feedback resolution badges (when applicable): color-coded (Implemented: green, Planned: yellow, Declined: red, Under Review: blue)
- Admin response visible in expanded feedback details view

---

#### Screen 5.7: My Support Cases List

**Purpose**: View and manage all submitted support cases and feedback with filtering and search capabilities

**Layout Type**: List view with filters, search, and action buttons

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Filter Bar | filter group | No | Filter controls including: **Status Filter** (multi-select dropdown: Open, In Progress, Resolved, Closed; Default: Open + In Progress), **Type Filter** (multi-select dropdown: Support Request, Feedback; Default: All types), **Date Range Filter** (date picker; Default: Last 90 days) | Filters are cumulative (AND logic) | ENT-support-case.status, ENT-support-case.submitted_at |
| Search Bar | text input | No | Search cases by case ID, title, keywords | Min 3 chars to trigger search, real-time search; searches across Case ID, Title, Description, Message content (REQ-032-107) | no graph field (control) |
| Quick Stats Bar | stats component | N/A | Displays summary metrics: Open (X), In Progress (X), Resolved (X), Unread Messages (X) | Display only; computed over all of the clinic's cases, independent of the list filters (REQ-032-117) | no graph field (display component) |
| Case List Table | data table | N/A | Displays cases matching filters with 8 columns (see below); 20 cases per page default | Sortable columns, paginated; default sort by Last Updated descending | no graph field (list of the column rows below) |
| **Table Column 1**: Case ID | link | N/A | Unique case identifier (format: CASE-YYYY-#####); Width: 140px | Clickable link to case detail view (Screen 5.8); Sortable | ENT-support-case.case_id |
| **Table Column 2**: Title | text | N/A | Case title; Width: 250px | Truncated with ellipsis if >40 chars; full title shown on hover; Sortable | ENT-support-case.title |
| **Table Column 3**: Type | badge | N/A | Case type; Width: 120px | Support Request / Feedback; Color-coded badge; Sortable | ENT-support-case.case_type |
| **Table Column 4**: Status | badge | N/A | Current status with color coding; Width: 100px | Open (blue), In Progress (yellow), Resolved (green), Closed (gray); Sortable | ENT-support-case.status |
| **Table Column 5**: Feedback Resolution | badge | No | Resolution outcome for feedback cases; Width: 120px | Implemented (green) / Planned (yellow) / Declined (red) / Under Review (blue); Empty if not feedback or not set; Not sortable | ENT-support-case.feedback_resolution |
| **Table Column 6**: Submitted Date | datetime | N/A | Case creation timestamp (format: YYYY-MM-DD HH:mm); Width: 130px | Local timezone; Sortable | ENT-support-case.submitted_at |
| **Table Column 7**: Last Updated | datetime | N/A | Most recent modification timestamp (format: YYYY-MM-DD HH:mm); Width: 130px | Local timezone; Default sort column (descending); Sortable | ENT-support-case.last_updated_at |
| **Table Column 8**: Unread | badge/icon | No | Unread message indicator; Width: 60px | Shows unread message count if admin replied (e.g., "2 new"); Empty if no unread; Not sortable | ENT-support-case-message.is_read |
| Pagination Controls | component | N/A | Navigate through case list pages | 20 cases per page default; Shows: Previous, 1, 2, 3, ..., Next | no graph field (control) |

**Business Rules**:

- Default view shows Open and In Progress cases from last 90 days, sorted by Last Updated descending (one shared Rule with the admin case list: FR-034 REQ-034-114)
- The case list shows 20 cases per page by default (REQ-032-118)
- Providers can view all their submitted cases (both support requests from Screen 5.5 and feedback from Screen 5.6)
- Clicking case row or Case ID opens Screen 5.8 (Support Case Detail View); a case opened from a notification link opens directly on Screen 5.8 whatever the list filters (REQ-032-112)
- Status badges color-coded (Open=blue, In Progress=yellow, Resolved=green, Closed=gray)
- Type badges color-coded (Support Request=orange, Feedback=purple)
- Feedback Resolution badges color-coded (Implemented=green, Planned=yellow, Declined=red, Under Review=blue)
- Unread Messages indicator shows count of admin messages provider hasn't viewed yet (e.g., "2 new") (REQ-032-108)
- Cases with unread messages highlighted with subtle background color or bold text
- Search is real-time and searches across: Case ID, Case Title, Original Description, Message content (REQ-032-107)
- Filters are cumulative (AND logic between different filter types) (REQ-032-107)
- Filter options: Status (Open, In Progress, Resolved, Closed; default Open and In Progress), Type (Support Request, Feedback; default all types), Date Range (custom range on the case creation date; default last 90 days); several selections within one filter combine as OR (REQ-032-107)
- Filter selections persist during session (REQ-032-107)
- Quick Stats bar shows counts over all of the clinic's cases, independent of the list filters (REQ-032-117)
- If case has new admin messages since last view, "New Reply" badge shown prominently

**Notes**:

- Use sticky table header for scrolling through long case lists
- Display empty state message if no cases match filters: "No cases found. Try adjusting your filters or submit a new request via Contact Support." (REQ-032-133)
- Display empty state if no cases exist: "You haven't submitted any support cases yet. Visit Contact Support or Feedback & Suggestions to get help." (REQ-032-133)
- Show total case count matching current filters at top of table: "Showing X cases" (REQ-032-134)
- Consider implementing saved filter presets as future enhancement (e.g., "Open Issues", "All Feedback")
- Highlight urgent cases (High/Urgent priority) with warning icon in list

---

#### Screen 5.8: Support Case Detail View

**Purpose**: View complete case information, full communication thread with admin, and engage in two-way conversation

**Layout Type**: Detail view with communication interface

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Case ID | text (readonly) | N/A | Unique case identifier (e.g., CASE-2025-12345) | Display only | ENT-support-case.case_id |
| Case Title | text (readonly) | N/A | Case title | Display only | ENT-support-case.title |
| Status Badge | badge | N/A | Current case status with color coding | Open (blue), In Progress (yellow), Resolved (green), Closed (gray) | ENT-support-case.status |
| Feedback Resolution Badge | badge | No | Resolution outcome for feedback cases | Implemented (green), Planned (yellow), Declined (red), Under Review (blue); Only shown for feedback cases when resolution is set | ENT-support-case.feedback_resolution |
| Case Type | text (readonly) | N/A | Support Request or Feedback | Display only | ENT-support-case.case_type |
| Priority | text (readonly) | N/A | Case priority level (Low, Medium, High, Urgent) | Display only | ENT-support-case.priority |
| Submitted Date | datetime (readonly) | N/A | When case was created | Display only | ENT-support-case.submitted_at |
| Last Updated | datetime (readonly) | N/A | Most recent modification | Display only | ENT-support-case.last_updated_at |
| Original Description | text block | N/A | Initial submission description | Display only, expandable if long | ENT-support-case.description |
| Communication Thread | threaded conversation | N/A | Two-way conversation showing all messages from admin and provider with full context | Scrollable, chronological (oldest first), shows sender name, sender type badge, timestamp, message content, attachments | ENT-support-case-message.sender_name, ENT-support-case-message.sender_type, ENT-support-case-message.sent_at, ENT-support-case-message.content, ENT-support-case-message.attachments |
| Reply Message Box | textarea | No | Message composer for replying to admin | Max 5000 chars; enabled for Open, In Progress and Resolved cases, disabled for Closed cases (after a reopen request is sent it stays disabled and the screen shows "Request sent, awaiting admin"); Character counter displayed (REQ-032-110, REQ-032-114) | ENT-support-case-message.content |
| Attach Files Button | file upload | No | Attach files to reply message | Max 5 files, 10MB per file, formats: JPG, PNG, PDF, DOC, DOCX (REQ-032-110) | ENT-support-case-message.attachments |
| Send Reply Button | button | N/A | Sends reply message to admin | Enabled only if message box has content; disabled for Closed cases; a reply to a Resolved case reopens it (REQ-032-109) | no graph field (control) |
| Request Reopen Button | button | N/A | Request to reopen closed case | Only visible for Closed cases; opens reopen request modal (Screen 5.9) | no graph field (control) |
| Case Timeline | vertical timeline | N/A | Shows all case events with full context | Displays: case created, status changes, feedback resolution updates, messages sent/received, case resolved, case closed; Readonly, scrollable, reverse chronological (newest first) | ENT-support-case-timeline-event.event_type, ENT-support-case-timeline-event.event_timestamp, ENT-support-case-timeline-event.description |
| Back to List Button | button | N/A | Returns to My Support Cases list (Screen 5.7) | Click action, preserves filter state (REQ-032-132) | no graph field (control) |

**Communication Thread Structure**:

Each message in the thread displays:

- **Sender**: "Admin Support Team" or "You" (provider name)
- **Sender Type Badge**: Admin / Provider
- **Timestamp**: Date and time of message (e.g., "Jan 25, 2026 at 2:30 PM")
- **Message Content**: Full message text with formatting support
- **Attachments**: If any, displayed as downloadable links with file icons and file size
- **Read Status**: Shows "New" badge for unread admin messages

**Business Rules**:

- Case detail view shows complete communication thread with all messages from admin and provider
- Providers can reply to admin messages for Open, In Progress and Resolved cases via Reply Message Box; a reply to a Resolved case reopens it (FR-034 REQ-034-139) (REQ-032-109)
- When provider replies, message is sent to FR-034 system and appears in admin's case view (FR-034 Screen 3)
- An admin reply notifies the provider (support.case_admin_reply) and a provider reply notifies the assigned admin, or all support staff if unassigned (support.case_user_reply); recipients, content and channels are defined by the notification catalogue (FR-030 REQ-030-065 and REQ-030-066) (REQ-032-111)
- System marks messages as read when provider opens case detail view (REQ-032-108)
- Unread admin messages marked with "New" badge until provider views case
- For Resolved cases, Reply Message Box stays enabled with the banner: "This case was marked as resolved. Replying will reopen it." (REQ-032-109)
- For Closed cases, Reply Message Box is disabled; provider can only click "Request Reopen" button; after a request is sent the screen shows "Request sent, awaiting admin" (REQ-032-109, REQ-032-114)
- Communication Thread displays messages in chronological order (oldest first) to show conversation flow
- Case Timeline displays events in reverse chronological order (newest first) to show latest updates
- Attachment files validated before upload (file type, size, virus scan) (REQ-032-110)
- System displays confirmation after successful reply: "Reply sent. The support team will respond soon." (REQ-032-136)
- If provider navigates away with unsaved message content, system prompts: "You have unsaved changes. Discard?" (REQ-032-040)

**Notes**:

- Use different visual styling for admin messages vs provider messages (similar to chat interface: admin=gray background, provider=white background)
- Display attachment thumbnails with download links for images
- Use sticky header for case detail when scrolling through long communication threads
- Show typing indicator when admin is composing reply (future enhancement via WebSocket)
- Consider implementing desktop notifications for new admin replies (future enhancement)
- Show character count below Reply Message Box: "X / 5000 characters"
- Display file upload progress bar when attaching files
- For attached images, show inline preview thumbnails in communication thread

---

#### Screen 5.9: Reopen Case Request Modal

**Purpose**: Allow provider to ask the admin to reopen a closed case, with a reason

**Layout Type**: Modal dialog

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Previous Resolution Summary | text (readonly) | N/A | Resolution summary from when case was previously resolved | Display only, helps provider provide context | ENT-support-case-resolution.resolution_summary |
| Previous Closure Date | datetime (readonly) | N/A | Date when case was closed | Display only | ENT-support-case.closed_at |
| Reopening Reason | textarea | Yes | Reason for reopening case | Min 20 chars, max 500 chars; Example: "The issue is still occurring after following all troubleshooting steps" (REQ-032-113) | ENT-support-case-message.content |
| Priority Update | dropdown select | No | Priority the provider would like, sent as text in the reopen-request message; the admin decides | Options: Keep Current, Low, Medium, High, Urgent; Default: Keep Current | no graph field (sent as text in the message) |
| Submit Reopen Request Button | button | Yes | Submits the reopen request to admin as a flagged message in the case thread | Validates reason length; the admin is told through the FR-034 user-reply notice | no graph field (control) |
| Cancel Button | button | Yes | Closes modal without sending a request | No changes made | no graph field (control) |

**Business Rules**:

- Modal only accessible from Screen 5.8 when viewing Closed cases (REQ-032-113)
- System displays previous resolution summary and closure date for context
- Reopening reason required (min 20 chars) to prevent accidental/spam reopening (REQ-032-113)
- Provider can optionally state a requested priority, sent as text; the admin decides the priority (REQ-032-113)
- When submitted: (REQ-032-114)
  - A flagged reopen-request message (reason and optional requested priority as text) is added to the case thread through FR-034 (REQ-034-178)
  - The case stays Closed; only an admin can reopen it in FR-034
  - The admin is told through the FR-034 user-reply notice (support.case_user_reply) to the assigned admin, or all support staff if unassigned
- System displays confirmation: "Reopen request submitted. We'll review your case shortly." (REQ-032-137)
- After submission, modal closes and provider returns to Screen 5.8, which shows "Request sent, awaiting admin"; the case status is still Closed and the Reply Message Box stays disabled
- If an admin accepts the request, the admin reopens the case in FR-034 (status Open, REQ-034-145) and the Reply Message Box is enabled again
- If an admin answers but keeps the case Closed, the "Request sent, awaiting admin" banner clears and the Request Reopen button returns, so the provider may ask again (REQ-032-114)

**Notes**:

- Display warning if case was recently closed (e.g., within 24 hours): "This case was recently closed. Are you sure the issue persists?" (REQ-032-138)
- Consider adding "Reopen Reason Templates" dropdown for quick selection (e.g., "Issue persists", "New information available") (future enhancement)

---

#### Screen 5.10: Service Status

**Purpose**: Display platform service status and incident reports

**Layout Type**: Status page interface

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Overall Status Indicator | badge | No | Current platform status (All Systems Operational, Partial Outage, Major Outage, or Status not available when no status can be shown; the values are owned by FR-033, REQ-033-080) | Color-coded: green/yellow/red | ENT-service-status.overall_status |
| Service Components Status | list | No | Status of individual services/components | Each component: name, status (Operational, Degraded, Down), last updated | ENT-service-status.components |
| Incident History | timeline | No | Recent incidents and maintenance windows | Each incident: title, description, status (Investigating, Identified, Monitoring, Resolved), start time, end time, affected services | ENT-service-status.incidents |
| Maintenance Schedule | list | No | Upcoming scheduled maintenance | Each maintenance: title, description, scheduled start/end time, affected services | ENT-service-status.maintenance |

**Business Rules**:

- Service status page displays real-time platform health
- Overall status: "All Systems Operational" (green), "Partial Outage" (yellow), "Major Outage" (red), "Status not available" (grey) when no status can be shown
- Individual service components show status: Operational (green), Degraded (yellow), Down (red)
- Incident history shows recent incidents with timeline and resolution details
- Maintenance schedule shows upcoming planned maintenance windows
- Status updates automatically when admin updates status via admin platform (REQ-032-115)
- Status update notifications by email are a future enhancement, not in this release (FR-033 REQ-033-032) (REQ-032-115)

**Notes**:

- Status page layout: dashboard-style with status indicators and timeline
- Overall status badge: large, prominent, color-coded
- Service components: grid/list with status badges and last updated timestamps
- Incident timeline: chronological list with expandable details
- Maintenance schedule: calendar view or list view with countdown timers

---

## Business Rules

### General Module Rules

- **Rule 1**: All provider profile changes (logo, name, description, languages, awards) propagate to patient-facing quote comparison view within 1 minute (REQ-032-014)
- **Rule 2**: Provider notification preferences enforced by S-03 Notification Service for all platform notifications, except critical system alerts and mandatory provider notices, which bypass preferences. Which notices are mandatory, their recipients and their content are defined by the notification Rules (FR-020 REQ-020-020 and FR-030 Non-Disableable by Default) (REQ-032-009; REQ-032-031)
- **Rule 3**: All account settings changes (phone, timezone, password) logged in audit trail with timestamp, user ID, and IP address (REQ-032-020)
- **Rule 4**: Billing settings are accessible only to the holder of the "View and Edit Billing Settings" permission, which FR-031 grants to the Owner by default (REQ-031-005); roles without it cannot see or access billing settings (tab hidden from navigation) (REQ-032-022, REQ-032-141)
- **Rule 5**: All profile, language, awards, account, and notification fields documented in this FR are provider-editable within the Provider Dashboard (subject to role restrictions noted); reviews content and Help Centre articles are read-only views fed by their respective modules (staff roster managed by FR-009); providers may post responses to reviews via FR-013 Screen 6 response composer but cannot edit or delete review records (REQ-032-041)
- **Rule 6 — Provider account-status banner**: Provider account status is owned by FR-015. (REQ-032-030)
  - **Suspended**: The Owner and every FR-009 team member can still log in and see a persistent, non-dismissible banner on every Provider Platform page: "Your account is temporarily suspended. Reason: [admin-provided reason]. Contact support@hairlineapp.com for assistance." The reason is the Screen 4 reason recorded in FR-015. While suspended, the provider cannot receive new inquiries, submit quotes, or accept new work (FR-015 Rule 9); profile, documents, reviews, billing, and team management (FR-009 Rule 10) are view-only, except that the Owner can still update the bank details (audit-logged, REQ-032-067). Account security (password change), notification preferences, Help Centre, and support cases (Screens 5.5–5.9) remain available so the provider can contact admins, and the Owner can still submit the account closure request (REQ-032-067). A Suspended Owner who has not yet set a password can still use the activation link; the status stays Suspended afterwards (FR-015, REQ-032-067). Chat with patients on the provider's open `In Progress` and `Aftercare` cases also stays available. Clinical notes, photos, and aftercare answers and actions are blocked until the admin reassigns or decides the case (FR-015 Screen 4). (REQ-032-067)
  - **Deactivated**: Login is disabled for the Owner and all team members. A login attempt shows "This account has been deactivated. Contact support@hairlineapp.com for assistance." and no session is created. (REQ-032-068)
  - **Reactivated**: The banner is removed on the next page load and normal editing returns; nothing cancelled by the suspension is restored (FR-015 Screen 5). (REQ-032-069)

### Data & Privacy Rules

- **Privacy Rule 1**: Bank account details encrypted at rest using AES-256 and masked in UI (e.g., ●●●●●●1234) (REQ-032-017)
- **Privacy Rule 2**: Password stored as bcrypt hash (cost factor 12+), never stored in plain text (REQ-032-019)
- **Privacy Rule 3**: Approved account-closure requests result in FR-015 deactivation (account status = "Deactivated"; there is no separate "Deleted" status), with data archived (retention follows the system PRD, Platform-Wide Rules: One 10-year retention period) (REQ-032-023)
- **Audit Rule**: All profile changes, account settings changes, billing settings changes, and account closure requests logged in audit trail with: timestamp, user ID, IP address, action, old value, new value (bank details, password, phone and email values are masked) (REQ-032-020)
- **GDPR Compliance**: Provider account closure request gives the provider a path to request erasure (FR-015 deactivation with data archival per FR-023, not permanent deletion) (REQ-032-077)
- **Unsaved Changes Rule**: System displays unsaved changes indicator (e.g., dot or asterisk) on tabs with unsaved edits; when provider attempts to navigate away or quit, system displays reminder dialog "You have unsaved changes. Are you sure you want to leave?" with options to save, discard, or cancel (REQ-032-040)
- **Concurrent Edits Rule**: Provider profile saves are last-save-wins. If a provider user and an admin (FR-015), or two provider users, edit the same fields at the same time, the later save overwrites the earlier one; there is no conflict check and no conflict message. A save applies only the fields the user changed; untouched fields are not rewritten, so last save wins only when two people change the same field. Every save is logged in the audit trail with old and new values (REQ-032-042)

### Admin Editability Rules

**Editable by Admin (via A-09: System Settings & Configuration and FR-033: Help Centre Content Management)**:

- Help Centre content (FAQs, tutorial guides, troubleshooting tips, resource library, video tutorials, policy information)
- System language options available in profile language selection (owned by FR-021 and surfaced through settings)
- Country calling codes available in phone number selection (FR-026)
- Timezone options available in account settings (FR-026)
- Password policy parameters (configurable: max login attempts, lockout duration, OTP expiry, resend cooldown; password complexity is fixed, see system PRD, Platform-Wide Rules: Password and one-time-code policy) (FR-026)

**Fixed in Codebase (Not Editable)**:

- Password complexity requirements: minimum 12 characters with an uppercase letter, a lowercase letter, a digit and a special character, fixed by the platform password policy (REQ-SYS-007; REQ-032-066)
- Encryption algorithms: AES-256 for data at rest, TLS 1.3 for data in transit
- Role-based access control rules: billing settings need the permission "View and Edit Billing Settings", held by FR-031 with the default Owner only (REQ-032-141)
- Password hash algorithm: bcrypt with cost factor 12+
- Account closure workflow: admin deactivation through FR-015 only (no "Deleted" status), data retained (retention follows the system PRD, Platform-Wide Rules: One 10-year retention period)

**Configurable with Restrictions**:

- Notification preference options: admins can add/remove notification types via system configuration, but core notification types (quote, schedule, treatment, aftercare, review) are required (REQ-032-084)
- Bank account validation rules: S-02 Payment Service validates bank account format per country, admin cannot modify validation logic

### Payment & Billing Rules

- **Billing Rule 1**: Bank account details validated by S-02 Payment Service before saving (format validation only, no funds verification) (REQ-032-025)
- **Billing Rule 2**: Bank account details used by FR-017 billing workflow for provider payouts (admin-triggered after treatment completion)
- **Billing Rule 3**: Bank account changes need the permission "View and Edit Billing Settings" (FR-031, default Owner only); roles without it cannot see or access billing settings (tab hidden from navigation) (REQ-032-022, REQ-032-141)
- **Billing Rule 4**: Bank account details encrypted at rest and masked in UI (only last 4 digits visible in read-only view) (REQ-032-017)

### Integration, Security and Operating Rules

- **FR-015: Provider Management (Admin-Initiated) / Module A-02**: Commission display and account status
  - **Why needed**: Admins set commission, payout method, and provider status in FR-015
  - **Integration point**: Screen 4 Commission & Payout panel reads FR-015 Tab 7 values (FR-029 configuration); Rule 6 reads provider status and the latest suspension reason from FR-015 Screens 4-5
- **FR-021 / A-09: Multi-Language & Localization**: Language options for provider profile capacity
  - **Why needed**: Profile language selection must display centrally managed languages without conflating spoken-language capacity with Provider Dashboard UI language preference
- **FR-034 / A-10: Support Center & Ticketing**: Provider support request and feedback submission management with two-way communication
  - **Integration point**: Form submissions create support cases with provider ID linked and Ticket Source = "Provider Portal", Submitter Type = "Provider"; providers view and interact with their cases through Screen 5.7 (My Support Cases) which queries FR-034 case data including full communication thread; provider replies sent to FR-034 Communication Thread appear in admin's case detail view (FR-034 Screen 3); notification events (support.case_admin_reply, support.case_user_reply) trigger via S-03 (REQ-032-100)
- **Entity 1: Provider Profile Data (from PR-01: Auth & Team Management)**: Provider account information
  - **Why needed**: Settings module requires existing provider account with clinic name, email, and role information
  - **Source**: Provider onboarding module (A-02: Provider Management & Onboarding creates provider account; PR-01 manages team members)
- Provider support requests submitted via Help Centre: we aim to respond within 24 hours on business days (REQ-032-103)
- Providers access web platform via modern browsers (Chrome, Safari, Firefox, Edge - last 2 versions) per NFR-006
- Admins update Help Centre content at least monthly to keep resources current and relevant
- Admins aim to review and process provider account closure requests within 5 business days (a review target, not a guarantee)
- Provider profile updates (logo, awards) reviewed by admin for quality assurance (future enhancement, not MVP)
- Bank account details remain valid for at least 12 months; providers responsible for updating if bank account changes
- **Technology**: Image uploads (logo, awards) should use resumable upload protocol to handle network interruptions during large file uploads
- **Performance**: Profile updates should use optimistic UI updates (display success immediately, synchronize with backend asynchronously) to improve perceived performance
- **Storage**: Bank account details encrypted at rest using AES-256; encryption keys managed via secure key management service (e.g., AWS KMS, Google Cloud KMS)
- **Integration 1**: Provider Settings → S-03 Notification Service (notification preference enforcement)
  - **Authentication**: OAuth 2.0 bearer token (service-to-service)
  - **Error handling**: Retry with exponential backoff on 5xx errors; if S-03 unavailable for >5 minutes, log error and notify admin
- **Integration 2**: Billing Settings → S-02 Payment Service (bank account validation)
  - **Authentication**: OAuth 2.0 bearer token (service-to-service)
- **Integration 3**: Help Centre → Admin Content Database (read-only content display)
  - **Authentication**: Internal API (user authentication required, RBAC enforced per FR-009 as this is an authenticated provider area)
  - **Error handling**: If content unavailable, display cached version with "Content may be outdated" warning; retry after 1 minute
- **Authentication**: Multi-factor authentication (MFA) required for Owner role when accessing billing settings (future enhancement)
- **Authorization**: Role-based access control (RBAC) enforced for billing settings (permission "View and Edit Billing Settings", FR-031, default Owner only); API endpoints validate user role before allowing access
- **Encryption**: All provider data encrypted in transit (TLS 1.3) and at rest (AES-256); bank account details use field-level encryption with separate encryption keys
- **Audit trail**: Log all settings changes (profile, account, notifications, billing) with timestamp, user ID, IP address, action, old value, new value (REQ-032-020)
- **Threat mitigation**: Rate limiting on password change endpoint (max 5 attempts/hour/user) to prevent brute force attacks; rate limiting on image upload endpoint (max 10 uploads/hour/user) to prevent abuse (REQ-032-049)
- **Compliance**: GDPR-compliant account closure (FR-015 deactivation with data archival); PCI-DSS compliance for bank account data handling (no card data stored, only bank account details for payouts)
- **Provider Notification Preferences**: Owned by FR-030 (Notification Rules & Configuration). Screen 3 shows and edits it: six notification type toggles (quote, schedule, treatment start, aftercare, review, promotion/discount) and the email and push channels, one record per provider organization.

---

## Dependencies

- FR-015: Commission display and account status
- FR-020 / S-03: Notification preferences integration
- FR-021: Language options for provider profile capacity
- FR-026: Country codes, timezone options (fixed offsets, REQ-026-121), password policy (REQ-SYS-007)
- FR-031: Permission "View and Edit Billing Settings" (default Owner only) and the per-feature role matrix
- FR-009: Team roles and team member accounts
- FR-017: Bank account details for payouts and payout readiness (REQ-017-064)
- FR-033: Help Centre content, view and vote records (REQ-033-096, REQ-033-097)
- FR-013: Provider review list and review detail screens
- FR-034: Provider support request and feedback submission management with two-way communication

---

## User Scenarios & Testing

### User Story 1 - Complete Provider Profile Setup (Priority: P1)

A newly onboarded provider (Owner role) completes their clinic profile by uploading logo, entering description, selecting languages, and adding awards to maximize visibility to patients during quote comparison.

**Why this priority**: Profile completeness directly impacts patient trust and quote request conversion rate. Providers with complete profiles (logo, awards, description) receive 40% more quote requests than providers with incomplete profiles.

**Independent Test**: Can be fully tested by creating new provider account, uploading logo and awards, saving profile, and verifying profile appears correctly in patient quote comparison view.

**Acceptance Scenarios**:

1. **Given** provider has newly created account with incomplete profile, **When** provider navigates to Profile section and uploads clinic logo (2MB PNG), enters description (200 chars), selects 3 languages (English, Turkish, Spanish), and saves profile, **Then** system saves profile successfully, displays "Profile updated successfully" message, and profile appears in patient app within 1 minute with logo, description, and language tags
2. **Given** provider has completed basic profile, **When** provider adds award entry (name: "Best Hair Transplant Clinic 2023", description: "Awarded by Medical Tourism Association", year: 2023, uploads award image 1.5MB JPEG), **Then** system validates award image size and format, saves award entry, displays award in "Awards & Certifications" section in provider profile
3. **Given** provider attempts to save profile with missing required field (description empty), **When** provider clicks "Save Changes", **Then** system validates form, highlights description field in red, displays error "Clinic description is required (min 50 chars)", and prevents saving until description completed

---

### User Story 2 - Configure Notification Preferences (Priority: P1)

A provider clinic coordinator configures notification preferences to receive email and push notifications for quote and schedule alerts, but disables aftercare notifications (handled by different team).

**Why this priority**: Notification preferences directly impact provider response time to patient inquiries. Providers who configure preferences to match their workflow respond to quotes 30% faster than providers using default settings.

**Independent Test**: Can be fully tested by configuring notification preferences, triggering test notifications (quote alert, schedule reminder), and verifying notifications sent only via enabled channels.

**Acceptance Scenarios**:

1. **Given** provider has default notification preferences (all types enabled, email and push enabled), **When** provider navigates to Settings → Notifications, disables "Aftercare Notifications" toggle, saves preferences, **Then** system saves preferences, displays "Notification preferences updated" message, updates S-03 Notification Service, and provider receives no aftercare notifications but receives quote/schedule notifications via email and push
2. **Given** provider disables all notification types, **When** provider clicks "Save Preferences", **Then** system displays confirmation dialog "Warning: You have disabled all notifications. You may miss important updates about inquiries, appointments, and reviews. Are you sure?", requires provider confirmation, and if confirmed, saves "all disabled" preference and S-03 stops sending notifications (except critical system alerts and mandatory notices such as `quote.cancelled_inquiry`)

---

### User Story 3 - Update Account Settings (Phone, Timezone, Password) (Priority: P1)

A team member updates their own phone number, changes their own timezone, and changes their password for security.

**Why this priority**: Account settings ensure provider security and localization. Timezone accuracy ensures providers don't miss appointment times due to timezone confusion.

**Independent Test**: Can be fully tested by updating phone number, timezone, and password in account settings, verifying changes saved correctly, and confirming password change email sent.

**Acceptance Scenarios**:

1. **Given** provider has phone number +90 555 123 4567 (Turkey) and timezone (GMT+3) Istanbul, **When** provider navigates to Account Settings, changes country code to +44 (UK), enters phone number 7700 900123, changes timezone to (GMT+0) London, saves settings, **Then** system validates phone number format for UK, saves phone number in international format (+44 7700 900123), saves the timezone for this person only, displays success message, and all future dashboard timestamps for this person display in London timezone (other team members keep their own, REQ-032-145)
2. **Given** provider wants to change password, **When** provider enters current password "OldP@ssw0rd2023!", enters new password "NewP@ssw0rd2024!", enters confirmation "NewP@ssw0rd2024!", clicks "Change Password", **Then** system validates current password matches database, validates new password meets security policy (≥12 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char), hashes new password using bcrypt, saves password hash, logs password change in audit trail, displays "Password changed successfully" message, and sends email notification to provider email address
3. **Given** provider enters incorrect current password when changing password, **When** provider submits password change form, **Then** system validates current password, detects mismatch, displays error "Current password is incorrect", and prevents password change until correct current password entered

---

### User Story 4 - Manage Billing Settings (Owner Role Only) (Priority: P1)

A provider Owner adds bank account details for receiving payouts from Hairline platform after completing first treatment.

**Why this priority**: Billing settings required for provider payouts per FR-017. Without bank account details, provider cannot receive payout for completed treatments. 95% of providers add billing settings within 7 days of completing first treatment.

**Independent Test**: Can be fully tested by adding bank account details as Owner role, verifying S-02 validation succeeds, confirming bank account saved encrypted, and testing non-owner role denied access.

**Acceptance Scenarios**:

1. **Given** provider Owner has completed first treatment and needs to receive payout, **When** provider Owner navigates to Settings → Billing, enters bank account details (Account Holder: "Istanbul Hair Clinic Ltd", Bank: "Garanti BBVA", Account Number: "TR123456789012345678901234", SWIFT: "TGBATRISXXX", IBAN: "TR12 0001 0012 3456 7890 1234 56"), clicks "Save Bank Account", **Then** system sends validation request to S-02 Payment Service, S-02 validates bank account format, system saves bank account details encrypted with AES-256, logs billing settings change in audit trail, displays "Bank account details saved successfully" message, sends confirmation email to Owner, and bank account used for next provider payout
2. **Given** provider Owner enters invalid IBAN format (too short), **When** provider Owner submits bank account form with IBAN "TR1234", **Then** system validates IBAN format, detects invalid format (Turkey IBAN requires 26 chars), displays error "Invalid IBAN format. Turkey IBAN must be 26 characters (e.g., TR12 0001 0012 3456 7890 1234 56)", and prevents saving until valid IBAN entered
3. **Given** provider has Manager role (not Owner), **When** the Manager navigates to Settings & Support > Settings, **Then** system validates the "View and Edit Billing Settings" permission (FR-031, default Owner only), finds it missing, and hides the Billing tab from navigation (non-owner cannot see or access billing settings)

---

### User Story 5 - Access Help Centre Resources (Priority: P2)

A provider searches Help Centre for answer to question "How do I edit a quote after submission?" and finds answer in FAQ without contacting support.

**Why this priority**: Help Centre self-service reduces support ticket volume by 40% and improves provider satisfaction. 70% of provider questions resolved via Help Centre without support contact.

**Independent Test**: Can be fully tested by accessing Help Centre, searching for FAQ, reading answer, submitting feedback, and verifying support request form works.

**Acceptance Scenarios**:

1. **Given** provider has question about editing quotes, **When** provider navigates to Help Centre, clicks "FAQs" category, selects topic "Quote Management", clicks question "How do I edit a quote after submission?", **Then** system expands answer with detailed instructions, provider reads answer, clicks "Was this helpful? Yes", system records feedback for admin analytics
2. **Given** provider needs to contact support, **When** provider navigates to Help Centre, clicks "Contact Support", fills support form (Subject: "Payment issue", Message: "I haven't received my payout for last week", uploads screenshot 2MB PNG), submits request, **Then** system validates form, sends support request to admin team, displays confirmation "Support request submitted. Case #[number]. We aim to respond within 24 hours on business days.", and admin receives support request in admin dashboard
3. **Given** provider wants to download quote template, **When** provider navigates to Help Centre, clicks "Resource Library", clicks "Download Quote Template" (PDF file), **Then** system initiates file download, provider saves file to local device

---

### User Story 6 - View and Reply to Support Cases (Two-Way Communication) (Priority: P2)

A provider submits a support request about a technical issue, receives admin response, replies with additional information, and tracks the case resolution through two-way conversation.

**Why this priority**: Two-way communication with admin support improves provider satisfaction and reduces resolution time by 40% compared to email-only support. Providers need visibility into case status and ability to provide follow-up information without creating duplicate tickets.

**Independent Test**: Can be fully tested by submitting support request via Screen 5.5, viewing case in My Support Cases screen (Screen 5.7), reading admin reply, sending reply message with attachment, verifying message appears in admin's case view (FR-034 Screen 3), and confirming notifications sent via S-03.

**Acceptance Scenarios**:

1. **Given** provider submitted support request yesterday about payment issue, **When** admin replies to case with troubleshooting steps, **Then** provider receives email notification "Your support case CASE-2025-12345 has a new reply", provider clicks link in email, system opens the case directly on its detail screen, provider reads admin's reply in Communication Thread, provider clicks Reply Message Box, types "Thank you, I tried those steps but still having the issue", attaches error screenshot, clicks Send Reply, system sends reply to FR-034, displays confirmation "Reply sent", and admin receives notification via S-03
2. **Given** provider has 3 open support cases and 2 closed cases, **When** provider navigates to Help Centre → My Support Cases, **Then** system displays case list with 5 cases total, default filter shows 3 open cases (Open + In Progress statuses), each case row shows Case ID, Title, Type, Status badge, Submitted Date, Last Updated, and Unread indicator showing "2" for cases with new admin replies, provider clicks filter to include Closed status, system displays all 5 cases
3. **Given** provider's issue was resolved and case is marked Closed, **When** provider discovers issue persists 2 days later, navigates to My Support Cases, opens closed case, **Then** system displays case with Status "Closed" and resolution summary, Reply Message Box is disabled with message "This case is closed. Click 'Request Reopen' if issue persists.", provider clicks Request Reopen button, system opens modal, provider enters reopening reason "Issue is still occurring after following all troubleshooting steps", selects priority "High", clicks Submit, system adds a flagged reopen-request message to the thread, tells the admin through the FR-034 user-reply notice, keeps the case Closed, displays confirmation "Reopen request submitted" and shows "Request sent, awaiting admin" with the reply box still disabled (REQ-032-113, REQ-032-114)
4. **Given** provider wants to find past case about billing, **When** provider opens My Support Cases, enters "payout" in search bar, selects Resolved status filter, **Then** system displays all resolved cases containing keyword "payout" in Case ID, Title, Description, or Messages, provider clicks case to view details and reviews the case history for reference

---

### User Story 7 - Request Account Closure (Priority: P2)

A provider closing their clinic permanently requests account closure, and an admin processes the request by deactivating the provider in FR-015.

**Why this priority**: Account closure gives the provider a path to leave the platform and request erasure, and ensures the platform doesn't keep inactive accounts open. Closure is implemented as FR-015 deactivation with data archival per FR-023 compliance requirements; there is no separate "Deleted" status.

**Independent Test**: Can be fully tested by submitting an account closure request as provider, verifying admin receives request, admin deactivates the provider in FR-015, provider status becomes Deactivated, the FR-015 cascade runs, and provider data is archived.

**Acceptance Scenarios**:

1. **Given** provider is closing clinic permanently, **When** provider navigates to Settings → Account Settings, clicks "Request account closure", checks "I understand" checkbox, enters reason "Closing clinic permanently", clicks "Submit Closure Request", **Then** system creates account closure request with status "Pending Admin Review", logs the request in audit trail, sends notification to admin team, displays confirmation "Account closure request submitted. We aim to review and process your request within 5 business days. You will receive an email once your account is deactivated.", and provider account keeps its current status until admin processes it
2. **Given** admin receives account closure request, **When** admin deactivates the provider from the request via FR-015 Screen 4, **Then** system sets account status to "Deactivated", blocks provider login, hides the provider profile, cancels non-terminal cases under the FR-015 cascade, retains all data in archive per FR-023, sets the request to "Approved", and sends the FR-015 deactivation email
3. **Given** provider has 3 active bookings, **When** provider submits an account closure request, **Then** system accepts the request without blocking; when the admin later deactivates the provider, the 3 bookings are cancelled under the FR-015 cascade with patient and admin-support notifications, and any captured payments are reconciled by FR-017

---

### Edge Cases

- What happens when **provider uploads 10MB logo image exceeding 5MB limit**?
  - System validates image size during upload, detects size exceeds limit, displays error "Image too large. Maximum size is 5MB. Please compress or choose a smaller image.", and prevents upload until valid image selected (REQ-032-001)

- How does system handle **provider changes password to same as current password**?
  - System validates new password ≠ current password, detects match, displays error "New password must be different from current password", and prevents password change until different password entered (REQ-032-065)

- What occurs if **S-03 Notification Service unavailable when provider saves notification preferences**?
  - System attempts to update S-03 with new preferences, detects S-03 unavailable (timeout or 5xx error), queues preference update for retry (exponential backoff), displays success message to provider "Notification preferences updated" (optimistic UI), logs error for admin monitoring, and retries preference update every 1 minute for up to 5 minutes; if S-03 still unavailable after 5 minutes, admin receives alert (REQ-032-083)

- What happens when **S-02 Payment Service returns validation error for bank account details**?
  - System receives validation error from S-02 (e.g., "Bank not found" or "SWIFT code mismatch"), displays error message to provider "Bank account validation failed: [error detail from S-02]. Please verify your bank details and try again.", prevents saving bank account details, and provider must correct details and retry (REQ-032-087)

- How does system handle **the Owner role is handed to another person**?
  - A Hairline admin hands the Owner role over (FR-015); the previous Owner becomes a Manager, and next time that user navigates to Settings & Support > Settings, the Billing tab is hidden from navigation (non-owner cannot see or access billing settings); existing bank account details stay with the clinic and are accessible to the new Owner (REQ-032-089)

- What occurs if **Help Centre content fails to load due to network issue**?
  - System attempts to fetch Help Centre content from admin content database, detects network timeout or error, displays cached version of Help Centre content (if available) with warning banner "Content may be outdated. Please refresh to load latest updates.", and provides "Retry" button for manual refresh (REQ-032-097)

- What happens when **the Owner submits a second closure request while one is pending**?
  - System refuses the submission with "A closure request is already pending.", creates no second record, and the closure card keeps showing the pending request with the button disabled (REQ-032-071)

- How to manage **provider uploads award image with virus or malicious content**?
  - System scans uploaded image using anti-virus/malware scanning service (e.g., ClamAV), detects malicious content, deletes uploaded file, displays error "Image upload blocked due to security concerns. Please try a different image or contact support if this was a mistake.", logs security event for admin review, and prevents award image from being saved (REQ-032-048)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-032-001**: System MUST allow providers to upload and update clinic logo/profile picture (max 5MB, JPEG/PNG, min 200x200px)
- **REQ-032-002**: System MUST allow providers to select supported languages using the centrally managed system language options owned by FR-021 (Multi-Language & Localization), which are surfaced via FR-026 App Settings.
- **REQ-032-003**: System MUST allow providers to add, edit, delete awards with direct image upload (name, description, year, award image max 2MB)
- **REQ-032-004**: System MUST allow providers to update basic clinic information (name, description, contact email)
- **REQ-032-005**: System MUST allow each team member to configure their own phone number with worldwide country code selection (FR-026 country codes)
- **REQ-032-006**: System MUST allow each team member to select their own timezone from the FR-026 list of fixed-offset options (GMT-12 to GMT+14)
- **REQ-032-007**: System MUST allow each team member to change their own password with current password verification and the platform password policy (REQ-SYS-007)
- **REQ-032-008**: System MUST allow providers to configure unified notification preferences (individual notification type toggles for quote, schedule, treatment start, aftercare, review, and promotion/discount notifications + global channel preferences: email, push)
- **REQ-032-009**: System MUST enforce notification preferences via S-03 Notification Service (FR-020 integration)
- **REQ-032-010**: System MUST allow provider Owners to manage billing settings (bank account details for payouts, FR-017 integration)
- **REQ-032-011**: System MUST restrict billing settings access to the holder of the permission "View and Edit Billing Settings", held by FR-031 with the default Owner only (REQ-031-005)
- **REQ-032-012**: System MUST allow providers to access Help Centre with admin-managed content (FR-033 integration)
- **REQ-032-013**: System MUST allow the Owner to request account closure; the request is processed by an admin, who deactivates the provider through FR-015 (no self-service deactivation)

### Data Requirements

- **REQ-032-014**: System MUST persist provider profile data (logo, name, description, languages, awards) and propagate to patient quote comparison view within 1 minute
- **REQ-032-015**: System MUST persist account settings per person on the team member record (phone number in international format, timezone, password hash), for every role
- **REQ-032-016**: System MUST persist notification preferences and synchronize with S-03 Notification Service within 1 minute
- **REQ-032-017**: System MUST persist bank account details encrypted at rest (AES-256) and mask in UI (last 4 digits visible)

### Security & Privacy Requirements

- **REQ-032-018**: System MUST encrypt bank account details at rest using AES-256
- **REQ-032-019**: System MUST hash passwords using bcrypt (cost factor 12+) and never store plain text passwords
- **REQ-032-020**: System MUST log all profile changes, account settings changes, billing settings changes, and account closure requests in audit trail (timestamp, user ID, IP address, action, and old/new values; bank details, password, phone and email values are masked)
- **REQ-032-021**: System MUST send email notification to provider after password change (security alert)
- **REQ-032-022**: System MUST enforce role-based access control for billing settings (permission "View and Edit Billing Settings", FR-031, default Owner only; roles without it cannot see or access billing settings tab)
- **REQ-032-023**: System MUST process approved account-closure requests as FR-015 deactivation (account status = "Deactivated", standard FR-015 cascade, data archived; retention follows the system PRD, Platform-Wide Rules: One 10-year retention period)

### Integration Requirements

- **REQ-032-024**: System MUST integrate with S-03 Notification Service to enforce provider notification preferences (FR-020)
- **REQ-032-025**: System MUST integrate with S-02 Payment Service to validate bank account details format before saving
- **REQ-032-026**: System MUST integrate with FR-026/FR-021 language configuration to provide centrally managed language options in profile language selection (FR-021 is canonical for supported locales; FR-026 surfaces these via App Settings)
- **REQ-032-027**: System MUST integrate with FR-026 to provide country codes and fixed-offset timezone options in account settings
- **REQ-032-028**: System MUST integrate with FR-033 to display admin-managed Help Centre content
- **REQ-032-029**: System MUST show provider Owners a read-only Commission & Payout panel in Screen 4 with commission model, value, Flat Rate Currency, Effective Date, any scheduled configuration, and payout timing (automatic release on the Stripe Connect rail; the one platform-wide settlement period owned by FR-029 on the manual rail; there is no per-clinic payout frequency), plus the payout method (chosen by the admin when the clinic is created in FR-015) and payout readiness
- **REQ-032-030**: System MUST apply Rule 6: show a persistent Account Suspended banner with the admin reason to all provider users while suspended, restrict editing to the listed exceptions, and block login with a deactivation message once deactivated
- **REQ-032-031**: System MUST NOT offer a provider notification preference toggle for any mandatory provider notice, and MUST deliver each mandatory notice to the affected provider regardless of notification type and channel preferences. Which notices are mandatory, to whom they go and what they say is defined by the notification Rules: FR-020 REQ-020-020 for the inquiry-cancelled quote notice (`quote.cancelled_inquiry`) and FR-030 Non-Disableable by Default for the others
- **REQ-032-141**: System MUST apply the who-edits-what table in Screen 1 (General Business Rules): clinic profile, languages, awards and documents are edited by the Owner and a Manager by default, gated by the FR-031 permission "Edit Profile"; notification settings are gated by "Edit Notification Settings" (REQ-032-142); the account closure request by the Owner only; personal account settings by every role for their own account only; billing settings need the permission "View and Edit Billing Settings", held by FR-031 with the default Owner only (REQ-031-005)
- **REQ-032-142**: System MUST let only the holders of the FR-031 permission "Edit Notification Settings" (by default the Owner and a Manager) change the clinic's notification settings; other roles see them read-only; every change is audit-logged with the user who made it
- **REQ-032-143**: System MUST send support case notices (admin reply, status change, resolved) always, with no toggle; Email and Push MAY both be off for a notification type, but mandatory notices ignore the setting
- **REQ-032-144**: System MUST show Account Email read-only for every role. The Owner's login email is changed only by a Hairline admin (FR-015, REQ-015-114); a team member's email is changed by contacting support
- **REQ-032-145**: System MUST save the timezone per person; at a person's first login System MUST set it without a prompt to the listed whole-hour offset nearest to the browser time zone (UTC when the browser zone cannot be read), and the person can change it on Screen 2 at any time; dates display with the fixed offsets of the FR-026 timezone list (REQ-026-121)
- **REQ-032-146**: System MUST show and require the bank form only when the Payout Method is Manual bank transfer; for Stripe Connect it MUST show a status panel and a "Complete Stripe sign-up" link; Payout Readiness is display only and owned by FR-017 (REQ-017-064)
- **REQ-032-147**: System MUST offer Active and Preparation locales in the language list, display every catalog locale already saved, and keep a saved entry when its locale becomes Inactive
- **REQ-032-148**: System MUST run Reviews tab filter, sort and paging on the server over the whole review list, show the Edited marker (FR-013 REQ-013-032), and link to the FR-013 provider review list and review detail screens

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-25 | 1.20 | Cross-FR alignment: password complexity follows the platform password policy (REQ-SYS-007, REQ-032-066); no other wording change. | Product Owner / Documentation |
| 2026-11-24 | 1.19 | Logic review pass 2: video view recorded after 30 seconds of play; provider only replies (no resolve control); support form limits aligned with FR-034 (subject and feedback title minimum 10, up to 5 attachments, DOC added); phone number required, unique per user within the provider and verified when changed; who-edits-what table names the FR-031 permission per row (Edit Profile, Edit Notification Settings, View and Edit Billing Settings) and notification settings follow "Edit Notification Settings"; reopen request outcome (admin reopens in FR-034, or answers and the Request Reopen button returns); closure card pending state and refusal of a second request; Account Name sync step and Owner handover rule; timezone set silently at first login; audit steps for phone and timezone changes; "we aim to review within 5 business days" for closure. Rules changed: REQ-032-061, 062, 064, 071, 073, 102, 104, 114, 125, 141, 142, 145. | Product Owner / Documentation |
| 2026-11-24 | 1.18 | Logic review pass 1: support case reply and reopen rules aligned with FR-034 (reply enabled for Resolved, reopen request is a flagged message, case stays Closed); 24-hour response note on business days; Service Status fourth value and no subscription; closure and role wording (keeps its current status, Owner role handed over by an admin, Suspended Owner exceptions); Account Email read-only and per-person account settings including timezone; notification settings roles and support notices; bank form for Manual bank transfer only with Stripe panel; language list; Help Centre view and vote records; Reviews tab server-side paging and Edited marker; billing permission cited from FR-031 with a who-edits-what table; new rules REQ-032-141 to REQ-032-148. | Product Owner / Documentation |
| 2026-11-22 | 1.17 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.16) and the change requests CR-FR032-20261015-01, CR-FR032-20261015-02, CR-FR032-20261015-03, CR-FR032-20261016-01, CR-FR015-20261027-01 and CR-FR029-20261015-01 are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Joachim Trung Tuan | 2026-10-18 | Approved FR-032 v1.10 to v1.12 via MTG-002 decision log (documentation only), including CR-FR032-20261016-01 |
| Product Owner | Joachim Trung Tuan | 2026-10-27 | Approved FR-032 v1.13 (documentation only) |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Based on**: FR-032 from system-prd.md, Provider Platform Transcriptions Part 1 & 2
**Last Updated**: 2026-11-25
