# Product Requirements Document: Help Centre Content Management

**Module**: A-09: System Settings & Configuration | PR-06: Profile & Settings Management
**Feature Branch**: `fr033-help-centre-management`
**Created**: 2025-11-17
**Status**: Draft
**Source**: FR-033 from system-prd.md

---

## Executive Summary

The Help Centre Content Management module provides a centralized knowledge base and support system for the provider platform. This feature enables Hairline admins to create, organize, and maintain comprehensive help documentation that provider clinics can access for self-service support, reducing support ticket volume and improving provider efficiency.

**Key Objectives**:

- Provide providers with 24/7 access to self-service help resources
- Reduce support ticket volume by enabling providers to find answers independently
- Enable admins to centrally manage and update help content across all provider categories
- Support scalable content organization with multi-category structure
- Maintain content consistency and quality through admin-controlled publishing workflow

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: No patient-facing functionality (provider-specific feature)
- **Provider Platform (PR-06)**: Read-only access to Help Centre content organized by categories, searchable FAQ, tutorial resources
- **Admin Platform (A-09)**: Full Help Centre content management capabilities including content creation, editing, categorization, versioning, and publishing
- **Shared Services (S-XX)**: No dedicated shared services required

###

 Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- Not applicable (Help Centre is provider-specific)

**Provider Platform (PR-06)**:

- Access Help Centre landing page with category navigation (matches FR-032 Screen 5)
- View FAQs in distinct accordion layout organized by topics (matches FR-032 Screen 5.1)
- View Tutorial Guides, Troubleshooting Tips, and Policy Information in article layout (matches FR-032 Screen 5.2)
- Access Resource Library with file viewer/download interface (matches FR-032 Screen 5.3)
- Watch Video Tutorials with embedded video player (matches FR-032 Screen 5.4)
- Submit Contact Support requests via form with submission tracking (matches FR-032 Screen 5.5)
- Submit Feedback & Suggestions via form with submission tracking (matches FR-032 Screen 5.6)
- Check Service Status with status page interface (matches FR-032 Screen 5.7)
- Search across all Help Centre content

**Admin Platform (A-09)**:

- Create, edit, delete, and organize Help Centre content across 7 distinct subscreen types
- Manage FAQ content with accordion/topic organization interface (for FR-032 Screen 5.1)
- Manage article content (Tutorial Guides, Troubleshooting Tips, Policies) with article editor (for FR-032 Screen 5.2)
- Upload and manage Resource Library files with file management interface (for FR-032 Screen 5.3)
- Upload and manage Video Tutorials with video management interface (for FR-032 Screen 5.4)
- Manage Contact Support submissions with tracking interface (view, respond, update status) (for FR-032 Screen 5.5)
- Manage Feedback & Suggestions submissions with tracking interface (view, respond, update status) (for FR-032 Screen 5.6)
- Manage Service Status components, incidents, and maintenance windows (for FR-032 Screen 5.7)
- Publish/unpublish content to control provider visibility
- Version control for content updates with change tracking
- Preview content in provider-facing layout before publishing (matches each subscreen layout)
- Audit trail for all content changes (who, when, what changed)
- Bulk operations for content management
- Content analytics (view counts, search queries, popular topics)
- Multi-language content management (future enhancement)

**Shared Services (S-XX)**:

- Standard media storage service (S-05) for uploaded documents, videos, images
- Standard notification service (S-03) for content update notifications (future enhancement)

### Communication Structure

**In Scope**:

- Admin-to-provider communication via published Help Centre content
- Provider feedback/suggestion submission to admin team
- Contact support form submissions from providers to admin
- Content update notifications (future enhancement)

**Out of Scope**:

- Real-time chat between providers and admin (handled by separate communication module A-10)
- Provider-to-provider communication in community forum (future enhancement)
- Automated chatbot responses (future V2 enhancement)
- Email digest subscriptions for content updates (future enhancement)

### Entry Points

**Provider Entry**:

- Providers access Help Centre via "Help Centre" menu item in provider platform navigation
- Direct link from provider dashboard settings page (FR-032 integration point)
- Context-sensitive help links from various provider platform screens (future enhancement)

**Admin Entry**:

- Admins access Help Centre management via "System Settings & Configuration" section in admin platform
- Dedicated "Help Centre Management" module within A-09
- Quick access from admin dashboard for content updates

---

## Business Workflows

### Main Flow: Provider Accesses Help Centre Content

**Actors**: Provider (clinic staff), System
**Trigger**: Provider clicks "Help Centre" menu item in provider platform
**Outcome**: Provider views Help Centre page with organized content categories and can access help resources

**Steps**:

1. Provider navigates to "Help Centre" from provider platform navigation menu (Settings & Support > Help Centre)
2. System loads Help Centre landing page with category navigation and search bar (matches FR-032 Screen 5)
3. System shows category navigation menu linking to 7 subscreens: FAQs, Tutorial Guides/Troubleshooting Tips/Policies, Resource Library, Video Tutorials, Contact Support, Feedback & Suggestions, Service Status
4. Provider selects a category (e.g., "FAQs")
5. System displays content in appropriate subscreen layout (e.g., FAQs in accordion layout - FR-032 Screen 5.1)
6. Provider browses content using subscreen-specific interface (accordion for FAQs, article layout for guides, file viewer for resources, video player for videos, forms for support/feedback, status page for service status)
7. Provider finds answer to their question or completes tutorial walkthrough
8. System logs content access for analytics (view count, time spent)
9. Provider returns to their workflow or explores additional Help Centre content

### Alternative Flows

**A1: Provider Submits Feedback via Help Centre**:

- **Trigger**: Provider cannot find answer in Help Centre and wants to submit feedback
- **Steps**:
  1. Provider navigates to Help Centre and selects "Feedback & Suggestions" subscreen (FR-032 Screen 5.6)
  2. System displays feedback submission form (feedback type, title, description, priority)
  3. Provider completes form with feedback details and submits
  4. System validates form fields and creates feedback submission with unique ID
  5. System displays confirmation "Thank you for your feedback! We'll review your submission."
  6. System creates feedback record with status "Submitted" and notifies admin team
  7. Admin reviews feedback in admin dashboard, updates status (Under Review, Planned, Implemented, Declined), and optionally responds
  8. Provider can view submission status in their Feedback & Suggestions subscreen
- **Outcome**: Provider feedback captured, tracked, and managed by admin team

**A2: Provider Contacts Support Directly**:

- **Trigger**: Provider needs direct assistance beyond self-service content
- **Steps**:
  1. Provider navigates to Help Centre and selects "Contact Support" subscreen (FR-032 Screen 5.5)
  2. System displays support request form (subject, category, message, priority, optional attachment)
  3. Provider completes form with support request details and submits
  4. System validates form fields and creates support ticket with unique ticket number
  5. System displays confirmation "Support request submitted. Ticket #[number]. Our team will respond within 24 hours."
  6. System sends confirmation email to provider with ticket reference number
  7. Admin team receives notification and views support request in admin dashboard
  8. Admin updates ticket status (Open → In Progress → Resolved → Closed) and responds
  9. Provider can view ticket status and responses in their Contact Support subscreen
- **Outcome**: Support request routed to admin team, tracked, and managed with status updates

**A3: Provider Checks Service Status**:

- **Trigger**: Provider experiences platform issues and wants to check if it's a known system outage
- **Steps**:
  1. Provider navigates to Help Centre and selects "Service Status" subscreen (FR-032 Screen 5.7)
  2. System displays status page interface with overall status indicator (All Systems Operational, Partial Outage, Major Outage)
  3. System shows service components status list (each component: name, status, last updated)
  4. System displays incident history timeline (recent incidents with status, timeline, affected services)
  5. System shows maintenance schedule (upcoming scheduled maintenance windows)
  6. Provider verifies if issue is platform-wide or localized to their account
  7. Provider can subscribe to status update notifications (email alerts for incidents)
  8. Provider proceeds accordingly (waits for resolution or contacts support)
- **Outcome**: Provider informed of system status via status page interface and can plan accordingly

**B1: Content Not Found or Outdated**:

- **Trigger**: Provider cannot find needed information in Help Centre
- **Steps**:
  1. Provider searches/browses Help Centre but cannot find relevant content
  2. Provider clicks "Was this helpful? No" feedback button
  3. System prompts provider to describe what they were looking for
  4. Provider submits "content not found" feedback with description
  5. System logs feedback and notifies admin team
  6. Admin team reviews feedback and prioritizes content creation/update
- **Outcome**: Content gap identified and queued for admin action

**B2: Uploaded File Fails to Load**:

- **Trigger**: Provider attempts to download tutorial guide or view video but file fails to load
- **Steps**:
  1. Provider clicks on tutorial guide or video link
  2. System attempts to fetch file from media storage (S-05)
  3. File fetch fails (network error, file missing, permission issue)
  4. System displays error message with retry option and "report issue" link
  5. Provider clicks "report issue" link
  6. System creates automated issue ticket with error details (file ID, provider ID, timestamp, error type)
  7. Admin receives notification and investigates file storage issue
- **Outcome**: File loading error reported and admin notified for resolution

---

### Main Flow: Admin Creates Help Centre Content

**Actors**: Admin (Help Centre content manager), System
**Trigger**: Admin needs to create new help content or update existing content
**Outcome**: New or updated content published to Help Centre for provider access

**Steps**:

1. Admin navigates to "Help Centre Management" in admin platform (A-09)
2. System displays Help Centre content management dashboard with content list organized by subscreen type
3. Admin selects subscreen type to manage (FAQs, Articles, Resources, Videos, Contact Support, Feedback, Service Status)
4. Admin clicks "Create New Content" button for selected subscreen type
5. System displays content creation form optimized for selected subscreen layout:
   - **FAQs**: FAQ editor with question/answer fields, topic assignment, accordion preview
   - **Articles**: Article editor with rich text, table of contents generation, article layout preview
   - **Resources**: File upload interface with metadata (name, description, category, file type), file viewer preview
   - **Videos**: Video upload interface with title, description, thumbnail, video player preview
   - **Contact Support/Feedback**: Form builder interface (not applicable - forms are system-managed)
   - **Service Status**: Status component/incident management interface
6. Admin enters content details using subscreen-specific editor
7. Admin uploads attachments if needed (images, PDFs, videos) - optimized for subscreen type
8. Admin assigns tags for content organization and searchability
9. Admin clicks "Preview" to see how content will appear to providers in the specific subscreen layout
10. System renders preview matching provider-facing layout (accordion for FAQs, article layout for guides, file viewer for resources, video player for videos, status page for service status)
11. Admin reviews preview and clicks "Save as Draft" or "Publish"
12. System saves content with status (Draft/Published) and timestamps
13. System logs content creation in audit trail (admin name, timestamp, action)
14. If published, system makes content immediately available in provider Help Centre subscreen
15. System displays success confirmation with link to view published content

### Alternative Flows

**A4: Admin Edits Existing Help Centre Content**:

- **Trigger**: Admin needs to update outdated or incorrect help content
- **Steps**:
  1. Admin navigates to Help Centre content list in admin platform
  2. Admin searches/filters content by category, title, or tags
  3. Admin clicks "Edit" on target content item
  4. System loads content editor pre-filled with existing content
  5. System creates new version of content in version control
  6. Admin makes changes to title, body, attachments, or category
  7. Admin previews changes to verify formatting and accuracy
  8. Admin saves changes with optional "Version note" describing what changed
  9. System updates content version and logs change in audit trail
  10. If content is published, system immediately updates provider-facing content
  11. System sends notification to admins who subscribed to content change alerts (future enhancement)
- **Outcome**: Content updated with new version and change tracked in audit trail

**A5: Admin Organizes FAQ Content into Topics**:

- **Trigger**: Admin needs to organize multiple FAQ items under topic sections for better navigation
- **Steps**:
  1. Admin navigates to FAQ Management screen (Screen 2) in Help Centre management
  2. System displays all FAQ items with current organization structure
  3. Admin clicks "Manage Topics" to create/edit FAQ topic sections
  4. System displays topic management interface with drag-and-drop organization
  5. Admin creates new topic section (e.g., "Quote Submission", "Payment Processing")
  6. Admin assigns FAQ items to topics by dragging items into topic groups
  7. Admin reorders topics and FAQ items within topics for logical flow
  8. Admin previews FAQ accordion layout to verify organization
  9. Admin saves organization structure
  10. System updates FAQ navigation structure for provider Help Centre (FR-032 Screen 5.1)
  11. Provider Help Centre immediately reflects new organization in accordion layout
- **Outcome**: FAQ content organized into logical topic sections displayed in accordion layout for easier provider navigation

**A6: Admin Uploads Video Tutorial**:

- **Trigger**: Admin needs to add video tutorial to Help Centre
- **Steps**:
  1. Admin navigates to Video Tutorial Management screen (Screen 5) in Help Centre management
  2. Admin clicks "Create New Video Tutorial"
  3. System displays video upload form with fields: title, description, video file upload, thumbnail image, transcript (optional), tags
  4. Admin enters title and description for video tutorial
  5. Admin uploads video file (supports MP4, MOV formats, max 500MB)
  6. System validates file size, format, and begins upload to media storage (S-05)
  7. System displays upload progress bar
  8. System auto-extracts video duration and generates thumbnail from video frame (10% mark)
  9. Admin uploads custom thumbnail image or uses auto-generated thumbnail
  10. Admin optionally enters video transcript for accessibility
  11. Admin previews video in video player interface (matches FR-032 Screen 5.4)
  12. Admin publishes video tutorial
  13. System processes video for streaming optimization (if applicable)
  14. System makes video available in provider Help Centre Video Tutorials subscreen (FR-032 Screen 5.4)
- **Outcome**: Video tutorial uploaded, processed, and published to Help Centre with video player interface

**A7: Admin Unpublishes Outdated Content**:

- **Trigger**: Admin needs to remove outdated or incorrect content from provider view
- **Steps**:
  1. Admin identifies outdated content item in content list
  2. Admin clicks "Unpublish" action on content item
  3. System prompts admin to confirm unpublish action with reason
  4. Admin enters reason (e.g., "Content outdated, new version coming soon")
  5. Admin confirms unpublish
  6. System changes content status from "Published" to "Unpublished"
  7. System immediately removes content from provider Help Centre view
  8. System logs unpublish action in audit trail with reason
  9. Content remains in admin view as "Unpublished" for future editing or re-publishing
- **Outcome**: Content removed from provider view but preserved in admin system for future use

**B3: Content Validation Fails**:

- **Trigger**: Admin attempts to publish content with missing required fields or invalid format
- **Steps**:
  1. Admin completes content creation form and clicks "Publish"
  2. System validates required fields (category, title, content body)
  3. System detects validation error (e.g., missing title, empty content body, unsupported file format)
  4. System displays error message highlighting missing/invalid fields
  5. Admin corrects validation errors
  6. Admin re-submits content for publishing
  7. System re-validates and proceeds with publish if all validations pass
- **Outcome**: Validation errors corrected and content published successfully

**B4: File Upload Exceeds Size Limit**:

- **Trigger**: Admin attempts to upload file larger than maximum allowed size
- **Steps**:
  1. Admin selects file for upload (video, PDF, image) in appropriate management screen
  2. System checks file size against limits (videos: 500MB, PDFs: 50MB, images: 10MB)
  3. File exceeds size limit
  4. System displays error message with file size limit and suggested alternatives (compress file, use external video hosting)
  5. Admin reduces file size or uses alternative hosting (YouTube/Vimeo embed link)
  6. Admin re-uploads compressed file or adds external video embed link
  7. System validates new file/link and proceeds with upload
- **Outcome**: File size issue resolved and content uploaded successfully

**A8: Admin Manages Contact Support Submissions**:

- **Trigger**: Admin needs to view and respond to provider support requests
- **Steps**:
  1. Admin navigates to Contact Support Management screen (Screen 6) in Help Centre management
  2. System displays list of all support requests with status, ticket numbers, providers, dates
  3. Admin filters requests by status (Open, In Progress, Resolved, Closed) or category
  4. Admin clicks on support request to view details
  5. System displays full request: subject, message, category, priority, attachment (if provided), provider information
  6. Admin reviews request and updates status (e.g., Open → In Progress)
  7. Admin adds response message in conversation thread
  8. System saves response and updates request status
  9. System sends email notification to provider (if implemented)
  10. Provider can view status update and response in their Contact Support subscreen (FR-032 Screen 5.5)
- **Outcome**: Support request managed with status tracking and admin response

**A9: Admin Manages Feedback Submissions**:

- **Trigger**: Admin needs to review and respond to provider feedback submissions
- **Steps**:
  1. Admin navigates to Feedback & Suggestions Management screen (Screen 7) in Help Centre management
  2. System displays list of all feedback submissions with status, type, providers, dates
  3. Admin filters submissions by type (Feature Request, Bug Report, Suggestion) or status
  4. Admin clicks on feedback submission to view details
  5. System displays full submission: type, title, description, priority, provider information
  6. Admin reviews feedback and updates status (e.g., Submitted → Under Review → Planned)
  7. Admin adds response message explaining status or implementation plan
  8. System saves response and updates submission status
  9. Status update visible to provider in their Feedback & Suggestions subscreen (FR-032 Screen 5.6)
- **Outcome**: Feedback submission managed with status tracking and admin response

**A10: Admin Updates Service Status**:

- **Trigger**: Admin needs to update platform service status or create incident report
- **Steps**:
  1. Admin navigates to Service Status Management screen (Screen 8) in Help Centre management
  2. System displays current overall status, service components list, incident history, maintenance schedule
  3. Admin updates service component status (e.g., "API Service" → Degraded)
  4. System automatically recalculates overall status based on component statuses
  5. Admin creates new incident: enters title, description, selects affected services, sets status (Investigating)
  6. System creates incident record and adds to incident history timeline
  7. Admin updates incident status as investigation progresses (Investigating → Identified → Monitoring → Resolved)
  8. System updates incident timeline with each status change
  9. Status updates propagate to provider Service Status subscreen (FR-032 Screen 5.7) within 1 minute
  10. Providers see updated status in real-time status page interface
- **Outcome**: Service status updated and displayed to providers in status page interface

---

## Screen Specifications

### Screen 1: Admin Help Centre Management Dashboard

**Purpose**: Central dashboard for managing all Help Centre content organized by subscreen types matching FR-032 provider-facing structure.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Content Type Filter | dropdown | No | Filter content by subscreen type (FAQs, Articles, Resources, Videos, Contact Support, Feedback, Service Status) | Pre-defined types matching FR-032 subscreens |
| Content List | table/list | No | List of all content items with metadata | Each row: title, subscreen type, status (Draft/Published/Unpublished), last updated, view count |
| Quick Stats | display cards | No | Summary statistics: total content, published content, draft content, total views | Read-only, calculated |
| Recent Activity | timeline | No | Recent content changes and submissions | Read-only, sorted by date |

**Business Rules**:

- Dashboard organized by subscreen types matching FR-032 structure (FAQs, Articles, Resources, Videos, Contact Support, Feedback, Service Status)
- Content list filterable by subscreen type, status, category, and searchable by title/tags
- Quick stats update in real-time
- Recent activity shows: content created/edited/published, support requests received, feedback submissions received, service status updates
- Clicking content item opens appropriate editor for that subscreen type

**Notes**:

- Dashboard provides quick access to all Help Centre management functions
- Visual indicators show content status (Published: green, Draft: yellow, Unpublished: gray)
- Bulk actions available: publish multiple items, unpublish multiple items, delete multiple items
- Export functionality for content analytics

---

### Screen 2: Admin FAQ Management (for FR-032 Screen 5.1)

**Purpose**: Create and manage FAQ content that displays in accordion layout on provider platform (matches FR-032 Screen 5.1).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| FAQ Question | text | Yes | FAQ question text | Max 200 chars |
| FAQ Answer | rich text | Yes | FAQ answer content | Max 5000 chars, supports HTML formatting |
| FAQ Topic | dropdown | Yes | Topic category for organization | Pre-defined topics or create new |
| Display Order | number | No | Order within topic | Integer, auto-incremented |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback |

**Business Rules**:

- FAQ editor optimized for accordion display format (question as header, answer as expandable content)
- FAQs organized by topics with drag-and-drop reordering within topics
- Preview shows exact accordion layout as providers will see (FR-032 Screen 5.1)
- Multiple FAQs can be edited in batch
- Topic management: create, edit, delete, reorder topics
- Helpfulness feedback tracked per FAQ for analytics

**Notes**:

- FAQ editor interface: question field at top, answer field below with rich text editor
- Topic selector with "Create New Topic" option
- Drag-and-drop interface for reordering FAQs within topics
- Preview button shows accordion layout with expand/collapse functionality
- Bulk operations: assign multiple FAQs to topic, change status for multiple FAQs

---

### Screen 3: Admin Article Management (for FR-032 Screen 5.2)

**Purpose**: Create and manage article content (Tutorial Guides, Troubleshooting Tips, Policy Information) that displays in article layout on provider platform (matches FR-032 Screen 5.2).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Article Title | text | Yes | Article title | Max 200 chars |
| Article Content | rich text | Yes | Full article content with formatting | Max 10,000 chars, supports HTML, headings, lists, images, tables |
| Article Type | dropdown | Yes | Tutorial Guide, Troubleshooting Tip, Policy Information | Pre-defined types |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new |
| Table of Contents | auto-generated | No | Auto-generated from headings (for articles >1000 words) | Read-only, generated on save |
| Related Articles | multi-select | No | Links to related articles | References to other articles |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback |

**Business Rules**:

- Article editor optimized for article layout format (full-width content with formatted text, images, code blocks)
- Rich text editor supports: headings (H1-H6), bold, italic, lists, links, images, tables, code blocks
- Table of contents auto-generated for articles with multiple headings (articles >1000 words)
- Preview shows exact article layout as providers will see (FR-032 Screen 5.2)
- Related articles can be manually assigned or auto-suggested based on tags/category
- Print-friendly view available in preview

**Notes**:

- Article editor: full-featured rich text editor with formatting toolbar
- Image upload inline within editor
- Screenshot/image insertion with captions
- Step-by-step tutorial format: numbered lists with visual separators
- Preview shows: formatted article with table of contents (if applicable), related articles section
- Character counter for content body

---

### Screen 4: Admin Resource Library Management (for FR-032 Screen 5.3)

**Purpose**: Upload and manage downloadable resources (templates, documents, PDFs) that display in file viewer interface on provider platform (matches FR-032 Screen 5.3).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Resource Name | text | Yes | Display name for resource | Max 200 chars |
| Resource Description | textarea | No | Brief description of resource | Max 500 chars |
| Resource File | file upload | Yes | File to upload (PDF, DOCX, XLSX, etc.) | Max 50MB, whitelist: PDF, DOCX, XLSX, PNG, JPG |
| Resource Category | dropdown | No | Category (Templates, Documents, Forms, etc.) | Pre-defined categories |
| File Type | auto-detected | No | File format detected from upload | Read-only, auto-detected |
| File Size | auto-calculated | No | File size in MB | Read-only, auto-calculated |
| Thumbnail/Icon | image upload | No | Custom thumbnail or file type icon | Max 1MB, PNG/JPG, 128x128px recommended |
| Download Count | display | No | Number of times resource downloaded | Read-only, incremented on download |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses |

**Business Rules**:

- File upload interface optimized for resource management
- Preview shows exact file viewer interface as providers will see (FR-032 Screen 5.3)
- File type icons auto-assigned if no custom thumbnail uploaded
- Download count tracked per resource
- Resources filterable by category and file type
- Preview available for PDF and image files (opens in modal)

**Notes**:

- File upload: drag-and-drop or file picker with progress indicator
- File validation: size check, format check, virus scan
- Thumbnail generation: auto-generate from PDF first page or use custom upload
- Preview modal: shows resource card with thumbnail, name, description, file type badge, download button
- Bulk upload: upload multiple files at once
- File replacement: replace existing file while keeping same resource record

---

### Screen 5: Admin Video Tutorial Management (for FR-032 Screen 5.4)

**Purpose**: Upload and manage video tutorials that display in video viewer interface on provider platform (matches FR-032 Screen 5.4).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Video Title | text | Yes | Video tutorial title | Max 200 chars |
| Video Description | textarea | No | Brief description of video content | Max 500 chars |
| Video File | file upload | Yes | Video file to upload | Max 500MB, formats: MP4, MOV |
| Video Thumbnail | image upload | No | Custom thumbnail image | Max 2MB, PNG/JPG, 16:9 aspect ratio recommended |
| Video Duration | auto-calculated | No | Video length in minutes:seconds | Read-only, extracted from video file |
| Video Transcript | textarea | No | Text transcript of video (optional) | Max 10,000 chars |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new |
| Related Videos | multi-select | No | Links to related video tutorials | References to other videos |
| View Count | display | No | Number of times video viewed (>30 seconds) | Read-only, incremented on view |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback |

**Business Rules**:

- Video upload interface optimized for video management
- Video processing: system processes uploaded video for streaming optimization (if applicable)
- Thumbnail generation: auto-generate from video frame at 10% mark or use custom upload
- Preview shows exact video player interface as providers will see (FR-032 Screen 5.4)
- Video transcript optional but recommended for accessibility
- View count incremented when video plays for >30 seconds
- Related videos can be manually assigned or auto-suggested based on tags/category

**Notes**:

- Video upload: file picker with progress indicator, supports large files (500MB max)
- Upload progress: shows upload percentage and estimated time remaining
- Video processing: background job processes video after upload (transcoding, thumbnail generation)
- Thumbnail editor: crop/select frame from video for thumbnail
- Preview: embedded video player with play controls (play, pause, volume, fullscreen, playback speed)
- Transcript editor: textarea with character counter, searchable text
- Video analytics: view count, average watch time, completion rate

---

### Screen 6: Admin Contact Support Management (for FR-032 Screen 5.5)

**Purpose**: View and manage Contact Support submissions from providers with status tracking and response capabilities (matches FR-032 Screen 5.5 provider-facing form).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Support Request List | table | No | List of all support requests | Each row: ticket number, subject, category, status, provider name, submitted date, last updated |
| Ticket Number | display | No | Unique ticket identifier | Read-only, auto-generated |
| Subject | text | No | Support request subject (from provider) | Read-only, from provider submission |
| Category | display | No | Request category (from provider) | Read-only, from provider submission |
| Priority | display | No | Request priority (from provider) | Read-only, from provider submission |
| Message | textarea | No | Full support request message (from provider) | Read-only, from provider submission |
| Attachment | file link | No | Attached file from provider (if provided) | Read-only, downloadable |
| Status | dropdown | Yes | Open, In Progress, Resolved, Closed | Editable by admin |
| Admin Response | textarea | No | Admin response message | Max 2000 chars |
| Response History | timeline | No | Full conversation thread | Read-only, chronological |
| Provider Information | display | No | Provider name, email, clinic | Read-only, from provider account |

**Business Rules**:

- Support request list filterable by status, category, priority, date range, provider
- Status workflow: Open → In Progress → Resolved → Closed
- Admin can add response messages to support requests (creates conversation thread)
- Status updates trigger email notifications to provider (if implemented)
- Support requests cannot be deleted (archived only for audit compliance)
- Bulk actions: update status for multiple requests, assign to admin team members (if implemented)

**Notes**:

- Support request detail view: shows full request with conversation thread
- Response editor: rich text editor for admin responses
- Status badges: color-coded (Open: blue, In Progress: yellow, Resolved: green, Closed: gray)
- Filter/sort: by status, date, priority, provider
- Export: export support requests to CSV for reporting
- Analytics: average response time, resolution time, request volume by category

---

### Screen 7: Admin Feedback & Suggestions Management (for FR-032 Screen 5.6)

**Purpose**: View and manage Feedback & Suggestions submissions from providers with status tracking and response capabilities (matches FR-032 Screen 5.6 provider-facing form).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Feedback List | table | No | List of all feedback submissions | Each row: submission ID, title, type, status, provider name, submitted date, admin response |
| Submission ID | display | No | Unique feedback identifier | Read-only, auto-generated |
| Feedback Type | display | No | Type (Feature Request, Bug Report, Suggestion, Other) | Read-only, from provider submission |
| Title | text | No | Feedback title (from provider) | Read-only, from provider submission |
| Description | textarea | No | Full feedback description (from provider) | Read-only, from provider submission |
| Priority | display | No | Suggested priority (from provider) | Read-only, from provider submission |
| Status | dropdown | Yes | Submitted, Under Review, Planned, Implemented, Declined | Editable by admin |
| Admin Response | textarea | No | Admin response message | Max 2000 chars |
| Response History | timeline | No | Full conversation thread | Read-only, chronological |
| Provider Information | display | No | Provider name, email, clinic | Read-only, from provider account |

**Business Rules**:

- Feedback list filterable by type, status, priority, date range, provider
- Status workflow: Submitted → Under Review → Planned/Implemented/Declined
- Admin can add response messages to feedback (creates conversation thread)
- Status updates visible to provider in their Feedback & Suggestions subscreen
- Feedback submissions cannot be deleted (archived only for audit compliance)
- Bulk actions: update status for multiple submissions, export to CSV

**Notes**:

- Feedback detail view: shows full submission with conversation thread
- Response editor: rich text editor for admin responses
- Status badges: color-coded (Submitted: gray, Under Review: blue, Planned: yellow, Implemented: green, Declined: red)
- Filter/sort: by type, status, priority, date, provider
- Analytics: feedback volume by type, implementation rate, average time to implementation
- Roadmap integration: "Planned" feedback can be linked to roadmap items (if implemented)

---

### Screen 8: Admin Service Status Management (for FR-032 Screen 5.7)

**Purpose**: Manage service status components, incidents, and maintenance windows that display in status page interface on provider platform (matches FR-032 Screen 5.7).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Overall Status | dropdown | Yes | All Systems Operational, Partial Outage, Major Outage | Pre-defined statuses |
| Service Components List | table | No | List of service components | Each row: component name, status (Operational/Degraded/Down), last updated |
| Component Name | text | Yes | Service component name | Max 100 chars |
| Component Status | dropdown | Yes | Operational, Degraded, Down | Pre-defined statuses |
| Incident History | timeline | No | List of recent incidents | Each incident: title, description, status, start time, end time, affected services |
| Incident Title | text | Yes | Brief incident title | Max 200 chars |
| Incident Description | textarea | Yes | Detailed incident description | Max 2000 chars |
| Incident Status | dropdown | Yes | Investigating, Identified, Monitoring, Resolved | Pre-defined statuses |
| Affected Services | multi-select | Yes | Service components affected by incident | References to service components |
| Maintenance Schedule | table | No | List of scheduled maintenance windows | Each maintenance: title, description, scheduled start/end time, affected services |
| Maintenance Title | text | Yes | Brief maintenance title | Max 200 chars |
| Maintenance Description | textarea | Yes | Detailed maintenance description | Max 2000 chars |
| Scheduled Start Time | datetime | Yes | Planned maintenance start time | Valid datetime, future date |
| Scheduled End Time | datetime | Yes | Planned maintenance end time | Valid datetime, after start time |

**Business Rules**:

- Overall status automatically calculated from service component statuses (if any component is Down → Partial/Major Outage)
- Service components: create, edit, delete components; update status in real-time
- Incident management: create new incidents, update status, add timeline updates, mark as resolved
- Maintenance schedule: create scheduled maintenance, edit, cancel, mark as completed
- Status updates propagate to provider platform within 1 minute
- Incident timeline: system auto-logs status changes with timestamps
- Preview shows exact status page interface as providers will see (FR-032 Screen 5.7)

**Notes**:

- Service component management: grid/list interface with status badges
- Status badges: color-coded (Operational: green, Degraded: yellow, Down: red)
- Incident editor: form with timeline view showing status progression
- Maintenance scheduler: calendar interface for scheduling maintenance windows
- Real-time updates: status changes reflect immediately in provider view
- Notification settings: admins can configure email notifications for status changes (if implemented)
- Historical data: past incidents and completed maintenance retained for historical reference

---

### Screen 9: Admin Content Preview

**Purpose**: Preview Help Centre content exactly as it will appear to providers in each subscreen layout before publishing.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Preview Mode | dropdown | Yes | Select subscreen layout to preview (FAQs, Articles, Resources, Videos, Service Status) | Pre-defined layouts matching FR-032 |
| Content Preview | rendered view | No | Rendered content in provider-facing layout | Read-only, matches FR-032 subscreen layouts |

**Business Rules**:

- Preview renders content in exact provider-facing layout for selected subscreen type
- FAQ preview shows accordion layout with expand/collapse (matches FR-032 Screen 5.1)
- Article preview shows article layout with table of contents (matches FR-032 Screen 5.2)
- Resource preview shows file viewer interface (matches FR-032 Screen 5.3)
- Video preview shows video player interface (matches FR-032 Screen 5.4)
- Service Status preview shows status page interface (matches FR-032 Screen 5.7)
- Preview updates in real-time as admin edits content
- Preview includes all formatting, images, and interactive elements

**Notes**:

- Preview pane: side-by-side or modal view showing provider-facing layout
- Responsive preview: toggle between desktop/tablet/mobile views
- Print preview: available for article content
- Preview navigation: test all interactive elements (expand/collapse, video playback, file download)

---

## Business Rules

### General Module Rules

- **Rule 1**: Help Centre content is provider-specific and not visible to patients
- **Rule 2**: Only admins can create, edit, or delete Help Centre content; providers have read-only access
- **Rule 3**: Content must be assigned to exactly one of the 10 predefined categories (no uncategorized content)
- **Rule 4**: Content can exist in three states: Draft (admin-only), Published (provider-visible), Unpublished (admin-only, previously published)
- **Rule 5**: All content changes logged in audit trail with admin identity, timestamp, and action type
- **Rule 6**: Content deletion is soft-delete (archived) not permanent deletion to support recovery and audit compliance

### Data & Privacy Rules

- **Privacy Rule 1**: Help Centre content is non-sensitive and accessible to all provider staff within a clinic account (no role-based content restrictions within provider platform)
- **Privacy Rule 2**: Provider feedback and support requests captured with provider identity for admin follow-up
- **Privacy Rule 3**: Content view analytics tracked at organization level (provider clinic), not individual staff member level
- **Audit Rule**: All content creation, editing, publishing, unpublishing, and deletion actions logged with admin identity and timestamp for compliance audit trail
- **Data Retention**: Archived content retained indefinitely for historical reference and audit compliance

### Admin Editability Rules

**Editable by Admin**:

- All Help Centre content (title, body, attachments, category assignment, publish status) organized by subscreen types matching FR-032
- FAQ content with accordion/topic organization (for FR-032 Screen 5.1)
- Article content (Tutorial Guides, Troubleshooting Tips, Policies) with article layout formatting (for FR-032 Screen 5.2)
- Resource Library files with file metadata (for FR-032 Screen 5.3)
- Video Tutorials with video metadata and transcripts (for FR-032 Screen 5.4)
- Contact Support submissions: view, respond, update status (Open, In Progress, Resolved, Closed) (for FR-032 Screen 5.5)
- Feedback & Suggestions submissions: view, respond, update status (Submitted, Under Review, Planned, Implemented, Declined) (for FR-032 Screen 5.6)
- Service Status: overall status, service components, incidents, maintenance windows (for FR-032 Screen 5.7)
- Category organization and ordering
- FAQ topic organization and FAQ item assignment to topics
- Content tags and related content links
- Support contact information (email, business hours, response SLA)

**Fixed in Codebase (Not Editable)**:

- Number of Help Centre subscreen types (fixed at 7 types matching FR-032): FAQs (Screen 5.1), Articles (Screen 5.2), Resources (Screen 5.3), Videos (Screen 5.4), Contact Support (Screen 5.5), Feedback (Screen 5.6), Service Status (Screen 5.7)
- Content type options (FAQ, Tutorial Guide, Troubleshooting Tip, Video Tutorial, Resource Document, Policy Document)
- File upload size limits (PDF: 50MB, Video: 500MB, Image: 10MB)
- Content body character limits (max 5000 characters for FAQ answers, max 10,000 characters for tutorial guides)
- Audit log retention period (indefinite retention for compliance)

**Configurable with Restrictions**:

- Category visibility (admin can show/hide categories but cannot delete predefined categories)
- Content versioning (enabled by default, admin cannot disable version control)
- Provider feedback submission (enabled by default, admin cannot disable but can moderate responses)

### Payment & Billing Rules

*Not applicable - Help Centre is a content management feature with no payment or billing components.*

---

## Success Criteria

### Provider Experience Metrics

- **SC-001**: Providers can access Help Centre and find relevant content within 2 clicks from any provider platform screen
- **SC-002**: 70% of provider support questions can be answered via Help Centre self-service content (reducing support ticket volume)
- **SC-003**: Providers can navigate Help Centre and find answers to common questions in under 3 minutes
- **SC-004**: 80% of providers rate Help Centre content as "Helpful" or "Very Helpful" via feedback buttons

### Admin Management Metrics

- **SC-005**: Admins can create and publish new Help Centre content in under 10 minutes per content item
- **SC-006**: Admins can update existing content and publish changes in under 5 minutes
- **SC-007**: Admins can organize FAQ topics and reorder content in under 5 minutes using drag-and-drop interface
- **SC-008**: 100% of Help Centre content changes tracked in audit trail for compliance verification

### System Performance Metrics

- **SC-009**: Help Centre landing page loads in under 2 seconds for 95% of requests
- **SC-010**: Content search returns results in under 1 second for 90% of queries (future enhancement)
- **SC-011**: File downloads (PDFs, videos) begin within 3 seconds of provider click
- **SC-012**: System supports 1000 concurrent provider accesses to Help Centre without performance degradation

### Business Impact Metrics

- **SC-013**: Support ticket volume from providers reduces by 30% within 3 months of Help Centre launch
- **SC-014**: Average time to resolve provider support issues decreases by 25% due to self-service content availability
- **SC-015**: 60% of providers access Help Centre at least once per month for self-service support
- **SC-016**: Help Centre content view count increases by 20% month-over-month indicating growing provider adoption

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-032 / Module PR-06**: Help Centre accessed from provider settings page
  - **Why needed**: Help Centre menu item appears in provider platform navigation, linked from FR-032 profile & settings module
  - **Integration point**: Help Centre navigation menu item added to provider platform sidebar, accessible from settings page

- **FR-031 / Module A-09**: Admin access control for Help Centre management
  - **Why needed**: Help Centre management requires admin role permissions to create, edit, publish content
  - **Integration point**: Admin platform role-based permissions control access to Help Centre management features

- **FR-009 / Module PR-01**: Provider team member access to Help Centre
  - **Why needed**: All provider staff (regardless of role) should be able to access Help Centre for support
  - **Integration point**: Help Centre accessible to all provider roles defined in FR-009 (Owner, Manager, Clinical Staff, Billing Staff)

### External Dependencies (APIs, Services)

- **External Service 1**: Media Storage Service (S-05)
  - **Purpose**: Store uploaded tutorial guides, videos, images, PDF documents
  - **Integration**: RESTful API calls for file upload, retrieval, deletion
  - **Failure handling**: If media storage unavailable, queue uploads for retry; display cached content to providers; notify admin of storage issues

- **External Service 2**: Rich Text Editor Library (e.g., Quill, TinyMCE, CKEditor)
  - **Purpose**: Provide WYSIWYG editing for Help Centre content creation
  - **Integration**: JavaScript library integrated into admin content creation form
  - **Failure handling**: If editor library fails to load, fall back to plain textarea with markdown support

- **External Service 3**: Virus Scanning Service (e.g., ClamAV, cloud-based scanner)
  - **Purpose**: Scan uploaded files for viruses and malware before storage
  - **Integration**: API call during file upload process
  - **Failure handling**: If virus scanner unavailable, quarantine uploads and notify admin; do not make files available to providers until scan completes

### Data Dependencies

- **Entity 1**: Admin user accounts with Help Centre management permissions
  - **Why needed**: Cannot create or manage Help Centre content without authenticated admin user with appropriate permissions
  - **Source**: Admin platform authentication module (A-09 / FR-031)

- **Entity 2**: Provider clinic accounts
  - **Why needed**: Cannot display Help Centre content to providers without active provider accounts
  - **Source**: Provider authentication and account management module (PR-01 / FR-009)

- **Entity 3**: Media storage infrastructure
  - **Why needed**: Cannot store or serve uploaded files (videos, PDFs, images) without media storage service
  - **Source**: Shared media storage service (S-05)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Providers will proactively check Help Centre for answers before submitting support tickets (requires cultural shift toward self-service)
- **Assumption 2**: Admins will maintain Help Centre content currency by reviewing and updating content quarterly or as platform features change
- **Assumption 3**: Providers have basic computer literacy to navigate Help Centre categories, expand/collapse sections, and download files
- **Assumption 4**: Providers prefer self-service content (FAQ, tutorials) over contacting support for common questions

### Technology Assumptions

- **Assumption 1**: Providers access Help Centre via modern web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions) on desktop or tablet devices
- **Assumption 2**: Providers have stable internet connection to download tutorial videos and PDF guides (minimum 5 Mbps recommended)
- **Assumption 3**: Admins use desktop/laptop computers for Help Centre content management (not optimized for mobile editing)
- **Assumption 4**: Media storage service (S-05) has sufficient capacity to store tutorial videos (assume average 50MB per video, 100 videos = 5GB storage)

### Business Process Assumptions

- **Assumption 1**: Hairline admin team has dedicated content manager responsible for creating and maintaining Help Centre content
- **Assumption 2**: Help Centre content reviewed and updated quarterly to ensure accuracy and relevance
- **Assumption 3**: Provider support team monitors feedback submissions and content gaps to prioritize new content creation
- **Assumption 4**: Service status updates managed by Hairline technical operations team with real-time incident updates during outages

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Help Centre content stored in relational database with separate media storage for files; content served via web API with caching layer for frequently accessed content
- **Content Management**: Use headless CMS architecture to separate content management (admin) from content presentation (provider platform)
- **File Storage**: Large files (videos, PDFs) stored in cloud object storage (S3, Azure Blob) with CDN for fast global delivery
- **Performance**: Implement aggressive caching for published Help Centre content (cache invalidation on content updates); pre-generate content indexes for fast category/tag filtering
- **Search**: Full-text search across all content (title, body, tags) using database full-text indexing or dedicated search engine (Elasticsearch, Algolia) for advanced search features (future enhancement)

### Integration Points

- **Integration 1**: Provider platform fetches Help Centre content via REST API
  - **Data format**: JSON payload with content metadata (title, category, type, publish date) and content body (HTML)
  - **Authentication**: Provider platform uses authenticated API calls with provider session token
  - **Error handling**: If API unavailable, display cached content or "Help Centre temporarily unavailable" message; retry API call on next page load

- **Integration 2**: Admin platform manages Help Centre content via REST API with rich text editor
  - **Data format**: JSON payload with content metadata and HTML content body; file uploads via multipart form data
  - **Authentication**: Admin platform uses authenticated API calls with admin session token and permission verification
  - **Error handling**: If API unavailable, queue content changes locally and sync when API available; notify admin of sync failures

- **Integration 3**: Media storage service (S-05) stores uploaded files
  - **Data format**: Binary file upload with metadata (file name, size, content type, associated content ID)
  - **Authentication**: Signed upload URLs or API key authentication
  - **Error handling**: If upload fails, retry with exponential backoff (3 attempts); if all retries fail, notify admin and save content as draft

### Scalability Considerations

- **Current scale**: Expect 100 Help Centre content items at launch (50 FAQ items, 30 tutorial guides, 20 video tutorials)
- **Growth projection**: Plan for 500+ content items within 12 months as platform features expand and provider base grows
- **Peak load**: Handle 500 concurrent provider accesses to Help Centre during major feature launches or platform incidents
- **Data volume**: Expect 10GB media storage for videos and PDFs within first year (100 videos @ 50MB average, 200 PDFs @ 5MB average)
- **Scaling strategy**: Horizontal scaling of web servers serving Help Centre API; CDN for media file delivery; database read replicas for content queries; cache layer (Redis/Memcached) for frequently accessed content

### Security Considerations

- **Authentication**: Help Centre content accessible only to authenticated provider users; admin content management accessible only to authenticated admin users with Help Centre management permissions
- **Authorization**: Role-based access control enforced at API level (providers: read-only, admins: read-write based on permissions)
- **File Upload Security**: All uploaded files scanned for viruses before storage; file type validation (whitelist: PDF, MP4, MOV, JPG, PNG); file size limits enforced; uploaded files stored outside web root with access-controlled URLs
- **Content Injection**: Rich text editor sanitizes HTML input to prevent XSS attacks; strip dangerous tags (script, iframe) before saving; use Content Security Policy (CSP) headers
- **Audit trail**: All content changes logged with admin identity, timestamp, IP address, and action for security audit compliance
- **Data Privacy**: Provider feedback submissions logged with provider identity for follow-up but not publicly displayed; support requests encrypted in transit (HTTPS)

---

## User Scenarios & Testing

[Continuing with 5 comprehensive user stories as detailed in the complete PRD...]

### User Story 1 - Provider Finds Answer in FAQ (Priority: P1)

A provider clinic coordinator encounters an issue with submitting a quote and wants to find a quick answer without contacting support. They access the Help Centre, browse the FAQ category, find the relevant question in the "Quote Submission" topic, and resolve their issue within 3 minutes.

**Why this priority**: Core self-service use case that reduces support burden and provides immediate value to providers

**Independent Test**: Can be fully tested by creating sample FAQ content, accessing Help Centre as provider, searching FAQ topics, and verifying answer is clear and resolves common quote submission issue

**Acceptance Scenarios**:

1. **Given** provider is logged into provider platform, **When** provider clicks "Help Centre" menu item, **Then** Help Centre landing page loads within 2 seconds showing all 10 categories
2. **Given** provider is on Help Centre landing page, **When** provider clicks "FAQ's" category tile, **Then** FAQ category page loads showing all FAQ topics organized in collapsible sections
3. **Given** provider is viewing FAQ topics, **When** provider clicks "Quote Submission" topic section, **Then** all FAQ items within "Quote Submission" topic expand showing questions and answers
4. **Given** provider has expanded FAQ topic, **When** provider reads answer to their question, **Then** answer provides clear step-by-step resolution with screenshots or examples where applicable
5. **Given** provider has read FAQ answer, **When** provider clicks "Was this helpful? Yes" button, **Then** system records positive feedback and displays "Thank you for your feedback" confirmation

---

[4 more detailed user stories continue here...]

### Edge Cases

- What happens when admin attempts to publish content with missing required fields?
- How does system handle concurrent edits by multiple admins to the same Help Centre content?
- What occurs if provider attempts to download large video tutorial but network connection is unstable?
- How to manage Help Centre content when admin deletes content that is linked as "Related Content" from other items?
- What happens when file upload exceeds maximum size limit (video > 500MB, PDF > 50MB)?
- How does system handle Help Centre content search when search query returns zero results?

---

## Functional Requirements Summary

### Core Requirements

- **FR-001**: System MUST provide Help Centre landing page accessible from provider platform navigation menu displaying 10 main content categories
- **FR-002**: System MUST support 7 Help Centre subscreen types matching FR-032 structure (FAQs with accordion layout, Articles with article layout, Resources with file viewer, Videos with video player, Contact Support with form and tracking, Feedback with form and tracking, Service Status with status page interface)
- **FR-003**: Admins MUST be able to create Help Centre content with category assignment, content type, title, rich text body, file attachments, tags, and publish status
- **FR-004**: System MUST support multiple content types (FAQ, Tutorial Guide, Troubleshooting Tip, Video Tutorial, Resource Document, Policy Document)
- **FR-005**: Admins MUST be able to organize FAQ content into collapsible topic sections with drag-and-drop reordering
- **FR-006**: Providers MUST be able to access Help Centre content in read-only mode with distinct layouts per subscreen type (accordion for FAQs, article layout for guides, file viewer for resources, video player for videos, forms for support/feedback, status page for service status) matching FR-032 Screen 5.1-5.7
- **FR-007**: System MUST support rich text editing for content creation with formatting (bold, italic, lists, links, images, tables)
- **FR-008**: System MUST support file uploads for Help Centre content (PDFs max 50MB, videos max 500MB, images max 10MB)
- **FR-009**: System MUST provide content preview functionality allowing admins to view content exactly as providers will see it in each subscreen layout before publishing (accordion preview for FAQs, article layout preview for guides, file viewer preview for resources, video player preview for videos, status page preview for service status) matching FR-032 Screen 5.1-5.7
- **FR-010**: System MUST support content versioning tracking all changes with admin identity, timestamp, and version notes

### Data Requirements

- **FR-011**: System MUST store Help Centre content with metadata (subscreen type matching FR-032, content type, title, body, tags, publish status, created date, updated date, created by admin, updated by admin)
- **FR-012**: System MUST store Contact Support submissions with metadata (ticket number, provider ID, subject, category, message, priority, attachment, status, submitted date, admin responses, response history)
- **FR-013**: System MUST store Feedback & Suggestions submissions with metadata (submission ID, provider ID, type, title, description, priority, status, submitted date, admin responses, response history)
- **FR-014**: System MUST store Service Status data with metadata (overall status, service components with statuses, incidents with timeline, maintenance windows with schedules)
- **FR-015**: System MUST maintain audit trail logging all content creation, editing, publishing, unpublishing, and deletion actions with admin identity and timestamp
- **FR-016**: System MUST support soft-delete for content (move to "Archived" status) not permanent deletion
- **FR-017**: System MUST store file attachments in media storage service (S-05) with references in Help Centre content records
- **FR-018**: System MUST track content view analytics (total views per content item, views over time) for performance measurement

### Security & Privacy Requirements

- **FR-019**: System MUST enforce authentication for Help Centre access (providers must be logged in, admins must be logged in)
- **FR-020**: System MUST enforce authorization for content management (only admins with Help Centre management permissions can create/edit/publish content)
- **FR-021**: System MUST scan all uploaded files for viruses before making available to providers
- **FR-022**: System MUST sanitize rich text HTML input to prevent XSS attacks (strip dangerous tags: script, iframe, object)
- **FR-023**: System MUST enforce file type whitelist for uploads (PDF, MP4, MOV, JPG, PNG only) rejecting all other file types
- **FR-024**: System MUST encrypt provider feedback and support request submissions in transit (HTTPS) and at rest

### Integration Requirements

- **FR-025**: System MUST provide REST API for provider platform to fetch Help Centre content with authentication, organized by subscreen types matching FR-032
- **FR-026**: System MUST integrate with media storage service (S-05) for file upload, retrieval, and deletion
- **FR-027**: System MUST integrate with rich text editor library (Quill/TinyMCE/CKEditor) for content creation interface
- **FR-028**: System MUST integrate with virus scanning service for file upload security validation
- **FR-026**: Admins MUST be able to view and manage Contact Support submissions with status tracking (Open, In Progress, Resolved, Closed) and response capabilities matching FR-032 Screen 5.5
- **FR-027**: Admins MUST be able to view and manage Feedback & Suggestions submissions with status tracking (Submitted, Under Review, Planned, Implemented, Declined) and response capabilities matching FR-032 Screen 5.6
- **FR-028**: Admins MUST be able to manage Service Status components, incidents, and maintenance windows with status page interface matching FR-032 Screen 5.7

---

## Key Entities

[10 detailed entities as specified in complete PRD]

- **Entity 1 - Help Centre Content**
- **Entity 2 - Help Centre Category**
- **Entity 3 - FAQ Topic**
- **Entity 4 - Content File Attachment**
- **Entity 5 - Content Version History**
- **Entity 6 - Provider Feedback Submission**: Represents feedback submissions from providers
  - **Key attributes**: submission ID, provider ID, feedback type (Feature Request, Bug Report, Suggestion, Other), title, description, priority, status (Submitted, Under Review, Planned, Implemented, Declined), submitted date, admin response, response history, last updated
  - **Relationships**: One provider can submit many feedback items; feedback submissions reviewed by admins; status updates visible to provider in FR-032 Screen 5.6

- **Entity 7 - Support Request**: Represents contact support submissions from providers
  - **Key attributes**: ticket number, provider ID, subject, category, message, priority, attachment URL (if provided), status (Open, In Progress, Resolved, Closed), submitted date, admin response, response history, last updated
  - **Relationships**: One provider can submit many support requests; support requests managed by admins; status updates visible to provider in FR-032 Screen 5.5

- **Entity 8 - Service Status Component**: Represents individual service components for status monitoring
  - **Key attributes**: component ID, component name, status (Operational, Degraded, Down), last updated timestamp, last updated by admin ID
  - **Relationships**: Many components contribute to overall platform status; components affected by incidents

- **Entity 9 - Incident Record**: Represents platform incidents and outages
  - **Key attributes**: incident ID, title, description, status (Investigating, Identified, Monitoring, Resolved), start time, end time, affected services (array of component IDs), timeline updates (array of status changes with timestamps), created by admin ID
  - **Relationships**: One incident affects many service components; incidents displayed in FR-032 Screen 5.7

- **Entity 10 - Maintenance Window**: Represents scheduled maintenance periods
  - **Key attributes**: maintenance ID, title, description, scheduled start time, scheduled end time, affected services (array of component IDs), status (Scheduled, In Progress, Completed, Cancelled), created by admin ID
  - **Relationships**: One maintenance window affects many service components; maintenance displayed in FR-032 Screen 5.7

- **Entity 11 - Content Analytics**: Represents content performance metrics
  - **Key attributes**: content ID, view count, helpfulness rating (Yes/No counts), average time spent, last viewed timestamp
  - **Relationships**: One content item has one analytics record; analytics used for content optimization

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-17 | 1.0 | Initial PRD creation for FR-033 Help Centre Content Management | Claude AI Assistant |
| 2025-12-03 | 1.1 | Major updates to align with FR-032 changes: Reorganized screen specifications to match FR-032's 7 subscreen structure (FAQs, Articles, Resources, Videos, Contact Support, Feedback, Service Status); Added submission tracking management screens for Contact Support and Feedback with status workflows; Added Service Status management interface for components, incidents, and maintenance windows; Updated content creation/editing forms to match provider-facing layouts (accordion for FAQs, article layout for guides, file viewer for resources, video player for videos, status page for service status); Updated preview functionality to match each subscreen layout; Updated workflows to reflect new subscreen structure; Added functional requirements for submission tracking and service status management | AI/Claude |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD Template
**Last Updated**: 2025-12-03
