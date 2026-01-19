# Product Requirements Document: Provider Dashboard Settings & Profile Management

**Module**: PR-06: Profile & Settings Management
**Feature Branch**: `fr032-provider-dashboard-settings`
**Created**: 2025-11-17
**Status**: ✅ Verified & Approved
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
- Providers request account deletion (soft-delete with admin approval)
- Providers browse Reviews as a tab within the Provider Profile detailed page to read patient feedback, filter by rating, and respond if workflow allows (responses handled by future enhancement; current scope is read-only)

**Admin Platform (A-XX)**:

- Admins create and manage Help Centre content (FAQs, guides, videos, resources)
- Admins approve provider account deletion requests

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

- Provider navigates to "Settings & Support > Settings" from main dashboard navigation
- Provider clicks on notification icon to configure preferences
- Provider accesses Help Centre from footer or help icon
- Provider Owner role accesses billing settings from financial dashboard

**System-Initiated**:

- System prompts provider to complete profile setup during onboarding
- System sends notification approval requests when admin creates platform-wide discount

---

## Business Workflows

### Main Flow: Update Provider Profile Information

**Actors**: Provider (Admin, Owner), System
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
6. Provider selects supported languages from multi-select dropdown (consumes centrally managed language list from FR-026)
7. Provider edits clinic name, description, contact email, Location - City
8. Provider clicks "Add Award" to add new award entry
   - System opens award form (name, issuer/organization, description, year, award image)
   - Provider fills award details and uploads award image
   - System validates award image (<2MB)
9. Provider clicks "Save Changes" on the current tab
10. System validates all required fields for the current tab (clinic name, description)
11. System saves profile updates for the current tab with timestamp
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
  3. System removes award from profile (soft-delete, retained in archive)
  4. System displays success message "Award deleted"
- **Outcome**: Award removed from public provider profile

**A3: Provider Selects Multiple Languages**:

- **Trigger**: Provider opens language selection dropdown
- **Steps**:
  1. System displays all available languages from centrally managed language list (FR-026)
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

**Actors**: Provider (any role), System
**Trigger**: Provider navigates to "Settings" → "Notifications"
**Outcome**: Provider notification preferences updated and enforced by S-03 Notification Service

**Steps**:

1. Provider navigates to Settings → Notifications
2. System displays unified notification settings with two sections:
   - **Section A: Notification Types** (individual toggles)
   - **Section B: Global Channel Preferences** (email, push)
3. Provider reviews current settings (all loaded from database)
4. Provider toggles individual notification types:
   - ☑ Quote Notifications (new inquiry received, quote expiring soon)
   - ☑ Schedule Notifications (appointment confirmed, appointment reminder)
   - ☑ Treatment Start Notifications (patient checked in, procedure started)
   - ☐ Aftercare Notifications (patient milestone completed, urgent aftercare alert) — DISABLED
   - ☑ Review Notifications (new review posted, review requires response)
   - ☑ Promotion/Discount Notifications (new platform discounts created by admin that require provider acceptance/opt-in)
5. Provider configures global channel preferences:
   - Email: ☑ Enabled (default email address from profile)
   - Push/In-App: ☑ Enabled (web portal notifications)
6. Provider clicks "Save Preferences" on the Notifications tab
7. System validates settings
8. System saves notification preferences to database
9. System displays success message "Notification preferences updated"
10. System logs preference change in audit trail
11. System updates S-03 Notification Service with new preference rules
12. S-03 enforces preferences for all future notifications (e.g., aftercare notifications will NOT be sent)

### Supporting Flow: Browse Reviews

**Actors**: Provider (any role), System  
**Trigger**: Provider selects `Reviews` tab within the Provider Profile detailed page  
**Outcome**: Provider views Reviews tab to filter/sort reviews and read full feedback that corresponds to review notifications.

**Steps**:

1. Provider opens Provider Profile page and selects Reviews tab.
2. System loads rating summary, distribution bars, filters, and first page of review cards.
3. Provider applies rating filters or changes sort order (e.g., "Most recent").
4. System updates list instantly; provider paginates if needed to view more results.
5. If provider arrived via a Review Notification, the associated review is auto-highlighted/highlighted within list.

**Outcome**: Provider can quickly review patient sentiment and correlate it with notifications without modifying review content.

### Alternative Flows

**A5: Provider Disables All Notification Types**:

- **Trigger**: Provider unchecks all notification type toggles
- **Steps**:
  1. Provider disables all five notification types
  2. Provider clicks "Save Preferences"
  3. System displays confirmation dialog "Warning: You have disabled all notifications. You may miss important updates about inquiries, appointments, and reviews. Are you sure?"
  4. Provider confirms or cancels
  5. If confirmed, system saves "all disabled" preference
  6. S-03 stops sending notifications to this provider (except critical system alerts)
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

**Actors**: Provider (any role), System
**Trigger**: Provider navigates to "Settings" → "Account Settings"
**Outcome**: Provider account settings updated (phone number with country code, timezone, password)

**Steps**:

1. Provider navigates to Settings → Account Settings
2. System displays account settings form with current values:
   - Phone Number: +90 555 123 4567 (country code + number)
   - Timezone: (GMT+3) Istanbul
   - Password: ●●●●●●●● (masked)
3. Provider clicks "Edit Phone Number"
4. System displays phone number editor with country code dropdown (consumes FR-026 country calling codes list)
5. Provider selects country code from worldwide list (e.g., +44 for UK)
6. Provider enters phone number (e.g., 7700 900123)
7. System validates phone number format for selected country code
8. Provider clicks "Save Phone Number"
9. System saves phone number in international format (+44 7700 900123)
10. Provider clicks "Change Timezone"
11. System displays timezone dropdown with multiple timezone options (GMT-12 to GMT+14)
12. Provider selects timezone (e.g., (GMT+0) London)
13. System saves timezone preference
14. Provider clicks "Change Password"
15. System displays password change form:
    - Current Password: [input field]
    - New Password: [input field]
    - Confirm New Password: [input field]
16. Provider enters current password and new password (following password policy from FR-026)
17. System validates:
    - Current password matches database
    - New password meets security policy (≥12 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char)
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

- **Trigger**: Provider relocates clinic to different timezone
- **Steps**:
  1. Provider selects new timezone from dropdown
  2. System saves timezone preference
  3. All future timestamps in provider dashboard display in new timezone
  4. Existing data timestamps remain in UTC but display converted to new timezone
- **Outcome**: Provider sees all dates/times in new local timezone

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
  4. System validates new password against FR-026 password policy
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
2. System validates user role = Owner (permission check per FR-009)
3. System displays billing settings form with existing bank account details (if previously saved):
   - Account Holder Name: [text field]
   - Bank Name: [text field]
   - Account Number: [masked, e.g., ●●●●●●1234]
   - Routing/SWIFT Code: [text field]
   - IBAN (if applicable): [text field]
4. Provider Owner clicks "Edit Bank Account Details"
5. System displays editable form with current values (account number unmasked)
6. Provider Owner updates bank account information:
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
  3. Provider Owner fills in all bank account fields
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
- **Outcome**: Non-owner cannot see or access billing settings (per FR-009 single-owner permissions)

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
9. System expands answer with detailed instructions
10. Provider reads answer
11. Provider clicks "Was this helpful?" feedback (Yes/No)
12. System records feedback for admin analytics
13. Provider navigates to "Tutorial Guides" category
14. System displays guide list (e.g., "How to Create Your First Quote", "Setting Up Notifications")
15. Provider clicks on guide "How to Create Your First Quote"
16. System displays step-by-step guide with screenshots
17. Provider reads guide
18. Provider returns to Help Centre home
19. Provider clicks "Contact Support"
20. System displays support contact form:
    - Subject: [text field]
    - Message: [textarea]
    - Attachment: [file upload - optional]
21. Provider fills form and submits support request
22. System sends support request to admin team
23. System displays confirmation "Support request submitted. Our team will respond within 24 hours."

### Alternative Flows

**A10: Provider Downloads Resource from Resource Library**:

- **Trigger**: Provider needs downloadable template or document
- **Steps**:
  1. Provider navigates to "Resource Library" category
  2. System displays list of downloadable resources (PDFs, templates, guides)
  3. Provider clicks "Download Quote Template"
  4. System initiates file download
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
  6. Provider clicks "Was this helpful?" feedback
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
  3. System displays overall platform status indicator (All Systems Operational, Partial Outage, Major Outage)
  4. System shows list of service components with current status and last updated time
  5. System displays recent incident history timeline and upcoming maintenance schedule (if any)
  6. Provider reviews status information to determine whether issue is platform-wide or local
  7. Provider optionally subscribes to status update notifications (if enabled per FR-020/notifications)
  8. Provider decides whether to wait, retry, or contact support (Contact Support flows above)
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
  5. System records feedback with reference to the viewed content item and provider account
  6. System forwards feedback to admin/content team via FR-034 (e.g., as a low-priority ticket or feedback case)
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
  7. System creates an issue/support case in FR-034 including file identifier, provider, and error details
  8. System confirms to provider that the issue has been reported
- **Outcome**: File loading problem is surfaced to admins/ops via FR-034 while provider receives clear feedback

---

### Main Flow: Request Account Deletion

**Actors**: Provider (any role), Admin, System
**Trigger**: Provider navigates to "Settings" → "Account Settings" → "Delete Account"
**Outcome**: Provider account deletion request submitted to admin for approval (soft-delete, not hard-delete)

**Steps**:

1. Provider navigates to Settings → Account Settings
2. Provider scrolls to bottom of page
3. Provider clicks "Delete Account" button (in red/warning color)
4. System displays account deletion warning dialog:
   - "Warning: Deleting your account will remove access to the Hairline platform."
   - "This action cannot be undone."
   - "All your quotes, bookings, and financial data will be archived."
   - "If you have active bookings or pending payments, please contact support before deleting your account."
   - [Checkbox] "I understand that this action is permanent and my account data will be archived."
   - Reason for deletion: [textarea] (optional)
5. Provider checks "I understand" checkbox
6. Provider enters reason for deletion (optional): "Closing clinic permanently"
7. Provider clicks "Submit Deletion Request"
8. System validates:
   - Provider has no active bookings (status = "Scheduled" or "Confirmed" or "In Progress")
   - Provider has no pending payouts
9. System creates account deletion request record with status "Pending Admin Approval"
10. System logs deletion request in audit trail (user, timestamp, reason)
11. System sends deletion request notification to admin team
12. System displays confirmation to provider "Account deletion request submitted. Our team will review and process your request within 5 business days. You will receive an email confirmation once your account is deleted."
13. Provider account remains active until admin approves deletion
14. Admin reviews deletion request in admin dashboard (A-XX: Provider Management)
15. Admin verifies provider has no active obligations
16. Admin approves deletion request
17. System performs soft-delete:
    - Provider account status changed to "Deleted"
    - Provider login disabled
    - Provider profile hidden from patient quote requests
    - All provider data retained in archive (per FR-023 data retention: minimum 7 years)
    - Bank account details encrypted and archived
18. System sends email confirmation to provider "Your account has been deleted. Your data has been archived per our data retention policy."

### Alternative Flows

**A13: Provider Cancels Deletion Request**:

- **Trigger**: Provider changes mind before submitting deletion request
- **Steps**:
  1. Provider clicks "Delete Account"
  2. System displays warning dialog
  3. Provider reads warning
  4. Provider clicks "Cancel" button
  5. System closes dialog without creating deletion request
- **Outcome**: Account deletion canceled, provider account remains active

**B13: Active Bookings Prevent Deletion**:

- **Trigger**: Provider has active bookings and attempts to delete account
- **Steps**:
  1. Provider clicks "Delete Account"
  2. Provider completes deletion form
  3. Provider clicks "Submit Deletion Request"
  4. System validates provider obligations
  5. System detects 3 active bookings (status = "Confirmed")
  6. System displays error "Cannot delete account. You have 3 active bookings. Please complete or cancel all bookings before deleting your account. For assistance, contact support at <support@hairlineapp.com>."
  7. Provider contacts support or waits for bookings to complete
- **Outcome**: Deletion request blocked until bookings completed

**B14: Pending Payouts Prevent Deletion**:

- **Trigger**: Provider has pending payouts and attempts to delete account
- **Steps**:
  1. Provider submits deletion request
  2. System validates financial status
  3. System detects pending payout of $2,500 scheduled for next week
  4. System displays error "Cannot delete account. You have pending payout of $2,500 scheduled for [date]. Please wait for payout to complete or contact support."
  5. Provider waits for payout or contacts support
- **Outcome**: Deletion request blocked until payout processed

---

## Screen Specifications

### Screen 1: Profile Management

**Purpose**: Allow provider to update clinic profile information visible to patients during quote comparison. This screen is organized as 6 tabs within the Provider Profile page (Settings & Support > Provider profile).

**Tab Structure**:

#### Tab 1: Basic Information

**Purpose**: Display and edit core clinic profile information including profile picture, name, rating, and contact details.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing |
|------------|------|----------|-------------|------------------|----------------|
| Profile Picture | image upload | No | Clinic branding image displayed in patient app | Max 5MB, JPEG/PNG only, min 200x200px, recommended 500x500px | **Inline Edit**: Click image area to open upload dialog with file picker; shows preview before save; crop/resize tool available; save/cancel buttons appear during edit |
| Cover Image | image upload | No | Large banner image for clinic profile | Max 10MB, JPEG/PNG only, recommended 1920x300px | **Inline Edit**: Click image area to open upload dialog with file picker; shows preview before save; crop/resize tool available; save/cancel buttons appear during edit |
| Clinic Name | text | Yes | Official clinic name | Max 200 chars, min 3 chars | **Inline Edit**: Click text to activate edit mode; field becomes editable input; save (✓) and cancel (✗) buttons appear; validation on blur; saves immediately on save button click |
| Review Rating | display | No | Average rating from patient reviews (read-only) | Display format: X.X/5.0 stars with total review count (e.g., "4.8/5.0 - Based on 127 reviews") | **Read-only**: Displays current average rating; clicking rating or "View all reviews" text navigates to Reviews tab (Tab 5) |
| Edit Profile Button | button | N/A | Quick access to edit mode for all fields in tab | N/A | **Toggle Action**: Clicking button toggles all editable fields in tab into edit mode simultaneously; button text changes to "Cancel Edit" when active; allows bulk editing of multiple fields |
| About/Description | textarea | Yes | Brief clinic description for patients | Max 500 chars, min 50 chars | **Inline Edit**: Click textarea to activate edit mode; expands to show full textarea with character counter (e.g., "245/500 characters"); save/cancel buttons appear; real-time validation; saves on save button click |
| Contact Phone (Public) | object | No | Public-facing clinic phone number shown in profile "About" section | Contains `Country Code` (dropdown, FR-026) and `Number` (text, numeric only, length validated per country code) | **Inline Edit**: Click to activate edit mode; field becomes object with dropdown for country code and input for number; auto-formats on blur (e.g., "+90 555 123 4567"); save/cancel buttons appear; saves on save button click |
| Contact Email | email | Yes | Clinic contact email shown on provider public profile and used for communications | Valid email format; must be unique if changed | **Inline Edit**: Click email to activate edit mode; field becomes editable input with email validation; shows validation error if invalid format; save/cancel buttons appear; saves on save button click |
| Location - City | text | No | City where clinic is located | Max 100 chars | **Inline Edit**: Click city name to activate edit mode; field becomes editable input; save/cancel buttons appear; saves on save button click |
| Location - Country | dropdown | No | Country where clinic is located | Values from centrally managed country list (FR-026); optional but recommended | **Inline Edit**: Click country name to activate edit mode; field becomes dropdown selector with search; shows country list from FR-026; save/cancel buttons appear; saves on save button click |
| Website URL | url | No | Public-facing clinic website shown in profile "About" section | Valid URL format (http/https); auto-prepends https:// if protocol missing | **Inline Edit**: Click URL to activate edit mode; field becomes editable input with URL validation; auto-formats on blur (adds https:// if missing); shows validation error if invalid; save/cancel buttons appear; saves on save button click |

**Business Rules**:

- Profile picture displayed in profile section; clicking opens upload dialog
- Cover image displayed as a banner on the top of the provider profile in patient app;
- If no logo uploaded, system displays clinic name initials as fallback
- Review rating displays average rating (e.g., "4.8/5.0") with total review count (e.g., "Based on 127 reviews"); clicking navigates to Reviews tab
- All fields support inline editing: clicking a field activates edit mode with save/cancel buttons
- Unsaved changes indicator (dot/asterisk) appears on tab label when edits are made
- Each field can be edited independently; changes saved per field or via "Save All" button
- Profile changes logged in audit trail with timestamp and user
- Profile updates propagate to patient app within 1 minute

**Notes**:

- **Profile Picture**: Image upload via file picker; shows preview after upload before saving; crop/resize functionality available to ensure proper aspect ratio; if no image uploaded, displays clinic name initials as fallback
- **Cover Image**: Image upload via file picker; shows preview after upload before saving; crop/resize functionality available to ensure proper aspect ratio;
- **Inline Editing Behavior**: Clicking any editable field highlights it with border/background change and shows save (✓) and cancel (✗) buttons; field becomes editable input/textarea/dropdown; validation occurs on blur or save; changes persist immediately on save button click; cancel button discards changes and reverts to original value
- **Character Counter**: About/Description field shows real-time character counter (e.g., "245/500 characters") with color change when approaching limit (yellow at 80%, red at 95%)
- **Bulk Edit Mode**: "Edit Profile" button toggles all editable fields in tab into edit mode simultaneously; button text changes to "Cancel Edit" when active; allows editing multiple fields before saving all at once via "Save All" button
- **Unsaved Changes**: Unsaved changes indicator (dot or asterisk) appears on tab label when any field has unsaved edits; indicator disappears when all changes saved
- **Field Validation**: Real-time validation feedback shown inline (e.g., red border for invalid email, green checkmark for valid); error messages appear below field when invalid

---

#### Tab 2: Languages

**Purpose**: Manage languages spoken at the clinic.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing |
|------------|------|----------|-------------|------------------|----------------|
| Supported Languages | chip/pill list | Yes | Languages spoken at clinic | At least 1 language required; consumes centrally managed language list from FR-026 | **Inline Edit**: Add language: click "+ Add Language" button to open dropdown with all available languages from FR-026; select language to add chip immediately; Remove language: click X icon on chip to remove (confirmation required if last language); Reorder: drag-and-drop chips to prioritize; changes save automatically or via "Save" button; unsaved changes indicator appears on tab label |

**Business Rules**:

- Languages displayed as removable chips/pills with X button on each chip
- Clicking "+ Add Language" opens dropdown with all available languages from FR-026
- Selected languages immediately appear as chips; removing a chip removes it from selection
- At least 1 language must be selected (validation prevents removing last language)
- Changes saved automatically when language added/removed, or via "Save" button
- Unsaved changes indicator appears on tab label when edits are made
- Language changes logged in audit trail

**Notes**:

- Each language chip displays language name (e.g., "English", "Turkish", "Spanish")
- Chips support drag-and-drop reordering to prioritize languages (most important first)
- Visual feedback: chip highlights on hover; removal requires confirmation if it's the last language
- Language list consumed from FR-026 (centrally managed with country list)

---

#### Tab 3: Staff List

**Purpose**: Manage clinic staff members and team roles.

**Implementation**: This tab displays **FR-009: Provider Team & Roles Management > Screen 1**.

See FR-009 Screen 1 for complete field specifications, business rules, and staff management functionality.

---

#### Tab 4: Awards

**Purpose**: Manage clinic awards, certifications, and recognitions.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing |
|------------|------|----------|-------------|------------------|----------------|
| Awards List | card/list | No | Clinic awards, certifications, recognitions | Each award: name (max 100 chars), issuer/organization (max 150 chars, optional), description (max 300 chars), year (1900-current year), award image (max 2MB, JPEG/PNG) | **Inline Edit**: Add award: click "+ Add Award" button to open award form (modal or inline expansion) with fields: name (text), issuer/organization (text, optional), description (textarea, max 300 chars), year (number dropdown 1900-current), image upload (drag-and-drop or file picker, max 2MB); Edit award: click "Edit" icon/button on award card to expand inline editor with all fields editable; Delete award: click "Delete" icon/button on award card, confirmation dialog appears; Reorder: drag-and-drop award cards to prioritize; each award saves independently or via "Save All" button; unsaved changes indicator appears on tab label |

**Business Rules**:

- Awards displayed as cards/rows with: award image thumbnail, name, issuer/organization, year, description snippet
- Clicking "Edit" on an award card opens inline editor (or modal) with all award fields editable
- Clicking "+ Add Award" opens award form (name, issuer/organization, description, year, image upload)
- Awards support drag-and-drop reordering to prioritize most important awards
- Award image upload supports drag-and-drop; max 2MB, JPEG/PNG only
- Changes saved per award (inline save) or via "Save All" button
- Unsaved changes indicator appears on tab label when edits are made
- Award changes logged in audit trail

**Notes**:

- Each award card displays: image thumbnail (or placeholder), award name (bold), issuer/organization, year, description (truncated with "Read more" if long)
- Inline editing: clicking "Edit" expands award card to show editable fields with save/cancel buttons
- Award image upload: click image area to upload/replace; supports drag-and-drop
- Awards list supports reordering via drag-and-drop handles
- Empty state: "No awards added yet. Click '+ Add Award' to showcase your achievements."

---

#### Tab 5: Reviews

**Purpose**: Browse all patient reviews with filtering and sorting capabilities (read-only).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing |
|------------|------|----------|-------------|------------------|----------------|
| Overall Rating Summary | display | No | Average rating and total review count (e.g., "4.8/5.0 - Based on 127 reviews") | Read-only; calculated from Reviews service | **Read-only**: Displays current average rating with star display and total review count; updates automatically when new reviews added |
| Rating Distribution | bar chart | No | Percentage/count visualization for 5★ through 1★ reviews | Read-only; calculated from Reviews service | **Read-only**: Bar chart showing distribution of ratings (e.g., 60% 5-star, 25% 4-star, etc.) with counts; updates automatically |
| Rating Filters | checkbox/pill group | No | Filter reviews by rating (5★, 4★, 3★, 2★, 1★); multiple selections allowed | Client-side filtering; selections persist per session | **Interactive**: Click rating pill/checkbox to toggle filter; multiple ratings can be selected; filtered results update immediately; filter state persists during session |
| Sort Dropdown | dropdown | No | Sort order options: "Most recent" (default), "Highest rated", "Lowest rated", "Oldest first" | Client-side sorting; selection persists per session | **Interactive**: Select from dropdown to change sort order; results update immediately; sort preference persists during session |
| Review Cards | list | No | List of review cards displaying: reviewer avatar/name, treatment type, rating stars, review date, review text (truncated), optional "Read more" link | Read-only content from Reviews service; pagination supported | **Read-only**: Review cards display review information; click "Read more" to expand full review text; click reviewer name/avatar (if implemented) may show reviewer profile; cards update automatically when new reviews added |
| Pagination Controls | control group | No | Page navigation: page numbers, next/previous buttons, page-size selector (10/20/50 per page) | Client-side pagination | **Interactive**: Click page numbers or next/previous to navigate; select page size from dropdown; pagination state persists during session |

**Business Rules**:

- Reviews data is read-only in FR-032; providers cannot edit/delete reviews
- Overall rating displays average (e.g., "4.8/5.0") with total count (e.g., "Based on 127 reviews")
- Rating distribution shows bar chart with counts/percentages for each star rating
- Filters and sort selections persist per user session
- Clicking a review notification (from notifications) opens this tab with relevant review auto-highlighted
- Data sourced from Reviews service; loading/empty/error states handled
- Reviews update automatically when new reviews are posted

**Notes**:

- Review cards display: reviewer avatar/name, treatment type, rating stars, review date, review text (truncated with "Read more")
- Filters and sort controls at top of reviews list
- Pagination controls: page numbers, next/previous, page-size selector (10/20/50 per page)
- Empty state: "No reviews yet. Reviews will appear here once patients leave feedback."
- Timestamp of last sync with Reviews service displayed at bottom

---

#### Tab 6: Documents

**Purpose**: Manage clinic documents including medical licenses, certifications, insurance, and other compliance documents. Providers can upload, replace, delete, and view their documents. Admins can also upload additional documents via FR-015 for oversight purposes.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Inline Editing |
|------------|------|----------|-------------|------------------|----------------|
| Upload Document Button | button | No | Primary action to upload new document | Opens upload modal | **Interactive**: Click to open "Upload Document" modal with fields: Document Type (dropdown), Document File (file picker), optional notes |
| Document List | list/cards | No | List of uploaded documents with metadata | Displays all provider and admin-uploaded documents | **Interactive**: Document cards in list/grid format; each card shows document name, type badge, upload date, file size, uploaded by (Provider/Admin), and action buttons (View, Replace, Delete) |
| Document Name | text (display/edit) | Yes | Filename of document | Auto-generated from uploaded file; max 200 chars; editable via "Rename" action | **Editable**: Click "Rename" icon/button on document card to edit filename; save on blur or Enter key |
| Document Type | dropdown | Yes | Document type selection | Options: "Medical License", "Board Certification", "Insurance", "Malpractice Insurance", "Business License", "Other" | **Editable**: Select from dropdown when uploading; can be changed via "Edit" action on document card |
| Document File | file upload | Yes | Upload document file | Accepted formats: PDF, JPG, PNG, DOCX, XLSX; Max 10MB per file | **Interactive**: Drag-and-drop or click to browse; file picker validates format/size before upload |
| Upload Date | date (display) | N/A | Date when document was uploaded | Timestamp format: "MMM DD, YYYY" (e.g., "Jan 15, 2025"); auto-generated | **Read-only**: Displays upload date with relative time on hover (e.g., "Uploaded 3 months ago") |
| Uploaded By | badge (display) | N/A | Who uploaded the document: "Provider" or "Admin" | Badge displays "You" for provider uploads, "Admin" for admin uploads | **Read-only**: Badge color: green for "You", blue for "Admin" |
| File Size | text (display) | N/A | Document file size | Format: "X.X MB" or "X KB"; auto-calculated | **Read-only**: Displays file size |
| Notes | text (optional) | No | Optional notes about document | Max 500 chars; editable | **Editable**: Click "Edit Notes" on document card to add/edit notes; save on blur or via Save button |
| View/Download Button | button | No | Action button to view or download document | Opens document in new browser tab or downloads file depending on file type | **Interactive**: Click to view PDF in browser or download file; button label: "View" for PDFs, "Download" for other file types |
| Replace Button | button | No | Action button to replace existing document with new version | Opens file picker to upload replacement | **Interactive**: Click "Replace" button on document card; file picker opens; validates format/size; on upload, old version archived (soft delete) and new version becomes active; confirmation toast: "Document replaced successfully" |
| Delete Button | button | No | Action button to delete document | Opens confirmation dialog; performs soft delete | **Interactive**: Click "Delete" button on document card; confirmation dialog: "Are you sure you want to delete [document name]? This action cannot be undone." On confirm, document soft-deleted; confirmation toast: "Document deleted successfully" |

**Business Rules**:

- **Provider Document Management**: Providers can upload, replace, delete, and view their own documents
- **Admin Oversight**: Admins can upload additional documents via FR-015 Tab 6 (e.g., documents received via email, external verifications). Admin-uploaded documents display "Admin" badge
- **Document Sync**: Documents uploaded by provider in FR-032 sync to FR-015 within 1 minute for admin visibility
- **Empty State**: If no documents uploaded yet, display message: "No documents on file. Upload your clinic documents (medical license, certifications, insurance) to get started." with prominent "Upload Document" button
- **Upload Modal Fields**:
  - Document Type: Dropdown (required) - "Medical License", "Board Certification", "Insurance", "Malpractice Insurance", "Business License", "Other"
  - Document File: File picker (required) - Accepted formats: PDF, JPG, PNG, DOCX, XLSX; Max 10MB
  - Notes: Text area (optional) - Max 500 chars; helpful for adding context (e.g., "License expires Dec 2026")
  - On submit: Document uploaded, confirmation toast: "Document uploaded successfully"
- **Replace Document**: Clicking "Replace" on a document card opens file picker; uploading new file replaces current version; old version archived (soft delete) with timestamp
- **Delete Document**: Clicking "Delete" opens confirmation dialog; on confirm, document soft-deleted (not permanently removed); admin can view deleted documents in FR-015 for audit purposes
- **Document Permissions**: Providers can only delete/replace documents they uploaded; Admin-uploaded documents display "View Only" (providers cannot delete/replace, but can download)
- **Audit Logging**: All document actions (upload/replace/delete/view/download) logged with timestamp, user, action type, and IP address (visible in FR-015 Tab 8: Activity Log)
- **Security**: Document URLs are secure, time-limited signed URLs; direct file access not allowed
- **File Validation**:
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
- Error state: If document fetch fails, display "Unable to load documents. Please refresh or contact support."
- Document cards display icon based on file type (PDF icon for PDFs, image icon for JPG/PNG, generic doc icon for DOCX/XLSX)
- Drag-and-drop upload: Providers can drag files directly onto the Documents tab to upload (opens upload modal with file pre-selected)

---

**General Business Rules (All Tabs)**:

- Each tab can be saved independently; system displays unsaved changes indicator (dot/asterisk) on tab label when edits are made
- When provider attempts to navigate away or quit, system displays reminder dialog "You have unsaved changes. Are you sure you want to leave?" with options to save, discard, or cancel
- All profile changes logged in audit trail with timestamp and user
- Profile updates propagate to patient app within 1 minute
- All profile fields are provider-editable from the provider dashboard (subject to role/permissions defined in FR-009 where applicable)
- Inline editing: clicking editable fields activates edit mode with save/cancel buttons; changes persist immediately on save
- **Tab Editability**:
  - **Fully Editable**: Tab 1 (Basic Information), Tab 2 (Languages), Tab 4 (Awards), Tab 6 (Documents) - providers can add, edit, delete content inline
  - **External Module**: Tab 3 (Staff List) - displays FR-009 Screen 1; see FR-009 for functionality
  - **Read-Only**: Tab 5 (Reviews) - completely read-only; managed by Reviews service, providers cannot edit/delete reviews

---

### Screen 2: Account Settings

**Purpose**: Allow provider to manage phone number, timezone, and password for account security and localization. This screen is organized as a tab within the Settings page (Settings & Support > Settings > Account Information tab).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Role-Based Behavior |
|------------|------|----------|-------------|------------------|-------------------|
| Account Name | text/display | Yes | Display name for the account | Max 200 chars | **Owner**: Unified with clinic name (read-only, synced from Tab 1: Basic Information); **Staff**: Editable display name (defaults to First Name + Last Name, can be customized) |
| First Name | text | Yes | User's first name | Max 50 chars, letters and spaces only | Editable by all roles (Owner and Staff) |
| Last Name | text | Yes | User's last name | Max 50 chars, letters and spaces only | Editable by all roles (Owner and Staff) |
| Account Email | email | Yes | Email address for login and communications | Valid email format, unique in system | Editable by all roles (Owner and Staff) |
| Phone Number - Country Code | dropdown | Yes (if phone provided) | Worldwide country calling code | Consumes FR-026 country calling codes list (e.g., +1, +44, +90, +234) | Editable by all roles |
| Phone Number - Number | text | No | Provider phone number | Numeric only, length validated per country code format | Editable by all roles |
| Timezone | dropdown | Yes | Provider's local timezone for date/time display | Multiple timezone options (GMT-12 to GMT+14) | Editable by all roles |
| Current Password | password | Yes (for password change) | Current password for verification | Must match existing password hash | Editable by all roles |
| New Password | password | Yes (for password change) | New password | Min 12 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char (!@#$%^&(),.?\":{}<>) per FR-026 | Editable by all roles |
| Confirm New Password | password | Yes (for password change) | Confirm new password | Must match New Password field | Editable by all roles |

**Business Rules**:

- **Account Name Unification (Owner Role)**:
  - For Owner accounts (main account holder/provider admin): Account Name is unified with the clinic name from Tab 1: Basic Information (clinic name field)
  - Account Name field is read-only for Owner role; it automatically syncs when clinic name is updated in Tab 1
  - If Owner updates clinic name in Tab 1, Account Name in Tab 2 updates automatically (within 1 minute)
  - Account Name displays clinic name with read-only indicator (e.g., "Istanbul Hair Clinic" with lock icon or "Synced with clinic name" helper text)
  - Rationale: Owner account represents the clinic organization, so account name should match clinic name for consistency across the platform
  
- **Account Name (Staff Roles)**:
  - For Staff roles (Manager, Clinical Staff, Billing Staff): Account Name is editable and independent from clinic name
  - Default Account Name for staff is "First Name + Last Name" (e.g., "John Smith")
  - Staff can customize Account Name to any display name (e.g., "Dr. John Smith", "John S.", "J. Smith")
  - Account Name for staff is used for display purposes in dashboard, notifications, activity logs, and team member listings
  - Staff Account Name changes do not affect clinic name or other staff members' account names
  - Rationale: Staff are individual team members, not the clinic itself, so they should have personalized display names
  
- Phone number country code and number stored together in international format (e.g., +44 7700 900123)
- Timezone preference applies to all date/time displays in provider dashboard
- Existing timestamps in database remain in UTC, converted to provider's timezone for display
- Password change requires correct current password (security measure)
- New password must meet password policy from FR-026 (FIXED in codebase, not admin-editable)
- Password change event logged in audit trail (timestamp, user ID, IP address)
- Email notification sent to provider email address after successful password change (security alert)
- All account-level fields (account name, first name, last name, account email, phone number, timezone, password) are provider-editable by the logged-in user, subject to role-based restrictions (Account Name read-only for Owner) and FR-026 security rules and FR-009 role permissions

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
- Include a dedicated **Delete Account** warning card at the bottom of the Account Information tab with explanatory copy and a red `Delete account` button; clicking the button opens the Account Deletion dialog described in the "Request Account Deletion" flow, where the reason textarea remains provider-editable while approval status stays admin-controlled
- Account Settings shares the Settings page with Notification Preferences as a two-tab interface; the `Account Information` tab (this screen) is the default tab when landing on Settings
- Each tab can be saved independently; system displays unsaved changes indicator on tabs with edits
- When provider attempts to navigate away or quit, system displays reminder dialog for unsaved changes

---

### Screen 3: Notification Preferences

**Purpose**: Allow provider to configure unified notification preferences (individual notification types + global channel preferences). This screen is organized as a tab within the Settings page (Settings & Support > Settings > Notification Preferences tab).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Notifications | toggle/checkbox | No (default enabled) | New inquiry received, quote expiring soon | Toggle on/off |
| Schedule Notifications | toggle/checkbox | No (default enabled) | Appointment confirmed, appointment reminder | Toggle on/off |
| Treatment Start Notifications | toggle/checkbox | No (default enabled) | Patient checked in, procedure started | Toggle on/off |
| Aftercare Notifications | toggle/checkbox | No (default enabled) | Patient milestone completed, urgent aftercare alert | Toggle on/off |
| Review Notifications | toggle/checkbox | No (default enabled) | New review posted, review requires response | Toggle on/off |
| Promotion/Discount Notifications | toggle/checkbox | No (default enabled) | New platform discounts created by admin that require provider acceptance/opt-in | Toggle on/off |
| Email Notifications | toggle/checkbox | No (default enabled) | Send notifications via email | Toggle on/off, email address from profile |
| Push/In-App Notifications | toggle/checkbox | No (default enabled) | Show notifications in web portal | Toggle on/off |

**Business Rules**:

- Notification preferences are profile-specific (apply to entire provider organization, not individual team members)
- If all notification types disabled, show confirmation dialog warning provider may miss important updates
- Notification preferences saved and enforced by S-03 Notification Service (FR-020)
- Global channel preferences override individual notification types (e.g., if Email disabled, no notifications sent via email regardless of individual toggles)
- Each tab (Profile, Account Information, Notification Preferences, Billing) can be saved independently; system displays unsaved changes indicator (e.g., dot or asterisk) on tabs with unsaved edits
- When provider attempts to navigate away or quit, system displays reminder dialog "You have unsaved changes. Are you sure you want to leave?" with options to save, discard, or cancel
- Critical system alerts (e.g., payment failure, security breach) bypass preferences and always sent via all available channels
- Preference changes logged in audit trail
- Preference updates propagate to S-03 within 1 minute
- All notification type and channel toggles are provider-editable from the `Settings → Notification Preferences` tab in the provider dashboard

**Notes**:

- Display notification types in collapsible sections with examples (expand to show what notifications are included)
- Provide "Enable All" / "Disable All" quick action buttons
- Show real-time preview of notification channels (e.g., "You will receive Quote Notifications via Email and Push")
- Display last preference update timestamp
- Provide "Test Notification" button to send sample notification and verify settings work
- Notification Preferences appears as the second tab on the Settings page beside Account Information; toggling between tabs should maintain unsaved changes warning if applicable
- Each tab has its own "Save" button; unsaved changes indicator appears on tab label when edits are made

---

### Screen 4: Billing Settings (Owner Role Only)

**Purpose**: Allow provider Owner to manage bank account details for receiving payouts from Hairline platform. This screen is organized as a tab within the Settings page (Settings & Support > Settings > Billing tab). Non-owner roles cannot see or access this tab.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Account Holder Name | text | Yes | Full name or business name on bank account | Max 200 chars, alphabetic and spaces only |
| Bank Name | text | Yes | Official name of bank | Max 200 chars |
| Account Number | text | Yes | Bank account number | Format varies by country, validated by S-02 Payment Service |
| Routing/SWIFT Code | text | Yes | Bank routing code (USA) or SWIFT code (international) | 8-11 chars for SWIFT, 9 digits for USA routing |
| IBAN | text | Conditional (if applicable) | International Bank Account Number | Format validated per country (e.g., Turkey = 26 chars) |

**Business Rules**:

- Billing settings accessible ONLY to Owner role (per FR-009 role permissions)
- Non-owner roles cannot see or access billing settings (tab hidden from navigation)
- Account number masked in read-only view (e.g., ●●●●●●1234), unmasked in edit mode
- Bank account details encrypted at rest using AES-256
- Bank account information validated by S-02 Payment Service before saving
- Bank account changes logged in audit trail (Owner user, timestamp, action)
- Email confirmation sent to Owner after bank account details updated
- Bank account details used by FR-017 billing workflow for provider payouts
- If bank account validation fails, display error message from S-02 and prevent saving

**Notes**:

- Provide country selector to determine required fields (e.g., IBAN required for EU, routing number required for USA)
- Show bank account format examples based on selected country
- Provide "Verify Bank Account" button to test bank account details with S-02 before saving
- Display last bank account update timestamp
- Show next scheduled payout date and amount (if available)
- Provide link to payout history (handled by PR-05: Financial Management & Reporting)

---

### Screen 5: Help Centre

**Purpose**: Provide provider access to help resources, FAQs, guides, and contact support (content managed by admin via FR-033). Help Centre is organized as a main landing page with subscreens for each content type, each with distinct layouts optimized for their content format.

**Entry Point**: Provider navigates to "Help Centre" from settings menu or footer link

**Main Landing Page**:

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search Bar | text | No | Global search across all Help Centre content | Max 200 chars, autocomplete suggestions |
| Category Navigation | navigation menu | No | Links to subscreens: FAQs, Tutorial Guides, Troubleshooting Tips, Policy Information, Resource Library, Video Tutorials, Contact Support, Feedback & Suggestions, Service Status | N/A |
| Most Popular Articles | card list | No | Top 5 most viewed/helpful articles across all categories | Read-only, sorted by view count/helpfulness |
| Recently Updated | card list | No | Latest 5 updated articles across all categories | Read-only, sorted by update date |

**Business Rules**:

- All Help Centre content is read-only for providers (content managed exclusively by admins via FR-033)
- Search functionality searches across all content types (FAQs, articles, resources, videos)
- Help Centre content updates (from admin) propagate to providers within 1 minute
- Breadcrumb navigation available on all subscreens for easy return to home

---

#### Screen 5.1: FAQs

**Purpose**: Display frequently asked questions organized by topic with expandable/collapsible layout

**Layout Type**: Distinct FAQ layout (accordion/expandable sections)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| FAQ Topic Filter | category filter | No | Filter FAQs by topic (e.g., "Quote Management", "Payment Settings", "Aftercare") | Pre-defined topics from admin |
| FAQ Questions | accordion list | No | List of FAQ items with question and expandable answer | Each FAQ: question (text), answer (rich text/HTML), topic category, helpfulness rating |
| "Was this helpful?" Feedback | button group | No | Yes/No buttons for each FAQ | Records feedback for admin analytics |

**Business Rules**:

- FAQs organized by topic with expandable/collapsible accordion sections
- Clicking question expands to show answer; clicking again collapses
- Multiple FAQs can be expanded simultaneously
- Topic filter updates list instantly (client-side filtering)
- Feedback (Yes/No) recorded per FAQ for admin analytics
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

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Article Title | display | No | Title of tutorial guide/tip/policy | Read-only |
| Article Content | rich text/HTML | No | Formatted article content with headings, lists, images, screenshots | Read-only, supports HTML formatting |
| Article Metadata | display | No | Publication date, last updated date, author (admin), category | Read-only |
| Table of Contents | navigation | No | Auto-generated from article headings (for long articles) | Read-only, clickable anchor links |
| Related Articles | card list | No | Related articles from same or other categories | Read-only, links to other articles |
| "Was this helpful?" Feedback | button group | No | Yes/No buttons | Records feedback for admin analytics |

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
- Share article functionality (copy link, email link)

---

#### Screen 5.3: Resource Library

**Purpose**: Display downloadable resources (templates, documents, PDFs) in file viewer layout

**Layout Type**: File viewer/download interface

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Resource List | card/grid | No | List of downloadable resources with thumbnails/icons | Each resource: name, description, file type, file size, download count, last updated |
| Resource Category Filter | filter | No | Filter by resource type (Templates, Documents, Forms, etc.) | Pre-defined categories from admin |
| File Type Filter | filter | No | Filter by file format (PDF, DOCX, XLSX, etc.) | Pre-defined file types |
| Preview Button | button | No | Preview resource before download (if supported format) | Opens preview modal or new tab |
| Download Button | button | No | Download resource file | Initiates file download |

**Business Rules**:

- Resources displayed as cards/grid with file type icons and metadata
- Clicking resource card shows details: description, file size, download count, last updated date
- Preview available for PDF and image files (opens in modal or new tab)
- Download initiates file download; download count incremented
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

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Video List | card/grid | No | List of video tutorials with thumbnails | Each video: title, description, duration, thumbnail, view count, publish date |
| Video Player | embedded player | No | Video player with play controls | Supports play, pause, volume, fullscreen, playback speed |
| Video Transcript | expandable section | No | Text transcript of video (if available) | Read-only, expandable/collapsible |
| Related Videos | card list | No | Related video tutorials | Read-only, links to other videos |
| "Was this helpful?" Feedback | button group | No | Yes/No buttons | Records feedback for admin analytics |

**Business Rules**:

- Videos embedded with standard video player controls (play, pause, volume, fullscreen, playback speed)
- Video thumbnails displayed in grid/list view
- Clicking video card opens video player (inline or modal)
- Video transcripts available (if provided by admin) in expandable section below player
- View count incremented when video plays for >30 seconds
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

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Support Request Form - Subject | text | Yes | Support request subject line | Max 200 chars |
| Support Request Form - Category | dropdown | No | Request category (Technical Issue, Billing Question, Feature Request, etc.) | Pre-defined categories |
| Support Request Form - Message | textarea | Yes | Detailed support request message | Max 2000 chars, min 20 chars |
| Support Request Form - Priority | dropdown | No | Request priority (Low, Medium, High, Urgent) | Default: Medium |
| Support Request Form - Attachment | file upload | No | Optional screenshot or document | Max 10MB, common file types (PDF, PNG, JPG, DOCX) |
| Submission Tracking | list | No | List of submitted support requests with status | Each request: subject, category, status (Open, In Progress, Resolved, Closed), submitted date, last updated, ticket number |

**Business Rules**:

- Support contact form auto-populates provider contact information (name, email, clinic name)
- Form submission creates support ticket with unique ticket number
- Support request confirmation displayed: "Support request submitted. Ticket #[number]. Our team will respond within 24 hours."
- Form submissions automatically create support cases in FR-034 Support Center & Ticketing System with status 'Open'; case management, admin responses, and status updates are handled in FR-034
- Submission tracking shows all user's support requests with status updates
- Status updates: Open → In Progress → Resolved → Closed
- Provider can view request details and add follow-up messages (if implemented)
- Email notification sent to provider when admin responds or updates status

**Notes**:

- Form layout: fields stacked vertically with clear labels and validation
- File upload: drag-and-drop or file picker, shows upload progress
- Submission tracking: table/list view with status badges, sortable by date/status
- Ticket details: expandable view showing full conversation thread (if multi-message support implemented)
- Estimated response time displayed: "Average response time: 24 hours"

---

#### Screen 5.6: Feedback & Suggestions

**Purpose**: Submit feedback and feature requests with submission tracking

**Layout Type**: Form interface with submission tracking

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Feedback Form - Type | dropdown | Yes | Feedback type (Feature Request, Bug Report, Suggestion, Other) | Pre-defined types |
| Feedback Form - Title | text | Yes | Brief title for feedback | Max 100 chars |
| Feedback Form - Description | textarea | Yes | Detailed feedback description | Max 2000 chars, min 20 chars |
| Feedback Form - Priority | dropdown | No | Suggested priority (Low, Medium, High) | Default: Low |
| Submission Tracking | list | No | List of submitted feedback with status | Each submission: title, type, status (Open, In Progress, Resolved, Closed), feedback resolution (if applicable: Implemented, Planned, Declined), submitted date, admin response |

**Business Rules**:

- Feedback form allows providers to submit feature requests, bug reports, and suggestions
- Form submission creates feedback record with unique ID
- Confirmation displayed: "Thank you for your feedback! We'll review your submission."
- Form submissions automatically create feedback cases in FR-034 Support Center & Ticketing System with status 'Open'; case tracking, admin responses, and resolution status are handled in FR-034
- Submission tracking shows all user's feedback submissions with status
- Status updates follow unified workflow: Open → In Progress → Resolved → Closed (feedback resolution outcome—Implemented, Planned, Declined—tracked separately in FR-034)
- Admin can respond to feedback (if implemented); response visible in tracking list
- Feedback helps prioritize platform improvements

**Notes**:

- Form layout: similar to Contact Support form
- Feedback type selector determines form fields (e.g., Bug Report may include "Steps to Reproduce")
- Submission tracking: table/list view with status badges
- Status badges: color-coded (Open: blue, In Progress: yellow, Resolved: green, Closed: gray)
- Feedback resolution badges (when applicable): color-coded (Implemented: green, Planned: yellow, Declined: red, Under Review: blue)
- Admin response visible in expanded feedback details view

---

#### Screen 5.7: Service Status

**Purpose**: Display platform service status and incident reports

**Layout Type**: Status page interface

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Overall Status Indicator | badge | No | Current platform status (All Systems Operational, Partial Outage, Major Outage) | Color-coded: green/yellow/red |
| Service Components Status | list | No | Status of individual services/components | Each component: name, status (Operational, Degraded, Down), last updated |
| Incident History | timeline | No | Recent incidents and maintenance windows | Each incident: title, description, status (Investigating, Identified, Monitoring, Resolved), start time, end time, affected services |
| Maintenance Schedule | list | No | Upcoming scheduled maintenance | Each maintenance: title, description, scheduled start/end time, affected services |

**Business Rules**:

- Service status page displays real-time platform health
- Overall status: "All Systems Operational" (green), "Partial Outage" (yellow), "Major Outage" (red)
- Individual service components show status: Operational (green), Degraded (yellow), Down (red)
- Incident history shows recent incidents with timeline and resolution details
- Maintenance schedule shows upcoming planned maintenance windows
- Status updates automatically when admin updates status via admin platform
- Providers can subscribe to status updates (email notifications for incidents)

**Notes**:

- Status page layout: dashboard-style with status indicators and timeline
- Overall status badge: large, prominent, color-coded
- Service components: grid/list with status badges and last updated timestamps
- Incident timeline: chronological list with expandable details
- Maintenance schedule: calendar view or list view with countdown timers
- Subscribe button: "Get email notifications for service incidents"

---

## Business Rules

### General Module Rules

- **Rule 1**: All provider profile changes (logo, name, description, languages, awards) propagate to patient-facing quote comparison view within 1 minute
- **Rule 2**: Provider notification preferences enforced by S-03 Notification Service for all platform notifications (except critical system alerts which bypass preferences)
- **Rule 3**: All account settings changes (phone, timezone, password) logged in audit trail with timestamp, user ID, and IP address
- **Rule 4**: Billing settings accessible ONLY to Owner role; non-owner roles cannot see or access billing settings (tab hidden from navigation)
- **Rule 5**: All profile, language, awards, account, and notification fields documented in this FR are provider-editable within the Provider Dashboard (subject to role restrictions noted); conversely, reviews content, staff roster, and Help Centre articles remain read-only views fed by their respective modules

### Data & Privacy Rules

- **Privacy Rule 1**: Bank account details encrypted at rest using AES-256 and masked in UI (e.g., ●●●●●●1234)
- **Privacy Rule 2**: Password stored as bcrypt hash (cost factor 12+), never stored in plain text
- **Privacy Rule 3**: Account deletion requests result in soft-delete (account status = "Deleted", data archived per FR-023 data retention: minimum 7 years)
- **Audit Rule**: All profile changes, account settings changes, billing settings changes, and account deletion requests logged in audit trail with: timestamp, user ID, IP address, action, old value, new value
- **GDPR Compliance**: Provider account deletion request allows provider to exercise "right to erasure" (soft-delete with data archival, not permanent deletion)
- **Unsaved Changes Rule**: System displays unsaved changes indicator (e.g., dot or asterisk) on tabs with unsaved edits; when provider attempts to navigate away or quit, system displays reminder dialog "You have unsaved changes. Are you sure you want to leave?" with options to save, discard, or cancel

### Admin Editability Rules

**Editable by Admin (via A-09: System Settings & Configuration and FR-033: Help Centre Content Management)**:

- Help Centre content (FAQs, tutorial guides, troubleshooting tips, resource library, video tutorials, policy information)
- System language options available in profile language selection (centrally managed with country list in FR-026)
- Country calling codes available in phone number selection (FR-026)
- Timezone options available in account settings (FR-026)
- Password policy parameters (configurable: max login attempts, lockout duration, OTP expiry, resend cooldown; FIXED in codebase: password complexity rules) (FR-026)

**Fixed in Codebase (Not Editable)**:

- Password policy complexity requirements: min 12 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char (!@#$%^&(),.?\":{}|<>) (FR-026)
- Encryption algorithms: AES-256 for data at rest, TLS 1.3 for data in transit
- Role-based access control rules: billing settings accessible only to Owner role (FR-009)
- Password hash algorithm: bcrypt with cost factor 12+
- Account deletion workflow: soft-delete only, data retained per FR-023 (minimum 7 years)

**Configurable with Restrictions**:

- Notification preference options: admins can add/remove notification types via system configuration, but core notification types (quote, schedule, treatment, aftercare, review) are required
- Bank account validation rules: S-02 Payment Service validates bank account format per country, admin cannot modify validation logic

### Payment & Billing Rules

- **Billing Rule 1**: Bank account details validated by S-02 Payment Service before saving (format validation only, no funds verification)
- **Billing Rule 2**: Bank account details used by FR-017 billing workflow for provider payouts (admin-triggered after treatment completion)
- **Billing Rule 3**: Bank account changes require Owner role; non-owner roles cannot see or access billing settings (tab hidden from navigation)
- **Billing Rule 4**: Bank account details encrypted at rest and masked in UI (only last 4 digits visible in read-only view)

---

## Success Criteria

### Provider Experience Metrics

- **SC-001**: Providers can complete profile setup (logo, description, languages, awards) in under 5 minutes
- **SC-002**: 90% of providers successfully update profile information on first attempt without errors
- **SC-003**: Providers can configure notification preferences in under 2 minutes

### Provider Efficiency Metrics

- **SC-004**: Providers can change account settings (phone, timezone, password) in under 3 minutes
- **SC-005**: Provider support requests submitted via Help Centre receive first response within 24 hours for 95% of requests
- **SC-006**: 70% of provider questions resolved via Help Centre self-service (without contacting support)

### Admin Management Metrics

- **SC-007**: Admins can manage Help Centre content for all categories (FAQs, guides, videos, resources)
- **SC-008**: Help Centre content updates propagate to provider platform within 1 minute
- **SC-009**: 100% of provider profile changes, account settings changes, and billing settings changes logged in audit trail

### System Performance Metrics

- **SC-010**: Profile updates (logo, description, awards) save and display within 2 seconds for 95% of requests
- **SC-011**: Notification preference changes propagate to S-03 Notification Service within 1 minute
- **SC-012**: System supports 1000 concurrent provider settings updates without degradation
- **SC-013**: Bank account validation via S-02 Payment Service completes within 3 seconds for 95% of requests

### Business Impact Metrics

- **SC-014**: Provider profile completion rate increases to 85% (all sections completed: logo, description, languages, awards, phone, billing)
- **SC-015**: Support ticket volume related to settings/profile issues reduced by 40% (due to Help Centre self-service)
- **SC-016**: Provider satisfaction score for settings management improves to 4.5+ out of 5

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-020 / S-03: Notification Service**: Notification preferences integration
  - **Why needed**: Provider notification preferences must be enforced when S-03 sends notifications (quote alerts, schedule reminders, review notifications)
  - **Integration point**: When provider saves notification preferences, system updates S-03 preference rules; S-03 checks preferences before sending each notification

- **FR-026 / A-09: App Settings & Security Policies**: Language options for profile (centrally managed with country list)
  - **Why needed**: Profile language selection must display available system languages
  - **Integration point**: Profile language dropdown consumes centrally managed language list from FR-026 system configuration (same as country list management)

- **FR-026 / A-09: App Settings & Security Policies**: Country codes, timezone options, password policy
  - **Why needed**: Account settings require worldwide country calling codes, timezone list, and password validation rules
  - **Integration point**: Phone number country code dropdown consumes FR-026 country list; timezone dropdown consumes FR-026 timezone list; password change validates against FR-026 password policy

- **FR-009 / PR-01: Provider Team & Role Management**: Role-based access control for billing settings
  - **Why needed**: Billing settings must be accessible ONLY to Owner role per FR-009 role permissions
  - **Integration point**: System validates user role before allowing access to billing settings; non-owner roles denied access

- **FR-017 / A-05: Admin Billing & Financial Management**: Bank account details for payouts
  - **Why needed**: Bank account details saved in billing settings used by FR-017 for provider payouts
  - **Integration point**: When admin triggers provider payout (FR-017), system retrieves bank account details from billing settings

- **FR-033 / A-09: Help Centre Content Management**: Help Centre content
  - **Why needed**: Help Centre displays admin-managed content (FAQs, guides, videos, resources)
  - **Integration point**: Help Centre reads content from admin-managed content database; content updates from admin propagate to provider Help Centre view

- **FR-034 / A-10: Support Center & Ticketing**: Provider support request and feedback submission management
  - **Why needed**: Provider submissions via Screen 5.5 (Contact Support) and Screen 5.6 (Feedback & Suggestions) automatically create support cases in FR-034 ticketing system
  - **Integration point**: Form submissions create support cases with provider ID linked; providers view submission status and admin responses through FR-032 UI querying FR-034 data

### External Dependencies (APIs, Services)

- **S-02 Payment Processing Service**: Bank account validation
  - **Purpose**: Validates bank account details format before saving in billing settings
  - **Integration**: RESTful API call to S-02 with bank account details (account number, SWIFT/routing code, IBAN)
  - **Failure handling**: If S-02 validation fails, display error message to provider and prevent saving; provider must correct bank details and retry

- **S-03 Notification Service**: Notification preference enforcement
  - **Purpose**: Enforces provider notification preferences when sending notifications
  - **Integration**: System updates S-03 preference database when provider saves notification preferences; S-03 queries preferences before sending each notification
  - **Failure handling**: If S-03 unavailable during preference save, queue preference update for retry; provider sees success message but preferences may take up to 5 minutes to propagate

### Data Dependencies

- **Entity 1: Provider Profile Data (from PR-01: Auth & Team Management)**: Provider account information
  - **Why needed**: Settings module requires existing provider account with clinic name, email, and role information
  - **Source**: Provider onboarding module (A-02: Provider Management & Onboarding creates provider account; PR-01 manages team members)

- **Entity 2: System Configuration Data (from A-09: System Settings & Configuration / FR-026)**: Language list (centrally managed with country list), country codes, timezone list, password policy
  - **Why needed**: Account settings and profile require system-wide configuration data
  - **Source**: FR-026 provides centrally managed language and country lists consumed by settings module

- **Entity 3: Help Centre Content (from FR-033: Help Centre Content Management)**: FAQs, guides, videos, resources
  - **Why needed**: Help Centre displays admin-managed content
  - **Source**: A-09 (admins create and manage Help Centre content via FR-033)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Providers will complete profile setup (logo, description, awards) within first 7 days of account activation to maximize patient quote requests
- **Assumption 2**: Providers will enable at least email notifications (most providers prefer email over push)
- **Assumption 3**: Provider Owners will add bank account details before completing first treatment (required for receiving payouts)
- **Assumption 4**: Providers will use Help Centre for common questions before contacting support (self-service first)

### Technology Assumptions

- **Assumption 1**: Providers access web platform via modern browsers (Chrome, Safari, Firefox, Edge - last 2 versions) per NFR-006
- **Assumption 2**: Providers have stable internet connection for image uploads (logo, awards)
- **Assumption 3**: Providers have access to bank account information (account number, SWIFT/routing code) when setting up billing
- **Assumption 4**: Help Centre content (videos, documents) delivered via CDN for fast loading

### Business Process Assumptions

- **Assumption 1**: Admins update Help Centre content at least monthly to keep resources current and relevant
- **Assumption 2**: Admins review and approve provider account deletion requests within 5 business days
- **Assumption 3**: Provider profile updates (logo, awards) reviewed by admin for quality assurance (future enhancement, not MVP)
- **Assumption 4**: Bank account details remain valid for at least 12 months; providers responsible for updating if bank account changes

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Settings module requires real-time synchronization with S-03 Notification Service for preference enforcement; use message queue for asynchronous preference updates to prevent blocking
- **Technology**: Image uploads (logo, awards) should use resumable upload protocol to handle network interruptions during large file uploads
- **Performance**: Profile updates should use optimistic UI updates (display success immediately, synchronize with backend asynchronously) to improve perceived performance
- **Storage**: Bank account details encrypted at rest using AES-256; encryption keys managed via secure key management service (e.g., AWS KMS, Google Cloud KMS)

### Integration Points

- **Integration 1**: Provider Settings → S-03 Notification Service (notification preference enforcement)
  - **Data format**: JSON payload with provider ID, notification type toggles (quote, schedule, treatment, aftercare, review), channel preferences (email, push)
  - **Authentication**: OAuth 2.0 bearer token (service-to-service)
  - **Error handling**: Retry with exponential backoff on 5xx errors; if S-03 unavailable for >5 minutes, log error and notify admin

- **Integration 2**: Billing Settings → S-02 Payment Service (bank account validation)
  - **Data format**: JSON payload with account holder name, bank name, account number, SWIFT/routing code, IBAN, country code
  - **Authentication**: OAuth 2.0 bearer token (service-to-service)
  - **Error handling**: Display S-02 validation error message to provider; prevent saving until validation succeeds

- **Integration 3**: Help Centre → Admin Content Database (read-only content display)
  - **Data format**: JSON API response with Help Centre content (categories, articles, FAQs, videos, resources)
  - **Authentication**: Internal API (user authentication required, RBAC enforced per FR-009 as this is an authenticated provider area)
  - **Error handling**: If content unavailable, display cached version with "Content may be outdated" warning; retry after 1 minute

### Scalability Considerations

- **Current scale**: Expected 100-200 providers updating settings daily at launch
- **Growth projection**: Plan for 1,000 providers updating settings daily within 12 months
- **Peak load**: Handle 10x normal load during onboarding campaigns (1,000 concurrent profile updates)
- **Data volume**: Expect 500KB average per provider profile (logo, awards, settings); total ~50MB for 100 providers, ~500MB for 1,000 providers
- **Scaling strategy**: Horizontal scaling of API servers; CDN for image delivery (logos, awards); database read replicas for Help Centre content

### Security Considerations

- **Authentication**: Multi-factor authentication (MFA) required for Owner role when accessing billing settings (future enhancement)
- **Authorization**: Role-based access control (RBAC) enforced for billing settings (Owner role only); API endpoints validate user role before allowing access
- **Encryption**: All provider data encrypted in transit (TLS 1.3) and at rest (AES-256); bank account details use field-level encryption with separate encryption keys
- **Audit trail**: Log all settings changes (profile, account, notifications, billing) with timestamp, user ID, IP address, action, old value, new value
- **Threat mitigation**: Rate limiting on password change endpoint (max 5 attempts/hour/user) to prevent brute force attacks; rate limiting on image upload endpoint (max 10 uploads/hour/user) to prevent abuse
- **Compliance**: GDPR-compliant account deletion (soft-delete with data archival); PCI-DSS compliance for bank account data handling (no card data stored, only bank account details for payouts)

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
2. **Given** provider disables all notification types, **When** provider clicks "Save Preferences", **Then** system displays confirmation dialog "Warning: You have disabled all notifications. You may miss important updates about inquiries, appointments, and reviews. Are you sure?", requires provider confirmation, and if confirmed, saves "all disabled" preference and S-03 stops sending notifications (except critical system alerts)

---

### User Story 3 - Update Account Settings (Phone, Timezone, Password) (Priority: P1)

A provider updates their phone number, changes timezone to match clinic location after relocation, and changes password for security.

**Why this priority**: Account settings ensure provider security and localization. Timezone accuracy ensures providers don't miss appointment times due to timezone confusion.

**Independent Test**: Can be fully tested by updating phone number, timezone, and password in account settings, verifying changes saved correctly, and confirming password change email sent.

**Acceptance Scenarios**:

1. **Given** provider has phone number +90 555 123 4567 (Turkey) and timezone (GMT+3) Istanbul, **When** provider navigates to Account Settings, changes country code to +44 (UK), enters phone number 7700 900123, changes timezone to (GMT+0) London, saves settings, **Then** system validates phone number format for UK, saves phone number in international format (+44 7700 900123), saves timezone preference, displays success message, and all future dashboard timestamps display in London timezone
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
3. **Given** provider has Admin role (not Owner), **When** provider Admin navigates to Settings & Support > Settings, **Then** system validates user role, detects role ≠ Owner, and hides the Billing tab from navigation (non-owner cannot see or access billing settings)

---

### User Story 5 - Access Help Centre Resources (Priority: P2)

A provider searches Help Centre for answer to question "How do I edit a quote after submission?" and finds answer in FAQ without contacting support.

**Why this priority**: Help Centre self-service reduces support ticket volume by 40% and improves provider satisfaction. 70% of provider questions resolved via Help Centre without support contact.

**Independent Test**: Can be fully tested by accessing Help Centre, searching for FAQ, reading answer, submitting feedback, and verifying support request form works.

**Acceptance Scenarios**:

1. **Given** provider has question about editing quotes, **When** provider navigates to Help Centre, clicks "FAQs" category, selects topic "Quote Management", clicks question "How do I edit a quote after submission?", **Then** system expands answer with detailed instructions, provider reads answer, clicks "Was this helpful? Yes", system records feedback for admin analytics
2. **Given** provider needs to contact support, **When** provider navigates to Help Centre, clicks "Contact Support", fills support form (Subject: "Payment issue", Message: "I haven't received my payout for last week", uploads screenshot 2MB PNG), submits request, **Then** system validates form, sends support request to admin team, displays confirmation "Support request submitted. Our team will respond within 24 hours.", and admin receives support request in admin dashboard
3. **Given** provider wants to download quote template, **When** provider navigates to Help Centre, clicks "Resource Library", clicks "Download Quote Template" (PDF file), **Then** system initiates file download, provider saves file to local device

---

### User Story 6 - Request Account Deletion (Priority: P2)

A provider closing their clinic permanently requests account deletion, and admin reviews and approves deletion request.

**Why this priority**: Account deletion allows provider to exercise GDPR "right to erasure" and ensures platform doesn't retain inactive accounts. Account deletion implemented as soft-delete with data archival per FR-023 compliance requirements.

**Independent Test**: Can be fully tested by submitting account deletion request as provider, verifying admin receives request, admin approves deletion, provider account soft-deleted, and provider data archived.

**Acceptance Scenarios**:

1. **Given** provider is closing clinic permanently, **When** provider navigates to Settings → Account Settings, clicks "Delete Account", checks "I understand" checkbox, enters reason "Closing clinic permanently", clicks "Submit Deletion Request", **Then** system validates provider has no active bookings or pending payouts, creates account deletion request with status "Pending Admin Approval", logs deletion request in audit trail, sends notification to admin team, displays confirmation "Account deletion request submitted. Our team will review and process your request within 5 business days.", and provider account remains active until admin approves
2. **Given** admin receives account deletion request, **When** admin reviews deletion request in admin dashboard, verifies provider has no active obligations, approves deletion request, **Then** system performs soft-delete (account status changed to "Deleted", provider login disabled, provider profile hidden from patient quote requests, all data retained in archive per FR-023), sends email confirmation to provider "Your account has been deleted. Your data has been archived per our data retention policy."
3. **Given** provider has 3 active bookings, **When** provider attempts to submit account deletion request, **Then** system validates provider obligations, detects active bookings, displays error "Cannot delete account. You have 3 active bookings. Please complete or cancel all bookings before deleting your account. For assistance, contact support at <support@hairlineapp.com>.", and blocks deletion request until bookings completed

---

### Edge Cases

- What happens when **provider uploads 10MB logo image exceeding 5MB limit**?
  - System validates image size during upload, detects size exceeds limit, displays error "Image too large. Maximum size is 5MB. Please compress or choose a smaller image.", and prevents upload until valid image selected

- How does system handle **provider changes password to same as current password**?
  - System validates new password ≠ current password, detects match, displays error "New password must be different from current password", and prevents password change until different password entered

- What occurs if **S-03 Notification Service unavailable when provider saves notification preferences**?
  - System attempts to update S-03 with new preferences, detects S-03 unavailable (timeout or 5xx error), queues preference update for retry (exponential backoff), displays success message to provider "Notification preferences updated" (optimistic UI), logs error for admin monitoring, and retries preference update every 1 minute for up to 5 minutes; if S-03 still unavailable after 5 minutes, admin receives alert

- What happens when **S-02 Payment Service returns validation error for bank account details**?
  - System receives validation error from S-02 (e.g., "Bank not found" or "SWIFT code mismatch"), displays error message to provider "Bank account validation failed: [error detail from S-02]. Please verify your bank details and try again.", prevents saving bank account details, and provider must correct details and retry

- How does system handle **provider Owner changes role to Admin (no longer Owner)**?
  - When admin changes provider's role from Owner to Admin (via FR-009), system detects role change, and next time user navigates to Settings & Support > Settings, the Billing tab is hidden from navigation (non-owner cannot see or access billing settings); existing bank account details remain saved and accessible to new Owner role user

- What occurs if **Help Centre content fails to load due to network issue**?
  - System attempts to fetch Help Centre content from admin content database, detects network timeout or error, displays cached version of Help Centre content (if available) with warning banner "Content may be outdated. Please refresh to load latest updates.", and provides "Retry" button for manual refresh

- How to manage **provider uploads award image with virus or malicious content**?
  - System scans uploaded image using anti-virus/malware scanning service (e.g., ClamAV), detects malicious content, deletes uploaded file, displays error "Image upload blocked due to security concerns. Please try a different image or contact support if this was a mistake.", logs security event for admin review, and prevents award image from being saved

---

## Functional Requirements Summary

### Core Requirements

- **REQ-032-001**: System MUST allow providers to upload and update clinic logo/profile picture (max 5MB, JPEG/PNG, min 200x200px)
- **REQ-032-002**: System MUST allow providers to select supported languages using the centrally managed system language options owned by FR-021 (Multi-Language & Localization), which are surfaced via FR-026 App Settings.
- **REQ-032-003**: System MUST allow providers to add, edit, delete awards with direct image upload (name, description, year, award image max 2MB)
- **REQ-032-004**: System MUST allow providers to update basic clinic information (name, description, contact email)
- **REQ-032-005**: System MUST allow providers to configure phone number with worldwide country code selection (FR-026 country codes)
- **REQ-032-006**: System MUST allow providers to select timezone from multiple timezone options (GMT-12 to GMT+14)
- **REQ-032-007**: System MUST allow providers to change password with current password verification and security policy validation (FR-026)
- **REQ-032-008**: System MUST allow providers to configure unified notification preferences (individual notification type toggles for quote, schedule, treatment start, aftercare, review, and promotion/discount notifications + global channel preferences: email, push)
- **REQ-032-009**: System MUST enforce notification preferences via S-03 Notification Service (FR-020 integration)
- **REQ-032-010**: System MUST allow provider Owners to manage billing settings (bank account details for payouts, FR-017 integration)
- **REQ-032-011**: System MUST restrict billing settings access to Owner role only (FR-009 role permissions)
- **REQ-032-012**: System MUST allow providers to access Help Centre with admin-managed content (FR-033 integration)
- **REQ-032-013**: System MUST allow providers to request account deletion (soft-delete with admin approval required)

### Data Requirements

- **REQ-032-014**: System MUST persist provider profile data (logo, name, description, languages, awards) and propagate to patient quote comparison view within 1 minute
- **REQ-032-015**: System MUST persist account settings (phone number in international format, timezone, password hash)
- **REQ-032-016**: System MUST persist notification preferences and synchronize with S-03 Notification Service within 1 minute
- **REQ-032-017**: System MUST persist bank account details encrypted at rest (AES-256) and mask in UI (last 4 digits visible)

### Security & Privacy Requirements

- **REQ-032-018**: System MUST encrypt bank account details at rest using AES-256
- **REQ-032-019**: System MUST hash passwords using bcrypt (cost factor 12+) and never store plain text passwords
- **REQ-032-020**: System MUST log all profile changes, account settings changes, billing settings changes, and account deletion requests in audit trail (timestamp, user ID, IP address, action, and appropriately masked old/new values where sensitive data is involved)
- **REQ-032-021**: System MUST send email notification to provider after password change (security alert)
- **REQ-032-022**: System MUST enforce role-based access control for billing settings (Owner role only; non-owners cannot see or access billing settings tab)
- **REQ-032-023**: System MUST perform soft-delete for account deletion requests (account status = "Deleted", data archived per FR-023 minimum 7 years)

### Integration Requirements

- **REQ-032-024**: System MUST integrate with S-03 Notification Service to enforce provider notification preferences (FR-020)
- **REQ-032-025**: System MUST integrate with S-02 Payment Service to validate bank account details format before saving
- **REQ-032-026**: System MUST integrate with FR-026/FR-021 language configuration to provide centrally managed language options in profile language selection (FR-021 is canonical for supported locales; FR-026 surfaces these via App Settings)
- **REQ-032-027**: System MUST integrate with FR-026 to provide country codes and timezone options in account settings
- **REQ-032-028**: System MUST integrate with FR-033 to display admin-managed Help Centre content

---

## Key Entities

- **Entity 1 - Provider Profile**: Represents clinic public-facing profile information
  - **Key attributes**: provider ID, clinic logo URL, optional cover image URL (static asset reference), clinic name, clinic description, contact email, public clinic phone, clinic website URL, clinic country, clinic city, supported languages (array), awards (array of award objects: name, issuer/organization, description, year, image URL), last updated timestamp, updated by user ID
  - **Relationships**: One provider has one profile; one profile has many awards; profile displayed to many patients during quote comparison

- **Entity 2 - Provider Account Settings**: Represents provider account configuration
  - **Key attributes**: provider ID, phone number (international format), country code, timezone, password hash, last password change date, password change history (timestamps), last updated timestamp
  - **Relationships**: One provider has one account settings record; account settings linked to provider profile

- **Entity 3 - Provider Notification Preferences**: Represents provider notification configuration
  - **Key attributes**: provider ID, quote notifications (boolean), schedule notifications (boolean), treatment start notifications (boolean), aftercare notifications (boolean), review notifications (boolean), email enabled (boolean), push enabled (boolean), last updated timestamp
  - **Relationships**: One provider has one notification preferences record; notification preferences enforced by S-03 Notification Service

- **Entity 4 - Provider Billing Settings**: Represents provider bank account details for payouts
  - **Key attributes**: provider ID, account holder name, bank name, account number (encrypted), routing/SWIFT code, IBAN (if applicable), last updated timestamp, updated by user ID (Owner role), S-02 validation status
  - **Relationships**: One provider has one billing settings record (accessible only to Owner role); billing settings used by FR-017 for provider payouts

- **Entity 5 - Provider Account Deletion Request**: Represents provider account deletion request workflow
  - **Key attributes**: request ID, provider ID, reason for deletion, request date, requested by user ID, status (Pending Admin Approval / Approved / Rejected), reviewed by admin ID, review date, review notes
  - **Relationships**: One provider can have multiple deletion requests (but only one "Pending" at a time); deletion request reviewed by one admin

- **Entity 6 - Help Centre Content (Admin-Managed)**: Represents help resources displayed to providers
  - **Key attributes**: content ID, category (FAQ / Tutorial Guide / Troubleshooting / Resource Library / Video Tutorial), title, body (HTML/Markdown), attachments (file URLs), created date, created by admin ID, last updated date, updated by admin ID
  - **Relationships**: Help Centre content created and managed by admins (FR-033); one provider can view many help centre content items (read-only)

- **Entity 7 - Provider Reviews View (Read-Only)**: Represents aggregated reviews and list data shown in Tab 5 (Reviews tab) within Screen 1 (Provider Profile)
  - **Key attributes**: provider ID, average rating, total reviews count, rating distribution (counts per star), reviews array (review ID, reviewer name, avatar URL, rating, review text, treatment type, review date), last sync timestamp
  - **Relationships**: Data sourced from Reviews module/service; provider can filter/sort but cannot mutate review records within FR-032

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-17 | 1.0 | Initial PRD creation for FR-032: Provider Dashboard Settings & Profile Management | AI/Claude |
| 2025-12-03 | 1.1 | Major updates: Removed SMS functionality throughout; Reorganized Screen 1 (Profile Management) into 5 tabs (Basic Information, Languages, Staff List, Awards, Reviews) with detailed inline editing specifications; Added account name unification rules (Owner accounts unified with clinic name, Staff accounts editable); Removed Screen 6 (Reviews now Tab 5 in Screen 1); Reorganized Screen 5 (Help Centre) into 7 subscreens with distinct layouts (FAQs, Articles, Resource Library, Video Tutorials, Contact Support, Feedback, Service Status); Updated navigation paths to "Settings & Support > Settings" and "Settings & Support > Provider profile"; Removed password change after 90 days requirement; Added per-tab save functionality with unsaved changes indicators; Updated language list references to FR-026 (centrally managed with country list); Removed admin metrics (profile completion, notification trends); Updated non-owner access restrictions (hidden tabs instead of error messages); Removed preview public profile functionality; Removed profile picture circle shape requirement and drag-and-drop; Updated all field specifications with inline editing details | AI/Claude |
| 2025-12-07 | 1.2 | **Major update - Full document management capabilities:** Added Tab 6: Documents to Screen 1 (Profile Management) with full provider document management (upload, replace, delete, view); Providers can now manage their own compliance documents (medical licenses, certifications, insurance) with drag-and-drop upload, file validation (PDF/JPG/PNG/DOCX/XLSX, max 10MB), document versioning (old versions archived on replace), soft delete, and optional notes; Admin-uploaded documents display "Admin" badge and are view-only for providers; Added document sync with FR-015 (bidirectional, within 1 minute); Updated Tab 3: Staff List to clarify display-only nature with "Manage Team" button linking to FR-009 for full staff management; Added Seat Usage Summary to Tab 3 showing current usage vs. seat limit; Updated Screen 1 tab count from 5 to 6 tabs; Updated General Business Rules to accurately reflect tab editability (Fully Editable: Tabs 1,2,4,6; Display-Only with External Management: Tab 3 via FR-009; Read-Only: Tab 5 Reviews); Added security rules (time-limited signed URLs), audit logging, sort/filter options, and comprehensive empty/error/loading state handling | AI/Claude |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | 2025-12-03 | ✅ Approved |
| Technical Lead | [Name] | 2025-12-03 | ✅ Approved |
| Stakeholder | [Name] | 2025-12-03 | ✅ Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Based on**: FR-032 from system-prd.md, Provider Platform Transcriptions Part 1 & 2
**Last Updated**: 2025-12-03
